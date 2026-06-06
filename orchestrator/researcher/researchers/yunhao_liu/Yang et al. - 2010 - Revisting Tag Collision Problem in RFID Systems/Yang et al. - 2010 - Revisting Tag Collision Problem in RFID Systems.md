# Revisting Tag Collision Problem in RFID Systems

Lei Yang $^{*}$ , Jinsong Han $^{*}$ , Yong Qi $^{*}$ , Cheng Wang $^{\ddagger}$ , Yunhao Liu $^{\dagger}$ , Ying Cheng $^{\S}$ , Xiao Zhong $^{\S}$

\*Department of Computer Science and Technology

Xi'an Jiaotong University, Xi'an, China

$^{\dagger}$ Department of Computer Science and Engineering

Hong Kong University of Science and Technology, Hong Kong, China

$^{\ddagger}$ Department of Computer Science and Technology

Tongji University, Shanghai, China

§IBM Research China

Abstract—In RFID systems, the reader is unable to discriminate concurrently reported IDs of tags from the overlapped signals, and a collision happens. Many algorithms for anti-collision are proposed to improve the throughput and reduce the latency for tag identification. Existing anti-collision algorithms mainly employ CRC based collision detection functions for determining whether the collision happens. Generating CRC codes, however, requires complicated computations for both RF tags and readers, and hence incurs non-trivial time consumption, becoming the bottleneck. In this study, we design a Quick Collision Detection (QCD) scheme based on the bitwise complement function plus collision preamble, which significantly reduces the number of gates for computation and facilitates to simplify the IC design of RFID tags. The QCD scheme does not require any modification on upper-level air protocols, so it can be seamlessly adopted by current anti-collision algorithms. Through comprehensive analysis and simulations, we show that QCD improves the identification efficiency by 40%.

Keywords-RFID, Collision Detection, CRC, Bitwise Complement

# I. INTRODUCTION

Radio Frequency Identification (RFID) has gained substantial attentions recently due to the adoption in many applications such as logistics, retails, assert management, access control $[23]$ , and health care. These RFID based systems typically comprise of a number of readers and tags. Attaching to objects or persons, tags can report their IDs to readers via RF signals. The RF based communication enables RFID based systems to identify or localize objects without keeping the tags in sight or touch, hereby facilitating the automatic identification and localization $[1]$ $[24]$ $[28]$ .

Identifying tags is like a challenge-response procedure. Within its detecting range, a reader broadcasts a frame, which comprises of a number of slots. Upon receiving the frame, each tag randomly selects a slot, and transmits its ID to the reader in that slot. If only one tag responds in a given slot, the reader can successfully receive the tag's ID. Accordingly, such a slot is termed as a single slot. If none of tags responds in a slot, the slot is termed as idle slot. If there are more than one tag respond in a slot, the overlapped signals will cause a collision on the RF communication channel, which is called Tag Collision problem. Correspondingly, a slot with a collision is termed as collided slot. If a collision happens, each collided tag has to reselect a slot to transmit its ID in the next frame, which may cause delay on the identification procedure.

One attempt for solving Tag Collision is to extend the RF bandwidth. A larger RF bandwidth can provide more non-collided channels to tags. But physically extending RF bandwidths is not adopted by popular RFID standards due to the scarcity of available RF Spectrums $[2]$ $[3]$ . Another solution is to employ anti-collision algorithms. Anti-collision algorithms can be classified into two categories, viz. Framed Slotted ALOHA based (FSA) and Binary Tree based (BT). The key issue of anti-collision solutions is the identification efficiency, i.e., identifying all tags with minimum time duration. The identification efficiency of these algorithms depends on the efficiency of their collision detection functions, which are used for determining the types of slots. However, current detection functions used by RFID systems are inefficient due to the adoption of CRC code.

There are two major ways to establish a detection collision function. One is to utilize special hardware for sensing collisions in wireless channels. Designing such hardware, however, is costly and especially unaffordable to low-cost RFID tags [22]. The other approach is to utilize CRC as the collision detection. In a given slot, a tag emits its ID together with the ID's CRC code. The reader uses the CRC codes to validate the ID for this tag. If the ID and the code match, the slot is identified as a single slot. Otherwise, a collision happens in this slot. We term this method as CRC-CD, as illustrated in Figure 1. In the following, we denote crc(.) as the CRC operation. We also denote $\vee$ as the signal overlapping, which can be abstracted as the bitwise Boolean sum [5] [6]. For example, the overlapping result of two tags' ID signals is

![](images/b69dc2f0fe41179afb34f713857c2f66400668156ffb0308665a9dea042400da.jpg)



Figure 1. CRC-CD Scheme

$$
(0 1 1 0 0 1) \vee (0 1 0 0 1 0) = (0 1 1 0 1 1)
$$

In Figure 1, the reader first computes

$$
c r c (i d _ {1} \vee i d _ {2} \vee \dots \vee i d _ {m})
$$

, and then determines the slot is a collided slot if the result is equivalent with

$$
c r c (i d _ {1}) \vee c r c (i d _ {2}) \vee \dots \vee c r c (i d _ {m})
$$

If the slot is collided, the reader needs to launch another frame for identifying those collided tags, until all tags are successfully identified. Thus, none of the idle or collided slot is helpful to identify tags. In fact, the reader identifies tags only in single slots. Unfortunately, the throughput of the single slots, which is defined as the ratio of the number of single slots to the total number of slots in the identification procedure, is very low in most FSAs. For example, we will show that the throughput of FSAs cannot exceed 0.37 later in Lemma 1, indicating that existing anti-collision algorithms cannot identify any tag in around 63% slots.

The observation motivates us to revisit the solutions of tag collision problem. Clearly, if we are able to reduce the time consumed in determining those idle slots, the identification process will be remarkably improved. Adopting CRC-CD as the collision detection function, however, leads several shortcomings to current detection functions. First, CRC-CD is based on the cyclic redundancy check algorithm. The computing complexity of CRC is $\mathcal{O}(l)$ , where l is the length of ID. Second, CRC-CD requires more than 100 instructions for generating a CRC code, which is non-trivial for RFID tags due to their extremely limited computation capacity. Third, the length of CRC codes is relatively long so that the communication overhead is high. For example, ISO 18000-6 (also compatible with EPC Gen 2) employs 32 bits CRC function. Indeed, CRC-CD becomes the barrier of collision detection functions.

