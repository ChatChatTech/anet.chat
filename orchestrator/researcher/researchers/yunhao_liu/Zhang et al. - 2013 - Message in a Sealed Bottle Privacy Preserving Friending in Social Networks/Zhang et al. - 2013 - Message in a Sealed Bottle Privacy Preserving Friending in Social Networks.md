# Message in a Sealed Bottle: Privacy Preserving Friending in Social Networks

Lan Zhang∗, Xiang-Yang Li,†, Yunhao Liu,∗‡ ∗ Department of Computer Science and Technology, School of Software, TNList, Tsinghua University † Department of Computer Science, Illinois Institute of Technology ‡ Department of Computer Science and Engineering, HKUST

Abstract—Many proximity-based mobile social networks are developed to facilitate connections between any two people, or to help a user to find people with a matched profile within a certain distance. A challenging task in these applications is to protect the privacy of the participants’ profiles and personal interests.

In this paper, we design novel mechanisms, when given a preference-profile submitted by a user, that search persons with matching-profile in decentralized multi-hop mobile social networks. Our mechanisms also establish a secure communication channel between the initiator and matching users at the time when the matching user is found. Our rigorous analysis shows that our mechanism is privacy-preserving (no participants’ profile and the submitted preference-profile are exposed), verifiable (both the initiator and the unmatched user cannot cheat each other to pretend to be matched), and efficient in both communication and computation. Extensive evaluations using real social network data, and actual system implementation on smart phones show that our mechanisms are significantly more efficient than existing solutions.

Index Terms—Private Profile Matching, Secure Communication, Decentralized Mobile Social Networks.

# I. INTRODUCTION

A boom in mobile hand-held devices greatly enriches the social networking applications. Many social networking services are available on mobile phones (e.g., JuiceCaster, MocoSpace and WiFace [23]) and majority of them are location-aware (e.g., FourSquare, BrightKite and Loopt). However, most of them are designed for facilitating people connections based on their real life social relationship [15], [19]. There is an increasing difficulty of befriending new people or communicating with strangers while protecting the privacy of real personal information.

Friending and communication are two important basic functions of social networks. When people join social networks, they usually begin by creating a profile, then interact with other users. Profile matching is a common and helpful way to make new friends with common interests or to search for experts [22]. Some applications help a user automatically find users with similar profile within a certain distance. For example, in the social network Color, people in close proximity (within 50 meters) can share photos automatically based on their similarity. MagnetU [1] matches one with nearby people for dating, friend-making. Small-talks [21] connects proximate users based on common interests. These applications use profiles to facilitate friending between proximate strangers and enable privacy preserving people searching to some extent.

Observe that in practice the mobile Internet connection may not always be available and it may incur high expense. Thus, in this work we focus on proximity-based decentralized mobile social networks (MSN) based on short-range wireless technologies such as WiFi and Bluetooth. However the increasing privacy concern becomes a barrier for adopting MSN. People are unwilling to disclose personal profiles to arbitrary persons in physical proximity before deciding to interact with them. The insecure wireless communication channel and potentially untrusted service provider increase the risk of revealing private information.

Friending based on private profile matching allows two users to match their personal profiles without disclosing them to each other. There are two mainstreams of approaches to solve this problem. The first category provides private attributes matching based on private set intersection (PSI) and private cardinality of set intersection (PCSI), [12], [20]. The second category measures the social proximity by private vector dot product [7], [9], [25]. They rely on public-key cryptosystem and homomorphic encryption, which results in expensive computation cost and usually requires a trusted third party. Multiple rounds of interactions are required to perform the presetting (e.g. exchange public keys) and private matching between each pair of users. Moreover, most protocols are unverifiable: there lack efficient methods to verify the result. Furthermore, in these approaches, matched users and unmatched users all get involved in the expensive computation and learn their matching results (e.g. profile intersection) with the initiator. These limitations hinder the adoption of the SMCrelated private matching methods in MSN.

A secure communication channel is equally important in MSN. Although the matching process is private, the following chatting may still be disclosed to the adversary and more privacy may be leaked. Most protocols assume that there is a secure communication channel established by using publickey cryptosystem. This involves a trusted third party and key management, which is difficult to manage in decentralized MSN.

Facing these challenges, we first formally define the privacy preserving verifiable profile matching problem in decentralized MSN (Section II). We then propose several protocols (Section

III) to address the privacy preserving profile matching and secure communication channel establishment in decentralized social networks without any presetting or trusted third party. We take advantage of the common attributes between matching users, and use it to encrypt a message with a secret channel key in it. In our mechanisms, only a matching user can decrypt the message. A privacy-preserving profile matching and secure channel construction are completed simultaneously with one round communication. The secure channel construction resists the Man-in-the-Middle attack. Both precise and fuzzy matching/search in a flexible form are supported. The initiator can define a similarity threshold, the participant whose similarity is below the threshold learns nothing. A sequence of welldesigned schemes make our protocols practical, flexible and lightweight, e.g., a remainder vector is designed to significantly reduce the computation and communication overhead of unmatched users. Our profile matching mechanisms are also verifiable which thwart cheating about matching result. We also design a mechanism for location privacy preserved vicinity search based on our basic scheme. Compared to most existing works (Section VI) relying on the asymmetric cryptosystem and trusted third party, our protocols require no presetting and much less computation. To the best of our knowledge, these are the first privacy-preserving verifiable profile matching protocols based on symmetric cryptosystem.

We rigorously analyze the security and performance of our mechanisms (Section IV). We then conduct extensive evaluations on the performances of our mechanisms using large scale social network data, Tencent Weibo. Our results (Section V) show that our mechanisms outperform existing solutions significantly. We also implement our protocols on laptop and mobile phone and measure the computation and communication cost in real systems. In our mobile-phone implementation, a user only needs about 1.3ms to generate a friending request. On average, it only takes a non-candidate user about 0.63ms and a candidate user 7ms to process this request.

# II. SYSTEM MODEL AND PROBLEM DEFINITION

# A. System Model

A user in a mobile ad hoc social networking system usually has a set of attributes. The attribute can be anything generated by the system or input by the user, including his/her location, places he/she has been to, his/her social groups, experiences, interests, contacts, keywords of his/her blogs, etc. According to our analysis of two well-known social networking systems (Facebook and Tencent Weibo [2]), more than 90% users have unique profiles. Thus for most users, the complete profile can be his/her fingerprint in social networks. Then, in most social networks, friending usually takes two typical steps: profile matching and communication. These applications cause a number of privacy concerns.

1) Profile Privacy: The profiles of all participants, including the initiator, intermediate relay users and the matched targets, should not be exposed without their consents. For

participants, protecting their profiles is necessary and can reduce the barrier to participate in MSN. Note that, the exact location information is also a part of the user’s profile privacy.

2) Communication Security: The messages between a pair of users should be transmitted through a secure communication channel. We emphasize that the secure communication channel establishment has been ignored in most previous works which address the private profile matching in decentralized MSN. In practice, after profile matching, more privacy, even profile information, may be exposed via communication through an insecure channel.

In this paper, we address the verifiable privacy preserving profile matching and secure communication channel establishment in decentralized MSN without any presetting or trusted third party. Formally, each user $v _ { k }$ in a social network has a profile set $A _ { k }$ consisting of $m _ { k }$ attributes, $\begin{array} { r l } { A _ { k } } & { { } = } \end{array}$ $\{ a _ { k } ^ { 1 } , a _ { k } ^ { 2 ^ { - } } , . . . , a _ { k } ^ { m _ { k } } \}$ . The number of attributes is not necessary the same for different users. An initiator $v _ { i }$ represents his/her desired user by a request profile with $m _ { t }$ attributes as $A _ { t } =$ $\{ a _ { t } ^ { 1 } , a _ { t } ^ { 2 } , . . . , a _ { t } ^ { m _ { t } } \}$ . Our mechanism allows the initiator to search a matching user in a flexible way by constructing the request profile in the form of $A _ { t } = ( N _ { t } , O _ { t } )$ . Here

