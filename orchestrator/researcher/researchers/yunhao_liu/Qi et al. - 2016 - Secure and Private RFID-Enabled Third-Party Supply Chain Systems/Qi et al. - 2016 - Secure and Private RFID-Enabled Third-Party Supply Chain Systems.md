# Secure and Private RFID-Enabled Third-Party Supply Chain Systems

Saiyu Qi,∗ Yuanqing Zheng,† Mo Li,‡ Li Lu,§ and Yunhao Liu¶

Abstract—Radio Frequency Identification (RFID) is a key emerging technology for supply chain systems. By attaching RFID tags to various products, product-related data can be efficiently indexed, retrieved and shared among multiple participants involved in an RFID-enabled supply chain. The flexible data access property, however, raises security and privacy concerns. In this paper, we target at security and privacy issues in RFID-enabled supply chain systems. We investigate RFID-enabled Third-party Supply chain (RTS) systems and identify several inherent security and efficiency requirements. We further design a Secure RTS system called SRTS, which leverages RFID tags to deliver computationlightweight crypto-IDs in the RTS system to meet both the security and efficiency requirements. SRTS introduces a Private Verifiable Signature (PVS) scheme to generate computation-lightweight crypto-IDs for product batches, and couples the primitive in RTS system through careful design. We conduct theoretical analysis and experiments to demonstrate the security and efficiency of SRTS.

# 1 INTRODUCTION

Radio Frequency Identification (RFID) is a key emerging technology for supply chain systems. Compared with printed tags (e.g., barcodes, QR codes), RFID tags have moderate storage capacity to store unique IDs and support longdistance communication. By attaching tags to products, supply chain participants can read a tag to efficiently track the labeled product. The tag ID serves as an index to retrieve the product-related data from a database. Such an RFIDbased supply chain facilitates information sharing among participants, enabling substantially improved product handling efficiency [1].

For instance, Toll Global Logistics, one of Asia’s largest logistics providers, has adopted the RFID technology to track the tagged products of its served firms and cut labor costs [3]. The RFID infrastructure can be further leveraged to share product information with the participants involved in the supply chain. The sender stores IDs into tags and

∗School of Cyber Engineering, Xidian University, China   
†Department of Computing, Hong Kong Polytechnic University, Hong Kong   
‡School of Computer Engineering, Nanyang Technological University, Singapore   
§School of Computer Science and Engineering, University of Electronic Science and Technology, China   
• ¶TNLIST, School of Software, Tsinghua University, China

![](images/25cdfec81d482dcc980d99a88efaf276612e8f2dd1932c918500258b056bfd0b.jpg)



Fig. 1: Diverse requirements of different participants in an RFID-enabled RTS system.

uploads the production messages indexed by the IDs in its database. The sender then delegates the logistics provider to deliver the tagged products to the receiver in a way that the latter two participants can flexibly read the tag IDs to retrieve the production messages of the labeled products from the sender’s database.

Despite the flexibility of data sharing enabled by RFID technology, it raises security and privacy concerns [4]. When tagged products flow in RTS system, the production messages stored in the sender’s database should not be freely exchanged by the logistics provider and the receiver without any security guarantees. Given that the three participants typically belong to different trust sectors, different participants may have diverse requirements as shown in Figure 1.

First, the sender and the receiver may be concerned about the privacy for the production messages of product batches against the logistics provider as the messages may be sensitive. Without privacy guarantee, a honest-butcurious logistics provider can collect production messages and explore non-trivial business secrets (e.g., production details, strategic relationships, buying interests of the receiver, etc). For instance, the logistics provider may use the collected messages together with out-of-bound information (e.g., product trading volume, transfer time, etc) to gradually infer the business transactions between the sender and the receiver. The sender and the receiver thus may be concerned about the privacy for the production messages of each delivered product batch, which we term as batch privacy.

Second, the logistics provider and the receiver may be concerned about non-repudiation for the production messages of product batches to prevent the sender from denying the creation of them. Without non-repudiation guarantee, a malicious sender may deny the creation of production messages to avoid economic loss. For instance, when a problematic product mismatched with its production message is found and needs to be recalled, a malicious sender may blame the logistics provider or the receiver, and refuse to recall the product. In fact, product delivery service is not always reliable in real trading systems. As exposed by China e-commerce complaints and rights of public service platform [5], customers receive inferior or fake products frequently in E-commerce business. The logistics provider and the receiver thus may be concerned about the non-repudiation for the production messages of each delivered product batch, so that they can prove the receipt of the whole batch or a certain product in the batch, which we term as batch nonrepudiation and item non-repudiation, respectively.

Third, a large scale RTS system involves delivery of large amount of product batches. Ensuring privacy and nonrepudiation for production messages of product batches among the three participants through crypto-tools may incur prohibitive communication and computation overhead. Specifically, when a product batch is delivered in the RTS system, the logistics provider may need to receive and process secured production messages for each product in the batch. As logistics provider is on the critical path of each product batch delivery, it easily becomes a bottleneck of the RTS system. The three participants thus are concerned about the delivery efficiency of product batches, which we term as batch efficiency.

In this paper, we target at security and efficiency issues in RFID-enabled Third-party Supply chain (RTS) system. We design SRTS, a Secure RTS system, to ensure the above three concerned requirements. Instead to directly exchange secured production messages through communication link, S-RTS leverages RFID tags to deliver computation-lightweight crypto-IDs in the RTS system. Crypto-IDs serve as product IDs for product identification purpose as used in general RFID framework with the following two additional security properties: (1) crypto-IDs have non-repudiation property from which both the logistics provider and the receiver can acquire evidences to prove batch and item non-repudiations; and (2) crypto-IDs have privacy property to hide the content of the production messages. SRTS leverages the security properties of crypto-IDs as well as careful protocol design to achieve batch privacy, batch non-repudiation and item nonrepudiation. By leveraging tags to distribute computationlightweight crypto-IDs, SRTS also reduces the communication and computation overhead, achieving batch efficiency.

SRTS implements this idea through two steps. SRTS first introduces a Private Verifiable Signature (PVS) scheme to efficiently sign production messages as a whole in a privacy-preserving way. The signing result can be properly encoded into computation-lightweight crypto-IDs. SRTS then provides a set of distributed protocols to combine PVS scheme with RTS system through careful design. Specifically, product batch transfer protocol is executed in the delivery of a product batch. The sender generates crypto-IDs from the production messages of the batch through PVS scheme. After the delivery, both the logistics provider and the receiver acquire evidences from tag carried crypto-IDs. Later, the two parties can use the acquired evidences in a product batch arbitration protocol and an auditable itemlevel arbitration protocol to prove batch non-repudiation and item non-repudiation, respectively. The evidences are used in different ways in the two protocols to optimize the performance.

Our contributions can be summarized as follows. To our best knowledge, we are the first to propose efficient solutions to achieve these key security and efficiency requirements for large-scale RTS systems. We formulate and study three major security and efficiency requirements in RTS systems, i.e., batch privacy, batch non-repudiation/item non-repudiation and batch efficiency. We devise the SRTS scheme to achieve the desired requirements. We carry out extensive evaluation and evaluate the applicability of our approach on commodity C1G2 RFID systems.

# 2 BACKGROUND AND PROBLEM

# 2.1 RFID framework

Current RFID systems generally consist of three main components: RFID tags, RFID readers and a database. Lightweight commodity RFID tags harvest energy from RFID readers and backscatter incident signals to communicate with the RFID readers [1], [2]. The RFID tags have moderate storage capability with small onboard non-volatile memory, e.g., the Alien ALN-9640 passive RFID tags are equipped with a 512-bit user memory [28]. RFID readers can read/write a small amount of data (e.g., 512 bits) from/to user memory of RFID tags [28], [29]. Restricted by the small memory of RFID tags, product details are not carried by the tags but stored in the database, and accessed by the tag IDs as indexes to achieve fine-grained information sharing among participants. By labeling the products with RFID tags, supply chain participants can read tag IDs to efficiently track the labeled products and product details, which greatly facilitates the logistics and product management.

# 2.2 RFID-enabled RTS system

An RFID-enabled RTS system consists of three participants: a logistics provider and two cooperative firms. We name the logistics provider as Relaynode and distinguish the two firms as Sender and Receiver. Sender transfers tagged product batches to Receiver through Relaynode. We describe detailed operations shortly.

To transfer a product batch, Sender attaches RFID tags to the batch. Depending on the applications, tags can be attached in different levels, such as item-level, packet-level or container-level. In this paper, we focus on item-level tag attachment as other levels can be easily extended from itemlevel.

Each product of the batch corresponds to a message $i d _ { i } | | m _ { i } ,$ which consists of an ID $i d _ { i }$ and a production message $m _ { i }$ . Sender writes $i d _ { i }$ into the attached tag and stores the message $m _ { i }$ in its database indexed by $i d _ { i } .$ . We consider a general case where the production messages of the products within the same batch may be different. For instance, a hospital (Receiver) may order a batch of medicines from a medicine company (Sender), with the batch containing different types of medicines.

![](images/85a9711616951924db380b5218498d5f76de5e46a0804d03e4c264df686ec6ed.jpg)



Fig. 2: Product batch transfer.

# 2.3 Desired requirements

When a product batch is transferred through RTS system, different participants are concerned about different security requirements against other participants for the batch. Yet, the three participants hope to afford lightweight batch delivery overhead. In summary, the participants are concerned about following three requirements:

Batch privacy: Sender wants to share the production message $m _ { i }$ of each product in the batch with Receiver. As the content of $m _ { i }$ might be related to sensitive business matters, both Sender and Receiver do not want to leak $m _ { i }$ to Relaynode.   
Batch and item non-repudiation: Both Relaynode and Receiver want to obtain the ability to publicly prove batch non-repudiation—convincing an authority the receipt of the product batch with each product associated with a production message $m _ { i } ;$ and item nonrepudiation—convincing an authority the receipt of a certain product in the batch associated with a production message $m _ { i }$ .   
Batch efficiency: To achieve the above two security requirements, the production message $m _ { i }$ of each product in the batch needs to be properly equipped with privacy and non-repudiation properties and delivered from Sender to Relaynode and Receiver. As Relaynode is on the critical path of each product batch delivery, all the three participants hope to minimize the delivery overhead to avoid Relaynode becomes a bottleneck of the RTS system.

# 3 OVERVIEW OF SRTS

Basically, SRTS combines cryptographic tools with RFID framework to achieve the desired security and efficiency requirements. SRTS leverages RFID tags to deliver computation-lightweight crypto-IDs in the RTS system to reduce the communication and computation overhead. For a product batch, each product tag is loaded with a crypto-ID and the corresponding production message is stored at Sender’s database indexed by the crypto-ID. The crypto-ID serves as a product ID to identify the product as used in RFID framework with two additional security properties: (1) crypto-IDs have non-repudiation property from which both Relaynode and Receiver can acquire receipt evidences of a product batch. The constructed evidences can be used to prove batch and item non-repudiations for the product batch; and (2) the crypto-IDs have privacy property to hide the content of the production messages. As a result, the only way to acquire the production messages is to access Sender’s database, which is only allowed by Receiver. In the following, we first give a strawman item-level solution, which presents partial design principles of SRTS. This solution then leads to our final design of SRTS.

# 3.1 A strawman item-level solution

A strawman design might be to encode a signed commitment as a cypto-ID, with the production message committed in the commitment. During the transfer of a product batch, both Relaynode and Receiver can directly collect the signed commitments from the product tags as evidences. Receiver is further allowed to use the signed commitments as indexes to retrieve the production messages from Sender’s database. In an arbitration, Relaynode/Receiver could choose to reveal one or all of the collected signed commitments to an authority to prove item non-repudiation or batch nonrepudiation, respectively. After convincing that the revealed signed commitment(s) is(are) correctly signed by Sender, the authority then requires Sender to reveal the committed production messages. Due to the security of commitment scheme, revealing tampered production messages will be detected by the authority.

This design, however, incurs prohibitive signature processing overhead. In a large-scale RTS system, where a large amount of product batches are delivered, the participants have to process tag carried digital signatures (contained in the signed commitment) in item-level. For a batch of n products, Sender needs to generate n signatures, and Relaynode and Receiver need to verify n signatures. Signature computation could incur considerable overhead (see detailed experiments in Section 6), and thus delay the transportation in RTS system. Besides, low-cost, storage-constrained tags cannot accommodate excessively long signatures, e.g., a 320- bit ECDSA signature alone may consume more than half of the commodity tag memory.

# 3.2 Our design

Instead, our design of SRTS provides a new signature scheme called Private Verifiable Signature (PVS) scheme, whose signing result can be encoded into computationlightweight crypto-IDs. SRTS then provides a set of distributed protocols to combine PVS scheme with RFID framework through careful design.

PVS scheme: PVS scheme adopts a commit-then-sign pattern to sign the production messages of a product batch as a whole in two ways: public signing and private signing. In public signing, the production messages are committed into commitments and the concatenation of which are further signed by a digital signature scheme. The production messages as well as the signature is then output as a message batch-signature (MB) pair. In private signing, the production messages are committed and then signed in the same way as in the public signing, while the commitments as well as the signature is output as a commitment batchsignature (CB) pair. Both the MB and CB pairs incur constant signature storage and computation overhead regardless of the number of the production messages. PVS scheme guarantees that both the MB pair and the CB pair are unforgeable while the CB pair hides but binds the committed production messages. All these security properties are formally proved in security models.

