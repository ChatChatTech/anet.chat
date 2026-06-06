# Generic Composite Counting in RFID Systems

Haoxiang Liu∗, Wei Gong†, Lei Chen∗, Wenbo He‡, Kebin Liu†, Yunhao Liu†

∗Department of Computer Science and Engineering, Hong Kong University of Science and Technology

†School of Software and TNLIST, Tsinghua University

‡School of Computer Science, McGill University

Email: {hliuab, leichen}@cse.ust.hk, {gongwei, kebin, yunhao}@greenorbs.com, wenbohe@cs.mcgill.ca

Abstract—Counting the number of RFID tags is a fundamental issue and has a wide range of applications in RFID systems. Most existing protocols, however, only apply to the scenario where a single reader counts the number of tags covered by its radio, or at most the union of tags covered by multiple readers. They are unable to achieve more complex counting objectives, i.e., counting the number of tags in a composite set expression such as $( S _ { 1 } \bar { \bigcup } S _ { 2 } ) - ( S _ { 3 } \bigcap S _ { 4 } )$ . This type of counting has realistic significance since it provides more diversity than existing counting scenario, and can be applied in various applications.

In this paper, we formally introduce the RFID composite counting problem, which aims at counting the tags in arbitrary set expression. We obtain strong lower bounds on the communication cost of composite counting. We then propose a generic Composite Counting Framework (CCF) that provides estimates for any set expression with desired accuracy. The communication cost of CCF is proved to be within a small factor from the optimal. We build a prototype system for CCF using USRP software defined radio and Intel WISP computational tags. Also, extensive simulations are conducted to evaluate the performance of CCF. The experimental results show that CCF is generic, accurate and time-efficient.

# I. INTRODUCTION

Radio Frequency Identification (RFID) is envisioned as a promising technology and sometimes a prerequisite for the Internet of Things (IOT). Every object in the physical world can be equipped with an RFID tag that bears a unique ID. An RFID reader is adopted to identify the tags using wireless communication. Due to the small size and ultra-low power of tags, RFID holds immense potential in applications such as localization [1], supply chain management [2] and object tracking [3]. According to forecasts, the global RFID market will reach US18.7\$ billion by the year 2017 [4].

Counting the number of RFID tags, and thus the number of corresponding objects, is a fundamental issue in RFID systems [5]. Motivated by its importance, a number of counting schemes have been proposed to address this problem [5]– [13]. Most existing schemes only work in the simple scenario in which a single reader counts the number of tags in its covered area. We call this counting scenario simple counting. This simple scenario, however, fails to meet practical and complex application demands. The reasons are three-fold. First, multiple readers can be deployed in practical RFID systems, since a single reader has limited coverage area. Thus, tags to count may be covered by different readers instead of a single one. Second, tags may be mobile rather than static. Consequently, readers read different tags at different times. Third, the counting objective can be various, depending on specific applications. More precisely, the target tags may be obtained via different kinds of tag set operations. Consider the following three examples:

Warehouse management. One primary target of warehouse management is to obtain the total amount of goods (tags) in the large warehouse. It is clearly infeasible to use one static reader to count the tags, since the typical communication distance between a reader and passive tags is limited to 12 meters [14]. Therefore, the counting operation should be conducted at different locations to cover the entire warehouse. Then the union of the covered tags at these locations constitutes the target tag set. Note that duplicate counting should be avoided due to coverage overlap among the readers.

Conference statistics. In a conference, each conference room is equipped with an RFID reader. The organizers distribute RFID wristbands to participants in order to enable real-time people tracking. Some useful conference statistics can be obtained over time, such as the number of participants that visit both conference room A and B during time $[ t _ { 1 } , t _ { 2 } ]$ . In this case, the readers in room A and B have to collaboratively count the intersection of their reading results, i.e., $\left| A ( t _ { 1 } , t _ { 2 } ) \cap B ( t _ { 1 } , t _ { 2 } ) \right.$ |.

Tag authentication. Tag authentication aims to distinguish the genuine tags from the counterfeit ones [15]. Given a set of genuine tag IDs A in the authentication server and a set of tags B to be verified, we wish to count the number of genuine and counterfeit tags in B, namely |AB| and $| B - A |$ respectively. Tag authentication requires operations like set intersection and difference.

All above examples require counting the cardinality of a set expression rather than a single set, which are dramatically different from the simple counting problem. The set expressions involve set operators including union, intersection and difference. More generally, the expression can be extended to any combination of the set operations, depending on the application demands. For example, let Si be the set of participants who have visited the i-th conference room during a time period in the aforementioned example 2. By counting $| ( S _ { 1 } \bigcup S _ { 2 } ) - ( S _ { 3 } \bigcap S _ { 4 } )right.$ |, we manage to derive the number of people visiting room 1 or 2, but not both 3 and 4, as illustrated in Figure 1. In light of the composite set expression embodied in this type of RFID counting, we call it composite counting in contrast to simple counting. Often in many applications, it is desirable to just estimate the number of tags rather than explicitly identifying each tag, since exact result is often unnecessary and the overhead of exact counting is prohibitively high for large tag number. We therefore address composite counting by probabilistic estimation, which is usually more time-efficient. The words counting and estimation will be used interchangeably throughout this paper.

Unfortunately, composite counting cannot be trivially solved by simple counting techniques due to the following reasons. First, most simple counting techniques give an estimate for the number of tags rather than deterministic identification, since exact result is often not necessary for many applications and the overhead of exact counting is prohibitively high for large tag number, namely $O ( n )$ where n is the tag number. As a result, tag IDs in each set are unknown in simple counting, and thus we cannot solve composite counting by direct set operations. Notice that we still use estimation for composite counting in this paper for sake of efficiency and scalability. Second, we cannot simply mimic operators like union and difference with addition and subtraction. For example, it is obviously incorrect to approximate $| S _ { 1 } | U S _ { 2 } |$ with $\left| S _ { 1 } \right| + \left| S _ { 2 } \right|$ , or approximate $| S _ { 1 } - S _ { 2 } |$ with $\vert \vert S _ { 1 } \vert - \vert S _ { 2 } \vert \vert$ .

This paper offers a comprehensive study of the composite counting problem that is useful in a variety of RFID applications. First, we establish strong lowers bound on the communication cost for any composite counting method, by leveraging communication complexity theory. The lower bounds help us to benchmark the performance of our counting protocol. We then propose a generic Composite Counting Framework (CCF) that can estimate the cardinality of arbitrary set expression with desired accuracy. CCF exploits a small synopsis for each tag set to estimate, whose size is sublinear w.r.t the set cardinality. Furthermore, we design a protocol to efficiently construct the synopsis from tag sets. We demonstrate that the communication cost of our protocol is within a small logarithm factor from the lower bounds. We implement a prototype system of CCF using USRP software radios [16] and Intel WISP computational tags [17], which only requires a slight modification to the EPCGlobal Class-1 Generation-2 (C1G2) standard [18]. Finally, we extensively evaluate the performance of CCF using real-world datasets.

This paper makes the following contributions:

Composite counting and lower bounds. We introduce and formulate the composite counting problem and provide lower bounds of its communication cost using communication complexity theory.   
• Generic framework. We propose a generic Composite Counting Framework (CCF) that is able to estimate the number of tags in arbitrary set expression with desired accuracy. The key feature of CCF is that the estimation is solely based on small synopsis rather than original tag sets.   
Efficient composite counting protocol. We design an efficient protocol that constructs the synopsis from tag sets. The communication cost of our protocol is only within a small factor from the lower bounds.   
• Prototype implementation. We build a prototype system

![](images/6a20dc4804e501424aadffd38d8bcf9cedc71e9655800135cb9e587dd02732ee.jpg)



Fig. 1. A composite counting example. A reader is located in each conference room. People wearing RFID tags will be identified by the reader once they enter the room. Let Si be the tag set read by the reader in room i, and $| E | =$ $\left| ( S _ { 1 } \bigcup S _ { 2 } ) - ( S _ { 3 } \bigcap S _ { 4 } ) \right|$ . Then participants $a , c \in E$ and b ∈/ E. Thus, the counting result is $| E | = 2$ in this example.

