# SOLONet: Sub-optimal location-aided overlay network for MANETs

Abhishek Patil · Yunhao Liu · Li Xiao · A.-H. Esfahanian · Lionel M. Ni

Published online: 4 January 2007 -C Springer Science + Business Media, LLC 2007

Abstract Overlay networks have made it easy to implement multicast functionality in MANETs. Their flexibility to adapt to different environments has helped in their steady growth. Overlay multicast trees that are built using location information account for node mobility and have a low latency. However, the performance gains of such trees are offset by the overhead involved in distributing and maintaining precise location information. As the degree of (location) accuracy increases, the performance improves but the overhead required to store and broadcast this information also increases. In this paper, we present SOLONet, a design to build a sub-optimal location aided overlay multicast tree, where location updates of each member node are event based. Unlike several other approaches, SOLONet doesn’t require every packet to carry location information or each node maintain location information of every other node or carrying out expensive location broadcast for each node. Our simulation results indicate that SOLONet is scalable and its sub-optimal tree performs very similar to an overlay tree built by using precise location information. SOLONet strikes a good balance between the advantages of using location information (for building efficient overlay multicast trees) versus the cost of maintaining and distributing location information of every member nodes.

Keywords MANET . Overlay . Multicast . Location aware optimization . Service discovery

# 1 Introduction

Mobile ad hoc networks (MANETs) are characterized by mobile nodes and constantly changing network topology. Implementing multicast in such a dynamic environment is a challenging task. A recent survey of the various multicast routing protocols for ad hoc networks is presented in [10]. As pointed out by [28], traditional IP-layer multicast [19, 23, 31] for MANETs have a lot of signaling overhead as it needs to take into account the network dynamics in addition to the (multicast) group dynamics. The widespread deployment of IP multicast has been held back by a variety of issues [11]. Overlay multicast is a new mechanism to support group communication. In comparison to traditional IP multicast, application layer (overlay) multicast relies on the underlying unicast protocols to adapt to the changing network topology. As a result, the application layer has to track only the group dynamic. Due to its ease of implementation and flexibility to adapt, overlay multicast networks (though not as efficient as IP layer multicast) are finding many practical applications in MANETs. AMRoute [7], PAST-DM [14], and LGT [8] are some of the overlay multicast protocols that have been proposed for MANETs. In recent years, we have seen a

A. Patil (-) Kiyon Inc., 9381 Judicial Drive, Suite 160, San Diego, CA 92121 and Department of Computer Science and Engineering, Michigan State University, East Lansing, MI 48824, USA e-mail: abhishek@kiyon.com

Y. Liu Department of Computer Science, Hong Kong Univ of Science and Tech, Kowloon, Hong Kong e-mail: liu@cs.ust.hk

L. Xiao . A.-H. Esfahanian Department of Computer Science and Engineering, Michigan State University, East Lansing, MI 48824, USA e-mail: {lxiao, esfahanian}@cse.msu.edu

L.M. Ni Department of Computer Science and Engineering, Hong Kong Univ of Science and Tech, Kowloon, Hong Kong e-mail: ni@cs.ust.hk

![](images/5c4b6a55a67ae03d0e601c2435b422c9c390d53833546bc56c4215496e0d6559.jpg)



Fig. 1 Overlay tree and it corresponding network layer links

dramatic increase in research interest shown towards context aware computing and location-sensing techniques [4, 16, 17, 26, 27, 32, 40]. Consequently, position based approach for routing [8, 34] is becoming practical.

Figure 1 shows a typical overlay tree with its underlying physical layer links. As seen from the figure, data exchange between member nodes requires traversing other member nodes. This introduces high latency, which increases as the number of member nodes increases. Also, there are several links that carry identical packets (meant for different member nodes). As a result, application layer multicast is not as efficient as IP-based multicast. Recently, in an attempt to improve the efficiency of overlay multicast, researchers have proposed the idea of using location-aware overlay multicast trees [8]. Figure 2 shows such an example. A locationaided tree would keep track of member node’s movement and would be frequently updated to account for any change in the node positions. The nodes that are physically close to each other would be neighbors in the logical tree Fig. 2(c) and the delay at a particular member node will be proportional to its actual distance from the source node. There are several issues with location-aided approach that need close attention. For example, how to effectively distribute the location informa-

![](images/4908aef66b8b62977023d2c5cf07f6e67f0a2df9e06d4481c8aed98efc99c4a1.jpg)



Member nodes Non-Member nodes Physical Links Logical Links

Fig. 2 Random vs location-aided overlay tree

tion of each member node to other members? How precise should the location information be? How often should this information be updated? Chen and Nahrstedt [8] propose two algorithms (LGK and LGS) to build overlay multicast trees using location information. However, their approach involves storing location information of every member node at every other member node and sending location information in every packet header or periodic location update packets. Location broadcast is a costly affair and if every node starts to broadcast its current location information, then it would quickly lead to the broadcast storm problem [6, 35]. The method proposed in this paper builds location-aided overlay trees without requiring every member node to know the location of every other node, or doing costly location update broadcasts periodically. Another aspect of LGT [8] is the use of exact location information for each node. Intuitively, precise location information would lead to a better overlay tree. However, obtaining exact location of a node is a difficult task, especially in indoor environments where ad hoc networks are usually implemented. Frequent updates would be necessary to maintain the accuracy of this information. As the node number and mobility increases, the update frequency would exponentially increase. There is a tradeoff between the advantages of building a location-aided overlay tree versus the distribution and precision of this location information.

This paper presents an extension of our earlier work SOLONet [29]. In SOLONet, the physical topology is partitioned into smaller areas (cells) having a certain geometric shape (e.g., triangle, square, hexagon, etc). Figure 3 shows an example of such a partitioning. The idea is to make location updates event-based. A node will report a change in its location only when it crosses border to a neighboring cell. While in a particular cell, the node will report the center of that cell as its location. A leader node is selected in each cell to localize certain operation, aid in service discovery and to reduce the number of broadcast messages. A node wishing to form or join an existing overlay network (for a particular service) would query its local leader instead of broadcasting the query to each node in the network. Using ns2 (for simulations), we compare the performance of our design with an ‘optimal’ overlay tree. We also evaluate the scalability of SOLONet and take a closer look at its performance for different cell areas and member size. Also, we study the impact on performance for different (location) update intervals.

![](images/1341fdf36e99b99e5e93f06c6e5f77755b2c3be545ba2597420ee1cf9464be0a.jpg)



Fig. 3 Entire topology partitioned into smaller cells

The rest of the paper is structured as follows. Section 2 summarizes previous work on overlay multicast and briefly compares and contrasts our approach with some of the protocols proposed earlier. Section 3 presents an in-depth description of our design. Section 4 presents a detailed analysis of our leader selection algorithm. Section 5 looks at our SOLONet implementation with the help of an example. Section 6 presents our simulation results. Finally, Section 7 concludes the paper and presents directions for future research.

# 2 Related research

Several overlay multicast protocols [3, 5, 8, 9, 14] have been proposed and studied in recent past. Many of them have addressed the issue of building an efficient overlay multicast tree. The NICE [5] project aims to address the issues involved in data stream applications—real-time data applications that are characterized by a very large set of receivers having low bandwidth. NICE arranges the end host into sequentially numbered layers, which defines the multicast overlay data path. The basic operation of NICE is to create and maintain a hierarchy consisting of a set of end hosts. The members at the top of the hierarchy maintain state about O(log N) other members, where N is the number of nodes in the network. Member nodes keep information about members ‘near’ to them in the hierarchy and have limited knowledge about other members. This structure helps localize the effects of a member failure. Hosts at each layer are partitioned into clusters that have a cluster leader. Unlike SOLONet, the leader selection in NICE does not make use of any location or the battery strength information. In NICE, each cluster size depends on the set of hosts that are close to each other; whereas, in our approach, the cell edges (physical boundaries) define the association to a cell. NICE is not defined for MANETs and hence it does not take into account node movement.

Ad-hoc multicast routing protocol (AMRoute [7]) makes use of user-multicast trees and dynamic logical cores to build a robust multicast network. It creates per group multicast distribution tree using unicast tunnels between group members. The bidirectional tunnels are created between member nodes that are close to each other (neighbors in the multicast tree) to form a virtual mesh. From this mesh, a subset of links is used to create a multicast distribution tree). The path taken by the unicast tunnel can change with the changing network topology without affecting the user multicast tree. Similar to SOLONet’s leader nodes, AMRoute maintains a logical core node. However, unlike SOLONet (where there are several leader nodes present in the network, in case of AMRoute), there is one logical core node for every tree. The core node is responsible for mesh and tree creation. Non-core members only act as passive responding agent. The logical core is also responsible for discovering new group members, creating, and maintaining the multicast tree for data distribution. The core can migrate dynamically depending on the group membership or network connectivity. Having one core per group has the advantage of reducing the signaling overhead. A group may have more than one core for a short period. In case of more than one core in the same group, the core resolution algorithm resolves the conflict by assigning the node with the highest IP address as the core node. SOLONet follows a similar approach where the leader node conflict is resolved by choosing the node with the lowest IP address. The same algorithm can help in the assignment of a new core incase the earlier core node leaves the group or is unavailable due to link or node failure. To avoid the sequence number wrap-around problem, AMRoute requires that the ad hoc network multicast group have a certain validity period.

