# E3FS: Efficient, Secure, and Verifiable Fuzzy Search with Data Updates in Hybrid-Storage Blockchains

Pengcheng Sun∗, Lan Zhang∗† , Jiandong Liu∗, Chen Tang∗, Jialiang Wang∗

∗ University of Science and Technology of China, Hefei, China

† Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, China

{special0806,jdliu,chentang1999,wjl937672039}@mail.ustc.edu.cn, zhanglan@ustc.edu.cn

Abstract—The hybrid-storage blockchain (HSB) facilitates flexible data sharing and search applications across decentralized clients. However, ensuring data privacy and result integrity, while enhancing query and result verification efficiency in HSBbased search applications over dynamic datasets, poses significant challenges. In this paper, we propose E3FS, the first efficient, secure, and verifiable search scheme over dynamically updatable datasets in HSB systems, supporting multi-keyword fuzzy search, an important search function. E3FS accelerates search and verification through an updatable hybrid index with an efficient on-chain process. This design integrates encrypted LSH-based Bloom filters for maintaining file keyword information and an inverted index linking each keyword to a novel authenticated index tree spanning multiple files. Lightweight digests of these trees are stored on-chain to assist with verification, achieving sublinear search and verification costs. Moreover, the framework guarantees forward privacy by securely updating and refreshing both on-chain and off-chain index with new secrets upon each data update. Experimental results demonstrate that our solution outperforms state-of-the-art methods, achieving at least 58.6× faster search and 34.4× faster verification while reducing communication overhead by approximately 60×.

# I. INTRODUCTION

Blockchain, as a tamper-resistant ledger technology, has been widely adopted in distributed applications such as healthcare, IoT and supply chain management for trustworthy data management [1]–[6]. To handle large-scale data, many services employed hybrid storage blockchain (HSB) systems that integrate on-chain and off-chain storage, thereby enhancing scalability and improving data search efficiency [7]–[10]. As an important search mechanism, fuzzy keyword search plays a crucial role in HSB systems. For instance, healthcare centers leverage HSB to dynamically share electronic medical records for diagnosis and drug development while maintaining authoritative verifiable records [10]–[12]. In such scenarios, when doctors and researchers are uncertain about the exact spelling of medical terms, fuzzy keyword search enables users to obtain results as accurately as possible despite entering minor spelling errors or approximate keywords. However, offchain servers in HSB systems cannot always be fully trusted in such privacy-sensitive applications. Hence, ensuring data security and query result integrity is essential, making privacy protection and result verification critical challenges.

![](images/cd1282632a55d218f16c25d8ba238e57066de8827783f2a5ce8bc48f48b84d54.jpg)



Fig. 1: Verifiable Queries in Hybrid Storage Blockchain.

Non-private blockchain-aided verifiable keyword search in dynamic databases has been widely explored, encompassing functionalities such as multi-keyword search and fuzzy search [13]–[19]. Recently, some studies have observed potential threats to result correctness and privacy protection in these methods. One category of research has developed verifiable fuzzy search schemes for HSB using verification techniques, such as cryptographic accumulators and Merkle Hash Trees (MHT) [13]. Another category of research focuses on secure and verifiable search functionalities for simple queries (e.g., exact single-keyword or multi-keyword searches) utilizing primitives such as homomorphic encryption and searchable encryption (SE) [8]–[10]. However, existing solutions can not simultaneously achieve verifiability and privacy preservation for complex multi-keyword fuzzy search in HSB systems.

This paper employs a typical HSB architecture for search applications [13]–[19]. As shown in Fig. 1, the data owner outsources the data and Authenticated Data Structure (ADS) constructed from the data to an off-chain service provider (SP) while sending the corresponding digests of ADS on-chain. To ensure the integrity of search results, the SP generates proofs, i.e., Verification Objects (VO), which users can use to validate the search results against the on-chain digests.

In this paper, we take the first steps toward achieving efficient, secure, and verifiable multi-keyword fuzzy search with data updates in HSB. The first challenge lies in the limited on-chain and user-side resources for verification. Traditional secure and verifiable fuzzy search schemes and data structures are designed for off-chain cloud environments, assuming either computationally powerful clients [20], [21] or trusted server assistance [22]. However, extending these techniques to HSB systems poses significant challenges. These techniques often require a linear scan of files and generate numerous proofs to be verified, resulting in substantial on-chain storage and verification overhead—especially problematic for blockchains and users in HSB systems with limited storage and computational resources. Another challenge is privacy risks during data updates. Existing secure and verifiable fuzzy search techniques are typically designed for static databases [20]–[22], making them unsuitable for dynamic HSB systems. When adding or deleting files using these techniques, untrusted servers can infer update information for specific keywords by repeatedly querying the dataset with historical query tokens and VOs after each update, leading to a forward privacy risk [8], [10].

To balance on-chain and off-chain overheads, we propose a novel hybrid index that offloads computationally intensive tasks to the off-chain server, while storing only metadata onchain to assist with verification. It reduces the search and verification costs from linear [20], [22] to sublinear relative to dataset size and avoids on-chain computations. Specifically, the hybrid index is partitioned into three interrelated components to accelerate search and verification processing. To alleviate the verification burden on both the blockchain and users, we construct an inverted authenticated index tree for each keyword on top of encrypted Bloom filters while storing only lightweight digests associated with these index trees on-chain. Multi-keyword fuzzy search can be efficiently performed on a reduced file space based on the least frequent keyword in the query, allowing off-chain untrusted servers to generate far fewer VOs to be verified, thereby reducing the verification overhead for both users and the blockchain.

To mitigate privacy risks during updates, we proposed a dynamic secure and verifiable fuzzy search protocol with forward privacy guarantee. The protocol prevents servers with access to historical query tokens and VOs from linking updated indexes, which is achieved by refreshing the hybrid index using a secret counter. The hybrid index is tailored for dynamic HSB and is an optimized, updatable version of existing structures. Each updated index forms a hidden, chain-like connection to the previous index, which is accessible only through newly generated user tokens, thereby ensuring forward privacy.

To comprehensively address the efficiency and security challenges, we propose ${ \mathrm { E } } ^ { 3 } { \mathrm { F } } { \mathrm { S } } .$ , an Efficient, sEcure, and vErifiable Fuzzy Search scheme over dynamic data in HSB systems. To summarize, our contributions are as follows:

• To the best of our knowledge, this is the first study to achieve efficient, secure, and verifiable fuzzy search on encrypted dynamic data in hybrid storage blockchain.   
• We propose a novel hybrid index structure and a secure, verifiable fuzzy search scheme $\mathrm { E ^ { 3 } F S }$ , offering the following advantages over state-of-the-art works: (1) It reduces the cost of verifiable fuzzy search from linear [20], [22] to sublinear relative to the dataset size. (2) It enables secure dynamic updates with forward privacy guarantees.   
• We conduct extensive evaluations on a real-world dataset [23]. Concretely, we compare E3FS with stateof-the-art schemes [21], [22] under equivalent parameters in terms of time and communication costs. The results demonstrate significant performance advantages for $\mathrm { E ^ { 3 } F S }$ . Specifically, search and verification speeds

are at least 58.6× and 34.4× faster, respectively. The communication cost for verification remains under 20KB, outperforming other schemes by approximately 60×.

# II. RELATED WORK

# A. Fuzzy Keyword Search Processing over Encrypted Data

Extensive research has developed secure fuzzy keyword search protocols in outsourced databases [24]–[33]. These methods generally fall into two categories: wildcard edit distance comparisons [24]–[29] and Locality-Sensitive Hashing (LSH) with Bloom filters [30]–[32]. While wildcard-based methods enable efficient single-keyword fuzzy search, they often incur high computational costs due to the need for a predefined dictionary. LSH-based methods, on the other hand, are tailored for multi-keyword searches. These schemes achieve multi-keyword fuzzy search without a predefined dictionary, though with some loss in accuracy [30]–[32]. However, these methods mainly address semi-honest servers and do not support result verification. Recent studies have made notable progress. Some works [20]–[22], [34] achieved secure and verifiable fuzzy search in static databases. However, they are not suitable for dynamic HSB with data updates.

# B. Verifiable Search Processing over Blockchain

Verifiable search mechanisms in blockchain systems are utilized to validate results provided by untrusted full nodes or service providers within HSB systems. Recent advancements have primarily focused on the design of ADS, with MHT and cryptographic accumulators as commonly used tools. To against malicious full nodes, significant efforts have been made to enhance non-private verifiable search capabilities, supporting various query types such as Boolean search [14]–[17], range search [7], [15]–[17], [35], [36], and fuzzy search [13]. To enhance data privacy, several studies [37]–[39] have used SE to construct encrypted indexes on-chain, enabling searches via trusted smart contracts. However, the high storage and computation demands significantly burden the blockchain. Recent research has focused on secure and verifiable search in HSB, but the range of supported search types remains limited compared to non-private protocols. For example, some studies [8]–[10], [40] have achieved secure and verifiable dynamic single-keyword and conjunctive keyword searches with forward privacy guarantees. Despite significant advancements, current protocols lack a dynamic, secure, and efficient solution for verifiable fuzzy multi-keyword searches in HSB systems.

# III. PRELIMINARIES

# A. Multi-Keyword Fuzzy Search Over Encrypted Data (MFSE)

MFSE is a widely used and effective method for secure multi-keyword fuzzy search [30]–[32]. It consists of the following key components:

• Keyword Transformation: Each keyword is converted into a vector using keyword representations like unigram [31]. For example, the keyword “secure” is represented as the unigram set {s1, e1, c1, u1, r1, e2}, where s1 and $\mathrm { e } 2$ indicate the first $\cdot _ { \mathrm { { s } } } ,$ and second $\cdot _ { \mathrm { e } } ,$ in the word, respectively. Each unigram occupies a specific position in the vector, with its corresponding element set to 1.

• LSH and Bloom-Filter-based Index/Query: MFSE employs LSH functions [41] to generate the index/query vector by hashing keyword vectors in each file/query into an m-bit Bloom filter. LSH maps similar items to the same bucket with high probability, enabling fuzzy matching even in the presence of misspellings. In our scheme, we adopt the commonly used p-stable LSH [42].   
• Trapdoor-based keyword search: Each index and query Bloom filter is encrypted using ASPE [43], and keyword search is performed by computing the inner product between the encrypted index and encrypted query Bloom filters (serving as trapdoors for retrieval), which determines the relevance score between a file and a query.

# B. Asymmetric Scalar-Product-Preserving Encryption (ASPE)

ASPE [43] allows the computation of the same inner product for encrypted vectors as would be obtained in the plaintext domain. It can be used to identify the relationship between the encrypted index and the trapdoor corresponding to a query. The secret key is defined as $S K = \{ M _ { 1 } , M _ { 2 } , S \}$ , where $M _ { 1 } , M _ { 2 } \in \mathbb { R } ^ { d \times d }$ are two invertible matrices, and $S \in \{ 0 , 1 \} ^ { d }$ is a splitting vector. The functionalities of ASPE are as follows:

• IndexGen(I, SK). It takes as input the secret key SK and d-dimensional index vector I, and outputs the encrypted index EncSK(I).   
• TrapGen(Q, SK). It takes as input the secret key SK and d-dimensional query vector Q, and outputs the trapdoor $E n c _ { S K } ( \mathcal { Q } )$ .   
• Search $( C _ { \mathbb { Z } } , C _ { \mathbb { Q } } )$ . It takes as input the encrypted index $C _ { \mathcal { I } }$ and the trapdoor $C _ { \mathcal { Q } }$ , and outputs the inner product R of $C _ { \mathcal { I } }$ and $C _ { \mathcal { Q } }$ as the search result.

# C. Homomorphic MAC (HMAC)

HMAC is a homomorphic verification technique that allows the verification of data correctness through algebraic operations on the data. In this paper, we adopt the homomorphic MAC for real numbers, denoted as HMAC [20], which consists of four algorithms described as follows:

• KeyGen(λ). It takes a security parameter λ as input and outputs a key-based pseudo-random function (PRF) $F _ { k }$ : $\{ 0 , 1 \} ^ { * } \to { \mathbb { R } } _ { \lambda }$ and a random number α. The secret key is defined as s $k = \{ k , \alpha \}$ .   
• $\mathsf { A u t h } ( s k , L , m )$ . It takes as inputs the secret key sk, a message m $\in \mathbb { R } _ { \lambda }$ , and a label $L \in \{ 0 , 1 \} ^ { * }$ associated with m. It outputs an authentication object o for m.   
• $\mathsf { E v a l } ( \vec { o } _ { \mathbb { Z } } , \vec { o } _ { \mathbb { Q } } )$ . It takes as inputs two authentication vectors, $\vec { o } _ { \mathcal { T } }$ and $\vec { o } _ { \Omega }$ , corresponding to the index and query, respectively. It outputs a tag σ, which is the evaluation of an arithmetic circuit f on $( \vec { o } _ { \mathbb { Z } } , \vec { o } _ { \Omega } )$ .   
• $\mathsf { V e r } ( s k , \vec { L } , m , \sigma )$ . It takes as input the secret key $s k ,$ , the labeled program $\vec { L } = ( f , L _ { \mathcal { T } } , L _ { \mathcal { Q } } )$ , the computation result m, and the tag σ. It outputs either True or False, indicating whether m is the correct result of the computation.

![](images/5240e52fc492a109cb3a72735b2fe7ffd1a2ec3b504bc717450c5455e8ec9a5b.jpg)



Fig. 2: System Model of E3FS   
IV. PROBLEM FORMULATION

In this section, we present the problem formulation of secure verifiable fuzzy search over dynamic encrypted data in HSB.

# A. System Model and Workflow

As illustrated in Fig. 2, this paper considers a system model based on a hybrid storage blockchain, involving four entities: the Data Owner (DO), the Data User (DU), the off-chain Service Provider (SP), and the Blockchain (BC).

• Data Owner. The DO owns the raw data and constructs secure indexes and ADS for verifiable keyword search. It then outsources the encrypted database, secure indexes, and ADS to the SP (Step 1). A small digest of the ADS is uploaded to the BC for record-keeping (Step 2). When new data needs to be updated, the DO sends the updated information to both the SP and the BC (Step 3).   
• Data User. The DU is the entity that requests data search services. It initiates either a fuzzy or exact keyword search from the SP and generates the trapdoor with assistance from the DO, which is then sent to the SP (Steps 4–5). Upon receiving the search result and the VO from the SP, the DU can verify the result by combining the digest from the BC with the VO (Steps 6–8).   
• Service Provider. The SP, with ample computational and storage resources, offers storage and search services. Due to trust concerns, upon receiving a query, the SP performs the search computations and constructs the corresponding VO to ensure result verifiability. Finally, the SP sends both the search result and VO to the DU (Step 6).   
• Blockchain. The BC stores the digest of ADS (Step 2). Due to its immutability, all records on-chain are considered trustworthy. During data updates, the BC receives the updated information from the DO and updates the digest accordingly (Step 3). For each query, the BC provides the corresponding digest to the DU for verification (Step 8).

# B. Threat Model

In our system, three participants—DO, DU, and SP—and a blockchain platform BC are involved. DO and DU are assumed to be honest, faithfully executing protocols and safeguarding data privacy. The BC is treated as a trusted, tamper-resistant storage platform, whereas the SP is potentially malicious, which may attempt to 1) infer private information from encrypted data and queries or 2) return fabricated or incomplete results when providing service. Besides, the communication channels are assumed secure. This threat model is suitable for scenarios where DO and DU share a database, outsourced to a powerful SP for search services, with BC used for maintaining immutable records [7], [8], [13], [18].

To ensure data privacy and result integrity, this paper aims to ensure that, throughout the search process, the SP learns nothing other than some non-private information typically permitted in secure search applications [30]–[32], and the correctness and completeness of its returned results are verifiable. Regarding the information to protect, we follow the widely adopted known background model (KBM) [30]– [32] in secure search applications to ensure data and query privacy. In this model, all dataset and query information must remain concealed from the SP, except for certain background information, including: (i) size pattern: database size during setup and update; (ii) query pattern: whether a query has been executed previously; (iii) access pattern: whether specific file identifiers match the query; (iv) update pattern: whether updates exist for the keywords in the query. Moreover, recent literature [44], [45] has pointed out a forward privacy threat, where background information may expose file-keyword associations after file additions or deletions, making it vulnerable to file-injection attacks. Thus, our scheme must protect such information following data updates, ensuring compliance with the forward privacy properties [44]. Regarding the result correctness and completeness verification, the DU with VO generated by the SP must be able to verify that 1) the returned results R satisfy the query and haven’t been tampered with, and 2) no files that satisfy the query are omitted.

We proceed to formulate the privacy and verifiability properties of our scheme. First, we define the following notions related to information during a protocol run:

• History: All plaintext data processed in the system, including the dataset D, keyword set W, historical queries Q, and historical updates U .   
• View: All data and messages acquired by the SP during its interaction with the DO and DU.   
• Trace: The background information the SP is permitted to infer, i.e., size pattern, query pattern, access pattern, and update pattern.

Based on these notions, we define the data and query privacy (under the KBM model), forward privacy, and correctness and completeness verifiability in Definitions 1-3.

Definition 1. (KBM-Security) Consider a query request sequence with a line of keyword-trapdoor pairs. A scheme π is KBM-secure if, for any probabilistic polynomial-time (PPT) adversary A, the distinguishing probability between the SP’s View V in π and the simulated View V′ generated by a simulator S taking the Trace as input, is negligible.

Definition 2. (Forward Privacy) Given a dataset D and an update request (add/delete) for a file with identifier id containing keyword w. Let T be the Trace obtained by the SP during such update, and let T ′ be the Trace generated by a simulator S given the input (|D|, ut, id), where ut ∈ {add, delete}. A scheme π is forward private if any PPT adversary A can distinguish T from T ′ only with negligible probability.

Definition 3. (Correctness and Completeness Verifiability) Given a dataset D, a query verification algorithm is successful if, for any PPT adversary A, the probability that A produces a query Q, a search result R, and a verification object VO that pass verification is negligible. Specifically, A succeeds if VO passes verification and one of the following holds: 1) R contains a file d∗ ∈ D/ or d∗ does not satisfy Q; 2) R does not contain a file $d ^ { \ast } \in \mathcal { D }$ that satisfies Q.

Further privacy concerns and potential protections: This paper mainly focuses on data and query privacy under the KBM model, as well as forward privacy. However, recent works pointed out that forward privacy may not be sufficient in scenarios where the query and access pattern leaks information [45]. To mitigate this concern, techniques such as Oblivious RAM [46] could be used to ensure that each query and access request reveals no content.

# C. Problem Statement

Based on the aforementioned system and threat model, this paper focuses on designing secure protocols and ADS to effectively support secure dynamic multi-keyword fuzzy search with forward privacy guarantees. DUs can efficiently perform searches within the HSB system and verify the correctness and completeness of the returned query results.

# V. EFFICIENT SECURE HYBRID INDEX

In this section, we design a novel hybrid index to facilitate efficient and secure fuzzy search in dynamic HSB, while ensuring the verifiability of search results. Our index stores the keyword information of outsourced files using a hybrid index collaboratively maintained by participants. By arranging the link between keywords and files efficiently via LSH-based Bloom filters and inverted index trees, our hybrid index allows participants to efficiently retrieve files using multiple keywords in both exact and fuzzy forms. The search complexity is linear to the number of files associated with the least frequent keyword in the query. Leveraging cryptographic primitives such as ASPE and PRF, all operations on our hybrid index maintain strict data security and forward privacy. Additionally, we authenticate the index using HMAC and hash functions, securely maintaining computation proofs to ensure verification. Furthermore, we extend the index structure to efficiently handle databases with skewed keyword distributions.

The hybrid index is constructed by DO and collaboratively stored by participants—BC, SP, and DO to enable verifiable fuzzy search while fully utilizing storage and computational capacities. As illustrated in Fig. 3, they are 1) T-MAP, stored in the SP with abundant resources, which is a collection of authenticated balanced binary trees (A-BBT) that encompass the forward and inverted indexes between keywords and files; 2) O-MAP, stored in the resource-constrained DO, which is a lightweight dictionary used to store information for secure updates; and 3) B-MAP, stored in the resource-constrained

![](images/d443f0017ac4c003ae4c3e6ac4d1a667edbf4c2c494bb6ce71e810ae32ebd87e.jpg)



Fig. 3: Example of the hybrid index for keyword w.

BC, which is a lightweight dictionary used to securely store the digests of ADS for further verification.

# A. Hybrid Index Data Structure

T-MAP Structure. The T-MAP is the core structure of the hybrid index, stored at the SP to perform computations such as search and VO generation. It facilitates efficient search and verification by compressing the search space. At a high level, T-MAP consists of two main components: a forward index collection containing encrypted keyword information of outsourced files and an inverted index that efficiently and securely organizes the forward index collections. The forward index payload for each outsourced file is a Bloom filter encrypted with ASPE, populated with keywords. To achieve efficient search and verification, we utilize a commonly employed inverted index on top of the forward index payloads for all files. In the inverted index, the identifier and forward index of each file are linked to several keywords included in the file. This linkage is constructed using newly designed secure and authenticated balanced binary trees (A-BBT), where each A-BBT is associated with a keyword w and is denoted as $\mathcal { T } _ { w }$ . Besides, each keyword is associated with a counter that increments with the file update to ensure forward privacy. The structure is defined as follows.

Definition 4. (T-MAP) The T-MAP is a dictionary where the key is an encrypted token of a keyword w, and the value is an A-BBT that stores information about files containing w. The encrypted token is defined as $f _ { k _ { 2 } } ( \sigma _ { w } \| \alpha )$ , where $k _ { 2 }$ is a PRF key, $\sigma _ { w }$ is the LSH value of w, and α is the update counter for w. The fields of a node n in A-BBT are defined as follows:

• id: Encrypted file identifier, which appears in leaf nodes.   
• $\pi _ { i d } \colon$ The hash of $F _ { i d } ,$ which appears in leaf nodes.   
• EBF : ASPE.Index $\mathsf { G e n } ( \mathbb { Z } _ { i d } )$ , where $\mathcal { T } _ { i d }$ is the forward index of the file $F _ { i d }$ with keywords inserted.   
• ABF : HMAC.Auth(EBF ), which is the authentication tag of the encrypted index EBF .   
• H : $h ( i d \| \pi _ { i d } \| E B F \| A B F \| H _ { l } \| H _ { r } )$ , where $H _ { l }$ and $H _ { r }$ are the hash values of the left and right child nodes of n, respectively. For a non-leaf node, $H \_ =$ $\begin{array} { r } { h ( E B F \| A B F \| H _ { l } \| H _ { r } ) } \end{array}$ .

Alg. 1 shows the detailed construction process of an A-BBT for the keyword $w ,$ which can be divided into three main steps:

• Forward Index Construction: To construct the forward index, for each file $F _ { i }$ containing the keyword $w ,$ the DO first converts each keyword in $F _ { i }$ into a uni-gram

