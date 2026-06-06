# Wonder: Efficient Tag Identification for Large-scale RFID Systems

Haoxiang Liu $^{*}$ , Kebin Liu $^{\dagger}$ , Wei Gong $^{\dagger}$ , Yunhao Liu $^{\dagger}$ , Lei Chen $^{*}$

\*Department of Computer Science and Engineering, Hong Kong University of Science and Technology

$^{\dagger}$ School of Software and TNList, Tsinghua University

Email: {hliuab, leichen}@cse.ust.hk, {gongwei, kebin, yunhao}@greenorbs.com

Abstract—Efficient tag identification is fundamentally required in large-scale RFID systems. Tag signal collision degrades identification efficiency as tag IDs involved in collision cannot be decoded. The situation becomes even worse in large-scale RFID systems when tag cardinality booms. Existing anti-collision protocols focus on either reducing collision probability or adopting spread spectrum techniques. Unfortunately, the former approach cannot resolve collision radically and the latter one occupies extra bandwidth resources. To address these issues, we propose to resolve tag collision using orthogonal Walsh code, in which tags map their IDs to a group of Walsh codes and transmit them sequentially. The reader can retrieve tag IDs by inverse mapping even under collision circumstances. We further design a new efficient tag identification protocol, Wonder, which reduces identification time without spreading the bandwidth. We conduct extensive simulations to examine its effectiveness and the results show that our protocol significantly improves identification efficiency over previous anti-collision protocols.

# I. INTRODUCTION

Radio Frequency Identification (RFID) has attracted increasing attentions nowadays due to its small form and ultra-low power. RFID technology can be used in a wide range of applications, such as access management, item tracking, and supply chain management $[1]$ , $[2]$ . An RFID system typically consists of readers and a large amount of tags. Each tag is attached to certain item and has its ID stored in the memory which can be retrieved by the reader in a contactless manner. Specifically, the reader transmits a RF signal as stimulus to the tags. Upon capturing the signal, tag responds its ID in a backscatter channel. So the reader can collect the IDs of tags for item identification.

A key challenge in tag identification process is signal collision. More precisely, when tags respond IDs to the reader simultaneously, the signals collide and no signal can be decoded correctly by the reader. Consequently, the tags have to retransmit their data, leading to system performance degradation. To address this tag-collision problem, many methods are introduced, namely TDMA [3], [4], [5], [6], [7] method and CDMA [8] method. In TDMA-based methods, tags are prevented from interfering with each other by transmitting in different time slots. One typical TDMA-based identification protocol is Frame Slotted Aloha (FSA), adopted as EPC Class-1 Generation-2 (C1G2) standard [9]. In CDMA-based methods, tags are assigned with different orthogonal or approximately orthogonal spreading codes, which are used to encode the transmitted data. Reader can then decode the transmitted data using the same encoding code, even if several concurrent transmissions are in the same frequency band. Despite their anti-collision property, those schemes are inefficient to tackle down the tag collision problem. For TDMA protocols, tags choose time slot for transmission independently, so collision is still likely to happen. Moreover, the performance deteriorates as the number of tags increases. One possible way to mitigate collision is to increase the number of available slots, but more slots result in lower efficiency. CDMA uses spread spectrum communication to allow multiple access, which can speed up the tag identification process by reading several tags simultaneously. However, CDMA significantly increases the spectrum width but it is infeasible to employ spread spectrum communication in spectrum limited circumstances. In addition, spread spectrum modulation imposes heavy overhead on tags.

The RFID-based airport baggage tracking system (RATS) is one of our ongoing projects. It is used to track customers' baggage in the airport to prevent baggage loss and incorrect placement by utilizing RFID technology. For example, customers' baggage might get lost while being unnoticed, and it also happens that baggage are incorrectly conveyed to a wrong airplane. RATS deals with both problems effectively. One may notice that the first problem is analogous to the well-studied missing tag problem, but the second problem is quite different. The incorrectly placed baggage is obvious not missing since it still can be identified by the reader. In our system as well as various other RFID systems, the IDs of entire tag set is known in advance because tags can be designed by the airport. This kind of RFID system is denoted as closed loop RFID system. For example in RATS, readers are connected to backend server which stores all tags' Electronic Product Codes (EPC). Each time, the reader might need to identify a subgroup of tags, which for example may belong to the same airplane. Since the reader does not know which tags are located in the reading area, it needs to identify all tags to prevent the interfusion of wrong tags. We are motivated by this project to design a fast and reliable tag identification protocol. We propose a novel Walsh code-based tag identification protocol Wonder.

![](images/6cf7b56cbd0cb5ea9b83e6efdcbb6e78824b41d33b3914ccdaf9482831e1dabe.jpg)



