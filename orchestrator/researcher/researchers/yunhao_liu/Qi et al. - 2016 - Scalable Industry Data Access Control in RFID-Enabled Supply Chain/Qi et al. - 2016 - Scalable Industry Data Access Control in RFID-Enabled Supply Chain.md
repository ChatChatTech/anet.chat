# Scalable Industry Data Access Control in RFID-Enabled Supply Chain

Saiyu Qi∗, Yuanqing Zheng†, Mo Li‡, Yunhao Liu§ and Jinli Qiu¶

∗School of Cyber Engineering, Xidian University, China

†Department of Computing, The Hong Kong Polytechnic University, Hong Kong

‡School of Computer Engineering, Nanyang Technological University, Singapore

§TNLIST, School of Software, Tsinghua University, China

¶Department of Computer Science and Technology, Xi’an Jiaotong University, China

Abstract—By attaching RFID tags to products, supply chain participants can identify products and create product data to record the product particulars in transit. Participants along the supply chain share their product data to enable information exchange and support critical decisions in production operations. Such an information sharing essentially requires a data access control mechanism when the product data relates to sensitive business issues. However, existing access control solutions are illsuited to the RFID-enabled supply chain, as they are not scalable in handling a huge number of tags, introduce vulnerability to the product data, and perform poorly to support privilege revocation of product data. We present a new scalable industry data access control system that addresses these limitations. Our system provides an item-level data access control mechanism that defines and enforces access policies based on both the participants’ role attributes and the products’ RFID tag attributes. Our system further provides an item-level privilege revocation mechanism by allowing the participants to delegate encryption updates in revocation operation without disclosing the underlying data contents. We design a new updatable encryption scheme and integrate it with Ciphertext Policy-Attribute Based Encryption (CP-ABE) to implement the key components of our system.

Index Terms—Industry data, Access control, RFID, Supply chain

# I. INTRODUCTION

In supply chain data management, participants can attach RFID tags to products, automatically identify products and create product data to record the product particulars in transit. The product data can thus be shared among participants, which facilitates information exchange and supports critical decisions in production operations [1], [2].

To facilitate data management, a service provider is usually appointed to coordinate the data sharing between participants. Each participant only needs to communicate directly with the service provider for data submission/retreival. In such a paradigm, each product is associated with an RFID tag with a unique ID that can be used to index its relevant product data managed by the service provider. When a participant receives a tagged product, it can use the tag ID as an index to submit its own product data or retrieve the corresponding product data submitted by other participants. In practice, the service provider could be a commercial supply chain manager such as GT Nexus [3] or a certain participant in the supply chain.

Product data stored in the service provider can be closely related to sensitive business issues and thus the data privacy becomes a natural concern. Strict data access control should be applied to disallow unauthorized data access from other entities or even the service provider itself. For instance, the pharmaceutical supply chain tracks tagged drugs and establishes a pedigree for each drug, e.g., counterfeit certificate, time of delivery, manufacturers, etc [4]. The drug pedigrees should be accessed by retailers and consumers to check whether the drugs are from trustworthy participants [5]. However, drug pedigrees may contain sensitive business matters subject to various malicious accesses. Drug counterfeiters and competitive manufacturers can exploit software vulnerabilities to gain unauthorized access to the service provider; a curious service provider may actively explore the content of its managed drug pedigrees; and any attackers with physical access to the service provider can access all the drug pedigrees in memory. Therefore, participants highly desire the data confidentiality and access control based on participant defined policies.

A straightforward but inefficient approach is to encrypt product data using cryptographic primitives and distribute decryption keys only to authorized participants. A large scale supply chain, however, needs to handle millions of products going through many participants. The products can spread worldwide and thus the intermediate participants as well as the final consumer of a product are generally unknown in advance. Therefore, it is hard to manage and distribute decryption keys in advance.

In practice, instead of designating a particular partner, a participant may want to provide access to the ones with certain attributes. For instance, a USA drug manufacturer may allow access to the ones that have both ‘USA’ and ‘FDA’ attributes, or the ones who are ‘Retailer’ or ‘Consumer’. Recently, a new cryptographic primitive called Ciphertext Policy-Attribute Based Encryption (CP-ABE) [9] is proposed to provide attribute based access control. With CP-ABE, a user can specify access policies based on logical expressions over user attributes for data encryptions before uploading to a third-party database. A key authority assigns each user a credential corresponding to the set of attributes that describe the user’s features (e.g., company nationality, business domain, etc). CP-ABE ensures that only users with attributes satisfying the logical expression can decrypt the data. In addition, as the database only stores encrypted data, even the service provider cannot learn any nontrivial information about the data.

Despite those benefits, CP-ABE is ill-suited to secure the product data of RFID-enabled supply chains for three main reasons. First, CP-ABE was designed to protect data associated with users, providing data access control in user-level; it is thus not scalable to protect product data associated with products, which requires item-level data access control. Second, CP-ABE relies on a key authority to manage all the credentials of attributes, which is a target for compromise. If the key authority is compromised or the credentials are occasionally exposed, the product data of the whole supply chain can be decrypted. Third, CP-ABE introduces substantial credential issuing overhead for supply chain participants to revoke access privilege of product data in item-level.

In this paper, we develop a scalable industry data access control system for RFID-enabled supply chain that (1) provides item-level data access control and (2) enforces item-level privilege revocation.

Our system provides a new item-level data access control mechanism, which defines and enforces role attributes (for participants) and tag attributes (for products) to regulate itemlevel data access control. A participant may define an access policy to be a logical expression over the role attributes and a tag attribute. An authorized partner must have the credentials of both satisfactory role attributes and the tag attribute so as to access the corresponding data of the particular product, which preclude adversaries outside the supply chain (who lack the credential of tag attributes) or unauthorized participants within the supply chain (who lack the credential of satisfactory role attributes). More importantly, the credentials of role attributes for participants are issued by a key authority while the tag attributes and their credentials can be locally generated by participants and stored in tags for distribution. Our system uses this mechanism to address the first two limitations of CP-ABE. First, the mechanism scales to support millions of products where the generation and maintenance of their tag attributes and credentials do not have to go through the key authority. Second, since the key authority only manages the credentials of role attributes, compromising it does not expose the product data, which is encrypted by both role attributes and tag attributes.

Our system provides a new item-level privilege revocation mechanism in a way that overcomes the inefficiency hurdles of CP-ABE. Generally, our revocation mechanism consists of two steps. When a participant wants to revoke the data access privilege of some participants for a product, it first updates the tag attribute/credential pair stored in the tag. It then delegates the service provider to update the tag attribute contained in the access policies of the corresponding encrypted product data without revealing any additional information about the data. Our system uses this mechanism to address the third limitation of CP-ABE. The mechanism does not involve the key authority to issue any credentials to participants and only incurs minimal computation and communication overhead. We believe that our item-level privilege revocation mechanism could greatly enhance the flexibility and security of our system. For instance, an intermediate participant may leave the supply chain after completing its production tasks or be temporally compromised by an attacker. In both cases, the downstream participant of the leaved participant can immediately revoke the leaved one’s data access privilege about the products.

![](images/795d480a1b1a0877d0695eb84dc5d5dc9c277879a0542bfdbaf7df09e6dde2de.jpg)



Fig. 1. An example of an RFID-enabled supply chain consisting of three participants. A tagged product flows through the chain and is sequentially processed by the participants. The participants rely on the service provider to share their product data.

We devise a new encryption scheme called updatable encryption and integrate with Ciphertext Policy-Attribute Based Encryption (CP-ABE) [9] to enforce the key components of our system. With complete design, we further evaluate the performance of our system through large-scale experiments to show its efficiency and scalability.

The rest of this paper is organized as follows. We describe the system model and problem in Section II. We present the design details of our system in Section III. In Section IV, we conduct theoretical analysis to prove the security properties of our schemes. In Section V, we examine the efficiency of our system. At last, we review the related works in Section VI and conclude this paper in Section VII.

# II. SYSTEM MODEL AND PROBLEM DESCRIPTION

# A. RFID-enabled Supply chains

An RFID-enabled supply chain is typically composed of three components: RFID tags (attached to products), readers (owned by participants for tag interrogation) and a database (at the service provider for data management). Supply chain participants (e.g., manufacturers, deliverers, and retailers) create, store, and share product data through the service provider and leverage the RFID tags to track the product data in the database.

Figure 1 depicts an illustrative example, where the supply chain consists of three participants. When a product enters the supply chain, the product is labeled with a tag. The tagged product then flows through the supply chain and is sequentially processed by the participants. Each participant generates its own data record about the product. The three participants rely on a service provider to share their product data, i.e., each participant can submit its product data record to the provider or retrieve the product data records submitted by others from the provider.

As for the supply-chain structure, we assume that participants may only know their direct upstream and downstream participants and may continuously join and leave the chain. For ease of presentation, we assume that one centralized service provider is appointed for data management. In practice, the service provider can be deployed in a distributed manner or in a cloud.

![](images/ad6d35a5913e0ddc7fb2e3c076ce49029d1700736f9af6a3795206869c09df18.jpg)



Fig. 2. An example of data access control in an RFID-enabled supply chain consisting of three participants. For a tagged product, each participant generates a product data record, associates the record with an access policy, and submits it to the service provider for sharing purpose.

# B. Security model

In this paper, we consider honest but curious service provider, i.e., the service provider follows our proposed system in general, but may try to explore as much product data as possible based on participant inputs. We also consider that participants may try to access product data outside the scope of their access privileges independently or cooperatively. Communication channel between the participants and the service provider are assumed to be secured using security protocols like SSL.

# C. Design Requirements

We aim to develop a scalable industry data access control system for RFID-enabled supply chain. Figure 2 shows an example of data access control in an RFID-enabled supply chain consisting of three participants. When a tagged product flows through the supply chain, each participant generates a product data record (participant i for record i) and submits the record to the service provider. As these records can be closely related to sensitive business issues, each participant wants to specify an access policy for its record so that only certain authorized partners within the supply chain can access its record. For instance, policy 1 specified by participant 1 states that “Participant 2 can access”, which means that participant 2 is the only authorized partner to record 1.

In the following, we identify four design requirements that a scalable industry data access control system in RFID-enabled supply chain should support:

• Data privacy: The basic design requirement is to prevent unauthorized entities from learning any nontrivial information about the product data submitted by participants. As the product data may contain highly sensitive information about products (e.g., counterfeit information, business relationship between participants, etc.), we need to strictly ensure data privacy.   
• Item-level access control: When a tagged product flows through a supply chain, each participant should be able to specify an access policy to its own data record about the product. The policy should be fine-grained so that the participant can precisely define the authorized partners.   
• Item-level privilege revocation: When a participant receives a tagged product, it can (optionally) choose to:

1) revoke the access privilege of its upstream participants to the product data records generated by its downstream participants, and 2) at the same time preserve the access privilege of the downstream participants to the product data records generated by the upstream participants.

• Scalability and efficiency: We want to achieve itemlevel access control and privilege revocation with high scalability. Also, we want to incur small memory cost that is affordable for low cost RFID tags and prevent implementing complex cryptographic algorithms on tags.

# D. Limitations of CP-ABE

CP-ABE fails to satisfy the above design requirements with efficiency and security guarantees mainly due to following three reasons.

First, CP-ABE is not scalable to protect product data associated with products, which requires item-level data access control. Suppose a tagged product enters the supply chain and a participant wants to share its data record about the product with its partners. As the data record is associated with the product, the participant regulates: (1) who are retailers in USA or France and (2) who have the privilege to process the product (within the same supply chain) can access this data record. Note that the condition (2) is necessary to preclude a retailer in USA but in another supply chain to access this record.

