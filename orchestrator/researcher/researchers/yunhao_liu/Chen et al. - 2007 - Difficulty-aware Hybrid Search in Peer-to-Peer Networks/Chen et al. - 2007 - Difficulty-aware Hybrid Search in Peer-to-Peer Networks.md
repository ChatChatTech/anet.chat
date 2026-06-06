# Difficulty-aware Hybrid Search in Peer-to-Peer Networks

Hanhua Chen $^{\dagger}$ , Hai Jin $^{\dagger}$ , Yunhao Liu $^{\ddagger}$ , Lionel M. Ni $^{\ddagger}$

$^{\dagger}$ School of Computer Science and Technology
Huazhong Univ. of Science and Technology
{chenhanhua, hjin}@hust.edu.cn

$^{\ddagger}$ Dept. of Computer Science and Engineering Hong Kong Univ. of Science and Technology {liu, ni}@cse.ust.hk

# Abstract

By combining an unstructured protocol with a DHT-based global index, hybrid Peer-to-Peer (P2P) improves search efficiency in terms of query recall and response time. The key challenge in hybrid search is to estimate the number of peers that can answer a given query. Existing approaches assume that such a number can be directly obtained by computing item popularity. In this work, we show that such an assumption is not always valid, and previous designs cannot distinguish whether items related to a query are distributed in many peers or are in a few peers. To address this issue, we propose QRank, a difficulty-aware hybrid search, which ranks queries by weighting keywords based on term frequency. Using rank values, QRank selects proper search strategies for queries. We conduct comprehensive trace-driven simulations to evaluate this design. Results show that QRank significantly improves the search quality as well as reducing system traffic cost compared with existing approaches.

# 1. Introduction

Since the emergence of peer-to-peer (P2P) [8-10, 20] file sharing applications, such as Napster [3], and Gnutella [4], millions of users have started using P2P tools to share desired files. P2P networks have shown a great potential as a network tool for harnessing the information stored on desktops.

Decentralized P2Ps utilize different search techniques. Unstructured P2P networks commonly employ flooding to locate items (in this paper, we use the terms “file” and “item” interchangeably). Each query is tagged with a maximum Time-To-Live (TTL) to limit the number of hops it travels. In structured P2Ps, items are located though distributed hash table (DHT) interfaces. Recent studies show that flooding is effective for locating highly replicated items, but less effective for rare items. In [12], Loo's experiment showed that queries for rare items in Gnutella have very low recall rate. Around $18\%$ of all Gnutella queries return no results, despite the fact that for at least two thirds of these queries there are results available in the system. In addition, such queries have poor response time. On the contrary, DHTs guarantee perfect recalls and good response time for rare items, while incur significant bandwidth cost for popular item publishing and multiple-keyword search.

Hybrid P2P networks have recently attracted much attention $[11, 12, 21]$ . To make this concept clear, let us consider a simple example in our daily life. When we need an answer for an easy question, such as “what is the date today”, probably we can get it from most of the people around us. For a difficult question, such as “Shakespeare’s sonnets”, randomly asking people around us may not work, and we would achieve better (or quicker) results looking it up in books in the library or consulting with experts. This scenario is similar to the selection of flooding and DHT in P2P networks. A hybrid P2P network combines an unstructured flooding network with a structured DHT-based global index $[11, 12]$ . Searches are performed either by flooding the unstructured network, or by looking up in the DHTs, according to the popularity of items. Hybrid P2P networks improve the recall and response time of queries for rare items with low bandwidth overhead, as well as maintaining good recall and response time for highly replicated items.

The key issue in improving hybrid search is how to better estimate the number of peers that can answer a question (query), such that we can determine the best search operation. Existing approaches for differentiating queries fall into two categories. The first type is detection-based, called simple hybrid strategy, in which a search is first performed via flooding. If not enough results returned within a predefined time, the query is resumed as a DHT query $[11]$ . Although both popular and rare items can be ultimately located, locating rare items has a worse response time than pure DHT and extra cost is incurred by pre-flooding. A second approach uses aggregation information gathered through a gossiping method to estimate the popularity of the items $[21]$ . By using a threshold on the number of related items to determine whether flooding or DHT, such approaches outperform simple hybrid techniques.

