# Rumor Riding: Anonymizing Unstructured Peer-to-Peer Systems

Yunhao Liu, Senior Member, IEEE, Jinsong Han, Member, IEEE, and Jilong Wang, Member, IEEE

Abstract—Although anonymizing Peer-to-Peer (P2P) systems often incurs extra traffic costs, many systems try to mask the identities of their users for privacy considerations. Existing anonymity approaches are mainly path-based: peers have to pre-construct an anonymous path before transmission. The overhead of maintaining and updating such paths is significantly high. We propose Rumor Riding (RR), a lightweight and non-path-based mutual anonymity protocol for decentralized P2P systems. Employing a random walk mechanism, RR takes advantage of lower overhead by mainly using the symmetric cryptographic algorithm. We conduct comprehensive trace-driven simulations to evaluate the effectiveness and efficiency of this design, and compare it with previous approaches. We also introduce some early experiences on RR implementations.

Index Terms—Mutual anonymity, non-path-based, random walk, peer-to-peer.

# 1 INTRODUCTION

PEER-TO-PEER (P2P) networks, such as Napster, Gnutella, and BitTorrent, have become essential media for information dissemination and sharing over the Internet. Concerns about privacy, however, have grown with the rapid development of P2P systems. In distributed and decentralized P2P environments, the individual users cannot rely on a trusted and centralized authority, for example, a Certificate Authority (CA) center, for protecting their privacy. Without such trustworthy entities, the P2P users have to hide their identities and behaviors by themselves. Hence, the requirement for anonymity has become increasingly critical for both content requesters and providers.

A number of methods [1], [2], [3], [4] have been proposed to provide anonymity. Most, if not all, of them achieve anonymous message delivery via nontraceable paths comprised of multiple proxies or middle agent peers. Those approaches, also known as path-based approaches, require users to setup anonymous paths before transmission. In most cases, the path is a layer-encrypted data structure. Although path-based protocols provide strong anonymity, an anonymous path has to be preconstructed, which requires the initiator to collect a large number of IP addresses and public keys. Also, an initiator has to perform asymmetric key based cryptographic encryptions, for example RSA [5], when wrapping the layer-encrypted packets. Both the peer collection and content encryption introduce high costs. Practically, users often expect to establish a long anonymous path and update the path periodically to defend against the analysis from attackers [6]. In highly dynamic P2P systems, when a chosen peer leaves, the whole path fails. Unfortunately, such a failure is often difficult to be known by the initiator. Therefore, a “blindly-assigned” path is very unreliable, and users have to frequently probe the path and retransmit messages.

To address the above issues, we propose a non-path-based anonymous P2P protocol called Rumor Riding (RR). In RR, we first let an initiator encrypt the query message with a symmetric key, and then send the key and the cipher text to different neighbors. The key and the cipher texts take random walks separately in the system, where each walk is called a rumor. Once a key rumor and a cipher rumor meet at some peer, the peer is able to recover the original query message and act as an agent to issue the query for the initiator. We call the agent peer as a sower in this paper. The similar idea is also employed during the query response, confirm, and file delivery processes. Thus, the rumors serve as the primitives of this protocol to achieve mutual anonymity and meet the design objectives.

In RR, anonymous paths are automatically constructed via the rumors’ random walks. Neither the initiator nor the responder needs to be concerned with path construction and maintenance. Extending the scope of anonymous servents from a small clique of nodes to the entire P2P network, RR significantly increases the anonymity degree of a system.

RR employs a symmetric cryptographic algorithm to achieve anonymity, which significantly reduces the cryptographic overhead for the initiator, the responder, and the middle nodes. In addition, as initiating peers have no requirement on extra information for constructing paths, the risk of information leakage, caused by links that are used for peers to request the IP addresses of anonymous proxies, is eliminated.

The rest of this paper is structured as follows: In Section 2, we describe the related work on anonymous communications. In Section 3, we present the design of the RR protocol. Section 4 discusses the key issues and the anonymity degree of RR. Section 5 presents simulation results and performance evaluations. We conclude the work in Section 6.

. Y. Liu is with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, and also the Tsinghua National Lab for Information Science and Technology. E-mail: yunhao@greenorbs.com.   
. J. Han is with the School of Electronic and Information Engineering, Xi’an Jiaotong University, Xi’an, Shaanxi, China. E-mail: hjs.jason@mail.xjtu.edu.cn.   
. J. Wang is with the Network Research Center, Tsinghua University, Room 3-221, FIT Building, Beijing 100084, P.R. China.

Manuscript received 8 Jan. 2009; revised 25 Aug. 2009; accepted 29 Sept. 2009; published online 30 Apr. 2010.

Recommended for acceptance by A. Boukerche. For information on obtaining reprints of this article, please send e-mail to: tpds@computer.org, and reference IEEECS Log Number TPDS-2009-01-0007. Digital Object Identifier no. 10.1109/TPDS.2010.98.

# 2 RELATED WORK

Since Chaum [4] pioneered the concept of anonymity, many approaches have been proposed to support anonymous communications. The approaches fall into two categories: path-based anonymous delivery and anonymous multicast.

Onion Routing [7], as well as its second generation, Tor [8], are the most popular path-based protocols providing initiator anonymity based on a layered-encryption method. They mainly focus on the IP layer rather than the application level. APFS [9] adopts the initiator anonymous protocols like Onion Routing to provide responder anonymity in P2P systems. Shortcut Protocol [2] provides P2P mutual anonymity with a reduced response delay. Crowds [1] introduces a random forwarding mechanism to intermediate nodes. When receiving a packet, a peer has two options: forwarding the packet to a randomly chosen peer or directly sending it to the destination peer.

$\mathrm { P ^ { 5 } }$ [3] is based on the anonymous multicast. To make the broadcasting scalable, $\mathrm { P ^ { 5 } }$ employs a virtual tree to construct anonymous broadcasting groups. $\mathrm { P ^ { 5 } }$ also utilizes a noise mechanism, which enables peers within a group to send packets at a fixed rate for concealing the initiator’s ID. Anonymous multicast-based approaches, however, are not suitable for P2P systems as the initiator has to know the destination node’s ID.

Since random walk is the building block of our protocol design, we provide a brief overview of random walk approaches. Lv et al. [10] propose a multiple random walk based query algorithm to replace the flooding method for reducing the network traffic in Gnutella-like systems. In [11], Adamic et al. propose an algorithm, which works well in power-law graphs. The work attempts to make the search scalable and reduce the network traffic. Gkantsidis et al. [12] study the properties of random walk in depth via statistical methods and reveal some factors for improving the system performance. Bisnik et al. [13] provide a mathematical model to analyze the performance of random walk, and develop an adaptive algorithm to reduce the search overhead. Bhattacharjee et al. present a random based search protocol for unstructured P2P systems [14]. Sybilguard [15] employs random routes in a social network trust topology to defend against sybil attacks. All of these prior studies strongly support the workability and efficiency of random walk in P2P systems.

# 3 RUMOR RIDING

Rumor Riding (RR) includes five major components: Rumor Generation and Recovery, Query Issuance, Query Response, Query Confirm, and File Delivery.

# 3.1 Rumor Generation and Recovery