Fig. 1. Walsh code superposition.

Wonder resolves tag collision by utilizing a class of orthogonal codes called Walsh codes. Any two Walsh codes in the same code set are orthogonal to each other so that a Walsh code can be distinguished even when it superimposes with others. Other than transmitting IDs, tags map IDs to Walsh codes and transmit Walsh codes instead. Consequently, simultaneous channel access becomes possible since Walsh codes are collision resistant. However, we have a small number of Walsh codes while the ID space is huge. To address this challenge, we use the multiple Walsh codes to uniquely represent one ID. At the receiver end, the closed loop feature makes it possible to rebuild the tag IDs with corresponding received Walsh codes. In the rebuilding process, false positive identification can happen. We present probability analysis on false positive rate and further propose a solution that solves false positive problem and ensures identification reliability.

The main difference between this design and the traditional CDMA-based method are two fold. First, in our protocol tags transmit merely Walsh codes, while in CDMA, tags transmit ID modulated by spreading codes, which can be either Gold codes or Walsh codes. Second, CDMA is pure code division and our protocol is time division in essence. Tags still transmit in different slots although one slot can tolerate the simultaneous transmission of multiple tags.

The major contributions of this work are as follows:

- We apply the orthogonal Walsh code in the RFID tag identification to resolve tag collision. Differing conventional CDMA-based methods, we do not increase the spectrum width.   
- We propose efficient and reliable tag identification protocol under closed loop settings. The evaluation results show that our protocol is efficient. It reduces the overall identification time by an order of magnitude compared with several typical protocols.   
- We solve the false positive problem at the reader side and give probabilistic analysis of false positive rate. Furthermore, we have remedy methods in case false positive occurs,

TABLE I. CORRELATION RESULTS 

<table><tr><td>Correlation</td><td>Result(zero bit lag)</td></tr><tr><td> $sup \star w_1$ </td><td>4</td></tr><tr><td> $sup \star w_2$ </td><td>4</td></tr><tr><td> $sup \star w_3$ </td><td>4</td></tr><tr><td> $sup \star w_4$ </td><td>0</td></tr></table>

thereby ensuring the reliability.

The rest of this paper is organized as follows. In Section II related work is reviewed. In Section III, we introduce preliminary knowledge and our baggage tracking system. In Section IV, we addresses several design issues and propose our tag identification protocol Wonder. We conduct experiments in large RFID systems in Section V. The work is concluded in Section VI.

# II. RELATED WORK

The anti-collision tag identification protocols can be primarily classified into two types according to their anti-collision schemes. One is TDMA-based protocols and the other is CDMA-based protocols. The TDMA-based protocols can further be subdivided into two categories, namely aloha-based [3], [4], [5] and tree-based [6], [7]. Aloha-based protocols such as frame slotted aloha (FSA) [9], dynamic framed slotted aloha (DFSA) [4] and enhanced dynamic slotted aloha (EDFSA) [3] avoid tag collision by arranging tags to transmit in different time slots. However, tag collision cannot be thoroughly avoided in case multiple tags choose the same slot to transmit IDs. Tree-based approaches resolve tag collision by splitting collided tags into subsets, and schedule the subsets to transmit separately. The splitting process terminates until the subset contains only one tag and can then be identified. Thus, the identification process can be organized as a tree structure where each node in the tree represents a subset. Tree-based protocols split tags either using random binary number [10], [6] or query [11], [6].

Recently, physical layer signal processing techniques are exploited in resolving tag collision. Zhang et al. apply Analog Network Coding(ANC) proposed by Katti et al. [12] to improve reading throughput [13]. By subtracting the already decoded signals from a collided signal, the reader can resolve collision. This approach needs signal construction and subtraction in physical layer, while it is avoided in our method. What is more, Yue et al. [14] propose a bloom filter based tag identification and information collection protocol, which applies bloom filter in tag identification and achieves throughput improvement. It also assumes a closed loop setting where tag IDs are known in advance. The accuracy relies heavily on every bit in the bloom filter basis. Under noisy channel, however one bit is easily corrupted by noise, leading to false negative identification. As a result, identification reliability cannot be guaranteed. Kong et al. [15] design a parallel identification protocol that encodes tag ID into a specially designed pattern which makes the reader easily recover tag collision.

![](images/bd38dc0e6417b0a179a4e2c1f7ac0bb3db7f21377b6a6ff18fb98e898b9e5d2a.jpg)



Fig. 2. Illustration of a working section in RATS.

The CDMA-based approach is studied by Mutti et al. $[8]$ , in which code division multiplexing techniques are used to decode tag collision. The work also proposes a scheme that efficiently counts the number of tags based on spread-spectrum communication. However, as mentioned previously conventional spreading spectrum communication is not well applicable in circumstances where spectrum resource is limited. Also the complex encoding and decoding scheme makes it not suitable for large-scale RFID systems.