• $N _ { t }$ consists of α necessary attributes. All of them are required to be owned by a matching user;   
• $O _ { t }$ consists of the rest $m _ { t } - \alpha$ optional attributes. At least β of them should be owned by a matching user.

The acceptable similarity threshold of a matching user is $\theta =$ $\frac { \alpha + \beta } { m _ { t } }$ . Let $\gamma = m _ { t } - \alpha - \beta$ . When $\gamma = 0 ,$ , a perfect match is required. A matching user $v _ { m }$ with a profile $A _ { m }$ must satisfy that

$$
N _ {t} \subset A _ {m} \text {   and   } | O _ {t} \cap A _ {m} | > \beta . \tag {1}
$$

When $A _ { t } ~ \subset ~ A _ { m } , ~ v _ { m }$ is a perfect matching user. In a decentralized MSN, a request will be spread by relays until hitting a matching user or meeting a stop condition, e.g. expiration time. Then the initiator $v _ { i }$ and the matching user $v _ { m }$ decide whether to connect each other.

# B. Adversary Model

In the profile matching phase, if a party obtains one or more users (partial or full) attribute sets without their explicit consents, it is said to conduct user profiling [12]. Two types of user profiling are taken into consideration.

In the honest-but-curious (HBC) model, a user tries to learn more profile information than allowed by inferring from the information he/she receives but honestly follow the mechanism. In a malicious model, an attacker deliberately deviates from the mechanism to learn more profile information or cheat. In this work we consider several powerful malicious attacks.

Definition 1 (Dictionary profiling): A powerful attacker who has obtained the dictionary of all possible attributes tries to determine a specific user’s attribute set by enumerating or guessing all likely attribute sets.

Definition 2 (Cheating): In the process of profile matching, a participant may cheat by deviating from the agreed protocol, e.g., cheat the initiator with a wrong matching conclusion. Most existing private profile matching approaches are vulnerable to the dictionary profiling attack and cheating.

In the communication phase, an adversary can learn the messages by eavesdropping. The construction of a secure channel may suffer the Man-in-the-Middle (MITM) attack.

There are other saboteur attacks. e.g. the deny of service (DoS) attack can be prevented by restricting the frequency of relaying requests from the same user. Some saboteur behaviors are precluded, such as altering or dropping the requests or replies.

# C. Design Goal

The main goal and great challenge of our mechanism is to conduct efficient matching against the user profiling and cheating, as well as establish a secure communication channel thwarting the MITM attack in a decentralized manner. In our mechanism, a user’s privacy is protected from the user whose similarity is not up to his/her defined threshold. Specifically, we define different privacy protection levels $P P L ( A _ { k } , v _ { j } )$ of a profile $A _ { k }$ of $v _ { k }$ against a user $v _ { j }$ .

Definition 3 (Privacy Protection Level): Four different privacy protection levels will be discussed in this work:

PPL0: If $P P L ( A _ { k } , v _ { j } ) = 0 , v _ { j }$ can learn the profile $A _ { k }$

PPL1: If $P P L ( A _ { k } , v _ { j } ) = 1 , v _ { j }$ can learn the intersection of $A _ { k }$ and $A _ { i }$ .

PPL2: If $P P L ( A _ { k } , v _ { j } ) = 2 , v _ { j }$ can learn the α necessary attributes of $A _ { k }$ and the fact that at least β optional attributes are satisfied. Specially, when $\alpha = 0 , v _ { j }$ learns the fact that the cardinality of $A _ { k } \cap A _ { j }$ exceeds the threshold.

PPL3: If $P P L ( A _ { k } , v _ { j } ) = 3 , v _ { j }$ learns nothing about $A _ { k }$ .

We design our mechanism to achieve PPL2 against matching users and PPL3 against unmatched users in both HBC and malicious model and thwart cheating. We also optimize the mechanism to reduce the overhead for unmatched users. Furthermore, in our mechanism human interactions are needed only to decide whether to connect their matching users.

# III. PRIVACY PRESERVING PROFILE MATCHING AND SECURE COMMUNICATION

# A. Basic Mechanism

Observe that the intersection of the request profile and the matching profile is a nature common secret shared by the initiator and the matching user. Our main idea is to use the request profile as a key to encrypt a message. Only a matching user, who shares the secret, can decrypt the message efficiently.

Figure 1 illustrates our basic privacy preserving search and secure channel establishment mechanism. Here, we first draw an outline of how the initiator creates a request package and how a relay user handles the request package.

The initiator starts the process by creating a request profile characterizing the matching user and a secret message containing a channel key for him/her. The request profile is a set of sorted attributes. Then he/she produces a request profile vector by hashing the attributes of the request profile one by one. A profile key is generated based on the request profile vector using some publicly known hashing function. The initiator encrypts the secret message with the profile key. A remainder vector of the profile vector is yield for fast exclusion by a large portion of unmatched persons. To support a flexible fuzzy search requiring no perfect match, the initiator can define the necessary attributes, optional attributes and the similarity threshold of the matching profile. And a hint matrix is constructed from the request vector according to the similarity definition, which enables the matching person to recover the profile key. In the end, the initiator packs the encrypted message, the remainder vector and the hint matrix into a request package and sends it out. Note that the required profile vector will not be sent out.

When a relay user receives a request from another user, he/she first processes a fast check of his/her own profile vector with the remainder vector. If no sub-vector of his/her profile vector fits the remainder vector, he/she knows that he/she is unmatched and will forward the request to other relay users immediately. Otherwise, he/she is a candidate target and will generate a candidate profile vector set by some linear computation with his/her profile and the hint matrix. Then a candidate profile key set is obtained. In the basic mechanism, If any of his/her candidate keys can decrypt the message correctly, he/she is an matching user and the searching and secret key exchange complete. Otherwise, he/she just forwards the request to other relay users.

# B. Profile Vector and Key Generation

To protect the profile privacy and support a fuzzy search, a cryptographic hash (e.g. SHA-256) of the attribute is adopted as the attribute equivalence criterion in this mechanism. However, due to the avalanche effect, even a small change in the input will result in a mostly different hash. Although consistent attribute name can be provided by the social networking service, the attribute fields or the tags are created by users. Some inconsistency may be caused by letter case, punctuation, spacing, etc.. For example, ”basketball” and ”Basketball” generate totally different cryptographic hashes. So a profile normalization is necessary before the cryptographic hashing to ensure two attributes which are considered equivalent to yield the same hash value. Words normalization has been well studied in research areas like search engines and corpus management [18]. In our mechanism, we use some common techniques to normalize the users profile, including removing whitespace, punctuation, accent marks and diacritics, converting all letters to lower case, converting numbers into words, text canonicalization, expanding abbreviations, converting the plural words to singular form. After the profile normalization, most inconsistences caused by spelling and typing are eliminated. The sematic equivalence between two different words are not in this paper’s consideration.

Assume the cryptographic hash function is H which yields n-bit length hash value. With a sorted normalized profile

![](images/f1da112a2746850c8a27cd7aa82ed57d3611891362438675352c51e3a7d2e828.jpg)



Fig. 1. The procedure to create a request package by the initiator and handle a request package by some forwarder.

$A _ { k } = [ a _ { k } ^ { 1 } , a _ { k } ^ { 2 } , . . . , a _ { k } ^ { m } ] ^ { T }$ , a profile vector is $H _ { k } = \mathbf { H } ( A _ { k } ) =$ $[ h _ { k } ^ { 1 } , h _ { k } ^ { 2 } , . . . , h _ { k } ^ { \tilde { m } } ] ^ { T }$ k . Here $h _ { k } ^ { i } = \mathbf { H } ( a _ { k } ^ { i } )$ . A profile key is created with $H _ { k } , K _ { k } = \mathbf { H } ( H _ { k } )$ . Figure 2 shows the profile vector and key generation of an example profile. With the key of the required profile, the initiator encrypts the secret message using a symmetric encryption technique like Advanced Encryption Standard (AES). Any person who receives it tries to decrypt the secret message with his/her own profile key. Only the exactly matching person will decrypt the message correctly.

