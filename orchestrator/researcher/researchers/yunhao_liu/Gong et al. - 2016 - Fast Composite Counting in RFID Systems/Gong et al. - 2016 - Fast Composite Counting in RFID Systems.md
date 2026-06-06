# Fast Composite Counting in RFID Systems

Wei Gong, Member, IEEE, Haoxiang Liu, Lei Chen, Member, IEEE, Kebin Liu, Member, IEEE, and Yunhao Liu, Fellow, IEEE

Abstract—Counting the number of tags is a fundamental issue and has a wide range of applications in RFID systems. Most existing protocols, however, only apply to the scenario where a single reader counts the number of tags covered by its radio, or at most the union of tags covered by multiple readers. They are unable to achieve more complex counting objectives, i.e., counting the number of tags in a composite set expression such as $( S _ { 1 } \bar { \bigcup } S _ { 2 } ) \ : - \ : ( S _ { 3 } \bigcap S _ { 4 } \breve { ) }$ . This type of counting has realistic significance as it provides more diversity than existing counting scenario, and can be applied in various applications. We formally introduce the RFID composite counting problem, which aims at counting the tags in an arbitrary set expression and obtain its strong lower bounds on the communication cost. We then propose a generic Composite Counting Framework (CCF) that provides estimates for any set expression with desired accuracy. The communication cost of CCF is proved to be within a small factor from the optimal. We build a prototype system for CCF using USRP software defined radio and Intel WISP computational tags. Also, extensive simulations are conducted to evaluate the performance of CCF. The experimental results show that CCF is generic, accurate and time-efficient.

Index Terms—Cardinality estimation, composite counting, RFID tags.

# I. INTRODUCTION

R ADIO Frequency Identification (RFID) is envisioned asa promising technology and sometimes a prerequisite for a promising technology and sometimes a prerequisite for the Internet of Things (IOT) [1]. Every object in the physical world can be equipped with an RFID tag that bears a unique ID. An RFID reader is adopted to identify the tags using wireless communication. Due to the small size and ultra-low power of tags, RFID holds immense potential in applications such as localization, supply chain management and object tracking.

Counting the number of RFID tags, and thus the number of corresponding objects, is a fundamental issue in RFID

Manuscript received October 02, 2014; revised March 24, 2015; July 13, 2015; and September 01, 2015; accepted September 15, 2015; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor S. Chen. This work was supported in part by the NSFC under Grants No. 61303196 and No. 61103187 and the NSFC Distinguished Young Scholars Program under Grant No. 61125202. The work of L. Chen was supported in part by the Hong Kong RGC Project NHKUST637/13, the National Grand Fundamental Research 973 Program of China under Grant 2014CB340303, the NSFC under Grant No. 61328202, and NSFC Guang Dong under Grant No. U1301253.

W. Gong is with the School of Computing Science, Simon Fraser University, Burnaby, BC V5A 1S6, Canada (e-mail: gongweig@sfu.ca).

H. Liu and L. Chen are with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong (e-mail: hliuab@cse.ust.hk; leichen@cse.ust.hk).

K. Liu and Y. Liu are with the School of Software, Tsinghua National Lab for Information Science and Technology, Tsinghua University, Beijing 100084, China (e-mail: kebin@greenorbs.com; yunhao@greenorbs.com).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TNET.2015.2483681

systems [2]. Motivated by its importance, a number of counting schemes have been proposed to address this problem [2]–[8]. Most existing schemes only work in the simple scenario in which a single reader counts the number of tags in its covered area. We call this counting scenario simple counting. This simple scenario, however, fails to meet practical and complex application demands. The reasons are three-fold. First, multiple readers can be deployed in practical RFID systems, since a single reader has limited coverage area. Thus, tags to count may be covered by different readers instead of a single one. Second, tags may be mobile rather than static. Consequently, readers read different tags at different times. Third, the counting objective can be various, depending on specific applications. More precisely, the target tags may be obtained via different kinds of tag set operations. Consider the following examples:

• Warehouse management. One primary target of warehouse management is to obtain the total amount of goods (tags) in the large warehouse. It is clearly infeasible to use one static reader to count the tags, since the typical communication distance between a reader and passive tags is limited to 12 meters [9]. Therefore, the counting operation should be conducted at different locations to cover the entire warehouse. Then the union of the covered tags at these locations constitutes the target tag set. Note that duplicate counting should be avoided due to coverage overlap among the readers.

• Conference statistics. In a conference, each conference room is equipped with an RFID reader. The organizers distribute RFID wristbands to participants in order to enable real-time people tracking. Some useful conference statistics can be obtained over time, such as the number of participants that visit both conference room and during the same period $[ t _ { 1 } , t _ { 2 } ]$ . In this case, the readers in room and have to collaboratively count the intersection of their reading results, i.e., $| A ( t _ { 1 } , t _ { 2 } ) \cap B ( t _ { 1 } , t _ { 2 } ) |$ .

All above examples require counting the cardinality of a set expression rather than a single set, which are dramatically different from the simple counting problem. The set expressions involve set operators including union, intersection and difference. More generally, the expression can be extended to any combination of the set operations, depending on the application demands. For example, let $S _ { i }$ be the set of participants who have visited the $i ^ { t h }$ conference room during a time period in the aforementioned example 2. By counting $| ( \bar { S } _ { 1 } \bigcup S _ { 2 } ) - ( S _ { 3 } \bigcap S _ { 4 } ) |$ , we manage to derive the number of people visiting room 1 or 2, but not both 3 and 4, as illustrated in Fig. 1. Note that we focus on the applications where multiple readers work in parallel and all sets in the expression correspond to the same time interval. The scenarios where different sets are over different time intervals are temporarily beyond our discussion in this work, e.g., a reader encounters different tag sets sequentially. In light of the composite set expression embodied in this type of RFID counting, we call it composite counting in contrast to simple counting. Often in many applications, it is desirable to just estimate the number of tags rather than explicitly identifying each tag, since exact result is often unnecessary and the overhead of exact counting/identification is prohibitively high for large quantities of tags. The words counting and estimation will be used interchangeably throughout this paper.

![](images/2dd35006f685723e822641a3f5d97e6fe0b8da04a3a70444cec38b082ee00aab.jpg)



Fig. 1. A composite counting example. A reader is located in each conference room, and all readers work in parallel. People wearing RFID tags will be identified by the reader once they enter the room. Let $\breve { S } _ { i }$ be the tag set read by the reader in room in some fixed time interval, and $| E | = { \big | } { \big | } ( S _ { 1 } \bigcup S _ { 2 } ) { \big . } { \dot { - } }$ $( S _ { 3 } \cap S _ { 4 } )$ . Then participants $a , c \in E$ and $b \notin E$ . Thus, the counting result is $| E | = 2$ in this example.

Unfortunately, composite counting cannot be trivially solved by simple counting techniques due to the following reasons. First, most simple counting techniques give an estimate for the number of tags rather than deterministic identification, as justified before. As a result, tag IDs in each set are unknown in simple counting, and thus we cannot solve composite counting by direct set operations. Notice that we still use estimation for composite counting in this paper for sake of efficiency and scalability. Second, we cannot simply mimic operators like union and difference with addition and subtraction. For example, it is obviously incorrect to approximate $| S _ { 1 } \cup S _ { 2 } |$ with $| S _ { 1 } | + | S _ { 2 } |$ , or approximate $| S _ { 1 } - S _ { 2 } |$ with $| | S _ { 1 } | - | \bar { S } _ { 2 } | |$ .

This paper offers a comprehensive study of the composite counting problem that is useful in a variety of RFID applications. First, we establish strong lower bounds on the communication cost for any composite counting method, by leveraging communication complexity theory. The lower bounds help us to benchmark the performance of our counting protocol. We then propose a generic Composite Counting Framework (CCF) that can estimate the cardinality of arbitrary set expression with desired accuracy. CCF exploits a small synopsis (a sample) for each tag set to estimate, whose size is sublinear w.r.t the set cardinality. Furthermore, we design a protocol to efficiently construct the synopsis from tag sets. We demonstrate that the communication cost of our protocol is within a small logarithm factor from the lower bounds. We implement a prototype system of CCF using USRP software radios [10] and Intel WISP computational tags [11], which only requires a slight modification to the EPCGlobal Class-1 Generation-2 (C1G2) standard [12]. Finally, we extensively evaluate the performance of CCF using both real-world datasets and large-scale simulations.

The rest of this paper is organized as follows. In Section II, we review the related work. In Section III, we formulate the composite counting problem. We present the lower bounds in Section IV and the design of CCF in Section V. We show the prototype implementation in Section VI and conduct the simulations in Section VII. We discuss some relevant issues in Section VIII. Finally, we conclude the paper in Section IX.

# II. RELATED WORK

There has been a stream of RFID counting protocols under the simple counting model. Kodialam et al. propose Unified Probabilistic Estimator (UPE) [2]. In UPE, each tag participates in the slots with a carefully chosen probability , and the estimation is made using the number of empty and collision slots. Qian et al. [4] propose Lottery Frame (LoF) Estimator, in which tags choose slot according to geometric distributed random numbers, making the number of slots $O ( \log n )$ . In [6], an estimation scheme Average Run based Tag estimator (ART) is designed. The authors attribute its efficiency to the non-trivial estimation metric it utilizes, i.e., the average run size of nonempty slots. Then, Zheng et al. [7] use a two-phase scheme Zero-One Estimator (ZOE) that achieves high efficiency. Recently, Chen et al. [8] gain deeper and fundamental insights into the counting problem and claim the importance of two-phase methodology in protocol design. While some of the previous techniques [4], [8] can be extended to estimate the set union cardinality, they are not applicable to set intersection and difference. While one-time set difference and set intersection solutions are proposed in [13], it is unable to process arbitrary set expression.

There is also some similarity between the RFID composite counting problem in this paper and counting distinct elements among multiple sets in data stream research[14]. We can view each RFID tag as an element in the data stream. But there are some fundamental differences between the two problems. First, the communication model is different. Specifically, in the data stream model, we can handle each element arrived in the stream directly whereas in RFID the reader has to communicate with tags in time-slotted model. In other words, the reader cannot fetch a value associated with any tag straightforwardly. Second, each element in the data stream can only be accessed a small number of times, while the reader can communicate with tags multiple rounds, depending on specific demands.

Besides probabilistic counting, many anti-collision based identification schemes have been designed to improve the efficiency of identifying tag IDs. Although tag identification can can derive the exact number of tags once tag IDs are collected, the efficiency is unacceptable for large-scale systems counting requirements.

