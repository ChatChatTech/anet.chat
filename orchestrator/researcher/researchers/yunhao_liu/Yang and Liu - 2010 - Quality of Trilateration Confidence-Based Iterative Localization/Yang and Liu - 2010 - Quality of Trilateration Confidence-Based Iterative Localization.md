# Quality of Trilateration: Confidence-Based Iterative Localization

Zheng Yang, Student Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—The proliferation of wireless and mobile devices has fostered the demand for context-aware applications, in which location is one of the most significant contexts. Multilateration, as a basic building block of localization, however, has not yet overcome the challenges of 1) poor ranging measurements; 2) dynamic and noisy environments; and 3) fluctuations in wireless communications. Hence, multilateration-based approaches often suffer from poor accuracy and can hardly be employed in practical applications. In this study, we propose Quality of Trilateration (QoT) that quantifies the geometric relationship of objects and ranging noises. Based on QoT, we design a confidence-based iterative localization scheme, in which nodes dynamically select trilaterations with the highest quality for location computation. To validate this design, a prototype network based on wireless sensor motes is deployed and the results show that QoT well represents trilateration accuracy, and the proposed scheme significantly improves localization accuracy.

Index Terms—Localization, noisy range measurements, trilateration, wireless ad-hoc and sensor networks.

# 1 INTRODUCTION

ERVASIVE and mobile systems for context-aware comput-P ing are growing at a phenomenal rate. In most current applications such as pervasive medical care, smart space, wireless sensor network surveillance, mobile peer-to-peer computing, etc., location is the most essential context. Many localization algorithms are designed in recent years, among which multilateration plays an important role. By measuring the distance from multiple reference positions, the position of an object can be computed. Fig. 1a plots an example of trilateration, a particular form of multilateration, which utilizes three references to calculate the location of an object in two dimensions. Obviously, the object to be localized should locate at the intersection of three circles centered at each reference. The computed location is unique as long as three references are nonlinear.

Being quite popular because of the ease of implementation, trilateration-based approaches are facing many challenges. First and foremost, although several ranging techniques are developed, such as Received Signal Strength (RSS) [1], Time of Arrival (TOA), and Time Difference of Arrival (TDOA) [2], [3], error is inevitable in all of them. For example, the RSS-based techniques estimate the distance between two communication devices by assuming a known rate of signal attenuation over distance. Consequently, RSS is sensitive to the channel noise, signal interference, attenuation, and reflection, all of which have significant impact on signal amplitude. RSS also suffers from transmitter, receiver, and antenna variability. For the propagation-time-based ranging techniques (TOA and TDOA), the signal propagation speed often exhibits variability as a function of temperature or humidity; so, we cannot assume the propagation speed being constant across a large field. Moreover, the inaccuracy of time synchronization also leads to ranging errors.

Indeed, this study is motivated by our recent prototype of a wireless sensor network in a coal mine, consisting of 27 CrossBow Mica2 sensor nodes [4]. The basic goal of the system is to monitor gas and water leakage. During emergency, the system is also expected to navigate the miners out or help to search trapped miners [5]. Among all those functions, to know the location of each sensor is of great importance. The straightforward multilaterationbased localization was employed as our early attempt. However, the localization turns out to be a failure because the noisy distance estimation greatly degrades the quality of trilateration in the following four aspects:

Uncertainty. Fig. 1b illustrates an example of trilateration under noisy ranging measurements. During our experiments, we often met the situation that the three circles do not intersect at a common point. In other words, there does not exist any position satisfying all distance constraints.

Nonconsistency. In many cases, a single node has many reference neighbors. Any subgroup of them (no less than three) can locate this node by multilateration. The computed result, however, is varying if different groups of references are chosen, resulting in nonconsistency. Thus, when alternative references are available, existing approaches fail to determine which combination of references provides the best results.

Ambiguity. Flip [6], [7] is a kind of ambiguity, in which the references create a mirror through which the position can be reflected. The flip ambiguity occurs very often under noisy ranging measurements or in sparsely connected networks.

Error propagation. The results of a multihop localization process are based on a series of single-hop multilaterations in an iterative manner [3]. In such a process, errors, coming from each step of multilateration, propagate and accumulate [8], [9].

Taking the trilateration as a representative of all forms of multilateration, we focus on the localization accuracy under noisy ranging measurements. In order to address the four previously mentioned challenges, we propose the concept of Quality of Trilateration (QoT), which is inspired by the key observation that different geometric forms of trilaterations provide different levels of accuracy. The metric QoT quantitatively describes such differences and, more importantly, helps to compare and make choices of trilaterations. This metric enables the ability of distinguishing and avoiding poor trilaterations that are of much uncertainty or potential flip ambiguity.

![](images/3619e8c8970bc37f61f3923a7c16061f9587765a1cc447903e29dc409c48ddef.jpg)



(a)

![](images/a92d52ca69af26df9f5448406530fa94b393195eab2e5c0d41f360de5bf8fc4d.jpg)



(b)   
Fig. 1. Trilateration. (a) Precise ranging measurement. (b) Noisy ranging measurement.

Based on QoT, a Confidence-based Iterative Localization (CIL) scheme is designed, in which each node is assigned a confidence value to indicate its localization accuracy. Initially, all beacon nodes have the maximum confidence while other nodes are with the minimum confidence. The localization process is conducted in the order from high confidence nodes to low confidence ones by iteratively using trilaterations. At each stage, CIL selectively utilizes trilaterations and reduces the likelihood of using low-confidence references, which effectively alleviates the error propagation.

