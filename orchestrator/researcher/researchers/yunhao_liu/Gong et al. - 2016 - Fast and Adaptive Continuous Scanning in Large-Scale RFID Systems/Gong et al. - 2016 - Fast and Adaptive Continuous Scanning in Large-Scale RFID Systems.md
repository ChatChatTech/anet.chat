# Fast and Adaptive Continuous Scanning in Large-Scale RFID Systems

Wei Gong, Member, IEEE, Haoxiang Liu, Xin Miao, Member, IEEE, Kebin Liu, Member, IEEE, Wenbo He, Member, IEEE, Lan Zhang, Member, IEEE, and Yunhao Liu, Fellow, IEEE, ACM

Abstract—Radio Frequency Identification (RFID) technology plays an important role in supply chain logistics and inventory control. In these applications, a series of scanning operations at different locations are often needed to cover the entire inventory (tags). In such continuous scanning scenario, adjacent scans inevitably read overlapping tags multiple times. Most existing methods suffer from low scanning efficiency when the overlap is small, since they do not distinguish the size of overlap which is an important factor of scanning performance. In this paper, we analytically unveil the fundamental relationship between the performance of continuous scanning and the size of overlap, deriving a critical threshold for the selection of scanning strategy. Further, we design an accurate estimator to approximate the overlap. Combining the estimate and a compact data structure, an adaptive scanning scheme is introduced to achieve low communication time. Through detailed analysis and extensive simulations, we demonstrate that the proposed scheme significantly outperforms previous approach in total scanning time.

Index Terms—Continuous scanning, RFID tags, intersection estimation.

# I. INTRODUCTION

R ADIO Frequency Identification (RFID) technology hasbeen widely used in a number of applications, such as been widely used in a number of applications, such as inventory control, supply chain logistics and object tracking. Compared with traditional bar code systems, RFID has the following advantages. First, it extends the operation range from inches to meters. Second, RFID readers can communicate with tags in non-line-of-sight scenario, allowing tags to be embedded in objects.

A fundamental operation in RFID systems is tag scanning, which aims to collect tag IDs to identify the associated objects.

Manuscript received February 07, 2015; revised October 26, 2015; accepted January 01, 2016; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor S. Chen. This work was supported in part by the NSFC under Grants No. 61472268, No. 61303196, No. 61472218, and No. 61472211. W. Gong and H. Liu are the co-primary authors.

W. Gong is with the School of Computing Science, Simon Fraser University, Burnaby BC V5A 1S6, Canada (e-mail: gongweig@sfu.ca).

H. Liu is with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong (e-mail: haoxiang@greenorbs.com).

X. Miao, K. Liu, L. Zhang, and Y. Liu are with the School of Software, Tsinghua National Lab for Information Science and Technology, Tsinghua University, Beijing 100084, China (e-mail: miao@greenorbs.com; kebin@greenorbs.com; zhanglan@greenorbs.com; yunhao@greenorbs.com).

W. He is with the School of Computer Science, McGill University, Montreal, QC H3A 0E9, Canada (e-mail: wenbohe@cs.mcgill.ca).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TNET.2016.2521333

![](images/9691e6c08ccce07bffc47564152d6ed5f44f982be17a58584a8769bdf4460fa1.jpg)



(a)

![](images/694c011a56baededa86d501e1317d2b1cf53d95e67e10472bdcdaa5a5b37b234.jpg)



(b)   
Fig. 1. The scanning performance depends on the portion of overlap. If it is large, select the unknown tags first. Otherwise, identify directly. (a) Large overlap (b) Small overlap.

For example, a clothes retailer stocks a large volume of clothes in a warehouse. Every piece of them is affixed with an RFID tag. In order to manage the inventory, it is necessary for the retailer to scan the tags to keep track of the clothes. Considering that the clothes (tag) volume may be as large as tens of thousands, and the scanning is frequently operated, a fast scanning method is desired.

In practice, the typical communication distance between an RFID reader and off-the-shelve passive tags is within 12 meters [1]. A single scan clearly cannot cover the entire warehouse. Consequently, a series of scanning operations are needed to identify all the tags, which is defined as continuous scanning. In continuous scanning, adjacent scans inevitably read overlapping tags multiple times, resulting in redundancy. Fig. 1(a) illustrates an example. is the tag set to be identified, and is the tag set that is previously collected. Tags in the overlap of A and B are read twice.

Sheng et al. [2] investigated the continuous scanning problem and proposed an approach that avoids collecting tags in the overlapping region. Their idea is to take advantage of the tags previously gathered (i.e., ) to only collect the unknown tags (i.e., ). The approach starts with a tag selection phase that keeps the tags in active and meanwhile suppress tags in . However, it suffers from low efficiency when the overlap is small (Fig. 1(b)), since the overhead of selection phase overwhelms the benefits it brings. In this case, it is better to directly collect all the tags in and remove the redundant IDs in the back-end server.1

In this paper, we observe that the performance of continuous scanning heavily depends on the portion of overlap, and propose an Adaptive COntinuous Scanning scheme (ACOS). We systemically quantify the fundamental relationship between the scanning performance and the overlap, deriving a critical

1We assume the server has powerful computing capability.

threshold for the selection of scanning strategy. In ACOS design, several challenges must be addressed. First, how to accurately and efficiently estimate the overlap? Second, how to design an efficient method to avoid reading redundancy $( A \cap B )$ in case the overlap is large? To address the first challenge, we design a lightweight estimator to approximate the overlap based on the idea of MinHash [3]. The estimate is then compared with the threshold to select the scanning strategy. To address the second challenge, we construct a compact tag selector and broadcast it to the tags in . Notified by the selector, tags in suppress communication with the reader and will not report their IDs afterwards.

The major contributions of this work can be summarized as follows.

• We observe that the performance of continuous scanning is closely related to the portion of overlap. We analytically quantify the fundamental relationship between the scanning performance and the overlap, deriving a critical threshold for scanning strategy selection.   
• We design an accurate estimator for the overlap based on MinHash. The scanning strategy is chosen by comparing the estimate with the threshold.   
We propose ACOS, an adaptive scanning scheme that incorporates the estimator and a compact tag selector. Detailed theoretical analysis and extensive simulations are conducted to verify the efficiency of our scheme.

# II. RELATED WORK

Existing work on tag identification can be divided into two categories, namely single scanning and continuous scanning. In single scanning, the research focuses on designing anti-collision protocols. The protocols generally fall into two classes according to the collision arbitration method: ALOHA-based protocols [4], [5] and tree-based protocols [6], [7]. In ALOHAbased protocols, the reader broadcasts a frame size to the tags indicating the number of slots in the frame. Each tag randomly selects a slot in the frame and responds its ID. If multiple tags respond in the same slot, their signals collide and none of them can be decoded by the reader. The collided tags are arranged to transmit in the next frame. Tree-based approaches resolve tag collision by splitting collided tags into subsets, and schedule the subsets to transmit separately. The splitting process terminates until the subset contains only one tag. The identification process can be organized as a binary tree.

Different from single scanning, the key challenge in continuous scanning is how to deal with overlapping tags. The most related work to ours is Collecting Unknown (CU) proposed by Sheng et al. [2]. CU employs an algorithm that simply avoids reading overlapping tags, which has two drawbacks. First, CU is an inefficient strategy when the portion of overlap is small. Second, even if the overlap is large, the tag selection approach in CU can be further improved. In this paper, we study the fundamental relationship between the scanning performance and the portion of overlap, and solve both deficiencies of CU. Our solution is based on ALOHA protocol, but orthogonal to all the anti-collision protocols. In addition, unknown tag identification problem is studied in [8], [9]. Xie et al. [10] conduct the first comprehensive experimental study on mobile reader scanning. They mostly focus on practical issues while our work is more generalized.

Some other topics also investigate tag set operations, such as missing tag detection [11] and tag searching [12]. In missing tag detection, the objective is to quickly pinpoint missing tags in the whole tag set. The problem is essentially finding a subset of tags. Tag searching problem focuses on quickly searching a given set of tags in a batch of unknown ones. This problem can be formulated as finding the intersection of two sets. Both topics are different from continuous scanning problem, since continuous scanning aims to identify the unknown tags while the other two deal with known tags. Apart from the tag scanning or identification problem, there are a series of works that study tag estimation problem in which the objective is to acquire the rough number of tags with desired accuracy [13]–[16]. In this paper, we also study an ”estimation” problem but it is totally different from the tag estimation problem. Our goal is to estimate a ratio of two tag sets rather than the size of a single tag set.

# III. SYSTEM MODEL AND PROBLEM STATEMENT

# A. System Model

An RFID continuous scanning system consists of three components: a reader (preferably a mobile reader), a number of tags and a back-end server. The back-end server stores the gathered tag IDs. The reader continuously changes its location to interrogate the tags and reports the IDs to the server via high speed networks. So the communication time between reader and server can be neglected, and we mainly focus on the wireless communication time between reader and tags. According to the EPC C1G2 [17], RFID tags are required to implement a set of mandatory functions, such as responding ID, reading and writing memory. Besides, tags are capable of performing simple computations such as lightweight hash functions.