However, differentiating among queries by estimating the number of items containing all the query terms has a fatal flaw. As identified by H. Zhang et al. [17], the interested locality is a common and powerful principle of P2P file sharing systems. If a peer has a particular piece of content that a user is interested in, it is very likely the peer has other items that user has interest as well. Hence, for a given query, when it is estimated that there are many related items in the network, it is not necessary that many peers have the desired files. Current approaches cannot distinguish whether the many items related to a query are distributed in many peers or are in a few peers, thus fail to provide a proper selection on flooding or DHT.

To address this issue, we propose QRank, a difficulty-aware hybrid search scheme, which employs a push synopsis based random gossiping algorithm $[6, 13]$ to gather statistical information and term frequency. Using the rank values, QRank selects proper search strategies for queries. Trace-driven simulation results show that QRank significantly improves the search quality as well as reducing system traffic cost compared with known approaches.

The rest of the paper is organized as follows. Section 2 discusses the related work. Section 3 introduces the basic idea of QRank. Detailed design of QRank scheme is presented in Section 4. Section 5 describes how we collect a real trace. Performance evaluation is presented in Section 6. We conclude the work in Section 7.

# 2. Related work

Hybrid P2P model is first introduced by Loo et al. [12]. Having observed that the Gnutella network is inefficient for locating rare items, Loo et al. propose the SimpleHybrid architecture, combining Gnutella and DHT based PIER [11]. SimpleHybrid search first performs flooding techniques with limited TTL. Queries that return no results within 30 seconds are reissued using the PIER search engine. Using this method the recall rate for rare items is improved. The results also show PIER returns the first result within 10-12 seconds. Hence, SimpleHybrid approach reduces the average latency for rare items to 40-42 seconds, which is 65 seconds by flooding only. In addition, SimpleHybrid reduces the number of queries that receive no results in Gnutella by 18%. The drawback of SimpleHybrid is twofold. First, due to the pre-flooding operation, the response time for rare items is much longer than that directly using DHT. Second, the method incurs unnecessary bandwidth cost for rare items.

To better identify rare items, Zaharia and Keshav proposed a gossip based scheme called GAB $[21]$ . GAB uses pushing synopsis based random gossip scheme to get global statistics on the number of copies. Search selection is based on the popularity of items. When a query arrives, GAB sums up all the counts of titles that contain all the terms in the query. If the sum is above a specified threshold, the query will be flooded; otherwise, it will be looked up in the DHT. Compared with SimpleHybrid, GAB achieves a 10-20% higher recall rate, a 20-25% smaller response time, and a 45% reduction in the mean volume of query traffic. GAB, however, has a limited accuracy due to the fact that many titles containing the desired terms does not always mean that many peers can answer the query. Some queries may have unimportant keywords which degrade the estimation accuracy (in this paper, we use the terms “term” and “keyword” interchangeably).

It is well-known that weighting of terms provides improved retrieval because it differentiates useful terms from less useful ones, for example the $TF \times IDF$ scheme [15]. To weight a term in a specific query, TF quantifies the fact that terms more frequently used in a query are likely important to describe the meaning of the query. It is defined by,

$$
T F _ {t} = 1 + \log_ {\mathrm{e}} f _ {q, t} \tag {1}
$$

where $f_{q,t}$ denotes the frequency of term $t$ in query $q$ . Generally, a verbose, descriptive query can provide an indication of term importance [7, 15]. IDF, inverse document frequency, quantifies the fact that terms appearing in many documents in a collection are less important for differentiating the query.

$$
I D F _ {t} = \log_ {\mathrm{e}} (1 + \frac {N}{f _ {t}}) \tag {2}
$$

where $N$ is the total number of documents in the collection and $f_{t}$ denotes the number of documents in which term $t$ appears. The following equation is a standard form of $TF \times IDF$ to weight a term $t$ with the specified query $q$ .

$$
\omega_ {t} = T F _ {t} \times I D F _ {t} = (1 + \log_ {\mathrm{e}} f _ {q, t}) \times \log_ {\mathrm{e}} (1 + \frac {N}{f _ {t}}) \tag {3}
$$

Such methods however are not directly applicable to P2P systems. First, in a dynamic P2P system, the absence of global statistical information hinders the use of IDF to differentiate terms in a query. Second, different from queries in traditional information retrieval application, P2P queries are typically short and when they are issued, all terms are usually used only once, offering less help for using TF. In order to address this issue, we propose QRank for hybrid P2P systems.

# 3. QRank design