# C. Remainder Vector and Hint Matrix

So far, with the profile key, we have realized a naive private profile matching and secure channel establishment. However, the naive mechanism has some flaws making it unpractical.

1) The search is not flexible. The initiator cannot query any subset of other’s profile. For example, he/she need to find a ”student” studying ”computer science” regardless of the ”college”.   
2) A perfect matching is required and no fuzzy search is supported. In most cases, the initiator need only find some person with profile exceeding the required similarity threshold to the requested profile.   
3) All participants must decrypt the message, although most of them hold wrong keys. It wastes the computation resource and increases the search delay.

Improving the naive basic mechanism, our new mechanism allows the initiator to search a user in a flexible way $A _ { t } ~ = ~ ( N _ { t } , O _ { t } )$ , as described in Section II-A. We use a Remainder Vector for fast excluding most unmatched users. And a hint matrix is designed to work with the remainder vector to achieve efficient free-form fuzzy search.

1) Remainder Vector: Assume that there are $m _ { t }$ attributes in the request profile, $p$ is a prime larger than $m _ { t } . \mathrm { A }$ remainder vector $R _ { k }$ consists of the remainders of all hashed attributes in the input $H _ { k }$ divided by $p ,$ as illustrated in Fig. 2.

$$
R _ {k} = [ h _ {k} ^ {1} \mod p, h _ {k} ^ {2} \mod p,..., h _ {k} ^ {m} \mod p ] ^ {T}. \tag {2}
$$

Then the following theorem is straightforward.

![](images/97bdf0933842b65afc5bdd5c83ceed4d3dd29b01a2f983f86f0dee599348440e.jpg)



Fig. 2. The procedure to generate the profile key and remainder vector with a sample user profile.

Theorem 1: Consider two attributes’ hashes $h ^ { i } = \mathbf { H } ( a ^ { i } )$ and $h ^ { j } = \mathbf { H } ( a ^ { j } )$ , remainder $r ^ { i } \equiv h ^ { i }$ mod $p$ and remainder $r ^ { j } \equiv h ^ { j }$ mod $p . \mathrm { ~ H ~ } r ^ { i } \neq r ^ { j }$ , then $h ^ { i } \neq h ^ { j }$ .

Assume that the remainder vector of the required profile $A _ { t }$ $R _ { t } = [ r _ { t } ^ { 1 } , r _ { t } ^ { 2 } , . . . , r _ { t } ^ { m _ { t } } ] ^ { T }$ , and a relay user’s ofile vector $H _ { k }$ $R _ { t } ,$ $m _ { t }$ attribute subsets $H _ { k } ( r _ { t } ^ { i } )$ fitting each $r _ { t } ^ { i } .$ . Here $\forall h _ { k } ^ { x } \in H _ { k } ( r _ { t } ^ { i } )$ : $h _ { k } ^ { x }$ mod $p \ = \ r _ { t } ^ { i } .$ , i.e., attributes in $H _ { k } ( r _ { t } ^ { i } )$ yields the same remainder $r _ { t } ^ { i }$ when divided by $p .$

A combination of one element from each candidate attribute subset forms a profile vector of the relay user. If the candidate attribute subset $H _ { k } ( r _ { t } ^ { i } )$ is ∅, the corresponding element in the combination is unknown and the relay user fails to meet the required attribute $a _ { t } ^ { i }$ according to Theorem 1. The relay user is a candidate matching user of the request if there exist at least one combination, denoted by $H _ { c }$ , that satisfies the following:

1) The α necessary attributes are all known, i.e.

$$
H _ {k} (r _ {t} ^ {i}) \neq \emptyset , \forall i \leq \alpha ; \tag {3}
$$

2) The number of unknown elements don’t exceed γ, i.e.

$$
\left| \left\{H _ {k} (r _ {t} ^ {i}) \mid \alpha <   i \leq m _ {t}, H _ {k} (r _ {t} ^ {i}) = \emptyset \right\} \right| \leq \gamma ; \tag {4}
$$

3) Since $H _ { t }$ and $H _ { k }$ are both sorted, the elements of $H _ { c }$ should still keep the order consistent with $H _ { k }$ , i.e.

$$
\forall h _ {k} ^ {x} \in H _ {c}, h _ {k} ^ {y} \in H _ {c}. \tag {5}
$$

$$
h _ {k} ^ {x} \in H _ {k} (r _ {t} ^ {i}), h _ {k} ^ {y} \in H _ {k} (r _ {t} ^ {j}), i <   j \Rightarrow x <   y.
$$

We call $H _ { c \textbf { a } }$ candidate profile vector. Without satisfying the three conditions, a profile is not possible to match the request and will be excluded immediately.

In a fuzzy search, during the fast checking procedure, if there is no candidate profile vector that can be constructed by the relay user’s profile vector, then he/she is unmatched and he/she can forward the package. An ordinary relay user commonly has only dozens of attributes, so there won’t be many candidate profile vectors. Using the remainder vector, quick exclusions of a portion of unmatched users can be made.

2) Hint Matrix: A hint matrix is constructed to support a flexible fuzzy search. It describes the linear constrain relationship among the $\beta + \gamma$ optional attributes. With its help a matching user exceeding the similarity threshold can recover γ unknown attributes, so as to generate the correct profile key. Note that when a perfect matching user is required, no hint matrix is needed.

The constrain matrix with γ rows and $\gamma + \beta$ columns is:

$$
C _ {\gamma \times (\gamma + \beta)} = [ I _ {\gamma \times \gamma}, R _ {\gamma \times \beta} ]. \tag {6}
$$

Here matrix I is $\mathbf { a } \gamma$ dimensional identity matrix, R is a matrix of size $\gamma \times \beta ,$ , each of its elements is a random nonzero integer.

Multiplying the constrain matrix to the optional attributes of the required profile vector, the initiator gets a matrix B:

$$
B = C \times [ h _ {t} ^ {\alpha + 1}, h _ {t} ^ {\alpha + 2},..., h _ {t} ^ {m _ {t}} ] ^ {T} \tag {7}
$$

Then the hint matrix M is defined as matrix C, followed by matrix B, i.e.,

$$
M = [ C, B ]. \tag {8}
$$

When $\gamma > 0 ,$ the initiator generates the hint matrix and sends it with the encrypt message and the remainder vector.

In a fuzzy search, after the fast check, if the relay user is a candidate matching user, he/she constructs a set of candidate profile vector $H _ { c }$ with unknowns. By definition of the candidate profile vector, each $H _ { c }$ has no more than $\gamma$ unknowns, and any unknown $h _ { c } ^ { i } .$ , which is the i-th element of $H _ { c } .$ has $i > \alpha . \ \mathrm { N o w } ,$ , the unknowns of a candidate profile vector can be calculated by solving a system of linear equations:

$$
C \times [ h _ {c} ^ {\alpha + 1}, h _ {c} ^ {\alpha + 2},..., h _ {c} ^ {m _ {t}} ] ^ {T} = B \tag {9}
$$

Equivalently, we have $[ I , R ] \times [ h _ { c } ^ { \alpha + 1 } , h _ { c } ^ { \alpha + 2 } , . . . , h _ { c } ^ { m _ { t } } ] ^ { T } = B$ This system of equations has equal to or less than γ unknowns. It has a unique solution. With the solution, a complete candidate profile vector $H _ { c } ^ { \prime }$ is recovered. For each $H _ { c } ^ { \prime } ,$ a candidate key $K _ { c } \ = \ \mathbf { H } ( H _ { c } ^ { \prime } )$ can be generated. If any of the relay user’s candidate keys decrypts the message correctly, he/she is a matching user and gets the encrypted secret. Else, he/she forwards the request to the next user.

