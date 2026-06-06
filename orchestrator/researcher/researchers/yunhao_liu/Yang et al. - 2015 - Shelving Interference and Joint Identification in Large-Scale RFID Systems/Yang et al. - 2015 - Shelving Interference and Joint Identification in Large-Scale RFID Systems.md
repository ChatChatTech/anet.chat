# Shelving Interference and Joint Identification in Large-scale RFID Systems

Lei Yang, Member, IEEE, Yong Qi, Member, IEEE, Jinsong Han, Member, IEEE, Cheng Wang, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Prior work on anti-collision for Radio Frequency IDentification (RFID) systems usually schedule adjacent readers to exclusively interrogate tags for avoiding reader collisions. Although such a pattern can effectively deal with collisions, the lack of readers’ collaboration wastes numerous time on the scheduling process and dramatically degrades the throughput of identification. Even worse, the tags within the overlapped interrogation regions of adjacent readers (termed as contentious tags), even if the number of such tags is very small, introduce a significant delay to the identification process. In this paper, we propose a new strategy for collision resolution. First, we shelve the collisions and identify the tags that do not involve reader collisions. Second, we perform a joint identification, in which adjacent readers collaboratively identify the contentious tags. In particular, we find that neighboring readers can cause a new type of tag collision, cross-tag-collision, which may impede the joint identification. We propose a protocol stack, named Season, to undertake the tasks in two phases and solve the cross-tag-collision. We conduct extensive simulations and preliminary implementation to demonstrate the efficiency of our scheme. The results show that our scheme can achieve above 6× improvement on the identification throughput in a large-scale dense reader environment.

Index Terms—RFID, Tag Collision, Reader Collision, Season

# 1 INTRODUCTION

Radio Frequency Identification systems have been deployed in a variety of application domains, such as logistic and supply chain management [1], access control [2], theft detection [3], and tracking [4], etc. An RFID system typically consists of a large number of readers and tags. RFID tags are attached to products and target to enable the identification of those objects. Tags usually have no energy and can only be activated when they are within the electromagnetic field of a reader. The reader interrogates the tags and collects their IDs via RF signals, without the need of keeping in sight or touch. In contrast to the conventional barcode system, RFID systems have many advantages, such as non-optical proximity, long transmission range, and quick identification. Therefore, the promising RFID technology is expected to be widely used in the near future.

The signal collision is one of the most challenging issues when implementing the RFID technology. There are three types of RFID signal collisions. The first type of collision occurs when more than one tag responds simultaneously. In this situation, the signals coming from multiple tags may interfere with each other and prevent the reader from resolving any tag’s ID. We call the first collision as “tag

• L. Yang, Y. Qi and J. Han are with the Department of Computer Science and Technology, Xi‘an Jiaotong University, Xi‘an , China. E-mail: young@tagsys.org, qiy@mail.xjtu.edu.cn, hanjinsong@gmail.com.   
• C. Wang is with the Department of Computer Science and Engineering, Tongji University, Shanghai , China. E-mail: 9chengwang@gmail.com.   
Y. Liu is with the Tsinghua National Lab for Information Science and Technology, Tsinghua University, Beijing, China. E-mail: yunhao@greenorbs.com.

![](images/e3db1d6181e3bcfd71e232df4619817e3a3bc467e63adf5a956f31996614e33d.jpg)  
(a)

![](images/764a0cbffa717e35b8d18630664730aab676d281cba417a43acd2f10898fc255.jpg)



![](images/db7060d3265c474bdac3e5bbbb9418b1580b8cffbc370bab6cfcd47bc6d3393d.jpg)  
(c)   
Fig. 1. Collisions in RFID systems.

