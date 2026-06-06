# SHAD: Privacy-friendly Shared Activity Detection and Data Sharing

Feng Han, Lan Zhang, Xuanke You, Guangjing Wang, Xiang-Yang Li

Department of Computer Science and Technology, University of Science and Technology of China

Abstract—Nowadays, there is a growing demand for sharing multimedia data among participants in the same activity. With existing social applications, users need to conduct friending and data sharing operations manually, which is troublesome due to changing attendees and highly diverse data content of different activities. To tackle this issue, in this work we propose a novel system SHAD to achieve privacy-friendly shared activity detection and multimedia data auto-sharing based on users' historical multimodal data. Facing noisy, incomplete and asynchronous data, as well as inaccurate recognition results of machine learning models, we design an algorithm to aggregate multimodal data relevant to the same activity and propose an activity-semantic graph to comprehensively characterize each activity by fusing knowledge of multimodal data. Based on the activity-semantic graph, the privacy-preserving shared activity detection and data sharing method is designed, which protects both raw data and semantic information of data. We implemented our system and conducted comprehensive evaluations with real-life multimodal data (including photos and motion sensor data). The results show the efficacy of our system. We can achieve 94.9% precision and 91.5% recall for shared activity detection.

# I. INTRODUCTION

Massive multimodal data, e.g., photos, videos, audio data, and other sensor data, are generated during various social/group activities like conferences, parties, and sports games. There is a common need for participants in the same activity to establish social connections and share data about this activity. For example, people may share photos and videos after a party or share motion sensor data after playing tennis for further professional sports analysis $[1]$ . Nowadays, there are a series of applications designed for social connection management and data sharing, e.g., Instagram, Facebook and Wechat, however, the friending and sharing operations still need to be conducted manually by users.

Due to the changing attendees and diverse multimodal content of social activities, it is quite cumbersome to manage user groups of different activities and determine which part of the data to share for each activity. In this work, we aim to design a system which is able to automatically detect users' shared activities, manage multimodal data and social connections by activities, and share the activity relevant data in a privacy-preserving way. To achieve this non-trivial goal, we need to answer the following challenging questions:

1) Which parts of multimodal data are from the same activity? For each user, multimodal data is generated during different activities from time to time. Segmenting data by activities is a well-known challenging task for continuous data such as the motion sensor data and videos. For discrete data like photos, it is still difficult to determine which data are from the same activity due to the irregular sample frequency and highly diverse content. Matching cross-modal data, e.g., matching photos and pieces of motion sensor data from the same activity, is even harder, since data of different modalities capture different features of an activity. Moreover, the data is noisy (e.g., there may be some irrelevant photos) and incomplete.

2) Who attended the same activity together? Given a collection of users, we need to detect their shared activities based on their historical multimodal data, e.g., photos, videos and motion sensor data. A straight-forward idea is to use machine learning models to recognize activities $[2]$ and attendees $[3]$ . However, the ability of models for various modalities differs. Some activities, especially complex activities like a party, are difficult to recognize in some modality. Besides, inaccurate recognition results of different modalities may yield conflicting interpretations of the same activity. As an example, an activity may be recognized as playing tennis by using photo, but be considered as playing badminton by using motion sensor data. Last but not least, the shared activity detecting process should not incur heavy communication or computation cost for mobile devices. Hence, some computation-hungry models cannot be adopted.

3) How to protect users' privacy during the detection and data sharing process? Considering rich personal information in multimodal data, not only the raw data but also the semantic information of the data and interactions among users should be well protected from unauthorized parties.

Facing the aforementioned challenges, we propose a system called SHAD to automatically detect users who have attended the same activity together based on their historical data, then select and share data relevant to this activity. The whole process is conducted in a privacy-preserving way. Our design greatly facilitates social activity relevant friendship and multimodal data management as well as data sharing. The contributions of this work can be summarized as follows:

\- To the best of our knowledge, SHAD is the first work addressing shared activity detection based on multimodal historical data. We design an algorithm to aggregate multimodal data relevant to the same activity by measuring both semantic and temporal proximity among data pieces. Meanwhile, our algorithm solves the conflicting interpretations of data of different modalities, so as to detect incorrect semantic tags to further improve the activity recognition accuracy or irrelevant data pieces to prevent privacy leakage. (§III) By fusing knowledge of multimodal data, we propose an activity-semantic graph to comprehensively characterize the semantic and temporal information of each activity. It provides a unified representation of different types of activities, which is independent of the modality of the data, and enables shared activity detection by calculating similarity between activity-semantic graphs. (§IV)

- To respect users' privacy, we design a secure shared activity detection protocol based on the activity-semantic graph and Private Set Intersection (PSI). During the whole process, our system protects both raw data and semantic information of data, and achieves secure communication and interaction. (§V)   
- We implemented our system and conducted comprehensive evaluations with real-life multimodal data (including photos and motion sensor data). The results show the efficacy of our system. For the shared activity detection, the average precision and recall are 94.9% and 91.5% for photo sharing, 99.9% and 98.3% for sensor data sharing. The tags of activities become more accurate by removing conflicting tags when using multimodal data. (§VI)

# II. SYSTEM OVERVIEW

# A. Motivation Scenario

When several users have participated in the same activity, which is defined as their shared activity, they may want to share the activity-relevant multimedia data and maintain the social relationships with each other. Fig. 1 illustrates an example scenario. Two users have attended a table tennis match together. They may add each other as friends of table tennis and share photos and motion sensor data for further professional analysis. During the friending and sharing process, there are two roles: Requester and Sender. The requester wants to manage social connections by finding users who have shared activities with him/her, and request activity-relevant data from them. The sender is willing to share the data relevant to the shared activities with other participants. Both the sender and the requester require the privacy guarantee that only the information relevant to the shared activity will be disclosed to only the participants of this activity.

In order to make the problem setting more general, we assume that:

(1) Data has no other metadata information (e.g. GPS) except the generation time;   
(2) Users are semi-honest-but-curious, i.e., they follow the protocol and do not forge the data, but they may want to get information from others beyond their shared activities.

# B. Design Principles

In this work, we aim to achieve privacy-preserving shared activity detection and data sharing given several users' multimodal historical data. The following requirements should be considered in our system design:

1) Accuracy: The system should detect shared activities accurately. Detection errors may cause a privacy disclosure when a non-shared activity is identified as a shared

