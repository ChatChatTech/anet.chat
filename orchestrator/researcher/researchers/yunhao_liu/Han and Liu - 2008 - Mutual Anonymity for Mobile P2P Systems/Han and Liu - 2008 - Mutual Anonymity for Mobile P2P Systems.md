# Mutual Anonymity for Mobile P2P Systems

Jinsong Han, Member, IEEE Computer Society, and Yunhao Liu, Senior Member, IEEE Computer Society

Abstract—Mobile Peer-to-Peer Networks (MOPNETs) have become popular applications due to their ease of communication and resource sharing patterns in unfixed network infrastructures. As privacy and security are coming under increasing attention, many mobile and ad hoc network protocols attempt to provide mutual anonymity for users. Most existing anonymous designs, however, are path based, where the anonymous communications are achieved via a predetermined path. Such a design suffers from unreliable delivery and high processing overheads and is not practical. We propose a scalable secret-sharing-based mutual anonymity protocol, termed PUZZLE, which enables anonymous query issuance and file delivery for MOPNETs in ad hoc environments by employing Shamir’s secret sharing scheme. We present the design of PUZZLE, analyze its degree of security and anonymity, and evaluate its performance by comprehensive trace-driven simulations. Experimental results show that compared with previous designs, PUZZLE achieves mutual anonymous communications with a lower cryptography processing overhead and higher degree of anonymity.

Index Terms—Mobile Peer-to-Peer, mutual anonymity, secret sharing.

# 1 INTRODUCTION

Mobile Peer-to-Peer Network (MOPNET) [1], [2], [3] Acomprises a set of moving devices, called peers, that are self-organized as an ad hoc network (without any fixed infrastructure). MOPNET peers cooperate to share resources with each other via short-range wireless technologies such as IEEE 802.11, Bluetooth, or Ultra-Wideband (UWB).

The requirements for both privacy and anonymity [4] have become increasingly essential in many MOPNET applications recently. Achieving anonymity in MOPNETs allows a peer to arbitrarily communicate with other nodes while its identity cannot be determined by anyone. Anonymity usually comprises three parts: initiator anonymity, responder anonymity, and mutual anonymity (providing both the initiator and responder anonymity). The initiator (responder) anonymity protects the initiator (responder) from being exposed to all other entities including the responder (initiator) during the message delivery. Most previous works only provide the initiator or sender anonymity. On the other hand, mutual anonymity in MOPNETs often implies 1) initiator and responder anonymity and 2) anonymous communication, in which any other party cannot identify a pair of peers as anonymously communicating with each other [5].

The past years have seen an increasing emphasis on anonymity in the mobile ad hoc network (manet) literature [6], [7], [8], [9], [10], including senders’ privacy protection, anonymous routing, and tracing resistance. Those works, however, barely meet the mutual anonymity requirement in MOPNETs.

The majority of those approaches are path based: delivering messages over a number of predetermined untraceable paths. The path-based techniques are inherited from wired network environments such as Mix [11] and onion routing [12]. In such a scheme, paths are encrypted using asymmetric cryptographic algorithms, for example, RSA, and the messages are encapsulated in a layered encrypted packet. As illustrated in Fig. 1, a source node A utilizes a predetermined path, for example, an onion route [12], to deliver messages to a destination node D. Before delivery, A collects the IP addresses and public keys of the intermediate nodes B and C to form the layered encrypted packets. The packets are embedded in the routing information of the anonymous path. During transmission, the intermediate nodes decrypt the received messages using their private keys and seek the IP address of the next hop, like peeling a layer from the received packet. Note that each intermediate node only knows its direct predecessor and its direct successor. This feature is guaranteed by using RSA algorithms. At last, the destination node D receives the innermost layer of the original packet and recovers the content of the message using its own private key. In this procedure, no other node except A has complete knowledge about the routing, content, and source node of the delivered messages. Path-based approaches achieve high security and low traffic cost.

In most wireless scenarios, however, it is extremely difficult in practice to guarantee the reliability of message delivery via path-based approaches. The above argument is derived from the following observations. First, the predetermination of the anonymous path cannot guarantee the reliable message delivery in the highly dynamic MOPNET environment. Since all paths are constructed by the source node, it has to probe the availability of nodes in those paths. Second, even though the source node confirms that those intermediate nodes are active before message delivery, the paths are still undependable due to the mobility of nodes in MOPNETs. When an intermediate node moves out of range, the path will crash. Third, the paths should be periodically updated for security concerns. Otherwise, adversaries are able to mount a set of attacks [13] to compromise users’ privacy. The maintenance and update overheads to support the anonymous paths are cumbersome, especially for source-limited initiating nodes.

![](images/74c80b0e0a9372a7e2aab1a97f19bdc0583c07ac1ec49325810e973bdd06292b.jpg)



Fig. 1. Path-based anonymous routing scheme.

In addition, the processing overhead is often high due to the usage of an asymmetric key cipher. A source node has to conduct multiple encryptions with the public keys of the intermediate nodes in the path, while each intermediate node also needs to perform a decryption with its private key upon receiving the layered encrypted packets. To confuse the observer, all layered encrypted packets should be padded with the same length. The additional overhead limits the practical implementation of anonymity in manets.

In this work, we propose a mutual anonymity protocol in MOPNETs, called PUZZLE. PUZZLE employs Shamir’s Secret Sharing (SSS) scheme [14] to anonymously issue queries and utilizes the Information Dispersal Algorithm (IDA) [15] to achieve anonymous downloading. PUZZLE leverages the broadcasting feature of manets to achieve mutual anonymity. We introduce reasonable redundancy into MOPNETs to enhance the reliability of this protocol. The main advantages of our design include the nonpathbased anonymous query issuance and file downloading, reliable message delivery, high degree of anonymity, and low cryptographic overhead compared with previous designs. We evaluate PUZZLE by trace-driven simulations and contrast its performance with existing approaches.

The rest of this paper is organized as follows: We discuss the related works in Section 2. We introduce the system model and tools in Section 3. We present the PUZZLE protocol in Section 4 and analyze the degree of anonymity and security of PUZZLE in Section 5. Our simulation and evaluations are presented in Section 6. We conclude this work in Section 7.

# 2 RELATED WORK

Many approaches have been proposed for anonymous communication over the Internet [5], [16], [17], [18], [19], [20]. The methods that provide anonymity are normally categorized into two models: degrading broadcasting and path-based forwarding. Most are designed based on cryptographic measures, for example, the asymmetric ciphe algorithm. The degrading broadcasting, borrowing the idea of anonymous multicasting, broadcasts encrypted messages, which can only be revealed by the desired receivers. The drawback of those approaches is that they often incur huge amounts of traffic into the network. The most representative proposal is P5 [21]. To keep the broadcasting scope scalable, ${ \bar { \mathrm { P } } } ^ { 5 }$ organizes all peers into different broadcasting channels using a logic hierarchical tree. $\mathrm { P ^ { 5 } }$ also introduces noise packets to maintain a fixed communication rate among the peers in a channel to confuse traffic analyzers. Each message is encrypted using the destination peer’s public key so that only the desired receiver can recover the message. Although $\mathrm { P ^ { 5 } }$ refines the broadcast channel size and avoids flooding each message into the whole network, it is difficult to keep the communication scalable in a large-scale P2P system. $\mathrm { P ^ { 5 } }$ requires an initiator to know the public keys of all possible responders, which is a critical assumption in P2P systems. Therefore, having the same features, other degrading broadcasting based models are also inappropriate for P2P systems.

