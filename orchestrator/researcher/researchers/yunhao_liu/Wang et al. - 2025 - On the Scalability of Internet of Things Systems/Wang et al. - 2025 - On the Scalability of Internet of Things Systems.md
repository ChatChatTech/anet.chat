# JCST Papers

# Only for Academic and Non-Commercial Use

Thanks for Reading!

# Survey

Computer Architecture and Systems

Artificial Intelligence and Pattern Recognition

Computer Graphics and Multimedia

Data Management and Data Mining

Software Systems

Computer Networks and Distributed Computing

Theory and Algorithms

Emerging Areas

![](images/f8d79fb3048b512154f41c811b3ecc5aa193d66b2d3ca7774b30584cb2df0a46.jpg)



![](images/c3db5d5b1c0c2735aaf2713de0dbf0fbdcfddc7899a3ffef8349660b56b7fb47.jpg)  
JCST WeChat

Subscription Account

JCST URL: https://jcst.ict.ac.cn

SPRINGER URL: https://www.springer.com/journal/11390

E-mail: jcst@ict.ac.cn

Online Submission: https://mc03.manuscriptcentral.com/jcst

Twitter: JCST\_Journal

LinkedIn: Journal of Computer Science and Technology

# On the Scalability of Internet of Things Systems

Ji-Liang Wang $^{1}$ (王继良), Senior Member, CCF, IEEE, Member, ACM
Shuai Tong $^{2}$ (童率), Member, CCF, ACM, IEEE
Xiang-Yang Li $^{3}$ (李向阳), Fellow, ACM, IEEE, Senior Member, CCF
Zheng Yang $^{1}$ (杨铮), Fellow, IEEE, Senior Member, CCF, Member, ACM
Fu Xiao $^{4}$ (肖甫), Senior Member, CCF, IEEE, Member, ACM
and Yun-Hao Liu $^{2,5,*}$ (刘云浩), Fellow, CCF, ACM, IEEE

$^{1}$ School of Software, Tsinghua University, Beijing 100084, China   
$^{2}$ Department of Automation, Tsinghua University, Beijing 100084, China   
$^{3}$ School of Computer Science and Technology, University of Science and Technology of China, Hefei 230026, China   
$^{4}$ School of Computer Science, Nanjing University of Posts and Telecommunications, Nanjing 210023, China   
$^{5}$ Global Innovation Exchange Institute, Tsinghua University, Beijing 100084, China

E-mail: jiliangwang@tsinghua.edu.cn; tongshuai@mail.tsinghua.edu.cn; xiangyangli@ustc.edu.cn; yangzheng@tsinghua.edu.cn
xiaof@njupt.edu.cn; yunhao@tsinghua.edu.cn

Received January 14, 2025; accepted May 22, 2025.

Abstract The rapid growth of the Internet of Things (IoT) demands efficient system architectures and protocols to ensure consistent performance at scale. This paper explores the scalability of IoT systems across three key layers: sensing, network, and control. IoT scalability is the ability of a system to maintain consistent and reliable performance despite a continuous increase in connected devices. To evaluate scalability, we introduce the scalability indicator (SI), a metric designed to assess an IoT system's scalability capability. Through extensive research and real-world deployments, we identify key challenges in data sensing, routing, and system control. Our study presents a model to understand these challenges and proposes strategies to optimize resource utilization, ensuring efficient data collection. The findings also emphasize the key influencing factors for the stable performance of large-scale IoT systems, providing valuable insights for how to design scalable systems that can meet the growing demand for interconnected devices.

Keywords Internet of Things (IoT), network scalability, wireless sensor network, routing protocol

# 1 Introduction

The Internet of Things (IoT) connects everyday objects, enabling them to sense and exchange data through sensors, processors, and communication hardware $^{[1, 2]}$ . It is reported that the number of IoT-connected devices has exceeded 16.6 billion by the end of 2023, a growth of 15% over 2022 $^{[3, 4]}$ . The global IoT market is expected to grow up to 114.2 billion dollars by the end of 2025, as depicted in Fig.1. As the scale of IoT systems expands, maintaining efficiency and scalability becomes a critical challenge. Small inefficiencies that are manageable in smaller systems can quickly escalate as the system scale grows up.

The general architecture of IoT systems, shown in Fig.2, comprises three layers: the sensing layer for data collection, the network layer for data transmission, and the control layer for system management. These layers are closely interconnected, and their performance collectively determines system scalability. As the number of devices grows, these layers have to process data collection, transmission, and system management more efficiently. It is essential to explore scalable solutions for IoT systems that optimize resource usage.

![](images/40f59f8dc2f3c84cba99e3c3261a058965701d8d0afcd331b28f8755574f7420.jpg)



Fig.1. Growth trends of global IoT market $^{[5]}$ .

Early IoT systems, such as wireless sensor networks (WSNs), were designed to explore the feasibility and potential of IoT technology. These systems, with fewer than 1000 nodes, faced significant scalability challenges. As the number of devices grew, data collection and network management became increasingly difficult. Furthermore, many devices were battery-powered, leading to energy constraints. Table 1 outlines some of these pioneering systems, highlighting both their capabilities and the scalability issues they encountered.

Scalability is a fundamental requirement of IoT systems, as it determines how well a system can expand while maintaining functionality. However, the term “scalability” is often used ambiguously. To better understand and evaluate scalability, precise models are required. Previous studies have explored scalability from different perspectives, such as data processing $^{[11]}$ , transmission $^{[12]}$ , and resource management $^{[13]}$ . These studies often focus on isolated aspects of scalability, but a comprehensive model is needed to account for the interactions among the sensing, network, and control layers.

![](images/62c3c3f95dcf9cd11ed1d40e12927ba3f381e009ff997ab67128d4083314f5a6.jpg)



Fig.2. Network architecture of IoT systems, consisting of three layers: sensing (data collection), network (data transmission), and control (system management). These layers interact to ensure scalability as the system grows. MIB: management information base.

Table 1. Network Scale and Performance Comparison of Typical IoT Systems 

<table><tr><td>System</td><td>Year</td><td>Development</td><td>Scale (Number of Nodes)</td><td>Duration (day)</td><td>Data Collected (%)</td></tr><tr><td>Great Duck Island Monitoring[6]</td><td>2002</td><td>UC Berkeley</td><td>149</td><td>19</td><td>&lt;40.0</td></tr><tr><td>VigilNet[7]</td><td>2005</td><td>Virginia Tech.</td><td>200</td><td>90–180</td><td>40.0</td></tr><tr><td>Volcano Monitoring[8]</td><td>2007</td><td>Harvard Univ.</td><td>16</td><td>19</td><td>68.5</td></tr><tr><td>Trio[9]</td><td>2006</td><td>UC Berkeley</td><td>557</td><td>120</td><td>60.0</td></tr><tr><td>iSENSE[10]</td><td>2013</td><td>Jadavpur Univ.</td><td>100</td><td>30</td><td>75.0</td></tr></table>