![](images/b1bfb01d7b774c37e66735c72cec3e8a44ce35f245eec075ed504073c2ce8d8a.jpg)



Fig. 1: Example scenario of SHAD.

activity, or a bad user experience when users cannot correctly tag friends and obtain desired data.

2) Privacy: During the detection and sharing process between requester and sender, the system should protect users' raw data and semantic information of each activity from anyone who didn't participate in this activity, and protect users' interactions from eavesdropping.   
3) Efficiency: For a good user experience, the system should not cause large computation and communication cost and long response time.

# C. Basic Idea and System Model

As shown in Fig. 2, there are two key steps of SHAD: 1) multimodal data aggregation: each user needs to aggregate his/her own multimodal data pieces from the same activity; 2) shared activity detection: based on the data of each activity, two users need to determine their shared activities in a privacy-preserving way. The most challenging issue for data aggregation is how to determine the boundaries of different activities and match data pieces of different modalities. To address this issue, our core idea is to extract semantic tags from all data pieces and convert the multimodal data aggregation task to a data clustering task based on semantic and temporal proximity among data pieces. During the clustering process, outliers can also be detected, which are mainly caused by incorrect semantic tags or irrelevancy to the detected activities (e.g., a screen shot during a party). Based on the aggregation results, we design an activity-semantic graph to represent each activity by assembling its relevant semantic tags and temporal information of multimodal data. Then the shared activity detection is carried out by a our secure activity-semantic graphs matching protocol. With the careful design of the activity-semantic graph, we are able to reduce the computation and communication overhead of the secure computation protocol.

Distance among semantic tags. To realize the multimodal data clustering, we need to quantify the distance among semantic tags, which is not trivial. First, for data of different modalities, a set of machine learning models can be utilized to produce tags, which however may have diverse semantic levels (e.g., running and sports) or cover different semantic domains (e.g., playground and running). Second, some tags may be polysemes which cause ambiguity in the data aggregation. To tackle these issues, we introduce tags' semantic level and subordinate relations between them. A tag with a more general meaning has a higher semantic level. A subordinate relation is defined as <hyponymy → hyperonymy>. For example, running → sports which means sports has a higher semantic level and is the "parent" of running. Two tags with one common "parent" are "siblings". Let the set of all semantic tags be V. E refers to the set of edges representing subordinate relations among them. A mapping Sim: $(\mathcal{V} \times \mathcal{V}) \to (0, 1]$ yields the semantic similarity between two semantic tags. We adopt the subordinate relation and path similarity defined in WordNet [4], which is a well-known large lexical database of English, to construct E and calculate Sim.

![](images/f6a6737fca6248cea973fe63af2a5a18d84db493fa04ef56b4557c1aea650326.jpg)



Fig. 2: Idea and architecture of SHAD. The data aggregation(§III) and activity-semantic graph construction(§IV) are local operations. The shared activity detection and data transmission(§V) require user interaction.

<table><tr><td> $\mathcal{V}$ </td><td>the set of all semantic tags</td></tr><tr><td> $\mathcal{E}$ </td><td>the set of all edges between tags</td></tr><tr><td> $\mathcal{A}$ </td><td>the set of all activities</td></tr><tr><td> $\mathcal{D}$ </td><td>the set of all data pieces</td></tr><tr><td>Sim</td><td>similarity function of two semantic tags</td></tr><tr><td>F</td><td>semantic tag extraction function</td></tr><tr><td>A</td><td>data aggregation function</td></tr><tr><td>P(d)</td><td>the set of corresponding points of the data piece d</td></tr><tr><td>p=(v,ts,te)</td><td>a data point with tag v and duration (ts,te)</td></tr><tr><td>O(p)</td><td>the data piece to which point p belongs</td></tr><tr><td>Dis(pi,pj)</td><td>distance between two points pi,pj</td></tr><tr><td>C(p)</td><td>the predicted category of point p</td></tr><tr><td>VC</td><td>the conflict set</td></tr><tr><td>Ga</td><td>activity-semantic graph of an activity a</td></tr><tr><td> $\mathcal{G}_{\mathcal{A}_r}(\mathcal{G}_{\mathcal{A}_s})$ </td><td>the set of graphs of requester (sender)</td></tr><tr><td>I</td><td>the importance factor</td></tr><tr><td>ε</td><td>the weakening factor</td></tr><tr><td>S(Gi;Gj)</td><td>the similarity of Gi to Gj</td></tr><tr><td>Ga.DT</td><td>the discrete-time point set of graph Ga</td></tr></table>

TABLE I: Notation table

Semantic representation of activities. Let the set of all activities be A, and the set of all data pieces be D. Each data piece $d_{i} \in D$ has two attributes $t_{s}$ and $t_{e}$ , representing its start time and end time. $F : D \to \{V | V \subseteq V\}$ is the semantic tag extraction function, which maps each data piece to a set of tags. $A : D \to A$ is the data aggregation function, which organizes data pieces of the same activity together. The activity-semantic graph is designed to represent the semantic and temporal information of an activity.

Definition 1 (Activity-Semantic Graph):

The activity-semantic graph of an activity $a \in A$ is $G_{a} = \{V, E, (t_{s}, t_{e})\}$ , where the node set $V \subseteq V$ , the edge set $E \subseteq E$ , and $(t_{s}, t_{e})$ represents the time interval of this activity. Each node $v_{j} \in V$ is a tag of this activity, and has an attribute $v_{j}$ .weight indicating its importance.

# D. Architecture and Typical Workflow

The system architecture is shown in Fig. 2.

1) Users' local operations: Each user locally applies function $F$ to generate tags for all his/her data pieces, and then aggregates his/her own multimodal data pieces from the same activity with function $A$ . During the aggregation, SHAD conducts outlier detection to find incorrect tags or irrelevant data, and also solves the conflicting interpretations of multimodal data. The detail is presented in §III. Finally, each user locally generates activity-semantic graph for each activity.   
2) Secure shared activity detection: A requester communicates with a sender following our privacy-preserving activity-semantic graph matching protocol to detect their shared activities. If they have a shared activity, they can secretly establish a connection marked by this activity. Then, the sender can send the encrypted data of shared activities to the requester if the requester needs. The detail is presented in §V.

# III. SEMANTIC TAG EXTRACTION AND DATA AGGREGATION

# A. Semantic Tag Extraction