# D. Location Attribute and Its Privacy Protection

In localization enabled MSN, a user usually searches matching users in vicinity. Most systems require a user to reveal his/her own current location, which violates the user’s privacy. There are some work dedicated to privacy-preserving proximity discovering, $e . g .$ , Sharp [5], [13], [26]. In our mechanism, we consider location as a dynamic attribute which will be updated while the user moves, and design a location privacy preserving vicinity search method compatible with our private profile matching mechanism using fuzzy search scheme with the help of hint matrix. The dynamic attribute also improves the privacy protection for static attributes.

1) Lattice based Location Hashing: We map the twodimensional location to the hexagonal lattice. The lattice point set is a discrete set of the centers of all regular hexagons. The lattice is formally defined as $\{ x = u _ { 1 } a _ { 1 } + u _ { 2 } a _ { 2 } \mid ( u _ { 1 } , u _ { 2 } ) \in$ $\mathbb { Z } ^ { 2 } \}$ . Here $a _ { 1 } , a _ { 2 }$ are linearly independent primitive vectors which span the lattice. Given the primitive vectors $a _ { 1 } , a _ { 2 }$ , a point of the lattice is uniquely identified by the integer vector $u \ = \ ( u _ { 1 } , u _ { 2 } )$ . Let d denote the shortest distance between lattice points, for simplicity, we choose the primitive vectors $\begin{array} { r } { a _ { 1 } = ( d , 0 ) ; a _ { 2 } = ( \frac { 1 } { 2 } d , \frac { \sqrt { 3 } } { 2 } d ) } \end{array}$ .

Defining a geography location as the origin point O and the scale of the lattice cell d, with the lattice definition, a location can be hashed to its nearest lattice point. Given a user $v _ { k } \mathrm { ^ { \prime } s }$ current location $l _ { k } ( t )$ at time t and his/her vicinity range D, his/her vicinity region can be hashed to a lattice point set, $V _ { k } ( O , d , l _ { k } ( t ) , D )$ , consisting of central lattice point, i.e. the hash of $l _ { k } ( t )$ , and other lattices points whose distances to the center lattice point are less than D.

2) Location Privacy Preserved Vicinity Search: Intuitively, given the distance bound to define vicinity, if two users are within each other’s vicinity, the intersection of their vicinity regions will have a proportion no less than a threshold Θ. If the vicinity region is a circle, $\Theta = 0 . 3 9$ . The initiator calculates his/her vicinity lattice point set $V _ { i } ( O , d , l _ { i } ( t ) , D )$ . If a user $v _ { k }$ is in his/her vicinity, then $v _ { k } \mathrm { ^ { \prime } s }$ vicinity lattice point set $V _ { k } ( O , d , l _ { k } ( t ) , D )$ should satisfy the requirement:

$$
\theta_ {k} = \frac {\left| V _ {i} (O , d , l _ {i} (t) , D) \bigcap V _ {k} (O , d , l _ {k} (t) , D) \right|}{\left| V _ {k} (O , d , l _ {k} (t) , D) \right|} \geq \Theta \tag {10}
$$

To conduct location privacy preserved vicinity search, the initiator won’t send his/her vicinity lattice point set directly. Using the sorted lattice points, he/she generates a dynamic profile key, a dynamic remainder vector and a dynamic hint matrix in the same way as processing other attributes. So a vicinity search works as a fuzzy search with similarity threshold Θ. Only participants in his/her vicinity who has a certain amount of common lattice points with him/her can generate the correct dynamic profile key with the help of the dynamic remainder vector and hint matrix.

3) Location Based Profile Matching: Compared to static attributes like identity information, location is usually a temporal privacy. When constructing profile vector of a user, we can hash the concatenation of each static attribute and his/her current dynamic key instead of directly hash static attributes. So the hash values of the same static attribute are completely changed when user update his/her location. It will greatly increase the difficulty for the malicious adversary to conduct dictionary profiling.

# E. Privacy-Preserving Profile Matching Protocols

We are now ready to present our privacy preserving profile matching protocols. Here we present three different protocols that achieve different levels of privacy protection.

1) Protocol 1: Under Protocol 1, a unmatched user doesn’t know anything about the request. The matching user knows the intersection of the required profile and his/her own profile

# Protocol 1: Privacy Preserving Profile Matching

1) The initiator encrypts a random number x and a public predefined confirmation information in the secret message $E _ { K _ { t } }$ t(conf irmation, x) by the required profile key $K _ { t }$ . And he/she sends the request out.   
2) A candidate relay user can verify whether he/she decrypts the message correctly by the confirmation information. If he/she does not match, he/she just forwards the request to the next user. If he/she is matching, he/she can reply the request by encrypting the predefined ack information and a random number $y$ along with any other message (e.g. the intersection cardinality) by x, say $E _ { x } ( a c k , y )$ , and sends it back to the initiator.

# Protocol 2: Privacy Preserving Profile Matching

1) The initiator encrypts a random number x in the secret message $E _ { K _ { t } } ( x )$ by the request profile key $K _ { t }$ .   
2) A candidate matching user cannot verify whether he/she decrypts the message correctly. Let the candidate profile key set be $\{ K _ { c } ^ { 1 } , K _ { c } ^ { 2 } , \ldots , K _ { c } ^ { z } \}$ . He/she decrypts the message in the request with each candidate profile key to get a set of numbers, say $U = \{ u _ { j } \ | \ u _ { j } = D _ { K _ { c } ^ { j } } ( E _ { K _ { t } } ( x ) ) \}$ . Then he/she encrypts the predefined ack information and a random number $y$ by each $u _ { j }$ as the key, and sends the acknowledge set $\{ E _ { u _ { j } } ( a c k , \bar { y } ) \}$ to the initiator, for a public ack.   
3) The initiator excludes the potential malicious repliers whose response time exceeds the time window or the cardinality of reply set exceed the threshold. He/she decrypts the replies with x. If he/she gets a correct ack information from a reply, the corresponding replier is a matching user.

after Step 1 in the HBC model, and he/she can decide whether to reply. The initiator doesn’t know anything about any participant until he/she gets a reply. With replies, he/she knows the matching users and even the most similar replier by the cardinality information. Then he/she can start secure communication with a matching user encrypted by $x + y$ or with a group of matching users encrypted by x. However, in malicious model, if the matching user has a dictionary, he/she can learn the whole request profile by the recovered profile vector.

2) Protocol 2: To prevent malicious participants, we design Protocol 2, which is similar to Protocol 1, but it excludes the confirmation information from the encrypted message.

Under Protocol 2, after the first round of communication, the participants won’t know anything about the request in both HBC model and malicious model. The initiator knows who are the matching users and even the most similar one according to the replies. Then the initiator can start secure communication with a matching user protected by the key $x { + y }$

or with a group of matching users protected by x. In malicious model, if a participant has a dictionary of the attributes, he/she may construct a large candidate profile key set and send it to the initiator. However, an ordinary user with about dozens of attributes can make a quick reaction and reply a small size acknowledge set. While it takes much longer for a malicious user due to a large number of candidate attribute combinations. So the initiator can identify the malicious repliers by response time and the cardinality of reply set.

Consider an unlikely case that, an adversary constructs the attribute dictionary from other similar social networking system and the the attribute space is not large enough. In this case, in Protocol 1, the request profile may be exposed via dictionary profiling by malicious participants. Although Protocol 2 protects the request profile from any participants, a malicious initiator may learn the profile of unmatching repliers.

3) Protocol 3: To prevent the dictionary profiling by malicious initiator, we improve Protocol 2 to Protocol 3 which provides a user personal defined privacy protection.

