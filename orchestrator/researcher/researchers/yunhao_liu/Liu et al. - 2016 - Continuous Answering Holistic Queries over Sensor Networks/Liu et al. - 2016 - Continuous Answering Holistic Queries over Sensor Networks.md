# Continuous Answering Holistic Queries over Sensor Networks

Kebin Liu, Lei Chen, Yunhao Liu, Wei Gong, Amiya Nayak

Abstract—Sensor networks are widely used in various domains like the intelligent transportation systems. Users issue queries to sensors and collect sensing data. Due to the low quality sensing devices or random link failures, sensor data are often noisy. In order to increase the reliability of the query results, continuous queries are often employed. In this work we focus on continuous holistic queries like Median. Existing approaches are mainly designed for non-holistic queries like Average. However, it is not trivial to answer holistic ones due to their non-decomposable property. We first propose two schemes based on the data correlation between different rounds, with one for getting the exact answers and the other one for deriving the approximate results. We then combine the two proposed schemes into a hybrid approach, which is adaptive to the data changing speed. We evaluate this design through extensive simulations. The results show that our approach significantly reduces the traffic cost compared with previous works while maintaining the same accuracy.

Index Items—Ubiquitous computing, Sensor networks, Distributed data structures.

# 1 INTRODUCTION

Sensor networks are now widely used in many applications, from habitat monitoring to location tracking and intelligent transportation systems. In these applications, sensors are often deployed in a large area to obtain measurements of various kinds of parameters. In order to collect and analyze sensing data, users issue various queries, such as selection query, aggregate queries (Max, Count, and Sum) and etc. In general, aggregate queries can be classified into two different categories, non-holistic queries and holistic queries [11]. Non-holistic queries [13], such as Count and Sum, share the decomposable characteristic, that is, for an arbitrary query Q on data set S, there is a function f, such that for all S=S1S2, Q(S)=f(Q(S1), Q(S2)). If there is no such a function f, the query Q is holistic. For example, a quantile query means to find the certain value that has the user specified rank among all the values, for which we cannot find such a function f. There are many differences between these two types of queries. Non-holistic queries usually provide one single result (e.g. count value or sum value). Moreover, since these queries are decomposable, partial results from downstream sensor nodes can be combined to one single result in an intermediate node without loss of information. For example, with a tree-like routing structure [21, 23], the partial result of an Average query contains only two variables: the number of sensors and the summation of all values in a sub-branch rooted at the intermediate node. In a quantile query, however, the distribution information of all sensor values must be collected. Many efforts have been made for handling non-holistic queries, such as TAG [21, 23], Cougar [33] etc., but few of them, if any, addressed holistic queries.

Holistic queries are actually as popular as nonholistic queries. For example, when the values sensed by sensors have noise, it makes more sense to get a median result of the monitoring area than to derive an

 K. Liu , Y. Liu and W. Gong are with MOE Key Lab for Information System Security, School of Software, Tsinghua National Lab for Information Science and Technology, Tsinghua University.   
 L. Chen is with the Department of Computer Science and Engineering, HKUST, HongKong.   
 A. Nayak is with the School of Electrical Engineering and Computer Science, University of Ottawa.

average result, since the noise may affect the average result largely. Thus, holistic queries can be used to get the approximate data distribution.

To answer holistic queries in a sensor network, many challenging issues need to be addressed. Obviously, a naïve approach requiring all sensors to deliver their values to the sink is energy inefficient. To save power, in-network aggregation [21] is introduced, in which messages from downstream nodes are merged into one, and the computation is distributed within the entire network. Due to the limitation of message size, the merging process may lose some information. Many prior attempts have been done to create sophisticated data structures and algorithms which try to keep the most useful information with a limited message size. Generally, these methods can only achieve approximate results with some error guarantee by introducing different restricts and pruning algorithms on the data structure [13, 28]. In many cases, we need the exact answers from the network. Furthermore, in many application scenarios, especially under tough environments such as coal mines and underwater, a WSN prefers continuous queries, and one-shot result is regarded as noisy and unreliable. In other words, the same query process needs to be executed periodically in order to improve accuracy and reliability. Strong correlations (temporal correlations) exist between data in different rounds, which are often overlooked by previous approaches in answering holistic queries.

In this paper, we explore the correlation between data of different rounds and present two approaches to monitor continuous holistic queries, one for getting the exact answers and the other one for deriving the approximate results. Then, we propose an effective hybrid approach that adaptively selects appropriate one based on data changing speed and improves the performance of continuous queries. We take one example of the holistic queries, Median, to illustrate our proposals. Median is a typical as well as important type of holistic queries. For example, according to our experience in deploying the GreenOrbs [20] system, a forest surveillance sensor network with up to 330 sensor nodes, we find that it is usually of great significance to derive the general status of a monitoring area rather than single reading. This requirement can be fulfilled by fusing sensor readings from different nodes with the Average or Median query.

Sensor nodes, however, are error prone that can report noisy or even error readings. In this case, the results of Average query can be largely affected by a small number of outliers and deviate from groundtruth. In contrast, the Median query is resistant to noisy readings and thus can provide robust and accurate result. In fact, the proposed methods can be naturally extended for other types of holistic queries. We will discuss the generalization in Section 7. The major contributions of this work are as follows:

1) We present a flexible bucket (F-Bucket)-based histogram approach to compute exact answer to a query. A histogram summary is used to collect the value distribution information. The query of a new round is guided by prior results so that the temporal correlations between two rounds are exploited. After several initial rounds, we can obtain the exact answers continuously.   
2) We also employ a wavelet-like approximate algorithm to offer a reasonable approximate result with some error bound guarantee, especially when the sensing values in the sensor network change quickly.   
3) We propose a hybrid approach, combining F-Bucket and wavelet-like approaches, to handle the continuous holistic queries. If the sensor values in network are relatively stable, we apply an exact algorithm to calculate the exact median. When the data changes quickly, our approach can adaptively switch to the approximate algorithm.

The rest sections of this paper are organized as follows. Section 2 illustrates prior works that are related to ours. Section 3 presents the overall process and refining algorithms of exact query algorithm. The wavelet-like approximate algorithm is presented in Section 4. Section 5 discusses the hybrid approach. In Section 6 we evaluate our algorithms with simulation experiments. We conclude this work in Section 7.

# 2 RELATED WORK

Query processing in sensor networks has drawn significant attentions from worldwide researches. Users issue various types of queries, such as selection queries [16] and aggregate queries [31]. L-PEDAPs [30] focused on routing tree construction and maintenance for query processing. Uncertainties may exist in both sensing data [1] and queries. For example, Zhang et al. [38] studied the problem of calculating the aggregate while the query location is uncertain. Ye et al. [34, 35] proposed to determine possible query results among all imprecise sensing data. Security issues [36] have been considered in query processing. By combining homomorphic encryption and secret sharing, SIES [26] achieved both confidentiality and integrity. While encryption-based aggregates provided better security, they, however, still had limitations in the usage of aggregation functions and the data integrity. RCDA [3] attempted to overcome these drawbacks by introducing “recoverability” to aggregate queries by which servers can recover all sensing data with low extra overhead. Yu et al. [37] presented a method which aiming at secure continuous aggregation querying.

