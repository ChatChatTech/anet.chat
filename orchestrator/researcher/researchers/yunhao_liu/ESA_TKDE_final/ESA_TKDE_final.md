# ESA: Privacy-Preserving Data Sharing Framework with Efficient Fuzzy Search and Access Control

Pengcheng Sun, Lan Zhang, Xinming Wang, Chen Tang, Yihan Wang, Zhonghao Hu, Yunhao Wang, Hui Jin

Abstract—Cloud-assisted data sharing offers substantial convenience to resource-constrained users, enabling them to outsource data to public clouds and permit authorized users to perform retrievals. However, ensuring data privacy remains a significant challenge. Attribute-Based Keyword Search (ABKS) facilitates authorized searches over encrypted data, yet most existing ABKS schemes are primarily tailored for exact searches. They lack effective support for fuzzy search, which severely limits the practicality and efficiency. In this paper, we propose ESA, a novel privacy-preserving framework supporting multi-keyword fuzzy search with arbitrary Boolean semantics and fine-grained access control in data sharing. ESA introduces the Prime Filter, a novel data structure, along with a divide-and-conquer access control mechanism to achieve secure, efficient, and accurate fuzzy search. To enable authorized multi-keyword fuzzy search, the Prime Filter is designed as a unified primitive for both indexing and querying. It seamlessly integrates fuzzy search and access-policy enforcement by leveraging the indivisibility of prime numbers. To ensure reliable access control during both the search and decryption phases, ESA proposes a divide-andconquer mechanism that leverages blockchain to coordinate the off-chain and on-chain indexes. Finally, we extend ESA from the perspective of non-repudiation. Formal security analysis demonstrates that ESA is secure under the known background model. Extensive evaluations confirm ESA’s advantages, demonstrating search speeds up to 2–86× faster than state-of-the-art methods, with precision exceeding 95%.

Index Terms—Multi-keyword fuzzy search, Attribute-based keyword search, Searchable Encryption, Blockchain.

# I. INTRODUCTION

E FFICIENT search in data-sharing applications, such asmedical research, IoT, and financial services, has become increasingly important with the rapid growth of interconnected data [1]–[3]. To alleviate the maintenance burden of largescale shared data, resource-constrained data owners often

This work was supported in part by the National Key R&D Program of China under Grant 2021YFB2900103, in part by China National Natural Science Foundation under Grant 62441228 and Grant 62132018, and in part by the Science and Technology Tackling Program of Anhui Province under Grant 202423k09020016. (corresponding author: Lan Zhang)

Pengchen Sun, Xinming Wang, Chen Tang, and Yihan Wang are with the School of Computer Science and Technology, University of Science and Technology of China, Hefei 230026, China (e-mail: special0806@mail.ustc.edu.cn; xinmingwang@mail.ustc.edu.cn; chentang1999@mail.ustc.edu.cn; wyhappylife2016@mail.ustc.edu.cn).

Lan Zhang is with the School of Computer Science and Technology, University of Science and Technology of China, Hefei 230026, China, and also with the Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, Hefei 230026, China (e-mail: zhanglan@ustc.edu.cn).

Zhonghao Hu is with the Key Laboratory of Internet and Industrial Integration and Innovation, China Academy of Information and Communications Technology, MIIT, Beijing 100191, China (e-mail: huzhonghao@caict.ac.cn).

Yunhao Wang and Hui Jin are with the Lenovo Research, Beijing 100094, China (e-mail: wangyh43@lenovo.com; jinhui8@lenovo.com).

![](images/4c58142dc25176e76508def49fd0dafe160fe8415b934c5d7aa2ab5ca369f7c8.jpg)



Fig. 1. Example of privacy-preserving ABKS schemes, where authorized users with different attribute keys can search for and decrypt different data.

outsource their data to public cloud servers that provide search functionalities [3]–[5]. However, data and query privacy become crucial concerns. Untrusted servers may gain access to sensitive information or even enable unauthorized users to conduct arbitrary searches [4], [5]. A common solution is to encrypt the data before outsourcing. However, encryption greatly limits flexible search and efficient data sharing.

Secure and authorized search has become a focal point of both academic research and societal applications [6]. To address these requirements, existing solutions predominantly adopt attribute-based keyword search (ABKS) [7]–[10]. It combines the advantages of two cryptographic primitives: searchable encryption (SE) [11]–[15] and attribute-based encryption (ABE) [16], [17]. In these schemes, as depicted in Fig. 1, data owners encrypt their data with access control policies before outsourcing it to the server. Users with various attributes submit encrypted keyword queries to the server, and they can retrieve only the ciphertexts whose access-control policies are satisfied by their attribute sets.

Limitations of existing methods. Fuzzy keyword search is an important search mechanism used in many applications, including cloud storage, document management systems, and e-commerce platforms [18]. It supports user-friendly and flexible retrieval by matching queries with minor spelling errors or approximate keywords. However, most existing ABKS schemes are tailored for exact keyword search (as shown in Table I), limiting their applicability to multi-keyword fuzzy search due to inherent differences in the underlying encryption primitives. By contrast, recent private multi-keyword fuzzy search schemes [19]–[24] employ techniques such as localitysensitive hashing (LSH) and Bloom filters. They combine these structures with scalar product encryption to enable efficient and accurate fuzzy search. Nevertheless, the specialized data structures and encryption mechanisms required for efficient fuzzy search make it difficult to directly integrate existing ABKS schemes into such settings. Thus, a critical question in data sharing is: how to achieve efficient multi-keyword fuzzy search with fine-grained access control?

Challenge. The central challenge lies in achieving privacypreserving authorized multi-keyword fuzzy search without sacrificing search precision or efficiency. As discussed above, existing ABKS schemes were originally designed for exact keyword search and are ill-suited for this purpose. For exact search, the matching process between indexes, queries, and user attributes is deterministic, resulting in no false positives. In contrast, the precision of multi-keyword fuzzy search is highly sensitive to the choice of specialized data structures and parameter settings [19]–[24]. While ABKS schemes could theoretically incorporate techniques such as LSH to enable fuzzy search, our experiments show a precision drop of over 70% (see Fig. 10 in §VII-D), making this approach impractical for real-world deployment. Furthermore, as data volume increases, existing ABKS frameworks incur greater computational overhead than dedicated private fuzzy search schemes based on symmetric encryption. Thus, there is a pressing need for more efficient and accurate frameworks to enable private authorized multi-keyword fuzzy search.

Fortunately, we observe that user attributes can be embedded into customized fuzzy search data structures in a manner analogous to keywords. In this way, successful search matching requires an inverse containment relationship: the query’s keywords must be contained in the index, while the query’s attributes must contain the access policy encoded in the index. However, securely separating keywords from attributes, while still distinguishing access policies from search policies, remains a significant challenge. The indistinguishability property of prime numbers offers a desirable feature to satisfy both the inverse containment requirement and the need for policy separation. Specifically, the product of a prime number and the reciprocal of another prime number is never an integer. Based on this intuition, we propose ESA, a privacy-preserving framework for authorized multi-keyword fuzzy search in data sharing. Compared to existing methods (as shown in Table III), ESA supports fine-grained access control and provides improved precision, flexibility, and efficiency.

ESA Design. The core of ESA consists of a novel data structure called the Prime Filter and a divide-and-conquer access control mechanism. To enable authorized multi-keyword fuzzy search, the Prime Filter is designed as a unified primitive for both indexing and querying, integrating fuzzy search and access control policies. Leveraging the indivisibility property of prime numbers allows for the embedding of both keywords and attributes, without compromising keyword distinguishability and search precision. To guarantee consistent and reliable access control during both the search and decryption phases, we introduce a divide-and-conquer mechanism that harnesses blockchain technology to coordinate on-chain and off-chain indexes. Specifically, the off-chain indexes built on the Prime Filter enable efficient fuzzy search. The on-chain indexes, constructed with ABE, have ciphertext-size invariance and ensure reliable decryption. Finally, we develop a secure protocol that supports efficient fuzzy search with arbitrary Boolean semantics and fine-grained access control. We also extend ESA from the perspective of non-repudiation: blockchainbased deposit locking and immutability enable ESA to deter dishonest payments and computations. Our contributions are summarized as follows:

• We propose ESA, a privacy-preserving framework designed to address multi-keyword fuzzy search with finegrained access control in data sharing. Furthermore, ESA supports arbitrary Boolean semantics in search queries and incorporates a blockchain-based mechanism to ensure non-repudiable data transactions.   
• We design Prime Filter, a novel index structure for authorized multi-keyword fuzzy search that unifies fuzzy keyword embedding and attribute-policy embedding within a single index, which existing structures cannot support. It delivers improvements in the computational efficiency of encrypted search while also maintaining high precision.   
• We devise a divide-and-conquer access control mechanism featuring two hybrid index designs for secure data sharing, leveraging blockchain technology. By synergistically combining on-chain and off-chain indexes, it rigorously enforces access policies while preserving ciphertext-size invariance, thereby enabling lightweight storage, efficient search, and reliable decryption.   
• We formally prove the security of our protocol and demonstrate its efficiency and practicality through extensive evaluations. ESA achieves up to 2–86× faster performance and maintains over 95% precision, while reducing on-chain storage by approximately 66.7%, comparable to SOTA schemes. Besides, it remains robust to varying numbers of embedded attributes and consistently delivers high performance across diverse parameter settings.

# II. RELATED WORK

# A. Searchable Encryption (SE)

SE enables secure search functionality over encrypted databases. Recent research has proposed SE schemes with increasingly sophisticated capabilities, supporting features such as single keyword search [2], [15], multi-keyword search [25], range queries [26], and Boolean search with sublinear complexity [11]. However, most existing SE schemes only support exact keyword search. Li et al. [27] proposed the first scheme supporting single-keyword fuzzy search over encrypted data by constructing fuzzy keyword sets with wildcards. Later, Wang et al. [19] advanced this line of work by employing LSH and Bloom filters, thereby enabling multi-keyword fuzzy search without requiring predefined fuzzy keyword sets. Subsequent studies [20]–[24] have further improved the precision and efficiency of multi-keyword fuzzy search. However, they primarily address search precision and efficiency, often neglecting access control functionalities. Our ESA framework bridges the gap by enabling both private multi-keyword fuzzy search and fine-grained access control.

# B. Attribute-based keyword search (ABKS)

ABE [16], [17] enables data owners to enforce fine-grained access control based on user attributes. To support search functionality under attribute-based authorization, a line of work known as ABKS [8] combines ABE with SE. Compared with directly searching over ABE-encrypted files, ABKS schemes significantly reduce computational overhead and allow queries from multiple users with different access privileges. Recent ABKS frameworks enable exact matching under various functional settings, including single-keyword search [10], [28], multi-keyword search [7], [8], [29], and Boolean search [5], [30]. Despite supporting attribute-based authorization, existing ABKS schemes are designed for exact keyword matching. They fundamentally rely on deterministic primitives and do not support fuzzy search, nor can they handle fuzzy search under general Boolean semantics. Table I summarizes the main differences between representative ABKS schemes and ESA. As shown, ESA is the first to simultaneously provide (i) general Boolean fuzzy search and (ii) fine-grained access control within a unified framework.

TABLE I COMPARISON WITH REPRESENTATIVE ABKS SCHEMES 

<table><tr><td>Scheme</td><td>Fine-grained Access Control</td><td>Multi-keyword Search</td><td>Fuzzy Search</td></tr><tr><td>[10], [28]</td><td>√</td><td>×</td><td>×</td></tr><tr><td>[7], [8], [29]</td><td>√</td><td>√</td><td>×</td></tr><tr><td>[5], [30]</td><td>√</td><td>√ (Boolean)</td><td>×</td></tr><tr><td>ESA (Ours)</td><td>√</td><td>√ (Boolean)</td><td>√</td></tr></table>

# C. Blockchain-Based Approaches for Data Sharing

Blockchain, as a tamper-resistant ledger technology, ensures the traceability and immutability of data. Recent research has explored leveraging blockchain to introduce secure query capabilities and fairness into data-sharing systems. One line of work directly stores indexes on the blockchain and enables search operations [31], [32], thereby mitigating malicious behavior by centralized entities and ensuring fairness through smart contracts. However, these approaches often incur significant storage and computational overhead on the blockchain. Alternatively, other studies [33]–[35] enhance the verifiability of search integrity by storing proofs on the blockchain, enabling users to verify the correctness of search results returned by cloud servers. Additionally, some blockchain-based solutions offer both secure query functionality and access control mechanisms [9], [36]. Nevertheless, these schemes are generally restricted to supporting only exact keyword queries.

