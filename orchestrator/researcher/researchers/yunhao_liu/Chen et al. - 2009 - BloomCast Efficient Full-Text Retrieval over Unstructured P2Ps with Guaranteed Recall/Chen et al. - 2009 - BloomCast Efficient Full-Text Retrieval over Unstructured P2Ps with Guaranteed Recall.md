# BloomCast: Efficient Full-Text Retrieval over Unstructured P2Ps with Guaranteed Recall

Hanhua Chen, Hai Jin

School of Computer Sci. and Tech.

Huazhong University of Sci. and Tech.

Wuhan, 430074, China

{chenhanhua,hjin}@hust.edu.cn

Xucheng Luo

School of Computer Sci. and Engin.

University of Electronic Sci. and Tech. of China

Chengdu, 610054, China

xucheng@uestc.edu.cn

Yunhao Liu, Lionel M. Ni

Department of Computer Sci. and Engin.

Hong Kong University of Sci. and Tech.

Clear Water Bay, Kowloon, Hong Kong

{liu, ni}@cse.ust.hk

# Abstract

Efficient and effective full-text retrieval in unstructured peer-to-peer networks remains a challenge in the research community. First, it is difficult, if not impossible, for unstructured P2P search protocols to effectively locate items with guaranteed recall rate. Second, existing schemes to improve search successful rate often rely on replicating a large number of item replicas across the wide area network, incurring a large amount of communication and storage cost. In this paper we propose BloomCast, an efficient and effective full-text retrieval scheme, in unstructured P2P networks. BloomCast is effective because it guarantees perfect recall rate with high probability. It is efficient because the overall communication cost of full-text search is reduced below a formal bound. Furthermore, by casting Bloom Filters instead of the raw documents across the network, BloomCast significantly reduces the communication cost and storage cost for replication. We demonstrate the power of BloomCast design through both mathematical proof and comprehensive simulations. Results show that BloomCast outperforms existing schemes in terms of both recall rate and communication cost.

# 1. Introduction

With the emergence of peer-to-peer (P2P) file sharing applications, such as Napster [25] and Gnutella [6], millions of users have used P2P systems to search desired data. A P2P network has also shown a great potential to become a popular network tool for sharing information on the Internet based on the following observations. First, information on the Internet resides on millions of sites in a distributed manner. P2P based systems have the ability to leave the shared, but distributed, data at their origins instead of collecting and maintaining them in a centralized repository. Second, there are significant performance, scalability, and availability benefits by distributing the indexing and querying loads over a large number of collaborating peers. Third, a distributed P2P search system is more robust than a centralized search system as the failure of a single server is unlikely to paralyze the entire search system. Finally, there is growing concern about the fact that the world is dependent on a few quasi-monopolistic search engines. It is difficult to guarantee that they always bring objective results to users due to their susceptibility to commercial interests, possible biases in geographic and thematic coverage, or even censorship for different reasons [1].

Existing P2P full-text search schemes can be divided into two types: DHT-based global index and federated search engine over unstructured protocols. DHT-based searching engines are based on distributed indexes that partition a logically global inverted index in a physically distributed manner. Due to the exact match problem of DHTs, such schemes provide poor full-text search capacity. In federated search engines over unstructured P2Ps [17, 19], queries are processed based on flooding. Search recall rate is difficult to be guarantied with acceptable communication cost.

Unstructured P2Ps are commonly believe to be the best candidate for supporting full-text retrieval because the matching operations can be handled at the nodes that store the relevant documents. Replication strategies are often utilized to improve search performance in unstructured P2Ps. The existing replication strategies can be divided into two categories. The first type is the query popularity aware strategies [9]. The number of replicas is determined by the query’s popularity. Cohen et al. [9] claims that the squareroot replication strategy, where the number of the replicas is proportional to the square-root of the query popularity/rate, has the optimal search performance. In this scheme, the items with high query rate are highly replicated for future query searching, thus the search performance for popular items are improved. However, it is also proved that this strategy is inefficient for solving “insoluble queries”, the queries for rare and non-existent items. The second type of replication strategy is independent of the popularity of the query, such as Bubblestorm [32] and RWPS [12]. By replicating a proper number of document replicas randomly across a P2P network, such kind of schemes can improve search recall rate greatly. However, since simply replicating document reference or selected metadata can not successfully support full text retrieval, existing replication strategies needs to replicate full document across the network, raising possibly unacceptable communication and storage costs.