of CCF using USRP software radios and WISP computational tags, which only requires a slight update to the EPCGlobal C1G2 standard.

The rest of this paper is organized as follows. In Section II, we review the related work. In Section III, we formulate the composite counting problem. We present the lower bounds in Section IV and the design of CCF in Section V. We show the prototype implementation in Section VI and conduct the simulations in Section VII. We conclude the paper in Section VIII.

# II. RELATED WORK

There has been a stream of RFID counting protocols under the simple counting model [5]–[13], [19]. These protocols are based on probabilistic estimators that achieve required accuracy and confidence level. The underlying MAC layer of the protocols is slotted ALOHA. In specific, the reader sends a sequence of slots to the tags, and each tag responds in a slot according to its local random number. Kodialam et al. propose Unified Probabilistic Estimator (UPE) [5]. In UPE, each tag participates in the slots with a carefully chosen probability $p ,$ and the estimation is made using the number of empty and collision slots. Kodialam et al. present Enhanced Zero Based Estimator (EZB) in their follow-up work [6]. EZB shares similar strategy with UPE, while it only uses empty slots and probability p to compute the estimation. Qian et al. [7] propose Lottery Frame (LoF) Estimator, in which tags choose slot according to geometric distributed random numbers, making the number of slots O(logn). Zheng et al. [10] introduce a novel structure called Probabilistic Estimation Tree (PET) and further improve the estimation efficiency to O(loglogn). In [11], an estimation scheme Average Run based Tag estimator (ART) is designed. The authors attribute its efficiency to the non-trivial estimation metric it utilizes, i.e., the average run size of non-empty slots. Then, Zheng et al. [12] use a two-phase scheme Zero-One Estimator (ZOE) that achieves high efficiency. Recently, Chen et al. [13] gain deeper and fundamental insights into the counting problem and claim the importance of two-phase methodology in protocol design.

Some of the previous techniques [6]–[8], [10], [13] can be extended to estimate the set union cardinality, although they primarily target the simple counting scenario. They consider the response from a tag set as a bitmap, where the state of each slot represents a bit. The union estimation can be fulfilled by combining the bitmaps of each set in certain way. For example in [7] and [13], the bitmaps are merged using bitwise OR operation. However, those techniques are no longer applicable to set intersection and difference. In [15], a counting scheme called INformative Counting (INC) is proposed to estimate the intersection and difference size. However, INC is inefficient and more importantly, not extended to composite set expression estimation.

Besides probabilistic counting, a large amount of work in RFID tries to improve the efficiency of identifying tag IDs. Many anti-collision schemes have been designed, such as ALOHA-based schemes [20], [21] and tree-based schemes [22]. Apparently, we can derive the exact number of tags once tag IDs are collected. Although tag identification can address the composite counting problem, the efficiency is unacceptable for large-scale systems. Also, some work discusses the robustness and security issues of tag identification and counting in a more practical sense [23], since radio region of RFID reader is often irregular.

# III. PROBLEM FORMULATION

In this section, we formulate RFID composite counting problem. We consider multiple tag sets $S _ { 1 } , S _ { 2 } , . . . , S _ { m }$ . Each set contains a number of unknown tags to be interrogated by the reader(s) at certain location and time. Either location or time can be different among the sets to consider spatial and temporal diversity. Namely, the tags can be distributed in a vast area beyond a single reader’s coverage, thus multiple readers at different locations should be used. Besides, the tags can be mobile so that the reader captures different tags at different time. Given an application specific set expression E over sets $\{ S _ { i } | 1 \le i \le m \}$ and operators $\{ \cup , \cap , - \}$ , the objective of composite counting is to estimate the cardinality |E|. For example, $| E | = | ( S _ { 1 } \bigcup S _ { 2 } ) - ( S _ { 3 } \bigcap S _ { 4 } )$ |. We assume a back-end server with powerful processing capability, which is connected to the readers via high speed networks. The server is responsible for estimating |E| with the data reported by the readers.

We adopt the typical slotted ALOHA model for RFID communication [24]. Time period is divided into a sequence of slots. In each slot, the reader initializes communication by broadcasting commands and associated parameters. Then tags that participate in the slot respond their messages synchronously. Since the tags are incapable of sensing each other, they decide whether to participate depending on their local states, e.g., the received commands and stored information. The reader and tags simply exchange O(1) bits in one slot, as the tags are synchronized and their replies can be treated as a whole. A slot can fall into two categories according to the wireless channel state. If there is at least one tag responding, the corresponding slot is called non-empty slot. Otherwise the slot is empty.

Following the convention of RFID counting problem, there are two key metrics to evaluate the performance of composite counting, namely efficiency and accuracy. First, a desirable counting approach should be time efficient and scalable to a large amount of tags. As the readers and server are connected via high-speed networks, the communication cost between them can be neglected. We mainly consider the time of wireless communication between the reader and tags. Thus, a counting approach that requires fewer time slots and fewer bits in one slot would be more efficient. Second, counting output should accurately reflect the actual number of tags. Similar to previous probabilistic counting schemes [5]–[13], the accuracy of composite counting is described by (ε,δ)-approximation. Let $n = \left| E \right|$ and the estimate of n be ˆn. We say that ˆn is an (ε, δ)-estimate for n if $P r ( | \hat { n } - n | \leq \varepsilon n ) \geq 1 - \delta .$ . For example, when n = 1000, a (0.1,0.05)-approximation of n outputs a number in range [900,1100] with probability at least 0.95.

# IV. COMPOSITE COUNTING LOWER BOUNDS

In this section, we derive communication cost lower bounds for composite counting. The lower bound decides the minimum communication cost required to solve the composite counting problem. It provides guidelines for counting protocol design and helps to benchmark the proposed protocol. To measure the communication cost, we follow the conventional definition of communication complexity [25], which quantifies the amount of bits exchanged between two parties to collaboratively compute a function, e.g., counting the size of an expression. We will provide the lower bounds for counting union, intersection and difference between two sets, since they are basic components of composite counting.

1) Lower Bound for Set Union Counting: We aim at counting the union of two tag sets S and $S _ { 2 } ,$ which we call RFID set Union Counting problem (RUC). We use reduction to derive the complexity lower bound for RUC. Reduction is a commonly used approach to obtain the complexity of a problem. Specifically, if we wish to obtain the complexity of a hard problem A, we usually resort to another hard problem B. We say A can be reduced to B if a protocol to solve B could also be adopted as a building block to solve A. Consequently, problem A is no harder than B, and thus the complexity of A is a lower bound of B.

Here we choose a Two-party set Union Counting (TUC) problem as the hard problem B. The definition of TUC is given in Definition 1. We show that RUC can be reduced to TUC. Note that the models of RUC and TUC are different in two aspects, which hinders direct reduction. First, TUC has only two communication parties Alice and Bob. However, in $R U C ,$ we have more parties, namely the tags in $S _ { 1 }$ and $S _ { 2 } .$ , their associated readers and the back-end server. In addition, tags in $S _ { 1 }$ and $S _ { 2 }$ cannot communicate with each other. Since we focus on the communication cost between readers and tags, this model can be further simplified: we treat the backend server as a reader to directly communicate with tags in $S _ { 1 }$ and $S _ { 2 } ,$ as shown in Figure 2(a). Second, in TUC Alice and Bob know $S _ { 1 }$ and $S _ { 2 } .$ , whereas in RUC tags in $S _ { 1 }$ and $S _ { 2 }$ are distributed and their IDs are unknown. Given these discrepancies, we introduce an intermediate problems I to bridge the gap, which is defined in Definition 2. The reduction sequence is $R U C \to I \to T U C$ .

![](images/c3ab58b9538601b7885218f1b955941e63285b2437a2dbd38d4f70e4e947e8a0.jpg)



Fig. 2. The communication models of RUC, I and TUC.

