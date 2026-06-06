# Optimizing Bloom Filter Settings in Peer-to-Peer Multikeyword Searching

Hanhua Chen, Member, IEEE, Hai Jin, Senior Member, IEEE, Lei Chen, Member, IEEE, Yunhao Liu, Senior Member, IEEE, and Lionel M. Ni, Fellow, IEEE

Abstract—Peer-to-Peer multikeyword searching requires distributed intersection/union operations across wide area networks, raising a large amount of traffic cost. Existing schemes commonly utilize Bloom Filters (BFs) encoding to effectively reduce the traffic cost during the intersection/union operations. In this paper, we address the problem of optimizing the settings of a BF. We show, through mathematical proof, that the optimal setting of BF in terms of traffic cost is determined by the statistical information of the involved inverted lists, not the minimized false positive rate as claimed by previous studies. Through numerical analysis, we demonstrate how to obtain optimal settings. To better evaluate the performance of this design, we conduct comprehensive simulations on TREC WT10G test collection and query logs of a major commercial web search engine. Results show that our design significantly reduces the search traffic and latency of the existing approaches.

Index Terms—Bloom filter, DHT, multikeyword search, P2P.

# 1 INTRODUCTION

With the emergence of peer-to-peer (P2P) [1] file sharing applications, millions of users have used P2P systems to search desired data. A P2P network has also shown a great potential to become a popular network tool for sharing information on the web [2], where information resides on millions of sites in a distributed manner. P2P-based systems have the ability to leave the shared, but distributed, data at their origins instead of collecting and maintaining them in a centralized repository.

Existing P2P retrieval mechanisms provide a scalable distributed hash table (DHT) [3] that allows every individual keyword to be mapped to a set of documents/nodes across the network that contain the keyword. Using this single-keyword-based index, a list of entries for each keyword in a query can be retrieved by using existing DHT lookups. For multikeyword search, the simple solution which merges the results of each keyword search incurs a lot of traffic. Given

- H. Chen and H. Jin are with the Services Computing Technology and System Laboratory, Cluster and Grid Computing Laboratory, School of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan 430074, China.
E-mail: {chenhanhua, hjin}@hust.edu.cn.   
- L. Chen is with the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong. E-mail: leichen@cse.ust.hk.   
- Y. Liu is with the TNLIST, School of Software, Tsinghua University, China, and the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong. E-mail: yunhaoliu@greenorbs.com.   
- L.M. Ni is with the Shanghai Key Lab of Scalable Computing and Systems at Shanghai Jiao Tong University, Shanghai, China, and the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong.
E-mail: ni@cse.ust.hk.

Manuscript received 18 Mar. 2008; revised 10 Oct. 2008; accepted 5 Nov. 2010; published online 21 Dec. 2010.
Recommended for acceptance by D. Cook.
For information on obtaining reprints of this article, please send e-mail to: tkde@computer.org, and reference IEEECS Log Number TKDE-2008-03-0150. Digital Object Identifier no. 10.1109/TKDE.2011.14.

an example, considering a two-keyword query “peer-to-peer network,” the query is decomposed into “peer-to-peer” and “network” and then the two keywords are searched separately with a consequent intersection operation. A potentially large amount of data traffic will be raised across the wide area network.

It is well known that Bloom Filter (BF) [4] is an effective way to reduce such communication cost [5], [6]. A BF is a lossy but succinct and efficient data structure to represent a set S, which can efficiently process the membership query such as “is the element x in the set S.” By transmitting the encoded sets instead of raw sets among peers, the communication cost can be effectively saved. Applying BF is not difficult, but how to get optimal results in terms of minimum communication cost is not trivial.

In this work, we show mathematically that the optimal setting of BF in terms of communication cost is determined by the global statistical information of the involved items on both sides, not the minimized false positive rate as claimed by the previous studies [5]. We further demonstrate how to get optimal settings through numerical analysis. Moreover, we find that the intersection order between sets is indeed important for multikeyword search; thus, we design optimal order strategies based on BF for both queries with "AND" and "OR" operators.

We conduct comprehensive trace-driven simulations on Text Retrieval Conference (TREC) WT10G [7] test collection and the query logs of a major commercial web search engine to evaluate the performance of this design. Results show that our design significantly reduces the search traffic and latency of the existing approach, respectively.

To summarize, we made the following main contributions in this work:

1. We show mathematically that the optimal setting of BF in terms of traffic cost is determined by the numbers of items involved on both sides when using a BF.

2. We derive an effective approach to achieve BF optimal settings through numerical analysis.

The road map of this paper is outlined as follows: Section 2 discusses related work. Section 3 introduces the system design. Section 4 describes the simulation methodology. Performance evaluation is presented in Section 5. We conclude the paper in Section 6.

# 2 RELATED WORK

There are generally two types of decentralized P2P search engines: federated search engines over unstructured P2P networks and DHT-based distributed global inverted index on top of structured P2P networks.

In federated search engines, peers that maintain indexes of their local documents are organized in an ad hoc fashion. A simple search method is flooding. Each query is tagged with a maximum Time-To-Live (TTL) to limit the number of hops it travels. In order to reduce the search cost, many approaches have focused on the issue of query routing.

The proposed algorithms often need to perform the query search in two levels, the peer level and document level. First, a group of peers with potential answers are detected. Second, the query is transferred to the selected most relevant peers to evaluate the query against their local indexes and return the matched answers. Finally, the retrieved answers are merged to produce a single answer set for the user. In PlanetP [8], each peer replicates a global term-to-peer inverted index which contains a mapping “ $t \to p$ ” if term $t$ is in the local index of peer $p$ . For each query, it ranks the peers using an IDF-like relevance model. In practice, it is difficult for every node to maintain such global index information in a large-scale network.

The search performance of a federated search engine can be further improved using superpeer-based P2P architectures [9], which consider the inherent heterogeneity of peers. In this kind of architecture, peers with more memory, processing power, and network connection capacity provide distributed directory services for efficient and effective resource location. Thus, the peers that are limited in these resources won't become bottlenecks in the network. In [10], Shen et al. proposed a hierarchical summary indexing framework for efficient content search in superpeer P2P networks. In their scheme, the documents are summarized in three levels: document level, peer level, and super peer level. For each level, the summarization process consists of two steps. In the first step, they use VSM to represent the information of this level as vectors, where each component of the vector corresponds to the importance of a term. The vectors are then further reduced from a large-dimensional space to a much smaller one using SVD to facilitate indexing. For searching, they extend the existing high-dimensional indexing technique—Vector Approximation file (VA-file) to perform efficient $K$ Nearest Neighbor (KNN) searching for text documents.

Another approach to improve the search performance of the federated search design takes advantage of the enhanced properties of its network topology. Zhang and colleagues [11] identify the natural principle in Gnutella and other P2P networks called interest-based locality, which reveals that a P2P user often stores similar items. Peers with similar interest are linked together. By forwarding the queries through the interest-based shortcuts, their scheme reduces a significant amount of unnecessary flooding. In Bibster [12], peers advertise their expertise, which contains a set of topics that the peer is an expert in. Other peers may accept these advertisements or not, thus creating a semantic link to their neighbors. These semantic links form a semantic overlay for intelligent query routing. A language model-based method is designed by Lu and Callan [13] to locally rank the neighboring peers. Queries are forwarded to the top-ranked neighbors who are most likely to have the answers. An SSW [14] overlay network dynamically clusters peers with semantically similar data closer to each other and maps these clusters in a high-dimensional semantic space into a one-dimensional small-world network that has an attractive trade-off between search path length and maintenance costs.

DHT-based searching engines are based on distributed indexes that partition a logically global inverted index in a physically distributed manner. Currently, there are two kinds of distributed index mechanisms: single-term-based inverted indexes and term-set-based indexes.

Searching with a single-term-based distributed index can retrieve the list of documents/nodes for each keyword in a query. In $[15]$ , frequent terms of a document are selected to be published into the global index. When such a keyword is published, the list of other terms in the document is replicated with the identifier of the document in the posting list. Multikeyword search is performed by first locating the position of the DHT node which is responsible for a given keyword and then performing a local search in the posting list for other keywords. Finally, the list of documents that contain all the keywords is returned as the results. Little is known about the performance of the full text search using selected keyword publishing, because a few selected frequent terms may not be representative for a document $[16]$ and such replication strategy may incur unacceptable storage and communication cost. Another scheme performs a distributed intersection operation for multikeyword search. Based on the global single-term-based inverted index built on DHT, the multikeyword search looks up the sets for different keywords from multiple peers across the wide area network and returns the intersection. Although only a few nodes need to be contacted, each node has to send a potentially large amount of data across the wide area network. Zhang and Suel $[6]$ propose to use multiple rounds BFs to reduce the cost for large-scale textual collections. By transmitting the BFs of sets instead of raw sets among peers, block by block, the BF-based schemes effectively reduced the communication cost. Reynolds and Vahdat $[5]$ claim that optimal BF settings can be achieved through minimizing the false positive of a BF. In this paper, we show that minimizing the false positive of a BF is far from optimal settings.

