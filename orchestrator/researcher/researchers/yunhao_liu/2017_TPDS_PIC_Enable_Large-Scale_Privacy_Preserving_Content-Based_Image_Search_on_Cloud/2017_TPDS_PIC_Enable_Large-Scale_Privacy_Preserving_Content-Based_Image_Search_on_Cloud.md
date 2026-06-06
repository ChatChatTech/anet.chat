# PIC: Enable Large-Scale Privacy Preserving Content-Based Image Search on Cloud

Lan Zhang , Member, IEEE, Taeho Jung, Student Member, IEEE, Kebin Liu, Member, IEEE, Xiang-Yang Li, Fellow, IEEE, Xuan Ding, Jiaxi Gu, and Yunhao Liu, Fellow, IEEE

Abstract—Many cloud platforms emerge to meet urgent requirements for large-volume personal image store, sharing and search. Though most would agree that images contain rich sensitive information (e.g., people, location and event) and people’s privacy concerns hinder their participation into untrusted services, today’s cloud platforms provide little support for image privacy protection. Facing large-scale images from multiple users, it is extremely challenging for the cloud to maintain the index structure and schedule parallel computation without learning anything about the image content and indices. In this work, we introduce a novel system PIC: A Privacy-preserving Image search system on Cloud, which is a step towards feasible cloud services which provide secure content-based large-scale image search with fine-grained access control. Users can search on others’ images if they are authorized by the image owners. Majority of the computationally intensive jobs are handled by the cloud, and a querier can now simply send the query and receive the result. Specially, to deal with massive images, we design our system suitable for distributed and parallel computation and introduce several optimizations to further expedite the search process. Our security analysis and prototype system evaluation results show that PIC successfully protects the image privacy at a low cost of computation and communication.

Index Terms—Large-scale image search, privacy protection, Map-Reduce

# 1 INTRODUCTION

AS on-board cameras get more and more popular,numerous high-resolution photos/videos are genersearching large-scale image data become challenging. Increasing number of service providers support cloud based image/video services, e.g., Amazon Cloud Drive, Apple iCloud, Cloudinary, Flicker, Youtube and Google. Contentbased image search is a core functionality for various image/video applications, e.g., personal image/video management, criminal investigation using crowd-sourced photos/videos (e.g., the Boston Marathon investigation) and medical image study and diagnosis. Usually, video search can be reduced to some sort of key frame search, e.g., Video Google [1]. However, there are a lot of sensitive information in image data, and increasing worry about privacy could hinder many potential useful image services [2], [3]. For example, the face search functionality of Facebook has been abandoned for two years due to the privacy concern from users and governments. A start-up smartphone app Keep-Safe hides images and videos from unauthorized users by simply encrypting image folders with a PIN code, and it owned 13 million users and gained 2 millions dollars investment. Although keeping sensitive images safe, simple encrypting disables the content-based image search functionality. While leveraging the power of cloud and crowdsourcing, the owner requires the right to protect his/her images from any unauthorized parties (including the service provider), meanwhile keep the ability to search all authorized images.

State-of-the-art image search systems typically extract distinctive feature descriptors (high-dimension feature vectors) from interest points of images to measure their content similarity, e.g., 128 dimensional SIFT [5]. One image is usually described by hundreds of feature vectors (as shown in Fig. 1), and millions of photos uploaded to the cloud imply billions of feature vectors. Therefore, it is necessary to introduce optimization techniques such as indexing or distributed computing to accelerate the search process, e.g., [6], [7]. But most previous efforts did not support image privacy protection or assumed that feature vectors do not reveal content of images. However, recent researches show that an image can be approximately reconstructed based on the output of a blackbox feature descriptor software such as those classically used for image indexing [4], [8]. As presented in Fig. 1, the image reconstructed using SIFT feature vectors appears quite similar as the original image, and shows a good match with the original one. Those methods are entirely automatic and much better reconstruction may be achieved with user interaction. The reconstruction allows clear interpretation of the semantic image content, which arouses great concerns on the image privacy in the image indexing and search systems.

![](images/fb51897a9e6e9f9cd1263ebf3a8107a9f89659ce8bee42ff59e873c1f84be6c3.jpg)



(a)Compare original image and reconstructed image using SIFT feature vector. [5]

![](images/5d85129e1eb94ad2fa9a5583f71573e15230919340c7fb63564753ca69049f6e.jpg)



(b) Feature vector detection and matching results between original image and reconstructed image.   
Fig. 1. Comparison between original image and images reconstructed from feature vectors.

As a result, large-scale outsourced personal images need efficient yet private content-based search urgently. Existing large-scale image indexing and search systems usually do not support privacy protection mechanisms. Some existing systems [9] tag images with keywords and metadata, and search the occurrences of encrypted tags in an exact match manner. Those systems cannot support content-based image search, whose core is measuring distances between vision feature vectors. Some systems use homomorphic encryption to achieve private vector distance measurement, but reveal search results to the cloud and cost expensive computation, e.g., [10] and [11]. PoP [12] supports privacypreserving outsourced photo search, but it cannot deal with massive images.

To implement a desired privacy-friendly image search platform, we need to address several conflicted critical challenges. First, all feature vectors should be encrypted, the search process should be completed in a non-interactive way, and all storage and majority of computation should be outsourced to the cloud, while the cloud cannot learn the images, feature vectors and search results. Second, a user should be able to search freely on all his/her authorized images on the cloud, which could be encrypted by keys from multiple owners. Third, facing large image sets, the cloud should leverage the power of indexing and parallel computing using encrypted data. Traditional secure multi-party computation (SMC) [13], [14], [15], or homomorphic encryption ([10], [11]) cannot be the solution to the large-scale image search problem. On one hand, the garbled circuit’s size is exponentially greater than the size of the input, which is often very large in image search (e.g.,, thousands of 128 dimensional feature vectors of real values), so the communication and computation overhead is beyond practicality. On the other hand, a simple homomorphic will allow the decrypter of the final result to also decrypt the ciphertext of image content. Moreover, both of them may lead to rounds of interactions among the image owner, cloud server and the querier, and the image owners need to always stay online. Besides, they cannot support key conversion or parallel computation. Facing all these challenges, we carefully design a novel system PIC: A Privacypreserving Image search system on Cloud using lightweight multi-level homomorphic encryption as a building block to implement an efficient non-interactive image search outsourcing. The main contributions of this work are summarized as follows:

We propose a novel architecture and a whole set of techniques to support similarity computing and indexing on encrypted feature vectors, which thus enable feasible private feature-based image search upon large-scale encrypted images with untrusted cloud. Our system also supports privacy-preserving image storage and sharing among users. Users can search on others’ images if they are authorized by the image owners. Our system outsources the majority of the search job to the cloud side, but neither the image content nor the query is revealed to the cloud. What’s more, during the search, no interaction is required between the data owner and the querier or the cloud.

Our private search mechanism is compatible with the state-of-the-art image search to guarantee the search accuracy. We propose to boost privacypreserving search with distributed and parallel computation, and carefully design our encrypted indexing suitable for MapReduce framework. Several optimizations are introduced to further expedite the search process without privacy loss.

We implement a prototype including both cloud side and client side. The cloud is a cluster of computers with distributed file system (Hadoop HDFS) and MapReduce architecture (Hadoop MapReduce), and clients are Android phone and laptops. We evaluate our system using more than one million highly diverse real-life photos. The security analysis shows that PIC successfully protect the image privacy, and the evaluation shows the efficiency of our system, which is capable to be used in a wide range of platforms including resource-bounded mobile devices.

The rest of this paper is organized as follows. Section 2 reviews the image search model and introduces building blocks of PIC, and Section 3 gives an overview of our system framework. Section 4 presents the detail of our basic design and we refine system design in Section 5. We show the security of PIC in Section 6 with theoretical proof. To evaluate the practicality, we present comprehensive experiments in Section 7. Section 8 discusses the related work, and Section 9 concludes this paper.

# 2 PRELIMINARY

We address the problem of efficient large-scale image searching with untrusted cloud servers. Different from existing work focusing on the search efficiency, we also consider the image privacy (the image itself and its feature descriptors) of the image owner and the query privacy (the query image content and the query result) of the querier.

# 2.1 Large Scale Image Search

To guarantee the search accuracy, we employ the common large-scale image search model in the computer vision field. Here, we briefly review it.

In the field of computer vision, feature descriptor is widely adopted for image similarity measurement. Given an image $I ,$ interest points are detected and one feature vector $\mathbf { x } _ { i }$ is extracted for each interest point to indicate the appearance characteristics around this point. The image’s feature descriptor consists of all extracted feature vectors, denoted as $\pmb { \chi } : = \{ \pmb { x } _ { 1 } , \ldots , \pmb { x } _ { \alpha } \}$ . To achieve robust and fast image ¼ f gdescription, different types of descriptors are proposed, e.g. , SIFT [5] and SURF [16]. Given a specific type of descriptor, feature vectors are usually of the same dimension, e.g., the SIFT vector is 128 dimension.

# 2.1.1 Voting-Based Search Model

Many modern content-based image retrieval systems manage millions of images, i.e., billions of high-dimension feature vectors. Given a query descriptor $\pmb { \chi } : = \{ \pmb { x } _ { 1 } , \ldots , \pmb { x } _ { \alpha } \}$ of the query image ${ \cal I } _ { x } ,$ ¼ f ghere xi is the ith feature vector. and a set of descriptors $\{ \bar { \mathbf { Y } } ^ { 1 } , \ldots , \bar { \mathbf { Y } } ^ { N } \}$ of images in the big database, where $\mathbf { Y } ^ { n }$ f gis the descriptor of the nth image, existing solutions (e.g., [6] and [7]) usually search similar images of $I _ { x }$ as follows:

1. Let the score of each image in database be $S ^ { n }$ , and initialize all scores to 0.   
2. For each feature vector $\mathbf { x } _ { i }$ of $\mathbf { \boldsymbol { x } }$ and for each feature vector $\mathbf { y } _ { j } ^ { n }$ in database, the score $S ^ { n }$ is increased by $S ^ { n } : = S ^ { n ^ { \prime } } + \delta ( \mathbf { x } _ { i } , \mathbf { y } _ { j } ^ { n } )$ , where $\delta ( \mathbf x _ { i } , \mathbf y _ { i } ^ { n } )$ is the matching ¼ þ ð Þ ð Þfunction measuring the similarity between feature vector $\mathbf { x } _ { i }$ and $\mathbf { y } _ { j } ^ { n }$ based on k-nearest neighbors. Formally, the matching function is defined as

