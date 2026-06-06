Received July 14, 2019, accepted July 27, 2019, date of publication August 2, 2019, date of current version August 28, 2019.

Digital Object Identifier 10.1109/ACCESS.2019.2933150

# A Two-Stage RPSO-ACS Based Protocol: A New Method for Sensor Network Clustering and Routing in Mobile Computing

XIAOHUI WANG , HAORAN GU, YUNHAO LIU, AND HAO ZHANG

School of Aeronautics, Beihang University, Beijing 100191, China

Corresponding author: Xiaohui Wang (xhwang@buaa.edu.cn)

This work was supported in part by the National Natural Science Foundation of China under Grant 41804165, and in part by the Key Laboratory of Spacecraft Design Optimization and Dynamic Simulation Technologies, Ministry of Education.

ABSTRACT In the field of mobile computing, after the placement of sensor nodes, energy efficiency of data transmission in the sensor network is becoming a critical issue as the sensor nodes are battery-operated devices. Most of the proposed protocols implement clustering based methods in order to balance the energy consumption among the sensor nodes through data aggregation. In this paper, a new method named a two-stage RPSO-ACS based protocol is proposed to improve the energy efficiency and network operation quality in the data transmission process, prolonging the lifespan of the network. Firstly, in the process of cluster head (CH) selection, the resampling particle swarm optimization (RPSO) is introduced, which shows better precision and efficiency than particle swarm optimization (PSO) and genetic algorithm (GA). Secondly, after the selection of cluster head, instead of the single-hop transmission from the cluster heads to base station (BS), which is used in many papers, we adopt multi-hop transmission to save energy. The ant colony optimization (ACO) is used to select the relay nodes between the cluster heads and the base station for the purpose of minimizing the energy consumption in the transmission process. In addition, we determine the reasonable threshold based on the energy consumption curve of the transmission. In this way, the nodes within a radius of the threshold from BS communicate with BS directly to save energy. Experimental results show that the proposed methods achieve the goal of improving the energy efficiency and operation quality of the sensor network in comparison to traditional methods.

INDEX TERMS Sensor network, energy efficiency, RPSO-ACS based protocol, resampling particle swarm optimization, ant colony algorithm.

# I. INTRODUCTION

In mobile computing, wireless sensor networks (WSN) has emerged as powerful platforms in many different applications to percept information and transmit data. For surveillance and security, camera sensor nodes need to be deployed in the target area. Since all the nodes run on battery, when the battery runs out, the node is dead. Therefore, it is of great significance to utilize the energy of the sensor network optimally after placement. In this way, after transmitting a certain amount of data, the total energy consumption would be lower, the alive nodes would be more and the coverage of the sensor network would be better.

To address this problem, many researchers have proposed different kinds of solutions [1], [2]. The basic method

The associate editor coordinating the review of this manuscript and approving it for publication was Xuxun Liu.

is to transfer information from all sensor nodes to the base station (BS) directly. However, this method consumes too much energy, especially for nodes far away from BS. To improve the efficiency, an effective relay selection scheme for prolonging the lifetimes of nodes is designed based on the battery-friendly nature of the battery [3], but the quality of surveillance decreases. Clustering mechanisms are more suitable for sensor networks with continued data flowing. At each round, the network is divided into several clusters, all the sensor nodes transmit data to their respective CH and every CH aggregates data and forwards them to the BS [4]. A representative clustering protocol is called the LEACH [5] which selects cluster heads randomly and performs data aggregation processes in the clusters at each round. Compared to the LEACH, PEGASIS [6] consumes less energy per round. LEFC [7] cluster the sensor network by local information of the nodes. Though these methods improve the energy efficiency to some extent, the cluster distribution of them is uneven, which causes the unbalance energy consumption of sensor nodes. In this way, some nodes might die quickly and the network surveillance quality could be affected.

In recent years, swarm based optimization algorithms are used in the routing protocols as an efficient way. Ant colony optimization (ACO), simulating the behavior of ants when finding food sources [8], is a candidate method for multi-path routing to maximize network life time [9]. But the drawback of multi-path routing is that a large amount of data flow through the nodes near the BS, making them die immediately. Particle swarm optimization (PSO) [10], which simulates the flock of birds searching for food, is used in LEACH based routing. Latiff et al. [11] introduce the PSO-based clustering (PSO-C), which is considered as an energy-aware routing protocol that adopts the PSO technique to construct clusters. In [12]–[15], PSO is used to establish clusters and select CHs in a WSN. The optimization target is to minimize the intra-cluster distance and maximize the energy of selected CHs. So the cluster distribution is more uniform and results are better than LEACH. However, PSO is still easy to get trapped in local optimum prematurely. After some iterations, some particles might still be far away from the potential optimal position, which called ’moving lag’. Furthermore, they ignore how CHs send the aggregated data to BS. Each CH transmit data to BS directly, which is unrealistic. If a CH is far away from BS, the energy consumption of communication would beyond our acceptability. An improvement in their research is that a CH select other CHs between itself and BS as relay nodes, so the communication distance of it would decrease. But the routes of CH towards BS are always not the optimal path which consumes the least energy. In addition, because most of CHs also act as a relay node, the energy consumption on them become much larger, making them easy to die, which increases the load imbalance of sensor network.