To address the above problems, we propose a proper replication strategy, BloomCast, to support efficient and effective full-text retrieval in this paper. By replicating an optimal number of Bloom Filters (BF) [3], [27] of a document uniformly and randomly across the P2P network, Bloom-Cast can achieve perfect recall rate while significantly reducing the communication/storage cost for replicating. A BF is a lossy but succinct and efficient data structure to represent a set S, which can efficiently process the membership query such as “is the element x in the set S”. By transmitting and storing the encoded sets instead of raw documents among peers, the communication/storage costs can be effectively saved. We show that by distributing an optimal number of item and query replicas uniformly and randomly across the network BloomCast can achieve perfect recall rate with high probability while the optimal number of replicas is determined by the network size of P2P system. BloomCast hybridizes a lightweight DHT with an unstructured P2P overlay to support network size estimation and random node sampling. We conduct comprehensive simulation to evaluate this design. Results show that BloomCast can achieve perfect recall rate with largely reduced overhead.

The remainder of the paper is organized as follows. In Section 2, we discuss related work. Section 3 presents the design of BloomCast. We evaluate the performance of this design in Section 4. The conclusion is given in Section 5.

# 2. Related Work

Full-text content search is an important issue in distributed P2P information sharing systems. Without centralized index servers, nodes in a decentralized P2P system have to cooperate with each other to perform a fulltext search for desired documents. There is a large body of literature, which discusses the full-text search issue in P2P networks. Existing P2P content search schemes can be divided into two types: DHT-based distributed global inverted index on top of structured P2P networks [22] and federated search engines over unstructured P2P networks [19].

# 2.1 Full-text Search in Structured P2P Networks

DHT-based full-text searching engines utilize distributed global indexes, which partition a logically global inverted index in a physically distributed manner, to support multikeyword full-text searching. Existing distributed index mechanisms can be classified into two types: single-termbased inverted indexes and term-set-based indexes.

Built on existing DHTs, single-term-based distributed index can effectively support single keyword search by retrieving the list of documents/nodes for each single keyword. Because of the utilized exact hashing techniques, the DHT-based schemes, however, fail to support queries with multiple keywords. Tang et al. [31] proposed a hybrid index scheme, where frequent terms of a document are selected to be published into the global index. When such a keyword is published, the list of other terms in the document is replicated with the identifier of the document in the posting list. Multi-keyword search is performed by first locating the position of the DHT node which is responsible for a given keyword and then performing a local search for other keywords in the posting list. Finally only the list of documents that contain all the keywords is returned as the results. Little is known about the performance of the full text search using selected keyword publishing, because a few selected frequent terms may not be representative for a document [24]. Moreover, such replication strategy may incur unacceptable storage and communication cost. Another scheme performs a distributed intersection operation for multi-keyword search. Based on the global single term based inverted index built on DHT, the multi-keyword search looks up the sets for different keywords from multiple peers across the wide area network and returns the intersection. Although only a few nodes need to be contacted, each node has to send a potentially large amount of data across the wide area network, making such scheme unscalable. To improve, Reynolds et al.[23] used BFs to reduce such cost incurred by distributed intersection. In our previous work [8], [20], we showed through mathematical proof and extensive simulation that the optimal settings of a BF is determined by the popularizes of keywords other than the minimized false positive rate.

Another way to reduce the bandwidth cost is to precompute the index using term-set indexing. The major challenge of such scheme is that term-set-based index may need exponential index size. To reduce the unacceptable index size, Podnar et al. [22] proposed to index only highly discriminative keyword combinations in a distributed global index in a structured P2P network. Although their method can reduce the total number of combinations to be indexed, it is difficult to guarantee that the keyword set that users are interested in are exactly the keyword set selected for indexes. Motivated by the fact that queries can reflect the real information requirements of users, Bender et al. [2] proposed to index the term sets by considering the correlation between the keywords in queries. In their design, a DHT node stores additional posting lists for term sets that are strongly correlated with the terms it is originally responsible for. Although such term-set indexing schemes reduce the scale of indexes, it is difficult to build a complete search system on top of the proposed methods.

