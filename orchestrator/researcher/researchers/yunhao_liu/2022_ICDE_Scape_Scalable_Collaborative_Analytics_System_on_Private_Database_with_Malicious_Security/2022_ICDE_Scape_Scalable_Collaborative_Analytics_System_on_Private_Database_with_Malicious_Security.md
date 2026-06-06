# Scape: Scalable Collaborative Analytics System on Private Database with Malicious Security

Feng Han $^{*}$ $^{\dagger}$ , Lan Zhang $^{*}$ , Hanwen Feng $^{\dagger}$ , Weiran Liu $^{\dagger}$ , and Xiangyang Li $^{*}$

\*University of Science and Technology of China, †Alibaba Group

\*hf1996@mail.ustc.edu.cn, {\*zhanglan03, xiangyang.li}@gmail.com, †{fenghanwen.fhw, weiran.lwr}@alibaba-inc.com

Abstract—Many data applications can be facilitated or even spawned by joint analysis on databases held by different owners, but privacy concerns are currently the biggest hindrance. Though a practical privacy-preserving collaborative database analytics system is strongly desired, existing approaches do not support efficient queries for several essential SQL operators such as the general join, especially on large databases.

In this paper, we propose, analyze, and implement Scape, a Scalable Collaborative Analytics system on Private databases with malicious security. In Scape, databases from different parties are secretly shared to three non-colluding computing parties. Users can perform various SQL queries (including fully functional Join, Group by, Aggregation, etc.) on shared databases, and all entities learn nothing beyond their priori knowledge during the whole execution even when they deviate from protocols. At the heart of Scape lies several asymptotically efficient SQL protocols. Particularly, our general join protocol has $O(n \log^{2} n + m)$ communication/computation cost when joining two tables with $O(n)$ rows to a table with $O(m)$ rows, significantly outperforming the state-of-the-art approach with $O(n^{2})$ cost. The benchmark results confirm the advantages of Scape, which is up to $25\times$ faster than the baseline.

# I. INTRODUCTION

Analyzing data from multiple sources can benefit or even spawn many applications such as medical studies, online advertising, credit investigation, and financial services. However, as the enactment of many privacy regulations and laws and the increasingly fierce competition among IT companies, many data owners are not legally allowed or willing to directly share their data with others. How to effectively perform collaborative analysis of different owners' databases without revealing private data to other parties becomes an urgent problem, which has received a lot of attention from academia and industry.

Secure Multi-party Computation (MPC) is a cryptographic tool enabling privacy-preserving analytics. At a high level, many MPC mechanisms involve secret sharing schemes $[1]$ and protocols manipulating the shares. A secret sharing scheme can split private data x into multiple shares in a recoverable manner such that any subset of no more than a threshold number of shares reveals nothing about x. Parties holding these shares can jointly execute a secure protocol for a specific functionality f and obtain shares of $f(x)$ without learning extra information. The value of $f(x)$ can be recovered from shares when needed. With secure protocols for designated analytics tasks, such a framework enables data owners to conduct collaborative analytics without revealing any extra information about their data beyond the results.

Though MPC provides an appealing security guarantee, directly using general MPC techniques $[2]$ , $[3]$ is rather expensive and currently cannot provide practical solutions. Most existing collaborative analytics systems leverage other techniques to improve the performance of MPC. However, they either rely on trusted third parties which have access to the plaintext data (like Conclave $[4]$ ) or only ensure controlled information leakage by using differential privacy $[5]$ (such as Shrinkwrap $[6]$ and SAQE $[7]$ ). Meanwhile, there are systems (like TrustedDB $[8]$ , EnclaveDB $[9]$ and ObliDB $[10]$ ) using trusted hardware to get rid of MPC, which, however, require different trust assumptions and are vulnerable to various attacks (e.g., side-channel attack).

Very few works, including SMCQL [11], Senate [12], and Secrecy [13], present MPC-based collaborative analytics, which ensure no information leakage without relying on trusted third parties or trusted hardware. Those works have introduced various optimizations and significantly improved the performance compared with directly using general MPC. Nonetheless, when the databases to be analyzed are moderately large (say, having around 1 million rows), their performance is still cumbersome, inheriting from the high asymptotic complexity of their protocols for some usual operations. Meanwhile, SMCQL and Secrecy only achieve semi-honest security, assuming that corrupted parties faithfully follow the prescribed protocol. In practice, participants can easily carry out malicious attack by deviating from the protocol. We indeed need a stronger guarantee of malicious security to defend against such attacks. It is more challenging to achieve efficient collaborative analytics with malicious security since achieving malicious security usually introduces extra overhead.

# A. Scape Overview

Towards more efficient and secure multi-party data analytics, we propose Scape, a Scalable Collaborative Analytics system on Private databasE with malicious security.

Architecture and Security Model. Similar to the existing collaborative analytics application $[13]$ , $[15]$ , Scape involves three roles: data owners, computing parties, and clients. Data owners have private data, while computing parties answer statistical questions from clients on all databases. Scape contains three computing parities and puts no limitation on the numbers of data owners and clients, and data owners can also act as the computing parties as in $[13]$ .

At a high level, Scape works as follows: (1) All data owners secretly share their datasets $X$ to three computing parties; (2)

<table><tr><td rowspan="2" colspan="2">Operators</td><td>SMCQL [11] Senate [12]</td><td colspan="2">Secrecy [13]</td><td colspan="2">Scape</td></tr><tr><td>Comm. cost (bit)</td><td>Comm. cost (bit)</td><td>Rounds</td><td>Comm. cost (bit)</td><td>Rounds</td></tr><tr><td rowspan="2">Group by aggregation</td><td>Total</td><td> $O(n \log^2 n)$ </td><td> $O(n \log^2 n)$ </td><td> $O(n)$ </td><td> $O(n \log^2 n)$ </td><td> $O(\log^2 n)$ </td></tr><tr><td>After sorting</td><td> $O(n)$ </td><td> $O(n)$ </td><td> $O(n)$ </td><td> $O(n)$ </td><td> $O(\log n)$ </td></tr><tr><td rowspan="2">Join</td><td>non-unique keys</td><td> $O(n^2)$ </td><td rowspan="2"> $O(n^2)$ </td><td rowspan="2"> $O(1)$ </td><td> $O((n \log^2 n + m))$ </td><td> $O(\log^2 n)$ </td></tr><tr><td>unique keys</td><td> $O(n \log^2 n)^*$ </td><td> $O(n \log n)$ </td><td> $O(\log n)$ </td></tr><tr><td rowspan="2">Semi-join</td><td>non-unique keys</td><td> $O(n^2)$ </td><td rowspan="2"> $O(n^2)$ </td><td rowspan="2"> $O(\log n)$ </td><td> $O((n \log^2 n))$ </td><td> $O(\log^2 n)$ </td></tr><tr><td>unique keys</td><td> $O(n \log^2 n)^*$ </td><td> $O(n \log n)$ </td><td> $O(\log n)$ </td></tr></table>

$^{1}$ \* represents that the listed cost is evaluated when inputs are unsorted; If sorted, the cost can be reduced to $O(n \log n)$ .   
2 Senate and Scape achieve malicious security, while SMCQL and Secrecy consider semi-honest security.   
$^{3}$ SMCQL and Senate are built upon Yao’s garbled circuits [14] whose round complexity is $O(1)$ , while their concrete communication/computation cost is higher than that of Scape and Secrecy.

TABLE I: Asymptotic communication/computation comparisons of basic operators. Here n is the number of input rows and m is the output size limitation of Join. We treat the length of the attributes in bits as constant.

A query $Q$ issued by a client will be broadcasted to computing parties; (3) Computing parties coordinately execute a secure protocol converting their shares of the original datasets $X$ into the shares of $Q(X)$ , and send their shares of $Q(X)$ to the client. (4) The client reconstructs the result $Q(X)$ from shares.

In Scape's security model, three computing parties do not collude. The adversary can be malicious, and corrupt at most one computing party. Scape ensures that, during the whole execution, the adversary learns nothing beyond her prior knowledge (including an upper bound on the number of rows in every join result during analytics $^{1}$ ). This security model is known as malicious security with an honest majority [16], and we compare it with that of previous works in Table.II).

<table><tr><td>Systems</td><td>Parties</td><td>Malicious security</td><td>Corrupt number</td></tr><tr><td>SMCQL [11]</td><td>2</td><td> $\times$ </td><td> $\leq 1$ </td></tr><tr><td>Secrecy [13]</td><td>3</td><td> $\times$ </td><td> $\leq 1$ </td></tr><tr><td>Senate [12]</td><td>m</td><td> $\checkmark$ </td><td> $\leq m - 1$ </td></tr><tr><td>Scape</td><td>3</td><td> $\checkmark$ </td><td> $\leq 1$ </td></tr></table>

TABLE II: Security Comparison with existing systems. Scape is strictly more secure than Secrecy but less secure than Senate. SMCQL and Scape are generally incomparable, but Scape's security guarantee is arguably better than that of SMCQL as it is hard to ensure that an adversary is semi-honest.

Example Application Scenario. While Scape works for an arbitrary number of data owners, it particularly fits for the most common scenarios where two data owners want to collaboratively analyze their data. In real-world scenarios, data owners could be any organizations, which may not have the specialized knowledge of MPC. A data security service provider (DSSP) can help them to conduct the analytics via serving as one computing party and deploying Scape protocols on two data owners such that they can act as computing parties as well. It is reasonable to assume that these three parties (two data owners and a DSSP) do not collude. Two data owners naturally do not collude; otherwise, they can directly share their private data to conduct analytics on the plaintext. For a DSSP, collusion harms its reputation and violates regulations.

Supported SQL Operators. Maliciously secure protocols for SQL operators lie at the heart of Scape, and they can be composed to answer clients' queries. Scape provides efficient

$^{1}$ This is caused by general join (see later in this section) and is unavoidable for efficient general join (see Section II for more discussions).

protocols for all SQL operators that were supported in previous MPC-based collaborative analytics [11]–[13], including various types of Join, Select, Order-by, Aggregate, Group-by-aggregation, Distinct. These operators are sufficient for many queries. Other operators can also be supported since we have protocols for Turing complete operations like AND and XOR.

# B. Complexity Summary

The poor asymptotic complexity of protocols for several SQL operators was the major obstacle to a scalable collaborative analytics system. A notable example is the general Equal-Join that joins two relations according to two keys, where both keys could be unique or non-unique. We abbreviate equal-join as Join in the follow-up. For this operator, existing protocols [11]-[13] suffer from $O(n^2)$ communication/computation cost for relations with $O(n)$ rows. When $n$ is large, the protocols are cumbersome.

We design asymptotically efficient protocols for various SQL operators, including general Join (PK-FK join & non-primary-foreign key join), Join on unique keys (PK-PK join), Semi-Join, and Group-by, advancing the state of the art. The asymptotic communication/computation comparisons between our protocols and protocols from previous works (SMCQL [11], Senate [12] and Secrecy [13]) are presented in Table.I.

Notably, we provide the most efficient protocol for general (Semi-)Join, which has $O(n \log^{2} n + m)$ (instead of $O(n^{2})$ ) communication/computation cost and $O(\log^{2} n)$ round complexity. Here m is an upper bound on the number of rows in the joint relation and $m \ll n^{2}$ in most cases. We also reduce the cost of (Semi-)Join on unsorted unique keys from $O(n \log^{2} n)$ to $O(n \log n)$ and reduce the round complexity of Group-by from $O(n)$ (in Secrecy) to $O(\log n)$ (or $O(\log^{2} n)$ for unsorted relations). We remark that shared relations are usually unsorted, particularly after being processed by other operators. We further apply a rich set of optimizations to improve the concrete performances of SQL protocols and optimize the way of composing them to answer user queries, making Scape practical even for large datasets.

# C. Evaluation Summary

We compare Scape with SMCQL, Senate, and Secrecy, showing the improvements of Scape in concrete performances. We re-implemented Secrecy in our environment, and observe that Scape is up to $25\times$ faster than Secrecy when answering most SQL queries on 65.5K-row datasets, while Secrecy provides semi-honest security and Scape achieves malicious security. To answer three queries in [11], Scape on 1K-row datasets is $1.05 \times \sim 10 \times$ faster than SMCQL on 50-row datasets. We take Senate's reported results on specific queries they chose and evaluate Scape with the same queries with less computation and network resources (than those in their experiments). Compared with Senate on 3.2K-row datasets, Scape on 16K-row datasets costs $2.6 \times \sim 89 \times$ less time.

![](images/8998d4ac76e3f1e22b82365689aaa1051d3ab4dd52e9697d98a3af7f9c1b156c.jpg)



Fig. 1: Scape's technique overview.

We further benchmark Scape with real-world queries selected from TPC-H benchmark $[17]$ in both WAN and LAN settings. In the LAN setting (1Gbps bandwidth and 1.7ms RTT), all queries can be processed within 1min on 32K-row datasets (or within 20min on 512K-row datasets). In the WAN setting (100Mbps and 20ms RTT), the time cost is only slightly $(2.27\times\sim2.64\times)$ larger, demonstrating the practicability of Scape in real-world applications.

