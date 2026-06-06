# Resource Allocation Using Multiple Edge-Sharing Multicast Trees

Abhishek Patil, Abdol-Hossein Esfahanian, Yunhao Liu, Senior Member, IEEE, and Li Xiao, Member, IEEE

Abstract—A typical multicast network consists of a single tree, in which only a few internal nodes contribute most resources and are involved in performing the multicast functionality. This leads to an uneven and inefficient utilization of network resources. The problem is more pronounced in mobile ad hoc networks (MANETs), where network resources are limited. One solution is to split the multicast content over a number of trees. This provides several paths for the multicast content and would involve more nodes in implementing multicast functionality. Although this approach improves network utilization, overall multicast latency increases. This paper presents a distributed algorithm to construct multiple edge-sharing trees (MESTs) for small group multicast. MESTs balance the resource allocation and delay constraints by choosing to overlap certain edges that have low weight. Simulation results show that MESTs can generate multicast networks that have low delays and fair resource utilization. MESTs are designed to work with any form of multicast in both wired and wireless networks.

Index Terms—Fair resource allocation, minimum spanning tree (MST), mobile ad hoc networks (MANETs), multicast.

# I. INTRODUCTION

HE CONCEPTS presented in this paper can be applied to any form of multicast—wired or wireless networks. However, as a continuation of our previous research [10], [12], the work presented here focuses mostly on overlay multicast in wireless mobile ad hoc networks (MANETs). Our work can easily be adapted to other forms of multicast. MANETs are characterized by mobile nodes and a constantly changing network topology. Implementing multicast in such a dynamic environment is not an easy task. Due to its ease of implementation and flexibility to adapt, overlay multicast networks are finding many practical applications in MANETs. Similar to other tree-based multicast networks, overlay multicast also

Manuscript received December 5, 2006; revised September 23, 2007 and November 1, 2007. This work was supported in part by the U.S. National Science Foundation under Grant CCF-0514078, Grant CNS-0551464, and Grant CNS-0721441, by the National High Technology Research and Development Program of China (863 Program) under Grant 2007AA01Z180, and by The Hong Kong University of Science and Technology Nansha Research Fund under Contract NRC06/07.EG01. The review of this paper was coordinated by Dr. L. Cai.

A. Patil is with Kiyon, Inc., San Diego, CA 92121 USA (e-mail: patilabh@ msu.edu).

A.-H. Esfahanian and L. Xiao are with the Department of Computer Science and Engineering, Michigan State University, East Lansing, MI 48824 USA (e-mail: esfahanian@cse.msu.edu; lxiao@cse.msu.edu).

Y. Liu is with the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Kowloon, Hong Kong (e-mail: liu@cs.ust.hk).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TVT.2007.913183

suffers from the resource utilization problem. In a typical multicast tree, only a small number of nodes are actively involved in implementing multicast functionality. For example, there are a few internal nodes that perform the task of duplicating and forwarding packets and a large number of leaf nodes that only act as receivers of packets. These leaf nodes do not contribute any resources to the multicast tree. MANETs are characterized by scarce network resources. Due to this uneven distribution of responsibility, certain nodes will run out of resources (e.g., battery strength) faster than other nodes, leading to bottleneck nodes in the multicast trees. The lifetime of a multicast tree depends on the lifetime of a bottleneck node. Proper resource allocation is essential for extending the life of an overlay (or any) multicast network.

The delay (or latency) in a multicast tree is equal to the time that it takes for all the leaf nodes to receive the packets (data) sent by the source node. There are two main techniques that can help bring down this delay: 1) reducing source eccentricity and 2) reducing the tree weight. The edge weight could indicate a variety of link parameters or a combination of several such parameters (like bandwidth, signal strength, round trip time, etc.). In this paper, edge weight refers to the edge length—i.e., the distance between two nodes. In most networks (e.g., wireless), this would also indicate the network delay. The first approach tries to reduce the source node’s eccentricity. The eccentricity εG(v) of a node v in a connected graph G is the length of the longest of all the shortest paths between v and every other node in G. A higher fan-out at interior nodes results in a low depth tree (i.e., smaller source eccentricity), thus having a shorter delay. However, such a tree would have a large number of leaf nodes. For example, a binary tree has 50% leaf nodes [9], whereas a tree with an average fan-out of 16 will have 90% leaf nodes. Thus, it is necessary to have an overlay multicast tree that maintains a good balance between the multicast latency and utilization of network resources. There are many distributed algorithms for generating shortest path trees; however, most of them pay little attention to the network utilization issues. The other method focuses on constructing low-weight trees. The weight of a tree is the sum of the weights of its edges.

This paper concentrates on constructing several low-weight multicast trees to reduce the overall delay. We present a distributed algorithm for building multiple edge-sharing trees (MESTs) for small group multicast. MESTs aim to uniformly distribute the multicast functionality across all the nodes in the group with little impact on the multicast delay. A MEST can work with any distributed algorithm to construct minimum spanning trees (MSTs). This paper describes a MEST with respect to the Gallager, Humblet, and Spira (GHS) algorithm [2].

