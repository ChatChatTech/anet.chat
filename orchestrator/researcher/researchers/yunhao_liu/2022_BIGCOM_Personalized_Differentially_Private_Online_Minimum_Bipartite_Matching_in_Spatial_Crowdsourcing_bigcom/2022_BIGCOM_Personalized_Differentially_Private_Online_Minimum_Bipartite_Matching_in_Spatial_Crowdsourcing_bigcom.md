# Personalized Differentially Private Online Minimum Bipartite Matching in Spatial Crowdsourcing

Chaojie Lv‡, Lan Zhang† and Xiang-Yang Li∗

School of Computer Science and Technology, The CAS Key Laboratory of Wireless-Optical Communications,

University of Science and Technology of China

‡chjlv@mail.ustc.edu.cn, †zhanglan@ustc.edu.cn, ∗xiangyangli@ustc.edu.cn

Abstract—Mobile devices and mobile applications benefit people’s mobility. In some applications such as Uber and Didi, drivers and passengers (i.e., users) submit locations to the server to match each other. However, the server may be untrusted and location privacy becomes a huge concern. Users expect to enjoy matching while protecting their locations and different users have different levels of location privacy. In this paper, we consider the personalized privacy-preserving online minimum bipartite matching problem. To solve this problem, we design a Personalized Quadtree-Based privacy-preserving matching Framework (PQBF). In this framework, we propose a privacy method using the truncated Geometric Mechanism on the quadTree (GMT). GMT allows users to intuitively select generalization regions with different sizes, which is user-friendly. We then formulate the distance on the quadtree using earth mover’s distance (EMD) to select the closest worker-task pair. Considering the huge time overhead of distance calculation, we provide a way to accelerate. We show that our method satisfies ϵ-geo-indistinguishability on the quadtree and give the time complexity of PQBF. Experiments on synthetic data and real data show that our mechanism is more effective than previous mechanisms in terms of total distance. PQBF saves up to 35.9% total distance than a state-of-the-art algorithm.

Index Terms—Differential privacy, geo-indistinguishability, online minimum bipartite matching, geometric mechanism, quadtree

# I. INTRODUCTION

People’s travel is benefited by mobile applications, such as Uber [1] and Didi [2]. In these applications, drivers and passengers (i.e., users) submit locations to match each other online. Semantic information on these locations may reveal users’ work, hobbies, and relationships [3]. And the locations may be used improperly or leaked by the application (i.e., the server). Location privacy has already caught the attention of users. But the high level of location privacy protection leads to inaccurate locations, which deteriorates the quality of matching.

Matching is one form of task assignment in spatial crowdsourcing. In the privacy-preserving task assignment, a lot of researches focus on protecting the locations of workers or tasks, not both. For example, Squicciarini et al. [4] considers that real task locations are known and then noisy worker locations are given by a location obfuscation strategy. However, the locations of tasks also need to be protected since they may leak the locations of previous workers with the help of matching information. Moreover, workers and tasks have different expectations for the levels of location privacy. Some may want better matching services, and therefore reduce the levels privacy protection, while others want high privacy protection. Currently, some studies [5], [6] propose new notions satisfying users’ privacy requirements in different scenarios. And much of the work that consider personalized privacy protection with different levels of location privacy are mostly used for statistical data and rarely for online matching.

In this paper, we study the personalized privacy-preserving online minimum bipartite matching in spatial crowdsourcing that workers and tasks (i.e., users) has their own privacy preferences and submit the noisy locations to the semi-honest server waiting to be matched. Online matching is a form of online task assignment and has extensive researches [7]– [11]. We then design a Personalized Quadtree-Based privacypreserving matching Framework (PQBF). In this framework, we propose a privacy mechanism using the truncated Geometric Mechanism [12] on the quadTree [13] (GMT). GMT allows the user to select an acceptable coarse-grained level on the quadtree to generalize his location which is user-friendly and then perturb the generalized location using truncated geometric mechanism to satisfy ϵ-geo-indistinguishability. To select the closest worker-task pair, we formulate distance using earth mover’s distance (EMD) on the quadtree. Considering the huge time overhead of distance calculation, we provide a way to accelerate and thus it is efficient to match on the quadtree. Our main contributions are summarized as follows.

1) This paper studies personalized privacy-preserving online minimum bipartite matching problem in terms of minimizing the total distance.   
2) This paper provides a personalized quadtree-based privacy-preserving matching framework PQBF. PQBF includes a privacy mechanism GMT that satisfies ϵ- geo-indistinguishability. Most importantly, GMT allows the user to select the generalized region intuitively according his own personalized privacy preference. Then the distance is formulated on the quadtree to select “closest” worker-task pair and the distance calculation is accelerated for efficient matching.   
3) When satisfying ϵ-geo-indisinguishability, our PQBF is more effective than existing methods on both synthetic and real data in terms of total distance. PQBF saves up to 35.9% total distance than a state-of-the-art algorithm [11].

In the rest of this paper, we review related work in Section II. We define our problem in Section III. We describe our framework in Section IV, present the evaluation in Section V and conclude the paper in Section VI.

# II. PRELIMINARIES AND RELATED WORK

We review the notion of differential privacy based on our work and then discuss related work.

# A. Differential Privacy

Differential privacy [14] is a golden privacy protection criterion with a strict definition of privacy, which has been widely used in databases [15], social networks [16], [17], the smart grid [18], federated learning [19], [20], etc. Its variant ϵ- geo-indistinguishability [21] has a wide range of applications in location privacy. ϵ-geo-indistinguishability can ensure that two different locations $\ell _ { 1 } , \ell _ { 2 }$ perturbed to the same point z are indistinguishable, and their probability ratio is bounded by the privacy parameter ϵ and the distance $d ( \ell _ { 1 } , \ell _ { 2 } )$ between $\ell _ { 1 }$ and $\ell _ { 2 }$ . More formally,

Definition 1 ( [21]). The mechanism M satisfies ϵ-geoindistinguishability on domain R if and only if for any two positions $\ell _ { 1 } , \ell _ { 2 } ~ \in ~ \mathcal { R }$ and output $z \in { \mathcal { Z } } ,$ the following inequality holds:

$$
\frac {P r [ M (\ell_ {1}) = z ]}{P r [ M (\ell_ {2}) = z ]} \leq e ^ {\epsilon \cdot d (\ell_ {1}, \ell_ {2})} \tag {1}
$$

We consider that the domain of region R and the domain of output Z are the same. If locations are on a two-dimensional plane, the distance $d ( \cdot , \cdot )$ can be the Euclidean distance, that is, $d ( \ell _ { 1 } , \ell _ { 2 } ) = \| \ell _ { 1 } - \ell _ { 2 } \| _ { 2 }$ , where ∥ · ∥2 represents L2 norm. If locations are on a one-dimensional plane, the distance $d ( \cdot , \cdot )$ can be the absolute value of the difference, that is, $d ( \ell _ { 1 } , \ell _ { 2 } ) =$ $| \ell _ { 1 } - \ell _ { 2 } |$ . Small ϵ implies a higher level of location privacy protection. Small $d ( \cdot , \cdot )$ also means a higher level of location privacy protection.

The planar Laplace mechanism proposed by [21] is a popular method, which satisfies ϵ-geo-indistinguishability. Given a privacy budget ϵ and an actual location ℓ, the probability of this mechanism on any output location $\ell ^ { \prime }$ is:

$$
P r [ M _ {\epsilon} (\ell) = \ell^ {\prime} ] = \frac {\epsilon^ {2}}{2 \pi} e ^ {- \epsilon \cdot d (\ell , \ell^ {\prime})}. \tag {2}
$$

# B. Related Work

