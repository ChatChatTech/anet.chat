# Secure Undirected-Graph Computation Towards Efficiency and Scalability

Jialiang Wang∗, Lan Zhang∗, Jiandong Liu∗, Feng Han∗†

∗ School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

† Alibaba Group, Hangzhou, China

{wjl937672039, jdliu}@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, fengdi.hf@alibaba-inc.com

Abstract—Collaborative analysis on graph data from diverse sources has shown great promise in finance, social networking, and predictive modeling. However, efficiently collaborative graphdata computations involving different parties while ensuring data privacy pose a significant challenge. To address this issue, we introduce a novel secure undirected-graph message passing (SUMP) protocol, which is specially optimized for secure analysis of undirected graph data. Our SUMP algorithm adopts a newly designed encoding paradigm to reduce the processing overhead in existing algorithms. The data scale in processing is reduced by around 2× in our SUMP algorithm compared to existing works. We apply SUMP to implement a graph-analysis framework, Topk common neighbors (TKCN), which facilitates analyzing the relationships related to entities in graphs. To further optimize the efficiency and scalability, we adopt fewer and more efficient secure binary operations, differently from numerous expensive secure comparison operations in existing implementations. Our evaluations on real-world datasets demonstrate that, our SUMP algorithm accelerates the state-of-the-art by 1.99×. Our secure TKCN implementation achieves a speed up by 700× over the state-of-the-art on large-scale datasets.

Index Terms—secure multi-party computation, graph analysis, MPC

# I. INTRODUCTION

Collaborative graph data analysis [1], [2] has proven to be effective for data-analytic tasks involving graphs from different parties. Such applications include infectious disease tracking [2], advertising recommendations [1], and traffic control [1]. However, privacy concerns are integral in such applications since the graph data usually contains privacy information related to individuals. For example, in infectious disease tracking, different communities collaborate to find suspected infected persons timely based on their collected graphs describing the contacts of their inhabitants. In this application, it is crucial to ensure that the computation process does not leak the private information of inhabitants. Thus, it is a critical task to design a secure graph computation protocol that can efficiently conduct various collaborative graph analysis tasks without privacy leakage.

Existing works have designed several secure graph computation protocols [1], [2], [3], [4] for both directed and undirected graphs based on secure multi-party computations (MPC) [5], [6]. These protocols designed graph analysis frameworks based on message passing, which facilitates data analysis by exchanging and updating data attached to different nodes in a graph. Typical graph analytic implementations enforced by message passing include top-k common neighbors (TKCN) [7], [8], which evaluates the correlations of nodes in graphs via the number of their common neighbors. Current works enhance the security of message passing by ensuring its data-processing steps satisfy the obliviousness requirement [1], [2], [9], i.e., the data access patterns and function calls are independent of the private inputs. Concretely, they optimize subprotocols in message passing including Sort, Shuffle, Scatter, Gather, Permute, and GetShares. However, existing works still suffer significant performance overhead primarily due to the fact that the obliviousness requirement boils up the processed data volumes and processing steps.

To understand the performance bottleneck, we revisit the data processing steps in existing designs and identify the critical points that lead to boil-up in processing overhead. We note that existing works encode an input graph as a tuple list of its nodes and direct edges from sources to destinations. Existing works encode node a with data d as $( a , a , d )$ and the direct edge from node a to b with data d as a threeitem tuple, $( a , b , d )$ . Then, the parties conduct data analytic tasks by passing messages from each node a to its outneighbors and updating the data on nodes and edges based on a prespecified rule. However, this design incurs additional preprocessed data volume for undirected graphs as each edge needs to be encoded as two opposite-directional edges between its incident nodes.

Inspired by the aforementioned observations, we design a more efficient secure undirected-graph message passing (SUMP) protocol. To improve the efficiency of messagepassing frameworks on undirected graphs, our SUMP protocol encodes the input graph more effectively and reduces the size of data involved in computing while ensuring functionality and security. Instead of representing each edge in an undirected graph as two opposite-direction tuples as in existing works, we store each edge in a single tuple. However, directly removing a tuple in one direction is inapplicable since in message passing, data needs to be passed in both directions between nodes, and the data on edges are updated separately from different directions. To overcome this obstacle, we enforce the tuple structure with an additional field to store data in both directions. That is, the edge between a and b is now encoded as $( a , b , d _ { 1 } , d _ { 2 } )$ , where $d _ { 1 }$ and $d _ { 2 }$ are data for different directions. Further, our protocol avoids extra data fields from participating in Sort, Shuffle and Permute, to save overhead, while previous works involve all data. In this way, the data volume in processing is reduced by roughly half without sacrificing functionality. We further simplify the data structure for particular graph analytic tasks that consist of idempotent operations [10] like TKCN and Maximal Independent Set [2], where one data field is sufficient as we prove that the data attached to edges in both directions are always identical. In this case, our SUMP archives much improved practical efficiency.

TABLE I   
COMPUTATION OVERHEADS MEASURED BY SECURE COMPUTATION GATES OF SUB-PROTOCOLS IN MESSAGE-PASSING FRAMEWORK1. 

<table><tr><td>Methods</td><td>Sort</td><td>Shuffle</td><td>Scatter/Gather</td><td>Permute</td><td>GetShares</td></tr><tr><td>SOTA [2]</td><td> $C_1Nlog^2(N)$ </td><td> $C_2Nd$ </td><td> $C_3Nlog(N)$ </td><td> $C_4dN$ </td><td> $C_5dN$ </td></tr><tr><td>SUMP</td><td> $C_1nlog^2n$ </td><td> $C_2nd$ </td><td> $C_3nlogn$ </td><td> $C_4(d+r)n$ </td><td> $C_5(d+r)n$ </td></tr><tr><td> $\text{SUMP-O}^2$ </td><td> $C_1nlog^2n$ </td><td> $C_2nd$ </td><td> $C_3nlogn$ </td><td> $C_4dn$ </td><td> $C_5dn$ </td></tr></table>

1 For undirected graph G(V,E), $N = | v | + 2 | E | , n = | v | + | E |$ . Sorting, Shuffle, Scatter, Gather, Permute, and GetShares are sub-protocols mentioned before. d is the bit-length for encoding an edge with one data field, and r is the bit-length of one data field. $C _ { i } , i \in [ 5 ]$ are constants.   
2 SUMP-O is the SUMP protocol particularly optimized for idempotent tasks.

As an important application, we implement efficient and secure TKCN based on SUMP. In addition to the performance improvement offered by SUMP, we also optimize the efficiency of TKCN by replacing the precise neighboring match-up in current implementations [11]with a probabilistic match-up via bitmap [12], which computes the approximate number of common items in two input lists. In this way, the neighboring match-ups in TKCN can be completed via fewer and more efficient secure binary operations in bitmaps instead of more expensive secure comparisons in existing works, which greatly speeds up TKCN.

Our main contributions are summarized as follows:

• A more efficient protocol, SUMP for secure undirected-graph computations. Our proposed secure undirected-graph computation protocol, SUMP achieves superior performance compared to the state-of-the-art [2] via more effective data encoding and processing strategies for undirected graphs. The detailed comparisons are summarized in Table I. Moreover, for graph analytic tasks that consist of idempotent operations, we further simplify the processed data structure to reduce the data redundancy and improve the practical efficiency of SUMP.   
• A scalable top-k common neighbors (TKCN) implementation based on SUMP. We implement a scalable TKCN algorithm for collaboratively graph tasks, which greatly speeds up the current implementations [11] based on our improved SUMP and an optimized probabilistic neighboring match-up strategy. Our implementation using efficient secure binary operations reduces the computation complexity of current methods by a factor of $O ( d ^ { 2 } / \ell ) ( \ell \ll d ^ { 2 } )$ , where l is bit-length for encoding one data field and d is a tunable constant that controls the approximation accuracy in matching neighbors in TKCN.

These advantages render our implementations scalable for large-scale graphs with numerous data sizes.

• Practical speeds up in secure collaborative graph analysis validated via abundant experiments. Our experiments on real-world datasets attest to the merit of our SUMP and TKCN implementations in terms of efficiency. Our SUMP protocol achieves a 1.31× to $1 . 9 9 \times$ speed up compared to the state-of-the-art [2]. Our TKCN implementation reduces the time cost of the current implementation [11] by a factor of 100 to 700 and shows to be scalable in large-scale graphs.

The outline of the paper is as follows. We introduce preliminary and necessary knowledge in Section II. Then, we introduce the security model and workflow in Section III. TSubsequently, we present the specific protocol design of SUMP in Section IV and the protocol design of TKCN in Section V. Finally, we present the experimental design and results for verifying efficiency and scalability in Section VI.

# II. PRELIMINARIES

In this section, we introduce notations and some relevant concepts from the literature of secure graph computations.

# A. Notations

We first introduce the notations utilized in this paper. In graph computations, $\mathcal { G } = ( \nu , \mathcal { E } )$ defines a graph, where each node $\tt v \in \mathcal { V }$ has the form of $\boldsymbol { \mathrm { v } } = ( \boldsymbol { \mathrm { v } } . i d , \boldsymbol { \mathrm { v } } . v a l )$ , and each edge $\textsf { e } \in { \mathcal { E } }$ has the form $\boldsymbol { \mathsf { e } } = ( ( \boldsymbol { \mathsf { u } } . i d , \boldsymbol { \mathsf { v } } . i d ) , \boldsymbol { \mathsf { e } } . v a l )$ . We uniformly denote the attributes val of a node (or an edge) as its payload. We denote an upper letter X as a vector with elements $X =$ $( X _ { 1 } , \ldots , X _ { n } )$ , a bold upper letter T as a matrix consisting of multiple column vectors with the same length $l _ { \mathbf { T } }$ . We denote $\mathbf { T } [ i ]$ as the $i ^ { t h }$ column vector of T, $\mathbf { T } _ { j }$ as the $j ^ { t h }$ row vector of T, and $\mathbf { T } _ { j } [ i ]$ as the the $j ^ { t h }$ element of $\mathbf { T } [ i ] .$ . We denote a length-n permutation as $\pi = ( \pi ( 1 ) , \pi ( 2 ) , \ldots , \pi ( n ) )$ , $Y =$ $\pi \circ X$ means applying π on a vector X, which outputs $Y =$ $( X _ { \pi ( 1 ) } , \ldots , X _ { \pi ( n ) } ) . \pi ^ { - 1 }$ means the inverse of permutation π. We denote $a | b$ as the result of concatenating two values $a , b ,$ and $X | Y$ as a new vector whose $i ^ { t h }$ element is $X _ { i } | Y _ { i }$ . If ∀x ∈ $X , x \in \{ 0 , 1 \}$ , we denote ¬X as the vector whose $\cdot i ^ { t h }$ element is $1 - X _ { i }$ . Given a vector X, we denote $s _ { i } ^ { X } = \{ j | 1 \leq j \leq$ $i , X _ { j } = X _ { i } \}$ as a set of indexes of elements that equal to $X _ { i }$ and appear before $X _ { i }$ in X , and $p _ { i } ^ { X } = \{ j | i \leq j \leq n , X _ { j } =$ $X _ { i } \}$ means set of elements that that equal to $X _ { i }$ and appear after $X _ { i }$ in X. Due to the space constraint, we omit the details of the underlying secret sharing schema and simply write ⟨v⟩ to refer to the shared value of v. We denote $\langle \mathbf { W } \rangle \gets \langle \mathbf { X } \rangle \cdot \langle \mathbf { Y } \rangle$ as $\langle W _ { i } \rangle  \langle X _ { i } \rangle \cdot \langle Y _ { i } \rangle$ which $" \cdot "$ means the multiply/XOR operation between two shared vectors. Given a function $\otimes :$ $\mathbb { F } \times \mathbb { F }  \mathbb { F }$ , $\forall a , b , c \in \mathbb { F } \colon 1 )$ if $a \otimes b = b \otimes a ,$ then it is commutative; 2) if $a \otimes b \otimes c = ( a \otimes b ) \otimes c ,$ then it is associative; 3) if $a \otimes a = a .$ , then it is idempotent.

# B. Secure functionalities

Our protocol requires the following secure functionalities in [2], [13].

1) $\langle \mathbf { T } ^ { \prime } \rangle  \mathcal { F } _ { s h u f f l e } ( \langle \mathbf { T } \rangle )$ : It takes a shared matrix ⟨T⟩ as input and outputs $\langle \mathbf { T } ^ { \prime } \rangle = ( \langle \mathbf { T } _ { \sigma ( 1 ) } \rangle , \allowbreak . . . , \langle \mathbf { T } _ { \sigma ( l _ { \mathbf { T } } ) } \rangle )$ , where σ is a length-lT random permutation.   
2) $\pi  \mathcal { F } _ { s o r t } ( \langle X \rangle )$ : It takes a shared vector ⟨X⟩ as input, and outputs a permutation π which satisfies $X _ { i } \leq X _ { j + 1 }$ for $j \in [ 1 , | X | )$ .   
3) $\langle Y \rangle \gets \mathcal { F } _ { a g g } ( \langle X \rangle , \langle V \rangle , \bigoplus , D i r ) \colon$ : It takes two length-n shared vectors $\langle X \rangle , \langle V \rangle$ , where X is sorted, and a public associative aggregate function L as input. It outputs ⟨Y ⟩ such that for $i \in [ 1 , n ] , Y _ { i } = \bar { \bigoplus } _ { j \in s _ { i } ^ { X } } V _ { j }$ if $D i r = t r u e$ , and $Y _ { i } = \bigoplus _ { j \in p _ { i } ^ { X } } V _ { j }$ otherwise.

# C. Message passing framework

We adopt and optimize the message passing framework for secure graph computation proposed in [2]. Similarly as in [2], a graph G is represented as a matrix $\mathbf { G } = ( U , V , F , D )$ . Here, $f l a g \in F$ marks whether the tuple is a node or an edge, and $d a t a \ \in \ D$ represents the data belonging to this tuple. For each node $\tt v \in \mathcal { V }$ and each edge $( ( \mathfrak { u . i d } , \mathfrak { v . i d } ) , \mathbf { e . v } a l ) \in \mathcal { E }$ , there exists a row vector $( \boldsymbol { \mathrm { v } } . i d , \boldsymbol { \mathrm { v } } . i d , 0 , \boldsymbol { \mathrm { v } } . v a l )$ and a row vector $( \mathfrak { u } . i d , \mathfrak { v } . i d , 1 , \mathfrak { e } . v a l )$ in G, respectively.