Our approach adopts the slotted ALOHA model as underlying MAC protocol. The time is divided into a sequence slots of equal size. At the beginning of each slot, the reader issues a request, and tags respond in the second half of the slot. A slot can fall in three categories according to the number of responding tags. If no tag responds, the slot is called an empty slot. If only one tag responds, it is denoted as singleton slot. The transmitted signal in a singleton slot can be successfully decoded by the reader. If multiple tags respond simultaneously, the reader will detect a collision, and thus the slot is called collision slot. Tags have two types of responds as specified by the reader's request: a 96-bit ID or a single bit. We formally denote the single-bit response as short response in this paper. The short response contains no information but to inform the reader a non-empty slot. The time of an ID slot and short response slot are denoted as $t _ { i d }$ and $t _ { s } ,$ respectively. Additionally, we denote $t _ { b }$ as the time for the reader to transmit 1 bit. A common relation is $t _ { s } < t _ { b } < t _ { i d }$ , since reader usually adopt a lower transmission rate than tags[11], [18].

# B. Problem Statement

The objective of continuous scanning is to collect tag IDs in each reading location. As shown in Fig. 1, we have two tag sets. is the set of tags to be identified in current location. contains the tags gathered in previous locations and stored in the server. The tags in $A - B$ are defined as unknown tags, and those in $A \cap B$ are defined as known tags. Therefore, the problem is to design an efficient method to collect the unknown tags with minimum communication time.

While C1G2 protocol has some built-in functions to inventory a number of tags, it has limitations in many ways. For example, exact persistence times cannot be set by the user, in some commercial readers, e.g., impinj [19] and using flag to determine whether a tag has been inventoried might fail in ‘Dual Search’ mode [19]. Furthermore, the availability of four sessions in C1G2 for each tag is limited when multiple readers are spatially distributed to cover a large region that might be overlapped. In summary, our aim is to design a robust and general continuous scanning scheme, which works with spatial-temporal diversity from tags and readers, e.g., mobile tags and multiple readers.

# IV. ACOS DESIGN AND ANALYSIS

In this section, we present the detailed design and analysis of ACOS.

# A. Quantifying Continuous Scanning

Generally, there are two strategies to identify the unknown tags in $A - B$ in continuous scanning. The first one is a onephase approach called Collect All, or CA for short. Namely, the reader collects all the tags in and uploads the IDs to the back-end server. The server is responsible for duplicate elimination, i.e., removing the redundant IDs at the back end. The second one is a two-phase approach called Select Unknown, or SU for short. It consists of a selection phase and a collection phase. In the selection phase, the reader suppresses the known tags from responding afterwards, while keeping the unknown tags active. In the collection phase, the reader only reads the active tags. These two strategies exhibit differently when the relationship between set and varies. To compare the performance of CA and SU, we separately measure the communication time between the reader and tags of each strategy and make a comparison. The details are as follows.

1) Communication Time of CA: We use the typical Framed Slotted ALOHA-based ID collection protocol (FSA) for CA. In FSA, the reader broadcasts a frame size $f ,$ and each tag randomly selects a slot in the frame to respond. Generally, let be the number of tags to identify. The expected number of empty slots $r _ { 0 }$ and singleton slots $r _ { 1 }$ in the frame can be easily obtained.

$$
r _ {0} = f (1 - \frac {1}{f}) ^ {n} \approx f e ^ {- \rho} \tag {1}
$$

$$
r _ {1} = n (1 - \frac {1}{f}) ^ {n - 1} \approx n e ^ {- \rho} \tag {2}
$$

where $\rho = n / f$ .

Following the EPC C1G2 [17], there are three types of slots in identification: empty slot, collision slot, and singleton slot, in which identification information will be collected. We define frame efficiency $E F$ as the proportion of singleton slot time in the frame. Note that singleton slot time here includes the time for tag ID transmission, hence it is approximately equal to $t _ { i d } . ^ { 2 }$ The empty slot time $\left( t _ { e m p t y } \right)$ and collision slot time $\left( t _ { c o l l i s i o n } \right)$ are much shorter (empty slot time is even shorter than collision slot time). Let $\begin{array} { r } { \alpha = \frac { t _ { e m p t y } ^ { - } } { t _ { i d } } } \end{array}$ and tid $\begin{array} { r } { \beta = \frac { t _ { c o l l i s i o n } } { t _ { i d } } } \end{array}$ . We calculate $E F$ as follows

$$
E F = \frac {r _ {1} t _ {i d}}{r _ {1} t _ {i d} + r _ {0} t _ {\text { empty }} + (f - r _ {0} - r _ {1}) t _ {\text { collision }}} \tag {3}
$$

$$
= \frac {r _ {1}}{r _ {1} + r _ {0} \alpha + (f - r _ {0} - r _ {1}) \beta}. \tag {4}
$$

should be maximized to achieve minimum communication time.

Now we calculate the optimal value of $\rho$ that achieves maximum frame efficiency. Given $r _ { 0 }$ and $r _ { 1 }$ , we have $\begin{array} { r } { E F = \frac { \rho } { e ^ { \rho } + ( 1 - \beta ) \rho + \alpha - \beta } } \end{array}$ . Let the first order derivative of $E F$ w.r.t. be 0, we derive $e ^ { \rho } ( 1 - \rho ) = 1 - \alpha / \beta .$ . Therefore, the optimal value of $\cdot _ { \rho , \cdot }$ denoted as $\hat { \rho } ,$ satisfies $e ^ { \hat { \rho } } ( 1 - \hat { \rho } ) = 1 - \alpha / \beta$ .

FSA protocol needs several rounds of frames due to tag collision. Let $n _ { i }$ be the number of unidentified tags before the $i ^ { t h }$ round. Initially, $n _ { 1 } ~ = ~ n$ . The number of tags identified (singleton slots) in the $i ^ { t h }$ round is $\Delta n = n _ { i } e ^ { - \hat { \rho } }$ according to (1). Then we have the following induction

$$
n _ {i + 1} = n _ {i} - \Delta n = (1 - e ^ {- \hat {\rho}}) n _ {i}.
$$

Solving the induction, we have $n _ { i } ~ = ~ n ( 1 - e ^ { - { \hat { \rho } } } ) ^ { i - 1 }$ . Since the process terminates when $n _ { i } ~ < ~ 1$ ,The identification will run $\begin{array} { r } { r = \ln ( \frac { 1 } { n } ) / \ln ( 1 - e ^ { - \hat { \rho } } ) } \end{array}$ rounds. Finally, we sum over the frames in all rounds to calculate the total communication time. More precisely, the cost is $\begin{array} { r } { \sum _ { i = 1 } ^ { r } ( r _ { 1 } ^ { i } + r _ { 0 } ^ { i } \alpha + ( f _ { i } - r _ { 0 } ^ { i } - r _ { 1 } ^ { i } ) \beta ) t _ { i d } } \end{array}$ , where $r _ { 0 } ^ { i }$ and $r _ { 1 } ^ { i }$ are the expected number of empty slots and singleton slots in the $i ^ { t h }$ frame of size $f _ { i }$ . With a bit calculation, we have

$$
\begin{array}{l} \sum_ {i = 1} ^ {r} (r _ {1} ^ {i} + r _ {0} ^ {i} \alpha + (f _ {i} - r _ {0} ^ {i} - r _ {1} ^ {i}) \beta) t _ {i d} = \frac {e ^ {- \rho}}{\beta e ^ {\hat {\rho}} + 1 - \beta} t _ {i d} \sum_ {i = 1} ^ {r} n _ {i} \\ \approx \frac {n}{\beta e ^ {\hat {\rho}} + 1 - \beta} t _ {i d}. \tag {5} \\ \end{array}
$$

Therefore, the overall communication time to identify tags is $\frac { n } { \beta e ^ { \hat { \rho } } + 1 - \beta } t _ { i d }$ . Note that $\frac { 1 } { \beta e ^ { \hat { \rho } } + 1 - \beta }$ is a constant. We let $\gamma =$ . With this general result, we establish Theorem 1. $\frac { 1 } { \beta e ^ { \hat { \rho } } + 1 - \beta }$

Theorem 1: The communication time of CA is $| A | \gamma t _ { i d }$ .

Proof: The result directly follows (5).

2) Communication Time of SU: The communication time of SU is the sum of selection cost and collection cost. The selection time essentially depends on the specific selection method. Despite this, we can temporarily use a general form $\lambda | B | ( \lambda \geq 1 )$ to describe the cost, since the reader has to transmit at least 1 bit to preclude each tag in from , i.e., select tags in $A - B$ . The parameter is method specific. We will give the for our selection approach later in Section IV-C. The time of collection phase can be easily derived from (5).

Theorem 2: The communication time of SU is $\lambda | B | +$ $| A - B | \gamma t _ { i d }$ .

Proof: The communication time of Su Is the sum of selection phase and collection phase.

3) Performance Comparison: Based on Theorem 1 and Theorem 2, we have the following conclusion. If

2If some systems do require exact singleton slot time, it is intuitive to make changes in following formulas since it follows the same derivations.

