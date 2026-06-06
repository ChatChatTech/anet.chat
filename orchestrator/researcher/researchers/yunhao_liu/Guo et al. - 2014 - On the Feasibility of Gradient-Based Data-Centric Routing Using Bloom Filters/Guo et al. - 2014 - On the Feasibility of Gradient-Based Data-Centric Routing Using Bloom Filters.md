# On the Feasibility of Gradient-Based Data-Centric Routing Using Bloom Filters

Deke Guo, Member, IEEE, Yuan He, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Gradient-based routing using Bloom filters is an effective mechanism to enable data-centric queries in multihop networks. A node compressively describes its data items as a Bloom filter, which is then diffused away to the other nodes with information decay. The Bloom filters form an information potential that eventually navigates queries to the source node by ascending the potential field. The existing designs of Bloom filters, however, have critical limitations with respect to the feasibility of gradient-based routing. The compressed routing entries appear to be noisy. Noise in unrelated routing entries is very likely to equal to even outweigh information in right routing entries, thus blinding a query to its desired destination. This work addresses the root cause of the mismatch between the ideal and the practical performance of gradient-based routing using Bloom filters. We first investigate the impact of decaying model on the effectiveness of routing entries, and then evaluate the negative impact of noise on routing decisions. Based on such analytical results, we derive the necessary and sufficient condition of feasible gradient-based routing using Bloom filters. Accordingly, we propose a receiver-oriented design of Bloom filters, called Wader, which satisfies the necessary and sufficient condition. The evaluation results demonstrate that Wader guarantees the correctness and efficiency of gradient-based routing with high probability.

# 1 INTRODUCTION

NFORMATION-GUIDED routing has widely studied as a Iscalable approach for settings with intensive load of data-centric query processing, compared to those stateless routing ones, such as flooding and random walk. Bloom filter (bf) [1] is deemed as a suitable tool to realize the information-guided data-centric routing in overlay networks [2], [3], wireless sensor networks [4], [5], and ad hoc networks [6], [7], [8].

The data-centric routing means that any query about data with specific attribute values can be forwarded to those unknown sources in the network. The common idea among such proposals is that each node uses a Bloom filter to describe the membership information of its data items, i.e., whether an item is stored at the node or not. Every node then broadcasts its Bloom filter to nodes within its propagation range, for example, h hops. Each link, associated with all the received Bloom filters through it, is maintained as a routing entry. If a node needs to route a query to a destination residing within h hops away, it forwards the query over the link, which has at least one associated Bloom filter to satisfy the query. Each node, however, needs large space to store its routing entries each consists of lots of Bloom filters and hence incurs long delay to scan each routing entry for a routing decision. Such problems become

severe when the average node degree gets higher and the propagation range of Bloom filters increases.

Kumar et al. improve the previous mechanisms by proposing a gradient-based routing mechanism using Bloom filters [9]. The basic idea is to exponentially decay the information in each Bloom filter while propagating it within the given range. Meanwhile, in a routing entry, a link is associated with the union of all received Bloom filters through it. Note that each routing entry does not contain the complete membership information of any item. Hence, a query is sent via the link whose associated routing entry has the maximum amount of information of the queried item. Such a mechanism significantly saves storage space and shortens the delay of answering a query. Acer et al. present the weak state routing [8] for large and dynamic networks that is similar to that proposed in [9].

The nature of gradient-based routing mechanism is that each node as a source creates an information gradient in a potential field. Hints about all data on a source are stored in routing entries of some intermediate nodes, and can be utilized to guide queries to the source. Thus, the information gradients enable efficient decisions of routing by ascending the potential field. Ideally, any query will be forwarded to its desired destination once it enters the propagation region of the source. In practice, however, given a query, we find that noise, formalized in Definition 3, in unrelated routing entries is very likely equal to even outweigh information of the queried item in right routing entries. Thus, gradient-based routing is blinded to the right routing decisions and forwards the queries in a floodinglike manner, as demonstrated in Section 5.5.

In this paper, we address the root cause of the mismatch between the ideal and the practical performance of the gradient-based routing mechanism, and explore approaches to guarantee the routing feasibility and efficiency. This basically involves the following two criteria. First, once a query enters the potential field of a desired destination, the amount of information in right routing entries on the intermediate nodes should keep increasing as the query is forwarded toward the destination. This criterion ensures that each node holds an information gradient in a certain potential field. Second, it should be guaranteed with high probability that noise in unrelated routing entries does not exceed the information strength of the queried item in right routing entries. That is, each node should appropriately suppress the strength of noise at its outgoing links so that it can clearly distinguish right outgoing links from other interfering ones. In this way, a query can be navigated by ascending the potential field along a single path. Bearing these points in mind, we propose the design of receiveroriented decaying Bloom filters for gradient-based routing. Our contributions are summarized as follows:

1. To the best of our knowledge, we are the first to disclose the fact that the existing gradient-based routing mechanisms deteriorate to a flooding-like mechanism and even fail to route queries to the desired destinations. We then derive two criteria to ensure the feasibility of gradient-based routing.   
2. We analyze the strength of useful information in the right routing entry and that of noise in unrelated routing entries. The results show that the existing gradient-based routing mechanisms satisfy the first design criterion under an appropriate constraint, while having critical limitations to meet the second criterion.   
3. We accordingly derive the necessary and sufficient condition of the second design criterion, which guarantees the feasibility of gradient-based multihop routing. Thus, we propose a novel design of Bloom filters for the existing gradient-based routing mechanisms, called Wader. Our simulations demonstrate that Wader guarantees the routing feasibility with high probability.   
4. Although the analytical results presented in this paper first assume the network is regular, the basic idea and methodologies can be applied to more general networks after minimal modifications, as discussed in Section 4.4.

The rest of this paper is organized as follows: Section 2 summarizes some related work. Section 3 analyzes the effect of decaying models in the gradient-based routing. Moreover, we examine the strength of useful information in right routing entries and that of noise in those unrelated routing entries. In Section 4, we derive the necessary and sufficient condition that ensures a feasible gradient-based routing mechanism using Bloom filters, and then propose the design of Wader. Section 5 presents the performance evaluation results. We conclude this work in Section 6.

# 2 RELATED WORK

X. Li et al. propose a similar routing scheme [5], [10] with a different decaying model of Bloom filters. A Bloom filter is propagated without any loss within the first given hops from the source, while decays exponentially or linearly outside the given hops from the source.

Gradient-based routing has been widely studied as a scalable approach for settings with a high query frequency in wireless sensor networks where sensor nodes push their data toward the sink [11], [12]. The gradient can take different forms such as the hop count, energy consumption, or physical distance. The motivation of gradient-based routing is to identify the neighboring nodes through which a destined sink is reached by ascending the potential field.

In the simplest scenario, all traffic is sent to a single sink node. In this case, a single gradient rooted at the sink node is built and maintained in the network. The authors of [13] propose the directed diffusion protocol. In this protocol, the sink node advertises its interest to all other nodes and nodes matching the interest push data to the sink. The gradient is a reply link to a neighbor from which the interest was received. The authors propose a variant of directed diffusion in the literature [14]. Each node is associated with a height that is the minimum distance in terms of the number of hops from the sink. The difference between a node’s height and the one of its neighbor is considered as the gradient on that link. Similarly, the gradient-based routing [11], [15] also sets up a hop-count-based gradient during a setup phase.

The insight behinds the above protocols is to construct a gradient field for each query. They, however, are not suitable for data-centric routing where each node may issue an arbitrary query for collecting data from the network. Actually, constructing and maintaining a gradient field for each query will incur huge network traffic. Additionally, it is not practical for each node to keep gradient fields rooted at all query sources due to its limited resources. In contrast, the gradient-based routing using Bloom filters forms a gradient filed rooted at each node, i.e., all data at each node are encoded into one gradient field, and is suitable for datacentric routing.

