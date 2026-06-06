# Resource Allocation using Multiple Edge-Sharing Multicast Trees

Abhishek Patil 1 , A-H. Esfahanian1 , Li Xiao1 and Yunhao Liu2

1 Dept of Computer Science and Engineering

Michigan State University

East Lansing, MI 48824

{patilabh,esfahanian,lxiao}@cse.msu.edu

2 Dept of Computer Science

Hong Kong Univ of Science and Technology

Kowloon, Hong Kong

liu@cs.ust.hk

Abstract 1 - Implementing multicast in MANETs is a challenging task. A typical multicast network consists of a single tree, in which only a few internal nodes contribute most resources and are involved in performing the multicast functionality. This leads to an un-even utilization of network resources. This problem is more prominent in MANETs where network resources are limited. A possible solution to the problem is to split the multicast content over a number of trees. Multiple trees provide several paths for the multicast content and get more nodes involved in implementing the multicast functionality. However, in such a setup, not all the trees get to use the best weight edges, thus the overall multicast latency increases. This paper presents MEST, a distributed algorithm to construct multiple edge-sharing trees for small group multicast. MEST balances the resource allocation and delay constraints by choosing to overlap certain edges that have low weights. Our simulation results show that MEST is scalable and can generate multicast networks that have low delay and fair resource utilization.

Keywords: Resource Allocation, Graph Theory, Multicast, Mobile Ad Hoc Networks, MANET, Wireless Networks, Simulation, Mobile Networks.

# I. INTRODUCTION

Mobile ad hoc networks (MANETs) are characterized by mobile nodes and constantly changing network topology. Implementing multicast in such a dynamic environment is a not an easy task. As pointed out by [17], traditional IP-layer multicast for MANETs has a lot of signaling overhead as it needs to take into account the network dynamics in addition to the (multicast) group dynamics. In recent years, several researchers have proposed the concept of application layer (overlay) multicast. Overlay multicast is gaining popularity due to its easy of implementation and flexibility. Overlay multicast relies on the underlying unicast protocols to adapt to the changing network topology. As a result, the application layer has to track only the group dynamic. Due to its ease of implementation and flexibility to adapt, overlay multicast networks (though not as efficient as IP layer multicast) are finding many practical applications in MANETs. AMRoute [4], PAST-DM [10], SOLONet [19] and LGT [6] are some of the overlay multicast protocols that have been proposed for MANETs. Similar to other multicast networks, overlay multicast also suffers from the resource utilization problem (also referred to as the fairness issue in some literature). This fairness issue results from the fact that in a typical multicast tree, only a small number of nodes and edges are actively involved in implementing the multicast functionality. For example, there are a few internal nodes that perform the task of duplicating and forwarding packets and a large number of leaf nodes that only act as receivers of packets. These leaf nodes do not contribute any resources to the multicast tree. MANETs are characterized by scarce network resources. Due to this uneven distribution, certain nodes will run out of resources (e.g. battery strength) faster than other nodes, leading to bottleneck nodes in the multicast trees. As explained by Wang and Gupta [23], the lifetime of a multicast tree depends on the lifetime of a bottleneck node. Proper resource allocation can help better utilize the available resource and extend the life of an overlay multicast network.

The delay in a multicast tree is equal to the time it takes for all the leaf nodes to receive the packets (data) sent by the source node. There are two main techniques that can help reduce this delay: source eccentricity and tree weight. The first approach tries to reduce the source node’s eccentricity. (The eccentricity of a node v in a connected graph G is length of the longest of all the shortest paths between v and every other point in G). A higher fan-out at interior nodes results in a low depth tree (low source eccentricity), thus having a shorter delay.

However, a tree with higher fan-out at interior nodes would have a large number of leaf nodes. For example, a binary tree has half the nodes as leaf nodes [15]. A tree with an average fan-out of 16 will be shorter (lower delay) but will have 10% internal nodes that perform the multicast functionality. Thus it is necessary to have a well constructed overlay multicast tree which would maintain a good balance between the multicast latency and utilization of network resources. There are many distributed algorithms [3, 5, 11, 16] for generating shortest path trees; however, most of them pay little attention to the network utilization issues.

![](images/544db445a301c549f9c40a044f7bbec44351e39b47bc4c770ba2a49696a83920.jpg)



Figure 1: Multicast content split and sent over multiple trees.

The other method for reducing delay is by constructing low weight trees. (The weight of a tree is the sum of weights of its edges.) Low weight trees tend to have lower delays as they try to use low weight edges during their construction. In this paper, we concentrate on the second approach to reduce delay: constructing multiple low weight multicast trees.

