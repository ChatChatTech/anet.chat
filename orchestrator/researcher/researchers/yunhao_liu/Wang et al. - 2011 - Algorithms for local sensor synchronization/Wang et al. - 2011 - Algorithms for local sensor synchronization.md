# Algorithms for Local Sensor Synchronization

Lixing Wang, Yin Yang, Xin Miao, Dimitris Papadias, Yunhao Liu

Department of Computer Science and Engineering, Hong Kong University of Science and Technology

Clear Water Bay, Hong Kong

{lxwang, yini, miao, dimitris, liu}@cse.ust.hk

Abstract— In a wireless sensor network (WSN), each sensor monitors environmental parameters, and reports its readings to a base station, possibly through other nodes. A sensor works in cycles, in each of which it stays active for a fixed duration, and then sleeps until the next cycle. The frequency of such cycles determines the portion of time that a sensor is active, and is the dominant factor on its battery life. The majority of existing work assumes globally synchronized WSN where all sensors have the same frequency. This leads to waste of battery power for applications that entail different accuracy of measurements, or environments where sensor readings have large variability.

To overcome this problem, we propose LS, a query processing framework for locally synchronized WSN. We consider that each sensor $n_i$ has a distinct sampling frequency $f_i$ , which is determined by the application or environment requirements. The complication of LS is that $n_i$ has to wake up with a network frequency $F_i \geq f_i$ , in order to forward messages of other sensors. Our goal is to minimize the sum of $F_i$ without delaying packet transmissions. Specifically, given a routing tree, we first present a dynamic programming algorithm that computes the optimal network frequency of each sensor; then, we develop a heuristic for finding the best tree topology, if this is not fixed in advance.

# I. INTRODUCTION

A sensor is a device with a radio and limited computation capabilities, which takes physical measurements such as temperature, light and humidity. A wireless sensor network (WSN) consists of a base station that collects measurements and/or aggregate information, and a set of sensor nodes, each of which is able to directly communicate with other sensors (or the base station) within the area of its radio coverage. Users register continuous queries at the base station, which are processed based on the sensor measurements. The transmission of sensor readings to the base station are performed according to the topology of the WSN, which can be either tree-based (e.g., [12]) or multi-path (e.g., [17]). This work follows the tree-based paradigm due to its simplicity and high energy efficiency.

In most applications, especially WSN deployed in harsh or difficult to access environments, sensor battery power is the main bottleneck of the entire system. In order to minimize energy consumption, instead of sensors being on continuously they operate in cycles. Specifically, within a cycle, each sensor is active for a fixed duration, during which it (i) collects measurements from the environment, (ii) receives data from other sensors in its network neighborhood, (iii) possibly performs computations $^{1}$ on the received and collected measurements, (iv) broadcasts data to the WSN, and then enters the sleep mode until it wakes up for the next cycle.

The power consumption of a sensor is dominated by the time that its radio remains on $[9][18][21]$ . Accordingly, since a sensor switches on its radio for a fixed duration in every cycle, its energy cost is proportional to the frequency of the cycles. Existing work has focused on query processing in globally synchronized WSN, where all sensors have the same frequency. This leads to waste of battery power for applications that entail different accuracy of measurements (depending on the sensor location), or environments where sensor readings have large variability. To overcome this problem, we propose LS (for local synchronization), a novel framework that permits sensors to have different frequencies. For instance, in a factory setting, temperature sensors in engine rooms, or other areas susceptible to fire, must sample much more frequently than sensors in warehouses. In other cases, the different frequencies may be imposed by the variability of measurements, e.g., a sensor that has stable readings for long periods should turn on less often than another whose readings change with a high rate.

Let the sampling frequency $f_{i}$ of sensor node $n_{i}$ be the minimum frequency by which $n_{i}$ should turn on in order to take measurements. Given $f_{i}$ , the goal of LS is to determine a network frequency $F_{i}$ of each sensor $n_{i}$ so that: (i) $F_{i}$ is at least as high as $f_{i}$ in order to satisfy the accuracy requirements, (ii) $n_{i}$ is active when it needs to forward messages from other sensors to the base station, and (iii) the sum of network frequencies for all sensors in the WSN is minimized. Fig. 1a shows an example subtree of a WSN containing three sensors $n_{1} - n_{3}$ and their sampling frequencies $f_{1} - f_{3}$ . Sensor $n_{1}$ is in the path of $n_{2}$ and $n_{3}$ ; i.e., it must forward messages from these sensors to the base station, implying that $n_{1}$ should be active whenever $n_{2}$ and $n_{3}$ are active. Fig. 1b and Fig. 1c illustrate two solutions towards this. In Fig. 1b, the network frequency $F_{2}$ of $n_{2}$ increases with respect to its sampling frequency ( $\Delta_2 = F_2 - f_2 = 1$ ), achieving synchronization of $n_{1}$ and $n_{2}$ ( $n_{1}$ and $n_{3}$ are already synchronized). Consequently, $n_{2}$ can sample with higher frequency (3 instead of 2) since its energy consumption is dominated by the radio. In Fig. 1c, the network frequencies $F_{1}$ and $F_{3}$ become 4, whereas $F_{2} = f_{2} = 2$ (i.e., $n_{2}$ wakes up once for every two cycles of $n_{1}$ and $n_{3}$ ). The first solution is better because the total increase ( $\Sigma \Delta_i$ ) of the network frequency compared to the sampling frequency is smaller (1 versus 2). Since the sampling frequencies are fixed and given, minimizing $\Sigma\Delta_{i}$ is equivalent to minimizing the total network frequencies.

![](images/2dcde6e3c59a61baf33d86cb99d0dbc0fed4a914e3fd880eb082aeb755fc265a.jpg)



(a) Sampling frequencies

![](images/9b4a0691bdf0957b05a9abac2d1470d4c2a0158c1aa22f77bf4ec14183c11bdc.jpg)



(b) Optimal network frequencies

![](images/3c51ce7cd9ec85daf4d5d52fb3a8cbcd10570cb0703e0c701e1b571633fd1a93.jpg)



(c) Suboptimal network frequencies   
Fig. 1 Subtree with three sensor nodes

Searching for the optimal network frequencies in a WSN is a challenging task, for two reasons. First, there is an infinite search space for the network frequency $F_{i}$ of a node $n_{i}$ , which can be any real number satisfying $F_{i} \geq f_{i}$ so that $n_{i}$ is synchronized with the sensors directly connected to it. Second, locally optimal solutions do not necessarily lead to globally optimal ones. Fig. 2a extends the subtree of Fig. 1a by adding two more sensors $n_{4}$ and $n_{5}$ , with $f_{4}=2$ and $f_{5}=4$ . Fig. 2b expands the solution of Fig. 1b to this setting. Given that $F_{1}=3$ , the best values for the network frequencies of $n_{4}$ and $n_{5}$ are $F_{4}=F_{5}=6$ (i.e., a multiple of $F_{1}=3$ ), yielding $\Sigma\Delta_{i}=7$ ( $\Delta_{2}+\Delta_{4}+\Delta_{5}$ ). On the other hand, by expanding the solution of Fig. 1c, we obtain the network frequencies of Fig. 2c, which are minimal ( $\Sigma\Delta_{i}=4$ ) for this setting.

![](images/b934b63a88d89074575a03709a9543c00c36ce575120ba95b60e8c95d804ae3b.jpg)



(a) Sampling frequencies

![](images/a7c57ff8b644918a086ed28ff50a5834815f486cd07421826aeb65d38cad8479.jpg)



(b) Suboptimal network frequencies

![](images/e60bd1ed8ac347e7a1e9f9a5dab43b334909a4e794759c3158bfb4843cd4f6b4.jpg)



(c) Optimal network frequencies   
Fig. 2 Subtree with five sensor nodes

The problem is more complex when the tree topology is not given, but it has to be computed so that it minimizes $\Sigma\Delta_{i}$ . To our knowledge, the only previous work [11] on locally synchronized WSN requires proxies. On the other hand, LS achieves energy-efficient local synchronization without additional hardware. Specifically, (i) given a tree topology, we compute the optimal network frequencies through a polynomial-time dynamic programming algorithm; (ii) we employ effective heuristics to obtain a high-quality tree topology, if this is not fixed in advance. Extensive experiments demonstrate that LS leads to substantial energy savings compared to the globally synchronized framework.

The rest of the paper is organized as follows. Section II surveys related work. Section III formally defines two key tasks in local synchronization: the computation of the optimal network frequencies and the tree topology. Section IV and V provides efficient algorithms for the above tasks, respectively. Section VI examines the effectiveness of the proposed algorithms using real and synthetic WSN data. Section VII concludes the paper.

# II. RELATED WORK

Section II-A overviews data transmission in WSN. Section II-B surveys WSN query processing methods that minimize energy consumption.

# A. Data Transmission in a WSN

Due to their limited radio range, most sensors in the WSN cannot transmit directly to the base station, but must communicate with the latter through other sensors. These connections are represented by a connectivity graph G where: (i) every node $n_{i} \in G$ corresponds to a sensor (we use the terms sensor and node interchangeably), and (ii) an edge $(n_{i}, n_{j}) \in G$ denotes that sensors $n_{i}, n_{j}$ are within the radio range of each other $^{2}$ . Fig. 3a shows a graph consisting of five sensors $n_{1}$ to $n_{5}$ , and a base station $n_{0}; n_{1}$ and $n_{2}$ can communicate directly with the base station $n_{0}$ . On the other hand, $n_{3}, n_{4}$ and $n_{5}$ must relay their messages through $n_{1}$ and $n_{2}$ . Since there are multiple choices for $n_{3}-n_{5}$ to reach the base station, the WSN must select a routing scheme that determines the routing path for each message.

![](images/6be1b4ccf39a2713671cbcca217310439ffa0eac3bf156ed9e8a0dfc24a6431d.jpg)



(a) Connectivity graph

![](images/281ea0173327fe38ff5b58f025b1713771ee98b2d46ed959e840073a6a4e9a45.jpg)



(b) Suboptimal tree

![](images/1af102a13ee725548e3b5dfd642f8fcd827f3a1dcada288af5b9564128ebfba1.jpg)



(c) Optimal tree   
Fig. 3 Tree topologies for WSN

A large class of routing schemes organizes sensors in tree topologies [13]. Specifically, a spanning tree is built from the connectivity graph, with the base station acting as the root. Most approaches only consider min-hop trees, in order to minimize packet losses [8]. A spanning tree $T \subseteq G$ is min-hop, if and only if the number of edges between every node $n_{i}$ and $n_{0}$ is the minimum among all possible paths in G. For example, the tree in Fig. 3b is min-hop, whereas that in Fig. 3c, is not because $n_{5}$ needs 3 hops to reach $n_{0}$ and there is a shorter path $n_{5}-n_{2}-n_{0}$ in G. In multi-path routing schemes [2][17], a message may arrive at the base station through several paths. In the example of Fig. 3a, a data packet from $n_{4}$ may be transmitted to both $n_{1}$ and $n_{2}$ . Compared with routing trees, multi-path schemes are more robust, at the cost of higher energy consumption and duplicate packets received by the base station. Manjhi et al. [15] propose Tributaries-and-Deltas, combining tree and multi-path routing.

