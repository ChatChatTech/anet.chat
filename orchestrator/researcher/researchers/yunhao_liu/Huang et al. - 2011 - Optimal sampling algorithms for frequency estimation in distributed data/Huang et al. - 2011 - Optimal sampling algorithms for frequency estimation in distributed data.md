# Optimal Sampling Algorithms for Frequency Estimation in Distributed Data

Zengfeng Huang

Ke Yi

Yunhao Liu

Guihai Chen

Hong Kong University of Science and Technology

{huangzf, yike, liu}@cse.ust.hk

Shanghai Jiaotong University

gchen@nju.edu.cn

Abstract—Consider a distributed system with n nodes where each node holds a multiset of items. In this paper, we design sampling algorithms that allow us to estimate the global frequency of any item with a standard deviation of $\varepsilon N$ , where N denotes the total cardinality of all these multisets. Our algorithms have a communication cost of $O ( n + { \sqrt { n } } / \varepsilon )$ , which is never worse than the $O ( n + 1 / \varepsilon ^ { 2 } )$ cost of uniform sampling, and could be much better when $n \ll 1 / \varepsilon ^ { 2 }$ . In addition, we prove that one version of our algorithm is instance-optimal in a fairly general sampling framework. We also design algorithms that achieve optimality on the bit level, by combining Bloom filters of various granularities. Finally, we present some simulation results comparing our algorithms with previous techniques. Other than the performance improvement, our algorithms are also much simpler and easily implementable in a largescale distributed system.

# I. INTRODUCTION

Consider a distributed system with n nodes where each node holds a list of (item, frequency) pairs, recording the local frequency of these items. In this paper, we study the problem of estimating the global frequencies of the items where an item’s global frequency is the sum of all the local frequencies at all the nodes, with minimum communication. This problem is motivated by many applications in distributed databases, network monitoring, sensor networks, data centers, cloud computing, etc. For example, estimating the frequencies of queried keywords is a routine task for search engines, while the query logs have to be stored in a distributed manner due to their sheer scale. The recently developed MapReduce framework [8] has provided a highly efficient and reliable programming environment for processing massive distributed data sets. As another example, in DDoS attacks the attacker tries to send a lot of traffic to the same victim via many different routes, so any individual router may not see a large number of packets destined to the victim. Thus in order to detect DDoS attacks we will have to estimate the global frequency of destination IP addresses. Other examples include estimating the popularity of files in peer-to-peer file-sharing networks, reporting the occurrences of different species of birds in a sensor network, and so on.

# A. Problem definition

We assume that the items are drawn from a bounded universe $[ u ] = \{ 1 , \dots , u \}$ . There are n distributed nodes in the system; we denote the local count of item i at node $j \ \mathrm { b y } \ x _ { i , j }$ , and the global count of item i is $y _ { i } = \textstyle \sum _ { j } x _ { i , j }$ . The total count of all items is denoted $N = \textstyle \sum _ { i } y _ { i }$ . There is a coordinator C whose job is to estimate $y _ { i }$ for all $i \in [ u ]$ by communicating with the nodes with minimum cost. Here and further the word “cost” will always refer to “communication cost”.

Since computing all the $y _ { i } \mathrm { \dot { s } }$ exactly incurs high costs and is often unnecessary, we will allow an absolute error of at most εN for some small $\varepsilon > 0$ . When probabilistic algorithms are concerned, this should be achieved with at least constant probability. This error definition has been used in most works on this problem [6, 7, 12, 13, 19]. Under such an error definition, we can zero out all the frequencies less than $\varepsilon N$ , so that the output size is bounded by $1 / \varepsilon$ . On the other hand, if we use a relative ε-error, then we are forced to make very accurate estimations for low-frequency items, which is expensive yet unnecessary. Note that there are some proposals of a (p, ε)-error [2, 11] that guarantees a relative ε-error only for frequencies at least $p N$ , which we briefly discuss in Section VII.

# B. Preliminaries and previous results

There is a simple deterministic algorithm with cost $O ( n / \varepsilon )$ . The idea is to ask each node to send in all its items with local counts greater than $\varepsilon N / n$ . Thus, for any item, each node contributes an error at most $\varepsilon N / n$ , totaling $\varepsilon N$ from all the n nodes. This simple algorithm has been used in some previous work [5], and is conjectured to be optimal for deterministic algorithms, although there has not been a proof.

With randomization there is potential to do better. To start with, it is well known [18] that uniformly sampling each item with probability $p = 1 / \varepsilon ^ { 2 } N$ suffices to estimate the count of any item within an error of $\varepsilon N$ with constant probability. To do the sampling, we need to compute N and then broadcast $p$ to all nodes, which require $O ( n )$ communication. The total (expected) cost of the sampling is thus $O ( n + p N ) = O ( n + 1 / \varepsilon ^ { 2 } )$ . So uniform sampling beats the deterministic algorithm when $n > 1 / \varepsilon$ . But how about the case $n < 1 / \varepsilon$ , which is more likely in real applications? Bear in mind that the ε-error as defined is an absolute error of $\varepsilon N$ , where $N$ is the total count of all items, so typical values of ε range from 0.0001 to 0.01 (see e.g. [6]), while n in real systems is usually no more than a few hundred.

Zhao et al. [21] defined a general sampling framework for the frequency estimation problem. Let $g : \mathbb { N } \longrightarrow [ 0 , 1 ]$ be a sampling function. If an item has local count x at a node, then the node with probability $g ( x )$ samples this item and sends the item together with its local count x to the coordinator. In addition to the local count x, we also allow the function $g ( x )$ to depend on $N , n , \varepsilon .$ . Set $Y _ { i , j } = x _ { i , j }$ if the coordinator receives the (item, count) pair $( i , x _ { i , j } )$ from node $j$ , and $Y _ { i , j } = 0$ otherwise. Then the coordinator can estimate $y _ { i }$ using (define $\begin{array} { r } { \frac { 0 } { 0 } = 0 ) } \end{array}$ 号

$$
Y _ {i} = \frac {Y _ {i , 1}}{g (Y _ {i , 1})} + \dots + \frac {Y _ {i , n}}{g (Y _ {i , n})}, \tag {1}
$$

which was shown [21] to be an unbiased estimator with variance

$$
\operatorname{Var} \left[ Y _ {i} \right] = \sum_ {j = 1} ^ {n} \operatorname{Var} \left[ \frac {Y _ {i}}{g \left(x _ {i , j}\right)} \right] = \sum_ {j = 1} ^ {n} \frac {x _ {i , j} ^ {2} \left(1 - g \left(x _ {i , j}\right)\right)}{g \left(x _ {i , j}\right)}. \tag {2}
$$

This framework is more general and should intuitively do better than uniform sampling. But as pointed out in [21], central to this framework is the choice of the sampling function $g .$ To be able to estimate $y _ { i }$ with error at most $\varepsilon N$ with a constant probability, we need to choose a g such that $\mathrm { V a r } [ Y _ { i } ] = \bar { \cal O } ( ( \varepsilon N ) ^ { 2 } )$ ). From (2) it is clear that Var[Yi] gets smaller as g gets larger. On the other hand, the expected total number of (item, count) pairs sent to the coordinator is $\textstyle \sum _ { i , j } g ( x _ { i , j } )$ , so we would want to choose the smallest g such that $\operatorname { V a r } [ Y _ { i } ] = O ( ( \varepsilon N ) ^ { 2 } )$ .

