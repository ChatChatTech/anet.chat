# Ad-hoc Anonymity: Privacy Preservation for Location-based Services in Mobile Networks

Junliang Liu∗, Zheng Yang∗†, Yunhao Liu∗† ∗Hong Kong University of Science & Technology †TNList, School of Software, Tsinghua University Email: {  }

Abstract—Location-based Service (LBS) becomes increasingly important for wireless and mobile networks. In current LBS schemes, Service Providers (SPs) require users report their accurate locations, which can be illegally used by adversaries to infer sensitive information of users. Privacy disclosure raises serious concerns and limits the application of LBS. Previous solutions either rely on pre-installed centralized intermediary or assume cooperative users. Other distributed solutions, lacking of user obligation, only provide relatively poor anonymity. In this study, we propose a new solution of pseudonym change, which works for non-cooperative users and in the absence of intermediary. The basic idea behind our solution is ad-hoc anonymity. The proposed solution allows users to decide whether or not participating according to their own wills. In addition, artificially generated dummies mix up all the users who have participated in pseudonym changes at different times. Theoretical analysis demonstrates that asynchronous pseudonym change and dummy participation notably enhance privacy protection. We implement our solution on a real-world dataset of mobile phone users, which is collected at Boston, MA, and by the Reality Mining, MIT. The simulation results show that our approach significantly outperforms existing solutions.

# I. INTRODUCTION

The proliferation of positioning technology and mobile computing has fostered the demand of location-based services (LBSs). LBSs enable a range of applications through exploiting user locations. The most common application is online maps. For instance, Google Map Mobile [1] provides detailed maps according to a users current location. Advanced service providers (SPs) also inform users near-by facilities (e.g., restaurants, hotels, or shopping malls) or public activities, (e.g., art performances or road shows).

In current LBS schemes, SPs require users reporting their accurate locations, which plants potential intrusion of location privacy. SPs may sell user data to third parties. Adversaries can analyze these released data and obtain information illegally. Attacker can even disguise as a legal SP, or invade the databases of genuine but careless SPs. In these cases, user location information are exposed to adversaries, which would bring about further information leaking of religion belief, health status, political affiliation, and life style. [2] Privacy disclosure raises the concerns of LBS users and limits the development and application of LBS [3].

A direct countermeasure is to report location information anonymously. When communicating with SPs, each user employs a pseudonym instead of its actual identity. Anonymity breaks the linkage between location information and real identity. Even if locations are exposed, attackers are unaware of the subject. However, simple anonymity provides poor protection from privacy disclosure because, in some cases, locations are highly identity-related. Service requests at a private area can expose the owner of this area, no matter whether a pseudonym is used or not. The knowledge of ownership information is usually obtained by other means. Once a pseudonym gets compromised, it becomes totally meaningless since then, because all behaviors behind this pseudonym are open in the air. Using unchanged pseudonyms increases the risk of being tracked.

Many approaches have been proposed to address the aforementioned tracking attack. Regular pseudonym changing is an effective way to obscure attackers. Even if a user’s identity has been disclosed at a certain time and place, after it changes its pseudonym, attackers are no longer able to link the subsequent private information with the previously recognized identity. Previous studies have shown that it is not easy to fool attackers [4]. It is possible for an attacker to link a new pseudonym with the corresponding old pseudonym given the temporal and spatial relevance of these two. Therefore, a key issue of pseudonym-based protection is how to hide the pseudonym relevance. Fig. 1 gives an example illustrating the importance of hiding pseudonym relevance. Specifically, changing pseudonym alone is useless; therefore one should change its pseudonym simultaneously with other users in order to confuse adversaries. A large number of cooperative users increase the confusion at the attackers side, thus reducing the chance of a pseudonym being compromised. The problem is how to form coalition in mobile and ad-hoc environment, in which users are supposed to be autonomous and self-centered.

Most existing solutions rely on pre-installed intermediary to force user cooperation [4]–[6]. Rather than communicating with SPs directly, a user must submit its location to the intermediary whenever it requests for LBSs. The intermediary gathers location reports from different users, mixes these reports by techniques like data degradation, and then releases the processed reports to SPs. It also informs a user about the appropriate timing to change its pseudonym. Though intermediary performs well, its deployment and maintenance induce huge costs and efforts, and it blocks customized privacy for users, which limit the usability.

On the other hand, several distributed user-centric schemes [7]–[9] enable users to customize their own privacy requirement. User-centric schemes allow a user acting selfishly, changing its pseudonym together with other users only when itself needs to do so. This reduces the overhead of helping other users in pseudonym change. Nevertheless, the noncooperative nature of users limits the achievable degree of privacy. In order to obtain a high degree of privacy, it is essential to have as many users as possible to change their pseudonyms synchronously, which is almost impossible for distributed proposals.

![](images/c3d32b3bb463951836ce4dcbddaffa2cd42a66ff2d3e0ba8f21ec4bdbd7be134.jpg)



(a) Two users change their pseudonyms at time 4 and time 6. Their privacy is weak due to the high relevance between new and old pseudonyms. An attacker can still track them separately.