Some studies try other methods such as using mobile sink node [16]–[18], [21]. The mobile sink node travels across the sensing area to collect data from CHs. In this way, when transmitting data, the communication distance between CHs and sink node would be much smaller so that the energy consumption is reduced greatly. In [19], both static and mobile sinks are used. Wang et al. [20] utilizes multiple mobile sink nodes to collect data in the WSN. The rationale velocities and first positions of the sinks are studied. The results shows that network lifespan is improved as the number of sink nodes is increased up to a definite point. However, in the data collection process, only the CHs near the mobile sink send data to it, while others are inactive, which influences the network monitoring effect. Some important information might not be transmitted in time, leading to serious consequence.

In conclusion, the previous work either use cluster based strategy which fail to make an optimal plan about how CHs transmit data to BS or use mobile BS which decreases the network monitoring effect. To make a better plan, we propose a new protocol: a two-stage RPSO-ACS optimization method for clustering and routing of sensor networks.

![](images/9bd99028e5f95c64fef7b165aa84e196da57c6dab8a333b81db055a0996937aa.jpg)



FIGURE 1. Sit of nodes.

In our previous work, the RPSO combined with the hierarchical strategy is used to address the coverage optimization problem of sensor network [22].

In this paper, we assume that the camera nodes have been placed optimally to gain the best coverage ratio as shown in Fig.1, and then on the basis of it we propose a two-stage RPSO-ACS based protocol to improve the energy efficiency and network surveillance quality in the data transmission process, prolonging the lifespan of the network. Firstly, the energy consumption curve of the transmission is analyzed. All the nodes are classified into two groups according to the distances between them and BS. The nodes near the BS transmits information to the BS directly to save energy while others goes to clustering process. Then, in the clustering process at each round, we adopt the resampling particle swarm optimization(RPSO) [23], which is introduced in our previous work. Compared with PSO, RPSO has better computational efficiency and it is easier to jump out from local optimum. Our objective of the clustering is to select the nodes with the highest energy and minimize the intra-cluster distance. And then each node sends data to its corresponding cluster head. After the cluster heads have aggregated the data, the Ant Colony System (ACS) is used to select the relay nodes between each cluster head and BS, finding optimal transmission path which consume the least energy.

The contributions of this paper can be summarized as follows:

• A new transmission strategy is proposed. The energy consumption curve of the transmission is analyzed, then the range could be determined so that the nodes around the base station transmits information to the base station directly to save energy;

• The resampled particle swarm optimization (RPSO) algorithm is utilized to select the cluster head, improving the optimal solutions significantly compared to PSO;

• After the selection of cluster head, instead of the single-hop transmission from the cluster heads to BS, we adopt multi-hop transmission to save energy. The ant colony algorithm is used to select the relay nodes between the cluster heads and the base station, so that the energy consumption in the transmission process is the lowest.

![](images/da7b52ef2b402f97cfe147594d106e572f7c478a195c095122d81a09346c71c9.jpg)



FIGURE 2. Radio energy consumption model.

The rest of the paper is organized as follows. In Sect. II, the model of the two-stage RPSO-ACS protocol is described. In Sect. III, we introduce the resampling particle swarm optimization(RPSO) and ant colony optimization (ACO). Then experimental results are presented and analyzed in Sect. IV. In Sect. V, we conclude the paper, pointing out the directions for the future works.

# II. THE MODEL OF THE PROBLEMS

# A. THE NETWORK MODEL

The methods of finding the optimal deployment of the camera sensor network to get the best coverage is introduced in [22]. We apply the methods in a 500 ∗ 500 monitoring region with 300 camera nodes, the working radius $r _ { s }$ of all the camera nodes is 30m and the angle of view is $\pi / 4$ . The placement of the nodes after optimization is shown in Fig.1. The initial energy of each node is 1J.

The following basic assumptions are made in this paper:

• Sensors are homogeneous;   
• Sensors have the same initial energy;   
• There is no obstacle between each pair of sensor nodes;

# B. ENERGY MODEL

The energy model used here is described in [8]. As shown in Fig.2, the transmitter consumes energy to run the radio electronics and the power amplifier, and the receiver consume energy to run the radio electronics.