# II. TECHNIQUE OVERVIEW

We give a high-level overview of our techniques in Fig.1. We first present the steps of the system design.

Step 0: baseline solution from general MPC. There are basic (Turing complete) MPC protocols for boolean operations (AND and XOR) [16], [18] and arithmetic operations (ADD and MUL) [19], [20]. SQL operators can be implemented by circuits composed of these operations.

Protocols for circuits are usually tailored for the underlying secret sharing scheme, so the latter's choice heavily affects the overall performance. We choose the $(3,2)$ -replicated sharing scheme [16], since it enables the most efficient protocols for circuits, which can be composed to implement most SQL operators. This scheme splits private data into three shares, and any two of three shares can be used to recover the original private data. Leveraging this scheme, Scape is designed to have three non-colluding computing parties hold three shares. We use the maliciously secure protocols for circuits provided in the ABY $^{3}$ [3] framework.

At this stage, SQL operators are naively implemented using basic circuits. Along the way, the communication/computation cost of a protocol, on rough terms, is proportional to the size of circuits, which can be huge, even quadratic in the input size, without specific optimizations.

Step 1: specific optimization for Join. Various Join are essential to collaborative analytics. However, the conventional way of implementing Join (used in SMCQL and Secrecy) for $O(n)$ -row relations needs $O(n^{2})$ -size circuits, significantly affecting the performances.

PK-PK join is closely related to the context of circuit-based Private Set Intersection (PSI). Recent advances in circuit PSI, which take plaintext data as inputs and outputs (shared) Join results, have significantly improved the performance. In practice, however, a more proper execution flow would be letting data owners prepare the shared inputs before actual operations; thus Join usually applies to shared data, and most PSI approaches won't apply there. We follow the sort-compare-shuffle (SCS) solution [21], which is also used in Senate [12]. Specifically, if two input relations are pre-sorted, they can be merged in the sorted order using an $O(n \log n)$ -size circuit (provided in Bitonic sorter [22]). After the merge operation, equal keys become adjacent and can be found via an $O(n)$ -size circuit. If two input relations are unsorted, the circuit size of Bitonic sorter is increased to $O(n \log^2 n)$ .

It is more challenging to design an efficient protocol for general Join where keys might be non-unique. For PK-PK Join, equal keys only occur when two keys belong to different relations, while for Join on non-unique keys, equal keys can be from the same relation without subsequent processing. If we follow the same approach above, we will soon get into an obstacle when finding equal keys while obliviously indicating their original belongings. The naive solution needs an $O(n^{2})$ -size circuit. It was an open problem to design an efficient circuit for this task until the very recent work proposed by Krastnikov et al. [23]. They designed an elegant procedure that computes some global parameters of relations (including the number of equal keys w.r.t. each key) in the beginning. Using these parameters can reduce the cost of subsequent procedures. Its total circuit size is $O(m \log^{2} m)$ , where m is the upper bound on the number of rows in the Join result and $m \geq n$ . Our general Join can be considered as the (first also optimized) implementation of this algorithm on shared data with the complexity of $O(n \log^{2} n + m)$ (instead of $O(m \log^{2} m)$ ). Our improvements come from the technique we introduce in the following steps, and the detailed comparison between our general Join protocol and [23] will be presented in Section IV.

The execution flow of Krastnikov et al.'s circuit depends on the upper bound m. Therefore, in the secret-shared version of Krastnikov et al.'s solution, m must be revealed to computing parties. We note this leakage is indeed inevitable for any efficient solution. Without a meaningful upper bound, computing parties have to store enough secret-shared data for representing all possible joint relations of maximum size $O(n^{2})$ . Nonetheless, m can be trivially set as the total number of rows in two relations when considering Join on a unique key and a non-unique key (PK-FK join). For non-primary-foreign key join, data owners can estimate an upper bound m in the beginning and send it to computing parties who would abort the protocol if the real value exceeds the estimated value.

At this stage, by implementing Join with optimized circuits, the complexity of communication/computation is reduced. In the following steps, we further improve the concrete performance and reduce the round complexity.

Step 2: replacing oblivious sorting. Oblivious sorting is widely used in MPC implementations of SQL operators. However, the most efficient oblivious sorting algorithm/protocol [22] is still expensive, requiring $O(n \log^{2} n)$ communication/computation cost. Luckily, after analyzing the protocols for “sorting-built-in” operators, e.g., Join and Semi-join, we have a main observation:

we do not always need sorting when we are using it.

Specifically, we generalize purposes of using oblivious sorting as to re-order a shared relation according to some shared order, while the order can be determined through sorting the “key” vector. This generalization immediately allows us to reduce the cost of sorting in the following two cases.

T0: A permutation-like key vector. We first consider the simplest case where the components of the n-dimension shared key vector $\left[\overrightarrow{p}\right]$ are pairwise-distinct values in $[1,n]$ . Notice that $\left[\overrightarrow{p}\right]$ essentially defines a permutation of size n and there are efficient semi-honest secure oblivious permutation protocols [24], [25] achieving $O(n)$ communication cost and $O(1)$ round complexity. So, we can directly leverage the permutation protocol to achieve this purpose, thus circumventing oblivious sorting. We further strengthen the protocols into maliciously secure ones as presented in Section VI-A.

T1: An arbitrary key vector. For the most general case that the values of shared key vector $\left[\overrightarrow{p}\right]$ can be arbitrary, we can sort $\left[\overrightarrow{p}\right]$ alone (instead of the whole relation), and generate a shared permutation $\left[\pi\right]$ representing a sort of $\left[\overrightarrow{p}\right]$ . Then, we just need to permute the relation according to $\left[\pi\right]$ .

We further abstract specific cases in SQL operators into two functions and design efficient protocols to generate the permutation without using full oblivious sorting.

T2: Distributing items according to a “sparse” key vector. In cases (such as the join circuit [23]), we need to re-order and distribute the components of an n-dimension relation $\left[\overrightarrow{x}\right]$ into an m-dimension relation, according to a “sparse” n-dimension key vector $\left[\overrightarrow{p}\right]$ whose components are pairwise-distinct values in $[1,m]$ (n < m), such that the result relation $\left[\overrightarrow{y}\right]$ satisfying $y_{p_{i}} = x_{i}$ . The method in [23] is to first obliviously sort the relation and then use another $O(m \log m)$ -size circuit for padding. Our idea is to extend $\left[\overrightarrow{p}\right]$ into a shared permutation $\left[\pi\right]$ of size m with which we can achieve the distribution goal through the efficient permutation protocol.

Given a random shared $m$ -size permutation $\llbracket \omega \rrbracket$ , assume we can somehow transform $\llbracket p_i \rrbracket$ (resp. $\llbracket \omega_j \rrbracket$ ) into another shared value $\llbracket p_i' \rrbracket$ (resp. $\llbracket \omega_j' \rrbracket$ ), such that $p_i'$ (resp. $\omega_j'$ ) does not leak information about $p_i$ (resp. $\omega_j$ ), while $p_i' = \omega_j'$ iff $p_i = \omega_j$ . Then, the parties can open and compare the plaintext $(\overrightarrow{p'}, \omega')$ and re-order $\llbracket \omega \rrbracket$ into $\llbracket \pi \rrbracket$ , such the first $n$ elements of $\llbracket \overrightarrow{p'} \rrbracket$ and $\llbracket \pi \rrbracket$ are equal. The transformation function above can be realized with soPRF (to be introduced in Section III), and details are in Section IV-A4.

T3: Matching equal components. In existing PK-PK join algorithm for unsorted relations (i.e. SCS algorithm), after two relations are vertically concatenated, a crucial step is to obliviously sort the relation according to the key vector. This step is to make equal components become neighbors, so we can obtain the joint relation via comparing neighbors.

We observe that, matching the equal components of two vectors $\left[\overrightarrow{x^{\prime}}\right]$ and $\left[\overline{y}\right]$ can be achieved by comparing their transformed values $\overrightarrow{x^{\prime}}$ and $\overrightarrow{y^{\prime}}$ in a similar way to T2. But this approach leaks the joint relation size to computing parties [26]. This undesired leak can be avoided by sending $\overrightarrow{x^{\prime}}$ and $\overrightarrow{y^{\prime}}$ to two parties separately; they then sort the vectors and permute the corresponding relations. Finally, the target relation can be obtained by applying a “partial” SCS algorithm (with the cost of $O(n\log n)$ ) to the two “sorted” relations. The additional design ensuring malicious security is in Section V-A1.

Step 3: reducing the round complexity of traversal. The oblivious traversal is the fundamental procedure to general (Semi-)Join protocol and group-by. At a high level, it takes as input a shared relation $\llbracket T\rrbracket = ((\llbracket x_1\rrbracket, \llbracket y_1^{\mathrm{b}}\rrbracket), \ldots, (\llbracket x_n\rrbracket, \llbracket y_n^{\mathrm{b}}\rrbracket))$ , where each row $(x_i, y_i^{\mathrm{b}}) \in \{0, 1\}^* \times \{0, 1\}$ . It outputs a shared vector $\llbracket \overrightarrow{z}\rrbracket = (\llbracket z_1\rrbracket, \ldots, \llbracket z_n\rrbracket)$ , where $z_i = h(z_{i-1}, (x_i, y_i^{\mathrm{b}}))$ for a specific iteration function $h$ . A straightforward implementation would compute $\llbracket z_i\rrbracket$ after having $\llbracket z_{i-1}\rrbracket$ , resulting in a circuit with $O(n)$ depth, or a protocol with $O(n)$ -rounds. As the dimension $n$ can be very large for collaborative analytics, this round complexity becomes the bottleneck of performance.

Our goal is to reduce the circuit depth for the traversal procedure. All traversal procedures in Scape have the form:

$$
z _ {i} = h (z _ {i - 1}, (x _ {i}, y _ {i} ^ {\mathsf {b}})) = \left\{ \begin{array}{l} \theta (z _ {i - 1}, x _ {i}), \text {if} \phi (z _ {i - 1}, x _ {i}) \& y _ {i} ^ {\mathsf {b}} \\ x _ {i}, \text {otherwise.} \end{array} \right.
$$

where $\theta(z_{i-1}, x_i)$ can either be an identity function, i.e. $\theta(z_{i-1}, x_i) = z_{i-1} + x_i$ , or a function outputting the first input, i.e., $z_{i-1}$ ; $\phi$ can either be an always-true predication or a comparison predication, i.e., outputting $(z_{i-1} > x_i)$ (or $(z_{i-1} < x_i))$ ; $\overrightarrow{y}^{\mathrm{b}}$ is called the group indicator array.

It is known that, when a function f is associative, i.e., $f(f(f(x_{1},x_{2},),x_{3}),x_{4}) = f(f(x_{1},x_{2}),f(x_{3},x_{4}))$ , traverse f on a vector can be done in parallel. This paradigm has been widely used in distributed computation frameworks like MapReduce [27]. Our intuition here is to transform a non-associative iteration function h into an “equivalent” associative function. To this end, we introduce an additional indicator array $\overrightarrow{s}^{b}$ so that h can be transformed to an equivalent associative function g:

$$
(z _ {i}, s _ {i} ^ {\mathsf {b}}) = g ((z _ {i - 1}, s _ {i - 1} ^ {\mathsf {b}}), (x _ {i}, y _ {i} ^ {\mathsf {b}})),
$$

where $z_{i}=h(z_{i-1},(x_{i},y_{i}^{\mathsf{b}}))$ and $s_{i}^{\mathsf{b}}=s_{i-1}^{\mathsf{b}}\cdot y_{i}^{\mathsf{b}}$ .

We generalize this intuition into a classical structure of concurrent computation called parallel prefix network [28] and reduce the circuit depth (and thus the round complexity) into $O(\log n)$ . More details are presented in Section VI-B.

Step 4: optimizing compositions for client queries. A complex query can usually be realized through different compositions of SQL operators, and the costs could be different. Particularly, in Scape, many operators have more efficient implementations for sorted inputs, while some operators have built-in sorting procedures. Intuitively, if we place those “sorting-sensitive” operators after “sorting-built-in” operators, we can save some sorting procedures. Moreover, we notice that performing a complete Join is unnecessary for queries that do not include non-linear operations between the attributes from two relations, and several operations turn out to be redundant. Based on these observations, we develop a cost model that measures the cost of different compositions and gives the optimal one. More details are presented in Section V-B.

Notation: $\left[\overrightarrow{y}\right]\leftarrow\mathcal{F}_{\mathrm{perm}}(\left[\pi\right],\left[\overrightarrow{x}^{\prime}\right])$ .
Input: $\left[\pi\right]=\left(\left[\pi(1)\right],\ldots,\left[\pi(n)\right]\right)$ and $\left[\overrightarrow{x}^{\prime}\right]=\left(\left[x_{1}\right],\ldots,\left[x_{n}\right]\right)$ .
Functionality:
1) Abort if the inputs are inconsistent.
2) Generate an array $\overrightarrow{y}$ : $y_{\pi(i)} = x_i$ , for all $i \in [1, n]$ .
3) Secret share $\overrightarrow{y} = \pi^{-1} \cdot \overrightarrow{x}$ to the parties.   
Fig. 2: Ideal functionality of oblivious permutation.