# III. PRELIMINARIES

Three important techniques are used as building blocks in our design, which are briefly described below. Besides, the main notations used in this paper are summarized in Table II.

# A. Asymmetric Scalar-Product-Preserving Encryption (ASPE)

ASPE [37] is an encryption scheme that enables scalar product computations directly over ciphertext. It can be used to verify the relationship between an encrypted index and a query in a privacy-preserving manner. Let $n$ denote the security parameter. The secret key consists of $\{ M _ { 1 } , M _ { 2 } , S \}$ , where $M _ { 1 } , M _ { 2 } \ \in \ \mathbb { R } ^ { n \times n }$ are invertible matrices, and $S \in \{ 0 , 1 \} ^ { n }$ is a splitting vector. The functions of ASPE are as follows:

Index encryption. Given an n-dimensional index vector $\mathcal { T } ,$ each element $i _ { j } \in \mathcal { I }$ is processed as follows: if $S [ j ] = 1 ( 1 \leq$ $j \leq n )$ , set $\begin{array} { r } { i _ { j } ^ { \prime } = i _ { j } ^ { \prime \prime } = i _ { j } ; } \end{array}$ otherwise, let $\begin{array} { r } { i _ { j } ^ { \prime } = \frac { 1 } { 2 } i _ { j } ^ { - } + r , i _ { j } ^ { \prime \prime } = } \end{array}$ ${ \begin{array} { l } { { \frac { 1 } { 2 } } i _ { j } - r , } \end{array} }$ , where r is a random number. Then I is split into two vectors $\mathcal { T } ^ { \prime }$ and ${ \mathcal { T } } ^ { \prime \prime }$ , it encrypt $\mathcal { T } ^ { \prime } , \mathcal { T } ^ { \prime \prime }$ with $\{ M _ { 1 } ^ { \top } , M _ { 2 } ^ { \top } \}$ into $\{ M _ { 1 } ^ { \top } \cdot \mathcal { T } ^ { \prime } , M _ { 2 } ^ { \top } \cdot \mathcal { T } ^ { \prime \prime } \}$ as the secure index.

Trapdoor encryption. Given an n-dimensional query vector Q, each element $q _ { j } \in \mathcal { Q }$ is processed as follows: $\mathrm { i f } \ S [ j ] =$ $0 ( 1 \leq j \leq n )$ , set $q _ { j } ^ { \prime } = q _ { j } ^ { \prime \prime } = q _ { j } ;$ otherwise, let $\begin{array} { r } { q _ { j } ^ { \prime } = \frac { 1 } { 2 } q _ { j } + } \end{array}$ $r ^ { \prime } , q _ { i } ^ { \prime \prime } = { \textstyle \frac { 1 } { 2 } } q _ { j } - r ^ { \prime } .$ , where $r ^ { \prime }$ is a random number. Then Q is split into two vectors $\mathcal { Q } ^ { \prime }$ and $\mathcal { Q } ^ { \prime \prime }$ , it encrypt $\mathcal { Q } ^ { \prime } , \mathcal { Q } ^ { \prime \prime }$ with $\{ M _ { 1 } ^ { - 1 } , M _ { 2 } ^ { - 1 } \}$ into $\{ M _ { 1 } ^ { - 1 } \cdot \mathcal { Q } ^ { \prime } , M _ { 2 } ^ { - 1 } \cdot \mathcal { Q } ^ { \prime \prime } \}$ as the trapdoor.

Search. Given an encrypted index and an encrypted query, the search is performed by computing:

$$
R = (M _ {1} ^ {\top} \mathcal {I} ^ {\prime}) ^ {\top} (M _ {1} ^ {- 1} \mathcal {Q} ^ {\prime}) + (M _ {2} ^ {\top} \mathcal {I} ^ {\prime \prime}) ^ {\top} (M _ {2} ^ {- 1} \mathcal {Q} ^ {\prime \prime}) \tag {1}
$$

as the search result. Since $M _ { 1 }$ and $M _ { 2 }$ are invertible, Eq. (1) simplifies to $R = \mathcal { T } ^ { \prime \top } \mathcal { Q } ^ { \prime } + \mathcal { T } ^ { \prime \prime \top } \mathcal { Q } ^ { \prime \prime } = \mathcal { T } ^ { \top } \mathcal { Q } .$ , thus correctly preserving the scalar product in the encrypted domain.

# B. Locality-Sensitive Hashing (LSH)

LSH is a widely used algorithm for approximate nearest neighbor search in high-dimensional spaces [38]. It hashes input items with a higher probability of hashing similar items to the same hash value. A LSH family H is $( r _ { 1 } , r _ { 2 } , p _ { 1 } , p _ { 2 } ) \cdot$ - sensitive if any two points a, b and $h \in H$ satisfy:

$$
i f d (a, b) \leq r _ {1}: \operatorname * {P r} [ h (a) = h (b) ] \geq p _ {1};
$$

$$
i f d (a, b) \geq r _ {2}: \operatorname * {P r} [ h (a) = h (b) ] \leq p _ {2},
$$

where $d ( a , b )$ is the distance between a and b. In our scheme, we employ the bit sampling LSH [38], which generates hash values by selecting k positions from the object’s vector and concatenating the bits at those k positions.

# C. Access Structure in Attribute-based Encryption

In ABE schemes, access policies are defined over a set of attributes. In this paper, we adopt the AND-gate policy [39] to specify the access structure. Specifically, given an attribute set $\mathcal { L } ~ = ~ \{ L _ { 1 } , L _ { 2 } , . ~ . ~ . , L _ { n } \}$ , where each attribute $L _ { i }$ has a corresponding set of values $V _ { i } = \{ v _ { i , 1 } , v _ { i , 2 } , \cdot \cdot \cdot , v _ { i , n _ { i } } \}$ . An access policy is defined as $\mathcal { A } = \{ A _ { 1 } , A _ { 2 } , . . . , A _ { n } \}$ , where $A _ { i } \in V _ { i } \cup \{ * \}$ denotes either a specific required value of $L _ { i }$ or the wildcard ∗ indicating “do not care”. Given a concrete user assignment $\boldsymbol { l } = ( l _ { 1 } , \ldots , l _ { n } )$ with $l _ { i } ~ \in ~ V _ { i } .$ , we consider that l satisfies $4 \ \operatorname { i f f } \ \forall i \ \in \ \{ 1 , 2 , \dots , n \}$ , either $A _ { i } ~ = ~ * ~ \mathrm { o r }$ $l _ { i } ~ = ~ A _ { i }$ . Furthermore, we employ a standard ABE scheme with constant-size ciphertexts [39] as a building block for constructing the on-chain access-control index. The concrete instantiation used by ESA is provided in §V.C as part of the system construction.

# IV. PROBLEM STATEMENT

In this section, we first present the system model, followed by a description of the threat model and design goals.

TABLE II SUMMARY OF NOTATIONS 

<table><tr><td>Notation</td><td>Definition</td></tr><tr><td> $\mathcal{I}, \mathcal{Q}$ </td><td>the index vector, the query vector</td></tr><tr><td> $Enc(\tau_D), Enc(\tau_Q)$ </td><td>the encrypted index, the trapdoor</td></tr><tr><td> $\mathcal{L}, \mathcal{A}$ </td><td>the attribute set, the access policy</td></tr><tr><td> $id \in \{0,1\}^*$ </td><td>the file identifier</td></tr><tr><td>MSK</td><td>the ASPE secret key  $\{M_1, M_2, S\}$ </td></tr><tr><td>DB</td><td>a set of files  $\{D_1, D_2, \cdots, D_n\}$ </td></tr><tr><td> $W_{D_i}$ </td><td>a keyword set  $\{w_1, w_2, \cdots, w_n\}$  of file  $D_i$ </td></tr></table>

# A. System Model

As shown in Fig. 2, our scheme considers a system model that comprises five entities: the data owner (DO), the authorized data users (DU), the cloud server (CS), the blockchain (BC), and the attribute authority (AA) (not shown).

• Data Owner. The DO (individual or organization) owns the raw data and is responsible for constructing the secure, searchable index of its data for sharing. Specifically, the DO extracts keywords, formulates access policies, and subsequently encodes them locally to construct the index for each file (step 1). Subsequently, the DO generates two distinct encrypted indexes: one is outsourced to the CS for keyword search and the other to the BC for authorized access and non-repudiation transactions (steps 2-3).   
• Data User. The DUs are the authorized data purchasers assigned with a set of attributes, enjoying search services. The DU requests keyword searches and, with assistance from the DO, generates the corresponding trapdoors, which are then sent to both the CS and BC (Step 4). Upon receiving search results, the DU utilizes its attribute key issued by the AA to decrypt the ciphertext (Step 7).   
• Cloud Server. The CS acts as a collaborator in data sharing, providing computational and storage resources, as well as search services. Upon receiving a trapdoor, it performs searches on the locally stored encrypted offchain index. It then requests the corresponding on-chain index linked to the search results from the BC (Step 5).   
• Blockchain. The BC serves as a trusted platform to guarantee protocol execution and facilitate fair payments through tamper-proof records. Upon receiving the search results from the CS, it executes the on-chain search algorithm via smart contracts and returns the ciphertexts of the target file identifiers to the DU (Step 6).   
• Attribute Authority. The AA is a trusted entity responsible for assigning attributes and issuing cryptographic keys. It provides encryption keys to the DO and attributebased decryption keys to DUs.

# B. Threat Model

We adopt a threat model consistent with prior secure keyword search literature [19]–[21]. In our system, the DO is typically a reputable or authoritative institution. It is assumed to be honest, faithfully executing the protocol and safeguarding data privacy. The DU, CS, and peer nodes of the blockchain are considered semi-honest. That is, they follow the protocol correctly but may attempt to infer sensitive information or access data beyond their authorized privileges. The BC itself is regarded as a trusted, tamper-resistant storage platform. Additionally, all communication channels among the entities are assumed to be secure. This threat model is realistic in scenarios where a resource-constrained DO outsources data to a powerful CS to provide search services to authorized users, while the BC maintains immutable records [9].

![](images/4bb46af3fe57b11211887328b49e1e737eae89207118d477db7c7d3fcf90b8a0.jpg)



Fig. 2. System Model of ESA.

To ensure data privacy, we follow the widely adopted Known Background Model (KBM) [19]–[22] in private fuzzy search applications for security proof. In this model, the CS may possess additional background knowledge, such as statistical information about files and queries (e.g., file distribution and keyword frequency), which can potentially be exploited to infer certain plaintext-ciphertext pairs. Following the formalism in [19], we use the concepts of history, view, and trace to characterize the information exposed during protocol execution. The history consists of all plaintext data processed in the system, including the dataset, keyword set, and historical queries. Given the history, the view is all the messages that an adversary can acquire, i.e., encrypted index and trapdoors. The trace is the background information that the adversary is permitted to infer from the history. Besides, we follow the standard security notions of indistinguishability against chosen-plaintext attacks (IND-CPA) for the ABE primitive.

Definition 1. (KBM-Security) Given a query sequence consisting of keyword-trapdoor pairs, a scheme π is said to KBM-secure if, for any probabilistic polynomial-time (PPT) adversary A, the distinguishing advantage between the real view V (generated by π) and the simulated view V′ (generated by a simulator S from the trace) is negligible.

# C. Design Goals

We design ESA to enable privacy-preserving search services for data sharing, with the following overarching goals:

• Multi-keyword Fuzzy Boolean Search: The proposed scheme should effectively support fuzzy search with arbitrary Boolean semantics over encrypted data.   
• Privacy Preservation: The privacy of both plaintext data and user queries must be protected.   
• Fine-grained Access Control: Only users whose attributes meet the access policies of the corresponding files are permitted to search for and access the shared data.   
• High Efficiency: The proposed scheme should incur low computational and communication overhead.

![](images/99ff647a081f0920dd5589fe3248a798b84ad28b9c6f4f6ee87b4c83f20b8c58.jpg)



![](images/6925e06f74569be4298b2d23c1f408c184a03fbfff275e63951e8a0167944007.jpg)



Fig. 3. Overview of the ESA index framework. Each file $D _ { i }$ is associated with two correlated indexes generated by the DO. The on-chain index $T _ { o n } [ x _ { i d _ { i } } ]$ is a lightweight ABE ciphertext encoding the attributes and file identification of $D _ { i } ,$ , and is stored on the BC. The off-chain index $T _ { o f f } [ x _ { i d _ { i } } ]$ i is constructed by the ASPE-encrypted Prime Filter that embeds the keywords and attributes of $D _ { i }$ i, and is stored on the CS. Both indexes share the same random key $\boldsymbol { x } _ { i d _ { i } } ,$ , enabling CS-side encrypted matching and BC-side decryption control to be jointly performed. The DU submits trapdoors for search, the CS requests the corresponding on-chain entry from the BC, and the matched result is returned to the DU for final decryption.