The protocol design of message passing is composed of preprocessing and online phases after the parties secretly share the input graph G. In its preprocessing phase, the parties compute $\bar { \langle \mathbf { G } ^ { 1 } \rangle } \bar {  } \mathcal { F } _ { s h u f f l e } \bar { ( \langle \mathbf { G } \rangle ) }$ ) and $\langle \bar { \mathbf { G } } ^ { \hat { 2 } } \rangle \gets \mathcal { F } _ { s h u f f l e } ( \langle \mathbf { G } ^ { 1 } \rangle )$ . $\mathbf { W . L . O . G }$ , we assume σ is the permutation in the second invocation of $\mathcal { F } _ { s h u f f l e } ,$ which means $\mathbf { G } ^ { 2 } = \sigma \circ \mathbf { G } ^ { 1 }$ . Then, the parties compute $\boldsymbol \pi _ { s } \gets \mathcal { F } _ { s o r t } ( \langle \mathbf G ^ { 1 } [ 1 ] | \mathbf G ^ { 1 } [ 3 ] \rangle )$ and $\pi _ { d } ~ $ $\mathcal { F } _ { s o r t } ( \langle \mathbf { G } ^ { 2 } [ 2 ] | \mathbf { G } ^ { \hat { 2 } } [ 3 ] \rangle )$ ). In its online phase, a message passing consists of three steps.

1) Scatter: Each node sends a message on its outgoing edges. The parties compute $\langle \mathbf { G } ^ { s } \rangle = \langle \pi _ { s } \circ \mathbf { G } ^ { 1 } \rangle$ , update the values of $\langle \mathbf { G } ^ { s } [ 4 ] \rangle$ by computing $\langle \mathbf { G } ^ { s } [ 4 ] \rangle = \dot { \bf \Phi } \lnot \langle \mathbf { \bar { G } } ^ { s } [ 3 ] \rangle \cdot \langle \mathbf { G } ^ { s } [ 4 ] \rangle$ and $\langle \mathbf { G } ^ { s } [ 4 ] \rangle  \mathcal { F } _ { a g g } ( \langle \mathbf { G } ^ { s } [ 1 ] \rangle , \langle \mathbf { \bar { G } } ^ { s } [ 4 ] \rangle , + , t r u e )$ .   
2) Gather: Each node gathers all messages from its incoming edges. The parties compute $\langle \mathbf { G } ^ { d } \rangle$ by invoking $\mathcal { F } _ { s h u f f l e } \mathrm { : }$ $\langle \mathbf { G } ^ { d } \rangle = \langle ( \pi _ { r } ^ { - 1 } \circ \sigma \circ \pi _ { s } ) \circ \mathbf { G } ^ { s } \rangle$ , and compute $\langle Y \rangle \gets$ $\mathcal { F } _ { a g g } ( \langle \mathbf { G } ^ { d } [ 2 ] \rangle , \langle \mathbf { G } ^ { d } [ 4 ] \rangle , \oplus , f a l s e )$ .   
3) Apply: Each node updates its payload based on gathered messages. The parties update the value of $\langle \mathbf { G } ^ { d } [ 4 ] \rangle$ with $\langle \mathbf { G } _ { i } ^ { d } [ 4 ] \rangle = \oplus ( \langle \bar { \mathbf { G } } _ { i } ^ { d } [ 4 ] \rangle , \langle \bar { Y } _ { i } \rangle )$ ), and compute $\langle \mathbf { G } ^ { s } \rangle = \langle ( \pi _ { r } \circ$ $\bar { \sigma } ^ { - 1 } \circ \pi _ { d } ^ { - 1 } ) \circ \mathbf { G } ^ { d } \rangle$ .

# III. SYSTEM OVERVIEW

Architecture and security model. The system architecture and workflow are shown in Fig. 1. Our system involves three roles: data owners, computing parties, and clients. Each data owner has a private graph and is willing to contribute his own data for collaborative analysis. The computing parties answer queries from clients on the graph which is the result of concatenating all graphs together. Our framework contains three semi-honest non-colluding computing parties, which means they won’t deviate from the agreed protocol but may try to infer the information of private graphs during the computation. The number of computing parties is related to the underlying MPC protocol, and our implementation based on ABY3 [6] requires three computing parties. There is no restriction on the number of data owners and clients, and Data owners or clients can also act as the computing parties as long as the security assumption is not violated.

Security analysis. We assume the queries and the scale of graphs are public knowledge similar to [2]. We follow the standard security model same as [6]. The security objective of the system is answering queries without any information leakage expect for the scale of graphs. Our following protocols are the sequential composition of individual secure functionalities mentioned in Section II and the security of these underlying protocols has been proved in [2], [6], [13]. All intermediate results of these functionalities can be simulated with random strings having the same length, which directly clarifies the security of our protocol. In conclusion, The security of our protocols is directly implied via standard composition theorems [14] if all basic protocols are secure. Due to space constraints, we omit the formal security proof.

Workflow. The workflow of our framework can be divided into two phases: 1) In the preprocessing phase, each data owner generates the matrix representation of his own graph as described in Section II, and secret shares the data to the computing parties. 2) In the computation phase, once all data owners confirm a specific query proposed by the client, the computing parties generate and execute the secure protocol to generate the result in the secret sharing form and send the result to the client. Finally, the client reconstructs the result. Steps ⃝1 -⃝3 in Fig. 1 correspond to our optimization techniques.

# IV. PROTOCOL DESIGN FOR SUMP

In this section, we present the design of an efficient secure undirected-graph message passing (SUMP) protocol for collaborative graph analysis, which significantly speeds up the state-of-the-art message passing protocols on undirected graphs. Our SUMP protocol achieves improved performance by encoding the input undirected graph data more effectively, reducing the processed data volumes and avoiding additional data fields from participating in secure operations as much as possible. Specifically, for universal computation tasks, SUMP reduces the data volumes by roughly half by storing the passed data between two nodes in both directions in a single tuple instead of two as in existing works [2]. Moreover, for tasks consisting of idempotent operations, we prove the data in both directions are always identical and the number of data fields can be further reduced.

![](images/149342141a40258423b5e0e09c8f510737b6c0ceb9a97f4c4e7ac54816f45bcf.jpg)



Fig. 1. The workflow of our system. In the P reprocessing P hase, the data owners process and represent the data according to our specified preprocessing steps and data structures. Subsequently, the original data is securely and confidentially shared among three computing parties using MPC tools. The computing parties execute the agreed-upon algorithms during the online phase, following the conventions established by the data owners and the querying entities. Finally, the results are delivered to the querying entities. Step ⃝1 represents "Trading more data fields for fewer tuples", step $\textcircled{2}$ represents "Halving the data fields for idempotent operations" and ⃝3 represents "Reducing the cost of TKCN utilizing bitmap".

# A. Protocol Design for Universal Computation Tasks