# 3.1. “Many items” ≠ “many peers”

Current hybrid search selections are based on the assumption that when a query has many related items, these items are distributed among many peers. It is demonstrated in diverse traces of popular P2P systems $[17]$ , nevertheless, P2P users prefer to store similar items of interest on their local disks. As shown in the example in Fig. 1, both queries a and b have a similar number of related items. However, since items related to query a are widely distributed, flooding will be more effective than a DHT for query a. On the other hand, a DHT is better for query b, as its results are available on only a few nodes in the network. Selecting search strategies on the number of related items often leads to degradation of query recall and an increase in search traffic.

QRank employs a ranking model by weighting the difficulty of queries and selects the best search strategy based on rank values. It is known that keywords in a query might be differently discriminative for searching. Considering the query “peer-to-peer network”, more items and peers contain the keyword “network” than the keyword “peer-to-peer” because “network” is a less specific term than “peer-to-peer”. But clearly, “peer-to-peer” is more important in this query.

![](images/ba6e10a1d36d2e024d2c101ad4a5735bcb5c5d4a93fbec52e5f76bf502eb9a70.jpg)



Figure 1. “Many items” ≠ “many peers”

# 3.2. Gathering global statistics

QRank counts the frequency of terms in the network by using a gossip-style algorithm [6]. It first lets all unstructured super peers browse their local index. When a keyword t is picked out the first time, this peer flips a coin up to k times and counts the times it sees heads before the first tail. It saves this count in a value called CT. Then the peer gossips the CT values for all keywords with other peers. During each round of gossip, each node chooses a random neighbor and sends the neighbor its CT values. Upon receiving CT from a neighbor, a peer computes the maximum value of CT, i.e., maxCT. Such gossip scheme causes the computation of aggregation information to converge exponentially [6]. After $\log(n)$ rounds of gossip, where n is the maximum number of all the nodes involved in the gossip, all the nodes will get the global statistics. Moreover, the count of the number of keywords, with high probability, is roughly $2^{maxCT}/0.77351$ (the number in the denominator comes from the mathematical principles described in [5]).

# 3.3. Weighting query terms

In our query term weighting model, documents are identified by titles. Each title T contains a set of keywords: $T = (k_{1}, k_{2}, ..., k_{n})$ , and a query q is a sequence of terms, $q = (t_{1}, t_{2}, ..., t_{m})$ . QRank weighting model has two parameters, Inverse Peer Frequency (IPF) and Term Frequency (TF). IPF is given by $IPF_{t} = \log_{e} \left(1 + \frac{N}{f_{t,p}}\right)$ , where N is the number of peers in the P2P network, and $f_{t,p}$ denotes the number of peers which have items containing term t. Terms that appear in more peers are less important and vice versa.