In this paper, we present MEST – a distributed algorithm for building multiple edge-sharing multicast trees. MEST aims to uniformly distribute the multicast functionality across all the nodes in the group with little change in the multicast delay. Our MEST algorithm is designed to run on top of any distributed algorithm for constructing a minimum spanning tree of a given graph (e.g. [2, 8, 22]). In this paper, however, we describe MEST with respect to the GHS algorithm [8]. An interesting point to note here is that the concept of MEST can be applied to any kind of multicast network. Although this paper describes MEST with respect to overlay multicast, MEST algorithm can be used to improve the resource allocation (as well as keep the delay under control) in any wired multicast network or IP-based multicast in MANETS. MEST constructs several multicast trees in the same network. Each tree constitutes a separate sub-group and all the nodes participating in the multicast subscribe these sub-groups. The multicast content is split into smaller stripes and each stripe is then sent over one of the multicast trees (Figure 1). (Note that we chose to use the word stripes instead of fragments, to avoid confusion with ‘fragment of a graph’). Several papers propose the use of multiple multicast trees for mesh creation in order to have redundant links to improve reliability. Although improving reliability is not MEST’s primary objective, the MEST algorithm can also be used in building a reliable redundant mesh network. In such a network, the multicast content is not split into smaller stripes; instead, each MEST multicast tree will provide an alternative path to the multicast data. If one path fails, the nodes re-route the data over one of the other alternative paths.

We carried out several simulations to examine the scalability and performance of MEST. Overall, our simulation results indicate that MEST is highly scalable and has a lower delay as compared to a single tree multicast. We were also able to determine the best overlap threshold value for a given scenario. The simulation results also show significant reduction in the delay as the number of trees increase. However, we strongly believe that there would be other factors (like file fragmentation overhead) that need close examination in order to check if they offset this performance improvement.

The rest of the paper is structured as follows. Section II looks at previous work done in the area of uniform resource allocation. Section III gives a brief introduction of the GHS algorithm to our readers. Section IV presents detailed description of our MEST algorithm. In Section V we present simulation results for MEST. Finally, Section VI concludes the paper and presents directions for future research.

# II. RELATED RESEARCH

Several overlay multicast protocols [4, 6, 10, 19] have been proposed and studied for MANETs in recent past. All of them are based on single tree multicast and are geared to address the efficiency issues of overlay multicast. In recent years, the issue of resource allocation has caught the attention of many researchers [14, 15, 18, 24].

Like MEST, SplitStream algorithm [15] tries to distribute the multicast load by constructing multiple multicast trees. However, SplitStream is based on a complex infrastructure (Pastry [20] and Scribe [21]) and requires the help of nonmembers to construct multicast trees. MEST on the other hand is much simpler and doesn’t require any help from the nonmember nodes, thus making it compatible with any kind of underlying network. Although, SplitStream focuses on improving the resource utilization of the network, it doesn’t pay much attention to the delay constraints. The algorithm attempts to accommodate member nodes with different bandwidth capacities. In doing so, it makes use of the Scribe mechanism to limit the number of outgoing connections from a member node. As a result, a ‘child node’ might be forced to connect further down the tree resulting in higher delay.

Young [24] suggested a k-MST algorithm for building a reliable mesh structure. Their algorithm builds multiple edgedisjoint minimum spanning trees. The algorithm works by removing an edge from the graph once it is used by a tree. This tends to build trees that greatly vary in their weight and hence the multicast latency. During the later stages of such an algorithm, the newer trees end-up having the high weight edges (which were rejected by the earlier trees). The final tree would be the one with the highest delay since it is using all the high weight edges that were not used by the earlier trees. The k-MST algorithm differs from MEST since it tries to build edge disjoint multiple tree and has a primary goal of constructing a mesh network. In the k-MST algorithm, if one tree fails, data can be sent over another redundant tree. However, the multicast delay would increase since the data is being transferred over a tree with a high weight. It should be noted that such a method works well only for a mesh case. It cannot be used for address the resource allocation problem since the delay involved in simultaneous transfer of multicast content would be unacceptable. Some of the content would come over a tree that has the highest weight (maximum delay).

The strategy adopted in [14, 18] are different from ours essentially. They rely on accounting and charging methods to solve the unfairness problem, that is, group members served as a forwarder charges for its service to its children to make up its contribution to the system. Overcast [12] maintains a single tree and uses a dedicated server to optimize the bandwidth utilization across the network.

# III. GHS ALGORITHM

Gallagher, Humblet, and Spira (GHS) [8] were one of the first to provide a solution to the problem of constructing a minimum spanning tree in a disturbed manner. The following two sub-sections give a brief description of their algorithm and the message exchange between nodes. Interested readers should refer to the GHS paper [8] for further details.

