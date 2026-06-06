# POP: Privacy-preserving Outsourced Photo Sharing and Searching for Mobile Devices

Lan Zhang $^{*}$ , Taeho Jung $^{\ddagger}$ , Cihang Liu $^{*}$ , Xuan Ding $^{*}$ , Xiang-Yang Li $^{*\dagger\ddagger}$ , Yunhao Liu $^{*}$

\* School of Software, Tsinghua University Beijing

$^{\dagger}$ Department of Computer Science and Technology, Tsinghua University Beijing

$^{\ddagger}$ Department of Computer Science, Illinois Institute of Technology, Chicago, IL

Abstract—Facing a large number of personal photos and limited resource of mobile devices, cloud plays an important role in photo storing, sharing and searching. Meanwhile, some recent reputation damage and stalk events caused by photo leakage increase people's concern about photo privacy. Though most would agree that photo search function and privacy are both valuable, few cloud system supports both of them simultaneously. The center of such an ideal system is privacy-preserving outsourced image similarity measurement, which is extremely challenging when the cloud is untrusted and a high extra overhead is disliked. In this work, we introduce a framework POP, which enables privacy-seeking mobile device users to outsource burdensome photo sharing and searching safely to untrusted servers. Unauthorized parties, including the server, learn nothing about photos or search queries. This is achieved by our carefully designed architecture and novel non-interactive privacy-preserving protocols for image similarity computation. Our framework is compatible with the state-of-the-art image search techniques, and it requires few changes to existing cloud systems. For efficiency and good user experience, our framework allows users to define personalized private content by a simple check-box configuration and then enjoy the sharing and searching services as usual. All privacy protection modules are transparent to users. The evaluation of our prototype implementation with 31,772 real-life images shows little extra communication and computation overhead caused by our system.

# I. INTRODUCTION

With the proliferation of smart personal devices (e.g., smartphone, tablet PC) as well as the emergence of wearable devices (e.g., Google Glass), huge amounts of photos are produced everyday. Facing the challenge of photo management on resource-limited mobile devices, users often choose to outsource the burdensome storage and search jobs to cloud servers such as Amazon Cloud Drive, Dropbox and some image-oriented cloud (Cloudinary). Various social networking systems (Flickr, Facebook, Google Plus etc.) also provide photo sharing services for personal uses.

Considering the rich sensitive information (e.g., people, location and event) embedded in photos, privacy becomes a critical issue when photos are outsourced to third parties. Today's cloud-based photo services are still in a struggle between the search functionality and users' privacy. For example, the image recognition technique introduced by Facebook was very controversial in 2011, because the objects in users' photos such as faces and cars can be automatically recognized and searched [2], [18]. Tracking and stalking become easier with various image search engines (e.g., Google Image Search, Yahoo! Image Search). This controversy finally made Facebook to switch off its face recognition service in 2012. But it has brought back the functionality recently due to the need for image search, along with much disapproval. To handle such privacy issues, Google has decided to forbid face recognition on Google Glasses. To some extent, the above privacy concerns come from the fear that our photos might be illegally searched by a malicious hacker, especially when the search can be automatically conducted by a machine. And this is probably one of the primary reasons why users want to get rid of face recognition. However, the object recognition techniques could bring powerful ability to image search, e.g., finding photos with a specific friend. Using the access control mechanism alone can not protect outsourced photos from untrusted cloud. And simply disabling automatic recognition or simply encrypting the sensitive content (e.g., P3 [26]) is not the desired solution, because it also eliminates the utilities lying in the image search functionality.

Though both the search functionality and users' privacy are valuable, few today's cloud system supports both of them simultaneously. The most challenging part is outsourcing the content-based image search to the cloud while preventing the cloud from learning anything about the image content and the query. The core of the search computation is measuring distances (or similarity) among image vectors, which requires both additive and multiplicative operations. Fully homomorphic encryption (supporting both operations) could be an ideal solution, but existing schemes, e.g., [10], are still impractical due to their unacceptably large computation cost. Some secure multi-party computation (SMC) methods [17], [33] can support privacy-preserving vector similarity measurement. However, they require rounds of online interactions between the image owner and queriers, which is contrary to the goal of outsourcing and the owner cannot guarantee to stay online. Ideally, privacy-sensitive users should have an option to use the secure version of photo sharing and searching system with little extra overhead, in which image search with object recognition is allowed for authorized users but the privacy leakages due to untrusted server and automatic recognition are prevented.

To achieve this vision, we introduce a novel framework POP, does just that, enabling mobile device users to enjoy cloud-based photo sharing and search as well as preserve their privacy. To address the challenge raised by outsourced privacy-preserving image similarity measurement, we propose two efficient non-interactive vector distance computation protocols. Via our framework, an owner can share his photos on the cloud safely with fine-grained privacy protection policies; and an authorized querier can send queries to the cloud to search on others' photos. Despite such outsourcing, POP does not reveal the private image contents or the query contents (including its result) to the cloud. To more aggressively enhance the performance, we further introduce the optimized variant $POP_{bin}$ where the computation overhead is reduced by a half with only a little loss of accuracy. POP can be considered as a step towards easily deployable frameworks for privacy-preserving outsourced photo sharing and searching services. Any cloud can adopt it to attract privacy-seeking mobile users with the following advantages:

1. The framework is designed in a modularized manner and requires few changes to existing cloud platforms. To guarantee the search accuracy, our framework is compatible with the state-of-the-art image search techniques.   
2. For the mobile user, the majority of heavy jobs (storage, access control and searching) are outsourced to cloud servers, without breaching users' photo-related privacy.   
3. For image similarity measurement, we design two privacy-preserving vector distance computation protocols for both real and binary vectors, which are the core of our solution. Different from the existing multi-party computation based methods, our protocols enable efficient vector distance computation in a non-interactive way, which means the photo owner does not have to interact with the cloud or the querier.   
4. To achieve good user experience, all privacy protection modules work automatically and are transparent to users after one simple privacy setting.   
5. We implement and evaluate our framework using 31,772 real-life images on both smartphones and laptops. The evaluation shows that very low extra overhead is incurred by our method.

# II. BACKGROUNDS AND MOTIVATION

One of our main contributions is enabling efficient photo sharing and searching on encrypted photos. In order to achieve high search accuracy, POP leverages the state-of-the-art image search technologies in computer vision field. Here, we briefly review the search techniques, and then discuss the privacy issues emerging from them in this section.

# A. Descriptors Based Image Search

Images are usually searched by their contents. Different types of visual descriptors are proposed to model the visual characteristics of the image, e.g., color, intensity, texture or objects within the image. Various image contents can be recognized and localized (e.g., people [14] and face [31]) using visual descriptors. Among these, human face detection received extraordinary attention and is one of the most mature object detection techniques so far [30], [31].

The feature descriptor is usually constructed as a set of numeric vectors, denoted as feature vectors. There are some statistical feature vectors (e.g., intensity/color histograms). Also, many well designed visual descriptors are proposed to achieve accurate image search, e.g., SIFT [18] and SURF [2]. In those works, each feature vector is generated from an interest point of the image to describe the visual characteristics around the point. Interest points are pixels containing distinguishing information of the image [21]. In general, all feature vectors belonging to the same descriptor have the same dimension (e.g., SIFT has 128 dimensions and SUFR has 64 dimensions). The numeric type of vectors may be real number [2], [18] or binary [5], [25], and different types of vectors are used for different applications. Specifically, with a little accuracy loss, binary descriptors are usually more efficient in computation and suitable for resource-restricted mobile applications. We design our framework capable of dealing with both real number and binary feature vectors.