The path-based forwarding approaches construct predetermined paths for anonymous data delivery. The most pioneering approaches are Mix [11] and onion routing [12]. The major difficulty is that the sender has to obtain a lot of information about the middle nodes, including their IP addresses, public keys, and so on. Specifically, APFS [22] allows users to contact each other depending on untrusted proxies via path-based techniques. Crowds [23] and Hordes [19] employ probabilistic forwarding mechanisms when delivering messages. Each intermediate node can either forward a message to the destination or relay it to a random chosen successor peer. MorphMix [18], Freedom [16], Tarzan [5], and Tor [17] are all implemented based on onion routing to provide anonymous services.

Regarding manets, recent anonymity efforts have mainly focused on anonymous routing. ANODR [8] is the first ondemand anonymous routing protocol in manets. ANODR makes use of trapdoor information to guarantee that only the receiver can open the encrypted message. The response to a request is anonymized by using onion routing [12]. It employs flooding to deliver the packets and symmetric key cipher for achieving anonymity. However, the source node has to know the ID of the destination node before routing discovery. In this sense, the receiver reveals its identity to the source node. MASK [10], mainly deployed on the MAC layer, enhances anonymity by constructing a secure and anonymous link between two neighboring nodes before on-demand route discovery. As MASK needs a trusted authority before system deployment, it is not suitable for decentralized MOPNETs, in which there is no trusted third party. MASK also has to reveal the receiver’s ID to the sender in anonymous communications.

Other works in wireless networks are aiming to protect specified peers such as the sink node [24] or location privacy proposed by Panda Hunting [25]. Location-Based Services [6] and Mix Zones [7] develop middleware services to protect the user location information in manets and wireless sensor networks. Those works do not focus on mutual anonymity in MOPNETs.

PUZZLE has two main differences from previous approaches: 1) we employ a secret sharing scheme to enable initiator anonymity P2P manets, which is beyond the traditional path-based designs, most of which mainly use onion routing based on predetermined secure paths, and 2) neither the initiator nor the responder needs to reveal their ID or even a pseudonym to the other side. In contrast, a sender has to know the receiver’s IP address or pseudonym to form an onion path in most of the previous approaches.

# 3 SYSTEM MODEL AND TOOLS

In this section, we introduce the tools and system model of PUZZLE.

# 3.1 Secret Sharing Scheme

The objective of a secret sharing scheme is to share a secret key among several participants and protect that key from loss. In this scheme, a secret sender (or dealer) divides a secret s into n pieces and distributes them to n participants. Some or all of these pieces, called shares, can be pooled together to recover the original secret. One of the most popular secret sharing schemes is SSS [14]. SSS is a threshold secret sharing scheme, which allows a subset T , containing no less than $t \left( t < n \right)$ participants, to recover the secret. More details of the SSS mechanism are available in [14]. Since the polynomial interpolation of SSS algorithms is $O ( n l o g ^ { 2 } n )$ , the complexity of the Lagrange interpolation needed to recover the secret is $O ( t l o g ^ { 2 } t )$ [14].

# 3.2 Information Dispersal Algorithm

The drawback of SSS is that all of the shares are of the same size jsj, where jsj is the size of the original secret. Thus, if the secret is a large-size file, SSS is not efficient. In this design, we use another splitting scheme, IDA, which was first introduced by Rabin [15]. Similar to SSS, a ðt; nÞ IDA intends to distribute a message s among n processors. Meanwhile, the recovery of the information is available if the collection of shares is up to t $( 1 < t < n )$ . The key difference between IDA and SSS is that the length of each distributed fragment of IDA is jsj=t. Clearly, IDA is more space efficient than SSS in splitting large files. IDA is usually employed together with erasure code schemes [15]. As the basic IDA does not provide protection from malicious parties for the data, we combine SSS and IDA together as a Secret IDA (SIDA) [26] in this design.

# 3.3 System Model

For the simplicity of discussion, we assume the MOPNET is deployed over a manet using IEEE 802.11. All wireless links are symmetric, which means that if a node A is in the transmission range of node B, B is also in the transmission range of A. In addition, all the peers can broadcast data packets to their neighboring nodes or directly send a unicast packet to a particular neighbor via a MAC interface. To keep anonymity in PUZZLE, peers can anonymously broadcast a packet with a specific multicast address in which all 1’s can be used as the source or destination MAC address. In addition to employing PUZZLE, we also assume that MOPNETs can still use AODV [27] for normal packet routing.

PUZZLE focuses on unstructured decentralized MOP-NET systems. In such systems, peers are interlinked with their neighbors, forming an overlay network. Flooding is usually used as the search method. A query is continuously broadcast until a desired file is found or the query travels a given number of hops. If a peer can provide the requested object, a response message will be delivered back to the source peer along the inverse of the query path, and a direct download path is constructed between the downloader and the source peer, as illustrated in Fig. 2.

![](images/14cf45ab00531f94b1a8da5496da29b914f0541a13b54f8523cad39b0ab2e060.jpg)



Fig. 2. Normal query flooding in unstructured MOPNET networks.

# 4 PUZZLE PROTOCOL

In this section, we first give a brief overview of PUZZLE and then present the details of this design.

# 4.1 Overview

The PUZZLE protocol rebuilds the basic query cycle to meet the anonymity requirement. The brief flow of a new anonymous query cycle is comprised of three phases: query issuance, reply-confirm, and file delivery. At the very beginning, each initiator employs the ðt; nÞ SSS and SIDA to distribute a symmetric key and an encrypted query message into n pieces of shares. These shares are flooded thereafter in MOPNETs. After shares have been broadcasted a certain number of hops, some peers, called agents, collect at the least t different shares of one query. These peers recover the query messages and start flooding the original query in MOPNETs. If we perform flooding without any constraints, each node would become an agent without the traffic load being scalable. To decrease the traffic load, PUZZLE performs a probabilistic flooding to spread shares in MOPNETs. We detail the probabilistic model in Section 4.2 and further discuss the parameter selection in our simulation and evaluation part. A responding peer that is able to provide the requested file delivers the response message to an agent through an onion path. An agent peer uses SIDA again to generate shares from the reply message and sends the shares back along the reversed paths to the initiator. The confirmation message is also delivered via an onion path, which is discussed in detail in Section 4.3. Finally, the responder splits the file into fragments using SIDA, and the fragments are delivered to the initiator along the reversed paths. In this process, the identities and sensitive information about the initiator and responder are completely hidden.

PUZZLE leverages the AODV routing table. Each peer holds entries for shares received from or sent to the neighbors. As a result, the reversed share paths can be followed correctly. In addition, a time-out scheme is introduced to remove failed queries and keep the table size scalable.

In addition, query share delivery in PUZZLE is a little different from the normal query process. Each peer that receives a query share has two choices: anonymously broadcasting this share to all other neighbors or just forwarding it to a randomly chosen neighbor via unicast.

![](images/a1faad3ead12fb83a294066d442ce2008c936494096899fceb03876de18f51f4.jpg)



Fig. 3. Anonymous query.

The selection between broadcast and unicast is determined based on a probability $p ,$ which is a system parameter assigned to newly joining peers.