# III. PRELIMINARIES

# A. Notations

We denote $[m, n]$ as the set $\{m, \ldots, n\}$ for $m, n \in \mathbb{N}$ with $m < n$ , $\overrightarrow{x'} = (x_1, \ldots, x_n)$ as an array with length $|\overrightarrow{x'}| = n$ . Given a relation $T$ , we denote $T_i$ as its $i^{\text{th}}$ tuple, $T[v]$ as the array containing all values of the attribute $v$ , and $T_i[v]$ as the $i^{\text{th}}$ value of $T[v]$ . We sometimes use $\mathbf{t} \in T$ as a tuple in $T$ , $\mathbf{t}[v]$ as the value of the attribute $v$ in $\mathbf{t}$ , and $\mathbf{t}[\neg v]$ as the tuple $\mathbf{t}$ without the value $\mathbf{t}[v]$ . We explicitly write $v^{\text{b}}$ if each value of $v$ can only be 0 or 1. We write $\overline{T[v^{\text{b}}]} = (1 - T_1[v^{\text{b}}], \ldots, 1 - T_n[v^{\text{b}}])$ . Specifically, $f^{\text{b}}$ is denote as the validity indicator attribute representing whether the respective tuple is valid. The result of Joining two two relations $L$ and $R$ on the join attribute $k$ is $J = L \bowtie_k R = \{(k, \mathbf{t}_L[\neg k], \mathbf{t}_R[\neg k]) | \mathbf{t}_L \in L, \mathbf{t}_R \in R, \mathbf{t}_L[k] = \mathbf{t}_R[k]\}$ . We denote $\pi : [1, n] \to [1, n]$ as a permutation function, and $\overrightarrow{y} = \pi \cdot \overrightarrow{x'}$ as applying $\pi$ on $\overrightarrow{x'} = (x_1, \ldots, x_n)$ to get $\overrightarrow{y} = (x_{\pi(1)}, \ldots, x_{\pi(n)})$ .

# B. Secret sharing and basic functionalities

Secret Sharing. We use (3,2)-replicated sharing [3] in Scape with three computing parties $P_1, P_2, P_3$ . A secret data $x \in \{0,1\}^k$ is split into three shares $[[x]]_1 = (x_1, x_2), [[x]]_2 = (x_2, x_3), [[x]]_3 = (x_3, x_1)$ with the constraint that $x = x_1 + x_2 + x_3 \mod 2^k$ (we say $[[x]]_i$ is an arithmetic share) or $x = x_1 \oplus x_2 \oplus x_3$ for $x \in \mathbb{Z}_2^k$ (we say $[[x]]_i^{\mathsf{B}}$ is a binary share). Note that any two parties $P_i, P_j$ can reconstruct $x$ from $[[x]]_i, [[x]]_j$ , while any single party $P_i$ learns nothing about $x$ from $[[x]]_i$ . Type conversions between a binary share and an arithmetic share is realized by evaluating the ripple-carry full adder circuit [28]. We may omit the party index and simply write $[[x]]$ to have a uniform description when related operations need to be done for all computing parties.

The parties can locally evaluate ADD circuit $([x] + [y])$ or XOR circuit $([x]^{\mathsf{B}}\oplus [y]^{\mathsf{B}})$ without communication. Evaluating MUL circuit $([x]\times [y])$ or AND circuit $([x]^{\mathsf{B}}\odot [y]^{\mathsf{B}})$ needs one round of communication. The above four operations between a public constant $x$ and a shared value $[y]$ $([y]^{\mathsf{B}})$ can be done locally without communication. To achieve malicious security, the multiplication triple [16] is used to verify the correctness of each MUL (AND) operation without explicitly reconstructing the resulting value. The equality test $(=)$ and comparisons $(<,>,\leq,≥)$ defined in $\mathbb{Z}_{2^k}$ needs $O(\log k)$ rounds and $O(k)$ -bit communication cost for $O(k)$ -bit inputs. Parties can locally generate a random shared value $[[r]]$ with the protocol in [16].

Notation: $\left[\overrightarrow{z}\right]\leftarrow\mathcal{F}_{\mathrm{trav}}(\left[\left[T=(\overrightarrow{x},\overrightarrow{y}^{\mathrm{b}})\right],\theta,\phi,\mathrm{lfPos}\right).$ Input: $|T|=n$ , for $i\in[1,n]$ : $(x_{i},y_{i}^{\mathrm{b}})\in\{0,1\}^{*}\times\{0,1\}$ . $\theta:\{0,1\}^{*}\times\{0,1\}^{*}\to\{0,1\}^{*}$ , $\phi:\{0,1\}^{*}\times\{0,1\}^{*}\to\{0,1\}$ . IfPos is a boolean value.

Functionality:
1) Abort if the inputs are inconsistent.
2) Compute an array $\overrightarrow{z}$ :
• If lfPos is true: $z_{1}=x_{1}$ and for $i\in[2,n]$ :
    a) if $\phi(z_{i-1},x_{i})\&y_{i}^{\mathrm{b}}$ : $z_{i}=\theta(z_{i-1},x_{i})$ .
    b) otherwise: $z_{i}=x_{i}$ • If lfPos is false: $z_{n}=x_{n}$ and for $i\in[1,n-1]$ :
    a) if $\phi(z_{i+1},x_{i})\&y_{i}^{\mathrm{b}}$ : $z_{i}=\theta(z_{i+1},x_{i})$ .
    b) otherwise: $z_{i}=x_{i}$ 3) Secret share $\overrightarrow{z}$ to the parties.   
Fig. 3: Ideal functionality of oblivious traversal. In the follow-up, we mean the case IfPos is true when we refer to traversal, and the case IfPos is false when we refer to traversal in reverse order.

We use $[x]$ to represent the $(2,2)$ -additive share of $x \in \{0,1\}^k$ . That is, $P_i$ has $[x]_i = x_i$ and $P_j$ has $[x]_j = x_j$ with the constraint that $x = x_i + x_j \mod 2^k$ (or $x = x_i \oplus x_j$ ). We denote $\llbracket x \rrbracket \xrightarrow{i,j} [x]$ as converting $\llbracket x \rrbracket$ into $[x]$ between $P_i$ and $P_j$ , and $[x] \xrightarrow{i} \llbracket x \rrbracket$ as converting $[x]$ between $P_{i-1}$ and $P_{i+1}$ into $\llbracket x \rrbracket$ , where $P_{i\pm 1}$ refers to the next (+) or previous (-) party of $P_i$ with wrap around. We use the protocol in [26] to realize such conversions.

Oblivious sorting. Sorting networks such as bitonic sorter provide an in-place, input-independent, and easy-to-parallel way to sort n binary-sharing values in $O(\log^{2}n)$ rounds and $O(n\log^{2}n)$ bits of communication. It takes $O(\log n)$ rounds and $O(n\log n)$ bits of communication to merge two pre-sorted binary-sharing arrays into one n-length sorted array. We denote $sort_{a\uparrow b\downarrow}(T)$ as sorting the relation T by the order of a and then by the order of b, where $\uparrow$ stands for descending order, and $\downarrow$ stands for ascending order.

Shared oblivious PRF. When computing parties share a PRF key and some input values, they can get shares of PRF outputs by securely evaluating the PRF circuit in an MPC manner. This functionality is introduced as shared oblivious PRF (soPRF) in [26]. We denote the functionality by $\mathcal{F}_{\mathrm{soPRF}}$ which on inputs a shared key $[k_{\mathrm{PRF}}]$ and a shared input $[x]$ outputs $[y]$ such that $y = \mathrm{PRF}(k_{\mathrm{PRF}}, x)$ . Instead of AES circuit in [26], we use a more lightweight LowMC [29] circuit which can be evaluated in $O(1)$ rounds with $O(n)$ -bit communication cost.

Permutation generation. Given a shared bit-vector $\llbracket \overrightarrow{v^b}\rrbracket$ , [25] provides a protocol that generates a shared permutation $\llbracket \pi \rrbracket$ representing a stable sort of $\overrightarrow{v^b}$ with $O(1)$ rounds and $O(|\overrightarrow{v^b}|)$ -bit communication cost. We denote this functionality by $\mathcal{F}_{\mathrm{perGen}}$ . If the input is $([1], [0], [1], [0])$ , its (obliviously) stable sort result is $([0], [0], [1], [1])$ by moving $[1]$ on the $1^{\text{st}}$ place to the $3^{\text{rd}}$ place, $[0]$ on the $2^{\text{nd}}$ place to the $1^{\text{st}}$ place, etc. Therefore, the output permutation is $([3], [1], [4], [2])$ .

Other basic functionalities. Scape additionally requires two functionalities. $F_{checkZero}$ outputs true if the input $[x]$

Input: Two shared relations $[L]$ and $[R]$ , the join attribute $k$ , and a public value $m$ .

# Functionality:

1) Abort if the inputs are inconsistent.   
2) $J = \{(k, \mathbf{t}_L[\neg k], \mathbf{t}_R[\neg k]) | \mathbf{t}_L \in L, \mathbf{t}_R \in R, \mathbf{t}_L[k] = \mathbf{t}_R[k]\}$   
3) $L^{\prime} = \{\mathbf{t}_{L}|\mathbf{t}_{L}\in L,\mathbf{t}_{L}[k]\notin J[k]\}$   
4) $R^{\prime} = \{\mathbf{t}_{R}|\mathbf{t}_{R}\in R,\mathbf{t}_{R}[k]\notin J[k]\}$   
5) If $|J| + |L'| > m$ or $|J| + |R'| > m$ , output abort.   
6) Attach dummy tuples to $J$ to make its size $m$ .   
7) Secret share $J$ to the parties.

Fig. 4: Ideal functionality of general Join.

is [0] and false otherwise. $\mathcal{F}_{\mathrm{shuffle1p}}$ takes $[\overrightarrow{x}]$ = $([\overline{x_1}],\ldots ,[\overline{x_n} ])$ and a plaintext permutation $\pi$ of size $n$ from some $P_{i}$ as inputs. It outputs $[\pi \cdot \overrightarrow{x} ]$ . The protocols realizing them are introduced in [30] and [26], respectively.

# IV. CONSTRUCTING GENERAL JOIN

Now we present the efficient protocol for general Join. Our starting point is Krastnikov et al.'s efficient circuit [23]. This circuit can be sequentially decomposed to sub-circuits for the following six procedures: group dimension calculation, separation, position calculation, distribution, expansion, and alignment. In this work, we provide protocols for these procedures, such that composing these protocols could give a protocol for general Join. Also, since these protocols are just sequentially composed, our final protocol is malicious secure once these invoked protocols satisfy standard malicious security. Note that Krastnikov et al.'s circuit takes as input an upper bound m on the number of rows in the joint relation and our protocol inherits this requirement. The ideal functionality of general Join we realized is shown in Fig.4.

Directly implementing the circuit in [23] with secret sharing would suffer from high round complexity (for traversal-involved procedures) and high communication cost (for sorting-involved procedures). We design an optimized circuit for the traversal and leverage a maliciously secure permutation protocol to avoid oblivious sorting in many cases, thus improving the performance. Their ideal functionalities, named $F_{trav}$ and $F_{perm}$ , are shown in Fig.3 and Fig.2.

We first present our protocols for non-primary-foreign key join in a hybrid manner, where $F_{trav}$ , $F_{perm}$ and other basic functionalities introduced in Section III are invoked in a black-box manner. We also discuss further optimizations for PK-FK join. Then we will give a detailed comparison between our protocol and the original circuit [23].

# A. Secure general Join protocol

1) Group dimension calculation: This procedure finds useful global parameters of relations to be joint.

- Inputs: two relations $[L]$ and $[R]$ , and the join key $k$ . Without loss of generality, we denote all attributes except $k$ of $L$ (resp. $R$ ) by one attribute $d_L$ (resp. $d_R$ ), since there is no calculation between them in Join.   
- Outputs: A merged relation $[T]$ from $[L]$ and $[R]$ with five new attributes $g^{\mathrm{b}}$ , $\alpha_{L}$ , $\alpha_{R}$ , $e^{\mathrm{b}}$ , and $s_{R}$ . Specifically, for each tuple $\mathbf{t} \in L \cup R$ : $\mathbf{t}[g^{\mathrm{b}}] = 1$ iff $\mathbf{t} \in R$ ; $\mathbf{t}[\alpha_L]$ (resp. $\mathbf{t}[\alpha_R]$ ) represents the number of tuples (in the relation $L$ (resp. $R$ )) whose attribute values of $k$ are equal to that

![](images/ca69e946e4ba297605615558108592beb9fa8f1ace072e5f7e7ed5e0349bae9f.jpg)



