# Collective Memory for Detecting Nonconcurrent Clones: A Localized Approach for Global Topology and Identity Tracing in IoT Networks

Jing Xu, Kai Xing, Member, IEEE, Chi Zhang, Member, IEEE, Shuo Zhang, Chunlin Zhong,

Haojin Zhu, Senior Member, IEEE, Zheng Yang, Member, IEEE, Yunhao Liu, Fellow, IEEE

Abstract—Clone attack is considered as a severely destructive threat in Internet of Things (IoT), because 1. the attack may be easily launched due to the deficiency of hardware architecture and the limited resources against physical capture and compromise; 2. it may trigger a large variety of insider and outsider attacks.

Different from traditional clone attack detection approaches that ground on a large amount of data traversing the network (e.g., locations, identities), this paper tackles this problem by answering the following fundamental questions: do we really need so much raw information? whether there is an alternative for local event detection by a node far away from that event? when acquiring/tracing global knowledge of a system/network, do we really need a global collection effort? These questions are of much importance in a large variety of networks.

Specifically, this paper provides a collective memory design for global topology and identity tracing (GTI Tracing), via a localized computing paradigm within neighborhood. This localized paradigm computationally builds a connection of identity and topology from time and space domain to a new computation domain. Such a computation domain retains four properties: transitivity, global convergence, determinacy, and causality. With byte-size information at an arbitrary device, it can recover and keep tracing global topology and identity information, and thus providing deterministic detection of clones. Both theoretical analysis and experimental study have shown the advantages of the proposed design in both detection accuracy and privacy protection, at a cost of light communication, storage and computation overhead at each device.

Index Terms—clone attacks, Internet of Things.

# I. INTRODUCTION

N most Internet of Things applications, security provi-I sioning is often envisaged as a fundamental requirement. However, due to the deficiency of system architecture, IoT

This research was partially supported by the National Natural Science Foundation of China (Grand No. 61332004, 61871362, 61972453). (Corresponding Author: Kai Xing)

J. Xu, K. Xing, S. Zhang, Z. Xu and C. Zhong are with the School of Computer Science and Technology, University of Science and Technology of China (email:{jxu125, zshuo, xzhh, chlzhong}@mail.ustc.edu.cn; kxing@ustc.edu.cn)

C. Zhang is with the School of Information Science and Technology, University of Science and Technology of China (email:chizhang@ustc.edu.cn)

H. Zhu is with the Department of Computer Science and Engineering, Shanghai Jiao Tong University (email:zhu-hj@cs.sjtu.edu.cn)

Z. Yang and Y. Liu are with the School of Software, Tsinghua University (email: hmilyyz@gmail.com; yunhao@tsinghua.edu.cn)

Copyright (c) 20xx IEEE. Personal use of this material is permitted. However, permission to use this material for any other purposes must be obtained from the IEEE by sending a request to pubs-permissions@ieee.org.

devices are often vulnerable to physical capture attacks [1]– [3], and have limited protection to preclude an adversary to access the memory, processing, sensing and communication parts. Thus, an IoT device can be easily compromised and replicated at any locations in the network. We usually call such kind of attacking procedure as clone attack (or node replication attack). The clones have the same authority as legitimate nodes, basing on them attackers can launch a large variety of destructive attacks to the network.

It is interesting to observe that most approaches [4]–[7] against clone attacks retain an implicit common ground in the designs: there usually requires a considerable amount of information (IDs, Locations, etc.) collected/traversed throughout the network [8], [9]. If there is any information from two devices in different neighborhood but containing the same ID/feature, an alarm is raised against clone attacks. Therefore, they either rely on extra information, e.g., location/topology information; or launch global data collection for sufficient information for the detection [10].

Generally, existing approaches against clone attacks either relies on centralized designs that may need to collect data from every IoT device, leading to considerable amount of data relays, or ground on decentralized probability based schemes, sometimes with a poor detection accuracy due to deficient information. Besides, most approaches may also impose a high risk of privacy information disclosure during the collection of identity/topology information (e.g., location, identities, links, RSSI, Packet Sequence Number .etc) [11].

However, to launch global data collection in order to detect a local event, e.g. the appearance of a clone, seems too costly in a network. Whether there is an economical alternative for local event detection by a node far away from that event? This question is of much importance in a large variety of networks.

This paper addresses these issues and aims to answer the question: whether there is an economical way for global tracing of identity and topology without a large amount of raw information traversing the network? The answer to this question would be important to IoT and many other network applications.

In this paper, we propose a localized computational paradigm called GTI Tracing (Global Topology and Identity Tracing), for connecting identity and topology from time and space domain to a computation domain. It relies on a concept of collective memory: the consensus of all the nodes on the global knowledge of identities and topology in the network. Specifically, every IoT device launches GTI computation paradigm to compute/update a byte-size result (called chaotic code), and piggy-backs this code within its regular beacon messages to its one-hop neighbors. Since the clones would inevitably generate contradictions in the computation domain, a node could infer when and where the clone attack occurs in the network, if any inconsistence is found within its code(sequence).

GTI Tracing has the following features:

• To the best of our knowledge, GTI Tracing first time provides clone attack detection in a novel computation domain instead of traditional communication paradigms, for global tracing of identity and topology without raw data traversing the network.   
• GTI Tracing first time demonstrates the feasibility that the global information of temporal-spacial connections between identity and topology could be integrated into a byte-size code. Such a localized collective memory design makes it efficient and easy to launch various tasks and be generalized to other decentralized networks.   
• GTI Tracing is capable of tracing identity and topology globally and continuously for a timely and deterministic answer to a series of questions related to ‘What’, ‘When’, and ‘Where’ of a local topological event.

This paper is organized as follows. A brief review of current approaches for clone attack detection is given in Section II. The preliminaries and models are introduced in Section III. The general design principle of GTI Tracing is proposed in IV. We elaborate and accurately prove that our design meets all the required properties in Section V. The detailed description of GTI Tracing based clone attack detection is presented in Section VI, and the security analysis and performance evaluation are reported in Section VII. After that, a brief discussion is provided in Section VIII. Finally, we conclude this paper in Section IX.

# II. RELATED WORK

Various effort has been devoted to defending against clone attack in IoT networks and related fields. [5]–[9], [12]–[15].

A straightforward solution is to monitor the network in a centralized way by collecting the neighborhood information (e.g. location, neighbor list, etc.) from each device by the base station. The existence of a clone attack can be detected if two devices are in different neighborhood devices while having the same ID/feature.

Shaw et al. [16] proposed to detect clone attacks by storing the unique signal characteristic for each device on the BS. However, it is impractical to track the signal characteristics of nodes in a multi-hop communication scenarios in Internet of Things. In localized voting/misbehavior detection schemes [17]–[20], the legitimacy of a given node is agreed/voted based on the local observations of nodes within a neighborhood. Nevertheless, these approaches don’t have the ability to detect clones with normal behavior, and may fail when multiple clones in close proximity collude. Furthermore, localized voting/misbehavior detection schemes are not capable of detecting distributed clones which may appear at any place in the network.

To the best of our knowledge, employing witness nodes for clone attack detection [4] is the first non-naive detection scheme against distributed clone attacks. However, it needs to multicast to selected witness nodes in order to ensure high detection probability, and thus may result in a high communication overhead. Conti et al. [21] proposed an improvement of the Randomized Multicast (RM)RM scheme by optimizing the criteria of witness selection, in which the witness nodes are deterministically selected at each detection round and changed from round to round based on a random number that varies randomly at different rounds. Zhu et al. [22] proposed another criteria for witness selection : location claims are sent to all nodes (witnesses) within a single cell or multiple cells based on a probabilistic function. [23] take a improved LEACH protocol to determine the suitable scale of the sensor cluster and choose the node with higher energy to become a cluster head, then rely on those cluster head to collect messages and detect the replicated nodes. [24] [25] similarly use the node cluster method but accomplish the detection with the sparse characteristics of the cloned nodes. [26] [27] employ random walk to select the witness node(RWND).

Set operations is another effective detection scheme to detect clone attacks. Choi et al. [28] proposed to divide the network into exclusive sub-regions and check if there is any overlapping between them. Note that the length of the messages increases linearly during the report merge along tree structure, the total amount of data to be transferred for membership checking may be considerable high.

Different from all the above strategies, Brooks et al. [29] proposed a centralized detection method in that the base station detects replica attacks at frequency domain based on the random (master) key usage statistics from the network. The result of this scheme heavily relies on the underlying random key establishment scheme [30], in which a random key ring is preloaded to each node and two neighbors share the same key if their key rings have at least one key in common. The following assumption is the basics of the effectiveness of this approach: the number of node pairs that select the same random key is independent and identically distributed. Some alternative solutions such as social fingerprints [31], random walk [32] utilize randomness in another way to detect clones. EDD [33], [34] is a distributed clone detection based on the randomness of encounters and further the discrepancy of the trace between clone and ordinary nodes. [35] proposed two schemes based on the data correlation about continuous holistic queries to against the low quality of sensing devices caused by clone attack in wireless sensor network. HSC-IoT [36] is a physically unclonable function security protocol based on resource-efficient, which could provide a lightweight mutual authentication scheme for the resource-limited devices. Shashidhar [37] first attempted to explore the potential of the epidemic schemes to detect replicas. In [38], an identity mechanism called Zero Knowledge Protocol (ZKP) was proposed for the authentication of sensor nodes.

In the mobility scenarios, XED [34] proposed the first design for clone detection in mobile sensor networks by applying a challenge-and-response strategy. However, it is vulnerable to node collusion. [39] leveraged the intersection of message transmission paths and Sequential Probability Ratio Test to overcome the nodes’ velocities, while in SPRT [40], the Base Station (BS) keeps tracking locations of every node. Both of them applied statistical test by assuming that: the speed of a clone computed according to the information of encounters may exceed the pre-configured speed limit. In TDD [41], the ordinary nodes play the role of the BS by checking the oneway hash chain carried by each encounters. A clone is detected by looking for the inconsistency of the time stamps of the hash chain. MDS approach [42] is a novel location-independent centralized design supporting hybrid (both static and mobile) networks. It adopts multidimensional scaling (MDS) method, in which the BS built a topology map with the collected pairwise distances of all the nodes Since two nodes with the same ID will lead to distortion of the reconstructed map, MDS detects clones in a centralized way without the need to know the geographical location of the victim/clones. In addition, the HIP-HOP [43] approach detected clones in mobile network based on the fact that if two witness nodes were either onehop or two-hop neighbors, then either the witness nodes or the node connecting two witness nodes would find the location conflict of clones. However, the probability of clone detection will be reduced if witness nodes far away from each other.

For storage concerns, Zhang et al. [44] took advantage of double ruling and Bloom filter. Dong et al. [45] proposed LSCD (low-storage clone detection) by launching detection in a non hotspot region. It utilized the remaining energy to create as many detection routes as possible to reduce the storage requirements at each node.

As discussed above, due to the limited detection range by the detectors and the high communication overhead for information collection, the existent schemes have their limitation for detecting clone attacks in Internet of Things. Compared to existent work, GTI Tracing not only achieves deterministic detection, but also provides lower communication/storage overhead. What’s more, global and continuous tracing of identity and topology becomes affordable in the network.

# III. PRELIMINARIES, NETWORK AND SECURITY MODELS

# A. Network Model

In this paper, we focus on loosely synchronized and decentralized IoT networks. The topology of the network is assumed to be stable or change slowly. Namely the nodes in the network either are static or move slowly.

Specifically, the network is modeled as $G ( V , E )$ , where V represents N resource-constrained IoT nodes $\{ 1 , 2 , \cdots , n \}$ , and E represents the links between these nodes. The locations of these nodes are deterministic after deployment.

We further assume that the clocks of all nodes are loosely synchronized [46]–[48]. In particular, $t _ { 1 } , t _ { 2 } , \cdots , t _ { i } , \cdots , t _ { j } , \cdots$ are used to represent the time epochs in the network, where $t _ { i } < t _ { j }$ given $i < j , i , j \in Z ^ { + }$ . During each time epoch t, each node periodically handshake with its one-hop neighbors, in order to keep both being aware of the existence and availability of each other 1.

Let $\mathcal { N } ( u )$ denote the neighborhood of $u .$ For any two arbitrary neighboring nodes u and v, we can infer that $\mathcal { N } ( u )$ and $\mathcal { N } ( v )$ are different $( \mathcal { N } ( u ) \neq \mathcal { N } ( v ) )$ since $u \not \in \mathcal { N } ( u )$ but $u \in \mathcal { N } ( v )$ and $v \not \in \mathcal { N } ( v )$ but $v \in \mathcal { N } ( u )$ .