# 4.2 Anonymous Query

An initiator peer starts an anonymous query for a desired file F by following two phases: 1) share generation and 2) share flooding/forwarding. We give an example in Fig. 3, where initiator I employs (2, 3) SIDA to split a query into three shares in the share generation phase and sends them to three neighbors: $N _ { 1 } , N _ { 2 } ,$ , and $N _ { 3 }$ . After share flooding and forwarding, peers $P _ { 1 } , P _ { 2 } ,$ , and $P _ { 3 }$ recover the original query. They flood this query, and eventually, this query reaches a responder R. The detailed description about the two phases is given as follows:

Share generation. The initiator I randomly selects a list of neighboring peers $N _ { 1 } , N _ { 2 } \ldots N _ { n }$ . It generates a random AES key $K _ { s \prime }$ which is used to encrypt $f ,$ the file ID or name of F . To distribute the query message, I employs the SIDA as shown in Fig. 4.

Meanwhile, I creates a sequence number sq to mark this query. In addition, I creates a pair of RSA keys, public key $K _ { I + }$ and private key $K _ { I }$ -. Before sending these messages, I embeds $K _ { I + }$ into those packets. For each share packet, I also attaches a packet sequence number $s p .$ Peer I randomly chooses neighboring peers $N _ { i }$ and sends the packet $< s h _ { i } , K _ { I + } , s q , s p _ { i } > , i = 1 , \ldots , n ,$ , to them, respectively.

Scalable share spreading. After the shares are sent from $I ,$ they start to spread in the MOPNET. A potential issue is that the shares may spread to all nodes in the MOPNET if the moving hops of shares are not limited. This is unnecessary and incurs a huge traffic cost to MOPNETs. To solve this problem, we inherit the limited flooding scheme in wired P2P systems to constrain the spreading scope of each share. I randomly generates a TTL value for each share to bound the traveling hops. The TTL is decremented by one at each intermediate node. The initial TTL values of shares are not necessarily identical. However, the value is no larger than a maximum Cmax, which represents the network radius in terms of hops.

# Algorithm:Share distribution

Select random AES key $K _ { s }$ and encryptf as e = E(f).

Split e into n fragments using $\mathrm { I D A } , e _ { 1 } , . . . , e _ { n } .$

Split $K _ { \mathrm { s } }$ into n shares using (t, n) SSS, $K \mathbf { s } _ { \scriptscriptstyle 1 } , . . . , K s _ { \scriptscriptstyle n } .$

Distribute $( e _ { i } , K s _ { i } , t )$ to n shares $s h _ { i } , i = 1 . . n .$

Fig. 4. Distributing a query message.

# Algorithm: Query reconstruction

Receiving $t \ ( t < n )$ or more shares $s h _ { i } \mathbf { = } ~ ( e _ { 1 } , \ K s _ { 1 } ) , . . . , \ ( e _ { t } ,$ $K s _ { t } )$ and t.

Reconstruct e from $e _ { _ { 1 } } , . . . , e _ { _ t } .$

Reconstruct Ks from $K s _ { \scriptscriptstyle 1 } , \ldots , K s _ { \scriptscriptstyle t } .$

Decrypt e as $f = D _ { \kappa \mathrm { s } } \left( e \right) .$

Fig. 5. Reconstructing a query message.

Share flooding/forwarding decision. When each ${ \cal I } ^ { \prime } \mathrm { s }$ neighbor receives a new query share, it broadcasts the share in the probability $p ,$ or forwards the share to a randomly chosen neighbor in the probability ð1 - pÞ. For broadcast, the peer $N _ { i }$ sets all bits of the MAC and IP addresses of the source and destination as one. Otherwise, $N _ { i }$ simply forwards the share packet to a randomly chosen neighbor except I.

For both broadcasting and forwarding patterns, any peer keeps an entry of each share in its local routing table. When shares are inserted into the system, each peer carries out the same operations as above to process a received share. Each peer marks those distinct shares with an identical sq marked as an identical set. When the number of distinct shares in a set exceeds t, the peer can recover the original query. Our experimental results show that a careful selection of the value of $p$ would lead to a fast gathering of the shares. Without loss of generality, we assume that $\dot { P _ { 1 } }$ is one of the peers that collects an enough number of shares to recover f by employing the algorithm in Fig. 5.

In PUZZLE, we mainly use AODV as the routing protocol for the neighboring nodes to connect with each other. Note that using AODV does not compromise the anonymity. The routing table and data packets in AODV include some fields such as “Destination,” “Source,” “Next Hop,” and “Hop Count,” which reflect some information about the network connections and may cause anonymity concerns. The initiator and responder in PUZZLE, however, cannot be located because AODV is used for the share delivery among neighboring nodes, rather than directly transferring a packet from the initiator to the responder.

Normal query flooding. When $P _ { 1 }$ obtains the recovered $f ,$ it can flood the original query for I. $P _ { 1 }$ embeds its $\mathrm { I P }$ address into the query message and then floods the message in MOPNETs. Note that $P _ { 1 }$ is not aware of ${ \cal I } ^ { \prime } \mathrm { s }$ identity. In this situation, $P _ { 1 }$ becomes an agent peer of I. Before flooding, $P _ { 1 }$ appends its public key to the query message. This operation is for constructing an onion path in the reply-confirm phase, which is explained in Section 4.3. $\mathrm { A s }$ illustrated in Fig. 2, the query message eventually reaches the responder $R ,$ a peer that is willing to provide the queried file.

Due to the query flooding, some peers may receive replicated queries with an identical sq but different $P _ { i }$ (that is, the peer receives replicated queries from different anonymous agents of a given initiator). In this case, the peer simply drops the query for the purpose of saving network resources, which is a similar strategy adopted by wired P2P systems to handle the query replication.

In fact, the first phase of PUZZLE has provided sender anonymity for manets. If we do not need to protect the receiver anonymity, the anonymous query mechanism of PUZZLE is sufficient to protect the sender’s privacy. For MOPNET users, we also need to provide anonymity in the entire query cycle, that is, anonymizing reply-confirm and file delivery phases.

![](images/ec527c75d2cd7a95720b3af39e58323ed32e058b29bfb50e8b0407449f7304e9.jpg)



Fig. 6. Reply and confirm.

# 4.3 Reply and Confirm

In this phase, PUZZLE allows the responder and initiator to exchange their reply and confirm messages based on onion routing. As shown in Fig. 6, R anonymously delivers the reply message to agent P1 via an onion path. P1 then employs a SIDA scheme to return this reply to I, and I sends the confirmed message through another onion path to R. The details are given as follows:

Reply. For replying to I and obtaining a confirmed message from $I , { \hat { R } }$ builds two anonymous paths in advance based on a bidirectional onion protocol.

Forwarding path

$$
F P = \left\{X, \left\{Y, \dots \left\{P _ {1}, \{r e p l y, R P, s q \} K _ {P _ {1} ^ {+}} \right\}, \dots \right\} K _ {Y ^ {+}} \right\} K _ {X ^ {+}} \Bigg \}.
$$

Returning path

$$
R P = \{U, \{V, \dots \{W, \{R, f i x m i x \} K _ {W ^ {+}} \}, \dots \} K _ {V ^ {+}} \} K _ {U ^ {+}} \},
$$

where fixmix is the padding bits.

