# Continuous Answering Holistic Queries over Sensor Networks

Kebin Liu†, Lei Chen‡, Minglu Li†, Yunhao Liu‡

†Shanghai Jiao Tong University ‡Hong Kong University of Science and Technology

kebin@cse.ust.hk, leichen@cs.ust.hk, li-ml@cs.sjtu.edu.cn, liu@cs.ust.hk

# Abstract

Wireless sensor networks (WSNs) are widely used for various monitoring applications. Users issue queries to sensors and collect sensing data. Due to the low quality sensing devices or random link failures, sensor data are often noisy. In order to increase the reliability of the query results, continuous queries are often employed. In this work we focus on continuous holistic queries like Median. Existing approaches are mainly designed for non-holistic queries like Average. However, it is not trivial to answer holistic ones due to their non-decomposable property. We propose two schemes for answering queries under different data changing conditions. While sensor data changes slowly, based on the data correlation between different rounds, we propose one algorithm for getting the exact answers. When the data changing speed is high, we propose another approach to derive the approximate results. We evaluate both designs through extensive simulations. The results demonstrate that our approach significantly reduces the traffic cost compared with previous works while maintaining the same accuracy.

# 1. Introduction

Sensor networks are now widely used in many applications, from habitat monitoring to location tracking and inventory management. In these applications, sensors are often deployed in a large area to obtain measurements of various kinds of parameters. In order to collect and analyze sensing data, users issue various queries, such as selection query, aggregate queries (Max, Count, and Sum) and etc. In general, aggregate queries can be classified into two different categories, non-holistic queries and holistic queries [11]. Non-holistic queries [8], such as Count and Sum, share the decomposable characteristic, that is, for an arbitrary query Q on data set S, there is a function f, such that for all S=S1∪S2, Q(S)=f(Q(S1), Q(S2)). If there is no such a function f, the query Q is holistic. For example, a quantile query means to find the certain value that has the user specified rank among all the values, for which we cannot find such a function f. There are many differences between these two types of queries. Non-holistic queries usually provide one single result (e.g. count value or sum value). Moreover, since these queries are decomposable, partial results from downstream sensor nodes can be combined to one single result in an intermediate node without loss of information. For example, with a tree-like routing structure [3, 13], the partial result of an Average query contains only two variables: the number of sensors and the summation of all values in a sub-branch rooted at the intermediate node. In a quantile query, however, the distribution information of all sensor values must be collected. Many efforts have been made for handling non-holistic queries, such as TAG [3, 13], Cougar [14] etc., but few of them, if any, addressed holistic queries.

Holistic queries are actually as popular as nonholistic queries. For example, when the values sensed by sensors have noise, it makes more sense to get a median result of the monitoring area than to derive an average result, since the noise may affect the average result largely. Thus, holistic queries can be used to get the approximate data distribution.

To answer holistic queries in a sensor network, many challenging issues need to be addressed. Obviously, a naïve approach requiring all sensors to deliver their values to the sink is energy inefficient. To save power, in-network aggregation [3] is introduced, in which messages from downstream nodes are merged into one, and the computation is distributed within the entire network. Due to the limitation of message size, the merging process may lose some information. Many prior attempts have been done to create sophisticated data structures and algorithms which try to keep the most useful information with a limited message size. Generally, these methods can only achieve approximate results with some error guarantee by introducing different restricts and pruning algorithms on the data structure [1, 8]. In many cases, we need the exact answers from the network. Furthermore, in many application scenarios, especially under tough environments such as coal mines and underwater, a WSN prefers continuous queries, and one-shot result is regarded as noisy and unreliable. In other words, the same query process needs to be executed periodically in order to improve accuracy and reliability. Strong correlations (temporal correlations) exist between data in different rounds, which are often overlooked by previous approaches in answering holistic queries.

In this paper, we explore the correlation between data of different rounds and present two approaches to monitor continuous holistic queries, one for getting the exact answers and the other one for deriving the approximate results. These two approaches are designed for different conditions. When sensory data changing speed is low, we can use the exact scheme to obtain exact query answers. When sensory data changes quickly, the exact scheme will be inefficient and thus we propose a wavelet-like approximate algorithm to derive approximate results efficiently. We take one example of the holistic queries, Median, to illustrate our proposals. In fact, the proposed methods can be naturally extended for other types of queries. The major contributions of this work are as follows:

1) We present a flexible bucket (F-Bucket)-based histogram approach to compute exact answer to a query. A histogram summary is used to collect the value distribution information. The query of a new round is guided by prior results so that the temporal correlations between two rounds are exploited. After several initial rounds, we can obtain the exact answers continuously.   
2) We also employ a wavelet-like approximate algorithm to offer a reasonable approximate result, especially when the sensing values in the sensor network change quickly.   
3) Through extensive simulations, we evaluate both designs and compare with previous approaches.