Instead of using CRC-CD, we propose a Quick Collision Detection (QCD) scheme, to accelerate the collision detection process. Adopting bitwise complement as the collision detection function, QCD can significantly reduce the complexity of IC design as well as the number of gates required by RFID tags. We also leverage a collision preamble to further speed up the collision detection process. Our theoretical analysis and experimental results show that QCD can save more than 40% time for both FSA and BS anti-algorithms during the tag identification. The rest of this paper is organized as follows. We discuss the related works in Section II and revisit the efficiency of existing anti-collision algorithms in Section III. Then formally define the collision detection problem and present the design of QCD in Section IV. We theoretically analyze the performance of QCD and compare QCD with CRC-CD in details in Section V. Last, we extensively evaluate QCD in Section VI and conclude the paper in Section VII.

# II. RELATED WORKS

In the literature, the works related to the collision detection comprise of two categories, Framed Slotted ALOHA based and Binary Tree based algorithms.

Framed Slotted ALOHA (FSA) based algorithms: Roberts [17] first proposes an ALOHA-based anti-collision scheme for RFID identification. Lee [8] finds that the reader obtains a maximum identification throughput within its scanning field when the size of frame equals to the number of tags. Lee also leverages his observation to propose a dynamic FSA, which improves the throughput by adaptively tuning the length of current frame based on the number of collided slots reported from the previous frame. Similarly, EPC Gen2 [2] adopts a variation of FSA, 'Q-Adaptive', which also adaptively adjusts the frame length according to the type of last slot. If the last slot is idle or collided, the reader will end the current frame immediately and launch a new detecting frame. The length of new frame will be shorter than the current frame if the last slot is an idle one, otherwise it will be longer if the last slot is collided.

Binary Tree (BT) based algorithms: The binary tree (BT) based RFID identification protocols has been adopted by another well-known RFID air protocol, ISO 18000-6 [3]. Hush and Wood [12] analyze the throughput of BT based algorithms by using the conclusion from [11]. Myung and Lee [9] [10] propose an Adaptive Binary Splitting (ABS) protocol to reduce collisions and identify tags efficiently. ABS starts the tag identification only from readable cycles and uses random numbers for splitting the tag sets. ABS achieves a quick identification by eliminating unnecessary cycles. In particular, researchers develop Query Tree (QT) based anti-collision algorithms to resolve the 'starvation problem' that may occur in both FSAs and BTs [18] [19]. QT based protocols distributes tags in a binary tree according to their IDs. The reader broadcasts a query with a bit string prefix $(q_{1}q_{2}\cdots q_{x})$ . The tag which has a match prefix in its ID responds the query with it's ID. If the responses collide, the reader appends one bit to prefix, $(q_{1}q_{2}\cdots q_{x}0)$ or $(q_{1}q_{2}\cdots q_{x}1)$ in the next slot. Then the tags with the prefix $(q_{1}q_{2}\cdots q_{x})$ are further spitted into two sets. The process continues until only one tag responds. In this way, each tag can be recursively distinguished. Myung and Lee [9] [10] presents an Adaptive Query Splitting (AQS), which is an advanced version of the QT protocol. Since each tag can be deterministically identified, QT resolves the starvation problem, in which a specific tag may not be identified for a long time. Unfortunately, QT based approaches suffer from malicious interfering. When a 'malicious' tag keeps responding, QT fails to identify any tag. However, a bad thing can be turned into a good one. In [20], the authors develop such a kind of 'malicious' tags, called 'blocker tags', to selectively protect consumer's privacy.

Reader-Tag and Reader-Reader collisions: Besides the tag-tag collisions, there are other two types of collisions in multi-reader environments: Reader-Tag collision and Reader-Reader collision. In a recent work $[21]$ $[25]$ , the authors analyze these two types of collisions. When a reader A is within another reader B's scanning field, the response from tags targeted at A will be 'drown' by B's signals. This collision is defined as Reader-Tag collision, which can be addressed by assigning different channels to adjacent readers, or scheduling their interrogations into different slots. If a region is overlapped by two readers' scanning signals, the tags within this region cannot differentiate the signals simultaneously emitted from two readers. Such a collision is called Reader-Reader collision. The effective way to address the Reader-Reader collision is to avoid activating two readers at the same time. In our work, the term of collision only refers to tag-tag collisions. We assume that there are no collisions of other two types.

Bitwise boolean sum model: Recently, the bitwise Boolean sum model is widely used in the design of RFID security protocols. Choi and Roh [6] observe that the strength of signals through the forward channel, i.e., from the reader to tags, should be stronger than that of the backward channel, i.e., from tags to the reader. In QT based algorithms, since the reader utilized queries with increasing prefix via the forward channel, if some eavesdroppers within the channel hear the query, they can retrieve the tag's ID. Therefore, the authors in [5] propose a backward channel based protection method. The main idea is to allow the reader to send a randomly generated pseudo-ID. The pseudo-ID, mixed with the tag's real ID through a bitwise Boolean sum operation, is sent to the reader. The reader utilizes the pseudo-ID to resolve the real ID from the overlapped signals. Since the eavesdropper lacks the knowledge of pseudo-IDs, it cannot know the real ID. Lim et al [5] also focus on the backward channel based protection. They propose a randomized bit-encoding scheme to strengthen the privacy for RFID tags and alleviate the 'same-bit' problem, in which some bits of the ID could be disclosed. They also define an entropy-based metric to effectively measure the performance of privacy protection.

# III. EFFICIENCY OF EXISTING ANTI-COLLISION ALGORITHMS

To elaborate the shortcoming of CRC-CD based collision detection functions, we revisit the principles and efficiency

Table I
NOTIONS 