# V. THE DESIGN OF ESA

In this section, we integrate insights from both off-chain and on-chain index models with relevant cryptographic principles to design suitable indexing structures. Besides, we propose a security protocol that enables efficient multi-keyword fuzzy search with fine-grained access control.

# A. Main Idea

Our data sharing framework is built upon two innovative indexing structures, which are stored separately on the server and the blockchain, as shown in Fig. 3. These structures work collaboratively to support multi-keyword fuzzy search with fine-grained access control and non-repudiable transactions.

To enable privacy-preserving fuzzy search with fine-grained access control, we replace the traditional Bloom filter index for multi-keyword fuzzy search with a novel structure called the Prime Filter. The Prime Filter embeds both keywords and attribute values while preserving keyword distinguishability and maintaining a low false-positive rate for search tasks. During the construction of indexes and trapdoors, we employ specific prime encoding rules to integrate both keywords and attributes into the Prime Filter. It allows the system to efficiently search for files that meet both keyword queries and access policy requirements. The core of the Prime Filter’s design leverages the indivisibility of prime numbers. Specifically, the product of one prime number and the reciprocal of another prime is never an integer. Thus, we determine whether a file matches a query by checking whether the inner product of the corresponding index and trapdoor results in an integer.

To ensure secure access and non-repudiation, we leverage blockchain technology to promote honest protocol execution and fee payments. Specifically, both the search results returned by the CS and the trapdoors submitted by the DU are recorded on the BC for non-repudiation. A lightweight on-chain index $T _ { o n }$ is employed to enforce access control over the final data. After the CS completes the search using the off-chain index $T _ { o f f }$ , it returns the results to the BC and links them to the onchain index $T _ { o n }$ . The DU can then decrypt the relevant results based on $T _ { o n }$ and its attribute keys to obtain the final data. The entire transaction process is governed by a predefined smart contract, which mitigates disputes arising from insufficient evidence and establishes trust among all parties involved.

# B. Prime-based Off-chain Index

We now present the detailed design of the off-chain index structure, Prime Filter, and illustrate how to integrate the keyword search and access policies through this structure.

Bloom filters are well-known for rapid membership query support. In most multi-keyword fuzzy search schemes [19]– [21], both the index and query are represented as real vectors using Bloom filters. The magnitude of their inner product is then used to assess the match between an index and a query. To realize multi-keyword fuzzy search with access control, our basic idea is to encode keywords and attributes into the Bloom filter for each index and the corresponding query using prime numbers and their reciprocals. With this design, the inner product of the index and query will yield an integer if and only if both the keywords and attributes match. This property enables us to perform authorized fuzzy searches efficiently, without resorting to complex protocols.

However, two challenging problems remain: (1) To maintain a low false-positive rate, the Bloom filter must be sufficiently large, which in turn increases the computational overhead of search tasks. (2) Whether employing prime number encoding or the 0-1 encoding of Bloom filters, it is difficult to avoid conflicts between keyword matching and attribute matching. Intuitively, a correct match requires that the query contains all the attributes specified in the index, while the index includes all the keywords specified in the query. This inverse containment relationship makes it difficult to distinguish and process keywords and attributes in the index and query vectors, often resulting in incorrect matches.

We address the above issues through the careful design of a prime-based structure and an encoding strategy.

1) Prime Number Based Structure: To address the first problem, we propose a prime number-based structure to reduce the computational overhead of search tasks. Building upon the basic idea, we define an n-dimensional vector I and an melement sequence of prime numbers p, where n and m are coprime. The keyword insertion process follows these steps: Each keyword is first hashed to a positive integer r using a uniform hash function h. The integer r is then mapped via modulo operations: $u = r$ mod n and j = r mod m. Finally, the u-th prime number from $p$ is inserted into the j-th position of the vector I. Such an index structure helps to reduce the index dimension, thereby lowering the search overhead.

Observation. Given two coprime integers n and m, and two integers t and r chosen independently at random from $\{ 0 , 1 , \ldots , m n - 1 \}$ , define the events A as t ≡ r (mod $n ) ,$ , and B as $t \equiv r$ (mod m). Then, the probability that both A and B occur is given by $\operatorname* { P r } [ A \cap B ] = 1 / ( m n )$ .

According to this observation, the probability that any two keywords yield the same value through the modulo operations is $\frac { 1 } { m n }$ . We refer to this phenomenon as a coding conflict, as formally defined in Definition 2.

Definition 2. (Coding Conflict) Given two distinct keywords w1 and $w _ { 2 } ,$ and a uniform hash function $h : \{ 0 , 1 \} ^ { * } \to \mathbb { N } ,$ , let n and m be two coprime positive integers. A coding conflict occurs if $h ( w _ { 1 } )$ mod $n = h ( w _ { 2 } )$ mod m.

According to Def. 2, we can calculate the probability of a coding conflict occurring when inserting k keywords into an n-dimensional vector. Each keyword is mapped to a position in this vector using a sequence of m prime numbers as described above. Given k distinct keywords, the probability that a coding conflict occurs is $1 \ { \stackrel { \cdot } { - } } \ { \frac { P ( m n , k ) } { ( m n ) ^ { k } } }$ P (mn,k)(mn)k , where P (mn, k) = $P ( m n , k ) =$ $( m n ) ! / ( m n - k ) !$ denotes the number of permutations.

2) Prime Number Encoding Strategy: To address the second problem, we propose a reverse prime number encoding strategy to resolve conflicts between keyword search and access control policies. This strategy is inspired by the observation that a query succeeds only when an inverse containment relationship holds: the index must contain all queried keywords, and the query must contain all attributes required by the index. To implement this, we represent keywords and attributes as two disjoint sets of prime numbers. We then encode them into the index and trapdoor using reciprocal forms in opposite directions, leveraging the indivisibility property of prime numbers. Since the product of a prime and the reciprocal of a different prime is never an integer, this approach ensures that only when both keywords and attributes match will the inner product yield an integer. This design preserves the semantic distinction between keyword matching and attribute verification, thereby enabling accurate, fine-grained access control within fuzzy search.

3) Prime Filter Design: Building upon the aforementioned data structure and encoding strategy, we propose a new structure, termed the Prime Filter, for generating indexes and trapdoors, as outlined in Alg. 1. The core idea is to use LSH and PRFs to map keywords and attributes to two distinct prime-number sets, each with a prime cardinality. For index construction, each keyword is mapped to a unique prime number in its designated set, while each attribute is mapped to the reciprocal of a prime number from its corresponding set. These values are then inserted into the index vector. Conversely, for trapdoor generation, each keyword in the query is mapped to the reciprocal of a specific prime number within its set, whereas each attribute is mapped directly to a prime number within its corresponding set.

![](images/596d4effaea36c36c38c6b7b9aeed9f4705044df1d3ac5575b479428b8dec98c.jpg)



Fig. 4. Example of the construction procedure of the Prime Filter.

Example. The construction procedure of the Prime Filter for both the index and the trapdoor is illustrated in Fig. 4. Consider a keyword set $\{ A , B , C , D \}$ associated with a file, which is governed by the access policy $\{ A _ { 1 } , A _ { 2 } , A _ { 3 } \}$ , and a query $\cdots A \cap B \cap C ^ { \prime \prime }$ with $\{ A _ { 1 } , A _ { 2 } , A _ { 3 } , A _ { 4 } \}$ . We demonstrate the operation of Alg. 1 using two concise sets of prime numbers: $p = \{ 3 , 5 , 7 , 1 1 \}$ and $q = \{ 5 0 3 , 5 0 9 , 5 2 1 , 5 2 3 \}$ . Initially, the 2-gram algorithm is applied to quantize each keyword into a vector, which is subsequently mapped to a prime number using LSH and PRF (lines 2-8). Simultaneously, each attribute is mapped to a prime number via two PRFs (lines 13-15). Assuming the following mappings: $\{ A \to 3 , B \to 5 , C \to$ $7 , D  1 1 , A _ { 1 }  5 0 9 , A _ { 2 }  5 0 3 , A _ { 3 }  5 2 1 , A _ { 4 }  5 2 3 \}$ . These prime numbers and their reciprocals are then inserted according to the rules in Alg. 1 (lines 9–12, 16–19). Notably, the insertion rules for the index and the trapdoor are mutually reversed. In this example, the search and access polices are consistent, and the inner product of these two vectors yields an integer, indicating a successful match.

Comparison with Bloom Filter. The Prime Filter preserves the Bloom filter’s no-false-negative property. At the same time, it serves as a more expressive index that simultaneously supports fuzzy keyword embedding and attributepolicy embedding, which classical probabilistic filters cannot achieve. Like Bloom filters, the Prime Filter may incur false positives. Suppose k keywords are inserted into the Prime Filter using l standard hash functions according to the rule described above. The false positive rate of our structure is given by $( 1 ~ - ~ ( 1 ~ - ~ \frac { 1 } { m n } ) ^ { k \hat { l } } ) ^ { l }$ . In privacy-preserving fuzzy search systems, both Bloom filter and our Prime Filter are ultimately represented as n-dimensional real-valued vectors and encrypted using ASPE [19]–[22]. Hence, the search and storage complexities are determined by the encryptedindex dimension n. By introducing a factor $m ,$ the Prime Filter achieves a substantially lower false-positive rate than the Bloom filter for the same encrypted-index dimension. Equivalently, for a given false-positive target, it requires a smaller dimension, leading to reduced computational cost in encrypted search while preserving precision.

Remark. The structure constructed by Alg. 1 seamlessly integrates both search and access policies. In § V-D, we detail how it can be securely encrypted to preserve confidentiality.

# C. ABE-based On-chain Index

Considering that the Prime Filter, despite its extremely low false positive rate, may still result in unauthorized search results. To address this issue, we design an index stored on the blockchain, which strictly regulates access to the original data and provides verifiable records for further auditing. Moreover, to establish trust among data-sharing participants, the blockchain also serves as a trusted ledger that maintains immutable evidence. It can help to prevent disputes, such as the DU refusing to pay or the CS transmitting incorrect results. However, given the limited storage and computational capacity of the blockchain, a key challenge lies in designing lightweight on-chain indexes that can fulfill these goals efficiently.

Algorithm 1: Prime Filter Construction   
Input: LSH family $H = \{h_i : \{0,1\}^* \to \{0,1\}^* | i \in [1,l]\}$ ;
PRFs $h_0' : \{0,1\}^* \to R$ and $h_1' : \{0,1\}^* \to \{0,1\}^*$ ;
Keyword set $W_{D_i}$ ; Access policy A; Two prime sequences $p = \{p_1, p_2, ..., p_m\}, q = \{q_1, q_2, ..., q_l\}$ .

1 Initialize an n-dimensional vector I, setting all entries to 1;
2 foreach $w_j \in W_{D_i}$ do
3 Initialize a 676-dimensional vector $v_j$ with all entries 0;
4 Map $w_j$ to $v_j$ using 2-gram encoding;
5 foreach $v_j$ do
6 for i = 1 to l do
7 $s_{i,j} \leftarrow h_i(v_i); r_{i,j} \leftarrow h_0'(s_{i,j});$ 8 $p_k \leftarrow p[r_{i,j} \mod |p|]; pos \leftarrow r_{i,j} \mod n;$ 9 if mode = Index then
10 $I[pos] \leftarrow I[pos] \times p_k;$ 11 else if mode = Trapdoor then
12 $I[pos] \leftarrow I[pos] \times \frac{1}{p_k};$ 13 foreach $A_j \in A$ do
14 $s_j' \leftarrow h_1'(A_j); r' \leftarrow h_0'(s_j');$ 15 $q_k \leftarrow q[r' \mod |q|]; pos \leftarrow r' \mod n;$ 16 if mode = Index then
17 $I[pos] \leftarrow I[pos] \times \frac{1}{q_k};$ 18 else if mode = Trapdoor then
19 $I[pos] \leftarrow I[pos] \times q_k;$ 20 return the constructed Prime Filter I.

To address these issues, we propose a hybrid indexing architecture that offloads the computationally intensive fuzzy search operations to off-chain components while maintaining a lightweight on-chain index. The on-chain index is a simple key–value structure containing ABE ciphertexts. It works in conjunction with the off-chain index to enforce access control over the final data. To minimize blockchain overhead, the ciphertexts stored in the on-chain index follow the constantsize ABE ciphertext design of [39].