Our main idea for designing SUMP is "More data fields are better than more tuples". As we mentioned in Section II, the cost of secure algorithms is associated with four numbers: the total number of tuples n, the bit length of one tuple m, the bit length of sorted key k and the bit length of data field d. Doubling tuples influences all secure algorithms, Sort, Shuffle, Scatter, Gather, Permute, and GetShares. However, when using an extra data field to finish bidirectional message passing, only Permute and once-only Getshares are influenced by $m ^ { \prime } \ = \ m + d$ while baseline cost also increases as $n ^ { \prime } = n + | E |$ . We design the SUMP protocol while avoiding extra data fields from participating in all secure operations to save costs.

Offline preprocessing phase. The data owners will perform the following preprocessing steps on the undirected graph data $G ( V , E )$ : Each node and edge is represented as a tuple that contains two data fields $( u , v , d _ { 1 } , d _ { 2 } )$ ). Then sorting the plaintext data according to keywords u||v.

Online message-passing phase. In the online messagepassing phase, we need to send and receive messages on the same edge. We still use scatter/gather to represent send (receive) messages from one node to another. Every node u sends its original data to $d _ { 1 }$ of its edges and then exchanges the direction to let every node v send its original data to $d _ { 2 }$ of edges. Then every node v receives the data message from u and stores it in temp data field $d _ { 2 }$ and exchanges the direction. Every node u receives the data message from v and stores it in temp data field $d _ { 2 }$ . Without loss of generality, we assume that the initial tuple list is sorted by src field. Fig. 2 shows details.

# B. Optimization for Idempotent-Operation-Based Computation Tasks

Through our observation of commonly used operations, we have identified their idempotent property. Leveraging this property, we can further optimize the SUMP protocol to simultaneously avoid an increase in both additional data fields and tuples. When we focus on those functions that have the idempotent property, we can find that the data from u and v can be directly computed on edge tuples and the result can be stored in only one data field. Firstly, we explain the correctness of this approach in layman’s terms: the idempotent nature of operations ensures that repetitive computations of the same element do not impact the final result. Commonly used operations, such as Gather algorithms with L = AND/OR/MAX/MIN all meet this property. Fig. 3 shows details.

# V. APPLICATION: SUMP-BASED TOP-K COMMON NEIGHBORS

Built upon the SUMP framework established in Section IV, we implement a widely adopted graph analytic algorithm, topk common neighbors (TKCN), which reflects the correlations of nodes in graphs using the number of their common neighbors. Our algorithms reduce the computation complexity of current implementations by a factor of $O ( d ^ { 2 } / \ell ) ( \ell ~ \ll ~ d ^ { 2 } )$ and each computation step in our implementation is cheaper. Here l is the bit-length for encoding the data field and d is a tunable constant that controls the approximation accuracy. In addition to the speed-up offered by SUMP, we further optimize the TKCN efficiency by calculating the number of common neighbors approximately using bitmap [12]. These improvements render our TKCN implementations scalable for large-scale graphs, which cannot be achieved by current implementations [2].The design of secure TKCN is divided into two parts, namely how to calculate CN and how to safely output the k nodes which have Top-k CN values corresponding to each node.

Notation: $\langle \mathbf { G } ^ { s } \rangle \gets \mathcal { P } _ { \mathtt { S U M P } } ( \mathbf { \langle { G } ^ { s } \rangle } , \pi _ { r } , \pi _ { d } , \sigma , \oplus )$   
Parameters: A shared matrix $\langle \mathbf { G } ^ { s } \rangle = ( \langle \overline { { U } } \rangle , \langle V \rangle , \langle F \rangle , \langle D \rangle )$ , two permutation in plaintext πr and $\pi _ { d } ,$ a secret permutation $\sigma ,$ and a public aggregate function L.   
Protocol:   
1) The parties update the values of $\langle \mathbf{G}^s [4]\rangle$ : $\langle \mathbf{G}_i^s [4]\rangle = \neg \langle F_i\rangle \cdot \langle \mathbf{G}_i^s [4]\rangle$ .

2) The first scatter process: $\langle \mathbf{G}^s [4]\rangle \leftarrow \mathcal{F}_{\mathrm{agg}}(\langle \mathbf{G}^s [1]\rangle, \langle \mathbf{G}^s [4]\rangle, \bigoplus, true)$ .

3) The first gather process: the parties invoke $\mathcal{F}_{\mathrm{shuffle}}$ to compute $\langle \mathbf{G}^d\rangle = \langle (\pi_r^{-1} \circ \sigma \circ \pi_s) \circ \mathbf{G}^s\rangle$ . Then the parties compute $\langle A\rangle$ : $\langle A_i\rangle = \neg \langle F_i\rangle \cdot \langle \mathbf{G}_i^d [4]\rangle$ for $i \in [1,n]$ . and update the values of $\langle \mathbf{G}^d [4]\rangle$ : $\langle \mathbf{G}^s [4]\rangle \leftarrow \mathcal{F}_{\mathrm{agg}}(\langle \mathbf{G}^s [1]\rangle, \langle \mathbf{G}^s [4]\rangle, \bigoplus, false)$ .

4) The second scatter process: The parties compute a new shared column vector $\langle \mathbf{G}^d\rangle$ : $\langle \mathbf{G}^d [5]\rangle \leftarrow \mathcal{F}_{\mathrm{agg}}(\langle \mathbf{G}^s [2]\rangle, \langle A\rangle, \bigoplus, true)$ .

5) The second gather and the final apply process:
- The parties invoke $\mathcal{F}_{\mathrm{shuffle}}$ to compute $\langle \mathbf{G}^n\rangle = \langle (\pi_r \circ \sigma^{-1} \circ \pi_s^{-1}) \circ \mathbf{G}^d\rangle$ .
- Update $\langle \mathbf{G}^n [5]\rangle$ : $\langle \mathbf{G}^n [5]\rangle \leftarrow \mathcal{F}_{\mathrm{agg}}(\langle \mathbf{G}^s [1]\rangle, \langle \mathbf{G}^n [5]\rangle, \bigoplus, false)$ .
- Update $\langle \mathbf{G}^s [4]\rangle$ with $\langle \mathbf{G}_i^s [4]\rangle = \bigoplus (\langle \mathbf{G}_i^s [4]\rangle, \langle \mathbf{G}_i^n [4]\rangle, \langle \mathbf{G}_i^n [5]\rangle)$ for $i \in [1,n]$ .

Output: $\langle \mathbf{G}^s\rangle = (\langle U\rangle, \langle V\rangle, \langle F\rangle, \langle D\rangle)$   
Fig. 2. Secure universal message passing protocol