collision”, as shown in Fig. 1-(a). The second type of collision occurs in a multi-reader environment, as illustrated in Fig. 1-(b). In this example, readers $r _ { 1 }$ and $r _ { 2 }$ share an overlapped interrogation region (In this paper, we define such a region as ‘contentious region’, the tags within contentious regions as ‘contentious tags’, and other tags as ‘non-contentious tags’). If there are some tags in this region, they cannot resolve the commands from $r _ { 1 }$ or $r _ { 2 }$ when two readers concurrently broadcast their commands. We call this type of collisions as ‘reader collision’. The third type of collision is termed as reader-tag collision, which occurs when one reader is in another reader’s interrogation region. As shown in Figure 1-(c), reader $r _ { 1 }$ is located in $r _ { 2 } \mathrm { ^ { 2 } s }$ interrogation region. Tag $t _ { 1 } \mathrm { ' } s$ response will be ‘drowned’ by the commands from reader $r _ { 2 } .$ , and resulting in a failure that r1 is unable to receive $r _ { 1 }$ is unable to receive $t _ { 1 } \mathrm { \Delta } ^ { \prime } \mathrm { s }$ ID.

Clearly, avoiding collisions is a crucial task in RFID systems, especially when readers are densely deployed. The algorithms to resolve the aforementioned collisions are known as anti-tag-collision, anti-reader-collision, and anti-reader-tag collision algorithms, respectively. As a costeffective and source-limited device, the RFID tag cannot afford the relatively complicated anti-collision algorithms adopted in traditional wireless networks, such as CSMA, CDMA, FDMA, etc. Existing RFID anti-collision algorithms mainly employ Time Dividing Multiple Accesses (TDMA), which allows tags and readers to send signals in different time slots. For example, Framed Slotted ALOHA (FSA) [5], [23]–[26], which is a dominant anti-tag-collision protocol, requires tags to respond in randomly chosen time slots.

By reconsidering the solution of reader-collision in another perspective, we find that it is not necessary to constrain neighboring readers in a strictly sequential processing pattern for the purpose of anti-collision. Usually, the majority of tags are non-contentious in common R-FID applications. They can be concurrently identified by multiple readers because there is no reader collision in those tags. Hence, we propose to identify tags in two phases. In the first phase, we simply allow multiple readers to identify the non-contentious tags simultaneously, while shelving the reader collisions. In this way, the identification throughput of non-contentious tags will be significantly improved. In the second phase, we design efficient protocols to identify the contentious tags. We find that a reader, if it just passively monitors, can facilitate the identification responses from contentious tags that are interrogated by another reader. This observation motivates us to enable collaboration among neighboring readers to enormously reduce the identification delays of contentious tags.

In this paper, we propose a novel scheme, Season, to improve the efficiency for anti-collision based RFID identification. The Season protocol works in two phases. In the first phase, we propose the Season-I protocol in which all readers ignore the reader collisions and concurrently identify non-contentious tags. Season-I extends the existing anti-tag-collision algorithms by adaptively tuning the size of frame to improve the throughput of identification. In the second phase, neighboring readers jointly identify contentious tags. Different from existing approaches, our scheduling protocol, named Season-II, just selects only one reader from neighboring readers to perform the interrogation and lets the others passively collect data from contentious tags. Thus, neighboring readers are able to collaborate with each other in the identification of contentious tags, and save vast time consumed in scheduling. Adopting joint identification, we find that the collaborative readers may face an emerging collision, termed as cross-range collision. We develop another anti-tag-collision protocol, Season-III, to combat the cross-range collision and achieve fast identification.

The rest of this paper is organized as follows. We introduce the system model in Section 2. We present the design of Season in Section 3 and the analysis in Section 4. In Section 5, we examine the performance of Season via preliminary implementation and extensive simulations based on real traces from a large-scale logistics system. At last, we review related work in Section 6 and conclude this paper in Section 7.

# 2 SYSTEM MODEL

In our model, we use slotted channel as the communication model between readers and tags. The transmissions happen within predefined and equally spaced intervals, termed as slots. The reader guarantees the slot synchronization via energizing probe/request. Obviously, the time required to identify tags is proportional to the number of tags. All readers are connected by wired or wireless networks which enables them to communicate with each other at high speed.

Consider a set of readers $\mathcal { R } ~ = ~ \{ r _ { 1 } , \cdot \cdot \cdot , r _ { m } \}$ are demployed at a region. An identification procedure is the procedure to identify all the tags within the region at a time. In this paper, we use the terms ‘collect a tag’, ‘collect data from a tag’, and ‘identify a tag’ interchangeably. For simplicity, we assume a unit disk model for the interrogation region of a reader. Note that our scheme is not constrained by this assumption. We denote $T _ { i } = \{ t _ { 1 } , \cdots , t _ { n } \}$ as the tag set. The tags in $T _ { i }$ i nare located in the interrogation region of reader $r _ { i } . ~ \mathcal { T } ~ = ~ \cup _ { r _ { i } \in \mathcal { R } } T _ { i }$ denotes the set of i r iall tags. The neighboring reader set of $r _ { i }$ is denoted as $\Gamma ( r _ { i } )$ . The tags in $T _ { i } ^ { C } ~ = ~ \cup _ { r _ { i } \in \Gamma ( r _ { i } ) } ( T _ { i } \cap T _ { j } )$ are the i icontentious tags of reader $r _ { i }$ r r i j. They are located in the overlapped regions between $r _ { i }$ iand its neighboring readers. On the contrary, the tags in $T _ { i } ^ { N } = \cup _ { r _ { i } \in \Gamma ( r _ { i } ) } ( T _ { i } \backslash T _ { j } )$ , where $T _ { i } \backslash T _ { j } ~ = ~ \{ t | t ~ \in ~ T _ { i } ~ \& ~ t ~ \notin ~ { \bar { T } } _ { j } \}$ r r i j, are non-contentious tags i jof reader $T _ { i } ^ { C } \cap T _ { i } ^ { N } = \emptyset$ $r _ { i } .$ i j They are only covered by reader $T _ { i } = \dot { T } _ { i } ^ { C } \cup T _ { i } ^ { N }$ ilicity, we let. $r _ { i } .$ . Clearly, $n _ { i } ^ { \mathrm { { 0 } } } = | T _ { i } ^ { N } | , n _ { i } ^ { \mathrm { { 1 } } } = | T _ { i } ^ { C } |$ $n _ { i j } ^ { 1 } = | T _ { i } ^ { C } \cap T _ { j } ^ { C } |$

i i iWe use a undirect graph $\grave { G } = ( \mathcal { R } , E )$ jto denote RCG. Readers $r _ { i }$ and $r _ { j } ,$ ,where $r _ { i } , r _ { j } \in \mathcal { R } .$ , are adjacent in G i j i jif their corresponding nodes are connected by an edge, $i . e .$ ., $( r _ { i } , r _ { j } ) \ \in \ E$ . The degree $d ( r _ { i } )$ of reader $r _ { i }$ is the i jnumber of edges connected to $r _ { i }$ i iin RCG. The maximum idegree of graph G is defined as $\Delta ( G ) = m a x _ { r \in \mathcal { R } } d ( r )$ . rWe assume the readers can be well synchronized through some synchronization protocols [10]. More details about technical background on RFID collisions can be found in Appendix A.

# 3 SEASON

In this section, we first present three important observations that motivate our design. We then present the design of Season and describe the three protocols we propose.

# 3.1 Observations

We observe three intuitive but important facts in practice:

Observation 1: Majority of tags are non-contentious due to the well advanced deployment of readers. If we allow the readers concurrently interrogate non-contentious tags, we can improve the identification throughput. Hence, a key step of improving the identification throughput is to enable the concurrency for neighboring readers in identifying noncontentious tags. This observation motivates us to handle the non-contentious and contentious tags separately.

Observation 2: The minor contentious tags indeed cause the major delay during the identification. Sometimes, only one contentious tag may incur a large delay. As shown in Fig. 2(a), there is one contentious tag in the contentious region between $r _ { 1 }$ and $r _ { 2 }$ , while no tag is in the contentious region between $r _ { 1 }$ and $r _ { 3 }$ . However, both reader $r _ { 1 }$ and $r _ { 3 }$ are not aware of this situation since they have no knowledge about the locations of tags. These two readers have to be activated exclusively if utilizing prior works [6]–[8]. Therefore, we seek to design new identification pattern for contentious tags.

![](images/42dda421f9b38edef64feb772f3cc1681163588809b2f2caa9ee23daddffb718.jpg)



(a)

![](images/19e71fb332d53bd50a3a49bab7e0039edd157c1b3e6dc51563f055b910470896.jpg)



(b)   
Fig. 2. (a) Potential reader collisions incur significant delay; (b) The signal from tag $t _ { 1 }$ will be received by reader $r _ { 1 }$ and $r _ { 2 }$ .

Observation 3: The signals from the contentious tags can be received by the readers that cover these tags. For instance, the responding signal generated by the contentious tag $t _ { 1 }$ will be received by two neighboring readers $r _ { 1 }$ and $r _ { 2 } ,$ , as shown in Fig. 2-(b). If we can deliberately arrange one reader to interrogate the contentious tag while its neighboring readers passively listen to the response from the tag, the system is able to retrieve the data from the contentious tag even there is a potential reader collisions in RCG. Unfortunately, existing approaches do not leverage this feature.

# 3.2 Overview

Motivated by the above observations, we split an identification procedure into two phases. In Phase-I, the system identifies all non-contentious tags. We term this phase as Shelving Interference. In Phase-II, neighboring readers jointly and collaboratively identify contentious tags. We call this phase as Joint Identification. Hence, we propose our anti-collision scheme, Season, to undertake the tasks of these two phases. Season is a protocol stack comprising of three protocols. Season-I is designed to collect data from non-contentious tags in Phase-I. Phase-II includes multiple rounds. In each round, we first employ Season-II to determine appropriate readers for actively interrogating contentious tags while keeping other readers passively listening. Then we conduct Season-III to collect data from contentious tags. The iterative execution of Season-II and Season-III continues until the system collects data from all contentious tags.

# 3.3 Season-I

In Phase-I, Season-I allows neighboring readers to concurrently identify tags in spite of the signal interference occurred at contentious tags. Although those contentious tags cannot correctly resolve the readers’ query commands, this treatment helps us to naturally distinguish all non-contentious tags from contentious tags. The noncontentious tags transmit their IDs and then transfer into the silent state. Our approach can guarantee that the majority of tags can be identified after Phase-I, if most tags are located in non-contentious regions, and hence significantly improve the identification throughput. In an ideal case, there are no contentious tags and all tags can be identified after Phase-I.

Season-I is a state based anti-tag-collision protocol. Similar to FSA, it divides the identification procedure into many frames and each frame contains several equivalent time slots. Being different from FSA based approaches, Season-I adaptively tunes the length of frame to optimize the identification latency. That is, the reader will terminate the frame once it successfully receives a tag’s ID and then start a new frame.

Obviously, each tag independently transmits its ID with a probability of $1 / f$ in each slot. One important goal of Season-I is to choose appropriate f so as to minimize the expected identification time. Not surprisingly, the optimal choice of $\textit { f i s } | T _ { i } ^ { N } |$ . The problem of choosing an optimal f ifor ALOHA based approaches has been widely studied in the literature [11] [12]. But the challenge is that we usually do not know the number of tags in advance. Fortunately, a number of recent works [13]–[16], effectively estimate the number. We adopt USE [13] in Season. We require the reader to estimate number $| T _ { i } ^ { N } |$ before identification. iIn detail, the reader maintains a variable k to record the number of tags that have been collected so far. Initially, $k = 0$ . To minimize the identification time, we dynamically adjust the frame to $\lvert T _ { i } ^ { N } \rvert - k$ after the k-th tag is collected.

# 3.4 Season-II

After all readers finish their identification of noncontentious tags, the system enters into Phase-II. Based on our third observation, we design joint identification protocols to identify contentious tags. For a group of neighboring readers, we only let one of them become active to interrogate the tags while others stay in silence and just passively listen to the signals from contentious tags. Joint identification has two clear advantages: (1) A joint identification can avoid reader collisions among neighboring readers since only one of them sends query commands, (2) Reduce the identification delay significantly because the readers concurrently receive the IDs of continuous tags.

For easy illustration, we term the reader being responsible for interrogating tags as active reader and the reader staying in listening state as passive reader. Hence, the first task in Phase-II is to select appropriate active readers from a group of neighboring readers. We propose Season-II for determining proper active readers.

In our system model, the edges of a reader in RCG represent the contentious regions that the reader shared with its neighbors. In RCG, we determine active readers according to two conditions as follows: (1) they are able to cover edges as most as possible; (2) these active readers will not incur signal interference among themselves if they are concurrently activated. Namely, the selected active readers are not adjacent in RCG. Clearly, these two conditions are the Necessary Conditions for the optimal selection of active readers. We thereby convert the problem of selecting active readers to finding the Maximal Weighted Independent Set (MWIS) in an undirected graph.

Given an undirected graph G. A independent set of V is a subset $S \subseteq V$ such that any two nodes $n , v \in S$ are not neighbors in $V ,$ and every node $w \in S$ has at least one neighbor in $S .$ . The MIS of V is the maximal independent set generated from V . A natural variant of MIS is the maximal weighted independent set (MWIS), where each node is associated with a weight. Solving MWIS is to find a MIS with the maximal total weight of its nodes.

In our problem, we set the weight of each node as the number of its edges since we attempt to employ the minimum nodes (active readers) to cover the maximum edges (contentious regions) in RCG. We adopt a MWIS solution proposed by [17] to determine active readers. For example, as illustrated Fig. 4-(a), the set of active readers is $\boldsymbol { A } _ { 1 } =$ $\{ r _ { 2 } , r _ { 6 } , r _ { 7 } \}$ while others are considered as passive readers, $i . e .$ , the set of passive readers is $\mathcal { P } _ { 1 } = \{ r _ { 1 } , r _ { 3 } , r _ { 4 } , r _ { 5 } \}$ . By activating the active readers in $\mathcal { A } _ { 1 }$ and keeping the readers in $\mathcal { P } _ { 1 }$ listening, the contentious regions corresponding to the edges that are connected to the nodes in $\mathcal { A } _ { 1 }$ are covered by active readers. Thus, the contentious tags in those regions can be powered and successfully collected. However, only one round of finding MWIS is insufficient to cover all the contentious regions. From Fig. 4-(a), we find that the tags in the contentious regions corresponding to edge $( r _ { 4 } , r _ { 5 } )$ cannot be powered by any active readers because both $r _ { 4 }$ and $r _ { 5 }$ are passive readers.

To cover all contentious regions, we start the next scheduling round. In this round, we first let each node mark the edges that have covered in previous scheduling rounds and modify the node’s weight as the number of unmarked edges connected to this node. If the weight of a node equals zero, this node does not involve in this scheduling round. In this way, the active reader set becomes $\mathcal { A } _ { 2 } = \{ r _ { 5 } \}$ and passive reader set is $\mathcal { P } _ { 2 } = \{ r _ { 4 } \}$ in RCG, as shown in Fig. 4- (b). After the second round, all the contentious regions are covered. In practice, Season-II will be executed iteratively until all nodes’ weights become zero.

# 3.5 Season-III

Season-III is designed to tackle a new tag collision. Assume readers $r _ { 1 }$ and $r _ { 2 }$ are chosen as active readers, as shown in Fig. 3. A tag collision happens at reader $r _ { 3 }$ when tag $t _ { 1 }$ and $t _ { 2 }$ are interrogated by $r _ { 1 }$ and $r _ { 2 }$ , respectively. In this case, reader $r _ { 1 }$ can correctly receive the ID of $t _ { 1 }$ and reader $r _ { 2 }$ can retrieve the ID of $t _ { 2 }$ . However, reader $r _ { 3 }$ cannot collect any ID because of the collision from two tags. We define such a tag collision as cross-range tag collision 1. Furthermore, both of reader $r _ { 1 }$ and reader $r _ { 2 }$ have no knowledge about whether reader $r _ { 3 }$ has collected data from all contentious tags. They have to continuously power the contentious tags event if these tags are successfully collected, in order to avoid the misread by passive reader. This leads to a confusion from readers $r _ { 1 }$ and $r _ { 2 } \colon$ when they should stop powering contentious tags? The above issue indicates that Season-I cannot be directly applied to collect data from contentious tags. Therefore, we propose a randomized protocol, Season-III, to allow active and passive readers to identify contentious tags collaboratively.

![](images/e0169d5b024f14505342e8d5b0e3dbedbc25c197b34d0d50051117ac991c6a87.jpg)



Fig. 3. Cross-range tag collision: A tag collision happens at reader $r _ { 3 }$ when tag $t _ { 1 }$ and $t _ { 2 }$ are interrogated by $r _ { 1 }$ and $r _ { 2 } ,$ , respectively. In this case, reader $r _ { 1 }$ can correctly receive the ID of $t _ { 1 }$ and reader $r _ { 2 }$ can retrieve the ID of $t _ { 2 }$ . However, reader $r _ { 3 }$ cannot collect any ID because of the collision from two tags.

![](images/3c2de470298070ca4b6f49031fc12cd9342610325638dd285ede8826a277be31.jpg)



(a)

![](images/db7b0f9a7134bd9537c0a01404a82385dea9f790914680c821cb746ffde1f38d.jpg)



(b)   
Fig. 4. The number on the edge represents the real number of contentious tag. Active readers are shown in highlight. The number in bracket denotes the weight of the reader. $( \mathsf { a } )$ In the first round, active reader set is $\mathcal { A } _ { 1 } ~ = ~ \{ r _ { 2 } , r _ { 6 } , r _ { 7 } \} ~ ; ~ ( 6 )$ In the second round, active reader set is $\mathcal { A } _ { 2 } = \{ r _ { 5 } \}$ 人

Given that the set of active readers is  and the set of passive readers is the $\mathcal { P }$ in the current scheduling round. Season-III works as follows.

On one hand, for active readers:

1) Each active reader $r _ { i } ~ \in { \mathcal { A } }$ starts a special frame ito estimate the number of its contentious tags in its contentious regions using USE [13]. The number is denoted as $n _ { i } ^ { 1 }$ , which can be approximated to $| T _ { i } ^ { C } |$ . For instance, $n _ { 6 } ^ { 1 } \approx 5 , n _ { 2 } ^ { 1 } \approx 3 + 5 + 8 + 9 = 2 5$ i as shown in Fig. 4-(a).