Fig. 5: Example of group dimension calculation. $(\overline{g^{\mathrm{b}}}$ is $\overline{T[g^{\mathrm{b}}]}$ ) of $\mathbf{t}$ , or formally, $\mathbf{t}[\alpha_L] = |\{\mathbf{t}'|\mathbf{t}'\in L,\mathbf{t}'[k] = \mathbf{t}[k]\} |$ (resp. $\mathbf{t}[\alpha_R] = |\{\mathbf{t}'|\mathbf{t}'\in R,\mathbf{t}'[k] = \mathbf{t}[k]\} |)$ . $\mathbf{t}[e^{\mathrm{b}}]\in \{0,1\}$ indicates whether the tuple $\mathbf{t}$ will be in the joint relation. $\mathbf{t}[s_R]$ is only available when $\mathbf{t}\in R$ and denotes the serial number of $\mathbf{t}$ in its "group" (consisting all tuples in $R$ with the same attribute value of $k$ as $\mathbf{t}$ ).

An example of this procedure is given in Fig.5. The protocol proceeds as follows.

(1) Add an indicator attribute $g^{\mathsf{b}}$ to two relations, such that $[[\mathbf{t}[g^{\mathsf{b}}]] = 0$ for each tuple $\mathbf{t} \in L$ and $[[\mathbf{t}[g^{\mathsf{b}}]] = 1$ for each tuple $\mathbf{t} \in R$ . Then, vertically merge two relations $[[L]]$ and $[[R]]$ as a new relation $[[T]]$ , and invoke the oblivious sorting protocol to sort $[[T]]$ with $sort_{k \downarrow g^{\mathsf{b}} \downarrow}(T)$ .   
(2) Compute three temporary indicator attributes: $s^{b}, g_{d}^{b}, g_{u}^{b}$ . For each tuple $T_{i} \in T$ : $T_{i}[s^{b}] = 1$ iff $T_{i}$ belongs to L, its next tuple $T_{i+1}$ is from R, and $T_{i}[k] = T_{i+1}[k]$ . $T_{i}[g_{d}^{b}] = 1$ iff $T_{i}$ is not the first tuple of its “group” (consisting all tuples in T with the same attribute value of k as $T_{i}$ ). $T_{i}[g_{u}^{b}] = 1$ iff $T_{i}$ is not the last tuple of its “group”. They are computed as follows.

a) $\llbracket T_i[g_d^{\mathsf{b}}]\rrbracket = (\llbracket T_{i - 1}[k]\rrbracket = ?\llbracket T_i[k]\rrbracket)$ .   
b) $\llbracket T_i[g_u^\mathsf{b}]\rrbracket = (\llbracket T_i[k]\rrbracket = ?\llbracket T_{i+1}[k]\rrbracket)$ .   
c) $\llbracket T_i[s^{\mathsf{b}}]\rrbracket = (\llbracket T_i[g^{\mathsf{b}}]\rrbracket \oplus \llbracket T_{i + 1}[g^{\mathsf{b}}]\rrbracket)\odot \llbracket T_i[g_u^\mathsf{b}]\rrbracket .$

(3) Invoke $\mathcal{F}_{\mathrm{trav}}$ for three times with inputs formed by $([(\overrightarrow{x},\overrightarrow{y^{\mathsf{b}}})],\theta ,\phi ,\mathrm{IsPos})$ , where $\overrightarrow{y^{\mathsf{b}}}$ is $T[g_d^{\mathsf{b}}]$ , $\theta (a,b) = a + b$ , $\phi (\cdot)$ =true, IsPos =true, and $\overrightarrow{x}$ is $T[s^{\mathsf{b}}],\overline{T[g^{\mathsf{b}}]},T[g^{\mathsf{b}}]$ for each time. The outputs are shared temporary attribute values $[T[v^{\mathsf{b}}]]$ , $[T[s_L]]$ , $[T[s_R]]$ .

(4) Invoke $\mathcal{F}_{\mathrm{trav}}$ in reverse order for three times with inputs formed by $([[(\overrightarrow{x},\overrightarrow{y^b})],\theta ,\phi ,\mathrm{IsPos})$ , where $\overrightarrow{y^b}$ is $T[g_u^b]$ , $\theta (a,b) = a$ , $\phi (\cdot)$ =true, $\mathrm{IsPos} = \mathrm{false}$ , and $\overrightarrow{x}$ is $T[v^{\mathrm{b}}],T[s_L^{\mathrm{b}}],T[s_R^{\mathrm{b}}]$ for each time. The outputs are $[T[e^{\mathrm{b}}]],[T[\alpha_{L}]],[T[\alpha_{R}]]$ .

2) Separation: This procedure separates the relation $\llbracket T\rrbracket$ obtained above again into two sorted relations.

- Inputs: a relation $[T]$ and $|L|$ and $|R|$ .   
- Outputs: $[L^S]$ , $[R^S]$ . $L^S$ consists of the tuples in $T$ from $L$ and is sorted in the ascending order of $k$ . So does $[R^S]$ .

Note that each tuple contains $g^{b}$ indicating where it is from. By stably sorting according to $g^{b}$ , we can separate the relation, and ensure two result relations are sorted in the order of k.

(1) Invoke $\mathcal{F}_{\mathrm{perGen}}$ on input the bit-array $[T[g^b]]$ and obtain a shared permutation $[\pi_{\mathrm{sort}}]$

(2) Invoke $\mathcal{F}_{\mathrm{perm}}$ on inputs $[\pi_{\mathrm{sort}}]$ and $[T]$ and obtain $[T^S]$ .   
(3) Define the first $|L|$ tuples of the result as $[[L^S]]$ , and the last $|R|$ tuples as $[[R^S]]$ .

3) Position calculation: This procedure computes the last position of each tuple to be placed in the final joint relation. It also checks whether the input m is sufficient.

\- Inputs: two relations $\llbracket L^{S}\rrbracket$ and $\llbracket R^{S}\rrbracket$ , and $m$ .

\- Outputs: Two relations $\llbracket L^P\rrbracket$ and $\llbracket R^P\rrbracket$ with a new attribute $p$ . For each tuple $\mathbf{t} \in L^P \cup R^P$ , $\mathbf{t}[p]$ represents the index where $\mathbf{t}$ last appears in the join result.

Our protocol proceeds as follows.

(1) Compute three shared temporary arrays $\llbracket \overrightarrow{a}\rrbracket, \llbracket \overrightarrow{b}\rrbracket, \llbracket \overrightarrow{p}\rrbracket$ and a temporary shared value $\llbracket c_1\rrbracket$ . After initializing $\llbracket c_1\rrbracket = \llbracket 0\rrbracket$ , the parties compute:

a) For i=1 to $|L^{S}|$ : $[c_{1}]=[c_{1}]+\left[L_{i}^{S}[\alpha^{R}]\right];\left[a_{i}\right]=[c_{1}]$ .   
b) For i=1 to $|L^{S}|$ : $[c_{1}]=[c_{1}]+1-[[L_{i}^{S}[e^{\mathsf{b}}]];[b_{i}]=[c_{1}]$ .   
c) For i=1 to $|L^{S}|$ : $\llbracket p_{i}\rrbracket = \llbracket L_{i}^{S}[e^{\flat}]\rrbracket \cdot (\llbracket a_{i}\rrbracket - \llbracket b_{i}\rrbracket) + \llbracket b_{i}\rrbracket$ .

Then, $c_{1}$ equals $|J| + |L'|$ in Fig. 4. $[[L^P]]$ is obtained by appending an new attribute $p$ such that $[[L^P[p]]] = [[\overrightarrow{p}]]$ .

(2) $\llbracket R^P\rrbracket$ and $\llbracket c_2\rrbracket$ are obtained similarly, by replacing $\alpha_{R}$ with $\alpha_{L}$ . $c_{2}$ equals to $|J| + |R'|$ .

(3) Abort if $\left(\llbracket c_1\rrbracket \leq ?m\right)\odot \left(\llbracket c_2\rrbracket \leq ?m\right)$ is false.

An example is shown in the upper left corner of Fig. 6, where $|J| = 8$ , $|L'| = 1$ and $c_{1} = 9$ . The check in step 3 is necessary to ensure the values of $L^{P}[p]$ and $R^{P}[p]$ are pairwise-distinct in $[1,m]$ .

4) Distribution: This procedure distributes each tuple in two relations $\llbracket L^P\rrbracket$ and $\llbracket R^P\rrbracket$ according to the position attributes $\llbracket L^P[p]\rrbracket$ and $\llbracket R^P[p]\rrbracket$ obtained in the above step.

\- Inputs: Two relations $\llbracket L^P\rrbracket$ and $\llbracket R^P\rrbracket$ , and $m$ .

\- Outputs: two relations $\llbracket L^D\rrbracket$ and $\llbracket R^D\rrbracket$ where each relation has $m$ tuples. The $L_i^S[p]$ -th tuple in $L^D$ should be equal to $i$ -th tuple in $L^S$ . So does $R^D$ . They also include an additional indicator attribute $o^b$ indicating whether the tuple is dummy.

As mentioned in T3 of Section II, our idea is to extend $\llbracket L^{P}\rrbracket[p]$ (resp. $\llbracket R^{P}[p]\rrbracket$ ) into a permutation $\llbracket\pi_{L}\rrbracket$ (resp. $\llbracket\pi_{R}\rrbracket$ ) of size m, such that permuting an m-dimension array according to this permutation will place the i-th tuple to the $\llbracket L^{S}\rrbracket_{i}[p]$ -th (resp. $\llbracket R^{S}\rrbracket_{i}[p]$ ) position. The detailed protocol $P_{p2Per}$ is presented in Fig. 7.

(1) Invoke $\mathcal{P}_{\mathrm{p2Per}}([L^P[p]],m)$ to obtain $[\pi_L]$ .   
(2) Append $m - |L^S|$ dummy tuples to the end of $[[L^P]]$ , and add an indicator attribute $o^{\mathsf{b}}$ to $[[L^P]]$ to indicate whether a tuple is dummy, namely, $[[L_i^P[o^\mathsf{b}] = 0]]$ for $1 \leq i \leq |L|$ and $[[L_i^P[o^\mathsf{b}] = 1]]$ for $|L| < i \leq m$ .

(3) Invoke $\mathcal{F}_{\mathrm{perm}}([[\pi_L]], [L^P])$ to obtain $[L^D]$ .

(4) Obtain $\llbracket R^D\rrbracket$ in a similar way by repeating step 1-3.

5) Expansion: For each dummy tuple $\llbracket \bot \rrbracket$ of $\llbracket L^D \rrbracket$ (resp. $\llbracket R^D \rrbracket$ ), this procedure replaces it with the first non-dummy tuple behind it. For example, $(\llbracket \bot \rrbracket_1, \llbracket \bot \rrbracket, \llbracket \mathbf{t}_1 \rrbracket, \llbracket \bot \rrbracket, \llbracket \mathbf{t}_2 \rrbracket)$ will be changed into $(\llbracket \mathbf{t}_1 \rrbracket, \llbracket \mathbf{t}_1 \rrbracket, \llbracket \mathbf{t}_1 \rrbracket, \llbracket \mathbf{t}_2 \rrbracket, \llbracket \mathbf{t}_2 \rrbracket)$ .

\- Inputs: two relations $\llbracket L^{D}\rrbracket$ and $\llbracket R^{D}\rrbracket$ .

\- Outputs: two relations $[L^E]$ and $[R^E]$ . For each non-dummy tuple $\mathbf{t} \in L^D$ (resp. $\in R^D$ ), there will be $\mathbf{t}[\alpha_R]$ (resp. $\mathbf{t}[\alpha_L]$ ) copies in $L^E$ (resp. $R^E$ ). Meanwhile

This protocol first copies $\llbracket R^{D}[\alpha_{L}]\rrbracket$ into an array $\llbracket ad_{L}\rrbracket$ . Then, it invokes the traversal functionality $F_{trav}$ in reverse order for multiple times with inputs formed by $(\llbracket(\overrightarrow{x},\overrightarrow{y^{\flat}})\rrbracket,\theta,\phi,\operatorname{IsPos})$ , where $y^{b}$ is $L^{D}[o^{b}]$ , $\theta(a,b)=a$ , $\phi(\cdot)=\operatorname{true}$ , $\operatorname{IsPos}=\operatorname{false}$ , and $\overrightarrow{x}$ is each attribute array of $\llbracket L^{D}\rrbracket$ except $\llbracket L^{D}[o^{b}]\rrbracket$ for each time. The result relation is $\llbracket L^{E}\rrbracket$ . $\llbracket R^{E}\rrbracket$ is obtained by following the above steps and appending a new attribute $\alpha_{DL}$ where $R^{E}[\alpha_{DL}]=\overrightarrow{ad}_{L}$ .

6) Alignment: This procedure aligns the tuples of $[R^E]$ according to the position attribute $\alpha_{DL}$ , horizontally merges the aligned relation with $[L^E]$ , obtaining the joint result $[J]$ .

\- Inputs: Two relations $\llbracket R^{E}\rrbracket$ and $\llbracket L^{E}\rrbracket$