We extract semantic information from multimodal data to enable the cross-modality data comparison. In our prototype system, we take two common data modalities (photos and motion sensor data) as an example. Deep learning provides a powerful set of techniques to extract various information from photos, e.g., object detection [5] and scene recognition [6]. There are also lots of attempts for activity recognition based on motion sensor data using various machine learning methods, such as SVM [7] and CNN with recurrent units [8]. Since the focus of this work is not on label extraction, we adopt the state-of-the-art models as black boxes to produce labels for multimodal data pieces. Please see §VI for model details of label extraction. Obtaining labels of each piece of data, we use the tool pyWSD [9] to convert those labels into semantic tags so that each tag has a specific meaning, i.e., not a polyseme. As an example, the label badminton extracted from the sensor data is converted to the tag badminton.n.01 $^{1}$ .

# B. Data Aggregation and Outlier Tags Detection

In this section, we present the algorithm to aggregate multimodal data pieces from the same activity, which is the function A defined in §II.C. We first group single modal data pieces based on their temporal and semantic proximity, and then we aggregate the different modal data of the same activity. One challenge here is that the semantic tags extracted from data may be incorrect, and the tags extracted from different modal data may conflict with each other, which may reduce the accuracy of data aggregation and shared activity detection. By considering those incorrect tags or tags of irrelevant activities as outliers, we design our algorithm to filter such tags as many as possible.

1) Single modal data aggregation: Intuitively, data relevant to the same activity should be proximate in both temporal and semantic domains, and one tag which is semantically disparate from the previous and subsequent tags is more likely to be an outlier. Based on the intuition, we design the single modal data aggregation algorithm based on DBSCAN [10], because it achieves good performance in the presence of noisy data points.

Firstly, we treat each tag of each data piece as a separate point. For example, given one data piece $d$ with a duration $(t_s, t_e)$ and two tags $F(d) = \{v_1, v_2\}$ , the set of corresponding points is $P(d) = \{p_1, p_2\}$ , where $p_1 = (v_1, t_s, t_e), p_2 = (v_2, t_s, t_e)$ . We record the data piece to which the point $p$ belongs as $O(p)$ . We carefully define the distance between points to make two points stay closer when their semantic meanings are similar and their generation time are close.

Definition 2 (Distance Between Points): For two points $p_i = (v_i, t_{s_i}, t_{e_i})$ , $p_j = (v_j, t_{s_j}, t_{e_j})$ , we define the distance between points as