Zhao et al. [21] proposed to use $g ( x ) = x / ( x + d )$ for some fixed d. When using such a $g , { \mathrm { V a r } } [ Y _ { i } ]$ simplifies to $d y _ { i }$ . Since yi can be as large as $\Theta ( N )$ , we will have to set $d = \Theta ( \varepsilon ^ { 2 } N )$ in order to guarantee $\begin{array} { r } { \mathrm { V a r } [ Y _ { i } ] = O ( ( \varepsilon N ) ^ { 2 } ) } \end{array}$ for any i. Thus, the communication cost of their algorithm is Pi,j g(xi,j ) = Pi,j xi,jd+xi,j . $\begin{array} { r } { \sum _ { i , j } g ( x _ { i , j } ) = \sum _ { i , j } \frac { x _ { i , j } } { d + x _ { i , j } } } \end{array}$ In the worst case (when all the $x _ { i , j } \mathrm { ^ { \circ } s }$ are no more than $d )$ , this is at least $\textstyle { \frac { 1 } { 2 } } \sum _ { i , j } { \frac { x _ { i , j } } { d } } \ = \ \Theta ( N / d ) \ = \ \Theta ( 1 / \varepsilon ^ { 2 } )$ . We also need to compute $N$ and broadcast d to all nodes, so the total cost is $\Theta ( n + 1 / \varepsilon ^ { 2 } )$ , which is the same as that of uniform sampling. [21] also proposed some other complicated heuristics, but they do not improve the $\Theta ( n + 1 / \varepsilon ^ { 2 } )$ worst-cast cost. Therefore, although Zhao et al. [21] proposed a nice general sampling framework, they did not demonstrate whether this framework yields a solution that is asymptotically better than uniform sampling.

# C. Our results

In this paper we answer the above question in the affirmative, and in a very strong sense. Specifically, we obtain the following results.

We first show in Section III that the linear sampling function1 $g _ { 1 } ( x ) = x \sqrt { n } / \varepsilon N$ achieves ${ \mathrm { V a r } } [ Y _ { i } ] \leq$ ${ \cal O } ( ( \varepsilon N ) ^ { 2 } )$ , which, by Chebyshev’s inequality, allows us to estimate $y _ { i }$ within an error of $\varepsilon N$ with constant probability. The communication cost is $\begin{array} { r l } { \sum _ { i , j } g ( x _ { i , j } ) = } & { { } } \end{array}$ $O ( \sqrt { n } / \varepsilon )$ under any input2. This is clearly better than the $O ( n / \varepsilon )$ deterministic bound. It is also much better than the ${ \cal O } ( 1 / \varepsilon ^ { 2 } )$ uniform sampling cost when $n \ll 1 / \varepsilon ^ { 2 }$ . In the (rare) case $n > 1 / \varepsilon ^ { 2 }$ , uniform sampling still performs better.

Next, we prove an $\Omega ( \operatorname* { m i n } \{ \sqrt { n } / \varepsilon , 1 / \varepsilon ^ { 2 } \} )$ lower bound on the worst-case cost for all valid sampling functions. A sampling function is valid if it achieves ${ \mathrm { V a r } } [ Y _ { i } ] ~ \leq$ ${ \cal O } ( ( \varepsilon N ) ^ { 2 } )$ for all i under any input. This means that sampling with $g _ { 1 }$ and uniform sampling are respectively optimal in the cases $n < 1 / \varepsilon ^ { 2 }$ and $n > 1 / \varepsilon ^ { 2 }$ .

Although we have found optimal sampling functions for all values of n and ε, these are actually not the main results of this paper. We observe that on some inputs, it is possible to further reduce the communication cost. Consider an extreme case where all the $x _ { i , j } \mathrm { ^ { \circ } s }$ are either 0 or 1. If we use $g _ { 1 }$ , the cost is $\Theta ( { \sqrt { n } } / \varepsilon )$ . (In fact, due to the “linear” feature of $g _ { 1 }$ , its cost $\textstyle \sum _ { i , j } g _ { 1 } ( x _ { i , j } )$ is almost always $\Theta ( \sqrt { n } / \varepsilon ) . )$ In this case, $g _ { 1 }$ samples each $x _ { i , j } = 1$ with probability $\sqrt { n } / \varepsilon N$ . However, we observe from (2) that when the $x _ { i , j } \mathrm { ^ { \circ } s }$ are all very small, we can afford to use a smaller sampling rate while still keeping Var[Yi] small. Indeed, in this case we can sample each $x _ { i , j } ~ = ~ 1$ with probability $n / ( \varepsilon N ) ^ { 2 }$ while still having $\mathrm { V a r } [ Y _ { i } ] = O ( ( \varepsilon N ) ^ { 2 } )$ ). When using such a sampling rate, the total cost reduces to $\Theta ( N n / ( \varepsilon N ) ^ { 2 } ) = \Theta ( n / \varepsilon ^ { 2 } N )$ ,

1The function is actually $g _ { 1 } ( x ) =$ min $\{ x { \sqrt { n } } / \varepsilon N , 1 \}$ as any g cannot exceed 1. We omit the $\cdots _ { \mathrm { m i n } } , $ here and further for brevity.

2Henceforth we omit the $O ( n )$ ) term for computing N and broadcasting g to all nodes when considering the algorithms’ costs, because 1) it makes the bounds cleaner; 2) this cost is common to all algorithms in this sampling framework; and 3) this cost is due to computing $N _ { \ast }$ which can be easily shown to be unavoidable if N is unknown.

which, interestingly, approaches 0 as $N \to \infty$ , and can be much lower than both the $\Theta ( { \sqrt { n } } / \varepsilon )$ cost of $g _ { 1 }$ and the $\Theta ( 1 / \varepsilon ^ { 2 } )$ cost of uniform sampling. Although practical cases are not as extreme, it is very common to have a lot of small $x _ { i , j } \mathrm { ^ { \circ } s }$ due to the heavy tail property of many real-world distributions. Of course, in view of the above lower bound, it is not possible to beat (the better of) $g _ { 1 }$ and uniform sampling on the worst input, but can we do something better for these typical, not-so-worst cases?

The answer is yes. In Section IV we show that the sampling function

$$
g _ {2} (x) = \min \{x ^ {2} n / (\varepsilon N) ^ {2}, x / \varepsilon^ {2} N \}
$$

also achieves $\mathrm { V a r } [ Y _ { i } ] ~ \le ~ { \cal O } ( ( \varepsilon N ) ^ { 2 } )$ with the optimal worst-case cost of O(min $\{ { \sqrt { n } } / \varepsilon , 1 / \varepsilon ^ { 2 } \} ,$ ). So in the worst case, it performs the same as $g _ { 1 }$ (for $n < 1 / \varepsilon ^ { 2 } )$ and uniform sampling (for $n > 1 / \varepsilon ^ { 2 } )$ . To analytically establish the superiority of $g _ { 2 } , \mathrm { w e }$ prove that it is instanceoptimal [9], $\mathrm { i . e . }$ , for every given input $I : \{ x _ { i , j } \} , g$ 2 has the optimal cost (up to a constant factor) among all the valid sampling functions on that input. More precisely, let $\begin{array} { r } { o p t ( I ) = \sum _ { i , j } g _ { 2 } ( x _ { i , j } ) } \end{array}$ be the cost of sampling with $g _ { 2 }$ on input $I ,$ we show that any valid sampling function must have cost $\Omega ( o p t ( I ) )$ on $I ,$ which essentially means that $g _ { 2 }$ is the best sampling function on every single input. This is a much stronger optimality notion than the traditional worst-case optimality.

So far we have treated an (item, count) pair as a communication unit. If one desires a more precise analysis, such a pair actually consumes O(log u + log N ) bits. To further reduce the communication cost, we design techniques that are more careful about the bits they send. We show in Section V how to reduce the communication cost on the bit level by using multiple Bloom filters [1, 16] at different levels of granularity. Although $g _ { 1 }$ is not as good as $g _ { 2 }$ in terms of sampling, it is particularly amenable to Bloom filters. It turns out that we can remove the extra $O ( \log u + \log N )$ factor completely when using $g _ { 1 }$ , $\mathrm { i . e . }$ , we obtain an algorithm communicating $O ( \sqrt { n } / \varepsilon )$ bits. The instance-optimal sampling function $g _ { 2 }$ is more difficult to directly plug into Bloom filters, but then we use an interesting combination of $g _ { 1 }$ and $g _ { 2 }$ to achieve a cost of $\begin{array} { r } { O \left( o p t ( I ) \log ^ { 2 } \left( \frac { \sqrt { n } } { \varepsilon \cdot o p t ( I ) } \right) \right) } \end{array}$ bits.

Finally, we comment that all our algorithms are very simple, and can be easily implemented in a large-scale distributed system. In particular, they can be easily accomplished in the MapReduce framework. Thus, we would claim that our algorithms are both theoretically interesting and practically useful.

# II. RELATED WORK