The challenging issue here is the parameter $TF$ . The standard query term weighting method in traditional information retrieval field, $TF_{t} = 1 + \log_{\mathrm{e}}f_{q,t}$ , is not applicable here. We analyze the Gnutella query trace provided by Zeinalipour-Yazti [22]. The five hour trace, which is collected by crawling the Gnutella network using 17 workstations, is quite representative for real world P2P systems. We observe that the average length of Gnutella queries is 3.54 terms and $83\%$ queries have no more than 5 terms, far from the average length of the queries in TREC-3 (query #151-200) set, which is 19.08 terms per query on average [7] for traditional text retrieval task. Hence the variable $f_{q,t}$ , the frequency that a keyword occurs in a query, is always 1 in the equation of $TF_{t}$ , leading the $TF_{t}$ a constant.

To address this problem, QRank replaces $TF_{t}$ with $apTF_{t}$ where $apTF_{t}=1+\alpha\log_{e}\frac{f_{t}}{f_{t,p}}$ , $f_{t}$ is the number of items whose titles contain t, and $f_{t}/f_{t,p}$ denotes the average frequency that the term t appears in a peer, while $\alpha>0$ is the parameter scaling the contribution of $apTF_{t}$ . Then the QRank weight is given by

$$
\omega_ {t} = a p T F _ {t} \times I P F _ {t} = (1 + a \log_ {\mathrm{e}} \frac {f _ {t}}{f _ {t , p}}) \times \log_ {\mathrm{e}} (1 + \frac {N}{f _ {t , p}}) \tag {4}
$$

# 3.4. Search selection

We define the difficulty of queries, $\varpi_q$ , by

$$
\varpi_ {q} = \frac {\sum_ {t \in q} \omega_ {t}}{| q |} \tag {5}
$$

where $|q|$ denotes the length of query q. We use $\sigma_{q}$ to quantify by how far the weights of terms differ from $\varpi_{q}$ ,

$$
\sigma_ {q} = \frac {\sum \left(\omega_ {t} - \varpi_ {q}\right) ^ {2}}{| q |} \tag {6}
$$

When a query is issued, QRank selects flooding or DHT according to the rank values $(\varpi_{q}, \sigma_{q})$ of the query. As it is difficult for a system administrator to provide simple thresholds for both $\varpi_{q}$ and $\sigma_{q}$ , QRank uses a Support Vector Machine (SVM) [19] to classify a query into different types.

Based on the traces collected, a training set is formed. In order to label each example with best search type in the data set $\{(\varpi_{q}, \sigma_{q}, \text{BestSearchType})\}$ for training the search type classifier, where the label BestSearchType is either “Flooding” or “DHT”, we define the metric vector $M = (m_{1}, m_{2}, m_{3}, \ldots, m_{n})$ .

The metrics have two kinds. Some of the metrics such as recall could be positive, i.e., the higher the value, the higher the quality. Other metrics are negative, i.e., the higher the value, the lower the quality. To normalize the metric values for queries, we scale positive metrics according to Eq.(7). For negative metrics, their values are scaled according to Eq.(8).

$$
V _ {i, j} = \left\{ \begin{array}{c c c} \frac {m _ {i , j} - m _ {i} ^ {\min}}{m _ {i} ^ {\max} - m _ {i} ^ {\min}} & \text { if } & m _ {i} ^ {\max} - m _ {i} ^ {\min} \neq 0 \\ 1 & \text { if } & m _ {i} ^ {\max} - m _ {i} ^ {\min} = 0 \end{array} \right. \tag {7}
$$

$$
V _ {i, j} = \left\{ \begin{array}{c c c} \frac {m _ {i} ^ {\max} - m _ {i , j}}{m _ {i} ^ {\max} - m _ {i} ^ {\min}} & \text {if} & m _ {i} ^ {\max} - m _ {i} ^ {\min} \neq 0 \\ 1 & \text {if} & m _ {i} ^ {\max} - m _ {i} ^ {\min} = 0 \end{array} \right. \tag {8}
$$

where $m_{i,j}$ denotes the value of the $i^{th}$ metric of query $q_{j}$ and $V_{i,j}$ denotes the normalized value of $m_{i,j}$ . Then we define the utility function as

$$
\text { Utility } (q _ {j}) = \sum_ {\mathrm{i}} (V _ {i, j} \times W _ {i}) \tag {9}
$$

where $W_{i} \in [0,1]$ and $\sum_{i} W_{i} = 1$ . $W_{i}$ is a normalized weight value given by users to represent the degree of the importance of metric $m_{i}$ .

We consider three metrics $(m_{1}, m_{2}, m_{3})$ as follows, although this method can be easily extended to more metrics. Recall quantifies the percentage of relevant items returned as results for a query. Latency denotes the average latency of query results. Traffic quantifies the bandwidth cost for searching a query. Thus, the utility function for query $q_{j}$ is given by

$$
\text { Utility } \left(q _ {j}\right) = \frac {m _ {1 , j} - m _ {1} ^ {\min}}{m _ {1} ^ {\max} - m _ {1} ^ {\min}} \times W _ {1} + \sum_ {i = 2} ^ {3} \left(\frac {m _ {i} ^ {\max} - m _ {i , j}}{m _ {i} ^ {\max} - m _ {i} ^ {\min}} \times W _ {i}\right) \tag {10}
$$

Using the set of Gnutella query logs, we randomly extract 6759 examples as a training data set to train a classifier. Each example is represented as $(\varpi_{\mathrm{q}}, \sigma_{\mathrm{q}}, \text{BestSearchType})$ , where the label BestSearchType is either “Flooding” or “DHT”, whichever has the better value of utility function. In order to get a good classifier, QRank varies $\alpha$ , the parameter scaling the contribution of $apTF_{t}$ in Eq.(4), and tests several SVM kernels, including linear, polynomial, and Gaussian. We use cross-validation technique [19] for training and testing. Table 1 summarizes the experimental results of the trained classifier. The results show that the trained classifier has good classification Precision, Recall, and F-Measure [19] for both search types.

Table 1. Classification of experimental results 

<table><tr><td>Search Type</td><td>Precision</td><td>Recall</td><td>F-Measure</td></tr><tr><td>Flooding</td><td>0.970</td><td>0.891</td><td>0.929</td></tr><tr><td>DHT</td><td>0.868</td><td>0.963</td><td>0.913</td></tr></table>

# 4. Hybrid search with QRank

In this section we introduce the operations of QRank. We first give an overview of QRank hybrid search, and then focus on the method of collecting global information in distributed P2P networks. We will also discuss how to improve the search performance by using adaptive methods.

# 4.1. QRank hybrid search

A QRank P2P network has four kinds of nodes: unstructured super peers, structured super peers, normal peers, and bootstrap peers. A normal peer publishes its title list to one or more unstructured super peers that are assigned to it by a bootstrap peer. Unstructured super peers store the lists of items present at a number of normal peers and execute query searching on their behalf. In order to enable both flooding and DHT search in each unstructured super peer, every unstructured super peer of QRank connects to at least one structured super peer. To reduce the overhead of DHT maintenance, only a small fraction of nodes with good connectivity and long uptimes are promoted to structured super peers and participate in the global DHT.

When a normal peer issues a query, the query is first sent to a connected unstructured super peer. The unstructured super peer computes $\varpi_{q}$ , $\sigma_{q}$ as the input of the embedded QRank classifier using the global statistical information of $f_{t}$ , $f_{t,p}$ , and N, which are defined in Section 3.3. The query is then checked by QRank classifier to select flooding or DHT.

# 4.2. Global information collection

QRank gathers the global statistic of $f_{t}$ , $f_{t,p}$ , and N in the query rank model using a pushing synopsis based random gossip algorithm. It is a variant of the distributed algorithm outlined in [13]. The algorithm has three main operations.

(1) Synopsis generation: at the initialization phase, each super peer browses its local title index and generates a local synopsis using the duplicated-insensitive counting technique pioneered by Flajolet and Martin [5]. We design the following synopsis data structure for the statistic of $f_{t}$ , $f_{t,p}$ , and N.

A synopsis (see Figure 2) includes: 1) bitvec\_peer, a bit vector for counting N, the global number of peers; 2) an index with the format: {(keyword, bitvec\_item\_keyword, bitvec\_peer\_keyword)}, where bitvec\_peer\_keyword is a bit vector for the statistic $f_{t,p}$ (the number of peers containing the keyword), and bitvec\_item\_keyword is the bit vector for the statistic $f_{t}$ (the number of items containing the keyword).

(2) Synopsis gossip: As we discussed in Section 3, the synopses are disseminated among super peers using a randomized gossip algorithm [6]. In each round of gossip a super peer chooses a random neighbor and sends the neighbor its synopsis. Figure 3 gives an example of one round of gossip, where nodes A-G are super peers.

![](images/4d01f60133642bc40705a2eb8a791e7ad0745d760df09215b9026fc5d46b9a8f.jpg)



Figure 2. Data structure of synopsis

![](images/fc805e0e13e6da8d5c486cbe422730438c6d9880ab92d0abc572c1e866de4088.jpg)



Figure 3. An example of one round of gossip

(3) Synopsis merging: When a super peer receives the synopsis from its neighbor, it will merge the synopsis as follows: 1) perform the bitwise-or operation on the bit vectors bitvec\_peer from both synopses for counting the global number of peers; 2) browse the two synopses, and for the keywords in both synopses perform the bitwise-or operation on the pair of bit vectors bitvec\_item\_keyword and the pair of bit vectors bitvec\_peer\_keyword; and 3) for those keywords in the synopsis of the neighbor but not in the local synopsis, perform a union operation.