To enforce such a regulation, a strawman CP-ABE solution is to define a small set of role attributes (e.g. ‘retailer’, ‘USA’, ‘France’) to describe the features of participants and a large set of tag attributes to identify each tagged product, and appoint a key authority to issue credentials of proper attributes to each participant. In this way, the participant can specify an access policy (‘retailer’ AND (‘USA’ OR ‘France’) AND ‘TagAtt’) for its product data record; and a participant with the credential of attributes {‘retailer’, ‘USA’, ‘TagAtt’} can decrypt the data. However, this means that when a tagged product flows through the supply chain, each participant within the chain has to apply a credential for its role attributes as well as the tag attribute, which poses heavy computation and communication overhead on the key authority when handling millions of tagged products.

As the overhead of a credential is proportional to the number of its attributes, a better way is to manage role attributes and tag attributes separately. A participant applies from the key authority a credential of its role attributes at once and credentials of tag attributes for tagged products when needed. Unfortunately, CP-ABE disallows a participant to jointly use two different credentials to decrypt ABE-encryptions. This is due to the collusion-resistance property of CP-ABE, which states that multiple credentials can only be able to decrypt an encryption if at least one of the credentials could decrypt it on its own. Originally, this property is used to prevent large-scale data leakage from an attacker that manages to get a hold of a few credentials.

Second, all the participants have to trust the key authority to securely manage their credentials, which introduces vulnerability to their product data records. The credentials may be leaked due to ill-managements. An adversary can exploit software vulnerabilities to gain unauthorized access to servers; curious or malicious administrators at a hosting can snoop on the credentials; and attackers with physical access to servers can access all credentials in memory. The leaked credentials could be used to decrypt the product data of the whole supply chain stored in the service provider. Trusting a key authority to securely manage their credentials is often unacceptable to supply chain participants whose product data is highly sensitive.

![](images/7b64bb57150d7cae112c1228584c1841824a3d342b7f55eef65c3fcd1f54f64f.jpg)



Fig. 3. An example of item-level data access control. Participants with satisfiable attributes regarding the policy are partners and can access the record, while the ones with unsatisfiable attributes regarding the policy are non partners and cannot access the record.

Third, CP-ABE introduces substantial credential issuing overhead to support item-level revocation. To revoke the data access privilege of its upstream participants for a product, a participant has to inform the key authority to issue two credentials with the old tag attribute and a new tag attribute (respectively) for each of its downstream participants. For instance, suppose the revoked participants use the tag attribute ‘TagAtt’ to regulate the access policies of their product data records. A downstream participant with role attributes ‘retailer’ and ‘USA’ has to acquire a credential of attributes {‘retailer’, ‘USA’, ‘TagAtt’} and a credential of attributes {‘retailer’, ‘USA’, ‘New-TagAtt’} from the key authority. With the two credentials, the downstream participant can then: (1) use the new tag attribute ‘New-TagAtt’ to regulate the access policy of its product data record to preclude the access privilege of the revoked participants; (2) still use the former credential to access the product data records of the revoked participants; and (3) use the latter credential to access the product data records of other downstream participants.

# III. SYSTEM DESIGN

# A. Design principle

1) Item-level data access control: We use two types of attributes: role attributes and tag attributes to specify data access policies. Role attributes generally refer to different properties of participants. For instance, ‘USA’ describes the location of participants; ‘drug’ describes the production type of manufacturers. Role attributes alone however do not provide sufficient granularity to specify item-level data access policies. We thus introduce tag attributes to identify tagged products. A tag attribute is similar in essence to a unique tag ID, but is carefully designed to enforce cryptographic functionality. We use ‘TagAtt’ to denote a tag attribute.

Access policy to a product data record is defined as a logical expression over role attributes AND the associated tag attribute. As a result, a participant can specify access policy in item-level by incorporating the tag attribute in the policy when encrypting its product data record. Figure 3 illustrates an example where a participant shares its product data record with certain participants named partners. In this example, the partners are retailers in USA and France who have rights to process the product. The participant specifies the access policy as (‘retailer’ AND (‘USA’ OR ‘France’) AND ‘TagAtt’) and submits the policy enforced record to the service provider. By doing so, the participant with role attribute ‘producer’ and the one without the tag attribute ‘TagAtt’ are non partners and are precluded from the data record, while the participant with attributes satisfying the access policy is a partner and thus can access the data record. The service provider is also excluded from the data record since it does not have satisfiable attributes.

The data access privileges of participants are regulated by attribute credentials, i.e., an authorized participant must have the credentials of satisfiable attributes to decrypt product data records. Our system manages the credentials of attributes in a distributed manner. First, we use a key authority to manage role attributes and their credentials. We rely on the key authority to check if the role attributes match the properties of the participants when issuing the role attribute credentials. As the cardinality of role attributes is small and can be fixed in the system initialization, this management only requires the key authority to issue lightweight role attribute credentials to participants once in the system initialization. Second, we put the management of tag attribute credentials in the hands of the participants. As the cardinality of tag attributes is large (million-level) and cannot be fixed in the system initialization, this management relieves the key authority from issuing large amounts of tag attribute credentials during the production and disabling its ability to decrypt the product data records.

A participant encrypts its product data records with access policies defined from role attributes and tag attributes and uploads the policy enforced encryptions to the service provider. When a downstream participant receives a tagged product, it can retrieve the policy enforced encryptions (submitted by upstream participants) about the product from the service provider. Without credential of the tag attribute, however, the participant cannot decrypt. As large number of tagged products can flow through many participants within the supply chain, it is hard to distribute the credentials of tag attributes for all the participants in advance. To solve this problem, we leverage tags as a natural medium to distribute the credentials of their attributes to all the participants (within the supply chain). Although commodity passive tags only have very limited memory (e.g., 512 bits in ALN-9640 tags), our compact design of tag attribute credentials can fit in such a small space.

Enforcement of distributed credential issuing: We enforce the above distributed credential issuing mechanism by combing symmetric encryption scheme with CP-ABE [9]. We apply CP-ABE to encode the credentials of role attributes into CP-ABE decryption keys. Initially, the key authority generates a public/master key pair for a list of role attributes and publishes the corresponding public key. Each participant then requests the key authority for a credential of a set of role attributes which the participant possesses.

To incorporate tag attributes, we encode credentials of tag attributes into symmetric keys. When a tagged product enters the supply chain, the first participant of the chain generates a tag attribute and a symmetric key. The tag attribute-symmetric key pair forms a tag token and is stored in the attached tag. To prevent the tag token to be stolen by an outsider of the supply chain, a participant can use lightweight encryption schemes such as AES to encrypt the tag token and share the decryption key with its direct upstream and downstream participants.

We use double encryption paradigm to generate policy enforced encryption. Given a tagged product, a participant first encrypts to a logical expression over role attributes using the CP-ABE scheme and then encrypts the result by using the symmetric key contained in the tag token. Such a paradigm precisely enforces the access policy desired in our system (a logical expression over role attributes AND a tag attribute). Participants can decrypt the policy enforced encryption only if they possess the credentials of both satisfiable role attributes and the tag attribute.

2) Item-level privilege revocation: Item-level privilege revocation means that a participant could revoke the data access privileges of its upstream participants for a product. To preserve regular data access control after the revocation, the participant should be able to complete two tasks: 1) revoke the access privileges of its upstream participants to the product data records generated by its downstream participants, and 2) meanwhile preserve the access privileges of the downstream participants to the product data records generated by the upstream participants.

To complete task 1, the participants can locally update the tag token. To complete task 2, the participant can download the policy enforced encryptions of its upstream participants, use the old tag tokens to decrypt them and the new tag tokens to re-encrypt them, and submit them to the service provider. Such a solution, however, incurs high computation and communication overhead. Instead, our revocation mechanism allows the participant to delegate the service provider to update the access policies of the policy enforced encryptions of its upstream participants. The update operation is lightweight and does not require decryption, thus preserving data privacy. Comparing with CP-ABE, Our mechanism allows the participant to complete revocation operation by itself, thus does not involving the key authority to issue credentials to any participants.

Figure 4 illustrates a usage scenario of our revocation mechanism, where participant 2 wants to revoke the data access privilege of the upstream participant 1 for a product. To do so, participant 2 directly updates the tag token stored in the attached tag. It then sends a delegation request to the service provider to enable it to update the tag attribute of the policy enforced encryption submitted by participant 1. After that, participant 1 is precluded from the product data record of participant 3 as participant 3 will use the updated tag token to encrypt its data record, while participant 3 can still access the product data record of participant 1. During the above process, the key authority is not involved for credential issuing.

![](images/df2d9c6a04586be69de0d88091a7cb97f8397477d4760c9072385cdc03862057.jpg)



Fig. 4. An example of item-level revocation. Participant 2 updates the tag token stored in the attached tag and sends a delegation request to the service provider to enable it to update the tag attribute of the policy enforced encryption submitted by participant 1. After that, participant 3 will use the updated tag token to encrypt its data record and participant 1 is revoked.

Enforcement of access policy updating: General symmetric encryption schemes do not support access policy updates without decryption. To solve this problem, we design a new encryption scheme called updatable encryption scheme to support this functionality. We use this scheme to replace the general symmetric encryption scheme. As a result, the credentials of tag attributes become the secret keys of the updatable encryption scheme.

Our updatable encryption scheme is inspired by the Proxy Re-Encryption [16], in which a proxy can update an encryption under an old key to another encryption under a new key without decryption. Such an approach, however, requires 1024- bit encryption keys to achieve standard security, while current passive tags only have 512-bit user memory. Furthermore, the security of the scheme is not proved in proper security model. Besides, recent proposals [22]–[26] only allow one-time update operation, while we desire multi-time update operations to support multiple revocation operations by different participants within the same supply chain.

We design a new updatable encryption scheme to overcome the above drawbacks. The tag token consists of a tag attribute and a secret key of the updatable encryption scheme. Our design ensures the length of the tag token to be suitable for current passive tags. In a revocation operation, the participant sends a re-key to the service provider for it to update the access policies of policy enforced encryptions. Our design also ensures that the leakage of re-key does not break the data privacy and the policy enforced encryptions can be updated multiple times. We define two security models in supply chain setting to formalize malicious revoked participants and malicious service provider, respectively. We prove the security of our updatable encryption scheme in the two models.

# B. Cryptographic primitives: CP-ABE

The CP-ABE scheme [9] consists of four algorithms: (Setup, Encrypt, KeyGen, Decrypt).

• Setup(λ): On input a security parameter λ, the algorithm outputs a public key PK and a master key MSK.

• Encrypt(PK, RP, m): On input the public key PK, an access policy RP and a message m, the algorithm outputs an encryption CT.   
• KeyGen(MSK, S): On input the master key MSK and a set S of attributes, the algorithm outputs a private key SK. An attribute can be any string.   
• Decrypt(PK, CT, SK): On input the public key $P K ,$ an encryption CT and a private key SK, if the set S of attributes associated with SK satisfies the access policy $R P$ associated with CT, the algorithm outputs a message m.

# C. Updatable encryption

Our updatable encryption scheme builds on bilinear map.