![](images/22e0b9f224ed1c1a52bcb9fbba98f5fcec4a1910a74b2c7736e90b25aa3d7662.jpg)



Fig. 1. Multicast content split into smaller pieces and sent over multiple trees.

A MEST constructs several multicast trees in the same network. Each tree constitutes a separate subgroup, and all the nodes participating in the multicast subscribe to these subgroups. The multicast content is split into several smaller stripes, and each stripe is then sent over one of the multicast trees (Fig. 1). Many papers propose the use of multiple multicast trees for creating a redundant mesh network that improves the overall reliability. Although improving reliability is not a MEST’s primary objective, the MEST algorithm can also be used in building a reliable redundant mesh network. In such a network, the multicast content is not split into smaller stripes; instead, each MEST multicast tree will provide an alternative path to the multicast data. If one path fails, the nodes can reroute the data over an alternative path.

This paper presents several simulation scenarios that examine the scalability and performance of a MEST. The simulations investigated several aspects of the protocol, like the threshold value, the number of multiple trees, the effect of file fragmentation (equal or unequal fragment sizes), and the overlap index. The results indicate that a MEST is scalable and has a lower delay, as compared to a single-tree overlay multicast network. It also highlights many interesting observations that are being considered in our future research.

The rest of this paper is structured as follows. Section II examines previous work done in this area. Section III provides a detailed description of our algorithm. Section IV presents simulation results to analyze and compare MESTs. Finally, Section V concludes this paper and presents directions for future research.

# II. RELATED RESEARCH

Several overlay multicast protocols have been proposed and studied for MANETs. All of them are based on single-tree multicast and are geared to address the efficiency issues of overlay multicast. In recent years, the issue of resource allocation has caught the attention of many researchers.

Like a MEST, the SplitStream algorithm [9] tries to distribute the multicast load by constructing multiple multicast trees. However, SplitStream is based on a complex infrastructure and requires the help of nonmembers to construct multicast trees. The expected amount of state maintained by each node is $O ( \log | N | )$ . The expected number of messages to build the forest is $O ( | N | \log | N | )$ if the trees are well balanced or $O ( | N | ^ { 2 } )$ in the worst case. MESTs, on the other hand, are much simpler and do not require any help from the nonmember nodes, thus making them compatible with any kind of underlying network. Although SplitStream focuses on improving the resource utilization of the network, it does not pay much attention to the delay constraints. The algorithm attempts to accommodate member nodes with different bandwidth capacities. In doing so, it makes use of the Scribe mechanism to limit the number of outgoing connections from a member node. As a result, a new node would be forced to connect further down the tree, resulting in a higher delay.

Young et al. [11] suggested a k-MST algorithm to build a reliable mesh structure. The algorithm builds multiple edgedisjoint MSTs and works by removing an edge from the graph once it is used by a tree. This tends to build trees that greatly vary in their weight and, hence, the multicast latency. During the later stages of such an algorithm, the newer trees end up having the high-weight edges (which were rejected by the earlier trees). The final tree would be the one with the highest delay, because it is using all the high-weight edges that were not used by the earlier trees. The k-MST algorithm differs from a MEST since it tries to build edge-disjoint multiple trees and has a primary goal of constructing a mesh network. In the k-MST algorithm, if one tree fails, data can be sent over another redundant tree. However, the multicast delay would increase as the data is being transferred over a tree with a high weight. It should be noted that such a method works well only for a mesh case. It cannot be used for addressing the resource allocation problem due the delay involved in simultaneous transfer of multicast content would be unacceptable. Some of the content would come over a tree that has the highest weight (maximum delay).

The strategies adopted in [7] and [8] are essentially different from ours. They rely on accounting and charging methods to solve the unfairness problem: Group members that served as a forwarder node charge their child(ren) node for the service that they receive. Overcast [6] maintains a single tree and uses a dedicated server to optimize the bandwidth utilization across the network.

# III. MEST ALGORITHM

A MEST can be considered as several instances of a modified GHS algorithm [2] running in a sequence, one after the other. At the start, all the nodes run the GHS algorithm to produce the first tree (T1), then the second run gives tree $T _ { 2 }$ , and so on, until the desired number of multicast trees has been generated.

# A. Preliminaries

In cases where there are multiple multicast trees, the highest weight multicast tree contributes the most delay; thus, the delay of the overall system is determined by this (highest weight) tree. Edge-disjoint multicast trees use different edges in each tree. Therefore, they would do a better job in solving the resource allocation problem. However, if they are not constructed correctly, they are a poor choice when it comes to meeting the delay requirement. An example is shown in Fig. 2, where node D is the source of multicast content. For this graph, it is possible to find many pairs of edge-disjoint spanning trees. Two such pairs are shown [Fig. 2(b) and (c)]. In Fig. 2(b), $T _ { 1 }$ is an MST, whereas its counterpart $T _ { 2 }$ has very high latency. This is because it is forced to use all the high-weight edges that were rejected by $T _ { 1 }$ . The network resources are evenly used between the two trees; however, the overall multicast delay would be determined by $T _ { 2 }$ . On the contrary, in the case of Fig. 2(c), the lightweight edges are equally distributed between the two spanning trees; hence, the overall delay is lower compared to the earlier case. Now, consider the case where two trees share an edge. Fig. 2(d) shows two spanning trees (one of them minimum) that have two common edges (DE and EF). Such a multicast tree may be obtained by having a condition that allows the overlap of edges that satisfy certain criteria (e.g., edges with lengths below a certain threshold or edges connected to nodes that have low degrees). This threshold should be wisely chosen. A very high value would lead to several overlapping edges, decreasing the network utilization. A very low value would increase the multicast latency. In the example, we chose the cutoff threshold for edge sharing to be five. Different thresholds would produce different degrees of edge overlap among trees.