# A. Overview

The GHS protocol works by combining fragments (disconnected components of a graph) along the shortest edge joining them. The protocol maintains a forest of trees, each identified by its fragment id (fragid) which consists of the fragment’s level number and fragment’s core node’s id. At start, all the nodes are at level 0 and every node is an individual fragment. Each fragment attempts to asynchronously find a minimum weight out going edge (mwoe) into another fragment. When such an edge is found the two fragments exchange ‘connect’ messages and attempt to combine to form a larger component. As fragments join, the level of the combined component increases by one (if certain conditions are satisfied). There are a few rules that need to be followed in order for this merger (and level increase) to happen:

1. Suppose a fragment $\mathrm { F _ { l } }$ at level m (m>0) encounters a connect message from a smaller fragment $\mathrm { F _ { s } }$ at level m-p (p<m) at the other side of the mwoe, the smaller fragment is absorbed as a part of the larger fragment. The level and fragid of the combined larger fragment stays unchanged i.e. $\mathrm { F _ { l } }$ at m.   
2. If the two fragments are at the same level m and have the same mwoe, then they combine to form a larger fragment at level m+1. The mwoe edge which joined the two fragments is then termed as the ‘core’ of the fragment.   
3. On the other hand, if a fragment at level m encounters a larger fragment (at level x; x>m) along it mwoe, it delays $\mathrm { i t } ^ { \prime } \mathrm { s }$ connect message until it reaches a level at least equal to x.

The rules for combining fragments ensure that a new fragment at level m+1 will be formed by the combination of at least two fragments at level m. Thus, a fragment at level p will contain at least $2 ^ { \mathrm { p } }$ nodes. Therefore, log N is an upper bound on the fragment levels. The wait in rule 3 is essential since communication latency required to find it mwoe is proportional to the fragment size. If this delay is not implemented, it may result in a loop. An example is shown in Figure 2.

![](images/8641180b43b4db5b1106ee72966602d876247134798f28b6f4039e87f5a9d719.jpg)



Figure 2: Example of a delayed merge.

When the two fragments combine, the nodes in these fragments (other than the core nodes) are not immediately informed about the identity and level of the new fragment. In this example, let’s say F and F’ (both at the same level) combine along their mwoe (in this case PQ). Now the new fragment is one level higher. The fragid has changed to the new mwoe. Now, P and Q know about the new level and fragid. However, there are several other nodes in each fragment (e.g. A and B) who won’t know about this change until they get some message (e.g. initiate message) from the P or Q. At some point node A gets an initiate message from P and it updates its level. Node B on the other hand still has the old id and level. If the wait in the third rule is not implemented, node B might send a connect message to A thus causing a loop. The wait ensures that B waits till its level increases at least to that of A. When that happens, B realizes that they belong to the same component.

# B. GHS Example

As an example of the GHS algorithm, consider Figure 3. At t=0, all nodes are at level 0. At some later time, nodes A and B merge to form a larger fragment at level 1. Similarly, nodes E and F combine on their mwoe to form $\mathrm { F } '$ at level 1. Further ahead, node C and node D get absorbed into F and F’ respectively. After some more time, the two fragments merge on the edge BF to form a larger fragment $\mathrm { F } ^ { \prime \prime }$ with level 2. At a later point in time, node G gets absorbed into this larger fragment.

![](images/ab25a637e32e4bb8a1e70f844a434c68a7f5306badd552213f5bf283b6168972.jpg)



Figure 3: GHS Example.

# IV. MEST ALGORITHM

Our MEST algorithm can runs on top of any distributed algorithm for constructing a minimum spanning trees of a given graph (e.g. Async [22], Awerbuch [2], GHS [8]). In this paper, however, we describe MEST with respect to the GHS algorithm. MEST can be considered as several instances of the GHS algorithm running in a sequence one after the other. At start, all the nodes run the GHS algorithm to produce the first tree $( \mathrm { T } _ { 1 } ) ,$ then the second run gives tree T2 and so on, till all the desired number of multicast trees have been generated.

# A. Preliminaries

In case of multiple multicast trees, the highest weight multicast tree contributes the most delay and so, the delay of the overall system is determined by this (highest-weight) tree. Since edge disjoint multicast trees would use different edges in each tree, ideally, they would do a better job in solving the resource allocation problem. However, if edge disjoint trees are not constructed correctly, they may not be the best choice when it comes to delay constraints. An example is shown in Figure 4. For the given graph, it is possible to find many pairs of edge disjoint spanning trees. Note that each multicast tree has to be a spanning tree since it has to cover all the multicast member nodes. Two such pairs are shown (Figure 4b & 4c). In Figure 4b, T1 is a minimum spanning tree. However, other multicast tree $( \mathrm { T } _ { 2 } )$ has a very high latency since it is using all the high weight edges that were rejected by the minimum spanning tree (T1). With the two trees, the network resources are evenly used; however the overall multicast delay would be determined by the slowest amongst the two trees (T2). Unlike Figure 4b, in case of Figure 4c, the light weight edges are equally distributed between the two spanning trees and hence the overall delay is lower compared to the earlier case.