Definition 1: In TUC, Alice and Bob each knows a set $S _ { 1 \subseteq }$ [n] and $S _ { 2 } \subseteq [ n ]$ , and they would like to derive $| S _ { 1 } \cup S _ { 2 } |$ by exchanging as few bits as possible, as shown in Figure 2(c).

Definition 2: I is a three-party communication problem, as shown in Figure 2(b). Alice and Bob each knows a set $S _ { 1 } \subseteq [ n ]$ and $S _ { 2 } \subseteq [ n ]$ , but they are not allowed to communicate with each other. The third party Carol aims to obtain $| S _ { 1 } | U S _ { 2 } |$ by communicating with Alice and Bob.

Without loss of generosity, we let the tag sets in RUC be subsets of [n] to be in line with the input of TUC and I. The following Lemma 1 gives the reduction from RUC to TUC. The proofs of all lemmas and theorems in this paper are left in the Appendix.

Lemma 1: The communication complexity of RUC is bounded by TUC from below.

Now, we derive a lower bound for TUC in Lemma 2, by leveraging a strong space lower bound for estimating the number of distinct elements (called $F _ { 0 } )$ in the union of two data streams [26]. These two problems are essentially the same since TUC also aims at counting the number of distinct elements within two sets. Additionally, the space lower bound in $F _ { 0 }$ estimation can be applied here since the space requirement in the data stream model is equivalent to the communication cost in communication complexity model.

Lemma 2: Any protocol for TUC with (ε, δ)-approximation must exchange $\Omega \big ( \frac { 1 } { \tt e ^ { 2 } } \big )$ ) bits between the two parties, for any $\begin{array} { r } { \mathfrak { E } = \Omega ( \frac { 1 } { \sqrt { n } } ) } \end{array}$ .

Lemma 1 and 2 naturally yield Theorem 1 below.

Theorem 1: Any protocol for RUC with (ε, δ)-approximation must use $\Omega ( \frac { 1 } { \tt e ^ { 2 } } )$ bits, for any $\begin{array} { r } { \mathfrak { E } = \Omega ( \frac { 1 } { \sqrt { n } } ) } \end{array}$ .

Theorem 1 gives a lower bound for union size estimation in composite counting.

2) Lower Bound for Set Intersection Counting: We would like to count the intersection of tag sets $S _ { 1 }$ and $S _ { 2 } ,$ , denoted as RFID set Intersection Counting problem (RIC). We assume tag IDs are subsets of [n] as before. Again, reduction is used to derive the communication lower bound for RIC. The hard problem B here we choose is a Two-party set Intersection Counting problem T IC, which is defined in Definition 3.

Definition 3: T IC is a two party communication problem, where Alice and Bob have $S _ { 1 } \subseteq [ n ]$ and $S _ { 2 } \subseteq [ n ]$ , respectively. They want to obtain $| S _ { 1 } \cap S _ { 2 } |$ by exchanging as few bits as possible.

RIC and T IC have different communication models. Namely, RIC has the model in Figure 2(a), while T IC has the model in Figure 2(c). So we use the same method as before to perform the reduction, and have the following lemma.

Lemma 3: The communication complexity of RIC is bounded by T IC from below.

Lemma 4 below shows an existing communication complexity lower bound for T IC [27].

Lemma 4: Any protocol for T IC with (ε, δ)-approximation must exchange $\Omega ( \textstyle { \frac { n } { | S _ { 1 } \bigcap S _ { 2 } | \varepsilon } } )$ bits between the two parties.

Then we easily obtain Theorem 2 from Lemma 3 and 4, which offers a lower bound for intersection estimation

Theorem 2: Any protocol for RIC with (ε, δ)-approximation must use $\Omega \big ( \frac { n } { | S _ { 1 } \cap S _ { 2 } | \varepsilon } \big )$ bits.

|  |3) Lower Bound for Set Difference Counting: The difference of two sets $S _ { 1 } - S _ { 2 }$ is simply $S _ { 1 } \cap \bar { S } _ { 2 }$ . Hence, we can apply all the results of set intersection counting, except that the  operator is replaced with . Denote the RFID set Difference Counting problem as RDC, and we have Theorem 3.

Theorem 3: Any protocol for RDC with (ε, δ)-approximation must use $\Omega ( { \frac { n } { | S _ { 1 } - S _ { 2 } | \varepsilon } } )$ bits.

# V. COMPOSITE COUNTING FRAMEWORK

In this section, we present the main design of the composite counting framework CCF. We show by leveraging set synopsis, we can accurately estimate the cardinality of union, intersection, difference and more generally, any composite set expression. We next design an efficient protocol that collects synopsis from tag sets to perform the estimation. The communication cost of our protocol is close to the lower bounds. A summary of notations are summarized in Table I.

# A. Synopsis-based Estimator

1) Why Synopsis: There are several reasons why we use synopsis to estimate. First, the communication cost of using original tag sets can be prohibitively high for large sets. The synopsis, however, can be considered as a small sample of the original tag set, which makes the estimation much more efficient. Second, synopsis effectively achieves composite counting despite its small size, which allows us to build a truly generic framework. At last, synopsis can be maintained and updated in real time, ensuring the flexibility of the framework.

2) Single Set Estimation: We start illustrating the estimation method from single set perspective. Consider a set S with n tags $\left\{ I D _ { 1 } , I D _ { 2 } , . . . , I D _ { n } \right\}$ . The aim is to estimate the number of tags n. The basic intuition is as follows. Assume that tag IDs in S are uniformly distributed in an interval $[ l , u ]$ . Let $S _ { ( k ) }$ be the k-th smallest tag ID in S. Due to the uniformity, the expected value of $S _ { ( k ) }$ is $\displaystyle { \dot { l } } + { \frac { u - l } { n } } k$ . Hence, we can utilize $S _ { ( k ) }$ to inversely deduce n. In specific, n can be estimated as $\frac { ( \dot { u } - l ) k } { S _ { ( k ) } - l }$ . In most cases, we do not have such distribution properties. Hash functions, however, can bridge the gap and transform the tag IDs with any distribution to uniform distribution. In particular, each tag in $S$ can compute a hash value $h ( I D )$ using a uniform hash function $h : S  [ D ]$ and its ID, where D is the hash size. After normalization, the values $h ( I D _ { 1 } ) / D , h ( I D _ { 2 } ) / D , . . . , h ( I D _ { n } ) / D$ can be approximately viewed as uniformly distributed in $[ 0 , 1 ]$ . In order to avoid hash collisions, the hash space should be $O ( n ^ { 2 } )$ (see the birthday paradox [28]). With $\overset { \vartriangle } { \boldsymbol { D } } = O ( n ^ { 2 } )$ , we can ensure that for any $I D _ { i }$ and $I D _ { j } ~ ( i \neq j ) , h ( I D _ { i } ) \neq h ( I D _ { j } )$ with large probability. In the rest of this paper, we always use a sufficiently large hash size and do not consider hash collisions. Let the k-th smallest normalized hash value be $h _ { ( k ) }$ . The set cardinality n can be unbiasedly estimated as $\begin{array} { r } { \hat { n } = \frac { k - 1 } { h _ { ( k ) } } } \end{array}$ h(k) , according to the previous analysis. For example, if the 4-th smallest normalized hash value $h _ { ( 4 ) }$ is 0.3, then there are approximately $\frac { 3 } { 0 . 3 } = 1 0$ tags in the set.

TABLE I TABLE OF NOTATIONS 

<table><tr><td>Notation</td><td>Meaning</td></tr><tr><td> $h(S)$ </td><td>hash set of  $S$  (normalized)</td></tr><tr><td> $h_{(k)}$ </td><td>the  $k$ -th smallest value in  $h(S)$ </td></tr><tr><td> $T_S$ </td><td>synopsis of  $S$ </td></tr><tr><td> $k$ </td><td>synopsis size</td></tr><tr><td> $n_{\bigcup}$ </td><td> $|S_1 \cup S_2|$ </td></tr><tr><td> $n_{\bigcap}$ </td><td> $|S_1 \cap S_2|$ </td></tr><tr><td> $n_{-}$ </td><td> $|S_1 - S_2|$ </td></tr><tr><td> $n_E$ </td><td>size of general set expression  $E$ </td></tr></table>