Another strategy to reduce the communication cost is to precompute the index using term-set indexing techniques. Some preliminary experiments in $[17]$ have shown that the term-set-based indexing is promising for multikeyword search across the wide area network. However, the major drawback of term-set-based index is the exponential index size. To reduce the unacceptable index size, Podnar et al. [18] proposed to index only highly discriminative keyword (HDK) combinations in a distributed global index. Although their method can reduce the total number of combinations in the global index, a large number of keys generated by HDK schemes are never or rarely used in queries, causing substantial consumption of both resources of bandwidth and storage. In [19], the HDK indexing schemes are extended by taking into account the popularity of term combinations appearing in user queries. The query-driven indexing (QDI) strategy uses query statistics to filter out superfluous keys. However, the scheme relies on a very large query log, which probably is unavailable for nodes in a P2P system. Bender et al. [20] proposed to index keyword sets in queries issued by P2P users. In their design, a DHT node responsible for keyword x stores additional posting lists for term sets including x that are frequently searched together in previous query logs. Although such a term-set indexing scheme reduces the scale of indexes, it suffers from the problem of cold start because a distributed intersection operation is also required if a query has not been searched before.

# 3 SYSTEM DESIGN

In this section, we first give a brief overview of our hybrid P2P network design for P2P multikeyword search, and focus on how to optimize the communication cost of DHT-based multikeyword search using an optimal BF. We then describe the optimization strategies for “AND” queries and “OR” queries. In Section 3.3, we propose an optimized intersection-order strategy for multikeyword queries. We present the pushing synopsis gossip algorithm for collecting global statistical information in Section 3.4. Section 3.5 shows how to solve the scalability problem in our design.

# 3.1 Solution Outline

In this design, a hybrid P2P network $[21]$ is a combination of 1) an unstructured P2P network which can use a gossiping algorithm to gather global statistical information, and 2) a BF enabled overlay based on DHT global inverted indexes. Each peer participates in an unstructured network and acts as a structured DHT node as well. (For example, in the P2P web search application, a peer represents a webserver.) With the facility of an unstructured network, the system utilizes a push-synopsis gossip algorithm for gathering the global statistical information such as keyword popularity. For keyword search, an inverted index can be built based on existing DHT lookup services $[3]$ which associates a keyword to a posting list of documents containing the keyword. While our approach is general to any of these DHT techniques, for simplicity, the following discussion assumes architecture closely related to the Chord protocol $[3]$ . In order to reduce the communication cost, we use a BF for distributed intersection and union required by the multikeyword search. When a query comes, peers can minimize the communication cost by adjusting BF parameters to optimal settings according to the statistical popularity of the keywords in the query.

The virtual host technique [22] has been widely used to address the load balance issue of decentralized structure P2Ps caused by the wide variation in node capacity (heterogeneity) and heavy-tailed query distributions (skew). Using the concept of virtual servers, each physical node can be responsible for more than one logical host depending on its capacity. For example, in Chord, each virtual server is responsible for a contiguous region of the identifier space but a physical node can own noncontiguous portions of the ring by having multiple virtual servers. By transferring virtual servers from heavily loaded nodes to lightly loaded nodes, existing schemes can solve the problem of load balances in decentralized DHTs. In this design, we use the strategy proposed by Rao et al. [22], where each light node periodically and randomly probes a heavy node in the DHT. Then, the heavy node selects and transfers to the light one a virtual server, which will not make the light one overloaded. Since the network bandwidth is the major resource bottleneck in webserver-like workload [22], in the design, we mainly focus on the communication cost. To cope with the unbalanced load caused by skewed distribution of query terms, we can use the splitting and merging strategies proposed by Rao et al. [22], where the bandwidth cost for each virtual server is monitored. When the load of a virtual server is higher than a predefined threshold, we split the virtual server by dividing the length of the ID space owned by the virtual server. Thus, the load of a virtual server in the DHT can be bounded by a predefined threshold. In the same way, the light load virtual servers can be merged into a new virtual server with the load within the bound.

![](images/0d7da5b4f3c4aab384babd8d83d335f42431854811a1d3e7f94a24f1a7822036.jpg)



Fig. 1. Queries length distribution.

# 3.2 Minimizing Communication Cost for Multikeyword Search

Before we discuss the mechanism for reducing the communication cost for multikeyword search, we introduce the following concepts:

Observations on user behaviors. We recently analyzed four months query logs of a major commercial web search engine. The query length distribution is plotted in Fig. 1, from which we can observe that 56 percent of the queries consist of at least two terms. This indicates that multikeyword search is quite common in web content searching.

Bloom filter. We review the basic of BF, following the framework of references [4]. A BF is essentially a bit vector $bitvec\_m$ with m bits, initially all set to 0, that facilitates membership test to a finite set $S = \{x_{1}, x_{2}, \ldots, x_{n}\}$ of n elements from a universe U. It uses a set of k uniform and independent hash functions $\{h_{1}, h_{2}, \ldots, h_{k}\}$ to map the universe U to the bit address space $[1 - m]$ . For each element x belonging to S, the bits $h_{i}(x)$ are set to 1 for

TABLE 1
Notations Used in the Algorithm 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $n$ </td><td>Number of elements inserted into a BF</td></tr><tr><td> $m$ </td><td>Size of the bit vector used as a BF</td></tr><tr><td> $k$ </td><td>Number of hash functions used for a BF</td></tr><tr><td> $f$ </td><td>False positive rate of a BF</td></tr><tr><td> ${f}_{min}$ </td><td>Minimized false positive rate of a BF</td></tr><tr><td> $X$ </td><td>The set of the IDs of the documents that containing keyword  $x$ </td></tr><tr><td> ${BF}\left( X\right)$ </td><td>The BF for set  $X$ </td></tr><tr><td> $Y \cap {BF}\left( X\right)$ </td><td>The estimated intersection of sets  $X$  and  $Y$  based on  $\operatorname{BF}\left( X\right)$  and  $Y$ </td></tr><tr><td> $r$ </td><td>Number of bits each item in the posting list takes</td></tr></table>

$1 \leq i \leq k$ . To check whether an item y is in S or not, we check whether all $h_{i}(y)$ are set to 1. If not, y clearly is not a member of S. If all $h_{i}(y)$ are set to 1, we assume that y is in S.

After all the $n$ elements of $S$ are hashed and inserted into the BF, the probability that a specific bit of bitvec\_m is still 0 is

$$
p = \left(1 - \frac {1}{m}\right) ^ {k n} \approx e ^ {- k n / m}. \tag {1}
$$

After n elements inserted into the bitvec\_m, the probability of a false positive is the probability that a new element is not in S, but is separately hashed by the k hash functions to a number of k "1" bits of the bitvec\_m.

$$
f = (1 - p) ^ {k} = \left(1 - e ^ {- k n / m}\right) ^ {k}. \tag {2}
$$

Before we introduce our algorithm for multikeyword search, we list the notations used in our algorithm in Table 1.

# 3.2.1 AND Query

A common solution for a multikeyword search needs conducting a distributed intersection operation in a wide area network. Fig. 2a gives an example of a two-keyword $(x, y)$ search. The query is first routed to the DHT node which is responsible for keyword x. Then, X, the set of identifiers of documents that contain keyword x, is transmitted to the node which is responsible for keyword y for a consequent intersection operation to achieve $X \cap Y$ , where Y is the set of document identifiers whose corresponding documents contain keyword y. The final results are returned to the client.

Based on the analysis of the four months query logs in the WT10G data collection, we find that in most cases, the minimal cardinality of the set of documents that contain any single keyword in a query is much larger than the cardinality of the intersection of all the sets. Thus, in a DHT-based P2P web search system, the straightforward distributed intersection operation only achieves a relatively small result set at the cost of sending complete sets in the wide area network. Clearly, the communication cost can be saved by transmitting the BF of sets instead of raw sets among peers for distributed intersection. Existing work $[5]$ claimed that minimizing the false positive rate of a BF is most efficient in reducing the communication cost. In this paper, we show that this is not the case.

![](images/a00c8662efe1faaaed117137d8927f00d18a286ccec9465335ca1061586df35d.jpg)



(a)

![](images/5ed2382ae9ca46eb3b701aabd80fbf32df73bc433df4503440daf9ad145f3643.jpg)



(b)   
Fig. 2. Straightforward distributed intersection versus BF-based strategy.

# Algorithm 1 Distributed algorithm for "AND" query

Require: Query q (x and y);

Lists of postings separately containing x and y and accommodated by DHT nodes $S_{x}$ and $S_{y}$ in a distributed manner.

Ensure: List of documents containing both $x$ and $y$

Step (1): issue query

1: Client chooses $S_{x}$ to send query $q(x,y)$ .

Step (2): compute BF(X)

1: $S_{x}$ identifies the set X which contains all the documents containing x.   
2: $S_{x}$ generates a BF with optimal settings for X using hash functions $\{h_{j}(.), 1 \leq j \leq k\}$   
3: $S_{x}$ transmits BF(X) to $S_{y}$ .