Definition 4 (Attribute Entropy): For an attribute $a ^ { i }$ with $t ^ { i }$ values $\{ x _ { j } : j = 1 , \ldots , t ^ { i } \} . \ P ( a ^ { i } = x _ { j } )$ is the probability that the attribute $a ^ { i }$ of a user equals $x _ { j }$ . The entropy of the attribute $a ^ { i }$ is $\begin{array} { r } { S ( { a } ^ { i } ) = - \sum _ { i = 1 } ^ { t ^ { i } } P ( { a } ^ { i } = x _ { j } ) \log P ( { a } ^ { i } = x _ { j } ) } \end{array}$ ti .

Definition 5 (Profile Entropy): The entropy of a profile $A _ { k }$ is $\begin{array} { r } { S ( A _ { k } ) = \sum _ { i = 1 } ^ { m _ { k } } S ( a ^ { i } ) } \end{array}$ .

A participant can determine his/her personal privacy protection level by giving an acceptable profile entropy leakage upper limit $\varphi .$ Based on the user defined protection level, Protocol 3 is ϕ-entropy private for each user.

Definition 6 (ϕ-Entropy Private): A protocol is ϕ-entropy private when the entropy of possible privacy leakage is not greater than the upper limit $\varphi \colon S ( L e a k ( A _ { k } ) ) \leq \varphi .$

A user can use k-anonymity (thus $\varphi = \log { \frac { n } { k } } )$ or use the most sensitive attribute (thus $\varphi = \operatorname* { m i n } ( S ( a ^ { i } ) ) )$ to decide $\varphi .$ .

Protocol 3 is privacy-preserving when the initiator is not malicious. and it is ϕ-private for each participant even when the initiator can conduct a dictionary profiling.

# F. Establishing Secure Communication Channel

As presented in the profile matching protocols, the random number x generated by the initiator and y generated by a matching user have been exchanged secretly between them, which is resistant to the Man-in-the-Middle attack. Numbers x and y are the communication keys shared by a pair of matching users. Furthermore, our mechanism also discovers the community consisting of users with similar profile as the initiator and establish the group key x for secure intracommunity communication.

# IV. SECURITY AND EFFICIENCY ANALYSIS

# A. Security and Privacy Analysis

1) Profile Privacy: During the generation of the profile key, we use the hash value (with SHA-256) of the combination of the static attribute and the dynamic attribute (i.e. location), which greatly increases the protection of the static attribute.

# Protocol 3: User-defined Privacy Preserving Profile Matching

1) The initiator encrypts a random number x in the secret message without any confirmation information by the required profile key, say $E _ { K _ { t } } ( x )$ .   
2) A candidate matching user cannot verify whether he/she decrypts the message correctly. He/she selects a set of candidate profile $\{ \bar { A } _ { c } ^ { 1 } , A _ { c } ^ { 2 } , \ldots \bar { , } A _ { c } ^ { z } \}$ which satisfies that $S ( \bigcup _ { i = 1 } ^ { z } A _ { c } ^ { i } ) \leq \varphi .$ And he/she generates the corresponding candidate profile keys $\{ K _ { c } ^ { 1 } , K _ { c } ^ { 2 } , \ldots , K _ { c } ^ { z } \}$ . He/she decrypts the message in the request with each candidate profile key to get a set of numbers, say $U = \{ u _ { j } \mid u _ { j } =$ $D _ { K _ { c } ^ { j } } ( E _ { K _ { t } } ( x ) ) \}$ }. Then he/she encrypts the predefined ack information and a random number y by each $u _ { j } ,$ , and sends back the acknowledge set $\{ E _ { u _ { j } } ( a c k , y ) \}$ back to the initiator.   
3) The initiator excludes the malicious replier whose response time exceeds the time window or the cardinality of reply set exceed the threshold and decrypts the replies with x. If he/she gets a correct ack information from a reply, the corresponding replier is matching.

We use 256-bit-key AES as the encryption method. The 256- bit profile key is used as the secret key to encrypt the message by AES. Only the encrypted message will be transmitted, and no attribute information will be transmitted in any data packets. Therefore no user can obtain other user’s attribute hash to build a dictionary. To acquire the profile information of the initiator or other participants the attacker needs to decrypt the request/reply message correctly and confirm the correctness. This is extremely difficult due to the choice of SHA-256, 256-bit-key AES and the random salt x.

In the HBC model only users owning matching attributes can decrypt each other’s messages correctly. Unmatched user cannot obtain any information from the encrypted message. Table I(a) presents the protection level of our protocols in this model. Compared to the existing PSI and PCSI approaches, our protocols provide Level 2 privacy protection for matching users and don’t leak any information to unmatched users.

In the malicious model, it is impossible for the adversary to build an attribute dictionary in our system. If an adversary constructs the dictionary from other sources, e.g., other similar social networking systems, in most cases, the cardinality m of the dictionary is very large, which makes the dictionary profiling difficult. With a remainder vector, it takes an adversary $\left( { \frac { m } { p } } \right) ^ { m _ { t } }$ guesses to compromise a user’s profile with $m _ { t }$ attributes. Here $p$ is a small prime number like 11. In Tencent Weibo, we found that $m \ : \simeq \ : 2 ^ { 2 0 }$ and the average attribute number of each user is 6. When the adversary tries to guess a user’s profile by brute force, it will take about $2 ^ { 1 0 0 }$ guesses. If considering keywords of a user, m is even larger. Especially in localizable MSN, the vast dynamic location attribute will greatly increase the attribute set and make the dictionary profiling more infeasible.

# TABLE I

THE PRIVACY PROTECTION LEVEL OF OUR PROTOCOLS. v IS THE INITIATOR, vm IS A MATCHING USER AND vu IS A UNMATCHING USER. $A _ { i } ,$ , $A _ { m } \ \mathrm { A N D } \ A _ { u }$ ARE THEIR CORRESPONDING PROFILES. $\boldsymbol { v } _ { i } ^ { \prime }$ IS A MALICIOUS INITIATOR WITH A PROFILE DICTIONARY. $\boldsymbol { v } _ { p } ^ { \prime }$ IS A MALICIOUS PARTICIPANT WITH A PROFILE DICTIONARY EAVESDROPPING THE COMMUNICATION. NC STANDS FOR NON-CANDIDATE, AND CD STANDS FOR CANDIDATE.

(a) In HBC model. 

<table><tr><td>PPL</td><td> $(A_{I}, v_{M})$ </td><td> $(A_{I}, v_{U})$ </td><td> $(A_{M}, v_{I})$ </td><td> $(A_{U}, v_{I})$ </td></tr><tr><td>Protocol 1</td><td>1</td><td>3</td><td>2</td><td>3</td></tr><tr><td>Protocol 2</td><td>3</td><td>3</td><td>2</td><td>3</td></tr><tr><td>Protocol 3</td><td>3</td><td>3</td><td>2</td><td>3</td></tr><tr><td>PSI</td><td>3</td><td>3</td><td>1</td><td>1</td></tr><tr><td>PCSI</td><td>3</td><td>3</td><td> $|A_{I} \cap v_{U}|$ </td><td> $|A_{I} \cap v_{U}|$ </td></tr></table>

(b) In Malicious model.

