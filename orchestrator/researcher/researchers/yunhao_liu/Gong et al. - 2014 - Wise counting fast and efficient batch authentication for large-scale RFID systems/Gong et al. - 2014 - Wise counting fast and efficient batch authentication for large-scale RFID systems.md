# Wise Counting: Fast and Efficient Batch Authentication for Large-Scale RFID Systems

Wei Gong\*†, Yunhao Liu\*, Amiya Nayak†, Cheng Wang†

{gongwei,yunhao}@greenorbs.com, {nayak,cwan3}@uottawa.ca

\*School of Software, TNLIST, Tsinghua University, China

†School of Electrical Engineering and Computer Science, University of Ottawa, Canada

# ABSTRACT

Radio Frequency Identification technology (RFID) is widely used in many applications, such as asset monitoring, e-passport and electronic payment, and is becoming one of the most effective solutions in cyber physical system. Since the identification alone does not provide any guarantee that tag corresponds to genuine identity, authentication of tag information is needed in most RFID systems. Meanwhile, as the number of tags is rapidly growing in recent years, per-tag based methods suffer from severely low efficiency and thus give way to probabilistic batch authentication. Most previous methods, however, share a common drawback from statistical perspective: they fail to explore correlation information, i.e., they do not comprehensively utilize all the information in authentication data structures. In addition, those schemes are not scalable well when multiple tag sets need to be verified simultaneously. In this paper, we propose a fast and efficient batch authentication scheme, Wise Counting (WIC), for large-scale RFID systems. We are the first to formally introduce the general batch authentication problem with multiple tag sets and give counterfeits estimation scheme with high efficiency. By employing a novel hierarchical authentication structure, we show that WIC is able to fast and efficiently authenticate both a single tag set and multiple tag sets in an easy, intuitive way. Through detailed theoretical analysis and extensive simulations, we validate the design of WIC and demonstrate its large superiority over state-of-the art approaches.

# Categories and Subject Descriptors

C.2.1 [Network Architecture and Design]: Wireless Communication; H.4 [Information Systems Applications]: Miscellaneous

# Keywords

RFID tags, batch authentication, counterfeits estimation, hierarchical data structure

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

MobiHoc’14, August 11–14, 2014, Philadelphia, PA, USA.

Copyright 2014 ACM 978-1-4503-2620-9/14/08 ...\$15.00.

http://dx.doi.org/10.1145/2632951.2632963 .

# 1. INTRODUCTION

Since friend or foe system was first developed in Second World War, Radio Frequency Identification (RFID) technology is widely used in many fields, such as asset monitoring[1][2][3], e-passport [4] and electronic payment [5][6], and is becoming one of the most effective solutions in cyber physical system [7][8][9]. A typical RFID system mainly consists of three parts: tag, reader and backend server. The tag, which is often attached to the object, contains a unique identification - Electronic Product Code (EPC) [10]. The reader is usually in charge of identification, i.e., querying the tag and collecting the information from it. The backend server that is connected to the reader can perform various operations, such as searching further object information according to specific EPC. But identification itself does not provide any means to certainly assure that the collected ID/EPC exactly corresponds to the genuine identity. Therefore, tag authentication (or verification) is indeed necessary.

Previously, much work focus on how to securely and effectively authenticate a single tag. Supposed that there are N tags registered in backend server. By leveraging the oneway hash function, Hash Lock scheme is proposed to linearly search the backend database [11]. The authentication complexity of it is O(N). To achieve better performance, the search efficiency is improved to O(log N) based on tree data structure, at the expense of storage spaces on tag [12][13]. Nevertheless, those per-tag based approaches suffer from severe scalability problem in batch authentication mode. As stated in [14], one reader can only authenticate 103 batches (each with 10,000 tags) per day. It is unlikely to accept such a low authentication efficiency in practice. Meanwhile, as RFID technology is used as one of the most important anti-counterfeiting measures for fastmoving consumer goods that are growing fast over years [15], the population of tags is expected to dramatically increase in the next few years. Thus one of top concerns for practical large-scale RFID systems is how to efficiently authenticate tags in batch.

The key advantage of batch authentication over per-tag based methods is the relaxation of the result, i.e., trading a small authentication failure probability for better authentication performance. So we also call it probabilistic batch authentication. There are two different but close-related probabilistic batch authentication problems: counterfeits detection and counterfeits estimation. In counterfeits detection problem, the result of authentication is binary. For example, in [14], positive result means detection of counterfeits. Negative result indicates that all tags in the batch are judged as legitimate with high probability. Obviously, this type of result is so coarse since it is unable to discriminate a batch with only one counterfeit tag from a batch with all fake tags. In fact, many RFID applications need to know more detailed information about counterfeits. Consequently, a fine-grained authentication scheme is proposed to approximate the count of counterfeit tags, addressing counterfeits estimation issue [16]. Although these two problems are separated, they are complementary to each other. Typically, the administrator of RFID system first performs counterfeits detection operation. If the result turns out to be positive, then counterfeits estimation algorithm can be used to obtain an accurate count of counterfeits. In this paper, we aim to efficiently solve counterfeits estimation problem with arbitrary accuracy requirements.

![](images/f1407039a8fa9e1f241bfa8bc4b483227f081dd4a5c876d9bd4c56b390da6c17.jpg)



(a) Continuous scanning

![](images/04be89ec9c9fc874681e0fa4391495c746754d2fac786a0a38c237e8bf423cf7.jpg)



(b) Inventory control

![](images/bf7f4bf09befee1b5d8eaea3a0683cfe3c78f8857af964d67b5fde749ac9f566.jpg)



(c) Flow monitoring   
Figure 1: Scenarios of authenticating multiple tag sets

By reviewing former methods from statistical perspective, we observe two important issues that are neglected before. First, they view authentication synopses as separate entities and thus do not explore correlation information among them [14][16]. Second, the estimation is confined on singletonobserved synopses which account for a relative small fraction, wasting a large amount of other authentication synopses [16]. In sum, counterfeits estimators in previous work are not statistically efficient since they do not comprehensively utilize all the information in authentication structures, giving plenty of rooms for authentication efficiency optimization. More importantly, most previous methods are designed for authenticating one single batch at a time. But in practice, it would always be required to authenticate multiple tag sets/batches simultaneously.

In this paper, we propose a fast and efficient batch authentication scheme, Wise Counting (WIC), for large-scale RFID systems. First, we formally formulate the general counterfeits estimation problem for probabilistic batch authentication with multiple tag sets. Then, we introduce a novel hierarchical authentication structure, which combines uniform random hash and minimum order statistics. With the help of this building block data structure, WIC achieves $\begin{array} { r } { \mathcal { O } \big ( \frac { N } { \varepsilon ^ { 2 } | C | } \operatorname { l o g } \log N \big ) } \end{array}$ authentication complexity (communication complexity), where |C| is the number of counterfeits from multiple tag sets and ε is the desired relative error. Through detailed analysis and extensive simulated comparison, we show that WIC is significantly advantageous over previous methods.

The major contributions of this work are as follows.