Besides the work of Zhao et al. [21] which is the closest work to ours, a number of related problems have been studied by the database and distributed computing communities.

The heavy hitter problem [6, 13] has been well studied in the centralized case. The goal here is to report all items with frequency exceeding φN for some user specified $\phi ,$ not report items with frequency below $\left( \phi - \varepsilon \right) N$ , while we do not care frequencies in between. Our algorithms clearly solve this problem in the distributed setting. Zhao et al. [20] studied the distributed heavy hitter problem while using a relative λ-error $( 0 ~ < ~ \lambda < ~ 1 ) \colon$ the heavy hitters’ global counts are more than τ while the non-heavy hitters’ counts should be less than $\lambda \tau .$ for some threshold $\tau .$ The communication cost of their algorithm is $O ( n u \lambda ^ { 2 } )$ , so it only applies to situations where there is a very small universe. Furthermore, note that $O ( n u )$ is a trivial upper bound (each node sending all items would cost this much), so this algorithm beats the naive solution only when there is a very large gap between the heavy and non-heavy hitters. Meanwhile, they also showed a matching $\tilde { \Omega } ( k u \lambda ^ { 2 } )$ lower bound3 This apparent hardness of the problem actually stems from distinguishing between a global count of 1 and $1 / \lambda$ , which corresponds to using a very small $\tau . \mathrm { I f } \ \tau = \phi n$ as mostly used in the literature [6], this problem can be in fact solved efficiently as shown in this paper.

The distributed $t o p { - } k$ problem [4, 14, 15] is another related one, where the goal is to find the top-k most frequent items. Cao and Wang [4] designed an algorithm that solves this problem exactly, but it could ship all the data to the coordinator on some inputs. They also proved that their algorithm is instance-optimal, but this only holds for inputs following a certain distribution and the optimality ratio is as large as $O ( n ^ { 2 } )$ . Note that our instance-optimality ratio is a constant and it holds for any input. The apparent difficulty of their approach stems from situations where the k-th frequent item is very close to the $( k + 1 )$ -st one, and they want to detect this exactly. Patt-Shamir and Shafrir [15] considered a more solvable version of the problem where they allow a relative ε-error when separating the top-k list from the rest. The communication cost of their algorithm is $\tilde { O } ( 1 / p ^ { * } \varepsilon ^ { 2 } )$ where $p ^ { * }$ is the frequency of the k-th frequent item divided by N . Their algorithm uses multiple rounds of uniform sampling to estimate the frequencies. If we use our algorithms in place of uniform sampling, the cost improves to $\tilde { O } ( \sqrt { n } / p ^ { * } \varepsilon )$ when $n \ll 1 / \varepsilon ^ { 2 }$ . Using our instance-optimal algorithm will result in a larger improvement for certain inputs, although it is hard to analytically quantify, since instance optimality has to be stated for a specific problem and in a clearly defined framework. Michel et al. [14] generalized and improved the algorithm of [4], but with no analytical results.

The distributed approximate quantile problem has also been well studied, where the goal is to return a set of items whose ranks are between $\left( \phi - \varepsilon \right) N$ and $( \phi + \varepsilon ) N$ for all $0 < \phi < 1$ . It is known [6] that the frequency estimation problem reduces to the quantile problem, but the best algorithms for the latter incur $\tilde { O } ( n / \varepsilon )$ costs [10, 17], at least a factor ${ \tilde { O } } ( { \sqrt { n } } )$ worse than our bounds.

Finally, there have been a lot of interests in the problem of continuously tracking the heavy hitters, quantiles, and top-k items in distributed data [3, 5, 19]. The tracking problem is more general as it requires solving the respective problems at all times continuously, rather than a one-shot computation. However, all these cited works studied only deterministic algorithms; in fact, the deterministic complexity for tracking the heavy hitters and quantiles has been settled at $\tilde { \Theta } ( n / \varepsilon )$ in [19]. We believe that the techniques developed in this paper could lead to probabilistic schemes solving these problems with cost ${ \tilde { O } } ( { \sqrt { n } } / \varepsilon )$ .

# III. A WORST-CASE OPTIMAL SAMPLING FUNCTION

In this section, we show that the sampling function $g _ { 1 } ( x ) = x \sqrt { n } / \varepsilon N$ is worst-case optimal. In this section and Section $\mathrm { I V }$ , we measure the communication cost as the expected total number of (item, count) pairs sampled and sent to the coordinator, $\begin{array} { r } { \mathrm { i . e . , } \sum _ { i , j } g ( x _ { i , j } ) } \end{array}$ for a given $g .$ In Section V we will conduct a more precise analysis measuring the cost in terms of the bits communicated.

Theorem $3 . I \colon$ The sampling function $g _ { 1 } ( x )$ = $x \sqrt { n } / \varepsilon N$ has a cost of $O ( \sqrt { n } / \varepsilon )$ and achieves $\begin{array} { r } { \dot { \mathrm { V a r } } [ \dot { Y } _ { i } ] = \frac { 1 } { 4 } ( \varepsilon N ) ^ { 2 } } \end{array}$ for all i.

Proof: The analysis of the cost is trivial: $\begin{array} { r } { \sum _ { i , j } g _ { 1 } ( x _ { i , j } ) ~ \le ~ \sum _ { i , j } x _ { i , j } \sqrt { n } / { \varepsilon N } ~ = ~ N \cdot \sqrt { n } / { \varepsilon N } ~ = ~ } \end{array}$ $\sqrt { n } / \varepsilon$ .

Now we consider the variance of $Y _ { i }$ . Since we sample an item with probability one $( \mathrm { i . e . }$ , zero variance) when the local count $x _ { i , j } > \varepsilon N / \sqrt { n }$ , it is sufficient to consider the worst case when all $x _ { i , j } \leq \varepsilon N / \sqrt { n }$ . By (2), we have

$$
\begin{array}{l} \operatorname{Var} [ Y _ {i} ] = \sum_ {j = 1} ^ {n} \frac {x _ {i , j} ^ {2} (1 - x _ {i , j} \sqrt {n} / \varepsilon N)}{x _ {i , j} \sqrt {n} / \varepsilon N} \\ = \frac {\varepsilon N}{\sqrt {n}} \sum_ {j = 1} ^ {n} x _ {i, j} - \sum_ {j = 1} ^ {n} x _ {i, j} ^ {2} \\ \leq \frac {\varepsilon N}{\sqrt {n}} y _ {i} - \frac {1}{n} y _ {i} ^ {2} \quad (\text { Cauchy   -   Schwartz }) \tag {3} \\ \end{array}
$$

$$
= - \left(\frac {y _ {i}}{\sqrt {n}} - \frac {\varepsilon N}{2}\right) ^ {2} + \frac {(\varepsilon N) ^ {2}}{4} \leq \frac {1}{4} (\varepsilon N) ^ {2}.
$$

Next we establish the worst-case optimality of $g _ { 1 }$ when $n < 1 / \varepsilon ^ { 2 }$ . For the (unrealistic) case $n > 1 / \varepsilon ^ { 2 } .$ uniform sampling turns out to be optimal already. Recall that a sampling function $g$ is valid if there exists some constant c such that on any input, g achieves ${ \mathrm { V a r } } [ Y _ { i } ] \leq$ $c ( \varepsilon N ) ^ { 2 }$ for all i.

Theorem $3 . 2 \colon \mathrm { A n y }$ valid sampling function has cost $\Omega ( \operatorname* { m i n } \{ \sqrt { n } / \varepsilon , 1 / \varepsilon ^ { 2 } \} )$ on some input.

Proof: Let g be any valid sampling function. We will consider the following two cases, respectively.

$1 ) n < 1 / \varepsilon ^ { 2 } \colon$ In this case, we consider an input where $x _ { i , j } ~ = ~ \varepsilon N / \sqrt { n }$ for all $i , j$ . Thus each item has $y _ { i } =$ $n x _ { i , j } = \varepsilon { \sqrt { n } } \cdot N$ copies over all n nodes, and there are $N / x _ { i , j } = \sqrt { n } / \varepsilon$ such $x _ { i , j } \mathrm { ^ { \circ } s }$ .

From (2) we have