2) Reader $r _ { i }$ divides the procedure into several frames. iEach frame contains $\bar { n } _ { i } ^ { 1 }$ time slots, where $n _ { i } ^ { 1 }$ is a i iconstant. In each frame, every contentious tag in $r _ { i } \mathrm { { ' } s }$ icontentious regions randomly selects a slot to transmit

1. In essence, this collision is a form of tag collision instead of a new type of signal collision.

its ID. Namely, each tag independently transmits its ID with the probability of $1 / n _ { i } ^ { 1 }$ in each time slot.

3) Reader $r _ { i }$ ialways sends an NACK feedback to the itag even if it successfully receives the tag’s ID. This treatment is to force contentious tags always transmit its ID in each frame. In this way, we can guarantee every contentious tag has a chance to be identified by either active or passive readers.   
4) After collecting data from all the contentious tags within its contentious regions, reader $r _ { i }$ still keeps the itags in the active state by powering the tags in this round because its neighboring passive readers may miss some tags due to the cross-range tag collision. This is in contrast to Season-I which immediately forces a tag to enter the silent state if the tag is collected in a slot. Until it receives “FINISH” messages from all its neighboring passive readers, the active reader ends its job in the current identification procedure. Note that once a reader becomes an active reader, it will quit Season after the current round.   
5) Before ending its interrogation in this round, reader $r _ { i }$ broadcasts a $^ { \mathrm { \sc } } \mathrm { S I L E N C E } ^ { \mathrm { \prime \prime } }$ i command to its contentious tags to force them to enter the silent state in the following scheduling rounds. The reader also sets its weight to zero in RCG.