We first introduce some notation before presenting the algorithm. Let the attribute universe be $\mathcal { L } = \{ L _ { 1 } , L _ { 2 } , \ldots , L _ { n } \}$ , and for each $L _ { i }$ its value domain be $V _ { i } = \{ v _ { i , 1 } , v _ { i , 2 } , \ldots , v _ { i , n _ { i } } \}$ . The AA specifies an access policy $\boldsymbol { \mathcal { A } } = \{ A _ { 1 } , A _ { 2 } , . . . , A _ { n } \}$ over L and each DU has a concrete attribute assignment. With these definitions, we now present the ABE algorithm with constant ciphertext size as follows:

1) ABE.Setup: The AA randomly chooses $x , y \in \mathbb { Z } _ { p } ^ { * }$ as the master secret key, denoted as $\mathsf { A B E . m s k } = ( x , y )$ . Then, for each attribute $L _ { i } \in \mathcal { L } , 1 \le i \le n ,$ and each possible value $v _ { i , k _ { i } } \in V _ { i } , 1 \le k _ { i } \le n _ { i }$ , the public parameters are defined as:

$$
X _ {i, k _ {i}} = g ^ {- H _ {1} (x \| i \| k _ {i})}, \quad Y _ {i, k _ {i}} = e (g, g) ^ {H _ {1} (y \| i \| k _ {i})}. \tag {2}
$$

Here, $H _ { 1 } : \{ 0 , 1 \} ^ { * } \to \mathbb { Z } _ { p } ^ { * }$ is a hash function. The public key is given by ABE.mpk $= ^ { ' } ( g , \{ X _ { i , k _ { i } } , Y _ { i , k _ { i } } \} )$ .

2) ABE.KeyGen: Let $\boldsymbol { l } ~ = ~ ( l _ { 1 } , \ldots , l _ { n } )$ denote the DU’s concrete attribute assignment with $l _ { i } = v _ { i , k _ { i } ^ { * } } \in V _ { i } .$ . The $\mathbf { A A }$ randomly selects sk $\in \mathbb { Z } _ { p } ^ { * }$ and binds each attribute of the DU with its corresponding value. Specifically, for each i,

$$
\sigma_ {i, k _ {i} ^ {*}} = g ^ {H _ {1} (y \| i \| k _ {i} ^ {*})} \cdot H _ {2} (s k) ^ {H _ {1} (x \| i \| k _ {i} ^ {*})}, \tag {3}
$$

where $H _ { 2 } : \mathbb { Z } _ { p } ^ { * } \to \mathbb { G }$ is a hash function. The attribute secret key is defined as $S K = ( s k , \{ \sigma _ { i , k _ { i } ^ { * } } \} _ { i = 1 } ^ { n } )$ .

3) ABE.Enc: For a file protected by the access policy A, the DO aggregates all constrained attributes and corresponding values in A through multiplicative operations. Let ${ \mathcal { T } } _ { A } = \{ i \ |$ $i \in \{ 1 , 2 , \ldots , n \} , A _ { i } \neq * \}$ and, for each $i \in \mathcal { I } _ { A }$ , let $\kappa ( i )$ be the index such that $v _ { i , \kappa ( i ) } = A _ { i }$ . Define the aggregates

$$
\left\langle X _ {\mathcal {A}}, Y _ {\mathcal {A}} \right\rangle = \left\langle \prod_ {i \in \mathcal {I} _ {\mathcal {A}}} X _ {i, \kappa (i)}, \prod_ {i \in \mathcal {I} _ {\mathcal {A}}} Y _ {i, \kappa (i)} \right\rangle . \tag {4}
$$

Let id be the identifier of the file. The DO randomly selects $s \in \mathbb { Z } _ { p } ^ { * }$ and constructs the index ciphertext for the file as:

$$
e _ {i d} = \mathsf {A B E}. \mathsf {E n c} (m p k, i d, \mathcal {I} _ {\mathcal {A}}) = \left\{\mathcal {I} _ {\mathcal {A}}, C _ {0}, C _ {1}, C _ {2} \right\} \tag {5}
$$

where $C _ { 0 } = i d \cdot Y _ { \cal A } ^ { s } , C _ { 1 } = g ^ { s } , C _ { 2 } = X _ { \cal A } ^ { s }$ . This ciphertext is of constant size, meaning that its length remains independent of the number of attributes in A. The BC initializes an empty key-value map $T _ { o n }$ , and the ciphertext is inserted into the map as $T _ { o n } [ x _ { i d } ] = e _ { i d } .$ , where $x _ { i d }$ is a random number. The DO then sends $x _ { i d }$ to the CS, which uses it to associate with the off-chain index value of the corresponding file.

4) ABE.Dec: Upon receiving the ABE ciphertext $e _ { i d }$ from the BC, the DU computes the aggregated attribute key component $\begin{array} { r } { \sigma _ { \mathcal { A } } = \prod _ { i \in \mathbb { Z } _ { \mathcal { A } } } \sigma _ { i , k _ { i } ^ { * } } } \end{array}$ using their own secret key $S K$ . The ciphertext is then decrypted using the following equation:

$$
i d = \frac {C _ {0}}{e (\sigma_ {\mathcal {A}} , C _ {1}) \cdot e (H _ {2} (s k) , C _ {2})} \tag {6}
$$

In the proposed design, the decryption time remains constant, and the decryption process succeeds if and only if the user’s assignment l satisfies the access policy A defined by DO.

# D. Multi-keyword Fuzzy Boolean Search Protocol

Building upon the proposed off-chain and on-chain indexing scheme, we take conjunctive normal form queries as an example to present the detailed construction of our multi-keyword fuzzy Boolean search protocol. The protocol consists of the following five algorithms: KeyGen, IndexGen, TokenGen, Off-Chain Search, and On-Chain Search.

1) KeyGen(n, s): Given a parameter n, the DO generates the ASPE secret key $M S K = \{ M _ { 1 } , M _ { 2 } , S \}$ , where $M _ { 1 } , M _ { 2 } \in$ $\mathbb { R } ^ { n \times n }$ are invertible matrices, and $S ~ \in ~ \{ 0 , 1 \} ^ { n }$ is an ndimensional vector. Given another parameter $s _ { 1 } .$ , the DO generates two keys $H K = \{ K _ { i } \mid K _ { i } \stackrel { \mathbb { R } } { \longleftarrow } \{ 0 , 1 \} ^ { s _ { 1 } } , i \in \{ 0 , 1 \} \}$ for the two PRFs $h _ { 0 } ^ { \prime }$ and $h _ { 1 } ^ { \prime }$ . Next, the AA runs the ABE.Setup algorithm to generate the ABE master public key ABE.mpk and secret key ABE.msk. Then it executes ABE.KeyGen to generate the corresponding attribute key SK for the DU.

2) IndexGen(DB, MSK): The DO executes the index generation algorithm as follows:

• Data preprocessing. For each file $D _ { i }$ in the database DB, the DO extracts the keyword set $W _ { D _ { i } }$ from $D _ { i }$ and defines the access policy A. The DO then executes Alg. 1 to generate an n-dimensional Prime Filter $\tau _ { D }$ for $D _ { i }$ .   
• Index encryption. Initialize two n-dimensional zero vectors I ′ and $I ^ { \prime \prime }$ . For each $j \in [ 1 , n ]$ , if $S [ j ] = 1$ , set $I ^ { \prime } [ j ] = I ^ { \prime \prime } [ j ] = \tau _ { D } [ j ] ;$ ; if $S [ j ] = 0 $ , set $\begin{array} { r } { I ^ { \prime } [ j ] = \frac { 1 } { 2 } \tau _ { D } [ j ] + r } \end{array}$ and $\begin{array} { r } { I ^ { \prime \prime } [ j ] = \frac { 1 } { 2 } \tau _ { D } [ j ] - r , } \end{array}$ where r is a random number. Encrypt τD as $\mathit { E n c } ( \tau _ { D } ) = \{ M _ { 1 } ^ { \top } I ^ { \prime } , M _ { 2 } ^ { \top } I ^ { \prime \prime } \}$ , and store it as the off-chain index on the CS. Then, execute ABE.Enc to obtain the ciphertext $e _ { i d } .$ . The DO sets $T _ { o n } [ x _ { i d } ] = e _ { i d }$ as the on-chain index stored on the BC, where $x _ { i d }$ serves as a reference to the off-chain index.

3) Trapdoor(Q, MSK): The DO executes the trapdoor generation algorithm as follows:

• Data preprocessing. For a query Q, the DO takes each search keyword $w _ { i }$ from $Q$ and the DU’s attribute list l as input. The DO then executes Alg. 1 to generate an n-dimensional Prime Filter $\tau _ { Q }$ for $Q$ .   
• Trapdoor encryption. Initialize two n-dimensional zero vectors $Q ^ { \prime }$ and $Q ^ { \prime \prime }$ . For each $j \in [ 1 , n ]$ , if $S [ j ] = 0$ , set $Q ^ { \prime } [ j ] = Q ^ { \prime \prime } [ j ] = \tau _ { Q } [ j ] ; { \mathrm { i f ~ } } S [ j ] = 1$ , set $\begin{array} { r } { Q ^ { \prime } [ j ] = \frac 1 2 \tau _ { Q } [ j ] + } \end{array}$ $r ^ { \prime }$ and $\begin{array} { r } { Q ^ { \prime \prime } [ j ] = \frac { 1 } { 2 } \tau _ { Q } [ j ] - r ^ { \prime } } \end{array}$ , where $r ^ { \prime }$ is a random number. Encrypt $\tau _ { Q }$ as $\tilde { E } n \dot { c } ( \tau _ { Q } ) = \{ M _ { 1 } ^ { - 1 } Q ^ { \prime } , M _ { 2 } ^ { - 1 } Q ^ { \prime \prime } \}$ and use it as the trapdoor for the Off-Chain Search algorithm.   
4) Off-Chain Search(Enc(τD), Enc(τQ)): The CS performs secure matching between the encrypted index $E n c ( \tau _ { D } )$ and the encrypted trapdoor $E n c ( \tau _ { Q } )$ by computing

$$
R = (M _ {1} ^ {\top} I ^ {\prime}) ^ {\top} (M _ {1} ^ {- 1} Q ^ {\prime}) + (M _ {2} ^ {\top} I ^ {\prime \prime}) ^ {\top} (M _ {2} ^ {- 1} Q ^ {\prime \prime}). \tag {7}
$$

If R satisfies the matching condition $( \mathbf { e } . \mathbf { g } . , \ R \in \mathbb { Z } )$ , the CS returns the key $x _ { i d }$ of the corresponding entry in the on-chain map $T _ { o n }$ to the DU; otherwise, the match fails.

5) On-Chain Search( $\{ x _ { i d } \} ) .$ : The DU invokes the smart contract to search over the set $\{ x _ { i d } \}$ obtained from the CS. The smart contract returns the corresponding ciphertexts $\{ e _ { i d } \}$ of the file identifiers, which are encrypted using ABE. The DU then applies the ABE.Dec algorithm to decrypt these ciphertexts and recover the identifiers of the matching files. Using these file identifiers, the DU can subsequently obtain the target data from the DO.

E. Extension to General Boolean Search and Non-repudiation

1) Extension to General Boolean Search: As previously discussed, ESA has been presented primarily for conjunctive keyword searches. Nevertheless, it can be naturally extended to support fuzzy search with arbitrary Boolean semantics. Any Boolean expression can be rewritten into disjunctive normal form (DNF) as $\mathcal { C } _ { 1 } \vee \mathcal { C } _ { 2 } \vee \cdots \vee \mathcal { C } _ { k }$ , where each clause $\mathcal { C } _ { i } = \bigwedge _ { w \in P _ { i } } w \wedge \bigwedge _ { u \in N _ { i } } \neg u$ contains a set $P _ { i }$ of positive (AND) keywords and a set $N _ { i }$ of negated (NOT) keywords.

For each clause $\mathcal { C } _ { i } ,$ we construct a query matrix $Q _ { i } \in \mathbb { R } ^ { t _ { i } \times }$ n as follows (see Fig. 5): the first row of $Q _ { i }$ encodes the conjunction of all keywords in $P _ { i }$ using the same Prime-Filter-based encoding as in the basic conjunctive search; each

![](images/c38c08939f0bdb875d9690280f2c78c16e5fd138418fe13307c2511e4755a0bb.jpg)



Fig. 5. Working process of general Boolean fuzzy search.

