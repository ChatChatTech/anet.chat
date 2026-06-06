# Topology Shaping for Time Synchronization in Wireless Sensor Networks

Xiaoxu Li $^{1}$ , Qiang Ma $^{2}$ , Wei Sun $^{1}$ , Kebin Liu $^{2}$ , Yunhao Liu $^{2}$

1 Department of Computer Science and Engineering, Hong Kong University of Science and Technology

2 TNLIST, School of Software, Tsinghua University

Abstract—Time synchronization plays an important role in wireless sensor networks (WSNs). Due to the unique features of WSNs such as remote deployment, low-cost hardware, and restrictive energy supply, accurate and robust time synchronization is still a challenging task. Many approaches have been proposed to improve the performance and efficiency of time synchronization. Existing schemes, however, do not pay enough attention to the impacts of varying network topology properties, including network diameter, degree distribution, and the like. They can experience unexpected performance degradation in many real systems.

To address these issues, we present a novel approach, which tries to improve the performance of existing time synchronization algorithms by introducing a virtual overlay. We propose an integrated model, called topo-refiner, which encodes the impact of different network topology features to the precision and robustness of time synchronization. Also, we design a novel optimization algorithm to build a virtual overlay from the underlying communication network. Our approach is orthogonal to existing clock synchronization methods, and can improve their performance by operating these methods atop the virtual layer. Finally, in order to verify the effectiveness of our approach, we conduct extensive simulations on synthetic and real system traces, as well as testbed experiments. Results show that topo-refiner is practical, and quickly adapts to varying time synchronization accuracy requirements for applications in WSNs.

# I. INTRODUCTION

A wide range of applications in WSNs requires its participants to maintain a common notion of time, which necessitates the use of a synchronization service $[3]$ . For example, applications using TDMA require locally well synchronization between neighbor nodes. Furthermore, common services in WSNs, such as power management $[12]$ $[24]$ $[19]$ , data collection $[14]$ , and network security $[17]$ , also depend on the existence of global time. However, due to the extreme limitations on sensor nodes (e.g., limited computation and storage capabilities, tight energy budget, and unstable clock rate), accurate time synchronization remains a challenging task.

Due to the clock drift $^{1}$ , ad-hoc communication delay, and network topology properties, accurate time synchronization service is hard to achieve in WSNs. Previous research on this issue mostly focuses on how to compensate errors caused by clock drift and message delay to achieve better synchronization accuracy (e.g., FTSP [13], ODS [25], and TIRP [9]). These schemes, however, do not pay enough attention to the impact of different topology properties on the performance of time synchronization methods. For instance, given two WSNs with topologies shown in Fig.1(a) and Fig.1(b) respectively, they have an equal number of nodes and links. The only delicate difference between the two cases is that, node 6 is connected with node 5 in (a), instead of node 2 in (b). Assuming that we carry out FTSP, the state-of-the-art time synchronization protocol, on the two topologies. In the experiment, node 1 is allocated as the root, which periodically broadcasts timestamp messages. And a, b, c stand for three synchronization paths. Then clock offset between each other node and the root is calculated. A node denoted by a circle with large radium and dark color implies that the node exhibits a large clock offset with the root. Intuitively, it is easy to find that nodes in (b) achieve better synchronization accuracy than those in (a). Also, the specific clock offset value of each node is shown in Fig.1(c).

Many existing time synchronization methods are flooding-based, which try to compensate errors caused by clock drift and message delay. But such approaches suffer accumulated errors at each hop, and the synchronized state may not be preserved with the growth of network size and changes of network topology. A question comes to us, can we improve the performance of existing time synchronization methods by minor adjusting network topology? In fact, our observation is supported by [10], they have proved that the smallest possible global skew $^{2}$ that any algorithm can achieve is $\Omega(D\mathcal{T}/2)$ , where D denotes the diameter of the graph, and T denotes the message delay. Meanwhile, no continuous clock synchronization algorithm can achieve a better bound on the local skew $^{3}$ than $\Omega(\alpha\mathcal{T}(1+\log_{1/\varepsilon}D))$ , where $\varepsilon$ is the clock rate, and $\alpha\in\mathcal{O}(1-\varepsilon)$ is the lower bound of clock drift. The theoretical proofs point out that, besides clock drift and message delay, network topology properties is another significant factor that influences the performance of synchronization service. Therefore, we argue that the design of time synchronization scheme should take topology properties into account for the best performance. There are several challenges for us to overcome. (1) Once a WSN is deployed, the topology is kind of fixed. It is not realistic to change the underlying network topology. The problem is proved in [5] [9] that the resulting synchronization between two arbitrary nodes depends on the effective diameter of a virtual overlay, which is used for operating time synchronization methods. (2) By building a virtual overlay, existing time synchronization methods operate on the overlay as operating on the underlying network. The challenge is, how to model our problem, in order to get a virtual overlay, which has the minimized effective diameter with taking many topology properties (e.g., degree distribution and cost of communication) into account. In algebraic graph theory, the constraint between Laplacian eigenvalue and network diameter impels us to build an integrated model, which takes original network topology information as input, and output the expected overlay topology. (3) Another challenge is that we must find a proper way to set up the overlay, which can easily operates in real networks, and not costs so much energy consuming. As we all know, we can change sensor nodes power to enable topology control, but it may cause unnecessary energy consumption. In our approach, we introduce a one-hop synchronization scheme, namely Reference Broadcast Synchronization (RBS), to build up the overlay. With this method, we do not need to change the power of sensor nodes.