# III. PRELIMINARY

# A. Walsh Code

Walsh Code is a kind of orthogonal code. A Walsh code is a binary sequence which only consists of -1 and 1. A set of Walsh codes can be generated by applying Hadamard transform [16] repeatedly. There are totally $2^{l}$ Walsh codes in a set with length $2^{l}, l \in N^{+}$ . For example, if the length of Walsh code is $2^{2} = 4$ , then there are altogether 4 such Walsh codes.

One attractive property of Walsh code is its orthogonality. Specifically, the cross-correlation between any two Walsh codes in the same set is zero. Thus we can say that any two different Walsh codes are mutually orthogonal. In contrast, the auto-correlation between a Walsh code and itself has a spike when perfectly aligned. The correlation properties make it possible to distinguish one Walsh code from others in the same set. Even if several Walsh codes superimpose, we can still identify each of them by conducting correlation between the superimposed code and each Walsh code in the set. For example, we have four 4-bit Walsh codes, namely $w_{1}$ , $w_{2}$ , $w_{3}$ , and $w_{4}$ . Let the superimposed code be $sup = w_{1} + w_{2} + w_{3}$ , as shown in Fig. 1. We separately conduct correlation between sup and $w_{i} (1 \leq i \leq 4)$ . The results are shown in Table I. Through the results, we can easily find out that $w_{1}$ $w_{2}$ and $w_{3}$ reside in sup while $w_{4}$ does not.

# B. Framed slotted aloha

Framed Slotted Aloha Protocol (FSA) is a typical anti-collision protocol adopted as EPC C1G2 standard [9]. In FSA, the reader broadcasts a frame consisting

![](images/f433d012f4d70722c5a3591862af88d1dff0d6ec77d0a17cfe4ede41b709e889.jpg)



Fig. 3. Mapping from ID to Walsh codes, where i denotes the Walsh code index. For example, 1 means the first among all 128 codes.   
![](images/e022b4ab2788ffde3703ac5830d623999571061d646a258c62c1b7509428fd84.jpg)



Fig. 4. Walsh code transmission in one frame. Assume there are 4 tags and each of them chooses 3 time slots for transmission.

of several time slots at the start of identification. Upon receiving the frame, each tag randomly selects a time slot to reply its ID to the reader. A time slot can be classified into three categories according to number of tags involved. Specifically, a time slot can be an empty slot when there is no tag responding. If only one tag responds, this slot can be termed as a single slot, from which the reader can retrieve the ID successfully. If more than one tag sends in the same slot, collision occurs and the reader cannot identify any tag involved in the collision. Such a slot is termed collided slot. Whenever collision happens, the reader will send a new frame and the identification process is repeated until all tags are successfully identified.

# C. RATS overview

RATS is a RFID-based airport baggage tracking system. Fig. 2 shows a brief illustration of a working section in RATS. The major function of RATS is to reliably track customer baggage and ensure that baggage are correctly conveyed to their associated flights, considering that baggage loss and misplacement in the airport cause great financial loss to both the airports and the airline companies. For each flight we identify all its corresponding baggage before they leave the airport building for the airplane. We store a 96-bit Electronic Product Code (EPC) in each RFID tag, which is attached to a piece of baggage. For simplicity, we denote the EPC as tag ID in the rest of this paper. A reader is used to identify the tags (baggage) and check whether the baggage is conveyed to the correct flight. Note that RATS is a closed loop RFID system and each reader is connected to a backend server where all tags ID are stored. In the following of this paper, we denote

C as the set of tags RATS supports, so that $|C|$ becomes the system capacity. Note that $|C|$ can be significantly larger than the number of tags identified each time, which is only a subset of C. Identification efficiency is a major factor should be considered in RATS. In order to achieve this objective, we should effectively resolve tag collision and reduce the overall identification time. Driven by such a demand in our ongoing project, we aim to design an efficient and reliable tag identification protocol in large-scale RFID systems.

# IV. TAG IDENTIFICATION

To design an efficient identification protocol with Walsh codes, several issues must be addressed:

• How to map tag IDs to Walsh codes.   
- How to choose time slots for transmission once Walsh codes are obtained.   
- How to rebuild IDs from Walsh codes at the reader side.   
- How to resolve false positive identification to achieve reliability.

From subsection IV-A to IV-E we address each of the issues. Based on these steps, we further propose the identification protocol Wonder in IV-F.

# A. Mapping ID to Walsh codes