Combining PVS scheme with RTS system: SRTS combines PVS scheme with RTS system by providing a set of distributed protocols. SRTS provides a product batch transfer protocol as shown in Figure 2. To transfer a product batch, Sender privately signs the production messages of the batch to generate a CB pair and divides the pair into crypto-IDs. During the transfer, both Relaynode and Receiver can directly recover the CB pair from the tags as evidence. Additionally, Receiver can choose to retrieve the production messages from Sender, incorporate them with the CB pair to generate a MB pair, and stores the MB pair as its evidence.

SRTS provides a product batch arbitration protocol to prove batch non-repudiation. In the protocol, Relaynode/Receiver directly reveals its CB/MB pair of the batch to an authority to prove batch non-repudiation for the product batch. Due to the non-repudiation property of CB pair, the authority convinces that the commitments contained in the CB pair is generated from Sender. The authority further requires Sender to reveal these committed production messages. Due to the binding property of CB pair, revealing tampered production messages will be detected by the authority. Due to the non-repudiation property of MB pair, the authority directly convinces that the production messages contained in the MB pair is generated from Sender.

To efficiently prove item non-repudiation, SRTS provides an auditable item-level arbitration protocol. The protocol starts with a lightweight item non-repudiation proof phase which involves the exchange of attestations, and followed by an expensive audit phase which involves the reveal of a CB/MB pair. The protocol guarantees that if all participants behave correctly in the item non-repudiation proof phase, then the audit phase can be ignored. Whereas if misbehavior occurs, audit phase will be triggered and the malicious participant will be detected. Such a separation enforces all the participants behave in the lightweight item nonrepudiation proof phase, and the expensive audit phase thus can be ignored.

# 4 SRTS: PRIVATE VERIFIABLE SIGNATURE

In this section, we focus on PVS scheme and analyze its security properties. PVS scheme is the key component of S-RTS to achieve lightweight batch-level signature processing (computation and storage) overhead.

With the PVS scheme, Sender can sign production messages to generate either an MB pair or a CB pair. The MB pair reveals the production messages, while the CB pair hides the production messages. Both the CB and MB pairs involve one signature regardless of the number of the production messages.

PVS scheme guarantees several security properties including: (1) both the MB pair and the CB pair are unforgeable, (2) the CB pair hides the production messages, and (3) the CB pair can only be opened to the hidden production messages.

TABLE 1: Important notations 

<table><tr><td>Notations</td><td>Definitions</td></tr><tr><td>(pk, sk)</td><td>Public-secret key pair of digital signature scheme</td></tr><tr><td>s</td><td>Signature of digital signature scheme</td></tr><tr><td>ck</td><td>Commitment key of string commitment scheme</td></tr><tr><td>com</td><td>Commitment of string commitment scheme</td></tr><tr><td>r</td><td>Random number used to generate commitment com</td></tr><tr><td>U</td><td>Domain of random number r</td></tr><tr><td> $\{str_i\}_{num}$ </td><td>Concatenated batch of num messages  $str_1||...||str_num$ </td></tr><tr><td>(PK, SK)</td><td>Public-secret key pair of PVS scheme</td></tr><tr><td> $(\{m_i\}_n, \delta_{MB})$ </td><td>Message batch-signature(MB) pair of PVS scheme</td></tr><tr><td> $\{m_i\}_n$ </td><td>Concatenated batch of n production messages  $m_1||...||m_n$ </td></tr><tr><td> $\delta_{MB}$ </td><td>Signature in MB pair</td></tr><tr><td> $(\{mc_i\}_n, \delta_{CB})$ </td><td>Commitment batch-signature(CB) pair of PVS scheme</td></tr><tr><td> $\{mc_i\}_n$ </td><td>Concatenated batch of n PVS commitments  $mc_1||...||mc_n$ </td></tr><tr><td> $\delta_{CB}$ </td><td>Signature in CB pair</td></tr></table>

# 4.1 Notations and preliminaries

We list the important nations used in PVS scheme in Table 1. To sign product messages by PVS scheme, all the production messages need to be first concatenated to form a long message. At a high level, our construction adopts a multicommit then single-sign mechanism to compose two crypto primitives: digital signature scheme and string commitment scheme.

Digital signature: A digital signature scheme $\prod _ { D } { \bf \Pi } = { \bf \Pi }$ (skg, sig, ver) consists of a key generation algorithm skg(), a signing algorithm sig() and a verification algorithm ver(). We require the signing algorithm to support the signing of variable length message. The security property of a signature scheme is that an adversary cannot forge a valid messagesignature pair.

String commitment: A string commitment scheme $\Pi _ { S }$ = (ckg, commit) consists of a key generation algorithm ckg() and a committing algorithm commit(). A user can use commit() to generate a commitment for a string. The security properties of a commitment scheme are (1) hiding: the commitment does not leak any information about the string, and (2) binding: it is hard for the user to produce two different strings and a commitment such that the commitment is valid to both the strings.

# 4.2 Definition of PVS scheme

By using the above two crypto primitives as building blocks, PVS scheme is constructed to provide six algorithms $\Pi =$ (KeyGen, Sign, Verify, PriSign, PriVerify, Check). We briefly introduce the six algorithms as follows:

${ \mathsf { K e y G e n } } ( \lambda ) \to ( P K , S K ) .$ : On input a security parameter $\lambda ,$ this algorithm outputs a public-secret key pair (PK, SK).   
Sign(PK, SK, $\{ m _ { i } \} _ { n } )  ( \{ m _ { i } \} _ { n } , \ \delta _ { M B } ) \colon$ : On input a public key PK, a secret key SK and production

messages $\{ m _ { i } \} _ { n } ,$ this algorithm outputs an MB pair $( \{ m _ { i } \} _ { n } , \delta _ { M B } )$ , which can be verified by Verify().

Verify(PK, {mi}n, δMB) → (Accept, Reject): On input a public key PK and an MB pair $( \{ m _ { i } \} _ { n } , \delta _ { M B } )$ , this algorithm verifies the validity of $( \{ m _ { i } \} _ { n } , \delta _ { M B } )$ and outputs either Accept or Reject.   
PriSign(PK, SK, $\{ m _ { i } \} _ { n } )  ( \{ m c _ { i } \} _ { n } , \ \delta _ { C B } , \ \{ r _ { i } \} _ { n } ) :$ : On input a public key $P K , a$ secret key SK and production messages $\{ m _ { i } \} _ { n } ,$ this algorithm outputs a CB pair $( \{ m c _ { i } \} _ { n } , \bar { \delta _ { C B } } )$ and witnesses $\{ r _ { i } \} _ { n }$ . The CB pair can be verified by PriVerify().   
PriVerify(PK, $\{ m c _ { i } \} _ { n } , \ \delta _ { C B } ) \ $ (Accept, Reject): On input a public key PK and a CB pair $( \{ m c _ { i } \} _ { n } , \delta _ { C B } )$ , this algorithm verifies the validity of $( \{ m c _ { i } \} _ { n } , \delta _ { C B } )$ and outputs either Accept or Reject.   
Check(PK, {mi}n, {ri}n, {mci}n, δCB) → (Accept, Reject): On input a public key $P K ,$ production messages $\{ m _ { i } \} _ { n } ,$ witnesses $\{ r _ { i } \} _ { n }$ and a CB pair $( \{ m c _ { i } \} _ { n } ,$ $\delta _ { C B } )$ , this algorithm checks whether $\{ m _ { i } \} _ { n }$ is the original production messages committed in $( \{ m c _ { i } \} _ { n }$ , $\delta _ { C B } )$ and outputs either Accept or Reject.

# 4.3 Security Properties

The security of a PVS scheme is defined by four security properties: MB-unforgeability, CB-unforgeability, Binding and Privacy. Comparing with a general digital signature scheme, which only provides MB-unforgeability, a PVS scheme provides three additional security properties.

MB-unforgeability: Intuitively, MB-unforgeability means that it is computationally infeasible for an adversary A to forge a valid MB pair $( \{ \dot { m _ { i } } \} _ { n } , \delta _ { M B } )$ with respect to the signer.

Definition 1 (MB-unforgeability): A PVS scheme $\bar { \Pi } \ =$ (KeyGen, Sign, Verify, PriSign, PriVerify, Check) satisfies the MB-unforgeability property if every probabilistic polynomial time (p.p.t.) adversary A has negligible advantage to win in the following experiment.

Experiment $\mathbf{Exp}_{\mathcal{A}}^{MB-unf}[\mathrm{PVS}]$ : $(PK, SK) \leftarrow \mathsf{KeyGen}(\lambda)$ ; $(\{m_i\}_n^*, \delta_{MB}^*) \leftarrow \mathcal{A}^{\text{Sign}(SK, PK, \bot)}(\lambda, PK)$ ;  
output 1 if Verify $(PK, \{m_i\}_n^*, \delta_{MB}^*) \to \mathsf{Accept} \land \{m_i\}_n^* \notin M$ ;  
else output 0

