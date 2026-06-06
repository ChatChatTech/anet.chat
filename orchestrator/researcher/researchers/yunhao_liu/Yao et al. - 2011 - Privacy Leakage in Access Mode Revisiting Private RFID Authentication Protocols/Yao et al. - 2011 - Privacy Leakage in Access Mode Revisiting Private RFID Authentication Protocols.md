# Privacy Leakage in Access Mode: Revisiting Private RFID Authentication Protocols

Qingsong Yao†‡, Jinsong Han†‡, Yong Qi†, Lei Yang†‡, Yunhao Liu‡\*

†School of Electronic and Information Engineering, Xi’an Jiaotong University, China

‡Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong, China

\*TNLIST, School of Software, Tsinghua University, China

qsyao@yahoo.cn, {jasonhan, liu}@cse.ust.hk, qiy@mail.xjtu.edu.cn, matrixmaker@gmail.com

Abstract—Existing RFID Privacy-Preserving Authentication (PPA) solutions mainly focus on the design of crypto based interactive protocols between readers and tags. Although the cryptographic mechanisms enable randomization and enhance protocol-level privacy, the access mode in RFID systems is less random and may leak private information. We introduce a new attack based on such privacy leakage in access mode, where we show that the mainstream RFID PPA protocols, including the linear, tree-based, and synchronization-based solutions, are not private. We also show that this new attack is easy to conduct, e.g., we can track tags that employ typical tree-based PPA protocols without the need of compromising tags. We discuss the applicability of the attack. Moreover, we provide useful recommendations to strengthen existing PPA protocols in defending against such attacks. The simulation results demonstrate the practicability and effectiveness of this attack.

Keywords-access mode; RFID; privacy leakage; proven private; authentication protocol

# I. INTRODUCTION

Radio Frequency IDentification (RFID) enables remote identification of objects. As a promising technology, RFID facilitates identification, localization, and monitoring in many applications [1]. Due to the even less resources than sensor-based applications [2, 3], RFID systems face increasingly emerging concerns on privacy leakage [4]. Without protection, the private information related to a tag, such as an item’s ID or user’s location can be exposed to attackers. To solve this issue, many crypto based protocols have been proposed in the literature [5, 6]. Those solutions, termed as privacy-preserving authentication (PPA) protocols, allow legitimate readers to privately authenticate legitimate tags. Mainstream PPA approaches usually fall into three categories, linear [7-9], tree-based [10, 11], and synchronization-based protocols [12, 13].

Since seldom works are presented on multiple tags [14] and multiple readers [15] applications, we study in this work the one tag one reader case. Generally, a RFID system is composed of tags, readers and backend server which keeps a database of all the tags’ information. The communication between the backend server and readers is generally considered secure, employing high speed local Ethernet. On the other hand, the communication between tags and readers is insecure. Considering both reader and tag cannot be sure of the legitimacy of the other side before authentication, the reader and tag have to authenticate each other mutually. The mutual authentication process can be abstracted into a threeway protocol, as illustrated in Fig. 1.

In this paper, we define the combination of the backend server and RFID readers as ‘the reader’. At the very beginning, each tag shares a unique key with the reader. During a process of authentication, the reader sends out a challenge to the tag and the tag responds with an AuthTag message which authenticates itself to the reader. Upon the response, the reader searches in the database to find a matched key which can generate a same AuthTag, while the key should be the one shared with the authenticating tag. A tag will be considered as legitimate if such a match is found. Then the reader emits an AuthReader message to authenticate itself to the tag. Typically, PPA protocols employ lightweight crypto based mechanisms, for example, hash functions [16]. The principle behind the crypto based PPA protocols is to randomize tags’ responses in order to confuse attackers and protect the privacy for tags. So that attackers cannot link the encrypted responses to the corresponding tags.

To specify the privacy strength of different protocols, many efforts have been made in defining privacy models [17-20]. They are based on the assumptions on different levels of adversary’s abilities in distinguishing tags. Many PPA protocols have been proposed and some of them are proven private under the privacy models. Typically, the improved randomized hash-lock protocols can achieve weakprivacy as proved in [18], the Dimitriou’s tree-based protocol [11] can reduce the tracking probability to a negligible extend when the branching factor is sufficiently large [9], the protocol proposed by Ma et al. [13] is proven to be of strong unpredictability, which is a stronger notion than destructive-privacy defined in [19].

Unfortunately, all of these works only focus on the computation process or results during authentication. The privacy flaws incurred by distinguishable access modes have not been deeply studied before. Thus, although PPA protocols can effectively enhance privacy protection in computation, RFID privacy may still be jeopardized in other aspects. Despite the responses, we find that the access mode, which determines the majority of the processing time for each authentication, also has distinguishable information. Since a reader cannot directly identify a tag if the response is encrypted, the reader has to perform a search to locate the keys corresponding to the tag before authentication. For different tags, the time needed for localization is not equal due to the searching method and storage organization in the backend system. For example, in a typical hash-lock [7] based approach, a reader conducts linear search in its database to find a proper key that can generate the hash value in the response from a tag. Suppose that a tag $T _ { \mathrm { i } } ^ { \ast } \mathrm { { s } }$ key is stored at the position some records before the position where another tag $\bar { T _ { j } } \mathrm { \bar { s } }$ key is stored the in the database. During the authentication procedure, $T _ { j }$ needs more time than $\bar { T } _ { i }$ to processing the records between the two tags’ keys. To gather such distinguishable information, an attacker can either collect data directly from regular authentication process or act as a relay between the reader and tag. Both methods are passive and hence are hard to detect.

![](images/52ed197d26e973f970db47cfd91008fe659e2db53ff16bf56f93358c503b8a46.jpg)



Figure 1. Abstract mutual authentication protocol