As we have seen above, efficient full-text search in structured P2P networks remains an open issue in the P2P community [15]. The root cause is that DHTs are based on their exact hashing schemes, providing poor search capacity.

# 2.2 Search in Unstructured P2P Networks

It is commonly believed that unstructured P2Ps are promising to provide full-text content searching in large scale distributed environments. In this kind of search networks, peers which maintain indexes of their local documents are organized in an ad-hoc fashion. Without a global index, unstructured P2P networks rely on flooding based schemes to distribute queries to the network and handle them on peers containing desired documents. Unstructured P2Ps, however, fail to provide efficient and effective search performance. A problem of unstructured P2P search engine is the limit of scalability in a large scale network due to the exponentially growing communication cost. The other problem is that the recall rate can not be guaranteed unless a query is flooded exhaustively throughout the network. A lot of efforts have been done to improve search efficiency.

Existing unstructured federated P2P search schemes often perform the query evaluation in two levels, the peer level and document level. The scheme first detects a group of peers with potential answers to the query, and then the query is submitted to the selected peers to evaluate the query against their local indexes and return the matched answers [11]. The search performance of unstructured federated P2P search engines can be further improved using super-peer based P2P architectures [26], which considers the inherent heterogeneity of peers [29]. Peers with more memory, processing power, and network connection capacity provide distributed directory services for resource location. Thus the peers with limited resources won’t become bottlenecks in the search network. Federated P2P search approaches can also take advantage of the enhancedproperties of the network topology [28], [10] to avoid a significant amount of unnecessary flooding. In [28] H. Zhang et al. proposed to link peers with similar interest. By forwarding the queries through the interest-based shortcuts, a significant amount of unnecessary flooding is avoided. Peers in Bibster [13] network advertise their expertise, a set of topics the peer is an expert in. Peers create semantic links to their neighbors according to the expertise similarity based on the received advertisements. Thus intelligent query routing protocol is designed by using the semantic links through the semantic overlay. SSW [10] dynamically clusters peers with semantically similar data closer to each other and maps these clusters in a high-dimensional semantic space into a one-dimensional small world network to improve the search performance.

Another promising scheme for content search in unstructured federated P2P systems is to utilize replication strategies to improve the search performance. By replicating items and queries properly across the network, such strategies can significantly improve the search successful rate while avoiding exhaustively flooding the unstructured P2P networks.

Existing replication strategies in unstructured P2P networks can be divided into two categories, the query popularity aware replication approach and the query popularity independent replication strategy.

In the query popularity aware replication strategies, the number of replicas is determined by the query popularity. Let $r _ { i }$ denote the number of replicas of item i.The sum of the replica amounts is $\begin{array} { r } { R \ = \ \sum _ { i = 1 } ^ { m } r _ { i } } \end{array}$ . Let $q _ { i }$ denote the query rate of item i, which is the fraction of all the queries that are issued for item i. The number of replicas in this strategy is $r _ { i } = f ( q _ { i } )$ . Two natural strategies among existing schemes are uniform and proportional strategies, while in the uniform replication strategy, all items are equally replicated, that is $r _ { i } = R / m$ . In the proportional replication strategy, the number of replicas is proportional to the query rates, that is $r _ { i } = R \times q _ { i }$ . Cohen et al. [9] have studied the two query-rate based strategies. Their results show that both the strategies are not better than square-root strategy, where the number of replicas is proportional to the square-root of the query rates. It is also proved that query popularity aware replication strategies are only efficient for“soluble queries”, while for the rare items, the search performance is low. Furthermore, how to identify popular and unpopular queries is difficult, if not impossible.