1. We are the first to define batch authentication problem with multiple tag sets and provide a fast and efficient authentication scheme, WIC, which works well with one or more tag sets.   
2. We design a novel hierarchical authentication structure to significantly reduce authentication and communication overheads. In particular, WIC wisely utilize all minimum order statistics of this data structure to obtain much more accurate counterfeits estimate, compared with previous methods. We also give a general and implementable communication protocol for both readers and tags using WIC.   
3. We validate the design of WIC through both theoretical analysis and extensive simulations. We also show that WIC is effective and significantly outperforms state-of-the-art approaches.

# 2. PRELIMINARIES

# 2.1 Motivation

Previous work on batch authentication are designed for simple scenario in which only one tag set needs to be verified. Authenticating multiple tag sets, however, are required in many practical and complex scenarios to meet various demands. Considering the following three examples as shown in Figure 1:

1. Continuous scanning is a common and basic method in large-scale RFID system [17][18][19]. It uses multiple continuous scanning operations to cover a much larger area than a single scanning. Figure 1(a) shows that a mobile reader performs scanning several times to collect all book information on the bookshelf. In order to authenticate all books, we need to verify compound set as: $R = R _ { 1 } \cup R _ { 2 } \cup \ldots \cup R _ { n }$ , where $R _ { i }$ is the set of scanned tags in i-th scanning.

2. Inventory control generally employs multiple static readers deployed at different locations, according to density, size and orientation of objects in warehouse [20][21][22]. As illustrated in Figure 1(b), Reader1 and Reader2 are deployed to cover all goods in the warehouse. If we want to authenticate the goods that both covered by Reader1 and Reader2, then the compound set $R = R _ { 1 } \cap R _ { 2 }$ needs to be tested, where $R _ { 1 }$ and $R _ { 2 }$ are the sets of tags scanned by Reader1 and Reader2 respectively.

3. Flow monitoring is essential for many large-scale events for security reason, such as rallies, conferences and sport games [23]. Figure 1(c) demonstrates an example in stadium with 2 entrances and 2 exits. A reader is equipped at each gate to monitor people flow passing by and the person who holds a genuine taggedticket is authorized to go in and out unlimited times. If administrator needs to estimate the number of unauthorized audiences in the stadium, the compound set $R \ = \ ( R _ { 1 } \cup R _ { 2 } ) \ - \ ( R _ { 3 } \cup R _ { 4 } )$ needs to be authenticated, where $R _ { 1 } , R _ { 2 } , R _ { 3 }$ and $R _ { 4 }$ are the sets of tags scanned by Entrance1, Entrance1, Exit1 and Exit2, respectively.

# 2.2 Challenges

Estimating the number of counterfeits in multiple tag sets at the same time is an important but not trivial problem in large-scale RFID systems. Since multiple tag sets might have intersections as shown in Figure 1, it cannot be easily reduced to estimate the counterfeits number one set by one set. Of course, there is a naive way to authenticate multiple tag set: first aggregate all raw tag information on server from each scanning/set, then compute the compound set according to required set expression, finally authenticate the compound set. Although this naive method works, it violates several principles that we strive to. First, the authentication process should be fast and time-efficient, i.e., the communication overhead should be kept minimum. Second, the raw tag information transmission is better to be avoided since it may create potentials for infringements of RFID data privacy [24].

# 2.3 Problem Formulation

In a typical RFID system, the backend server often registers a number of tags which are said to be legal. Let S be the set of all legitimate tags on server and N be the cardinality of S. Usually, there are $\mathcal { T } _ { 1 } , \mathcal { T } _ { 2 } , . . . , \mathcal { T } _ { l }$ tag sets to be verified, where l is an integer more than 1. In many scenarios (e.g., using multiple readers to cover a large area), the system administrator needs to know how many counterfeit tags in the compound expressions of Ti. We therefore generalize this as

$$
\mathcal {T} ^ {\prime} = \mathcal {T} _ {1} \bigodot \mathcal {T} _ {2} \bigodot \dots \bigodot \mathcal {T} _ {l},
$$

where $\tau ^ { \prime }$ is the final compound set to be verified, and J can be replaced by any one of − (difference), ∪ (union), and ∩ (intersection).

Moreover, we define that the tag is counterfeit if the tag’s information is not registered on the server. Otherwise, the tag is genuine. Similar to most prior work [14][16][25], we do not discuss the problem the genuine tag is attached to counterfeit goods, vice versa. Any problems related to tag misplacement/duplication are beyond the scope of this paper. Further, we assume that both genuine and counterfeit tags obey the same transmission protocol. By the definition

Table 1: Main Notations 

<table><tr><td>Symbols</td><td>Descriptions</td></tr><tr><td> $\mathcal{S}$ </td><td>the set of registered tags.</td></tr><tr><td> $\mathcal{T}$ </td><td>the set of tags to be verified.</td></tr><tr><td> $\mathcal{C}$ </td><td>the set of counterfeits tags.</td></tr><tr><td> $\mathcal{G}$ </td><td>the set of genuines tags.</td></tr><tr><td> $N$ </td><td>the cardinality of tags registered on server</td></tr><tr><td> $n$ </td><td>the cardinality of tags to be verified</td></tr><tr><td> $M$ </td><td>the cardinality of  $\mathcal{T} \cup \mathcal{S}$ .</td></tr><tr><td> $f$ </td><td>the size of frame.</td></tr><tr><td> $c$ </td><td>the counterfeit ratio.</td></tr><tr><td> $||$ </td><td>the cardinality of set.</td></tr><tr><td> $^{\wedge}$ </td><td>the estimate of original parameter.</td></tr><tr><td> $\mathcal{A}^{\mathcal{T}}$ </td><td>the HAS of set  $\mathcal{T}$ .</td></tr></table>

of counterfeits, we use C to denote the set of counterfeits to be verified, thus

$$
\mathcal {C} = \mathcal {T} ^ {\prime} - \mathcal {S}.
$$

The counterfeits estimation in probabilistic batch authentication is to obtain the approximate cardinality of C, i.e., |C|. In order to measure the accuracy of estimation result, we use two parameters: relative standard error ε and failure probability δ. Thereby the result of counterfeits estimation, ˆ|C|, must satisfy

$$
\operatorname * {P r} \left[ \left| \frac {| \mathcal {C} |}{| \hat {\mathcal {C}} |} - 1 \right| \leq \varepsilon \right] \geq 1 - \delta . \tag {1}
$$

For instance, if the exact number of counterfeits is 100, and $\varepsilon = 0 . 0 1 , \delta = 0 . 0 1$ , then the output estimate ˆ|C| should be between 99 to 101 with probability 0.99. Similarly, we use G to denote the set of genuines in verified sets. The main notations are listed in Table 1.

# 2.4 Communication Model

We adopt the listen-before-talk mode and frame slotted ALHOA as the basic communication model, similar to [16][26]. In this model, the reader first queries tags with several predefined commands and parameters. Each tag then performs computations on board and decides whether and what to reply to reader based on preloaded transmission protocol. Besides EPC code, each tag has its own random hash function H or random number generator that takes several input parameters, e.g., frame size, EPC code [27].