This paper introduces a model to define and assess the scalability of IoT systems. The model considers the three core layers: sensing, network, and control. As these layers grow, each faces distinct scalability challenges. The sensing layer must cope with increasing data collection demands, the network layer must handle larger volumes of data transmission, and the control layer must manage increased complexity in system tasks like fault diagnosis. We propose three criteria for evaluating IoT scalability.

1) Manageable Sensing Demand. As the system grows, the sensing layer should be able to handle more data without a significant increase in resource usage per node.   
2) Efficient Use of Routing Resources. The network layer should not be overwhelmed as more nodes are added.   
3) Bounded Control Overhead. The control layer should avoid excessive overhead that interferes with core system functions.

We analyze the sensing, routing, and control layers to develop a structured approach for quantifying scalability and optimizing resource allocation.

This paper presents a structured approach to analyze and evaluate IoT scalability under various conditions, drawing insights from our long-term and large-scale IoT deployments. We built systems to examine IoT scalability, beginning with the GreenOrbs project $^{[14]}$ , which monitored forest environments, and followed by the CitySee system $^{[15]}$ , one of the largest outdoor wireless sensor networks designed to monitor urban environmental factors. These projects highlighted key scalability challenges, including managing communication between devices, handling large-scale data collection, and addressing network diagnosis and control overheads. This paper extends our understanding of these challenges by providing a formal model to analyze IoT scalability.

This paper is structured as follows. Section 2 presents the model and definition of the scalability indicator (SI) metric. Section 3 explores the sensing efficiency at the sensing layer. Section 4 focuses on the routing efficiency at the network layer. Section 5 examines the control overhead at the control layer. Section 6 provides a case study to validate the scalability model. Finally, Section 7 gives an illustration of related work, and Section 8 concludes the paper.

# 2 Metric Definition

This paper explores the factors affecting the scalability of IoT systems, and presents a model to define and evaluate IoT scalability. IoT systems can be viewed as comprising three key layers, i.e., the sensing layer, the network layer, and the control layer, each of which may become a potential bottleneck when the system scales up. Therefore, a comprehensive model for IoT scalability must address the constraints imposed by these three layers.

To determine whether an IoT system is scalable, the following three core criteria must be met.

Criterion 1. Manageable Increase of Sensing Resource Demand. As the system scales, the sensing layer generates exponentially increasing data volumes. A scalable system must enhance its sensing capacity without inducing a proportional rise in per-node resource consumption (e.g., computational power, storage, or energy). If resource demands grow super-linearly with system size, unsustainable overhead will emerge, ultimately limiting scalability. This criterion guarantees that the system maintains efficient resource utilization while accommodating expanding data requirements.

Criterion 2. Preservation of Routing Resources During Network Expansion. The addition of IoT devices to the network must not deplete critical transmission resources (e.g., bandwidth, energy) at individual nodes. Each device must retain its ability to participate in data transmission without exhausting its allocated resources. This ensures that network growth does not create node-level bottlenecks (e.g., congestion, energy depletion) or compromise the overall system reliability.

Criterion 3. Bounded Control Overhead. As the system scales, the overhead associated with control tasks (e.g., fault diagnosis, topology maintenance, and security protocols) must remain subordinate to the overhead of core sensing and transmission operations. If control-related costs become too large, the system's ability to prioritize and execute its primary functions — data collection and transmission—will degrade. This criterion ensures that management tasks remain lightweight and optimized for scalability.

These criteria emphasize two key dimensions for evaluating IoT scalability.

1) Data capacity: the system ability to enhance sensing data collection and transmission efficiency as it scales.   
2) Cost efficiency: the system ability to control the growth of resource overhead (e.g., energy, bandwidth, and computation) as it expands.

Previous literature has typically focused on a single layer (e.g., the network layer) or has concentrated solely on data capacity without considering resource overhead. As a result, these studies cannot comprehensively assess the scalability of the entire IoT system.

To operationalize this framework, we propose scalability indicator (SI), a quantitative metric that evaluates the scalability of an IoT system. SI is defined as the maximum amount of data that can be sensed and transmitted by an IoT system, given finite resources at each node. SI captures two key aspects of IoT scalability: 1) capacity to collect and transmit valid data across varying system scales, and 2) capacity to maintain bounded resource consumption at each node (e.g., energy, bandwidth). By considering both data capacity and cost efficiency, this metric enables an accurate assessment of an IoT system's ability to scale while managing resource usage effectively.

Subsequently, we illustrate how to evaluate the SI of a given IoT system. SI is influenced by the three primary layers of the IoT architecture. Table 2 present the definition of related variables.

Table 2. Summary of Variables 

<table><tr><td>Variable</td><td>Description</td></tr><tr><td> $Res$ </td><td>Available resources per node</td></tr><tr><td> $N$ </td><td>Number of nodes</td></tr><tr><td> $R_{Sen}$ </td><td>Resources for sensing tasks</td></tr><tr><td> $E_{Sen}$ </td><td>Sensing efficiency</td></tr><tr><td> $D_{Sen}$ </td><td>Valid data sensed</td></tr><tr><td> $R_{Rout}$ </td><td>Resources for routing tasks</td></tr><tr><td> $E_{Rout}$ </td><td>Routing efficiency</td></tr><tr><td> $D_{Rout}$ </td><td>Data supported for routing</td></tr><tr><td> $R_{Ctrl}$ </td><td>Resources for control tasks</td></tr></table>

1) Sensing Layer. To perform sensing tasks, IoT nodes must allocate resources, including energy, computation, and storage, to operate sensors and process the collected data. Let $R_{Sen}$ represents the resources allocated by each node for sensing tasks. To quantify how effectively a node converts its allocated resources into meaningful data, we define the sensing efficiency of each IoT node as $E_{Sen}$ , which depends on the specific sensor hardware and sensing tasks. For an IoT system, the amount of valid data sensed by each node is:

$$
D _ {\mathrm{Sen}} = E _ {\mathrm{Sen}} \times R _ {\mathrm{Sen}}.
$$

2) Network Layer. At the network layer, data packets are forwarded from source to destination through multi-hop routing. Each node consumes resources $R_{Rout}$ for routing tasks, with efficiency $E_{Rout}$ measuring how effectively these resources are used. $E_{Rout}$ varies based on the routing protocol, influencing resource utilization and performance. The total data a node can support for routing is determined by:

$$
D _ {\mathrm{Rout}} = E _ {\mathrm{Rout}} \times R _ {\mathrm{Rout}}.
$$

3) Control Layer. The control layer ensures the seamless operation of the IoT system by performing tasks such as failure monitoring and network diagnosis. The resources allocated for control tasks are denoted as $R_{Ctrl}$ . Combined with resources for sensing $R_{Sen}$ and routing $R_{Rout}$ , the total resource consumption is constrained by the node's available resources Res, expressed as:

$$
R _ {\text { Sen }} + R _ {\text { Rout }} + R _ {\text { Ctrl }} = \text { Res }. \tag {1}
$$

Sensed data $D_{\text{Sen}}$ and routed data $D_{\text{Rout}}$ are mutually constrained: when $D_{\text{Sen}} > D_{\text{Rout}}$ , the node's transmission capacity becomes the bottleneck, and the valid data $SI = D_{\text{Rout}}$ ; conversely, when $D_{\text{Sen}} < D_{\text{Rout}}$ , the sensing capacity limits performance, and $SI = D_{\text{Sen}}$ . The IoT system achieves optimal performance when sensing and routing capacities are balanced, i.e., $D_{\text{Sen}} = D_{\text{Rout}}$ , maximizing the valid data contribution SI.

To estimate the optimal SI for a given network, we enforce $D_{Sen} = D_{Rout}$ on each node. Substituting the expressions for $D_{Sen}$ and $D_{Rout}$ , we obtain:

$$
E _ {\mathrm{Sen}} \times R _ {\mathrm{Sen}} = E _ {\mathrm{Rout}} \times R _ {\mathrm{Rout}}. \tag {2}
$$

Using the resource constraint from (1), $R_{\mathrm{Sen}} = Res - R_{\mathrm{Rout}} - R_{\mathrm{Ctrl}}$ , we substitute $R_{\mathrm{Sen}}$ into (2):

$$
E _ {\text { Sen }} \times (R e s - R _ {\text { Rout }} - R _ {\text { Ctrl }}) = E _ {\text { Rout }} \times R _ {\text { Rout }}.
$$

Solving for $R_{\mathrm{Rout}}$ , we derive:

$$
R _ {\text { Rout }} = \frac {E _ {\text { Sen }} (R e s - R _ {\text { Ctrl }})}{E _ {\text { Rout }} + E _ {\text { Sen }}}. \tag {3}
$$

Finally, substituting (3) into the expression for $D_{Rout}$ , the valid data contribution SI for the entire IoT sys-

tem is:

$$
\begin{array}{l} S I = D _ {\text { R   o   u   t }} \times N \\ = E _ {\text {Rout}} \times R _ {\text {Rout}} \times N E _ {\text {Rout}} \times E _ {\text {Rout}} (R _ {\text {Rout}}) \tag {4} \\ = N \times \frac {E _ {\mathrm{Rout}} \times E _ {\mathrm{Sen}} (R e s - R _ {\mathrm{Ctrl}})}{E _ {\mathrm{Rout}} + E _ {\mathrm{Sen}}}. \\ \end{array}
$$

Here, Res represents the total resources available per node, while $E_{Sen}$ , $E_{Rout}$ , and $R_{Ctrl}$ depend on the sensing, routing, and control mechanisms of the IoT system, respectively.

The valid data contribution SI is a key metric for evaluating how effectively an IoT system adapts to increasing network sizes while preserving functionality and data integrity. On the one hand, a system is deemed scalable if its SI increases with network expansion, demonstrating its capacity to support a growing number of devices without degrading data collection and transmission performance. On the other hand, if the SI stagnates or decreases as the network grows, it reflects diminishing performance and a lack of scalability. In Sections 3–5, we analyze the SI of IoT systems under various sensing, routing, and control mechanisms, respectively.

# 3 Sensing Efficiency

Sensing efficiency $E_{Sen}$ measures the amount of valid data collected per unit of sensing resource. It is a key metric for evaluating IoT system performance, as it balances data acquisition with resource constraints such as energy, processing power, and storage.

In traditional IoT systems that use dedicated sensors (e.g., temperature, humidity, or light sensors), $E_{Sen}$ is closely linked to hardware specifications and the frequency of sensor activation. These sensors convert physical phenomena into digital signals, with resource consumption increasing linearly as the data acquisition grows. For instance, a temperature sensor requires a fixed resource K (including power, computation, and transmission costs) for each measurement. As a result, sensing efficiency $E_{Sen}$ simplifies to 1/K, remaining constant ( $E_{\mathrm{Sen}} \propto O(1)$ ) regardless of scale. This is because resource consumption grows linearly with data demands.

To address this limitation, adaptive sampling techniques adjust the measurement frequency based on environmental conditions. During stable periods, sensors reduce sampling rates and interpolate data, thus lowering resource consumption while maintaining data resolution. During periods of rapid changes, the sampling frequency increases to capture finer details. While these strategies slow the rate of resource usage growth, they still maintain a linear relationship between data acquisition and resource expenditure. This fundamental scalability challenge remains, especially as IoT networks expand or data requirements increase.

Dedicated sensor-based methods face scalability challenges. As the size of the IoT system increases—e.g., with more sensors or more frequent data acquisition—the total resource consumption can rise significantly. Therefore, while adaptive sensing techniques provide a more efficient use of resources, they are not a complete solution for managing large-scale IoT systems where resource constraints become more pronounced.

Recent innovations have led to participant sensing schemes, which eliminate the need for dedicated sensors. Instead, they leverage existing node functionalities to infer environmental data. In this approach, resource consumption is front-loaded during system deployment (e.g., setup and incentive mechanisms), represented as a fixed cost K. Once the system is deployed, node additions do not incur additional active resource costs. As the network grows to N nodes, the initial resource cost K is distributed across all nodes, reducing per-node resource consumption to K/N. This results in sensing efficiency $E_{Sen}$ scaling superlinearly with network size ( $E_{\mathrm{Sen}} \propto O(N)$ ), as efficiency improves with the number of participating nodes. These schemes not only improve scalability but also optimize utility, mobility, and operational costs. They are especially well-suited for large-scale IoT deployments in wide-area environments.

In summary, sensor-based systems are limited by linear resource scaling, but participant sensing decouples resource consumption from network size, enabling more scalable and energy-efficient data collection. This distinction highlights the critical role of sensing mechanisms in the long-term viability of IoT systems as they grow in complexity and scope.

# 4 Routing Efficiency