Step (3): compute $Y \cap \mathrm{BF}(X)$

1: $S_{y}$ identifies the set Y which contains all the documents containing y.   
2: $Y \cap BF(X) \leftarrow \emptyset$   
3: for i = 1 to |Y| do   
4: $S_{y}$ checks $b_{i}$ , an item of Y against BF(X) with hash functions $\{h_{j}(.), 1 \leq j \leq k\}$ .   
5: if $\forall(j)(1\leq j\leq k)$ , s.t. $h_{j}(b_{i})=1$ then   
6: $Y \cap BF(X) \leftarrow (Y \cap BF(X)) \cup \{b_i\}$ .   
7: $S_{y}$ transmits $Y \cap \mathrm{BF}(X)$ to $S_{x}$ .

Step (4): reverse verification

1: $S_{x}$ picks out the false positive.   
2: $X \cap Y \leftarrow X \cap (Y \cap BF(X))$ .   
3: $S_{x}$ sends the results $X \cap Y$ to the client.

For the same example discussed above, our design reduces the communication cost by sending an optimal BF based on X, BF(X), instead of sending X itself, as illustrated in Fig. 2b. When BF(X) is transmitted to the DHT node which is responsible for keyword y, the node determines the intersection of X and Y based on BF(X). Because the BF has no false negatives, the result set will contain all elements of the true intersection. Due to the possible false positives, the result set may contain elements that contain only keyword y but not x. Typically, a client would like to retrieve only the exact intersection of X and Y. Thus, the result set, denoted by $Y \cap \text{BF}(X)$ , is sent back to the DHT peer responsible for keyword x to remove the false positives from $Y \cap \text{BF}(X)$ by calculating $X \cap (Y \cap \text{BF}(X))$ , which is equivalent to $X \cap Y$ . Algorithm 1 shows the process of distributed intersection for “AND” queries in detail.

Note that for large inverted lists, we may need to transfer the lists block by block using multiple rounds of Bloom Filters $[6]$ . For simplicity, in this paper when introducing the BF optimization scheme, we use only one round of BF, which encodes the entire list. We will see that the BF optimization technique is general to the cases with different rounds of BFs.

Given a fixed false positive $f$ , if the fraction $\lambda$ of the elements of $Y$ actually contain $x$ , that is to say $\lambda = \frac{|X \cap Y|}{|Y|}$ , the number of the extratransmitted elements is in proportion to $(1 - \lambda)|Y|$ .

Thus, the communication cost of the BF-based intersection is quantified by

$$
m + (1 - \lambda) f | Y | r + 2 | X \cap Y | r. \tag {3}
$$

We assume that each element in the set takes r bits. To minimize the communication cost of BF-based distributed intersection algorithms, the communication cost for transmitting $X \cap Y$ can be ignored [5] since it represents the final intersection result, which must be sent back. We substitute f from (2). Thus, the extra communication cost for distributed intersection is

$$
f (m, k) = m + (1 - \lambda) (1 - e ^ {- k | X | / m}) ^ {k} | Y | r.
$$

In [5], Reynolds and Vahdat quantified the extra communication cost by ignoring $\lambda$ based on the observation that $|X \cap Y|$ is much less than $|Y|$ in large collections in most cases, which agrees with the analysis results based on our query logs and data set. In the analysis for the extra communication cost of distributed intersection algorithm in this paper, we follow the same approximation and consider the upper bound of the extra communication cost quantified by

$$
f (m, k) \leq m + (1 - e ^ {- k | X | / m}) ^ {k} | Y | r. \tag {4}
$$

Equation (4) shows that the minimized communication cost can be achieved by adjusting the settings of BFs. As (4) shows, the optimal settings are determined by the global statistical information of keywords, not simply by the minimized false positive rate as claimed in [5].

In [6], Zhang and Suel have shown how to expand Bloom Filter techniques to cope with the queries with arbitrary number of keywords using multiple petals effectively and efficiently, each petal performing the intersection for the inverted list for one term. In this design, we address a different problem—how to achieve the optimal BF settings in different petals. To describe the problem addressed in this design more clearly, we follow the communication structure in [6] and illustrate the process in more detail in Fig. 3.

Fig. 3b shows an example of processing queries with three keywords. For simplicity, here we use only one round of BF [6]. The DHT node for keyword x first transfers $\mathrm{BF}(X)$ to the DHT node for keyword y, which checks the documents in Y against $\mathrm{BF}(X)$ and transfers the $Y \cap \mathrm{BF}(X)$ back to the node for keyword x. Then, the node for x filters the false positives and obtains the exact intersection $X \cap Y$ . In step (2), the node for x calculates the optimal setting of $\mathrm{BF}(X)$ according to $|X|$ and $|Y|$ . In the second petal, including steps (4)-(6), the node for x transfers the $\mathrm{BF}(X \cap Y)$ to the node for z to obtain the exact intersection $X \cap Y \cap Z$ in the same way. In steps (2) and (4), the BFs will separately use the optimal numbers of involved items on both sides. It is clear that the optimal settings can be achieved to expand the algorithm to support longer queries. In Section 5.2, we show how we achieve the optimal settings of a BF in detail.

![](images/4460ed26cb60df2b30d710f1d00f90a0d2c033402b262a8dd116782830bc3752.jpg)



(a)

![](images/f1853e59635290fdac7bab19d420acda2b52d85fccad4f366d05217728209162.jpg)



(b)   
Fig. 3. Intersection algorithms for a query with more keywords.

In the algorithm for “AND” queries, it is also possible to send $Y \cap \text{BF}(X)$ directly to the client rather than first sending it back to the DHT node responsible for keyword x. This will further reduce more communication cost but suffer from a slight loss in the result precision due to the false positive of BF. Given reasonable values of $|X|$ , $|Y|$ , k, and m, the upper bound of the number of the transmitted wrong elements is $(1 - e^{-k|X|/m})^{k}|Y|$ . The upper bound of the precision of the final result is $\frac{|X \cap Y|}{|X \cap Y| + (1 - e^{-k|X|/m})^{k}|Y|} \times 100\%$ .

# 3.2.2 OR Query

In some applications, we need "OR" queries, which desire the results containing any keyword in the query. Such query is critical for queries whose keywords are rare in the system. A search engine may combine both the "AND" and "OR" results for a multikeyword query to the users. Fig. 4a presents an example of the straightforward strategy for a two-keyword "OR" query. At the beginning, the query is separately sent to the DHT nodes responsible for keywords $x$ and $y$ , respectively. Then, the DHT nodes separately send back the complete list for each keyword. At last, the results of both keywords are merged at the client. Thus, the total communication cost is $(|X| + |Y|)r$ .

In our design shown in Fig. 4b, the query is first routed to the DHT node which is responsible for keyword x. Then, BF(X) will be forwarded to the DHT node that is responsible for keyword y to pick out the documents which are not in X by checking elements in Y using BF(X). Only the set picked out, denoted by Y-BF(X), is returned to the client for a consequent union operation. Algorithm 2 shows the process of distributed union for “OR” queries in detail. The communication cost can be quantified as

$$
\begin{array}{l} m + (| X | + | Y - B F (X) |) r = m \\ + (| X | + (1 - f) (| Y | - | X \cap Y |)) r. \tag {5} \\ \end{array}
$$

![](images/cba9ab7c1eda84970dceb62758c85a260a09c358df589e29185f08a1d0828799.jpg)



(a)

![](images/cdaae01c02c7d21b99329109a9b6c4515f4306b950d2a28f081937d463d3eaf2.jpg)



(b)   
Fig. 4. Straightforward distributed union versus BF-based strategy.

Algorithm 2 Distributed algorithm for "OR" queries   
Require: Query q (x or y);
Lists of postings separately containing x and y and accommodated by DHT nodes $S_{x}$ and $S_{y}$ in a distributed manner.

Ensure: The estimated set of documents containing $x$ or $y$

Step (1): issue query

1: Client chooses $S_{x}$ to send query q (x, y).

Step (2): return result $X$

1: $S_{x}$ identifies the list of postings $X$ which contains the documents containing $x$ .

2: $S_{y}$ sends X to the client.

Step (3): computing BF(X).

1: $S_{x}$ creates an empty m-bits bit vector for $\mathrm{BF}(X)$ , the bloom filter with minimized false positive, for X.

2: $S_{x}$ generates a BF with optimal settings for $X$ using hash functions $\{h_j(.), 1 \leq j \leq k\}$ .

3: $S_{x}$ transmits BF(X) to $S_{y}$ .

Step (4): estimate union

1: $S_{y}$ identifies the list of postings, $Y$ , which contains the documents containing $y$ .

2: $Y - BF(X) \leftarrow \emptyset.$

3: for i = 1 to |Y| do

4: $S_y$ checks item $b_i$ against BF(X) by using hash functions $\{h_j(.), 1 \leq j \leq k\}$ .

5: if $\exists(j)(1 \leq j \leq k)$ , s.t. $h_{j}(b_{i}) = 0$ then