Given a query image, one needs following three steps to search the top-k similar images from the database. Firstly, predefined image descriptor is extracted from the query image. Secondly, each feature vector in the query image is compared with feature vectors from the database images. Thirdly, similarity score for every database image is measured based on the vector comparison and finally the top-k high-score images are returned to the querier.

# B. Privacy Implications

Rich content of photos raises various privacy implications. There are many mature techniques to detect and recognize the objects within the photos as aforementioned. These techniques can possibly be used to automatically analyze the photos to mine sensitive information with various data mining techniques. Combining the location stamps and time stamps embedded in a photo, more sensitive information about the person may be derived (e.g., home location, occupation, level of incoming). Therefore, the private part (denoted as Region Of Privacy (ROP) hereafter) of a photo needs to be protected, so that no human or machine runnable algorithm can learn sensitive information in the photo.

Besides the outsourced photos, the query sent to the cloud side incurs privacy implications as well. Even though the uploaded photos are well protected via encryption so that the cloud does not gain useful information of them, their contents can be easily deduced if the queries' contents and results are revealed to the cloud. Since the entire search process should be outsourced to the cloud for resource saving, protecting queries' contents as well as the results is equally important to protecting the uploaded photos.

# III. SYSTEM OVERVIEW

POP is designed for mobile users who require both outsourced photo services and privacy protection. Figure 1 illustrates the architecture and workflow of our framework $^{2}$ . With this framework design, POP can provide the following services: (1) privacy-preserving photo storage outsourcing; (2) fine-grained photo sharing with privacy protection enforcement; (3) light-weight photo searching for mobile devices.

![](images/4b29f6e38b706183cad88b310b743aaf23ef8a56d867b3ed5da709517694b87a.jpg)



(a) Photo Owner Side   
![](images/72f6dc669a2d9e4c3c8a029fe8c972f01b3f5c56f4b8ca2dabc2d7fe10c981fe.jpg)



(b) Querier Side   
Fig. 1: POP System Overview

# A. Privacy Preserving Photo Storage

Before users upload their photos to cloud servers for sharing, the photos need to be pre-processed. Firstly, the region of privacy (ROP), which is a rectangle defined by two pixel-level coordinates (top-left and bottom-right) on the photo, is either automatically or manually determined. In the automatic manner, the user can select a category of objects as private content, e.g., faces and car plates. Then all private objects will be automatically detected by object recognition algorithm and set as ROPs, e.g., the face in Fig. 2. Otherwise, the owner can also manually define the ROP by selecting a rectangle region on the photo. Users who cannot determine the private content can simply define the whole image as ROP to prevent potential information leakage. Then, the feature vectors of the ROP are extracted according to the definition of the image descriptor (Section II-A). Note that, hereafter we use the human faces as example ROPs of photos in this work, but other objects such as pedestrians and cars, can also be defined as ROPs with corresponding recognition algorithms. Moreover, except defining ROP, all the following operations are conducted automatically by the system and transparent to users.

After the ROP is selected, it is separated into public part and secret part, where the public part doesn't contain any sensitive information and the secret part is encrypted such that only the authorized users with keys can access to it and recover the original ROP. We review the following three different methods for the separation:

1. Mask: fills public part of ROP with solid black (all intensity values '0') and takes the original ROP as secret part.   
2. P3 [26]: separates ROP based on a threshold in the DCT frequency domain; sets the higher frequency part as secret part and the remaining as public part.   
3. Blur [20]: a normalization box filter is applied to ROP to generate the public part; subtracts the public part from ROP in a pixel-wise way to achieve the secret part.

Then, the public part of the whole photo is produced by replacing its ROP with the public part of ROP (as shown in Fig. 2). Our experiment (Section VI) shows that all three methods are resistant to automatic detection algorithms, but the blur based method outperforms others in the storage cost, hence we adopt the blur as the default separation method in POP. After extracting the private part from ROP, the owner encrypts the secret part as well as its image descriptor as a private bag, and uploads the private bag to the search cloud. Then, he also uploads the public part of the original photo as a public bag to the sharing cloud (Fig. 1(a)).

# B. Fine-grained Photo Sharing

POP allows fine-grained photo sharing among users. The photo owner uses an access control scheme (e.g., [3], [7]) to encrypt the search keys so that only the authorized users with certain attributes can obtain search keys. As the Step 5 in Fig. 1(a), the owner encrypts the search keys under the access rule that he defines, and the encrypted search keys are uploaded to the sharing cloud and made published. Obtaining the search key, the authorized user can generate valid photo queries and decrypt the private part of ROP. The completed original images can be recovered simply by merging the public parts of images and the private parts of ROPs. Here, all these operations are also automatic and transparent to users, and the authorized user can browse the shared images as usual.

# C. Light-weight Photo Searching

When a querier wants to search a photo among someone else's photos, he pre-processes the querying photo to achieve the corresponding image descriptor. Then, only if satisfying the owner's access rule, he can retrieve the search keys to search on the owner's photos, but it is the cloud who conducts the searching job and returns the result to the querier obliviously, i.e. without knowing contents of the owner's ROPs or the contents of the query photo. After fetching the query result, as mentioned above, system generate the original image for the querier transparently. For the querier, the whole system appears like common image search systems. Fig. 1(b) illustrates the search procedure.

# D. System Design Goals

Our system is designed to achieve efficiency, privacy protection and accuracy goals.

![](images/23cd69b4e231c4c728571f244f1151dc60170122bc7aeebb6c416517e764c316.jpg)  
Fig. 2: Public/Private Part of ROP. Images in the upper row are public part of image and images in the lower row are private part of ROP.

- Efficiency: To overcome the resource limitation of mobile client, operations at the user side should be light-weight, and most of the expensive computations should be outsourced to the cloud side.   
- Privacy Preservation: Users outsource not only the storage of photos but also the searching to the cloud side in $POP$ . Therefore, the framework is expected to protect users' privacy in various aspects:

1. ROP Privacy: Unauthorized party should not learn secret part of ROP including cloud servers,   
2. Query Privacy: Cloud servers should not learn query photos,   
3. Result Privacy: Cloud servers should not learn search results, which are all non-trivial challenges since cloud servers are the party who conducts the searching jobs on the photos stored at his side.   
- Accuracy: Introducing the privacy protection mechanism should not bring much accuracy loss. That is, the search result from $POP$ should be comparable with traditional image search technologies conducted on plain texts of photos.

# E. Threat Model

W.l.o.g., we assume curious-but-honest cloud servers and malicious users in this work. Cloud servers will follow the protocol specification in general, but they will try their best to harvest any information about user's photos. This is a justifiable assumption because deviating from the protocol and not returning a correct search result will lead to bad user experience as well as potential revenue loss of the service provider. However, they might conduct extra work to illegally harvest useful information from the protocol communications in order to infer the secret part of ROP or the contents of queries, which is sensitive information to be protected. On the other hand, queriers may misbehave throughout the protocol to infer the search keys to forge a valid photo query, where the search keys are supposed to be kept secret as well.

# IV. SYSTEM DESIGN

In this section, we first present the building blocks of our system, and then give the detail of our non-interactive private image search protocol, which is the core of the system and one of our main contributions.

# A. Building Blocks of Our System

POP is a modularized and well integrated image sharing and searching system, which consists of several building blocks.

1) Image Search: Image search is composed of three steps: image descriptor extraction, finding matching vector and similarity score calculation.

Extracting Image Descriptor. As described in Section II, the visual descriptor is extracted from the interest points of each photo, where the interest points are automatically detected (e.g., [21]). Then, the descriptor $X = \{x_{1}, x_{2}, \cdots\}$ of an image $I_{x}$ is extracted, where $x_{i}$ is a feature vector.