Routing efficiency measures how much valid data a node can transmit per unit of resource consumed. It depends on both the routing protocol and the total number of nodes. We measure the routing efficiency by first modeling the capacity of a single node, i.e., $CP_{i}$ for the i-th node, which represents the maximum number of data packets a node can transmit. Next, we estimate the valid data packets transmitted by the entire network using the $CP_{i}$ for each node and the ratio R of valid data to total transmissions. The total valid data VD is calculated as:

$$
V D = \sum_ {i = 1} ^ {N} C P _ {i} \times R.
$$

The value of R depends on the routing protocol, as different protocols use varying data forwarding strategies. Assuming each node consumes a constant amount of resources, c, the routing efficiency $E_{Rout}$ is calculated as:

$$
E _ {\mathrm{Rout}} = \frac {V D}{c \times N}.
$$

This formula allows us to evaluate routing efficiency across various IoT protocols by analyzing their impact on R and overall network performance. Below, we analyze the routing efficiency of several commonly used IoT routing protocols.

# 4.1 Flooding Protocol

Flooding is a simple routing protocol where each node receives and forwards packets to all its neighbors, ensuring that packets reach every node. While effective in dynamic IoT networks, it results in high resource consumption.

The replication of packets causes redundant transmissions, with each packet being forwarded across multiple paths. In a fully connected network, a packet can be forwarded up to N-1 times, where N is the number of nodes. As a result, the ratio of valid data to total transmissions is at most 1/N. Flooding also assumes that all nodes have similar roles and resources, giving each node a nearly identical capacity k. The total valid data in a flooding network is:

$$
V D _ {\text { flooding }} = \sum_ {i = 1} ^ {N} C P _ {i} \times R = N \times k \times \frac {1}{N} = k.
$$

The routing efficiency is:

$$
E _ {\text { R   o   u   t }} = \frac {V D _ {\text { f   l   o   o   d   i   n   g }}}{c \times N} = \frac {k}{c \times N} \propto O \left(\frac {1}{N}\right).
$$

In flooding, both k (node capacity) and c (resource consumption) are constant. However, the unrestricted forwarding leads to low routing efficiency, which decreases as the network size grows. Larger networks also face higher risks of collisions, congestion, and delays, potentially causing packet loss.

# 4.2 Global Link State Routing Protocol

Some protocols determine data routing paths using the global link state, such as OSPF (Open Shortest Path First). In these protocols, each router maintains the state of every link in the network and computes the shortest path whenever it has data to transmit. To enable this, nodes flood the network with link state advertisements containing their connectivity and cost information, ensuring every node builds a complete map of the network's topology.

For a network with N nodes and E links, the number of messages required for this process is approximately $O(E)$ . In the worst case, where the network is fully connected, the number of links E approaches $N(N-1)/2$ , resulting in the resource consumption for establishing the global link state database, $r_{database}$ , being proportional to $O(N^{2})$ . Once the topology map and routing database are established, the network enters a steady-state operation for data transmission. The average transmission path length is approximately the radius of the network, i.e., $\sqrt{N}$ . However, in highly dynamic IoT environments, the link state map must be frequently updated to reflect changes in the network. This frequent updating imposes a significant resource burden on each node. The resources consumed by maintaining the database reduce the data capacity of each node, $CP_{i}$ , which becomes proportional to $O(k-r_{\text{database}})$ , where k represents the node's total capacity.

During data transmission, each packet requires an average of $\sqrt{N}$ forwarding steps. Therefore, the ratio of valid data to total transmissions is approximately $O(1/\sqrt{N})$ . The total valid data $VD_{GLS}$ in the network can be expressed as:

$$
\begin{array}{l} V D _ {\mathrm{GLS}} = \sum_ {i = 1} ^ {N} C P _ {i} \times R = N \times (k - r _ {\text { database }}) \times \frac {1}{\sqrt {N}} \\ = k \sqrt {N} - r _ {\mathrm{database}} \sqrt {N}. \\ \end{array}
$$

The routing efficiency is then given by:

$$
E _ {\mathrm{Rout}} = \frac {V D _ {\mathrm{GLS}}}{c \times N} = \frac {k \sqrt {N} - r _ {\mathrm{database}} \sqrt {N}}{c \times N} \propto O \left(\frac {1}{\sqrt {N}}\right).
$$

At the best case where link state changes are infrequent, the resources consumed by database maintenance are negligible compared with data transmission, and the routing efficiency simplifies to approximately $O(1/\sqrt{N})$ . In extreme cases of very frequent updates, $E_{Rout}$ approaches zero due to the overwhelming resource burden by establishing the link state database.

# 4.3 Weak State Routing Protocol

Weak state routing uses a probabilistic forwarding mechanism for efficient and adaptive data transmission. Each node maintains a weak state table, assigning probabilities to potential routes based on factors like signal strength, link quality, buffer size, and distance. This reduces redundant transmissions by forwarding messages to a single designated neighbor.

The core of the weak state routing protocol is a probabilistic routing path selection model that adapts to dynamic IoT links using physical event fields. These fields represent environmental factors and physical conditions that influence routing decisions. Typical weak state table assigns probabilities based on the followings.

- Quality of Forwarding (QoF): choosing the neighbor with the best forwarding links.   
- Signal Strength: choosing the neighbor with the strongest signal.   
- Buffer Size: avoiding nodes that are currently overloaded with traffic.   
- Distance Metrics: selecting neighbors that provide the shortest path to the destination.

In this protocol, each valid packet is forwarded over an average path length of $\sqrt{N}$ , as each node forwards to one neighbor, not broadcasting to all. Each node's data capacity $CP_{i}$ is determined by its hardware capacity k, and no global state database is required. With $\sqrt{N}$ forwarding steps per packet, the ratio of valid data to total transmissions, R, is $O(1/\sqrt{N})$ . The total valid data, $VD_{ws}$ , is:

$$
V D _ {\mathrm{ws}} = \sum_ {i = 1} ^ {N} C P _ {i} \times R = N \times k \times \frac {1}{\sqrt {N}} = k \sqrt {N}.
$$

The routing efficiency $E_{Rout}$ is therefore:

$$
E _ {\mathrm{Rout}} = \frac {V D _ {\mathrm{WS}}}{c \times N} = \frac {k \sqrt {N}}{c \times N} \propto O (1 / \sqrt {N}).
$$

This indicates that routing efficiency decreases as network depth $\sqrt{N}$ increases. While a deeper network enhances reachability, it requires more forwarding steps, reducing efficiency. Optimizing the placement of gateways or sink nodes can minimize $\sqrt{N}$ , maintaining efficiency while conserving resources. The scalability of the model comes from its ability to adapt as the network grows. Since each node forwards based on real-time conditions, the protocol avoids redundant transmissions. As the network expands, the routing overhead remains proportional to $\sqrt{N}$ rather than N, requiring fewer updates across nodes.