6: $Y - BF(X) \leftarrow (Y - BF(X)) \cup \{b_i\}.$

7: $S_{y}$ transmits $Y-\mathrm{BF}(X)$ to the client.

By avoiding repeatedly sending the intersection of X and Y, our algorithm for distributed union is promising for reducing traffic cost of some queries (especially, the queries consist of rare but strongly correlated terms). Mathematically, the benefit of communication cost by BF is

$$
M _ {s a v e d} = (| X | + | Y |) r - (m + | X | r + (1 - f) | Y - X | r)
$$

$$
= (1 - f) | X \cap Y | r + f | Y | r - m.
$$

Using the global statistics information of keywords, we can use a threshold to select the strategy. If $\frac{M_{saved}}{(|X|+|Y|)r} > \delta$ , where $\delta$ is a threshold, we use BF for distributed union operation; otherwise, we use the straightforward strategy. Note that $Y\text{-BF}(X)$ is slightly different from $Y - X$ due to the false positives. Thus, some results of $X \cap Y$ will be missed in the final results. Given reasonable values of $|X|$ , $|Y|$ , $m$ , and $k$ , the number of missed elements is in proportion to $|Y - X|$ , equivalent to $|Y| - |X \cap Y|$ . Specifically, $Y\text{-BF}(X)$ will miss $(1 - e^{-k|X|/m})^k |Y - X|$ elements that belong to $Y$ . Thus, the recall of the final result will slightly decrease by $\frac{(1 - e^{-k|X|/m})^k (|Y| - X \cap Y)}{|X \cup Y|} \times 100\%$ .

![](images/d74e9e74fda079a0ac650d50b05f2025bb8d0a99c0a3dca8cb7ff05c77a97100.jpg)



Fig. 5. Trade-off between loss rate and communication cost.

Fig. 5 examines the trade-off between the loss rate and the communication cost. It shows that when m is increased, the communication cost increases while the loss rate decreases. In this example, the communication cost can be reduced from $5 \times 10^{7}$ bits without using BFs to $3.14 \times 10^{7}$ bits at a loss rate of 11.4 percent, when $|X| = 100 K$ , $|Y| = 100 K$ , $|X \cap Y| = 60 K$ , and r is set to 250 bits. The loss rate can become quite acceptable by using a BF with larger size, while the communication cost will rise.

When we choose algorithms in a real-world system design, we may consider this trade-off between the search quality for the user and system resource consumption. In this design, we minimize the false positive to achieve the best recall rate. Given a specific ratio of m/n, i.e., the number of bits per element, it is easy to prove that the false positive rate f is minimized when $k = \frac{m}{n} \ln 2$ [5] and the minimal false positive rate is

$$
f _ {m i n} = 0. 6 1 8 5 ^ {\frac {m}{n}}. \tag {6}
$$

By substituting $f$ in (4) from (5), the communication cost for distributed union is

$$
m + (| X | + (1 - 0. 6 1 8 5 ^ {\frac {m}{| X |}}) (| Y | - | X \cap Y |)) r. \tag {7}
$$

Given a minimized false positive, we can make a decision for the union based on $M_{saved}$ .

From Fig. 4b, we can find that the keywords in the “OR” query may have inevitable differences of recall in the distributed union operations due to the false positive of BFs. The first keyword won’t have any missing results while the later ones may have missing ones. In the distributed union algorithm, we do not consider a complete search mechanism using reverse verification like the distributed intersection algorithm presented in Section 3.2.1. Such technique indeed achieves 100 percent recall for all the keywords but consumes even more communication cost than the straightforward strategy shown in Fig. 4a that transmits all the sets separately and directly to the client. In practice, when we design a real-world system, we can use some weighting techniques to differentiate the importance of keywords. For example, we can use the IDF [16] to let the rarer keywords in the query have higher weights and process such keywords before popular keywords.

# 3.3 Intersection-Order Optimization Strategy

For a query with more than two keywords, it is intuitive that there is much benefit if we first perform distributed intersection operations for the pairs of keywords that have smaller size of intersection. However, it is difficult to estimate the size of intersection incurred by two keywords before we get the exact intersection. In our design, we use BF to estimate the size of intersection between two sets for any given two keywords $[23]$ .

# 3.3.1 Intersection Size Estimation

Suppose that we have two BFs separately representing X and Y with the same number of m bits and using the same set of k hash functions. It is intuitive that the inner product of the two BFs can be used to measure their similarity. Mathematically, the ith bit will be set to "1" in both BFs if it is set by using some element in $X \cap Y$ , or if it is set to "1" simultaneously by some element in $X - (X \cap Y)$ and by another element in $X - (X \cap Y)$ . In total, the probability that the ith bit is set to "1" in both BFs can be quantified as

$$
\begin{array}{l} \left(1 - \left(1 - \frac {1}{m}\right) ^ {k | X \cap Y |}\right) \\ \left. + \left(1 - \frac {1}{m}\right) ^ {k | X \cap Y |} \left(1 - \left(1 - \frac {1}{m}\right) ^ {k | X - (X \cap Y) |}\right) \right. \tag {8} \\ \times \left(1 - \left(1 - \frac {1}{m}\right) ^ {k | Y - (X \cap Y) |}\right). \\ \end{array}
$$

After some algebraic simplification, the expected magnitude of the inner product of the two BFs can be quantified using the equation in [23].

$$
\begin{array}{l} p = m \left(1 - \left(1 - \frac {1}{m}\right) ^ {k | X |} - \left(1 - \frac {1}{m}\right) ^ {k | Y |} \right. \tag {9} \\ \left. + \left(1 - \frac {1}{m}\right) ^ {k (| X | + | Y | - | X \cap Y |)}\right). \\ \end{array}
$$

Using the two BFs for X and Y, it is easy to obtain the magnitude of the inner product p. Thus, given $|X|$ , $|Y|$ , k, m, and p, we can get an estimated size of $X \cap Y$ using (10).

$$
\begin{array}{l} | X \cap Y | = \\ - \frac {\log_ {1 - \frac {1}{m}} \left(\frac {p}{m} + \left(1 - \frac {1}{m}\right) ^ {k | X |} + \left(1 - \frac {1}{m}\right) ^ {k | Y |} - 1\right)}{k} + (| X | + | Y |). \tag {10} \\ \end{array}
$$

# 3.3.2 Learning from Queries

The difficulty in applying the above intersection size estimation scheme in a system design is that it is infeasible to exhaustively identify all the combination of term pairs and also impossible to predict all the combination of interests due to the vast communication cost. In this paper, we utilize the query history to find out near optimal pairs. Specifically, we monitor queries on the DHT nodes to which the BF is transmitted so that interesting correlations can be inferred. More specifically, in Fig. 2b, BF(X) is cached in the DHT node responsible for keyword y for calculating the cardinality of the intersection $X \cap Y$ . The more frequently keywords x and y are searched together by users, the more correlated they are. Then, the estimated intersection size will be stored on both DHT nodes for x and y for the future queries.

# 3.4 Gathering Global Keyword Popularity

Within the structure of a hybrid P2P network, we use a variant of the push-synopsis gossip algorithm first proposed in $[24]$ to gather global keyword popularity in the web. The robust algorithm enables every peer to quickly collect the global statistical term frequency in the P2P web.

It is not difficult to see that the global frequency of a term x can be obtained from the node holding the inverted list of x. In this design, we do not obtain the statistics from DHT nodes during query processing due to the extra latency by obtaining such information via DHTs. Specifically, the inquiry message needs to be transferred $O(\log(N))$ hops across the wide area network (application layer) to obtain the term frequency. In contrast by using the gossip algorithm, each node can obtain the global term frequency for all the keywords directly from the local synopsis with a constant latency $O(1)$ , greatly reducing the query processing time.

The main idea of the method is as follows: consider the example of $|X|$ , the global statistical frequency of keyword x, the method first lets all peers in the network check their local index. When the keyword x is found the first time in a document on a peer, this peer does the following experiment: it flips a coin up to t times and counts the number of times the head appears before the first tail. It saves this count in a value called $FC(x)$ . Then, the $FC(x)$ is gossiped among the peers in the network. During each round of gossip, each node chooses a random neighbor and sends the neighbor the $FC(x)$ value it locally holds. After receiving the $FC(x)$ values from a neighbor, a peer computes the maximum value of $FC(x)$ , i.e., $maxFC(x)$ . The results in [25] show that the robust gossip scheme leads the computation of aggregated information to converge exponentially: after $O(\log(n))$ rounds of gossip, where n is the number of nodes in the network, all peers will get $|X|$ with high probability. Moreover, the value of $|X|$ is roughly $2^{maxFC(x)-1}/0.77351$ with high probability [26].

The pushing synopsis-based gossiping algorithm for estimating global statistical keyword frequency has three main operations:

1. Synopsis generation. At the initialization phase when a peer joins the network the first time, it browses its local index and generates a local synopsis using the duplicated-insensitive counting technique proposed by Flajolet and Martin [26]. The synopsis structure is designed as $(x, bitvec_x)$ , where $bitvec_x$ is a bit vector for counting the statistical frequency of keyword x. Considering initializing bitvec\_x as an example, when a peer finds keyword x in a document the first time, it does the coin flip experiment and saves the $FC(x)$ value in bitvect\_x by setting the $FC(x)$ th bit to "1."