# B. Security Model

In this paper, we assume that IoT devices are not tamperresistant [49]. All the security information of a compromised or captured device could be released to the attacker. The attackers can replicate the compromised node, and distribute the clones throughout the network. Note that the cloned nodes contain all the legitimate information of the compromised node (e.g. ID, keys, code, etc.). Thus the clones and legitimate nodes have the same legitimacy to participate in the network operation.

According to the existent work against clone attacks [4], [28], [42], it is usually assumed that it is difficult for the attacker to create new legitimate security information (keys, codes, etc.). We adopted the same assumption that new IDs and certificated information for clones cannot be created by the adversary.

Particularly, this paper focuses on the scenarios of continuously monitoring. This is based on two perceptions in practice: 1. attacks occur endlessly, not just once; 2. a late detection is usually meaningless. Therefore, we assume that the whole network is continuously monitored for a timely detection of attacks.

# C. Notations and Illustrations

Before deployment, each node i is initialized with a group of unique number $A _ { i } = \{ a _ { i } ^ { 0 } , a _ { i } ^ { 1 } , . . . , a _ { i } ^ { t } \}$ , and a unique chaotic code $\bar { x _ { i } ^ { 0 } } .$ , where $a _ { i } ^ { k } , x _ { i } ^ { 0 } \in \bar { R } ^ { + } , i \in \{ \bar { 0 } , . . . , t \}$ . Specifically, we set $\begin{array} { r } { a _ { i } ^ { t } \dot { = } \frac { 1 } { \sqrt { q _ { i } ^ { t } } } , x _ { i } ^ { 0 } \dot { = } p _ { i } . } \end{array}$ , where both $p _ { i }$ and $q _ { i } ^ { t }$ are unique prime numbers, and $\forall a _ { i } ^ { t } \in A \ q _ { i } ^ { t } > n ^ { 2 }$ .

We also require A be linearly independent over the field of rational numbers Q, which means none of the element $a _ { i } ^ { t } \in A$ can be written as a linear combination of the other numbers in the collection with rational coefficients. The proof of $A \ ' \mathrm { s }$ rational independence is provided later in Section V.

After deployment, node i first registers itself to its neighborhood. Then at each time epoch $t ,$ it piggybacks the following information, its chaotic code $\ v x _ { i } ^ { t }$ and the codes ${ x _ { j \in \mathcal { N } ( i ) } ^ { t - 1 } }$ received at last time epoch, in its beacon messages with signed signature $S i g _ { i }$ , as shown in the following,

$$
i \to \mathcal {N} (i): \{I D _ {i}, x _ {i} ^ {t}, x _ {j \in \mathcal {N} (i)} ^ {t - 1}, S i g _ {i} \}
$$

This procedure helps keeping each node posted with the code information within two hops. Therefore, each node i has to faithfully compute and report its chaotic code to its one-hop neighbors.

Let $\ v x _ { i } ^ { t }$ represent the chaotic code of node i at time epoch t, we have

$$
X _ {i} = \{x _ {i} ^ {0}, x _ {i} ^ {1}, \dots , x _ {i} ^ {t} \}
$$

1beacon mechanism is commonly available in a large variety of networks for periodically notifications/advertisements

represents the chaotic code sequence of node i from time epoch 0 to time epoch t, and

$$
X ^ {t} = \{x _ {1} ^ {t}, x _ {2} ^ {t}, \dots , x _ {n} ^ {t} \}
$$

represents the chaotic codes of all the nodes at time epoch t in G(V, E).

Given a network of n nodes, let ${ \cal S } = \{ s _ { 1 } , s _ { 2 } , \ldots \}$ denote the phase space, and $s _ { i }$ denote a point in the phase space representing the state of the network topology and corresponding codes at each node. When the topology changes from state $s _ { j }$ to state $s _ { j + 1 }$ at time epoch $t _ { 1 } .$ the chaotic code $X _ { i }$ of node i would transit from a stable state with code $\boldsymbol { x } _ { i } ^ { t _ { 1 } }$ to a new state (when adding or removing a node/link), then converges to a stable state again with a new code $x _ { i } ^ { t _ { 2 } }$ , as shown in the following,

$$
X ^ {t _ {1}} \xrightarrow {x _ {i} ^ {t _ {1}} \rightarrow x _ {i} ^ {t _ {2}}} X ^ {t _ {2}} \tag {1}
$$

To further illustrate the process, we let $F ( X ^ { t } )$ be a deterministic nonlinear function of the global chaotic code state transition of Xt, where $X ^ { t } = ( x _ { 1 } ^ { t } , \bar { x _ { 2 } ^ { t } } , . . . , x _ { n } ^ { t } )$ , where

$$
X ^ {t + 1} = F (X ^ {t}) \tag {2}
$$

$$
= F (x _ {1} ^ {t}, x _ {2} ^ {t},..., x _ {n} ^ {t}) \tag {3}
$$

$$
= \left\{x _ {1} ^ {t + 1}, x _ {2} ^ {t + 1},..., x _ {n} ^ {t + 1} \right\} \tag {4}
$$

where

$$
x _ {i} ^ {t + 1} = f (x _ {j \in \mathcal {N} (i)} ^ {t}) \tag {5}
$$

Then we have

$$
F (X ^ {t}) = F (x _ {1} ^ {t}, x _ {2} ^ {t},..., x _ {n} ^ {t}) \tag {6}
$$

$$
= \{f (x ^ {t} (\mathcal {N} _ {1})), f (x ^ {t} (\mathcal {N} _ {2})),..., \tag {7}
$$

$$
\left. f \left(x ^ {t} \left(\mathcal {N} _ {n}\right)\right) \right\} \tag {8}
$$

# D. Node Model

In this section, we model each node in the network as a neuron. The course of the action response of each node to outside stimulus, can be divided into two parts: the rising stimulus stage, the falling stage. During the rising stimulus stage, the output of the node goes beyond 1. Subsequent to this, there is a falling stage with the output less than 1.

Particularly, we have the following definitions

Local Convergence: The difference of two adjacent chaotic codes of a node $\bar { \boldsymbol { i } } , | \boldsymbol { x } _ { i } ^ { t + 1 } - \boldsymbol { x } _ { i } ^ { t } |$ , reaches  convergence (namely $| x _ { i } ^ { t + 1 } - x _ { i } ^ { t } | < \epsilon )$ .

Global Convergence: Every node in the network has reached local convergence.

We further provide the status definition of a node:

• Stable State: a node enters into the stable state if it reaches local convergence (namely $\lvert x _ { i } ^ { t + 1 } - x _ { i } ^ { t } \rvert < \epsilon )$ .

• Disturbed State: a node could enter into the disturbed status at time epoch t if both conditions hold: 1. this node was under stable state at previous time epoch t − 1; and 2. there is a topological change around node i (i.e.,

node/edge addition/deletion in $\mathcal { N } ( i ) )$ , or there is a code in $X _ { j \in \mathcal { N } ( i ) } ^ { t }$ is larger than 1, at time epoch t.

Remark: In the stable state, a node is sensitive to outside stimulus, i.e., entering into the rising stimulus stage. While in the falling stage, a node will be no longer sensitive to outside stimulus, i.e., staying in the falling stage.

Particularly, in order to facilitate the mathematical modeling, we introduce the following functions.

• Node-wise Reciprocal Generation:

$$
\text {   If   } x _ {i} ^ {t - 1} > 1 \text {:   } w _ {i} ^ {t} = \frac {1}{x _ {i} ^ {t - 1}};
$$

$$
\text {   If   } x _ {i} ^ {t - 1} <   1 \text {:} w _ {i} ^ {t} = x _ {i} ^ {t - 1}
$$

• Pseudo-Geometric Neighborhood Mean: the pseudogeometric mean value of the neighborhood codes in N (i):

$$
\mu_ {i} ^ {t} = (\prod_ {j \in \mathcal {N} (i)} w _ {j} ^ {t}) ^ {a _ {i} ^ {t}}
$$

# IV. GTI TRACING DESIGN: GLOBAL TOPOLOGY AND IDENTITY TRACING

In this section, we introduce the design of Global Topology and Identity Tracing (GTI Tracing), for connecting identity and topology from time and space domain to a computation domain.

# A. Design Principles

Note that the global knowledge of identities and topology is the key to clone detection. Specifically, we adopt four properties: transitivity, global convergence, determinacy, and causality in our design. These four properties ensure the causal association of the mapping between the local chaotic code x and a unique state s of the network in the phase space S, in which s retains the global knowledge of identity and topology.

• Transitivity: Any topology change at an arbitrary position in a network under global convergence, will result in a disturbance (spike) of the chaotic codes of the nodes around that position. This disturbance (spike) will further lead to code spikes of the neighbors of these nodes, and repeatedly spread over the network. Eventually this will break the stable state of all the nodes in the network, which mimics a butterfly effect.

• Global Convergence: During the spread of code spikes (butterfly effect in the network), once a node breaks its stable state, its chaotic code will soon converges, and reenter into a new stable state.

• Determinacy: Given the global knowledge of a network under global convergence, any topology change causes a deterministic change of the chaotic code at each node.

• Causality: Given a state s under global convergence (the global knowledge of topology and code), different topological changes result in different non-overlapping traces in the phase space S, so do the local chaotic code sequences. That is, there is a one-to-one correspondence between the topological change and the code (sequence). Namely different causes (topological changes) lead to different results (codes).

# B. Building Blocks of GTI Tracing

In the following, we introduce the basic modules of GTI Tracing: Disturbance Amplification Module, and Convergence Module.

1) Disturbance Amplification Module: The Disturbance Amplification Module is designed for ensuring the transitivity property of GTI Tracing, and guarantees that any topological change should result in a butterfly effect (code spikes) spreading over the network.

Considering an arbitrary node i under the Stable State, once there is a topological change around node i at time epoch t−1 $( \mathrm { i . e . }$ , node/link addition/deletion in $\mathcal { N } ( i ) )$ , or there is a code ${ \boldsymbol { x } } _ { j \in \mathcal { N } ( i ) } ^ { t - 1 }$ that is larger than 1, node i would enter the Disturbed State from the Stable State. Specifically, it will execute the Disturbance Amplification Module just once at time epoch t, as shown in the following.

• Step 1. Status Estimation: If $\exists x _ { j \in N ( i ) } ^ { t - 1 } > 1$ xt−1j∈N (i) > 1, or N (i)t 6= $\mathcal { N } ( i ) ^ { t } \neq$ $\mathcal { N } ( i ) ^ { t - 1 }$ , then the status of node i would enter into the Disturbed State, else let $x _ { i } ^ { t } = x _ { i } ^ { t - 1 }$ and go back to Step 1 at next time epoch.   
• Step 2. Node-wise Reciprocal Generation:

$$
\text {   If   } x _ {j} ^ {t - 1} > 1 \text {:   } w _ {i} ^ {t} = \frac {1}{x _ {i} ^ {t - 1}};
$$

$$
\text {   If   } x _ {j} ^ {t - 1} <   1 \text {:} w _ {i} ^ {t} = x _ {j} ^ {t - 1}
$$

• Step 3. Pseudo-Geometric Neighborhood Mean: the pseudo-geometric mean value of the neighborhood codes in $\bar { \mathcal { N } } ( i ) \bar { : } \mu _ { i } ^ { t } = ( \prod _ { i \ldots i } w _ { j } ^ { t } ) ^ { a _ { i } ^ { t } }$ j∈N (i)

• Step 4. Spike Generation: Compute $\begin{array} { r } { x _ { i } ^ { t } = \frac { 1 } { \mu _ { i } ^ { t } } } \end{array}$ 1µt . Since the iPseudo-Geometric Neighborhood Mean is in the range (0, 1), the output $\ v x _ { i } ^ { t }$ must be larger than 1.

• Step 5. Quit and enter into the Convergence Module.

After the execution of the Disturbance Amplification Module, the newly updated code of node i at time epoch $t , \ x _ { i } ^ { t } .$ , must be larger than 1. Namely, node i generates a spike code to its neighbors at time epoch t, which again spreads via the beacon scheme to node i’s neighbors.

The design philosophy is: any spike triggered by a topological change or a neighborhood code spike, should be able to lead to spikes to those neighboring nodes under the Stable State, and repeatedly spread over the network and breaks the stable states of all other nodes. This procedure leads all the nodes quitting from the Stable State and entering the Disturbed State, which mimics a butterfly effect.

