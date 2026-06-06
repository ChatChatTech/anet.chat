# Mutual anonymous overlay multicast

Li Xiaoa,∗, Yunhao Liub, Wenjun Guc , Dong Xuanc , Xiaomei Liua

aDepartment of Computer Science and Engineering, Michigan State University, East Lansing, MI 48824, USA bDepartment of Computer Science, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong cDepartment of Computer Science and Engineering, Ohio State University, Columbus, OH 43210, USA

Received 17 December 2005; received in revised form 31 March 2006; accepted 10 April 2006

Available online 12 June 2006

# Abstract

Multicast services are demanded by a variety of applications. Many applications require anonymity during their communication. However, there has been very little work on anonymous multicasting and such services are not available yet. Due to the fundamental differences between multicast and unicast, the solutions proposed for anonymity in unicast communications cannot be directly applied to multicast applications. In this paper we define the anonymous multicast system, and propose a mutual anonymous multicast (MAM) protocol including the design of a unicast mutual anonymity protocol and construction and optimization of an anonymous multicast tree. MAM is self-organizing and completely distributed. We define the attack model in an anonymous multicast system and analyze the anonymity degree. We also evaluate the performance of MAM by comprehensive simulations.

© 2006 Elsevier Inc. All rights reserved.

Keywords: Multicast mutual anonymity; Explicit tree; NP-hard; Relative resource usage; Average worst-case delay

# 1. Introduction

It is well known that multicast services are demanded by a variety of applications, e.g., video conferencing, Internet based education, NASA TV, software updates etc. However, the inability of the Internet to support multicast is patent. In order to alleviate this, multicast services on overlay networks have been proposed [4,6,7,10,11,24,26,30,32,34,35,37] and implemented [9] by the research community. The salient features of overlays include ease of deployment and flexibility. We envision that in the near future, a wide variety of applications will be able to enjoy multicast services on overlay networks. Apart from commercial applications, we believe that government and military organizations will also use such services due to the advantages that multicast has to offer.

It follows to expect that, as multicast services continue to be deployed, existing and future multicast applications will also demand the security features that unicast communications have. Security in multicast communication has been addressed in [5,20,25]. Most of the work here focuses on authentication of the senders and receivers and the efficient distribution of the keys to all legal group members and exclusion of members that leave the group. Our focus here is providing anonymity in multicast communications. Anonymity is an important component of security and is demanded by many applications, especially in critical multicast services like military and emergency applications, where strategic information and critical updates are transmitted to multiple destinations needing anonymity from external observers. Multi-party video conferencing applications carrying classified information will need anonymity from external observers and other members in the group. Large business organizations may have to multicast database updates to many sites for synchronization, and such applications will demand anonymity from rival organizations.

Solutions proposed for anonymity in unicast communications cannot be directly applied to multicast applications. The fundamental difference between multicast and unicast is the concept of a group in multicast. There is a relationship among multiple nodes including the source(s) and destination(s) that are correlated, unlike in unicast where only one sender and one receiver are communicating. Due to the correlation among nodes, there are special challenges in achieving anonymity in multicast:

(1) The anonymity semantics in multicast are different from those in unicast. For sender anonymity, the sender needs to hide not only from one receiver, but from a subset of, or all the receivers. In receiver anonymity, the receiver may need to hide not only from the sender, but also from other receiver(s). There is a special issue in anonymity in multicast called group anonymity, where the presence of the group is not disclosed to outsiders. The involvement of multiple members makes it very difficult to hide the existence of the group. (2) Multicast services naturally need the existence of a tree. Exposing this tree itself will compromise the degree of anonymity. In contrast, in unicast, the path from a sender to a receiver is much easier to hide. (3) Membership management is a challenging issue in multicast. Member joining and leaving makes anonymity difficult. (4) There are other inherent challenges for secure multicast services such as group key management.

There has been very little work on anonymous multicast. Simple solutions [17,33] have been proposed to achieve multicast anonymity by inserting some proxies (called SAM) into the tree. However, this tree may itself not be efficient. The authors attempt to provide sender anonymity and receiver anonymity. They do not address issues of providing mutual and group anonymity.

In this paper, we use an overlay solution and propose the mutual anonymous multicast (MAM) protocol, including the design of a unicast mutual anonymity protocol, and construction and optimization of an anonymous multicast tree. MAM is selforganizing and completely distributed. The main contributions of this paper are as follows:

• We define different types of anonymity in an anonymous multicast system, and show the rationale of our focus on multicast mutual anonymity.   
• We propose the MAM protocol and address the critical issues in this protocol, which include an efficient and robust unicast initiator anonymity protocol, an efficient unicast mutual anonymity protocol, and an effective anonymous multicast construction approach. The self-organized and completely distributed design of MAM can efficiently realize mutual anonymity in overlay multicast systems.   
We define the attack model to an anonymous multicast system, and theoretically analyze the anonymity degree of the MAM protocol.   
By comprehensive simulation study, we show the effectiveness of MAM in a dynamic environment.

The rest of this paper is organized as follows. Section 2 discusses related work. Section 3 presents the MAM protocol design. Section 4 analyzes anonymity degree. Section 5 evaluates the performance of the MAM protocol. We conclude the work in Section 6.

# 2. Related work

We introduce the related work in this section. We will focus on the work on (1) basic multicast (no security and anonymity), (2) anonymous unicast, and (3) multicast anonymity.

# 2.1. Basic multicast

Originally, multicast research was focused on network layer. However, no real multicast service has been provided at the network layer. The main issues in network-layer multicast are deployment and scalability issues. Recently, the focus has been expanded to include application-layer multicast [4,6,7,10,11,21,24,26,30,32,35,37]. It is well believed that application-layer solutions provide much flexibility in design and implementation. Overlays are increasingly being used to deploy network services for different applications [26] since they have the advantages of being easy to implement and flexible in adapting to dynamic underlying networks. Popular applications on overlay include routing and multicast overlays [3], QoS overlays, scalable object location, scalable event propagation, wireless and mobile systems, and cluster-based overlays constructed among sensor nodes [19].

# 2.2. Anonymous unicast

Overlay anonymous unicast have been reported, such as in Tarzan [13] and our work [36]. The essential techniques to achieve unicast anonymity can be classified into the following categories: routing, addressing, layered encryption, and traffic covering. In the routing approach, there can be either indirect forwarding, i.e. the use of intermediate nodes (forwarders) to hide correlation between the sender and the receiver [8,22,31], or flooding [29]. In addressing, it can be implicit, i.e. the address contains no information either on the actual location of the addressee or on the physical reachability of the addressee [15,16], or explicit, i.e. the address contains information that can be used in a straightforward manner to route a message to the addressee [33]. Layered encryption is often used in anonymity protocols [8,31]. Traffic covering can prevent traffic timing analysis [14,18]. These techniques often work together to achieve anonymity. For example, indirect forwarding needs layered encryption to encrypt the identities of forwarders. Flooding needs implicit address. Flooding is too costly (not efficient) but it is simple and can be used for local anonymity. It can also be used to achieve distributed receiver anonymity. It can be combined with indirect forwarding to achieve scalability and efficiency.

