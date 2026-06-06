# Robust Component-based Localization in Sparse Networks

Xiaoping Wang, Yunhao Liu, Senior Member, IEEE, Zheng Yang, Member, IEEE, Kai Lu, and Jun Luo

Abstract—Accurate localization is crucial for wireless ad-hoc and sensor networks. Among the localization schemes, component-based approaches specialize in localization performance. By grouping nodes into increasingly large rigid components, component-based localization algorithms can properly conquer network sparseness and anchor sparseness. However, such design is sensitive to measurement errors. Existing robust localization methods focus on eliminating the positioning error of a single node. Indeed, a single node has two dimensions of freedom in 2D space and only suffers from one type of transformation: translation. As a rigid 2D structure, a component suffers from three possible transformations: translation, rotation, and reflection. A high degree of freedom brings about complicated cases of error productions and difficulties on error controlling. This study is the first work addressing how to deal with ranging noises for component-based methods. By exploiting a set of robust patterns, we present an Error-TOlerant Component-based algorithm (ETOC) that not only inherits the high-performance characteristic of component-based methods, but also achieves robustness of the result. We evaluate ETOC through a real-world sensor network consisting of 120 TelosB motes as well as extensive large-scale simulations. Experiment results show that, comparing with the-state-of-the-art designs, ETOC can work properly in sparse networks and provide more accurate localization results.

Index Terms—Component-based localization; Location ambiguity; Robust localization; Structural error tolerance

# 1 INTRODUCTION

Location awareness is highly critical for wireless ad-hoc and sensor networks. Due to the constraints on hardware cost and energy consumption, however, it is unfeasible to equip all nodes with positioning hardware (e.g., GPS receivers). Instead, only a few nodes are configured with location information in the network setup phase, called anchors. Other nodes then locate themselves by the internode distance measurements. We call this procedure network localization. Note that the density of the network for localization is defined by the distance-measurement density. As the communication range is usually much larger than the distance-measurement range [1], a communication-dense network may be localization-sparse.

There is a theory of network localization [2] for analyzing the sufficient and necessary conditions to locate a sparse network, called RRT-3B condition. Using this conclusion, we can identify the maximum localizable part in a given network instance. Hence, RRT-3B indicates the upper bound of the number of nodes that can be successfully located from a given network. However, there is a gap between the upper bound and the performance of realistic localization algorithms.

To narrow the gap, there are increasing literatures on localization algorithms, falling into two categories: node-based design $[3, 4]$ and component-based design $[5]$ . Node-based localization algorithms try to locate the entire network by individually locating each non-anchor node, which is also called sequential localization. Research on this subject $[6]$ shows that the Sweeps algorithm $[3]$ is able to localize all the sequentially localizable networks. That is, Sweeps achieves the utmost performance of the node-based design. Nevertheless, there is still a performance gap between Sweeps and the theoretical limit $[2]$ . Overall, node-based design suffers the inherent limitation that it requires each located node to be self-localizable, which is not necessary for network localization.

To break the limitation of node-based design, component-based localization is proposed [5]. A component is defined as a set of nodes that forms a rigid structure. As components are rigid, they can be located as a whole. Hence, besides each single node, component is another basic unit for localization. Using components as intermediate results, nodes can collaborate with each other, thus to conquer network sparseness. Figure 1 demonstrates how to use the component concept for locating a network. Figure 1(a) shows the distance graph of a given network, where four non-anchor nodes $n_1 - n_4$ have three neighboring anchors $a_1 - a_3$ and the edges denote the distance measurements among them. Under the view of each single node, none of them can be localized, because each node can only find one neighboring anchor. In contrast to locating each single node, we can integrate the nodes into a component, as shown by the shaded area in Figure 1(b). The component can determine its physical embedding by the neighboring anchors, thus all nodes in the component are located simultaneously. To summarize, component-based designs can properly conquer network sparseness and anchor sparseness, thus to achieve higher performance than the node-based ones.

![](images/e72c75040b1bcd4f5744da6cde9b79d0bbcb74149569324ca1356bb930b620fa.jpg)



(a)

![](images/beec0535d0edd913554830837ac55bab379df6c1df79f13f6c459004757df2b9.jpg)



(b)   
Fig. 1. Basic concept of component-based localization. (a) The distance graph of a network; (b) Network localization by component concept.

Existing component-based algorithms $[5]$ , however, are based on the idealized model that assumes accurate distance measurements between neighboring nodes. Nevertheless, measurement errors are inevitable in practice. Based on the noisy measurements, the localization result may suffer structural deformation, which locates a component by an incorrect embedding in the physical coordinate system. Once a structural deformation is triggered, the error of the result is not determined by the measurement errors, but by the moved distances caused by the deformation. Hence, the structural deformation may lead to huge errors in the result set. To address such difficulties, researchers propose the concept of robust localization $[7]$ , which guarantees the uniqueness of the localization result under noisy distance measurements. Unfortunately, existing designs can only achieve robustness in node-based localization schemes $[4, 7]$ . As we know, a single node has two dimensions of freedom in 2D space (e.g., X-Y coordinates) and only suffers from one type of transformation: translation. In contrast, a component suffers from three possible transformations: translation, rotation, and reflection, and has three dimensions of freedom. A high level of freedom obviously brings about complicated cases of error producing and difficulties on error controlling. For component-based approaches, to the best of our knowledge, there is no related work on how to deal with measurement noises before this study.

To bridge the gap, we analyze how noisy ranging destroys the robustness of component realization. To quantify the impact of noises, an error tolerance for a component is defined as the upper bound of ranging errors under which the component can be localized uniquely (without deformation). By the concept of error tolerance, we present an Error-TOlerant Component-based algorithm (ETOC) that can achieve guaranteed robustness of the localization result. In addition, as a component-based design, ETOC inherits the property of high performance, where performance refers to the number of successfully localized nodes out of all non-anchor nodes. We evaluate ETOC through a real-world sensor network. The network consists of 120 TelosB motes distributed in an area of $126 \times 145\mathrm{m}^2$ . Experimental results show that ETOC can localize the network entirely in spite of the network sparseness. Extensive simulations also show that, comparing with the original component-based algorithm [5] and robust node-based algorithm [7], ETOC achieves high localization performance and better error control.

![](images/9f48b2993fbee355f623240d0b5892aa2727179c2871616ed11877c4ed3a4f00.jpg)



Fig. 2. The flowchart of component-based algorithms.

