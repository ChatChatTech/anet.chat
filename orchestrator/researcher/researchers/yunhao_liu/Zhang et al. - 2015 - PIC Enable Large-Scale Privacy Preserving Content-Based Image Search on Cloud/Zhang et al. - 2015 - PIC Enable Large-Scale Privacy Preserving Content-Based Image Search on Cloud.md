# PIC: Enable Large-scale Privacy Preserving Content-based Image Search on Cloud

Lan Zhang $^{*}$ , Taeho Jung $^{\dagger}$ , Puchun Feng $^{*}$ , Kebin Liu $^{*}$ , Xiang-Yang Li $^{\dagger}$ , Yunhao Liu $^{*}$

\*School of Software, Tsinghua University

$^{\dagger}$ Department of Computer Science, Illinois Institute of Technology

Abstract—Many cloud platforms emerge to meet urgent requirements for large-volume personal image store, sharing and search. Though most would agree that images contain rich sensitive information (e.g., people, location and event) and people's privacy concerns hinder their participation into untrusted services, today's cloud platforms provide little support for image privacy protection. Facing large-scale images from multiple users, it is extremely challenging for the cloud to maintain the index structure and schedule parallel computation without learning anything about the image content and indices. In this work, we introduce a novel system PIC: a Privacy-preserving Image search system on Cloud, which is a step towards feasible cloud services which provide secure content-based large-scale image search with fine-grained access control. Users can search on others' images if they are authorized by the image owners. Majority of the computationally intensive jobs are handled by the cloud, and a querier can now simply send the query and receive the result. Specially, to deal with massive images, we design our system suitable for distributed and parallel computation and introduce several optimizations to further expedite the search process. Our security analysis and prototype system evaluation results show that PIC successfully protects the image privacy at a low cost of computation and communication.

Keywords-large-scale image search; privacy preserving; map-reduce ;

# I. INTRODUCTION

As on-board cameras get more and more popular, numerous high-resolution photos are generated every day, which makes storing, sharing and especially searching large-scale images become challenging. Increasing number of service providers support cloud based image services, e.g. Amazon Cloud Drive, Apple iCloud, Cloudinary, Flicker and Google. Content-based image search is a core functionality for various image applications, e.g., personal image management, criminal investigation using crowdsourced photos (e.g. the Boston Marathon investigation) and medical image study and diagnosis. However, there are a lot of sensitive information in images, and increasing worry about privacy could hinder many potential useful image services $[1]$ . For example, the face search functionality of Facebook has been abandoned for two years due to the privacy concern from users and governments. While leveraging the power of cloud and crowdsourcing, the image owner requires the right to protect his/her images from

![](images/41d7a01621dec4b5dc07c5b710883ef66fee5d86b6caf2500293255e74b30dfe.jpg)



(a) Compare original image and reconstructed image using SIFT feature vector. [2]

![](images/d8eaef41ac9fd36b5cb4d9f34aad2744198474d2d3afc92b24313cd31f46b8ca.jpg)



(b) Feature vector detection and matching results between original image and reconstructed image.   
Fig. 1. Comparison between original image and images reconstructed from feature vectors.

any unauthorized parties (including the service provider), meanwhile keep the ability to search all authorized images.

State-of-the-art image search systems typically extract distinctive feature descriptors (high-dimension feature vectors) from interest points of images to measure their content similarity, e.g. 128-dimensional SIFT [3]. One image is usually described by hundreds of feature vectors (as shown Figure 1), and millions of photos uploaded to the cloud imply billions of feature vectors. Therefore, it is necessary to introduce optimization techniques such as indexing or distributed computing to accelerate the search process, e.g. [4], [5]. But most previous efforts did not support image privacy protection or assumed that feature vectors do not reveal content of images. However, recent researches show that an image can be approximately reconstructed based on the output of a blackbox feature descriptor software such as those classically used for image indexing [2], [6]. As presented in Figure 1, the image reconstructed using SIFT feature vectors appears quite similar as the original image, and shows a good match with the original one, which arouses great concerns on the image content privacy in the image indexing and search systems.

As a result, large-scale outsourced personal images need efficient yet private content-based search urgently. Some existing systems $[7]$ tag images with keywords and metadata, and search the occurrences of encrypted tags in an exact match manner. Those systems cannot support content-based image search, whose core is measuring distances between vision feature vectors. Some systems use homomorphic encryption to achieve private vector distance measurement, but reveal search results to the cloud and cost expensive computation, e.g., [8] and [9]. PoP [10] supports privacy-preserving outsourced photo search, but it cannot deal with massive images.

To implement a desired privacy-friendly image search platform, we need to address several critical challenges. First, the search process should be completed in a non-interactive way, and all storage and majority of computation should be outsourced to the cloud, while the cloud cannot learn the images, feature vectors and search results. Second, a user should be able to search freely on all his/her authorized images on the cloud, which could be encrypted by keys from multiple owners. Third, facing large image sets, the cloud should leverage the power of indexing and parallel computing using encrypted data. Traditional secure multi-party computation (SMC) [11]–[13], or simple homomorphic encryption ([8], [9]) cannot be the solution to the large-scale image search problem. On one hand, the garbled circuit's size is exponentially greater than the size of the input, which is often very large in image search, so the communication and computation overhead is beyond practicality. On the other hand, a simple homomorphic will allow the decrypter of the final result to also decrypt the ciphertext of image content. Moreover, both of them may lead to rounds of interactions among the image owner, cloud server and the querier, and the image owners need to always stay online. Besides, they cannot support key conversion or parallel computation. Therefore, we design a novel system PIC: a Privacy-preserving Image search system on Cloud using lightweight multi-level homomorphic encryption as a building block to implement an efficient non-interactive image search outsourcing. The main contributions of this work are summarized as follows:

\- We propose a whole novel system and techniques towards feasible private feature-based image search upon large-scale encrypted images with untrusted servers. Our system also supports privacy-preserving image storage and sharing among users. Users can search on others' images if they are authorized by the image owners. Our system outsources the majority of the search job to the cloud side, but neither the image content nor the query is revealed to the cloud. What's more, during the search, no interaction is required between the data owner and the querier or the cloud.

\- Our private search mechanism is compatible with the state-of-the-art image search to guarantee the search accuracy. We also carefully design our system to make it suitable for distributed or parallel computation and introduce several optimizations to boost large-scale image search without privacy loss. Especially, we implement our privacy-preserving image storage, sharing and search in Hadoop MapReduce system.

\- We evaluate our system using more than one million highly diverse real-life photos. Our implementation shows the efficiency of our system that allows the system to be used in a wide range of platforms including resource-bounded ones.

# II. PRELIMINARY

We address the problem of efficient large-scale image searching with cloud servers. Different from existing work focusing on the search efficiency, we also consider the image privacy (the image itself and its feature descriptors) of the image owner and the query privacy (the query image content and the query result) of the querier.

# A. Large Scale Image Search

To guarantee the search accuracy, we employ the state-of-the-art large-scale image search model in the computer vision field. Here, we briefly review it.