# III. PROBLEM FORMULATION

In this section, we formulate RFID composite counting problem. We consider multiple tag sets $S _ { 1 } , S _ { 2 } , \ldots , S _ { m }$ $( m > 1 )$ . Each set contains a number of unknown tags to be interrogated by some reader(s) at a certain location and time. Either location or time can be different among the sets to consider spatial and temporal diversity. Given an application specific set expression over sets $\{ S _ { i } | 1 ~ \le ~ i ~ \le ~ m \}$ and operator set $O ^ { - } = \{ \cup , \cap , - \}$ as follows,

$$
E = S _ {1} \text {   op   } S _ {2} \text {   op   } S _ {3} \dots \text {   op   } S _ {m} (\text {   op   } \in O) \tag {1}
$$

the objective of composite counting is to estimate the cardinality . For example, $\begin{array} { r } { | \dot { E | } = | ( S _ { 1 } \bigcup S _ { 2 } ) - ( S _ { 3 } \bigcap S _ { 4 } ) } \end{array}$ . To derive in RFID systems efficiently is nontrivial. We can easily calculate exactly by identifying each tag in $S _ { i } ( 1 \leq i \leq m )$ . This exact solution requires $\textstyle { \bar { O ( } } \sum _ { i = 1 } ^ { m } | { \bar { S _ { i } } } | )$ communication cost that is very time-consuming for large-scale systems. Besides, exact solution is often not required in practice. Hence, we resort to estimation for , which is more time-efficient. We also make some assumptions. We assume a back-end server with powerful processing capability, which is connected to the readers via high speed networks. The server is responsible for estimating with the data reported by the readers.

We adopt the typical slotted ALOHA model for RFID communication [15]. Time period is divided into a sequence of slots. In each slot, the reader initializes communication by broadcasting commands and associated parameters. Then tags that participate in the slot respond their messages synchronously. Since the tags are incapable of sensing each other, they decide whether to participate depending on their local states, e.g., the received commands and stored information. The reader and tags simply exchange bits in one slot, as the tags are synchronized and their replies can be treated as a whole. A slot can fall into two categories according to the wireless channel state. If there is at least one tag responding, the corresponding slot is called non-empty slot. Otherwise the slot is empty.

Similar to previous probabilistic estimation schemes [2]–[8], the accuracy of composite counting is described by $( \varepsilon , \delta ) \mathopen { } \mathclose \bgroup  \partial \aftergroup \egroup  \mathopen { } \mathclose \bgroup ( \varepsilon , \delta \aftergroup \egroup ) \mathopen { } \mathclose \bgroup  - \mathrm { a p - }$ proximation. Let $n = | E |$ and the estimate of be . We say that is an -estimate for if $P r ( | \hat { n } - n | \leq \varepsilon n ) \geq 1 - \delta$ . For example, when , a -approximation of outputs a number in the range of [900, 1100] with probability at least 0.95.

# IV. COMPOSITE COUNTING LOWER BOUNDS

Before introducing the detailed composite counting framework, we derive communication cost lower bounds for composite counting to set benchmark for the performance of our proposed framework. The lower bound decides the minimum communication cost required to solve the composite counting problem. To measure the communication cost, we follow the conventional definition of communication complexity [16], which quantifies the amount of bits exchanged between two parties to collaboratively compute a function, e.g., counting the size of an expression. We will provide the lower bounds for counting union, intersection and difference between two sets, since they are basic components of composite counting.

1) Lower Bound for Set Union Counting: We aim at counting the union of two tag sets $S _ { 1 }$ and $S _ { 2 }$ , which we call RFID set Union Counting problem $( R U C )$ . We use reduction to derive the complexity lower bound for $R U C$ . Reduction is a commonly used approach to obtain the complexity of a problem. Specifically, if we wish to obtain the complexity of a hard problem , we usually resort to another hard problem . We say can be reduced to if a protocol to solve could also be adopted as a building block to solve . Consequently, problem is no harder than , and thus the complexity of is a lower bound of .

![](images/a60d8a3b5e48e91846c19b9f44c9471c1176b87c4ce0b9c54a52856c1eed913a.jpg)



Fig. 2. The communication models of , and . (a) Model of . (b) Model of . (c) Model of .

Here we choose a Two-party set Union Counting ( ) problem between Alice and Bob as problem . The definition of $T U C$ is given in the following. We show that $R U C$ can be reduced to .

TUC: Alice and Bob each knows a set $S _ { 1 } \subseteq [ n ]$ and $S _ { 2 } \subseteq$ , and they want to estimate $| S _ { 1 } \cup S _ { 2 } |$ by exchanging as few bits as possible, as shown in Fig. 2(c).

Note that the models of and are different in two aspects, which hinders direct reduction. First, has only two communication parties Alice and Bob. However, in $R U C$ , we have more parties, namely the tags in $S _ { 1 }$ and $S _ { 2 }$ , their associated readers and the back-end server. To simplify $R U C _ { \mathrm { { : } } }$ we treat the back-end server as a virtual reader to directly communicate with tags in $S _ { 1 }$ and $S _ { 2 }$ , as shown in Fig. 2(a). Second, in $T U C$ Alice and Bob know $S _ { 1 }$ and $S _ { 2 }$ , whereas in $R U C$ tags in $S _ { 1 }$ and $S _ { 2 }$ are distributed and their IDs are unknown. Given these discrepancies, we introduce an intermediate problems to bridge the gap as follows. The reduction sequence is $R U C \to I \to { \overline { { T U C } } }$ .

I: is a three-party communication problem. Alice and Bob each knows a set $S _ { 1 } \subseteq [ n ]$ and $S _ { \mathbf { 2 } } ~ \subseteq ~ [ n ]$ . The third party Carol aims to estimate $| S _ { 1 } \cup S _ { 2 } |$ by communicating with Alice and Bob, as shown in Fig. 2(b).

Without loss of generality, we can set $n ~ = ~ \left| S _ { 1 } \bigcup S _ { 2 } \right|$ in and so that they have the same problem input format with . The following Lemma 1 gives the reduction from $R U C \to I \to T U C$ .

Lemma 1: The communication complexity of is bounded by below.

Based on the reduction in Lemma 1 and an existing lower bound for , Theorem 1 gives a communication complexity lower bound for . The proofs of all lemmas and theorems in this paper are included in the Appendix.

Theorem 1: Given user-specified constant $\begin{array} { r } { \varepsilon = \Omega \left( \frac { 1 } { \sqrt { | S _ { 1 } | \bigcup S _ { 2 } | } } \right) } \end{array}$ , any randomized protocol for with relative error must use $\textstyle \Omega ( { \frac { 1 } { \varepsilon ^ { 2 } } } )$ bits.

2) Lower Bound for Set Intersection Counting: We aim to count the intersection of tag sets $S _ { 1 }$ and $S _ { 2 }$ , denoted as RFID set Intersection Counting problem $( R I C )$ . We assume tag IDs are subsets of $[ n ]$ as before. Again, reduction is used to derive the communication lower bound for $R I C$ . The problem here we choose is a Two-party set Intersection Counting problem , which is defined as follows.

TIC: Alice and Bob have $S _ { 1 } \subseteq [ n ]$ and $S _ { 2 } \subseteq [ n ]$ , respectively. They want to estimate $| S _ { 1 } \cap S _ { 2 } |$ by exchanging as few bits as possible.

and have different communication models. Namely, has the model in Fig. 2(a), while has the model in Fig. 2(c). So we use the same method aforementioned to perform the reduction. Again we may set $n = | S _ { 1 } \bigcup S _ { 2 } |$ in as well. The following lemma compares the complexity of to .

Lemma 2: The communication complexity of is bounded by below.

Then we obtain Theorem 2 based on Lemma 2 and an existing lower bound for [14].

Theorem 2: Given user-specified constant , any randomized protocol for with relative error must use $\Omega \left( { \frac { | S _ { 1 } \bigcup S _ { 2 } | } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } } \right)$ bits.

There are several points worth noting. First, we assume as a constant here because it is specified before each estimation. This assumption agrees with most existing single-set RFID counting schemes, such as ART [6], ZOE [7], SRC [8]. Accordingly, the lower bound in above theorem does scale with changing in different user settings. But for some schemes that do concern the range of $\varepsilon ,$ the direct comparison with our lower bound is not applicable. For example, UPE [2] is a biased RFID counting scheme and may fail when is small [8]. Second, randomized protocols in above theorem do not always perform better than naive RFID identification. Therefore we examine the relationship between them and find a critical threshold as in the following lemma.

Lemma 3: Given user-specified constant $\begin{array} { r } { \varepsilon = \Omega \left( \frac { 1 } { | S _ { 1 } \bigcap S _ { 2 } | } \right) } \end{array}$ ， both randomized protocols with relative error and naive identification for must use $\Omega \left( { \frac { | S _ { 1 } \bigcup S _ { 2 } | } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } } \right)$ bits.

It is worth noting that when $\varepsilon ~ > ~ { \frac { 1 } { \left| S _ { 1 } \bigcap S _ { 2 } \right| } }$ , probably naive 1 identification approaches would be more efficient. But it depends on the additional overhead that specific naive approach might bring, such as Aloha anti-collision.

3) Lower Bound for Set Difference Counting: The difference of two sets $S _ { 1 } - S _ { 2 }$ is simply $S _ { 1 } \cap \bar { S } _ { 2 }$ . Hence, we can apply all the results of set intersection counting, except that the operator is replaced with . Denote the RFID set Difference Counting problem as , and we have Theorem 3.

Theorem 3: Given user-specified constant , any randomized protocol for with relative error must use $\Omega \left( { \frac { | S _ { 1 } \bigcup S _ { 2 } | } { | S _ { 1 } - S _ { 2 } | \varepsilon } } \right)$ bits.

# V. COMPOSITE COUNTING FRAMEWORK

In this section, we present the main design of our composite counting framework. We show by leveraging set synopsis, we can accurately estimate the cardinality of union, intersection, difference and more generally, any composite set expression. A summary of notations are summarized in Table I.

# A. Synopsis-Based Estimator

1) What is Synopsis: A synopsis for a tag set is virtually a small set of random samples drawn from it. The sampling technique can be diverse. For synopsis in this paper, we use

TABLE I TABLE OF NOTATIONS 