<table><tr><td>PPL</td><td>Protocol 1</td><td>Protocol 2</td><td>Protocol 3</td></tr><tr><td> $(A_I, v_P')$ </td><td>0</td><td>3</td><td>3</td></tr><tr><td> $(A_M, v_I')$ </td><td>2</td><td>2</td><td> $\varphi$ -entropy</td></tr><tr><td> $(A_M, v_P')$ </td><td>2</td><td>3</td><td>3</td></tr><tr><td> $(A_U, v_I')$ </td><td>3</td><td>3 for NC $A_c$ for CD</td><td>3 for NC $\varphi$ -entropy for CD</td></tr><tr><td> $(A_U, v_P')$ </td><td>3</td><td>3</td><td>3</td></tr></table>

There is an unlikely case that the dictionary size is not large enough. This kind of adversary also compromises other PSI based approaches. Table I(b) shows the protection level of our protocols in this case. Protocol 1 cannot protect the initiator’s privacy from the dictionary profiling. But it provides Level 2 privacy for replying matching users and unconditional Level 3 privacy for other users. Protocol 2 provides unconditional Level 3 privacy for the initiator. It also provides unconditional Level 3 privacy for all participants against any other persons except the initiator. Only if the initiator is an adversary with the dictionary, he/she may compromise the candidate user’s privacy. Protocol 3 still provides unconditional Level 3 privacy for the initiator and incardinate users, and Level 3 privacy for the candidate users against any other person except the initiator. Moreover, it provides personal defined ϕ-entropy privacy for all candidate users against a malicious initiator.

2) Verifiability: In majority of existing profile matching approaches, only one party learns the true result. There lacks an efficient way for the other party to verify the result. Our protocols are verifiable and resists cheating. In our protocols, matching users are required to reply $E _ { x } ( a c k , y )$ . In the HBC model, only the matching user can get the correct x. An unmatched user cannot cheat the initiator to pretend to be matched. Consequently, the initiator can only obtain the correct y of the matching user. So both the initiator and participants cannot cheat each other. In the malicious model, it takes an adversary with a dictionary much longer time to guess the correct key. Hence a nonmalicious user can distinguish the adversary by his/her reply delay.

# B. Performance Analysis

1) Computational Cost: For an initiator, it takes $O ( m _ { t } \log m _ { t } )$ operations for sorting attributes, $m _ { t } ~ + ~ 1$ hashing operations for profile key generation and mt modulo operations for remainder vector generation. $\gamma ( \gamma + \beta )$

operations are needed to calculate the hint matrix if the required similarity $\theta < 1 0 0 \%$ . One symmetric encryption is needed with the profile key.

For a participant $v _ { k } ,$ , it takes $O ( m _ { k } \log m _ { k } )$ operations for sorting its attributes, $m _ { k }$ hashing for profile vector generation and $m _ { k }$ modulo operations for remainder calculation. After fast checking by remainder vector, if a participant $v _ { k }$ is not a candidate user, no more computation is need. $\mathrm { ~ I f ~ } \boldsymbol { v } _ { k }$ is a candidate user, let the number of his candidate profile vector be $\kappa _ { k } .$ . It takes this user $\kappa _ { k }$ hashing to generate candidate profile keys. If there is a hint matrix, user $v _ { k }$ needs to solve $\kappa _ { k }$ $\gamma ( \gamma + \beta )$ -dimension linear equation systems. The computation cost is $O ( \kappa _ { k } m _ { t } ^ { 3 } )$ . In the end, $\kappa _ { k }$ symmetric decryptions with the profile key. Note that the expected $\kappa _ { k }$ is $\varepsilon ( \kappa _ { k } ) = { \binom { m _ { k } } { \alpha + \beta } } \times$ $\begin{array} { r } { \left( \frac { 1 } { p } \right) ^ { \alpha + \beta } } \end{array}$ . For example, in Tencent Weibo the average attribute number is 6 and the maximum number is 20. Then if $\alpha +$ $\beta = 6 ,$ , even a large $m _ { k } = 2 0$ and small prime number $p =$ 11 result in a very small $\varepsilon ( \kappa _ { k } ) ~ = ~ 0 . 0 2$ . So it takes small computation cost even for a candidate user. We can show that the expected candidate users is only a small portion of all users and the portion decreases greatly with the increase of $m _ { t }$ and $p .$ It may be considered that larger $p$ will weaken the security due to the decreased difficulty of dictionary profiling. Our testing and analysis show that even a small $p , e . g . , p = 1 1$ , can significantly reduce the number of candidate users. So an initiator can choose a proper p to efficiently control the amount of candidate users as well as achieve the secure protection of profile privacy.

2) Communication Cost: To conduct profile matching with all users, the initiator only need one broadcast to send the request to all participants. The size of the request message is at most $( 1 - \theta ) \bar { 3 } 2 m _ { t } ^ { 2 } \bar { + } ( 2 8 8 - 2 5 6 \theta ) m _ { t } + 2 5 6$ bits. For example, the user of Tencent Weibo has 6 tags in average and 20 tags at most. To search a 60% similar user, the request is about 190B in average and 1KB at most. In Protocol 1, only the matching user will reply the request. So the transmission cost of Protocol 1 is one broadcast and $O ( 1 )$ unicasts. In Protocol $^ { 2 , }$ only the candidate matching user will reply the request. So the transmission cost of Protocol 2 is one broadcast and $O ( n * ( \frac { 1 } { p } ) ^ { m _ { t } \theta } )$ unicasts. For example, when $p = 1 1 , m _ { t } = 6 .$ , $\theta = 0 . 6 ,$ there are only about $\scriptstyle { \frac { 1 } { 5 6 1 0 } }$ fraction of users will reply. In Protocol 3, the communication cost of reply is even smaller than Protocol 2 because of the personal privacy setting. Note that a reply in all three protocols is only 32Byte.

Comparison between our protocols and PSI and PCSI based approaches (omitted due to space limit) shows that our protocols are efficient. A computation time comparison with dot product based on approach is suggested to refer to [7].

# V. EVALUATION USING REAL DATA AND SYSTEM

# A. Real Social Networking System Analysis

Our evaluations are based on the profile data of Tencent Weibo [2]. Tencent Weibo is one of the largest micro-blogging websites in China, which is a platform for building friendship and sharing interests online. This dataset has 2.32 million

TABLE IIMEAN COMPUTATION TIME FOR OUR BASIC OPERATION.(MS)

<table><tr><td></td><td>SHA-256</td><td>Mod  $p$ </td><td>AES Enc</td></tr><tr><td>Laptop</td><td> $1.2 \times 10^{-3}$ </td><td> $3.1 \times 10^{-4}$ </td><td> $8.7 \times 10^{-4}$ </td></tr><tr><td>Phone</td><td> $4.8 \times 10^{-2}$ </td><td> $5.7 \times 10^{-2}$ </td><td> $2.1 \times 10^{-2}$ </td></tr><tr><td></td><td>Multiply-256</td><td>Compare-256</td><td>AES Dec</td></tr><tr><td>Laptop</td><td> $1.4 \times 10^{-4}$ </td><td> $1.0 \times 10^{-5}$ </td><td> $9.6 \times 10^{-4}$ </td></tr><tr><td>Phone</td><td> $3.2 \times 10^{-2}$ </td><td> $1.0 \times 10^{-3}$ </td><td> $2.5 \times 10^{-2}$ </td></tr></table>

TABLE IIIMEAN COMPUTATION TIME FOR BASIC OPERATIONS FOR ASYMMETRICCRYPTOSYSTEM BASED SCHEME.(MS)

<table><tr><td></td><td>1024-exp</td><td>2048-exp</td><td>1024-mul</td><td>2048-mul</td></tr><tr><td>Laptop</td><td>17</td><td>120</td><td> $2.3 \times 10^{-2}$ </td><td> $1 \times 10^{-1}$ </td></tr><tr><td>Phone</td><td>34</td><td>197</td><td> $1.5 \times 10^{-1}$ </td><td> $2.4 \times 10^{-1}$ </td></tr></table>

users’ personal profiles, including the year of birth, the gender, the tags and keywords. Tags are selected by users to represent their interests. If a user likes mountain climbing and swimming, he/she may select ”mountain climbing” or ”swimming” to be his/her tag. Keywords are extracted from the tweet/retweet/comment of a user. There are total 560419 tags and 713747 keywords. As presented in Figure 3, each user has 6 tags in average and 20 tags at most. So when the adversary tries to guess a user’s profile with 6 tags by brute force, it will take him/her about $2 ^ { 1 0 0 }$ guesses.