RR employs the AES algorithm [16] to encrypt original messages. The key size is 128-bit. To determine whether a pair of cipher and key rumors hit, we employ a Cyclic Redundancy Check (CRC) function to attach a CRC value, CRC(M), to the message M. For received key rumors and cipher rumors, the sower S uses AES to recover a message ${ \bar { M ^ { \prime } } }$ and the checksum CRCðM0 Þ. It then performs the CRC function to the recovered M’ and compares the result with CRCðM0 Þ. If they match, the sower $S$ is aware that it has successfully recovered a message M. The purpose of the CRC function is to avoid using a complex text understanding technique to distinguish a meaningful M.

![](images/b8a4a5598518fd0416ccc626a921af4148401a84f642f8d73ae7e5031329456b.jpg)



Fig. 1. Query issuance.

# 3.2 Query Issuance

When an initiator I wishes to issue an anonymous query, it first generates the query content $q ,$ and a public key $K _ { I } ^ { + }$ . Node I then uses an AES cryptographic algorithm to encrypt q into a cipher text C with a symmetric key K. It organizes the key $\mathbf { \bar { \Sigma } } _ { K }$ and the cipher text $C$ into two query rumors, $q _ { K }$ and $q _ { C }$ . In Gnutella, each packet is labeled with a Descriptor ID, a string that uniquely identifies the packet. RR also uses the descriptors to identify rumors. Thus, two random number strings, $I D q _ { K }$ and $I D q _ { C } ,$ are used to label the two rumors. After generation, I forwards the rumor messages to two randomly chosen neighbors, as illustrated by the dashed and dotted lines in Fig. 1. The query cipher rumor and the query key rumor then start their random walks.

The strategy of processing rumors is different from that of processing normal queries. RR requires every node to temporarily keep a local cache to store the received rumors. When a node receives a query key rumor, it performs the rumor recovery procedure to check all cached cipher rumors. If a decrypted rumor holds a plaintext matching the CRC value, $q$ will be successfully recovered. Whatever there is a match or not, this intermediate node reduces the TTL value of the received rumor by one, keeps a temporary record containing the ID of the rumor in the local cache, and forwards it to a randomly chosen neighbor. The procedure continues until the TTL value of this rumor is reduced to zero. For the received query cipher rumor, the process is similar. Therefore, if a pair of query rumors reach a certain node, no matter what the sequence is, this node will eventually recover the original $q .$ The key issue with this procedure is that the number of rumors and their initial TTL values need to be carefully selected so that at least one pair of rumors, including a key and a cipher, will meet. On the other hand, local adversaries may eavesdrop on the traffic and launch traffic analysis attack to locate the initiator’s identity. In the Gnutella protocol, the traveling length of a query message is limited by two unsigned fields: TTL and Hops. When issuing plaintext query, an initiator sets a positive number in TTL, and zero in Hops. The query is passed from one servent to another, and each servent decreases the TTL by one and increases Hops by one before sending the message to the next servent. Thus, if an adversary receives a message with a Hops set as zero, it knows that the node sent the message is the initiator. To avoid this, RR initializes a nonzero positive number $w ( 1 <$ < w < 127Þ in the Hops fields of rumors before sending them out. Normally, a small number between $7$ and 10 would be sufficient to confuse the adversaries. Suppose the expected length of rumors’ walking is $L ,$ the TTL value should be $L + w$ . We present the determination of L in Section $3 . 7$ and detailed discussion on the parameter settings in Section 4.

![](images/9040d0970a0e046b8a97d001f4de7f7ae1b6598a4288249b3a6ba384b9bbec7c.jpg)



Fig. 2. Query response.

If one intermediate node that recovers q is willing to act as an agent peer, it conducts a search on behalf of the unknown I. We call this agent node a sower. When a peer identifies itself as a sower, it proceeds as follows: First, it checks the TTL values defined in the rumors. If they are not zero, the sower forwards the rumors out, so that if there are attackers who can overhear some of the messages sent to the sower, it is still not trivial to determine whether or not the peer is a sower. Second, the sower, $S _ { a } ,$ , as illustrated in Fig. 1, attaches the original query message $q$ with its IP address, and then issues the query marked with a label $I D _ { q }$ in a plaintext $( I D _ { q }$ is also used for $S _ { a }$ to locate the correlated $q _ { K }$ and $q _ { C } )$ . In this operation, we avoid a blind flooding. Instead, we employ a probability-basedflooding, in which the sower selects a subset of its neighbors and issues the query. Note that the sower does not send the query to the nodes which sent or have been sent the two rumors of this query. Such a selective flooding is effective on defending against collaborating attacks, on which we have more discussions in Section 4.2. For the neighboring nodes that do not send or have not been sent the two rumors, the sower sends the plaintext query to each of those nodes with a probability $p .$ The $p$ is like a threshold. The sower can first compute a random value between [0, 1], and then compare to the $p .$ If the value is less than $p ,$ the sower sends the query, otherwise does not send. Upon receiving the query, the neighboring nodes forward the query to each of its neighbors (expect the sower) with the probability $p .$ Such a procedure continues until the query packet exhausts its TTL. The selective flooding has a constrained flooding scope compared to the the blind flooding, which can reduce the redundant traffic caused by multiple sowers’ flooding. The probability p is a systematic parameter. We examine the proper setting of $p$ through our simulation. In later discussions, we use the $l q _ { K }$ and $l q _ { C }$ to denote rumor paths from I to $S _ { a }$ .

![](images/1e92ac90988a4568f2168b0074d72f4f171eac8383b716a226905662c7a2583e.jpg)



Fig. 3. Query confirm.

# 3.3 Query Response

When a receiving node the query has a copy of the desired file, it becomes a responder R. To respond to the query, R encrypts the plain text of the response message $r ,$ using the initiator’s public key $K _ { I } ^ { + }$ . It encrypts $< ( r ) _ { K _ { r } ^ { + } } , \bar { I } D _ { q } , \mathrm { I P } _ { S _ { a } } , \bar { K } _ { R } ^ { + } >$ using $\mathrm { A E S } ,$ where $\dot { K } _ { R } ^ { + }$ Iis the public key generated by $R ,$ and encloses the cipher text and the key into two response rumors, $r _ { K }$ and $r _ { C }$ . They are then assigned with $I D r _ { K }$ and $I D r _ { C } ,$ , respectively.

After being sent out from $R ,$ two rumors start their random walks in the system. We illustrate the procedure in Fig. 2. RR guarantees that at least one pair of rumors meet at a certain peer $S _ { b } .$ We use $l r _ { K }$ and $l r _ { C }$ to denote their paths from R to $S _ { b }$ . Sb decrypts the cipher text in $r _ { C }$ with the key in $r _ { K } ,$ , and recovers the IP address of sower $S _ { a }$ .

If $S _ { b }$ volunteers to forward the response for $R ,$ it contacts $S _ { a }$ via a TCP connection, and forwards these two response rumors to $S _ { a }$ . Note that $S _ { b }$ also attaches its IP address, $I D q ,$ , $I D r _ { K } ,$ and $I D r _ { C }$ to the two rumors. When $S _ { a }$ receives the responses $r _ { K }$ and $r _ { C } ,$ it delivers them to the originating peers of $q _ { K }$ and $q _ { C } .$ Two response rumors are marked with $I D q _ { K }$ and $I D q _ { C } ,$ , to help them walk along the reversed paths of $l q _ { K }$ and $l q _ { C } .$ . The successor nodes continue this procedure. Thus, two response rumors make use of $l q _ { K }$ and $l q _ { C }$ to reach I.

Having two response rumors, I recovers $( r ) _ { K _ { I } ^ { + } }$ from $r _ { K }$ and $r _ { C } ,$ and then decrypts $( r ) _ { K _ { I } ^ { + } }$ to recover the original response message $^ { r , }$ using its private key $K _ { I } ^ { - }$ . A flooding search procedure may raise multiple responses. To simplify the demonstration, we assume that I only selects one candidate as the provider. Without loss of generality, we continue using R to denote the selected provider.

# 3.4 Query Confirm

In the query confirm phase, I uses the responder’s public key to encrypt the confirm message c. It then encrypts $< ( c ) _ { K _ { o } ^ { + } } , I D r _ { K } , I D r _ { C } , { \mathrm { I P } _ { S _ { b } } > }$ and obtains two confirm rumors, $c _ { K }$ and $c _ { C } ,$ which take random walks in the system. Note that two confirm rumors are marked with new descriptors: $I D c _ { K }$ and $I D c _ { C }$ . We assume that $c _ { K }$ and $c _ { C }$ collide in a new sower $S _ { a } ^ { \prime } .$ . We denote their paths from I to $S _ { a } ^ { \prime }$ by $l _ { c _ { K } }$ and ${ l } _ { c _ { C } } .$ . When $S _ { a } ^ { \prime }$ recovers the IP address of $S _ { b }$ from $c _ { K }$ and $c _ { C , }$ , it directly contacts $S _ { b }$ to forward $c _ { K }$ and $c _ { C }$ attached with $I D r _ { K }$ and $I D r _ { C }$ via a TCP link, as shown in Fig. 3. The $c _ { K }$ and $c _ { C }$ are then delivered along the reversed paths of $l r _ { K }$ and $l r _ { C }$ until they reach R.

# 3.5 File Delivery

After recovering the confirm message from (c) $K _ { R } ^ { + } ,$ using its private key $K _ { R } ^ { - } ,$ R employs a digital envelope technique to encrypt the file into cipher $C _ { F }$ . Instead of including $C _ { F }$ into the rumor generation, R encrypts $< I D c _ { K } , I D c _ { C } , \mathrm { I P } _ { S _ { a } ^ { \prime } } >$ to generate the data cipher rumor and the data key rumor, and attaches the digital envelop payload to the data cipher rumor. The large data cipher rumor and the small data key rumor first take random walks to meet each other at a sower $S _ { b } ^ { \prime } ,$ then traverse the path from $S _ { b } ^ { \prime }$ to $S _ { a } ^ { \prime }$ via a TCP connection, and eventually reach I along the reversed paths of $l _ { c _ { K } }$ and ${ l } _ { c _ { C } } .$ Upon receiving the digital envelop, I recovers the desired file using its private key. For large-size files, responders can split them into multiple segments.

# 3.6 Multiple Rumor Riding

Previous designs employ multiple walkers, say k-walkers, to shorten the query delay. After L hops, k-walkers should cover approximately the same amount of peers as a onewalker covers after $k \times L$ hops, while the response time can be significantly reduced. To accelerate the query cycle, in RR, an initiator can issue multiple rumors in the query cycle. We denote this scheme as (i, j)-RR, which issues i cipher rumors and j key rumors. Another advantage of the use of multiple rumors is that RR can be more reliable as more sowers can serve the query.

# 3.7 Rumor TTL

The selection of rumor TTL, together with the number of cipher and key rumors, determines 1) how many sowers a query will have, and 2) how the sowers are distributed. The tradeoff is that for each query, RR requires a number of sowers randomly distributed in the entire system, but too many sowers will lead to unacceptable overhead. In order to guarantee the diversity of the sowers, a simple and lightweight method is needed for estimating Oðlog nÞ, where n is the size of the P2P overlay. Also, to reduce the unnecessary overhead, peers need to observe the diversity of sampling sowers to adjust the TTL value of rumors. The adaptive TTL determination of RR comprises two phases: (a) setting initial TTL value, and (b) adaptively adjusting TTL.