![](images/00c1e73c48ab5a6a8aa6e3e32a593000d196785bec00d16df09f62a9557aaf53.jpg)  
Fig. 2. Edge-disjoint versus edge-overlapping trees. (a) Original graph. (b) Edge-disjoint spanning trees—high delay. (c) Edge-disjoint spanning trees—reduced delay. (d) Edge-overlapping spanning trees—low delay.

1) Other Factors That Affect Delay: In case of edge-sharing trees, a factor that might affect the delay is the number of times that an edge is reused. This is important because a shared edge has to carry packets for different multicast groups that use it in their multicast trees. For example, in Fig. 2(d), the two common edges (DE and EF) have to carry packets for both the trees. A packet would be queued at a node if it is currently sending or receiving another packet over the common edge. In case of streaming applications, this delay would always be present since there is a constant stream of data to be sent by the node. To eliminate delays due to queuing, we suggest setting an upper bound on the number of trees that can share a particular low-weight edge. Since each application has its own specific requirement, the upper bound would be application dependent.   
2) Special Cases: A bridge is an edge of a graph whose removal will result in a disconnected graph. For graphs that contain a bridge edge, it is not possible to have multiple trees that are completely edge disjoint. In the example shown in

![](images/762053c40a923411ae70e8084b45313a2f168df3ed9614dc0de86c62b0d08217.jpg)



Fig. 3. Example of bridge edge.   
Fig. 3, edge BG is a bridge edge and will be present in any spanning tree of this graph. Our MEST algorithm has a special stage called the “completed state,” which identifies bridge edges. Our algorithm marks a bridge edge as “S” to indicate that this is a special-case edge, which has to be included in all the spanning trees.

# B. Construction of MEST

Let us say we have a network of $" n "$ nodes and that we want to construct $" m "$ multicast trees $( T _ { 1 } , T _ { 2 } , \ldots , T _ { m } )$ with a few overlapping edges (satisfying a particular threshold criteria). At the start $( t = 0 )$ , each node runs an instance of the GHS algorithm, and there are $^ { \ast } m \times n ^ { \prime \prime }$ fragments. Each node maintains a variable called the frigid, which stores the fragment ID of the components with which the node is currently associated. Nodes also maintain arrays of length “m” for each of their edges. The $" m "$ elements of the array correspond to the “m” trees, where the edge can potentially be a branch. As an example, if a node had three edges and we were looking to construct two edgesharing spanning trees, then that node would maintain three arrays each of length two. Fig. 4 shows one such example: Here, we have considered two nodes B and E, each having four edges. Each edge array would have three elements, each corresponding to a multicast tree. At the end of the MEST algorithm, the value of each element would reflect the status of that edge for a particular tree. Each element of the edge array can be marked with one of the following values by the MEST algorithm.

“B” Edge that forms a branch in the current tree.   
“R” Rejected edge: Edge by the current tree since it joins another node of the same fragment.   
“U” Usable edge (basic edge): Edge checked to see if it is the best edge for this node.   
$\mathbf { \ddot { \delta t } X } ^ { \prime \prime }$ Unusable edge: Edge used by an earlier tree.   
“S” Mandatory edge (e.g., bridge edge): Special case.

At the start, edge arrays at each node are initialized so that every element in the array is marked as “U.” This allows the first run of GHS to choose any edge that it wants.

Thus, in a way, the first tree is a true MST for that graph. During the formation of the kth tree, a node will mark the kth element of an edge array as $\mathbf { \ddot { \delta } } \mathbf { \delta B } ^ { \prime \prime }$ if the corresponding edge is being used in that tree. If certain conditions are met, then the node marks the $k +$ 1th and higher element of that edge as “X.” This is done so that the edge is not reused in later trees. For edges that are allowed to overlap, the higher elements are marked usable (i.e., they are left as “U”). When a node is in the nth $( n > k )$ GHS execution (formation of $T _ { n } )$ , it will use an edge only if it finds that the nth element of that edge array is marked as “U.” As the algorithm progresses, more trees are found, and some of the previously used edges are marked as “X,” making them unavailable in subsequent trees. The following two rules determine which used edge is not marked as “X.”

1) If the edge weight is below the minimum weight threshold, it may be shared by more than one multicast tree. In this case, the edge will be left marked as “U” (i.e., usable), thus making them available to the following GHS runs.   
2) If the edge is a bridge that connects two components of the graph (e.g., Fig. 3), it will be shared among all the multicast trees. A bridge edge is hard to detect. Section III-E explains how this condition is detected and handled.

