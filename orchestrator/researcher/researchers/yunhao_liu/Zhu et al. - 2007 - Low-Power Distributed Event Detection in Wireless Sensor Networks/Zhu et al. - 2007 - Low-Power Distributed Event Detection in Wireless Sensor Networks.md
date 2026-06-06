# Low-Power Distributed Event Detection in Wireless Sensor Networks

Yanmin Zhu, Yunhuai Liu, Lionel M. Ni

Hong Kong University of Science and Technology

{zhuym, yunhuai, ni}@cse.ust.hk

Zheng Zhang

Microsoft Research Asia

zzhang@microsoft.com

Abstract—In this paper we address the problem of energyefficient event detection in wireless sensor networks (WSNs). Duty cycling is a fundamental approach to conserving energy in WSNs. However, it brings challenges to event detection in the sense that an event may be undetected or undergo a certain delay before it is detected, in particular when sensors are low duty-cycled. We investigate the fundamental relationship between event detection and energy efficiency. Based on a simplified network model, we quantify event detection performance by deriving the closed forms of detection delay and detectability. We also characterize the intrinsic tradeoff that exists between detection performance and system lifetime, which helps flexible design decisions for WSNs. In addition, we propose a completely localized algorithm, CAS, to cooperatively determine sensor wakeups. Without relying on location information, CAS is easy to implement and scalable to network density. Theoretical bounds of event detection are also studied to facilitate the comparative study. Comprehensive experiments are conducted and results demonstrate that CAS significantly improves detection performance.

# I. INTRODUCTION

Continuous monitoring and event detection are two major classes of applications for wireless sensor networks (WSNs) [1]. In monitoring applications, sensor nodes regularly report sensory readings. Event detection applications, however, are concerned with detecting events and sensor nodes report data only when an event is detected. In this paper, we focus on WSNs for event detection. Many appealing applications, such as fire surveillance, pollution detection and radiation prevention [2], fall in the class of event detection.

Tiny sensor nodes are very resource-constrained and the most severe constraint is limited energy. It has been a great challenge to obtain long-lived operational WSNs with short-lived sensor nodes. The most effective way to approach longevity is duty cycling (or, putting sensors into power-save mode). Duty cycling, however, brings challenges to the design of WSNs. It degrades event detection since at any time only a fraction of the sensor nodes is active, in particular, when sensor nodes are low duty-cycled. Detection performance concerned by detection applications includes detectability and detection delay. With duty-cycled sensor nodes, an event may be undetected, or is detected but the detection is associated with a certain latency.

We leverage two essential properties of event detection applications to design energy-efficient detection protocols. First, physical events are usually persistent, rather than ephemeral, which can last for seconds or even minutes after their occurrence. Examples for such events are fire, pollution, and radiation. Second, a broad class of applications accepts a certain detection delay. After all, application-level delays for a detected event are inevitable since it takes time for the network to report the event through hop-by-hop transmissions. In our approach, each sensor node sleeps most of the time and wakes up every $\tau _ { c y c l e }$ time units. While in active mode, a sensor detects any potential event that occurs in its vicinity. Let $\tau _ { o n }$ denote the active time in every cycle of $\tau _ { c y c l e } .$ . The duty cycle of the sensor node is

$$
\delta = \tau_ {o n} / \tau_ {\text { cycle }}. \tag {1}
$$

It suggests two ways in (1) to reduce the duty cycle of sensor nodes: either shorten $\tau _ { o n }$ or lengthen $\tau _ { c y c l e } .$ . In practice, $\tau _ { o n }$ is assigned the minimum time needed for detecting and processing of one event. $\tau _ { o n }$ is usually very small, on the order of tens of milliseconds [1]. It is apparent that when $\tau _ { o n }$ is fixed, a longer sensor cycle implies a lower duty cycle. The key, however, is the setting of $\tau _ { c y c l e }$ for a given WSN because it directly influences detection delay and detectability. A longer sensor cycle leads to a longer delay and a lower detectability. In other words, it controls the tradeoff between event detection and energy efficiency.