In phase (a), during the P2P Bootstrapping process, each fresh peer retrieves a list of neighbors from the bootstrapping server. The fresh node can set the mean value of those in the responses as its initial TTL value of rumors.

In phase (b), RR employs random walk based schemes similar to the ones used in [15]. A peer can periodically insert several pairs of “sampling” rumors into the network. Those rumors are set with the peer’s current TTL setting and its IP address. The initiator sets a timer for each rumor. Any sower of such a pair of sampling rumors records the retained TTL of two rumors and then directly sends the TTL information as well as a timestamp to the initiator through a TCP connection. During the process, we do not need to consider the anonymity. The initiator observes the ID (IP address) of the responding sower and the distribution of the reported TTL. Also, the mechanism facilitates to balance the tradeoff between the length of anonymous paths and the latencies of query, response, or file delivery by adaptively tuning the setting of TTL. For example, the initiator can leverage a long TTL to increase the probability of collision, while increasing the number of rumors for reducing the latency. Utilizing this mechanism, an initiator can also adaptively tune the settings of TTL value of rumors L or the number of rumors k to increase the diversity of anonymous paths. Increasing the diversity of sower distribution can increase the probability that RR generates more disjointed anonymous paths between the initiator and sowers, and hence creates more different paths between the initiator and the responder.

# 3.8 Rumor Cache

In RR, each peer needs to cache a number of received rumors before the rumors are matched, which raises a concern of the storage overhead. RR does not incur much storage overhead to individual peers. The storage overhead is highly related to the speed of query generation. In P2P systems, the speed of query generation is relatively low, e.g., each peer normally issues no more than 0.3 queries per minute on average [17]. Therefore, the storage overhead for each peer is relatively small in general, which is acceptable to current PCs. We will further discuss the storage overhead in Section $5 ,$ based on our simulation and preliminary implementation. In addition, we propose a FIFO based rumor removal mechanism for handling the cache overflow. More details of this mechanism can be found in [18].

# 4 DISCUSSION

We now examine several key issues in the RR design. We first focus on how to ensure that each query has at the least one sower and that the sowers are evenly distributed over the system. We then discuss the attack models and analyze the anonymity degree of RR.

# 4.1 Sower Distribution and Collision Rate

In RR, we select the random walk as the rumor spreading method. P2P systems mainly utilize three communication patterns to deliver messages: flooding [19], random walk, and end-to-end delivery. Some existing works, for example $\mathrm { P ^ { 5 } }$ , employ the flooding pattern, which is not suitable for P2P systems due to the huge traffic overhead. The end-toend delivery, which is used by the path-based approaches, however, may compromise the anonymity of the initiator or responder, as the destinations of the delivered messages have to be known in advance. As we discussed in the Section 1, path-based model also suffers from the unreliability of fixed paths and high computation overhead caused by layered encrypted encapsulation. Based on these observations, we select random walk as the fundamental anonymizing method. The distinct features of random walk mechanism are as follows: First, random walk mechanism introduces randomness to the message delivery such that the difficulty for attackers to trace back to the initiator or responder is increased. Second, this mechanism potentially involves all peers in the anonymizing process, so that the anonymous proxy set is extended from a small group in path-based approaches to the entire P2P network.