Remark: Every node under the Stable State executes the Disturbance Amplification Module only once, and then enters to the Convergence Module.

2) Convergence Module: The Convergence Module ensures the convergence property of GTI Tracing. Once after deployment or quit from the stable state, each node i in the network would repeatedly launch the Convergence Module until convergence.

• Step 1. Node-wise Reciprocal Generation:

$$
\text {   If   } x _ {j} ^ {t - 1} > 1 \text {:   } w _ {i} ^ {t} = \frac {1}{x _ {i} ^ {t - 1}};
$$

$$
\text {   If   } x _ {j} ^ {t - 1} <   1 \text {:} w _ {i} ^ {t} = x _ {j} ^ {t - 1}
$$

• Step 2. Pseudo-Geometric Neighborhood Mean: the pseudo-geometric mean value of the neighborhood codes in $\mathcal { N } ( i ) \dot { : } \mu _ { i } ^ { t } = ( \quad \prod \quad w _ { j } ^ { t } ) ^ { a _ { i } ^ { t } }$ j∈N (i)

• Step 3. Code Update: If $x _ { i } ^ { t - 1 } < 1$ , and $| x _ { i } ^ { t } - x _ { i } ^ { t - 1 } | < \epsilon$ , let $x _ { i } ^ { t } = x _ { i } ^ { t - 1 }$ (namely Local Convergence), otherwise $x _ { i } ^ { t } = \mu _ { i } ^ { t }$ .

• Step 4. Global Convergence Estimation: Repeat step $1 \mathrm { ~ - ~ } 3$ at next time epoch. If the code reaches Local Convergence for D continuous time epochs, where D is related to the diameter of the network, the status of node i is changed from the Disturbed State to the Stable State, and quit from Convergence Module.

The following provides a brief illustration indicating how the module leads to convergence. Detailed proof will be given later.

Without the loss of generality, suppose all the neighbors of node i are already in the Disturbed State at time epoch $t - 1$ . Note that their codes must be in the range (0, 1) at next time epoch t.

At time epoch (0, 1) $t + 1$ , since every code $\boldsymbol { x } _ { j \in \mathcal { N } ( i ) } ^ { t }$ is in the i would be in the range (0, 1) again. As time proceeds, the code of node i produced from the Convergence Module would converge to some value (complete and detailed proof is in codes of a node i, |xt+1i − xti|, would be less than , which Section V). Namely the difference of two consecutive chaotic $i , \ \lvert x _ { i } ^ { t + 1 } - x _ { i } ^ { t } \rvert$ means node i enters into local convergence.

# C. GTI Tracing: Global Topology and Identity Tracing

This section introduces the complete computation paradigm of GTI Tracing, as shown in Fig.1.

Right after deployment, every node j begins periodical beaconing to its neighborhood $\mathcal { N } ( j )$ , in which it piggybacks its chaotic code $x _ { j } .$ . Similarly, node i may receive the chaotic codes of $x _ { j } { \mathrm { ~ i f ~ } } j \in { \mathcal { N } } ( i )$ .

At each time epoch t, after $i \in \mathcal { N } ( j )$ receives $j ^ { \circ } \mathrm { s }$ beacon, it first verifies the authenticity of the message. If the message passes the authenticity check, node i will update its code with xt+1 a $\bar { \boldsymbol { x } } _ { i } ^ { t + 1 }$ t the next time epoch $t + 1$ , as shown in the following GTI Tracing Algorithm.

Fig.1 provides a brief illustration indicating how GTI tracing design leads to disturbance and convergence. Detailed proof will be given later in Section V.

Specifically, given a node i under the Stable State, once there is a disturbance in $\mathcal { N } ( i )$ , node i would enter into the Disturbed State from the Stable State, and launch the Disturbance Amplification Module for just once.

After the execution of the Disturbance Amplification Module, node i will repeatedly launch the Convergence Module until convergence. According to the GTI Tracing algorithm, node i repeatedly updates its chaotic code based on the pseudogeometric neighborhood mean $\mu _ { i } ^ { t }$ , until $| x _ { i } ^ { t + 1 } - x _ { i } ^ { t } | < \epsilon$ for continuous D time epochs.

Particularly, whe n |xt+1i $| x _ { i } ^ { t + 1 } - x _ { i } ^ { t } | < \epsilon$ for continuous D time epochs, we will fix $\boldsymbol { x } _ { i } ^ { t + 1 } ~ = ~ \boldsymbol { x } _ { i } ^ { t }$ , in order to speedup the convergence.

Algorithm 1 GTI Tracing Algorithm   
Require: $x_{i}^{t}$ , each node i's code at time epoch t; $X_{\mathcal{N}(i)}^{t}$ , all the code of node $i'$ neighborhood;
1: Initialization: node i is initialized to Stable State.
2: while $t \geq 0$ do
3: if Status Estimation = Disturbed State then
4: Disturbance Amplification Module.
5: t=t+1
6: while Convergence Estimation ≠ Stable State do
7: Convergence Module
8: t=t+1
9: end while
10: Continue
11: end if
12: t=t+1
13: end while

![](images/ffa1833ab2d5bf8a7dd13a5669e2dde2a0e75393ed6ff6ce14946dcdcb9c713b.jpg)



Fig. 1: GTI Tracing Computation Algorithm

# V. THEORETICAL ANALYSIS OF GTI TRACING ALGORITHM

In this section, we conduct theoretical analysis on the four properties of GTI Tracing: transitivity, convergence, determinacy, and causality.

# A. Transitivity, Convergence and Determinacy

Theorem V.1. Transitivity: Given a connected network $G ( V , E )$ under global convergence, if there is a topological change at an arbitrary place (without breaking the network connectivity), the proposed GTI Tracing design will lead to code spikes spreading to all the nodes under the Stable State, mimicking a butterfly-effect.

Proof. Given a connected network $G ( V , E )$ under global convergence, namely all the nodes are under the Stable State and keep running the state estimation step of the Disturbance Amplification Module.

Suppose there is a topological change (node/edge addition/deletion) in the neighborhood of node i at time epoch $t - 1$ . Obviously, due to the topological change, the neighbor set $\mathcal { N } ( i )$ at time epoch t must be different from that at time epoch $t - 1$ .

Therefore, according to GTI Tracing design, node i must enter into the Disturbed State and begin to run the Disturbance Amplification Module for just once. Therefore node i will generate a spike code at time epoch t, i.e., $x _ { i } ^ { t } > 1$ .

This spike code will further be heard by the neighbors in $\mathcal { N } ( i )$ via the beacon scheme. According to GTI Tracing design, this spike code would further lead the nodes in $\mathcal { N } ( i )$ changing status to the Disturbed State from the Stable State. Similarly, this procedure would repeatedly lead to spikes in $\mathcal { N } ( i )$ and again in $\mathcal { N } ( \mathcal { N } ( i ) )$ , and so on, until all the nodes in the network change status to the Disturbed State from the Stable State. Namely the proposed GTI Tracing design leads to code spikes spreading to all the nodes under the Stable State, mimicking a butterfly effect. □

Lemma V.1. The code $\ v x _ { i } ^ { t }$ of any node i at any time epoch t could be represented in the form $p _ { 1 } ^ { \alpha _ { 1 } } p _ { 2 } ^ { \alpha _ { 2 } } . . . p _ { n } ^ { \alpha _ { n } }$ , and $\alpha _ { i }$ is an algebraic number, where $p _ { i }$ is a unique prime number associated with node i during initialization.

Proof. Based on GTI Tracing, we propose the generic form of the code value of each node by mathematical induction.

base case: During initialization, each node i is initialized with $x _ { i } ^ { 0 } = p _ { i }$ , obviously the proposition holds in this case with $\alpha _ { i } = 1$ .

inductive step: Without loss of generality, we assume the proposition holds for $\ v x _ { i } ^ { t }$ . Next we are going to prove by induction for xt+i $\boldsymbol { x } _ { i } ^ { t + 1 }$

According to the GTI Tracing process, at time epoch t, the code of each node could be represented in the form $p _ { 1 } ^ { \alpha _ { 1 } } p _ { 2 } ^ { \alpha _ { 2 } } . . . p _ { n } ^ { \alpha _ { n } }$ .

Considering an arbitrary node i at the time epoch $t + 1$ , we have

$$
x _ {i} ^ {t + 1} = (\prod_ {j \in \mathcal {N} (i)} w _ {j} ^ {t}) ^ {a _ {i} ^ {t + 1}}
$$

, where $\begin{array} { r } { a _ { i } ^ { t + 1 } = \frac { 1 } { \sqrt { q _ { i } ^ { t + 1 } } } , q _ { i } ^ { t + 1 } } \end{array}$ ai √ √ q t +1i , q i is a unique prime number larger than n2. Since the wtj is of the form of xtj = pα1j1 pα22 $n ^ { 2 }$ $\dot { w } _ { j } ^ { t }$ $x _ { j } ^ { t } = p _ { 1 } ^ { \alpha _ { 1 j } } p _ { 2 } ^ { \alpha _ { 2 j } } . . . p _ { n } ^ { \alpha _ { n j } }$ α2j αnj or its reciprocal $\textstyle { \frac { 1 } { x _ { j } ^ { t } } }$ , with the characteristic function