Intuitively, we can encode tag IDs with Walsh codes because of their anti-collision property. One key question is how to choose the appropriate length for Walsh codes. We consider this issue from two aspects. First, the number of collision-free tags we can encode increases with the number of Walsh codes we use. Since the number of Walsh codes with length $2^{l}$ is precisely $2^{l}$ , we can alternatively say that the number of collision-free tags we can encode increases with code length. In addition, multiple codes can be utilized to encode one tag ID. For instance, if we use 2 Walsh codes with length 4 to encode a tag ID, the number of tags we can encode should be $4^{2}=16$ . Given this, we have the following inequality to achieve the system capacity $|C|$

$$
(2 ^ {l}) ^ {b} \geq | \mathbf {C} | \tag {1}
$$

where b is the number of codes to encode a tag ID and $2^{l}$ is the code length. Thus, we can derive b

$$
b = \lceil \frac {l n | \mathbf {C} |}{l l n 2} \rceil \tag {2}
$$

Second, we should try to be compatible with the EPC C1G2 standard. In specific, tag IDs are normally 96 or 128 bits in the EPC C1G2 standard. If tags encode their IDs using Walsh codes, the length of information bits, i.e., Walsh codes, should also desirably be 96 or 128. Since the length of Walsh code should be integer power of 2, we set the length of Walsh code 128, or $2^{l}=128$ . In this paper, the system capacity is considered to be $2^{28}$ , which is fairly enough for practical use in large RFID systems. Thus, we can derive b=4 from Eq. 2. Consequently, we encode a tag ID using 4 Walsh codes. Each tag should transmit 4 Walsh codes sequentially instead of its ID as in traditional approaches.

Further, we introduce the encoding method, namely how to build a one-to-one mapping from a tag ID to 4 Walsh codes. Specifically, we enumerate all instances in the representation domain of 4 Walsh codes as shown in Fig. 3. Then for each tag, we randomly select one instance in the representation domain, write the 4 Walsh codes in the tag's memory and remove it from the domain. This mapping process is repeated until all the tags are encoded. When the identification starts, each tag reads the Walsh codes from its memory and transmits them one after another (which we will introduce later). According to the mapping rule, we can safely establish that for an arbitrary tag, each of its 4 corresponding Walsh codes can be viewed as uniformly distributed in the 128 Walsh codes since each instance is drawn randomly out of the domain.

# B. Choosing time slots

Our design is based on the framed slotted model, in which the time slots are synchronized by the reader. There are totally 4 identification rounds, and in each round a tag transmit one Walsh code in its encoding. In specific, in the i-th identification round, the reader broadcasts a frame consisting of f time slots. Each tag finds the i-th Walsh code w in its encoding and randomly selects k out of f slots to transmit w. Fig. 4 illustrates this scenario. The slots are selected using the tag ID and k independent hash functions $\{h_{1}, h_{2}, ..., h_{k}\}$ , and each hash function has an output uniformly distributed in the set $\{1, 2, 3, ..., f\}$ . In other words, w is transmitted in k time slots $h_{1}(ID), h_{2}(ID), ..., h_{k}(ID)$ simultaneously. If multiple hash functions choose the same time slot, only one of them counts. Therefore, each time slot in the frame has the same probability to hold the transmission.

# C. Rebuilding tag ID

We denote the tag set in the reading range as N, with cardinality $n = |\mathcal{N}|$ . As discussed previously, each tag transmits 4 Walsh codes and each of them is transmitted in k slots in a separate frame. Due to the collision resistant property, the reader can retrieve all Walsh codes in the frame by signal correlation. We can describe a retrieved Walsh code using 3 parameters, namely the tag it belongs to, the frame number and the slot number. Specifically, a Walsh code w can be written as $w(t, i, j)$ where t, i and j denote the tag index, frame number and the received slot number respectively. For example, $w(t_{1}, 2, 3)$ means that Walsh code w is generated by tag 1 and is received in slot 3 in the second frame.

If the reader can find 4 Walsh codes sent by the same tag, it can rebuild the tag ID by inverse mapping, as shown in Fig. 5. However, in practice the reader cannot actually tell from which tag a Walsh code comes, i.e. t in $w(t,i,j)$ is unknown. Even worse, the reader might group four Walsh codes that are not generated by the same tag, as shown in Fig. 6 where 4 mistakenly grouped Walsh codes are highlighted.

![](images/4bfe8c4ffd61989a8fe7b6846fca74a7047260d8d5d8225f324179475e896964.jpg)



Fig. 5. Received Walsh codes at the sender side with tag index.