The bitwise-or operation has the effect of computing the maximal of the CT values of the independent experiments in an order-insensitive manner. After $\log(n)$ rounds of gossip, every node gets the global statistics. If the first “1” bit counting from the left end of a bitvector is at the ith position, the global statistic count associated with the bitvector is, with high probobility, $2^{i}/0.77351$ . Figure 4 shows the process at Peer B after it merges the synopsis that Peer A gossips to it. Here we only show the bitvec\_item\_keyword part of the synopsis, and other parts have similar operations.

# 4.3. Adaptive hybrid search

Due to the dynamic property of P2P networks, the accuracy of QRank is influenced by the uptime of a peer. In adaptive search, when a new query is issued to an unstructured super peer, the peer first asks its neighboring super peers. If all the neighbors agree on the same search type, the agreed search type will be performed. Otherwise, the decision of the peer with longest uptime will be used. The maximum uptime $Uptime_{max}$ of neighbors will be tagged in the query to forward.

![](images/398b95669d00e773e201dc7d04daa6799f2c8a2f4043861076d295f8215b92ef.jpg)  
Figure 4. Synopsis merging

During flooding, when a query $(q, Uptime_{max})$ is forwarded to a super peer, the peer will compare $Uptime_{max}$ tagged with the query and its own uptime $Uptime_{local}$ . If $Uptime_{local} > Uptime_{max}$ , and the local classifier suggests the query should be looked in DHT, flooding will be stopped and a consequent DHT lookup will be performed. In order to prevent looking up DHT multiple times, this DHT lookup operation will be discussed with the source peer.