There are several key issues before such a scheme can be applied in real applications. First, we need to quantify detection delay and detectability given the network parameters. Second, we need a distributed algorithm to schedule sensor wakeups so that detection performance can be optimized. The maximum detection delay for an event is $\tau _ { c y c l e } .$ However, a WSN is usually densely deployed, and it has been reported that as many as 20 sensors can be deployed in one square meter [3]. With dense deployment, detection delay can be much less than $\tau _ { c y c l e }$ if the wakeups of the sensor nodes are elaborately scheduled.

This paper has made the following contributions. First, we investigate in detail the fundamental relationship between event detection and energy efficiency, and characterize the intrinsic tradeoff between detection performance and lifetime extension. Second, we quantify detection performance of a random independent wakeup network by deriving the closed forms of detection delay and detectability. Third, we propose a completely distributed algorithm CAS to schedule sensor wakeups, which significantly reduces detection delay and improves detectability.

# A. Related Work

Many valuable research efforts have been made for energy conservation in WSNs through duty cycling. Energy-quality tradeoffs for objecting tracking were studied in [4]. Probabilistic coverage in WSNs has been studied in the context of object tracking [5]. A testbed of 70 sensor nodes was deployed to detect and track the positions of moving vehicles [6]. In this system, 5% of deployed motes serve as sentries and non-sentries operates at a 4% duty cycle.

A number of algorithms were proposed to turn off redundant sensor nodes while maintaining the sensing coverage. In PEAS [7], a sensor node probes neighbors to find if there is active neighbors. If receiving acknowledgement from an active neighbor, it goes to sleep. Network-provisioning [8] identifies a redundant sensor node whose sensing coverage is jointly covered by its active neighbors. Tian and Georgana [9] noted the underestimation problem that exists in [8] and proposed a randomized algorithm to determine the active schedule of the sensor nodes. Several efforts [10] take both sensing coverage and network connectivity into account. These algorithms provide full sensing coverage and meanwhile maintain network connectivity.

# B. Paper Organization

The rest of the paper is organized as follows. In Section II, we analyze event detection delay and lifetime extension based on a simplified network model. We describe the design of CAS in Section III. Experimental results are presented in Section IV. Finally, we conclude the paper in Section V.

# II. ANALYSIS OF DETECTION AND LIFETIME

# A. System Model

We consider that n sensor nodes are randomly deployed in a unit square field. A sensor node is composed of three major units: processor, sensing device and radio transceiver. Ideally, each unit can have separate power control [11]. We assume that the duty cycle of the transceiver is given, which is subject to the control of communication protocols. We only study the duty cycling of the sensing device. The transceiver does not necessarily have the same duty cycle with the sensing device. The consequent advantage is the increased flexibility for our protocol to work with different communication protocols. It is important to note that a sensor node can actually be attached with multiple sensing devices of different types. For simplification, however, we assume that a sensor node is equipped with a single sensing device throughout the analysis and the protocol design. Later, we call a sensor node just a sensor for short if it is not confused with the sensing device.

In the analysis, we consider a simple algorithm, in which each sensor wakes up periodically, once in every cycle. In the rest of the cycle, the sensor stays in power-save mode. The wakeup selection is random and independent of other sensors. We refer to this algorithm as RIW. We are interested in low duty-cycled WSNs. Thus, we can safely assume that $\tau _ { o n } { \ll } \tau _ { c y c l e } .$ The example timing of three sensors with RIW is shown in Fig. 1.

![](images/4bac1351639b6bc42dc27b47a86e8f31c892801a0d2c56728a85df0c91a13076.jpg)



Fig. 1. The timing of three example sensors using the RIW algorithm