In the field of computer vision, feature descriptor is widely adopted for image similarity measurement. Given an image I, interest points are detected and one feature vector $x_{i}$ is extracted for each interest point to indicate the appearance characteristics around this point. The image's feature descriptor consists of all extracted feature vectors, denoted as $X := \{x_{1}, \ldots, x_{\alpha}\}$ . To achieve robust and fast image description, different types of descriptors are proposed, e.g., SIFT [3] and SURF [14]. Given a specific type of descriptor, feature vectors are usually of the same dimension, e.g., the SIFT vector is 128-dimension.

1) Voting-based Search Model: Many modern content-based image retrieval systems manage millions of images, i.e., billions of high-dimension feature vectors. Given a query descriptor $X := \{x_{1}, \ldots, x_{\alpha}\}$ of the query image $I_{x}$ , and a set of descriptors $\{Y^{1}, \cdots, Y^{N}\}$ of images in the big database, where $Y^{n}$ is the descriptor of the n-th image, existing solutions (e.g., [4] and [5]) usually search similar images of $I_{x}$ as follows:

1. Let the score of each image in database be $S^n$ , and initialize all scores to 0.

2. For each feature vector $x_{i}$ of X and for each feature vector $y_{j}^{n}$ in database, the score $S^{n}$ is increased by $S^{n} := S^{n} + \delta(\mathbf{x}_{i}, \mathbf{y}_{j}^{n})$ , where $\delta(\mathbf{x}_{i}, \mathbf{y}_{j}^{n})$ is the matching function measuring the similarity between feature vector $x_{i}$ and $y_{j}^{n}$ based on k-nearest neighbors. Formally, the matching function is defined as

$$
\delta \left(\mathbf {x} _ {i}, \mathbf {y} _ {j} ^ {n}\right) = \left\{ \begin{array}{l l} 1 & \text { if } \mathbf {y} _ {j} ^ {n} \text { is   a } k \text {-NN of } \mathbf {x} _ {i} \\ 0 & \text { otherwise } \end{array} \right. \tag {1}
$$

For the k-NNs search, the dissimilarity of feature vectors are typically measured by Euclidean distance.

3. By ranking the image scores, images with largest scores are selected as the matched images of the query image.

2) Indexing-based Approximate k-NNs Search: A very large number of feature vectors make the accurate k-nearest neighbors (k-NNs) search too expensive. Approximate search greatly improves the performance with a little loss of accuracy. The most common way is indexing large-scale feature vectors by partitioning them into groups using high-dimensional clustering, e.g., [15] and [5]. Given a query feature vector, the system firstly finds the closest cluster header, and then distances between the query vector and the cluster members are computed to get the k-NNs. As a result, many clusters can be pruned quickly to accelerate the searching process.

# B. Multi-level Homomorphic Encryption (HE)

To implement efficient non-interactive image search and outsource the index maintenance to the cloud side, we need a light-weight encryption method which supports both homomorphic computing and key conversion. We carefully explore existing encryption protocols and employ a multi-level homomorphic encryption protocol presented by Xiao et al. [16]. The protocol is defined as follows:

Definition 1: The multi-level homomorphic encryption is defined by three algorithms $(K,\mathsf{HE.E},\mathsf{HE.D})$ , where K,HE.E and HE.D are the key generation, encryption and decryption algorithms, and it satisfies HE.D(HE.E(m,k)) = m given $k \leftarrow K(1^{\lambda})$ .

We review the design and security proof of this protocol, and make sure it is correct. Notably, we utilize the following good properties of this protocol in our work:

# Additive and Multiplicative Homomorphism:

$$
\mathrm{HE}. \mathrm{E} (m _ {1}, k) \cdot \mathrm{HE}. \mathrm{E} (m _ {2}, k) = \mathrm{HE}. \mathrm{E} (m _ {1} m _ {2}, k)
$$

$$
\mathrm{HE}. \mathrm{E} (m _ {1}, k) + \mathrm{HE}. \mathrm{E} (m _ {2}, k) = \mathrm{HE}. \mathrm{E} (m _ {1} + m _ {2}, k)
$$

This also implies the homomorphism over any polynomial function $f$ , i.e.,

$$
\begin{array}{l} f \left(\mathrm{HE.E} \left(m _ {1}, k\right), \mathrm{HE.E} \left(m _ {2}, k\right), \dots , \mathrm{HE.E} \left(m _ {l}, k\right)\right) \\ = \mathrm{HE.E} (f (m _ {1}, m _ {2}, \dots , m _ {l}), k) \\ \end{array}
$$

Key Conversion: If we have $k = \prod_{i} k_{i}$ for the key $k$ , the encryption has the following property:

$$
\left(\prod_ {i} k _ {i} ^ {- 1}\right) \cdot E (m, 1) \cdot \left(\prod_ {i} k _ {i}\right) = E (m, \prod_ {i} k _ {i}) = \mathrm{HE}. \mathrm{E} (m, k)
$$

This implies that one does not need to decrypt and re-encrypt the message to alter the key of a ciphertext, which is very useful in our system design. Note that a randomizer is omitted for the sake of simplicity, so it is not possible to attack this encryption via brute-force search if the ciphertext size is large enough.

# C. Distance Calculation via HE

We can conduct the distance calculation for two feature vectors x, y on the ciphertexts as follows, where $\mathbf{x}(j)$ refers to the j-th dimension of the feature vector x, and $\mathrm{D}(\mathbf{x}, \mathbf{y}) = \mathrm{d}^{2}(\mathbf{x}, \mathbf{y})$ .

$$
\mathrm{HE.E} (\mathrm{D} (\mathbf {x}, \mathbf {y}), k) = \sum_ {k} (\mathrm{HE.E} (\mathbf {x} (j), k) - \mathrm{HE.E} (\mathbf {y} (j), k)) ^ {2}
$$

Then, the distance calculation can be outsourced to anyone who does not know the key on ciphertexts and neither the feature vectors nor the calculation output will be revealed. Hereafter, we use the notation $\phi_{D}(\cdot)$ to denote the function which conducts distance calculation given homomorphic ciphertexts of two vectors. That is:

$$
\phi_ {D} \left(\mathrm{HE.E} (\mathbf {x}, k), \mathrm{HE.E} (\mathbf {y}, k)\right) = \mathrm{HE.E} (D (\mathbf {x}, \mathbf {y}), k).
$$

Note that, the numeric type of feature vectors may be real number, but the homomorphic encryption is based on large integers, therefore we use the fixed point representation [17] to represent real numbers for its efficiency. And in the following parts, we omit the real-integer conversion and use normal arithmetic operations on real numbers for simplicity.

![](images/05f86ba4bcbffde34cff24a902ceecd0dcc318f10fbcac0048ddcbe6ca0c8ea6.jpg)



Fig. 2. PIC Architecture

# III. SYSTEM OVERVIEW

# A. Architecture & Entities

We design a novel architecture to let users store, share and search images privately via external cloud without conducting computationally heavy tasks. The entire outsourced computation is conducted on the ciphertexts of image feature descriptors directly, therefore users' image content privacy and query privacy are preserved against cloud servers or other adversaries. Note that, original images can be protected by symmetric encryption as usual. Fig. 2 describes the flow of our system, and our system has the following entities:

Users: a user can be an image owner and an image querier simultaneously. An owner stores and shares his images with others by outsourcing them to the cloud servers, and a querier searches an image on the DB located at the cloud server side.

Cloud Server (CS): The cloud server is in charge of majority of the computation and the storage throughout the system. Whenever a transaction request arrives, he processes the request by computing on the ciphertexts. CS could be any commercial cloud service providers who are willing to improve their services to attract more privacy-sensitive users.

Key Agent (KA): To make sure no one within the system learn the final key used in the encryption, we introduce a key agent, who manages various secret keys. Majority of the transaction between users and CS is relayed by KA. KA could be any agent who is unlikely to collude with the CS or a specific user.

# B. Threat Model

The trusted party (TP) is introduced only to generate the keys, who could be an auditor or a notary public and is assumed to be fully trusted. However, the cloud server (CS) and the key agent (KA) who conducts most of the computation may be motivated to infer useful information from the outsourced computation, and they are assumed to be semi-honest, i.e., they will follow the protocol specification in general, but will also try their best to harvest the content of the encrypted communication. In general, TP, CS and KA are well protected, so we do not consider compromise attack in this paper. Also, although CS and KA are assumed to be semi-honest, the probability that both of them collude with a specific user is extremely small. Therefore, we assume that it is not possible to have a user who collude with both CS and KA.

# IV. BASIC SYSTEM DESIGN

With the preliminaries and the system architecture, we are ready to present the detailed design of our system PIC. The system supports the following four operations to serve the users: initialization, key generation & policy announcement, image upload and privacy preserving image search with access control.

# A. Initialization

Firstly, TP picks the system parameter for the homomorphic encryption [16] and publishes it. Then, TP generates a master key k to be used in the homomorphic encryption, and he finds two random keys $k_{CS}, k_{KA}$ such that $k_{CS}k_{KA} = k$ and sends $k_{CS}, k_{KA}$ to CS and KA respectively via secure channel.

# B. Key Generation & Policy Announcement

Whenever a new user u joins the system, TP generates three random keys $k_{u}, k_{u}^{\prime}, k_{u}^{\prime\prime}$ such that $k = k_{u} k_{u}^{\prime} k_{u}^{\prime\prime}$ . Then, he gives $k_{u}^{\prime}$ to the cloud server (CS), $k_{u}^{\prime\prime}$ to the key agent (KA) and $k_{u}$ to the user u via secure channel.

Then, the user defines the access policy which controls who can/cannot search on his images. The policy is described by an access tree as in CP-ABE [18], and it is uploaded to CS for further access control.

Submitting raw attributes to CS will reveal the user's identity information. Therefore, the attributes as well as access policy should be masked before uploading. Note that the access control policy is used as a black-box building block in our system, and here we present a simple policy which works with CP-ABE as a baseline method. When joining the system, every user describes his access policy with an access tree, but the attributes at the leaf nodes are replaced with the hashed values. Whenever a querier wishes to search on a group of specified users or the entire DB, the querier submits his hashed attributes to CS. CS then matches these hashed attributes with the access policies in the DB to find out the group of users that the querier is qualified to search on. We evaluate the practicality of the access policy by investigating a real social networking system (in SectionVI-C), and our analysis shows that for most cases the simple access policy is sufficient and practical. For some special cases, there can be other better options for the access control (e.g., anonymous IBE with predicate encryption [19]) which achieves better anonymity, but this is not our main contribution, and we leave it as one of our future works to study.

# C. Image Upload

Whenever a new user u uploads some images, he first extracts feature descriptors from them, and encrypts the descriptors using his key $k_{u}$ as follows:

HE.E( $\{X_{i,1},X_{i,2},\cdots\},k_{u}$ ).

Then, the user needs to either update or create the index cluster for his feature descriptors. There are two phases for the index cluster update or construction. (1) Indices construction: cluster representatives are selected from feature vectors as centroids of the cluster. (2) Clustering: other vectors are assigned to clusters. Various clustering techniques can be applied to choose the representatives and assign the vectors, and different clustering techniques have different performance and accuracy. One can simply use k-mean clustering to cluster the vectors. At each time the user wants to update the index cluster, he will either re-construct the index or just incrementally append new representatives or nodes into the current clusters.

After the clusters are prepared, he appends references to the nodes in the cluster which points to the corresponding ciphertexts of feature vectors. Then, the raw index clusters are sent to CS. To reduce the communication overhead, the user can send only the change of the index cluster instead. After he completes the update (or creation), the ciphertexts are sent to KA.

KA, upon receiving the ciphertexts, conducts the following operation for every ciphertext to get the ciphertexts with altered key $k_{u}k_{u}^{\prime}$ :

$$
k _ {u} ^ {\prime - 1} \mathtt {H E . E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k _ {u}\right) k _ {u} ^ {\prime} = \mathtt {H E . E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k _ {u} k _ {u} ^ {\prime}\right)
$$

Then, KA sends the new ciphertexts with altered key to CS. CS conducts the following operation to get the final ciphertexts:

$$
\begin{array}{l} k _ {u} ^ {\prime \prime - 1} \mathrm{HE.E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k _ {u} k _ {u} ^ {\prime}\right) k _ {u} ^ {\prime \prime} = \mathrm{HE.E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k _ {u} k _ {u} ^ {\prime} k _ {u} ^ {\prime \prime}\right) \\ = \mathrm{HE.E} \left(\left\{\mathbf {X} _ {i, 1}, \dots \right\}, k\right) \\ \end{array}
$$

Then, CS merges the user $u$ 's index cluster with the global one for his DB, but leaving a label to mark the owner of the cluster.

# D. Privacy Preserving Search with Access Control

One image search has two phases: level-1 search and level-2 search. In the level-1 search, KA first finds out the cluster representative in the index cluster which is closest to the querying feature vector. Then, he finds out the k-nearest neighbors (k-NNs) of the querying feature vector within the cluster in the level-2 search.

Level-1 Search. When a querier q wants to search an image, he first extracts the feature descriptor (i.e., a set of feature vectors) from the querying image. Then, he encrypts the feature descriptor of the querying image $X_{q}$ with his key $k_{q}$ as HE.E( $X_{q}, k_{q}$ ), and submits the ciphertexts to KA. Then, KA alters the ciphertext to HE.E( $X_{q}, k_{q}k_{q}^{\prime}$ ) and sends them to CS, and CS finally alters the ciphertexts to

$$
\begin{array}{l} \mathbf {H E . E} \left(\mathbf {X} _ {q}, k _ {q} k _ {q} ^ {\prime} k _ {q} ^ {\prime \prime} k _ {C S} ^ {- 1}\right) = \mathbf {H E . E} \left(\mathbf {X} _ {q}, k k _ {C S} ^ {- 1}\right) \\ = \mathrm{HE.E} \left(\mathbf {X} _ {q}, k _ {K A}\right) \\ \end{array}
$$

Besides, the querier also uploads his hashed attributes to CS. CS then searches all users' policies and find out the users that the querier is qualified to search on their images. Then, CS computes the following altered ciphertexts, where $\{y_{o}\}$ refers to the set of feature vectors referenced (via ciphertext) by the representatives in previously found owners' index clusters:

$$
\begin{array}{l} k _ {C S} \mathsf {H E}. \mathsf {E} \left(\left\{\mathbf {y} _ {o} \right\}, k\right) k _ {C S} ^ {- 1} = \mathsf {H E}. \mathsf {E} \left(\left\{\mathbf {y} _ {o} \right\}, k k _ {C S} ^ {- 1}\right) \\ = \mathrm{HE.E} \left(\left\{\mathbf {y} _ {o} \right\}, k _ {K A}\right) \\ \end{array}
$$

After all the altered ciphertexts are ready, CS computes the $\phi_{\mathrm{D}}(\cdot)$ function (Section II-C) for every pair of

$(\mathrm{HE.E}(\mathbf{x},k_{KA}),\mathrm{HE.E}(\mathbf{y},k_{KA}))$ , where $x\in X_{q}$ is a feature vector belonging to a descriptor in the querying image, and $y\in\{y_{o}\}$ . Then, CS achieves the pairwise encrypted distances, which are sent to KA.

KA is able to decrypt the distances since the ciphertexts are encrypted under his key $k_{KA}$ . After decrypting the distances, he finds out the minimum distance for every $x \in X_{q}$ , which is the distance to the NN of x.

Level-2 Search. After finding the nearest neighbor among the representatives for every $x \in X_{q}$ , KA further requests the distances between the x and all the vectors within the NN's cluster.

Upon receiving the request, CS generates the following altered ciphertexts using the key conversion (Section II-B) and $\phi_{\mathsf{D}}(\cdot)$ function as aforementioned, where $\{y_{c}\}$ is the set of vectors within the NN's cluster:

$$
\left\{ \right.\left.\left\{\mathrm{HE.E} \left(\mathrm{D} (\mathbf {x}, \mathbf {y}), k _ {K A}\right)\right\} _ {\forall \mathbf {y} \in \left\{\mathbf {y} _ {c} \right\}} \right\} _ {\forall \mathbf {x} \in \mathbf {X} _ {u}}
$$

Then, he sends these ciphertexts of distances as well as the image IDs associated with the feature vectors in the ciphertexts to KA. KA then decrypts the ciphertexts and determines the $k$ -NNs among $\{\mathsf{HE.E}(\mathsf{D}(\mathbf{x},\mathbf{y}),k_{KA})\}_{\forall \mathbf{y}\in \{\mathbf{y}_c\}}$ for each $\mathbf{x}\in \mathbf{X}$ . Based on the distances and the corresponding image IDs, he calculates the score $S^n$ of all images (Section II) appearing in the image IDs sent from CS and returns the image ID with the highest score to the querier. The querier then retrieves the encrypted image from the DB. One can further apply oblivious transfer (will be described in Section VII) to prevent the CS from inferring the query result by monitoring its memory access.

In this level-2 search, if CS does not find k ciphertexts within the cluster, he also chooses the next NN among the representatives and sends the corresponding ciphertexts to KA as well. This is repeated until he finds out at least k ciphertexts to return to KA.

# V. SYSTEM REFINEMENTS

The basic system we proposed in previous section achieves efficient privacy-preserving image search in some cases, e.g. people recognition in a face image collection, but its performance is degraded in more general cases as we discuss below. Therefore, we further improve our system to boost up the performance in this section.

# A. Dealing with High-resolution Images

A feature descriptor usually contains a set of high dimensional feature vectors, e.g. 128 dimension for SIFT. Since each dimension is a 64-bit real value, when we consider the encryption, each feature vectors' size becomes 64KB because each dimension of the vector is encrypted with a $4 \times 4$ matrix with 256-bit integers. Then, the number of feature vectors in an image determines the size of the feature descriptor of the image. In the face recognition, 9 feature vectors are enough to conduct an accurate search because face models are well developed. However, for complicated image with hundreds of feature vectors, the size of ciphertexts is not acceptable for many mobile devices. Therefore, we further optimize our system using visual words ([4], [20]) to reduce the communication overhead. By quantizing the space of feature vector, we can obtain a visual dictionary. An image can be represented with the frequency histogram of visual words, by choosing the nearest word for each of its feature vectors. Then the feature descriptor is significantly reduced to one $n$ -dimensional frequency vector. The similarity between images can be computed by the scalar product of two frequency vectors of the images. To minimize the accuracy loss caused by quantizing the feature vector space, we weight the frequency vector with term frequency inverse document frequency (tf-idf, [20]). The experimental results in peer works ([20]) and our evaluation result (Section VI-E) show that using this weighted frequency vector instead of exact feature vectors brings a negligible accuracy loss. In our advanced scheme, we use weighted frequency vector with visual dictionary as our feature image descriptor.

# B. Leveraging the Parallel Computation

We further expedite the search process leveraging the MapReduce framework. To do so, our search scheme must support parallelism. By designing the search process as the level-1 search and the level-2 search, one can complete both searches (finding the NN among the representatives and the k-NNs within the cluster) by arbitrary number of mappers and one reducer. The ciphertexts of the feature vectors and the querying vector will be given to the mappers, who conducts the homomorphic operations and the key modification to generate the ciphertexts of the distances. Then, these are sent to the reducer at the KA side who decrypts and sorts the distances.

However, there is a problem if our approach is directly implemented with a MapReduce framework. Unless the data is stored with special format (e.g., bucketized), sorting limits the number of reducers to one because the mappers do not emit the (key,value)=(image ID, distance) pairs in a sorted order. Since the sorting order depends on the querying feature vector, the number of reducers will be always 1. This is a great bottle-neck since the reducer needs to wait for all (key,value) pairs emitted from all mappers before it continues to the sorting. To solve this bottleneck, we can return all the neighbors within a certain threshold distance instead of the exact NN in the level-1 search or the k-NNs in the level-2 search. By doing so, we can theoretically have arbitrary number of reducers to finish the search task in a parallel manner. If the threshold is chosen such that not enough results are found, one can easily use a binary search manner to adjust the threshold until he finds enough results to further proceed.

For the clustering algorithm, extended cluster pruning $[5]$ , $[15]$ provides a promising way for efficient clusters construction and queries processing. We apply the extended cluster pruning with recursion in the advanced scheme. Due to the space limitation, we omit the detail of the approach here.

# C. Advanced Scheme

Only the image upload and the privacy preserving image search with access control will be changed in the advanced scheme. The changed operations are as follows:

1) Image Upload: The user u firstly extracts the feature vectors from every image that he wants to upload to CS. Then, he uses k-mean clustering to find the k clusters among all his vectors, and sets all the centroids as elements in the visual dictionary of k elements. Hereafter, we use $D_{u}$ to denote user i's dictionary. After $D_{u}$ is generated, user u also calculates the k-dimensional weighted frequency vector of each image I as $f_{I}$ , and uses CP-ABE to encrypt all parameters in the weight function ( $\{f_{i,I}, f_{i}\}_{i}, N$ ) as well as $\mathbf{D}_{u}$ : ABE.E( $D_{u}, \{f_{i,I}, f_{i}\}_{i} = 1, \cdots, k, N$ ). User u sends this ciphertext to CS, and encrypts all weighted frequency vectors as: HE.E( $\{f_{I}\}_{I}, k_{i}$ ). Then, he uses aforementioned extended cluster pruning approach with recursion to construct an index tree of all $f_{I}$ 's, where each node contains the reference to the corresponding encrypted vector. The raw index tree is sent to CS (if only updated, only the changed parts are sent to CS), and the encrypted ciphertexts are sent to KA.