# 5. Simulation methodology

In this section we first discuss how we collect Gnutella traces. Then we introduce the design of our simulation system.

# 5.1. Gnutella trace collection

We developed a crawler to collect topology information of Gnutella. The crawlers are written in Java based on limewire's $[2]$ open source client, and run in parallel using 40 threads. It can explore more than 50,000 peers within half an hour.

Using the crawler we crawled 7 topologies with sizes of 31747, 34206, 45650, 48134, 57926, 68737, and 75643 nodes. In Figure 5, we plot the distribution of the node degree corresponding to the collected Gnutella Topology traces on a log-log scale. The plots of all data sets are in good agreement with previous results [14].

# 5.2. Simulation design

We wrote a simulator in Java to compare QRank with the GAB search technique. We first generate the underlying network topology. Based on generated network, we simulate hybrid P2P overlay and the search techniques.

![](images/3064e0987287d8e692034b307f781e7cce176944a6831ebb8e2f4d10b0b62a42.jpg)



Figure 5. Gnutella trace

In order to better represent real world systems, we consider both the underlying physical topology and the P2P overlay. We use BRITE $[1]$ to generate a physical topology with 100,000 nodes, and then use the Gnutella traces we collected to simulate the P2P overlay, where all P2P nodes are mapped into the underlying physical topology. The communication cost between two logical P2P neighbors is calculated based on the physical shortest path between this pair of nodes. The ultra peers of the Gnutella trace are nominated as unstructured super peers in the hybrid P2P overlay. The uptime of peers follows the distribution of Gnutella P2P systems reported in $[16]$ . About 10% ultra peers have an average uptime longer than 80 minutes and we nominate such peers as DHT nodes.

In order to compute the query popularity, we use the Gnutella query trace which we analyzed in Section 3. We simulate files with the file names generated from exact queries. The file distribution is computed according to the study result in [16] that files in P2P network exhibits popularity characteristics that fit a log-quadratic distribution $y = 10^{-2.98x^2 - 0.68 - 0.07}$ , where $x$ is the percentage of unique files ranked in log scale, and $y$ is the percentage of all files in log scale.

To gather global statistics, we simulate the push-synopsis based randomized gossip method. We also implement the $apTF \times IPF$ ranking model. QRank leverages the fact that the global statistics are slowly changing in the large scale P2P networks. Hence, infrequent computation of these statistics is sufficient for good performance. The communication cost for the gossiping algorithm is quite acceptable for a real world system.

# 6. Performance evaluation

QRank considers both search quality and efficiency. Quality focuses on user-perceived qualities, such as number of results, recall and search latency, while efficiency focuses on resource utilization, such as bandwidth cost.

Figure 6 plots the number of returned results for all the queries, in which 38.5% QRank queries return more than 100 results, but only 22% GAB queries do so, showing that QRank greatly outperforms GAB for highly replicated items.

Figure 6 also shows that 12.1% GAB queries return nothing while only 2.5% QRank queries return nothing, which means the hit rate for rare items is significantly increased. QRank reduces the number of queries that receive no results by 79%.

![](images/0f4d81655bf4632eaf98d38194f6e9b6b23b1c29857fa94005f03550542b0c16.jpg)



Figure 6. Number of results

![](images/164a2bdac8de0af5fcd5ece4036569a76f0228a20e209bcb04f61c4aa483dc64.jpg)



