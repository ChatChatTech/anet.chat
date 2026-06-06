# Quality of Trilateration: Confidence based Iterative Localization

Zheng Yang and Yunhao Liu

Hong Kong University of Science and Technology

{yangzh, liu}@cse.ust.hk

# Abstract

The proliferation of wireless and mobile devices has fostered the demand of context aware applications. Location is one of the most significant contexts. Multilateration, as a basic building block of localization, however, have not yet overcome the challenges of (1) poor ranging measurement; (2) dynamic and noisy environments; (3) fluctuations in wireless communications. Hence, they often suffer poor accuracy and can hardly be employed in practical applications. In this study, we propose Quality of Trilateration (QoT) that quantifies the geometric relationship of objects and the ranging noise. Based on QoT, we design a confidence based iterative localization scheme, in which nodes dynamically select trilaterations with the highest quality for localization. To validate this design, a wireless sensor network prototype is deployed and results show that QoT well represents trilateration accuracy, and the proposed scheme significantly improve localization performances.

# 1. Introduction

Pervasive and mobile systems for context-aware computing are growing at a phenomenal rate. In most of today’s applications such as Pervasive Medicare, Wireless Sensor Network (WSN) Surveillance, Mobile Peer-to-Peer, etc., location is the most essential context. Many localization algorithms are designed in recent years, among which multilateration plays an important role. By measuring the distance from multiple reference positions, the position of an object can be computed. Figure 1(a) plots an example of trilateration, a form of multilateration, which utilizes three references to calculate an object position in two dimensions. Obviously the object to be localized should locate at the intersection of three circles centered at each reference position. We can determine a unique position by trilateration as long as references are non-linear.

Being quite popular because of the ease of implementation, trilateration based approaches are facing many challenges. First and foremost, although several ranging techniques are developed, including Received Signal Strength (RSS) [8] measurements and propagation time based measurements (e.g. ToA and TDoA) [15], error is inevitable in all of them. For example, RSS techniques estimate the distance between two nodes by assuming a known rate of signal attenuation over distance. Consequently, RSS is sensitive to channel noise, interference, attenuators, and reflection, all of which have significant impact on signal amplitude. RSS also suffers from transmitter, receiver, and antenna variability. For the propagation time based ranging measurements, the signal propagation speed often exhibits variability as a function of temperature or humidity, so we cannot assume the propagation speed is constant across a large field. Moreover, the inaccuracy of synchronization also results in ranging errors.

The noisy distance measurement degrades the quality of trilateration in the following four aspects:

Uncertainty. Figure 1(b) illustrates an example of trilateration under noisy ranging measurement. During our experiments we often met the situation that the three circles do not intersect at a common point. In other words, there does not exist any position satisfying all distance constraints.

Non-consistency. In many cases, one sensor node has many reference neighbors. Any subgroup of them (no less than three) can locate this node by multilateration. The results, however, are typically different under different groups of references, resulting in non-consistency. Thus, when alternative references are available, existing approaches fail to determine which combination of references provides accurate localization.

Ambiguity. Flip [3, 9] is a kind of ambiguity, in which the references create a mirror through which the position can be reflected. The flip ambiguity occurs very often if under noisy ranging measurement.

Error propagation. The results of a multihop localization process are based on a series of single hop multilaterations in an iterative manner [16]. In such a process, errors, coming from each step of multilateration, propagate and accumulate [14, 20].

![](images/790d3ed32b34d3540391f1abbe59081ac63cf7c7116db6196d0b4fde892cd67b.jpg)



![](images/4d2888d749f52f5017493a66d5d0f5fa4e5d1dd807b714dbda754223f56cc644.jpg)



Figure 1: Trilateration

Taking trilateration as a representative of multilateration, we focus on the accuracy issue of localization under noisy ranging measurement. In order to address the above challenges, we first propose the concept of Quality of Trilateration (QoT), which is inspired by the key observation that different geometric forms of trilaterations provide different levels of localization accuracy. The metric QoT quantitatively describes such differences and, more importantly, helps to compare and make choices of trilaterations. This mechanism enables the ability of distinguishing and avoiding poor trilaterations with much uncertainty or potential flip ambiguity.