Other than the approaches designed for answering aggregate queries, some data collection techniques [6, 7, 17] can be used to answer aggregate queries as well. However the focuses of those approaches are efficient data collection, not only on answering aggregate queries. Consequently we will review the work for decomposable aggregate queries and holistic aggregate queries.

As mentioned in Section 1, for the decomposable aggregate queries, there are already much works that have been done, such as TAG [21, 23], BBQ [9], Cougar [33], TiNA [29], Sketch [5], PGA [10]. TAG [21, 23] introduced the in-network aggregation scheme to minimize the amount of transmitted messages. BBQ [9] proposed using the statistical modeling techniques to answer various queries. In Cougar [33] approach, when given a user query, a query optimizer generates an efficient query plan for query processing. TiNA[29] exploited the temporal correlation between readings. Sketch [5] generalized the duplicate-insensitive characteristics to answer the aggregate queries such as Count, SUM. PGA [10] exploited range caching [10, 25] to reduce the number of exchanged messages, in which each node caches error filter for its sub-tree. They also introduced an algorithm, based on potential gains, to adaptively adjust the error thresholds.

With respect to the holistic aggregate queries that we focus on in this paper, there are not many related approaches. To generalize, there are three mainstream techniques for answering the holistic queries, which are centralized approaches, sampling approaches, and histogram-based approaches. TAG [21] presented a centralized approach for holistic in which sensor values are transmitted to the root where the aggregate result is calculated. Sampling is another type of technique for answering the holistic queries. SIA [27] proposed a framework for secure information aggregation and discussed the sampling-based computation of Median query. Histogram is a common structure for storing data distribution information in answering holistic queries. There are many types of histograms, such as equal-length histogram, equal-depth histogram and Wavelet-based histograms [24]. All histograms share the common point that they group values into buckets [11], so these methods are also regarded as buckets-based approaches. Hellerstein [14] introduced a waveletbased aggregation scheme which can also produce results of increasing resolution over time. Q-digest [28] is another kind of buckets-based approach which allows overlapping buckets. Besides, Q-digest guarantees an error of O(log()/m) with message size of m. Greenwald et al. [12] designed an online algorithm for computing ε-approximate quantile summary for large data stream with a worst-case space requirement of $O ( l o g ( \varepsilon N ) / \varepsilon )$ . Cormode et al. [4] proposed distributed-tracking schemes for finding accurate quantiles with error guarantees. They assumed each remote site maintains a local data stream. Greenwald et al. [13] presented algorithms which can provide ε-approximate answers for quantile with message size $O ( l o g ^ { 2 } ( n ) / \varepsilon )$ . Some other methods such as Manku etc. [22] presented hybrid approximate algorithms for computing frequency counts over data streams. ASP [15] presented tree based space-efficient scheme for calculating the frequent items and quantile.

Other than query processing over sensor networks, there are many other interesting works in the literature [18, 32], such as energy efficient coverage problem in sensor networks [2], moving object tracking [8], event detection [19] and etc.

# 3 EXACT QUERY SCHEME

We assume that a Median query is executed upon a dataset S within the range [1, ] and the total number of sensors in the network is n. The range here refers to integer values, the real value range can be converted into integer range by multiple a large enough integer. The output of Q is a data element d [1, ] such that the number of sensor values which are smaller (or larger) than d is n/2. A straightforward approach to get answers for Q is to retrieve all the values from sensors, however, as mentioned before, this is not energy efficient. Thus, in this paper, we propose a histogram-based approach to get exact answers for continuous queries. Specifically, we use the histogram summary structure to store the value distribution of the network. Each bucket in the histogram counts the number of values in a certain range. The exact query algorithm works when data values in sensor network are relatively stable over time. Since the sensor values are relatively stable and highly correlated among different rounds, the Median result can be searched in multiple rounds. In each round, we adjust the ranges of buckets, that is, subdividing the range where the median is located and assigning the subdivided small ranges to all intermediate buckets in the next round. After a few rounds, the ranges of all intermediate buckets will be of length 1, thus, we can get the exact median result continuously. When the median value runs out the ranges handled by these intermediate buckets, we need to adjust the range again. The range refining is conducted at the sink and the schema is flooded to the network. The detailed steps of this approach are discussed in following sections.

# 3.1 Data Structure

In the exact query approach, we apply the bucket histogram, which is referred as F(lexible)-Bucket, to get the exact answer for the query. The F-Bucket schema is assigned at the sink and then flooded to the whole network. One F-Bucket F consists of a list of triples which are denoted as buckets, $F = \{ B o , B _ { 1 } , . . . , B _ { i } , . . . \hat { B } _ { m - l } \}$ and $B i = ( m i n , m a x , c o u n t )$ , where integer m denotes the maximum number of the buckets determined by the message size, each bucket Bi has a range [Bi.min, Bi.max] defined by the min and max, and Bi.count counts the number sensor values in this range. Note that the ranges associated to bucket Bi and Bi+1 are consecutive, thus, Bi.max+1 = Bi+1.min. F-Bucket is flexible because the ranges corresponding to buckets are not fixed and can be refined periodically according to recent query results. An example of the F-Bucket with 6 buckets is illustrated in Figure 1.

In order to reduce the transmitted bytes, messages do not carry full F-Buckets but only buckets that are not empty (count > 0). We apply the in-network aggregation at intermediate nodes to merge all the partial F-Buckets received from children.

# 3.2 Query Processing

Although our query algorithm can work over arbitrary topology structures, to simplify the discussion we assume a tree-like routing topology [17, 19]. All sensor nodes in the network are organized into a spanning tree rooted by a special node called sink as illustrated in Figure 2. Take the Median query as an example, each round the leaf node builds an F-Bucket of only one bucket with its own value and transmits to its parent. An intermediate node receives F-Buckets from children and merges them with its own F-Bucket to an integrated one. The intermediate node then sends the new F-Bucket to its parent as well. In the end of the round, the sink merges all the received F-Buckets to a final one and calculates the

![](images/bc9327b384e7636f554d25d9ab10f65bbeaaebc72b1cbb1ee4b4ef0ebfe3902a.jpg)



Figure 1 An example of F-Bucket

![](images/607239fe3b10ae806a729eef21fb18cf6f528cc3c693804e4e8adda8ed41dc30.jpg)



Figure 2 Network Topology