Specifically, RR rumors are sent in random directions, and each peer forwards a rumor to one of its neighbors without any bias. According to the observations in [13], random walk achieves statistical properties similar to independent sampling for reasonable networks, for example the small world [20] or power law networks [13], [21]. Studies in [14], [22] show that if the walk length is sufficiently large, the final receivers of a random walk query are randomly distributed. We define collision distance, $H _ { c d } ,$ as the number of hops along the shortest path that rumors walk from the initiator to the sower in a query. When taking the $H _ { c d }$ to be $O ( \log n )$ , the sowers are evenly distributed, guaranteed by the observations in [14]. Our simulation results in Section 5 show that carefully selecting parameters will lead to desired collision distances.

![](images/d97b325396cd9d0cb1f8961ce1d0b120e1966035b2bcd6a85b9721ddd7f6c8d2.jpg)



Fig. 4. Collision rate in ðk; kÞ-RR.

We assume that each peer accessed by a rumor is an independent sample from a space of uniform distribution. A peer becomes a sower if it receives a pair of rumors. For a $\mathsf { \Gamma } ( i , j ) \mathsf { - R R }$ scheme, there are i cipher rumors and j key rumors. Without loss of generality, we assume that each rumor has a fixed TTL value of L. After rumor spreading, the popularity of cipher rumors is $i \times L ,$ where the popularity means the total number of peers receiving the cipher rumor. We further assume that those nodes are distinct with each other and the distribution is uniformly random. On the key rumor path, the probability of a peer only being visited by this key rumor and not having the cipher rumor is $( 1 { \dot { - } } i \times L / { \dot { n } } )$ . The probability of a key rumor terminating its walk without hitting a cipher rumor is given by $( 1 - i \times L / n ) ^ { L }$ . Thus, the probability of a successful collision in a $( i , j ) – \mathrm { R R }$ is given by:

$$
p _ {h} = 1 - (1 - i \times L / n) ^ {j \times L}. \tag {1}
$$

We also introduce a parameter - to indicate the acceptable collision rate. The expected collision rate is formulated subject to the constraint: $p _ { h } \ge 1 - \tau , 0 < \tau \ll 1$ . Combining this with (1) we have

$$
j \times L \times \log (1 - i \times L / n) \geq \log (\tau). \tag {2}
$$

To keep the collision rate $p _ { h }$ at a high level, say 99 percent, peers can choose the proper $i , j ,$ and L according to (1) and (2). We calculate three typical distributions in (1, 1), (1, k), and $( k , \ k ) – \mathrm { R R }$ schemes to examine the optimal setting of i and j. Based on (2), we can investigate the optimal theoretical distribution of $p _ { h }$ . Indeed, the $( k , k ) – \mathrm { R R }$ scheme achieves a higher collision rate than others in most cases. Thus, we assert that the (k, k)-RR scheme is a proper choice for a high collision rate. We simulate the $p _ { h }$ of $\mathsf { \bar { ( } } k , \bar { k } ) \mathsf { { - } } \mathsf { R } \mathsf { R }$ with a $1 0 ^ { 6 }$ node network and plot the results in Fig. 4. We see that a larger TTL value of rumors corresponds to a higher collision rate, while increasing the number of rumors also leads to a higher collision rate. On the other hand, a higher collision rate often yields more overhead due to the larger k and L. We also investigate the lower bounds of $k \times L$ settings, which guarantee the different collision rates. With enlarging the size of P2P networks, the lower bounds increase as well. Fig. 5 plots lower bounds of $k \times L$ as the function of network size under different $p _ { h }$ requirements. The results show that in a million-node network, if ph closely approaches 1, adopting a setting of $k \times L$ near 3,000 yields a 99.99 percent probability of a pair of rumors colliding with each other. If we slightly reduce the collision rate from 99.99 percent to 90 percent, the least needed $k \times L$ dramatically decreases below 1,500. It is worth noticing that adopting appropriate $p _ { h } ,$ say 90 percent, for rumors’ collision while needs a small $k \times L ,$ , would benefit the RR performance from saving a significant amount of traffic.

![](images/f1f96a1d9cf2f32fd93d54da8d9434e5e3a9742a6c3ceb9e63d4e9562182b860.jpg)



Fig. 5. Collision rate under different $k \times L .$ .

As we mentioned, the collision distance is another important factor balancing the tradeoff between the user anonymity and the query delay. Initiators hope that the sower peers reside as far away as possible, since the sowers recover the query messages and might help adversaries to locate the initiator if they are compromised. Thus, the number of rumors needs to be limited as well. We show our simulation results for the rumor settings in a practical network in Section 5.

# 4.2 Anonymity Analysis

In this section, we first discuss the degree of anonymity that RR achieves, and then analyze the protocol effectiveness under various attack scenarios.

# 4.2.1 Anonymity Model

There are two main categories of anonymity models for defining the anonymity degree. The models in the first category define the anonymity of a certain node as the number of peers that have an equiprobable chance of being the given node, which is termed as anonymity set. The second category employs measurements based on information theory, for example the mutual information [23], to reflect the similarity between two entities, such as the input/output links or real/suspected participants. The anonymity set used by the first category is widely adopted due to its capability of capturing the common features of anonymity. The second model focuses on the information leakage in anonymous systems. The typical usage of the model is to analyze the anonymity in so called covert channels. We adopt the first anonymity model and define the Anonymity Degree (AD) as the probability of making an incorrect guess to identify a participant. A higher degree infers that better anonymity has been achieved.

In RR, when an intermediate node receives a query or confirm rumor, it forwards the rumor to a randomly chosen neighbor. From an observer’s perspective, any rumor sending node might be the actual initiator of the rumor. Similarly, when an intermediate node receives a response or data rumor, any intermediate node delivering the rumor could be a potential receiver. Therefore, an individual observer (initiator, responder or an intermediate node) cannot distinguish the initiator and responder from the other peers. Thus, if the number of nodes in the P2P system is n, the initiator’s or responder’s AD is $( n - 2 ) / ( n - 1 )$ from the viewpoint of a normal observer (the number of potential initiators/responders is n - 1).

# 4.2.2 Attacks

We assume that the number of adversary nodes is $m ,$ so the probability of a peer being an adversary is $m / n$ . In some cases, adversaries may merely observe the fact that a peer is sending information, without any knowledge about the transmitted data. We claim that the protocol achieves unlinkability to the initiator and responder, if they cannot be identified when communicating with each other. In our attack model, we assume that, based on the records, the adversary nodes are able to observe and store the communication traversing them and guess the identity of nodes that initiated those transmissions. Adversaries also have the capability to perform active attacks which include dropping, hijacking, and forging packets, controlling flows and connections of the network, etc. We categorize the major attacks that threaten a P2P anonymity protocol, and briefly discuss why RR is invulnerable, while leave a full discussion in our technical report [18].

Collaborating attack. Neighboring adversaries may collaborate to monitor the traffic passing through and share the information in order to identify the possible neighboring initiators. When two adversaries neighboring the initiator receive a pair of rumors of a message, one of them may forward the key rumor to another. The latter will recover the message, and guess that the node sending the rumor is the initiator.