On the other hand, for passive readers:

1) During the estimate phase of active readers, each passive reader $r _ { j } \in \mathcal { P }$ listens to the responses from jtags and estimates the number $n _ { j } ^ { 1 }$ of contentious jtags within the contentious regions between it and its neighboring active readers. The $n _ { i } ^ { 1 }$ estimated by passive readers may be less than $| T _ { j } ^ { \mathcal { \bar { C } } } |$ , since there jmay exist contentious regions among passive readers. After estimation, $\begin{array} { r } { n _ { j } ^ { 1 } = | \bigcup _ { r _ { i } \in \Gamma ( r _ { i } ) \& r _ { i } \in \mathcal { A } } | \frac { \ d } { \ d t } \cap T _ { j } ^ { C } ) | } \end{array}$ . For example, $n _ { 4 } ^ { 1 } = 8$ and $n _ { 5 } ^ { 1 } = 5 + 8 + 9 = 2 2$ jin Fig. 4(a).   
2) Reader $r _ { j }$ passively listens to the responses from jcontentious tags during its neighboring active readers’ interrogation. After collecting these tags, it sends a “FINISH” message to its neighboring active readers.   
3) If reader $r _ { j }$ has no neighboring passive readers in this jround, it ends its job in current identification procedure and sets its weight to zero in RCG. Otherwise, it still executes the Season protocols in the next scheduling round.

The role of readers may change during the scheduling round. Assume the scheduling sequence of active readers is $\{ { \mathcal { A } } _ { 1 } , { \mathcal { A } } _ { 2 } \}$ , where $\mathcal { A } _ { 1 } ~ = ~ \{ r _ { 2 } , r _ { 6 } , r _ { 7 } \}$ and $\mathcal { A } _ { 2 } ~ = ~ \{ r _ { 5 } \}$ as illustrated in the example shown in Fig. 4. Reader $r _ { 5 }$ is a passive reader in the first round but it becomes an active reader in the second round. Once a reader becomes an active reader in one round, its weight will become zero and then finishes identification process.

To illustrate execution of Season, we give an example shown in Fig. 4. At the beginning of the first round shown in Fig. 4-(a), active reader $r _ { 2 }$ estimates the number of its contentious tags $n _ { 2 } ^ { 1 } \approx 3 + 5 + 8 + 9 = 2 5$ . At the same time, the passive reader $r _ { 5 }$ estimates the number of its contentious tags in the current round $n _ { 5 } ^ { 1 } \approx 9 + 5 + 8 = 2 2$ . Reader $r _ { 2 }$ continues to power tags until it collects the 25 tags and also receives the “FINISH” messages from $r _ { 1 } , r _ { 3 }$ , $r _ { 4 }$ and $r _ { 5 }$ . Concurrently, $r _ { 5 }$ listens to the tags’ replies. After successfully collecting its 22 tags, it sends a “FINISH” message to $r _ { 2 } , \ r _ { 6 }$ and $r _ { 7 } .$ . At the end of the first round, all of the readers adjust their weights. Readers $r _ { 1 } , r _ { 2 } , r _ { 3 } , r _ { 6 } ,$ and $r _ { 7 }$ set their weights to zero and report their collections. In the second round as shown in Fig. 4-(b), there are only $r _ { 4 }$ and $r _ { 5 } \mathrm { ^ { * } s }$ weights not equaling to zero in RCG. Reader $r _ { 5 }$ is selected as the active reader. It starts to power tags and $r _ { 4 }$ listens to the tags’ replies. The procedure ends when $r _ { 4 }$ sends a “FINISH” message to $r _ { 5 }$ .

# 4 ANALYSIS

In this section, we analyze the performance of Season theoretically. More extened discusion to potential challenges can be found in on Appendix B.

# 4.1 Analysis of Season-I

We analyze the expected number of time slots required by Season-I in a single identification procedure. Let $n _ { i } ^ { 0 } =$ $| \dot { T } _ { i } ^ { N } |$ i|. According to our design in Season-I, each frame $k ,$ iwhere $0 \leq k \leq n _ { i } ^ { 0 }$ , starts when the k-th tag is identified iand ends upon the identification of (k+1)-th tag. Let $I _ { k } ( r _ { i } )$ k ibe a random variable that denotes the length of k-th frame. Then, the expected identification time is given by:

$$
I \left(r _ {i}\right) = E \left[ \sum_ {k = 0} ^ {n _ {i} ^ {0} - 1} I _ {k} \left(r _ {i}\right) \right] = \sum_ {k = 0} ^ {n _ {i} ^ {0} - 1} E \left[ I _ {k} \left(r _ {i}\right) \right]
$$

There are $n _ { i } ^ { 0 } - k$ unidentified tags in frame k. Each of them itransmits its ID with a probability of $P _ { k } = 1 / ( n _ { i } ^ { 0 } - k )$ 号 k ifor each time slot. Then the probability of a successful transmission in a time slot of frame k is given by:

$$
P _ {s} (k) = P _ {k} \left(1 - P _ {k}\right) ^ {n _ {i} ^ {0} - k - 1} = \frac {1}{n _ {i} ^ {0} - k} \left(1 - \frac {1}{n _ {i} ^ {0} - k}\right) ^ {n _ {i} ^ {0} - k - 1}
$$

Clearly, $I _ { k } ( r _ { i } )$ is a geometrically distributed random varik iable with parameter $( n _ { i } ^ { 0 } - k ) P _ { s } ( k )$ . Thus,

$$
\begin{array}{l} I \left(r _ {i}\right) = \sum_ {k = 0} ^ {n _ {i} ^ {0} - 1} E \left[ I _ {k} \left(r _ {i}\right) \right] = \sum_ {k = 0} ^ {n _ {i} ^ {0} - 1} \frac {1}{\left(1 - \frac {1}{n _ {i} ^ {0} - k}\right) ^ {n _ {i} ^ {0} - k - 1}} \tag {1} \\ = \sum_ {k = 1} ^ {n _ {i} ^ {0}} \frac {1}{(1 - \frac {1}{k}) ^ {k - 1}} \leq n _ {i} ^ {0} e \\ \end{array}
$$

Therefore, the total expected identification time during Phase-I equals $\operatorname* { m a x } _ { r _ { i } \in \mathcal { R } } I ( r _ { i } )$ and the throughput equals $1 / e \approx 0 . 3 6$ .

# 4.2 Analysis of Season-II

Intuitively, Season-II is partially similar to Colorwave [7], which is a graph-coloring based anti-reader-collision approach, but they are essentially different as follows. (1) Season-II is only used to collect contentious tags such that the time consumed in scheduling is far smaller than that of Colorwave. (2) Assuming they have the same scheduling rounds, the scheduling of Season-II is one round less than that of Colorwave because all readers in the last round are passive readers. (3) Season spends less identification time than Colorwave in each round except the first round. This is because the contentious tags collected at the current round will not involve in identification in the next round, $i . e . ,$ the number of tags drops off after each round in Season. In contrast, Colorwave needs to recollect these tags within one reader’s interrogation region. (4) Season-II is more stable than Colorwave and employs less scheduling rounds, which will be demonstrated by our experimental results.

# 4.3 Analysis of Season-III

In Phase-II, the identification time is consumed in collecting contentious tags by active readers or passive readers. There is a slight difference in the analysis of identification time between these two type readers. We first give detailed analysis on active readers and then extend the analysis to passive readers.