# 3. WISE COUNTING OVERVIEW

Wise Counting is an efficient probabilistic batch authentication scheme that provides accurate counterfeits estimate, achieving optimal authentication efficiency.

Following a common practice in RFID authentication, the backend server has stored all the information of registered tags. When authentication starts, the backend server initializes parameters according to the user defined requirements, ε and δ. Then the server sends those parameters to readers through a secure line. The readers use those received parameters to gather authentication information from tags to be verified. After aggregating all the authentication information from readers, the server performs verification to derive counterfeits estimate.

![](images/5af998b49c9fcf60e6514e15411e5f55197fb03813b76a597ea147aab0533661.jpg)



Figure 2: Hierarchical authentication structure generation.

With a novel Hierarchical Authentication Structure (HAS) as later shown in Section 4, WIC goes through the following main steps:

1. The reader queries the tags in the operation range and builds its own HAS $( \mathcal { A } ^ { \mathcal { T } _ { i } } )$ for Ti.   
2. The server aggregates HASes from readers and derives observed counterfeits ratio based on the compound set expression.   
3. The server estimates the cardinality of ${ \widehat { T ^ { \prime } \cup S } } \left( \left| { \widehat { T ^ { \prime } \cup S } } \right| \right)$ . Since C is a portion of ${ \mathcal { T } } ^ { \prime } \cup { \mathcal { S } } ,$ then we combine the observed counterfeits ratio and $| \widehat { T ^ { \prime } \cup \mathcal { S } } |$ to deduce the counterfeits estimate, ˆ|C|.

The next few sections elaborate on the above steps and provide detailed analysis.

# 4. DATA STRUCTURE

In this section, we describe how to generate hierarchical authentication structure from the tag set and then give the basic estimation formula.

Here we employ uniform random hash and minimum order statistics to produce HAS. As shown in Figure 2, initially the reader issues the query command to tags. Each tag then decides when (in which time slot) and what to reply according to received parameters, such as frame size $( f )$ and random seed. The reply procedure is based on slotted ALOHA model and is virtually divided into two layers. In the first layer, each tag chooses replied time slot based on a uniform random hash function, similar to much prior work [14][25][26]. At the reader side, all slots are marked as 1. In the second layer, each tag replies a uniform random number, R(EP C), between [0,1]. At the same time, the reader receives all the random numbers from tag(s) and records only the minimum number. In order to understand the principle of HAS, we are better to set aside possible collisions and just assume that the reader is able to extract minimum number from many tags’ responses in one time slot. The details about the generation of replied random number on tag and reception of minimum random number on reader are given in Section 6. The final HAS consists of f numbers. If the number is 1, it stands for no response in this time slot. Otherwise, the number is the minimum of all responses in this time slot. The pseudocodes of HAS generation are given in Algorithm 1 for the tag and Algorithm 2 for the reader.

Algorithm 1 HAS generation algorithm for the tag   
1: Receive a probing message from reader, containing frame size f and random seed r.
2: Compute reply slot number $sn = \mathcal{H}(EPC, f, r)$ .
3: while TRUE do
4: wait-for-slot-start().
5: if sn == 0 then
6: generate random number $R(EPC)$ .
7: RepMinRndProc(R).
8: else
9: $sn \leftarrow sn - 1$ , keep silent.
10: end if
11: end while

Algorithm 2 HAS generation algorithm for the reader   
1: Initialize $A^{T}[i] \leftarrow 1.0 (1 \leq i \leq f)$ ;
2: Broadcast a request to tags, including frame size f and random seed r.
3: for i = 1 to f do
4: issue-slot-start() command.
5: wait-for-tags-response().
6: if there is no response in this slot then
7: $A^{T}[i] \leftarrow 1$ .
8: else
9: $A^{T}[i] \leftarrow RecMinRndProc()$ .
10: end if
11: end for

Let n be the number of tags in tested set (T ) and $\textstyle \lambda = { \frac { n } { f } }$ be the mean number of tags’ responses in each slot. $\mathrm { W e }$ generate authentication synopsis $\dot { \boldsymbol { A } } ^ { \mathcal { T } } [ i ]$ where $i = 1 , 2 , . . . , f$ using Algorithm 1 and 2. We then study the characteristic of $\boldsymbol { \mathcal { A } } ^ { \mathcal { T } } [ i ]$ and find that if f is sufficiently large such that $\begin{array} { r } { ( 1 - \frac { 1 } { f } ) ^ { f } \approx \frac { 1 } { e } } \end{array}$ , then $\boldsymbol { \mathcal { A } } ^ { \mathcal { T } } [ i ]$ approximates an independent sample from right truncated exponential distribution with rate parameter $\lambda ,$ where the cumulative distribution function is as follow 1