![](images/2d4efea32d5850a59282ae0ab03a6d6a951bc7b560de3665ede69cc5f03cb603.jpg)



(b) Two users change their pseudonym simultaneously at time 5. The relevance is broken as their new pseudonyms get mixed. An attacker cannot distinguish their courses any more.   
Fig. 1. Spatial/Temporal Relevance and Pseudonym Change

We propose a new solution of pseudonym change, which works for self-centered users and in the absence of intermediary. Different from existing approaches, users can asynchronously renew their pseudonyms; while at the same time, achieve a degree of privacy close to that of synchronous pseudonym change. The basic idea behind our solution is adhoc anonymity. When a user need to change its pseudonym, it forms an ad-hoc pseudonym change set together with users who are willing to change. In addition, artificially generated dummies mix up all the users who have participated in pseudonym changes at different times.

Compared to existing works, our proposal has following advantages:

1) Lightweight. Ad-hoc anonymity is lightweight and distributed, relying on no intermediary deployment. It protects user private information without additional costs of SPs, acceptable by both users and SPs in practice.   
2) Quality of Services. Ad-hoc anonymity provides differentiated services. Users can customize their desired privacy level. We also take the continuity of LBSs into account. Our approach allows non-cooperative users who change pseudonyms only when they would like to do so, avoiding unnecessary loss of quality of services.

3) Effectiveness. Asynchronous pseudonym change with dummy participation enhances user location privacy. The performance is comparable with intermediary-based approaches.

4) Our design is validated through a real-world dataset of mobile users, which is collected at Boston, MA, and by the

Reality Mining, MIT [10]. The dataset contains over 500,000 hours of continuous data on daily human behavior and group interaction.

The rest of the paper is organized as follows. Section II describes the scenario and preliminaries. Section III summarizes related works. We present the theory and design of applying dummies in asynchronous pseudonym change in section IV. In section V, the formal protocol of the proposed Ad-hoc Anonymity is provided. We evaluate our design in Section VI and compare it with previous works. Section VII presents the conclusion of this study.

# II. PRELIMINARY

We consider pedestrian users communicating with SPs using WiFi capable hand-held mobile devices, such as PDAs or smart phones. Each device is equipped with localization module like GPS or Skyhook [11], and communicates with SPs through WiFi access points (APs). We assume that the communication between end-users and SPs is secure, i.e. the wireless channel is encrypted.

We consider the LBSs are untrustworthy. An attacker can be a disguised service provider, or is capable of compromising an existed SP and accessing its data. Moreover, malicious SPs may collude to track a user. Under such attacker model, all users’ location updates can be obtained by an attacker and be exploited to track users. For two reasons we do not consider attacking methods requiring attackers in proximity to users, such as eavesdropping at MAC layer, having agents swarming a user, or participating user cooperations. First, such active attacks are expensive. An attacker needs to set up agents to cover the entire trace of a user, or tail after a user all the time, both of which are impractical. Second, to perform such active attacks on a user, attckers have to be physically close to the user. This usually means that the location of the user is previously leaked.

Generally, protecting location privacy is costly, as it sacrifices quality of services to confuse adversaries. For pseudonym-based approaches, each time a user changes its pseudonym, its ongoing service sessions between itself and SPs are interrupted, losing the continuity of services. For instance, a location-based advertisement application records a list of “ads already read” for each user, in order to avoid sending duplicated ads to a same user. Once a user changes its pseudonym, it would be recognized as a brand new user by the SP, and receives ads it has seen before.

The anonymity of a target user can be measured by the size of an anonymity set [5], [12] that consists of all pseudonyms possibly used by it. As not all pseudonyms have equal probability of being the target, information entropy is commonly used as a finer grained metric of privacy [6], [9], [13], [14]. The entropy of an anonymity set reflects the effective size of the anonymity set, which is the amount of additional information (in terms of number of bits) an adversary need to acquire before it compromises a user successfully. Suppose $X ( i )$ is the set of all possible pseudonyms corresponding to a ( )user $i ,$ and for $j \in X ( i ) , p _ { i } ( j ) = P r ( j = i )$ is the probability of j being $i \ ' s$ ( ) ( ) = ( = ) pseudonym in use. The entropy of pseudonym i is defined as:

$$
H (i) = - \sum_ {j \in X (i)} p _ {i} (j) \log p _ {i} (j)
$$

It reaches the maximum when $\begin{array} { r } { \forall j \in X ( i ) , p _ { i } ( j ) \ = \ \frac { 1 } { | X ( i ) | } . } \end{array}$ . The maximum entropy is $H _ { m } ( i ) = \log | X ( i ) |$ |. Conversely, an ( ) = log ( )entropy of k means the effective size of anonymity set is $2 ^ { k }$ .

# III. RELATED WORKS

# A. k-Anonymity

k-Anonymity [5] focuses on camouflaging single location update. It ensures every piece of revealed location information is indistinguishable from at least other k −  pieces 1by data degradation. Instead of reporting accurate position, a k-anonymous region that encloses k users is reported by each of the k users. This approach reduces spatial precision significantly; on the other hand, attackers cannot individually identify each user from its k-anonymity peers.