There are two ways to choose forwarders in the indirect forwarding approaches. It can be in a centralized fashion, such as Onion [31], or a distributed fashion, such as Crowds [27] and Tor [12]. In the centralized fashion, some centers (the sender or receiver) choose the whole list of forwarders and use layered encryption techniques to encrypt them. The list of forwarders will be piggybacked in the message. The problem is the center needs to know the global network information, which is not scalable in a large-scale network. In the distributed fashion, during the message forwarding, the next-hop forwarder is decided by the current forwarder (there are certainly some variations). The mechanism is scalable and can be applied in sender anonymity. However, it is hard, if not impossible, for the latter to be used in receiver anonymity.

# 2.3. Anonymous multicast

Little work [17,33] has reported on anonymous multicasting. Anonymous multicast communication service is not available yet. Authors in [33] proposed the use of a proxy, called the SAM server, to hide some receivers. The main idea is first to add a SAM server as a normal node into a multicast tree, then attach receivers to the SAM server so that they are hidden by the server from other members. The concept of SAM server is a kind of extension to proxy or mixer in unicast. There are some drawbacks of this system. If there are multiple receivers attached to a SAM server, there exists another multicast anonymity problem among these receivers. The SAM server can be a target of attack. Also, the SAM servers should be trusted. Some types of multicast anonymity have not been addressed, such as multicast mutual anonymity and multicast group anonymity. Preliminary results of our proposed overlay anonymous multicast protocol have been presented in [34].

# 3. MAM protocol

In this section, we define multicast anonymity and present the design of MAM protocol.

# 3.1. Definition of multicast mutual anonymity

Before we give the definition of anonymous multicast, we specify roles of nodes in a multicast system. Nodes that belong to the multicast group are called group members. We label a node as a sender if it sends a multicast message to other nodes that are group members. The other group members that receive this message are called receivers. Note that we assume every node could be a sender and a receiver in the service. Nodes that are neither senders nor receivers are called outsiders to the group.

Definition 1 (Multicast mutual anonymity). Here a set of members desire to be hidden from others. Members in such a set need to achieve mutual anonymity from each other. Such a set can be a pair, such as the sender and a receiver; or one receiver and another receiver. The set also can be multiple members and may even include all members (i.e. complete anonymity).

Multicast mutual anonymity can cover multicast sender anonymity (hide the sender’s identity) and receiver anonymity (hide one or more receivers’ identities). Of course multicast sender anonymity and receiver anonymity can be achieved by simpler protocols than that for multicast mutual anonymity. Multicast mutual anonymity is the focus of this paper. Another type of multicast anonymity is group anonymity, which hides the existence of a multicast group session from all outsiders. Traffic covering approaches can be used to achieve multicast group anonymity, which is beyond the scope of this paper.

We define three types of nodes in a MAM system.

Anonymous member nodes, AM nodes in short, are the member nodes whose identities need to be hidden from all member/non-member nodes.

Non-anonymous member nodes, NM nodes in short, are the member nodes that need not be hidden from others.

Middle outsiders, MO nodes in short, are the nodes that do not need to receive any packets from the source for their own purpose, but provide packet forwarding service for the multicast system. If needed, MO nodes are invited by the system for improving the overall efficiency. They do not hide their identity.

One naïve approach to achieve anonymous multicast services is to treat multicast as a set of unicast communications from the sender to the individual receivers and then directly apply one of the unicast anonymity schemes discussed in Section 2. While the approach is simple, it is inefficient. To achieve high efficiency and reduce the redundancy of multicast message transmissions among multiple receivers, multicast always relies on some structure to deliver a message. The structure is usually a tree, and the tree can be source- or core-based. Unicast is a special case of multicast, where the structure is a path. The potential solution to anonymous multicast must center on the concept of the tree. We believe it is the main difference and also the source of challenges in achieving anonymity in multicast compared with anonymity in unicast.

# 3.2. Design consideration of anonymous multicast systems

We need to consider both multicast tree efficiency and anonymity degree in the design of a multicast mutual anonymity protocol. An example is shown in Fig. 1, in which we can see that an optimal multicast tree without (Fig. 1(a)) and with (Fig. 1(c)) anonymity concern are very different, where the cost of an AM–NM connection is 6 times that of an NM–NM connection and the cost of an AM–AM connection is 15 times that of an NM–NM connection. We have the following objectives in designing MAM protocol:

(1) High mutual anonymity degree: the identity of each anonymous node (AM), whether a sender or a receiver, in a multicast group should be hidden from all group members and outsiders.   
(2) Delivery efficiency: a smart tree with consideration of anonymity is built with low average delay and low resource usage.   
(3) Distributed fashion: the construction of the anonymous multicast system must be completely self-organizing and in a distributed manner. No trusted central server is involved. Further, MAM must be robust in a dynamic overlay environment.   
(4) Self-optimization: MAM will allow all the nodes to incrementally optimize the system, by reconstructing the tree and inviting more middle outsiders (MO nodes) to improve the overall performance.

Here is the basic idea of MAM. A set of NM nodes form an efficient multicast tree in terms of bandwidth and/or delay. Nodes of the tree are degree-bounded. Early AM nodes connect unsaturated NM nodes, or MO nodes (if MO nodes have been invited), on the tree using a unicast initiator anonymity protocol. When there is no unsaturated NM node in the tree, a joining

![](images/9e3cd6c13daa2b07de04e5f47d6b16808c5253d4fff6d8d96193594050520b1a.jpg)



Fig. 1. An example of multicast tree with and without anonymity concern.

AM node will connect to another unsaturated AM node in the tree using a unicast mutual anonymity protocol. If there are too many AM nodes in the system, MO nodes will be invited to join the multicast tree so that the new AM node can connect with the MO node using a unicast anonymity protocol. When to invite MO nodes depends on the cost ratio of unicast initiator anonymity protocol and unicast mutual anonymity protocol, and the ratio of AM nodes in a system. The pseudo code for a joining node P is as below.

P contacts a bootstrapping server and gets a list of members;

P contacts one active member and gets a full list of members;

If (P is an NM node)

make a direct connection to an unsaturated NM node;

If (P is an AM node)

If (P can find unsaturated NM members)

make AM–NM connections with few unsaturated NMs;

else

If (P can find unsaturated AM members)

make AM–AM connections with several AMs;

If (# of AMs/# of NMs > IT)

Invite MO nodes;

if (timeout)

tree optimization;

Therefore, there are mainly the following three key issues to be addressed in MAM: a unicast initiator anonymity protocol for AM–NM connections, a unicast mutual anonymity protocol for AM–AM connections, and anonymous multicast tree construction and optimization, which are discussed in detail in following subsections.

# 3.3. Unicast initiator anonymity protocol design

The idea of Onion and a reverse Onion can be used to achieve initiator anonymity for bi- directional communication. Since an AM node has more than one choice for NM nodes to make AM–NM connections with, we optimize the Onion protocol as follows to keep both strong anonymity and robustness.

In the improved protocol for AM–NM connection, a $R e \mathrm { - }$ mailer (a reverse Onion) is generated by the AM node for the NM node to anonymously send messages to the AM node. In the AM → NM communication direction, the AM node uses an approach similar to Crowds and Tor, in which each middle node in the path can make a decision to forward the message to another middle node or the NM node. This approach is more robust than Onion in the case of middle node failure. In order to simplify the protocol description, we use S to denote the AM node, and use R to denote the NM node, as below. Note that S knows R’s identity, but R does not know anything about S. Since this connection is initiated by S, we also label S as the initiator. In the rest of the paper, we use {M}K to indicate that M is encrypted with the key K. $K p _ { + }$ denotes $p \mathrm { ^ { * } s }$ public key and $K p _ { - }$ − denotes $p \mathrm { ^ { \circ } s }$ private key.

Step 1: The node S first generates m, the number of middle nodes in the Remailer. S then randomly selects a list of m nodes, p0, p1, p2, . . . , pm−1 to form a Remailer. The lifetime of this one- time Remailer in seconds is also generated. The Remailer is built with S as the last member of the path and with $p _ { i }$ in the middle. It is of the form:

$$
\{p _ {m - 1}, \{p _ {(m - 2)}, \dots \{p _ {0}, \{S \} K p _ {0 +} \dots \}
$$

$$
K p _ {(m - 2) +} \} K p _ {(m - 1) +} \} K _ {R +}.
$$

Step 2: S randomly selects a node, $q _ { 0 } .$ , sends it the message: $S \to q _ { 0 } : \{ R _ { \ O } \}$ , {Remailer, lifetime} $K _ { R + } \}$ .