In MOPNET, each peer may receive a number of normal query messages. Those messages are usually flooded by some agent peers. PUZZLE allows each peer to temporarily store the received query messages in a cache table. In this table, each entry has a time stamp to record the receiving time of the query message. More recent messages indicate that the relevant agent peers are more likely to be active. Therefore, R selects those peers with fresh time stamps from the cache table to construct the onion paths. In this way, the constructed onion path is much more reliable.

The reply message includes a description of provided files. R delivers the packets through $F \bar { P }$ to $P _ { 1 }$ . When the reply packet reaches P1, P1 first decrypts the cipher and gets the sq and file name. It then checks the $s q$ in its local routing table. $P _ { 1 }$ then integrates all received replies into a single reply message $I n R e p l y _ { - } P _ { 1 }$ and uses $K _ { I + }$ to encrypt it. In addition, $P _ { 1 }$ employs a ðs; tÞ threshold SIDA scheme $( s < t )$ to distribute $I n R e p l y \mathcal { P } _ { 1 }$ to t shares and marks them with $s q$ and another sequence number $s q \mathrm { _ { - } } P _ { 1 }$ , which distinguishes reply shares from other agent peers. Then, $P _ { 1 }$ delivers those reply shares back along the virtual reversed paths based on $s q .$ Each intermediate node that receives a reply packet first searches the sq in its routing table. If there is an entry marked $s q ,$ the intermediate node delivers the reply message to the peer who sent the corresponding query message to it. If the corresponding query message was received via anonymous broadcasting, the intermediate node simply broadcasts the reply. If there is no entry marked with sq, the intermediate node simply discards the packet. All reply share packets eventually reach I.

![](images/6b43a949410d55be0d901644cf9045b538dd1605ee263c0e463d250fff4bff0e.jpg)



Fig. 7. File delivery.

Confirm. Upon s reply shares from $P _ { 1 }$ , I recovers the reply message InReply $P _ { 1 }$ from s reply shares. Generally, there could be more than one agent peer of I. Therefore, I may receive more than one reply from certain peers delivered by those $P _ { i } , i = 1 , \ldots , m$ . I picks one as a responder, for example, R. I then creates a list L for all available agents $P _ { i } ,$ where $L = \{ P _ { 1 } \ldots P _ { m } \}$ . In addition, I selects a number $t ^ { \prime } < m$ as the SIDA threshold for splitting the requested file. I sends the packet embedded with the list L, t 0 , and $K _ { I + }$ to the first peer that is appointed by the responder R on its onion return path ðRP Þ. As shown in Fig. 6, I and R complete the reply-and-confirm procedure anonymously.

# 4.4 File Delivery

Upon the confirm message, R delivers the targeted file F to I. In this phase, R first splits F into fragments using SIDA and then delivers them back along the reversed paths marked by $s q ,$ which is shown in Fig. 7.

File splitting. After receiving the request-confirm packet from the last onion peer in RP , R makes use of SIDA to split the file into fragments, which is presented in Fig. 8.

R finally generates m split data fragment packets $s h _ { i } ^ { \prime }$ for m peers in L and marks the packet as a data type and labels it sq. All information in list L is put into every packet as well. After these steps, R randomly chooses its m neighbors and sends the above packets (if R’s neighbors are less than $m ,$ R can send some packets to the same neighbor).

Fragments delivery. Each peer who receives a fragment packet randomly selects a peer d from L and forwards the packet to it. Peer d then delivers the packet to the next peer marked sq. The next peer would do the same operation

# Algorithm: File fragmenting

Select a random AES key $K'$ and encrypt $F$ with $K': e' = E_K(F + hash(F))$ Encrypt key $K'$ with key $K_{I+}$ to get $T'$ Partition $e'$ into $m$ fragments using $(t', m)$ IDA and obtain $e'_1, \ldots, e'_m$ .

Partition $T'$ into $m$ shares using $(t', m)$ SSS to get $T'_1, \ldots, T'_m$ .

Distribute $(e'_i, T'_i)$ to $sh'_i, i = 1..m$ .   
Fig. 8. Splitting a file into fragments.

Algorithm: File reconstruction 

