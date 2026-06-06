# Popularity adaptive search in hybrid P2P systems

Xiaoqiu Shi a,∗, Jinsong Han b, Yunhao Liu b, Lionel M. Ni b

a Department of Computer Science, Wenzhou University, Zhejiang, China

b Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong

# a r t i c l e i n f o

Article history:

Received 9 June 2007

Received in revised form

19 September 2008

Accepted 23 September 2008

Available online 17 October 2008

Keywords:

Hybrid peer-to-peer

Flooding

DHT

Dynamic

Content popularity

# a b s t r a c t

In a hybrid peer-to-peer (P2P) system, flooding and DHT are both employed for content locating. The decision to use flooding or DHT largely depends on the population of desired data. Previous works either use local information only, or do not consider dynamic factors of P2P systems. In this paper, we propose a Popularity Adaptive Search method for Hybrid (PASH) protocol. By dynamically estimating the content popularity, PASH properly selects search methods so as to efficiently saves query traffic cost and response time. We evaluate PASH through synthetic and trace-driven simulations. The results show that PASH outperforms existing approaches and it also scales well.

© 2008 Published by Elsevier Inc.

# 1. Introduction

Since the emergence of Napster [17] in 1999, the Peer-to-Peer (P2P) model has been increasingly popular along with deployment in file sharing, distributed directory service, web cache, storage and grid computing [8,11,18,25,26,28,29,27]. Many P2P systems report huge numbers of simultaneously active participants, with millions, if not billions, of participating machines. Those participants include home PCs as well as enterprise computers. They are called peers or servants, each acting as both a server and/or a client.

P2Ps used to be classified as centralised, decentralised structured, and decentralised unstructured [15] models. Centralised models, such as Napster, have a constantly-updated directory hosted at central locations. The main drawback of centralised models is the vulnerability to single point failure. Decentralised unstructured P2P systems, such as Gnutella [4] and KaZaA [5], eliminate a centralised directory and employ flooding-based search techniques. Although flooding-based search is effective for locating popular items, it often performs poorly in search latency and result quality when queries are focused on rare items. This is because a flooding-based search sometimes fails to return matches of desired data due to the partial coverage problem of flooding scope. As an alternative, decentralised structured models, such as Chord [23], CAN [19], Pastry [20], and Tapestry [7], are proposed. In those systems, P2P topology is highly organised and files are placed at specified locations based on Distributed Hash Tables (DHT), which make the queries for rare items easier to answer. Fig. 1 makes a comparison between the flooding-based and DHTbased search.

To improve search quality and efficiency for both popular and rare items, hybrid P2P approaches are introduced [13,14]. By combining the unstructured P2Ps with a structured DHT-based global index, queries are handled in a hybrid manner: popular items are found via flooding, while rare items are found via a DHT-based algorithm. The major challenge in Hybrid P2Ps is how to identify rare items in a decentralised and self-organised environment.

Many efforts have been made for hybrid searches, such as the SimpleHybrid [13,14] and GAB [30]. However, they do not successfully deal with the dynamic nature of P2P networks where peers frequently join and leave the systems. Aiming at improving the hybrid search in dynamic environments, we propose a Popularity Adaptive Search for Hybrid P2P (PASH). PASH employs a network dynamic sensing infrastructure and uses the results to guide/adjust the search decision-making. We evaluate PASH through synthetic and trace-driven simulations and contrast it with a most recent work GAB [30]. The results show that PASH outperforms existing approaches in terms of both query traffic cost and search response time.

The rest of the paper is organised as follows: Section 2 presents the related work. Section 3 discusses the major challenges in

![](images/d7733e27a21bca4e2cfa3434c42a83bbfb354e2f7c89e629c5b61ad70c8ff156.jpg)



□Requesting Node·Nodes with iteml △ Nodes with item2   
(a) Flooding based search.

![](images/a0440c6aeda60d39bf3c05d3d5efba35b3b6e41c336fb3f05676cba0ee0211e7.jpg)



---> Flooding Queries Flooding Scope →DHT Queries   
(b) DHT based search.

Fig. 1. Comparison for flooding with DHT-based search. Flooding is effective in searching popular items (only 1 hop needed to find item1), but performs poorly for rare items (5 hops needed to find item2). In contrast, DHT is efficient to find the rare items, while the maintenance of DHT is costly.

current hybrid P2Ps. Section 4 proposes our PASH approach. We describe the simulation methodology in Section 5 and present performance evaluation on PASH in Section 6. We conclude this work in Section 7.

# 2. Related work

A spectrum of approaches has been proposed to improve search quality and efficiency in decentralised P2P systems, such as DHT, flooding, topology optimisation and hybrid search.

DHT-based search techniques [23,19,20,7] have been widely studied. An overview of DHT-based search approaches can be found in [1]. In such a scheme, items are inserted into a distributed hash table and found by specifying their unique keys. To efficiently implement a DHT, the DHT-based search algorithm must be able to determine which node is responsible for storing the item associated with the given key and then map the keys to nodes in a load-balanced manner. Meanwhile, each node needs to maintain a routing table based on the DHT overlay to forward messages and lookup items.

Flooding-based approaches are widely deployed in practical decentralised and unstructured P2P systems such as Gnutella. In those systems, peers are interconnected in an ad-hoc pattern, and queries are flooded in P2P overlays. To make Gnutella-like networks scalable, a random walk based search algorithm [15] is introduced. GIA [2] modifies the k-walker algorithms and includes flow control, dynamic topology adaptation, and one-hop replication to handle the problem of nodes’ heterogeneity. In [31], authors proposed a popularity biased algorithm to enhance the efficiency of random walk based search. In each step of queries’ random walks, the next destination is determined based on the content popularities of current peer’s neighbours.

Since Gnutella-like P2P is effective for locating highly replicated items but reluctant to find rare ones, a hybrid search infrastructure, SimpleHybrid, is proposed. SimpleHybrid combines Gnutella and the DHT-based PIERSearch [13,14]. To improve the search efficiency, GAB [30] makes search decisions based on global statistics of documents’ popularity (In this paper, we will use the terms of ‘‘item’’ and ‘‘document’’ interchangeably.). GAB outperforms SimpleHybrid by using a gossip algorithm to make popularity-biased search possible. However, global statistics of documents’ popularity obtained from gossip in GAB do not well reflect the dynamic characteristic of peers’ frequently joining and leaving. This leads to unnecessary flooding or inappropriate document publishing in DHT.

Recently, topology optimisation has gained increasing concerns. For P2P systems, optimising the network topology can improve search efficiency according to the network performance. Liu et al. [12] optimise the topology by addressing the mismatch topologies between P2P overlay and the underlying network. The authors in [10,9] focus on the topology optimisation challenge in wireless P2P environments and propose an application-driven topology control algorithm to improve the node fairness and energy efficiency. The topology optimisation and PASH may complement each other to contribute an optimal search infrastructure. The advantages of topology optimisation approaches include adaptive neighbouring node selection and efficient search overlay construction. Different from topology optimisation approaches, PASH constructs a smart node overlay aiming at sensing item dynamic rate in the network. In practice, we can first implement the topology optimisation to construct an efficient P2P overlay, and then conduct PASH to achieve popularity adaptive search. We believe that the combination of the topology optimisation scheme and PASH will further improve the search efficiency in both the wired and wireless environments.