An alternative way is delaying location reports until k different location queries have occurred at a particular region. This shrinks the size of enclosure region, improving the data accuracy, while sacrificing the timeliness and impeding services that require real-time location updates.

k-anonymity approaches rely on centralized intermediary to collect user locations and calculate the enclosure regions. Moreover, it is vulnerable to adversaries with tracking ability. Despite the indistinguishability of each single location report of a user, the combination of these location report forms a trajectory, which may be unique and reveal the user identity.

# B. Pseudonyms and Mix Zone

As using long-term persistent pseudonym reveals user identity, one must change its pseudonym regularly to disturb tracking. The problem is how to conceal the relevance between new and old pseudonyms. For example, a user updates its location at p with pseudonym A, then changes to pseudonym $\mathbf { \mathcal { A } ^ { \prime } }$ and updates its location $p ^ { \prime } .$ Given the spatial proximity of p and $p ^ { \prime } ,$ , an adversary can easily guess that A and $\mathbf { \mathcal { A } ^ { \prime } }$ share the same identity.

A countermeasure is Mix Zone [4]. A mix zone is a region that no SP has ever registered any LBS in it and thus no location need to be updated inside it. Once two or more users are in a same zone concurrently, they can change to new pseudonyms immediately. As long as the mix zone is not large enough to incur distinct spatial diversity, attackers can hardly link each new pseudonym with the corresponding old pseudonym correctly. Suppose n users change their pseudonyms in the mix zone. Then for each new pseudonym, attackers can only infer the correct old pseudonym with a probability of ${ \frac { 1 } { n } } .$ An intermediary is needed to maintain possible mix zones forehanded, which prevents customized user privacy.

Alternatively, some distributed mix zone formation strategies are proposed, such as Silent Period [7] and Swing & Swap [8]. The former enables a mobile user changing its pseudonym jointly with another approaching users through entering a silent period simultaneously, in which all nearby users suppress their location updates and wield new pseudonyms. The latter is user-centric, which allows a user broadcasting a union pseudonym change request to neighbors once it feels a change is needed. The neighbors with same needs would reply the request, and jointly form a pseudonym change union.

The limitation of these approaches is that, due to the rarity of concurrency at same place, the number of neighboring users who are willing to participate in a pseudonym change is restricted. Although [8] proposes swapping pseudonym with a random cooperator instead of using new pseudonym, the size of anonymity set is still bounded by the neighborhood scale, and swapping pseudonyms might incur problems like SPs sending data to wrong users.

# C. Path Confusion

Path confusion [15] extends the idea of mix zone to vehicular networks by exploiting road intersections as mix zones. Imagine a user A passes an intersection and another user B passes the same intersection later. The intermediary would postpone the publication of A’s location reports until B passes the intersection, then release the two reports of A and B to SPs simultaneously. This mixes two users’ trails at the intersection, though it sacrifices the timeliness significantly.

CacheCloak [6] improves the timeliness of path confusion through prediction. Intermediary predicts a user’s movement and retrieves all data on the predicted course from SPs. Users request LBS data on predicted courses from the intermediary. Once user deviates from the predicted course, a new predicted course is constructed. The predicted course ends at another user’s predicted course, thus confusing attackers.

CacheCloak requires powerful intermediary that is capable of making accurate prediction and caching all kinds of service data at different locations. Moreover, it is not suitable for pedestrian users as the pedestrian movements are not as predictable as that of vehicles.

![](images/2693910259c7700d810a051a7d5ae61546245d942b3afc9ceb354578c8f97bb2.jpg)



(a) Pseudonym change without dummy

![](images/efe7179fd81505f503560589c92a09aa8162ff73b7d52e2610d3f15d10ab0e77.jpg)



(b) Pseudonym change with dummy   
Fig. 2. Motivating Example

# IV. ASYNCHRONOUS PRIVACY

# A. Motivating Example