<table><tr><td>Notation</td><td>Meaning</td></tr><tr><td> $h(S)$ </td><td>hash set of  $S$  (normalized)</td></tr><tr><td> $h_{(k)}$ </td><td>the  $k^{th}$  smallest value in  $h(S)$ </td></tr><tr><td> $T_S$ </td><td>synopsis of  $S$ </td></tr><tr><td> $k$ </td><td>synopsis size</td></tr><tr><td> $n_{\bigcup}$ </td><td> $|S_1 \cup S_2|$ </td></tr><tr><td> $n_{\bigcap}$ </td><td> $|S_1 \cap S_2|$ </td></tr><tr><td> $n_{-}$ </td><td> $|S_1 - S_2|$ </td></tr><tr><td> $n_E$ </td><td>size of general set expression  $E$ </td></tr><tr><td> $J = \frac{n_{\bigcap}}{n_{\bigcup}}$ </td><td>Jaccard similarity between two sets</td></tr></table>

hash functions to draw random samples. Moreover, although a synopsis is significantly small in size compared to the original set, it can preserve many properties in set computation, e.g., union and intersection, if carefully designed. In other words, a well-designed synopsis scheme is able to let user operate on synopses the same as over original sets. For example, suppose we have two set $S _ { 1 } ~ = ~ \bar { \{ 1 , 2 , 4 , 5 , 7 , 8 , 9 , 1 0 \} }$ and $S _ { 2 } = \{ 2 , 3 , 5 , 7 , 8 , 1 0 , 1 3 , 1 5 , 1 8 \}$ . Then we have two synopses $s _ { 1 } ~ = ~ \{ 9 , 1 0 \}$ and $s _ { 2 } ~ = ~ \{ 1 5 , 1 8 \}$ which keep two maximum elements from $S _ { 1 }$ and $S _ { 2 } .$ . Now if we need to know two maximum elements of $S _ { 1 } \cup S _ { 2 } ,$ , which is , we could get exactly the same result by computing two maximum elements of $s _ { 1 } \cup s _ { 2 }$ .

2) Why Synopsis: There are several reasons why we use synopsis to estimate. First, the communication cost of using original tag sets can be prohibitively high for large sets. The synopsis, however, has a much smaller size than the original tag set, which makes the estimation much more efficient. Second, synopsis effectively achieves composite counting despite its small size, which allows us to build a truly generic framework. At last, synopsis can be maintained and updated in real time, ensuring the flexibility of the framework.

3) Single Set Estimation: We start illustrating the estimation method from single set perspective. Consider a set with tags $\{ I D _ { 1 } , I D _ { 2 } , \ldots , I \bar { D _ { n } } \}$ . The aim is to estimate the number of tags . The basic intuition is as follows. Assume that tag IDs in are uniformly distributed in an interval . Let $S _ { ( k ) }$ be the $k ^ { t h }$ smallest tag ID in . Due to the uniformity, expected value of to inversely ded $\textstyle S _ { ( k ) } { \mathrm { ~ i s ~ } } l + { \frac { u - l } { n } } k$ . Hence, we can utilizec, can be estimated $S _ { ( k ) }$ a s . In most cases, we do not have such distribution $\frac { ( u - l ) k } { S _ { ( k ) } - l }$ properties. Hash functions, however, can bridge the gap and transform the tag IDs with any distribution to uniform distribution. In particular, each tag in $S$ can compute a hash value $h ( I D )$ using a uniform hash function $h : { \bar { S } }  [ D ]$ and its ID, where is the hash size. After normalization, the values $h ( I D _ { 1 } ) / D , h ( I D _ { 2 } ) / D , \dots , h ( I D _ { n } ) / D$ can be approximately viewed as uniformly distributed in . In order to avoid hash collisions, the hash space should be ${ \dot { O } } ( n ^ { 2 } )$ (Derived from well-known Birthday Paradox). With $D \ = \ \dot { O } ( n ^ { 2 } )$ , we can ensure that for any $I D _ { i }$ and $I D _ { j } ~ ( i \ne j ) , h ( I D _ { i } ) \ne h ( I D _ { j } )$ with large probability. In the rest of this paper, we always use a sufficiently large hash size and do not consider hash collisions. Let the $k ^ { t h }$ smallest normalized hash value be $h _ { ( k ) }$ . The set cardinality can be unbiasedly estimated as $\begin{array} { r } { \hat { n } = \frac { k ^ { \underline { { \cdot } } } - 1 } { h _ { ( k ) } } , } \end{array}$ h（）， according to the previous analysis. For example, if the $\ddot { 4 } ^ { t h }$ smallest normalized hash value $h _ { ( 4 ) }$ is 0.3, then there are approximately $\frac { 3 } { 0 . 3 } = 1 0$ tags in the set.

To achieve $( \varepsilon , \delta )$ -approximation of $n ,$ the value of should be determined accordingly. We have the following lemma that decides .

Lemma 4: To achieve -estimate for $\begin{array} { r } { n , k = \Theta ( \frac { 1 } { \varepsilon ^ { 2 } } l n \frac { 1 } { \delta } ) } \end{array}$ .

4) Set Union Estimation: The estimation techniques proposed above can be naturally applied to estimate the union of two tag sets. For set $S _ { i } ~ ( i { \mathrm { ~ = ~ } } 1 , 2 )$ , let $T _ { S _ { i } }$ be the smallest hash values in $h ( S _ { i } ) . T _ { S _ { i } }$ is defined as the synopsis of $S _ { i }$ , and its size is usually smaller than $| S _ { i } | . T _ { S } $ and $T _ { S _ { 2 } }$ are obtained using the same hash function. According to the single set estimation technique, if we can obtain the $\bar { k ^ { t h } }$ smallest hash value in $h ( S _ { 1 } ) \bigcup h ( \bar { S } _ { 2 } )$ , estimate for $^ n \cup$ is easily achieved. In fact, the $k ^ { t h }$ smallest hash value in $h ( \breve { S } _ { 1 } ) \bigcup h ( S _ { 2 } )$ is essentially the largest element in $T _ { S _ { 1 } \mid \mid S _ { 2 } }$ . Nevertheless, $T _ { S _ { 1 } \backslash { \vert { \cal { S } } _ { 2 } } }$ is unknown and we can only compute $T _ { S _ { i } }$ directly. Lemma 5 describes how to build the $T _ { S _ { 1 } \mid \mid S _ { 2 } }$ from $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ .

Lemma 5: The smallest values in $T _ { S _ { 1 } } \bigcup T _ { S _ { 2 } }$ comprise the synopsis of $S _ { 1 } \cup S _ { 2 }$ , i.e., $T _ { ( S _ { 1 } \mid { \cal { S } } _ { 2 } ) } .$ .

By Lemma 5, we can use $h _ { ( k _ { \parallel } | ) } ^ { \cup } = \operatorname* { m a x } \{ T _ { ( S _ { 1 } \bigcup S _ { 2 } ) } \}$ to estimate $^ n \lfloor \rfloor$ , as in the single set scenario. Hence, we have the following estimator

$$
\hat {n} _ {\bigcup} = \frac {k - 1}{h _ {(k _ {\bigcup})}}. \tag {2}
$$

This method can be illustrated by a simple example. Assume $\begin{array} { r c l c l } { k } & { = } & { 4 , \ T _ { ( S _ { 1 } ) } } & { = } & { \{ 0 . 0 1 , 0 . 0 3 , 0 . 0 5 , 0 . 0 7 \} } \end{array}$ and $\begin{array} { r l r } { T _ { ( S _ { 2 } ) } } & { { } = } & { \{ 0 . 0 3 , 0 . { \dot { 0 } } { \dot { 4 } } , 0 . 0 7 , 0 . 0 8 \} } \end{array}$ . Then $\begin{array} { r l } { T _ { ( S _ { 1 } \bigcup \ S _ { 2 } ) } } & { { } = } \end{array}$ $\{ 0 . 0 1 , 0 . 0 3 , 0 . 0 4 , 0 . 0 5 \}$ and $h _ { ( k _ { \parallel } _ { \parallel } ) } = 0 . 0 5$ . Hence, $\mathsf { \bar { \Pi } } _ { | S _ { 1 } \bigcup S _ { 2 } | }$ can be estimated as $3 / 0 . 0 5 = 6 \widetilde { 0 }$ .

According to Lemma 4, we obtain Theorem 4 that gives the size of synopsis for $( \varepsilon , \delta )$ -estimate.

Theorem 4: To achieve -estimate for , $4 ; \quad { \mathrm { ~ } } T o$ $^ { f o r } \quad n _ { \bigcup } ,$ $\begin{array} { r } { k = \Theta \big ( \frac { 1 } { \varepsilon ^ { 2 } } l n \frac { 1 } { \delta } \big ) } \end{array}$ .

5) Set Intersection Estimation: Consider two tag sets $S _ { 1 }$ and $S _ { 2 }$ and their synopsis $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ . The objective is to estimate $^ n \cap$ based on $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ . We represent $^ n \cap$ by the product of two terms , where $J = \frac { \mathop { n } ^ { \prime } \bigcap } { \mathop { n } _ { | ~ | } }$ n is called the Jaccard ${ } ^ { n } \bigcap { } = n _ { \bigcup } J { } _ { \mathrm { : } }$ similarity between $S _ { 1 }$ and $S _ { 2 }$ . Thus, $\bar { } \bar { } \bar { } \bar { } \bar { } \bar { } \bar { } \bar { } \bar { } \bar { } \bar { }$ can be estimated as follows.

$$
\hat {n} _ {\bigcap} = \hat {n} _ {\bigcup} \hat {J}. \tag {3}
$$

According to (3), estimation for $^ n \cap$ can be divided into separate estimation for and $^ n \mathrm { U }$ . In fact, if we have $( \varepsilon / 3 , \delta )$ -estimate for both and $^ n \cup$ , we can obtain $( \varepsilon , \delta )$ -estimate for $^ n \cap$ . The reason is given in $\top ( 4 ) - ( 5 )$ , where (5) shows that ${ \hat { \boldsymbol { n } } } _ { \bigcap }$ is an $( { \dot { \varepsilon } } ) \mathbf { - e s - }$ timate for . $^ n \cap$

$$
(1 - \varepsilon / 3) ^ {2} n _ {\bigcup} J \leq \hat {n} _ {\bigcup} \hat {J} \leq (1 + \varepsilon / 3) ^ {2} n _ {\bigcup} J \tag {4}
$$

$$
\begin{array}{l} (1 - \varepsilon) n _ {\bigcap} = (1 - \varepsilon) n _ {\bigcup} J \leq \hat {n} _ {\bigcap} = \leq (1 + \varepsilon) n _ {\bigcup} J \\ = (1 + \varepsilon) n _ {\bigcap}. \tag {5} \\ \end{array}
$$