Recently, the query popularity independent replication strategy has attracted much attention. All items are equally replicated regardless of the popularity of the related queries. For full-text search, documents and queries are both replicated to some randomly selected nodes. Inspired by the birthday paradox [21], the well-chosen replica numbers guarantee the collision of document replica and query with high probability. RWPS [12] employs random walk to sample some random nodes. However, random walk is not fault-tolerant, a failed node in the path could reduce replica amount. Thus, the search success probability can not be guaranteed. On the other hand, random walk has long latency. To overcome the shortcoming of RWPS, Terpstra et al. propose Bubblestorm [32] to achieve probabilistically exhaustive search. Bubblestorm employs random multigraph to connect peers. A TCP based protocol is needed to keep the attributes of random multi-graph. A serious problem of query popularity independent replication strategy is that it can not support full-text search unless the whole documents are replicated. Thus, it raises a large amount of communication/storage cost in the network.

To address the above problems, we propose BloomCast, a novel replication strategy to support efficient and effective full-text retrieval in this paper. By replicating an optimal number of Bloom Filters instead of the raw documents uniformly and randomly across the P2P network, BloomCast can achieve perfect recall rate while significantly reducing the communication/storage cost for replicating. We further show the optimal number of replicas is determined by the network size of P2P system. We design a query language to support full-text search based on the Bloom Filter membership verification. BloomCast hybridizes a lightweight DHT with an unstructured P2P overlay to support network size estimation and random node sampling.

# 3. BloomCast

We model the replication strategy using Balls and Bins model, where each peer in the network is a bin while query replicas and data replicas are two sets of balls with different colors (Let the replicas of data be red balls and the replicas of a query green). Thus finding the desired item is similar to a procedure that the query and data item balls are tossed into bins with a specific strategy respectively and the balls of both color can meet in some bins. In large-scale P2P systems, it is not easy for requesters to know which bin contains the desired item balls and thereby toss the query ball into this bin. Intuitively, if the number of data item balls or queries is large enough, according to the Balls-and-Bins model, a collision of two kinds of balls in some bin can be guaranteed with high probability. Mathematically, over N bins, tossing r red balls and g green balls uniformly and randomly. The probability that no bin has both a green and red ball is

$$
1 - \frac {r \cdot q}{N ^ {2}} \cdot N = 1 - \frac {r \cdot q}{N} \tag {1}
$$

Thus, the probability that at least a bin contains both a red ball and a green ball can be bounded by

$$
p > 1 - e ^ {- \frac {r \cdot g}{N}} \tag {2}
$$

It is not difficult to see from the equation that for a given network scale the probability is monotonically increasing as the product $r \cdot g$ increases.