Now consider the case where two trees can share an edge. Figure 4d shows two spanning trees (one of them minimum) that have two common edges (DE and EF). Such a multicast tree may be obtained by having a condition that allows the overlap of edges that satisfy a certain condition. For example, edges having weight below a certain threshold or edges connected to nodes that have very low degree. This threshold should be wisely chosen. A value too high would lead to several overlapping edges, decreasing the network utilization and a value too low would increase the multicast latency. In the example, we choose the cut-off threshold for edge sharing as 5. In Section V, we show the best overlapping threshold for a particular scenario.

Other factors affecting the delay: In case of edge-sharing trees, a factor that might affect the delay is the number of times an edge is re-used. This is important because a shared edge has to carry packets for different multicast groups since it is part of several multicast trees. For example, in case of Figure 4d, the two common edges (DE and EF) have to carry packets for both the trees. A packet would be queued at a node if that node is currently sending or receiving another packet over the common edge. Depending on the queue length, this queuing might result in additional delay. In case of nonstreaming applications, a packet would be queued only if an overlapping edge is at the same delay-distance from the source node in multiple trees. In case of streaming applications, this delay would always be present since there is constant stream of data to be sent by the node. In order to eliminate any further delays due to queuing, we suggest setting an upper bound on the number of trees that can share a particular low-weight edge.

Special cases: A bridge is an edge of a graph whose removal will result in a disconnected graph. For graphs that contain bridge edges, it is not possible to have multiple trees that are completely edge disjoint. Figure 5 shows such an example. In the example, edge BG is a bridge edge and will be present in any spanning tree of this graph. In our MEST algorithm, we mark a bridge edge with the $\mathbf { \partial } ^ { 6 } \mathbf { S } ^ { \prime }$ tag to indicate that this is a special case edge, which has to be included in all the spanning trees.

# B. Basic Operation

Let’s say we want to construct ‘m’ multicast trees $( \mathrm { T } _ { 1 } , \mathrm { T } _ { 2 } , \dots$ $\mathrm { T } _ { \mathrm { m } } )$ which may have some overlapping edges. Since each node is running an instance of the GHS algorithm, at t=0 there are $\cdot _ { \mathrm { ~ m ~ X ~ n ~ } } ,$ fragments. Each node maintains a variable called the fragid which stores the fragment id (fragid) of the components that the node is currently associated with. Nodes also maintain separate arrays (of length = ‘m’) for each of its edges.

![](images/8ae35b66cc2addf3e6a7d06feeb9b2b44d31d443acdb93465f587f4aabacdab2.jpg)



![](images/9b8cefa226063d644243ddacaa13ebdcdd8227658cc80a45e4cf84a8f49beba7.jpg)



![](images/10f74c91c35d6daab3dcd6ade2379ab9d83de015d709b29ac3ed87919698b232.jpg)



![](images/7201545cf871c0551b9d6321311302f64a19b6f7a2d08ee1bd6f492c6ef9b96e.jpg)



Figure 5: Example of Bridge edge.

The ‘m’ elements of the edge array correspond to the ‘m’ trees that the edge can potentially be part of. An element of the edge array can have one the following values:

‘B’ = Edge forms a branch in the current tree.

‘R’ = Rejected edge - edge was by the current tree since it joins another node of the same fragment.

‘U’ = Usable edge (Basic edge). This edge will be checked to see if it’s the best edge for this node.

‘X’ = Edge was used by an earlier tree. An edge marked as X will not be used in current tree.

‘S’ = Usable edge (Special case – bridge edge)