Algorithm 1: Tag Identification algorithm   
Input : Tag set in database M;
Received Walsh codes in 4 frames {w(i,j)};
Output: The candidate identified tag set N $^{*}$ ;
1 N $^{*}$ = 0
2 for u ∈ [1,m] do
3    Derive 4 Walsh codes w $_{d}$ (u,i′)(1 ≤ i′ ≤ 4);
4    flag = true;
5    for i′ ∈ [1,4] do
6    for j′ ∈ G(w $_{d}$ (u,i′)) do
7    if w(i′,j′) does not exist then
8    flag=false;
9    Break;
10    if flag == true then
11    N $^{*}$ = N $^{*}$ ∪ {ID(u)};
12 Return N $^{*}$ ;

Despite the problem above, we resort to the tag IDs stored in the backend server to rebuild tag IDs. Denote the set of tag IDs stored in the server database as $\mathcal{M}$ with cardinality $m = |\mathcal{M}|$ . For each ID in $\mathcal{M}$ , the reader adopts the same encoding as the tags do and derives 4 Walsh codes. Denote $w_{d}(u,i^{\prime})$ as the $i^{th}$ Walsh code generated from the $uth$ ID in $\mathcal{M}$ where $1\leq u\leq m$ . Also for $w_{d}(u,i^{\prime})$ , the reader can obtain several time slots $\mathcal{G}(w_{d}(u,i^{\prime}))$ using the previously introduced hash function set $\{h_i(1\leq i\leq k)\}$ . Then it runs Algorithm 1 on the received Walsh codes to examine whether the $uth$ ID, $ID(u)$ , indeed exists in the tags to be identified. If $ID(u)$ exists, we put it into a candidate tag set denoted as $\mathcal{N}^*$ .

Algorithm 1 works as follows. For a tag in M, if the mapped 4 Walsh codes are properly received in the corresponding expected frames and slots (the tag and reader share the same hash function set), the tag is considered to exist in N. The algorithm screens out the impossible tags in M and returns the candidate tag set $N^{*}$ . It is obvious that any tag in N should be identified into $N^{*}$ .

![](images/13aec4fe24e7c353fc39fe6f88fe992bd77acd61d0c4ee125cb0e1283f70d6ff.jpg)



Fig. 6. Received Walsh codes at the sender side without tag index.

However, it is possible that some tags that do not exist in N whereas still falls into $N^{*}$ . We denote such situation as false positive. To illustrate how false positive happens, we introduce two concepts: slot conflict and frame conflict. If two tags transmit the same Walsh code in the same slot, we say they encounter a slot conflict. Further, we define that a tag experiences frame conflict if its has slot conflicts in all k transmission slots in a frame. Note that it is impossible to exactly tell whether a tag in M belongs to N if it meets frame conflict in all 4 frames, since each slot it transmits happens to accommodate a same Walsh code. This is the reason why false positive occurs. False positive results in identification of non-existing tag so that $|\mathcal{N}^{*}| \geq |\mathcal{N}|$ . For an illustrative example of false positive, please refer to subsection IV-E. In the following subsection, we give the probability analysis of false positive rate.

# D. False positive rate analysis

For presentation convenience, we summarize the notations in Table II. According to the discussions in subsection IV-A and IV-B, we can calculate $p_{c}$ as follows:

$$
p _ {c} = (1 - (1 - \frac {1}{a} (1 - (1 - \frac {1}{f}) ^ {k})) ^ {n}) ^ {k} \tag {3}
$$

Since the 4 Walsh codes are generated independently with each other, so we can calculate $p_{fp}$ as follows

$$
\begin{array}{l} p _ {f p} = \prod_ {i = 1} ^ {b} p _ {c} \\ = (1 - (1 - \frac {1}{a} (1 - (1 - \frac {1}{f}) ^ {k})) ^ {n}) ^ {k b} \tag {4} \\ \end{array}
$$

From Taylor expansion, we have

$$
\begin{array}{l} 1 - (1 - \frac {1}{f}) ^ {k} = 1 - (1 - e ^ {- k / f}) \\ = \frac {k}{f} + \frac {1}{2 !} \frac {k ^ {2}}{f} - \frac {1}{3 !} \frac {k ^ {3}}{f} + \dots \tag {5} \\ \end{array}
$$

Since $k \ll f$ , we only take the first term and derive

$$
\begin{array}{l} p _ {f p} = (1 - (1 - \frac {1}{a} (1 - (1 - \frac {1}{f}) ^ {k})) ^ {n}) ^ {k b} \\ \approx \quad (1 - (1 - \frac {k}{a f}) ^ {n}) ^ {k b} \tag {6} \\ \end{array}
$$

TABLE II. NOTATION OF PARAMETERS 

<table><tr><td>Parameters</td><td>Definitions</td></tr><tr><td> $p_c$ </td><td>The probability of frame conflict in one frame</td></tr><tr><td> $p_{fp}(f,n)$ </td><td>The false positive probability  $p_{fp}$ </td></tr><tr><td>a</td><td>The number of Walsh codes with length 128</td></tr><tr><td>b</td><td>The number of Walsh codes used to encode one tag ID</td></tr><tr><td>n</td><td>The number of tags to be identified n = |N| &lt; |M| = m</td></tr><tr><td>f</td><td>The frame size</td></tr><tr><td>k</td><td>The number of hash functions</td></tr></table>