Our problem can be viewed as a Coupon Collector’s Problem [18], [19]. In the classical Coupon Collector’s problem, there are n types of coupons. At each trial a coupon is random chosen. Each chosen coupon is equally likely to be from any of the n types, and the random choices of the coupons are mutually independent with a probability of $1 / n$ . The problem is: what is the minimum number of trails required to collect at least one copy of each of the n types? Consequently, the time for collecting the n tags in Season is similar to the minimum time for collecting coupons.

# 4.3.1 Active Reader

Considering an active reader $r _ { i } .$ , the probability of its icontentious tags transmitting their IDs equals $1 / n _ { i } ^ { 1 }$ where $n _ { i } ^ { 1 }$ idenotes the number of its contentious tags. Therefore, ithe probability that an active reader successfully receives a tag’s ID in a given time slot is:

$$
P _ {s} = \frac {1}{n _ {i} ^ {1}} (1 - \frac {1}{n _ {i} ^ {1}}) ^ {n _ {i} ^ {1} - 1} \approx \frac {1}{e n _ {i} ^ {1}}
$$

Note above approximation holds when $n _ { i } \to \infty ,$ which is iformulized and strictly proven in [18]. The identification process can be viewed as a coupon collection problem as follows. In each slot, the reader $r _ { i }$ collects one of the $n _ { i } ^ { 1 }$ tags with probability $\mathit { P _ { s } } \left( i . e . \right.$ i i, only one tag responds), and scollects no tag (i.e. collision happen or no tag responds) with probability $1 - n _ { i } ^ { 1 } P _ { s }$ . The objective of reader $r _ { i }$ is to i s icollect all tags. We utilize the approach proposed in [19] to facilitate our analysis. We can view the process as divided into epochs, where epoch k begins with the slot when the k-th tag is identified and ends (inclusive) when the $( k + 1 ) \cdot$ - th tag is identified. We define the random variable $I _ { k } ( r _ { i } )$ , $0 \leq k \leq n _ { i } ^ { 1 } - 1$ k i, as the length of epoch k. Clearly, the iexpected identification time $I ( r _ { i } )$ is given by:

$$
I (r _ {i}) = E \left[ \sum_ {k = 0} ^ {n _ {i} ^ {1} - 1} I _ {k} (r _ {i}) \right]
$$

It is easy to find that $I _ { k } ( r _ { i } )$ is a geometrically distributed with parameter $( n _ { i } ^ { 1 } - k ) P _ { s }$ . Thus, by linearity of expectation, we have

$$
\begin{array}{l} I \left(r _ {i}\right) = E \left[ \sum_ {k = 0} ^ {n _ {i} ^ {1} - 1} I _ {k} \left(r _ {i}\right) \right] = \sum_ {k = 0} ^ {n _ {i} ^ {1} - 1} \frac {1}{\left(n _ {i} ^ {1} - k\right) P _ {s}} = \frac {1}{P _ {s}} \sum_ {k = 1} ^ {n _ {i} ^ {1}} \frac {1}{k} \\ = \frac {1}{P _ {s}} \bar {H} _ {n} \approx n _ {i} ^ {1} e \bar {H _ {n}} \\ \end{array}
$$

where $H _ { n }$ denotes the n-th Harmonic number and equals nto ln n + Θ(1), implying that

$$
I (r _ {i}) \approx n _ {i} ^ {1} e (\ln n _ {i} ^ {1} + \Theta (1)) = n _ {i} ^ {1} e \ln n _ {i} ^ {1} + \mathcal {O} (n _ {i} ^ {1}) \tag {2}
$$

# 4.3.2 Passive Reader

Considering a passive reader $r _ { i }$ , the probability of its conitentious tags transmitting their IDs is not equivalent since the neighboring active readers of $r _ { i }$ broadcast frames with different lengths. Assume reader $r _ { j }$ is one of neighboring active readers of $r _ { i }$ . We define $n _ { i } ^ { 1 }$ jas the number of $\cdot { T _ { j } ^ { C } }$ and $n _ { i j } ^ { 1 }$ ias the cardinality of $T _ { i } ^ { C } \cap T _ { i } ^ { \not C }$ j. Then the probability that ij only one tag t , where $t \in T _ { i } ^ { \not C } \cap T _ { j } ^ { C }$ , transmits its ID is given by

$$
P _ {i j} = \frac {1}{n _ {j} ^ {1}} \left(1 - \frac {1}{n _ {j} ^ {1}}\right) ^ {n _ {i j} ^ {1} - 1}
$$

Obviously, only when one tag responds in one of the reader’s contentious regions, the reader can successfully receives the tag’s ID. Therefore, according to the total probability theorem [20], the probability that reader $r _ { i }$ successfully receives a tag ID in a given time slot is:

$$
\begin{array}{l} P _ {s} = \sum_ {r _ {j} \in (\Gamma (r _ {i}) \cap \mathcal {A})} P _ {i j} \cdot \prod_ {r _ {k} \in (\Gamma (r _ {i}) \cap \mathcal {A}) \setminus r _ {j}} (1 - P _ {i k}) \\ = \sum_ {r _ {j} \in (\Gamma (r _ {i}) \cap \mathcal {A})} \frac {P _ {i j}}{1 - P _ {i j}} \cdot \prod_ {r _ {k} \in (\Gamma (r _ {i}) \cap \mathcal {A})} (1 - P _ {i k}) \\ \end{array}
$$

where  is the active reader set in the current round. Let $\begin{array} { r } { \Pi = \prod _ { r _ { k } \in \ O ( \Gamma ( r _ { i } ) \cap \mathcal { A } ) } ( 1 - P _ { i k } ) } \end{array}$ ,

$$
\begin{array}{l} {P _ {s}} {= \Pi \cdot \sum_ {r _ {j} \in (\Gamma (r _ {i}) \cap \mathcal {A})} \frac {P _ {i j}}{1 - P _ {i j}}} \\ = \Pi \cdot \sum_ {r _ {j} \in (\Gamma (r _ {i}) \cap \mathcal {A})} \left(\frac {1}{1 - P _ {i j}} - 1\right) \\ = \Pi \cdot \left(\sum_ {r _ {j} \in (\Gamma (r _ {i}) \cap \mathcal {A})} \frac {1}{1 - P _ {i j}} - m\right) \\ \end{array}
$$

where $m = | \{ r _ { j } | r _ { j } \in ( \Gamma ( r _ { j } ) \cap A ) \} |$

j j jAccording to Cauchy inequality, we have

$$
\frac {m}{\sum_ {r _ {j} \in (\Gamma (r _ {i}) \cap \mathcal {A})} \frac {1}{1 - P _ {i j}}} \leq \sqrt [ m ]{\Pi}
$$

![](images/c9b87ca1704f07fa11608cdb222cae78ed19ea6cd472f32e83629fc10e88ffd0.jpg)



(a)

![](images/7fd4a144f197cd90f828bffb20fffd7827246f7358f1ac0ff5879c2050e991b9.jpg)



(b)   
Fig. 5. (a) The multiple readers scenario in our lab; (b) The deploy map in postal processing center.

![](images/9908ca6437bb492f58d5f83e09401434bfc30dfb2bc96b0e61bae224fbd09e01.jpg)  
(a) Sparse

![](images/0fb387b7c293254ccd53f676b51ea7a95a3cd2b081736705fa12fe7e7996d1f5.jpg)



(b) Moderate

![](images/df760bd9df3377d8c4349dda65e59eade60b5846f927053237d3b81e127d19be.jpg)



(c) Dense   
Fig. 6. Randomly generated three separate RCGs with 100 readers, labeled with “Sparse”, “Moderate”, and “Dense”.