\- Outputs: The joint result $[J]$ .

The protocol proceeds as follows. The relation $R^{E}$ is aligned in steps (1) \~ (3) and is merged into $L^{E}$ in step (4). We only need to align and merge the original attribute array $R^{E}[d_{R}]$ , and these attributes added during the protocol will not be in the result.

(1) Compute two temporary arrays $\llbracket \overrightarrow{a}\rrbracket$ and $\llbracket \overrightarrow{b}\rrbracket$ . Note that Expansion may generate many copies for each tuple, $a_{i}$ represents that there will be $a_{i}$ copies appearing before $R_{i}^{E}$ . $b_{i}$ represents the position that $R_{i}^{E}[d_{R}]$ will placed in $J$ . Initialize $\llbracket a_{|R^{E}| + 1} = 0\rrbracket$ , and for $\mathrm{i} = |R^{E}|$ to 1:

a) Compute $\llbracket a_i\rrbracket = \llbracket a_{i + 1}\rrbracket +\llbracket R_i^E [\alpha_{DL}]\rrbracket -\llbracket R_i^E [e^{\mathsf{b}}]\rrbracket .$

b) Compute $\llbracket b_i\rrbracket = i - (\llbracket R_i^E [s_R]\rrbracket -1)\cdot (\llbracket R_i^E [\alpha_L]\rrbracket -1) +$ $\llbracket a_i\rrbracket \cdot (\llbracket R_i^E [\alpha_R]\rrbracket -1).$

(2) Find the permutation $\llbracket \pi \rrbracket$ that will place components of $R^{E}[d_{R}]:\llbracket \pi (i)\rrbracket = \llbracket R_{i}^{E}[e^{\mathsf{b}}]\rrbracket \cdot (\llbracket b_{i}\rrbracket -i) + i.$

(3) Permute $R^{E}[d_{R}]$ with $[\pi]$ : $\mathcal{F}_{\mathrm{perm}}([\pi], [\left[R^{E}[d_{R}]\right])$ , and the result is the aligned relation $[R^{A}]$ .

(4) Obtain the join result $[J]$ by horizontally concatenating the following attribute arrays: $[L^E [k]], [L^E [d_L]], [R^A]$ , and $[J[f^b]]$ . Here, $J[f^{\mathrm{b}}] = R^{E}[e^{\mathrm{b}}]$ , and $J_{i}[f^{\mathrm{b}}] = 1$ means the tuple $J_{i}$ is valid.

We do not remove invalid tuples from J; otherwise, the exact size, instead of the upper bound m, of the joint relation J will be leaked to computing parties. Invalid tuples will be “ignored” in subsequent protocols and will be removed after revealing the result to clients.

Optimization for PK-FK join. When k is a primary key of L and a foreign key of R, the public value m can be directly set as $|L| + |R|$ since each tuple in R can appear at most once in the join result. So the computation of $\alpha_{L}$ , the expansion and alignment of R is omitted, and the distribution of $R^{S}$ is proceeded by permuting $R^{S}$ with the permutation representing a stable sorting on $R^{S}[e^{b}]$ . The size of Join result can be reduced into $|R|$ by retaining the first $|R|$ tuples.

# B. Comparison and cost analysis.

We give a step-wise comparison of our protocol and the circuit [23] in Table III. Since we utilized efficient permutation protocols to reduce the cost of oblivious sorting in group

![](images/e51ede626b375f5a1a3e253072fa2b826eaa94892355642d19206ab7f08759e3.jpg)



Fig. 6: Example of position calculation, distribution, expansion and alignment.

Notation: $\llbracket \pi \rrbracket \leftarrow \mathcal{P}_{\mathrm{p2Per}}(\llbracket \overrightarrow{p} \rrbracket, m)$ .

Inputs: The values of $\left[\overrightarrow{p}\right]$ , $p_{1},\ldots,p_{n}$ are distinct values in $[1,m]$

Output: the shared permutation $[\pi]$ .

# The protocol:

1) Get $\llbracket \tau \rrbracket = (\llbracket 1 \rrbracket, \ldots, \llbracket m \rrbracket)$ by setting $\llbracket i \rrbracket = (i, 0, 0)$ .   
2) Invoke $\mathcal{F}_{\mathrm{shuffle}}([[\tau]])$ to obtain $[\omega]$ .   
3) Invoke $\mathcal{F}_{\mathrm{soPRF}}$ with $[[\omega], [\overrightarrow{p}]$ , and the random shared PRF key $[k_{\mathrm{PRF}}]$ as input to obtain $[\overrightarrow{\omega^e}]$ and $[\overrightarrow{p^e}]$ .   
4) Securely open $\llbracket \overrightarrow{\omega^e}\rrbracket ,\llbracket \overrightarrow{p^e}\rrbracket .$   
5) Verifies that each item $p_i^e \in \overrightarrow{p^e}$ is distinct, and also exist $j \in [1, m]$ such that $\omega_j^e = p_i^e$ . If this is not true, aborts.   
6) Get an array $\overrightarrow{v}$ , where $v_{i}$ equals the index of the $i$ -th element of $\overrightarrow{\omega^{e}}$ that don't belong to $\overrightarrow{p^{e}}$ .   
7) Generate the permutation $\llbracket \pi \rrbracket$ :   
a) For $1 \leq i \leq n$ : $\llbracket (\pi(i)) \rrbracket = \llbracket p_i \rrbracket$ .   
b) For $n < i \leq m$ : $\llbracket \pi(i) \rrbracket = \llbracket \omega(v_{i-n}) \rrbracket$ .   
8) return $[\pi]$ .

Fig. 7: Generating permutation with an array with distinct values. After randomly shuffling $\tau, \omega$ becomes a random permutation to each party $P_i$ . Without knowing $k_{\mathrm{PRF}}$ , $P_i$ learns nothing but its length about $\vec{p}$ given $\vec{w^e}$ and $\vec{p^e}$ . $\mathcal{P}_{\mathrm{p2Per}}$ takes $O(m)$ bits of communication cost and $O(1)$ rounds.

dimension calculation, separation, distribution and alignment, these steps in our protocol enjoy smaller communication cost than those in [23]; the overall communication cost is thus reduced from $O(m \log^2 m)$ to $O(n \log^2 n + m)$ . Moreover, the communication round of our protocol ( $O(\log^2 n)$ ) is smaller than a naive MPC-implementation's round ( $O(m)$ ), as we designed and leveraged an efficient traversal circuit in group dimension calculation and expansion.

<table><tr><td rowspan="2">Procedures</td><td rowspan="2">Comm. cost of [23]</td><td colspan="2">Scape</td><td rowspan="2">Opt</td></tr><tr><td>Comm. cost</td><td>Rounds</td></tr><tr><td>Group dim.</td><td> $O(n \log^{2} n)$ </td><td> $O(n \log^{2} n)$ </td><td> $O(\log^{2} n)$ </td><td>T1</td></tr><tr><td>Separation</td><td> $O(n \log^{2} n)$ </td><td> $O(n)$ </td><td> $O(1)$ </td><td>T1</td></tr><tr><td>Pos. cal.</td><td> $O(n)$ </td><td> $O(n)$ </td><td> $O(1)$ </td><td></td></tr><tr><td>Distribution</td><td> $O(m \log m)$ </td><td> $O(m)$ </td><td> $O(1)$ </td><td>T2</td></tr><tr><td>Expansion</td><td> $O(m)$ </td><td> $O(m)$ </td><td> $O(\log m)$ </td><td></td></tr><tr><td>Alignment</td><td> $O(m \log^{2} m)$ </td><td> $O(m)$ </td><td> $O(1)$ </td><td>T0</td></tr></table>

TABLE III: Asymptotic communication/computation comparisons for procedures of non-primary-foreign key join. Here n is the number of input rows and m is the output size limitation. “Opt” indicates the optimization technique (which is labeled and illustrated in Section II) used in each step.

# V. OTHER SQL OPERATORS AND COMPOSITION STRATEGY

This section presents MPC protocols for other SQL operators and then shows the optimized strategy of composing multiple operators to realize a complex query.

# A. Constructing other operators

1) PK-PK join: If two input relations $[L]$ and $[R]$ are pre-sorted according to join attribute k, Join can be done with the sort-compare-shuffle (SCS) protocol [21].

(1) Conduct the same operations as the step 1 of group dimension calculation in general Join.   
(2) Set $\llbracket T_i[f^{\mathsf{b}}]\rrbracket = \llbracket T_i[g^{\mathsf{b}}]\rrbracket \cdot (\llbracket T_{i-1}[k]\rrbracket = ?\llbracket T_i[k]\rrbracket)$ and compute $\llbracket T_i[d']\rrbracket = \llbracket T_i[f^{\mathsf{b}}]\rrbracket \cdot \llbracket T_{i-1}[d]\rrbracket$ .   
(3) Invoke $\mathcal{P}_{\mathrm{shuffle}}([T])$ to obtain the Join result.

The protocol for two disordered inputs proceeds as follows.

(1) Invoke $\mathcal{F}_{\mathrm{soPRF}}(k_{\mathrm{PRF}},[[L[k]]])$ and $\mathcal{F}_{\mathrm{soPRF}}(k_{\mathrm{PRF}},[[R[k]]])$ with a random shared $[k_{\mathrm{PRF}}]$ , and reveal the outputs $[L[s]]$ and $[R[s]]$ to $P_1$ and $P_2$ respectively, who verify the received values are distinct.   
(2) $P_{1}$ generate permutation $\pi_L$ representing a sorting of $L[s]$ . The parties invoke $\mathcal{F}_{\mathrm{shuffleip}}(\pi_L, [L], P_1)$ to obtain $[L']$ . The parties verify whether $[L'[s]]$ is sorted with the comparison circuit, and abort if not.   
(3) Similarly, The parties obtain $\llbracket R'\rrbracket$ with $\pi_R$ input by $P_2$ , and verify whether $\llbracket R'[s]\rrbracket$ is sorted.   
(4) Invoke the SCS protocol with input $[L']$ and $[R']$ , and replace k with s in its sorting and comparison phase.

This protocol follows the technique of T3 in Section II, and its complexity is $O(n \log n)$ . $P_1$ and $P_2$ learn nothing from the received soPRF without knowing $k_{\mathrm{PRF}}$ . Checking whether $[[L'[s]]]$ and $[[R'[s]]]$ are sorted is necessary to ensure security in the presence of a malicious adversary, who may input a wrong permutation if he corrupts $P_1$ or $P_2$ .

2) Semi-join: If we invoke $sort_{x\downarrow}((\overrightarrow{x},\sigma))$ , where $[\sigma=(1,2,\ldots,|\overrightarrow{x}|)]$ , then we get $[\overrightarrow{y}]$ and $[\pi]$ where $y_i=x_{\pi(i)}$ . We observe that $[\overrightarrow{y}]$ can be permuted back to $[\overrightarrow{x}]$ by invoking $\mathcal{F}_{\mathrm{perm}}([\pi],[\overrightarrow{y}])$ . Since the Semi-Join of two relation $[R]$ and $[L]$ with the join attribute k essentially computes: $[\mathbf{t}_R[f^\mathrm{b}]=(\vee_{\mathbf{t}_L\in L}\mathbf{t}_L[k]=_{?}\mathbf{t}_R[k])]$ for each tuple $t_R\in R$ , our general Semi-Join proceeds as follows:

(1) Concatenate $[L[k]]$ and $[R[k]]$ to get $[T[k]]$ , and add two attribute $\pi$ and $g^{\mathsf{b}}$ , where $T[\pi] = (1, \ldots, |T|)$ , $T_i[g^{\mathsf{b}}] = 0$ for $1 \leq i \leq |L|$ and $T_i[g^{\mathsf{b}}] = 1$ for $|L| < i \leq |T|$ .   
(2) Invoke $\text{sort}_{k \downarrow g \downarrow}(T)$ , and compute $[[T[f_{\pi}^{\mathsf{b}}]]]$ in the way similar to $e^{\mathsf{b}}$ in group dimension calculation of Join.   
(3) Invoke $\mathcal{F}_{\mathrm{perm}}([T[\pi]], [T[f_{\pi}^{\mathrm{b}}]])$ and keep the last $|R|$ output values as $[R[f^{\mathrm{b}}]]$ .

In this way, we can ignore irrelevant attributes. For a special case that $k$ is primary keys of both relations and two relations are disordered, we utilize the soPRF to reduce the cost of oblivious sorting similar to Join.

![](images/63e9e2aea9145c3fd2eb5d8fff1976a8d7f4f2d8fe4721e9ed06b0b0805a2961.jpg)



Fig. 8: Example of joining L and R on primary key k.

![](images/8944e9b5f453625f190d287da539695a7acefde46815dfc477a5845908598bab.jpg)



Fig. 9: Workflow of semi-join on primary key k with disordered inputs. $(i)^{*}$ means the $i^{th}$ step of the general semi-join protocol.