Progressively Adaptive Sub-Tree in Dynamic Mesh (PAST-DM) [14] is an overlay protocol that constantly adapts to the changing network topology and attempts to generate an optimized overlay multicast tree. It tries to eliminate redundant physical links so that the overall bandwidth consumption of the multicast session is reduced. The protocol constructs a virtual mesh that connects all member nodes.

Each node implements a neighbor discovery protocol using the extended ring search algorithm with an upper limit on the search radius. The nodes periodically exchange link state information with their neighbors in a non-flooding manner. With several such exchanges, a node’s link state will be carried over to faraway nodes. By looking at the link state of each node, a node gets a view of the entire topology. This information is used (by every source node) to build a Source-Based Steiner tree. The source node puts subgroup information into data packet header before unicasting it to its children. A subgroup forms a sub-tree rooted at one of the first level children. Each child then runs the Source-Based Steiner tree algorithm in order to deliver the data packet to its subgroup. This might be a problem since it puts a lot of computing overhead on each member node. Also, the packet (header) size would be large in case of higher group membership. Another issue is during the link state broadcast. The authors suggest that with random offset, a broadcast storm problem can be avoided. However, it is not clear if random offset method would work if there are large number of member nodes.

Location Guided Tree (LGT) [8] is a small group multicast scheme similar to DDM [20]. It builds overlay multicast trees (in MANET) using geometric distance as an approximation of link costs. The scheme proposes two tree construction algorithms: greedy k-ary tree construction (LGK) and Steiner tree construction (LGS). The algorithms are based on the assumption that longer geometric distances require more network-level hops to reach destination. LGS constructs the Steiner tree using geometric length as link costs. In case of LGK, the source node selects k nearest neighbors as its children and partitions the remaining nodes according to their distance to the children nodes. Each child then selects k-nearest nodes as its children and continues with the tree expansion. In the LGT approach, each member node is assumed to have knowledge of its geometric location. Every node includes its current location information in each data packet header. If a node doesn’t have data packets to transmit for a long time, it sends periodic update (null) packets carrying its location information in the header. Each node also maintains location information of every other member node in the group. This might be a problem in case of high group membership. Similar to LGT, our approach assumes that each node knows its geometric location. However, in SOLONet, the location updates are event based and nonperiodic. Besides, nodes in SOLONet do not report their exact location; instead they report the center of the current cell as their location. Also, only the source node maintains location of each member nodes in the group and all updates from member nodes are directed towards the source node. LGT is a small group multicast scheme while, SOLONet is highly scalable due to its localized service discovery broadcast.

# 3 Design of SOLONet

We begin the description of our SOLONet design by first discussing the various components (like location computation, cell area, cell shape etc) involved.

# 3.1 Location and geometry identification

In SOLONet, the entire topology is partitioned into smaller cells (Fig. 3). We assume that each node has knowledge of the cell structure for the given topology. Organizers of special events (such as games or concerts), where overlay multicast may be implemented, may distribute a coordinate file or a hash function that defines the geometry of the topology. Mobile users, who wish to participate in the multicast network may download the coordinate file (or hash function) from the organizer’s website. An alternative approach would be to automate this process so that the nodes obtain the coordinates (topology map) at startup during IP assignment (or they request a copy from a neighboring node that has already joined the network). We also assume that each node knows its current location. This information may be relative to some reference point in the topology and can be computed using the hash function or the coordinate file. To monitor their movement, nodes may use location sensing techniques like GPS in outdoor environment or one of the several indoor location sensing techniques [1, 4, 16–18, 26, 27, 33, 40] available.

# 3.2 Initial setup

When the ad-hoc network comes online for the first time, it will run some form of an IP allocation algorithm (e.g., Prophet Algorithm [41]) to get a unique IP address. This IP address will be used to identify each node. In the next few subsections, we discuss some characteristics of the partitioned topology.

# 3.2.1 Shape of the cell

Our design doesn’t put any restriction on the shape of the cells. In theory, the topology can be partitioned into several (non-overlapping) cells of any shape. However, by using repetitive regular cell structures, we can make use of the geometric properties for that shape. Each shape will have its own advantages. A hexagon can closely resemble a coverage area for a given cell, while a square is easier to divide into smaller areas if the density of nodes in a cell is high.

# 3.2.2 Size of the cell

Our design requires that all nodes in any cell are one-hop neighbors of each other. In case of a square cell, for example, nodes at the two ends of the diagonal are farthest apart. Therefore, the size of a square cell should be such that the length of its diagonal is less than the coverage radius. This will allow any node in the cell to directly communicate with any other node in that cell. Similar calculations can be done for cells of other shapes using the geometric properties for that shape. Later in the simulation section (Section 6.3), we have a detailed discussion on the effect of cell size and node density.

Table 1 Typical state table at each local leader node 

<table><tr><td>Node ID</td><td>X</td><td>Y</td><td>Type of service</td><td>Battery strength</td><td>Time in cell</td></tr><tr><td>12</td><td>76.22</td><td>108.37</td><td>Gateway to Internet</td><td>50%</td><td>4 min 27 sec</td></tr><tr><td>57</td><td>73.76</td><td>111.29</td><td>Live Surgery Video</td><td>89%</td><td>1 min 12 sec</td></tr><tr><td>23</td><td>75.32</td><td>105.12</td><td>Medical Record Files</td><td>24%</td><td>4 Sec</td></tr></table>

# 3.2.3 Cell size and transmission range

A major factor that needs to be considered when deciding the size of the cell is the coverage area for the technology being used to implement the system. G. Anastasi and group [2], through various experiments, have shown that in case of 802.11 b ad hoc networks, the coverage area for a node is around 100–130 m at the lowest data rate − 1 Mbps. Their study also reveals that the transmission area and throughput depends on the height of the transmitter with respect to the receiver. Similar results may be used for other networks in order to determine the optimal cell size. Our design criteria states that each node in a cell should be able to communicate with every other node in the same cell—meaning the communication has to be single hop with nodes in the same cell. In case of 802.11 b technologies a cell size of $7 5 \times 7 5 \mathrm { m } ^ { 2 }$ (or $1 0 0 \times 1 0 0 \mathrm { m } ^ { 2 } )$ may be used in light loads. If the density of a node is very high, $5 0 \times 5 0 \mathrm { m } ^ { 2 }$ may be a good choice. Similar choices can be made for other wireless technologies.

# 3.2.4 Center of the cell

Since the cell topology is known to each node, computing the center of its current cell would not be difficult (using some geometric property of the cell’s shape). Each node maintains a cellID. During the startup phase, a node checks its position to determine which cell it is current in. This information helps the node to set its cellID parameter. The CID would change when the node moves to a different cell.

# 3.3 Member nodes and leaders

Each cell would have a local leader to assist in the service discovery (and tree building) process. This section gives an overview of the responsibilities of a member and a leader node.

# 3.3.1 Leader responsibilities

Member nodes constantly update their local leader with information about their location (and service type, battery strength, etc). A leader node maintains a table containing information about each node in its cell. Rows in such a table may look like the ones shown in Table 1. The leader purges a node’s entry after it receives a disconnect message from it. The disconnect message may be sent either when the node is gracefully shutdown or has moved to a neighboring cell (and associated with the local leader in that cell). The leader node periodically broadcasts a beacon packet to all the nodes in its cell. This beacon message aids in leader selection process, serves as a feedback to the nodes and indicates that the leader node is alive. The details of the beacon packet are discussed in Section 4.2. Figure 5 shows a typical communication time-line in every cell. Storing service type of each node is important for service discovery by other nodes in the network. The presence of leader nodes helps in localizing certain operations and limiting the service discovery broadcast to a small fraction of nodes.

Additional responsibilities of a leader could be time slicing of node transmissions or cell splitting. If the node density in a cell is higher than a certain threshold, the leader may assign time slots to each node to avoid collisions between their transmissions. Leader nodes may coordinate with neighboring leaders to assign skewed transmission timeslots so that there is minimal collision between the two cells. These time slots may be carried in the beacon message sent by the leader (Fig. 5). Another alternative to solve the high cell density problem could be cell splitting. This paper does not cover detail discussion on cell splitting or time slot assignment in this paper. Several papers in the literature that explain how this can be carried out.

# 3.3.2 Node responsibilities