$$
\sum_ {r _ {j} \in (\Gamma (r _ {i}) \cap \mathcal {A}} \frac {1}{1 - P _ {i j}} \geq \frac {m}{\sqrt [ m ]{\Pi}}
$$

Therefore,

$$
P _ {s} \geq m \Pi (\Pi^ {- 1 / m} - 1)
$$

$$
I (r _ {i}) = \frac {1}{P _ {s}} H _ {m} \leq m \Pi (\Pi^ {- \frac {1}{m}} - 1) H _ {m} \tag {3}
$$

# 5 PERFORMANCE EVALUATION

We now evaluate Season using real-world logistics and tracking traces.

# 5.1 Evaluation Methodology

# 5.1.1 Testbed and deployment

In our preliminary implementation, we implement the Season protocols in a prototype system based on G2M5477, which is a programmable tag module manufactured by G2 Microsystems, to examine the feasibility of Season on tags. We deploy three ALR-9900 readers in Portable and Adjustable Mounting Framework (PAMF) with 3m wide and 4m height, as shown in Fig. 5-(a). The three reader antennas are located on the top, left and right bars in the PAMF. We specify the reader hopping between 50 channels in the 902MHz 928MHz. The channel spacing is about 500KHz. The RF power is adjusted to 20dBm. We also put $4 ^ { * } 3 ^ { * } 5 { = } 6 0$ boxes on a testing tray and each box is attached with off-the-shelf passive tags. To further validate the feasibility of joint identification, we use a NI PXI-1044 RFID testing tool with PXI 5600 receiver as our passive reader. We uniformly set the power of antenna as 20 dBm which supports around an interrogation range of 2m.

We deploy a prototype with five readers in a logistics enterprise, Xi’an postal processing center in Shaanxi, China. The center is the one of the seven largest postal processing centers in China. It covers an area of about $1 6 , 1 2 8 m ^ { 2 }$ and contains 30 importing/exporting gates. Fig.5-(b) shows the architectural plans of the center. We attach more than 100 passive tags into pouches and find that the percentage of contentious tags is less than 10% for a stable and full coverage.

# 5.1.2 Simulating Real RFID Applications

For simulation, we use two typical application scenarios and three random reader topologies described as follows.

Warehouse: According to our measurement results in Xi’an postal center, we simulate a total of $1 2 * 6 = 7 2$ readers for covering the entire center in a square-grid formation. Each reader is located at one vertex in the grid. Each reader has an interrogating range of $7 m .$ , which has 126 contentious regions. We employ the real EMS trace of this center, which deliveries 2,456 items, including express mails, parcels, and boxes, to a medium-size city each day on average. We collect the delivery records in the month of December, 2009 as our basic dataset. The dataset contains 78,606 records.

Object tracking: We collect the tracking dataset from the RFID Ecosystem project [21]. The deploying map is shown in [22]. There are 30 readers (or antennas) in the deployment area. The tracking dataset has 1653 records. Each record includes the tag locations, source, and identification time.

Random Topologies: Without losing generality, we also randomly generated 3 separate RCGs with 100 readers, labeled with “Sparse”, “Moderate”, and “Dense”, respectively. They have different maximum degrees to reflect the three deploying topologies, as summarized in Table 1. The topologies of these three RCGs are also illustrated in Fig.6.

# 5.1.3 Performance Metrics

Assume the set of time slots consumed by a single reader $r _ { i }$ is $\mathcal { T } ( r _ { i } )$ i, then the identification time of this reader equals $I ( r _ { i } ) = | \mathcal { I } ( r _ { i } )$ |. Besides the identification itme, we also measure the throughput and delay, which are defined as follows.

Throughput: It is defined as the ratio of total number of tags to the overall identification time, denoted as λ. Namely,

$$
\lambda = \frac {| T |}{| \bigcup_ {r _ {i} \in \mathcal {R}} \mathcal {I} (r _ {i}) |}
$$

Average Delay: The delay of tag t, denoted as $D ( t )$ , is defined as the expected number of time slots consumed by tag t in waiting for its identification. The average delay is defined as

TABLE 1 Summary of applications 

<table><tr><td>Scenarios</td><td># of readers</td><td># of max degree</td><td># of edges</td><td># of tags</td></tr><tr><td>Warehouse</td><td>72</td><td>4</td><td>126</td><td>2,456</td></tr><tr><td>Tracking</td><td>30</td><td>3</td><td>29</td><td>1,653</td></tr><tr><td>Sparse</td><td>100</td><td>3</td><td>133</td><td>50,000</td></tr><tr><td>Moderate</td><td>100</td><td>8</td><td>343</td><td>50,000</td></tr><tr><td>Dense</td><td>100</td><td>16</td><td>495</td><td>50,000</td></tr></table>

![](images/cb53fd452529263c259ad07c81eef5225cc9e90ecbe622d994b06365d93dbbc2.jpg)



Fig. 8. Throughput

![](images/7a2a0f2d33773ab340d906edb978a0e1dc7235d7a0bf71ae7cb8d1b5a1ad20ae.jpg)



Fig. 9. Read rate

![](images/41ddd73c2f0f3658506b6f4bb8bc16442aa0e1e9c8136ea90134f3f556e14bbd.jpg)



Fig. 10. Time

![](images/33848485fc003f6fc83ab1129575a641352cce7da09a621f21bbced42362229f.jpg)



Fig. 11. Throughput

![](images/f68ac7f8a9e90d61a35e5b4605bfe8f62956a414e14bf11eb1dc4e89dfe57d9d.jpg)



(a) Without reader collision   
![](images/40d06f791cf13a938c00aef4999247b32200171374816e0648e5ec3ed57f2db4.jpg)



(b) With reader collision   
Fig. 7. The identification results are shown in our visualization tool. In the figure, these tags attached in the highlighted boxes are collected.

$$
D _ {a v g} = \frac {\sum_ {t _ {i} \in T} D (t _ {i})}{| T |}
$$

In practice, the reader cannot accurately collect all the tags in their interrogation region even if there is no reader collisions due to environment noise, multi-path, signal attenuation, and other factors. We use read rate, defined as the ratio of the number of correctly collected tags to the total number of tags in the interrogation region, to measure the feasibility of our approach. We also evaluate the efficiency of anti-reader-collision by using the total number of scheduling rounds.

# 5.2 Implementation Results

Based on our prototype system, we measure the throughput of Q-Adaptive and Season-I. Q-Adaptive is a variant of FSA and adopted by EPCglobal standards [5]. It is the most widely used anti-tag-collision protocol. From the results shown in Fig. 8, we observe that our approach is far more efficient than Q-Adaptive. According to our analysis in Section IV, the theoretical result of Season-I’s throughput is 0.36. We find that the throughput of Season-I is between 0.34 and 0.37 in 60% of the testing cases, which is very close to the theoretical result.

We investigate the impact of reader collisions by checking the read rate in an identification procedure. We deploy 60 passive tags and three Alien readers on PAMF, and then observe the differences between two scenarios without and with reader collision. For better visualization, we design a client tool to visually display the identified tags in threedimensions. In the interface, the boxes whose tags are identified are shown in highlight and the others displayed in semi-translucence. In the first scenario, we activate three readers in turn. The identification results of one test are shown in Fig.7-(a). The readers on the left, top, and right bars collect 34, 15, and 29 tags, respectively. We repeat the same identification test for 50 times, and observe that the average read rates of the left and right readers are 0.75 and 0.66, respectively, while that of the top reader is only around 0.26. The top reader has such a low read rate is that the tags are attached to the left vertical sides of boxes, which has poor signal transmissions to the top reader. In the second scenario, we concurrently activate three readers and show the results of one test in Fig. 7-(b). Due to the reader collisions, the readers on the left, top, and right bars only collect 13, 6, and 8 tags, respectively. We also repeat the second scenario for 50 times. The results show that the average read rates of the left, top and right readers drop by 42%, 14%, and 45% on average. Our experiments indicate that the reader collision is indeed a very serious problem in practical RFID applications. Note that the C1G2 standard specifies that the RFID reader uses frequency hopping to avoid interference across readers when identifying tags in the same area. The reader we use hops between 50 channels in the 902MHz ∼ 928MHz ISM band. FCC regulations specify that a reader can have a maximum channel dwell time of 0.4 seconds in any ten second period to reduce interference in a channel [5]. Therefore, we cannot exactly make these readers colliding all the time. The exhibited impact of reader collision is only based on a statistical result. That is why some tags are still identified in the second experiment.

For testing joint identification, we employ a NI PXI-1044 testing tool with a PXI 5600 receiver as the passive reader. We also employ an Alien reader as the active reader. The tags are put in the middle between these two readers, with a distance 2.5m in between. The CDF of read rate of our passive reader is shown in Fig. 9. We can observe that the passive reader achieves a read rate of 0.73 in 60% of testing cases. The average value of its read rates is up to 0.71, which is nearly as good as that in the single-reader deploying scenario.

![](images/9f28a3b0ccd0dd8aefb305f6f5be5ee448dd32e7061bdcd13fc47cea5e1c9f1f.jpg)



Fig. 12. Scheduling rounds

![](images/765a5015eef26112ed37d3a4f152286206d7df61f90ed421ab84738758e7e88d.jpg)



Fig. 13. Throughput

![](images/b2f5f4b1ebd8e9085765c827b4408110b970b61ab71f2304caf23f81c01f09d3.jpg)



Fig. 14. Delays

# 5.3 Simulation Results

Identifying tags without reader collisions. We first simulate the environment of deploying a single reader to show the performance of identifying non-contentious tags. We compare Season-I with prior anti-tag-collision protocols with number of tags ranging from 1 to 1000. The identification time of three types of protocols, FSA based approach, Balanced Tree (BT) based approach, and Season, is shown in Fig.10. From the figure, we observe that the identification time of each protocol is proportional to number of tags. Among them, Season-I is much faster than both FSA and BT based approaches. Especially when the number of tag is above 100, Season-I has 30.6% and 42.2% time saving on average than BT and FSA, respectively. Furthermore, we also evaluate the throughput of these anti-tag-protocols and report the result in Fig.11. The results show that Season-I is the best anti-tag collision protocol whose maximum throughput is up to 0.4 and 60% of the cases has a throughput higher than 0.37. However, the throughput of FSA and BT is typically lower than 0.29. We also observe that BT is the most stable protocol, 90% of the cases keeps around 0.25 to 0.26.

Identifying tags with reader collisions. In the experiment, we simulate multi-reader environments to show the performance of Season under reader-collision. We compare Season with DCS and Colorwave via the number scheduling rounds needed for anti-reader-collision. DC-S and Colorwave employ the graph coloring method to schedule the readers. The results are shown in Fig.12. Season has the least number all the time compared with other anti-reader-collision protocols in the five scenarios. For example, Season only needs 4 scheduling rounds in the ‘warehouse’ scenario where the maximum degree of RCG is 4. However, DCS and Colorwave require 27 and 28 rounds due to the high probability of collision among their randomly chosen colors in RCG. DCS is better than Colorwave since DCS knows the maximum degree of RCG in advance and this information helps DCS to reduce the probability of color collision.

Furthermore, we measure the overall throughput of three protocols in the five scenarios and show the results in Fig.13. The overall throughput of Season is much higher than other two approaches due to the concurrent identification of non-contentious tags and joint identification of contentious tags. For example, the overall throughput of Season in ‘sparse’ scenario is 8.5, meaning 8.5 tags can be identified per slot on average. Finally, we measure the average delay of the three protocols and plot the results in Fig.14. In all the five scenarios, the average delay of Season is no more than 300 time slots, which can be negligible in practice. It also indicates that Season can be applied in mobile environments to identify high-speed tags (up to 9 m/s). On the other hand, DCS and Colorwave suffer from a longer delay, i.e., the longest delay is up to 62,352 time slots, in which some tags have to wait for at least 2 minutes before the reader collects them.

# 6 RELATED WORKS

In the literature, RFID anti-tag-collision mechanisms comprise of two categories, Framed Slotted ALOHA (FSA) based [5], [23]–[25] and Binary Tree (BT)based algorithms [26], [27]. The well known RFID organization, EPC Global, adopts a variation of FSA, ‘Q-Adaptive’ in its protocol family, EPC Gen2 [5], which adaptively tunes the frame length according to the type of last slot. Lee et al. [23] find that the maximum identification throughput can be achieved within a reader’s scanning field when the size of detecting frame equals to the number of tags. Sheng et al. [24] focus on the fundamental problems of continuously scanning in RFID systems. Xie et al. [25] involves the practical conditions in the design of probabilistic model of RFID systems. The binary tree based algorithm has been adopted by another well-known RFID protocol family, ISO 18000- 6 [26]. When designing tree based algorithms, researchers usually organize the tags in a binary tree according to their IDs and identify the tags by using the tree based search technique. Myung and Lee [27] propose an adaptive binary splitting (ABS) protocol to reduce collisions and efficiently identify tags based on previous result. Prtal et al. [32] evaluate a set of well-known RFID anti-tag-collision protocols and propose a new collision resolution protocol, BSTSA, which combines the strengths of bote tree-based and aloha-based protocols.

For avoiding reader collisions, Colorwave [7] is one of pioneer works. Colorwave tries to color the readers randomly in a RCG such that each pair of interfering readers can gain different colors. In [29], the authors suggest k-coloring of the interference graph, where the k is the number of available channels. Recently, EPCGlobal [5] proposes a dense reading mode, in which the tag responses happen in different channels to avoid collisions. In [30], the authors design a Q-learning process to arrange channels and allocate time slots for readers with a help of a training process. In [8], the author proposes a tag-access-scheduling protocol (EGA) based on STDMA. Tang, et al. [9] study a challenging problem of scheduling the activation of the readers without collision such that the system can wok in a stable way in the long term.

To speed-up the identification procedure, Floerkemeier [31] suggests estimating the cardinality of tags based on the number of idle slots in the current frame. Kodialam and Nandagopal [13] propose two estimation algorithms, Unified Simple Estimator (USE) and Unified Probabilistic Estimator (UPE) with three estimators. They also analyze the operating range and accuracy of USE and UPE. Bu [33] et al. studied an efficient solution against misplacement errors which is a major concern in production economics. Unlike the preview work which focuses on data processing, their method studies the misplace problem from the communication protocol design perspective. Their distributed solution enables each reader to independently detect misplaced tags. Liu [34] et al., studies the integration of RFID and wireless sensor networks to expend their overall functionality and capacity. Zhou [35] et al. propose a efficient multidimensional fusion algorithm on IoT data.

# 7 CONCLUSION

Anti-collision is a crucial task in RFID systems. In this paper, we propose an anti-collision protocol stack, Season, to improve the identification efficiency for densely deployed RFID systems. In our future work, we plan to extend our scheme to mobile reader environments [36] and explore more practical issues in the RFID identification procedure, such as the asynchronization, background noise, and the like.

# ACKNOWLEDGEMENT

This work is supported in part by China 973 Program under Grant 2011CB302705, Grant No. 61373175, and the Fundamental Research Funds for the Central Universities of China under Project No. 2012jdgz02 (Xian Jiaotong University).

# REFERENCES

[1] B. Sheng, C. C. Tan, Q. Li, and W. Mao, “Finding Popular Categories for RFID Tags,” in Proceedings of MobiHoc, 2008.   
[2] T. Kriplean, E. Welbourne, N. Khoussainova, V. Rastogi, M. Balazinska, G. Borriello, T. Kohno, and D. Suciu, “Physical Access Control for Captured RFID Data,” Pervasive Computing, 2007.   
[3] C. C. Tan, S. Bo, and L. Qun, “How to Monitor for Missing RFID tags,” in Proceedings of ICDCS, 2008.   
[4] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “LANDMARC: Indoor Location Sensing Using Active RFID,” in Proceedings of IEEE PerCom, 2003.

[5] “EPCglobal RFID Class-1 Gen2 UHF RFID Protocol,” Standard, 2005.   
[6] D. W. Engels and S. E. Sarma, “The Reader Collision Problem,” in Proceedings of IEEE SMC, 2002.   
[7] J. Waldrop, D. W. Engels, and S. E. Sarma, “Colorwave: An Anticollision Algorithm for the ReaderCcollision Problem,” in Proceedings of IEEE ICC, 2003.   
[8] Z. Zhou, H. Gupta, S. R. Das, and X. Zhu, “Slotted Scheduled Tag Access in Multi-Reader RFID Systems,” in Proceedings of ICNP, 2007.   
[9] S. Tang, J. Yuan, X. Y. Li, G. Chen, Y. Liu, and J. Zhao, “RASPberry: A Stable Reader Activation Scheduling Protocol in Multi-reader RFID Systems,” in Proceedings of ICNP, 2009.   
[10] L. S. Leong, N. M. Ng, A. R. Grasso, and P. H. Cole, “Synchronization of RFID Readers for Dense RFID Reader Environments,” in Proceedings of SAINT Workshops 2006.   
[11] J. F. Kuros and K. W. Ross, Computer Networking: A Top-Down Approach Featuring the Internet, 2005.   
[12] F. C. Schoute, “Dynamic Frame Length ALOHA,” IEEE Transactions on Communications, 1983.   
[13] M. Kodialam and T. Nandagopal, “Fast and Reliable Estimation Schemes in RFID Systems,” in Proceedings of MobiCom, 2006.   
[14] C. Qian, H. Ngan, and Y. Liu, “Cardinality Estimation for Largescale RFID Systems,” in Proceedings of PerCom, 2008.   
[15] T. Li, S. Wu, S. Chen, and M. Yang “Energy Efficient Algorithms for the RFID Estimation Problem,” in Proceedings of INFOCOM, 2010.   
[16] H. Han,B. Sheng, C. Tan, Q. Li, W. Mao and S. Lu, “Counting RFID Tags Efficiently and Anonymously,” in Proceedings of INFOCOM, 2010.   
[17] S. Basagni, “Finding a Maximal Weighted Independent Set in Wireless Networks,” Telecommunication Systems, 2001.   
[18] S. Vasudevan, D. Towsley, D. Goeckel, and R. Khalili, “Neighbor Discovery in Wireless Networks and the Coupon Collector’s Problem,” in Proceedings of IEEE MobiCom, 2009.   
[19] R. Motwani and P. Raghavan, Randomized Algorithms, 1996.   
[20] D. Khoshnevisan, Probability, 2007.   
[21] E. Welbourne, K. Koscher, E. Soroush, M. Balazinska, and G. Borriello, “Longitudinal Study of a Building-scale RFID Ecosystem,” in Proceedings of ACM MobiSys, 2009.   
[22] http://rfid.cs.washington.edu/deployment/   
[23] S. R. Lee, S. D. Joo, and C. W. Lee, “An Enhanced Dynamic Framed Slotted ALOHA Algorithm For RFID Tag Identification,” in Proceedings of MobiQuitous, 2005.   
[24] B. Sheng, Q. Li, and W. Mao, “Efficient Continuous Scanning in RFID Systems,” in Proceedings of INFOCOM, 2009.   
[25] L. Xie, B. Sheng, C. C. Tan, H. Han, Q. Li, and D. Chen, “Efficient Tag Identification in Mobile RFID Systems,” in Proceedings of INFOCOM, 2009.   
[26] “RFID For Item Management Air Interface. Part-6,” ISO 18000-6 Standard, 2003.   
[27] J. Myung and W. Lee, “Adaptive Binary Splitting: A RFID Tag Collision Arbitration Protocol for Tag Identification,” Mobile Networks and Applications, 2006.   
[28] www.impinj.com/   
[29] H. Gupta, Z. Zhou, S. R. Das, and Q. Gu, “Connected Sensor Cover: Self-organization of Sensor Networks for Efficient Query Execution,” IEEE/ACM Transaction on Networking, 2006.   
[30] J. Ho, D. W. Engels, and S. E. Sarma, “HiQ: A Hierarchical Q-learning Algorithm to Solve the Reader Collision Problem,” in Proceedings of IEEE SAINT Workshops 2006.   
[31] C. Floerkemeier and E. Zurich, ”Transmission Control Scheme for Fast RFID Object Identification,” in Proceedings of PerCom Workshop, 2006.   
[32] T. F. L. Porta, G. Maselli, and C. Petrioli, “Anticollision Protocols for Single-Reader RFID Systems: Temporal Analysis and Optimization,” IEEE TMC, 2011.   
[33] K. Bu, B. Xiao, Q. Xiao, and S. Chen, “Efficient misplaced-tag pinpointing in large RFID systems”, IEEE TPDS, 2012.   
[34] H. Liu, M. Bolic, A. Nayak, and I. Stojmenovic, “Taxonomy and Challenges of Integration of RFID and Wireless Sensor Networks,” IEEE Network, 2008   
[35] J. Zhou, L. Hu, F. Wang, H. Lu, and K. Zhao, “An Efficient Multidimensional Fusion Algorithm for IoT Data Based on Partitioning,” Tsinghua Science and Technology, 2013.   
[36] X. Wang, X. Lin, Q. Wang, and W. Luan, “Mobility Increases the Connectivity of Wireless Networks,” IEEE/ACM Transactions on Networking, 2012

![](images/965f53609d1f75ee22cce0af5f1abf29895a590fa04c1725cbca736f3e1b3a43.jpg)



Lei Yang received the BS degree in computer science and engineering fqrom Xi’an Jiaotong University in 2004. He is currently a Ph.D. Student at the Xi’an Jiaotong University. His research interests include RFID, pervasive computing, and network security. He is a member of the IEEE Computer Society, and the ACM.

![](images/507193a3994eb2391b8a965d596e150dc651de35622d118508686ce8dfbbd54e.jpg)



Yong Qi received his Ph.D. degree in computer science and technology fromq Xi’an Jiaotong University in 2001. He is a full professor in the Depaqrtment of Computer Science and Technology of Xin Jiaotong Universitqy. His research interests include sensor networks, operating system, distributed middlewqare, and services computing. He is a member of IEEE.

![](images/93693cab1d69cef7f2200c64fdce321b6642cd963cdb6248020b3ed17af3eda6.jpg)



Jinsong Han received the PhD degree in computer science and engineering from the Hong Kong University of Science and Technology in 2007. He is currently an associate professor at the Xi’an Jiaotong University. His research interests include peer-to-peer computing, anonymity, pervasive computing, network security, and high speed networking. He is a member of the IEEE Computer Society, and the ACM.

![](images/0c11a6ad5b03d56c4928b048ae7116774686e43f9d709f82ccfac2c715abd239.jpg)



Cheng Wang received his PhD degree in Department of Computer Science at Tongji University in 2011. His research interests include wireless communications and networking,mobile social networks, and mobile cloud computing.

![](images/0109b633e7bf17a049bc52e6519a60460eae5f84abb7e406fffd924ef5e4e4e0.jpg)



Yunhao Liu received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. Being a member of Tsinghua National Lab for Information Science and Technology, he holds Tsinghua EMC Chair Professorship. Yunhao is the Director of Key Laboratory for Information System Security, Ministry of Education, and Professor at

School of Software, Tsinghua University. He is also a faculty member at the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include pervasive computing, peer-to-peer computing, and sensor networks.