![](images/19ddbc7457679adfa21a40e4ef840805352eeec7115e073042a409c8d13c1cce.jpg)



(a) original topology

![](images/d5bf83e9eb3817af403412336494270e235122efc0409a222ebdbf74b7f2c3d3.jpg)



(b) refined topology

![](images/c8a00afaaddb18a039e86dd680805066b6cbb262499b627ded4fba77579f2fa9.jpg)



(c) Clock offset of each node   
Fig. 1: Different topologies impact on the accuracy of FTSP (Flooding Time Synchronization Protocol). (a) shows the original topology, and (b) is a refined topology. Node 1 is root, which periodically broadcasts synchronization message, and path a, b, and c denote three synchronization paths existing in two topologies. (c) shows clock offset value of each node.

This work proposes a novel strategy which tries to improve the performance of existing time synchronization algorithms by introducing a virtual overlay. A clock synchronization algorithm operates on the virtual layer as though it were the original network. In our approach, we present an integrated model, named topo-refiner, which encodes different practical constraints in WSNs. Also, we design a novel speedy algorithm to build a virtual overlay from the underlying communication network. The experimental results show that clock synchronization algorithms takes advantage of the virtual overlay. Our optimization approach is orthogonal to existing time synchronization methods, and brings benefits to these time synchronization algorithms. In short, the main contributions of this paper includes:

- To the best of our knowledge, our method is the first to investigate topology fine-tuning for the time synchronization problem, which takes real network conditions and energy efficiency into account. And it is orthogonal to current solutions.   
- We propose the optimization problem using the properties of the second smallest eigenvalue of graph

Laplacian, and obtain an optimal solution for the modelled time synchronization problem. Then we design a speedy algorithm that can be easily used in real systems.

Meanwhile, we introduce a topology refining scheme, which is energy efficiency, instead of depleting nodes' communication power.

\- The optimization model is evaluated by trace-driven simulations, and testbed experiments as well. The experiment results show that our method improves the accuracy of time synchronization prominently.

The rest of this paper is organized as follows. In section 2 and section 3, we introduce our approach in details. And experiments and evaluation results are illustrated in section 4 and section 5. Then, we introduce the related works about the current progress in time synchronization field in section 6. Finally, we will summarize this work in section 7.

# II. PRELIMINARY

In this section, we define the virtual layer used in our approach, including terminologies, network and clock models, as well as the means we use to build the virtual overlay. Both the models and methods are applied to design the integrated model topo-refiner in section 3.

# A. Network and Clock Models

We model a wireless sensor network as a connected, undirected graph $G = (V, E)$ of diameter D, where V represents a set of participating nodes in the network and and E represents that of bidirectional communication links. Each node is equipped with a continuous hardware clock $H(t)$ , and maintains a logical clock $L(t)$ . The hardware clock experiences an unstable, but bounded clock drift $\xi \in (0, 1)$ , which is subject to environment temperature, voltage, etc. We assume that at all times, the clock rate $h(t) := \frac{d}{dt} H(t) \in (1 - \xi, 1 + \xi)$ . In practice, the logical clock values are not allowed to change substantially within a short time, and it should behave as a real clock. The logical clock also has a bounded relative clock rate, and the logical clock value $L(t) = \int_{0}^{t} h(\tau) l(\tau) d\tau$ , with $l(t) \in (\alpha, \beta), \alpha, \beta > 0$ . Wireless communication is leveraged for synchronization messages exchanging among nodes. Exchanging messages, however, costs some time, that is highly non-deterministic. But it is also bounded by $\tau \in (0, \hat{\tau})$ . For instance, in CC2420, hardware clock drifts up to 40ppm per second, and $\hat{\tau}$ is up to a few ms. The goal of a clock synchronization algorithm is to output a logical value, such that at any time, the logical clock of different nodes are as close as possible.

![](images/5bfbe3ae02412604d0685d144c5a3a832721610bb378c0717e0b41bcc500f1bc.jpg)



Fig. 2: Reference Broadcast Synchronization scheme. Node $a$ and $c$ are two neighbors of node $b$ . At time $t$ , node $b$ broadcasts a beacon, and node $a$ and $c$ record their local timestamps when they receive the beacon. At time $t'$ , node $a$ and $c$ exchange their timestamps information, and they can estimate each other's local clock values.

# B. Virtual Layer Model

In this approach, we build a virtual layer provides a virtual topology $G^{sync} = (V, E^{sync})$ for time synchronization service, where each edge $(u, v) \in E^{sync}$ represents that u and v can estimate each others' the logical clock values by some means, such as point-to-point messages. Certainly, the edge in the virtual layer is related with a certain error, which depends on the precision of the estimation methods. Usually, we can manage network topology by changing nodes communication power. In this work, we present an alternative method to build the virtual layer. Reference broadcast synchronization (RBS) [7], a one-hop synchronization scheme, gives an accurate estimate of logical clock values between two-hop nodes. With RBS scheme, nodes send reference beacons to their neighbors using physical layer broadcasts. When a neighbor receives the reference, it records the beacon arrival time, and uses the time as a point of reference for comparing their logical clocks. The details of RBS mechanism are illustrated in Fig.2.