At start, edge arrays at each node are initialized so that every element in it is marked as $\mathbf { \tilde { U } } ^ { , }$ . This allows the first run of GHS to choose any edge it wants. Thus in a way, the first tree is a true MST for that graph. During the formation of the $\operatorname { k } ^ { \mathrm { { t h } } }$ tree, a node will mark the $\mathrm { \dot { k } } ^ { \mathrm { t h } }$ element of an edge array as $ { \mathbf { \ell } } ^ { 6 }  { \mathbf { B } } ^ { \prime }$ if the corresponding edge is being used (as a branch) in that tree. If certain conditions are met, then the node marks the ${ \mathrm { k } } { + } 1 ^ { \mathrm { t h } }$ and higher element of that edge as $\mathbf { \delta } ^ { \ast } \mathbf { X } '$ . This is done so that that edge is not reused in later trees. When a node is in the $\mathrm { n } ^ { \mathrm { t h } }$ (n>k) GHS execution (formation of T ), it will use an edge only if it finds that the $\mathrm { n } ^ { \mathrm { t h } }$ element of that edge array marked as ‘U’. As explained earlier, certain edges are allowed to overlap, in which case, the higher elements of those edges are not marked as ‘X’. As the algorithm progresses more trees are found and some of the previously used edges (elements in the edge array) are marked as $\mathbf { \hat { x } } _ { \mathbf { \hat { x } } } ,$ , making them unavailable in subsequent trees. There are two rule that determine which used edge not to be marked as ‘X’:

i. If the edge weight is below the minimum weight threshold, it may be shared by more than one multicast tree. In this case, a node will not mark higher elements of a recently used edge as unavailable (‘X’) for subsequent trees. Instead these elements will remain as ‘U’ thus making them available to the following GHS runs. However, if there is a bound on the number if edges that can be shared (for example a 3-edge overlapping multiple multicast trees), then a node can mark higher elements in the array as ‘X’ if this bound is reached.

ii.If the edge is a bridge connecting two components of the graph (e.g. Figure 5), this edge will be shared amongst all the multicast trees. A bridge edge is hard to detect. Section D explains how this condition is detected and handled.

In order to lower queuing delay on shared edges (and also to improve resource sharing), nodes in MEST will not re-use an edge if they have the option of choosing an un-used edge that falls below the threshold. This also gives rise to the possibility that the new trees that are generated are edgedisjoint. For example, if the cut-off threshold in Figure 4 was set to 6, MEST could generate edge-disjoint trees similar to Figure 4c.

There are no bounds on the number of trees that can be generated using MEST for implementing a particular multicast. The algorithm tries its best to select different set of edges in every iteration (each tree). However, it should be noted that beyond a certain point, there is no additional improvement in the resource utilization since all the edges have been used in at least one tree. Beyond a certain point, additional trees will be reusing edges used in at least one tree generated in an earlier iteration. This could possibly increasing the delay due to congestion along the edges that are most used.

# C. MEST Messages

Most of the message passing between the nodes is similar to the one used in GHS algorithm except for some minor modifications as explained here. Nodes in GHS belong to one of the three states: Sleeping state, Find state and Found state. A node is in the Sleeping state until it starts executing the protocol or is awaken by a message from another node. The two nodes adjacent to the core change their state to Find and start a new iteration by broadcasting an initiate message along the branches of the fragment. Upon receiving the initiate message, a node enters the Find state and forwards the initiate message to its neighbors (in the fragment). The initiate message thus propagates to all the nodes in the fragment. The initiate message contains the fragid and the fragment level. A node in Find mode updates its fragid and level number to the one in the initiate message. Next, the node picks its minimum weight edge incident on a node in another fragment. To check if an edge is going to a node in a different fragment, a node sends a test message (containing the node’s fragid and level number) across the edge. A node receiving a test message responds back with an ‘accept’ or a ‘reject’ message depending on whether it belongs to the same or different fragment as the sending node.

Once a node identifies its ‘best edge’, it sends a report message towards the fragment’s core. This report message contains the id and weight of its best edge. Interior nodes hold back their report message till it has received reports from all of its child nodes. The internal node’s report contains the smallest of its best edge or the outbound fragment branch on which has the minimum best edge was found. There are two interesting things to note. If a node is a leaf node, then its report message contains the basic edge weight as infinity. If no node has outgoing edge, then the algorithm is complete and the fragment is an MST of the graph. After the two nodes adjacent to the core have exchanged the report messages, the mwoe for that iteration is determined. A Change-core message is then sent over the branches of the fragment to indicate the new core. A connect message is exchanged by the two fragments over the mwoe before moving to the next level.

In the original GHS algorithm, a single degree node responds back with a report message containing the ‘best edge’ weight as infinity. In GHS, the node’s parent doesn’t do much with this information since its primary interest is in finding the smallest of its base edge or outgoing branch containing the smallest edge. In MEST, however, a node is able to examine only the edges that are marked usable (i.e. ‘U’). A node may finds that it is a single degree node for a particular run of GHS. This may be true for other trees (i.e. there might be other edges connecting that node to the rest of the graph). In MEST, a node will send negative infinity in its report message if it detects that it truly is a single degree node for the entire graph. Since there is only one edge connecting it to the rest of the graph, this edge has to be included in all the trees. When the node receives a negative infinity in a report from its child node, it will not mark all the elements in the edge array as ‘S’; thus making it available to subsequent trees.