![](images/98061b5916a44d2d5b42aee777431bf54ac7ed5e5968ab5054a048f0484848d8.jpg)  
Fig. 3. A motivating example of sampling-based estimation. is a subset of . $A _ { s }$ is a simple random sample drawn from . $\frac { \mid B \bigcap A _ { s } \mid } { \mid A _ { s } \mid }$ can be used to estimate the ratio $\frac { \mid B \mid } { \mid A \mid }$

The method to estimate $^ n \cup$ with $( \varepsilon / 3 , \delta )$ -accuracy has been explained earlier. Now we show how to give $( \varepsilon / 3 , \delta )$ -estimate for the similarity using $T _ { S }$ and $T _ { S _ { 2 } }$ . The key idea is based on random sampling. Consider a motivating example in Fig. 3, where we have set and its subset $B \subset A$ , and wish to estimate the ratio $\frac { | \rrangle | } { | A | }$ . If we draw a simple random sample1 $A _ { s }$ from , then $\frac { | B \bigcap { \dot { A } } _ { s } | } { \left| A _ { s } \right| }$ can be used to approximate the ratio $\frac { | B | } { | A | }$ This technique can be used to estimate . Clearly, ${ \cal J } = \widehat { \frac { \Pi } { \scriptstyle { \cal J } \displaystyle _ { \scriptstyle \bigcup } } } =$ nU ${ \frac { h ( S _ { 1 } ) \bigcap h ( S _ { 2 } ) } { h ( S _ { 1 } ) \bigcup h ( S _ { 2 } ) } } . h ( S _ { 1 } ) \bigcup h ( S _ { 2 } )$ and $h ( S _ { 1 } ) \bigcap h ( S _ { 2 } )$ correspond to and in the example respectively. Note that $T _ { S _ { 1 } \backslash { \vert { \cal { S } } _ { 2 } } }$ is virtually a simple random sample drawn from $h ( S _ { 1 } ) \bigcup { \overline { { h } } } ( S _ { 2 } )$ , and therefore corresponds to $A _ { s }$ . Therefore, we substitute and $A _ { s }$ in $\frac { | B \bigcap A _ { s } | } { \left| A _ { s } \right| }$ |As| with $h ( S _ { 1 } ) \bigcap h ( S _ { 2 } )$ and $T _ { S _ { 1 } \bigcup S _ { 2 } }$ respectively and derive the following estimator for

$$
\hat {J} = \frac {\left| T _ {S _ {1}} \bigcup_ {S _ {2}} \bigcap h (S _ {1}) \bigcap h (S _ {2}) \right|}{\left| T _ {S _ {1}} \bigcup_ {S _ {2}} \right|}. \tag {6}
$$

Note that for any hash value in $T _ { S _ { 1 } \backslash { \vert { \cal { I } } \vert { \cal { S } } _ { 2 } } }$ , if it is in $h ( S _ { i } ) ( i = 1$ , 2), it must also belong to $T _ { S _ { i } }$ and vice versa. Hence, the hash set $h ( S _ { i } ) \ ( i = 1 , 2 )$ in Equation can be replaced with the synopsis $T _ { S _ { i } }$ , which leads to (7) below.

$$
\hat {J} = \frac {\left| T _ {S _ {1}} \bigcup_ {S _ {2}} \cap T _ {S _ {1}} \cap T _ {S _ {2}} \right|}{k}. \tag {7}
$$

According to [17], we know this $\hat { J }$ is an unbiased estimator and its variance is $\mathcal { O } ( 1 / k )$ . Thus, for any user-specified constant $\varepsilon >$ , there is a constant $\dot { k } = \mathcal { O } ( 1 / \varepsilon ^ { 2 } )$ such that the error of estimate $\hat { J }$ is no more than . For instance, if we choose $k = 1 0 0$ , the expected error of should be less than or equal to 0.1.

Substituting (2) and (7) to (3), we have the estimate for $n _ { \cap }$

$$
\hat {n} \bigcap = \frac {\left| T _ {S _ {1}} \bigcup_ {S _ {2}} \bigcap T _ {S _ {1}} \bigcap T _ {S _ {2}} \right|}{k} \frac {k - 1}{h _ {(k)} \bigcup}. \tag {8}
$$

Now we decide the synopsis size that ensures $( \varepsilon , \delta )$ -approximation of $^ n \cap$ , and get the following theorem.

Theorem 5: To achieve $( \varepsilon , \delta )$ -estimate for $n _ { \bigcap } , k$ is at least $\begin{array} { r } { \Theta \big ( \frac { 1 } { \varepsilon ^ { 2 } . I } l n \frac { 1 } { \delta } \big ) } \end{array}$ .

6) Set Difference Estimation: This time, we wish to estimate $n _ { - }$ with $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ . Estimating difference is essentially similar to estimating intersection, since $S _ { 1 } - S _ { 2 } = S _ { 1 } \cap \bar { S } _ { 2 }$ . Therefore, we just apply the results in the last section without further elaboration. The estimator $\hat { n } _ { - }$ for $n _ { - }$ is

$$
\hat {n} _ {-} = \frac {\left| T _ {S _ {1}} \bigcup_ {S _ {2}} \bigcap (T _ {S _ {1}} - T _ {S _ {2}}) \right|}{k} \frac {k - 1}{h _ {(k)} \bigcup}. \tag {9}
$$

1A simple random sample is a subset of individuals (a sample) chosen from a larger set (a population).

Theorem 6 decides the synopsis size that ensures $( \varepsilon , \delta ) { \mathfrak { - a p } } \cdot$ proximation of $n _ { - }$ . It directly follows from Theorem 5.

Theorem 6: To achieve $( \varepsilon , \delta )$ -estimate for $n _ { - } ,$ , is at least $\begin{array} { r } { \Theta \big ( \frac { 1 } { \varepsilon ^ { 2 } C } l n \frac { 1 } { \delta } \big ) } \end{array}$ , where $\begin{array} { r } { C = \frac { n _ { - } } { n _ { \bigstar } } } \end{array}$

7) General Expression Estimation: We now consider $\mathrm { e s - }$ timating the cardinality of general set expression $E .$ . Assume $E$ contains sets $S _ { 1 } , \bar { S } _ { 2 } , \bar { \dots } , S _ { m }$ . We then express $| E |$ as a product of two terms $\textstyle \frac { | \boldsymbol { E } | } { | \bigcup _ { i = 1 } ^ { m } S _ { i } | } | \bigcup _ { i = 1 } ^ { m } S _ { i } | . \operatorname { | } \bigcup _ { i = 1 } ^ { m } \boldsymbol { \dot { S } } _ { i } |$ can be estimated using its synopsis $^ { \top } \bigcup { \cal S } _ { i } :$ , which is a trivial extension of estimating the union of two sets. In specific, it can be estimated as $\frac { k - 1 } { h _ { ( k } }  \\  ) ^ { ) }$ where $h _ { ( k _ { \bigcup } ) } = \operatorname* { m a x } \{ T _ { \bigcup { S _ { i } } } \}$ , which is similar to (2).

Estimating the ratio $\begin{array} { r } { R = \frac { | E | } { | \bigsqcup _ { i = 1 } ^ { m } S _ { i } | } } \end{array}$ is an extension of estimating $J$ and $C .$ . Denote $E _ { T }$ as the set with each $S _ { i }$ in replaced with its synopsis $T _ { S _ { i } }$ . For example, if $E = ( S _ { 1 } \bigcup S _ { 2 } ) - \big ( S _ { 3 } \bigcap S _ { 4 } \big )$ , we have $E _ { T } \ { \stackrel {  } { = } } \ ( T _ { S _ { 1 } } \bigcup T _ { S _ { 2 } } ) - ( T _ { S _ { 3 } } \bigcap T _ { S _ { 4 } } )$ . The estimate for is then ErnU $\frac { | E _ { T } \bigcap { T } | \bigcup _ { i = 1 } ^ { m } { s _ { i } } } { k }$ , which is similar to (7). Combining the two estimates above, we get the estimator for $n _ { E }$

$$
n _ {\hat {E}} = \frac {\left| E _ {T} \cap T _ {\bigcup_ {i = 1} ^ {m} S _ {i}} \right|}{k} \frac {k - 1}{h _ {(k \bigcup)}} \tag {10}
$$

where $h _ { ( k _ { \parallel } ) } = m a x \{ T _ { \bigcup S _ { i } } \}$ . To achieve $( \varepsilon , \delta )$ -guarantee, we obtain Theorem 7 below, which also follows from Theorem 5 .

Theorem $7 ;$ To achieve -estimate for $n _ { E }$ , is at least $\begin{array} { r } { \Theta \big ( \frac { 1 } { \varepsilon ^ { 2 } R } l n \frac { 1 } { \delta } \big ) } \end{array}$ .

# B. Efficient Composite Counting Protocol

In this section, we design an efficient composite counting protocol in RFID systems, which implements the algorithms in the last section. We analyze the communication cost of our protocol and compare it with the lower bounds.

1) Protocol Design: To achieve the synopsis based estimation, we need the smallest hash values of each tag set. We focus on explaining how to obtain the smallest hash value (without normalization), since other $k - 1$ hash values can be obtained similarly. Our protocol is based on the slotted ALOHA communication model. It exploits binary search to obtain the smallest hash value.