$$
\begin{array}{l} E _ {T} (k, d) = E _ {T - e l e c} + E _ {T - a m p} \\ = E _ {T - e l e c} + k \times \varepsilon_ {a m p} \times d ^ {n} \\ = \left\{ \begin{array}{l} k \times E _ {e l e c} + k \times \varepsilon_ {f s} \times d ^ {2}, d \leq d _ {0} \\ k \times E _ {e l e c} + k \times \varepsilon_ {m p} \times d ^ {4}, d > d _ {0} \end{array} \right. \tag {1} \\ \end{array}
$$

$$
E _ {R} (k) = k \times E _ {\text { elec }} \tag {2}
$$

$$
d _ {0} = \sqrt {\varepsilon_ {f s} / \varepsilon_ {m p}} \tag {3}
$$

TABLE 1. Simulation parameters of RPSO-ACO protocol. 

<table><tr><td colspan="2">Simulation parameters of hybrid RPSO-ACO algorithm</td></tr><tr><td>Parameter</td><td>Value</td></tr><tr><td>Sensor field region ( $m^{2}$ )</td><td>(500*500)</td></tr><tr><td>Base station location (m)</td><td>(400,250)</td></tr><tr><td>Number of nodes (n)</td><td>300</td></tr><tr><td>Initial energy of a node ( $E_{0}$ ) (J)</td><td>1</td></tr><tr><td>Data packet length ( $k_{1}$ ) (bit)</td><td>4000</td></tr><tr><td> $E_{elec}$  (nJ/bit)</td><td>50</td></tr><tr><td> $\varepsilon_{fs}$  (pJ/bit/ $m^{2}$ )</td><td>10</td></tr><tr><td> $\varepsilon_{mp}$  (pJ/bit/ $m^{4}$ )</td><td>0.0013</td></tr><tr><td>visual angle</td><td> $\pi/4$ </td></tr><tr><td>visual range (m)</td><td>30</td></tr></table>

where $E _ { T }$ is the energy cost by data transmission and $E _ { R }$ is the energy cost by data reception. $E _ { e l e c } , \ \varepsilon _ { f s }$ and $\varepsilon _ { m p }$ respectively represents the energy required by the electronic circuit, the amplification coefficient of the amplifier in free space and the amplification coefficient of the amplifier in the multipath. $\varepsilon _ { m p }$ is used when the transfer distance is larger than threshold d0. k is the number of bits of data transmitting.

For the simulations described in the paper, the parameters are shown in Tab.1

# C. FILTER CLOSE-RANGE NODES

After all the sensor nodes are deployed in an optimal manner to maximum the coverage of the network [22], they become stationary. Similar to LEACH, the network operating time is divided into rounds. In each round, all the sensor nodes collect the data within its detection range. All the nodes are divided into two groups: the nodes near the base station (BS) transmit the data directly to the base station and other nodes send data to their corresponding cluster head (CH).

Based on the energy model, the energy consumption per bit of transmitting and receiving data depends on the number of transmission and d. We can see that if the distance between BS and sensor node is sufficiently small then the energy consumption is small for direct communication in comparison to cluster based communication.

As shown in $\mathrm { F i g } . 3 _ { \mathrm { \scriptsize { i } } }$ , where $d _ { 1 }$ is the distance between BS and sensor node, $d _ { 2 }$ is the distance between sensor node and cluster head, $d _ { 3 }$ is the distance between cluster head and station. The energy consumption for direct communication to BS is shown in (5), the energy consumption for cluster based communication is presented in (5). Even though $d _ { 2 }$ and $d _ { 3 }$ are close to 0, the consumption for cluster based communication is Equation (6), if Equation (7) is satisfied, the energy consumption for direct communication $E _ { n - B S }$ would be smaller than the consumption for cluster based communication $E _ { n - C H - B S }$ .

As shown in Fig.4, we can see if the distance between base station and sensor node is within 93.65m, Equation (7) is satisfied, which means the energy consumed by direct transmission to BS is less than which consumed by cluster based communication $( E _ { d 1 } < E _ { d 2 } + E _ { d 3 } )$ , so in our method, the nodes within a radius of 93.65m from BS communicate with BS directly to save energy.

![](images/ef2ad6c0309c40a5bc4b48711defff7c72b71079fe75602d8b6fa354e970f2b8.jpg)



FIGURE 3. Communication to BS.

![](images/bd0cad3dec064b10d224df94015534e460171fc262ff0a790b7c69c825715581.jpg)



FIGURE 4. Energy consumption of amplifier.

$$
E _ {n - B S} = k \times E _ {e l e c} + k \times \varepsilon_ {a m p} * d _ {1} ^ {n} \tag {4}
$$

$$
\begin{array}{l} E _ {n - C H - B S} = 3 \times k \times E _ {e l e c} + k \times \varepsilon_ {a m p} \times d _ {2} ^ {n} \\ + k \times \varepsilon_ {a m p} \times d _ {3} ^ {n} \tag {5} \\ \end{array}
$$

$$
E _ {n - C H - B S} = 3 \times k \times E _ {e l e c} \tag {6}
$$

$$
k \times \varepsilon_ {a m p} \times d _ {1} ^ {n} <   2 \times k \times E _ {e l e c} \tag {7}
$$

# D. DIVIDING CLUSTERS

Then at each round, the cluster heads are elected by RPSO based on their locations and energy in the nodes group which beyond a radius of 93.65m from BS. The number of clusters takes up 5% of the number of all nodes alive [2]. To optimize the selection of cluster heads, the following objective function is used to compute the optimum:

$$
f _ {o b j} = \varepsilon \times f _ {1} + (1 - \varepsilon) \times f _ {2} \tag {8}
$$

where ε is the weight that ranges between 0 and 1. And $f _ { 1 }$ and $f _ { 2 }$ are given by

$$
f _ {1} = \max [ \frac {\sum_ {i = 1} ^ {n} d (n o d e _ {k i} , C H _ {k})}{N u m _ {k}} ] \tag {9}
$$

![](images/3a80afba75158f1745df69306381f28a9c3df91c072ac364f60648985e96717a.jpg)



FIGURE 5. Select delivery path from CH to BS.

In this function, $n o d e _ { k i }$ is the node i belong to the cluster k, $C H _ { k }$ is the cluster head in the cluster k, Numk is the number of nodes that belong to the cluster k. Therefore, $f _ { 1 }$ is the maximum intra-cluster distance among all the clusters.

$$
f _ {2} = \frac {\text { clusterNum } \times \max (E)}{E n} \tag {10}
$$

where clusterNum is the number of clusters, max(E) is the maximum energy of all nodes alive, and En is the sum of total current energy of the cluster heads. In this way, $f _ { 2 }$ is the ratio of cluster heads energy to the maximum energy of nodes. In the experiment, ε is set to 0.6 while 1 − ε is 0.4

# E. FINDING THE BEST WAY TO BS

After cluster heads have been selected, nodes would communicate with its nearest cluster head and send data. After cluster heads finish receiving data, they would send the data by wireless links to BS. Due to the long distance between CHs and BS, the energy consumption of direct communication is very large. So it is necessary to choose relay nodes. We use Ant Colony Optimization (ACO) to choose relay nodes, finding the lowest energy paths from cluster heads to BS. The following objective function is used to find the best way:

$$
f _ {o b j} = 2 N \times E _ {e l e c} + \sum_ {i = 1} ^ {N} \varepsilon_ {a m p} d _ {i j} ^ {n}. \tag {11}
$$

where N is the the number of passing nodes, $d _ { i j }$ is the distance from current node i to next node j, $E _ { e l e c } , \varepsilon _ { a m p }$ and n is the energy consumption constant shown in radio energy model.

Because the number of sensor nodes is large, ACO has difficulty in finding the best way quickly and accurately. Therefore, we add a limit to the alternative nodes set of each CH. As shown in Fig.6, a cluster head would choose the nodes which stay within the rectangular area between the CH and the BS as candidates to reduce the complexity of path. The width of the area is given by Equation.12. As the number of clusters decreases, the width increase to ensure that there are enough alternative nodes.

$$
\text { width } = 2 0 \times (1 + \frac {\text { clusterNum } _ {\text { begin }} - \text { clusterNum }}{\text { clusterNum } _ {\text { begin }}}) \tag {12}
$$

![](images/51d931f5edccc0fb1010a9fe964a714483e2d3caebe2f183b715e652f1db7801.jpg)



FIGURE 6. Select nodes under the limitation.   
![](images/65844202ed2f93fed741656fca8df3ecb0e500b8592b2f53cc11d778256c87dd.jpg)



FIGURE 7. Clustering and data transmission.

where clusterNumbegin is the number of clusters at the beginning, while clusterNum is the number of clusters at current round. 20m is the width of the transmission area at the beginning, as the alive nodes and clusterNum decreases, the width of the area increases to ensure adequate relay nodes in the area.

The optimization process of this paper is shown in Fig.7 and Fig.8.

• Initializing node energy and node location.   
• Grouping nodes based on distance from node to BS.   
• Selecting cluster heads by RPSO for remote nodes.   
• Obtaining the optional relay nodes between each CH and BS.   
• Finding the best way between each CH and BS by ACO.   
• Sending the data and calculating energy consumption.   
• Calculating the number of alive nodes.   
• Starting a new round.

# III. ALGORITHM

# A. RESAMPLING PARTICLE SWARM OPTIMIZATION

Particle Swarm Optimization (PSO) is widely used because of its high-performance and flexibility. However, there are potential problems of the classical PSO. Since the initial position and initial velocity of the particle are random, even after several rounds of iteration, there would still be particles far away from the optimal solution, which slow down the speed of the entire group toward the optimal solution. For high-dimensional multi-peak problems, PSO is easy to fall into local optimal solution.

![](images/2b2aec0404c6188a1fd37937dce4cf49833b81995c63a4ef620d5fd2c6aa2a7d.jpg)



FIGURE 8. System flow chart.

To overcome the shortcomings mentioned above and improve the performance of PSO, the resampling process, inspired by the Particle Filter (PF) [24], [25], was introduced to PSO. The new optimization algorithm is called Resampling Particle Swarm Optimization (RPSO). The main steps for resampling are as follows: 1) Determine whether it is necessary to resample low-weight particles according to the step. 2) Give each particle a weight value as Equation (13) and Equation (14).