1) Personalized Differential Privacy: A number of work, started by [22], introduce personalized privacy into differential privacy [14] attempting to catch the expectations of different user privacy levels. But the mechanism proposed by [22] can only be used for some real-valued functions and cannot be used for other common functions, such as counts, median and min/max. To overcome this problem, Jorgensen et al. [23] design the sampling mechanism and the personalized exponential mechanism to satisfy personalized differential privacy. Then there are many works [24]–[26] to improve these two mechanisms. Chen et al. [27] propose another notion of personalized local differential privacy (PLDP) that takes both privacy levels and safe regions into account. Chen et al. [27] then design a mechanism to learn the user distribution over a region. However, the above mechanisms are used for statistical data and are not suitable for location publishing. Also, a lot of work [28]–[33] consider personalized differential privacy in different scenarios.

2) Location Privacy Protection in Spatial Crowdsourcing: Location privacy has been extensively studied in recently years because of the widespread use of the mobile applications [34]. Although there are some studies [35], [36] using encryption to protect location privacy to provide services and some studies [37] using the policy, we limit our scope to location generalization (e.g., cloaking) and location perturbation (e.g., differential privacy) of location obfuscation [34]. Location generalization [38]–[41] converts an accurate location into a cloaked region, which does not guarantee protection of the user’s location when the adversary has the prior knowledge about the user distribution.

On the other hand, location perturbation (e.g., differential privacy [14]) protects the output by injecting noise, which is independent of the adversary’s prior knowledge. There are extensive studies [42]–[46] on privacy-preserving spatial range counting. But they don’t focus on online matching.

Online minimum bipartite matching is a form of task assignment. In the privacy-preserving task assignment, Wang et al. [47] consider that the server has all the real task locations and perturbed worker locations. The authors formulate a mixed-integer non-linear programming problem to minimize the expected travel distance under ϵ-geo-indistinguishability. Qian et al. [48] additionally maximizes task completion quality which includes rewards given to workers in the optimization problem. Rather than minimizing the expected travel distance, Squicciarini et al. [4] minimize the quality loss due to obfuscation, and further reduce the complexity through discretization and exploiting features in road networks. However, these schemes are for offline situations and solving optimization problems has high time complexity.

More recently, To et al. [49] propose privacy-preserving models for quantifying the worker-task pair reachability in an online manner. Different from [49], Tao et al. [11] focus on quantifying minimum distance. [11] proposes a privacy mechanism based on Hierarchically Well-Separated Trees (HSTs) and further design a faster implementation via random walk. However, HST is constructed based on the prior knowledge of the user distribution and may be quite different from the true user distribution. Compared with [11], we consider personalized privacy preferences. We also provide many generalized regions of different sizes for users to select, which is more intuitive and more user-friendly.

# III. PROBLEM DEFINITION

In this section, we briefly introduce the quadtree and then formulate the personalized privacy-preserving online minimum bipartite matching problem.

# A. Quadtree

A quadtree [13] is widely adopted in spatial data [42], [45], [50]. The quadtree recursively partitions a region into four equal quadrants. Specifically, the root node (level 0) in the quadtree represents the region R. Level 1 has four nodes, representing four subregions, obtained by partitioning region R equally horizontally and vertically. Similarly, the nodes at level h $; ( 2 \leq h \leq H )$ represent subregions obtained by equally partitioning the corresponding regions of nodes at level (h−1) horizontally and vertically. As the level increases, the region represented by each node becomes more fine-grained. The user can choose an acceptable coarse-grained level to generalize the location.

# B. Problem Formulation

There are three roles in our model: the server, the worker and the task. Users are used to represent workers and tasks. The server is semi-honest, which means that the server remains curious about the locations of workers and tasks but honestly accepts data and performs matching. A worker w has a true location $\ell _ { w }$ and personalized privacy preference $( h _ { w } , \epsilon _ { w } )$ , where $h _ { w }$ represents that the level selected by worker w on the quadtree and $\epsilon _ { w }$ is worker w’s privacy budget such that the location satisfies ϵw-geo-indistinguishability. A task t also has a true location $\ell _ { t }$ and personalized privacy preference $\left( h _ { t } , \epsilon _ { t } \right)$ . Workers and tasks protect their locations for locations are private. Personalized privacy preferences are public since exposing them does not leak locations. The three roles perform the following process: First, workers and tasks noise their locations according to their own personalized privacy preferences and submit the locations to the server. Second, the server matches workers and tasks immediately. Finally, the server sends the matching back to the corresponding worker and task.

Assume that all the workers and tasks are on region R. Define the distance between worker w and task t on region R as $d _ { R } ( w , t )$ . Define a matching as S which consists of workertask pairs. Define the total distance of a matching S on region R as $\begin{array} { r } { d _ { R } ( S ) = \sum _ { ( w , t ) \in S } d _ { R } ( w , t ) } \end{array}$ . We formulate the problem in this paper.

Personalized Differentially Private Online Minimum Bipartite Matching (PDPOMBM). The semihonest server matches dynamically arriving workers $W = ( w _ { 1 } , w _ { 2 } , \cdot \cdot \cdot , w _ { | W | } )$ and tasks $T = ( t _ { 1 } , t _ { 2 } , \cdot \cdot \cdot , t _ { | T | } )$ immediately. PDPOMBM aims to design a privacy mechanism that satisfies all the personalized privacy preferences of workers and tasks while finding a maximum-cardinality matching with minimum total distance.

# IV. DESIGN

In this section, we propose a Personalized Quadtree-Based privacy-preserving matching Framework (PQBF) to the PDPOMBM problem. Specifically, We first present the overview solution in Section IV-A. We show the construction of the quadtree in Section IV-B. We then design a user-friendly privacy mechanism that satisfies ϵ-geo-indistinguishability at each level of quadtree in Section IV-C. We further formulate the distance on the quadtree to match the closest one in Section IV-D. Finally, we accelerate distance calculation and show the time complexity of PQBF in section IV-E.

# A. Overview

We present a personalized privacy-preserving matching framework PQBF as shown in Fig. 1. The workflow of PQBF is mainly divided into the following steps:

1) The server builds and distributes the quadtree: The server builds a quadtree of height H based on region R, and publishes it for online matching between workers and tasks.   
2) Users (i.e., workers and tasks) add noise to locations locally and submit their parameters: each user u has a location $\ell _ { u }$ and personalized privacy preference $\left( h _ { u } , \epsilon _ { u } \right)$ . User u generalizes location $\ell _ { u }$ to a region on the quadtree and perturbs the generalized region by a differentially private mechanism. Then the user submits the perturbed region and personalized privacy preference to the server.   
3) The server matches workers and tasks immediately: the data of workers and tasks arrives dynamically, the server compares workers and tasks at the same level or between different levels on the quadtree, selects the “closest” pair, and matches immediately.   
4) The worker obtains the true location of the task: After the worker and the task are matched, the worker uses an extra privacy channel to obtain true location of the task, and the matching is completed.

![](images/0ae08c51ddd061638f6735c84e5e0b9feb5da77ccbc0b9eb15068f37a4c6d9f7.jpg)



Fig. 1. Overview

Similar to [11], we mainly focus on the design of the privacy mechanism and matching. Threat of workers is out of the scope of this work.

# B. Construction of the Quadtree

We use a conservative partition structure, quadtree, to partition the region R since workers and tasks arrive dynamically and the server cannot predict the distribution of their locations very accurately. The server builds a quadtree of height H based on region R. A quadtree partitions region R into H + 1 levels, each level representing a region size. Height H can be determined by some factors, including the size of the region R and user expectations for the matching service. It’s user-friendly to select an acceptable coarse-grained level to generalize the location. For example, if there is only one building around the user and he wants to get better matching service, he will choose a large level so the generalized region covers only this building. On the contrary, if he pays more attention to privacy, he can choose a smaller level and make the generalized region larger to cover other buildings to hide himself. The choice of level is related to the size of region R, the user’s service needs and privacy needs.

The server then assigns numbers to the nodes of quadtree from left to right and from top to bottom as shown in Fig. 2. Since there are $4 ^ { h }$ nodes at level h, the number of the leftmost node at level h $( 0 \leq h \leq H )$ is $( 4 ^ { h } - 1 ) / 3$ and the number of the rightmost at level h is $( 4 ^ { \acute { h } + 1 } - 1 ) / 3 - 1$ . We denote ${ \mathcal { X } } _ { h } = \{ ( 4 ^ { h } - 1 ) / 3 , ( 4 ^ { h } - 1 ) / 3 + 1 , \cdots , ( 4 ^ { h + 1 } - 1 ) / 3 - 1 \}$ as the numbers of all nodes at level h on the quadtree. The relationship between node number $j ~ ( j ~ > ~ 0 )$ and its parent node number i is $i = \lfloor ( j - 1 ) / 4 \rfloor$ . Subsequently, the server publishes the quadtree.