To achieve $( \varepsilon , \delta )$ -approximation of n, the value of k should be determined accordingly. We have the following lemma that decides k.

Lemma 5: To achieve (ε, δ)-estimate for n, $\begin{array} { r } { k = \Theta \big ( \frac 1 { \varepsilon ^ { 2 } } l n \frac 1 8 \big ) } \end{array}$

3) Set Union Estimation: The estimation techniques proposed above can be naturally applied to estimate the union of two tag sets. The problem is to estimate $n _ { \mathrm { U } }$ given $S _ { 1 }$ and $S _ { 2 } .$ . For set $S _ { i } ( i = 1 , 2 )$ , let $T _ { S _ { i } }$ be the k smallest hash values in $h ( S _ { i } ) . ~ T _ { S _ { i } }$ is defined as the synopsis of $S _ { i } ,$ and its size k is usually smaller than $| S _ { i } | . ~ T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ are obtained using the same hash function.

Lemma 6: The k smallest values in $T _ { S _ { 1 } } \cup T _ { S _ { 2 } }$ comprise the synopsis of $S _ { 1 } \bigcup S _ { 2 } ,$ i.e., $T _ { ( S _ { 1 } \cup S _ { 2 } ) }$ .

By Lemma 6, we can use $\operatorname { \dot { \cal h } } _ { ( k _ { \lfloor \rfloor } ) } = m a x \{ T _ { ( S _ { 1 } \cup S _ { 2 } ) } \}$ to estimate $n _ { \mathrm { U } } .$ , as in the single set scenario. Hence, we have the following estimator

$$
\hat {n} _ {\bigcup} = \frac {k - 1}{h _ {(k _ {\bigcup})}} \tag {1}
$$

This method can be illustrated by a simple example. Assume $k ~ = ~ 4 , ~ T _ { ( S _ { 1 } ) } ~ = ~ \{ 0 . 0 1 , 0 . 0 3 , 0 . 0 5 , 0 . 0 7 \}$ and $\begin{array} { r l r } { T _ { ( S _ { 2 } ) } } & { { } = } & { \left\{ 0 . 0 3 , 0 . 0 4 , 0 . 0 7 , 0 . 0 8 \right\} } \end{array}$ . Then $\begin{array} { r l } { T _ { ( S _ { 1 } \bigcup S _ { 2 } ) } } & { { } = } \end{array}$ $\{ 0 . 0 1 , 0 . 0 3 , 0 . 0 4 , 0 . 0 5 \}$ and $h _ { ( k _ { \bigcup } ) } = 0 . 0 5$ . Hence, $| \dot { S } _ { 1 } \dot { \cup } \dot { S _ { 2 } } |$ can

![](images/69892de2792b12a58f2fa047b2c77a3e3bbad283d83489d4a3cf517079485a15.jpg)



Fig. 3. A motivating example of sampling-based estimation. B is a subset of A. As is a simple random sample drawn from A. $\frac { \left| B \bigcap A _ { s } \right| } { \left| A _ { s } \right| }$ can be used to estimate the ratio $\frac { | B | } { | A | }$ .

be estimated as $3 / 0 . 0 5 = 6 0 $

According to Lemma $5 ,$ we obtain Theorem 4 that gives the size of synopsis for (ε, δ)-estimate.

Theorem 4: To achieve (ε,δ)-estimate for $n _ { \bigcup } , \quad k _ { \bigstar } =$ $\Theta \big ( \textstyle \frac { 1 } { \varepsilon ^ { 2 } } l n \frac { 1 } { \delta } \big )$ .

4) Set Intersection Estimation: Consider two tag sets $S _ { 1 }$ and $S _ { 2 }$ and their synopsis $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ . The objective is to estimate $n _ { \bigcap }$ based on $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ . We represent $n _ { \bigcap }$ by the product of two terms $n _ { \bigcap } = n _ { \bigcup } J ,$ , where $\begin{array} { r } { J = \frac { n _ { \bigcap } } { n _ { \lfloor \rfloor } } } \end{array}$ is called the Jaccard similarity between $S _ { 1 }$ and $S _ { 2 }$ . Thus, $n _ { \bigcap }$ can be estimated as follows.

$$
\hat {n} _ {\cap} = \hat {n} _ {\cup} \hat {J} \tag {2}
$$

In fact, if we have $( \varepsilon / 3 , \delta )$ -estimate for both J and $^ { n _ { \mathrm { U } } , }$ we can obtain $( \varepsilon , \delta )$ -estimate for $n _ { \bigcap }$ . The reason is given in Equation 3-4.

$$
(1 - \varepsilon / 3) ^ {2} n _ {\bigcup} J \leq \hat {n} _ {\bigcup} \hat {J} \leq (1 + \varepsilon / 3) ^ {2} n _ {\bigcup} J \tag {3}
$$

which infers

$$
(1 - \varepsilon) n _ {\bigcup} J \leq \hat {n} _ {\bigcup} \hat {J} \leq (1 + \varepsilon) n _ {\bigcup} J \tag {4}
$$

The method to estimate $^ { n } \cup$ with $( \varepsilon / 3 , \delta )$ -accuracy has been explained earlier. Now we show how to give $( \varepsilon / 3 , \delta )$ -estimate for the ratio J using $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ . The key point is based on random sampling. Consider a motivating example in Figure 3, where we have set A and its subset $B \subset A$ , and wish to estimate the ratio $\frac { | B | } { | A | }$ . If we draw a simple random sample1 $A _ { s }$ from A, then $\frac { | B \bigcap { \dot { A } } _ { s } | } { \left| A _ { s } \right| }$ can be used to approximate the ratio $\frac { | B | } { | A | }$ . Back to our case, the synopsis $T _ { S _ { 1 } \cup S _ { 2 } }$ is virtually a simple random sample drawn from $S _ { 1 } \cup S _ { 2 } .$ but with the tag IDs mapped to hash values. Hence, a reasonable estimate for J is

$$
\hat {J} = \frac {\left| T _ {S _ {1} \cup S _ {2}} \cap h (S _ {1}) \cap h (S _ {2}) \right|}{\left| T _ {S _ {1} \cup S _ {2}} \right|} \tag {5}
$$

$$
= \frac {\left| T _ {S _ {1} \cup S _ {2}} \cap T _ {S _ {1}} \cap T _ {S _ {2}} \right|}{k} \tag {6}
$$

The derivation from Equation 5 to 6 follows from the fact that for any element in $T _ { S _ { 1 } \cup S _ { 2 } }$ , if it is in $h ( S _ { i } ) ( i = 1 , 2 )$ , it must also be in $T _ { S _ { i } }$ and vice versa. Substituting Equation 1 and 6

to Equation 2, we have

$$
\hat {n} _ {\cap} = \frac {\left| T _ {S _ {1} \cup S _ {2}} \cap T _ {S _ {1}} \cap T _ {S _ {2}} \right|}{k} \frac {k - 1}{h _ {(k \cup)}} \tag {7}
$$

Now we decide the synopsis size k that ensures (ε, δ)-approximation of $n _ { \bigcap } ,$ and get the following theorem.

Theorem 5: To achieve (ε,δ)-estimate for $n _ { \mathord { \left/ { \vphantom { n _ { \Theta } } } \right. \kern - delimiterspace } \mathrm { \Gamma } } ,$ k is at least $\Theta \big ( \frac { 1 } { \tt g ^ { 2 } J } l n \frac { 1 } { \tt \bar { \delta } } \big )$ .