Step 3: A peer $q _ { i }$ can elect itself to act as a deliver with a predefined forwarding probability h. If $q _ { i }$ is self-elected, the message {Remailer, lifetime} $K _ { R + }$ will be delivered to the non-anonymous member node R directly. Otherwise, $q _ { i }$ will randomly select another node, $q _ { i + 1 }$ and forward the message {R, {Remailer, lifetime} $\langle K _ { R + } \}$ to it.

Step 4: On receiving the message {Remailer, lifetime} $K _ { R + }$ R uses its private key to decrypt the encrypted message.

Step 5: R generates a symmetric key K, and encrypts the multicast packet f with K. R then encrypts K with its private key. It keeps sending multicast packets with the format as below through the Remailer to S:

$$
R \to S: \{f \} K, \{K \} K _ {R -}.
$$

Step 6: S uses R’s public key to decrypt the symmetric key $K ,$ and uses K to decrypt the content encrypted by K.

At any time, a node R may have one or more Remailers. It will check the age and the expected lifetime for each Remailer periodically and delete obsolete Remailers. Each live Remailer corresponds to one AM node. Each AM node may connect with different NM nodes with the same or different Remailers for two reasons: increasing the difficulty for a NM node to guess the identity of the AM node, and providing multiple paths to the AM node in case of failure of any middle nodes in a Remailer. Two many Remailers for the same AM node will increase overhead, which can be adjusted by setting shorter lifetimes for the Remailers.

# 3.4. A unicast mutual anonymity protocol design

When a joining AM node cannot find an unsaturated NM node in the tree, one option for him is to connect to another unsaturated AM node in the tree using a unicast mutual anonymity protocol. Most unicast mutual anonymity protocols [13,27,29,31,36] were proposed for file sharing systems and may not be applicable here directly because of their low efficiency. Therefore, we need to design a new unicast mutual anonymity protocol. Designing an efficient mutual anonymity protocol is difficult, but is possible here by utilizing the mechanism of MO node invitation.

We can use IP addresses to identify NM/MO nodes because they do not need to be anonymous. Instead, each AM node randomly selects an 18 byte value using a given algorithm to ensure its uniqueness when it joins the system. Note that AM nodes may change their $\mathrm { I D } _ { \mathrm { A M } }$ at any time for anonymity consideration. At the time of its joining, each AM node is bounded with one or multiple MO nodes, which means an AM node sends Remailers to its bounded MO nodes, and its $\mathrm { I D } _ { \mathrm { A M } }$ and bounded MO nodes’ IP addresses, $\mathrm { \dot { \Omega } . g . \ I D _ { A M } \mathrm { - I P _ { M O _ { 1 } } } }$ , $\begin{array} { r } { \ldots , \mathrm { I D } _ { \mathrm { A M } ^ { - } } \mathrm { I P } _ { \mathrm { M O } _ { i } } , \ldots . } \end{array}$ , will be kept in other NM nodes.