Before we formally describe the design of Ad-hoc Anonymity, we use an example to demonstrate how dummy usage enhances location privacy. Suppose five users are in an area, accessing LBSs with pseudonyms A, B, C, E, and $\mathcal { F }$ at the beginning. As Fig. 2(a), A, B, C decide to change their pseudonyms together, while $\mathcal { E }$ and $\mathcal { F }$ refuse to cooperate as they want to keep current service sessions. ${ \mathcal { A } } , { \mathcal { B } } , { \mathcal { C } }$ jointly perform the first round of pseudonym change and yield new pseudonyms $B ^ { \prime } , C ^ { \prime } , A ^ { \prime } ,$ , respectively. Later, $\mathcal { E }$ and $\mathcal { F }$ have finished their service sessions, and are ready to change their pseudonyms. This time, $A ^ { \prime } , B ^ { \prime } , { \mathcal { C } } ^ { \prime }$ refuse to help them because new service sessions have just begun. As a result, only $\mathcal { E }$ and $\mathcal { F }$ change pseudonyms in the second round, yielding ${ \dot { \mathcal { F } } } ^ { \prime }$ and $\mathcal { E } ^ { \prime } .$ . After a period of time, $A ^ { \prime } , B ^ { \prime } , { \mathcal { C } } ^ { \prime }$ agree on another pseudonym change, change to $B ^ { * } , A ^ { * } , \mathcal { C } ^ { * }$ respectively. Finally, all five users leave the area with their new pseudonyms. A series of pseudonym changes create two separated anonymity set $\{ \mathcal { A } ^ { \ast } , \mathcal { B } ^ { \ast } , \mathcal { C } ^ { \ast } \}$ and $\{ \mathcal { E } ^ { \prime } , \mathcal { F } ^ { \prime } \}$ of size  and , respectively. And 3 2the corresponding entropies are   ≈ . and $\log 2 = 1$ . loSince E is obviously not relevant to $A ^ { * } , B ^ { * }$ 1 59, and $\mathcal { C } ^ { * }$ log 2 = 1, an attacker has at least chance to make a successful guess about ${ \boldsymbol { \mathcal { E } } } { ^ { \prime } } { \mathrm { { s } } }$ 50%actually used pseudonym.

Now consider another scenario in which a dummy is used. A dummy is artificially generated and manipulated by a human user. It communicates to SPs routinely and reports the same location information as its owner’s. Once there is a pseudonym change, the owner joins based on its willing, and the dummy participates randomly. In this case, the five users still do not agree on the time of changing pseudonyms. However, this time, during the first round $( { \mathcal { A } } , { \mathcal { B } } , { \mathcal { C } }$ are the participants.), one of them generates a dummy pseudonym $\mathcal { D } ^ { \prime }$ and releases it afterwards, as shown in Fig. 2(b). In the second round, the dummy tosses a coin and decides to participating the pseudonym change of $\mathcal { E }$ and ${ \mathcal F } .$ . After the second round, $\mathcal { E } , \mathcal { F }$ has changed to ${ \mathcal { F } } ^ { \prime } , { \mathcal { E } } ^ { \prime }$ respectively, and the dummy $\mathcal { D } ^ { \prime }$ has changed to $\mathcal { D } ^ { \prime \prime }$ . The dummy ceases to update its location and gets disposed by its owner after the final round.

An attacker is aware of the occurrence, participants, and produced new pseudonyms of any pseudonym change via its observation. It knows neither the correspondence between new and old pseudonym, nor which pseudonym is dummy. Fig. 3 shows all possible pseudonym change paths of $\mathcal { F }$ and A. The size of the anonymity set of $\mathcal { F }$ is . In an attacker’s eyes, 5even if it discovers the existence of a dummy, it can hardly tell which one of $A ^ { \prime } , B ^ { \prime } , { \mathcal { C } } ^ { \prime } , { \mathcal { D } } ^ { \prime \prime }$ is the dummy. Considering the probability distribution, there are two cases.

• Case $1 , \ D ^ { \prime \prime }$ is the dummy, the probabilities of $\mathcal { F }$ being $A ^ { * } , B ^ { * } , \mathcal { C } ^ { * } , \mathcal { E } ^ { \prime } , \mathcal { F } ^ { \prime }$ are $\{ 0 , 0 , 0 , 1 / 2 , 1 / 2 \}$ respectively.   
• Case 2. One of ${ \mathcal { A } } ^ { \prime } , B ^ { \prime } , { \mathcal { C } } ^ { \prime }$ 0 0 1 2 1 2is the dummy, the probabilities are $\{ 1 / 9 , 1 / 9 , 1 / 9 , 1 / 3 , 1 / 3 \}$ .

The probabilities of case 1 and case 2 are $1 / 4$ and $3 / 4$ 1 4 3 4correspondingly. Therefore, the integrated probability distribution of $\mathcal { F }$ is $\{ 1 / 1 2 , 1 / 1 2 , 1 / 1 2 , 3 / 8 , 3 / 8 \}$ , and the entropy $H ( \mathcal { F } ) = 1 . 9 6$ 1 12 1 12 1 12 3 8 3 8. Similarly, the probability distribution of $\mathcal { A }$ is $\{ 5 / 1 8 , 5 / 1 8 , 5 / 1 8 , 1 / 1 2 , 1 / 1 2 \}$ , and $H ( A ) = 2 . 1 4$ . Compared 5 18 5 18 5 18 1 12 1 12 ( ) = 2 14to the situation without dummy, the entropies are much larger.

# B. Privacy Analysis

We analyze the gain of entropy from dummy usage. Consider 3 rounds of pseudonym change of $n _ { i }$ participants in each round $( i = 1 , 2 , 3 )$ . For simplicity, we assume the 3 pseudonym = 1 2 3change sets are pairwise disjoint. Consider a user A attending round 1. Its entropy is $n _ { 1 }$ after the pseudonym changes.