<table><tr><td>Notion</td><td>Definition</td></tr><tr><td> $\mathcal{F}$ </td><td>The frame length</td></tr><tr><td> $n$ </td><td>The number of tags within the reader’s detecting range</td></tr><tr><td> $m$ </td><td>The number of tags transmitting IDs simultaneously in one slot</td></tr><tr><td> $\vee$ </td><td>Bitwise boolean sum operation</td></tr><tr><td> $s_{i}$ </td><td>Signal sent by the  $i$ -th tag</td></tr><tr><td> $s$ </td><td>Signal received by reader</td></tr><tr><td> $crc(.)$ </td><td>CRC operation</td></tr><tr><td> $r$ </td><td>Random number( a positive integer)</td></tr><tr><td> $c$ </td><td>Checksum</td></tr><tr><td> $\oplus$ </td><td>Concatenation operation</td></tr><tr><td> $|s|$ </td><td>The length of the signal  $s$ </td></tr><tr><td> $\overline{s}$ </td><td>Bitwise complement operation</td></tr><tr><td> $\tau$ </td><td>The time consumed for transmitting one bit</td></tr><tr><td> $l_{id}, l_{prm}, l_{crc}$ </td><td>The length of tag’s ID, collision preamble, and CRC code</td></tr><tr><td> $N_{0}, N_{1}, N_{c}$ </td><td>The number of idle slots, single slots, and collided slots</td></tr><tr><td> $\lambda$ </td><td>The throughput of anti-collision algorithm</td></tr></table>

of FSA and BT based anti-algorithms. For ease of exploration, we summarize the main notions in Table I.

# A. Framed Slotted ALOHA based algorithms

Framed Slotted ALOHA (FSA) based algorithms [2] [3] [7] [8] employ a randomized method to reduce the collision probability. In a FSA algorithm, the reader divides a detecting frame into $\mathcal{F}$ slots. Each tag randomly selects a slot in the frame for transmitting its ID. In a given slot, multiple tags may transmit their ID simultaneously and thereby yield a collision. In this case, each collided tag will transmit its ID in a randomly chosen slot in the next frame. This procedure continues until all tags have been successfully identified.

Before showing the efficiency of FSAs, we introduce several necessary definitions. In the i-th slot of a detecting frame of FSA, we denote the random variable $X_{i}=1$ as the event that NONE of tags responds, $Y_{i}=1$ as the event that only one tag transmits its ID, and $Z_{i}=1$ as the event that a collision happens. Note that $X_{i}+Y_{i}+Z_{i}=1$ for any slot i in the detecting frame. Let $N_{0}=\sum_{i=1}^{F}X_{i}$ to denote the total number of idle slots, $N_{1}=\sum_{i=1}^{F}Y_{i}$ to denote the total number of single slots, and $N_{c}=F-N_{0}-N_{1}$ to denote the total number of collision slots. We define the throughput $\lambda$ of FSA as

$$
\lambda = \frac {N _ {1}}{N _ {0} + N _ {1} + N _ {c}}
$$

Lemma 1: In a detecting frame with $\mathcal{F}$ slots, if $n \approx \mathcal{F}$ , the maximum throughput of FSA is given by $\lambda_{max} \approx 0.37$ , where $n$ denotes the total number of tags.

Proof: Since

$$
N _ {1} = \sum_ {i = 1} ^ {\mathcal {F}} Y _ {i} = \mathcal {F} \binom {n} {1} \left(\frac {1}{\mathcal {F}}\right) \left(1 - \frac {1}{\mathcal {F}}\right) ^ {n - 1}
$$

$$
\approx n e ^ {- n / \mathcal {F}}
$$

, we have

$$
\lambda = \frac {N _ {1}}{N _ {0} + N _ {1} + N _ {c}} = \left(\frac {n}{\mathcal {F}}\right) e ^ {- n / \mathcal {F}}
$$

We can achieve the maximum throughput by computing the partial derivative of $\lambda$ with respect to $\mathcal{F}$ .

$$
\frac {\partial \lambda}{\partial \mathcal {F}} = - \frac {n}{\mathcal {F} ^ {2}} e ^ {\frac {- n}{\mathcal {F}}} + \frac {n ^ {2}}{\mathcal {F} ^ {3}} e ^ {- \frac {n}{\mathcal {F}}} = 0
$$

Therefore, the optimal length of frame is $\mathcal{F} = n$ , and the maximum throughput is 0.37.

$$
\lambda_ {m a x} = \frac {1}{e} \approx 0. 3 7
$$

From Lemma 1, we observe that only 37% slots are used by FSAs to successfully identify tags, while more than 63% slots are under utilized in the entire identification procedure. In addition, FSAs suffer from a potential flaw, 'tag starvation problem' [9], where some specific tags are unable to complete the identification for a long time if they always collide with others.

# B. Binary Tree based algorithms

The Binary Tree (BT) based anti-collision algorithms $[3]$ $[10]$ employ a virtual binary tree to organize the IDs of tags. For identifying a tag, the reader lunches a slotted identification procedure and recursively probe the tree from the root to leaves. Every tag owns a counter, in which the value is initialized as 0. In each slot, a tag transmits its ID if and only if the value of its counter equals to 0. At the very beginning, all tags transmit their ID concurrently. After each slot, the reader claims the type of this slot, i.e., the slot is idle, single, or collided. According to the reader's report, each tag changes its counter. If a collision happens in the previous slot, the tags which are involved in the collision randomly select 0 or 1, and add the number to the counter. The other tags which are not involved in collision directly increase their counter by 1. Consequently, the entire tag set is split into two subsets. In one subset, each tag's counter is 0. In the other subset, each tag's counter is equals or greater than 1. In a non-collided slot, all tags decrease their counter by 1. The tags that have been identified keep silent until the identification process terminates. A BT based anti-collision algorithm is illustrated in Figure 2. We examine the average throughput of BT via Lemma 2.

![](images/9010c5cee1bba94a249a96e946a738a694cd7abb4adb0cfc4ceb54c7ea58c41f.jpg)



Figure 2. The process of BT algorithm.

Lemma 2: For identifying n tags using BT based algorithms, the average total number of needed slots is 2.885n, including 1.443n collided slots, 0.442n idle slots, and n single slots. The average throughput $\lambda_{avg} = 0.35$ .

Proof: Borrowing the conclusion from [11] [12], the average number of collided slots is 1.443n, and the average number of idle slots is 0.442n in the whole process. Hence, we obtain the average throughput of BT as

$$
\lambda_ {a v g} = \frac {n}{1 . 4 4 3 n + 0 . 4 4 2 n + n} = 0. 3 5
$$

Base on Lemma 1 and 2, we can find that both FSAs and BTs can only use 35% – 37% slots to successfully identify tags, while more than 60% slots are not utilized. If we can shorten the time consumed for identifying the types of unused slots, we can improve the efficiency of anti-collision algorithms significantly.

# IV. QUICK COLLISION DETECTION

In this section, we formulate the collision detection problem. We then present our collision detection methodology, Quick Collision Detection (QCD) scheme.

# A. Problem Formulation