Finally we obtain the approximation

$$
p _ {f p} \approx (1 - e ^ {- n k / a f}) ^ {k b} \tag {7}
$$

We first decide the optimal number of hash functions $k$ given $n$ and $f$ . We take the derivative of $p_{fp}$ with respect to $k$ in Eq. 7 and derive the optimal $k$ value $k_{opt}$

$$
k _ {o p t} = \frac {a f}{n} \ln 2 \tag {8}
$$

Plugging in Eq. 8 to Eq. 7, we can obtain the frame length $f$

$$
f = - \frac {n \ln p _ {f p}}{a b (\ln 2) ^ {2}} \tag {9}
$$

We get two key observations from the Eq. 9. First, the frame size f is linear with respect to the number of tags n, given the false positive rate. Second, f is monotonically increasing with the false positive rate $p_{fp}$ . Hence, we should increase the frame size if we want to achieve smaller false positive rate.

# E. Identification reliability

In the previous subsection, we present the discussion based on the false positive rate $p_{fp}$ . However, the baggage identification system requires high reliability, since the loss of customers baggage leads to bad consequences. Therefore, we should guarantee the reliability despite false positive situations. Here we propose an efficient false positive detection method that compensates for possible errors.

Fig. 7 presents an illustrative false positive example. Each row in Fig. 7 represents 4 Walsh codes mapped from a tag ID in candidate set $\mathcal{N}^*$ . The tuples marked on each Walsh code stands for (Walsh code, slots) pair. Tag5 is suspected to be false positive, since each (Walsh code, slots) pair is duplicated by other tags. For instance, pairs $(2,\{3,9,24\})$ , $(5,\{20,7,43\})$ , $(8,\{34,13,4\})$ , $(6,\{16,11,17\})$ are duplicated by tag1, tag2, tag3 and tag4 respectively. Algorithm 2 gives the false positive detection algorithm. It sequentially checks if each tag ID in $\mathcal{N}^*$ is false positive or not. Note that tag IDs in $\mathcal{FP}$ returned by Algorithm 2 are only suspected to be false positive but not confirmed, because

Algorithm 2: False positive detection algorithm   
Input : Candidate identified tag set N*;
Output: The suspected false positive tag set FP;
1 FP = 0
2 for each tag t in N* do
3 if t has frame conflict in all 4 frames then
4    FP = FP ∪{ID(t)};
5 Return FP;

Algorithm 3: Wonder reader operation   
1 Obtain the estimated number of tags $\hat{n}$ ;
2 Calculate the frame size $f$ based on $\hat{n}$ and the expected
3 false positive rate;
4 for $i \in [1,4]$ do
5    Broadcast the $ith$ frame with size $f$ and serial
    number $i$ ;
6    Receive the information in each slot;
7    Run correlation in each slot and retrieve Walsh
    codes;
8 Run algorithm 1 to generate candidate tag set $\mathcal{N}^*$ ;
9 Run algorithm 2 to generate suspected false positive
    tag set $\mathcal{F}\mathcal{P}$ ;
10 for $ID \in \mathcal{F}\mathcal{P}$ do
11    Broadcast $ID$ to query;
12    if no ACK received then
13 $\mathcal{N}^* = \mathcal{N}^* - \{ID\}$ ;

there can be tags having such ID after all. Algorithm 2 only needs at most two passes through $N^{*}$ . Hence the detection algorithm has a runtime complexity of $O(n^{*})$ , which turns out to be time efficient.

For each suspected false positive ID, the reader must verify whether it is indeed false positive. To fulfill this, it will broadcast the ID to all the tags to query if any tag has such an ID. The tag having such ID will acknowledge the reader while others remain silent. As a result, the reader will consider the suspected false positive ID as an existing one if it receives an ACK.

# F. Protocol description

The tag identification process of Wonder consists of four phases, namely cardinality estimation phase, advertisement phase, responding phase, and acknowledgement phase. To determine the proper frame size f, the reader needs to estimate the number of tags $\hat{n}$ quickly using method in [17]. In each round of the advertisement phase, the reader broadcasts a message containing a frame size f and a serial number s. The frame size f is calculated based on $\hat{n}$ and the expected false positive rate. The serial number s is required because tags should know which among the 4 Walsh codes to transmit upon receiving the advertisement. When the tag is about to respond, it uses the predefined k hash functions to obtain the transmission slots, and then transmits the Walsh codes. The reader conducts correlation to retrieve Walsh codes in each slot. After 4 frames, the reader manages to gather all the transmitted Walsh codes and received slot numbers. It runs Algorithm 1 and Algorithm 2 afterwards, and finally comes to the acknowledgement phase. Algorithm 3 and Algorithm 4 describe Wonder for both the reader and tag operation, respectively.