We first use an illustrative example to express the general idea and then formally describe the protocol details. Assume we have 4 tags in a set. Their hash values are 4 bits in binary format, namely 0100, 0101, 0111, and 1110. The reader continuously sends 1-bit messages to the tags to reduce the search space. Initially, it sends a bit $\dot { } _ { \mathbf { 0 } } ,$ to the tags. The 4 tags store $^ { \circ }$ in their memory as prefix string $p r e f$ , and check whether $^ { \circ }$ is a prefix of their hash values. If so, they respond the reader with a bit $^ { \circ } 1 ^ { \circ }$ . Obviously, tags with hash values 0001, 0011, and 0100 will respond. Thus, the reader detects a non-empty slot and is convinced that there exists at least one hash value starting with $^ { \circ }$ . Further, the reader sends another $^ \circ$ to match the second bit in the hash values. Again, the tags append the received $^ { \circ }$ to and get $^ { \circ } 0 0 ^ { \circ }$ . Then they use $^ { \mathfrak { c } } 0 0 ^ { \mathfrak { , } }$ to do prefix matching. But this time, no successful matching exists. So the reader will detect an empty slot. After that, the reader tries $^ { \circ } 1 ^ { \circ }$ still for the second bit in hash values. All tags change to $^ { \mathfrak { c } } 0 1 ^ { \mathfrak { s } }$ (actually, all tags should change the last bit in $p r e f$ to $^ { \mathfrak { c } } 1 ^ { \mathfrak { s } }$ if they receive $^ { \circ } 1 \rangle$ . The procedure continues until the reader finds 0100 as the smallest hash value. Fig. 4 gives an illustration of the entire search procedure. If we still need to seek the second smallest hash value, we should keep the tag with 0100 silent, clear in all tags' memory, and repeat the procedure above. When the hash values are collected, we activate those tags that are kept silent. The detailed synopsis collection protocol for reader and tags are shown in Algorithm 1 and 2.

Algorithm 1: The synopsis collection algorithm for reader.   
Input: Synopsis size k, hash value length l (in binary).
Output: The synopsis.
for i ← 1 to k do
    minHash = ' '
    for j ← 1 to l do
    Send '0' to the tags and wait for the response r
    if r is empty then
    Send '1' to the tags
    Append '1' to minHash
    else
    Append '0' to minHash
    end
    end
    Add minHash to the synopsis
end
Activate all the silent tags
return synopsis

Algorithm 2: The synopsis collection algorithm for tags.   
Input: Hash value h(ID), length of h(ID) l (in binary).
pref = ' '
i = 0
while TRUE do
    Receive the bit b from the reader
    Append b to pref
    if pref is prefix of h(ID) then
    Respond reader with '1'
    else
    Keep silent in this slot
    end
    i ← i + 1
    if i = l then
    i ← 0
    if pref = h(ID) then
    Keep silent until activated
    end
    Clear pref
    end
end

2) Performance Analysis: We analyze the communication cost of our synopsis collection protocol. Obviously, for each $^ \circ$ in the target hash value, the reader spends 1 slot. For each $^ { \circ } 1 ^ { \circ }$ in the smallest hash value, the reader spends 2 slots: first with $^ { \circ }$ and then with $^ { \circ } 1 ^ { \circ }$ . Hence, the number of slots to collect one of the smallest hash values is $\Theta ( l )$ , where is the length of hash values in binary format. Considering that there are $O ( 1 )$ bits exchanged in each slot, the communication cost of our protocol for one tag set is $\Theta ( l )$ bits. Recall that the hash space should be sufficiently large to avoid collisions. In terms of two-set composite counting, the hash space should be $^ { n _ { \mathrm { l } } ^ { 2 } } |$ to avoid collision within $S _ { 1 } \cup S _ { 2 }$ . Thus, $\Theta ( l ) = \Theta ( \log n _ { \lfloor \ \rfloor } )$ . Then the communication overhead of estimating $| S _ { 1 } o p S _ { 2 } |$ where $o p \in \{ \bigcup , \bigcap , - \}$ should be $\Theta ( k$ log $^ { n } \bigcup ^ { }$ , where is the synopsis size. Incorporating the the foregoing analysis about , we have the following results. (Here is considered as a user-specified constant so $\frac { \overline { { \underline { { 1 } } } } } { \varepsilon }$ factor between the two bounds is not considered.)

![](images/4a8202fe7a055c9e7d67433c6dc22464d49ed04baf4452f4b8fa03d869052bde.jpg)  
Fig. 4. An illustrative example showing how the search procedure works. Each non-empty slot contains a reader's command followed by a tag's response.

• By Theorem 4, the communication cost of estimating with $( \varepsilon , \delta )$ -approximation in our protocol is $\Theta ( k$ log $n _ { \bigcup } ) = \Theta \left( \frac { \log n _ { \bigcup } } { \varepsilon ^ { 2 } } l n \frac { 1 } { \delta } \right)$ gUn . By Theorem 1, the lower bound for estimating $^ n \cup$ with $( \varepsilon , \delta )$ -approximation is   
$\begin{array} { r } { \Omega \big ( \frac { 1 } { \varepsilon ^ { 2 } } \big ) } \end{array}$ , when $\varepsilon = \Omega \left( { \frac { \mathrm { _ { 1 } } } { \sqrt { ^ { n } \lfloor } { \bigcup } } } \right)$ n . We observe the overhead of our protocol is within a small logarithm factor from the lower bound.   
• By Theorem 5 and Theorem 6, the communication overhead of estimating $n _ { o p }$ with $( \varepsilon , \delta )$ -approximation in our protocol is $\begin{array} { r } { { \tilde { n } } _ { \bigcup } ) = \Theta \left( \frac { n } { n _ { o p } } \frac { \log { n } } { \varepsilon ^ { 2 } } l n \frac { 1 } { \delta } \right) } \end{array}$ nop 1ognUlns) , where $o p \in \{ \bigcap , - \}$ . By Theorem 2 and Theorem 3, the lower bound for estimating $n _ { o p } \left( o p \in \{ \bigcap , - \} \right)$ with $( \varepsilon , \delta ) \mathopen { } \mathclose \bgroup  - \mathrm { a p - }$ proximation in RFID systems is $\Omega \left( \frac { { { n } } } { \varepsilon { { n } _ { o p } } } \right)$ enop Thus, the overhead of our protocol is also within a small logarithm factor from the lower bound.

# VI. IMPLEMENTATION

We implement the prototype of CCF using USRP softwaredefined reader and WISP computational tags, as shown in Fig. 5. We briefly introduce USRP reader and WISP below.

USRP Reader: We adopt a USRP implementation of EPC Gen-2 RFID reader [18], and customize it to the protocol described in Algorithm 1. We use RFX900 daughter board and Laird S9028 circular polarized antenna with the USRP. The reader is connected to a laptop via Gigabit Ethernet. All the experiments are run at carrier frequency of 900 MHz.

WISP Tags: We implement the protocol in Algorithm 2 using WISP 4.1DL computational tags. WISP is an open source EPC Gen-2 RFID tag that includes a programmable 16 bit MSP430 microcontroller. WISP is battery-less and harvests energy from the reader's signal like ordinary passive tags. WISP implements most parts of EPC Gen-2 standard, such as decoding the reader's commands, generating a random number, responding its ID etc. Since CCF requires a slight modification to the EPC Gen-2 standard, we incorporate the new features in our protocol into the original WISP code.

![](images/ff3d165e8c7ca1c29bde69437c4a4a399ff21cc7bb14534689ca2ee8969ba004.jpg)



Fig. 5. USRP and 4 WISP computational tags.

![](images/b2850f4d9bdea027d0df62c57e132f2fc36e56e617b4f88511267178ddbb280e.jpg)



Fig. 6. The communication between the reader and WISP in one round of identification. Query and ACK are reader signals, while RN16 and EPC are tag signals.

In EPC Gen-2 standard, the reader communicates with tags using the following procedure. The reader initiates communication by sending a command that could be , , , etc. We focus on the command, which the reader uses to identify the tag ID. It is important because a new command in our protocol is designed based on . Upon receiving the command, tags respond a 16-bit random number RN16. Then the reader sends an to the tag, and waits for the tag ID (EPC code). The whole communication procedure is plotted in Fig. 6.

In CCF, we design the command based on as depicted in Fig. 8(b), and add it into the command set. We keep the PHY/MAC field of in , since they are vital for the reader to negotiate the uplink communication parameters with the tags. We create a specialized field BIT in that corresponds to the 1-bit message in the synopsis collection protocol. To collect the synopsis, the reader repeatedly sends the command until it finds the smallest hash values. When receiving the command, each tag performs prefix matching, and issues a short response if the matching is successful. To be compatible with the original WISP code and be robust to channel error, we use a Fixed 16-bit string (F16) as the short response here. The difference between F16 and RN16 is that F16 is the same for all tags. Since tags are synchronized by the reader and their F16s are identical, the reader is allowed to robustly differentiate a non-empty slot with an empty slot due to constructive interference. In addition, tags are not required to report their IDs after . Fig. 7 plots the signals to search the smallest hash value in 4 WISPs using our prototype. We preload the 4-bit hash values 0100, 0110, 1100, and 1110 in the 4 WISPs, respectively. After 5 rounds, the smallest hash value 0100 can be found by the reader.

![](images/df10f65df5695ac6736ca75d21a5c375dd07378c531a07b3e4d20b18d5bac24d.jpg)



Fig. 7. The communication between the reader and 4 WISPs when searching for the smallest hash value 0100. Search 0(1) means the BIT field in is set to 0(1).The first command is followed by the superposition of two F16s, so the slot is non-empty. The second command is followed by an empty slot. The fourth command is followed by only one F16, so the slot is non-empty.

<table><tr><td></td><td>Command</td><td>PHY/MAC</td><td>Session</td><td>Q</td><td>CRC-5</td></tr><tr><td># of bits</td><td>4</td><td>4</td><td>5</td><td>4</td><td>5</td></tr></table>

<table><tr><td></td><td>Command</td><td>PHY/MAC</td><td>BIT</td><td>CRC-5</td></tr><tr><td># of bits</td><td>4</td><td>4</td><td>1</td><td>5</td></tr></table>

(b)   
Fig. 8. The packet formats of and command. (a) command. (b) command.

Although our protocol can be implemented in a real communication system, there is deficiency to thoroughly evaluate the performance of CCF using this prototype. The communication distance between URSP and WISP is limited, which makes large-scale counting difficult to experiment. Therefore, we turn to simulations to further investigate CCF.

# VII. EVALUATION

We conduct extensive simulations under different scenarios to investigate the accuracy and efficiency of CCF. The simulations are divided into two parts. First, we provide a case study of CCF using real-world RFID datasets. Then, we further study the performance of CCF in larger-scale RFID systems.

# A. Case Study

We evaluate CCF using the AMD Hope RFID dataset [19]. This dataset contains information collected at the ”Hackers On Planet Earth” (HOPE) conference in 2008. The

TABLE II DATASET CHARACTERISTICS 

<table><tr><td>Room combination</td><td>Abbr.</td></tr><tr><td>Turing  $\bigcup (\cap)$  Engressia</td><td>TE</td></tr><tr><td>Hopper  $\bigcup (\cap)$  18thFloor</td><td>H1</td></tr><tr><td>Hackerspace  $\bigcup (\cap)$  Phones</td><td>HP</td></tr><tr><td>Turing – AMD</td><td>TA</td></tr><tr><td>Engressia – Art</td><td>EA</td></tr><tr><td>Hopper – Radio</td><td>HR</td></tr><tr><td>(Turing  $\bigcup$  AMD – Art)  $\cap$  Engressia</td><td>E1</td></tr><tr><td>(Turing–Art–AMD)  $\bigcup$  Hopper</td><td>E2</td></tr><tr><td>(Turing  $\bigcup$  Engressia) – (Hopper  $\cap$  Art)</td><td>E3</td></tr></table>