$$
D i s (p _ {i}, p _ {j}) = \left\{ \begin{array}{c l} 1 - \sqrt {f (\triangle t) \times S   i m (v _ {i} , v _ {j})}, & O (p _ {i}) \neq O (p _ {j}) \\ 1, & O (p _ {i}) = O (p _ {j}) \end{array} \right.
$$

where

$$
\Delta t = \left\{ \begin{array}{c} 0, \quad (t _ {e _ {i}} \geq t _ {s _ {j}} \& \& t _ {s _ {i}} \leq t _ {e _ {j}}) \\ \min (| t _ {s _ {i}} - t _ {e _ {j}} |, | t _ {s _ {j}} - t _ {e _ {i}} |), \quad o t h e r w i s e \end{array} \right.
$$

$$
f (\triangle t) = \left\{ \begin{array}{l l} \sin (\frac {\pi}{2 (\triangle t + 1)}), & \triangle t <   1 d a y \\ 0. & o t h e r w i s e \end{array} \right.
$$

$\triangle t$ represents the disparity of generation time between two data pieces, and it is 0 when two generation duration overlap. $Dis(p_i, p_j) \in [0,1]$ , and the higher the similarity between two points, the smaller the distance is. Specially, we hope that the point whose corresponding tag is incorrect will be recognized as an outlier. If the distance between the points from same data piece is small, they may converge directly into one category, so we define the distance between points from the same data piece as 1. Given the different sampling rates of different modal data, we measure $\triangle t$ in hours for photos, and in minutes for sensor data. Then we run DBSCAN on the set of points $\bigcup_{d \in D} P(d)$ . $C(p)$ represents the predicted category of a point $p$ . When $p$ is an outlier according to DBSCAN, $C(p) = -1$ . Then the tags of outliers may be incorrect or irrelevant.

Secondly, we aggregate data pieces of the same activity as described by Algorithm 1. The principle of aggregation is that two data pieces $d_1$ and $d_2$ belong to one activity if $\exists p_1 \in P(d_1)$ , $\exists p_2 \in P(d_2) \to C(p_1) = C(p_2)$ . The total time span

Algorithm 1 Single modal data aggregation   
function AGGREGATE1(C) //C is point clustering result
Initialize: $A = \{d\}$ for $d \in D$ , flag = 0
//D is the set of all data pieces
while flag == 0 do //until no activity need to merge
    flag = 1
    for $a_i, a_j \in A$ do
    if $\text{JUDGE}(a_i, a_j)$ then //two activities need to merge
    merge $a_i$ and $a_j$ ; flag = 0 $A_f, D_1, D_2, D_3 = \text{TIMEADJUST}(A)$ return $A_f$ // $A_f$ is the set of activities.

function JUDGE( $a_i, a_j$ ) //whether two activities need to merge.
    for $d_1 \in a_i$ do
    for $d_2 \in a_j$ do
    if $\exists p_1 \in P(d_1), p_2 \in P(d_2), C(p_1) = C(p_2)$ then
    return True
    return False

function TIMEADJUST(A)
    for $a \in A$ do $a.t_s = \min(d.t_s \text{ for } d \in a); a.t_s = \max(d.t_e \text{ for } d \in a)$ $A_1 = \{a \in A \text{ if } |a| == 1\}$ $A_2 = \{a \in A \text{ if } |a| > 1\}$ $D_1 = \bigcup_{a \in A_2} a; D_2 = \emptyset$ for $a_1 \in A_1$ do
    for $a_2 \in A_2$ do
    if ( $a_1.t_e \geq a_2.t_s \&\&a_1.t_s \leq a_2.t_e$ ) then $D_2 = D_2 \cup a_1; a_2 = a_1 \cup a_2; A_1.pop(a_1);$ Break; $D_3 = \bigcup_{a \in A_1} a;$ if $A_1 \neq \emptyset$ then
    merge activities in $A_1$ within a one-hour interval;
    add those new activity into $A_2$ return $A_2, D_1, D_2, D_3$

covering all data pieces in one activity is used as the duration of this activity. After that, if all the points of one data piece are outliers, this data piece itself makes one activity. We record the set of such activities as $\mathcal{A}_1$ , the set of other activity as $\mathcal{A}_2$ , and $D_1 = \bigcup_{a \in \mathcal{A}_2} a$ . Then we merge each activity $a_1 \in \mathcal{A}_1$ with the activity $a_2 \in \mathcal{A}_2$ if their time intervals overlap. We record the set of data pieces of the activities that was successfully merged in $\mathcal{A}_1$ as $D_2$ . If there still exists activity in $\mathcal{A}_1$ , we merge the activities in $\mathcal{A}_1$ within a one-hour interval into one new activity. We record the set of data pieces of those new activities as $D_3$ .

Thirdly, we filter outlier tags. If an outlier point belongs to one data piece $d \in D_{1} \cup D_{2}$ , its tag is more likely incorrect, then we remove it from $F(d)$ . If an outlier point belongs to one data piece $d \in D_{3}$ , there is not enough context information for us to make a conclusion, then we keep it.

Through these three steps, we aggregate single modal data pieces and filter out outlier tags. The better clustering of points will bring better data aggregation. The performance of data aggregation is shown in §VI.

2) Multi-modal data aggregation and conflict resolution: The principle of multi-modal data aggregation is that two activities of different modality are the same activity if they temporally overlap, and they will be merged into one activity.

Then we solve the conflicts between tags.

In our system, sensor data produce tags reflecting users' motion state, and photos produce visual tags. Since it's unlikely for a person to conduct two motions at the same time, we define all the hyponymy tags of sport.n.01 and game.n.01 as conflict set $V_{C}$ . Then we define the conflict between tags of the same activity as the existence of sibling relation between two tags in $V_{C}$ . For example, badminton.n.01 and tennis.n.01 have common parent court\_game.n.01 which means they are siblings, so two tags cannot appear simultaneously in the same activity. We solve the conflicts according to the reliability of the recognition model and the amount of evidence data. In our implementation, we set the reliability of the sensor data model and the photo model as $R_{S} = 0.94$ and $R_{N} = 0.85$ according to those two models' performance. For each conflict tag v, we multiply the reliability of the corresponding model by the amount of data pieces containing this tag as the confidence score of this tag. Then we compare the confidence scores of all siblings and keep the tag with the highest score. For example, tennis.n.01 extracted from 2 photos and badminton.n.01 extracted from 3 pieces of sensor data are conflicting in one activity. The score of tennis.n.01 is $0.85 \times 2 = 1.7$ , score of badminton.n.01 is $0.94 \times 3 = 2.82$ , so the tag tennis.n.01 is removed, which is correct according to the groudtruth.

# IV. ACTIVITY-SEMANTIC GRAPH

After semantic extraction and data aggregation, the multimodal data of the same activity are aggregated. In this section, we present the construction of the activity-semantic graph for each activity.

Basically, each node represents a semantic tag and the weight of the node should depend on the amount and modality of data pieces containing this tag. SHAD allows users to define the importance factor I for each data modality, which represents the reliability of the prediction results of this modality. We denote importance factors for sensor data and photo data as $I_{S}$ and $I_{P}$ , where $I_{S} + I_{P} = 1$ .

The graph $G_{a}$ of an activity $a$ is constructed as follows:

(1) We initialize $G_{a}.E = \emptyset$ , $G_{a}.V = \bigcup_{\{d|A(d) = a\}} F(d)$ . We query each tag $v \in G_{a}.V$ to obtain all hyponymy-hypernymy paths from $v$ to the root, e.g., entity.n.01 for nouns, in WordNet. We append all the paths into $G_{a}.E$ and all the nodes into $G_{a}.V$ .   
(2) For each node v without hyponymy nodes in graph $G_{a}$ , we call it "leaf node", and set its weight as the weighted sum of the amount of data from which v is extracted. For example, v is extracted from 2 photos and 3 pieces of sensor data, then v.weight = $2 \times I_{P} + 3 \times I_{S}$ .   
(3) For each non-leaf node $v$ , $v.\text{weight} = \epsilon \times \max \{u.\text{weight} | u \in h_v\}$ , where $h_v$ is the set of hyponymy nodes of $v$ .   
(4) $G_{a}.t_{s} = \min \{d.t_{s}|A(d) = a\}$ , $G_{a}.t_{e} = \max \{d.t_{e}|A(d) = a\}$ .

SHAD allows tags to have different weights because they contribute differently to describing activities. We set the weight of each non-leaf node as the maximum weight of its hyponymy nodes multiplied by a weakening factor $\epsilon$ ( $\epsilon=0.5$ in our experiment). The reason is that, the more important its hyponymy nodes, the non-leaf node is also more important for describing this activity. Besides, the tags with lower level can describe the most concrete details of the activity, and the tags which are extracted from more data are more important to sketch this activity. Fig. 3 illustrates one example of the graph.

Then we define the graph similarity.

Definition 3 (graph similarity): Give $G_{i} = \{V_{i}, E_{i}, (t_{s_{i}}, t_{e_{i}})\}$ , $G_{j} = \{V_{j}, E_{j}, (t_{s_{j}}, t_{e_{j}})\}$ , we define the similarity of $G_{i}$ to $G_{j}$ as

$$
S (G _ {i}; G _ {j}) = \left\{ \begin{array}{l l} \frac {\sum_ {v \in V _ {i} \cap V _ {j}} G _ {j} . v . w e i g h t}{\sum_ {v \in V _ {j}} G _ {j} . v . w e i g h t}, & f l a g = T r u e \\ 0, & f l a g = F a l s e \end{array} \right.
$$

where $flag = (t_{e_i} \geq t_{s_j} \& \& t_{s_i} \leq t_{e_j})$ , and the weight of nodes here are of $G_j$

If the time intervals of two graphs do not overlap, it means that the activities represented by the two graphs didn't happen at the same time, then the similarity is 0. The similarity is asymmetric to characterize that two graphs contain information of each other differently. For example, given a large graph $G_{1}$ and a small graph $G_{2}$ , $S(G_{1};G_{2})$ is usually larger than $S(G_{2};G_{1})$ to indicate that their common nodes covers a larger portion of $G_{2}.V$ . Our activity-semantic graph provides the unified representation of the activity and enables activity similarity calculation at the semantic level.

# V. SECURE SHARED ACTIVITIES DETECTION

# A. Secure Shared Activity Detection Protocol

The data relevant to the shared activity usually contain similar semantic information, e.g., same objects and scene. In this section, we first present how to detect shared activities by calculating the similarity between activity-semantic graphs and then introduce the secure protocol with privacy protection.

The requester and sender build their graphs of recent activities locally as aforementioned, which are $G_{A_{r}}=\{G_{a_{r}} \mid a_{r} \in A_{r}\}$ and $G_{A_{s}}=\{G_{a_{s}} \mid a_{s} \in A_{s}\}$ respectively. The requester determines whether the sender has participated in one of his/her historical activity $a_{r}$ by measuring similarity between $G_{a_{r}}$ and all activities in $G_{A_{s}}$ which coincide with $a_{r}$ . There could be more than one activity graphs temporally overlapping with $a_{r}$ , because in the local aggregation stage data pieces relevant to the same activity are not necessarily merged into one graph due to the inaccurate tags and discontinuous sampling. To deal with separated graphs of the same activity, the sender combine all his/her graphs temporally overlapping with $a_{r}$ to build a neighbor graph $G_{N_{a_{r}}^{s}}$ of $G_{a_{r}}$ . The requester computes the similarity $S(G_{N_{a_{r}}^{s}}; G_{a_{r}})$ and adds the sender as a friend from activity $a_{r}$ if the similarity exceeds his threshold. Also the sender can calculate the similarity by himself/herself to determine whether to send relevant data to the requester.

Definition 4 (Neighbor graph): Give two sets of activity graphs $\mathcal{G}_{\mathcal{A}_r} = \{G_{a_r}\mid a_r\in \mathcal{A}_r\}$ and $\mathcal{G}_{\mathcal{A}_s} = \{G_{a_s}\mid a_s\in \mathcal{A}_s\}$ , for one activity $a_{r}\in \mathcal{A}_{r}$ , The neighbor graph $G_{N_{a_r}^s}$ of $G_{a_r}$ is:

$$
G _ {N _ {a _ {r}} ^ {s}} = \{\bigcup_ {a _ {s} \in N _ {a _ {r}} ^ {s}} G _ {a _ {s}}. V, \bigcup_ {a _ {s} \in N _ {a _ {r}} ^ {s}} G _ {a _ {s}}. E, (\min _ {a _ {s} \in N _ {a _ {r}} ^ {s}} G _ {a _ {s}}. t _ {s}, \max _ {a _ {s} \in N _ {a _ {r}} ^ {s}} G _ {a _ {s}}. t _ {e}) \}
$$

where $N_{a_r}^s = \{a_s \mid a_s \in \mathcal{A}_s, (G_{a_r}.t_e \geq G_{a_s}.t_s\& \& G_{a_r}.t_s \leq$

![](images/82f8eb5176131c6c4c7167aecc6791fd0961ec241a54807b3061e2272190e5d7.jpg)



![](images/6d4590f5f04abc948e8a1e97927583d1d847193ffe4e8864e79ee7b09ee76a78.jpg)



![](images/15e196de66fed859cf1848292bd551b3c8e374a621624d12b80f897691bb56c8.jpg)



![](images/b1e4931d5880bbaf183c1ac327340f7cdeabf20846ee16659acf7d3098bdb638.jpg)  
Fig. 3: An example of semantic tags and activity-semantic graph.

$G_{a_s}.t_e) = True\}.$

During the detection process, both requester and sender can protect their raw data from unmatched users. However, they need to share the activity graphs with each other for the similarity calculation. Considering the semantic information in activity graphs, it is also necessary to protect the activity graphs as well as the similarity results. To fulfill our privacy requirement, we propose a secure shared activity detection protocol based on PSI. The key idea is to only allow a pair of users to learn the node intersection of their graphs so that they calculate the similarity based on the node intersection separately. PSI allows two parties who each holds a set of private items to compute their intersection in the way that only the intersection will be revealed to these two parties and any other party cannot learn anything about either the input or output of the computation. To facilitate the set intersection calculation, we conduct a time discretization operation to convert the time span of a graph to discrete time points. As an example, $G_{a}.(t_{s}, t_{e}) = (2018.06.01.20.31.31, 2018.06.01.22.31.31)$ is converted into $G_{a}.DT = \{2018060120, 2018060121, 2018060122\}$ . Specifically, the protocol works as follows:

(1) The requester converts the graph of $a_r$ into the set of (node, discrete-time) pairs, which is $\{(v,t)|v\in G_{a_r}.V,t\in G_{a_r}.DT\}$ , and launches a request for shared activity detection.   
(2) The sender constructs the set of all his/her graphs since he/she does not know the time interval of the requested activity. He/she generates the set $\bigcup_{a_s\in \mathcal{A}_s}\{(v,t)|v\in G_{a_s}.V,t\in G_{a_s}.DT\}$ .   
(3) The requester and sender run the PSI protocol [11], and get the intersection of two sets.   
(4) The requester approximates intersection is $G_{N_{a_r}^s}.V \cap G_r.V$ and computes $S(G_{N(a_r)};G_{a_r})$ using the weight of nodes in $G_{a_r}$ . If the similarity exceeded his/her threshold, the requester adds the sender as a friend from activity $a_r$ .   
(5) If the requester further requests activity relevant data from the sender, the sender would compute the approximate $S(G_{a_r};G_{a_s})$ for each activity $a_{s} \in \mathcal{A}_{r}$ , and compares those values with his/her threshold to decide whether an activity is a shared activity according to his/her standard. The sender can choose the data pieces from the shared activities, and encrypt data with AES-128 using the hash value of the PSI result as the key. Then he/she sends the encrypted data to the requester.

When the requester has multiple interested activities, he can run the protocol with a union set $\{(v,t)\}$ of those activities.

# B. Privacy Analysis

Our protocol achieves the desired privacy requirements guaranteed by the security of OT-based PSI [11] and AES-

128. After steps (1)-(4) of our protocol, both the requester and sender can only learn the intersection of their sets of (node, discrete-time) pairs, which means they can only learn the information they already know about the activity they have participated in. After steps (5), the requester can only obtain some data pieces relevant to the shared activities from the sender with the sender's permission.

For a third party, due to the security of PSI, no raw data or plain semantic tags can be learned during step (1)-(4). In step (5), the raw data pieces are encrypted by AES-128 and the key is the hash of the PSI result which is unknown to any third party. Because the large amount of all possible tags and the uncertainty of time span, the number of all possible (node, discrete-time) pairs is pretty large. The possible number of PSI results is 2 to the power of the number of all possible (node, discrete-time) pairs, so it is extremely large. So the difficulty of decrypting encrypted data by a third party is equivalent to the difficulty of exhaustive key search attack on AES-128.

As a conclusion, our protocol protects the raw data, semantic tags and temporal tags of each activity from any users who haven't participated in this activity. Besides, the raw data will only be shared with the owner's consent. The potential privacy, however, comes from the inaccurate shared activity detection, which depends on both accuracy of semantic tags and user defined thresholds. If a non-shared activity is detected as a shared activity, sender's data could be unintendedly shared to the requester. We will analyze the risk of data leakage in §VI.

# VI. IMPLEMENTATION AND EVALUATION

# A. Data Collection

Photos: We collected 8811 photos from 19 volunteers. The social relationships between volunteers include colleagues, family members and roommates. 17 pairs of volunteers had shared activities. Those photos were generated in their shared or non-shared social activities such as sports games, tourism, party, and academic conferences. The time span of the photo set is from 2016.12 to 2018.07. The photo owner provided one tag for each of his/her photos to indicate the corresponding activity.

Sensor data: We used two datasets to train our sensor data model. Dataset 1 was released by WISDM lab collected with Actitracker App [12], including walking, jogging, sitting, standing and lying down. We only used it to train our activity recognition model. Dataset 2 contains 685 MB accelerometer and gyroscope data collected from our 36 volunteers when they were performing group activities including walking together, playing badminton and playing table tennis. The sampling rate of sensor data is 100Hz.

![](images/9dc5f742c439d98a80468fe0b23239ec8110660f603a5804cc396b93fb224d4f.jpg)



Fig. 4: Confusion matrix of activity recognition.

Multimodal data case study: We collected sensor data and photos of one social activity, 6 volunteers playing table tennis. The sensor data was collected from the users' smart watches when they were playing table tennis. The photos were taken by the participants during the game. We collected 297 photos and sensor data with a total duration of approximately 260 minutes.

# B. Implementation and Experiment Configuration

# 1) Semantic Extraction:

Photos: For image semantic tag extraction, we adopt an image description model to extract as comprehensive information (e.g., objects, scene, event) as possible with low computation cost. Specifically, we used Neural Image Caption (NIC) [13], which is a widely-used image captioning model with good performance. It produced a sequence of words related to different concepts in each photo. Then we used the pyWSD tool to remove ambiguous meanings of words. Besides, only verbs and nouns were kept as the semantic tags of photos.

Sensor data: Among various machine learning model for activity recognition using sensor data $[7]$ $[8]$ , we chose the one of the latest deep learning model proposed in $[14]$ because of its efficiency and accuracy. We divided the combination of Dataset 1 and Dataset 2 into the training set and the test set, and trained the activity recognition model. Firstly, we filtered out the noise of sensor data. We conducted residuals analysis by calculating residuals root mean square error (RMSE) of different cutoff frequency, and chose the cutoff frequency when the fitted exponential curve decreases by 95%. Secondly, we segmented data with a sliding window into fixed length 256 samples, and then calculated the Short Time Fourier Transform (STFT) features. In this way, the variation of frequency and phase of the sensor signal can be well quantified. Finally, STFT features were fed into the deep learning model. Then we used pyWSD to convert each label into the a specific semantic meaning to generate the tag.

2) Data Aggregation: There are two important parameters in DBSCAN: (1) eps is the maximum distance between two samples for one to be considered as in the neighborhood of the other. (2) MinPts is the number of samples in a neighborhood for a point to be considered as a core point. In order to determine eps and MinPts, we ran the experiments to quantify the effect of this two parameters on single-modal data aggregation. Adjusted Rand Index (ARI) is computed to measure the quality of single-modal data aggregation. ARI is a value with range [-1,1], and the closer ARI is to 1, the better the performance of data aggregation is. According to the experiments, we set $eps = 0.82$ , MinPts=4 for photo data, and $eps = 0.45$ , MinPts=5 for sensor data.

<table><tr><td></td><td>Data of truly shared activities</td><td>Data of truly non-shared activities</td></tr><tr><td>Data of detected shared activities</td><td>TP</td><td>FP</td></tr><tr><td>Data of detected non-shared activities</td><td>FN</td><td>TN</td></tr></table>

TABLE II: The notations of metrics for measuring detection.

3) Shared activity detection: We used precision = $\frac{TP}{TP+FP}$ and recall = $\frac{TP}{TP+FN}$ to quantify the performance of our shared activity detection. The higher precision means higher ability to protect privacy and lower risk of data leakage, the higher recall means better usability.

# C. Evaluation of System

1) Photo data sharing: In this section, we evaluated the performance of shared activity detection using photos only.