<table><tr><td>Given  $t' < m$  shares ( $e_{1}', T_{1}', t'$ ),..., ( $e_{t'}, T_{t'}, t'$ )</td></tr><tr><td>Reconstruct  $e'$  from  $e_{1}', \ldots, e_{t'}$ </td></tr><tr><td>Reconstruct  $T'$  from  $T_{1}', \ldots, T_{t'}$ </td></tr><tr><td>Decrypt  $T'$  with  $I$ &#x27;s private key to get  $K'$ </td></tr><tr><td>Decrypt  $e'$  as  $F = D_{K'}(e')$ , checkout  $F$  with  $hash(F)$ </td></tr></table>

Fig. 9. Reconstructing a file from fragments.

until the data packet reaches some members of L. This peer in L delivers the packet to I along some reversed paths.

File reconstruction. I keeps checking on the number of sq-marked data packets it receives. When the number exceeds $t ^ { \prime } , \ I$ recovers the desired file from the received fragments by employing the algorithm in Fig. 9.

# 5 ANONYMITY AND SECURITY ANALYSIS

# 5.1 Anonymity

We first analyze the anonymity degree of PUZZLE for different parties.

The initiator and responder. The probability for an initiator (responder) to randomly guess the responder’s (initiator’s) identity is $1 / ( N - 1 )$ , where N is the number of nodes in the system. The reply of the query is forwarded by the agent peers. If the responder is not the agent peer, its identity is hidden by the onion path. With the onion path, the expected number of path reformations required for c attackers to determine the initiator is $O ( \left( N / c \right) ^ { 2 } ) \left[ 2 8 \right]$ .

The middle nodes. In the query flooding path, the middle nodes can be categorized into two groups: peers who receive the shares and the remaining peers except the initiator and responder. For the first group, the probability of the members being able to correctly guess the initiator or the responder is $1 / ( \breve { N } - 1 )$ Þ. Now, we discuss the situation of the systems under attacks from collaborating malicious peers. Suppose x is a malicious peer that is nearest to the initiator, say, x is the fewest hops away from the initiator among all attackers. Let $p _ { d } ( i )$ denote the probability of existing i peers between the initiator and first malicious peer x. The initiator itself occupies the zeroth position, N is the number of total peers, M is the number of malicious peers, and l is the path length of the channel between the initiator and an agent peer that receives shares from x. S is a subset of the whole system in which the peers get their shares from the initiator.

We continue to use the same notations as in [23]. Let $H _ { k } ,$ , $k \geq 1$ , denote the event in which the first collaborator x on the path occupies the kth position on the path, where the initiator itself occupies the zeroth position (and possibly others), and denote $H _ { i + } = H _ { i } \lor H _ { i + 1 } \lor H _ { i + 2 } . . . .$ Let I denote the event that the initiator is just before x on the path. Given this notation, we calculate the probability $P ( I | \bar { H } _ { 1 + } ) .$ , that is, what is the probability that attackers correctly guess the initiator identity?

Therefore, $H _ { k } , k \geq 1 ,$ which denotes the event that the first adversary on the path occupies the kth position on the path, is

$$
\operatorname * {P r} [ H _ {k} ] = \left(\frac {N - M}{N}\right) ^ {k - 1} \cdot \frac {M}{N}.
$$

(Here, each peer is a malicious one with the probability $M / N . )$ Meanwhile, we use $p _ { s } ( t )$ to denote the probability that collaborating adversaries receive t different shares of a $( t , n )$ SSS and $p _ { f }$ as the forwarding probability. Here, the $p _ { f }$ is different from the flooding/forwarding probability p. We consider $p _ { f }$ as the probability that a node is willing to forward the received share. In the MOPNET, some selfish nodes may drop the received packets, as we will discuss in Section 6.3. Thus,

$$
\begin{array}{l} \operatorname * {P r} [ I | H _ {1 +} ] = \sum_ {i = 1} ^ {l} \left(\frac {N - M}{N}\right) ^ {i - 1} \cdot \frac {M}{N} \cdot p _ {f} ^ {i - 1} \cdot p _ {d} (i) \cdot p _ {s} (t) \\ \leq \frac {M}{N} \cdot \left(\frac {1 - \left(\frac {N - M}{N}\right) ^ {l + 1}}{1 - \frac {N - M}{N}}\right) \left(\frac {| S |}{N - 1}\right) ^ {t} \\ \leq \left(1 - \left(1 - \frac {M}{N}\right) ^ {l + 1}\right) \cdot \left(\frac {| S |}{N - 1}\right) ^ {t}. \\ \end{array}
$$

The file is split into fragments when being delivered. Even though an attacker could recover a file from the shares, it cannot decrypt the content from the ciphertext without the private key of the initiator. Suppose $x ^ { \dagger }$ is the malicious peer that is nearest to the responder. The probability that attackers correctly guess the responder’s identity is

$$
\begin{array}{l} \operatorname * {P r} [ R | H _ {1 +} ] = \sum_ {i = 1} ^ {l ^ {\prime}} \left(\frac {N - M}{N}\right) ^ {i - 1} \cdot \frac {M}{N} \cdot p _ {f} ^ {i - 1} \cdot p _ {d} (i) \cdot p _ {F} (t ^ {\prime}) \\ \leq \frac {M}{N} \cdot \left(\frac {1 - \left(\frac {N - M}{N}\right) ^ {l ^ {\prime} + 1}}{1 - \frac {N - M}{N}}\right) \left(\frac {| F g |}{N - 1}\right) ^ {t ^ {\prime}} \\ \leq \left(1 - \left(1 - \frac {M}{N}\right) ^ {l ^ {\prime} + 1}\right) \cdot \left(\frac {| F g |}{N - 1}\right) ^ {t ^ {\prime}}, \\ \end{array}
$$

where t 0 is the threshold of $( t ^ { \prime } , m )$ SIDA, $p _ { F } ( t ^ { \prime } )$ is the probability that collaborating attackers receive t 0 different fragments for $\textbf { a } ( t ^ { \prime } , m )$ SIDA, $F g$ is a subset of the whole system in which the peers get file fragments from the responder, l 0 is the path length of the channel between the responder and an agent peer that receives the fragment from the malicious peer $x ^ { \prime } ,$ and $p _ { f }$ is the forwarding probability number of peers on the data packet transfer path. In current large-scale MOPNET systems, all the probability of exposure in the above cases becomes extremely small.

# 5.2 Security

PUZZLE employs encryption methods in both query flooding and file delivery to achieve information security. Malicious peers may cooperate to implement attacks. PUZZLE makes such attacks difficult by the following three operations:

1. The SSS scheme protects the initiators’ privacy with perfect security.   
2. The file split pattern of SIDA provides computational security to responders.   
3. The cryptographic mechanism provides unlinkability security for transferring data.

Definition 1. Perfect security is that given any t shares of a $( t , n )$ secret sharing scheme, the polynomial is uniquely determined to compute the secret s. On the other hand, given t - 1 or fewer shares, the secret can be any element in the field, and hence, those shares cannot reveal any further information regarding the secret.

Theorem 1. PUZZLE holds perfect security in share distribution.

Proof. In the ðt; nÞ SSS scheme $( t < n ) .$ , given any t shares, the polynomial is uniquely determined. Hence, the secret s can be computed. On the other hand, given $t -$ 1 or fewer shares, the secret can be any element in the field. Thus, those shares do not supply any further information regarding the secret [29]. If $\dot { S } _ { 0 }$ is the secret, for every $k < t ,$ let $S _ { 1 } , \ldots , S _ { k }$ be any k shares. Then, $\mathrm { P r } ( S _ { 0 } | S _ { 1 } , \ldots , S _ { k } ) = \mathrm { P r } ( S _ { 0 } )$ . Indeed, we claim that the share distribution procedure of PUZZLE holds perfect secrecy. tu

Definition $2 . A \ ( t , n )$ threshold scheme $( t < n )$ is computationally secure if for any two secrets S0 and $S ^ { \prime \prime }$ and for any $k < t ,$ the distributions on shares $D ( S ^ { \prime } : S _ { 1 } ^ { \prime } , \ldots , S _ { k } ^ { \prime } ) \stackrel { \cdot } { }$ and $D ( S ^ { \prime \prime }$ : $S _ { 1 } ^ { \prime \prime } , \ldots , S _ { k } ^ { \prime \prime } )$ introduced by the scheme are polynomially indistinguishable [30].

Definition 3. Two sets $E _ { 0 } = \{ X _ { n } \}$ and $E _ { 1 } = \{ Y _ { n } \}$ are polynomially indistinguishable if for every polynomial-time algorithm, A and every $c > 0$ , there exists an integer N such that for all $n \geq N$

$$
\left| \operatorname * {P r} (A (X _ {n}) = 1) - \operatorname * {P r} (A (Y _ {n}) = 1) \right| <   \frac {1}{n ^ {c}}.
$$

Theorem 2. SIDA achieves computational security.

Proof. We assume that there exist secrets $s _ { 1 }$ and $s _ { 2 }$ and an algorithm A that can distinguish them from their spaces $S _ { 1 }$ and $S _ { 2 }$ w i t h a h i g h p r o b a b i l i t y : $\mathrm { P r } ( a ) = | \operatorname* { P r } ( A ( s _ { 1 } / S _ { 1 } ) = 1 ) - \operatorname* { P r } ( A ( s _ { 2 } / { S _ { 2 } } ) = 1 ) | > 0 . 5 .$

Then, we construct another algorithm B that can breach the polynomial indistinguishable encryption algorithm E by distinguishing between $E ( s _ { 1 } )$ and $\dot { \boldsymbol E } ( s _ { 2 } )$ in the probability

$$
\operatorname * {P r} (b) = \operatorname * {P r} | B (E (s _ {1}) / E (S _ {1})) - B (E (s _ {2}) / E (S _ {2})) |.
$$

If $E ^ { \prime } = S I D A ( E ( s ^ { \prime } ) ) = e _ { 1 } ^ { \prime } \dots e _ { n } ^ { \prime }$ and $X \subset E ^ { \prime } , \ | X | < t ,$ , we then get $X _ { 1 }$ and $X _ { 2 }$ from $E ( S _ { 1 } )$ and $E ( S _ { 2 } )$ and use A to guess whether the secret corresponds to $s _ { 1 }$ or s2. B can also output the same guess. If A guesses the correct result with a probability of more than 50 percent, then B would obtain the correct result with a significant probability:

$$
\operatorname * {P r} (b) = \operatorname * {P r} | B (e ^ {\prime} / S ^ {\prime}) | > 0. 5.
$$

We employ polynomial indistinguishable encryption algorithms in PUZZLE. Therefore, we conclude that the first assumption is nonexistent. In fact, the encryption algorithms’ security ensures that the t - 1 fragments in X give no more information than E. Further, there is absolutely no information to reveal the secret without more than t - 1 shares, as we prove in Theorem 1. tu

# 6 PERFORMANCE EVALUATION

In this section, we first define the performance metrics and describe the simulation methodology. We then present our observations on the distribution of shares so that we can illustrate the relationship among the parameters such as the flooding probability and the threshold of SSS. We also present the response time of PUZZLE, compared with the onion routing scheme. In addition, we investigate and compare the success rate of transactions of PUZZLE and onion-based schemes.

# 6.1 Metrics

In a P2P system, the QoS of a search depends on the number of peers being explored (queried), the response time, and the traffic overhead [31], [32]. Hence, the evaluation of PUZZLE focuses on the following performance metrics: redundant agent degree, traffic cost, response time, success rate of transaction, and security overhead.

Redundant agent degree refers to the number of agent peers. We are mainly concerned with two major issues here: the number of agent peers and the number of peers receiving shares. In PUZZLE, agent peers start normal queries after successfully recovering a query message. We must guarantee that there exist a number of agent peers to flood the query for the initiator. For this reason, we are particularly interested in the relationship between the protocol parameters and the amount of qualified query agents. On the other hand, it is obviously useless to query the same content too many times, while this occurs if the number of the qualified query agents is not carefully controlled. Hence, we need to examine the distribution of shares in MOPNETs to guarantee the search scope without too much overhead.

Traffic cost is one of the most important metrics on which network administrators focus their concerns. In our simulation, we count the packets used for anonymous query or normal query flooding as the traffic cost of those procedures.

Response time is the parameter that is of concern for users. We define the response time of a query as the period from when a query is issued until the initiator receives the first query hit from a responder.

Success rate of transactions is the proportion of successfully finished transactions. Such a transaction is a complete query cycle including successful query issuance, reply, confirm, and file downloading.

Security overhead is defined as the cost spent in the encryption and decryption of RSA, AES, and SIDA in PUZZLE.

# 6.2 Methodology

We evaluate PUZZLE by trace-driven simulations. The underlying manet topologies are generated using CMM [33]. The CMM is a recent wireless topology generating tool, which is able to simulate both mobile scenarios and social network features in manets. In our simulation, we simulate a 50 km  50 km area composed of 10,000 nodes. The initialized positions of peers are generated using CMM, and all peers self-organize into a manet. Over the manet, we build a MOPNET overlay, and the topologies of this overlay are obtained from the DSS Clip2 trace [34]. We predefine the speed of each peer through CMM to enable the mobility. The speed of the nodes are randomly generated following the uniform distribution in the range $1 \sim 6 \mathrm { m } / \mathrm { s } .$ . At any given second, there might be a number of peers moving out of the area tested and new nodes joining or introduced. In the tested area, an ACTIVE\_ROUTE\_TIME-OUT (ART) is set to 3 seconds for each link between two communicating nodes [27]. In our simulation, ART is a constant value that reflects how long a route is kept in the routing table of a node after the last transmission of a packet on that route. To simulate the query cycle, a peer is randomly chosen as the sender, and the potential responders that hold the targeted file are located according to a Zipf distribution [35].

![](images/c6149a783c84e66948630dc88858c1b8852e390e6fc8097de538d3835dc3f786.jpg)



Fig. 10. Number of agent peers versus threshold ratio.   
![](images/78db7e9bb988647b13a1c698a1fcaa600c545d23a9d625f77ad44fa709155922.jpg)



Fig. 11. Number of agent peers versus flooding probability.

We also run the crypto software kits on a PDA, Dopod 830. We find that the average processing speed of a 1,024-bit RSA is 71.4 milliseconds per decryption or signature generation and 5.1 milliseconds per encryption or signature verification. We also obtain 63.8 Mbps as the AES speed and 13.1 Mbps as the SHA-1 speed.

In MOPNETs, peers frequently join and leave. We simulate the dynamic peer changes by assigning a lifetime in seconds to every peer. The average of this value is 600 seconds [36]. The lifetime decrements by one after each passing second. When a peer’s lifetime reaches zero, it leaves in the following second. After a certain number of peers leave the network, we randomly introduce the same number of peers to the MOPNET.

# 6.3 Results

The redundant agent degree in PUZZLE is relevant to the number of agent peers and the number of peers receiving shares. The result is mainly dependent on the average flooding probability $p ,$ the threshold ratio $t / n$ of SIDA. To guarantee that enough agent peers are involved in a share query, an initiator has two options: 1) increasing the flooding probability $p$ and 2) decreasing the threshold ratio $t / n .$ . Increasing $p$ is effective but may incur too much traffic overhead. On the other hand, for a given ðt; nÞ SSS or SIDA, increasing the ratio of $t / n$ requires more shares to recover the original query, which potentially decreases the number of agent peers. In our simulation, we record the number of agent peers using different threshold ratios $t / n$ or flooding probabilities $p .$ Figs. 10 and 11 plot the results and indicate that in most cases, the flooding probability $p$ can be less than 0.5, and $t / n$ is greater than 0.5. In a real MOPNET, it is fairly easy to adjust these two parameters for specific requirements. Our strategy is to minimize $p$ and maximize $t / { \bar { n } } ,$ , in order to generate traffic overload as little as possible for share flooding while guaranteeing that there are sufficient anonymous agents in MOPNETs. To do so, we need to comprehensively select the proper $p$ and $t / n$ according to the share distribution and traffic cost.