5) Set Difference Estimation: This time, we wish to estimate n with $T _ { S _ { 1 } }$ and $T _ { S _ { 2 } }$ . Estimating difference is essentially similar to estimating intersection, since $S _ { 1 } - S _ { 2 } = S _ { 1 } \bigcap \bar { S } _ { 2 }$ . Therefore, we just apply the results in the last section without further elaboration. The estimator $\hat { n } _ { - }$ for $n _ { - }$ is

$$
\hat {n} _ {-} = \frac {\left| T _ {S _ {1} \cup S _ {2}} \cap (T _ {S _ {1}} - T _ {S _ {2}}) \right|}{k} \frac {k - 1}{h _ {(k _ {\cup})}} \tag {8}
$$

Theorem 6 below directly follows from Theorem 5.

Theorem 6: To achieve (ε, δ)-estimate for n , k is at least $\Theta \big ( \frac { 1 } { \tt g ^ { 2 } C } l n \frac { 1 } { \tt \delta } \big )$ , where $\begin{array} { r } { C = \frac { n _ { - } } { n _ { | | } } . } \end{array}$ .

6) General Expression Estimation: We now consider estimating the cardinality of general set expression E. Assume E contains m sets $S _ { 1 } , S _ { 2 } , . . . , S _ { m }$ . We then express $| E |$ as $\frac { | E | } { | \bigcup _ { i = 1 } ^ { m } S _ { i } | } | \bigcup _ { i = 1 } ^ { m } S _ { i } | . \ | \bigcup _ { i = 1 } ^ { m } S _ { i } |$ can be estimated using its synopsis $T _ { \mathrm { U } S _ { i } }$ , which is a trivial extension of estimating the union of two sets. Estimating the ratio R = |E| -m Si $\begin{array} { r } { R = \frac { \left| E \right| } { \left| \bigcup _ { i = 1 } ^ { m } S _ { i } \right| } } \end{array}$ is an extension of estimating J and C. Denote $E _ { T }$ | i=1 |as the set with each $S _ { i }$ in E replaced with its synopsis $T _ { S _ { i } }$ . For example, if $E =$ $( S _ { 1 } \bigcup S _ { 2 } ) - ( S _ { 3 } \bigcap S _ { 4 } )$ , we have $E _ { T } = \overset { \cdot } { ( } T _ { S _ { 1 } } \bigcup T _ { S _ { 2 } } ) - ( T _ { S _ { 3 } } \bigcap T _ { S _ { 4 } } )$ . We get the estimator

$$
n _ {\hat {E}} = \frac {\left| E _ {T} \cap T _ {\bigcup_ {i = 1} ^ {m} S _ {i}} \right|}{k} \frac {k - 1}{h _ {(k _ {\bigcup})}} \tag {9}
$$

where $h _ { ( k _ { \parallel } ) } = m a x \{ T _ { \bigcup S _ { i } } \}$ . To achieve (ε, δ)-guarantee, we obtain Theorem 7 below, which also follows from Theorem 5.

Theorem 7: To achieve (ε,δ)-estimate for $n _ { E } ,$ , k is at least $\Theta \big ( \frac { 1 } { \tt g ^ { 2 } R } l n \frac { 1 } { \tt \bar { \delta } } \big )$ .

# B. Efficient Composite Counting Protocol

In this section, we design an efficient composite counting protocol in RFID systems, which implements the algorithms in the last section. We analyze the communication cost of our protocol and compare with the lower bounds.

1) Protocol Design: To achieve the synopsis based estimation, we need the k smallest hash values of each tag set. We focus on explaining how to obtain the smallest hash value (without normalization), since other k  1 hash values can be obtained similarly. Our protocol is based on the slotted ALOHA communication model. It exploits binary search to obtain the smallest hash value.

We first use an illustrative example to express the general idea and then formally describe the protocol details. Assume we have 4 tags in a set. Their hash values are 4 bits in binary format, namely 0100, 0101, 0111, and 1110. The reader continuously sends 1-bit messages to the tags to reduce the search space. Initially, it sends a bit $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ to the tags. The 4 tags store $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ in their memory as prefix string $p r e f ,$ and check whether $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ is a prefix of their hash values. If so, they respond the reader with a bit ’1’. Obviously, tags with hash values 0001, 0011, and 0100 will respond. Thus, the reader detects a non-empty slot and is convinced that there exists at least one hash value starting with $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ . Further, the reader sends another $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ to match the second bit in the hash values. Again, the tags append the received $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ to pre f and get ’00’. Then they use ’00’ to do prefix matching. But this time, no successful matching exists. So the reader will detect an empty slot. After that, the reader tries $\ ' _ { 1 } '$ still for the second bit in hash values. All tags change $p r e f$ to $\mathbf { \Phi } _ { 0 1 } \cdot \mathbf { \Phi } _ $ (actually, all tags should change the last bit in pre f to $\ ' _ { 1 } '$ if they receive $\mathbf { \vec { \tau } } _ { 1 } \mathbf { \vec { \tau } } )$ . The procedure continues until the reader finds 0100 as the smallest hash value. If we still need to seek the second smallest hash value, we should keep the tag with 0100 silent, clear $p r e f$ in all tags’ memory, and repeat the procedure above. When the k hash values are collected, we activate those tags that are kept silent.

Algorithm 1: The synopsis collection algorithm for reader.   
Input : Synopsis size k, hash value length l (in binary).
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
    | Respond reader with '1'
    else
    | Keep silent in this slot
    end
    i ← i + 1
    if i = l then
    | i ← 0
    if pref = h(ID) then
    | Keep silent until activated
    end
    Clear pref
    end
end

![](images/66fe7529144a5e2003236f218e44ca9d0cc7a98b91f49b7bb2f468198306470d.jpg)



Fig. 4. USRP and 4 WISP computational tags.

The detailed synopsis collection protocol for reader and tags are shown in Algorithm 1 and 2.

2) Performance Analysis: We analyze the communication cost of our synopsis collection protocol. Obviously, for each $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ in the target hash value, the reader spends 1 slot. For each $\ ' _ { 1 } '$ in the smallest hash value, the reader spends 2 slots: first with $\overrightarrow { \mathbf { \nabla } } 0 ^ { \circ }$ and then with $\ ' _ { 1 } '$ . Hence, the number of slots to collect one of the k smallest hash values is $\Theta ( l )$ , where l is the length of hash values in binary format. Considering that there are $O ( 1 )$ bits exchanged in each slot, the communication cost of our protocol for one tag set is $\Theta ( l )$ bits. Recall that the hash space should be sufficiently large to avoid collisions. In terms of two-set composite counting, the hash space should be $n _ { \mathrm { U } } ^ { 2 }$ to avoid collision within $S _ { 1 } \cup S _ { 2 }$ . Thus, $\Theta ( l ) = \Theta ( l o g n _ { \bigcup } )$ . Then the communication overhead of estimating $| S _ { 1 } o p S _ { 2 } |$ where $o p \in \{ \cup , \cap , - \}$ should be $\Theta ( k l o g n _ { \bigcup } )$ , where k is the synopsis size. Incorporating the the foregoing analysis about k, we have the following results.

Theorem 8: In our protocol, the communication cost of estimating $n _ { \mathrm { U } }$ with (ε, δ)-approximation is $\Theta \big ( \frac { l o g n _ { \bigcup } } { \mathfrak { E } ^ { 2 } } l n \frac { 1 } { \delta } \big )$ ( log n-ε2 ln 1δ ).

By Theorem 1, the lower bound for estimating $n _ { \mathrm { U } }$ with (ε, δ)-approximation is $\Omega \big ( \frac { 1 } { \tt e ^ { 2 } } \big )$ , when $\begin{array} { r } { \mathfrak { E } = \Omega \big ( \frac { 1 } { \sqrt { n _ { \bigcup } } } \big ) } \end{array}$ . We observe the overhead of our protocol is within a small logarithm factor from the lower bound.

Theorem 9: In our protocol, the communication overhead of estimating $n _ { o p }$ with (ε, δ)-approximation is $\Theta \big ( \frac { n _ { \bigcup } } { n _ { o p } } \frac { l o g n _ { \bigcup } } { \varepsilon ^ { 2 } } l n \frac { 1 } { \ S } \big )$ nop where $o p \in \{ \cap , - \}$ .

