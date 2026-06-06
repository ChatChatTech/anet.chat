# Mechanism Design for Finding Experts Using Locally Constructed Social Referral Web

Lan Zhang, Student Member, IEEE , Xiang-Yang Li, Senior Member, IEEE, Jingsheng Lei, Jiaguang Sun, and Yunhao Liu, Senior Member, IEEE

Abstract—In this work, we address the problem of distributed expert finding using chains of social referrals and profile matching with only local information in online social networks. By assuming that users are selfish, rational, and have privately known cost of participating in the referrals, we design a novel truthful efficient mechanism in which an expert-finding query will be relayed by intermediate users. When receiving a referral request, a participant will locally choose among her neighbors some user to relay the request. In our mechanism, several closely coupled methods are carefully designed to improve the performance of distributed search, including, profile matching, social acquaintance prediction, score function for locally choosing relay neighbors, and budget estimation. We conduct extensive experiments on several data sets of online social networks. The extensive study of our mechanism shows that the success rate of our mechanism is about 90 percent in finding closely matched experts using only local search and limited budget, which significantly improves the previously best rate 20 percent. The overall cost of finding an expert by our truthful mechanism is about 20 percent of the untruthful methods, e.g., the method that always selects high-degree neighbors. The median length of social referral chains is 6 using our localized search decision, which surprisingly matches the well-known small-world phenomenon of global social structures.

Index Terms—Mechanism design, strategyproof, social networks, referral web, distributed search, small world

# 1 INTRODUCTION

INDING experts matching desired attributes is common Fand useful in real life, for example, to find a student studying math from a nearby collage to be a home tutor or to invite a computer engineer professor to give a talk. Online social networks (OSN), like Facebook and LinkedIn, are powerful resources for finding experts due to the abundant personal attribute information. So far, there are two methods of expert finding in industry and literature. One is searching in a large database with the global information. The other strategy is distributed search using a chain of social referrals through acquaintances. Searching a referral chain can help people find the experts who cannot be obtained by using search engines. Evans et al. [1] found that targeting questions to specific friends can receive in-depth answers. Asking a favor from or making friends with the target person are usually much easier with recommendations from his friends than just being a stranger [2]. Moreover, there are limits as to the amount and the kinds of information that a user is able or willing to make available to the public at large [3]. For example, many users of online social networks have made their profiles unsearchable to public or only visible to friends or people from certain networks. Searching for some information or experts thus becomes a matter of searching the social network with a chain of personal referrals from the searcher (or initiator) to the expert with only local information.

The homophily principle [4] enables the efficient construction of referral chains in online social networks. A lot of existing work has proved that social networks are searchable through short pairwise connections [5], [6]. For online social networks, our analysis (presented in Section 4) of a Facebook data set shows about 99 percent users are within 6 hops on average. Compared to using a single social networking site,a cross-sites people search may be much more helpful with hundreds of social networking sites. For example, if you are looking for a trustworthy lawyer who works in your city and one of your good friends on Facebook knows a well reputed lawyer on Linkedin who is unsearchable. In this case, an efficient cross-site user search/referral can be easily completed through your friend but not any single site search engine. Aggregation of information from multiple social networks for a person has been facilitated by projects such as OpenID, DataPortability, and various microformats. Existing aggregators include Friend-Feed, MyBlogLog, Jaiku, and Plaxo.

The social referral path is supposed to be done voluntarily in existing work. The results along this line typically emphasize that the completed paths tend to be short, thus ignoring the fact that a vast majority of paths never reach their ultimate targets [7]. It has been reported in [8] that the only parameter governing the success of a search is not related to the topology or search procedure, but the probability of termination at each step. Most paths are terminated for the reason that participants are not sufficiently motivated to relay messages. Thus, taking user’s self-interest into consideration is necessary for a successful chain of social referrals. In this paper, we propose a new search mechanism for expert finding in online social networks. Our mechanism exploits the homophily principle of social networks. Based on the similarity calculation, and acquaintance probability estimation, we design a truthful local search mechanism that works well even with possible selfish behavior.

Our main contributions. In this work, we design a truthful mechanism for expert finding by a chain of individuals from the initiator to the expert, where each intermediate user makes a decision using only local information. Our mechanism also takes the users’ self-interest into account with a well-designed payment strategy. We assume that each intermediate user has a privately known cost of participating in the chain of social referrals. We theoretically prove that our mechanism is truthful, i.e., each intermediate user will maximize her utility if she truthfully declared her cost and executed the search procedure. We also estimate the required budget for searching an expert with some profile. We conduct extensive experiments to study the performance of our mechanism. Our experimental results show that the social referral path found by our mechanism is significantly shorter than the one found by previous approaches. The total cost of intermediate agents participating in the chain is also much smaller than naive approaches such as using a high-degree neighbor. Moreover, the success rate of our localized search strategy is about 90 percent, which is significantly better than the best reported success rate 20 percent [9], [10]. Part of this work has been published in [11]. Compared with [11], in this paper, we complete the search method with incremental local learning, and add theoretical analysis and proof for our mechanism. We also greatly enrich our mechanism measurements with more data set analysis and experimental analysis.

Paper organization. The rest of the paper is organized as follows. In Section 2 we present the network model for expert finding and our similarity calculation method. In Section 3 we present our truthful mechanism for finding experts using chain of referrals. We report our evaluation results in Section 4, review the related work in Section 5 and conclude the paper in Section 6.

# 2 SYSTEM MODEL AND PRELIMINARIES

# 2.1 Problem Formulation Using Online Social Networks

A social network is modeled by a graph $G = ( V , E )$ . Every user $v _ { i } \in V$ ¼ ð Þin G has a unique identity, called i for 2simplicity. By profiling or data collection, each user $v _ { i }$ is associated with an m-dimension profile vector $A _ { i } =$ $\langle a _ { i } ^ { 1 } , a _ { i } ^ { 2 } , \ldots , a _ { i } ^ { m } \rangle$ ¼, which represents her characteristics and h isocial groups. Here the value $a _ { i } ^ { j } ,$ represents a characterization of user i for the jth attribute. The link $v _ { i } v _ { j } \in E$ between $v _ { i }$ and $v _ { j }$ 2is the acquaintance connection. For example, the friendship in Facebook, the co-authorship in co-author networks and communication in email networks. User $v _ { i }$ is called a neighbor of $v _ { j }$ in the social network G if the link $v _ { i } v _ { j }$ exists. We assume that each user only knows the profile of her neighbors.

In this work, we study finding experts in social networks via a chain of referrals by some intermediate users. Assume that there is an initiator, say $v _ { 0 } ,$ , who wants to find an expert, characterized by a profile vector $\mathcal { A } _ { t } = \langle a _ { t } ^ { 1 } , a _ { t } ^ { 2 } , \ldots , a _ { t } ^ { m } \rangle$ . Due to the ambiguity of profile, we say that a user $j$ has a matching profile with $\boldsymbol { A } _ { t }$ if the “distance” between her profile $A _ { j }$ Aand the target profile $\boldsymbol { A } _ { t }$ is within a small error bound -. The Ainitiator will ask her neighbors to help her to find a matching expert. The process will be iterated until the expert is found or some termination conditions are met $( \mathrm { e . g . }$ , the maximum number of referrals, or the total cost incurred for search). The output is a social referral path $\mathbf { P } ( v _ { 0 } , v _ { t } )$ from the initiator $v _ { 0 }$ to a target user $v _ { t }$ ð Þwith the matching profile.