$$
\delta_ {i} ^ {t} = \left\{ \begin{array}{l l} 0 & x _ {i} ^ {t} \leq 1 \\ 1 & x _ {i} ^ {t} > 1 \end{array} \right.
$$

we have

$$
\begin{array}{l} x _ {i} ^ {t + 1} = (\prod_ {j \in \mathcal {N} (i)} (w _ {j} ^ {t})) ^ {a _ {i} ^ {t + 1}} \\ = (\prod_ {j \in \mathcal {N} (i)} (x _ {j} ^ {t}) ^ {(- 1) ^ {\delta_ {j} ^ {t}}}) ^ {a _ {i} ^ {t + 1}} \\ = (\prod_ {j \in \mathcal {N} (i)} p _ {1} ^ {(- 1) ^ {\delta_ {j} ^ {t}} \alpha_ {1 j} ^ {t}} p _ {2} ^ {(- 1) ^ {\delta_ {j} ^ {t}} \alpha_ {2 j} ^ {t}} \dots p _ {n} ^ {(- 1) ^ {\delta_ {j} ^ {t}} \alpha_ {n j} ^ {t}}) ^ {\alpha_ {i} ^ {t + 1}} \\ = \prod_ {j \in \mathcal {N} (i)} p _ {1} ^ {(- 1) ^ {\delta_ {j} ^ {t}} a _ {i} ^ {t + 1} \alpha_ {1 j} ^ {t}} p _ {2} ^ {(- 1) ^ {\delta_ {j} ^ {t}} a _ {i} ^ {t + 1} \alpha_ {2 j} ^ {t}} \dots p _ {n} ^ {(- 1) ^ {\delta_ {j} ^ {t}} a _ {i} ^ {t + 1} \alpha_ {n j} ^ {t}} \\ \begin{array}{r l r} & {\frac {\sum_ {j \in \mathcal {N} (i)} (- 1) ^ {\delta_ {j} ^ {t}} \alpha_ {1 j}}{\sqrt {q _ {i} ^ {t + 1}}}} & {\frac {\sum_ {j \in \mathcal {N} (i)} (- 1) ^ {\delta_ {j} ^ {t}} \alpha_ {2 j}}{\sqrt {q _ {i} ^ {t + 1}}} \dots p _ {n} \frac {\sum_ {j \in \mathcal {N} (i)} (- 1) ^ {\delta_ {j} ^ {t}} \alpha_ {n j}}{\sqrt {q _ {i} ^ {t + 1}}}} \\ & {= p _ {1}} & \end{array} \\ \end{array}
$$

Since $\alpha _ { k j } ^ { t } , k \in \{ 1 , . . . n \}$ is an algebraic number, the summation of these algebraic numbers $\sum _ { j \in \mathcal { N } ( i ) } \alpha _ { k j } , k \in \{ 1 , 2 , . . . , n \}$ would also be an algebraic number. Similarly, the product of $a _ { i } ^ { t + 1 } ( \mathrm { i . e . , } \frac { 1 } { \sqrt { q _ { i } ^ { t + 1 } } } )$ ai and an algebraic number is also an algebraic number. Therefore, ai $a _ { i } ^ { t + 1 } \sum _ { j \in \mathcal { N } ( i ) } \alpha _ { k j } , k \ \in \ \{ 1 , 2 , . . . , n \}$ is an j∈N (i) algebraic number. Let $\alpha _ { j } ^ { t + 1 }$ denote this algebraic number. We have

$$
x _ {i} ^ {t + 1} = p _ {1} ^ {\alpha_ {1 j} ^ {t + 1}} p _ {2} ^ {\alpha_ {2 j} ^ {t + 1}} \dots p _ {n} ^ {\alpha_ {n j} ^ {t + 1}}
$$

Note that node i is an arbitrary node in the network. By induction, the code of any node i at any time epoch $t { + } 1$ could be represented in the form $p _ { 1 } ^ { \alpha _ { 1 } } p _ { 2 } ^ { \alpha _ { 2 } } . . . p _ { n } ^ { \alpha _ { n } }$ , where $p _ { i }$ is a unique prime number associated with node i during initialization, and $\alpha _ { i }$ is an algebraic number. □

![](images/f37ceefd84baa1393cabb6d1ee0551bae4dfc1cd0361293f42be1a3047e5709a.jpg)



Fig. 2: A standard example of disturbance propagation path

Lemma V.2. Given the network G(V,E) under global convergence, suppose v is a node in the neighborhood of the source node u of the disturbance at time epoch $t _ { 0 } .$ . Given an arbitrary node i who retains the initial knowledge of the network, with its current chaotic code in the form $x _ { i } ^ { t } = { p } _ { 1 } ^ { \alpha _ { 1 i } ^ { t } } { p } _ { 2 } ^ { \alpha _ { 2 i } ^ { t } } . . . { p } _ { n } ^ { \alpha _ { n i } ^ { t } } , \alpha _ { l i } ^ { t }$ αt2i could be expressed with a linear combination of the products of $\begin{array} { r } { \dot { \mathbf { \xi } } a _ { j } ^ { t _ { k } } \ ( i . e . , \frac { \mathbf { \xi } _ { 1 } } { \sqrt { q _ { j } ^ { t _ { k } } } } ) , \ : l , j \in n , t _ { k } \in \{ t _ { 0 } , . . . , t \} } \end{array}$ q t kj .

Proof. To illustrate the combinatorial arrangement of the elements $a _ { j } ^ { k } \in A$ in the exponent parts of code $\mathit { x } _ { i } ^ { t } ,$ , we expand $\ v x _ { i } ^ { t }$ as

$$
\begin{array}{l} x _ {i} ^ {t} = p _ {1} ^ {\alpha_ {1 i} ^ {t}} p _ {2} ^ {\alpha_ {2 i} ^ {t}} \dots p _ {n} ^ {\alpha_ {n i} ^ {t}} \\ = (\prod_ {j \in \mathcal {N} (i)} (w _ {j} ^ {t - 1})) ^ {a _ {i} ^ {t}} \\ = \prod_ {j \in \mathcal {N} (i)} p _ {1} ^ {(- 1) ^ {\delta_ {j} ^ {t - 1}} a _ {i} ^ {t} \alpha_ {1 j} ^ {t - 1}} p _ {2} ^ {(- 1) ^ {\delta_ {j} ^ {t - 1}} a _ {i} ^ {t} \alpha_ {2 j} ^ {t - 1}} \dots p _ {n} ^ {(- 1) ^ {\delta_ {j} ^ {t - 1}} a _ {i} ^ {t} \alpha_ {n j} ^ {t - 1}} \\ \end{array}
$$

According to the above, taking the topology of Figure 2 as an example, for each base number $p _ { l } .$ , we expand its exponent α tl i $\alpha _ { l i } ^ { t }$ as

$$
\begin{array}{l} \alpha_ {l i} ^ {t} = a _ {i} ^ {t} \sum_ {j \in \mathcal {N} (i)} (- 1) ^ {\delta_ {j} ^ {t - 1}} \alpha_ {l j} ^ {t - 1} \\ = a _ {i} ^ {t} \sum_ {j \in \mathcal {N} (i)} ((- 1) ^ {\delta_ {j} ^ {t - 1}} a _ {j} ^ {t - 1} \sum_ {k \in \mathcal {N} (j)} ((- 1) ^ {\delta_ {k} ^ {t - 2}} a _ {k} ^ {t - 2} \\ \dots a _ {z} ^ {t _ {0} + 2} \sum_ {v \in \mathcal {N} (z)} ((- 1) ^ {\delta_ {v} ^ {t _ {0} + 1}} a _ {v} ^ {t _ {0} + 1} (\sum_ {h \in \mathcal {N} (v)} \alpha_ {h} ^ {t _ {0}} - \alpha_ {u} ^ {t _ {0}}))) \tag {9} \\ \end{array}
$$

which is a linear combination of the products of $a _ { j } ^ { t _ { k } }$ atj $( \mathrm { i . e . , } \frac { 1 } { \sqrt { q _ { j } ^ { t _ { k } } } } ) , l , j \in n , t _ { k } \in \{ t _ { 0 } , . . . , t \}$ . Proof completes. q q t kj

□

Theorem V.2. Convergence: Given a connected network $G ( V , E )$ under global convergence, and a topological change at an arbitrary place (without breaking the network connectivity), the proposed GTI Tracing design could eventually lead the network to global convergence again, namely the codes of all the nodes in $G ( V , E )$ would re-converge to the Stable State.

Proof. Given a connected network $G ( V , E )$ under global convergence, note that any topological change would result in spikes throughout the network. Given an arbitrary node i, suppose a while after the topological change, node i has been disturbed and begins launching the Convergence Module.

During the execution of Convergence Module in Section IV-B, its chaotic code must be in the range (0, 1). According to Lform $x _ { i } ^ { t } = p _ { 1 } ^ { \alpha _ { 1 } ^ { t } } p _ { 2 } ^ { \alpha _ { 2 } ^ { t } } . . . p _ { n } ^ { \alpha _ { n } ^ { t } }$ ume its code is characterized . Without loss of generality, let $\alpha _ { m a x } ^ { t }$ denote the absolute value of exponent with the largest absolute value among all the numbers in $\{ \alpha _ { 1 } ^ { t } , \alpha _ { 2 } ^ { t } , \cdot \cdot \cdot , \alpha _ { n } ^ { t } \}$ . Namely,

$$
\alpha_ {m a x} ^ {t} = \max \| \alpha_ {i} ^ {t} \|, i \in 1, 2, \dots , n
$$

Note that the code $x _ { i } ^ { t + 1 } = p _ { 1 } ^ { \alpha _ { 1 } ^ { t + 1 } } p _ { 2 } ^ { \alpha _ { 2 } ^ { t + 1 } } . . . p _ { n } ^ { \alpha _ { n } ^ { t + 1 } }$ αt+11 p 22t+1 αt+1 αt+1 , considering arbitrary exponential component $\alpha _ { k } ^ { t + \overline { { 1 } } }$ αk , we have

$$
| \alpha_ {k} ^ {t + 1} | = | \frac {1}{\sqrt {q _ {i} ^ {t + 1}}} \sum_ {j \in \mathcal {N} (i)} \delta_ {k} ^ {t} \alpha_ {k} ^ {t} | <   \frac {n \times \alpha_ {m a x} ^ {t}}{\sqrt {q _ {i} ^ {t + 1}}} <   \alpha_ {m a x} ^ {t}
$$

, given that all the elements $q _ { i } ^ { t }$ is greater than $n ^ { 2 }$ .

This indicates that $\alpha _ { m a x } ^ { t + 1 }$ continuously shrinks from $\alpha _ { m a x } ^ { t }$ during the execution of Convergence Module. As the gap between $\ v x _ { i } ^ { t }$ and $\boldsymbol { x } _ { i } ^ { t + 1 }$ becomes narrower, node i will reach the termination condition of local convergence.

Note that node i is an arbitrary node in the network. After every node i in the network reaches local convergence, the network reaches global convergence, namely the Stable State.

![](images/022e6b7e3c7bcd6ba22b510c14918ccaa713378a0540087899eb226fa8c551a4.jpg)

Theorem V.3. Determinacy: GTI Tracing is a deterministic computation process, i.e., under the same initialization setting, given the same specific input, GTI Tracing always return the same result.

Proof. According to the GTI Tracing design proposed in Subsection $\mathrm { I V - C } ,$ since all the functions in GTI Tracing are injective one-to-one functions, no matter whether there is topological change or not, the current state of the network determines the next state it will be.

Therefore, under the same initialization setting and the same specific disturbance (i.e., topological changes), GTI Tracing would always return the same result. Besides, the evolution process always evolves along the same sequence of states in the phase space S (namely the course in the phase space).

# B. Causality

In this section, we introduce several Lemmas before discussing causality.

Lemma V.3. Let $\{ p _ { 1 } , p _ { 2 } , . . . , p _ { n } \}$ be unique prime numbers, $\{ \log ( p _ { 1 } ) , \log ( p _ { 2 } ) , . . . , \log ( p _ { n } ) \}$ are linearly independent over $\mathbb { Q } ,$ that is, $i f \left\{ c _ { 1 } , c _ { 2 } , . . . , c _ { n } \right\}$ are rational numbers with

$$
c _ {1} \log (p _ {1}) + c _ {2} \log (p _ {2}) + \dots + c _ {n} \log (p _ {n}) = 0
$$

then $c _ { 1 } = c _ { 2 } = \ldots = c _ { n } = 0 .$

Proof. If $\sum _ { i = 1 } ^ { n } c _ { j } \log ( p _ { j } ) = 0$ then $\sum _ { j = 1 } ^ { n } y _ { j } \log ( p _ { j } ) = 0$ where j=1 $y _ { j } \in \mathbb { Z }$ is the product of $c _ { j }$ and the largest common denominator of $\{ c _ { 1 } , c _ { 2 } , . . . , c _ { n } \}$ .

Therefore the condition of the lemma could be rewritten as $\log ( \prod _ { j = 1 } ^ { n } p _ { j } ^ { y _ { j } } ) = 0$ , which implies $\sum _ { i = 1 } ^ { n } p _ { j } ^ { y _ { j } } = 1$ p j . Note that it is j=1 j=1 only possible when $y _ { j } = 0$ for all $j .$ Indeed, we have

$$
\sum_{\substack{1\leq j\leq n\\ y_{j}\geq 0}}p_{j}^{y_{j}} = \sum_{\substack{1\leq i\leq n\\ y_{j} <   0}}p_{i}^{y_{i}}
$$

According to the uniqueness, and the prime property, this decomposition implies $y _ { j } = 0$ for all $j .$ Namely $c _ { 1 } = c _ { 2 } =$ $\ldots = c _ { n } = 0$ .

Lemma V.4. Given $\{ p _ { 1 } , p _ { 2 } , . . . p _ { n } \}$ be different integers $>$ 1, squarefree and pairwise relatively prime, then the set $\{ { \sqrt { p _ { 1 } } } , { \sqrt { p _ { 2 } } } , \ldots { \sqrt { p _ { n } } } \}$ are linearly independent over the field of rational Q.

Proof. We will prove more general that as a vector space, the dimension of the field extension gotten from Q, by adjoining the square roots of n integers > 1 which are squarefree and pairwise relatively prime, is $2 ^ { n }$ . Proceed by induction on the number of such integers adjoined.

Obviously this proposition works for $n = 1$ and $n = 2 .$ .

Assume it works for 1, 2, ..., n roots. Let $\{ p _ { 1 } , p _ { 2 } , . . . , p _ { n } , p _ { n + 1 } \}$ be such a set of $n + 1$ integers. Let us use the letters E and F to represent the following fields:

$$
E = \mathbb {Q} (\sqrt {p _ {1}},..., \sqrt {p _ {n - 1}})
$$

$$
F = E (\sqrt {p _ {n}})
$$

By induction, d $\operatorname { l i m } ( E ) ~ = ~ 2 ^ { n - 1 }$ and $\dim ( F ) \ : = \ : 2 ^ { n }$ . We would be done with the proof if we could show that $\sqrt { p _ { n + 1 } }$ is not an element of F .

Assume otherwise, that $\sqrt { p _ { n + 1 } }$ is in F . Then for some $a , b$ in $E ,$ we can write:

$$
\sqrt {p _ {n + 1}} = a + b * \sqrt {p _ {n}}
$$

Squaring both sides gives:

$$
p _ {n + 1} = a ^ {2} + 2 * a * b * \sqrt {p _ {n}} + b ^ {2} * p _ {n}
$$

$$
\mathrm{or} 2 * a * b * \sqrt {p _ {n}} = p _ {n + 1} - a ^ {2} - b ^ {2} * p _ {n}
$$

The righthand side lies in E. Three cases are possible:

1) $a \ = \ 0 :$ Then ${ \sqrt { p _ { n + 1 } } } \ = \ b * { \sqrt { p _ { n } } } .$ . This implies that $\sqrt { p _ { n + 1 } * p _ { n } } \ = \ b * p _ { n }$ lies in E. Then the set of n integers $\left\{ p _ { 1 } , p _ { 2 } , . . . , p _ { n - 1 } , p _ { n + 1 } * p _ { n } \right\}$ satisfies the induction hypothesis, so the dimension of this field extension must be $2 ^ { n }$ . On the other hand, this field extension must be exactly $E ,$ whose dimension is $2 ^ { ( n - 1 ) }$ , a clear contradiction. Thus this case is impossible.   
2) $b = 0 \colon$ Then ${ \sqrt { p _ { n + 1 } } } = a$ lies in E. and the set of n integers $\left\{ p _ { 1 } , p _ { 2 } , . . . , p _ { n - 1 } , p _ { n + 1 } \right\}$ satisfies the induction hypothesis, so the dimension of this field extension must be $2 ^ { n }$ . On the other hand, this field extension must be exactly E, whose dimension is $2 ^ { ( n - 1 ) }$ , again a contradiction. Thus this case is impossible.   
3) $\sqrt { p _ { n } }$ is in E: Then $F = E$ , which is also a contradiction, since the dimension of F is twice that of E. Thus this case, too, is impossible.