Another scenario is the event-based data collection. In [16], the sensor readings are categorized into a set of highlevel events. For any event detected by a random sensor, a potential field with harmonic functions is built such that the greedy routing with the potential is guaranteed to reach the source. In this way, the sink node will pull data from interest event sources by ascending the potential fields. The approaches in [16], however, are not suitable for datacentric routing where each node holds large number of raw data not only several high-level events. In contrast, gradient-based routing using Bloom filters focuses on this type of network applications.

# 3 QUANTITATIVE ANALYSIS OF GRADIENT-BASED ROUTING USING BLOOM FILTERS

# 3.1 Preliminaries of Bloom Filters

A set X of n items is represented by a Bloom filter using a vector of m bits that are initially set to 0. A Bloom filter uses k independent hash functions $h _ { 1 } , h _ { 2 } , \ldots , h _ { k }$ with a range $\{ 1 , \ldots , m \}$ . When inserting an item x to X, all bits of $B f a d d r e s s ( x )$ (consisted of $h _ { i } ( x )$ for $1 \leq i \leq k )$ will be set to 1. To answer a membership query for any item x, users check whether all bits $h _ { i } ( x )$ are set to 1. If not, x is not a member of X. If yes, we assume that x is a member of $X ,$ although we might be wrong due to a false positive which suggests that the item x is in X even though it is not.

![](images/d7621732234e57f70d03908208ff6abe2978a512eeb9029ce814a86a5f24e1e3.jpg)



Fig. 1. Arrow sizes represent the amount of information about the content hosted at the rightmost node. The noise, depicted as small arrows, is present at those unrelated routing directions [9].

Let $p _ { 0 }$ be the probability that a random bit of a Bloom filter is $0 ,$ and let n be the number of items that have been added to the Bloom filter, then $p _ { 0 } = ( 1 - 1 / m ) ^ { n \times k } \approx e ^ { - }$ nk=m. Now we test membership of an element $x _ { 1 } \notin X .$ . Each of k bits of $B f a d d r e s s ( x _ { 1 } )$ is 1 with a probability as above. The probability of all of k bits being 1, which would cause a false positive, is then

$$
f = (1 - p _ {0}) ^ {k} \approx (1 - e ^ {- k \times n / m}) ^ {k}.
$$

It is minimized when $k = \lfloor ( m / n ) \ln 2 \rfloor$ .

Definition 1. For a set X with n items and its Bloom filter bf, $\theta ( x , b f )$ denotes the amount of information in $b f f o r \ \forall x \in X$ , that is the number of bits being 1 in BfaddressðxÞ. Let $\theta ( b f )$ denote the expectation of the number of bits set to 1 in the bf. It equals to m multiply the probability $p _ { 1 }$ that a random bit in the bf is set to 1. The $p _ { 1 } \ i \stackrel { . } { s } 1 - ( 1 - 1 / m ) ^ { k \times n }$ , and hence

$$
\theta (b f) \approx m \times (1 - e ^ {- k \times n / m}). \tag {1}
$$

# 3.2 Overview of the Gradient-Based Routing Scheme

For the ease of mathematical analysis, we first use a regular graph to model a multihop network and reconsider more general networks in Section 4.4. Although the analytical results presented in this paper assume that the network is regular, the basic idea and methodologies can be applied to more general networks. Let c denote the number of neighbors in a regular network or the average node degree in an irregular network.

The key idea of gradient-based routing scheme is captured in Fig. 1, which also shows the aforementioned two criteria of the gradient-based routing scheme. First, each node uses a local Bloom filter, denoted as $b f ,$ to describe the membership information of its data items. Second, every node exponentially decays its local $b f$ while propagating it within the given propagation range, for example, h hops. It is clear that nodes close to the origin have strong information about the content at the origin node because more bits in the decayed $b f$ are used to represent the information about the direction in which the data are located. The strength of this information decreases with distance until it becomes indistinguishable from noise, due to collisions in hashing. Thus, an information potential from the origin node is established and will eventually navigate queries to the origin node. Third, each link is associated with a routing entry that is the union [1] of all the received Bloom filters through it. Finally, if a node needs to route a query to a destination residing within h hops away, the query is forwarded via the link whose associated routing entry has the maximum amount of information of the queried item.

We enforce each local bf to travel isolated from origin to nodes within its propagation region and is not merged along the way with other filters. This effort is the precondition to conquer the duplicate decayed versions of $b f ,$ which reduces the accuracy of the gradient-based routing. Thus, if a random node receives many decayed versions of the same bf via different neighbors, it should only keep one of the filters, which travels the least number of nodes.

It is easy to derive that each node will cause network traffic of size $\begin{array} { r } { \dot { m ^ { } } \times \sum _ { i = 1 } ^ { h } ( c - 1 ) ^ { i - 1 } } \end{array}$ to enable the gradient-based routing mechanism. Additionally, each node maintains a Bloom filter for each of about c routing entries; hence, each node consumes $O ( m \times c )$ storage space on average. Consider that each node has to combine $\sum _ { i = 1 } ^ { \infty } ( c - 1 ) ^ { i - 1 }$ Bloom filters for generating a routing entry. The computation complexity of such a union operation is $\begin{array} { r } { \mathrm { ~ { ~ O ~ } ~ } ( m \times \sum _ { i = 1 } ^ { h ^ { \star } } ( c - 1 ) ^ { i - 1 } ) } \end{array}$ .

# 3.3 Decaying Models of Bloom Filters

Clearly, the decaying model of Bloom filters is a dominating factor that affects the correctness and efficiency of gradientbased routing mechanisms. In this paper, we focus on the exponential model because the similar results can be achieved under the linear decaying model.

The value of $\theta ( x , b f )$ approximately equals to k for $\forall x \in X$ . There are two models to reduce $\theta ( x , b f )$ by decaying the bf. In the exponential model, if a bit in $B f a d d r e s s ( x )$ is 1, it remains 1 at a constant probability $1 / d$ during each round of decay. In the linear model, number of d random bits that are 1 in $B f a d d r e s s ( x )$ become 0 during each decay. Note that d is a decay factor in both models and is a positive real number.

Definition 2. Let $b f _ { i }$ denote a new Bloom filter resulted from the ith round decay of a bf where $1 \leq i \leq h . \ b f _ { i }$ remains $\theta ( b f _ { i } )$ bits set to 1. If the model is exponential, then

$$
\theta (b f _ {i}) = \left\lceil \frac {\theta (b f _ {i - 1})}{d} \right\rceil . \tag {2}
$$

According to the network model and the basic idea of the gradient-based routing using Bloom filter, a Bloom filter a node produces can be received by $T _ { i } = c ( c - 1 ) ^ { i - 1 }$ nodes in the i round, and a node should also receive $T _ { i }$ Bloom filters in their i round due to the symmetry. Thus, each node A can receive $( c - 1 ) ^ { i - 1 }$ decaying Bloom filters in their i round via any link linkj. The received Bloom filters by node A are recorded as $b f _ { i } ^ { l } .$ , where $1 \leq i \leq h$ and $1 \leq \mathsf { \bar { l } } \leq \left( c - 1 \right) ^ { i - 1 }$ . Thus, the number of decaying Bloom filters a node can receive from the whole system through linkj is denoted as $| l i n k _ { j } | ,$ , and $\begin{array} { r } { | l i n k _ { j } | = \sum _ { i = 1 } ^ { h } \overline { { ( c - 1 ) ^ { i - 1 } } } } \end{array}$ .

As mentioned in [1], the union of homogeneous Bloom filters can be realized by a logical or operation between their bit vectors. Thus, the union of $| l i n k _ { j } |$ decaying Bloom filters results in a joint Bloom filter $b f ( l i n k _ { j } )$ for a link $l i n k _ { j }$ of node A. The $b f ( l i n k _ { j } )$ acts as a probabilistic summary of all items which are reachable from node A along a routing path of at most h hops, and is given by

$$
b f (l i n k _ {j}) = \bigcup_ {i = 1} ^ {h} \bigcup_ {l = 1} ^ {(c - 1) ^ {i - 1}} b f _ {i} ^ {l}. \tag {3}
$$