$$
\operatorname{Var} \left[ Y _ {i} \right] = \sum_ {j = 1} ^ {n} \frac {(\varepsilon N) ^ {2} / n \cdot (1 - g \left(x _ {i , j}\right))}{g \left(x _ {i , j}\right)}.
$$

Since we requequal, we have $\mathrm { V a r } [ Y _ { i } ] ~ \le ~ c ( \varepsilon N ) ^ { 2 }$ $x _ { i , j }$ are $\begin{array} { r } { \frac { 1 - g ( x _ { i , j } ) } { g ( x _ { i , j } ) } \leq c , } \end{array}$ $\begin{array} { r } { g ( x _ { i , j } ) \geq \frac { 1 } { 1 + c } . } \end{array}$

The cost of $g$ is thus

$$
\sum_ {i, j} g (x _ {i, j}) = \sqrt {n} / \varepsilon \cdot \frac {1}{1 + c} = \Omega (\sqrt {n} / \varepsilon).
$$

2) $n > 1 / \varepsilon ^ { 2 } ;$ In this case, we consider an input where there is only one item in the universe $u \ : = \ : 1$ , and it exists only at $1 / \varepsilon ^ { 2 }$ nodes with $x _ { 1 , j } = \varepsilon ^ { 2 } N$ at each of these nodes; the other nodes are empty.

From (2) we have

$$
\operatorname{Var} \left[ Y _ {1} \right] = (\varepsilon N) ^ {2} \frac {1 - g \left(\varepsilon^ {2} N\right)}{g \left(\varepsilon^ {2} N\right)}.
$$

By the requirement that $\operatorname { V a r } [ Y _ { 1 } ] \leq c ( \varepsilon N ) ^ { 2 }$ , we have

$$
g (\varepsilon^ {2} N) \geq \frac {1}{1 + c}.
$$

The cost of g is thus $1 / \varepsilon ^ { 2 } \cdot g ( \varepsilon ^ { 2 } N ) = \Omega ( 1 / \varepsilon ^ { 2 } )$ .

# IV. AN INSTANCE-OPTIMAL SAMPLING FUNCTION

In this section, we first show that the sampling function

$$
g _ {2} (x) = \min \{x ^ {2} n / (\varepsilon N) ^ {2}, x / \varepsilon^ {2} N \}
$$

also achieves $\mathrm { V a r } [ Y _ { i } ] ~ = ~ { \cal O } ( ( \varepsilon N ) ^ { 2 } )$ . In terms of cost, since $g _ { 2 } ( x ) \leq g _ { 1 } ^ { 2 } ( x )$ , the cost of $g _ { 2 }$ is always no more than that of $_ { g _ { 1 } ; }$ also since $g _ { 2 } ( x ) \leq x / \varepsilon ^ { 2 } N$ , its cost is at most ${ \cal O } ( 1 / \varepsilon ^ { 2 } )$ . Thus it has the optimal worst-case cost of $O ( \operatorname* { m i n } \{ \sqrt { n } / \varepsilon , 1 / \varepsilon ^ { 2 } \} )$ ). To analytically establish its superiority, we later prove that it is instance-optimal, i.e., for any input I , its cost is optimal among all valid sampling functions for I.

Theorem 4.1: The sampling function $g _ { 2 } ( x )$ achieves $\operatorname { V a r } [ Y _ { i } ] \leq O ( ( \varepsilon N ) ^ { 2 } )$ for all i.

Proof: Similar to the proof of Theorem 3.1, we can assume that $g _ { 2 } ( x _ { i , j } ) ~ < ~ 1$ for all j; otherwise its contribution to $\mathrm { V a r } [ Y _ { i } ]$ is zero. From (2), we have

$$
\begin{array}{l} \operatorname{Var} \left[ Y _ {i} \right] = \sum_ {j = 1} ^ {n} \frac {x _ {i , j} ^ {2} \left(1 - g _ {2} \left(x _ {i , j}\right)\right)}{g _ {2} \left(x _ {i , j}\right)} \leq \sum_ {j = 1} ^ {n} \frac {x _ {i , j} ^ {2}}{g _ {2} \left(x _ {i , j}\right)} \\ = \sum_ {j = 1} ^ {n} x _ {i, j} ^ {2} \max \left\{\frac {(\varepsilon N) ^ {2}}{n x _ {i , j} ^ {2}}, \frac {\varepsilon^ {2} N}{x _ {i , j}} \right\} \\ \leq \sum_ {j = 1} ^ {n} \left(x _ {i, j} ^ {2} \frac {(\varepsilon N) ^ {2}}{n x _ {i , j} ^ {2}} + \sum_ {j = 1} ^ {n} x _ {i, j} ^ {2} \frac {\varepsilon^ {2} N}{x _ {i , j}}\right) \\ = O ((\varepsilon N) ^ {2}). \\ \end{array}
$$

To prove that $g _ { 2 }$ is instance-optimal, for any input $I : \{ x _ { i , j } \}$ we write $\begin{array} { r } { o p t ( I ) \ = \ \sum _ { i , j } g _ { 2 } ( x _ { i , j } ) } \end{array}$ which is the cost of $g _ { 2 }$ . We then show that any valid sampling function on I must have cost $\Omega ( o p t ( I ) )$ .

Theorem 4.2: On input $I : \{ x _ { i , j } \}$ , any valid sampling function must have cost $\Omega ( o p t ( I ) )$ .

Proof: Let g be any valid sampling function, and we will show that $\begin{array} { r } { \sum _ { i , j } g ( x _ { i , j } ) = \Omega ( o p t ( I ) ) } \end{array}$ . We will prove it by contradiction: If $\begin{array} { r } { g ( x _ { i , j } ) < \frac { 1 } { 2 } g _ { 2 } ( x _ { i , j } ) } \end{array}$ ) for some $x _ { i , j } ,$ we show that it is possible to construct another input $\bar { I } ^ { \prime }$ (with the same N, n, ε so that g stays the same) on which $g$ fails to achieve $\mathrm { V a r } [ Y _ { i } ] \leq c ( \varepsilon N ) ^ { 2 }$ . In the proof we will use $c = 1$ for simplicity; the same proof works for any other constant c by properly adjusting the parameters.

We consider the following two cases:

1) $n < 1 / \varepsilon ^ { 2 }$ : If $x _ { i , j } \leq \varepsilon N / \sqrt { n }$ , then we construct $I ^ { \prime }$ by setting $x _ { i , j } ^ { \prime } = x _ { i , j }$ for all $j .$ Now the global count of item i is $y _ { i } \stackrel { \sim } { = } n x _ { i , j } = \varepsilon \sqrt { n } \cdot N \leq N$ . We set the other $x _ { i , j } ^ { \prime }$ so that $\textstyle \sum _ { i , j } x _ { i , j } ^ { \tilde { \prime } } = \tilde { N }$ . Thus the variance of $Y _ { i }$ is

$$
\operatorname{Var} \left[ Y _ {i} \right] = n \left(\frac {x _ {i , j} ^ {2}}{g \left(x _ {i , j}\right)} - x _ {i, j} ^ {2}\right).
$$

Note that when $n \ < \ 1 / \varepsilon ^ { 2 }$ and $x _ { i , j } ~ \le ~ \varepsilon N / \sqrt { n }$ , we have $g _ { 2 } ( x _ { i , j } ) = x _ { i , j } ^ { 2 } n / ( \varepsilon N ) ^ { 2 }$ , so by the assumption that $\begin{array} { r } { g ( x _ { i , j } ) < \frac { 1 } { 2 } g _ { 2 } ( x _ { i , j } ) } \end{array}$ ,

$$
\operatorname{Var} [ Y _ {i} ] > n \left(\frac {2 (\varepsilon N) ^ {2}}{n} - \left(\frac {\varepsilon N}{\sqrt {n}}\right) ^ {2}\right) = (\varepsilon N) ^ {2}.
$$

If $x _ { i , j } > \varepsilon N / \sqrt { n } > \varepsilon ^ { 2 } N$ , we construct $I ^ { \prime }$ by setting $x _ { i , j } ^ { \prime } = x _ { i , j }$ for $1 \leq j \leq m$ , where $m = \operatorname* { m i n } \{ N / x _ { i , j } , n \}$ . One can check that $m x _ { i , j } ^ { 2 } > ( \varepsilon N ) ^ { 2 }$ always holds. So