The rest sections of this paper are organized as follows. Section 2 illustrates prior works that are related to ours. Section 3 presents the overall process and refining algorithms of exact query algorithm. The wavelet-like approximate algorithm is presented in Section 4. In Section 5 we evaluate our algorithms with simulation experiments. We conclude this work in Section 6.

# 2. Related work

As mentioned in Section 1, for the decomposable queries, there are already much works that have been done, such as TAG [3, 13], BBQ [12], Cougar [14], TiNA [15], Sketch [16], PGA [17]. TAG [3, 13] introduced the in-network aggregation scheme to minimize the amount of transmitted messages. BBQ [12] proposed using the statistical modeling techniques to answer various queries. In Cougar [14] approach, when given a user query, a query optimizer generates an efficient query plan for query processing. TiNA[15] exploited the temporal correlation between readings. Sketch [16] generalized the duplicate-insensitive characteristics to answer the aggregate queries such as Count, SUM. PGA [17] exploited range caching [17, 18] to reduce the number of exchanged messages, in which each node caches error filter for its sub-tree. They also introduced an algorithm, based on potential gains, to adaptively adjust the error thresholds.

Other than the approaches designed for answering aggregate queries, some data collection techniques [19, 20, 21] can be used to answer aggregate queries as well. However the focuses of those approaches are efficient data collection, not only on answering aggregate queries.

With respect to the holistic queries that we focus on in this paper, there are not many related approaches. To generalize, there are three mainstream techniques for answering the holistic queries, which are centralized approaches, sampling approaches, and histogram-based approaches. TAG [3] presents a centralized approach for holistic in which sensor values are transmitted to the root where the aggregate result is calculated. Sampling is another type of technique for answering the holistic queries. SIA [4] proposes a framework for secure information aggregation and discusses the sampling-based computation of Median query. Histogram is a common structure for storing data distribution information in answering holistic queries. There are many types of histograms, such as equallength histogram, equal-depth histogram and Waveletbased histograms [10]. All histograms share the common point that they group values into buckets [11], so these methods are also regarded as buckets-based approaches. Hellerstein [9] introduces a wavelet-based aggregation scheme which can also produce results of increasing resolution over time. Q-digest [1] is another kind of buckets-based approach which allows overlapping buckets. Besides, Q-digest guarantees an error of O(log(σ)/m) with message size of m. Greenwald et al. [5] design an online algorithm for computing ε-approximate quantile summary for large data stream with a worst-case space requirement of O(log(εN)/ε). Cormode et al. [2] propose distributedtracking schemes for finding accurate quantiles with error guarantees. They assume each remote site maintains a local data stream. Greenwald et al. [8] present algorithms which can provide ε-approximate answers for quantile with message size O(log2 (n)/ε). Some other methods such as Manku etc. [6] presents hybrid approximate algorithms for computing frequency counts over data streams. ASP [7] presents tree-based space-efficient scheme for calculating the frequent items and quantile.

Other than queries over sensor networks, there are many other interesting works in the network literature, such as energy efficient coverage problem in sensor networks [22], moving object tracking [23], and etc.

# 3. Exact query scheme

We assume that a Median query is executed upon a dataset S within the range [1, σ] and the total number of sensors in the network is n. The range here refers to integer values, the real value range can be converted into integer range by multiple a large enough integer. The output of Q is a data element d ∈[1, σ] such that the number of sensor values which are smaller (or larger) than d is n/2. A straightforward approach to get answers for Q is to retrieve all the values from sensors, however, as mentioned before, this is not energy efficient. Thus, in this paper, we propose a histogrambased approach to get exact answers for continuous queries. Specifically, we use the histogram summary structure to store the value distribution of the network. Each bucket in the histogram counts the number of values in a certain range. The exact query algorithm works when data values in sensor network are relatively stable over time. Since the sensor values are relatively stable and highly correlated among different rounds, the Median result can be searched in multiple rounds. In each round, we adjust the ranges of buckets, that is, subdividing the range where the median is located and assigning the subdivided small ranges to all intermediate buckets in the next round. After a few rounds, the ranges of all intermediate buckets will be of length 1, thus, we can get the exact median result continuously. When the median value runs out the ranges handled by these intermediate buckets, we need to adjust the range again. The range refining is conducted at the sink and the schema is flooded to the network. The detailed steps of this approach are discussed in following sections.

# 3.1. Data structure