logNow suppose A employs a dummy during round 1, and the dummy takes part in round 2 and 3. Define $n _ { i } ^ { * } = n _ { i } + 1$ , for each resulting pseudonym $X _ { 1 _ { i } }$ from round 1 $( i = 1 , \ldots , n _ { 1 } )$ , $p _ { 1 _ { i } } = P r ( X _ { 1 _ { i } } = \mathcal { A } ) = 1 / n _ { 1 } ^ { * }$ . For each $X _ { 2 i } , i = 1 , \dotsc , n _ { 2 } .$ , $p _ { 2 _ { i } } ~ = ~ P r ( X _ { 2 _ { i } } ~ = ~ { \mathcal A } ) ~ = ~ 1 / n _ { 1 } ^ { * } n _ { 2 } ^ { * }$ =. For each $X _ { 3 _ { i } } , i \ =$ $1 , \ldots , n _ { 3 } + 1$ = ) = 1 =(including the dummy pseudonym after round $3 ) , p _ { 3 _ { i } } = P r ( X _ { 3 _ { i } } = { \mathcal { A } } ) = 1 / n _ { 1 } ^ { * } n _ { 2 } ^ { * } n _ { 3 } ^ { * }$ . The entropy of A is

$$
\begin{array}{l} H _ {3} (\mathcal {A}) = - \sum_ {i = 1} ^ {n _ {1}} p _ {1 _ {i}} \log p _ {1 _ {i}} - \sum_ {i = 1} ^ {n _ {2}} p _ {2 _ {i}} \log p _ {2 _ {i}} - \sum_ {i = 1} ^ {n _ {3} + 1} p _ {3 _ {i}} \log p _ {3 _ {i}} \\ = \log n _ {1} ^ {*} + \frac {1}{n _ {1} ^ {*}} \log n _ {2} ^ {*} + \frac {1}{n _ {1} ^ {*} n _ {2} ^ {*}} \log n _ {3} ^ {*} \\ \end{array}
$$

This is larger than $n _ { 1 }$ (obtained without a dummy).

This result can be generalize to k rounds of pseudonym change. Let $n _ { i }$ denote the number of participants in round i and define $n _ { 0 } = 0$ . The resulting entropy of A is

![](images/8b29b904619f6170bb483f7ef2ac42d1e70bd76b99bfbd4292cab4a7201bece2.jpg)



(a) F ’s possible paths

![](images/3765458a8dd5725022a36f8dfef3cbdea3c578fc1818c572d1dce8169f617585.jpg)



(b) A’s possible paths   
Fig. 3. View of Attackers

$$
H _ {k} (\mathcal {A}) = \sum_ {i = 1} ^ {k} \left[ \left(\prod_ {j = 0} ^ {i - 1} \frac {1}{n _ {j} ^ {*}}\right) \log n _ {i} ^ {*} \right]
$$

Note that, k is the number of rounds participated by the dummy. As $H _ { k + 1 } ( A ) \ - \ H _ { k } ( A ) \ = \ \prod _ { i = 0 } ^ { k } ( 1 / n _ { j } ^ { * } )$ log $n _ { k + 1 } ^ { * } ,$ ( ) ( ) = (1 ) logthe additional benefit decreases as the dummy participating more rounds if all $n _ { i } –  s$ are approximating to each other. It is reasonable to recycle the dummy at an appropriate time once it is less effective.

The ambitious participation of pseudonym change seems to reveal the dummy. Suppose a dummy joins k pseudonym changes sequentially. An attacker only sees that every two adjacent pseudonym changes share a pseudonym. (As in Fig. 2(b), round 1 and 2 share $\mathcal { D } ^ { \prime }$ , whereas round 2 and round 3 share $\mathcal { D } ^ { \prime \prime } . )$ The attacker has no idea whether these common pseudonyms correspond to a same user (who possibly being the dummy). Three rounds {A, B, C}, {C, E, F} and $\{ \mathcal { F } , A , B \}$ produces the same phenomenon as above example. Consequently, there is no pseudonym participating multiple rounds of pseudonym change in attackers’ eyes and ambitious participation is transparent to attackers.

We summarize the benefits of using dummies in pseudonym change. First of all, a dummy does not care the quality of services as much as its owner, thus it can give up its ongoing service session and swift to a new pseudonym with less hesitate. Second, as a dummy involves in different pseudonym change unions, it enlarges the anonymity set of itself. It also benefits all cooperating participants by enlarging their anonymity set, as the dummy chains the pseudonym changes process at different time. In one word, the use of dummy enables users changing their pseudonyms asynchronously, and mixes up all participants.

# V. PROTOCOL DESIGN

Ad-hoc Anonymity consists of two main parts: asynchronous pseudonym and anonymity with dummy participation.

# A. Asynchronous Pseudonym Change

Ordinarily, a user updates its location to SPs in as good accuracy and precision as possible using a pseudonym and expects to receive high quality of services. It customizes the privacy preference by setting a maximum lifetime T for each pseudonym. When a pseudonym is overdue, a user prefers to believe that it takes a high risk of getting compromised and thus needs a pseudonym change. The more privacy, the shorter T is set. When the user has used a pseudonym for more than T time, it enters preparation phase and plans to change its pseudonym as soon as possible.