(1) Similar to the step 1-3 of the PK-PK Join with disordered inputs, The parties obtain $\llbracket L^{\prime}[s]\rrbracket$ and $\llbracket R^{\prime}[s]\rrbracket$ with $\sigma_{L}$ and $\sigma_{R}$ inputted by $P_{1}$ and $P_{2}$ .   
(2) Invoke the general Semi-Join protocol with input $\llbracket L' \rrbracket$ , $\llbracket R'\rrbracket$ and replace $k$ with $s$ , to obtain $\llbracket R'[f^{\mathrm{b}}] \rrbracket$ .   
(3) Invoke $\mathcal{F}_{\mathrm{shuffle1p}}(\sigma_R^{-1},[[R'[f^{\mathrm{b}}],R'[s]]],P_2)$ to obtain $[R[f^{\mathrm{b}}]]$ and $[R''[s]]$ . The parties verify whether $[R''[s]]]$ equals $[R[s]]$ to ensure the correctness of $\sigma_R^{-1}$ .

3) Select: Given a Select operator with a Where predicate $\gamma(\cdot)$ , which can be an arbitrary logical expression, we set the validity indicator attribute of $\mathbf{t} \in T$ as $[[\mathbf{t}[f^{\mathrm{b}}] = \gamma(\mathbf{t})]]$ .

4) Aggregate: Scape's supported aggregate functions includes Max, Min, Count, Sum, Avg. Before the aggregation, the value of $v$ of each tuple $\mathbf{t}$ is updated into $[\mathbf{t}[v] = \mathbf{t}[f^{\mathrm{b}}] \cdot \mathbf{t}[v]]$ . Count(\*) is equivalent to $\text{Sum}(f^{\mathrm{b}})$ , and $\text{Avg}(v)$ equals $\text{Sum}(v)/\text{Sum}(f^{\mathrm{b}})$ . Max/Min needs $O(\log n)$ rounds.

5) Order-by: The Order-by a relation $[T]$ in the ascending order of the attribute v is done with $sort_{f^{b}\uparrow v\downarrow}(T)$ . The operators involving multiple attributes and various combinations of ASC or DESC can be programmed in a similar way.

6) Group-by-aggregation: The queries with the form “Select Agg(v) From T Group by k” can be realized by four steps:

(1) Invoke $\text{sort}_{f^{\flat} \uparrow k \downarrow}(T)$ to sort $[[T]]$ .   
(2) Obtain the group indicator: $\llbracket T_i[g^{\mathrm{b}}]\rrbracket = (\llbracket T_i[k]\rrbracket = ?$ $\llbracket T_{i - 1}[k]\rrbracket)$ , so that $\mathbf{t}[g^{\mathrm{b}}] = 0$ if $\mathbf{t}\in T$ is the first one of its group (consisting of all tuples with the same value of $k$ as $\mathbf{t}$ ), otherwise $\mathbf{t}[g^{\mathrm{b}}] = 1$ .   
(3) Invoke $\mathcal{F}_{\mathrm{trav}}([T[v], T[g^{\mathrm{b}}]], \theta, \phi, \mathrm{true})$ to obtain the output attribute $T[r]$ , where $\theta(a, b) = a + b$ , $\phi(\cdot) = \mathrm{true}$ for sum/count, or $\theta(a, b) = a$ , $\phi(a, b) = a > ?$ $b(a < ?b)$ for $\max(\min)$ .   
(4) Compute $\llbracket T_i[f^{\mathbf{b}}]\rrbracket = \llbracket T_i[f^{\mathbf{b}}]\rrbracket \cdot \llbracket \overline{T_{i + 1}[g]}\rrbracket .$   
(5) Invoke $\mathcal{P}_{\mathrm{shuffle}}([T])$ to obtain the result.   
7) Distinct: This operator is done by changing the step (3)-(4) of Group-by into computing $\llbracket T_i[f^b]\rrbracket = \llbracket T_i[f^b]\rrbracket \cdot \llbracket \overline{T_i[g]}\rrbracket$ .

![](images/22fb6b3df64833144a90979baa3737cd4c8dac2660573f9e0c85ca95f0cacff3.jpg)



Fig. 10: Example of “Select Min(v) as r From T Group by k”.

# B. The strategy of composing operators

A complex query can be conducted by composing multiple operators in sequential order. We use the cost model to choose the query plan with the lowest cost. The cost of naively composing two operators equals the sum of their respective cost, so we easily summarize a rule: pushing forward the operators with no increase in output size. Meanwhile, the constructions of some operators can be modified to reduce the cost for several individual composition cases.

1) Making “sorting sensitive” operators adjacent: Order-by, Group-by, Distinct and Join are “sorting sensitive”. The sorting can be omitted or be more efficiently conducted with oblivious permutation when composing those operators. For example, if Order-by k follows Group-by k, the random shuffling of Group-by is omitted, and the result can be obtained by invoking $F_{perm}$ to permute the relation with the permutation representing a stable sorting on $f^{b}$ .   
2) Splitting the Join operator: For some queries with Group-by or Distinct after Join, performing a complete Join is unnecessary. Taking “Select Sum(L.d) From L Join R on L.k=R.k Group by k” as an example, $\left[\mathbf{t}[v]\right]=\left[\mathbf{t}[g^{b}]\right]\cdot\left[\mathbf{t}[d]\right]\cdot\left[\mathbf{t}[\alpha_{R}]\right]$ for each tuple $t\in T$ can be computed after group dimension calculation, and the final result can be obtained with the steps 3-5 of Group-by by replacing $\left[T[g^{b}]\right]$ with $\left[T[g_{d}^{b}]\right]$ . The query “Aspirin Count” in [11] is an example with Distinct:

$$
\begin{array}{l} \text {Select Count(Distinct pid) From d Join m on d.pid = m.pid} \\ \text {Where d.diag = hd and m.med = aspirin} \\ \text {and d.time \leq m.time ;} \end{array}
$$

It can be transformed into:

$$
\begin{array}{l} \text { Select   Count } (^ {*}) \text {   From   } d \text {   Join   } m \text {   on   } d. p i d = m. p i d \\ \text {   Where   } d. \text { diag } = h d \text {   and   } m. \text { med } = \text { aspirin   } \\ \text { Group   by   } p i d \text {   Having   } \operatorname{Min} (d. t i m e) \leq \operatorname{Max} (m. t i m e); \\ \end{array}
$$

After group dimension calculation, the result can be obtained with the steps 3-4 of Group-by, comparisons and SUM.

# VI. SCAPE'S ADVANCED TOOLS

# A. Malicious-secure oblivious permutation

Oblivious permutation [25] in the semi-honest setting is based on random shuffling, which can permute a shared array $\left[\overrightarrow{x^{\prime}}\right]$ with an undisclosed random permutation $\sigma$ . Efficient random shuffling is done by the way that three parties take turns to shuffle $(2,2)$ -additive shares in pairs and re-share the shuffled values into the $(3,2)$ -replicated shares. (Which is the same as steps 2-4 ignoring the operation of $\left[\overrightarrow{m}\right]$ in Fig. 11.) In this process, $\overrightarrow{x^{\prime}}$ is shared among at least two parties at each step, thus no party can learn $\overrightarrow{x^{\prime}}$ . Each permutation $\sigma_{i}$ used for shuffling is known to only two parties $P_{i-1}$ and

Notation: $\left[\overrightarrow{y}\right]\leftarrow\mathcal{P}_{\text{shuffle}}(\left[\overrightarrow{x}\right])$ .

Inputs: $\left[\overrightarrow{x}\right]=\left(\left[x_{1}\right],\ldots\left[x_{n}\right]\right)$ .

# The protocol:

1) The parties generate a random shared value $[a]$ , and compute $[\overrightarrow{m} ] = [a\cdot \overrightarrow{x^{\prime}} ] = ([a\cdot x_{1}],\dots ,[a\cdot x_{n}]).$   
2) $P_{1}$ and $P_{3}$ locally compute 2-out-of-2 shared of $\overrightarrow{x}$ and $\overrightarrow{m}$ : $[[\overrightarrow{x}]]\xrightarrow{1,3} [\overrightarrow{x}^{1}], [[\overrightarrow{m}]]\xrightarrow{1,3} [\overrightarrow{m}^{1}].$   
3) for i = 1 to 2 do:

a) $P_{i}$ and $P_{i - 1}$ shuffle $[\overrightarrow{x}^i ]$ , $[\overrightarrow{m}^i ]$ with a random generated permutation $\sigma_i\colon \sigma_i\cdot ([\overrightarrow{x}^i ],[ \overrightarrow{m}^i ])\to ([\overrightarrow{x}^i ]_1,[\overrightarrow{m}^i ]_1]).$   
b) $P_{i}$ and $P_{i - 1}$ re-randomize $[\overrightarrow{x}^{i + 1}],[\overrightarrow{m}^{i + 1}]$ .   
c) $P_{i - 1}$ sends his shares to $P_{i + 1}$ .   
4) $P_{2}$ and $P_{3}$ shuffle the shares with a random permutation $\sigma_{3}$ , and transform the shares into the three party sharing form: $\sigma_{3} \cdot [\overrightarrow{x}^{3}] \xrightarrow{1} [\overrightarrow{x}^{5}], \sigma_{3} \cdot [\overrightarrow{m}^{3}] \xrightarrow{1} [\overrightarrow{m}^{5}]$ .   
5) $P_{1}$ and $P_{2}$ transform the result into the three party sharing form: $[\overrightarrow{x}^2] \xrightarrow{3} [\overrightarrow{x}^4], [\overrightarrow{m}^2] \xrightarrow{3} [\overrightarrow{m}^4]$ .   
6) The parties securely open $a$ , and compute: $\llbracket \overrightarrow{y}^1 \rrbracket = \llbracket a \cdot \overrightarrow{x} - \overrightarrow{m} \rrbracket, \llbracket \overrightarrow{y}^2 \rrbracket = \llbracket a \cdot \overrightarrow{x}^4 - \overrightarrow{m}^4 \rrbracket, \llbracket \overrightarrow{y}^3 \rrbracket = \llbracket a \cdot \overrightarrow{x}^5 - \overrightarrow{m}^5 \rrbracket$ .   
7) for k = 1 to 3 do:   
a) The parties collaborate to generate random values $\overrightarrow{r}^k = \{r_1^k, \ldots, r_n^k\}$ . They run $\mathcal{F}_{\text{checkZero}}([[\sum r_i^k \cdot y_i^k]])$ , where $y_i^k \in \overrightarrow{y}^k$ , and abort if the output is false.   
8) return: $\llbracket \overrightarrow{x}^{5}\rrbracket$

Fig. 11: Random shuffling protocol

$P_{i}$ , thus no party knows the true permutation applied on $\vec{x}$ : $\sigma = \sigma_{1} \circ \sigma_{2} \circ \sigma_{3}$ . The result of shuffling is $\sigma \cdot \vec{x}$ .

<table><tr><td>Commitment</td><td> $P_1$ </td><td> $P_2$ </td><td> $P_3$ </td><td>Verification</td></tr><tr><td>multiplication</td><td>√</td><td>√</td><td>√</td><td> $a \cdot \overrightarrow{x} \stackrel{?}{=} \overrightarrow{y}$ </td></tr><tr><td> $[\overrightarrow{x}^{1}] \to [\overrightarrow{x}^{2}]$ </td><td>√</td><td></td><td>√</td><td> $a \cdot \overrightarrow{x}^{4} \stackrel{?}{=} \overrightarrow{y}^{4}$ </td></tr><tr><td> $[\overrightarrow{x}^{2}] \to [\overrightarrow{x}^{3}]$ </td><td>√</td><td>√</td><td></td><td rowspan="2"> $a \cdot \overrightarrow{x}^{5} \stackrel{?}{=} \overrightarrow{y}^{5}$ </td></tr><tr><td> $[\overrightarrow{x}^{3}] \to [[\overrightarrow{x}^{5}]]$ </td><td></td><td>√</td><td>√</td></tr></table>

TABLE IV: The three columns in the middle indicate whether $P_{i}$ could alter the shared values in each step, and those modification can be caught by verifying the equation of the last column.

We notice that after transferring a $(3,2)$ -replicated shared value into a $(2,2)$ -additive shared value, a malicious party could alter the shared values by changing their shares. Instead of using general zero-knowledge proofs [15] with a heavy cost, we use multiplication commitment to verify that each party honestly follows the protocol, which is similar to the protocol implementing the security functionality $F_{shuffle1p}$ in [26]. Compared to [26], we need to take additional checking procedures to ensure that the (shared) permutation remains unchanged even if one party is malicious. The superscript on shared values, e.g., $\left[\overline{x^{1}}\right]$ , is used to denote a possible change in the shared value by an adversary. As shown in Table IV, three verifications can catch each possible data modification by an adversary with high probability $(1-O(\frac{1}{2^{k}})$ , where k is the bit length of each share).