We then discuss the impact of $p$ and $t / n$ on the share distribution. Each query cycle produces a different share distribution in different average flooding probabilities. After running 1,000 query cycles, we show typical distributions of the shares in the MOPNET. It is shown that raising the flooding probability or lowering the threshold ratio both lead to an increment in query scope. We choose two nodes whose IDs are 273 and 258. They have 11 neighbors in the topology. Figs. 12 and 13 compare their share distributions with different flooding probabilities. Our experimental results show that most distributions of shares about the probability follow binomial distributions, as illustrated in Figs. 12 and 13.

![](images/75cb1da1caedc508cd0123818d6860b09eb8ab2b12eaa7abbdff5c6492b9f543.jpg)



(a)

![](images/125d4b017bf0d2488a6cdc3e2227cf372ce23c44f67733d6fc8846c3ee3d57ee.jpg)



Fig. 12. Share distribution of node 273. (a) The number of distinct peers with shares from zero to five. (b) The number of distinct peers with shares from 6 to 11.

![](images/c1f561932894514ac1833a5f9b196a289bbb937a3e59f956c5200142b4eaba87.jpg)



(a)

![](images/d78ff5a5a2bb8978e04664c07e67ef4b584523a8b232b2f55d1d21f46eddb2d5.jpg)



(b)

Fig. 13. Share distribution of node 258. (a) The number of distinct peers with shares from zero to five. (b) The number of distinct peers with shares from 6 to 11.   
![](images/6981d38930a3b46ddb78311dce8d1c0f58b3c82fa1ba75be5a506fe20a4306bf.jpg)



(a)

![](images/c4c62dae8c8d1980c95d8549efe547e4afc33db47211c32414199b0d0904a7f0.jpg)