By Theorem 2, the lower bound for estimating $n _ { o p } ( o p \in$ $\{ \cap , - \} )$ with (ε, δ)-approximation in RFID systems is $\Omega ( \frac { n _ { \bigcup } } { \varepsilon n _ { o p } } )$ ε nop . Thus, the overhead of our protocol is also within a small logarithm factor from the lower bound.

3) Synopsis update: Practically, we may want to update the synopsis of tag sets in real time to cope with mobile tags. Update can be easily achieved by periodically running the protocol. It is up to the application demands whether to merge the old and new synopsis or simply use the new one.

# VI. IMPLEMENTATION

We implement the prototype of CCF using USRP softwaredefined reader and WISP computational tags, as shown in Figure 4. We briefly introduce USRP reader and WISP below. USRP reader: We adopt a USRP implementation of EPC Gen-2 RFID reader [29], and customize it to the protocol described in Algorithm 1. We use RFX900 daughter board and Laird S9028 circular polarized antenna with the USRP.

![](images/36e07fbdeca26e91cc6bd08817cb0a36206ac9714ad600d98932c7ef4fbe25f5.jpg)



Fig. 5. The communication between the reader and WISP in one round of identification. Query and ACK are reader signals, while RN16 and EPC are tag signals

![](images/82e75c2e7a5c213e3753bea861fc5cc0db005d0a6d2c6399fcabbf6c1812a85b.jpg)



Fig. 6. The communication between the reader and 4 WISPs when searching for the smallest hash value 0100. Search 0(1) means the BIT field in SEARCH is set to 0(1).The first SEARCH command is followed by the superposition of two F16s, so the slot is non-empty. The second SEARCH command is followed by an empty slot. The fourth SEARCH command is followed by only one F16, so the slot is non-empty.

The reader is connected to a laptop via Gigabit Ethernet. All the experiments are run at carrier frequency of 900MHz.

WISP tags: We implement the protocol in Algorithm 2 using WISP 4.1DL computational tags. WISP is an open source EPC Gen-2 RFID tag that includes a programmable 16 bit M“““‘SP430 microcontroller. WISP is battery-less and harvests energy from reader’s signal like ordinary passive tags. WISP implements most parts of EPC Gen-2 standard, such as decoding the reader’s commands, generating a random number, responding its ID etc. Since CCF requires a slight modification to the EPC Gen-2 standard, we incorporate the new features in our protocol into the original WISP code.

In EPC Gen-2 standard, the reader communicates with tags using a procedure as follows. The reader initiates communication by sending a command that could be QUERY, READ, SELECT, etc. We focus on the QUERY command, which the reader uses to identify the tag ID. It is important because a new SEARCH command in our protocol is designed based on QUERY. Upon receiving the QUERY command, tags respond a 16-bit random number RN16. Then the reader sends an ACK to the tag, and waits for the tag ID (EPC code). The whole communication procedure is plotted in Figure 5.

In CCF, we design the SEARCH command based on QUERY as depicted in Figure 7(b), and add it into the command set. We keep the PHY/MAC field of QUERY in SEARCH, since they are vital for the reader to negotiate the uplink communication parameters with the tags. We create a specialized field BIT in SEARCH that corresponds to the 1-bit message in the synopsis collection protocol. To collect the synopsis, the reader repeatedly sends the SEARCH command until it finds the k smallest hash values. When receiving the SEARCH command, each tag performs prefix matching, and issues a short response if the matching is successful. To be compatible with the original WISP code and be robust to channel error, we use a Fixed 16-bit string (F16) as the short response here. The difference between F16 and RN16 is that F16 is the same for all tags. Since tags are synchronized by the reader and their F16s are identical, the reader is allowed to robustly differentiate a non-empty slot with an empty slot due to constructive interference [30]. In addition, tags are not required to report their IDs after SEARCH. Figure 6 plots the signals to search the smallest hash value in 4 WISPs using our prototype. We preload the 4-bit hash values 0100, 0110, 1100, and 1110 in the 4 WISPs, respectively. After 5 rounds, the smallest hash value 0100 can be found by the reader.

<table><tr><td></td><td>Command</td><td>PHY/MAC</td><td>Session</td><td>Q</td><td>CRC-5</td></tr><tr><td># of bits</td><td>4</td><td>4</td><td>5</td><td>4</td><td>5</td></tr></table>

(a) QUERY command 

<table><tr><td></td><td>Command</td><td>PHY/MAC</td><td>BIT</td><td>CRC-5</td></tr><tr><td># of bits</td><td>4</td><td>4</td><td>1</td><td>5</td></tr></table>

(b) SEARCH command   
Fig. 7. The packet formats of QUERY and SEARCH command.

Although our protocol can be implemented in a real communication system, there is deficiency to thoroughly evaluate the performance of CCF using this prototype. The communication distance between URSP and WISP is limited, which makes large-scale counting difficult to experiment. Therefore, we turn to simulations to further investigate CCF.

# VII. EVALUATION

We conduct extensive simulations using real-world dataset to investigate the accuracy and efficiency of CCF. The dataset used is called the AMD Hope RFID dataset [31], which contains information collected at the ”Hackers On Planet Earth” (HOPE) conference in 2008. The conference distributes RFID badges (tags) to the attendees that can uniquely identify and track them in the conference. According to their own interest, attendees may visit difference conference rooms which hold various talks and events. Each tuple in the dataset includes the snapshot timestamp, tag ID, and conference room the attendee visits. There are totally 21 rooms equipped with RFID readers, and each room has a unique name corresponding to the event topic in it, such as Turing and Engressia. We treat the attendees have visited each room as a set. In this case study, we randomly selects 9 out of 21 rooms and count the number of attendees of various set expressions among them.

In Table II, we summarize the rooms we choose and the expressions we use. For the expressions involving two rooms, we use their initials as abbreviation. For example, expressions between room Turing and Engressia are represented as TE for short. For other complex expressions including 4 sets (the last three tuples in Table II), we use E1, E2, and E3 for short. Each expression has a specific meaning. For instance, E3 denotes the people are interested in Turing or Engressia but not both Hopper and 18thFloor. Table III lists the actual number of attendees of all expressions as ground truth.

TABLE II DATASET CHARACTERISTICS 

<table><tr><td>Room combination</td><td>Abbr.</td></tr><tr><td>Turing  $\bigcup (\cap)$  Engressia</td><td>TE</td></tr><tr><td>Hopper  $\bigcup (\cap)$  18thFloor</td><td>H1</td></tr><tr><td>Hackerspace  $\bigcup (\cap)$  Phones</td><td>HP</td></tr><tr><td>Turing – AMD</td><td>TA</td></tr><tr><td>Engressia – Art</td><td>EA</td></tr><tr><td>Hopper – Radio</td><td>HR</td></tr><tr><td>(Turing  $\bigcup$  AMD – Art)  $\cap$  Engressia</td><td>E1</td></tr><tr><td>(Turing–Art–AMD)  $\bigcup$  Hopper</td><td>E2</td></tr><tr><td>(Turing  $\bigcup$  Engressia) – (Hopper  $\cap$  Art)</td><td>E3</td></tr></table>

TABLE III GROUND TRUTH 

<table><tr><td></td><td>TE</td><td>H1</td><td>HP</td></tr><tr><td>Union</td><td>1054</td><td>1112</td><td>1147</td></tr><tr><td>Intersection</td><td>755</td><td>1051</td><td>982</td></tr><tr><td></td><td>TA</td><td>EA</td><td>HR</td></tr><tr><td>Difference</td><td>420</td><td>391</td><td>466</td></tr><tr><td></td><td>E1</td><td>E2</td><td>E3</td></tr><tr><td>Expression</td><td>349</td><td>1075</td><td>512</td></tr></table>

# A. Simulation settings and comparison protocols