A major difference between the system model used in this study and previous studies for finding friends/ experts is that here we assume that each user i has a cost $c ^ { i }$ for querying her neighbors to get a target expert for some initiator. We assume that the cost $c ^ { i }$ is privately known only to $v _ { i } .$ . The initiator originally has a budget B for performing the task of finding experts in the social network. We say that finding experts using such a path $\mathbf { P } ( v _ { 0 } , v _ { t } )$ is feasible if the total cost requested by users on ð Þthis path is at most the budget B of the initiator. If we know the whole network and the cost vector, the problem becomes the simple shortest path problem. A truthful mechanism can also be designed in such centralized approach [12]. However, in the practical social network setting, several challenges need to be addressed to solve this problem. The challenges include the follows:

1. computing the profile similarity and acquaintance probability,   
2. designing localized referral strategy since each intermediate user only knows her neighbors, and   
3. designing a payment mechanism to make participants tell truth without any global information for lies checking.

As the number of users grows exponentially with the social distance from the initiator, a search strategy is needed to select the correct user among hundreds of acquaintances to form the next link of the referral path using only local information. There are two basic strategies in people/expert search: 1) choosing a high degree neighbor, or 2) “closest” neighbor by profile distance. In Section 4, we found by experiments that our profile similarity based strategy outperforms the high degree strategy greatly.

# 2.2 Similarity and Acquaintance Probability

Similarity breeds connection.It has been well observed that the shorter the social distance between two users, the higher the probability that they are acquainted to each other or have a shorter network distance [4]. A social distance is usually given as a metric of the similarity or relevance between two users. There are some existing social distance measurements, for example, organizational hierarchy distance[5], or geographical distance. In this work, we use the similarity of two users’ attributes as the social distance measurement to indicate the similarity between them. Then we use users’ similarity to estimate their probability of acquaintance.

Distance and similarity of attributes.The attribute could be discrete categorical characteristics such as social group or gender, or numerical characteristics such as age or vertex degree. For each attribute $a ^ { k } ,$ , an attribute distance $d _ { i j } ^ { k } = d ^ { k } ( a _ { i } ^ { k } , a _ { j } ^ { k } )$ is defined. For example, the distance of gen-¼ ð Þder could be 0 for two users of the same sex, and 1 otherwise. The distance of age could be $d ^ { k } ( x , y ) = | x - y |$ . ð Þ ¼ j  jBased on the attribute distance, the attribute similarity is given as

![](images/2b2fa37961002c1208db736992a5be870b40f63fe29900c7ae538b1334e9b6dc.jpg)



Fig. 1. The ego network of a random selected vertex in facebook social network graph, whose degree is 71.

$$
s _ {i j} ^ {k} = 1 - \frac {d _ {i j} ^ {k}}{\max _ {(i , j)} d _ {i j} ^ {k}}. \tag {1}
$$

The similarity between users $v _ { i }$ and $v _ { j }$ is a vector $S _ { i j }$ (or denoted as $\dot { S } ( A _ { i } , A _ { j } ) )$ ) defined as $S _ { i j } = \langle \bar { s } _ { i j } ^ { 1 } , s _ { i j } ^ { 2 } , . . . , s _ { i j } ^ { m } \rangle$ .

ð Þ ¼ h iWe notice that the similarity of different attributes contribute differently to acquaintance probability. Some attributes are strong evidences of acquaintance and some are weak. Users who are close in the strong positive evidence have a high probability of acquaintance. We model the acquaintance probability of two users using the logistic function [13] about their profile similarity vector. Specifically, if $E _ { i , j }$ is the event that the user $v _ { i }$ and $v _ { j }$ are acquainted and $\tilde { E } _ { i , j }$ is the event that they are not acquainted, define the probability $\begin{array} { r } { \mathbf { P r } \big ( E _ { i , j } | S _ { i j } = X \big ) = l o g i t ^ { - 1 } ( \beta X ) = \frac { 1 } { 1 + e ^ { - \beta X } } } \end{array}$ : Here the parameter $\beta$ j ¼ ¼ ð Þ ¼ þ is an m-dimensional vector to be studied later. Let $r ( X )$ be the odds ratio when that similarity equals X, i.e., we define r X  Pr Ei;j ð Þ j Sij¼X1 Pr E S X Pr Ei;j ð Þ j Sij¼XPr E\~ S X . $X ,$ $\begin{array} { r } { r ( X ) = \frac { \mathbf { P r } \left( E _ { i , j } \mid S _ { i j } = X \right) } { 1 - \mathbf { P r } \left( E _ { i , j } \mid S _ { i j } = X \right) } = \frac { \mathbf { P r } \left( E _ { i , j } \mid S _ { i j } = X \right) } { \mathbf { P r } \left( \tilde { E } _ { i , j } \mid S _ { i j } = X \right) } } \end{array}$ Then for a vector $X = ( x ^ { 1 } , x ^ { 2 } , \cdot \cdot \cdot , x ^ { m } )$ Þ, we have

$$
\beta \cdot X = \beta^ {0} + \beta^ {1} x ^ {1} +... + \beta^ {m} x ^ {m} = \ln (r (X)), \tag {2}
$$

where $\beta ^ { 0 }$ is the intercept, and $\beta ^ { k }$ describes the size of the contribution of the similarity of attribute $a ^ { k }$ on the acquaintance relationship. A positive $\beta ^ { k }$ means the similarity of $a ^ { k }$ increases the probability of acquaintance, while a negative $\beta ^ { k }$ means a decrease effect; a large $\beta ^ { k }$ means that the attribute $a ^ { k }$ strongly influences the probability. We define

$$
\text { profile   similarity }: \quad s _ {i j} = \beta \cdot S _ {i j},
$$

which is the weighted summary of all the attributes similarities. For profile similarity, the larger the value, the closer the two profiles. In the Facebook data set (introduced in Section 4.1), the largest profile similarity is about 3:5252 for the MIT data set and 3:6063 for the Harvard data set. Note that here the profile similarity could be negative values.

Let the probability that the similarity vector between two randomly selected profiles $A _ { i }$ and $A _ { j }$ equals X be $\mathbf { P r } \big ( S _ { i j } = X \big )$ . Then, the probability that $v _ { i }$ and $v _ { j }$ are ¼acquaintances is Pr Ei;j  Sij  X    Prð Þ Sij¼X ^ Ei;j $\begin{array} { r } { \mathbf { P r } \big ( E _ { i , j } \mid S _ { i j } = X \big ) = \frac { \mathbf { P r } \big ( S _ { i j } = X \wedge E _ { i , j } \big ) } { \mathbf { P r } \big ( S _ { i j } = X \big ) } } \end{array}$ from Pr  Sij X Bayes theory. Then a simple computation shows that $\begin{array} { r } { r ( X ) = \frac { \mathbf { P r } \left( S _ { i j } = X \wedge E _ { i , j } \right) / \mathbf { P r } \left( S _ { i j } = X \right) } { \mathbf { P r } \left( S _ { i j } = X \wedge \tilde { E } _ { i , j } \right) / \mathbf { P r } \left( S _ { i j } = X \right) } = \frac { | \{ ( V _ { i } , V _ { j } ) | S _ { i j } = X \wedge E _ { i , j } \} | } { | \{ ( V _ { i } , V _ { j } ) | S _ { i j } = X \wedge \tilde { E } _ { i , j } \} | } } \end{array}$ . So we can ¼ ^ð Þ ð Þ¼ jfð Þ j ¼ ^use logistic regression to derive the parameter $\beta$ jby learning $r ( X )$ from a known graph, such as a local graph like the ego ð Þnetwork. With the parameter $\beta ,$ we can predict the acquaintance probability in an unknown graph given the profile vectors of two users. Note that the larger the profile similarity, the higher the probability they are acquaintances.