# 3. Challenging issues in popularity based search

In hybrid P2P systems, different heuristics have been used to identify which items are rare or popular, such as search frequency of keywords, keyword pair frequency, searching result size history, sampling of neighbouring nodes, and historical statistics on item replicas [30]. For example, in [13,14], a query is flooded with a limited depth first, and, if no result is returned, the query goes to the DHT. Such a design is simple and effective but inefficient in that it incurs extra overhead. It also increases the response time when searching rare documents and wastes bandwidth due to unfruitful flooding.

The most recent work is GAB [30]. In the design of GAB, when a node receives a document title it has not indexed before, it tosses a coin up to k times and counts the number of heads before the first tail appears. It stores this value of this title and then exchanges it with other nodes by gossip to compute a maximum value. As a result, the maximum value of this title can be represented the popularity of this document. Thus, a more widely replicated document would have a larger popularity value.

Each node maintains a histogram of the popularity values of the documents it holds and a flooding threshold. When a peer would like to issue a query with a set of keywords, it first seeks the popularity values for that set of keywords and then compares them with the flooding threshold to determine the search selection.

Our observations show that GAB is effective when peers are stable and active in a long run, for example, acting as the ultrapeers. In most P2P systems, however, not all ‘‘normal’’ hosts have as long expected uptimes as ultrapeers and they leave or join the P2P network randomly. The study in [21] shows that in Gnutella about half of the peers in the system are replaced by newcomers within one hour. Under a dynamic environment, as shown in Fig. 2, popularity computed from GAB does not reflect the snapshot of resources’ replication in P2P networks well.

![](images/5b730eb1415ece9604a0176c6833442a0590784d5ecb4e8dda0f623ce5dedfab.jpg)



(a) Nodes leave with replicas lost.

![](images/20f79ee38851be6b8a7e41129a74d7931a11584c8c0872971d0ce204329b05ef.jpg)



(b) Nodes join with replicas added.

Fig. 2. Without considering the dynamic feature, gossip-obtained popularity values are not accurate in P2P environments.   
![](images/4312715b85f7d18cff108696013c3f972cb516d9524261d20c3cfac57bcb42f7.jpg)



(a) When n > 1.

![](images/2ebb628fa195e5b5167101164707227a7aad76082f34f3085e3eb679afbd0ac9.jpg)



(b) When n < 1.   
Fig. 3. Utility decline.

Our analysis below will show that the statistic of item replicas in GAB is always a monotone increasing function of the gossip rounds.

Let θ denote a round of gossip, vi (θ ) is replicas statistics of item i in gossip round θ and vij is the popularity value of item i from node j. In GAB, for all $v _ { i } \left( \theta \right)$ and θ , we have Eqs. (1) and (2).