$$
\operatorname{Var} \left[ Y _ {i} \right] = m x _ {i, j} ^ {2} \left(\frac {1}{g \left(x _ {i , j}\right)} - 1\right) > (\varepsilon N) ^ {2} \left(\frac {1}{g \left(x _ {i , j}\right)} - 1\right).
$$

When $n < 1 / \varepsilon ^ { 2 }$ and $x _ { i , j } > \varepsilon ^ { 2 } N , g _ { 2 } ( x _ { i , j } ) = 1$ . So by the assumption, we have $g ( x _ { i , j } ) < 1 / 2$ . Thus

$$
\operatorname{Var} [ Y _ {i} ] > (\varepsilon N) ^ {2}.
$$

2) $n > 1 / \varepsilon ^ { 2 } \colon \mathrm { I f ~ } x _ { i , j } \le N / n < \varepsilon N / \sqrt { n }$ , we set $x _ { i , j } ^ { \prime } =$ $x _ { i , j _ { c } }$ for all $j .$ By the assumption, we have $g ( x _ { i , j } ) <$ < 2(εN)2 , then we have $\frac { n x _ { i , j } ^ { \star } } { 2 ( \varepsilon N ) ^ { 2 } }$ nx i,j 2

$$
\operatorname{Var} \left[ Y _ {i} \right] = n \left(\frac {x _ {i , j} ^ {2}}{g \left(x _ {i , j}\right)} - x _ {i, j} ^ {2}\right) > n \left(\frac {2 (\varepsilon N) ^ {2}}{n} - x _ {i, j} ^ {2}\right) > (\varepsilon N) ^ {2}.
$$

If $x _ { i , j } > N / n$ , then we set $x _ { i , j } ^ { \prime } = x _ { i , j }$ for $1 \le j \le$ $N / x _ { i , j }$ . In this case, $x _ { i , j }$ may be either greater than or less than $\varepsilon ^ { 2 } N$ . If it is less than $\varepsilon ^ { 2 } N$ , then $g _ { 2 } ( x _ { i , j } ) =$ $x _ { i , j } / \varepsilon ^ { 2 } N$ , and

$$
\mathrm{Var} [ Y _ {i} ] = \frac {N}{x _ {i , j}} \left(\frac {x _ {i , j} ^ {2}}{g (x _ {i , j})} - x _ {i, j} ^ {2}\right) > \frac {N x _ {i , j}}{g (x _ {i , j})} - (\varepsilon N) ^ {2} > (\varepsilon N) ^ {2}.
$$

If $x _ { i , j }$ is greater than $\varepsilon ^ { 2 } N$ , we have $g _ { 2 } ( x _ { i , j } ) = 1$ and hence $g ( x _ { i , j } ) < 1 / 2$ , so

$$
\operatorname{Var} \left[ Y _ {i} \right] = N x _ {i, j} \left(\frac {1}{g \left(x _ {i , j}\right)} - 1\right) > (\varepsilon N) ^ {2}.
$$

Summarizing all cases, g cannot be a valid function if $\begin{array} { r c l } { g ( x _ { i , j } ) } & { < } & { \frac { 1 } { 2 } g _ { 2 } ( x _ { i , j } ) } \end{array}$ . This holds for all $i , j$ , so $\begin{array} { r } { \sum _ { i , j } g ( \bar { x } _ { i , j } ) = \tilde { \Omega } ( o p t ( \bar { I } ) ) } \end{array}$ .

# V. REDUCING COMMUNICATION BY BLOOM FILTERS

In this section we will conduct a more precise analysis of the communication cost in terms of the number of bits transmitted. If the nodes directly send a sampled (item, count) pair to the coordinator, the cost will be $O ( \log u + \log N )$ bits per pair. Below we show how to reduce this cost by encoding the sampled items into Bloom filters. Recall that a Bloom filter is a spaceefficient encoding scheme that compactly stores a set of items S. The particularly interesting feature is that it uses O(1) bits per item, regardless of the length of the item. A Bloom filter does not have false negatives, but may have a constant false positive probability q for any queried item. More precisely, if the queried item is in $S .$ the answer is always “yes”; if it is not in S, then with probability $q$ it returns “yes” and with probability $1 - q$ returns “no”. The false positive probability q can be made arbitrarily small by using $O ( \log ( 1 / q ) )$ bits per item. We omit the details of Bloom filters (see e.g. [1] for general information and [16] for the current state of the Bloom filter), but only point out that the false positive probability q can be computed exactly from |S| and the size of the Bloom filter. These two numbers only require $O ( \log | S | + \log \log ( 1 / q ) )$ bits, so transmitting them together with the Bloom filter does not affect the $O ( \log ( 1 / q ) )$ )-bit cost per item.

Sampling with $\mathbf { \mathbf { \mathit { g } } _ { 1 } }$ , the easy case.: Although $g _ { 1 }$ has a higher sampling rate than $g _ { 2 }$ , its linear feature (when $x \leq \varepsilon N / \sqrt { n } )$ does have an advantage when it comes to saving bits: $\frac { Y _ { i , j } } { g _ { 1 } ( Y _ { i , j } ) }$ is either 0 or $\varepsilon N / \sqrt { n }$ in the estimator (1). This is independent of $x _ { i , j }$ , which means that for any sampled (item, count) pair, the nodes do not actually need to send the count! Thus, the set of (item, count) pairs a node sends to the coordinator becomes just a set of items, which can be encoded in a Bloom filter. Suppose for now that $x _ { i , j } \leq \varepsilon N / \sqrt { n }$ for all $i , j$ . In this case, each node $j$ simply samples item i with probability $g _ { 1 } ( x _ { i , j } )$ , then encodes the sampled items into a Bloom filter and sends it to the coordinator. For any $i \in [ u ]$ , suppose among the n Bloom filters that the coordinator has received, $Z _ { i }$ of them asserts its existence, then we can estimate $y _ { i }$ as

$$
Y _ {i} = \frac {\varepsilon N}{\sqrt {n}} \cdot \frac {Z _ {i} - n q}{1 - q}. \tag {4}
$$

We show that (4) is an unbiased estimator and has a small variance. We also note that for the analysis to go through, the nodes need to use independent random hash functions in their Bloom filters.

$$
\text { Lemma   5.1: } \mathbf {E} [ Y _ {i} ] = y _ {i}; \operatorname{Var} [ Y _ {i} ] \leq \frac {(\varepsilon N) ^ {2}}{4 (1 - q) ^ {2}}.
$$

Proof: We define $Z _ { i , j }$ to be the indicator random variable set to 1 if the Bloom Filter from node $j$ asserts that it contains the item i, and 0 otherwise. It is easy to see that $\mathrm { P r } [ Z _ { i , j } = 1 ] = g _ { 1 } ( x _ { i , j } ) + ( 1 - g _ { 1 } ( x _ { i , j } ) ) q$ , and thus $\mathbf { E } [ Z _ { i , j } ] = g _ { 1 } ( x _ { i , j } ) + ( 1 - g _ { 1 } ( x _ { i , j } ) ) q$ . Then we have

$$
\begin{array}{l} \mathbf {E} [ Y _ {i} ] = \frac {\varepsilon N}{\sqrt {n}} \cdot \frac {\mathbf {E} [ Z _ {i} ] - n q}{1 - q} \\ = \frac {\varepsilon N}{\sqrt {n}} \cdot \frac {\sum_ {j = 1} ^ {n} \mathbf {E} [ Z _ {i , j} ] - n q}{1 - q} \\ = \frac {\varepsilon N}{\sqrt {n}} \cdot \frac {(1 - q) \sum_ {j = 1} ^ {n} g _ {1} (x _ {i , j}) + n q - n q}{1 - q} \\ = \frac {\varepsilon N}{\sqrt {n}} \sum_ {j = 1} ^ {n} g _ {1} (x _ {i, j}) = y _ {i}. \\ \end{array}
$$

The variance of the estimator is