Algorithm 1: Construction of A-BBT   
Input: The file and identity set (D(w), ID(w)) for keyword w, security parameter m, ASPE key sk1, HMAC key sk2, PRF keys {k1, {k'i}ℓ i=1}, and LSH family H = {ha_i,b_i}ℓ i=1.

1 B ← FuzzyMapping(D(w), H, {k'i}ℓ i=1);
2 tag ← empty queue;
3 node ← A-BBT(ID(w), B, sk1, sk2, k1)
4 Function A-BBT(ID(w), B, sk1, sk2, k1):
5    if |ID(w)| = 1 then
6    node.id ← f_k1(ID(w)[0]), node.π ← h(F_id);
7    node.EBF ← ASPE.IndexGen(B_i, sk1);
8    node.ABF ← HMAC.Auth(sk2, Li, EBF);
9    node.H ← h(id||π||EBF||ABF||H⊥||H⊥);
10    Put f_k1(Li) into tag;
11    else
12    ID(w)_ℓ ← randomly select [|B|/2] B
13    ID(w)_r = ID(w) - ID(w)_ℓ;
14    lchild ← A-BBT(ID(w)_ℓ, {B}_ℓ, sk1, sk2, k1);
15    rchild ← A-BBT(ID(w)_r, {B}_r, sk1, sk2, k1);
16    node.left = lchild, node.right = rchild;
17    for j = 1 to m do
18    B_i[j] = max(lchild.B[j], rchild.B[j]);
19    node.EBF ← ASPE.IndexGen(B_i, sk1);
20    node.ABF ← HMAC.Auth(sk2, Li, EBF);
21    node.H ← h(id||π||EBF||ABF||H_l||H_r);
22    Put f_k1(Li) into tag;
23    return node;

24 Function FuzzyMapping (D(w), H, {k'i}ℓ i=1, m):
25    G ← {g_i | g_i = f_k_i' · h_a_i,b_i, 1 ≤ i ≤ l}, B ← empty set;
26    for each file F_i in D(w) do
27    Initialize an m-bit zero Bloom filter B_i;
28    for each keyword w_j in F_i do
29    Transforms w_j into a uni-gram vector v_j;
30    Insert v_j into B_i using G;
31    Put B_i into B;
32    return B;

vector [31]. These vectors are then inserted into an mdimensional Bloom filter $B _ { i }$ using PRF-encrypted LSH, ensuring that both misspelled and correct keywords map to the same bucket. The use of PRF eliminates correlations between different Bloom filters (lines 24–32). Next, the DO applies ASPE.IndexGen to encrypt these Bloom filters, producing a 2m-dimensional encrypted vector, which is the forward index EBF for $F _ { i }$ (lines 7, 19).

• Inverted Index Construction: To construct the inverted index that maps the keyword w to the files containing it, the DO builds a balanced binary index tree using the $E B F s$ of these files as the leaf nodes. Each non-leaf node in the index tree contains a 2m-dimensional encrypted vector, representing the union of the keywords contained in the $E B F s$ of its child nodes. For instance, if $B _ { l }$ and $B _ { r }$ are the Bloom filters of the left and right child nodes of a non-leaf node $n ,$ , the union is computed as: $B _ { n } [ j ] =$ max $( B _ { l } [ j ] , B _ { r } [ j ] ) , 0 \ \le \ j \ \le \ m$ . The encrypted vector for the non-leaf node is then computed as: $E B F _ { n } ~ =$ $\mathsf { A S P E . l n d e x G e n } ( B _ { n } , s k _ { 1 } )$ . (lines 16–19)   
• Authentication: To enable the DU to identify tampered or incomplete results, the A-BBT is authenticated before outsourcing (lines 8, 20). For each node n in the A-BBT, the DO runs HMAC.Auth to generate an authentication

object $A B F _ { n }$ and store the label $L _ { n }$ of $E B F _ { n }$ in the tag. The $A B F _ { n }$ is used to generate the VO for corresponding searches, while the tag is used for result verification.

Based on this structure, regardless of the number of keywords in the query, each target file can be located by first retrieving an infrequent keyword w from the query and then searching the A-BBT associated with w. This process incurs an $O ( | D ( w ) | )$ overhead, where $D ( w )$ denotes the file set containing w. Additionally, by performing a top-down search, subtrees in the A-BBT that do not satisfy the search condition can be pruned, enabling more efficient sublinear time complexity.

O-MAP Structure. The O-MAP is a lightweight dictionary maintained by the DO to track update counts for each keyword. When file updates or trapdoor generation tasks are performed, the DO uses the locally stored O-MAP to update tokens, breaking the correlation between updated indexes and previous trapdoors. The structure is defined as follows:

Definition 5. (O-MAP). The O-MAP is a dictionary where the key is the LSH value of a keyword w, denoted as $\sigma _ { w } ,$ and the value is the update counter for w, denoted as α.

B-MAP Structure. The B-MAP is a lightweight dictionary maintained by the BC to store digests of each keyword’s A-BBT for verification. When the SP sends search results and the VO to the DU, the DU verifies the results using the immutable evidence in the B-MAP. To minimize storage overhead on the BC, only the root hash of each A-BBT and several tags generated by HMAC.Auth for authenticating the A-BBT are stored in the B-MAP. The structure is defined as follows:

Definition 6. (B-MAP). The B-MAP is a dictionary where the key is an encrypted token of a keyword w, identical to the key in T-MAP, and is defined as $f _ { k _ { 2 } } ( \sigma _ { w } \| \alpha )$ . The value is defined as $h ( r o o t _ { T _ { w , \alpha } } ) \| t a g _ { \mathbf { \alpha } }$ , where $h ( r o o t _ { T _ { w , \alpha } } )$ is the hash of the root of the A-BBT for w and α, and tag represents the authentication tags for $\mathcal { T } _ { w , \alpha } .$

# B. Hybrid Index Construction

The detailed construction process of our hybrid index is illustrated in Alg. 2. First, the DO initializes three empty maps (line 1): Tmap, Bmap, and Omap, which are used to store T-MAP, B-MAP, and O-MAP, respectively. For each keyword w, the DO initializes the update counter $\alpha \ : = \ : 0$ and generates the LSH value $\sigma _ { w }$ of w (line 3). The DO then runs FuzzyMapping to create a Bloom filter as the forward index for each $F _ { i } \in { \mathcal { D } } ( w )$ and constructs the inverted index tree $\mathcal { T } _ { w , \alpha }$ based on Def. 4 (line 6). Next, the DO adds $( \sigma _ { w } , \alpha )$ to Omap, adds $( f _ { k _ { 2 } } ( \sigma _ { w } \Vert \alpha ) , \mathcal { T } _ { w , \alpha } )$ to Tmap, and adds $( f _ { k _ { 2 } } ( \sigma _ { w } \| \alpha ) , h ( r o o t _ { T _ { w , \alpha } } ) \| t a g )$ to Bmap (line 7). Finally, the DO uploads Bmap to the BC, sends Tmap to the SP, and keeps Omap locally (line 12).

# C. Extension to Multi-Way Version for A-BBT

In many applications, keywords exhibit a skewed distribution, meaning that certain keywords may be shared by a large number of files. This results in oversized A-BBTs for some keywords, leading to high costs for constructing and maintaining the index [8], [21]. To address this challenge, one optimization approach is to apply a multi-way tree to reduce the number of non-leaf nodes in the A-BBT. This approach can significantly reduce the index construction and search complexity at the cost of more processing overhead at each layer of A-BBTs. For skewed distributed keyword scenarios, the size of the tree generally has a greater impact on processing time than the computation time per layer, as analyzed in our experiment in Section VIII. To achieve this, we extend the A-BBT into a balanced multi-way tree, termed A-BMT. The construction process of A-BMT is similar to that of A-BBT, with the key difference being that each node can have multiple children. The definition of each node remains largely the same as in Def. 4, except for the hash value of non-leaf nodes, which is modified as follows: $H = h ( E B F \vert \vert A B F \vert \vert H _ { 1 } \vert \vert \cdot \cdot \cdot \vert \vert H _ { n } )$ , where n is the number of child nodes. The A-BMT construction features the same functionalities as the A-BBT in terms of privacy protection and correctness verification.

Algorithm 2: Construction of Hybrid Index   
Input: The dataset $\mathcal{D}$ , keyword space $\mathcal{W}$ , security parameter $m$ , ASPE key $sk_1$ , HMAC key $sk_2$ , PRF keys $\{k_1, k_2, \{k_i'\}_{i=1}^\ell\}$ , and LSH family $\mathcal{H} = \{h_{a_i, b_i}\}_{i=1}^\ell$ 1 Initialize three empty maps: Bmap, Tmap, Omap;

2 for each keyword $w \in \mathcal{W}$ do

3 $\alpha \leftarrow 0$ , $\sigma_w \leftarrow$ FuzzyKeyword $(w, \mathcal{H})$ ;

4 $\mathcal{ID}_{w,\alpha} \leftarrow \{i \mid F_i \in \mathcal{D}(w)\}$ ;

5 $\mathcal{B} \leftarrow$ FuzzyMapping $(\mathcal{D}(w), \mathcal{H}, \{k_i'\}_{i=1}^\ell, m)$ ;

6 $\mathcal{T}_{w,\alpha}, tag \leftarrow$ A-BBT $(\mathcal{ID}_{w,\alpha}, \mathcal{B}, sk_i, sk_2, k_1)$ ;

7    Put $(\sigma_w, \alpha)$ into Omap; Put $(f_{k_2}(\sigma_w \| \alpha), \mathcal{T}_{w,\alpha})$ into Tmap; Put $(f_{k_2}(\sigma_w \| \alpha), h(root_{\mathcal{T}_w,\alpha}) \| tag)$ into Bmap;

8 Function FuzzyKeyword $(w, \mathcal{H})$ :

9    Transform $w$ into a uni-gram vector $v$ ;

10 $\sigma_w = h_{a_1, b_1}(v) \| \cdots \| h_{a_\ell, b_\ell}(v)$ ;

11    return $\sigma_w$ ;

12 return Bmap to BC and Tmap to SP.

# VI. EFFICIENT SECURE VERIFIABLE FUZZY SEARCH

In this section, we design an efficient, secure, and verifiable fuzzy search protocol, denoted as $\mathrm { E ^ { 3 } F S }$ . As illustrated in our system model (cf. Fig. 2), after the index construction phase, the protocol comprises four algorithms: file update, trapdoor generation, keyword search, and result verification. Leveraging the updatable hybrid index, the protocol securely updates the index structure based on a secret counter and generates a trapdoor for each query to facilitate secure searches with forward-privacy protection. Verification is performed by the DU using the VO from the SP and digests from the BC. These algorithms are designed to meet stringent requirements for data privacy and forward privacy while achieving sublinear complexity in both the search and verification processes.

# A. File Update

To support dynamic updates while ensuring forward privacy, we utilize the secret counter stored in the O-MAP on the DO to facilitate the update process. During each update, the DO first increments the locally stored counter and then generates new tokens and keys based on it for the updated file indexes and trapdoors. This approach effectively breaks the link between historical trapdoors and the newly updated files, thereby forming an implicit chained index structure. The detailed update protocol is presented in Alg. 3.

Algorithm 3: File Update   
Input: Update file pair $(w, \mathcal{ID}_{ut}(w), \mathcal{D}_{ut}(w))$ , update type $ut$ , security parameter $m$ , ASPE key $sk_1$ , HMAC key $sk_2$ , LSH family $\mathcal{H} = \{h_{a_i,b_i}\}_{i=1}^\ell$ , and PRF keys $\{k_1, k_2, k_3, \{k_i'\}_{i=1}^\ell\}$   
DO:

1 $\overline{\sigma_{w}} \leftarrow$ FuzzyKeyword(w);
2 $\alpha \leftarrow$ Omap.GET( $\sigma_{w}$ ), $\alpha \leftarrow \alpha + 1$ , Put ( $\sigma_{w}, \alpha$ ) in Omap;
3 for each id in $ID_{ut}(w)$ do
4 if ut is delete then
5 $\lfloor$ $id \leftarrow -id;$ 6 $B \leftarrow$ FuzzyMapping( $D_{ut}(w)$ , $H, \{k_{i}'\}_{i=1}^{\ell}, m);$ 7 $sk_{1} \leftarrow \{M_{1}, M_{2}, f_{k_{3}}(\sigma_{w} \| \alpha)\};$ 8 $T_{w,\alpha}, tag \leftarrow A-BBT(ID_{ut}(w), D_{ut}(w), sk_{1}, sk_{2}, k_{1});$ 9 Return ( $f_{k_{2}}(\sigma_{w} \| \alpha), T_{w,\alpha}$ ) to SP and $(f_{k_{2}}(\sigma_{w} \| \alpha), h(root_{T_{w,\alpha}} \| tag))$ to BC.
SP:
Put ( $f_{k_{2}}(\sigma_{w} \| \alpha), T_{w,\alpha}$ ) into Tmap;
BC:
Put ( $f_{k_{2}}(\sigma_{w} \| \alpha), h(root_{T_{w,\alpha}} \| tag)$ ) into Bmap.

For the keyword-file pairs to be updated, the DO first runs FuzzyKeyword to obtain the token $\sigma _ { w }$ for the keyword w. Next, the DO retrieves the counter α of w from the locally stored Omap and increments it to $\alpha + 1$ in Omap (lines 1–2). Before generating the updated index, the DO checks the update type for each file. If it is a deletion operation, the id of the file is set to $^ { 6 6 } - i d ^ { 5 }$ (lines 3–5). Then the DO runs FuzzyMapping to create a forward index for each file $F _ { i } ~ \in ~ \mathcal { D } _ { u t } ( w )$ and constructs a new index tree $\mathcal { T } _ { w , \alpha }$ based on Def. 4 (lines 6–8). Finally, the DO sends the updated index $( f _ { k _ { 2 } } ( \sigma _ { w } \Vert \alpha ) , \mathcal { T } _ { w , \alpha } )$ to the SP and the updated digest $( f _ { k _ { 2 } } ( \sigma _ { w } \| \alpha ) , h ( r o o t _ { \mathcal { T } _ { w , \alpha } } ) \| t a g )$ to the BC. The SP and BC then insert the received index and digest into Tmap and Bmap, respectively (lines 9–11).

# B. Trapdoor Generation

For trapdoor generation, given a keyword query $\mathcal { Q } ^ { \mathrm { ~ ~ } } =$ $\{ w _ { 1 } , w _ { 2 } , \ldots , w _ { q } \}$ from the DU (as shown in Alg. 4), the DO first selects the keyword with the estimated lowest frequency, assumed to be $w _ { 1 }$ , to minimize the search space. The DO then runs FuzzyKeyword to obtain the LSH value $\sigma _ { w _ { 1 } }$ and retrieves the update counter of $w _ { 1 }$ from Omap (line 1). Next, the DO constructs the Bloom filter for Q using PRF-encrypted LSH (lines $2 \substack { - 6 } )$ . For each update counter $\alpha ,$ the DO generates the token $\kappa = f _ { k _ { 2 } } ( \sigma _ { w _ { 1 } } \| \alpha )$ for the inverted index. Subsequently, the DO runs ASPE.TrapGen to generate the encrypted token τ for the forward index and applies HMAC.Auth to create the authentication tag ν for Q (lines 8–12). Finally, the DO sends the trapdoor $\mathcal { T } \mathcal { D } = \{ \kappa _ { i } , \tau _ { i } , \nu _ { i } \} _ { i = 0 } ^ { \alpha }$ to the SP.

Example 1. Fig. 4 illustrates an example of the trapdoor generation process for the keyword $w _ { 1 }$ before and after an update. In the initialization phase, denoted as time $T _ { 1 }$ , the SP stores the initial A-BBT for $w _ { 1 }$ , and the BC stores the corresponding initial digest of the A-BBT. In the update phase, denoted as time $T _ { 2 } ,$ , new files with identifiers $i d _ { 1 3 } , i d _ { 1 4 }$ , and $i d _ { 1 5 }$ are added. The DO first increments the update counter $\alpha ,$ and runs $\operatorname { A l g } .$ 1 to generate the updated A-BBT. The encrypted token and the digest stored on the BC are also updated based on α. When a query is issued, the old token cannot be linked to the latest trapdoor. Specifically, the tokens $\kappa , \tau ,$ , and ν generated at $T _ { 1 }$ cannot be used to query the index generated at $T _ { 2 }$ . This ensures that $\mathrm { E ^ { 3 } F S }$ guarantees forward privacy.

Algorithm 4: Trapdoor Generation   
Input: A keyword query $Q = \{w_{1}, w_{2}, \cdots, w_{q}\}$ , security parameter m, ASPE key $sk_{1}$ , HMAC key $sk_{2}$ , PRF keys $\{k_{1}, k_{2}, k_{3}, \{k_{i}^{\prime}\}_{i=1}^{\ell}\}$ , and LSH family $H = \{h_{a_{i},b_{i}}\}_{i=1}^{\ell}$ 1 $\sigma_{w_{1}} \leftarrow \text{Fuzzykeyword}(w_{1}), \alpha \leftarrow \text{Omap.GET}(\sigma_{w_{1}})$ ;

2 $G \leftarrow \{g_{i} | g_{i} = f_{k_{i}^{\prime}} \cdot h_{a_{i},b_{i}}, 1 \leq i \leq l\}$ ;

3 Initialize an m-bit zero Bloom filter B;

4 for each keyword $w_{i}$ in Q do

5 Transform $w_{i}$ into a uni-gram vector $v_{i}$ ;

6 Insert $v_{i}$ into B using G;

7 TD ← empty set;

8 for i = $\alpha$ to 0 do

9 $\kappa \leftarrow f_{k_{2}}(\sigma_{w_{1}} \| i), sk_{1} \leftarrow \{M_{1}, M_{2}, f_{k_{3}}(\sigma_{w} \| i)\}$ ;

10 $\tau \leftarrow \text{ASPETrapGen}(B, sk_{1})$ ;

11 $\nu \leftarrow \text{HMAC.Auth}(sk_{2}, L_{Q_{i}}, \tau)$ ;

12 Add $(\kappa, \tau, \nu)$ to TD;

13 return Trapdoor TD.

![](images/a173120518d068d528ca20ad8fa95c280ed317388c7466d55029cabeb06752b1.jpg)



Fig. 4: Example of the trapdoor generation for keyword $w _ { 1 }$ before and after update with forward-privacy guarantee.

# C. Keyword Search

The keyword search algorithm is executed by the SP, which quickly locates specific A-BBTs using the trapdoor $\mathcal { T D }$ provided by the DU. The algorithm then can perform a top-down search on these A-BBTs in parallel, obtaining the search results and generating the VO with sublinear complexity relative to dataset size, as shown in Alg. 5. Our designed VO consists of two parts: $V O _ { c r }$ and $V O _ { c p } ,$ , which are used to verify the correctness and completeness of the results, respectively. The $V O _ { c r }$ is generated using the HMAC algorithm, while $V O _ { c p }$ comprises the following components: (1) the EBF , ABF , and hash values of child nodes from non-leaf nodes that do not meet the search criteria along the search path; (2) the $i d , \pi _ { i d } , E B F .$ , and ABF from the leaf nodes on the search path. Starting from the root node, the SP uses ASPE.Search to compute the inner product between the $E B F$ of the node and the trapdoor T D. It then checks whether the current node contains all the query keywords by comparing the inner product with the threshold T .

• If the current node n is a leaf node, the SP computes $V O _ { c r }$ by HMAC.Eval(n.ABF, ν), sets $V O _ { c p } = ( n . i d ,$ n.π, n.EBF, n.ABF, H⊥, H⊥), and adds $( V O _ { c r } , V O _ { c p } )$ to the V O for n. If ASPE.Search( $n . E B F , \tau ) ~ \geq ~ T$ , indicating that a target file has been found, the SP adds $n . i d$ to the result set R (lines 8–13).

Algorithm 5: Keyword Search   
Input: Trapdoor $\mathcal{T}\mathcal{D} = \{\kappa_i,\tau_i,\nu_i\}_{i=0}^{\alpha}$ , Threshold $T$ 1 Initialize two empty sets: $\mathcal{R}$ and $\mathcal{V}\mathcal{O}$ ;  
2 for each $(\kappa_i,\tau_i,\nu_i)$ in $\mathcal{T}\mathcal{D}$ do  
3 Initialize two empty sets: $R_i$ and $VO_i$ ;  
4 $\mathcal{T}_{w,i} \leftarrow \text{Tmap.GET}(\kappa_i)$ ;  
5 Search $(\mathcal{T}_{w,i},\tau_i,\nu_i,R_i,VO_i)$ ;  
6 Add $R_i$ to $\mathcal{R}$ and $VO_i$ to $\mathcal{V}\mathcal{O}$ ;  
7 Function Search $(n,\tau,\nu,R,VO)$ :  
8 if $n$ is a leaf node then  
9 if APSE.Search(n.EBF, $\tau$ ) $\geq T$ then  
10 Add n.id into $R$ ;  
11 $VO_{cr} \leftarrow \text{HMAC.Eval}(n.ABF,\nu)$ ;  
12 $VO_{cp} \leftarrow (n.id,n.\pi,n.EBF,n.ABF,H_\perp,H_\perp)$ ;  
13 Add $(VO_{cr},VO_{cp})$ to $VO$ ;  
14 else  
15 if APSE.Search(n.EBF, $\tau$ ) $\geq T$ then  
16 Search(n.lchild, $\tau,\nu,R,VO$ );  
17 Search(n.rchild, $\tau,\nu,R,VO$ );  
18 else  
19 $VO_{cr} \leftarrow \text{HMAC.Eval}(n.ABF,\nu)$ ;  
20 $VO_{cp} \leftarrow (n.EBF,n.ABF,H_l,H_r)$ ;  
21 Add $(VO_{cr},VO_{cp})$ to $VO$ ;  
22 return Result $\mathcal{R}$ and Verification Objects $\mathcal{V}\mathcal{O}$ to DU.

• If the current node n is a non-leaf node, the SP first checks whether ASPE.Search $( n . E B F , \tau ) \ge T$ . If the condition is satisfied, the SP continues the search by invoking the Search function to examine the left and right child nodes of the current node (lines 15–17). Otherwise, n does not meet the query requirements. The SP prunes the subtree of n to reduce search complexity and applies HMAC.Eval to compute $V O _ { c r }$ for n. The SP then sets $V O _ { c p }$ to $( n . E B F , n . A B F , H _ { l } , H _ { r } )$ and adds $( V O _ { c r } , V O _ { c p } )$ to the V O, serving as proof of nonintersection between the query and index (lines 19–21).

Example 2. Fig. 5 illustrates an example of performing a keyword search and generating the VO for the query $\begin{array} { r c l } { Q } & { = } & { \{ w _ { 1 } , w _ { 2 } , w _ { 3 } \} } \end{array}$ . Assume that the keyword $w _ { 1 }$ is selected and has been updated once. In the two $\mathsf { A - B B T s } ,$ only documents $f _ { 4 }$ and $f _ { 1 5 }$ contain all the keywords in Q. Consequently, the result set $\begin{array} { r l r } { \mathcal { R } } & { { } = } & { \{ 4 , 1 5 \} } \end{array}$ is returned, along with $\{ ( 1 3 , \pi _ { 1 3 } , E B F _ { 1 3 } , A B F _ { 1 3 } , H _ { \perp } , H _ { \perp } )$ , $\begin{array} { c c } { { ( E B F _ { 1 6 } , A B F _ { 1 6 } , H _ { 1 4 } , H _ { \perp } ) , } } & { { ( 1 5 , \pi _ { 1 5 } , E B F _ { 1 5 } , A B F _ { 1 5 } , H _ { \perp } ) } } \end{array}$ , $H _ { \perp } ) , ( 4 , \pi _ { 4 } , E B F _ { 4 } , A B F _ { 4 } , H _ { \perp } , H _ { \perp } ) , ( 5 , \pi _ { 5 } , E B F _ { 5 } , A B F _ { 5 }$ , $H _ { \perp } , H _ { \perp } ) , ( E B F _ { 8 } , A B F _ { 8 } , H _ { 7 } , H _ { 1 } ) \}$ are returned as the $V O _ { c p }$ , and $\{ V O _ { c r } ^ { 1 3 } , V O _ { c r } ^ { 1 6 } , V O _ { c r } ^ { 1 5 } , V O _ { c r } ^ { 4 } , V O _ { c r } ^ { 5 } , V O _ { c r } ^ { 8 } \}$ is returned as the $V O _ { c r }$ . Note that non-leaf nodes passing verification do not need to provide information, as the parent nodes of child nodes matching the query inherently satisfy the query. This approach effectively filters out nodes that are not part of the search path, including intermediate nodes, thereby enhancing both search and verification efficiency.

# D. Verification

For efficient verification, instead of directly checking fuzzy search results, the DU reproduces the search trace on the $\mathsf { A } \mathrm { - }$ ${ \mathsf { B B T s } } ,$ as presented in Alg. 6. Upon receiving the result set R and the verification object set VO, the DU first retrieves the root hash $h ( r o o t \tau _ { w , i } )$ and the tag set tag for each corresponding A-BBT from the on-chain stored Bmap using the trapdoor $\{ \kappa _ { i } \} _ { i = 0 } ^ { \alpha }$ (line 2). Next, the DU reconstructs the root hashes using $V O _ { c p }$ to verify the completeness of the search results. If any reconstructed root hash differs from those stored on the BC, the algorithm returns $\tt r e j e c t$ , indicating incomplete results (lines 3–5). If the completeness check is passed, the DU proceeds to verify the correctness of the search results. For each $V O _ { c r _ { i j } }$ in $\nu \mathcal { O } _ { i } ,$ the DU decrypts the $t a g$ using the key $k _ { 1 }$ to obtain the label value $L _ { i j }$ for verification. The function HMAC.Ver is then called to perform the verification, and if the output is false, indicating incorrect results, the algorithm returns $\tt r e j e c t$ (lines 6–9). If both the completeness and correctness verifications pass, the algorithm returns accept, indicating that the SP has honestly executed the search.

Algorithm 6: Verification   
Input: $\{\kappa_i, L_{Q_i}\}_{i=0}^{\alpha}, \{VO_i\}_{i=0}^{\alpha}$ , Threshold $T$ , PRF key $k_1$ and HMAC key $sk_2$ 1 for $i = \alpha$ to 0 do
2 $(h(root_{\mathcal{T}_{w,\alpha}}), tag) \leftarrow \text{Bmap.GET}(\kappa_i)$ ;
3    Rebuild $h(root_{\mathcal{T}_{w,i}'})$ by all $VO_{cp_j} \in VO_i$ ;
4    if $h(root_{\mathcal{T}_{w,i}'}) \neq h(root_{\mathcal{T}_{w,i}})$ then
5    return Reject
6    for each $VO_{crij}$ in $VO_i$ do
7 $L_{ij} \leftarrow \text{PRF.Dec}(k_1, tag)$ ;
8    if HMAC.Ver( $sk_2$ , $\{L_{ij}, L_{Q_i}\}, T, VO_{crij}$ ) then
9    return Reject
10 return Accept.

![](images/bffb7abb11eeb93e7889d5a966882eb022ce10af079375233d1da5818642f775.jpg)



Fig. 5: Example of the keyword search and VO generation processes over the A-BBTs of keyword $w _ { 1 }$ .

# VII. THEORETICAL ANALYSIS

In this section, we present the theoretical analysis of E3FS regarding its complexity, security, and verification properties.

# A. Complexity Analysis

In this subsection, we theoretically analyze the asymptotic computation and communication complexity of $\mathrm { E } ^ { \mathrm { 3 } } \mathrm { F } \bar { \mathrm { S } }$ and compare it with several state-of-the-art works [21], [22].

Theorem 1. The computation cost of the Index Construction, Update, Trapdoor Generation, Search, and Verification algorithms in $E ^ { 3 } F S$ is given by $\mathcal { O } ( m ^ { 2 } N ) , \mathcal { O } ( m ^ { 2 } u ) , \mathcal { O } ( \alpha m ^ { 2 } )$ , $\mathcal { O } ( m n _ { 1 } )$ , and $\mathcal { O } ( m n _ { 2 } )$ , respectively. Here, m denotes the index length; N and u are the total and updated number of keyword-file pairs; α is the update count for keyword w; $n _ { 1 }$ is the number of files containing the least frequent keyword in a query; and $n _ { 2 }$ is the number of returned match/mismatch proofs. The communication costs for trapdoor and VO transmission are $\mathcal { O } ( \alpha ) ( | f | + | B | + | \mathbb { R } | )$ and $\mathcal { O } ( n _ { 2 } ) ( | h | + | B | + | \mathbb { R } | )$ , respectively, where $| B |$ is the Bloom filter length, |f | is the PRF output length, and h is the keyed-hash length.

TABLE I: Performance Comparison Regarding Computation and Communication Costs 

<table><tr><td rowspan="2">Schemes</td><td colspan="5">Computation cost</td><td colspan="2">Communication cost</td></tr><tr><td>Index Construction</td><td>Update</td><td>Trapdoor</td><td>Search</td><td>Verification</td><td>Trapdoor</td><td>Verifiable Object</td></tr><tr><td>MFSE [30]</td><td> $\mathcal{O}(m^{2}n)$ </td><td>-</td><td> $\mathcal{O}(m^{2})$ </td><td> $\mathcal{O}(mn)$ </td><td>-</td><td> $\mathcal{O}(1)|B|$ </td><td>-</td></tr><tr><td>VRMFS [22]</td><td> $\mathcal{O}(m^{2}n)$ </td><td>-</td><td> $\mathcal{O}(m^{2})$ </td><td> $\mathcal{O}(mn)$ </td><td> $\mathcal{O}(mn)$ </td><td> $\mathcal{O}(1)|B|$ </td><td> $\mathcal{O}(n)|\mathbb{R}|$ </td></tr><tr><td>VFSA [21]</td><td> $\mathcal{O}(Mkn)$ </td><td>-</td><td> $\mathcal{O}(qk)$ </td><td> $\mathcal{O}(qkn)$ </td><td> $\mathcal{O}(n_{3}p\log p)$ </td><td> $\mathcal{O}(qk)|h|$ </td><td> $\mathcal{O}(n_{3})(|h|+|\mathbb{G}|)+\mathcal{O}(d)(|B|+|\mathbb{G}|)$ </td></tr><tr><td>E3FS</td><td> $\mathcal{O}(m^{2}N)$ </td><td> $\mathcal{O}(m^{2}u)$ </td><td> $\mathcal{O}(\alpha m^{2})$ </td><td> $\mathcal{O}(mn_{1})$ </td><td> $\mathcal{O}(mn_{2})$ </td><td> $\mathcal{O}(\alpha)(|f|+|B|+|\mathbb{R}|)$ </td><td> $\mathcal{O}(n_{2})(|h|+|B|+|\mathbb{R}|)$ </td></tr></table>

n: Number of files; q: Number of query keywords; k: Number of keyed-hash functions; M: Total number of keywords; d: Number of returned files; n3: Number of mismatch proofs in VFSA (generally $n _ { 1 } \leq n , n _ { 2 } \leq n _ { 3 } \leq$ n); p: Order of the cyclic multiplicative group.

Proof. The index construction phase consists of three main steps: plaintext index generation, encryption, and authentication. The time required for plaintext index generation depends on the number of keywords per file. The encryption and authentication costs are linear in the number of keyword-file pairs, with complexities of $\mathcal { O } ( m ^ { 2 } N )$ and $\mathcal { O } ( m N )$ , respectively. They are one-time operations and will not affect users’ experience. Similar to index construction, the update cost is $\mathcal { O } ( m ^ { 2 } u )$ . Trapdoor generation involves α multiplications with m-dimensional matrices, resulting in a per-query complexity of $\mathcal { O } ( \alpha m ^ { 2 } )$ . Search is dominated by the matching operation, specifically the inner product of the trapdoor and index within the target A-BBT. Its worst-case complexity is $\mathcal { O } ( m n _ { 1 } )$ , with an average case of $\mathcal { O } ( m \log n _ { 1 } )$ . Verification primarily relies on the HMAC.Ver algorithm, which verifies mismatch nodes and matching leaf nodes in the target A-BBT, leading to a complexity of $\mathcal { O } ( m n _ { 2 } )$ . Both trapdoor and VO transmission require only one communication round per query, with communication complexity linear to α and $n _ { 2 } .$ , respectively.

Comparison with existing works: As shown in Table I, VRMFS [22] and VFSA [21] represent the state-of-the-art works in secure and verifiable multi-keyword fuzzy search. Compared to [22], $\mathrm { E ^ { 3 } F S }$ improves search and verification efficiency by reducing its complexities from linear to sublinear relative to the dataset size. Specifically, for search complexity, E3FS reduces the factor n to a smaller $n _ { 1 }$ , and for verification complexity, it reduces the factor n and $n _ { 3 }$ to a generally smaller n2 compared to [21], [22]. Regarding communication costs, $\mathrm { E ^ { 3 } F S }$ incurs slightly higher trapdoor transmission overhead than [21], [22]. However, for VO transmission, E3FS achieves lower costs due to the reduced number of VOs.

# B. Security Analysis

To prove the security of $\mathrm { E ^ { 3 } F S }$ , we adopt the simulationbased approach [47]. The History is defined as $\begin{array} { r l } { { \mathcal { H } } } & { { } = } \end{array}$ $\{ \mathcal { D } , \mathcal { T } _ { O } , \mathcal { T } _ { T } , \mathcal { T } _ { B } , \mathcal { Q } , \mathcal { U } \}$ , where D represents the plaintext file set, $\mathcal { T } _ { O } , \mathcal { T } _ { T }$ , and $\mathcal { T } _ { B }$ denote the Omap, Tmap, and Bmap, respectively, $\mathcal { Q } = \{ { \mathcal { Q } } _ { 1 } , \ldots , { \mathcal { Q } } _ { t } \}$ is the set of executed queries, and U is the set of executed updates. The View is defined as $\mathcal { V } = \{ \mathcal { D } ^ { * } , \mathcal { I } _ { T } ^ { * } , \mathcal { T } _ { B } ^ { * } , \mathcal { T } \mathcal { D } , \mathcal { U } ^ { * } \}$ , where $\mathcal { D } ^ { \ast } \mathcal { I } _ { T } ^ { \ast } , \mathcal { I } _ { B } ^ { \ast }$ , and $\ b { \mathcal { U } } ^ { * }$ are the encrypted forms of $\mathcal { D } , \mathcal { I } _ { T } , \mathcal { I } _ { B }$ , and U respectively, and $\mathcal { T D }$ is the set of query trapdoors. The Trace is defined as follows:

• Size pattern: The size of file set D, keyword set W, keyword-file pairs $\textstyle \sum _ { w \in { \mathcal { W } } } { \mathcal { D } } ( w )$ , and each A-BBT.

• Query pattern: Denoted as $Q ( { \mathcal { D } } , { \mathcal { Q } } ) = M ,$ , where M is a brinary matrix. In the i-th row, if $M _ { i j } = M _ { i z } = 1$ , we say the query $\mathcal { Q } _ { j }$ and $\mathcal { Q } _ { z }$ get the same file. In our scheme, the SP can also infer if two queries utilize the same keyword to search a specific A-BBT.   
• Access pattern: Denoted as $A ( \mathcal { D } , \mathcal { Q } ) = \{ a _ { \mathcal { Q } _ { 1 } } , \ldots , a _ { \mathcal { Q } _ { t } } \}$ , where $a _ { \mathcal { Q } _ { i } } ~ = ~ \{ ( i d , s c o ) | F _ { i d } \in \mathcal { D } ( \mathcal { Q } _ { i } ) \}$ and sco represents the relevance score between Qi and the file $F _ { i d }$ .   
• Update pattern: Denoted as $U P ( w ) ~ = ~ \{ t , u t , i n d \}$ , where t is the update timestamp, $u t \ \in \ \{ a d d , d e l e t e \}$ , and ind is the updated files related to the keyword w.

Theorem 2. $E ^ { 3 } F S$ ensures KBM-secure and forward privacy.

Proof. The authentication on A-BBT influences the unforgeability of search results but does not affect the security of the outsourced data. Therefore, we prove the theorem without authentication. The updated index is constructed for update operations by introducing new random numbers and ASPE keys, following similar steps to those outlined here. For simplicity, the construction steps are omitted.

To construct an indistinguishable View $\gamma _ { s }$ against V, the simulator S performs the following steps:

Step $\boldsymbol { \mathbf { \mathit { 1 } } } \colon \boldsymbol { \mathcal { S } }$ generates the simulated dataset $\mathcal { D } _ { s } ^ { * } .$ Specifically, $s$ generates each simulated file $D _ { S _ { i } } ^ { * } \in \{ 0 , 1 \} ^ { | \breve { D } _ { i } ^ { * } | }$ , where $i \in$ $[ | \mathcal { D } ^ { * } | ]$ and $D _ { i } ^ { * } \in \mathcal { D } ^ { * }$ . S then outputs $\mathbf { \mathit { \hat { D } } } _ { S } ^ { * } = \{ \hat { D } _ { S _ { i } } ^ { * } \ \vert \ i \in [ \vert \mathbf { \mathit { D } } ^ { * } \vert ] \}$ .

Step $2 \colon \boldsymbol { S }$ randomly generates a new $A S P E$ key $s k ^ { \prime } =$ $\{ M _ { 1 } ^ { \prime } , M _ { 2 } ^ { \prime } , S ^ { \prime } \}$ and a new PRF keys $k _ { 2 } ^ { \prime } .$ .

Step 3: S generates the simulated query $\mathcal { Q } _ { \mathcal { S } }$ and trapdoor $\mathcal { T D } _ { \mathcal { S } }$ . For each query $\mathcal { Q } _ { i } \in \mathcal { Q }$ and each keyword $w _ { j } \in \mathcal { Q } .$ , S first constructs the simulated query $\mathcal { Q } _ { S _ { i } }$ and the simulated keyword $w _ { S _ { i } }$ . For the Bloom filter $B _ { i } \in \{ 0 , 1 \} ^ { m }$ of $\mathcal { Q } _ { i }$ and $B _ { w _ { i } } \in \{ 0 , \bar  1 \} ^ { m }$ of $w _ { j } , s$ randomly generates the simulated $B _ { S _ { i } } ~ \in ~ \{ 0 , 1 \} ^ { m }$ and $\smash { B _ { w s _ { i } } \in \{ 0 , 1 \} ^ { m } }$ , ensuring that the number of 1s in $B _ { S _ { i } }$ jand $B _ { w _ { S } }$ matches that in $B _ { i }$ and $B _ { w _ { j } }$ . Then, S selects the same keyword $w _ { i } ~ \in ~ \mathcal { Q } _ { i }$ from the History and applies FuzzyKeyword to generate $\sigma _ { w _ { \mathcal { S } _ { i } } }$ . Finally, S encrypts $B _ { S _ { i } }$ using ASPE.TrapGen with $s k ^ { \prime }$ and encrypts $\sigma _ { w _ { i } }$ with $f _ { k _ { 2 } ^ { \prime } } . \ s$ outputs the simulated trapdoor $\mathcal { T } \mathcal { D } _ { S } = \{ ( f _ { k _ { \rangle } ^ { \prime } } ( \sigma _ { w _ { S _ { \rangle } } } ) , \dot { E } n c _ { s k ^ { \prime } } ( B _ { S _ { i } } ) ) \mid i \in [ t ] \}$ .

2 i Step 4: S generates the simulated secure index $\mathcal { T } _ { T s } ^ { * }$ and $\mathcal { T } _ { B _ { S } } ^ { * }$ . or each . The ${ \cal D } _ { S _ { i } } ^ { * } \ \in \ { \cal D } _ { S } ^ { * } ,$ erates a , where $V _ { S _ { i } }$ $D _ { i } ^ { * } \in \mathcal { D } ( w _ { j } )$ $w _ { j } \in \mathcal { Q } , s$ set $D _ { S _ { i } } ^ { * } \in { \mathcal { D } } _ { S } ( w _ { S _ { i } } )$ . For each $w _ { j } \in { \mathcal { Q } } ,$ , if $w _ { j } \in D _ { i } ^ { * } , s$ updates $V _ { S _ { j } }$ as $V _ { S _ { j } } + B _ { w _ { S _ { i } } }$ . Next, S replaces all elements in $V _ { S _ { \tau } }$ j that exceed 1 with 1. Subsequently, S constructs the simulated A-BBT $\mathcal { T } _ { w _ { s _ { i } } }$ for $w _ { S _ { j } }$ based on Alg. 1. For $\mathcal { T } _ { B _ { S } } ^ { * } , { S }$ constructs it using the root hash of each A-BBT $\mathcal { T } _ { w _ { s _ { i } } } .$ . Finally, S outputs the encrypted index $\mathcal { T } _ { T s } ^ { * } = \{ ( f _ { k _ { 2 } ^ { \prime } } ( w _ { S _ { j } } ) , \mathcal { T } _ { w _ { S _ { i } } } ) ~ | ~ w _ { S _ { j } } \in \mathcal { Q } _ { S } \}$ and $\mathcal { T } _ { B _ { S } } ^ { * } = \{ ( f _ { k _ { 2 } ^ { \prime } } ( w _ { S _ { j } } ) , h ( r o o t _ { T _ { w _ { S } } } ) ) \ | \ w _ { S _ { j } } \in \mathcal { Q } _ { S } \} .$ .

Step 5: Finally, S outputs $\mathcal { V } _ { S } = \left\{ \mathcal { D } _ { S } ^ { * } , \mathcal { L } _ { T _ { S } } ^ { * } , \mathcal { L } _ { B _ { S } } ^ { * } , \mathcal { T } \mathcal { D } _ { S } \right\}$

The simulated View $\gamma _ { s }$ has the same Trace as V, and no PPT adversary can efficiently distinguish between V and $\nu _ { s }$ . The privacy of the original data is ensured through symmetric encryption. Additionally, the security provided by ASPE and PRF guarantees the privacy of the index and query. The introduction of randomness through ASPE ensures the indistinguishability of trapdoors. Furthermore, while the twostage separation of the index could potentially lead to crossleakage of the information in Query pattern, as noted in prior works [32], this issue is addressed in E3FS by using distinct ASPE keys for each keyword. Therefore, $\mathrm { E ^ { 3 } F S }$ is KBM-secure, ensuring both data privacy and query privacy. Furthermore, in the update algorithm, the updated ASPE key $f _ { k _ { 3 } } ( \sigma _ { w } \| \alpha )$ and the updated token $f _ { k _ { 2 } } ( \sigma _ { w } \| \alpha )$ are used to encrypt and search the updated index, respectively, preventing any linkage between previous trapdoors and the updated data. Therefore, forward privacy is guaranteed.

# C. Verification Analysis

Theorem 3. $E ^ { 3 } F S$ guarantees correctness and completeness verifiability for search results.

Proof. For completeness verification, due to the collision resistance of hash functions, the unforgeability of each index in $\mathrm { E ^ { 3 } F S }$ is guaranteed by the root hash of A-BBTs. Finding a hash collision at any position in the authenticated A-BBT while keeping the root digest unchanged is computationally infeasible. Moreover, in our scheme, the root hash is stored on the trusted blockchain. After receiving the result, the DU can reconstruct the root hash and retrieve the unforgeable root hash from the BC for comparison. Therefore, E3FS ensures completeness verifiability. For correctness verification, $\mathrm { E ^ { 3 } F S }$ employs HMAC to authenticate each node in the A-BBTs, ensuring evaluation correctness [20]. The proof of HMAC’s correctness and security is omitted for brevity. □

# VIII. EXPERMENTS

In this section, we compare our E3FS protocol with state-ofthe-art secure verifiable fuzzy search protocols for encrypted databases [21], [22] under various system settings. Additionally, we evaluate the on-chain performance of $\mathrm { E ^ { 3 } F S }$ i n a simulated blockchain network. Our protocol demonstrates superior performance in terms of efficiency and communication overhead while also supporting dynamic updates.

# A. Implementation Details

Datasets. We conducted experiments using a real-world medical dialogue dataset [23], which contains 792,099 question-answer pairs from medical conversations. The dataset was processed into 3, 000 files for our experiments, with 5, 000 keywords extracted, averaging 80 keywords per document.

Baselines. We compared our approach with one classical method and two state-of-the-art methods: (1) MFSE [30]. The original secure fuzzy multi-keyword search. (2) VRMFS [22] and VFSA [21]. They improve upon MFSE by supporting verifiability. VFSA uses a Bloom filter tree structure, while VRMFS uses individual Bloom filters for indexing, achieving better performance in separate sub-protocols. These three methods are designed for outsourced databases and do not account for blockchain support or dynamic updates.

![](images/b8d5de7272fc4d47851cef67d6c1daa305b196d8371e1984685f44fff71c9128.jpg)



(a) Adding a letter

![](images/0875203dec89b57d5cd32a0e2575f33e1a26d9bb7df374d07ec597269a848d42.jpg)



(b) Missing a letter

![](images/1a431731f77789e82d85ef2e98ffd7310f1a73e8b7b832f1962dc1aba36227c9.jpg)



(c) Misspelling a letter

![](images/1dd5eb305ee46d833ffc15a43fbd9dc5883a0317c2fa84c373ece2913853c18a.jpg)



(d) Swapping two letters   
Fig. 6: Accuracy for Varying Representations & LSH Numbers

Metric. We evaluated our approach from two perspectives: efficiency and communication overhead. The following metrics are considered: (1) the algorithms’ runtime; (2) the size of the VO and trapdoor; (3) the on-chain overhead.

Parameter Setup. Similar to [22], [31], we used unigram to represent keywords. We evaluated the accuracy of three different representations (i.e., unigram, bigram, and trigram) against four common types of keyword spelling errors: letter addition, letter omission, letter substitution, and letter swapping. The accuracy is defined as the ratio of correctly matched keywords (i.e., when the hash bucket string of a keyword is the same for both incorrect and correct spellings) to the total number of keywords. As shown in Fig. 6, unigram outperforms bigram and trigram across all error types. Therefore, we used unigram for efficiency evaluations and set the number of LSH functions to 6. Additionally, the Bloom filter (BF) for indexing has a dimension of 1, 200 with 10 hash functions, and the average false positive rate is calculated as $( 1 - e ^ { - ( 8 0 \cdot 1 0 ) / 1 2 0 0 } ) ^ { k } \leq \bar { 0 . 1 \% }$ .

Implementations. We evaluated the binary-tree and the quadtree versions of E3FS, denoted for simplicity as E3FS (A-BBT) and $\mathrm { E ^ { 3 } F S }$ (A-BMT), respectively. All experiments were conducted on a machine with 16 GB of RAM and 16 AMD cores. Both the client and server were implemented in Python, while the blockchain component was tested by deploying smart contracts to a locally simulated Ethereum network using TestRPC. We reported the average results from 10 runs of each experimental setup.

# B. Evaluation of Index Construction

We now evaluate the index construction performance of different schemes. Fig. 7 illustrates the impact of the number of documents, the number of keywords, and the length of BF on index construction efficiency on the DO side.

Impact of the number of documents. We fixed the total number of extracted keywords at $| \mathcal { W } | ~ = ~ 4 , 0 0 0$ and the BF length at $\mathcal { M } = 1 , 2 0 0$ . As shown in Fig. 7a, the time cost of index construction for these schemes increases as the dataset size grows. Among the schemes, $\mathrm { E ^ { 3 } F S }$ is faster than VFSA but slower than VRMFS and MFSE. This is due to the complex verification functionalities in E3FS and VFSA, which require additional intermediate index computations. The indexing time of $\mathrm { E ^ { 3 } F S }$ (A-BMT) is superior to that of E3FS (A-BBT) because the number of nodes in A-BMT is significantly smaller than that in A-BBT.

![](images/a79d3787a395c59bc7d8f1fe8a65cf4241441febf56db3b590040a5b79467ee1.jpg)  
10 2 (a) Varying |D|

![](images/596413169189f569869d05dafedcb7fd853624eeec1e10f0a4d4fa9b8d6d8f8c.jpg)  
(b) Varying |W|

![](images/650a5067c587159ffcbf4f1f4a3c878005f1ba66b33afb3eae4a750d3725a2a6.jpg)  
(c) Varying M

800 1200 1600 2000 24Length of BFs Fig. 7: Index Construction Performance.   
![](images/d148437464ce19ff8a6861151788b3bbedfb8b30edbd441d59f9260438df83ca.jpg)

![](images/c01b7d1cca7534893e72cb6bfb4ab276f226d51c129e07b7942d8d8c6589498f.jpg)



Fig. 8: Update Performance.

Impact of the number of keywords. We fixed the number of documents at $| \mathcal { D } | = 5 0 0$ and the BF length at $\mathcal { M } = 1$ , 200 to observe how the number of keywords affects the efficiency of index construction. As shown in Fig. 7b, as the number of keywords increases, the index construction time for VFSA increases, while the other four methods remain relatively stable. This behavior occurs because, in VFSA, the use of accumulator-based index authentication causes the time cost of index construction to grow with the number of keywords, whereas other methods are unaffected.

Impact of the length of BF. Since the indexes of these methods are constructed using BF, we examine the impact of BF length. We fixed $| \mathcal { D } | = 5 0 0$ and $| \mathcal { W } | = 4 , 0 0 0$ . As shown in Fig. 7c, as the length of BF increases, the time cost of index construction for all schemes slightly rises because a longer BF increases the computational complexity of encryption.

Although E3FS performs less efficiently than MFSE and VRMFS during index construction, it is a one-time operation, and the overhead is entirely acceptable in real-world scenarios. In contrast, E3FS provides more robust and efficient search and verification, along with support for dynamic updates.

# C. Evaluation of Update

We evaluated the update costs on the DO side, including the time required to generate the new indexes and trapdoors after several updates. As shown in the left figure of Fig. 8, with the BF length fixed at $\mathcal { M } = 1 , 2 0 0$ , we tested the time required to update the index as the number of initial files and extracted keywords varied. As the number of updated indexes increases, the update time for $\mathrm { E ^ { 3 } F S }$ also increases. However, the impact of different initial file counts and extracted keyword quantities is minimal, as the additional hashing time required for updates is negligible. We also tested the time required to generate trapdoors as the number of query keywords increases. As shown in the right figure of Fig. 8, the results indicate that as the number of update times grows, the time to generate trapdoors increases linearly from 0.1s to 0.4s, while the number of query keywords had almost no effect on the results.

![](images/5954efbeea0dcf32fa7e58b1b7bd630ba255067be65ae9ae3e84cd4e0b4e3061.jpg)



(a) Varying |W|

![](images/9be03efa2a7e8baffcca15bcb1a04d44543380a78aa56412999a104362715c2c.jpg)



(b) Varying M   
Fig. 9: Trapdoor Construction Performance.

# D. Evaluation of Trapdoor Construction

The factors influencing the efficiency and size of trapdoor construction mainly consist of two aspects: the number of query keywords k and the length of the trapdoor. For fairness, we set the update counter α = 0. Fig. 9a illustrates the impact of the number of query keywords. As shown in the figure, as the number of query keywords increases from 2 to 10, the trapdoor construction time and size for VFSA increase, while the other three methods remain relatively stable. The trapdoor construction time and size for E3FS and VRMFS are similar about 10ms and 100KB, respectively, slightly higher than those for MFSE and VFSA. Fig. 9b also depicts the effect of the length of the trapdoor. As the length of BF increases from 800 to 2, 400, the trapdoor construction time and size also slightly increase for $\mathrm { E ^ { 3 } F S }$ and VRMFS, while the other two methods remain relatively stable. All four methods exhibit trapdoor construction times below 0.1s, meeting real-time requirements.

# E. Evaluation of Search Delay

Fig. 10 illustrates the impact of the number of documents, the number of keywords, and the length of BF on search efficiency on the SP side.

Impact of the number of documents. We fixed $| \mathcal { W } | = 4 , 0 0 0$ and $\mathcal { M } = 1 , 2 0 0$ . As shown in Fig 10a, as the dataset size increases, the search time for E3FS and VFSA exhibits a sublinear growth trend, while MFSE and VRMFS show linear growth, aligning with our theoretical analysis. Specifically, E3FS outperforms the other methods, being approximately 20000× faster than VFSA, 5× faster than MFSE, and 58.6× faster than VRMFS. VFSA and VRMFS extend MFSE for verifiability but incur extra overhead for VO generation, which slows search speed. In contrast, E3FS uses inverted index trees that narrow the search to files containing a specific keyword. Moreover, blockchain-stored immutable hashes and tags streamline VO generation. E3FS requires only a few inner product computations for matching and VO generation, making it significantly faster. The performance of A-BMT and A-BBT exhibits slight fluctuations, as their efficiency depends on the distribution of queried keywords. When the queried keywords appear in only a few files, A-BBT usually outperforms A-BMT by pruning more subtrees, thereby reducing computational overhead. Conversely, when keywords are present in most files, A-BMT performs better due to its smaller tree height and fewer nodes to process.

![](images/c98065ebd0edcc61bd8fd17e69b8c36708dd18ef79f83da725305a42e27cc7bb.jpg)



2 (a) Varying |D|

![](images/f5a1f21ae3436b0b40b0aa4343e6f6ce69f26e7e97108e2f15b845dd5bff0276.jpg)  
(b) Varying |W|

![](images/070d4d3dd1c3464c7b556f8138eb0c9954046eafba365f76023f186d57e5dab0.jpg)



(c) Varying M

1200 1600 2000Length of BFsFig. 10: Search Performance.   
![](images/77f4d52b797d40520654f812f44fa1f10169b26cb58912106594ab986e2583d5.jpg)



2 (a) Varying |D|

![](images/a539da11a085ea6e44f4e493e6e593a1334f2630581e3cb841b3511560a747ec.jpg)  
(b) Varying |W|

![](images/efd7b10bcc47915d09b1d8d9d98626915afd814947965a8fe0ec57ac510218d4.jpg)  
(c) Varying M   
1200 1600 2000 Fig. 11: Verification Performance.

Impact of the number of keywords. We fixed $| \mathcal { D } | = 5 0 0$ and M = 1, 200. As shown in Fig. 10b, as the number of keywords increases from 1, 000 to 5, 000, the search time for all methods remains relatively stable. This is because the number of extracted keywords affects index construction but does not impact the efficiency of the search phase.

Impact of the length of BF. We fixed |D| = 500 and $| \mathcal { W } | =$ 1, 000. As shown in Fig. 10c, as the length of the BF increases from 800 to 2, 400, the search time for these methods increases correspondingly. This is because the computational complexity of the search increases as M increases.

# F. Evaluation of Verification Delay

Fig. 11 illustrates the impact of the number of documents, the number of keywords, and the length of BF on verification efficiency on the DU side. We used parameters relevant to the search experiments. As shown in Fig. 11a, as the dataset size increases, the verification time for all methods also grows because more indexes are involved in verification. Our method outperforms the others, being at least 34.4× faster than VFSA and 124× faster than VRMFS. Similar to the search phase, as the number of keywords increases, the verification time for all methods remains relatively stable as shown in Fig. 11b. Moreover, as the BF length increases from 800 to 2, 400, the verification time for these methods also increases as shown in Fig. 11c. The slight fluctuation in the verification performance of A-BMT and A-BBT is similar to the search experiment, as it depends on the actual nodes processed on A-BBT or A-BMT.

# G. Evaluation of Communication Overhead

Fig. 12 illustrates the impact of the number of documents, the number of keywords, and the length of the BF on the size of the VO. As shown in Fig. 12a, as the dataset size increases, the VO size for VFSA and VRMFS grows, while E3FS (A-BBT) and E3FS (A-BMT) remain stable. Our method outperforms the others, as it avoids the need to validate a large number of indexes. For example, when $| \mathcal { D } | = 2 , 5 0 0 ,$ the VO size of $\mathrm { E ^ { 3 } F S }$ is only about 0.02% of VFSA and 1.7% of VRMFS. Similar performance trends can be observed in 1.0  30 Fig. 12b and Fig. 12c. Notably, the VO sizes generated by 0.5 these methods are not sensitive to the number of keywords or the length of the BF. This is because the size of each VO 500 1000 1500 2000 2500Number of documents object returned by these methods is nearly constant.

![](images/ac93e62e571a8527d9743790c68257d8a0494634002f3aae33efd0aca4447f8e.jpg)  
1(a) Varying |D|

![](images/566bcf651c6a1f2f198e95aad7e075b1b3a05ddc5daf1285237e6fa2ffe4d78e.jpg)  
(b) Varying |W|

![](images/fb2081619f4caa6bde6f00942c4a34469fb3d1ceadfe2718844db556e9fc58b6.jpg)  
(c) Varying |M|

1200 1600 2Length of BFsFig. 12: The Size of VO.   
![](images/d4ed0dd0d3309e7f95d75a4e4d10cfc0339785a44848be09e29a81c48e0946f1.jpg)

![](images/41de1385569c731ed35bb300d2c92ff53d025aafd42f085b3c83ba784f5d5dcb.jpg)  
Fig. 13: On-chain Performance.

# H. Evaluation of on-chain performance

We also evaluated the average on-chain gas consumption, latency, and storage overhead for maintaining the ADS (i.e., Bmap) across different dataset sizes and keyword space sizes. The on-chain overhead of E3FS is relatively low, with the time required to upload the ADS for 2,500 files to the blockchain being under 60 seconds, and the required storage space being less than 1000 KB, as shown in Fig. 13. As shown in the left figure, the gas consumption and latency for recording the ADS on-chain increase linearly with the size of the keyword space, while the number of files has a lesser impact. This is because the number of key-value pairs recorded on-chain is determined by the number of keywords. The right figure of Fig. 13 further confirms this result, showing that as the keyword space increases, the on-chain storage overhead grows, while the number of files has a smaller effect.

# IX. CONCLUSION

In this study, we propose ${ \mathrm { E } } ^ { 3 } { \mathrm { F } } { \mathrm { S } } ,$ , a framework designed to support verifiable and secure fuzzy search in hybrid storage blockchains over dynamically updatable data. E3FS leverages a newly designed updatable hybrid index with efficient onchain storage to enable secure and efficient authenticated fuzzy indexing. By incorporating the hybrid index with verification mechanisms and forward-privacy protection designs, E3FS ensures data and query security, as well as result verifiability, with sublinear computational complexity for each query. Experimental results on a real-world dataset demonstrate the superior performance of $\mathrm { E ^ { 3 } F S }$ compared to existing baselines.

# ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 62441228, Science and Technology Tackling Program of Anhui Province, No.202423k09020016.

# REFERENCES

[1] M. Wang, Y. Guo, C. Zhang, C. Wang, H. Huang, and X. Jia, “Medshare: A privacy-preserving medical data sharing system by using blockchain,” IEEE Transactions on Services Computing, vol. 16, no. 1, pp. 438–451, 2023.   
[2] H. Wu, Z. Li, R. Song, and B. Xiao, “Enabling privacy-preserving and efficient authenticated graph queries on blockchain-assisted clouds,” IEEE Transactions on Knowledge and Data Engineering, vol. 35, no. 9, pp. 9728–9742, 2023.   
[3] X. Xiang and X. Zhao, “Blockchain-assisted searchable attribute-based encryption for e-health systems,” Journal of Systems Architecture, vol. 124, p. 102417, 2022.   
[4] F. Chen, J. Wang, C. Jiang, T. Xiang, and Y. Yang, “Blockchain based non-repudiable iot data trading: Simpler, faster, and cheaper,” in IEEE INFOCOM 2022 - IEEE Conference on Computer Communications, pp. 1958–1967, 2022.   
[5] C. Li, Y. Cao, Z. Hu, and M. Yoshikawa, “Blockchain-based bidirectional updates on fine-grained medical data,” in 2019 IEEE 35th International Conference on Data Engineering Workshops (ICDEW), pp. 22–27, 2019.   
[6] C. Zhang, Y. Guo, H. Du, and X. Jia, “Pfcrowd: Privacy-preserving and federated crowdsourcing framework by using blockchain,” in 2020 IEEE/ACM 28th International Symposium on Quality of Service (IWQoS), pp. 1–10, 2020.   
[7] Q. Liu, Y. Peng, M. Xu, H. Jiang, J. Wu, T. Wang, T. Peng, and G. Wang, “Mpv: Enabling fine-grained query authentication in hybrid-storage blockchain,” IEEE Transactions on Knowledge and Data Engineering, vol. 36, no. 7, pp. 3297–3311, 2024.   
[8] N. Cui, D. Wang, J. Li, H. Zhu, X. Yang, J. Xu, J. Cui, and H. Zhong, “Enabling efficient, verifiable, and secure conjunctive keyword search in hybrid-storage blockchains,” IEEE Transactions on Knowledge and Data Engineering, vol. 36, no. 6, pp. 2445–2460, 2024.   
[9] Y. Guo, C. Zhang, C. Wang, and X. Jia, “Towards public verifiable and forward-privacy encrypted search by using blockchain,” IEEE Transactions on Dependable and Secure Computing, vol. 20, no. 3, pp. 2111– 2126, 2022.   
[10] B. Chen, T. Xiang, D. He, H. Li, and K.-K. R. Choo, “Bpvse: Publicly verifiable searchable encryption for cloud-assisted electronic health records,” IEEE Transactions on Information Forensics and Security, vol. 18, pp. 3171–3184, 2023.   
[11] M. Wang, Y. Guo, C. Zhang, C. Wang, H. Huang, and X. Jia, “Medshare: a privacy-preserving medical data sharing system by using blockchain,” IEEE Transactions on Services Computing, 2021.   
[12] S. Liu, L. Chen, G. Wu, H. Wang, and H. Yu, “Blockchain-backed searchable proxy signcryption for cloud personal health records,” IEEE Transactions on Services Computing, vol. 16, no. 5, pp. 3210–3223, 2023.   
[13] Q. Liu, Y. Peng, Z. Tang, H. Jiang, J. Wu, T. Wang, T. Peng, and G. Wang, “veffchain: Enabling freshness authentication of rich queries over blockchain databases,” IEEE Transactions on Knowledge and Data Engineering, vol. 36, no. 5, pp. 2285–2300, 2024.   
[14] C. Zhang, C. Xu, H. Wang, J. Xu, and B. Choi, “Authenticated keyword search in scalable hybrid-storage blockchains,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE), pp. 996–1007, 2021.   
[15] C. Xu, C. Zhang, and J. Xu, “vchain: Enabling verifiable boolean range queries over blockchain databases,” in Proceedings of the 2019 International Conference on Management of Data, pp. 141–158, 2019.   
[16] H. Wang, C. Xu, C. Zhang, and J. Xu, “vchain: a blockchain system ensuring query integrity,” in Proceedings of the 2020 ACM SIGMOD International Conference on Management of Data, pp. 2693–2696, 2020.   
[17] H. Wang, C. Xu, C. Zhang, J. Xu, Z. Peng, and J. Pei, “vchain+: Optimizing verifiable blockchain boolean range queries,” in 2022 IEEE 38th International Conference on Data Engineering (ICDE), pp. 1927– 1940, 2022.   
[18] S. Li, Z. Zhang, J. Xiao, M. Zhang, Y. Yuan, and G. Wang, “Authenticated keyword search on large-scale graphs in hybrid-storage blockchains,” in 2024 IEEE 40th International Conference on Data Engineering (ICDE), pp. 1958–1971, 2024.   
[19] S. Li, Z. Zhang, M. Zhang, Y. Yuan, and G. Wang, “Authenticated subgraph matching in hybrid-storage blockchains,” in 2024 IEEE 40th International Conference on Data Engineering (ICDE), pp. 1986–1998, 2024.

[20] Z. Wan and R. H. Deng, “Vpsearch: Achieving verifiability for privacypreserving multi-keyword search over encrypted cloud data,” IEEE transactions on dependable and secure computing, vol. 15, no. 6, pp. 1083–1095, 2016.   
[21] Q. Tong, Y. Miao, J. Weng, X. Liu, K.-K. R. Choo, and R. H. Deng, “Verifiable fuzzy multi-keyword search over encrypted data with adaptive security,” IEEE Transactions on Knowledge and Data Engineering, vol. 35, no. 5, pp. 5386–5399, 2022.   
[22] X. Li, Q. Tong, J. Zhao, Y. Miao, S. Ma, J. Weng, J. Ma, and K.- K. R. Choo, “Vrfms: Verifiable ranked fuzzy multi-keyword search over encrypted data,” IEEE Transactions on Services Computing, vol. 16, no. 1, pp. 698–710, 2022.   
[23] S. Chen, Z. Ju, X. Dong, H. Fang, S. Wang, Y. Yang, J. Zeng, R. Zhang, R. Zhang, M. Zhou, P. Zhu, and P. Xie, “Meddialog: a large-scale medical dialogue dataset,” arXiv preprint arXiv:2004.03329, 2020.   
[24] J. Li, Q. Wang, C. Wang, N. Cao, K. Ren, and W. Lou, “Enabling efficient fuzzy keyword search over encrypted data in cloud computing.” Cryptology ePrint Archive, Paper 2009/593, 2009.   
[25] J. Li, Q. Wang, C. Wang, N. Cao, K. Ren, and W. Lou, “Fuzzy keyword search over encrypted data in cloud computing,” in IEEE INFOCOM 2010 - IEEE Conference on Computer Communications, pp. 1–5, 2010.   
[26] H. Zhang, S. Zhao, Z. Guo, Q. Wen, W. Li, and F. Gao, “Scalable fuzzy keyword ranked search over encrypted data on hybrid clouds,” IEEE Transactions on Cloud Computing, vol. 11, no. 1, pp. 308–323, 2021.   
[27] Q. Liu, Y. Peng, S. Pei, J. Wu, T. Peng, and G. Wang, “Prime inner product encoding for effective wildcard-based multi-keyword fuzzy search,” IEEE Transactions on Services Computing, vol. 15, no. 4, pp. 1799–1812, 2020.   
[28] Y. Li, J. Ning, and J. Chen, “Secure and practical wildcard searchable encryption system based on inner product,” IEEE Transactions on Services Computing, vol. 16, no. 3, pp. 2178–2190, 2023.   
[29] Q. Liu, S. Pei, K. Xie, J. Wu, T. Peng, and G. Wang, “Achieving secure and effective search services in cloud computing,” in 2018 17th IEEE International Conference On Trust, Security And Privacy In Computing And Communications/ 12th IEEE International Conference On Big Data Science And Engineering (TrustCom/BigDataSE), pp. 1386–1391, 2018.   
[30] B. Wang, S. Yu, W. Lou, and Y. T. Hou, “Privacy-preserving multikeyword fuzzy search over encrypted data in the cloud,” in IEEE INFOCOM 2014 - IEEE Conference on Computer Communications, pp. 2112–2120, 2014.   
[31] Z. Fu, X. Wu, C. Guan, X. Sun, and K. Ren, “Toward efficient multikeyword fuzzy search over encrypted outsourced data with accuracy improvement,” IEEE Transactions on Information Forensics and Security, vol. 11, no. 12, pp. 2706–2716, 2016.   
[32] J. Chen, K. He, L. Deng, Q. Yuan, R. Du, Y. Xiang, and J. Wu, “Elimfs: achieving efficient, leakage-resilient, and multi-keyword fuzzy search on encrypted cloud data,” IEEE Transactions on Services Computing, vol. 13, no. 6, pp. 1072–1085, 2017.   
[33] Z. Fu, L. Xia, X. Sun, A. X. Liu, and G. Xie, “Semantic-aware searching over encrypted data for cloud computing,” IEEE Transactions on Information Forensics and Security, vol. 13, no. 9, pp. 2359–2371, 2018.   
[34] J. Shao, R. Lu, Y. Guan, and G. Wei, “Achieve efficient and verifiable conjunctive and fuzzy queries over encrypted data in cloud,” IEEE Transactions on Services Computing, vol. 15, no. 1, pp. 124–137, 2019.   
[35] C. Zhang, C. Xu, J. Xu, Y. Tang, and B. Choi, “GEM2-tree: A gasefficient structure for authenticated range queries in blockchain,” in 2019 IEEE 35th International Conference on Data Engineering (ICDE), pp. 842–853, 2019.   
[36] Q. Shao, S. Pang, Z. Zhang, and C. Jing, “Authenticated range query using sgx for blockchain light clients,” in Database Systems for Advanced Applications, pp. 306–321, 2020.   
[37] S. Hu, C. Cai, Q. Wang, C. Wang, X. Luo, and K. Ren, “Searching an encrypted cloud meets blockchain: A decentralized, reliable and fair realization,” in IEEE INFOCOM 2018 - IEEE Conference on Computer Communications, pp. 792–800, 2018.   
[38] P. Jiang, F. Guo, K. Liang, J. Lai, and Q. Wen, “Searchain: Blockchainbased private keyword search in decentralized storage,” Future Generation Computer Systems, vol. 107, pp. 781–792, 2020.   
[39] Z. Chen, Q. Li, X. Qi, Z. Zhang, C. Jin, and A. Zhou, “Blockope: Efficient order-preserving encryption for permissioned blockchain,” in 2022 IEEE 38th International Conference on Data Engineering (ICDE), pp. 1245–1258, 2022.

[40] J. G. Chamani, Y. Wang, D. Papadopoulos, M. Zhang, and R. Jalili, “Multi-user dynamic searchable symmetric encryption with corrupted participants,” IEEE Transactions on Dependable and Secure Computing, vol. 20, no. 1, pp. 114–130, 2023.   
[41] P. Indyk and R. Motwani, “Approximate nearest neighbors: towards removing the curse of dimensionality,” in Proceedings of the Thirtieth Annual ACM Symposium on Theory of Computing, pp. 604–613, 1998.   
[42] M. Datar, N. Immorlica, P. Indyk, and V. S. Mirrokni, “Locality-sensitive hashing scheme based on p-stable distributions,” in Proceedings of the Twentieth Annual Symposium on Computational Geometry, pp. 253–262, 2004.   
[43] W. K. Wong, D. W.-l. Cheung, B. Kao, and N. Mamoulis, “Secure knn computation on encrypted databases,” in Proceedings of the 2009 ACM SIGMOD International Conference on Management of data, pp. 139– 152, 2009.   
[44] Y. Zhang, J. Katz, and C. Papamanthou, “All your queries are belong to us: The power of file-injection attacks on searchable encryption,” USENIX Security Symposium,USENIX Security Symposium, Jan 2016.   
[45] D. Liu, W. Wang, P. Xu, L. T. Yang, B. Luo, and K. Liang, “d-DSE: Distinct dynamic searchable encryption resisting volume leakage in encrypted databases,” in 33rd USENIX Security Symposium (USENIX Security 24), pp. 2563–2580, 2024.   
[46] S. Garg, P. Mohassel, and C. Papamanthou, “Tworam: efficient oblivious ram in two rounds with applications to searchable encryption,” in Annual International Cryptology Conference, pp. 563–592, Springer, 2016.   
[47] R. Curtmola, J. Garay, S. Kamara, and R. Ostrovsky, “Searchable symmetric encryption: improved definitions and efficient constructions,” in Proceedings of the 13th ACM conference on Computer and communications security, pp. 79–88, 2006.