$| A | \gamma t _ { i d } \ge \lambda | B | + | A - B | \gamma t _ { i d } , \mathrm { i . e . , } \frac { | A \bigcap _ { } B | } { | B | } \ge \lambda / \gamma t _ { i d }$ , we choose SU as the scanning strategy. Otherwise, we choose CA. The term $C ( A , B ) = \textstyle { \frac { | A \bigcap { B } | } { | B | } }$ , which depicts the portion of overlap, is called the containment of in . Denote as the optimal scanning time. The relationship between $T$ and $C ( A , B )$ can be quantified in (6)

$$
T = \left\{ \begin{array}{l l} \lambda | B | + | A - B | \gamma t _ {i d}, & C (A, B) \geq \lambda / \gamma t _ {i d} \\ | A | \gamma t _ {i d}, & C (A, B) <   \lambda / \gamma t _ {i d} \end{array} \right. \tag {6}
$$

where the critical threshold used for strategy selection is $\lambda / \gamma t _ { i d }$ .

# B. Set Containment Estimation

In the last section, we analytically quantify the relationship between scanning performance and $C ( A , B )$ . The key point, therefore, is to estimate $C ( A , B )$ to optimize the performance. In this section, we introduce three estimators that progressively refines one another to estimate $C ( A , B )$ .

The first two estimators are based on inclusion-exclusion principle. By inclusion-exclusion principle, we have

$$
\begin{array}{l} C (A, B) = \frac {| A | + | B | - | A \bigcup B |}{| B |} \\ = \frac {| A |}{| B |} + 1 - \frac {| A \bigcup B |}{| A \bigcap B |} C (A, B). \tag {7} \\ \end{array}
$$

We introduce $J ( A , B ) = { \frac { | A \bigcap B | } { | A { \big | } \ B { \big | } } }$ , which is called the Jaccard similarity of and [20]. So from (7) we get

$$
C (A, B) = \frac {J (A , B)}{1 + J (A , B)} \left(1 + \frac {| A |}{| B |}\right). \tag {8}
$$

Since the server knows as a priori, there are two unknowns to estimate $C ( A , B )$ , namely $| A |$ and $J ( A , B )$ . To obtain $| A |$ , various tag cardinality estimation schemes can be leveraged. For example, Qian et al. proposed a fast estimation scheme in [?], which achieves fairly accurate result with small overhead. Hence, the focus is shifted to estimating $J ( A , B )$ . It is clearly infeasible to enumerate the IDs in and to exactly figure out $J ( A , B )$ due to the high communication cost of collecting each ID in . We instead design two time-efficient probabilistic estimators based on MinHash [3] to estimate $J ( A , B )$ (for $C ( A , B )$ , computing formula 7 is needed). The first one is a preliminary estimator in which tags are required to compute multiple hash functions. The second one is an enhanced estimator in which tags only compute one hash function while achieving higher time efficiency.

1) Multiple Hash-Based Similarity Estimator: We present the Multiple Hash-based similarity Estimator (MHE) ${ \hat { J } } _ { m } ( A , B )$ . The basic idea of MHE is to let each tag in and generate a hash value, and the minimum hash values of two sets are compared to derive ${ \hat { J } } _ { m } ( A , B )$ . Let be a hash function that uniformly maps the tag IDs in and to distinct values in $\{ 0 , 1 , 2 , \ldots , D - 1 \}$ . We define $( h ( A ) )$ , min $. ( h ( B ) )$ as the smallest values in set $h ( A )$ and $h ( B )$ , respectively. If $\iota ( h ( A ) ) \ : = \ : \operatorname* { m i n } ( h ( B ) )$ , it implies that this minimum hash value is generated by the same tag ID in and $B ,$ which obviously lies in $A \cap B$ . Since each tag ID has same probability to be mapped to the the smallest hash value, we obtain $P r ( \operatorname* { m i n } ( h ( A ) ) = \operatorname* { m i n } ( h ( B ) ) ) = J ( A , B )$ . Note that hash collisions should be avoided to guarantee the distinctness of hash values among and . According to the arguments in the birthday problem [21], should be $O ( | A \cup B | ^ { 2 } )$ to guarantee distinctness if each tag ID is mapped to $\{ 0 , 1 , 2 , \ldots ,$ $D - 1 \}$ uniformly at random. In the rest of this paper, we set $D = \tilde { O ( } | A \cup B | ^ { 2 } )$ and assume all hash values are distinct, i.e., no hash collisions exist.

Denote $X \in \{ 0 , 1 \}$ as the random variable that is 1 if min $( h ( A ) ) \ = \ \operatorname* { m i n } ( h ( B ) )$ and 0 otherwise. Then is an unbiased estimator for $J ( A , B )$ , despite that the estimation variance is too high to be useful. To reduce the variance of the estimator, we use independent hash functions and repeat the procedure times. Let the observations be $\{ X _ { 1 } , X _ { 2 } , \ldots , X _ { k } \} . \ J ( A , B )$ can be estimated using the mean as $\begin{array} { r } { \hat { J } _ { m } ( A , B ) ~ = ~ \bar { X } ~ = ~ \frac { 1 } { k } \sum _ { i = 1 } ^ { k } X _ { i \cdot } ~ \hat { J } _ { m } ( A , B ) } \end{array}$ is also an unbiased estimator since $E [ \hat { J } _ { m } ( A , B ) ] = E [ \bar { X } ] = J ( A , B )$ . Observe that the estimation variance decreases as we increase . We show how many hash functions would be sufficient to reach desired accuracy requirement in the following Lemma 1 and Lemma 2. We adopt the typical $( \epsilon , \delta ) \mathrm { - a p p r o x - }$ imation to describe the accuracy of an estimator, where and are called absolute error bound and failure probability, respectively.

Lemma 1: To meet the accuracy requirement that $\begin{array} { r } { P r ( | \hat { J } _ { m } ( A , B ) - J ( A , B ) | < \varepsilon ) > 1 - \delta , k \ge \frac { 2 } { \varepsilon ^ { 2 } } \ln { \frac { 2 } { \delta } } } \end{array}$ .

Proof: This is a typical chernoff bound [21] for 0-1 random variable $X _ { i }$ . The Detailed proof is omitted.

Lemma 1 gives a bound w.r.t. absolute error . The bound w.r.t. relative error is shown in Lemma 2.

Lemma 2: To meet the requirement that $P r ( | \hat { J } _ { m } ( A , B )$ $\begin{array} { r } { J ( A , B ) | < \varepsilon J ( A , B ) ) > 1 \stackrel { \cdot } { - } \delta , k \geq \frac { 2 + \varepsilon } { \varepsilon ^ { 2 } J } \ln \frac { 2 } { \delta } } \end{array}$ .

Proof: By Chernoff Bound, we have $\hat { P r } ( | \hat { J } _ { m } ( A , B ) \ -$ $\begin{array} { r l r } { J ( A , B ) | } & { { } \ge } & { \varepsilon J ( A , B ) ) \le 2 e x p ( - \frac { \varepsilon ^ { 2 } } { 2 + \varepsilon } \cdot J ( A , B ) k ) } \end{array}$ . It follows that $P r ( | { \hat { J } } _ { m } ( A , B ) - J ( A , B ) | \ \leq \ \varepsilon J ( A , B ) ) \ >$ 1-2exp(- $\cdot \frac { \varepsilon ^ { 2 } } { 2 \pm \varepsilon } \cdot J ( \dot { A } , B ) \dot { k } )$ m2 . To achieve $( \epsilon , \delta ) \mathrm { - a c c u r a c y } .$ , we get $\begin{array} { r } { 2 \exp ( - \frac { \varepsilon ^ { 2 } } { 2 + \varepsilon } \cdot J ( A , B ) k ) > \delta } \end{array}$ m2 . Solving this inequality, we have $\begin{array} { r } { k \geq \frac { 2 + \overline { { \varepsilon } } } { \varepsilon ^ { 2 } J } \bar { \ln } \frac { 2 } { \delta } } \end{array}$ .

Now the critical issue is to search the minimum hash value from tags in , i.e., $( h ( A ) )$ , since the server can easily calculate $\left( h ( B ) \right)$ given as priori. We design an algorithm that exploits binary search. In specific, the reader keeps broadcasting a one-bit query that is used to sequentially match each bit in the hash values, until the minimum hash value is found. Fig. 2 illustrates an example of the search algorithm. In the first slot, the reader broadcast a $^ \circ$ to check if any hash value starts with prefix $^ \circ$ . Two tags with hash values 010, 011 issue a short response to claim their existence. The reader detects a non-empty slot and proceeds to the second bit. The reader again queries with $^ \circ$ in the second slot, but detects an empty slot as neither 010 or 011 has 0 in their second bit. So it queries with $^ { \mathfrak { c } } 1 ^ { \mathfrak { s } }$ afterwards. The process is repeated until the reader finds $^ { \circ } 0 1 0 ^ { \circ }$ as the minimum hash value. Algorithm 1 and 2 show the pseudo code of the the search algorithm for reader and tags. Note that the each should have a bit string in their memory to store the queries from the reader so far to make the algorithm work. It follows from the algorithm that for each $^ { \circ }$ in the minimum hash value, the communication cost between the reader and tags is one slot, and for each $^ { \mathfrak { c } } 1 ^ { \mathfrak { s } }$ , the cost is 2 slots. Therefore, the total number of slots of this algorithm is $m _ { 0 } ( x ) + 2 m _ { 1 } ( x )$ , where $m _ { 0 }$ and $m _ { 1 }$ are the number of $^ \circ$ and $^ { \circ } 1 ^ { \circ }$ in the minimum hash value $x = \operatorname* { m i n } ( h ( A ) )$ , respectively. Moreover, we have