A comparison of aforementioned IoT routing strategies, along with their descriptions and routing efficiencies, is presented in Table 3.

# 5 Control Efficiency

Control overhead refers to the resources consumed for maintaining the IoT systems, including control messages for establishing network topology, network failure diagnosis, and node energy management. Control overhead impacts the network performance, energy consumption, and overall efficiency, as it is key for ensuring the smooth running of the whole system.

Global state control mechanisms rely on prior knowledge and global queries to identify known symptoms of network failures. This approach incurs substantial diagnostic overhead, scaling with the number of nodes, resulting in a resource consumption proportional to the number of links in the network E, i.e.,

$$
R _ {\mathrm{Ctrl}} = \alpha \times E,
$$

where $\alpha$ is a constant representing the average number of control messages each node exchanges. In the worst case, where the network is fully connected, the number of links E approaches $N(N-1)/2$ . Thus, the resource consumption for the control layer is approximate to $O(N^{2})$ . Each node sends control messages to all the other nodes, and the number of control messages grows linearly with the number of nodes. In a dynamic network, routing tables need frequent updates. Each update involves multiple control messages that scale with the number of nodes. Besides, maintaining an up-to-date network topology requires control messages to be exchanged regularly among all nodes. Global network diagnostic processes involve each node sending a control message to every other node to gather state information, meaning the total number of control messages (and thus the control overhead) scales linearly with the number of nodes. Even if not every node needs to communicate with every other node, factors like broadcasting or multi-hop routing can still result in a linear increase in control resource consumption.

Table 3. Efficiency Comparison of IoT Routing Strategies 

<table><tr><td>Routing Strategy</td><td>Description</td><td>Efficiency</td></tr><tr><td>Flooding protocol</td><td>Forwarding messages to all nodes in the network, high redundancy</td><td> $O(1/N)$ </td></tr><tr><td>Global link state routing</td><td>Exchanging global network topology and link states to choose paths</td><td> $O(1/\sqrt{N})$ </td></tr><tr><td>Weak state routing</td><td>Using probabilistic selection to reduce overhead and adapt to dynamics</td><td> $O(1/\sqrt{N})$ </td></tr></table>

Some work uses a local link state mechanism for network control, which significantly reduces the control overhead by diagnosing network issues using only local information. A representative weak-state control mechanism is Agnostic Diagnosis (AD) $^{[16]}$ , an online lightweight failure detection approach. AD is motivated by the fact that the system metrics (e.g., radio-on time, number of packets transmitted) of IoT sensors usually exhibit certain correlation patterns. Violations of such patterns indicate potential silent failures. By leveraging the observation of transmission patterns and internal states of IoT nodes, this approach identifies temporal dependencies and spatial similarities in local network states, such as radio frequency time and transmission traffic. These patterns correlate with network faults, and significant deviations indicate potential issues without the need of extensive data collection. This local-only approach means that the control overhead remains constant regardless of the number of nodes in the network. The resources needed by network control $R_{Ctrl}$ at each node is now approximate to $O(D)$ , where D is the average number of neighbor nodes, highlighting the effectiveness and scalability of the local state based control mechanism. It also allows for the efficient and scalable management of IoT networks, ensuring robust performance even as the network size increases.

# 6 Scalability Evaluation of Existing Systems

# 6.1 Global State Based IoT Systems

Early IoT systems rely on global state information for sensing, routing, and system management. At the sensing layer, end nodes use customized sensors for data collection, where each processing cycle yields one piece of sensing data, with an efficiency of $E_{\mathrm{Sen}} \propto O(1)$ . At the routing layer, early systems use the flooding protocol for data transmission, where each message is broadcasted across all N nodes, leading to a routing efficiency of $E_{Rout}$ , which diminishes as the network scales, with $E_{\mathrm{Rout}} \propto O(1/N)$ . At the control layer, the system requires all nodes to store and continuously update a shared database for the global network state, where the control overhead increases as the network scales up, i.e., $R_{\mathrm{Ctrl}} \propto O(N^{2})$ . Figs.3(a) and 3(b) demonstrate the sensing and routing overhead in global state based IoT systems under varying network scales and protocol configurations, assuming a sensor operation power of 15 mW (typical for temperature sensors) and wireless transmission power of 10 mW (characteristic of BLE communications) with 15-byte data packets. The results show that energy overhead exhibits rapid growth with increasing node count, highlighting the fundamental trade-off between network scalability and energy efficiency in large-scale deployments.

![](images/c20deae939cdd98fb5310239c5173ee9d1bf4e602ef09fbcb5b4a5806d082407.jpg)



(a)   
![](images/3fa5e27c22e8401cbd2a7dbdb5ca860c190f40abe43e392cd38792514b916a03.jpg)



(b)

![](images/7c4c57386454e30e0e5c72ebce2369127cd00fd74d65e873b1e54388485fea68.jpg)



(c)   
Fig.3. System performance for global state based IoT systems, considering sensing overhead, routing overhead, and scalability indicator (SI) under different protocol settings. (a) System sensing overhead. (b) Network routing overhead. (c) Scalability indicator (SI).

Table 4 summarizes the efficiency and resource costs of each layer. The combined impact of these factors results in high resource consumption with limited scalability. As illustrated in (4), the SI for the whole IoT system is computed as:

$$
S I = \frac {N \times (E _ {\text {Rout}} \times E _ {\text {Sen}} (R e s - R _ {\text {Ctrl}}))}{E _ {\text {Rout}} + E _ {\text {Sen}}}.
$$

Substituting the analysis results in Table 3 into the formula of SI, we can get:

$$
\begin{array}{l} S I = N \times \left(\frac {k _ {0} \times k _ {1} / N \times (R e s - k _ {2} N ^ {2})}{k _ {0} + k _ {1} / N}\right) \\ = k _ {0} k _ {1} \times \frac {N (R e s - k _ {2} N ^ {2})}{k _ {0} N + k _ {1}}. \\ \end{array}
$$

The coefficients $k_{0}$ , $k_{1}$ , and $k_{2}$ are protocol-dependent parameters influenced by factors such as packet length and transmission duty cycle. The expression $Res - k_{2}N^{2}$ , representing the resource availability accounting for sensing and routing costs, remains positive but diminishes as the node count N increases. Fig.3(c) illustrates the SI evolution across network scales under different protocol configurations (corresponding to different IoT systems: ZebraNet $^{[17]}$ , Volcano monitoring $^{[8]}$ , and Hospital clinic $^{[18]}$ ), revealing a distinct non-linear trajectory. For small networks (low N), minimal resource consumption in sensing, routing, and control operations enables efficient resource allocation to core functionalities, driving SI improvement through enhanced connectivity and data utility. However, as N expands beyond a critical threshold, exponentially growing routing/control demands and diminishing sensing/routing efficiencies ( $E_{Sen}$ , $E_{Rout}$ ) dominate system behaviors.