![](images/1b6e18e67d317f00b833a8bdbd9a75db66a7b56b42725e71b56184604b28eb3d.jpg)



Fig. 2. the Node Numbers on the Quadtree

# C. Personalized Local Generalization and Perturbation

The user u expects to be matched while protecting his location $\ell _ { u }$ with a guarantee of $\epsilon _ { u } .$ -geo-indistinguishability. Hence, we design a privacy mechanism using the truncated Geometric Mechanism [12] on the quadTree [13] (GMT). Specifically, a user u generalizes his location $\ell _ { u }$ and perturbs the generalized location locally using his own personalized privacy preference $\left( h _ { u } , \epsilon _ { u } \right)$ based on the quadtree that is distributed by the server.

1) Personalized Local Generalization: The user u selects level $h _ { u }$ to locally generalize the location $\ell _ { u }$ to a region on the quadtree. According to the property of quadtree, there is exactly one region containing location $\ell _ { u }$ at level $h _ { u }$ . We denote the node number corresponding to this region as $i _ { u } .$ .

As described in Section III-A, higher-level nodes on the quadtree means more fine-grained regions. The user generalizes his location $\ell _ { u }$ to region R if $h _ { u } = 0$ and the user only wants to tell the server that he is on region R. In contrast, the user generalizes his location $\ell _ { u }$ to some finest-grained region assigned by the server if $h _ { u } = H$ and the user afford this level of location privacy.

2) Personalized Local Perturbation: Simply generalizing the location does not guarantee protection of the user location. For example, the owner of a suburban house selects a region that is too fine-grained and his true location may be learned by the server. Inspired by [21], we extend ϵ-geoindistinguishability to each level of the quadtree. Specifically, the probability of any two node numbers $i _ { 1 } , i _ { 2 }$ at level $h _ { u }$ perturbed to the same node number $\tilde { i }$ is indistinguishable for a user u, that is,

$$
\frac {P r [ M (i _ {1}) = \tilde {i} ]}{P r [ M (i _ {2}) = \tilde {i} ]} \leq e ^ {\epsilon_ {u} \cdot d (i _ {1}, i _ {2})}, \tag {3}
$$

where $i _ { 1 } , i _ { 2 } , \tilde { i } \in \mathcal { X } _ { h _ { u } }$ and $d ( i _ { 1 } , i _ { 2 } ) = | i _ { 1 } - i _ { 2 } |$ | for they are onedimensional values. It’s noted that in most cases, the closer the node numbers are, the closer the locations are. The above equation is similar to PLDP mentioned in [27], where the safe region is seen here as the whole region R and the number of locations depends on the chosen level. The another difference is that PLDP uses the standard differential privacy for data aggregation and we use ϵ-geo-indistinguishability for online matching.

The planar Laplace mechanism mentioned in Section II-A does not apply to Eq. (3) because its input is a two-dimensional continuous location rather than a one-dimensional discrete node number. We consider the truncated geometric mechanism (GM) [12]. The original GM adds noise to the output to satisfy the standard differential privacy and the probability of GM is $\begin{array} { r } { P r [ M _ { G M } ( i ) = \tilde { i } ] = \frac { 1 - \tilde { \alpha ^ { } } } { 1 + \tilde { \alpha } } \alpha ^ { | i - \tilde { i } | } } \end{array}$ where $\alpha = e ^ { - \epsilon / \Delta }$ and $\Delta$ is the sensitivity of output function. We choose $\Delta = 1$ , modify GM slightly and then use GM on the quadTree (GMT). Specifically, given the node number $i _ { u }$ , GMT chooses to output a noisy node number $\tilde { i } _ { u }$ with a probability

$$
P r [ M (i _ {u}) = \tilde {i} _ {u} ] = \left\{ \begin{array}{l l} \frac {1}{1 + \alpha} \alpha^ {| i _ {u} - \tilde {i} _ {u} |} & \text { when   } \tilde {i} _ {u} \in \mathcal {B} _ {h _ {u}}, \\ \frac {1 - \alpha}{1 + \alpha} \alpha^ {| i _ {u} - \tilde {i} _ {u} |} & \text { when   } \tilde {i} _ {u} \in \mathcal {I} _ {h _ {u}}, \end{array} \right. \tag {4}
$$

where $\begin{array} { r } { \alpha = e ^ { - \epsilon _ { u } } , \mathcal { B } _ { h _ { u } } = \{ \frac { 4 ^ { h _ { u } } - 1 } { 3 } , \frac { 4 ^ { h _ { u } + 1 } - 1 } { 3 } - 1 \} } \end{array}$ 3 , 4hu+1−1 − 1} and iu,˜iu ∈ 3 $i _ { u } , \tilde { i } _ { u } \in$ $\mathcal { T } _ { h _ { u } }$ . The following theorem ensures that GMT satisfies ϵ-geoindistinguishability:

Theorem 1. For the user u, GMT satisfies $\epsilon _ { u } { - } g e o { - }$ indistinguishability at level $h _ { u }$ of the quadtree, $i . e . ,$ , satisfies (3).

Proof. The proof consists of two parts: 1) The probability sum of all possible outputs obtained from any input $i _ { u }$ using mechanism M is equal to 1, that is, P(4hu+1−1)/3−1˜ h P r[M (iu) = ˜i] = 1; 2) The mechanism $\sum _ { \tilde { i } = ( 4 ^ { h _ { u } } - 1 ) / 3 } ^ { \setminus ( 4 ^ { h _ { u } + \tilde { 1 } } - 1 ) / 3 - \tilde { 1 } } P r [ M ( i _ { u } ) \ = \ \tilde { i } ] \ = \ 1 ; \ 2 )$ i=(4 u −1)/3 M satisfies ϵu-geo-indistinguishability, i.e., P r[M(i1)=˜i]P r[M(i )=˜i] $\frac { P r [ M ( i _ { 1 } ) = \tilde { i } ] } { P r [ M ( i _ { 2 } ) = \tilde { i } ] } \leq$ $e ^ { \epsilon _ { u } \cdot | i _ { 1 } - i _ { 2 } | }$ for any $i _ { 1 } , i _ { 2 } , \tilde { i } \in \mathcal { T } _ { h _ { \boldsymbol { u } } }$ .

We first give the proof of 1): Set $i _ { m a x } = ( 4 ^ { h _ { u } + 1 } - 1 ) / 3 - 1$ and $i _ { m i n } = ( 4 ^ { h _ { u } } - \mathbf { \bar { 1 } } ) / 3$ . We have

$$
\begin{array}{l} \sum_ {\tilde {i} = (4 ^ {h _ {u}} - 1) / 3} ^ {(4 ^ {h _ {u}} + 1) - 1) / 3 - 1} P r [ M (i _ {u}) = \tilde {i} ] = (\sum_ {\tilde {i} = i _ {m i n}} ^ {i _ {u} - 1} + \sum_ {\tilde {i} = i _ {u}} ^ {i _ {m a x}}) P r [ M (i _ {u}) = \tilde {i} ] \\ = \frac {\alpha}{1 + \alpha} + \frac {1}{1 + \alpha} \\ = 1. \\ \end{array}
$$

We then show the proof of 2): Given any inputs $i _ { 1 } , \ i _ { 2 }$ and their same output ˜i, probability $P r [ M ( i _ { 1 } ) = \tilde { i } ]$ and probability $P r [ M ( i _ { 2 } ) = \tilde { i } ]$ have the same constant coefficients, either $\frac { 1 - \alpha } { 1 + \alpha }$ 1+α or $\frac { 1 } { 1 + \alpha }$ , by Eq. (4). Hence, the constant coefficients can cancel each other out in the probability ratio and we only consider non-constant coefficients:

$$
\begin{array}{l} \frac {P r [ M (i _ {1}) = \tilde {i} ]}{P r [ M (i _ {2}) = \tilde {i} ]} = \frac {\alpha^ {| i _ {1} - \tilde {i} |}}{\alpha^ {| i _ {2} - \tilde {i} |}} \\ = e ^ {- \epsilon_ {u} (| i _ {1} - \tilde {i} | - | i _ {2} - \tilde {i} |)} \\ \leq e ^ {\epsilon_ {u} \cdot | i _ {1} - i _ {2} |}, \\ \end{array}
$$

where the third inequality is from the triangle inequality.

In personalized local perturbation, the user u perturbs his node number $i _ { u }$ through Eq. (4) to get perturbed node number $\tilde { i } _ { u } ,$ which satisfies ϵ-geo-indistinguishability. After that, user u submits the user type (i.e., worker or task), perturbed node number $\tilde { i } _ { u }$ and personalized privacy preference $\left( h _ { u } , \epsilon _ { u } \right)$ to the server, waiting to be matched.

# D. Matching

The server receives the user type, perturbed node number $\tilde { \dot { \ i } } _ { u } ^ { \ 1 }$ iu and personalized privacy preference $( h _ { u } , \epsilon _ { u } )$ online. The server continuously maintains the task queue $L _ { t }$ and the worker queue $L _ { w }$ and then immediately matches the new user with the unmatched users in the queues. Note that there is no such situation where the unmatched user types have both workers and tasks. Hence, there are four cases encountered by the server:

Case 1: The unmatched user type only has the task and the newly arrived user type is also the task: Add the new task to the task queue $L _ { t }$

Case 2: The unmatched user type only has the worker and the newly arrived user type is also the worker: Add the new worker to the worker queue $L _ { w }$ .

Case 3: The unmatched user type only has the task and the newly arrived user type is the worker: Select the task closest to the new worker from task queue $L _ { t } .$ match and delete the closest task from $L _ { t }$ . Since it is difficult to calculate the distance of the worker and the task at different levels on the quadtree, we randomly project them to level $g \ ( g \in \{ 1 , 2 , \cdot \cdot \cdot , H \} )$ ) and calculate the distance at this level (We will formulate the definition of the distance between the worker and the task on the quadtree later).

Case 4: The unmatched user type only has the worker and the newly arrived user type is the task: Similar to Case 3, only the worker and the task are exchanged.

Next, we formulate the distance $d ( w , t )$ between worker w and task t and thus the closest user can be found. Note that close node numbers means they are close in distance on region R in most cases. If worker w and task t are at the same level of quadtree, i.e., $h _ { w } = h _ { t }$ , we use the absolute value of the difference between the two node numbers $i _ { w }$ and $i _ { t }$ as the distance $d ( w , t ) , \mathrm { i . e . , } d ( w , t ) = \left| i _ { w } - i _ { t } \right|$ . Node number $i _ { u }$ can be converted into a one-hot vector ${ \bf v } _ { h _ { u } , i _ { u } }$ of length $4 ^ { h _ { u } }$ . All the components of ${ \bf v } _ { h _ { u } , i _ { u } }$ are assigned the value 0 except for

1In the rest of this paper, we will omit the tilde of node number $i _ { u }$ without ambiguity.

$i _ { u } \mathrm { t h }$ component that is assigned the value 1. We slightly abuse the notation and use ${ \bf v } _ { u }$ to denote ${ \bf v } _ { h _ { u } , i _ { u } }$ . Another expression equivalent to $d ( w , t )$ is to take the accumulation function of the vector and calculate the L1 norm of difference to get the distance when $h _ { w } = h _ { t }$ . Earth mover’s distance (EMD) corresponds exactly to this form, which is

$$
E M D (\mathbf {v} _ {w}, \mathbf {v} _ {t}) = \sum_ {a = 0} ^ {4 ^ {h _ {w}} - 1} | \sum_ {b = 0} ^ {a} \mathbf {v} _ {w} (b) - \sum_ {b = 0} ^ {a} \mathbf {v} _ {t} (b) |, \tag {5}
$$

where ${ \mathbf { v } } _ { u } ( b )$ represents the bth component of vector $\mathbf { v } _ { u } .$

If worker w and task t are at different levels, i.e., $h _ { w } \neq h _ { t } .$ , we first project them into a random level g and then calculate the distance at level $g$ as $d ( w , t )$ . Specifically, $\pi _ { g } ( \mathbf { v } _ { u } )$ is denoted as a vector of $\mathbf { v } _ { u }$ projected to level g. There are three cases of $\pi _ { g } ( \mathbf { v } _ { u } )$ as shown in Fig. 3: (a) When $g = h _ { u } ,$ ,

![](images/e52a429ef99df350ccb28ae6187b32103b3b006eb45c021fddd672771519e43c.jpg)  
Fig. 3. Three Cases of $\pi _ { g } ( \mathbf { v } _ { u } )$

$\pi _ { g } ( \mathbf { v } _ { u } ) = \mathbf { v } _ { u } . \ ( \mathbf { b } )$ When $g < h _ { u } .$ , the node values of current level are aggregated to the corresponding parent nodes up to level $^ { g , }$ i.e., the projected vector $\pi _ { g } ( \mathbf { v } _ { u } )$ is the aggregation of vector $\mathbf { v } _ { u } . \mathbf { \Pi } ( \mathbf { c } )$ When $g > h _ { u }$ , since it isn’t known that which of the child nodes contributes this value, we consider that this value is uniformly split into four child nodes up to level $^ { g , }$ i.e., the projected vector $\pi _ { g } ( \mathbf { v } _ { u } )$ is a uniform split of vector $\mathbf { v } _ { u } .$ . Now, we define the distance $\scriptstyle d ( w , t )$ between worker w and task t as:

$$
d (w, t) := E M D (\pi_ {g} (\mathbf {v} _ {w}), \pi_ {g} (\mathbf {v} _ {t})). \tag {6}
$$

Fortunately, Eq. (6) is also equivalent to $| i _ { w } - i _ { t } |$ | when worker w and task t are at the same level of the quadtree. And the closest user can be determined.

Complexity Analysis: If task t and worker w are at the same level, we directly calculate the absolute value of the difference between the two node numbers, which takes only $O ( 1 )$ time. If task t and worker w are at different levels, by Eq. (6), we enumerate all components of vectors of length 4g and then calculate the distance, which takes 4g time. Hence, the time complexity of calculating the distance is $O ( 4 ^ { g } )$ .

# E. Accelerating Distance Calculation

Calculating the distance results in a huge time overhead. We propose a way to accelerate. The key observation is that the non-zero components of $\pi _ { g } ( \mathbf { v } _ { u } )$ are same and consecutive. And the distance can be calculated efficiently without converting node numbers into vectors.

Recall that worker w and task t are projected into level g to calculate the distance $d ( w , t )$ . Let $l e _ { u } , \ r i _ { u }$ and $n _ { u }$ be the minimum index of non-zero components, maximum index of none-zero components and the number of nonzero components on the projected vector $\pi _ { g } ( \mathbf { v } _ { u } )$ , respectively. According to the relationship between parent and child node numbers, $l e _ { u } , \ r i _ { u }$ and $n _ { u }$ can be calculated recursively. We divide the distance $d ( w , t )$ defined in Eq. (6) into the following three cases to accelerate distance calculation.

Case 1: $\mathrm { I f } ~ g \le h _ { w }$ and $g \leq h _ { t } .$ , we use $j _ { w }$ and $j _ { t }$ to represent the node numbers of worker w and task t after projected to level $^ { g , }$ respectively. Note that $j _ { u }$ can easily be obtained recursively by $i _ { u } .$ . Then, the distance can be represented as $d ( w , t ) = | j _ { w } - j _ { t } |$ .