remaining row encodes one negated keyword $u \in N _ { i }$ under NOT semantics. Given the encrypted index vector $I ,$ the server computes the corresponding result vector $R _ { i }$ for each clause. A file is deemed to satisfy the Boolean query if and only if there exists some clause $\mathcal { C } _ { i }$ such that the first entry of $R _ { i }$ is an integer (all AND-keywords in $P _ { i }$ are satisfied), while all other entries of $R _ { i }$ are non-integers (each NOT-keyword in $N _ { i }$ is absent). In this way, AND semantics are captured by the first row of each clause matrix, NOT semantics by the additional rows, and OR semantics by accepting a file as long as at least one clause $\mathcal { C } _ { i }$ satisfies the above condition. This construction thus supports general Boolean fuzzy search.

2) Extension to Non-repudiation. In data-sharing systems, driven by economic incentives, the parties involved may engage in malicious behaviors such as dishonest payments or incomplete computations. Inspired by [31], our solution introduces non-repudiation through the use of smart contracts, aiming to establish a financially equitable search mechanism. In our scheme, all participants are treated equally and are economically incentivized to perform computations honestly. As a result, honest participants consistently receive their rightful rewards, while malicious participants are subject to penalties. For simplicity, we treat the non-repudiation mechanism as a subroutine and provide only a high-level overview.

As illustrated in Fig. 6, we utilize a smart contract to facilitate fair transactions. In this process, the DS first submits a deposit to the smart contract. For each search, encrypted trapdoors and search results are stored on the blockchain. The DU must also deposit a transaction amount and submit a trapdoor to the smart contract. In addition, we introduce a time-locked transaction period, denoted as $T _ { 1 }$ . Within this period, the CS can submit off-chain search results to the contract for on-chain search and claim rewards. If $T _ { 1 }$ elapses without completion, the DU’s search request expires, and the deposit is refunded. Owing to the indistinguishability of trapdoors stored on the blockchain, the DU can repeatedly search for the same content and observe whether the CS performs computations honestly and returns consistent results, thereby ensuring the completeness of search results and achieving non-repudiation.

# VI. THEORETICAL ANALYSIS

In this section, we present a comprehensive analysis of ESA in terms of correctness, complexity, and security.

# A. Correctness Analysis

Theorem 1. The ESA protocol is correct; that $i s ,$ for each query, it returns correct results with overwhelming probability.

TABLE III COMPARISON OF REPRESENTATIVE FUZZY SEARCH SCHEMES 

<table><tr><td></td><td>Multi-keyword Search</td><td>Flexibility</td><td>Access Control</td><td>Communication Cost</td><td>Storage Cost</td><td>Search Time</td></tr><tr><td>Wang et al. [19]</td><td>√</td><td>×</td><td>×</td><td> $\mathcal{O}(b)$ </td><td> $\mathcal{O}(N \cdot b)$ </td><td> $\mathcal{O}(N \cdot b)$ </td></tr><tr><td>Fu et al. [20]</td><td>√</td><td>×</td><td>×</td><td> $\mathcal{O}(b)$ </td><td> $\mathcal{O}(N \cdot b)$ </td><td> $\mathcal{O}(N \cdot b)$ </td></tr><tr><td>Chen et al. [21]</td><td>√</td><td>×</td><td>×</td><td> $\mathcal{O}(b)$ </td><td> $\mathcal{O}(\sum_{w \in W} |D(w)| \cdot b)$ </td><td> $\mathcal{O}(|D(w)| \cdot b)$ </td></tr><tr><td>Li et al. [22]</td><td>√</td><td>×</td><td>×</td><td> $\mathcal{O}(b)$ </td><td> $\mathcal{O}(N \cdot b)$ </td><td> $\mathcal{O}(N \cdot b)$ </td></tr><tr><td>Tong et al. [40]</td><td>√</td><td>×</td><td>×</td><td> $\mathcal{O}(k \cdot l)$ </td><td> $\mathcal{O}(N \cdot b)$ </td><td> $\mathcal{O}(k \cdot l \cdot N)$ </td></tr><tr><td>Liu et al. [23]</td><td>√</td><td>√</td><td>×</td><td> $\mathcal{O}(\mu \cdot k \cdot d)$ </td><td> $\mathcal{O}(N \cdot \kappa_i \cdot d)$ </td><td> $\mathcal{O}(N \cdot \mu \cdot k \cdot \kappa_i \cdot d)$ </td></tr><tr><td>Ours</td><td>√</td><td>√</td><td>√</td><td> $\mathcal{O}(d)$ </td><td> $\mathcal{O}(N \cdot d)$ </td><td> $\mathcal{O}(N \cdot d)$ </td></tr></table>

N: the number of files; W : the keyword space; |D(w)|: the number of files matching keyword w. b: the dimension of the Bloom-filter-based index vector; d: the index and query vector length in [23] and our scheme (d ≪ b); l: the number of hash functions; k: the number of keywords in a query; κi: the number of keywords in a file Di; µ: the security parameter in [23]. Flexibility denotes the ability to combine multiple keywords with logical operators such as AND and OR.

![](images/a3eaba4c6e78fde70a5e75b984d0e8c09affde9b543a84ca5427d10a3d188eeb.jpg)



Fig. 6. System model of our non-repudiation design.

Proof. In the ESA protocol, the correctness of the constantsize ABE algorithm follows directly from the results presented in [39]; thus, we omit its proof for brevity. The correctness of our search algorithm relies on the accurate matching of keywords and attributes, which is ensured by the indivisibility property of prime numbers. The search result—namely, the inner product of the index and trapdoor—will be an integer if and only if both the keyword search policy and the access policy conditions are satisfied. Moreover, the correctness of the ciphertext inner product computation is guaranteed by the ASPE scheme, as described in [37]. We now prove that the false positive rate is extremely low.

Coding Conflict Probability. A coding conflict occurs when two distinct keywords are mapped to the same position in the n-dimensional index vector and the m-dimensional prime sequence, respectively. This is equivalent to randomly selecting k numbers with replacement from a set of mn distinct elements. The probability that at least two of the k selected numbers coincide (i.e., a collision occurs) is given by $\begin{array} { r } { 1 - \frac { P ( m n , k ) } { ( m n ) ^ { k } } } \end{array}$ .

False Positive. Both the Prime Filter and the LSH components introduce false positives. According to Alg. 1, there are mn possible mapping outcomes for any keyword. Analogous to the Bloom filter, the false positive rate for an n-dimensional Prime Filter with an m-dimensional prime sequence using l hash functions is given by $( 1 - ( 1 - \textstyle { \frac { 1 } { m n } } ) ^ { k \bar { l } } ) ^ { l }$ , where k denotes the number of inserted items. For an $( r _ { 1 } , r _ { 2 } , p _ { 1 } , p _ { 2 } ) \cdot$ - sensitive LSH family, the false positive rate introduced by LSH is $p _ { 2 } ^ { l }$ [19]. Therefore, the overall false positive rate of ESA is approximated as $( 1 - ( 1 - p _ { 2 } ) ^ { k } ( 1 - \frac { \ l _ { 1 } } { m n } ) ^ { k l } ) ^ { l }$ 1 )kl)l. This result indicates that ESA achieves higher precision even with a smaller vector dimension. Furthermore, our on-chain ABEbased index ensures that data beyond a user’s access policy remains undecryptable, thereby preserving correctness. □

# B. Complexity Analysis

We theoretically analyze the asymptotic complexities of communication, storage, and computation for ESA, and compare these with existing multi-keyword fuzzy search schemes.

Theorem 2. Given a query Q, the communication cost for trapdoor transmission, the storage cost for the index, and the computation cost for search in ESA is given by O(d), O(N ·d), and $O ( N \cdot d ) ,$ , respectively. Here, d denotes the length of the index and N is the total number of files.

Proof. We focus on several important operations that contribute to the communication, storage, and computation costs. The communication cost primarily arises from trapdoor transmission, which requires one communication round per query. This incurs a complexity that is linear in the index length, i.e., $\mathcal O ( d )$ . The storage cost includes two parts: (1) the index stored on the DS, with complexity of $\mathcal { O } ( N \cdot d )$ , linear in both the number of files and d; (2) the index stored on the BC, with a constant size per file, resulting in complexity linear in the number of files. The computation cost for search is dominated by the matching operation, namely the inner product between the trapdoor and the index, with complexity of $\mathcal { O } ( N \cdot d )$ .

Comparison with existing works: As shown in Table III, this work presents the first secure fuzzy search protocol that supports arbitrary Boolean semantics and fine-grained access control, while achieving a search cost of only $\mathcal { O } ( N \cdot d )$ . In contrast, existing secure fuzzy search protocols [19]–[23], [40] do not support access control and generally incur a search cost of $\mathcal { O } ( N \cdot b )$ , where $b > d .$ Among these, the scheme in [21] achieves faster performance by limiting the search to a smaller file space. Regarding communication and storage costs, our scheme also demonstrates superior efficiency by reducing the factor b used in most related works to the smaller parameter d. Overall, ESA substantially reduces the costs associated with secure fuzzy search while enhancing functionality.

# C. Security Analysis

Recall that ESA integrates SE and ABE to enable fuzzy search with fine-grained access control. Under the adversarial model described in §IV-B, we first analyze the data confidentiality of the ABE-encrypted ciphertexts under IND-CPA security and then prove the KBM-security of ESA.

Lemma 1. (IND-CPA Security of the ABE Primitive) The constant-size ABE primitive of [39] used in ESA is IND-CPA secure under the bilinear Diffie–Hellman exponent assumption. Therefore, the ABE ciphertext tuple $( C _ { 0 } , C _ { 1 } , C _ { 2 } )$ stored in the on-chain index inherits this IND-CPA indistinguishability.

Proof. This lemma follows directly from the main security theorem of [39], where the authors formalize the IND-CPA game for ABE and prove that no PPT adversary can distinguish encryptions of two equal-length messages with more than negligible advantage. Since ESA uses this ABE primitive without modifying its encryption interface, the ciphertext components $\big \{ C _ { 0 } , C _ { 1 } , C _ { 2 } \big \}$ stored in the on-chain index preserve the same IND-CPA guarantees. Hence, these ciphertexts can be replaced by simulated ABE encryptions in our KBM-security proof without affecting the adversary’s view. □

To demonstrate the security of our fuzzy search scheme, we adopt the widely used simulation-based proof technique [19]. Before presenting the proof, we first introduce the necessary formal notations.

History: $\mathcal { H } = ( D B , I _ { 1 } , I _ { 2 } , W _ { Q } , A )$ , where H is the raw data in plaintext. Specifically, DB is the file set, $I _ { 1 }$ and $I _ { 2 }$ are the indexes constructed from DB and stored by the DS and BC, respectively; $W _ { Q } = ( w _ { 1 } , w _ { 2 } , \cdot \cdot \cdot , w _ { n } )$ is a series of queries, and $A = \left( A _ { 1 } , A _ { 2 } , \cdot \cdot \cdot , A _ { m } \right)$ is an access policy.

View: $\mathcal { V } = ( \sigma _ { I _ { 1 } } , \sigma _ { I _ { 2 } } , \sigma _ { T } )$ , where V is the ciphertext form of $\mathcal { H } , \mathrm { i . e . }$ , the off-chain index $\sigma _ { I _ { 1 } }$ , the on-chain index $\sigma _ { I _ { 2 } } ,$ , and the trapdoor $\sigma _ { T }$ . The adversary can only see V.

Trace: $T r ( \mathcal { H } )$ denotes the information that the adversary can capture, including the access pattern and search pattern. The access pattern is denoted as $\mathcal { A P } ( D B , W _ { Q } )$ = $\left\{ \alpha ( w _ { 1 } ) , \alpha ( w _ { 2 } ) , \ldots , \alpha ( w _ { n } ) \right\}$ , where $\alpha ( w _ { i } ) ~ = ~ ( D _ { j } , s _ { i j } ) , j ~ \in$ $\left[ 1 , | D B | \right]$ , and $s _ { i j }$ denotes the relevance score between the keyword wi and the file $D _ { j }$ . The search pattern is denoted as $\mathcal { Q P } ( D B , W _ { Q } ) = M$ , where M is a binary matrix. We say that the queries wj and wz get the same file if $M _ { i j } = M _ { i z } = 1$ .

Theorem 3. (KBM-Security) The ESA protocol is secure under the Known Background Model.