Matching Feature Vector. Given a feature vector $\mathbf{x} \in \mathbf{X}$ and another descriptor $\mathbf{Y}$ , let $d(\mathbf{x}, \mathbf{y})$ be Euclidean distance between two feature vectors $\mathbf{x} \in \mathbf{X}$ and $\mathbf{y} \in \mathbf{Y}$ . Then given the $\mathbf{x}$ 's nearest neighbor $\mathbf{y}_{nn} \in \mathbf{Y}$ , $\mathbf{x}$ and $\mathbf{Y}$ are a matching pair iff:

$$
\delta \left(\mathbf {x}, \mathbf {Y}\right) = \frac {\mathrm{d} \left(\mathbf {x} , \mathbf {y} _ {n n}\right)}{\min _ {\mathbf {y} \in \mathbf {Y} - \left\{\mathbf {y} _ {n n} \right\}} \left(\mathrm{d} \left(\mathbf {x} , \mathbf {y}\right)\right)} <   \alpha
$$

That is, iff the ratio between nearest distance and the second nearest distance is less than a threshold $\alpha$ , $\mathbf{x}$ and $\mathbf{Y}$ are a matching pair. For most object recognition algorithms, $\alpha$ is set as 0.5.

Similarity Score. Given a querying descriptor X and a queried descriptor Y, the similarity score between X and Y are defined as the number of matching pair X has, i.e.,

$$
\mathrm{S} (\mathbf {X}, \mathbf {Y}) = \sum_ {\mathbf {x} _ {i} \in \mathbf {X}, \delta (\mathbf {x} _ {i}, \mathbf {Y}) <   \alpha} 1 \tag {1}
$$

Given a querying image, matching images with high similarity score can be searched in a database.

2) Cryptographic Tools: Our system also takes advantage of rich cryptographic algorithms for privacy protection in cloud-based image search. It includes: homomorphic encryption, attribute based encryption and oblivious transfer.

Homomorphic Encryption. We employ Paillier's cryptosystem [24] as a building block which has the following homomorphism $^{3}$ : $\mathrm{HE.E}(m_{1})\mathrm{HE.E}(m_{2})=\mathrm{HE.E}(m_{1}+m_{2})$ and $\mathrm{HE.E}(m_{1})^{m_{2}}=\mathrm{HE.E}(m_{1}m_{2})$ , where $\mathrm{HE.E}(m)$ denotes the ciphertext of m. Paillier's cryptosystem is proven to be semantically secure against chosen plaintext attack (SS-CPA), which implies that any ciphertext of any message is indistinguishable to a randomly chosen element among the ciphertext space.

Note that the numeric type of feature vectors may be real number, but the Paillier's cryptosystem is based on large integers, therefore we need to use integers to represent real numbers first. POP uses the fixed point representation to represent real numbers rather than floating-point representation due to its efficiency.

Ciphertext-Policy Attribute Based Encryption We also adopt ciphertext-policy attributed based encryption (CP-ABE) [3] for access control due to its generality and security. Other

Protocol 1 Secret & Search bag generation

1: The owner of $I_{x}$ randomly picks a symmetric key $K_{e}$ and uses symmetric encryption (AES in this paper) to encrypt the private part of the ROP as $\mathsf{AES.E}_{K_{e}}(\mathsf{S}(\mathsf{R}(I_{x})))$ . $K_{e}$ is encrypted via CP-ABE under his privacy policy as $\mathsf{ABE.E}(K_{e})$ .

2: For every dimension $\mathbf{x}(k)$ in every vector $\mathbf{x} \in \mathbf{X}$ , he computes the following homomorphic ciphertexts using his $PK$ and $\mathbf{r}$ :

$$
\mathrm{HE.E} \left(\left(\mathbf {x} (k)\right) ^ {2}\right), \mathrm{HE.E} \left(- \mathbf {r} (k) \cdot \mathbf {x} (k)\right)
$$

attribute based encryption methods can also be adopted, e.g., [7]. In the CP-ABE, a trusted authority (not the image service provider) takes response of generating public parameters. Given the public parameters, a data owner can encrypt a message such that only the users satisfying a certain access rule can decrypt it. Secret keys of users contain attribute values for the key holders, and the access rule is expressed with boolean operators (AND, OR etc.) and attribute values. CP-ABE is proven to be IND-CCA1 secure, which implies the semantic security against chosen plaintext attack.

Oblivious Transfer The k-n oblivious transfer (OT) [6] let a receiver obtain any subset of k items from the sender's n items, while the sender remains oblivious of the receiver's selection, and the receiver remains oblivious of other items as well.

# B. System Join

Whenever a new user joins the system, he generates a pair of Paillier Keys $PK$ , $SK$ and picks a random vector $\mathbf{r}$ , which has the same dimension of the feature vector. Then, he uses CP-ABE to encrypt $PK$ , $SK$ , $\mathbf{r}$ under the access rule he wishes to enforce (i.e. who can search on his images). He uploads the following to the sharing cloud, which are the search keys to be used in the photo searching later.