Case 2: If $h _ { t } ~ \leq ~ g ~ \leq ~ h _ { w }$ or $h _ { w } ~ \le ~ g ~ \le ~ h _ { t }$ , without loss of generality, we assume that $h _ { t } \ \leq \ g \ \leq \ h _ { w }$ . If task t is the ancestor of worker w on the quadtree, we use $p o s _ { w }$ to represent the position of worker w on the $\pi _ { g } ( \mathbf { v } _ { t } )$ , i.e., $p o s _ { w } = n _ { w } - l e _ { t } + 1$ as shown in Fig. 4. Thus the distance is

![](images/d9be28931111114dbb13229013960f455b5455dfce5e9ee6fdf2bbe1c730b32a.jpg)



Fig. 4. Distance Calculation when $h t \leq g \leq h _ { w }$ and t is an ancestor of w

$$
\begin{array}{l} d (w, t) = \left(\sum_ {k = 1} ^ {\text { pos } _ {w} - 1} \frac {k}{n _ {t}}\right) + \left(\sum_ {k = 0} ^ {n _ {t} - \text { pos } _ {w}} \frac {k}{n _ {t}}\right) \\ = \frac {(p o s _ {w} - 1) p o s _ {w}}{2 n _ {t}} + \frac {(n _ {t} - p o s _ {w} + 1) (n _ {t} - p o s _ {w})}{2 n _ {t}} \\ = \frac {n _ {t} + 1 - 2 p o s _ {w}}{2} + \frac {p o s _ {w} (p o s _ {w} - 1)}{n _ {t}}, \\ \end{array}
$$

where the first equation divides $n _ { t }$ components of $\pi _ { g } ( \mathbf { v } _ { t } )$ into two parts with $p o s _ { w }$ as the dividing point. If task t is not the ancestor of worker w, we have the distance

$$
d (w, t) = \left\{ \begin{array}{l l} \frac {n _ {t} - 1}{2} + (n _ {w} - r i _ {t}), & \text {if n_{w} >ri_{t}}, \\ \frac {n _ {t} - 1}{2} + (l e _ {t} - n _ {w}), & \text {if n_{w} <  le_{t}}. \end{array} \right.
$$

![](images/e0e10c34dac739d56d32e6d55d09a5da5d57743b776ad036f08dbcba6422530c.jpg)



Fig. 5. Distance calculation when $g > h _ { w } \geq h _ { t }$ and t is an ancestor of w

Case 3: If $g > h _ { w }$ and $g > h _ { t }$ , without loss of generality, we assume that $g \ > \ h _ { w } \ \geq \ h _ { t } .$ . If task t is the ancestor of worker w on the quadtree as shown in Fig. 5, we use $m ^ { * }$ to represent the turning point where the accumulation function of worker w’s projected vector $\pi _ { g } ( \mathbf { v } _ { w } )$ is greater than or equal to task t’s, i.e., $\begin{array} { r } { \{ ( m - l e _ { t } + 1 ) \cdot \frac { 1 } { n _ { t } } \} = \lfloor \frac { ( l e _ { w } - 1 ) n _ { t } - ( l e _ { t } - 1 ) n _ { w } } { n _ { t } - n _ { w } } \rfloor } \end{array}$ $m ^ { * } = \arg \operatorname* { m i n } _ { m \in \mathbb { N } } ( m - l e _ { w } + 1 ) \cdot \frac { 1 } { n _ { w } } \geq$ . We have nw

$$
\begin{array}{l} d (w, t) = \sum_ {k = 1} ^ {l e _ {w} - l e _ {t}} \frac {k}{n _ {t}} + (\sum_ {k = l e _ {w} - l e _ {t} + 1} ^ {m ^ {*} - l e _ {t}} \frac {k}{n _ {t}} - \frac {k - (l e _ {w} - l e _ {t})}{n _ {w}}) \\ + (\sum_ {k = m ^ {*} - l e _ {t} + 1} ^ {r i _ {w} - l e _ {t}} \frac {k - (l e _ {w} - l e _ {t})}{n _ {w}} - \frac {k}{n _ {t}}) + \sum_ {k = 1} ^ {r i _ {t} - r i _ {w}} \frac {k}{n _ {t}} \\ = \frac {C _ {t}}{2 n _ {t}} + \frac {C _ {w}}{2 n _ {w}}, \\ \end{array}
$$

where $C _ { t } = ( 1 + m ^ { * } - l e _ { t } ) ( m ^ { * } - l e _ { t } ) - ( r i _ { w } + m ^ { * } - 2 l e _ { t } +$ $1 ) ( r i _ { w } - m ^ { * } ) + ( r i _ { t } - r i _ { w } ) ( r i _ { t } - r i _ { w } + 1 )$ and $C _ { w } = - ( m ^ { * } -$ $l e _ { w } + 1 ) ( m ^ { * } - l e _ { w } ) + ( r i _ { w } + m ^ { * } - 2 l e _ { w } + 1 ) ( r i _ { w } + m ^ { * } )$ . If

![](images/24f2fd20eb6be23b57801c9c242292f06c1a4ec8bf80847f6fe9290512f21111.jpg)



Fig. 6. Distance calculation when $g > h _ { w } \geq$ ht and t is not an ancestor of w

task t is not the ancestor of worker w as shown in Fig. 6, the distance is

$$
d (w, t) = \frac {n _ {t} - 1}{2} + \frac {n _ {w} - 1}{2} + (\max \{l e _ {t}, l e _ {w} \} - \min \{r i _ {t}, r i _ {w} \}).
$$

In view of the above three cases, the distance between worker w and task t can be efficiently calculated.

Now, we analyse the time complexity of the framework PQBF.

Theorem 2. Given H that is the height of quadtree. Given |W | and |T | that are the numbers of workers and tasks, respectively. The total time complexities for the user and the server are O(H) and $O ( | W | \cdot | T | \cdot H )$ , respectively.

Proof. For users, the time complexity of finding the node on the quadtree and personalized local generalization is $O ( H )$ and the complexity of personalized local perturbation is O(1). Thus the total time complexity for the user is $O ( H )$ .

For the server, the server only needs to distribute the parameters of the quadtree without constructing the quadtree. After all, the server only cares about the submitted node numbers. Thus, the time complexity of construction is O(1). When matching, the time complexity of calculating $l c _ { u } , \ r i _ { u }$ and $n _ { u }$ is $O ( H )$ and the time complexity of calculating the distance between worker w and task t is also O(H) in Section IV-E. In the worst case, workers has to compare with all tasks, which takes $O ( | W | \cdot | T | \cdot H )$ time. Thus the total time complexity for the server is $O ( | W | \cdot | T | \cdot H )$ . □

# V. EVALUATION

In this section, we evaluate the performance of our PQBF framework.

# A. Experimental Setup

# a) Datasets:

1) Synthetic data: The experimental settings for synthetic data are shown in table 1, where the bold parts are the default values. Specifically, in a 256 × 256 space, a Gaussian distribution with parameters µ and σ is used to generate workers $W = ( w _ { 1 } , w _ { 2 } , \cdot \cdot \cdot , w _ { | W | } )$ and tasks $T ~ = ~ ( t _ { 1 } , t _ { 2 } , \cdot \cdot \cdot , t _ { | T | } )$ , similar to [11]. Workers and tasks arrive in random order, and the server matches immediately. Inspired by [23], we randomly divide users into three groups: conservative, moderate and liberal. The privacy budgets of users in conservative, moderate and liberal groups are $\epsilon _ { C } , \epsilon _ { M }$ and $\epsilon _ { L } ,$ , respectively. A smaller privacy budget yields a higher level of privacy. The fractions of users in conservative, moderate and liberal groups are $f _ { C } , f _ { M }$ and $f _ { L } ,$ , respectively. We use H as the height of the quadtree published by the server. Users uniformly randomly select levels on the quadtree. Note that ϵ-geo-indistinguishability has privacy protection capability of level 8 of the quadtree in the 256×256 space but $P Q B F$ has users with random uniform levels. For the sake of fairness and considering users with high expectations of matching services, we choose H = 11 as the default value.

TABLE I EXPERIMENTAL SETTINGS FOR SYNTHETIC DATA 