The detection delay of an event, denoted by $D ,$ is defined as the amount of time elapsed from the instant when the event occurs to the instant when the first sensor detects it. D is a random variable because the factors that determine the delay, such as event arrival time, covering sensors and their wakeups, are all unpredictable. The detectability of an event with duration t is the probability that it can be detected by at least one sensor. The detectability of an event is 100% if its duration exceeds the sensor cycle. Although events are usually persistent, we still study the detectability of an event whose duration is shorter than the sensor cycle since it reflects the capability of the network to capture events. We study the detection of any event that occurs anywhere within the field and arrives at any time.

In the rest of this paper, we make the following assumptions.

Binary detection model Each sensor has a sensing range $( R _ { s } )$ . An event is reliably detected by an active sensor if its distance to the sensor is less than the sensing range.   
Time synchronization We assume the time synchronization mechanism is available for loose time synchronization. Protocols for clock synchronization in WSNs can be found in [12], which achieves accuracy on the order of milliseconds.   
• Stationary events After an event has occurred, it remains at the location where it happens.

# B. Detection Analysis

We analyze detection delay and detectability given a fixed sensor cycle. Since $\tau _ { o n }$ is much smaller than $\tau _ { c y c l e , \astrosun }$ we firstly assume that $\tau _ { o n }$ is negligible for analysis simplicity. The complete analysis with consideration of $\tau _ { o n }$ follows. Due to page limitation, we omit proof details.

Lemma 1. A point is covered by k sensors, and their wakeups are fixed values $w _ { i } ,$ and $w _ { i } \geq w _ { i + 1 } , 1 \leq i \leq k - 1$ . The expected delay of any event at this point is

$$
E [ D ] = \frac {1}{\tau_ {\text {cycle}}} \left(\sum_ {i = 1} ^ {k} w _ {i} ^ {2} - \sum_ {i = 1} ^ {k} w _ {i} w _ {(i + 1) \bmod k} - \left(w _ {1} - w _ {k} - \tau_ {\text {cycle}} / 2\right) \tau_ {\text {cycle}}\right). \tag {2}
$$

Note that in Lemma 1, we fix both the set of covering sensors and their wakeups. Next, we relax the assumption of fixed wakeups and give Lemma 2.

Lemma 2. A point is covered by k sensors, whose wakeups are randomly and uniformly selected over $[ 0 , \tau _ { c y c l e ] }$ . The expected delay of any event at this point is $\tau _ { _ { c y c l e } } / ( k + 1 )$ .

The proof of Lemma 2 involves integral calculation and uses the following probability knowledge. Let $W _ { i } , ~ 1 \leq i \leq k$ , denote the sensor wakeups which is a uniform random variable.

Lemma 3. In a unit square field of n sensors deployed according to random uniform deployment, any point is covered by M sensors. The probability mass function of M is given by

$$
P \{M = k \} = \binom {n} {k} \left(\pi R _ {s} ^ {2}\right) ^ {k} \left(1 - \pi R _ {s} ^ {2}\right) ^ {n - k}. \tag {3}
$$

M is a random variable having binomial distribution with parameters $\pi R _ { s } ^ { 2 }$ and n. Next, we relax the assumption in Lemma 2 that the point is covered by a fixed set of k sensors.

Theorem 1. In a unit square field, n sensors with $R _ { s }$ are deployed according to random uniform deployment. The expected delay in the whole field is given by

$$
\mu = \frac {\tau_ {c y c l e} \left(1 - \left(1 + n \pi R _ {s} ^ {2}\right) \left(1 - \pi R _ {s} ^ {2}\right) ^ {n}\right)}{(n + 1) \pi R _ {s} ^ {2}}. \tag {4}
$$

To derive a more accurate analysis of expected delay, we relax the assumption that the length of $\tau _ { o n }$ is negligible. Let h(i) denote the following function