When a node first comes online, it waits and listens for the beacon message from the leader node. Once it hears the beacon, it knows who the local leader is. The node provides the leader with information about its current location, battery power, and services that it can provide. After the first update, all subsequent updates to this leader carry only the battery and current location information.

![](images/50079f1452c3b36e0c32e33945f7b737fc533ef1d959a4b5cce59cb4dcb3bf74.jpg)  
a) A member node cross the border into a neighboring cell

![](images/897603ea98aea5f35b1a82bbf801193a3eba0130da75479e853eb78079ca6684.jpg)  
b) It maintains its association with the old leader till it hears a beacon from the new leader.

![](images/1dd3919a6016f9a6192e3d3e51a66e2f10b5a88e0bb00cde6d9ae14be3065cdd.jpg)  
c) After hearing the beacon, it associates with the new leader

![](images/8bde5e5b9103f40fb756d0543384090f2f9d9748ee45797eeb6849443458d88d.jpg)  
d) After successful association, it disconnects with the old leader.

Fig. 4 Node association with a new leader after crossing cell boundary   
![](images/2fc6fa2d570da380096b0dabc7b6839e628ca7956b5c03d6bd2d8f6616deabfd.jpg)



Fig. 5 Time-line showing all the communication happening in a cell (during normal operation)

When a node enters a new cell, it defers its disconnect message to the old leader till it is able to connect to the leader in the new cell. The node waits for a time equal to the periodicity of the beacon in an attempt to know who the local leader is Fig. 4(a). After receiving the beacon message, this node would know the leader’s IP address or other relevant details Fig. 4(b). The node would then send an association message to the new leader. The scenario where the leader’s beacon message is lost or the neighboring cell has no leader is discussed in later sections. After successfully associating with a new leader, the node disconnects from the old leader Figs. 4(c) and (d). This deferred disconnect procedure ensures that a node is always connected to at least one leader. Since the node has just crossed the cell boundary, it is most likely going to be in the coverage of the old leader. After association with the new leader, the node provides it with information about its current location, battery power, and services that it can provide. Similar to the startup case, after the first update, all subsequent updates to this leader carry only the battery and current location information.

The next section gives detail description of the role a leader node plays in service discovery and how a location-aided overlay tree is formed.

# 3.4 Service discovery

When a member node wishes to get a particular service, it would query its local leader. The node may provide the address (if known) of the source node that provides the requested service. For example, there may be a few nodes in the network that act as gateway nodes and provide access to the Internet. A node that wishes to access the Internet may request its local leader to find a gateway node. If the requesting node knows the IP of a gateway node, it may provide the IP along with its request to the local leader nodes. After receiving such a request, the leader node checks its local table (similar to Table 1) to see if the source node is in its list (i.e., in the same cell). If the requested node is not found locally, the leader forwards the request to its neighboring leaders Fig. 6(b) using the expanded ring search algorithm [30]. The leader first forwards the request to its immediate neighboring leaders. If that fails, it increases its search space (expands the search radius) and forwards the request to the next set of leaders which are further away. It must be noted that this message exchange between leaders may be multi-hop communication (and might involve non-member nodes) as far away leader nodes will not be one hop neighbors. Since the service discovery message is exchanged only between leader nodes, it can be viewed as a multicast between leader nodes. The depth of this multicast tree depends on the cell in which the requested node is found. In its message, the leader node provides IP address and the cell ID of the requesting node. We have tried to keep this message as small as possible by having only two items (IP and CID) in the message. Since there are very few leader nodes in the entire network the overhead will be very low. Each leader node, upon receiving the service discovery message, checks its local node list to see if the requested (service) node is in its cell. If the requested node is found, then the leader forwards the request (message) to that node (Fig. 6) and sends a positive ACK to the requesting leader.

In the event that the requesting node doesn’t get any response for a timeout period, it resends its request. Certain request may not generate any reply either because there is no node in the entire network that can provide the requested service or because the leader in the requested node’s cell is dead (Fig. 10). Both of these problems can be solved if the timeout period follows an exponential back-off scheme. Such a scheme would give enough time for any leader selection process, which may have started during the service discovery process, to complete. The system can be configured so that after a certain number of timeouts, a node stops making request for that service.

Fig. 6 Building a location aware overlay tree   
![](images/0987eeb5a8d2cc0883122ee9734a2f0cce23f0df4da3b745e10f08bb54156c37.jpg)



a) A node wants to join an existing overlay

![](images/ab05e9974f23b9507d99cba72832a417830b4da9b2860b14b9f645d7460454bf.jpg)



b) Leader broadcasts the request to other

![](images/e3726cadf1af347692df9517c27f9d72be60dfadea790b786298f30b10be059d.jpg)



c) Source node located. Source contacts the requestor and gives address of the nearest node to connect to.

![](images/ecc6f095bb6a8a2f52d87b9ff7e7042bd81c75c4a727a61743a1de82d2e6cc93.jpg)



d) New overlay tree.   
Leader nodes   
. Member nodes   
Requesting node   
. Source node

# 3.5 Joining an overlay tree

The node that provides services (like data storage, access to Internet, computing resources etc) to member nodes in a multicast tree is referred to as the source node. This source node would usually have more resources at its disposal. It is the root of the multicast tree which is built for providing a particular service. The source node is responsible for building and the growth of the multicast tree. It stores the CIDs of the member nodes that it is currently serving. When it receives a request for service (from a new member), it extracts the CID (from the request message) and finds the position of the requesting node. The position is assumed to be in the center of the requestor’s cell. Simulations in Section 6.1 investigate the performance with this assumption. The source node now checks its internal tree-table to find node(s) that may be in the same cell or neighboring (closest) cell as the requesting node. It now contacts the requesting node and provides it with the IP address of a member node nearest to it. The source also provides appropriate information to this designated ‘nearest’ relay node about the requesting node Fig. 6(c). With this information, the requesting node can now connect to a near-by (physically close) member node, which would in turn provide the required service Fig. 6(d). As our simulations confirm, the latency with this approach is much lower compared to the case where a source node randomly selects a node in the tree for the requestor to connect to.

In case of prioritized overlay multicast [38], the source node will also provide information about the priority of the service that it provides. This would help in the formation of a prioritized overlay tree. At the time of request, the requesting node may be part of some other group(s) having a different priority. For example, in a particular hospital, all doctors, nurses or resident students doctors may have their own category (viz doctor net, nurse grp, student org) in addition to a common (low priority) group called hospital net. In an emergency, a group of doctors, nurses, and residents may form a high priority network to address a specific patient case. Detailed discussion on priority trees and their formation can be found in [38].

# 3.6 Degree bounded locations based tree

Consider an example of building a simple location-aided (sub-optimal) tree using the model Fig. 7(a) described in the previous section. The request to join will propagate through leaders until it finally reaches the source node. The source node now looks at its internal topology map and finds a member node that is nearest to the requesting node. This ‘plain’ approach may lead to the case where one or more of the relay nodes become a single point of failure. In addition, it may happen that the packet delivery load may not have been evenly distributed amongst the relay nodes creating several connections at a node; thus making it a bottleneck. More connections mean larger state-tables and higher power consumption. In short, this would lead to faster depletion of resources (battery power, memory, etc) at the bottleneck node. It may also cause collisions between the different connections directly affecting the throughput. To eliminate the weakness of such a ‘plain’ tree, we propose a degree bounded architecture. In this approach, after a source node receives a request, it looks at its internal topology map and finds a set of member nodes that are near to the requesting node. This set will consist of nodes that are in the same cell, immediate neighboring cell, and up to three cells away from the requesting node. In order to keep the search result small, we chose to look up to three cells away. This default setting may be changed in a dense topology where the multicast tree may have several member nodes. In such a case, the source may consider member nodes that are in the same cell, immediate neighboring cell, and one cell away. Restricting the ring of nearest neighbors will keep the found set as small as possible.

Fig. 7 Degree bound location aware tree   
![](images/eaa0072d5078b890c39f7f109027b148cb9c242733cbba2d043eea63f2324479.jpg)



0   
Source Node

Bottleneck Node   
![](images/ee8e6f3815d9264997854f20a1b7e8e6b01c58d7cb75b05a2b25903e30059928.jpg)



Member Nodes   
(a)   
(b)