When more than one user has the same profile, we say there are collisions for this profile. Figure 4 shows that more than 90% users have unique profiles.

![](images/bab2d2a111a395c7d7cb511309bd8f8ce0ec380babaf3f8ee03aec232dd4b04a.jpg)



Fig. 3. Users’ attribute number distribution.

![](images/b0974c7be2f19c0a6a1080e259578b3d1a40f2c75fdaa250a946d7b4282e7b69.jpg)



Fig. 4. Profile uniqueness and collisions of users.

# B. Computation and Communication Performance

We then exam the computation performance of our protocols on mobile devices and PC. The mobile phone is HTC G17 with 1228Hz CPU, 1GB RAM. The laptop is Think Pad X1 with i7 2.7GHz CPU and 4GB RAM. Table II shows the mean execution time of our basic computation and Table III shows the mean execution time for basic operations for asymmetric cryptosystem based scheme. The basic operations of our mechanism are much cheaper than the 1024-bit or 2048-bit modular multiplication and exponentiation used by the asymmetric cryptosystem based schemes. We evaluate our protocol on the Tencent Weibo dataset. Table IV presents the breakdown of time cost for our protocol. As an example, for a user with 6 attributes, the time need to generate a request is only about $3 . 9 \times 1 0 ^ { - 2 }$ ms on laptop and 1.3 ms on mobile phone. On average it takes a non-candidate user about $3 . 9 \times 1 0 ^ { - 2 }$ ms on laptop and 0.63 ms on phone to process the request. For a candidate user the computation cost is about $4 \times 1 0 ^ { - 2 }$ ms on laptop and 7 ms on phone for each candidate key. The time cost of all the operations in our protocols are quite small compared with the computation time of asymmetric cryptosystem based approaches, e.g. the evaluation result of [7]. Table V shows a typical scenario in a mobile social network with 100 users. The numbers of attributes are chosen based on the analysis of Tencent Weibo. With the comparison of numerical result based on implementation on the mobile phone, it is clearly that our protocol is efficient in both computation and communication.

TABLE IVDECOMPOSED COMPUTATION TIME OF OUR PROTOCOLS BASED ON THETENCENT WEIBO DATASET.(MS)

<table><tr><td colspan="4">Laptop</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>MatrixGen</td><td> $7.2 \times 10^{-3}$ </td><td> $1.0 \times 10^{-3}$ </td><td> $2.4 \times 10^{-2}$ </td></tr><tr><td>KeyGen</td><td> $8.1 \times 10^{-3}$ </td><td> $2.3 \times 10^{-3}$ </td><td> $2.5 \times 10^{-2}$ </td></tr><tr><td>RemainderGen</td><td> $1.9 \times 10^{-3}$ </td><td> $3.1 \times 10^{-4}$ </td><td> $6.2 \times 10^{-3}$ </td></tr><tr><td>HintGen</td><td> $4.7 \times 10^{-3}$ </td><td> $2.8 \times 10^{-4}$ </td><td> $5.6 \times 10^{-2}$ </td></tr><tr><td>HintSolve</td><td> $3 \times 10^{-2}$ </td><td> $1.1 \times 10^{-3}$ </td><td>1.1</td></tr><tr><td colspan="4">Phone</td></tr><tr><td></td><td>Mean</td><td>Min</td><td>Max</td></tr><tr><td>MatrixGen</td><td> $2.6 \times 10^{-1}$ </td><td> $4.4 \times 10^{-2}$ </td><td> $8.9 \times 10^{-1}$ </td></tr><tr><td>KeyGen</td><td> $6.3 \times 10^{-2}$ </td><td> $4.8 \times 10^{-2}$ </td><td> $1.4 \times 10^{-1}$ </td></tr><tr><td>RemainderGen</td><td> $3.4 \times 10^{-1}$ </td><td> $5.7 \times 10^{-2}$ </td><td>1.14</td></tr><tr><td>HintGen</td><td>1.2</td><td> $1.4 \times 10^{-1}$ </td><td>12</td></tr><tr><td>HintSolve</td><td>6.9</td><td> $2.6 \times 10^{-1}$ </td><td>250</td></tr></table>

# C. Protocol Performance Evaluations

Based on the user attributes of Tencent Weibo, we evaluate the efficiency of our protocols. Two typical situations are taken into consideration. In the first case, all users have equal size of attributes which is similar to the vector based scheme. We use the attribute data of all 52248 users with 6 attributes. In the second case, we randomly sample 1000 users from all users to conduct profile matching.

In both cases, we exam the similarity between all pairs of users as the ground truth. Then we run our profile matching protocols at different similarity levels. Figure 5 shows the number of candidate users of our protocol change with similarity requirement and the prime number p. The result shows that in both cases, the number of candidate users approaches the number of true matching users with increasing p. And a small p can achieve small size of candidate users and significantly reduce unwanted computation and communication cost for unmatching users.

There is a worry that, the candidate profile key set may be very large for candidate users. Figure 6 presents the number of candidate profile keys during the matching with different similarity level and prime p. The result shows that in real social networking system like Tencent Weibo, the candidate key set is small enough to achieve efficient computation for candidate users.

# VI. RELATED WORK

Most previous private matching work are based on the secure multi-party computation (SMC) [10]. There are two mainstreams of approaches to solve the private profile-based friending problem. The first category is based on private set intersection (PSI) and private cardinality of set intersection (PCSI) [12], [20]. Early work in this category mainly address the private set operation problem in database research, e.g. [3], [8], [11]. [12], [20] provide well-designed protocols to privately match users’ profiles based on PSI and PCSI. The second category is based on private vector dot product [9]. [7], [24] considers a user’s profile as vector and use it to measure social proximity. A trusted central server is requited to precompute users social coordinates and generate certifications and keys. [25] improves these work with a fine-grained private matching. However, in the PSI based schemes, any user can learn the profile intersection with any other user. The PCSI and dot product based approaches cannot support a precise specific profile matchings. These protocols often rely on public-key cryptosystem and/or homomorphic encryption which results in expensive computation cost and usually requires a trusted third party. Even unmatched users involve in the expensive computation. Furthermore, these protocols are unverifiable.

![](images/9a05f362f8c80efed0c31e661ae0c453067f5ecaed57e1cd67748ab82aa5f369.jpg)



(a) users with 6 attributes

![](images/24a7b7ddcd024361b2033a53498508742c1fa5f3dc4660c1f157440b05853559.jpg)



(b) diverse numb. of attributes

Fig. 5. Candidate user proportion with different similarity and prime number.   
![](images/59a9ee33e25be40c415c99669bdba253e09b187d072585e52880afbb01c1fe6d.jpg)



(a) users with 6 attributes

![](images/5bc84425f5e52d574d4fb511a3fac8c9673fcc4218401fff36ba656c07e8c59b.jpg)



(b) diverse num. of attributes   
Fig. 6. Size of candidate profile key set with different similarities.

Secure communication channel construction is very important in practical private friending system but is often ignored. Secure communication channels are usually set up by authenticated key agreement protocols. This can be performed by relying on a public-key infrastructure, e.g., based on RSA or the Diffie-Hellman protocol.The public-key based methods allow parties to share authenticated information about each other, however they need a trusted third party. Although Diffie-Hellman key exchange method allows two parties to jointly establish a shared secret key, it is known to be vulnerable to the Man-in-the-Middle attack. Device pairing is a another technique to generate a common secret between two devices that shared no prior secrets with minimum or without additional hardware, e.g. [4], [14], [16]. However, they employ some out-of-band secure channels to exchange authenticated information or leverage the ability of users to authenticate each other by visual and verbal contact. The interaction cost is not well suited to MSN where secure connections are needed immediately between any users. With these existing schemes, it is more complicated to establish a group key.