When an AM node $\mathbf { \Gamma } ( \mathbf { A M } _ { 1 } )$ decides to make a connection to another AM node $\left( \mathsf { A M } _ { 2 } \right)$ , it will select one of its bounded MO nodes $( \mathrm { M O } _ { i } )$ to establish a connection with one of $\mathbf { A M } _ { 2 } \mathbf { \ ' } _ { \mathbf { S } }$ bounded nodes $( \mathbf { M O } _ { j } )$ . The connection between $\mathbf { A M } _ { 1 }$ and MOi, and the connection between $\mathrm { A M } _ { 2 }$ and $\mathbf { M O } _ { j }$ , are established by the unicast initiator anonymous protocol introduced in the previous section. A connection of $\mathrm { I D } _ { \mathrm { A M _ { 1 } } } \mathrm { - I P _ { M O _ { i } } - I P _ { M O _ { j } } - I D _ { A M _ { 2 } } }$ is therefore established to achieve mutual anonymity between $\mathbf { A M } _ { 1 }$ and $\mathbf { A M } _ { 2 }$ .

# 3.5. Anonymous multicast tree construction

Many previous studies have intensively studied how to build an efficient overlay and optimize a random overlay, so we will not focus on this issue in this paper. We use an idea similar to the Narada protocol [11] to build our multicast overlay among NM/MO nodes. The basic idea of Narada is to construct an efficient connected mesh first. Narada then constructs shortest path spanning trees of the mesh, each tree rooted at the corresponding source using well-known routing algorithms.

As in Narada, every NM node and invited MO node has a full list of all the members. A joining node is able to get a list of group members (not necessarily complete or accurate) by an out-of- band bootstrap mechanism, and randomly selects several unsaturated members to connect with. If the new joining node is an AM node that needs to hide its identity, it will randomly select one or multiple unsaturated NM/MO nodes forming anonymous connections with them, which is described in Section 3.3. When a node leaves, it will notify its neighbor and this information will be propagated to other group members along the mesh. When a node fails, the failure will be detected locally and delivered to the other group member. In both cases, the parent and the children of this node will know the situation. The parent of this node will stop transfer information to this node and the children of this node will make new connections to other nodes in the tree.

The multicast tree needs to be maintained. All the NM nodes probe their distances with all the other NM nodes and share the information among the overlay, so that every single node has an identical distance table including each pair of the NM nodes. As our design is for small sized systems, maintaining such a list is not difficult. For large-scaled overlay multicast groups, MAM will adopt the membership maintenance mechanism of the original non-anonymous multicast system among NM nodes to solve the scalability problem. For example, NM nodes can choose a list mixed with members on the path from source and a random set of members [9]. The distance between a NM node and an AM node is not available because the AM node is anonymous to NM nodes, but it is also not necessary since the AM node is connected with a NM node via a number of middle nodes, which makes the direct distance between the AM node and the NM node meaningless in optimizing the tree. However, the $\mathrm { I D } _ { \mathrm { A M } } \mathrm { s }$ of the AM nodes can be kept in the NM nodes, and a NM node knows the number of AM nodes that connect with it via anonymous passage but does not know their identities. The optimization of the multicast tree has three faces: (1) the NM nodes periodically probe their neighbors and update their links to optimize the underlying mesh topology; (2) based on the distance information in the distance table, a minimum spanning tree among NM nodes for data transfer is always able to built on the top of the mesh overlay [11]; (3) to guarantee the performance of the multicast tree, each NM node will subtract the number of its connected AM nodes from its bounded degree.

When a joining AM node cannot find an unsaturated NM node in the tree, one option is to connect it to another unsaturated AM node in the tree using a unicast mutual anonymity protocol described in Section 3.4. However, we do not wish to see too many AM–AM mutually anonymous connections for performance reasons. Therefore, in some situations, MAM considers inviting some MO nodes to help by joining the system. We define an invitation threshold (IT). When the ratio of AM nodes to NM/MO is greater than the value of IT, the system will try to invite some MO nodes to join. When MO nodes are invited into the systems, joining AM nodes will have chances to join the tree by making AM–NM connections instead of more expensive AM–AM connections.

# 3.6. Cost and latency of anonymous connections

There is additional cost and latency for multicast systems when we try to provide anonymity to a set of member nodes, and hence it is of great importance to discuss this cost and latency.

We have the following observations on the cost and latency of the above proposed unicast mutual anonymity protocols of MAM.

First, the selection of the number of middle nodes, m, has great impact on the anonymity degree and the cost of the connections. Obviously there is a tradeoff between the anonymity degree and the cost. Specifically, a larger m will result in a higher anonymity degree while incurring larger cost and latency.

Second, the predefined forwarding probability h also partially influences the cost and latency of data delivery in the system. In MAM, for simplicity, we uniformly select the value of h for the peering nodes. In real systems, nodes may select h independently, and the variety of h will improve the anonymity degree provided to the clients.

Third, the average cost of an AM–AM connection is at least two times greater than an AM–NM/MO connection. If we take (1) the dynamic nature of the member nodes and (2) each AM node may use a set of NM/MO and switch some of them, into consideration, the average cost of an AM–AM connection is more than twice of that of an AM–NM/MO connection.

# 4. Anonymity degree analysis

# 4.1. Attack model

We assume that the attacker will break into some overlay nodes that are chosen randomly in one round, and try to figure out who the AM nodes are using the information that he obtains from the broken nodes. We assume the attacker can find the single parent and k children of all the nodes that have been broken. We also assume that the broken node keeps forwarding the packets in the same way as it did before it was broken. We call the parents of all those broken nodes the potential root of a subtree with AM nodes, which is called an implicit tree. The attacker will give each potential root a coefficient that is related with the probability regarded by the attacker as the root of the implicit tree by utilizing the information he obtains from all the broken nodes. A node that is more likely to be the root of the implicit tree has a higher coefficient, which means it is more important than other broken nodes and more prone to further attack.

The objective of the attacker is to use the above coefficients for future attacks, e.g., the attacker can launch a congestion attack on to the potential root(s) to deny the service of as many receivers as possible, or the attacker can launch another break in attack to the potential root(s) to find the identity of the root of the implicit tree. No matter what the next attack is, the attacker will try to attack the node(s) that are more likely to be closer to the root of the implicit tree since he can potentially deny service to more receivers if he launches a congestion attack or has a higher probability to get the identities of all the receivers in the implicit tree if he launches a break in attack.

One thing to be reminded of here is that two broken nodes that are two layers apart can generate a broken tree with a length of three by sharing information with each other. An example is that node A is in the ith layer, while node B is in the (i + 2)th layer. After sharing the parent and children information with each other, node A finds that the parent of node B is actually one of its children, so a three layer broken tree is generated by nodes A and B. In this case, an unbroken node can also be on a broken tree as long as both its parent and at least one of its children are broken. We call node A the head of the broken tree if and only if node A is broken while its parent and grandparent are not broken. Similarly, we call node B the tail of the broken tree if and only if node B is broken while none of its children and grandchildren is broken. If node A is in the ith layer and node B is in the jth layer, we call this broken tree a broken tree with length $j - i + 1$ , which is basically the number of nodes in this broken path. Generally, all the broken nodes can form a broken forest comprised of several broken trees that are subtrees of the implicit tree. We denote the length of a broken tree as the length of the longest broken path in the broken tree.

# 4.2. Anonymity degree analysis

The metric we use to analyze anonymity degree is $P _ { \mathrm { r e v e a l } }$ , which is the probability that the identity of an AM node is revealed. If the AM node itself is broken, this probability is 1, otherwise, we calculate this probability according to a weight. Each node has a weight that stands for how sure the attacker thinks that this node’s parent or one of its children is an AM node. Each node could be the root of a broken tree or the tail of a broken path, which we will define later. We believe the longer the broken tree or the broken path is, the more weight the attacker will give to this node. Our analysis is focused on how to get the weight of each node based on the distribution of the length of the broken tree or broken path.

In this section, we assume the multicast tree structure is a k-nary incomplete tree with L + 1 layers and the root node is at layer 0. Here an incomplete tree means that some receivers are not in the Lth layer. The receivers can be located from the first layer to the Lth layer. We assume in the incomplete tree scenario, each node has either 0 or k children. We introduce the incomplete tree in the hope of achieving better bandwidth efficiency since there is no redundant link in an incomplete tree. Here, we introduce a set of parameters $\{ q _ { i , j } \}$ , which is a value given to each node $p _ { i , j }$ in the tree. We let $q _ { i , j }$ be 1 if node $p _ { i , j }$ is a real node in the tree. We let $q _ { i , j }$ be 0 if it does not exist in the tree. We also assume that the attacker has successfully broken into N nodes in this tree. Since the attacker chooses the nodes randomly for break in attack, the probability of each node in the tree being broken is equal, which is

$$
p _ {\text { broken }} = N \left/ \sum_ {i = 0} ^ {L} \sum_ {j = 1} ^ {k ^ {i}} q _ {i, j} \left. \right.. \tag {1}
$$

We first analyze anonymity degree of AM as a sender and then analyze the anonymity degree of AM as a receiver. If the root of the tree is one of the broken nodes, the attacker has already obtained all the information he needs. Otherwise, there is a probability $P _ { \mathrm { a t t a c k } } ^ { s }$ that the real root will be regarded as the root and may be subject to the next attack. The overall probability that the identity of the root is revealed is shown below,

$$
P _ {\text { reveal }} ^ {s} = P _ {\text { broken }} + (1 - P _ {\text { broken }}) * P _ {\text { attack }} ^ {s}, \tag {2}
$$

$$
p _ {\text { attack }} ^ {s} = \sum_ {j = 1} ^ {k} \left(w _ {1, j} ^ {s} / \sum_ {i = 1} ^ {L} \sum_ {j = 1} ^ {k ^ {i}} w _ {i, j} ^ {s}\right), \tag {3}
$$

$$
w _ {i, j} ^ {s} = \left\{ \begin{array}{l l} 0 & (q _ {i, j} = 0), \\ P _ {\text { broken }} * \left(\sum_ {l = 1} ^ {L} p _ {i, j} ^ {s} (l) * f (l)\right) & (q _ {i, j} = 1, i = 1), \\ P _ {\text { broken }} * (1 - P _ {\text { broken }}) * \left(\sum_ {l = 1} ^ {L} p _ {i, j} ^ {s} (l) * f (l)\right) & (q _ {i, j} = 1, i = 2), \\ P _ {\text { broken }} * (1 - P _ {\text { broken }}) ^ {2} * \left(\sum_ {l = 1} ^ {L} p _ {i, j} ^ {s} (l) * f (l)\right) & (q _ {i, j} = 1, i > 2), \end{array} \right. \tag {4}
$$

where $w _ { i , j } ^ { s }$ is the weight given to node $n _ { i , j }$ (i.e. jth node in ith layer), which is the head of a broken tree; $p _ { i , j } ^ { s } ( l )$ is the probability that the length of the broken tree with node $n _ { i , j }$ as the head is $l ; f ( l )$ is a function that increases when l increases. The exact form of $f ( l )$ depends on the attacker’s policy. We choose $f ( l ) = l$ in this paper.

In an incomplete tree, different nodes at the same layer have different probabilities of being the head of a broken tree of a specific length. A node that has more “deeper” descendant has higher probability of being a head of a long broken tree and vice versa.

Here, $p _ { b c } ( i )$ is the probability that i children have been broken. Similarly, $p _ { b g } ( i )$ is the probability that i grandchildren have been broken. $p _ { i } ( l | b n ~ = ~ j )$ is the probability that the longest broken tree among j trees is of length l, given that j children of a parent, which is in the (i − 1)th layer, have been broken in the ith layer. $p _ { b c } ( i ) , p _ { b g } ( i )$ and $p _ { i } ( l | b n = j )$ can be calculated as:

$$
p _ {b c} (i) = \binom {k} {i} * p _ {\text { broken }} ^ {i} * (1 - p _ {\text { broken }}) ^ {k - i}, \tag {6}
$$

$$
p _ {b g} (i) = \left(\sum_ {n = 1} ^ {k ^ {2}} q _ {i + 2, k ^ {2} j - k ^ {2} + n} i\right) * p _ {\text { broken }} ^ {i}
$$

$$
* (1 - p _ {\text { broken }}) \left(\sum_ {n = 1} ^ {k ^ {2}} q _ {i + 2, k ^ {2} j - k ^ {2} + n}\right) - i, \tag {7}
$$

$$
\begin{array}{l} p _ {i, j} ^ {s} (l | b n = j) \\ = \left\{ \begin{array}{l l} 0 & (l = 0), \\ \sum_ {m = 1} ^ {j} \left(\binom {j} {m} * \overline {{p _ {i , j} ^ {s} (l)}} ^ {m} * \left(\sum_ {n = 1} ^ {l - 1} \overline {{p _ {i , j} ^ {s} (n)}}\right) ^ {j - m}\right) & (l > 0). \end{array} \right. \tag {8} \\ \end{array}
$$

$$
\begin{array}{l} p _ {i, j} ^ {s} (l) = \\ \left\{ \begin{array}{c c} 0 & (q _ {i, j} = 0), \\ 0 & (l \leqslant 0 \text {   or   } l > L), \\ 1 & (q _ {i + 1, k j} = 0, l = 1), \\ (1 - p _ {\text { broken }}) ^ {k + \sum_ {n = 1} ^ {k ^ {2}} q _ {i + 2, k ^ {2} j - k ^ {2} + n}} & (q _ {i + 1, k j} = 1, l = 1), \\ 0 & (q _ {i + 1, k j} = 0, l > 1), \\ \sum_ {n = 1} ^ {k ^ {2}} q _ {i + 2, k ^ {2} j - k ^ {2} + n} & \\ \sum_ {j = 1} ^ {k ^ {2}} (p _ {b g} (j)) & \\ * p _ {i + 2, j} ^ {s} (l - 2 | b n = j)) & (\text { otherwise }). \\ * p _ {b c} (0) + \sum_ {j = 1} ^ {k} (p _ {b c} (j)) & \\ * p _ {i + 1, j} ^ {s} (l - 1 | b n = j)) & \end{array} \right. \tag {5} \\ \end{array}
$$

Here, $\overline { { p _ { i , j } ^ { s } ( l ) } }$ is calculated as

$$
\overline {{p _ {i , j} ^ {s} (l)}} = \left(\sum_ {j = k i - k + 1} ^ {k i} p _ {i, j} ^ {s} (l)\right) / k. \tag {9}
$$

So far, we have finished analyzing how to get $P _ { \mathrm { r e v e a l } }$

For anonymity degree of AM as a receiver, we denote the AM node we consider as $p _ { u , t }$ . Its parent is $\operatorname { } p _ { u - 1 , [ t / k ] }$ and grandparent is $p _ { u - 2 , [ [ t / k ] / k ] }$ . Here, we denote [i] as the largest integer that is no more than i. We give the formulae to calculate the probability that the identity of the AM as a receiver is revealed as below:

$$
P _ {\text { reveal }} ^ {r} = (1 - (1 - P _ {\text { broken }}) ^ {2}) + (1 - P _ {\text { broken }}) ^ {2} * P _ {\text { attack }} ^ {r}, \tag {10}
$$

$$
w _ {i, j} ^ {r} = \left\{ \begin{array}{c l} 0 & (q _ {i, j} = 0), \\ 0 & (q _ {i, j} = 1, q _ {i + 1, k j} = 0), \\ P _ {\text {broken}} * (1 - P _ {\text {broken}}) * \left(\sum_ {l = 1} ^ {L - 1} p _ {i, j} ^ {r} (l) * f (l)\right) & (q _ {i, j} = q _ {i + 1, k j} = 1, q _ {i + 2, k ^ {2} j} = 0, \{i, j \} \neq \{u - 1, [ t / k ] \}), \\ \left(\sum_ {l = 1} ^ {L - 1} p _ {i, j} ^ {r} (l) * f (l)\right) * P _ {\text {broken}} & (q _ {i, j} = q _ {i + 1, k j} = 1, q _ {i + 2, k ^ {2} j} = 0, \{i, j \} = \{u - 1, [ t / k ] \}), \\ P _ {\text {broken}} * (1 - P _ {\text {broken}}) ^ {2} * \left(\sum_ {l = 1} ^ {L - 1} p _ {i, j} ^ {r} (l) * f (l)\right) & (q _ {i, j} = q _ {i + 1, k j} = q _ {i + 2, k ^ {2} j} = 1, \{i, j \} \neq \{u - 2, [ [ t / k ] / k ] \}), \\ P _ {\text {broken}} * (1 - P _ {\text {broken}}) * \left(\sum_ {l = 1} ^ {L - 1} p _ {i, j} ^ {r} (l) * f (l)\right) & (q _ {i, j} = q _ {i + 1, k j} = q _ {i + 2, k ^ {2} j} = 1, \{i, j \} = \{u - 2, [ [ t / k ] / k ] \}), \end{array} \right. \tag {11}
$$

![](images/353fce1f1c7f64bf3825633e220bbe8645d1742338fd36ba5244248a9c964180.jpg)



Fig. 2. Anonymity degree of AM as a sender.

$$
p _ {\text { attack }} ^ {r} = \left\{ \begin{array}{l l} 0 & u = 1, \\ \frac {w _ {u - 1 , [ t / k ]} ^ {r}}{\sum_ {i = 1} ^ {L} \sum_ {j = 1} ^ {k ^ {i}} w _ {i , j} ^ {r}} / k, & u = 1, \end{array} \right. \tag {12}
$$

$$
p _ {i, j} ^ {r} (l) = \left\{ \begin{array}{c l} 0 & (l > u - 1), \\ 0 & (l <   1 \text {   or   } i <   1), \\ 1 & (l = 1, i = 1), \\ 1 - p _ {\text { broken }} & (l = 1, i = 2), \\ (1 - p _ {\text { broken }}) ^ {2} & (l = 1, i > 2), \\ p _ {\text { broken }} * p _ {i - 1, [ j / k ]} ^ {r} (l - 1) + (1 - p _ {\text { broken }}) * p _ {\text { broken }} & (\text { otherwise }). \\ * p _ {i - 2, [ [ j / k ] / k ]} ^ {r} (l - 2) \end{array} \right. \tag {13}
$$

Here, the definition of $p _ { i , j } ^ { r } ( l )$ is similar to $p _ { i , j } ^ { s } ( l )$ , which is defined above.

# 4.3. Numerical results and discussions

In the following discussion, we will consider the numerical results based on the above formulae for anonymity degree in the incomplete tree. The incomplete tree we use is a binary tree. The root node has four grandchildren; one is the root of a complete subtree with 2 leaves in the third layer, one is the root of a complete subtree with 4 leaves in the fourth layer, one is the root of a complete subtree with 8 leaves in the fifth layer and the other is the root of a complete subtree with 16 leaves in the sixth layer. The data are obtained in MATLAB.

Figs. 2 and 3 show the sensitivity of anonymity degree to broken ratio. Different curves represent different combinations of k and L. Anonymity degree is represented by $P _ { \mathrm { r e v e a l } } .$ . Smaller $P _ { \mathrm { r e v e a l } }$ means better anonymity degree. It is obvious that anonymity degree improves as broken ratio decreases.

When the percentage of broken nodes and L is fixed, anonymity degree improves when k increases. This is because when the tree grows wider, the broken nodes tend to be in different branches. The length of the broken tree tends to decrease.

When the percentage of broken nodes and k is fixed, anonymity degree improves when L increases. This is because when the tree grows deeper, the length of the broken tree tends to decrease.

The AM sender anonymity of the incomplete tree in our example in Fig. 2 is between those of the complete binary tree with all receivers in the third or sixth layer. This is obvious because the AM sender’s anonymity improves when the tree grows. We observe that the difference between the incomplete tree curve and the complete tree curve with six layers is very slight. This is because the children of the sender who has fewer descendants will have comparatively small weight, which helps to improve the AM sender’s anonymity. Actually, we can achieve significant bandwidth efficiency with little sacrifice of the AM sender’s anonymity.

The AM receiver anonymity of the incomplete tree in our example in Fig. 3 is worse than that of the complete tree with sixth layers. This is because fewer nodes will be considered as the parent of the receiver, therefore, the comparative weight of the AM receiver’s parent tends to increase. We observe that among all the AM receivers in the incomplete tree, the higher AM receivers have better anonymity than the lower ones. This is because their parents tend to be the tail of a shorter broken tree, which helps to decrease their weight. This fact holds under the assumption that the attacker does not know the layer of the AM receiver. We observe that the differences among different AM receivers in the incomplete tree case and the difference between the incomplete tree case and the complete tree case are very slight. This is because the AM receiver’s anonymity is dominated by the probability that the sender or the receiver is broken, which is determined by the percentage of broken nodes. This means that significant bandwidth efficiency can be achieved with little sacrifice of the AM receiver’s anonymity.

![](images/cd10e02a3afd98a99c0f35d0cd990223bca7bac473efea53e0d7812bf9625675.jpg)



Fig. 3. Anonymity degree of AM as a receiver.

# 5. Performance evaluation

We experimentally measure the additional overhead incurred in our design for achieving AM–NM and AM–AM anonymous connections, and use comprehensive simulations to evaluate the effectiveness of MAM.

# 5.1. Simulation methodology

Two types of topologies, physical and logical topologies, are generated in our simulation. The physical topology should represent the real topology with Internet characteristics. The logical topology represents the overlay system built on top of the physical topology. The communication cost between two logical neighbors is calculated based on the physical shortest path between this pair of nodes. To simulate the performance of the MAM protocol in a more realistic environment, the two topologies must accurately reflect the topological properties of real networks in each layer. BRITE [1] is a topology generation tool that provides the option to generate topologies based on the AS Model. Using BRITE, we generate physical topologies with 3000–7000 nodes. The average number of neighbors of each node ranges from 4 to 10. The 100–300 overlay nodes are randomly selected from the nodes in the physical topologies.

To reflect the real overlay systems, in the experiments we report here, member nodes are coming and leaving according to the distribution observed in [28]. The mean of the distribution is chosen to be 1800 s. The value of the variance is chosen to be half of the value of the mean. In each experiment, a number of nodes join the system at the first 120 s of the simulation in random sequence. The lifetime of each node will be decreased by one after passing each second. A member will leave in the next second when its lifetime reaches zero. During each second, there are a number of members leaving the system, and we then randomly pick up (turn on) a similar number of members from the physical network to join the system.

In all the experiments, every 50 s, random nodes are selected as senders to multicast data at a constant rate, and the simulations run for 60 min. In the MAM protocol, the lifetime of Remailers is randomly selected from 50 to 200 s. In addition, we set up the number of nodes per layer and the tree height of the overlay topology according to the results of Section 4 to guarantee the anonymity degree of the AM nodes.

# 5.2. Cost measurement of encryption techniques

We measure the cost of basic cryptography techniques to obtain base data for our further simulation. In the first experiment, we measured the data on five crypto servers, in which 2000 overlay servers and clients of the ChinaPCCN are involved. For each area center, local machines initiate: (1) 900,000 symmetric encryption requests, each of which encrypts a 1–100 KB length file, (2) 900,000 Mac code generation requests, each of which generates a 20 Byte MAC code for a 1–100 K length file, and (3) 10,000 RSA encryption and decryption requests, which, respectively, call for a signature or verification for the 10,000 MAC results generated above.

In our second experiment, we ran the crypto software kits [2] on a desktop PC with an 800 MHz Pentium III CPU and 256 Mbytes of memory, 20 GBytes hard disk and 10/100M Ethernet card. We ran each test 10 times, and used the average data.

On crypto servers, the average 1024-bit RSA decryption count per second is from 17.12 to 103.09 compared to 14.6 for software tools. The encryption is from 322.4 to 1941.7 compared to 275 for software. Normally the RSA encryption is about 10–19 times faster than the decryption process. The 768- bit and 512-bit test results also validate it. In most cases, the 1024-bit key RSA can be regarded as a sufficient security cryptography algorithm, so in our simulation on the overlay multicast system, we chose the 1024-bit RSA as the crypto process in the onion path and used 45.87 and 864 per second, from the crypto server’s results, as the reference values of the 1024-bit RSA performance.

The DES performance is in the range from 2.24 to 8.78 Mbps, and the 3DES is from 1.89 to 6.43 Mbps. The hash function of MD5 performance is from 0.97 to 11.64 Mbps, and SHA-1 is from 3.23 to 11.28 Mbps. The software implementation performance is almost at the average level of those five servers. Therefore, we chose 5.41 Mbps as the DES speed and 7 Mbps as the SHA-1 speed.

# 5.3. Performance metrics

We compare the performance of three different approaches: optimal, MAM, and RAND. In Optimal, the anonymous multicast tree is optimized using an offline algorithm. In a naïve approach, indicated as “RAND”, each joining node randomly selects a member to connect to the multicast tree.

We use two performance metrics: relative resource usage (RRU) and average worst-case delay (AWD).

The stress of a physical link is defined in [11] as the number of identical copies of a packet carried by a physical link. We define resource usage as $\textstyle \sum _ { j = 1 } ^ { n } d _ { j } \times s _ { j }$ , where $d _ { j }$ is the delay of link j and $s _ { j }$ is the stress of link j. Resource usage is one of the parameters of seriously concerned to network administrators. Heavy network traffic limits the scalability of overlay networks [23]. RRU is defined as the ratio of the resource usage of MAM or other approaches to the optimal anonymous multicast tree. AWD is the average delay from the source to the farthest node that gets the multicast packets, when nodes are selected at random as the source nodes in multiple runs.

# 5.4. Simulation results

When there is no member needing to hide its identity, the system will be the same as normal end system multicast. Intuitively, the total cost of the system will increase when the number of nodes need to be hidden increases. We first show MAM’s performance by increasing the number of nodes that need to achieve anonymity (AM nodes) in the system.

With 3000 physical nodes and 200 overlay multicast members, Figs. 4 and 5 plot the RRU and AWD of different approaches versus the number of AM nodes in the system. When the ratio of AM nodes in the system is small, MAM’s RRU is very close to the optimal solution. MAM’s AWD is very close to the optimal solution when less than half of the nodes are AM nodes. We vary the system size from 100 to 400, and the physical network size from 2000 to 8000. The results are consistent, indicating that MAM maintains effectiveness, and the RRU and AWD of MAM are not sensitive to the system size or the physical networks size. If all of the members in a system are AM nodes, even the optimal solution will be as bad as the naïve RAND approach, and a system of smaller size can incur greater traffic overhead than a system with larger size. Hence, in MAM, we propose to avoid a situation where all the members are AM nodes by inviting MO nodes into the system. Frankly, it is always helpful if more MO nodes can join the system. However, the overhead of inviting MO nodes is hard to predict: they merely provide service to the system but do not consume the multicast content.

![](images/96b7f826541186de172f8e69bf82927ac18dd4d3a8c5b8345a0efc8b3def7874.jpg)



Fig. 4. RRU vs. the number of AM nodes.

![](images/b4302225304452a07420622771014e34eacecea3a90f137225544071043e07b4.jpg)



Fig. 5. AWD vs. the number of AM nodes.

In the “MAM” protocol, MO nodes are not invited. We can see that when the percentage of AM nodes is large, both RRU and AWD degrade significantly. We investigate the effectiveness of inviting MO nodes to join in Figs. 4 and 5 using the “MAM– MO” protocol, in which MO nodes are invited when the ratio of AM nodes in the system reaches 90%. The improvement is substantial for a system with more than 270 AM nodes (90% of the system).

The next question is when is the best time for the system to invite MO nodes, i.e. what is the best IT. Figs. 6 and 7 show the RRU improvement and AWD improvement versus the number of invited MO nodes for a different given number of AM nodes in a system with 200 overlay multicast members. RRU/AWD improvement is defined as the percentage of the RRU/AWD improvement with the MAM–MO protocol over the MAM protocol without MO node invitation. “RRU-n”/ “AWD-n” means the RRU/AWD improvement for a given number of n AM nodes. In general, inviting more MO nodes means better performance with the assumption that we have an infinite number of available MO nodes to be invited.

![](images/7eecf56e3d6f729aa3cf69602a5ce529443a2f4d1f480f8174b7ea3f97eb57c5.jpg)



Fig. 6. RRU improvement vs. # of invited MO nodes.

![](images/bd96f191e02559a16824628f750bad786a98868f74a496a38b833945f6e014e2.jpg)



Fig. 7. AWD improvement vs. # of invited MO nodes.

However, when a certain number of MO nodes have been invited, inviting more MO nodes is not as effective as before. For example, there is a clear jump in Fig. 6 for RRU-120, which shows that when 30 MO nodes have been invited, inviting more MO nodes gives little additional RRU improvement, where the corresponding IT is 120/(200 + 30) = 52%. Similarly, the ITs for RRU-150 and RRU-180 are 47% and 47%. If we calculate the ITs from Fig. 7, we have 46%, 52%, and 47% for AWD-120, AWD-150, and AWD-180, respectively.

Therefore, our interpretation of the experimental results is that when less than around 50% of the nodes wish to be anonymous, MAM may be directly used with no need to invite MO nodes; otherwise, MO nodes should be invited to keep the ratio of AM nodes in the system at about 50%. Beyond this, inviting more MO nodes is not necessary.

# 6. Conclusion and future work

In this paper, we propose the MAM protocol to provide anonymous multicast service. Our analysis shows that the anonymity degree of AM nodes is correlated with the broken ratio, tree degree, and tree depth. We also show that the incomplete multicast tree can achieve a similar anonymity degree with much higher bandwidth efficiency, compared to the complete multicast tree.

Our performance evaluation shows that MAM is an effective approach to construct an efficient anonymous multicast tree. When the percentage of AM nodes in a system is below a certain level, without inviting MO nodes, MAM performs almost the same as the optimal solution. We also show that inviting a certain ratio of MO nodes can be very effective for a system with a large number of AM nodes.

# Acknowledgments

This work was supported in part by the US National Science Foundation under grants CCF- 0325760, CCF-0514078, CNS-0549006, CNS 0551464, CCF-0329155, and CCF-0546668. The authors would like to thank anonymous reviewers for their insightful and constructive comments and critiques.

# References

[1] BRITE, http://www.cs.bu.edu/brite/.   
[2] RSAREF20, http://tirnanog.ls.fi.upm.es/Servicios/Software/ap\_crypt/ disk3/rsaref20.zip, 1994.   
[3] D. Andersen, H. Balakrishnan, F. Kaashoek, R. Morri, Resilient overlay networks, in: Proceedings of the SOSP, 2001.   
[4] S. Banerjee, B. Bhattacharjee, C. Kommareddy, Scalable application layer multicast, in: Proceedings of the ACM SIGCOMM, 2002.   
[5] R. Canetti, J. Garay, G. Itkis, D. Micciancio, M. Naor, B. Pinkas, Multicast security: a taxonomy and some efficient constructions, in: Proceedings of the INFOCOM, 1999.   
[6] M. Castro, P. Druschel, A. Kermarrec, A. Rowstron, Scribe: a large-scale and decentralized application-level multicast infrastructure, IEEE JSAC, 2002.   
[7] M. Castro, M.B. Jones, A.-M. Kermarrec, A. Rowstron, M. Theimer, H. Wang, A. Wolman, An evaluation of scalable application-level multicast built using peer-to-peer Overlays, in: Proceedings of the IEEE INFOCOM, 2003.   
[8] D. Chaum, Untraceable electronic mail return addresses, and Digital Pseudonyms, Comm. ACM, (1981) 84–88.   
[9] Y. Chu, A. Ganjam, T. Ng, S. Rao, K. Sripanidkulchai, J. Zhan, H. Zhang, Early experience with an internet broadcast system, in: Proceedings of the USENIX, 2004.   
[10] Y. Chu, S. Rao, S. Seshan, H. Zhang, Enabling conferencing applications on the Internet using an overlay multicast architecture, in: Proceedings of the ACM SIGCOMM, 2001.   
[11] Y. Chu, S.G. Rao, H. Zhang, A case for end system multicast, in: Proceedings of the ACM SIGMETRICS, 2000.   
[12] R. Dingledine, M. J. Freedman, D. Molnar, The free haven project: distributed anonymous storage service, in: H. Federrath (Ed.), Workshop on Design Issues in Anonymity and Unobservability, Lecture Notes in Computer Science, vol. 2009, Springer, Berlin, (2001) 67–95.   
[13] M. Freedman, R. Morris, Tarzan: A peer-to-peer anonymizing network layer, in: Proceedings of the CCS, 2002.

[14] X. Fu, B. Graham, D. Xuan, R. Bettati, W. Zhao, Analytical and empirical analysis of countermeasures to traffic analysis attacks, in: Proceedings of the IEEE International Conference on Parallel Processing (ICPP), 2003.   
[15] E. Gabber, P. Gibbons, D. Kristol, Y. Matias, A. Mayer, Consistent, yet anonymous, web access with LPWA, Commun. ACM 42 (2) (February 1999) 42–47.   
[16] E. Gabber, P. Gibbons, Y. Matias, A. Mayer, How to make personalized web browsing simple, secure, and anonymous, in: Proceedings of the Conference on Financial Cryptography, 1997.   
[17] C. Grosch, Framework for anonymity in IP-multicast environment, in: Proceedings of the IEEE GLOBECOM, 2000.   
[18] Y. Guan, X. Fu, D. Xuan, P. Shenoy, R. Bettati, W. Zhao, NetCamo: camouflaging network traffic for QoS-guaranteed mission critical applications, IEEE Trans. Systems, Man, Cybernet. 2001.   
[19] I Gupta, K. Bitman, Holistic operations in large-scale sensor network systems: a probabilistic peer-to-peer approach, in: Proceedings of the International Workshop on Future Directions in Distributed Computing (FuDiCo), 2002.   
[20] P. Kruus, J. Macker, Techniques and issues in multicast security, in: Proceedings of the MILCOM, 1998.   
[21] X. Liao, H. Jin, Y. Liu, L.M. Ni, D. Deng, AnySee: peer-to-peer live streaming, in: Proceedings of the INFOCOM, 2006.   
[22] X. Liu, Y. Liu, L. Xiao, Improving query response delivery quality in peer-to-peer systems, IEEE Trans. Parallel and Distributed systems, 2006.   
[23] Y. Liu, X. Liu, L. Xiao, L.M. Ni, X. Zhang, Location-aware topology matching in unstructured P2P systems, in: Proceedings of the IEEE INFOCOM, 2004.   
[24] Y. Liu, Z. Zhuang, L. Xiao, L.M. Ni, A distributed approach to solving overlay mismatch problem, in: Proceedings of the 24th International Conference on Distributed Computing Systems (ICDCS), 2004.   
[25] M. Moyer, J. Rao, P. Rohatgi, A survey of security issues in multicast communications, IEEE Network, 1999.   
[26] A. Nakao, L. Peterson, A. Bavier, A routing underlay for overlay networks, in: Proceedings of the ACM SIGCOMM, 2003.   
[27] M.K. Reiter, A.D. Rubin, Crowds: anonymity for web transactions, ACM Trans. Inform. System Security, (November 1998) 66–92.   
[28] S. Saroiu, P. Gummadi, S. Gribble, A measurement study of peer-topeer file sharing systems, in: Proceedings of the Multimedia Computing and Networking (MMCN), 2002.   
[29] R. Sherwood, B. Bhattacharjee, A. Srinivasan, P5: A protocol for scalable anonymous communication, in: Proceedings of the IEEE Symposium on Security and Privacy, 2002.   
[30] S. Shi, J.S. Turner, Routing in overlay multicast networks, in: Proceedings of the IEEE INFOCOM, 2002.   
[31] P.F. Syverson, D.M. Goldschlag, M.G. Reed, Anonymous connections and onion routing, in: IEEE Symposium on Security and Privacy (S&P’97) (1997) pp.44–53.   
[32] M. Waldvogel, R. Rinaldi, Efficient topology-aware overlay network, in: Proceedings of the ACM HotNets, 2002.   
[33] N. Weiler, Secure anonymous group infrastructure for common and future internet application, in: Proceedings of the 17th Annual Computer Security Applications Conference (ACSAC’01), 2001.   
[34] L. Xiao, X. Liu, W. Gu, D. Xuan, Y. Liu, A design of overlay anonymous multicast protocol, in: Proceedings of the IPDPS, 2006.

[35] L. Xiao, A. Patil, Y. Liu, L. M. Ni, A.-H. Esfahanian, Prioritized overlay multicast in ad-hoc environments, IEEE Comput. Magazine (February 2004) 67–74.   
[36] L. Xiao, Z. Xu, X. Zhang, Low-cost and reliable mutual anonymity protocols in peer-to-peer networks, IEEE Trans. Parallel Distributed Systems, 2003.   
[37] Z. Xu, C. Tang, Z. Zhang, Building topology-aware overlays using global soft-state, in: Proceedings of the 23rd International Conference on Distributed Computing Systems (ICDCS), 2003.

Li Xiao received the B.S. and M.S. degrees in computer science from Northwestern Polytechnic University, China, and the Ph.D. degree in computer science from the College of William and Mary in 2002. She is an assistant professor of computer science and engineering at Michigan State University. Her research interests are in the areas of distributed and Internet systems, overlay systems and applications, sensor networks, system resource management, and design and implementation of experimental algorithms. She is a member of the ACM, the IEEE, the IEEE Computer Society, and IEEE Women in Engineering.

Yunhao Liu received the B.S. degree in Automation from Tsinghua University, China, in 1995, the M.A. degree from Beijing Foreign Studies University, China, in 1997, and the Ph.D. degree in Computer Science from Michigan State University in 2004. He is now an assistant professor of Department of Computer Science at Hong Kong University of Science and Technology. His research interests are in the areas of peer-to-peer computing, pervasive computing, distributed systems, network security, embedded systems, and high-speed networking. He is a member of the IEEE and the IEEE Computer Society.

Wenjun Gu received the B.S. and M.S. degrees in Electronic Engineering from Shanghai Jiao Tong University, China, in 2000 and 2003, respectively. He is currently working towards the Ph.D. degree in the Department of Computer Science and Engineering at The Ohio State University. His research interests include security and distributed computing in overlay, ad hoc and wireless sensor networks.

Dong Xuan received his B.S. and M.S. degrees in Electronic Engineering from Shanghai Jiao Tong University (SJTU), China, in 1990 and 1993, and Ph.D. degree in Computer Engineering from Texas A&M University in 2001. Currently, he is an assistant professor in the Department of Computer Science and Engineering, The Ohio State University. He was on the faculty of Electronic Engineering at SJTU from 1993 to 1997. In 1997, he worked as a visiting research scholar in the Department of Computer Science, City University of Hong Kong. From 1998 to 2001, he was a research assistant/associate in Real-Time Systems Group of the Department of Computer Science, Texas A&M University. He received the National Science Foundation (NSF) CAREER award in 2005. His research interests include real-time computing and communications, network security and distributed systems.

Xiaomei Liu received the B.S. degree in Electronics and Information System Technology from East China Normal University in 1996, the M.S. degree in Computer Engineering in University of Toledo in 2000. She is currently a Ph.D. student at the Michigan State University. Her research interests include distributed operating systems and computer network. She is a student member of the IEEE and the IEEE Computer Society.