To lower the queuing delay on shared edges (and to improve resource sharing as well), nodes in a MEST will not reuse an edge if they have the option of choosing an unused edge that falls below the threshold. This helps increase the possibility that new trees generated are edge disjoint (good for resource utilization). For example, if the cutoff threshold in Fig. 2 were set to six, a MEST would have generated edge-disjoint trees similar to those in Fig. 2(c).

There are certain bounds on the number of trees that can be generated using a MEST. The algorithm tries its best to select a different set of edges while generating each tree. However, beyond a certain point, there is no additional improvement in the resource utilization since all the edges have been used in at least one tree. After a certain point, additional trees will reuse edges used in at least one tree generated in an earlier iteration. Excessive reuse of edges would increase the delay due to congestion caused by packets that belong to different trees that pass along the shared edges. Therefore, it is important to set an upper bound on the number of trees generated using a MEST. We have observed that it is beneficial to keep this number equal to or less than the connectivity of the graph.

# C. MEST Messages

Messages that pass between the nodes would be similar to the underlying MST algorithm (e.g., GHS). Nodes in GHS belong to one of the following three states: 1) sleeping; 2) find; and 3) found. A node is in the sleeping state until it starts executing the protocol or is awoken by a message from another node.

# D. Identifying Single-Degree Nodes

In the original GHS algorithm, a single-degree node (i.e., a node with only one edge) responds back with a report message that contains the “best edge” weight as infinity. In GHS, the node’s parent does not do much with this information because its primary interest is in finding the smallest of its base edge or outgoing branch that contains the smallest edge. In a MEST, however, a node is able to examine only the edges that are marked usable (i.e., “U”). A node may find that it is a single-degree node for a particular run of GHS. This may be true for other trees (i.e., there might be other edges that connect that node to the rest of the graph). In a MEST, a node will send negative infinity in its report message if it detects that it truly is a single-degree node for the entire graph. Since there is only one edge that connects it to the rest of the graph, this edge must be included in all the trees. When the node receives a negative infinity in a report from its child node, it will not mark all the elements in the edge array as “S,” thus making it available to subsequent trees.

![](images/5b18708e90980e876434ce3660f68f02add74f5c95ff6db26c0cad33c4c6871d.jpg)



Fig. 4. Example of edge array at each node for three-tree MEST.   
![](images/2ccff081c7f6e363364e758e53ab10b95b0cc36da64cde7237bfb2e268bcf3d9.jpg)



Fig. 5. MEST example.

# E. Bridge Condition

In a MEST, we introduce a fourth state called the completed state. This state is reached when a GHS run is terminated—i.e., an MST has been found. In a MEST, however, this is not true. Bridge edges could be missed, leading to one or more fragments that have reached the completed state. When a fragment attains the completed state, the nodes that are adjacent to the core broadcast an override message along the branches of the fragment. Upon receiving an override message, a node checks to see if any of its unavailable edges connect to a different fragment. This check is carried by sending a test message (containing the node’s fragid and level number) across the edge. Upon receiving a test message, the node on the other side replies back with a reject (same fragment) or accept (different fragment) message. An override message from the core is sent back with an override response message. When the node receives an accept message from the other side, it sends the weight of the outgoing edge along with the response. In the case of a reject message, it replies with infinity as the weight. If the core nodes receive several override response messages, they pick the edge that has the smallest weight.

TABLE I EDGE ARRAYS WHEN MEST STARTS 