Our experiment allows A to submit message batches to a signing oracle Sign(SK, PK, ⊥), which returns the corresponding MB pairs. All the queried message batches are recorded in a set M. We define the advantage of A as Ad $\mathbf { A d v } _ { \mathcal { A } } ^ { M B - u n f } [ \mathrm { P V S } ] = \operatorname* { P r } [ \mathbf { E x p } _ { \mathcal { A } } ^ { M B - u n f } [ \mathrm { P V S } ] \Rightarrow 1 ] .$ vMB-unfA [PVS] = Pr[ExpMBA .

CB-unforgeability: Intuitively, CB-unforgeability means that it is computationally infeasible for an adversary A to forge a valid CB pair $( \{ m c _ { i } \} _ { n } , \delta _ { C B } )$ with respect to the signer.

Definition 2 (CB-unforgeability): A PVS scheme $\prod { } =$ (KeyGen, Sign, Verify, PriSign, PriVerify, Check) satisfies the CB-unforgeability property if every probabilistic polynomial time (p.p.t.) adversary A has negligible advantage to win in the following experiment.

Experiment $\mathbf{Exp}_{\mathcal{A}}^{CB-unf}[\mathrm{PVS}]$ : $(PK, SK) \leftarrow \operatorname{KeyGen}(\lambda)$ ;

$$
\left(\left\{m c _ {i} \right\} _ {n} ^ {*}, \delta_ {C B} ^ {*} \right. \leftarrow \mathcal {A} ^ {\text { PriSign } (S K, P K, \bot)} (\lambda , P K);
$$

output 1 if PriVerify(PK, {mci}∗n, δ∗CB) → Accept

$$
\wedge \left\{m c _ {i} \right\} _ {n} ^ {*} \notin M;
$$

else output 0

Our experiment allows A to submit (message batch, witnesses) pairs to a signing oracle PriSign(SK, PK, ⊥), which returns the corresponding CB pairs. The commitment batches contained in all the returned CB pairs are recorded in a set M. We define the advantage of A as CB-unf $\mathbf { A d v } _ { A } ^ { C B - u n f } [ \mathrm { P V S } ]$ vCB-unf[PVS] = Pr[ExpA $= \operatorname* { P r } [ \mathbf { E x p } _ { A } ^ { C B - u n f } [ \operatorname { P V S } ] \Rightarrow 1 ]$ [PVS] ⇒ 1].

Binding: Intuitively, binding means that it is computationally infeasible for an adversary A to produce message batches $\{ m _ { i } \} _ { n } \ne \{ m _ { i } ^ { \prime } \} _ { n }$ and a CB pair $( \{ { \bar { m } } c _ { i } \} _ { n } , \ \delta _ { C B } )$ , such that $\{ m c _ { i } \} _ { n }$ is valid to both $\{ m _ { i } \} _ { n }$ and $\{ m _ { i } ^ { \prime } \} _ { n } .$ .

Definition 3 (binding): A PVS scheme $\prod = ( { \mathsf { K e y G e n } } , { \mathsf { S i g n } } ,$ Verify, PriSign, PriVerify, Check) satisfies the binding property if every probabilistic polynomial time (p.p.t.) adversary A has negligible advantage to win in the following experiment.

[PVS]:

$$
\left(\left\{m _ {i} \right\} ^ {1} _ {n}, \left\{r _ {i} \right\} ^ {1} _ {n}, \left\{m _ {i} \right\} ^ {2} _ {n}, \left\{r _ {i} \right\} ^ {2} _ {n}, \left\{m c _ {i} \right\} _ {n}, \delta_ {C B}\right) \leftarrow
$$

$$
\leftarrow \mathcal {A} (\lambda , P K, S K);
$$

$$
\wedge \operatorname{Check} (P K, \left\{m _ {i} \right\} ^ {2} _ {n}, \left\{r _ {i} \right\} ^ {2} _ {n}, \left\{m c _ {i} \right\} _ {n}, \delta_ {C B})
$$

→ Accept

$$
\wedge \left\{m _ {i} \right\} ^ {1} _ {n} \neq \left\{m _ {i} \right\} ^ {2} _ {n};
$$

else output 0

We define the advantage of A as $\mathbf { A d v } _ { \mathcal { A } } ^ { b i n d } [ \mathrm { P V S } ] \ =$ $\operatorname* { P r } [ \mathbf { E x p } _ { \mathcal { A } } ^ { b i n d } [ \mathrm { P V S } ] \Rightarrow 1 ]$ pbindA [PVS] ⇒ 1].

Privacy: Intuitively, privacy means that it is computationally infeasible for an adversary A to learn non-trivial knowledge about the message batch $\{ m _ { i } \} _ { n }$ from a CB pair $( \{ m c _ { i } \} _ { n } , \mathsf { \bar { \delta } } _ { C B } )$ .

Definition 4 (privacy): A PVS scheme Q = (KeyGen, Sign, Verify, PriSign, PriVerify, Check) satisfies the privacy property if every probabilistic polynomial time (p.p.t.) adversary A has negligible advantage to win in the following experiment.

$\begin{array} { r } { \mathrm { E x p e r i m e n t } { \mathbf E x p } _ { \mathcal { A } } ^ { P r i v } [ \mathrm { P V S } ] { \mathrm { : } } } \\ { ( P K , S K ) \gets \mathsf { K e y G e n } ( \lambda ) ; } \end{array}$

$$
(\{m _ {i} \} _ {n} ^ {1}, \{m _ {i} \} _ {n} ^ {2}) \leftarrow \mathcal {A} (\lambda , P K);
$$

$$
b \xleftarrow {R} \{0, 1 \};
$$

$$
\left(\left\{m c _ {i} \right\} _ {n} ^ {b}, \delta_ {C B}, \left\{r _ {i} \right\} _ {n} ^ {b}\right) \leftarrow \operatorname{PriSign} (P K, S K, \left\{m _ {i} \right\} _ {n} ^ {b});
$$

$$
b ^ {\prime} \leftarrow \mathcal {A} (\lambda , P K, \{m c _ {i} \} _ {n} ^ {b}, \delta_ {C B});
$$

output 1 if $b ^ { \prime } { = } b ,$ else output 0

Our experiment uses indistinguishability of multiple messages, which allows A to submit two message batches and get a CB pair. The committed messages are chosen randomly from one of the two message batches. A then sses which mesantage of A as $\mathbf { A d v } _ { A } ^ { P r i v } [ \mathrm { P V S } ] = \operatorname* { P r } [ \mathbf { E x p } _ { A } ^ { P r i v } [ \mathrm { P V S } ] \Rightarrow 1 ] \mathrm { ~ - ~ }$ $1 / 2$

# 4.4 Construction of PVS scheme

We describe a concrete PVS scheme in Table 2. Next, we analyze the security of our construction.

TABLE 2: Construction of Private Verifiable Signature 

<table><tr><td>KeyGen(λ) → (PK, SK):— (pk, sk) ← skg(λ);— ck ← ckg(λ);— Output PK = (pk, ck) and SK = sk.</td></tr><tr><td>Sign(PK, SK, {mi}n) → ({mi}n, δMB):— for 1 ≤ i ≤ n:— ri← R U;— comi← commit(ck, mi, ri);— s ← sig(sk, {comi}n);— δMB = (s, {ri}n);— Output a MB pair ({mi}n, δMB).</td></tr><tr><td>Verify(PK, {mi}n, δMB) → (Accept, Reject):— for 1 ≤ i ≤ n:— comi← commit(ck, mi, ri);— ver(pk, s, {comi}n) = valid/invalid?— If valid, output Accept, else output Reject.</td></tr><tr><td>PriSign(PK, SK, {mi}n) → ({mci}n, δCB, {ri}n):— for 1 ≤ i ≤ n:— ri← R U;— comi← commit(ck, mi, ri);— s ← sig(sk, {comi}n);— {mci}n = {comi}n;— δCB = s;— Output a CB pair ({mci}n, δCB) and witnesses {ri}n.</td></tr><tr><td>PriVerify(PK, {mci}n, δCB) → (Accept, Reject):— ver(pk, δCB, {mci}n) = valid/invalid?— If valid, output Accept, else output Reject.</td></tr><tr><td>Check(PK, {mi}n, {ri}n, {mci}n, δCB) → (Accept, Reject):— for 1 ≤ i ≤ n:— mci= commit(ck, mi, ri)?— If all equal, output Accept, else output Reject.</td></tr></table>

Theorem 1. If the digital signature scheme $\Pi _ { D }$ is unforgeable and if the string commitment scheme $\Pi _ { S }$ is binding, then our construction of PVS scheme Q achieves MBunforgeability.

Proof. When A submits a message batch $\{ m _ { i } \} _ { n }$ to the signing oracle $\mathsf { S i g n } ( S K , P K , \perp )$ , the oracle computes a commitment batch $\{ m c _ { i } \} _ { n }$ for $\{ m _ { i } \} _ { n } ,$ , signs $\{ m c _ { i } \} _ { r }$ n using the underlying digital signature scheme, and returns an MBpair $( \dot { \{ m _ { i } \} } _ { n } , \stackrel { \smile } { \delta _ { M B } } )$ . Suppose A queried l message batches $\mathsf { \bar { ( } } \{ m _ { i } \} _ { n ^ { 1 } } ^ { \mathrm { i } } , \cdots , \{ m _ { i } \} _ { n ^ { l } } ^ { l } )$ to the signing oracle Sign(SK, PK, ⊥), and $( \{ m _ { i } \} _ { n } ^ { * } , \delta ^ { * } { } _ { M B } )$ is the purported forgery output by A. The forgery must fall in at least one of the following two cases: (1) Case 1: For every message batch $\left\{ m _ { i } \right\} _ { n ^ { j } } ^ { j } ( 1 { \leq } j { \leq } l )$ submitted by A, the corresponding commitment batch $\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ is different from the commitment batch $\{ m c _ { i } \} _ { n } ^ { * }$ of $\{ m _ { i } \} _ { n } ^ { * ^ { * } } ( 2 )$ Case 2: There is a message batch $\{ m _ { i } \} _ { n ^ { j } } ^ { j } ~ ( 1 { \leq } j { \leq } l )$ submitted by A such that its commitment batch $\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ equals $\{ m c _ { i } \} _ { n } ^ { * }$ . We thus conclude $\mathbf { A d v } _ { \mathcal { A } } ^ { M B - u n f } [ \mathrm { P V S } ] \leq \mathrm { P r } [ \dot { \mathrm { C a s e ~ 1 } } ] +$

In the first case, the adversary A could be used to build an adversary B to break unforgeability of the digital signature scheme. At the beginning, B is given a public key pk of the digital signature scheme and generates a commitment key ck of the string commitment scheme. B then generates a public key of PVS scheme $P K = ( p k , c k )$ and gives PK to A. B simulates the oracle Sign(PK, SK, ⊥) as follows. When A queries a message batch $\left\{ m _ { i } \right\} _ { n ^ { j } } ^ { j } ~ ( 1 { \leq j } { \leq l } )$ , B generates witnesses $\{ r _ { i } \} _ { n ^ { j } } ^ { j }$ and uses this batch as well as ck to generate a commitment batch $\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ for $\{ m _ { i } \} _ { n ^ { j } } ^ { j } . ~ B$ then submits

$\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ to its own signing oracle sig(sk, ⊥) of the digital signature scheme to get a signature $s ^ { j }$ . Finally, B returns an MB-pair $( \{ m _ { i } \} _ { n ^ { j } } ^ { j } , \ \delta _ { M B } )$ to $\scriptstyle A ,$ where $\delta _ { M B } = ( s ^ { j } , \{ r _ { i } \} _ { n ^ { j } } ^ { j } )$ . When A outputs $( \dot { \{ m _ { i } \} } _ { n } ^ { * } , \delta ^ { * } { } _ { M B } )$ , B parses ${ \delta ^ { * } } _ { M B } = ( s ^ { * } , \{ r _ { i } \} _ { n } ^ { * } ) .$ , computes a commitment batch $\{ m c _ { i } \} _ { n } ^ { * }$ from $\{ m _ { i } \} _ { n } ^ { * }$ and $\{ r _ { i } \} _ { n } ^ { * } ,$ and outputs a message-signature pair $( \{ m c _ { i } \} _ { n } ^ { * } , s ^ { * } )$ . Obviously, Pr[Case 1] equals the probability of B to break unforgeability of the digital signature, which happens with negligible probability.

In the second case, the adversary A could be used to build an adversary B to break binding of the string commitment scheme. At the beginning, B is given a commitment key ck of the string commitment scheme and generates a public-secret key pair (pk, sk) of the digital signature scheme. B then generates a public key of PVS scheme $P K = ( p k , c k )$ and gives PK to A. B simulates the oracle Sign(PK, SK, ⊥) as follows. When A queries a message batch $\left\{ m _ { i } \right\} _ { n ^ { j } } ^ { j } ( 1 { \leq } j { \leq } l )$ , B generates witnesses $\{ r _ { i } \} _ { n ^ { j } } ^ { j }$ and uses $\left\{ \boldsymbol { r } _ { i } \right\} _ { n ^ { j } } ^ { j }$ as well as ck to generate a commitment batch $\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ for $\{ m _ { i } \} _ { n ^ { j } } ^ { j }$ . B then signs $\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ by using sk to get a signature $s ^ { j } .$ Finally, B returns an MB-pair $( \{ m _ { i } \} _ { n ^ { j } } ^ { j } , \ \delta _ { M B } )$ to A, where $\delta _ { M B } = ( s ^ { j } , \{ r _ { i } \} _ { n ^ { j } } ^ { j } )$ . When A outputs $( \{ m _ { i } \} _ { n } ^ { * } , \ \delta _ { M B } ^ { * } )$ , B finds the message batch $\left\{ m _ { i } \right\} _ { n ^ { j } } ^ { j } ~ ( 1 { \leq } j { \leq } l )$ submitted by A with $\{ m _ { i } \} _ { n ^ { j } } ^ { j } \ \neq \{ m _ { i } \} _ { n } ^ { * }$ but $\{ \tilde { m } c _ { i } \} _ { n ^ { j } } ^ { j } ~ = ~ \{ m c _ { i } \} _ { n } ^ { * }$ . B then finds a message $m _ { i } \in \{ m _ { i } \} _ { n ^ { j } } ^ { j }$ and a message $m _ { i } ^ { \prime } \in \{ m _ { i } \} _ { n } ^ { * }$ satisfying the condition commit(ck, mi, ri) = commit(ck, $m _ { i } ^ { \prime } , ~ r _ { i } ^ { \prime } )$ and outputs $( m _ { i } , \ r _ { i } , \ m _ { i } ^ { \prime } , \ r _ { i } ^ { \prime } )$ . Obviously, Pr[Case 2] equals the probability of B to break binding of the string commitment scheme, which is negligible.

Theorem 2. If the digital signature scheme $\Pi _ { D }$ is unforgeable, then our construction of PVS scheme Q achieves CB-unforgeability.

Proof. The adversary A could be used to construct an adversary B to break unforgeability of the digital signature scheme. At the beginning, B is given a public key pk of the digital signature scheme and generates a commitment key ck of the string commitment scheme. B then generates a public key of PVS scheme $P K = ( p k , c k )$ and gives PK to A. B simulates the oracle $\mathsf { P r i S i g n } ( S K , P K , \perp )$ as follows. When A queries a message batch $\{ m _ { i } \} _ { n ^ { j } } ^ { j }$ and witnesses $\{ r _ { i } \} _ { n ^ { j } } ^ { j } , \boldsymbol { B }$ uses $\{ r _ { i } \} _ { n ^ { j } } ^ { j }$ n n  as well as ck to generate a commitment batch $\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ for $\{ m _ { i } \} _ { n ^ { j } } ^ { j } . \ B$ further queries $\{ m c _ { i } \} _ { n ^ { j } } ^ { j }$ to its own signing oracle $\mathsf { s i g } ( \bar { s } k , \perp )$ to get a signature sj . B then returns a CB-pair $( \{ m c _ { i } \} _ { n ^ { j } } ^ { j } , \ \delta _ { C B } ^ { j } )$ to A, where $\delta _ { C B } ^ { j } \ : = \ : s ^ { j }$ . When A Obviously, outputs $( \{ m c _ { i } \} _ { n } ^ { * } , \tilde { \delta } ^ { * } { } _ { C B } )$ $\mathbf { A d v } _ { \mathcal { A } } ^ { C B - u n f } [ \mathrm { P V S } ]$ , B directly outputs n equals the probability of B to $( \{ m c _ { i } \} _ { n } ^ { * } , \ \delta ^ { * } { } _ { C B } )$ . break unforgeability of the digital signature scheme, which is negligible. 

Theorem 3. If the string commitment scheme $\Pi _ { S }$ is binding, then our construction of PVS scheme Q achieves binding.

Proof. The adversary A could be used to construct an adversary B to break binding of the string commitment scheme. At the beginning, B is given a commitment key ck of the string commitment scheme and generates a public-secret key pair $( p k , s k )$ of the digital signature scheme. B then generates a public-secret key pair (PK, SK) of PVS scheme with $\overset { \triangledown } { P } K = ( p \bar { k } , c k )$ and $S K = { \dot { s } } k$ and gives (PK, SK) to A. Suppose A outputs $( \{ m _ { i } \} ^ { 1 } { } _ { n } , \{ r _ { i } \} ^ { 1 } { } _ { n } , \{ \stackrel {  } { m _ { i } } \} ^ { 2 } { } _ { n } , \{ r _ { i } \} ^ { 2 } { } _ { n } , \{ m c _ { i } \} _ { n } , \{ \stackrel {  } { \delta _ { C B } } \}$ satisfying the condition Check $( P K , \{ m _ { i } \} ^ { 1 } { } _ { n } , \{ r _ { i } \} ^ { 1 } { } _ { n } , \{ m { c } _ { i } \} _ { n } ,$ $\delta _ { C B } ) \ \to \ \mathcal { I }$ Accept ∧ Check(PK, $\{ m _ { i } \} _ { ~ n } ^ { 2 } , ~ \{ r _ { i } \} _ { ~ n } ^ { 2 } , ~ \{ m c _ { i } \} _ { n } , ~ \delta _ { C B } )$ → Accept $\wedge \{ m _ { i } \} ^ { 1 } { } _ { n } \neq \{ m _ { i } \} ^ { 2 } { } _ { n } . \ \bar { B }$ finds $m _ { i } \in \{ m _ { i } \} ^ { 1 } { } _ { n }$ and $m _ { i } ^ { \prime } \in \{ m _ { i } \} ^ { 2 } { } _ { n }$ satisfying the condition commit $\mathbf { \Phi } _ { c k , \ m _ { i } , \ r _ { i } } )$ = commit(ck, $m _ { i } ^ { \prime } , r _ { i } ^ { \prime } { \stackrel { . } { ) } } \wedge { \stackrel { . } { m } } _ { i } \not = m _ { i } ^ { \prime }$ and outputs $( m _ { i } , \ r _ { i } , \ m _ { i } ^ { \prime } ,$ $r _ { i } ^ { \prime } )$ . Obviously, $\mathbf { A d v } _ { A } ^ { b i n d } [ \mathrm { P V S } ]$ equals the probability of B to break binding of the string commitment scheme, which is negligible. 

Theorem 4. If the string commitment scheme $\Pi _ { S }$ is hiding, then our construction of PVS scheme Q achieves privacy.

Proof. The adversary A could be used to construct an adversary B to break hiding (semantic security of multiple messages) of the string commitment scheme. At the beginning, B is given a commitment key ck of the string commitment scheme and generates a public-secret key pair (pk, sk) of the digital signature scheme. B then generates a public key of PVS scheme $P K = ( p k , c k )$ and gives PK to A. B simulates the oracle $\mathsf { P r i S i g n } ( P K , S K , \perp )$ as follows. When A submits $( \{ m _ { i } \} _ { n } ^ { 1 } , \{ m _ { i } \} _ { n } ^ { 2 } )$ , B submits $( \{ m _ { i } \} _ { n } ^ { 1 } , \{ m _ { i } \} _ { n } ^ { 2 } )$ to its own committing oracle of the string commitment scheme to get a commitment batch $\{ m c _ { i } \} _ { n } ^ { b }$ . B then runs $s \gets$ $\mathsf { s i g } ( \bar { \{ } m c _ { i } \} _ { n } ^ { b } ,$ , sk), sets $\delta _ { C B } = s ,$ and returns $( \{ m c _ { i } \} _ { n } ^ { b } , \delta _ { C B } )$ to A. Suppose A outputs b0. B also outputs b0 as its guess. Obviously, $\mathbf { A d v } _ { \mathcal { A } } ^ { p r i v } [ \mathrm { P V S } ]$ equals the advantage of B to break hiding of the string commitment scheme, which is negligible.

# 5 SRTS: PROTOCOL DESIGN

In this section, we focus on SRTS. It consists of three protocols: product batch transfer, product batch arbitration and auditable item-level arbitration.

# 5.1 Initialization

In SRTS, the three participants leverage existing secure network communication protocols (such as SSL/TLS) to achieve reliable message exchange. When two participants need to exchange messages, they first authenticate the identity of each other and then establish a secure channel to exchange messages.

Both the Relaynode and Receiver need to have their own public-private key pairs of digital signature scheme. Their public keys need to be certified by the key authority and published, so that anyone can verify the validity of their signatures.

To guarantee the security of SRTS, Sender needs to generate a public-secret key pair (PK, SK) of PVS scheme and requests a certificate for PK from a key authority so that anyone can verify the validity of PK. Recall that a PK consists of a public key pk of a digital signature scheme and a commitment key ck of a string commitment scheme. The commitment scheme requires ck to be correctly generated by a trustworthy party to guarantee its security properties. To achieve this, we require the key authority to only accept pk from Sender, generates ck by itself to form a public key PK $\mathbf { \boldsymbol { \mathbf { \mathit { \sigma } } } } = ( p \boldsymbol { \boldsymbol { k } } , c \boldsymbol { k } )$ , and issues a certificate on PK.

![](images/a7954e1a49e22d396164dd27f4b053cac18e841f1ca85d0611dc3b4aa9b93d8f.jpg)



Fig. 3: Product batch transfer in Relaynode case.

# 5.2 Product batch transfer

# 5.2.1 Message batch processing

To transfer a product batch of n products, Sender generates the production messages $\{ m _ { i } \} _ { n }$ for the product batch. Sender then generates n crypto-IDs for $\{ m _ { i } \}$ n through steps S1-S3:

S1: Sender runs the PriSign() algorithm of PVS scheme to generate a CB pair for $\{ m _ { i } \} _ { n }$ and witnesses:

$$
\left(\left\{m c _ {i} \right\} _ {n}, \delta_ {C B}, \left\{r _ {i} \right\} _ {n}\right) \leftarrow \operatorname{PriSign} (P K, S K, \left\{m _ {i} \right\} _ {n})
$$

S2: Consider the commitment batch $\{ m c _ { i } \} _ { n }$ in the CB pair. Notice that $\{ m c _ { i } \} _ { n }$ represents a long message $m c _ { 1 } \tilde { | } | m c _ { 2 } | | . . . | | m c _ { n }$ . For each commitment mci, Sender concatenates $m c _ { i }$ with an in-batch index i, where i is the position of $m c _ { i }$ in the long message. Sender then encodes each indexed commitment i||mci as a crypto-ID idi and stores the n crypto-IDs into the n product tags. Sender attaches a batch tag to the product batch and stores the common signature δCB into it. Notice that a commitment mci is actually a random element of a group G, which can properly serve as a general ID to uniquely identify a tag.

S3: Sender creates a batch record in its database. The batch record contains a two-layer index structure. The common signature $\delta _ { C B }$ of the CB pair is used as the first-layer index for the whole batch record. The crypto-IDs are used as the second-layer index for the individual elements of both the production messages and the witnesses:

$$
\left(\delta_ {C B}, \{i d _ {i} | | m _ {i} \} _ {n}, \{i d _ {i} | | r _ {i} \} _ {n}\right)
$$

# 5.2.2 Sender → Relaynode

The process is shown in Figure 3 and described as follows. Sender directly transfers the product batch to Relaynode. Upon receiving it, Relaynode can use the tag carried cypto-IDs to identify and track each product in the batch. Relaynode can also collect the cypto-IDs from the product tags as well as the common signature from the batch tag to recover a CB pair through steps S1-S2:

S1: Relaynode concatenates the collected cypto-IDs following the order of their concatenated in-batch indexes to recover a commitment batch $\{ m c _ { i } \} _ { n } ;$ :

$$
\{m c _ {i} \} _ {n} = m c _ {1} | | m c _ {2} | |... | | m c _ {n}
$$

Relaynode then combines the commitment batch with the collected common signature to recover the CB pair:

$$
\left(\left\{m c _ {i} \right\} _ {n}, \delta_ {C B}\right)
$$

S2: Relaynode runs the PriVerify() algorithm of PVS scheme to verify if the CB pair is valid:

![](images/c92193ad8dacc57749e0d945491aba88392801fa31bbb75b95d7c772377082e7.jpg)



Fig. 4: Product batch transfer in Receiver case.

$$
\text { PriVerify } (P K, \{m c _ {i} \} _ {n}, \delta_ {C B}) = \text { Accept? }
$$

If valid, Relaynode stores the CB pair $( \{ m c _ { i } \} _ { n } , \delta _ { C B } )$ as an evidence in its database. Later, Relaynode transfers the product batch to Receiver.

# 5.2.3 Relaynode → Receiver

The process is shown in Figure 4 and described as follows. Upon receiving the product batch from Relaynode, Receiver can use the tag carried cypto-IDs to identify and track each product in the batch. Receiver can also collect the cypto-IDs from the product tags as well as the common signature from the batch tag to recover an MB pair through steps S1-S4:

S1-S2: Similar with Relaynode, Receiver recovers a CB pair and runs the PriVerify() algorithm of PVS scheme to verify its validity.   
S3: If the CB pair $( \{ m c _ { i } \} _ { n } , \delta _ { C B } )$ is valid, Receiver returns the common signature $\delta _ { C B }$ in the CB pair to Sender to fetch the production messages and the witnesses:

$$
\left(\left\{i d _ {i} \right| \left| m _ {i} \right\rbrace_ {n}, \left\{i d _ {i} \right| \left| r _ {i} \right\rbrace_ {n}\right)
$$

S4: Receiver runs the Check() algorithm of PVS scheme to verify if the fetched production messages are the exact ones committed in the CB pair:

$$
\operatorname{Check} \left(P K, \left\{m _ {i} \right\} _ {n}, \left\{r _ {i} \right\} _ {n}, \left\{m c _ {i} \right\} _ {n}\right) = \text { Accept }?
$$

If valid, Receiver recovers an MB pair from the CB pair:

$$
\left(\{m _ {i} \} _ {n}, \delta_ {M B}\right) = \left(\{m _ {i} \} _ {n}, \left(\delta_ {C B}, \{r _ {i} \} _ {n}\right)\right)
$$

and stores the MB pair as an evidence in its database.

After the above four steps, Receiver accepts the fetched production messages $\{ i d _ { i } | | \bar { m } _ { i } \} _ { n }$ as valid for the received product batch. For each product with tag carried crypto-ID $i d _ { i } ,$ Receiver can easily search the corresponding production message $m _ { i }$ from $\{ i d _ { i } | | m _ { i } \} .$ n .

# 5.3 Product batch arbitration

# 5.3.1 Relaynode case

The process is shown in Figure 5 and described as follows. To prove batch non-repudiation for the product batch, Relaynode starts an arbitration with the authority through steps S1-S4:

S1: Relaynode sends its evidence $( \{ m c _ { i } \} _ { n } , \delta _ { C B } )$ (the CB pair) of the product batch to the authority.   
S2: The authority runs the PriVerify() algorithm of PVS scheme to verify the evidence:

$$
\operatorname{PriVerify} \left(P K, \left\{m c _ {i} \right\} _ {n}, \delta_ {C B}\right) = \text { Accept }?
$$

![](images/f2e2c4743b4fba036252a8f5d1ef38dcf6df0fb8bb30947e977a45e3134bbc8d.jpg)



Fig. 5: Product batch arbitration in Relaynode case.

S3: If Accept, the authority returns the common signature $\delta _ { C B }$ in the CB pair to Sender to fetch the production messages and the witnesses of the product batch:

$$
\left(\left\{i d _ {i} \right| \left| m _ {i} \right\rbrace_ {n}, \left\{i d _ {i} \right| \left| r _ {i} \right\rbrace_ {n}\right)
$$

S4: The authority runs the Check() algorithm of PVS scheme to verify if the fetched production messages are the exact ones committed in the evidence:

$$
\operatorname{Check} \left(P K, \left\{m _ {i} \right\} _ {n}, \left\{r _ {i} \right\} _ {n}, \left\{m c _ {i} \right\} _ {n}\right) = \text { Accept }?
$$

If Accept, the authority convinces the receipt of a product batch with each product associated with a production message $m _ { i } { \in } \{ m _ { i } \} _ { n }$ .

# 5.3.2 Receiver case

To prove batch non-repudiation for the product batch, Receiver starts an arbitration with the authority through steps S1-S2:

S1: Receiver sends its evidence $( \{ m _ { i } \} _ { n } , \delta _ { M B } )$ (the MB pair) of the product batch to the authority.   
S2: The authority runs the algorithm Verify() of PVS scheme to verify the evidence:

$$
\operatorname{Verify} (P K, \{m _ {i} \} _ {n}, \delta_ {M B}) \rightarrow \text { Accept? }
$$

If Accept, the authority convinces the receipt of a product batch with each product associated with a production message $m _ { i } { \in } \{ m _ { i } \} _ { r }$ n .

# 5.4 Auditable item-level arbitration

Auditable item-level arbitration supports a more flexible scenario where Relaynode/Receiver may want to prove item non-repudiation, i.e., receipt of a certain product (in a product batch) from Sender associated with a production message mi to the authority. The protocol involves exchange of attestations, which are signed messages. For simplicity, we use the notion Sign(m) to denote a signed message m as well as the corresponding signature.

# 5.4.1 Relaynode case

The process is shown in Figure 6 and described as follows. To prove item non-repudiation for a certain product, Relaynode starts an arbitration with the authority through steps S1-S4 (S1-S3 belong to item non-repudiation proof phase and S4 belongs to audit phase):   
S1: Relaynode concatenates a notion Proof-request with the commitment $m c _ { i }$ of the product, and signs the whole message to generate an attestation:

$$
\operatorname{Sign} _ {\text { Relaynode }} (\text { Proof - request } | | m c _ {i})
$$

![](images/4213651c0680c734e360a9bdacaa12df73d42d1c1101d954954ee7cc0ab2feac.jpg)



Fig. 6: Auditable item-level arbitration in Relaynode case.

Relaynode then sends this attestation to the authority. Notice that mci is contained in the CB pair stored by Relaynode.

S2: Upon receiving the attestation, the authority records it, sends the commitment $m c _ { i }$ to Sender and requests the latter to reveal the production message committed in $m c _ { i }$ .

S3: Upon receiving $m c _ { i } ,$ Sender decides whether to accept the authority’s request. If accept, Sender concatenates a notion Accept with a production message $m _  i , $ , and signs the whole message to generate an attestation:

$$
\operatorname{Sign} _ {\text { Sender }} (\text { Accept } | | m _ {i})
$$

If reject, Sender concatenates a notion Reject with the commitment $m c _ { i } ,$ and signs the whole message to generate an attestation:

$$
\mathrm{Sign} _ {\mathrm{Sender}} (\mathsf {R e j e c t} | | m c _ {i})
$$

Sender then returns its attestation to the authority.

On the other hand, the authority either checks if $m _ { i }$ is the exact production message committed in $m c _ { i }$ and records the attestation. If the first case happens, the authority convinces the receipt of a product associated with the production message $m _ { i } .$ . Finally, the authority informs the proof result to Relaynode.

S4: If a malicious Sender refuses to reveal the production message for a valid commitment $m c _ { i } ,$ then Relaynode can choose to send the CB pair, which includes $m c _ { i } ,$ to the authority to prove the validity of mci.

Efficiency: The design of the audit phase S4 enforces both Sender and Relaynode to correctly execute the item non-repudiation proof phase S1-S3; otherwise their malicious behaviours will be detected by the authority through S4. But if Sender and Relaynode correctly execute item non-repudiation proof phase, auditable item-level arbitration protocol will end and S4 will not be executed. From Figure 6, we can clearly see that the item non-repudiation proof phase only involves the commitment or the production message of the targeted product, and the CB pair of a product batch is not involved. Overall, we can conclude that our protocol in Relaynode case prunes the abundant overhead incurred by the rest products in the same batch.

# 5.4.2 Receiver case

Receiver can prove item non-repudiation for a certain product through four steps similar with the Relaynode case.

S1: Receiver sends an attestation:

$$
\operatorname{Sign} _ {\text { Receiver }} (\text { Proof - request } | | m _ {i})
$$

to the authority. Note that $m _ { i }$ is contained in the MB pair stored by Receiver.

S2: Upon receiving the attestation, the authority records it, sends the message $m _ { i }$ to Sender and requests the latter to decide if to accept the message.   
S3: If Sender decides to accept, it directly returns an attestation:

$$
\operatorname{Sign} _ {\text { Sender }} (\text { Accept } | | m _ {i})
$$

to the authority. Otherwise, Sender returns an attestation:

$$
\operatorname{Sign} _ {\text { Sender }} (\text { Reject } | | m _ {i})
$$

to the authority.

S4: Receiver sends the MB pair, which includes $m _ { i } ,$ to the authority to prove the validity of $m _ { i }$ .

Efficiency: The efficiency is similar with the Relaynode case, and we just ignore it here. Clearly, we can also conclude that our protocol in Receiver case prunes the abundant overhead incurred by the rest products (and protects the privacy of their production messages) in the same batch.

# 5.5 Security analysis

We now analyze the security of SRTS. Specifically, we focus on Batch privacy and Batch and Item non-repudiation.

# 5.5.1 Batch privacy

Consider the product batch transfer protocol of SRTS in which a product batch is transferred. Sender only stores a CB pair into the tags of the product batch. Due to privacy property of PVS scheme, it is infeasible for Relaynode to learn any non-trivial knowledge about the production messages from the CB pair. Formally, Relaynode can be described as the adversary defined in Definition 4 (privacy) and the security is proved in Theorem 4.

# 5.5.2 Batch non-repudiation

We analyze Batch non-repudiation in Relaynode case and Receiver case separately as follows.

Relaynode case: Consider the Relaynode case of the product batch arbitration protocol in SRTS. Suppose Relaynode wants to prove batch non-repudiation for a product batch. Relaynode shows the CB pair of the product batch for the authority to verify. Due to CB unforgeability of PVS scheme, the authority convinces receipt of a product batch with each product associated with a product message committed in mci. Formally, Relaynode can be described as a weak version of the adversary defined in Definition 2 (CB-unforgeability) and the security is proved in Theorem 2.

The authority then requests Sender to reveal the production messages $\{ m _ { i } \} _ { n }$ committed in the CB pair. Due to binding property of PVS scheme, Sender cannot reveal tampered production messages $\{ m _ { i } ^ { \prime } \} _ { r }$ n which can also pass the check. Formally, Sender can be described as the adversary defined in Definition 3 (binding) and the security is proved in Theorem 3.

Combining the above two steps, the authority convinces receipt of a product batch with each product associated with a production message $m _ { i } \in \{ m _ { i } \} _ { n }$ .

Receiver case: Consider the Receiver case of the product batch arbitration protocol in SRTS. Suppose Receiver wants to prove batch non-repudiation for a product batch. Receiver shows the MB pair of the product batch for the authority to verify. Due to MB unforgeability of PVS scheme, the authority convinces receipt of a product batch with each product associated with a production message $m _ { i }$ contained in the MB pair. Formally, Receiver can be described as the adversary defined in Definition 1 (MB-unforgeability) and the security is proved in Theorem 1.

# 5.5.3 Item non-repudiation

We analyze Item non-repudiation in Relaynode case and Receiver case separately as follows.

Relaynode case: Consider the Relaynode case of the auditable item-level arbitration protocol in SRTS. Suppose Relaynode wants to prove item non-repudiation for a certain product. The audit phase S4 enforces a malicious Sender to accept the revealing request for a valid commitment; since if the malicious Sender chooses to reject, then it must provide a reject attestation in S3 to the authority. In this case, Relaynode shows the CB pair to verify the commitment in S4. Due to CB unforgeability of PVS scheme, the authority confirms that the commitment is valid. As the reject attestation is signed by Sender, due to unforgeability of signature scheme, the authority can use this attestation to accuse that Sender rejects a valid commitment.

The audit phase S4 also enforces a malicious Relaynode to prove item non-repudiation for a valid product; since if Relaynode provides a fake commitment in S1, Sender can safely reject to reveal the production message committed in the commitment. In this case, the malicious Relaynode cannot show a valid CB pair to verify the fake commitment in S4 due to CB unforgeability of PVS scheme. Recall that Relaynode already provided a request attestation in S1 to the authority, which is signed by Relaynode. Due to unforgeability of signature scheme, this request attestation can be used by the authority to accuse that Relaynode requests to prove item non-repudiation for a fake product (commitment).

Receiver case: Consider the Receiver case of the auditable item-level arbitration protocol in SRTS. The analysis is similar with the Relaynode case, and we just ignore it here.

# 6 PERFORMANCE EVALUATION

# 6.1 Selection of crypto-primitives

Recall that PVS scheme builds on top of two cryptoprimitives: namely digital signature scheme and string commitment scheme. We now consider several instantiations of the two crypto-primitives that can be used to implement PVS scheme.

BLS signature scheme: We consider BLS signature scheme [33] as an instantiation of the digital signature scheme. In this scheme, a secret key is a random value x selected from an interval [0, q-1] where q is a prime number. The corresponding public key is $g ^ { x }$ where g is a generator of a group G with order $q .$ To sign a message m, one computes h=H(m) where H() is a hash function hashing m to an element of G, and computes a signature $s i g { = } h ^ { x }$ . Given $\scriptstyle { p k = g ^ { x } }$ and $s i g { = } h ^ { x } ,$ the verification of the signature sig is performed by checking the equivalence $e ( s i g , g ) { = } e ( H ( m )$ , $g ^ { x } { \bar { ) } }$ . Here, $e ( \cdot , \cdot )$ is a bilinear map $G \times G \to G _ { T }$ mapping two elements of group G to an element of group $G _ { T }$ .

Pedersen commitment scheme: We consider Pedersen commitment scheme [26] as an instantiation of the string commitment scheme. In this scheme, a commitment key ck comprises a generator g of a group G with prime order q and a random element h of G. To commit to a string m in an interval [0, q-1], one draws a random value r in [0, q-1] and computes the commitment $c o m { = } g ^ { m } h ^ { r }$ . To open a commitment, one sends the tuple $( m , r )$ to the verifier who checks whether $c o m { = } g ^ { m } h ^ { r }$ .

Hash commitment scheme: We consider Hash commitment scheme as another instantiation of the string commitment scheme, which can be used to replace Pedersen commitment scheme with security-efficiency tradeoff. A commitment of Hash commitment scheme is a hash value $\mathrm { H } ( m , r )$ , where H() is a collision-resistant hash function, m is the committed string and r is a random number.

Compared with the Pedersen commitment scheme, the Hash commitment scheme enjoys higher efficiency but suffers weaker security. The computation overhead of Hash commitment scheme is more efficient than Pedersen commitment scheme. Instead, Hash commitment provides informal hiding property. Although an output of a hash function is thought to hide the underlying input in some works [34], the hiding property of hash function is not formally defined and guaranteed in the cryptographic literature.

# 6.2 Computation overhead

We compare SRTS with the basic Item-level Solution (IS) as discussed in Section 2 in terms of cryptographic operations. According to our crypto selection, both IS and SRTS can be built on two compositions of digital signature and string commitment, namely “BLS signature + Perdersen commitment” and “BLS signature + Hash commitment”. We term the two instantiations as PE-based scheme and HA-based scheme. We compare the performance of PE-IS, HA-IS and PE-SRTS, HA-SRTS. The computation overhead of BLS signature is dominated by exponentiation operation $\mathbb { E } \mathrm { x p } _ { G }$ on group G and pairing operation $\mathtt { P a i r } _ { e }$ of bilinear map e. The computation overhead of Pedersen commitment is dominated by exponentiation operation $\operatorname { E x p } _ { G }$ on group G. The computation overhead of Hash commitment is dominated by hash operation H.

TABLE 3: Comparison of IS and SRTS in terms of cryptographic operations 

<table><tr><td></td><td>Sender</td><td>Relaynode</td><td>Receiver</td></tr><tr><td>PE-IS</td><td> $nExp_G + 2nExp_G$ </td><td> $2nPair_e$ </td><td> $2nPair_e + 2nExp_G$ </td></tr><tr><td>PE-SRTS</td><td> $Exp_G + 2nExp_G$ </td><td> $2Pair_e$ </td><td> $2Pair_e + 2nExp_G$ </td></tr></table>

Table 3 summarizes the cryptographic operations of PE-IS and PE-SRTS incurred at the three participants respectively, when a batch of n products are transferred through RTS system. The comparison of HA-IS and HA-SRTS is similar and is ignored. The computation benefit of SRTS is derived from the signature processing overhead (signature generation for Sender and signature verification for Relaynode and

![](images/418ad80a93c1b8430748bde126fc33e697bb4f5de91f29ca4c11d85eae2ca56d.jpg)



(a) Computation overhead (s) at Sender side

![](images/a2db2aff4f0399f11ec42d372f8eb3487240c4be5d08717245f6441916ee729f.jpg)



(b) Computation overhead (s) at Relaynode side

![](images/c6ef7c4354cbb9129167b1371f95aeed81c02b308d5d81b17d66e01b2393d1f6.jpg)



(c) Computation overhead (s) at Receiver side   
Fig. 7: Comparison of IS and SRTS.

Receiver). SRTS requires the three participants to process 1 signature while IS requires the three participants to process n signatures. As shown in Table 3, SRTS reduces computation complexity from $n { \mathrm { E x p } } _ { G }$ to ExpG at Sender side and from 2nPaire to $2 \mathtt { P a i r } _ { e }$ at both Relaynode and Receiver sides. Importantly, SRTS incurs constant computation complexity at Relaynode regardless of the size of the product batch, thus avoiding Relaynode as a bottleneck of the RTS system.

# 6.3 Tag memory overhead

We compare with the IS as a baseline in terms of tag storage overhead. Recall that SRTS requires each tag to store a crypto-ID, which is a commitment concatenated with an inbatch index. We set the in-batch index to be 16 bits long to support at most $2 ^ { 1 6 } { = } 6 5 5 3 6$ products in a batch. Compared with IS, SRTS avoids the tag storage of digital signatures. PE-IS and HA-IS raise 672 bits storage while PE-SRTS and HA-SRTS raise 336 bits storage. We see that SRTS saves about 50% tag storage overhead compared with IS. Note that SRTS achieves more tag storage benefit if other long-length digital signature schemes are adopted.

# 6.4 Experiment results

In our implementation, we adopt the Pairing Based Cryptography (PBC) libraries [35], [36], [37] to implement BLS signature, Pedersen commitment and Hash commitment. All the experiment results represent the average of 10 trials.

Each of Sender, Relaynode and Receiver has a backend server and multiple readers. The readers are used to bundle tag carried messages and forward the messages to the server via internal network for further computation. Current enterprises often own commercial-level servers to complete their computation tasks. In our experiments, we use a computation abundant PC to simulate the commerciallevel server of each of the three participants, and conduct our experiments on the PC. The PC is equipped with a 16- Core AMD Opteron Processor and 16GB RAM, running 64- bit Ubuntu 13.10.

We compare the performance of IS and SRTS at the three participants to transfer a batch of n products. In our experiment, we generate n random production messages. We vary n from 2000 to 10000. Figure 7 (a)-(c) show the experiment results at the three participants, respectively. The experiment results show that SRTS incurs far less computation

TABLE 4: Speed-up ratio of SRTS vs. IS 

<table><tr><td>Number of tags</td><td>2000</td><td>4000</td><td>6000</td><td>8000</td><td>10000</td></tr><tr><td>Sender side-PE</td><td>4.3</td><td>4.5</td><td>4.5</td><td>4.4</td><td>4.3</td></tr><tr><td>Sender side-HA</td><td>4.7</td><td>5.0</td><td>5.1</td><td>4.7</td><td>4.9</td></tr><tr><td>Relaynode side</td><td>1977</td><td>4262</td><td>6290</td><td>8097</td><td>10120</td></tr><tr><td>Receiver side-PE</td><td>3.7</td><td>3.7</td><td>3.7</td><td>3.7</td><td>3.6</td></tr><tr><td>Receiver side-HA</td><td>3.3</td><td>3.3</td><td>3.2</td><td>3.4</td><td>3.4</td></tr></table>

overhead compared with IS. To transfer a batch of 10000 products with PE-SRTS, Sender costs 845s (3662s with PE-IS), Relaynode costs 0.257s (2601s with PE-IS) and Receiver costs 2307s (8416s with PE-IS). Notice that at Relaynode side, SRTS incurs constant computation overhead regardless of the number of products. The reason is that Relaynode only needs to run PriVerify() algorithm once.

Table 4 lists the speed up ratio of SRTS against IS at the three participants. At Sender side, SRTS achieves 4.4 times to 5.2 times speed up (lines 1-2). At Relaynode side, the speed up of SRTS grows linearly with the number of products, from 2000 times to 10000 times (line 3). At Receiver side, SRTS achieves 3.2 times to 3.8 times speed up (lines 4-5). The experiment results confirm our complexity analysis shown in Table 3.

# 6.5 Parallelization of SRTS

A design advantage of SRTS is that it is highly parallelizable. In transferring a batch of n products, the computation task of Sender can be divided into n independent commitment computation tasks and a signing task, and the computation task of Receiver can be divided into n independent commitment computation tasks and a signature verifying task.

We implement a parallel version of SRTS and compare the computation overhead of parallel-SRTS and original SRTS to process a batch of n products. We vary n from 2000 to 10000. Figure 8 (a)-(b) show the experiment results at Sender and Receiver sides, respectively. Our results show that parallel-SRTS achieves obvious speed up compared with SRTS. To transfer a batch of 10000 products with PEparallel-SRTS, Sender costs 153s (755s with PE-SRTS) and Receiver costs 933s (2162s with PE-SRTS).

Table 5 lists the speed up ratio of parallel-SRTS and SRTS at Sender and Receiver sides. At Sender side, parallel-SRTS achieves 4 times to 5 times speed up (lines 1-2). At Receiver side, parallel-SRTS achieves 2 times to 2.3 times speed up (lines 3-4).

![](images/56fec87e80d229660bd622b161fe0624f1a2129c1cd817f62dc8359985bf07b2.jpg)



(a) Computation overhead (s) at Sender side

![](images/a64bd4bbed0b527f1f99ac82c517b1b630e160bafd7b1b0eaf698a48015747d8.jpg)



(b) Computation overhead (s) at Receiver side   
Fig. 8: Comparison of SRTS and parallel-SRTS.

TABLE 5: Speed-up ratio of parallel-SRTS vs. SRTS 

<table><tr><td>Number of tags</td><td>2000</td><td>4000</td><td>6000</td><td>8000</td><td>10000</td></tr><tr><td>Sender side-PE</td><td>4.1</td><td>4.8</td><td>5.0</td><td>4.8</td><td>4.9</td></tr><tr><td>Sender side-HA</td><td>4.0</td><td>4.2</td><td>4.2</td><td>4.6</td><td>4.5</td></tr><tr><td>Receiver side-PE</td><td>2.2</td><td>2.3</td><td>2.2</td><td>2.2</td><td>2.3</td></tr><tr><td>Receiver side-HA</td><td>1.9</td><td>2.1</td><td>2.0</td><td>2.1</td><td>2.2</td></tr></table>

# 6.6 Tolerating tag errors and failures

In SRTS, when a product batch is transferred in the RTS system, Relaynode and Receiver need to collect the crypto-IDs from the attached tags to recover a commitment batch, from which they can further derive a CB pair or an MB pair. However, RFID tag is not a robust medium to carry message. In specific, a tag may suffer from: (1) tag error, i.e., the tag carries a wrong crypto-ID; (2) tag failure, i.e., the tag loses its functionality and its crypto-ID cannot be read anymore.

To tolerate tag errors and tag failures, we propose to extend the concept of crypto-ID to design redundant crypto-ID. Our idea is to combine Reed-Solomon code (RS code) with crypto-ID. A Reed-Solomon code is termed as RS(n, k) with s-bits symbols. The RS encoder takes k s-bits symbols to generate n redundant s-bits codewords. The RS decoder can correct up to s errors or up to r erasures with $2 s + r <$ 2t.

Recall that a crypto-ID is an indexed commitment i||mci. For a product batch with n products, we encode the corresponding commitment batch $\{ m c _ { i } \} _ { n } = m c _ { 1 } | | m c _ { 2 } | | . . . | | m c _ { n }$ into a redundant commitment batch by encoding every k×s bits of the commitment batch into n×s bits code words. We then equally divide the redundant commitment batch into n pieces. For each piece rmci, we concatenate it with an index i and generate a redundant crypto-ID i||rmci. Clearly, our redundant crypto-IDs can tolerant tag errors and tag failures.

We compare the performance of RS code with that of PE-SRTS. We use the implementation of a popular RS(255, 223) code [42]. We conduct two groups of experiments: (1) We use the PriSign() algorithm to generate a CB pair and then use the RS encoder to encode the commitment batch contained in the CB pair into a redundant commitment batch. (2) We use the RS decoder to decode a redundant commitment batch into a commitment batch, use the batch to form a CB pair, and run Check() algorithm on the CB pair. We measure the percentage of the time of the RS encoder/decoder against the total time and summarize the result in Table 6. From the table, we can see that the performance of RS code is negligible comparing with that of PE-SRTS. In the worst case, the overhead of RS code accounts for less than 0.2% of that of PE-SRTS.

TABLE 6: Comparison of RS code with PE-SRTS (seconds) 

<table><tr><td>Tag num</td><td>PriSign</td><td>Encode</td><td>Per</td><td>Check</td><td>Decode</td><td>Per</td></tr><tr><td> $2 \times 10^{3}$ </td><td>144</td><td>0.263</td><td>0.2%</td><td>131</td><td>0.063</td><td>0.048%</td></tr><tr><td> $4 \times 10^{3}$ </td><td>304</td><td>0.427</td><td>0.1%</td><td>309</td><td>0.129</td><td>0.042%</td></tr><tr><td> $6 \times 10^{3}$ </td><td>457</td><td>0.545</td><td>0.1%</td><td>453</td><td>0.188</td><td>0.041%</td></tr><tr><td> $8 \times 10^{3}$ </td><td>565</td><td>0.759</td><td>0.1%</td><td>610</td><td>0.253</td><td>0.041%</td></tr><tr><td> $10 \times 10^{3}$ </td><td>722</td><td>0.926</td><td>0.1%</td><td>714</td><td>0.318</td><td>0.045%</td></tr></table>

# 6.7 Implementation on commodity C1G2 RFID systems

SRTS does not require any modifications to the commodity passive tags or implement additional cryptographic functionality on the tags. Instead, a tag only needs to carry short crypto-IDs for reading and writing purposes. SRTS satisfies the 512 bits-storage constraint of commodity passive tags. We use the Write command to write data into RFID tags. One Write command allows the reader to write a 16-bit data block. To write large-length data, the reader needs to divide the data into multiple 16-bit blocks and write them via several Write commands. On the other hand, The Read command supports bulk data collection, which allows the reader to collect up to 512 bits per Read operation.

We use the Alien ALR 9900+ commodity RFID reader with regular parameters (e.g., 30dBm transmission power) to interrogate commodity passive RFID tags. The data transfer program is developed based on the Alien RFID reader SDK codes. Our implementation only requires the C1G2 routine operations. So we believe that our implementation can be easily extended to other commodity RFID platforms. We select two different types of widely used passive tags – ALN-9640 and AD-224 tags both with 512-bit user memory.

We focus on the communication overhead of data transfer between the reader and the tag. Figure 9 shows the communication overhead involved in the transfer of a 336- bits crypto-ID. As we can see, it requires more time to write a crypto-ID into tag, because as mentioned the Write command only allows the reader to write a 16-bit data block per Write operation. As a result, the reader needs to first divide the ID into several blocks and transfer them one by one which consumes longer time. In comparison, the Read operation consumes less time since it only requires one Read operation to collect the whole ID.

![](images/127506a03006785a01bb8eb82a38f2e69b8115490598763c24a335792c52b829.jpg)



Fig. 9: Overhead (ms) of a 336-bits crypto-ID.

# 7 RELATED WORK

Currently, many works have studied security issues in RFID systems. Private preserving authentication (PPA) protocols [7]–[15] are such a type of protocols which enable a reader to authenticate the validity of a tag in a privacy-preserving way. In these protocols, the reader interacts with the tag in several rounds for authentication. The interacted messages are computed based on a secret key shared between the reader and the tag. If the authentication is successful, the reader can locate a record from a backend database for the tag. The shared secret key can thus be treated as a crypto-ID for identification and index purposes. These works target at tag authentication problem and thus have totally different goals with our work.

Recently, some works have studied security issues in RFID-enabled supply chain systems [16], [17], [19]. Juels et al. [16] solve the key supply chain problem in RFID-enabled supply chain network. Secure keys are directly stored in tags by using secret sharing. During the supply chain, only authorized distributors can recover the secure keys from tags and use them to decrypt the data stored in tags. Although key supply chain simplifies data privacy protection, some desired security properties (e.g., data non-repudiation) are not easy to be obtained. Blass et al. [17] propose a technique to authenticate whether a tag has been processed through a valid path in a supply chain network. The idea is to use polynomial signature together with homomorphic encryption, which allows the path information stored in a tag to be continuously updated when it flows through a valid path. Their technique provides authentication and privacy guarantee for the path information. However, the path information must be generated in fixed format (looks like random numbers), while we aim to provide security guarantee for general production messages. Chaves et al. [19] propose a solution to protect privacy of production message in RFID-enabled product recall. In their solution, sensitive production message can be encoded in a privacypreserving manner and stored in tags for problematic product identification. Their solution, however, does not consider data non-repudiation. Besides, our work targets at a different model of RFID-enabled supply chain systems comparing with all these works.

We design PVS scheme to provide security guarantees and reduce signature processing overhead, including both computation and storage, for large-scale RTS system. We notice that in the crypto literature, there are many other powerful signature schemes [38]–[41]. We next discuss the suitability of these schemes when deploying in RTS system. Designated verifier signature [38] can convince a designated

verifier the authenticity of a signed message. This scheme cannot be directly deployed in RTS system as it convinces a designated verifier in such a way that the verifier cannot prove the signature to a third party. In RTS system, however, sender needs to transfer non-repudiable messages to relaynode and receiver, so that the two can record these messages as evidences and later prove them to an authority for arbitration. Multi-signature [39], aggregate signature [40] and batch signature [41] are designed to reduce signature processing overhead. These schemes, however, fall in following drawbacks when deploying in RTS system. First, multi-signature and aggregate signature work in a multisigners scenario, while in RTS system, all the signatures are signed by sender. Second, batch signature fasts signature verification overhead, but does not reduce signature storage overhead. Finally, all the three schemes do not protect privacy of the signed messages, while message privacy (which we term as batch privacy) is a desired requirement in RTS system.

# 8 CONCLUSION

In this paper, we target at security and privacy issues in RFID supply chain systems. We consider RFID-enabled Third-party Supply chain (RTS) system. We analyze the essential structure of RTS system and identify three inherent requirements, including batch privacy, batch and item non-repudiation and batch efficiency, about production messages. We design a Secure RTS system called SRTS, which incorporates a Private Verifiable Signature (PVS) scheme, to achieve the desired requirements. With SRTS, the production messages of a product batch are equipped with privacy and non-repudiation properties and can be efficiently transferred in the RTS system. In the future work, we plan to improve SRTS so that the receiver can directly recover production messages from tag carried crypto-IDs, removing the communication overhead between the sender and the receiver.

# REFERENCES

[1] R. Want, “An Introduction to RFID Technology”, IEEE Pervasive Computing, vol. 5, issue 1, pp. 25-33, 2005.   
[2] G. Vannucci, A. Bletsas and D. Leigh, “A Software-Defined Radio System for Backscatter Sensor Networks”, IEEE Transactions on wireless communications, Vol. 7, No. 6, 2008.   
[3] “Toll Global Logistics Expects RFID to Provide Significant Savings”, http://www.rfidjournal.com/articles/view?7552   
[4] S. Cai, C. Su, Y. Li, R. Deng and T. Li, “Protecting and Restraining the Third Party in RFID-Enabled 3PL Supply Chains,” in Proceedings of ICISS, 2010.   
[5] “China e-commerce complaints and rights of public service platform”, http://b2b.toocle.com/zt/315/list–11–1.html.   
[6] B. Santos and L. Smith, “RFID in the Supply Chain: Panacea or Pandora’s Box?”, Communications of the ACM, Vol. 51, No. 10, 2008.   
[7] L. Lu, J. Han, R. Xiao and Y. Liu, “ACTION: Breaking the Privacy Barrier for RFID Systems”, in Proceedings of IEEE INFOCOM, 2009.   
[8] T. Li, W. Luo, Z. Mo and S. Chen, “Privacy-preserving RFID Authentication based on Cryptographical Encoding”, in Proceedings of IEEE INFOCOM, 2012.   
[9] T. Li and R. Deng, “Vulnerability Analysis of EMAP-An Efficient RFID Mutual Authentication Protocol”, in Proceedings of ARES, 2007.   
[10] A. X. Liu, L. A. Bailey and A. H. Krishnamurthy, “RFIDGuard: A Lightweight Privacy and Authentication Protocol for Passive RFID Tags”, Journal of Security and Communication Networks, Vol. 3, No. 5, 2010.

[11] T. Van Le, M. Burmester and B. de Medeiros, “ Universally Com-time efficiency in meeting arbitrary accuracy requirement. ZOEWe propose TIGHT, a cross-layer design for RF distance posable and Forward-secure RFID Authentication and Authenticat-                ounding in passive wireless systems, specifically the UHF ed Key exchange”, in Proceedings of ACM ASIACCS, 2007.n round. Moreover, ZOE rapidly converges to optimly requires 1-bit response from the RFID tags per e   
[12] M. Burmester, B. De Medeiros and R. Motta, “Robust, anonymousrameter configurations and achieves high estimation efficiency.tion round. Moreover, ZOE rapidly converges to optimal pa-RFID authentication with constant key-lookup”, in Proceedings ofe enhance the robustness of cardinality estimation over noisymeter configurations and achieves high estimation efficiency.RCS protocol while employs the methodologies of Bistatic ACM ASIACCS, 2008.   FID Reader and ana   
[13] A. Juels and S. Weis, “Defining strong privacy for RFID”, in                 ment RF distance bounding at physical layer. We have consid-Proceedings of IEEE PerCom, Workshop PerTec, 2007.dio/USRP platform in concert with the WISPannels. We implement a prototype system based o   
[14] T. Dimitriou, “A Secure and Efficient RFID Protocol that couldZOE only requires slight updates to the EPCglobal C1G2 stan-Radio/USRP platform in concert with the WISP RFID tags. make Big Brother (partially) Obsolete”, in Proceedings of IEEEOE only requires slight updates to the EPCglobal C1G2 stan-rocessing delay, spectral aspects and device synchronization. PerCom, 2006.     e have analy   
[15] C. C. Tan, B. Sheng and Q. Li, “Secure and Serverless RFID Au-formance of ZOE in large-scale settings. The results demon-dard. We also conduct extensive simulations to evaluate the per-Distance fraud, Guessing and Clocking attacks while it reduces thentication and Search Protocols”, IEEE Transactions on wirelessate that ZOE outperforms the most recent cardinality estima-rmance of ZOE in large-scale settings. The results demoncommunications, Vol. 7, No. 3, 2008.n protocols.ate that ZOE outperforms the moe time advantage during Deferred   
[16] A. Juels, R. Pappu and B. Parno, “Unidirectional Key Distributiondetection attacks. We implement a prototype and evaluate our Across Time and Space with Applications to RFID Security”, in heme for delay measurement, viability of response function Proceedings of USENIX Security, 2008.   
[17] E. Blass, K. Elkhiyaoui and R. Molva, “Tracker: Security andEFERENCES       1508 Privacy for RFID-based Supply Chains”, in Proceedings of NDSS,[1] Alien Technology, Morgan Hill, CA, USA, “Alien Technology,” [On-REFERENCES 2011. li   
[18] K. Elkhiyaoui, E. Blass and R. Molva, “CHECKER: on-site check-  [2] EPCglobal, Brussels, Belgium, “Class 1 Generation 2 UHF[1] Alien Technology, Morgan Hill, CA, USA, “Alien Technology,” [On-[16] T. Hao, R. Zhou, G. Xing, and M. Mutka, “Wizsync: Exploiting ing in RFID-based supply chains”, in Proceedings of ACM WiSec,air interface protocol standard “Gen 2”,” [Online]. Available:  [1] S. Brands and D. Chaum, “Distance bounding protocols,” in EURO-Wi-Fi infrastructure for clock synchronization in wireless sensor 2012.h[2] ECRnet   
[19] L. W. F. Chaves and F. Kerschbaum, “Industrial Privacy in RFID-[3] “Gen 2 RFID tools,” [Online]. Available: https://www.cgran.org/wiki/       [2] G. P. Hancke, “Design of a secure distance bounding channel for RFID,”[17] D. Allan and H. Machlan, “Time transfer using nearly simultabased Batch Recalls”, in Proceedings of Enterprise DistributedGen2 J. Netw. Comput. Appl., vol. 34, no. 3, pp. 877–887, May 2011. Object Computing Conference Workshops, 2008.[4] Ettus Research, Santa Clara, CA, USA, “Ettus Gen2[3] J. Munilla, A. Ortiz, and A. Peinado, “Distance bou   
[20] E. Liu and A. Kumar, “Leveraging information sharing to increaseAvailable: http://www.ettus.com[4] Ettus Research, Santa Clara, CA, USA, “Ettus Research,” [Online].void-challenges for RFID,” presented at the Workshop RFID Security, supply chain configurability”, in Proceedings of International Con-[5] “WISP platform,” [Online]. Available: http://wisp.wikispaces.comAvailable: http://www.ettus.comGraz, Austria, Jul. 2006.        SenSys, Toronto, ON, Canada, 2012. ference on Information Systems, 2003.[6] M. Buettner and D. Wetherall, “An em [5] “WISP platform,” [Online]. Available[4] K. B. Rasmussen, C. Castelluccia,   
[21] A. Melski, L. Thoroe and M. Schumann, “Managing RFID data informance,” in Proc. ACM MobiCom, 2008, pp. 223–234.[6] M. Buettner and D. Wetherall, “An empirical study of UHF RFID per-“Proximity-based access control for implantable medical devices,” in supply chains”, International Journal of Internet Protocol Technol-[7] J. I. Capetanakis, “Tree algorithms for packet broadcast channels,”formance,” in Proc. ACM MobiCom, 2008, pp. 223–234.Proc. ACM CCS, 2009, pp. 410–419. ogy, Vol. 2, Nos. 3/4, 2007.IEEE Trans. Inf. Theory,[7] J. I. Capetanakis, “Tree[5] N. Sastry, U. Shankar, and   
[22] A. Hofer, A. Knemeyer and P. Murphy, “The Roles of Procedural[8] S. Chen, M. Zhang, and B. Xiao, “Efficient information collectionIEEE Trans. Inf. Theory, vol. IT-25, no. 5, pp. 505–515, Sep. 1979.       synchronizing clocks,” in Proc. ACM SenSys, Berkeley, CA, USA, and Distributive Justice in Logistics Outsourcing Relationships”,protocols for sensor-augmented RFID networks,” in Proc. IEEE[8] S. Chen, M. Zhang, and B. Xiao, “Efficient information collection          2009. Journal of Business Logistics, 33(3): 196–209, 2012.INFOCOM, 2011, pp. 3101–3109.protocols for sensor-augmented RFID networks,       21] T. Schmid, P. Dutta, and M. Srivastava, “High   
[23] C. P. Schnorr, “Efficient identification and signatures for smart[9] K. Finkenzeller, RFID Handbook: Radio-Frequency IdentificationINFOCOM, 2011, pp. 3101–3109.          power time synchronization an oxymoron no more,” in Proc. cards”, CRYPTO, 1989.Fundamentals and A[9] K. Finkenzeller, RFACM/IEEE IPSN, Sto   
[24] S. Goldwasser, S. Micali and C. Rackoff, “The knowledge complex-[10] G. R. Grimmett and D. R. Stirzaker, Probability and Random Pro-Fundamentals and Applications. New York, NY, USA: Wiley, 2000.[8] M. G. Kuhn, “An asymmetric security mechanism for navigation signals,”[22] F. Ferrari, M. Zimmerling, L. Thiele, and O. Saukh, “Efficient netity of interactive proof-systems”, in Proceedings of STOC, 1985.cesses, 3rd ed. Oxford, U.K.: Oxford Univ. Press, 2001.[10] G. R. Grimmett and D. R. Stirzaker, Probability and Random in Proc. Inf. Hiding Workshop, 2004, pp. 239–252.work flooding and time synchronization with glossy,” in P   
[25] C. Schnorr, “Efficient signature generation by smart cards”, Jour-[11] H. Han, B. Sheng, C. C. Tan, Q. Li, W. Mao, and S. Lu, “Countingcesses, 3rd ed. Oxford, U.K.: Oxford Univ. Press, 2001.[9] Q. Ren and Q. Liang, “Throughput and energy-efficiency-aware pro-ACM/IEEE IPSN, Chicago, IL, USA, 2011. nal of Cryptology, 4(3):161–174, 1991.RFID tags efficiently and anonymou[11] H. Han, B. Sheng, C. C. Tan, Q. Li,tocol for ultra-wideband communicati23] S. Ganeriwal et al., “Estimating c   
[26] T. Pedersen, “Non-Interactive and Information-Theoretic Secure  RFID tags efficiently and anonymously,” in Proc. IEEE INFOCOM,A Cross-layer Approach,” IEEE Trans. Mobile Comput., vol. 7, no. 6,duty-cycling in sensor networks,” IEEE/ACM Trans. Netw., vol. Verifiable Secret Sharing”, in Proceedings of CRYPTO 1991.         2010, pp. 1–9.pp. 805–816, Jun. 2008.17, no. 3, pp. 843–856, Jun. 2009.   
[27] G. Fuchsbauer, “Automorphic Signatures in Bilinear Groups and         [12] M. Kodialam and T. Nandagopal, “Fast and reliable estimation[10] J. Clulow, G. P. Hancke, M. G. Kuhn, and T. Moore, “So near and yet[24] T. Schmid, Z. Charbiwala, Z. Anagnostopoulou, M. Srivastava, an Application to Round-Optimal Blind Signatures”, in Proceed-schemes in RFID systems,” in Proc. ACM MobiCom, 2006, pp.so far: Distance bounding attacks in wireless networks,” in Proc. ESAS,and P. Dutta, “A case against routing-integrated time synchroings of IACR, 2009.   322–333.2006, pp. 83–97.nization,” in Proc   
[28] “Alien Technology”, http://www.alientechnology.com, 2012.         [13] M. Kodialam, T. Nandagopal, and W. C. Lau, “Anonymous tra[11] K. B. Rasmussen and S. Capkun, “Realization of RF distance bound[25] Z. Yang, L. Cai, Y. Liu, and J. Pan, “Environment-a   
[29] “Class 1 Generation 2 UHF Interface Protocol Standard ‘Gen2’,         in Proc. USENIX Security, 2010, p. 25. EPCglobal”, http://www.epcglobalinc.org/standards/uhfc1g2,2] V. Pavel Nikitin and K. V. S. Rao, “Antennas and propagation in UHF        2012. 2012.RFI   
[30] S. Chen, M. Zhang and B. Xiao, “Efficient Information Collection[13] C. Cremers, K. B. Rasmussen, and S. Capkun, “Distance hijacking attackstime-synchronized link protocol for energy-constrained multi-Protocols for Sensor-augmented RFID Networks”, in Proceedingson distance bounding protocols,” in Proc. IEEE SP, 2012, pp. 113–127.     hop wireless networks,” in Proc. SECON, Reston, VA, USA, of IEEE INFOCOM, 2011.4] S. Capkun, M. Srivastava, 2006.   
[31] T. Li, S. Chen and Y. Ling, “Identifying the Missing Tags in a Largewith covert base stations, Netw. Embedded Syst. Lab., Los Angeles, CA, RFID System”, in Proceedings of ACM MobiHoc, 2010.   
[32] Y. Zheng and M. Li, “Fast Tag Searching Protocol for Large-Scale Ultra-Wideband Signals andZhenjiang Li (M’12) received the B.E. degree RFID Systems”, in Proceedings of IEEE ICNP, 2011.         Systems in Communication Engineering. Hoboken,from the Department of Comput   
[33] D. Boneh, B. Lynn and H. Shacham, “Short Signatures from the2004. Technology at Xi’an Jiaotong University, Xi’an, Weil Pairing”, Journal of Cryptology, 2004.6] J. Werb and C. Lanzl, “Designing a positioninChina, in 2007. He re   
[34] M. Farb, Y.H. Lin, H.J. Kim, J. McCune and A. Perrig, “SafeSlinger:and people indoors,” IEEE Spectrum, vol. 35, no. 9, pp. 71–78, Sep. 1998.Ph.D. degrees from the Department of Electronic Easy-to-Use and Secure Public-Key Exchange”, in Proceedings of7] U.S. Dept. Commerce. (2001, Jan.). Assessment of compatibility betweenand Computer Engineering and Department of ACM MobiCom 2013.ultra-wideband deviceCo   
[35] B. Lynn. “The pbc library”, http://crypto.stanford.edu/pbc/NTIA Spec. Publ. 01-43.Kong University of Science and Techno   
[36] “jPBC:[18] S. Rag Java, S. K Pairing and K. g Kong i Based, “Reco9 and Cryptography”,able patch slot an- respectively. His http://gas.dia.unisa.it/projects/ jpbctenna for circular polarization diversity,current research in   
[37] A. De Caro, and V. Iovino, “jPBC: Java pairing based cryptogra-vol. 3, no. 4, pp. 419–425, Sep. 2008.tributed systems and mobile computing. He is a phy”, in Proceedings of IEEE ISCC, 2011.9] J. D. Griffin and G. D. Durgin, “Completemember of the IEEE.   
[38] M. Jakobsson, K. Sako, and R. Impagliazzo, “Designated verifierradio and RFID systems,” IEEE Antennas Propag. Mag., vol. 51, no. 2, proofs and their applications”, in Proceedings of EUROCRYPT,pp. 11–25, Apr. 2009. 1996.0] R.   
[39] T. Okamoto. “A digital multisignature scheme using bijectiveCTU Prague, Prague, Czech Republic. [Online]. Available: http://www. public-key cryptosystems”, ACM Transactions on Computer Sys-attplus.eu/hamradio/projekty/article/cppl\_b.pdf tems, 1998.   
[40] D. Boneh, C. Gentry, B. Lynn, and H. Shacham, “Aggregate and   His current research interest includes wireless Verifiably Encrypted Signatures from Bilinear Maps”, in proceed-sensor networks. He is a student member of the ings of EUROCRYPT, 2003.