$$
\begin{array}{l} \mathrm{Var} [ Y _ {i} ] = \frac {(\varepsilon N) ^ {2}}{n (1 - q) ^ {2}} \mathrm{Var} [ Z _ {i, j} ] \\ { = } { \frac { ( \varepsilon N ) ^ { 2 } } { n ( 1 - q ) ^ { 2 } } \sum _ { j = 1 } ^ { n } \mathrm{Var} [ Z _ { i , j } ] } \\ \end{array}
$$

$$
\begin{array}{l} = \frac {(\varepsilon N) ^ {2}}{n (1 - q) ^ {2}} \sum_ {j = 1} ^ {n} ((g _ {1} (x _ {i, j}) + (1 - g _ {1} (x _ {i, j})) q) \\ (1 - g _ {1} (x _ {i, j}) - (1 - g _ {1} (x _ {i, j})) q)) \\ = \frac {(\varepsilon N) ^ {2}}{n (1 - q) ^ {2}} \left(\frac {n}{4} - \left(\frac {(1 - q) y _ {i}}{\varepsilon N} - \frac {(1 - 2 q) \sqrt {n}}{2}\right) ^ {2}\right) \\ \leq \frac {(\varepsilon N) ^ {2}}{4 (1 - q) ^ {2}}. \\ \end{array}
$$

Thus, it is sufficient to set a constant q so that ${ \mathrm { V a r } } [ Y _ { i } ] =$ ${ \cal O } ( ( \varepsilon N ) ^ { 2 } )$ . Since now each sampled (item, count) pair only consumes $O ( \log ( 1 / q ) ) = O ( 1 )$ bits, the total cost is $O ( \sqrt { n } / \varepsilon )$ bits.

Sampling with $\mathbf { \mathbf { \mathit { g } _ { 1 } } }$ , the general case.: The above simple scheme works when all $x _ { i , j } \le \varepsilon N / \sqrt { n }$ . When $x \ge \varepsilon N / \sqrt { n } , g _ { 1 } ( x )$ hits 1 and is no longer linear. So any $x _ { i , j } \geq \varepsilon N / \sqrt { n }$ cannot be encoded in a Bloom filter, and unfortunately, there could be $O ( \sqrt { n } / \varepsilon )$ of them, costing $O ( \sqrt { n } / \varepsilon \cdot ( \log u + \log N ) )$ bits. Smarter techniques are thus needed for the general case when the $x _ { i , j } \mathrm { ^ { \circ } s }$ take arbitrary values.

We write each $x _ { i , j }$ in the form of

$$
x _ {i, j} = a _ {i, j} \frac {\varepsilon N}{\sqrt {n}} + b _ {i, j}, \tag {5}
$$

where $a _ { i , j }$ and $b _ { i , j }$ are both non-negative integers and $\begin{array} { r } { a _ { i , j } \le \frac { \sqrt { n } } { \varepsilon } , b _ { i , j } < \frac { \varepsilon N } { \sqrt { n } } } \end{array}$ , bi,j . Note that

$$
y _ {i} = \frac {\varepsilon N}{\sqrt {n}} \sum_ {j = 1} ^ {n} a _ {i, j} + \sum_ {j = 1} ^ {n} b _ {i, j}. \tag {6}
$$

The term $\textstyle \sum _ { j = 1 } ^ { k } b _ { i , j }$ can be estimated using Lemma 5.1 since bi,j $\begin{array} { r } { b _ { i , j } < \frac { \bar { \varepsilon } N } { \sqrt { n } } } \end{array}$ < √εNn , so we focus on estimating the first term N with variance $O ( ( \varepsilon n ) ^ { 2 } )$ .

Our idea is to consider each $a _ { i , j }$ in its binary form and dealing with each bit individually. Let $a _ { i , j } [ r ]$ be the r-th rightmost bit of $a _ { i , j }$ (counting from 0). For each $^ { r , }$ node $j$ encodes all the items i where $a _ { i , j } [ r ] = 1$ in a Bloom filter with false positive probability $q _ { r }$ . Intuitively, $q _ { r }$ should be smaller for more significant bits (i.e., larger $r )$ , but we will derive this relationship later. For any item i, suppose $Z _ { i , i }$ r is the number of Bloom filters that asserts $a _ { i , j } [ r ] = 1$ . Below we show that

$$
A _ {i} = \frac {\varepsilon N}{\sqrt {n}} \sum_ {r = 0} ^ {\log (\sqrt {n} / \varepsilon)} 2 ^ {r} \frac {Z _ {i , r} - n q _ {r}}{1 - q _ {r}}
$$

is an unbiased estimator for the first term of (6) and bound its variance.

$$
\text { Lemma   5.2: } \mathbf {E} [ A _ {i} ] = \frac {\varepsilon N}{\sqrt {n}} \sum_ {j = 1} ^ {n} a _ {i, j}; \operatorname{Var} [ A _ {i} ] \leq
$$

$$
(\varepsilon N) ^ {2} \sum_ {r = 0} ^ {\log (\sqrt {n} / \varepsilon)} 2 ^ {2 r} \frac {q _ {r}}{1 - q _ {r}}.
$$

r=0Proof: Let $\begin{array} { r } { c _ { i , r } = \sum _ { j = 1 } ^ { n } a _ { i , j } [ r ] } \end{array}$ . Since there are $n -$ $c _ { i , i }$ r Bloom filters which may, with probability $q _ { r }$ , assert $a _ { i , j } [ r ] = 1$ despite $a _ { i , j } [ r ] = 0$ , it is easy to see that ${ \bf E } [ Z _ { i , r } ] = c _ { i , r } + ( n - c _ { i , r } ) q _ { r }$ , and $\mathrm { V a r } [ Z _ { i , r } ] = ( n -$ $c _ { i , r } ) q _ { r } ( 1 - q _ { r } ) \leq n q _ { r } ( 1 - q _ { r } )$ . Thus we have

$$
\begin{array}{l} \mathbf {E} [ A _ {i} ] = \frac {\varepsilon N}{\sqrt {n}} \sum_ {r = 0} ^ {\log (\sqrt {n} / \varepsilon)} 2 ^ {r} \frac {\mathbf {E} [ Z _ {i , r} ] - n q _ {r}}{1 - q _ {r}} \\ = \frac {\varepsilon N}{\sqrt {n}} \sum_ {r = 0} ^ {\log (\sqrt {n} / \varepsilon)} 2 ^ {r} c _ {i, r} = \frac {\varepsilon N}{\sqrt {n}} \sum_ {j = 1} ^ {n} a _ {i, j}, \\ \end{array}
$$

and

$$
\begin{array}{l} \operatorname{Var} \left[ A _ {i} \right] = \frac {(\varepsilon N) ^ {2}}{n} \sum_ {r = 0} ^ {\log (\sqrt {n} / \varepsilon)} \frac {2 ^ {2 r}}{(1 - q _ {r}) ^ {2}} \operatorname{Var} \left[ Z _ {i, r} \right] \\ \leq (\varepsilon N) ^ {2} \sum_ {r = 0} ^ {\log (\sqrt {n} / \varepsilon)} 2 ^ {2 r} \frac {q _ {r}}{1 - q _ {r}}. \\ \end{array}
$$

So as long as we set $q _ { r } \leq 1 / 2 ^ { 3 r + 1 }$ , we can bound $\mathrm { V a r } [ A _ { i } ]$ by $O ( ( \varepsilon n ) ^ { 2 } )$ , as desired. The cost for each $a _ { i , j } [ r ] = 1$ is thus $O ( \log ( 1 / q _ { r } ) ) = O ( r )$ bits. Since each ai,j [r] = 1 represents 2r √εN $a _ { i , j } [ r ] = 1$ $2 ^ { \bar { r } } { \frac { \dot { \varepsilon } { \dot { N } } } { \sqrt { n } } }$ n copies of an item, the amortized cost for every $\textstyle { \frac { \varepsilon N } { \sqrt { n } } }$ copies is $O ( r / 2 ^ { r } ) = O ( 1 )$ bits. Therefore, the total communication cost is $O ( \sqrt { n } / \varepsilon )$ bits.

Theorem 5.3: When sampling with $g _ { 1 }$ , the communication cost can be made to $O ( \sqrt { n } / \varepsilon )$ bits.