The source now sorts this found set by assigning weights proportional to the degree (number of connections) of the node and its ‘closeness’ to the requesting node. The total weight $( W _ { T } )$ for a node is calculated such that a node closer to the requesting node would contribute positively while a node with high degree node would tend to bring down the $W _ { T }$ value. Table 2 shows one such calculation. In this example, nodes in immediate neighboring cells are assigned a neighbor weight $( W _ { N } )$ of 1. The $\mathsf { W } _ { N }$ value for a node is higher if it is farther away from the requesting node. The degree weight $( W _ { D } )$ of a node is directly proportional to its current degree. In our example, we have kept the $\mathrm { W } _ { D }$ of a node equal to its current degree. To make the process of relay node selection light weight, the computation of $\mathrm { W } _ { T }$ is kept as simple as possible. The source selects the node with the highest $W _ { T }$ value as the relay node and provides the requesting node with its address. The requesting node can now connect to this node. This approach would ensure that a near-by node with little or no connections get selected as relay node for a new connection Fig. 7(b); thus evenly distributing the load. A similar algorithm can also be used when the source node decides to reorganize the multicast tree to compensate for changes in member node positions due to its mobility.

# 3.7 Event-based update

Every source maintains a list of member nodes that it serves (either directly or through other members). A member node updates the source with its new location (CID) only if it changes its cell. This approach reduces the amount of location updates and the associated overhead. The updates are sent to the source in-band along with the ACK packets. The source node can alter the tree structure if the location update(s) indicate a major change in the topology. Although the resulting (location aware) tree is sub-optimal, one can appreciate the gains of this method compared to the expensive broadcast approach which is used when precise location information is needed for tree construction. Simulation results in Section 5 show that this approach pays a very little performance penalty compared to an approach where exact location information is used.

Table 2 Weight calculation for a requesting node 

<table><tr><td>Node ID</td><td>Location</td><td>Relative position</td><td> $W_{N}$ </td><td> $W_{D} = Degree$ </td><td> $X = \sqrt{(W_{D}^{2} + W_{N}^{2})}$ </td><td> $W_{T} = (X)^{-1}$ </td></tr><tr><td>24</td><td>Cell (4E)</td><td>One cell away</td><td>2</td><td>2</td><td>2.83</td><td>0.35</td></tr><tr><td>8</td><td>Cell (2B)</td><td>Two cells away</td><td>3</td><td>2</td><td>3.87</td><td>0.25</td></tr><tr><td>17</td><td>Cell (2F)</td><td>Neighboring cell</td><td>1</td><td>4</td><td>4.12</td><td>0.24</td></tr></table>

# 4 Leader selection for cells

Before we get into the details of the leader section process, the next two sub-sections look at some of the arrangements in our design that aid the leader selection process.

# 4.1 Responsibilities of leaders

Every leader performs activities that can aid in the selection of a new leader in case of its failure. In addition to the location and the service information, each leader also maintains battery status and the time a particular node spent in its cell (Table 1). Weights are assigned to the battery strength, timein-cell and node’s current location information. The entries in the list are sorted according to the result of this weighting function. The first two nodes or the top 10% nodes (whichever is greater) in this sorted list are called candidate nodes— meaning that these nodes are potential candidates for leadership in case the current leader fails. Listed below are some important parameters used to choose the candidate nodes.

# 4.1.1 Time information

It has been observed in [12] that hosts that have been stationary for a period of time are more likely to remain stationary as compared to those currently in motion. Thus, choosing a node that has shown little movement or no movement as the leader would greatly increase the chances that it would stay in that cell for a long time.

# 4.1.2 Battery strength

A leader has a lot of responsibilities and this demands battery power. A node which has good battery strength should be selected as the leader, so that it can perform the leadership responsibilities without interruption for a long time.

# 4.1.3 Location

A leader situated more or less towards the center of the cell can serve all the cell nodes with little delay. Even if this node were to be in motion, it would take a longer time for it to move out of the cell due to its distance from the cell’s periphery.

The next section shows how the sorted list is made available to all the nodes in the cell through the beacon message.

# 4.2 Beacon message

Every leader periodically broadcasts a beacon packet containing a sorted list of nodes in its cell. These beacon messages serve three purpose.

# 4.2.1 Leader’s heartbeat

Beacon is a way for the leader to tell the other nodes that it is alive. If nodes do not receive beacons for a pre-configured timeout period, they would suspect that the leader is no longer available. The use of timeout will help prevent false detection. A beacon packet may be lost due to noise, multi-path fading or collision with some other transmission. Noise and fading depend on environmental conditions while collision (although rare) may depend on density of member nodes. Collision can be reduced by assigning time-slots to each node. The timeout value is not fixed as it depends on the above factors (noise and collision rate in that environment). It will be available to the nodes at start up when they acquire the topology coordinates (or hash function). The leader node may become unavailable for the following two reasons. The user ‘pulled the plug’—turned off the device in an unconventional manner (e.g., suddenly removed the batteries). In such a scenario, the leader node would die without informing any other node. The other case is when a leader sends a message saying that it is stepping down but the message was lost (perhaps due to noise or collision). The use of periodic beacon will help detect the above two scenarios.

# 4.2.2 Aid in leader selection

The beacon message contains the sorted list of nodes (Fig. 8). Leader failures are very rare; however, in case the current leader fails, all the nodes would detect the failure after certain number of beacon messages are missed by the leader. The nodes would then examine the sorted (node) list that came in the latest beacon broadcast. The first candidate node has to acknowledge that it is taking leadership before the next beacon period. If it fails to do so, the second candidate node sends a broadcast declaring itself as the leader. The possibility that both nodes become unavailable at the same time is very rare and if it happens, then after another timeout, the next candidate node in the sorted list takes over the leadership. One of the responsibilities of the new leader is to provide its IP address information to the leaders in the immediate neighboring cells.

![](images/83c994a976a221ab7b97e5ec7e2c83abafd9cee1ba21094e78d0dd9829320e21.jpg)



Fig. 8 Beacon message from the leader node

# 4.2.3 Feedback to each node

The beacon message can serve as a feedback to each node to indicate that its message (containing location and battery information) reached the leader without any error. The beacon message would help identify the IP address of the new leader node when a node crosses over into a new cell. In case of a crowded cell, the beacon may also contain the time slots telling each node when to transmit its information thus to avoid collisions between two (or more) nodes. Implementing slotted transmission in a non-dense cell is optional. Nodes can also use the beacon to synchronize their clock with the leader node.

# 4.3 Hello!! Anybody home?

This section describes a worst case scenario. When a node crosses border and enters a neighboring cell, it maintains its association with the old leader and waits for the beacon from the new leader. What if there is no leader in the new cell or if the leader there died? In our design, the node waits a little longer than the timeout period mentioned above. This would give other nodes (originally present in that cell) enough time to take over the leadership. After this long wait, if there is still no sign of a beacon from a leader, the node assumes that the neighboring cell was empty—neither the leader nor member nodes were present. The node now broadcasts a message containing its IP and its desire to become the leader Fig. 10(a). Since the cell size is such that any node in that cell will hear this broadcast, the node waits for a small timeout period for response from any other node that might recently enter the cell Fig. 10(b). If there was another node that entered the cell at approximately the same time, the node with the lower IP would take over the leadership. After the node has taken the leadership responsibility, it sends a disconnect message to the old leader. During this leader election process, the node was still associated with the old leader. Since the node has recently crossed the border, the inaccuracy in its location information would be close to the location inaccuracy for a node in the older cell, which is near the border of the cell.

# 4.4 Initiation of leader selection

There are three scenarios when a leader selection is required as described below:

# 4.4.1 When the network first comes online

This scenario is similar to the case where a node has entered a cell with no leader. We follow the same leader selection procedure described in Section 4.3 and choose the node with the lowest IP as the local leader. Figure 10 explains this procedure. The first leader may not be the best leader in terms of battery power, location and other factors. However, one of the responsibilities of the leader node is to find a good replacement leader. Thus, the subsequent leaders would be wisely chosen based on the available information.

# 4.4.2 Leader wishes to give up leadership

There can be different cases that may cause a leader to give up its leadership—proximity to the cell boundary, running low on battery or the user has gracefully switched off (shut down) the mobile device. After it has decided to quit, the leader sends a broadcast message informing all the nodes. One of the candidate nodes takes over the leader responsibilities.

# 4.4.3 Exceptional cases—rare in occurrence

Leader’s quit message was lost due to collision or noise or the user switched off the device in an unconventional manner. Both these conditions are seldom possible and would be detected by the absence of beacon messages for a timeout period. In this scenario, one of the candidate nodes takes over the leadership responsibility. The candidate node list will be available to all the nodes from the leader’s previous beacon message. Figure 9 shows a time of events that happen after a leader’s sudden death.

# 5 Implementation by example

In this section, we provide implementation details for our SOLONet concept with the help of an example. We consider the case of a streaming application. The method shown in this section is just a guideline to provide some basic architecture over which an actual system can be designed. An actual implementation may as well be a complete deviation from the method proposed here. Since a streaming application provides stricter design constraints, a non real-time application can easily work with this implementation. We propose to use TDMA based MAC (Fig. 11) for our SOLONet system. In a regular 802.11 network, the communication between nodes is CSMA/CA based. However, this method does not provide 100% guaranteed delivery. Since we want our control messages (carrying various information to and from between the source node and the rest of the member nodes) to be guaranteed in order for the proper working of the system, we reserve a special slot for control signaling.