The conclusion is that $\sqrt { p _ { n + 1 } }$ cannot lie in F . By contradiction to the assumption, we have that $\{ { \sqrt { p _ { 1 } } } , { \sqrt { p _ { 2 } } } , \ldots { \sqrt { p _ { n } } } \}$ are linearly independent over the field of rational Q. Proof complete. □

Lemma V.5. Given k squarefree integers $0 < n _ { 1 } < n _ { 2 } <$ < $\cdots < n _ { k }$ (a number is called squarefree if it is a products of mutually distinct prime numbers), then their square roots are linearly independent over the field of rational Q. Namely

$$
c _ {1} \sqrt {n _ {1}} + c _ {2} \sqrt {n _ {2}} + \dots + c _ {n} \sqrt {n _ {k}} = 0, c _ {i} \in \mathbb {Q},
$$

then $c _ { 1 } = c _ { 2 } = . . . = c _ { k } = 0$ holds.

Proof. Given k squarefree integers, without loss of generality, all the prime factors form a set $P = \{ p _ { 1 } , p _ { 2 } , . . . p _ { n } \}$ . If such nontrivial linear dependence exists, that

$$
c _ {1} \sqrt {n _ {1}} + c _ {2} \sqrt {n _ {2}} + \ldots + c _ {n} \sqrt {n _ {k}} = 0
$$

with all $c _ { i } \in \mathbb { Q }$ and nonzero. Specifically, the integers where the prime factor pi appears constitute a set $I , | I | > 1$ , we single out any of the primes involved and express its root rationally in terms of the roots of the other primes:

$$
\sqrt {p _ {j}} = \frac {\sum_ {i \neq I} c _ {i} \sqrt {n _ {i}}}{\sum_ {i \in I} c _ {i} \sqrt {\frac {n _ {i}}{p _ {j}}}}
$$

If division was illegal, it means that $\sum _ { i \in I } c _ { i } { \sqrt { \frac { n _ { i } } { p _ { j } } } } = 0 .$ ciq , and we replace the original linear dependence with this simpler one and repeat the argument. After finitely many steps we end up with a relation

$$
\sqrt {p _ {k}} \in \mathbb {Q} (\sqrt {p _ {1}}, \sqrt {p _ {2}},..., \sqrt {p _ {k - 1}})
$$

where $p _ { 1 } , p _ { 2 } , . . . p _ { k } , k \geq 1$ , are distinct prime numbers, that $\mathrm { i s } , \quad \sqrt { p _ { k } }$ expresses rationally in terms of the roots ${ \sqrt { p _ { 1 } } } , { \sqrt { p _ { 2 } } } , . . . , { \sqrt { p _ { k - 1 } } }$ . From Lemma ${ \mathrm { V . 4 } } ,$ we know that relation is impossible, therefore $\{ { \sqrt { n _ { 1 } } } , { \sqrt { n _ { 2 } } } , . . . , { \sqrt { n _ { k } } } \}$ are linearly independent over Q. □