The rest of this paper is organized as follows. We present the preliminary knowledge in Section 2. In Section 3, we introduce the robust patterns for ETOC. Experimental studies are presented in Section 4. We introduce related work in section 5. Finally, we conclude the work in Section 6. This study is an extension of our previous work published in IEEE ICNP 2010 [8].

# 2 PRELIMINARY

In this section, we briefly introduce the basic idea of the component-based localization algorithm. Then, we analyze the key issue of achieving robustness in component-based scheme.

# 2.1 TERMINOLOGY

We do not assume any measurement model or node distribution in this paper. The input of the problem is the target node set and anchor node set, as well as a set of distance measurements. The aim is to locate as many non-anchor nodes as possible with robustness guarantee of the localization result.

We use a distance graph $G=(V,E)$ to represent a given network, in which each vertex in V denotes a node in the wireless network and each edge $(i,j)\in E$ denotes a distance measurement between node pair $(i,j)$ . Associated with each edge, we use a function $d(i,j):E\to R$ to denote the distance value, also abbreviated as $d_{ij}$ . We suppose a small portion of nodes, called anchors, know their locations in advance. Without loss of generality, m anchors are labeled from 1 to m, together with n-m ordinary nodes labeled from $m+1$ to n, where n denotes the total number of nodes in the network. The ground truth position of each node is denoted by $p_{i},1\leq i\leq n$ . We uniformly use node to represent a wireless device and use edge to represent the distance measurement of two nodes.

# 2.2 Overview of the Component-based Localization

A component is a set of nodes that form a globally rigid structure in the distance graph. As components are globally rigid, the relative position of each node in a component is fixed. That is, all nodes in a component can only be operated by global transformations. In node-based localization algorithms, the target is each zero-dimension node. In contrast, component-based algorithms directly locate the two-dimension components. By this means, nodes can cooperate with each other, as long as they belong to the same component. Hence, component-based localization algorithms can properly conquer network sparseness and anchor sparseness, as demonstrated by the example shown in Figure 1.

![](images/92af310f4668662b8a3c0d514007cf3e9952da2ca01199478d833c5676eee9c1.jpg)



(a)

![](images/b51726a0e0cec896e20d911e54079adc0576f5c42c27ef1a00a50ac196ce8055.jpg)  
(b)

![](images/777270686934f597fa8974acc2629eb6fd572cf74b64e0a28314ea1c0040da7e.jpg)



(c)

![](images/771f37b2345fdf17afbe486c3a9ca3585b199b784b2f3f62f6cbe2f1e02e437c.jpg)



(d)   
Fig. 3. Realization patterns of components. (a) Three (or more) internal anchors; (b) Two internal anchors; (c) One internal anchor; (d) No internal anchor.

![](images/f793390389945d5c0d59a9b5bdccdd28ece93e9b85307b4a8a067aaa6bda52e3.jpg)



Fig. 4. The ambiguity issue of component-based localization.

In implementation view, as the relative positions of the nodes in a component are fixed, we adopt a local coordinate system to indicate this relationship. The aim of component-based localization is to locate the component in the physical coordinate system defined by all anchors. Hence, the key issue of component-based localization is how to convert the local coordinate system into the physical coordinate system by the anchors and the intercomponent distance measurements. A component-based localization algorithm contains three main procedures: component generation, component mergence, and component realization. We show the flowchart of the localization process in Figure 2. The details of each step are as follows:

1. Component generation partitions the network into a set of components. A component is initialized by a triangle in the network for initializing a local coordinate system. Then, other nodes join the newly generated component by locating itself into this local coordinate system. This process is the same as traditional trilateration.   
2. Component mergence stitches two components to generate a larger component. We merge components by converting the local coordinate system of one component to that of the other one, thus the local coordinates can present the relative positions of all merged nodes. Merging components can integrate the anchor information of the merged components. Hence, this process may convert two non-realizable components into one realizable component.   
3. Component realization localizes a component as a whole, which converts the local coordinate system of a component to the physical coordinate system. After the coordinate system conversion, all nodes are located simultaneously. As components are all globally rigid, components are realized by rigid transformations: translation, rotation, and reflection.

As component mergence and component realization are both based on converting the local coordinate system, the key issue of component-based localization is the coordinate system conversion. Traditional local map stitching $[7, 9]$ converts the coordinate system by three or more common nodes. In contrast, component stitching converts the local coordinate system by both the common nodes and the inter-coordinate-system measurements. Clearly, stitching local maps is a special case of stitching components. We take component realization as an example, where the target coordinate system is the physical coordinate system defined by the anchors. We first differentiate the role of anchors. If an anchor belongs to the target component, we say the anchor is an internal anchor; otherwise, it is an external anchor. By enumerating the number of internal anchors, we conclude the complete patterns for component realization. All patterns are illustrated in Figure 3, where the shaded area denotes a component, the solid squares denote anchors, the soft circles denote non-anchor nodes, and edges denote distance measurements between nodes. If there is an edge connecting an in-component node and an external anchor, we say the component has an edge linked to an anchor. Then, we list all the patterns as follows:

(a) the target component has three or more internal anchors;   
(b) the target component has two internal anchors and at least one edge linked to an anchor;   
(c) the target component has one internal anchor and at least two edges linked to two distinct anchors;   
(d) the target component has four edges linked to at least three distinct anchors, where the number nodes associated with these edges is at least three in the component.

Once a component matches one of the patterns, we can convert the local coordinate system by solving simultaneous polynomial equations [5].

# 2.3 Ambiguity Issue in Component-based Localization

When the distance measurements are noisy, the two coordinate systems may not be precisely aligned. Such misalignment may produce ambiguities in localization result. Clearly, if we locate the component to the ground truth location in the physical coordinate system, the embedding will accept the measurement errors, where the embedded distance falls in an acceptable range of the measured distance. However, there may also exist alternative embeddings that match the embedded distances with the measured distances.

For the example shown in Figure 1, if the measured distance between $a_{2}$ and $n_{4}$ is a bit shorter than the accurate value, the embedding of the component will be “rotated” to the place shown in Figure 4. We also plot the ground truth embedding of the component by the dashed lines and circles in this figure. If we evaluate the embedding by the discrepancy between the embedded distance and the measured distance, the rotated embedding matches the measured distance better, thus to become the final result. Comparing the two embeddings, we observe huge errors for all located nodes. In a word, if there exist multiple embeddings for a component that accept all of the noisy distance measurements, we say the localization result of the component is ambiguous. Hence, we define a localization algorithm is robust, if it can properly avoid the ambiguities.