![](images/bd60a8547ba8822d23b7b7b9d224087643afa6cda60011d3e3de2745465cdb43.jpg)



Fig. 9 Communication time-line— failure of a leader and selection of a new leader

![](images/f07f92151e571b43f5a5cf9587f4c5f3d91ea0e352c407732ef3e632d4977dec.jpg)



(a)

![](images/db8a82c18335b03db967e5b373b769a72b0b36bf59430a4feebfa1b03493e024.jpg)



(b)

![](images/268f47e3701a1504a973ab51241f9a409caa2a37468f9d2db69fd735bffac6e4.jpg)



(c)

Fig. 10 Leader selection during initialization or when no leader is present in a new cell   
Fig. 11 TDMA based MAC for ensure guaranteed signaling   
![](images/eb8935a6cc87788239425d437217d518982a57dd4f07cd3efcf51143c3aa7392.jpg)



The rest of the time is used for regular packet transmission (CSMA/CA). The MAC is designed such that the control messaging is guaranteed. This will ensure that important messages (tree construction or new connection) from the source node (as well information from member nodes regarding their location and outgoing degree) are never lost. The control signal may also contain information for node synchronization and other activities. The information gathering mechanism (where location information and outgoing degree information from member nodes is collected by the source) can be either proactive (poll based) or reactive (member node sends a message when there is any change).

All the member nodes would have a finite buffer to hold the data that they receive from their parent node. In case of non-real time application, this helps in retransmissions while in real-time applications (where there is no ACK or retries involved), this buffer serves to reduce jitter and latency related discontinuities in the play back. This assumption is not unrealistic because most modern applications that are capable of playing real-time data (e.g. Realplayer, Quicktime or Windows Media player) use buffering during their play back. As a side effect, this buffering will also help take care of any latencies that may be introduced due to the multi-hop nature of the system. Since the multicast tree is location based, the latency involved would be low (as seen from the simulation results in the next section). In addition, node movement would not be a major concern because all the updates (and tree re-constructions) are event based. Therefore, the effect of node movement would not be felt until the tree is re-arranged.

In order to have a smooth transition to the new allocation, our system enforces a rule whereby it is the responsibility of the parent node to finish the current buffer transmission to it child nodes before it begins to use the new tree structure. Since our system is location based, it is easy to see that even when the tree is re-arranged, it would not result in a major restructuring (or reconnections) between nodes. Overlay multicast works at the application layer and hence, the destination address on each packet would come from the higher layer.

Fig. 12 Tree re-construction and node connectivity   
![](images/26383ac955f989cc548d5b71d10b534d5ede9cc141b076e40e73cfe368604c5a.jpg)



Member nodes Non-Member nodes Physical Links Logical Links

As a result, a packet meant for a child node (from a parent member) would not be lost even if the tree is reconstructed. In the end, the underlying unicast connection between the two member nodes would handle the delivery of the packet. In Fig. 12, the tree reconstruction results in node D changing its parent from B to C. As a result, node B is responsible to finish all the buffered data for node D after the tree rearrangement. The underlying unicast protocol would ensure that the buffered packets at B would find their way to node D.

# 6 Simulations

Simulations were carried out using ns2.26. As of this writing, ns2 doesn’t have any extension for simulating overlay multicast in MANETs. With the help of C-programming and bash scripting, the traffic pattern generated by CMU’s cbrgen utility was modified to represent a location-aided overlay network. The Prim’s algorithm was used to generate the multicast trees. The distance of the nodes was used as the weight in calculating the MSTs. The setdest utility was used to generate different node positions and movement patterns. The nodes in the simulation move according to the ‘random waypoint’ model [21]. According to the model, when the simulation starts, each node is stationary at a particular location in the specified area for a time equal to the specified pause time. After the pause time expires, the nodes select a random destination within the given area and start to move with the maximum specified speed (during the creating of the scenario file). After reaching the destination, the nodes stay stationary for a time equal to the pause time and select another destination and proceed towards it. It is easy to see that smaller pause time means higher mobility. For all the simulations, DSR was the underlying unicast protocol. Tworay ground model is used as the radio propagation model. We use the IEEE 802.11 DCF as the MAC protocol.

The first set of simulations compare an optimal tree (which is built by using precise location information of member nodes) and our proposed sub-optimal (SOLONet) overlay tree. The optimal tree that we generate is similar to the tree generated by the LGT approach (except for some of the packet level optimizations suggested by LGT). This optimal tree utilizes exact location information and builds a Steiner tree where the link cost is the geometric distance between the nodes. In case of SOLONet tree, nodes report the center of their current cell as their location. Therefore, SOLONet’s Steiner tree is not built with precise location information. This comparison is done for two different areas: 500 × 500 m2 and 800 × 800 m2. The second simulation set aims to show the scalability of our design. We compare the performance for 10, 15, 20 and 30 member nodes. The third simulation set compares the performance for difference choices of cell area and for different number of member nodes. We compare the performance for 25 × 25, 50 × 50, 100 × 100 125 × 125 and 250 × 250 m2 for a topology of 500 × 500 m2. In all the three scenarios, the file size used for transfer is 50 KB and the packet size is 512 bytes. During our initial rounds of simulations, we had tested the performance with various file and packet sizes. Our experiments showed that while the completion time showed a linear increase when the file size was increased, increasing the packet size caused a proportional (not necessarily linear) drop in the completion time. The 50 KB-file and 512-packet size were chosen for ease of simulation. In all the simulations, the ‘Completion Time’ is the time it takes for all the nodes to receive the 50 KB sent by the source node. Completion time indicates the latency in the network. For example, the total latency for a given network (or a multicast tree) can be expressed in terms of the highest of all the completion time values for its node. A network with lower completion time is better since its overall delay is small. The completion time value will greatly depend on how well the tree is constructed. Completion time will depend on the delay-distance between the source and the farthest leaf. This is the same as the eccentricity1 of the source node. In this paper, we use completion time as our performance metric.

![](images/7bdf97685db5081a2bc64a863d9672987b92d054a764101aa9ac4e26ae343f79.jpg)



![](images/86fa289d711690ebf4c50f9eba05f710b6b6306461640784bc6312c0a19417a9.jpg)



Fig. 13 Comparison between accurate location information and location reported as the center of the cell

Table 3 t-Test comparison between optimal and sub-optimal 

<table><tr><td rowspan="2">Simulation area</td><td rowspan="2">p-value</td><td colspan="6">Update time</td></tr><tr><td>5 Sec</td><td>10 Sec</td><td>20 Sec</td><td>40 Sec</td><td>70 Sec</td><td>100 Sec</td></tr><tr><td rowspan="2"> $500 \times 500$ </td><td>1-tail</td><td>7.24 e-06</td><td>0.000134</td><td>0.003781</td><td>0.001651</td><td>0.001818</td><td>0.023289</td></tr><tr><td>2-tail</td><td>1.45 e-05</td><td>0.000268</td><td>0.007562</td><td>0.003301</td><td>0.003637</td><td>0.046578</td></tr><tr><td rowspan="2"> $800 \times 800$ </td><td>1-tail</td><td>0.028161664</td><td>0.011959</td><td>0.095029</td><td>0.053384</td><td>0.006982</td><td>0.003333</td></tr><tr><td>2-tail</td><td>0.056323328</td><td>0.023919</td><td>0.190058</td><td>0.106769</td><td>0.013964</td><td>0.006665</td></tr></table>

# 6.1 Optimal vs sub-optimal (vs random)

Each node updates its local leader with information about their current location. The periodicity of this update determines the accuracy of the location information present at the local leader. This location information will be used during the formation of the location-aware tree. As mentioned earlier, there is a trade off between the frequency of updates and the overhead involved. With lower update times, the node information will be most current at the leader nodes. However if each node were to initiate frequent updates, the network would be swamped with update packets. This section presents results of simulations for different update times.

The simulation is performed for an area of $5 0 0 \times 5 0 0 \mathrm { m } ^ { 2 }$ and $8 0 0 \times 8 0 0 \mathrm { m } ^ { 2 }$ . The cell size in both cases was chosen to be $1 0 0 \times 1 0 0 \mathrm { m } ^ { 2 }$ . The movement pattern was 5 m/sec with a

pause time of 10 sec. The total number of nodes was set to 150 and the number of member nodes was kept at 15. These nodes report the center of their (respective) cells as their location during the formation of the overlay tree. In each case, the (tree building) start time was a randomly chosen value between 0 and the update value (chosen for that particular simulation scenario). For example if the update value chosen was 70 sec, then the start time would be randomly distributed between 0–70 sec. By having start-up time between 0 and update time, we try to simulate the situation where an overlay tree was built using location information that was updated “start-time” sec before. Each simulation result is the average of 50 different scenarios. From Fig. 13, it is clear that the performance of a sub-optimal tree closely matches with that of an optimal tree. Figure 13 also shows the performance when no location information is used (i.e. a random overlay tree).