Based on QoT, a Confidence based Iterative Localization (CIL) scheme is designed, in which each node is assigned a confidence value to indicate its localization accuracy. Initially, all beacon nodes have the maximum confidence while all un-localized nodes are with the minimum confidence. The localization process is conducted in the order from high confidence nodes to low confidence ones by continuously using trilaterations to perform positioning. At each stage, CIL selectively utilizes references and trilaterations, which reduce the likelihood of using low confidence references, effectively alleviating the error propagation.

We validate our design by deploying a prototype system with 24 Telos sensor nodes at university campus. The results show that QoT well indicates the effect of trilaterations. Based on the trace data derived from the implementation, we then conduct large-scale simulations to examine the efficiency and scalability of CIL design as well as compare with previous localization approaches. The results show that CIL significantly outperforms existing localization schemes in terms of accuracy.

The rest of the paper is organized as follows. In Section 2, we formally define QoT. The design of CIL is presented in Section 3. We discuss the prototype implementation and simulation results in Section 4. We summarize related work in Section 5 and conclude this work in Section 6.

# 2. Quality of Trilateration (QoT)

Trilaterations are previously classified as (1) unfeasible, if three references are collinear, or (2) feasible, if not. Based on our observation that the geometric relation of reference nodes significantly affects the localization effect, we believe a fine grained method is necessary. QoT is beyond a binary output function, providing a quantitative evaluation of different forms of trilaterations. Indeed, QoT can be extended to multilateration straightforwardly, but for simplicity of discussion, in this paper we focus on the scenario of trilaterations only.

To avoid misunderstanding, we use “beacons” to denote the sensor nodes equipped with positioning devices (for example, GPS receiver); while use “references” to denote the localized nodes based on which we can locate other nodes by trilateration. Let $t = \operatorname { T r i } ( s ,$ , $\{ s _ { i } , i = 1 , 2 , 3 \}$ ) denote a trilateration for s based on three reference nodes $s _ { i \cdot }$ Let $p ( s )$ be the real location of sensor node s and $p _ { t } ( s )$ be the estimated location of s by trilateration t. Let $d ( s _ { i } , s _ { j } )$ denote the real distance between two neighbor nodes $s _ { i }$ and $s _ { j } .$ We assume it possesses some probability distribution denoted by $f _ { s _ { i } , s _ { j } } ( { \boldsymbol { x } } )$ , where $x \in \ [ 0 , \ + \infty )$ denotes the distance value. Any point $p$ in a 2D plane, the probability density of p is given by