$$
\mathbf {A B E . E} \left(\{P K, S K, \mathbf {r} \mod n) \right\rbrace
$$

# C. Public & Private Bag Generation

When an owner wants to upload his photo $I_{x}$ , the ROP $\mathbb{R}(I_{x})$ is selected either automatically or manually, and the image descriptor X of ROP is extracted. X is a set of fixed-dimension feature vectors $X = \{x_{1}, x_{2}, x_{3}, \cdots\}$ . A photo may have several ROPs (several persons in the same photo), but w.l.o.g we consider only one ROP per image since multiple ROP is a simple extension. Then, the owner separates the ROP as public ROP P $(\mathbb{R}(I_{x}))$ and secret ROP S $(\mathbb{R}(I_{x}))$ as in Section III-A, and the following public bag is uploaded to the sharing cloud:

$$
I _ {x, \text { pub }} = \left\{I _ {x} - \mathbb {S} \left(\mathbb {R} \left(I _ {x}\right)\right) \right\} \quad (\text { pixel - wise })
$$

After the public bag is uploaded, the owner encrypts the private part of ROP as the private bag using symmetric encryption such as AES-256. Also, for the cloud-based search, he homomorphically encrypts the feature descriptor, which are stored in the search bag (Protocol 1).

Protocol 2 Privacy-preserving Distance Calculation

1: The cloud conducts the following homomorphic operations for all $k$ :

$$
\mathrm{HE.E} \left(- \mathbf {r} (k) \cdot \mathbf {x} _ {i} (k)\right) ^ {2 \mathbf {C} _ {1} \left(\mathbf {y} _ {j} (k)\right)} = \mathrm{HE.E} \left(- 2 \mathbf {x} _ {i} (k) \mathbf {y} _ {j} (k)\right),
$$

$$
\mathrm{HE.E} \left(\left(\mathbf {x} _ {i} (k)\right) ^ {2}\right) \cdot \mathrm{HE.E} (- 2 \mathbf {x} _ {i} (k) \mathbf {y} _ {j} (k)) \cdot \mathbf {C} _ {2} (\mathbf {y} _ {j} (k))
$$

$$
= \mathrm{HE.E} \left(\left(\mathbf {x} _ {i} (k) - \mathbf {y} _ {j} (k)\right) ^ {2}\right)
$$

2: Then, he computes:

$$
\prod_ {k} \mathrm{HE.E} \left(\left(\mathbf {x} _ {i} (k) - \mathbf {y} _ {j} (k)\right) ^ {2}\right) = = \mathrm{HE.E} \left(\mathrm{d} ^ {2} \left(\mathbf {x} _ {i}, \mathbf {y} _ {j}\right)\right)
$$

Then, the private bag and the search bag of $I_{x}$ are:

$$
I _ {x, \text { pri }} = \left\{ \begin{array}{c} \mathsf {A E S}. \mathsf {E} _ {K _ {e}} \left(\mathsf {S} \left(\mathsf {R} \left(I _ {x}\right)\right)\right) \\ \mathsf {A B E}. \mathsf {E} \left(K _ {e}\right) \end{array} \right\}
$$

$$
I _ {x, \mathbf {s c h}} = \left\{ \begin{array}{c} \mathrm{HE.E} (\mathbf {X} ^ {2}) \\ \mathrm{HE.E} (- \mathbf {r} \circ \mathbf {X}) \end{array} \right\}
$$

where $X^{2}$ and $-r \circ X$ represent the sets $\left\{(\mathbf{x}_{i}(k))^{2}\right\}_{\forall i,k}$ and $\{-\mathbf{r}(k) \cdot \mathbf{x}_{i}(k)\}_{\forall i,k}$ (Hadamard product between -r and each $x_{i}$ ) respectively. The private/search bag are uploaded to the sharing/search cloud respectively.

# D. Cloud-based Image Search

When a querier wants to search an image $I_{y}$ among a specific owner's images, he extracts corresponding image descriptor Y and obtains the owner's search keys ABE.E(PK, SK, r) from the server. If he is authorized to search on the owner's images, he will successfully decrypt the search keys and further proceed. Next, he encodes every single dimension of the feature vectors in the querying image as follows:

$$
\mathbf {C} _ {1} \left(\mathbf {y} _ {j} (k)\right) = \mathbf {r} (k) ^ {- 1} \cdot \mathbf {y} _ {j} (k)
$$

$$
\mathbf {C} _ {2} \left(\mathbf {y} _ {j} (k)\right) = \mathrm{HE.E} \left(\left(\mathbf {y} _ {j} (k)\right) ^ {2}\right)
$$

Consequently, the querier achieves two sets of encoded feature descriptors $\mathbf{C}_{1}\left(\mathbf{Y}\right)$ , $\mathbf{C}_{2}\left(\mathbf{Y}\right)$ corresponding to $I_{y}$ . He then sends these two sets to the cloud server to outsource the image search. After receiving the encoded descriptors, the cloud conducts several homomorphic operations to achieve the encrypted pairwise distances between $x_{i}$ and $y_{j}$ for all i,j with $I_{x,sch}$ in the search cloud (Protocol 2). Then, he sends all the ciphertexts of results back to the querier.

Upon receiving the ciphertexts of pair-wise distances, the querier uses $SK$ to decrypt every $\mathrm{d}^2(\mathbf{x}_i, \mathbf{y}_j)$ . Then, he finds the top-2 nearest distances to compute the similarity scores between feature descriptor $\mathbf{X}$ and every $\mathbf{Y}$ according to Eq. 1.

# E. Image Retrieval

Based on the similarity scores, the querier requests the public bags as well as the private bags of the top-k similar images from the sharing cloud (e.g., by requesting the URLs). However, explicit request reveals the search result to the server. Even if every secret part of ROP is encrypted and the query contents are well protected, cloud may infer side information by gathering the statistics of the image retrieval (e.g., popular images and frequently visited images). Thus, we need to hide the retrieval pattern as well.

To achieve this requirement, we employ the k-n OT (Section IV). Since it is extremely expensive to construct a k-n OT with a large n, we do not directly run a k-n OT across the whole database to obliviously retrieve k images. Instead, we try to find a trade-off between privacy and performance as follows. The querier determines a random subset $\sigma' \subseteq DB$ which contains the set of images $\sigma$ that he wants to retrieve. The sizes of $\sigma$ and $\sigma'$ are k and n respectively. Then, the querier and the sharing cloud engage in a k-n OT to let the querier obliviously select the k images.

# V. SECURITY ANALYSIS AND REFINEMENT

# A. Security Analysis

Firstly, the secret part of ROP is well protected by the symmetric encryption, whose key is encrypted with CP-ABE proven to be semantically secure. Besides, the search keys are also protected by the CP-ABE. Therefore, clouds cannot infer sensitive information from its storage in POP.

Next, we prove by the following game that POP reveals no useful information to the cloud servers during the photo search procedure.

Initialize: System is initialized, and relevant cryptosystems (Paillier's cryptosystem, CP-ABE, OT etc.) are initialized by the challenger C. C publishes relevant public keys to the adversary A.

Setup: C generates and encrypts the search keys, and preprocesses a set of photos I by the specification of POP such that A cannot search on I. Then, he publishes the encrypted search keys as well as public/secret/search bags to A.

Phase 1: A achieves polynomial number of encoded descriptors (encoded with C's search keys) without knowing corresponding original descriptors.

Challenge: A submits two photos $I_{0}, I_{1}$ to C. C selects a bit $y \in \{0, 1\}$ uniformly at random, and generates two sets of encoded feature descriptor $\mathbf{C}_{1}(\mathbf{Y}), \mathbf{C}_{2}(\mathbf{Y})$ corresponding to $I_{y}$ (Section IV-D), which are given to A.

Guess: A gives a guess $y'$ on y.

The advantage of $\mathcal{A}$ in this game is defined as $\mathrm{adv} = \Pr [y' = y] - \frac{1}{2}$ . It is not hard to see this is an adversarial cloud server's advantage in inferring, since the game is designed to 'mimic' a cloud server's transaction.

Theorem 1: Any probabilistic polynomial time adversary (PPTA) has at most negligible advantage in above game.

We will present only the key idea for the proof of the theorem because of the space limit. We define two PPTAs $A_{1}$ and $A_{2}$ with limited views, where PPTA $A_{i}$ is only given the encoded feature descriptor $\mathbf{C}_{i}(\mathbf{Y})$ and $A_{i}$ 's advantage is $adv_{i} = Pr[y_{i}' = y]$ . Each PPTA will give his guess $y_{i}'$ on y in the above game with his view. Then, if $A_{1}$ and $A_{2}$ agree on the same guess, A with both views will also give the same guess, otherwise A's advantage does not change. Then, we can achieve the following equation after doing a series of algebraic manipulation to the total probability $Pr[y' = y]$ containing four conditional probabilities:

$$
\mathrm{adv} = \frac {\left(\frac {1}{2} + \mathrm{adv} _ {1}\right) \left(\frac {1}{2} + \mathrm{adv} _ {2}\right)}{\frac {1}{2} - 2 \mathrm{adv} _ {1} \mathrm{adv} _ {2}} - \frac {1}{2}
$$

Both Paillier's cryptosystem and CP-ABE are proved to be semantically secure against chosen plaintext attack $^{4}$ [3], [24]. Hence, A does not have a significant chance to get SK, $r^{-1}$ in ABE. E $(PK, SK, r^{-1})$ or Y in $\mathbf{C}_{2}(\mathbf{Y})$ , which means $adv_{2}$ is negligible. Besides, the function family $x \to \mu x \mod n$ is $\epsilon$ -pairwise independent for negligible $\epsilon$ , and $\mu^{-1}x \mod n$ is close to uniform in $Z_{n}$ . Therefore, he does not have a significant chance to get $y_{j}(k)$ in $C_{1}(y_{j}(k))$ either, which implies a negligible $adv_{1}$ . Since both $adv_{1}, adv_{2}$ are negligible, adv is negligible too. Therefore, adversarial clouds cannot do much better than random guess in the above game, which means the clouds do not learn about sensitive information during the photo search transactions.

Besides the adversarial cloud servers, we have also assumed malicious queriers in our adversarial model. However, unauthorized malicious users are not as threatening as cloud servers since they never get involved in any transaction with valid users. All they can do except compromising the server is to try man-in-the-middle attacks to sniff the search results, but this can be trivially prevented by introducing secure communication channel. Even if they compromised a server, CP-ABE guarantees the indistinguishability of the ciphertexts. In conclusion, malicious users do not learn about sensitive information either.

# B. Refinements for Binary Descriptor

Some image retrieval systems use binary image feature descriptors because they are more compact and computationally manageable than real number ones, with a little accuracy loss in content recognition $[1]$ . It is more suitable for resource-limited applications. However, directly applying POP in mobile platforms with binary descriptors does not fully exploit the advantage of it. The exponentiation operations contribute to majority of the computation overhead in our cryptographic building blocks, but both image owners and queriers need $\Theta(\alpha)$ exponentiations throughout the protocol where $\alpha$ is the number of interest points in a image.

To relax this bottleneck, we further design our framework for the special case where binary descriptors are used (refer to the system as $POP_{bin}$ ), Note that for any two vectors x, y, we have:

$$
\mathrm{d} ^ {2} (\mathbf {x}, \mathbf {y}) = \sum_ {k} (\mathbf {x} (k) - \mathbf {y} (k)) ^ {2} = \sum_ {k} \mathbf {x} (k) \oplus \mathbf {y} (k)
$$

where $\mathbf{x}(k)$ is the k-th bit of x and $\oplus$ is the bitwise XOR operator. Therefore, we consider using a succinct garbled circuit in combination with homomorphic encryption to achieve a lightweight and non-interactive framework dedicated to binary descriptor based search, which is one of our contributions.

1) Yao's Garbled Circuit: To enhance the understanding, we briefly review Yao's garbled circuit (GC), and we direct the readers to relevant literal works [17] for technical details. Yao's Garbled Circuit is designed for two-party computation, where $P_x$ and $P_y$ wish to jointly compute a function $F$ over

$^{4}$ CP-ABE is proved to achieve IND-CPA, which implies SS-CPA.

# Protocol 3 Secret & Search Bag Generation

1: The owner randomly picks a key $K_{e}$ and uses symmetric encryption (AES in this paper) to encrypt the private part of the ROP as $\mathbf{AES.E}_{K_e}(\mathbb{S}(\mathsf{R}(I_x)))$ . $K_{e}$ is encrypted via CP-ABE under his privacy policy as $\mathbf{ABE.E}(K_e)$ .   
2: For every bit $\mathbf{x}(k)$ in every vector $\mathbf{x} \in \mathbf{X}$ , he generates and shuffles the following table:

$$
\text { if } \mathbf {x} (k) = 0
$$

$$
\boxed { \begin{array}{l l} \gamma_ {0} = H ^ {k} (s) \cdot K ^ {0} & \mathsf {A E S}. \mathsf {E} _ {\gamma_ {0}} (\mathsf {H E}. \mathsf {E} (0)) \\ \gamma_ {1} = H ^ {k} (s) \cdot K ^ {1} & \mathsf {A E S}. \mathsf {E} _ {\gamma_ {1}} (\mathsf {H E}. \mathsf {E} (1)) \end{array} }
$$

$$
\begin{array}{c c} \hline \text {if} \mathbf {x} (k) = 1 \\ \hline \gamma_ {0} = H ^ {k} (s) \cdot K ^ {0} & \mathsf {A E S . E} _ {\gamma_ {0}} (\mathsf {H E . E} (1)) \\ \gamma_ {1} = H ^ {k} (s) \cdot K ^ {1} & \mathsf {A E S . E} _ {\gamma_ {1}} (\mathsf {H E . E} (0)) \\ \hline \end{array}
$$

which represents $\mathbf{x}(k)$ 's garbled gate $\mathsf{G}(\mathbf{x}(k))$ .

their private input x and y using a garbled boolean circuit. Here we use an XOR gate as an example.

![](images/6843cdf3830b188a5c3c7428d7b7cb05456ee2cdb1fce70f0dac1e91ca5d7719.jpg)  
Fig. 3: Gate

<table><tr><td> $k_{a}^{0}$ </td><td> $k_{b}^{0}$ </td><td> $\mathbf{AES.E}_{k_{a}^{0}}(\mathbf{AES.E}_{k_{b}^{0}}(k_{z}^{0}))$ </td></tr><tr><td> $k_{a}^{0}$ </td><td> $k_{b}^{1}$ </td><td> $\mathbf{AES.E}_{k_{a}^{0}}(\mathbf{AES.E}_{k_{b}^{1}}(k_{z}^{1}))$ </td></tr><tr><td> $k_{a}^{1}$ </td><td> $k_{b}^{0}$ </td><td> $\mathbf{AES.E}_{k_{a}^{1}}(\mathbf{AES.E}_{k_{b}^{0}}(k_{z}^{1}))$ </td></tr><tr><td> $k_{a}^{1}$ </td><td> $k_{b}^{1}$ </td><td> $\mathbf{AES.E}_{k_{a}^{1}}(\mathbf{AES.E}_{k_{b}^{1}}(k_{z}^{0}))$ </td></tr></table>

TABLE I: Garbled Gate $\mathfrak{G}(w_a\oplus w_b)$

Two random values $k_{i}^{0}, k_{i}^{1}$ are chosen to represent the bit values 0 and 1 for each wire $w_{i}$ . Then, the shuffled Table I represents the garbled XOR gate (shuffled so that inputs are not inferred from the row number). Given two garbled inputs, the evaluator can obliviously evaluate the boolean gate by looking up the shuffled table and decrypting the output to get a garbled output.

2) System Join: The new joiner generates a pair of Paillier keys $PK, SK$ and picks two symmetric encryption keys $K^0, K^1$ as well as a random seed $s$ . Then, he defines a privacy policy to specify which group of people are authorized to search on his images. $PK, SK, K^0, K^1$ and $s$ are encrypted using CP-ABE as ABE.E $\left(\{PK, SK, K^0, K^1, s\}\right)$ , which are uploaded to the sharing cloud as his search keys. Finally, he uses $PK$ to encrypt 0,1 homomorphically for later use, i.e., HE.E(0), HE.E(1).   
3) Public & Private Bag Generation: To upload a photo $I_{x}$ , the owner extracts the ROP $\mathbb{R}(I_{x})$ as well as the binary image descriptor X, and generates the public bag as in the original framework POP. After uploading the public bag to the sharing cloud, he symmetrically encrypts the private part of ROP, and keeps it as well as the key in the private bag. Then, he uses a collision-resistant hash function $H(\cdot)$ and the search keys to garble each bit as a garbled gate (Protocol 3), where $H^{k}(\cdot)$ denotes applying the hash function for k times.

From the protocol, the feature vector x is encrypted to a series of garbled gates (Fig. 4), and the following are

![](images/e05d597957f166ff3a40923eef670dec482122c54c6b36896dc5055a5f207992.jpg)



Fig. 4: Garbled gates G(x) from Protocol 3

# Protocol 4 Privacy-preserving Distance Calculation

1: For every garbled gate $\mathsf{G}(\mathbf{x}_i(k))\in \mathsf{G}(\mathbf{x}_i)$ , the cloud server looks up and symmetrically decrypts HE.E $(\mathbf{x}_i(k)\oplus \mathbf{y}_j(k))$ from the shuffled table.  
2: Then, he computes:

$$
\begin{array}{l} \prod_ {k} \mathrm{HE.E} \left(\mathbf {x} _ {i} (k) \oplus \mathbf {y} _ {j} (k)\right) = \mathrm{HE.E} \left(\sum_ {k} \mathbf {x} _ {i} (k) \oplus \mathbf {y} _ {j} (k)\right) \\ = \mathrm{HE.E} \left(\mathrm{d} ^ {2} \left(\mathbf {x} _ {i}, \mathbf {y} _ {j}\right)\right) \\ \end{array}
$$

corresponding private bag and search bag of $I_{x}$ :

$$
I _ {x, \text { pri }} = \left\{ \begin{array}{c} \mathsf {A E S}. \mathsf {E} _ {K _ {e}} \left(\mathsf {S} \left(\mathsf {R} \left(I _ {x}\right)\right)\right) \\ \mathsf {A B E}. \mathsf {E} \left(K _ {e}\right) \end{array} \right\}
$$

$$
I _ {x, \mathrm{sch}} = \left\{\mathbf {G} (\mathbf {X}) \right\}
$$

4) Cloud-based Image Search: To search a photo $I_{y}$ from other's ones, the querier extracts corresponding descriptor Y and obtains the owner's ABE.E ( $\{PK, SK, K^{0}, K^{1}, s\}$ ). If he successfully decrypts it, he further uses $H^{k}(s)K^{0}$ or $H^{k}(s)K^{0}$ to encode each k-th bit $\mathbf{y}(k)$ as the garbled input GI ( $\mathbf{y}(k)$ ) to finally achieve the set of garbled inputs GI (Y), which is uploaded to the cloud. The cloud server conducts homomorphic operations to achieve HE.E ( $d^{2}(\mathbf{x}_{i}, \mathbf{y}_{j})$ ) for all i, j without interacting with the requester or the image owner (Protocol 4). Then, he sends the ciphertexts back to the querier, who proceeds as POP.