# D. Bridge Condition

In MEST, we introduce a fourth state called Completed state. This state is reached when a GHS run terminates, i.e., when no node has any outgoing edge for that fragment. In plain GHS, this condition is reached when all the nodes have been found (i.e. a multicast tree for the graph has been found). In MEST however, since not all edges get examined, bridge edges might be missed leading to one or more fragments that have reached the Completed state. When a fragment attains the Completed state, the nodes adjacent to the core broadcast an override message along the branches of the fragment. Upon receiving an override message, a node checks to see if any of its unavailable edges connect to a different fragment. This check is carried out in the same manner as in GHS - by sending a test message (containing the node’s fragid and level number) across the edge. Upon receiving a test message, the node on the other side replies back with a reject (same fragment) or accept (different fragment) message. An override message from the core is replied back with an override response message. When the node receives an accept message from the other side, it sends the weight of the outgoing edge along with the response. In case of a reject message, it replies with infinity as the weight. If several override response messages are received by the core nodes, they pick the edge that has the smallest weight.

# E. MEST Example

![](images/da52e0bf0094d7d5c8e2417d89d9f1400859e6a2f4925c65e2e06f5bbf01db0e.jpg)



Figure 6: MEST example

Table I: Edge arrays after T1 

<table><tr><td>Node</td><td colspan="4">Edge Arrays</td></tr><tr><td>A</td><td> $E_B$ [B,X]</td><td> $E_D$ [R,U]</td><td> $E_E$ [B,X]</td><td> $E_F$ [R,U]</td></tr><tr><td>B</td><td> $E_A$ [B,X]</td><td> $E_C$ [B,S]</td><td> $E_E$ [R,U]</td><td> $E_F$ [R,U]</td></tr><tr><td>C</td><td> $E_B$ [B,S]</td><td></td><td></td><td></td></tr><tr><td>D</td><td> $E_A$ [R,U]</td><td> $E_E$ [B,U]</td><td></td><td></td></tr><tr><td>E</td><td> $E_A$ [B,X]</td><td> $E_B$ [R,U]</td><td> $E_D$ [B,U]</td><td> $E_F$ [B,U]</td></tr><tr><td>F</td><td> $E_A$ [R,U]</td><td> $E_B$ [R,U]</td><td> $E_E$ [B,U]</td><td></td></tr></table>

Table II: Edge arrays after T2 

<table><tr><td>Node</td><td colspan="4">Edge Arrays</td></tr><tr><td>A</td><td> $E_B$ [B,X]</td><td> $E_D$ [R,B]</td><td> $E_E$ [B,X]</td><td> $E_F$ [R,R]</td></tr><tr><td>B</td><td> $E_A$ [B,X]</td><td> $E_C$ [B,B]</td><td> $E_E$ [R,B]</td><td> $E_F$ [R,R]</td></tr><tr><td>C</td><td> $E_B$ [B,B]</td><td></td><td></td><td></td></tr><tr><td>D</td><td> $E_A$ [R,B]</td><td> $E_E$ [B,B]</td><td></td><td></td></tr><tr><td>E</td><td> $E_A$ [B,X]</td><td> $E_B$ [R,B]</td><td> $E_D$ [B,B]</td><td> $E_F$ [B,B]</td></tr><tr><td>F</td><td> $E_A$ [R,R]</td><td> $E_B$ [R,R]</td><td> $E_E$ [B,B]</td><td></td></tr></table>

We illustrate the working of MEST by using Figure 6 (slight modification of Figure 4) as an example. The weight threshold for reusing edges is set to 5. At the end of the first GHS run, the edge array entries at various nodes are as shown in Table I. Edge BC is marked special, which edge DE and EF are re-usable in the second tree since they fall below the threshold. Table II shows the array entries after the second tree has been constructed. Although this is a simple example showing two multicast trees, in real network scenarios we may have a more complex graph with higher connectivity that gives several multicast trees.

# V. SIMULATIONS

Simulations were carried out using Network Simulation (ns2.26) [1]. As of this writing, ns2 doesn’t have any extension for simulating overlay multicast in MANETs. With the help of C-programming and bash/tcl scripting, the traffic pattern generated by CMU’s cbrgen utility was modified to represent an overlay network. Additional modules were written to simulate our MEST algorithm (for multiple trees) and the Prim’s algorithm [7] (for generating a single MST).

In all the result graphs, MST corresponds to the results for a single tree multicast in which the multicast spanning tree is a minimum spanning tree built using Prim’s algorithm. The setdest utility was used to generate different node positions and movement patterns. The nodes in the simulation move according to the ‘random waypoint’ model [13]. Table III shows the default simulation parameters. In the following subsections, simulation parameters when not mentioned follow the one given in this table. All the simulation results are average of 25 random scenarios.