TABLE V   
COMPARISON OF EFFICIENCY WITH EXISTING SCHEME IN TYPICAL SCENARIO. $m _ { t } = m _ { k } = 6 , \gamma = \beta = 3 , p = 1 1 , n = 1 0 0 , t = 4 . M _ { 2 }$ AND $M _ { 2 }$ ARE FOR 1024-BIT AND 2048-BIT MODULAR MULTIPLICATION. E2 AND E2 ARE FOR 1024-BIT AND 2048-BIT EXPONENTIATION. 

<table><tr><td></td><td>Party</td><td>FNP [8]</td><td>FC10 [6]</td><td>Advanced [12]</td><td>Protocol 1</td></tr><tr><td rowspan="2">Computation</td><td> $P_1$ </td><td> $612E_3$ </td><td> $1500M_2$ </td><td> $1800E_3$ </td><td> $7SHA + 6Mod + Enc (P_1)$ </td></tr><tr><td> $P_k$ </td><td> $5E_3$ </td><td> $12E_2$ </td><td> $12E_3$ </td><td> $6SHA + 6Mod (NC)$  $54\kappa_k + (6 + \kappa_k)SHA + 6Mod + \kappa_kDec (CD)$ </td></tr><tr><td>Computation(ms)</td><td> $P_1$ </td><td>120564</td><td>225</td><td>354600</td><td> $0.7 (P_1)$ </td></tr><tr><td>On phone</td><td> $P_k$ </td><td>985</td><td>408</td><td>2364</td><td> $0.63 (NC)$  $1.8\kappa_k + 0.63 (CD)$ </td></tr><tr><td>Communication(KB)</td><td>All</td><td>151</td><td>300</td><td>704</td><td>0.22</td></tr><tr><td>CommunicationTransmission</td><td>All</td><td>1 broadcast100 unicasts</td><td>200 unicasts</td><td>500 unicasts</td><td>1 broadcast&lt; 100 (#candidates unicasts)</td></tr></table>

Attribute based encryption is designed for access control of shared encrypted data stored in a server [17]. Only the user possessing a certain set of credentials or attributes is able to access data. All the ABE schemes rely on asymmetric-key cryptosystem, which cost expensive computation. And they require a complicate setup and a server.

# VII. CONCLUSIONS

In this paper, we design a novel symmetric-encryption based privacy-preserving profile matching and secure communication channel establishment mechanism in decentralized MSN without any presetting or trusted third party. Several protocols were proposed for achieving verifiability and different levels of privacy. We rigorously analyzed the performance of our protocols and compared them with existing protocols. We conducted extensive evaluations on the performances using a large scale dataset from real social networking. The results show that our mechanisms outperform existing solutions significantly. We are integrating the techniques into an ongoing social networking project.

# ACKNOWLEDGMENT

The research is supported in part by NSFC Major Program 61190110, China 863 Program under grant No. 2011AA010100, ,China 973 Program under grant No.2011CB302705, the NSFC program under Grant No.61272426 and China Postdoctoral Science Foundation funded project under grant No. 2012M510029. The research of Xiang-Yang Li is partially supported by NSF CNS-0832120, NSF CNS-1035894, NSF ECCS-1247944, NSFC Program under Grant No. 61170216, No. 61228202, China 973 Program under Grant No.2011CB302705.

# REFERENCES

[1] “Magnetu,” http://magnetu.com.   
[2] “Tencent weibo,” http://t.qq.com/.   
[3] R. Agrawal, A. Evfimievski, and R. Srikant, “Information sharing across private databases,” in Proceedings of ACM SIGMOD, 2003, pp. 86–97.   
[4] D. Balfanz, D. K. Smetters, P. Stewart, and H. C. Wong, “Talking to strangers: Authentication in ad-hoc wireless networks,” in Proceedings of NDSS, 2002.   
[5] W. Chang, J. Wu, and C. C. Tan, “Friendship–based location privacy in mobile social networks,” International Journal of Security and Networks, vol. 6, no. 4, pp. 226–236, 2011.

[6] E. De Cristofaro and G. Tsudik, “Practical private set intersection protocols with linear complexity,” in Financial Cryptography and Data Security, 2010, pp. 143–159.   
[7] W. Dong, V. Dave, L. Qiu, and Y. Zhang, “Secure friend discovery in mobile social networks,” in Proceedings of IEEE INFOCOM, 2011.   
[8] M. J. Freedman, K. Nissim, and B. Pinkas, “Efficient private matching and set intersection,” in EUROCRYPT, 2004, pp. 1–19.   
[9] I. Ioannidis, A. Grama, and M. Atallah, “A secure protocol for computing dot-products in clustered and distributed environments,” in Proceedings of IEEE ICPP, 2002.   
[10] T. Jung, X. Mao, X.-Y. Li, S. Tang, W. Gong, and L. Zhang, “Privacypreserving data aggregation without secure channel: multivariate polynomial evaluation,” in Proceedings of IEEE INFOCOM, 2013.   
[11] L. Kissner and D. Song, “Privacy-preserving set operations,” in Advances in Cryptology–CRYPTO, 2005, pp. 241–257.   
[12] M. Li, N. Cao, S. Yu, and W. Lou, “Findu: Privacy-preserving personal profile matching in mobile social networks,” in Proceedings of IEEE INFOCOM, 2011.   
[13] X.-Y. Li and T. Jung, “Search me if you can: privacy-preserving location query service,” in Proceedings of IEEE INFOCOM, 2013.   
[14] J. M. McCune, A. Perrig, and M. K. Reiter, “Seeing-is-believing: Using camera phones for human-verifiable authentication,” in Proceedings of IEEE S&P, 2005.   
[15] K. Okamoto, W. Chen, and X.-Y. Li, “Ranking of closeness centrality for large-scale social networks,” in FAW, 2008.   
[16] S. Pasini and S. Vaudenay, “Sas-based authenticated key agreement,” in PKC, 2006.   
[17] A. Sahai and B. Waters, “Fuzzy identity-based encryption,” in EURO-CRYPT, 2005, pp. 457–473.   
[18] R. Sproat, A. W. Black, S. Chen, S. Kumar, M. Ostendorf, and C. Richards, “Normalization of non-standard words,” Computer Speech & Language, vol. 15, no. 3, pp. 287–333, 2001.   
[19] S.-J. Tang, J. Yuan, X. Mao, X.-Y. Li, W. Chen, and G. Dai, “Relationship classification in large scale online social networks and its impact on information,” in Proceedings of IEEE INFOCOM, 2011.   
[20] M. Von Arb, M. Bader, M. Kuhn, and R. Wattenhofer, “Veneta: Serverless friend-of-friend detection in mobile social networking,” in Proceedings of IEEE WIMOB, 2008.   
[21] Z. Yang, B. Zhang, J. Dai, A. C. Champion, D. Xuan, and D. Li, “E-smalltalker: A distributed mobile system for social networking in physical proximity,” in Proceedings of IEEE ICDCS, 2010.   
[22] L. Zhang, X.-Y. Li, J. Lei, J. Sun, Y. Liu, “Mechanism design for finding experts using locally constructed social referral web,” in TPDS, 2013.   
[23] L. Zhang, X. Ding, Z. Wan, M. Gu, and X. Li, “Wiface: A secure geosocial networking system using wifi-based multi-hop manet,” in ACM MobiSys MCS workshop, 2010.   
[24] L. Zhang, X.-Y. Li, Y. Liu, and T. Jung, “Verifiable private multi-party computation: Ranging and ranking,” in Proceedings of IEEE INFOCOM, 2013.   
[25] R. Zhang, Y. Zhang, J. Sun, and G. Yan, “Fine-grained private matching for proximity-based mobile social networking,” in Proceedings of IEEE INFOCOM, 2012.   
[26] Y. Zheng, M. Li, W. Lou, and Y. T. Hou, “Sharp: Private proximity test and secure handshake with cheat-proof location tags,” in ESORICS, 2012.