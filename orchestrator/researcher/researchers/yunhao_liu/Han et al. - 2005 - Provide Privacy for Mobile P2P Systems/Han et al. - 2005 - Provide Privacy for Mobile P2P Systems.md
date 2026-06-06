# Provide Privacy for Mobile P2P Systems

Jinsong Han $^{1}$ , Yanmin Zhu $^{1}$ , Yunhao Liu $^{1}$ , Jianfeng Cai $^{2}$ , Lei Hu $^{3}$

$^{1}$ Department of Computer Science, Hong Kong University of Science & Technology, Hong Kong

$^{2}$ Department of Computer Science, Texas A&M University, USA

$^{3}$ The State Key Laboratory of Information Security, Chinese Academy of Science, Beijing, China

{jasonhan, zhuym, liu}@cs.ust.hk, j0c1194@cs.tamu.edu, hu@is.ac.cn

# Abstract

Nowadays privacy and anonymity have become an increasing requirement in wireless networks. However, current mobile peer-to-peer architectures have not taken into account anonymity, especially the mutual anonymity between two nodes. In this paper, we propose a mutual anonymity protocol, called Secret-sharing-based Mutual Anonymity Protocol (SMA), for mobile P2P networks. Our simulation results show that SMA achieves mutual anonymity in mobile P2P networks with a low cryptography processing overhead.

# 1. Introduction

Wireless technology has promoted mobile peer-to-peer networks into a high flexible information sharing system. In the past years, user privacy requirements have become increasingly urgent, and anonymity issue in such systems has not been fully addressed.

In mobile P2P environment, anonymity $[1]$ can be divided into three types: resistant-censorship (or publishing anonymity), initiator or responder anonymity, and mutual anonymity (both initiator and responder anonymity). Strictly defined, mutual anonymity is made up of three parts: an anonymous initiator, an anonymous responder and anonymous communications between the two parties.

This paper focuses on decentralized mobile P2P networks[5, 7, 11]. All participants in a mobile P2P system communicate with their neighbors. Theoretically no node has any knowledge of other peers two or more hops away. Based on this observation, a mobile P2P network is able to achieve partial anonymity at least among those non-neighboring peers.

However, current mobile P2P protocols fail to provide real anonymity guarantees. Since queries are flooded in plain text, contents of these messages are exposed to malicious nodes, and attackers can easily This work was partially supported by Hong Kong RGC DAG 04/05.EG01, NSFC 60373041.

guess the identities of the communication parties. Also, every node is monitored by its neighbors. Hence, mobile P2P systems cannot provide initiator and responder anonymity in each node's very local environment.

In this paper, we propose a mutual anonymous protocol, called Secret-sharing-based Mutual Anonymity (SMA). SMA provides initiator and responder anonymity, as well as communication security in mobile P2P systems. In SMA, we employ a secret sharing scheme to anonymously issue queries, and use the information dispersal algorithm (IDA) $[12]$ together with the onion routing $[20]$ to redundantly deliver requested data.

The rest of this paper is organized as follows. In the next section, we introduce some previous work related to this topic. Section 3 presents the SMA design. In Section 4, we analyze anonymity and security degree of SMA. Simulation results are presented in Section 5. We conclude the work in Section 6.

# 2. Related Work

Initiator anonymity can be achieved by forwarding packets through a predetermined path made by the sender, such as MorphMix $[15]$ and Onion $[20]$ . Instead of allowing initiators to create paths, in Crowds $[14]$ peers randomly selects a succeed peer to build a furtive path. Hordes $[19]$ is similar to Crowd, but deploys multicast services and anonymously sends a reply back to the initiator. Freedom $[3]$ and Tarzan $[6]$ are implemented over IP and transport layers and depending on Onion Routing to build main architectures. NICE $[23]$ is based on a Reputation record mechanism or trust interface technology.

Peer-to-peer Personal Privacy Protocol (P $^{5}$ ) [18], based on a global broadcast channel, aims at mutual anonymity. The basic idea of P $^{5}$ is that all participants in the channel send fixed length encrypted meaningful or noise messages at a fixed rate as if all participants are grouped in a logic ring. Each joining peer is mapped to a special group using a hash of their public key. As the $P^{5}$ is based on the assumption that the initiator knows the public key of the query responder, it is difficult to be appropriately used. Anonymous Peer-to-peer File Sharing (APFS) [16], designed for mutual anonymous communications, mainly based on a Mix like anonymity scheme. Initiators anonymously send queries to some coordinators acting as tail nodes for available indices of requesting documents. The tail node returns lists of current available servers. Initiator peers then anonymously contact the servers to send requests and receive data. All anonymous communications of this framework are based on the onion path.