![](images/6185a4c2a9aad52f19998ffa32af8f847cab4c380d37681edf85bf9c4abe9dba.jpg)



Fig. 6. One round of gossip.

2. Synopsis disseminating. The synopses are disseminated among peers using the randomized gossip algorithm proposed in [25]. During gossip round, each node randomly chooses a neighbor and sends the selected neighbor its synopsis. In Fig. 6, we illustrate an example of one round of gossip.   
3. Synopsis merging. When a peer receives the synopsis from its neighbor, it checks the synopsis it receives against its own synopsis and performs the following merging operation. For the keyword t in both synopses, it performs the bitwise-or operation on the pair of bit vectors for bitvec\_t; and for those keywords in the synopsis of the neighbor but not in the local synopsis, it merges the relevant bit vector into its own synopsis. Fig. 7 shows the process at Peer B after it merges the synopsis that Peer A gossips to it. The bitwise-or operation has the effect of computing the maximal of the FC values of the independent experiments in an order-insensitive manner.

In addition to the three operations, we must deal with the change of the global statistics over time because of leaving of nodes. Note that a synopsis with a counter much larger than its exact number almost surely contains data from every local index node. However, a particular local node who leaves has no way of deleting what it has ever contributed the synopsis, making the global statistics stale. To cope with this problem, in our design when a node receives a synopsis with a counter number larger than some maximum value V, it drops both the incoming and its local bit vector in the synopsis. It then recomputes a local synopsis based on its current document set and performs the gossip protocol based on the new synopsis. This periodic purging of old statistics guarantees that stale information will eventually leave the system. We will study the optimal choice of V in future work.

We will analyze the extra cost introduced by the gossip algorithm in Section 5.3 in detail. It is easy to see that such a design is a trade-off between resource utilization and user-perceived qualities (search latency).

# 3.5 Scalability

In P2P text retrieval, the potential number of results for a given query is roughly proportional to the number of documents in the network. The communication cost of returning all results to the client will grow linearly with the size of the network. Bloom filter techniques can yield a substantial constant-factor improvement, but it does not eliminate the linear growth in cost. By combining the top-k pruning techniques with the Bloom Filter techniques, the scalability problem can be effectively solved $[6]$ . Proposing a comprehensive solution for large-scale P2P text retrieval is out of the scope of this paper. We focus on the optimizing the Bloom Filter settings in this paper.

![](images/0da179629986dad819140a8ce650caac3ba3e5a3a701b79fd20bcc9f740fa4f9.jpg)



Fig. 7. Synopsis merging.

# 4 SIMULATION METHODOLOGY

In this section, we first introduce the data set and query logs we use for the evaluation of our design, and how we collect the traces of Gnutella for simulating the P2P topology. We then discuss the design of our simulator for P2P web multikeyword search.

# 4.1 Web Data Collection

Since there has been no standard data set for evaluating the performance of content-based P2P web search, we built one based on TREC [7] WT10G web corpus, a large test set widely used for performance evaluation in web retrieval research area. The data set includes 10 GB, 1.69 million webpage documents and a set of queries (we use the "title" field of a TREC topic as a query [7]). The WT10G data were divided into 11,680 collections based on document URLs. Each collection on average has 144 documents with the smallest one having only five documents. The average size of each document is 5.91 KB. All data set was stemmed with the Porter algorithm to reduce words to their roots (e.g., "putting" becomes "put" and common stop words such as "the," "and," etc., were removed from the data set [7]. Table 2 summarizes the statistics for the test data set.

# 4.2 Queries

The number of queries provided by US National Institute of Standards and Technology (NIST) for the TREC WT10G web test collection is far from enough to be used in studies on P2P web search. We evaluate our design using the query logs which we have analyzed in Section 3.2. The four months query logs are quite representative for real-world systems.

TABLE 2
Statistics of the WT10G Data Set 

<table><tr><td>Parameters</td><td>Value</td></tr><tr><td>Number of documents</td><td>1,692,096</td></tr><tr><td>Number of collections</td><td>11,680</td></tr><tr><td>TREC topics</td><td>501 550</td></tr><tr><td>Average number of documents of a collection</td><td>144</td></tr><tr><td>Average size of documents</td><td>5.91KB</td></tr></table>

# 4.3 Gnutella Trace

We have developed a crawler in Java based on the limewire $[27]$ open source client to collect topology information of Gnutella network. According to Gnutella protocol $[28]$ , a ping message with settings TTL = 2 and HOP = 0 is regarded as a crawler ping, and peers which receive a crawler ping should respond with appropriate pong messages. Based on this mechanism, our crawler discovers the topology of Gnutella P2P network by performing a breadth first search. From our experience and observations during the crawling, we find that some clients such as Gnucleus and Morpheus (based on GnucDNA) do not respond to the crawler ping appropriately. Fortunately, these clients send an information page summarizing servants' status to any web browser trying to connect to it. Motivated by this, we also developed a web spider as a means of collecting topology information from these clients. We then integrated the web spider into the crawler, which accelerated the crawling process greatly. Our crawler ran in parallel with 40 threads, and can discover more than 50,000 peers within half an hour.

We have crawled seven topologies with different scales of 31,747, 34,206, 45,650, 48,134, 57,926, 68,737, and 7,5643 nodes, respectively, for this simulation. We use the Gnutella topology trace we collected to simulate a real P2P network.

# 4.4 Hybrid P2P Networks

In order to well represent real-world systems, we consider both the underlying physical topology and the P2P overlay. The physical topology should represent the real topology with Internet characteristics. Previous studies have shown that a large-scale Internet physical topology follows the small-world and power law properties. The topology of a small-world network has the properties of sparseness, short global separation, and high local clustering of nodes while power law denotes the property of the node degree distribution. The study of Tangmunarunkit et al. [29] found that the topologies generated using the AS Model have the properties of the small world and power law. BRITE [30] is a topology generation tool that provides the option of generating topologies based on the AS Model. Using BRITE, we generate a physical topology with 100,000 nodes.

We use the Gnutella traces we collected to simulate the P2P overlay. All P2P nodes in the trace are mapped into the underlying physical topology. The communication cost between two logical neighbors is calculated based on the physical shortest path between the pair of nodes. The 1,692,096 documents in the WT10G data set can be divided into 11,680 collections (servers) according to ULR of the webpages. In the simulations, we randomly distribute the collections into the Gnutella peers. Thus, each peer acts as a webserver in the P2P web. We simulate Chord protocol to support single-keyword-based global inverted index.

# 5 PERFORMANCE EVALUATION

In this section, we first introduce the metrics that we use in the evaluation. Then, we analyze how to achieve BF optimal settings for the algorithm proposed in Section 3.2 through numerical method with Matlab. Based on the analysis results, we conduct comprehensive simulation to compare our design with the work proposed in [5], [6].

# 5.1 Metrics

In the evaluation, we mainly consider two metrics, traffic and search latency.

# 5.1.1 Traffic

P2P traffic has a significant impact on the underlying network. Heavy network traffic limits the scalability of P2P networks. We define the traffic as network resource used in the search process, which is mainly a function of the length of the links, the bandwidths, and other related expenses $[31]$ .

Specifically, in the P2P network, when a message is transferred over the application layer overlay network from a peer to another, the message actually traverses a path consisting of a set of underlying physical links. The cost caused by this single hop over the P2P overlay is calculated by adding up the cost of the underlying links: $Tc = M \sum_{i} L_{i} / B_{i}$ , where M is the size of the message and $L_{i}$ and $B_{i}$ , respectively, represent the length and the bandwidth of the ith link in the physical layer the message traverses. Generally, a query processing message travels multiple hops across the application layer overlay network. Thus, the traffic is the summed cost of all the hops.

In the experiment, we use BRITE [30] to simulate the underlying physical network across which the packets are transferred. The parameters of the physical links simulated with BRITE include the euclidean length, the bandwidth, and other configurations of the physical links. The traffic cost values are eventually computed according to the sizes of the transferred data and the related parameters of the underlying physical links.

# 5.1.2 Search Latency

Short search latency is always desirable in P2P systems. Search Latency for a query is the sum of the underlying Internet latency during each hop in the overlay between the time when query is issued and the first result is returned. The time required to send a network message includes the propagation time as determined by the distance between the underlying Internet nodes and the transmission time. The overall transmission time is computed by $M/B + L/s$ , where M is the size of the transmitted data (bits), B is the link bandwidth (bps), L is the length of physical link, and s is the propagation speed in medium. We configure the upload bandwidth of a Peer according to the measurement study on MSN from Microsoft [32] in 2007. The study has shown that 97.2 percent MSN video users have upstream bandwidth higher than 128 Kbps (16 KBps) (see Table 3). This corresponds to a DSL1 line quality. In the experiment, we set the upload bandwidth of a peer to 128 Kbps (16 KBps) and set the download bandwidth to 768 Kbps (96 KBps). On one hand, this conservative configuration about peer bandwidth capacity indeed pushes the system performance examination close to the system limits. On the other hand, in practice, a real-world peer-assisted text retrieval system may not want to fully exploit the available bandwidth of a high capacity peer, as doing so might deter their participation.

TABLE 3
User Bandwidth Breakdown (Kbps) 

<table><tr><td></td><td>Modem</td><td>ISDN</td><td>DSL1</td><td>DSL2</td><td>Cable</td><td>Ethernet</td></tr><tr><td>download</td><td>64</td><td>256</td><td>768</td><td>1500</td><td>3000</td><td>&gt;3000</td></tr><tr><td>upload</td><td>64</td><td>256</td><td>128</td><td>384</td><td>768</td><td>768</td></tr><tr><td>share (%)</td><td>2.8</td><td>4.3</td><td>14.3</td><td>23.3</td><td>18.0</td><td>37.3</td></tr></table>

# 5.2 Optimal Setting of Bloom Filter

In this section, we show how to achieve the minimized communication cost defined in Section 3.2 by using optimal settings of BFs. We analyze the communication cost quantified by (4) with Matlab. We consider three typical situations in Fig. 8: 1) $|X| < |Y|$ , 2) $|X| = |Y|$ , and 3) $|X| > |Y|$ . We set $r$ to 250 bits based on the research results conducted on Google search engine, which show that the average URL length measured in character is 31.2 characters [33]. We adjust the parameters $m$ and $k$ and examine how the value of $f(m, k)$ changes.