$$
h (i) = \left\{ \begin{array}{l} \tau_ {\text { cycle }} - i \tau_ {\text { on }}, \text {   if   } 0 \leq i <   d \\ 0, \text {   otherwise } \end{array} , \text { where   } d = \left\lfloor \frac {\tau_ {\text { cycle }}}{\tau_ {\text { on }}} \right\rfloor . \right. \tag {5}
$$

Corollary 1. In a unit square field, n sensors with $R _ { s }$ are deployed according to random uniform deployment. The active time of the sensing device in each cycle $i s \ \tau _ { o n } .$ The expected delay in the field is bounded by

$$
\mu = \sum_ {i = 1} ^ {n} \left(\frac {h (i)}{i + 1} \times \binom {n} {i} \left(\pi R _ {s} ^ {2}\right) ^ {i} \left(1 - \pi R _ {s} ^ {2}\right) ^ {n - i}\right). \tag {6}
$$

In what follows, we analyze the detectability. Notice that when the density is low some parts in the field may not be covered by any sensor. As a result, events falling into these parts are never detected. As this phenomenon inherently results from the initial deployment of the sensors, we exclude such events in calculating the expected detectability. We define the detectability as the conditional probability of event detection on the condition that at least one sensor covers the event.

Theorem 2. In a unit square field, n sensors with $R _ { s }$ are $d e \mathrm { - }$ ployed according to random uniform deployment. The detectability of an event with duration $t , t ^ { < } \tau _ { c y c l e }$ , is given by

$$
\chi (t) = 1 - \left(1 - t \pi R _ {s} ^ {2} / \tau_ {\text {cycle}}\right) ^ {n} + \left(1 - \pi R _ {s} ^ {2}\right) ^ {n}. \tag {7}
$$

Corollary 2. In a unit square field, n sensors with $R _ { s }$ are deployed according to random uniform deployment. The active time of the sensing device in each cycle is $\tau _ { o n } .$ The detectability of an event with duration $t , t ^ { < } \tau _ { c y c l e } ,$ is bounded by

$$
\chi (t) = 1 - \sum_ {i = 1} ^ {n} \binom {n} {i} \left(1 - \pi R _ {s} ^ {2}\right) ^ {n - i} \left(\pi R _ {s} ^ {2} (1 - t / h (i))\right) ^ {i}. \tag {8}
$$

# C. Tradeoff Characterization

In general, when the sensing device or the transceiver is active, the processor should also be active to execute appropriate programs. Let $\phi _ { P } , \phi _ { S } ,$ , and $\varPhi _ { R }$ denote the power rates of processor, transceiver, and sensing device, respectively. The duty cycle of the transceiver is denoted by ψ. The lifetime, $\begin{array} { r } { T _ { l i f e } , } \end{array}$ is computed as follows

$$
\Gamma_ {l i f e} = \xi \cdot \left(\psi \times \Phi_ {R} + (\psi + \delta) \Phi_ {P} + \delta \times \Phi_ {S}\right) ^ {- 1}. \tag {9}
$$

Note that in (9), we do not consider the situation where the active time of the transceiver overlaps with that of the sensing device. The power consumption of the processor is computed twice while it should have been counted only once. This implies that the above $\varGamma _ { l i f e }$ is a little smaller than the real lifetime.

The relationship between network lifetime and event detection is very useful for understanding the intrinsic tradeoff between energy efficiency and detection performance. This helps flexible design decisions of different WSNs. We derive tradeoff formulas by combining (4), (7) and (9). We prefer closed formulas as they ease the combination.

Theorem 3. For a network with n randomly deployed sensors whose sensing range is $R _ { s } ,$ the network lifetime as a function of the expected delay is

$$
\Gamma_ {l i f e} (\mu) = \xi \cdot \left(\psi \left(\Phi_ {R} + \Phi_ {P}\right) + y (\mu)\right) ^ {- 1}, \text { where }
$$

$$
y (\mu) = \frac {\tau_ {o n} \left(\Phi_ {S} + \Phi_ {P}\right) \left(1 - \left(1 + n \pi R _ {s} ^ {2}\right) \left(1 - \pi R _ {s} ^ {2}\right) ^ {n}\right)}{\mu (n + 1) \pi R _ {s} ^ {2}}, \tag {10}
$$

and the network lifetime as $a _ { \scriptscriptstyle * }$ function of the expected detectability is

$$
\Gamma_ {l i f e} (\chi) = \xi \cdot \left(\psi \left(\Phi_ {R} + \Phi_ {P}\right) + \eta (\chi)\right) ^ {- 1}, \text { where }
$$

$$
\eta (\chi) = \tau_ {o n} \left(\Phi_ {S} + \Phi_ {P}\right) \left(1 - \sqrt [ n ]{1 + \left(1 - \pi R _ {s} ^ {2}\right) ^ {n} - \chi}\right) \left(t \pi R _ {s} ^ {2}\right) ^ {- 1}. \tag {11}
$$

# III. CAS: COORDINATED WAKEUP SCHEDULING

The analysis of RIW in the previous section reveals that there is a fundamental tradeoff between energy efficiency and detection performance. The network lifetime can be significantly extended by exploiting detection delays. RIW provides us a baseline of event detection with low duty-cycled sensors. It is simple and easy to implement but does not provide optimal detection performance. This is because the sensors that are close to each other may wakeup at about the same time due to the lack of awareness about their neighboring sensors.

It is apparent for applications that smaller delay and higher detectability are more preferable when the duty cycle is fixed. Thus, the key issue is the scheduling of sensor wakeups that can produce minimal delay and maximal detectability when the sensor cycle is fixed. However, wakeup scheduling for a distributed WSN is highly challenging. The sensing coverage of each sensor is different and may partly overlap with those of others. This suggests that an optimal schedule of sensor wakeups at a point may not necessarily be optimal for other points. Our goal is optimal detection within the whole field. In spite of the challenges, we have the instructive observation that the sensors that reside closely should separate their wakeups as much as possible. In light of the observation, we propose CAS, a fully distributed wakeup scheduling algorithm for event detection optimization.

# A. Overview

Before the system starts detecting events, CAS is executed to schedule sensor wakeups at the initialization stage. After CAS finishes, each sensor has determined its wakeup and enters the detecting stage, in which the sensor is alternatively in active mode and sleep mode. In each cycle, a sensor wakes up once at the wakeup time determined at the initialization stage and detects any potential event within its sensing vicinity.

CAS is a fully localized algorithm and every sensor determines its wakeup through multiple rounds of wakeup adjustments based on a joint effort with its neighbors. CAS consists of two components: distributed scheduling coordination and aggressive wakeup adjustment. The former component defines the protocol for distributed coordination and the latter one is the algorithm executed at each sensor to adjust its wakeup. The design details are described in the next subsections. CAS assumes that every sensor is aware of the distance to each of its neighbors.

# B. Distributed Scheduling Coordination

To separate wakeups of nearby sensors, it is essential for each sensor to cooperate with its neighbors. To this end, we need design the protocol defining the distributed coordination among sensors. The key issues here are twofold. First, we need determine for each sensor the set of neighboring sensors that it needs to cooperate with. Second, we need design the coordination protocol through which sensors carry on distributed cooperation.

We introduce a design parameter, cooperative range, denoted by CR. It defines, for every sensor, the set of neighbors, which is within the range of CR from the sensor, to cooperate with in determining its wakeup. It is clear that $0 < C R \leq 2 R _ { s }$ . If two sensors are further than 2Rs from each other, they do not have overlapped sensing coverage, and therefore need not to cooperate. Apparently, CR impacts on detection performance. The impact of CR is studied with simulations in Section V. Here, we assume that the communication range (Rt) is greater than 2Rs, which holds for most sensors.

The CAS state transition diagram is illustrated in Fig. 2. CAS consists of an initial wakeup-exchange phase and multiple rounds of wakeup adjustments. At the initial phase, every sensor randomly selects a wakeup time and informs it to its neighbors using an INIT broadcast. The length of the exchange phase should be such set that every sensor is able to successfully broadcast its INIT. Each sensor maintains a table of the wakeups of its cooperative neighbors. Upon receiving an INIT from a cooperative neighbor, a sensor extracts the wakeup of this sender, and stores it in the table.

![](images/3512557ed938e37938c512e4b7a6501e3e0e95f2e4e9cb5303e992c62634722d.jpg)



Fig. 2. CAS state transition diagram

Multiple rounds of wakeup adjustments follow the exchange phase and each round takes the same period. In each round, a sensor can make at most once wakeup adjustment. At the beginning of each round, a new wakeup is computed based on the wakeups of its cooperative neighbors. How the new wakeup is computed will be discussed in the next subsection. An adjustment request on its wakeup is formed if the new wakeup helps reduce detection delay within its vicinity. Next, sensors should contend for wakeup adjustment to avoid parallel adjustments because of computation dependency of new wakeups.

A simple backoff technique is employed to realize the contention. A timer is started upon the generation of the adjustment request. When the timer fires a sensor broadcasts the UPDT if it holds an adjustment request, and then commits the adjustment on its wakeup. Upon receiving an UPDT, a sensor checks the ID list in this message. If it is included in the list, it suppresses its own timer and hence cancels its adjustment request. Meanwhile, it updates the sender’s wakeup in its local table. The ID list mitigates the problem of asymmetric distance estimation.

The number of adjustment rounds, denoted by NR, is a system design parameter. A small NR incurs less message exchanges but results in a lower degree of optimization. NR should be adaptive to the density of sensors. A higher density needs a larger NR. In simulations, we find that the NR that allows on average two UPDTs per sensor leads to a steady system status.

# C. Aggressive Wakeup Adjustment

Given the wakeups of its cooperative neighbors, a sensor needs to determine whether it should adjust its wakeup and what the new wakeup is. CAS regards the cooperative neighbors as equally important in detecting events within its coverage. It is because they are all close to it and their sensing coverage highly overlaps with its own. This suggests that an event that occurs within its vicinity can probably be detected by any of them.

CAS is a completely localized algorithm, in which each sensor can only manipulate its own wakeup time. For each sensor, it is desirable to evenly distribute the wakeups of its cooperative neighbors and itself over $\tau _ { c y c l e } ,$ which produces the least expected delay and the highest detectability. A wakeup separation is the time difference of two consecutive wakeups. The fundamental property of the evenly distributed wakeups is that the variance of the separations formed by the wakeups is zero. A smaller variance indicates more even distribution of the wakeups. In light of this, each sensor tries to reduce the variance of the wakeup separations seen by it.

The key issue here is how to select the new wakeup so that the variance of the separations can be reduced as much as possible. According to CAS, each sensor takes an aggressive approach to adjusting its wakeup. We consider a sensor G and suppose that it has m cooperative neighbors. CAS considers the wakeup separations formed by the m cooperative neighbors (excluding itself). G identifies the maximum separation and then selects the new wakeup by placing its wakeup in the middle of the maximum wakeup separation. If the resulting new variance is less than the previous one, G will generate a request to update its wakeup.

# IV. PERFORMANCE EVALUATION

# A. Experiment Setting

To evaluate the performance of CAS, we conducted comprehensive simulations. The performance metrics are detection delay and detectability. We adopt the configuration data based on the eXtreme Scale Mote [1]. The simulation setting is shown in Table 1. Event arrival follows the Poisson process. The sensing field is a square with the side length L. To have different deployment densities of sensors, we fix the length of L and vary the number of sensors deployed in the sensing field.

Table 1. Simulation Settings 

<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td> $R_t$ </td><td>20 m</td><td>L</td><td>300 m</td></tr><tr><td> $R_s$ </td><td>8 m</td><td>ξ</td><td>100 J</td></tr><tr><td> $Φ_S$ </td><td>19.4 mW</td><td> $τ_{cycle}$ </td><td>10s</td></tr><tr><td> $Φ_P$ </td><td>24 mW</td><td> $τ_{on}$ </td><td>0.1s</td></tr><tr><td> $Φ_R$ </td><td>24 mW</td><td>n</td><td>3600</td></tr></table>

# B. Results

To study the impact of cooperative range, we vary CR from $0 . I R _ { s }$ to $2 R _ { s } .$ . Fig. 3 and Fig. 4 plot detection delay and detection percentage against CR, respectively. At first, both the mean and the standard deviation of delays decrease gradually as CR increases. They both reach the minimum when CR is around 1.3Rs. Afterwards, the mean and the standard deviation increase as CR increases. This is reasonable because when CR is zero CAS falls back to RIW and when CR is large a sensor over considers those sensors whose coverage actually overlaps little with its own. We observe that the detection percentage increases with increasing CR and reaches the maximum when CR is around 1.3Rs. The two experiments suggest that a good choice for CR is between $[ 1 . 1 R _ { s } , 1 . 4 R _ { s } ]$ .

![](images/d370de187fc484b3790694f30c8f43fccd00acf4bab70a498cb3808b4f3bf6e8.jpg)



Fig. 3. Detection delay vs. cooperative range

![](images/2097344f6d3367735b708c218bfaae4924dc4c2bb47c0f1b7d7c39d0fa3f2a03.jpg)



Fig. 4. Detectability vs. cooperative range

![](images/0d5f4d3a9964cdbb74ab33da81ff1e2388ef6bf764cc8c812f86a56229347655.jpg)



Fig. 5. Delay comparison with different densities

![](images/be2217a0e364670a43ebb6ac326cc1de11c92b12130c56484b6371dc7dc611de.jpg)



Fig. 6. Detectability comparison with different densities, t=2s

![](images/ee6b2665001a2572b5395a684f421c10eee5666e3182cd9d78786178ab2aba36.jpg)



Fig. 7. Delay comparison

![](images/2cc7921346152a632cf90ef7f1ceb589cac31c3dd797420e67e890d27810d19e.jpg)



Fig. 8. Detectability comparison

We present a comparative study, comparing CAS with the theoretical lower bound (LOB), and RIW. It is very difficult to derive the actual lower bounds. We present the lower bounds based on an optimistic model. A point in the field is covered by on average $n \bar { \pi } R _ { s } ^ { ~ 2 } / L ^ { 2 }$ . For this point, the optimal scheduling for these sensors is to evenly separate the wakeups. This results in

$$
\begin{array}{l} \mu_ {L O B} = \tau_ {\text { cycle }} L ^ {2} / 2 n \pi R _ {s} ^ {2}, \sigma_ {L O B} = \sqrt {\tau_ {\text { cycle }} L ^ {2} / 1 2 n \pi R _ {s} ^ {2}}, \\ \chi_ {L O B} (t) = \left\{ \begin{array}{l} t n \pi R _ {s} ^ {2} / \tau_ {\text {cycle}} L ^ {2}, \text {if} t <   \tau_ {\text {cycle}} L ^ {2} / n \pi R _ {s} ^ {2} \\ 1, \text {otherwise} \end{array} , \right. \tag {12} \\ \end{array}
$$

where µLOB, σLOB, and χLOB denote the lower bounds of expected delay, standard deviation and detectability, respectively. The lower bounds are over optimistic and can never be achieved in reality because it is impossible to have such real deployment.

We compare three algorithms in terms of detection delay and detectability under different sensor density configurations in Fig. 5 and Fig. 6, respectively. When studying detectability, we set a short event duration, t=2s. We can see CAS is much superior to RIW and the improvement of CAS over RIW becomes more significant when sensor density is high. To have a more careful look at the improvement, we further show detection delay and detectability for the configuration of 3600 sensors in Fig. 7 and Fig. 8. CAS reduces as high as 35% of the mean of delays compared with RIW. The mean of delays achieved by CAS is only 24% higher than that of LOB. We vary event duration from 1s to 10s in Fig. 8. When the event duration is 1s, CAS increases as high as 25% of detectability compared with RIW.

# V. CONCLUSION

In this paper, we have studied low-power event detection in WSNs. The analysis of event detection and lifetime extension quantifies the detection performance of low duty-cycled detection protocols and reveals the potential lifetime extension by exploiting detection delay. RIW is simple but does not provide optimal detection performance. To improve detection performance, we proposed CAS, which is a fully localized algorithm for detection optimization. CAS only requires minimal knowledge of distances to its neighbors and is scalable to network density. Comprehensive evaluation results demonstrate that CAS significantly improves detection performance in terms of detection latency and detectability.

# ACKNOWLEDGMENT

This research was supported in part by Hong Kong RGC Grant HKUST6183/05E, the Key Project of China NSFC Grant 60533110, and the National Basic Research Program of China (973 Program) under Grant No. 2006CB303000.

# REFERENCES

[1] P. Dutta, M. Grimmer, A. Arora, S. Bibyk, and D. Culler, "Design of a Wireless Sensor Network Platform for Detecting Rare, Random, and Ephemeral Events," in Proceedings of IPSN, 2005.   
[2] S. Brennan, A. Mielke, and D. Torney, "Radioactive Source Detection by Sensor Networks " IEEE Transactions on Nuclear Science, vol. 52, 2005.   
[3] E. Shih, S. H. Cho, N. Ickes, R. Min, A. Sinha, A. Wang, and A. Chandrakasan, "Physical Layer Driven Protocol and Algorithm Design for Energy-Efficient Wireless Sensor Networks," in Proceedings of MobiCom, 2001.   
[4] C. Gui and P. Mohapatra, "Power Conservation and Quality of Surveillance in Target Tracking Sensor Networks," in Proceedings of MobiCom, 2004.   
[5] S. Ren, Q. Li, H. Wang, X. Chen, and X. Zhang, "Probabilistic Coverage for Object Tracking in Sensor Networks," in Proceedings of MobiCom poster, 2004.   
[6] T. He, S. Krishnamurthy, J. Stankovic, T. Abdelzaher, L. Luo, T. Yan, L. Gu, J. Hui, and B. Krogh, "Energy-efficient surveillance systems using wireless sensor networks," in Proceedings of Mobisys'04, 2004.   
[7] F. Ye, G. Zhong, J. Cheng, S. Lu, and L. Zhang, "PEAS: A Robust Energy Conserving Protocol for Long-lived Sensor Networks," in Proceedings of ICDCS, 2003.   
[8] D. Tian and N. D. Georganas, "A Node Scheduling Scheme for Energy Conservation in Large Wireless Sensor Networks," Wireless Communication and Mobile Computing, vol. 3, pp. 271-290, 2003.   
[9] T. Yan, T. He, and J. A. Stankovic, "Differentiated Surveillance for Sensor Networks," in Proceedings of SenSys, 2003.   
[10] X. Wang, G. Xing, Y. Zhang, C. Lu, R. Pless, and C. Gill, "Integrated Coverage and Connectivity Configuration in Wireless Sensor Networks," in Proceedings of SenSys, Los Angeles, CA, USA, 2003.   
[11] V. Shnayder, M. Hempstead, B.-r. Chen, G. Werner-Allen, and M. Welsh, "Simulating the Power Consumption of Large-Scale Sensor Network Applications," in Proceedings of SenSys, Baltimore, MD, 2004.   
[12] J. Elson, L. Girod, and D. Estrin, "Fine-Grained Network Time Synchronization using Reference Broadcasts," in Proceedings of OSDI, Boston, MA, 2002.