$$
q _ {i} = \frac {1}{\sqrt {2 \sigma \pi}} e x p (- \frac {(F (x _ {i}) - p _ {g}) ^ {2}}{2 \sigma}) \tag {13}
$$

$$
Q _ {i} = \frac {q _ {i}}{\sum_ {i = 1} ^ {N} q _ {i}} \tag {14}
$$

where $q _ { i }$ is the weight value given to particle i, F (x) is the fitness function, $p _ { g }$ stands for the current global optimal value, σ is the sample variance of $F ( x _ { i } ) \mathrm { ~ - ~ } p _ { g }$ . Qi is the unitary weight value given to particle i. 3) For each particle, if $Q _ { i } < q _ { t }$ , then

$$
x _ {i} (t) = \bar {x} _ {i} (t) \tag {15}
$$

where x¯i(t) is the new position introduced randomly, $q _ { t } ~ =$ ${ \overline { { Q } } } - 2 * \sigma ^ { 2 } ( Q )$ . The way to update velocities is shown in (16).

$$
v _ {i} (t) = \frac {T + t}{2 T} \bar {v} _ {i} (t) + \frac {T - t}{2 T} v _ {i} (t) \tag {16}
$$

where t is the current step, T is the maximum step, $\bar { \nu _ { i } } ( t )$ is the new velocity introduced randomly, we can see because of $\frac { T + t } { 2 T }$ and $\frac { T - \bar { t } } { 2 T }$ the larger the number of steps, the larger the proportion of $\bar { \nu _ { i } } ( t )$ . The RPSO, introducing the resampling technique to PSO, improved performance of particle swarm optimization. The pseudo code of RPSO is presented in Algorithm 1.