(b)   
Fig. 14. Traffic cost. (a) Traffic cost caused by 3-11 shares. (b) Traffic cost caused by 13-19 shares.

The results show that the optimal threshold ratio of $t / n$ in the $( t , n )$ SIDA approximately approaches $( 1 - p )$ , where $p$ is the average flooding probability. In this scenario, PUZZLE can guarantee enough agent peers (at least one but no more than 10; see Figs. 10 and 11) and limit the traffic cost to no larger than the normal query flooding. PUZZLE allows peers to flexibly choose the threshold to balance the trade-off between the number of agent peers and the traffic cost. We may enlarge the number of agent peers and search scopes by increasing $p .$ However, it is hard to make the query scalable by allowing all peers arbitrarily to choose their individual $p .$ Indeed, the traffic cost added by PUZZLE is mainly caused by share flooding. We show the average traffic cost of share flooding in Fig. 14. It is obvious that the more the shares are split, the higher the traffic cost is. In PUZZLE, either a low $p$ combined with a low $t / n$ or a high $p$ with a high $t / n$ have the same effect in generating the same number of agent peers. In Fig. $^ { 1 4 , }$ w e also compare the traffic cost of PUZZLE using different settings with that of normal flooding. Based on the results shown in Figs. 10, 11, 12, 13, and 14, we constrain p within 0.5 such that enough agent peers are obtained at a scalable traffic cost level.

Fig. 15 plots the response time of PUZZLE. In this experiment, the $t / n$ is $0 . 7 ,$ and the $p$ is 0.3. We see that the response time of PUZZLE is about twice as much as that of normal flooding queries, while onion-routing-based schemes are about three times as much. There are two reasons why PUZZLE outperforms onion-routing-based schemes in terms of response time. First, the path failure of onion-routing-based schemes causes a large number of retransmission in MOPNETs, which enlarges the end-to-end delay in message delivery. Second, the middle peers in onion paths are randomly selected by initiators. The onion path would be tremendously longer than the shortest path between two communicating nodes, for example, the initiator and its agent peer. In contrast, the agent peers are placed on exactly the shortest path between the initiator and agent peer. PUZZLE also obtains more than one agent peer, so the probability of agent peers being on the shortest path between the initiator and responder is higher than that of the onion-routing-based schemes.

![](images/482d27cb53ca23018fd89f7b6ac1ab2068429e2ae988b8195cff1952a3a4ae7c.jpg)



Fig. 15. Response time comparison.

![](images/6ec20187c0bfa97ae726938a21a97c67908402db2a6ecd81f4bca326afb3f324.jpg)



Fig. 16. Reliability comparison.   
![](images/3e4591bf5b6b1d257881afe55063e2fa7fc109e118404c9d869de03056771313.jpg)



Fig. 17. Under free-riding attacks.   
![](images/cc7278a33f93e64391b4f8bb8dce68621fb753c08e52ab5949e58705755c0825.jpg)



Fig. 18. Under active attacks.

Evaluated by using the success rate of transactions, PUZZLE performs much better than the path-based approaches. We compare the PUZZLE and pure-onionrouting-based query cycles in Fig. 16. The dynamic rate reflects the variety of links caused by peers’ mobility in MOPNETs. We can see that the manet’s dynamics incur a significant impact on the success rate of transactions, especially when employing the path-based schemes. We observe the change of success rate of transactions at different distances in terms of hops between the initiator and responder. The fixed path may fail at a high probability due to ART expiration, which is mostly caused by the mobility of nodes in MOPNETs. In Fig. 16, the transaction success rate of onion-routing-based schemes degrades sharply when enlarging the dynamic rate of MOPNETs. In contrast, PUZZLE can leverage the redundancy ability to mitigate the dynamic influence. Note that the reliability can be improved by introducing some trusted and stable nodes into MOPNETs. This definitely incurs tremendous management overhead and is not suitable for the highly dynamic and distributed MOPNETs.

We also investigate the reliability of PUZZLE under unreliable manet environments. We introduce both selfish and malicious peers to degrade the reliability of MOPNETs. Their attacks are conducted under two scenarios. In threat A, the selfish peers, which are named free riders, simply drop the shares and query packets passing through them. While in threat B, malicious peers start active attacks, including hijacking, forging, or dropping all packets passing through them. In this experiment, we consider both of the attacks above.

At the beginning of each scenario, all peers work as a “good” peer. With an increase in the number of malicious peers, the success rate decreases correspondingly. In this experiment, we set the dynamic rate of MOPNETs as 0.1, and the average distance between the initiator and responder is 10 hops. We observed the impact of attacks from selfish and malicious peers to the success rate of the transactions in Figs. 17 and 18. Our experiment result shows that PUZZLE defends against most passive attacks and active attacks before the proportion of malicious peers reaches 60 percent.

The main security process of PUZZLE includes share distribution and the reconstruction procedure, RSA encryption and decryption, and AES encryption and decryption. If the average number of agent peers is m and the average length of an onion path is r, we show the number of security related operations among relevant peers in a complete search procedure in Table 1. We can see that PUZZLE only needs a small number of security-related operations, which incur a very low security overhead.

# 7 CONCLUSIONS

We propose a mutual anonymity protocol, called PUZZLE, for mobile P2P (MOPNET) systems. PUZZLE mainly utilizes the SSS scheme and secure IDA to anonymize query issuance and file downloading. We evaluate PUZZLE by comprehensive trace-driven simulations. Compared with existing path-based designs, PUZZLE achieves mutual anonymity in MOPNETs with a higher degree of anonymity and lower cryptographic processing overhead.

TABLE 1 Major Security Processes with Different Algorithms in PUZZLE 

<table><tr><td colspan="2">SIDA</td><td colspan="2">RSA</td><td colspan="2">AES</td></tr><tr><td>Distribution</td><td>Reconstruction</td><td>Encryption</td><td>Decryption</td><td>Encryption</td><td>Decryption</td></tr><tr><td>m+2</td><td>2m+1</td><td>2r+1</td><td>2r+1</td><td>2</td><td>2</td></tr></table>

# ACKNOWLEDGMENTS

This research was supported in part by the National High Technology Research and Development Program of China (863 Program) under Grant 2007AA01Z180, NSF China Key Project 60736016, Hong Kong RGC Grants HKUST6152/06E and N\_HKUST614/07, and HKUST Nansha Research Fund NRC06/07.EG01.

# REFERENCES