In the exact query approach, we apply the bucket histogram, which is referred as F(lexible)-Bucket, to get the exact answer for the query. The F-Bucket schema is assigned at the sink and then flooded to the whole network. One F-Bucket F consists of a list of triples which are denoted as buckets, $F = \{ B _ { 0 } , B _ { I } , . . . ,$ $B _ { i } , . . . B _ { m - l } \}$ and $B _ { i } = ( m i n ,$ , max, count), where integer m denotes the maximum number of the buckets determined by the message size, each bucket $B _ { i }$ has a range [Bi.min, Bi.max] defined by the min and max, and $B _ { i } .$ .count counts the number sensor values in this range. Note that the ranges associated to bucket $B _ { i }$ and $B _ { i + I }$ are consecutive, thus, $B _ { i \cdot }$ .max+ $. I = B _ { i + I } . m i n$ . F-Bucket is flexible because the ranges corresponding to buckets are not fixed and can be refined periodically according to recent query results. An example of the F-Bucket with 6 buckets is illustrated in Figure 1.

![](images/083494185be61305250f0c7f8abf26b3e14d20e249670806d24929070a1d9249.jpg)



Figure 1. An example of F-Bucket

In order to reduce the transmitted bytes, messages do not carry full F-Buckets but only buckets that are not empty (count > 0). We apply the in-network aggregation at intermediate nodes to merge all the partial F-Buckets received from children.

# 3.2. Query processing

Although our query algorithm can work over arbitrary topology structures, to simplify the discussion we assume a tree-like routing topology [3, 13]. All sensor nodes in the network are organized into a spanning tree rooted by a special node called sink as illustrated in Figure 2.

![](images/36581262ad788251bc6bfe18c378c93bb1277f578d5d228e4ee8f2d8615e68ab.jpg)



Figure 2. Network topology

Take the Median query as an example, each round the leaf node builds an F-Bucket of only one bucket with its own value and transmits to its parent. An intermediate node receives F-Buckets from children and merges them with its own F-Bucket to an integrated one. The intermediate node then sends the new F-Bucket to its parent as well. In the end of the round, the sink merges all the received F-Buckets to a final one and calculates the median result. During a continuous Median query, the above process repeats round by round. The range refining algorithms finds the range where the median value is located and subdivides it to all intermediate buckets. After a few rounds all the intermediate buckets handle a range of length 1 and the rest ranges are handled by two boundary buckets. The median value is located in the range of intermediate buckets and exact median results can be calculated continuously. When the median runs out the range of intermediate buckets, the range refining algorithm will adjust the ranges of buckets.

Algorithm 1 Intermediate node processing   
1: Generate value v; //start processing
2: Build F-Bucket Fv;
3: Receive F-Buckets from children;
4: for all Fi in received F-Bucket list do
5: Fv = Merge (Fv, Fi);
6: end for;
7: Transmit Fv; //transmit message to parent;

3.2.1. Intermediate node operation The processing of an intermediate node is illustrated in algorithm 1. Basically, the intermediate node collects the F-Buckets, merges them and sends the merged one to upper level. The merging of two F-Buckets is simple because the range of each bucket is fixed, we only need to merge their count of corresponding buckets that are associated to the same range. As shown in Figure 3, $F _ { I }$ and $F _ { 2 }$ have 3 and 4 nonempty (count > 0) buckets respectively, in the merged F-Buckets $F ,$ there are 5 buckets and the counts in corresponding buckets of $F _ { I } ,$ , $F _ { 2 }$ are summed. For example, the buckets in $F _ { I }$ and $F _ { 2 }$ with same range [11, 20] have count of 6 and 1 respectively, and then the count of bucket [11, 20] in F is 7 (6+1).

3.2.2. Result calculation With the received F-Bucket in sink, we can answer a Median query. Algorithm 2 illustrates the steps to compute a Median result. According to Algorithm 2, the return value is a range that covers the query result. If the returned range is of length 1, we can get the exact median.

![](images/53c69539195400f33d86babef56c7c2869ae69dbb3f473561f78a1b2b01ab3d8.jpg)



Figure 3. Merge two F-Buckets

Algorithm 2 Calculating\_Median (F, n)   
1: rank = n/2;
2: sum = 0;
3: i = 0;
4: while sum < rank do
5:    sum = sum + F.bucket[i].count;
6:    i++;
7: end while
8: Return range of F.bucket[i];

# 3.3. Range refining

At the very beginning, all buckets are equal length; during the continuous query, the range assignment will be adjusted to fit the value distribution better. The refining process assigns more buckets to the range where the queried median is located and adjust this assignment while the value distribution changes. As the historical data accumulated at the sink, we have an anterior prediction about the real median value. Based on this prediction, we can adjust the range granularity associated to each bucket. The refining algorithm will assign a fine granularity monitoring to the range which covers the median value with high probability and a coarse granularity monitoring to the rest. Most buckets are assigned to the candidate range (called focused window) and each bucket handles a range of length 1 after a few rounds.