[41] M. Bellare, J.A. Garay, and T. Rabin, “Fast batch verification forComput., vol. 5, no. 1, pp. 25–33, Jan.–Mar. 2005.      [24] R. Want, “An introduction to RFID technology,” IEEE Pervasive[22] M. Jain et al., “Practical, real-time, full duplex wireless,” in Proc. ACM modular exponentiation and digital signatures”, in Proceedings of[25] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, “Season: ShelvingComput., vol. 5, no. 1, pp. 25–33, Jan.–Mar. 2005.MobiCom, 2011, pp. 301–312. EUROCRYPT, 1998.interference and j[25] L. Yang, J. Han, Y] S. Hong, J. Mehlman   
[42] RS code implementation, https://github.com/zxing/zxingProc. IEEE INFOCOM, 2011, pp. 3092–3100.               interference and joint identification in large-scale RFID systemslicing,” in Proc. ACM SIGCOMM, 2012, pp. 37–48.

![](images/1ec41990f65b1a881478c447b8462b62a864cb4026609f06833a4cf58f870edf.jpg)



Saiyu Qi received the B.S. degree in computera large RFID system,” in Proc. IEEE SECON, 2011, 2007. science and technology from Xi’an Jiaotong Uni-Yang, and J. Chen, RFID and Sensor Networks: Archi-M. Fischer, “Fully integrated passive UHF RFID versity, Xi’an, China, in 2008, and the Ph.D. de-ls, Security and Integrations. New York, NY, USA:Yang, and J. Chen, RFID and Sensor Networks: Archi- 16.7 μW minimum RF input power,” IEEE J. Solidgree in computer science and engineering from.ols, Security and Integrations. New York, NY, USA: Hong Kong University of Science and Technolo-. Li, “PET: Probabilistic estimating tree for large-scale gy, Hong Kong, in 2014.,” IEEE Trans. Mobile Co. Li, “PET: Probabilistic esti