The figures show that higher update times result in higher latency (longer completion time). With higher update times, the information about the nodes’ location is more out-ofdate as a result; the multicast tree is less efficient. There is a trade-off involved in building an efficient multicast tree versus the overhead involved in refreshing node information (update period). In general, networks involving low mobility can maintain a low overhead by having a low update period. We conducted statistical (t-test with significance of 0.005) analysis on the simulation data. The test results are shown in Tables 3–5. According to the t-test results, there is no statistically significant performance difference between optimal and sub-optimal at the updated period levels 5 sec through 40 sec. However, the completion times are significantly lower in order optimal < suboptimal < random in case of 70 sec and 100 sec at the level of 0.05 for both areas.

Table 4 t-Test comparison between optimal and random 

<table><tr><td rowspan="2">Simulation area</td><td rowspan="2">p-value</td><td colspan="6">Update time</td></tr><tr><td>5 Sec</td><td>10 Sec</td><td>20 Sec</td><td>40 Sec</td><td>70 Sec</td><td>100 Sec</td></tr><tr><td rowspan="2"> $500 \times 500$ </td><td>1-tail</td><td>1.19 e-08</td><td>1.18 e-08</td><td>1.99 e-08</td><td>2.7 e-08</td><td>1.18 e-07</td><td>3.43 e-07</td></tr><tr><td>2-tail</td><td>2.38 e-08</td><td>2.36 e-08</td><td>3.97 e-08</td><td>5.4 e-08</td><td>2.36 e-07</td><td>6.86 e-07</td></tr><tr><td rowspan="2"> $800 \times 800$ </td><td>1-tail</td><td>3.25045 e-13</td><td>6.28 e-13</td><td>4.69 e-13</td><td>1.06 e-12</td><td>1.07 e-12</td><td>6.17 e-13</td></tr><tr><td>2-tail</td><td>6.50091 e-13</td><td>1.26 e-12</td><td>9.37 e-13</td><td>2.12 e-12</td><td>2.13 e-12</td><td>1.23 e-12</td></tr></table>

Table 5 t-Test comparison between sub-optimal and random 

<table><tr><td rowspan="2">Simulation area</td><td rowspan="2">p-value</td><td colspan="6">Update time</td></tr><tr><td>5 Sec</td><td>10 Sec</td><td>20 Sec</td><td>40 Sec</td><td>70 Sec</td><td>100 Sec</td></tr><tr><td rowspan="2"> $500 \times 500$ </td><td>1-tail</td><td>3.53 e-08</td><td>6.1 e-08</td><td>6.17 e-08</td><td>2.29 e-07</td><td>5.34 e-07</td><td>1.23 e-06</td></tr><tr><td>2-tail</td><td>7.07 e-08</td><td>1.22 e-07</td><td>1.23 e-07</td><td>4.58 e-07</td><td>1.07 e-06</td><td>2.45 e-06</td></tr><tr><td rowspan="2"> $800 \times 800$ </td><td>1-tail</td><td>1.10139 e-12</td><td>1.43 e-12</td><td>1.03 e-13</td><td>4.15 e-14</td><td>3.32 e-13</td><td>3.28 e-11</td></tr><tr><td>2-tail</td><td>2.20278 e-12</td><td>2.86 e-12</td><td>2.06 e-13</td><td>8.3 e-14</td><td>6.64 e-13</td><td>6.55 e-11</td></tr></table>

# 6.2 Scalability consideration

We repeated the above simulations for an area of $5 0 0 \times 5 0 0 \mathrm { m } ^ { 2 }$ for different number of member nodes—10, 15, 20, and 30 nodes. The update time of 20 sec was chosen— which meant that the nodes updated their location information randomly in 0 to 20 sec. The results in Fig. 14 show that the completion time increases with the increase in the member nodes, which was expected. The simulation also ascertains the scalability of our design—the performance of optimal and sub-optimal trees is very close.

# 6.3 Effects of smaller cell size

The aim of this set of simulations was to find a relation between the performance and cell size. Cell sizes of $2 5 \times 2 5$ , $5 0 \times 5 0 , 1 0 0 \times 1 0 0 , 1 2 5 \times 1 2 5 ,$ , and $2 5 0 \times 2 5 0 \mathrm { m } ^ { 2 }$ were checked. The topology area was chosen to be $5 0 0 \times 5 0 0 \mathrm { m } ^ { 2 }$ . The simulations also had varying member size—10, 15, 20, and 30 members. The movement pattern was 1 m/sec (human walk) with a pause time of 10 sec. It is easy to see from the result in Fig. 15 that the performance holds an inverse relation with the cell size. Smaller cell area gives an improvement in the performance. This is because smaller cell areas imply higher accuracy in the location information used for building the location tree.

# 6.3.1 Discussion

This improvement in performance (with smaller cell size) is offset by an increase in the service broadcast overhead. When the topology is divided into large number of small cells, any broadcast (during service discovery) would now pass through more leaders and will take longer to reach the entire leader set. As a result, the service discovery process will be slower and very inefficient. On the other hand, with larger cells, the location accuracy is lowered but the communication overhead and the propagation delays are reduced. Thus, there is a tradeoff between the overhead in service discovery and the performance of the overlay tree. Here is a simple back-of-theenvelope calculation showing the effect of smaller cell size. Consider the easiest case of controlled broadcast where the service discovery broadcast message reaches a leader node not more than once. In a topology that is partitioned into four cells, there will be at least three broadcast messages generated during any service discovery. If the topology is further divided into smaller cells with each cell having half the earlier length, total cells now increases to sixteen and the broadcast messages increases to fifteen. The number of broadcast keeps increasing exponentially (as seen in Fig. 16) every time the cell size is further divided to half its current length. The worst case scenario is when the cell size is so small that every cell has just one node in it. In such a case, the broadcasts will be between each node and will be exponentially proportional to the number of member nodes. This is the same as the case where no cells are used. The purpose of using cell structure is to limit the broadcast only between the leader nodes.

![](images/65d9fe4853e8930733b5523a25dc47b2b37f8526d4784c7e669709cf344e4ec5.jpg)



Fig. 14 Scalability of the protocol

![](images/959ad0646cd9b4f9a4432a7a108a638f18761efc317203d66465e9fd96032975.jpg)



Fig. 15 Performance of SOLONET for different cell sizes and member nodes

![](images/7a7e1c9f42f79edb7ba8d5406a62296d8efa9877a1c7587da783c25505eb59af.jpg)



(a)   
$1 / 4 ^ { \mathrm { t h } }$ area (square)

![](images/cca67c2babad9d28e8e347efb806002a070a7e155cd7cb660380b50b3bac1fad.jpg)



(b)   
$1 / 1 6 ^ { \mathrm { t h } }$ area (square)

![](images/9edfc45299da6c8bedb5cbd4eef366016a22d82b88feb10fa7ec2c54d3aea4ca.jpg)



$1 / { 4 } ^ { \mathrm { t h } }$ area (triangle)

![](images/283a6adec9b9bce0ae8b3113ab64e2e0ebb2191b64365593a6139e99ee35be38.jpg)



$1 / 1 6 ^ { \mathrm { t h } }$ area (triangle)   
Fig. 16 Broadcast scenario

# 6.3.2 Reducing broadcast overhead in small cells

Figure 15 shows how decreasing the cell size improves the location accuracy and hence the performance of a locationaided tree. However, this improvement comes at the cost of high overheard during any service discovery broadcast Fig. 17(a). In order to solve this problem, we propose some enhancements to our architecture. We suggest the use of two separate cell partitions (each of different sizes). The service discovery mechanism would refer to a larger cell partition called service discovery cells. These large service discovery cells would house several smaller regular cells. The regular cells would be used by nodes during their normal operations (like leader selection, event based update, beacon message, etc). The larger cells on the other hand will be used only by leader nodes during the service discovery process. Certain cell leaders would be designated as service leaders for that region. The selection of service leaders can be predetermined. For example, if the service discovery cell consists of four regular cells, then the service leaders can be chosen as follows:

$$
\{2 p + 2 x, 2 q + 2 y \} [ p = 0, n \& q = 0, m ]
$$

where $n = 1 / 2 \times ( n o .$ . of longitudinal cells); $m = l / 2 \ \times \ ( n o .$ of latitudinal cells)

This gives (2,2); (2,4); (4,6); (6,2). . . etc as the service leader set (e.g. Fig. 17(b)).

During any service discovery process, a service leader would forward the broadcast message to its neighboring service leaders and to the regular leaders in its service discovery cell. With smaller cell size for regular operations, we have the benefit of better location accuracy while larger service cell limit the broadcast overhead between service leaders only Fig. 17(b).