We ran the data aggregation algorithm for each user's photos with different parameters and compute ARI. ARI reaches highest value 0.795 when $eps = 0.82$ and MinPts=4, and 305 tags were detected as incorrect tags among 47,837 tags. Filtering those incorrect tags can make the description of one activity and friend tags more accurate. We set $eps = 0.82$ and MinPts=4 in the subsequent experiment.

We ran the secure shared activity detection protocol between pairs of users who have shared activities. We asked each pair of users to request data of all shared activities from each other, resulting in $17 \times 2 = 34$ results. We compared the performance under different thresholds with or without filtering inaccurate tags. As shown in Fig. 5 and Fig. 6, we suggest that users set the threshold at about 0.5, which can ensure good privacy protection and high usability. The result with or without filtering inaccurate tags are similar. Model will extract similar semantics tags from photos of the same scene, although those tags may be wrong. Incorrect tags have little effect on the calculation results of graph similarity because both users' graphs may contain the same incorrect tags.

We measured the correlation between the number of users' shared activities and performance as shown in Fig. 7. The larger the number of shared activities is, which means that users maintain a closer relationship and have more data generated in the shared activities, the harder to detect all data pieces of shared activities. So the recall as the number of shared activities increases.

<table><tr><td></td><td colspan="3">precision(%)</td><td colspan="3">recall(%)</td></tr><tr><td>Threshold</td><td>0.1</td><td>0.5</td><td>0.9</td><td>0.1</td><td>0.5</td><td>0.9</td></tr><tr><td>secure detection</td><td>85.4</td><td>94.9</td><td>99.5</td><td>98.7</td><td>91.5</td><td>61.6</td></tr><tr><td>direct detection</td><td>87.8</td><td>95.4</td><td>99.9</td><td>97.3</td><td>91.3</td><td>61.6</td></tr></table>