Figure 7. Recall rate

![](images/06d82bf407931c31f0d6373f86ed8d46e4f9fe88c8abe9fe64afe102b12a1d8d.jpg)



Figure 8. Average latency

![](images/a649ad6d59fb0d0cc5d4ebd65e27a85992e8f8c0406a4f6b95f64d901f1b6d2a.jpg)



Figure 9. Traffic cost

![](images/cc0f77438cad089d9ab68fb62e2bd1b13139923794ba7e4952dd0155cbc4a157.jpg)



Figure 10. Search efficiency

![](images/0765d1a7e7bd26982ad1c6fb55e08073c54fd33ed09cb0acc4ae45b3a8effe6c.jpg)



Figure 11. Utility

We also conducted offline experiments for the optimal search policy. With the optimal policy, every query is performed with either DHT or flooding, whichever has a better value for the utility function defined in Eq.(10). Figure 6 also plots how well the optimal search policy can do. We can see that the performance of QRank is very close to the optimal selection.

The Recall denotes the percentage of returned relevant items out of all relevant items in the network. Figure 7 plots the recall rate of all the queries where more than 68% queries using QRank have a recall rate higher than 80%. By using GAB, less than 40% queries have a recall rate higher than 80%. Figure 7 also shows that 72.9% QRank queries have a recall rate of 100% while 59.2 GAB queries have a recall rate of 100%. At the same time, 12.1% GAB queries have recall rate of 0% while only 2.5% QRank queries have recall rate of 0%. Figure 7 also plots how well the optimal search policy can do. We can see that the recall of QRank is very close to that of the optimal search selection.

Short search latency is always desirable in P2P systems. Figure 8 shows that about 45% QRank queries have short average latency less than 7 seconds, while only about 15% GAB queries achieve such short average latency.

We also noticed in Fig. 8 that a number of queries have average response time with only slight differences. This is because the latency of DHT is decided by the Chord [18] latency, $\frac{1}{2}\log N$ , where $N$ is the total number of the structured super peers in the hybrid P2P network.

P2P traffic has significant impact on the underlying network. Heavy network traffic limits the scalability of P2P networks. We define the traffic cost as network resource used in an information search process of P2P systems, which is mainly a function of consumed network bandwidth and other related expenses. Specifically, we assume that all the messages have the same length. When messages traverse an overlay connection during a given time period, the traffic is the summed traffic cost of all the hops. The traffic cost of a hop is given by: $Tc = M \sum_{i} L_{i} / B_{i}$ , where M is the size of the message and $L_{i}$ and $B_{i}$ respectively represent the length and the bandwidth of the physical links that this message traverses on the underlying physical network during this during this hop in the overlay.

Figure 9 plots traffic cost of all the queries. About 72% of QRank queries have a traffic cost less than $1.8 \times 10^{4}$ , while only 37% GAB queries achieve traffic cost less than $1.8 \times 10^{4}$ .

Figure 9 also plots how well the optimal search policy can do. It shows that the average query traffic of QRank is very close to that of the optimal search selection strategy.

To better evaluate the overall performance of QRank, we also define two comprehensive metrics: Search Efficiency and Search Utility.

Search Efficiency is defined as the ratio of recall to search traffic cost, $Efficiency = recall / traffic cost$ . It is a more fair comparison than looking at recall and search traffic cost separately. In P2P search we often desire to achieve higher recall with lower traffic cost.

Figure 10 shows the contrast of Search efficiency among QRank, GAB, and the optimal. We can see that QRank outperforms GAB. The statistical average search efficiency is increased by 177.2%. The efficiency of QRank is very close to that of the optimal search selection.

Search Utility, as defined in Section 4, considers multiple metrics, including average latency of results, recall and traffic cost, and is used to guide the selection of the classifier. As shown in Fig. 11, QRank improves search utility compared with GAB.

# 7. Conclusions

Hybrid search provides better search efficiency for P2P systems. To further improve its performance, we need to better estimate how many peers can answer a given query so as to determine a proper search strategy for the query. In this paper, we propose QRank, a query difficulty-aware scheme, which employs a push-synopsis based random gossiping algorithm to gather query information and term frequency. Using the rank values, QRank is able to better select a proper search strategy. We collect real P2P traces and design a trace-driven simulator to evaluate this design. Experimental results show that QRank significantly outperforms the existing approaches in terms of search efficiency and quality.