When a collision occurs, the physical signals emitted by multiple tags are overlapped, so that they are indistinguishable for identifying the tags. Indeed, the overlapped signals can be considered as a bitwise Boolean sum. Given that there are m tags selecting a given slot t, the final signal received by the reader is $s = s_{1} \vee s_{2} \vee \cdots \vee s_{m} = \vee_{i=1}^{m} s_{i}$ and $|s| = |s_{1}| = \cdots = |s_{m}|$ , where s denotes the final signal received by the reader, $s_{i}$ denotes the signal sent by the i-th tag, $\vee$ represents the bitwise Boolean sum operation, and $|s|$ denotes the length of the signal.

Existing approaches mainly employ CRC-CD for collision detection. For example, according to the well-known RFID standard, EPC Class-1 Gen-2 [2], a tag transmits its EPC ID (64 bits) as well as a CRC code (32 bits) to the reader in a given slot. The reader then computes a CRC code of the received ID and compares the result with the received CRC code. If they are not match, a collision happens.

Otherwise, there is no collision. As shown in Figure 4, solving the collision detection problem through CRC-CD algorithm is equivalent to deciding whether the value of $crc(\vee_{i=1}^{m}id_{i})$ is equal to the value of $\vee_{i=1}^{m}crc_{i}$ . According to the analysis in [4], the error of CRC is $2^{-r}$ , where the r is the strength of CRC. For example, the error of CRC-32 is $1/2^{32}$ . Such an error is negligible for practical applications. However, CRC is a sophisticated error-detection and error-correction technique for the capacity-limited RFID tag. CRC requires the tag to allocate relatively large computing resource, while some functions of CRC, for example the error correction, are not necessary for detecting collisions.

![](images/1b0fb388ad8ca1c7909357d5666153ba2f4cb68370ac96274cb0fbf2046c54b7.jpg)



![](images/7873461c89cda8cdb665bc21345b794161415d8cf2ce9807264877cfc8859fee.jpg)



![](images/a5c550f751463394efd897bc3fd9af3e5f585c0f699092c279dd067b4e7e7a2e.jpg)



Figure 3. Tag identification procedure with preamables

For improving the collision detection, we aim to detect all collisions as quickly as possible with low computation complexity. We take this objective to guide the design of our detection scheme. Different from CRC-CD based approaches, we allow each tag to send a collision preamble before transmitting its ID. The preamble comprises a random positive integer $r_{i}$ and an additional checking code $c_{i}$ . Namely, the collision preamble is $r_{i} \oplus c_{i}$ , where the $\oplus$ denotes the concatenation operation. Therefore, if there are m ( $m \geq 1$ ) tags concurrently transmitting their preambles in a given slot, the final signal received by the reader is $s = r \oplus c$ , where $r = \vee_{i=1}^{m} r_{i}$ and $c = \vee_{i=1}^{m} c_{i}$ . We define the function $f(r_{i}) = c_{i}$ as a collision function and elaborate its definition as follows:

Definition 1 (Collision function): Given that a set of positive integers $R = \{r_{1}, r_{2}, \cdots, r_{m}\}$ , where $m \geq 1$ , and there are at least two elements are not equal in R when m > 1, $f(x)$ is a collision function if it meets the conditions that m > 1 if and only if $f(\vee_{i=1}^{m} r_{i}) \neq \vee_{i=1}^{m} f(r_{i})$ .

With above definition, collision detection problem can be formalized as follows. Suppose that there are $m$ ( $m \geq 1$ ) tags choosing a given slot to transmit their IDs. In this slot, each of these m tags selects a random positive integer $r_i$ and transmits $r_i \oplus f(r_i)$ . We assume that if $m > 1$ , there are at least two tags' random integers are different. Based on Definition 1, the collision detection problem is equivalent to determining whether $f(\vee_{i=1}^m r_i)$ is equal to $\vee_{i=1}^m f(r_i)$ . If $f(\vee_{i=1}^m r_i) = \vee_{i=1}^m f(r_i)$ , there is only one tag replying in the slot, i.e., $m = 1$ . Otherwise, a collision happens and hence $m > 1$ . Figure 4 illustrates the situation when a collision happens.

![](images/3dea97546969c2182f1188dcc1a9164c71ffaf7d39115c377b774ab2ab22bc93.jpg)



Figure 4. Formulation for collision detection problem

Based on the received s, the reader can distinguish the type of given slot and perform operations accordingly. If the slot is idle or collided, the reader moves to next slot. If the slot is 'single', the reader commands the tag to report ID. Figure 3 shows the tag identification procedure. Note that in QCD, the length of a single slot is different from that of an idle or collided slot. Moreover, tags only transmit their collision preambles in idle or collided slots in QCD. In contrast, previous approaches require each tag to transmit the ID and CRC code in any types of slots. Therefore, the variable-length mechanism of QCD can reduce the time consumed for the transmission in both idle and collided slots.

# B. Quick Collision Detection

To improve the detecting efficiency, we aim to seek a simple and fast collision detection function $f(r)$ for QCD. There are a large number of collision functions in the literature. Among them, we find that the function $f(r) = \bar{r}$ fulfills our requirements, where $\bar{r}$ denotes the bitwise complement operation. We prove the feasibility and correctness of this selection as follows.

Theorem 1: if $(r) = \bar{r}$ is a collision function, where $\bar{r}$ is bitwise complement of $r$ .

Proof: Given a positive integer set $R = \{r_{1}, r_{2}, \cdots, r_{m}\}$ and $m \geq 1$ . If m > 1, we assume that there are at least two different elements in R. We need to prove the following two claims:

1) $m > 1 \Rightarrow f(\vee_{i=1}^{m}) \neq \vee_{i=1}^{m} f(r_{i})$

Since m > 1, we assume that $r_{i} \neq r_{j}$ , where $r_{i}, r_{j} \in R$ . Hence, there must exist a $k, 1 \leq k \leq |r|$ , such that the k-th bit in $r_{i}$ is not equal to that in $r_{j}$ , namely $r_{i}^{k} \neq r_{j}^{k}$ , where $r^{k}$ denotes the k-th bit in r. Since $r_{i}^{k} \neq r_{j}^{k} \Rightarrow r_{i}^{k} \vee r_{j}^{k} = 1$ , according to the principle of Boolean sum [13], the Boolean sum operation on each bit is independent with those on other bits. Thus, we have $(r_{i} \vee r_{j})^{k} = 1 \Rightarrow (\vee_{i=1}^{m} r_{i})^{k} = 1$ . The bitwise complement on one bit is also independent with those on other bits, thus