Proof. Given two histories that yield the same Trace, if an adversary cannot distinguish which one is generated by the simulator, the privacy-preserving scheme is considered secure. To demonstrate this, let S be a simulator that can generate a view $\mathcal { V } ^ { \prime } = ( \sigma _ { I _ { 1 } } ^ { \prime } , \sigma _ { I _ { 2 } } ^ { \prime } , \sigma _ { T } ^ { \prime } )$ indistinguishable from the adversary’s view V. The simulator S proceeds as follows:

Step 1: S randomly selects $D _ { i } ^ { \prime } \in \{ 0 , 1 \} ^ { | D _ { i } | }$ for each $D _ { i } \in$ DB, where $i \in [ 1 , | D B | ]$ , and outputs $\bar { D } B ^ { \prime } = \{ D _ { i } ^ { \prime } | i \in$ [1, |DB|]}.

Step 2: S randomly chooses two invertible matrices $M _ { 1 } ^ { \prime }$ , $M _ { 2 } ^ { \prime } ~ \in ~ \mathbb { R } ^ { n \times n }$ , an n-dimensional vector $S ^ { \prime } \in \{ 0 , 1 \} ^ { n }$ , two pseudo-random functions $h _ { 0 } ^ { \prime \prime } , h _ { 1 } ^ { \prime \prime }$ , and an ABE secret key $A B E . m s k ^ { \prime } . \ S$ sets $M S K ^ { \prime } = \{ \bar { M } _ { 1 } ^ { \prime } , M _ { 2 } ^ { \prime } , S ^ { \prime } \}$ .

Step 3: S constructs $\sigma _ { T } ^ { \prime } , \sigma _ { I _ { 1 } } ^ { \prime } , \sigma _ { I _ { 2 } } ^ { \prime }$ as follows:

• σ′T : S constructs $W _ { Q } ^ { \prime } \mathrm { , }$ , where for each $w _ { i } ~ \in ~ W _ { Q }$ , it generates an n-dimensional vector $w _ { i } ^ { \prime } \in \mathsf { 1 } ^ { n }$ . Numbers are inserted into $w _ { i } ^ { \prime } ,$ ensuring that each inserted prime number or reciprocal of the prime number is the same

as the result of executing Alg. 1 on $w _ { i }$ , but in a different position. Since each attribute can be treated as a keyword, the construction follows the same method. For each $w _ { i } ^ { \prime } \in W _ { Q } ^ { \prime }$ , the corresponding trapdoor is generated via the T rapdoor(w′, M SK′) algorithm, resulting in $\sigma _ { T } ^ { \prime } = \{ \mathrm { E n c } ( w _ { 1 } ^ { \prime } )$ , Enc $( w _ { 2 } ^ { \prime } ) , \ldots , \mathrm { E n c } ( w _ { k } ^ { \prime } ) \}$ }.

• $\sigma _ { I _ { 1 } } ^ { \prime }$ : To generate $\sigma _ { I _ { 1 } } ^ { \prime } , ~ { \cal { S } }$ generates an n-dimensional vector $I _ { D _ { i } ^ { \prime } } \in \mathbb { 1 } ^ { n }$ as the index for each file $D _ { j } ^ { \prime }$ . For each $w _ { i } \in W _ { Q } , \operatorname { i f } \ w _ { i } \in f _ { j }$ , where $1 \leq j \leq | D B | , \bar { s }$ updates ${ { I } _ { { D } _ { i } ^ { \prime } } }$ to $I _ { D _ { i } ^ { \prime } } \times w _ { i } ^ { \prime } .$ . The IndexGen algorithm is then used to produce $\sigma _ { I _ { 1 } } ^ { \prime } = E n c ( I _ { D _ { i } ^ { \prime } } )$ for all $1 \leq j \leq | D B |$ . • $\sigma _ { I _ { 2 } } ^ { \prime } \colon S$ generates $\sigma _ { I _ { 2 } } ^ { \prime }$ by calling the ABE.Enc algorithm using the key ABE.msk′.

Step 4: S outputs the simulated view $V ^ { \prime } = ( \sigma _ { I _ { 1 } } ^ { \prime } , \sigma _ { I _ { 2 } } ^ { \prime } , \sigma _ { T } ^ { \prime } )$

We now argue the indistinguishability between the real view V and the simulated view $\mathcal { V } ^ { \prime }$ . By Lemma 1, the ABE-based ciphertexts of $\sigma _ { I _ { 2 } }$ are IND-CPA secure, and thus no PPT adversary can distinguish $\sigma _ { I _ { 2 } }$ from the simulated ciphertexts $\sigma _ { I _ { 2 } } ^ { \prime }$ . Moreover, the indistinguishability of $\sigma _ { I _ { 1 } }$ and $\sigma _ { I _ { 1 } } ^ { \prime }$ , as well as that of $\sigma _ { T }$ and $\sigma _ { T } ^ { \prime }$ , follows from the security of ASPE and the pseudo-random functions. Additionally, the adversary, armed with keyword and trapdoor pairs, cannot discern the output of the linear analysis [41] from a random string, given the indistinguishability property of the pseudo-random function. Therefore, no PPT adversary can distinguish V from $\mathcal { V } ^ { \prime }$ , establishing KBM-security.

# VII. IMPLEMENTATION AND EVALUATIONS

In this section, we evaluate ESA by assessing its computational and communication costs, search precision, and onchain performance, in comparison with SOTA schemes.

# A. Experiment Setup

Implementation and Dataset. We develop a prototype of ESA on a machine equipped with 16GB RAM and 16-core AMD processors, running Ubuntu 20.04. The smart contract is deployed on a locally simulated Ethereum network using TestRPC. The data owner’s side and the smart contract are implemented in Python and Java, respectively, with Solidity and JavaScript used as intermediate interactive languages. To validate the practical feasibility of our scheme, we perform a performance evaluation on a medical conversation dataset [42] containing 792,099 question-answer pairs. For experimental purposes, this dataset is divided into 10,000 files.

Parameters. Our evaluation is under different parameter settings. Specifically, we set the file set size within the range $N \in [ 2 0 0 0 , 1 0 0 0 0 ]$ and extract 10 to 20 keywords from each file, resulting in a total of 15,217 keywords for building the indexes. The attribute space is set to $\alpha \in [ 0 , 3 2 ]$ ; for each file, we randomly assign a set of attribute values as access policies. Each query contains $k \in [ 1 , 2 0 ]$ keywords. Similar to previous work [19]–[21], we generate fuzzy queries by replacing a character in each keyword and allowing at most two fuzzy keywords per query. We also randomly generate attribute values to construct trapdoors. We set the Prime Filter size n to 251 dimensions, the prime sequence sizes |p| and |q| to 41 and 23, respectively, and the number l of LSH to 10.

![](images/cc87fef23c608685f435fb2267af753e4491d51df1644c1f6f52182e26742476.jpg)



(a) Build index vs. file set size

![](images/50b3695b500a23a70298ece1c9c3cdb599eff55bce6eafef300834394c04b6d5.jpg)



(b) Trapdoor vs. keyword number

![](images/b70a6e2fd3ca8cd313e77ce742e39415244bccee0f44ef410799b692f6b56c52.jpg)



(c) Search vs. file set size

![](images/6fba0bd39eaadfdbd7358e6103993bc256a2882cf023e037f279d441069df439.jpg)



(d) Search vs. keyword number   
Fig. 7. Comparison of the execution time between ESA, VRFMS, PIPE, and MFS. (a) The index generation time with different N. (b) The trapdoor generation time of a query with different k. (c) The time for search under different file set sizes with fixed query keyword number k = 5. (d) The time for search under different keyword numbers with fixed file size N = 10, 000.

![](images/e752815ac9ce3afb08966b72f710f07188ebeddd438a6ff20c44142f7eae144d.jpg)



(a) Search vs. attribute number

![](images/98794fdcf7c5a40bde29a5a9c68c6f88351d6ee8bd0e966a47264315a30161f6.jpg)



(b) Trapdoor size   
Fig. 8. Analysis of the impact of the number of attributes on search efficiency and the impact of keywords on communication cost.

The parameters are selected to balance security, false positives, and efficiency. We keep n at the consistent scale as [23] to ensure sufficient entropy for ASPE-based encryption with a compact index. We use l = 10, which balances precision gain and hashing cost. We choose primes |p| and |q| to maintain coprimality with n and reduce collisions. Under our maximum keyword setting, the false-positive rate of the Prime Filter is approximately below $1 0 ^ { - 6 }$ according to the analysis in §VI-A. Moreover, sensitivity results in §VII-F confirm robustness across a wide range of parameters.

Baselines. For multi-keyword fuzzy search methods, we select the widely used framework MFS [19], along with two SOTA schemes, VRFMS [22] and PIPE [23]. Besides, we choose a commonly used ABKS scheme [10], which supports authorized exact search, as a baseline and use LSH functions to process the keywords in an attempt to support both access control and fuzzy search. For on-chain performance evaluation, we compare ESA with Medshare [5], which supports exact search and access control for blockchain-based data sharing.

# B. Evaluation of Computation Overhead

We present the computational overhead of ESA and the baseline methods in Fig. 7. The experimental results demonstrate that ESA significantly outperforms all baselines with respect to trapdoor construction and search efficiency. In addition, we analyze the impact of the number of attributes on search efficiency, as well as the performance of the ABE protocol for the on-chain index (§V-C).

Index Construction. The index construction process is a one-time computation that consists of two main steps: index generation and encryption. The computational overhead in index generation primarily stems from hash function computations, whereas index encryption is mainly dominated by matrix multiplications. As shown in Fig. 7(a), the time cost of index construction for all methods scales linearly with the number of documents. ESA is significantly more efficient than MFS and VRFMS, and its efficiency is comparable to that of PIPE. Specifically, ESA is approximately 47× faster than MFS and 58× faster than VRFMS. Both ESA and PIPE exhibit superior performance, thanks to their low-dimensional index designs.

Trapdoor Construction. The trapdoor construction process is analogous to index construction. We evaluate the impact of the number of keywords contained in a query on trapdoor construction efficiency. As shown in Fig. 7(b), ESA demonstrates slightly better performance than PIPE and markedly outperforms VRFMS and MFS, being approximately 4× faster than PIPE and 270× faster than both VRFMS and MFS.

Search Delay. With regard to search performance, Figs. 7(c) and 7(d) illustrate the effects of both the number of documents and the number of query keywords on search delay at the CS side. Owing to the Prime Filter design, ESA consistently achieves superior performance compared to the baselines.

• Impact of the number of documents. We fix the number of query keywords at k = 5. As shown in Fig.7(c), the search time for each scheme increases linearly with the dataset size. Notably, ESA outperforms all other methods, being approximately 2× faster than PIPE, 3.4× faster than MFS, and 86× faster than VRFMS.   
• Impact of the number of keywords. We fix the number of documents at N = 10, 000. As shown in Fig.7(d), the search time of PIPE increases linearly with the number of query keywords, whereas the search times for MFS, VRFMS, and ESA remain nearly constant. Among all schemes, ESA exhibits the lowest overall search time. For example, when N = 10, 000 and k = 20, a single search requires 0.6s for MFS, 30s for VRFMS, and 2.7s for PIPE, while ESA completes the search in just 0.3s.

Attribute Influence Analysis. To evaluate the impact of attribute set size on search delay, we assess the performance of ESA with varying attribute sets. As shown in Fig. 8(a), we conduct experiments with different file set sizes and numbers of keywords. The results indicate that the attribute set size has little effect on search delay, as the Prime Filter size remains fixed regardless of how many attributes are inserted.

Performance of the ABE Protocol for On-Chain Index. We evaluate the latency overhead and ciphertext size of the adopted ABE scheme under varying numbers of attributes. As shown in Table IV, the time costs for the Setup and KeyGen phases increase linearly with the number of attributes, while the computational overheads for the Enc and Dec phases, as well as the ciphertext size, remain constant and incur minimal time consumption. These properties make the scheme wellsuited for resource-constrained users and blockchain systems. General Boolean Search Delay. We further evaluate the efficiency of the general Boolean search introduced in §V-E1. Several representative Boolean queries in DNF form are tested, including pure conjunction, conjunction with negation, and multi-clause disjunctions. The search efficiency is measured with N = 4000 under the same settings as the conjunctivesearch experiments. As shown in Table V, a three-keyword conjunctive query costs 139 ms and is used as the baseline. Adding one negated keyword increases the latency only slightly to 151 ms (1.09×). When the query consists of two and three clauses, the cost grows to 283 ms (2.04×) and 421 ms (3.03×), respectively, which is roughly linear in the number of clauses. These results indicate that ESA supports general Boolean fuzzy search with only a small clause-dependent overhead compared with basic conjunctive search, while preserving the overall efficiency characteristics of ESA.