Algorithm 1 RPSO Algorithm   
given the size of the swarm N, the maximum step of iteration T
set $i = (1, \ldots, N)$ , t = 0
initialize the particles $x_i(0)$ , $p_i(0)$ , $v_i(0)$ while convergence is not arise, do
    for each time step t, do
    if the resampling step comes, then $q_i = \frac{1}{\sqrt{2\sigma\pi}} exp(-\frac{(F(x_i) - p_g)^2}{2\sigma})$ $Q_i = \frac{q_i}{\sum_{i=1}^{N} q_i}$ $q_t = \overline{Q} - 2\sigma^2(Q)$ if $Q_i < q_t$ , do $x_i(t) = \bar{x}_i(t)$ $v_i(t) = \frac{T + t}{2T} \bar{v}_i(t) + \frac{T - t}{2T} v_i(t)$ end if
    end if
    for each particle i, do $v_i(t + 1) = \chi v_i(t) + c_1 r_1[p_i - x_i(t)] + c_2 r_2[p_g - x_i(t)]$ $x_i(t + 1) = x_i + v_i(t + 1)$ update $p_i(t + 1)$ , $p_g(t + 1)$ $p_i(t + 1) = best\{p_i(t), f(X_i(t + 1))\}$ $p_g(t + 1) = best\{p_i(t + 1)\}$ end for
    end for
end while
return $p_g^*$

# B. ANT COLONY OPTIMIZATION

Ant colony optimization (ACO) takes inspiration from the foraging behavior of ant species. These ants deposit pheromone on the ground in order to mark some favorable path that attract other members of the colony. Ant colony optimization exploits a similar mechanism for solving optimization problems. [26]

The main steps for ACO are follows: 1) Making a list. The list include unvisited cities and the pheromone on the path. 2) Choosing the next city by Equation (17).

argmax[tau(r , u)α ∗ eta(r , u)β ], rand < q0

$$
\operatorname{cumcom} \left[ \frac {\operatorname{tau} (r , u) ^ {\alpha} * \operatorname{eta} (r , u) ^ {\beta}}{\sum \operatorname{tau} (r , u) ^ {\alpha} * \operatorname{eta} (r , u) ^ {\beta}} \right], \quad \text { rand } \geq q _ {0} \tag {17}
$$

$$
e t a (r, u) = \frac {1}{\left| d _ {r u} - 9 3 . 6 5 \right|} \tag {18}
$$

where $t a u ( r , u )$ is the pheromone between current position and unvisited cities, eta(r, u) is the man-made expectations as shown in Equation (18) $d _ { r u }$ is the distance between current position and unvisited cities, argmax chooses the city with max value, cumcom chooses the next city by roulette, q0 is a parameter determining the possibility about choosing argmax. 3) Updating the pheromone concentration. If an ant reach BS, we would calculate the distance he has traveled, and then update the pheromone concentration by Equation (19). After all ants reach destination compute pheromone loss by Equation (20).

$$
t a u = t a u + \frac {1}{s c o r e} \tag {19}
$$

$$
t a u = (1 - \eta) * t a u \tag {20}
$$

where tau is the pheromone on the way that the ant passed, score is the objective function shown in Equation (11), η is loss factor.

The pseudo code of Ant colony optimization is presented in Algorithm 2.

Algorithm 2 Ant Colony Optimization   
given the maximum step of iteration T, the number of ants N
set $i = (1, \ldots, N)$ , t = 0
initialize the pheromone tau, unvisited cities, best score
for each time step t, do
    for each ant i, do
    while destination is not arise, do
    choose next city in unvisited cities by Equation (17)
    end while
    calculate score
    if score < bestscore, do
    bestscore = score
    end if
    tau(r, s) = tau(r, s) + $\frac{1}{score}$ end for
    tau(r, s) = (1 - η) * tau(r, s)
end for
return the best path

# IV. SIMULATION EXPERIMENT AND RESULTS ANALYSIS A.SIMULATION DESCRIPTION

# 1) SIMULATION ENVIRONMENT

In order to confirm the effective-ness of the proposed protocol, experiments are designed and implemented on

![](images/1df130493649335ba9543fdcda4538d049a03a034f4e1361af3f11f3c0b3a841.jpg)



FIGURE 9. Number of alive nodes over time.

MATLAB 2017a software platform. They are conducted on a Core i5-3450 3.1 GHz PC with 8GB memory, running Windows 7.

# 2) SIMULATION METRICS

To compare the performance of the proposed routing algorithm with the prevalent ones, we measure the following metrics:

# a: NUMBER OF DATA MESSAGES

The number of data massages metric determines how many data messages are received to the base station from the network. The more amount of data messages received at the BS reveals less die rate of nodes and expenses of energy.

# b: NUMBER OF ALIVE NODE

The performance of a network depends on the lifetime of its nodes. If the lifetime of the nodes is high then the network performs well and also transmits more data to the base station.

# c: ENERGY

This matric greatly affect the network as the lifetime of a node and then will affect the number of data being transmitted by the nodes. So the low expenses of energy will increase network performance.

# d: COVERAGE RATIO

Coverage ratio the effectiveness of the network on the observation of the target area.

we assume that once the number of alive nodes is less than 200, the network die. Therefore, we run 200 rounds and analyze the results gained by each protocol. At each round, it cost 300 iterations (70s) for RPSO based clustering process and 500 iterations(20s) for ACO based routing process.

# B. RESULTS AND ANALYSIS

# 1) DATA TRANSMISSION

Fig.9 and Fig.10 respectively represent of the number of alive nodes and the number of data messages received by BS over time. In Fig.9, RPSO-ACO select higher energy and denser

![](images/ce393ad2d73845b5fa38e2c45d37141697f2a4cb434ee508ae6cacc82827f1ab.jpg)