Sampling with $\mathbf { \mathit { g } _ { 2 } . } _ { \mathbf { \mathit { i } _ { \delta } } }$ Because of its non-linear feature, the term $Y _ { i , j } / g _ { 2 } ( Y _ { i , j } )$ will depend on the actual value of $x _ { i , j }$ when sampling with $g _ { 2 }$ , so it is more difficult to save bits. In the following, we show how to combine $g _ { 1 }$ and $g _ { 2 }$ to reduce the communication cost to $\begin{array} { r } { O \left( o p t ( \bar { I _ { \mathbf { \theta } } } ) \log ^ { 2 } \left( \frac { \sqrt { k } } { \varepsilon \cdot o p t ( I ) } \right) \right) } \end{array}$ bits, which is better than using either $g _ { 1 }$ alone or $g _ { 2 }$ alone.

We observe that the estimator Yi = Pnj=1 g2(Y ) $\begin{array} { r } { Y _ { i } = \sum _ { j = 1 } ^ { n } \frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , j } ) } } \end{array}$ Yi,j is itself another a frequency estimation problem, when we consider $\frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , j } ) }$ as the local count of item i at node $j .$ So if $Y _ { i }$ estimates $y _ { i }$ well and we can estimate $Y _ { i }$ well, we will be estimating yi well. To estimate $Y _ { i , \ast }$ we simply run the sampling algorithm with $g _ { 1 }$ on the $\frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , j } ) } \mathrm { ~ ^ { , } s , i . e . ~ }$ Yi,j , we sample each $\frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , j } ) }$ with probability $g _ { 1 } \left( \frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , j } ) } \right)$ and then encode the sampled items into Bloom filters as above.

Let $T _ { i }$ be the estimator thus obtained. It is clear that it is an unbiased estimator. Its variance, by the law of total variance, is

$$
\begin{array}{l} \operatorname{Var} \left[ T _ {i} \right] = \mathbf {E} \left[ \operatorname{Var} \left[ T _ {i} \mid Y _ {i} \right] \right] + \operatorname{Var} \left[ \mathbf {E} \left[ T _ {i} \mid Y _ {i} \right] \right] \\ \leq O ((\varepsilon N) ^ {2}) + (\varepsilon N) ^ {2} = O ((\varepsilon N) ^ {2}). \\ \end{array}
$$

Now we analyze the cost of this algorithm. First of all, since

$$
\mathbf {E} \left[ \sum_ {i, j} \frac {Y _ {i , j}}{g _ {2} (Y _ {i , j})} \right] = \mathbf {E} \left[ \sum_ {i} y _ {i} \right] = N,
$$

the $\frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , j } ) } \mathrm { \mathrm { ^ { * } s } }$ form exactly another instance of the frequency estimation problem with the same $N , n , \varepsilon$ (albeit in expectation), so its cost is no more than $O ( \sqrt { n } / \varepsilon )$ bits. To see the real improvement, the key observation is that overall there are only $o p t ( I )$ non-zero $\frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , i } ) } \mathrm { \bar { s } } .$ Yi,j whereas there are much more non-zero local counts in the original problem. When encoding a non-zero $\frac { Y _ { i , j } } { g _ { 2 } ( Y _ { i , j } ) }$ , we write it in the form of (5) and spend $O ( r )$ bits for every $a _ { i , j } [ r ] = 1$ . This is $O ( \log ^ { 2 } { a _ { i , j } } )$ bits. (Note that we cannot use the charging argument as in Theorem 5.3 because here we need to bound the cost in terms of $o p t ( I ) . )$ Thus the total number of bits required is

$$
\begin{array}{l} \sum_ {i, j, a _ {i, j} \neq 0} \log^ {2} a _ {i, j} \leq o p t (I) \log^ {2} \left(\frac {\sum_ {i , j} a _ {i , j}}{o p t (I)}\right) \\ { = } { o p t ( I ) \log ^ { 2 } \left( \frac { \sqrt { n } } { \varepsilon \cdot o p t ( I ) } \right) , } \\ \end{array}
$$

where equality holds when all the $\boldsymbol { a } _ { i , j } \mathrm { \widetilde { s } }$ are equal.

Theorem 5.4: When sampcation cost can be made to $g _ { 2 }$ $\begin{array} { r } { O \left( o p t ( I ) \log ^ { 2 } \left( \frac { \sqrt { n } } { \varepsilon \cdot o p t ( I ) } \right) \right) } \end{array}$

Remarks: When $\begin{array} { r l r } { n } & { { } > } & { 1 / \varepsilon ^ { 2 } } \end{array}$ as argued in Section III we should sample the g2(Yi,j) ’s $\frac { Y _ { i } , \bar { j } } { g _ { 2 } ( Y _ { i } , j ) } \mathrm { \large ^ { 3 } s }$ Yi,j b y uniform sampling, which is better than using $g _ { 1 }$ So the bound in the theorem above should be O opt(I) log2  min{√n/ε,1/ε2}opt(I)  $\begin{array} { r } { O \left( o p t ( I ) \log ^ { 2 } \left( \frac { \operatorname* { m i n } \{ \sqrt { n } / \varepsilon , 1 / \varepsilon ^ { 2 } \} } { o p t ( I ) } \right) \right) } \end{array}$ , to be more precise.

# VI. SIMULATION RESULTS

We generated a data set with $u = 1 0 , 0 0 0$ items with their frequencies following the Zipf distribution, $\mathrm { i . e . }$ , the i-th item has a frequency $y _ { i } \propto 1 / i$ . We make the total count of all items to be $N = 1 0 ^ { 9 }$ . This represents a heavy-tail distribution that is typical in many real-world applications. Then for each item we randomly split its global count to $n = 1 0 0 0$ nodes.

a) Sampling functions.: We We first compared the performance of the three sampling functions: $g _ { 0 } ( x ) =$ $x / ( x + d )$ proposed in [21], and the two functions $g _ { 1 }$ and $g _ { 2 }$ proposed in this paper. The purpose of this comparison is two-fold: 1) we would like to see how large the gap is between worst-case optimality and instance optimality on a typical data set; and 2) directly sampling with these functions without using the techniques of Section V is extremely simple and this might be desirable in some implementations.

We have tested with varying error parameters (d for $g _ { 0 }$ and ε for $g _ { 1 } , g _ { 2 } )$ and plotted the results in Figure 1 (the three dashed lines). Each data point in the plot is the result of 100 repeated runs with the same parameter. The $y -$ coordinate is the average cost (in terms of bytes, where each (item, count) pair is counted as 8 bytes) over the 100 runs. For each of the top-100 frequent items, we estimate its frequency and compute the variance of the 100 runs. Then we take the maximum variance of the 100 items as the x-coordinate. The reason for looking at the worst variance is that our goal is to estimate the frequency of every item reasonably well. From the plot we see that $g _ { 2 }$ is generally 2 to 3 times cheaper than $g _ { 1 }$ for achieving the same variance, and $g _ { 1 }$ is 2 to 3 times cheaper than $g _ { 0 }$ (note the log scale on y). So the difference is not as extreme as in the example we gave in the beginning, but we think we are happy to see this improvement on such a typical data set.

![](images/d0147d2e2f306d2f47a71f367c7764b0c702b18bf2413cea3b762a757fb0eb73.jpg)



Fig. 1. Simulation results for different sampling functions (dashed lines) and for various algorithms based on Bloom filters (solid lines).

b) Combining with Bloom filters.: We have implemented our algorithm of using $g _ { 1 }$ with Bloom filters and the algorithm of using $g _ { 1 } , g _ { 2 }$ together with Bloom filters. In the Bloom filters, we used the simple hash functions $h ( x ) \ = \ ( a x ^ { 2 } + b x + c )$ mod $p$ where p is a large prime, while each node uses random $a , b , c$ generated independently.

The results are also plotted in Figure 1 (the solid lines). We can see that the use of Bloom filters has reduced the cost of $g _ { 1 }$ by almost a factor of 10. As seen before, sampling with $g _ { 2 }$ is more difficult to combine with Bloom filters, and as a result, the improvement is not as dramatic. The end result is that the two algorithms performed quite similarly. For instance, both of them transmitted $1 . 5 \times 1 0 ^ { 4 } \approx 1 5 \mathrm { K }$ bytes to estimate the counts for the top-100 items with a maximum standard deviation of $1 0 ^ { 6 }$ , which corresponds to $\varepsilon = 0 . 0 0 1$ , a typical error as suggested in [6]. Note that the raw data has roughly $n u = 1 0 ^ { 7 }$ (item, count) pairs, which amounts to 80M of data.