[1] JXTA, http://www.jxta.org/, 2007.   
[2] O. Wolfson, B. Xu, H. Yin, and H. Cao, “Search-and-Discover in Mobile P2P Network Databases,” Proc. 26th Int’l Conf. Distributed Computing Systems (ICDCS), 2006.   
[3] O. Wolfson, B. Xu, H. Yin, and H. Cao, “Searching Local Information in Mobile Databases,” Proc. 22nd Int’l Conf. Data Eng. (ICDE), 2006.   
[4] Anonymity, http://freehaven.net/anonbib/topic.html, 2007.   
[5] M. Freedman and R. Morris, “Tarzan: A Peer-to-Peer Anonymizing Network Layer,” Proc. Ninth ACM Conf. Computer and Comm. Security (CCS), 2002.   
[6] M. Gruteser and D. Grunwald, “Anonymous Usage of Location-Based Services through Spatial and Temporal Cloaking,” Proc. First ACM Int’l Conf. Mobile Systems, Applications, and Services (MobiSys), 2003.   
[7] A.R. Beresford and F. Stajano, “Location Privacy in Pervasive Computing,” IEEE Pervasive Computing, vol. 2, pp. 46-55, 2003.   
[8] J. Kong and X. Hong, “ANODR: Anonymous on Demand Routing with Untraceable Routes for Mobile Ad-Hoc Networks,” Proc. ACM MobiHoc, 2003.   
[9] H. Choi, W. Enck, J. Shin, P. McDaniel, and T.F.L. Porta, “ASR: Anonymous and Secure Reporting of Traffic Forwarding Activity in Mobile Ad Hoc Networks,” Technical Report NAS-TR-0034-2006, Dept. Computer Science and Eng., Pennsylvania State Univ., 2006.   
[10] Y. Zhang, W. Liu, and W. Lou, “Anonymous Communications in Mobile Ad Hoc Networks,” Proc. IEEE INFOCOM, 2005.   
[11] D. Chaum, “Untraceable Electronic Mail Return Addresses, and Digital Pseudonyms,” Comm. ACM, vol. 24, pp. 84-90, 1981.   
[12] D. Goldschlag, M. Reed, and P. Syverson, “Onion Routing,” Comm. ACM, vol. 42, pp. 39-41, 1999.   
[13] M.K. Wright, M. Adler, B.N. Levine, and C. Shields, “The Predecessor Attack: An Analysis of a Threat to Anonymous Communications Systems,” ACM Trans. Information and System Security, vol. 7, pp. 489-522, 2004.   
[14] A. Shamir, “How to Share a Secret,” Comm. ACM, vol. 22, pp. 612-613, 1979.   
[15] M.O. Rabin, “Efficient Dispersal of Information for Security, Load Balancing, and Fault Tolerance,” J. ACM, vol. 36, pp. 335-348, 1989.   
[16] A. Back, I. Goldberg, and A. Shostack, “Freedom Systems 2.1 Security Issues and Analysis,” white paper, Zero Knowledge Systems, Inc., 2001.   
[17] R. Dingledine, N. Mathewson, and P. Syverson, “Tor: The Second-Generation Onion Router,” Proc. 13th Usenix Security Symp., 2004.   
[18] M. Rennhard and B. Plattner, “Introducing MorphMix: Peer-to-Peer Based Anonymous Internet Usage with Collusion Detection,” Proc. ACM Workshop Privacy in the Electronic Soc., 2002.   
[19] C. Shields and B.N. Levine, “A Protocol for Anonymous Communication over the Internet,” Proc. Seventh ACM Conf. Computer and Comm. Security (CCS), 2000.   
[20] B. Zhu, S. Jajodia, M.S. Kankanhalli, F. Bao, and R.H. Deng, “An Anonymous Routing Protocol with the Local-Repair Mechanism for Mobile Ad Hoc Networks,” Proc. Third Ann. IEEE Conf. Sensor, Mesh and Ad Hoc Comm. and Networks (SECON), 2006.

[21] R. Sherwood, B. Bhattacharjee, and A. Srinivasan, “P5: A Protocol for Scalable Anonymous Communication,” Proc. IEEE Symp. Security and Privacy, 2002.   
[22] V. Scarlata, B.N. Levine, and C. Shields, “Responder Anonymity and Anonymous Peer-to-Peer File Sharing,” Proc. IEEE Ninth Int’l Conf. Network Protocols (ICNP), 2001.   
[23] M.K. Reiter and A.D. Rubin, “Crowds: Anonymity for Web Transactions,” ACM Trans. Information and System Security, vol. 1, pp. 66-92, 1998.   
[24] J. Deng, R. Han, and S. Mishra, “Intrusion Tolerance and Anti-Traffic Analysis Strategies for Wireless Sensor Networks,” Proc. IEEE Int’l Conf. Dependable Systems and Networks (DSN), 2004.   
[25] P. Kamat, Y. Zhang, W. Trappe, and C. Ozturk, “Enhancing Source-Location Privacy in Sensor Network Routing,” Proc. 25th Int’l Conf. Distributed Computing Systems (ICDCS), 2005.   
[26] H. Krawczyk, “Secret Sharing Made Short,” Proc. 13th Ann. Int’l Cryptology Conf. Advances in Cryptology, 1994.   
[27] C.E. Perkins, E.M. Royer, and S.R. Das, Ad Hoc On-Demand Distance Vector Routing, IETF RFC 3561, 2003.   
[28] M. Wright, M. Adler, B.N. Levine, and C. Shields, “An Analysis of the Degradation of Anonymous Protocols,” Proc. Ninth Symp. Network and Distributed System Security (NDSS), 2002.   
[29] H. Krawczyk, “Distributed Fingerprints and Secure Information Dispersal,” Proc. 12th Ann. ACM Symp. Principles of Distributed Computing (PODC), 1993.   
[30] O. Goldreich, “A Note on Computational Indistinguishability,” Information Processing Letters, vol. 34, pp. 277-281, 1990.   
[31] Y. Liu, L. Xiao, X. Liu, M. Ni, and X. Zhang, “Location Awareness in Unstructured Peer-to-Peer Systems,” IEEE Trans. Parallel and Distributed Systems, vol. 16, pp. 163-174, Feb. 2005.   
[32] W.W. Terpstra, J. Kangasharju, C. Leng, and A.P. Buchmann, “BubbleStorm: Resilient, Probabilistic, and Exhaustive Peer-to-Peer Search,” Proc. ACM SIGCOMM, 2007.   
[33] M. Musolesi and C. Mascolo, “A Community Based Mobility Model for Ad Hoc Network Research,” Proc. ACM/SIGMOBILE Int’l Workshop Multi-Hop Ad-Hoc Networks: From Theory to Reality, 2006.   
[34] DSS Clip2 Trace, http://dss.clip2.com, 2005.   
[35] L. Breslau, P. Cao, L. Fan, G. Phillips, and S. Shenker, “Web Caching and Zipf-Like Distributions: Evidence and Implications,” Proc. IEEE INFOCOM, 1999.   
[36] S. Sen and J. Wang, “Analyzing Peer-to-Peer Traffic across Large Networks,” ACM/IEEE Trans. Networking, vol. 12, pp. 219-232, 2004.

![](images/0b9bcf35e88f7ebd4177caacb2ed6ebf0e9d86f285e9f45c0caca121d0f1857b.jpg)



Jinsong Han received the BS degree in computer science from the Shandong University of Technology, China, in 1997, the MEng degree in computer science from Shandong University, China, in 2000, and the PhD degree in computer science and engineering from the Hong Kong University of Science and Technology, in 2007. He is now a postdoctoral fellow in the Department of Computer Science and Engineering, Hong Kong University of Science and Technol-

ogy. His research interests include peer-to-peer computing, anonymity, network security, pervasive computing, and high-speed networking. He is a member of the IEEE Computer Society and the ACM.

![](images/a504b8771bc76a552b290714841061cdbeb843af45be0443047fd7c393fe5c5d.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MA degree from Beijing Foreign Studies University, China, in 1997, and the MS and the PhD degree in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is now an assistant professor in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research inter-

ests include peer-to-peer computing, pervasive computing, and sensor networks. He is a senior member of the IEEE Computer Society and a member of the ACM.