Our oblivious permutation protocol is shown in Fig. 12. Assume the real permutation applied on $[ \pi, \vec{x} ]$ is $\sigma$ , then $[ \rho ] = [ \sigma \cdot \pi ]$ and $[ [\vec{y}] = [ \sigma \cdot \vec{x} ]]$ . The correctness of protocol follows from $\pi^{-1} \cdot \vec{x} = \rho^{-1} \cdot \vec{y} = (\sigma \pi)^{-1} (\sigma \vec{x})$ .

# B. Round-efficient oblivious traversal

As mentioned, the correctness of $g(g(T_1, T_2), T_3) = g(T_1, g(T_2, T_3))$ can be verified under all possible combination Notation: $\llbracket \overrightarrow{y} \rrbracket \leftarrow \mathcal{P}_{\mathrm{perm}}(\llbracket \pi \rrbracket, \llbracket \overrightarrow{x'} \rrbracket, )$ .

Inputs: $\llbracket \pi = (\pi(1),\ldots ,\pi (n))\rrbracket ,\llbracket \overrightarrow{x'} = (x_1,\dots x_n)\rrbracket .$

# The protocol:

1) The parties invoke $\mathcal{P}_{\mathrm{shuffle}}([ \pi, \overrightarrow{x} ])$ to obtain $[\rho]$ and $[\overrightarrow{z} ]$   
2) The parties securely open $\rho$ .   
3) The parties locally compute $\rho^{-1} \cdot [\overrightarrow{z}]$ to obtain $[\overrightarrow{y}]$ .

Fig. 12: Oblivious permutation protocol   
![](images/1997c2a14c700273e55a193a93164ab67485c31c787af5c911659449b24feffa.jpg)



Fig. 13: Example of the general oblivious traversal protocol when $\phi(\cdot) = \text{true}$ and $\theta(a, b) = a + b$ .

of the functions $\theta$ and $\phi$ . Assume $z_{i:j}$ as the result of $z$ of $j^{th}$ tuple if the traversal is computed only on $T_{i:j} = \{(x_l, y_l^{\mathsf{b}}) | l \in [i,j]\}$ , and $s_{i:j}^{\mathsf{b}}$ indicates whether the values of $y^{\mathsf{b}}$ are all true in $T_{i:j}$ . The values of variables $z_{i:i}$ and $s_{i:i}^{\mathsf{b}}$ should be initialized as: $[z_{i:i}] = [x_i], [s_{i:i}^{\mathsf{b}}] = [y_i^{\mathsf{b}}]$ . For $1 \leq i \leq k < j \leq n$ :

$$
(\llbracket z _ {i: j} \rrbracket , \llbracket s _ {i: j} ^ {\mathsf {b}} \rrbracket) = g ((\llbracket z _ {i: k} \rrbracket , \llbracket s _ {i: k} ^ {\mathsf {b}} \rrbracket), (\llbracket z _ {k + 1: j} \rrbracket , \llbracket s _ {k + 1: j} ^ {\mathsf {b}} \rrbracket)).
$$