We also did our best-effort implementation of the algorithm of [21], which heuristically improves the bare use of $g _ { 0 }$ . We followed their description and optimized two sets of parameters. This gave the two data points in Figure 1, which are roughly 3 times worse than our algorithms. It is possible to tune the parameters to obtain other cost-variance tradeoffs, but it is doubtful that there exists a point on its tradeoff curve where it is better than ours.

We also generated data sets with different distributions to test the performance of the algorithms. We set the frequency of i-th item $y _ { i } \propto ( 1 / i ) ^ { \alpha }$ (the general definition of the $\mathrm { Z i p f ) }$ , then by varying the value of α, we get different distributions. The Simulation results for different α’s are plotted in Figure 2. Here we also set $u = 1 0 , 0 0 0$ and $N = 1 0 ^ { 9 }$ , and for each item we randomly split its global count to $n = 1 0 0 0$ nodes.

# VII. RELATIVE ERRORS

Here we briefly discuss how to guarantee a $( p , \varepsilon )$ - error, i.e., estimating every $y _ { i } ~ \ge ~ p N$ with variance $( \varepsilon y _ { i } ) ^ { 2 }$ . First, it is known [11] that a uniform sample of size $O ( 1 / \varepsilon ^ { 2 } p )$ achieves this guarantee. Next we see if the general sampling framework can bring any improvement. Recall that the sampling function of [21], $g ( x ) = x / ( x + d )$ , has a variance of $\mathrm { V a r } [ Y _ { i } ] = d y _ { i }$ . We need $d y _ { i } = ( \varepsilon y _ { i } ) ^ { 2 }$ , namely, $d = \varepsilon ^ { 2 } y _ { i }$ , for all $y _ { i } \geq p N$ . So we need to set $d = \varepsilon ^ { 2 } p N$ , which implies that the cost could be $O ( N / d ) = O ( 1 / \varepsilon ^ { 2 } p )$ .

Now consider the linear sampling function $g ( x ) =$ $x / a$ for some $a$ . From (3) in the proof of Theorem 3.1 we have $\mathrm { V a r } [ Y _ { i } ] = a y _ { i } - y _ { i } ^ { 2 } / n$ . Thus we need $a y _ { i } - y _ { i } ^ { 2 } / n \leq$ $( \varepsilon y _ { i } ) ^ { 2 }$ , namely $a \leq ( \varepsilon ^ { 2 } + 1 / n ) y _ { i }$ for all $y _ { i } \geq p N$ . So it suffices to set $a = ( \varepsilon ^ { 2 } + 1 / n ) p N$ , which means that the cost is O(N/a) = O  1(ε2+1/n)p  $\begin{array} { r } { O ( N / a ) = O \left( \frac { 1 } { ( \varepsilon ^ { 2 } + 1 / n ) p } \right) } \end{array}$ . This, again, is better than $O ( 1 / \varepsilon ^ { 2 } p )$ when $\dot { n } \ll 1 / \varepsilon ^ { 2 }$ .

However, the sampling function $g _ { 2 }$ is tailored for the absolute error. It remains an interesting problem to see if there is an instance-optimal sampling function for $( p , \varepsilon )$ - errors.

![](images/1f2d668f1321de0ef659e7eda3089ff2d8a0101c220ff2dd6c9f7a6d78b5b9c0.jpg)



![](images/dc42e73327e5aa80db8c5fe0c9099aef75ae85703714529dbc056b7d01febe01.jpg)



![](images/00ab0169b5e7ee62d289de3224be3b99e49a04917db21bac971086b041a23160.jpg)



Fig. 2. Simulation results for different α’s.

# VIII. REMARKS AND OPEN PROBLEMS

In this paper we have designed worst-case optimal and instance-optimal sampling algorithms for the distributed frequency estimation problem. However, we need to emphasize that the optimality of our algorithms holds only within the sampling framework defined in Section I. Theoretically, it is an intriguing open question to determine the (worst-case) complexity of the problem with no restrictions on the way how the algorithm works. This could be a difficult problem, since even the deterministic complexity is not understood yet. Note that, however, instance-optimality will not be possible to achieve if we do not have any restrictions on the algorithm, since we can design a “wild guessing” algorithm that just outputs the result directly if the input is the one being guessed, while falls back to a naive algorithm on all other inputs. No reasonable algorithm can beat this algorithm on that particular input.

# REFERENCES

[1] http://en.wikipedia.org/wiki/bloom filter.   
[2] B. Aronov, S. Har-Peled, and M. Sharir. On approximate halfspace range counting and relative epsilonapproximations. In Proc. Annual Symposium on Computational Geometry, pages 327–336, 2007.   
[3] B. Babcock and C. Olston. Distributed top-k monitoring. In Proc. ACM SIGMOD International Conference on Management of Data, 2003.   
[4] P. Cao and Z. Wang. Efficient top-k query calculations in distributed networks. In Proc. ACM Symposium on Principles of Distributed Computing, 2004.   
[5] G. Cormode, M. Garofalakis, S. Muthukrishnan, and R. Rastogi. Holistic aggregates in a networked world: Distributed tracking of approximate quantiles. In Proc. ACM SIGMOD International Conference on Management of Data, 2005.   
[6] G. Cormode and M. Hadjieleftheriou. Finding frequent items in data streams. In Proc. International Conference on Very Large Data Bases, 2008.   
[7] G. Cormode and S. Muthukrishnan. An improved data stream summary: The count-min sketch and its applications. Journal of Algorithms, 55(1):58–75, 2005.

[8] J. Dean and S. Ghemawat. MapReduce: Simplified data processing on large clusters. Communications of the ACM, 51(1), 2008.   
[9] R. Fagin, A. Lotem, and M. Noar. Optimal aggregation algorithms for middleware. Journal of Computer and System Sciences, 66:614–656, 2003.   
[10] M. Greenwald and S. Khanna. Power conserving computation of order-statistics over sensor networks. In Proc. ACM Symposium on Principles of Database Systems, 2004.   
[11] Y. Li, P. M. Long, and A. Srinivasan. Improved bounds on the sample complexity of learning. Journal of Computer and System Sciences, 62:516–527, 2001.   
[12] G. Manku and R. Motwani. Approximate frequency counts over data streams. In Proc. International Conference on Very Large Data Bases, 2002.   
[13] A. Metwally, D. Agrawal, and A. E. Abbadi. An integrated efficient solution for computing frequent and top-k elements in data streams. ACM Transactions on Database Systems, 2006.   
[14] S. Michel, P. Triantafillou, and G. Weikum. KLEE: A framework for distributed top-k query algorithms. In Proc. International Conference on Very Large Data Bases, 2005.   
[15] B. Patt-Shamir and A. Shafrir. Approximate distributed top-k queries. Distributed Computing, 21:1–22, 2008.   
[16] E. Porat. An Optimal Bloom Filter Replacement Based on Matrix Solving. Computer Science–Theory and Applications, 5675:263–273, 2009.   
[17] N. Shrivastava, C. Buragohain, D. Agrawal, and S. Suri. Medians and beyond: New aggregation techniques for sensor networks. In Proc. International Conference on Embedded Networked Sensor Systems, 2004.   
[18] V. N. Vapnik and A. Y. Chervonenkis. On the uniform convergence of relative frequencies of events to their probabilities. Theory of Probability and its Applications, 16:264–280, 1971.   
[19] K. Yi and Q. Zhang. Optimal tracking of distributed heavy hitters and quantiles. In Proc. ACM Symposium on Principles of Database Systems, 2009.   
[20] H. Zhao, A. Lall, M. Ogihara, and J. Xu. Global iceberg detection over distributed data streams. In Proc. IEEE International Conference on Data Engineering, 2010.   
[21] Q. Zhao, M. Ogihara, H. Wang, and J. Xu. Finding global icebergs over distributed data sets. In Proc. ACM Symposium on Principles of Database Systems, 2006.