median result. During a continuous Median query, the above process repeats round by round. The range refining algorithms finds the range where the median value is located and subdivides it to all intermediate buckets. After a few rounds all the intermediate buckets handle a range of length 1 and the rest ranges are handled by two boundary buckets. The median value is located in the range of intermediate buckets and exact median results can be calculated continuously. When the median runs out the range of intermediate buckets, the range refining algorithm will adjust the ranges of buckets.

# Algorithm 1 Intermediate Node Processing

1: Generate value v; //start processing   
2: Build F-Bucket Fv;   
3: Receive F-Buckets from children;   
4: for all Fi in received F-Bucket list do   
5: Fv = Merge (Fv, Fi);

6: end for;   
7: Transmit $F \nu ;$ //transmit message to parent node;

Algorithm 2 Calculating\_Median (F, n)   
```txt
1: rank = n/2;
2: sum = 0;
3: i = 0;
4: while sum < rank do
5:    sum = sum + F.bucket[i].count;
6:    i++;
7: end while
8: Return range of F.bucket[i]; 
```

# 3.2.1 Intermediate node operation

The processing of an intermediate node is illustrated in algorithm 1. Basically, the intermediate node collects the F-Buckets, merges them and sends the merged one to upper level. The merging of two F-Buckets is simple because the range of each bucket is fixed, we only need to merge their count of corresponding buckets that are associated to the same range. As shown in Figure 3, F1 and F2 have 3 and 4 nonempty (count > 0) buckets respectively, in the merged F-Buckets F, there are 5 buckets and the counts in corresponding buckets of $F _ { 1 , }$ F2 are summed. For example, the buckets in F1 and F2 with same range [11, 20] have count of 6 and 1 respectively, and then the count of bucket [11, 20] in F is 7 (6+1).

![](images/6d3ba2fa820a630a71290071faf2c5bce347b5fbc1a8e41410edcc66c3a39e04.jpg)



Figure 4 Range refining in initial rounds

# 3.2.2 Result calculation

With the received F-Bucket in sink, we can answer a Median query. Algorithm 2 illustrates the steps to compute a Median result. According to Algorithm 2, the return value is a range that covers the query result. If the returned range is of length 1, we can get the exact median.

# 3.3 Range Refining

At the very beginning, all buckets are equal length; during the continuous query, the range assignment will be adjusted to fit the value distribution better. The refining process assigns more buckets to the range where the queried median is located and adjust this assignment while the value distribution changes. As the historical data accumulated at the sink, we have an anterior prediction about the real median value. Based on this prediction, we can adjust the range granularity associated to each bucket. The refining algorithm will assign a fine granularity monitoring to the range which covers the median value with high probability and a coarse granularity monitoring to the rest. Most buckets are assigned to the candidate range (called focused window) and each bucket handles a range of length 1 after a few rounds.

With the refining algorithms, we can guarantee the exact result for arbitrary query. The basic idea of a refining algorithm is multi-pass search. The continuous query rounds are divided to 3 different types. Considering median, in initial rounds we try to find a narrow range contains the median value. This is achieved by subdividing the current range where median is located. At last, most of buckets are assigned to monitor this range and each of them is

![](images/6fd0eb85828eae1ee99ffd9744029dd5d161c44cdde8de40ff023ff2b06bafd7.jpg)



Figure 3 Merge Two F-Buckets

corresponding to a value interval of length 1. Then in the following continuous rounds, querying will focus on this range (focused window) and extract the accurate median value. When the median value runs out this range due to value changing, one or more refresh rounds will rediscover the focused window.

1) Initial rounds: At the very beginning, Initial rounds are applied to detect the focused window, as shown in Figure 4, assuming that the sensor values are among S = [0, 174] and there are at most 7 buckets in one F-Bucket.

In the first round, the monitoring range S is divided in to 7 equal parts and each bucket counts the number of values that lie in its range. After this round, as shown in Figure 4 the median value is located in bucket A. The range associated to A ([50, 74]) is subdivided in the second round and handle by bucket A1 to A5. The rest ranges are combined and handled by B ([0, 49]) and C ([75, 174]). After the second round, the range covering median shrinks to [60, 64] (A3) which is narrow enough and regarded as the focused window. The process of finding the focused window may continue for several rounds and it will end in at most log() rounds. In the following continuous rounds, bucket A1 to A5 are assigned to the focused window and each bucket handles a range of length 1.

2) Continuous rounds: Each Continuous round can provide an accurate answer for the median query till the median value runs out the focused window. Process of each node in continuous rounds is similar to that in initial rounds.

![](images/3bc89f9526ee8d9b030e81242eb28a93ddc6e343ed9b0ef7fa6a42f287163295.jpg)



Figure 6: Hierarchical Refining Algorithm

3) Refresh rounds: When the median value runs out the focused window due to value changing, the refresh round will relocate the focused window to adapt the new data distribution. We propose two algorithms for refining the range assignment, Slip refining and Hierarchical refining.

Slip refining: This algorithm slips the focused window to the same direction which the median value moved towards. The slipping distance is equal to the length of focused window.

As shown in Figure 5, if the median has run into the range of bucket C ([65, 174]), then in the refresh round the ranges handled by B and A1 to A6 are combined to a new range [0, 64] which is assigned to B and the focused window slips to [65, 69] and is assigned to A1 to A6 again. Bucket C charges the rest range. This process will continue till the focused window catches up the median again.

Hierarchical refining: The second refining algorithm is Hierarchical refining. In the Slip refining, we guess that the median lies in the range adjacent to current focused window and slip the window to the adjacent range. However, if the median changes fast, we need multiple rounds to catch up with it. In the Hierarchical refining, we first use an additional round to relocate the rough range covering median. Then slip the focused window to it. A running example is illustrated in Figure 6. In this example, the median value runs out the current focused window [60, 64] to range [65, 174] handled by bucket C. The range of bucket C is subdivided and assigned to buckets A1 to C and the current focused window is merged to bucket B. Buckets A1 to A5 each handles a range with equal length to the prior focused window which is 5 in this example. Since we assume that the data changing is slow, median value will be located in A1 to A5 with high probability. As shown in Figure $^ { 6 , }$ the focused window is relocated to range [65, 69] and new continuous rounds begin.

![](images/bf4e74805be224f09eb6df0cadfb225233281e43c22e1400171d342eb6779a64.jpg)



Figure 7 Example of Merging Two AF-Buckets

# 4 WAVELET-LIKE APPROXIMATE QUERY ALGORITHM

When sensor values change quickly, the range refining process will be called frequently which leads to very high communication cost. In fact, under such a situation, the temporal correlation over time is weak and it is not appropriate to use F-Bucket any more. Thus, we propose a wavelet-like approximate algorithm to get approximate answers to the query. In this algorithm, queries in different rounds are independent, so the data changing over time will not affect the query processing. We still use the histogram summary to store the information. Different from the exact query, each bucket in this structure stores the average of a group of values and buckets are sorted by their values, which is similar to the formulation of Haar wavelet [24]. Intermediate sensors combine data structures from downstream nodes, insert their own values and forward the structure to upper nodes. Finally, at the sink we get an aggregated data structure, with which we can run varying queries. For example, if we want the median value, we can choose the value in the middle position of this list. In the following sections we will show details of this algorithm as well as the error bound in the worst case.