![](images/44ba9242a714b7ceed6d085bbb462c5d9bb92671ccd6ffb44c22ce3c7ce34c2a.jpg)



Fig. 5. Global flip.

![](images/b4a1e710e080cefb7c9149cfd371a2b453602dcb7952563d82421d67ec22482c.jpg)



Fig. 6. Illustration of Case 2.

![](images/219199b068a9713ccaf8a9b62f928723f46cbe43489d6caf217ecc3a2744106a.jpg)



Fig. 7. Illustration of Case 3.

![](images/46a1d8e7986e59bbee43510b0538eae458ede0e5c372902a4e58cfe4e6cd9da9.jpg)



(a)

![](images/3a8afee9d6f25239f6687b77c74a0d9244ebb4a1aad00a6c8c41bb275dea357b.jpg)



(b)   
Fig. 8. Illustration of Case 4. (a) Robust evaluation by error tolerance; (b) The symmetric case.

# 3 ROBUST COORDINATE SYSTEM CONVERSION PATTERNS

In this section, we investigate robust patterns for the coordinate system conversion without ambiguities. We also use component realization to show the robust coordinate system conversion patterns, for the sake of better differentiating the source and target coordinate system. Clearly, these robust patterns can be directly used for component mergence. As shown in Figure 3, there are only four patterns to do the conversion, so that we discuss each pattern in each of the following sub-sections. In addition, we assume that the in-component positions of the nodes are computed by robust node-based algorithms $[4, 7]$ without ambiguities.

# 3.1 Robust Realization with Three or More Internal Anchors

As three nodes are enough to determine a coordinate system, the conversion can accomplished by purely using the alignment of the internal anchors. To uniformly number the patterns, we rewrite this pattern as follow. Case 1: the component contains three or more internal anchors.

The in-component coordinates of the anchors may contain errors because of the noisy distance measurements. Hence, it is unlikely that the anchors will precisely align in both of the coordinate systems. For this issue, there is a closed-form and least-square optimal method, called coordinate system registration $[10]$ .

Nevertheless, this conversion only considers the alignment of the anchors. When the anchors are approximately collinear, the conversion may flip the non-anchor nodes to incorrect positions. As shown in Figure 5, if the result is flipped, node $n_1$ will be localized to the position $n_1'$ , which is far from its ground truth position. To avoid this problem, ETOC requires that the width of the anchors must be large enough according to the measurement errors. Here, the width of anchors is defined as the minimal distance of two parallel lines that contain all the anchors. When the requirement is not satisfied, ETOC will try to realize the component through other patterns.

# 3.2 Robust Realization with Two Internal Anchors

Two internal anchors are not enough to determine a coordinate system, because the coordinate system may flip against the axis of the two anchors. Hence, we need at least one additional constraint to make this problem solvable, described as follow. Case 2: the component contains two anchors and at least one edge linked to an external anchor.

As shown in Figure 6, for each node linked to an external anchor, it can obtain at least three distance estimates with anchors: one is the direct distance measurement with the external anchor and the other two are the in-component distances to the internal anchors. Then, the physical location of the node can be computed by trilateration. Then, we obtain at least three nodes that know their physical locations, so that we can convert the coordinate system by following Case 1.

# 3.3 Robust Realization with One Internal Anchor

When a component contains only one anchor, we cannot directly adopt the coordinate system registration. In this section, we present a novel robust mechanism to address this problem.

The internal anchor can only prevent translation of the component. To make the coordinate system conversion problem solvable, two edges (distance measurements) are required to eliminate possible rotation and reflection, described as follow. Case 3: the component contains one anchor and two distinct non-anchor nodes connecting with two distinct anchors.

As illustrated in Figure 7, the shaded area denotes a component C, and it contains an anchor $a_{1}$ and two nodes $n_{1}, n_{2}$ sharing two edges with two external anchors $a_{2}, a_{3}$ . Let $\alpha, \theta$ , and $\varphi$ denote the angle values of $\angle a_{2}a_{1}a_{3}, \angle n_{1}a_{1}a_{2}$ , and $\angle n_{2}a_{1}a_{3}$ , respectively. Since all the distances are known, we can compute the values of these angles from $\Delta a_{2}a_{1}a_{3}, \Delta n_{1}a_{1}a_{2}$ , and $\Delta n_{2}a_{1}a_{3}$ , respectively. Define $S=\{\alpha+\theta+\varphi, \alpha+\theta-\varphi, \alpha-\theta+\varphi, \alpha-\theta-\varphi\}$ . Let $\delta$ denote $\min\{|\cos\beta_{1}-\cos\beta_{2}|\}$ for all $\beta_{1}, \beta_{2}\in S$ and $l_{1}, l_{2}$ denote the in-component distances of node pair $(a_{1},n_{1}), (a_{1},n_{2})$ , respectively. Then, the upper bound of ranging errors under which the component can be realized uniquely (defined as the error tolerance of the component) can be expressed as:

$$
T _ {c} = \frac {1}{2} \frac {l _ {1} l _ {2}}{l _ {1} + l _ {2}} \delta . \tag {1}
$$

We leave the proof of this proposition, as well as the bound of the error tolerance estimate, in the appendix.

By recent studies [11], the localization error is approximately linear with the measurement error in robust localization. The maximum error of the in-component distances is at most twice of the localization error, only if the actual localization errors are collinear and with different directions. Hence, there is a linear relationship between the measurement error and the computed distance inside a component. By comparing error tolerance $T_{C}$ with the error, the worst-case probability of ambiguities is bounded. If the error is lower than $T_{C}$ , ETOC can realize this component robustly.

ETOC converts the coordinate system by the following two steps. First, ETOC computes the physical locations of node $n_{1}$ and node $n_{2}$ . As shown in Figure 7, by the distance constraints, node $n_{1}$ may flip against axis $a_{1}a_{2}$ , thus to have two candidate locations denoted by $n_{1}$ and $n_{1}'$ in the figure. Similarly, node $n_{2}$ may flip against axis $a_{1}a_{3}$ , thus to have two candidate locations denoted by $n_{2}$ and $n_{2}'$ . Hence, the number of candidate distances between nodes $n_{1}$ and $n_{2}$ is four, i.e. the distances between the location pairs $(n_{1}, n_{2})$ , $(n_{1}, n_{2}')$ , $(n_{1}', n_{2})$ , and $(n_{1}', n_{2}')$ . Then, ETOC selects the candidate distance with minimum difference from the in-component distance between nodes $n_{1}$ and $n_{2}$ . Note that each candidate distance uniquely determines a location pair of nodes $n_{1}$ and $n_{2}$ . As a result, nodes $n_{1}$ and $n_{2}$ are located simultaneously. Together with anchor $a_{1}$ , we obtain three nodes that know their physical coordinates. Then, following Case 1, ETOC converts the coordinate system.