He is currently an Assistant Professor with the2012.IEEE Trans. Mobile Comput., vol. 11, no. 11, pp. School of Cyber Engineering, Xidian Universi-. Li, “Fast tag searching protocol for large-scale RFID. 2012., and Y. Deval, “A 60 μW LNA for 2.4 GHz wireless ty, China. His research interests include appliedc. IEEE ICNP, 2011, pp. 363–372.. Li, “Fast tag searching protocol for large-scale RFID cryptography, cloud security, distributed system-n, D. Jin, C. Huang, and H. Min, “Evaluating and opti-c. IEEE ICNP, 2011, pp. 363–372. s, and pervasive computing.nsumption of anti-collision protn, D. Jin, C. Huang, and H. Min,       Bagga, “Distance bounding pro

![](images/d10d73e61fc367ff71adfc7b46efcabe75d9922796393b04e03deae951e3a5b9.jpg)



Yuanqing Zheng (S’11) received the B.S. degreeYuanqing Zheng received PhD degree from the2004. in electrical engineering and M.E. degree in com-School of Computer Engineering in NanyangYuanqing Zheng (S’11) received the B.S. degree      Cheng Li (S’13) received the B.E. degree from munication and information system from BeijingTechnological University in 2014. Before that hein electrical engineering and M.E. degree in com-the Department of Electronic and Engineering Normal University, Beijing, China, in 2007 andreceived the B.S. degree in Electrical Engineer-munication and information system from Beijing       at the University of Electronic Science and 2010, respectively, and is currently pursuing theing and the M.E. degree in Communication andNormal University, Beijing, China, in 2007 and Technology of China, Chengdu, China, in 2010. Ph.D. degree in computer engineering at NanyangInformation System from Beijing Normal Univer-      2010, respectively, and is currently pursuing theHe is currently a second year Ph.D. student Technological University, Singapore.sity, Beijing, China, in 2007 and 2010 respective-Ph.D. degree in computer engineering at NanyangCroatia: InTec Open, 2011.of Nanyang Technological University, Singapore. ly.Te iesHis