In AMD Hope dataset, tag IDs are in range [0, 10,000]. Hence, each ID can be encoded in 14 bits. According to the EPCGlobal C1G2 standard, a slot to transmit a 14-bit ID takes 0.9ms. A slot containing a 1-bit short response is 0.4ms. The hash size is set to 100,000, or 17 bits in binary form. All simulation instances are repeated 150 runs, unless otherwise specified.

Since tag identification is a naive counting method, we use it as comparison for all expressions. Also, we compare CCF with existing schemes that only work in specific type of expressions. We compare with the most efficient protocol so far — SRCM [13] in union estimation. INC [15] is chosen for comparison in intersection and difference estimation. Note that the protocols for comparison cannot achieve generic composite counting as CCF.

# B. Accuracy

We study the estimation accuracy of CCF with various synopsis size k. Consistent with previous work, we use relative error as the accuracy metric. Relative error is defined as $| { \hat { n } } - n | / n ,$ , where ˆn is the estimate and n is the actual expression size.

Figure 8 depicts the estimation accuracy of various kinds of expressions while different synopsis sizes k are applied. For each type of expression, we select three instances from the dataset. The figures show that one can always improve the estimation accuracy by increasing the synopsis size, which apparently incurs more communication overhead. Figure 8(a)

![](images/c0671176d5a2bd06e71ace9d1e3cb9159329ff600ae2ed6fd1a4ccb8ed7256f7.jpg)



(a) union estimation

![](images/f111545be843c5063c7c7251b48e18a63e9340f87a2c0e5273e9c758c327fc6e.jpg)



(b) intersection estimation

![](images/1084fed661109112c08832faea0507f1c8fc70d9b597c30741ad1095a3ad2fee.jpg)



(c) difference estimation

![](images/f8a466538729b1b000dcc66b3e7f4007d982a9f48c00ad8c74a166287c172642.jpg)



(d) composite expression estimation

Fig. 8. Evaluation of estimation accuracy under different set expressions and synopsis sizes.   
![](images/3e561f72f52356f2794f5eaf9dcc05ee3808a57e4aad01fc6ec7af3c4959cb84.jpg)



(a) union estimation

![](images/c21c78a2702ed32103414a086d236c4f84d15bcaab032d08d395d5c723c69f4e.jpg)



(b) intersection estimation

![](images/d716bc79f3f2caef66a92a6e9b1f4a414652be0dbf68294655e54df28727f461.jpg)



(c) difference estimation

![](images/e6f8cfebf30c023458a614d7412985edf6eee2470a024a78bea989158690cab9.jpg)



(d) composite expression estimation   
Fig. 9. Evaluation of estimation time to ε = 0.1 under different set expressions.

suggests that synopsis size of 100 is enough to achieve relative error rate below 10% when counting more than 1,000 people. Moreover, as shown by TE in Figure 8(b), EA in Figure 8(c) and E1 in Figure 8(d), we need larger synopsis to estimate a smaller expression size to the same accuracy level. This is consistent with our theoretical analysis. For example, to estimate |E1| = 349 to relative error of 10%, the synopsis size k should be as least 150. In contrast, to estimate E2 = 512, k = 100 will achieve the same accuracy.

# C. Communication time

We compare the communication time of CCF with recent estimation protocols given the same accuracy requirement. Here we fix the relative error ε = 0.1, which is sufficiently accurate for many applications. Figure 9 plots the total time required to estimate the size of various expressions to relative error 0.1. We observe from Figure 9(a) that the cost of CCF is close to the SRCM protocol—the best protocol to estimate the union size so far (actually SRCM is near optimal). However, SRCM is unable to estimate intersection and difference size, let alone other complex expressions. In Figure 9(b)-9(c), we find that CCF is more efficient than the existing protocol INC, when estimating intersection and difference size. More precisely, the estimation time of INC is 2.4 and 5.3 the time of CCF in average when estimating intersection and difference, respectively. Furthermore, we notice that CCF is far more efficient than direct identification. The reason is that deterministic identification requires tags to transmit the entire ID, which takes much longer than a short response. Also, identification involves all tags whereas CCF only uses a much smaller synopsis.

# VIII. CONCLUSION

In this paper, we formally introduce the composite counting problem in RFID systems, and obtain the lower bounds on its communication cost. We propose a generic composite counting framework (CCF), which is able to estimate the cardinality of any set expression with desired accuracy. Desirably, the communication cost of CCF is within a small factor from the lower bounds. We implement a prototype system using USRP reader and WISP computational tags, and conduct simulations to evaluate the performance of CCF. The experimental results show that our framework is generic, accurate and efficient.

# IX. ACKNOWLEDGEMENT

This study is supported in part by the NSFC Distinguished Young Scholars Program under Grant No. 61125202, and the NSFC under Grant No. 61103187. We also would like to acknowledge the support from the USRP2reader codes from the Open RFID Lab (ORL) project [32].

# REFERENCES

[1] L. Ni, Y. Liu, Y. Lau, and A. Patil, “Landmarc: Indoor location sensing using active rfid,” in Proceedings of IEEE Percom, 2003.   
[2] R. Angeles, “Rfid technologies: Supply-chain applications and implementation issues,” Information Systems Management, vol. 22, no. 1, pp. 51–65, 2005.   
[3] C. Tan, B. Sheng, and Q. Li, “How to monitor for missing rfid tags,” in Proceedings of ICDCS, 2008.   
[4] “Advancements and prospects of forward directional antennas for compact handheld rfid readers,” http://cdn.intechopen.com/pdfs/ 44990/InTech-Advancements and prospects of forward directional antennas for compact handheld rfid readers.pdf.   
[5] M. Kodialam and T. Nandagopal, “Fast and reliable estimation schemes in rfid systems,” in Proceedings of Mobicom, 2006.   
[6] M. Kodialam, T. Nandagopal, and W. Lau, “Anonymous tracking using rfid tags,” in Proceedings of Infocom, 2007.   
[7] C. Qian, H. Ngan, Y. Liu, and L. M. Ni, “Cardinality estimation for large-scale rfid systems,” Parallel and Distributed Systems, IEEE Transactions on, vol. 22, no. 9, pp. 1441–1454, 2011.