With the refining algorithms, we can guarantee the exact result for arbitrary query. The basic idea of a refining algorithm is multi-pass search. The continuous query rounds are divided to 3 different types. Considering median, in initial rounds we try to find a narrow range contains the median value. This is achieved by subdividing the current range where median is located. At last, most of buckets are assigned to monitor this range and each of them is corresponding to a value interval of length 1. Then in the following continuous rounds, querying will focus on this range (focused window) and extract the accurate median value. When the median value runs out this range due to value changing, one or more refresh rounds will rediscover the focused window.

1) Initial rounds: At the vary beginning, Initial rounds are applied to detect the focused window, as shown in Figure 4, assuming that the sensor values are among S = [0, 174] and there are at most 7 buckets in one F-Bucket.

![](images/cd6e08a13068d694925fa16e8776d4f4252177ad1ece0e0b24c53372ff3bb823.jpg)



Figure 4. Range refining in initial rounds

In the first round, the monitoring range S is divided in to 7 equal parts and each bucket counts the number of values that lie in its range. After this round, as shown in Figure 4 the median value is located in bucket A. The range associated to A ([50, 74]) is subdivided in the second round and handle by bucket A1 to $A _ { 5 } .$ . The rest ranges are combined and handled by B ([0, 49]) and C ([75, 174]). After the second round, the range covering median shrinks to [60, 64] (A3) which is narrow enough and regarded as the focused window. The process of finding the focused window may continue for several rounds and it will end in at most log(σ) rounds. In the following continuous rounds, bucket $A _ { I }$ to $A _ { 5 }$ are assigned to the focused window and each bucket handles a range of length 1.

2) Continuous rounds: Each Continuous round can provide an accurate answer for the median query till the median value runs out the focused window. Process of each node in continuous rounds is similar to that in initial rounds.   
3) Refresh rounds: When the median value runs out the focused window due to value changing, the refresh round will relocate the focused window to adapt the new data distribution. We propose two algorithms for refining the range assignment, Slip refining and Hierarchical refining.

Slip refining: This algorithm slips the focused window to the same direction which the median value moved towards. The slipping distance is equal to the length of focused window.

![](images/f19b8ee136825c69edc0458d0d5873fd3b02100609684b392d46c21a401bf1fc.jpg)



Figure 5. Slip refining algorithm

As shown in Figure 5, if the median has run into the range of bucket C ([65, 174]), then in the refresh round the ranges handled by B and $A _ { I }$ to $A _ { 6 }$ are combined to a new range [0, 64] which is assigned to B and the focused window slips to [65, 69] and is assigned to $A _ { I }$ to $A _ { 6 }$ again. Bucket C charges the rest range. This process will continue till the focused window catches up the median again.

Hierarchical refining: The second refining algorithm is Hierarchical refining. In the Slip refining, we guess that the median lies in the range adjacent to current focused window and slip the window to the adjacent range. However, if the median changes fast, we need multiple rounds to catch up with it. In the Hierarchical refining, we first use an additional round to relocate the rough range covering median. Then slip the focused window to it. A running example is illustrated in Figure 6.

![](images/7463e775770b5e6ff4e2b5c0b85b498cabf60d7f695225e3437f413350916d90.jpg)



Figure 6. Hierarchical refining algorithm

In this example, the median value runs out the current focused window [60, 64] to range [65, 174] handled by bucket C. The range of bucket C is subdivided and assigned to buckets A to C and the current focused window is merged to bucket B. Buckets $\mathbf { A } _ { 1 }$ to $\mathbf { A } _ { 5 }$ each handles a range with equal length to the prior focused window which is 5 in this example. Since we assume that the data changing is slow, median value will be located in $A _ { I }$ to $A _ { \mathfrak { s } }$ with high probability. As shown in Figure $^ { 6 , }$ the focused window is relocated to range [65, 69] and new continuous rounds begin.

# 4. Wavelet-like approximate query scheme

When sensor values change quickly, the range refining process will be called frequently which leads to very high communication cost. In fact, under such a situation, the temporal correlation over time is weak and it is not appropriate to use F-Bucket any more. Thus, we propose a wavelet-like approximate algorithm to get approximate answers to the query. In this algorithm, queries in different rounds are independent, so the data changing over time will not affect the query processing. We still use the histogram summary to store the information. Different from the exact query, each bucket in this structure stores the average of a group of values and buckets are sorted by their values, which is similar to the formulation of Haar wavelet [10]. Intermediate sensors combine data structures from downstream nodes, insert their own values and forward the structure to upper nodes. Finally, at the sink we get an aggregated data structure, with which we can run varying queries. For example, if we want the median value, we can choose the value in the middle position of this list. In the following sections we will show details of this algorithm as well as the error bound in the worst case.

# 4.1. Data structure in approximate query