nd pervasive computing.He is currently an assistant professor withHis research interests include distributed systems     nsor networks. He is a student member of the the Department of Computing in the Hong Kongand pervasive computing. c=US&amp;lc=engIEEE. Polytechnic University. His research interest in-la, “ISM-band and Short Range Device Antennas,”

cludes human centered computing, mobile and wireless computing,           Texas Instrum. Inc., Dallas, TX, USA, 2005. RFID systems, etc. He is a member of IEEE and ACM.[36] Agilent Technologies Notes, Agilent PNA Microwave

![](images/6b7e7890f179cdc5ca13ffcf0c9be5ec42581a68406d6fde189a1f706deea269.jpg)



science and technology from Tsinghua University,Mo Li (M’06) received the B.S. degree in computerMo Li received the B.S. degree in computerPreneel, “Distance bounding in noisy environments,”       the Department of Computer Science and Beijing, China, in 2004, and the Ph.D. degree inscience and technology from Tsinghua University,science and technology from Tsinghua Univer-007, vol. 4572, pp. 101–115.Technology from Tsinghua University, Beijing, computer science and engineering from Hong KongBeijing, China, in 2004, and the Ph.D. degree insity, Beijing, China, in 2004, and the Ph.D. de-China, in 2004 and the Ph.D. degree from University of Science and Technology, Hong Kong,computer science and engineering from Hong Konggree in computer science and engineering fromthe Department of Computer Science and in 2009.University of Science and Technology, Hong Kong,Hong Kong University of Science and Technolo-Muhammad Jawad Hussain received the B.E. de-Engineering at Hong Kong University of He is currently an Assin 2009.gy, Hong Kong, in 2009.gree in avionics from theScience and Technology,