TABLE III GROUND TRUTH 

<table><tr><td></td><td>TE</td><td>H1</td><td>HP</td></tr><tr><td>Union</td><td>1054</td><td>1112</td><td>1147</td></tr><tr><td>Intersection</td><td>755</td><td>1051</td><td>982</td></tr><tr><td></td><td>TA</td><td>EA</td><td>HR</td></tr><tr><td>Difference</td><td>420</td><td>391</td><td>466</td></tr><tr><td></td><td>E1</td><td>E2</td><td>E3</td></tr><tr><td>Expression</td><td>349</td><td>1075</td><td>512</td></tr></table>

conference distributes RFID badges (tags) to the attendees that can uniquely identify and track them in the conference. According to their own interest, attendees may visit difference conference rooms which hold various talks and events. Each tuple in the dataset includes the snapshot timestamp, tag ID, and conference room the attendee visits. There are a total of 21 rooms equipped with RFID readers, and each room has a unique name corresponding to the event topic in it, such as Turing and Engressia. We treat the attendees who have visited each room as a set. In this case study, we randomly selects 9 out of 21 rooms and count the number of attendees of various set expressions among them. In Table II, we summarize the rooms we choose and the expressions we use. For the expressions involving two rooms, we use their initials as abbreviation. For example, expressions between room Turing and Engressia are represented as TE for short. For other complex expressions including 4 sets (the last three tuples in Table II), we use E1, E2, and E3 for short. Each expression has a specific meaning. For instance, E3 denotes the people are interested in Turing or Engressia but not both Hopper and 18thFloor. Table III lists the actual number of attendees of all expressions as ground truth.

1) Simulation Settings and Comparison Protocols: In AMD Hope dataset, tag IDs are in range [0, 10,000]. Hence, each ID can be encoded in 14 bits. According to the EPCGlobal C1G2 standard, a slot to transmit a 14-bit ID takes 0.9 ms. A slot containing a 1-bit short response is 0.4 ms. The hash size is set to 100,000, or 17 bits in binary form. All simulation instances are repeated 150 runs, unless otherwise specified.

Since tag identification is a naive counting method, we use it as comparison for all expressions. We choose two tag identification protocol, namely the Aloha-based identification protocol and a more recent protocol called probabilistic Tree Hopping (TH) [20]. Also, we compare CCF with existing schemes that only work in specific type of expressions. We compare with the most efficient protocol so far — SRCM [8] in union estimation. INC [21] is chosen for comparison in intersection and difference estimation. Note that the protocols for comparison cannot achieve generic composite counting as CCF.

![](images/3c8e9b289142f07856d098f6bb5603dec8f84739f1db7b1d5ae2b03e259e745b.jpg)



(a)

![](images/291f4be49b82cfe533ec22f4cd97c6c413dd310e79eb7e3f05f42850b246abc5.jpg)



(b)

![](images/47e42cd99ff82cc0ac12a290177fb4e70ccb46c73644d1ccce1514ff30d22114.jpg)



（c）

![](images/ed011b0241414c092af5905f351fd0f612c62e5a58c71e9bc4b01cf5f66ba24b.jpg)



(d)

Fig. 9. Evaluation of estimation accuracy under different set expressions and synopsis sizes. (a) union estimation. (b) intersection estimation. (c) difference estimation. (d) composite expression estimation.   
![](images/64fae03871fc66d898567cca03458e83dbec1f5d88772b698358d35fbe33558d.jpg)



(a)

![](images/026789ce89f652b1a050f45717a580cfa36dd754a890e762d7912fc5776f833a.jpg)



(b)

![](images/182c7016ce1ddc6eee677c511665eedab22fe86bb8095c4eae0ca476e497f5ba.jpg)



![](images/a9408714c76662582aa6204aff750c00453d9b47edfafa76cee3efebf6c3043c.jpg)



Fig. 10. Evaluation of estimation time to $\varepsilon = 0 . 1$ under different set expressions. (a) union estimation. (b) intersection estimation. (c) difference estimation. (d) composite expression estimation.

2) Accuracy: We study the estimation accuracy of CCF with various synopsis size . Consistent with previous work, we use relative error as the accuracy metric. Relative error is defined as $| { \hat { n } } - n | / n$ , where is the estimate and is the actual expression size.

Fig. 9 depicts the estimation accuracy of various kinds of expressions while different synopsis sizes are applied. For each type of expression, we select three instances from the dataset. The figures show that one can always improve the estimation accuracy by increasing the synopsis size, which apparently incurs more communication overhead. Fig. 9(a) suggests that synopsis size of 100 is enough to achieve relative error rate below 10% when counting more than 1,000 people. Moreover, as shown by TE in Fig. 9(b), EA in Fig. 9(c) and E1 in Fig. 9(d), we need larger synopsis to estimate a smaller expression size to the same accuracy level. This is consistent with our theoretical analysis. For example, to estimate $| E 1 | = 3 4 9$ to relative error of 10%, the synopsis size should be as least 150. In contrast, to estimate $| E 2 | = 5 1 2 , k = 1 0 0$ will achieve the same accuracy.

3) Communication Time: We compare the communication time of CCF with recent estimation protocols given the same accuracy requirement. Here we fix the relative error $\varepsilon \ = \ 0 . 1$ , which is sufficiently accurate for many applications. Fig. 10 plots the total time required to estimate the size of various expressions to relative error 0.1. We observe from Fig. 10(a) that the cost of CCF is close to the SRCM protocol—the best protocol to estimate the union size so far (actually SRCM is near optimal). However, SRCM is unable to estimate intersection and difference size, let alone other complex expressions. In Fig. 10(b)–(c), we find that CCF is more efficient than the existing protocol INC, when estimating intersection and difference size. More precisely, the estimation time of INC is 2.4 and 5.3 the time of CCF in average when estimating intersection and difference, respectively. Furthermore, we notice that CCF is far more efficient than tag identification, either Tree Hopping or Aloha-based identification. As shown in Fig. 10(d), the estimation time of Alhoa-based scheme and TH is 1.99 and 1.58 of CCF in average, respectively. The reason is that Aloha-based identification requires tags to transmit the entire ID, which takes much longer than a short response. Although Tree Hopping is faster than Aloha-based identification, its communication overhead grows linearly with the number of tags as in Aloha-based identification, but with a smaller factor. The synopsis size in CCF, however is sublinear w.r.t the number of tags.

# B. Large-Scale Simulation

To further evaluate the performance of CCF in these systems, we conduct more simulations as follows.

The simulation settings is a little different from the case study. First, generally the tag IDs are 96 bits rather than 14 bits, as specified in the C1G2 standard, which allows objects to be labeled. As a result, the ID slot is extended to 2.4 ms. Second, we manually set the number of tags in each set to 100,000. Correspondingly, the hash size is adjusted to 100,000,000 to avoid hash collisions. Specifically, we create 4 tag sets , , and . We aim to estimate the size of 4 kinds of expressions: , , , and $E = ( A \bigcup B - C ) \bigcap D$ .

1) Accuracy: We evaluate the relationship between accuracy of CCF and target expression size, when the synopsis size is fixed to 600. Table IV lists the simulation results (r.e. stands for relative error). We find that the estimate accuracy for union basically keeps the same when changes. However, the estimate accuracy for $| A \cap B | , | A ^ { \setminus } - \dot { B } |$ and drops when the target size becomes smaller. Both trends coincide with our analysis of estimators in Section V-A. Notice that we are always able to achieve desirable accuracy, if the synopsis size is chosen appropriately according to the target expression size.

2) Communication Time: In this part, we set $| A \cup B | \ =$ , , , and $| E | = 2 0 0 0 0$ .

![](images/8c5a8cd0fb28ea75182926c15f72d9c441dcf0b956082e05a7f6d7c11d9e021c.jpg)



![](images/d57300c18e080c752c7bd00967c4afacbd600c49aee0b5d4918651acaf10987a.jpg)



![](images/5be9f6bdf7177a2e678a12911069619c511d743856aed3bc3b47e52cd8cbfa58.jpg)



![](images/fedde899cb51ee920cf99620727402c43831be6302386d5680f0115f3d0f041b.jpg)



Fig. 11. Evaluation of estimation time under different set expressions and accuracy requirements. (a) estimation. (b) estimation. (c) $| A - B |$ estimation. (d) estimation.

TABLE IV ACCURACY OF CCF WITH VARIED EXPRESSION SIZES. 

<table><tr><td> $|A \cup B|$ r.e</td><td>190,0000.036</td><td>175,0000.035</td><td>160,0000.029</td><td>145,0000.035</td><td>130,0000.03</td><td>115,0000.033</td></tr><tr><td> $|A \cap B|$ r.e.</td><td>10,0000.146</td><td>25,0000.093</td><td>40,0000.058</td><td>55,0000.048</td><td>70,0000.041</td><td>85,0000.035</td></tr><tr><td> $|A - B|$ r.e.</td><td>10,0000.11</td><td>25,0000.074</td><td>40,0000.057</td><td>55,0000.053</td><td>70,0000.052</td><td>85,0000.047</td></tr><tr><td> $|E|$ r.e.</td><td>10,0000.167</td><td>25,0000.098</td><td>40,0000.084</td><td>55,0000.066</td><td>70,0000.064</td><td>85,0000.056</td></tr></table>

Fig. 11 compares the estimation time of CCF and existing protocols when relative error varies from 0.06 to 0.14. Note that all the results are derived from real simulations rather than mathematical bounds, since mathematical bounds are usually too loose to reflect real protocol performances. Overall, the estimation time increases as the relative error drops for all protocols. In $| A \cup B |$ estimation, our protocol is 1.56 slower than SRCM, whereas up to 1400 faster than Aloha-based identification and 1000 faster than Tree Hopping when $\varepsilon = 0 . 1 4$ . In $| A \cap B |$ and $| A - B |$ estimation, CCF is 2.1 and $3 . 3 \times$ faster than INC in average. In terms of estimating , CCF is as much as $7 5 . 4 \times$ faster than Aloha-based identification and $5 2 \times$ faster than Tree Hopping. Although identification always achieves 0% error rate, the accuracy and communication time tradeoff achieved in CCF is desirable. Furthermore, we observe that the advantage of CCF over identification in large-scale settings is more significant compared with the results in the case study, since the cost of identification grows linearly with the tag number while CCF is sublinear.