![](images/8ad3d31f4807ec0a6506e2e6e89219d46a9b4738831ec9bccc7636ed6518996a.jpg)



Fig. 2. The minimum hash value search process. The black and gray nodes are existing tags, in which the black node represents the tag with the minimum hash value. Solid boxes denote queries that have non-empty reply, and dotted boxes denote queries with empty reply.

Algorithm 1: The minHash search algorithm for reader.   
min ← ””;  
for i ← 1 to log D do  
    Broadcast ‘0’;  
    Wait for response;  
    If response is empty then  
    Broadcast ‘1’;  
    Append ‘1’ to min;  
    else  
    Append ‘0’ to min;  
    end  
end  
return min;

$$
m _ {0} (x) + 2 m _ {1} (x) <   2 (m _ {0} (x) + m _ {1} (x)) = 2 \log D.
$$

Considering that the algorithm should run $\begin{array} { r } { k \ = \ { \cal O } ( \frac { 1 } { \varepsilon ^ { 2 } } \ln \frac { 1 } { \delta } ) } \end{array}$ rounds (for absolute error in Lemma 1), the cost of MHE should be $O ( \frac { \log D } { \varepsilon ^ { 2 } } \ln \frac { 1 } { \delta } )$ slots.

2) Single Hash-Based Similarity Estimator: The multiple hash-based estimator requires many rounds of estimation. Therefore, it will be computationally expensive for tags to calculate many hash functions. Can we reduce the computational cost of tags while maintaining the communication cost? In fact, we can just use one hash function to achieve even faster estimation. Specifically, we let the tags in and compute one hash function and select the smallest hash values from $h ( A )$ and $h ( B )$ . Define $h _ { k } ( A )$ as the smallest hash values of . $h _ { k } ( B )$ and $h _ { k } ( A \cup B )$ are similarly defined for and $A \bigcup B$ . Due to the property of uniform hashing, $h _ { k } ( A \cup B )$ can be considered as a simple random sample3 drawn from $A \bigcup B$ , but with the tag IDs mapped to hash values. Then, $| h _ { k } ( \bar { A } \bigcup B ) \bigcap h _ { k } ( A ) \bigcap h _ { k } ^ { - } ( B ) |$ is the subset of samples in that are hashed from $| A \cap B |$ . We therefore can use ${ \frac { | h _ { k } ( A \bigcup B ) \bigcap h _ { k } ( A ) \bigcap h _ { k } ( B ) | } { k } }$ k to approximate $\begin{array} { c c l } { { { \cal J } ( A , B ) } } & { { = } } & { { { \frac { | A \bigcap B | } { | A | \big d B | } } } } \end{array}$ , given all hash values are distinct. Thus the Single Hash-based Estimator (SHE) is

3A simple random sample is a subset of individuals (a sample) chosen from a larger set (a population).

Algorithm 2: The minHash search algorithm for tags.   
prefix ← ;
i ← 0;
While True do
    query ← wait for query;
    If query ≠ 1 then
    Append query to prefix;
    else
    Replace the last bit of prefix to 1;
    end
    If h starts with prefix then
    Short response;
    else
    Keep silent;
    end
    i = i + 1;
    If i = log D then
    i = 0
    If prefix = h then
    Keep silent until activated
    end
    Clear prefix;
    end
end

$\begin{array} { r l r } { \hat { J } _ { s } ( A , B ) } & { { } = } & { \frac { | h _ { k } ( A \bigcup B ) \bigcap h _ { k } ( A ) \bigcap h _ { k } ( B ) | } { k } } \end{array}$ . We show that k $\hat { J } _ { s } ( A , B )$ is unbiased.

Lemma $3 \colon \hat { J } _ { s } ( A , B )$ is an unbiased estimator for $J ( A , B )$ .

Proof: The sampling probability is $k / | A \cup B |$ . Let random variable $X _ { i }$ be 1 if element is sampled in and else 0. Then we have $\begin{array} { r c l } { \hat { J } _ { s } ( A , B ) } & { = } & { \frac { 1 } { k } \sum _ { i \in { \cal A } \bigcap B } { \cal X } _ { i } } \end{array}$ . The expectation of ${ \hat { J } } _ { S } ( A , B )$ is

$$
E [ \hat {j} _ {s} (A, B) ] = \frac {| A \bigcap B |}{k} E [ X _ {i} ] = \frac {| A \bigcap b |}{k} \frac {k}{| A \bigcup B |} = J (A, B).
$$

Hence $\hat { J } _ { s } ( A , B )$ is an unbiased estimator.

The value of to achieve $( \epsilon , \delta )$ -approximation is the same as that in Lemma 1 and Lemma 2.

In SHE, we have to collect the smallest hash values from . To achieve this, we design an efficient minimum hash value search algorithm. The intuition of our algorithm is as follows. The hash values in $h ( A )$ can be considered as evenly distributed in space $[ 0 , D - 1 ]$ . Hence, if we divide $[ 0 , D - 1 ]$ into subintervals of equal size $\begin{array} { r } { \frac { D } { | \boldsymbol { h } ( \boldsymbol { A } ) | } \approx \frac { D } { | \boldsymbol { A } | } } \end{array}$ , then ideally each subinterval contains one hash value, as shown in Fig. 3. By interval partition, we expectedly reduce the search space for one hash value, from the entire interval to $\textstyle { \frac { D } { | A | } }$ . To achieve the partition, the reader finds the smallest integer that satisfies $\begin{array} { r } { 2 ^ { r } \geq \frac { D } { | A | } } \end{array}$ , i.e., $\begin{array} { r } { r \ = \ \lceil \log _ { 2 } \frac { D } { | A | } \rceil } \end{array}$ . The first $\boldsymbol { D } \_ { r }$ bits in the hash values are used to distinguish the subintervals, which we call subinterval prefix. When searching the hash values in a specific subinterval, the reader simply broadcasts the corresponding subinterval prefix to select the corresponding tags. For example, suppose $| A | = 1 , 0 0 0$ , then $r = 9$ and the subinterval prefixes are:

![](images/3972335f5e6523422181c18e7724e0669b44cea631b9efe86736f96f69e60cbc.jpg)



Fig. 3. The ideal distribution of 5 hash values in $[ 0 , D - 1 ]$ . We evenly partition the interval to 5 subintervals. $k = 3$ smallest hash values are located in the 3 rightmost subintervals.

Algorithm 3: The -minimum hash value search algorithm for reader.   
minArray ← []; r ← $\left\lceil \log_{2} \frac{D}{|A|} \right\rceil$ ;
for i ← 0 to $2^{\log D - r} - 1$ do
    Broadcast the binary string of i;
    Wait for response;
    While response is non-empty do
    min ← binarySearch();
    Add min to minArray;
    Broadcast the binary string of i;
    Wait for response;
    end
end
return minArray;

$\{ 0 \} ^ { 9 } , \{ 0 \} ^ { 8 } 1 , \ldots , \{ 1 \} ^ { 9 }$ . Note that $\textstyle { \frac { D } { | A | } }$ is not necessarily integral power of 2. So prefix matching might divide $[ 0 , D - 1 ]$ into approximately even subintervals.

The search process starts from subinterval . In each subinterval, we conduct binary search to find the contained hash values as described in Algorithm 1 and 2, until smallest hash values are gathered. If a subinterval contains multiple hash values, we should repeatedly search the minimum hash value among unknown ones the until the subinterval is clear. When a hash value is found, we let the corresponding tag keep silence to prevent it from interrupting the following search (they will be activated when the search process terminates). In Fig. 4 we use a binary tree to illustrate how the algorithm works. Initially, we search in the subinterval with prefix 00, which contains hash value 001. Then in the second subinterval, no hash value with prefix 01 exists. So we turn to the third subinterval and find 100, 101. So far, we have gathered three hash values and the search terminates. Algorithm 3 shows the pseudo code of the minimum hash value search algorithm for the reader. The algorithm for tags is the same as Algorithm 2.

The communication cost of SHE depends on the distribution of minimum hash values. Consider the situation where each subinterval contains one hash value, the communication cost is $\begin{array} { r } { O \big ( \frac { 1 } { \varepsilon ^ { 2 } } \log \frac { D } { | A | } \ln \frac { 1 } { \delta } \big ) } \end{array}$ slots, which is better than MHE. Even in the worst case, the cost of SHE is $O ( \frac { \log D } { \varepsilon ^ { 2 } } \ln \frac { 1 } { \delta } )$ 2 slots, which is the same as MHE. Note that both MHE and SHE are sublinear algorithms $\operatorname { w . r . t . } | A \cup B |$ . Hence, the communication cost of estimation is much more efficient than that of identification, which is linear to the number of tags. This ensures the lightweight property of our estimator.