In RR, a sower selects a subset of its neighbors to send the plaintext query, and the two collaborating nodes will not receive the query. Fig. 6 illustrates the selective flooding of RR. In this way, adversaries only bet that the monitored node is an initiator or a responder. Thus, the AD of the initiator or responder becomes $1 - 1 / ( 1 + s )$ , where s is the number of sowers of this pair of rumors. Suppose an initiator is neighboring c local collaborating nodes. If c exceeds 2, then the AD becomes $1 - 1 / ( 1 + s \times ( 1 - p ) ^ { ( c - 2 ) } )$ , where p is the probability of a sower choosing a neighbor to send the query. Hence, RR is not subject to the local collaborating attack, if the adversaries cannot compromise more than three neighbors of the monitored node. For the nonlocal collaborating attack, we discuss the defense together with the traceback attack later.

![](images/7d41601ce69e26108b1a936a87122f775f9de553607413bdc2cb3ccc3ece6191.jpg)



![](images/b1f60934849eeb9b030641f1bb6688c6ac0200564a6668f149525c729dbf4742.jpg)



Fig. 6. Collaborating attack versus RR. (a) Collaborating attack. (b) Selective flooding of sowers.

Timing attack. In a timing attack [24], the adversary deduces the correlation among the timings of packets, such as the response time of a query, the time difference of a query, the time interval between two sequential packets, etc., to locate a transmission. Timing attacks pose a serious threat to path-based approaches. RR is invulnerable in that 1) rumors are delivered over the overlay network in a random walk manner, and RTT measurements do not reveal the real distance to the responder; 2) if adversaries want to trace the rumor via the time difference to locate the responder, they need to trace one query rumor from the initiator to a sower, then trace the plaintext query message from the sower to the responder, which is not trivial; and 3) a sower issues a request only after it obtains a pair of query rumors, so the response time is mainly dependent on the random walks of rumors, which are unpredictable. All of these factors make it difficult to launch a timing attack.

Predecessor attack. In some anonymous systems, an initiator repeatedly communicates to a specific responder in many rounds. In [25], Wright et al. elaborate the predecessor attack, where the adversary can control a subset of the nodes in anonymous systems and passively log the possible communications between the initiator and responder. In RR, rumors walk randomly and interact with random sowers. The sowers of a given initiator or responder are unpredictable and randomly distributed over the system. Hence, adversaries are not able to perform such an attack to identify the initiator or responder via sowers, and RR is not subject to this type of attack.

Traffic analysis attack. An adversary can extract traffic flow information such as packet count, message volume, and communication pattern, etc., and build correlations between the initiator, responder, and their communication [26]. Similar to timing attacks, traffic analysis attacks can compromise the initiator’s or responder’s anonymity, if adversaries control a large fraction of the network. For example, based on traffic shaping [27], adversaries clog traffic in the suspected nodes and observe the traffic change when they slightly mitigate the clogging traffic. Thus, the real traffic can be deduced. Performing this attack consequentially along the reversed path of the traffic, adversaries can easily determine the initiator. RR is much less vulnerable to this attack since subsequent messages do not belong to the same traffic, and there are not any continuous paths in RR.

Traceback attack. Adversaries start from a known sower to trace back to the initiator along the rumor paths. The adversary examines the stored routing state of the peers to identify the paths between the initiator and responder. We consider the users’ anonymity in two attack scenarios: 1) One-way back tracking: adversaries that are on the rumor path back-track and collaborate with each other to detect the source node of this rumor; 2) Multiple-ways back tracking: at least one adversary intercepts both the cipher rumor and the key rumor. When there are no global adversaries or active tracebacks, RR achieves a high degree of anonymity under traceback attacks.

# 5 EXPERIMENTS

Additional latency of data delivery, bandwidth consumed by anonymous traffic, and crypto processing, if they exist, are necessary in order to provide anonymity. In this section, we evaluate the RR design through trace-driven simulations and some implementations.

# 5.1 Metrics

We use the following metrics for evaluating RR:

Collision rate. To verify the theoretical results in Section 4, we examine the distribution of collision rate with real traces. Besides the verification, we also use the results to guide the selection of rumor parameters.

Collision distance. A longer collision distance often means a higher anonymity level, but also increases the delay of a query as well as the traffic overhead. On the other hand, the collision distance must be sufficiently large to guarantee sower diversity, as we discussed in Section 4.

Sower diversity. The metric reflects the distribution of sower locations in the P2P systems. Evenly random distribution of sower location leads to a higher anonymity degree.

Number of sowers. Since each sower implements a selective flooding search for an initiator, too many sowers will incur a large number of replicated query messages, and too few sowers will result in failure on providing enough redundancy and reliability.

Traffic overhead. The amount of traffic overhead represents the comprehensive latency in data delivery and bandwidth. We assume that a query cycle involves e edges in the P2P overlay. For each edge in the P2P overlay, there is a unique path mapped into the physical internet layer with the length l. For each message enrolled in one query cycle, we calculate the sum of the distances that this message passes through. Therefore, the traffic overhead of a query cycle is defined as $\begin{array} { r } { C = M \times L = \sum \left| m _ { i } \right| \times l _ { i } , 1 \leq \bar { i } \leq e , } \end{array}$ where $| m _ { i } |$ is the size of the traversed messages. Specifically, we are more interested in the extra traffic overhead caused by anonymous components. We define the extra traffic overhead as the total traffic overhead of a query cycle in an anonymized P2P system minus that of a query cycle in a nonanonymized P2P system.

Response time. In P2P systems, it is defined as the time elapsed from when a query is issued to when the first response arrives. In our simulation, the response time is defined as the time from the start of rumor spreading to the time when the initiator receives the first response message.

Crypto latency. The overhead incurred by the main cryptographic algorithms. We examine the cryptographic overhead incurred by RR compared with other anonymity protocols. We use the processing overhead in one AES operation as the basic unit to make conversions between RSA and AES. Thus we can investigate the cryptographic overhead incurred by different algorithms.

![](images/a91a3098172f37f9dc918876b6a12daab4e883e3920d3eca117710f4e191c93c.jpg)



Fig. 7. Theoretical collision rate.

# 5.2 Methodology

The P2P topologies come from two sources. One is based on the DSS Clip2 trace, which collected log data from January 2001 to June 2001. The other one is a more recent snapshot kit of Ion P2P [28], which logged data from September 2004 to February 2005, including topologies with high degree nodes (i.e., maintaining more than 30 neighbors). When adopting Ion’s traces into the simulated topologies, we only use the ultrapeers of its snapshots, which perform the flooding search in a hybrid Gnutella. To simulate the physical internet layer below the P2P overlay, we used BRITE [29] to generate 30,000 - 100,000 nodes in the internetlike topologies.

To perform the security algorithms used in RR protocol, we employ Crypto++ to perform the standard cryptographic functions. Our experiments for simulation and implementation are both conducted on several desktop PCs, typically with Pentium M 3.2G CPU, 1GBytes memory, 40G hard disk, and 10/100M Ethernet card. We also simulate the dynamic properties of the P2P overlay network by assigning a lifecycle to each peer. The lifetime is generated according to the distribution observed in [30]. The mean of the distribution is chosen to be 600 seconds [31], [32]. The value of each peer’s lifecycle is decreased by one with each passing second. When peers use up their lifetimes at the end of each second, they leave the system in the following second, and other fresh peers selected from the physical internet layer join in as replacements. In our simulation, we mainly compare RR with a typical Onion Routing approach, Shortcut protocol [2].