Fig. 17 Smaller cell size—more service discovery broadcasts   
![](images/5585ef59cdf8b5cf1b627f44f357bbba9a463f65962fdd69b84981deebe1893f.jpg)



![](images/274581106f7ccc017b7e96d211d6d516deae3d878d3019935e1aa137efba1d00.jpg)



# 6.3.3 Cell size and mobility

When a node moves from one cell to another cell, it reports a change in its location to the source node. The change is reported as a new CellID (CID). The source node may decide to rearrange the overlay tree to compensate for the new positions. This reshuffling would lead to several new connections (and equal number of disconnections) between member nodes. We defined the term reconnections to indicate the new connection number. The cell size should be chosen such that the reconnection number is small. Reconnections are expensive—every new connection would change the route information at the underlying network layer at all the intermediate non-member nodes. This may initiate route discovery process depending on how the underlying unicast protocol is implemented. Also, with every reconnection, state tables have to be made at the source and destination node for the new connection. The simulation setup was similar to the one used in Section 6.3. The topology area was $5 0 0 \times 5 0 0 \mathrm { m } ^ { 2 }$ . Simulation for cell sizes of $^ { \prime } 2 5 \times 2 5 , 5 0 \times 5 0 , 1 0 0 \times 1 0 0 , 1 2 5 \times 1 2 5$ , and $2 5 0 \times 2 5 0 \mathrm { m } ^ { 2 }$ were carried out with varying member size—10, 15, 20, and 30 members. The movement pattern was 1 m/sec (human walking) and 5 m/sec (human running) with a pause time of 0 sec (continuous movement), 10 sec, and 20 sec. The simulation follows the ‘random waypoint’ model [21]. Since the performance is sensitive to movement pattern, all the results in this set are average of 30 different movement scenarios (generated by ns2 for the same pause time and speed combination).

The number of reconnections for a speed of 5 m/sec was much higher compared to speeds of 1 m/sec (Fig. 18). Within each speed, higher pause times gave lesser reconnections on an average (clearly seen in Figs. 18(c) and (d) for $\mathrm {  ~ p = 0 , }$ s = 1). One would think that smaller cell size should be used only if the node mobility is low. The reason being with high mobility, nodes will constantly cross cell boundaries triggering frequent location updates and hence, higher reconnections (re-organizing the overlay tree). However, our simulation results were a little counter-intuitive. Our simulation results indicate that for lower speeds (1 m/s), the number of reconnections start at a lower values and keep increasing until the cell area reaches about $1 0 0 \times 1 0 0 \mathrm { { m } } ^ { \bar { 2 } }$ . Beyond $1 0 0 \times 1 0 0 \mathrm { m } ^ { 2 }$ , the average reconnection number starts to fall until it reaches the lowest at $2 5 0 \times 2 5 0 \mathrm { m } ^ { 2 }$ (as expected).

![](images/e077130919917f7f1aedf470a4d1fc676f60d8d2a1a923c915fd7952de11efb1.jpg)



![](images/ba81586db2434f71bc904823a0309227bd99e3a56369bb959cfbda9e0c4795d3.jpg)



(b)

![](images/1815460ea4a49f9790babfef0d86c224e6b3c50d3d3a6f15cfe78ff3d99813b0.jpg)



![](images/f554966be885400a5bea93c7ec9db7f21c2960852934c3ae7db834d078d1ed0b.jpg)



(d)   
Fig. 18 Cell size vs Node mobility

![](images/359b001ec56f570e88de2e4e1886a90cb825562db1bdd3abda33c47e8feae740.jpg)



a) smaller size cell – no reconnection   
![](images/95c4eb00c0b8bf25d75cbf4318cc63a135ceaf2484c07269320ba8622f23c26d.jpg)



![](images/c3eaf3e857418c4ba3c8b7c3a8eb15a1068a0d23388781b135c43bed48e3c182.jpg)



b) larger cell size causes reconnection   
![](images/4cd70b0df61c3f80e4fdeb10cf81a77ceb6ba3a7bb5cfdb167ea4363cda0fca2.jpg)



Fig. 19 Effect of larger cell size on connection pattern

This anomalous behavior can be explained with the help of Fig. 19. The source node maintains a CID for every member node in its tree. When a node moves to a new cell, it reports the new CID to the source. In our design, the source assumes the center of the new cell as the new location of the recently moved member node. This is where the problem lies. The source node periodically re-computes the overlay tree in order to compensate for node movement and their new position. With small size cells, the distance between the centers of neighboring cells is very small as compared to the one in larger size cells. As a result, when the tree is rebuilt, smaller cell will not see many reconnections. However, in case of large cells, nodes that have just crossed a cell boundary would report a major change in their location causing several updates. We ran simulations for update time of 20, 30, and 60 sec. For a much larger cell size (beyond $1 0 0 \times 1 0 0 \mathrm { m } ^ { 2 } )$ ), the shorter update interval and lower speeds are not enough for nodes to travel across boundaries and so the number of reconnections starts to go down. This is clearly seen in case of 20 sec and 30 sec update Figs. 18(a) and (b) where the number of reconnections start to go down beyond $1 0 0 \times 1 0 0 \mathrm { m } ^ { 2 }$ while in case of 60 sec, the curve starts to fall around $1 2 5 \times 1 2 5 \mathrm { m } ^ { 2 }$ .

# 7 Conclusion and future work

This paper presents SOLONet, a design to build sub-optimal overlay multicast trees, which tries to strike a balance between the advantages of using location information for building efficient overlay multicast trees versus the cost of maintaining and distributing location information of every member node. SOLONet eliminates the need to do expensive location broadcast for each node and doesn’t require each node to know the location of every other node. The SOLONet architecture partitions the physical topology into smaller cells. By having a local leader in each cell, the system is able to localize several tasks and aid in the service discovery mechanism. The paper gives a detailed description of the service discovery mechanism, local leader selection process, and the use of a beacon message for carrying out various activities.

Our simulation results show that SOLONet is scalable and its performance closely matches that of an optimal overlay multicast tree. We have conducted a detailed analysis of the performance of SOLONet with different cell sizes and have also examined the effect of smaller cell size. In our current simulations, we have considered square cells; however in the future, we plan to test SOLONet with other shapes and see the effect of shape to the system performance. We are also investigating an algorithm that can adaptively divide a cell into smaller sub-cells if the density of nodes increases beyond a certain value.

Acknowledgments This research is supported in part by US National Science Foundation under grants CCF 0514078, CNS 0549006, and CNS 0551464, by Hong Kong RGC Grant HKUST6183/05E, China National Natural Science Foundation grant No. 60573053, the Key Project of National Natural Science Foundation of China under Grant No. 60533110 and the National Basic Research Program of China (973 Program) under Grant No. 2006CB303000.

# References

1. Ekahau Positioning System, http://www.ekahau.com/.   
2. G. Anastasi, E. Borgia, M. Conti and E. Gregori, Wi-Fi in ad hoc mode: A measurement study, in: Presented at PerCom 2004 (March 2004).   
3. D. Andersen, H. Balakrishnan, M. Kaashoek and R. Morris, The case for resilient overlay networks, in: Presented at 8th Annual Workshop on Hot Topics in Operating Systems (HotOS-VIII) (May 2001).   
4. P. Bahl and V.N. Padmanabhan, RADAR: An in-building RF-based user location and tracking system, in: Presented at IEEE INFOCOM (March 2000).   
5. S. Banerjee, B. Bhattacharjee and C. Kommareddy, Scalable application layer multicast, in: Presented at ACM SIGCOMM (August 2002).   
6. K.P. Birman, M. Hayden, O. Ozkasap, Z. Xiao, S. Ni, Y. Tseng, Y. Chen and J. Sheu, The Broadcast storm problem in a mobile ad hoc network, in: Presented at 5th Annual ACM/IEEE International Conference on Mobile Computing and Networking (August 1999).   
7. E. Bommaiah, M. Liu, A. MvAuley and R. Talpade, AMRoute: Ad hoc multicast routing protocol, in: Presented at Internet Draft, draft-manet-amroute-00.txt (March 2002).   
8. K. Chen and K. Nahrstedt, Effective location—guided tree construction algorithm for small group multicast in MANET, in Presented at IEEE INFOCOM (May 2002).   
9. Y. Chu, S. Rao and H. Zhang, A case of end system multicast, in: Presented at ACM Sigmetrics (June 2000).   
10. C.D.M. Cordeiro, H. Gossain and D.P. Agrawal, Multicast over wireless mobile ad hoc networks: Present and future directions, In: IEEE Networks, vol. 17 (January 2003).