We find that the intersection order is critical for minimizing the communication cost. In Fig. 8b, we can observe that when $|X|$ is larger than $|Y|$ , BF does not work for minimizing the communication cost at all. The optimal strategy is setting m to 0 that means transmitting no BF but fetching the original set Y to the DHT node that is responsible for keyword x. Figs. 8a and 8c show that when $|X|$ is not greater than $|Y|$ , the communication cost can be minimized.

In the simulation, we vary the value of k from 1 to 10. Fig. 9 shows that when the value of k varies from 1 to 5 with fixed value of m, the communication cost decreases; while the communication cost changes very slightly when k varies from 5 to 10. The minimized value appears when k = 8. Thus in the experiments, we use a set of eight hash functions. On the contrary, the value of $f(m, k)$ is significantly influenced by the variable m. The minimal value of $f(k, m)$ can be achieved when m is set as an optimal value.

The results demonstrate that the optimal BF is determined by the popularities of keywords and the intersection order. Much benefit can be achieved if we transfer the BF for the set of a less popular keyword to the DHT node responsible for a popular keyword during the process of distributed intersection. Based on these observations, given $|X|$ , $|Y|$ , the objective of our optimal BF-based intersection algorithm is to enable each node intelligently choose the optimal m and the intersection order to achieve the minimal communication cost.

In this design, we first sort the keywords for an intersection operation in increasing order according to their popularities, $|X| < |Y|$ . By varying the values of $|X|$ and $|Y|$ , we obtain a set of sample values for optimal m. Fig. 10 plots the optimal values of m for any given $|X|$ and $|Y|$ . The results show that with the same values of $|X|/|Y|$ , the value $m/|X|$ is a constant, where m is the optimal setting. For simplicity, we use u to denote $|Y|/|X|$ and v to denote $m/|X|$ . Thus, we can derive a function $v = f(u)$ .

We use Matlab least-squares polynomial curve-fitting tools to find best fits. Fig. 11 shows the curves for fits. The three-cubed curve $v = 0.0001u^3 - 0.01u^2 + 0.42u + 11.06$ better fits the distribution of the optimal m. Thus, each node can determine the optimal settings of BF according to the popularities of query keywords with no extra configuration cost. In the rest of simulations, every DHT node calculates the optimal m by $m = f(u)|X|$ .

![](images/f6d1f7524a371c369934531ff1bb4a9c610cac1186e902d4c86aff586f6054bf.jpg)



(a)

![](images/56218efe90e1f4ac62e1d0c459003fa6c8d81b80dd2c223ab31e506385ebf4d5.jpg)



(b)

![](images/cfe2afd7f4d3bfb969e7a423c006ca4baf69a82b67f3efdf118dee4214c1f94a.jpg)



(c)

Fig. 8. Minimizing extra communication cost incurred by BF for different keyword popularity. (a) $|X| = 10\mathrm{K}$ , $|Y| = 1,000\mathrm{K}$ . (b) $|X| = 1,000\mathrm{K}$ , $|Y| = 10\mathrm{K}$ . (c) $|X| = 100\mathrm{K}$ , $|Y| = 100\mathrm{K}$ .   
![](images/1d527eb02d7ae4b53219d6fa172f529776e07ed90a019490428480e36d9f18cb.jpg)



(a)

![](images/7534fe81a795ed92d309f666c3e367c1eabf5cf7d7dd2afd04680d9040b5de0d.jpg)



(b)   
Fig. 9. The changes of the communication cost with the changes of parameter k. (a) $|X| = 10 \, K$ , $|Y| = 1,000 \, K$ . (b) $|X| = 100 \, K$ , $|Y| = 100 \, K$ .

![](images/bd5c24ff6cd6b37809117a4f20161c36aea8c0655f42a0f36e4d0c49bf229d74.jpg)  
Fig. 10. Distribution of optimal m settings.

# 5.3 Results

Based on the above results, we compare the performance achieved by our method with that of the previous work [5], [6]. Since all the designs aim at improving the performance of multikeyword queries processing, we do not include single-term queries in the experiments.

For simplicity, we use the legends to denote the strategies in the evaluation and summarize all the notations used in the experiment figures in Table 4, where $A = \{\mathrm{P} : : \text{sorting query terms according to popularity for distributed intersection}\}$ , $B = \{\mathrm{M} : : \text{optimizing } m \text{ for minimizing communication cost, F.}: \text{setting } m \text{ for minimizing false positive of BF}\}$ , and $C = \{\mathrm{I} : : \text{keyword pairs with smaller intersection size are searched together, U.}: \text{unaware of the intersection size}\}$ .

We can use P.F. to denote the baseline. In P.F. strategy, we first perform one round of Bloom Filter exchange from the DHT nodes holding the shortest inverted list to the other nodes. A round of such operation consists of a sequence of several petals as shown in Fig. 3b, where $|X| \leq |Y| \leq |Z| \leq \cdots$ . For each petal, we choose the hash function domain which achieves the minimal false positives. After all petals have been performed, we send the surviving items in the shortest list to the nodes holding remaining keywords.

The P.F. strategy indeed simulates the SBPA with only one round of Bloom Filter. We have noticed that Zhang and Suel [6] evaluated the SBPA algorithm using a collection of 1.8 TB 120 million webpages they had crawled. In such a large collection, for the average query, the shortest inverted list contains one million elements. To cope with such large-scale collection, the SBPA algorithm uses several rounds of Bloom Filters. It transfers the shortest inverted list block by block in the form of Bloom Filters. In each round for a block, they compute intersection between a block of the shortest list and the other lists. In this work, we use the WT10G data collection, which includes 10 GB 1.69 million webpages. Although the WT10G test collection is widely used in the text retrieval area, we find it not large enough to return as large numbers of hits for most queries as those from the large-scale collection used in [6]. We examine the length of the shortest inverted lists for all the query logs in the global index built for WT10G collection. Fig. 12 plots the number of items in the shortest inverted lists. It shows that 90 percent of the shortest inverted lists in our experiment have less than 10 K elements; while the shortest list for an average query has 4.2 K elements. This length is more than two orders of magnitudes lower than that of the text collection presented in [6]. Thus, in the simulation, we only use one round of Bloom Filter. Since in this work, we focus on optimizing settings of Bloom Filters, the comparison between our scheme and SBPA both using one round Bloom Filter is fair.

![](images/49b494b80eb0fc1debe01f881bbb84626e274679f9f86b7afe795a0809cb244c.jpg)



Fig. 11. Polynomial curve fitting for distribution of optimal m.

TABLE 4
Notations of Strategies 

<table><tr><td colspan="2">Notation</td><td>Description of Strategy</td></tr><tr><td>A.</td><td>P.</td><td>sorting query terms according to popularity</td></tr><tr><td rowspan="2">B.</td><td>M.</td><td>optimizing m for minimizing communication cost</td></tr><tr><td>F.</td><td>optimizing m for minimizing false positive of BF</td></tr><tr><td rowspan="2">C.</td><td>I.</td><td>keyword pairs with smaller intersection size are searched together</td></tr><tr><td>U.</td><td>unaware of the intersection set size</td></tr></table>

The strategy I. which searches keyword pairs with smaller intersection size first is to improve the efficiency of queries with three or more keywords. To make the comparison clear, when examining the benefit of strategy I., we will conduct experiments with the query logs that have three or more keywords to evaluate the strategy separately. We first separately examine the two-keyword queries and the queries with more than two keywords in the query logs, and then merge the results to present the overall performance.