Xiao et al. [22] provide a Shortcut-responding Protocol anonymity solution in pure P2P systems. In this protocol, an initiator binds an onion-structured returning path with each query. Each peer that receives the query decides whether or not to devote itself as the query agent node in a probability. The main advantages of this work include the shorter-than-normal return path patterns and the high degree of security for the RSA-based encryption method.

# 3. Design of SMA

# 3.1 Secret sharing overview

The primary motivation of the secret sharing scheme is to avoid a single point of failure in key maintenance procedure. One of the most popular secret sharing schemes is Shamir's $(k, n)$ secret sharing scheme (SSS) [17], in which any $k' (k' < k)$ players cannot acquire any information about the secret. A mathematical illustration of Shamir's scheme is as follows.

Preparation: The dealer chooses a large prime number $p$ . The secret to be shared is an integer $s$ with $0 \leq s < p$ . The dealer chooses distinct $x_{i}$ ( $i = 1,..,n$ ) pair wise $t$ . For $n$ participants, the dealer randomly chooses $t - 1$ independent integers $a_{j}$ with $0 \leq a_{j} < p$ for $j = 1,2,\dots,t - 1$ .

# Computing shares:

$$
- \text {   Define   } f (x) = s + a _ {1} x +... + a _ {t - 1} x ^ {t - 1} \bmod p.
$$

$$
- \text {   The   share   for   the   } i \text {-th   participant   is   } (x _ {i}, f (x _ {i})) \text {   for   } i = 1, 2,..., n.
$$

# Distributing shares:

\- Distribute each share $(x_{i},f(x_{i}))$ to each participant.

# Recovering shares:

\- When any $t$ participants come together, they can solve the set of equations to recover $s$ (and also $a_i$ ).

The complexity of Lagrange interpolation is $O(t\log_{2}t)$ .

IDA[13] is first introduced by Rabin. Similarly, it intends to distribute information $s$ among $n$ participants. The difference between IDA and Shamir's scheme is that the length of each shares of IDA is $|S| / m$ , where $S$ is the original information. Therefore IDA is more space efficient. IDA is often employed together with the erasure code scheme.

In our SMA protocol, we use SSS to distribute a symmetric key when issuing queries anonymously. To defend against attacks in the middle, we employ a secret information dispersal algorithm, SIDA[9] to achieve secure file-transferring.

# 3.2 SMA Design

Before presenting the details of SMA, we first introduce some notations used in this paper. We let $f$ denote the desired file name or id, $A$ denote the initiator of a query, $V_{i}$ denote $A$ 's neighboring nodes, $B$ denote the query responder, $P_{i}$ denote nodes in mobile P2P systems and $sn$ denote the sequence number to mark queries. We use $A \to B$ : $M$ , to represent $A$ sending a message $M$ to $B$ . We use $K_{X}$ to represent the public key of $X$ and $K$ to denote the AES key. We define $\{M\}_{K}$ as encrypting the message $M$ with the key $K$ (RSA or AES).

In SMA, we also add a local switch table to record the packet's information received from or sent to the neighbors in each node. In addition, a timeout-drop scheme is employed to improve efficiency. The details of SMA are as follows.

# 3.2.1 Anonymous query

(1) The initiator A randomly selects a list of neighboring nodes, $V_{1}$ , $V_{2}$ ... $V_{n}$ . It generates a random AES key T, which is used to encrypt f.

# Distribution method:

Select random key $T$ and encrypt $f$ as $e = E_{T}(f)$ .

Partition $e$ into $n$ fragments using IDA, $e_1 \ldots e_n$ .

Partition $T$ into $n$ shares using $(k, n)$ SSS, $T_{1}...T_{n}$ .

Distribute $(e_i, T_i, k)$ to $n$ pieces $s_i$ .

Meanwhile, A produces a sequence number sn to identify a certain query. Also, A creates a pair of RSA keys, here we denote the public key $K_{A+}$ . For driving the reply back, A also creates an anonymous onion path for potential responder:

$$
F P = \{X, \{Y,.. \{Z, \{A, f i x m i x, s n \} K _ {A +} \} K _ {Z +} \},.. \} K _ {Y +} \} K _ {X +} \}.
$$