$$
v _ {i} (\theta) = v _ {i} (\theta - 1) \forall v _ {i j} = \left\{ \begin{array}{l l} v _ {i} (\theta - 1) & \text { if } v _ {i} (\theta - 1) > v _ {i j} \\ v _ {i j} & \text { if } v _ {i} (\theta - 1) <   v _ {i j} \end{array} \right. \tag {1}
$$

$$
\Delta v _ {i} = v _ {i} (\theta) - v _ {i} (\theta - 1) = \left\{ \begin{array}{l l} 0 & \text { if   } v _ {i} (\theta - 1) > v _ {i j} \\ > 0 & \text { if   } v _ {i} (\theta - 1) <   v _ {i j}. \end{array} \right. \tag {2}
$$

Obviously, the statistics of replicas in GAB will remain unchanged or increase even though there is a decrease in item replicas because of node departure. Indeed, under a dynamic environment, GAB statistics are far from accurate.

Inaccurate popularity values may lead to wrong search decisions and degrade the search efficiency. Let η denote the ratio of the real popularity value of an item to the popularity value obtained from gossip. While the latter value is less than the former one, $\eta > 1 ;$ otherwise, $\eta < 1$ .

If the flooding threshold is set at $T _ { f } ,$ , when η > 1, queries for the items whose real popularity values are within the interval [Tf , ηTf ] would be incorrectly published to DHT, because their gossipobtained popularity values are among $[ T _ { f } / \eta , T _ { f } ]$ . On the other hand, when $\eta \ < \ 1$ , queries for the items whose real popularity values are within the interval $[ \eta T _ { f } , T _ { f } ]$ would be incorrectly flooded since their gossip-obtained popularity values are within the interval $[ T _ { f } , T _ { f } / \eta ]$ .

Both situations would result in a decline of the search performance described by Eqs. (3) and (4). Fig. 3 plots the integrated metric, utility function $U ( p _ { i } )$ , where p is the popularity value for item i, proposed by the authors of GAB [30] and shows the performance decline when $\eta > 1$ and $\eta < 1$ .

$$
\Delta U _ {1} = \sum_ {p _ {i} = T _ {f}} ^ {\eta T _ {f}} \left[ U _ {D H T} (p _ {i}) - U _ {f l o o d} (p _ {i}) \right] <   0, \quad \eta > 1 \tag {3}
$$

$$
\Delta U _ {2} = \sum_ {p _ {i} = \eta T _ {f}} ^ {T _ {f}} \left[ U _ {\text { flood }} (p _ {i}) - U _ {D H T} (p _ {i}) \right] <   0, \quad \eta <   1. \tag {4}
$$

Motivated to achieve a flexible hybrid P2P search mechanism that can work well in dynamic environment, we propose PASH, a hybrid search method which adaptively adopts the dynamic of items’ popularities, to improve the search accuracy and efficiency.

# 4. PASH design

In PASH, the popularity value of an item is computed based on historical statistics on item replicas as well as their dynamics information. In PASH, all nodes perform the gossip algorithm as described in GAB to collect the global popularity information about item replicas. PASH, however, designates a set of ‘‘smart nodes’’ as sensing nodes to detect the network dynamic rate. The sensing results are distributed to all PASH nodes and used to tune the popularity values. Such an adjustment results in more accurate items’ popularities. The working flow of PASH is shown in Fig. 4.

Now we define the systems parameters of PASH. Given that there are R replicas for all the items, and $R _ { i }$ replicas for item i in the P2P system. Thus, $\sum R _ { i } = R$ . We define

(1) $\beta _ { i } ,$ the dynamic rate of the item i’s replicas per time unit:

$$
\beta_ {i} = \frac {1}{R _ {i}} \frac {d R _ {i}}{d t}. \tag {5}
$$

(2) β, the dynamic rate of the replicas of all items per time unit:

$$
\beta = \frac {1}{R} \frac {d R}{d t}. \tag {6}
$$

In general, nodes randomly join and leave the P2P systems. Accordingly, the dynamic of those joining or leaving nodes would have even influences on replicas dynamics of different items. It means that in decentralized P2P, we can use the β to approximate to the β . Let C denote the number of items that a node can provide to share. We assume that

• at time t, there are $\lambda _ { 1 }$ node with $C _ { 1 } , \lambda _ { 2 }$ node with $C _ { 2 } , \ldots , \lambda _ { j }$ node with $C _ { j } , \ldots , \lambda _ { u }$ node with $C _ { u } ,$ , respectively, where $\textstyle \sum _ { j = 1 } ^ { u } \lambda _ { j } = n$ and $\textstyle \sum _ { j = 1 } ^ { u } \lambda _ { j } C _ { j } = R$ .

![](images/26722bd17e6c4707b3c0fdef90b0943c655fb1d511257a5388c972edc033d8ce.jpg)



Fig. 4. Flooding/DHT determination in PASH.

• in the time period ∆t, there are $\varDelta \lambda _ { 1 }$ nodes with $C _ { 1 } , \varDelta \lambda _ { 2 }$ nodes with $C _ { 2 } , \ldots , \varDelta \lambda _ { j }$ nodes with $C _ { j } , \ldots , \varDelta \lambda _ { u }$ nodes with $C _ { u }$ leaving the system. Meanwhile, there are $\xi _ { 1 }$ nodes with $C _ { 1 } , \xi _ { 2 }$ nodes with $C _ { 2 } , \ldots , \xi _ { i }$ nodes with $C _ { i } , \ldots , \xi _ { v }$ nodes with $C _ { v }$ joining the system. The distribution of nodes’ joining or leaving is statistically homogeneous.   
• at time $t + \Delta t ,$ there are $n ^ { \prime }$ nodes in the system, where $n ^ { \prime } =$ $\begin{array} { r } { n - \sum _ { j = 1 } ^ { u } \varDelta \lambda _ { j } + \sum _ { i = 1 } ^ { v } \xi _ { i } . } \end{array}$ .

Thus, we derive Eq. (7) from above assumptions.

$$
\begin{array}{l} \beta = \frac {\Delta R}{R \Delta t} = \frac {k \sum_ {i = 1} ^ {v} C _ {i} \xi_ {i} - \sum_ {j = 1} ^ {u} C _ {j} \Delta \lambda_ {j}}{\left(\sum_ {j = 1} ^ {u} C _ {j} \lambda_ {j}\right) \Delta t} \\ = \frac {1}{R \Delta t} \left(k \sum_ {i = 1} ^ {v} C _ {i} \xi_ {i} - \sum_ {j = 1} ^ {u} C _ {j} \Delta \lambda_ {j}\right), \quad 0 \leq k \leq 1. \tag {7} \\ \end{array}
$$

If the item set introduced by newly joined nodes is totally different from the existing items in the P2P system, $k = 0$ . That is, the item set of newly joined nodes has no overlap with the item set of existing nodes. If the newly joined nodes do not introduce new items, $k = 1$ . Normally, k would be a value between zero and one according to the overlap ratio.

Suppose that the statistics value of item i’s replicas, $v _ { i } ~ ( \theta ) ,$ , is computed using the gossip algorithm at time $t + \varDelta t _ { 0 } .$ . At time $t + \Delta t$ $( \varDelta t _ { 0 } < \varDelta t )$ , we expect that PASH is able to tune this value with a parameter γ to better reflect the real item replicas in the system. Then we have:

$$
v _ {i} (\theta) \leftarrow v _ {i} (\theta) \cdot \gamma , \quad \text { where } \gamma = 1 + \beta (\Delta t - \Delta t _ {0}).
$$

We also need to compute $\eta ,$ the ratio of the real popularity value to the gossip-obtained popularity value, i.e. $\eta \ : = \ : \gamma \ : \times \ : n / n ^ { \prime }$ . It is difficult, if not impossible, to measure the accurate $\eta \ : 0 \Gamma \gamma$ in a real P2P system. Therefore, our later discussion will focus on how to estimate η and $\gamma ,$ and then use the values select a search pattern.

# 4.1. Node type and message type

In PASH, all nodes are divided into three groups: smart nodes, backup smart nodes, and lazy nodes. Smart nodes act as sensors to detect the dynamic of item popularity in the system. Each of them maintains a host list, SmartNodes List, and a list of the monitored nodes as well as the global replica dynamic rate $\beta _ { g }$ and the local replica dynamic rate $\beta _ { l } .$ . Backup smart nodes are candidates for smart nodes, maintaining a host list and $\beta _ { g }$ as well. The others are lazy nodes. Each node whether it is a smart, backup smart or lazy one maintains the information of the smart node it belongs to.

In the Gnutella 0.6 [6], byte 15 of the GUID field is reserved. We utilize the first two bits of this byte to identify the node’s type, where ‘‘00’’ means lazy, ‘‘01’’ means backup smart, and $" 1 0 "$ $\tt o r  ^ { \alpha } { } ^ { \ -- } 1 1 ^ { \prime \prime }$ means smart. Furthermore, $" 1 0 "$ means a smart node is $" \mathrm { i d l e } "$ and $" 1 1 "$ means a smart node is ‘‘busy’’. When a smart node is capable of monitoring extra nodes, it marks itself as ‘‘idle’’, otherwise as ‘‘busy’’. Each node marks its neighbours as ‘‘smart’’, ‘‘backup smart’’, or ‘‘lazy’’. For a smart node, the third bit of byte 15 in GUID field is used as a ‘‘calculating bit’’. The default value of this bit is set to $\ " { } _ { \mathrm { 0 } } \cdot \{ \mathbf { \Gamma } _ { \mathrm { ~ \tiny ~ A ~ O ~ } } \}$ .

To reduce the traffic cost, we further modified the PING/PONG messages of Gnutella 0.6 protocol to piggyback the dynamics information of the system. We present the modified PING/PONG messages in Fig. 5. All types of PONG message have a ‘‘sensor’’ field to indicate to which smart node the responding node belongs.

One key issue here is how many smart nodes we need to deploy in the P2P system. An obvious tradeoff is that too many smart nodes incur unnecessary overhead and too few might lead to inaccuracy. We need to consider the size of the P2P system, computational capability of each node, sensing coverage, expected sensing accuracy, and acceptable traffic overhead, etc. In PASH, we select a proper ratio of the number of smart nodes to the number of all nodes through experiments, and we have more discussions on this issue in Section 5.

Each smart node maintains a SmartNodes List. It includes a number of other smart nodes. When initialising, a smart node creates its SmartNodes List from its host list. All smart nodes construct a mesh, as illustrated in Fig. 6. A smart node would utilise the information of ‘‘sensor’’ field in the received PONG messages. For example, a smart node S receives a PONG message, in which the ‘‘sensor’’ field has indicated a node U is a smart node but not included in S’s local SmartNodes List. The node S will try to contact node U. If node U is active, node S includes U into its SmartNodes List. In this way, smart nodes can expand their SmartNodes Lists. As an option, SmartNodes List could be implemented as a subset of the host list in order to reduce the storage cost.

# 4.2. Smart node selection

Suppose the P2P system has n nodes. Among them, there are x smart nodes. PASH thereby sets the probability of a node becoming a smart node to $x / n .$ .

When a fresh node joins the system, it obtains a host list from the bootstrapping node. Those nodes will become its neighbouring nodes. We define the smart node selection threshold as $p = s \times$ $( x / n )$ , where s is the number of a fresh node’s neighbours. $\mathrm { I f } p < 1$ , the fresh node acts as a lazy node. Now we consider the situation of $p > = 1$ . For the fresh node, we assume the number of smart nodes in its neighbours is q, and the number of backup smart nodes is $r .$ The fresh node determines whether it can act as a smart by comparing p, q and r. If $p > q$ , it becomes a smart node; i $\dot { p } < q$ and $p > r ,$ it becomes a backup smart node; If $p \ < \ q$ and $p \ < \ r ,$ the fresh node becomes a lazy node.

When a smart node leaves the system normally, it selects a backup smart node from its host list as its successor. The smart node then transfers the list of the monitored nodes to its successor. In addition, it informs its leaving to all other backup smart nodes in its host list with a ‘‘busy’’ Smart PING message. When a smart node is overloaded, it balances its work by delivering a part of its list of the monitored nodes to a backup smart node in its host list. Each leaving or overloaded smart node sends a ‘‘busy’’ Smart PING message to the monitored nodes to inform the handover. Meanwhile, the chosen smart node sends the ‘‘idle’’ Smart PING messages to those monitored nodes to confirm this replacement.

![](images/fb65587d8754b71a6c850eb4a37fc8605e6990d71f63acc8d3c23813f633c907.jpg)



(a) The modified ‘‘GUID’’ field.

<table><tr><td>GUID</td><td>...</td><td> ${\beta }_{g}$ </td><td>time stamp for  ${\beta }_{g}$ </td><td>...</td></tr></table>

(b) Smart PING.

<table><tr><td>GUID</td><td>...</td><td>sensor</td><td> ${\beta }_{l}$ </td><td>size of monitoring set</td><td>...</td></tr></table>

(c) Smart PONG.

<table><tr><td>GUID</td><td>...</td><td>sensor</td><td>...</td></tr></table>

(d) Backup PONG or Lazy PONG.   
Fig. 5. PING/PONG messages in PASH.

<table><tr><td>Smart Node</td><td>Smart Node List</td></tr><tr><td>7</td><td>14,8,11</td></tr><tr><td>14</td><td>7,8,18,19,20</td></tr><tr><td>11</td><td>7,21,27</td></tr><tr><td>19</td><td>14,20,23,38,27</td></tr><tr><td>23</td><td>19,20,27</td></tr><tr><td>38</td><td>19,27,21</td></tr><tr><td>27</td><td>18,19,11,38</td></tr><tr><td>20</td><td>14,19,23</td></tr><tr><td>21</td><td>38,11</td></tr><tr><td>18</td><td>14,8,27</td></tr><tr><td>8</td><td>7,14,18</td></tr></table>

(a) Initial mesh topology among the Smart Nodes.

![](images/9d37b843bf32414fb74b5ae29273c1831b31a94d074ba7dac822f0836ba432f1.jpg)



<table><tr><td>Smart Node</td><td>Smart Node List</td></tr><tr><td>7</td><td>14,8,11</td></tr><tr><td>14</td><td>7,8,18,19,20</td></tr><tr><td>11</td><td>7,21,27</td></tr><tr><td>19</td><td>14,20,23,38,27</td></tr><tr><td>23</td><td>19,20,27</td></tr><tr><td>38</td><td>19,27,21</td></tr><tr><td>27</td><td>18,19,11,38</td></tr><tr><td>20</td><td>14,19,23</td></tr><tr><td>21</td><td>38,11</td></tr><tr><td>18</td><td>14,8,27</td></tr><tr><td>8</td><td>7,14,18</td></tr></table>

(b) Node 19, 11, 14, 8 and 7 are requested to be as collector.

![](images/4d24e80913c9ae66d02281a01c7213e57f4a03a326e2da5fa99e6ebad7c7d41c.jpg)



<table><tr><td>Smart Node</td><td>Smart Node List</td></tr><tr><td>7</td><td>14,8,11,20,27, 21,18,19</td></tr><tr><td>14</td><td>7,8,18,19,20,23, 38</td></tr><tr><td>11</td><td>7,21,27</td></tr><tr><td>19</td><td>14,23,38,27</td></tr><tr><td>23</td><td>19,20,27</td></tr><tr><td>38</td><td>19,27,21</td></tr><tr><td>27</td><td>18,19,11,38</td></tr><tr><td>20</td><td>14,19,23</td></tr><tr><td>21</td><td>38,11</td></tr><tr><td>18</td><td>14,8,27</td></tr><tr><td>8</td><td>7,14,18</td></tr></table>

(c) Node 19 forwards the request to node 14, and node 11,14, 8 forward the request to node 7.

![](images/bc2f65e320d5434e29c35dcd8423cc76db695ce41b98895eab0a300e7209080c.jpg)



<table><tr><td>Smart Node</td><td>Smart Node List</td></tr><tr><td>7</td><td>14,8,11,20,27, 21,18,19,23,28</td></tr><tr><td>14</td><td>7,8,18,19,20,23, 38</td></tr><tr><td>11</td><td>7,21,27</td></tr><tr><td>19</td><td>14,23,38,27</td></tr><tr><td>23</td><td>19,20,27</td></tr><tr><td>38</td><td>19,27,21</td></tr><tr><td>27</td><td>18,19,11,38</td></tr><tr><td>20</td><td>14,19,23</td></tr><tr><td>21</td><td>38,11</td></tr><tr><td>18</td><td>14,8,27</td></tr><tr><td>8</td><td>7,14,18</td></tr></table>

(d) Node 7 is elected as a collector for all other nodes.

![](images/35cb6e390d872315341da4a9c5a0e87cf30e2e9ae6f7953e86c6f39d90ff1f11.jpg)



Fig. 6. Collectors’ selection.

When a node joins the system, whatever role it chooses, say as a lazy node, a backup smart node, or a smart node, it selects one and only one ‘‘idle’’ smart node as its sensor node. The chosen smart node will add the newly joining node into its monitoring list. During its lifetime, the new joining node would not change its sensor node except when: (1) the smart node hands over the duty to another smart node; or (2) the sensor is abnormally offline.

In the second case, the node would check its host list to choose another ‘‘idle’’ smart node as its sensor.

# 4.3. Popularity dynamics sensing

PASH requires each smart node detect the changes of its monitored nodes and share this information with other smart nodes.

# 4.3.1. Local sensing

Periodically, a smart node checks the replica changes of the nodes in its monitoring list and computes the local dynamic rate of the replicas, $\beta _ { l } .$ To make the local sensing available, a smart node still holds the information of leaving nodes in its host list until this sensing time period ends in case it loses the trace of those leaving nodes. Suppose the sensing time period is τ and there are $\psi _ { 1 }$ node with $C _ { 1 } , \psi _ { 2 }$ node with $C _ { 2 } , \ldots , \psi _ { j }$ node with $C _ { j } , \ldots , \psi _ { s }$ node with $C _ { s }$ in last sensing time point t. During this time period, there are $\varDelta \psi _ { 1 }$ nodes with $C _ { 1 } , \varDelta \psi _ { 2 }$ nodes with $C _ { 2 } , \ldots , \varDelta \psi _ { j }$ nodes with $C _ { j } , \ldots , \varDelta \psi _ { s }$ nodes with $C _ { s }$ no longer active, and $\zeta _ { 1 }$ nodes with $C _ { 1 } , \zeta _ { 2 }$ nodes with $C _ { 2 } , \ldots , \zeta _ { i }$ nodes with $C _ { i } , \ldots , \zeta _ { g }$ nodes with $C _ { g }$ joining the monitoring set. Then, $\beta _ { l }$ is given by Eq. (8).

![](images/5533104ff9866f23c280a57f066ed7dcb71b911d7ec24bbaaaa3a70ed9fcc3e7.jpg)



Fig. 7. Global exchange period and sub-periods.

$$
\beta_ {l} = \frac {\Delta R _ {l}}{R _ {l} \Delta t} = \frac {k \sum_ {i = 1} ^ {g} C _ {i} \zeta_ {i} - \sum_ {j = 1} ^ {s} C _ {j} \Delta \psi_ {j}}{\tau \sum_ {j = 1} ^ {s} C _ {j} \psi_ {j}}. \tag {8}
$$

The local sensing period τ for each smart node is equal to the global exchange period and is adjusted accordingly when a new global exchanging period is adopted. The adaptive is discussed next.

# 4.3.2. Global exchanging

Smart nodes obtain the perspective of the global dynamics by periodically exchanging the detected dynamic information of monitored nodes. During a globally exchanging period, each smart node has an option for its role: acting as a collector or a noncollector. A collector is in charge of collecting, computing, and releasing the global dynamic information, while a non-collector only provides its local information and accepts updated global dynamic information from the collector.

A smart node can be a collector candidate if and only if there is no other node in its SmartNodes List has an IP address smaller than itself. Otherwise, it will request the node with the smallest IP address in its SmartNodes List as the collector. The requested node would serve as a collector if and only if there is no other Smart node with a smaller IP address in the SmartNodes List of its own. Otherwise, it would forward/redirect the request to the node with the smallest IP address in its SmartNodes List. Fig. 6 plots an example of this election routine. For saving traffic overhead, a requested non-collector node forwards/redirects all requests with only one packet instead of sending a bunch of packets for those requests.

To lessen the processing cost and traffic overhead, a smart node that currently is a non-collector would call the collector election routine only under the following three situations: (a) its current collector node is no longer active; (b) there exists a new coming smart node with a smaller IP address than the current collector in its SmartNodes List; (c) as a newly joining node, when there is no collector node. On the other hand, a smart node serving as a collector would call the collector election routine only if it includes a new smart node with a smaller IP address into its SmartNodes List.

The global exchange period is divided into two sub-periods, shown in Fig. 7. In the first sub-period, a collector issues Smart PING messages, in which the ‘‘calculating bit’’ is set $\tan ^ { \bullet } 1 ^ { \prime \prime }$ , to all the requesting non-collectors and waits for replied PONG messages. Each non-collector provides the dynamic rate of its local replicas, $\beta _ { l } ,$ as well as the size of its monitoring set, $n _ { l } ,$ to the collector with a Smart PONG message.

In the second sub-period, the collector collects all received $\beta _ { l }$ and computes $\beta _ { g } .$ . Suppose the collector has received r PONG messages, each with information $( \beta _ { l i } , n _ { l i } )$ , it computes $\beta _ { g }$ as follows.

$$
\beta_ {g} = \frac {\sum_ {i = 1} ^ {r} n _ {l i} \beta_ {l i}}{\sum_ {i = 1} ^ {r} n _ {l i}}. \tag {9}
$$

The collector then forwards the updated $\beta _ { g }$ to all of the requesting smart nodes with a Smart PING message, in which the ‘‘calculating $\mathrm { b i t " }$ is reset to ‘‘0’’. When the requesting smart nodes receive the message, they deliver the information to all their monitoring nodes also by sending Smart PING messages.

# 4.4. Search selection

PASH utilises the global dynamic information to adjust item popularity when publishing a query or gossiping the item popularity to other nodes.

Whenever a node receives a query for item i, it will compute the popularity value of item i before making a search decision. For any node, suppose current time is t, the popularity value for item i that the node has held is $p _ { i } ( t _ { 0 } )$ with a timestamp $t _ { 0 } ,$ where $t _ { 0 } ~ < ~ t ,$ it adjusts $p _ { i } ( t _ { 0 } )$ into $p _ { i } ( t )$ by using Eq. (10).

$$
p _ {i} (t) \leftarrow p _ {i} (t _ {0}) \cdot \gamma = p _ {i} (t _ {0}) [ 1 + \beta_ {g} (t - t _ {0}) ]. \tag {10}
$$

If $p _ { i } ( t )$ exceeds the threshold $T _ { f } ,$ the query will be flooded. Otherwise, the query will be issued via DHT.

During the Gossip process, if a node has known a $v _ { i } ,$ , the replica statistic of item i with a timestamp t1. When receiving a gossip message from a node j at time t, within which the replica statistic of item i is $v _ { i j }$ with a timestamp $t _ { 2 } ,$ , it updates $v _ { i }$ by using Eq. (11)

$$
\begin{array}{l} v _ {i} = \gamma_ {1} v _ {i} \forall \gamma_ {2} v _ {i j} = v _ {i} [ 1 + \beta_ {g} (t - t _ {1}) ] \forall v _ {i j} [ 1 + \beta_ {g} (t - t _ {2}) ] \\ = \left\{ \begin{array}{l l} v _ {i} [ 1 + \beta_ {g} (t - t _ {1}) ], & \text { if   } v _ {i} [ 1 + \beta_ {g} (t - t _ {1}) ] \geq v _ {i j} [ 1 + \beta_ {g} (t - t _ {2}) ] \\ v _ {i j} [ 1 + \beta_ {g} (t - t _ {2}) ] & \text { if   } v _ {i} [ 1 + \beta_ {g} (t - t _ {1}) ] <   v _ {i j} [ 1 + \beta_ {g} (t - t _ {2}) ]. \end{array} \right. \tag {11} \\ \end{array}
$$

# 4.5. Sensing and exchanging period

As indicated in Section 4.3, the local sensing period τ for each smart node is equal to the global exchange period. For accurate prediction, the P2P system requires an adaptive tuning mechanism for determining the sensing period τ . In PASH, the τ is initialised as a pre-determined system parameter and adaptive to the dynamic of replicas. A smart node collects l latest $\beta _ { g } \{ \beta _ { g _ { 1 } } , \beta _ { g _ { 2 } } , \ldots , \beta _ { g _ { i } } , \ldots , \beta _ { g _ { l } } \}$ and uses Eq. (12) to compute $\delta _ { \beta } ,$ , as 1 2the deviation of $\beta _ { g }$ i.

$$
\delta_ {\beta} = \frac {1}{l} \sum_ {i = 1} ^ {l} \left| \beta_ {g _ {i}} - \overline {{\beta_ {g}}} \right| = \frac {1}{l} \sum_ {i = 1} ^ {l} \left| \beta_ {g _ {i}} - \frac {1}{l} \sum_ {i = 1} ^ {l} \beta_ {g _ {i}} \right|. \tag {12}
$$

From the Eq. (12), we find that a larger $\delta _ { \beta }$ reflects a large variety of $\beta _ { g }$ . In contrast, a smaller $\delta _ { \beta }$ indicates a less unstable popularity dynamic rate. If $\delta _ { \beta }$ is equal to zero, the popularity dynamic rate keeps stable and the sensing frequency could be decreased. Therefore, it is possible to construct a tuning function that is inversely proportional to $\delta _ { \beta } ,$ , termed as $f ( \tau , \delta _ { \beta } )$ , and use it to adjust the value of τ . In the prototype version of PASH, we adopt a simple $f ( \tau , \delta _ { \beta } )$ to compute the new value of τ as shown in Eq. (13).

$$
\tau^ {\prime} = f (\tau , \delta_ {\beta}) = \tau \cdot (1 - \delta_ {\beta}). \tag {13}
$$

![](images/4062bcf030d8da5dfbe0965ad0ef3f7435f9fc1e3ffc791a28a3e644bb012cdd.jpg)



Fig. 8. Smart node ratio determination.

![](images/24f929894859608af31c4f7ef54405fe98efb038cfd42b91f4880f9e051bcca1.jpg)



Fig. 9. Computing accuracy.

# 5. Simulation methodology and metrics

We evaluate PASH through synthetic and trace-driven simulations. The Ion P2P Snapshots [24] we used in this work include topologies of a hybrid Gnutella system from 2004 to 2005. Based on the real P2P topologies from this trace, we construct our testbed with a P2P network including $1 0 ^ { 3 } – 1 0 ^ { 4 }$ peers. To perform the flooding and DHT search simultaneously, we mainly include ultrapeers into our testing topologies. Each peer holds resources which follow the Zipf distribution. The physical internet layer is generated by BRITE [16], in which the internet topology holds about 30 000 nodes. Peers are joining and leaving the network based on existing observations on P2P behaviours [22].

In our simulation, we construct the DHT by using the SHA-1 algorithm. Therefore, any key stored in nodes has a size of 20 bytes. The flooding search is performed by employing the Breadth First Search (BFS) algorithm. To investigate the search performance, we simulate $1 0 ^ { 5 }$ queries iteratively for each run and report the average of 30 runs.

We use the following metrics to evaluate PASH performance.

Estimation error. It is used to evaluate the accuracy of estimated popularity values of items when performing PASH. Since the dynamic change of P2P systems is considered by PASH, we expect PASH can report more accurate popularity values of items when making the selection between flooding and DHT.

Traffic overhead. From the network administrators’ point of view, traffic cost is the most important metric to reflect the impact caused by P2P applications. In the $\mathrm { P 2 P }$ overlay, each edge is uniquely mapped into a path in the underlying internet layer, whose length is l. In one query cycle, we calculate the sum of the distances of the enrolled edges that this message traversed. Thus, the traffic overhead of a query cycle can be computed as $\begin{array} { r } { H = M \times L = \sum | m _ { i } | \times l _ { i } , 1 \le i \le e , } \end{array}$ where $| m _ { i } |$ is the size of messages that traverse, and e is number of enrolled edges. We report the traffic overhead per link in performing PASH to reflect the reduced traffics cost.

![](images/4e293581e8569cb401047ae01ddce2275e5d79f15818d00a4440c999c4434902.jpg)



Fig. 10. Estimation error vs. system dynamic rate (Topology size is $1 0 ^ { 3 } )$ .   
![](images/378aff7d253a62f98132969e9102fc582a36b7013f5bf3b5249fc9fbe3d40ce3.jpg)



Fig. 11. Estimation error vs. system dynamic rate (Topology size is $1 0 ^ { 4 } )$ .   
![](images/841640644bfd770a2023630d382d63c97daace3bed63181528fbddb0ff3d46dc.jpg)



Fig. 12. Estimation error vs. ratio of cheating nodes (Topology size is $1 0 ^ { 3 } ) .$

Response time. This is an important metric which end users of P2P systems are mainly concerned. Shorter response time leads to higher degree of satisfaction and better service quality. In this work, we define the response time as the period of time from starting a search to receiving the first response, and show the response time reduction achieved by PASH.

![](images/2b1dbf90912a99c2095bdf8dead478a7f940134ac6bc2e82bc7933654a900260.jpg)



Fig. 13. Estimation error vs. ratio of cheating nodes (Topology size is 104).

![](images/120f0f09edea44674e64b8a2f89382e1e8405ec97e1228179c86d141c7e121e4.jpg)



Fig. 14. Traffic overhead.

![](images/fd3c18a534b559bad66e3f94a4a9116b8d19f694e89c39723331499fed4e0072.jpg)



Fig. 15. Traffic overhead per overlay link.

We also examine several system parameters of PASH, such as the smart node ratio and algorithm convergence. These important parameters guarantee the effectiveness and efficiency of PASH.

# 6. Performance evaluation

We first determine the best smart node ratio of PASH. As mentioned in Section 4, we employ a probability based smart node assignment scheme. We compute the expected sensing accuracy of different traces. Fig. 8 plots the expected smart node ratio x/n in two representative P2P topologies. For any given P2P topology, the sensing accuracy increases when enlarging the x/n ratio. We increase the smart node ratio x/n from 0, and stop when the derivative of sensing accuracy tends towards zero.

![](images/1c88c8c47fff0b9c4d89dd713f743ae9289f7cf323cb60eced30eb8001d8e930.jpg)



Fig. 16. CDF curve of response time of 105 queries (Topology size is 103).   
![](images/e13259016d51d7610e846aa738960c77ebf8bf24460ef75461abf4fc2593230a.jpg)



Fig. 17. CDF curve of response time of 105 queries (Topology size is 104).

At this point, we say the system obtains a sufficient smart ratio. The results show that the proper value of x/n is about 15% when there are about 1000 nodes, whereas this value is less than 10% when the size of P2P topology reaches 104.

We find the proper ratio would decrease when the size of the system increases. Fig. 9 depicts this trend with different computing accuracy. Indeed, the larger the P2P network size is, the fewer smart nodes are needed. Following our smart node generation strategy, PASH always selects those nodes with a probability p = S×x/n, where S is the number of candidate peers. In this way, those nodes with higher connection degree would be selected as smart nodes with a higher probability. As shown in Fig. 9, PASH reduces the smart node ratio when increasing the system size, while the computing accuracy of popularity values can still be guaranteed.

After determining the proper smart node ratio, PASH makes use of it to compute the popularity values for the requested items. Here we compare PASH with GAB and QRank [3] in the estimating accuracy of item popularity. QRank is a most recent work targeting on the hybrid search. QRank involves the resource distribution into the search selection. All these three approaches would incur some estimation errors in the flooding/DHT decision.

We define the estimation error ε by $\varepsilon ~ = ~ ( E - P ) / P$ , where the E is estimation value and P is the exact popularity value of an item. Figs. 10 and 11 show that PASH outperforms GAB in estimating the accuracy of popularity values of items in a dynamic P2P system. We also adopt the PASH to QRank for investigating the search efficiency. We find that the QRank can leverage PASH to significantly increase the computing accuracy as shown in Figs. 10 and 11.

![](images/bf31665a1c1fef37f20315bcf3b478f8a9dca752431c2b53eefbf1d05d48d493.jpg)



Fig. 18. Response time reduction under different dynamic rates.

Besides the network tuning, node cheating also has a significant impact on the estimation accuracy. If a number of nodes cheats on the reported $\beta _ { g }$ , they can mislead the search selection. In our simulation, we randomly select a number of nodes as the malicious nodes to perform the cheating operation. If the node is a lazy node or backup smart node, it only cheats on the reported replicas. If the node is a smart node, it also cheats on computing $\beta _ { g } .$ . The objective of cheating operation is performed by introducing a large deviation to the $\beta _ { g } .$ . For example, if a malicious smart node computes $\beta _ { g }$ as 30% at time t, it will enlarge the value of $\beta _ { g }$ to 80%. Figs. 12 and 13 plot the performance of PASH with enlarging the number of malicious nodes. We find that PASH is still robust if the ratio of malicious node is less than 10% and the P2P network is not very dynamic. If there were too many malicious nodes in the P2P system, PASH would suffer from the cheating operation and could not provide accurate estimation. It would effectively defend against the cheating operation if constructing trust management systems or incentive mechanisms in P2P networks [32], which may be out of the scope of this paper.

Another key issue is the convergence of PASH, that is, how fast the PASH is able to enter a stable state. To this end, we keep inserting queries into the system at a fixed speed, around 100 queries per second. The desired objects follow the Zipf distribution [16]. We also assign each node a lifetime that follows a log-quadratic curve [22], which can be approximated by using two Zipf distributions. We observe the change of network traffic in the system. At the very beginning, PASH has a minor impact on the system as peers do not come and leave frequently, and the traffic overhead of using GAB is similar to PASH, as shown in Fig. 14. Later, when the network tunes due to the peers’ joining and leaving, the traffic overhead decreases as PASH avoids unnecessary flooding. Specifically, PASH works steadily after about 200 s.

In Fig. 15, we show the average traffic overhead of PASH on P2P overlay. The curves indicate that PASH reduces traffic overhead on overlay link by about 20%–35%. Note that we let both protocols search the same items. PASH is particularly effective for those items whose popularity values are close to the flooding/DHT threshold. Another benefit in using PASH is the reduction of response time. Figs. 16 and 17 show that the average response time of queries is reduced by 50%. It is because that the more accurate selections between flooding and DHT help PASH outperform GABlike protocols in both the traffic overhead and response time. On the other hand, the network tuning may raise an impact on the response time. As shown in Fig. 18, we also investigate the response time reduction under different dynamic rate and network size. We compute the reduction ratio of response time as $\mathrm { R T _ { R e d } = }$ $1 - \mathrm { R T _ { P A S H } / R T _ { G A B } }$ , where $\mathrm { R T _ { P A S H } }$ and $\mathsf { R T } _ { \mathrm { G A B } }$ denote the response time of PASH and GAB, respectively. We find that PASH can save more response time in the highly dynamic P2P network since the $\mathrm { R T _ { R e d } }$ increases if enlarging the dynamic rate.

Recent advances in wireless communications have led to the development of more ubiquitous P2P services. Especially, the mobile wireless P2P system has gained increasing attention. Wireless mobile P2P users are usually self-organized and interconnected in the Ad Hoc pattern. Meanwhile, the mobile P2P network becomes more dynamic and unstable than wired P2P environments. PASH is thoroughly decentralised and computes the popularity of items in a distributed way. As we discussed above, PASH is effectively resilient to the network tuning, which enables it to support efficient search in mobile P2P systems.

# 7. Conclusion

In a hybrid P2P system, flooding and DHT are both employed for content locating. The decision to use either a flooding search or a DHT search depends on the population of desired data. Existing works do not consider the dynamic factors of P2P systems when counting data popularities.

In this paper, we propose PASH, which provides an efficient and accurate search decision mechanism by dynamically detecting the P2P overlay change and hereby refining the estimation of the content popularity. By enrolling the P2P dynamic factor, not only can the traffic overhead be reduced in P2P systems, end users can also obtain the desired resource with shorter search latency. The simulation results validate the effectiveness of our overall design — making proper search selection decision and saving the traffic cost as well as the response time.

# References

[1] H. Balakrishnan, M.F. Kaashoek, D. Karger, R. Morris, I. Stoica, Looking up data in P2P systems, Communications of ACM 46 (2) (2003).   
[2] Y. Chawathe, S. Ratnasamy, L. Breslau, N. Lanham, S. Shenker, Making gnutellalike P2P systems scalable, in: Proceedings of ACM SIGCOMM, 2003.   
[3] H. Chen, H. Jin, Y. Liu, L.M. Ni, Difficulty-aware hybrid search in peer-to-peer networks, in: Proceedings of International Conference on Parallel Processing, ICPP, 2007.   
[4] Gnutella, http://gnutella.wego.com/, 2002.   
[5] Kazaa, http://www.kazaa.com/, 2008.   
[6] Gnutella protocol specification, http://rfc-gnutella.sourceforge.net, 2008.   
[7] K. Hildrum, J.D. Kubatowicz, S. Rao, B.Y. Zhao, Distributed object location in a dynamic network, in: Proceedings of ACM Symp. on Parallel Algorithms and Architectures, 2002.

[8] H. Jiang, S. Jin, Exploiting dynamic querying like flooding techniques for unstructured peer-to-peer networks, in: Proceedings of IEEE ICNP, 2005.   
[9] A.K.-H. Leung, Y.-K. Kwok, On topology control of wireless peer-to-peer file sharing networks: Energy efficiency, fairness and incentive, in: Proceedings of the 6th IEEE International Symposium on World of Wireless Mobile and Multimedia Networks, WOWMOM, 2005.   
[10] A.K.-H. Leung, Y.-K. Kwok, On localized application-driven topology control for energy efficient wireless peer-to-peer file sharing, IEEE Transactions on Mobile Computing 7 (2008) 66–80.   
[11] B. Liu, W.C. Lee, D.L. Lee, Supporting complex multi-dimensional queries in P2P systems, in: Proceedings of IEEE ICDCS, 2005.   
[12] Y. Liu, L. Xiao, X. Liu, L.M. Ni, X. Zhang, Location awareness in unstructured peer-to-peer systems, IEEE Transactions on Parallel and Distributed Systems 16 (2005).   
[13] B.T. Loo, J.M. Hellerstein, R. Huebsch, S. Shenker, I. Stoica, Enhancing P2P filesharing with an internet-scale query processor, in: Proceedings of VLDB, 2004.   
[14] B.T. Loo, R. Huebsch, I. Stoica, J.M. Hellerstein, The case for a hybrid P2P search infrastructure, in: Proceedings of the International Workshop on Peer-To-Peer Systems, IPTPS, 2004.   
[15] Q. Lv, P. Cao, E. Cohen, K. Li, S. Shenker, Search and replication in unstructured peer-to-peer networks, in: Proceedings of ACM ICS, 2002.   
[16] A. Medina, A. Lakhina, I. Matta, J. Byers, BRITE: An approach to universal topology generation, in: Proceedings of the International Workshop on Modeling, Analysis and Simulation of Computer and Telecommunications Systems, MASCOTS, 2001.   
[17] Napster, http://www.napster.com/, 2008.   
[18] D. Qiu, R. Srikant, Modeling and performance analysis of bittorrent-like peerto-peer networks, in: Proceedings of ACM SIGCOMM, 2004.   
[19] S. Ratnasamy, P. Francis, M. Handley, R. Karp, S. Shenker, A scalable contentaddressable network, in: Proceedings of ACM SIGCOMM, 2001.   
[20] A. Rowstron, P. Druschel, Pastry: Scalable, decentralized object location, and routing for large-scale peer-to-peer systems, in: Proceedings of ICDS, 2001.   
[21] S. Saroiu, P.K. Gummadi, S.D. Gribble, A measurement study of peer-topeer file sharing systems, in: Proceedings of the Multimedia Computing and Networking, MMCN, 2002.   
[22] M.T. Schlosser, S.D. Kamvar, Availability and locality measurements of peerto-peer file systems, in: Proceedings of ITCom: Scalability and Traffic Control in IP Networks, 2002.   
[23] I. Stoica, R. Morris, D. Karger, M.F. Kaashoek, H. Balakrishnan, Chord: A scalable peer-to-peer lookup service for internet applications, in: Proceedings of ACM SIGCOMM, 2001.   
[24] D. Stutzbach, R. Rejaie, Characterizing the two-tier gnutella topology, in: Proceedings of ACM SIGMETRICS, 2005.   
[25] G. Swamynathan, B.Y. Zhao, K.C. Almeroth, Exploring the feasibility of proactive reputations, in: Proceedings of the International Workshop on Peer-To-Peer Systems, IPTPS, 2006.   
[26] C. Wu, B. Li, rStream: Resilient peer-to-peer streaming with rateless codes, in: Proceedings of ACM Multimedia, 2005.   
[27] D. Xuan, S. Chellappan, X. Wang, S. Wang, Analyzing the secure overlay services architecture under intelligent ddos attacks, in: Proceedings of IEEE ICDCS, 2004.   
[28] L. Yin, G. Cao, DUP: Dynamic-tree based update propagation in peer-to-peer networks, in: Proceedings of IEEE ICDE, 2005.   
[29] Z. Zhang, S. Chen, Y. Ling, R. Chow, Resilient capacity-aware multicast based on overlay networks, in: Proceedings of IEEE ICDCS, 2005.   
[30] M. Zaharia, S. Keshav, Gossip-based search selection in hybrid peer-to-peer networks, in: Proceedings of the International Workshop on Peer-To-Peer Systems, IPTPS, 2006.

[31] M. Zhong, K. Shen, Popularity-biased random walks for peer-to-peer search under the square-root principle, in: Proceedings of the International Workshop on Peer-To-Peer Systems, IPTPS, 2006. [32] R. Zhou, K. Hwang, PowerTrust: A robust and scalable reputation system for trusted peer-to-peer computing, IEEE Transactions on Parallel and Distributed Systems 18 (2007).

![](images/e4085fc69bb3e92c019bb0b980b7f3732f840337ffc55d90c436ec711208953d.jpg)



Xiaoqiu Shi received her B.S. degree in Physics Department from Zhejiang University, China, in 1985, and an M.Eng. degree in Computer Science and Technology Department from Zhejiang University, China, in 2000. She now is a professor in Computer Science Department at Wenzhou University, China.

![](images/4b808aa868f28e30fa77ccaabf0015c657e4b38aae281fcd801f8f95100a185e.jpg)



Jinsong Han received his B.S. degree in Computer Science Department from Shandong University of Technology, China, in 1997, an M.Eng. degree in Computer Science Department from Shandong University, China, in 2000, and a Ph.D. degree in Computer Science and Engineering at Hong Kong University of Science and Technology, in 2007. He is now a postdoctoral fellow in the Department of Computer Science and Engineering at Hong Kong University of Science and Technology (HKUST). His research interests include peer-to-peer computing, anonymity, network security, pervasive computing, and high-speed networking.

He is a member of the IEEE Computer Society, and a member of ACM.

![](images/0313177ff65d5df5215fb658559909a8354c6a20a52db84e184fd3670b79cce9.jpg)



Yunhao Liu received his B.S. degree in Automation Department from Tsinghua University, China, in 1995, and an M.A. degree in Beijing Foreign Studies University, China, in 1997, and an M.S. and a Ph.D. degree in Computer Science and Engineering at Michigan State University in 2003 and 2004, respectively. He is now with the Department of Computer Science and Engineering at Hong Kong University of Science and Technology (HKUST). He is also an adjunct professor of Xi’an Jiaotong University. His research interests include peer-to-peer computing, pervasive computing and sensor networks. He is a senior

member of the IEEE Computer Society, and a member of ACM.

![](images/ce2fac0dcc906d25c76aa9f8bcc623e80703f1655f1000419a70605df88f3a08.jpg)



Lionel M. Ni earned his Ph.D. degree in Electrical and Computer Engineering from Purdue University, West Lafayette, IN, in 1980. He is Chair Professor in the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology (HKUST). He is also Director of the HKUST China Ministry of Education/Microsoft Research Asia IT Key Lab and Director of the HKUST Digital Life Research Center. A fellow of IEEE, Dr. Ni has chaired many professional conferences and has received a number of awards for authoring outstanding papers.