1) Preparation Phase: A user seeks for collaborators for pseudonym change. We consider users being selfish, thus only users in preparation phase will cooperate. Users can be clustered by their connected AP, and the coverage region of an AP forms a potential mix zone naturally. A user in preparation phase needs to find a region that contains some other users in preparation phase. It is possible that a user must pass through several AP zones before it runs into another collaborator.

At the moment a user enters preparation phase and each time it enters a new zone, it broadcasts a pseudonym change request to all other users in proximity. Once a user in preparation phase (or it will enter preparation phase soon) receives such a request, it responds to the sender. The sender waits for a period of time collecting responses. In case of no responder showing up, it stays in preparation phase and waits for another opportunity. If some responders are found, the sender and all responders form an ad-hoc pseudonym change union and shift to change phase.

A user in preparation phase can keep on accessing LBSs if it likes, but it replaces the accurate location by the coverage area of corresponding AP in its location reports. This cloaks the spatial relevance between its new and old pseudonym and guarantees the indistinguishability between its new pseudonym and other newly born pseudonyms after its future pseudonym change.

2) Pseudonym Change Phase: In this phase, users in a coalition change their pseudonyms together. Each participant selects a random period, and suppresses all communication with SPs during this period. After the silent period, it generates a new pseudonym and resumes communication with SPs with the new one. All previous ongoing service sessions are terminated, and a user starts new sessions for its subscribed LBSs after pseudonym change.

# B. Dummy Participation

1) Dummy Generation: A dummy is a virtual user but acts as a real one. It is generated by its owner. Dummies also use pseudonyms to make them indistinguishable from human users. Though a dummy can be born at any time, its exposure to the outer world needs to be carefully considered. Otherwise, it gets recognized by adversaries because it looks like an unknown user coming from nowhere. An owner should keep its dummy doing nothing until the right time comes.

The chance to activate a dummy is the pseudonym change its owner involves. During the pseudonym change, all users keep silent to SPs, and resume communication after a random period. The owner can release its dummy to interact with SPs at this moment. On an attacker’s side, it observes that the number of pseudonyms increases by 1 after the pseudonym change, and hence suspects a dummy has been injected into this zone. However, given n users and n  pseudonyms after + 1change, each newly born pseudonym has merely a probability of $\textstyle { \frac { 1 } { n + 1 } }$ being the dummy. This protects the dummy from being n+1 recognized by attackers early and easily.

2) Dummy Manipulation: A dummy is manipulated by its owner to interact with SPs routinely. Its behavior is just the same as a normal user does. As long as the owner remains in the zone, it receives pseudonym change requests from other users in preparation phase from time to time. The owner could freely take part in any pseudonym change initiated by these requesters. Alternatively, rather than participating on its own, it asks its dummy cooperating with requesters. The owner accordingly avoids frequent interruption of its ongoing LBS sessions caused by pseudonym change.

Although ambitious participation would not tell a dummy, to enhance privacy, we let a dummy take part in pseudonym changes probabilistically rather than deterministically. Upon receiving a pseudonym change request, a dummy cooperates at a probability p, which could be tuned by its owner. No matter the dummy is going to join or not, the owner could always prefer to participate at its own will.

3) Dummy Disposal: First, a dummy is needed to be disposed when its owner is going to leave. Pair of users leaving an area and entering another one simultaneously is likely to be a dummy and its owner. Such information can be captured by attackers through observation. Another case of dummy disposal occurs when a dummy becomes less meaningful. As mentioned in Section IV-B, the entropy gain is getting trivial for a long-time used dummy. It is necessary to recycle a over due dummy.

Discarding is the simplest way to deal with the dummy. However, the opportunity is important. Considering the example in Section IV-A, if $\mathcal { D } ^ { \prime \prime }$ get destroyed as soon as the second round of pseudonym change is finished, the attacker is convinced that a dummy has joined both round 1 and round 2. By a simple intersection of two pseudonym change sets, the attacker could figure out the dummy and thus learns that $\mathcal { E } ^ { \prime } , \mathcal { F } ^ { \prime }$ have no relevance with A, B, C. To overcome this, the owner should only destroy the dummy right after any round of pseudonym change the dummy involved. As shown in section IV-A, the attacker cannot identify the dummy during the entire life cycle of the dummy under such strategy.

# C. Recognizability of Dummies

The generation and disposal of a dummy might provide an attacker with additional information, as they potentially imply the owner of the dummy. In Fig. 2(b), the attacker could guess the owner of the dummy is among A, B, and C. To counter this, a smart owner could change its strategy of dummy creation. Rather than releasing the dummy after a round of pseudonym change the owner involves, it can release the dummy after any round of pseudonym change happens after it enters the zone, even if itself is not involved. Under such strategy, all the five users could be the owner of the dummy in the example. Similarly, the disposal could be conducted after any pseudonym change happens in the zone.

# VI. EVALUATION

# A. Simulation Setup