![](images/4487bba07b5278845c5a843d708c4f917f04280e4bf86ae7391c99ad13d22466.jpg)



Fig. 7. Illustrative example of false positive situation.

Algorithm 4: Wonder tag operation   
1 for $i \in [1,4]$ do
2 Receive the ith frame;
3 Use hash function set to choose transmission slots;
4 Transmit the ith mapped Walsh code;
5 if receive queryID then
6 if queryID equals to own ID then
7 Transmit ACK;

# V. PERFORMANCE EVALUATION

In this section, we conduct simulation to evaluate our protocol Wonder. We compare the efficiency of our protocol with two baseline tag identification protocols. The three protocols for comparison are Enhanced Dynamic Framed Slotted Aloha (EDFSA), Adaptive Binary Splitting(ABS) and slotted-CDMA. The former two are pure TDMA-based. EDFSA is one of the most effective aloha based identification protocol and ABS is a typical efficient tree based identification protocol. By slotted-CDMA we mean this is also a slotted protocol, while in each slot tags are assigned different spreading codes. Collision can still happen if two tags are assigned the same spreading codes as well as transmitting in the same slot. The comparison metrics are as follows.

- Identification time: It is defined as the total amount of time spent to identify all tags.   
- Identification delay: We both measure the per tag delay as well as average delay among all tags. Per tag delay is defined as the time spent for each tag to be identified. Average delay is the mean of per tag delay.

We vary the number of tags to compare the metrics above. By default, we set the false positive rate to $10^{-4}$ , and we also vary the false positive rate in subsection

![](images/83194370067b3b3f5626b955593189e8682d069c8144345fda193ca6ef60b07c.jpg)



(a) Compare with TDMA

![](images/fc69793fd65c6c07efe24471eded141bed17acbd5f36729ee07eed2a89c11888.jpg)



(b) Compare with slotted-CDMA   
Fig. 8. Identification time comparison with TDMA-based approaches and slotted-CDMA.

V-D. Note that in all the figures, Wonder-X represents the protocol with false positive rate $10^{-X}$

# A. Simulation setup

We adopt the Philips I-Code specification [18] and the EPC C1G2 standard as basic simulation settings. Namely, each tag ID is 96 bits long and the tag bit rate is $53Kb / s$ . Also each tag should wait for a period of $302\mu s$ before transmitting its information, either ID or Walsh code. Therefore, the slot time for ID transmission is $\tau_{id} = 2113\mu s$ . Similarly, as the Walsh code is 128 bits long, the slot time for Walsh code transmission is $\tau_{wc} = 2717\mu s$ . The reader has a different transmission bit rate of $26.5Kb / s$ . As the advertisement message sent by the reader is very short, its corresponding time is ignored. So we only consider the waiting time $302\mu s$ in terms of reader transmission.

# B. Identification time

We fix the false positive rate to $10^{-4}$ . We separately compare Wonder with TDMA-based and CDMA-based approaches. Fig. 8(a) shows the TDMA-based approach comparison, when the number of tags ranges from 500 to 5000. For each number of tags, we run the simulation 100 times and take the average result. The simulation shows that ABS and EDFSA perform similarly while Wonder significantly reduces the identification time. Wonder achieves 6.3% of the overall identification time of ABS and 6.6% of EDFSA, because it fully takes advantage of the collision resistant property of Walsh codes. Also notice the identification time of Wonder grows linearly as the number of tags increases, which is consistent with the theoretical analysis.

Fig. 8(b) presents the CDMA approach comparison. It can be seen that slotted-CDMA outperforms Wonder in terms of identification time. Nevertheless, Wonder does not lag too far behind. In terms of spectrum, Wonder is far economical than slotted-CDMA, since the high chipping frequency in CDMA results in large spectrum occupancy.

# C. Identification delay

In Fig. 9, we show the CDF of per tag delay with the number of tags fixed to 2500. As can be seen, per tag delay is uniformly distributed in ABS while it exhibits like stairs in EDFSA since EDFSA is a framed slotted protocol. Per tag delay in Wonder is concentrated around 1000ms, since tags are almost identified simultaneously after 4 consecutive frames. Even if false positive occurs, the confirmation phase will not take much time. In our protocol, no tag waits for a much longer time than others before identified, which is denoted as "tag starvation problem". Fig. 10 presents the average delay of the protocols. We see that Wonder has much less average delay than ABS and EDFSA.