TABLE III: Comparison of shared activity detection in secure way and direct way

We ran the shared activity detection using truly time interval instead of discrete time, and the comparison of the result between secure detection and direct detection is shown in TabIII. Our secure protocol using discrete time leads to a slightly higher recall and lower precision. The two activity-semantic graphs of the same activity from different users may be not temporally overlap, since people may attend and leave the activity and collect data asynchronously. However, the two set of discrete-time of this two graphs may have overlap, resulting in the higher recall of the secure way. Meanwhile, using discrete-time also allows a small portion of the data pieces not generated in shared activity to be shared, resulting in a slightly lower precision.

![](images/387499b02e8b0ee5ed5db8525bcc0b28031b5e9da0afcd20ac2ac49a774cfed5.jpg)



Fig. 5: Average precision of photo sharing with or without removing error tags.

![](images/08efd04d5da81dc01a2f81221ed4988a2c7efb3a2564b0ff351eadb2de020658.jpg)



Fig. 6: Average recall of photo sharing with or without removing error tags.

![](images/a258dab47bd4df5da4ba470d15cdb64ebb08b7a6cc649312bfef79a4a03721c2.jpg)



Fig. 7: Detection performance of different user pairs

2) Sensor data sharing: The sensor model is able to output eight labels and achieves the accuracy of 94.5% in test set as shown in Fig. 4. The model generates a tag for each 2.56-second data segment. To reduce our computation in data aggregation, we divided data in one minute, and decide the tag of each minutes data segment with voting method. Then, we run the data aggregation algorithm and calculate ARI under different parameter settings. We get the height ARI=0.981 when eps=0.45 and MinPts=5. We ran the secure shared activity detection protocol between pairs of users who have shared activities. When threshold is 0.5, the average precision and recall are 99.9% and 98.3% respectively. The performance of detection based on sensor data is better than photo based detection, because the type of activities is simple and the performance of data aggregation is better.