# VI. IMPLEMENTATION AND EVALUATION

# A. Development Environment

We implemented both client side and cloud side of POP. The client side program is developed for Android smartphones and the commodity laptops for performance comparisons, and the cloud side program is developed only for the laptops. We used HTC G17 (1228Hz CPU, 1G RAM) and ThinkPad X1 (i7, 2.7GHz CPU, 4G RAM).

The CP-ABE is implemented based on the PBC library, and other building blocks (SectionIV) are implemented in Java, including the AES (128-bit), Paillier's cryptosystem (512-bit primes $p, q$ ), $k-n$ oblivious transfer and the fixed point operations. Based on these building blocks, we implemented the core protocols in both variants $POP$ and $POP_{bin}$ . The automatic ROP detection is implemented with cascade object detection (e.g., face detection) [31]. We employed widely used 64-dimensional SURF descriptor [2] and 128-dimensional SIFT descriptor [18] for the variant of real number descriptors ( $POP$ ), and 64 bit binary SURF and 128 bit binary SIFT for $POP_{bin}$ . Although our evaluation is conducted with these descriptors, our system is compatible with other vector-based descriptors too. Both the object detection and descriptor extraction are implemented using the image process library OpenCVfor Window and Android. ROP separation (Mask, P3 [26], and Blur) is also implemented with it.