In our work we consider tree topologies. However, in our setting, conventional minimum spanning tree algorithms (i.e., Prim's and Kruskal's) do not necessarily minimize the network frequency. Fig. 3b illustrates a counter-example using Prim's algorithm that starts with a single node and keeps adding the edge with the minimum cost, which is defined as the $\Delta_{i}$ incurred in the path from the new node to the sink. We begin with the base station $n_0$ and insert all edges that connect it with nodes $(n_{1}, n_{2})$ within its range. Assuming that $n_{0}$ is always on, these edges have zero cost. Then, $n_{3}$ is appended as a child of $n_{1}$ also with zero cost. Subsequently, the algorithm adds node $n_{5}$ , which increases the frequency of $n_{2}$ to 2 ( $\Delta_{2}=1$ ), and finally $n_{4}$ with cost $\Delta_{1}=2$ . The overhead of this tree measured by $\Sigma\Delta_{i}$ is 3. On the other hand, the optimal spanning tree in Fig. 3c has cost 2. The complication is due to the fact that edge weights are not constant, but keep changing according to the nodes already inserted in the tree.

# B. Query Processing in WSN

WSN query processing techniques can be classified into three categories, depending on their restrictions on the sensors' sampling and network frequencies. Methods (e.g., [3], [19], [20], [22]) in the first category assume that all sensors have the same sampling frequency $f$ . The second class consists of techniques (e.g., [12], [13]) that allow different sensors to have different sampling rates, but require that they use the same network frequency $F = \max \{f_i \mid \forall n_i\}$ . Finally, the methods of [11] provide flexibility on frequency assignment using additional base-station-like devices called proxies that form the backbone of the WSN. Specifically, (i) each sensor is assigned to one proxy; (ii) all the sensors assigned to the same proxy have the same frequency; and (iii) sensors assigned to different proxies may have different frequencies. The use of proxies, however, limits the applicability of [11], since they increase the financial costs of the WSN system, as well as the difficulty for its deployment.

Besides the above, the network community has proposed Low Power Listening (LPL) [7], a low-level protocol for unsynchronized WSNs that allows sensors to have arbitrary working cycles. Unlike synchronized WSNs, in LPL a sensor $n_{i}$ may be asleep when another node $n_{j}$ needs it to forward a message. When this happens, $n_{j}$ postpones the message, and keeps probing $n_{i}$ by continuously sending preamble signals, until $n_{i}$ wakes up and responds. The two sensors then perform the delayed data transmissions. Due to such delays, LPL may not be suitable for applications with strict responsiveness requirements. Furthermore, the sender of the preamble signals (i.e., $n_{j}$ ) must stay active for long periods, which drains up its battery power. The above problems amplify as the height of the routing tree increases. In contrast, the proposed methods do not incur any result delays or prolonged transmissions of control signals.

# III. PROBLEM DEFINITION

Let $f_{i}$ be the sampling frequency of sensor node $n_{i}; f_{i}$ is a real number determined by the application requirements on accuracy, or the variability of measurements. The proposed LS (local synchronization) assigns to each $n_{i}$ an individual network frequency $F_{i}$ , rather than a global one. In practice, since the work cycle of a sensor must be sufficiently long to complete the necessary sensing, computation and communication tasks, its network frequency must not exceed a constant $F_{max}$ . Let N be the total number of sensors excluding the base station. Our goal is to minimize the objective function $\Phi = \sum_{i=1}^{N} F_{i}$ , referred to as the cost of the WSN. This cost determines the total time that sensors are active, and therefore, it dominates the overall energy consumption. The proposed methods can be easily extended to other aggregates such as maximum and weighted sum. We assume that the WSN uses a tree topology T, which guides the routing of messages between sensors. Table I summarizes frequent symbols.

TABLE I
SUMMARY OF NOTATIONS 

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $G, T$ </td><td>WSN connectivity graph and routing tree</td></tr><tr><td> $N$ </td><td>Number of sensors in the WSN</td></tr><tr><td> $\Phi$ </td><td>Cost of the WSN</td></tr><tr><td> $n_i$ </td><td> $i$ -th sensor (if  $1 \leq i \leq N$ ), or the base station (if  $i=0$ )</td></tr><tr><td> $f_i, F_i$ </td><td>Sampling and network frequency of  $n_i$ </td></tr><tr><td> $F_i^{LB}$ </td><td>Lower bound of  $F_i$  defined in Lemma 2</td></tr><tr><td> $F_{max}$ </td><td>Maximum possible network frequency</td></tr><tr><td> $T_i$ </td><td>Subtree of  $T$  rooted at  $n_i$ </td></tr><tr><td> $\Phi_i^{F_i}$ </td><td>Minimum cost of subtree  $T_i$  for a given  $F_i$ </td></tr></table>

Each sensor must be able to communicate with the base station, in order to report its measurements and / or in-network computation results. To model this, we first introduce the concept of local synchronization between two directly connected sensors.

Definition 1 (Local Synchronization): Given a routing tree T, an internal node $n_{i}$ , and its child $n_{j}$ , $n_{i}$ and $n_{j}$ are locally synchronized (or simply synchronized when the context is clear), if and only if (i) $n_{i}$ and $n_{j}$ start one of their respective cycles at the same time, and (ii) there exists a positive integer k such that $F_{i}=k\cdot F_{j}$ .

Intuitively, when a node $n_{i}$ is synchronized with its child $n_{j}$ , $n_{i}$ is able to process and / or forward every message from $n_{j}$ on time. Among the two conditions in the Definition 1, (i) is a low-level networking issue, e.g., the clocks of the two sensors need to be synchronized $^{3}$ , whereas (ii) restricts the sensors' network frequencies in LS query processing. Hence, in the following we assume that (i) is always satisfied. We next model our main constraint.

Lemma 1: Every sensor is able to communicate with the base station $n_{0}$ in each cycle, if and only if every pair of parent-child nodes in T are locally synchronized.

Based on whether T is given, we distinguish two different versions of the problem. The first, referred to as Problem 1, takes T as an input (e.g., determined by an existing algorithm based on link quality considerations [6]), and computes the network frequencies of the sensors that minimize $\Phi$ . In the second version (Problem 2), T is unknown; instead, given the WSN connectivity graph G, LS selects both the optimal topology $T \subseteq G$ and the network frequencies to minimize $\Phi$ . Compared with Problem 1, the additional flexibility on T may lead to further reduction of $\Phi$ , at the expense of an enlarged search space. Formally, we state the above two problems as follows.

Problem 1: Given a routing tree T and the sampling frequency $f_{i}$ of each node $n_{i}$ , compute the network frequency $F_{i}$ of each $n_{i}$ so that (i) $F_{max} \geq F_{i} \geq f_{i}$ , (ii) every pair of parent-child sensors in T are locally synchronized and (iii) $\Phi = \sum_{i=1}^{N} F_{i}$ is minimized.

Problem 2: Given the connectivity graph G and the sampling frequency $f_{i}$ of each node $n_{i}$ , find the best routing tree $T \subseteq G$ that minimizes $\Phi = \sum_{i=1}^{N} F_{i}$ , where the network frequency $F_{i}$ of each sensor $n_{i}$ is computed according to Problem 1.

Unfortunately, we have the following negative result.

Theorem 1: Problem 2 is NP-hard.

Proof: (by reduction to set cover) Given an instance of the set cover problem that involves a set E of elements and another S of subsets, construct a corresponding connectivity graph G as follows. G contains the base station $n_{0}$ , as well as two layers of sensors. For each subset $s \in S$ (resp. element $e \in E$ ) in the set cover instance, we create a first-layer (resp. second-layer) node in G. Furthermore, whenever a subset s contains an element e in the set cover instance, we add an edge connecting $n_{s}$ and $n_{e}$ in G, where $n_{s}$ and $n_{e}$ are the corresponding nodes of s and e, respectively. Additionally, there is an edge in G between each node on the first layer and the base station $n_{0}$ . The sampling frequency of every first-layer (resp. second-layer) node is 1 (resp. 2). Then, we solve Problem 2 with the above G to obtain the optimal routing tree T. The set of first-layer nodes in T that are parent to at least one second-layer node correspond to the optimal solution of the set cover instance. Therefore, Problem 2 is at least as hard as set cover. Moreover, first-layer (resp. second-layer) nodes always require 1 (resp. 2) hops to the reach the base station in any spanning tree of G. Therefore, the routing tree $T \subseteq G$ is always min-hop, meaning that Problem 2 is still as hard as set cover under the min-hop limitation.

In the following, we describe solutions to both problems. In addition, we discuss their extensions to the case when the routing tree (in Problem 1) or the connectivity graph (in Problem 2) changes over time.

# IV. FINDING NETWORK FREQUENCIES

This section focuses on Problem 1, i.e., optimal network frequency computation with a given routing tree T. Section IV-A lays down the theoretical foundation of the proposed solution. Section IV-B describes an efficient dynamic programming algorithm, and analyses its space and time complexity. Section IV-C provides further optimizations.

# A. Theoretical Foundation

We first investigate the range of feasible values for the network frequency $F_{i}$ of a node $n_{i}$ . Apart from $f_{i}$ , there is a tighter lower bound for $F_{i}$ , as follows.

Lemma 2: Given a node $n_i$ and the subtree $T_i \subseteq T$ rooted at $n_i$ , a lower bound for the network frequency $F_i$ of $n_i$ is

$$
F _ {i} ^ {L B} = \max \left\{f _ {j} \mid \forall n _ {j} \in T _ {i} \right\} \tag {1}
$$

Proof: (by induction) For any node $n_{j} \in T_{i}$ , clearly $F_{j} \geq f_{j}$ according to the problem definition. Suppose that a node $n_{x}$ is along the path from $n_{j}$ to $n_{i}$ whose network frequency $F_{x}$ satisfies that $F_{x} \geq f_{j}$ . Let $n_{y}$ be the parent node of $n_{x}$ . Since $n_{x}$ and $n_{y}$ are locally synchronized, we have $F_{y} \geq F_{x} \geq f_{j}$ . By induction, $F_{i} \geq f_{j}$ .

For instance, in Fig. 2a, the network frequency $F_{4}$ of $n_{4}$ must be no smaller than $F_{i}^{LB} = \max \{f_{1}, f_{2}, f_{3}, f_{4}, f_{5}\} = 4$ . Observe that $f_{4} = 2 < F_{i}^{LB}$ ; consequently, $f_{4}$ in our example does not have any impact on the choice of $F_{4}$ . To avoid complicated notations, in the rest of Section IV-A we assume that for each sensor $n_{i}$ , $f_{i} = F_{i}^{LB}$ ; whenever this is not the case, $F_{i}^{LB}$ is used in place of $f_{i}$ .