To simulate realistic human mobility patterns for Ad-hoc Anonymity, we utilizes a trace-based simulation. We obtained the Reality Mining Dataset from MIT Media Lab. The dataset is collected through smart phones with pre-installed data collection softwares. One hundred human subjects have participated in the project for over nine months. The dataset includes approximately 500,000 hours of data in total, on users’ location, communication and device usage behavior [10]. More than 3,000,000 location update records are used for our simulation.

The performance of our design is measured mainly based on two metrics. Entropy defined in Section II is applied to measure the achieved privacy level of each individual user. To reflect user-centric nature, we assign each user a preferred maximum duration of a pseudonym, and reset a user’s entropy to 0 once it has used the same pseudonym longer than its preferred duration threshold. We also apply mean service session duration to measure the impacts of changing pseudonyms on quality of services. We consider a service provider of online map services. A user uploads its location continuously and retrieves geographic information from the SP. We assume that the SP is always available for user request and would not interrupt service sessions actively. Mean service session duration of a user is defined as the timespan between it starting a service session to the end caused by pseudonym change on average. This metric indicates user experience in the sense of how often it is interrupted from a service. Any privacy preserving approach that disturbs users frequently would not be accepted by both SPs and users.

We compare Ad-hoc Anonymity with Swing [8], which is also user-centric. In Swing, once a user desires a pseudonym change, it polls its neighbors, and only these also need pseudonym change would respond and form the pseudonym change set. In addition, we also implement a simple intermediary based protocol, which enforce all users in proximity cooperating once someone asks for a pseudonym change.

![](images/698f32c4b6841404d7fae56557858fd4fadaf141203ec7f58ad345e83a3b1f0c.jpg)



(a) 83 active users

![](images/74acf6d2326a4fc69637b52e3c2958a38c5321fb50db38d2c7846714da0bf267.jpg)



(b) 58 active users

![](images/894d62bf9a77643e0362633aab0dc0fe06f190793e9c6d63c9531ed005d99967.jpg)



(c) 31 active users   
Fig. 4. Entropy v.s. Time

![](images/9535019441635a2e148f409746d3d4fc5651a2553c4b38aca60c0c6e0aa4456a.jpg)



(a) 83 active users

![](images/a564dfafe04d8c22e51fa7481f3aa1b67279f201d160296265d549c6f2b7ee11.jpg)



(b) 58 active users

![](images/4180eb00c07328506a50e567ee3ff248a157d6bbd28eac94d11008e93d604221.jpg)



(c) 31 active users   
Fig. 5. Entropies of Different Users

# B. Results and Analysis

1) Entropy: We first observe the time evolution of the mean entropy across all users. Fig. 4 shows the results in three typical weeks, representing cases of high, medium, and low user density, respectively. Each figure displays 200 samples uniformly distributed across the corresponding week. The value of each sample is the mean entropy across all users active at that time. In all the three cases, Ad-hoc Anonymity outperforms Swing, and approaches the intermediary based protocol. In the low user density case, Ad-hoc Anonymity significantly enhances user privacy when the number of potential cooperators is small.

Fig. 5 presents the entropy distribution among all active users in corresponding weeks. Despite users’ entropies differentiate due to different privacy preferences and movement patterns; for every single user, Ad-hoc Anonymity dominates the performance of Swing. Take Fig. 5(a) as example, the enhancement in entropy for most users are around , which 1implies the effective sizes of corresponding anonymity sets are as much as double those of Swing. When the density of users is sparse (Fig. 5(c)), the gap between Ad-hoc Anonymity and Swing gets more significant. In this case, all users have an average entropy less than  in Swing, and our scheme log 2 = 1guarantees a  entropy for most users.

log 2Fig. 6 shows the cumulative distribution function of individuals with different entropy. About  users in Swing have 40%their entropies lower than , suffering high risk of getting 1compromised as their effective anonymity set is smaller than . 2Our scheme guarantees about  users have their entropies higher than . About half users have entropies higher than , 1 2which means that a user is always indistinguishable among different pseudonyms, comparable with using intermediary.

We also look at density variation for mean entropy. Fig. 7 shows different mean entropy across enclosed users for areas with different population. The enhancement of Ad-hoc Anonymity increases slightly as the user density gets larger. The result also shows the robustness of Ad-hoc Anonymity under low-density environment, where Swing fails to provide users with mean entropy higher than .

Fig. 8 shows the aggregated results in different weeks. The dropping around week  is due to the Christmas vocation and 51the divergence of subject movements in holidays. The result shows persistent superiority of Ad-hoc Anonymity over Swing, especially in weeks with high density of users.

2) Service Session Duration: Fig. 9 presents user individual mean service session duration across a week. Both of Ad-hoc Anonymity and Swing are user-centric approaches, thus the performances on preserving service session are approximating. Compared to intermediary based protocol, every user has its service sessions extended by adopting Ad-hoc Anonymity. The increases vary from a few minutes to more than half an hour.

Fig. 10 shows the CDF of mean service session duration. In intermediary based protocol, almost  users have their 60%average service session time less than 20 minutes, which implies that  users adopting intermediary based protocol 60%get their service sessions interrupted every 20 minutes on average. Meanwhile, the fraction of such users drops to  in 20%Ad-hoc Anonymity. Besides,  users of Ad-hoc Anonymity have their service sessions longer than 40 minutes, which is only achieved by  users of intermediary based protocol.