3) Case study for multimodal data sharing: We use the data collected from the table tennis game to simulate scenarios for multimodal data sharing. Our algorithm can solve the tag conflict when merging photos and sensor data, which will improve the accuracy of the tags of activity. NIC model has poor recognition ability for the scene of playing table tennis. It always generates tag tennis.n.01 due to its training data. The tags extracted from sensor data are all table\_tennis.n.01 after data aggregation and incorrect tags filtering. When merging photos and sensor data, tennis.n.01 will be removed.

We set up two sets of experiments: the requester has no sensor data while the sender has sensor data, and the sender and requester have the same amount of sensor data pieces. We assigned a certain proportion of the photos to the requester while the other photos to the sender, and then we calculated the graph similarity $\text{Sim}(G_{a_r}; G_{a_s})$ as shown in Fig. 8. When the requester has no sensor data as shown in Fig. 8(a), his activity-semantic graph won't contain node table\_tennis.n.01. The sender has table\_tennis.n.01 extracted from the sensor data, so when $I_S$ of sender increases, which means the weight of $G_{a_s}$ . (table\_tennis.n.01) increases, $\text{Sim}(G_{a_r}; G_{a_s})$ becomes lower. As the number of sender's photos decreases, less tags are from photos and less weight of the other tags except table\_tennis.n.01. which also result in the lower $Sim(G_{a_r};G_{a_s})$ . When the requester has sensor data as shown in Fig. 8(b), $Sim(G_{a_r};G_{a_s})$ is similar with different $I_S$ .

Therefore, combining multimodal data can result in the larger graph similarity of the same activity, thereby can improve the recall of shared activity detection.

# D. Micro-Analysis of System Cost

The device we implemented our system are mobile phones (HUAWEI Mate9), smart watches(Huawei-Watch and Moto-360) and computer (Intel i7-6700 CPU 3.40GHz). We implemented the NIC model on computer and migrated it to Android phones with TensorFlow. We implemented sensor model with TensorFlow, DBSCAN with scikit-learn, and secure shared activity detection protocol on the computer.

To process one photo, the average run time of NIC model is 3.67 s on the phone, and 2.41 s on the computer with CPU. The average number of tags extracted from one photo is 5.6. The average run time of human activity recognition model is 0.03s to tag a 2.56s sensor data piece. In data aggregation process, distance matrix between points should be precomputed before DBSCAN. We calculated all possible semantic distances in advance and accelerated the computation of the distance matrix by querying tables. The average time to compute the distance matrix against the number of tags is shown in Fig. 9. For secure shared activity detection, PSI operation are extremely fast within seconds as shown in Fig. 10.

# VII. RELATED WORK

To the best of our knowledge, there are few approaches addressing the problem of privacy-preserving shared activities detection based on multimodal data. Our work is related to existing work in the following areas.

There exist massive amount of research of visual understanding, such as object detection $[5]$ , face detection $[3]$ and action recognition $[2]$ . An image description model $[13]$ can produce more comprehensive information from photos with minimum cost. There are also lots of work addressing activity recognition using sensor data using various machine learning methods $[15]$ $[7]$ $[8]$ . In this work, we adopt existing models to extract semantic tags from data pieces to design the representation of complex activities and then focus on the secure matching of different activities.

To discover whether users are being together and to establish a connection, some methods require users to perform specific actions, such as shaking [16], or with specific devices [17]. Without the user's participation, sensor data [18] and location information [19] are used to infer users' linkage. For social event detection, multimedia data are widely used such as videos [20] and images [21], and lots of work did this combining information from social networks [22]. Most of those work neglected relations among multimodal data and many of them didn't take privacy into consideration. For the secure computation protocol, existing privacy-preserving record matching methods [23] mainly address comparison of pairs of data items, and privacy-preserving searching methods mainly focus on searching data with keywords [24] or features [25] while we need to compare sets of correlated data items, i.e., activity-semantic graphs.

![](images/7633f541eed18bd00c7a936cf8262cde581a08ffaa5c21af4b959e83ed9557b0.jpg)



(a) Requester has no sensor data

![](images/d869b1b5b93f9576fce651b9cac94a7988dfcffbe7bc0594770c29cb9871e251.jpg)



(b) Requester has sensor data   
Fig. 8: The calculated graph similarity against the proportion of requester's photos in case study.

# VIII. CONCLUSION