However, besides $F_{max}$ , there is no obvious upper bound for $F_{i}$ . Fig. 4a shows an example subtree rooted at sensor $n_{1}$ , which has two children $n_{2}$ and $n_{3}$ . The sampling frequencies are $f_{1}=13$ , $f_{2}=5$ , and $f_{3}=11$ , respectively. Suppose that $n_{2}$ (resp. $n_{3}$ ) have $Cl_{2}$ (resp. $Cl_{3}$ ) child nodes, which all have identical sampling frequencies to their respective parent. The marginal cost of increasing $F_{2}$ (resp. $F_{3}$ ) is then multiplied by $Cl_{2}+1$ (resp. $Cl_{3}+1$ ), as every child of $n_{2}/n_{3}$ must also increase their network frequency by the same amount to synchronize with their respective parent. Fig. 4b lists several values for $F_{1}$ and the corresponding $F_{2}$ and $F_{3}$ that minimizes the overall cost of $T_{1}$ , while satisfying the synchronization requirements. The best $F_{1}$ depends on $Cl_{2}$ and $Cl_{3}$ : when both $n_{2}$ and $n_{3}$ have numerous (e.g., >50) children, the best $F_{1}$ is 55, which in our example is a common multiple of both $f_{2}$ and $f_{3}$ , and thus, minimizes the cost of the subtrees $T_{2}$ and $T_{3}$ . Observe that this is far larger than either one of $f_{1}-f_{3}$ . In general, $f_{2}$ and $f_{3}$ can be non-integer values (e.g., 3.1 and 9.7), in which case the best $F_{1}$ may exceed even the product of $f_{2}$ and $f_{3}$ , depending on the number of children attached to $n_{2}$ and $n_{3}$ .

![](images/23281ea12b256163642010c1b966fc70cd844ae90e1ead5b77c187a848951773.jpg)



(a) Subtree $T_{I}$

<table><tr><td> $F_1$ </td><td> $F_2$ </td><td> $F_3$ </td></tr><tr><td>13</td><td>6.5</td><td>13</td></tr><tr><td>14</td><td>7</td><td>14</td></tr><tr><td>15</td><td>5</td><td>15</td></tr><tr><td>16</td><td>16/3</td><td>16</td></tr><tr><td>20</td><td>5</td><td>20</td></tr><tr><td>21</td><td>5.25</td><td>21</td></tr><tr><td>22</td><td>5.5</td><td>11</td></tr><tr><td>55</td><td>5</td><td>11</td></tr></table>

(b) Network frequencies   
Fig. 4 Example of choosing network frequencies

The above example also demonstrates that there is an infinite search space for a network frequency value $(F_{l})$ , rendering even a brute-force solution rather complicated. We tackle the problem using a top-down approach. Two key issues are (i) how to determine the network frequencies of top-level nodes that are directly connected to the base station, and (ii) given the network frequency $F_{i}$ of an internal node $n_{i}$ , how to choose the network frequencies of its children. We first focus on (ii). In particular, consider a child $n_{j}$ of $n_{i}$ ; in order to synchronize $n_{i}$ and $n_{j}$ , their network frequencies must satisfy that $F_{i}=k\cdot F_{j}$ for a positive integer k, according to Definition 1.

Meanwhile, since $F_{j} \geq f_{j}$ , we have $k \leq \lfloor F_{i} / f_{j} \rfloor$ . Hence, there is a finite number of possible $F_{j}$ 's.

Lemma 3: Let $n_i$ be an internal node of $T$ , and $n_j$ be a child of $n_i$ . Given the network frequency $F_i$ of $n_i$ , the network frequency $F_j$ must take one of the following values

$$
F _ {j} \in \left\{F _ {i} / k \mid k = 1, 2, 3,..., \left\lfloor F _ {i} / f _ {j} \right\rfloor \right\} \tag {2}
$$

For example, in Fig. 4, when $F_{1}$ is set to 13, according to Lemma 3, there are two possible values (13 and 13/2=6.5) for $F_{2}$ , and only one (13) for $F_{3}$ . The question now is how to select the best $F_{j}$ for the child $n_{j}$ among the above possibilities. Intuitively, since $F_{i}$ is already given, the choice of $F_{j}$ only affects the descendants of $n_{j}$ . Accordingly, the best $F_{j}$ is the one that minimizes the subtree $T_{j}$ rooted at $n_{j}$ .

Lemma 4: Given a node $n_i$ , suppose that its network frequency $F_i$ is already determined. Let $\Phi_i^{F_i}$ be the minimum cost of subtree $T_i \subseteq T$ rooted $n_i$ with respect to $F_i$ . Then, $\Phi_i^{F_i}$ can be computed recursively as follows:

$$
\Phi_ {i} ^ {F _ {i}} = F _ {i} + \sum_ {\text { child   } n _ {j} \text {   of   } n _ {i}} \min \left\{\Phi_ {j} ^ {F _ {i} / k} \left| k = 1, 2,... \left\lfloor F _ {i} / f _ {j} \right\rfloor \right. \right\} \tag {3}
$$

where $\Phi_{j}^{F_{i}/k}$ is the minimum cost of subtree $T_{j}$ given $F_{j}=F_{i}/k$ .

Proof: Consider an arbitrary child node $n_{j}$ of $n_{i}$ . According to the definition of Problem 1, besides $f_{j}$ , the value of $F_{j}$ only affects the network frequencies of $n_{j}$ 's parent (i.e., $F_{i}$ of $n_{i}$ ) and children (and, recursively, the descendants of $n_{j}$ ). Since $F_{i}$ is fixed and given, the choice of $F_{j}$ has impact only on the cost of the subtree $T_{j}$ . Therefore, the best $F_{j}$ should minimize the cost of $T_{j}$ , which, combined with Lemma 2, leads to Equation (3).

As a special case, when $n_{i}$ is a leaf node, $\Phi_{i}^{F_{i}}$ is simply $F_{i}$ . Based on Lemma 4, once $F_{i}$ is determined, it is straightforward to compute $\Phi_{i}^{F_{i}}$ , as well as the best network frequencies of all nodes in the subtree $T_{i}$ , through exhaustive search. For instance, in Fig. 2, given $F_{4}=6$ , $F_{5}$ must be 6, since $f_{5}=4>6/2$ . $F_{1}$ can be either 3 or 6. In the former case, $F_{2}=F_{3}=3$ , hence $\Phi_{1}^{3}=3+3+3=9$ . In case that $F_{1}=6$ , $F_{2}$ can be 2, 3, or 6, $F_{3}$ can be 3 or 6, and the minimum possible cost for $T_{1}$ is $\Phi_{1}^{6}=6+2+3=11$ . Since $\Phi_{1}^{3}<\Phi_{1}^{6}$ , the best value for $F_{1}$ is 3, and, thus, $\Phi_{4}^{6}=6+\Phi_{1}^{3}+6=21$ .

However, the number of possible values for a network frequency increases exponentially with the depth of the node in the tree topology. To reduce the number of potential values, we now describe our most important theoretical result, which entails the recursive equation (3), only if $F_{i}$ is a regular network frequency, defined as follows.

Definition 2 (Regular Network Frequency): A network frequency $F_{i}$ is regular, if and only if either (i) $F_{i} = f_{i}$ or (ii) there exists a node $n_j \neq n_i$ in the subtree $T_{i}$ rooted at $n_i$ such that $F_{i} = k \cdot f_{j}$ for a positive integer $k$ .

For instance, among the values of $F_{1}$ listed in Fig. 4b, only 13, 15, 20, 22 and 55 are regular ones (shown in grey). In general, $n_{1}$ 's regular network frequencies are $f_{1} = 13$ and multiples of $f_{2} = 5$ (e.g., 15, 20, 55), or $f_{3} = 11$ (22, 55), since all children of $n_2$ and $n_3$ have the same sampling frequencies as their respective parent.

Theorem 2: Given an internal node $n_i$ and a network frequency $F_i$ , let $F'_i$ be the highest regular network frequency for $n_i$ satisfying $F'_i \leq F_i$ . Then:

$$
\Phi_ {i} ^ {F _ {i}} = \Phi_ {i} ^ {F _ {i} ^ {\prime}} \cdot F _ {i} / F _ {i} ^ {\prime} \tag {4}
$$

Furthermore, suppose that when $F_{i}^{\prime}$ is assigned to $n_i$ , the best network frequency for each node $n_j \in T_i$ is $F_{j}^{\prime}$ . Then, when $F_{i}$ is assigned to $n_i$ , the optimal network frequencies for the nodes in $T_{i}$ are:

$$
F _ {j} = F _ {j} ^ {\prime} \cdot F _ {i} / F _ {i} ^ {\prime}, \forall n _ {j} \in T _ {i} \tag {5}
$$

Proof: We first prove that Equation (5) gives a feasible solution for $T_i$ that leads to a subtree cost of $\Phi_i^{F_i}$ given in Equation (4). Because when $F_i'$ is assigned to $n_i$ , $F_j'$ is the optimal network frequency of any node $n_j$ in $T_i$ , it must also be a feasible network frequency for $n_i$ . Hence, $F_j \geq F_j' \geq f_j$ . Meanwhile, consider any internal node $n_x \in T_i$ and one of its children $n_y \in T_i$ . Let $F_x'$ and $F_y'$ be the optimal network frequencies of $n_x$ and $n_y$ , respectively, when $F_i'$ is assigned to $n_i$ . Clearly, $F_x'$ is a multiple of $F_y'$ . Let integer $k_{xy} = F_x' / F_y'$ . According to Equation (5), $F_x / F_y = F_x' / F_y' = k_{xy}$ . Hence, $F_x$ is a multiple of $F_y$ , which enables the local synchronization of $n_x$ and $n_y$ . Additionally, we have

$$
\Phi_ {i} ^ {F _ {i}} = \sum_ {n _ {j} \in T _ {i}} F _ {j} = \sum_ {n _ {j} \in T _ {i}} \frac {F _ {j} ^ {\prime} \cdot F _ {i}}{F _ {i} ^ {\prime}} = \frac {F _ {i}}{F _ {i} ^ {\prime}} \cdot \sum_ {n _ {j} \in T _ {i}} F _ {j} ^ {\prime} = \frac {\Phi_ {i} ^ {F _ {i} ^ {\prime}} \cdot F _ {i}}{F _ {i} ^ {\prime}} \tag {6}
$$

Next we prove by induction that $\Phi_{i}^{F_{i}}$ given in Equation (4) is indeed the minimum cost when $F_{i}$ is assigned to $n_{i}$ . In the base case, $n_{i}$ is a leaf node in T. The theorem holds trivially, since $\Phi_{i}^{F_{i}}=F_{i}$ , and $\Phi_{i}^{F_{i}^{\prime}}=F_{i}^{\prime}$ . In the induction step, suppose that each child node $n_{j}$ of $n_{i}$ satisfies the theorem. Specifically, given an arbitrary node $n_{x}$ , let the function $CR_{x}(F_{x})$ that returns the highest regular network frequency for $n_{x}$ satisfying that $CR_{x}(F_{x})\leq F_{x}$ . As a special case, $CR_{i}(F_{i})=F_{i}^{\prime}$ . The induction assumption is stated as follows.