11. C. Diot, B.N. Levine, B. Lyles, H. Kassem and D. Balensiefen, Deployment issues for the IP multicast service and architecture, in: IEEE Network Magazine (January/February 2000).   
12. R. Dube, C.D. Rais, K. Wang and S.K. Tripathi, Signal stability based adaptive routing (SSA) for ad hoc mobile networks, in: Presented at IEEE Personal Communication (February 1997).   
13. M. Gerla and J.T. Tsai, Multicluster, mobile multimedia radio network, ACM-Blatzer Wireless Network (1995).   
14. C. Gui and P. Mohapatra, Efficient overlay multicast for mobile ad hoc networks, in: Presented at Wireless Communications and Networking Conference (WCNC) (March 2003).   
15. C. Gui and P. Mohapatra, Scalable multicast in mobile ad hoc networks, in: Presented at Infocom (March 2004).   
16. A. Haeberlen, E. Flannery, A. Ladd, A. Rudys, D. Wallach and L. Kavraki, Practical robust localization over large-scale 802.11 wireless networks, in: Presented at Mobicom 2004 (September 2004).   
17. J. Hightower, L. Liao, D. Schulz and G. Borriello, Bayesian Filtering for Location Estimation, IEEE Pervasive Computing (July–September 2003).   
18. J. Hightower, R. Want and G. Borriello, SpotON: An indoor 3D location sensing technology based on RF signal strength, in: Presented at UW CSE 00-02-02 (February 2000).   
19. J. Jetcheva and D.B. Johnson, Adaptive demand-driven multicast routing in multi-hop wireless ad hoc networks, in: Presented at MobiHoc (October 2001).   
20. L. Ji and M.S. Corson, Differential destination multicast—A MANET multicast routing protocol for small groups, Presented at IEEE INFOCOM (April 2001).   
21. D. Johnson and D. Maltz, Dynamic source routing in ad hoc wireless networks, Mobile Computing (1996).   
22. B. Karp and H.T. Kung, GPSR: Greedy perimeter stateless routing for wireless networks, in: Presented at ACM/IEEE MOBICOM (August 2000).   
23. S.J. Lee, M. Gerla and C.C. Chiang, On demand multicast routing protocol, Presented at IEEE WCNC (September 1999).   
24. C.R. Lin and M. Gerla, Adaptive clustering for mobile wireless networks, IEEE Journal on Selected Areas in Communications Vol. 15 (1996).   
25. M. Mauve, H. F¨ußler, J. Widmer and T. Lang, Position-based multicast routing for mobile ad-hoc networks, Presented at Technical Report TR-03-004 (2003).   
26. L.M. Ni, Y. Liu, Y.C. Lau and A. Patil, LANDMARC: Indoor location sensing using active RFID, in: Presented at IEEE PerCom (March 2003).   
27. D. Niculescu and B. Nath, VOR base stations for indoor 802.11 positioning, in: Presented at Mobicom 2004 (September 2004).   
28. K. Obraczka, G. Tsudik and K. Viswanath, Pushing the limits of multicast in ad hoc networks, in: Presented at IEEE ICDCS (April 2001).   
29. A. Patil, Y. Liu, L. Xiao, A.-H. Esfahanian and L.M. Ni, SOLONet: Sub-optimal location-aided overlay network for MANETs, in: Presented at IEEE Mobile Ad hoc and Sensor Systems (October 2004).   
30. C.E. Perkins, E.M. Royer and S.R. Das, Ad hoc on demand distance vector (AODV) routing, in: Presented at Internet Draft, draft-ietfmanet-aodv-10.txt (March 2002).   
31. E.M. Royer and C.E. Perkins, Multicast operation of the ad-hoc on-demand distance vector routing protocol, in: Presented at ACM MOBICOM (August 1999).   
32. A. Smailagic, D.P. Siewiorek, J. Anhalt, D. Kogan and Y. Wang, Location sensing and privacy in a context aware computing environment, in: Pervasive Computing (2001).   
33. J. Small, A. Smailagic and D. Siewiorek, Determining User Location for context aware computing through the use of a wireless LAN infrastructure (December 2000).

34. I. Stojmenovic, Position based routing in ad hoc networks, in: IEEE Commmunications Magazine Vol. 40 (July 2002) pp. 128–134.   
35. Y.C. Tseng, S.Y. Ni and E.Y. Shih, Adaptive approaches to relieving broadcast storms in a wireless multihop mobile ad hoc networks, in: Presented at IEEE 21st International Conference on Distributed Computing Systems (2001).   
36. J. Wu, Dominating-set-based routing in ad hoc wireless networks, in: Handbook of Wireless Networks and Mobile Computing, I. Stojmenovic, Ed.: John Wiley & Sons (2002) pp. 425–450.   
37. J. Wu and F. Dai, Broadcasting in ad hoc networks based on selfpruning, in: Presented at IEEE INFOCOM (March 2003).   
38. L. Xiao, A. Patil, Y. Liu, L.M. Ni and A.-H. Esfahanian, Prioritized overlay multicast in ad-hoc environments, IEEE Computer Magazine (February 2004).   
39. Y. Xue and B. Li, A Location-aided power-aware routing protocol in mobile ad hoc networks, in: Presented at IEEE GLOBECOM (November 2001).   
40. M. Youssef, A. Agrawala and A.U. Shankar, WLAN location determination via clustering and probability distributions, in: Presented at IEEE PerCom (March 2003).   
41. H. Zhou, L.M. Ni and M.W. Mutka, Prophet address allocation for large scale MANETs, Ad Hoc Networks Journal Vol. 1 (November 2003).

![](images/652c390a1a01d4fbe00c605eed084c59bdbbb592b5a4be6cf174f18f07ae8719.jpg)



Abhishek Patil received his BE degree in Electronics and Telecommunications Engineering from University of Mumbai (India) in 1999 and an MS in Electrical and Computer Engineering from Michigan State University in 2002. He finished his PhD in 2005 from the Department of Computer Science and Engineering at Michigan State University. He is a research engineer at Kiyon, Inc. located in San Diego, California. His research interests include wireless mesh networks, UWB, mobile ad hoc networks, application layer multicast, location-aware computing, RFIDs, and pervasive computing.

![](images/2de87bac0656db9a06e1b7fc78d59613b18acfdf42ababa97225f024b0caf91d.jpg)



Yunhao Liu received his BS degree in Automation Department from Tsinghua University, China, in 1995, and an MA degree in Beijing Foreign Studies University, China, in 1997, and an MS and a Ph.D. degree in Computer Science and Engineering at Michigan State University in 2003 and 2004, respectively. He is now an assistant professor in the Department of Computer Science at Hong Kong University of Science and Technology. His research interests include wireless sensor networks, peer-to-peer and grid computing, pervasive computing, and network security. He is a senior member of the IEEE Computer Society.

![](images/8db196e9e900faa63abb661643f712b5c9dfd252a80c7c803ab8d221332ee75f.jpg)



Li Xiao received the BS and MS degrees in computer science from Northwestern Polytechnic University, China, and the PhD degree in computer science from the College of William and Mary in 2002. She is an assistant professor of computer science and engineering at Michigan State University. Her research interests are in the areas of distributed and Internet systems, overlay systems and applications, and sensor networks. She is a member of the ACM, the IEEE, the IEEE Computer Society, and IEEE Women in Engineering.

![](images/dbe5f6e0bb3f167095651a0b6b21492b2218c1cf694719a09ed7a27d85053209.jpg)



Abdol-Hossein Esfahanian received his B.S. degree in Electrical Engineering and the M.S. degree in Computer, Information, and Control Engineering from the University of Michigan in 1975 and 1977 respectively, and the Ph.D. degree in Computer Science from Northwestern University in 1983. He was an Assistant Professor of Computer Science at Michigan State University from September 1983 to May 1990. Since June 1990, he has been an Associate Professor with the same department, and from August 1994 to May 2004, he was the Graduate Program Director. He was awarded ‘The 1998 Withrow Exceptional Service Award’, and ‘The 2005 Withrow Teaching Excellence Award’. Dr. Esfahanian has published articles in journals such as IEEE Transactions, NETWORKS, Discrete Applied Mathematic, Graph Theory, and Parallel and Distributed Computing. He was an Associate Editor of NETWORKS, from 1996 to 1999. He has been conducting research in applied graph theory, computer communications, and fault-tolerant computing.

![](images/80f8728813035a497cc06c951b5abe6ecad3ce307b1ae7b16197b41bcabe9e93.jpg)



Lionel M. Ni earned his Ph.D. degree in electrical and computer engineering from Purdue University in 1980. He is Chair Professor and Head of Computer Science and Engineering Department of the Hong Kong University of Science and Technology. His research interests include wireless sensor networks, parallel architectures, distributed systems, high-speed networks, and pervasive computing. A fellow of IEEE, Dr. Ni has chaired many professional conferences and has received a number of awards for authoring outstanding papers.