FIGURE 10. The amount of data received by base station over time.

TABLE 2. The amount of data transmitted in LEACH, PSO-C, RPSO-ACO, PSO-ACO. 

<table><tr><td>Number of data (Mbit)</td><td>LEACH</td><td>PSO-C</td><td>RPSO-ACO</td><td>PSO-ACO</td></tr><tr><td>mean</td><td>121.601</td><td>134.354</td><td>222.608</td><td>221.479</td></tr><tr><td>max</td><td>122.284</td><td>140.316</td><td>224.672</td><td>223.548</td></tr><tr><td>min</td><td>120.084</td><td>128.392</td><td>220.268</td><td>219.104</td></tr></table>

area node as its cluster heads in every round, so the alive nodes number of it is higher than other protocols. Because of the large areas need to be observed, the clusters of LEACH and PSO-C need to send data to the base station at a very long distance, so its nodes die quickly in the beginning of time. Fig.10 shows the number of data packages received at the base station. In all the protocols (LEACH, PSO-C, RPSO-ACO and PSO-ACO), each package is transmitted to the cluster head through a single hop, and then the LEACH and PSO-C send the data to BS directly, the RPSO-ACO and PSO-ACO send the data to BS through relay nodes. Due to a more even distribution of energy consumption, the nodes mortality rate in RPSO-ACO in Fig.10 is the least, so more data would be sent to BS than other protocols. We can see in the Fig.10 the data received by BS is improved from 121.6Mbit to 222.6Mbit.

Tab.2 shows the the optimal results of LEACH,PSO-C, RPSO-ACO and PSO-ACO. Compared with other protocols, the mean, maximum and minimum value obtained by RPSO-ACO are all higher in each case. RPSO-ACO obtained about 224.672Mbit in its max data throughput and 222.608Mbit in its mean data throughput after running ten times.

Compared with LEACH, the max data amount of RPSO-ACO is increased by 84%. Compared with PSO-C, the max data amount of RPSO-ACO is increased by 60%, and the interval size of results is reduced from 5.962Mbit to 4.404Mbit. Compared with PSO-ACO, the max data amount of RPSO-ACO is increased by 1.124Mbit, and the interval size is reduced from 4.444Mbit to 4.404Mbit.

It is clear that the proposed RPSO-ACO performs best among the four methods, the amount of data received by BS can reach 224.672Mbit, which is the highest of all. Therefore, the RPSO-ACO can solve the problem better, getting more accurate solutions and performing much more stable.

![](images/243917b514c78211fb51242758a41f4bc08811af930ce2577c6429cd6e05b6bd.jpg)



FIGURE 11. Energy consumption over the total data received by BS.

![](images/6d1e874d35e498ca50e714f337a09f592cd864d06cfcf20901a2807230264abc.jpg)



FIGURE 12. Coverage ratio of monitoring region over time.

# 2) ENERGY CONSUMPTION

Fig.11 is the energy consumption over the total amount of data received by BS. In Fig.11 LEACH and PSO-C have high energy consumption by transmitting data in most times, while the energy consumption of RPSO-ACO is lower and more stable. In LEACH and PSO-C, at the beginning, the energy consumption is high and the nodes far away from BS would die quickly, and the average distance of alive nodes form BS would be shorter. In RPSO-ACO, the alive nodes are evenly distributed in the area, so the energy consumption of receiving unit data is stable.

# 3) COVERAGE RATIO

Fig.12 represents the coverage ratio of monitoring region over time. In Fig.12, the coverage ratio of LEACH and PSO-C drop rapidly at the beginning because the cluster head nodes far from the BS consume too much energy and quickly die. The decrease in the number of alive nodes is one of the reasons for the decline in coverage. At the same time, due to the rapid death of the cluster heads far from the BS, alive nodes of LEACH and PSO-C would distribute densely around

![](images/a7d28760ef935d09410e9f30a02ff6f352f503060478ccacef484e83569b7753.jpg)  
FIGURE 13. Node distribution in 50th round.

![](images/a2d72313bdde728549c7641f7b648f462549dab395870c6be27d3e0a36932bb1.jpg)



FIGURE 14. Node distribution in 200th round.

the base station. RPSO-ACO establishes clusters based on energy and node density clustering, and uses ACO to find the optimal way to the BS. So the energy consumption of the nodes is more even and the total of them is less, leading to more alive nodes and making them more evenly distributed in the monitoring region, which improves the observation coverage.

Fig.13 and Fig.14 is the nodes distribution of LEACH, PSO-C, RPSO-ACO and PSO-ACO in 50 round, 150 round. We can see that alive nodes of LEACH quickly approach the base station over time and PSO-C also has similar problem.

TABLE 3. Coverage ratio of monitoring region of LEACH, PSO-C, RPSO-ACO, PSO-ACO in 200 rounds. 

<table><tr><td>coverage ratio</td><td>LEACH</td><td>PSO-C</td><td>RPSO-ACO</td><td>PSO-ACO</td></tr><tr><td>mean</td><td>0.2562</td><td>0.3103</td><td>0.6094</td><td>0.5814</td></tr><tr><td>max</td><td>0.2649</td><td>0.3513</td><td>0.6396</td><td>0.6121</td></tr><tr><td>min</td><td>0.2480</td><td>0.2934</td><td>0.5790</td><td>0.5401</td></tr></table>

RPSO-ACO and PSO-ACO don’t have this problem. Alive nodes number of RPSO-ACO and PSO-ACO are much more than LEACH, PSO-C and the nodes are more evenly distributed in the monitoring region, increasing the coverage ratio.