$$
\big (f \big (\vee_ {i = 1} ^ {m} r _ {i} \big) \big) ^ {k} = \left(\overline {{\vee_ {i = 1} ^ {m} r _ {i}}}\right) ^ {k} = 0
$$

Algorithm 1 Quick Collision Detection   
Input: final signal s and slot t
Output: The type of slot t:
    0 - represents idle slot
    1 - represents single slot
    2 - represents collided slot
1: The reader receives final signal s
2: if s = 0 then
3: return 0
4: else
5: The reader retrieves r and c from s
6: if c = f(r) then
7: return 1
8: else
9: return 2
10: end if
11: end if

On the other hand,

$$
\begin{array}{l} r _ {i} ^ {k} \neq r _ {j} ^ {k} \Rightarrow (\bar {r _ {i}}) ^ {k} \neq (\bar {r _ {j}}) ^ {k} \\ \Rightarrow (f (r _ {i})) ^ {k} = (\bar {r _ {i}}) ^ {k} \neq (\bar {r _ {j}}) ^ {k} = (f (r _ {j})) ^ {k} \\ \Rightarrow (f (r _ {i})) ^ {k} \vee (f (r _ {j})) ^ {k} = 1 \\ \end{array}
$$

Thus,

$$
\left(\vee_ {i = 1} ^ {m} f (r _ {i})\right) ^ {k} = 1
$$

We have $(f(\vee_{i=1}^{m}r_{i}))^{k}=0$ and $(\vee_{i=1}^{m}f(r_{i}))^{k}=1$ , which indicates that the k-th bit in $f(\vee_{i=1}^{m}r_{i})$ is different from the k-th bit in $\vee_{i=1}^{m}f(r_{i})$ . Therefore,

$$
f (\vee_ {i = 1} ^ {m} r _ {i}) \neq \vee_ {i = 1} ^ {m} f (r _ {i})
$$

2) $f(\vee_{i = 1}^{m}r_{i})\neq \vee_{i = 1}^{m}f(r_{i})\Rightarrow m > 1)$

Suppose $m = 1$ , we have $f(\vee_{i=1}^{m} r_i) = f(r_i) = \bar{r}_i$ and $\vee_{i=1}^{m} f(r_i) = \vee_{i=1}^{m} \bar{r}_i = \bar{r}_i$ . This is a contradiction with our assumption. Hence, $m > 1$ .

In summary, $f(r) = \bar{r}$ is a collision function.

Utilizing $f(r) = \bar{r}$ as the collision function, we present QCD algorithm in Algorithm 1. Note that we have a weak assumption that if more than one tag replies concurrently, there are at least two tags emitting different random integers. We define the length of the random integer as the strength of QCD, and denote it as l-bits. The probability that our assumption does not hold is $0.5^{lm} \leq 0.5^{2l}$ . There is a tradeoff when selecting the l. A smaller l results in smaller integers, which increases the probability of different tags selecting a same integer. In this case, the computing result is incorrect. If the l is too large, it may incur high communication latency, although the correctness can be guaranteed with high probability. In practice, we recommend to adopt l = 8. Correspondingly, the length of collision preamble is 16-bit, and we will further discuss the tradeoff via simulations in Section VI.

# V. EFFICIENCY ANALYSIS

QCD significantly improves the efficiency for anticollision algorithms on twofold. First, utilizing bitwise complement operation saves a large amount of time consumed on collision detection. Second, the communication latency of QCD can be dramatically reduced by using the preamble mechanism. In this section, we theoretically analyze the improvement made by QCD on FSA and BT based approaches. We also compare QCD with CRC-CD in terms of complexity and overhead.

For ease of exploration, we assume that the time for transmitting one bit is $\tau$ , the length of ID is $l_{id}$ -bits, the length of CRC codes is $l_{crc}$ -bits, and the length of collision preambles is $l_{prm}$ -bits.

# A. Improvement on FSA

According to Lemma 1, the maximum throughput of FSA is $37\%$ . Therefore, the minimum total number of slots for identifying $n$ tags is $n / 0.37 = 2.7n$ . The transmission time is $t_{crc} = 2.7n\tau (l_{id} + l_{crc})$ if using CRC-CD. For QCD, the time is $t_{qcd} = n\tau (l_{prm} + l_{id}) + 1.7n\tau l_{prm}$ . Compared to CRC-CD, the minimum efficiency improvement made by QCD, denotes as EI, is defined as follows.

$$
E I = \frac {t _ {c r c} - t _ {q c d}}{t _ {c r c}} = \frac {0 . 6 2 9 3 l _ {i d} + l _ {c r c} + l _ {p r m}}{l _ {c r c} + l _ {i d}}
$$

Following the specification of EPC [2], we adopt $l_{id} = 64$ and $l_{crc} = 32$ . We theoretically summarize the minimum efficiency improvement on FSA based approaches with different strength of QCD in Table II. For example, when the strength of QCD is 8-bit, QCD improves the efficiency of identification process for FSAs up to 58.64%.

Table II
EI ON FSA WITH VARIOUS STRENGTH OF QCD 

<table><tr><td>Strength of QCD</td><td>EI</td></tr><tr><td>4-bit</td><td>≥ 0.6698</td></tr><tr><td>8-bit</td><td>≥ 0.5864</td></tr><tr><td>16-bit</td><td>≥ 0.4198</td></tr></table>

Table III AVERAGE EI ON BT WITH VARIOUS STRENGTH OF QCD 

<table><tr><td>Strength of QCD</td><td>EI</td></tr><tr><td>4-bit</td><td>≈ 0.6856</td></tr><tr><td>8-bit</td><td>≈ 0.6023</td></tr><tr><td>16-bit</td><td>≈ 0.4356</td></tr></table>

Table IV COMPARISON BETWEEN CRC-CD AND QCD 

<table><tr><td>Scheme</td><td>CRC-CD</td><td>QCD</td></tr><tr><td># of instruction</td><td>More than 100 instructions</td><td>Only 1 instruction</td></tr><tr><td>Complexity</td><td> $\mathcal{O}(l)$ </td><td> $\mathcal{O}(1)$ </td></tr><tr><td>Memory</td><td>1KB</td><td>16bits</td></tr><tr><td>Transmission</td><td>96bits</td><td>16bits</td></tr></table>