<table><tr><td>Parameters</td><td>Settings</td></tr><tr><td> $|W|$ </td><td> $\{300, 400, \mathbf{500}, 600, 700\}$ </td></tr><tr><td> $|T|$ </td><td> $\{100, 200, \mathbf{300}, 400, 500\}$ </td></tr><tr><td>mean  $\mu$ </td><td> $\{75, 100, \mathbf{125}, 150, 175\}$ </td></tr><tr><td>standard deviation  $\sigma$ </td><td> $\{20, 30, \mathbf{40}, 50, 60\}$ </td></tr><tr><td>privacy budget  $\epsilon$ </td><td> $\epsilon_{C} = 0.01, \epsilon_{M} = 0.2, \epsilon_{L} = 1.0$ </td></tr><tr><td> $f_{C}$ </td><td> $\{0.1, 0.2, 0.3, 0.4, 0.5, \mathbf{0.54}, 0.6\}$ </td></tr><tr><td> $f_{M}$ </td><td>0.37</td></tr><tr><td> $f_{L}$ </td><td> $1.0 - (\epsilon_{C} + \epsilon_{M})$ </td></tr><tr><td> $H$ </td><td> $\{7, 9, \mathbf{11}, 13, 15\}$ </td></tr></table>

2) Real data (Similar to [49]): We use the T-drive dataset [51], [52], which has over 33, 000 GPS trajectories generated by taxis in 3 months. We randomly sample 500 locations as task locations and 500 locations as worker locations as shown in Fig. 9(a). Since the dataset does not give privacy preferences (i.e., a level $h _ { u }$ on the quadtree and a privacy budget $\epsilon _ { u } ) _ { : }$ , we assign the same setting to users as synthetic data. We then execute the algorithms to compare the results.

b) Compared Algorithms: In the PDPOMBM problem, we compare the following three algorithms with our PQBF: Non-private, the planar Laplacian mechanism [21], and TBF [11].

1) Non-private: The algorithm is the non-private mechanism and just uses the greedy algorithm to match the nearest users one by one.

2) Laplace: Laplace uses the planar Laplacian mechanism [21] which is a widely adopted technique to add noise to locations locally, and then the server greedily matches the nearest users.

3) TBF: TBF [11] is the state-of-the-art algorithm. Specifically, it builds an HST tree based on the pre-sampled locations (We use 20 uniformly sampled locations). The user then uses random walk to find the perturbed leaf node with his privacy budget, and finally the server finds the nearest user according to the distance on the HST tree to match.

c) Metrics: We use the total distance $d _ { R } ( S )$ of the matching S obtained by algorithms for comparison.   
d) Implementation: All the algorithms are implemented in Python. We run experiments on a computer with 4 Intel(R) Core(TM) i5-6500 3.20GHz processors and 16GB memory. Each experiment is repeated 10 times. And average results are reported.

# B. Experimental Results

Total Distance of Varing |W |. Fig. 7(a) shows the results of the total distance as a function of the number of workers $| W |$ . Non-private is most effective algorithm since it uses real locations to calculate. Our framework PQBF saves up to 45.7% and 26.0% total distance than Laplace and PTBF, respectively.

Total Distance of Varing |T |. Fig. 7(b) shows the results of the total distance as a function of the number of tasks |T |. Our PQBF outperforms Laplace and PTBF by up to 49.7% and 35.9%, respectively.

Total Distance of Varing µ. Fig. 7(c) shows the results of the total distance as a function of µ. Our framework PQBF is the most effective when satisfying ϵ-geo-indistinguishability. When $\mu = 1 2 5$ , it means that users are concentrated on the nearly central regions and algorithms have low total distance. Also, the total distance of PQBF is about 42.6% and 24.5% lower than Laplace and PTBF, respectively.

Total Distance of Varing σ. Fig. 7(d) shows the results of the total distance as a function of σ. PQBF achieves up to 48.1% and 34.9% shorter total distance than Laplace and TBF, respectively.

Total Distance of Varing fC . Fig. 7(e) shows the results of the total distance as a function of the smallest privacy budget’s proportion $f _ { C }$ . More users tend to be conservative as $f _ { C }$ increases, which leads to large the total distance of the same algorithm. Again, PQBF is still the most effective privacy algorithm in most cases.

Total Distance of Varing H. Fig. 7(f) shows the results of the total distance as a function of the quadtree’s height H. As H increases, more users have opportunity to select more finegrained regions and thus the total distance of PQBF becomes smaller. Non-private, Laplace and TBF are independent with H and only slightly fluctuate due to randomness.

Running time of Varing H. Fig. 8 shows the run time of the PQBF framework with and without distance calculation acceleration. We denote PQBF without distance calculation acceleration as PQBF w.o. DCA. All parameters take default values except for H. As H increases, the running time of PQBF hardly changes, while the running time of PQBF w.o. DCA increases exponentially.

![](images/8fdf2c4dd2d7f90773f93ce6b132d6e4a2eec12e7f95212930646e37b7ce1b1a.jpg)



(a) Total Distance of Varing |W |

![](images/4d46d2b930eb9d1ac4032d02d0198f0580d4f01f7d025c882fc32db7f95296a7.jpg)



(b) Total Distance of Varing |T |

![](images/37e887b71fe905b955fdb8db9fedbab92934a02ad823ee97399ca754d9f31f89.jpg)



(c) Total Distance of Varing |µ|

![](images/161559733ab8e5ae7d708125dba1538e90a0035013273d5dc025f078ae8cf93e.jpg)



(d) Total Distance of Varing |σ|

![](images/faf9d385e890028b18a9ddacfad807889ca904a937ff319b02c6ac1da5a6f15c.jpg)



(e) Total Distance of Varing $f _ { C }$

![](images/808b5ef6d0acb43964af5192ea6aeba80484d49a4e3bb916ab3ec4b054a5ebfe.jpg)



(f) Total Distance of Varing H   
Fig. 7. Results of Synthetic Data

![](images/dacfe7372d5e7afbfbaf1ec0fc6d407e5b1b5e4bdd32f50e94e561673e2cb90b.jpg)



Fig. 8. the comparison of the running time

Real Dataset. Fig. 9(a) is the distribution of 1000 users randomly selected from the real dataset. The users are not uniformly distributed in the region and concentrated in the region with large x-axis. The green plus nodes represents tasks and the blue circle nodes represents workers. Fig. 9(b) and Fig. 9(c) shows the results of the real dataset. In Fig. 9(b), as $f _ { C }$ increases, the total distance of PQBF increases more slowly than that of TBF and thus PQBF gradually outperforms TBF. In Fig. 9(c), the total distance of PQBF is up to 16.1% and 9.5% lower than Laplace and TBF, respectively.

Summary of Results. Our algorithm PQBF is more effective than the compared privacy-preserving algorithms Laplace and TBF on synthetic data and real data. It can save up to 49.7% and 35.9% total distance than Laplace and TBF, respectively. If users accept more fine-grained regions (i.e., large H), our PQBF achieves better results.

# VI. CONCLUSION

In this paper, we consider the personalized differentially private online minimum bipartite matching. To solve this problem, we design a Personalized Quadtree-Based privacypreserving matching Framework (PQBF). In this framework, we propose the GMT method on the quadtree whose structure allows users to intuitively select different generalization regions and using the truncated geometric mechanism satisfies ϵ-geo-indistinguishability at each level of the quadtree. We then formulate the distance using EMD on the quadtree and accelerate the distance calculation for efficient matching. The performance on both simulated and real data in evaluation demonstrates the effectiveness of our framework.

# ACKNOWLEDGMENT

This work was partially supported by National Key R&D Program of China under Grant No. 2021ZD0110400, China National Natural Science Foundation with No. 62132018, No. 61932016, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002. This work was partially supported by “the Fundamental Research Funds for the Central Universities” and the University Synergy Innovation Program of Anhui Province with No. GXXT-2019-024.

# REFERENCES

[1] Uber, https://www.uber.com/.

![](images/5ca15be3de0fe8c9304b2ad82f8a20c58cc94f54d37f353cb5ca7419e05055f5.jpg)