$$
f _ {t} (p) = \prod_ {i = 1} ^ {3} f _ {s, s _ {i}} \left(d \left(p, p \left(s _ {i}\right)\right). \right.
$$

We define Disk(p, R) as a disk area centered at p with radius R. The parameter R is application specified for different requirements of localization accuracy. The quality of trilateration t is defined as

$$
\begin{array}{l} Q (t) = \operatorname * {P r} (p \in D i s k (p (s), R)) \\ = \int_ {p} f _ {t} (p) d p, p \in D i s k (p (s), R). \\ \end{array}
$$

Normally, the real position p(s) is unknown in practice. Thus, we use the estimated value $p _ { t } ( s )$ instead of p(s) to define QoT.

![](images/2782352cc758bce079f9d765565aaf94830f838c9a257c2f99fbc07c44576100.jpg)  
(a)

![](images/2dbb9aa1dcd2d6da34b5848746058e0458a2dc01c49aa971ff088ed394d5e232.jpg)  
(b)

![](images/0228ea9a13a7fff810844de5bb525332f8121418396390f12be8ecf49c6e9fe3.jpg)



(c)

![](images/215d50cf053dbc47d5813d2a93f3b45cdd96f187e5d5e075c42c97d1821ce331.jpg)



(d)

![](images/cfff48decd23e637582fced645a0abb166f4fd199541b78087767c83c334b0d7.jpg)



![](images/8da0ae549070f324f4213d171bc1e6e845fb8bba2e78e5fe3d6c053638b7f0e4.jpg)



(f)   
Figure 2: The impact of geometric relations on QoT

$$
\begin{array}{l} Q (t) = \operatorname * {P r} (p \in D i s k (p _ {t} (s), R)) \\ = \int_ {p} f _ {t} (p) d p, p \in D i s k (p _ {t} (s), R). \\ \end{array}
$$

$$
\text { where } p _ {t} (s) = \underset {p ^ {\prime}} {\arg \max} \operatorname * {P r} (p \in D i s k (p ^ {\prime}, R)).
$$

To deal with location uncertainty, Least-Squares (LS) optimization [11, 16] is often used to minimize the differences between the measured and estimated distances. In LS based approaches, all references are treated equally. Such equality is not always valid due to the inherent difference of ranging noise. According to definition QoT, the determination of $p _ { t } ( s )$ is inclined to the references with smaller noise. This change attempts to serve as a better way to deal with uncertainty other than LS.

We conduct a simulation to analyze the impact of geometric relationship on QoT. Figure 2(a), (b), and (c) show the ground truths of three cases of trilaterations. The solid dots are the references and the soft dots are nodes to be localized. Assuming normal noises in ranging measurement, the corresponding probability distributions are shown in Figure 2(d), (e), and (f), respectively. In the first case, Figure 2(d) displays the probability distribution of a general case. In the second case, Figure 2(e) indicates a high probability of flip ambiguity as three reference nodes almost lie in a line. In the third case, Figure 2(f) plots a concentrated probability distribution which is accord with the fact that three references in Figure 2(c) are well separated around the node to be localized.

Other than geometric relation of reference nodes, the definition of QoT also considers the ranging noise, performing a comprehensive evaluation of trilateration. Generally speaking, accurate ranging measurement provides relatively concentrated probability distribution, and thus increases the QoT.

# 3. Confidence based Iterative Localization

# 3.1 Confidence

The confidence indicates how much we trust the localization result. Suppose a node s is directly localized by trilateration t = Tri(s, {si, i = 1, 2, 3}). The confidence of s based on trilateration t is defined as:

$$
C _ {t} (s) = Q (t) \cdot \prod_ {i = 1} ^ {3} C \left(s _ {i}\right).
$$

If reference node $s _ { i }$ has relatively low confidence, the confidence of s cannot be high no matter Q(t) is. On the other hand, if confidence of $s _ { i }$ is high, the confidence of s depends on Q(t).

In real deployments of WSNs, a sensor node usually has more than three neighbors for communication connectivity. By using a heuristic selection, a non-beacon node chooses the trilateration with the highest confidence to locate itself. Suppose CT(s) is the set of candidate trilaterations, including all trilaterations which can determine the position of s. When locating s, s chooses $t _ { \mathrm { m a x } }$ among these candidate trilaterations according to:

$$
t _ {\max} = \underset {t} {\arg \max} (C _ {t} (s)), t \in C T (s).
$$

The confidence of s is defined as:

$$
C (s) = \left\{ \begin{array}{l l} 1, & \text { if   } s \text {   is   a   beacon } \\ \max _ {t \in C T (s)} (C _ {t} (s)), & \text { otherwise } \end{array} \right.
$$

# 3.2 Confidence based Iterative Localization

The confidence based iterative localization (CIL) is based on the accessional confidence computation. Initially, all beacon nodes have the maximum confidence while all un-located nodes are with the minimum confidence. The computation process is conducted in the order from high confidence nodes to low confidence ones by continuously using trilaterations to perform positioning. In CIL, a sensor node receives information from a number of reference nodes with different levels of confidence. It does not blindly utilize all information from reference nodes any longer. Oppositely, a non-beacon node elaborately calculates the confidence and selectively uses the trilateration with the highest confidence to locate itself.

In this section, a distributed algorithm for confidence computation is developed based on the Bellman-Ford’s shortest path algorithm. We treat the ground truth of a network deployment as a graph $G =$ $( V , E )$ . All nodes in the network are mapped to vertices in G. In addition, we add a virtual source vertex s to V in order to transfer the confidence computation to the single source shortest path computation. The edge set E contains all communication links between two nodes and $\{ ( s , b ) \mid b$ is a beacon vertex}. For any node v, we define $\delta ( \nu ) = - \mathrm { l o g } \ C ( \nu )$ . Let t(u, v) denote the trilaterations which are for v and based on u. We define

$$
t _ {\max} (u, v) = \underset {t \in t (u, v)} {\arg \max} (Q (t)).
$$

For any edge (u, v), the weight is defined as

$$
w (u, v) = \left\{ \begin{array}{c l} 0, & \text { if } u = s \\ \infty , & \text { if } u \neq s \& t (u, v) = \phi \\ - \log (Q (t _ {\max})), & \text { otherwise } \end{array} \right.
$$

# Lemma 1. (Optimal Substructure)

Suppose δ(v) achieves its minimum value by trilateration $t = \mathrm { T r i } ( \nu , \{ u _ { i } , i = 1 , 2 , 3 \} )$ , then all ${ \delta ( { u _ { i } } ) }$ achieve their minimum values.

Proof: According to the definition of confidence, we have

$$
C (v) = C _ {t} (s) = \prod_ {i = 1} ^ {3} C \left(u _ {i}\right) \cdot Q (t).
$$

Thus $\delta ( \nu ) = \sum _ { i = 1 } ^ { 3 } \delta ( u _ { i } ) + w ( u _ { 1 } , \nu )$ . Suppose to the contrary that $\delta ^ { \prime } ( u _ { 1 } )$ can be achieved and $\delta ^ { \prime } ( u _ { 1 } ) \leq \delta ( u _ { 1 } )$ . Then we obtain a solution of v by

$$
\delta^ {\prime} (v) = \delta^ {\prime} (u _ {1}) + \sum_ {i = 2} ^ {3} \delta (u _ {i}) + w (u _ {1}, v) \leq \delta (v),
$$

contradicting with our assumption. Therefore, $\delta ( \nu )$ satisfies optimal substructure property. ■

# Lemma 2. (Triangle Inequality)

For any edge $( u _ { 1 } , \ \nu ) \in E , \delta ( \nu ) \leq \sum _ { i = 1 } ^ { 3 } \delta ( u _ { i } ) + w ( u _ { 1 } , \nu )$ ,

where $u _ { 2 }$ and $u _ { 3 }$ are two vertices adjacent to v but different with $u _ { 1 }$ .

Proof: According to the definition of confidence, we have

$$
C (v) \geq \prod_ {i = 1} ^ {3} C \left(u _ {i}\right) \cdot \max _ {t \in t \left(u _ {1}, v\right)} (Q (t))
$$

Then we get

$$
\begin{array}{l} \log (C (v)) \geq \log (\prod_ {i = 1} ^ {3} C (u _ {i})) + \log (\max _ {t \in t (u _ {1}, v)} (Q (t))) \\ \Rightarrow - \log (C (v)) \leq - \log (\prod_ {i = 1} ^ {3} C (u _ {i})) - \log (\max _ {t \in t (u _ {1}, v)} (Q (t))) \\ \Rightarrow \delta (v) \leq \sum_ {i = 1} ^ {3} \delta \left(u _ {i}\right) + \min _ {t \in t \left(u _ {1}, v\right)} (- \log (Q (t))) \\ \Rightarrow \delta (v) \leq \sum_ {i = 1} ^ {3} \delta \left(u _ {i}\right) + w \left(u _ {1}, v\right) \\ \end{array}
$$

Therefore, our defined $\delta ( \nu )$ satisfies the triangle inequality. ■

According to Lemma 1 and $2 , \delta ( \nu )$ can be seen as a metric of distance. Based on Bellman-Ford’s algorithm, a distributed confidence computation algorithm is designed for CIL. Let d(v) denote the in process result of $\delta ( \nu )$ and $p ( \nu )$ denote the location of v.

Algorithm: Distributed Confidence Computation   
1: while any neighbor u of v changes $d(u)$ or $p(v)$ 2: compute $t_{\max}(u,v)$ and $w(u,v)$ // suppose $t_{\max}(u,v)=\operatorname{Tri}(v,\{u_i,i=1,2,3\})$ // without loss of generality, let $u=u_1$ 3: if $d(v)>\sum_{i=1}^{3}\delta(u_i)+w(u,v)$ 4: then
5: compute $p(v)$ by $t_{\max}(u,v)$ 6: $d(v)=\sum_{i=1}^{3}\delta(u_i)+w(u,v)$ 7: broadcast new $d(v)$ and $p(v)$ 8: end
9: end

# Theorem 1. (Correctness of Distributed Confidence Computation)

Let the above algorithm run on a weighted graph $G =$ $( V , E )$ with a source vertex s and weight function w. For any vertex, it can be localized if the algorithm returns $d ( \nu ) = \delta ( \nu ) _ { ; }$ ; while it cannot if $d ( \nu ) = \infty$ .

Proof: According to Lemma 1 and 2, δ(v) satisfies the optimal substructure and triangle inequality properties.

In addition, all edge weights are nonnegative in the definition of weight function w. Based on the correctness of Bellman-Ford’s algorithm, the proposed distributed algorithm correctly computes the confidence of each vertex. ■

# 3.3 Location Refinement

Localization is often conducted in a distributed manner, so the computation sequence of nodes cannot be guaranteed. Thus, we cannot expect all nodes being localized with the highest confidence if only one opportunity is given. In CIL, the location can be refined whenever a higher confidence location is available. Such kind of flexibility alleviates error propagation by accepting higher confidence location.

For example, Figure 3(a) depicts a process of traditional localization algorithms. The nodes labeled 1 and 2 are localized by other ones which are already aware of their locations. Later nodes 1 and 2 can be references to position other nodes. All nodes end computation once they are localized. In CIL, as shown in Figure 3(b), node 1 continuously evaluates different trilaterations after being localized. After noticed by the location update of node 2, node 1 finds the newly formed trilateration based on node 2. This trilateration is with higher confidence than the previous one because the original references nearly lie in a line. Thus node 1 recalculates its location based on the new trilateration and informs neighbors its location update.

Location refinement enhances the localization accuracy，but it may introduce additional communication and computation cost. For example, once a node refines its location, it instantly broadcasts the new location. Unfortunately, the node is not able to stop the locating process based on its old location. In this situation, the two processes of computation based on the new and old information, respectively, are simultaneously conducted in the entire network, although one of them is meaningless. In our design, we employ a mechanism to constrain the instant broadcasting of new calculated positions of sensor nodes.

![](images/b2e8653a8d7e860143ede59d54e05cb6a7340dfd7555e835c8f2f8a7a4e96d24.jpg)



(a) Traditional

![](images/5f6a56145ef80ffcd5ac5e1ecdbd921bc8a61108994b333382da4bcc1708e3de.jpg)



(b) CIL   
Figure 3: Comparison of traditional approaches and CIL

# 4. Performance Evaluation

We first examine the effectiveness of QoT by deploying a prototype system at HKUST campus. Large scale simulations are further conducted to test the algorithm scalability under varied network parameters.

# 4.1 Prototype Experiment

The hardware layer of the prototype is constructed on the Telos motes with Atmel128 processor and CC2420 transceiver. We fit each node with a shelf, which supports the sensor node 150cm high. We utilize Radio Signal Strength Indication (RSSI) from the transceivers to estimate the distances between nodes. The transmitting power of sensor nodes is set to 1mW and transmitting range could reach as far as 50m with more than -90dbm receiving signal strength. We construct a distance estimator according to the most widely used signal propagation model: the log-normal shadowing model [17]. Due to the coarse and non-monotone correspondence between the RSSI and distance in the real measurements, the relative error of the distance estimation can be up to 110%.

As discussed above, both geometric relation and ranging accuracy affect trilateration quality. For better understanding the impact of geometric relation of reference nodes on localization accuracy, we eliminate the factor of different level of ranging error by setting all reference nodes the same distances form the node to be localized. The design of the testbed is illustrated in Figure 4. Twelve references are evenly deployed in a circle with 20 meters radius. The node s to be localized is put at the center of this circle. Thus, s has the same distance, 20 meters, from all references. Based on rotational invariance, we fix one of the reference, say a, at the position of 0 degree; and let the other two references, say b and c, freely choose their positions from 30 to 330 degrees.

The objective of this experiment is to test the effectiveness of QoT. We use 100 sample distance estimations between references and s for trilaterations. Due to the ranging noise, the localization results are different with each other. The proportion of high quality results depends on the geometric relation of reference nodes. In Figure 5(a), we calculate values of QoT at different combination of positions of b and c. The deep color denotes large value of QoT. As shown, when b and c locate at 120 and 240 degree respectively, the maximum of QoT is achieved. This result is due to the fact that three references a, b, and c are well separated around s. The deep color in Figure 5(b) means a relatively large percentage of high quality results. It can be observed that in practice the localization accuracy is much different when we vary the positions of b and c.

![](images/cee97c8de6aaf3694dedfba6ce2d7c830ce0c12bbfecf856dc7c87d9017030aa.jpg)



Figure 4: The design of experiment

![](images/538fdb372fe57553cca354c75fb1429454e33791e96f1a2a2e7e0d8324e938b0.jpg)  
(a) QoT

![](images/4cfd392b52101b4d65cadef519e98f860469b344b4d4748a059e316c2e2079c7.jpg)



(b) High quality trilateration   
Figure 5: The effectiveness of QoT

Indeed, the similarity of Figures 5(a) and (b) leads to the conclusion that QoT well represents the accuracy of trilateration.

# 4.2 Large-scale Simulation

We generate networks of 600 nodes randomly distributed in a square area. A typical communication range is 40m and the average degree of network topology is 16. The densely deployed networks help to better exhibit the effectiveness of CIL since more candidate trilaterations can be used when locating one node. We integrate the results from 100 network instances.

We consider different strategies of choosing candidate trilaterations for comparison. In our proposed CIL, a node always chooses the one provides the highest confidence. We also utilize the strategy of AHLoS [16] to delegate a class of multihop localization algorithms in which nodes are located indiscriminately once they can be located and never change their localization results. Here we adopt RSS based AHLoS for comparison.

We first explore the impact of ranging error while ignore the impact of error propagation. This can be done by using the real positions of nodes when they are used as references to locate others. Figure 6 plots the confidence values at different levels of ranging error. For both strategies, the confidence value decreases upon the increase of the ranging error.

We observe that our proposed CIL always outperforms AHLoS which suggests the positive effects if geometric relationship is considered. Figure 7 shows the impact of ranging error on the localization accuracy. For all strategies, the average error linearly increases along with increasing ranging error. CIL also succeeds in producing the less error then AHLoS. Comparing Figure 6 and Figure 7, CIL provides better localization results than the traditional localization algorithm. The typical localization errors of sensor nodes, when use different strategies, are provided in Figure 8.

In multihop localization algorithms, the error propagation needs to be carefully considered since errors in every step accumulate and affect the localization accuracy of sequential localized nodes. In our simulations, error propagates along with the localization process are shown in Figure 9. We calculate the cumulative error of all localized nodes and observe that CIL provides the least speed of error propagation, which is desirable for a multihop localization algorithm. Further, the notable gap between AHLoS and CIL indicates the importance of geometric relationship on multihop localization algorithms. Even if in a 600 nodes network (not very large), the localization error of AHLoS rapidly grows and finally becomes unacceptable.

Figure 10 plots the characteristics of error propagation. As shown, nearly 90% of nodes have at most 10m error by CIL. For AHLoS, however, only 60% of nodes have less than 10m error. We believe the percentage of high accuracy localized nodes will be even lower in large-scale sensor networks due to error propagation.

The gain of localization accuracy in case location refinement is used is highlighted in Figure 11. It is observed that 80% of nodes improve their locations. Although the remaining 20% of nodes degrade, the degree of deterioration is small compared to the improvement. Hence, location refinement effectively achieves more accurate localization results.

# 5. Related Work

Existing localization approaches fall into two categories. Range-based approaches [1, 10, 12, 15, 16, 21] assume that sensor nodes are able to measure the distance and/or the relative directions of neighbor nodes. Range-free approaches [2, 4-6, 13, 18] do not assume such special hardware functionality, and each sensor node merely gets the existence of its neighbor nodes.

![](images/f81ae145b3169d2268994cadc375bb97d223019bf32f4ead7a22fe96f74332fc.jpg)



Figure 6: The impact of ranging error on confidence

![](images/42209ad77c63c459c23087e96bec183e7e35ecfd350a8feed62b2f89437ed963.jpg)



Figure 7: The impact of ranging error on accuracy

![](images/0d1f6e948454d82f75726ebb947714434eb9d0d8d97cf12abd1b753637c6c0f7.jpg)



Figure 8: Localization errors of sensor nodes

![](images/9fc80e7998e6f88f539f353449c9696308ef0cc1d066453f33a7f5cf96ab40c7.jpg)



Figure 9: Error propagation

![](images/f6bcb9faf0bc5406d4830b0c4c8d47e2c86286de8f2fa15a900764217781e728.jpg)



Figure 10: Empirical cumulative function of location errors

![](images/c415dd42d80fa88962090d4c1fa9a6ed729f674dd1230aaa65452cca378c8aba.jpg)



Figure 11: Accuracy gain from location refinement

# 5.1 Range-based Approaches

For range-based approaches, many efforts have been made for the accuracy issues of localization in several aspects. Some works [8, 17] focus on the radio propagation model, placing hopes on better understandings of radio attenuation. Mathematical models have been established to map signal strength to distance. Since many environmental factors affect wireless signal propagation, however, it is difficult to map the signal strength to distance. Some previous works turn their attention to develop new ranging techniques. The propagation time based approaches such as Time of Arrival (TOA) and Time Difference of Arrival (TDOA) [15, 16] provide less ranging error than RSSI based approaches. Moreover, the technique of Angle of Arrival (AOA) [12] has also been introduced, which allows nodes to estimate the relative directions between neighbors by setting an antenna array for each node. All of TOA, TDOA, and AOA measurement requires hardware devices expensive in both manufacture cost and energy consumptions. Some works [14, 20] concern the characteristics of error propagation in multihop localization approaches and make efforts to limit such phenomena.

It is also important to analyze the performance of multilaterations, a basic building block of localization. To the best of our knowledge, robust quadrilateral [9] is the first work that considers the geometric relationship of nodes when locating sensors, in which trilaterations are used only when they satisfy the robustness condition. The robustness condition is designed based on geometric element (such as line segment and angle) in order to avoid flip ambiguity as much as possible.

Error management [7] has been introduced for iterative localization to prevent error propagation. Similar to CIL, it uses error registries to select nodes that participate in the localization based on their relative contribution to the localization accuracy. CIL differs from that work in (1) quantifying trilateration effects; (2) considering geometric relationship of references during neighbor selection; (3) employing broadcasting tokens to reduce extra computation and communication cost introduced by location update.

# 5.2 Range-free Approaches

Due to the hardware limitations and energy constraints of sensor devices, range-free localization approaches are cost-effective alternatives to range-based approaches. Since there is no way of measuring physical distances among nodes, existing range-free approaches largely depend on connectivity measurements with a high density of seeds [4, 18]. Most existing range-free approaches, however, would fail in anisotropic sensor networks, where holes exist among sensor nodes. In anisotropic networks [6], the Euclidean distances between a pair of nodes may not correlate closely with the hop counts between them because the path between them may have to curve around intermediate holes, resulting poor localization accuracy. Recently, a distributed method [19] has been proposed to detect hole boundary by using only the connectivity information. Based on that work, REP [5] is proposed to deal with the “distance mismatch” problem in anisotropic networks.

# 6. Conclusions

Trilateration, as a basic building block of localization, have not yet overcome the challenges of poor ranging measurement; dynamic and noisy environments; and fluctuations in wireless communication. Hence, they often suffer poor accuracy and can hardly be employed in practical applications. To address these challenges and truly adopt dilatation approaches in practical applications, in this study, we propose the concept of QoT, which takes both geometric relationship and ranging errors into accounts. Based on QoT, a confidence based iterative localization approach, CIL, is designed. A prototype is deployed at HKUST campus and the results show that QoT well represents trilateration accuracy. Furthermore, intensive large-scale simulations are conducted to examine the efficiency and scalability of the proposed localization approach. Both experiment and simulation results show that the CIL significantly outperforms previous designs.

# Acknowledgements

This work is supported in part by the Hong Kong RGC grant HKUST6169/07E, the National Basic Research Program of China (973 Program) under grant No. 2006CB303000, the National High Technology Research and Development Program of China (863 Program) under grant No. 2007AA01Z180, HKUST Nansha Research Fund NRC06/07.EG01, and NSFC Key Project grant No. 60533110.

# Reference

[1] P. Bahl and V. N. Padmanabhan, "RADAR: An In-Building RF-Based User Location and Tracking System," in Proceedings of IEEE INFOCOM, 2000.   
[2] N. Bulusu, J. Heidemann, and D. Estrin, "GPS-less Low Cost Outdoor Localization for Very Small Devices," IEEE Personal Communications Magazine, 2000.   
[3] D. Goldenberg, P. Bihler, M. Cao, J. Fang, B. Anderson, A. S. Morse, and Y. R. Yang, "Localization in Sparse

Networks using Sweeps," in Proceedings of ACM MobiCom, 2006.   
[4] T. He, C. Huang, B. M. Blum, J. A. Stankovic, and T. F. Abdelzaher, "Range-Free Localization Schemes in Large Scale Sensor Networks," in Proceedings of ACM MobiCom, 2003.   
[5] M. Li and Y. Liu, "Rendered Path: Range-Free Localization in Anisotropic Sensor Networks with Holes," in Proceedings of ACM MobiCom, 2007.   
[6] H. Lim and J. C. Hou, "Localization for Anisotropic Sensor Networks," in Proceedings of IEEE INFOCOM, 2005.   
[7] J. Liu, Y. Zhang, and F. Zhao, "Robust Distributed Node Localization with Error Management," in Proceedings of ACM MobiHoc, 2006.   
[8] D. Lymberopoulos, Q. Lindsey, and A. Savvides, "An Empirical Characterization of Radio Signal Strength Variability in 3-D IEEE 802.15.4 Networks Using Monopole Antennas," in Proceedings of EWSN, 2006.   
[9] D. Moore, J. Leonard, D. Rus, and S. Teller, "Robust Distributed Network Localization with Noisy Range Measurements," in Proceedings of ACM SenSys, 2004.   
[10] L. M. Ni, Y. Liu, Y. C. Lau, and A. Patil, "LANDMARC: Indoor Location Sensing Using Active RFID," in Proceedings of IEEE PerCom, 2003.   
[11] D. Niculescu and B. Nath, "Ad hoc Positioning System (APS)," in Proceedings of IEEE GLOBECOM, 2001.   
[12] D. Niculescu and B. Nath, "Ad Hoc Positioning System (APS) using AoA," in Proceedings of IEEE INFOCOM, 2003.   
[13] D. Niculescu and B. Nath, "DV Based Positioning in Ad hoc Networks," Journal of Telecommunication Systems, 2003.   
[14] D. Niculescu and B. Nath, "Error Characteristics of Ad Hoc Positioning Systems (APS)," in Proceedings of ACM MobiHoc, 2004.   
[15] N. B. Priyantha, A. Chakraborty, and H. Balakrishnan, "The Cricket Location-Support System," in Proceedings of ACM MobiCom, 2000.   
[16] A. Savvides, C. Han, and M. B. Strivastava, "Dynamic Fine-grained Localization in Ad-hoc Networks of Sensors," in Proceedings of ACM MobiCom, 2001.   
[17] S. Y. Seidel and T. S. Rappaport, "914 MHz Path Loss Prediction Models for Indoor Wireless Communications in Multifloored Buildings," IEEE Transactions on Antennas and Propagation, vol. 40, pp. 209-217, 1992.   
[18] Y. Shang, W. Ruml, Y. Zhang, and M. P. J. Fromherz, "Localization from Mere Connectivity," in Proceedings of ACM MobiHoc, 2003.   
[19] Y. Wang, J. Gao, and J. Mitchell, "Boundary Recognition in Sensor Networks by Topological Methods," in Proceedings of ACM MobiCom, 2006.   
[20] K. Whitehouse, A. Woo, C. Karlof, F. Jiang, and D. Culler, "The Effects of Ranging Noise on Multi-hop Localization: An Empirical Study," in Proceedings of ACM/IEEE IPSN, 2005.   
[21] Z. Yang, M. Li, and Y. Liu, "Sea Depth Measurement with Restricted Floating Sensors," in Proceedings of IEEE RTSS, 2007.