Such a behavior highlights a fundamental limitation in the scalability of traditional global state based IoT systems: while the SI of those systems may initially improve as the network expands, the quadratic growth of resource costs creates a hard cap on scalability. As N increases, the network's ability to maintain high functionality diminishes, making it unsuitable for large-scale deployment.

# 6.2 Weak State Based IoT System

Weak state based IoT systems utilize a more resource-efficient approach for sensing, routing, and system management. At the sensing layer, participatory sensing is employed, where users' personal devices (such as smartphones and wearables) collect data. The sensing efficiency $E_{Sen}$ scales linearly with the number of nodes, i.e., $E_{\mathrm{Sen}} \propto O(N)$ , meaning that each additional node contributes proportionally to the system's data-gathering capacity without overburdening the network. At the network layer, weak-state routing reduces transmission overhead compared with flooding protocols. In weak-state routing, each message follows a probabilistic path to its destination, involving only one neighboring node in each forwarding step. The routing efficiency $E_{Rout}$ scales as $O(1/\sqrt{N})$ , significantly improving on the $O(1/N)$ efficiency of flooding. The probabilistic routing mechanism ensures that the resource cost grows much slower than in global-state systems, maintaining high efficiency even in large networks. At the control layer, weak state based systems use local state management, where nodes store information about their immediate neighbors rather than maintaining a global state database. The control resource consumption $R_{Ctrl}$ scales as $O(D)$ , where D is the average number of neighboring nodes, which is much smaller than N and grows slowly as the network expands. This localized approach reduces the control overhead while still supporting effective coordination and fault management, allowing the system to scale more efficiently.

Table 5 summarizes the overall efficiency and resource consumption of the IoT system under the weak-state model at each layer. By substituting the analysis results from Table 4 into (4), we can calculate the SI for weak state based IoT systems as follows:

Table 4. Evaluation of Efficiency and Resource Consumption for Global State Based IoT Systems 

<table><tr><td>Protocol Layer</td><td>Value</td><td>Description</td><td>Order</td></tr><tr><td>Sensing layer</td><td> $E_{\text{Sen}}$ </td><td>Sensing efficiency: collecting data from physical environments using specialized sensor hardware</td><td> $O(1)$ </td></tr><tr><td>Network layer</td><td> $E_{\text{Rout}}$ </td><td>Routing efficiency: delivering the sensing data from source nodes to sink nodes or gateways</td><td> $O(1/N)$ </td></tr><tr><td>Control layer</td><td> $R_{\text{Ctrl}}$ </td><td>Control resources consumption: managing the IoT network, processes data, and diagnoses any network issues</td><td> $O(N^{2})$ </td></tr></table>

Table 5. Evaluation of Efficiency and Resource Consumption for Weak State Based IoT Systems 

<table><tr><td>Protocol Layer</td><td>Value</td><td>Description</td><td>Order</td></tr><tr><td>Sensing layer</td><td> $E_{\text{Sen}}$ </td><td>Data collection using non-dedicated sensors</td><td> $O(N)$ </td></tr><tr><td>Network layer</td><td> $E_{\text{Rout}}$ </td><td>Data delivery using weak-state routing</td><td> $O(1/\sqrt{N})$ </td></tr><tr><td>Control layer</td><td> $R_{\text{Ctrl}}$ </td><td>Network management with local state</td><td> $O(D)$ </td></tr></table>

$$
\begin{array}{l} S I = \frac {N \times (E _ {\text {Rout}} \times E _ {\text {Sen}} (R e s - R _ {\text {Ctrl}}))}{E _ {\text {Rout}} + E _ {\text {Sen}}} \\ = N \times \left(\frac {k _ {0} N \times k _ {1} / \sqrt {N} \times (R e s - k _ {2} D)}{k _ {0} N + k _ {1} / \sqrt {N}}\right) \\ = k _ {0} k _ {1} \times \frac {N ^ {2} \times (R e s - k _ {2} D)}{k _ {0} N \sqrt {N} + k _ {1}}. \\ \end{array}
$$

The combination of linear sensing efficiency $E_{\mathrm{Sen}} \propto O(N)$ , slow-decreasing routing efficiency $E_{\mathrm{Rout}} \propto O(1/\sqrt{N})$ , and nearly constant control resource consumption $R_{\mathrm{Ctrl}} \propto O(D)$ makes the weak state based system highly scalable. Unlike global state based systems, where the SI rapidly decreases as N increases due to quadratic or worse scaling of resource costs, weak state based systems maintain a balance between functionality and resource consumption. This balance ensures that the SI either remains stable or increases as the network size grows, allowing the system to support larger IoT deployments without significant performance degradation.

Fig.4 shows the SI for IoT systems under various parameter settings (i.e., $k_{0}$ , $k_{1}$ , and $k_{2}$ from typical IoT deployments), revealing performance evolution with network expansion. Global state based systems exhibit initial SI gains from improved connectivity but suffer performance collapse as the quadratic growth in sensing/routing overhead and control-layer saturation create bottlenecks. In contrast, weak state based systems (GreenOrbs $^{[14]}$ ) achieve sustained scalability by maintaining stable sensing/routing efficiency, minimizing performance degradation even at large scales. These results quantify how protocol design balances functional gains against resource constraints in IoT scalability.

![](images/5e65eac9e492aa5bcbc7acc56a5ae98d884dda7ade14f95f030d1c193b3d2f05.jpg)



Fig.4. SI evaluation of existing IoT systems.

Building upon the principles of weak-state IoT systems, recent deployments such as The Things Network (TTN) represent the state-of-the-art in scalable community-based IoT infrastructures. TTN relies on the LoRaWAN standard and adopts a star-of-stars topology, where end devices communicate directly with community-operated gateways. Its crowdsourced deployment model and cloud-assisted control inherit the weak-state principle by avoiding global synchronization, multi-hop routing, and quadratic control overhead. As a result, the system maintains nearly constant per-node overhead and achieves sustainable scalability. Compared with early global-state systems such as ZebraNet, which relied on flooding-based routing and global coordination, the improvement in scalability is striking. In ZebraNet, the SI quickly saturates and remains below 30, limiting the system's scalability. In contrast, TTN already supports millions of devices worldwide. With each device typically transmitting several packets per day, the aggregated SI reaches the order of $10^{4} \sim 10^{5}$ . This highlights how the weak-state paradigm, combined with community-driven infrastructure and wide-area protocols, enables unprecedented scalability in modern IoT deployments.