Tab.3 shows the coverage ratio of monitoring region of LEACH, PSO-C, RPSO-ACO and PSO-ACO in 200 round. Compared with LEACH, the mean, maximum and minimum value of RPSO-ACO are all higher in each case, the max coverage ratio is increased by 37.5% and the value of it reaches 0.6396. Compared with PSO-C, the max coverage ratio is increased by 28.8%. RPSO-ACO is also better than PSO-ACO. Compared with PSO-ACO, the max coverage ratio is increased by 2.75%, and the interval size of results is reduced from 0.0720 to 0.0606. It shows that RPSO-ACO cover the largest area, and RPSO-ACO has higher calculation accuracy and convergence speed.

# V. CONCLUSION AND FUTURE WORK

In this paper, we propose a two stage RPSO-ACO based protocol to address the data transmission problem of wireless sensor networks. Through the strategy we find the best data transmission path, improve the network lifetime, increase the amount of data in the transmission process and elevate observation coverage ratio. The conclusions of this paper could be summarized as follows:

1) RPSO is adopted in the clustering optimization problem. In this algorithm, some unimportant particles would be replaced to improve algorithmic efficiency. The experiments show that compared to PSO, the optimal results of RPSO is more stable and more precise.   
2) RPSO-ACO optimization protocol is used to solve clustering and routing problems. The experiments show that it gets higher data transmission capacity, longer network lifetime, higher coverage ratio and performs much more stable than LEACH, PSOC and PSO-ACO.   
3) A new transmission strategy is proposed, if the distance between the sensor node and base station is less than a certain value, the node should transmit data directly to base stations regardless of the structure and scale of sensor networks. In this way, data would be transmitted with minimal energy consumption.

For the future work, we would like to investigate the following issues. Firstly, We would improve RPSO to make it more efficient, faster and more accurate to obtain the optimal solution. Then the network connectivity would be further discussed [27], [28], the optimization problems of which would be studied based on a novel transmission strategy. On the other hand, the novel deployment strategy of the sensor network [29] and other data collection scheme [30] would be studied.

# REFERENCES

[1] X. Liu, T. Qiu, and T. Wang, ‘‘Load-balanced data dissemination for wireless sensor networks: A nature-inspired approach,’’ IEEE Internet Things J., to be published. doi: 10.1109/JIOT.2019.2900763.   
[2] X. Liu and P. Zhang, ‘‘Data drainage: A novel load balancing strategy for wireless sensor networks,’’ IEEE Commun. Lett., vol. 22, no. 1, pp. 125–128, Jan. 2018.   
[3] J. Li, W. Liu, T. Wang, H. Song, X. Li, F. Liu, and A. Liu, ‘‘Batteryfriendly based relay selection scheme to prolong lifetime for sensor nodes in Internet of Things,’’ IEEE Access, vol. 7, pp. 33180–33201, 2019.   
[4] A. A. Abbasi and M. Younis, ‘‘A survey on clustering algorithms for wireless sensor networks,’’ Comput. Commun., vol. 30, nos. 14–15, pp. 2826–2841, 2007.   
[5] W. R. Heinzelman, A. Chandrakasan, and H. Balakrishnan, ‘‘Energyefficient communication protocol for wireless microsensor networks,’’ in Proc. 33rd Annu. Hawaii Int. Conf. Syst. Sci., Jan. 2000, pp. 1–10.   
[6] S. Lindsey and C. S. Raghavendra, ‘‘PEGASIS: Power-efficient gathering in sensor information systems,’’ in Proc. IEEE Aerosp. Conf., vol. 3, Mar. 2002, p. 3.   
[7] Y.-F. Huang, N.-C. Wang, and M.-C. Chen, ‘‘Performance of a hierarchical cluster-based wireless sensor network,’’ in Proc. IEEE Int. Conf. Sensor Netw., Ubiquitous, Trustworthy Comput., Jun. 2008, pp. 349–354.   
[8] M. Dorigo and G. Di Caro, ‘‘Ant colony optimization: A new meta-heuristic,’’ in Proc. Congr. Evol. Comput. (CEC), Jul. 1999, pp. 1470–1477.   
[9] S. Okdem and D. Karaboga, ‘‘Routing in wireless sensor networks using an ant colony optimization (ACO) router chip,’’ Sensors, vol. 9, no. 2, pp. 909–921, 2009.   
[10] J. Kennedy and R. Eberhart, ‘‘Particle swarm optimization,’’ in Proc. IEEE Int. Conf. Neural Netw., Nov./Dec. 1995, pp. 1942–1948.   
[11] N. M. A. Latiff, C. C. Tsimenidis, and B. S. Sharif, ‘‘Energy-aware clustering for wireless sensor networks using particle swarm optimization,’’ in Proc. IEEE 18th Int. Symp. Pers., Indoor Mobile Radio Commun. (PIMRC), Sep. 2007, pp. 1–5.   
[12] M. Azharuddin and P. K. Jana, ‘‘Particle swarm optimization for maximizing lifetime of wireless sensor networks,’’ Comput. Elect. Eng., vol. 51, pp. 26–42, Apr. 2016.   
[13] J. RejinaParvin and C. Vasanthanayaki, ‘‘Particle swarm optimizationbased clustering by preventing residual nodes in wireless sensor networks,’’ IEEE Sensors J., vol. 15, no. 8, pp. 4264–4274, Aug. 2015.   
[14] M. Azharuddin and P. K. Jana, ‘‘PSO-based approach for energy-efficient and energy-balanced routing and clustering in wireless sensor networks,’’ Soft Comput., vol. 21, no. 22, pp. 6825–6839, 2017.   
[15] Y. Liang and H. Yu, ‘‘PSO-based energy efficient gathering in sensor networks,’’ in Mobile Ad-hoc and Sensor Networks (Lecture Notes in Computer Science), vol. 3794. Berlin, Germany: Springer, 2005, pp. 362–369.   
[16] M. R. Jafri, N. Javaid, A. Javaid, and Z. A. Khan, ‘‘Maximizing the lifetime of multi-chain PEGASIS using sink mobility,’’ Mar. 2013, arXiv:1303.4347. [Online]. Available: https://arxiv.org/abs/1303.4347   
[17] C. Tunca, S. Isik, M. Y. Donmez, and C. Ersoy, ‘‘Ring routing: An energyefficient routing protocol for wireless sensor networks with a mobile sink,’ IEEE Trans. Mobile Comput., vol. 14, no. 9, pp. 1947–1960, Sep. 2014.   
[18] K. Tian, B. Zhang, K. Huang, and J. Ma, ‘‘Data gathering protocols for wireless sensor networks with mobile sinks,’’ in Proc. IEEE Global Telecommun. Conf. (GLOBECOM), Dec. 2010, pp. 1–6.   
[19] X. Wu and G. Chen, ‘‘Dual-sink: Using mobile and static sinks for lifetime improvement in wireless sensor networks,’’ in Proc. IEEE 16th Int. Conf. Comput. Commun. Netw. (ICCCN), Aug. 2007, pp. 1297–1302.   
[20] J. Wang, Y. Yin, J. Zhang, S. Lee, and R. S. Sherratt, ‘‘Mobility based energy efficient and multi-sink algorithms for consumer home networks,’’ IEEE Trans. Consum. Electron., vol. 59, no. 1, pp. 77–84, Feb. 2013.   
[21] T. A. Al-Janabi and H. S. Al-Raweshidy, ‘‘A centralized routing protocol with a scheduled mobile sink-based AI for large scale I-IoT,’’ IEEE Sensors J., vol. 18, no. 24, pp. 10248–10261, Dec. 2018.