In the approximate query algorithm, the data structure is different from F-Bucket and we will refer to the approximate structure as AF-Bucket, where each AF-Bucket is represented as: $F ^ { \prime } = \{ [ b _ { 0 } , b _ { I } , . . . , b _ { i } , . . . , b _ { m - I } ] { \} }$ count(F’), loglen(F’)}; $( b _ { i } { < } b _ { i + I } )$ . $F ^ { \prime }$ consists of m sorted values and an integer count which denotes the number of values rolled in to this structure. Variable loglen indicates the number of values rolled in one bucket loglen = log(count/m). In this structure, $b _ { i }$ is the approximate value along with function $r a n k ( b _ { i } ) \ =$ count×(i/m). For example an AF-Bucket $\begin{array} { r l } { F ^ { \prime } } & { { } = } \end{array}$ $\{ [ 3 , 6 , 1 0 , 1 5 ] , 8 , 1 \}$ , count $F \ ' ) = 8$ means there are 8 values in this structure and loglen(F’) = 1 means each bucket represents $2 ^ { 1 } = 2$ values. Value 3 is the average of the 0th and 1th values and 6 is the average of the 2th and 3th values, etc.

# 4.2. Query processing

The query processing in approximate query has no range refining steps. Each round is an independent oneshot query. In each round, the leaf nodes construct new AF-Buckets and insert their values in. Then the AF-Buckets are delivered to their parents. In an intermediate node, the received AF-Buckets are merged together to be an integrated one. This merging process reduces transmissions at the cost of losing some information. Finally, the sink aggregates all received AF-Buckets to an integrated one and calculates the query results. The following subsections shows details of the merging process in the intermediate nodes and the result calculation in the sink.

# 4.2.1. Intermediate node operation

The processing in an intermediate node is illustrated in Algorithm 3.