# 4.1 Data Structure in Approximate Query

In the approximate query algorithm, the data structure is different from F-Bucket and we will refer to the approximate structure as $\scriptstyle \mathbf { A F - B u c k e t } ,$ where each AF-Bucket is represented as: $F ^ { \prime } = \{ [ b _ { 0 } , b _ { 1 } , . . . , b _ { i } , . . . , b _ { m - }$ 1], count(F’), loglen(F’)}; (bi<bi+1). F’ consists of m sorted values and an integer count which denotes the number of values rolled in to this structure. Variable loglen indicates the number of values rolled in one bucket loglen = log(count/m). In this structure, bi is the approximate value along with For example an $\begin{array} { r l } { \mathrm { f u n c t i o n } _ { \mathrm { A F - B u c k e t } } r a n k ( b _ { i } ) } & { = } \\ { \mathrm { A F - B u c k e t } r ^ { \prime } } & { = } \end{array}$ count×(i/m) $\{ [ 3 , 6 , 1 0 , 1 5 ] , 8 , 1 \} ,$ , count(F’) = 8 means there are 8 values in this structure and $\begin{array} { r } { l o g l e n ( F ^ { \prime } ) = 1 } \end{array}$ means each bucket represents $2 ^ { 1 } = 2$ values. Value 3 is the average of the 0th and 1th values and 6 is the average of the 2th and 3th values, etc.

![](images/021ba770a32940304cf119438008d7a80b1cbf30b695ed68c536c1bcff970d6e.jpg)



Figure 8 Example of Zero-padding

# 4.2 Query Processing

The query processing in approximate query has no range refining steps. Each round is an independent one-shot query. In each round, the leaf nodes construct new AF-Buckets and insert their values in. Then the AF-Buckets are delivered to their parents. In an intermediate node, the received AF-Buckets are merged together to be an integrated one. This merging process reduces transmissions at the cost of losing some information. Finally, the sink aggregates all received AF-Buckets to an integrated one and calculates the query results. The following subsections shows details of the merging process in the intermediate nodes and the result calculation in the sink.

# 4.2.1 Intermediate node operation

The processing in an intermediate node is illustrated in Algorithm 3. During the process of inserting the own value v to the AF-Bucket list, two cases have to be dealt with. If there is one AF-Bucket $F ^ { \prime }$ in the list with count less than m, we can insert v to the value list of $F ^ { \prime }$ and resort the list. If all AF-Buckets’ count are no less than $m ,$ we construct a new AF-Bucket with only one value v and add it to AF-Bucket list. The merging process of two AF-Buckets ${ F ^ { \prime } } _ { a } { = } \{ [ a _ { 0 } , a _ { 1 } , . . . , a _ { m - 1 } ] ,$ , count(F’a), loglen(F’a)} and $F ^ { \prime } { } _ { b } { = } \{ [ b _ { 0 } , b _ { 1 } , . . . , b _ { m - 1 } ]$ , count(F’b), loglen(F’b)} is discussed as follows:

1) If $c o u n t ( F ^ { \prime } { } _ { a } ) ~ = ~ c o u n t ( F ^ { \prime } { } _ { b } ) ~ > ~ m$ (in other words $l o g l e n ( F _ { a } ^ { \prime } ) = l o g l e n ( F _ { b } ^ { \prime } ) > 0 )$ , we put all values in $F ^ { \prime } { } _ { a }$ and $F ^ { \prime } { } _ { b }$ into a double size (2\*m) temp list T and these values are resorted while being inserted to T. Then, the average of every two values in list T is calculated to construct the merged AF-Bucket $\boldsymbol { F ^ { \prime } } _ { c } .$ Finally, double the variable count and have the loglen plus one. This process is shown in Algorithm 4. Figure 7 shows an example of the merging of two AF-Buckets. In this example, $F ^ { \prime } { } _ { a }$ and $F ^ { \prime } { } _ { b }$ are two input AF-Buckets and $F ^ { \prime } { } _ { c }$ is the merged AF-Bucket. As described in Algorithm 4, the values in $F ^ { \prime } { } _ { a }$ and F’b are put into the temp list T. The values in T are sorted. As shown in Figure $^ { 7 , }$ in this example we assume that the sorted list T is [a0, b0, a1, a2, b1, a3, b2, b3]. Then the average of every pair of values is used to construct a new AF-Bucket $F ^ { \prime } { } _ { c }$ with the count doubled and loglen equals to one plus that in $F ^ { \prime } { } _ { a } \left( F ^ { \prime } { } _ { b } \right)$ .