In this work, we propose a framework enabling secure shared activity detection based on users' multimodal historical data, which also facilitates multimodal data and social relationships management. Our experiments demonstrate the feasibility and efficiency of our design. Our activity-semantic graph provides a unified representation of diverse activities. It not only supports cross-modal activity data comparison, but also can be applied to other promising applications such as user profiling and friend recommendation. Our detection method can be easily extended to deal with data with more metadata information, e.g., GPS locations. More user-friendly functions can also be easily added, such as allowing users to define privacy tags to protect data with specific content and utilizing image similarity comparison techniques to avoid transmitting similar photos. There are still many intriguing issues that need further research. First, the semantic tags yielded by current machine learning models are still not accurate and comprehensive enough. Second, the computation and communication overhead in a multi-party scenario should be further reduced. Third, how to prevent malicious attacks like data falsification remains a challenging issue.

# ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This work is supported by the National Key R&D Program of China 2017YFB1003003, NSF China under Grants No. 61822209, 61932016,61751211, 61572281, 61520106007, and the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] R. Marin-Perianu, M. Marin-Perianu, P. Havinga, S. Taylor, R. Begg, M. Palaniswami, and D. Rouffet, “A performance analysis of a wireless body-area network monitoring system for professional cycling,” Personal and Ubiquitous Computing, vol. 17, no. 1, pp. 197–209, 2013.

![](images/5de891f0c24e0b907fa5fa014c40a460bae923c93bfa2b8024f6436203702ed8.jpg)



Fig. 9: Time cost of distance matrix computation.

![](images/1658820ef66e06bd342de8f4433693db5d6266f5f8295f36a4e2ab24c25cb0f5.jpg)



Fig. 10: Time cost of PSI operation.

[2] L. Wang, Y. Qiao, and X. Tang, “Action recognition with trajectory-pooled deep-convolutional descriptors,” in CVPR, 2015, pp. 4305–4314.   
[3] F. Schroff, D. Kalenichenko, and J. Philbin, “Facenet: A unified embedding for face recognition and clustering,” in CVPR, 2015, pp. 815–823.   
[4] G. A. Miller, “Wordnet: a lexical database for english,” Communications of the ACM, vol. 38, no. 11, pp. 39–41, 1995.   
[5] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, “You only look once: Unified, real-time object detection,” in CVPR, 2016, pp. 779–788.   
[6] B. Zhou, A. Lapedriza, J. Xiao, A. Torralba, and A. Oliva, “Learning deep features for scene recognition using places database,” in Advances in neural information processing systems, 2014, pp. 487–495.   
[7] J.-L. Reyes-Ortiz, L. Oneto, A. Samà, X. Parra, and D. Anguita, “Transition-aware human activity recognition using smartphones,” Neurocomputing, vol. 171, pp. 754–767, 2016.   
[8] F. J. Ordóñez and D. Roggen, “Deep convolutional and lstm recurrent neural networks for multimodal wearable activity recognition,” Sensors, vol. 16, no. 1, p. 115, 2016.   
[9] L. Tan, “Pywsd: Python implementations of word sense disambiguation (wsd) technologies [software],” 2014.   
[10] M. Ester, H.-P. Kriegel, J. Sander, and X. Xu, “Density-based spatial clustering of applications with noise,” in Int. Conf. Knowledge Discovery and Data Mining, vol. 240, 1996.   
[11] B. Pinkas, T. Schneider, and M. Zohner, “Scalable private set intersection based on ot extension.” IACR Cryptology ePrint Archive, 2016.   
[12] J. W. Lockhart, G. M. Weiss, J. C. Xue, S. T. Gallagher, A. B. Grosner, and T. T. Pulickal, “Design considerations for the wisdom smart phone-based sensor mining architecture,” in SensorKDD. ACM, 2011.   
[13] O. Vinyals, A. Toshev, S. Bengio, and D. Erhan, “Show and tell: A neural image caption generator,” in CVPR, 2015, pp. 3156–3164.   
[14] Z. Y. X.-Y. L. Guangjing Wang, Lan Zhang, “Socialite: Social activity mining and friend auto-labeling,” in IPCC, 2018.   
[15] N. Xiao, P. Yang, Y. Yan, H. Zhou, and X.-Y. Li, “Motion-fi: Recognizing and counting repetitive motions with passive wireless backscattering,” in INFOCOM. IEEE, 2018.   
[16] B. Groza and R. Mayrhofer, “Saphe: simple accelerometer based wireless pairing with heuristic trees,” in MoMM, 2012.   
[17] L. Zhang, X.-Y. Li, W. Huang, K. Liu, S. Zong, X. Jian, P. Feng, T. Jung, and Y. Liu, “It starts with igaze: Visual attention driven networking with smart glasses,” in MobiCom. ACM, 2014.   
[18] M. Miettinen, N. Asokan, T. D. Nguyen, A.-R. Sadeghi, and M. Sobhani, "Context-based zero-interaction pairing and key evolution for advanced personal devices," in SIGSAC. ACM, 2014, pp. 880-891.   
[19] M. Backes, M. Humbert, J. Pang, and Y. Zhang, “walk2friends: Inferring social links from mobility profiles,” in SIGSAC. ACM, 2017.   
[20] X. Chang, Y.-L. Yu, Y. Yang, and A. G. Hauptmann, “Searching persuasively: Joint event detection and evidence recounting with limited supervision,” in MM. ACM, 2015, pp. 581–590.   
[21] H. Cai, Y. Yang, X. Li, and Z. Huang, “What are popular: Exploring twitter features for event detection, tracking and visualization,” in MM, 2015.   
[22] L. Zhang, X.-Y. Li, K. Liu, T. Jung, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in mobile social networks,” IEEE Transactions on Mobile Computing, vol. 14, no. 9, pp. 1888–1902, 2014.   
[23] A. Inan, M. Kantarcioglu, G. Ghinita, and E. Bertino, “Private record matching using differential privacy,” in EDBT, 2010.   
[24] N. Cao, C. Wang, M. Li, K. Ren, and W. Lou, “Privacy-preserving multi-keyword ranked search over encrypted cloud data,” IEEE Transactions on parallel and distributed systems, vol. 25, no. 1, pp. 222–233, 2013.   
[25] L. C. Zhang, T. Jung, K. Liu, X. Li, X. Ding, J. Gu, and Y. Liu, “Pic: Enable large-scale privacy preserving content-based image search on cloud,” IEEE Trans. Parallel Distrib. Syst., vol. 28, pp. 3258–3271, 2017.