<table><tr><td>Node</td><td colspan="4">Edge Arrays</td></tr><tr><td>A</td><td> ${\mathrm{E}}_{\mathrm{{AB}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{AD}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{AE}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{AF}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td></tr><tr><td>B</td><td> ${\mathrm{E}}_{\mathrm{{BA}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{BC}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{BE}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{BF}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td></tr><tr><td>C</td><td> ${\mathrm{E}}_{\mathrm{{CB}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td></td><td></td><td></td></tr><tr><td>D</td><td> ${\mathrm{E}}_{\mathrm{{DA}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{DE}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td></td><td></td></tr><tr><td>E</td><td> ${\mathrm{E}}_{\mathrm{{EA}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{EB}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{ED}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{EF}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td></tr><tr><td>F</td><td> ${\mathrm{E}}_{\mathrm{{FA}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{FB}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{FE}}}\left\lbrack {\mathrm{U},\mathrm{U}}\right\rbrack$ </td><td></td></tr></table>

TABLE II EDGE ARRAYS AFTER $T _ { 1 }$ 

<table><tr><td>Node</td><td colspan="4">Edge Arrays</td></tr><tr><td>A</td><td> $E_{AB}[B,X]$ </td><td> $E_{AD}[R,U]$ </td><td> $E_{AE}[B,X]$ </td><td> $E_{AF}[R,U]$ </td></tr><tr><td>B</td><td> $E_{BA}[B,X]$ </td><td> $E_{BC}[B,S]$ </td><td> $E_{BE}[R,U]$ </td><td> $E_{BF}[R,U]$ </td></tr><tr><td>C</td><td> $E_{CB}[B,S]$ </td><td></td><td></td><td></td></tr><tr><td>D</td><td> $E_{DA}[R,U]$ </td><td> $E_{DE}[B,U]$ </td><td></td><td></td></tr><tr><td>E</td><td> $E_{EA}[B,X]$ </td><td> $E_{EB}[R,U]$ </td><td> $E_{ED}[B,U]$ </td><td> $E_{EF}[B,U]$ </td></tr><tr><td>F</td><td> $E_{FA}[R,U]$ </td><td> $E_{FB}[R,U]$ </td><td> $E_{FE}[B,U]$ </td><td></td></tr></table>

TABLE III EDGE ARRAYS AFTER $T _ { 2 }$ 

<table><tr><td>Node</td><td colspan="4">Edge Arrays</td></tr><tr><td>A</td><td> ${\mathrm{E}}_{\mathrm{{AB}}}\left\lbrack  {\mathrm{B},\mathrm{X}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{AD}}}\left\lbrack  {\mathrm{R},\mathrm{B}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{AE}}}\left\lbrack  {\mathrm{B},\mathrm{X}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{AF}}}\left\lbrack  {\mathrm{R},\mathrm{R}}\right\rbrack$ </td></tr><tr><td>B</td><td> ${\mathrm{E}}_{\mathrm{{BA}}}\left\lbrack  {\mathrm{B},\mathrm{X}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{BC}}}\left\lbrack  {\mathrm{B},\mathrm{B}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{BE}}}\left\lbrack  {\mathrm{R},\mathrm{B}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{BF}}}\left\lbrack  {\mathrm{R},\mathrm{R}}\right\rbrack$ </td></tr><tr><td>C</td><td> ${\mathrm{E}}_{\mathrm{{CB}}}\left\lbrack  {\mathrm{B},\mathrm{B}}\right\rbrack$ </td><td></td><td></td><td></td></tr><tr><td>D</td><td> ${\mathrm{E}}_{\mathrm{{DA}}}\left\lbrack  {\mathrm{R},\mathrm{B}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{DE}}}\left\lbrack  {\mathrm{B},\mathrm{B}}\right\rbrack$ </td><td></td><td></td></tr><tr><td>E</td><td> ${\mathrm{E}}_{\mathrm{{EA}}}\left\lbrack  {\mathrm{B},\mathrm{X}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{EB}}}\left\lbrack  {\mathrm{R},\mathrm{B}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{ED}}}\left\lbrack  {\mathrm{B},\mathrm{B}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{EF}}}\left\lbrack  {\mathrm{B},\mathrm{B}}\right\rbrack$ </td></tr><tr><td>F</td><td> ${\mathrm{E}}_{\mathrm{{FA}}}\left\lbrack  {\mathrm{R},\mathrm{R}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{FB}}}\left\lbrack  {\mathrm{R},\mathrm{R}}\right\rbrack$ </td><td> ${\mathrm{E}}_{\mathrm{{FE}}}\left\lbrack  {\mathrm{B},\mathrm{B}}\right\rbrack$ </td><td></td></tr></table>

# F. MEST Example

We illustrate the construction of a MEST by using Fig. 5 as an example. The weight threshold for reusing edges is set to 5. When the algorithm starts, each node’s edge array elements are initialized to “U” (Table I), indicating that all the edges are usable. At the end of the first run, the array entries at various nodes are updated, as shown in Table II. Edge BC is marked as special (since it is a bridge edge), whereas edges DE and EF are reusable in the second tree since they fall below the threshold. Table III shows the array entries after the second tree has been constructed. Although this is a simple example that shows two multicast trees, in real network scenarios, we may have a more complex graph with higher connectivity that gives several multicast trees.

# G. Complexity Analysis

Complexity of a MEST will depend on the underlying MST algorithm. In this paper, since we describe MESTs with GHS as the underlying MST algorithm, we analyze its complexity with respect to GHS. The GHS algorithm has a message complexity of $O ( E + N$ log N ) and a time complexity of O(N log N ). Our MEST algorithm is essentially “m” repetitions of the GHS algorithm, except for the last step (completed state). During a particular GHS run, when each fragment reaches the completed state, the complexity for each fragment is the same as GHS: $O ( E _ { i } + N _ { i }$ log Ni), where $E _ { i }$ (and $N _ { i } )$ are the number of edges (and nodes) in fragment i. For a particular run, these fragments merge along their shortest outgoing edges, ultimately forming one fragment, which is the spanning tree (for the

TABLE IV SIMULATION PARAMETERS 

<table><tr><td>Simulation Area</td><td>500x500  $m^{2}$ </td></tr><tr><td>Total number of nodes</td><td>150</td></tr><tr><td>Number of member nodes</td><td>15, 20, 25, 30</td></tr><tr><td>Packet size</td><td>512 bytes</td></tr><tr><td>Total File size</td><td>512000 bytes</td></tr><tr><td>Ad-hoc Routing Protocol</td><td>DSR</td></tr><tr><td>Pause Time</td><td>10 sec</td></tr><tr><td>Max speed</td><td>5 m/sec</td></tr></table>

original graph) that was generated for that run. It should be noted that