$$
\forall \text { child } n _ {j} \text { of } n _ {i}, \forall F _ {j}, \frac {\Phi_ {j} ^ {F _ {j}}}{F _ {j}} = \frac {\Phi_ {j} ^ {C R _ {j} (F _ {j})}}{C R (F _ {j})} \tag {7}
$$

According to Lemma 2, when $F_{i}$ is assigned to $n_{i}$ , $F_{j}$ must be $F_{i} / k$ for a positive integer $k \trianglelefteq F_{i} / f_{j}$ . Similarly, when $F_{i}'$ is assigned to $n_{i}$ , $F_{j}$ must be $F_{i}' / k$ for a positive integer $k \trianglelefteq F_{i} / f_{j}$ . We now prove that $\lfloor F_{i} / f_{j} \rfloor = \lfloor F_{i}' / f_{j} \rfloor$ by contradiction. Suppose that $\lfloor F_{i} / f_{j} \rfloor \neq \lfloor F_{i}' / f_{j} \rfloor$ . Then, since $F_{i}' \leq F_{i}$ , we have $\lfloor F_{i}' / f_{j} \rfloor < \lfloor F_{i} / f_{j} \rfloor$ , and, thus, $F_{i}' \trianglelefteq F_{i} / f_{j} \rfloor : f_{j} \leq F_{i}$ . However, $\lfloor F_{i} / f_{j} \rfloor : f_{j}$ a regular frequency for $n_{i}$ , as it is an integer multiple of $f_{j}$ . This contradicts with the fact that $F_{i}'$ is the largest regular network frequency for $n_{i}$ satisfying $F_{i}' \leq F_{i}$ .

Substituting $F_{j}$ with $F_{i} / k$ and $F_{i}' / k$ in Equation (7), respectively, we obtain

$$
\forall k = 1, 2, \dots \left\lfloor F _ {i} / f _ {j} \right\rfloor , \frac {\Phi_ {j} ^ {F _ {i} / k}}{F _ {i} / k} = \frac {\Phi_ {j} ^ {C R _ {j} (F _ {i} / k)}}{C R _ {j} (F _ {i} / k)} \tag {8}
$$

$$
\forall k = 1, 2, \dots \left\lfloor F _ {i} / f _ {j} \right\rfloor , \frac {\Phi_ {j} ^ {F _ {i} ^ {\prime} / k}}{F _ {i} ^ {\prime} / k} = \frac {\Phi_ {j} ^ {C R _ {j} (F _ {i} ^ {\prime} / k)}}{C R _ {j} (F ^ {\prime} / k)} \tag {9}
$$

Next we prove $CR_{j}(F_{i}/k)=CR_{j}(F'_{i}/k)$ by contradiction. Suppose that $CR_{j}(F_{i}/k)\neq CR_{j}(F'_{i}/k)$ . Because $F'_{i}<F_{i}$ , $CR_{j}(F'_{i}/k)<CR_{j}(F_{i}/k)$ . Hence, $F'_{i}<CR_{j}(F_{i}/k)\cdot k\leq F_{i}$ . Since $CR_{j}(F_{i}/k)$ is a multiple of $f_{x}$ of a node $n_{x}$ in $T_{j}\subseteq T_{i}$ , and k is a positive integer, $CR_{j}(F_{i}/k)\cdot k$ is also a multiple of $f_{x}$ , meaning that $CR_{j}(F_{i}/k)\cdot k$ is a regular network frequency for $n_{i}$ that is closer to $F_{i}$ than $F'_{i}$ , which contradicts with the definition of $F'_{i}$ . Therefore, $CR_{j}(F_{i}/k)=CR_{j}(F'_{i}/k)$ , and, consequently, the right hand side of Equation (8) equals that of Equation (9). Their respective left hand side must be equal as well:

$$
\frac {\Phi_ {j} ^ {F _ {i} / k}}{F _ {i}} = \frac {\Phi_ {j} ^ {F _ {i} ^ {\prime} / k}}{F _ {i} ^ {\prime}} \tag {10}
$$

Let $k^{*} \leq \lfloor F_{i}/f_{j} \rfloor$ be the positive integer satisfying:

$$
\forall k = 1, 2, \dots \left\lfloor F _ {i} / f _ {j} \right\rfloor , \Phi_ {j} ^ {F _ {i} ^ {\prime} / k ^ {*}} \leq \Phi_ {j} ^ {F _ {i} ^ {\prime} / k} \tag {11}
$$

According to Lemma 3 and the fact that $\lfloor F_i / f_j\rfloor = \lfloor F_i' / f_j\rfloor$ , we have

$$
\Phi_ {i} ^ {F _ {i} ^ {\prime}} = F _ {i} ^ {\prime} + \sum_ {\text { child } n _ {j}} \Phi_ {j} ^ {F _ {i} ^ {\prime} / k ^ {*}} \tag {12}
$$

Multiplying both sides of Inequality (11) by $F_{i} / F_{i}'$ , we obtain

$$
\forall k = 1, 2, \dots \left\lfloor F _ {i} / f _ {j} \right\rfloor , \frac {\Phi_ {j} ^ {F _ {i} ^ {\prime} / k ^ {*}} \cdot F _ {i}}{F _ {i} ^ {\prime}} \leq \frac {\Phi_ {j} ^ {F _ {i} ^ {\prime} / k} \cdot F _ {i}}{F _ {i} ^ {\prime}} \tag {13}
$$

Combining Equation (10) and Inequality (13), we obtain

$$
\forall k = 1, 2, \dots \left\lfloor F _ {i} / f _ {j} \right\rfloor , \Phi_ {j} ^ {F _ {i} / k ^ {*}} \leq \Phi_ {j} ^ {F _ {i} / k} \tag {14}
$$

Therefore, according to Lemma 3, we have

$$
\begin{array}{l} \Phi_ {i} ^ {F _ {i}} = F _ {i} + \sum_ {\text { child } n _ {i}} \Phi_ {j} ^ {F _ {i} / k ^ {*}} \\ = F _ {i} + \sum_ {\text { child } n _ {j}} \frac {\Phi_ {j} ^ {F _ {i} ^ {\prime} / k ^ {*}} \cdot F _ {i}}{F _ {i} ^ {\prime}} \\ = \frac {F _ {i}}{F _ {i} ^ {\prime}} \left(F _ {i} ^ {\prime} + \sum_ {\text {child} n _ {j}} \Phi_ {j} ^ {F _ {i} ^ {\prime} / k ^ {*}}\right) \tag {15} \\ = \frac {\Phi_ {i} ^ {F ^ {\prime}} \cdot F _ {i}}{F ^ {\prime}} \\ \end{array}
$$

The second line in the above equation is based on Equation (10), whereas the last step is based on Equation (12). Therefore, the theorem also holds for $n_i$ .

In the example of Fig. 4, consider an irregular frequency $F_{1} = 16$ . $F_{1}' = 15$ is the highest regular frequency satisfying $F_{1}' \leq F_{1}$ . According to Fig. 4b, when $F_{1} = 16$ is assigned to $n_{1}$ , the optimal values for $F_{2}$ and $F_{3}$ are $16/3$ and 16 respectively. Meanwhile, when $F_{1}' = 15$ is assigned to $n_{1}$ , the best network frequencies for $n_{2}$ and $n_{3}$ are $F_{2}' = 5$ and $F_{3}' = 15$ respectively. Clearly, $\Phi_{1}^{16} / \Phi_{1}^{15} = F_{2}/F_{2}' = F_{3}/F_{3}' = 16/15$ .

Theorem 2 indicates that $\Phi_{i}^{F_{i}}$ is a piece-wise linear function of $F_{i}$ . Specifically, as $F_{i}$ grows from one regular value to the next one, $\Phi_{i}^{F_{i}}$ increases linearly with $F_{i}$ ; when $F_{i}$ reaches the next regular value, $\Phi_{i}^{F_{i}}$ suddenly drops. Subsequently, $\Phi_{i}^{F_{i}}$ again increases linearly with $F_{i}$ until the next regular frequency, possibly with a different slope. Fig. 5 plots $\Phi_{I}^{F_{I}}$ against $F_{I}$ in the example of Fig. 4, assuming that $n_{2}$ and $n_{3}$ have 2 and 3 child nodes respectively. Regular frequencies for $n_{I}$ between 13 and 55 are shown on the x-axis. The piece-wise linear pattern, as well as the sudden drops in $\Phi_{I}^{F_{I}}$ at regular values for $F_{I}$ , can be clearly observed in the plot.

![](images/060ae01953e12045d0bbbf7544f6cbeed74dcd4442128a8e9a5160838b2c4e65.jpg)



Fig. 5 Example plot of $\Phi_i^{F_i}$ vs. $F_{i}$

Another consequence of Theorem 2 is that an irregular $F_{i}$ always leads to a higher subtree cost than the corresponding regular value $F_{i}'$ preceding $F_{i}$ . Therefore, for each top-level node $n_{i}$ for which there is no restriction on its network frequency $F_{i}$ , it suffices to consider only its regular values of $F_{i}$ .

Corollary 1: Given a node $n_{i}$ that is directly connected to the base station, the optimal network frequency of $n_{i}$ must be regular.

For a node $n_j$ whose parent is another sensor $n_i$ , its network frequency is restricted to the values described in Lemma 3. Consequently, given a irregular frequency $F_j$ of $n_j$ , the highest regular frequency $F_j'$ preceding $F_j$ may not be able to synchronize with $n_i$ . Hence, the best frequency for $F_j$ can be irregular. For such nodes, the following algorithm utilizes Theorem 2 to reduce the computation of $\Phi_j^{F_j}$ to that of $\Phi_j^{F_j'}$ .

# B. Algorithm

Given the routing tree $T$ and the sampling frequencies $f_{I}, f_{2}, \ldots, f_{N}$ , LS searches for the optimal network frequencies $F_{I}^{*} - F_{N}^{*}$ in two steps. First, it computes the minimum cost $\Phi^{*}$ of the entire WSN and gradually completes a hash table $H$ . Second, guided by $H$ , LS finds the optimal values $F_{I}^{*} - F_{N}^{*}$ that sum up to $\Phi^{*}$ . The hash table $H$ contains entries of the form $\langle n_{i}, F_{i} \rangle \to \Phi_{i}^{F_{i}}$ , where the key is a node $n_{i}$ and a regular frequency $F_{i}$ for $n_{i}$ , and the value $\Phi_{i}^{F_{i}}$ is the minimum cost of the subtree $T_{i}$ rooted at $n_{i}$ , given $F_{i}$ .