3) Advanced Set Containment Estimator: Recall that both MHE and SHE aim to estimate $J ( A , B )$ , and $C ( A , B )$ can be calculated using $J ( A , B )$ and based on (7). The problem here is, the communication overhead of deriving is inevitable. Now we present an advanced estimator for $C ( A , B )$ which further saves the overhead of deriving . Specifically, we estimate $| A \cap B |$ directly rather than referring to inclusion-exclusion. The following equation gives our insight

$$
C (A, B) = \frac {| A \bigcap B |}{| B |} = \frac {J (A , B)}{| B |} | A \bigcup B |. \tag {9}
$$

In $( 9 ) , J ( A , B )$ can be obtained by either MHE or SHE, and $| B |$ is known. The other term $| A \cup B |$ is estimated as follows. Think of a hash function that maps each tag ID in and to values in $\{ 0 , 1 , \ldots , D - 1 \}$ uniform at random. The $k ^ { t h }$ smallest hash value in $h ( A \cup B ) ,$ , denoted as $h ^ { ( k ) } ( A \cup B )$ , is expectedly located at the point ${ \frac { D } { | A \left[ \int B | k \right. } }$ . Therefore, the union size $| A \cup B |$ can be estimated as $\frac { D k } { h ^ { ( k ) } ( A \bigcup B ) }$ Note that this estimator for $| A \cup B |$ is compatible with SHE for $J ( A , B )$ , since only the smallest hash values in and are required to perform the estimation. Hence, these two estimations can be achieved simultaneously. The communication overhead of the advanced set containment estimator is equal to that of SHE, and further improves the time efficiency compared with the former two methods to derive $C ( A , B )$ since deriving is no longer needed.

# C. Compact Tag Selector

In case Select Unknown (SU) is the better strategy, we need an efficient unknown tag selection method. We show that the previous selection method in [2] is inefficient. A new compact tag selector is introduced and incorporated in ACOS.

Previous Method: The existing method proposed in [2] exploits the transition of slot state to select the unknown tags. Specifically, the reader sends a frame and a random number . Each tag in replies a short response in slot $h ( I D , r ) \in$ $\{ 0 , 1 , \ldots f - 1 \}$ , where is a hash function. The reader locally generates a virtual frame $f ^ { \prime }$ and maps the tags in to $f ^ { \prime }$ with the same and . If an empty slot in $f ^ { \prime }$ turns out to be a non-empty slot in $f ,$ , the tags in that map to this slot must be unknown. Fig. 5 gives an illustrative example of this method. Multiple frames are used until all unknown tags are selected with high probability (with false positive). The communication cost of this method is proportional to $| A \cup B |$ according to the analysis in [2].

The Compact Tag Selector: We design a compact selector to efficiently select the unknown tags by utilizing Bloom filter [22]. Bloom filter is a bit vector that compactly represents a set. To build the tag selector, the reader constructs a vector of bits and initialize every bit to 0. It chooses independent hash functions $h _ { 1 } , h _ { 2 } , \ldots , h _ { k }$ , and each has an output uniformly distributed in $\{ 1 , 2 , \ldots , m \}$ . For each tag $\mathrm { I D } b \in B$ , positions $h _ { 1 } ( b ) , h _ { 2 } ( b ) , \ldots , h _ { k } ( b )$ in the bit vector are set to 1. Consequently, the reader encodes set into a compact structure. In the selection phase, the selector is broadcast to . When receiving the selector, every tag with ID $a \in A$ checks positions $h _ { 1 } ( a ) , h _ { 2 } ( a ) , \ldots , h _ { k } ( a )$ in the selector. If any of the positions is 0, then . So is an unknown tag and keeps active. If all the positions in the vector are 1, classifies itself into $A \cap B _ { : }$ , and keeps silence in the collection phase. Since Bloom filter yields false positive, $| A - B | \times P _ { F P }$ tags in $A - B$ may be incorrectly suppressed. Note that both existing method and the Bloom filter allow false positives.

![](images/ddd3b604c47ccf2d702f2ec25e0cbd5f4826d3db5bfef555660dd61f98f1d1d2.jpg)



(a)

![](images/022e38d425a3f01395b33b32350836c8e40b140af8fc182c59095e2f6df763bc.jpg)



(b)

![](images/452923640a6800bf46fe9070cce81ac911e2238d6c544ff620173421f97d9a53.jpg)



Fig. 4. An example of $k = 3$ minimum hash value search. The black nodes represent existing hash values. A hash value is underlined if it is found. The highlighted subtrees are subintervals. The search terminates in the $3 ^ { r d }$ subinterval from the left. (a) Subinterval 1, prefix 00. (b) Subinterval 2, prefix 01. (c) Subinterval 3, prefix 10.   
![](images/fa2efba7dab7c05fcc552c8bc18509c10a300a9ab95676673d7282b21a54d135.jpg)



Fig. 5. The existing unknown tag selection method. The $4 ^ { t h }$ slot in frame f is non-empty while is empty in f'. Hence, tag 5 must be an unknown tag.

Now, we show how the reader determines the optimal parameters and , given a desired false positive rate $P _ { F P }$ . Let $B F ( B )$ represent the Bloom filter for set . The false positive rate can be easily obtained as

$$
\begin{array}{l} p _ {F P} = \operatorname * {P r} [ x \in B F (B) \bigcap x = 1 ] ^ {k} \\ = \left(1 - \left(1 - \frac {1}{| B F (B) |}\right) ^ {k | B |}\right) ^ {k} \\ \approx (1 - e ^ {- k | B F (B) | / | B |}) ^ {k}. \tag {10} \\ \end{array}
$$

From (10), we can calculate the optimal number of hash functions that achieve minimum false positive rate

$$
k = \ln 2 \frac {| B F (B) |}{| B |}. \tag {11}
$$

Hence, given the optimal and , the Bloom filter size becomes

$$
| B F (B) | = \frac {- \ln p _ {F P}}{(\ln 2) ^ {2}} | B |. \tag {12}
$$

With false positive rate $P _ { F P ; }$ , the optimal number of hash functions and Bloom filter size can be derived from (11) and (12). Here we can determine the value of in Section $\mathrm { I V } { \ - } \mathbf { A }$ , which is $\begin{array} { r } { \lambda = \frac { - \ln p _ { F P } } { ( l n 2 ) ^ { 2 } } t _ { b } } \end{array}$ from (12). Therefore, the relationship

Algorithm 4: The adaptive continuous scanning scheme ACOS.   
Input: $B$ , $P_{FP}$ , $\hat{\rho}$ .

Estimates $C(A, B)$ ;

If $\hat{C}(A, B) < \frac{-\ln P_{FP} t_b}{(ln2)^2 \gamma t_{id}}$ then

Directly collect the IDs in $A$ using ALOHA-based protocol;

else

Generate a Bloom filter $BF(B)$ and select tags in $A - B$ ;

Collect the IDs in $A - B$ using ALOHA-based protocol;

end

between total scanning time and $C ( A , B )$ in (6) can be renewed in (13), where $T _ { A C O S } , T _ { e s t }$ are the scanning time of ACOS and estimation time, respectively. The communication cost of our compact tag selector is proportional to $| B | < | A \bigcup B |$ , given the same false positive rate. Hence, our approach is more efficient, especially when $| A \cup B |$ is much larger than .

$$
T _ {A C O S} = \left\{ \begin{array}{l} \frac {- \ln p _ {F P} | B |}{(\ln 2) ^ {2}} t _ {b} + | A - B | \gamma t _ {i d} + T _ {e s t}, C (A, B) \geq \frac {- l n p _ {F P} t _ {b}}{(\ln 2) ^ {2} \gamma t _ {i d}} \\ | A | \gamma t _ {i d} + T _ {e s t}, C (A, B) <   \frac {- \ln p _ {F P} t _ {b}}{(\ln 2) ^ {2} \gamma t _ {i d}} \end{array} . \right. \tag {13}
$$

# D. Adaptive Continuous Scanning Scheme

Now we wrap up and show the general design of ACOS. ACOS basically comprises of two phases, namely estimation phase and execution phase. In estimation phase, we adopt the estimator in Section IV-B to estimate $C ( A , B )$ . In the execution phase, we can adaptively decide the better scanning strategy (CA or SU) according to (13). If SU is adopted, we use compact selector to select the unknown tags. Algorithm 4 presents the adaptive continuous scanning scheme in detail.

Now we quantitatively show that ACOS outperforms nonadaptive scanning strategies in expected scanning time. By nonadaptive strategy, we refer to Collect All (CA) and Select Unknown (SU). Since continuous scanning can be divided into a series of two-tag-set scenes, we only need to show that ACOS outperforms non-adaptive strategies in each two-tag-set scene. Given no prior knowledge of tag distribution, ACOS is translated to either CA or SU with equal probability. Therefore, the expected scanning time of ACOS in two-tag-set scene is

$$
E [ T _ {A C O S} ] = \frac {1}{2} T _ {C A} + \frac {1}{2} T _ {S U} + T _ {e s t}. \tag {14}
$$

Then $E [ T _ { A C O S } ]$ is smaller than either $T _ { C A }$ or $T _ { S U }$ . Take $T _ { C A }$ as an example, $\begin{array} { r } { T _ { C A } - E [ T _ { A C O S } ] = \frac { 1 } { 2 } T _ { C A } - T _ { e s t } } \end{array}$ . Since $T _ { e s t }$ is $O ( \log D ) \ = \ O ( \log | A \bigcup B | )$ while either $T _ { C A }$ or $T _ { S U }$ is $O ( | A \cup B | ) , T _ { C A }$ is larger than $E [ T _ { A C O S } ]$ asymptotically. In conclusion, the ACOS is more time efficient in expectation compared with non-adaptive scanning strategies.

# V. DISCUSSION

Hardware Requirements: The hardware implementation of ACOS requires the programmability on both reader and tag. For reader, the user-defined command is supported by most commercial readers, e.g., Impinj speedway series. ACOS can use built-in commands, e.g, Query, to construct frame which is used to interrogate tags. When we need collect ID, traditional C1G2 workflow shall be followed to do so. At the same time, ACOS needs to define several user-defined commands. The first major group of user-defined commands is the MinHash search which can broadcast command type and corresponding data, e.g., single bit $^ { \circ } \mathrm { , ~ } ^ { \circ } \mathrm { 1 } ^ { \mathrm { 3 } }$ , and bit string. The second one is for constructing bloom filter and selecting tags. For tag side, ACOS can be implemented using programmable passive tags, e.g., WISP [23], or active tags, e.g., OpenBeacon [24].

Hash Functions: The set similarity estimation is based on MinHash. In theory, perfect MinHash requires that all elements in the set have equal probability to be the minimum element of image under the hash function. This requirement, however, is unrealistic in practical use. Several work addresses this problem by proposing approximate MinHash families [25]. In Section VI, we show that simple hash functions with pseudorandom output can achieve ideal results, which are favorably lightweight and friendly for tags to use.

The Biased Estimation: We have proven that the two estimators for set similarity, namely ${ \hat { J } } _ { m } ( A , B )$ and $\hat { J } _ { s } ( A , B )$ , are unbiased. However, rather than estimated straightforwardly, the set containment is derived from ${ \hat { J } } ( A , B )$ . Referring to (8), we have $\begin{array} { r } { \hat { C } ( A , B ) \sim \frac { \hat { J } ( A , B ) } { 1 + \hat { J } ( A , B ) } } \end{array}$ . By Jensen's inequality, we have

$$
E \left[ \frac {\hat {J} (A , B)}{1 + \hat {J} (A , B)} \right] \leq \frac {E [ \hat {J} (A , B) ]}{1 + E [ \hat {J} (A , B) ]} = \frac {J (A , B)}{1 + J (A , B)}.
$$

Therefore, the estimate of $C ( A , B )$ is biased. We may choose to add a bias correction to acquire more accurate estimate. According to our evaluation, however, this biased estimator already achieves satisfactory result.

Dealing With Growing : As the continuous scanning process proceeds, the known tag set, i.e., set will grow larger. As a result, the communication cost of both set containment estimation and tag selection will gradually become higher. To prevent this situation, we can periodically update set . Specifically, for the tags identified scanning locations before, we can exclude them from , where is a parameter that can be tuned according to the radio coverage of the reader. We should ensure that the tags covered by the reader across reading locations hardly overlap.

Alternative for Searching Minhash Values: There is an alternative for searching min hash values as follows. This method has two-pass. Let be the minimal hash value in set B. In the first pass, the reader first broadcasts H to A. Then each tag in set A keeps listening and replies to the reader only when its hash value is less than or equal to . If reader gets any response, it means $( h ( A ) ) < = \operatorname* { m i n } ( h ( B ) )$ . Otherwise, we start the second phase which is to repeat the first phase. The only difference is let be the minimal hash value in set A and broadcast it to set B. All tags in B follows the way as set A does in the first phase. Then if there is any response, that means $( h ( A ) ) =$ min $\left( h ( B ) \right)$ . Otherwise, $( h ( A ) ) > \operatorname* { m i n } ( h ( B ) )$ . Note that in our former scheme, the number of bits transmitted by the reader is always less than or equal to $2 ^ { * }$ (number of bits in the smallest hash value), whereas in this alternative scheme the number of bits transmitted by the reader is exactly twice the number of bits in the smallest hash value. From this perspective, former scheme maybe better in terms of communication cost. On the other hand, if in some systems, the transmission waiting time matters, this two-pass scheme might achieve better time efficiency. Anyway, the difference between those two scheme is not too much compared to other communication overhead, such as transmission of tag ID. For practical implementation, we can make the choice based on specific system parameters.

Deployment Issues: When deploying ACOS into field, we are going to face a lot of challenges, such as missing reading, mutual interference, and the power of reader. In [10], they had done an excellent job in giving a framework which can optimize reading performance in various practical settings. ACOS can follow this framework in real world deployment. In particular, we can apply their probabilistic backscattering model which can effectively depict the regularities during reading. Moreover, effective scanning windows can be employed to evaluate the reading performance across multiple tags.

# VI. PERFORMANCE EVALUATION

In this section, we evaluate the performance of ACOS under extensive simulations. First, we assess the accuracy and cost of set containment estimators. Then we compare ACOS with the recent methods under various settings.

# A. Simulation Settings

Timings: We follow the EPC C1G2 [17] and Phillips I-code specification [26]. According to the standard, reader transmits at rate ranging from 26.7 kbps to 128 kbps. Tags transmit at rate ranging from 32 kbps to 640 kbps. The transmission rates are varied to adjust to different channel conditions and application scenarios. In this simulation, we select typical transmission rates for reader and tags to be compatible to prior arts [11], [27]. In our settings, the reader transmission rate is 26.7 kbps and tag transmission rate is 53 kbps. Hence, it takes 0.037 ms and 0.019 ms for the reader and tag to send 1 bit, respectively. Also, we should consider the waiting time before reader and tag transmission. We refer to [11] and set the waiting time to 0.3 ms. After amortizing the waiting time to each bit, we keep the following timing relation in the simulation.

$$
t _ {b}: t _ {s}: t _ {i d} = 1: 8: 5 5
$$

where the unit time is about 0.038 ms. Note that here $t _ { s }$ is larger than $t _ { b }$ due to the amortized waiting time. Due to the diversity of manufacturers, the timings might be slightly different, but generally have the same scale.

![](images/74473c34522a9b57bb4b1e382cbeceda1b7259644e76a9280b612c112a564446.jpg)



(a)

![](images/0ade234574279cfe071e5fa0887de4df0e5adf2243d380572568e4ccd535c266.jpg)



(b)

![](images/8938fa9dd37a8e0798541e31ba076759676300b62a8c1db34486851912f71e8d.jpg)



（c）

Fig. 6. Estimate using MHE for $J ( A , B )$ . Then std when number of hash functions is 20 is not shown, since it is much larger than others. (a) Mean. (b) Relative error. (c) Standard deviation.   
![](images/c7bbfbefad6e18009e9aa142718d2d54e264165057933620fb403b227bac68ce.jpg)



![](images/0e6eb1cec0fd18ab5ff9d1aca9772575aa73f134988073a8f2a2d5354999e0e4.jpg)



(b)

![](images/1288363875bf6dbad0510042e1900be24cf8bf523c586bf4987f93e6f615087e.jpg)



（c）

Fig. 7. Estimate using SHE for $J ( A , B )$ . Then std when number of samples is 20 is not shown, since it is much larger than others. (a) Mean. (b) Relative error. (c) Standard deviation.   
![](images/6a7c7d2f4c4f9be9b2229df20598d5e02982455ca5cfa3c8817956ebe5e72edf.jpg)



(@)

![](images/c9f70a002124bb08b951dfb90d335225d1ed0244d2acbfe68a0384f7f923068e.jpg)



(b)

![](images/0f3a622088e8dace5210d84845309ada189bc68f2d78037c2940796ef360b116.jpg)



（c）  
Fig. 8. Estimate using advanced estimator. Then std when number of hash functions is 20 is not shown, since it is much larger than others. (a) Mean. (b) Relative error. (c) Standard deviation.

False Positive Rate: The tags to be scanned might be thousands. Hence, we set the false positive rate $P _ { F P }$ to be $1 0 ^ { - 4 }$ to keep almost all tags identified. Although $P _ { F P }$ impacts the threshold in (13), our scheme is adaptive thus does not rely on a specific $P _ { F P }$ .

Optimal Identification Time: According to our analysis in Section IV-A, the optimal identification time for tags is $n \gamma t _ { i d }$ . According to [2], $\alpha ~ = ~ 0 . 0 5$ and $\beta ~ = ~ 0 . 1$ in (4). We solve $\begin{array} { r } { e ^ { \hat { \rho } } ( 1 - \hat { \rho } ) = 1 - \frac { \alpha } { \beta } } \end{array}$ to derive the optimal value $\hat { \rho }$ and can be therefore derived using . $\begin{array} { r } { \gamma = \frac { 1 } { \beta e ^ { \hat { \rho } } + 1 - \beta } } \end{array}$ 1

Number of Tags in : In the simulation, we assume is known as a prior for MHE and SHE. One can employ the approach in [13] to quickly estimate .

# B. Set Containment Estimation

We use three metrics to evaluate the accuracy of set containment estimation. For simplicity, we use to represent $\hat { C } ( A , B )$ . The first metric is the mean $E [ \hat { c } ]$ . The second metric is relative error, defined as $\frac { | c - \hat { c } | } { c }$ where is the actual set containment. C The third metric is standard deviation (std) $\pmb { \sigma } = \sqrt { E [ ( c - \hat { c } ) ^ { 2 } ] }$ . In this experiment, both and are set to 5000 and varies from to 0.1 to 0.9. The experiment is repeated 50 times.

The results in Figs. 6 and 7 show the accuracy of , when estimator MHE and SHE are adopted for $J ( A , B )$ . Fig. 8 shows the accuracy of advanced estimator. We make the following observation from these figures. First, is approximately unbiased, since the $E [ \hat { c } ]$ is very close to when ranges from 0.1 to 0.9. Second, the relative error of estimation drops when we increase the number of hash functions (in MHE) or the number of samples (in SHE and advanced estimator). As illustrated in Figs. 6(b) and 7(b), if we choose 100 hash functions/samples, the relative error decreases to approximately 0.1 when $c = 0 . 5$ . Also, we observe from Fig. 8(b) that the advanced estimator is more accurate than MHE and SHE based estimator. The relative error stays below 0.2 across all values for , while in Figs. 6(b) and 7(b) the relative error is sometimes large. In addition, the relative error for MHE and SHE decreases when increases. This is easy to understand by Lemma 2. Third, the standard deviation basicallt gets smaller when more hash functions/samples are used, as shown in Figs. 6(c), 7(c) and 8(c). For example, the std drops from $5 . 2 \times 1 0 ^ { - 3 }$ with 40 hash functions to $2 . 5 \times 1 0 ^ { - 3 }$ with 100 hash functions, when $c = 0 . 5$ .

![](images/c8b13adf74d031fd3d8be5729e9bdf570f64c6fee91a30fef62525b9be3c893b.jpg)



Fig. 9. Vary $k , | A | = 5 , 0 0 0$ .

![](images/6f8f71d84871d623e036abb2e9fe0cf0aa6be3eb0a1ea13b651287ca4dbca386.jpg)  
Fig. 10. Vary $| A | , \mathbf { k } = 1 0 0 .$ .

Moreover, we examine the communication cost of estimation. Note that the communication cost of estimating is essentially the communication cost of estimating $J ( A , B )$ . Therefore, we just evaluate the cost of MHE and SHE separately. Two parameters and may impact the cost, where is the number of hash functions in MHE or number of samples in SHE. The evaluation is conducted from two perspectives. First, we fix to 5,000, and vary from 40 to 100. The results are presented in Fig. 9. The communication cost of MHE and SHE increase with . Particularly, SHE has slower growth trend since the cost of SHE is approximately $\begin{array} { r } { O ( \log { \frac { D } { | A | } } \bar { k } ) } \end{array}$ , while that of MHE is $O ( \log D k )$ . Second, we vary $| A |$ and keep $k = 1 0 0$ . In Fig. 10, we observe that SHE is more efficient than MHE. Additionally, the cost of MHE is independent of , whereas the cost of SHE slightly decreases as the grows. This observation further verifies our cost analysis. Due to its better efficiency and comparable accuracy, we use SHE in our following simulations.

# C. Impact of Estimation Error

We investigate how the estimation error of impacts the overall performance of ACOS. Note that ACOS selects the better strategy between Collect All and Select Unknown based on the estimation of and the constant threshold. If the estimation error grows to certain extent that results in the selection of secondary strategy, the performance of ACOS will not be the optimal. So we need to know how much inaccuracy ACOS can handle to still maintain optimal strategy selection in various scenarios. The threshold $\frac { \dot { - } l n p _ { F P } { } ^ { t } b } { ( \ln 2 ) ^ { 2 } \gamma t _ { i d } } = \dot { 0 . 3 9 }$ (In2）2ytid given all constants in the simulation settings. Here we still consider three scenarios $c = 0 . 1 , c = 0 . 5$ and $c = 0 . 9$ to allow for small, medium and large overlap between two consecutive scans. Without loss of generality, we set $| A | \ = \ 5 0 0 0$ . The simulation results are shown in Fig. 11. Each figure shows the ideal scanning time when estimation error is 0 and the actual scanning time when estimation error varies. We find that the impact of estimation error on scanning time depends on the value of . In specific, when approaches the threshold $0 . 3 9 , \mathrm { e . g . , } c = 0 . 5$ , the relative estimation error less than will result in secondary strategy selection. When is away from 0.39, e.g., $c = 0 . 1$ or $c = 0 . 9$ , the scanning time of ACOS is less sensitive to estimation error. In some extreme cases such as is very close to 0.39, very small estimation error is likely to result in secondary strategy.

# D. Performance Comparison

We compare the performance of ACOS with the recent continuous scanning approach CU, tag identification protocol Adaptive Binary Splitting (ABS) [6], and a more recent protocol called probabilistic Tree Hopping (TH) [7]. ABS deals with tag mobility and classify tags into staying tags, arriving tags and leaving tags in identification, which is similar to continuous scanning. In specific, in Fig. 1(a) tags in $A \cap B ,$ , $A - B$ and $B - A$ can be viewed as staying tags, arriving tags and leaving tags in ABS, respectively. ACOS selects the better scanning strategy from Collect All (CA) and Select Unknown (SU), based on the estimation . We call the other strategy that is not eventually selected by ACOS as secondary strategy. For example, if CA is selected by ACOS, then SU becomes the secondary strategy. In conclusion, we compare ACOS with four methods, CU, ABS, TH, and the secondary strategy. The estimation time is included in ACOS but not in the other methods. In this experiment, we only consider one scanning location as depicted in Fig. 1.

To consider different continuous scanning scenarios, we vary the set containment . Namely is set to 0.1, 0,5 and 0.9. For each , we set $| B | = 5 , 0 0 0$ and change from 3,500 to 5,000. Fig. 12 illustrates the comparison in terms of scanning time among the four methods. In all scenarios, ACOS outperforms CU, ABS, TH, and secondary. For example, when $c \ = \ 0 . 1$ and $| A | = 3 { , } 5 0 0$ , ACOS is 16% faster than secondary, 48% faster than ABS, 40% faster than TH, and 44% faster than CU. The reason why ACOS always outperforms lies in two aspects. First, when is small (Fig. 12(a)), ACOS chooses CA, which is apparently the better strategy. In contrast, CU selects tags in $A - B$ first, resulting in large overhead. ABS and TH do not perform well when the overlap is small. Second, when is large (Figs. 12(b) and 12(c)), both ACOS and CU adopt a tag selection phase. ACOS is better than CU due to the efficiency of compact tag selector. ABS and TH perform well in large overlap but still worse than ACOS and CU. In Table I, we further present the percentage of estimation cost in ACOS under various settings. It is evident that our estimation scheme is time efficient, constituting no more than 11% of total scanning cost. Therefore, even if estimation cost is counted, ACOS still achieves much performance gain compered with CU.

# E. Multiple Scanning Locations

We further evaluate the performance of ACOS in multiple scanning location scenario, in which the reader makes a series of moves to scan more tags. We experiment with 5 and 15 scanning locations. The number of tags covered in each scanning location is set from 5,000 to 15,000. The overlap between adjacent scans is randomly chosen, i.e., the value of is randomly generated in . The experiment results are shown in Fig. 13.

![](images/65d9500c4aee9137724c4b66f8458f099d6f49de1c09497b66f0ef2deac54610.jpg)



(@)

![](images/64baa0362d018720cc9127601aba7ec38dea94616a6c48c2dddc4dc968ce44ac.jpg)



(b)

![](images/2c396c53c31d572a23b474124c1adbfc4702deb724cbf25a0408a3da7de634ed.jpg)



Fig. 11. The impact of estimation error on scanning time. (a) . (b) . (c) .   
![](images/9e403464a8af27f0a7edd8d92b66c18c1d8c7cc6e0d69803276c3e4feaa480ed.jpg)



(a)

![](images/2cc73653e08c38245663308e4f6259835814fa365eeb9459ecd02a8ecafbce81.jpg)



(b)

![](images/9f8e89fd25785584ead50989a1f8d6078cc01acd084c0edd738c676deabdf0a3.jpg)



（C）

Fig. 12. The scanning time with different parameter settings. $| B | = 5 , 0 0 0 . c \in \{ 0 . 1 , 0 . 5 , 0 . 9 \}$ . Hence, . For each $c , | A |$ is varied from 3,500 to 5,000. (a) . (b) . (c) .   
![](images/21693bc5d85caa05d7e4eb208953714c087c2d2f3ab254006d3e4c514d9e5880.jpg)



![](images/5a77da2dbc6aeb29dbeed19f32978a682182a0f4dfbe7eb1a2cc21e3ca1291f1.jpg)



(b)   
Fig. 13. The scanning time of multiple consecutive scanning locations. In each setting, the number of tags in reader's coverage is varied from 5,000 to 15,000. (a) 5 locations. (b) 15 locations.

TABLE I PERCENTAGE OF ESTIMATION COST IN ACOS. 

<table><tr><td rowspan="2">c</td><td colspan="4">Number of tags</td></tr><tr><td>3,500</td><td>4,000</td><td>4,500</td><td>5,000</td></tr><tr><td>0.1</td><td>6.46%</td><td>5.5%</td><td>4.97%</td><td>4.5%</td></tr><tr><td>0.5</td><td>9.0%</td><td>7.77%</td><td>6.45%</td><td>5.74%</td></tr><tr><td>0.9</td><td>10.96%</td><td>9.12%</td><td>7.58%</td><td>6.45%</td></tr></table>

We find that in all experiment settings, ACOS is more time efficient than CU and ABS. This is because ACOS is not only an adaptive approach but also has a more efficient tag selection method compared with CU.

# VII. CONCLUSION

In this paper, we propose an Adaptive COntinuous Scanning scheme ACOS. In ACOS, we analytically unveil the fundamental relationship between the performance of continuous scanning and the tag set containment. In addition, lightweight estimation algorithms for tag set containment are designed to choose the scanning strategy. ACOS significantly outperforms the existing continuous scanning method in scanning time.

# ACKNOWLEDGMENT

The authors would like to thank the anonymous reviewers for their feedback.

# REFERENCES

[1] D. Sen, P. Sen, and A. M. Das, RFID for Energy and Utility Industries. Tulsa, OK, USA: Pennwell, 2009.   
[2] B. Sheng, Q. Li, and W. Mao, “Efficient continuous scanning in RFID systems,” in Proc. IEEE INFOCOM, 2010, pp. 1–9.   
[3] A. Z. Broder, M. Charikar, A. M. Frieze, and M. Mitzenmacher, “Minwise independent permutations,” in Proc. STOC, 1998, pp. 327–336.   
[4] S. Lee, S. Joo, and C. Lee, “An enhanced dynamic framed slotted ALOHA algorithm for RFID tag identification,” in Proc. MobiQuitous, 2005, pp. 166–172.   
[5] J. R. Cha and J. H. Kim, “Dynamic framed slotted ALOHA algorithms using fast tag estimation method for RFID system,” in Proc. IEEE CCNC, 2006, pp. 768–772.   
[6] J. Myung and W. Lee, “Adaptive splitting protocols for RFID tag collision arbitration,” in Proc. MobiHoc, 2006, pp. 202–213.   
[7] M. Shahzad and A. Liu, “Probabilistic optimal tree hopping for RFID identification,” IEEE/ACM Trans. Netw., vol. 23, no. 3, pp. 796–809, Jun. 2015.   
[8] X. Liu, B. Xiao, S. Zhang, and K. Bu, “Unknown tag identification in large RFID systems: An efficient and complete solution,” IEEE Trans. Parallel Distrib. Syst., vol. 26, no. 6, pp. 1775–1788, Jun. 2015.   
[9] X. Liu et al., “Efficient unknown tag identification protocols in largescale RFID systems,” IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 12, pp. 3145–3155, Dec. 2014.   
[10] L. Xie, Q. Li, X. Chen, S. Lu, and D. Chen, “Continuous scanning with mobile reader in RFID systems: An experimental study,” in Proc. MobiHoc, 2013, pp. 11–20.   
[11] T. Li, S. Chen, and Y. Ling, “Efficient protocols for identifying the missing tags in a large RFID system,” IEEE/ACM Trans. Netw., vol. 21, no. 6, pp. 1974–1987, Dec. 2013.   
[12] M. Chen, W. Luo, Z. Mo, S. Chen, and Y. Fang, “An efficient tag search protocol in large-scale RFID systems,” in Proc. IEEE IN-FOCOM, 2013, pp. 899–907.

[13] Y. Zheng and M. Li, “PET: Probabilistic estimating tree for large-scale RFID estimation,” IEEE Trans. Mobile Comput., vol. 11, no. 11, pp. 1763–1774, Nov. 2012.   
[14] M. Shahzad and A. Liu, “Every bit counts: Fast and scalable RFID estimation,” in Proc. Mobicom, 2012, pp. 365–376.   
[15] Z. Zhou, B. Chen, and H. Yu, “Understanding RFID counting protocols,” IEEE/ACM Trans. Netw., 2014, to be published.   
[16] W. Gong, K. Liu, X. Miao, and H. Liu, “Arbitrarily accurate approximation scheme for large-scale RFID cardinality estimation,” in Proc. IEEE INFOCOM, 2014, pp. 477–485.   
[17] “EPC radio-frequency identity protocols Class-1 Generation-2 UHF RFID Protocol for communications at 860 MHz-960 MHz,” 2008.   
[18] M. Buettner and D. Wetherall, “An empirical study of UHF RFID performance,” in Proc. MobiCom, 2008, pp. 223–234.   
[19] Impinj, “Understanding EPC Gen2 search modes and sessions,” [Online]. Available: https://support.impinj.com/hc/en-us/articles/ 202756158-Understanding-EPC-Gen2-Search-Modes-and-Sessions   
[20] “Jaccard index,” 2015 [Online]. Available: http://en.wikipedia.org/ wiki/Jaccard\_index   
[21] M. Mitzenmacher and E. Upfal, Probability and Computing: Randomized Algorithms and Probabilistic Analysis. Cambridge, U.K.: Cambridge Univ. Press, 2005.   
[22] B. H. Bloom, “Space/time trade-offs in hash coding with allowable errors,” Commun. ACM, vol. 13, no. 7, pp. 422–426, 1970.   
[23] “WISP platform,” 2012 [Online]. Available: http://wisp.wikispaces. com/WISPFirmware   
[24] “OpenBeacon,” [Online]. Available: http://www.openbeacon.org/   
[25] P. Indyk, “A small approximately min-wise independent family of hash functions,” in Proc. SODA, 1999, pp. 454–456.   
[26] Philips Semiconductors, “Philips I-CODE UID smart label IC functional specification,” 2004 [Online]. Available: http://www.nxp.com/ documents/data\_sheet/SL092030.pdf   
[27] H. Yue, C. Zhang, M. Pan, Y. Fang, and S. Chen, “Unknown-target information collection in sensor-enabled RFID systems,” IEEE/ACM Trans. Netw., vol. 22, no. 4, pp. 1164–1175, Aug. 2014.

![](images/1e7a194a89947fec347c0f146ff7ba56e428fc5ff7d4191bab93671964e16380.jpg)



Xin Miao received the B.S. degree from the Computer Science and Technology Department, Tsinghua University, Beijing, China, in 2005, and the Ph.D. degree in computer science and engineering from Hong Kong University of Science and Technology, Hong Kong, in 2013. His research interests include sensor networks and RFID.

![](images/3de21af49a30a7f9b5a9f3ea08a6b4734bf3bca983d6c86ed61e72e8095a20bd.jpg)



Kebin Liu received the B.S. degree from the Department of Computer Science, Tongji University, Shanghai, China, and the M.S. degree from Shanghai Jiaotong University, Shanghai, China. He is a joint Ph.D. student with the Department of Computer Science and Engineering, Shanghai Jiaotong University, and the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong. His research interests include sensor networks and distributed systems.

![](images/7a9b1406d3f7136978e87d30a932b0af1fc1db14c80addd7c73d47c8c8debcd6.jpg)



Wenbo He is currently an Assistant Professor with the School of Computer Science, McGill University, Montreal, QC, Canada. She received the Ph.D. degree from the University of Illinois at Urbana-Champaign, Urbana, IL, USA, in 2008. After that, she has been an Assistant Professor with the Computer Science Department, University of New Mexico, Albuquerque, NM, USA, from 2008 to 2010, and an Assistant Professor with the Electrical Engineering Department, University of Nebraska–Lincoln, Lincoln, NE, USA, from 2010 to 2011. Her research interests

include mobile and pervasive computing and network security.

![](images/555b852c2ad08ac6ba3021e3d6e4cfcbd1cd9d689a671e7c0060ac5d9d300d3b.jpg)



Wei Gong received the B.S. degree from the Department of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan, China, in 2003, and the M.S. and Ph.D. degrees from the School of Software and Department of Computer Science and Technology, Tsinghua University, Beijing, China, in 2007 and 2012, respectively. His research interests include wireless sensor networks, RFID applications, and mobile computing.

![](images/3a182db663b8e4affb6193e52079e5b95937e16facce773bad2144de39f6bbc9.jpg)



Lan Zhang received the Bachelor degree from the School of Software and the Ph.D. degree from the Department of Computer Science and Technology, Tsinghua University, Beijing, China, in 2007 and 2014, respectively. Her research interests span social networks, privacy, secure multi-party computation and mobile computing, etc.

![](images/47c8e66f974bd7fe304f845c87e5a75bfc3e57c2c4edeb72786dddcf533a8340.jpg)



Haoxiang Liu received the B.S. degree from the Department of Computer Science and Technology, Shanghai Jiao Tong University, Shanghai, China, in 2007. He is currently a Ph.D. candidate with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong. His research interests include RFID applications and mobile computing.

![](images/8e315071542e7a4c7f30e3a2a24cc20e15ce83a9258ccc383e2faf6098abff25.jpg)



Yunhao Liu received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, MI, USA, in 2003 and 2004, respectively. He is currently the Chang Jiang Professor with the School of Software and TNLIST, Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a Fellow of the IEEE and the ACM.