![](images/419c06b70f9136f66f0e8111afc217cda527a706f2a375c6966adfc29c9cbb5e.jpg)



Fig. 2. The acquaintance probability between the neighbors of randomly selected ego network and target estimated by the local paramete $\beta$ and global parameter b.

# 2.3 Ego Network and Incremental Local Learning

Recall that we assume that for finding experts in a social network, every person only knows the information of the target person and his current immediate one-hop neighbors in the social network. Here we present a method to learn the parameter $\beta$ locally for acquaintance probability calculation.

Before a user starts a search, she can create an ego network (also called a personal network) centered on herself to learn all the information needed for acquaintance probability calculation. In the ego network, the node set V includes the vertex itself and all her direct friends in the social network G. The edge set $E _ { i }$ consists of all the edges between vertices in $V _ { i } .$ Fig. 1 shows an example of the ego network of a randomly selected person from Facebook data set. We can learn r X from the ego network and $\beta$ can be updated ð Þalong the chain during the search procedure.

A natural question is then “Is ego network sufficient enough?” Newman[14] has shown that one’s immediate neighbors in the acquaintance network are far from being a random sample, although they show some characteristics of the whole network. We compare the acquaintance probability estimated by globally learned $\beta$ parameter and $\beta$ parameter learned from ego networks, as shown in Fig. 2. Here the ego vertex and the target vertex are both chosen randomly. We find that the probabilities almost have the same relative magnitude among all neighbors in both estimations. The difference between the two lines are mainly caused by a higher density of the ego network than the whole graph. So the ego networks in a social network is a typical sample of the whole graph, and the result shows that the ego networks can give us some sufficient evidence on acquaintance.

# 3 STRATEGYPROOF MECHANISM DESIGN

In this section, we present our truthful mechanism for finding experts in a social network using social referrals.

# 3.1 Finding Experts Mechanism Definition

We suppose that all users are selfish and rational, which means that they will optimize their strategies to maximize their utilities and they will make consistent decisions in the same conditions. For a searching task, the initiator has a privately known budget B and each other user $v _ { i }$ has a privately known cost $c ^ { i }$ when she is asked to participate in the referrals.

# 3.1.1 Search Procedure

Before we present our mechanism, we first give an overview of the search procedure for finding experts using a chain of social referrals. There are five phases during our expert search procedure:

1. Initialization phase. The initiator $v _ { 0 }$ checks her neighbors to see whether the target is among them. If the target is among her neighbors, the search stops and it does not incur any additional cost. Otherwise, the initiator estimates the budget B based on the profile similarity $s _ { 0 t }$ between her profile and the target profile $\boldsymbol { A } _ { t }$ .   
2. ABidding phase. The initiator $v _ { 0 }$ announces the search task by giving the profile $\boldsymbol { A } _ { t }$ of the target expert. Any her neighbor $v _ { k }$ Awho intends to participate in the social referral will declare a price $d ^ { k } .$ , which is not necessarily her true cost, via a sealed-bid within a bidding time window.   
3. Winner decision phase. The profile similarity between each neighbor $v _ { k }$ and the target is known to $v _ { 0 }$ since v can access the profile of $v _ { k }$ . User $v _ { 0 }$ chooses a winner neighbor, say $v _ { w } ,$ as the next-hop vertex based on a score function (which will be discussed in detail later) and pays a compensation $d ^ { k }$ to the chosen neighbor $v _ { w } .$   
4. Execution phase. The selected neighbor $v _ { w }$ continues the search task as a new initiator whose budget is $B - d ^ { k }$ until an expert with a “closely matching” pro-file is found.   
5. Bonus payment phase. Once the search is completed successfully, the initiator will pay a bonus to every agent in this social referral path.

# 3.1.2 Algorithmic Mechanism Design

In the expert finding algorithm, the input is the target profile $\boldsymbol { A } _ { t } ,$ the budget $B ,$ and an acceptable lowest similarity  Abetween the profile of the found expert and the sought target given by the initiator. The objective is to find the target by a chain of social referrals and pay intermediate neighbors with the limited budget.

We refer to every selfish rational participant as an agent in this game, who is also a vertex in the social graph. There are n agents. It will cost $c ^ { k }$ for each agent $v _ { k }$ to perform a searching task. In this work, we assume that $c ^ { k }$ is a private input, which is the true cost only known by $v _ { k } .$ . When bidding for the task, an agent $v _ { k }$ can choose to declare a price $d ^ { k } ,$ , which could be the true cost $c ^ { k }$ or any other valid cost. Let $d = \langle d ^ { 1 } , d ^ { 2 } , \cdot \cdot \cdot d ^ { n } \rangle$ . We define our expert finding mechanism as $\mathbf { M } = ( \mathbf { O } , \mathbf { p } ) ,$ i, which is composed of an output function $\mathbf { O } ( d )$ ¼ ð Þand an n-tuple payment function $\langle \pmb { \mathrm { p } } ^ { 1 } ( d ) , \pmb { \mathrm { p } } ^ { 2 } ( \dot { d } ) , \dots , \pmb { \mathrm { p } } ^ { n } ( d ) \rangle$ ð Þ. An output O is a social referral path consists of a sequence of vertices, say $\mathbf { O } = \{ v _ { j _ { 1 } } , v _ { j _ { 2 } } , \ldots , v _ { j _ { l } } \}$ , where $v _ { j _ { 1 } }$ is simply $v _ { i }$ and $v _ { j l }$ ¼ f   g has a matching profile with the sought target profile $\boldsymbol { A } _ { t }$ if Athe search is successful. The goal of the mechanism is to find a user, say $v _ { j _ { l } }$ such that the profile similarity between the target profile $\boldsymbol { A } _ { t }$ and the profile $A _ { j _ { l } }$ of user $v _ { j _ { l } }$ is maximized (at Aleast a value $\xi ) ,$ while the total payment from the initiator is no more than her budget, i.e., max $S ( A _ { j _ { l } } , \mathcal { A } _ { t } )$ , while $\begin{array} { r } { \sum _ { v _ { i _ { l } } \in \mathbf { O } } \mathbf { p } ^ { j _ { k } } \le B _ { \ l } } \end{array}$ ð A Þ. When the search fails, we denote the output kas f.

Each agent’s preferences are given by a valuation function: $\nu ^ { k } ( c ^ { i } , \mathbf { O } ) \stackrel { - } { = } - c ^ { k } \mathrm { i } \hat { \mathbf { i } } \thinspace v _ { k } \in \mathbf { O }$ , and $0 \mathrm { i f } \ v _ { k } \notin \mathbf { O }$ . The utility function ð Þ ¼of the agent $v _ { k }$ is