We first consider the collision rate of a single rumor spreading. To verify the theoretical results discussed in Section 4.1, we simulate rumor spreading procedures in the traces with a (k, k)-RR scheme. We experiment in the sample space of rumor numbers k 2 ½1::10 and path length L 2 ½1::256 (the default TTL value in Gnutella is 7). The average results of the collision rates are presented in Fig. 8. It is observed that the collision rates are usually higher than they are in the theoretical results, which are shown in Fig. 7. Since the topology in Gnutella networks follows smallworld properties, a random path in the P2P topology often traverses high-degree nodes, causing the collision rates to be higher than they are in homogeneous networks, in which the node degree follows a uniform distribution. For example, when $\mathrm { T T L } = 9 , k = 2$ , the theoretical result of collision rate is only 2.9 percent, but the simulation result is 15.1 percent. This phenomenon is particularly obvious in the dense topologies of the Ion’s traces. Combining the results of theoretical and real experiments, we suggest that the selection of the number of rumors k and the TTL value of each rumor L should follow $k \times L \geq 1 0 0$ .

![](images/9104d46ebf738e5e51bb79e4d97f9fd413900c2b71c26f2fbe3f4740f419f9c9.jpg)



Fig. 8. Collision rate of simulation.

As discussed in Section 4, the collision distance is important in balancing the tradeoff between user anonymity and the query delay in the RR design. In the results of the $( k , k ) – \mathrm { R R }$ scheme plotted in Fig. 9, it is shown that if L is larger than $2 5 ( 6 \leq k \leq 1 0 )$ , the average collision distance is no less than 5. On the other hand, a small $k ,$ say less than $6 ,$ guarantees that the most collision distance will be larger than 5. While k exceeds $^ { 6 , }$ the collision distance tends to be constrained within $2 \sim 5$ hops. Considering the fact that anonymity is more important than latency, we suggest that the number of rumors k should be kept to a maximum of 6.

Ideally, sowers should be uniformly distributed over the entire system so that for a given peer, distinct sowers are generated in different RR executions. Otherwise, since an initiator would have fixed sowers no matter how many rounds of RR it performs, attackers can easily perform the predecessor attack to locate it. We use the distinct sower ratio (D) to evaluate the diversity. If a peer performs g rounds of RR, and generates d distinct sowers $( d \leq g )$ , the distinct sower ratio of this peer is given by $D = ( d / g ) \times 1 0 0$ percent. By repeatedly running RR for each node in its lifecycle with the results obtained in the collision distance simulation, we see that when L is larger than 30 and the $k \in [ 1 . . 6 ]$ , the ratio D is larger than 92 percent. The results in Fig. 10 show that D increases rapidly when increasing the TTL of rumors. Therefore, selecting the constrains $L > 3 0$ and $1 \le k \le 6$ can effectively provide a safe collision distance and the random distribution of sowers.

![](images/e0a73ab09403a0a61b39b00a4395cdb9bf9083e4546791b202755972ddb49dc3.jpg)



Fig. 10. Sower diversity.

After selecting proper values of k and L for diversifying the sower locations, RR needs to provide the diversity of paths along which rumor messages probe. In this simulation, we examine the diversity of the distance that rumors walk from the initiator to the sower. The TTL value of rumors is constrained by $k \times L = 1 5 0$ in our experiments. Fig. 11 plots the frequency that the rumors appear in different distance bins in the setting of different $( k , k )$ RR. The distance of rumors travel before colliding is approximately ranging in a randomly uniform distribution in RR. Combining the sower diversity result, we can conclude the overall rumors achieve an approximate uniform distribution when the rumor TTL is following the above constraints.

In the meantime, RR needs to balance the tradeoff between the reliability and the overhead. Obviously, the reliability is first guaranteed by having at least one sower to serve each query. If too many sowers involve in the query issuance, the redundancy of sowers, however, may introduce large amount of overhead such that the P2P system is not scalable. We thus use the number of sowers to evaluate the reliability as well as the redundancy in order to guarantee the reliability while not incurring too many query messages. To this end, we investigate the distribution of the number of sowers under different RR settings. As shown in Fig. 12, when we select $k \times L \leq 2 0 0 ,$ each $( k , k ) – \mathrm { R R }$ scheme has no more than 10 sowers $( 1 \leq k \leq 6 )$ . Therefore, k  L should be in the range [100..200], which provides a range of the number of sowers [2..10], in order to meet both the reliability and the scalability requirements.

![](images/f64b6699863796495dbbeebdfc760b1802e0a82d737c99ffbcce6e76576ecbb3.jpg)



Fig. 9. Collision distance.

![](images/8c8bf3d548a1c93a27b9eb1b4ea7c6db6ca7ac4ad1b1c28a0855ccef989c292f.jpg)



Fig. 11. Rumor diversity.

![](images/c98a4aab7bef9621d2062de6ea701f9b5fc61b9c33bacde6681901ce48dd523f.jpg)



Fig. 12. Number of sowers.

We then consider the extra traffic. We compare RR with a typical Onion Routing based work, Shortcut protocol [2]. We insert 10,000 queries into the system, and Fig. 13 plots the cumulative distribution of the extra traffic overhead of (k, k)-RR schemes with $k \times L = 1 5 0 .$ . Note that a larger L means more traffic overhead. Traffic overhead is highly correlated with the length of packets. Using Onion Routing based approaches, the length of packets depends on the length of delivery path. In common, the onion packets are padded with some random bits for confusing the the traffic analysis attackers. A random bit string with a size of peeled off layer should be appended to the end of the onion packet at each hop. In this way, the onion packets are maintained with the same length along the entire path, which leads to large traffic overhead compared to RR. In contrast, the cipher rumor of RR only contains an encrypted cipher that has no need of wrapping or padding. Those features reduce the traffic cost of RR, especially for those cipher rumors, compared to the Shortcut. The key rumors, however, will incur extra traffic cost in P2P systems. In addition, the usage of multiple rumors also incurs traffic overhead. Therefore, RR does not perform better than Shortcut in terms of traffic cost in some cases. In Fig. 13, we observe that the average traffic overhead incurred by the Shortcut protocol is slightly less than that of the (6, 6)-RR scheme, which is the maximum value of our suggested settings. Except for this case, the traffic overhead of RR is much smaller than that of the Shortcut protocol.

Users of current P2P systems often have rigid requirements on the response time for requesting resources. We show the cumulative distribution curves of response times in different (k, k)-RR schemes in Fig. 14, comparing them with those of the Shortcut protocol. The major factor that helps RR to achieve a low latency is its small cryptographic processing overhead.

![](images/a25832c89b6ab73a8c243c3d791375ffb0c6c448893a28fd87d774f5a03a3c6a.jpg)



Fig. 14. Cumulative distribution of response time.