TABLE IV TIME AND STORAGE COST OF ABE SCHEME FOR ON-CHAIN INDEX (MS). 

<table><tr><td>Attribute Number</td><td>Setup</td><td>KeyGen</td><td>Encrypt</td><td>Decrypt</td><td>Ciphertext Size (Byte)</td></tr><tr><td>4</td><td>27.45</td><td>16.11</td><td>2.13</td><td>7.05</td><td>248</td></tr><tr><td>8</td><td>52.68</td><td>47.94</td><td>3.84</td><td>6.03</td><td>248</td></tr><tr><td>16</td><td>80.67</td><td>74.37</td><td>4.60</td><td>5.58</td><td>248</td></tr><tr><td>24</td><td>102.69</td><td>93.62</td><td>2.54</td><td>4.84</td><td>248</td></tr><tr><td>32</td><td>148.71</td><td>151.69</td><td>5.03</td><td>6.77</td><td>248</td></tr></table>

TABLE V EFFICIENCY OF BOOLEAN SEARCH UNDER DIFFERENT LOGICAL FORMS.

<table><tr><td>Query</td><td>Clauses</td><td>Time (ms)</td><td>Overhead</td></tr><tr><td> $w_{1} \wedge w_{2} \wedge w_{3}$ </td><td>1</td><td>139</td><td>1×</td></tr><tr><td> $w_{1} \wedge w_{2} \wedge \neg w_{3}$ </td><td>1</td><td>151</td><td>1.09×</td></tr><tr><td> $(w_{1} \wedge w_{2} \wedge \neg w_{3}) \vee (w_{4} \wedge \neg w_{5})$ </td><td>2</td><td>283</td><td>2.04×</td></tr><tr><td> $(w_{1} \wedge w_{2}) \vee (w_{3} \wedge w_{4}) \vee w_{5}$ </td><td>3</td><td>421</td><td>3.03×</td></tr></table>

# C. Evaluation of Communication Overhead

Considering that the primary communication cost arises from trapdoor transmission, we test the impact of the number of query keywords on trapdoor size to assess communication overhead. As shown in Fig. 8(b), as the number of keywords increases, the trapdoor size for PIPE grows, while ESA, MFS, and VRFMS remain stable. That is because the trapdoor dimensions are fixed in these three schemes. ESA is slightly higher than MFS and PIPE, but outperforms VRFMS. All four methods exhibit trapdoor construction sizes below 500 KB, meeting practical requirements for real-world applications.

# D. Evaluation of Search Precision

We evaluate the effectiveness of our scheme using precision, a widely adopted metric in fuzzy search systems [19], [20], [23] for measuring the ability to suppress false positives. Let $t _ { p }$ denote true positives and $f _ { p }$ false positives. Precision is defined as $t _ { p } / ( t _ { p } + f _ { p } )$ . A higher precision indicates a lower false-positive rate and thus a stronger filtering capability. A key parameter in these schemes is the number of keywords k in a query. In addition to supporting access control, our method introduces a new parameter: the number of attributes in a query, denoted as α, which may influence search precision. Therefore, we evaluate the precision for both exact and fuzzy searches under various settings of k and α.

Exact Search. Fig. 9(a) presents the precision of these schemes under exact keyword search. The results show that the precision of MFS slightly decreases from 100% to 97% as k increases from 1 to 10, owing to the accumulation of false positives generated per keyword. In contrast, the precision of VRFMS and PIPE marginally increases from 95% to 98% and from 96% to 100%, respectively. Similarly, the precision of ESA shows an increase from 97% to 100% as k increases when $\alpha = 0$ , since the impact of false positives caused by LSH functions diminishes for larger k.

Fuzzy search. Fig. 9(b) shows that ESA outperforms both MFS and VRFMS—achieving a 9%–30% improvement in precision—and performs comparably to PIPE. Specifically, ESA’s precision remains steady at around 95% when k = 1, then rises to nearly 100% for $k \geq 4 ,$ maintaining perfect precision as the number of keywords increases. This improvement stems from the reduction in false positives: as more correct keywords appear in the query, the impact of fuzzy matches diminishes.

Attribute Influence Analysis. We further examine the effect of attribute set size on search precision under various numbers of query keywords, as depicted in Fig. 9(c) and 9(d). The observed fluctuations in precision result from mapping attributes to different prime numbers and their reciprocals, which can cause slight variations in determining whether the inner product is an integer. Overall, the influence of the attribute set size on precision is negligible.

Evaluation of the LSH-based ABKS Scheme. To demonstrate the effectiveness of our method, we further evaluate the performance of approaches that integrate LSH to process keywords within a common ABKS scheme [10]. We first assess accuracy under three typical types of spelling errors: letter addition, letter omission, and letter substitution. Accuracy is defined as the ratio of correctly matched keywords to the total number of keywords. A match is considered correct when the hash-bucket string of a misspelled keyword is identical to that of its correctly spelled counterpart. As shown in Fig.10(a), the results indicate that direct keyword matching yields an overall accuracy consistently below 75%. We then evaluate the precision of exact and fuzzy search tasks, as shown in Fig.10(b). For exact search, precision can be improved by increasing the number of LSH functions. However, its fuzzy-search precision stays at least 70% below that of our method, making it impractical for real-world applications. This limitation arises because, after LSH processing in ABKS schemes, keywords are directly transformed into ciphertexts. As a result, they lack the computational structures—such as Bloom filters in traditional fuzzy-search schemes—that support flexible element insertion and correlation-score computation. Furthermore, the search time of the LSH-based ABKS approach is at least 3, 000× longer compared to our method.

![](images/d4f7eecdec066e323e07bece32afa9700c52eea2c447ae30ff3dfd72c71fb879.jpg)



(a) Exact search

![](images/55a0a01d1720698053b6aa926bb5d800ee85cdf673d52169c067f2ab40d5c280.jpg)  
(b) Fuzzy search

![](images/f32e0f099eebd0194527e86d3de9938658607cbf318e5278f2098dbe4ab8234d.jpg)



(c) Exact search

![](images/94856ea328cfb89c6a04afb5f6035bf8f951e9c6bea3114d33867b77d7edcf5a.jpg)



(d) Fuzzy search

Fig. 9. Comparison of the precision between ESA, VRMFS, PIPE, and MFS, set N = 3000. (a) and (b): Precision for exact search and fuzzy search under different k with fixed α = 0. (c) and (d): Precision for exact search and fuzzy search under different attribute numbers α with $k = 2 , k = 4 , \overset { \cdot } { k } = 6 .$ .   
![](images/e37239934170f8e0a63d1d785fae27c72de018aa3abe509db7c77f53936bceae.jpg)



(a) Precision of keyword matching

![](images/a6d6cd812e3901cd69fbcf34a4e4d6af33f62d88eee5400ab2011c0fbfa94394.jpg)



(b) Precision of files search

Fig. 10. Precision for Varying LSH Numbers in LSH-based ABKS schemes.   
![](images/b417ab3adadc9a76d30253080e0a186558deed09c616edfa66aada8d3061700f.jpg)  
Index (Medshare)  Search (Medshare) Index (ESA) Search (ESA)   
Medshare  Search (Medshare) ESA Search (ESA)

Fig. 11. Evaluation of the on-chain performance.

# 0.2 E. Evaluation of On-chain Performance

1000 2000 4000 6000 8000 To assess the feasibility of ESA, we evaluate its on-chain performance and compare it to Medshare [5]. Specifically, we measure gas consumption, storage overhead, and search performance by implementing the smart contract on Ethereum. Consistent with the settings in Medshare, we set the gas price to 1 Gwei. Assuming an exchange rate of 1 Ether = \$200, deploying our smart contract incurs a cost of approximately \$0.18, whereas Medshare requires about \$0.74. As shown in Fig.11(a), the gas cost for posting indexes and performing searches with ESA is lower than that of Medshare. Moreover, the gas cost for search operations remains nearly constant in ESA, contributing to a user-friendly experience. Additionally, ESA outperforms Medshare in both storage overhead and search performance. As shown in Fig.11(b), the storage overhead of ESA is approximately one-third that of Medshare, while the search time for Medshare is about 30× longer than that of ESA. Furthermore, the search time for both schemes is unaffected by the number of indexes, as the time complexity of key-value pair matching is O(1). Since the non-repudiation extension in ESA is realized through smartcontract execution, the resulting overhead is determined by the main contract operations, such as index posting and on-chain search. Therefore, the gas usage, storage overhead, and onchain search latency evaluated in this section characterize the cost and efficiency of integrating non-repudiation into ESA.

![](images/fb3007d3540c4fbfd4626f75bb922ebd6a35024d510837d8179e2b645f036c5a.jpg)



(a)

![](images/68a98184a0cf6eb75e19a9366b551fa684bab82559b03937f0234d8885e9f476.jpg)



(b)

![](images/34f361071d96c31bf310642a42a29991f69f1662740ecf16cd4c94887020e820.jpg)



(c)   
Fig. 12. Parameter sensitivity of ESA about (a) the Prime Filter dimension n, (b) the prime-sequence length |p|, and (c) the number of LSH l.

# F. Parameter Sensitivity Analysis

We evaluate the parameter sensitivity of ESA to the Prime 0 Filter dimension n, the prime-sequence lengths |p| and |q|, 5 and the number of LSH functions l, with fixed $N = 2 0 0 0$ and $k = 2 ,$ as shown in Fig.12.

Fig.12(a) shows that increasing n yields only marginal pre-Latecision gains once $n \geq 2 5 1$ , while search time grows steadily arcdue to the longer vectors. Thus, $n = 2 5 1$ provides a good Sprecision–efficiency balance. Fig.12(b) shows that varying |p| has minimal impact on both precision and time. Since |p| and |q| play similar roles in determining the Prime Filter’s primeslot structure, this stability also applies to reasonable choices of |q|. Our defaults $| p | = 4 1$ and $| q | = 2 3$ , therefore keep the index compact while maintaining high precision. Fig.12(c) illustrates a precision–cost tradeoff: as l increases, precision remains at a relatively high level, but search time increases more noticeably. Values between l = 10 and $l = 2 0$ already achieve high precision with moderate overhead. Overall, ESA remains stable across a broad parameter range, validating our default configuration.

# VIII. CONCLUSION

In this paper, we propose ESA, a privacy-preserving datasharing framework designed to enable multi-keyword fuzzy search and fine-grained access control. We introduce Prime Filter, a novel data structure for indexing and querying that leverages a prime number embedding strategy. Building on Prime Filter and an ABE protocol as foundational components, we realize secure, authorized multi-keyword fuzzy search with arbitrary Boolean semantics. Utilizing blockchain technology, we design a divide-and-conquer access control mechanism to filter search results that infringe upon the established access policy. Furthermore, our scheme achieves non-repudiation in data transactions with the assistance of smart contracts. Formal security proofs and extensive experiments demonstrate the security and feasibility of ESA in practical applications.

# REFERENCES