$$
u ^ {k} = \mathbf {p} ^ {k} (d) + \nu^ {k} (c ^ {k}, \mathbf {O}). \tag {3}
$$

The utility function is the objective function each agent aims to optimize in the bidding phase.

In the winner decision phase, the decider needs to select one from all participants as the next link. Without causing ambiguity and to simplify the expression, here we use $d ^ { k }$ as the normalized value of the declared price of $v _ { k }$ and $s _ { k t }$ as the normalized value of the profile similarity between $v _ { k }$ and $v _ { t }$ . The score function for the winner decision is defined as

$$
\eta_ {k} = f (d ^ {k}, s _ {k, t}). \tag {4}
$$

$f$ could be any function that entails: 1) $\partial { \eta _ { k } } / \partial { d ^ { k } } \geq 1$ and 2) $\partial \eta _ { k } / \partial s _ { k , t } < 0 .$ . After extensive testing, we use the following function in this work

$$
\eta_ {k} = d ^ {k} + (1 - s _ {k, t}), \tag {5}
$$

which has been proved to yield a good performance in our experiments. Any intermediate user could choose the neighbor with the minimum h as the next link.

The payment function is $\mathbf { p } ^ { k } ( d ) = d ^ { k } + b ^ { k } ( d )$ if $v _ { k } \in \mathbf { O }$ and 0 otherwise. Here $b ^ { k }$ ð Þ ¼ þ ð Þis the bonus paid to user $v _ { k } .$ 2. When an agent $v _ { k }$ is chosen as a vertex of the social referral path, she will get $d ^ { k }$ as her compensation no matter the search is successful or not. The bonus $b ^ { k }$ will be paid in the payment phase only when a feasible output is found. In the decision phase, an agent $v _ { k }$ is selected because it has the smallest score $\eta _ { k }$ among all the neighbors of an intermediate user. Let $\eta _ { x }$ be the second smallest score in that stage, and we have $\eta _ { x } \geq d ^ { k } + ( 1 - s _ { k t } )$ . Then the value of bonus $\Breve { b } ^ { k }$ is defined as:

$$
b ^ {k} = \eta_ {x} - \eta_ {k} = \eta_ {x} - (1 - s _ {k t}) - d ^ {k}. \tag {6}
$$

Once the target is found, the bonus will be paid to agents in the social referral path from the remainder of the budget. In other words, we need

$$
\sum_ {v _ {k} \in \mathbf {O}} b ^ {k} (d) \leq B - \sum_ {v _ {k} \in \mathbf {O}} d ^ {k}. \tag {7}
$$

Since the budget is limited, there’s a chance that B is not enough to cover the bonus, i.e., inequality (7) is violated. In this case, the bonus will be paid to the agents in the descending order of the similarity of their successor agents until the budget is used, $\mathrm { i . e . , }$ , the agent who has selected a neighbor with a higher profile similarity will get paid bonus first. Using the bonus strategy we provide incentives for agents to maximize their utilities by declaring the true cost as well as choosing the next vertex with a higher similarity to the target. So an agent could maximize her utility as well as optimize the objective function. This claim will be proved formally later.

With the definition of payment and valuation function, the utility of the agent $v _ { k }$ is

$$
u ^ {k} = d ^ {k} - c ^ {k} + b ^ {k}. \tag {8}
$$

# 3.2 Mechanism Analysis

We assume that agents are all rational and selfish and each agent intends to maximize her own utility only. Then we have that our mechanism is truthful. Recall that a mechanism is truthful if for all $v _ { k }$ and all $d ^ { k } .$ , each agent’s strategy is to declare her true cost, i.e., $d ^ { i } = c ^ { i }$ and truth-telling maximizes her utility.

Theorem 1. Our mechanism M is truthful.

Proof. Please refer to Appendix A in the supplementary file, which can be found on the Computer Society Digital Library at http://doi.ieeecomputersociety.org/10.1109/ TPDS.2013.117.

It is obvious that our mechanism also satisfies the participation constraints, that is whenever an agent is truth-telling, her utility is non-negative.

# 4 EXPERIMENTS AND MEASUREMENT

# 4.1 Data Set

Facebook is the most popular online social network with more than 1 billion users, which makes it a powerful resource for finding experts. Here we use the real facebook data of MIT and Harvard for our analysis and experiments, which contains attributes of students and faculty from different departments. The data set is provided by the work [15], [16]. In this data set the isolated vertices are ignored. In the MIT data set, there are 6;440 users and 5; 02;504 friendship edges among them. In this undirected graph, the mean node degree is 78:0286 and the median node degree is 56. The graph diameter is 8 and the average path length between two vertices is 2:72. Ninety nine vertices are reachable to each other within 6 hops. For comparison, we also use the real facebook data from Harvard, which contains 15,000 users. We present more detail about the data set in the Appendix B, available in the online supplemental material.

# 4.2 Acquaintance Probability Prediction Using Profiles

In the data set, there are seven attributes in each user’s profile, which are “student/faculty”, “gender”, “major”, “second major/minor”, “dorm/house”, “high school” and “year”. We learn the b parameter for the seven attributes in the data set by logistic regression. The detailed method is discussed in Section 2. More detail about the attributes and b parameter are presented in the Appendix B in the supplementary file, available online.

With the b parameter, given two users’ profile vector, we can calculate their profile similarity and estimate their acquaintance probability. Fig. 3 presents the real acquaintance probability in MIT and Harvard via statistical analysis and the acquaintance probability estimated by our model via profile vector. It shows a good match between the real probability and our estimation. So our similarity calculation is an effective metric for acquaintance relationship.

![](images/403c8aa877f380e7b5afc8d718c9a4343bf363e76d9cfab8b676a0c16bee43f5.jpg)



Fig. 3. Acquaintance probability change with similarity in MIT and Harvard Facebook data sets.

# 4.3 Basic Max Similarity Search Strategy

Although shorter paths exist between vertices, it will be quite difficult to find the shortest path using only local acquaintance knowledge of immediate neighbors. In this section, we analyze the performance of our similarity based local search strategy and compare it with other local search strategies and real small world experiments. The basic search strategy without paying intermediate users gives us a baseline search performance of the our expert finding mechanism.

# 4.3.1 Performance of Different Search Strategies

If each user does not incur a cost for participating in the social referral web, several search strategies could be used here: random walk, high degree [17], and high similarity strategies. In the random walk strategy, an intermediate user will select a successor from her neighbors randomly and simply avoid the users already participated in the chain of social referral. It was proved that the path length by random walk is $O ( \ln ^ { 2 } ( N ) )$ for a random network of N ð ð ÞÞnodes. In the high degree strategy, an intermediate user selects the neighbor with the highest degree, who is more likely to know the target by virtue of the fact that she knows so many people. The third strategy, high similarity strategy, called MaxSim in this work, will select the neighboring user with the largest profile similarity (higher acquaintance probability) to the target.