(a) Sampled 1000 Users’ Distribution of the real dataset

![](images/79da3cd9ce99a707cbaf3d30c7f544baee4170ac63ca96c43cedff84966b3e60.jpg)



(b) Total Distance of Varing $f _ { C }$

![](images/5fca320d3fc1b811a023731b2fdbbebf196553ff66ec70adebd7a833fd327fbe.jpg)



(c) Total Distance of Varing H   
Fig. 9. Results of Real Data

[2] Didi, https://www.didiglobal.com.   
[3] R. Shokri, G. Theodorakopoulos, J. L. Boudec, and J. Hubaux, “Quantifying location privacy,” in 32nd IEEE Symposium on Security and Privacy, S&P 2011, 22-25 May 2011, Berkeley, California, USA. IEEE Computer Society, 2011, pp. 247–262.   
[4] A. C. Squicciarini and C. Qiu, “Location privacy protection in vehiclebased spatial crowdsourcing via geo-indistinguishability,” in 39th IEEE International Conference on Distributed Computing Systems, ICDCS 2019, Dallas, TX, USA, July 7-10, 2019. IEEE, 2019, pp. 1061–1071.   
[5] X. Li, C. Zhang, T. Jung, J. Qian, and L. Chen, “Graph-based privacypreserving data publication,” in 35th Annual IEEE International Conference on Computer Communications, INFOCOM 2016, San Francisco, CA, USA, April 10-14, 2016. IEEE, 2016, pp. 1–9.   
[6] H. Du, L. Chen, J. Qian, J. Hou, T. Jung, and X.-Y. Li, “Patronus: A system for privacy-preserving cloud video surveillance,” IEEE Journal on Selected Areas in Communications, vol. 38, no. 6, pp. 1252–1261, 2020.   
[7] A. Meyerson, A. Nanavati, and L. J. Poplawski, “Randomized online algorithms for minimum metric bipartite matching,” in Proceedings of the Seventeenth Annual ACM-SIAM Symposium on Discrete Algorithms, SODA 2006, Miami, Florida, USA, January 22-26, 2006. ACM Press, 2006, pp. 954–959.   
[8] N. Bansal, N. Buchbinder, A. Gupta, and J. Naor, “A randomized o(log2 k)-competitive algorithm for metric bipartite matching,” Algorithmica, vol. 68, no. 2, pp. 390–403, 2014.   
[9] L. Zhang, X. Li, K. Liu, T. Jung, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in mobile social networks,” IEEE Trans. Mob. Comput., vol. 14, no. 9, pp. 1888–1902, 2015.   
[10] Y. Tong, J. She, B. Ding, L. Chen, T. Wo, and K. Xu, “Online minimum matching in real-time spatial data: Experiments and analysis,” Proc. VLDB Endow., vol. 9, no. 12, pp. 1053–1064, 2016.   
[11] Q. Tao, Y. Tong, Z. Zhou, Y. Shi, L. Chen, and K. Xu, “Differentially private online task assignment in spatial crowdsourcing: A tree-based approach,” in 36th IEEE International Conference on Data Engineering, ICDE 2020, Dallas, TX, USA, April 20-24, 2020. IEEE, 2020, pp. 517– 528.   
[12] A. Ghosh, T. Roughgarden, and M. Sundararajan, “Universally utilitymaximizing privacy mechanisms,” in Proceedings of the 41st Annual ACM Symposium on Theory of Computing, STOC 2009, Bethesda, MD, USA, May 31 - June 2, 2009, M. Mitzenmacher, Ed. ACM, 2009, pp. 351–360.   
[13] H. Samet, Foundations of multidimensional and metric data structures, ser. Morgan Kaufmann series in data management systems. Academic Press, 2006.   
[14] C. Dwork and A. Roth, “The algorithmic foundations of differential privacy,” Found. Trends Theor. Comput. Sci., vol. 9, no. 3-4, pp. 211– 407, 2014.   
[15] C. Li, M. Hay, G. Miklau, and Y. Wang, “A data- and workload-aware query answering algorithm for range queries under differential privacy,” Proc. VLDB Endow., vol. 7, no. 5, pp. 341–352, 2014.   
[16] M. Hay, C. Li, G. Miklau, and D. D. Jensen, “Accurate estimation of the degree distribution of private networks,” in ICDM 2009, The Ninth IEEE International Conference on Data Mining, Miami, Florida, USA,

6-9 December 2009, W. Wang, H. Kargupta, S. Ranka, P. S. Yu, and X. Wu, Eds. IEEE Computer Society, 2009, pp. 169–178.   
[17] Z. Qin, T. Yu, Y. Yang, I. Khalil, X. Xiao, and K. Ren, “Generating synthetic decentralized social graphs with local differential privacy,” in Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, CCS 2017, Dallas, TX, USA, October 30 - November 03, 2017, B. M. Thuraisingham, D. Evans, T. Malkin, and D. Xu, Eds. ACM, 2017, pp. 425–438.   
[18] J. Zhao, T. Jung, Y. Wang, and X. Li, “Achieving differential privacy of data disclosure in the smart grid,” in 2014 IEEE Conference on Computer Communications, INFOCOM 2014, Toronto, Canada, April 27 - May 2, 2014. IEEE, 2014, pp. 504–512.   
[19] R. C. Geyer, T. Klein, and M. Nabi, “Differentially private federated learning: A client level perspective,” CoRR, vol. abs/1712.07557, 2017.   
[20] A. Li, L. Zhang, J. Wang, F. Han, and X. Li, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, 2021.   
[21] M. E. Andres, N. E. Bordenabe, K. Chatzikokolakis, and C. Palamidessi, ´ “Geo-indistinguishability: differential privacy for location-based systems,” in 2013 ACM SIGSAC Conference on Computer and Communications Security, CCS’13, Berlin, Germany, November 4-8, 2013, A. Sadeghi, V. D. Gligor, and M. Yung, Eds. ACM, 2013, pp. 901–914.   
[22] M. Alaggan, S. Gambs, and A. Kermarrec, “Heterogeneous differential privacy,” J. Priv. Confidentiality, vol. 7, no. 2, 2016.   
[23] Z. Jorgensen, T. Yu, and G. Cormode, “Conservative or liberal? personalized differential privacy,” in 31st IEEE International Conference on Data Engineering, ICDE 2015, Seoul, South Korea, April 13-17, 2015, J. Gehrke, W. Lehner, K. Shim, S. K. Cha, and G. M. Lohman, Eds. IEEE Computer Society, 2015, pp. 1023–1034.   
[24] Y. Nie, W. Yang, L. Huang, X. Xie, Z. Zhao, and S. Wang, “A utilityoptimized framework for personalized private histogram estimation,” IEEE Trans. Knowl. Data Eng., vol. 31, no. 4, pp. 655–669, 2019.   
[25] B. Niu, Y. Chen, B. Wang, J. Cao, and F. Li, “Utility-aware exponential mechanism for personalized differential privacy,” in 2020 IEEE Wireless Communications and Networking Conference, WCNC 2020, Seoul, Korea (South), May 25-28, 2020. IEEE, 2020, pp. 1–6.   
[26] B. Niu, Y. Chen, B. Wang, Z. Wang, F. Li, and J. Cao, “Adapdp: Adaptive personalized differential privacy,” in 40th IEEE Conference on Computer Communications, INFOCOM 2021, Vancouver, BC, Canada, May 10-13, 2021. IEEE, 2021, pp. 1–10.   
[27] R. Chen, H. Li, A. K. Qin, S. P. Kasiviswanathan, and H. Jin, “Private spatial data aggregation in the local setting,” in 32nd IEEE International Conference on Data Engineering, ICDE 2016, Helsinki, Finland, May 16-20, 2016. IEEE Computer Society, 2016, pp. 289–300.   
[28] Y. Li, S. Liu, J. Wang, and M. Liu, “A local-clustering-based personalized differential privacy framework for user-based collaborative filtering,” in Database Systems for Advanced Applications - 22nd International Conference, DASFAA 2017, Suzhou, China, March 27-30, 2017, Proceedings, Part I, ser. Lecture Notes in Computer Science, K. S. Candan, L. Chen, T. B. Pedersen, L. Chang, and W. Hua, Eds., vol. 10177. Springer, 2017, pp. 543–558.   
[29] X. Meng, S. Wang, K. Shu, J. Li, B. Chen, H. Liu, and Y. Zhang, “Towards privacy preserving social recommendation under personalized privacy settings,” World Wide Web, vol. 22, no. 6, pp. 2853–2881, 2019.