Let $e ^ { - { \frac { r \cdot g } { N } } } = 1 - p ^ { ' } = e ^ { - c ^ { 2 } }$ , we then have the following equation,

$$
r \cdot g = N \cdot c ^ {2} \tag {3}
$$

where $c = { \sqrt { - \ln ( 1 - p ^ { \prime } ) } }$

We assume the size of an item is d, while the size of a query is q. Thus the replication cost including document and the query can be roughly quantified by

$$
C o s t = r \cdot d + g \cdot q \tag {4}
$$

Given a specified upper bound of failure rate, the optimal replication strategy should achieve a minimized replication cost.

$$
\left\{ \begin{array}{l} \min (C o s t = r \cdot d + g \cdot q) \\ s. t. r \cdot g = N \cdot c ^ {2} \end{array} \right. \tag {5}
$$

The minimal cost can be achieved when $\begin{array} { r } { r = c \cdot \sqrt { \frac { N \cdot q } { d } } } \end{array}$ and $\begin{array} { r } { g = c \cdot \sqrt { \frac { N \cdot d } { q } } . } \end{array}$ . The result shows that the formal bound of the replication cost using BloomCast strategy is $O ( { \sqrt { N } } )$ ).

# 3.1. BloomCast Protocol

A challenge of the above model is that it can not provide real full-text search capacity unless the full documents are replicated. Even we replicate an optimal number of documents across the P2P network, the communication and storage cost may be unacceptable. For example, in the P2P network with 1,000,000 nodes, we need to deploy the scale of thousand document replicas across the wide area network. Assume each document have an average size of 1MB, then we need at least 1GB storage cost for replicating each document. This also incurs a large amount of communication cost in the wide area networks, making such schemes not feasible in real world distributed P2P networks.

To address this problem, we propose to use Bloom Filter [3], [27] to reduce the storage/communication costs. A BF is essentially a bit vector $b i t v e c _ { m }$ with m bits, initially all set to 0, that facilitates membership test to a finite set $S ~ = ~ \{ x _ { 1 } , x _ { 2 } , \ldots , x _ { n } \}$ of n elements from a universe U . It uses a set of k uniform and independent hash functions $\{ h _ { 1 } , h _ { 2 } , \ldots , h _ { k } \}$ to map the universe U to the bit address space $[ 1 - m ]$ . For each element x belonging to S, the bits $h _ { i } ( x )$ are set to 1 for i from 1 to k. To check whether an item y is in $S$ or not, we check whether all $h _ { i } ( y )$ are set to 1. If not, y clearly is not a member of S. If all $h _ { i } ( y )$ are set to 1, we assume that y is in S. After all the n elements of S are hashed and inserted into the BF, the probability that a specific bit of bitvecm is still 0 is

$$
p = (1 - (\frac {1}{m}) ^ {k n}) \approx e ^ {- k n / m} \tag {6}
$$

After n elements inserted into the $b i t v e c _ { m } ,$ , the probability of a false positive is the probability that a new element is not in S, but is separately hashed by the k hash functions to a number of k “1” bits of the bitvecm.

$$
f = (1 - p) ^ {k} = (1 - e ^ {- k n / m}) ^ {k} \tag {7}
$$

Given a specific ratio of m/n, i.e., the number of bits per element, it is easy to prove that the false positive rate f is minimized when and the minimal false positive rate is [4].

$$
f _ {m i n} = 0. 6 1 8 5 ^ {\frac {m}{n}} \tag {8}
$$

By distributing the document replicas in the form of Bloom Filters instead of a raw data, BloomCast is able to achieve significant cost savings while supporting accurate full text retrieval with high probability. The basic idea of the scheme is as below.

When a peer joins the network, it browses its local index. For each document it contains, it generates a Bloom Filter to represent it. It browses the document from the beginning to the end. When it meets a term in the document the first time, it inserts the term into the Bloom Filter by using the set of k hash functions, $\{ h _ { j } ( \cdot ) , 1 \leq j \leq k \}$ . When it meets the end of the document, it attaches the url and other information for this document to the Bloom Filter and samples random nodes in the network to deploy the replicas. Algorithm 1 describes the BloomCast Bloom Filter replicating strategy in detail.

Algorithm 1 Cast Bloom Filters   
Require: EstimatedNetworkSize = N is achieved
1: for all documents in local collection do
2: create an empty bit vector with m bits for document $x, BF_{x}$ ;
3: for all terms in a document do
4: insert t into $BF_{x}$ by using the set of hashing functions $\{h_{j}(\cdot), 1 \leq j \leq k\}$ ;
5: end for
6: end for
7: replicate $BF_{x}$ together with $url_{x}$ , the URL of X, to an optimal number of uniformly and randomly sampled nodes, which is determined by N;
8: return .

# 3.2. Query Evaluation

When a user issues a query, BloomCast protocol replicates it to an optimal number of randomly and uniformly sampled peers. Every involved peer checks all the Bloom Filters replicated locally. The member verification mechanism provided by the Bloom Filter can effectively enable multi-keyword full text retrieval. If all the keywords are tested to be contained in the Bloom Filter, the replica should be the desired result with high probability. The url of the document is then returned as the results for the client to download the document. If any keyword is tested to be not an member of the Bloom Filter, it is clearly not what the user wants. Note, due to the false positives of Bloom Filters, the returned results may contain undesired documents with very low probability. This may lead to a slight decrease of the precision of the final results while keeping the recall rate perfect. We will further discuss how to adjust the Bloom Filter settings to achieve the tradeoff between the precision and the communication cost. Algorithm 2 describe the query evaluation process in detail.

![](images/64b9f0e6a20f130b712fe0bb8607f454a9de413a8bb4980817159fd1a57814c4.jpg)



Figure 1. Hybrid Architecture of BloomCast

# 4. Performance Evaluation

In this section, we first introduce the simulation methodology. Then we present the performance evaluation results.

# 4.1. Simulation Methodology

To implement the above design, two key issues must be solved. The first is how to obtain the network size N, which determines the numbers of item replicas and query replicas. The second is the how to sample the optimal number of nodes randomly and uniformly. To address these problems, a hybrid architecture, which introduces a lightweight DHT subsystem in an unstructured P2P network, is utilized. Figure 1 shows the architecture of BloomCast. The DHT subsystem is composed of some stable nodes of the unstructured P2P. All nodes register their state information in the DHT subsystem. Nodes can access the DHT subsystem by way of random walk or DNS mapping function. We have introduced the hybrid P2P architecture in our previous work [7].

In the simulation, we vary the size of Gnutella topology from 50, 000 to 250, 000 nodes. A sub-set of the Gnutella ultra nodes are selected as the DHT nodes for node number estimating and node sampling. The Chord [30] protocol is used to connect the DHT nodes.

Algorithm 2 Query Evaluation of BloomCast   
1: $R \leftarrow \emptyset;$ 2: for all BFs replicated in this peer do
3: BooleanContainFlag $\leftarrow$ True;
4: for all terms Q do
5: if $\exists(j)(1 \leq j \leq k)s.t.BF_{x}[h_{j}(t)] = 0$ then
6:    ContainFlag $\leftarrow$ False;
7:    end if
8:    end for
9:    if ContainFlag = True then
10: $R \leftarrow R \cup \{url_{x}\};$ 11:    end if
12: end for
13: return R.

![](images/491424db3c4c046c588e5bb6a11cf8307d301541b0e28507dbb9b30cd5c74af4.jpg)



Figure 2. Recall of BloomCast

There has been no standard data set established for evaluating the performance of content-based P2P full-text retrieval [18]. Our simulations are based on Text Retrieval Conference (TREC) WT10G web corpus, a large test set widely used for performance evaluation in text retrieval research area. The dataset includes 10 gigabyte, 1.69 million web page documents and a set of queries [14]. All data set was stemmed with the Porter algorithm to reduce words to their root (e.g., “putting” becomes “put”) and common stop words such as “the”, “and”, etc. were removed from the data set [5].

# 4.2. Results

BloomCast considers both search quality and efficiency. Quality focuses on user-perceived qualities, while efficiency focuses on resource utilization. The main metrics for evaluating search performance include recall, replication cost per document, communication cost, and search efficiency.

![](images/c6d11e937d3c099ccec18442447d7d70e6271c97d8c97845bf055fc5608b6806.jpg)



Figure 3. Replication Cost of BloomCast

![](images/687f7de072e01cbbb13e0fc973bce9b771d9b527a69805d610ce33bfc531229b.jpg)



Figure 4. Communication Cost of BloomCast

The recall is defined as the percentage of relevant documents returned as results for a query. It is a widely accepted standard metric in the information retrieval research area.

$$
\text { Recall } (q) = \frac {\# \text {   of   relativant   documents   returned }}{\text { total   } \# \text {   of   relativant   documents   in   the   network }} \tag {9}
$$

where q is the query issued by a user. Ideally, a P2P user desire to achieve higher recall to 1.

As shown by Fig. 2, the BloomCast algorithm can achieve perfect recall rate. This is quite important for unstructured P2P networks, especially for unpopular items [7]. The results shows that by replicating an optimal number of replicas across the network, the BloomCast system can guarantee nearly 100% recall, making the search quality of unstructured P2P networks acceptable. The results also show that we can further control the recall rate by varying the number of replicas.

The replication cost per document examines how the Bloom Filter based item replication strategy can reduce the cost. In a P2P search system, such as P2P web search engines and large-scale digital library systems, where queries are more frequent than data creation, the replication strategy makes a good tradeoff. Although it needs some cost for replicating, it can be compensated for during the searching phase. Figure 3 shows that the total amount of data need for replication are greatly reduced. By replicating the Bloom Filters of documents instead of the raw documents, the proposed BloomCast is quite efficient.

The search communication cost is the total number of messages involved during search. The results in Fig. 4 show that the search communication cost of BloomCast are significantly smaller than Gnutella protocol. The communication cost of Gnutella increases fast when the network size increases while it increases slowly in BloomCast design.

![](images/5a772618cd1ccbd67e2c29bd6c5facd74afc34e0f6f883b6ac57fc825e5404ca.jpg)



Figure 5. Search Efficiency of BloomCast

The search efficiency is defined as the ration of recall to the communication cost.

$$
E f f i c i e n c y (q) = \frac {\text { Recall }}{\text { Communication   Cost }} \tag {10}
$$

It is a more fair comparison than looking at recall or communication cost separately [16]. Figure 5 shows the overall search efficiency. The results show that BloomCast can provide much better search efficiency than Gnutella.

According to the above results, BloomCast achieves the perfect recall rate at a low communication overhead.

# 5. Conclusion

In this paper we propose BloomCast, an efficient and effective full-text retrieval scheme, in unstructured P2P networks. BloomCast is effective because it grantees perfect recall rate with high probability. It is efficient because the overall communication cost of full-text search is reduced below a formal bound. Furthermore, by casting Bloom Filters instead of the raw documents across the network, BloomCast significantly reduces the communication cost and storage cost for replication. We demonstrate the power of BloomCast design through both mathematical proof and comprehensive simulations. Results show that BloomCast outperforms existing schemes in terms of both recall rate and communication cost.

# 6. Acknowledgement

This work is supported by National Natural Science Foundation of China (NSFC) and Research Grants Council (RGC) Joint Research Scheme under grant No.60731160630 and HKUST Nansha Research Fund and Hong Kong Research Grant Council N HKUST614\07.

# References

[1] M. Bender, S. Michel, P. Triantafillou, G. Weikum, and C. Zimmer. P2P Content Search: Give the Web Back to the People. In Proceedings of IPTPS, Santa Barbara, CA, USA, 2006.   
[2] M. Bender, S. Michel, P. Triantafillou, G. Weikum, and C. Zimmer. P2P Content Search: Give the Web Back to the People. In Proceedings of IPTPS 2006, 2006.   
[3] B. H. Bloom. Space/time trade-offs in hash coding with allowable errors. Communication of the ACM, 13(7):422–426, 1971.   
[4] A. Broder and M. Mitzenmacher. Network Applications of Bloom Filters: A Survey. Internet Mathematics, 1(4):485– 509, 2004.   
[5] J. Callan. Distributed information retrieval. Advances in Information Retrieval, pages 127–150, 2000.   
[6] Y. Chawathe, S. Ratnasamy, L. Breslau, N. Lanham, and S. Shenker. Making gnutella-like p2p systems scalable. In Proceedings of ACM SIGCOMM 2003, pages 407–418, Karlsruhe, Germany, 2003. ACM.   
[7] H. Chen, H. Jin, Y. Liu, and L. M. Ni. Difficulty-aware hybrid search in peer-to-peer networks. IEEE Transactions on Parallel and Distributed Systems (TPDS), 21(1), 2009.   
[8] H. Chen, H. Jin, J. Wang, L. Chen, Y. Liu, and L. M. Ni. Efficient multi-keyword search over p2p web. In Proceedings of WWW 2008, pages 989–998. ACM, 2008.   
[9] E. Cohen and S. Shenker. Replication strategies in unstructured peer-to-peer networks. In Proceedings of ACM SIG-COMM 2002, pages 177–190, Pittsburgh, PA, USA, 2002. ACM.   
[10] E. Courses and T. Surveys. Semantic small world: an overlay network for peer-to-peer search. In Proceedings of ICNP 2004, pages 228–238, 2004.   
[11] F. M. Cuenca-Acuna, C. Peery, R. P. Martin, and T. D. Nguyen. Planetp: Using gossiping to build content addressable peer-to-peer information sharing communities. In Proceedings of HPDC 2003, pages 236–246. IEEE, 2003.   
[12] R. A. Ferreira, M. K. Ramanathan, A. Awan, A. Grama, and S. Jagannathan. Search with probabilistic guarantees in unstructured peer-to-peer networks. In Proceedings of P2P 2005, pages 165–172, Konstanz, Germany, 2005. IEEE.   
[13] P. Haase, J. Broekstra, M. Ehrig, M. Menken, P. Mika, M. Plechawski, P. Pyszlak, B. Schnizler, R. Siebes, S. Staab, and C. Tempich. Bibster: A Semantics-Based Bibliographic Peer-to-Peer System. In Proceedings of ISWC, Hiroshima, Japan, 2004.   
[14] D. Hawking. Overview of TREC-9 Web Track. In Proceedings of TREC-9, pages 131–150, November 2000.   
[15] J. Li, B. Loo, J. Hellerstein, M. Kaashoek, D. Karger, and R. Morris. On the feasibility of peer-to-peer web indexing and search. In Proceedings of IPTPS 2003, pages 207–215, 2003.   
[16] T. Lin and H. Wang. Search performance analysis in peerto-peer networks. In Proceedings of IEEE P2P 2003, page 204, Washington, DC, USA, 2003. IEEE.

[17] J. Lu. Full-Text Federated Search in Peer-to-Peer Networks. PhD thesis, Carnegie Mellon University, 2007.   
[18] J. Lu and J. Callan. Federated search of text-based digital libraries in hierarchical peer-to-peer networks. In Proceedings of ECIR 2005, pages 52–66. Springer, 2005.   
[19] J. Lu and J. Callan. User modeling for full-text federated search in peer-to-peer networks. In Proceedings of the 29th annual international ACM SIGIR conference on Research and development in information retrieval, pages 332–339, NY, USA, 2006. ACM.   
[20] X. Luo, Z. Qin, J. Han, and H. Chen. DHT-assisted Probabilistic Exhaustive Search in Unstructured P2P Networks. In Proceedings of IEEE IPDPS 2008, pages 1–9, Miami, Florida, USA, 2008. IEEE.   
[21] R. Motwani and P. Raghavan. Randomized Algorithms. Cambridge University Press, Cambridge, 1995.   
[22] I. Podnar, M. Rajman, T. Luu, F. Klemm, and K. Aberer. Scalable peer-to-peer web retrieval with highly discriminative keys. In Proceedings of ICDE 2007, pages 1096–1105, Istanbul, Turkey, 2007. IEEE.   
[23] P. Reynolds and A. Vahdat. Efficient peer-to-peer keyword searching. In Proceedings of Middleware 2003, pages 21– 40.   
[24] S. Robertson. Understanding Inverse Document Frequency: on Theoretical Arguments for IDF. Journal of Documentation, 60:503–520, 2004.   
[25] S. Saroiu, K. Gummadi, and S. Gribble. Measuring and analyzing the characteristics of napster and gnutella hosts. Multimedia Systems Journal, 9(2):170–184, 2003.   
[26] H. Shen, Y. Shu, and B. Yu. Efficient Semantic-Based Content Search in P2P Network. IEEE Transactions on Knowledge and Data Engineering (TKDE), pages 813–826, 2004.   
[27] H. Song, S. Dharmapurikar, J. Turner, and J. Lockwood. Fast Hash Table Lookup Using Extended Bloom Filter: An Aid to Network Processing. In Proceedings of ACM SIG-COMM, Philadelphia, PA, USA, 2005.   
[28] K. Sripanidkulchai, B. Maggs, and H. Zhang. Efficient content location using interest-based locality in peer-to-peer systems. In Proceedings of INFOCOM 2003. IEEE.   
[29] M. Srivatsa, B. Gedik, and L. Liu. Large Scaling Unstructured Peer-to-Peer Networks with Heterogeneity-Aware Topology and Routing. IEEE Transactions on Parallel and Distributed Systems (TPDS), pages 1277–1293, 2006.   
[30] I. Stoica, R. Morris, D. Karger, M. F. Kaashoek, and H. Balakrishnan. Chord: a scalable peer-to-peer lookup service for internet applications. In Proceedings of ACM SIGCOMM 2001, pages 149–160, San Diego, California, USA, 2001. ACM.   
[31] C. Tang and S. Dwarkadas. Hybrid global-local indexing for effcient peer-to-peer information retrieval. In Proceedings of NSDI 2004, page 16, Berkeley, CA, USA, 2004. USENIX Association.   
[32] W. W. Terpstra, J. Kangasharju, C. Leng, and A. P. Buchmann. Bubblestorm: Resilient, probabilistic, and exhaustive peer-to-peer search. In Proceedings of ACM SIGCOMM 2007, pages 49–60, Kyoto, Japan, 2007. ACM.