We select 1;000 pairs of source and target from the MIT data set randomly, and run these three strategies to locally find the chain of social referral with/without path length constraint. Our extensive experiments show that the random walk strategies performs the worst. Thus, we just compare the results between high degree and high similarity strategies. Fig. 4 presents the path length distribution of paths and Table 1 presents the mean length, median length and successful rate of each strategy. Experiment results show that our high similarity local search strategy outperforms the high degree strategy in the mean length and median length greatly as we consider the attribute similarity to estimate the acquaintanceship. On the other hand, without path length constraint, the high degree strategy can achieve 99:8 percent success rate with some path that is more than 1;000 hops long; our similarity bias local search strategy may have 4:8 percent failure, but has only one path with length exceeding 100 (length 114). We analyze the 48 failed searches (among 1;000 search requests) and find that they all have targets with low node degrees, with a mean node degree 7:8. Meanwhile, they all have a very small profile similarity between the initiator and the target. If there is a path length constraint, e.g. 100, the successful rate of the high degree strategy is reduced to 80:6 percent, which is much lower than the successful rate of our high similarity strategy 93:1 percent.

![](images/8cd4c971f3b9910b23e32c9433e9175d515b2f61c34c75bbb39e76e22166dbc9.jpg)



Fig. 4. Path lengths of different local search strategies for 100 pairs of randomly selected initiators and targets in MIT Facebook data set. The small subfigure is the result with linear axis.

Consider the result of the work in [18] of social network search. They used friendship network data from a community website, Club Nexus, with 2,000 users, average node degree $8 ,$ and average shortest path 4. They compared 5 attributes simultaneously for the target and a user. In their experiments, the mean length is 135, and the median length is 28, which are much larger than our result, mostly because we learn the parameters locally to enable better acquaintanceship estimation.

# 4.3.2 Analysis of MaxSim Search Strategy

We compare the search result between MIT (6,440 users) and Harvard (15,000 users). The median path length with 100 randomly selected pairs of initiator/targets in Harvard data set is $5 ,$ the mean value is 46:7 without a length constraint. When there is a path length constraint (here we choose 100), the mean path length is 10:6 and the search success rate is 91 percent. As we have analyzed, the large mean path length is due to some extra long paths caused by some low node-degree targets and the low similarity between the initiator and target.

Fig. 5 demonstrates the path length distribution of the 1;000 found paths in the MIT data set using our local search

TABLE 1 Search Results of High Degree and Similarity Bias Strategies 

<table><tr><td></td><td>length constraint</td><td>mean</td><td>median</td><td>success rate</td></tr><tr><td>HighDegree</td><td>∞</td><td>126</td><td>12</td><td>99.8%</td></tr><tr><td>MaxSim</td><td>∞</td><td>22</td><td>6</td><td>95.2%</td></tr><tr><td>HighDegree</td><td>100</td><td>17</td><td>7</td><td>80.6%</td></tr><tr><td>MaxSim</td><td>100</td><td>11.6</td><td>6</td><td>93.1%</td></tr></table>

![](images/edb465b37ef22e771aa4cc1ecbedbf5229f5bc50383a546672689ce731516994.jpg)



Fig. 5. The path length distribution for the 1;000 paths experiment.

method. Since the average shortest path length between users in the network is 2:72, our experiment results show that our strategy is efficient to find almost shortest paths using local search with only local information.

Fig. 6 presents the relationship between path length and acquaintance probability between two users. Generally, lower acquaintance probability will cause longer paths. However, according to Figs. 5 and $^ { 6 , }$ no matter how small the acquaintance probability is, short paths still exist and can be found using local search strategy.

We study the changes of the similarity with the target and the node degree along some random chosen social referral chains. We found that the node degree along the referral chain is irregular while the similarity increases. Please refer to Fig. $^ { 1 7 }$ (in Appendix C, available in the online supplemental material) for details. Furthermore, we analyze the similarity change along the true shortest path. We search the shortest paths of 10;000 random selected pairs of source and target from the MIT data set by Dijkstra algorithm. The result shows that 63 percent relays associate with increasing similarity to the target, only 18 percent relays associate with decreasing similarity. The analysis implies the reasonableness of our similarity bias strategy.

# 4.3.3 Performance with Real World Consideration

There are some existing shortest referral path search experiments in real world. We notice an interesting phenomenon here: the median path length of our search strategy is similar as the well-known small world experiments conducted by Travers and Milgram [9] and Dodds et al. [10]. It implies that the online social network Facebook describes the acquaintance relationship of the real world social network to some extent. However, the success rate of the small world experiments is very low.

![](images/575ed22d61875fd4ba94123cc15b35eb7ca341c43732dba95f8d095ce16c8247.jpg)



Fig. 6. The relationship between path length and acquaintance probability.

![](images/37ddbd40db1188166d05ba72fd6274533d8b9ae10e0a77ffb9a6b8dc4ccd22f6.jpg)



Fig. 7. The successful rate of MaxSim and High Degree search of 1,000 random request with different attrition rate.

In experiment conducted by Travers and Milgram [9], some people are able to construct short chains comprising an average of approximately five intermediaries, but 80 percent people in their experiments never reached the target. And in the most recently repeated small world experiment, conducted by Dodds et al. [10] those completed chains were only four hops long, but only 0:4 percent of about 24,000 chains that started (a total of 384) reached their targets. Most paths were terminated because some participants drop the message instead of relaying messages. In Travers and Milgram’s experiment, chains were observed to terminate with probability 0:25. We therefore conduct a more realistic search experiment with an attrition rate at each step of the chain construction. The attrition rate indicates the probability a participant terminates the chain. We randomly select 1,000 pairs of source and target. Figs. 7 and 8 illustrate the successful rate and chain length of the high degree search strategy and our high similarity search strategy. The increase of attrition rate courses great decrease of success rate. When the attrition rate is 0:25 which are consistent with Milgram’s experiment, the success rate is only 17 percent for high degree strategy, while it is 25 percent for our high similarity strategy which is 5 percent higher than the Milgram’s result. Moreover, a much shorter mean length is achieved with an attrition rate. The mean path length is 3:5

![](images/ef4ed91badb4b803dc11d11cce421bcc2a3f8ba3d3b5eac99403e659ff834d3a.jpg)



Fig. 8. The path length of MaxSim and High Degree search of 1,000 random request with different attrition rate.

TABLE 2 Search Performance of Three Mechanisms 

<table><tr><td colspan="4">Uniform distribution of costs</td></tr><tr><td>mechanism</td><td>mean length</td><td>median length</td><td>success rate</td></tr><tr><td>MaxSim</td><td>11.4</td><td>5</td><td>89%</td></tr><tr><td>SumScore</td><td>14.3</td><td>6</td><td>82%</td></tr><tr><td>ProdScore</td><td>26.5</td><td>19.5</td><td>68%</td></tr><tr><td colspan="4">Normal distribution of costs</td></tr><tr><td>mechanism</td><td>mean length</td><td>median length</td><td>success rate</td></tr><tr><td>MaxSim</td><td>11.4</td><td>5</td><td>89%</td></tr><tr><td>SumScore</td><td>15.1</td><td>6</td><td>87%</td></tr><tr><td>ProdScore</td><td>18.9</td><td>12</td><td>83%</td></tr></table>

when attrition rate is 25 percent compared to 24:6 without attrition and the median length also decreases to 3 which approaches to the true average shortest path length 2:72. The existing work and our experiments show that, the main course of the failure is that the participants are not sufficiently motivated. As a result, a payment mechanism is quite necessary for a successful search.

To be more realistic, we consider the situation that an urgent request is demanded while some users are not online. The result shows that when the offline users are less than 70 percent, the success rate and path length don’t deteriorate significantly. Please refer to Figs. 18 and 19 (in Appendix D, available in the online supplemental material) for details.