[22] X. Wang, H. Gu, H. Zhang, and H. Chen, ‘‘Novel RPSO based strategy for optimizing the placement and charging of a large-scale camera network in proximity service,’’ IEEE Access, vol. 7, pp. 16991–17000, 2019.   
[23] X. Wang, H. Zhang, S. Fan, and H. Gu, ‘‘Coverage control of sensor networks in IoT based on RPSO,’’ IEEE Internet Things J., vol. 5, no. 5, pp. 3521–3532, Oct. 2018. [Online]. Available: https://ieeexplore.ieee.org/document/8344823/   
[24] J. D. Hol, T. B. Schon, and F. Gustafsson, ‘‘On resampling algorithms for particle filters,’’ in Proc. IEEE Nonlinear Stat. Signal Process. Workshop, Sep. 2006, pp. 79–82.   
[25] R. Douc and O. Cappe, ‘‘Comparison of resampling schemes for particle filtering,’’ in Proc. IEEE 4th Int. Symp. Image Signal Process. Anal. (ISPA), Sep. 2005, pp. 64–69.   
[26] F. Farahnakian, A. Ashraf, T. Pahikkala, P. Liljeberg, J. Plosila, I. Porres, and H. Tenhunen, ‘‘Using ant colony system to consolidate VMs for green cloud computing,’’ IEEE Trans. Services Comput., vol. 8, no. 2, pp. 187–198, Mar./Apr. 2015.   
[27] J. N. Al-Karaki and A. Gawanmeh, ‘‘The optimal deployment, coverage, and connectivity problems in wireless sensor networks: Revisited,’’ IEEE Access, vol. 5, pp. 18051–18065, 2017.   
[28] A. Tripathi, H. P. Gupta, T. Dutta, R. Mishra, K. K. Shukla, and S. Jit, ‘‘Coverage and connectivity in WSNs: A survey, research issues and challenges,’’ IEEE Access, vol. 6, pp. 26971–26992, 2018.   
[29] X. Liu, ‘‘Node deployment based on extra path creation for wireless sensor networks on mountain roads,’’ IEEE Commun. Lett., vol. 21, no. 11, pp. 2376–2379, Nov. 2017.   
[30] J. Tan, W. Liu, M. Xie, H. Song, A. Liu, M. Zhao, and G. Zhang, ‘‘A low redundancy data collection scheme to maximize lifetime using matrix completion technique,’’ EURASIP J. Wireless Commun. Netw., vol. 2019, p. 5, Dec. 2019. doi: 10.1186/s13638-018-1313-0.

![](images/dac3e3be7b74e39586015fc74f7b5b0a30f83cd8cc4f16a0e2aeb7fe89a9ea52.jpg)



XIAOHUI WANG received the B.S. and Ph.D. degrees from Beihang University, Beijing, in 2001 and 2009, respectively. She is currently an Assistant Professor with the Department of Spacecraft Design, School of Astronautics, Beijing University of Aeronautics and Astronautics, researching on optimization theory and methods, and complex system optimization.

HAORAN GU, photograph and biography not available at the time of publication.

YUNHAO LIU, photograph and biography not available at the time of publication.

HAO ZHANG, photograph and biography not available at the time of publication.