Shortcut employs Onion Routing to deliver the message. Using Onion Routing, the initiator (or the responder) has to encrypt the packet using the public keys of nodes on the path. The number of those asymmetric key based encryptions depends on the number of nodes on the delivery path of the packet. Each node on the path will decrypt the packet, using its private key. In contrast, RR utilizes the symmetric key based algorithm to perform encryptions (or decryptions), which significantly reduces the cryptographic processing overhead. This feature results in a low latency for RR. On the other hand, RR can adopt multiple pairs of rumors for accelerating each query cycle in P2P systems. In one query cycle, multiple rumors may revoke multiple sowers to flood the queries simultaneously. On the contrary, Shortcut merely has one anonymous agent to flood the query in one query cycle. The concurrent flooding of RR will effectively improve the search latency. Clearly, the average response latency is decreased when we increase the number of sowers. However, more rumors incur more traffic overhead and message replications.

We now examine the storage overhead caused by the cache mechanism of RR. Previous works [17] show that each node generates 0.3 queries per minute on average. We thereby set six query workloads as each peer issues 0.3, 1, 3, 10, 30, and 60 queries per minute. For each case, we sort all peers according to the amount of cache usage, and plot the cache usage of top 10,000 peers in Fig. 15. We also show the average cache usage in Fig. 16. We find that most of the peers only consume no more than 170 Kbyte of their caches under the test case of each node issuing 0.3 queries per minute, while the average cache usage is 24.9 Kbyte in this case. When the workload is enlarged to an extreme case, where each node issues one query per second, the cache usage is 1.5 Mbyte in average, while the maximum cache usage is less than 10M. The results show that the storage overhead of RR’s cache mechanism is acceptable for current PC configurations.

![](images/6847998f786a03433889d4c37c56b0acf125d78e11053e544e83b6eb808be510.jpg)



Fig. 13. Cumulative distribution of traffic overhead.

![](images/32180d4e3b693e39058b3e54ad9a83944737d366106f8a68134d4a652721090e.jpg)



Fig. 15. Storage overhead of cache in top 10,000 peers.

![](images/1c3b544e72e4ccd8f98847921889a50bf7839234b1b32982e362c7a584652dc8.jpg)



Fig. 16. Average cache usage.   
![](images/12312222c4810041491cd8118e0590329a0ae201df1c37306afb0666b47d2e39.jpg)



Fig. 17. Average cryptographic overhead of the initiator/responder.   
![](images/7f00986a9f630066df2160bb89a99e77d4f73467df958cc10afeb66510d8640d.jpg)



Fig. 18. Average cryptographic overhead of intermediate nodes.

We also examine the cryptographic overhead of the RR protocol. Figs. 17 and 18 contrast the average cryptographic overhead of RR and the Shortcut protocol in a query cycle. We can see that RR significantly reduces the cryptographic overhead for the initiators, responders, and intermediate nodes. The total cryptographic overhead of the initiator or responder is linearly proportional to the length of the Onion path when using the Shortcut protocol. Fig. 17 reflects this trend. Compared to RR, the Onion Routing technique leads to an overtly high cryptographic overhead for Shortcut users. Also, the computation overhead spent by the intermediate nodes on the Onion paths is significantly higher than RR. We find the ratio of the cryptographic overhead of RR to that of Onion Routing spent on the path is below 0.01, as shown in Fig. 18.

![](images/f9a2bf9cf8886f799fffa64b65589349a32aba9a69212db6d2ac11f5d6292b83.jpg)



Fig. 19. Average throughput of cryptographic operations.   
![](images/3dcc68b87a7098d1941abcef2b87f85d0f55fd9d67bdbfa44972f20d1d6f5ec4.jpg)



Fig. 20. Average packet throughput.

We implement a RR prototype on the Window XP platform. We use the Crypto++ Library to implement all built-in cryptographic algorithms. We set the default and maximum size of cache as 6MByte and 50MByte, similar to the settings of a popular P2P file sharing software BitComet [33]. The time-duration for cipher rumors is 2 minutes, and the time-duration is 10 minutes for key rumors. The size of the file fragment is 512 Kbytes. We examine the throughput and the latency of RR. Fig. 19 presents the average throughput of cryptographic operations, including AES key generation, AES operation, and RSA operation. In RR, the throughput of an initiator query depends on the rumor generation speed, which is mainly determined by the AES key generation and AES encryption. Fig. 20 summarizes the average packet throughput of each RR peer. The results show that the capacity of initiating rumors and local searching in caches are acceptable even in heavy loaded P2P systems.

# 6 CONCLUSION

We propose a lightweight and non-path-based mutual anonymity protocol for P2P systems, Rumor Riding (RR). Employing a random walk concept, RR issues key rumors and cipher rumors separately, and expects that they meet in some random peers. The results of trace-driven simulations and simple implementations show that RR provides a high degree of anonymity and outperforms existing approaches in terms of reducing the traffic overhead and processing latency. We also discuss how RR can effectively defend against various attacks.

Future and ongoing work includes accelerating the query speed, introducing mimic traffic to confuse attackers, and optimizing the k and L combination to further reduce the traffic overhead. We will also investigate other security properties of RR, such as the unlinkability, information leakage, and failure tolerance when facing different attacks. It would also be interesting to explore the possibility of implementing this lightweight protocol in other distributed systems, such as grid systems and ad-hoc networks.

# ACKNOWLEDGMENTS

This research was supported in part by the NSFC/RGC Joint Research Scheme N\_HKUST602/08 and N\_HKUST614/07, National Basic Research Program of China (973 Program) under Grant 2010CB328000, the 985 Program of China (Next generation Tsinghua Campus Network), the NSFC 60873262, Hong Kong Innovation and Technology Fund ITP/037/ 09LP, and the China Postdoctoral Science Foundation funded project No.20090461298.

# REFERENCES

[1] M.K. Reiter and A.D. Rubin, “Crowds: Anonymity for Web Transactions,” ACM Trans. Information and System Security, vol. 1, no. 1, pp. 66-92, Nov. 1998.

[2] L. Xiao, Z. Xu, and X. Zhang, “Low-Cost and Reliable Mutual Anonymity Protocols in Peer-to-Peer Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 14, no. 9, pp. 829-840, Sept. 2003.

[3] R. Sherwood, B. Bhattacharjee, and A. Srinivasan, “P5: A Protocol for Scalable Anonymous Communication,” Proc. IEEE Symp. Security and Privacy, pp. 58-70, 2002.

[4] D. Chaum, “Untraceable Electronic Mail Return Addresses, and Digital Pseudonyms,” Comm. ACM, vol. 24, no. 2, pp. 84-90, Feb. 1981.

[5] R. Rivest, A. Shamir, and L. Adleman, “A Method for Obtaining Digital Signatures and Public-Key Cryptosystems,” Comm. ACM, vol. 21, no. 2, pp. 120-126, 1978.

[6] M.K. Wright, M. Adler, B.N. Levine, and C. Shields, “The Predecessor Attack: An Analysis of a Threat to Anonymous Communications Systems,” ACM Trans. Information and System Security, vol. 7, no. 4, pp. 489-522, Nov. 2004.

[7] D. Goldschlag, M. Reed, and P. Syverson, “Onion Routing,” Comm. ACM, vol. 42, no. 2, p. 39, 1999.