# 8. Acknowledgements

This work was supported in part by NSFC grant No.60433040, National 973 Key Basic Research Program under grant No.2003CB317003, and the Cultivation Fund of the Key Scientific and Technical Innovation Project, Ministry of Education of China under grant No.705034.

# References

[1] "BRITE, http://www.cs.bu.edu/brite."   
[2] "Limewire, http://www.limewire.com."   
[3] "Napster, http://www.napster.com."   
[4] Y. Chawathe, S. Ratnasamy, and L.Breslau, "Making Gnutella-like P2P Systems Scalable," In Proceedings of ACM SIGCOMM, 2003.   
[5] P. Flajolet and G. N. Martin, "Probabilistic Counting Algorithms for Data Base Applications," Journal of Computer and System Sciences, Vol. 31, 1985, pp. 182-209.

[6] D. Kempe, A. Dobra, and J. Gehrke., "Gossip-Based Computation of Aggregation Information," In Proceedings of IEEE FOCS, 2003.   
[7] K. L. Kwok, "A New Method of Weighting Query Terms for Ad-hoc Retrieval," In Proceedings of ACM SIGIR, 1996.   
[8] D. Li, X. Li, and J. Wu, "Fission E: A Scalable Constant Degree and Low Congestion DHT Scheme Based on Kautz Graph," In Proceedings of IEEE INFOCOM, 2005.   
[9] X. Liao, H. Jin, Y. Liu, L. M. Ni, and D. Deng, "AnySee: Peer-to-Peer Live Streaming," In Proceedings of IEEE INFOCOM, 2006.   
[10] Y. Liu, X. Liu, L. Xiao, L. M. Ni, and X. Zhang, "Location-Aware Topology Matching in P2P Systems," In Proceedings of IEEE INFOCOM, 2004.   
[11] B. T. Loo, J. M. Hellerstein, R. Huebsch, S. Shenker, and I. Stoica, "Enhancing P2P File-Sharing with an Internet-Scale Query Processor," In Proceedings of VLDB, 2004.   
[12] B. T. Loo, R. Huebsch, I. Stoica, and J. M. Hellerstein Proceedings of IPTPS, "The Case for a Hybrid P2P Search Infrastructure," In Proceedings of IPTPS, 2004.   
[13] S. Nath, P. B. Gibbons, S. Seshan, and Z. R. Anderson, "Synopsis Diffusion for Robust Aggregation in Sensor Networks," In Proceedings of ACM SenSys, 2004.   
[14] M. Ripeanu, A. Iamnitchi, and I. Foster, "Mapping the Gnutella Network," IEEE Internet Computing, Vol. 6, No.1, 2002, pp. 50-57.   
[15] G. Salton and C. Buckley., "Term Weighting Approaches in Automatic Text Retrieval," Information Processing and Management, Vol. 24, 1988, pp. 513-523.   
[16] S. Saroiu, P. Gummadi, and S. Gribble, "A Measurement Study of Peer-to-Peer File Sharing Systems," In Proceedings of Multimedia Computing and Networking (MMCN), 2002.   
[17] K. Sripanidkulchai, B. Maggs, and H. Zhang, "Efficient Content Location Using Interest-Based Locality in Peer-to-Peer Systems," In Proceedings of IEEE INFOCOM, 2003.   
[18] I. Stoica, R. Morris, D. Karger, F. Kaashoek, and H. Balakrishnan, "Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications," In Proceedings of ACM SIGCOMM, 2001.   
[19] V. Vapnik, The Nature of Statistical Learning Theory. New York: Springer, 1999.   
[20] L. Xiao, X. Zhang, A. Andrzejak, and S. Chen, "Building a Large and Efficient Hybrid Peer-to-Peer Internet Caching System," IEEE Transactions on Knowledge and Data Engineering, Vol. 16, No.6, 2004, pp. 754-769.   
[21] M. Zaharia and S. Keshav, "Gossip-based Search Selection in Hybrid Peer-to-Peer Networks," In Proceedings of IPTPS, 2006.   
[22] D. Zeinalipour-Yazti, V. Kalogeraki, and D. Gunopulos, "Exploiting Locality for Scalable Information Retrieval in Peer-to-Peer Networks," Information Systems, Vol. 30, 2005, pp. 277-298.