[30] W. Wang, L. Chen, and Q. Zhang, “Outsourcing high-dimensional healthcare data to cloud with personalized privacy preservation,” Comput. Networks, vol. 88, pp. 136–148, 2015.   
[31] S. Zhang, L. Liu, Z. Chen, and H. Zhong, “Probabilistic matrix factorization with personalized differential privacy,” Knowl. Based Syst., vol. 183, 2019.   
[32] L. Cui, Y. Qu, M. R. Nosouhi, S. Yu, J. Niu, and G. Xie, “Improving data utility through game theory in personalized differential privacy,” J. Comput. Sci. Technol., vol. 34, no. 2, pp. 272–286, 2019.   
[33] Z. Wang, J. Hu, R. Lv, J. Wei, Q. Wang, D. Yang, and H. Qi, “Personalized privacy-preserving task allocation for mobile crowdsensing,” IEEE Trans. Mob. Comput., vol. 18, no. 6, pp. 1330–1341, 2019.   
[34] H. Jiang, J. Li, P. Zhao, F. Zeng, Z. Xiao, and A. Iyengar, “Location privacy-preserving mechanisms in location-based services: A comprehensive survey,” ACM Comput. Surv., vol. 54, no. 1, pp. 4:1–4:36, 2021.   
[35] X. Li and T. Jung, “Search me if you can: Privacy-preserving location query service,” in Proceedings of the IEEE INFOCOM 2013, Turin, Italy, April 14-19, 2013. IEEE, 2013, pp. 2760–2768.   
[36] J. Chen, K. He, Q. Yuan, M. Chen, R. Du, and Y. Xiang, “Blind filtering at third parties: An efficient privacy-preserving framework for locationbased services,” IEEE Transactions on Mobile Computing, vol. 17, no. 11, pp. 2524–2535, 2018.   
[37] X. Chen, X. Wu, X. Li, X. Ji, Y. He, and Y. Liu, “Privacy-aware highquality map generation with participatory sensing,” IEEE Trans. Mob. Comput., vol. 15, no. 3, pp. 719–732, 2016.   
[38] C. Cornelius, A. Kapadia, D. Kotz, D. Peebles, M. Shin, and N. Triandopoulos, “Anonysense: privacy-aware people-centric sensing,” in Proceedings of the 6th International Conference on Mobile Systems, Applications, and Services (MobiSys 2008), Breckenridge, CO, USA, June 17-20, 2008, D. Grunwald, R. Han, E. de Lara, and C. S. Ellis, Eds. ACM, 2008, pp. 211–224.   
[39] I. Krontiris and T. Dimitriou, “Privacy-respecting discovery of data providers in crowd-sensing applications,” in IEEE International Conference on Distributed Computing in Sensor Systems, DCOSS 2013, Cambridge, MA, USA, May 20-23, 2013. IEEE Computer Society, 2013, pp. 249–257.   
[40] L. Pournajaf, L. Xiong, V. S. Sunderam, and S. Goryczka, “Spatial task assignment for crowd sensing with cloaked locations,” in IEEE 15th International Conference on Mobile Data Management, MDM 2014, Brisbane, Australia, July 14-18, 2014 - Volume 1, A. B. Zaslavsky, P. K. Chrysanthis, C. Becker, J. Indulska, M. F. Mokbel, D. Nicklas, and C. Chow, Eds. IEEE Computer Society, 2014, pp. 73–82.   
[41] I. J. Vergara-Laurens, D. Mendez, and M. A. Labrador, “Privacy, quality of information, and energy consumption in participatory sensing systems,” in IEEE International Conference on Pervasive Computing and Communications, PerCom 2014, Budapest, Hungary, March 24-28, 2014. IEEE Computer Society, 2014, pp. 199–207.   
[42] G. Cormode, C. M. Procopiuc, D. Srivastava, E. Shen, and T. Yu, “Differentially private spatial decompositions,” in IEEE 28th International Conference on Data Engineering (ICDE 2012), Washington, DC, USA (Arlington, Virginia), 1-5 April, 2012, A. Kementsietsidis and M. A. V. Salles, Eds. IEEE Computer Society, 2012, pp. 20–31.   
[43] J. Zhang, X. Xiao, and X. Xie, “Privtree: A differentially private algorithm for hierarchical decompositions,” in Proceedings of the 2016 International Conference on Management of Data, SIGMOD Conference 2016, San Francisco, CA, USA, June 26 - July 01, 2016, F. Ozcan, ¨ G. Koutrika, and S. Madden, Eds. ACM, 2016, pp. 155–170.   
[44] Y. Yan, X. Gao, A. Mahmood, T. Feng, and P. Xie, “Differential private spatial decomposition and location publishing based on unbalanced quadtree partition algorithm,” IEEE Access, vol. 8, pp. 104 775–104 787, 2020.   
[45] S. Li, Y. Geng, and Y. Li, “A differentially private hybrid decomposition algorithm based on quad-tree,” Comput. Secur., vol. 109, p. 102384, 2021.   
[46] S. Shaham, G. Ghinita, R. Ahuja, J. Krumm, and C. Shahabi, “HTF: homogeneous tree framework for differentially-private release of location data,” in SIGSPATIAL ’21: 29th International Conference on Advances in Geographic Information Systems, Virtual Event / Beijing, China, November 2-5, 2021, X. Meng, F. Wang, C. Lu, Y. Huang, S. Shekhar, and X. Xie, Eds. ACM, 2021, pp. 184–194.   
[47] L. Wang, D. Yang, X. Han, T. Wang, D. Zhang, and X. Ma, “Location privacy-preserving task allocation for mobile crowdsensing with differential geo-obfuscation,” in Proceedings of the 26th International Conference on World Wide Web, WWW 2017, Perth, Australia, April

3-7, 2017, R. Barrett, R. Cummings, E. Agichtein, and E. Gabrilovich, Eds. ACM, 2017, pp. 627–636.   
[48] Y. Qian, Y. Ma, J. Chen, D. Wu, D. Tian, and K. Hwang, “Optimal location privacy preserving and service quality guaranteed task allocation in vehicle-based crowdsensing networks,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 7, pp. 4367–4375, 2021.   
[49] H. To, C. Shahabi, and L. Xiong, “Privacy-preserving online task assignment in spatial crowdsourcing with untrusted server,” in 34th IEEE International Conference on Data Engineering, ICDE 2018, Paris, France, April 16-19, 2018. IEEE Computer Society, 2018, pp. 833–844.   
[50] C. Fu, H. Huang, and R. Weibel, “Adaptive simplification of GPS trajectories with geographic context - a quadtree-based approach,” Int. J. Geogr. Inf. Sci., vol. 35, no. 4, pp. 661–688, 2021.   
[51] J. Yuan, Y. Zheng, C. Zhang, W. Xie, X. Xie, G. Sun, and Y. Huang, “T-drive: driving directions based on taxi trajectories,” in 18th ACM SIGSPATIAL International Symposium on Advances in Geographic Information Systems, ACM-GIS 2010, November 3-5, 2010, San Jose, CA, USA, Proceedings, D. Agrawal, P. Zhang, A. E. Abbadi, and M. F. Mokbel, Eds. ACM, 2010, pp. 99–108.   
[52] J. Yuan, Y. Zheng, X. Xie, and G. Sun, “Driving with knowledge from the physical world,” in Proceedings of the 17th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Diego, CA, USA, August 21-24, 2011, C. Apte, J. Ghosh, and´ P. Smyth, Eds. ACM, 2011, pp. 316–324.