# 4.4 Search with a Payment Mechanism

In this section, we study the performance of our truthful mechanisms with payment. We consider two distributions of the real cost $c ^ { k } { : }$ the uniform distribution in the range 0; 100 ; the normal distribution with mean $\mu = 5 0$ and vari-½  ¼ance s 10. We compare the budgets with different cost ¼distributions of three search mechanisms:

1. Mechanism MaxSim: In the decision phase of each intermediate user, a neighbor with the maximum similarity to the target will be selected without considering the declared price, and the mechanism will pay the user her declared price. Observe that this mechanism is not truthful: every user could declare a price as high as she likes. We estimate the lowest budget of this untruthful mechanism by assuming that every user declares the true cost.   
2. Mechanism SumScore: This is our search mechanism presented in Section 3. The score function is $\eta ^ { k } =$ $\hat { d } ^ { k } + ( 1 - s _ { k , t } )$ .   
þ ð  Þ3. Mechanism ProdScore: This mechanism is similar to the mechanism presented in Section 3, except that the score function is: $\eta ^ { k } = d ^ { k } \times ( 1 - s _ { k , t } )$ . It is easy to ¼  ð  Þshow that this mechanism is also truthful, using techniques similar to that in Section 3.

# 4.4.1 Search Performance

We study the performance of these three different strategies by randomly selecting 100 pairs of initiators and targets from the MIT data set. Table 2 summarizes the measurement of these three different mechanisms. Mechanism Max-Sim is cost independent: it just tries to maximize the similarity. Mechanism MaxSim outperforms the other two in search. Mechanism SumScore performs a little worse than

![](images/89cd280c842f2742aab7f4f19c8fa7fae725ccbb2f7694532ec7d68516e1dbdc.jpg)



Fig. 9. The required budget versus different path length for three mechanisms with uniform cost distribution.

![](images/1219340b967840f504acd7e83ed7ef3dc58109f289042452cf2a7a7f871fb34f.jpg)



Fig. 10. The required budget versus different similarity for three mechanisms with uniform cost distribution.

![](images/011c1c9cd8580f2265da541d514b1b789dcf9901eadbb0ec16ae44d5685e9afd.jpg)



Fig. 11. The required budget versus path length for three mechanisms with normal cost distribution.

Mechanism MaxSim. Mechanism ProdScore performs the worst because its score function prefers nodes with smaller cost more than good similarity.

# 4.4.2 Budget Requirement

We investigate the cost and budget requirement with uniform distributed cost. Figs. 9 and 10 present the required budget of three mechanisms, i.e., the minimum payment needed for having a successful search.

We then study the cost and budget requirement with normal distributed cost. Figs. 11 and 12 present the required budget.

Table 3 shows the average cost per hop in the social referral chain found by mechanisms SumScore and Prod-Score. We found that mechanism ProdScore generates a lower average cost at the cost of losing some search efficiency. Since Mechanism MaxSim is cost independent, the lower bound of its average per-hop cost is the mean value 50 with both uniform and normal cost distributions. In fact, for any other cost-independent/untruthful mechanisms, e.g., high degree mechanism, the average per-hop cost is also at least 50.

![](images/e109d267eef816ba6d8824ac6bdf71c71ce1c4dbda7e65eb2ce8a6a427032440.jpg)



Fig. 12. The required budget versus different similarity for three mechanisms with normal cost distribution.

TABLE 3 Average Cost per-Hop for Mechanisms SumScore and ProdScore 

<table><tr><td colspan="4">Uniform distribution of costs</td></tr><tr><td>mechanism</td><td>declaration</td><td>bonus</td><td>total</td></tr><tr><td>SumScore</td><td>6.1</td><td>3.2</td><td>9.3</td></tr><tr><td>ProdScore</td><td>2.8</td><td>1.6</td><td>4.4</td></tr><tr><td colspan="4">Normal distribution of costs</td></tr><tr><td>mechanism</td><td>declaration</td><td>bonus</td><td>total</td></tr><tr><td>SumScore</td><td>32.3</td><td>3</td><td>35.3</td></tr><tr><td>ProdScore</td><td>28.9</td><td>2.5</td><td>31.4</td></tr></table>

The mechanism MaxSim has the best search performance, but requires a much larger budget, which could be potentially unbounded when users lie about their real cost. Mechanism SumScore creates shorter paths with higher cost, while mechanism ProdScore achieves small average cost per-hop, but often found longer paths. Both mechanisms SumScore and ProdScore can find cheap and short paths to the target and produce similar overall path cost. Mechanism SumScore has a higher success rate (i.e., waste less pay) and satisfies our optimization objective better. By Fig. 9, we notice that the budget isn’t proportional to the product of mean price and path length, which implies that if only there exist cheap short paths, our mechanism can find them. We also notice that the bonus will not incur significant extra pay, especially when the users’ costs follow normal distribution. Small bonus used in our mechanism does motivate users to declare their true cost.

# 5 RELATED WORK

Given a description of a desired expert, there are two kinds of expert finding methods without using payment: 1) global expert finding: finding a person or a group of ranked persons, similar enough to the desired one with global information; 2) distributed expert finding: searching a desired person via a chain of social referrals using local acquaintance information in a social network, e.g. the small world routing.

Global expert finding. This is usually based on a large database with global information and mainly focuses on linking humans to expertise areas (known as expertise retrieval). There are already some well-known large-scale online expert search systems like Spock and zoominfo. Some commercial expert search engines have been invested in companies like IBM and Microsoft. Some organization expert finding systems like [19] have studied knowledge management to utilize human knowledge within an organization as well as possible. Most research in this area focus on tracing, mining and organizing evidences of expertise, and linking the evidences to humans. Serdyukov and Hiemstra [20] designed schemes for expertise evidence finding outside a well organized database. They showed the importance of global web sources of expertise evidence for expert finding. Recently, social networks are also utilized to find professionals. Zhang et al. [21] proposed an approach to find the expertise by considering both personal information and relationship information with other experts. Lappas et al. [22] proposed to find a team of experts by considering the team formation problem in social networks. Balog et al. have done a lot of work about expertise retrieval [23] and provided a good overview of expertise retrieval in [24]. All these schemes fall into the category of global expert finding by using some global databases or central server and focus on expertise evidence mining and organization. Social networks play a role of furnishing expertise evidence through providing the friendships between persons.

There are also some work [25], [26], [27], [28], [29] use social feature to improve information routing and dissemination in social networks.

In this work, we focus on searching people with matching attributes in online social network in a distributed manner with only local information, which is also known as the small world routing problem. Finding evidence of expertise is not in the scope of this work.

Distributed expert finding (i.e., small world routing). The small world problem has been popular since forty years ago [30], which conducted experiments to prove that everyone is connected to everyone else via six degrees of separation. In [31], the small world problem was divided into topological problem and algorithmic problem. The topological problem is that for a randomly chosen pair of individuals, there exists, with a high probability, a “short” chain of intermediaries that connect them. Here short is usually interpreted as proportional to the logarithm of the population size. The algorithmic small world problem is that in order to locate a service provider, a person must actively traverse some chains of referrals. An individual need effectively navigate these short chains themselves, with every intermediate individual having only local knowledge (e.g., her own friends) of the social network.