# 3.4 Robust Realization with No Internal Anchor

When the distance measurements are accurate, four interconnected edges are able to form a system of overdetermined simultaneous equations for converting a coordinate system $[5]$ . However, such mechanism is sensitive to the measurement errors. To avoid the ambiguities, we solve this case by five interconnected edges, which is fairly close to the optimal result. Case 4: there are five edges connecting the component with anchors forming one of the structures shown in Figure 8.

As shown in Figure 8(a), there are three distinct nodes $n_1, n_2, n_3$ in the component, where node $n_1$ and node $n_2$ share two edges with two external anchors respectively, and node $n_3$ shares an edge with another external anchor. We label the anchors by $a_1, a_2, a_3, a_4$ , and $a_5$ . Though we use different notations for these anchors, we only demand that they map to at least three distinct anchors. We draw two lines through $a_1, a_2$ , and $a_3, a_4$ , and they intersect at the point $a'$ . Then, the physical location of point $a'$ is known. As shown in Figure 8(a), the angle value of $\alpha$ can be computed from $\Delta a'a_1a_4$ . Further, as $\Delta n_1a_1a_2$ and length $a'a_2$ are known, we can compute angle value $\theta$ and distance $l_1$ from $\Delta a'n_1a_1$ . Similarly, we can compute the angle value $\varphi$ and distance $l_2$ from $\Delta a'n_2a_4$ . As we already obtain the angle values of $\alpha, \theta$ , and $\varphi$ as well as the distances of $l_1$ and $l_{2}$ , we can evaluate the robustness of this structure by error tolerance. If it is robust, we get the physical positions of node $n_{1}$ and node $n_{2}$ by Case 3. Taking nodes $n_{1}$ and $n_{2}$ as two anchors, we can convert the coordinate system by the case with two internal anchors, i.e. Case 2. According to case 2, an additional edge $(n_{3}, a_{5})$ is required. Finally, after computing the location of node $n_{3}$ , the whole component is located.