Bilinear map: Bilinear map [21] is a mathematical tool to construct a rich types of cryptographic primitives. We present a few facts related to efficiently computable bilinear maps. Let $G _ { 1 } , G _ { 2 } , G _ { T }$ be groups of prime order $p .$ Let $g$ and h be generators of $G _ { 1 }$ and $G _ { 2 }$ respectively. Let e be a bilinear map: $G _ { 1 } \times G _ { 2 } {  } G _ { T }$ . The bilinear map e has three properties: (1) for all $u { \in } G _ { 1 } , \ v { \in } G _ { 2 }$ and $x , y \in Z _ { p } , e ( u ^ { x } , v ^ { y } ) { = } e ( u , v ) ^ { x y } ;$ $\left( 2 \right) e ( g , h ) \neq 1 ; \left( 3 \right) ( p , G _ { 1 } , G _ { 2 } , G _ { T } , e , g , h )$ can be efficiently generated and the bilinear map e: $G _ { 1 } \times G _ { 2 } {  } G _ { T }$ is efficiently computable.

Our updatable encryption scheme consists of six algorithms: (USetup, UKeyGen, UEncrypt, UDecrypt, UKeyUpdate, EncUpdate). The first algorithm USetup outputs some parameters for other algorithms to use. The subsequent three algorithms (UKeyGen, UEncrypt, UDecrypt) consist of a general symmetric key encryption scheme. The last two algorithms (UKeyUpdate, EncUpdate) are designed for key updating and encryption updating respectively. The functionalities of the six algorithms are shown as follows:

• USetup(λ): On input a security parameter $\lambda ,$ the algorithm outputs a public parameter ugp and a private parameter usp.   
• UKeyGen(usp): On input the private parameter usp, the algorithm outputs a secret key USK.   
• UEncrypt(m, ugp, USK): On input a message m, the public parameter ugp and a secret key USK, the algorithm outputs an encryption $C ^ { U P }$ .   
• UDecrypt $C ^ { U P }$ , USK): On input an encryption $C ^ { U P }$ and a secret key USK, the algorithm outputs a message m.   
• UKeyUpdate(USK): On input a secret key USK, the algorithm outputs a new secret key $U S K '$ and a re-key rk between the old/new key pair.   
• EncUpdate $( C ^ { U P }$ , rk): On input an encryption under USK and a re-key rk, the algorithm outputs a new encryption $C ^ { U P ^ { \ , } }$ under USK’. This algorithm updates an encryption under a secret key to an encryption under a new secret key by using the re-key between the two secret keys.

Table I presents the details of our updatable encryption scheme. We explain our design in three steps. We first show how to use a secret key USK to encrypt/decrypt an encryption $C ^ { U P }$ . We then describe how to update USK to a new key $U S K '$ as well as a re-key rk. Finally, we describe how to use rk

# TABLE I DETAILS OF UPDATABLE ENCRYPTION

• USetup(λ): Chooses a random number x∈ $Z _ { p }$ and computes $\scriptstyle { X = e ( g , h ) ^ { x } }$ . Outputs ugp=X and usp=x.   
• UKeyGen(usp): Given usp=x, chooses a random number a∈ $\because Z _ { p } ,$ computes $g ^ { a }$ and $h ^ { \frac { x } { a } }$ . Outputs $U S K { = } ( g ^ { a } , h ^ { \frac { x } { a } } )$ .   
• UEncrypt(m, ugp, USK): Given m, ugp=X and $U S K { = } ( g ^ { a } , h ^ { \frac { x } { a } } )$ , chooses a random number $s \in Z _ { p }$ and computes $C _ { 1 } { = } m X ^ { s }$ and $C _ { 2 } { = } ( g ^ { a } ) ^ { s } .$ . Outputs $C ^ { U P } { = } ( C _ { 1 } , C _ { 2 } )$ .   
• UDecrypt $( C ^ { U P } ,$ , USK): Given $C ^ { U P } { = } ( C _ { 1 } , ~ C _ { 2 } )$ and $U S K { = } ( g ^ { a } , \ h ^ { \frac { x } { a } } )$ , computes:

$$
e (C _ {2}, h ^ {\frac {x}{a}}) = e ((g ^ {a}) ^ {s}, h ^ {\frac {x}{a}}) = e (g, h) ^ {x s} = X ^ {s}
$$

Computes $\scriptstyle { m = { \frac { m X ^ { s } } { X ^ { s } } } }$ mXs and outputs m.

X • UKeyUpdate(USK): Given a USK, first updates USK as:

$$
U S K ^ {\prime} = \left(g ^ {a a ^ {\prime}}, h ^ {\frac {x}{a a ^ {\prime}}}\right) \leftarrow U S K = \left(g ^ {a}, h ^ {\frac {x}{a}}\right)
$$

where $a ^ { \prime }$ is chosen randomly from $Z _ { p } .$ . Sets $r k { = } a ^ { \prime } .$ . Outputs USK’ and rk.

• EncUpdate(CUP, rk): Given $C ^ { U P }$ and rk, updates $C ^ { U P }$ as:

$$
C ^ {U P ^ {\prime}} = (C _ {1}, C _ {2} ^ {r k}) \leftarrow C ^ {U P} = (C _ {1}, C _ {2})
$$

where (C1, Crk2 )=(C1, ((ga)s)a0 )=(C1, (gaa0 )s). Outputs $C ^ { U P ^ { \prime } } .$

to update $C ^ { U P }$ encrypted by USK to a new encryption $C ^ { U P ^ { \prime } }$ encrypted by USK’.

USK contains two elements $( g ^ { a } , h ^ { \frac { x } { a } } )$ . In the execution of UEncrypt(m, ugp, USK), $u g p { = } X { = } e ( g , h ) ^ { x }$ is used to generate a secret $X ^ { s }$ , which is used to hide m in an encryption element $C _ { 1 }$ . Also, the element $g ^ { a }$ of USK is used to generate another encryption element $C _ { 2 }$ . The final encryption $\bar { C } ^ { U P }$ consists of two encryption elements $( C _ { 1 } , C _ { 2 } )$ .

In the execution of UDecrypt $C ^ { U P } , U S K ) , h ^ { \frac { x } { a } }$ is used with $C _ { 2 }$ to reconstruct the secret $X ^ { s }$ through bilinear map. $C _ { 1 }$ is then divided by $X ^ { s }$ to recover the message m.

In the execution of UKeyUpdate(USK), both the elements $( g ^ { a } , h ^ { \frac { x } { a } } )$ of USK are refreshed by a random number $a ^ { \prime } \in Z _ { p }$ . The distribution of the new secret key $U S K '$ is identical to a secret key generated by UKeyGen(usp). The re-key rk between USK/USK’ is $a ^ { \prime }$ .

In the execution of EncUpdate(CUP, rk), the second element $C _ { 2 }$ of $C ^ { U P }$ is refreshed by rk. By doing so, we convert the encryption under USK into a new encryption under $U S K '$ . The update operation does not require any decryption.

# D. Item-level access control and revocation

In the following, we describe how to integrate our updatable encryption scheme with CP-ABE to achieve item-level access control and revocation. For clarity, we term “a tagged product” as “a tag” in this subsection.

Initialization: The service provider, key authority and participants need to exchange some cryptographic parameters. The key authority generates (PK, MSK)←Setup(λ) for its managed role attributes. It publishes PK and the role attributes and keeps MSK secret. Also, the first participant in the supply chain generates $( u g p , u s p ) {  } \mathsf { U S e t u p } ( \lambda )$ . The participant then delegates the service provider to publish ugp and keeps usp secret. On the other hand, each participant maintains a table to store the published PK, role attributes and ugp. Each participant then selects a subset of suitable role attributes and acquires the corresponding credential from the key authority.

Tag preparation: When a tag T enters the supply chain, the first participant generates a random number as tag attribute $a t t _ { T }$ and a secret key $U S K _ { T } {  } \mathsf { U K e y G e n } ( u s p )$ as the corresponding credential. The participant sets the tag token as (attT , $U S K _ { T } )$ and saves the tag token into $T .$ To reduce the tag storage overhead, the tag attribute $a t t _ { T }$ is derived from the secret key $U S K _ { T }$ by computing a hash function on it, so that attT does not need to be explicitly stored in the tag.

When T flows through the supply chain, each participant can perform three operations: data submission, data retrieval and privilege revocation by using the tag token.

Data submission: This operation allows a participant with tag token $( a t t _ { T } , U S K _ { T } )$ to submit a product data record $( a t t _ { T }$ , $C ^ { \bar { U } P } , P )$ to the service provider. $\boldsymbol { a t t } _ { T }$ is the tag attribute used for index purpose and $( C ^ { U P } , P )$ is a policy enforced encryption with the participant specified access policy P. The record generation process is presented in Algorithm 1.

Algorithm 1 {role attributes, PK, product data, ugp, tag token (attT , $U S K _ { T } ) \}$   
1: Define RP according to the role attributes
2: $CT = (P, C) \leftarrow \text{Encrypt}(PK, RP, \text{product data})$ 3: $C^{UP} \leftarrow U\text{Encrypt}(C, ugp, USK_{T})$ 4: Return ( $att_{T}, C^{UP}, P$ )

The participant defines a role based policy $R P$ and ABEencrypts the product data bound to RP. The resulted ABE encryption $C T$ contains a policy part P and an encrypted data part C. The participant then encrypts C by using the secret key $U S K _ { T }$ contained in the tag token to get the policy enforced encryption $( C ^ { U P } , P )$ . Finally, the participant submits a product data record $( a t t _ { T } , C ^ { U P } , P )$ to the service provider.

Our system uses general symmetric encryption scheme to increase the plaintext size supported by both updatable encryption scheme and CP-ABE. In particular, the updatable encryption scheme/CP-ABE only encrypts a symmetric key and uses the key to encrypt the plaintext. For simplicity, we do not explicitly indicate the usage of the general symmetric encryption scheme.

Data retrieval: This operation allows a participant with tag token (attT , USKT ) to retrieve and decrypt the product data records submitted by other participants. The participant uses the tag attribute attT as an index to retrieve all the submitted product data records about the tag and tries to decrypt them. For a retrieved record $( a t t _ { T } , C ^ { U P } , P )$ , the decryption process is presented in Algorithm 2.

Algorithm 2 {product data record $( a t t _ { T } , C ^ { U P } , P ) .$ tag token (attT , USKT ), PK, credential of role attributes}   
1: $C \leftarrow \text{UDecrypt}(C^{UP}, USK_{T})$ 2: $CT \leftarrow (P, C)$ 3: $m \leftarrow \text{Decrypt}(PK, CT, \text{credential of role attributes})$ 4: Return m

The participant decrypts $C ^ { U P }$ by using the secret key $U S K _ { T } .$ . The decrypted C and P forms a valid ABE encryption CT . After that, the participant uses its credential of role attributes to decrypt the ABE encryption.