$$
\sum E _ {i} = E _ {\text { total }} - \text { number   of   fragments } - 1. \tag {1}
$$

During the completed state, the following messages are generated in each fragment: 1) override; 2) override response; 3) test; 4) reject; 5) connect; and 6) change core. Therefore, the total number of messages is proportional to number of fragments − 1 (the last fragment does not need to exchange any messages—it is the final tree). Thus, the overall complexity of the MEST algorithm is $" m "$ times that of GHS. Now, because the number of MEST trees $( ^ { 6 6 } m ^ { 3 } )$ is much less than the total number of nodes in the topology $\binom { 6 6 } { 5 } N ^ { 5 } )$ , the complexity of MESTs can be expressed as $O ( E + N$ log N ), which is the same as that for GHS. The complexity of MESTs is lower when they run over other MST algorithms like [3] or [4], which have a better complexity compared to GHS. Techniques from [5] can also help improve the complexity.

# IV. SIMULATIONS

Simulations were carried out using Network Simulation (ns2.26). As of this writing, ns2 does not have any extension for simulating overlay multicast in MANETs. With the help of C-programming and bash/tcl scripting, the traffic pattern generated by CMU’s cbrgen utility was modified to represent an overlay multicast network in MANETs. Additional modules were written to generate multiple multicast trees based on our MEST algorithm. Prim’s algorithm finds an MST for a connected weighted graph. We used a code that implements Prim’s algorithm [1] (adjacency matrix searching) for generating an arbitrary MST of a given graph. This MST was used to generate a single-tree overlay multicast network.

Based on the results from our previous work [10], [12] with overlay multicast, we decided to use dynamic source routing as the ad hoc routing protocol and a packet size of 512 B for all the simulations. The setdest utility was used to generate different node positions and movement patterns. The nodes in the simulation move according to the “random waypoint” model. Table IV shows the default simulation parameters. Each simulation result is an average of 25 samples. In all the simulations, the edge weight for a link between two nodes is directly proportional to the distance between them, and a lower threshold corresponds to preferred edges.

# A. MEST versus Single Tree

The first set of simulations was intended to compare the performance of single-tree (overlay) multicast with (overlay)

![](images/a4904095b1b1648925c0c2e2a9295d0ea0c688ef377dc54ef1c78a2a79a00ae5.jpg)



![](images/0ea918507da1bbf2ea9ed37e6993e369e9978a014f9d8e4e12fdc13b12517723.jpg)



Fig. 6. Single tree versus MESTs with respect to delay and utilization. (a) Comparing latency of MESTs with single tree. (b) Comparing utilization between MESTs and single tree.   
![](images/f99f2a3708b299d91ef31d7d1af4ceb5347ad19ee9a57fb792344f520dc9294e.jpg)



(a)

![](images/f26ac2a64ceca1e8f9273ea3608e606197cddb4823910934b8c5a5f77dce1ffb.jpg)



(b)   
Fig. 7. Effect of threshold on delay and utilization. (a) Latency for different thresholds. (b) Number of leaves for different thresholds.

multicast using multiple trees built with our new MEST algorithm. We used our algorithm to generate three multicast trees for each scenario. We examined the resource allocation (in terms of leaf nodes—lower means better) and the overall multicast delay, which is the largest delay among the three multicast trees. The results in Fig. 6(a) show that, for the same number of nodes, MESTs gave significantly lower multicast latency, as compared to a single-tree network. Similarly, Fig. 6(b) shows that MESTs had a few leaf nodes. This meant that more nodes were involved in the multicast functionality—i.e., better resource utilization.

# B. Threshold

We wanted to find the relation between threshold and the performance of a MEST. Fig. 7 shows the results for a set of simulations that tested the impact of increasing threshold values on the multicast delay and resource utilization. The performance curves tend to “flatten out” for higher threshold values. This is because a higher threshold allows more edges to overlap. Many of these edges will be high-weight edges. When an edge is used in multiple trees, it encounters congestion delays since it has to handle packets for multiple trees. In the worst case, when the threshold is set to infinity, all the MEST trees would correspond to the same tree. A close examination reveals that for this setup, the optimal threshold value is 75 m. At 75 m, the number of leaves in the multicast tree was lowest while the delay was near minimum. As part of future work, we are developing a heuristic model that could help determine the optimal threshold for a given setup.

# C. Multiple Trees

Our next simulation objective was to test for the effect of the number of multicast trees on the performance (delay versus utilization). We tested for two cases based on the fragment distribution on each tree.

1) Equal Size Fragments: In this round of simulations, we equally split the multicast content over two, three, four, and five trees, respectively. Fig. 8 shows the results. As the number of trees increased, the multicast latency showed significant improvement, and more nodes got involved in the multicast process. Thus, reducing the total number of leaf nodes (i.e., better resource utilization).   
2) Fragment Size Proportional to the Tree Weight: It is important to note that the gain in performance seen in Fig. 8 is not proportional to the number of trees over which the content is divided. This is because each tree has a different weight. For example, if we want to transfer 1000 kb of data, the content would be divided as 500 kb each on two trees or 250 kb each for four trees, and so on. Since each tree has a different total weight, it takes more or less time to complete the transfer. The total multicast delay is governed by the slowest tree (i.e., the largest weight tree). To overcome the problem of variable