$$
\delta (\mathbf {x} _ {i}, \mathbf {y} _ {j} ^ {n}) = \left\{ \begin{array}{l l} 1 & \text { if   } \mathbf {y} _ {j} ^ {n} \text {   is   a   } k - \mathrm{NN} \text {   of   } \mathbf {x} _ {i} \\ 0 & \text { otherwise } \end{array} \right. \tag {1}
$$

For the k-NNs search, the dissimilarity of feature vectors are typically measured by Euclidean distance.

3. By ranking the image scores, images with largest scores are selected as the matched images of the query image.

# 2.1.2 Indexing-Based Approximate k-NNs Search

A very large number of feature vectors make the accurate k-nearest neighbors (k-NNs) search too expensive. Approximate search greatly improves the performance with a little loss of accuracy. The most common way is indexing largescale feature vectors by partitioning them into groups using high-dimensional clustering, e.g., [17] and [7]. Given a query feature vector, the system first finds the closest cluster header, and then distances between the query vector and the cluster members are computed to get the k-NNs. As a result, many clusters can be pruned quickly to accelerate the searching process.

# 2.2 Multi-Level Homomorphic Encryption (HE)

To implement efficient non-interactive image search and outsource the index maintenance to the cloud side, we need a light-weight encryption method which supports both homomorphic computing and key conversion. We carefully explore existing encryption protocols and employ a multilevel homomorphic encryption protocol presented by Xiao et al. [18]. The protocol is defined as follows:

Definition 1. The multi-level homomorphic encryption is defined by three algorithms (K; HE:E; HE:D), where K; HE:E and HE:D are the key generation, encryption and decryption functions respectively, and it satisfies HE: $\mathtt { D } \big ( \mathtt { H E . E } ( m , k ) \big ) = m$ given $k \gets K ( \dot { 1 } ^ { \lambda } )$ ð ð ÞÞ ¼, here m is the plain message and k is a key generðated by K.

We review the design and security proof of this protocol, and make sure it is correct. Notably, we utilize the following good properties of this protocol in our work:

Additive and Multiplicative Homomorphism:

$$
\mathrm{HE.E} (m _ {1}, k) \cdot \mathrm{HE.E} (m _ {2}, k) = \mathrm{HE.E} (m _ {1} m _ {2}, k)
$$

$$
\mathrm{HE.E} (m _ {1}, k) + \mathrm{HE.E} (m _ {2}, k) = \mathrm{HE.E} (m _ {1} + m _ {2}, k),
$$

This also implies the homomorphism over any polynomial function f , i.e.,

$$
f (\mathrm{HE.E} (m _ {1}, k), \mathrm{HE.E} (m _ {2}, k), \dots , \mathrm{HE.E} (m _ {l}, k))
$$

$$
= \mathrm{HE.E} (f (m _ {1}, m _ {2}, \dots , m _ {l}), k),
$$

Key Conversion: If we have $k = \prod _ { i } k _ { i }$ for the key $k ,$ the ¼ encryption has the following property

$$
\left(\prod_ {i} k _ {i} ^ {- 1}\right) \cdot E (m, 1) \cdot \left(\prod_ {i} k _ {i}\right) = E \left(m, \prod_ {i} k _ {i}\right) = \mathrm{HE.E} (m, k),
$$

This implies that one does not need to decrypt and reencrypt the message to alter the key of a ciphertext, which is very useful in our system design. Note that a randomizer is omitted for the sake of simplicity, so it is not possible to attack this encryption via brute-force search if the ciphertext size is large enough.

# 2.3 Distance Calculation Via HE

We can conduct the distance calculation for two feature vectors x; y on the ciphertexts as follows, where $\mathbf { x } ( j )$ refers to ð Þthe jth dimension of the feature vector $\mathbf { x } ,$ and $\mathsf { D } ( \mathbf { x } , \mathbf { y } ) = \mathsf { d } ^ { 2 } ( \mathbf { x } , \mathbf { y } )$

$$
\operatorname{HE.E} (\mathsf {D} (\mathbf {x}, \mathbf {y}), k) = \sum_ {k} (\operatorname{HE.E} (\mathbf {x} (j), k) - \operatorname{HE.E} (\mathbf {y} (j), k)) ^ {2},
$$

Then, the distance calculation can be outsourced to anyone who does not know the key on ciphertexts and neither the feature vectors nor the calculation output will be revealed. Hereafter, we use the notation $\phi _ { \mathsf { D } } ( \cdot )$ to denote the ð Þfunction which conducts distance calculation given homomorphic ciphertexts of two vectors. That is

$$
\phi_ {\mathsf {D}} (\mathrm{HE.E} (\mathbf {x}, k), \mathrm{HE.E} (\mathbf {y}, k)) = \mathrm{HE.E} (\mathsf {D} (\mathbf {x}, \mathbf {y}), k).
$$

# 2.4 Fixed Point Representation

The numeric type of feature vectors may be real number, but the homomorphic encryption used in this paper is based on large integers, therefore we need to use integers to represent real numbers first. In PIC, we use the fixed point representation ([19]) to represent real numbers due to its simplicity when applying elementary arithmetic operations to it.

![](images/f98835c71670d31e6f53e244f77fe2d9e0df16b7aa1b88d796b9b907360ce576.jpg)



Fig. 2. PIC Architecture

Given a real number a and a fixed precision $p ,$ an m 1-dimension binary array A satisfies the following in þthe fixed point representation with Two’s Complement

$$
\left\{ \begin{array}{l l} A [ 0 ] = 0 \wedge \sum_ {k = 1} ^ {m} A [ k ] \cdot 2 ^ {- k + p} \approx a & a \geq 0 \\ A [ 0 ] = 1 \wedge - \sum_ {k = 1} ^ {m - 1} (A [ k ] \oplus 1) \cdot 2 ^ {- k + p} - A [ m ] \cdot 2 ^ {- k + m} \approx a & a <   0 \end{array} \right..
$$

The minimum unit of this representation is $2 ^ { p - m } { \mathrm { ( i . e . } }$ precision), and the range of this representation is $\hat { ( } - 2 ^ { p - 1 } , 2 ^ { p - 1 } )$ . Then, we use the following integer to repreð Þsent the real number a (with some errors less than the minimum unit)

$$
\mathfrak {f} (a) = \left\{ \begin{array}{l l} \sum_ {k = 1} ^ {m} A [ k ] \cdot 2 ^ {m - k} & \text { if } A [ 0 ] = 0 \\ - \sum_ {k = 1} ^ {m} (A [ k ] \oplus 1) 2 ^ {m - k} & \text { if } A [ 0 ] = 1 \end{array} \right.,
$$

which is the definition of signed integer with Two’s complement.

Note that the addition/subtraction $( x \pm y )$ , multiplication $( x \cdot y )$ and the division (xy) are all elementary arithmetic oper-ations closed in integer domain $( \mathrm { i . e . , } a / b$ is the quotient of ab). We assume $m , p$ are pre-defined parameters based on the range and precision requirements of the application. For simplicity, we will omit the real-integer conversion and use normal arithmetic operations on real numbers in the following presentation, but the values must be converted to the fixed point representation and fixed point representation operation should be applied in applications.

# 3 SYSTEM OVERVIEW

We present the overview of our system design, threat model and the security assumption before further presenting design details.

# 3.1 Architecture & Entities

We design a novel architecture to let users store, share and search images privately via external cloud without conducting computationally heavy tasks. Leveraging lightweight multi-level homomorphic encryption as a building block, we construct the index on encrypted feature vectors and propose to separate indexing and search to cloud server (CS) and key agent (KA), and bridge different parties using key transfer, thus ensures the search private and noninteractive. The entire outsourced computation is conducted on the ciphertexts of image feature descriptors directly, therefore users’ image content privacy and query privacy are preserved against cloud servers (including CS and KA) or other adversaries. Note that, original images can be protected by symmetric encryption as usual. Fig. 2 describes the flow of our system, and our system has the following entities:

Users. A user can be an image owner and an image querier simultaneously. An owner stores and shares his images with others by outsourcing them to the cloud servers, and a querier searches an image on the DB located at the cloud server side.

Cloud Server. The cloud server is in charge of majority of the computation and the storage throughout the system. Whenever a transaction request arrives, he processes the request by computing on the ciphertexts. CS could be any commercial cloud service providers who are willing to improve their services to attract more privacy-sensitive users.

Key Agent. To make sure no one within the system learns the final key used in the encryption, we introduce a key agent, who manages various secret keys and also conduct the nearest neighbor search. Majority of the transaction between users and CS is relayed by KA. KA could be any agent who is unlikely to collude with the CS or a specific user. For example, for crowd-sourced criminal investigation, KA can be a government-controlled agent; for medical image analysis, KA can be an authoritative medical organization; for personal image management, KA can be reputable information security service provider.

A trusted party (TP) is introduced only to generate the keys, who could be an auditor or a notary public. The detailed work flow will be presented in Sections 4 and 5.

# 3.2 Threat Model

The trusted party only generates the keys, and is assumed to be fully trusted. However, the cloud server and the key agent who conducts most of the computation may be motivated to infer useful information from the outsourced computation, and they are assumed to be semi-honest, i.e., they will follow the protocol specification in general, but will also try their best to harvest the content of the encrypted communication. In general, TP,CS and KA are well protected, so we do not consider compromise attack in this paper. Also, although CS and KA are assumed to be semi-honest, the probability that both of them collude with a specific user is extremely small. Therefore, we assume that it is not possible to have a user who collude with both CS and KA.

# 3.3 Security Assumption

Because we employ the homomorphic encryption in Xiao et al. [18] whose security relies on the assumption that prime factorization is hard, we also assume that the following prime factorization is hard:

Definition 2 (Prime Factorization). A prime factorization problem is to solve all $p _ { i } { ' } s$ given a product of prime numbers $n = \prod _ { i } p _ { i }$ .

# 4 BASIC SYSTEM DESIGN

With the preliminaries and the system architecture, we are ready to present the detailed design of our system PIC, which addresses the privacy-preserving image search on cloud. The system supports the following four operations to serve the users: Initialization, key generation & policy announcement, image upload and privacy preserving image search with access control.

# 4.1 Initialization

First, TP picks the system parameter for the homomorphic encryption [18] and publishes it. Then, TP generates a master key k to be used in the homomorphic encryption, and he finds two random keys $k _ { C S } , k _ { K A }$ such that $k _ { C S } k _ { K A } = k$ and sends $k _ { C S } , k _ { K A }$ ¼to CS and KA respectively via secure channel.

# 4.2 Key Generation & Policy Announcement

Whenever a new user u joins the system, TP generates three random keys $k _ { u } , k _ { u } ^ { \prime } , k _ { u } ^ { \prime \prime }$ such that $\dot { k } = k _ { u } k _ { u } ^ { \prime } k _ { u } ^ { \prime \prime }$ . Then, he gives $k _ { u } ^ { \prime }$ to the cloud server, $k _ { u } ^ { \prime \prime }$ ¼to the key agent and $k _ { u }$ to the user u via secure channel.

Then, the user defines the access policy which controls who can/cannot search on his images. The policy is described by an access tree as in CP-ABE [20], and it is uploaded to CS for further access control.

Submitting raw personal attributes to CS will reveal the user’s identity information. Therefore, the attributes as well as access policy should be masked before uploading. Note that the access control policy is used as a black-box building block in our system, and here we present a simple policy which works with CP-ABE as a baseline method. When joining the system, every user describes his access policy with an access tree, but the attributes at the leaf nodes are replaced with the hashed values. Whenever a querier wishes to search on a group of specified users or the entire DB, the querier submits his hashed attributes to CS. CS then matches these hashed attributes with the access policies in the DB to find out the group of users that the querier is qualified to search on. We evaluate the practicality of the access policy by investigating a real social networking system (in Section 7.4), and our analysis shows that for most cases the simple access policy is sufficient and practical. For some special cases, there can be other better options for the access control (e.g., anonymous IBE with predicate encryption [21]) which achieves better anonymity, but this is not our main contribution, and we leave it as one of our future works to study.

# 4.3 Image Upload

Whenever a new user u uploads some images, he first extracts feature descriptors from them, and encrypts the descriptors using his key $k _ { u }$ as follows:

$$
\mathrm{HE.E} \big (\left\{\mathbf {X} _ {i, 1}, \mathbf {X} _ {i, 2}, \dots \right\}, k _ {u} \big).
$$

Then, the user needs to either update or create the index cluster for his feature descriptors. There are two phases for the index cluster update or construction.

1) Indices construction: Cluster representatives are selected from feature vectors as centroids of the cluster.   
2) Clustering: Other vectors are assigned to clusters.

Various clustering techniques can be applied to choose the representatives and assign the vectors, and different clustering techniques have different performance and accuracy. One can simply use k-means clustering to cluster the vectors. At each time the user wants to update the index cluster, he will either re-construct the index or just incrementally append new representatives or nodes into the current clusters.

After the clusters are prepared, he appends references to the nodes in the cluster which points to the corresponding ciphertexts of feature vectors. Then, the raw index clusters are sent to CS. To reduce the communication overhead, the user can send only the change of the index cluster instead. After he completes the update (or creation), the ciphertexts are sent to KA.

KA, upon receiving the ciphertexts, conducts the following operation for every ciphertext to get the ciphertexts with altered key $k _ { u } k _ { u } ^ { \prime }$

$$
k _ {u} ^ {\prime - 1} \mathrm{HE.E} \big (\{\mathbf {X} _ {i, 1}, \dots \}, k _ {u} \big) k _ {u} ^ {\prime} = \mathrm{HE.E} \big (\{\mathbf {X} _ {i, 1}, \dots \}, k _ {u} k _ {u} ^ {\prime} \big).
$$

Then, KA sends the new ciphertexts with altered key to CS. CS conducts the following operation to get the final ciphertexts

$$
\begin{array}{l} k _ {u} ^ {\prime \prime - 1} \mathrm{HE.E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k _ {u} k _ {u} ^ {\prime}\right) k _ {u} ^ {\prime \prime} = \mathrm{HE.E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k _ {u} k _ {u} ^ {\prime} k _ {u} ^ {\prime \prime}\right) \\ = \operatorname{HE.E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k\right). \\ \end{array}
$$

Then, CS merges the user u’s index cluster with the global one for his DB, but leaving a label to mark the owner of the cluster.

# 4.4 Privacy Preserving Search with Access Control

One image search has two phases: Level-1 search and level-2 search. In the level-1 search, KA first finds out the cluster representative in the index cluster which is closest to the querying feature vector. Then, he finds out the k-nearest neighbors (k-NNs) of the querying feature vector within the cluster in the level-2 search.

Level-1 Search. When a querier q wants to search an image, he first extracts the feature descriptor (i.e., a set of feature vectors) from the querying image. Then, he encrypts the feature descriptor of the querying image $\mathbf { X } _ { q }$ with his key $k _ { q }$ as HE:E $\left( \mathbf { X } _ { q } , k _ { q } \right)$ , and submits the ciphertexts to KA. Then, KA alters the ciphertext to HE: $\therefore \left( \mathbf { X } _ { q } , k _ { q } ^ { ^ { \bullet } } k _ { q } ^ { \prime } \right)$ and sends them to CS, and CS finally alters the ciphertexts to

$$
\begin{array}{l} \mathrm{HE.E} \left(\mathbf {X} _ {q}, k _ {q} k _ {q} ^ {\prime} k _ {q} ^ {\prime \prime} k _ {C S} ^ {- 1}\right) = \mathrm{HE.E} \left(\mathbf {X} _ {q}, k k _ {C S} ^ {- 1}\right) \\ = \operatorname{HE.E} \left(\mathbf {X} _ {q}, k _ {K A}\right). \\ \end{array}
$$

Besides, the querier also uploads his hashed attributes to CS. CS then searches all users’ policies and finds out the users that the querier is qualified to search on their images. Then, CS computes the following altered ciphertexts, where $\left\{ \mathbf { y } _ { o } \right\}$ refers to the set of feature vectors referenced (via f gciphertext) by the representatives in previously found owners’ index clusters

$$
\begin{array}{l} k _ {C S} \mathrm{HE.E} \left(\left\{\mathbf {y} _ {o} \right\}, k\right) k _ {C S} ^ {- 1} = \mathrm{HE.E} \left(\left\{\mathbf {y} _ {o} \right\}, k k _ {C S} ^ {- 1}\right) \\ = \mathrm{HE.E} \left(\left\{\mathbf {y} _ {o} \right\}, k _ {K A}\right). \\ \end{array}
$$

After all the altered ciphertexts are ready, CS computes the f function (Section 2.3) for every pair of

$\left( \mathtt { H E . E } ( \mathbf { x } , k _ { K A } ) , \mathtt { H E . E } ( \mathbf { y } , k _ { K A } ) \right)$ , where $\mathbf { x } \in \mathbf { X } _ { q }$ is a feature vecð Þð Þ ð Þ 2tor belonging to a descriptor in the querying image, and $\mathbf { y } \in \{ \mathbf { y } _ { o } \}$ . Then, CS achieves the pairwise encrypted distan-2 f gces, which are sent to KA.

KA is able to decrypt the distances since the ciphertexts are encrypted under his key $k _ { K A }$ . After decrypting the distances, he finds out the minimum distance for every $\mathbf { x } \in \mathbf { X } _ { q } ,$ which is 2the distance to the NN of x. This NN search must be conducted by the key agent instead of the cloud server or any user. Because, if the cloud server has a key to decrypt those distances, then it can also decrypt feature vectors too; while it is unreasonable to involve any user in this distance computation. This is a major reason we introduce the key agent.

Level-2 Search. After finding the nearest neighbor among the representatives for every $\mathbf { x } \in \mathbf { X } _ { q } ,$ , KA further requests the 2distances between the x and all the vectors within the NN’s cluster.

Upon receiving the request, CS generates the following altered ciphertexts using the key conversion (Section 2.2) and $\phi _ { \mathsf { D } } ( \cdot )$ function as aforementioned, where $\left\{ \mathbf { y } _ { c } \right\}$ is the set ðÞof vectors within the NN’s cluster

$$
\left\{ \right.\left.\left\{\mathrm{HE.E} (\mathsf {D} (\mathbf {x}, \mathbf {y}), k _ {K A}) \right\} _ {\forall \mathbf {y} \in \{\mathbf {y} _ {c} \}} \right\} _ {\forall \mathbf {x} \in \mathbf {X} _ {u}}.
$$

Then, he sends these ciphertexts of distances as well as the image IDs associated with the feature vectors in the ciphertexs to KA. KA then decrypts the ciphertexts and determines the k-NNs among $\big \{ \mathrm { H E . E } ( \mathsf { D } ( \mathbf { x } , \mathbf { y } ) , k _ { K A } ) \big \} _ { \forall \mathbf { y } \in \{ \mathbf { y } _ { \mathcal { L } } \} }$ for each $\mathbf { x } \in \mathbf { X } .$ f gð Þð Þ 8 2f g  Based on the distances and the corresponding image 2IDs, he calculates the score $S ^ { n }$ of all images (Section 2) appearing in the image IDs sent from CS and returns the image ID with the highest score to the querier. The querier then retrieves the encrypted image from the DB. One can further apply oblivious transfer (will be described in Section 8) to prevent the CS from inferring the query result by monitoring its memory access.

In this level-2 search, if CS does not find k ciphertexts within the cluster, he also chooses the next NN among the representatives and sends the corresponding ciphertexts to KA as well. This is repeated until he finds out at least k ciphertexts to return to KA.In practice, it happens when k is too large and won’t cause significant performance loss.

# 5 SYSTEM REFINEMENTS

The basic system we proposed in previous section achieves efficient privacy-preserving image search in some cases, e.g., people recognition in a face image collection, but its performance is degraded in more general cases, when the feature vector number of an image is large or the total image number is huge. Therefore, we further leverage the following methods to improve our system to boost up the performance.

# 5.1 Dealing with High-Resolution Images

A feature descriptor usually contains a set of high dimensional feature vectors, e.g., 128 dimension for SIFT. Since each dimension is a 64 bit real value, when we consider the encryption, each feature vector’ size becomes 64 KB because each dimension of the vector is encrypted with ${ \textbf { a } } 4 \times 4$ matrix with 256 bit integers. Then, the number of feature vectors in an image determines the size of the feature descriptor of the image. In the face recognition, 9 feature vectors are enough to conduct an accurate search because face models are well developed. However, for complicated image with hundreds of feature vectors, the size of ciphertexts is not acceptable for many mobile devices. Therefore, we further optimize our system using visual words ([1], [6]) to reduce the communication overhead. By quantizing the space of feature vector, we can obtain a visual dictionary. An image can be represented with the frequency histogram of visual words, by choosing the nearest word for each of its feature vectors. Then the feature descriptor is significantly reduced to one n-dimensional frequency vector. The similarity between images can be computed by the scalar product of two frequency vectors of the images. To minimize the accuracy loss caused by quantizing the feature vector space, we weight the frequency vector with term frequency inverse document frequency (tf-idf, [1]). The experimental results in peer works ([1]) and our evaluation result (Section 7.6) show that using this weighted frequency vector instead of exact feature vectors brings a negligible accuracy loss. In our advanced scheme, we use weighted frequency vector with visual dictionary as our feature image descriptor.

# 5.2 Leveraging the Parallel Computation

We further expedite the search process leveraging the Map-Reduce framework. To do so, our search scheme must support parallelism. By designing the search process as the level-1 search and the level-2 search, one can complete both searches (finding the NN among the representatives and the k-NNs within the cluster) by arbitrary number of mappers and one reducer. The ciphertexts of the feature vectors and the querying vector will be given to the mappers, who conducts the homomorphic operations and the key modification to generate the ciphertexts of the distances. Then, these are sent to the reducer at the KA side who decrypts and sorts the distances.

However, there is a problem if our approach is directly implemented with a MapReduce framework. Unless the data is stored with special format (e.g., bucketized), sorting limits the number of reducers to one because the mappers do not emit the (key,value)=(image ID, distance) pairs in a sorted order. Since the sorting order depends on the querying feature vector, the number of reducers will be always 1. This is a great bottle-neck since the reducer needs to wait for all (key,value) pairs emitted from all mappers before it continues to the sorting. To solve this bottleneck, we can return all the neighbors within a certain threshold distance instead of the exact NN in the level-1 search or the k-NNs in the level-2 search. By doing so, we can theoretically have arbitrary number of reducers to finish the search task in a parallel manner. If the threshold is chosen such that not enough results are found, one can easily use a binary search manner to adjust the threshold until he finds enough results to further proceed.

For the clustering algorithm, extended cluster pruning [7], [17] provides a promising way for efficient clusters construction and queries processing. We apply the extended cluster pruning with recursion in the advanced scheme. Due to the space limitation, we omit the detail of the approach here.

# 5.3 Advanced Scheme

Only the image upload component and the privacy preserving image search component will be changed in the advanced scheme. The changed operations are as follows:

# 5.3.1 Image Upload

The user u first extracts the feature vectors from every image that he wants to upload to CS. Then, he uses k-means clustering to find the k clusters among all his vectors, and sets all the centroids as elements in the visual dictionary of k elements. Hereafter, we use $\mathbf { D } _ { u }$ to denote user i’s dictionary. After $\mathbf { D } _ { u }$ is generated, user u also calculates the k-dimensional weighted frequency vector of each image I as $\mathbf { f } _ { I } ,$ and uses CP-ABE to encrypt all parameters in the weight function $( \{ f _ { i , I } , f _ { i } \} _ { i } , N )$ ) as well as $\mathbf { D } _ { u }$

$$
\mathsf {A B E . E} \big (\mathbf {D} _ {u}, \{f _ {i, I}, f _ {i} \} _ {i} = 1, \dots , k, N \big).
$$

User u sends this ciphertext to CS, and encrypts all weighted frequency vectors as

$$
\mathrm{HE.E} \left(\left\{\mathbf {f} _ {I} \right\} _ {I}, k _ {i}\right).
$$

Then, he uses aforementioned extended cluster pruning approach with recursion to construct an index tree of all $\mathbf { f } _ { I } { ' } \mathbf { s } _ { I }$ , where each node contains the reference to the corresponding encrypted vector. The raw index tree is sent to CS (if only updated, only the changed parts are sent to CS), and the encrypted ciphertexts are sent to KA.

KA, upon receiving the ciphertexts, conducts the key modification to alter the ciphertexts to

$$
\mathrm{HE.E} \big (\{\mathbf {f} _ {I} \} _ {I}, k _ {u} k _ {u} ^ {\prime \prime} \big).
$$

Then, KA sends the new ciphertexts to CS, who conducts another key modification to achieve the final ciphertexts

$$
\mathrm{HE.E} \big (\{\mathbf {f} _ {I} \} _ {I}, k _ {u} k _ {u} ^ {\prime \prime} k _ {u} ^ {\prime} \big) = \mathrm{HE.E} \big (\{\mathbf {f} _ {I} \} _ {I}, k \big).
$$

# 5.3.2 Privacy Preserving Search with Access Control

Same as the basic scheme, we also have two phases in a search.

Level-1 Search. When a querier q wants to search an image, he first extracts the feature vectors from the querying image. Then, he retrieves the $\mathsf { A B E . E } \big ( \mathbf { D } _ { o } , \{ f _ { i , I } , f _ { i } \} _ { i } \big ) =$ $1 , \cdots , k , N ) ^ { \prime } \mathbf { s }$ f g ¼of all image owner o’s that he wants to search    Þon, and decrypts the dictionaries as well as the parameters with his attributes. Then, he looks up each dictionary to create a frequency vector of his querying image for each $\mathbf { D } _ { o } .$ . Then, he calculates m weighted frequency vectors with the decrypted parameters, which are encrypted as

$$
\mathrm{HE.E} \big (\{\mathbf {f} \} _ {\text { all   owners }}, k _ {q} \big).
$$

This is relayed by KA (after altering the key to $k _ { q } k _ { q } ^ { \prime \prime } )$ and finally arrives CS who finally alters the key to $k _ { q } k _ { q } ^ { \prime \prime } k _ { q } ^ { \prime } = k$ . ¼Then, CS finds out the index trees of the users that querier q wishes to search on, and conducts the following key modification, where $\left\{ \mathbf { y } _ { o } \right\}$ refers to the set of frequency vectors reff gerenced (via ciphertext) by the cluster leaders in those index trees

$$
\mathrm{HE.E} \big (\big \{\mathbf {y} _ {o} \big \}, k k _ {C S} ^ {- 1} \big) = \mathrm{HE.E} \big (\big \{\mathbf {y} _ {o} \big \}, k _ {K A} \big).
$$

Then, CS computes the $\phi _ { D } ( \cdot )$ function for every pair of $\left( \mathtt { H E . E } ( \mathbf { x } , k _ { K A } ) , \mathtt { H E . E } ( \mathbf { y } , k _ { K A } ) \right)$ ðÞwhere x is the frequency vector ð Þð Þ ð Þof the querying image, and $\mathbf { y } \in \{ \mathbf { y } _ { o } \}$ . The outputs of the 2 f gfunction are the pairwise encrypted distances, which are sent to KA.

KA proceeds with MapReduce framework. He sends the ciphertexts to his mappers, each mapper decrypts the distances and emits the (key,value)=(image ID,distance) to his reducers, and the reducers find out the distances above a threshold u, which corresponds to the distance of x’s nearest neighbors.

Level-2 Search. After finding the NNs, KA further requests the distances between x and all vectors under those NNs in the index trees.

Upon receiving the request, CS generates the encrypted distances using the key modification as well as the $\phi _ { D } ( \cdot )$ ðÞfunction. These are sent to KA who sends those ciphertexts to his mappers to let them decrypt the distances. The (image ID,distance) pairs are sent to his reducers, and they finally find out the images whose distances are above another threshold u .

# 6 SECURITY ANALYSIS

The security of the system is given by the security of the weakest link. Since the participating adversaries are more powerful than non-participating adversaries and colluding adversaries are more powerful than single adversary, we analyze the security in the worst case scenario: Colluding participating adversaries, including CS, KA and users (TP is fully trusted). Note that CS and KA do not collude with each other, and a user can collude with at most one party between CS and KA. Therefore, we have the following two cases: Colluding user and CS; colluding user and KA.

It is already formally proved in [18] that the homomorphic encryption is secure against colluding user & CS or colluding user $\& \ K \Lambda ,$ , hence no party in the system can infer the plaintext from the ciphertext without knowing the key. We only analyze the extra information leakage in our system.

Colluding User and KA. Colluding user and KA only learn $k _ { u } , k _ { u } ^ { \prime \prime }$ during the key generation, index construction or the index update. During the image search, KA receives a number of encrypted distances $\mathtt { H E . E } ( \mathsf { D } ( \mathbf { x } , \ \mathbf { y } ) , k _ { K A } )$ which are encrypted with $k _ { K A }$ ð ð Þ Þ. Then, KA can decrypt the distances, and the colluding user (a querier in this case) will know all the distances between the encrypted feature vectors in the database and his querying feature vector. However, the ciphertexts of the nodes are not even sent to KA or user before the query result is given to the user. Therefore, the user only learns a number of distances, which is not useful to infer the images in CS’s database.

Besides, the user can only get the query result, which is the ciphertext of the queried image. Therefore, colluding user and CS do not gain useful information except the valid search result.

Colluding User and CS. Colluding user and CS only learn $k _ { u } , k _ { u } ^ { \prime }$ during the key generation. During the index forest construction and the index update, CS may share the ciphertext

$$
\mathrm{HE.E} \big (\{\mathbf {X} _ {i, 1}, \mathbf {X} _ {i, 2}, \dots \}, k _ {u} k _ {u} ^ {\prime} \big),
$$

received from KA with user, from which the user can use the key modification to achieve the ciphertext

$$
\mathrm{HE.E} \big (\{\mathbf {X} _ {i, 1}, \mathbf {X} _ {i, 2}, \dots \}, k _ {u} ^ {\prime} \big).
$$

However, since $k _ { u } ^ { \prime }$ is unknown to both parties, it is not possible to infer $\mathbf { X } _ { i , 1 } , \mathbf { X } _ { i , 2 } ,$ from the ciphertexts. During the   image search, CS may also share the ciphertexts of the distance with the user, but neither CS nor the user is able to infer the distance from the ciphertext since none of them know the key $k _ { K A }$ .

# 7 IMPLEMENTATION AND EVALUATION

In this section, we first present the implementation of PIC and the datasets used in the experiments, then we evaluate the performance of our basic scheme using SIFT feature vectors and advanced scheme using weighted frequency vector from different aspects. For simplicity, in the following statement, we denote the basic scheme as PIC-sfv and the advanced scheme as PIC-wfv.

# 7.1 System Implementation

We build PIC including both cloud side and client side. On the cloud side, each of KA and CS consists of a cluster of computers with standard distributed file system (Hadoop HDFS) and MapReduce architecture (Hadoop MapReduce). In this evaluation, we use four PCs (Intel Core i3-3240 CPU, 3.4 GHz, 4G RAM) for each cluster. The network bandwidth is 100 Mbps. Each cluster has one name node and three data nodes, which is a small but full-featured data center to demonstrate the feasibility and efficiency of our parallel design. Certainly, the performance can be greatly improved when using more powerful data center [22]. On the client side, we implement our system for both Windows OS laptop and Android phone. In this evaluation, we use a laptop ThinkPad X1 (2.7 GHz CPU, 4 GB RAM), and a mobile phone HTC G17 (1228 Hz CPU, 1 GB RAM). There is also a trusted party that in charge of key generation. In our experiments TP is a single PC with the same hardware as the node of the cluster. Due to the space limitation, in this paper, we omit the evaluation results on the laptop, whose runtime is the same order of magnitude as the Android phone.

We implement all cryptographic components of our system by Java. We use three commonly used descriptors to evaluate the practicality of our system, including 128-dimensional SIFT descriptor [5], 64-SURF and 128- SURF [16], which are highly distinctive and fast to compute. Nevertheless, our schemes are also compatible with other image descriptors. The descriptor extraction is implemented using the OpenCV library for Window and Android. Due to the space limitation, in this paper, we only present the results of the most popular descriptor, 128-SIFT, and 64-SURF and 128-SURF achieve similar performance as using 128-SIFT.

# 7.2 Image Collections and Queries

To explore the performance of our approach in real-life image applications, we evaluate our system with two popular image datasets.

INRIA Holiday dataset (Holiday) [23] contains 1491 personal holidays photos in high resolution (most are 2,560\*1,920). There are 6,767,563 SIFT feature vectors of dimensionality 128 extracted from those images. The dataset contains 500 image groups, each of which represents a distinct scene or object. For the search experiments, the query is a photo of a scene, and the goal is to return other k photos of this scene.   
Flickr image dataset (Flickr1M) [24] contains one million diverse images from Flickr with 1.4 billion precomputed SIFT feature vectors in total. For the search experiments, the query is randomly selected images, and k most similar images are returned.

We analyze the feature vector number of each image in two datasets. The mean feature vector number is 2,200 and 2,988 for Holiday and Flickr1M respectively. Half images have less than 2,000 feature vectors and 80 percent images have less than 5,000 feature vectors.

We evaluate PIC-sfv using SIFT feature vectors from both datasets. For the evaluation of PIC-wfv, 1,000 visual words are learned from 6 K randomly selected images of Flickr1M as the vocabulary. And a 1,000-dimension weighted frequency vector is generated for each image by clients.

# 7.3 Parameter Selection

Before the system evaluation, we analyze the system parameters of clustering algorithm and MHE, and set them to achieve accurate and secure search.

# 7.3.1 Search Parameters Selection

There are three parameters governing the computation, communication and search performance for both schemes, including: (1) The number C of created clusters, which determines delay overhead and search accuracy. Larger C results in a longer clustering process and lower search accuracy, but a smaller search delay. To achieve optimal search quality, We follow the work [7], [17] to set $C = { \sqrt { N } }$ , resulting in $2 \sqrt { N }$ ¼homomorphic distance calculations, where N equals number of feature vectors for PIC-sfv and number of weighted frequency vectors for PIC-wfv. (2) The number k of nearest neighbors, which influence the search accuracy. Voting-based methods are not very sensitive to k for large collections [6], and we set $k = 5$ in our evaluation, which ¼produces good search results (Section .7.6). (3) The nodes numbe $N _ { n o d e }$ in the parallel computation. Existing work like [22] have studied the performance gain as the number of work nodes increases. Based on those work, it is easy to estimate the performance of our system with more computing nodes.

For PIC-wfv, another key parameter is the size of the visual vocabulary v. Larger v yields more accurate search result. It also determines the dimension of the weighted frequency vector for each image. As a result, the computation and communication cost increase linearly with v. Based on the ground truth of Holiday, we set $v = 1 0 0 0$ to optimize ¼the search accuracy (93.4 percent) with acceptable overhead.

TABLE 1 Computation Cost for Each Operation Using a Single PC (s) 

<table><tr><td colspan="4">Common Operations</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Feature Extract</td><td>8.7</td><td>1.56</td><td>12.03</td></tr><tr><td>Parameter Init</td><td>0.002</td><td>0.002</td><td>0.003</td></tr><tr><td>Master Key Gen</td><td>&lt;0.001</td><td>&lt;0.001</td><td>&lt;0.001</td></tr><tr><td>KA&amp;CS Keys Gen</td><td>0.001</td><td>0.001</td><td>0.001</td></tr><tr><td>Triple Keys Gen</td><td>0.002</td><td>0.002</td><td>0.003</td></tr><tr><td>Access Tree Gen</td><td>&lt;0.001</td><td>&lt;0.001</td><td>&lt;0.001</td></tr><tr><td>Decrypt Distance</td><td>&lt;0.001</td><td>&lt;0.001</td><td>&lt;0.001</td></tr><tr><td colspan="4">Operations of PIC-sfv</td></tr><tr><td>Encrypt One SIFT-Vec</td><td>0.034</td><td>0.03</td><td>0.047</td></tr><tr><td>Key Modification (per SIFT-Vec)</td><td>0.052</td><td>0.048</td><td>0.063</td></tr><tr><td>Homomorphic Euclidean Distance</td><td>0.031</td><td>0.029</td><td>0.033</td></tr><tr><td colspan="4">Operation of PIC-wfv</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Freq-Vec Gen</td><td>0.70</td><td>0.005</td><td>3.84</td></tr><tr><td>Encrypt One Freq-Vec</td><td>1.93</td><td>1.59</td><td>2.67</td></tr><tr><td>Key Modification (per Freq-Vec)</td><td>0.29</td><td>0.25</td><td>0.85</td></tr><tr><td>Homomorphic Dot Product</td><td>0.20</td><td>0.18</td><td>0.33</td></tr></table>

$\lambda = 1 2 8 , m = 2 ,$ the SIFT-vec is 128-dimension SIFT feature vector, the Freq-¼ ¼Vec is 1,000-dimension weighted frequency feature vector.

# 7.3.2 Security Parameters Selection

For the MHE, there are two parameters - and m governing the security level and overhead of the system. The system can withstand an attack with up to m ln ploy - chosen ð Þplaintexts, while the communication cost increases linearly with m- and computation cost increases exponentially with m-. As a result, there is a tradeoff between security and efficiency. In our experiments, we choose m=2 and $\lambda = 1 2 8 ,$ , which allows m ln $\lambda ^ { 1 0 } \sim 9 7$ plaintext ¼ attacks with good computation and communication cost. This might be dangerous for local applications, because normally adversaries are allowed to access decryption oracle for a polynomial times, but our system will remain safe since the cloud server will not allow such ”decryption oracle access” for several times.

# 7.4 Micro-Analysis for Each Operation

We analyze the additional computation and communication overhead introduced by our system except the image process related overhead in this section.

# 7.4.1 Computation Overhead

The runtime of each operation is summarized in Table 1 and then the detailed analysis is presented as follows.

![](images/0debacf8d1a90a61b7aef1f1eafc65867b1276fb0a10fc3181c8d391f250a30e.jpg)



Fig. 3. Users’ attribute number distribution of Tencent Weibo.

![](images/0465b5d209b46c7f74bf0ae92e29e935ad2557beac6d797b37104703623677c0.jpg)



Fig. 4. The proportion of Tencent Weibo users having common attributes. The blue line is for all users with different number of attributes. The red line is for those users who have 6 attributes.

Initialization. This operation requires the selection of system parameters for MHE and three random encryption keys $k , k _ { C S } , k _ { K A } ,$ , which are 4 4 matrices, such that $k = k _ { C S } k _ { K A }$ . Both operations are executed at TP side and ¼they takes less than 5 ms in total, which is negligible.

Key Generation & Policy Announcement. In this step, it requires TP to select three random keys $k _ { i } , k _ { i } ^ { \prime } , k _ { i } ^ { \prime \prime }$ such that $k \overset { = } { = } k _ { i } k _ { i } ^ { \prime } k _ { i } ^ { \prime \prime }$ , which costs less than 3 ms. Besides, it also ¼involves an owner’s access tree generation. We evaluate the performance of our access control methods based on the profile data of Tencent Weibo [25], which is one of the largest social networking platform in China. This dataset has 2.32 million users’ personal profiles, including their year of birth, gender, graduate school, profession and other tags. There are 770,166 different attributes in total.Each user has 6 attributes in average and 20 attributes at most, as shown in Fig. 3. Fig. 4 illustrates the proportion of users sharing different number of common attributes. 60 percent users have no common attribute with others, about 20 percent users share one common attribute with others, and 98 percent users share less than four common attributes with others. Our analysis suggests that a small access tree with limited attributes $( \mathrm { e . g . , }$ 6 attributes), is enough to narrow down the size of authorized users (only 0.2 percent is valid), and its generation time is only $8 \times 1 0 ^ { - 3 } \mathrm { m s }$ . Given the access tree, the runtime to authenticate the attributes of a querier is less than 1 ms. So the cost for access control is negligible.

Image Upload. For PIC-sfv, the cluster construction is first executed by each owner, and the runtime increases linearly with the feature vector number (Fig. 5). For two image sets, it takes 20 seconds to cluster feature vectors of 100 randomly selected images. Then the owner encrypts every descriptor using his key ki. As shown in Table 1, it takes 34ms to encrypt each 128 dimension feature vector. The runtime to encrypt the descriptor of each image depends on the its feature vector number as depicted in Fig. 5. Fig. 6 shows runtime to encrypt one image from two images sets, which is 75 s in average. After the ciphertexts are sent to KA, KA conducts a key modification to alter the encryption key of the ciphertexts. As shown in Fig 6, it takes 155 s to modify the key of an image in average. The key modification at CS side is the same operation as KA’s one and thus omitted.

![](images/5e035113cf57fe5fa6bacdf4a17d517c20be12938358b460b9a6216de6b0a805.jpg)



Fig. 5. Runtime of upload operation versus SIFT feature vector number (PIC-sfv).

![](images/6e6ca32694987acc8b358060b9f052e6b81b41bd208919b5707c799644c680ac.jpg)



Fig. 6. CDF of runtime of upload operation for each image in two image sets (PIC-sfv).

For PIC-wfv, based on the visual word vocabulary, the owner generates weight frequency vector for each image, whose runtime is proportional to the feature vector number of this image (Fig. 7). For two image sets, it takes 0.7 s per image in average. Then the owner encrypts the weighted frequency vector of each image, whose runtime is depicted in Fig 8. It takes less than 1.5s to encrypt one image. Fig 8 also presents the time cost of key modification for each image by KA (or CS), which is about 0.29 s.

Privacy Preserving Image Search with Access Control. The querier first encrypts the image descriptor (SIFT feature vectors or one weighted frequency vector), whose run time is the same as the one in the image upload (Figs. 6 and 8). The key modifications by KA and CS are also the same. Besides, in PIC-sfv, CS needs to compute the ciphertexts of all squared Euclidean distances. Using a single machine, each distance takes 31 ms and the whole time cost depends on the number of query feature vectors and the size of searched vectors collection in DB, i.e., #cluster cluster size ð þ Þ
#featurevector 31 ms. In PIC-wfv, CS computes the ciphertexts of all dot products, each takes 200 ms by one machine and the whole time cost just depends on the image collection size, i.e., #cluster cluter size 200 ms. After CS preð þ Þ 
pares all the ciphertexts, KA decrypts them to achieve the distances or dot products, and sort them to find out the NN. For both schemes, each decryption requires less than 1ms and it takes about 0.5s to decrypt 1,000 distances. We use quick-sort to sort the distances, but we omit the run time analysis since this is a standard sorting method. For Holiday, without MapReduce functions, using PIC-sfv each query (with more than 3,000 feature vectors) averagely takes about

![](images/ba6b0bd5929893c23960d116dd1e68b5d2b7c8edb30eb6fc47fdd9db1d53f144.jpg)



Fig. 7. 1,000-dimension weighted frequency vector generation for one image versus feature vector number of this image (PIC-wfv).

![](images/f436fdefaac64a56cd898152b03030be24f50cc12f452afb46e9de31f9d4057a.jpg)



Fig. 8. CDF of runtime of upload operation for each image in two image sets (PIC-wfv).

100 machine-hours to find the matching image among the 1,491 images; using PIC-wfv each query takes about 15 machine-seconds. Deploying our MapReduce implementations on the 4-node small data center, the delay is reduced to about 17 hours for PIC-sfv and reduced to 4 s for PIC-wfv.

As a brief summary, both PIC-sfv and PIC-wfv have same initialization delay and similar runtime for index construction and frequency vector generation. However, PIC-wfv uses only one 1000-dimension weighted frequency vector to represent each image, while in PIC-sfv the descriptor of each image is a set of 128-dimension SIFT feature vectors. When the size of feature vectors is small, two scheme has comparable performance. But as the feature vector size increases, PIC-sfv’s overhead increases linearly while PIC-wfv keeps the runtime almost a constant. Moreover, for the privacypreserving image search, our schemes work excellently with MapReduce framework to reduce the response time.

# 7.4.2 Communication Overhead

We first summarize the size of the transmitted data structure in Table 2. Then we analyze the communication cost for each operation.

Initialization. TP needs to send key $k _ { C S }$ and $k _ { K A }$ to CS and KA respectively, and the mean size of a single key is 0.84 KB.

Key Generation & Policy Announcement. TP sends $k _ { i } , k _ { i } ^ { \prime } k _ { i } ^ { \prime \prime }$ to the user i, CS and KA respectively, and each key’s size is 0.84 KB. Based on the data of Tencent Weibo, the size of the access tree with 6 attributes is about 0.2 KB.

Image Upload. The user informs CS of the change in the index cluster, but it is almost negligible. Main communication overhead comes from the ciphertexts transmission. For PIC-sfv, uploading the encrypted feature vectors incurs #feature vector 64 KB data transmission. For PIC-wfv, the size of ciphertexts (encrypted weighted frequency vector) for each image is 580 KB, which is constant. Similarly, KA also needs to send out the same size ciphertexts to CS.

TABLE 2 Communication Cost of Each Data Structure (KB) 

<table><tr><td colspan="4">Common Data</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Key</td><td>0.84</td><td>0.19</td><td>1.4</td></tr><tr><td>Access Tree</td><td>0.18</td><td>0.03</td><td>0.63</td></tr><tr><td>Encrypted Distance</td><td>0.56</td><td>0.41</td><td>0.65</td></tr><tr><td colspan="4">Data of PIC-sfv</td></tr><tr><td>Encrypted SIFT-Vec</td><td>64</td><td>62.8</td><td>65.1</td></tr><tr><td colspan="4">Data of PIC-wfv</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Encrypted Freq-Vec</td><td>580</td><td>578.9</td><td>581.2</td></tr></table>

$\lambda = 1 2 8 , m = 2 ,$ , the SIFT-vec is 128-dimension SIFT feature vector, the Freq-¼ ¼Vec is 1,000-dimension weighted frequency feature vector.

![](images/9184d730cc210daefaaa040308df996e4538658ea3cad4b6ff23e2ddfcb84e0e.jpg)



Fig. 9. Computation overhead distribution among CS, KA and client for a single query.

Privacy Preserving Image Search with Access Control. First, the querier encrypts the query descriptor and sends the corresponding ciphertexts to KA, which is

#feature vector 64KB for PIC-sfv and 580 KB for PICwfv. KA also sends the same amount of ciphertexts to CS. For PIC-sfv, in the level-1 search, after CS computes the encrypted distances for all representatives, the encrypted distances are sent back to KA, the size is 0.56 KB each and the whole size is #cluster 0:56 KB. During the level-2 search, CS computes the encrypted distances for all vectors within the NN’s cluster, and sends them to KA (cluster size 0:56 KB). For PIC-wfv, similarly, CS computes and send all encrypted dot products to KA, whose size is #cluster cluster size 0:56KB. For Holiday, the ð þ Þ 
transmitted data between CS and KA during search is about 2,800 KB for two rounds search of PIC-sfv and 43 KB for PIC-wfv.

# 7.5 Macro-Analysis for Each Entity

We analyze the overall computation overhead for each entity in this section. Similarly, we only analyze the additional overhead except the image process related one.

Cloud Server. The computational delay at CS side during the image upload comes from key modification. In PIC-sfv, it is #feature vector 52ms (Fig. 5) and about 200 s for 80 percent images (Fig. 6). Using PIC-wfv, it takes about 1.2s for 80 percent images. During the image search, the computation cost of CS comes from the homomorphic distance calculation. For a single node, the cost is #cluster cluter size ð þ Þ
#feature vector 31 ms using PIC-sfv and #cluster cluter size 200 ms using PIC-wfv.

Þ 
Key Agent. KA experiences the same delay as CS during the image upload. The computation cost of KA during search comes from decrypting all distances and ranking them to find the NN. The run time is 0.5 s to process 1,000 distances.

Client. The computational delays occur during the system join, image upload and the image search for an ordinary user. The system join cost is negligible (about 3 ms). In PICsfv, the clustering cost is negligible compared to the encryption cost, and encryption cost is #feature vector 34 ms (Fig. 5). So the computational delay of upload is about 100 s for 80 percent images from the two image sets (Fig. 6). Similarly, for PIC-wfv, the computational delay during upload for 80 percent images is only about 2.2 s and 1.5 s in average (Fig. 8). During search, the client does nothing but waits for the search result from the cloud and the delay is summation of the computational delay at CS and KA.

In summary, for a querier, after providing a query image, the response time is mainly the computational delay accumulation of image encryption, two key modifications, homomorphic distance calculation, distance decryption and ranking. When the querier can access all 1,491 images of Holiday on the cloud, the average response time of each query is about 17 hours and 8 minutes for PIC-sfv and 7.21 seconds for PIC-wfv. Here the delay can be greatly reduced as the cloud scales up from 4 nodes to hundreds of nodes. Besides, compared to exiting multi-part secure computation based methods, by our approach, during the search no interaction is required for the client and 97 percent computation is carried out by CS, leaving KA and clients very limited overhead (Fig. 9).

# 7.6 Performance Comparison

Compare with Alternative Methods. [18] has compared its cost against the well-known homomorphic encryption scheme of Gentry [26]. Gentry’s scheme needs more than 900 seconds to add two 32 bit numbers, and more than 67,000 seconds for the multiplication, but the cost for [18] is only 0.1 ms and 108 ms respectively. The reason is that Gentry’s fully homomorphic encryption is based on the ”learning with errors” (LWE) problems in lattice system, which allows users to apply as many multiplications as they want on the ciphertexts. [18] is based on number theory and group theory, which only supports a limited number of homomorphic operations, but is sufficient for our application. So, [18] is much more practical and compact. We also realize private Euclidean distance computation using a partial homomorphic encryption (Paillier encryption) in the SMC manner (e.g., the method used in [21]). Using the same computer and test images, the Paillier-based (128 bit) takes about 0.5 s for feature vector encryption and 0.18 s for homomorphic distance computation. For Paillier-based method with 1,024 bit key or 2,048 bit key, it takes much longer time for distance computation. But in our work, they take only 0.034 s and 0.031 s respectively. The comparison shows the computation efficiency of our system.

Search Accuracy. First, we evaluate the search accuracy of our approaches according to the ground truth of 500 queries of Holiday. With k=5 (five nearest neighbors are fetched), the accuracy of PIC-sfv is 95.2 percent and of PIC-wfv is 93.4 percent. Here the accuracy is the success rate of 500 queries. A result is success if the returned k images contain at least one image from the same scene as the query image. So, our solution achieves privacy-preserving without sacrificing the search accuracy. When a vocabulary is learnt, PIC-wfv provides the similarly good accuracy as PIC-sfv.

Linear Search Versus Our Approaches with MapReduce. We implement the SIFT feature vector based scheme and the visual word based scheme using the Hadoop MapReduce framework to accelerate the search. To study the search efficiency of different schemes, we compare the computational overhead of our two schemes using a 4-node cluster with the one of conducting a linear search using a single computer on the raw images data. The comparison is presented at Fig. 10, which shows the overhead is reduced an order of magnitude by the SIFT feature vector based approach. Further more, the visual word based approach keeps the overhead a second-level constant.

![](images/97ac2bf30a43b58bf1258cc904c96cd95c160e582d87c38c3ca3cb32675900fe.jpg)



Fig. 10. Search time using different approaches versus feature vector number of the query image. Two different size searched image collections (1 K and 10 K) are selected randomly from Flickr1M.

Then we evaluate the improvement caused by adapting our privacy-preserving search to MapReduce framework. We run the 500 queries on the encrypted Holiday data set. With a single computer, the cluster based approach takes about 100 hours for each query, and the visual word based approach takes 15 seconds for each query. When running on the 4-node small cluster with our MapReduce adaptive implementation, the runtime reduces from 100 to 17 hours and from 15 seconds to 4s respectively. With a large cluster, the improvement will be much bigger.

With Versus Without Privacy Protection. By running the visual word based search on Holiday on the 4-node cluster in two cases, where all computation in the first case is conducted on the raw image data and all computation in the second case is conducted on ciphertexts as our system design. In the first case, the average response time for each query is 1.8 s and in the second case, that is 4 s. This slowdown is caused by image encryption, key modifications, homomorphic distance calculation, distance decryption. The result shows that our system provides good protection to the image privacy with reasonable extra overhead.

As a conclusion, leveraging the power of indexing and MapReduce, our system design improves the search performance greatly while keep a high search accuracy and well protected privacy.

# 8 RELATED WORK

# 8.1 Image Indexing and Search

There are numerous works addressing searching for similar images, and most of them are based on the local invariant descriptors. Typically, high-dimensional descriptors are extracted from the interest regions of images to represent the visual characteristics. Different types of descriptors are proposed to achieve efficient and accurate image matching result, e.g., SIFT [5] and SURF [16]. The 128 dimension SIFT descriptor is most widely used for image search due to its distinctiveness and computational efficiency. Usually, content-based video search can be reduced to some sort of key frame search. For example, Video Google [1] proposes an approach to search a user outlined object in videos using the pre-computed descriptor of the object. The search result is a ranked list of key frames. The most accurate approach to search similar images is to conduct the nearest neighbor search among image descriptors. But one high-resolution image is usually described by thousands of feature vectors and many image retrieval systems manage millions of images. Facing billions of high-dimensional vectors, the accurate nearest neighbor search is too expensive. Various feature vector indexing approaches are designed to boost up the search efficiency, e.g., cluster pruning [17] and extended cluster pruning [7]. Extended cluster pruning [7] provides a promising way for efficient clusters construction and queries processing, which outperforms comparable solutions, like p-sphere tree [27] and rank aggregation [28]. FAST [29] supports near-real-time semantic queries on cloud storage system via correlation-aware hashing and manageable flat-structured addressing. Recently, a lot of work speed up the search process based on visual words e.g., [6], which somewhat decrease the search accuracy. As commercial data center get more and more popular, it is also possible to improve the large-scale image search using parallelize computing. There are some work using MapReduce [30] to accelerate the indexing and search process, e.g., [31]. However, few of image indexing and search systems consider privacy protection of the image owner and querier.

# 8.2 Image Privacy Protection

There are some applications protecting image privacy by simply encrypting the image or blacking out private content, e.g., human face. [32] removes facial characteristics from the video frame to protect the face privacy of individuals in video surveillance. P3 [33] proposes a privacy preserving photo sharing scheme by separating an image into private part and public part. Both [32] and P3 only support privacy protection in image storage, leaving the result image of limited use and no image search is supported for the private image. GigaSight [34] proposes an Internet system for collection of crowd-sourced video from mobile devices, which blacks out sensitive information from video frames. For search purpose, each frame is analyzed by computer vision code to obtain tags as the index. Securing SIFT [35] proposes to extract feature over massive encrypted image data. [36] designs techniques to detect private images by learning privacy classifiers trained on a dataset of manually assessed Flickr photos. [37] uses kNN to protect feature vectors and a standard stream cipher to protect image pixels. Those work offer techniques to protect image privacy, but cannot support image similarity based search and the indices also expose sensitive information. [38] uses IES-CBIR to achieve encrypted storage and searching of images while preserving privacy. However, it cannot provide efficient search over large-scale image datasets.

# 8.3 Secure Multi-Part Computation

The core of content-based image search is measuring the distance between vectors. There are many existing methods addressing privacy-preserving vector distance among parties using secure multi-party computation (SMC) [13], [14], [15]. There are some work providing privacy-preserving image matching using classic homomorphic encryption, e.g., [10] and [11]. Those methods provide privacy protection to the query image as well as the outcome of the matching algorithm, but the result is not secure against the service provider. They all require rounds of online interactions with users during the search and incur expensive computation cost, so none of them can be scaled to address largescale image sets. Zhang et al. [39] designs a symmetric encryption method based attribute matching protocol for distributed social networking systems. Recently, Xiao et al. propose an efficient homomorphic encryption protocol for multi-user system [18]. It is a non-circuit based symmetrickey homomorphic encryption scheme, whose security is equivalent to the large integer factorization problem. We employ this protocol to design our system.

# 8.4 Searchable Symmetric Encryption

To ensure the security, text documents are usually encrypted before uploading to cloud. Searchable symmetric encryption (SSE) is proposed to search over encrypted text documents or image through keywords/tags. Curtmola et.al. [40] propose a thorough discussion on the framework of SSE. Cong et.al. extend the framework to ranked keyword search [9]. [41] presents a keyword-based semantic search framework for encrypted cloud data by generating metadata for each file. Existing SSE approaches only support search encrypted keywords by accurately matching. They cannot measure distance of encrypted vectors, thus cannot support content-based image search.

# 9 CONCLUSION

We have presented a novel system PIC towards privacy preserving content-based search on large-scale outsourced images. With our careful design, the majority of the computationally intensive image matching jobs are outsourced to the cloud in a non-interactive way, but the image and query privacy is preserved. To further expedite the search process, we enable the cloud to maintain the index structure and parallelize the search process without learning anything. We implement our prototype system using Hadoop MapReduce framework in a computer cluster, and our experiment results show the efficiency and the applicability of our system in a cloud platform.

# ACKNOWLEDGMENTS

The research is supported in part by NSF China under Grants No. 61572281, No. 61472218, No. 61502271. The research of Li is partially supported by China National Funds for Distinguished Young Scientists with No. 61625205,Key Research Program of Frontier Sciences, CAS, No. QYZDY-SSW-JSC002, NSFC with No. 61520106007, NSF ECCS-1247944, NSF CMMI 1436786, and NSF CNS 1526638.

# REFERENCES

[1] J. Sivic and A. Zisserman, “Video google: A text retrieval approach to object matching in videos,” in Proc. 9th IEEE Int. Conf. Comput. Vis., 2003, Art. no. 1470.   
[2] C. Bo, G. Shen, J. Liu, X.-Y. Li, Y. Zhang, and F. Zhao, “Privacy. tag: Privacy concern expressed and respected,” in Proc. 12th ACM Conf. Embedded Netw. Sens. Syst., 2014, pp. 163–176.   
[3] L. Zhang, K. Liu, X.-Y. Li, C. Liu, X. Ding, and Y. Liu, “Privacyfriendly photo capturing and sharing system,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., 2016, pp. 524–534.   
[4] P. Weinzaepfel, H. J-egou, and P. P-erez, “Reconstructing an image from its local descriptors,” in Proc. IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recog., 2011, pp. 337–344.

[5] D. G. Lowe, “Distinctive image features from scale-invariant keypoints,” Int. J. Comput. Vis., vol. 60, pp. 91–110, 2004.   
[6] H. J-egou, M. Douze, and C. Schmid, “Improving bag-of-features for large scale image search,” Int. J. Comput. Vis., vol. 87, pp. 316–336, 2010.   
[7] G. P. Gudmundsson, B. P. Jonsson, and L. Amsaleg, “A large-scaleperformance study of cluster-based high-dimensional indexing,” in Proc. Int. Workshop Very-Large-Scale Multimedia Corpus, Mining Retrieval, 2010, pp. 31–36.   
[8] M. Daneshi and J. Guo, “Image reconstruction based on local feature descriptors,” 2011.   
[9] C. Wang, N. Cao, K. Ren, and W. Lou, “Enabling secure and efficient ranked keyword search over outsourced cloud data,” IEEE Trans. Parallel Distrib. Syst., vol. 23, no. 8, pp. 1467–1479, 2012.   
[10] Z. Erkin, M. Franz, J. Guajardo, S. Katzenbeisser, I. Lagendijk, and T. Toft, “Privacy-preserving face recognition,” in Proc. 9th Int. Symp. Privacy Enhancing Technol., 2009, pp. 235–253.   
[11] A.-R. Sadeghi, T. Schneider, and I. Wehrenberg, “Efficient privacypreserving face recognition,” in Int. Conf. Inf. Security Cryptology, 2009, pp. 229–244.   
[12] L. Zhang, T. Jung, C. Liu, X. Ding, X.-Y. Li, and Y. Liu, “Pop: Privacy-preserving outsourced photo sharing and searching for mobile devices,” in Proc. IEEE 35th Int. Conf. Distrib. Comput. Syst., 2015, pp. 308–317.   
[13] T. Jung, X.-Y. Li, and S. Tang, “Privacy-preserving data aggregation without secure channel: Multivariate polynomial evaluation,” in Proc. 32nd IEEE Conf. Comput. Commun., 2013, pp. 2634–2642.   
[14] L. Zhang, X.-Y. Li, Y. Liu, and T. Jung, “Verifiable private multiparty computation: Ranging and ranking,” in Proc. IEEE INFO-COM, 2013, pp. 605–609.   
[15] T. Jung, X.-Y. Li, and M. Wan, “Collusion-tolerable privacypreserving sum and product calculation without secure channel,” in Proc. IEEE Trans. Dependable Secure Comput., 2014, pp. 45–57.   
[16] H. Bay, A. Ess, T. Tuytelaars, and L. Van Gool , “Speeded-up robust features (SURF),” Comput. Vis. Image Understanding, vol. 110, no. 3, pp. 346–359, 2008.   
[17] F. Chierichetti, A. Panconesi, P. Raghavan, M. Sozio, A. Tiberi, and E. Upfal, “Finding near neighbors through cluster pruning,” in Proc. 26th ACM SIGMOD-SIGACT-SIGART Symp. Principles Database Syst., 2007, pp. 103–112.   
[18] L. Xiao, O. Bastani, and I.-L. Yen, “An efficient homomorphic encryption protocol for multi-user systems,” IACR Cryptology ePrint Archive, vol. 2012, 2012, Art. no. 193.   
[19] R. Yates, “Fixed-point arithmetic: An introduction,” Digital Signal Labs, vol. 81, no. 83, 2009, Art. no. 198.   
[20] J. Bethencourt, A. Sahai, and B. Waters, “Ciphertext-policy attribute-based encryption,” in Proc. IEEE Symp. Security Privacy, 2007, pp. 321–334.   
[21] J. Katz, A. Sahai, and B. Waters, “Predicate encryption supporting disjunctions, polynomial equations, and inner products,” in Proc. Theory Appl. Cryptographic Tech. 27th Annu. Int. Conf. Adv. Cryptology, 2008, pp. 146–162.   
[22] A. Sangroya, D. Serrano, and S. Bouchenak, “Benchmarking dependability of mapreduce systems,” in Proc. IEEE 31st Symp. Rel. Distrib. Syst., 2012, pp. 21–30.   
[23] H. Jegou, M. Douze, and C. Schmid, “Hamming embedding and weak geometric consistency for large scale image search,” in Proc. 10th Eur. Conf. Comput. Vis., 2008, pp. 304–317.   
[24] “Flickr1m dataset,” [Online]. Available: http://www.multimedia -computing.de/wiki/Flickr1M   
[25] “Tencent weibo,” [Online]. Available: http://t.qq.com/   
[26] C. Gentry, “Fully homomorphic encryption using ideal lattices,” in Proc. 41st Annu. ACM Symp. Theory Comput., 2009, pp. 169–178.   
[27] J. Goldstein and R. Ramakrishnan, “Contrast plots and p-sphere trees: Space versus time in nearest neighbour searches,” in Proc. 26th Int. Conf. Very Large Data Bases, 2000, pp. 429–440.   
[28] C. Dwork, R. Kumar, M. Naor, and D. Sivakumar, “Rank aggregation methods for the web,” in Proc. 10th Int. Conf. World Wide Web, 2001, pp. 613–622.   
[29] Y. Hua, H. Jiang, and D. Feng, “Real-time semantic search using approximate methodology for large-scale storage systems,” IEEE Trans. Parallel Distrib. Syst., vol. 27, no. 4, pp. 1212–1225, Apr. 2016.   
[30] J. Dean and S. Ghemawat, “Mapreduce: Simplified data processing on large clusters,” Commun. ACM, vol. 51, no. 1, pp. 107–113, 2008.   
[31] D. Moise, D. Shestakov, G. Gudmundsson, and L. Amsaleg, “Indexing and searching 100 m images with MapReduce,” in Proc. 3rd ACM Int. Conf. Multimedia Retrieval, 2013, pp. 17–24.

[32] E. M. Newton, L. Sweeney, and B. Malin, “Preserving privacy by de-identifying face images,” IEEE Trans. Knowl. Data Eng., vol. 17, no. 2, pp. 232–243, Feb. 2005.   
[33] M.-R. Ra, R. Govindan, and A. Ortega, “P3: Toward privacypreserving photo sharing,” in Proc. 10th USENIX Conf. Netw. Syst. Des. Implementation, 2013, pp. 515–528.   
[34] P. Simoens, Y. Xiao, P. Pillai, Z. Chen, K. Ha, and M. Satyanarayanan, “Scalable crowd-sourcing of video from mobile devices,” in Proc. 11th Annual Int. Conf. Mobile Syst. Appl. Serv., 2013, pp. 139–152.   
[35] S. Hu, Q. Wang, J. Wang, Z. Qin, and K. Ren, “Securing sift: Privacy-preserving outsourcing computation of feature extractions over encrypted image data,” IEEE Trans. Image Process., vol. 25, no. 7, pp. 3411–3425, Jul. 2016.   
[36] S. Zerr, S. Siersdorfer, J. Hare, and E. Demidova, “Privacy-aware image classification and search,” in Proc. 35th Int. ACM SIGIR Conf. Res. Develop. Inf. Retrieval, 2012, pp. 35–44.   
[37] Z. Xia, X. Wang, L. Zhang, Z. Qin, X. Sun, and K. Ren, “A privacypreserving and copy-deterrence content-based image retrieval scheme in cloud computing,” IEEE Trans. Inf. Forensics Security, vol. 11, no. 11, pp. 2594–2608, Nov. 2016.   
[38] B. Ferreira, J. Rodrigues, J. Leit ?o, and H. Domingos, “Privacypreserving content-based image retrieval in the cloud,” in Proc. IEEE 34th Symp. Rel. Distrib. Syst., Sep. 2015, pp. 11–20.   
[39] L. Zhang, X.-Y. Li, K. Liu, T. Jung, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in mobile social networks,” IEEE Trans. Mobile Comput., vol. 14, no. 9, pp. 1888– 1902, Sep. 2015.   
[40] R. Curtmola, J. Garay, S. Kamara, and R. Ostrovsky, “Searchable symmetric encryption: Improved definitions and efficient constructions,” in Proc. 13th ACM Conf. Comput. Commun. Security, 2006, pp. 79–88.   
[41] Z. Xia, Y. Zhu, X. Sun, and L. Chen, “Secure semantic expansion based search over encrypted cloud data supporting similarity ranking,” J. Cloud Comput., vol. 3, no. 1, 2014, Art. no. 8.

![](images/c69d34bad15762750d015af2b13a5c6acff0b6f0bd77e64f4560d940a430e375.jpg)



Lan Zhang received her bachelor’s degree from School of Software at Tsinghua University, China, in (2007) and the PhD degreefrom the department of Computer Science and Technology, Tsinghua University, China, in (2014). She is currently a distinguished researcher at the School of Computer Science and Technology, at University of Science and Technology of China. Her research interests span privacy protection, secure multi-party computation and mobile computing, etc. She is a member of the IEEE.

![](images/609abbb95f9353a9674d10b30ba65917163de751e37e73210979f1ecdc446037.jpg)



Taeho Jung received the BE degree in computer software from Tsinghua University, Beijing, in 2007, and he is working toward the PhD degree in computer science at Illinois Institute of Technology. His research area, in general, includes privacy & security issues in mobile network and social network analysis. Specifically, he is currently working on the privacy-preserving computation in various applications and scenarios. He is a student member of the IEEE.

![](images/f23afb51c19f396722937af34ac4fb0b6ef42a4ba5ad3b65fb5916ea78a0ce7b.jpg)



Kebin Liu received the BS degree in Department of computer science from Tongji University, in 2004, and the MS and PhD degrees from Shanghai Jiaotong University, in 2007 and 2010. He is currently an assistant researcher in the School of Software and TNLIST, Tsinghua University. His research interests include WSNs and distributed systems. He is a member of the IEEE.

![](images/d2f491be3e17eadc53b2f103f25d973f8e5b57f5b532db73dbfda5b400a02f1a.jpg)



Xiang-Yang Li received the MS (2000) and the PhD (2001) degree at Department of Computer Science, University of Illinois at Urbana-Champaign, the bachelor degree at Department of Computer Science and a Bachelor degree at Department of Business Management, Tsinghua University, China, both in 1995. He is a full professor at School of computer science and technology, University of Science and Techonology of China, Hefei, China. His research interests include wireless networking, mobile computing, and security and privacy. He is a fellow of the IEEE and an ACM distinguished scientist.

![](images/c29761dc1eefbfd3627753638357741217e19a65703da0ff5618279ec835edde.jpg)



Xuan Ding received his bachelor’s degree from School of Software at Tsinghua University, China, in (2008) and the PhD degreefrom the department of Computer Science and Technology, Tsinghua University, China, in (2014). He is now a post doctor in the School of Software, Tsinghua University, China. His research interests span social networking privacy, privacyaware computing and data analysis, etc.

![](images/84f4c0c3304bd4854c6c0b42439ffe46ef35cec885133afc2f58ca73003458ff.jpg)



Jiaxi Gu received the bachelor’s degree from School of Computer Science and Technology at Northwestern Polytechnical University, China, in (2014). He is currently working towards the PhD degree from School of Computer Science and Technology, Northwestern Polytechnical University, China. His research interests span ubiquitous computing, privacy-aware computing and etc.

![](images/5325db6245f8be759688c9753d2ce426a8d6dfac9c5aa554c8b918d29d108452.jpg)



Yunhao Liu received the BS degree in Automation Department, Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering at Michigan State University in 2003 and 2004, respectively. He is now Chang Jiang professor and Dean of School of Software, Tsinghua University, China. He is a fellow of the IEEE.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.