Table V
SIMULATION SETUP 

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Simulation Area</td><td>100m × 100m</td></tr><tr><td>Number of readers</td><td>100</td></tr><tr><td>Identification range of the reader</td><td>3m</td></tr><tr><td>Tag ID</td><td>Randomly selected 96-bit ID</td></tr></table>

Table VI SIMULATION CASES 

<table><tr><td>Case</td><td># of tags</td><td># of slots</td></tr><tr><td>I</td><td>50</td><td>30</td></tr><tr><td>II</td><td>500</td><td>300</td></tr><tr><td>III</td><td>5000</td><td>3000</td></tr><tr><td>IV</td><td>5000</td><td>30000</td></tr></table>

# B. Improvement on BT

According to Lemma 2, the average throughput of BT based approaches is 0.35. Therefore, the average total number of slots for identifying n tags is $n/0.35 = 2.885n$ . If using CRC-CD, the communication time is $2.885n(l_{id} + l_{crc})\tau$ . In contrast, the communication time is $1.885nl_{prm}\tau + n(l_{prm} + l_{id})\tau$ if using QCD. If $l_{id} = 64$ bits and $l_{crc} = 32$ bits, the average EI is given as follows.

$$
E I = \frac {t _ {c r c} - t _ {q c d}}{t _ {c r c}} = \frac {0 . 6 5 3 3 l _ {i d} + l _ {c r c} - l _ {p r m}}{l _ {c r c} + l _ {i d}}
$$

We summarize the improvement on BT based approaches in Table III. Especially, if adopting 8-bit strength, QCD can contribute 60.23% efficiency improvement.

# C. CRC-CD vs. QCD

QCD outperforms CRC-CD due to the following advantages. First, CRC-CD is based on cyclic redundancy check algorithm whose complexity is $\mathcal{O}(l)$ , where $l$ is the length of ID, while the complexity of QCD's bitwise complement function is $\mathcal{O}(1)$ . Second, a CRC-CD operation requires more than 100 CPU instructions while QCD only needs 1 instruction in the checksum computation. Third, CRC-CD based approaches need to transmit 96-bits CRC codes in both idle and collided slots, while QCD only needs to transmit 16-bits codes for detecting collisions. Finally, CRC-CD requires 1KB extra memory for containing the lookup table, but the bitwise complement function only requires 16 bits to store the signal. We also compare QCD with CRC-CD based approaches in terms of complexity and overhead in Table IV.

# VI. PERFORMANCE EVALUATION

In this section, we evaluate our design via comprehensive simulations. Our evaluation focuses on four metrics: accuracy, delay, utilization rate, and efficiency improvements both on FSA and BT.

# A. Simulation Methodologies

The simulation setup is shown in Table V. Each tag is designed to have a 64-bits unique ID and 32-bits CRC code. We consider four cases in the simulation, in which the number of tags ranges from 50 to 50000 as shown in Table VI. These cases represent different application scenarios in real RFID systems. We repeat each test for 100 rounds with the same parameters, and report the average. To clear show the difference, we ignore the time synchronization and broadcasting identification queries during the transmission, which are the same in both QCD and CRC-CD based approaches.

# B. Accuracy

The first metric is the accuracy of collision detection, which is highly related to the strength of QCD. For reflecting the detection accuracy, we suppose the total number of collision slots is $n_{c}$ and the total number of correctly detected slots by QCD is $n_{c}^{\prime}$ , we define the accuracy of collision detection as

$$
A c c u r a c y = \frac {n _ {c} ^ {\prime}}{n _ {c}}
$$

In our experiments, we first employ FSA algorithm for checking the accuracy of collision detection of QCD with strength settings as 4, 8, and 16-bits, respectively. We present the accuracy result in Figure 5. We find that there are two ways to increase accuracy. On one hand, when enlarging the strength of QCD, the detection error is reduced. Indeed, setting the strength of QCD as 8-bits can achieve nearly $100\%$ accuracy. On the other hand, the total number of tags also has an impact on the detection accuracy. Reducing the number of tags can achieve higher accuracy. But this impact is not as significant as the change of QCD's strength. Especially, QCD can achieve nearly $100\%$ accuracy when taking 16-bits as the strength of QCD.

![](images/84ebaaf0e60471cec2e05b77684b9d57cada0f113c2188d2b82f8047ec28a6c7.jpg)



Figure 5. Accuracy comparison among different strength of QCD in four cases

Table VII FRAMED SLOTTED ALOHA BASED SIMULATION 

<table><tr><td>Case</td><td># of frame</td><td># of idle slots</td><td># of single slots</td><td># of collided slots</td><td>Throughput</td></tr><tr><td>50</td><td>6</td><td>39</td><td>50</td><td>110</td><td>0.25</td></tr><tr><td>500</td><td>7</td><td>1376</td><td>500</td><td>394</td><td>0.22</td></tr><tr><td>5000</td><td>8</td><td>15217</td><td>5000</td><td>3962</td><td>0.20</td></tr><tr><td>50000</td><td>8</td><td>164477</td><td>50000</td><td>39622</td><td>0.20</td></tr></table>

# C. Utilization Rate

The second metric is the Utilization Rate (UR). This parameter is defined as the ratio of the time consumed for transmitting IDs of tags to the total time of identification. This parameter shows 'effective time' we spend to successfully identify tags. We define the UR of QCD as

$$
U R = \frac {N _ {1} l _ {i d} \tau}{N _ {1} (l _ {p r m} + l _ {i d}) + (N _ {c} + N _ {0}) l _ {p r m} \tau}
$$

In fact, UR reflects the throughput of anti-collision algorithms. A higher UR contributes a larger throughput of successfully identified tags. A high strength, however, leads to a low throughput of QCD. To elaborate the tradeoff, we check the UR of QCD and show the result in Table IX. From the table, we can observe that when the UR decreases, the strength of QCD increases. In particular, if we employ 16-bit as the strength, the UR of QCD dramatically drops to below 50 % in all cases.