[8] R. Dingledine, N. Mathewson, and P. Syverson, “Tor: The Second-Generation Onion Router,” Proc. 13th USENIX Security Symp., pp. 303-320, 2004.

[9] V. Scarlata, B.N. Levine, and C. Shields, “Responder Anonymity and Anonymous Peer-to-Peer File Sharing,” Proc. IEEE Int’l Conf. Network Protocols (ICNP), pp. 272-280, Nov. 2001.

[10] Q. Lv, P. Cao, E. Cohen, K. Li, and S. Shenker, “Search and Replication in Unstructured Peer-to-Peer Networks,” Proc. 16th ACM Int’l Conf. Supercomputing, pp. 84-95, 2002.

[11] L.A. Adamic, R.M. Lukose, A.R. Puniyani, and B.A. Huberman, “Search in Power-Law Networks,” Physical Rev. E., vol. 64, p. 046135, 2001.

[12] C. Gkantsidis, M. Mihail, and A. Saberi, “Random Walks in Peerto-Peer Networks,” Proc. IEEE INFOCOM, 2004.

[13] N. Bisnik and A. Abouzeid, “Modeling and Analysis of Random Walk Search Algorithms in P2P Networks,” Proc. Second Int’l Workshop Hot Topics in Peer-to-Peer Systems, 2005.

[14] R. Morselli, B. Bhattacharjee, A. Srinivasan, and M.A. Marsh, “Efficient Lookup on Unstructured Topologies,” Proc. ACM Symp. Principles of Distributed Computing, 2005.

[15] H. Yu, M. Kaminsky, P.B. Gibbons, and A. Flaxman, “SybilGuard: Defending against Sybil Attacks via Social Networks,” IEEE/ACM Trans. Networking, vol. 16, no. 3, pp. 576-589, June 2008.

[16] “FIPS PUB 197: The Official AES Standard,” NIST, http:// csrc.nist.gov/archive/aes/index.html, 2001.   
[17] K. Sripanidkulchai, “The Popularity of Gnutella Queries and Its Implications on Scalability,” http://www-2.cs.cmu.edu/ \~kunwadee/research/p2p/gnutella.html, 2009.   
[18] J. Han, Y. Liu, and J. Wang, “Rumor Riding: Anonymizing Unstructured Peer-to-Peer Systems,” technical report, http:// www.cse.ust.hk/\~jasonhan/RR-TR.pdf, 2009.   
[19] S. Jiang, L. Guo, X. Zhang, and H. Wang, “LightFlood: Minimizing Redundant Messages and Maximizing Scope of Peer-to-Peer Search,” IEEE Trans. Parallel and Distributed Systems, vol. 19, no. 5, pp. 601-614, May 2008.   
[20] M. Li, W.-C. Lee, A. Sivasubramaniam, and J. Zhao, “SSW: A Small-World-Based Overlay for Peer-to-Peer Search,” IEEE Trans. Parallel and Distributed Systems, vol. 19, no. 6, pp. 735-749, June 2008.   
[21] C. Gkantsidis, M. Mihail, and A. Saberi, “Conductance and Congestion in Power Law Graphs,” Proc. ACM SIGMETRICS, 2003.   
[22] I. Abraham and D. Malkhi, “Probabilistic Quorums for Dynamic Systems,” Proc. Int’l Symp. Distributed Computing, 2003.   
[23] Y. Zhu, X. Fu, R. Bettati, and W. Zhao, “Analysis of Flow-Correlation Attacks in Anonymity Networks,” Int’l J. Security and Networks, vol. 2, nos. 1/2, pp. 137-153, Mar. 2007.   
[24] B.N. Levine, M.K. Reiter, C. Wang, and M. Wright, “Timing Attacks in Low-Latency Mix Systems,” Proc. Eighth Int’l Conf. Financial Cryptography, 2004.   
[25] M.K. Wright, M. Adler, B.N. Levine, and C. Shields, “The Predecessor Attack: An Analysis of a Threat to Anonymous Communications Systems,” ACM Trans. Information and System Security, vol. 7, no. 4, pp. 489-522, 2004.   
[26] Y. Zhu, X. Fu, B. Graham, R. Bettati, and W. Zhao, “Correlation-Based Traffic Analysis Attacks on Anonymity Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 21, no. 7, pp. 954-967, July 2009.   
[27] S.J. Murdoch and G. Danezis, “Low-Cost Traffic Analysis of Tor,” Proc. IEEE Symp. Security and Privacy, 2005.   
[28] D. Stutzbach, R. Rejaie, and S. Sen, “Characterizing Unstructured Overlay Topologies in Modern P2P File-Sharing Systems,” IEEE/ ACM Trans. Networking, vol. 16, no. 2, pp. 267-280, Apr. 2008.   
[29] A. Medina, A. Lakhina, I. Matta, and J. Byers, “BRITE: An Approach to Universal Topology Generation,” Proc. Int’l Workshop Modeling, Analysis and Simulation of Computer and Telecomm. Systems (MASCOTS), 2001.   
[30] S. Saroiu, P. Gummadi, and S. Gribble, “A Measurement Study of Peer-to-Peer File Sharing Systems,” Proc. Multimedia Computing and Networking (MMCN) Conf., 2002.   
[31] S. Sen and J. Wang, “Analyzing Peer-to-Peer Traffic across Large Networks,” IEEE/ACM Trans. Networking, vol. 12, no. 2, pp. 219- 232, Apr. 2004.   
[32] Y. Liu, L. Xiao, X. Liu, L.M. Ni, and X. Zhang, “Location Awareness in Unstructured Peer-to-Peer Systems,” IEEE Trans. Parallel and Distributed Systems, vol. 16, no. 2, pp. 163-174, Feb. 2005.   
[33] “BitComet Options,” http://wiki.bitcomet.com/BitComet\_ Options, 2009.

![](images/2988f4a843b2dedd3b616e3bd374bd3aef82038d9f0802adf3a0c2210d8a5504.jpg)



Yunhao Liu (SM ’06) received the BS degree in automation from Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. His research interests include peer-to-peer computing, pervasive computing, and sensor networks. He is a senior member of the IEEE and the IEEE Computer Society, and a member of the ACM. He is an ACM Distinguished Speaker. He serves

as an associate editor for IEEE Transactions on Parallel and Distributed Systems and IEEE Transactions on Mobile Computing.

![](images/666ff97c445941b5a4f4fb2ce6be92e72cd01a7e48aafdb7cc62d93b67470e1f.jpg)



Jinsong Han (M ’04) received the PhD degree in computer science and engineering from the Hong Kong University of Science and Technology in 2007. He is currently a postdoctoral fellow at the Xi’an Jiaotong University. His research interests include peer-to-peer computing, anonymity, pervasive computing, network security, and highspeed networking. He is a member of the IEEE, the IEEE Computer Society, and the ACM.

![](images/c8c6ebb3c49c74c7e55b1dc8f6244ce5c7f4ac44ed86b1a2e7a1b58f26e72c06.jpg)



Jilong Wang is an associate professor at Tsinghua University. He is also the director of Network Operation Center of several large-scale network infrastructures, including Tsinghua Campus Network (TUNET), China Next Generation Internet Backbone Network (CNGI-CER-NET2), and Trans-Eurasia Information Network (TEIN). His research interests include network management and network measurement. He is a member of the IEEE.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.