School of Computer Engineering, Nanyang Techno-He is currently an Assistant Professor with theHe is currently an Assistant Professor withEngineering (CAE), National University of ScienceHe is currently an Assistant Professor in logical University, Singapore. His research interestsSchool of Computer Engineering, Nanyang Techno-the School of Computer Engineering, Nanyangand Technology (NUST), Pakistan, in 2005 and theSchool of Computer Engineering at Nanyang include wireless sensor networking, pervasivelogical University, Singapore. His research interestsTechnological University, Singapore. His re-M.S. degree in information security from the Uni-Technological University, Singapore. His current computing, and mobile and wireless computing.include wireless sensor networking, pervasivesearch interests include wireless sensor net-versity of Electronic Science and Technology ofresearch interests includes wireless sensor he Association for Computing Machinery (ACM). Hecomputing, and mobile and wireless computing.working, pervasive computing, and mobile andChina (UESTC) in 2013. He is currently pursuing computing, mobile and wireless computing. He

won the ACM Hong KDr. Li is a member wireless computing.is a member of the I

nd the Hong Kong ICT Award Best Innovation and Research Grand Award inon the ACM Hong Kong Chapter Prof. Francis Chin Research Award in 2009Dr. Li is a member of the Association for Computing Machinery (ACM).engineering at UESTC. He has worked as a Design 2007.and the Hong Kong ICT Award Best Innovation and Research Grand Award inHe won the ACM Hong Kong Chapter Prof. Francis Chin Researchand Field Engineer for Electronic Warfare systems 2007.Award in 2009 and the Hong Kong ICT Award Best Innovation andfor over six years. Research Grand Award in 2007.His current research interests inXiang-Yan