![](images/c1fdac1939503555b7c18bc420727db4750b72197faf3672e60bf9d256632512.jpg)



Figure 1: Anonymous Issue a Query

Node $A$ randomly selects neighboring nodes $V_{i}$ , and sends $s_{i}$ , $i = 1..n$ to them, respectively. When sending these messages, $A$ embeds $K_{A+}$ in the packets: $A \rightarrow V_{i}: \{s_{i}, K_{A+}, sn, FP\}$

(2) When a neighbor of $A$ receives a new query share, it floods this share in probability $p$ . In other words, it forwards the query share to one of its neighboring node except $A$ in a probability $1 - p$ .

$$
V _ {i} \xrightarrow {\text { flooding } / p} P _ {j}: \left\{s _ {i}, K _ {A +}, s n, F P \right\}
$$

For both flooding and a single-direction-forwarding pattern, $V_{i}$ stores the received and forwarding information of each query in its local switch table.

Once a node receives a share query, it compares the sn in its switch table. If there exists a subset labeled the same sn without this share, the node appends the share information to this subset; otherwise it establishes a new subset labeled the new sn for this share. During certain number of hops, different shares labeled the same sn would be gathered in one or more nodes. Without loss of generality, we suppose $P_{1}$ is one of the nodes which collect enough number of shares of the query to recover f.

# Reconstruction method:

Given $k < n$ shares $s_i = (e_1, T_1) \ldots (e_k, T_k)$ .

Reconstruct $e$ from $e_1\ldots e_k$ .

Reconstruct $T$ from $T_{1}\ldots T_{k}$ .

Decrypt $f = D_{T}(e)$

When $P_{l}$ obtains the recovered f, it floods the query in plain text, if it is willing to serve as a query agent. The content of queries includes ID of $P_{l}$ , f, $K_{A+}$ , sn, and FP. Fig. 1 illustrates the above procedure of anonymous query issuance.

![](images/09b64f8c262955825f7e691b29a09d070af84658b1ec223c1ab76b4f75193160.jpg)



Figure 2: Query confirmation and file transferring

# 3.2.2 File Delivery

(1) Upon request $f$ , if a node $B$ is able to provide the requested file $F$ , it builds an anonymous reversed path:

$$
R P = \{U, \{V, \dots \{W, \{B, f i x m i x \} K _ {W} \}, \dots \} K _ {V} \} K _ {U} \}.
$$

B generates a reply message including an index of desired file and ID of $P_{1}$ , encrypting them with $K_{A+}$ and delivers the packet through FP to A anonymously. When the reply packets (from different responders) reach A, A decrypts the innermost cipher and gets the sn and files index.

(2) There could be more than one responder. At the same time, node A may receive more than one ID of agent node. A will pick one, B, as a responder, and creates a list L from the set of $P_{i}$ , where $L = \{P_{1}...P_{m}\}$ . In addition, it selects a threshold $k' < m$ for SIDA to split the requested file. Then Node A sends the confirm packet embedded with the list L and $k'$ to the first node which is appointed by the responder B on its onion return path RP.   
(3) $B$ gets the request-confirm packet from the last $RP$ onion node. It makes use of SIDA as follows.

# Distribution method:

Select random AES key $K$ and encrypt $f$ with $K$ : $e' = E_K(F + hash(F))$

Encrypt key K with key $K_{A+}$ to get $T'$

Partition $e'$ into $m$ fragments using $(k', m)$ IDA and obtain $e'_1 \ldots e'_m$ . $(m = |l|)$ .

Partition $T'$ into $m$ shares using $(k', m)$ SSS to get $T'_{1}... T'_{m}$ .

Distribute $(e'_{i}, T'_{i})$ to participant $s'_{i}$

B eventually creates m split data fragment packets $s'_{i}$ for m nodes in L, and marks the packet as a data type and labels it sn. The entire information of list L is put in every packet as well. After these steps $B$ randomly chooses its $m$ neighbors (if $B$ 's neighbors are less than $m$ , $B$ can send some packets to the same neighbor), and sends the above packets.

Each node which receives a packet randomly selects a node from L to forward the packet to. This relay node then delivers the packets to the next node marked sn. The data packets are relayed to reach some members of L. Those nodes in L will deliver the packet to A.

(4) Node A keeps a check on the number of sn-marked data packets it receives. Finally it recovers the file as follows.

# Reconstruction method:

Given $k' < m$ shares $(e'_1, T'_1, k'), ..., (e'_k, T'_k, k')$

Reconstruct $e'$ from $e'_{1} \ldots e'_{k}$ ,

Reconstruct $T'$ from $T'_{l}, \ldots, T'_{k'}$

Decrypt $T'$ with $A$ 's private key to get $K$

Decrypt $F = D_{K}(e')$ ; checkout the file with hash(F)

Figure 2 illustrates query reply, confirmation and file transferring procedure.

# 4. Discussions

# 4.1 Anonymity Degree Analysis

Now we analyze the degree of anonymity of SMA.

The initiator and responder: The probability for an initiator or a responder to randomly guess opposing party's identity is $1/(n-1)$ , where $n$ is the number of nodes in mobile P2P. Especially on the onion path, the expected number of path reformations required for $c$ attackers to determine the initiator out of $n$ participants is $A((n/c)^{l})$ , where $l$ is the length of the path between the initiator and responder [21].

The middle nodes: In the query-flooding path, the middle nodes can be divided into two groups: one includes the nodes who receive the shares. The other group is the remaining nodes except the initiator and responder. For the first group, its members make a random guess on who the initiator or the responder are will have probability of $1/(n-1)$ . Let $p_{x}(k)$ denote the probability of existing k hops between the initiator and node x. Here middle nodes mean all such nodes that have few hops from the initiator to themselves than x does. S is a subset of the whole mobile P2P systems in which the nodes get their shares from the initiator. The probability that guess whether the node from whom x obtains the share is the initiator is: $\frac{1}{|S|-1}\sum_{k=1}^{|S|-1}\frac{p_{k}(k)}{k}$ . On the file forwarding path, the

random guess probability that a certain node is the initiator is 1/(n-2). For those nodes that obtain file shares, the average probability that the guess a initiator or responder out will be: $\sum_{k=1}^{n-2} \frac{p_i(m)}{(n-2)m}$ , where $m$

is the number of nodes on the data packets transferring path. Considering the large amount of the practical mobile P2P systems nodes, all the exposed probabilities in the above cases become very small.

# 4.2 Security analysis

SMA deploys encryption methods both in the query flooding and the file transferring to achieve information security. Malicious nodes may cooperate together to implement attacks.

In anonymous query issuing procedure, SMA employs SSS to protect the initiators' privacy in a perfect security. Perfect secrecy is that, the adversary is unable to obtain any information from the cipher. Therefore the observed cipher text is completely meaningless. In $(t,n)$ SSS scheme $(t<n)$ , given any t shares, the polynomial is uniquely determined. Hence, the secret s can be computed. However, given t-1 or fewer shares, the secret can be any element in the field and thus those shares do not supply any further information regarding the secret [8]. Thus we claim that the share distribution procedure of SMA is perfect secrecy.

On the other hand, we claim that the file split pattern of SIDA provides a computatianl security to the responders.

Definition 1: Two ensembles of random variant, $E_0 = \{X_u\}$ and $E_1 = \{Y_u\} (u = 1,2,\dots)$ , are polynomial indistinguishable if for every (probabilistic) polynomial-time algorithm, $A$ , and every positive polynomial $p(u)$ such that for all sufficiently large $u$ , $\left|\Pr(A(X_u) = 1) - \Pr(A(Y_u) = 1)\right| < \frac{1}{p(u)}$ . A distinguishing

algorithm is the one that successfully guesses the correct distribution with probability $\frac{1}{2} + l^{c}$ , where l is the distribution index.

Theorem 1: Assume $E$ is a secure encryption algorithm. Then SIDA achieves computational security.

Proof: We assume that there exists an algorithm A which can polynomially distinguish the SIDA fragments of the ciphertexts of two different file $f_{u}$ and $g_{u}$ under E. Let the $(k', m)$ IDA algorithm [13] be defined on a finite field of q elements, $Z_{q}$ (with q prime). Let the bit lengths of $f_{u}$ and $g_{u}$ be $(k' \text{ ulog } q)$ .

![](images/83b6b4d26c7c9ca53ebadfcf23ce615fd17094a49a126c16bd45143572369ca0.jpg)



Figure 3: Traffic cost

Set $x_{u} = E(f_{u} \parallel hash(f_{u}))$ , $y_{u} = E(g_{u} \parallel hash(g_{u}))$ , and let $X_{u}$ and $Y_{u}$ be the SIDA fragments of $x_{u}$ and $y_{u}$ , respectively. Then there is positive polynomial $p(u)$ such that for sufficiently many u,

$$
\left| \operatorname * {P r} (A (X _ {u}) = 1) - \operatorname * {P r} (A (Y _ {u}) = 1) \right| \geq \frac {1}{p (u)}.
$$

Define a probabilistic polynomial-time algorithm $B$ as $B(x) = A(IDA(x))$ . By elementary linear algebra and the nature of IDA, it is easy to know that the probability that two different messages of $(k' \log q)$ bits, $x$ and $y$ , have same $k'$ -1 IDA fragments is $1/q$ , and so, the probability that different $x_u$ and $y_u$ have different fragments $X_u$ and $Y_u$ is $1-(1/q)^u \geqslant 1-1/q$ . Now we have

$$
\left| \operatorname * {P r} (B (E (f _ {u})) = 1) - \operatorname * {P r} (B (E (g _ {u})) = 1) \right| \geq \frac {q}{(q - 1) p (u)} \geq \frac {1}{2 p (u)}
$$

Actually the SIDA algorithm ensures that the m-1 fragments would not expose any information about files if we employ secure encryption algorithms[9].

In SMA, we use the RSA and AES as the practical secure algorithms. Some improved RSA based schemes can eventually provide the indistinguishability $[10]$ . Therefore, SMA is able to protect file information from malicious entities and defend security of the initiator and responder.

# 5. Performance Evaluation

We simulate mobile P2P topologies with DSS Clip [2] trace. Based on the basic distributions of peering node, we introduce mobile feature into these Traces. The results are consistent with different traces. In this discussion, we show the results on the trace May 25, 2001.

In our simulation, we simulate flooding search in a mobile P2P network by conducting Breath First Search algorithm from a specific node. A search operation is started by randomly choosing a node as the sender, and a keyword according to Zipf distribution [4]. We take 1,000 search operations in each run. We simulate dynamic node changes including joining and leaving by assigning a lifetime in seconds to every node. Each node can make a movement randomly so that the overlay topologies are changing accordingly.

![](images/8ac778ca7ec344d1b3da0686e922e0a0635a3577a8765f7c07b4e1e30f6d963b.jpg)



Figure 4: Response time

First we present the experimental results on traffic overhead and response time of SMA. Traffic cost is one of the most important parameters which network administrators focus on. The traffic cost added by SMA is mainly caused by the share flooding. We show the one hour average query cost in Fig. 3. Indeed, the more the shares are split, the higher the traffic cost is. When the split shares number is 12 and probability is 0.3, the average traffic cost is 23103, which is close to 24368, an average normal flooding traffic cost of the system. Although increasing the average probability leads to a high rate of query recovery from shares, the traffic cost grows as well. In our design, by setting a proper average probability as 0.3, we balance the traffic overhead and system reliability.

We define response time of a query as the time period from when the query is issued until when the source node receives a response result from the first responder. Figure 4 shows that the additional delay time caused by SMA is about 40% of the normal query response time. Considering the tradeoff with the mutual anonymity achievement, this additional delay is acceptable. We also notice that decreasing the threshold of SSS may result in a fast result-return for the increment of middle agents. However, the traffic cost would also increase.

We then present the security cost in our protocol increased by SMA protocol. Security overhead is defined as the cost spent in the shares distribution

Table 1: Security Overhead 

<table><tr><td>Algorithm</td><td>Iteration</td></tr><tr><td>SSS Distribution and Reconstruction</td><td>1+l</td></tr><tr><td>IDA Distribution and Reconstruction</td><td>1+l</td></tr><tr><td>SIDA Distribution and Reconstruction</td><td>1+1</td></tr><tr><td>1024bit RSA Encryption</td><td>2t+1</td></tr><tr><td>1024bit RSA Decryption</td><td>2t+1</td></tr><tr><td>128bit AES</td><td>4</td></tr></table>

and reconstruction procedure of SSS, RSA encryption and decryption, and AES encryption and decryption. We show the security related operations among relevant nodes in a complete search procedure in Table 1, when the average number of agent nodes is l and the average length of Onion path is t.

# 6. Conclusion

In this paper, we propose a mutual anonymity protocol, SMA, in mobile P2P systems. SMA employs Shamir's secret sharing scheme to let nodes issue queries and responders deliver requested files anonymously. Compared with previous designs, SMA achieves mutual anonymity in mobile P2P systems with a higher degree of anonymity and a lower cryptographic processing overhead.

Future work on SMA will lead into two directions. One is to reduce the traffic cost of the share flooding by using self-adapting mechanisms. The other is to deploy the SMA prototype combined with the construction of Freenet system to achieve the publish anonymity in real systems.

# 7. References

[1] Anonymity, http://freehaven.net/anonbib/topic.html   
[2] The Gnutella Protocol Spedification v0.4, http://www.clip2.com/GnutellaProtocol04.pdf   
[3] A. Back, I. Goldberg, and A. Shostack, "Freedom Systems 2.1 Security Issues and Analysis", Zero Knowledge Systems, Inc. White Paper, 2001.   
[4] L. Breslau, P. Cao, L. Fan, G. Phillips, and S. Shenker, "Web Caching and Zipf-like Distributions: Evidence and Implications", in Proceedings of IEEE INFOCOM, 1999.   
[5] Y. Chawathe, S. Ratnasamy, L. Breslau, N. Lanham, and S. Shenker, "Making Gnutella-like P2P Systems Scalable", in Proceedings of ACM SIGCOMM, 2003.   
[6] M. Freedman and R. Morris, "Tarzan: A Peer-to-Peer Anonymizing Network Layer", in Proceedings of the 9th ACM Conference on Computer and Communications Security (CCS), 2002.   
[7] T. Hobfeld, A. Mader, K. Tutschku, F. Andersen, C. Kappler, H. d. Meer, I. Dedinski, and J. Oberender, "An Architecture Concept for Mobile P2P File Sharing Ser-

vices", in Proceedings of Workshop of Information 2004 - Algorithms and Protocols for Efficient Peer-to-Peer Applications, 2004.   
[8] H. Krawczyk, "Distributed Fingerprints and Secure Information Dispersal", in Proceedings of the 12th annual ACM symposium on Principles of distributed computing, 1993.   
[9] H. Krawczyk, "Secret sharing made short", in Proceedings of the 13th annual of International cryptology conference on Advances in cryptology, 1994.   
[10] K. Kurosawa and T. Takagi, "Some RSA-Based Encryption Schemes with Tight Security Reduction", ASIA-CRYPT, 2003.   
[11] Y. Liu, X. Liu, L. Xiao, L. M. Ni, and X. Zhang, "Location-Aware Topology Matching in Unstructured P2P Systems", in Proceedings of IEEE INFOCOM, 2004.   
[12] R. J. McEliece and D. V. Sarwate, "On sharing secrets and Reed-Solomon codes", Communications of the ACM, 1981.   
[13] M. O. Rabin, "Efficient dispersal of information for security, load balancing, and fault tolerance", ACM JACM, 1989.   
[14] M. K. Reiter and A. D. Rubin, "Crowds: Anonymity for Web Transactions", ACM Transactions on Information and System Security, 1998.   
[15] Rennhard and B. Plattner, "Introducing MorphMix: peer-to-peer based anonymous Internet usage with collusion detection", in Proceedings of ACM workshop on Privacy in the Electronic Society, 2002.   
[16] V. Scarlata, B. N. Levine, and C. Shields, "Responder Anonymity and Anonymous Peer-to-Peer File Sharing", in Proceedings of the 9th International Conference of Network Protocol (ICNP), 2001.   
[17] A. Shamir, "How to share a secret", Communications of the ACM, 1979.   
[18] R. Sherwood, B. Bhattacharjee, and A. Srinivasan, "P5: A Protocol for Scalable Anonymous Communication", in Proceedings of IEEE Symposium on Security and Privacy, 2002.   
[19] C. Shields and B. N. Levine, "A Protocol for Anonymous Communication over the Internet", in Proceedings of 7th ACM Conference on Computer and Communication Security (ACM CCS), 2000.   
[20] P. F. Syverson, D. M. Goldschlag, and M. G. Reed, "Anonymous Connections and Onion Routing", in Proceedings of IEEE Symposium on Security and Privacy, 1997.   
[21] M. Wright, M. Adler, B. N. Levine, and C. Shields, "An analysis of the degradation of anonymous protocols." in Proceedings of the 9th annual of Symposium of Network and Distributed System Security, 2002.   
[22] L. Xiao, Z. Xu, and X. Zhang, "Low-cost and Reliable Mutual Anonymity Protocols in Peer-to-Peer Networks", IEEE Transactions on Parallel and Distributed Systems, 2003.   
[23] G. Zacharia and P. Maes, "Collaborative Reputation Mechanisms in Electronic Marketplaces", in Proceedings of 32nd Hawaii International Conference on System Sciences, Hawaii, 1999.