Algorithm 3 Intermediate Node Processing   
1: Generate value v; //start processing
2: Receive AF-Buckets $\{F'_{i}\}$ from children;
3: Insert v to $\{F'_{i}\}$ ;
4: while exist $F'_{i}$ $F'_{j}$ in $\{F'_{i}\}$ and $\loglen(F'_{i}) = \loglen(F'_{j})$ do
5: Merge ( $F'_{i}, F'_{j}$ );
6: end while
7: Transmit the merged $\{F'_{i}\}$ ; //transmit to parent;

2) If count(F’a) < m and count $( F ^ { \prime } b ) < m ,$ the merging is simpler. Values in $F _ { a } ^ { \prime }$ and $F ^ { \prime } { } _ { b }$ are put together to a temp array and resorted. Then the first m values are selected to store in $F ^ { \prime } { } _ { a }$ and the rest values are put to $F ^ { \prime } { } _ { b , }$ If count(F’a) + coun $\forall ( F ^ { \prime } b ) \leq m$ , then $F ^ { \prime } { } _ { b }$ is empty and can be removed from the AF-Bucket list.

Note that after the merging process, there may be more than one AF-Bucket in the list with different loglen, because only the AF-Buckets with same loglen can be merged. All of them are transmitted to upstream nodes and the number of AF-Buckets is less than log(n/m).

# 4.2.2 Result calculation

After the sink receives AF-Buckets, it merges them in the same way as discussed above. If there is still more than one AF-Bucket in the list that cannot be merged, the zero-padding merging algorithm is applied. If the loglen (count) of AF-Bucket $F ^ { \prime } { } _ { i }$ is smaller

than that of $F ^ { \prime } { } _ { i + 1 , }$ we pad zeros to $F ^ { \prime } { } _ { i }$ till $F ^ { \prime } { } _ { i }$ and $F ^ { \prime } { } _ { i + 1 }$ are equal length. Figure 8 shows an example of double an AF-Bucket by zero-padding. By this way, all the $\mathrm { A F _ { - } }$ Buckets are merged pair after pair. At last we get an integrated AF-Bucket and calculate the query result with it. For example in the Median query, we just remove the prior zeros in the final value list and use the value in the middle position of the remaining values as the approximation of the real median value in sensor network.

Algorithm 4 Merge $( \mathrm { F _ { a } , F _ { b } ) }$   
1: indexA = 0;
2: indexB = 0;
3: for i from 0 to 2×m - 1 do
4:    if indexB >= m or (indexA < m and F'_a[indexA] < F'_b[indexB])
5:    T[i] = F'_a[indexA];
6:    indexA++;
7: else
8.    T[i] = F'_b[indexB];
9:    indexB++;
10: end if
11: end for
12: for j from 0 to m-1 do
13:    F'_c[i] = (T[2i] + T[2i + 1])/2;
14: end for
15: count(F'_c) = 2 × count(F'_a);
16: loglen(F'_c) = loglen(F'_a) + 1;
17: Return F'_c;

# 4.3 Error bound

Merging of two AF-Buckets will lose information and cause error to the query results, take the Median query as an example, the relative percentage error is defined as:

$$
\operatorname{err} = \frac {\text { realRank } (c) - n / 2}{n} \tag {1}
$$

Though merging introduces errors, we can show that the error is bounded in the worst case, as stated in the following Theorem.

Theorem 1. The error introduced by merging of two AF-Buckets is within $O ( l o g ( n ) / m )$ .

Proof: Firstly we consider the case of merging of two AF-Buckets F’a and F’b with count = m and thus $l o g l e n ( c o u n t / m ) = 0$ . The merged result is denoted as $\boldsymbol { F ^ { \prime } } _ { c }$ . Note that in this situation value aj and bk have the exact rank.

If $c _ { i } \ = \ ( a _ { j } \ + \ b _ { k } ) / 2 , \ a _ { j } \ < \ b _ { k } ,$ minimum rank of ci is lowran $k ( c i ) = r a n k ( a _ { j } ) + r a n k ( b _ { k - 1 } )$ and the maximum rank of ci is $h i g h r a n k ( c i ) ~ = ~ r a n k ( a j + 1 ) ~ + ~ r a n k ( b k )$ . So the maximum rank error of ci is:

$$
\operatorname{errorRank} \left(c _ {i}\right) = \operatorname{rank} \left(a _ {j + 1}\right) - \operatorname{rank} \left(a _ {j}\right) + \operatorname{rank} \left(b _ {k}\right) - \operatorname{rank} \left(b _ {k - 1}\right) = 2 \tag {2}
$$

Note that if k = 0, maximum rank error of ci will be less, so in the following discussion, we just consider the situation that $k > 0$ . The situation of $c _ { i } = ( b _ { k } + a _ { j } ) / 2 ,$ , $a _ { j } > b _ { k }$ is the same to discussion above.

If $c _ { i } = ( a _ { j } + \mathsf { a } _ { j + 1 } ) / 2 , a _ { j } < \mathsf { a } _ { j + 1 } ,$ the minimum rank of average value ci is lowran $\dot { \ c } ( c i ) \ = \ r a n k ( a _ { j } ) \ + \ r a n k ( b _ { k } )$ in which bk is the nearest value that smaller than aj and the maximum rank of ci is highrank(ci) = rank(aj+1) + rank(bk+1) in which bk+1 is the nearest value bigger than $a _ { j + 1 }$ .

$$
\operatorname{errorRank} \left(c _ {i}\right) = \operatorname{rank} \left(a _ {j + 1}\right) - \operatorname{rank} \left(a _ {j}\right) + \operatorname{rank} \left(b _ {k + 1}\right) - \operatorname{rank} \left(b _ {k}\right) = 2 \tag {3}
$$

At the end, the rank error of ci is at most:

$$
\operatorname{errorRank} \left(c _ {i}\right) = 2 \tag {4}
$$

Secondly, we consider the case of merging of two AF-Buckets A and B with $c o u n t \ = \ m { \times } 2 ^ { l o g l e n }$ and thus loglen>0.

If $c _ { i } = ( a _ { j } + b _ { k } ) / 2 , a _ { j } < b _ { k } ,$ minimum rank of ci is lowrank(ci) = lowrank(aj) + lowrank(bk-1) and the maximum rank of ci is $h i g h r a n k ( c i ) = h i g h r a n k ( \mathsfit { a } _ { j + 1 } ) +$ highrank(bk). So the maximum rank error of ci is:

$$
\begin{array}{l} \operatorname{errorRank} \left(c _ {i}\right) = \operatorname{highRank} \left(C _ {i}\right) - \operatorname{lowRank} \left(c _ {i}\right) \\ = \text { highRank } (a _ {j + 1}) - \text { lowRank } (a _ {j}) + \text { highRank } (b _ {k}) - \text { lowRank } (b _ {k - 1}) \\ = \text { errorRank } (a _ {j + 1}) + 2 ^ {\text { loglen }} + \text { errorRank } (b _ {k}) + 2 ^ {\text { loglen }} \tag {5} \\ \end{array}
$$

Because AF-Buckets A and B have the same count and loglen, the rank error of ai and bi are the same, then

$$
\operatorname{errorRank} \left(c _ {i}\right) = 2 \times \left(\operatorname{errorRank} \left(a _ {j}\right) + 2 ^ {\text { loglen } (A)}\right) \tag {6}
$$

Similarly we can prove that in other cases, the maximum rank error is the same to function (6).

Then, according to the epagoge:

$$
\operatorname{loglen} = 1: \text { errorRank } (C 0) = 2 ^ {l}
$$

$$
\operatorname{loglen} = 2: \text { errorRank } (C 1) = 2 \times (\text { errorRank } (C 0) + 2 ^ {I}) = 2 \times 2 ^ {2}
$$

Assume:

$$
\operatorname{loglen} = i: \text { errorRank } (C i) = i \times 2 ^ {i}
$$

then:

$$
\operatorname{loglen} = i + 1: \text { errorRank } (C i + I) = 2 \times \left(i \times 2 ^ {i} + 2 ^ {i}\right) = (i + I) \times 2 ^ {i + I} \tag {7}
$$

In function (7), errorRank(Ci) denotes the maximum rank errors in an AF-Buckets with loglen i. If there are n nodes in the sensor network, the maximum value of loglen in the final AF-Bucket is log(n/m), so the maximum percentage rank error is:

$$
\frac {\log \left(\frac {n}{m}\right) \times \frac {n}{m}}{n} <   \frac {\log (n / m)}{m} \tag {8}
$$

Finally, during the result calculating, we use the zero-padding algorithm which may bring some errors in to query results. However, since our zero-padding and merging are from the AF-Bucket with smaller count to the AF-Bucket with bigger count pair after pair, so the biggest AF-Bucket does not need to pad zeros. Then the count in final integrated AF-Bucket is at most 2n and the maximum percentage rank error is log(2n/m)/m. Thus the error bound is O(log(n)/m).

# 5 HYBRID APPROACH

According to prior discussion, it is clear that when the data changing rate is low, the exact query scheme achieves very high efficiency. However, when sensor values change quickly, the range refining process will be called frequently which leads to very high communication cost. In this case, the approximate approach becomes more stable to answer the queries. However, how to adaptively select the appropriate scheme is non-trivial. To fully leverage the advantages of both methods, in this work, we propose a novel metric named efficiency which models how quickly the sensor value changes and its effect on query processing. Using this metric, our hybrid scheme adaptively applies different query algorithms under different circumstances during the query processing. The definition of efficiency metric will be described in detail in the following paragraph.

At the very beginning of that query, we use the exact query algorithm. Due to the data changing, the exact answer can not be obtained each round. The median will run out the focused window in some rounds and some other rounds are used to refine the range assignment. We denote all these rounds as noanswer round. The rounds that can provide an exact result as exact answer rounds. Then the ratio between the numbers of these two types of rounds specifies the efficiency of current query, efficiency = number(noanswer) / number(answer) . When the efficiency parameter rise above a certain user specified threshold, it will be switched to the approximate algorithm automatically. In the experiment of this paper, the efficiency parameter is set to 0.5 which indicates that there is at most one no-answer round per two exact answer rounds.

Our approach can also switch to the exact query algorithm when the data changing is slow. The switching parameter dependens on the efficiency parameter. Assume that when the median runs out the focused window, one additional round is used to refine the range assignment. Thus there are two noanswer rounds each time when the median run out focused window. So the number of exact answer rounds between two refinements is at least 2/efficiency. In other words, the median values will stay in the focused window for at least 2/efficiency rounds, and then the change of the median value is less than (m−2)×efficiency 2 (m denotes the number of buckets in exact query and then m-2 denotes the width of focused window) per round. When applying the approximate algorithm, we cache the approximate results of recent several rounds. When the results’ change is less than $\frac { ( \mathrm { m } - 2 ) \times \mathrm { e f f i c i e n c y } } { 2 }$ per round, we can switch to the exact query algorithm.

# 6 EVALUATION

In this section, we evaluate our hybrid algorithms for Median query in varying conditions. We also compare our algorithm with the LIST and Q-digest [28] approach. LIST is a simple un-aggregated data summarization scheme in which the summary is a list of distinct sensor values and a count for each value. Intermediate nodes receive summaries from its children and then form a list of all distinct values with their counts in the sub-tree. All distinct values and their counts are delivered to sink where quantile or other queries are answered. With this scheme we can derive exact answers for queries at the cost of high transmission traffic. We did not compare with [4] because the approaches developed in [4] mainly focused on distributed stream environment, not specialized for a wireless sensor network. The simulated sensors are organized on a balanced routing tree. Each parent nodes have 4 children. So the total number of sensors in this network can be 5, 21, 85, 341, 1365, 5461, etc. The monitoring data range is [1, 28]. Here we assume the wireless communication is ideal and there is no link loss. Thus we focus on the query algorithms. In each experiment, we run the continuous median queries for 500 rounds and calculate the average performance. Here we use the metric number of transmissions to evaluate the traffic cost of all these approaches which is defined as the total size of transmitted data packets in one round.

# 6.1 Experiment One

Firstly, we consider the exact query algorithm. Since LIST and our Flexible Buckets algorithms both can provide the exact answer for median query, we just evaluate their traffic cost. Each round, the sensor values has 25% probability to plus one and 25% probability to minus one. They have 50% probability to stay the same as prior round. The number of sensor nodes in the network is varying from 21 to 5461. The results are illustrated in Figure 9 where ‘Slip’ and ‘Hierarchical’ denote two different refining algorithms. The two approaches are tested on two different initial data distributions. Random data denotes that the sensor values are randomly generated in the beginning and Correlated data means the sensor values are correlated to each other. From Figures 9(a) and (b), we can find that our exact query algorithm transmits much less bytes than the LIST scheme. Moreover, the effects of two refining algorithms are similar on both data sets. This is because the data changing speed is slow, however, when data changes quickly, the performance of two refining algorithms will be different, which will be shown in the third experiment.

# 6.2 Experiment Two

Secondly, we evaluate the performance of the approximate algorithm (denoted as Wavelet-like). Precision and traffic cost are considered in our experiments. For a Median query, the relative percentage error is defined as $\begin{array} { c } { { \mathrm {  ~ \ q u e r ~ } } } \\ { { \mathrm { e r r } = \frac { \mathrm {  ~ \ r e a l r a n k } ( \mathrm {  ~ c } ) - n / 2 } { \mathrm {  ~ \ q u e r ~ } } } } \end{array}$ realrank(c)−??/2. In the first test, the number of values in an AF-Bucket structure varies from 6 to 32. The network size is fixed on 1365 sensor nodes. This test is conducted over two types of data sources, random date and correlated data. The results are reported in Figure 10. In Figure 10, the percentage error of median query decreases from 7% to less than 2% as the AF-Bucket size increasing from 6 to 32. In other words, the performance will be better with more traffic. When the AF-Bucket size is 12, the accuracy of median query is already higher than 97% on both random and correlated data. Then the next experiment is used to compare the traffic cost of our approximate approach (Wavelet-like) and LIST. The initial sensor values are generated randomly. The AF-Bucket size is set to 12 with which the percentage error is lower than 3% as illustrated in Figure 10. Figure 11 shows the maximum message size on different network size. Compared with the LIST approach, the maximum message size of our scheme is much less. Thus, the traffic load of sensor nodes in our approach is more balanced. Q-digest [28] is an important approximate approach on holistic queries. We compare our approximate algorithm with Q-digest. In this test, the percentage errors of both algorithms are set around 2% with appropriate parameter configuration. Figure 12 reports the transmission cost of the two algorithms, where our Wavelet-like approximate algorithm achieves the same precision with much less communication cost.

![](images/bd10c65d64b6def1154df1f8ab8eb2096aa3aa243344ecf9ce2258db8af157b0.jpg)



Figure 9(a) Traffic on Random Data

![](images/e6835634cd69c52dc82d18d2ffeeb5ac0bab74c5f68f285e60c3554c9d52f1e6.jpg)



Figure 9(b) Traffic on Correlated Data

![](images/7622dae528ede2bbd86c6acbc773013dee869ab32ebdd2f80b40f6cec8290971.jpg)



Figure 10 Percentage Errors

![](images/40014a312433ff2c938936b79d7602c8ea4246801bfc594f4afbaa9f4a1c5882.jpg)



Figure 11 Maximum Message Size

![](images/f42df7b1c78cbb06d8963367ea23f66f0c0d487eb383d6b4dc8a0b227e5cce80.jpg)



Figure 12 Traffic on Varying Networks

![](images/ce51901ce5c05977863e39d203fff68fa0b5a8f00183e4e7bf4ca26ab2ea7b6d.jpg)



Figure 13 Traffic on Changing Data

# 6.3 Experiment Three

In this experiment, we evaluate the performance of the hybrid algorithm. In this simulation we assume that the data changes to the same direction (worst case for exact query algorithm) and each node has 50% probability to change its value and 50% probability to stay the same. The data changing rate denotes the maximum value change of sensors in one round. For example when the changing rate is 10 per round, then each sensor value has 50% probability to change by [1, 10]. In this experiment, the efficiency parameter (in section 5) is set to 0.5. During the experiment, the data changing rate is varying from 5 to 30 per round.

The performances of exact query algorithms and approximate algorithm are shown in Figure 13. When the data changing rate is less than 10 per round, the exact query algorithms Slip and Hierarchical provide exact query answers with little communication cost. As the changing rate increasing, the range refining becomes more and more frequently and significantly increasing the communication cost. When the changing rate is above 15 per round, the approximate algorithm performs better than the above two methods. According to Figure 13, the Slip refining algorithm performs better than Hierarchical method. It is because that the Hierarchical refining needs an additional relocating round. So in the following test of the hybrid approach, we adaptively combine the Slip algorithm and Wavelet-like approximate algorithm. In the last test, we compare our approach with the Qdigest scheme. Both Q-digest and our hybrid approach achieve the percentage error around 2%. Then their communication costs are shown in Figure 14.

The experimental results show that the hybrid approach works better in varying conditions. The communication cost of our approach is much lower than Q-digest for varying data changing rate, especially when the sensor values change slowly, our hybrid method can reduce the traffic cost more than a half. As discussed in Section 5, our hybrid approach adaptively applies different algorithm under varying circumstances. As illustrated in Figure 14, the hybrid method selects the exact query scheme (Slip) when the data changing rate is low which saves more than a half traffic cost than Q-digest. When the dynamics of sensory readings become high, in this experiment, more than 15 per round, our hybrid approach automatically switches to the approximate algorithm.

![](images/7309f0c82392f9cb353773f4a28f347c7b6ecdffb4dab822307f09166f6a4065.jpg)



Figure 14 Traffic on Changing Data

# 7 CONCLUSIONS

In this paper, we tackle one type of popular queries, continuous holistic query, over sensor network. Compared to the counterpart of this type of query, non-holistic query, not much work has been done. However, holistic query is indeed important for many sensor network applications to collect statistical data. To avoid sending all the sensing data back to the sink, we propose two approaches to monitor continuous holistic queries, an exact one, Flexible Bucket (F-Bucket), to answer queries accurately and a wavelet-like approximate one to obtain the results with small error. Moreover, we present a hybrid approach based on the exact and approximation solutions, which applies the exact algorithm when the data changing rate is low and uses the approximation one when the rate becomes high. Experimental results show that the hybrid approach can achieve the similar accuracy but with much less traffic cost compared to the other approximate methods.

In this paper, we take one typical query Median as an example to illustrate our idea. In fact, the proposed methods can be naturally extended to solve other holistic queries. For example, all Quantile queries can be solved by our approach with different parameters. With the exact query scheme, we obtain varying quantiles by adjusting the position of focused window during range refining process. For the approximate scheme, different quantiles can be directly calculated with the data distribution in AF-Bucket. Generally, as both our exact and approximate schemes can return the data distribution of all sensor values using F-Bucket and AF-Bucket respectively, many other types of queries can be answered with the data distribution.

# REFERENCES

[1] R. Akbarinia, P. Valduriez and G. Verger, “Efficient Evaluation of SUM Queries Over Probabilistic Data”, IEEE Transactions on Knowledge and Data Engineering, vol.25, no.4, pp.764-775, 2013.   
[2] M. Cardei, J. Wu, “Energy-efficient Coverage Problems in Wireless Ad-Hoc Sensor Networks,” Computer Communications 29(4), 2006.   
[3] C.M. Chen, Y.H. Lin, Y.C. Lin and H.M. Sun, “RCDA: Recoverable Concealed Data Aggregation for Data Integrity in Wireless Sensor Networks”, IEEE Transactions on Parallel and Distributed Systems, vol.23, no.4, pp.727-734, 2012.   
[4] G. Cormode, M. Garofalakis, S. Muthukrishnan and R. Rastogi, “Holistic Aggregates in a Networked World: Distributed Tracking of Approximate Quantiles,” in Proceedings of SIGMOD, 2005.   
[5] J. Considine, F. Li, G. Kollios and J. Byers, “Approximate Aggregation Techniques for Sensor Databases,” in Proceedings of ICDE, 2004.   
[6] W. Choi, S. K. Das, “A Novel Framework for Energy-Conserving Data Gathering in Wireless Sensor Networks,” in Proceedings of INFOCOM, 2005.   
[7] D. Chu, A. Deshpande, J. M. Hellerstein and W. Hong, “Approximate Data Collection in Sensor Networks using Probabilistic Models,” in Proceedings of ICDE, 2006.

[8] L. Chih-Yu, P. Wen-Chih and T. Yu-Chee, “Efficient In-Network Moving Object Tracking in Wireless Sensor Networks,” IEEE Trans. on Mobile Computing, vol. 5, pp. 1044 - 1056, 2006.   
[9] A Deshpande, C. Guestrin, S. Madden, J. M. Hellerstein and W. Hong, “Model-Driven Data Acquisition in Sensor Networks,” in Proceedings of VLDB, 2004.   
[10] A. Deligannakis, Y. Kotidis and Y. Roussopoulos, “Hierarchical In-Network Data Aggregation with Quality Guarantees,” in Proceedings of EDBT, 2004.   
[11] J. Gray, A. Bosworth, A. Layman and H. Pirahesh, “Data Cube: A Relational Aggregation Operator Generalizing Group-by, Cross-tab, and Sub-totals,” in Proceedings of ICDE, 1996.   
[12] M. B. Greenwald and S. Khanna, “Space-Efficient Online Computation of Quantile Summaries,” in Proceedings of SIGMOD, 2001.   
[13] M. B. Greenwald and S. Khanna, “Power-Conserving Computation of Order-Statistics over Sensor Networks,” in Proceedings of ACM PODS, 2004.   
[14] J. M. Hellerstein, W. Hong, S. Madden and K. Stanek, “Beyond Average : Toward Sophisticated Sensing with Queries,” in Proceedings of IPSN, 2003.   
[15] J. Hershberger, N. Shrivastava, S. Suri and C. D. Toth, “Adaptive Spatial Partitioning for Multidimensional Data Streams,” in Proceedings of ISAAC, 2004.   
[16] H. Jiang, J. Cheng, D. Wang, C. Wang, and G. Tan. A General Framework for Efficient Continuous Multidimensional Top-k Query Processing in Sensor Networks”, IEEE Transactions on Parallel and Distributed Systems. Vol.23, no.9, pp.1668-1680, 2012.   
[17] Y. Kotidis, “Snapshot Queries: Towards Data-Centric Sensor Networks,” in Proceedings of ICDE, 2005.   
[18] M. Li, and Y. Liu, "Iso-Map: Energy-Efficient Contour Mapping in Wireless Sensor Networks", IEEE Transactions on Knowledge and Data Engineering, vol 22, no.5, pp. 699-710, 2010.   
[19] M. Li, Y. Liu, and L. Chen, "Non-Threshold based Event Detection for 3D Environment Monitoring in Sensor Networks", IEEE Transactions on Knowledge and Data Engineering, vol. 20, no.12, pp. 1699-1711, 2008.   
[20] Y. Liu, Y. He, M. Li, J. Wang, K. Liu and X.Y. Li, “Does wireless sensor network scale? A measurement study on GreenOrbs”, IEEE Transactions on Parallel and Distributed Systems, vol.24, no.10, pp.1983-1993, 2013.   
[21] S. Madden, M.J. Franklin, J. Hellerstein and W. Hong, “TAG: a Tiny AGgregation Service for Ad-Hoc Sensor Networks,” in Proceedings of OSDI, 2002.   
[22] G. Manku and R. Motwani, “Approximate Frequency Counts over Data Streams,” in Proceedings of VLDB, 2002.   
[23] S. Madden, R. Szewczyk, M. J. Franklin and D. Culler, “Supporting Aggregate Queries Over Ad-Hoc Wireless Sensor Networks,” in Proceedings of WMCSA, 2002.

[24] Y. Matias, J. S. Vitter and M. Wang, “Wavelet-Based Histograms for Selectivity Estimation,” in Proceedings of SIGMOD, 1998.   
[25] C. Olston, B. T. Loo and J. Widom, “Adaptive Precision Setting for Cached Approximate Values,” in Proceedings of SIGMOD, 2001.   
[26] S. Papadopoulos, A. Kiayias and D. Papadias, “Secure and Efficient In-Network Processing of Exact SUM Queries”, in Proceedings of ICDE 2011.   
[27] B. Przydatek, D. Song and A. Perrig, “SIA: Secure Information Aggregation in Sensor Networks,” in Proceedings of SenSys, 2003.   
[28] N. Shrivastava, C. Buragohain, D. Agrawal and S. Suri, “Medians and Beyond: New Aggregation Techniques for Sensor Networks,” in Proceedings of ACM SenSys, 2004.   
[29] M. A. Sharaf, J. Beaver, A. Labrinidis and P. K. Chrysanthis, “TiNA: A Scheme for Temporal Coherency-Aware In-Network Aggregation,” in Proceedings of MobiDe, 2003.   
[30] H.O. Tan, I. Korpeoglu and I. Stojmenovic, “Computing Localized Power-Efficient Data Aggregation Trees for Sensor Networks”, IEEE Transactions on Parallel and Distributed Systems, vol.22, no.3, pp.489-500, 2011.   
[31] C. Wang, C. Jiang, S. Tang and X.Y. Li, “SelectCast: scalable data aggregation scheme in wireless sensor networks”, IEEE Transactions on Parallel and Distributed Systems, vol.23, no.10, pp.1958-1969, 2012.   
[32] K. Xing, F. Liu, X. Cheng, and D. H.C. Du, "Real-time Detection of Clone Attacks in Wireless Sensor Networks", in Proceedings of ICDCS, 2008.   
[33] Y. Yao and J. Gehrke, “The Cougar Approach to In-Network Query Processing in Sensor networks,” in Proceedings of SIGMOD, 2002.   
[34] M. Ye, K.C.K. Lee, W. C. Lee, X. Liu and M.C. Chen, “Querying Uncertain Minimum in Wireless Sensor Networks”, IEEE Transactions on Knowledge and Data Engineering, vol.24, no.12, pp.2274-2287, 2012.   
[35] M. Ye, W.C. Lee, D.L. Lee and X. Liu, “Distributed Processing of Probabilistic Top-k Queries in Wireless Sensor Networks”, IEEE Transactions on Knowledge and Data Engineering, vol.25, no.1, pp.76-91, 2013.   
[36] Y. Yi, R. Li, F. Chen, A. X. Liu and Y. Lin, “A Digital Watermarking Approach to Secure and Precise Range Query Processing in Sensor Networks”, in Proceedings of INFOCOM, 2013.   
[37] L. Yu, J. Li, S. Cheng, S. Xiong and H. Shen, “Secure Continuous Aggregation in Wireless Sensor Networks”, IEEE Transactions on Parallel and Distributed Systems, vol.25, no.3, pp.762-774, 2014.   
[38] Y. Zhang, X. Lin, Y. Tao, W. Zhang and H. Wang, “Efficient Computation of Range Aggregates against Uncertain Location Based Queries”, IEEE Transactions on Knowledge and Data Engineering, vol.24, no.7, pp.1244-1258, 2012.

sensor networks, RFID applications, and mobile computing.

![](images/d19d725b64f596e343a3f3f75d11ab21a326c0233e7199041e181e3da8db25ef.jpg)



Kebin Liu received his BS degree in Department of Computer Science from Tongji University, in 2004, and the MS and PH.D degrees in Shanghai Jiaotong University, in 2007 and 2010. He is currently an assistant researcher in school of software and

TNLIST, Tsinghua University. His research interests include sensor networks and distributed systems.

![](images/2fd19c43ac0db56a50aa6a1cd74d02a28536a93d49822956c0df8f9995bb38d1.jpg)

Lei Chen received his BS degree in Computer Science and Engineering from Tianjin University, China, in 1994, the MA degree from Asian Institute of Technology, Thailand, in 1997, and the PhD degree in computer science from University of Waterloo, Canada, in

2005. He is now an Associate Professor in the Department of Computer Science and Engineering at Hong Kong University of Science and Technology. His research interests include multimedia database, sensor databases, peer-to-peer databases and probabilistic databases.

![](images/7aedaf0aac9c8427af48ffb9979ba4b14cbbcb9173f2f8f9d0390e0db15ea3c2.jpg)



Yunhao Liu received his BS degree in Automation Department from Tsinghua University, China, in 1995, and an MA degree in Beijing Foreign Studies University, China, in 1997, and an MS and a Ph.D. degree in Computer Science and Engineering at

Michigan State University in 2003 and 2004, respectively. He is now a professor in school of software and TNLIST, Tsinghua University. His research interests include sensor networks, security, and high-speed network.

![](images/c9081fabd985078e8e52479b007a6dd1d370338320d547082a69c6162badf2fa.jpg)



Wei Gong received the B.S. degree from the Department of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan, China, in 2003 and the M.S. and Ph.D. degrees in School of Software and Department of Computer Science and Technology

from Tsinghua University, in 2007 and 2012, respectively. His research interests include wireless