# B. Real-life Datasets

To measure the privacy protection and the cost of POP, we used the well-known Labelled Faces in the Wild (LFW) dataset [11], which consists of 30,281 real-life images collected from news photographs. We detect all human faces automatically and set those faces as ROPs of images, and 9 feature vectors are extracted as their image descriptor [19]. On average, ROP occupies less than 20% of each image for 80% images. We also used the INRIA Holidays dataset [12], which contains 1,491 high-resolution personal photos taken during their holidays (majority with resolution $2560px \times 1920px$ ). We set the entire image of the INRIA as the ROP.

![](images/9d23a6c553715550bae5ddd2707176f7311db7067e04628cbe57f1e660f9165e.jpg)



(a) LFW

![](images/aa8c12fcb91f0d335948ef322ddb9379d0bd6793c2caae6790957ed6928d3130.jpg)



(b) Holiday   
Fig. 5: Run time of ROP separation

# C. Image Recognition on Public Part

ROPs are separated in three different methods (Mask, P3 and Blur) respectively. To evaluate the safety against the object detection algorithms, we ran face detection $[31]$ and feature points detection $[16]$ algorithms on the public part of ROPs. On average, there are 1.1 faces in each original image in LFW, but only 0.017, 0.029 and 0.028 faces are detected in the public part of the ROPs generated by Mask, P3 and Blur respectively, and our manual examination shows that majority of the detections were false positives (e.g., some textures being detected as faces). Therefore, we conclude that almost no faces are detected in the public parts of images by algorithm. Also, no matched feature points are detected in the public parts of ROPs for both LFW and Holiday datasets as well. As a conclusion, all three methods provide good privacy protection against face/feature detection algorithms.

We also compare the computation cost and storage cost of three methods. Figure 5 illustrates the CDF of run time for processing each image with three methods. On average, Mask has the minimum computation cost with 0.0002s per image in LFW Dataset, and 0.02s per image in Holiday Dataset; Blur needs 0.037s for LFW Dataset and 0.68s for Holiday Dataset; P3 needs 0.35s for LFW Dataset and 24.9s for Holiday Dataset. This result also confirms that protecting the entire image is much more expensive than protecting the subregions of the image. Figure 6 and 7 present the normalized storage cost of three methods for LFW and Holiday. The sizes of Blur-processed images are only 73% of the original ones in Holiday dataset on average. In conclusion, Mask and Blur outperforms P3 in computation performance while Blur has the best storage performance, therefore POP uses Blur as the default method.

# D. Search Accuracy

In POP, the search procedure follows exactly the same vector-based similarity comparison as typical image search technologies (e.g., [25]). Also, the accuracy loss introduced by

TABLE II: Microbenchmarks (a) Image pre-process (LFW/Holiday) 

<table><tr><td colspan="4">Laptop (sec)</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Detect feature</td><td>0.28 / 8.7</td><td>0.17/1.56</td><td>1.21/12.03</td></tr><tr><td>Separate ROP</td><td>0.037/0.68</td><td>0.009/0.07</td><td>0.266/1.26</td></tr><tr><td>Encrypt S(R(I))</td><td>0.001/0.038</td><td>0.001/0.018</td><td>0.008/0.054</td></tr><tr><td colspan="4">Smartphone (sec)</td></tr><tr><td>Detect feature</td><td>0.46/15.6</td><td>0.21/4.32</td><td>1.85/22.7</td></tr><tr><td>Separate ROP</td><td>0.08/1.53</td><td>0.024/0.19</td><td>0.37/2.73</td></tr><tr><td>Encrypt S(R(I))</td><td>0.005/0.057</td><td>0.001/0.028</td><td>0.015/0.13</td></tr></table>

(b) Image search (average run time) 