Lemma 1. The number of bits set to 1 in any $b f ( l i n k _ { j } )$ of each node is given by

$$
\theta (b f (l i n k _ {j})) = m \big (1 - (1 - 1 / m) ^ {\beta (l i n k _ {j})} \big), \tag {4}
$$

where

$$
\beta (l i n k _ {j}) = \sum_ {i = 1} ^ {h} \sum_ {l = 1} ^ {(c - 1) ^ {i - 1}} \theta \big (b f _ {i} ^ {l} \big). \tag {5}
$$

Proof. Recall that $| l i n k _ { j } |$ j decaying Bloom filters received by a node through $l i n k _ { j }$ will be merged to construct $b f _ { i } ( l i n k _ { j } )$ . During the union process, $\beta ( l i n k _ { j } )$ balls are dropped into m bits of $b f ( l i n k _ { j } )$ randomly, i.e., the location of each ball is independently and uniformly chosen from m possibilities. $\beta ( l i n k _ { j } )$ denotes the total number of bits being 1 in those $| l i n k _ { j } |$ decaying Bloom filters. Let $p _ { 0 }$ denote the probability that a random bit in $b f ( l i n k _ { j } )$ is 0 after dropping all $\beta ( l i n k _ { j } )$ balls. Clearly, $p _ { 0 } =$ $\left( 1 - 1 / m \right) ^ { \beta ( l i n k _ { j } ) }$ . Let $p _ { 1 }$ denote the probability that a random bit in $b f ( l i n k _ { j } )$ is set to 1. Thus, $p _ { 1 } = 1 - p _ { 0 }$ . Therefore, the number of bits set to 1 in $b f ( l i n k _ { j } )$ is given by $\theta ( b f ( l i n k _ { j } ) ) = m ( 1 - ( 1 - 1 / m ) ^ { \beta ( l i n k _ { j } ) } )$ Þ. Thus proved. tu

# 3.4 Membership Information in Right Routing Entries

Before examining whether the first criterion can be satisfied, we measure the strength of membership information after propagating each Bloom filter within the given range.

In general, $\theta ( x , b f )$  k where an element x is represented by a bf. For the exponential decaying model, we measure the metric $\theta ( x , b f _ { i } )$ , which denotes the amount of membership information of x in a decaying Bloom filter $b f _ { i }$ . We can draw the following conclusion based on its definition.

Lemma 2. $\theta ( x , b f _ { i } )$ is a discrete random variable, denoted as $U _ { i }$ . Its possible values are integers ranging from 0 to k. The probability mass function of $U _ { i }$ is

$$
P (U _ {i} = a) = \frac {\binom {k} {k - a} \binom {\theta (b f) - k} {\theta (b f) - \theta (b f _ {i}) - k + a}}{\binom {\theta (b f)} {\theta (b f) - \theta (b f _ {i})}}, \tag {6}
$$

where $\theta ( b f _ { i } )$ is given by (2).

Proof. Assume a represents the possible value of $U _ { i } ,$ and is an integer ranging from 0 to k. Let $U _ { i } = a$ means that the amount of bits being 1 in the BfaddressðxÞ is a. After i rounds of decay of bf, the number of $\theta ( b f ) - \theta ( b f _ { i } )$ bits being 1 in $b f$ are reset to 0 in $b f _ { i }$ . The number of possibilities that outcome $b f _ { i }$ is

$$
\binom{\theta (b f)}{\theta (b f) - \theta (b f _ {i})}.
$$

The number of possibilities that just $k - a$ bits in $B f a d d r e s s ( x )$ are reset to 0 during the i rounds of decay is ${ \binom { k } { k - a } } { \binom { \theta ( b f ) - k } { \theta ( b f ) - \theta ( b f _ { i } ) - k + a } }$ . Then, the probability that $\theta ( x ,$ $b f _ { i } ) = a$ is given by (6). Therefore, Lemma 2 holds. tu

![](images/3d3233cc11de8d1a179d46a4b8713d6f14f5a68e2467d49752dc212ee091b273.jpg)



(a)Valid gradient-based routing.

![](images/37cd9fcea9720b5c5a14c84839a32c71800d0f5676346126ad3a44f3eac5f094.jpg)