# 7 Related Work

Previous research on IoT scalability has typically focused on individual dimensions such as data processing, transmission, or resource management. Luntovskyy and Globa $^{[6]}$ analyzed scalability from the perspective of data processing, emphasizing the optimization of cloud and fog computing for better resource distribution. Zyrianoff et al. $^{[7]}$ focused on data fusion strategies to reduce data volume and improve processing efficiency, addressing scalability primarily in terms of data handling. Arellanes and Lau and Predrag et al. $^{[19]}$ investigated the scalability of IoT systems through the aspect of data transfer and network capacities, proposing mechanisms to optimize control flow and reduce network load. Huang et al. $^{[20]}$ reviewed scalable network verification technologies, analyzing challenges in temporal and spatial scalability across data and control planes. Gupta et al. $^{[21]}$ examined vertical and horizontal scalability, focusing on the impact of hardware resources and proposing solutions such as microservices and load-balancing strategies to optimize resource usage.

Traditional wireless network capacity research has yielded foundational insights. Gupta and Kumar's theory establishes throughput scaling laws for dense ad hoc networks by analyzing the inherent interference limitations of wireless communication[22]. This theory primarily focuses on the network layer, overlooked the significant sensing and control overhead in IoT systems. Some research leverages Shannon's channel capacity to estimate the channel capacity limits for wireless communication under various conditions[23, 24]. They provide the theoretical framework for understanding the maximum achievable data rates and designing techniques like MIMO, network coding, and cooperative communication to approach these limits. These works typically concentrated on single-hop capacity, not encompassing full system-wide IoT. More recent research continues to refine capacity analysis for specific wireless networks, which are not directly adaptable to IoT scenarios without considering unique IoT constraints such as low computational capabilities and energy limitations[25, 26].

All previous studies generally analyzed IoT scalability from a fragmented perspective, focusing on only one aspect—whether data processing, network management, or resource allocation. In contrast, our work adopts a more holistic view by integrating the three critical layers of IoT systems: sensing, transmission, and management. We introduce scalability indicator (SI) as a comprehensive metric that evaluates scalability across these layers, addressing the combined effects on system performance and providing a unified approach to analyzing the scalability of IoT systems.

# 8 Conclusions

This paper provided a comprehensive study of IoT scalability across the sensing, network, and control layers. We introduced a theoretical model and the scalability indicator (SI) metric to assess the system's ability to maintain functionality and data integrity as the network size grows. By analyzing the sensing, routing, and control layers, we proposed a structured approach to quantify scalability and optimize resource allocation. Our findings highlight the need for balancing resource utilization across layers to ensure optimal performance. The SI serves as a crucial measurement metric of scalability, emphasizing the importance of maintaining stable system performance in large-scale IoT networks. These insights are critical for the future development of IoT infrastructures.

Conflict of Interest Yun-Hao Liu is an editorial board member for Journal of Computer Science and Technology and was not involved in the editorial review of this article. All authors declare that there are no other competing interests.

# References