![](images/1919f2dff5c35f0681a0863620fd97ee8373b1d72f403c27153d9f140c24eb34.jpg)



Fig. 6. CDF of Entropies

![](images/1387fa5eee50d5887e18a8d1aa1a60216ab43359e9fb4e2f0c5ddbd6be73ed18.jpg)



Fig. 7. Mean Entropy v.s. Zone Population

![](images/553a7f2f65df12648ca0fa3acd4d44915370fe545950ee3b7febf2c664c49306.jpg)



Fig. 8. Mean Entropy over Weeks

![](images/8a9ee5838aefd02d438e3b41af26e158c514c663dbfa03f8c929f58a6280638b.jpg)



Fig. 9. Mean Service Session Duration

![](images/9882da865ced137563135a6442068409f72522c29b2f4706e68843a2624e4f90.jpg)



Fig. 10. CDF of Service Session Duration

![](images/0cac18dc003dfa11b554d217012a5e91bfd1c39a385900d457729728bfb74e26.jpg)



Fig. 11. Service Sessions over Weeks

5%Fig. 11 shows the aggregated results of mean service session duration in different weeks. Ad-hoc Anonymity consistently outperforms the intermediary based protocol, and the gap is around 10-15 minutes. The improvement made by our solution encourages user acceptance of Ad-hoc Anonymity.

# VII. CONCLUSION

Existing location privacy schemes require pre-deployed intermediaries to coordinate user behaviors in mobile ad-hoc networks. We present a distributed location privacy protocol, Ad-hoc Anonymity, that obviates the need of intermediary by dummy usage. To endow user preferences on privacy, we allow users changing their pseudonyms asynchronously at their own will. This forms separated anonymity sets, which limits the achievable degree of privacy. Towards obtaining better anonymity, a dummy is employed to link pseudonym changes happening at different times in a region. A dummy can join pseudonym changes freely, and the common participation mixes users paths in different anonymity sets. Trace-based simulation of Ad-hoc Anonymity with real-world data of realistic human mobility patterns is conducted. The results show that Ad-hoc Anonymity outperforms previous user-centric privacy schemes in both protecting user privacy and prolonging user LBS sessions, revealing the potential of dummy usage in protecting location privacy.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program 61190110, NSFC under grant 61171067 and 61133016, National High-Tech R&D Program of China (863) under grant No. 2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200.

# REFERENCES

[1] “Google map for mobile,” http://m.google.com/maps.   
[2] M. Duckham and L. Kulik, Location privacy and location-aware computing. CRC Press, 2006, pp. 34–51.   
[3] L. Barkhuus and A. Dey, “Location-based services for mobile telephony: a study of users’ privacy concerns,” in Proc. Interact, Jan 2003.   
[4] A. R. Beresford and F. Stajano, “Location privacy in pervasive computing,” IEEE Pervasive Computing, vol. 2, no. 1, pp. 46–55, 2003.   
[5] M. Gruteser and D. Grunwald, “Anonymous usage of location-based services through spatial and temporal cloaking,” in Proc. MobiSys ’03, May 2003.   
[6] J. Meyerowitz and R. Choudhury, “Hiding stars with fireworks: location privacy through camouflage,” in Proc. MobiCom ’09, Sep 2009.   
[7] L. Huang, K. Matsuura, H. Yamane, and K. Sezaki, “Enhancing wireless location privacy using silent period,” in Proc. 2005 IEEE Wireless Communications and Networking Conference, Mar 2005.   
[8] M. Li, K. Sampigethaya, L. Huang, and R. Poovendran, “Swing & swap: user-centric approaches towards maximizing location privacy,” in Proc. WPES ’06, Oct 2006.   
[9] J. Freudiger, M. Manshaei, J.-P. Hubaux, and D. Parkes, “On noncooperative location privacy: a game-theoretic analysis,” in Proc. ACM CCS ’09, Nov 2009.   
[10] N. Eagle, A. S. Pentland, and D. Lazer, “Inferring friendship network structure by using mobile phone data,” in Proc. National Academy of Sciences, vol. 106, no. 36, Sep 2009, pp. 15 274–15 278.   
[11] “Skyhook wireless,” http://www.skyhookwireless.com/.   
[12] D. Chaum, “The dining cryptographers problem: Unconditional sender and recipient untraceability,” Journal of Cryptology, Jan 1988.   
[13] C. Diaz, S. Seys, J. Claessens, and B. Preneel, “Towards measuring anonymity,” Jan 2002.   
[14] A. Serjantov and G. Danezis, “Towards an information theoretic metric for anonymity,” in Proc. Workshop on Privacy Enhancing Technologies, Jan 2003.   
[15] B. Hoh, M. Gruteser, and H. Xiong, “Preserving privacy in gps traces via uncertainty-aware path cloaking,” in Proc. ACM CCS ’07, Jan 2007.