As coordinate system conversion is symmetric, this method can also work when we exchange anchors and the internal nodes, as shown in Figure 8(b). In addition, there is a special case that the two lines $a_1a_2$ and $a_3a_4$ are parallel (i.e. the point $a'$ does not exist). Then, we can testify that the error tolerance of this structure is zero. Hence, this special case is non-robust.

Compared with the complete pattern set shown in Figure 3, ETOC completely solves three out of four patterns. Specifically, cases 1-3 of ETOC solve patterns (a)-(c), respectively. Case 4 in ETOC partially solves pattern (d). Case 4 requires five edges, while the optimal result of pattern (d) requires four edges. In a word, ETOC can provide robustness for most components in a target network.

We conduct an experiment to examine how much the incompleteness of ETOC decreases the localization performance. The test scenario is a square normalized region $[0,1]^{2}$ with randomly distributed 20 anchor nodes and 180 non-anchor nodes. As we only test the localization patterns in this experiment, all the inter-node measurements are given as accurate values. We adopt distance measurement range to control the density of the network and test the distribution of patterns under diversified densities. We run the original component-based algorithm, BCALL [5], for comparison. Figure 9 shows the average of 50 test results, where the left and the right bars show the distributions of patterns for ETOC and BCALL under a certain average degree configuration, respectively. We use different colors to show the amount of nodes located by following each case, and the part marked by “nodes” shows the amount of nodes located as individual nodes. When the average degree is beyond 9, the whole network becomes globally rigid and a huge component can cover most nodes in it, so that this component is directly located by Case 1. Other cases play important roles when the average degree varies from 5 to 9. Compared with BCALL, ETOC decreases the proportion of Case 4 from 1.7% to 1.0%, and the decrease is acceptable for the overall performance.

# 3.5 Refinement of the Conversion Result

The pattern-based conversion result only utilizes the pattern-involved measurements to generate the coordinate conversion result. To further diminish errors, we refine the conversion result by all available measurements. Note that the refinement is optional, especially when the computational resource is limited.

The refinement procedure takes the pattern-based conversion result $(R_{0}, t_{0})$ as input, where $R_{0}$ is the rotation matrix with possible reflection, $t_{0}$ is the translation vector. By this input, node i at position $p_{s,i}$ in the source coordinate system is converted to the position, $P_{i}=R_{0}\times p_{s,i}+t_{0}$ , in the target coordinate system. Then, $P_{i}$ is the unrefined position of node i. Since the pattern-based conversion is sub-optimal, we only consider two rigid transformations to refine the result: translation t and rotation R, where t is a two-dimensional vector and R is a rotation matrix defined as:

![](images/b41cd30fe00cbbb4ec1aaf8b5db2487511ad157fc1c3b6d0f0ec4129b81c9c72.jpg)



Fig. 9. The test result of pattern distribution.

![](images/1fabf0a8d40fb02d4f865fc6c92f48effa6a06f82a86aa7958e497a598be7755.jpg)



Fig. 10. The deployment of the sensors.

![](images/b8796a26913ac4a37282c33525481e1a14bcdd6334d74235a91d6bed1115da38.jpg)



Fig. 11. Distance graph of the network.

![](images/1f646b757cdd2202acdd800c283c53f61c67b5505655a0b7e918b8284cbdf962.jpg)



Fig. 12. The average error for each component.

$$
R (\theta) = \left[ \begin{array}{c c} \cos \theta & - \sin \theta \\ \sin \theta & \cos \theta \end{array} \right]. \tag {2}
$$

Then, the goal of refinement is to find proper $(t, \theta)$ , such that the refined position $P_{i}^{\prime}=R(\theta)\times P_{i}+t$ for each node minimizes the residual error, defined as follow.

We also use component realization to describe the refinement. Let $A_{c}$ denote the set of internal anchors and $E_{c}$ denote the set of edges connecting the component with external anchors. For each edge $(i,j)\in E_{c}$ , we assume that node i denotes the node in the component and node j denotes the external anchor. Then, the error function is the combination of the squared positioning errors of the internal anchors and the squared distance errors of the interconnected edges. Hence, the goal of the refinement step is to find a proper tuple $(t,\theta)$ to minimize:

$$
\begin{array}{l} (t, \theta) = \\ \operatorname{argmin} _ {t, \theta} \left[ \eta \sum_ {i \in A _ {c}} (P _ {i} ^ {\prime} - p _ {i}) ^ {2} + (1 - \eta) \sum_ {(i, j) \in E _ {c}} \left(\left\| P _ {i} ^ {\prime} - p _ {j} \right\| _ {2} - \right. \right. \\ \left. \left. d _ {i j}\right) ^ {2} \right], \tag {3} \\ \end{array}
$$

where $P_{i}^{\prime}=R(\theta)\times P_{i}+t$ denotes the refined position of node i, $P_{i}$ denotes the unrefined position of node i, $p_{i}$ denotes the physical position of anchor i, $d_{ij}$ denotes the measured distance between node pair $(i,j)$ , and $\eta$ denotes the weight of each part. Specifically, we equally treat the two parts of estimate error, and set $\eta=0.5$ . Since the unrefined positions $P_{i}$ provides a sub-optimal initial value, the optimal solution will be directly obtained by a descent method. However, as the cost function is transcendental, derivative-based method will lead to high computational cost. Hence, we adopt Powell's conjugate gradient descent method [12] for this optimization problem.

# 4 EXPERIMENTS

We evaluate ETOC by both a real-world system and extensive simulations.

# 4.1 Experiment Setup

To validate the robustness and the performance, we evaluate ETOC by the data from a real-world sensor network (the GreenOrbs project [13, 14]). The network consists of 120 TelosB nodes that are deployed in an area of 126×145m². Figure 10 shows the node distribution, where circles denote the positions of the node. Data are collected in the deployed region and collected by a PC in the monitoring center. Between the deployed region and the monitoring center, six relay nodes are deployed for multi-hop routing. Based on the Time of Arrival (ToA) of acoustic signals, the inter-node distances are measured with maximum error of 0.3m. The average degree of the distance graph is 7.2. That is, the network is sparse for localization, considering the fact that trilateration requires the average degree to be beyond 10 for entirely locating a network [7]. Anchor nodes are manually configured on the boundary of the deployed region. We use this network to show the performance of ETOC. Further, we compared the localization result with that of BCALL to show the result accuracy of ETOC.

Besides the real-world system test, we also conduct extensive simulations to evaluate ETOC under a wide range of parameters. The scenario is a square normalized region $[0,1]^{2}$ with randomly distributed 200 nodes. We adopt distance measurement range r to control the density of the network. The distance information between neighboring nodes is corrupted by zero mean additive Gaussian noise [4], $N(0, \sigma^{2})$ . We take three deviations, i.e. $3\sigma$ , as the maximum error, so that the threshold for determining robustness is also $3\sigma$ . For each set of simulations, we take multiple runs and report the average.

We use three metrics in our simulations: performance, accuracy, and cost. The proportion of robustly located nodes out of all non-anchor nodes shows the performance of each algorithm. The standardized position estimate error (SPEE) indicates the localization accuracy of each algorithm, defined as the ratio of the mean position estimate error to the measurement range:

$$
S P E E = \frac {1}{n r} \sum_ {i = 1} ^ {n} \| p _ {i} - \hat {p} _ {i} \| _ {2} \times 100 \%, \tag{4}
$$

where n is the total number of located nodes, r is the range of distance measurement, and $p_{i}, \hat{p}_{i}$ are the ground truth and estimated positions of node i, respectively. We evaluate the cost by the mean number of trilaterations (a.k.a. multilaterations) needed for locating a node. When no nodes are localized from a network instance, i.e. n=0, we define the SPEE and cost to be not-a-number and do not count these data in the final result. Moreover, we conduct the experiments by controlling three parameters: the standard deviation of the ranging errors, the mean degree of the network, and the proportion of anchors.

We compare ETOC with three typical algorithms. BCALL [5] is the basic version of component-based localization algorithm without any robustness guarantee. As BCALL is originally designed for accurate distance measurements, we need to extend BCALL for measurement errors. We first finitely localize the components by its localization solver, i.e. solving simultaneous polynomial equations. Then, we select the candidate result with minimum stress, which is defined as the squared discrepancy between the localized inter-node distances and the measured distances. Robust quadrilaterals (RQ) [7] is a node-based design for guaranteed robustness, i.e. structural uniqueness of the localization result. The basic localization unit of RQ is four-node local maps. RQ sets a bound on the geometric element to avoid flip ambiguity, which is the only structural deformation of such local maps. We implement full RQ algorithm with cluster optimization to mitigate error accumulation. RRT-3B [2] is the theoretic result for the condition of network localization. RRT-3B does not really compute the location of each node, but shows which part of the network can be localized in the given distance measurements. Hence RRT-3B defines the upper bound of the node number that can be located from a given network instance.

# 4.2 Real-World System Test

We compare ETOC with BCALL in this test. As they are both component based algorithms, they follow the same execution procedure. Figure 11 shows the ground truth location of each node. Also, we use different colors to show the result of component generation, in which the solid squares denote anchors and the soft circles denote non-anchor nodes. The details of each step are as follows:

1. After component generation step, this network is partitioned into five components and eight isolated nodes, as shown in Figure 11.   
2. Then, we use the patterns of ETOC and BCALL to realize the components. First, component 1 can be localized through Case 1 (Pattern (a)), and component 2 can be localized through Case 2 (Pattern (b)).   
3. After component 1 is localized, component 3 can be localized through Case 3 (Pattern (c)).   
4. Next, component 4 is localized through Case 3 (Pattern (c)).   
5. Finally, all isolated nodes can be localized by trilateration.

We show the average error of each component and the isolated nodes (the last column) in Figure 12. The error is standardized to be the percentage of the maximum distance measurement range. From this figure, we conclude that ETOC achieves lower localization error than BCALL. Further, the error for each component is quite stable, while BCALL will lead to error accumulation. Clearly, ETOC performs better in error control.

# 4.3 The Impact of Measurement Errors

In this section, we evaluate the performance, accuracy and cost of ETOC, when the standard deviation of the errors varies. We fix the anchor proportion to 10% and set the average degree to be 15. The maximum proportion of measurement error varies from 0% to 15% with step length 1%. We report the mean result of 50 network instances in Figure 13.

Figure 13(a) plots the proportion of successfully located nodes against the error magnitude. The performance of ETOC decreases slightly with the increase of error magnitude, because the increased errors may make some components fail to pass the robustness test. In contrast, the performance of RQ decreases sharply with the increase of error magnitude. RQ relies on generating uniformly overlapped local maps to produce a global map. With the increase of ranging errors, the robustness test of RQ will drop more local maps, so that the performance decreases sharply when RQ fails to generate adequate overlapped local maps. In contrast, BCALL and RRT-3B are not sensitive to the measurement errors. BCALL always locates the components, as long as it follows the localization patterns. RRT-3B just tests the connectivity and the geometric property. The performances of these algorithms are quite stable over the tested range.

Figure 13(b) plots the SPEE against error magnitude. For ETOC and RQ, as they are both robust localization algorithms, the SPEEs are approximately linear with the ranging errors. In contrast, the SPEE of BCALL becomes considerably high, when the maximum error exceeds 10%. As BCALL does not have any error control mechanism, BCALL suffers severe error accumulation.

Figure 13(c) shows the number of trilaterations needed to locate a node for each algorithm. The costs of ETOC and BCALL are approximately optimal over the tested range, as they both locate most nodes in the network instances. In contrast, the cost of RQ first increases slightly for less than 10% errors. Then, the cost increases sharply when the error further enlarges. All of the algorithms need to generate all components or local maps in the generation step, no matter whether they are finally localized or not. As a result, the total cost is approximately a constant for each algorithm. Consequently, the average cost is inversely proportional to the number of successfully localized nodes.

# 4.4 The Impact of Network Density

In this section, we evaluate the performance, accuracy and cost of ETOC, when the network density varies. We fix the anchor proportion to 10% and set the errors to be at most 10% of distance measurement values. We adopt an empirical formula to control the average degree of the network instances linearly. The average degree of each network instance varies from 5 to 30 with step length about 0.05. We report the mean result in the bunch of 50 network instances in Figure 14.

Figure 14(a) plots the proportion of successfully located nodes against average degree. BCALL can locate most the network instances when the average degree achieves 10. ETOC can locate the entire network when the average degree is beyond 12. Being a component-based algorithm, ETOC inherits the characteristic of high performance. Component-based localization can integrate information on the granularity of components, thus can work well with low network density as well as low anchor density. The performance gap between BCALL and ETOC is mainly caused by the robustness test. In contrast, RQ demands the average degree to be over 25 for entirely localizing a network. Indeed, to guarantee robustness, RQ drops a large proportion of local maps in the local-map generation step, so that RQ needs high network density to compensate this.

![](images/c4cf3385e4eee5c6c722ff80df09186152f5813f450ab41bdb3e3901c8313b68.jpg)



(a)

![](images/fc8a3f95b37f535c135f432ab778ee8b2c22922fa3eb64bfdd16408c1fb6b459.jpg)



(b)

![](images/e0135be8870166cff605510928c6562408655f10935dbb444b74113b243ea0af.jpg)



(c)   
Fig. 13. The impact of error magnitude. (a) The percentage of successfully located non-anchor nodes; (b) The error of the localization result; (c) The average cost for locating a node.

![](images/31456e54b08fca8e28be68bd26f3fa29b7eef8163c267f82cb242a38bd333bd3.jpg)



(a)

![](images/983b4131122a65ce7931c0f300160d728e499758ea6e2a098228f43616b6a891.jpg)



(b)

![](images/e2da54533efd941c66c18211751500fa5ee07d3d54a715d569a81a7f38f5c51e.jpg)



(c)   
Fig. 14. The impact of average degree. (a) The percentage of successfully located non-anchor nodes; (b) The error of the localization result; (c) The average cost for locating a node.

![](images/78fb579be6762d518e839379cfbe72540bf6110439da036e0c78d93282e1d536.jpg)



(a)

![](images/288a7e76ab2542b318628565760e45db00a9da57e504a18779c66f4af257d969.jpg)



(b)

![](images/7d0ade64c5863b87ffdc0e854eef0018887073b52d5a7cbb2d03929ccf12798e.jpg)



(c)   
Fig. 15. The impact of anchor proportion. (a) The percentage of successfully located non-anchor nodes; (b) The error of the localization result; (c) The average cost for locating a node.

Figure 14(b) plots the SPEE against average degree. The SPEE of ETOC decreases when the average degree increases. In contrast, the SPEE of RQ keeps in the same level over all the tested range. RQ can hardly benefit from the increase of average degree, because RQ can only use three distance measurements at a time when generating a local map. In contrary, ETOC can utilize all measurements with neighboring nodes. Using more measurements can clearly diminish the error of the result, especially when the average degree is high. For BCALL, the change of SPEE is a bit complicated. The SPEE first increases, because the network is split into several small-scale components in this stage and the error accumulation is huge in this scenario. Then, the SPEE starts to decrease with the increase of network density. In this stage, the entire network forms one globally rigid component, so that more measurements can help to counteract the measurement errors. When the average degree is beyond 20, BCALL and ETOC have similar result precisions.

Figure 14(c) plots the mean number of trilaterations needed for locating a node by each algorithm. As we have discussed, the mean cost is inversely proportional to the total number of successfully localized nodes. The results match the localization performance well, as shown in Figure 14(a).

# 4.5 The Impact of Anchor Proportion

In this section, we evaluate the performance, accuracy and cost of ETOC, when the anchor density varies. We fix the average degree about 10 and set the errors to be at most $10\%$ of distance measurement values. The proportion of anchors varies from $5\%$ to $50\%$ with step length $5\%$ . We report the mean result of 50 network instances for each configuration in Figure 15.

Figure 15(a) plots the proportion of successfully localized nodes against anchor density. BCALL performs quite close to the theoretical limit. Component-based localization has the inherent advantage on integrating the anchor information, thus it can work well under very low anchor density. For ETOC, the only difference between ETOC and BCALL is that ETOC adopts robust patterns for localization. This difference, however, may be amplified by some boundary cases. As component-based localization is an iterative process, both ETOC and BCALL locate target networks by sequentially locate each component. Hence, once a component is rejected by the robust patterns of BCALL, it may further disturb other components to be located. This phenomenon gets worse when there are fewer anchors, because fewer anchors lead to less tolerance for component rejections. In contrast, the performance of RQ is linearly related to the anchor density. RQ requires generating uniformly overlapped local maps to form a global map. The network is partitioned into several medium-sized global maps. As a result, the probability of localizing these global maps is approximately linear with anchor density.

Figure 15(b) shows the SPEE against anchor density. The SPEEs of ETOC and RQ do not change much with the increase of anchor density. This phenomenon is due to the indirect use of anchors. More anchors cannot diminish the error of component or local map generation, so that it cannot provide evident improvement on overall accuracy. The SPEE of BCALL decreases with the anchor density. The increased anchor density helps to restrain error accumulation.

Figure 15(c) shows the number of trilaterations needed to localize a node for each algorithm. The costs are also inversely proportional to the number of successfully localized nodes.

# 5 RELATED WORK

Localization in wireless networks has been attracted significant research interest. Many researchers model the localization problem as a weighted graph realization problem and employ rigidity theory to analyze the corresponding problems $[2, 3, 15-19]$ . This model is also widely used for theoretical research $[20]$ and algorithm design $[3]$ . These works provide valuable insight in localization problem, such as a formal localization theory $[2]$ . Nevertheless, using rigidity theory assumes that the distance measurements between neighboring nodes are accurate, which is over-idealized for current ranging techniques $[1]$ .

To handle the noisy ranging measurement, many researchers propose to minimize the impact of ranging errors in node-based localization. Moore et al. first propose the concept of robust localization and introduce Robust Quadrilaterals to achieve this [7]. They point out that flip ambiguity is the only structural deformation for locating a single node, so that the result is proved to be robust. However, the experimental results show that this design suffers low performance, working properly only in dense networks. In contrast, ETOC inherits the high localization performance from component based localization.

Liu et al. [4] and Yang et al. [21] propose to enhance traditional trilateration with error management. They track the error in each step to minimize the expected error of the final localization result. Their methods perform well on diminishing the overall localization error of the result. However, they cannot provide any robustness guarantee. As structural deformation is topology-sensitive, it can be triggered by any tiny errors in special case. For example, approximately collinear anchors can always yield flip ambiguity in trilateration. Hence, purely tracking errors cannot completely avoid ambiguity issues.

Many works propose to localize a network by building local maps, and some of them $[22, 23]$ also address the robustness of stitching the local maps. The local map defined in these works is a special case of our component, i.e. Case 1 in this paper. As component is a more general concept, achieving robustness of component-based localization achieves higher localization performance and clearly brings about a harder problem. Besides, ETOC also give the quantitative analysis of robustly merging rigid structures, which is, to the best of our knowledge, the first work to do so.

In addition, there are many works focusing on localization in sparse networks. Sweeps algorithm $[3]$ relaxes triditional trilateration to bilateration to conquer network sparseness. However, this work requires accurate distance measurements. Besides, the connectivity information is often adopted to conquer network sparseness $[24, 25]$ . Jin et al. utilize circle packing technique to rebuild node locations from the connectivity information $[25]$ . Liu et al. partition the network into convex tiles, and adopt MDS to locate each tile $[24]$ . Jamali-Rad et al. investigate the problem of grid-based fingerprinting localization by access points (APs), and use of compressive sampling to recover the location of the target $[26]$ . They reformulate the problem by exchanging the signal readings among the APs to conquire the AP sparseness problem. Cheng et al. focus on the sparse localization problem in an underwater 3D scenario $[27]$ . They transform the 3D underwater positioning problem into its 2D counterpart via node projection, and adopt 2D localization technique to solve this problem. Compared with these works, ETOC guarantees the robustness of the localization result, thus to obtain more accurate positioning results.

# 6 CONCLUSIONS AND FUTURE WORK

We propose the concept of error tolerance for component based approaches. By exploiting a set of patterns, we design a robust localization algorithm, ETOC, which is the first work to address ranging noises for component based localization. Compared with existing works, ETOC obtains high localization performance and better error control. We evaluate ETOC through a real-world system and extensive simulations. The experimental results show that ETOC works properly in sparse networks and achieves more accurate results.

The future work is to further investigate the optimal robust pattern without any in-component anchors. Also, we will explore the quantitative relationship between the measurement errors and the positioning errors for more critical demands.

# ACKNOWLEDGMENT

This work is supported in part by NCET, NSFC/RGC Joint Research Scheme N\_HKUST602/08, National Basic Research Program of China (973 Program) under Grants No. 2011CB302705, the National High-tech R&D Program of China (863 Program) under Grants No. 2012AA01A301, 2012AA010901, and 2010CB328004, and NSF China 61170261, 61272142, 61272483, 61171067, 61133016, 61272056, and 61272482.

# REFERENCES

[1] C. Peng, G. Shen, Y. Zhang, Y. Li, and K. Tan, "BeepBeep: A high accuracy acoustic ranging system using COTS mobile devices," in ACM SenSys, Sydney, Australia, 2007, pp. 1 - 14.   
[2] J. Aspnes, T. Eren, D. K. Goldenberg, A. S. Morse, W. Whiteley, Yang Richard Yang, B. D. O. Anderson, and P. N. Belhumeur, "A Theory of Network Localization," IEEE Transactions on Mobile Computing, vol. 5(12), pp. 1-15, 2006.   
[3] D. Goldenberg, P. Bihler, M. Cao, J. Fang, B. Anderson, A. S. Morse, and Y. R. Yang, "Localization in sparse networks using Sweeps," in ACM MobiCom, Los Angeles, CA, 2006, pp. 110-121.   
[4] J. Liu, Y. Zhang, and F. Zhao, "Robust Distributed Node Localization with Error Management," in ACM MobiHoc, 2006, pp. 250 - 261.   
[5] X. Wang, J. Luo, Y. Liu, S. Li, and D. Dong, "Component-based localization in sparse wireless networks," IEEE/ACM Transactions on Networking (ToN), vol. 19(2), pp. 540-548, 2011.   
[6] J. Fang, M. Cao, A. S. Morse, and B. Anderson, "Sequential Localization of Sensor Networks," SIAM Journal on Control and Optimization, vol. 48, pp. 321-350, 2009.   
[7] D. Moore, J. Leonard, D. Rus, and S. J. Teller, "Robust distributed network localization with noisy range measurements," in ACM SenSys, Baltimore, MD, 2004, pp. 50 - 61.   
[8] X. Wang, Y. Liu, Z. Yang, J. Liu, and J. Luo, "ETOC: Obtaining robustness in component-based localization," in IEEE ICNP, 2010, pp. 62-71.   
[9] Y. Shang and W. Ruml, "Improved MDS-based localization," in IEEE INFOCOM, Hong Kong, China, 2004, pp. 2640 - 2651.   
[10] B. K. P. Horn, H. M. Hilden, and S. Negahdaripour, "Closed-form solution of absolute orientation using orthonormal matrices," Journal of the Optical Society of America A, vol. 5, pp. 1127-1135, 1988.   
[11] H. T. Kung, C.-K. Lin, T.-H. Lin, and D. Vlah, "Localization with snap-inducing shaped residuals (SISR): coping with errors in measurement," in the 15th annual international conference on Mobile computing and networking (Mobicom), 2009, pp. 333-344.   
[12] M. J. D. Powell, "An efficient method for finding the minimum of a function of several variables without calculating derivatives," The Computer Journal, vol. 7(2), pp. 155-162, 1964.   
[13] "GreenOrbs http://greenorbs.org/."   
[14] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, and X. Li, "Canopy closure estimates with GreenOrbs: Long-term large-scale sensing in the forest," in ACM SenSys, Berkeley, California, USA, 2009, pp. 99-112.   
[15] T. Eren, D. K. Goldenberg, W. Whiteley, Y. R. Yang, A. S. Morse, B. D. O. Anderson, and P. N. Belhumeur, "Rigidity, computation, and randomization in network localization," in IEEE INFOCOM, Hong Kong, China, 2004, pp. 2673 - 2684.   
[16] D. K. Goldenberg, A. Krishnamurthy, W. C. Maness, Y. R. Yang, and A. Young, "Network localization in partially localizable networks," in IEEE INFOCOM, Miami, FL, 2005, pp. 313 - 326

[17] R. Stoleru, T. He, S. S. Mathiharan, S. M. George, and J. A. Stankovic, "Asymmetric Event-Driven Node Localization in Wireless Sensor Networks," IEEE Transactions on Parallel and Distributed Systems (TPDS), vol. 23(4), pp. 634 -642, 2012.   
[18] Z. Zhong and T. He, "RSD: A Metric for Achieving Range-Free Localization beyond Connectivity," IEEE Transactions on Parallel and Distributed Systems (TPDS), vol. 22(11), pp. 1943 -1951, 2011.   
[19] J. Jeong, S. Guo, T. He, and D. H. C. Du, "Autonomous Passive Localization Algorithm for Road Sensor Networks," IEEE Transactions on Computers (TC), pp. 1622 -1637, 2011.   
[20] J. Aspnes, D. Goldenberg, and Y. R. Yang, "On the Computational Complexity of Sensor Network Localization," in Algorithmic Aspects of Wireless Sensor Networks: First International Workshop (ALGOSENSORS), 2004, pp. 32–44.   
[21] Z. Yang and Y. Liu, "Quality of Trilateration: Confidence-Based Iterative Localization," IEEE Transactions on Parallel and Distributed Systems (TPDS), vol. 21, pp. 631 - 640 2010.   
[22] O.-H. Kwon, H.-J. Song, and S. Park, "Anchor-Free Localization through Flip-Error-Resistant Map Stitching in Wireless Sensor Network," IEEE Transactions on Parallel and Distributed Systems (TPDS), vol. 21(11), pp. 1644-1657, 2010.   
[23] S. Lederer, Y. Wang, and J. Gao, "Connectivity-based localization of large scale sensor networks with complex shape," in IEEE INFOCOM, Phoenix, Arizona, USA, 2008, pp. 789 - 797.   
[24] W. Liu, D. Wang, H. Jiang, W. Liu, and C. Wang, "Approximate Convex Decomposition Based Localization in Wireless Sensor Networks," in IEEE INFOCOM, 2012, pp. 1853-1861.   
[25] M. Jin, S. Xia, H. Wu, and X. Gu, "Scalable and Fully Distributed Localization With Mere Connectivity," in IEEE INFOCOM, 2011, pp. 3164-3172.   
[26] H. Jamali-Rad, H. Ramezani, and G. Leus, "Sparse Multi-Target Localization Using Cooperative Access Points," in Sensor Array and Multichannel Signal Processing Workshop (SAM), 2012, pp. 353-356.   
[27] W. Cheng, A. Y. Teymorian, L. Ma, X. Cheng, X. Lu, and Z. Lu, "Underwater Localization in Sparse 3D Acoustic Sensor Networks," in IEEE Infocom, 2008, pp. 798-806.

![](images/f7dabe3fd723e6e911c8abcef721d4eab411c11dca8acacf867b38d29643f409.jpg)



Xiaoping Wang received his BS, MS, and Ph.D degree in the School of Computer Science from National University of Defense Technology, China, in 2003, 2005, and 2010, respectively. He is now an assistant professor in the School of Computer Science at National University of Defense Technology. His research interests include parallel and distributed computing.

![](images/2b56ff4309644d9cfa7c5a8e1da3d455b340ef79381c608f8517e140baa1cf26.jpg)



Yunhao Liu (M'02–SM'06) received his BS degree in Automation Department from Tsinghua University, China, in 1995, and an MA degree in Beijing Foreign Studies University, China, in 1997, and an MS and a Ph.D. degree in Computer Science and Engineering at Michigan State University in 2003 and 2004, respectively. He is a member of Tsinghua National Lab for Information Science and Technology, and the Director of Tsinghua National MOE Key Lab for Information Security

ty. He is also a faculty at the Department of Computer Science and Engineering, the Hong Kong University of Science and Technology. Being a senior member of IEEE, he is also the ACM Distinguished Speaker.

![](images/f7c780f8dca7cc141d6a561e79021cac2ce44f219de9df57f3dd41a6326b4794.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree from Hong Kong University of Science and Technology in 2010. His main research interests include wireless ad-hoc/sensor networks and pervasive computing. He has published over 40 of research papers in highly recognized journals and conference, including IEEE/ACM Transactions on Networking (ToN), IEEE

Transactions on Parallel and Distributed Systems (TPDS), ACM MobiCom, IEEE INFOCOM, IEEE ICDCS, IEEE RTSS, ACM SenSys, etc. He is a member of the IEEE and the ACM.

![](images/7f89ce1c0906bb561c1618002002c907795ec58737431484d3419d0faf70ddee.jpg)



Kai Lu received his BS and Ph.D degree in the School of Computer Science at National University of Defense Technology, China, in 1995 and 1999, respectively. He is now a professor in the School of Computer Science at National University of Defense Technology. His research interests include high performance computing, operating system, parallel computing, and sensor networking.

![](images/e075af9335ebcccf0041ce3535f86aa09741858a8e52cce92c9c4f22a10ffefd.jpg)



Jun Luo received his BS degree in Computer School from Wuhan University, China, in 1984, and an MS degree in the School of Computer Science at National University of Defense Technology, China, in 1989. He is now a professor in the School of Computer Science at National University of Defense Technology. His research interests include operating system, parallel computing, security,

and sensor networking.