Node $b$ is a common neighbor of node $a$ and node $c$ . At time $t$ , $b$ broadcasts a reference beacon, and all its neighbors receive the beacon at the same time. Node $a$ and node $c$ record their logical clock value when they receive the beacon. Then, they exchange their time stamp message by broadcasting the records. Node $a$ and node $c$ can estimate each other's clock values. Such estimation result has a kind of error. In [7], the authors have proved that the distribution of such error is Gaussian. Let node $b$ broadcast several beacons, and node $a$ and node $c$ can reduce the estimate error by exchanging messages many times. According to the experiment results, the estimation error can be reduced up to $0.16\mu s$ . The accuracy can satisfy most of applications in WSNs.

# C. Algebraic Graph Theory

The underlying communication network can be specified as a simple undirected graph. Formally, given an undirected graph $G = (V, E)$ , for each vertex v, let $deg(v)$ represent the degree of node v. The $n \times n$ adjacency matrix of the graph G is $A = [a_{ij}]$ , with $a_{ij} = 1$ if $(i, j) \in E$ and 0 otherwise. And let $\mathcal{D} = diag(d_1, ..., d_n)$ denote the degree matrix. Then, the Laplacian matrix $\mathcal{L}(G) = \mathcal{D} - \mathcal{A}$ . For instance, given a simple graph G, its Laplacian matrix $\mathcal{L}(G) := (l_{ij})_{n \times n}$ is defined as