KA, upon receiving the ciphertexts, conducts the key modification to alter the ciphertexts to: HE.E $\left(\left\{\mathbf{f}_{I}\right\}_{I}, k_{u}k_{u}^{\prime\prime}\right)$ . Then, KA sends the new ciphertexts to CS, who conducts another key modification to achieve the final ciphertexts: HE.E $\left(\left\{\mathbf{f}_{I}\right\}_{I}, k_{u}k_{u}^{\prime\prime}k_{u}^{\prime}\right) = \text{HE.E} \left(\left\{\mathbf{f}_{I}\right\}_{I}, k\right)$ .

2) Privacy Preserving Search with Access Control.: Same as the basic scheme, we also have two phases in a search.

Level-1 Search. When a querier q wants to search an image, he first extracts the feature vectors from the querying image. Then, he retrieves the ABE.E( $D_{o}, \{f_{i,I}, f_{i}\}_{i} = 1, \cdots, k, N$ )'s of all image owner o's that he wants to search on, and decrypts the dictionaries as well as the parameters with his attributes. Then, he looks up each dictionary to create a frequency vector of his querying image for each $D_{o}$ . Then, he calculates m weighted frequency vectors with the decrypted parameters, which are encrypted as: HE.E( $\{f\}_{all owners}, k_{q}$ ). This is relayed by KA (after altering the key to $k_{q}k_{q}^{\prime\prime}$ ) and finally arrives CS who finally alters the key to $k_{q}k_{q}^{\prime\prime}k_{q}^{\prime} = k$ . Then, CS finds out the index trees of the users that querier q wishes to search on, and conducts the following key modification, where $\{y_{o}\}$ refers to the set of frequency vectors referenced (via ciphertext) by the cluster leaders in those index trees: HE.E $(\{y_{o}\}, kk_{CS}^{-1}) = \text{HE.E}(\{y_{o}\}, k_{KA})$ . Then, CS computes the $\phi_{D}(\cdot)$ function for every pair of $(\text{HE.E}(\mathbf{x}, k_{KA}), \text{HE.E}(\mathbf{y}, k_{KA}))$ where x is the frequency vector of the querying image, and $y \in \{y_{o}\}$ . The outputs of the function are the pairwise encrypted distances, which are sent to KA.

KA proceeds with MapReduce framework. He sends the ciphertexts to his mappers, each mapper decrypts the distances and emits the (key,value)=(image ID,distance) to his reducers, and the reducers find out the distances above a threshold $\theta$ , which corresponds to the distance of x's nearest neighbors.

Level-2 Search. After finding the NNs, KA further requests the distances between x and all vectors under those NNs in the index trees.

Upon receiving the request, CS generates the encrypted distances using the key modification as well as the $\phi_{D}(\cdot)$ function. These are sent to KA who sends those ciphertexts to his mappers to let them decrypt the distances. The (image ID,distance) pairs are sent to his reducers, and they finally find out the images whose distances are above another threshold $\theta'$ .

# VI. IMPLEMENTATION AND EVALUATION

In this section, we first present the implementation of PIC and the datasets used in the experiments, then we evaluate the performance of our basic scheme using SIFT feature vectors and advanced scheme using weighted frequency vector from different aspects. For simplicity, in the following statement, we denote the basic scheme as PIC-sfv and the advanced scheme as PIC-wfv.

# A. System Implementation

We build PIC including both cloud side and client side. On the cloud side, each of KA and CS consists of a cluster of computers with distributed file system (Hadoop HDFS) and MapReduce architecture (Hadoop MapReduce). In this evaluation, we use four PCs (Intel Core i3-3240 CPU, 3.4GHz, 4G RAM) for each cluster. Each cluster has one name node and three data nodes, which is a small but full-featured data center to demonstrate our design, and the performance can be greatly improved when using large data center [21]. On the client side, we implement our system for both Windows OS laptop and Android phone. In this evaluation, we use a laptop ThinkPad X1 (2.7GHz CPU, 4GB RAM), and a mobile phone HTC G17 (1228Hz CPU, 1GB RAM). There is also a trusted party (TP) that in charge of key generation. In our experiments TP is a single PC with the same hardware as the node of the cluster. Due to the space limitation, in this paper, we omit the evaluation results on Android phone, whose runtime is the same order of magnitude as the laptop.

We implement all cryptographic components of our system by Java. We use three commonly used descriptors to evaluate the practicality of our system, including 128-dimensional SIFT descriptor [3], 64-SURF and 128-SURF [14], which are highly distinctive and fast to compute. Nevertheless, our schemes are also compatible with other image descriptors. The descriptor extraction is implemented using the OpenCV library for Window and Android. Due to the space limitation, in this paper, we only present the results of the most popular descriptor, 128-SIFT, and 64-SURF and 128-SURF achieve similar performance as using 128-SIFT.

TABLEI COMPUTATION COST FOR EACH OPERATION USING A SINGLE PC. (S) $\lambda = 128$ , $m = 2$ , THE SIFT-VEC IS 128-DIMENSION SIFT FEATURE VECTOR, THE FREQ-VEC IS 1000-DIMENSION WEIGHTED FREQUENCY FEATURE VECTOR.

<table><tr><td colspan="4">Common Operations</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Feature Extract</td><td>8.7</td><td>1.56</td><td>12.03</td></tr><tr><td>Parameter Init</td><td>0.002</td><td>0.002</td><td>0.003</td></tr><tr><td>Master Key Gen</td><td>&lt;0.001</td><td>&lt;0.001</td><td>&lt;0.001</td></tr><tr><td>KA&amp;CS Keys Gen</td><td>0.001</td><td>0.001</td><td>0.001</td></tr><tr><td>Triple Keys Gen</td><td>0.002</td><td>0.002</td><td>0.003</td></tr><tr><td>Access Tree Gen</td><td>&lt;0.001</td><td>&lt;0.001</td><td>&lt;0.001</td></tr><tr><td>Decrypt Distance</td><td>&lt;0.001</td><td>&lt;0.001</td><td>&lt;0.001</td></tr><tr><td colspan="4">Operations of PIC-sfv</td></tr><tr><td>Encrypt One SIFT-Vec</td><td>0.034</td><td>0.03</td><td>0.047</td></tr><tr><td>Key Modification (per SIFT-Vec)</td><td>0.052</td><td>0.048</td><td>0.063</td></tr><tr><td>Homomorphic Euclidean Distance</td><td>0.031</td><td>0.029</td><td>0.033</td></tr><tr><td colspan="4">Operation of PIC-wfv</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Freq-Vec Gen</td><td>0.70</td><td>0.005</td><td>3.84</td></tr><tr><td>Encrypt One Freq-Vec</td><td>1.93</td><td>1.59</td><td>2.67</td></tr><tr><td>Key Modification (per Freq-Vec)</td><td>0.29</td><td>0.25</td><td>0.85</td></tr><tr><td>Homomorphic Dot Product</td><td>0.20</td><td>0.18</td><td>0.33</td></tr></table>