$$
F (x; \lambda) \approx \left\{ \begin{array}{c l} 1 - e ^ {- \lambda x} & 0 \leq x \leq 1 \\ 0 & x <   0 \text {   or   } x > 1 \end{array} \right.
$$

and the correlation coefficient (ρ) of $\boldsymbol { \mathcal { A } } ^ { \mathcal { T } } [ i ]$ and $\mathcal { A } ^ { \mathcal { T } } [ j ]$ is

$$
\rho (\mathcal {A} ^ {\mathcal {T}} [ i ], \mathcal {A} ^ {\mathcal {T}} [ j ]) \approx - \frac {1}{n}, i \neq j.
$$

Therefore, we are able to easily obtain the MLE estimator of λ. Since the dependence between $\boldsymbol { \mathcal { A } } ^ { \mathcal { T } } [ i ]$ and $\mathcal { A } ^ { \mathcal { T } } [ j ]$ is so weak, we ignore it and get the simplified likelihood function

of λ as

$$
\mathcal {L} (\lambda) = e ^ {- \lambda \sum_ {i = 1} ^ {f} \mathbf {1} (\mathcal {A} ^ {\mathcal {T}} [ i ])} \prod_ {\mathcal {A} ^ {\mathcal {T}} [ i ] <   1} \lambda e ^ {- \lambda \mathcal {A} ^ {\mathcal {T}} [ i ]}.
$$

where $\mathbf { 1 } ( x )$ is an indicator function. If $x = 1 , \mathbf { 1 } ( x ) = 1$ . Otherwise, $\mathbf { 1 } ( x ) = 0 .$ The MLE of λ and thereby estimated number of tags in $\mathcal { A } ^ { T }$ are derived as

$$
\hat {\lambda} = \frac {\sum_ {i = 1} ^ {f} \mathbf {1} ^ {\prime} (\mathcal {A} ^ {\mathcal {T}} [ i ])}{\sum_ {i = 1} ^ {f} \mathcal {A} ^ {\mathcal {T}} [ i ]}, \hat {n} = f \hat {\lambda}. \tag {2}
$$

where $\mathbf { 1 } ^ { \prime } ( x )$ is an indicator function. If $x < 1 , \mathbf { 1 } ^ { \prime } ( x ) = 1$ . Otherwise, $\mathbf { 1 } ^ { \prime } ( x ) = 0$ .

In order to understand the simplicity of the estimation procedure, let’s see a toy example. Suppose that we test a tag set $( n = 1 0 0 )$ and get a HAS of size $7 \colon 0 . 0 7 6 8 , 0 . 0 1 8 3$ , 1, 0.0307, 0.0125, 0.1642, 0.1217. The estimated result $\hat { n } =$ $7 * { \frac { 6 } { 0 . 0 7 6 8 + 0 . 0 1 8 3 + 0 . 0 3 0 7 + 0 . 0 1 2 5 + 0 . 1 6 4 2 + 0 . 1 2 1 7 } } = 9 9$ .

# 5. ESTIMATING COUNTERFEITS AND GEN-UINES

After acquiring basic knowledge about our authentication data structure, now we first demonstrate our method to estimate the number of counterfeits and genuines in single set scenario. Later we introduce several techniques to extend estimation over compound sets.

# 5.1 Authenticating Single RFID Set

We first study an important characteristic of the probabilistic distribution for truncated exponential random variable.

Given $X _ { 1 } \sim E x p ( \lambda _ { 1 } ) , X _ { 2 } \sim E x p ( \lambda _ { 2 } )$ , and their corresponding right truncated distribution $\dot { X } _ { 1 } { } ^ { \prime } \ = \ \operatorname* { m i n } ( X _ { 1 } , 1 )$ , ${ X _ { 2 } } ^ { \prime } = \operatorname* { m i n } ( X _ { 2 } , 1 )$ . If $X _ { 1 }$ is independent of $X _ { 2 } ,$ then we have min $( { X _ { 1 } } ^ { \prime } , { X _ { 2 } } ^ { \prime } ) \sim \operatorname* { m i n } ( E x p ( \lambda _ { 1 } + \lambda _ { 2 } ) , 1 )$ . Further, we derive

$$
\operatorname * {P r} \left[ X _ {i} ^ {\prime} = \min \left(X _ {1} ^ {\prime}, X _ {2} ^ {\prime}\right) \right] = e ^ {- \left(\lambda_ {1} + \lambda_ {2}\right)} + \frac {\lambda_ {i}}{\lambda_ {1} + \lambda_ {2}} \left(1 - e ^ {- \left(\lambda_ {1} + \lambda_ {2}\right)}\right) \tag {3}
$$

, where $i = 1 , 2 .$

This characteristic tells us that if two exponential random variables are independent of each other, then minimum order of their truncated version is easily deduced.

Now we have only one set to be verified, $\tau ,$ and aim to estimate $\vert \mathcal { T } - \mathcal { S } \vert$ . The direct application of above equation is to divide the union, $\tau \cup s$ , into three independent parts: $\tau - s , \tau \cap s .$ and $s - \tau$ . We use $B _ { 1 } , \ B _ { 2 } , \ B _ { 3 }$ to denote virtual HASes for those three independent sets. Therefore we have 2

$$
\begin{array}{l} \operatorname * {P r} [ \mathcal {A} ^ {\mathcal {T}} = \mathcal {A} ^ {\mathcal {S}} ] = \operatorname * {P r} [ \min (\mathcal {B} _ {1}, \mathcal {B} _ {2}) = \min (\mathcal {B} _ {2}, \mathcal {B} _ {3}) ] \\ = \operatorname * {P r} [ \mathcal {B} _ {2} = \min (\mathcal {B} _ {1}, \mathcal {B} _ {2}, \mathcal {B} _ {3}) ] \\ \approx e ^ {- \frac {M}{f}} + (1 - e ^ {- \frac {M}{f}}) \frac {| \mathcal {T} \cap \mathcal {S} |}{M}. \\ \end{array}
$$

where M is the cardinality of ${ \mathcal { T } } \cup S .$ . We thus derive the estimation equations for the number of counterfeits and genuines in single set scenario as follows.

Theorem 1. For a large f such that $\begin{array} { r } { ( 1 - \frac { 1 } { f } ) ^ { f } \approx \frac { 1 } { e } } \end{array}$ , then

$$
| \hat {\mathcal {C}} | = | \widehat {\mathcal {T} - \mathcal {S}} | = \operatorname * {P r} ^ {\prime} [ \mathcal {A} ^ {\mathcal {T}} <   \mathcal {A} ^ {\mathcal {S}} ] \cdot \frac {\hat {M}}{\left(1 - e ^ {- \frac {\hat {M}}{f}}\right)} \tag {4}
$$

$$
| \hat {\mathcal {G}} | = | \widehat {\mathcal {T} \cap \mathcal {S}} | = (\operatorname * {P r} ^ {\prime} [ \mathcal {A} ^ {\mathcal {T}} = \mathcal {A} ^ {\mathcal {S}} ] - e ^ {- \frac {\hat {M}}{f}}) \cdot \frac {\hat {M}}{(1 - e ^ {- \frac {\hat {M}}{f}})} \tag {5}
$$

, where $\mathrm { P r ^ { \prime } }$ denotes observed probability in $\mathcal { A } ^ { T }$ and $\mathcal { A } ^ { s }$ .

The common unknown parameter in above two equations is $\hat { M } .$ Fortunately, the HAS of ${ \mathcal { T } } \cup { \mathcal { S } } , { \mathcal { A } } ^ { \tau \cup { \mathcal { S } } }$ , is just the slotwise min $( \mathcal { A } ^ { T } [ i ] , \mathcal { A } ^ { S } [ i ] )$ . It is easy to obtain Mˆ by applying equation 2 on $\smash { \mathcal { A } ^ { T \cup S } }$ . Further, if $\hat { M }$ is large enough that $e ^ { - \frac { \hat { M } } { f } }$ is close to 0, we derive simplified theorem 1 as

$$
| \hat {\mathcal {C}} | = \operatorname * {P r} ^ {\prime} [ \mathcal {A} ^ {\mathcal {T}} <   \mathcal {A} ^ {\mathcal {S}} ] \cdot \hat {M} \tag {6}
$$

$$
| \hat {\mathcal {G}} | = \operatorname * {P r} ^ {\prime} [ \mathcal {A} ^ {\mathcal {T}} = \mathcal {A} ^ {\mathcal {S}} ] \cdot \hat {M} \tag {7}
$$

# 5.2 Extension to Multiple RFID Sets

In many practical situations, we need to verify how many counterfeits are in the compound set

$$
\mathcal {T} ^ {\prime} = \mathcal {T} _ {1} \bigodot \mathcal {T} _ {2} \bigodot \dots \bigodot \mathcal {T} _ {l}
$$

, where $l \geq 1 , \mathrm { i . e . }$ , estimating $| \mathcal { C } | = | \mathcal { T } ^ { \prime } - S |$ . Still, let M be the cardinality of union, ${ \mathcal { T } } ^ { \prime } \cup { \dot { S } } .$ . The estimation procedure is composed of three steps. We will illustrate each step with a concrete example. Consider $\mathcal { T } ^ { \prime } = ( \mathcal { T } _ { 1 } \cap \mathcal { T } _ { 2 } ) \cup \mathcal { T } _ { 3 }$ .

Step one: Use relation $| A - B | = | A | - | A \cap B |$ to remove all set difference operator(s). In our example,

$$
\left| \left(\mathcal {T} _ {1} \cap \mathcal {T} _ {2}\right) \cup \mathcal {T} _ {3} - S \right| = \left| \left(\mathcal {T} _ {1} \cap \mathcal {T} _ {2}\right) \cup \mathcal {T} _ {3} \right| - \left| \left(\left(\mathcal {T} _ {1} \cap \mathcal {T} _ {2}\right) \cup \mathcal {T} _ {3}\right) \cap S \right|
$$

Step two: Use relation $( A \cap B ) \cup C = ( A \cup C ) \cap ( B \cup C )$ to replace union of set intersection by the intersection of set union. In our example,

$$
\left| \left(\mathcal {T} _ {1} \cap \mathcal {T} _ {2}\right) \cup \mathcal {T} _ {3} \right| = \left| \left(\mathcal {T} _ {1} \cup \mathcal {T} _ {3}\right) \cap \left(\mathcal {T} _ {2} \cup \mathcal {T} _ {3}\right) \right|
$$

and

$$
\left| \left(\left(\mathcal {T} _ {1} \cap \mathcal {T} _ {2}\right) \cup \mathcal {T} _ {3}\right) \cap S \right| = \left| \left(\mathcal {T} _ {1} \cup \mathcal {T} _ {3}\right) \cap \left(\mathcal {T} _ {2} \cup \mathcal {T} _ {3}\right) \cap S \right|
$$

Step three: Let c be the ratio of counterfeits to the all sets union, $\begin{array} { r } { \mathrm { i . e . , ~ } c = \frac { | { \mathcal { C } } | } { M } } \end{array}$ M . In order to get this counterfeits ratio, we first simply extended the theorem 1 to get the following equation:

$$
\operatorname * {P r} \left[ \mathcal {A} ^ {\mathcal {T} _ {0}} = \mathcal {A} ^ {\mathcal {T} _ {1}} = \dots = \mathcal {A} ^ {\mathcal {T} _ {d}} = \mathcal {A} _ {\cup} \right] \approx e ^ {- \frac {M}{f}} + \frac {(1 - e ^ {- \frac {M}{f}})}{M} \left| \bigcap_ {j = 0} ^ {d} \mathcal {T} _ {j} \right|
$$

, where $\mathcal { A } _ { \cup }$ is the HAS of $\cup _ { i = 0 } ^ { l } \mathcal { T } _ { i } , \ \mathcal { T } _ { 0 } = \mathcal { S } , \ | \cup _ { i = 0 } ^ { l } \mathcal { T } _ { i } | = M$ and 1 ≤ d ≤ l. 3 $1 \leq d \leq l .$

In our example, we thus have

$$
c = P 1 - P 2 \tag {8}
$$

Algorithm 3 Reply minimal random value for tag: Rep-MinRndProc()  
1: generate a random number $R(EPC)$ from unit exponential distribution EXP.
2: Save integer part of R into $j = \log \log N$ bits, as $I[0] \sim I[j-1]$ , position 0 is the highest bit.
3: Truncate decimal part of R into k = 10 bits, as $I[j] \sim I[j+k-1]$ , position j is the highest bit.
4: Initialize $T[i] \leftarrow 0$ , $1 \leq i < \log \log N + 10$ .
5: $i \leftarrow 0$ and wait-for-subslot-start().
6: for i = 0 to $j + k - 1$ do
7: wait-for-subslot-continue().
8: while TRUE do
9: Receive bit 'b' and $T[i] \leftarrow b$ .
10: if b == 1 then
11: if prefix i bits of T is equal to I then
12: instantly issue response and break while loop.
13: else
14: keep silent.
15: end if
16: end if
17: if b == 0 then
18: break while loop.
19: end if
20: end while
21: end for

where $P 1 = \mathrm { P r } [ \operatorname* { m i n } ( \mathcal { A } ^ { T _ { 1 } } , \mathcal { A } ^ { T _ { 3 } } ) = \operatorname* { m i n } ( \mathcal { A } ^ { T _ { 2 } } , \mathcal { A } ^ { T _ { 3 } } ) = \mathcal { A } _ { \cup } ]$ , $P 2 = \operatorname* { P r } [ \operatorname* { m i n } ( \mathcal { A } ^ { T _ { 1 } ^ { * } } , \mathcal { A } ^ { \hat { T _ { 3 } } } ) = \operatorname* { m i n } ( \mathcal { A } ^ { T _ { 2 } } , \mathcal { A } ^ { T _ { 3 } } ) = \mathcal { A } ^ { T _ { 0 } } = \mathcal { A } \cup$ .

Finally, by the definition of c, the estimated number of counterfeits for multiple tag sets is

$$
| \hat {\mathcal {C}} | = \hat {M} \cdot c ^ {\prime}. \tag {9}
$$

where $\hat { M }$ is obtained by simply applying equation 2 on $\mathcal { A } _ { \cup }$ and $c ^ { \prime }$ is the observed ratio in equation 8.

# 6. THE EFFICIENCY OF WISE COUNTING

In this section, we analyze the time complexity of WIC and propose an optimization based on the exponential pseudorandom number generator.

# 6.1 Time Complexity

For an arbitrary set expression of tag sets to be verified, the relative standard error of WIC can be derived as :

$$
\mathrm{RSE} _ {w i c} ^ {2} = \mathrm{E} (\frac {| \hat {\mathcal {C}} | _ {W I C}}{| \mathcal {C} |} - 1) ^ {2} \approx (f c) ^ {- 1}.
$$

Therefore if ε is the required relative error, the size of frame should be $f \approx \varepsilon ^ { - 2 } c ^ { - \bar { 1 } }$ for HAS generation in the first layer. 4

For the second layer in HAS generation, we need to derive the number of subslots for transmitting the minimal random number. From section 4, we know that $\boldsymbol { \mathcal { A } } ^ { \mathcal { T } } [ i ]$ follows a truncated exponential distribution: $\begin{array} { r } { \mathcal { A } ^ { T } [ i ] \sim \operatorname* { m i n } ( \frac { \mathrm { E X P } } { \lambda } , 1 ) } \end{array}$ , where EXP is the unit exponential variable.

Since we know there may be M tags’ responses in a single slot at worse and $\lambda \sim \mathcal { O } ( \dot { M } )$ . This indicates that O(log M )

4For simplicity, we do not include the analysis of δ in the rest part of this paper. Since it is well-known [28] that if we are able to achieve a constant $\delta ,$ we can repeat the process $\begin{array} { r } { \mathcal { O } ( \log \frac { 1 } { \delta ^ { \prime } } ) } \end{array}$ times to achieve arbitrary $\delta ^ { \prime } .$ .

Algorithm 4 Receive minimal random value for reader: RecMinRndProc()   
1: Initialize $T[i] \leftarrow 0, 1 \leq i < \log \log N + 10.$ 2: issue-subslot-start() command.
3: for i = 0 to $\log \log N + 9$ do
4:    issue-subslot-continue() command
5:    Broadcast bit '1' and wait-for-tags-response().
6:    if there is no response in this subslot then
7: $T[i] \leftarrow 0$ . Broadcast bit '0'.
8:    else
9: $T[i] \leftarrow 1$ .
10:    end if
11: end for
12: combine T's integer and decimal part into a float m.
13: return minimal value $2^{-m}$ .

bits need to be transmitted in a single slot. In the following, we reduce this transmit time by employing an exponential pseudorandom number generator to replace the uniform random number generator described in Section 4.

Now we take log operation on $\boldsymbol { \mathcal { A } } ^ { \mathcal { T } } [ \boldsymbol { i } ]$ to have: log $A ^ { \mathcal { T } } [ i ] \sim$ min(− log λ+log EXP, 0). This motivates us to use (log log M+ α) bits for transmission, where − log log M represents integer part and α denotes decimal part. Hence the total time complexity of WIC is $\varepsilon ^ { - 2 } c ^ { - 1 }$ (log log $M + \alpha )$ .

We observed that $\alpha = 1 0$ is enough in practice. For instance, if we need to verified $\mathcal { T } _ { 1 }$ , then the observed probability for $\operatorname* { P r } [ \mathcal { T } _ { 0 } = \mathcal { T } _ { 1 } = \mathcal { T } _ { \cup } ]$ is at most $2 ^ { - \alpha + 1 } = 0 . 0 0 2$ shifted from ground truth. This difference is negligible for many applications. Actually the value of α is tunable according to various accuracy requirements. Algorithm 3 and 4 present the implementation of how to reply and receive the minimal value for both tag and reader. It is worth noting that we make a slight difference here. Instead of finding the minimal value from many uniform distributed variables, we are trying to acquire the maximal value among exponential distributed variables. This conversion stems from

$$
\min (1, \mathcal {U} _ {0}, \mathcal {U} _ {1}, \dots) \Rightarrow \max (0, - \log \mathcal {U} _ {0}, - \log \mathcal {U} _ {1}, \dots),
$$

where Ui is uniform random number in [0,1] and hence − log Ui follows unit exponential distribution.

# 7. EVALUATION

In this section, we evaluate the performance of WIC and compare it with the state-of-the-art method INC [16] under extensive simulations.

# 7.1 Setup and Metrics

The simulations are conducted on a PC with Intel i7 CPU at 3.2GHz and 8GB RAM. We write our own simulator adopting C# programming language. We register 10,000,000 tags on server using MS SQLServer 2000 database. We take 500 runs for each experiment and report the average.

Estimation Accuracy: To evaluate the accuracy of WIC estimator, we use three standard metrics: Relative Standard Error (RSE), $| \textstyle { \frac { \hat { \theta } } { \theta } } - 1 | ;$ Standard Deviation (SD), $\sigma =$ $\sqrt { \operatorname { E } [ } ( { \hat { \theta } } - \theta ) ^ { 2 } ]  ;$ ; Norm Std Deviation (NSD), $\begin{array} { r } { \sigma ^ { \prime } = \frac { \sigma } { \mathrm { E } [ \theta ] } } \end{array}$ , where ˆθ is the estimate of original value θ. Without loss of generality, we vary the size of verified tag set $( \mathcal { T } _ { 1 } )$ from 1,000,000 to $5 , 0 0 0 { , } 0 0 0$ , but fix counterfeits ratio at 0.07 which is the reported statistics in [29]. As stated in Section 4, f is the size of frame in the first layer.

![](images/8c2b3a1cfa57c046fc93e0eef2548eff8affbc359fea79720178721487047910.jpg)



(a) Relative Standard Error.

![](images/b4fe6c223778ba6d6e9959c9f08fa929be39667dc4a19e57a17464636ef0aff4.jpg)



(b) Standard Deviation.

![](images/cac338d59f5c3b390ab4af220ed328be9a5b8cfa440526b7feb0d9b32f961a2e.jpg)



(c) Norm Std Deviation.

Figure 3: The accuracy of ˆ|C| vs |T1|, when |S| = N = 10, 000, 000, c = 0.07.   
![](images/65b38d67db2ca3d7eb1419962919f58454fa4e35c9346fb5faa4e24638a89de7.jpg)



(a) Relative Standard Error.

![](images/ea6e95e16b690a59762afe8650b4a082cf43b1791427d84b0ae86a34d8a1959e.jpg)



(b) Standard Deviation.

![](images/fdbdfadda55dacef63ddca141382fd3f90e343209e59d67a97ccfa4f800c1888.jpg)



(c) Norm Std Deviation.

Figure 4: The accuracy of ˆ|G| vs |T1|, when |S| = N = 10, 000, 000, c = 0.07.   
![](images/cec40dee6fd740ee1381ee6ce22699a4ee5034036968512d32c32967da362549.jpg)



(a) Fixed total transmission cost at 20KB.

![](images/4f21fa6e315d8def477809571d4c87ecde8a619f75501ac48472ea39ff83b83b.jpg)



(b) Fixed frame size at 51200.   
Figure 5: The accuracy $\vert \mathcal { T } _ { 1 } - \mathcal { S } \vert$ vs Reciprocal Counterfeit Ratio, when |S| = 10, 000, 000, $| \mathcal { T } _ { 1 } | = 1 0 , 0 0 0 , 0 0 0$ .

Figure 3 shows the result of estimator ˆ|C|. From those figures, we make several observations. First, the increase of frame size improves RSE of ˆ|C|. In particular, when the number of tags is 1,000,000, the RSE is 0.73 with f=32 and drops quickly to 0.10 with f=2048. Second, RSE remains almost unchanged as the number of verified tags grows. This nice probability confirms our former complexity analysis: the RSE is mainly related to frame size f and counterfeit ratio c, not the number of tags to be verified. It thus provides us scalable authentication scheme for large-scale RFID system. Third, SD and NSD of $| \hat { \mathcal { C } } |$ are also greatly reduced by larger frame size.

![](images/2ac787ca116f98191872c40f3834780b641071823a25e4b2fee876019a03c987.jpg)



(a) Fixed total transmission cost at 20KB.

![](images/9dc19eb544e326544127bb4e10ab76b2b6a707d2d6839a46733e181c69564e5f.jpg)



(b) Fixed frame size at 51200.

Figure 6: The accuracy $| ( ( T _ { 1 } \cup T _ { 2 } ) \cap T _ { 3 } ) - S |$ vs Reciprocal Counterfeit Ratio, when $| S | = 1 0 , 0 0 0 , 0 0 0 , | T _ { 1 } \cup T _ { 2 } \cup T _ { 3 } | =$ 10, 000, 000 .   
![](images/8025e04933ef150cb1d12103a61c36daf96aef7e446693f2885a05f9773f151c.jpg)



(a) with different relative error ε and c = 0.1.

![](images/3a30a7cf09e7902268de413a68ad0803ea2fcdf83b435450425a3bf21ef88809.jpg)



(b) with different relative error ε and c = 0.01.   
Figure 7: Communication cost between reader and tags (in log scale), when $| S | = 1 0 , 0 0 0 , 0 0 0 , | \mathcal { T } _ { 1 } | = 5 0 , 0 0 0 , 0 0 0 ,$

Similar trend can also be seen in Figure 4. But there is a major difference. Contrast to RSE of ˆ|C|, the RSE of ˆ|G| is diminishing as $\left| \mathcal { T } _ { 1 } \right|$ increases . This trend stems from the increasing genuines ratio due to increased $| { \mathcal { T } } _ { 1 } | ,$ since the number of counterfeits is static.

Single Set Authentication: Here we study how counterfeits ratio affects accuracy of estimators. We vary the reciprocal counterfeit ratio and keep the total transmission size and frame size fixed. As shown in Figure 5a, we use total transmission size budget for 20KB. The result shows

that our WIC is always advantageous over INC. For example, when reciprocal counterfeit ratio is 100, the RSE of WIC is 0.06 while RSE of INC is 0.44. The low performance of INC is mainly due to that they fail to examine the correlation information. The secondary factor may be more bits per slot used than WIC. This is confirmed by result in Figure 5b. We fix the frame size at 51200 to compare those methods, ignoring different lengths of time slot. The performance of INC is still worse than WIC, although the gap of RSE between INC and WIC is smaller than that in Figure 5a.

Multiple Sets Authentication: The settings for multiple set authentication are all same as in single set. The only difference is we need to authenticate a compound set expression: $| ( ( T _ { 1 } \cup T _ { 2 } ) \cap T _ { 3 } ) - S |$ . Note that for multiple sets INC does not have solution so far, so it is not included for comparison here. Figure 6a reports the RSE as a function of reciprocal counterfeits ratio. It shows that our WIC is still able to give accurate counterfetis estimate as in the single set situation, which is consistent with our asymptotic results in Section 5.2.

Communication Cost: We compare three methods given ε changing from 1% to 15% and the counterfeit ratio at 0.01 and 0.1 in single set situation. The communication cost results of three schemes are depicted in Figure 7. We assume perfect communication channel between reader and tags. The slot length for INC is 32 bits. Again, we can see that WIC achieves much lower communication cost than INC. For instance, total transmission cost of WIC is merely 4.7% of INC when $c = 0 . 0 1 , \varepsilon = 0 . 0 1$ . From a different perspective, above comparison results indicate that given a certain time budget, the authentication accuracy of WIC will still much better than INC.

# 8. RELATED WORK

To authenticate a batch of tags, there are two main categories of methods: deterministic and probabilistic. For small-scale RFID systems, deterministic methods that typically combine anti-collision protocol with per-tag authentication scheme work quite well [30]. The anti-collision protocols includes ALOHA-based EPCGlobal C1G2 standard [10] and tree-based ISO 18000-6 standard [31]. To securely verify a single tags, various schemes are designed according to different purposes, e.g., system anonymity [32], anticloning [33], hash-based authentication [11], key management using tree structure [12][13]. The best known efficiency O(1) is achieved by Lu et al. by employing a weak privacy model [34]. Those per-tag based approaches, however, suffer from severe scalability issue when the population of tags rapidly increases, since the complexity of deterministic scheme should be linear with the number of tags.

The first probabilistic batch authentication for large-scale RFID systems, SEBA, is proposed in [14]. By using single echo from each tag, SEBA is able to successfully detect counterfeits with high probability if the fraction of counterfeits exceeds predefined threshold. Since the result of SEBA only indicates whether there is counterfeit and is lack of further information, a fine-grained and scalable batch authentication scheme, INC, is introduced to accurately approximate the count of counterfeits [16]. From statistical perspective, we discover most previous methods fail to explore information in authentication data structures, leaving the correlation information and a great deal of authentication synopses unused. In contrast, WIC is statistically efficient in sense of Cramer-RAO lower bound. Moreover, those former methods can only efficiently authenticate one tag set whereas WIC still performs well with multiple tag sets.

Besides above probabilistic batch authentication schemes, a number of probabilistic cardinality estimation approaches are proposed. Kodialam et al. introduce the first probabilistic RFID estimation algorithm using linear counting. Unified Probabilistic Estimator (UPE) and Unified Probabilistic Estimator (UPE) are proposed to deal with different framesize constraints [26]. An asymptotically unbiased estimator, EZB, uses the number of zero slot in the frame to track the dynamics of tag population in both time and spatial domain [25]. Han et al. propose to use first non-empty slot observation to quickly estimate the cardinality [35]. Qian et al. propose LOF, which borrows the idea of FM-Sketch to geometrically approximate the count of tags [36]. Zheng et al. advance the estimation efficiency from O(log n) by LOF to O(log log n), where n is the number of tags to be estimated [37]. Average Run based Tag Estimation (ART) method uses a new statistical entity, average run length, to achieves 7x faster then UPE [38]. The first energy-efficient estimation scheme is proposed by Li et al [39]. Gong et al propose the first arbitrarily accurate approximation scheme for cardinality estimation using t-wise independent hash functions [40]. A comprehensive understanding of RFID counting protocols can be found in [41], which emphasizes the use of two-phase schemes. Although these algorithms can effectively derive the estimate of total number of tags in interested region, they are unable to distinguish counterfeit tags from genuine tags. They are thus not appropriately applicable in RFID authentication systems.

# 9. CONCLUDING REMARKS

In this paper, we propose a fast and efficient batch authentication scheme for large-scale RFID systems with optimal efficiency. First, we formally defined the general counterfeits estimation problem with multiple tag sets. Then we introduce a novel hierarchical authentication structure to efficiently encode tag sets. By using this statistically efficient data structure, WIC achieves $\mathcal { O } ( \textstyle \frac { - N } { \varepsilon ^ { 2 } | C | }$ log log N) authentication complexity. By theoretical analysis and extensive simulation comparisons, we show that WIC is significantly advantageous over previous state-of-the-art methods. We are currently working on adapting WIC to off-the-shelf commercial tags. In the future, we also plan to provide systematic implementations of WIC using software defined radios as we already have some initial designs.

# 10. ACKNOWLEDGMENTS

We would like to thank the anonymous reviewers for valuable and insightful comments. This work is supported in part by the NSFC Young Scholar No.61303196, NSFC Distinguished Young Scholars No.61125202 and Natural Sciences and Engineering Research Council (NSERC) of Canada grant No.CRDPJ-445199-12. We also acknowledge the support from the Open RFID Lab (ORL) project [42].

# 11. REFERENCES

[1] Frost & Sullivan. Global RFID Healthcare and Pharmaceutical Market. Industry Report, 2011.   
[2] Frost & Sullivan. Global RFID market. Industry Report, 2011.   
[3] How RFID Is Transforming VA Hospital Operations. www.rfidjournal.com/article/view/9819, 2012.   
[4] J. Hoepman, E. Hubbers, B. Jacobs, M. Oostdijk, and R. Schreur. Crossing Borders: Security and Privacy Issues of the European e-Passport. pages 152–167, 2006.   
[5] J. Collins. Hong Kong a´rs Airport to Tag Bags. RFID Journal, 2004.   
[6] M. Pelino, C. Mines, J. Warner, and S. Musto. M2M Connectivity Helps Telcos Offset Declining Traditional Services. Forrester Research, 2011.

[7] R. Want. RFID–A Key to Automating Everything. Scientific American, 290(1):56–65, 2004.   
[8] D. Ma, C. Qian, W. Li, J. Han, and J. Zhao. GenePrint: Generic and Accurate Physical-layer Identification for UHF RFID Tags. In Proc. of IEEE ICNP, 2013.   
[9] J. Han, C. Qian, D. Ma, X. Wang, J. Zhao, P. Zhang, W. Xi, and Z. Jiang. Twins: Device-free Object Tracking using Passive Tags. In Proc. of IEEE INFOCOM, 2014.   
[10] EPCglobal Radio-Frequency Identity Protocols Class-1 Generation-2 UHF RFID Protocol for Communications at 860 MHz-960MHz, 2008.   
[11] S. Weis, S. Sarma, R. Rivest, and D. Engels. Security and Privacy Aspects of Low-Cost Radio Frequency Identification Systems. Security in pervasive computing, pages 50–59, 2004.   
[12] L. Lu, J. Han, L. Hu, Y. Liu, and L.M. Ni. Dynamic Key-Updating: Privacy-Preserving Authentication for RFID Systems. In Proc. of IEEE PERCOM, 2007.   
[13] L. Lu, J. Han, R. Xiao, and Y. Liu. ACTION: Breaking the Privacy Barrier for RFID Systems. In Proc. of IEEE INFOCOM, 2009.   
[14] L. Yang, J. Han, Y. Qi, and Y. Liu. Identification-free Batch Authentication for RFID Tags. In Proc. of IEEE ICNP, 2010.   
[15] The spread of counterfeiting: Knock-offs catch on. The Economist, 2010.   
[16] W. Gong, K. Liu, X. Miao, Q. Ma, Z. Yang, and Y. Liu. Informative Counting Fine-grained Batch Authentication for Large-Scale RFID Systems. In Proc. of ACM MOBIHOC, 2013.   
[17] B. Sheng, Q. Li, and W. Mao. Efficient Continuous Scanning in RFID Systems. In Proc. of IEEE INFOCOM, 2010.   
[18] L. Xie, Q. Li, X. Chen, S. Lu, and D. Chen. Continuous Scanning with Mobile Reader in RFID Systems: an Experimental Study. In Proc. of ACM MOBIHOC, 2013.   
[19] H. Liu, W. Gong, X. Miao, K. Liu, and W. He. Towards Adaptive Continuous Scanning in Large-Scale RFID Systems. In Proc. of IEEE INFOCOM, 2014.   
[20] Y. Zheng and M. Li. P-MTI: Physical-layer Missing Tag Identification via Compressive Sensing. In Proc. of IEEE INFOCOM, 2013.   
[21] F. Gandino, R. Ferrero, B. Montrucchio, and M. Rebaudengo. DCNS: An Adaptable High Throughput RFID Reader-to-Reader Anticollision Protocol . Parallel and Distributed Systems, IEEE Transactions on, 24(5):893–905, 2013.   
[22] Y. Zheng and M. Li. Read bulk data from computational rfids. In Proc. of IEEE INFOCOM, 2014.   
[23] H. Liu, W. Gong, L. Chen, W. He, K. Liu, and Y. Liu. Generic Composite Counting in RFID Systems. In Proc. of IEEE ICDCS, 2014.   
[24] S.L. Garfinkel, A. Juels, and R. Pappu. RFID privacy: an overview of problems and proposed solutions. Security Privacy, IEEE, 3(3):34–43, May 2005.

[25] M. Kodialam, T. Nandagopal, and W.C. Lau. Anonymous Tracking Using RFID Tags. In Proceedings of IEEE INFOCOM, 2007.   
[26] M. Kodialam and T. Nandagopal. Fast and Reliable Estimation Schemes in RFID Systems. In Proc. of ACM MOBICOM, 2006.   
[27] H. Zhang, J. Gummeson, B. Ransford, and K. Fu. Moo: A Batteryless Computational RFID and Sensing Platform. Tech Report UMASS, 2011.   
[28] Rajeev Motwani. Randomized Algorithms. Cambridge university press, 1995.   
[29] ICC Counterfeiting Intelligence Bureau. Countering Counterfeiting: A Guide to Protecting and Enforcing Intellectual Property Rights. 1997.   
[30] T.F. La Porta, G. Maselli, and C. Petrioli. Anticollision Protocols for Single-Reader RFID Systems: Temporal Analysis and Optimization. IEEE Transactions on Mobile Computing, 10(2):267 –279, 2011.   
[31] Information technology Radio frequency identification for item management Part 6: Parameters for air interface communications at 860 MHz to 960 MHz, 2010.   
[32] Y.K. Lee, L. Batina, and I. Verbauwhede. Untraceable RFID authentication protocols: Revision of EC-RAC. In Proc. of IEEE RFID, 2009.   
[33] L. Bolotnyy and G. Robins. Physically Unclonable Function-Based Security and Privacy in RFID Systems. In Proc. of IEEE PERCOM, 2007.   
[34] L. Lu, Y. Liu, and X. Li. Refresh: Weak Privacy Model for RFID Systems. In Proc. of IEEE INFOCOM, 2010.   
[35] H. Han, B. Sheng, C.C. Tan, Q. Li, W. Mao, and S. Lu. Counting RFID Tags Efficiently and Anonymously. In Proceedings of IEEE INFOCOM, 2010.   
[36] C. Qian, H. Ngan, Y. Liu, and L.M. Ni. Cardinality Estimation for Large-Scale RFID Systems. IEEE Transactions on Parallel and Distributed Systems, 22(9):1441–1454, 2011.   
[37] Y. Zheng and M. Li. PET: Probabilistic Estimating Tree for Large-Scale RFID Estimation. IEEE Transactions on Mobile Computing, 11(11):1763–1774, 2012.   
[38] M. Shahzad and A. Liu. Every Bit Counts - Fast and Scalable RFID Estimation. In Proc. of ACM MOBICOM, 2012.   
[39] T. Li, S. S. Wu, S. Chen, and M. C. K. Yang. Generalized Energy-Efficient Algorithms for the RFID Estimation Problem. IEEE/ACM Transactions on Networking, 20(6):1978 –1990, 2012.   
[40] W. Gong, K. Liu, X. Miao, and H. Liu. Arbitrarily Accurate Approximation Scheme for Large-Scale RFID Cardinality Estimation. In IEEE INFOCOM, 2014.   
[41] B. Chen, Z. Zhou, and H. Yu. Understanding RFID Counting Protocols. In Proc. of ACM MOBICOM, 2013.   
[42] Open rfid lab, http://pdcc.ntu.edu.sg/wands/orl.