$$
l _ {i j} := \left\{ \begin{array}{l l} d e g (v _ {i}) & \text { if } i = j \\ - 1 & \text { if } i \neq j \text { and } v _ {i} \text { is   adjacent   to } v _ {j} \\ 0 & \text { otherwise } \end{array} \right.
$$

The Laplacian matrix [6] $\mathcal{L}(G)$ is a symmetric positive semi-defined matrix. Accordingly, all of its eigenvalues are nonnegative. Let $\lambda_1(\mathcal{L}) \leq \lambda_2(\mathcal{L}) \leq \ldots \leq \lambda_n(\mathcal{L})$ ( $n = |V|$ ) be the eigenvalues of $\mathcal{L}(G)$ . The multiplicity of zero eigenvalues of the Laplacian is equal to the number of connected components of $G$ . Consequently, for a connected graph, $\lambda_1 = 0$ and $\lambda_2 > 0$ . In the literature, $\lambda_2(\mathcal{L})$ is referred to as the algebraic connectivity of network. The problem was first addressed by Fiedler [6]. The second smallest eigenvalue of Laplacian has emerged as a critical parameter that is applied to several difficult problems [8] [15] in graph theory and system control. One of the most interesting connections is the relationship between $\lambda_2(\mathcal{L})$ and network diameter.

Theorem 1. [1] The eigenvalue $\lambda_{2}$ imposes an upper bound on the diameter of $G$ :

$$
\operatorname{diam} (\mathcal {L}) \leq 2 \lceil \frac {\Delta + \lambda_ {2} (\mathcal {L})}{4 \lambda_ {2} (\mathcal {L})} \ln (n - 1) \rceil
$$

where $\Delta$ is the maximal vertex degree of $G$ .

# III. TOPO-REFINER ARCHITECTURE DESIGN

As different topology properties can greatly influence the performance of time synchronization, we propose an integrated model topo-refiner to find an optimal solution of refining the current underlying communication topology by building a virtual overlay.

# A. An Integrated Optimization Model

Intuitively, if the diameter of virtual overlay is smaller than the original network diameter, time synchronization methods can achieve better accuracy by operating on the overlay. That means, our goal is to build a virtual overlay with the smallest network diameter, based on the underlying network. According to theorem 1, we can convert the problem of minimizing the network diameter to that of maximizing the second smallest eigenvalue $\lambda_{2}$ . The optimization problem can be formalized as:

$$
\Lambda : \max _ {G} \lambda_ {2} (\mathcal {L} (G)) \tag {1}
$$

Lemma 1. The optimization problem (1) can be converted to

$$
\begin{array}{l} \Lambda : \max _ {G} \gamma \\ s. t. P ^ {T} \mathcal {L} (G) P \geq \gamma I _ {n - 1} \\ \end{array}
$$

in which $\lambda_{2}$ is the upper bound of $\gamma$ , and $P$ is the unit matrix.

Proof: Given a Laplacian matrix $\mathcal{L}(G)-\gamma I_{n}$ , the eigenvalues of the matrix are $[-\gamma,\lambda_{2}-\gamma,\lambda_{3}-\gamma,\ldots,\lambda_{n}-\gamma]$ , so we have:

$$
\begin{array}{l} \lambda_ {2} \geq \gamma \\ \Leftrightarrow v _ {i} ^ {\prime T} (\mathcal {L} (\mathcal {G}) - \gamma I _ {n}) v _ {i} ^ {\prime} \geq 0, i = 2, \dots , n \text {   and   } v _ {1} ^ {\prime} = 1 \\ \Leftrightarrow \quad \text { for } x \in \mathbf {1}, x ^ {T} (\mathcal {L} (G) - \gamma I _ {n}) x \geq 0, x \neq 0 \\ \Leftrightarrow P ^ {T} (\mathcal {L} (G) - \gamma I _ {n}) P \geq 0 \\ \Leftrightarrow P ^ {T} (\mathcal {L} (G) P \geq P ^ {T} \gamma I _ {n} P = \gamma I _ {n - 1} \\ \end{array}
$$

Given a $\mathcal{L}(G)$ , we have $\max \gamma = \lambda_2$ .

The above optimization problem is formulated without considering any practical constraints in a real network. Intuitively, if two arbitrary nodes are allowed to communicate with each other directly, the network topology turns out to be a random graph, with the smallest diameter being exactly 1. This assumption, however, dose not hold in practice. For instance, in WSNs, the network diameter cannot be reduced to such small, due to the limitation of wireless communication range. To characterize the optimization problem for real networks, we need to add some constraints to the optimization model. In WSNs, we extract several typical constraints as follows:

- In our model, we use RBS scheme to set up the virtual overlay. Let G denote the original underlying communication graph, and $G^{RBS}$ denote a virtual that all the nodes in the network using RBS scheme. In our model, we allow that each node can estimate the logic clocks of other nodes at no more than the distance of two hops. In other words, a node can communicate with its two-hop neighbors using RBS scheme.   
- Base on the constraint above, if we allow a node to set up RBS scheme with all its two-hop neighbors, it may cause a problem that some nodes in the network may have too many neighbors. And these nodes become the bottleneck nodes in the network. This may lead to many network problems, such as unbalanced traffic load, and severe network interferences. To avoid this situation, we let the degree of each node not exceed a constraint $deg_{max}$ , and the value is set as the maximum degree of the original graph in our model.   
- Additionally, setting up RBS scheme between two nodes also costs time and energy. In order to reduce the overhead, we make that only a certain fixed number of nodes to participate in setting up RBS scheme.

Adding these three constraints, our objective function (1) can be modified as:

$$
\Lambda : \quad \max _ {G ^ {L}} \gamma \tag {2}
$$

$$
\text { s.t. } \quad P ^ {T} L _ {G} P \geq \gamma I _ {n} - 1 \tag {3}
$$

$$
\left(G ^ {L}\right) ^ {T} = G ^ {L} \tag {4}
$$

$$
G ^ {L} \geq G ^ {R B S} \tag {5}
$$

$$
G ^ {L} \cdot \mathbf {1} \leq d e g _ {\max} \cdot \mathbf {1} \tag {6}
$$

$$
\mathbf {1} \cdot G ^ {L} \cdot \leq 2 (1 + \varphi) | E |. \tag {7}
$$

Formula (2) is the objective function, and the output topology $G^{L}$ has the smallest diameter, considering the above conditions. Formula (4) says that $G^{L}$ is symmetric, because the communication in $G^{L}$ is bidirectional. Formula (5) to (7) refer to the three constraints respectively. The parameter $\varphi$ in the last line represents a percentage, which means how many new virtual links can be set up in the virtual overlay.

Corollary 1. The topology output by the optimization model, has the diameter $D' \geq \frac{1}{2} D$ , where $D$ is the diameter of original graph.

Proof: In our model, two-hop neighbors are allowed to set a virtual link between each other. The limiting case is that all the two-hop neighbors have virtual links. Then the virtual overlay is denoted as $G^{RBS}$ , with the diameter $D^{RBS} = \frac{1}{2}D$ . So using our model the diameter has the upper bound of $\frac{1}{2}D$ .

The general formulation of the optimization problem $\Lambda$ is time consuming and it does not provide any efficient clues about how to calculate $\lambda_{2}$ iteratively. In the next section, we propose a speedy algorithm to help us solve the optimization problem efficiently.

# B. A Speedy Algorithm

Give the original network, the algorithm takes the underlying network topology information as input, and outputs the virtual overlay topology. But the time complexity of the optimization problem is $\mathcal{O}(n^{2m})$ , in which n is the number of nodes, and m is the number of virtual links. That means the method is not feasible when the network has a large number of nodes. To solve the problem, we design a speedy algorithm.

Algorithm 1 Speedy Algorithm   
1: Compute the Laplacian matrix $\mathcal{L}(G)$ of the original graph $G$ 2: Compute the second smallest eigenvector $v_{2}$ of $\mathcal{L}(G)$ 3: Set $max_{t} = -1$ , $max_{i} = -1$ , $max_{j} = -1$ 4: for all possible edge $(i,j)$ with the original distance in 2 hops do  
5: set vector $\pmb{x}$ as $x_{i} = 1$ , $x_{j} = -1$ , and set others 0  
6: compute temp = $\pmb{v_2^T} \cdot \pmb{x} \cdot \pmb{x}^T \cdot \pmb{v_2}$ 7: if temp > max $_t$ 8: max $_t$ = t  
9: end if  
10: end for

In practice, multiple diameters may exist in a network, and the thinking of the speedy algorithm is that we can update the topology by adding one virtual link at each step.

For an adjacent matrix $A = [a_{ij}]$ of original graph G, we add a new link between i and j, which is equivalent to change $a_{ij}$ and $a_{ji}$ from 0 to 1. Then the values changes in the relevant Laplacian matrix $\mathcal{L}(G)$ is $l_{ii} = l_{ii} + 1$ , $l_{jj} = l_{jj} + 1$ , and $l_{ij} = l_{ij} - 1$ , $l_{ji} = l_{ji} - 1$ . Also, we denote the change of the Laplacian matrix as $L_G = L_G + Q$ , where

$$
Q _ {x y} := \left\{ \begin{array}{l l} 1 & \text { if } x = y = i \text { or } x = y = j \\ - 1 & \text { if } x = i y = j \text { or } x = j y = i \\ 0 & \text { otherwise } \end{array} \right.
$$

We can denote $Q = xx^{T}$ , where $\mathbf{x}^{T} = (0, \ldots, 0, x_{i} = 1, 0, \ldots, 0, x_{j} = -1, 0, \ldots, 0)_{n \times 1}$ . As we know $\lambda_{2}(L_{G}) = v_{2}^{T} L_{G} v_{2}$ , where $v_{2}$ is the eigenvector of $\lambda_{2}$ , after adding a new link to the original topology, the eigenvalue and eigenvector change to $\lambda' = (v_{2}^{T})' \cdot (\mathcal{L} + \mathbf{x} \cdot \mathbf{x}^{T}) \cdot v_{2}'$ . We assume that the structure of the network does not change too much when introducing a new link. Then we can approximately compute $\lambda' = v_{2}^{T} \cdot (\mathcal{L} + \mathbf{x} \cdot \mathbf{x}^{T}) \cdot v_{2} = \lambda_{2} + \mathbf{x} \cdot \mathbf{x}^{T} \cdot v_{2}$ .

Using the speedy algorithm, the model outputs an approximately optimal topology. The topology is the virtual layer setting up using RBS scheme, and a time synchronization algorithm can operate on it.

# IV. IMPLEMENTATION

To evaluate our method, we use both simulations and test-bed experiments. In simulations, we carried out a series of trace-driven experiments, including synthetic and a real system traces. And apart from the simulations, we also set up a 30-node testbed experiment to evaluate our method. In this section, we illustrate the configuration environment of the experiments, including empirical data, as well as three scenarios that will be adopted by the analysis in the next section.

# A. Experiment Environments

Synthetic trace: We generate 5 random graphs, each with 200 nodes. Every node has stochastic coordinates in a 2D space, and relative communication range. Ensuring the connectivity of the network, we approximately choose a small radium as the node's communication radium. Details of the synthetic trace are shown in Table 1.

TABLE I: Synthetic traces. 

<table><tr><td>Edges no.</td><td>Diameter</td><td>Max. degree</td></tr><tr><td>850</td><td>17</td><td>17</td></tr><tr><td>877</td><td>15</td><td>18</td></tr><tr><td>794</td><td>20</td><td>19</td></tr><tr><td>873</td><td>14</td><td>20</td></tr><tr><td>702</td><td>19</td><td>15</td></tr></table>

Real system trace: Meanwhile, in our simulations, we carry out an experiment using a real WSN system deployed in a city. The system contains four sub-networks, and we use one of them in our evaluation. The real system trace contains 236 nodes, with 1086 edges and maximum degree 14, as shown in Fig.3.

Testbed experiment: In order to verify the effectiveness of our approach, we also implement our method on the testbed. The testbed experiment contains 30 sensor nodes, and these nodes set up a multi-hop self-organizing WSN.

# B. Scenarios

We investigate the performance of our method in a variety of scenarios which demonstrate the efficiency of the method. The scenarios include comparison with a baseline algorithm in the diameter reduction ratio and cost, as well as the performance of time synchronization algorithms. In our cases, we use currently the state-of-the-art time synchronization algorithm FTSP in the experiments. For each scenario, we conduct 5 rounds of independent test.

![](images/97968a6fa1828f3f8f6cd6185fbe1f1b59dc1c2965d85f7a068c30c2058c7979.jpg)



Fig. 3: Real system graph

Diameter Reduction: As mentioned in the optimization problem, the objective function is set to achieve a smallest diameter subjected to the constraints. In this scenario, we try to find the performance of topo-refiner in diameter reduction. Also, we compare our method with a baseline algorithm. Each time adding a new virtual link each time, the diameter is calculated.

Degree Distribution: Degree distribution is related to network conflicts and affects the traffic loads. Assume that the underlying communication network is deployed with degree distribution management, in the virtual overlay, we also want to keep such degree constraint, and we set a degree constraint in our integrated model. In the experiments, we design several tests to observe the influence of nodes' degree, as well as the performance of topo-refiner with and without degree distribution constraint (DDC).

Time Synchronization Performance: We try to find the influence of our method on time synchronization algorithms performance. Two criterions are used to measure the time synchronization accuracy: global skew and local skew. We implement FTSP on the topology generated with topo-refiner and baseline algorithm.

# V. EVALUATION

We evaluated the performance of our model topo-refiner by testing each scenario in the experiments. Experiments with the identical setup are also performed for a baseline random algorithm.

# A. Diameter Reduction

Diameter reduction of topo-refiner is remarkable. We compare our approach with the baseline algorithm in this scenario. For each 200-nodes synthetic graphs, we implement both topo-refiner and the baseline approach. Each time adding a new virtual link to the graph, the second smallest eigenvalue $\lambda_{2}$ and the new diameter D are calculated. In the baseline algorithm, we keep all the constraints the same as in topo-refiner. While adding a new virtual link randomly, without taking the impact of the second smallest eigenvalue into account. In order to avoid losing the general comparison, we run 5 rounds of baseline algorithm for each topology graph. Then we use the average result of the 25 experiment results as the performance of the baseline algorithm.

![](images/2470c317606bb78baf3f754f9d9573eb2a2c82eaa3eb43e4e6d0a91643ae875a.jpg)



(a) Diameter reduction comparison

![](images/0caf02c3f6c808c9666f355e174faa2dcf51f2485c86ab49d45c4c6783e7311d.jpg)



(b) Impact of degree distribution constraint

![](images/8f54f76edbcea43a5cc8adc33471080ba4b167b8164f444eed4603f36c2b97c4.jpg)



(c) Diameter reduction with vs. without DDC

![](images/df8478951cae3bd9939f76a8821702eefaf5cd3e5111d5b145975f78fbb29b4f.jpg)



(d) Diameter reduction cost

![](images/76660e83dac771189ff01ad9c113de91eb7ea8f2746213f57adf2cb6d2479e44.jpg)



(e) Comparison of global skew using FTSP

![](images/52fc11181cd4f7b33029f931dd751d54b41793bb7bc7b4029d15db106c7a92de.jpg)



(f) Comparison of local skew using FTSP   
Fig. 4: Evaluation of topo-refiner, in topology fine tuning, time synchronization performance

The experimental results of 200-nodes synthetic topologies are shown in Fig.3. The x-axis is the number of newly added virtual links, and the y-axis is the diameter reduction ratio, which is equal to $\frac{Newdiamtermeter}{Originaldiameter}$ after adding a new virtual link. As the result shown, the diameter, using topo-refiner, is quickly reduced to an acceptable level, for example below 60% of original diameter, after adding a small number of virtual links. After reaching the acceptable level, the diameter does not change much with the increasing of newly added virtual links. In Fig.4(d), the y-axis is the diameter reduction profit. In our case, we have two kinds of calculation for this profit: First, assume that cost=the number of virtual links, then the profit can be calculated as

$$
p r o f i t = \frac {\text {   Diameter   reduction   ratio   }}{\text {   the   number   of   added   edges   }}.
$$

Second, according to law of diminishing returns, the cost and the number of virtual links is logarithmic. The profit can be rewrote as

$$
\text { profit } = \frac {\text { the   proportion   of   diameter   reduction }}{\log (\text { the   number   of   added   edges } + 1)}.
$$

In the result, we observe that we can add about 25% of the original number of edges to gain the maximum profit.

# B. Degree Distribution

In our integrated model, we add a degree distribution constraint in the optimization function. For majority of nodes in wireless sensor network, we prefer that nodes have a uniform degree distribution. The reason is obvious, the power of the network is limited, and a node with a large degree turns to be a critical node, which costs more power than others. Then, the degree distribution can help balance the power consumption, as well as reduce the interference of the whole network. In the scenario, we analyze the influence of degree distribution constraint in the model. As we can see the result in Fig.4(b), the y-axis $\frac{\Delta deg'}{\Delta deg}$ , where $(\Delta deg = \max(degree) - \min(degree))$ is the degree skew in original graph, and $\Delta deg'$ is the degree skew after adding a virtual link. The result shows that the degree skew is almost in linear increase with the number of virtual links, if we do not add degree distribution constraint in the model.

Second, we want to find out whether the model with degree distribution constraint compromises the performance of diameter reduction or not. The experiment result is showed in Fig.4(c). We can see that the diameter reduction ratios is nearly the same in the model with or without the constraint.

# C. Time Synchronization Performance

The most important aspect we want to find is that whether our approach improves the performance of time synchronization or not. In our cases, we use FTSP to test the performance of both topo-refiner and baseline algorithm. In simulations, we use the synthetic and real system traces, and the result is shown in Fig.4(e)(f) and Fig.6(a)(b). Also, we implement FTSP in the testbed experiment, and see the result in Fig.5(c)(d). As the result shown, the global and local skew is improved prominently. The details are shown in Table 2. From the results, we can observe that, using our approach, the global skew of FTSP has been improved almost $8 \mu s$ , and the local skew has been improved about $2 \mu s$ .

![](images/7b7734cf2763a8ca4217ade275661e6a71af0d2beeb63c15b0276f2344fc4721.jpg)



(a) 30-node original topology

![](images/70de7c8d8bb90e765b4d5b1c409514683977cc85e73ea6cf77578fc14bfb4375.jpg)



(b) 30-node optimal topology

![](images/815fc8fa5fb993693aa102c53b6dc6c67acb9521c41871603cdaba521683a818.jpg)



(c) FTSP: global skew

![](images/35b34138087f8a9e97216e69a6c94c9040cbdaeaa27363842fb390127c108f7a.jpg)



(d) FTSP: local skew

Fig. 5: 30-nodes experiment   
![](images/f92247461cc60e74afb3fe7f4f7b57c5de2d30270ba871f0cb25d608f829167d.jpg)



(a) FTSP: global skew

![](images/481f10f4799cf76f08e0d7775e14f772fd4658c8a2c59e0c160aecf4da913f0c.jpg)



(b) FTSP: Local skew   
Fig. 6: Real system evaluation

TABLE II: Accuracy of FTSP. 

<table><tr><td></td><td>Original topo.</td><td>Refined topo.</td></tr><tr><td>Global skew(μs)</td><td>19.51</td><td>11.71</td></tr><tr><td>Local skew(μs)</td><td>7.01</td><td>5.79</td></tr></table>

# VI. RELATED WORK

Clock synchronization has been studied extensively long before the advent of wireless sensor networks, both in theoretical and practical research $[18]$ $[23]$ . The classic solution is an atomic clock, such as in the global positioning system (GPS). Equipping each sensor with a GPS receiver is feasible, but there are limitations in the form of cost and energy. Classic clock synchronization algorithms rely on the ability to exchange messages at a high rate which may not be possible in WSNs. Traditional time synchronization algorithms like the Network Time Protocol (NTP) $[16]$ are due to their complexity not well suited for sensor network applications. In addition, as their application domain is different, they are not accurate enough for our purpose, even in LAN they may experience skews in the order of milliseconds.

Applications in WSNs require sophisticated algorithms for clock synchronization since the hardware clocks in sensor nodes are simple and may experience significant drift, due to environment temperature, voltage, etc. Also, in contrast to wired networks, the multi-hop character of wireless sensor networks complicates the problem, as one cannot simply employ a standard client/server clock synchronization algorithm. The Flooding Time Synchronization Protocol (FTSP) [13] is thought of as the state-of-art protocol. A root node is elected which periodically floods its current timestamp into the network forming an ad-hoc tree structure. MAC layer timestamping reduced possible sources of uncertainty in the message delay. Each node uses a linear regression table to convert between the local hardware clock and the clock of the reference node. Since the method is based on a tree structure, a cumulated error is introduced at each hop. Some methods, including fast flooding approaches(Glossy [4], PulseSync [2]), message delay modeling and against routing-integrated approaches(ODS [25],FEV [22] [20]), are proposed such as efficient flooding and uncertainties modeling, to improve the accuracy of FTSP.

Besides flooding-based approaches, there is another kind of time synchronization scheme, gradient time synchronization protocol (GTSP), which is non-structure based method. The approach is introduced to proof the theoretical bounds of time synchronization in distributed systems $[10]$ $[11]$ . The authors Kuhn al. $[21]$ proposed a practical way to apply GTSP in WSNs. One of the advantages of non-structure based methods is that a good local skew performance can be achieved.

Until now, the current protocols do not concern about the influence of network topology properties. However, the existing theoretical work has proved that both the global and local skews are related to network topology properties, especially network diameter. It has been proved that the skew of D/2 cannot be avoided on any graph G with diameter D. The authors Lenzen al. [11] [9] [10] also provide a set of optimal algorithms and proved that the global skew with the tight bound $\Omega(D\mathcal{T}/2)$ , where D denotes the diameter of the graph, and T denotes the message delay. Moreover, the local skew $\Omega(\alpha\mathcal{T}(1+\log_{1/\varepsilon}D))$ , where $\varepsilon$ is the clock rate, and $\alpha\in\mathcal{O}(1-\varepsilon)$ is the lower bound of clock drift. In [5] [9], the authors first introduce an abstraction of the underlying communication graph to verify the performance of clock synchronization algorithms, and the tight bounds are provided in the work.

# VII. CONCLUSION

In this work we propose an integrated optimization model, named topo-refiner. We first figure out the topology control strategy on time synchronization problem. Using the properties of the second smallest eigenvalue of graph Laplacian, we propose our method that output an abstraction of underlying communication graph with optimal diameter in a theoretical way. Then we design a speedy algorithm that can be operated in real systems. The integrated solution takes underlying network topology properties as input, and outputs the expected topology, taking multiple network topology properties into account. Finally, we carry out the experiments on both synthetic data and real system traces, and give carefully analysis of the results. The experiment results show that our method improves the performance of existing clock synchronization algorithms prominently. The goal of this paper is to bridge the gap between theory and practice performance of clock synchronization in WSNs. Our approach can also be extend to other applications in WSNs, such as fast packets forwarding. Actually, there are still other topologys properties need to be considered in order to satisfied the robustness conditions. This issue can be researched deeply in the future.

# REFERENCES

[1] A. Berman and X.D. Zhang. Lower bounds for the eigenvalues of laplacian matrices. Linear Algebra and its Applications, 316(1):13-20, 2000.   
[2] P. Sommer C. Lenzen and R. Wattenhofer. Optimal clock synchronization in networks. In Proceedings of Sensys, pages 225-238, 2009.   
[3] J. Elson and K. Römer. Wireless sensor networks: A new regime for time synchronization. ACM SIGCOMM Computer Communication Review, 33(1):149–154, 2003.   
[4] L. Thiele F. Ferrari, M. Zimmerling and O. Saukh. Efficient network flooding and time synchronization with glossy. In Information Processing in Sensor Networks (IPSN), 2011 10th International Conference on, pages 73–84, 2011.   
[5] T. Locher F. Kuhn, C. Lenzen and R. Oshman. Optimal gradient clock synchronization in dynamic networks. In Proceeding of the 29th ACM SIGACT-SIGOPS symposium on Principles of distributed computing, pages 430-439, 2010.   
[6] M. Fiedler. A property of eigenvectors of nonnegative symmetric matrices and its application to graph theory. Czechoslovak Mathematical Journal, 25(100):619–633, 1975.   
[7] L. Girod J. Elson and D. Estrin. Fine-grained network time synchronization using reference broadcasts. ACM SIGOPS Operating Systems Review, 36(SI):147–163, 2002.   
[8] Y. Kim and M. Mesbahi. On maximizing the second smallest eigenvalue of a state-dependent graph laplacian. Automatic Control, IEEE Transactions on, 51(1):116–120, 2006.

[9] F. Kuhn and R. Oshman. Gradient clock synchronization using reference broadcasts. Principles of Distributed Systems, pages 204-218, 2009.   
[10] C. Lenzen, T. Locher, and R. Wattenhofer. Clock synchronization with bounded global and local skew. In Foundations of Computer Science, 2008. FOCS'08. IEEE 49th Annual IEEE Symposium on, pages 509-518. IEEE, 2008.   
[11] C. Lenzen, T. Locher, and R. Wattenhofer. Tight bounds for clock synchronization. Journal of the ACM (JACM), 57(2):8, 2010.   
[12] Y. Liu, Y. He, M. Li, J. Wang, K. Liu, L. Mo, W. Dong, Z. Yang, M. Xi, J. Zhao, et al. Does wireless sensor network scale? a measurement study on greenorbs. In INFOCOM, 2011 Proceedings IEEE, pages 873–881. IEEE, 2011.   
[13] G. Simon M. Maróti, B. Kusy and Á. Lédeczi. The flooding time synchronization protocol. In Proceedings of Sensys, pages 39–49, 2004.   
[14] X. Mao, X. Miao, Y. He, T. Zhu, J. Wang, W. Dong, X. LI, and Y. Liu. Citysee: Urban co2 monitoring with sensors. In IEEE INFOCOM, 2012.   
[15] R. Merris. Laplacian matrices of graphs: a survey. Linear algebra and its applications, 197:143-176, 1994.   
[16] D.L. Mills. Internet time synchronization: The network time protocol. Communications, IEEE Transactions on, 39(10):1482–1493, 1991.   
[17] M. Pajic and R. Mangharam. Anti-jamming for embedded wireless networks. In Information Processing in Sensor Networks, 2009. IPSN 2009. International Conference on, pages 301–312. IEEE, 2009.   
[18] B. Patt-Shamir and S. Rajsbaum. A theory of clock synchronization. In Proceedings of the twenty-sixth annual ACM symposium on Theory of computing(STOC'94), pages 810-819, 1994.   
[19] A. Rowe, V. Gupta, and R.R. Rajkumar. Low-power clock synchronization using electromagnetic energy radiating from ac power lines. In Proceedings of the 7th ACM Conference on Embedded Networked Sensor Systems, pages 211–224. ACM, 2009.   
[20] T. Schmid, D. Torres, and M.B. Srivastava. Low-power high-precision timing hardware for sensor networks. In Proceedings of the 7th ACM Conference on Embedded Networked Sensor Systems, pages 337–338. ACM, 2009.   
[21] Philipp Sommer and Roger Wattenhofer. Gradient clock synchronization in wireless sensor networks. In Proceedings of the 2009 International Conference on Information Processing in Sensor Networks, pages 37–48. IEEE Computer Society, 2009.   
[22] Z. Anagnostopoulou M. B. Srivastava T. Schmid, Z. Charbiwala and P. Dutta. A case against routing-integrated time synchronization. In Proceedings of the 8th ACM Conference on Embedded Networked Sensor Systems, pages 267-280, 2010.   
[23] D. Veitch, S. Babu, and A. Pásztor. Robust synchronization of software clocks across the internet. In Proceedings of the 4th ACM SIGCOMM conference on Internet measurement, pages 219–232. ACM, 2004.   
[24] W. Ye, F. Silva, and J. Heidemann. Ultra-low duty cycle mac with scheduled channel polling. In Proceedings of the 4th international conference on Embedded networked sensor systems, pages 321–334. ACM, 2006.   
[25] Z. Zhong, P. Chen, and T. He. On-demand time synchronization with predictable accuracy. In INFOCOM, 2011 Proceedings IEEE, pages 2480–2488. IEEE, 2011.