Notation: $\langle \mathbf { G } ^ { s } \rangle \gets \mathcal { P } _ { \mathtt { S U M P - 0 } } ( \mathbf { \langle \mathbf { G } ^ { s } \rangle } , \pi _ { r } , \pi _ { d } , \sigma , \bigoplus )$   
Parameters: Same as $\mathrm { F i g } . 2$   
Protocol After step 3 of $\mathrm { F i g . } \ 2 { : }$   
4) The second scatter process: The parties update values of $\langle \mathbf{G}^d [4]\rangle \leftarrow \langle \mathbf{G}^d [4]\rangle \oplus \mathcal{F}_{\mathrm{agg}}(\langle \mathbf{G}^s [2]\rangle ,\langle A\rangle ,\bigoplus ,true)$ .  
5) The second gather and the final apply process:  
- The parties invoke $\mathcal{F}_{\mathrm{shuffle}}$ to compute $\langle \mathbf{G}^n\rangle = \langle (\pi_r\circ \sigma^{-1}\circ \pi_s^{-1})\circ \mathbf{G}^d\rangle$ .  
- Update $\langle \mathbf{G}^n [4]\rangle :\langle \mathbf{G}^n [4]\rangle \leftarrow \mathcal{F}_{\mathrm{agg}}(\langle \mathbf{G}^s [1]\rangle ,\langle \mathbf{G}^n [4]\rangle ,\bigoplus ,false)$ .  
- Update $\langle \mathbf{G}^s [4]\rangle$ with $\langle \mathbf{G}_i^s [4]\rangle = \bigoplus (\langle \mathbf{G}_i^s [4]\rangle ,\langle \mathbf{G}_i^n [4]\rangle ,\langle \mathbf{G}_i^n [4]\rangle)$ for $i\in [1,n]$ .  
Output: $\langle \mathbf{G}^s\rangle = (\langle U\rangle ,\langle V\rangle ,\langle F\rangle ,\langle D\rangle)$   
Fig. 3. Secure universal message passing protocol optimized idempotent operation.

TKCN. For calculating CN, we design an efficient CN algorithm based on the Bitmap data structure with AND/OR/Max operations and optimize protocols for these operations. Simultaneously, in practical applications, it’s common to use the topk closest neighboring nodes of each node as objects for further analysis [8], [15], [16], [17]. Directly outputting the number of common neighbors for all node pairs will leak the topology of the graph. Furthermore, we have converted conditional statements related to data into data oblivious expressions for outputting the Top-k value safely. Fig. 4 gives the detailed design. Specifically, in the offline stage, we agree on a value r and a hash function h based on the maximum degree of the graph owned by each data owner, in which r represents the length of the Bitmap. Before online calculation, the data owner will set the data field of each node to a Boolean array B[r] of length r based on the agreed hash function h. Firstly, initializing ∀ node $u \in \textit { V } , u . \mathbf { B } = \textbf { 0 }$ , then for neighbor v ∈ neighbors(u), u.B[h(v)] = 1.

Analysis of complexity improvement. In step 6 of the protocol 4, we performed bitwise AND operations on two secretly shared bitmaps. Each bitmap has a length of l. The overall cost comes from N l bitwise AND operations of secret shared values, requiring O(1) rounds of communication and a communication cost of O(N l). If $\langle \mathbf { G } \rangle [ 4 ]$ stores d node IDs for comparison, then each comparison between pairs of neighbor sets requires $d ^ { 2 }$ comparisons of secret shared values (more costs than AND). The total number of comparisons becomes $O ( N d ^ { 2 } )$ . Thus, the final speed up rate of TKCN is $\begin{array} { r } { O ( \frac { d ^ { 2 } } { l } ) , \ell \ll d ^ { 2 } } \end{array}$ .

# VI. EXPERIMENTS AND EVALUATIONS

In this section, we present experimental results that compare the efficiency of our SUMP protocol and TKCN implementations with the state-of-the-art [2], [11] on real-world graph datasets with various graph scales and data loads for nodes/edges.

# A. Implementation and Experiment Setup

We implement our SUMP protocols and TKCN implementations and compare their efficiency with the state-of-the-art baselines [2] by conducting graph computation tasks across various real-world datasets.

Implementation details. We implement our protocols based on Java. We need to point out that our experiment is based on the classic 6 rounds of secret shuffling [2] and parallel prefix networks of Scatter/Gather [13]. The improvement we have made is aimed at the secure undirected message passing framework itself, rather than a specific security protocol. Other existing works [1], [3] can also benefit from our optimizations.