# VIII. DISCUSSION

Several points are worth being further discussed here.

Synopsis Maintenance: The counting approach proposed in this paper is not only designed for transient scenarios, but also for long-term counting objectives. Particularly, the tags covered by a given reader can constantly change over time, which results in the change of synopsis. To obtain such long-term counting results, we should label the synopsis with a timestamp. If we want to count an expression during time interval $[ t _ { 1 } , t _ { 2 } ]$ , we simply search all synopsis obtained during $[ t _ { 1 } , t _ { 2 } ]$ for each involved set using their timestamp and merge them (by union). Long-term counting can be achieved based on these merged synopsis. To speed up timestamp searching and synopsis merge, we can use various techniques such as indexing, which is out of the scope of this paper.

Choosing Synopsis Size: Generally, to choose a proper value for the synopsis size before estimating expression , we have to know $\begin{array} { r } { R \ = \ \frac { | E | } { | \bigtriangledown _ { i = 1 } ^ { m } S _ { i } | } } \end{array}$ in advance according to Theorem 7. The calculation of , however, requires as well. We propose two solutions here. The first one is similar to solutions in [2]–[8]. We can initially set a big enough blind estimate for , say 1. Then few rounds of iteratively computing and k in turn could give a good guess for . Another solution is to set this blind estimate according to historical data or empirical study. Also, note that Theorem 7 just gives a theoretical bound for k, which provides a theoretical guarantee but is usually very loose. In practice, a much smaller value for k will achieve satisfactory result compared to the theoretical bound. For example, in Fig. 10(b), is enough to achieve 0.1 relative error in TE estimation. However, the theoretical bound according to Theorem 7 is $k = l n 1 0 * 1 0 5 4 / ( 7 5 3 * 0 . 1 * 0 . 1 ) = 3 2 2 > 1 0 0$ if we set $\varepsilon = \delta = 0 . 1$ .

Dealing With Small Target Tag Set: According to Theorem 7, the synopsis size or equivalently the communication overhead of estimation will grow as becomes small. At tipping point, it may exceed the communication overhead of trivial identification. There exists a critical threshold of the size of to decide whether to adopt exact identification or synopsis-based estimation. We set tag ID to 96 bits as in the standard [12]. Theoretically, if synopsis-based estimation has smaller overhead, the following inequality holds

$$
k \log | \bigcup_ {i = 1} ^ {m} S _ {i} | <   9 6 \sum_ {i = 1} ^ {m} S _ {i} \tag {11}
$$

where $| \cup _ { i = 1 } ^ { m } S _ { i } |$ is the length of hash value. According to Theorem 7, we have

$$
\frac {\lambda \left| \bigcup_ {i = 1} ^ {m} S _ {i} \right|}{| E | \varepsilon^ {2}} \ln \frac {1}{\delta} \log \left| \bigcup_ {i = 1} ^ {m} S _ {i} \right| <   9 6 \sum_ {i = 1} ^ {m} S _ {i} \tag {12}
$$

where is scale factor, since $\begin{array} { r } { k = \Theta ( \frac { 1 } { \varepsilon ^ { 2 } R } l n \frac { 1 } { \delta } ) } \end{array}$ . It follows that

$$
| E | > \frac {\lambda | \bigcup_ {i = 1} ^ {m} S _ {i} |}{9 6 \varepsilon^ {2} \sum_ {i = 1} ^ {m} S _ {i}} \ln \frac {1}{\delta} \log | \bigcup_ {i = 1} ^ {m} S _ {i} |. \tag {13}
$$

Since ${ \frac { | \bigcup _ { i = 1 } ^ { m } S _ { i } | } { \sum _ { i = 1 } ^ { m } S _ { i } } } \leq 1$ and $| \cup _ { i = 1 } ^ { m } S _ { i } | \leq \log \sum _ { i = 1 } ^ { m } S _ { i } , { \mathrm { i f ~ } } | E |$ satisfies the following inequality,

$$
| E | > \frac {\lambda}{9 6 \varepsilon^ {2}} l n \frac {1}{\delta} \log \sum_ {i = 1} ^ {m} S _ {i} \tag {14}
$$

it is better to choose synopsis-based identification.

# IX. CONCLUSION

Counting as a fundamental issue in RFID faces a lot of new challenges as various new scenarios and demands of RFID management are emerging. Compared to simple counting that has been studied for years, we introduce an even more general problem, the composite counting in RFID systems. We propose a generic composite counting framework for estimating cardinality of any set expression with desired accuracy. Through complexity analysis, prototype system validation, and large-scale simulations, we show that a large improvement is achieved in both time-efficiency and accuracy.

# APPENDIX A PROOF FOR LEMMAS AND THEOREMS

Proof for Lemma 1: The proof has two steps. First, the communication cost of is no lower than . The reason is that Alice and Bob in know their sets exactly, whereas $S _ { 1 }$ and $S _ { 2 }$ are unknown in . Hence, if can be solved using some protocol, can be solved in exactly the same way. Second, the communication overhead of is no lower than . The reason goes as follows. If there is a protocol that solves , we redirect all bits that flow from Alice to Carol in this protocol to Bob. Thus, Bob can count $| S _ { 1 } \cup S _ { 2 } |$ locally, and then sends bits to Alice to inform her the result. Thus, can be solved with no more bits than . Combining the two conclusions above, we obtain that the communication overhead of is no lower than .

Proof for Theorem 1: An existing communication complexity lower bound for TUC shows $\Omega \overline { { ( \frac { 1 } { \varepsilon ^ { 2 } } ) } }$ bits must be transmitted for any $\varepsilon = \Omega \left( { \frac { \ d H _ { 1 } } { \sqrt { | S _ { 1 } | { \bf U } _ { 2 } | } } } \right)$ [22]. Since $\begin{array} { r } { \Omega \big ( \frac { 1 } { \varepsilon ^ { 2 } } \big ) } \end{array}$ is a lower bound for , it must be a lower bound for in -approximation according to Lemma 1.

Proof for Lemma 2: The proof is similar to that of Lemma 1.

Proof for Theorem 2: An existing communication complexity lower bound [14] shows that at least $\Theta \left( { \frac { | S _ { 1 } \bigcup S _ { 2 } | } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } } \right)$ bits should be transmitted to solve for any randomized protocol. In Lemma 2, we show that is a more difficult problem to . Therefore, any randomized protocol that solves must also transmits $\left( \frac { | S _ { 1 } \bigcup S _ { 2 } | } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } \right)$ bits.

Proof for Lemma 3: For randomized protocols, from Theorem 2, we easily know that this lemma holds. So we need to examine whether $\left( \frac { | S _ { 1 } \bigcup S _ { 2 } | } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } \right)$ is still smaller than naive identification protocol which uses ${ \mathcal { O } } ( n )$ bits, when $\begin{array} { r } { \varepsilon = \Omega \left( \frac { 1 } { | S _ { 1 } \bigcap S _ { 2 } | } \right) } \end{array}$ The derivation is as follows.

$$
\begin{array}{l} \frac {\left| S _ {1} \bigcup S _ {2} \right|}{\left| S _ {1} \bigcap S _ {2} \right| \varepsilon} = \Omega \left(\frac {\left| S _ {1} \bigcup S _ {2} \right|}{\left| S _ {1} \bigcap S _ {2} \right| \frac {1}{\left| S _ {1} \bigcap S _ {2} \right|}}\right) \\ = \Omega (| S _ {1} \bigcup S _ {2} |) \\ = \Omega (| S _ {1} | + | S _ {2} |). \tag {15} \\ \end{array}
$$

Note that if naive identification protocol is adopted to solve $R I C _ { \mathrm { { : } } }$ then at least one bit should be transmitted for each tag in $| S _ { 1 } |$ and $| S _ { 2 } |$ . Even more bits are required if tag response collision is considered. Hence, the communication complexity for naive identification is strictly higher than $| S _ { 1 } | + | S _ { 2 } |$ . It follows from (15) that the communication complexity for naive identification is $\left( \frac { | S _ { 1 } \bigcup S _ { 2 } | } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } \right)$ . Therefore, $\Omega \left( { \frac { | S _ { 1 } | \bigcup S _ { 2 } | } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } } \right)$ is a lower bound for no matter randomized protocol or naive identification protocol is adopted.

Proof for Theorem 3: This theorem directly follows Theorem 2, since $S _ { 1 } - S _ { 2 } = S _ { 1 } \cap \bar { S } _ { 2 }$ .

Proof for Lemma 4:

$$
\begin{array}{l} P \{| \hat {n} - n | \leq \varepsilon n \} = P \left\{(1 - \varepsilon) n \leq \frac {k - 1}{h _ {(k)}} \leq (1 + \varepsilon) n \right\} \\ = P \left\{\frac {k - 1}{(1 - \varepsilon) n} \leq h _ {(k)} \leq \frac {k - 1}{(1 + \varepsilon) n} \right\}. \\ \end{array}
$$

Note that $h _ { ( k ) }$ follows beta distribution with parameters and [23]. Let $n - k + 1 [ 2 3 ]$ $\begin{array} { r } { x _ { 1 } = \frac { k - 1 } { ( 1 - \varepsilon ) n } } \end{array}$ and $\begin{array} { r } { x _ { 2 } = \frac { k - 1 } { ( 1 + \varepsilon ) n } } \end{array}$ . We have

$$
P \{x _ {1} \leq h _ {(k)} \leq x _ {2} \} = I _ {x _ {1}} (k, n - k + 1) - I _ {x _ {2}} (k, n - k + 1). \tag {16}
$$

Let the R.H.S. of (16) be greater or equal to . We have

$$
I _ {x _ {1}} (k, n - k + 1) - I _ {x _ {2}} (k, n - k + 1) \geq 1 - \delta . \tag {17}
$$

By (17), we get $\begin{array} { r } { k = \Theta \big ( \frac { 1 } { \varepsilon ^ { 2 } } l n \frac { 1 } { \delta } \big ) } \end{array}$ using the theory of order statistics [23].