![](images/8b7e9d33bb1735aa0290f1c18d04937528d5668272da4d369aa5d4a4b2a29f33.jpg)



Fig. 9. Per tag delay CDF.

![](images/3533d4361732e224b2f4e2b783e918224036b8c162fae894e7f92968e122d173.jpg)



Fig. 10. Average delay.

![](images/554584cc2843b7ab2293cf2c6d0b3759645f0b7e94ef83bce0a644bdcf302ace.jpg)



Fig. 11. Identification time with varied positive rate.

# D. Varying false positive rate

In the theoretical analysis, we show that the frame size is related to a desired false positive rate. In this subsection, we vary the false positive rate to evaluate identification time (other metrics should exhibit similar results). Fig. 11 shows that the identification time of Wonder increases as the desired false positive rate decreases. Nevertheless, even if the false positive rate is as small as $10^{-6}$ , the performance of Wonder is still much better than ABS and EDFSA. This is because the frame size is proportional to $\ln(p_{fp})$ where $p_{fp}$ is the false positive rate. Thus the frame size will not increase dramatically even if $p_{fp}$ becomes several magnitudes smaller.

# VI. CONCLUSION

Motivated by our ongoing airport baggage tracking project, we propose an efficient and reliable anticollision tag identification protocol Wonder in large-scale RFID systems. The protocol is based on the orthogonal Walsh code. Both the theoretical analysis and experiment results show that our protocol significantly reduces the overall identification time and therefore improves the throughput compared with traditional methods.

# VII. ACKNOWLEDGEMENT

This study is supported in part by the NSFC Distinguished Young Scholars Program under Grant No. 61125202, and the NSFC under Grant No. 61103187.

# REFERENCES

[1] L. Ni, Y. Liu, Y. Lau, and A. Patil, “Landmarc: Indoor location sensing using active rfid,” in Proc. of Percom, 2003.   
[2] K. Finkenzeller et al., RFID handbook: Fundamentals and applications in contactless smart cards, radio frequency identification and near-field communication. Wiley, 2010.   
[3] S. Lee, S. Joo, and C. Lee, “An enhanced dynamic framed slotted aloha algorithm for rfid tag identification,” in Proc. of Mobiquitous, 2005.   
[4] J. R. Cha and J. H. Kim, “Dynamic framed slotted aloha algorithms using fast tag estimation method for rfid system,” in Proc. of CCNC, 2006.   
[5] H. Vogt, “Efficient object identification with passive rfid tags,” in Proc. of Pervasive, 2002.   
[6] J. Myung and W. Lee, “Adaptive splitting protocols for rfid tag collision arbitration,” in Proc. of MobiHoc, 2006.   
[7] N. Bhandari, A. Sahoo, and S. Iyer, “Intelligent query tree (iqt) protocol to improve rfid tag read efficiency,” in Proc. of ICIT, 2006.   
[8] C. Mutti and C. Floerkemeier, “Cdma-based rfid systems in dense scenarios: Concepts and challenges,” in Proc. of RFID, 2008.   
[9] EPC Radio-frequency Identity Protocols Class-1 Generation-2 UHF RFID Protocol for Communications at 860MHz-960MHz, EPCglobal Std.   
[10] S. Weis, S. Sarma, R. Rivest, and D. Engels, “Security and privacy aspects of low-cost radio frequency identification systems,” in Proc. of First International Conference on Security in Pervasive Computing, 2003.   
[11] C. Law, K. Lee, and K. Siu, “Efficient memoryless protocol for tag identification,” in Proc. of DIAL-M, 2000.   
[12] S. Katti, S. Gollakota, and D. Katabi, “Embracing wireless interference: Analog network coding,” in Proc. of ACM Sigcomm, 2008.   
[13] M. Zhang, T. Li, S. Chen, and B. Li, “Using analog network coding to improve the rfid reading throughput,” in Proc. of ICDCS, 2010.   
[14] H. Yue, C. Zhang, M. Pan, Y. Fang, and S. Chen, “A time-efficient information collection protocol for large-scale rfid systems,” in Proc. of Infocom, 2012.   
[15] L. Kong, L. He, Y. Gu, M. Wu, and T. He, “A parallel identification protocol for rfid systems,” in Proc. of Infocom, 2014.   
[16] N. Ahmed, T. Natarajan, and K. Rao, “Discrete cosine transform,” IEEE Transactions on Computers, pp. 90–93, 1974.   
[17] C. Qian, H. Ngan, Y. Liu, and L. Ni, “Cardinality estimation for large-scale rfid systems,” IEEE Transactions on Parallel and Distributed Systems, vol. 22, pp. 1441–1454, 2011.   
[18] Philips, "I-code uid smart label ic functional specification."