# B. Image Collections and Queries

To explore the performance of our approach in real-life image applications, we evaluate our system with two popular image datasets. The INRIA Holiday dataset (Holiday) [22] contains 1491 personal holidays photos in high resolution (most are 2560\*1920). There are 6767563 SIFT feature vectors of dimensionality 128 extracted from those images. The dataset contains 500 image groups, each of which represents a distinct scene or object. For the search experiments, the query is a photo of a scene, and the goal is to return other $k$ photos of this scene. The Flickr images (Flickr1M) contains one million diverse images from Flickr with 1.4 billion pre-computed SIFT feature vectors in total. For the search experiments, the query is randomly selected images, and $k$ most similar images are returned. We evaluate PIC-sfv using SIFT feature vectors from both datasets. For the evaluation of PIC-wfv, 1000 visual words are learned from 6K randomly selected images of Flickr1M as the vocabulary. And a 1000-dimension weighted frequency vector is generated for each image by clients.

# C. Micro-Analysis for Each Operation

We analyze the additional computation and communication overhead introduced by our system except the image process related overhead in this subsection.

Computation Overhead: The runtime of each operation is summarized in Table I and then the detail analysis is presented as follows.

Initialization: This operation requires the selection of system parameters for MHE and three random encryption keys $k, k_{CS}, k_{KA}$ , such that $k = k_{CS}k_{KA}$ . Both operations are executed at TP side and they take less than 5ms in total, which is negligible.

Key Generation & Policy Announcement: This operation requires a selection of three random keys $k_{i}, k_{i}^{\prime}, k_{i}^{\prime\prime}$ such that $k = k_{i}k_{i}^{\prime}k_{i}^{\prime\prime}$ from TP, which cost less than 3ms. Besides, it also involves an owner's access tree generation. We evaluate the performance of our access control methods based on the profile data of Tencent Weibo, which is one of the largest social networking platform in China. This dataset has 2.32 million users' personal profiles. There are 770166 different attributes in total. Each user has 6 attributes in average and 20 attributes at most. 60% users have no common attribute with others, about 20% users share one common attribute with others, and 98% users share less than four common attributes with others. Our analysis suggests that a small access tree with limited attributes (e.g. 6 attributes), is enough to narrow down the size of authorized users (0.2%), and its generation time is only $8 \times 10^{-3}$ ms. Given the access tree, the runtime to authenticate the attributes of a querier is less than 1ms. So the cost for access control is negligible.

Image Upload: For PIC-sfv, the cluster construction is first executed by each owner, and the runtime increases linearly with the feature vector number (Fig. 3). For two image sets, it takes 20 seconds to cluster feature vectors of 100 randomly selected images. Then the owner encrypts every descriptor using his key $k_{i}$ . As shown in Table I, it takes 34ms to encrypt each 128-dimension feature vector. The runtime to encrypt the descriptor of each image depends on the its feature vector number as depicted in Fig. 3. Fig. 4 shows runtime to encrypt one image from two images sets, which is 75s in average. After the ciphertexts are sent to KA, KA conducts a key modification to alter the encryption key of the ciphertexts. As shown in Fig 4, it takes 155s to modify the key of an image in average. The key modification at CS side is the same operation as KA's one and thus omitted.

For PIC-wfv, based on the visual word vocabulary, the owner generates weight frequency vector for each image, whose runtime is proportional to the feature vector number of this image (Fig. 5). For two image sets, it takes 0.7s per image in average. Then the owner encrypts the weighted frequency vector of each image, whose runtime is depicted in Fig 6. It takes less than 1.5s to encrypt one image. Fig 6 also presents the time cost of key modification for each image by KA (or CS), which is about 0.29s.