Fig. 13 plots traffic of all the tested queries. The results show that the insight proposed in our work is quite valid. The result in Fig. 13 shows that with strategy M., the statistical average query traffic is significantly reduced by 26 percent.

Fig. 14 plots latency of all the tested queries. The result shows that with strategy M., the average query latency is reduced by 10 percent. About 63 percent queries using optimal strategy have latency less than 100 ms, while 55 percent queries of the baseline achieve such low latency.

![](images/f8939ef4919f518284ea174a0deef0f97914595de4a8d5dc477c23808f16d25d.jpg)



Fig. 12. Length of the shortest inverted lists.

![](images/f455be23c77ecd94d11ebcba968808a9e7a0f2583efe98df6f5ea76c938e4247.jpg)



Fig. 13. Traffic for distributed intersection using optimal BF.   
![](images/aa4d3f5ec52b69ee0c633db358cfcc4b19ed6a83f1f4e7c111c6fa72451ddb1d.jpg)



Fig. 14. Latency for distributed intersection using optimal BF.   
![](images/60c316dcaefaa7d291335e5c6659a77063d3606b806a22bf3d9ce4b2925f5cb6.jpg)



Fig. 15. Traffic for distributed intersection using intersection estimation.

In Figs. 15 and 16, we plot the traffic cost and latency of the proposed strategies and compare them with the baseline approach, where the legends A.B. have the same meaning with Figs. 13 and 14, and C. is a set, where $C = \{I: keyword pairs with smaller intersection size are searched together, U: unaware of the intersection set size\}$ . We compare the performance achieved by our strategies with the baseline approach. The baseline for multikeyword search can be denoted as U.P.F. which is equivalent to P.F.

Fig. 15 shows that with strategies of M., the average query traffic is reduced by 10 percent. With the strategies of I. and M., the average query traffic is significantly reduced by 13 percent. About 76 percent queries using the optimal strategy have a traffic cost less than 100, while 61 percent queries of the baseline achieve such low traffic cost.

Fig. 16 plots the latency of the tested queries. With all the strategies I. and M., the statistical average query latency is significantly reduced by 11 percent. About 62 percent queries using the optimal strategy have latency less than 100 ms, while only 50 percent queries of the baseline achieve such low latency.

![](images/6cec7412b7ce189c387abb55e3f0cdab898886dc0ca818037f905b3b491616dc.jpg)



Fig. 16. Latency for distributed intersection using intersection size estimation.   
![](images/12d371548b707c69562414cf92bd624c862bb6d8b8ac7dffa0e76cdf54095e3a.jpg)



Fig. 17. Traffic of distributed intersection for all the logs.   
![](images/4014b0603b9b6e9592d68b21feb86b43754b00719b8594a5cc0e103d6637cb81.jpg)



Fig. 18. Latency of distributed intersection for all the logs.

Figs. 17 and 18 plot the traffic cost and latency for all the queries we collected, where our algorithm greatly outperforms the baseline. Fig. 17 shows that with the strategies of I. and M., the statistical average query traffic is significantly reduced by 20 percent. About 72 percent queries using the optimal strategy have a traffic cost less than 100, while 61 percent queries of the baseline achieve such low traffic cost. Fig. 18 shows the similar results like those of Fig. 17 that query latency is greatly reduced with our proposed approaches.

We further examine the performance of our distributed union algorithm based on BF described in Section 3.2.2 by using the straightforward union operation as the baseline. Figs. 19 and 20 show the performance of distributed union algorithm, where the threshold is fixed at $\delta = 0.4$ . Fig. 19 shows that the traffic cost of the involved queries is effectively reduced. Statistically, the traffic cost is reduced by 49 percent. About 84 percent queries using our distributed union algorithm have a traffic cost less than 500, while only 75 percent involved queries of the baseline achieve such low traffic cost.

Fig. 20 shows that the latency is slightly increased using the BF-based distributed union algorithm. This is because the latency for the straightforward union is determined by the size of the matched set for the most popular keyword in the query. About 89 percent queries using our distributed union algorithm have latency less than 50 ms, while 90 percent involved queries of the baseline achieve such latency. The result also shows that for the queries with latency more than 100 ms, the latency of our algorithm is not worse than that of the baseline. Thus, our algorithm can greatly reduce the communication cost for "OR" queries as well as keep the latency acceptable.

![](images/a828db6822e7cc560819a9654ef0694ead59a927bc6c704585e32f4470f74f9d.jpg)



Fig. 19. Traffic for distributed union.   
![](images/93104174d73db49819e93b86c86b89e319ecc2697a1970376d87ccdc363b4678.jpg)



Fig. 20. Latency for distributed union.

We adjust the value of $\delta$ . Figs. 21 and 22 plot the reduction of traffic and increment of latency for different values of $\delta$ . Results show that when the threshold increases, the reduction of traffic cost increases apparently while the latency increment changes very slightly.

Another cost of this design is the synopsis for the gossip algorithm. In this design, the bit vector for each unique keyword takes 4 bytes. The average word length is about 5. Each term will take 9 bytes in the synopsis. There are about 5,792,000 distinct original words (not just the stems) in the WT10G collection. Hence, each peer needs a storage size below the bound of 49.7 MB for gathering the global information. Text compression using Burrows-Wheeler Transform can reduce the storage size to about 16.8 MB. Due to the facts that the global statistics on the web do not change dramatically (on the time scale of days to weeks) while the robust gossip algorithm converges exponentially, infrequent operations for computing the statistics, including transmitting, (de)compression, and merging the synopsis, are sufficient in a real system design.

The downside to the global text index-based scheme is that the maintenance overhead including inserting and updating cost may increase if nodes leave or join the network frequently. In a search system, such as web search engines and large-scale digital library systems, where queries are more frequent than insertions and updating, the global indexing scheme is a good trade-off. In this design, we assume that each node represents a webserver, which is much stable than a normal peer (a PC, for example) in the traditional P2P file sharing systems. On the other hand, for web searching applications, the overhead associated with explicitly updating an inverted index can also be offset by the savings to avoid repeatedly crawling the content of the network in a centralized repository.

![](images/56f9ca7e4eefcd103f736fca7bedb6f78e6b38f3f6160d47cf5123dc4463fc22.jpg)



Fig. 21. Traffic cost when varying the threshold.   
![](images/eb42be809a6e8e21a0d590ff16be1ab7941c0d8d2fac8cd1dee280655fc30051.jpg)



Fig. 22. Latency when varying the threshold.

# 6 CONCLUSIONS

In this paper, we show mathematically that the optimal setting of BF in terms of traffic cost is determined by the numbers of items involved on both sides. We derive an effective approach to achieve BF optimal settings through numerical analysis. We also proposed the optimal order strategies for both “AND” and “OR” queries. We conduct comprehensive simulations based on TREC WT10G test collection and the query logs of a commercial web search engine. Simulation results show that our design outperforms existing work. In the future work, we will try to examine the performance of more comprehensive solutions by using larger scale data collections.

# ACKNOWLEDGMENTS

This paper is supported by National Science Foundation of China and RGC Joint research fund under grant No. 60731160630 and NSFC fund under grant No. 60933011.

# REFERENCES

[1] H.V. Jagadish, B.C. Ooi, and Q.H. Vu, "Baton: A Balanced Tree Structure for Peer-to-Peer Networks," Proc. Int'l Conf. Very Large Data Bases (VLDB), pp. 661-672, 2005.