Tables VII and VIII show the distribution of slots and throughput when deploying QCD to the FSAs and BTs, respectively. In case I, we employ 50 tags and set the frame size as 30 slots. As a result, a FSA based algorithm may totally need 119 slots in average, including 39 idle slots, 50 single slots, and 110 collided slots. The throughput of FSAs in case I, II, III, and IV are 25%, 22%, 20%, and 20%, respectively. Note that the throughput is below the upper bound, i.e., 37% as we discussed in Section III, because the optimal frame size is not employed in our simulation. In practice, the reader cannot exactly know the number of tags in advance. Therefore, it is difficult to set the frame length as the optimal one. Detail discussion about the optimal frame size can be found in [8], [14]–[16].

Moreover, we find that the throughput of BTs is around 35%, which demonstrates the correctness of Lemma 2. Meanwhile, this observation also validates our assumption that the majority part of the identification process is consumed for dealing with collided or empty slots.

Combining above observations, we suggest taking 8-bits as the strength of QCD in practice, which is able to achieve a good balance between the accuracy and throughput of successfully identified tags.

# D. Identification Delay

Fast identification is the most significant factor in the mobile tag environment. The tag may move out of the

Table VIII
BINARY TREE BASED SIMULATION 

<table><tr><td>Case</td><td># of frame</td><td># of idle slots</td><td># of single slots</td><td># of collided slots</td><td>Throughput</td></tr><tr><td>50</td><td>137</td><td>19</td><td>50</td><td>68</td><td>0.36</td></tr><tr><td>500</td><td>1426</td><td>214</td><td>500</td><td>712</td><td>0.35</td></tr><tr><td>5000</td><td>14374</td><td>2187</td><td>5000</td><td>7187</td><td>0.34</td></tr><tr><td>50000</td><td>143998</td><td>21999</td><td>50000</td><td>71999</td><td>0.34</td></tr></table>

Table IX
UR COMPARISON AMONG DIFFERENT STRENGTH QCD 

<table><tr><td>Case</td><td>4-bit</td><td>8-bit</td><td>16-bit</td></tr><tr><td>50</td><td>66.78%</td><td>50.13%</td><td>33.44%</td></tr><tr><td>500</td><td>63.80%</td><td>46.84%</td><td>30.58%</td></tr><tr><td>5000</td><td>62.33%</td><td>45.27%</td><td>29.26%</td></tr><tr><td>50000</td><td>61.15%</td><td>44.03%</td><td>28.24%</td></tr></table>

reader's range before it identified by the reader if the identification is slow. We define the identification delay of tag $t_i$ as the interval between the start of identification and the time when the tag is identified. We utilize the average delay to understand the relationship between the delay and collision detection. The average delay is computed as

$$
D _ {a v g} = \frac {\sum_ {t _ {i} \in T} D _ {t _ {i}}}{| T |}
$$

where $D_{t_i}$ is the delay of tag $t_i$ and $T$ is the set of tags.

Figure 6 presents the average delay of CRC-CD (8-bit strength) and QCD. Evident from the graph, QCD significantly reduces the identification delay more than 80% in four cases. Specially, the $D_{avg}$ of QCD more sharply concentrate around the mean, which indicates QCD is more stable than CRC-CD.

# E. Efficiency Improvements

The last important metric is the efficiency improvement in terms of transmission latency. Leveraging the definition in Section V-A, we exam the EI of FSAs and BTs, respectively.

We adopt QCD to FSAs and BTs to compare the performance of QCD with that of CRC-CD. Figure 7(a) plots the comparison on the time consumption between CRC-CD based FSAs and QCD (8-bit strength) based FSAs. We observe that QCD based FSAs spend less than half of transmission time of CRC-CD based FSAs in all cases. When the number of tags increases, the difference also drastically enlarges.

Figure 7(b) shows the comparison on the time consumption between CRC-CD based BTs and QCD based BTs (with the 8-bits strength). The result also indicates QCD can significantly improve the latency of identification.

We show the EI of QCD based FSA in Figure 8(a). If setting the strength as 8-bits, QCD base FSAs shorten the time cost to 65%, 68%, 69%, and 70% of that used by CRC-CD based FSAs in case I, II, III, and IV, respectively. The values of EI in those four cases are all larger than the theoretic lower bound (41.98%). Especially, when we enlarge the strength of QCD, for example from 4-bits to 16-bits, the value of EI decreases due to the increased transmission overhead.

![](images/6fa3923a1bf0f39089ff1703211971919f37af314c32252170c7095b4011a4ba.jpg)  
Figure 6. Comparison of identification delay between CRC-CD and QCD

![](images/adc62adc493fea74ac0b6f64246b182b01d62b11cb4630eef94b708e17b88853.jpg)



![](images/7eb7333bd6365ab8183a53896f5483bdd8018edc789559a1a06274149eaeab5a.jpg)



(a) FSA   
![](images/8ba2f8781d40ddbbdd72c3c461a695781a3aa17586a853041b83bc156bafdf84.jpg)



![](images/760d48f7595cb55efd5912e50d1ae6162870871221b73a2f06b2b850a14d4391.jpg)



(b) BT   
Figure 7. The comparison on transmission time ( $\mu s$ ) between CRC-CD and QCD with the collision preamble of 8-bit strength on FSA and BT

Figure 8(b) plots the EI made by QCD against CRC-CD for BTs. In particular, the value of EI tends to be stable around an average value 48%, 60.23%, and 78% under the three strength settings. This result shows that the BT algorithm is more stable, which is also demonstrated by [11].

![](images/7a673c103c10ea779729b00c3577e66b3271ee49350edcb07b27b6b865836d28.jpg)



(a) FSA

![](images/d2093b869a8fcefa0d222459390e7d2a91437ce0b0d0a98f9695f97d41e35bca.jpg)



(b) BT   
Figure 8. Efficiency Improvement on FSA and BT

# VII. CONCLUSION

Collision detection is a crucial task in RFID systems. In this paper, we propose QCD, a fast and efficient collision detection scheme that does not require special hardware supports, e.g., the CRC design. Our theoretical analysis and comprehensive simulation results show that QCD can achieve accurate detection, and significantly reduce the transmission latency and communication overhead for existing anti-collision algorithms, compared with CRC-based approaches. In the future, we plan to explore more practical issues in the implementation of this scheme. Indeed, this design can be easily extended to other wireless fields, for example the neighbor discovery $[26]$ and coverage $[27]$ $[29]$ $[31]$ of sensor networks, and ad hoc network $[30]$ .

# ACKNOWLEDGMENT