A sophistic attacker can make use of this distinguishable information to identify or track a tag. Unfortunately, current designs of RFID PPA protocols seldom take this problem into consideration. Some previous works have been made to resist timing analysis, e.g. [13, 20]. But the first work only focuses on synchronization-based protocols. The second work analyzes linear search protocols, synchronization-based approaches and so-called undesynchronizable protocols, leaving out the tree-based protocols. Moreover, these two works consider computation cost only and do not take the access time into account. Indeed, the computation time is dominated by the access time, as we will illustrate in the experiments in Section VI. To our best knowledge, there is no systematical analysis on the privacy flaws incurred by distinguishable access modes has been made before. As a result, attackers can still compromise the privacy of RFID systems without the need of knowing keys shared by legitimate readers and tags.

In this paper, we propose a new attack pattern that leverages the distinguishable access mode of tags to break the privacy of RFID systems. The attack is lightweight and only makes use of differentiated features of tags, such as the access time duration and tag internal states, to identify or track tags. Unlike privacy-jeopardizing attacks proposed in previous works [5], there is no need to capture tags or crack crypto-based mechanisms when performing this attack. In addition, the newly designed attack is more general and can be launched to all types of PPA protocols. We systematically analyze representative PPA protocols from three mainstream categories and show their vulnerability under this attack. We analyze the applicability of this attack, and then demonstrate its practicability via experiments. The results show that the attack is effective and existing PPA protocols used to be proven-private may not be private any more. Furthermore, we present our recommendations to mitigate the impact from the proposed attack.

The rest of paper is organized as follows. In Section II, we introduce the adversary’s abilities, privacy notions, and related works of PPA protocols. In Section III, we present our attack and utilize it to attack three typical proven private protocols. In Section IV, we discuss the applicability of our attack. In Section V, we propose a set of useful recommendations. In Section VI, we conduct experiments and show the evaluation results. At last, we conclude the paper.

![](images/dbfdd52a0ae95f48ff17efe6a139fe524f258d5738188e1bbbb02e6bf01e2966.jpg)



Figure 2. The privacy model of Vaudenay

# II. RELATED WORKS

In this section, we introduce the privacy notions of PPA protocols. We also overview related works. In particular, we discuss three representative RFID PPA protocols in detail.

# A. Adversary’s Power and Privacy Notions

To specify the privacy issue and analyze privacy strength for different protocols, many efforts have been made in privacy notions and models [17-20]. They differ in assumptions on adversary’s abilities of distinguishing tags.

Avoine [17] formalizes an adversarial model and define the notions of existential untraceability and universal untraceability using an oracle model. Existential untraceability requires that no interaction sequence exists such that an adversary can successfully track a tag with nonnegligible possibility. Universal untraceability requires that not for all interaction sequences an adversary can track a tag with non-negligible possibility. Juels and Weis [18] propose a simpler but more flexible notion of strong privacy. They also propose a notion, the cross-reader privacy, which protects tags from multi-verifier with untraceability. In [19], Vaudenay details a model with variant privacy strengths. In such a model, an adversary can be strong, destructive, forward, weak, and narrow. The notions, strong, destructive, forward, and weak, indicate the reader’s ability to compromise tags. When a tag is compromised, all secret information, including its key stored in the tag, exposes. A weak adversary cannot compromise a tag. A forward adversary compromises a tag only at the end of attacking activities. A destructive adversary can destructively compromise a tag. A strong adversary can compromise a tag, after that the tag is put back in the system for circulation. A narrow adversary cannot get any result from a legitimate reader’s authenticating a tag, while a “wider” one can. A protocol is P private if the tracking probability of any adversary in class P is negligible. Obviously, the privacy strength follows a relation shown in Fig. 2, where the $\displaystyle \mathrm { \Omega } ^ { \mathrm { \tiny { c } } \mathrm { \tiny { c } } } = \mathrm { \stackrel { . } { > } } ^ { , }$ denotes the imply relation. In [20], the authors extend Vaudenay’s privacy model by allowing an adversary to obtain the reader’s computation time for searching a tag. All the above works focus on either the computation process or result during authentication. The privacy flaws incurred by distinguishable access modes have not been studied before. As a result, an adversary can still leverage the privacy leakage in the access mode of RFID systems to jeopardize privacy. For example, in [20] the authors suggest using a balanced binary search tree (BBST) to mitigate the difference in computation time. However, each node in BBST has a relatively stable accessing cost. The processing time of each tag related to the node also suffers from privacy leakage in the access model, as we will briefly illustrate in Section III.B.

Privacy notions are generally formalized by the adversary’s ability to distinguish tags. An adversary can leverage physical layer information to distinguish RFID tags [21, 22]. Zanetti et al. [21] present an intensive study on the physical-layer features of Ultra High Frequency (UHF) tags and utilize these features to break tag holder privacy. The proposed methods can gain high accuracy in classifying tags. However, it is only possible to uniquely identify a maximum of approx. $2 ^ { 6 }$ UHF RFID tags independently of the population size. In [22], Periaswamy et al. use the transmission time of EPC, PC and CRC to distinguish individual UHF passive tags. Cryptographic functionality enabled tags, which may not have to emit EPC, PC or CRC, may be indistinguishable.

# B. PPA Protocols

Depending on the different strategies of searching a tag in the backend database, mainstream PPA protocols can be categorized into three groups [5]: linear, tree-based, and synchronization-based approaches.

Most early designed PPA protocols are linear, e.g., hashlock based protocols [7, 18]. In [7], the authors provide a simple protocol, hash-lock, for RFID based access control. A tag uses the hash value of its secret key as a pseudonym. The pseudonym can be utilized as an identifier of this tag. Such an identifier is vulnerable to adversaries’ tracking. Randomized hash-lock protocols [7] emerge soon. They introduce random numbers when generating the hash values in the tags’ responses. The response from a tag in randomized hash-lock protocols contains no information from the reader or about the interaction session. Thus, the response can be recorded and replayed later to deceive legitimate readers.

An improved randomized hash-lock protocol [18] utilizes random numbers from both the reader and tag as inputs in hash operations to avoid replay attacks. As illustrated in Fig. 3, a reader sends out a query with a random number $R _ { 1 }$ to tag $T _ { i }$ . Upon the request, the tag generates a random number $R _ { 2 }$ and computes a hash value using its secret key and the two random numbers as inputs. The tag sends the hash value back to $R _ { 2 }$ as a response message for authentication. The reader then starts a searching process for locating the key of this tag. In the searching process, the reader exhaustively computes hash values for each key stored in the backend database until a matched key is found. Both the randomized and improved randomized hash-lock protocols can achieve weak-privacy as proved in [18].