Many research results were devoted to study various challenging algorithmic small world problems, e.g., [5], [17], [18], [32], [33], [34]. The base of these algorithms is selecting a successor by some greedy methods that optimize some metrics (e.g., degree, geography, social distance and profile similarity). Adamic et al. [17] introduced several local search strategies which utilize high degree nodes in power-law graphs. Wattes et al. [5] used the lowest common ancestor level in the social hierarchy as the similarity measurement between individuals. Adamic and Adar [18] did some simulated experiments on the email network and verified the models proposed by Watts et al.[5] and Kleinberg [32]. The email experiments explain why individuals are able to successfully complete chains in small world experiments using only local information. They also pointed out that in an online social network, where the data is incomplete and hierarchical structures are not well defined, local search strategies are less effective. The difficulty of the local search is also mentioned by Goel et al. [7], which states that the search distance in social networks is fundamentally different from topological distance, where the mean and median topological distances tend to be similar. Pairs of individuals who are already “close”, in the sense of sharing social, geographical, and demographic attributes, can find each other, but distant pairs cannot.

These efforts focus on designing and analyzing local search algorithms to find short paths, with a hypothesis that people will participate voluntarily. It has been well documented that in the small world experiments a vast majority of paths never reach their ultimate targets [7]: most paths were terminated because participants are not sufficiently motivated to relay messages. Thus, we need design a truthful mechanism that takes into account not only the participation cost of intermediate users, but also the selfish nature of these intermediate users.

# 6 DISCUSSION AND CONCLUSION

In this work, we addressed the local social referral problem in a large scale social network by taking users’ self-interests into consideration and designed a truthful mechanism that reduces the length of social referral chain, reduces the cost of social referrals, and improves the success rate, compared with previous efforts. There are several interesting questions not fully studied in this work. For example, we are designing some privacy mechanisms to protect the desired expert of the initiator and the attributes of all the participants. For example, [35], [36], [37], [38], [39]. We need to design a truthful mechanism when the initiator wants to find a target expert within certain hop distance, while tolerating the possibility of multiple experts were found by multiple social referral paths. We also need to design the mechanism to find a group of required experts who are well related. It is still challenging to estimate the path length and budget for the initiator.

# ACKNOWLEDGMENTS

The research was supported in part by NSFC Major Program 61190110, National High-Tech R&D Program of China (863) under grant No. 2011AA010100, and China 973 Program under grant No.2011CB302705. The research of Xiang-Yang Li was partially supported by National Science Foundation (NSF) CNS-0832120, NSF CNS-1035894, NSF ECCS-1247944, NSFC Program under Grant No. 61170216, No. 61228202, China 973 Program under Grant No.2011CB302705. Any opinions, findings, conclusions, or recommendations expressed in this paper are those of author(s) and do not necessarily reflect the views of the funding agencies (NSF, and NSFC). The research of Jingsheng Lei was supported by

NSFC Program under Grant No. 61272437, No.61073189, Innovation Program of Shanghai Municipal Education Commission (No. 13ZZ131) and Foundation Key Project of Shanghai Science and Technology Committee (No. 12JC1404500).

# REFERENCES

[1] B.M. Evans, S. Kairam, and P. Pirolli, “Do Your Friends Make You Smarter?: An Analysis of Social Strategies in Online Information Seeking,” Information Processing & Management, vol. 46, no. 6, pp. 679-692, 2010.   
[2] D.W. McDonald, “Recommending Collaboration with Social Networks: A Comparative Evaluation,” Proc. ACM SIGCHI Conf. Human Factors in Computing Systems (SIGCHI), 2003.   
[3] H. Kautz, B. Selman, and M. Shah, “Referral Web: Combining Social Networks and Collaborative Filtering,” Comm. ACM, vol. 40, no. 3, pp. 63-65, 1997.   
[4] M. McPherson, L. Smith-Lovin, and J.M. Cook, “Birds of a Feather: Homophily in Social Networks,” Annual Rev. of Sociology, vol. 27, pp. 415-444, 2001.   
[5] D.J. Watts, P.S. Dodds, and M.E. Newman, “Identity and Search in Social Networks,” Science, vol. 296, no. 5571, pp. 1302-1305, 2002.   
[6] J. Guare, Six Degrees of Separation. Dramatists Play Service, Inc., 1992.   
[7] S. Goel, R. Muhamad, and D. Watts, “Social Search in Small-World Experiments,” Proc. ACM 18th Int’l Conf. World Wide Web (WWW), 2009.   
[8] H.C. White, “Search Parameters for the Small World Problem,” Social Forces, vol. 49, no. 2, pp. 259-264, 1970.   
[9] J. Travers and S. Milgram, “An Experimental Study of the Small World Problem,” Sociometry, vol. 32, pp. 425-443, 1969.   
[10] P.S. Dodds, R. Muhamad, and D.J. Watts, “An Experimental Study of Search in Global Social Networks,” Science, vol. 301, no. 5634, pp. 827-829, 2003.   
[11] L. Zhang, X.-Y. Li, Y. Liu, Q. Huang, and S. Tang, “Mechanism Design for Finding Experts Using Locally Constructed Social Referral Web,” Proc. IEEE INFOCOM, 2012.   
[12] W. Wang and X.-Y. Li, “Low-Cost Routing in Selfish and Rational Wireless Ad Hoc Networks,” IEEE Trans. Mobile Computing, vol. 5, no. 5, pp. 596-607, May 2006.   
[13] M.I. Jordan, “Why the Logistic Function? A Tutorial Discussion on Probabilities and Neural Networks,” Technical Report 9503 Massachusetts Institute of Technology, 1995.   
[14] M.E. Newman, “Ego-Centered Networks and the Ripple Effect,” Social Networks, vol. 25, no. 1, pp. 83-95, 2003.   
[15] A.L. Traud, E.D. Kelsic, P.J. Mucha, and M.A. Porter, “Comparing Community Structure to Characteristics in Online Collegiate Social Networks,” SIAM Rev., vol. 53, pp. 526-543, 2011.   
[16] A.L. Traud, P.J. Mucha, and M.A. Porter, “Social Structure of Facebook Networks,” arXiv:1102.2166, 2011.   
[17] L.A. Adamic, R.M. Lukose, A.R. Puniyani, and B.A. Huberman, “Search in Power-Law Networks,” Physical Rev. E, vol. 64, no. 4, p. 046135,2001.   
[18] L. Adamic and E. Adar, “How to Search a Social Network,” Social Networks, vol. 27, no. 3, pp. 187-203, 2005.   
[19] T. Reichling, M. Veith, and V. Wulf, “Expert Recommender: Designing for a Network Organization,” Computer Supported Cooperative Work, vol. 16, no. 4/5, pp. 431-465, 2007.   
[20] P. Serdyukov and D. Hiemstra, “Being Omnipresent to be Almighty: The Importance of the Global Web Evidence for Organizational Expert Finding,” Proc. ACM SIGIR Workshop Future Challenges in Expertise Retrieval, 2008.   
[21] J. Zhang, J. Tang, and J. Li, “Expert Finding in a Social Network,” Proc. Advances in Databases: Concepts, Systems and Applications: 12th Int’l Conf. Database Systems for Advanced Applications, 2007.   
[22] T. Lappas, K. Liu, and E. Terzi, “Finding a Team of Experts in Social Networks,” Proc. 15th ACM SIGKDD Int’l Conf. Knowledge Discovery and Data Mining (SIGKDD), 2009.   
[23] K. Balog, M. De Rijke, and W. Weerkamp, “Bloggers as Experts: Feed Distillation Using Expert Retrieval Models,” Proc. 31st Ann. Int’l ACM SIGIR Conf. Research and Development in Information Retrieval (SIGIR), 2008.   
[24] K. Balog, Y. Fang, M. de Rijke, P. Serdyukov, and L. Si, “Expertise Retrieval,” Foundations and Trends in Information Retrieval, vol. 6, pp. 127-256, 2012.