[2] T. Suel, C. Mathur, J. wen Wu, J. Zhang, A. Delis, M. Kharrazi, X. Long, and K. Shanmugasundaram, "Odissea: A Peer-to-Peer Architecture for Scalable Web Search and Information Retrieval," Proc. Int'l Workshop Web and Databases (WebDB), 2003.   
[3] I. Stoica, R. Morris, D. Karger, F. Kaashoek, and H. Balakrishnan, "Chord: A Scalable Peer-to-Peer Lookup Service for Internet Applications," Proc. ACM SIGCOMM, 2001.   
[4] B.H. Bloom, "Space/Time Trade-Offs in Hash Coding with Allowable Errors," Comm. ACM, vol. 13, no. 7, pp. 422-426, 1971.   
[5] P. Reynolds and A. Vahdat, "Efficient Peer-to-Peer Keyword Searching," Proc. Int'l Conf. Distributed Systems Platforms and Open Distributed Processing (Middleware), 2003.   
[6] J. Zhang and T. Suel, "Efficient Query Evaluation on Large Textual Collections in a Peer-to-Peer Environment," Proc. IEEE Int'l Conf. Peer-to-Peer Computing (P2P), 2005.   
[7] D. Hawking, "Overview of the TREC-9 Web Track," Proc. Text REtrieval Conf. (TREC-9), 2000.   
[8] F.M. Cuenca-Acuna, C. Peery, R.P. Martin, and T.D. Nguyen, "Planetp: Using Gossiping to Build Content Addressable Peer-to-Peer Information Sharing Communities," Proc. IEEE Int'l Symp. High Performance Distributed Computing (HPDC), 2003.   
[9] B. Yang and H. Garcia-Molina, "Designing a Super-Peer Network," Proc. Int'l Conf. Data Eng. (ICDE), 2003.   
[10] H.T. Shen, Y.F. Shu, and B. Yu, "Efficient Semantic-Based Content Search in P2P Network," IEEE Trans. Knowledge and Data Eng., vol. 16, no. 7, pp. 813-826, July 2004.   
[11] K. Sripanidkulchai, B. Maggs, and H. Zhang, "Efficient Content Location Using Interest-Based Locality in Peer-to-Peer Systems," Proc. IEEE INFOCOM, 2003.   
[12] P. Haase, J. Broekstra, M. Ehrig, M. Menken, P. Mika, M. Olko, M. Plechawski, P. Pyszllak, B. Schnizler, R. Siebes, S. Staab, and C. Tempich, "Bibster - A Semantics-Based Bibliographic Peer-to-Peer System," Proc. Int'l Semantic Web Conf. (ISWC), 2004.   
[13] J. Lu and J.P. Callan, "Content-Based Retrieval in Hybrid Peer-to-Peer Networks," Proc. Conf. Information and Knowledge Management (CIKM), 2003.   
[14] M. Li, W.-C. Lee, and A. Sivasubramaniam, "Semantic Small World: An Overlay Network for Peer-to-Peer Search," Proc. IEEE Int'l Conf. Network Protocols (ICNP), 2004.   
[15] C. Tang and S. Dwarkadas, "Hybrid Global-Local Indexing for Efficient Peer-to-Peer Information Retrieval," Proc. Networked Systems Design and Implementation (NSDI), 2004.   
[16] S. Robertson, "Understanding Inverse Document Frequency: On Theoretical Arguments for Idf," J. Documentation, vol. 60, pp. 503-520, 2004.   
[17] O.D. Gnawali, "A Keyword-Set Search System for Peer-to-Peer Networks," master's thesis, Massachusetts Inst. of Technology, 2002.   
[18] I. Podnar, M. Rajman, T. Luu, F. Klemm, and K. Aberer, "Scalable Peer-to-Peer Web Retrieval with Highly Discriminative Keys," Proc. IEEE Int'l Conf. Data Eng. (ICDE), 2007.   
[19] G. Skobeltsyn, T. Luu, I.P. Zarko, M. Rajman, and K. Aberer, "Web Text Retrieval with a P2P Query-Driven Index," Proc. Ann. Int'l ACM SIGIR Conf. Research and Development in Information Retrieval (SIGIR), 2007.   
[20] M. Bender, S. Michel, P. Triantafillou, G. Weikum, and C. Zimmer, "P2P Content Search: Give the Web Back to the People," Proc. Int'l Workshop Peer-to-Peer System (IPTPS), 2006.   
[21] B.T. Loo, J.M. Hellerstein, R. Huebsch, S. Shenker, and I. Stoica, "Enhancing P2P File-Sharing with an Internet-Scale Query Processor," Proc. Int'l Conf. Very Large Data Bases (VLDB), 2004.   
[22] A. Rao, K. Lakshminarayanan, S. Surana, R.M. Karp, and I. Stoica, "Load Balancing in Structured P2P Systems," Proc. Int'l Workshop Peer-to-Peer System (IPTPS), 2003.   
[23] A. Broder and M. Mitzenmacher, “Network Applications of Bloom Filters: A Survey,” Internet Math., vol. 1, no. 4, pp. 484-509, 2005.   
[24] S. Nath, P.B. Gibbons, S. Seshan, and Z.R. Anderson, "Synopsis Diffusion for Robust Aggregation in Sensor Networks," Proc. Int'l Conf. Embedded Networked Sensor Systems (SenSys), 2004.   
[25] D. Kempe, A. Dobra, and J. Gehrke, "Gossip-Based Computation of Aggregation Information," Proc. Ann. IEEE Symp. Foundations of Computer Science (FOCS), 2003.   
[26] P. Flajolet and G.N. Martin, "Probabilistic Counting Algorithms for Data Base Applications," J. Computer and System Sciences, vol. 31, pp. 182-209, 1985.   
[27] The Gnutella Protocol Specification 0.6, 2002.

[28] Limewire, http://www.limewire.com, 2010.   
[29] H. Tangmunarunkit, R. Govindan, S. Jamin, S. Shenker, and W. Willinger, “Network Topology Generators: Degree-Based vs. Structural,” Proc. ACM SIGCOMM, 2002.   
[30] Brite, http://www.cs.bu.edu/brite/, 2010.   
[31] Y. Liu, X. Liu, L. Xiao, L.M. Ni, and X. Zhang, "Location-Aware Topology Matching in P2P Systems," Proc. IEEE INFOCOM, 2004.   
[32] C. Huang, J. Li, and W. Ross, "Can Internet Video-on-Demand Be Profitable?," Proc. ACM SIGCOMM, 2007.   
[33] N.F. Huang, R. Liu, C.H. Chen, Y.T. Chen, and L.W. Huang, "A Fast Url Lookup Engine for Content-Aware Multi-Gigabit Switches," Proc. Int'l Conf. Advanced Information Networking and Applications (AINA), 2005.

![](images/f739a51212fb39a71e03e459ca2394285246406156118d9b4389b9198a014ecb.jpg)



Hanhua Chen received the PhD degree in computer science and engineering from Huazhong University of Science and Technology in 2010, where he is now working as an associate professor. He worked at the Hong Kong University of Science and Technology as a postdoctoral research associate between 2009 and 2010, and as a visiting scholar between 2007 and 2009. His research interests include peer-to-peer computing and wireless sensor

networks. He is a member of the IEEE.

![](images/a52427dada8e9b9e8677dd50c99f9b24864adffa854cddbd4fb48ece98242b0d.jpg)



Hai Jin received the PhD degree in computer engineering from Huazhong University of Science and Technology (HUST) in 1994. He is a Cheung Kung scholars chair professor of computer science and engineering at Huazhong University of Science and Technology in China. He is now the dean of the School of Computer Science and Technology at HUST. In 1996, he was awarded a German Academic Exchange Service fellowship to visit the Technical Uni-

versity of Chemnitz in Germany. He worked at The University of Hong Kong between 1998 and 2000, and as a visiting scholar at the University of Southern California between 1999 and 2000. He was awarded Excellent Youth Award from the National Science Foundation of China in 2001. He is the chief scientist of ChinaGrid, the largest grid computing project in China, and the chief scientist of National 973 Basic Research Program Project of Virtualization Technology of Computing System. He is the member of Grid Forum Steering Group (GFSG). He has coauthored 15 books and published more than 400 research papers. His research interests include computer architecture, virtualization technology, cluster computing and grid computing, peer-to-peer computing, network storage, and network security. He is the steering committee chair of International Conference on Grid and Pervasive Computing (GPC), Asia-Pacific Services Computing Conference (APSCC), International Conference on Frontier of Computer Science and Technology (FCST), and Annual ChinaGrid Conference. He is a member of the steering committee of the IEEE/ACM International Symposium on Cluster Computing and the Grid (CCGrid), the IFIP International Conference on Network and Parallel Computing (NPC), and the International Conference on Grid and Cooperative Computing (GCC), International Conference on Autonomic and Trusted Computing (ATC), International Conference on Ubiquitous Intelligence and Computing (UIC). He is a senior member of the IEEE and a member of the ACM.

![](images/2456cc0ae0e4245418b915ae5a4dea74f96b6a0f5c46f20ee025797cc3eedebb.jpg)



Lei Chen received the BS degree in computer science and engineering from Tianjin University, China, in 1994, the MA degree from Asian Institute of Technology, Thailand, in 1997, and the PhD degree in computer science from the University of Waterloo, Canada, in 2005. He is now an associate professor in the Department of Computer Science and Engineering at The Hong Kong University of Science and Technology. His research interests include uncertain and prob-

abilistic databases, graph databases, multimedia and time series databases, and sensor and peer-to-peer databases. He is a member of the IEEE.

![](images/9c241f5a20751a58dddb483c93529ae6c3f07ca782cc85fc7fa6092ae141d645.jpg)



Yunhao Liu received the BS degree from the Automation Department, Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is a member of Tsinghua National Lab for Information Science and Technology, a professor at the School of Software at Tsinghua University, and the director of Tsinghua National MOE Key Lab for Information Security. He is also a faculty at the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology. Being a senior member of the IEEE, he is also the ACM distinguished speaker.

![](images/c6c4b10cb80ba363dab057a2878851efa4fbc662a9b6a3e156e608d69d5db849.jpg)



Lionel M. Ni is a chair professor in the Department of Computer Science and Engineering at The Hong Kong University of Science and Technology (HKUST). He also serves as the special assistant to the president of HKUST, director of the HKUST China Ministry of Education/Microsoft Research Asia IT Key Lab, and chair professor of Shanghai Key Lab of Scalable Computing and Systems at Shanghai Jiaotong University. He has chaired more than 30 professional conferences and has received six awards for authoring outstanding papers. He is a fellow of the IEEE.

For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.