Algorithm 3 Intermediate node processing   
1: Generate value v; //start processing
2: Receive AF-Buckets $\{F'_{i}\}$ from children;
3: Insert v to $\{F'_{i}\}$ ;
4: while exist $F'_{i} F'_{j}$ in $\{F'_{i}\}$ and $\text{loglen}(F'_{i}) = \text{loglen}(F'_{j})$ do
5: Merge ( $F'_{i}, F'_{j}$ );
6: end while
7: Transmit the merged $\{F'_{i}\}$ ; //transmit to parent;

During the process of inserting the own value v to the AF-Bucket list, two cases have to be dealt with. If there is one AF-Bucket $F ^ { \prime }$ in the list with count less than m, we can insert v to the value list of $F ^ { \prime }$ and resort the list. If all AF-Buckets’ count are no less than m, we construct a new AF-Bucket with only one value v and add it to AF-Bucket list. The merging process of AF-Buckets $\boldsymbol { F } _ { \ a } ^ { , } = \{ [ a _ { 0 } , a _ { 1 } , . . . , a _ { m - 1 } ] .$ , count $F _ { a } ^ { \prime } )$ , loglen( $\left. F _ { a } ^ { \prime } \right\}$ and $F ^ { , } _ { b } { = } \{ [ b _ { 0 } , b _ { 1 } , . . . , b _ { m - 1 } ] ,$ count $( F _ { b } ^ { \prime } )$ , loglen(F’b)} is discussed as follows:

1) If count $( F _ { a } ) =$ count $\mathbf { \nabla } ( F _ { b } ) > m$ (in other words loglen $( F _ { a } ^ { , } ) = l o g l e n ( F _ { b } ^ { , } ) > 0 )$ , we put all values in $F _ { a } ^ { \prime }$ and $F _ { ~ b } ^ { \prime }$ into a double size $( 2 ^ { * } m )$ temp list T and these values are resorted while being inserted to T. Then, the average of every two values in list T is calculated to construct the merged AF-Bucket $\boldsymbol { F } _ { c } ^ { \prime }$ . Finally, double the variable count and have the loglen plus one. This process is shown in Algorithm 4.

Algorithm 4 Merge(F’a, F’b)   
1: indexA = 0;
2: indexB = 0;
3: for i from 0 to $2 \times m - 1$ do

1: indexA = 0;   
2: indexB = 0;   
3: for i from 0 to $2 \times m \cdot 1$ do

4: if indexB >= m or (indexA < m and $F'_{a}[indexA] < F'_{b}[indexB]$ )
5: $T[i] = F'_{a}[indexA]$ ;
6: indexA++;
7: else
8. $T[i] = F'_{b}[indexB]$ ;
9: indexB++;
10: end if
11: end for
12: for j from 0 to m-1 do
13: $F'_{c}[i] = (T[2i] + T[2i + 1])/2$ ;
14: end for
15: $count(F'_{c}) = 2 \times count(F'_{a})$ ;
16: $loglen(F'_{c}) = loglen(F'_{a}) + 1$ ;
17: Return $F'_{c}$ ;

Figure 7 shows an example of the merging of two AF-Buckets. In this example, $F _ { a } ^ { \prime }$ and $F _ { ~ b } ^ { \ast }$ are two input AF-Buckets and $F _ { c } ^ { \prime }$ is the merged AF-Bucket. As described in Algorithm 4, the values in $F _ { a } ^ { \prime }$ and $F _ { ~ b } ^ { \ast }$ are put into the temp list T. The values in T are sorted. As shown in Figure 7, in this example we assume that the sorted list T is $[ a _ { 0 } , b _ { 0 } , a _ { I } , a _ { 2 } , b _ { I } , a _ { 3 } , b _ { 2 } , b _ { 3 } ]$ . Then the average of every pair of values is used to construct a new AF-Bucket $F _ { \mathrm { ~ c ~ } } ^ { \prime }$ c with the count doubled and loglen equals to one plus that in $F _ { a } ^ { \prime } ( F _ { b } ^ { \prime } )$ .

2) If count $( F _ { a } ^ { , } ) \ <$ m and coun $( F _ { b } ^ { \prime } ) ~ < ~ m _ { \mathrm { \scriptscriptstyle ~ \mathscr { D } ~ } }$ , the merging is simpler. Values in $F _ { a } ^ { \prime }$ and $F _ { ~ b } ^ { \ast }$ are put together to a temp array and resorted. Then the first m values are selected to store in $F _ { a } ^ { \prime }$ and the rest values are put to $F _ { b } ^ { \prime } .$ If count $( F _ { a } ^ { \prime } ) +$ count ${ \cal F } _ { b } ^ { \prime } ) \le m ,$ , then $F _ { ~ b } ^ { \prime }$ is empty and can be removed from the AF-Bucket list.

Note that after the merging process, there may be more than one AF-Bucket in the list with different loglen, because only the AF-Buckets with same loglen can be merged. All of them are transmitted to upstream nodes and the number of AF-Buckets is less than log(n/m).

![](images/5c2aa8f0ea243589802b4958c313a9eb7a408a49b868142d2db8525129cf2eac.jpg)



Figure 7. Example of merging two AF-Buckets

# 4.2.2. Result calculation

![](images/64b25409e151c81e8b0da6e720c5814e885e1aad9eb56eb6f44bf63ef7f3c8d5.jpg)



Figure 8. Example of zero-padding

After the sink receives AF-Buckets, it merges them in the same way as discussed above. If there is still more than one AF-Bucket in the list that can not be merged, the zero-padding merging algorithm is applied. If the loglen (count) of AF-Bucket ${ \bar { F } } _ { i } ^ { \prime }$ is smaller than that of $F _ { i + l } ^ { \prime } ,$ we pad zeros to $F _ { i } ^ { \prime }$ till $F _ { i } ^ { \prime }$ and $F _ { i + l } ^ { \prime }$ are equal length. Figure 8 shows an example of double an AF-Bucket by zero-padding. By this way, all the AF-Buckets are merged pair after pair. At last we get an integrated AF-Bucket and calculate the query result with it. For example in the Median query, we just remove the prior zeros in the final value list and use the value in the middle position of the remaining values as the approximation of the real median value in sensor network.

![](images/f2854265003078d090d584b6be8b08425d87a9308d0671cab0ddd017b7d621d5.jpg)



Figure 9(a). Traffic on random data

![](images/4059f1305137a1b7bd7958534410f38f3e3fbbe1802d9d8ce7d441586d97b3aa.jpg)



Figure 9(b). Traffic on correlated data

# 5. Evaluation

In this section, we evaluate our algorithms for Median query in varying conditions. We also compare our algorithm with the LIST and Q-digest [1] approach. LIST is a simple un-aggregated data summarization scheme in which the summary is a list of distinct sensor values and a count for each value. Intermediate nodes receive summaries from its children and then form a list of all distinct values with their counts in the sub-tree. All distinct values and their counts are delivered to sink where quantile or other queries are answered. With this scheme we can derive exact answers for queries at the cost of high transmission traffic. We did not compare with [2] because the approaches developed in [2] mainly focused on distributed stream environment, not specialized for a wireless sensor network. The simulated sensors are organized on a balanced routing tree. Each parent nodes have 4 children. So the total number of sensors in this network can be 5, 21, 85, 341, 1365, 5461, etc. The monitoring data range is [1, 28 ]. Here we assume the wireless communication is ideal and there is no link loss. Thus we focus on the query algorithms. In each experiment, we run the continuous median queries for 500 rounds and calculate the average performance. Here we use the metric number of transmissions to evaluate the traffic cost of all these approaches which is defined as the total size of transmitted data packets in one round.

# 5.1. Experiment one

Firstly, we consider the exact query algorithm. Since LIST and our Flexible Buckets algorithms both can provide the exact answer for median query, we just evaluate their traffic cost. Each round, the sensor values has 25% probability to plus one and 25% probability to minus one. They have 50% probability to stay the same as prior round. The number of sensor nodes in the network is varying from 21 to 5461. The results are illustrated in Figure 9 where ‘Slip’ and ‘Hierarchical’ denote two different refining algorithms. The two approaches are tested on two different initial data distributions. Random data denotes that the sensor values are randomly generated in the beginning and Correlated data means the sensor values are correlated to each other. From Figures 9(a) and (b), we can find that our exact query algorithm transmits much less bytes than the LIST scheme. Moreover, the effects of two refining algorithms are similar on both data sets. This is because the data changing speed is slow, however, when data changes quickly, the performance of two refining algorithms will be different, which will be shown in the third experiment.

# 5.2. Experiment two

Secondly, we evaluate the performance of the approximate algorithm (denoted as Wavelet-like). Precision and traffic cost are considered in our experiments. For Median query, the relative percentage error is defined as $e r r = ( r e a l R a n k ( c ) - n / 2 ) / n$ In the first test, the number of values in an AF-Bucket structure varies from 6 to 32. The network size is fixed on 1365 sensor nodes. This test is conducted over two types of data sources, random date and correlated data.

![](images/35dfae593b72e279e4c686cd44777461a8e3d24589a9e0c0569df0a8ced237c4.jpg)



Figure 10. Percentage error   
![](images/aa5242ae96cda7cbd44e3e872c49257de35bb0fcc47d0f6c02c79925b1cb3459.jpg)



Figure 12. Traffic on varying networks

The results are reported in Figure 10. In Figure 10, the percentage error of median query decreases from 7% to less than 2% as the AF-Bucket size increasing from 6 to 32. In other words, the performance will be better with more traffic. When the AF-Bucket size is 12, the accuracy of median query is already higher than 97% on both random and correlated data. Then the next experiment is used to compare the traffic cost of our approximate approach (Wavelet-like) and LIST. The initial sensor values are generated randomly. The AF-Bucket size is set to 12 with which the percentage error is lower than 3% as illustrated in Figure 10. Figure 11 shows the maximum message size on different network size. Compared with the LIST approach, the maximum message size of our scheme is much less. Thus, the traffic load of sensor nodes in our approach is more balanced. Q-digest [1] is an important approximate approach on holistic queries. We compare our approximate algorithm with Q-digest.

![](images/0abd728b38fd90b7609b23f261a5a5567aea1b70f8816ae3e1c04296f0435cdb.jpg)



Figure 11. Maximum message size

![](images/a96fc1f6789e90b0035af01ea4f60796c220edea8486d036082124504f7f3a07.jpg)



Figure 13. Traffic on changing data

In this test, the percentage errors of both algorithms are set around 2% with appropriate parameter configuration. Figure 12 reports the transmission cost of the two algorithms, where our Wavelet-like approximate algorithm achieves the same precision with much less communication cost.

# 5.3. Experiment three

In this experiment, we compare the traffic cost of our two algorithms. In this simulation we assume that the data changes to the same direction (worst case for exact query algorithm) and each node has 50% probability to change its value and 50% probability to remain the same. The data changing rate denotes the maximum value change of sensors in one round. For example when the changing rate is 10 per round, then each sensor value has 50% probability to change within [1, 10]. During the experiment, the data changing rate is varying from 5 to 30 per round.

The performances of exact query and approximate algorithms are shown in Figure 13. When the data changing rate is less than 10 per round, the exact query algorithms Slip and Hierarchical provide exact query answers with less communication cost. As the changing rate increasing, the range refining becomes more and more frequently which significantly increases the communication cost of the exact algorithms. When the changing rate is above 15 per round, the approximate algorithm performs much better than the above two methods. According to Figure 13, the Slip refining algorithm performs better than Hierarchical refining one. This is because that the Hierarchical refining needs an additional relocating round.

# 6. Conclusions

In this paper, we tackle one type of popular queries, continuous holistic query, over sensor network. Compared to the counterpart of this type of query, nonholistic query, not much work has been done. However, holistic query is indeed important for many sensor network applications to collect statistical data. To avoid sending all the sensing data back to the sink, we propose two approaches to monitor continuous holistic queries, an exact one, Flexible Bucket (F-Bucket), to answer queries accurately and a wavelet-like approximate one to obtain the results with small error. The exact algorithm is applied to get exact answers when the data changing rate is low. When the data changing rate becomes high, the exact scheme will be inefficient and we use the approximation algorithm. Experimental results show that our approach can achieve the similar accuracy but with much less traffic cost compared to the other methods.

# 7. Acknowledgements

This work is supported in part by the National Basic Research Program of China (973 Program) under grant No. 2006CB303000, the Hong Kong RGC grant HKUST6169/07E, NSFC Key Project grant No. 60533110 and NSFC Key Project grant No. 60736013.

# References

[1] N. Shrivastava, C. Buragohain, D. Agrawal and S. Suri, “Medians and Beyond: New Aggregation Techniques for Sensor Networks,” in Proceedings of ACM SenSys, 2004.   
[2] G. Cormode, M. Garofalakis, S. Muthukrishnan and R. Rastogi, “Holistic Aggregates in a Networked World:

Distributed Tracking of Approximate Quantiles,” in Proceedings of SIGMOD, 2005.   
[3] S. Madden, M.J. Franklin, J. Hellerstein and W. Hong, “TAG: a Tiny AGgregation Service for Ad-Hoc Sensor Networks,” in Proceedings of OSDI, 2002.   
[4] B. Przydatek, D. Song and A. Perrig, “SIA: Secure Information Aggregation in Sensor Networks,” in Proceedings of SenSys, 2003.   
[5] M. B. Greenwald and S. Khanna, “Space-Efficient Online Computation of Quantile Summaries,” in Proceedings of SIGMOD, 2001.   
[6] G. Manku and R. Motwani, “Approximate Frequency Counts over Data Streams,” in Proceedings of VLDB, 2002.   
[7] J. Hershberger, N. Shrivastava, S. Suri and C. D. Toth, “Adaptive Spatial Partitioning for Multidimensional Data Streams,” in Proceedings of ISAAC, 2004.   
[8] M. B. Greenwald and S. Khanna, “Power-Conserving Computation of Order-Statistics over Sensor Networks,” in Proceedings of ACM PODS, 2004.   
[9] J. M. Hellerstein, W. Hong, S. Madden and K. Stanek, “Beyond Average : Toward Sophisticated Sensing with Queries,” in Proceedings of IPSN, 2003.   
[10] Y. Matias, J. S. Vitter and M. Wang, “Wavelet-Based Histograms for Selectivity Estimation,” in Proceedings of SIGMOD, 1998.   
[11] J. Gray, A. Bosworth, A. Layman and H. Pirahesh, “Data Cube: A Relational Aggregation Operator Generalizing Group-by, Cross-tab, and Sub-totals,” in Proceedings of ICDE, 1996.   
[12] A Deshpande, C. Guestrin, S. Madden, J. M. Hellerstein and W. Hong, “Model-Driven Data Acquisition in Sensor Networks,” in Proceedings of VLDB, 2004.   
[13] S. Madden, R. Szewczyk, M. J. Franklin and D. Culler, “Supporting Aggregate Queries Over Ad-Hoc Wireless Sensor Networks,” in Proceedings of WMCSA, 2002.   
[14] Y. Yao and J. Gehrke, “The Cougar Approach to In-Network Query Processing in Sensor networks,” in Proceedings of SIGMOD, 2002.   
[15] M. A. Sharaf, J. Beaver, A. Labrinidis and P. K. Chrysanthis, “TiNA: A Scheme for Temporal Coherency-Aware In-Network Aggregation,” in Proceedings of MobiDe, 2003.   
[16] J. Considine, F. Li, G. Kollios and J. Byers, “Approximate Aggregation Techniques for Sensor Databases,” in Proceedings of ICDE, 2004.   
[17] A. Deligannakis, Y. Kotidis and Y. Roussopoulos, “Hierarchical In-Network Data Aggregation with Quality Guarantees,” in Proceedings of EDBT, 2004.   
[18] C. Olston, B. T. Loo and J. Widom, “Adaptive Precision Setting for Cached Approximate Values,” in Proceedings of SIGMOD, 2001.   
[19] Y. Kotidis, “Snapshot Queries: Towards Data-Centric Sensor Networks,” in Proceedings of ICDE, 2005.   
[20] D. Chu, A. Deshpande, J. M. Hellerstein and W. Hong, “Approximate Data Collection in Sensor Networks using Probabilistic Models,” in Proceedings of ICDE, 2006.   
[21] W. Choi, S. K. Das, “A Novel Framework for Energy-Conserving Data Gathering in Wireless Sensor Networks,” in Proceedings of INFOCOM, 2005.

[22] M. Cardei, J. Wu, “Energy-efficient Coverage Problems in Wireless Ad-Hoc Sensor Networks,” Computer Communications 29(4), 2006.

[23] L. Chih-Yu, P. Wen-Chih and T. Yu-Chee, “Efficient In-Network Moving Object Tracking in Wireless Sensor Networks,” IEEE Trans. on Mobile Computing, vol. 5, pp. 1044 - 1056, 2006.