Table III: Simulation Parameters 

<table><tr><td>Simulation Area</td><td>500x500  $m^{2}$ </td></tr><tr><td>Total number of nodes</td><td>150</td></tr><tr><td>Number of member nodes</td><td>15, 20, 25, 30</td></tr><tr><td>Packet size</td><td>512 bytes</td></tr><tr><td>Total File size</td><td>512000 bytes</td></tr><tr><td>Ad-hoc Routing Protocol</td><td>DSR [13]</td></tr><tr><td>Pause Time</td><td>10 sec</td></tr><tr><td>Max speed</td><td>5 m/sec</td></tr></table>

![](images/516774351d738fb7708eab8403ad837e52d26f51e029a8b4f6c3dae7e2fb3537.jpg)



a) Showing latency for all node sizes

![](images/163f0416bac1b8e1972e7dca1ee4146421350fd8567e8c4c6d32ea7b9833e5c3.jpg)



b) Comparing latency of MEST for 20 & 30 nodes w.r.t. MST

![](images/51e4b48bfa4c65f48c6d67037b054142e541730559fc81a6fa4103030b604ae8.jpg)



c) Showing no. of leaves for all node sizes

![](images/84723cb686750d7e6143172da1944ca46c779b9753615a0af79cbc5d6fcefd77.jpg)



d) Comparison between MEST 20 & 30 nodes w.r.t. their respective MST.   
Figure 7: Effect of threshold on delay and utilization.

# A. Threshold vs Latency/Leaves

Simulation results from Figure 7 show that there is a significant reduction in the multicast latency along with better utilization (fewer leaves) of the available network resources. Part of this improvement can be attributed to the parallel transmission over multiple trees. A close examination reveals that for this setup, the optimal threshold value is 75m. At 75m, the number of leaves in the overall multicast was minimum while the delay was near minimum. Another observation was that the performance curves tend to ‘flatten-out’ for higher threshold values. This is because at higher thresholds, more edges are allowed to overlap. When an edge is used in multiple trees, it encounters congestion delays since it has to handle packets for multiple trees. This delay is insignificant when the edge weight is small. However, when the threshold is high, longer edges are also allowed to overlap. In such cases, the congestion delays are comparable with the edge delays and hence, for higher threshold, the delay starts to increase. In the worst case, when the delay is set to infinity, all the MEST trees would correspond to the same tree.

# B. Overlap Index

As seen from Figure 8, the edge overlap increased with higher number of trees. This means that there would be more edges that are being re-used in multiple trees. This could potentially create congestion issues since the edge has to ‘serve’ several trees. We also observed a slight increase in the overlapping as the threshold value increases. This is expected as higher thresholds allow more edges to overlap. Also Figure 8a & b show that there is a slight increase in the overlap index as the number of member nodes increases.

# VI. CONCLUSION AND FUTURE WORK

We present MEST, a distributed algorithm for building multiple multicast trees in ad hoc environment. MEST is easy to implement and can work with any distributed algorithm for generating minimum spanning trees. Our simulation results show that MEST can significantly reduce the multicast delay and at the same time improve the network utilization. Although this paper describes MEST with reference to overlay multicast in MANETs, it should be noted however, that the concept of MEST can be easily extended to multicast in wired networks by considering stationary nodes or network layer (IP) multicast in MANETs.

![](images/5cc9bf4482a72b9844e833a6d2dfa90dc26db71c305bd88961f7bc2fb4f636f8.jpg)



a)

![](images/65d066902f4e354e51b7685601eaf7ff91c0331166c0536b7952e2dcdd4e4bbc.jpg)



Figure 8: Overlap index for multiple trees

In addition, even though the design of MEST was not meant to solve reliability issues, it can also be used to build a reliable mesh network - in which case, the same multicast data will be sent over different sub-trees (i.e. the multicast data won’t be split into smaller fragments).

Our currently work was targeted for small group multicast networks. In the future, we will focus our attention in making modifications to MEST so that it can work with a larger (multicast) group size. In our present idea, we have reduced the multicast delay by building low weight spanning trees. In the future, we will attempt to build multicast trees where the source node has a low eccentricity. Such trees would have a low multicast delay since the source node would have a shortest path with every node in tree. Existing algorithms for generating shortest path (low source eccentricity) tree pay little attention to the network utilization issues.

# REFERENCE