Essentially, $[z_i] = [z_{1:i}]$ and $[s_i^b] = [s_{1:i}^b]$ . We follow the Brent-Kung network [31] to design the circuit of $\mathcal{P}_{\mathrm{trav}}([\overrightarrow{x'}], [\overrightarrow{y^b}])$ and an example is shown in Fig 13. Our protocol needs twice the amount of communication cost compared to the naive method.

# VII. SECURITY ANALYSIS

We now argue the security of Scape protocols for user queries in the model of malicious security with an honest majority. By our design, a protocol for a user query is a sequential composition of protocols for SQL operators, which are further sequentially composed of basic protocols, including protocols for circuit evaluations, permutations, and so on. Therefore, the security of Scape is directly implied via standard composition theorems [32] if all basic protocols are secure. In the following, we provide a sketched analysis for each kind of basic protocol; The formal proof is deferred to the full version due to the space constraint.

Circuit evaluation. Circuit evaluation protocols refer to those fully composed of atomic protocols for boolean operations and arithmetic operations. Protocols for equality test, comparisons, and soPRF, as well as our traversal protocol, belong to this type. As all atomic protocols used in Scape are from ABY $^{3}$ [3], their security follows the original analysis [3] and the standard composition theorems.

Shuffling and permutation. Our shuffling/permutation protocols are based on the semi-honest secure protocols in [25]. To achieve malicious security, we follow the idea in [26] and utilize the multiplication commitment to verify whether each party follows the protocol. Particularly, we carefully set multiple verification steps to ensure that all malicious alterations will be detected, as illustrated in Table IV. Note that most SQL protocols are sequential compositions of circuit evaluation protocols and shuffle/permutation protocols, so their security follows.

![](images/eb14403a747cc10eb00a0d14ac4e4f016f496003bbaee526dcfc6bfe7d007bef.jpg)



Fig. 14: Permutation & shuffling

![](images/575ebb071976ef0d5b0c9c155b58c200312f1966d36e927627b5e00a45446b53.jpg)



Fig. 15: Basic operators

![](images/c3c83d7aeef21b360e52609e4a9d80fe00c82c6a5344d59807bd6ab8c61a6627.jpg)



Fig. 18: General join

![](images/83e85d6009d780dbeaf3a56c90db4ec9a8581fc0066fca8a66c1760caa675beb.jpg)



Fig. 19: PK-PK join

soPRF-based permutation generation. Join and Semi-join additionally involve a special kind of sub-protocols in which some party locally generates a permutation according to pseudorandom values outputted by soPRF. More precisely, $P_{p2Per}$ (Fig.7) in join, the step 2-3 in PK-PK join, and optimized semi-join protocol belong to this kind. On rough terms, as the party only has access to the pseudorandom values, the semi-honest security is preserved. We further apply several checking steps to ensure the permutation provided by the specific party is correct, achieving malicious security.

# VIII. EXPERIMENTS

In this section, we demonstrate Scape's improvements by evaluating each operator and running tests on real queries. Taking Secrecy [13] as the baseline, Scape's basic operators achieve up to $27 \times$ improvement in runtime, and up to $25 \times$ reduction in communication cost. This ratio increases as the amount of data grow due to our asymptotic improvements.

# A. Implementation and experiment setup

Implementation. We implement a prototype of our proposal based on Java and use netty to communicate among servers. We set the field size of secret sharing as 64 bits. For the parameters of LowMC, we set the block size l = 64, the key size $\kappa = 128$ , s-boxes per layer s = 13, the desired data complexity $d = 2^{30}$ , which results in the round being r = 12.

Experimental setup. We evaluate our framework on three physical machines with Intel $^{®}$ Core $^{TM}$ i9-9900K 3.60GHz CPU and 128GB RAM. Three servers are connected through a router. The LAN bandwidth is 1Gbps and RTT is 1.7ms. We simulate the WAN setting by limiting the bandwidth to 100 Mbps and RTT to 20ms with tc command. We ignore the cost for generating multiplication triples in subsequent evaluation.

Queries. We use 12 real-world queries with various input sizes to evaluate the scalability of our framework, where the first 5 representative queries come from [11] [12], and the last 7 queries are from the TPC-H benchmark. Except for “Password reuse”, we fix the data field size of all attributes as 64 bits. We follow the setting of the query “Password reuse” in [12] to set the user identifier as 32 bits and the password hash as 256 bits. Since the performance of an oblivious protocol is only about the data size and independent of data values, we randomly sample the data in all experiments while ensuring that no relational constraints are violated. In the following experiments, we assume the input relations are all pre-shared among three computing parties and are disordered.

![](images/070028df19cc1866806c065fbd2c7dfd9f8cad60d9803b05230a5983e96be260.jpg)



Fig. 16: Group by aggregation

![](images/70c7dd0f30e0883a946527bf5df5454cf7fd6be1bc2cc5276a78be9a330fb7db.jpg)



Fig. 17: Semi-join

# B. Scape's Building blocks

We evaluate our random shuffling and oblivious permutation with different input sizes, and compare their performance with the semi-honest version as shown in Fig. 14. To permute one million 64-bit data, the oblivious permutation of the semi-honest version takes 1.8s, while its malicious version takes 6.7s, which would be an acceptable cost for many applications.

# C. Scape's SQL operators

We first evaluate operators that do not involve operations between tuples, including where clauses and aggregation. We also measure the performance with the query Q6 in TPC-H benchmark that is entirely composed of the above operators. As shown in Fig. 15, our protocols for these operators are practical, taking less than 4s on relations with 1M tuples.

We evaluate two implementations of Order-by (T1 in Section II), where the naive one sorts the key attribute and non-key attributes together and the optimized one uses the generated shared permutation. Table V shows that our optimized one requires less communication and execution time. In subsequent experiments, we use the optimized one for all operators.

<table><tr><td rowspan="2">Number of non-key attr.</td><td colspan="3">Comm. cost (GB)</td><td colspan="3">Time (Min)</td></tr><tr><td>2</td><td>4</td><td>6</td><td>2</td><td>4</td><td>6</td></tr><tr><td>Naive</td><td>16.4</td><td>22.2</td><td>27.9</td><td>13.97</td><td>18.63</td><td>23.79</td></tr><tr><td>Optimized</td><td>11.8</td><td>11.9</td><td>12.0</td><td>10.07</td><td>10.13</td><td>10.18</td></tr></table>

TABLE V: Order-by with 1M tuples and one key attribute.

Our protocols for general Join, Join on unique keys, Semi-Join, and Group-by-aggregation, are asymptotically more efficient than previous works. We evaluate these protocols, re-implement Secrecy, and compare them on databases of various sizes, confirming our advantages.

Fig. 16 shows the time cost of Group-by. Secrecy's Group-by needs $O(n)$ rounds, so its Group-by-Max needs more than 17.8 minutes to process 65K input rows. Our Group-by-Sum/Max on 1M rows takes just around 10min. If the input tuples are sorted, our Group-by-Sum(Max) on 1M rows only takes 16.5s(28s), while Secrecy's Group-by-Sum(Max) on 65K rows needs (2min)17min.

When the join keys are non-unique, our semi-join only needs 23.7 minutes to deal with 1M rows per input. Its biggest overhead comes from oblivious sorting, so its execution time can be reduced to 165s if two inputs are pre-sorted. Secrecy's protocol needs $O(n^{2})$ comparison, which results in a huge communication cost. For example, when each input has 64K rows, it transfers of 104.7GB data and takes 32 minutes, while our protocol transfers 3.3GB of data and takes 1 minute.

![](images/7c8f35a45bf44fe8971e5ab2720ccd0d9a4f547e0da14503a2adf176bd72f276.jpg)



Fig. 20: Representative queries

Fig. 18 shows the scalability of our general Join protocol. When the key is a non-unique attribute in each relation, Scape is $27.7\times$ faster and the amount of communication cost is $25.6\times$ less than Secrecy, for input relations with 65K tuples. Our PK-FK join protocol reduces the time cost from 30 minutes (with general join) to 27 minutes over input relations with 1M tuples. As shown in Fig. 19, with 1M rows per input, the execution time of PK-PK join on disordered inputs is 5.7 minutes, which is comparable with the one on sorted inputs.

# D. Performance on benchmark

1) Representative queries: We benchmark Scape on five representative queries and compare the performance with Senate and SMCQL. We run three queries on SMCQL with the default configuration in its source code, where only 8 of 25 tuples per relation participate in the MPC part. We use the reported performance of Senate for comparison as Senate had not been open-sourced yet. Also, the computation and network resources (r5.12xlarge Amazon EC2 instances with 48 3.1 GHz vCPUs, and 384 GB RAM) used in its experiments are generally larger than those in ours.

Scape outperforms SMCQL and Senate as shown in Fig. 20. Apart from the fact that the replicated-secret-sharing-based protocols (Scape & Secrecy) are usually more efficient than garbled circuit-based ones (SMCQL & Senate), our performance gain comes from the asymptotic improvement of operators (as summarized in Table I) and our composition strategy. Taking “Recurrent C. Diff” as an example, we don’t perform a complete join, but compare adjacent rows after oblivious sorting. Then, Distinct is fulfilled by a Group-by-sum without sorting, which calculates whether there exists a row that satisfies all conditions for each group.

2) TPC-H benchmark: We test Scape on more complex query structures by evaluating the performance on seven queries selected from the TPC-H benchmark, where the performance on Q6 is already shown in Fig. 15.

Scaling behavior. As shown in Fig. 21, Scape performs well with large-scale inputs. The most expansive operator is PK-FK join, so the queries only involve PK-PK join, like Q4 and Q12, need less execution time, while the other queries containing multiple joins need more time. As a representative, we compare Secrecy and Scape with Q4 in Table VI.

Simulating real-world application. We repeat the performance experiment by evaluating Scape in the WAN setting. The results show that the execution in the WAN setting will

![](images/048a7103e5cd06a0442fec96d00667bcbdfe335e8b29f4e1e45ac1e4929dd55d.jpg)



Fig. 21: Performance on TPC-H queries

be $2.27 \times \sim 2.64 \times$ slower than in the LAN setting. The performance of Scape is acceptable in real-world scenarios.

<table><tr><td>Tuples per input</td><td> $2^{8}$ </td><td> $2^{10}$ </td><td> $2^{12}$ </td><td> $2^{14}$ </td><td> $2^{16}$ </td></tr><tr><td>Secrecy</td><td>1.3</td><td>4.8</td><td>17.4</td><td>145.7</td><td>1844</td></tr><tr><td>Scape</td><td>2.0</td><td>3.3</td><td>6.2</td><td>15.1</td><td>44.8</td></tr></table>

TABLE VI: Query4's execution time (s).

# IX. RELATED WORK

MPC framework. Many general-purpose MPC frameworks are proposed in semi-honest [2], [33], [34] setting, as well as malicious [18], [35], [36] settings. Scape builds on ABY3 [3] that implements the maliciously secure secret sharing protocol.

Outsourced database. Performing SQL queries on outsourced database is studied in the many literatures [37]–[40], where the queries are usually conducted with property-preserving encryption [41], [42]. In this setting, the cloud provides services to data owners. Its function is different from the MPC-based systems, which aim to provide a unified query interface on private databases owned by multiple owners.

MPC-based collaborative analytics systems. There are many systems that provide a wide range of SQL operators, e.g., SMCQL [11], Shrinkwrap [6], Conclave [4] Senate [12], and Secrecy [13]. For the most time-consuming operator join, many optimizations are achieved through differential privacy [6] or the introduction of a trusted third party [4], while Scape only need an upper bound of join size. There are also many works focusing on certain specific query types, e.g., free-connex join-aggregate queries [43] and PSI-aggregation [44]–[48].

Trusted hardware. Many secure query systems [8], [9], [49] are built on trusted hardware enclaves, e.g., SGX, However, a trusted hardware based system may suffer from side-channel attacks [50] or requires additional trust assumptions.

# X. CONCLUSIONS

In this paper, we tackle the important problem of performing SQL queries over multi-source databases with the assistance of three non-colluding computing parties, at most one among whom is malicious. Scape provides a rich set of optimizations that significantly improve the performances of SQL operators, e.g., join, semi-join, group-by. We conduct comprehensive experiments, and the results show Scape outperforms SOTA works and scales well to large-scale databases.

# ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research is supported by the National Key R&D Program of China 2021YFB2900103, NSFC with No. 61932016, No. 62132018, No. 61822209, Key Research Program of Frontier Sciences, CAS, No. QYZDY-SSW-JSC002, Fundamental Research Funds for the Central Universities, and Alibaba Research Intern Program.

# REFERENCES

[1] D. Chaum, C. Crépeau, and I. Damgard, “Multiparty unconditionally secure protocols,” in Proceedings of the twentieth annual ACM symposium on Theory of computing, 1988, pp. 11–19.   
[2] D. Demmler, T. Schneider, and M. Zohner, “Aby-a framework for efficient mixed-protocol secure two-party computation.” in NDSS, 2015.   
[3] P. Mohassel and P. Rindal, “Aby3: A mixed protocol framework for machine learning,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, 2018, pp. 35–52.   
[4] N. Volgushev, M. Schwarzkopf, B. Getchell, M. Varia, A. Lapets, and A. Bestavros, “Conclave: secure multi-party computation on big data,” in Proceedings of the Fourteenth EuroSys Conference 2019, 2019, pp. 1–18.   
[5] C. Dwork, A. Roth et al., “The algorithmic foundations of differential privacy.” Foundations and Trends in Theoretical Computer Science, vol. 9, no. 3-4, pp. 211–407, 2014.   
[6] J. Bater, X. He, W. Ehrich, A. Machanavajjhala, and J. Rogers, "Shrinkwrap: efficient sql query processing in differentially private data federations," Proceedings of the VLDB Endowment, vol. 12, no. 3, pp. 307-320, 2018.   
[7] J. Bater, Y. Park, X. He, X. Wang, and J. Rogers, “Saqe: practical privacy-preserving approximate query processing for data federations,” Proceedings of the VLDB Endowment, vol. 13, no. 12, pp. 2691–2705, 2020.   
[8] S. Bajaj and R. Sion, “Trusteddb: A trusted hardware-based database with privacy and data confidentiality,” IEEE Transactions on Knowledge and Data Engineering, vol. 26, no. 3, pp. 752–765, 2013.   
[9] C. Priebe, K. Vaswani, and M. Costa, “Enclavedb: A secure database using sgx,” in 2018 IEEE Symposium on Security and Privacy (SP). IEEE, 2018, pp. 264–278.   
[10] S. Eskandarian and M. Zaharia, “Oblidb: oblivious query processing using hardware enclaves,” arXiv preprint arXiv:1710.00458, 2017.   
[11] J. Bater, G. Elliott, C. Eggen, S. Goel, A. N. Kho, and J. Rogers, “Smcql: Secure query processing for private data networks.” Proc. VLDB Endow., vol. 10, no. 6, pp. 673–684, 2017.   
[12] R. Poddar, S. Kalra, A. Yanai, R. Deng, R. A. Popa, and J. M. Hellerstein, “Senate: A maliciously-secure {MPC} platform for collaborative analytics,” in 30th {USENIX} Security Symposium ( {USENIX} Security 21), 2021.   
[13] J. Liagouris, V. Kalavri, M. Faisal, and M. Varia, “Secrecy: Secure collaborative analytics on secret-shared data,” arXiv preprint arXiv:2102.01048, 2021.   
[14] V. Kolesnikov, A.-R. Sadeghi, and T. Schneider, “Improved garbled circuit building blocks and applications to auctions and computing minima,” in International Conference on Cryptology and Network Security. Springer, 2009, pp. 1–20.   
[15] S. Laur, J. Willemson, and B. Zhang, “Round-efficient oblivious database manipulation,” in International Conference on Information Security. Springer, 2011, pp. 262–277.   
[16] J. Furukawa, Y. Lindell, A. Nof, and O. Weinstein, “High-throughput secure three-party computation for malicious adversaries and an honest majority,” in Annual international conference on the theory and applications of cryptographic techniques. Springer, 2017, pp. 225–255.   
[17] “Tpc-h benchmark,” http://www.tpc.org/tpch/.   
[18] X. Wang, S. Ranellucci, and J. Katz, “Global-scale secure multiparty computation,” in Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, 2017, pp. 39–56.   
[19] I. Damgård, M. Keller, E. Larraia, V. Pastro, P. Scholl, and N. P. Smart, “Practical covertly secure mpc for dishonest majority—or: breaking the spdz limits,” in European Symposium on Research in Computer Security. Springer, 2013, pp. 1–18.   
[20] M. Keller, E. Orsini, and P. Scholl, “Mascot: faster malicious arithmetic secure computation with oblivious transfer,” in Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security, 2016, pp. 830–842.   
[21] Y. Huang, D. Evans, and J. Katz, “Private set intersection: Are garbled circuits better than custom protocols?” in NDSS, 2012.   
[22] K. E. Batcher, “Sorting networks and their applications,” in Proceedings of the April 30–May 2, 1968, spring joint computer conference, 1968, pp. 307–314.   
[23] S. Krastnikov, F. Kerschbaum, and D. Stebila, “Efficient oblivious database joins,” Proceedings of the VLDB Endowment, vol. 13, pp. 2132 – 2145, 2020.

[24] D. Bogdanov, S. Laur, and R. Talviste, “A practical analysis of oblivious sorting algorithms for secure multi-party computation,” in Nordic Conference on Secure IT Systems. Springer, 2014, pp. 59–74.   
[25] K. Chida, K. Hamada, D. Ikarashi, R. Kikuchi, N. Kiribuchi, and B. Pinkas, “An efficient secure three-party sorting protocol with an honest majority.” IACR Cryptol. ePrint Arch., vol. 2019, p. 695, 2019.   
[26] P. H. Le, S. Ranellucci, and S. D. Gordon, “Two-party private set intersection with an untrusted third party,” in Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security, 2019, pp. 2403–2420.   
[27] J. Dean and S. Ghemawat, “Mapreduce: simplified data processing on large clusters,” Communications of the ACM, vol. 51, no. 1, pp. 107–113, 2008.   
[28] D. Harris, “A taxonomy of parallel prefix networks,” in The Thrity-Seventh Asilomar Conference on Signals, Systems & Computers, 2003, vol. 2. IEEE, 2003, pp. 2213–2217.   
[29] M. R. Albrecht, C. Rechberger, T. Schneider, T. Tiessen, and M. Zohner, "Ciphers for mpc and fhe," in Annual International Conference on the Theory and Applications of Cryptographic Techniques. Springer, 2015, pp. 430-454.   
[30] K. Chida, D. Genkin, K. Hamada, D. Ikarashi, R. Kikuchi, Y. Lindell, and A. Nof, “Fast large-scale honest-majority mpc for malicious adversaries,” in Annual International Cryptology Conference. Springer, 2018, pp. 34–64.   
[31] R. P. Brent and H. T. Kung, “A regular layout for parallel adders,” IEEE transactions on Computers, vol. 31, no. 03, pp. 260–264, 1982.   
[32] R. Canetti, “Security and composition of multiparty cryptographic protocols,” Journal of Cryptology, vol. 13, pp. 143–202, 2000.   
[33] D. Bogdanov, S. Laur, and J. Willemson, “Sharemind: A framework for fast privacy-preserving computations,” in European Symposium on Research in Computer Security. Springer, 2008, pp. 192–206.   
[34] C. Liu, X. S. Wang, K. Nayak, Y. Huang, and E. Shi, “Oblivm: A programming framework for secure computation,” in 2015 IEEE Symposium on Security and Privacy. IEEE, 2015, pp. 359–376.   
[35] “Scale-mamba framework,” https://homes.esat.kuleuven.be/\~nsmart/SCALE/.   
[36] M. Keller, “Mp-spdz: A versatile framework for multi-party computation,” in Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications Security, 2020, pp. 1575–1590.   
[37] R. A. Popa, C. M. Redfield, N. Zeldovich, and H. Balakrishnan, "Cryptdb: Protecting confidentiality with encrypted query processing," in Proceedings of the Twenty-Third ACM Symposium on Operating Systems Principles, 2011, pp. 85–100.   
[38] Y. Sun, S. Wang, H. Li, and F. Li, “Building enclave-native storage engines for practical encrypted databases,” Proceedings of the VLDB Endowment, vol. 14, no. 6, pp. 1019–1032, 2021.   
[39] C. Sahin and A. El Abbadi, “Data security and privacy for outsourced data in the cloud,” in 2018 IEEE 34th International Conference on Data Engineering (ICDE). IEEE, 2018, pp. 1731–1734.   
[40] F. Hahn, N. Loza, and F. Kerschbaum, “Joins over encrypted data with fine granular security,” in 2019 IEEE 35th International Conference on Data Engineering (ICDE). IEEE, 2019, pp. 674–685.   
[41] M. Bellare, A. Boldyreva, and A. O'Neill, "Deterministic and efficiently searchable encryption," in Annual International Cryptology Conference. Springer, 2007, pp. 535-552.   
[42] O. Pandey and Y. Rouselakis, “Property preserving symmetric encryption,” in Annual International Conference on the Theory and Applications of Cryptographic Techniques. Springer, 2012, pp. 375–391.   
[43] Y. Wang and K. Yi, “Secure yannakakis: Join-aggregate queries over private data,” Proceedings of SIGMOD 2021, 2021.   
[44] S. Laur, R. Talviste, and J. Willemson, “From oblivious aes to efficient and secure database join in the multiparty setting,” in International Conference on Applied Cryptography and Network Security. Springer, 2013, pp. 84–101.   
[45] B. Pinkas, T. Schneider, C. Weinert, and U. Wieder, “Efficient circuit-based psi via cuckoo hashing,” in Annual International Conference on the Theory and Applications of Cryptographic Techniques. Springer, 2018, pp. 125–157.   
[46] B. Pinkas, T. Schneider, O. Tkachenko, and A. Yanai, “Efficient circuit-based psi with linear communication,” in Annual International Conference on the Theory and Applications of Cryptographic Techniques. Springer, 2019, pp. 122–153.

[47] P. Mohassel, P. Rindal, and M. Rosulek, “Fast databases and psi for secret shared data,” in Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications Security, 2020, pp. 1271–1287.   
[48] Y. Li, D. Ghosh, P. Gupta, S. Mehrotra, N. Panwar, and S. Sharma, "Prism: Private verifiable set computation over multi-owner outsourced databases," in Proceedings of the 2021 International Conference on Management of Data, 2021, pp. 1116-1128.   
[49] W. Zheng, A. Dave, J. G. Beekman, R. A. Popa, J. E. Gonzalez, and

I. Stoica, “Opaque: An oblivious and encrypted distributed analytics platform,” in 14th {USENIX} Symposium on Networked Systems Design and Implementation ( $\{NSDI\}$ 17), 2017, pp. 283–298.   
[50] W. Wang, G. Chen, X. Pan, Y. Zhang, X. Wang, V. Bindschaedler, H. Tang, and C. A. Gunter, “Leaky cauldron on the dark land: Understanding memory side-channel hazards in sgx,” in Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, 2017, pp. 2421–2434.