Revocation: This operation allows a participant with the tag token $( a t t _ { T } , ~ U S K _ { T } )$ of a tag $T$ to revoke the data access privilege of its upstream participants for $T .$ The participant first generates a new secret key $U S K { ' } _ { T }$ and a re-key rk: $( U S K ^ { , } \tau , \ r k ) { \gets } \mathsf { U K e y U p d a t e } ( U S K _ { T } )$ . The participant updates the tag token to $( a t t ^ { \prime } _ { T } , U S K ^ { \prime } _ { T } )$ by overwriting the original tag token in $T .$ Note that the tag attribute is a hash of the secret key. As the secret key is updated from $U S K _ { T }$ to $U S K { ' } _ { T }$ , the tag attribute is also changed from attT to $\boldsymbol { a t t ^ { \prime } } _ { T }$ . The participant then uses $U S K { ' } _ { T }$ to generate policy enforced encryption for its product data. $\boldsymbol { \mathrm { B y } }$ doing so, the participant precludes its upstream participants from the newly uploaded data.

In addition, the participant needs to delegate the service provider to update the submitted policy enforced encryptions about T so that the downstream participants can still decrypt them with the new tag token. To do so, the participant sends $( a t t _ { T } , \ a t t _ { \ T } ^ { \prime } , \ r k )$ to the service provider. The latter uses the old tag attribute $\boldsymbol { a t t } _ { T }$ as an index to search all the submitted product data records about T . For each searched record (attT , ${ \dot { C } } ^ { U P } , P ) ,$ , the updating process is described in Algorithm 3.

Algorithm 3 {product data record $( a t t _ { T } , C ^ { U P } , P ) , ( a t t _ { T } , a t t ^ { \prime } _ { T } ,$ rk)}   
1: $C^{UP'} \leftarrow EncUpdate(C^{UP}, rk)$ 2: $(att'_{T}, C^{UP'}, P) \leftarrow (att_{T}, C^{UP}, P)$ 3: Return $(att'_{T}, C^{UP'}, P)$

The service provider first updates $C ^ { U P } { \mathrm { ~ a s ~ } } C ^ { U P }$ and then updates the record $( a t t _ { T } , C ^ { U P } , \bar { P } ) \mathrm { a s } ( a t t ^ { \prime } { } _ { T } , C ^ { U P ^ { \prime } } , P ) .$ . Note that the updated record now contains the new tag attribute $\acute { a t t ^ { \prime } } _ { T }$ so that all the downstream participants can use $\acute { a t t ^ { \prime } } _ { T }$ to index this record. After the update operation, all the downstream participants can still access these product data records using the new tag token.

# IV. SECURITY ANALYSIS

We first analyze the security properties of our updatable encryption scheme as the security of our system builds on these properties.

# A. Security analysis of updatable encryption scheme

In the following, we prove that our updatable encryption scheme provides data privacy against revoked participants as well as the service provider. We formally define the desired security properties based on interactive game, which consists of an adversary (a malicious revoked participant or the service provider) and a challenger (our updatable encryption scheme). The adversary interacts with the challenger to attack our scheme. We then show that our updatable encryption scheme satisfies these security properties.

The data privacy of an encryption scheme can be formalized as IND-CPA [27]. Comparing with the standard definition of IND-CPA, a revoked participant and the service provider also own additional knowledge about revoked secret key and rekeys, respectively. We thus extend IND-CPA to define two security properties: Revoked Secret Key Resistant (RSKR)- IND-CPA and Re-Key Resistant (RKR)-IND-CPA. We prove that our updatable encryption scheme satisfies the two security properties.

Definition 1. RSKR-IND-CPA: An updatable encryption scheme satisfies RSKR-IND-CPA if all polynomial time adversaries have at most a negligible advantage to win the following 3-phase game.

Phase 1: The challenger runs the algorithms of the updatable encryption scheme to generate a public parameter UGP, a private parameter usp, a secret key USK. The challenger returns (UGP, USK) to the adversary. Upon receiving the pair, the adversary returns a polynomial bounded number q to the challenger.

Phase 2: The challenger runs the algorithms of the updatable encryption scheme to generate a sequence of secret keys $U S K _ { 1 } , U S K _ { 2 } , \cdot \cdot \cdot , U S K _ { q }$ from USK. The challenger then allows the adversary to send a polynomial bounded number of queries. In each query, the adversary selects a number i∈[1, q], a message m and sends $( i , m )$ to the challenger. The challenger generates an encryption $C _ { i } ^ { U P }$ of m by $U S K _ { i }$ and returns $\bar { C } _ { i } ^ { U P }$ to the adversary.

Phase 3: The adversary selects a number $i ^ { * } \in [ 1 , \ q ]$ , generates two equal-length messages $m _ { 0 } ^ { * } , \ m _ { 1 } ^ { * }$ and returns a challenge $( i ^ { * } , \ m _ { 0 } ^ { * } , \ m _ { 1 } ^ { * } )$ to the challenger. The challenger selects a message $m _ { \eta } ^ { * }$ from $( m _ { 0 } ^ { * } , ~ m _ { 1 } ^ { * } )$ by flipping a fair bit $\eta .$ The challenger then generates an encryption $C _ { i ^ { * } } ^ { U P }$ of $m _ { \eta } ^ { * }$ by $U S K _ { i }$ ∗ and returns $C _ { i ^ { * } } ^ { U \bar { P } }$ to the adversary.

Finally, the adversary returns a guess $\eta ^ { \prime } .$ . If $\eta { = } \eta ^ { \prime }$ , the adversary wins the game. We define the adversary’s advantage in the above game as $| P [ \eta = \eta ^ { \prime } ] - \frac { 1 } { 2 } |$ .

Theorem 1. Our updatable encryption scheme satisfies RSKR-IND-CPA based on the Decisional Bilinear Diffie-Hellman (DBDH) assumption.

DBDH Assumption. Let $y _ { 1 } , ~ y _ { 2 } , ~ y _ { 3 } , ~ z { \in } Z _ { p }$ be chosen at random. Let g and h be the generators of $G _ { 1 }$ and $G _ { 2 }$ respectively. The DBDH assumption [21] is that no probabilistic polynomial-time adversary B can distinguish the tuple $( g , g ^ { y _ { 1 } }$ , $g ^ { y _ { 3 } } , h , h ^ { y _ { 1 } } , h ^ { y _ { 2 } } , e ( g , h ) ^ { y _ { 1 } y _ { 2 } y _ { 3 } } )$ from the tuple $( g , g ^ { y _ { 1 } } , g ^ { y _ { 3 } } , h$ , $h ^ { y _ { 1 } } , h ^ { y _ { 2 } } , e ( g , h ) ^ { z } )$ with more than a negligible advantage. The advantage of B is:

$$
\left. \right.\left| P \left[ \mathcal {B} \left(g, g ^ {y _ {1}}, g ^ {y _ {3}}, h, h ^ {y _ {1}}, h ^ {y _ {2}}, e (g, h) ^ {y _ {1} y _ {2} y _ {3}}\right)\right] = \right.
$$

$$
0 - P [ \mathcal {B} (g, g ^ {y _ {1}}, g ^ {y _ {3}}, h, h ^ {y _ {1}}, h ^ {y _ {2}}, e (g, h) ^ {z}) ] = 0 |
$$

where the probability is taken over the random choice of the generators g and $h ,$ the random choice of $y _ { 1 } , y _ { 2 } , y _ { 3 } , z$ in $Z _ { p } ,$ and the random bits used by B.

Proof: Suppose there exists a polynomial time adversary A that can break RSKR-IND-CPA of our updatable encryption scheme with advantage . We can construct an adversary B to break the DBDH assumption with advantage $\frac { \epsilon } { 2 }$ as follows:

The challenger of DBDH game selects three groups: $G _ { 1 }$ , $G _ { 2 } , \ G _ { T }$ with an efficient bilinear map e and generators of $G _ { 1 }$ and $G _ { 2 } \colon g , \ h$ . The challenger flips a fair bit $\mu .$ . If $\scriptstyle \mu = 0$ , the challenger generates $( Y _ { 1 } , Y _ { 2 } , Y _ { 3 } , Y _ { 4 } , Y _ { 5 } , Y _ { 6 } , Z ) = ( g , g ^ { y _ { 1 } }$ , $g ^ { y _ { 3 } } , h , h ^ { y _ { 1 } } , h ^ { y _ { 2 } } , e ( g , h ) ^ { y _ { 1 } y _ { 2 } y _ { 3 } } )$ ; otherwise it generates $( Y _ { 1 } , Y _ { 2 }$ , $Y _ { 3 } , Y _ { 4 } , Y _ { 5 } , Y _ { 6 } , Z ) = ( g , g ^ { y _ { 1 } } , g ^ { y _ { 3 } } , h , h ^ { y _ { 1 } } , h ^ { y _ { 2 } } , e ( g , h ) ^ { z } )$ . The challenger then gives the generated $( Y _ { 1 } , \ Y _ { 2 } , \ Y _ { 3 } , \ Y _ { 4 } , \ Y _ { 5 } , \ Y _ { 6 }$ , Z ) to B.

Setup. B computes $X { = } e ( Y _ { 2 } , Y _ { 6 } ) { = } e ( g , h ) ^ { y _ { 1 } y _ { 2 } }$ . B chooses a random number $\beta \in Z _ { p }$ and computes $( Y _ { 2 } ) ^ { \beta } { = } g ^ { y _ { 1 } \beta }$ and $Y _ { 5 } ^ { \frac { 1 } { \beta } } { = } h ^ { \frac { y _ { 1 } } { \beta } } { = } h ^ { \frac { y _ { 1 } y _ { 2 } } { y _ { 2 } \beta } }$ V . B sets $U G P { = } X$ and $U S K { = } ( g ^ { y _ { 1 } \beta } , h ^ { \frac { y _ { 1 } y _ { 2 } } { y _ { 1 } \beta } } )$ and returns (UGP, USK) to A. The distribution of the constructed (UGP, USK) is identical with the valid ones generated by the algorithms of updatable encryption scheme. After that, B receives q from A.

Query. B maintains a list with size q. When receiving a query $( i , m )$ from A, B checks if there exists a pair $( i , \beta _ { i } )$ in the list. If yes, B chooses a random number s∈ $Z _ { p }$ and constructs an encryption $C _ { i } ^ { U P }$ :

$$
C _ {i} ^ {U P} = (C _ {i 1}, C _ {i 2}) = (m X ^ {s}, (g ^ {\beta_ {i}}) ^ {s})
$$

If no, B chooses a random number $\beta _ { i } \in Z _ { p } ,$ adds $\left( i , \mathbf { \nabla } \beta _ { i } \right)$ into the listthen returns $C _ { i } ^ { U P }$ generates an encryptio to A. The distribution n CUP $C _ { i } ^ { { \hat { U } } P }$ as above. Be constructed encryption is identical to the valid ones generated by the algorithms of updatable encryption scheme with the secret key USKi.

Challenge. A submits a challenge $( { i ^ { * } } , { m _ { 0 } } ^ { * } , { m _ { 1 } } ^ { * } )$ to B. B flips a fair bit η, retrieves $( i ^ { * } , \beta _ { i ^ { * } } )$ from its maintained list and constructs an encryption $C _ { i ^ { * } } ^ { U P } \mathrm { : }$ :

$$
C _ {i ^ {*}} ^ {U P} = (C _ {i 1 ^ {*}}, C _ {i 2 ^ {*}}) = (m _ {\eta} ^ {*} Z, (Y _ {3}) ^ {\beta_ {i ^ {*}}})
$$

If µ=0, then $Z { = } e ( g , h ) ^ { y _ { 1 } y _ { 2 } y _ { 3 } }$ . Let $s { = } y _ { 3 }$ , then we have $C _ { i 1 ^ { * } } = m _ { n } ^ { * } e ( g , h ) ^ { y _ { 1 } y _ { 2 } y _ { 3 } } = m _ { n } ^ { * } ( e ( g , h ) ^ { y _ { 1 } y _ { 2 } } ) ^ { y _ { 3 } } = m _ { n } ^ { * } X ^ { s }$ and $C _ { i 2 ^ { * } } { = } ( Y _ { 3 } ) ^ { \beta _ { i ^ { * } } } { = } ( g ^ { \beta _ { i ^ { * } } } ) ^ { y _ { 3 } } { = } ( g ^ { \beta _ { i ^ { * } } } ) ^ { s }$ . The distribution of the constructed encryption is identical with the valid ones generated by the algorithms of updatable encryption scheme with the secret key USKi∗ . If $\mu { = } 1$ , then ${ \cal Z } { = } e ( g , h ) ^ { z }$ . We then have $C _ { i 1 ^ { * } } { = } m _ { \eta } ^ { * } e ( g , h ) ^ { z }$ . Since z is random, $C _ { i 1 ^ { * } }$ ∗ is actually a random element of $G _ { T }$ from the view of $\mathcal { A }$ and the constructed encryption reveals no information about ${ m _ { \eta } } ^ { * }$ .

Guess. A submits a guess $\eta ^ { \prime }$ of η. If $\eta ^ { \prime } { = } \eta$ , B will output $\mu ^ { \prime } { = } 0$ to indicate that it was given a valid DBDH-tuple; otherwise it will output $\mu ^ { \prime } { = } 1$ to indicate that it was given a random 4-tuple.

In the case where $\mu { = } 1$ , A gains no information about η. Therefore, we have $\scriptstyle P [ \eta ^ { \prime } \neq \eta | \mu = 1 ] = { \frac { 1 } { 2 } }$ . Since B guesses $\mu ^ { \prime } { = } 1$ when $\eta ^ { \prime } \ne \eta ,$ , we have $P [ \mu ^ { \prime } = \mu | \mu { = } 1 ] { = } \frac { \bar { 1 } } { 2 }$ .

In the case where $\mu { = } 0 , \ A$ sees an encryption of $m _ { \eta } ^ { * }$ . The advantage of A is . Therefore, we have $P [ \eta ^ { \prime } { = } \eta | \mu { = } 0 ] { = } \frac { 1 } { 2 } { + } \epsilon$ . Since B guesses $\mu ^ { \prime } { = } 0$ when $\eta ^ { \prime } { = } \eta$ , we have $\scriptstyle P [ \mu ^ { \prime } = \mu | \mu = 0 ] = { \frac { \mathtt { I } } { 2 } } + \epsilon$ .

Combing the above analysis, the overall advantage of $\boldsymbol { B }$ in the DBDH game is:

$$
\begin{array}{l} P [ \mu = 0 ] P [ \mu^ {\prime} = \mu | \mu = 0 ] + P [ \mu = 1 ] P [ \mu^ {\prime} = \mu | \mu = 1 ] - \frac {1}{2} \\ = \frac {1}{2} P [ \mu^ {\prime} = \mu | \mu = 0 ] + \frac {1}{2} P [ \mu^ {\prime} = \mu | \mu = 1 ] - \frac {1}{2} \\ = \frac {1}{2} P [ \eta^ {\prime} = \eta | \mu = 0 ] + \frac {1}{2} P [ \eta^ {\prime} \neq \eta | \mu = 1 ] - \frac {1}{2} \\ = \frac {1}{2} (\frac {1}{2} + \epsilon) + \frac {1}{2} \times \frac {1}{2} - \frac {1}{2} = \frac {\epsilon}{2}. \\ \end{array}
$$

![](images/03243dd0d13ebe8ec80b9efbf76559a3d01ca46a7afee00f3f9c58edd56c8621.jpg)

Definition 2. RKR-IND-CPA: An updatable encryption scheme satisfies RKR-IND-CPA if all polynomial time adversaries have at most a negligible advantage to win the following 3-phase game.

Phase 1: The challenger runs the algorithms of the updatable encryption scheme to generate a public parameter $U G P$ , a private parameter usp, a secret key USK. The challenger returns $U G P$ to the adversary. Upon receiving it, the adversary returns a polynomial bounded number q to the challenger.

Phase 2: The challenger runs the algorithms of the updatable encryption scheme to generate a sequence of secret keys $U S K _ { 1 } , U S K _ { 2 } , \cdot \cdot \cdot , U S K _ { q }$ started from USK and record the corresponding re-keys $r k _ { 1 } , r k _ { 2 } , \cdot \cdot \cdot , r k _ { q }$ . The challenger then allows the adversary to send a polynomial bounded number of queries. In each query, the adversary selects to send j where j∈[1, q], or $( i , m )$ where $i \in [ 0 , \ q ]$ and m is a message. Upon receiving j, the challenger returns $r k _ { j }$ . Upon receiving $( i , m )$ , if $i \in [ 1 , \ q ]$ , the challenger generates an encryption $C _ { i } ^ { U P }$ of m by $U S K _ { i }$ and returns $\bar { C } _ { i } ^ { U P } \{$ ; if i=0, the challenger generates an encryption $C _ { 0 } ^ { U P }$ of m by USK and returns $C _ { 0 } ^ { \bar { U } P }$ .

Phase 3: The adversary generates two equal-length messages $m _ { 0 } ^ { * }$ , m∗1 and returns a challenge $( m _ { 0 } ^ { * } , \ m _ { 1 } ^ { * } )$ to the challenger. The challenger selects one of the two messages by flipping a fair bit $\eta ,$ generates an encryption $C ^ { U P }$ of $m _ { \eta } ^ { * }$ by USK and returns $C ^ { { \dot { U } } P }$ to the adversary.

Finally, the adversary returns a guess $\eta ^ { \prime }$ . If $\eta { = } \eta ^ { \prime }$ , the adversary wins the game. We define the adversary’s advantage in the above game as $\scriptstyle { | P [ \eta = \eta ^ { \prime } ] - { \frac { 1 } { 2 } } | }$ .

Theorem 2. Our updatable encryption scheme satisfies RKR-IND-CPA based on the DBDH assumption.

Proof: Suppose there exists a polynomial time adversary A that can break RKR-IND-CPA of our updatable encryption scheme with advantage . We build an adversary B to break the DBDH assumption with advantage $\frac { \epsilon } { 2 }$ . In the following, we just describe the difference with the proof of Theorem 1:

Similar with the proof of Theorem 1, the challenger of DBDH game gives $\boldsymbol { B }$ proper $( Y _ { 1 } , Y _ { 2 } , Y _ { 3 } , Y _ { 4 } , Y _ { 5 } , Y _ { 6 } , Z )$ based on flipping result of a fair bit $\mu .$

In the setup phase, B computes $X { = } e ( Y _ { 2 } , Y _ { 6 } ) { = } e ( g , h ) ^ { y _ { 1 } y _ { 2 } }$ . $\boldsymbol { B }$ chooses a random number $\beta \in Z _ { p }$ and computes $g ^ { \beta }$ . B sets UGP=X and $U S K { = } ( g ^ { \beta } , \ h ^ { \frac { y _ { 1 } y _ { 2 } } { \beta } } )$ . Note that B does not have enough knowledge to compute $h ^ { \frac { y _ { 1 } y _ { 2 } } { \beta } }$ . However, as B does not need to show USK to $A , A$ will not be aware of this event. B then returns UGP to A. After that, B receives q from ${ \mathcal { A } } .$

In the query phase, B chooses a sequence of random numbers α1, $\alpha _ { 2 } , \cdot \cdot \cdot , \alpha _ { q } \in Z _ { p }$ . The distribution of the constructed sequence is identical with the sequence of re-keys $r k _ { 1 } , r k _ { 2 } , \cdots$ , $r k _ { q }$ generated by the algorithms of the updatable encryption scheme. $\boldsymbol { B }$ then informs A to send queries. When receiving $j , B$ returns $\alpha _ { j }$ . When receiving (i, m), B chooses a random number $s { \in } Z _ { p }$ and constructs an encryption $C _ { i } ^ { U P }$ :

$$
C _ {i} ^ {U P} = \left(C _ {i 1}, C _ {i 2}\right) = \left(m X ^ {s}, \left(g ^ {\beta \alpha_ {1} \alpha_ {2} \dots \alpha_ {i}}\right) ^ {s}\right) \text {   if   } i \in [ 1, q ]
$$

$$
C _ {i} ^ {U P} = (C _ {i 1}, C _ {i 2}) = (m X ^ {s}, (g ^ {\beta}) ^ {s}) \text {   if   } i = 0
$$

B then returns $C _ { i } ^ { U P }$ to A.

In the challenge phase, $\boldsymbol { B }$ constructs an encryption $C ^ { U P }$

$$
C ^ {U P} = (C _ {1}, C _ {2}) = (m _ {\eta} ^ {*} Z, (Y _ {3}) ^ {\beta})
$$

If µ=0, then $Z { = } e ( g , h ) ^ { y _ { 1 } y _ { 2 } y _ { 3 } }$ . Let $s { = } y _ { 3 }$ , then we have $C _ { 1 } \mathrm { = } m _ { \eta } ^ { * } e ( g , h ) ^ { y _ { 1 } y _ { 2 } y _ { 3 } } \mathrm { = } m _ { \eta } ^ { * } ( e ( g , h ) ^ { y _ { 1 } y _ { 2 } } ) ^ { y _ { 3 } } \mathrm { = } m _ { \eta } ^ { * } X ^ { s }$ and $C _ { 2 } { = } ( Y _ { 3 } ) ^ { \beta } { = } ( g ^ { \ddot { \beta } } ) ^ { y _ { 3 } } { = } ( g ^ { \beta } ) ^ { s }$ . The distribution of the constructed encryption is identical to the valid ones generated by the algorithms of updatable encryption scheme with the secret key USK. If $\eta { = } 1$ , then ${ \cal Z } { = } e ( g , h ) ^ { z }$ . We then have $C _ { 1 } { = } m _ { n } ^ { * } e ( g , h ) ^ { z }$ . Since z is random, $C _ { 1 }$ is actually a random element of $G _ { T }$ from the view of A and the constructed encryption reveals no information about $m _ { \eta } ^ { * } .$ .

Finally, the guess phase is similar with the proof of Theorem 1. The overall advantage of B in the DBDH game is thus $\frac { \epsilon } { 2 } .$

# B. Security analysis of our system

Data privacy: In our system, participants follow double encryption paradigm to encrypt and submit their product data records (policy enforced encryptions). As a result, the service provider has to decrypt two layers of encryptions to access the underlying product data. Considering a tagged product flows through the supply chain; the RKR-IND-CPA property of updatable encryption scheme prevents the service provider to decrypt the outside layers of submitted policy enforced encryptions, and the security property of CP-ABE scheme prevents the service provider to decrypt the inside layers of submitted policy enforced encryptions. Double encryption paradigm also resists collusion attack between the service provider and the key authority, since the successful decryption requires tag attribute credentials.

Item-level access control: Recall that our access policy is defined over both role attributes AND tag attribute. The usage of AND tag attribute part first restricts that the potential authorized participants must have processed the tag. The usage of role attributes part further restricts a desired subset of actual authorized partners from the potential authorized participants (who have processed the tag). The key authority is also excluded from accessing the product data records as it does not manage the credentials of tag attributes.

Item-level revocation: We need to prove that a revoked participant with old tag attribute credentials cannot decrypt any encryption associated with a new tag attribute. Considering a tagged product flows through the supply chain, the RSKR-IND-CPA property of updatable encryption scheme prevents each revoked participant with its old tag attribute credential to decrypt any submitted policy enforced encryption associated with a new tag attribute.

# V. PERFORMANCE EVALUATION

We evaluate our system in four steps. We first investigate the performance of encrypting/decrypting product data for a tagged product at the participant side. We then compare the performance of our system against CP-ABE in achieving itemlevel access control and item-level privilege revocation. We next study the overall performance of our system through large-scale experiments. Finally, we evaluate whether our system can meet the resource requirements of commodity C1G2 RFID system. We use a java implementation [20] of CP-ABE and implement our updatable encryption scheme based on the Pairing Based Cryptography (PBC) library [17], [18], [19].

![](images/d7fc3e8e36dd78bcf36afc2e1701a7d48de2c5b89790a920435429bcb11c52a4.jpg)



![](images/6eb1424010b4fce16036359c60a85492d26cd4d51e3b119847c590b8e7c08048.jpg)



![](images/878ee23f18789c15ea46682eea687877bbdd90217079ab300219e45c219b1cb1.jpg)



(b) Computation overhead (ms) of decryption operation with all AND policy   
(c) Computation overhead (ms) of decryption operation with all OR policy

(a) Computation overhead (ms) of encryption operation   
Fig. 5. Performance comparison between parallel encryption/decryption operations and encryption/decryption operations.   
![](images/4e0bc19d8b559b0b71ccaefe401ecf71a88d8c14edd5ee4cdd4da591630769ad.jpg)



![](images/18a4c546ed47caec75fc8d5af4f14834f4c6ac4523fae53fa0f96f7eaaadfd8b.jpg)



![](images/5ae518d7c12699bd4344f66144c6511f36562aded8683afe9e0d8f97ad1253ca.jpg)



(a) Speedup ratio between parallel encryption operation and encryption operation   
(b) Speedup ratio between parallel decryption operation and decryption operation with all AND policy   
(c) Speedup ratio between parallel decryption operation and decryption operation with all OR policy   
Fig. 6. Speedup ratio between parallel encryption/decryption operations and encryption/decryption operations.

Recall that our system consists of three types of entities: supply chain participant, service provider and key authority. Each entity has its own server to execute cryptographic operations. Besides, each supply chain participant owns readers to collect tag tokens, which are then sent to its server for further processing. The servers of the three types of entities are connected through network for communication. In our experiment, we adopt high-end workstations to conduct the computation tasks. The workstations are equipped with 16- core AMD Opteron Processor 6320 and 16GB RAM running Ubuntu 13.10.

# A. Basic evaluation

In our system, a participant needs to frequently encrypt its product data and decrypt other participants’ product data. Therefore, we evaluate the basic overhead of encrypting/decrypting a policy enforced encryption. As current computation tasks are often conducted on multi-core PCs or even PC clusters, we investigate how our tasks can be paralleled by multi-cores. We compare the parallel version using multi-cores and the original version using single-core. Figure 5 shows the overhead of encryption/decryption with 108 KB data.

Figure 5(a) shows the encryption overhead as a function of the number of attributes contained in the associated policy. Our findings show that the overhead of the original version grows quickly with the number of attributes and use multicores can greatly increase the speed (as shown in Figure 6(a)). The reason is that the CP-ABE encryption operation consists of multiple independent sub tasks, which can be assigned to multi-cores for parallel execution. We also find that the overhead of both the versions have no strict linear relation with the number of attributes. The reason is that besides the CP-ABE encryption operation, the policy enforced encryption implementation also contains many other execution steps (i.e., data read/write-back and AES encryption), which cannot be paralleled and are not affected by the number of attributes.

On the other hand, the decryption overhead depends on the type of policies associated with the encryptions. Specifically, the policy of a policy enforced encryption regulates a minimum set of role attributes that a credential of role attributes needs to be satisfied for successful decryption. Due to the design of CP-ABE, the decryption overhead is affected by the number of attributes. Figures 5(b)-(c) show two computational extreme cases: all AND policy (where all attributes need to be satisfied) and all OR policy (where at least one attribute needs to be satisfied) respectively.

In the all AND case, the overhead of the original version grows quickly with the size of the policy (as shown in Figure 5(b)). The reason is that the minimum set is all the role attributes in the policy. Instead, using multi-cores can greatly increase the speed (as shown in Figure 6(b)). The reason is that processing each of the in-set role attributes raises several sub tasks and all these tasks are independent, which facilitates the parallel execution on multiple cores. Also, the overhead of both the versions have no strict linear relation with the number of attributes, and the reason is the same with the encryption case.

In the all OR case, the decryption overhead grows slowly with the size of the policy (as shown in Figure 5(c)). The reason is that the minimum set is any one of the role attributes in the policy. Besides, using multi-cores cannot increase the speed (as shown in Figure 6(c)). The reason is that processing one role attribute raises few sub tasks and the multiple cores cannot be fully utilized. Also, we find that the performance of the parallel version is even slower than the original version. Such a performance degradation is due to thread pool initialization and thread schedule raised in the recursive parallel framework.

![](images/9afe62b0d4c1eb14709163dbffa25bf3cb8a049ebc1917631d4de55e44672ca8.jpg)



![](images/0c8e4faa1759430722f4df3a8094c04e4f2b5ab2a44731994bf7dd9d8539498b.jpg)



(a) Computation overhead (min) as a (b) Communication overhead (MB) function of tag number as a function of tag number   
Fig. 7. Overhead of CP-ABE in achieving item-level data access control.

# B. Comparison of our system with CP-ABE

We compare the performance of our system against CP-ABE in achieving item-level access control, item-level privilege revocation and data privacy. All the experiments fully utilize the 16 cores of our PC to improve the running speed.

Access control overhead: CP-ABE requires the key authority to issue CP-ABE credentials for each of the participants in item-level. The storage and computation overhead of a CP-ABE credential is proportional to its associated attributes. For simplicity, we assume that each participant is described by 20 role attributes. A CP-ABE credential thus is associated with 21 attributes (20 role attributes and 1 tag attribute).

Figure 7(a) plots the computation overhead of the key authority to compute credentials of tagged products for one participant. The computation overhead grows linearly with the number of products. When 12000 tagged products flow through the supply chain, the key authority has to cost more than 2 hours to compute the credentials for each of the participants. Suppose the supply chain consists of 15 participants, the total computation delay can be as high as 30 hours.

Figure 7(b) plots the communication overhead of the key authority to distribute the credentials of tagged products for one participant. Similar to the computation overhead, the traffic volume grows linearly with the number of products. The key authority needs to distribute 340 MB credentials for each participant when 12000 tagged products flow through the supply chain. Moreover, credentials are actually secret keys for decryption purposes. These credentials thus need to be distributed through secure channels, which incurs further overhead for channel maintenance. As a large scale supply chain needs to handle millions of products, it poses heavy burdens on the key authority and renders such an approach inapplicable.

Instead, our system avoids fussy credential issuing tasks and leverages tags to locally distribute tag attribute credentials. Participants can immediately read the tag attribute credential of a product from the attached tag. By doing so, our system totally avoids the computation overhead and the communication overhead between the key authority and the participants, greatly improving product handling efficiency.

TABLE II REVOCATION COMPARISON IN HANDLING 6000 TAGGED PRODUCTS 

<table><tr><td>Scheme</td><td>Computation overhead</td><td>Communication overhead</td></tr><tr><td>CP-ABE</td><td>140 mins</td><td>340 MB</td></tr><tr><td>Our system</td><td>27 mins</td><td>6000×168 bits≈0.96 MB</td></tr></table>

Revocation overhead: In a revocation operation, CP-ABE relies on the key authority to issue two types of credentials for each of the unrevoked participants in item-level. For multiple tagged products and for a unrevoked participant, the computation overhead of the key authority doubles the computation overhead shown in Figure 7(a). The unrevoked participant needs to acquire an old credential and an updated credential for each tagged product to access its product data record. For the same reason, the communication overhead for credential distribution of the key authority also doubles the communication overhead shown in Figure 7(b).

Instead, our system allows the participant who conducts the revocation operation to locally update the tag tokens of tagged products and delegate the service provider to update policy enforced encryptions for them. Both of the update operations are computation efficient. The participant also needs to send a short 168-bit re-key for each tagged product to the service provider for it to update the encryptions, which is communication efficient. Table II compares the computation overhead and communication overhead of CP-ABE and our system to handle 6000 tagged products. According to the experiment results, our system dramatically reduces both the computation overhead and the communication overhead.

Data privacy: From the above comparison, we can see that CP-ABE relies on a key authority to manage all the credentials of attributes, introducing vulnerability to product data records. If the authority is compromised or the credentials are accidentally exposed, the product data of the whole supply chain can be decrypted. As a result, all the supply chain participants have to trust the key authority to securely manage their credentials. Instead, our system relies on tags to distribute the credentials of tag attributes, which precludes the key authority from accessing the product data of the supply chain.

# C. Evaluation of our system

A supply chain often processes a large amount of tagged products. To evaluate the performance of our system in this setting, we evaluate the overhead of our system through largescale experiments. We test our experiments on two computing platforms: a single PC and a cluster of servers. The first platform is exactly our 16-core PC; while the second platform is a cluster of three servers scheduled by hadoop infrastructure. Both the platforms use 12 CPU cores.

We evaluate the three key operations of our system, namely data submission, data retrieval and privilege revocation. We generate random product data following normal distribution.

![](images/db186d27e520d17e8509319bdfde50fa1be89e1104b317b6bf2e7ca187bf6536.jpg)



![](images/4623db8eced99afcd9795372ed37e50ed1ade452bf1d4589ac34252fcbe1c9dd.jpg)



![](images/9eb11d729674fd7b75ac1c27f9e00ac07be024e464b4777b2d058497ad158254.jpg)



(a) Computation overhead (s) of data submission as (b) Computation overhead (s) of data retrieval as a (c) Computation overhead (min) of data privilege50 tion 50 ion a function of tag number uta function of tag number uta revocation as a function of tag number

Fig. 8. Computation evaluation in the multi-cores single PC and the cluster of PCs with hadoop.C Number of Tags C 2000 4000 6000 8000 10000Number of Tags   
![](images/6fffb2b18d88026d0395cdb170c621bec4192401ff9447bedb84bbcb86246e75.jpg)



![](images/e7cbef7acbd267df7504c6137758ff4d412429982b4460ec55f235cea79957e1.jpg)



![](images/2f71dcc37aa58a726773b3c1d1746705cc4af3231df86790356f6d4bff5b8d76.jpg)



(a) Speedup of data submission between CP-ABE and our system as a function of tag number   
(b) Speedup of data retrieval between CP-ABE and our system as a function of tag number   
(c) Speedup of privilege revocation between multicores and hadoop as a function of tag number   
Fig. 9. Speedup evaluation in the multi-cores single PC and the cluster of PCs with hadoop.

Figures 8(a)-(c) show the computation overhead incurred by the three operations when processing a large amount of tagged products. We vary the number of products from 2000 to 10000.

In the data submission, we measure the time to encrypt policy enforced encryptions for all the products. The time can be as fast as about 2246 seconds (37 minutes) for 10000 products. In the data retrieval, we measure the time to decrypt policy enforced encryptions for all the products. The time can be as fast as about 2164 seconds (36 minutes) for 10000 products. For comparison purpose, we also measure the time to encrypt/decrypt CP-ABE encryptions for all the products in data submission/retrieval in Figures 8(a)-(b). From the two figures, we can see that CP-ABE performs better than our system. We list the performance speedup of CP-ABE vs. our system in data submission/retrieval in Figures 9(a)-(b). The reason is that our design of policy enforced encryption composes of an inner layer of CP-ABE encryption and an out layer of updatable encryption, which incurs additional encryption/decrpytion overhead.

In the privilege revocation, we measure the time to update the policy enforced encryptions for all the products. The time can be as fast as about 41 minutes for 10000 products.

We also notice that the three key operations need not to be frequently executed by supply chain participants. Generally, each participant only needs to execute the three operations once for tagged products. When a participant receives the products, it needs to execute one data submission operation for them. If the participant wants to retrieve product data records for them, it needs to execute one data retrieval operation. Once decrypted, the participant only needs to locally store the decryption result in plaintext for future usage (such as queries). To enhance data privacy, the participant can use lightweight symmetric cipher (e.g., AES) to re-encrypt the decryption result before local storage. The participant can further decide whether to execute privilege revocation operation for the received products; and if the decision is yes, it only needs to sent re-keys to the service provider and delegates the latter to execute the update operation. Thus, we believe the computation overhead is acceptable for real applications.

In the evaluation of the three operations, the multi-core platform always outperforms the hadoop platform as shown in Figures 9(a)-(c). This is because the multi-core platform assigns higher rate of computation resource to complete the three operations, while the hadoop platform incurs higher coordination overhead, e.g., task submission, data storage, etc.

# D. Implementation on commodity C1G2 RFID systems

We describe our implementation on commodity C1G2 RFID systems. Our system requires each tag to carry a tag token, which consists of a tag attribute and a secret key of the updatable encryption scheme. We select type f elliptic curve of PBC library to implement the updatable encryption scheme and the secret key is 496 bits long. As the tag attribute is a hash of the secret key, it does not need to be explicitly stored in the tag. As a result, a tag token is only 496 bits long.

An RFID reader can write/read tag tokens to/from an RFID tag with the C1G2 communication primitives. In particular, we use the Write command to write tag token into RFID tags, which allows the reader to write a 16-bit data block per operation. To transfer more data, the reader needs to divide the large trunk of data into several 16-bit blocks and write them via multiple Write operations. The Read command on the other hand supports the bulk data collection, which allows the reader to collect up to 512 bits per Read operation.

We use the Alien ALR 9900+ commodity RFID reader with the default settings (e.g., 30dBm transmission power) to interrogate commodity passive RFID tags. The data transfer program is developed based on the Alien RFID reader SDK codes. Our implementation only requires the C1G2 routine operations so we believe our design can also be implemented on other commodity RFID systems.

Current commodity RFID tags typically have different sizes of non-volatile memory which can be used to store the tag tokens. We test with two different types of widely used passive tags – ALN-9640 and AD-224 tags both with 512-bit user memory. As our tag token adopts compact 496-bit tag token, the user memory can accommodate the tag tokens. Our design does not require any modifications to the commodity passive tags or implement additional cryptographic functionality on the tags.

TABLE III COMMUNICATION TIME OF TAG TOKEN TRANSFER 

<table><tr><td>Types of passive tags</td><td>Writing time</td><td>Reading time</td></tr><tr><td>ALN-9640</td><td>509 ms</td><td>107 ms</td></tr><tr><td>AD-224</td><td>501 ms</td><td>100 ms</td></tr></table>

We focus on the communication overhead between the reader and the tags in tag token transfer. As the tag tokens are transferred using the C1G2 Write/Read primitives, the performance is largely dictated by the throughput of the commodity RFID system. Table III shows the communication overhead involved in the 496-bit tag token transfer. According to the experiment results, it requires more time to write tag tokens into tags, because as mentioned the Write command only allows the reader to write a 16-bit data block per Write operation. To transfer the 496-bit tag token, the reader needs to first divide the tag token into several blocks and transfer them separately which takes longer time. In comparison, the Read operation takes less time since it only requires one Read operation to collect the whole 496-bit tag token.

# VI. RELATED WORK

Besides the original CP-ABE scheme [9], there are also many other constructions of CP-ABE [28]–[32]. We briefly discuss the suitability of these schemes for our system. Many new CP-ABE schemes [29]–[32] extend the primary CP-ABE [9] from the aspects of security strength, flexibility and efficiency. Our system can immediately inherent these advantages by replacing the primary CP-ABE with these new CP-ABE schemes. Recently, Lewko et.al [28] propose a distributed version of CP-ABE (DCP-ABE) called DCP-ABE. In their scheme, multiple authorities could claim their own attributes and manage the corresponding credentials. On the other hand, one could jointly use the credentials across them for decryption purpose. This property enables DCP-ABE a good candidate to support item-level access control. However, DCP-ABE cannot be solely used to achieve item-level privilege revocation as the access policies of its encryptions cannot be updated without decryption.

Various applications in the RFID-enabled supply chain have been proposed [6]–[8], [11], [12], which heavily rely on a central service provider to coordinate supply chain data. Li et al. [6] propose to store tag data in a central database and share the data among different supply chain partners. Zanetti et al. [7] design a clone tag detection system, where a central server collects tracing data for tagged products when they move in the supply chain. Blass et al. [8] and Elkhiyaoui et al. [11] design several tag path authentication techniques, which rely on a central manager to issue path information for participants. Kerschbaum et al. [12] propose to establish trust relations leveraging RFID tags which requires a key authority to distribute secret keys. Different from those works, our system provides an item-level data access control mechanism that defines and enforces access policies based on participant attributes and tag credential.

Another line of RFID data sharing approach is to leverage the tag as a data transmitter [33], [34], [35], [36]. Kuerschner et al. [33] discuss the advantages of data on tag manner in the context of RFID-enabled supply chain. Pearson et al. [34] propose to store signatures in tags so that customers can authenticate the originality of the tagged products. Juels et al. [35] explore the mobility of tags and use them to distribute keys on a unidirectional channel through an RFID enabled supply chain. In [36], the authors design a solution to protect privacy in RFID-enabled batch recall. In their solution, product data are continuously added into the tag memory when tags flow through the supply chain and several cryptographic primitives are used to ensure RFID data privacy. Unfortunately, the usage of these works are limited by the storage constraint of RFID tags. As a tag can only store limited data, such a data on tag paradigm is not flexible enough to support various applications of RFID supply chain.

# VII. CONCLUSION

We present a scalable industry data access control system for RFID-enabled supply chain. Our new system addresses three main limitations of CP-ABE when used in the supply chain, including scalability bottlenecks in item-level data access control, compromising vulnerability at the key authority, and credential issuing overhead in item-level revocation. Our system provides two mechanisms to support scalable data access control and privilege revocation in item-level. The itemlevel data access control mechanism enforces access control based on role attributes and tag attributes and the item-level revocation mechanism enables a participant to revoke the data access privileges about a product of its upstream participants. Experiment results based on the large-scale simulation and the real implementation on commodity RFID systems demonstrate the scalability and efficiency of our system. For the future work, we plan to investigate security approaches to hide the access policies. In addition, our access control system assumes a trusted server. We plan to relax this assumption and protect data managed by curious service providers.

# ACKNOWLEDGMENT

We acknowledge the support from Singapore MOE AcRF grant MOE2013-T1-002-005, NTU NAP grant

M4080738.020, Hong Kong ECS (PolyU 252053/15E), The Key Program of NSFC-Guangdong Union FoundationVII. CONCLUSION (U1135002), National High Technology Research andVII. CONCLUSION Development Program (863 Program) (No. 2015AA011704) (No. 2015AA016007), and The Key Program of NSFC Grant (U1405255).

# REFERENCES

[1] “Data Sharing in the Pharmaceutical Supply Chain: A Series of Caserameter configurations and achieves high estimation efficiency.We enhance the robustness of cardinality estimation over noisy Studies”, www.hcsupplychainresearch.org/WP/IBM/ whitepaper.pdf.nnels. We implement a prototype system based on the GN   
[2] G.M. Gaukler, R.W. Seifert, “Applications of RFID in Supply Chains”, in Proceedings of Supply Chain Design and Management, 2007.annels. We implement a prototype system based on the dio/USRP platform in concert with the WISP RFID   
[3] http://www.gtnexus.com/.Radio/USRP platform iZOE only requires sligh   
[4] “Epedigree - Wikipedia, the free encyclopedia”, http://en.wikipedia.org/ZOE only requires slight updates to the EPCglobal C1G2 stan-dard. We also conduct extensive simulations to evaluate the perwiki/Epedigree.   
[5] “Pharma Logistics: Can RFID Heal Supply Chain Security?”,dard. We also conduct extensive simulations to evaluate the per-formance of ZOE in large-scale settings. The results demonhttp://www.inboundlogistics.com/cms/article/pharma-logistics-can-mance of ZOE in large-scale settings. The results dete that ZOE outperforms the most recent cardinality es rfid-heal-supply-chain-security/.ate that ZOE outperforms tn protocols.   
[6] Y. Li and X. Ding, “Protecting RFID Communications in Supply Chains”, in Proceedings of ACM ASIACCS, 2007.n protocols.   
[7] D. Zanetti, S. Capkun, and A. Juels, “Tailing RFID Tags for Clone Detection”, in Proceedings of NDSS, 2013.REFERENCES   
[8] E. Blass, K. Elkhiyaoui and R. Molva, “Tracker: Security and Privacy forREFERENCES RFID-based Supply Chains”, in Proceedings of NDSS, 2011.[1] Alien Technology, Morgan Hill, CA, USA, “Alien Technol   
[9] J. Bethencourt, A. Sahai and B. Waters, “Ciphertext-Policy Attribute-[1] Alien Technology, Morgan Hill, CA, USA, “Alien Technology,” [On-line]. Available: http://www.alientechnology.com Based Encryption”, in Proceedings of IEEE S&P, 2007.line]. Available: http://www.alientechnology.com[2] EPCglobal, Brussels, Belgium, “Class 1 Gene   
[10] “Securing RFID Data for the Supply Chain”, www.verisign.com/static[2] EPCglobal, Brussels, Belgium, “Class 1 Generation 2 UHFair interface protocol standard “Gen 2”,” [Online]. Available: /028573.pdf.air intehttp://ww   
[11] K. Elkhiyaoui, E. Blass and R. Molva, “CHECKER: on-site checkinghttp://www.epcglobalinc.org/standards/uhfc1g2[3] “Gen 2 RFID tools,” [Online]. Available: https://www.cgran.org/wiki/ in RFID-based supply chains”, in Proceedings of ACM WiSec, 2012.[3] “Gen 2 RFID tools,” [Online]. Available: https://www.cgran.org/wi   
[12] F. Kerschbaum and A. Sorniotti, “RFID Based Supply Chain PartnerGen2[4] Ettus Research, Santa Clara, CA, USA, “Ettus Research,” [Online]. Authentication and Key Agreement”, in Proceedings of ACM WiSec,[4] Ettus Research, Santa Clara, CA, USA, “Ettus Research,” [Online].Available: http://www.ettus.com 2009.A[5] “   
[13] R. Baden, A. Bender, N. Spring, B. Bhattacharjee and D. Starin,[5] “WISP platform,” [Online]. Available: http://wisp.wikispaces.com[6] M. Buettner and D. Wetherall, “An empirical study of UHF RFID per-“Persona: An Online Social Network with User-Defined Privacy”, in[6] M. Buettner and D. Wetherall, “An empirical study of UHF RFID per-formance,” in Proc. ACM MobiCom, 2008, pp. 223–234. Proceedings of ACM SIGCOMM, 2009.formance,” in Proc. ACM MobiCom,[7] J. I. Capetanakis, “Tree algorithms   
[14] J. A. Akinyele, C. Lehmann, M. Green, M. Pagano, Z. Peterson, A.[7] J. I. Capetanakis, “Tree algorithms for packet broadcast channels,”IEEE Trans. Inf. Theory, vol. IT-25, no. 5, pp. 505–515, Sep. 1979. Rubin, “Self-Protecting Electronic Medical Records Using Attribute-IEEE Trans. Inf. Theory, vol. IT-25, no. 5, pp. 505–515, Sep. 1979.[8] S. Chen, M. Zhang, and B. Xiao, “Efficient information collection Based Encryption”, in Proceedings of ACM CCS SPSM 2011.[8] S. Chen, M. Zhang, and B. Xiao, “Efficient information protocols for sensor-augmented RFID networks,” in Pr   
[15] N. Santos, R. Rodrigues, K. P. Gummadi, S. Saroiu, “Policy-Sealed Data:protocols for sensor-augmented RFID networks,” in Proc. IEEE A New Abstraction for Building Trusted Cloud Services”, in ProceedingsINFOCOM, 2011, pp. 3101–3109.[9] K. Finkenzeller, RFID Handbook: Radio-Frequency Identification of USENIX Security, 2012.[9] K. Finkenzeller, RFID   
[16] M. Blaze, G. Bleumer, and M. Strauss, “Divertible protocols and atomicFundamentals and Applications. New York, NY, USA: Wiley, 2000.[10] G. R. Grimmett and D. R. Stirzaker, Probability and Random Proproxy cryptography”, in Proceedings of EUROCRYPT, 1998.[10] G. R. Grimmett and D. R. Stirzaker, Probability and Racesses, 3rd ed. Oxford, U.K.: Oxford Univ. Press, 2001.   
[17] jPBC: Java Pairing Based Cryptography, http://gas.dia.unisa.it/projects/cesses, 3rd ed. Oxford, U.K.: Oxford Univ. Press, 2001.[11] H. Han, B. Sheng, C. C. Tan, Q. Li, W. Mao, and S. Lu, “Counting jpbc.[11] R   
[18] A. De Caro, and V. Iovino, “jPBC: Java pairing based cryptography”,RFID tags efficiently and anonymously,” in Proc. IEEE INFOCOM,2010, pp. 1–9. in Proceedings of IEEE ISCC, 2011.2010, pp. 1–9.[12] M. Kodialam and T. Nandagop   
[19] B. Lynn. “The pbc library”, http://crypto.stanford.edu/pbc/.[12] M. Kodialam and T. Nandagopal, “Fast and reliableschemes in RFID systems,” in Proc. ACM MobiCom   
[20] http://junwei-wang.github.io/cpabe/.schemes in RFID systems,” in 322–333.   
[21] D. Boneh and X. Boyen, “Efficient Selective Identity-Based Encryption322–333.[13] M. Kodialam, T. Nandagopal, and W. C. Lau, “Anonymous tracking Without Random Oracles”, Journal of Cryptology, 2011.[13] M. Kodialam, T. Nandagopal, and W. C. Lau, “Anonusing RFID tags,” in Proc. IEEE INFOCOM, 2007, pp   
[22] G. Ateniese, K. Fu, M. Green and S. Hohenberger, “Improved Proxy Re-using RFID tags,” in Proc. IEEE INFOCOM, 2007, pp. 1217–1225. encryption Schemes with Applications to Secure Distributed Storage”, in Proceedings of NDSS, 2005.   
[23] G. Ateniese, K. Fu, M. Green and S. Hohenberger, “Improved Proxy Reencryption Schemes with Applications to Secure Distributed Storage”, in ACM Transactions on Information and System Security, 2006.   
[24] M. Green and G. Ateniese, “Identity-Based Proxy Re-encryption”, in Proceedings of ACNS, 2007.   
[25] B. Libert and D. Vergnaud, “Unidirectional Chosen-Ciphertext Secure Proxy Re-encryption”, in Proceedings of PKC, 2008.   
[26] T. Isshiki, M. Nguyen and K. Tanaka, “Proxy Re-Encryption in a Stronger Security Model Extended from CT-RSA2012”, in Proceedings of CT-RSA, 2013.   
[27] O.Goldreich, Foundations of Cryptography: Part 2, Cambridge University Press, 2004.   
[28] A. Lewko and B. Waters, Decentralizing Attribute-Based Encryption, in Proceedings of EUROCRYPT, 2011.   
[29] R. Ostrovsky, A. Sahai and B. Waters, Attribute-Based Encryption with Non-Monotonic Access Structures, in Proceedings of ACM CCS, 2007.   
[30] B. Waters, ”Ciphertext-Policy Attribute-Based Encryption: An Expressive, Efficient, and Provably Secure Realization”, in Proceedings of PKC, 2011.

[31] T. Okamoto and K. Takashima, ”Fully Secure Functional Encryption[21] L. G. Roberts, “Aloha packet system with and without slots and cap-ture,” Comput. Commun. Rev., vol. 5, no. 2, pp. 28–42, 1975. with General Relations from the Decisional Linear Assumption”, inture,” Comput. Commun. Rev., vol. 5, no. 2, pp. 28–42, 1975.[22] M. Shahzad and A. X. Liu, “Every bit counts: Fast and scalable RFID Proceedings of CRYPTO, 2007.[22] M. Shahzad and A. X. Liu, “estimation,” in Proc. ACM M   
[32] A. Lewko and B. Waters, ”Unbounded HIBE and Attribute-Basedestimation,” in Proc. ACM MobiCom, 2012, pp. 365–376.[23] J. R. Smith, A. P. Sample, P. S. Powledge, S. Roy, and A. Mami-Encryption”, in Proceedings of Eurocrypt, 2011.[23] J. R. Smith, A. P. Sample, P. S. Powledge,shev, “A wirelessly-powered platform for se   
[33] C. Kuerschner, F. Thiesse, E. Fleisch, ”An analysis of data-on-tagshev, “A wirelessly-powered platform for sensing and computation,”in Proc. ACM UbiComp, 2006, pp. 495–506. concepts in manufacturing”, in Proceedings of MMS, 2008.in Proc. ACM UbiComp, 2006, pp. 495–506.[24] R. Want, “An introduction to RFID technology,” IEE   
[34] J. Pearson, ”Securing the Pharmaceutical Supply Chain with RFID and[24] R. Want, “An introduction to RFID technology,” IEEE PervasiveComput., vol. 5, no. 1, pp. 25–33, Jan.–Mar. 2005. Public-key infrastructure (PKI) Technologies”, white paper, 2005.Comput., vol. 5, no. 1, pp. 25–33, Jan.–Mar. 2005.[25] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, “Season: Sh   
[35] A. Juels, R. Pappu and B. Parno, ”Unidirectional Key Distribution[25] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, “Season: Shelvinginterference and joint identification in large-scale RFID systems,” in Across Time and Space with Applications to RFID Security”, in Pro-interference and joint identification in large-scale RFID systems,” inProc. IEEE INFOCOM, 2011, pp. 3092–3100. ceedings of USENIX Security, 2008.Proc. IEEE INFOCOM, 2011, pp.[26] R. Zhang, Y. Liu, Y. Zhang, an   
[36] L. W. F. Chaves and F. Kerschbaum, ”Industrial Privacy in RFIDbased[26] R. Zhang, Y. Liu, Y. Zhang, and J. Sun, “Fast identification of themissing tags in a large RFID system,” in Proc. IEEE SECON, 2011, Batch Recalls”, in Proceedings of Enterprise Distributed Object Comput-missing tags in a large RFID system,” in Proc. IEEE SECON, 2011,pp. 278–286. ing Conference Workshops, 2008.pp. 278–286.[27] Y. Zhang, L. T. Yang, and J. C

![](images/e4585570e50a4d92000036a0488b9b94fa7a4f6ecef6f5b8fa9f81bc90f9b679.jpg)



Saiyu Qi received the B.S. degree in computer sci-        . ence and technology from Xi’an Jiaotong University,       . Li, “PET: Probabilistic estimating tree for large-scale Xi’an, China, in 2008, and the Ph.D. degree in,” IEEE Trans. Mobile Comput., vol. 11, no. 11, pp. computer science and engineering from Hong Kong       n,” IEEE Trans. Mobile Comput., vol. 11, no. 11, pp.v. 2012. University of Science and Technology, Hong Kong,         . 2012.. Li, “Fast tag searching protocol for large-scale RFID in 2014. He is currently an Assistant Professor with c. IEEE ICNP, 2011, pp. 363–372. the School of Cyber Engineering, Xidian University,        n, D. Jin, C. Huang, and H. Min, “Evaluating and opti-China. His research interests include applied cryp-     nsumption of anti-collision protocols for applications tography, cloud security, distributed systems, and          s,” in Proc. ISLPED, 2004, pp. 357–362. pervasive computing.  ,” in Proc. ISLPED, 2

![](images/29acfc62afa1d0f8368a4f2a724b5719757eecfb7d5f5e29e6e4520bd9a7d93f.jpg)



Yuanqing Zheng (S’11) received the B.S. degreeYuanqing Zheng received PhD degree from thein electrical engineering and M.E. degree in comin electrical engineering and M.E. degree in com-School of Computer Engineering in Nanyang Tech-munication and information system from Beijing munication and information system from Beijingnological University in 2014. Before that he receivedNormal University, Beijing, China, in 2007 and Normal University, Beijing, China, in 2007 andthe B.S. degree in Electrical Engineering and the2010, respectively, and is currently pursuing the 2010, respectively, and is currently pursuing theM.E. degree in Communication and InformationPh.D. degree in computer engineering at Nanyang Ph.D. degree in computer engineering at NanyangSystem from Beijing Normal University, Beijing,Technological University, Singapore. Technological University, Singapore.China, in 2007 and 2010 respectively. He is cur-His research interests include distributed systems His research interests include distributed systemsrently an assistant professor with the Department ofand pervasive computing. and pervasive computing.Computing in the Hong Kong Polytechnic University. His research interest includes human centered computing, mobile and wireless computing, RFID

systems, etc. He is a member of IEEE and ACM.

![](images/78dd12b9dd83b3a4f8f52ba47f1b16445aecf20ff3a0b5f3690e93f5d4504cc5.jpg)



Mo Li (M’06) received the B.S. degree in computerMo Li received the B.S. degree in computer science Mo Li (M’06) received the B.S. degree in computerscience and technology from Tsinghua University,and technology from Tsinghua University, Beijing, science and technology from Tsinghua University,Beijing, China, in 2004, and the Ph.D. degree inChina, in 2004, and the Ph.D. degree in computer Beijing, China, in 2004, and the Ph.D. degree incomputer science and engineering from Hong Kongscience and engineering from Hong Kong University computer science and engineering from Hong KonUniversity of Science and Technology, Hong Konof Science and Technology, Hong Kong, in 2009.

niversity of Science and Technology, Hong Kong,n 2009.He is currently an Assistant Professor with the in 2009.He is currently an Assistant Professor with theSchool of Computer Engineering, Nanyang Techno-He is currently an Assistant Professor with theSchool of Computer Engineering, Nanyang Techno-logical University, Singapore. His research interests School of Computer Engineering, Nanyang Techno-logical University, Singapore. His research interestsinclude wireless sensor networking, pervasive comlogical University, Singapore. His research iinclude wireless sensor networking, pputing, and mobile and wireless computing.

clude wireless sensor networking, pervasiveomputing, and mobile and wireless computing.Dr. Li is a member of the Association for Computcomputing, and mobile and wireless computing.Dr. Li is a member of the Association for Computing Machinery (ACM). Heing Machinery (ACM). He won the ACM Hong Kong Chapter Prof. Francis Dr. Li is a member of the Association for Computing Machinery (ACM). Hewon the ACM Hong Kong Chapter Prof. Francis Chin Research Award in 2009Chin Research Award in 2009 and the Hong Kong ICT Award Best Innovation won the ACM Hong Kong Chapter Prand the Hong Kong ICT Award Best and Research Grand Award in 2007.

![](images/1e0d7fce44f11b3202be4527e7a7d886dd414feb051f352292f9cfe96ca7247c.jpg)



Award Best Innovation and Research Grand Award inYunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, USA, in 2003 and 2004, respectively. He is now Cheung Kong Professor and Dean of School of Software at Tsinghua University, China. Yunhao is a fellow of IEEE and ACM. His research interests include RFID and sensor network, the Internet and Cloud Computing.

![](images/1c1014fac1165458d88bd572a5d62370391220834e5ef9f1aa71a706e85a1ad8.jpg)



Jinli Qiu received the B.S. degree in computer science from National University of Defense Techonology, China, in 2007, and the M.E. degree in computer science and technology from Xi’an Jiaotong University, Xi’an, China, in 2014.