[1] X.-Y. Li, J. Qian, and X. Wang, “Can china lead the development of data trading and sharing markets?” Commun. ACM, vol. 61, no. 11, p. 50–51, 2018.   
[2] B. Chen, T. Xiang, D. He, H. Li, and K. R. Choo, “BPVSE: publicly verifiable searchable encryption for cloud-assisted electronic health records,” IEEE Trans. Inf. Forensics Secur., vol. 18, pp. 3171–3184, 2023.   
[3] X. Tang, C. Guo, K. R. Choo, Y. Liu, and L. Li, “A secure and trustworthy medical record sharing scheme based on searchable encryption and blockchain,” Comput. Networks, vol. 200, p. 108540, 2021.   
[4] Y. Peng, X. Li, K. Gu, J. Chen, S. K. Das, and X. Zhang, “Achieving efficient and privacy-preserving reverse skyline query over single cloud,” IEEE Trans. Knowl. Data Eng., vol. 37, no. 1, pp. 29–44, 2025.   
[5] M. Wang, Y. Guo, C. Zhang, C. Wang, H. Huang, and X. Jia, “Medshare: A privacy-preserving medical data sharing system by using blockchain,” IEEE Trans. Serv. Comput., vol. 16, no. 1, pp. 438–451, 2023.   
[6] K. Zhang, B. Hu, J. Ning, J. Gong, and H. Qian, “Pattern hiding and authorized searchable encryption for data sharing in cloud storage,” IEEE Trans. Knowl. Data Eng., vol. 37, no. 5, pp. 2802–2815, 2025.   
[7] D. Zhang, S. Wang, Q. Zhang, and Y. Zhang, “Attribute based conjunctive keywords search with verifiability and fair payment using blockchain,” IEEE Trans. Serv. Comput., vol. 16, no. 6, pp. 4168–4182, 2023.   
[8] Y. Miao, J. Ma, X. Liu, X. Li, Q. Jiang, and J. Zhang, “Attribute-based keyword search over hierarchical data in cloud computing,” IEEE Trans. Serv. Comput., vol. 13, no. 6, pp. 985–998, 2020.   
[9] X. Xiang and X. Zhao, “Blockchain-assisted searchable attribute-based encryption for e-health systems,” J. Syst. Archit., vol. 124, p. 102417, 2022.   
[10] M. Wang, Y. Miao, Y. Guo, C. Wang, H. Huang, and X. Jia, “Attributebased encrypted search for multi-owner and multi-user model,” in IEEE International Conference on Communications, ICC, 2021, pp. 1–7.   
[11] S. Patranabis and D. Mukhopadhyay, “Forward and backward private conjunctive searchable symmetric encryption,” in 28th Annual Network and Distributed System Security Symposium, NDSS, 2021.   
[12] J. G. Chamani, D. Papadopoulos, M. Karbasforushan, and I. Demertzis, “Dynamic searchable encryption with optimal search in the presence of deletions,” in 31st USENIX Security Symposium, USENIX Security, 2022, pp. 2425–2442.   
[13] P. Mondal, J. G. Chamani, I. Demertzis, and D. Papadopoulos, “I/oefficient dynamic searchable encryption meets forward & backward privacy,” in 33rd USENIX Security Symposium, USENIX Security, 2024.   
[14] H. Dou, Z. Dan, P. Xu, W. Wang, S. Xu, T. Chen, and H. Jin, “Dynamic searchable symmetric encryption with strong security and robustness,” IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 2370–2384, 2024.   
[15] S. Lv, Y. Huang, X. Li, T. Li, L. Guo, X. Chen, and Z. Liu, “LUNA: efficient backward-private dynamic symmetric searchable encryption scheme with secure deletion in encrypted database,” IEEE Trans. Knowl. Data Eng., vol. 37, no. 4, pp. 1961–1974, 2025.   
[16] F. Luo, H. Wang, X. Yan, and J. Wu, “Key-policy attribute-based encryption with switchable attributes for fine-grained access control of encrypted data,” IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 7245– 7258, 2024.   
[17] G. Lu, B. Waters, and D. J. Wu, “Multi-authority registered attributebased encryption,” in Advances in Cryptology - EUROCRYPT 2025 - 44th Annual International Conference on the Theory and Applications of Cryptographic Techniques, vol. 15603. Springer, 2025, pp. 3–33.   
[18] Q. Liu, Y. Peng, Z. Tang, H. Jiang, J. Wu, T. Wang, T. Peng, and G. Wang, “veffchain: Enabling freshness authentication of rich queries over blockchain databases,” IEEE Trans. Knowl. Data Eng., vol. 36, no. 5, pp. 2285–2300, 2024.   
[19] B. Wang, S. Yu, W. Lou, and Y. T. Hou, “Privacy-preserving multikeyword fuzzy search over encrypted data in the cloud,” in IEEE Conference on Computer Communications, INFOCOM, 2014, pp. 2112– 2120.   
[20] Z. Fu, X. Wu, C. Guan, X. Sun, and K. Ren, “Toward efficient multikeyword fuzzy search over encrypted outsourced data with accuracy improvement,” IEEE Trans. Inf. Forensics Secur., vol. 11, no. 12, pp. 2706–2716, 2016.   
[21] J. Chen, K. He, L. Deng, Q. Yuan, R. Du, Y. Xiang, and J. Wu, “Elimfs: Achieving efficient, leakage-resilient, and multi-keyword fuzzy search on encrypted cloud data,” IEEE Trans. Serv. Comput., vol. 13, no. 6, pp. 1072–1085, 2020.

[22] X. Li, Q. Tong, J. Zhao, Y. Miao, S. Ma, J. Weng, J. Ma, and K. R. Choo, “VRFMS: verifiable ranked fuzzy multi-keyword search over encrypted data,” IEEE Trans. Serv. Comput., vol. 16, no. 1, pp. 698–710, 2023.   
[23] Q. Liu, Y. Peng, S. Pei, J. Wu, T. Peng, and G. Wang, “Prime inner product encoding for effective wildcard-based multi-keyword fuzzy search,” IEEE Trans. Serv. Comput., vol. 15, no. 4, pp. 1799–1812, 2022.   
[24] Q. Tong, Y. Miao, J. Weng, X. Liu, K. R. Choo, and R. H. Deng, “Verifiable fuzzy multi-keyword search over encrypted data with adaptive security,” IEEE Trans. Knowl. Data Eng., vol. 35, no. 5, pp. 5386–5399, 2023.   
[25] N. Cui, D. Wang, J. Li, H. Zhu, X. Yang, J. Xu, J. Cui, and H. Zhong, “Enabling efficient, verifiable, and secure conjunctive keyword search in hybrid-storage blockchains,” IEEE Trans. Knowl. Data Eng., vol. 36, no. 6, pp. 2445–2460, 2024.   
[26] R. Guo, B. Qin, Y. Wu, R. Liu, H. Chen, and C. Li, “Luxgeo: Efficient and security-enhanced geometric range queries,” IEEE Trans. Knowl. Data Eng., vol. 35, no. 2, pp. 1775–1790, 2023.   
[27] J. Li, Q. Wang, C. Wang, N. Cao, K. Ren, and W. Lou, “Fuzzy keyword search over encrypted data in cloud computing,” in IEEE Conference on Computer Communications, INFOCOM, 2010, pp. 441–445.   
[28] H. Yin, Y. Li, H. Deng, W. Zhang, Z. Qin, and K. Li, “Practical and dynamic attribute-based keyword search supporting numeric comparisons over encrypted cloud data,” IEEE Trans. Serv. Comput., vol. 16, no. 4, pp. 2855–2867, 2023.   
[29] C. Fan, S. Wu, Y. Tseng, and A. Karati, “Attribute-based encryption supporting multi-keyword search with effective user revocation in public cloud storage,” IEEE Trans. Dependable Secur. Comput., vol. 22, no. 6, pp. 7790–7801, 2025.   
[30] K. He, J. Guo, J. Weng, J. Weng, J. K. Liu, and X. Yi, “Attribute-based hybrid boolean keyword search over outsourced encrypted data,” IEEE Trans. Dependable Secur. Comput., vol. 17, no. 6, pp. 1207–1217, 2020.   
[31] S. Hu, C. Cai, Q. Wang, C. Wang, X. Luo, and K. Ren, “Searching an encrypted cloud meets blockchain: A decentralized, reliable and fair realization,” in IEEE Conference on Computer Communications, INFOCOM, 2018, pp. 792–800.   
[32] Z. Chen, Q. Li, X. Qi, Z. Zhang, C. Jin, and A. Zhou, “Blockope: Efficient order-preserving encryption for permissioned blockchain,” in 38th IEEE International Conference on Data Engineering, ICDE, 2022, pp. 1245–1258.   
[33] Y. Guo, C. Zhang, C. Wang, and X. Jia, “Towards public verifiable and forward-privacy encrypted search by using blockchain,” IEEE Trans. Dependable Secur. Comput., vol. 20, no. 3, pp. 2111–2126, 2023.   
[34] J. G. Chamani, Y. Wang, D. Papadopoulos, M. Zhang, and R. Jalili, “Multi-user dynamic searchable symmetric encryption with corrupted participants,” IEEE Trans. Dependable Secur. Comput., vol. 20, no. 1, pp. 114–130, 2023.   
[35] P. Sun, L. Zhang, J. Liu, C. Tang, and J. Wang, “Eˆ 3fs: Efficient, secure, and verifiable fuzzy search with data updates in hybrid-storage blockchains,” in 41th IEEE International Conference on Data Engineering, ICDE, 2025, pp. 3890–3903.   
[36] C. Li, Y. Cao, Z. Hu, and M. Yoshikawa, “Blockchain-based bidirectional updates on fine-grained medical data,” in 35th IEEE International Conference on Data Engineering Workshops, ICDEW, 2019, pp. 22–27.   
[37] W. K. Wong, D. W. Cheung, B. Kao, and N. Mamoulis, “Secure knn computation on encrypted databases,” in Proceedings of the ACM SIGMOD International Conference on Management of Data, 2009, pp. 139–152.   
[38] J. Qian, Z. Huang, Q. Zhu, and H. Chen, “Hamming metric multigranularity locality-sensitive bloom filter,” IEEE/ACM Trans. Netw., vol. 26, no. 4, pp. 1660–1673, 2018.   
[39] Y. Zhang, D. Zheng, X. Chen, J. Li, and H. Li, “Computationally efficient ciphertext-policy attribute-based encryption with constant-size ciphertexts,” in Provable Security - 8th International Conference, ProvSec, vol. 8782, 2014, pp. 259–273.   
[40] Q. Tong, Y. Miao, J. Weng, X. Liu, K. R. Choo, and R. H. Deng, “Verifiable fuzzy multi-keyword search over encrypted data with adaptive security,” IEEE Trans. Knowl. Data Eng., vol. 35, no. 5, pp. 5386–5399, 2023.   
[41] B. Yao, F. Li, and X. Xiao, “Secure nearest neighbor revisited,” in 29th IEEE International Conference on Data Engineering, ICDE, 2013, pp. 733–744.   
[42] S. Chen, Z. Ju, X. Dong, H. Fang, S. Wang, Y. Yang, J. Zeng, R. Zhang, R. Zhang, M. Zhou, P. Zhu, and P. Xie, “Meddialog: A large-scale medical dialogue dataset,” CoRR, vol. abs/2004.03329, 2020.

![](images/362c6da63d91fa898e468177c19fc14a10b930af37bb8fc984d485c4a5000143.jpg)



Pengcheng Sun received the BS degree in mathematics and applied mathematics from Harbin Engineering University, China, in 2022. He is currently working toward the PhD degree in computer science and technology with the University of Science and Technology of China. His research interests include security and privacy issues in cloud computing, blockchain, and AI models.

![](images/b6d5c0ece562aa3ad0e12e04f1497118accf0dfcaf82d2f54fb03bcab7095e5f.jpg)



Yunhao Wang received the BS degree in mathematics from Wuhan University, China, in 1997. He is currently a researcher at Lenovo Research. His research interests include security and privacy of large language models.

![](images/ddd12cc96746b92d04102846699e80a107f04fa728dd83d7492203fc1cbe3275.jpg)



Lan Zhang received the bachelor’s degree from the School of Software, Tsinghua University, China, in 2007, and the PhD degree from the Department of Computer Science and Technology, Tsinghua University, China, in 2014. She is currently a professor with the School of Computer Science and Technology, University of Science and Technology of China. Her research interests include AIoT, agent network, and privacy protection.

![](images/0750c212a2e1cb9d876e039456e0a9c96c56b0a1a03e6f3010467deeb016c752.jpg)



Hui Jin received the MS degree from Harbin Engineering University, China, in 2012. She is currently a researcher at Lenovo Research. Her research interests include security and privacy of large language models.

![](images/d7dad33aad7e26c8040a28270113afc90b1817be3e8bef2dbf12ccbe01a5ff45.jpg)



Xinming Wang received the bachelor’s degree from Harbin Institute of Technology, China, in 2021, and the Master’s degree in computer technology from the University of Science and Technology of China, in 2025. He is currently with Tencent. His research interests include digital fingerprinting and blockchain applications.

![](images/edef12717cf96d9123d76c1f635a6d054ebaa5ab5ccfe086908e6b6793580d80.jpg)



Chen Tang received the BS degree in mathematics and applied mathematics from XiDian University, China, in 2020. He is currently working toward the PhD degree in computer technology with the University of Science and Technology of China. His research interests include model copyright protection, model fingerprinting, and model watermarking.

![](images/75a8065d482438651a2a3c445db0b04d185229872ca4fb691740fc4a2f164fde.jpg)



Yihan Wang received the BE degree in computer science and technology from Sichuan University, China, in 2020. She is currently working toward the PhD degree in computer technology with the University of Science and Technology of China. Her research interests include knowledge quality and data access control.

![](images/6b809057d219bccf80af4dbf90f852ddbad1a42bbca149b0a34649c817d63127.jpg)



Zhonghao Hu is currently a researcher at the China Academy of Information and Communications Technology (CAICT), affiliated with the Key Laboratory of Internet and Industrial Integration and Innovation, MIIT. His research interests include industrial internet, edge computing, and industrial control systems.