We validate our design by deploying a prototype system with 24 Telos sensor nodes at the university campus. The results show that QoT well represents trilateration accuracy. Based on the trace data derived from the testbed experiment, we conduct large-scale simulations to examine the efficiency and scalability of the CIL design and compare with previous localization approaches.

The rest of the paper is organized as follows: In Section 2, we formally define QoT. The design of CIL is presented in Section 3. We discuss the prototype implementation and simulation results in Section 4. We summarize related work in Section 5 and conclude this work in Section 6.

# 2 QUALITY OF TRILATERATION

Trilaterations are previously classified as 1) unfeasible, if three references are collinear or 2) feasible, if not. Based on our observation that the geometric relation of reference nodes significantly affects the localization accuracy, we believe a fine-grained evaluation is necessary. The metric of QoT is beyond a binary output function, providing a quantitative evaluation of different forms of trilaterations. To avoid misunderstanding, we use “beacons” to denote the nodes equipped with positioning devices (for example, GPS receiver); while use “references” to denote the localized nodes based on which we can locate other nodes by trilateration. Let $t = \mathrm { T r i } ( s , \{ s _ { i } , i = 1 , 2 , 3 \} )$ denote a trilateration for s based on three reference nodes $s _ { i } . \mathrm { L e t } p ( s )$ be the real location of node s and $p _ { t } ( s )$ be the estimated location of s by trilateration t. Let $d ( s _ { i } , s _ { j } )$ denote the distance between two neighbor nodes si and $s _ { j } .$ We assume it possesses some probability distribution denoted by a probability density function $\dot { f } _ { s _ { i } , s _ { j } } ( x )$ , where $x \in [ 0 , + \infty )$ denotes the distance value. The value of $f _ { s i , s j } ( \boldsymbol { x } )$ depends on the physical features of si and $s _ { j } ,$ and we assume it is known as a priori. Any point p in a 2D plane, the probability density of $p$ being the localization result of $t = \mathrm { T r i } ( s , \{ s _ { i } , i = 1 , 2 , 3 \} )$ Þ, is given by

$$
f _ {t} (p) = \prod_ {i = 1} ^ {3} f _ {s, s _ {i}} (d (p, p (s _ {i}))).
$$

We define $\mathrm { D i s k } ( p , R )$ as a disk area centered at p with radius R. The parameter R is application-specific for different accuracy requirements. The quality of trilateration t is defined as

$$
Q (t) = \operatorname * {P r} (p _ {t} (s) \in \operatorname{Disk} (p (s), R)).
$$

The large value of $Q ( t )$ indicates that the estimate location $p _ { t } ( s )$ is, with high probability, sufficiently close to the real location $p ( s ) ;$ ; and vice versa. Indeed, QoT can be extended to multilateration straightforwardly, but for simplicity of discussion, we focus on the scenario of trilaterations only. The definition of $Q ( t ) .$ , however, does not help much on its calculation since $p ( s )$ is unknown. Adopting the greedy heuristic, we use $\bar { p } ( s )$ instead of $p ( s )$ when calculating QðtÞ, where $\bar { p } ( s ) = \arg \operatorname* { m a x } _ { p } \mathrm { P r } ( p _ { t } ( s ) \in \mathrm { D i s k } ( p , R ) )$ for any point p in the plane. The substitution makes sense as the true position is most likely to occur within the area where the probability density is the highest. Hence,

$$
Q (t) = \operatorname * {P r} (p _ {t} (s) \in \operatorname{Disk} (\bar {p} (s), R)).
$$

![](images/a16381c3524615f53ea671b357f6aedea37ef169444577ae595e22a5ca3ef3e7.jpg)

(a)   
![](images/c13e6a98e3e44d743800a8839fa51b844ab67fae63400c4e996d73e1adf1549e.jpg)