This work is supported in part by National Natural Science Foundation of China (NSFC) (No.60933003 No.60736016, No.60873262, and No.60903155), China Postdoctoral Science Foundation funded project (No.20090461298) Hong Kong Innovation and Technology Fund GHP/044/07LP and ITP/037/09LP, National High Technology Research and Development Program of China (863 Program)(2009AA01Z116), the Science and Technology Research and Development Program of Shaanxi Province under Grant No.2008KW-02, and IBM Joint Project.

# REFERENCES

[1] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, "LANDMARC: Indoor Location Sensing Using Active RFID," in Proceedings of IEEE PerCom, 2003.   
[2] "EPCglobal Radio-Frequency Identity Protocols Class-1 Generation-2 UHF RFID Protocol for Communications at 860 MHz-960MHz Version 1.0.9," 2005.   
[3] "Information Technology Automatic Identification And Data Capture Techniques-Radio Frequency Identification For Item Management Air Interface. Part 6. Parameters for Air interface communications at 860-960 MHZ," ed: Standard ISO 18000-6, 2003.   
[4] J. F. Kuros and K. W. Ross, Computer Networking: A Top-Down Approach Featuring the Internet: Pearson Education, 2005.   
[5] T. L. Lim, T. Li, and S. L. Yeo, "Randomized Bit Encoding for Stronger Backward Channel Protection in RFID Systems," in Proceedings of PerCom, 2008.   
[6] W. Choi and B. H. Roh, "Backward Channel Protection Method for RFID Security Schemes Based On Tree-Walking Algorithms," in Proceedings of ICCSA, 2006.   
[7] F. C. Schoute, "Dynamic Frame Length ALOHA," IEEE Transactions on Communications, 1983.   
[8] S. R. Lee, S. D. Joo, and C. W. Lee, "An Enhanced Dynamic Framed Slotted ALOHA Algorithm For RFID Tag Identification," in Proceedings of MobiQuitous, 2005.   
[9] J. Myung and W. Lee, "Adaptive Splitting Protocols For RFID Tag Collision Arbitration," in Proceedings of MobiHoc, 2006.   
[10] J. Myung and W. Lee, "Adaptive Binary Splitting: A RFID Tag Collision Arbitration Protocol for Tag Identification," Mobile Networks and Applications, 2006.   
[11] J. I. Capetanakis, "Tree Algorithms For Packet Broadcast Channels," IEEE Transactions on Information Theory, 1979.   
[12] D. R. Hush and C. Wood, "Analysis Of Tree Algorithms For RFID arbitration," IEEE Transactions on Information Theory, 1998.   
[13] A. Papoulis, Probability Random Variables And Stochastic Processes: McGraw-Hill, 1965.   
[14] M. Kodialam, T. Nandagopal, and W. C. Lau, "Anonymous Tracking Using RFID Tags," in Proceedings of INFOCOM, 2007.   
[15] M. Kodialam and T. Nandagopal, "Fast and Reliable Estimation Schemes in RFID Systems," in Proceedings of MobiCom, 2006.   
[16] C. Qian, H. Ngan, and Y. Liu, "Cardinality Estimation for Large-scale RFID Systems," in Proceedings of PerCom, 2008.   
[17] L. G. Roberts, "ALOHA Packet System With And Without Slots And Capture," in Proceedings of SIGCOMM, 1975.

[18] C. Law, K. Lee, and K. Y. Siu, "Efficient Memoryless Protocol For Tag Identification," in Proceedings of DIALM Workshop, 2000.   
[19] F. Zhou, C. Chen, D. Jin, C. Huang, and H. Min, "Evaluating and Optimizing Power Consumption of Anti-Collision Protocols for Applications in RFID Systems," in Proceedings of ISLPED, 2004.   
[20] A. Juels, R. L. Rivest, and M. Szydlo, "The Blocker Tag: Selective Blocking of RFID Tags for Consumer Privacy," in Proceedings of CCS, 2003.   
[21] Z. Zhou, H. Gupta, S. R. Das, and X. Zhu, "Slotted Scheduled Tag Access in Multi-Reader RFID Systems," in Proceedings of ICNP, 2007.   
[22] K. Finkenzeller, RFID handbook: fundamentals and applications in contactless smart cards and identification: John Wiley & Sons Inc, 2003.   
[23] Li Lu, Jinsong Han, Lei Hu, Yunhao Liu, and Lionel M Ni, "Dynamic Key-Updating: Privacy-Preserving Authentication for RFID Systems", IEEE PerCom 2007, USA, March 2007.   
[24] Yunhao Liu, Zheng Yang, Xiaoping Wang, and Lirong Jian "Location, Localization, and Localizability", Journal of Computer Science and Technology (JCST), 25(2): 274-297, Mar, 2010.   
[25] Shao-Jie Tang, Jing Yuan, Xiang-Yang Li, GuiHai Chen, YunHao Liu, and JiZhong Zhao, "RASPberry: A Stable Reader Activation Scheduling Protocol in Multi-Reader RFID Systems", in Proceedings of IEEE ICNP 2009   
[26] Sudarshan Vasudevan, Don Towsley, Dennis Goeckel, Ramin Khalili, "Neighbor Discovery in Wireless Networks and the Coupon Collectors Problem", i n Proceedings of ACM Mobi-Com, 2009   
[27] Xiaole Bai, Santosh Kumar, Dong Xuan, Ziqiu Yun and Ten H. Lai, "Deploying Wireless Sensors to Achieve Both Coverage and Connectivity", in Proceedings of ACM MobiHoc, 2009   
[28] Daqiang Zhang, Jingyu Zhou, Minyi Guo, Jiannong Cao, Tianbo Li, "TASA: Tag-Free Activity Sensing Using RFID Tag Arrays", IEEE Transactions on Parallel and Distributed Systems, 2010   
[29] Xiaole Bai, Ziqiu Yun, Dong Xuan, Ten-Hwang Lai, Weijia Jia, "Optimal Patterns for Four-Connectivity and Full Coverage in Wireless Sensor Networks", IEEE Transactions on Mobile Computing, 2010   
[30] Cheng Wang, Xiang-Yang Li, Changjun Jiang, Shaojie Tang, Yunhao Liu and Jizhong Zhao, "Scaling Laws on Multicast Capacity of Large Scale Wireless Networks", in Proceedings of IEEE INFOCOM, 2009   
[31] X. Bai, Z. Yun, W. Jia and W. Zhao, "Pattern Mutation in Wireless Sensor Deployment", in Proceedings of IEEE INFOCOM, 2010