![](images/25d37c77ad6969fb460e1a3ba122ac495a13d45ea77872f0c610ddad28db0150.jpg)



(a)

![](images/20dd4ef4ccf39cc4103029e2354424dd4ec36c9d663d31b33ba0191ddb1112d5.jpg)



(b)

Fig. 8. Effect of an increasing number of trees. (a) Lower multicast delay as the number of trees increases. (b) More trees leave behind less leaf nodes.   
![](images/8a67627ab9cbaa57ad343966af26c8c33184b4c1e424d16973ff6b179a74bb12.jpg)



Fig. 9. Splitting the content in proportion to the tree weight.

tree delays, we examined another set of simulations where the file was unevenly split. From our previous example, if the tree weights are in the ratio of 45 : 55, we would divide the file as 550 and 450 kb each. For four trees, if the weight ratios are 1 : 2 : 3 : 4, the file would be split as 400, 300, 200, and 100 kb. With such an inverse division, the tree with the highest weight (and, hence, the largest delay) gets the smallest fragment of the file. We carried out a series of simulations to verify this hypothesis. The results of these experiments are shown in Fig. 9. As expected, we saw an improvement in the performance for all the cases.

# D. Overlap Index

The overlap index is defined as the ratio of the sum of the overlapping edges in all the multicast trees to the sum of the edges in all the multicast trees, i.e.,

$$
\mathrm{OI} = \sum \mathrm{OE} / \sum E _ {i} \tag {2}
$$

where $\displaystyle \sum$ OE gives the number of overlapping edges in all the trees, and $E _ { i }$ is the number of edges in the ith multicast tree. This parameter is significant because it gives an idea about the amount of edge reuse in the network. Ideally, we would like to have this number as small as possible, indicating less edges that are being shared between trees.

Fig. 10(a) shows that the edge overlap increased with a higher number of trees. This means that there would be more edges that are being reused in multiple trees. This could potentially create congestion issues since the edge has to “serve” several trees. We also observed a slight increase in the overlapping as the threshold value increases. This is expected, as higher thresholds allow more edges to overlap. Furthermore, comparing Fig. 10(a) and (b), we see that that there is a slight increase in the overlap index as the number of member nodes increases. This should not come as a surprise because as the number of nodes increase, the total number of edges between them increases. There would be more edges that satisfy the threshold criteria and, thus, increase the overlap index.

# V. CONCLUSION AND FUTURE WORK

We have presented the MEST—a distributed algorithm for building multiple edge-sharing multicast trees. A MEST is not restricted to ad hoc, wireless, or overlay networks. It can be used to solve the resource utilization issue in any multicast network. MESTs easy to implement and work with any distributed algorithm that can generate an MST for a given network. MESTs can also be used to improve the reliability and robustness of the network. Multiple trees would form a mesh that consists of redundant links. If used for the sole purpose of constructing a reliable mesh, MESTs would hold an advantage in terms of keeping the overall delay low. This is something that other reliability algorithms fail to take into account.

Our simulation results show that a MEST can significantly reduce the multicast delay and, at the same time, improve network utilization. The results show that more trees give better resource utilization (less leaf nodes) with considerably lower multicast latency compared to a single-tree system. Simulations with fragment size showed that the delay was much lower if the content was split in proportion to the tree weight. We also defined an overlap index that gives an idea about the degree of edge sharing between various trees. The impact of threshold and number of nodes on this parameter was studied and analyzed.

We would also like to focus our attention on developing a heuristic or a model for finding the optimal threshold for a given scenario. We believe that it would be a hard problem since the threshold value depends on several factors, like the characteristic of the network (wired, wireless, overlay, etc.), which is represented by the edge weight (distance, bandwidth,

![](images/410d9355b31f14898bb50a7bb99a5dff9c5e4d4ae098f30caaded9c201ef6987.jpg)



![](images/07a6c9af7caff98d1596863c0b9bb1ef4ecc05125bea9741b9e18d9b48cac10b.jpg)



(b)   
Fig. 10. Overlap index for multiple trees. (a) Overlap index for 20 nodes. (b) Overlap index for 30 nodes.

RSSI, RTT, etc.), the number of desired MEST trees, the underlying MST algorithm, and the delay requirements of the network.

# REFERENCES