Privacy Preserving Image Search with Access Control: The querier first encrypts the image descriptor (SIFT feature vectors or one weighted frequency vector), whose run time is the same as the one in the image upload (Fig. 4 and Fig. 6). The key modifications by KA and CS are also the same. Besides, in PIC-sfv, CS needs to compute the ciphertexts of all squared Euclidean distances. Using a single machine, each distance takes 31ms and the whole time cost depends on the number of query feature vectors and the size of searched vectors collection in DB, i.e. (\#cluster + cluter size) × #featurevector × 31ms. In PIC-wfv, CS computes the ciphertexts of all dot products, each takes 200ms by one machine and the whole time cost just depends on the image collection size, i.e. (\#cluster + cluter size) × 200ms. After CS prepares all the ciphertexts, KA decrypts them to achieve the distances or dot products, and sort them to find out the NN. For both schemes, each decryption requires less than 1ms and it takes about 0.5s to decrypt 1000 distances. We use quick-sort to sort the distances, but we omit the run time analysis since this is a standard sorting method. For Holiday, without MapReduce functions, using PIC-sfv each query (with more than 3000 feature vectors) averagely takes about 100 machine-hours to find the matching image among the 1491 images; using PIC-wfv each query takes about 15 machine-seconds. Deploying our MapReduce implementations on the 4-node small data center, the delay is reduced to about 17 hours for PIC-sfv and reduced to 4s for PIC-wfv.

![](images/6d7fc1c5c2361291b45d307e1360e66549b905a17dc1aba3a372d428a223f53a.jpg)



Fig. 3. Runtime of upload operation VS. SIFT feature vector Number (PIC-sfv).

![](images/20c0a04a4810b00e6c1604f29846b1282d325777c0e2164727f9c0167d160810.jpg)



Fig. 4. CDF of runtime of upload operation for each image in two image sets (PIC-sfv).

![](images/d63fe2423325354a949cdb6b3cd0897f9c8e918a1c725bba0aa69a981cc637cb.jpg)



Fig. 5. 1000-D weighted frequency vector generation VS. feature vector number of this image (PIC-wfv).

![](images/e2edff5f1c98f19769e754c52e0dab501c05fb9d354f32e6bee1eabf53782dab.jpg)



Fig. 6. CDF of runtime of upload operation for each image in two image sets (PIC-wfv).

As a brief summary, both PIC-sfv and PIC-wfv have same initialization delay and similar runtime for index construction and frequency vector generation. However, PIC-wfv uses only one 1000-dimension weighted frequency vector to represent each image, while in PIC-sfv the descriptor of each image is a set of 128-dimension SIFT feature vectors. When the size of feature vectors is small, two scheme has comparable performance. But as the feature vector size increases, PIC-sfv's overhead increases linearly while PIC-wfv keeps the runtime almost a constant. Moreover, for the privacy-preserving image search, our schemes work excellently with MapReduce framework to reduce the response time.

Communication Overhead: We first summarize the size of the transmitted data structure in Table II. Then we analyze the communication cost for each operation.

Initialization: TP needs to send key $k_{CS}$ and $k_{KA}$ to CS and KA respectively, and the mean size of a single key is 0.84KB.

Key Generation & Policy Announcement: TP sends $k_{i}, k_{i}^{\prime}k_{i}^{\prime\prime}$ to the user i, CS and KA respectively, and each key's size is 0.84KB. Based on the data of Tencent Weibo, the size of the access tree with 6 attributes is about 0.2KB.

TABLE II COMMUNICATION COST OF EACH DATA STRUCTURE. (KB) $\lambda = 128$ , $m = 2$ , THE SIFT-VEC IS 128-DIMENSION SIFT FEATURE VECTOR, THE FREQ-VEC IS 1000-DIMENSION WEIGHTED FREQUENCY FEATURE VECTOR. 

<table><tr><td colspan="4">Common Data</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Key</td><td>0.84</td><td>0.19</td><td>1.4</td></tr><tr><td>Access Tree</td><td>0.18</td><td>0.03</td><td>0.63</td></tr><tr><td>Encrypted Distance</td><td>0.56</td><td>0.41</td><td>0.65</td></tr><tr><td colspan="4">Data of PIC-sfv</td></tr><tr><td>Encrypted SIFT-Vec</td><td>64</td><td>62.8</td><td>65.1</td></tr><tr><td colspan="4">Data of PIC-wfv</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Encrypted Freq-Vec</td><td>580</td><td>578.9</td><td>581.2</td></tr></table>

Image Upload: The user informs CS of the change in the index cluster, but this is almost negligible. Main communication overhead comes from the ciphertexts transmission. For PIC-sfv, uploading the encrypted feature vectors incurs #feature vector × 64KB data transmission. For PIC-wfv, the ciphertexts (encrypted weighted frequency vector) size of each image is 580KB, which is constant. Similarly, KA also needs to send out the same size ciphertexts to CS.

Privacy Preserving Image Search with Access Control: First, the querier encrypts the query descriptor and sends the corresponding ciphertexts to KA, which is #feature vector × 64KB for PIC-sfv and 580KB for PIC-wfv. KA also sends the same amount of ciphertexts to CS. For PIC-sfv, in the level-1 search, after CS computes the encrypted distances for all representatives, the encrypted distances are sent back to KA, the size is 0.56KB each and the whole size is #cluster × 0.56KB. During the level-2 search, CS computes the encrypted distances for all vectors within the NN's cluster, and sends them to KA (cluster size × 0.56KB). For PIC-wfv, similarly, CS computes and send all encrypted dot products to KA, whose size is (#cluster + cluster size) × 0.56KB. For Holiday, the transmitted data between CS and KA during search is about 2800KB for two rounds search of PIC-sfv and 43KB for PIC-wfv.

# D. Macro-Analysis for Each Entity

We analyze the overall computation overhead for each entity in this subsection. Similarly, we only analyze the additional overhead except the image process related one. Cloud Server: The computational delay at CS side during the image upload comes from key modification. In PIC-sfv, it is #feature vector × 52ms (Fig. 3) and about 200s for 80% images (Fig. 4). Using PIC-wfv, it takes about 1.2s for 80% images. During the image search, the computation cost of CS comes from the homomorphic distance calculation. For a single node, the cost is (\#cluster + cluter size) × #feature vector × 31ms using PIC-sfv and (\#cluster + cluter size) × 200ms using PIC-wfv.

Key Agent: KA experiences the same delay as CS during the image upload. The computation cost of KA during search comes from decrypting all distances and ranking them to find the NN. The run time is 0.5s to process 1000 distances.

Client: The computational delays occur during the system join, image upload and the image search for an ordinary user. The system join cost is negligible (about 3ms). In PIC-sfv, the clustering cost is negligible compared to the encryption cost, and encryption cost is #feature vector × 34ms (Fig. 3). So the computational delay of upload is about 100s for 80% images from the two image sets (Fig. 4). Similarly, for PIC-wfv, the computational delay during upload for 80% images is only about 2.2s and 1.5s in average(Fig. 6). During search, the client does nothing but waits for the search result from the cloud and the delay is summation of the computational delay at CS and KA.

In summary, for a querier, after providing a query image, the response time is mainly the computational delay accumulation of image encryption, two key modifications, homomorphic distance calculation, distance decryption and ranking. When the querier can access all 1491 images of Holiday on the cloud, the average response time of each query is about 17 hours and 8 minutes for PIC-sfv and 7.21 seconds for PIC-wfv. Here the delay can be greatly reduced as the cloud scales up from 4 nodes to hundreds of nodes. Besides, compared to exiting multi-part secure computation based methods, by our approach, during the search no interaction is required for the client and 97% computation is carried out by CS, leaving KA and clients very limited overhead.

# E. Performance Comparison

Compare with alternative methods. [16] has compared its cost against the well-known homomorphic encryption scheme of Gentry [23]. Gentry's scheme needs more than 900 seconds to add two 32 bit numbers, and more than 67000 seconds for the multiplication, but the cost for [16] is only 0.1 ms and 108 ms respectively. The reason is that Gentry's fully homomorphic encryption is based on the "learning with errors" (LWE) problems in lattice system, which allows users to apply as many multiplications as they want on the ciphertexts. [16] is based on number theory and group theory, which only supports a limited number of homomorphic operations, but is sufficient for our application. So, [16] is much more practical and compact. We also realize private Euclidean distance computation using a partial homomorphic encryption (Paillier encryption) in the SMC manner (e.g. the method used in [19]). Using the same computer and test images, the Paillier-based method (128-bit) takes about 0.5s for feature vector encryption and 0.18s for homomorphic distance computation. But in our work, they take only 0.034s and 0.031s respectively. The comparison shows the computation efficiency of our system.

Search Accuracy. First, we evaluate the search accuracy of our approaches according to the ground truth of 500 queries of Holiday. With k=5 (five nearest neighbors are fetched), the accuracy of PIC-sfv is 95.2% and of PIC-wfv is 93.4%. Here the accuracy is the success rate of 500 queries. A result is success if the returned k images contain at least one image from the same scene as the query image. So, our solution achieves privacy-preserving without sacrificing the search accuracy. When a vocabulary is learnt, PIC-wfv provides the similarly good accuracy as PIC-sfv.

Linear Search vs. Our Approaches with MapReduce.

![](images/2a8d5b75d8a29c461ece94509dbbe79e7ff2f345849e2eae3f5dceced9b1c944.jpg)



Fig. 7. Search time using different approaches VS. feature vector number of the query image. Two different size searched image collections (1K and 10K) are selected randomly from Flickr1M.

We implement the SIFT feature vector based scheme and the visual word based scheme using the Hadoop MapReduce framework to accelerate the search. To study the search efficiency of different schemes, we compare the computational overhead of our two schemes using a 4-node cluster with the one of conducting a linear search using a single computer on the raw images data. The comparison is presented at Fig. 7, which shows the overhead is reduced an order of magnitude by the SIFT feature vector based approach. Further more, the visual word based approach keeps the overhead a second-level constant.

Then we evaluate the improvement caused by adapting our privacy-preserving search to MapReduce framework. We run the 500 queries on the encrypted Holiday data set. With a single computer, the cluster based approach takes about 100 hours for each query, and the visual word based approach takes 15 seconds for each query. When running on the 4-node small cluster with our MapReduce adaptive implementation, the runtime reduces from 100 to 17 hours and from 15 seconds to 4s respectively. With a large cluster, the improvement will be much bigger.

As a conclusion, leveraging the power of indexing and MapReduce, our system design improves the search performance greatly while keep a high search accuracy and well protected privacy.

# VII. RELATED WORK

Image Indexing and Search. There are numerous works addressing searching for similar images, and most of them are based on the local invariant descriptors, e.g., SIFT [3] and SURF [14]. The 128-dimension SIFT descriptor is most widely used for image search due to its distinctiveness and computational efficiency. The most accurate approach to search similar images is to conduct the nearest neighbor search among image descriptors. But it is too expensive facing billions of high-dimension vectors. Various feature vector indexing approaches are designed to boost up the search efficiency, e.g., cluster pruning [15] and extended cluster pruning [5]. Extended cluster pruning [5] provides a promising way for efficient clusters construction and queries processing. Besides clustering, recently, a lot of work speed up the search process based on visual words e.g. [4], which somewhat decrease the search accuracy. As commercial data center get more and more popular, it is also possible to improve the large-scale image search using parallelize computing. There are some work using MapReduce [24] to accelerate the indexing and search process, e.g. [25]. However, few of image indexing and search systems consider privacy protection of the image owner and querier.

# Secure Multi-part Computation and Homomorphic

Encryption. The core of content-based image search is measuring the distance between vectors. There are many existing methods addressing privacy-preserving vector distance among parties using secure multi-party computation (SMC) [11]–[13]. There are some work providing privacy-preserving image matching using classic homomorphic encryption, e.g., [8] and [9]. Those methods provide privacy protection to the query image as well as the outcome of the matching algorithm, but the result is not secure against the service provider. They all require rounds of online interactions with users during the search and incur expensive computation cost, so none of them can be scaled to address large-scale image sets. Recently, Xiao et al. proposes an efficient homomorphic encryption protocol for multi-user system [16]. It is a non-circuit based symmetric-key homomorphic encryption scheme, whose security is equivalent to the large integer factorization problem. We employ this protocol to design our system.

# VIII. CONCLUSION

We have presented a novel system PIC towards privacy preserving content-based search on large-scale outsourced images. With our careful design, the majority of the computationally intensive image matching jobs are outsourced to the cloud in a non-interactive way, but the image and query privacy is preserved. To further expedite the search process, we enable the cloud to maintain the index structure and parallelize the search process without learning anything. We implement our prototype system using Hadoop MapReduce framework in a computer cluster, and our experiment results show the efficiency and the applicability of our system in a cloud platform.

# ACKNOWLEDGMENT

Xiangyang Li is the contact author. This research is partially supported by NSF China Major Program 61190110 and National High Technology R&D Program of China (863 Program) under Grants No.2015AA01A201. The research of Li is partially supported by NSF CNS-1035894, NSF ECCS-1247944, NSF ECCS-1343306, NSF CMMI 1436786, NSFC 61170216, NSFC 61228202.

# REFERENCES

[1] C. Bo, G. Shen, J. Liu, X.-Y. Li, Y. Zhang, and F. Zhao, “Privacy.tag: Privacy concern expressed and respected,” in ACM SenSys, 2014.   
[2] P. Weinzaepfel, H. Jégou, and P. Pérez, “Reconstructing an image from its local descriptors,” in CVPR. IEEE, 2011.   
[3] D. G. Lowe, “Distinctive image features from scale-invariant keypoints,” IJCV, vol. 60, no. 2, 2004.   
[4] H. Jégou, M. Douze, and C. Schmid, “Improving bag-of-features for large scale image search,” IJCV, 2010.   
[5] G. P. Gudmundsson, B. P. Jónsson, and L. Amsaleg, “A large-scale performance study of cluster-based high-dimensional indexing,” in VLS-MCMR. ACM, 2010, pp. 31–36.   
[6] M. Daneshi and J. Guo, “Image reconstruction based on local feature descriptors,” 2011.   
[7] C. Wang, N. Cao, K. Ren, and W. Lou, “Enabling secure and efficient ranked keyword search over outsourced cloud data,” IEEE TPDS, vol. 23, no. 8, pp. 1467 – 1479, 2012.   
[8] Z. Erkin, M. Franz, J. Guajardo, S. Katzenbeisser, I. Lagendijk, and T. Toft, “Privacy-preserving face recognition,” in Privacy Enhancing Technologies, 2009, pp. 235–253.   
[9] A.-R. Sadeghi, T. Schneider, and I. Wehrenberg, in Information, Security and Cryptology.   
[10] L. Zhang, T. Jung, C. Liu, X. Ding, X.-Y. Li, and Y. Liu, “Pop: Privacy-preserving outsourced photo sharing and searching for mobile devices,” in ICDCS. IEEE, 2015.   
[11] T. Jung, X.-Y. Li, and S. Tang, “Privacy-preserving data aggregation without secure channel: Multivariate polynomial evaluation,” in IEEE INFOCOM, 2013.   
[12] L. Zhang, X.-Y. Li, Y. Liu, and T. Jung, “Verifiable private multiparty computation: Ranging and ranking,” in IEEE INFOCOM, 2013.   
[13] T. Jung, X.-Y. Li, and M. Wan, “Collusion-tolerable privacy-preserving sum and product calculation without secure channel,” in IEEE TDSC, 2014.   
[14] H. Bay, A. Ess, T. Tuytelaars, and L. Van Gool, “Speeded-up robust features (surf),” Computer vision and image understanding, vol. 110, no. 3, pp. 346–359, 2008.   
[15] F. Chierichetti, A. Panconesi, P. Raghavan, M. Sozio, A. Tiberi, and E. Upfal, “Finding near neighbors through cluster pruning,” in SIGMOD. ACM, 2007, pp. 103–112.   
[16] L. Xiao, O. Bastani, and I.-L. Yen, “An efficient homomorphic encryption protocol for multi-user systems.” IACR Cryptology ePrint Archive, vol. 2012, p. 193, 2012.   
[17] E. L. Oberstar, “Fixed-point representation & fractional math,” Oberstar Consulting, revision, vol. 1, 2007.   
[18] J. Bethencourt, A. Sahai, and B. Waters, “Ciphertext-policy attribute-based encryption,” in S&P. IEEE, 2007.   
[19] J. Katz, A. Sahai, and B. Waters, “Predicate encryption supporting disjunctions, polynomial equations, and inner products,” in Advances in Cryptology–EUROCRYPT. Springer, 2008.   
[20] J. Sivic and A. Zisserman, “Video google: A text retrieval approach to object matching in videos,” in ICCV. IEEE, 2003.   
[21] A. Sangroya, D. Serrano, and S. Bouchenak, “Benchmarking dependability of mapreduce systems,” in SRDS. IEEE, 2012.   
[22] H. Jegou, M. Douze, and C. Schmid, “Hamming embedding and weak geometric consistency for large scale image search,” in ECCV. Springer, 2008.   
[23] C. Gentry, “Fully homomorphic encryption using ideal lattices,” in STOC. ACM, 2009.   
[24] J. Dean and S. Ghemawat, “Mapreduce: simplified data processing on large clusters,” Communications of the ACM, vol. 51, no. 1, pp. 107–113, 2008.   
[25] D. Moise, D. Shestakov, G. Gudmundsson, and L. Amsaleg, "Indexing and searching 100m images with map-reduce," in International conference on multimedia retrieval. ACM, 2013.