[25] E. Bulut and B. Szymanski, “Exploiting Friendship Relations for Efficient Routing in Mobile Social Networks,” IEEE Trans. Parallel and Distributed Systems , vol. 23, no. 12, pp. 2254-2265, Dec. 2012.   
[26] Y. Wang, W.-S. Yang, and J. Wu, “Analysis of a Hypercube-Based Social Feature Multi-Path Routing in Delay Tolerant Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 24, no. 9, pp. 1706- 1716, Sept. 2013.   
[27] S. Wen, W. Zhou, J. Zhang, Y. Xiang, W. Zhou, and W. Jia, “Modeling Propagation Dynamics of Social Network Worms,” IEEE Trans. Parallel and Distributed Systems, vol. 24, no. 8, pp. 1633- 1643, Aug. 2013.   
[28] J. Fan, J. Chen, Y. Du, W. Gao, J. Wu, and Y. Sun, “Geo-Community-Based Broadcasting for Data Dissemination in Mobile Social Networks,” IEEE Trans. Parallel and Distributed Systems , vol. 24, no. 4, pp. 734-743, Apr. 2013.   
[29] S.-J. Tang, J. Yuan, X. Mao, X.-Y. Li, W. Chen, and G. Dai, “Relationship Classification in Large Scale Online Social Networks and Its Impact on Information,” Proc. IEEE INFOCOM, 2011.   
[30] S. Milgram, “The Small World Problem,” Psychology Today, vol. 2, no. 1, pp. 60-67, 1967.   
[31] D.J. Watts and S.H. Strogatz, “Collective Dynamics of Small-World Networks,” Nature, vol. 393, no. 6684, pp. 440-442, 1998.   
[32] J. Kleinberg, “The Small-World Phenomenon: An Algorithm Perspective,” Proc. 32nd Ann. ACM Symp. Theory of Computing (STOC), 2000.   
[33] J.M. Kleinberg, “Navigation in a Small World,” Nature, vol. 406, no. 6798, pp. 845-845, 2000.   
[34] O. Simsek and D. Jensen, “Decentralized Search in Networks Using Homophily and Degree Disparity,” Proc. 19th Int’l Joint Conf. Artificial Intelligence (IJCAI), 2005.   
[35] L. Zhang, X.-Y. Li, Y. Liu, and T. Jung, “Verifiable Private Multi-Party Computation: Ranging and Ranking,” Proc. IEEE INFOCOM, 2013.   
[36] T. Jung, X. Mao, X.-Y. Li, S. Tang, W. Gong, and L. Zhang, “Privacy-Preserving Data Aggregation Without Secure Channel: Multivariate Polynomial Evaluation,” Proc. IEEE INFOCOM, 2013.   
[37] X.-Y. Li and T. Jung, “Search Me if You Can: Privacy-Preserving Location Query Service,” Proc. IEEE INFOCOM, 2013.   
[38] T. Jung, X.-Y. Li, Z. Wan, and M. Wan, “Privacy Preserving Cloud Data Access with Multi-Authorities,” Proc. IEEE INFOCOM, 2013.   
[39] L. Zhang, X.-Y. Li, and Y. Liu, “Message in a Sealed Bottle: Privacy Preserving Friending in Social Networks,” Proc. IEEE Int’l Conf. Distributed Computing Systems (ICDCS), 2013.

![](images/79c6de0b441a26e1638cc6149c234e275463e6d6659ae1d764252956e62d64eb.jpg)



Lan Zhang received the bachelor’s degree in 2007 from School of Software at Tsinghua University. She is currently working toward the PhD degree in the Department of Computer Science and Technology, Tsinghua University, Beijing, China. Her research interests span social networks, privacy, secure multi-party computation and mobile computing, etc. She is a student member of the IEEE

![](images/2dc1ae4daae932976e3b7280f613fa18e9d7d23bb2fc779d197d2897f99bf906.jpg)



Xiang-Yang Li received the bachelor’s degree from the Department of Computer Science and the bachelor’s degree from the Department of Business Management from Tsinghua University, P.R. China, both in 1995. He received the MS degree in 2000 and the PhD degree in 2001 from the Department of Computer Science, University of Illinois at Urbana-Champaign. He is a professor at the Illinois Institute of Technology. He received the China National science Foundation (NSF) Outstanding Overseas Young Researcher (B). He published a monograph Wireless Ad Hoc and Sensor Networks: Theory and Applications. He coedited several books, including, Encyclopedia of Algorithms. His research interests include mobile computing, cyber physical systems, wireless networks, security and privacy, and algorithms. He is an editor of several journals, including IEEE Transaction on Parallel and Distributed Systems, IEEE Transaction on Mobile Computing. He is a senior member of the IEEE and a member of the ACM.

![](images/f7d849d202c6e1cddca0c58d97262b73b60ec0d58c858b04daf446e2b9788d92.jpg)



Jingsheng Lei received the BS degree in mathematics from Shanxi Normal University in 1987, and the MS and PhD degrees in computer science from Xinjiang University in 2000 and 2003, respectively. He is a professor and the dean of the College of computer science and technology, Shanghai University of Electronic Power. He has wide research interests, mainly including machine learning, data mining, pattern recognition and cloud computing. In these areas, he has published more than 80 papers in international journals or conferences. He serves as an editor-in-chief of the journal of computational information systems. He is the member of the Artificial Intelligence and Pattern Recognition Technical Committee of the China Computer Federation (CCF), member of the Machine Learning Technical Committee of the Chinese Association of Artificial Intelligence (CAAI), and member of the Academic Committee of ACM Shanghai Chapter.

![](images/0612250d4c4e8b1d0904f191c98f21db98a3772bc9e8fd8facc0e7b4f56eb9d2.jpg)



Jiaguang Sun received the graduate degree from the Department of Automation, Tsinghua University in 1970. He is the dean of School of Information Science and Technology and School of Software, Tsinghua University. He assumed the post of director at Tsinghua National Lab for Information Science and Technology (TNLIST). He is also the president of Executive Council of China Engineering Graphics Society and the vice president of National Natural Science Foundation of China. He has engaged in the research and teaching of computer graphics, computer aided design and computer aided management since 1975. He received the Science and Technology Development Awards 15 times awarded by the Nation and the Ministry. He has published many academic papers and also published four books as the first author. He is a member of the Chinese Academy of Engineering.

![](images/3340a8873373817867d99de3be3c7a937510ad8e68cfefb8e4a26dfc53609731.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is currently a Cheung Kong professor at Tsinghua University, as well as a faculty member with the Hong Kong University of Science and Technology. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a

senior member of the IEEE.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.