![](images/d33a4ec0d261b72b5bccfdb0639f19f98351099a18eea695a14dd5fc1005c82a.jpg)



Li Lu (S’07–M’07) received the Ph.D. degreeLi Lu received the Ph.D. degree from the KeyUniversity, Beijing, China, in 1995, and the M.S. from the Key Lab of Information Security, ChineseLab of Information Security, Chinese Academy ofand Ph.D. degrees in computer science from Academy of Science, in 2007. He is an AssociateScience, in 2007. He is an Associate Professorthe University of Illinois at Urbana-Champaign, Professor with the School of Computer Science andwith the School of Computer Science and En-Champaign, IL, USA, in 2000 and 2001, respec-Engineering, University of Electronic Science andgineering, University of Electronic Science andtively. He is a Professor of computer science at Technology of China. His research interests includeTechnology of China. His research interests in-the Illinois Institute of Technology, Chicago, IL, RFID technology and system, wireless network andclude RFID technology and system, wirelessUSA. His current research interests include span network security. He is an member of the IEEEnetwork and network security. He is an membersensor networks and algorithms. He is a senior Communication Society and ACM.of the IEEE Communication Society and ACM.member of the IEEE.

![](images/57a4ec6ae9cafb90ba2b1859dd66f4ad67493b8987bc0fb16c081c073439a1ef.jpg)



from the Department of Computer Science and En-Yunhao Liu (M’02-SM’06) received the B.S.Yunhao Liu received the B.S. degree from the gineering, Shanghai Jiao Tong University in 2009.degree from the Automation Department,Automation Department, Tsinghua University, He is an Associate Professor with Shanghai JiaoTsinghua University, Beijing, China, in 1995,Beijing, China, in 1995, and the M.S. and Ph.D. Tong University. His research interests include mo-and the M.S. and Ph.D. degrees in computerdegrees in computer science and engineering bile computing, wireless networks, vehicular ad hocscience and engineering from Michigan Statefrom Michigan State University, East Lansing, Networks and network security. He is a member ofUniversity, East Lansing, MI, USA, in 2003MI, USA, in 2003 and 2004, respectively. He the IEEE Computer and the IEEE Communicationand 2004, respectively. He is a member ofis a member of the Tsinghua National Lab for Societies.the Tsinghua National Lab for InformationInformation Science and Technology and the Di-Science and Technology and the Director of therector of the Tsinghua National MOE Key Lab Tsinghua National MOE Key Lab for Informationfor Information Security, both in Tsinghua, China. Security, both in Tsinghua, China. His currentHis current research interests include distributed

research interests include distributed systems and wireless sensorsystems and wireless sensor networks/RFID, Cyber physical systems, networks/RFID, Cyber physical systemand IoT. He is a senior member of IEEE.