<table><tr><td colspan="3">Laptop (sec)</td></tr><tr><td>POP</td><td>64 dimension</td><td>128 dimension</td></tr><tr><td>Encrypt Vector (owner)</td><td>1.02</td><td>2.01</td></tr><tr><td>Encode Vector (querier)</td><td>0.55</td><td>1.12</td></tr><tr><td>Decrypt Distance</td><td>0.016</td><td>0.016</td></tr><tr><td> $POP_{bin}$ </td><td>64 dimension</td><td>128 dimension</td></tr><tr><td>Encrypt Vector (owner)</td><td>0.51</td><td>1.03</td></tr><tr><td>Encode Vector (querier)</td><td>&lt; 0.001</td><td>&lt; 0.001</td></tr><tr><td>Decrypt Distance</td><td>0.016</td><td>0.016</td></tr><tr><td colspan="3">Smartphone (sec)</td></tr><tr><td>POP</td><td>64 dimension</td><td>128 dimension</td></tr><tr><td>Encrypt Vector (owner)</td><td>1.85</td><td>3.91</td></tr><tr><td>Encode Vector (querier)</td><td>0.64</td><td>1.37</td></tr><tr><td>Decrypt Distance</td><td>0.024</td><td>0.024</td></tr><tr><td> $POP_{bin}$ </td><td>64 dimension</td><td>128 dimension</td></tr><tr><td>Encrypt Vector (owner)</td><td>0.56</td><td>1.33</td></tr><tr><td>Encode Vector (querier)</td><td>&lt; 0.001</td><td>&lt; 0.001</td></tr><tr><td>Decrypt Distance</td><td>0.024</td><td>0.024</td></tr></table>

the fixed point representation is almost negligible (less than $\frac{1}{base^{scale}}$ in each value where base is often 10 and scale is greater than 5), therefore POP provides a comparable accuracy as existing image search techniques.

# E. Client Side Performance

1) Computation Overhead: For the photo owner, the computation overhead mainly comes from the following operations: (1) object detection and descriptor extraction; (2) ROP separation by Blur; (3) symmetric encryption of secret part; (3) descriptor encryption, which are all in the public & private bag generation. For the querier, the expensive operations include: (1) descriptor extraction; (2) descriptor encoding; (3) distance results decryption; (4) similarity calculation, which are all in the cloud-based photo searching. The time cost for other operations, e.g., fix point presentation conversion, are negligible. The cost for search key encryption and decryption by CP-ABE can also be ignored, since this is a one-time operation for each user which are sub-second.

As microbenchmark tests for each procedure (Table II), Table II(a) shows that protecting subregions (e.g., faces) of a image only takes the owner 0.31s to extract the descriptor and separate the ROP, while protecting the whole image takes 9.38s. Table II(b) presents the computation overhead of main procedures in POP and $POP_{bin}$ .

Public & Private Bag Generation Binary feature vector reduces the owner's computation overhead by half to 0.51s per feature vector. In a typical scenario in LFW dataset, there are only 9 feature vectors for each face. if we use 64 dimensional SURF descriptor, it takes 9.5s on laptops and 17s on smartphones to generate the public bag, private bag and search bag. When we use binary descriptor [25], the cost is reduced to 4.9s on laptops and 5.6s on smartphones, which is a significant reduction.

![](images/009298cfd273ae92a770e31b34fc723fc54cf08047cea30a7788aafe40c73998.jpg)



(a) Public

![](images/fdbc2fe488c7ecd0db8a92ca8a99dab799c110d4fa97f0aa7042045d0e6dd907.jpg)



(b) Secret

![](images/8eb03c63350ca73a132cba84e0ecdf5a172a4d7296a0867765ca42ef008845e5.jpg)



(c) Public+Secret

Fig. 6: Storage cost of three methods for the LFW dataset. (ROP is defined as faces). The cost is normalized by the original image file size.   
![](images/176879138d99a59e8a9ce2c61bf3be4d3254b0884f0f36d815a08981fa1664a8.jpg)



(a) Public Image

![](images/cb929666cac4665f25fd268046f8c7401b27f7c88977a2e1d9c31f5a0e3136b9.jpg)



(b) Secret Image

![](images/7e45c55f4f3393cf074f921260df70af0e74007b55c86daeecbb7f49749f2ea7.jpg)



(c) Public+Secret   
Fig. 7: Storage cost of three methods for the Holiday dataset. (ROP is defined as the whole image. The cost is normalized by the original image file size.

Cloud-based Photo Searching It takes a querier roughly 1s to encode the querying descriptor in POP. The run time becomes negligible in $POP_{bin}$ , and this is especially desirable for mobile devices. After the querier obtains the search result, it takes 0.016s on laptops and 0.024s on smartphones to decrypt each encrypted distance in both variants. In the LFW dataset, if a querier searches a photo among 1,000 photos, it takes 14s to process the search result on laptops and 22s on the smartphones on average. It is slightly beyond acceptable if owners have hundreds of photos on average. However, this non-negligible extra overhead comes from the linear search in all photos of an owner with a linear complexity, and it is promising and not trivial to reduce the complexity with existing optimized search mechanisms such as k-d tree [22]. Thus, the scalability can be achieved using those search algorithms.

2) Communication Overhead: The communication overhead for the image owner mainly comes from uploading public bag and private bag to the cloud. When using Blur to separate ROPs, as presented in Figure 6 and 7, the size of the public part is 90% of the original image in LFW Dataset and only 9.8% in Holiday Dataset. The size of the secret part is 16% in LFW Dataset and 63% in Holiday Dataset. The average size of encrypted descriptor is 72KB per image for both variants, and this can be further reduced to 690B per image when using a common lossless compression, e.g., ZIP. As a summary, for the LFW Dataset, the extra communication cost brought by POP or $POP_{bin}$ is roughly 6% of that for system without privacy consideration. But for the Holiday Dataset, our method actually save the communication cost by 27%.

The communication overhead for uploading the encoded feature descriptors (query) is approximately 36 KB in POP and 9 KB in $POP_{bin}$ , which are reduced to 350B and 90B respectively after compression. The communication overhead for downloading the similarity result is 128B for each compared image in the database, and the one for downloading each image is similar to the uploading overhead of the image owner. Note that, to achieve k-n oblivious transfer, the querier needs to download $(n - k)$ extra images from the search server to hide the search pattern, where n can be specified according to the trade-off between privacy and performance.

# F. Cloud Side Performance

On the clouds, similarly, the image storage and communication is 6% more for LFW Dataset and 27% less for Holiday Dataset. The main computation overhead is from the distance computation. We evaluated the search performance on

TABLE III: Vector distance computation cost (64/128-dimension) 

<table><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>Real number</td><td>0.18/0.36</td><td>0.16/0.35</td><td>0.19/0.37</td></tr><tr><td>Binary</td><td>0.018/0.035</td><td>0.003/0.013</td><td>0.046/0.078</td></tr></table>

laptops, (Table III), so the actual performance when deployed in more powerful cloud servers will be significantly improved. Our privacy-preserving distance protocols take nearly 0.18s to calculate the distance between two real number feature vectors (POP) and only 0.018s for binary feature vectors ( $POP_{bin}$ ). For well studied objects like faces (9 feature vectors in a descriptor), and for each owner, there are usually hundreds of images on the cloud. The computation time for a laptop to process one request is less than one minute. When there are large-scale complicated images whose ROPs may contain random objects other than faces, the optional optimization methods introduced may be introduced to reduce the query response time.

# VII. RELATED WORK

Image Privacy Protection A set of solutions are proposed to mask sensitive contents of images, e.g., human faces, to prevent any potential breach of owners' privacy, e.g., [4] and [29]. P3 [26] proposes to separate an image into a private part and a public part and simply encrypted the private part. But the produced public parts of those works are of limited utility and disable search on them. There are some literal works providing privacy-preserving face recognition in a face photos database [9], [28]. Those methods provide privacy protection to the requested images as well as the outcome, but the result is not secure against photo service provider and those works do not consider personal photo storage and sharing. Supporting privacy-preserving image search with untrusted server is still an open problem.