[1] "The Network Simulator - ns-2," http://www.isi.edu/nsnam/ns/.   
[2] B. Awerbuch, "Optimal distributed algorithms for minimum weight spanning tree, counting, leader election, and related problems," presented at STOC, 1987   
[3] B. Awerbuch, "Randomized distributed shortest paths algorithms," presented at Annual ACM Symposium on Theory of Computing, Seattle, Washington, 1989   
[4] E. Bommaiah, M. Liu, A. MvAuley, and R. Talpade, "AMRoute: Ad Hoc Multicast Routing Protocol," presented at Internet Draft, draftmanet-amroute-00.txt, March, 2002   
[5] K. M. Chandy and J. Misra, "Distributed computation on graphs: shortest path algorithms," Communications of the ACM, vol. 25, pp. 833 - 837, Nov 1982   
[6] K. Chen and K. Nahrstedt, "Effective Location - Guided Tree Construction Algorithm for Small Group Multicast in MANET," presented at IEEE INFOCOM, May, 2002   
[7] T. H. Cormen, C. E. Leiserson, and R. L. Rivest, Introduction to Algorithms. Cambridge, Mass., New York: MIT Press, McGraw-Hill, 1990   
[8] R. G. Gallager, P. A. Humblet, and P. M. Spira, "A distributed algorithm for minimum-weight spanning trees," ACM TOPLAS, vol. 5, pp. 66-77, January 1983   
[9] M. S. Gast, 802.11 Wireless Networks, A definitive Guide: O'Reilly Networking, April 2002

[10] C. Gui and P. Mohapatra, "Efficient Overlay Multicast for Mobile Ad Hoc Networks," presented at Wireless Communications and Networking Conference (WCNC), March, 2003   
[11] P. Humblet, "Another adaptive distributed shortest path algorithm," IEEE/ACM Transactions on Communications, vol. 39, pp. 995-1003, Jun. 1991   
[12] J. Jannotti, D. Gifford, K. Johnson, M. Kaashoek, and J. O’Toole, "Overcast: Reliable multicasting with an overlay network," presented at Fourth Symposium on Operating System Design and Implementation (OSDI), San Diego, CA, October 2000   
[13] D. Johnson and D. Maltz, "Dynamic source routing in ad hoc wireless networks," in Mobile Computing, 1996   
[14] S. Lee, R. Sherwood, and B. Bhattacharjee, "Cooperative Peer Groups in NICE," presented at IEEE INFOCOM 2003, April 2003   
[15] M. Castro, P. Druschel, A.-M. Kermarrec, A. Nandi, A. Rowstron, and A. Singh, "SplitStream: High-bandwidth multicast in a cooperative environment," presented at SOSP'03, Lake Bolton, New York, October, 2003   
[16] M. F. Mokbel, W. A. Elhaweet, and M. N. Elderini, "An Efficient Algorithm for Shortest Path Multicast Routing Under Delay and Delay Variation constraints," presented at Symposium on Performance Evaluation of Computer and Telecomm. Systems, SPECTS, Vancouver, Canada., 2000   
[17] K. Obraczka, G. Tsudik, and K. Viswanath, "Pushing the Limits of Multicast in Ad Hoc Networks," presented at IEEE ICDCS,, April, 2001   
[18] P.Antoniadis and C.Courcoubis, "Market Models for P2P Content Distribution," http://citeseer.nj.nec.com/560319.html.   
[19] A. Patil, Y. Liu, L. Xiao, A.-H. Esfahanian, and L. M. Ni, "SOLONet: Sub-Optimal Location-Aided Overlay Network for MANETs," presented at IEEE International Conference on Mobile Ad-hoc and Sensor Systems, MASS 2004, Fort Lauderdale, Florida, October 2004   
[20] A. Rowstron and P. Druschel, "Pastry: Scalable, distributed object location and routing for large-scale peer-to-peer systems," presented at IFIP/ACM International Conference on Distributed Systems Platforms (Middleware), Heidelberg, Germany, November, 2001   
[21] A. Rowstron, A.-M. Kermarrec, M. Castro, and P. Druschel, "SCRIBE: The design of a large-scale event notification infrastructure," presented at NGC2001, UCL, London, November 2001   
[22] G. Singh and A. J. Bernstein, "A highly asynchronous minimum spanning tree protocol," Distributed Computing, vol. 8, 1995   
[23] B. Wang and S. K. S. Gupta, "On maximizing lifetime of multicast trees in wireless ad hoc networks," presented at International Conference on Parallel Processing, ICPP-03, Kaohsiung, Taiwan, October 2003   
[24] A. Young, J. Chen, Z. Ma, A. Krishnamurthy, L. Peterson, and R. Y. Wang, "Overlay Mesh Construction Using Interleaved Spanning Trees," presented at INFOCOM 2004, March 2004