The searching efficiency of typical linear protocols is O(N), where N is the number of tags in the RFID system. Modern RFID applications, however, have millions of tags in common. Therefore, they need more efficient solutions. Tree-based protocols are thereby designed to provide scalable efficiency. Molnar and Wagner [10] propose a protocol to organize the keys of tags in a virtual key tree. Each tag has several keys instead of one key. The keys of a tag are correlated to a path from the root of the key tree to the leaf node assigned to the tag, as illustrated in Fig. 4. In Fig. 4, $T _ { 3 }$ has the keys $( k _ { 1 , 0 } , k _ { 2 , 0 } , k _ { 3 , 0 } )$ . During authentication, the tag will generate multiple responses by using its keys. The reader verifies the tag via multi-rounds interactions, as a tree-based search. For the example in Fig. 4, at the second level of the key tree, the reader will check the response received from the tag by using keys $k _ { 2 , 0 }$ and $k _ { 2 , 0 }$ respectively for determining the next moving direction. If the tag is $T _ { 3 } ,$ the reader will go down to the node of $M _ { 2 }$ after the verification of this level succeeds. For a tree of depth $d ,$ above protocol needs d rounds of interactions to verify a tag. When all the keys of $T _ { i }$ are verified, the authentication process completes and the reader accepts $T _ { i }$ as legitimate.

![](images/2ea1b781ca4bd555296833371385b52100ade5e298535929597af3161ad8bc05.jpg)



Figure 3. The improved randomized hash-lock protocol

![](images/c51e6d78af9c658a3ba4405965afd64445d388f5015352c89055939aa6169a17.jpg)



Figure 4. Tree based architecture   
![](images/9697a8cb73990e2805e0bd520f890ce1b071589e675202add6120bee8cc8df73.jpg)



Figure 5. Typical tree-based protocol

Dimitriou [11] proposes a protocol that requires a tag to generate a random number and involve the number into the hash operation. As shown in Fig. 5, tag $T _ { i }$ responds with ciphers $\{ F _ { k _ { j } ^ { i } } ( r ) \}$ , where the $k _ { j } ^ { i }$ is the key of $T _ { i }$ at the j-th level, the r is the concatenation of two random numbers, $N _ { T }$ and $N _ { R }$ which are generated by the tag and reader respectively, and $F _ { k } ( r )$ is a cryptographic hash function using k and r as inputs. Given d as the depth and δ as the branching factor, the efficiency of a balanced key tree is $O ( d { \times } \delta )$ . Such a key tree can accommodate $d ^ { \delta }$ tags. The treebased protocol can achieve ${ \cal O } ( \log _ { \delta } N )$ efficiency and hence is suitable for large scale RFID systems. Tree-based protocols, however, are vulnerable to compromising attacks if the branching factor of their key trees is small [9], even when dynamic key-updating is enabled [23]. When the branching factor is sufficiently large, the possibility of successfully tracking tags via compromising attacks is negligible [9].

Another type of protocols which can support efficient authentication is the synchronization-based approach. In particular, synchronization-based PPA approaches precompute possible outputs to accelerate the searching process and can improve the searching efficiency to O(1). For example, the OSK protocol [12] utilizes a pre-computed table. The size of such a table is $O ( m \times N )$ , where N is the number of the tags in the system and m is the number of precomputed possible results for each tags. An important property of OSK is that each tag is limited to reply no more than m times in its entire circulation life. When the reader receives a reply from $T _ { i }$ which remains in the range of the table, it can rapidly identify $T _ { i \cdot }$ Each time the tag is scanned, a pre-computed record is consumed. As a result, the finite table of pre-computed records can be gradually exhausted. When the tag is scanned more than m times by malicious readers, the tag cannot be authenticated any more.

To achieve better usability, Ma, Li, Deng, and Li (MLDL) [13] enables a tag which runs out of its precomputed records to be successfully authenticated. This protocol is illustrated in Fig. 6. If a legitimate tag $T _ { i }$ is interrogated with a challenge $c ,$ it computes I and $r _ { 1 }$ to comprise the response message, where I is computed as the output of a hash function with $T _ { i } { ^ \mathrm { 3 } \mathrm { s } }$ counter ctr and key k as inputs, $r _ { 1 }$ is a XOR (exclusive OR) result of padded ctr and the hash value with the $c , I ,$ and k as inputs. The tag then emits the response message and increases its counter ctr by 1 (consuming one reply quote). The message I in the response can help legitimate readers to identify the tag rapidly. That is because the reader has pre-computed and stored a tuple (I, k, ctr, ID) for each tag. If the reader accepts a tag as a legitimate one, it updates the related counter and tuple of this tag to keep in coordination with the tag. If a legitimate tag has not been maliciously scanned since the last successful authentication, the counter ctr held by the tag should equal the corresponding counter $_ { c t r } \mathrm { * }$ stored by the reader. Once a tag is interrogated by a malicious reader, the counters ctr in this tag will be updated to $c t r { + } 1$ , while the one stored in the reader keeps unchanged. Thus, if attackers keep interrogating the tag, all the tag’s pre-computed records will be used up and the tag becomes desynchronized with the reader. In this case, the reader has to authenticate the tag by exhaustively checking (usually by conducting a linear search) all its records if there exists a tuple $( \boldsymbol { I } ^ { \prime } , \boldsymbol { k } , c t \boldsymbol { r } ^ { \prime } , \boldsymbol { I } \boldsymbol { D } )$ that can generate a same response message. In this way, a legitimate tag can be authenticated no matter whether it is synchronized with the reader or not. This protocol is proven to be strong unpredictable, which is a stronger notion than destructive-private in Vaudenay’s model [19].