The first step involves two functions, namely CTC (short for compute total cost) and CSC (for compute subtree cost). Fig. 6 illustrates CTC. The method initially computes the lower bound $F_{i}^{LB}$ for the network frequency $F_{i}$ of each node $n_i$ (lines 2-4). According to Lemma 2, $F_{i}^{LB}$ is a tighter bound than $f_{i}$ ; whenever $f_{i} < F_{i}^{LB}$ , the latter is used instead (specifically, in Equations (2), (3), and Definition 2). After that, the algorithm examines each top-level node $n_i$ , and computes the minimum cost $\Phi_{i}^{min}$ of the subtree $T_{i}$ rooted at $n_i$ (lines 5-10). In particular, line 7 enumerates all regular values for $F_{i}$ that may possibly lead to the $\Phi_{i}^{min}$ , according to Corollary 1. Line 8 invokes the recursive procedure CSC (described below) to compute $\Phi_{i}^{F_{i}}$ ; the smallest $\Phi_{i}^{F_{i}}$ among all values of $F_{i}$ becomes $\Phi_{i}^{min}$ . Finally, line 10 sums up $\Phi_{i}^{min}$ for all top-level nodes to obtain the minimum overall cost $\Phi^{*}$ .

$CTC(T, f_{I}-f_{N})$ : returns $\Phi^{*}$ //CTC for compute total cost
// Input: T: routing tree, $f_{I}-f_{N}$ : sampling frequencies of the sensors
// Output: $\Phi^{*}$ : optimal cost of the entire WSN
1. Initialize $\Phi^{*}$ to 0, and H to an empty hash table
2. For each node $n_{i} \in T$ 3. Compute $F_{i}^{LB}$ according to Equation (1)
4. If $F_{i}^{LB} > f_{i}$ , use $F_{i}^{LB}$ in place of $f_{i}$ in the rest of the algorithm
5. For each $n_{i}$ that is directly connected to the base station in T
6. Initialize $\Phi_{i}^{min}$ to $+\infty$ 7. For each regular $F_{i}$ 8. Call $\Phi_{i}^{F_{i}} = CSC(T, f_{I}-f_{N}, n_{i}, F_{i}, H)$ 9. If $\Phi_{i}^{F_{i}} < \Phi_{i}^{min}$ , set $\Phi_{i}^{min}$ to $\Phi_{i}^{F_{i}}$ 10. Update $\Phi^{*}$ to $\Phi^{*} + \Phi_{i}^{min}$ 11. Return $\Phi^{*}$   
Fig. 6 Algorithm CTC