[1] R. C. Prim, “Shortest connection networks and some generalisations,” Bell Syst. Tech. J., vol. 36, pp. 1389–1401, Nov. 1957.   
[2] R. G. Gallager, P. A. Humblet, and P. M. Spira, “A distributed algorithm for minimum-weight spanning trees,” ACM Trans. Program. Lang. Syst., vol. 5, no. 1, pp. 66–77, Jan. 1983.   
[3] B. Awerbuch, “Optimal distributed algorithms for minimum weight spanning tree, counting, leader election, and related problems,” in Proc. 19th Annu. ACM Conf. Theory Comput., 1987, pp. 230–240.   
[4] G. Singh and A. J. Bernstein, “A highly asynchronous minimum spanning tree protocol,” Distrib. Comput., vol. 8, no. 3, pp. 151–161, Mar. 1995.   
[5] M. Faloutsos and M. Molle, “What features really make distributed minimum spanning tree algorithms efficient?” in Proc. ICPADS, 1996, p. 106.   
[6] D. K. Gifford, J. Jannotti, K. L. Johnson, M. F. Kaashoek, and J. W. O’Toole, “Overcast: Reliable multicasting with an overlay network,” in Proc. 4th Symp. OSDI, San Diego, CA, Oct. 2000, pp. 197–212.   
[7] P. Antoniadis and C. Courcoubis, “Market models for P2P content distribution,” in Proc. 1st Int. Workshop AP2PC, 2002, pp. 138–143.   
[8] S. Lee, R. Sherwood, and B. Bhattacharjee, “Cooperative peer groups in NICE,” in Proc. IEEE INFOCOM, San Francisco, CA, Apr. 2003, pp. 1272–1282.   
[9] M. Castro, P. Druschel, A.-M. Kermarrec, A. Nandi, A. Rowstron, and A. Singh, “SplitStream: High-bandwidth multicast in a cooperative environments,” in Proc. 19th ACM SOSP, Lake George, NY, Oct. 2003, pp. 298–313.   
[10] L. Xiao, A. Patil, Y. Liu, L. M. Ni, and A.-H. Esfahanian, “Prioritized overlay multicast in ad-hoc environments,” IEEE Comput. Mag., vol. 37, no. 2, pp. 67–74, Feb. 2004.   
[11] A. Young, J. Chen, Z. Ma, A. Krishnamurthy, L. Peterson, and R. Y. Wang, “Overlay mesh construction using interleaved spanning trees,” in Proc. INFOCOM, Hong Kong, Mar. 2004, pp. 396–407.   
[12] A. Patil, Y. Liu, L. Xiao, A.-H. Esfahanian, and L. M. Ni, “SOLONet: Sub-optimal location-aided overlay network for MANETs,” in Proc. IEEE Int. Conf. MASS, Fort Lauderdale, FL, Oct. 2004, pp. 324–333.   
[13] A. Patil, A.-H. Esfahanian, Y. Liu, and L. Xiao, “Resource allocation using multiple edge-sharing multicast trees,” in Proc. IEEE Int. Conf. MASS, Washington, DC, Nov. 2005, p. 371.

![](images/7184522a184155f06a59a8d42f9d42f7b2c3f9da67611249f3490212708b701d.jpg)



Abhishek Patil received the B.S. degree in electronics and telecommunications engineering from the University of Mumbai, Mumbai, India, in 1999 and the M.S. degree in electrical and computer engineering and the Ph.D. degree from Michigan State University, East Lansing, in 2002 and 2005, respectively.

He is currently a Wireless Research Engineer with Kiyon, Inc., San Diego, CA. His research interests include wireless technologies, mobile ad hoc networks (MANETs), location-aware computing, RFIDs, and pervasive computing.

![](images/00793da90fb6b72cdfa79b88a893df03016bfa918276df7778bb512ebbe5b8d6.jpg)



Abdol-Hossein Esfahanian received the B.S. degree in electrical engineering and the M.S. degree in computer, information, and control engineering from the University of Michigan, Flint, in 1975 and 1977, respectively, and the Ph.D. degree in computer science from Northwestern University, Evanston, IL, in 1983.

From September 1983 to May 1990, he was an Assistant Professor of computer science with Michigan State University, East Lansing, where he has been an Associate Professor since June 1990 and where

he was the Graduate Program Director from August 1994 to May 2004. He was an Associate Editor for Networks, An International Journal from 1996 to 1999. He has been conducting research in applied graph theory, computer communications, and fault-tolerant computing.

Dr. Esfahanian received the “The 1998 Withrow Exceptional Service Award” and “The 2005 Withrow Teaching Excellence Award.”

![](images/c039ec32350cd63d055465cc347ae7427eb128f8c1646cbfb56888728c4f2507.jpg)



Yunhao Liu (M’02–SM’06) received the B.S. degree from the Automation Department, Tsinghua University, Beijing, China, in 1995, the M.A. degree from Beijing Foreign Studies University in 1997, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, in 2003 and 2004, respectively.

He is currently an Assistant Professor with the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Kowloon, Hong Kong. His research interests include

peer-to-peer and grid computing, sensor networks, pervasive computing, network security, and high-speed networking.

Dr. Liu is a Senior Member of the IEEE Computer Society.

![](images/5c759ebb797e9c3bf5544f67c384aae1b856029e74286dfb9af6de2c252bd32e.jpg)



Li Xiao (M’00) received the B.S. and M.S. degrees in computer science from Northwestern Polytechnic University, Xi’an, China, and the Ph.D. degree in computer science from the College of William and Mary, Williamsburg, VA, in 2002.

She is an Assistant Professor of computer science and engineering with Michigan State University, East Lansing. Her research interests are distributed and Internet systems, overlay systems and applications, and wireless networks.

Dr. Xiao is a member of the Association for Computing Machinery, the IEEE Computer Society, and IEEE Women in Engineering.