(d）

![](images/eef0697a3cb442c34f143dbe115178d4bb246463838e7223cc1dfdf602a8e019.jpg)

(b)   
![](images/d235975b819734eec50fc4e54332ee0bc87d14264a97e8cfed101a3b9694b01e.jpg)



(e)

![](images/6ad0be73ec0e4fe26ddd37e2070649d01d355d531ac7ee70ad224f7353aff27f.jpg)



(c）  
![](images/153484367272462ea42368dddf361678602b16526b0c3e9d9614af2502675621.jpg)



(f)   
Fig. 2. The impact of geometric relations on QoT.

To calculate QðtÞ, a straightforward way is to integrate the probability density, i.e., $\begin{array} { r } { \bar { Q ( t ) } = \int _ { p } f _ { t } ( p ) d \bar { p } , p \in \mathrm { D i s k } \bar { ( p } ( s ) , R ) } \end{array}$ . In some cases, however, the integral is computationally infeasible for resource-constrained wireless nodes. Hence, the light-weighted sampling method is employed for approximation in our experiments.

To deal with location uncertainty, Least-Squares (LS) optimization [3], [10] is often used to minimize the differences between the measured and estimated distances. Compared to LS-based approaches, QoT provides additional information that indicates how accurate a particular trilateration is. Such difference enables QoT the ability of distinguishing and avoiding poor trilaterations that are of much location uncertainty or potential flip ambiguity.

We conduct simulations to analyze the impact of geometric relationship on QoT. Figs. 2a, 2b, and 2c show the ground truth of three examples of trilaterations. The black circles are the references and the white ones are the nodes to be localized. Considering the widely assumed normal noises in ranging measurements, the corresponding probability distributions are shown in Figs. 2d, 2e, and 2f, respectively. In the first example, Fig. 2d displays the probability distribution of a general case. In the second example, Fig. 2e indicates a high probability of flip ambiguity as three reference nodes almost lie in a line. In the third example, Fig. 2f plots a concentrated probability distribution which is in accord with the fact that three references in Fig. 2c are well separated around the node to be localized.

Other than geometric relation of reference nodes, QoT also considers the ranging noises between pairs of nodes. Specifically, an accurate ranging mechanism results in a relatively concentrated probability distribution, and thus increases the value of QoT.

# 3 CONFIDENCE-BASED ITERATIVE LOCALIZATION

# 3.1 Confidence

The confidence indicates how much we trust the localization result. Suppose a node s is directly localized by trilateration $t = \mathrm { { \hat { T r i } } } ( s , \{ s _ { i } , i = 1 , 2 , 3 \} )$ Þ. The confidence of s based on t is defined as:

$$
C _ {t} (s) = Q (t) \cdot \prod_ {i = 1} ^ {3} C (s _ {i}).
$$

If reference node $s _ { i }$ has relatively low confidence, the confidence of s cannot be high no matter how high $Q ( t )$ is. On the other hand, if confidence of $s _ { i }$ is high, the confidence of s depends on $Q ( t )$ .

In real deployments of wireless networks, a node usually has more than three neighbors, on average, due to the requirement of communication connectivity. By using a heuristic selection, a node to be located chooses the trilateration with the highest confidence to locate itself. Suppose $C T ( s )$ is the set of all candidate trilaterations that can be used to determine the position of s. When locating $s , t _ { \mathrm { m a x } }$ is chosen according to $\bar { t _ { \operatorname* { m a x } } } \bar { = } \arg \operatorname* { m a x } _ { t } ( C _ { t } ( s ) ) , t \in C T \bar { ( s ) }$ .

The confidence of s is accordingly defined as:

$$
C (s) = \left\{ \begin{array}{l l} 1, & \text { if   } s \text {   is   a   beacon }, \\ \max _ {t \in C T (s)} (C _ {t} (s)), & \text { otherwise }. \end{array} \right.
$$

According to the definition, the computation of confidence values is associated with the actual positioning process of trilateration and every node has its confidence value after it has been located.

As shown above, the confidence of a node depends on its neighbors. Due to the bilateral relationship of neighborhood, it is crucial to avoid infinite computation loops by analyzing the termination conditions, which are formulated in Lemma 1.

Lemma 1 (Termination of Confidence Computation). If a node s is localized by a trilateration $t = \mathrm { T r i } ( s , \{ \bar { s } _ { i } , i = 1 , 2 , 3 \} )$ , then $C ( s ) < C ( s _ { i } ) ^ { \mathsf { ^ { \prime } } } f o r a n y s _ { i }$ .

Proof. Without loss of generality, we only prove $C ( s ) <$ $C ( s _ { 1 } )$ . According to the definition of $C ( s )$ , we have

$$
\begin{array}{l} C (s) = C _ {t} (s) \\ = Q (t) \cdot \prod_ {i = 1} ^ {3} C (s _ {i}) \\ \leq Q (t) \cdot C (s _ {1}). \\ \end{array}
$$

As $Q ( t ) < 1$ according to the definition, we have $C ( s ) < C ( s _ { 1 } )$ . tu

Lemma 1 guarantees that if s is located by a reference $s _ { i } ,$ then it is impossible that $s _ { i }$ is located based on s directly or indirectly.

# 3.2 Confidence-Based Iterative Localization

The CIL uses the confidence values as an evaluating indicator during the localization process. Initially, all beacon nodes have the maximum confidence while all other nodes are with the minimum confidence. The computation process is conducted in the order from high-confidence nodes to low-confidence ones by iteratively using trilaterations. In $\operatorname { C I L } , \mathbf { a }$ node receives location information from a number of reference nodes with different levels of confidence. It does not blindly utilize all information from reference nodes any longer. Oppositely, a nonbeacon node elaborately calculates the confidence and selectively uses the trilateration with the highest confidence to locate itself.

In this section, a distributed algorithm for confidence computation is developed based on the Bellman-Ford’s shortest path algorithm. We model the ground truth of a network deployment as a weighted graph $G = ( V , E )$ . All nodes in the network are mapped to vertices in G. In addition, we add a virtual source vertex s to V in order to transfer the confidence computation to the single-source shortest path computation. The edge set $E$ contains all communication links between two nodes and the virtual edges $\{ ( s , b ) |$ b is a beacon vertexg. For any node v, we define $\delta ( v ) = - \log C ( v )$ . Let $t ( u , v )$ denote the set of trilaterations which use u as a reference to locate v. We define

$$
t _ {\max} (u, v) = \underset {t \in t (u, v)} {\arg \max} (Q (t)).
$$

For any edge (u; v), the weight is defined as

$$
w (u, v) = \left\{ \begin{array}{l l} 0, & \text { if } u = s, \\ \infty , & \text { if } u \neq s \text { and } t (u, v) = \phi , \\ - \log (Q (t _ {\max})), & \text { otherwise }. \end{array} \right.
$$

Lemma 2 (Optimal Substructure). Suppose $\delta ( v )$ achieves its minimum value by trilateration $t = \mathrm { { T r i } } ( v , \{ u _ { i } , i = 1 , 2 , 3 \} )$ , then all $\delta ( u _ { i } )$ achieve their minimum values.

Proof. According to the definition of confidence, we have

$$
C (v) = C _ {t} (s) = \prod_ {i = 1} ^ {3} C (u _ {i}) \cdot Q (t).
$$

Thus, $\begin{array} { r } { \delta ( v ) = \sum _ { i = 1 } ^ { 3 } \delta ( u _ { i } ) + w ( u _ { 1 } , v ) } \end{array}$ . Suppose to the contrary that $\delta ^ { \prime } ( u _ { 1 } )$ can be achieved and $\mathsf { \bar { \delta } } ^ { \prime } ( u _ { 1 } ) < \delta ( u _ { 1 } )$ . Then, we obtain a solution of v by

$$
\delta^ {\prime} (v) = \delta^ {\prime} (u _ {1}) + \sum_ {i = 2} ^ {3} \delta (u _ {i}) + w (u _ {1}, v) <   \delta (v),
$$

that contradicts with our assumption. Therefore, $\delta ( v )$ satisfies optimal substructure property. tu

Lemma 3 (Triangle Inequality). For any edge $( u _ { 1 } , v ) \in$ $\begin{array} { r } { E , \delta ( v ) \leq \sum _ { i = 1 } ^ { 3 } \bar { \delta ( u _ { i } ) } + w \bar { ( u _ { 1 } , v ) } } \end{array}$ ; where u2 and u3 are two vertices adjacent to v but different with $u _ { 1 }$ .

Proof. According to the definition of confidence, we have

$$
C (v) \geq \prod_ {i = 1} ^ {3} C \left(u _ {i}\right) \cdot \max _ {t \in t \left(u _ {1}, v\right)} \left(Q (t)\right).
$$

Then, we get

$$
\begin{array}{l} \log (C (v)) \geq \log \left(\prod_ {i = 1} ^ {3} C (u _ {i})\right) + \log \left(\max _ {t \in t (u _ {1}, v)} (Q (t))\right) \\ \Rightarrow - \log (C (v)) \leq - \log \left(\prod_ {i = 1} ^ {3} C \left(u _ {i}\right)\right) - \log \left(\max _ {t \in t \left(u _ {1}, v\right)} (Q (t))\right) \\ \Rightarrow \delta (v) \leq \sum_ {i = 1} ^ {3} \delta \left(u _ {i}\right) + \min _ {t \in t \left(u _ {1}, v\right)} (- \log (Q (t))) \\ \Rightarrow \delta (v) \leq \sum_ {i = 1} ^ {3} \delta \left(u _ {i}\right) + w \left(u _ {1}, v\right). \\ \end{array}
$$

Therefore, our defined $\delta ( v )$ satisfies the triangle inequality. tu

According to Lemmas 2 and $3 , \delta ( v )$ can be viewed as a metric of distance. Based on the Bellman-Ford’s algorithm, a distributed confidence computation algorithm is designed for CIL. Let $d ( v )$ denote the in-process result of $\delta ( v )$ and $p ( v )$ denote the in-process result of the computed location of v. Algorithm 1 is the pseudocode of the proposed CIL algorithm.

# Algorithm 1. Distributed Confidence Computation

1: Initialization: $\mathrm { d } ( \mathrm { v } ) = \mathrm { i n f i n i t y }$ for all nonbeacon nodes and 0 for all beacon nodes.

2: while any neighbor u of v changes $d ( u )$ or $p ( u )$

3: compute $t _ { \operatorname* { m a x } } ( u , v )$ and $w ( u , v )$ $/ /$ suppose $t _ { \mathrm { m a x } } ( u , v ) = \mathrm { T r i } ( v , \{ u _ { i } , i = 1 , 2 , 3 \} )$ $/ /$ without loss of generality, let $u = u _ { 1 }$

4: if $\begin{array} { r } { d ( v ) > \sum _ { i = 1 } ^ { 3 } d ( u _ { i } ) + w ( u , v ) } \end{array}$

5: then

6: compute pðvÞ by $t _ { \operatorname* { m a x } } ( u , v )$

7: $\begin{array} { r } { d ( v ) = \sum _ { i = 1 } ^ { 3 } d ( u _ { i } ) + w ( u , v ) } \end{array}$

8: broadcast new $d ( v )$ and $p ( v )$

9: end

10: end

Theorem 1 (Correctness of Distributed Confidence Computation). Let Algorithm 1 run on a weighted graph $G =$ $( V , E )$ with a source vertex s and a weight function w. For any vertex, it can be localized if the algorithm returns $d ( v ) = \delta ( v ) ;$ while it cannot be located $i f d ( v ) = \infty$ .

Proof. According to Lemmas 2 and 3, -ðvÞ satisfies the optimal substructure and triangle inequality properties. In addition, all edge weights are nonnegative in the definition of the weight function w. Based on the correctness of the Bellman-Ford’s algorithm, Algorithm 1 correctly computes the confidence of each vertex. tu

# 3.3 Location Refinement

Localization is often conducted in a distributed manner, so the computation sequence of nodes cannot be guaranteed. Consequently, we cannot expect that all nodes are localized with the highest confidence if only one opportunity is given. In CIL, the location can be refined whenever a higher confidence location is available. Specifically, in Algorithm 1, nodes reevaluate their locations once they are informed that their neighbors have location or confidence updates. Such kind of flexibility alleviates error propagation by decreasing the chance of error accumulation.

![](images/14141368621e1ab784ced098a562eed8f5058ccaec74cd239b68daf2b322a0e4.jpg)



(a)

![](images/2520caa8c712b5e08108324e09fe394e1bd9b694295908abbaf496ea058c1a1c.jpg)



(b)   
Fig. 3. Comparison of traditional approaches and CIL. (a) Traditional approaches without location refinements. (b) CIL.

For example, Fig. 3a depicts a process of traditional localization algorithms. The nodes labeled 1 and 2 are localized by the other ones (nodes 3-7) at known locations. In previous approaches without location refinement, nodes 1 and 2 end their location computation once they are localized and act as references in the following localization process. Oppositely, in CIL, node 1 continuously evaluates different trilaterations after being localized, as shown in Fig. 3b. After noticed by the location update of node 2, node 1 finds that the newly formed trilateration, based on nodes 2, 3, and 5, has a higher confidence value because the previous trilateration is based on three references (nodes 3, 4, and 5) that are approximately collinear. Thus node 1 recalculates its location based on the new trilateration and informs its neighbors the location update.

# 3.4 Efficiency

In this section, we discuss the efficiency of the proposed CIL algorithm. In most existing localization approaches without the location refinement, nodes are located one by one using trilaterations, so the computation and communication cost increase linearly with the size of networks [11].

As shown in Section 3.3, the mechanism of location refinement enhances the localization accuracy; however, it introduces additional communication and computation cost. For example, once a node refines its location, it instantly broadcasts the new location. Unfortunately, the node cannot stop the localization process based on its old location. As a result, two computation processes based on the latest and the early location are conducted simultaneously in the entire network, although one of them is meaningless. Fig. 4 shows an example of the diffusion of useless information. Suppose the first round of location knowledge is spreading in the network, whose border is denoted by a light-colored curve. After a while, a location update occurs at a node (the bigger one) and it immediately broadcasts the new location, resulting in a second round of location information propagation (denoted by dark-colored curve). The situation can be even worse if a node continuously refines its location and broadcasts the latest information. The number of meaningless information propagations equals to the number of location updates minus one (i.e., all rounds of computation processes except the latest one are wasted).

Multiple location updates for a single node can be attributed to several reasons. First, newly added nodes may change the existing trilateration selection. Figs. 5a and 5b give an example of such situation. At beginning, node 4 is located by trilateration based on nodes 1, 2, and 3, as shown in Fig. 5a. After a while, node 5, a newly installed one, begins to operate. Suppose node 5 has a high-confidence value (e.g., a beacon node); so, node 4 accordingly finds a high-quality trilateration based on nodes 1, 3, and 5 and updates its location, as shown in Fig. 5b.

Second, the physical movement of nodes is another reason for location updates in mobile networks. As illustrated in Fig. 5c, a reference node 2 moves from its original position (gray) to a new position (black) and forms a higher quality trilateration in conjunction with nodes 1 and 3. As a result, node 4 updates its location based on the new position of node 2. For the same reason, the movement of node 4 leads to location updates, as shown in Fig. 5d.

Third, location updates frequently occur even in static networks because of the uncontrolled order of localization processes, illustrated in Fig. 3 in Section 3.3.

![](images/db4fa64ff291b1659a8384568d79b2a7c70194a9a4d2770fa70d76fde427a972.jpg)



Fig. 4. Two processes of location information propagation in a network, and one of which is meaningless.

![](images/44223d14082015f118a8de843d36ddbf0e877e48f586407ceac18b60d2650971.jpg)  
Fig. 5. Cases of location update.

In the following discussion, we focus on how to reduce the communication costs of CIL. As we show, the instant broadcasting causes a large number of message floodings, most of which are actually useless. Therefore, a mechanism of limiting broadcast is desired.

We classify nodes into three states: STABLE, UNSTABLE, and UNKNOWN. Nodes in STABLE have known locations for a considerably long time (i.e., the localization results for them are stable). The STABLE nodes are the only ones that can do instant broadcasting. In the UNSTABLE state, nodes compute their locations continuously; thus, they keep location updating but without instant broadcasting. After a predefined delay time, nodes in UNSTABLE change their state to STABLE and begin to broadcast their locations. All the remaining nodes unaware of locations are in UNKNOWN, and they switch to UNSTABLE and start a timer as soon as they are localized for the first time.

In our simulations, we adopt the mechanism of delayed broadcasting in which nodes stay in UNSTABLE state sufficiently long until the location results become stable. Generally speaking, the predefined time for a node in UNSTABLE state is application-specific for different performance requirements, setting a trade-off between communication costs and the converging speed of localization processes. Large values of such delay time result in a less number of out-of-date location updates as well as a slow propagation speed of location information spreading. In practice, the adoption of delays is necessary; otherwise, the consequent traffic congestion due to message flooding will cause a failure of network communication.

A flexible solution is to assign a Time To Live (TTL) value to each broadcasting message, which indicates how many relays a message should be delivered. For example, a message with a TTL value of k means that this message can reach all k-hop neighbors but not any (k þ 1)-hop neighbors. When a node receives a message, it first updates its location accordingly and decreases the TTL value by 1. If the TTL value is nonzero, it broadcasts its latest location. By doing so, the localization process speeds up k times than the delayed broadcasting which broadcasts the location information only 1 hop at each step. The previous solutions of instant and delayed broadcasting are actually two special cases, corresponding to TTL values of infinity and 1, respectively. Fig. 6 plots two examples of small and large TTL values when a location update occurs in the node denoted by a bigger circle. Nodes within the gray closed curve are in STABLE state, while the ones between gray and black curves are in UNSTABLE state. A large TTL value often brings out a large number of UNSTABLE nodes. Obviously, the TTL value is a trade-off between communication cost and propagation speed of location information. In the following performance evaluations, the TTL is set to be 1 (the delayed broadcasting) to save communication cost.

![](images/e855882d56a285068a165d207cbdae806fbb57f53818b6f93743b7c7a9aaffc5.jpg)



![](images/7e8fc2027f2958e3c93352242dfcd6873a10b3e091140c886e303b0e4729cb61.jpg)



(b)   
Fig. 6. A flexible variant for constraining broadcasting. (a) Influenced area for a small TTL value. (b) Influenced area for a large TTL value.

![](images/b550752a6390d44fa619723328c9ce6a56ac2c9f3b13953f9c907886ac2c0544.jpg)



Fig. 7. The design of experiment.

# 4 PERFORMANCE EVALUATION

We examine the effectiveness of QoT by deploying a prototype system at the university campus. Large-scale simulations are further conducted to examine the algorithm scalability under varied network parameters.

# 4.1 Prototype Experiment

The hardware layer of the prototype is constructed on the T elos motes with Atmel128 processor and CC2420 transceiver. We fit each node with a shelf, which supports the sensor node 150 cm high. We utilize Radio Signal Strength Indication (RSSI) from the transceivers to estimate the distances between nodes. The transmitting power of sensor nodes is set to 1 mW and transmitting range could reach as far as 40 m with more than 90 dbm receiving signal strength. We construct a distance estimator according to the most widely used signal propagation model: the log-normal shadowing model [1]. Due to the coarse and nonmonotone correspondence between the RSSI and distance in the real measurements, the relative error of the distance estimation can be up to 110 percent.

As discussed above, the trilateration quality can be affected by both the geometry and the ranging accuracy. For better understanding the impact of geometric relation of reference nodes, we eliminate the factor of ranging noises by setting all reference nodes the same distances from the node to be localized. The design of the testbed is illustrated in Fig. 7. Twelve references are evenly deployed in a circle with 20 meters radius. The node s to be localized is put at the center of this circle. Thus, s has the same distance (20 meters) from all references. Based on rotational invariance, we fix one of the reference, say $^ { a , }$ at the position of 0 degree; and let the other two references, say b and c, freely choose their positions from 30 to 330 degrees.

The objective of this experiment is to test the effectiveness of QoT. We carry out trilateration based on 100 samples of the distance estimation between references and s. Due to the ranging noises, the localization accuracy is different under various distributions of reference nodes. In Fig. 8a, we calculate QoT at different combinations of positions of b and c. The dark color denotes large value of QoT. As shown, when b and c locate at 120 and 240 degree, respectively, the maximum of QoT is achieved. This result is due to the fact that three references a; b, and c are well separated around s. The dark color in Fig. 8b means a relatively large percentage of high-quality trilateration results obtained from the testbed experiments. It can be observed that, in practice, the localization accuracy is much different when we vary the positions of b and c. Indeed, the similarity of Figs. 8a and 8b leads to the conclusion that QoT well represents the accuracy of trilateration.

# 4.2 Large-Scale Simulation

We generate networks of 600 nodes randomly distributed in a square area. A typical communication range is 20 m and the average degree of network topology is 16. The densely deployed networks help to better exhibit the effectiveness of CIL since more candidate trilaterations can be used when locating a node. We integrate the results from 100 network instances. In our simulations, the distance measurements are obtained from the testbed experiment. Specifically, we measure and record the radio signal strengths at every small distance interval from 1 to 40 m (the maximum communication range in the experiment). Then, all simulations are conducted based on these data traces.

![](images/41fbd8d675e3e79bfec6af928ed2cb316b38ff24fb364f838e0eff13d6d70d40.jpg)



(a)

![](images/19da6aa9ce8ab43836207b6a131cfe5584fd8ef074eb2a3415b26df90aa8cfc7.jpg)



(b)   
Fig. 8. The effectiveness of QoT. (a) QoT. (b) High-quality trilateration.

![](images/28496de6936d7774a7865600dd6ea1f96669c7da78492332e6c2f13d2a0c174b.jpg)



Fig. 9. The impact of ranging error on confidence.

We consider different strategies of choosing candidate trilaterations for comparison. In our proposed CIL, a node always chooses the one which provides the highest confidence. For comparison, we also utilize the strategy of AHLoS [3] (based on RSS ranging) to delegate a class of multihop localization algorithms. In AHLoS, a node estimates its locations by multilaterations based on its neighbor reference nodes. When it is located, it becomes a reference node and assists other nodes in estimating their locations. Different from CIL, nodes in AHLoS are located once they can be located and never change their localization results.

We first explore the impact of ranging error while ignoring the impact of error propagation. This can be done by using the real positions of nodes when they are used as references to locate others. Fig. 9 plots the confidence values at different levels of ranging error. For both strategies, the confidence value decreases upon the increase of the ranging error.

We observe that our proposed CIL always outperforms AHLoS which suggests the positive effects if the geometry is considered. Fig. 10 shows the impact of ranging error on the localization accuracy. For all strategies, the average error linearly increases along with the increasing ranging error. Comparing Fig. 9 with Fig. 10, CIL also succeeds in producing less error than AHLoS.

In multihop localization algorithms, the error propagation needs to be carefully considered since errors in every step accumulate and affect the localization accuracy of sequentially localized nodes. In our simulations, error propagates along with the localization process, as shown in Fig. 11. We calculate the cumulative error of all localized nodes and observe that CIL provides the least speed of error propagation, which is highly desirable for any multihop localization algorithm. Further, the notable gap between AHLoS and CIL in Fig. 11 indicates the geometry plays an important role in error propagation. Even in a 600 nodes network (not very large), the localization error of AHLoS rapidly grows and soon becomes unacceptable.

![](images/70e265d59f5562b6279cac52860d31c7c2cc8b418a30bf01f9d678d8a2b8b05a.jpg)



Fig. 10. The impact of ranging error on accuracy.

Fig. 12 plots the characteristics of error propagation. Nearly 90 percent of nodes have at most 10 m error by CIL. For AHLoS, however, only 60 percent of nodes have less than 10 m error. We believe the percentage of nodes with high accuracy will be even lower in large-scale networks due to error propagation.

The performance gain with location refinement is highlighted in Fig. 13. It is observed that 80 percent of nodes improve their locations. Although the remaining 20 percent of nodes degrade (having negative accuracy gain), the degree of deterioration is small compared to the improvement. Hence, the scheme of location refinement effectively achieves more accurate localization results.

# 5 RELATED WORK

Recent advances in wireless sensor networks attract the attention of a lot of researchers with many efforts made for locating sensors. Existing localization approaches fall into two categories. Range-based approaches [2], [3], [12], [13], [14], [15], [16] assume that nodes are able to measure the distance and/or the relative directions of neighbor nodes. Range-free approaches [17], [18], [19], [20] do not assume such special hardware functionality, and each node merely knows the existence of its neighbor nodes.

![](images/98f4e0e0d31a70028589409659857ae26d48ae1c2dfffd9eaa47613189f48c72.jpg)



Fig. 11. Error propagation.

![](images/f55d9d166eb95f1ef394de8ad204e1e0c35bee78627596759f982c48fb8f20ba.jpg)



Fig. 12. Empirical cumulative function of location errors.

# 5.1 Range-Based Approaches

For range-based approaches, many efforts have been made for the accuracy of localization in several aspects. Some works [1] focus on the radio propagation model, placing hopes on better understanding of radio attenuation. Mathematical models have been established to map signal strength to distance. Since many environmental factors affect wireless signal propagation, however, accurate mapping is often impossible in practice. Some previous works turn their attention to develop new ranging techniques. The propagation-time-based approaches such as TOA and TDOA [2], [3] provide less ranging error than RSS-based approaches. Moreover, the technique of Angle of Arrival (AOA) [14] has also been introduced, which allows nodes to estimate the relative directions between neighbors by setting an antenna array for each node. All of TOA, TDOA, and AOA measurement requires hardware devices expensive in both manufacturing cost and energy consumption. Some works [8], [9] concern the characteristics of error propagation in multihop localization approaches and make efforts to limit such phenomena.

It is also important to analyze the performance of multilaterations, a basic building block of localization. To the best of our knowledge, robust quadrilateral [6] is the first work that considers the geometric relationship of nodes when locating nodes, in which trilaterations are used only when they satisfy the “robustness condition.” The robustness condition is designed based on geometric element (such as line segment and angle) in order to avoid flip ambiguity as much as possible.

Error management [21] has been introduced for iterative localization to prevent error propagation. Similar to CIL, it uses error registries to select nodes that participate in the localization based on their relative contribution to the localization accuracy. CIL differs from that work in 1) quantifying trilateration effects; 2) considering geometric relationship of references during neighbor selection; and 3) employing broadcasting tokens to reduce extra computation and communication costs introduced by location update.

![](images/7b66c184c5300990f9d3bb058aad5eb291dc4bd737f48a4735ded4896dceed03.jpg)



Fig. 13. Accuracy gain from location refinement.

# 5.2 Range-Free Approaches

Due to the hardware limitations and energy constraints of wireless devices, range-free localization approaches are cost-effective alternatives to range-based approaches. Since there is no way of measuring physical distances among nodes, existing range-free approaches largely depend on connectivity measurements with a high density of beacons [18], [19]. Most existing range-free approaches, however, fail in anisotropic networks, where holes exist among nodes. In anisotropic networks [20], the euclidean distances between a pair of nodes may not correlate closely with the hop counts between them because the path between them may have to curve around intermediate holes, resulting in poor localization accuracy. Recently, a distributed method [22] has been proposed to detect hole boundary by using only the connectivity information. Based on that work, REP [17] is proposed to deal with the “distance mismatch” problem in anisotropic networks.

# 6 CONCLUSIONS

Trilateration, as a basic building block of localization, has not yet overcome the challenges of poor ranging measurement, dynamic and noisy environments, and fluctuations in wireless communication. Hence, trilateration-based approaches often suffer from poor accuracy and can hardly be employed in practical applications. To address these challenges, we propose the concept of QoT, which takes both geometric relationship and ranging errors into accounts. Based on QoT, a CIL is accordingly designed. A prototype system for CIL is deployed at the university campus and the results show that QoT well represents trilateration accuracy. Furthermore, intensive large-scale simulations are conducted to examine the efficiency and scalability of the proposed localization approach. Both experiment and simulation results show that the CIL significantly outperforms previous designs.

# ACKNOWLEDGMENTS

Thisworkwas supportedin part by theHongKongRGC grant HKUST6169/07E, the NSFC/RGC Joint Research Scheme N\_HKUST 602/08, the National Basic Research Program of China (973 Program) under grant No. 2006CB303000, the National High Technology Research and Development Program of China (863 Program) under grant No. 2007AA01Z180, and the HKUST Nansha Research Fund NRC06/07.EG01. The preliminary results of this paper were published in the Proceedings of the IEEE ICDCS 2008.

# REFERENCES

[1] S.Y. Seidel and T.S. Rappaport, “914 MHz Path Loss Prediction Models for Indoor Wireless Communications in Multifloored Buildings,” IEEE Trans. Antennas and Propagation, vol. 40, no. 2, pp. 209-217, Feb. 1992.   
[2] N.B. Priyantha, A. Chakraborty, and H. Balakrishnan, “The Cricket Location-Support System,” Proc. ACM MobiCom, 2000.   
[3] A. Savvides, C. Han, and M.B. Strivastava, “Dynamic Fine-Grained Localization in Ad-Hoc Networks of Sensors,” Proc. ACM MobiCom, 2001.   
[4] M. Li and Y. Liu, “Underground Coal Mine Monitoring with Wireless Sensor Networks,” ACM Trans. Sensor Networks, vol. 5, no. 2, Mar. 2009.   
[5] M. Li, Y. Liu, J. Wang, and Z. Yang, “Sensor Network Navigation without Locations,” Proc. IEEE INFOCOM, 2009.   
[6] D. Moore, J. Leonard, D. Rus, and S. Teller, “Robust Distributed Network Localization with Noisy Range Measurements,” Proc. ACM Conf. Embedded Networked Sensor Systems (SenSys), 2004.   
[7] D. Goldenberg, P. Bihler, M. Cao, J. Fang, B. Anderson, A.S. Morse, and Y.R. Yang, “Localization in Sparse Networks Using Sweeps,” Proc. ACM MobiCom, 2006.   
[8] D. Niculescu and B. Nath, “Error Characteristics of Ad Hoc Positioning Systems (APS),” Proc. ACM MobiHoc, 2004.   
[9] K. Whitehouse, A. Woo, C. Karlof, F. Jiang, and D. Culler, “The Effects of Ranging Noise on Multi-Hop Localization: An Empirical Study,” Proc. ACM/IEEE Symp. Information Processing in Sensor Networks (IPSN), 2005.   
[10] D. Niculescu and B. Nath, “Ad Hoc Positioning System (APS),” Proc. IEEE Global Comm. Conf. (GLOBECOM), 2001.   
[11] J. Aspnes, T. Eren, D.K. Goldenberg, A.S. Morse, W. Whiteley, Y.R. Yang, B.D.O. Anderson, and P.N. Belhumeur, “A Theory of Network Localization,” IEEE Trans. Mobile Computing, vol. 5, no. 12, pp. 1663-1678, Dec. 2006.   
[12] C. Peng, G. Shen, Y. Zhang, Y. Li, and K. Tan, “BeepBeep: A High Accuracy Acoustic Ranging System Using COTS Mobile Devices,” Proc. ACM Conf. Embedded Networked Sensor Systems (SenSys), 2007.   
[13] P. Bahl and V.N. Padmanabhan, “RADAR: An In-Building RF-Based User Location and Tracking System,” Proc. IEEE INFOCOM, 2000.   
[14] D. Niculescu and B. Nath, “Ad Hoc Positioning System (APS) Using AoA,” Proc. IEEE INFOCOM, 2003.   
[15] L.M. Ni, Y. Liu, Y.C. Lau, and A. Patil, “LANDMARC: Indoor Location Sensing Using Active RFID,” ACM Wireless Networks, vol. 10, no. 6, pp. 701-710, 2004.   
[16] Z. Yang, Y. Liu, and X.-Y. Li, “Beyond Trilateration: On the Localizability of Wireless Ad-Hoc Networks,” Proc. IEEE INFOCOM, 2009.   
[17] M. Li and Y. Liu, “Rendered Path: Range-Free Localization in Anisotropic Sensor Networks with Holes,” Proc. ACM MobiCom, 2007.   
[18] T. He, C. Huang, B.M. Blum, J.A. Stankovic, and T.F. Abdelzaher, “Range-Free Localization Schemes in Large Scale Sensor Networks,” Proc. ACM MobiCom, 2003.   
[19] Y. Shang, W. Ruml, Y. Zhang, and M.P.J. Fromherz, “Localization from Mere Connectivity,” Proc. ACM MobiHoc, 2003.   
[20] H. Lim and J.C. Hou, “Localization for Anisotropic Sensor Networks,” Proc. IEEE INFOCOM, 2005.

[21] J. Liu, Y. Zhang, and F. Zhao, “Robust Distributed Node Localization with Error Management,” Proc. ACM MobiHoc, 2006.   
[22] Y. Wang, J. Gao, and J. Mitchell, “Boundary Recognition in Sensor Networks by Topological Methods,” Proc. ACM MobiCom, 2006.

![](images/d500640b1230512701114ef4beb28c40b759805d849bf486f66d90f6c0a6a95d.jpg)



Zheng Yang (M’06) received the BS degree in computer science from Tsinghua University, Beijing, China, in 2006. He is currently working toward the PhD degree in the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Hong Kong. His research interests include wireless ad hoc/sensor networks and pervasive computing. He is a student member of the IEEE, the IEEE Computer Society, and the ACM.

![](images/e27723dfcdf580ade074ecc5f876969f216e27deb19277923941b79284b8a311.jpg)



Yunhao Liu (SM’06) received the BS degree from the Automation Department, Tsinghua University, China, in 1995, the MA degree from Beijing Foreign Studies University, China, in 1997, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is currently with the Department of Computer Science and Engineering at The Hong Kong University of Science and Technology. He is a

member of the Tsinghua EMC Chair Professor Group, and also holds adjunct professorship at Xi’an Jiaotong University, Shanghai Tongji University, and Chongqing University. His research interests include wireless and sensor networking, peer-to-peer computing, and pervasive computing. He is a senior member of the IEEE and the IEEE Computer Society and a member of the ACM.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.