(b）Invalid gradient-based routing.   
Fig. 2. Illustrative examples of gradient-based routing.

Corollary 1. The expectation of Ui can be calculated by

$$
E [ U _ {i} ] = \sum_ {a = 0} ^ {k} a \times P (U _ {i} = a) = k / d ^ {i}. \tag {7}
$$

We can see that the expectation of $\theta ( x , b f _ { i } )$ under the exponential decaying model decrease with the increasing i. Fig. 2 plots an illustrative example of the propagation of a bf from node A. The color of propagation field becomes light from deep as the decay range increases. This result indicates that the number of membership information of $x \in X$ in bf reduces during the decaying transmission of bf.

Practically, a node receiving $b f _ { i }$ through a link $l i n k _ { j }$ also collects other $| l i n k _ { j } | - 1$ decaying Bloom filters through the same link. As shown in Fig. 2, node E receives a decaying Bloom filer from nodes A, B, and C through the same link $C  E$ . Thus, the metric $\theta ( x , b f _ { i } )$ fails to support a gradientbased routing mechanism because each node uses the union of all received Bloom filters through a link as a correlated routing entry. To address this issue, we propose a metric $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ that denotes the amount of information of x in a routing entry $b f _ { i } ( l i n k _ { j } )$ at the node receiving $b f _ { i }$ through linkj where $1 \leq j \leq c .$ .

Before measuring the metric in Lemma 3, we first define two events, used frequently in the rest of this paper. Given any bit in an empty Bloom filter, an event $E _ { = i } ^ { z }$ means that the bit is set to i after throwing z balls into the Bloom filter. The probability of $E _ { = 0 } ^ { z }$ can be calculated by $P ( E _ { = 0 } ^ { z } ) = ( 1 - 1 / \hat { m ) } ^ { z }$ . The probability of $E _ { = 1 } ^ { z }$ is given by $P ( E _ { = 1 } ^ { z } ) = 1 - P ( E _ { = 0 } ^ { z } )$ .

Lemma 3. The metric $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ is a discrete random variable, denoted as $V _ { i } .$ Its possible values are integers ranging from 0 to k. The probability mass function of $V _ { i }$ is

$$
P (V _ {i} = v) = \sum_ {a = 0} ^ {v} P (U _ {i} = a) \cdot P (W _ {i} = v - a | U _ {i} = a). \tag {8}
$$

Proof. In $b f _ { i } ,$ , let us consider an event $\theta ( x , b f _ { i } ) = a$ that a bits in $B f a d d r e s s ( x )$ are set to 1 while other $k - a$ bits are set to 0, where $0 \leq a \leq k$ . The probability of this event is given by (6). To achieve $\bar { b } f _ { i } ( l i n k _ { j } ) .$ , other $| l i n k _ { j } | - 1$ decaying Bloom filters merge with $b f _ { i }$ based on the union operation of Bloom filters. In other words, the number of $\alpha ( l i n k _ { j } )$ balls are thrown into $b f _ { i }$ randomly, where $\alpha ( l i n \bar { k _ { j } } ) = \beta ( l i n k _ { j } ) - \theta ( b f _ { i } )$ . Let us consider another event that $\theta ( x , b f _ { i } ) = a$ and there exists b bits in Bfaddress which are 0 in $b f _ { i }$ but are hit after throwing $\alpha ( l i n k _ { j } )$ balls into $b f _ { i } ,$ where $0 \leq b \leq k - a .$ . The probability of this event is denoted as $P ( W _ { i } = b | U _ { i } = a )$ , and is

$$
\binom {k - a} {b} P \Big (E _ {= 1} ^ {\alpha (l i n k _ {j})} \Big) ^ {b} \cdot P \Big (E _ {= 0} ^ {\alpha (l i n k _ {j})} \Big) ^ {k - a - b}.
$$

Assume that v represents the possible value of $V _ { i } ,$ and is an integer over ½0; k. An event $V _ { i } = v$ means that the amount of bits set to 1 in $B f a d d r e s s ( x )$ of $b f _ { i } ( l i n k _ { j } )$ is v. The probability of this event is given by (8). Thus proved. tu

# 3.5 Noise on Unrelated Routing Entries

Before examining whether the second criterion can be satisfied, we first give a formal definition about noise and then measure the strength of noise in unrelated routing entries at any node for an arbitrary query.

Definition 3. If a node V does not receive a decaying Bloom filter from the source node of x through link $L , L$ is called a link on V that is unrelated to x. Then, noise on L is defined as the amount of membership information in the corresponding routing entry of $L ,$ , namely the number 1s among the k bits of $B f a d d r e s s ( x )$ in the Bloom filter.

For the gradient-based routing mechanism, a node receiving a query for an item x selects $l i n k _ { j }$ so that $b f _ { i } ( l i n k _ { j } )$ contains the largest amount of membership information of x among all the filters. In other words, the node receiving $b f _ { i }$ through $l i n k _ { j }$ will send the query over $l i n k _ { j }$ if x belongs to a set represented by $b f _ { i }$ . Meanwhile, the noise at other links do not affect the decision of routing and thus can be neglected. It is the second criterion mentioned in Section 1. Before examining whether the second criterion can be satisfied, we have to measure the strength of noise at any unrelated link for any queries.

Given an item x represented by a bf and a node A receiving $b f _ { i }$ through its link $l i \dot { n } k _ { j } ,$ , let $\theta ( x , b f _ { i } ( l i n k _ { i } ^ { ' } ) )$ denote the amount of information of x in a routing entry $b f _ { i } ( l i n k _ { i } ^ { \prime } )$ at another link $l i n k _ { j } ^ { ' }$ . Given any Bloom filter, we use $r _ { 0 }$ and $r _ { 1 }$ to denote the fraction of bits set to zero and one in it, and use them as the probability that any 1 bit is set to 0 and 1, respectively. If node A did not receive a decayed version of bf through the link link0j, $\theta ( x , b f _ { i } ( l i n k _ { j } ^ { ' } ) )$ denotes the strength of noise on the information of x at that unrelated link, and is a discrete random variable, denoted as Y . Its possible value, denoted as $u ,$ is an integer ranging from 0 to k. The probability mass function of $\breve { Y }$ is defined as

$$
P (Y = u) = \binom {k} {u} r _ {1} ^ {u} r _ {0} ^ {k - u}. \tag {9}
$$

We then present the expected value of Y as follows:

Corollary 2. The expectation of $Y$ can be calculated by $\begin{array} { r } { E [ Y ] = \sum _ { u = 0 } ^ { k } u \times P ( Y = u ) } \end{array}$ .

# 3.6 Examinations of the Two Criteria

In this section, we show that the existing gradient-based routing mechanisms satisfy the first criterion under a reasonable constraint, while having critical limitations to meet the second criterion. Such existing mechanisms use the traditional designs of Bloom filters, as discussed in Section 4.3.

According to the first criterion in Section 1, a feasible mechanism of gradient-based routing should ensure that the value of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ increases together with $\theta ( x , b f _ { i } )$ when i decreases. As shown in Fig. 2a, the value of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ 号 should increase along a path $E  C  B  A .$ . Such a criterion essentially determines the feasibility of the gradient-based routing mechanism using Bloom filters. The metric is a function of i and $\alpha ( l i n k _ { j } )$ , but not a monotonic decreasing function of i because $\alpha ( l i n k _ { j } )$ is a discrete random variable with uncertain distribution. Under Lemma 3 and a reasonable constraint on $\beta ( l i n k _ { j } )$ , we may derive Theorem 1 to show that the first criterion of gradient-based routing can be satisfied.

![](images/bad11fac9715540299697a900b40d5089835c05a0689c5d2b235ed9c75e97703.jpg)  
Fig. 3. The expected values of $\theta ( x , b f _ { i } ( l i n k ) ) , \theta ( x , b f _ { i } )$ , and noise, where $n \stackrel { \bullet } { = } 1 0 0 , k = \mathrm { i } 6 , d = 1 . 2$ , and $h = 5 .$ .

Theorem 1. Given an item x represented by a bf, consider two nodes receiving $b f _ { i }$ and $b f _ { i + 1 }$ through linkj and $l i n k _ { j } ^ { ' } ,$ respectively. The expectation of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ decreases as the value of i increases $i f \ \beta ( l i n k _ { j } )$ approximately equals to $\beta ( l i n k _ { j } ^ { ' } )$ and $1 \leq i \leq h .$

Proof. Please refer to the supplementary file, which can be found on the Computer Society Digital Library at http:// doi.ieeecomputersociety.org/10.1109/TPDS.2013.11. tu

We further conduct simulations to evaluate the two criteria, especially the second one, in the following two scenarios. The simulations use the same configuration as that in Section 5.

In the scenario of existing gradient-based routing mechanisms, the configuration of Bloom filter is defined in Section 5.5. We can see from Fig. 3a that the expected value of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ is very close to that of noise and decreases slowly as the decay hop increases. Note that the value of m is derived from Section 3.1 when $b f$ generated at each node incurs a false positive with probability 0.0001. The root cause is presented in Sections 4.3 and 5.5. Consequently, the information potential formed by each Bloom filter is very smooth; hence, it cannot navigate queries by ascending the potential field. Finally, the gradient-based routing is blinded to the right routing decisions and has to forward the queries in a flooding-like manner.

We address the root cause of the above mismatch between the ideal and the practical performance of gradient-based routing by proposing wader, a receiveroriented design of Bloom filters in the next section. In the scenario of wader, Fig. 3b shows that the expected value of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ decreases as the decay hop increases, whereas always significantly outperforms that of noise. Note that the value of m is derived along the way mentioned in Section 4.3 when each routing entry yields a false positive with probability 0.0001. Consequently, the information potential formed by each Bloom filter works well to navigate queries by ascending the potential field. This demonstrates that Wader guarantees the correctness and efficiency of the gradient-based routing. The next section presents the details of Wader.

# 4 FEASIBILITY OF GRADIENT-BASED ROUTING

We first examine the impact of noise on the one-hop routing decision of gradient-based routing mechanism. We then derive the necessary and sufficient condition of the second criterion, which guarantees the feasibility of gradient-based multihop routing. We further propose Wader, a novel design of Bloom filters, to satisfy this condition. We also improve the adaptivity of Wader in regular as well as irregular networks.

# 4.1 Impact of Noise on Routing Decisions

Recall that $V _ { i } = \theta ( x , b f _ { i } ( l i n k _ { j } ) )$ denotes the amount of information of x in the right routing link $l i n k _ { j }$ at node A and its possible value, denoted as v, is an integer ranging from 0 to k. In addition, Y denotes the strength of noise in other unrelated routing links $l i n k _ { j } ^ { \prime }$ at node A and its possible value, denoted as $u ,$ is an integer ranging from 0 to k. If a query for an item x is out of the decay range of a destination node, a routing decision is made randomly. As shown in Fig. 2, all routing decisions along a path $K $ $H  G  E$ are made randomly. Otherwise, one of the following routing decisions would be adopted.

1. The value of u is less than v for any unrelated routing link $l i n k _ { j } ^ { ' } ,$ so that node A can distinguish $l i n k _ { j }$ from others and forward the query for x through $l i n k _ { j }$ . This is called an unicast decision. For example, a query toward node A is only forwarded to node C by node $E ,$ as shown in Fig. 2a.   
2. The value of u is equal to v for some unrelated routing links, however, is less than v for others. In this condition, node A cannot distinguish $l i n k _ { j }$ from other links $l i n k _ { j } ^ { ' }$ where $u = v ,$ and hence forwards the query through $l i n k _ { j }$ and such links together. This is called a multicast decision. For example, a query toward to node A is forwarded to node B as well as node D by node $C ,$ as shown in Fig. 2a.   
3. The value of u is larger than v for a link or links except linkj. The strength of noise about x at such links is higher than the strength of information about x at linkj. Therefore, the query will be wrongly forwarded to a link or links except $l i n k _ { j } .$ . This is called an invalid decision. For example, a query toward node A is wrongly forwarded to node D by node C, as shown in Fig. 2b.

We will prove the probability of each aforementioned decision in theory once a query enters the propagation field of a destination. Note that each node has c links averagely and each is associated with a Bloom filter as its routing entry.

Theorem 2. A node forwards a query for an item x according to the unicast decision if it receives $b f _ { i }$ from a destination of the query. The probability of this event is

$$
f _ {\text { unicast }} (V _ {i}) = \sum_ {v = 1} ^ {k} P (V _ {i} = v) \cdot \left(\sum_ {u = 0} ^ {v - 1} P (Y = u)\right) ^ {c - 2}. \tag {10}
$$

Proof. Please refer to the supplementary file, which is available online. tu

Theorem 3. A node forwards a query for an item x according to the multicast decision if it receives bfi from the destination. The probability of this event is

$$
f _ {\text { multicast }} (V _ {i}) = f _ {\text { valid }} (V _ {i}) - f _ {\text { unicast }} (V _ {i}), \tag {11}
$$

where

$$
f _ {\text { valid }} (V _ {i}) = \sum_ {v = 1} ^ {k} P (V _ {i} = v) \cdot \left(\sum_ {u = 0} ^ {v} P (Y = u)\right) ^ {c - 2}. \tag {12}
$$

Proof. Please refer to the supplementary file, which is available online. tu

Theorem 4. A node forwards a query for an item x using the invalid decision if it receives $b f _ { i }$ from the destination. The probability of this event is

$$
f _ {\text { invalid }} (V _ {i}) = 1 - f _ {\text { valid }} (V _ {i}). \tag {13}
$$

Proof. As discussed above, the probability that queries for x are forwarded successfully according to the unicast or multicast decision is given by (12). It is easy to infer that the probability of the event defined in this theorem is given by (13). Thus proved. tu

# 4.2 The Necessary and Sufficient Condition for Gradient-Based Multihop Routing

In the above section, we have discussed the conditions of unicast, multicast, and invalid decisions for one-hop routing decisions. Only one of such decisions will be chosen to deal with a query at each node. Theorems 2, 3, and 4 have proved the probability that each type of decision is chosen. Among the three decisions, the unicast results in a valid and desired gradient-based routing mechanism. In this case, a query for an item x is only biased at an intermediate node which receives a decaying Bloom filter from the destination and is closer to the destination than current node. The benefit of the unicast decision is that it can ensure the correctness of routing whereas does not produce redundant queries (forwarding a query to additional intermediate nodes). The multicast incurs another valid gradient-based routing mechanism at the cost of sending a query to some neighbors which do not receive a decaying Bloom filter from the destination. A gradient-based routing decision is called valid if it ensures an unicast or a multicast decision by preventing an invalid decision at nodes that reside within the decay range of the destination.

Note that the gradient-based routing using Bloom filters is essentially a probabilistic routing. Thus, it is impossible and there is no need to achieve an absolutely valid routing decision for each query. What we need is a valid gradientbased routing decision for any query with high probability. For any query, we can infer from Theorem 3 that the node which received $b f _ { i }$ from the destination of the query can make a valid gradient-based routing decision with probability $f _ { v a l i d } ( V _ { i } ) .$ , and an unicast routing decision with probability $f _ { u n i c a s t } ( V _ { i } )$ .

So far, we consider the valid gradient-based routing decision in the scenario of one hop transmission of queries. In practice, only potential destinations of a very few queries reside one hop away from the sources of queries. Thus, we consider a general scenario in which a query traverses multiple intermediate nodes along a multihop path before it reaches its destination. In this scenario, a query can be sent to its destination with high probability only if each intermediate node achieves a valid routing decision for the query with high probability.

# Definition 4 (Gradient-Based Routing for Multihop

Queries). Given a multihop query, a valid routing can ensure that the query is sent to its destination by a sequence of valid routing decisions made at intermediate nodes once it enters the decay range of its destination. An unicast routing for the query requires all unicast routing decisions at intermediate nodes. An invalid routing for the query means that the routing decision at any intermediate node is invalid. Figs. 2a and 2b plot a valid and an invalid routing for a multihop query, respectively.

Let  denote a lower bound, depending on applications, on the probability that each query is sent to its destination by a valid routing mechanism. According to Theorems 2 and 3, we can infer that the necessary and sufficient condition of a valid gradient-based routing mechanism for a multihop query is

$$
\prod_ {i = 1} ^ {h} f _ {\text { valid }} (V _ {i}) \geq \sigma . \tag {14}
$$

If we further seek all unicast routing decisions, the necessary and sufficient condition should be

$$
\prod_ {i = 1} ^ {h} f _ {\text { unicast }} (V _ {i}) \geq \sigma . \tag {15}
$$

Recall that the expectation value of the metric $\theta ( x$ ; $b f _ { i } ( l i n k _ { j } ) )$ decreases as the value of i increases as shown in Theorem 1. It is easy to infer that

$$
P (V _ {i} = v) > P (V _ {i + 1} = v) \text { for } \theta (x, b f _ {i}) \leq v \leq k, 1 \leq i <   h.
$$

On the other hand, the noise distribution is similar in Bloom filters associated with neighbor links at each node. In summary, $f _ { u n i c a s t } ( V _ { i } ) { > } f _ { u n i c a s t } ( V _ { i + 1 } )$ and $f _ { v a l i d } ( V _ { i } ) { > } f _ { v a l i d } ( V _ { i + 1 } )$ for any query. By now, (14) and (15) become (16) and (17), respectively, if we replace $f _ { u n i c a s t } ( V _ { i } )$ and $f _ { v a l i d } ( V _ { i } )$ with $f _ { u n i c a s t } ( V _ { h } )$ and $f _ { v a l i d } ( V _ { h } )$ , respectively,

$$
\left(f _ {\text { valid }} (V _ {h})\right) ^ {h} \geq \sigma , \tag {16}
$$

$$
\left(f _ {\text { unicast }} (V _ {h})\right) ^ {h} \geq \sigma . \tag {17}
$$

Inequality (16) or (17) acts as the necessary and sufficient condition of a feasible gradient-based multihop routing. Note that such a condition also holds for a single-hop and gradient-based routing. In the remainder of this paper, we will use inequality (16) or (17) to instruct the novel design of Bloom filters to satisfy this condition.

# 4.3 Wader

As mentioned in [1], many efforts have been made to optimize Bloom filters from different aspects. The common idea is to minimize the false positive probability or the size of an individual Bloom filter, which only represents all data at a single node. Such efforts, however, do not address the fact that each node uses the union of all received decaying Bloom filters through a link as a routing entry of that link. Although the fraction of bits set to one in each individual Bloom filter might be low, that in each routing entry becomes high due to the union of many decaying Bloom filters. Thus, given a query for any item at a random node, noise about the item in unrelated routing entries is very likely equal to or even stronger than the useful information in the right routing entries.

The above analytical as well as experimental results in Section 5.5 demonstrate that the existing designs of Bloom filters fail to support the gradient-based routing mechanism. To address this issue, we propose a novel design of Bloom filters for each routing entry, the union of many individual Bloom filters. The main idea, called Wader, is to derive the optimal configuration of each individual Bloom filter under the constraint of inequality (16) or (17), so as to satisfy the second criterion of gradient-based routing.

Besides the well-known metrics of Bloom filters (the number of items $n ,$ the size of Bloom filter $m ,$ and the number of hash functions $k ) ,$ , the decay factor d and decay range h are two additional dependent factors which impose constraints on inequalities (16) and (17).

Based on a given decaying model with parameters d and $h ,$ we first calculate $\theta ( b f )$ and $\theta ( b f _ { i } )$ according to (1) and (2). Note that $\theta ( b f )$ is a function of variables $m , \ n ,$ and $k ,$ whereas $\theta ( b f _ { i } )$ is a function of variables $m , n , k ,$ and d. We estimate the fraction of bits set to one $r _ { 1 }$ in each joint Bloom filter according to (4) and $m ,$ , and finally obtain the distribution of noise strength at each neighbor link based on (9). Note that $r _ { 1 }$ is a function of variables $m , n , k , d ,$ and h. Similarly, according to (8), we can achieve the distribution of information of any item x in a joint Bloom filter associated with a link through which a decaying Bloom filter is received from a destination. We calculate the probability of an unicast and a valid gradient-based routing decision by (10) and (12) which are functions of m, n, k, d, and h. Finally, inequality (16) or (17) is used to restrict the value of $m , n , k , d ,$ and h under a constraint of the lower bound .

The parameters $n , \ d ,$ and h should be assigned with appropriate values with regard to several factors, such as the topological properties, data distribution in the network, and query popularity, and so on. Many efforts have been made to estimate the topological properties, such as the network size [17], network diameter [18], and degree distribution [19], and to investigate the data distribution and query popularity [20]. Thus, it is reasonable to assume that we are given $n , d ,$ and h. In this case, inequalities (16) and (17) merely depend on parameters m and $k ,$ and hence we can optimize the number of hash functions k to maximize $f _ { u n i c a s t } ( V _ { h } )$ and $f _ { v a l i d } ( V _ { h } )$ . Accordingly, inequalities (16) and (17) can be satisfied with m as small as possible. It is well known that a single Bloom filter is optimal when $k = \left( m / n \right)$ ln 2. Such an optimal result, however, cannot ensure an optimal joint Bloom filter.

After optimizing $f _ { u n i c a s t } ( V _ { h } )$ or $f _ { v a l i d } ( V _ { h } )$ , we can calculate the optimal value of m and k by solving inequalities (16) and (17), respectively. So far, the parameters m, k, d, h, and n are configured. Consequently, these parameters of each individual Bloom filter each node proposes can ensure the fraction of bits set to one in each routing entry is low, and hence the second criterion of gradient-based routing can be satisfied.

# 4.4 Implementation Issues with Wader

According to the design approach in Section 4.3, the parameters $m , k , d , h ,$ and n can be optimized to ensure the second criterion of gradient-based routing in theory. With those parameters, the number of bits set to 1 in any routing entry can be calculated by (4). The following practical issues, however, directly affect the performance of Wader. The distributions of node degree and received BFs through every link are usually nonuniform. Thus, for the majority of links, the number of bits set to 1 in a routing entry usually does not equal to the estimated value $r _ { 1 } \times m$ . To make Wader be adaptive to dynamic network conditions, a practical implementation way is to let each node monitor the number of bits set to 1 in each routing entry. Once the number of bits set to 1 in a routing entry exceeds $r _ { 1 } \times m _ { i }$ , it denies all the Bloom filters received afterward. Such a method makes inequalities (16) and (17) always satisfied, and hence ensures the correctness and efficiency of Wader in practice.

We use a regular graph to model a multihop network for the ease of mathematical analysis and presentation, the theoretical design and practical implementation of Wader can guarantee the correctness and efficiency of the gradientbased routing with high probability. We further reconsider the gradient-based routing in more general networks.

An intuitive way is to revise the analytical results in Section 3 and the theoretical design of Wader in Section 4.3, given the average node degree c and the distribution of node degree. This way, however, is very complex to derive the desired analytical results. The second way is to borrow the theoretical design of Wader for regular networks, whose node degree is appropriated to the average node degree of an irregular network. The evaluation results in Section 5 show that the second way can ensure the feasibility of gradient-based routing with high probability. The root reason is that the practical implementation of Wader is adaptive to dynamic network conditions, and can deal with the mismatch between the topological properties of an irregular network and an appropriate regular network.

# 5 PERFORMANCE EVALUATION

We use PeerSim to implement Wader in a random network using the approach proposed in Section 4.4 to demonstrate that only Wader can guarantee the feasibility of gradientbased routing. PeerSim is a large-scale simulation framework for overlay networks aimed at developing and testing any kind of protocols in a dynamic overlay network. The simulation settings are as follow. PeerSim generates a random overlay network with 10,000 nodes, where the node degree ranges from 3 to 7 and the average node degree is $c = 5 .$ The average number of items hosted by each node is $n = 1 0 0$ .

![](images/52fe9c1ba976b5dc20f9f6fad60b2e0c01647470cd8da5fdcc20bdd3d4115d5c.jpg)



(a) $\theta ( x , b f _ { i } )$ and noise.

![](images/5dde73ed8a56b39a76c9443cba037df5970ba9a26da633d581511bd2e3ec9568.jpg)



(b) $\theta ( x , b f _ { i } ( l i n k ) )$ and noise   
Fig. 4. The probability mass functions of $\theta ( x , b f _ { i } )$ , $\theta ( x , b f _ { i } ( l i n k ) )$ and noise, where m ¼ 60;000, n ¼ 100, k ¼ 16, d ¼ 1:2, and $h = 5$ .

# 5.1 Effect of Decaying on Membership Information

Assume the decay factor is set to be $d = 1 . 2$ and the decay range is set to be $h = 5 ,$ depending on a given application. Then, we can derive that an optimal number of bits for each Bloom filter is $m = 6 0 , 0 0 0$ and the number of hash functions is $k = 1 6$ from the aspect of receiver. Given a $b f$ which represents a set $X ,$ we have analyzed the amount of information of any item $x \in X$ in a decay version of $b f$ in Lemma 2. The possible values of $\theta ( x , b f _ { i } )$ are integers ranging from 0 to $k = 1 6 ,$ . Fig. 4a shows the probability mass function of $\theta ( x , b f _ { i } )$ for $1 \leq i \leq 5$ and noise. The results match well with (6). As we can see from the figure, when the possible value increases, the probabilities of $\theta ( x , b f _ { i } )$ first go up and then go down for $1 \leq i \leq 5$ . On the other hand, the probabilities of $\theta ( x , b f _ { i } )$ for the large possible values decrease as the value of i increases, whereas that for those small possible values increase as the value of i increases. The experimental results exactly conform to the analytical results.

Recall that $\theta ( x , b f _ { i } )$ is not accurate enough to support a gradient-based routing mechanism because each node uses the union of all received Bloom filters through the same link as a routing entry for that link. As shown in Lemma $^ { 3 , }$ we replace $\theta ( x , b f _ { i } )$ with $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ to characterize the amount of information of x in a joint Bloom filter $b f _ { i } ( l i n k _ { j } )$ at the node which receives $b f _ { i }$ through $l i n k _ { j }$ . Fig. 4b shows the probability mass functions of $\theta ( \bar { x } , b f _ { i } ( l i n k _ { j } ) )$ and noise. The simulation results follow a similar trend as the theoretical results given by (8). As we can see from the figure, when the possible value increases, the probabilities of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ first go up and then go down where $1 \leq i \leq 5$ . On the other hand, the probabilities of the $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ for the large possible values decrease as the value of i increases, whereas that for those small possible values increase as the value of i increases.

Fig. 4b also shows that the expectation of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ decreases as the decay hop i increases, and thus the first criterion proposed in Section 1 is satisfied by Wader. In addition, the expectation of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ is larger than that of noise for $1 \leq i \leq h$ . This reveals the reason why a node holding $b f _ { i }$ can forward a query for an item x to a node holding a $b f _ { i - 1 }$ with high probability, and thus satisfy the second criterion proposed in Section 1. On the other hand, the simulation results conform to Theorem 1 in terms of the expectation value of $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ for $1 \leq i \leq h$ .

![](images/ae8cb509a0af1975d2a5d047e219fb8c4856d39d9c90d916d87c754d43af8e00.jpg)



(a) Unicast decision

![](images/49074b6e250b3f06696158efc192a74f6c60933063bb405f0fc6b17523c0ee39.jpg)



(b）Multicast decision

![](images/c8ba64fa6039f91a26a9dc7bdd72be28a52ef79ff4578ac37a781a16de1945cf.jpg)



(c) Valid decision

![](images/514067596848a4fbba266ece010dac64f326c003331a596bc517bf6c0b36bb36.jpg)



(d) Invalid decision   
Fig. 5. The probability of four types of routing decisions, where $m = 6 0 , 0 0 0 , n = 1 0 0 , k = 1 6 , d = 1 . 2 ,$ and $h = 5 .$ .

# 5.2 Performance of Wader

We examine the impact of noise on a gradient-based routing decision when each node adopts an optimal Bloom filter based on Wader. A gradient-based routing decision for a single-hop query can be valid (unicast or multicast) or invalid under the interference of noise in unrelated links once the query enters the decay range of a destination. The probabilities of the aforementioned routing decisions have been proved in Theorems 2, 3, and 4. Fig. 5 shows the probabilities of those routing decisions from aspects of both theory and practice.

We can see that the probability of an unicast routing decision decreases with the increasing of the decay hop, whereas the probability of a multicast routing decision increases with the increasing decay hop. The reason is that the expectation value of metric $\theta ( x , b f _ { i } ( l i n k _ { j } ) )$ decreases as the decay hop increases. Thus, the noise strength is more likely higher than $\theta ( x , b f _ { i } ( l i n k _ { j } ) ) ,$ Þ, and queries might suffer invalid or multicast routing decision. Fig. 5c shows that the probability of a valid routing decision decreases as the decay hop increases. The reason is that the negative effect of decreasing unicast routing decision outperforms the positive effect of increasing multicast routing decision. Fig. 5d shows that the probability of an invalid routing decision increases as the decay hop increases.

It is worth noticing that the probabilities of the unicast and valid decisions for routing a single-hop query are high for $1 \leq i \leq h$ . Thus, a multihop query can reach a destination through a sequence of valid even unicast routing decisions with high probability. As shown in Fig. 5, the curve of practical probability follows the same trend as the curve of the theoretical probability for each type of routing decision. The practical probability, however, is larger than the theoretical value for the unicast and valid routing decisions. In addition, Wader achieves lower probabilities of the multicast and invalid routing decisions than the theoretical values. In summary, the theoretical and practical results demonstrate that Wader guarantees the correctness and efficiency of the gradient-based routing for multihop queries with high probability.

![](images/4cdfc9c5987b3f885723d72615f6d01f781eee26b724f09a897df2166cad0471.jpg)



(a) Redundant queries

![](images/6ab26901a9861380319173e5519643a18c2a388ad62e006344dfb649a5fff140.jpg)



(b） Termination probability  
Fig. 6. Number of redundant queries and the probability that they will be terminated by receivers, where $m = 6 0 , 0 0 0$ , n ¼ 100, k ¼ 16, d ¼ 1:2, and $h = 5 .$ .

# 5.3 Design Effectiveness against Redundant Queries

A node possibly suffers the multicast or invalid decision, and then sends very few redundant queries, to neighbors which deviate from the potential destination. The experimental results will show that such queries can be terminated by receivers with high probability. As shown in Fig. 6a, the average number of redundant queries caused by routing one query increases as the decay hop increases. As shown in Fig. 6b, the termination probability of those redundant queries by receivers decreases as the decay hop increases, but the termination probability still remains at a high level. In summary, the practical results demonstrate that the negative effect of redundant queries can be controlled at a low level. This is helpful to ensure the feasibility and usability of the gradient-based routing.

# 5.4 Effect of Decay Parameters on Wader

Now we examine the effect of the parameters k and d on the probability that each query is sent to its destination through an unicast routing or a valid routing. As shown in Fig. 7a, given a fixed m and $d = 1 . 2 ,$ k is the only dependent factor of all four curves which follow a similar trend. They first ascend as k increases and quickly reach the peak, and then descend as k increases. The reason is that $\theta ( \bar { x } , b f _ { i } ( l i n k ) )$ and the noise strength increase for any x and $1 \leq i \leq h$ as k increases, and $\theta \bar { ( } x , b f _ { i } ( l i n k ) )$ is more likely higher than noise relatively. As discussed in Section 4.3, inequalities (16) and (17) are the benchmarks to optimize the parameters of Bloom filters. Given a lower bound  on the probability of an unicast routing or a valid routing for each query, we can find the optimal value of k under each scenario. Similarly, we can achieve the optimal k under varying value of m, and can finally find the global optimal k and m.

![](images/15cb84530b6d9cb4dc895d08dfd55f51912a4f3340bed02f1edf83dff8e006db.jpg)



(a) Effect of k

![](images/f41a01e7a16fd2ed6438707689045818ef79d2ca19a58b5dc804018e81248e62.jpg)



(b) Effect of d   
Fig. 7. Effect of k and d on the probability of an unicast or a valid routing, where m ¼ 60;000, n ¼ 100, and $h = 5 .$ .

![](images/3e983ff05e0be24a96fdf48dcb9be53e93671e81d154c2a8f753a69e939c3545.jpg)



(a) Valid decision

![](images/2d45df7fd6db7ca6897a6e1f6989f9ef39900361b2976004b193c06ac61a788b.jpg)



(b) Flooding ratio at any node   
Fig. 8. The one-hop routing decision at any node in the case of existing gradient-based routing schemes, where n ¼ 100, k ¼ 16, d ¼ 1:2, and $\bar { h } = 5$ .

As shown in Fig. 7b, given a fixed m and k ¼ 16, the probability of an unicast routing for any query decreases as the decay factor d increases in theory, and reaches almost zero after the decay factor exceeds a threshold. The reason is that $\theta ( x , b f _ { i } ( l i n k ) )$ and the noise strength decrease as the decay factor increases for $\forall x \in X$ and $1 \leq i \leq h ,$ and the noise strength is more likely higher than $\theta ( x , b f _ { i } ( l i n k ) )$ Þ. We can also see that the probability of the valid routing first decreases, and then increases as the decay factor increases. It is worth noticing that a small decay factor should be adopted to ensure the unicast routing with high probability, although a large decay factor can always guarantee the valid routing with high probability. For a large decay factor, we have to enlarge the value of k to satisfy the same lower bound , which results in unnecessarily higher computation cost.

# 5.5 Comparisons

In this section, we conduct simulations to evaluate the onehop routing decision of the existing gradient-based routing schemes, for example, HR-SDBF [5] and EDBF [9]. In our examinations, n ¼ 100, d ¼ 1:2, and $h = 5 ,$ . Recall that f denotes an upper bound on the false positive probability of the local Bloom filter at each node. Given f and n, we can optimize m and k with $m = \lceil n \times \log ( f ) / \log ( 0 . 6 1 8 5 ) \rceil$ and $\bar { k } = \lceil ( m / n ) \ln 2 \rceil$ [1]. The experimental results, as shown in Fig. 8, demonstrate that an arbitrary node always forwards any query to almost all of its neighbors, when f ranges from $1 0 ^ { - 1 0 ^ { - } } \mathrm { t o } \ \mathrm { i } 0 ^ { - 3 }$ . Although each node can make a valid decision, such a decision is a flooding one with high probability. As pointed out in Section 4.3, the fundamental reason is as follows: Although the fraction of bits set to one in each individual Bloom filter might be low, that in each routing entry becomes high, very close to 1, due to the union of many decaying Bloom filters. Thus, given a query for any innetwork item, noise in unrelated routing entries and the useful information in right routing entries approximate to k, $\mathrm { i . e . , } \theta ( x , b f _ { i } ( l i n k ) )$ and noise become undistinguishable.

Each node, thus, cannot identify the right forwarding direction; hence, the gradient-based routing using existing designs of Bloom filters deteriorate to the flooding mechanism. In contrast, the gradient-based routing using Wader ensures that a query, which enters the decay range of a desired destination, will be routed along the right direction toward the destination. Fig. 3 further demonstrates the benefits of Wader compared to the existing gradient-based routing schemes. So far, only Wader can guarantee the correctness and efficiency of the gradient-based routing using Bloom filter with high probability.

Given any query, the message complexity is n for the existing gradient-based routing mechanisms and is log n for Wader, where n and log n denote the network size and diameter, respectively. In resource-constrained contexts, for example, wireless sensor networks, Wader is more energyefficient since it significantly reduces the number of transmitted messages. Additionally, the query delay in Wader is at most log n and is similar to that of the existing gradient-based routing schemes.

# 6 CONCLUSION

This work focuses on the issue of gradient-based routing using Bloom filters. We start with thorough analysis, which discloses the fact that the existing gradient-based routing mechanisms deteriorate to inefficient flooding-like mechanisms and even fail to route queries to the desired destinations. To address this issue, we derive two criteria that ensure the feasibility of gradient-based routing and propose a novel design, called Wader, to satisfy the two criteria. The evaluation results demonstrate that Wader ensures the correctness and efficiency of the gradient-based routing, achieving apparent performance gain when compared with the existing approaches.

# ACKNOWLEDGMENTS

The authors would like to thank anonymous reviewers for their constructive comments. The work was partially supported by the National Basic Research Program (973 program) under Grants Nos. 2014CB347800 and 2012CB316200, and the NSFC under Grants Nos. 61170284 and 61170213.

# REFERENCES

[1] D. Guo, J. Wu, H. Chen, Y. Yuan, and X. Luo, “The Dynamic Bloom Filters,” IEEE Trans. Knowledge and Data Eng., vol. 22, no. 1, pp. 120-133, Jan. 2010.   
[2] S.C. Rhea and J. Kubiatowicz, “Probabilistic Location and Routing,” Proc. IEEE INFOCOM, pp. 1248-1257, Jun. 2004.   
[3] D. Bauer, P. Hurley, R. Pletka, and M. Waldvogel, “Bringing Efficient Advanced Queries to Distributed Hash Tables,” Proc. IEEE Conf. Local Computer Networks, pp. 6-14, Nov. 2004.   
[4] H. Yoo, M. Shim, and D. Kim, “Scalable Multi-Sink Gradient-Based Routing Protocol for Traffic Load Balancing,” EURASIP J. Wireless Comm. and Networking, vol. 2011, p. 85, 2011.   
[5] Y. Azar, A. Broder, A. Karlin, and E. Upfal, “HR-SDBF: An Approach to Data-Centric Routing in WSNs,” Int’l J. High Performance Computing and Networking, vol. 6, nos. 3/4, pp. 181- 196, Sept. 2010.   
[6] R. Gilbert, K. Johnson, S. Wu, B.Y. Zhao, and H. Zheng, “Location Independent Compact Routing for Wireless Networks,” Proc. ACM First Int’l Workshop Decentralized Resource Sharing Mobile Computing and Networking (MobiShare), Sept. 2006.   
[7] W.H. Yuen and H. Schulzrinne, “Improving Search Efficiency Using Bloom Filters in Partially Connected Ad Hoc Networks: A Node-Centric Analysis,” Computer Comm., vol. 30, no. 16, pp. 3000- 3011, 2007.

[8] U.G. Acer, S. Kalyanaraman, and A.A. Abouzeid, “Weak State Routing for Large-Scale Dynamic Networks,” IEEE/ACM Trans. Networking, vol. 18, no. 5, pp. 1450-1463, Oct. 2010.   
[9] A. Kumar, J. Xu, and E.W. Zegura, “Efficient and Scalable Query Routing for Unstructured Peer-to-Peer Networks,” Proc. IEEE INFOCOM, pp. 1162-1173, Mar. 2005.   
[10] X. Li, J. Wu, and J.J. Xu, “Hint-Based Routing in WSNs Using Scope Decay Bloom Filters,” Proc. Int’l Workshop Networking, Architecture, and Storages (IWNAS ’06 ), pp. 111-118, 2006.   
[11] J. Faruque, K. Psounis, and A. Helmy, “Analysis of Gradient-Based Routing Protocols in Sensor Networks,” Proc. IEEE/ACM Int’l Conf. Distributed Computing in Sensor Systems (DCOSS), pp. 258-275, Jun. 2005.   
[12] J. Liu, F. Zhao, and D. Petrovic, “Information-Directed Routing in Ad Hoc Sensor Networks,” IEEE J. Select. Areas Comm., vol. 23, no. 4, pp. 851-861, Apr. 2005.   
[13] C. Intanagonwiwat, R. Govindan, and D. Estrin, “Directed Diffusion: A Scalable and Robust Communication Paradigm for Sensor Networks,” Proc. ACM MobiCom, 2000.   
[14] C. Schurgers and M. Srivastava, “Energy Efficient Routing in Wireless Sensor Networks,” Proc. IEEE Military Comm. Conf. (MILCOM), 2001.   
[15] T. Watteyne, K. Pister, D. Barthel, M. Dohler, and I. Auge-Blum, “Implementation of Gradient Routing in Wireless Sensor Networks,” Proc. IEEE GLOBECOM, 2009.   
[16] H. Lin, M. Lu, N. Milosavljevic, and J. Gao, “Composable Information Gradients in Wireless Sensor Networks,” Proc. Int’l Conf. Information Processing in Sensor Networks, pp. 121-132, 2008.   
[17] L. Katzir, E. Liberty, and O. Somekh, “Estimating Sizes of Social Networks via Biased Sampling,” Proc. 20th Int’l Conf. World Wide Web, pp. 597-606, 2011.   
[18] J.C.S. Cardoso, C. Baquero, and P.S. Almeida, “Probabilistic Estimation of Network Size and Diameter,” Proc. Fourth Latin-Am. Symp. Dependable Comput. (LADC ’09), pp. 33-40, 2009.   
[19] D. Stutzbach, R. Rejaie, N.G. Duffield, S. Sen, and W. Willinger, “On Unbiased Sampling for Unstructured Peer-To-Peer Networks,” IEEE/ACM Trans. Networking, vol. 17, no. 2, pp. 377-390, 2009.   
[20] G. Da´n and N. Carlsson, “Power-Law Revisited: A Large Scale Measurement Study of P2P Content Popularity,” Proc. IEEE Ninth Int’l Conf. Peer-to-Peer Systems (IPTPS ’10), 2010.

![](images/b47a8c79fb87a376943967493bcc6060d0fe0e4f147efee913958254e0d1b620.jpg)



Deke Guo received the BS degree in industry engineering from the Beijing University of Aeronautic and Astronautic, Beijing, China, in 2001, and the PhD degree in management science and engineering from the National University of Defense Technology, Changsha, China, in 2008. He is currently an associate professor with the College of Information System and Management, National University of Defense Technology, Changsha, China. His

research interests include distributed systems, wireless and mobile systems, P2P networks, and interconnection networks. He is a member of the IEEE and ACM.

![](images/30764b07bbaa94180597f5c59a21509dff268605fa256b3e3309bb4b914340f8.jpg)



Yuan He received the BE degree from the University of Science and Technology of China, the ME degree from Institute of Software, Chinese Academy of Sciences, and the PhD degree from Hong Kong University of Science and Technology. He is a member of Tsinghua National Lab for Information Science and Technology. His research interests include sensor networks, peer-to-peer computing, and pervasive computing. He is a member of the r Society, and ACM.

![](images/6505dda53c2158316187c9ded927cc46075572ae046a9a6b32b59756ceaff9ed.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is currently EMC chair professor at Tsinghua University, as well as a faculty member with the Hong Kong University of Science and Technology. His research interests include wireless sensor network, peer-to-peer computing, and pervasive

computing. He is a senior member of the IEEE and the IEEE Computer Society.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.