Experimental setup and datasets. We evaluate our framework on one physical machine with Intel ® Core TM i5- 11500H 2.70GHz CPU and 16GB RAM. We considered two native undirected graph datasets, Facebook [18] and Wiki [19] and two common directed graph datasets, Cora [20] and CiteSeer [21] in the field of graph federation learning research [22] which can also be used as undirected graph data (like

Notation: $\mathbf { T }  \mathcal { P } _ { \mathrm { T K C N } } ( \mathbf { \partial } \langle \mathbf { G } ^ { s } \rangle , \pi _ { r } , \pi _ { d } , \sigma , k )$

Parameters: A shared matrix $\langle \mathbf { G } ^ { s } \rangle = ( \langle U \rangle , \langle V \rangle , \langle F \rangle , \langle D \rangle )$ , public hash function $h ,$ two permutation in plaintext $\pi _ { r }$ and $\pi ,$ a secret permutation $\sigma ,$ and an integer k.

# Protocol:

1) Initialization: The data owner parties set the values of $\mathbf { B } , \mathbf { B } [ h ( \mathbf { V } ) ] = 1 ,$ , others 0.   
2) The parties update the values of $\langle \mathbf { G } _ { i } ^ { s } [ 4 ] \rangle \colon \langle \mathbf { G } ^ { s } [ 4 ] \rangle \gets \mathcal { F } _ { S U M P } ( \mathbf { \Sigma } \langle \mathbf { \dot { G } } ^ { s } \rangle , \pi _ { r } , \pi _ { d } , \sigma , \bigoplus \mathbf { = } O R )$   
3) The parties update the values of $\langle \mathbf { G } ^ { s } [ \mathbf { 4 } ] \rangle \colon \langle \mathbf { G } _ { i } ^ { s } [ \mathbf { 4 } ] \rangle = \lnot \langle F _ { i } \rangle \cdot \langle \mathbf { G } _ { i } ^ { s } [ \mathbf { 4 } ] \dot { \rangle } .$   
4) Getting one neighbors: $\langle \mathbf { G } ^ { s } [ 4 ] \rangle \stackrel {  } {  } \mathcal { F } _ { \mathrm { a g g } } ^ {  } ( \langle \dot { \mathbf { G } } ^ { s } [ 1 ] \rangle , \langle \mathbf { G } ^ { s } [ 4 ] \rangle , \bigoplus = \dot { O } \dot { R } , t r u e ) .$   
5) Getting another neighbors:the parties invoke $\mathcal { F } _ { \mathrm { s h u f f 1 e } }$ to compute $\langle \mathbf { G } ^ { d } \rangle \overset { ^ { \prime } } { = } \langle ( \pi _ { r } ^ { - 1 } \circ \sigma \circ \pi _ { s } ) _ { . } \circ \mathbf { G } ^ { s } \rangle$ . Then the parties compute $\langle A \rangle { \mathrm { : } }$ $\langle A _ { i } \rangle \stackrel { = } { = } \lnot \langle F _ { i } \rangle \cdot \langle \mathbf { G } _ { i } ^ { d } [ 4 ] \rangle$ for $i \in [ 1 , n ]$ . Then compute a new shared column vector $\langle \mathbf { G } ^ { d } \rangle \colon \langle \mathbf { { G } } ^ { d } [ 5 ] \rangle \longleftarrow \mathcal { F } _ { \mathrm { a g g } } ( \langle \mathbf { G } ^ { s } [ 2 ] \rangle , \langle A \rangle , \bigoplus , t r u e )$ .   
6) Neighbors set intersection process: The parties compute a new shared column vector into $\langle \mathbf { G } ^ { \lambda } \rangle \colon \langle \mathbf { G } ^ { d } [ 5 ] \rangle \gets \langle \dot { \mathbf { G } } ^ { d } [ 5 ] \rangle \wedge \langle \bar { \mathbf { G } } ^ { d } [ 4 ] \rangle$   
7) Counting neighbors: $\begin{array} { r } { \langle \mathbf { G } ^ { d } [ \hat { \mathbf { { \mathbf { 4 } } } } ] \rangle \gets \sum _ { i = 1 } ^ { r } \langle \hat { \mathbf { G } } ^ { d } [ 5 ] _ { i } \rangle } \end{array}$   
8) Finding Top-k neighbors for i from 1 to k:   
• The first gather process: $\langle \mathbf { G } ^ { d } [ 5 ] \rangle \gets \mathcal { F } _ { \mathrm { a g g } } ( \langle \mathbf { G } ^ { s } [ 2 ] \rangle , \langle \mathbf { G } ^ { d } [ 4 ] \rangle | \langle \mathbf { G } ^ { d } [ 1 ] \rangle , \bigoplus = M a x , t r u e ) .$   
• The second gather process:   
• Getting a Top-k node: $\langle \mathbf { T } [ i ] \rangle  \langle \mathbf { G } ^ { s } [ 5 ] \rangle [ L _ { \langle \mathbf { G } ^ { s } [ 4 ] \rangle } : L _ { \langle \mathbf { G } ^ { s } [ 4 ] \rangle | \langle \mathbf { G } ^ { s } [ 2 ] \rangle } ] $   
• The parties update the values of $\langle \mathbf { G } ^ { s } [ \bar { 5 } ] \rangle \dot { : } \langle \mathbf { { \dot { G } } } _ { i } ^ { s } [ \bar { 5 } ] \rangle = \dot { \lnot \langle F _ { i } \rangle } \dot { \cdot } \langle \dot { \mathbf { G } } _ { i } ^ { s } [ \bar { 5 } ] \rangle$   
• The first scatter process: $\langle \mathbf { G } ^ { s } [ 5 ] \rangle \gets \dot { \mathcal { F } } _ { \mathrm { a g g } } ^ { - } ( \langle \mathbf { G } ^ { s } [ 1 ] \rangle , \langle \mathbf { G } ^ { s } [ 5 ] \rangle , + , t r u e ) .$   
• The second scatter process: the parties invoke Fshuffle to compute $\langle \overset { \cdot } { \mathbf { G } } ^ { d } \rangle = \langle ( \pi _ { r } ^ { - 1 } \circ \sigma \circ \pi _ { s } ) \circ \mathbf { G } ^ { s } \rangle$ , and update the values of $\langle \mathbf { G } ^ { d } [ 5 ] \rangle \colon$ $\langle \mathbf { G } ^ { s } [ 5 ] \rangle \gets \mathcal { F } _ { \mathrm { a g g } } ( \langle \dot { \mathbf { G } } ^ { s } [ 1 ] \rangle , \langle \mathbf { G } ^ { s } [ 4 ] \rangle , + , f a l s e ) .$   
• Preparing for next round: The parties update $\langle \mathbf { G } ^ { d } [ 4 ] \rangle \gets ( \langle \mathbf { 1 } \rangle - \langle \mathbf { G } ^ { d } [ 5 ] \rangle = = \langle \mathbf { G } ^ { d } [ 1 ] \rangle ) \cdot ( \langle \mathbf { 1 } \rangle - \langle \mathbf { G } ^ { d } [ 5 ] \rangle = = \langle \mathbf { G } ^ { d } [ 2 ] \rangle ) \cdot \langle \mathbf { G } ^ { d } [ 4 ] \rangle .$   
Output: Open shared value ⟨T⟩

$$
\mathcal {F} _ {\text {shuffle}} \text {to compute} \langle \mathbf {G} ^ {s} \rangle = \left\langle \left(\pi_ {r} \circ \sigma^ {- 1} \circ \pi_ {s} ^ {- 1}\right) \circ \mathbf {G} ^ {d} \right\rangle . \text {Then} \langle \mathbf {G} ^ {s} [ 5 ] \rangle \leftarrow \mathcal {F} _ {\text {agg}} (\langle \mathbf {G} ^ {s} [ 1 ] \rangle , \langle \mathbf {G} ^ {s} [ 4 ] \rangle | \langle \mathbf {G} ^ {s} [ 2 ] \rangle , \bigoplus = M a x, f a l s e)
$$

Fig. 4. Secure TKCN protocol

Tensor [23] and Stellargraph [24]). Table II shows the original number of nodes and edges of datasets.

TABLE II THE GRAPH DATASETS UTILIZED IN OUR EXPERIMENTS. 

<table><tr><td>Dataset</td><td>Node number</td><td>Edge number</td><td>Mean degree</td><td>Max degree</td></tr><tr><td>Facebook [18]</td><td>4039</td><td>88234</td><td>21.8</td><td>1045</td></tr><tr><td>Wiki [19]</td><td>11631</td><td>170918</td><td>14.7</td><td>3546</td></tr><tr><td>Cora [20]</td><td>2708</td><td>5278</td><td>1.9</td><td>168</td></tr><tr><td>CiteSeer [21]</td><td>3264</td><td>4536</td><td>1.4</td><td>99</td></tr></table>

Baseline algorithms. We compare our SUMP protocol and TKCN implementation with the following two baselines:

1) Basic Message Passing (BMP): We choose one of the most efficient implementations of secure graph computation solutions [2] as a specific implementation.   
2) Basic Top-k Common Neighbors (B-TKCN): We choose the CN algorithm based on node ID comparison [11] as the baseline algorithm. Due to the need for a comparison algorithm that guarantees 100% accuracy, the data field length of each tuple needs to be set to be consistent with the maximum degree d in the graph, and $d ^ { 2 }$ operations are required for the objective property.

# B. Evaluation of SUMP

This section presents the efficiency comparison between our SUMP protocols and the state-of-the-art baseline, BMP on real-world datasets. It shows that our SUMP and SUMP-O (i.e., the SUMP protocol optimized for idempotent operations) achieve 1.31×-1.81× and 1.51×-1.99× speed up compared to the baseline, respectively.

We compare the running time of sub-protocols of our and the baseline message passing protocols and calculate the overall speedup offered by our protocols. The results are summarized in Table III. It shows that the efficiency of all subprotocols of our SUMP and SUMP-O protocols outperforms those for the BMP baseline. Overall, our SUMP and SUMP-O protocols speed up BMP by 1.31×-1.81× and 1.51×-1.99×, respectively. We then compare the offline and online running times of our and the baseline message passing protocols for different numbers of input tuples. The comparison are depicted in Fig. 5 and Fig. 6, which show that our SUMP and SUMP-

![](images/c6dd9b8c05335fd82cceebfe753ab2c439eb6893639cb2e85858849168d8cda5.jpg)



![](images/fd82ca8352f6208c8986bda094ebc5e7f98e55c174aa8a9ef644627e41bf7041.jpg)