Fig. 7 shows CSC, which recursively computes the optimal cost $\Phi_i^{F_i}$ of the subtree $T_i$ rooted at node $n_i$ , given $F_i$ . When $F_i$ is irregular, the algorithm picks the highest regular frequency $F'_i$ satisfying $F'_i \leq F_i$ , calculates $\Phi_i^{F'_i}$ , and applies Theorem 2 to obtain $\Phi_i^{F_i}$ (lines 1-4). On the other hand, when $F_i$ is regular, Lemma 4 is used to compute $\Phi_i^{F_i}$ recursively (lines 6-13). The result is stored in a new entry of the hash table $H$ with key $<n_i, F_i>$ . When the same parameters $n_i, F_i$ are passed to CSC, the latter looks up $H$ for the stored $\Phi_i^{F_i}$ (line 5).   
CSC $(T, f_{I} - f_{N}, n_{i}, F_{i}, H)$ : returns $\Phi_{i}^{F_{i}}$ // CSC for compute subtree cost  
// Input: $T$ : routing tree  
// $f_{I} - f_{N}$ : sampling frequencies of the sensors  
// $n_{i}, F_{i}$ : root node of the subtree $T_{i}$ , and its network frequency  
// $H$ : hash table storing subtree costs  
// Output: $\Phi_{i}^{F_{i}}$ : minimum subtree cost of $T_{i}$ given $F_{i}$ 1. If $F_{i}$ is irregular with respect to $n_{i}$ 2. Let $F'_{i} < F_{i}$ be the highest regular network frequency for $n_{i}$ 3. Call $\Phi_{i}^{F_{i}} = \text{CSC}(T, f_{I} - f_{N}, n_{i}, F'_{i}, H)$ 4. Calculate $\Phi_{i}^{F_{i}}$ according to Equation (4), and return $\Phi_{i}^{F_{i}}$ 5. If $H$ contains an entry with key $< n_{i}, F_{i}>$ and value $\Phi_{i}^{F_{i}}$ , return $\Phi_{i}^{F_{i}}$ 6. If $n_{i}$ is a leaf node, return $F_{i}$ 7. Initialize $\Phi_{i}^{F_{i}}$ to $F_{i}$ 8. For each child $n_{j}$ of $n_{i}$ 9. Initialize $\Phi_{j}^{min}$ to $+\infty$ 10. For each value of $F_{j}$ described in Equation (2)  
11. Call $\Phi_{j}^{F_{j}} = \text{CSC}(T, f_{I} - f_{N}, n_{j}, F_{j}, H)$ 12. If $\Phi_{j}^{F_{j}} < \Phi_{j}^{min}$ , set $\Phi_{j}^{min}$ to $\Phi_{j}^{F_{j}}$ 13. Update $\Phi_{i}^{F_{i}}$ to $\Phi_{i}^{F_{i}} + \Phi_{j}^{min}$ 14. Add a new entry to $H$ with key $< n_{i}, F_{i}>$ and value $\Phi_{i}^{F_{i}}$ 15. Return $\Phi_{i}^{F_{i}}$   
Fig. 7 Algorithm CSC   
Fig. 8 describes the function CNF (short for compute network frequencies), which implements the second step of the

proposed solution, and computes the optimal frequencies top-down. The method starts by examining each top-level node $n_{i}$ , testing regular network frequencies $F_{i}$ of $n_{i}$ (lines 3-7). Since $F_{i}$ is regular, and CTC has called CSC with parameters $n_{i}$ and $F_{i}$ , the hash table H already contains an entry $<n_{i}, F_{i}> \rightarrow \Phi_{i}^{F_{i}}$ . The value of $F_{i}$ that minimizes the subtree cost for $T_{i}$ becomes the optimal frequency $F_{i}^{*}$ of $n_{i}$ . After determining the optimal frequencies for all top-level nodes, the algorithm continues to calculate the frequencies of their descendants. Specifically, given a node $n_{i}$ with known $F_{i}^{*}$ and one of its children $n_{j}$ , CNF enumerates all possible values for $F_{j}$ , and computes the minimum cost for subtree $T_{i}$ . For a regular $F_{j}$ , $\Phi_{j}^{F_{j}}$ is simply retrieved from H. When $F_{j}$ is irregular, $\Phi_{j}^{F_{j}}$ is obtained using Theorem 2 and H. In both cases, there is no need for recursive calls, since the computations have already been performed in CSC, and the results stored in H.

CNF $(T,f_{I} - f_{N})$ : returns $F_{I}^{*} - F_{N}^{*}$ // CNF for compute network frequencies   
// Input: $T$ : routing tree, $f_{I} - f_{N}$ : sampling frequencies of the sensors   
// Output: $F_{I}^{*} - F_{N}^{*}$ : optimal network frequencies of the nodes in $T$ 1. Call $\Phi^{*} = CTC(T,f_{I} - f_{N})$ 2. Let $H$ be the hash table used in CTC   
3. For each node $n_i$ that is directly connected to the base station $n_0$ 4. Initialize $\Phi_i^{min}$ to $+\infty ,F_i^*$ to NULL   
5. For each regular $F_{i}$ 6. Retrieve $\Phi_i^{F_i}$ from $H$ with key $< n_i,F_i>$ 7. If $\Phi_i^{F_i} <   \Phi_i^{min}$ , set $\Phi_i^{min}$ to $\Phi_i^{F_i}$ , and $F_{i}^{*}$ to $F_{i}$ 8. Repeat   
9. For each node $n_j$ satisfying (i) $F_{j}^{*}$ has not been determined and (ii) $F_{i}^{*}$ corresponding to the parent $n_i$ of $n_j$ has been determined   
10. Initialize $\Phi_j^{min}$ to $+\infty ,F_j^*$ to NULL   
11. For each value of $F_{j}$ described in Equation (2)   
12. Compute $\Phi_j^{F_j}$ using $H$ and Theorem 2   
13. If $\Phi_j^{F_j} <   \Phi_j^{min}$ , set $\Phi_j^{min}$ to $\Phi_j^{F_j}$ , and $F_{j}^{*}$ to $F_{j}$ 14. Until all optimal network frequencies are determined   
15. Return $F_{I}^{*} - F_{N}^{*}$   
Fig. 8 Algorithm CNF

Fig. 9 illustrates an example of the above algorithms. Assume that $F_{max} = 100$ according to the application requirements. The sampling frequencies are shown alongside their corresponding nodes. Among them, $f_{3}$ is smaller than the lower bound $F_{3}^{LB}$ given by Lemma 2, which equals the maximum sampling frequency (i.e., $f_{6} = 11$ ) in the subtree rooted at $n_{3}$ . Therefore, in the computation of the optimal network frequencies, the algorithms simply discard the original value $f_{3} = 2$ , and proceed as if $f_{3}$ were $F_{3}^{LB} = 11$ .   
![](images/809b43e20000f0f0d1bf3caa40721507c3292a8b0c24db7c4461ce4a5587ea4e.jpg)



(a) Sampling frequencies

<table><tr><td> $n_i$ </td><td> $F_i$ </td><td> $\Phi_i^{F_i}$ </td></tr><tr><td> $n_2$ </td><td>5</td><td>15</td></tr><tr><td> $n_2$ </td><td>12</td><td>20</td></tr><tr><td> $n_3$ </td><td>11</td><td>22</td></tr><tr><td> $n_l$ </td><td>13</td><td>58.5</td></tr><tr><td> $n_l$ </td><td>15</td><td>60</td></tr><tr><td colspan="3">...</td></tr></table>

(b) Hash table H

<table><tr><td>1</td><td> $CSC(n_1, 13)$ </td></tr><tr><td>2</td><td> $CSC(n_2, 6.5)$ </td></tr><tr><td>3</td><td> $CSC(n_2, 5)$ </td></tr><tr><td>4</td><td> $CSC(n_4, 5)$ </td></tr><tr><td>5</td><td> $CSC(n_5, 5)$ </td></tr><tr><td>6</td><td> $CSC(n_2, 13)$ </td></tr><tr><td>7</td><td> $CSC(n_2, 12)$ </td></tr><tr><td colspan="2">...</td></tr></table>

(c) Calls of CSC   
Fig. 9 Example of network frequency computation

Next we elaborate the computation of the optimal $F_{1}^{*}-F_{5}^{*}$ in the subtree $T_{1}$ rooted at $n_{1}$ . Since $n_{1}$ connects directly to $n_{0}$ , CTC enumerates all its regular frequencies, which include (i) $f_{1}=13$ and (ii) all multiples of $f_{2}=5$ , $f_{4}=f_{5}=4$ , and $F_{3}^{L,B}=f_{6}=11$ below $F_{max}=100$ . Assume that CTC first assigns $F_{1}=13$ , and invokes CSC to compute $\Phi_{l}^{I3}$ . Fig. 9c shows the 7 subsequent calls to CSC, listing only parameters $n_{i}$ and $F_{i}$ since the others remain the same for all invocations of CSC. In the first call $CSC(n_{1},13)$ , the hash table H does not have an entry with key $<n_{1},13>$ ; thus, CSC computes $\Phi_{l}^{I3}$ recursively by identifying the best value for the network frequencies $F_{2}$ and $F_{3}$ of $n_{1}$ 's child nodes $n_{2}$ and $n_{3}$ , given that $F_{1}=13$ . We first focus on $F_{2}$ . According to Lemma 3, there are two possible values for $F_{2}:F_{1}=13$ and $F_{1}/2=6.5$ . Suppose that CSC first calculates $\Phi_{2}^{6.5}$ by recursively calling $CSC(n_{2},F_{2}=6.5)$ . However, 6.5 is not a regular frequency for $n_{2}$ because it is not equal to $f_{2}=5$ , or a multiple of $f_{4}=f_{5}=4$ . Therefore, CSC finds the highest regular frequency $F'_{2}=5$ below 6.5, and calls $CSC(n_{2},5)$ .

To compute $\Phi_2^5$ , which has no corresponding entry in $H$ , CSC must determine the best $F_4$ and $F_5$ given $F_2 = 5$ . According to Lemma 3, there is only one possible value 5 for both $F_4$ and $F_5$ . In the next two steps, CSC calls itself with parameters $(n_4, 5)$ and $(n_5, 5)$ respectively, which return $\Phi_4^5 = \Phi_5^5 = 5$ . With this information, the third call to CSC (i.e., with parameters $n_2$ and 5) returns $\Phi_2^5 = 5 + \Phi_4^5 + \Phi_5^5 = 15$ , after adding a new entry $< n_2, 5 > = 15$ to $H$ . Subsequently, the second call to CSC with parameters $n_2$ and 6.5 then returns $\Phi_2^{6.5} = \Phi_2^5 \cdot 6.5 / 5 = 19.5$ , according to Theorem 2. Next, the first call $CSC(n_1, 13)$ tests the other possible $F_2 = 13$ for $n_2$ by calling $CSC(n_2, 13)$ , which leads to another invocation $CSC(n_2, 12)$ with the highest regular network frequency 12 below 13. The latter eventually returns $\Phi_2^{12} = 20$ , and after $CSC(n_2, 13)$ we have $\Phi_2^{13} = \Phi_2^{12} \cdot 13 / 12 = 65 / 3$ . Because $\Phi_2^{6.5} < \Phi_2^{13}$ , the minimum cost for subtree $T_2$ given $F_1 = 13$ is $\Phi_2^{6.5} = 19.5$ . The first call $CSC(n_1, 13)$ then computes the minimum cost for subtree $T_3$ rooted at $n_3$ , which is 26 when $F_3 = F_6 = 13$ . Accordingly, $\Phi_1^{13} = 13 + 19.5 + 26 = 58.5$ , concluding the computation of $CSC(n_1, 13)$ .

The outer function CTC then computes minimum subtree costs of $T_{1}$ with other regular values of $F_{1}$ , e.g., 15, 16, 20, 22, etc. Finally, CTC establishes that $\Phi_{l}^{I3}=58.5$ is the minimum cost for subtree $T_{1}$ among all values of $F_{1}$ . After the termination of CTC, CNF computes the optimal network frequencies top-down. CNF enumerates all regular values of $F_{1}$ and finds the one with the minimum $\Phi_{l}^{F_{1}}$ using the hash table H. Having determined that $F_{1}^{*}=13$ , CNF continues to calculate $F_{2}^{*}, F_{3}^{*}$ , and subsequently $F_{4}^{*}-F_{6}^{*}$ based on the optimal subtrees stored in H.

Theorem 3: The space and time complexity of the algorithmic framework is $O(N^2 \cdot C)$ and $O(N^2 \cdot C^2)$ , respectively, where $C = \lfloor F_{max} / f_{min} \rfloor$ , and $f_{min} = \min \{f_i | 1 \leq i \leq N\}$ .

Proof: We first prove that algorithm CTC takes $O(N^{2}\cdot C)$ space and $O(N^{2}\cdot C)$ time. Its space consumption is dominated by the storage of the hash table H, which consists of entries of the form $<n_i, F_i>\to\Phi_i^{F_i}$ , where $n_i$ is an arbitrary node, $F_i$ is a regular network frequency for $n_i$ , and $\Phi_i^{F_i}$ is the minimum cost of the subtree $T_i$ rooted at $n_i$ , when $F_i$ is assigned to $n_i$ . According to Definition 2, $F_i$ must be a multiple of the sampling frequency $f_j$ of a node $n_j\in T_i$ . Since $F_i\leq F_{max}$ and $f_j\geq f_{min}$ , the number of possible regular network frequencies for $n_i$ contributed by $n_j$ is upper bounded by $C=\lfloor F_{max}/f_{min}\rfloor$ . Since $n_j$ can be any of the $O(N)$ nodes in $T_i$ , the total number of regular network frequencies for $n_i$ is $O(N\cdot C)$ . Considering that $n_i$ can be any node in the WSN, the number of entries in $H$ is $O(N^2\cdot C)$ .

Regarding time complexity, the dominating factor is the time consumed by subroutine CSC, which computes the optimal subtree cost for a given node $n_{i}$ and its network frequency $F_{i}$ . The cases when $F_{i}$ is irregular, or when H contains an entry with key $<n_{i}, F_{i}>$ take negligible time to handle. Hence, it suffices to count the invocations of CSC with a regular $F_{i}$ and a combination of $<n_{i}, F_{i}>$ not processed before. In each such invocation, CSC recursively calls itself to compute the minimum subtree cost corresponding to each child node $n_{j}$ of $n_{i}$ . Specifically, the algorithm considers all possible network frequencies for $n_{j}$ given $F_{i}$ , which is bounded by C. Let $Cl_{i}$ be the number of the children of $n_{i}$ , CSC finishes in $O(Cl_{i} \cdot C)$ time. Counting all calls to CSC with fresh and regular inputs, the total time complexity is $\sum_{n_{i}} = O(C \cdot Cl_{i} \cdot N \cdot C) = O(N^{2} \cdot C^{2})$ .

Next we focus on CNF. Clearly, its space complexity is also dominated by the storage of H, which is bounded by $O(N^{2}\cdot C)$ as in CTC. Concerning time, after calling CTC, CNF enumerates all possible network frequencies of every node exactly once, which takes $O(N^{2}\cdot C)$ time. Hence, its time complexity is also $O(N^{2}\cdot C^{2})$ .

# C. Discussion

The value of C in Theorem 3 grows with $F_{max}$ . Next we present optimizations to limit the impact of $F_{max}$ , and significantly speed up network frequency computation. In the example of Fig. 9, one feasible solution is to set the network frequency of each sensor in $n_{1}-n_{6}$ to the highest sampling frequency $f_{1}=13$ among the 6 sensors, leading to a total cost of 78 for subtree $T_{1}$ . Clearly, setting $F_{1}>78$ will always result in a higher subtree cost for $T_{1}$ . Furthermore, since each sensor $n_{i}$ must have a network frequency $F_{i}\geq F_{i}^{LB}$ according to Lemma 2, when $F_{1}>43$ , even when $n_{2}-n_{5}$ use their respective minimum possible network frequency, the total cost for $T_{1}$ still exceeds that achieved with the above simple solution (i.e., 78). Therefore, it suffices to examine only regular frequencies for $F_{1}$ not exceeding 43. Note that this is a much tighter bound than $F_{max}=100$ . In addition, after obtaining $\Phi_{l}^{13}=58.5$ , the upper bound for $F_{1}$ can be further tightened to 23.5, since any higher value, plus the minimum possible network frequencies of $n_{2}-n_{5}$ , would result in a subtree cost for $T_{1}$ higher than the current best 58.5.

Based on the above observations, we modify algorithm CTC as follows. In line 7 of Fig. 6, the regular frequencies are enumerated in increasing order. Let $|T_{i}|$ be the number of nodes in $T_i$ ; an upper bound $F_i^{UB}$ for $F_i$ is initialized to $\max \{f_j | n_j \in T_i\} \cdot |T_i| - \sum_{j \not\in i, n_j \in T_i} F_j^{LB}$ , and incrementally maintained as $\Phi_i^{min} - \sum_{j \not\in i, n_j \in T_i} F_j^{LB}$ while the minimum subtree cost $\Phi_i^{min}$ for $T_i$ gets updated. The loop of lines 7-10 terminates as soon as $F_i$ exceeds $F_i^{UB}$ . Let $F_{UB}$ be the maximum value of $F_i^{UB}$ for all nodes after CTC finishes. If $F_{max} > F_{UB}$ , the latter replaces the former in the complexity analysis, since it is the actual upper bound of all network frequencies used in our algorithms.

A similar optimization applies to algorithm CSC, when computing the minimum subtree cost $\Phi_{j}^{min}$ (lines 10-12 in Fig. 7). Specifically, an upper bound $\Phi_{j}^{min}-\sum_{l\not\in j,n_{i}\in T_{j}}F_{l}^{LB}$ for $F_{j}$ is incrementally maintained, and the loop stops when $F_{j}$ exceeds it. In our running example, the $6^{th}$ call of CSC is eliminated, since $F_{2}=13$ plus $f_{4}$ and $f_{5}$ already exceeds the previously computed subtree cost $\Phi_{2}^{6.5}=19.5$ , when $F_{2}$ is set to 6.5.

Finally, we discuss the adaptation of the above algorithms to changes of the routing tree T. A straightforward solution is to re-compute the network frequencies of all sensors whenever T is modified. The main challenge is to ensure that after the transition to the new network frequencies, all sensors remain locally synchronized, while satisfying their respective sampling frequency requirements. Specifically, immediately after the new tree is applied, all sensors in the WSN wake up simultaneously, start a new cycle, and switch to their new network frequencies thereafter. This method assigns the optimal network frequency to each sensor at all times, but incurs considerable cost during transitions. An alternative approach reduces the cost of transitions as follows. First, based on historical data, we partition the sensors into dynamic nodes, which change their respective parents frequently, and static ones with stable parent nodes. Then, for each minimal subtree $T_{i}$ containing at least one dynamic node, we apply global synchronization to its corresponding subtree $T_{i}$ , i.e., all nodes in $T_{i}$ share the same network frequency. $T_{i}$ is then treated as a single node in algorithms CTC, CSC and CNF, with a weight proportional to the number of nodes in $T_{i}$ . Accordingly, network frequencies need to be re-computed only when at least one static node changes its parent in T, which happens infrequently.

# V. FINDING ROUTING TREES

This section focuses on Problem 2, i.e., finding the best routing tree from a given connectivity graph. Following the common practice in the WSN literature, we restrict the search space for routing schemes to min-hop routing trees [1]. Unfortunately, even under this additional restriction, Problem 2 is still intractable. Therefore, we resort to heuristic methods.

Based on the min-hop property, LS partitions nodes into layers, so that the l-th layer contains nodes requiring at least l hops to reach $n_{0}$ . Clearly, in a min-hop tree, the parent of a layer-l node must reside at layer l-1. LS starts from the layer $l_{max}$ of nodes that need the most hops to reach $n_{0}$ (i.e., the leaves of the routing tree T) and builds T bottom-up. Specifically, whenever LS examines a node $n_{j}$ at level l, the subtree $T_{j}$ rooted at $n_{j}$ containing nodes from levels $l+1$ to $l_{max}$ , has already been constructed. LS then extends $T_{j}$ by adding an appropriate parent $n_{i}$ of $n_{j}$ . Let $P_{j}$ denote the set of candidate parents of $n_{j}$ , which consists of layer l-1 nodes that are connected to $n_{j}$ in G. The selection of $n_{i}$ is performed according to the following heuristics.

Heuristic 1: Given a node $n_j$ , the parent $n_i \in P_j$ of $n_j$ should satisfy that $f_i \geq F_j^{LB}$ (Equation 1). If no such node exists in $P_j$ , the parent of $n_j$ is the node $n_i$ with the highest $f_i$ among all nodes in $P_j$ .

Heuristic 2: Given a node $n_j$ , if multiple nodes in $P_j$ have sampling frequencies no less than $F_j^{LB}$ , the parent of $n_j$ is the node $n_i \in P_j$ , that satisfies $f_i \geq F_j^{LB}$ and minimizes $f_i / \lfloor f_i / F_j^{LB} \rfloor$ .

Intuitively, Heuristic 1 aims at minimizing the value $\Delta_i = F_i - f_i$ for the parent node $n_i$ . In particular, in order to synchronize $n_i$ and $n_j$ , $F_i$ must be no less than $F_j$ , which, in turn, is lower bounded by $F_j^{LB}$ according to Lemma 2. Hence, the heuristic tries to pick a node $n_i \in P_j$ satisfying $f_i \geq F_j^{LB}$ , in which case it is possible that $\Delta_i = 0$ . When there is no such node in $P_j$ , $\Delta_i$ is lower bounded by $F_j^{LB} - f_i$ . Thus, the node $n_i$ with the highest $f_i$ (i.e., minimal $F_j^{LB} - f_i$ ) is chosen as $n_j$ 's parent. Heuristic 2, on the other hand, tries to minimize the network frequency $F_j$ for the child node $n_j$ . Specifically, since $F_i$ must be a multiple of $F_j$ , the lowest $F_j$ is obtained, when $F_i = f_i$ , and $F_j = F_i / \lfloor f_i / F_j^{LB} \rfloor = f_i / \lfloor f_i / F_j^{LB} \rfloor$ . Thus, Heuristic 2 chooses the parent $n_i$ that minimizes this value. Fig. 10 shows an algorithm that applies the above heuristics. Find\_Routing\_Tree first partitions all nodes into layers (line 1), and builds $T$ bottom-up. If a node $n_i$ is directly connected to the base station $n_0$ in $G$ , $n_0$ becomes the parent of $n_i$ . Otherwise, the best parent $P_i$ of $n_i$ is chosen according to Heuristic 1 (line 11) or 2 (line 12).

Find_Routing_Tree(G, $f_{1}$ - $f_{N}$ ): returns T
// Input: G: connectivity graph, $f_{1}$ - $f_{N}$ : sampling frequencies
// Output: T: routing tree of the WSN
1. Partition sensor nodes into layers
2. Let layer $l_{max}$ be the deepest layer
3. Initialize T with nodes $n_{1}$ - $n_{N}$ , and no edges
4. For $l = l_{max}$ DownTo 1
5.    For each node $n_{j}$ on layer l
6.    If l=1, add edge $<n_{0}, n_{j}>$ to T
7.    Else
8.    Compute $F_{j}^{LB}$ according to Equation (1)
9.    Let $P_{j}$ be the set of candidate parents of $n_{j}$ 10.    If there does not exist $n_{i} \in P_{j}$ such that $f_{i} \geq F_{j}^{LB}$ 11.    Choose $n_{i} \in P_{j}$ according to Heuristic 1
12.    Else, choose $n_{i} \in P_{j}$ according to Heuristic 2
13.    Add edge $<n_{i}, n_{j}>$ to T
14. Return T   
Fig. 10 Algorithm Find\_Routing\_Tree

The algorithm takes $O(N^{2})$ time (for choosing the best parent for each node) and $O(N^{2})$ space (for storing G), where N is the number of sensors. Since the network frequency assignment module has the same space and time complexities with respect to N according to Theorem 3, the proposed solution to Problem 2 takes $O(N^{2})$ time and space overall, meaning that it easily scales to large WSNs. Furthermore, our experiments, shown next, demonstrate that Find\_Routing\_Tree usually identifies high-quality trees that lead to significant energy savings.

Finally, changes in the connectivity graphs are handled as follows. Whenever at least one link in the current routing tree T is broken, we re-compute T using Find\_Routing\_Tree, as well as the network frequencies of the sensors. Otherwise, Find\_Routing\_Tree is invoked periodically, and the transition process starts when a better routing tree is detected.

# VI. EXPERIMENTAL EVALUATION

We have implemented the proposed methods in C++, and carried out all experiments on a Core 2 Duo 2.6GHz PC with 2GBytes of memory. We use two real datasets, Greenorbs (94 sensors), Intel Lab (52 sensors), and a synthetic one.

GreenOrbs : GreenOrbs [16] is deployed by our group in a forest area in China. It contains 94 active sensors measuring temperature, humidity and light per minute. In our experiments, we use the temperature readings. The WSN follows the collection tree protocol (CTP) [6]. Specifically, sensors are organized into a routing tree, which is periodically adjusted based on the current link quality conditions. We observed that during a period of 12 hours, there is only a small number of timestamps when the tree changed. Furthermore, a large part of the tree, which forms the backbone of the network remained stable throughout the testing period. Fig. 11a shows the geographic locations of the sensors and the base station, as well as the connectivity graph of the entire WSN.

![](images/b821c8a990c1688f29270265f0f4f45faf9b95ddd0b1c4996f71d3d6ff4d1fb8.jpg)



(a) GreenOrbs

![](images/2a5ea70f4c65357786d3a53b22a2022786ba2c474ad22a533069565fa977a68d.jpg)



(b) IntelLab

![](images/d47b31b6d9fa366c416c789c475eb00b9429ecd167e7972add631e0db15a7d2d.jpg)



Basé station   
(c) Synthetic (N=100)   
Fig. 11 Connectivity graphs of the datasets used in the experiments

We set the sampling frequency of each sensor $n_i$ based on the change rate of $n_i$ 's readings. The intuition is that a sensor with stable readings should sample less frequently than another whose readings change with a high rate. Specifically, suppose that node $n_i$ has collected $m$ samples $s_{i,1}, s_{i,2}, \ldots, s_{i,m}$ at $m$ timestamps $t_{i,1}, t_{i,2}, \ldots, t_{i,m}$ . The change rate $cr_i$ of $n_i$ is calculated by:

$$
c r _ {i} = \frac {\sum_ {j = 1} ^ {m - 1} \left| s _ {i , j + 1} - s _ {i , j} \right|}{\sum_ {j = 1} ^ {m - 1} t _ {i , j + 1} - t _ {i , j}} \tag {16}
$$

Let $f_{max}$ be the highest sampling frequency required by the application. The sampling frequency $f_i$ of a node $n_i$ is then:

$$
f _ {i} = \frac {c r _ {i} \cdot f _ {\text { max }}}{\max _ {j = 1} ^ {N} c r _ {j}} \tag {17}
$$

In our experiments, we use $f_{max}=20$ . Note that the specific value of $f_{max}$ does not affect the relative performance of the proposed methods. The maximum possible sampling frequency $F_{max}$ is set to $10:f_{max}=200$ . In all experimental settings, during the search for the optimal network frequencies, the algorithms always terminate earlier (i.e., using the optimizations described in Section IV-C) without testing the last regular frequency before $F_{max}$ .

IntelLab: IntelLab $^{4}$ includes data from 54 sensors that measure temperature, humidity, light and voltage every 31 seconds for a month. Similarly to GreenOrbs, we use temperature readings in the experiments. The sampling frequencies of the sensors are computed using Equations (16) and (17). The dataset does not include the connectivity graph G; instead, it lists the probability for each sensor $n_{i}$ to successfully deliver a message directly to a surrounding node $n_{j}$ . Accordingly, we add an edge $\langle n_{i}, n_{j} \rangle$ to G, whenever the probability of successful packet delivery between $n_{i}$ and $n_{j}$ is above 20%. Except for one sensor (ID=5), all others are connected in G. Meanwhile, the dataset does not mention the location or the connectivity of the base station. Hence, we simply treat sensor with ID 1 as the base station. Fig. 11b shows the resulting connectivity graph. Finally, there is no information on the routing tree.

Synthetic: We generate sensor locations uniformly within a $[0,1]\times[0,1]$ square. In the connectivity graph G, there is an edge $\langle n_{i}, n_{j} \rangle$ , if and only if, the distance between nodes $n_{i}$ and $n_{j}$ does not exceed 0.25. Fig. 11c displays the connectivity graph of 100 sensors. Additionally, the sampling frequencies are random numbers in the range [1, 100], which follow the Zipf distribution. Similar to the real datasets, the maximum possible network frequency $F_{max}$ is set to $10\cdot f_{max}=1000$ .

We investigate the energy savings and computational cost of LS, under four parameters: (i) number of nodes, (ii) distribution of the sampling frequencies, (iii) shape of the routing tree, and (iv) the number of dynamic nodes (i.e., with frequently changing parents). Sections VI-A and VI-B present results on real and synthetic datasets, respectively.

# A. Results for GreenOrbs and IntelLab

GreenOrbs and IntelLab, like most WSN currently under deployment, are restricted to relatively few nodes (under 100), for which the computational overhead of LS is negligible. Therefore, we defer the discussion on this cost for the synthetic data, and focus on the energy overhead. Specifically, let $t_{w}$ be the number of time units that a sensor is active per cycle, and P be the energy consumed per time unit. Given the sum of network frequencies $\Phi$ , the energy consumed by all sensors is $\Phi\cdot P\cdot t_{w}$ , which is proportional to $\Phi$ . Hence, in the following we simply report the value of $\Phi$ as the overall energy cost. We compare LS against the traditional globally synchronized (GS) approach, which sets the network frequency of each sensor to $f_{max}=\max\{f_{1},f_{2},\ldots,f_{N}\}$ . Clearly, the energy cost of GS is $\Phi=N\cdot f_{max}$ . We include two versions of LS: LS-Problem1 and LS-Problem2. The former considers a given routing tree T, whereas the latter computes T.

We first evaluate the impact of the number of nodes N on the total energy cost $\Phi$ , with a static tree T. Specifically, for GreenOrbs, LS-Problem1 uses a real routing tree $T_{real}$ , taken at an arbitrary timestamp. To vary N, we randomly remove leaf nodes from $T_{real}$ (and recursively, entire subtrees). IntelLab, on the other hand, does not include real routing trees. Hence, we evaluate only LS-Problem2, and vary N by removing random nodes. The sampling frequency of each node $n_{i}$ is fixed to the value computed based on the real change rate of $n_{i}$ 's readings, as described in the beginning of this section. Fig. 12 plots $\Phi$ as a function of N. Clearly, $\Phi$ grows with N for both LS and GS, since more sensors naturally lead to higher energy consumption. Comparing GS with LS, the former consumes significantly more energy, and the difference increases with N (note the logarithmic scale on the vertical axis). This is because when a new node $n_{i}$ is added, GS always assigns $F_{i} = f_{max}$ ; LS, on the other hand, usually sets $F_{i}$ to be far lower than $f_{max}$ since $n_{i}$ only needs to locally synchronize with its adjacent nodes. LS-Problem2 outperforms LS-Problem1, indicating that the proposed solution indeed generates better routing trees.

![](images/5c6d75affbf564ac235d8888f17464aa891d8b0e50b1a8ccf91d180d1f064218.jpg)



(a) GreenOrbs

![](images/c2e60a335a1f6da4c3ea5d66fdda63161f04653abb72bd419c6d53ab4b43e265.jpg)



(b) IntelLab   
Fig. 12 Energy cost $\Phi$ vs. number of nodes $N$

Next, we fix N to its maximum value, and study the effect of the sampling frequencies in the range $[1, 100]$ , generated according to Zipf distribution with skewness factor $\alpha$ . LS-Problem1 (resp. LS-Problem2) uses the real routing tree (resp. tree computed by the proposed heuristics) as before. Fig. 13 demonstrates the effect of $\alpha$ on $\Phi$ . Given the small node cardinality, a growing value of a decreases the probability that $f_{max}$ reaches its maximum value 100. Consequently, the cost of all methods drops. LS takes better advantage of this fact since it can isolate the effect of the high frequencies in their respective subtrees.

![](images/2a29133fd1d045b8587ca7be2480798598c923bea1e7c5f39fb440557936f117.jpg)



![](images/74877edefbaf8d798172798aa493dffeb3a89d53d7e60ae545900a9790ae6382.jpg)



Fig. 13 Energy cost $\Phi$ vs. sampling frequency skewness $\alpha$

Finally, we evaluate the impact of changing routing trees. Our implementation of LS is based on the second method discussed at the end of Section IV, which minimizes recomputations of network frequencies. In the GreenOrbs dataset, we identified 41 dynamic nodes among the real routing trees, which reside at the lowest levels of the tree. On average, network frequency re-computations are performed once every 40 times when T changes, which itself happens infrequently. Overall, LS using real routing trees achieves 34% energy savings compared to GS. To further investigate the effect of routing trees with different volatility, we randomly mark a number $N_{D}$ of nodes as dynamic in a bottom-up fashion, and evaluate the energy efficiency of LS. The total number of nodes N is fixed to its maximum value, and the sampling rates are derived from real readings. Fig. 14 demonstrates $\Phi$ against varying $N_{D}$ . The energy consumption of LS generally increases with $N_{D}$ , as more nodes are merged and share the same network frequencies. When the majority of sensors are dynamic, LS reduces to GS. Nevertheless, LS achieves considerable energy savings, even for relatively large values of $N_{D}$ ( $\sim50\%$ of N).

![](images/9e052e6662705d54e3cda7fdb9294e76c6af44040f68d3b6f5e7070bec82fd00.jpg)



(a) GreenOrbs

![](images/aee0f4b70c495afb696013d2ddd4e2767fcdc917f9e3c2d0a24ff9cbaa31a4a9.jpg)



(b) IntelLab   
Fig. 14 Energy cost $\Phi$ vs. number of dynamic nodes $N_{D}$

# B. Results for Synthetic Datasets

We repeat our experiments on a much larger synthetic dataset described in the beginning of this section. In addition to energy cost, we report the CPU time and the memory required by the proposed algorithms. We focus on static routing trees; the results for changing trees lead to similar conclusions as in GreenOrbs and IntelLab, and are omitted. Fig. 15 shows the effect of the number of nodes N, after fixing the skewness factor $\alpha$ of the sampling frequencies to 0.8. Similar to the real datasets, the energy overhead of all methods increases with N, and LS consistently outperforms GS. The CPU and memory overhead of LS grows quadratically with N, as predicted by Theorem 3. Nevertheless, even for N=10000, these costs are very low (i.e., less than 320 milliseconds and 7Mbytes), which confirms that the proposed algorithms could be utilized for WSN much larger than the ones currently deployed.

![](images/6e1d8ea39d50cd0bbf4b537848f1db0381fae4abac0209fdd32e99854888d8fe.jpg)



(a) Energy cost

![](images/d6da5ad180f814efb261ce6db3b6b6ab0165887d75b84e40a1f412fc49433ca0.jpg)



(b) Computational cost   
Fig. 15 Varying number of nodes

Fig. 16 fixes N=5000, and varies the skewness factor $\alpha$ of the sampling frequencies. Observe that, unlike the case of real datasets, the energy consumption of GS remains the same for all values of $\alpha$ because, due to the large number of nodes, there is always one that has the maximum sampling frequency 100. On the other hand, as $\alpha$ grows, the consumption of LS decreases for the reasons explained in the context of Fig. 13. The computational overhead of LS also drops because a lower $\Phi$ leads to a more restrictive upper bound on a node's network frequency. Consequently, the optimization of Section IV-C becomes more effective, leading to an earlier termination of the algorithm.

![](images/0eb4afccf2d84ef783a0f2c2095a8fcdbb825eda7f389e7aeccd7644f2869d3d.jpg)



(a) Energy cost

![](images/199a9019a84882fb999511a4cc052d1dff109104aab2e4b3538837739df50642.jpg)



(b) Computational cost   
Fig. 16 Varying the distribution of sampling frequencies

Fig. 17 investigates the impact of the routing tree on LS-Problem1. Specifically, we generate random trees with a given fanout fan for each internal node, and present the average of their results, after setting N=5000 and $\alpha=0.8$ . Since fan has no effect on GS, we report the ratio between the energy cost of LS and that of GS. The energy savings of LS increase with fan due to the fact that the height of the tree decreases; thus, a node $n_{i}$ with high $f_{i}$ influences fewer ancestors. The computational overhead also increases with fan because a higher fanout leads to a larger subtree for each internal node, and, consequently, more regular network frequencies to examine.

![](images/db2e73f17096859c8276cb9eb59efad9ba2ea567ab82fdfbc7881d1ebb0f13ca.jpg)



(a) Energy cost

![](images/112482da8255a5e7ceabcd8ddc174b74865b0c75ca688f14eb5f0804ae76f632.jpg)



(b) Computation cost   
Fig. 17 Varying the shape of the tree

# VII. CONCLUSION

This paper presents a novel framework that allows sensors to sample at different rates, while ensuring timely routing of packets. We focus on two versions of the problem, depending on whether the WSN topology is fixed or not. Extensive experiments, using real and synthetic datasets, demonstrate the effectiveness of local synchronization in both versions. In the future we plan to investigate the computation of routing trees that minimize the network frequencies and at the same time minimize the packet losses. Finally, another interesting direction is the extension of the proposed techniques to multi-path topologies.

# REFERENCES

[1] Akyildiz, I., Su, W., Sankarasubramaniam, Y., Cayirci, E. Wireless Sensor Networks: a Survey. Computer Networks, 38(4):393-422, 2002.   
[2] Considine, J., Li, F., Kollios, G., Byers, J. Approximate Aggregation Techniques for Sensor Databases. ICDE, 2004.   
[3] Deshpande, A., Guestrin, C., Madden, S., Hellerstein, J. M., Hong, W. Model-Driven Data Acquisition in Sensor Networks. VLDB, 2004.   
[4] Elson, J., Roemer, K. Wireless Sensor Networks: A New Regime for Time Synchronization. Computer Communication Review, 33(1):149-154, 2003.   
[5] Ganeriwal, S., Kumar, R., Srivastava, M. Timing-Sync Protocol for Sensor Networks. ACM SenSys, 2003.   
[6] Gnawali, O., Fonseca, R., Jamieson, K., Moss, D., Levis, P. Collection Tree Protocol. ACM SenSys, 2009.   
[7] Jurdak, R., Baldi, P., Lopes, C. Adaptive Low Power Listening for Wireless Sensor Networks. IEEE TMC, 6(8):988-1004, 2007.   
[8] Kim, S., Fonseca, R. Reliable Transfer on Wireless Sensor Networks. IEEE SECON, 2004.   
[9] Levis, P., Gay, D. TinyOS Programming. Cambridge University Press, 2009.   
[10] Li, Q., Rus, D., Global Synchronization in Sensor Networks. IEEE Transactions on Computers, 55(2):214-226, 2006.   
[11] Madden, S., Franklin, J. Fjording the Stream: An Architecture for Queries over Streaming Sensor Data. ICDE, 2002.   
[12] Madden, S., Franklin, M., Hellerstein, J. The Design of an Acquisitional Query Processor for Sensor Networks. SIGMOD, 2003.   
[13] Madden, S., Franklin, M., Hellerstein, J., Hong, W. TAG: a Tiny AGgregation Service for Ad-Hoc Sensor Networks. OSDI, 2002.   
[14] Madden, S., Szewczyk, R., Franklin, M., Culler, D. Supporting Aggregate Queries Over Ad-Hoc Wireless Sensor Networks. IEEE WMCSA, 2002.   
[15] Manjhi, A., Nath, S., Gibbons, B. Tributaries and Deltas: Efficient and Robust Aggregation in Sensor Network Streams. SIGMOD, 2005.   
[16] Mo, L., He, Y., Liu, Y., Zhao, J., Tang, S., Li, X., Dai, G. Canopy Closure Estimates with GreenOrbs: Sustainable Sensing in the Forest. ACM SenSys, 2009.   
[17] Nath, S., Gibbons, P., Seshan, S., Anderson, Z. Synopsis Diffusion for Robust Aggregation in Sensor Networks. SenSys, 2004.   
[18] Shnayder, V., Hempstead, M., Chen, B., Allen, G., Welsh, M. Simulating the Power Consumption of LargeScale Sensor Network Applications. ACM SenSys, 2004.   
[19] Silberstein, A., Braynard, R., Yang, J. Constraint Chaining: On Energy-Efficient Continuous Monitoring in Sensor Networks. SIGMOD, 2006.   
[20] Silberstein, A., Munagala, K., Yang, J. Energy-Efficient Monitoring of Extreme Values in Sensor Networks. SIGMOD, 2006.   
[21] Wu, Y., Li, X., Liu, Y., Lou, W. Energy-Efficient Wake-up Scheduling for Data Collection and Aggregation. IEEE TPDS, 21(2):275-287, 2009.   
[22] Yang, X., Lim, H., Özsu, M., Tan, K. In-Network Execution of Monitoring Queries in Sensor Networks. SIGMOD, 2007.