Privacy Preserving Cloud Services Many research efforts have been devoted to provide secure cloud-based storage, sharing and searching services to users. Those privacy preserving outsourced storage and sharing systems, e.g., [13] and [32], provide well access control to private data, but cannot support search on encrypted data. Searchable encryption is proposed to enable secure search over encrypted data via keywords. Reza et al. [8] proposed a thorough discussion on the framework of SSE. But the existing approaches, e.g., [15], [27], are focus on keywords search by examining the occurrences of the searched terms (or words). They are not suitable for content-based image search since they cannot measure the distance between encrypted feature vectors.

Privacy-preserving Euclidean Distance Euclidean distance can be computed privately among parties using secure multi-party computation (SMC) methods $[17]$ , $[33]$ . However, it requires online interaction between the image owner and queriers, and is unsuitable for the cloud based image service, where the owners are not guaranteed to stay online. Even using asynchronous SMC, the computation and communication overhead are exponentially large. $[23]$ proposes an approach using Fourier-related transforms to hide accurate sensitive data and to approximately preserve Euclidean distances among them. It works well for some data mining purposes on common datasets, but for feature vectors the distances still reveal information of the objects in images.

# VIII. CONCLUSION

We present a framework POP, which enables cloud servers to provide privacy-preserving photo sharing and searching service to mobile device users who intend to outsource photo management while protecting their privacy in photos. Our framework not only protects the outsourced photos so that no unauthorized users can access them, but also enables users to encode their image search so that the search can also be outsourced to an untrusted cloud server obliviously without leakage on the query contents or results. Our analysis shows the security of the framework, and the implementation shows a small storage overhead and communication overhead for both mobile clients and cloud servers.

# IX. ACKNOWLEDGMENT

This research is partially supported by NSFC 61125020 and NSFC 61472218. The research of Li is partially supported by NSF CNS-1035894, NSF ECCS-1247944, NSF CMMI 1436786, National Natural Science Foundation of China under Grant No. 61170216, No. 61228202 and No. 61272426.

# REFERENCES

[1] A. Alahi, R. Ortiz, and P. Vandergheynst, “Freak: Fast retina keypoint,” in CVPR. IEEE, 2012.   
[2] H. Bay, A. Ess, T. Tuytelaars, and L. Van Gool, “Speeded-up robust features (surf),” CVIU, vol. 110, no. 3, pp. 346–359, 2008.

[3] J. Bethencourt, A. Sahai, and B. Waters, “Ciphertext-policy attribute-based encryption,” in S&P. IEEE, 2007, pp. 321–334.   
[4] C. Bo, G. Shen, J. Liu, X.-Y. Li, Y. Zhang, and F. Zhao, “Privacy. tag: Privacy concern expressed and respected,” in SenSys. ACM, 2014.   
[5] M. Calonder, V. Lepetit, C. Strecha, and P. Fua, “Brief: Binary robust independent elementary features,” in ECCV, 2010.   
[6] J. Camenisch, G. Neven et al., “Simulatable adaptive oblivious transfer,” in EUROCRYPT. Springer, 2007, pp. 573–590.   
[7] M. Chase and S. S. Chow, “Improving privacy and security in multi-authority attribute-based encryption,” in CCS. ACM, 2009.   
[8] R. Curtmola, J. Garay, S. Kamara, and R. Ostrovsky, “Searchable symmetric encryption: improved definitions and efficient constructions,” in CCS. ACM, 2006.   
[9] Z. Erkin, M. Franz, J. Guajardo, S. Katzenbeisser, I. Lagendijk, and T. Toft, “Privacy-preserving face recognition,” in Privacy Enhancing Technologies. Springer, 2009, pp. 235–253.   
[10] C. Gentry, “Fully homomorphic encryption using ideal lattices.” in STOC, vol. 9, 2009, pp. 169–178.   
[11] G. B. Huang, M. Ramesh, T. Berg, and E. Learned-Miller, “Labeled faces in the wild: A database for studying face recognition in unconstrained environments,” Tech. Rep.   
[12] H. Jegou, M. Douze, and C. Schmid, “Hamming embedding and weak geometric consistency for large scale image search,” in ECCV, 2008.   
[13] T. Jung, X.-Y. Li, Z. Wan, and M. Wan, “Privacy preserving cloud data access with multi-authorities,” in INFOCOM. IEEE, 2013.   
[14] B. Leibe, E. Seemann, and B. Schiele, “Pedestrian detection in crowded scenes,” in CVPR. IEEE, 2005.   
[15] M. Li, S. Yu, W. Lou, and Y. T. Hou, “Toward privacy-assured cloud data services with flexible search functionalities,” in ICDCSW. IEEE, 2012.   
[16] T. Lindeberg, “Feature detection with automatic scale selection,” IJCV, vol. 30, no. 2, pp. 79–116, 1998.   
[17] Y. Lindell and B. Pinkas, “A proof of yao’s protocol for secure two-party computation.” IACR Cryptology ePrint Archive, p. 175, 2004.   
[18] D. G. Lowe, “Distinctive image features from scale-invariant keypoints,” IJCV, vol. 60, no. 2, pp. 91–110, 2004.   
[19] J. Luo, Y. Ma, E. Takikawa, S. Lao, M. Kawade, and B.-L. Lu, “Person-specific sift features for face recognition,” in ICASSP. IEEE, 2007.   
[20] M. McDonnell, “Box-filtering techniques,” Computer Graphics and Image Processing, vol. 17, no. 1, pp. 65–70, 1981.   
[21] K. Mikolajczyk and C. Schmid, “Scale & affine invariant interest point detectors,” IJCV, vol. 60, no. 1, pp. 63–86, 2004.   
[22] M. Muja and D. G. Lowe, “Fast approximate nearest neighbors with automatic algorithm configuration.” in VISAPP (1), 2009, pp. 331–340.   
[23] S. Mukherjee, Z. Chen, and A. Gangopadhyay, “A privacy-preserving technique for euclidean distance-based mining algorithms using fourier-related transforms,” VLDB Journal, vol. 15, no. 4, pp. 293–315, 2006.   
[24] P. Paillier, “Public-key cryptosystems based on composite degree residuosity classes,” in EUROCRYPT. Springer, 1999, pp. 223–238.   
[25] K. Peker, “Binary sift: Fast image retrieval using binary quantized sift features,” in CBMI, 2011.   
[26] M.-R. Ra, R. Govindan, and A. Ortega, “P3: Toward privacy-preserving photo sharing,” in NSDI. USENIX, 2013.   
[27] Y. Ren, Y. Chen, J. Yang, and B. Xie, “Privacy-preserving ranked multi-keyword search leveraging polynomial function in cloud computing,” in Globecom. IEEE, 2014.   
[28] A.-R. Sadeghi, T. Schneider, and I. Wehrenberg, “Efficient privacy-preserving face recognition,” in Information, Security and Cryptology. Springer Berlin Heidelberg, 2010, pp. 229–244.   
[29] P. Simoens, Y. Xiao, P. Pillai, Z. Chen, K. Ha, and M. Satyanarayanan, "Scalable crowd-sourcing of video from mobile devices," in MobiSys. ACM, 2013.   
[30] M. Turk and A. Pentland, “Eigenfaces for recognition,” Journal of cognitive neuroscience, vol. 3, no. 1, pp. 71–86, 1991.   
[31] P. Viola and M. J. Jones, “Robust real-time face detection,” International journal of computer vision, vol. 57, no. 2, pp. 137–154, 2004.   
[32] B. Wang, B. Li, and H. Li, “Oruta: Privacy-preserving public auditing for shared data in the cloud,” in CLOUD. IEEE, 2012.   
[33] L. Zhang, X.-Y. Li, Y. Liu, and T. Jung, “Verifiable private multi-party computation: ranging and ranking,” in INFOCOM. IEEE, 2013.