Corollary V.1. According to the induction proposed in Lemma V.1, given an arbitrary chaotic code expressed in the form $p _ { 1 } ^ { \alpha _ { 1 } } p _ { 2 } ^ { \alpha _ { 2 } } . . . p _ { n } ^ { \alpha _ { n } } , \alpha _ { i } ( i \in \{ 1 , . . . , n \} ,$ must be a linear expression 1 2 n of the products of $\begin{array} { r } { \dot { \mathbf { \xi } } a _ { j } ^ { t _ { k } } \doteq \frac { 1 } { \sqrt { q _ { \mathrm { + } } ^ { t _ { k } } } } , \dot { \jmath } \in n , t _ { k } \in \{ 0 , . . . , t \} } \end{array}$ qqtk . And $q _ { j } ^ { t _ { k } }$ is a unique prime, which means each term of $\alpha _ { i }$ is squarefree, thus we can get a set $P$ of the corresponding prime factors according to Lemma V.2 and Equation (9). Particularly, for the exponents $\alpha _ { l i } ^ { t _ { 1 } }$ and $\alpha _ { l j } ^ { t _ { 2 } }$ of the same base $p _ { l } ,$ , we have $P _ { i } =$ $\{ a _ { i } ^ { t _ { 1 } } , . . . , P ( \alpha _ { \mu } ^ { t _ { 0 } } ) \}$ and $\vec { P _ { j } } ^ { ' } = \{ a _ { j } ^ { t _ { 2 } } , . . . , P ( \alpha _ { \mu } ^ { t _ { 0 } } ) \}$ , where $P ( \alpha _ { \mu } ^ { t _ { 0 } } )$ is the prime factors set of $\alpha _ { \mu } ^ { t _ { 0 } }$ , obviously it does not contain other elements of the set $P _ { i }$ and $P _ { j }$ .

• when i and j are different, different nodes and time epochs clearly have $P _ { i } \neq P _ { j }$ .   
• if i and j are the same node under different topology changes, many terms in $P _ { i }$ and $P _ { j }$ are the same, but the prime factors set $P ( \alpha _ { \mu } ^ { t _ { 0 } } )$ of the disturbance source µ must be different.

In summary, we can obtain that for all $\mathit { x } _ { i } ^ { t } ,$ the exponents αl of the same base $p _ { l }$ in its generic form, must be unique according to Lemma V.5.

Theorem V.4. $I f \left\{ p _ { 1 } , p _ { 2 } , . . . , p _ { n } \right\}$ are non-zero algebraic numbers with $\left\{ \log p _ { 1 } , . . . , \log p _ { n } \right\}$ linearly independent over the $\mathbb { Q } ,$ then $\{ \log p _ { 1 } , . . . , \log p _ { n } \}$ are linearly independent over the algebraic numbers.

Proof. This is a equivalent corollary of Baker’s Theorem, specific and complete proofs can be found in [50] and [51].

□

Corollary V.2. According to Lemma V.3 and Theorem V.4, since $\{ p _ { 1 } , p _ { 2 } , . . . p _ { n } \}$ are different primes, $\left\{ \log p _ { 1 } , \log p _ { 2 } , \dots \log p _ { n } \right\}$ is linearly independent over algebraic numbers.

Theorem V.5. Gelfond–Schneider theorem:If a and b are algebraic numbers with $a \neq 0 , 1$ , and b irrational, then any value of $a ^ { b }$ is a transcendental number.

Proof. It was originally proved independently in 1934 by Aleksandr Gelfond [52] and Theodor Schneider. □

Lemma V.6. Given a connected network at global convergence state s of topology C and code X, after a topological change $C  C ^ { \prime }$ , the chaotic code at each node i must be different (i.e., unique), namely $x _ { i } ^ { t 1 } ~ \neq ~ x _ { j } ^ { t 2 }$ , where $i , j \in$ $\{ 1 , 2 , . . . , n \}$ .

Proof. Without loss of generality, we assume that the two chaotic code $x _ { i } ^ { t 1 } = p _ { 1 } ^ { \alpha _ { 1 i } ^ { t 1 } } p _ { 2 } ^ { \alpha _ { 2 i } ^ { t 1 } } . . . p _ { n } ^ { \alpha _ { n i } ^ { t 1 } }$ and $x _ { j } ^ { t 2 } = p _ { 1 } ^ { \alpha _ { 1 j } ^ { t 2 } } p _ { 2 } ^ { \alpha _ { 2 j } ^ { t 2 } } . . . p _ { n } ^ { \alpha _ { n j } ^ { t 2 } }$ are equal, namely

$$
p _ {1} ^ {\alpha_ {1 i} ^ {t 1}} p _ {2} ^ {\alpha_ {2 i} ^ {t 1}}... p _ {n} ^ {\alpha_ {n i} ^ {t 1}} = p _ {1} ^ {\alpha_ {1 j} ^ {t 2}} p _ {2} ^ {\alpha_ {2 j} ^ {t 2}}... p _ {n} ^ {\alpha_ {n j} ^ {t 2}}
$$

After take logarithm at both sides, we have

$$
\sum_ {k \in \{1, 2, \dots , n \}} \alpha_ {k i} ^ {t 1} \log (p _ {k}) = \sum_ {k \in \{1, 2, \dots , n \}} \alpha_ {k j} ^ {t 2} \log (p _ {k})
$$

Namely,

$$
\sum_ {k \in \{1, 2, \dots , n \}} \left(\alpha_ {k i} ^ {t 1} - \alpha_ {k j} ^ {t 2}\right) \log (p _ {k}) = 0
$$

According to Theorem V.4 and Corollary V.2, $\left\{ \log p _ { 1 } , . . . , \log p _ { n } \right\}$ are linearly independent over the algebraic numbers. Therefore we have $\alpha _ { 1 i } ^ { t 1 } = \alpha _ { 1 j } ^ { t 2 } , \alpha _ { 2 i } ^ { t 1 } = \alpha _ { 2 j } ^ { t 2 }$ αt12i α 2j , $\ldots , \alpha _ { n i } ^ { t 1 } = \alpha _ { n j } ^ { t 2 }$ ..., α ni α nj , which contradicts to Corollary V.1.

Therefore, after a topological change $C  C ^ { \prime }$ , each node i must have a unique chaotic code, namely $x _ { i } ^ { t 1 } \neq x _ { j } ^ { t 2 }$ , where $i , j \in \{ 1 , 2 , . . . , n \}$ .

□

Lemma V.7. Given a connected network at global convergence state s with topology C and code X, and two different topological changes $C  C _ { 1 }$ and $C  C _ { 2 } ,$ , each node i must have a unique chaotic code, namely $x _ { i } ^ { t _ { 1 } } | C 1 \neq x _ { j } ^ { t _ { 2 } } | C 2 ,$ , where $i , j \in \{ 1 , 2 , . . . , n \}$ .

Proof. According to GTI tracing functions, different topological changes would lead to different topological matrix $C _ { 1 }$ and $C _ { 2 }$ . For simplicity, we use i and $i ^ { \prime }$ represent the node $i \in C _ { 1 }$ and the node $i \in C _ { 2 }$ , respectively.

According to Lemma.V.6, two different nodes $i \in C _ { 1 }$ and $j ~ \in ~ C _ { 2 }$ must have different chaotic codes, where $i , j \in$ $\{ 1 , 2 , . . . , n \}$ , namely $x _ { i } ^ { t 1 } | C 1 \neq x _ { j } ^ { t 2 } | C 2$ when $i \neq j ,$ , no matter they are in the same topology or not.

Without loss of generality, we assume that the two chaotic code $x _ { i } = p _ { 1 } ^ { \alpha _ { 1 } } p _ { 2 } ^ { \alpha _ { 2 } } . . . p _ { n } ^ { \alpha _ { n } }$ and $x _ { i ^ { \prime } } = p _ { 1 } ^ { \alpha _ { 1 } ^ { \prime } } p _ { 2 } ^ { \alpha _ { 2 } ^ { \prime } } . . . p _ { n } ^ { \alpha _ { n } ^ { \prime } }$ α n are equal, namely

$$
p _ {1} ^ {\alpha_ {1}} p _ {2} ^ {\alpha_ {2}}... p _ {n} ^ {\alpha_ {n}} = p _ {1} ^ {\alpha_ {1} ^ {\prime}} p _ {2} ^ {\alpha_ {2} ^ {\prime}}... p _ {n} ^ {\alpha_ {n} ^ {\prime}}
$$

that is,

$$
\log (p _ {1} ^ {\alpha_ {1}} p _ {2} ^ {\alpha_ {2}}... p _ {n} ^ {\alpha_ {n}}) = \log (p _ {1} ^ {- \alpha_ {1} ^ {\prime}} p _ {2} ^ {- \alpha_ {2} ^ {\prime}}... p _ {n} ^ {- \alpha_ {n} ^ {\prime}})
$$

, we further have

$$
\sum_ {k \in \{1, 2, \dots , n \}} \left(\alpha_ {k} - \alpha_ {k ^ {\prime}}\right) \log (p _ {k}) = 0
$$

According to Theorem V.4 and Corollary V.2, $\{ \log p _ { 1 } , . . . , \log p _ { n } \}$ are linearly independent over the algebraic numbers. Therefore we have $\alpha _ { 1 } = \alpha _ { 1 ^ { \prime } } , \alpha _ { 2 } = \alpha _ { 2 ^ { \prime } }$ , ..., $\alpha _ { n } = \alpha _ { n ^ { \prime } }$ .

According to Corollary V.1, since both $\alpha _ { i }$ and $\alpha _ { i ^ { \prime } }$ belong to the field $\mathbb { Q } ( A )$ , they are rational independent, namely $\alpha _ { i } \neq$ $\alpha _ { i ^ { \prime } }$ . Therefore, both $\alpha _ { i }$ and $\alpha _ { i ^ { \prime } }$ are unique algebraic number.

Since $\{ p _ { 1 } , p _ { 2 } , . . . p _ { n } \}$ are unique primes, and the exponents of any base prime number are different, there will not be two identical chaotic code value. □

Theorem V.6. Causality: Given a specific initialization setting and a specific time-series input (i.e., topological changes), the proposed GTI Tracing design always produces a unique course in the phase space. That is,

• A unique cause corresponds to a unique course under the same settings: under the same initialization setting, given a unique time-series input, GTI Tracing always returns a unique result.   
• Different causes correspond to different courses under the same setting: under the same initialization setting, given different time-series inputs, GTI Tracing always produces different results.   
• Same cause corresponds to different courses under different settings: under different initialization settings, given the same time-series input, GTI Tracing always produces different results.   
• Different causes correspond to different courses under different settings: under different initialization setting, given different time-series input, GTI Tracing always produces different results.

Proof. The four properties hold according to Lemma V.6 and Lemma V.7. □

Corollary V.3. Deterministic Traceing: According to the proposed design, any change in the network could be deterministically traced.

According to the proposed analysis, any topology or identity changes in the network yields a unique code evolution course in the phase space S. Thus the code (sequence) could be used to deduce the code evolution course in the phase space, which further corresponds to the node/edge addition/deletion in the physical space.

Remark: Note that $p ^ { \alpha }$ is a transcendental number according to Theorem V.5, Algorithm 2 heavily relies on the complex problem of transcendental number factorization. Particularly, if a node retains the global knowledge of the network, it could launch exhaustive search in the combinatorial space of of limited numbers in A, to find the right linear expression of α as shown in Equation 9. If not, the node cannot find the right expression of α, since the problem of transcendental number factorization is still uncomputable. Therefore, unless an attacker compromise the whole network and obtain the global knowledge of code, topology, and identities of all the nodes, it cannot get any useful information from the proposed GTI Tracing design.

VI. GTI TRACING BASED CLONE ATTACK DETECTION

In this section, we propose two GTI Tracing based clone attack detection approaches.

A. GTI Code based Clone Detection

Given the network under global convergence and an outside stimulus (a topology change), note that each step of GTI tracing is deterministic and injective one-to-one mapping, a node/link addition (so does the deletion) would inevitably result in deterministic topology changes.

According to the Equation 9 and Corollary V.1, given the $\alpha _ { l i } ^ { \overline { { t } } }$ with, and ngest term, by extracting , we can uniquely locate t $\bar { a } _ { i } ^ { t } , ~ a _ { j } ^ { t - 1 }$ , $a _ { k } ^ { t - 2 } , \cdot \cdot \cdot , \bar { a _ { z } ^ { t _ { 1 } } }$ ak · , $- \alpha _ { u } ^ { t _ { 0 } }$ node of the disturbance. Specifically, the path $u - > v - >$ $\ldots - > k - > j - > i$ is the shortest path that the spike effect traverses from u to i, and the exponent of the base prime number $p _ { v } ^ { t }$ has the longest combinatorial term, in which the elements retains all the time epochs from t to $t _ { 0 } .$ .

# Algorithm 2 Code based Clone Attack Detection

Require: The detector node i, which has the global knowledge of the network under global convergence, namely the topology and the code of each node under last global convergence. Specifically, the code of each node j should be in the form $x _ { j } ^ { t 0 } = \overset { \sim } { p } _ { 1 } ^ { \alpha _ { 1 j } ^ { t 0 } } p _ { 2 } ^ { \alpha _ { 2 j } ^ { t 0 } } \cdots p _ { n } ^ { \alpha _ { n j } ^ { t 0 } }$ xtj . The chaotic code $x _ { i } ^ { t } = p _ { 1 } ^ { \alpha _ { 1 i } ^ { t } } p _ { 2 } ^ { \alpha _ { 2 i } ^ { t } } . . . p _ { n } ^ { \alpha _ { n i } ^ { t } }$ pαt1i p α t2i .. , where $\alpha _ { l i } ^ { t }$ is a linear expression of the products of $a _ { j } ^ { t _ { k } } \frac { 1 } { \sqrt { q _ { j } ^ { t _ { k } } } }$ a tj

Ensure: The source disturbance node ID

1: $x _ { i } ^ { t } = p _ { 1 } ^ { \alpha _ { 1 i } ^ { t } } p _ { 2 } ^ { \alpha _ { 2 i } ^ { t } } . . . p _ { n } ^ { \alpha _ { n i } ^ { t } }$ αt1i .

2: Expand $\alpha _ { l i } ^ { t } ,$ , as shown in Equation 9

3: Find the longest combinatorial term in $\alpha _ { l i } ^ { t } ,$ that the elements in this term retains all the time epochs from t to $t _ { 0 } ,$ and the element with the smallest time epoch label matches with the global knowledge of the network under last global convergence (namely the element is $\alpha _ { u } ^ { t _ { 0 } }$ rather than $a _ { u } ^ { t _ { 0 } } )$

4: Extract $- \alpha _ { u } ^ { t _ { 0 } }$ , path $u - > v - > . . . - > k - > j - > i$ return the source disturbance node u, the path $u - \mathrm { ~ > ~ }$ $v - > . . . - > k - > j - > i$

According to the determinacy and causality property of GTI Tracing, if a node i knows the global knowledge of the network under previous global convergence, it could use its current code to deterministically locate who (i.e., identity) leads to a new disturbance to the network, where is the code/topology change(i.e., locations), and whether it is a clone or not.

Specifically, by checking the paths $u - \ > \ v - \ > \ . . . - \ >$ $k - \mathbf { \omega } > \mathbf { j } - \mathbf { \omega } > \mathbf { \omega } _ { i }$ and their corresponding minus signs such as $- \alpha _ { u } ^ { t _ { 0 } }$ , it is easy to determine whether it is an edge addition/deletion or node addition/deletion,

Therefore, though a cloned node j can "pretend" to be legitimate by having all the valid security information, it cannot persuade others in the network, because every other node i can easily tell that j’s clone leads to illegal topology/identity match that is inconsistent with i’s chaotic code (sequence).

B. GTI Code Sequence based Clone Detection

In this section, we propose a coded sequence based detection scheme. Specifically, it adopts a scan line based detection method that searches candidate topology change that leads to a consistent code evolution from last global convergence state.

Given the network under global convergence and an outside stimulus (topology changes), when a node i identifies any code change, i may check whether there is a candidate topology change that leads to a consistent code evolution from last global convergence state (namely node i’s code sequence). Note that the determinacy and causality properties guarantee that there exists only one candidate topology change.

As shown in Code Sequence based Clone Detection Algorithm 3, given a node i who retains the initial knowledge of the network, we apply the scan line method to locate the a particular candidate of the topological change, i.e., launching GTI Tracing by checking every possible node/link addition/deletion.

Algorithm 3 Code Sequence based Clone Attack Detection   
Require: continuous code sequence for a monitor node i : $\{x_{i}^{0}, x_{i}^{1}, \ldots, x_{i}^{T}\}$ , adjacency matrix $C_{n \times n}$ , set of whole nodes S, all nodes' original codes $x_{j}^{0}, j \in S$ , number of iteration round r.

Ensure: cloned node ID and connection status of the illegal node

1: use the scan line algorithm (SLPF) to obtain the unique regions $R = \{R_{1}, R_{2}, \ldots, R_{m}\}$ formed by the node communication radius in the topology network.

2: add a zero column and row to $C_{n \times n}$ to becomes $C_{(n+1) \times (n+1)}$ .

3: detected ← false

4: for each element $R_{i} \in R$ do

5: for node $j \in S$ do

6: for node k within $R_{i}$ 's communication radius do $C_{n+1,k} = C_{k,n+1} = 1$ 7: end for

8: $x_{n+1}^{0} = x_{j}^{0}, r = 0$ 9: for node $s \in S$ do

10: run the GTI Tracing for one round.

11: end for

12: $r = r + 1$ 13: while codes have not converged yet do

14: if The current calculation result is inconsistent with the actual code sequence $\{x_{i}^{0}, x_{i}^{1}, \ldots, x_{i}^{T}\}$ then

15: break;

16: end if

17: for $s \in S$ do

18: run the GTI Tracing for one round.

19: end for

20: $r = r + 1$ 21: end while

22: if r == T then

23: detected ← true return $C_{(n+1) \times (n+1)}$ and node j

24: end if

25: end for

26: end for

Particularly, the computation complexity for the node i to keep tracing the dynamics of global identities and topological changes is $O ( n ^ { 2 } )$ . While for other nodes, only local code update is necessary. In other words, the proposed design offload the communication and storage overhead to computation domain, and also offload the global tracing and information collection cost to on-demand computation at any node.

To further illustrate the proposed algorithm, we randomly selected multiple nodes A, B, and C in the network and extract their code sequences for further illustration, as shown in Fig.3.

![](images/4ca8e4f3ff802a060c9e2a97a77907ac5fbd8b54a17f2d4ab93ad8c7f303de64.jpg)



Fig. 3: Example Illustration

As shown in Fig.4, it is interesting to observe that spikes appear in turn in the code sequences of these nodes according to their topological distance to the sources of the topological change.

![](images/d942e5c113f8294b674bb3b31994a0de698e9d737e1e1819779063018f115f0d.jpg)



Fig. 4: Example Code Sequences with A Spike Spread from Source 1

Remark: According to Fig.4, since spikes appear in turn in multiple nodes’ code sequences according to their topological distance to the source. This further provides a straightforward way to apply Alg.3, if there are multiple nodes at different positions collaboratively monitoring the network, we could use contour lines of spike arrival time to locate the source region of the topological change, which may greatly restrict the search space of the clone detection to a local region, and provide much better time complexity than the single detector scenario.

# VII. PERFORMANCE ANALYSIS

In this section, we conduct study on the resilience and effectiveness of our scheme against clone attack.

During implementation, Code Sequence Based Detection Algorithm 3 would be preferred due to its computation efficiency, and the following performance data are all based on that.

# A. Detection Resilience

When the attacker compromises a node u, replicates and distributes a clone v, it may determine v’s code codev according to the following methods:

• Case I: clone v selects $x _ { v } \ = \ x _ { u } , \ \forall u \in V$ given the network $G ( V , E )$ . Suppose node v generates a message C and forwards it to a neighbor $w \in \mathcal { N } ( v )$ . If w is legitimate, w should detect a code/edge/identity addition into its neighborhood and then generate a spike to its neighborhood codes. Since the change of code means the change of topology, a mismatch can be found by the detector node i in its code (sequence), since there will be a conflict of appearance of node u in the network. Particularly, the detector node i identifies the conflict by recovering the global knowledge of identities and topology of the network, i.e., by launching either the code or code sequence based detection algorithm, to identify the source of the butterfly effect.

Note that there is no incentive for the adversary to compromise all nodes in $\mathcal { N } ( v )$ in order to launch a clone attack. Furthermore, for a cloned area (containing cloned nodes only) that is larger than a typical open neighborhood, the changes of the codes of the boundary nodes can be easily identified and then revoked.

• Case II: clone v selects an arbitrary bit stream as $x _ { v } , \ x _ { v } \ \ne \ x _ { u } , \ \forall u \ \in \ V$ given the network $G ( V , E )$ . Obviously there will be a node/edge change among clone v’s neighborhood $\mathcal { N } ( v )$ . Since the change of code means the change of topology, a spike would be generated by a neighbor $w \in \mathcal { N } ( v )$ in its code sequence, and spread throughout the network.

According to Alg.2 (Code based Clone Attack Detection), clone v will be detected by the detector node i, since there will be a conflict of code and identity appearance/topology mismatch. This is because the mismatch corresponds to an abnormal representation of $x _ { i }$ with an algebraic exponent α that cannot be expressed by the linear combination of the elements in A. The location of the anomaly and its traverse path from the anomaly to the detector node i would further be deduced according to the detailed expression of the abnormal algebraic exponent α. Particularly, Alg.3 (Code Sequence based Clone Attack Detection) could detect the existence of such topology/identiy anomaly. To further detect the local region of such topology/identiy anomaly, there need multiple detectors collaboratively launching Alg.3, i.e., by using contour lines of spike arrival time (as shown in Fig.4), to locate the source region of the topological change.

• Case III: malign nodes fail to respond to spikes when clone or topology change occurs

Without loss of generality, we assume that not all the nodes in $\mathcal { N } ( v )$ are malign nodes. Namely there is at least one benign node in $\bar { \mathcal { N } ( \boldsymbol { v } ) }$ . There will be a path $u - >$ $v - > . . . - > k - > j - >$ i returned by Alg.2, which directly provides the source of the disturbance, and its path traversing to the detector i. For Alg.3, the discussion is similar with Case II.

# B. Detection Performance

In order to evaluate the detection performance of our design, we conduct simulation study with 300 nodes randomly deploy in a $1 0 , 0 0 0 \times 1 0 , 0 0 0$ area, with restricted communication range [100, 500]. The study is conducted on various network topologies, e.g., line-based, star-based, tree-based, ring-based, and mesh based.

As shown in Fig.5, an arbitrarily selected node is cloned to another area. The simulation is conducted over 100 different random topologies, within each we repeat 20 times clone attacks. The detection accuracy conform to our theoretical analysis, which is 100%.

![](images/23954b7957ab5e903e4063aae4d4d9b12dbbb00855db92f29f7753aa2a6ba239.jpg)



Fig. 5: Example Illustration of Clone Detection

As shown in Fig.6, the clone attack detection probability is always 100% in various scenarios. In particular, Fig.6(a) shows that the proposed detection algorithms have a deterministic detection for both large and small scale networks. Fig.6(b) depicts the detection performance in networks with different levels of complexity (average vertex connectivity used to represent the complexity and Denseness). It is worth mentioning in Fig.6(c) that when the number of clone attacks increases dramatically to a threshold, the computational power requirements of the detection algorithm will increase significantly. This is because the more attacks there are, the much more detectors are needed for locating the local region of the attacks.

The detection time cost for clone detection under the same network scale and environment is shown in Fig.9(a). Since MDSClone is a centralized solution, it takes a lot of time for the Base Station to collect information about the pairwise distance between nodes. As for SDD, the main delay comes from the identification for the witness nodes. Compared to them, our algorithm has a significant advantage with the least detection time.

![](images/2b1d9a368c8a74638e9672b74c47c8571b3c9201b7f3cba7ac934e6e93b85859.jpg)



(a)

![](images/967f034b6900ff3f5797769b1bc8250f530204f6a9057518e11b0568d33fbb3f.jpg)



(b)

![](images/f67a725ece87ad1335ae847e03163fe778b60e9a49bbc68d275f1749cc964319.jpg)



(c)   
Fig. 6: Clone Detection Probability vs. Network Scale (a) and Network Complexity (b) and Attack Frequency (c)

# C. Convergence Rate

In this section, the study on the convergence rate (i.e., the time duration for the network converging to next global convergence state) is conducted over different topologies and network scales. From the histogram Fig.7, we can see that the average convergence time epochs at each node could be roughly estimated as a normal distribution, which implies the convergence rate under different scales and topologies of network is limited by the network diameter D. This result is further verified in Fig.8, which shows that the time needed for the network from a global convergence state to the next global convergence state (given a random topological/identity change) is about $c \times D ,$ where D is the diameter of the network, and c is a small constant.

![](images/e39b9dececdb66e7320d4e5ea3b06d86c349ac1a96a7788bca9ce98f88ae224a.jpg)



Fig. 7: Histogram of the Convergence Time Epochs Needed at Each Node (connected random mesh network)

![](images/112fc6eacb1df00cfe59d6154cb123c7f12f9b4fdea1e20dd5cac00936f2a147.jpg)



Fig. 8: Average Convergence Time vs. Network Diameter

# D. Communication, Storage and Computation Overhead

In this section, we evaluate the performance of our detection scheme in terms of communication/storage overhead, and conduct a brief comparison with the most related work.

Note that the chaotic code is about 2 − 4 bytes. We can piggyback the codes with regular beacon messages. In this case, the algorithm will have no additional communication overhead, that is, its additional message complexity is O(1). As shown in the Fig.9(b), compared to other algorithms that require a large amount of information continuously collected and transmitted to the base station, the communication of our proposed algorithms is restricted to each node’s local neighbors.

For each node, all it needs to store is the code/identity of its neighbor nodes within 2 hops, and its complexity is $O ( d ^ { 2 } )$ (as shown in Fig.9(c)). The special case is that the monitoring node needs to record the complete code sequence. Therefore its storage complexity is $O ( d \cdot D + d ^ { 2 } )$ , where D refers to the network diameter, since the number of time epochs between two consecutive global convergence state is proportional to the network diameter.

![](images/e1ca906fd386b49133d5f3d75f52b7508efde4064110d13dd9ca95352117039e.jpg)



![](images/8048abdd7c30ec0b16461e6cf2c524996d8399c3cef42757a6ad8a5cd575df97.jpg)



(b)

![](images/16ccfd964a874e1d6968cb8e74b8638b9af40c73e53a6cd810a46359040fbb42.jpg)



Fig. 9: Performance Comparison on Detection Time, Communication Cost, and Storage Cost

Note that the computation cost at each node (except the detector) only involves simple operations, our algorithms have extremely low computation overhead at most nodes. For the detector node, it needs to compute the exact code evolution course of the network system from the initial network state, which is O(D).

# E. Comparison with Existent Work

In this section, we provide a brief study on various existing approaches against clone attacks for the scenarios of continuously monitoring. We simply put their communication cost, storage cost and detection probability together here to facilitate readers’ reading. Note that it is not fair to compare centralized, distributed and localized approaches together. When do comparison, readers may refer to their categories.

Particularly, the communication cost and storage cost are measured under the scenarios of continuously monitoring. This is based on two perceptions in practice: 1. attacks occur endlessly, not just once; 2. a late detection is usually meaningless. Therefore, we mainly focus on the scenarios of continuously monitoring, i.e., the network continuously executes these detection schemes.

Note that most localized approaches propose their cost study with node-wise analysis, we measure the communication cost and storage cost incurred by detector instead of global cost, as shown in Fig. I.

Note that the neighbor lists and location claims adopted in many approaches may incur too much overhead to be collected in continuously monitoring. In order to reduce the cost, these approaches have to be run periodically, which leads to a less timely detection. It means that these strategies may has limited ability in the scenarios of continuously monitoring. To avoid this limitation, our scheme provides an efficient localized solution. Once cloned nodes send out messages, these nodes can be deterministically detected in almost real-time.

# VIII. DISCUSSIONS

A. The Applicability of Alg.3: Convergence Rate and Topology Change Rate

As discussed in Section IV and Section VI, the code sequence based GTI Tracing detection scheme poses an implicit

<table><tr><td>Schemes</td><td>Communication Cost</td><td>Storage Cost</td><td>Detection Probability</td><td>Category</td></tr><tr><td>Broadcast [4]</td><td> $O(n)$ </td><td> $O(d)$ </td><td>100%</td><td>Distributed</td></tr><tr><td>RM [4]</td><td> $O(n\sqrt{n})$ </td><td> $O(\sqrt{n})$ </td><td> $< 1$ </td><td>Distributed</td></tr><tr><td>LSM [4]</td><td> $O(n\sqrt{n})$ </td><td> $O(\sqrt{n})$ </td><td> $< 1$ </td><td>Distributed</td></tr><tr><td>NI-LEACH [23]</td><td> $O(\frac{n}{d}\ln\frac{n}{d})$ </td><td> $O(\frac{n}{d})$ </td><td> $< 1$ </td><td>Centralized</td></tr><tr><td>RWND [26]</td><td> $O(\frac{n}{d}\ln\frac{n}{d})$ </td><td> $O(\frac{n}{d})$ </td><td> $< 1$ </td><td>Centralized</td></tr><tr><td>SET [28]</td><td> $O(n)$ </td><td> $O(d)$ </td><td>100%</td><td>Centralized</td></tr><tr><td>RED [21]</td><td> $O(nwdp\sqrt{n})$ </td><td> $O(wdp)$ </td><td> $< 1$ </td><td>Distributed</td></tr><tr><td>XED [34]</td><td> $O(1)$ </td><td> $O(n)$ </td><td> $< 1$ </td><td>Localized</td></tr><tr><td>SPRT [40]</td><td> $O(\sqrt{n})$ </td><td> $O(1)$ </td><td> $< 1$ </td><td>Centralized</td></tr><tr><td>TDD [41]</td><td> $O(\sqrt{n})$ </td><td> $O(n)$ </td><td> $< 1$ </td><td>Distributed</td></tr><tr><td>SDD [41]</td><td> $O(n)$ </td><td> $O(n)$ </td><td> $< 1$ </td><td>Localized</td></tr><tr><td>HOP [43]</td><td> $O(n)$ </td><td> $O(1)$ </td><td> $< 1$ </td><td>Localized</td></tr><tr><td>MDSClone [42]</td><td> $O(n\sqrt{n})$ </td><td> $O(nd)$ </td><td>100%</td><td>Centralized</td></tr><tr><td>Algorithm 2</td><td> $O(d^{2})$ </td><td> $O(d^{2})$ </td><td>100%</td><td>Localized</td></tr><tr><td>Algorithm 3</td><td> $O(d^{2})$ </td><td> $O(d \cdot D + d^{2})$ </td><td>100%</td><td>Localized</td></tr></table>

n:number of nodes, d: average node degree, D: the diameter of the network, w: number of witnesses generated by a neighboring node, p: probability of forwarding a message

TABLE I: Comparison with Existent Work assumption: during the time between a global convergence state and the next global convergence state, there is only one topology change (including clones) in the network. That is, the speed of the global convergence would be an important factor for the applicability of the proposed code sequence based detection design.

In order to better speedup the convergence, we enforce the chaotic code at each node stop updating and keep a fixed value once it enters into local convergence according to Subsection IV-B2. According to VII-C, the convergence rate of the code is proportional to the network diameter. Therefore, the proposed code sequence based detection design is a good candidate for the network with limited diameter and slow topology change rate, e.g., mesh topology/tree topology such as IoT networks, sensor networks, distributed systems, etc. However, it is not suitable for fast-moving networks, such as vehicular networks.

# B. Extension to Distributed Detection on Multiple Clones Deployed between two consecutive stable state

In general, Algorithm 2 works well in both non-concurrent and concurrent clone detection due to the completeness of its theoretical design. Its completeness and accuracy requires sufficient computing power. Algorithm 3 is computational efficient and good enough for the non-concurrent clone attack scenarios. For non-concurrent clones, it needs multiple detectors. However, if there are multiple concurrent clones, it could locate the residence areas of the clones, but not necessarily be the accurate positions and IDs. In this situation, the search space is limited in the residence area of the attacker instead of the whole network.

# IX. CONCLUSION

In this paper, we propose a novel global topology and identity tracing(GTI Tracing) scheme against clone attacks. It transforms the global tracing problem of identity and topology from the time and space domain to a computation domain. Specifically, we provides a constructive computation paradigm characterizing the residency (domain) of the local information (identity/topology change) and its mathematical connection to global knowledge of identities and topology in the computation domain.

Both theoretical study and experimental evaluation on the performance of detection, security, computation, communication, and storage has shown that, the proposed design provides deterministic detection and sound resiliency against clone attacks. The corresponding communication/computation/storage cost at each node is restricted within one-hop neighborhood, except that the computation cost at the detector node would be high.

This proposed layout work provides a new way of looking at the global tracing problem of local events for a large variety of distributed networks/systems. When acquiring/tracing global knowledge of a system/network, it is no longer necessary to make a global information collection effort. This may benefit related research in many other fields. For the future work, we plan to extend our scheme to other distributed networks and various attacks, e.g., sybil attack.

# REFERENCES

[1] A. Becher, Z. Benenson, and M. Dornseif, “Tampering with motes: Realworld physical attacks on wireless sensor networks,” in International Conference on Security in Pervasive Computing. Springer, 2006, pp. 104–118.   
[2] H. Zhu, R. Lu, X. Shen, and X. Lin, “Security in service-oriented vehicular networks,” IEEE Wireless Communications, vol. 16, no. 4, pp. 16–22, 2009.   
[3] Y. Meng, W. Zhang, and H. Zhu, “Securing consumer iot in the smart home: Architecture, challenges, and countermeasures,” IEEE Wireless Communications, vol. 25, pp. 53–59, 2018.   
[4] B. Parno, A. Perrig, and V. Gligor, “Distributed detection of node replication attacks in sensor networks,” in IEEE Security and Privacy, 2005, pp. 49–63.   
[5] R. Grewal, J. Kaur, and K. S. Saini, “A survey on proficient techniques to mitigate clone attack in wireless sensor networks,” in IEEE International Advance Computing Conference, 2015, pp. 1148–1152.   
[6] H. Wang, Y. Wen, Y. Lu, D. Zhao, and C. Ji, “Secure localization algorithms in wireless sensor networks: a review,” in Advances in Computer Communication and Computational Sciences. Springer, 2019, pp. 543–553.   
[7] M. Hossain, “Towards a holistic framework for secure, privacy-aware, and trustworthy internet of things using resource-efficient cryptographic schemes,” Ph.D. dissertation, The University of Alabama at Birmingham, 2018.   
[8] E. Benkhelifa, T. Welsh, and W. Hamouda, “A critical review of practices and challenges in intrusion detection systems for iot: Toward universal and resilient systems,” IEEE Communications Surveys & Tutorials, vol. 20, no. 4, pp. 3496–3509, 2018.   
[9] H. Xie, Z. Yan, and Z. Yao, “Data collection for security measurement in wireless sensor networks: A survey,” IEEE Internet of Things Journal, vol. 6, pp. 2205–2224, 2018.

[10] W. Z. Khan, M. S. Hossain, M. Y. Aalsalem, and N. M. Saad, “A cost analysis framework for claimer reporter witness based clone detection schemes in wsns,” Journal of Network and Computer Applications, vol. 63, pp. 68–85, 2016.   
[11] S. Roy and M. J. Nene, “Prevention of node replication in wireless sensor network using received signal strength indicator, link quality indicator and packet sequence number,” in Conference on Green Engineering and Technologies, 2016, pp. 1–8.   
[12] S. M. H. Mirshahjafari and B. S. Ghahfarokhi, “Sinkhole+ cloneid: A hybrid attack on rpl performance and detection method,” Information Security Journal: A Global Perspective, vol. 28, no. 4-5, pp. 107–119, 2019.   
[13] W. B. Jaballah, M. Conti, and G. Filè, “Whac-a-mole: Smart node positioning in clone attack in wireless sensor networks,” Computer Communications, vol. 119, pp. 66–82, 2018.   
[14] I. Butun, P. Österberg, and H. Song, “Security of the internet of things: Vulnerabilities, attacks and countermeasures,” IEEE Communications Surveys & Tutorials, 2019.   
[15] N. Usha and E. M. Anita, “An elaborate survey on node replication attack in static wireless sensor networks,” International Journal of Computer and Information Engineering, vol. 12, no. 10, pp. 797–804, 2018.   
[16] D. Shaw and W. Kinsner, “Multifractal modelling of radio transmitter transients for classification,” in IEEE Conference on Communications, Power and Computing, 1997, pp. 306–312.   
[17] M. Ding, D. Chen, K. Xing, and X. Cheng, “Localized fault-tolerant event boundary detection in sensor networks,” in IEEE 24th Annual Joint Conference of the IEEE Computer and Communications Societies, vol. 2, 2005, pp. 902– 913.   
[18] F. Liu, X. Cheng, and D. Chen, “Insider attacker detection in wireless sensor networks,” in IEEE International Conference on Computer Communications, 2007, pp. 1937–1945.   
[19] P. Kyasanur and N. H. Vaidya, “Detection and handling of mac layer misbehavior in wireless networks,” in IEEE Conference on Dependable Systems and Networks, 2002, pp. 173 – 182.   
[20] J. Newsome, E. Shi, and D. Song, “The sybil attack in sensor networks: analysis & defenses,” in International symposium on Information processing in sensor networks, 2004, pp. 259–268.   
[21] M. Conti, R. D. Pietro, L. Mancini, and A. Mei, “Distributed detection of clone attacks in wireless sensor networks,” IEEE Transactions on Dependable and Secure Computing, vol. 8, no. 5, pp. 685–698, 2011.   
[22] B. Zhu, V. G. K. Addada, S. Setia, S. Jajodia, and S. Roy, “Efficient distributed detection of node replication attacks in sensor networks.” in Computer Security Applications Conference, 2007, pp. 257–267.   
[23] G. Cheng, S. Guo, Y. Yang, and F. Wang, “Replication attack detection with monitor nodes in clustered wireless sensor networks,” in IEEE International Performance Computing and Communications Conference. IEEE, 2015, pp. 1–8.   
[24] C.-M. Yu, C.-S. Lu, and S.-Y. Kuo, “Compressed sensing-based clone identification in sensor networks,” IEEE Transactions on Wireless Communications, vol. 15, no. 4, pp. 3071–3084, 2016.   
[25] S. Zhang, Z. Ning, and Y. Cao, “Effective clone detection model based on compressed sensing in clustered wsns,” in International Conference on Computer Science and Artificial Intelligence, 2018, pp. 468–473.   
[26] W. Z. Khan, M. Y. Aalsalem, and N. Saad, “Distributed clone detection in static wireless sensor networks: random walk with network division,” PloS one, vol. 10, no. 5, p. e0123069, 2015.   
[27] M. Rui, Z. Tianbao, M. Ke, H. Changzhen, and Z. Xiaolin, “Singlewitness-based distributed detection for node replication attack,” Journal of Tsinghua University (Science and Technology), vol. 57, no. 9, pp. 909–913, 2017.   
[28] H. Choi, S. Zhu, and T. Laporta, “Set: Detecting node clones in sensor networks,” in International Conference on Security and Privacy in Communications Networks and the Workshops, 2007, pp. 341–350.   
[29] R. R. Brooks, P. Y. Govindaraju, M. Pirretti, N. Vijaykrishnan, and M. T. Kandemir, “On the detection of clones in sensor networks using random key predistribution,” IEEE Transactions on Systems, Man, and Cybernetics, pp. 1246–1258, 2007.   
[30] L. Eschenauer and V. D. Gligor, “A key-management scheme for distributed sensor networks,” in ACM conference on Computer and communications security, 2002, pp. 41–47.   
[31] K. Xing, F. Liu, X. Cheng, and D. H. C. Du, “Real-time detection of clone attacks in wireless sensor networks,” in 2008 The 28th International Conference on Distributed Computing Systems, 2008, pp. 3–10.   
[32] Y. Zeng, J. Cao, S. Zhang, S. Guo, and L. Xie, “Random-walk based approach to detect clone attacks in wireless sensor networks,” IEEE Journal on Selected Areas in Communications, vol. 28, no. 5, pp. 677– 691, 2010.

[33] C. M. Yu, C. S. Lu, and S. Y. Kuo, “Efficient and distributed detection of node replication attacks in mobile sensor networks,” in IEEE Vehicular Technology Conference, 2009, pp. 1–5.   
[34] C. M. Yu, Y. T. Tsou, C. S. Lu, and S. Y. Kuo, “Localized algorithms for detection of node replication attacks in mobile sensor networks,” IEEE Transactions on Information Forensics and Security, vol. 8, no. 5, pp. 754–768, 2013.   
[35] K. Liu, L. Chen, Y. Liu, W. Gong, and A. Nayak, “Continuous answering holistic queries over sensor networks,” IEEE Transactions on Parallel and Distributed Systems, vol. 27, no. 2, pp. 394–404, 2015.   
[36] M. Hossain, S. Noor, and R. Hasan, “Hsc-iot: a hardware and software co-verification based authentication scheme for internet of things,” in 2017 5th IEEE International Conference on Mobile Cloud Computing, Services, and Engineering (MobileCloud). IEEE, 2017, pp. 109–116.   
[37] N. Shashidhar, C. Kari, and R. Verma, “The efficacy of epidemic algorithms on detecting node replicas in wireless sensor networks,” Journal of Sensor and Actuator Networks, vol. 4, no. 4, pp. 378–409, 2015.   
[38] M. Mozumdar, M. Aliasgari, S. M. V. Venkata, and S. S. Renduchintala, “Ensuring authentication and security using zero knowledge protocol for wireless sensor network applications,” International Journal of Computing and Digital Systems, 2016.   
[39] V. Manickavasagam and J. Padmanabhan, “A mobility optimized sprt based distributed security solution for replica node detection in mobile sensor networks,” International Conference on Ad Hoc Networks, vol. 37, pp. 140–152, 2016.   
[40] J. W. Ho, M. Wright, and S. K. Das, “Fast detection of mobile replica node attacks in wireless sensor networks using sequential hypothesis testing,” IEEE Transactions on Mobile Computing, vol. 10, no. 6, pp. 767–782, 2011.   
[41] K. Xing and X. Cheng, “From time domain to space domain: Detecting replica attacks in mobile ad hoc networks,” in IEEE Conference on Information Communications, 2010, pp. 1–9.   
[42] M. C. PoYen Lee, ChiaMu Yu, “Mdsclone:multidimensional scaling aided clone detection in internet of things,” in Transactions on Information Forensics & Security, 2017.   
[43] M. Conti, R. Di Pietro, and A. Spognardi, “Clone wars: Distributed detection of clone attacks in mobile wsns,” Journal of Computer and System Sciences, pp. 654–669, 2014.   
[44] M. Zhang, V. Khanapure, S. Chen, and X. Xiao, “Memory efficient protocols for detecting node replication attacks in wireless sensor networks,” in 2009 17th IEEE International Conference on Network Protocols, 2009, pp. 284–293.   
[45] M. Dong, K. Ota, L. T. Yang, A. Liu, and M. Guo, “Lscd: A low-storage clone detection protocol for cyber-physical systems,” IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, vol. 35, no. 5, pp. 712–723, 2016.   
[46] K. Sun, P. Ning, and C. Wang, “Tinysersync: secure and resilient time synchronization in wireless sensor networks,” in ACM conference on Computer and communications security, 2006, pp. 264–277.   
[47] L. Chen and J. Leneutre, “A secure and scalable time synchronization protocol in ieee 802.11 ad hoc networks,” in International Conference on Parallel Processing Workshops, 2006, pp. 207–214.   
[48] K. Römer, “Time synchronization in ad hoc networks,” in Proceedings of the 2nd ACM international symposium on Mobile ad hoc networking and computing, 2001, pp. 173–182.   
[49] C. Zhang, Y. Song, Y. Fang, and Y. Zhang, “On the price of security in large-scale wireless ad hoc networks,” IEEE/ACM Transactions on Networking, vol. 19, no. 2, pp. 319–332, 2011.   
[50] A. Baker, Transcendental number theory. Cambridge university press, 1990.   
[51] A. Baker and G. Wüstholz, “Logarithmic forms and group varieties.” Journal für die reine und angewandte Mathematik, vol. 1993, no. 442, pp. 19–62, 1993.   
[52] A. Gelfond, “Sur le septieme probleme de hilbert,” Izvestia of the Russian Academy of Sciences. Mathematical Series, no. 4, pp. 623–634, 1934.