[1] Li Y, Zhang Y. Digital twin for industrial Internet. Fundamental Research, 2024, 4(1): 21–24. DOI: 10.1016/j.fm-re.2023.01.005.   
[2] Yao S, Lu Y, Niu K, Dai J, Dong C, Zhang P. Semantic information processing for interoperability in the industrial Internet of Things. Fundamental Research, 2024, 4(1): 8–12. DOI: 10.1016/j.fmre.2023.06.003.   
[3] IoT Analytics. State of IoT 2024: Number of connected IoT devices growing 13% to 18.8 billion globally, 2024. https://iot-analytics.com/number-connected-iot-devices/, May 2025.   
[4] Tong S, Wang J L. Progress and challenges of LoRa low power wide area networks. Acta Electronica Sinica, 2024, 52(10): 3623–3642. DOI: 10.12263/DZXB.20240471.   
[5] Statista. Worldwide Internet of Things (IoT) semiconductor and sensor market size, 2025. https://www.statista.com/statistics/471264/iot-number-of-connected-devices-worldwide/, Sept. 2025.   
[6] Mainwaring A, Culler D, Polastre J, Szewczyk R, Anderson J. Wireless sensor networks for habitat monitoring. In Proc. the 1st ACM International Workshop on Wireless Sensor Networks and Applications (WSNA '02), Sept. 2002, pp.88–97. DOI: 10.1145/570738.570751.   
[7] He T, Krishnamurthy S, Luo L, Yan T, Gu L, Stoleru R, Zhou G, Cao Q, Vicaire P, Stankovic J A, Abdelzaher T F, Hui J, Krogh B. VigilNet: An integrated sensor network system for energy-efficient surveillance. ACM Trans. Sensor Networks, 2006, 2(1): 1–38. DOI: 10.1145/1138127.1138128.

[8] Werner-Allen G, Lorincz K, Johnson J, Lees J, Welsh M. Fidelity and yield in a volcano monitoring sensor network. In Proc. the 7th Symposium on Operating Systems Design and Implementation, Nov. 2006, pp.381–396. DOI:10.5555/1298455.1298491.   
[9] Dutta P, Hui J, Jeong J, Kim S, Sharp C, Taneja J, Tolle G, Whitehouse K, Culler D. Trio: Enabling sustainable and scalable outdoor wireless sensor network deployments. In Proc. the 5th International Conference on Information Processing in Sensor Networks, Apr. 2006, pp.407–415. DOI: 10.1145/1127777.1127839.   
[10] Bisoi S, Bhunia S S, Roy S, Mukherjee N. iSENSE: Intelligent sensor monitoring services with integrated WSN testbed. Procedia Technology, 2013, 10: 564–571. DOI: 10.1016/j.protcy.2013.12.396.   
[11] Luntovskyy A, Globa L. Performance, reliability and scalability for IoT. In Proc. the 2019 International Conference on Information and Digital Technologies, Jun. 2019, pp.316–321. DOI: 10.1109/DT.2019.8813679.   
[12] Zyrianoff I, Borelli F, Biondi G, Heideker A, Kamienski C. Scalability of real-time IoT-based applications for smart cities. In Proc. the 2018 IEEE Symposium on Computers and Communications, Jun. 2018, pp.688–693. DOI: 10.1109/ISCC.2018.8538451.   
[13] Arellanes D, Lau K K. Evaluating IoT service composition mechanisms for the scalability of IoT systems. Future Generation Computer Systems, 2020, 108: 827–848. DOI: 10.1016/j.future.2020.02.073.   
[14] Liu Y, He Y, Li M, Wang J, Liu K, Mo L, Dong W, Yang Z, Xi M, Zhao J, Li X Y. Does wireless sensor network scale? A measurement study on GreenOrbs. In Proc. the 2011 IEEE INFOCOM, Apr. 2011, pp.873–881. DOI: 10.1109/INFCOM.2011.5935312.   
[15] Liu Y, Mao X, He Y, Liu K, Gong W, Wang J. CitySee: Not only a wireless sensor network. IEEE Network, 2013, 27(5): 42–47. DOI: 10.1109/MNET.2013.6616114.   
[16] Miao X, Liu K, He Y, Liu Y, Papadias D. Agnostic diagnosis: Discovering silent failures in wireless sensor networks. In Proc. the 2011 IEEE INFOCOM, Apr. 2011, pp.1548–1556. DOI: 10.1109/INFCOM.2011.5934945.   
[17] Zhang P, Sadler C M, Lyon S A, Martonosi M. Hardware design experiences in ZebraNet. In Proc. the 2nd International Conference on Embedded Networked Sensor Systems, Nov. 2004, pp.227–238. DOI: 10.1145/1031495.1031522.   
[18] Chipara O, Lu C, Bailey T C, Roman G C. Reliable clinical monitoring using wireless sensor networks: Experiences in a step-down hospital unit. In Proc. the 8th ACM Conference on Embedded Networked Sensor Systems, Nov. 2010, pp.155–168. DOI: 10.1145/1869983.1869999.   
[19] Jelenkovic P R, Momcilovic P, Squillante M S. Scalability of wireless networks. IEEE/ACM Trans. Networking, 2007, 15(2): 295–308. DOI: 10.1109/TNET.2007.892846.   
[20] Huang H L, Xu K, Li Q, Li T, Fu S T, Gao X Y. Scalable network verification technologies: State of the art and future. Acta Electronica Sinica, 2024, 52(4): 1083–1102. DOI: 10.12263/DZXB.20230682.   
[21] Gupta A, Christie R, Manjula P R. Scalability in Inter-

net of Things: Features, techniques and research challenges. International Journal of Computational Intelligence Research, 2017, 13(7): 1617–1627.   
[22] Gupta P, Kumar P R. The capacity of wireless networks. IEEE Transactions on Information Theory, 2000, 46(2): 388–404. DOI: 10.1109/18.825799.   
[23] Li S, Liu Y, Li X Y. Capacity of large scale wireless networks under Gaussian channel model. In Proc. the 14th ACM International Conference on Mobile Computing and Networking, Sept. 2008, pp.140–151. DOI: 10.1145/1409944.1409962.   
[24] Franceschetti M, Migliore M D, Minero P. The capacity of wireless networks: Information-theoretic and physical limits. IEEE Trans. on Information Theory, 2009, 55(8): 3413–3424. DOI: 10.1109/TIT.2009.2023705.   
[25] Lauridsen M, Kovács I Z, Mogensen P, Sorensen M, Holst S. Coverage and capacity analysis of LTE-M and NB-IoT in a rural area. In Proc. the 84th IEEE Vehicular Technology Conference (VTC-Fall), Sept. 2016. DOI: 10.1109/VTCFall.2016.7880946.   
[26] Vejlgaard B, Lauridsen M, Nguyen H, Kovacs I Z, Mogensen P, Sorensen M. Interference impact on coverage and capacity for low power wide area IoT networks. In Proc. the 2017 IEEE Wireless Communications and Networking Conference, Mar. 2017. DOI: 10.1109/WCNC.2017.7925510.

![](images/05c16cbaf64b0e175d951e9226f3902b6fd24a904677dd7567e83965b1fac08c.jpg)



Ji-Liang Wang received his B.E. degree in computer science and technology from the University of Science and Technology of China, Hefei, in 2007, and his Ph.D. degree in computer science and engineering from the Hong Kong University of Science and

Technology, Hong Kong, in 2011. He is currently an associate professor with the School of Software and BN-Rist (Beijing National Research Center for Information Science and Technology), Tsinghua University, Beijing. His research interests include wireless networks, the Internet of Things, and mobile computing.

![](images/f3c5102b00a20a2b95cec92c8632ed645b62803483b56163a687fac8d8959ca3.jpg)



Shuai Tong received his B.E. degree from Nankai University, Tianjin, in 2019, and his Ph.D. degree from Tsinghua University, Beijing, in 2024. He is currently a post-doctoral researcher at Tsinghua University, Beijing. His research interests include low-power

wide-area networks and the Internet of Things.

![](images/4b64f277e2a10de64d0db0b9d6e2f81ec89a573e845faf05fa12bba47ce7dd51.jpg)



Xiang-Yang Li received his Bachelor's degree from the Department of Computer Science, Tsinghua University, Beijing, in 1995, and his M.S. and Ph.D. degrees from the Department of Computer Science, University of Illinois at Urbana Champaign, in 2000

and 2001, respectively. He is a professor and the executive dean with the School of Computer Science and Technology, University of Science and Technology of China, Hefei. His research interests include Artificial Intelligence of Things (AIoT), privacy and security of AIoT, and data sharing and trading.

![](images/a974348fa5483a6c17d6b02b5c5a10448b6f76ff1ef251b5b606e7cd6c23bfc2.jpg)



Zheng Yang received his B.E. degree in computer science from Tsinghua University, Beijing, in 2006, and his Ph.D. degree in computer science from the Hong Kong University of Science and Technology, Hong Kong, in 2010. He is an associate pro-

fessor with Tsinghua University, Beijing. His main research interests include the Internet of Things and mobile computing.

![](images/7418b5fe0aef448ea57ffee67abd5852f09398f87f12c0cb35ba7bb06a37fa8b.jpg)



Fu Xiao received his Ph.D. degree in computer science and technology from the Nanjing University of Science and Technology, Nanjing, in 2007. He is currently a professor and a Ph.D. supervisor with the School of Computer Science, Nanjing Universi-

ty of Posts and Telecommunications, Nanjing. His main research interests include wireless sensor networks and mobile computing.

![](images/3caf3c1e6109f46eb3c451d6b650bb07cef00049558caaaa6760bdebd07bd391.jpg)



Yun-Hao Liu received his B.S. degree from the Automation Department, Tsinghua University, Beijing, in 1995, his M.A. degree from Beijing Foreign Studies University, Beijing, in 1997, and his M.S. and Ph.D. degrees in computer science and engineering

from Michigan State University, East Lansing, in 2003 and 2004, respectively. He is currently a professor with the Department of Automation and the dean of the Global Innovation Exchange Institute (GIX), Tsinghua University, Beijing.