Proof for Lemma 5: Let be the smallest values in $T _ { S _ { 1 } } \bigcup T _ { S _ { 2 } }$ . According to the definition of $T _ { ( S _ { 1 } \vert \ l \vert S _ { 2 } ) } ,$ , it suffices to show that the smallest hash values in $T _ { S _ { 1 } } \bigcup T _ { S _ { 2 } }$ are also the smallest ones in , namely . $h ( S _ { 1 } ) \bigcup h ( S _ { 2 } )$ $P = T _ { ( S _ { 1 } \left\lfloor \ j S _ { 2 } \right. } .$ This can be proved by contradiction. Suppose there exists $h ( S _ { 1 } ) \bigcup h ( \bar { S _ { 2 } } ) - ( \bar { T _ { S _ { 1 } } } \bigcup T _ { S _ { 2 } } )$ and $b \in \ P$ such that $a \ < \ b .$ . Without loss of generality, let $\iota \in h ( S _ { 2 } )$ . Then obviously $b \notin$ $T _ { S _ { 2 } }$ , since otherwise $a \in T _ { S _ { 2 } }$ , which contradicts the assumption of . Also, is larger than any hash value in $T _ { S _ { 2 } }$ according to the definition of $T _ { S _ { 2 } }$ . Since $b \ > \ a ,$ is also larger than any hash value in $T _ { S _ { 2 } }$ . Recall that $b \notin T _ { S _ { 2 } }$ , so there must be $k ^ { \prime } > | T _ { S _ { 2 } } | = k$ hash values in $T _ { S _ { 1 } } \bigcup { \dot { T } } _ { S _ { 2 } }$ that are smaller than , indicating $b \notin P$ . This contradicts the condition that $b \in P$ .

Proof for Theorem 4: Lemma 5 indicates that the smallest hash values from $S _ { 1 } \cup S _ { 2 }$ can be used to estimate $^ n \mathrm { U }$ . This coincides with the single set scenario that smallest hash values from can be used to estimate . Therefore, the of $( \varepsilon , \delta ) \mathopen { } \mathclose \bgroup  - \mathrm { e s - }$ timate for $^ n \cup$ is the same as in Lemma 4, which independent of $^ { n } \lfloor \rfloor \cdot$ .

Proof for Theorem 5: Let $k _ { 1 }$ and $k _ { 2 }$ be synopsis size that achieve $( \varepsilon / 3 , \delta )$ -estimate for and $^ { n _ { \mathrm { l } } } | \mathrm { \Delta } |$ , respectively. Then it is apparent that the value of should be $k = \operatorname* { m a x } \{ k _ { 1 } , k _ { 2 } \}$ . By ff bound of random sampling [24],. Additionally, we have shown tha $\begin{array} { r } { k _ { 1 } \ge \frac { 3 ( 6 + \varepsilon ) } { \varepsilon ^ { 2 } J } l n \frac { 2 } { \delta } > } \end{array}$ $\textstyle \frac { 1 8 } { \varepsilon ^ { 2 } J } l n { \frac { 2 } { \delta } }$ $\begin{array} { r } { \Theta \big ( \frac { 9 } { \varepsilon ^ { 2 } } l n \frac { 1 } { \delta } \big ) } \end{array}$ attain $( \varepsilon / 3 , \delta )$ -approximation. Hence, $k ~ = ~ \operatorname* { m a x } \{ k _ { 1 } , k _ { 2 } \} ~ =$ $\begin{array} { r } { \Theta \big ( \frac { 1 } { \varepsilon ^ { 2 } J } \dot { l } n { \frac { 1 } { \delta } } \big ) } \end{array}$ guarantees to give an $( \varepsilon , \delta )$ -estimate for $^ n \cap$ .

Proof for Theorem 6 and Theorem 7: We observe that the only difference among (8), (9) and (10) is that how we operate on the synopsis. Specifically, the operations among synopsis is identical to those in . Hence, the proofs of Theorem 6 and 7 are the same as Theorem 5.

# ACKNOWLEDGMENT

The authors would like to thank the anonymous reviewers for their insightful comments.

# REFERENCES

[1] J. Lim, S. Kim, H. Oh, and D. Kim, “A designated query protocol for serverless mobile RFID systems with reader and tag privacy,” Tsinghua Sci. Technol., vol. 17, no. 5, pp. 521–536, 2012.   
[2] M. Kodialam and T. Nandagopal, “Fast and reliable estimation schemes in RFID systems,” in Proc. MobiCom, 2006, pp. 322–333.   
[3] M. Kodialam, T. Nandagopal, and W. Lau, “Anonymous tracking using RFID tags,” in Proc. IEEE INFOCOM, 2007, pp. 1217–1225.   
[4] C. Qian, H. Ngan, Y. Liu, and L. M. Ni, “Cardinality estimation for large-scale RFID systems,” IEEE Trans. Parallel Distrib. Syst., vol. 22, no. 9, pp. 1441–1454, Sep. 2011.   
[5] T. Li, S. S. Wu, S. Chen, and M. C. K. Yang, “Generalized energy-efficient algorithms for the RFID estimation problem,” IEEE/ACM Trans. Netw., vol. 20, no. 6, pp. 1978–1990, Dec. 2012.   
[6] M. Shahzad and A. Liu, “Fast and accurate estimation of RFID tags,” IEEE/ACM Trans. Netw., vol. 23, no. 1, pp. 241–254, Feb. 2015.   
[7] Y. Zheng and M. Li, “Towards more efficient cardinality estimation for large-scale RFID systems,” IEEE/ACM Trans. Netw., vol. 22, no. 6, pp. 1886–1896, Dec. 2014.   
[8] Z. Zhou, B. Chen, and H. Yu, “Understanding RFID counting protocols,” IEEE/ACM Trans. Netw., 2014, to be published.   
[9] K. Finkenzeller et al., RFID Handbook: Fundamentals and Applications in Contactless Smart Cards, Radio Frequency Identification and Near-Field Communication. Hoboken, NJ, USA: Wiley, 2010.   
[10] “GNURadio tookit,” [Online]. Available: http://gnuradio.org/redmine/ projects/gnuradio/wiki   
[11] “WISP: Wireless Identification and Sensing Platform,” [Online]. Available: http://wisp.wikispaces.com   
[12] EPCglobal, Inc., “EPC Radio-frequency Identity Protocols Class-1 Generation-2 UHF RFID Protocol for Communications at 860 MHz–960 MHz,” 2008 [Online]. Available: http://www.gs1.org/ gsmp/kc/epcglobal/uhfc1g2/uhfc1g2\_1\_2\_0-standard-20080511.pdf   
[13] Q. Xiao, B. Xiao, and S. Chen, “Differential estimation in dynamic RFID systems,” in Proc. IEEE INFOCOM, Mini-Conf., 2013, pp. 295–299.   
[14] S. Ganguly, M. Garofalakis, and R. Rastogi, “Tracking set-expression cardinalities over continuous update streams,” VLDB J., vol. 13, no. 4, pp. 354–369, 2004.   
[15] J. R. Cha and J. H. Kim, “Dynamic framed slotted ALOHA algorithms using fast tag estimation method for RFID system,” in Proc. IEEE CCNC, 2006, pp. 768–772.   
[16] E. Kushilevitz and N. Nisan, Communication Complexity. Cambridge, U.K.: Cambridge Univ. Press, 2006.   
[17] A. Z. Broder, M. Charikar, A. M. Frieze, and M. Mitzenmacher, “Min-wise independent permutations,” in Proc. ACM STOC, 1998, pp. 327–336.   
[18] “Gen 2 RFID Tools,” 2013 [Online]. Available: https://moo.cmcl.cs. cmu.edu/trac/cgran/wiki/Gen2   
[19] University of California, Irvine, “AMD Hope RFID data,” [Online]. Available: http://networkdata.ics.uci.edu/data.php?d=amdhope   
[20] M. Shahzad and A. X. Liu, “Probabilistic optimal tree hopping for RFID identification,” IEEE/ACM Trans. Netw., vol. 23, no. 3, pp. 796–809, Jun. 2015.   
[21] W. Gong, I. Stojmenovic, A. Nayak, K. Liu, and H. Liu, “Fast and scalable counterfeits estimation for large-scale RFID systems,” IEEE/ACM Trans. Netw., 2015, to be published.   
[22] D. Woodruff, “Optimal space lower bounds for all frequency moments,” in Proc. SODA, 2004, pp. 167–175.   
[23] B. C. Arnold, N. Balakrishnan, and H. H. N. Nagaraja, A First Course in Order Statistics. Philadelphia, PA, USA: SIAM, 1992, vol. 54.   
[24] M. Mitzenmacher and E. Upfal, Probability and Computing: Randomized Algorithms and Probabilistic Analysis. Cambridge, U.K.: Cambridge Univ. Press, 2005.

![](images/8eed228de36ce011ec26a488091504419fb81b438572628665e9d536cff448b3.jpg)



Wei Gong received the B.S. degree from the Department of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan, China, in 2003 and the M.S. and Ph.D. degrees in School of Software and Department of Computer Science and Technology from Tsinghua University, in 2007 and 2012, respectively. His research interests include RFID applications, wireless networks, and mobile computing.

![](images/83e6c35e494614ab442bc0d0699722def27ddaae243418e1aac6687847ff76ad.jpg)



Haoxiang Liu received the B.S. degree from the Department of Computer Science and Technology, Shanghai Jiao Tong University, Shanghai, China in 2007. He is currently a Ph.D. candidate in the Department of Computer Science and Engineering, the Hong Kong University of Science and Technology. His research interests include RFID applications and mobile computing.

![](images/ffbdca190b00ba02c8f0003de072f20aaabe8a680cf5a8f2d8f2b15c7e0576c0.jpg)



Lei Chen received the BS degree in computer science and engineering from Tianjin University, China, in 1994, the MA degree from Asian Institute of Technology, Thailand, in 1997, and the PhD degree in computer science from the University of Waterloo, Canada, in 2005. He is now an Associate Professor in the Department of Computer Science and Engineering at Hong Kong University of Science and Technology. His research interests include uncertain databases, graph databases, multimedia and time-series databases, and sensor and peer-to-peer

databases. He is a member of the IEEE.

![](images/9963d0a7ef3203fe7e4b8d3482d9fdc445bf4224aa01b73df2de9787cfde5f6a.jpg)



Kebin Liu received his BS degree in Department of Computer Science from Tongji University, and an MS degree in Shanghai Jiaotong University, China. He is a joint PhD student in Department of Computer Science and Engineering at Shanghai Jiaotong University and Department of Computer Science and Engineering in Hong Kong University of Science and Technology, under supervision of Dr. Yunhao Liu. His research interests include sensor networks and distributed systems.

![](images/82290d0445dd27400ee597d15b04c032a34d4a102944a8ee789626568a445d4b.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is currently the Chang Jiang Professor at School of Software and TNLIST, Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is an IEEE Fellow since 2014.