[8] H. Han, B. Sheng, C. Tan, Q. Li, W. Mao, and S. Lu, “Counting rfid tags efficiently and anonymously,” in Proceedings of Infocom, 2010.   
[9] T. Li, S. Wu, S. Chen, and M. Yang, “Energy efficient algorithms for the rfid estimation problem,” in Proceedings of Infocom, 2010.   
[10] Y. Zheng and M. Li, “Pet: Probabilistic estimating tree for large-scale rfid estimation,” Mobile Computing, IEEE Transactions on, vol. 11, no. 11, pp. 1763–1774, 2012.   
[11] M. Shahzad and A. Liu, “Every bit counts: fast and scalable rfid estimation,” in Proceedings of Mobicom, 2012.   
[12] Y. Zheng and M. Li, “Zoe: Fast cardinality estimation for large-scale rfid systems,” in Proceedings of Infocom, 2013.   
[13] B. Chen, Z. Zhou, and H. Yu, “Understanding rfid counting protocols,” in Proceedings of Mobicom, 2013.   
[14] K. Finkenzeller et al., RFID handbook: Fundamentals and applications in contactless smart cards, radio frequency identification and near-field communication. Wiley, 2010.   
[15] W. Gong, K. Liu, X. Miao, Q. Ma, Z. Yang, and Y. Liu, “Informative counting: fine-grained batch authentication for large-scale rfid systems,” in Proceedings of MobiHoc, 2013.   
[16] “Gnuradio tookit,” http://gnuradio.org/redmine/projects/gnuradio/wiki.   
[17] “Wisp: Wireless identification and sensing platform,” http://www.seattle. intel-research.net/WISP.   
[18] “Epc radio-frequency identity protocols class-1 generation-2 uhf rfid protocol for communications at 860mhz-960mhz,” http://www.gs1.org/ gsmp/kc/epcglobal/uhfc1g2/uhfc1g2 1 2 0-standard-20080511.pdf, 2008.   
[19] W. Gong, K. Liu, X. Miao, and H. Liu, “Arbitrarily accurate approximation scheme for large-scale rfid cardinality estimation,” in Proceedings of Infocom, 2014.   
[20] S. Lee, S. Joo, and C. Lee, “An enhanced dynamic framed slotted aloha algorithm for rfid tag identification,” in Proceedings. of Mobiquitous, San Diego, USA, 2005.   
[21] H. Liu, W. Gong, X. Miao, K. Liu, and W. He, “Towards adaptive continuous scanning in large-scale rfid systems,” in Proceedings of Infocom, 2014.   
[22] J. Myung and W. Lee, “Adaptive splitting protocols for rfid tag collision arbitration,” in Proceedings of MobiHoc, Florence, Italy, 2006.   
[23] S. Chen, Y. Chen, and W. Trappe, “Inverting systems of embedded sensors for position verification in location-aware applications,” Parallel and Distributed Systems, IEEE Transactions on, vol. 21, no. 5, pp. 722– 736, 2010.   
[24] J. R. Cha and J. H. Kim, “Dynamic framed slotted aloha algorithms using fast tag estimation method for rfid system,” in Proceedings of CCNC, Las Vegas, USA, 2006.   
[25] E. Kushilevitz and N. Nisan, Communication complexity. Cambridge university press, 2006.   
[26] D. Woodruff, “Optimal space lower bounds for all frequency moments,” in Proceedings of SODA, 2004.   
[27] S. Ganguly, M. Garofalakis, and R. Rastogi, “Tracking set-expression cardinalities over continuous update streams,” The VLDB Journal, vol. 13, no. 4, pp. 354–369, 2004.   
[28] “Birthday problem,” http://en.wikipedia.org/wiki/Birthday problem.   
[29] “Gen 2 rfid tools,” https://www.cgran.org/wiki/Gen2.   
[30] Y. Wang, Y. He, X. Mao, Y. Liu, Z. Huang, and X. Li, “Exploiting constructive interference for scalable flooding in wireless networks,” in Proceedings of Infocom, 2012.   
[31] “Amd hope rfid data,” http://networkdata.ics.uci.edu/data.php?d= amdhope.   
[32] “Open rfid lab,” http://pdcc.ntu.edu.sg/wands/orl.   
[33] B. C. Arnold, N. Balakrishnan, and H. H. N. Nagaraja, A first course in order statistics. Siam, 1992, vol. 54.   
[34] M. Mitzenmacher and E. Upfal, Probability and computing: Randomized algorithms and probabilistic analysis. Cambridge University Press, 2005.

# X. APPENDIX

# Proof for Lemma 1

The proof has two steps. First, the communication cost of RUC is no lower than I. The reason is that Alice and Bob in I know their sets exactly, whereas $S _ { 1 }$ and S2 are unknown in RUC. Hence, if RUC can be solved using some protocol, I can be solved in exactly the same way. Second, the communication overhead of I is no lower than TUC. The reason goes as follows. If there is a protocol that solves I, we redirect all bits that flow from Alice to Carol in this protocol to Bob. Thus, Bob can count $| S _ { 1 } | U S _ { 2 } |$ locally, and then sends O(1) bits to Alice to inform her the result. Thus, TUC can be solved with no more bits than I. Combining the two conclusions above, we obtain that the communication overhead of RUC is no lower than TUC.

# Proof for Lemma 5

$$
\begin{array}{l} P \{| \hat {n} - n | \leq \varepsilon n \} = P \{(1 - \varepsilon) n \leq \frac {k - 1}{h _ {(k)}} \leq (1 + \varepsilon) n \} \\ = P \left\{\frac {k - 1}{(1 - \varepsilon) n} \leq h _ {(k)} \leq \frac {k - 1}{(1 + \varepsilon) n} \right\} \\ \end{array}
$$

Note that $h _ { ( k ) }$ follows beta distribution with parameters k and n − k + 1 [33]. Let x1 = k−1(1 ε)n $n - k + 1 \ [ 3 3 ]$ $\begin{array} { r } { x _ { 1 } = \frac { k - 1 } { ( 1 - \varepsilon ) n } } \end{array}$ and $\begin{array} { r } { x _ { 2 } = \frac { k - 1 } { ( 1 + \varepsilon ) n } } \end{array}$ . We have

$$
P \{x _ {1} \leq h _ {(k)} \leq x _ {2} \} = I _ {x _ {1}} (k, n - k + 1) - I _ {x _ {2}} (k, n - k + 1) \tag {10}
$$

Let the R.H.S. of Equation 10 be greater or equal to 1 − δ. We have

$$
I _ {x _ {1}} (k, n - k + 1) - I _ {x _ {2}} (k, n - k + 1) \geq 1 - \delta \tag {11}
$$

By Equation 11, we get $\begin{array} { r } { k = \Theta \big ( \frac { 1 } { \mathtt { E } ^ { 2 } } l n \frac { 1 } { \mathtt { \delta } } \big ) } \end{array}$ using the theory of order statistics [33].

# Proof for Lemma 6

Let P be the k smallest values in $T _ { S _ { 1 } } \cup T _ { S _ { 2 } }$ . According to the definition of $T _ { ( S _ { 1 } \cup S _ { 2 } ) } .$ , it suffices to show that the k smallest hash values in $T _ { S _ { 1 } } \bigcup T _ { S _ { 2 } }$ are also the k smallest ones in $h ( S _ { 1 } ) \cup h ( S _ { 2 } )$ , namely $P = T _ { ( S _ { 1 } \cup S _ { 2 } ) }$ . This can be proved by contradiction. Suppose there exists $a \in h ( S _ { 1 } ) \cup h ( S _ { 2 } ) -$ $( T _ { S _ { 1 } } \cup T _ { S _ { 2 } } )$ and $b \in P$ such that $a < b .$ Without loss of generality, let $a \in h ( S _ { 2 } )$ . Then obviously $b \notin T _ { S _ { 2 } }$ , since otherwise $a \in T _ { S _ { 2 } }$ , which contradicts the assumption of a. Also, a is larger than any hash value in $T _ { S _ { 2 } }$ according to the definition of $T _ { S _ { 7 } }$ . Since $b > a ,$ b is also larger than any hash value in $T _ { S _ { 2 } }$ . Recall that $b \notin T _ { S _ { 2 } }$ , so there must be $k ^ { \prime } > | T _ { S \rangle } | = k$ hash values in $T _ { S _ { 1 } } \cup T _ { S _ { 2 } }$ that are smaller than b, indicating b ∈/ P. This contradicts the condition that $b \in P .$ .

# Proof for Theorem 5

Let $k _ { 1 }$ and $k _ { 2 }$ be synopsis size that achieve $( \varepsilon / 3 , \delta )$ - estimate for J and $^ { n _ { \mathrm { l } } } \cup \cdot$ respectively. Then it is apparent that the value sampling [34], of k should be $k = m a x \{ k _ { 1 } , k _ { 2 } \}$ $\begin{array} { r } { k _ { 1 } \geq \frac { 3 ( 6 + \varepsilon ) } { \varepsilon ^ { 2 } J } l n \frac { 2 } { 8 } > \frac { 1 8 } { \varepsilon ^ { 2 } J } l n \frac { 2 } { 8 } } \end{array}$ . By Chernoff bound of random . Additionally, we have shown that k2 is $\Theta \big ( \frac { \mathfrak { s } } { \varepsilon ^ { 2 } } l n \frac { 1 } { \mathfrak { s } } \big )$ to attain $( \varepsilon / 3 , \delta )$ -approximation. Hence, $\begin{array} { r } { k = m a x \{ k _ { 1 } , \check { k } _ { 2 } \} = \Theta ( \frac { 1 } { \varepsilon ^ { 2 } J } l n \frac { 1 } { \delta } ) } \end{array}$ guarantees to give an (ε, δ)-estimate for $n _ { \bigcap }$ .