Fig. 5. The offline runtime for Fig. 6. The online runtime for different scale of inputs. different scale of inputs.

![](images/4d8ae8b43308ddef814f73cb2bb979b6949ae70d40ae25ce00933ac7c2a7e53f.jpg)



![](images/d2c4449f1bd4e70e2995ed225dd123fd6eecba7c340f4a1123270fc4f4cc4b0e.jpg)



Fig. 7. The runtime of message Fig. 8. The running time of Bpassing for different data field TKCN and TKCN-S for different bitlengths. accuracy.

TABLE IIITHE RUNTIME(S) OF SUB-PROTOCOLS AND ONE MESSAGE PASSING ROUND.1

<table><tr><td>Dataset</td><td>Methods</td><td>Sort</td><td>Shuffle</td><td>Gather</td><td>Permute</td><td>GetShares</td><td>Speedup</td></tr><tr><td rowspan="3">Facebook [18]</td><td>BMP [2]</td><td>16409</td><td>846</td><td>4798</td><td>76</td><td>640</td><td>1</td></tr><tr><td>SUMP</td><td>8161</td><td>744</td><td>2343</td><td>69</td><td>561</td><td>1.76</td></tr><tr><td>SUMP-O</td><td>7552</td><td>383</td><td>2446</td><td>37</td><td>325</td><td>1.89</td></tr><tr><td rowspan="3">Wiki [19]</td><td>BMP [2]</td><td>40655</td><td>1978</td><td>11964</td><td>201</td><td>1131</td><td>1</td></tr><tr><td>SUMP</td><td>18194</td><td>1566</td><td>6075</td><td>183</td><td>997</td><td>1.81</td></tr><tr><td>SUMP-O</td><td>17789</td><td>993</td><td>5893</td><td>112</td><td>635</td><td>1.99</td></tr><tr><td rowspan="3">Cora [20]</td><td>BMP [2]</td><td>1516</td><td>97</td><td>591</td><td>16</td><td>288</td><td>1</td></tr><tr><td>SUMP</td><td>1025</td><td>84</td><td>486</td><td>11</td><td>120</td><td>1.31</td></tr><tr><td>SUMP-O</td><td>1064</td><td>47</td><td>394</td><td>5</td><td>77</td><td>1.51</td></tr><tr><td rowspan="3">CiteSeer [21]</td><td>BMP [2]</td><td>1419</td><td>78</td><td>590</td><td>14</td><td>55</td><td>1</td></tr><tr><td>SUMP</td><td>1074</td><td>75</td><td>564</td><td>10</td><td>139</td><td>1.45</td></tr><tr><td>SUMP-O</td><td>986</td><td>50</td><td>432</td><td>6</td><td>72</td><td>1.60</td></tr></table>

O achieve constantly over 2× speed-up as the number of tuples increases. We also compare the running time of message passing for different data field bit-lengths, which shows that SUMP and SUMP-O speed up BMP by around 2× for all data field lengths. It is also noteworthy that SUMP-O outperforms SUMP for large data-field lengths, which aligns with our analysis in Section IV-A.

TABLE IV THE RUNNING TIME COMPARISON IN SECONDS OF TKCN IMPLEMENTATIONS REGARDING WHETHER TO USE SUMP-O.2 

<table><tr><td>TKCN</td><td>Top-k</td><td>Facebook</td><td>Wiki</td><td>Cora</td><td>Cite Seer</td><td>Average speedup</td></tr><tr><td rowspan="3">BMP [2]</td><td>Top1</td><td>225.2</td><td>440.1</td><td>17.7</td><td>15.6</td><td>1</td></tr><tr><td>Top3</td><td>245.1</td><td>475.6</td><td>22.6</td><td>20.2</td><td>1</td></tr><tr><td>Top5</td><td>267.9</td><td>518.0</td><td>28.3</td><td>25.4</td><td>1</td></tr><tr><td rowspan="3">SUMP-O</td><td>Top1</td><td>113.5</td><td>213.4</td><td>12.0</td><td>10.2</td><td>1.67</td></tr><tr><td>Top3</td><td>125.1</td><td>233.1</td><td>16.0</td><td>14.0</td><td>1.81</td></tr><tr><td>Top5</td><td>138.8</td><td>256.4</td><td>20.6</td><td>18.5</td><td>1.99</td></tr><tr><td colspan="2">Average speedup</td><td>1.96</td><td>2.04</td><td>1.42</td><td>1.45</td><td>1.71/1.71</td></tr></table>

# C. Evaluation of TKCN

We compare our TKCN implementation with the state-ofthe-art baseline, B-TKCN [2] on the real-world Facebook dataset [18]. We use TKCN and TKCN-S (i.e., the TKCN implementation based on SUMP-O) to denote top-k common neighbors algorithm using bitmap and use B-TKCN to denote top-k common neighbors algorithm using ID comparison [11]. It shows that our TKCN implementation speeds up the B-TKCN baseline on all datasets with comparable accuracy. Especially on large-scale graph datasets, our TKCN-S accelerates the baseline by 100× to 700×.

Fig 8 shows that the runtimr of our TKCN-S over B-TKCN to achieve different accuracy levels on the Facebook dataset with k = 1, 3, 5, achieving comparable accuracy (From 50% to 90% and at each comparative juncture, the variance in accuracy between the two methods remains within the narrow margin of 1%, with Ours TKCN-S consistently exhibiting superior accuracy.) The speedup of our TKCN-S generally increases as the target accuracy level increases, which ranges from 100× to 700×. Our method can complete the calculation task in about a few hundred seconds, but achieving the same accuracy using the benchmark method can take hours or even days. We notice that our TKCN-S implementation achieves more significant speedup on larger datasets and larger values of k compared to B-TKCN. This property renders our implementation scalable in large-scale graphs. Also, we would like to demonstrate once again through the implementation of TKCN that our improvements to the basic protocol have been successful, and SUMP and SUMP-O are effective in practical use. Table IV shows that our TKCN-S implementation method achieves 1.71× average speedup on all datasets over the tasks of top-k common neighbors compared with TKCN implemented on state-of-art baseline [2]..

# VII. RELATED WORK

Secure graph computations have proven to be effective in collaborative graph analysis while ensuring data privacy [1], [2], [3]. Abundant literature [1], [2] has designed secure graph computation protocols based on secure multi-party computation (MPC). There are two main directions in the design of MPC-based secure graph computation protocols, the twoparty protocols represented by GraphSC [1] and the three-party protocols represented by Araki [2]. Both types of work focus on the same message passing framework of directed graph algorithms and can’t be used directly in undirected graph data efficiently as we mentioned in Section IV. To our knowledge, there is currently no specific research on the secure message passing framework for undirected graph.

Another line of works intends to complete secure graph computations via trusted execution environment (TEE) [25], [26] and differential privacy (DP) [27], [28], [29]. Although TEE can achieve higher efficiency compared to MPC-based solutions, it is also vulnerable to side-channel attacks [30] or requires additional trust assumptions. Regarding DP-based protocols, Mazloom et al.’s recent research [3], [27] implements message-passing algorithms within a relaxed security framework permitting the leakage of differentially private data. Other works [28], [29] also use differential privacy techniques in graph computation but their focus is not on the message passing algorithm.