$R \rightarrow T_i:$ c; $T_i:$ $I = F_k(\text{ctr} \| pad_1);$ $r_1 = F_k(c \| I) \oplus (\text{ctr} \| pad_2);$ $\text{ctr} = \text{ctr} + 1;$ $T_i \rightarrow R:$ $r = r_1 \| I;$ R: if find the tuple $(I, k, \text{ctr}', ID)$ ;
if $\text{ctr}' \| pad_2 = F_k(c \| I) \oplus r_1$ $\text{ctr}' = \text{ctr}' + 1$ and $I = F_k(\text{ctr}' \| pad_1);$ accept the tag;
else reject;
else if exit $(I', k, \text{ctr}', ID)$ that $\text{ctr}' \| pad_2 = F_k(c \| I) \oplus r_1$ and $F_k(\text{ctr}' \| pad_1) = I$ $\text{ctr}' = \text{ctr}' + 1$ and $I = F_k(\text{ctr}' \| pad_1);$ accept the tag;
else reject the tag;   
Figure 6. The MLDL protocol

# III. THE AMA ATTACK

In this section, we present our attack to the three aforementioned typical protocols.

# A. Obseravations and Basic Idea

We observe that the access mode of tags in RFID systems lacks randomization processes. Some characteristics of tags’ access mode, such as the internal state and the search process of tags, affect their processing time and lead to distinguishable features, which cannot be concealed by using crypto-based mechanisms. Tags’ privacy may leak if an adversary utilizes these characters. We aim to design an attack pattern, Access Mode based Attack (AMA), to leverage those characters. We discuss the issue in three typical types of PPA protocols, respectively.

For linear protocols, the searching process of a tag is in a sequential access mode. Because a reader does not know the identity of a tag before authentication, the reader has to sequentially access its records and check if there is a proper one matching the tag’s response. The accessing and checking of a record consume time. Thus, the tags whose records are stored with different positions in the database show differences in terms of processing time. AMA can make use of these differences to distinguish or track a tag.

In tree-based protocols, the searching process for locating the leaf node of a tag comprises of a serial of comparisons along the path from the root of key tree to the leaf node related to the tag. At each level of the tree, the comparison operations that happen at a virtual middle node are also in a sequence for all branches of this node. Therefore, the accumulated processing time of a tag’s authentication is different from those of other tags, similar to the situation of linear protocols. With the observations on processing time, AMA can still identify a tag.

The synchronization-based approaches are a little more complicated. There are two kinds of tags if using synchronization-based approaches. Tags in the first type are the ones whose pre-computed records have not been exhausted. Those tags belonging to the first type can be identified with O(1) searching efficiency by utilizing precomputed table. The access mode of them is indistinguishable due to the similar processing time. The tags in the second are the ones whose pre-computed records are used up. For those tags, the synchronization-based approaches cannot utilize the pre-computed table, but employ another PPA schemes, very likely the linear based approaches, for authentication. Thus, a sophistic attacker can first keep maliciously interrogating the tag until the tag enters desynchronized state, and then perform the AMA attack. Meanwhile, the shift of a tag from synchronized state to desynchronized state will generate distinguishable differences from other tags to facilitate the attack.

![](images/1d1cf0e0900145d3ce3d9434f9d3a0436813c3164364e70f8d56155cbb5c113e.jpg)



Figure 7. Linear searching in sequential access mode

Based on above discussions, we believe AMA is a general threat to all PPA protocols. This attack is simple to perform by just measuring the processing time of a reader after the reader receives a tag’s authentication message.

# B. General AMA to PPAs

In this sub-section, we elaborate the general design of AMA to three typical PPA protocols. In particular, we also show the flaws of these protocols under AMA which are commonly considered as private.

To simplify the analysis, we suppose that the backend database is stored in random-access memory (RAM) and does not use caches (we will discuss the cases of using cache in the next sub-section). We also suppose the access time for a single record in the RAM database is $t _ { a }$ and the computation time for this record is $t _ { c } .$ . With the above hypothesis, we can simplify the analysis by focusing on the access time and computation time. We ignore the errors in adversaries’ measurement results.

# 1) AMA on the improved randomized hash-lock protocol

In the improved randomized hash-lock protocol, searching a tag’s record follows a sequential access mode, as illustrated in Fig. 7. Given two randomly chosen tags $T _ { 1 }$ and $T _ { 2 }$ . We assume that $T _ { 1 } { } ^ { , } \mathrm { s }$ record is stored with order $o _ { 1 }$ and $T _ { 2 } \mathrm { { ' } s }$ record is stored with order $o _ { 2 } .$ . Because the tag’s response varies at each time, the reader has to check from the first record in the database. After receiving the response from a legitimate tag, the access time and computation time for locating the tag’s record can be denoted as $x t _ { a }$ and $x t _ { c } ,$ respectively, where x is an integer. The integer x is indeed the offset of this record from the first record in the database. We use $t _ { s }$ to denote the cost for locating a single record, then

$$
t _ {s} = t _ {a} + t _ {c}.
$$

The difference in terms of time cost between $T _ { 1 }$ and $T _ { 2 } ,$ denoted as $D _ { 1 , 2 } ,$ is

$$
D _ {1, 2} = \left| \left(t _ {a} + t _ {c}\right) \times o _ {1} - \left(t _ {a} + t _ {c}\right) \times o _ {2} \right| = \left| o _ {1} - o _ {2} \right| \times t _ {s}.
$$

For the two tags $T _ { 1 }$ and $T _ { 2 } ,$ we have

$$
t _ {s} \leq D _ {1, 2} \leq (N - 1) \times t _ {s},
$$

where N is the number of tags in the system.

Since $T _ { 1 }$ and $T _ { 2 }$ are randomly chosen, their processing time should be independent with each other and follow a uniform distribution. Thus, the joint probability density function of $T _ { 1 }$ ’s time cost $t _ { 1 }$ and $T _ { 2 } \mathrm { { ' } s }$ time cost $t _ { 2 }$ is

$$
\begin{array}{l} f (t _ {1}, t _ {2}) = f (t _ {1}) \times f (t _ {2}) \\ = \left\{ \begin{array}{c} \frac {1}{((N - 1) t _ {s}) ^ {2}}, t _ {1}, t _ {2} \in [ t _ {s}, N t _ {s} ] \\ 0, e l s e \end{array} \right. \\ \end{array}
$$

The expected value of difference between two tags’ time costs is

$$
\begin{array}{l} E (D _ {1, 2}) = E \left| t _ {1} - t _ {2} \right| \\ = \int_ {t _ {s}} ^ {N t _ {s}} \int_ {t _ {s}} ^ {N t _ {s}} | x - y | f (x, y) d x d y \\ = \frac {(N - 1) t _ {s}}{3} \\ \end{array}
$$

Large-scale RFID systems are very common in current industry. Therefore, the difference is sufficiently distinguishable. Based on our prior experiences, the order of magnitude of $t _ { a }$ and $t _ { c }$ are ${ { 1 0 } ^ { - 6 } }$ seconds, the order of magnitude of N is $1 0 ^ { 6 }$ . Then the order of magnitude of the average difference is $1 0 ^ { 0 }$ seconds, which is easy to be observed by an adversary.

# 2) AMA on Dimitriou’s tree-based protocol

In tree-based protocols, the case is more complicated. We take Dimitriou’s protocol as an example for the analysis, while the attack is not limited to this protocol. All tree-based protocols, e.g. [24], in which a tag has a relatively stable access cost will suffer from this attack.

In Dimitriou’s tree-based protocol [11], the key searching at each level is to determine to which branch the reader will move. This process is also conducted as a sequential searching across all branches of current node. But for two tags, the absolute values of cost differences at each level may be either negative or positive. Thus, the overall difference cannot be straightforwardly deduced as the linear search protocols, which is not the case as claimed in [20].

Given the depth of the key tree is d and the branching factor is $\delta .$ Searching in a tree needs to process at least d records and at most $d { \times } \delta$ records, corresponding to the record on the leftmost leaf and the record on the rightmost leaf, respectively. Let $D _ { 1 , 2 }$ to denote the differences of their processing time for tags $T _ { 1 }$ and $T _ { 2 } ,$ then we have .

$$
d \times (t _ {a} + t _ {b}) \leq D _ {1, 2} \leq d \times \delta \times (t _ {a} + t _ {b}).
$$

The expected value of difference between two tags’ time cost is

$$
E (D _ {1, 2}) = \frac {d (\delta - 1) t _ {s}}{3}.
$$

The difference is directly proportional to the d and δ. If the δ is sufficiently large, the difference is observable. In existing works, the tracking possibility of tree-based protocol under compromising attacks descends as the branching factor of the key tree increases [9]. When the branching factor is also sufficiently large, the impact of compromising attack is negligible [9]. For a system with $2 ^ { 2 0 }$ tags, the tracking probability by compromising 20 tags declines from 95.5% to 3.9% as the branching factor increases from 2 to 1000. Under our attack, however, the order of magnitude of average difference between two tags is $1 0 ^ { - 3 }$ seconds when the branching factor is 1000, considering the order of magnitude of $t _ { a }$ and $t _ { c }$ are $\overline { { 1 0 ^ { - 6 } } }$ seconds. In fact, the experiment results in Section VI show that even a difference of 30 records in the processed number will ensure successful attack with high probability. This can be achieved when the branching factor is larger than 4. Thus, an adversary can perform tracking even when the branching factor is very large, which provides a lightweight but effective complement to the compromising attack [9].

Note that, BBST suggested in [20] is particular case of [11] with a full binary tree except that the searching can end on non-leaf nodes. The best case efficiency of BBST is O(1), while for worst case the search efficicency is O(logN). Thus it also suffers from the AMA attack. The pre-computation strategy suggested in [20] can solve the privacy flaw raised from computation but cannot eliminate the privacy leakage in access mode.

# 3) AMA on the MLDL protocol

In the MLDL protocol [13], the tags have two kinds of states, normal and abnormal. If a tag is in a normal state, it has not been scanned since the last successful authentication. The counter ctr stored in this tag is synchronized with the counter stored in the reader. Thus, the tag can be identified with searching efficiency O(1) via pre-computed tuples. If a tag is in an abnormal state, it has been scanned by a malicious reader at least once since the last successful authentication. Its counter becomes desynchronized with the corresponding $_ { c t r } ?$ stored in the reader. Then the tag can only be identified by the reader through exhaustive searching with efficiency O(N).

Given two randomly chosen tags utilizing the MLDL protocol, an adversary can force the two tags into two different states via deliberately scanning one of them for many times. Considering that O(1) is negligible compared to O(N), when N is sufficiently enough. The difference in terms of time cost between their processes should be O(N). Such a difference is obvious for an adversary to observe. If both of them are in an abnormal state, the attack is similar to the case of linear protocols, which means that the tags can be distinguished from each other as in the linear protocols. The expected value of difference between two tags’ time costs is about $( N - 1 ) { \times } t _ { s } / 2$ , which is larger than the value for linear protocols.

Above analysis focuses on three typical PPAs that are considered as private protocols. But the affected approaches are not limited to these protocols. In fact, most of the previously designed PPA protocols are vulnerable to AMA attacks and are not as private as they have been proven, considering the little attention paid on the distinguishable access modes before.

# IV. DISSCUSSION

In this section, we discuss the applicability of AMA.

# A. Applicability of measuring processing time

To launch AMA, an adversary should have the ability to measure the processing time consumed for locating a tag. In [18], it is considered that the adversary can obtain useful information about whether or not a reader accepts the output of a given tag as valid. This information is easy to obtain from most RFID applications. For example, an access card succeeds or fails to open a door, the “beep” sound when a payment card is accepted to complete a transaction, or a message authenticating the reader to the tag. In [19], a “wider” adversary can obtain this ‘side channel’ information by passive overhearing. Since a tag’s authentication message can be detected by monitoring the radio frequency signals transmitted in the air, the adversary can record the time point that the reader receives the message and the time point when the reader responds with an ACK message, i.e., the reader’s output. Then the processing time for the tag can be computed by a subtraction. An attacker can either collect data directly from regular authentication process or act as a man-in-themiddle between the reader and tag. Both methods are passive and hence easily to conduct and thus hard to detect.

# B. Stability in observed time differences

Besides the applicability, we also need to confirm that the differences in tags’ processing time are stable. AMA requires an adversary to observe the time used for a legitimate reader to answer a tag’s authentication message. Suppose the observed time for the reader to respond is $t _ { o b s e r v e } ,$ the time used for the reader to search and verify the tag is $t _ { \mathrm { s e a r c h } } .$ , and the overhead is $t _ { o v e r h e a d } ,$ we have

$$
t _ {\text { observe }} = t _ {\text { search }} + t _ {\text { overhead }}.
$$

If the database is stored in RAM and does not use any cache, the processing time for locating a certain tag, including the access time and computation time, is relatively stable and thus observable, as analyzed in Section III.

When the RFID system is huge, it is inevitable to store records on hard disks. The order of magnitude of access time for a record on hard disk will be of $1 0 ^ { - 2 }$ seconds, which dominates the hash computation time for this record. If the database is stored on hard disk without cache strategy, then the adversary can find difference between tags much easier than the case of RAM database discussed in Section III.

If the system utilizes cache schemes, the case becomes complicated, since there are different kinds of cache strategies. But we show below that the difference is still observable.

Given two tags $T _ { 1 }$ and $T _ { 2 } ,$ their orders in the database are $\quad O _ { 1 } , \quad O _ { 2 } ,$ while $o _ { 1 } < o _ { 2 }$ . During attacking each of the two tags, we allow the adversary to continuously attack the tag. This will cause the reader’s continuously processing of the tag. After several rounds of continuously searching the record for the related tag, the cache status for the tag becomes regular and the number of the cached records for this tag approaches the maximum. Suppose the number of cached records for $T _ { 1 }$ and $T _ { 2 }$ at this time are $c _ { 1 }$ and $c _ { 2 } .$ , respectively, then there may be two caching status.

$\bullet c _ { 1 } < o _ { 1 }$   
$\bullet \mathrm { ~  ~ \omega ~ } o _ { 1 } = c _ { 1 }$

![](images/0d51cdc461fd6d37dce048855585cafeb3036dd0bcfbcd91ca5293b75f3cb46c.jpg)



Figure 8. Random access mode

For the first case, there are still some records for processing $T _ { 1 }$ not cached. This is because $c _ { 1 }$ is the total cache available for processing tags. Then we have $c _ { 2 } = c _ { 1 }$ . Because $T _ { 2 }$ is stored behind $T _ { 1 } ,$ authenticating it requires processing more uncached records. Then authenticating $T _ { 2 }$ consumes more time than authenticating $T _ { 1 { \mathrm { : } } }$ , although the difference is smaller than the situation without caches.

For the second case, all the records for processing $T _ { 1 }$ are cached. In this case, the number of cached records for $T _ { 2 }$ may be larger than $c _ { 1 } .$ But the time consumed by these cached records is already larger than the total time consumption of processing $T _ { 1 }$ .

The $t _ { o v e r h e a d }$ in the observed time comprises the routine overheads, including the observation delay, and the transmitting time for the signals between reader and the backend database. The observation delay is the offset between the time point when the reader sends out authentication result and the time point when the adversary detects this message. The observation delay is tiny considering the high speed of the electromagnetic wave. The transmitting time between reader and the server is also tiny because of the high speed communication between the reader and server. Thus, the differences in the $t _ { o v e r h e a d }$ of the tags are relatively tiny compared to the observable differences in $t _ { s e a r c h }$ .

Combining the analysis for the observed time, the differences between tags are observable and this feature is relatively stable, as will be illustrated by the evaluation results in Section VI.

# V. RECOMMENDATIONS

In this section, we present on some recommendations for mitigating the impact of AMA attacks. The characteristic utilized by our attack is the lack of randomness in access mode other than computation. Thus, we propose some recommendations to bring randomness into the access mode of protocols.

# A. Access randomization

We propose the following two suggestions to randomize the tags’ access mode.

Random starting point   
• Random access

The random starting point strategy works as follows.

Each time for authenticating a tag, we let the reader start its search process from a randomly chosen position. When R reaches the last record in the database, R can perform a circular shift to move to the first record and continues the search process.

![](images/d00a4c62a9e4fdd5933309526486dab3a1c26a738b072824bce5058313bd71d6.jpg)



Figure 9. Location Updating

The random access strategy works on another way. During an exhaustive search, the records are processed in random sequence other than sequential sequence until a matched record is found, as illustrated in Fig. 8.

These two schemes are suitable for strengthening the improved random hash-lock protocol. For tree-based PPA protocols, the schemes can be applied on each virtual node for accessing its branches. In this way, the branches checked during locating for a tag varies at each authentication process. Thus, the accessing process in the database is randomized. Meanwhile, the access time and computation time for locating a certain tag varies at each authentication process. The processing time of tags will no longer be a distinguishable feature, which eliminates the observable features of processing time.

# B. Location updating

The above recommendations focus on randomizing the access when locating a tag. Another practical way is to change the location of a tag’s record after each authentication. The reader can update the location of tag $T _ { \mathrm { i } } { } ^ { \mathrm { * } }$ s record to a new randomly selected empty position in the database. If no empty position is found, the reader randomly chooses another record in the database and swaps $T _ { i } { ^ \mathrm { 3 } \mathrm { s } }$ position with this record, as illustrated in Fig. 9. Such a treatment introduces randomness into the storage of tags. The access mode is further randomized process time for authenticating a certain tag. Both linear and tree-based protocols can utilize this strategy to enhance privacy.

# C. Delayed response

Besides the above measurements, the reader can purposely introduce a random delay to each authentication process. The upper bound of the delayed time is the worst case of processing time among all tags. This scheme is effective to enhance privacy especially when the size of the system is small. But for a huge system, this scheme may incur a high latency when authenticating tags, which is unacceptable to some time-restricted applications.

# VI. EXPERIMENT AND EVALUATION

In this section, we evaluate the effectiveness of the proposed attack in terms of the adversary’s capability of differentiating tags. Indeed, this capability reflects the adversary’s success possibility in winning a privacy game [17-19].

TABLE I. SYSTEM INFORMATION 

<table><tr><td>Model: DELL PRECISION T3400</td></tr><tr><td>Processor: Intel® CoreTM 2 Duo CPU E8400@ 3.00GHz 2.99 GHz</td></tr><tr><td>L1 Cache: 32 K Bytes</td></tr><tr><td>L2 Cache: 6144 K Bytes</td></tr><tr><td>Installed memory (RAM): 8128MB (DDR2-800 DDR2 SDRAM)</td></tr><tr><td>Network adapter: Broadcom NetXstreams 57xx Gigabit Controller</td></tr><tr><td>System type: 64-bit Operating System</td></tr><tr><td>Operating system: Windows 7 Enterprise</td></tr><tr><td>Database: MySQL 6.0</td></tr><tr><td>Develop Language: Java</td></tr></table>

TABLE II. RESULTS UNDER AMA ATTACK [MICROSECONDS] 

<table><tr><td rowspan="2">Times\Tags</td><td colspan="2"> $T_1$ (order = 10107)</td><td colspan="2"> $T_2$ (order = 39971)</td></tr><tr><td>With hash</td><td>No hash</td><td>With hash</td><td>No hash</td></tr><tr><td>1</td><td>704359.452</td><td>653014.318</td><td>2690264.009</td><td>2484898.875</td></tr><tr><td>2</td><td>678684.338</td><td>627329.203</td><td>2692507.399</td><td>2487142.265</td></tr><tr><td>3</td><td>686784.975</td><td>635439.841</td><td>2703037.919</td><td>2497672.785</td></tr><tr><td>4</td><td>676594.591</td><td>620108.943</td><td>2686465.713</td><td>2481100.579</td></tr><tr><td>5</td><td>685333.068</td><td>628847.42</td><td>2695577.175</td><td>2469651.527</td></tr><tr><td>6</td><td>665363.612</td><td>603747.451</td><td>2692474.549</td><td>2466588.902</td></tr><tr><td>7</td><td>687404.337</td><td>636059.203</td><td>2693704.718</td><td>2467779.07</td></tr><tr><td>8</td><td>699973.275</td><td>638357.114</td><td>2683124.238</td><td>2457238.591</td></tr><tr><td>9</td><td>682756.728</td><td>631411.594</td><td>2684102.557</td><td>2458176.909</td></tr><tr><td>10</td><td>690120.632</td><td>628504.471</td><td>2691147.540</td><td>2485782.406</td></tr></table>

During the attack, the adversary records the time point when the tag finishes transmitting the authentication message and the time point when the reader emits an ACK. In our experiments, we use a set of RFID equipments, such as the NI PXI-1044 RFID testing tool with PXI 5600 receiver, as tools to capture these two time points. Note that attackers can employ any off-the-shelf RFID device as long as it can capture the RF signals, which makes it easy to perform AMA. We adopt a programmable tag based on the G2C5477 module from G2 Microsystems [25]. We employ this module to fulfill fundamental cryptographic functions. We also employ an off-the-shelf RFID reader, ALR-9900, manufactured by Alien Corporation [26], as the legitimate reader. We setup the backend database system, as illustrated in Table I. The backend system communicates with the reader through a local Ethernet.

We simulate $2 ^ { 2 0 }$ tags in the backend system. We mainly show results for the improved randomized hash-lock protocol. But the results can be extended to other protocols, as analyzed in Section III. The cryptographic hash algorithm adopted in the protocol is SHA-1. Each tag has a record stored in the database, containing a 64-bit ID and a 160-bit key of the tag. The total storage space is about 28 MB.

During the experiment, we allow a target tag to authenticate the legitimate reader for a number of times. Each time, we attack the tag by recording its processing time. We iteratively conduct AMA to each tag and evaluate the results with our metrics.

# A. Results of Performing AMA

During the experiment, we randomly choose two tags $T _ { 1 }$ and $T _ { 2 }$ and record the results when SHA-1 or direct comparison is employed. Their 10 results of processing time are listed in Table II. In the database, the tag $T _ { 1 }$ is correlated to the 10107th record, and $T _ { 2 }$ is correlated to the 39971th record. We can find that the processing time of a tag varies in different authentications. But the variation is slight compared to the overall processing time. The variation for $T _ { 1 }$ is in the range of about 40 milliseconds, which is about 5% of the overall processing time. For $T _ { 2 } ,$ the variation range is near 20 milliseconds, which is about 7% of the overall processing time. We can also find that the computation time used by hash functions is less than 10% of the total processing time, which supports our point in Section IV.

![](images/8dd8195c76dd05b17f7e3a167c718d5fe6e0d1d7b596cfa6ef7fd4983f59ea78.jpg)



Figure 10. Results from two randomly chosen tags

![](images/f7ec166ee8181f5c0fe7d5565c53b9b89eb5fd36a4288c9b41cce9a42b9597ba.jpg)



Figure 11. Statistical results with different differences in NRs

We plot the statistical results of two tags’ variations in Fig. 10. Based on Table II and Fig. 10, it is very clear that $T _ { 2 }$ always consumes much more time than $T _ { 1 } .$ . The difference between their time consumption is obvious and they can be easily differentiated.

We then evaluate the resolution power of AMA. This is done by reducing the difference of two tags’ processed number of records (NRs) until they cannot be definitely differentiated.

Fig. 11 shows the statistical results of the difference of two tags. It plots the result in the processing time to their difference in NR values. In this figure, we denote distance as the difference in NRs. In the improved randomized hash-lock protocol, the distance of two tags reflects how many records are between their records in the database. When the distance arises from 30 to 30000, the time difference between two tags increases accordingly, from around 1800 microseconds to around 1900 milliseconds. We find that when the distance between two tags is above 30, they can be distinguished from each other. This observation indicates that the resolution power of AMA is at least 30 when attacking a hash-lock PPA protocol. This condition is highly possible to be satisfied for any pair of tags in a large-scale RFID system. For example, in our testing system, there are 1,000,000 tags. The success rate of differentiating any two tags is at least (1000000 – 60)/1000000, i.e., 99.99%. This means that the attacker can distinguish two tags with nearly 100% possibility. The attacker can then launch further attacks, for example the tracking attack, on the tags and their carriers.

There is an interesting phenomenon we should pay attention to. When the distance between two tags is 30, their processing time difference is about 1800 microseconds. If considering the computation time only, the difference should be about 150 microseconds, where in our evaluation one time hash computation consumes about 5 microseconds. The time spent on access dominates the time spent on computations. This phenomenon supports our claim that the randomness-lacking access mode is the major source of RFID privacy leakage, while the computation time is negligible compared to the access time and unobservable.

# VII. CONCLUSION

Existing RFID PPA works mainly focus on randomizing the messages exchanged in authentication. Little consideration is paid to the access mode of tags. In this paper, we study the distinguishable access mode of tags in breaking private RFID systems. The attack based on this characteristic is lightweight but effective. Our analysis and experiment results show the effectiveness of the attack to RFID protocols that are proven private. Furthermore, we provide recommendations for defending against such attacks.

# ACKNOWLEDGMENT

This work is supported in part by Hong Kong ITF Fund GHP/044/07LP and ITP/037/09LP, NSFC under grants No. 60933003, No. 60736016, No. 60873262, and No. 60903155, China 863 Program under grant No. 2009AA01Z116, China 973 Program under grants No. 2011CB302705 and No. 2010CB328004, China Postdoctoral Science Foundation funded project under grant No. 20090461298, Shaanxi ISTC under Grant No. 2008KW-02, and IBM Joint Project.

# REFERENCES

[1] G. Roussos, and V. Kostakos, "RFID in pervasive computing: stateof-the-art and outlook," Pervasive and Mobile Computing, Vol. 5, No. 1, pp. 110-131, 2009.

[2] X. Wu, G. Chen, and S.K. Das, "Avoiding energy holes in wireless sensor networks with nonuniform node distribution," IEEE Transactions on Parallel and Distributed Systems, Vol. 19, No. 5, pp. 710-720, 2007.   
[3] X. Xu, X.-Y. Li, X. Mao, S. Tang, and S. Wang, "A delay-efficient algorithm for data aggregation in multihop wireless sensor networks," IEEE Transactions on Parallel and Distributed Systems, Vol. 22, No. 1, pp. 163-175, 2011.   
[4] M. Kodialam, T. Nandagopal, and W.C. Lau, "Anonymous tracking using RFID tags," in Proceedings of IEEE INFOCOM, 2007.   
[5] A. Juels, "RFID security and privacy: a research survey," IEEE Journal on Selected Areas in Communications, Vol. 24, No. 2, pp. 381-394, 2006.   
[6] G. Avoine, "Bibliography on security and privacy in RFID systems," available online at http://www.avoine.net/rfid/, 2011.   
[7] S.A. Weis, S.E. Sarma, R.L. Rivest, and D.W. Engels, "Security and privacy aspects of low-cost radio frequency identification systems," in Proceedings of SPC, 2003.   
[8] M. Ohkubo, K. Suzuki, and S. Kinoshita, "Efficient hash-chain based RFID privacy protection scheme," in UbiComp Privacy Workshop, 2004.   
[9] G. Avoine, E. Dysli, and P. Oechslin, "Reducing time complexity in RFID systems," in Proceedings of SAC, 2005.   
[10] D. Molnar, and D. Wagner, "Privacy and security in library RFID: issues, practices, and architectures," in Proceedings of ACM CCS, 2004.   
[11] T. Dimitriou, "A secure and efficient RFID protocol that could make big brother (partially) obsolete," in Proceedings of IEEE PerCom, 2006.   
[12] M. Ohkubo, K. Suzuki, and S. Kinoshita, "Cryptographic approach to "privacy-friendly" tags," in RFID Privacy Workshop, MIT, 2003.   
[13] C. Ma, Y. Li, R.H. Deng, and T. Li, "RFID privacy: relation between two notions, minimal condition, and efficient construction," in Proceedings of ACM CCS, 2009.   
[14] L. Yang, J. Han, Y. Qi, and Y. Liu, "Identification-free batch authentication for RFID tags," in Proceedings of IEEE ICNP, 2010.   
[15] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, "Season: shelving interference and joint identification in large-scale RFID systems," in Proceedings of IEEE INFOCOM, 2011.   
[16] A. Shamir, "SQUASH - a new MAC with provable security properties for highly constrained devices such as RFID tags," in Proceedings of FSE, 2008.   
[17] G. Avoine, "Adversarial model for radio frequency identification," IACR E-print report, Vol. 49, 2005.   
[18] A. Juels, and S.A. Weis, "Defining strong privacy for RFID," ACM Transactions on Information and System Security, Vol. 13, No. 1, pp. 1-23, 2009.   
[19] S. Vaudenay, "On privacy models for RFID," in Proceedings of ASIACRYPT, 2007.   
[20] G. Avoine, I. Coisel, and T. Martin, "Time measurement threatens privacy-friendly RFID authentication protocols," in Proceedings of RFIDSec, 2010.   
[21] D. Zanetti, B. Danev, and S. Čapkun, "Physical-layer identification of UHF RFID tags," in Proceedings of ACM Mobicom, 2010.   
[22] S.C.G. Periaswamy, D.R. Thompson, H.P. Romero, and J. DI, "Fingerprinting radio frequency identification tags using timing characteristics," in Proceedings of RFIDSec Asia, 2010.   
[23] Q. Yao, Y. Qi, J. Han, J. Zhao, X. Li, and Y. Liu, "Randomizing RFID private authentication," in Proceedings of IEEE PerCom, 2009.   
[24] T. Halevi, N. Saxena, and S. Halevi, "Using HB family of protocols for privacy-preserving authentication of RFID tags in a population," in Proceedings of RFIDSec, 2009.   
[25] http://www.g2microsystems.com/.   
[26] http://www.alientechnology.com/readers/alr9900.php.