# VIII. CONCLUSION

Secure graph computation is crucial for effective collaborative graph analysis while ensuring data privacy for involved parties. However, existing protocols suffer severe performance bottlenecks when applied in practice. Our SUMP protocol significantly improves the efficiency of state-of-the-art protocols [2] by reducing the data volume in processing by roughly half via novel message-encoding and protocol design. Via through analysis of tasks satisfying the idempotent [10] properties like TKCN, we then optimize the practical performance of SUMP for these tasks by further reducing the data fields in graphs by half without compromising the correctness. We implement the TKCN graph analytic algorithm based on SUMP and further optimize its efficiency via a carefully crafted approximation strategy to match up neighbors in graphs. Extensive experiments attest to the merit of our protocol designs in terms of efficiency, scalability, and accuracy.

# IX. ACKNOWLEDGEMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, and “the Fundamental Research Funds for the Central Universities” WK2150110024.

# REFERENCES

[1] K. Nayak, X. S. Wang, S. Ioannidis, U. Weinsberg, N. Taft, and E. Shi, “Graphsc: Parallel secure computation made easy,” in S&P. IEEE, 2015, pp. 377–394.   
[2] T. Araki, J. Furukawa, K. Ohara, B. Pinkas, H. Rosemarin, and H. Tsuchida, “Secure graph analysis at scale,” in CCS. ACM, 2021, pp. 610–629.   
[3] S. Mazloom, P. H. Le, S. Ranellucci, and S. D. Gordon, “Secure parallel computation on national scale volumes of data,” in Proceedings of the USENIX Security (2020), 2020, pp. 2487–2504.   
[4] N. Attrapadung, H. Morita, K. Ohara, J. C. N. Schuldt, T. Teruya, and K. Tozawa, “Secure parallel computation on privately partitioned data and applications,” in CCS. ACM, 2022, pp. 151–164.   
[5] A. C. Yao, “How to generate and exchange secrets (extended abstract),” in 27th Annual Symposium on Foundations of Computer Science, Toronto, Canada, 27-29 October 1986. IEEE Computer Society, 1986, pp. 162–167.   
[6] P. Mohassel and P. Rindal, “Aby3: A mixed protocol framework for machine learning,” in CCS(2018). ACM, 2018, pp. 35–52.   
[7] J. Shao, Z. Han, Q. Yang, and T. Zhou, “Community detection based on distance dynamics,” in SIGKDD. ACM, 2015, pp. 1075–1084.

[8] M. Wang, C. Wang, J. X. Yu, and J. Zhang, “Community detection in social networks: An in-depth benchmarking study with a procedureoriented framework,” Proceedings of the VLDB (2015)), vol. 8, no. 10, pp. 998–1009, 2015.   
[9] J. Kilian, “Founding cryptography on oblivious transfer,” in Proceedings of the 20th Annual ACM Symposium on Theory of Computing, May 2-4, 1988, Chicago, Illinois, USA, J. Simon, Ed. ACM, 1988, pp. 20–31. [Online]. Available: https://doi.org/10.1145/62212.62215   
[10] R. J. Valenza, Linear algebra: an introduction to abstract mathematics. Springer Science & Business Media, 2012.   
[11] MishaDemianenko, “Common neighbors,” 2023. [Online]. Available: https://neo4j.com/docs/graph-data-science/current/alphaalgorithms/common-neighbors/   
[12] J. L. Bentley, Programming pearls. Addison-Wesley, 1986.   
[13] F. Han, L. Zhang, H. Feng, W. Liu, and X. Li, “Scape: Scalable collaborative analytics system on private database with malicious security,” in ICDE. IEEE, 2022, pp. 1740–1753.   
[14] R. Canetti, “Security and composition of multiparty cryptographic protocols,” J. Cryptol., vol. 13, no. 1, pp. 143–202, 2000.   
[15] D. Liben-Nowell and J. M. Kleinberg, “The link prediction problem for social networks,” in CIKM. ACM, 2003, pp. 556–559.   
[16] N. Shibata, Y. Kajikawa, and I. Sakata, “Link prediction in citation networks,” J. Assoc. Inf. Sci. Technol., vol. 63, no. 1, pp. 78–85, 2012.   
[17] S. Fortunato, “Community detection in graphs,” CoRR, vol. abs/0906.0612, 2009.   
[18] J. Leskovec and A. Krevl, “SNAP Datasets: Stanford large network dataset collection,” http://snap.stanford.edu/data, Jun. 2014.   
[19] B. Rozemberczki, C. Allen, and R. Sarkar, “Multi-scale attributed node embedding,” J. Complex Networks, vol. 9, no. 2, 2021.   
[20] P. Sen, G. Namata, M. Bilgic, L. Getoor, B. Gallagher, and T. Eliassi-Rad, “Collective classification in network data,” AI Mag., vol. 29, no. 3, pp. 93–106, 2008.   
[21] R. A. Rossi and N. K. Ahmed, “The network data repository with interactive graph analytics and visualization,” in Proceedings of the AAAI(2015). AAAI Press, 2015, pp. 4292–4293.   
[22] J. Baek, W. Jeong, J. Jin, J. Yoon, and S. J. Hwang, “Personalized subgraph federated learning,” in Proceedings of the ICML 2023, ser. Proceedings of Machine Learning Research, vol. 202. PMLR, 2023, pp. 1396–1415.   
[23] Argung, “Graph regularization for document classification using natural graphs,” 2023. [Online]. Available: https://www.tensorflow.org/neural\_structured\_learning/tutorials /graph\_keras\_mlp\_cora   
[24] Huonw, “Stellargraph api: stellargraph.datasets.cora,” 2020.   
[25] X. Li, F. Li, and M. Gao, “FLARE: A fast, secure, and memory-efficient distributed analytics framework (flavor: Systems),” Proc. VLDB Endow., vol. 16, no. 6, pp. 1439–1452, 2023.   
[26] M. Du, P. Jiang, Q. Wang, S. S. M. Chow, and L. Zhao, “Shielding graph for exact analytics with SGX,” IEEE Trans. Dependable Secur. Comput., vol. 20, no. 6, pp. 5102–5112, 2023.   
[27] S. Mazloom and S. D. Gordon, “Secure computation with differentially private access patterns,” in Proceedings of the CCS(2018). ACM, 2018, pp. 490–507.   
[28] X. Lan, H. Jin, H. Guo, and X. Wang, “Efficient and secure quantile aggregation of private data streams,” IEEE Trans. Inf. Forensics Secur., vol. 18, pp. 3058–3073, 2023.   
[29] K. Huang, H. Hu, S. Zhou, J. Guan, Q. Ye, and X. Zhou, “Privacy and efficiency guaranteed social subgraph matching,” VLDB J., vol. 31, no. 3, pp. 581–602, 2022.   
[30] S. Constable, J. V. Bulck, X. Cheng, Y. Xiao, C. Xing, I. Alexandrovich, T. Kim, F. Piessens, M. Vij, and M. Silberstein, “Aex-notify: Thwarting precise single-stepping attacks through interrupt awareness for intel SGX enclaves,” in Proceedings of the USENIX Security (2023), 2023, pp. 4051–4068.