# GraphProxy: Communication-Efficient Federated Graph Learning with Adaptive Proxy

Junyang Wang∗, Lan Zhang∗†, Junhao Wang∗, Mu Yuan∗, Yihang Cheng∗, Qian Xu‡, Bo Yu‡ ∗ School of Computer Science and Technology, University of Science and Technology of China, Hefei, China † Institute of Artificial Intelligence, Hefei Comprehensive National Science Center ‡ Bestpay Co., Ltd, China Telecom, China {iswangjy,junhaow,ym0813,whcyh}@mail.ustc.edu.cn,{zhanglan}@ustc.edu.cn,{xuqian,yubo}@bestpay.com.cn

Abstract—Federated graph learning (FGL) enables multiple participants with distributed but connected graph data to collaboratively train a model in a privacy-preserving way. However, the high communication cost hinder the adoption of FGL in many resource-limited or delay-sensitive applications. In this work, we focus on reducing the communication cost incurred by the transmission of neighborhood information in FGL. We propose to search for local proxies that can play a substitute role as the external neighbors, and develop a novel federated graph learning framework named GraphProxy. GraphProxy utilizes representation similarity and class correlation to select local proxies for external neighbors. And we propose to dynamically adjust the proxy strategy according to the changing representation of nodes during the iterative training process. We also perform a theoretical analysis and show that using a proxy node has a similar influence on training when it is sufficiently similar to the external one. Extensive evaluations show the effectiveness of our design, e.g., GraphProxy can achieve 8× communication efficiency with only 0.14% performance degradation.

Index Terms—federated graph learning, communication efficiency

# I. INTRODUCTION

Graphs provide ubiquitous data structures to represent complex structures and interactions. A wide range of realworld problem domains (social networks, financial networks, biological networks, traffic networks) naturally employ graphs as modeling tools [1]–[5]. Graph neural networks (GNNs) have been increasingly adopted to encode complex features from graph data for downstream tasks [6]–[10].

In numerous real-world scenarios, graph data are stored separately by different parties [11]–[13]. For example, a bank often possesses sensitive information (e.g., age, education, and income) about customers. Financial transactions between customers occurring both within the same bank and across different banks form financial networks [14]. Due to privacy concerns, legal restrictions and potential conflicts of interest, the graph data held by each party cannot be aggregated for training [15], [16]. Federated graph learning (FGL) is a graph learning framework that enables multiple parties to collaboratively train GNNs while ensuring the decentralization and privacy of graph data.

Expensive cross-client communication in FGL. Compared to traditional neural networks like multi-layer perceptrons, the key to the success of graph neural networks lies in their ability to integrate node features with the underlying graph structure. This is achieved by iteratively exchanging neural information between connected nodes along the edges of the input graph [17]–[21]. However, there are edges between nodes from different parties in FGL (e.g., trades between costumers of different banks, and calls between users of different carriers) [16], [22], namely cross-client edges. Previous works [16], [22], [23] use cross-client edges for training by sharing the latest neighborhood information in the GNN’s aggregation phase. This scheme incurs prohibitive communication costs and high delays (about 6 to 8 times larger than the training time [23]). Conversely, ignoring cross-client edges for training will lead to bias in the learned global model and a significant performance degradation (up to 15%) [22], [24]. Efficient sharing of cross-client neighborhood information is hence the key to improving the performance of FGL.

Data-driven analysis. To better understand the motivation and challenge, we compare the accuracy and communication cost in Tab.I for two different FGL schemes on six graph datasets involving 50 participants1. Isolated FGL [12], [25], [26] without neighborhood information sharing in training, and Shared FGL [16], [22], [23] enables neighborhood information sharing through shared node embeddings. Both of them only use federated averaging [27] algorithm to aggregate model parameters. Obviously, neighborhood information sharing can bring significant performance improvement (up to 11.89%), but the additional communication cost is also huge. Communication cost increased by 97× on Amazon-Computers dataset.

Limitation of existing approaches. The early work Fed-Sage+ [12] attempted to enhance each client’s subgraph through graph generation before training. Each client jointly trains the generative model by transmitting model parameters and node embeddings. But the generated nodes tend to conform to local distributions rather than accurately representing external neighbors. FED-PUB [26] measures the similarity of each subgraph and designs a personalized parameter aggregation strategy. But it lacks performance guarantees due to the absence of cross client neighborhood information in each client. FedGraph [22] proposes to utilize cross-client edges by sharing all latest embedding of nodes used in training, but it incurs significant communication cost. The latest work, FedCog [16], designs a FGL scheme by local graph decoupling, but still incurs high communication cost to share all embeddings of external neighbors. There still lacks an efficient FGL solution that considers both communication efficiency and performance.

TABLE I: Isolated FGL v.s. Shared FGL. 

<table><tr><td>Dataset</td><td>Acc/Cost of Isolated</td><td>Acc/Cost of Shared</td><td> $\Delta$  Acc</td><td> $\Delta$  Cost</td></tr><tr><td>citeSeer</td><td>73.74% / 0.57G</td><td>76.12% / 0.88G</td><td>+ 2.38%</td><td>+ 0.54×</td></tr><tr><td>cora</td><td>71.98% / 0.17G</td><td>83.87% / 0.52G</td><td>+ 11.89%</td><td>+ 2.06×</td></tr><tr><td>cora - full</td><td>61.74% / 3.29G</td><td>70.81% / 21.46G</td><td>+ 9.07%</td><td>+ 5.52×</td></tr><tr><td>pubmed</td><td>86.29% / 0.23G</td><td>86.86% / 4.38G</td><td>+ 0.57%</td><td>+ 18.04×</td></tr><tr><td>amazon - ph</td><td>89.48% / 0.65G</td><td>93.71% / 32.70G</td><td>+ 4.23%</td><td>+ 49.31×</td></tr><tr><td>amazon - cs</td><td>82.41% / 1.00G</td><td>90.57% / 98.00G</td><td>+ 8.16%</td><td>+ 97×</td></tr></table>

Core idea. In this work, we focus on improving the communication efficiency of neighborhood information sharing in FGL. Instead of communicating neighborhood information based on all cross-client edges in all training rounds, we propose to dynamically search proxies for each client’s external neighbors in their local subgraph, then use proxies as the substitute for external neighbors in training.

GRAPHPROXY. In this work, we develop an FGL framework GRAPHPROXY to improve communication efficiency while maintaining model performance. In the neighborhood aggregation stage, GRAPHPROXY substitutes the role of some external neighbor nodes with local proxy nodes, thus greatly reducing the cross-client communication cost. Our design consists of two main modules: proxy searching and dynamic update. The proxy searching module quantifies the substitutability between local nodes and external neighbors, through measuring their representation similarity and class correlation. The dynamic update module in each client determines which node embeddings needs to exchange with other clients, by measuring the representation changes of nodes.

We summarize three key contributions as follows:

• To our best knowledge, we are the first to explore the idea to use local nodes to substitute external neighbors in federated graph learning. We also perform a theoretical analysis (Sec.IV-B) to show the plausibility of this idea.

• Based on the node proxy idea, we develop GRAPHPROXY, a novel FGL framework that improves the communication efficiency of the neighborhood information sharing stage. We propose a proxy searching algorithm that jointly considers embedding similarity and class correlation. And we design a dynamic update approach to further improve the adaptability of proxy nodes.

• We extensively evaluate GRAPHPROXY on six real-world public datasets with various client numbers. Experimental results show that GRAPHPROXY can reduce communication costs while maintaining model performance. Compared with strong baselines [16], [26], [27], GRAPHPROXY can achieve 8× communication efficiency while the performance degradation is only 0.14%.

# II. RELATED WORK AND PRELIMINARY

# A. Related Work

1) Federated learning: Federated learning frameworks are categorized into two main types based on the distribution of participant data: horizontal federated learning (HFL) and vertical federated learning (VFL). HFL involves participants with data from the same feature space but different samples, while VFL involves participants with complementary information of the same samples, but with a split feature space.

Under the HFL setting, communication efficiency is an important issue and has received much academic attention [28]–[31]. Some work reduce the communication cost by carefully selecting the subset of parties that need to be updated [32]. And some work propose to reduce communication cost by compressing update model parameters [33]–[35]. For VFL, previous work also studied communication efficiency optimization in the training [36] and inference [37] phases.

2) Federated graph learning: Above mentioned FL approaches focus on Euclidean data (e.g., image, text, and tabular data). For graph data that is non-Euclidean, federated graph learning (FGL) [12], [16], [22], [26] was proposed as an extension of FL.

Since the sample space is split among FGL participants, the local subgraphs on each client typically have cross-client edges with each other. Most of the early FGL work focus on improving the learning performance of GNNs without using cross-client edges. Zhang et al. [12] design a FGL framework FedSage+ to address the lack of local subgraph by jointly train a graph generator in each client. Clients train graph generators by local graph and send generated embedding each other to calculate loss, then simulate cross-client relationship. Peng et al. [25] design FedNI based on FedSage+ for FGL on medical data. Xie et al. [9] propose GCFL to dynamically choose client when training on non-iid graphs. Baek et al. [26] proposed FED-PUB to identify the similarity of each client’s subgraph by evaluating the output of each GNN, then adjust the model parameter aggregate strategy based on the similarity.

However, with the increasing complexity of real-world graph structure, the learning performance is shown to be bottlenecked by the lack of neighborhood information [16], [22], [23]. Therefore, recent work studied training GNNs using both local subgraph and cross-client edges by sharing embeddings. Chen et al. [22] propose to share node embeddings along cross-client edges in GNN’s neighborhood aggregation phase, and designed FedGraph, a node sampling method trained on large graphs. Du et al. [23] design the embedding caching strategy by weighing performance and time. Recently, Lei et al. [16] propose a two-stage strategy FedCog by decoupling subgraphs and sharing node embeddings, to train on graph data with numerous cross-client edges. They continue to optimize the graph structure of each subgraph and propose LNNC. Exploiting cross-client edges improves the learning performance while inevitably introducing communication overhead, so the trade-off between learning performance and communication overhead, as we study in this work, is urgently needed.

# B. Preliminary

In this subsection, we introduce the basic notations and definitions related to GNNs and federated learning, which will be used in our problem formalization and theoretical analysis. Notations are summarized in Tab.II.

1) Graph neural networks (GNNs): An L-layer GNN takes the features of a node and its L-hop neighbors as input and performs operations such as graph convolution [38], [39] or graph attention [40] to generate the embeddings of nodes. Then the learned node embeddings can be used for downstream tasks. We denote the graph dataset by $\mathcal { G } = ( \nu , \mathcal { E } )$ , and $\nu$ is the collection of n node instances $\{ ( x _ { i } , y _ { i } ) \} _ { i \in \mathcal { V } }$ , where $x _ { i }$ and $y _ { i }$ denote node features and labels. Let E denote the collection of edges, which can also be represented by an adjacency matrix $\mathbf { A } \in \{ 0 , 1 \} ^ { n \times n }$ . From an architectural point of view, the operation of each layer of GNN can be divided into two parts [41], namely the forward propagation operation and the neighborhood aggregation operation. The forward propagation operation can be formulated as:

$$
\tilde {\mathbf {h}} _ {o} ^ {(l)} = \psi^ {(l)} \cdot \mathbf {h} _ {o} ^ {(l - 1)}, \tag {1}
$$

where $\psi ^ { ( l ) }$ is the feature transformation mapping of layer l. The input of the initial layer is $\mathbf { h } _ { o } ^ { ( 0 ) } = x _ { o }$ . The neighborhood aggregation operation can be formulated as:

$$
\mathbf {h} _ {o} ^ {(l)} = \sum f _ {G} (o, e) \cdot \tilde {\mathbf {h}} _ {o} ^ {(l)}, \tag {2}
$$

where node e is the neighbor of node o on E (e could equal to o when represents self loop) and $f _ { G } ( o , e )$ is the affinity function.

Without loss of generality, in this work, we consider the node classification task using graph convolutional network (GCN) [38]. In GCN, $\psi ^ { ( l ) }$ is a fully-connected non-linearity layer and the non-linear function in the output layer is typically the Softmax. The affinity function is:

$$
f _ {G} (o, e) = \mathbf {A} _ {o e} / \sqrt {d _ {o} d _ {e}}, \tag {3}
$$

where $d _ { e }$ is the degree of e (including self-loop).

2) Federated averaging: The standard paradigm of federated learning is to learn a globally shared parameter $w _ { g l o b a l } =$ $w _ { 1 } = w _ { 2 } = \cdot \cdot \cdot = w _ { N }$ with N participants. FedAvg [27] is the most widely used method, which periodically aggregates the model parameters of individual clients by

$$
w _ {g l o b a l} = \frac {1}{\sum_ {j \in N} | \mathcal {V} _ {j} |} \sum_ {i \in N} | \mathcal {V} _ {i} | w _ {i}. \tag {4}
$$

# III. PROBLEM FORMALIZATION AND MAIN IDEA

# A. Problem Formalization

Scope. In this work, we consider the case of federated graph learning for node classification tasks with cross-client edges. We aim to reduce the communication cost of crossclient neighborhood information sharing during FGL training while maintaining learning performance.

In FGL, graph data $\mathcal { G } = ( \nu , \mathcal { E } )$ are distributed on N clients. The part owned by client i is $\mathcal { G } _ { i } ~ = ~ ( \mathcal { V } _ { i } , \mathcal { E } _ { i } )$ , where $\mathcal { E } _ { i }$ is composed of intra-edges $\mathcal { E } _ { i } ^ { i n t r a }$ and inter-edges $\mathcal { E } _ { i } ^ { i n t e r }$ (crossclient edges). Define $\textstyle \mathcal { V } = \bigcup _ { i \in N } \mathcal { V } _ { i }$ and $\textstyle { \mathcal { E } } = \bigcup _ { i \in N } { \mathcal { E } } _ { i }$ . The form of the loss function depends on whether cross-client edges are used.

TABLE II: Notation used in GraphProxy. 

<table><tr><td>Notation</td><td>Definition</td></tr><tr><td> $\mathcal{G}_{i}$ </td><td>Graph data in client  $i$ </td></tr><tr><td> $\mathcal{V}_{i}$ </td><td>Local node set in client  $i$ </td></tr><tr><td> $\mathcal{V}_{i}^{e}$ </td><td>External neighbor node set of client  $i$ </td></tr><tr><td> $\mathcal{V}_{i}^{o}$ </td><td>Client  $i$ &#x27;s nodes, which are others&#x27; external neighbors</td></tr><tr><td> $V_{i}^{o}(j)$ </td><td>Client  $i$ &#x27;s nodes, which have edges with client  $j$ </td></tr><tr><td> $\mathcal{E}_{i}$ </td><td>Edge set in client  $i$ </td></tr><tr><td> $\mathcal{E}_{i}^{inter}, \mathcal{E}_{i}^{intra}$ </td><td>Inter-edges and intra-edges in client  $i$ </td></tr><tr><td> $\mathcal{A}_{i}$ </td><td>Adjacency matrix in client  $i$ </td></tr><tr><td> $d_{o}$ </td><td>The degree of node  $o$ </td></tr><tr><td> $G_{test}$ </td><td>The Test dataset</td></tr><tr><td> $\psi^{(l)}$ </td><td>The feature transformation mapping of layer  $l$ </td></tr><tr><td> $f_{G}(o,e)$ </td><td>The affinity function of GNN</td></tr><tr><td> $S(x;\mathcal{V},\mathcal{E})$ </td><td>The neighborhood of  $x$  on graph  $(\mathcal{V},\mathcal{E})$ </td></tr><tr><td> $\tilde{\mathbf{h}}_{o}^{(l)}, \mathbf{h}_{o}^{(l)}$ </td><td>The intermediate and final output of node  $o$  in layer  $l$ </td></tr></table>

(1) Without cross-client edges: For client i, the loss can be defined as:

$$
F _ {i} (w; \mathcal {V} _ {i}, \mathcal {E} _ {i} ^ {\text { intra }}) = \frac {1}{| \mathcal {V} _ {i} |} \sum_ {\forall x \in \mathcal {V} _ {i}} f (w; S (x; \mathcal {V} _ {i}, \mathcal {E} _ {i} ^ {\text { intra }})). \tag {5}
$$

(2) With cross-client edges: Eq.(5) now needs to be formulated as follows:

$$
F _ {i} (w; \mathcal {V} _ {i} + \mathcal {V} _ {i} ^ {e}, \mathcal {E} _ {i}) = \frac {1}{| \mathcal {V} _ {i} |} \sum_ {\forall x \in \mathcal {V} _ {i}} f (w; S (x; \mathcal {V} _ {i} + \mathcal {V} _ {i} ^ {e}, \mathcal {E} _ {i})), \tag {6}
$$

where $\mathcal { V } _ { i } ^ { e }$ is the external neighbor nodes, w is the model weights to be learned, and $S ( x ; \mathcal { V } , \mathcal { E } )$ is the neighborhood of $x$ on $( \nu , \mathcal { E } )$ . Note that $\mathcal { V } _ { i } ^ { e }$ is only used as an auxiliary of aggregation to update the embedding of local nodes.

The goal of FGL is to solve the optimization problem:

$$
\min _ {w} F (w) = \sum_ {i = 1} ^ {N} q _ {i} F _ {i}, \tag {7}
$$

where qi = $\begin{array} { r } { q _ { i } = \frac { | \mathcal { V } _ { i } | } { \bigcup _ { j \in N } | \mathcal { V } _ { j } | } } \\ { . ~ . ~ } \end{array}$ is the aggregation weight of the model on client i.

# B. Main Idea

When training with cross-client edges, client i gets extra $\mathcal { V } _ { i } ^ { e }$ for $\gamma _ { i } \mathrm { ^ { * } s }$ aggregation, which along $\mathcal { E } _ { i } ^ { i n t e r }$ . When training without cross-client edges, client i could only aggregate $\nu _ { i }$ by itself along $\mathcal { E } _ { i } ^ { i n t r a }$ . The extra external neighbors’ information $( \mathcal { V } _ { i } ^ { e } )$ provide complements of neighborhood to client i, so that the samples in $\nu _ { i }$ end up with better embedding representations, which lead to the performance improvements. But there is no free lunch, the pay is high communication cost in real scenario.

Facing this challenge, we attempt to explore whether the gain brought by $\mathcal { V } _ { i } ^ { e }$ could be replaced. Therefore, we did experiments on two datasets with a naive policy that substitutes $\mathcal { V } _ { i } ^ { e }$ by random local nodes and maintains the graph structure. As shown in Fig.1, the random policy (RandomProxy) shows opposite effects on the two datasets. On the small-graph dataset, Cora, whose subgraphs have averaged 90 nodes,

![](images/70235cd66956d16a4985d74fb2177ae3a1c8040b5ee1cf33928fca848f08eced.jpg)



(a) Small-Graph Dataset Cora

![](images/9c5ff74a3268bc223e29bf3a58472a498fc1cc4c616dd74d35a980b08d464028.jpg)



(b) Large-Graph Dataset Pubmed   
Fig. 1: Effects of using local proxy nodes to substitute external neighbors in FGL.

RandomProxy improved 8.69% learning performance than Isolated FGL. Instead, on the large-graph dataset, Pubmed, whose subgraphs have averaged 660 nodes, RandomProxy degrades model performance by 2.99%. Experimental results show that it is promising to use local nodes to substitute external neighbors, but we need to make selections more carefully. We also perform a theoretical analysis (Sec.IV-B) and show that using a proxy node has a similar influence on training when it is sufficiently similar to the external one.

Based on this idea, we develop a framework named GRAPHPROXY that utilizes representation similarity and class correlation to select local proxies for external neighbors. Moreover, we propose to dynamically adjust proxy strategy according to the changing representation of nodes during the iterative training process.

# IV. GRAPHPROXY DESIGN

# A. Framework overview

In this section, we introduce the detailed design and implementation of GRAPHPROXY. We will first describe the framework overview of GRAPHPROXY, then the proxy searching module and dynamic update module.

GRAPHPROXY focuses on the neighborhood aggregation stage of each layer in GNN training. In this stage, GRAPH-PROXY replaces the role of some external neighbor nodes with local proxy nodes, thus greatly reducing the cross-client communication cost. GRAPHPROXY consists of two main modules: (1) proxy searching and (2) dynamic update.

In a training epoch, when backward propagation finishes, the proxy searching module leverages the available information of node embeddings to find local proxy nodes. Intuitively, proxy searching quantifies the substitutability between local nodes and external neighbors, using the representation similarity and class correlation. If a local proxy node is found, the client will use the proxy node for neighborhood aggregation in the next epoch. Otherwise, the client needs cross-client communication to obtain embeddings of external neighbors. After proxy searching, the dynamic update module in each client determines which node embeddings information needs to exchange with other clients, by measuring the representation changes of nodes. See Alg.1 for a more detailed and formal design of our GRAPHPROXY framework.

Algorithm 1: Framework of GraphProxy   
1 Input: N subgraph $\{\mathcal{G}_{i} = (\mathcal{V}_{i}, \mathcal{E}_{i})\}_{i=1}^{N}$ , GNN and local cache $w = \{w_{i}, w_{i}^{c}\}_{i=1}^{N}$ , dynamic strategy $V^{cal}, V^{com}$ , proxy strategy P and D, all threshold used $t = \{t_{i}\}_{i=1}^{N}$ .
2 Output: node processing strategy $\{V_{i}^{com}, V_{i}^{cal}\}_{i=1}^{N}$ , proxy strategy $\{P_{i}, D_{i}\}_{i=1}^{N}$ , all threshold used (t), w.
3 ▷Client:
4 for $l = 0, \ldots, L - 1$ do
5    for $i = 1, \ldots, N$ do
6 $\tilde{\mathbf{H}}_{i}^{(l)} = \psi^{(l)} \cdot \mathbf{H}_{i}^{(l-1)};$ 7    Share $\tilde{\mathbf{H}}_{i}^{(l)}$ based on $E_{i}$ and $V_{i}^{com};$ 8    for $i = 1, \ldots, N$ do
9    Receive needed external neighbors' $\tilde{\mathbf{E}}\tilde{\mathbf{H}}_{i}^{(l)}$ globally;
10    According to $P_{i}$ , Get proxy nodes' $\tilde{\mathbf{P}}\tilde{\mathbf{H}}_{i}^{(l)}$ locally;
11 $\mathbf{H}_{i}^{(l)} = \sum f_{G} \cdot (\tilde{\mathbf{H}}_{i}^{(l)} \cup \tilde{\mathbf{E}}\tilde{\mathbf{H}}_{i}^{(l)} \cup \tilde{\mathbf{P}}\tilde{\mathbf{H}}_{i}^{(l)})$ ;
12 Backward propagation and send updated $w_{i}$ to server;
13 for $i = 1, \ldots, N$ do
14 $P_{i}, D_{i} = Proxy\_Searching(\mathcal{G}_{i}, P_{i}, D_{i}, \tilde{\mathbf{H}}_{i}^{(l)}, \mathcal{V}_{i}^{cal}, t)$ 15    Notify source clients: Proxy was found.
16 Clients collect proxy results $V^{np} = \{V_{i}^{np}\}_{i=1}^{N};$ 17 $V^{cal}, V^{com} = Dynamic\_Update(\mathcal{G}, V^{np}, w, t, P, D);$ 18 ▷Server:
19 Receive $\{w_{i}\}_{i=1}^{N}$ then $w_{global} = \frac{1}{\sum_{m \in N} |V_{m}|} \sum_{i \in N} |\mathcal{V}_{i}| w_{i};$ 20 Send $w_{global}$ to all clients.

# B. Proxy Searching

In this part, we introduce the process of finding proxy nodes on the local subgraph. We propose to search proxy nodes with proximate embedding representations to external neighbor nodes, since these nodes tend to play a similar role in neighborhood aggregation.

In client i, GNN’s $\scriptstyle { l - \mathrm { l a y e r } ^ { 2 } }$ output embedding of a node x not only represents the features of x itself but also represents the result of aggregating l-hop neighbors of x along the graph structure (formally $S ( x ; \mathcal { V } _ { i } + \mathcal { V } _ { i } ^ { e } , \mathcal { E } _ { i } ) )$ . Therefore, it is reasonable to expect nodes with similar features and neighborhood structures to share a similar embedding. We propose a two conditions-based proxy searching algorithm that jointly considers embedding similarity and class correlation.

Factor-1: embedding similarity. The first factor we considered is the similarity of node embeddings. In each client, for each external neighbor v1, we calculate the Euclidean distance between $v _ { 1 } \ ' \mathrm { s }$ embedding and all local nodes. Then we treat the local node $( u _ { 4 }$ in $\mathrm { F i g } . 2 )$ that has the closest embedding as the proxy candidate. Considering the heterogeneity of different clients’ subgraphs, the range of embedding similarities is nonnormalized. Therefore, we design a process to determine an adaptive similarity threshold $( \epsilon _ { i } )$ in each client. Based on a leave-one-out idea, given a randomly sampled local node, we treat it as a simulated external neighbor and find the lowest embedding distance from the remaining local nodes. We perform the above process multiple times and use the average distance as the threshold. Then, if the proxy candidate has a lower embedding distance than the threshold, we consider the first condition to be satisfied.

![](images/c17a57d8defa4639d001fa80c3f17cdac7f398f02e8ff1d96a3e3473ba5660d4.jpg)



Fig. 2: Illustration of Proxy Searching.

Factor-2: class correlation. The consideration of class correlation in our design stems from two lines of empirical evidence. First, previous works on quality assessment of centralized graphs show that the quality of edges is strongly related to the class of endpoint nodes [42]–[44]. Second, edges between nodes of the same class bring more positive effects in GNNs training [19], [45], [46]. These edges improve the distinction between classes by ensuring similar nodes are closer together in the embedding space while dissimilar nodes are farther apart [46]–[48]. Therefore, we add the second condition for a proxy node: the predicted class of the proxy node must be the same as the original external neighbor $v _ { 1 }$ or one of the target local nodes (the local node that connects to v1, see $u _ { 1 } , u _ { 2 }$ in Fig.2). If the second condition holds, we determine this proxy candidate as the proxy node. Otherwise, the proxy node for this external neighbor is not found. See Alg.2 for a more detailed description.

As shown in Fig.2, once we found a proxy node, e.g., $u _ { 4 }$ for $v _ { 1 }$ , we will reconstruct the local subgraph with an abstracted node $p _ { v _ { 1 } }$ using the information copied from node $u _ { 4 }$ . The abstracted node $p _ { v _ { 1 } }$ is used as an auxiliary of aggregation to update the embedding of nodes $u _ { 1 }$ and $u _ { 2 }$ . Note that $p _ { v _ { 1 } }$ will not participate in local loss computation as a training sample.

Theoretical analysis. Furthermore, we theoretically analyze the influence of using proxy nodes to substitute the original external neighbor nodes in training. Without loss of generality, our analysis focus on training a 2-layer GCN model. First, we explore how a node’s final representation changes after using a node to replace its external neighbors (Lemma.1). Next, we specifically analyzed the influence of this change on training (Lemma.2).

Lemma 1. Suppose a node o is on client i, o has a neighbor node e stored on client $j .$ In epoch t, if the client j needs to communicate the latest embedding of e to client i, then i will obtain $\{ \tilde { h } _ { e } ^ { ( 1 ) } , \tilde { h } _ { e } ^ { ( 2 ) } \}$ ), h˜(2)e } for neighborhood aggregation operation.

Given a proxy node Pe for e, suppose the embedding set of $P _ { e }$ is $\{ \tilde { h } _ { e } ^ { ( 1 ) } + \epsilon _ { 1 } , \tilde { h } _ { e } ^ { ( 2 ) } + \bar { \epsilon } _ { 2 } \} . ~ \epsilon _ { j }$ is the distance between the j-layer embeddings of $P _ { e }$ and e. Let $\epsilon = ( \varphi _ { i } ^ { ( 2 ) } \cdot \epsilon _ { 1 } + \epsilon _ { 2 } )$ , $h _ { o } ^ { ( 2 ) }$ is the final embedding of o that using e, ${ h } _ { o ^ { \prime } } ^ { ( 2 ) }$ o ′ is the final

Algorithm 2: Proxy Searching   
1 Input: $\tilde{H}_e = \{\tilde{h}_e | e \in V_i^{cal}\}$ , $\tilde{H}_i$ , $V_i^{cal}$ , $\mathcal{V}_i$ , $\mathcal{E}_i^{inter}$ , proxy dict $P_i$ , proxy distance dict $D_i$ , classification model $M_c$ , threshold $\epsilon_i$ .

2 Output: proxy dict $P_i$ , proxy distance dict $D_i$ .

3 if needed update initialize then

4 $\quad \epsilon_i$ : Local simulation;

5 $\quad P_i, D_i$ : New dict;

6 for $x_e \in V_i^{cal}$ do

7 $\quad LC = \{M_c(\tilde{h}_e)\}$ ;

8 $\quad \textbf{for } x_o \in S(x_e; \mathcal{V}_i, \mathcal{E}_i^{inter})$ do

9 $\quad \bigcup LC = LC \cup \{M_c(\tilde{h}_o)\}$ ;

10 $\quad V_{KNN}, Distance = KNN(\tilde{h}_e, \tilde{H}_i)$ ;

11 Sort $V_{KNN}$ in ascending order by Distance;

12 $\quad \textbf{for } x_o, d_o \in V_{KNN}, Distance$ do

13 $\quad \textbf{if } d_o > \epsilon_i$ then

14 $\quad \bigcup Break$ ;

15 $\quad \textbf{if } M_c(\tilde{h}_o) \in LC$ then

16 $\quad \bigcup P_i(x_e) = x_o, D_i(x_e) = d_o$ ;

17 $\quad \bigcup Break$ ;

embedding of o that using $P _ { e } .$ Then the difference between o’s final layer output embedding obtained by training with $P _ { e }$ and training with e is:

$$
\left| \left| h _ {o ^ {\prime}} ^ {(2)} - h _ {o} ^ {(2)} \right| \right| = \left| \left| A _ {o e} / \sqrt {d _ {o} d _ {e}} \cdot \epsilon \right| \right|. \tag {8}
$$

Proof Sketch. In epoch t, after forward propagation in first layer, for each node q in client i, we get $\tilde { h } _ { q } ^ { ( 1 ) } = \varphi _ { i } ^ { ( 1 ) } \cdot x _ { q } ,$ then after neighborhood aggregation, we get

$$
h _ {o} ^ {(1)} = \varphi_ {i} ^ {(1)} \cdot x _ {o} + \sum_ {j \in S (o)} \varphi_ {i} ^ {(1)} \cdot x _ {j} \cdot f _ {G} (o, j), \tag {9}
$$

where $S ( o )$ is the abbreviation for $S ( o ; \mathcal { V } _ { i } + \mathcal { V } _ { i } ^ { e } , \mathcal { E } _ { i } )$ . After forward propagation in last layer, for each node q we get $\overset { \sim } { h } _ { q } ^ { ( 2 ) } = \varphi _ { i } ^ { ( 2 ) } \cdot h _ { q } ^ { ( 1 ) }$ · h(1q . Then o’s output of last layer is:

$$
\begin{array}{l} h _ {o} ^ {(2)} = \varphi_ {i} ^ {(2)} \cdot \varphi_ {i} ^ {(1)} \cdot x _ {o} + \varphi_ {i} ^ {(2)} \cdot \sum_ {j \in S (o)} \varphi_ {i} ^ {(1)} \cdot x _ {j} \cdot f _ {G} (o, j) \\ + \sum_ {j \in S (o)} \varphi_ {i} ^ {(2)} \cdot h _ {j} ^ {(1)} \cdot f _ {G} (o, j). \tag {10} \\ \end{array}
$$

We substitute Pe for e in $E q . ( l O )$ , and ge t h(2), $h _ { o ^ { \prime } } ^ { ( 2 ) }$ o then we can derive $| | h _ { o ^ { \prime } } ^ { ( 2 ) } - h _ { o } ^ { ( 2 ) } | |$ − .

FGL’s optimization objective is defined in Eq.7. And we found that if the gradient of loss function satisfies Lipschitz Smooth condition, the influence difference of using proxy node is less than α $. L \cdot | | A _ { o e } / \sqrt { d _ { o } d _ { e } } | | \cdot | | \nabla _ { w } l o s s ( w _ { t - 1 } , h _ { z } ) | | \cdot | | \epsilon | |$ .

Lemma 2. We measure the influence of the embedding of node o for each $z \in G _ { t e s t }$ by $C ( h _ { o } , h _ { z } ) = l o s s ( w _ { t - 1 } , h _ { z } ) \mathrm { ~ - ~ }$ $l o s s ( w _ { t } , h _ { z } )$ , where $h _ { z }$ is the embedding of z, loss $\ : ( w , h _ { z } ) \ :$ means the loss of model that with parameters w on $h _ { z } ,$ , and $C ( h _ { o } , h _ { z } )$ means the difference of loss on the sample of test dataset after using node o. If the gradient of loss function $\nabla _ { w } l o s s ( w _ { t } , h _ { z } )$ satisfies Lipschitz Smooth condition, then the influence difference of using proxy node is:

$$
\triangle C \leq \alpha L \cdot | | A _ {o e} / \sqrt {d _ {o} d _ {e}} | | \cdot | | \nabla_ {w} l o s s (w _ {t - 1}, h _ {z}) | | \cdot | | \epsilon | |. \tag {11}
$$

Proof Sketch. In epoch t, with gradient descent on node $^ { O , }$ the model parameters satisfies

$$
w _ {t} = w _ {t - 1} - \alpha \nabla_ {w} l o s s (w _ {t - 1}, h _ {o}), \tag {12}
$$

α is the learning rate of training. Then we can get

$$
l o s s (w _ {t}, h _ {z}) = l o s s (w _ {t - 1} - \alpha \nabla_ {w} l o s s (w _ {t - 1}, h _ {o}), h _ {z}). \tag {13}
$$

According to the Taylor Expansion

$$
l o s s (w _ {t}, h _ {z}) = l o s s (w _ {t - 1}, h _ {z})
$$

$$
- \nabla_ {w} \text { loss } (w _ {t - 1}, h _ {z}) \cdot \alpha \nabla_ {w} \text { loss } (w _ {t - 1}, h _ {o}).
$$

When training on a 2-layer GNN, the influence of node o is

$$
C (h _ {o}, h _ {z}) = \alpha \nabla_ {w} l o s s (w _ {t - 1}, h _ {z}) \cdot \nabla_ {w} l o s s (w _ {t - 1}, h _ {o} ^ {(2)}). (1 5)
$$

The influence difference of node o is $\bigtriangleup C = C ( h _ { o ^ { \prime } } , h _ { z } ) -$ $C ( h _ { o } , h _ { z } )$ , then

$$
\triangle C = \left| \left| \alpha \nabla_ {w} \text { loss } (w _ {t - 1}, h _ {z}) \right| \right|
$$

$$
\cdot \left| \left| \nabla_ {w} \text { loss } (w _ {t - 1}, h _ {o ^ {\prime}} ^ {(2)}) - \nabla_ {w} \text { loss } (w _ {t - 1}, h _ {o} ^ {(2)}) \right| \right|. \tag {16}
$$

$I f \nabla _ { w } l o s s ( w _ { t } , h _ { o } )$ satisfies Lipschitz Smooth condition

$$
\triangle C \leq \alpha L \cdot | | A _ {o e} / \sqrt {d _ {o} d _ {e}} | | \cdot | | \nabla_ {w} \text {loss} (w _ {t - 1}, h _ {z}) | | \cdot | | \epsilon | |. \tag {17}
$$

These theoretical analyses support the rationality of our proxy searching algorithm. And our ablation evaluations (Sec.V-C) also show its effectiveness.

Computation complexity. According to Eq.6, suppose client i has $| \nu _ { i } |$ local nodes and $| \nu _ { i } ^ { e } |$ external neighbor nodes. Then, for client i, the additional computational cost for a round of proxy searching is $\mathcal { O } ( | \mathcal { V } _ { i } ^ { e } | | \mathcal { V } _ { i } | )$ . This searching is essentially a K-nearest neighbors (KNN) process. We employ K-D Tree and reduces the cost to $\mathcal { O } ( | \mathcal { V } _ { i } ^ { e } | \log | \mathcal { V } _ { i } | )$ . Note that, thanks to our dynamic update module, the searching process is only performed in selected epochs.

# C. Dynamic Update

As training progresses, the embedding similarity and class correlation may change, resulting in the dynamics of substitutability. The dynamics here are mainly two cases. First, there may be a suitable proxy for external neighbors that could not find a proxy before. Second, the found proxy nodes may need to be updated. Therefore, we continue exploring a dynamic update strategy.

Utilizing local model changes. Once a proxy node is determined, it needs to be re-selected if the embeddings involved in the proxy searching module undergo significant changes. A naive solution is to compare all current embeddings against previous embeddings. However, if such a comparison operation is required for all training rounds, the additional computation cost is high. For client i, given R rounds of training, the computational cost is $\mathcal { O } ( \vert \mathcal { R } \vert \vert \nu _ { i } \vert )$ . Fortunately, we found that node embeddings from the same client may have homogeneous changes, which makes it promising to reduce the additional computational cost by identifying the trend of overall changes. Recall that for the forward propagation operation we defined in $\operatorname { E q . } ( 1 )$ , in each layer $l ,$ when the input is fixed, the change of $\mathbf { \widehat { \mathfrak { h } } } _ { i } ^ { ( l ) }$ depends only on $\varphi _ { i } ^ { ( l ) }$ . In the neighborhood aggregation operation as we defined in $\operatorname { E q . } ( 2 )$ , if $\mathcal { E } _ { i }$ and $f _ { G }$ are fixed, then nodes’ neighborhood aggregation is unchanged during training. Considering that the output of layer l − 1 is the input of layer l, so the embedding change of layer l is only related to the change of network parameters of this layer and before. So, we propose to use the changes in model parameters to estimate the changes in local nodes, thereby reducing comparison calculations.

Algorithm 3: Dynamic Update   
1 Input: $V^{np}$ , w and cache $w^{c} = \{w^{cal}, w^{com}\}$ , $t^{cal}$ , $t^{com}$ , proxy dict P, proxy distance dict D, $V^{o}$ , $V^{e}$ , maximum proxy distance $\epsilon$ .
2 Output: $V^{cal}$ , $V^{com}$ .
3 if needed initialize then
4 Initialize $t^{cal}$ , $t^{com}$ , $w^{cal}$ , $w^{com}$ 5 for i = 1, ..., N do
6 $V_{i}^{com}$ , $V_{i}^{cal} = \emptyset$ , $\emptyset$ ;
7 Calculate avg distance $\tilde{d}_{i}$ of $D_{i}$ ;
8 Update $t_{i}^{com}$ and $t_{i}^{cal}$ based on Eq.(18);
9 for i = 1, ..., N do
10 $\triangle w_{i} = ||w_{i} - w_{i}^{com}||$ ;
11 if $\triangle w_{i} > t_{i}^{com}$ then
12 $w_{i}^{com} = w_{i}$ ;
13 for j = 1, ..., N and $j \neq i$ do
14 if $\triangle w_{i} > t_{i}^{com}$ then
15 $V_{ij}^{com} = V_{i}^{o}(j)$ ;
16 Notify j: re-search;
17 else
18 $V_{ij}^{com} = V_{i}^{np}(j)$ ;
19 Notify j: $V_{ij}^{com}$ will be communicated;
20 for i = 1, ..., N do
21 Receive that $V_{i}^{R}$ will be received and need re-search;
22 $\triangle w_{i} = ||w_{i} - w_{i}^{cal}||$ ;
23 if $\triangle w_{i} > t_{i}^{cal}$ then
24 $V_{i}^{cal} = V_{i}^{e}$ , $w_{i}^{cal} = w_{i}$ ;
25 else
26 $V_{i}^{cal} = V_{i}^{R}$ ;

The dynamic update module in a client answers two questions: (1) Which embeddings need to transmit to other clients? (2) Which external neighbors need to re-calculate their local proxies? Our proposed Alg.3 maintains two thresholds $t ^ { c o m }$ (for question-1) and $t ^ { c a l }$ (for question-2) in each client.

Communication strategy. For a pair of clients $i , j ,$ , we define client-i’s nodes that have edges with client-j as $V _ { i } ^ { o } ( j )$ . Then after the last round of proxy searching, some nodes of $V _ { i } ^ { o } ( j )$ where the proxies were not found in client-j, and let $\bar { V _ { i } ^ { n p } } ( j )$ denote them. Let $\triangle w$ denote local model changes. In client-i, we check the condition $\triangle w < = t ^ { c o m }$ . If holds, then we only send the embeddings of nodes in $V _ { i } ^ { n p } ( j )$ ; otherwise, we send embeddings of all nodes in $V _ { i } ^ { o } ( j )$ , and notify client-j that it needs to re-calculate the proxies of $V _ { i } ^ { o } ( j )$ .

Calculation strategy. For client i, we define its external neighbors as $V _ { i } ^ { e }$ , and $V _ { i } ^ { R }$ is part of $V _ { i } ^ { e }$ that received recalculate messages from its origin clients. And we check the condition $\triangle w < = t ^ { c a l }$ . If holds, then in the next epoch client i needs to search the local proxies of $V _ { i } ^ { R } ;$ otherwise, client i need to search the local proxies for all $V _ { i } ^ { e }$ .

Threshold initialization and adaptive update. For the first few (e.g., 3-5) epochs of training, we do not perform proxy searching. Then we use the local model changes to initialize thresholds $t ^ { c o m }$ and $t ^ { c a l }$ . During training, we update them adaptively according to:

$$
t _ {i} = t _ {i} \cdot \frac {r _ {i}}{\tilde {d} _ {i} / \epsilon_ {i}}, \tag {18}
$$

where $\tilde { d } _ { i }$ is the local average proxy distance. Both $t ^ { c o m }$ and $t ^ { c a l }$ can be updated according to Eq.(18), but they are different in specific ratio $r _ { i }$ calculation. Let $\mathcal { V } _ { i } ^ { o }$ denote the set of nodes in client-i that are external neighbors of other clients. For $t ^ { c o m }$ , $r _ { i }$ is the ratio of found proxies in $\mathcal { V } _ { i } ^ { o } .$ , and for $t ^ { c a l }$ it is the ratio of found local proxies in $\mathcal { V } _ { i } ^ { e }$ . $t ^ { c o m }$ and $t ^ { c a l }$ are closely related to proxy searching process. Intuitively, when the ratio of found proxies is higher and the distance is lower, the threshold increases, thus the re-calculate frequency becomes lower. Note that the information used for the dynamic update module is all available locally. Our design reduces the computational cost of dynamic update from $\mathcal { O } ( \vert \mathcal { R } \vert \vert \nu _ { i } \vert )$ to O(|R|).

Privacy enhancement. Like the majority of existing FGL work [12], [16], [22], [23], we share local knowledge to achieve better model performance. Since our approach significantly reduces communication between participants, the privacy risks associated with our approach are at par with or even less than those posed by existing studies. Despite this, there remains a potential risk of revealing node neighborhood structure and classification information when sending out local node embeddings. Recent works [16], [22] propose that it is difficult to reverse the high-dimensional node attributes from low-dimensional embeddings. FedCog [16] proposes a privacy-preserving scheme, FedCog with LNNC. For the nodes that need to be shared with others but have no local neighbors, FedCog with LNNC adds the nearest local nodes as neighbors to them, thus achieving perturbation of neighborhood structure. Inspired by FedCog with LNNC, we developed an enhanced version that fortifies privacy protection, named S-GRAPHPROXY, which adjusts graph structure before training. Recall that $\mathcal { V } _ { i } ^ { o }$ is the set of nodes in client i that are external neighbors of other clients. First, we randomly sample a ratio $S$ of nodes from $\mathcal { V } _ { i } ^ { o }$ . For each sampled node, we add a local neighbor from $\mathcal { V } _ { i } ^ { o }$ with the closest distance but different class labels. The effect of adding a neighbor is twofold: First, it achieves perturbation of neighborhood structure; Second, since the added neighbor has a different class, GNN aggregation operation will protect the original classification information. We evaluate the effect of different ratios S and present a detailed discussion in Sec.V-D.

# V. EVALUATIONS

We evaluate GRAPHPROXY on six real-world graph datasets with 10 ∼ 50 clients. Our highlights are as follows:

• GRAPHPROXY achieves up to 8.1× communication efficiency and 0.88% performance improvement compare to recent baselines [16], [26], [27].   
• Albation studies show the superiority of our proposed proxy searching strategy on performance-cost trade-offs.   
• GRAPHPROXY shows robust effectiveness with respect to searching-related node embeddings and GNN depth.

# A. Experimental Configuration

1) Datasets: We use six real-world datasets for evaluating the performance of our work. The detail of the datasets is shown in Tab.III. To simulate the federated graph learning scenario, we randomly divide the node set into {10, 20, 30, 40, 50} parts by randomly generated ratios. Each node set and its associated edges are held by one client. On the subgraph of each client, we randomly selected 2/3 of the data as the train dataset, and the rest is the test dataset.

TABLE III: Datasets. 

<table><tr><td>Name</td><td>#Nodes</td><td>#Edges</td><td>#Features</td><td>#Classes</td></tr><tr><td>Cora</td><td>2,708</td><td>10,556</td><td>1,433</td><td>7</td></tr><tr><td>Citeseer</td><td>3,327</td><td>9,104</td><td>3,703</td><td>6</td></tr><tr><td>Pubmed</td><td>19,717</td><td>88,648</td><td>500</td><td>3</td></tr><tr><td>Amazon-Ph</td><td>7,650</td><td>238,162</td><td>745</td><td>8</td></tr><tr><td>Amazon-CS</td><td>13,752</td><td>491,722</td><td>767</td><td>10</td></tr><tr><td>Cora-full</td><td>19,793</td><td>126,842</td><td>8,710</td><td>70</td></tr></table>

2) Metrics: In node classification tasks, we evaluate our framework from two aspects: model performance and communication cost. For model performance, we focus on the accuracy on the test dataset. For communication cost, we measure it by the total amount of exchanged data between different clients and between clients and servers.   
3) Models and Settings: For all works, we use 2-layer GCNs with size (feature, embedding) and (embedding, class), then a Softmax layer, and we use mean as affinity function of each layer. We set a same federated update frequency. Our learning rate is in [0.01, 0.15] and the number of hidden units is 128. For our proposed privacy-preserving version, S-GRAPHPROXY, we set $S ~ = ~ 5 0 \%$ by default. We perform evaluations on 3 servers with Inter(R) Xeon(R) CPU E5- 2650 with 2.20GHz, each server with 4 Tesla P100 GPU. The CUDA Version is 11.1.   
4) Baselines: In our experiments, we adopt the following baselines for comparison: (1) FedAvg: Each client only uses the local subgraph for training, and shares parameters through fedavg (Isolated FGL). (2) FedAvg with Com: FedAvg with cross-client communication. Clients share neighborhood information along cross-client edges during training (Shared FGL). (3) FED-PUB: A personalized FGL framework [26]. For better classification performance, we do not mask the model parameters. (4) FedCog: A latest FGL framework proposed for scenarios with cross-client edges [16]. (5) FedCog with LNNC: A privacy-preserving version based on FedCog [16].

![](images/18e22f52928d1e160e9eda71b0dc4eaac2ce6ef41b5c2692d4a184f7e7f2b76a.jpg)  
-#-FedAvg --FedAvg\_with\_Com -+-FED-PUB -←- FedCog -← FedCog\_with\_LNNCc丨 GraphProxy ← S-GraphProxy

Fig. 3: Test Accuracy and Communication Cost (GB) on six datasets with five different client numbers.

# B. Overall Performance

We test our method on six real-world datasets. Fig.3 shows the test accuracy and communication cost between GRAPHPROXY and other methods. Compared with FedAvg with Com, GRAPHPROXY achieves average 3.22× communication efficiency on six datasets. Compared with FedCog, GRAPHPROXY achieves average 3.23× communication efficiency on six dataset. The average test accuracy of GRAPHPROXY is 83.72% on six datasets, the average test accuracy of FedAvg with Com is 83.75% and FedCog is 81.96%.

For example, on the Pubmed dataset, the average test accuracy of FedAvg with Com is 86.88% and the average communication cost is 3.23GB. The average test accuracy of FedCog is 85.86% and the average communication cost is 3.24GB. While GRAPHPROXY could achieve 86.74% test accuracy and only pay 0.40GB communication cost. GraphProxy achieves 8× communication efficiency than both of them. Compared with those methods (FedAvg, FED-PUB) without using crossclient edges, GRAPHPROXY still pays for additional communication costs, but the performance improvement is significant. GRAPHPROXY achieves average 6.32% performance improvement than FED-PUB. For S-GRAPHPROXY, experimental results show that the classification performance is slightly lower compared to GRAPHPROXY, the average degradation is 0.93%. Since the privacy of the shared embedding is protected, the degradation is acceptable.

# C. Effect of Proxy Searching strategy

Now we show the results of different searching strategies in the proxy searching process on Cora and Pubmed datasets. We selected four strategies for proxy search: (1) random proxy: We randomly select proxy nodes in local nodes. (2) label proxy: We randomly select proxy nodes in the node set that the class constraint we mentioned is satisfied. (3) nearest proxy: Compared to the external neighbor, we select the nearest local node as proxy. (4) ours: The nearest local node that satisfies the class constraint. For the first two strategies that are independent of embedding distance comparison, we compare their performance with/without dynamic update strategy, respectively.

As shown in Fig.4, both random proxy without dynamic update and label proxy without dynamic update result in a low test accuracy in two datasets. When random proxy and label proxy combine with our dynamic update, the test accuracy is improved while the communication cost is very high. This is because our dynamic update algorithm frequently found poorly matched proxies, thus requiring communication in most training epochs. In such cases, the goal of improving communication efficiency failed. Our searching strategy and the nearest strategy could reduce communication costs while maintaining model performance. Compared with the nearest strategy, our strategy achieves an average 0.21% performance improvement and reduces the communication cost by 2.9%.

TABLE IV: Performance of S-GraphProxy 

<table><tr><td rowspan="2" colspan="2">Method</td><td colspan="6">Cora</td><td colspan="6">Citeseer</td><td colspan="6">Amazon_cs</td></tr><tr><td>10C</td><td>20C</td><td>30C</td><td>40C</td><td>50C</td><td>Avg</td><td>10C</td><td>20C</td><td>30C</td><td>40C</td><td>50C</td><td>Avg</td><td>10C</td><td>20C</td><td>30C</td><td>40C</td><td>50C</td><td>Avg</td></tr><tr><td colspan="2">FedCog</td><td>0.8234</td><td>0.8258</td><td>0.8212</td><td>0.8211</td><td>0.8366</td><td>0.8256</td><td>0.7544</td><td>0.7638</td><td>0.7651</td><td>0.7635</td><td>0.7637</td><td>0.7621</td><td>0.9167</td><td>0.9203</td><td>0.9215</td><td>0.9203</td><td>0.9175</td><td>0.9193</td></tr><tr><td colspan="2">FedCog with LNNC</td><td>0.774</td><td>0.7675</td><td>0.7602</td><td>0.7573</td><td>0.7642</td><td>0.7646</td><td>0.7155</td><td>0.7445</td><td>0.7446</td><td>0.7415</td><td>0.7427</td><td>0.7378</td><td>0.9124</td><td>0.9109</td><td>0.906</td><td>0.906</td><td>0.9052</td><td>0.9081</td></tr><tr><td rowspan="5">S-GraphProxy</td><td> $S = 0$ </td><td>0.8383</td><td>0.8392</td><td>0.8429</td><td>0.8434</td><td>0.8428</td><td>0.8413</td><td>0.7634</td><td>0.7637</td><td>0.7621</td><td>0.7615</td><td>0.7621</td><td>0.7626</td><td>0.9353</td><td>0.9382</td><td>0.9384</td><td>0.9377</td><td>0.9375</td><td>0.9374</td></tr><tr><td> $S = 25$ </td><td>0.8316</td><td>0.8306</td><td>0.8281</td><td>0.8265</td><td>0.822</td><td>0.8278</td><td>0.7649</td><td>0.7637</td><td>0.7605</td><td>0.7566</td><td>0.7567</td><td>0.7605</td><td>0.9323</td><td>0.9358</td><td>0.9387</td><td>0.9366</td><td>0.9353</td><td>0.9357</td></tr><tr><td> $S = 50$ </td><td>0.831</td><td>0.825</td><td>0.8228</td><td>0.8204</td><td>0.818</td><td>0.8234</td><td>0.7662</td><td>0.759</td><td>0.7557</td><td>0.754</td><td>0.7489</td><td>0.7568</td><td>0.933</td><td>0.9353</td><td>0.934</td><td>0.933</td><td>0.9317</td><td>0.9334</td></tr><tr><td> $S = 75$ </td><td>0.8248</td><td>0.8146</td><td>0.8136</td><td>0.8175</td><td>0.8113</td><td>0.8164</td><td>0.7601</td><td>0.7578</td><td>0.7495</td><td>0.7537</td><td>0.7486</td><td>0.7539</td><td>0.93</td><td>0.9326</td><td>0.9351</td><td>0.9328</td><td>0.9309</td><td>0.9323</td></tr><tr><td> $S = 100$ </td><td>0.818</td><td>0.8104</td><td>0.8147</td><td>0.8121</td><td>0.803</td><td>0.8116</td><td>0.7578</td><td>0.7521</td><td>0.7457</td><td>0.7482</td><td>0.7445</td><td>0.7497</td><td>0.9283</td><td>0.9302</td><td>0.9287</td><td>0.9296</td><td>0.9292</td><td>0.9293</td></tr></table>

![](images/f5319fcefeaeed92f5aed072a845129dfa0390d1ac1bc2b8407640c6d29a0ecc.jpg)



(a) Acc—Cora

![](images/15047a757e08a6bb58a113ba40ef46ce1f32b5c8c7c704f02d97f02156364c8a.jpg)



(b) Cost—Cora

![](images/54b5e546fece88290eba956c14239a738defe444793c2df0e335da662003193f.jpg)



(c) Acc—Pubmed

![](images/bcb594a5e5308ccf2f9c4927addb945357509013a966e92b5f97d9c2b4823d7d.jpg)



(d) Cost—Pubmed

Fig. 4: Test Accuracy and Communication Cost (GB) of different seraching strategy.   
![](images/42b8737a231e0d825f38019aa19926e93a93a0f57f3044b7cd3ca145e1cadf8a.jpg)



(a) Test Accuracy.

![](images/08f98bfca16a618d596b9901052d9c7fd44da0feb6f42d76ff044e53e5a2ff2c.jpg)



(b) Communication Cost and Time.

![](images/2e693aa63d87ae2873ac353c7e972ad26a9be1e7791f54dfa4cea6604c189779.jpg)



(a) Test Accuracy.

![](images/e09d92397f486f69ac3c308991f92885e21acb535d2bfe271054e38dc3779a10.jpg)



(b) Average Searching Time (ms).   
Fig. 5: Efficiency under different layer’s models.   
Fig. 6: Efficiency comparison of different embedding choice.

# D. Effect of Privacy Enhancement

We adjust different protection ratios S on GRAPHPROXY, and report the performance of S-GRAPHPROXY on three datasets in Tab.IV. When we protect more nodes, the classification performance is slightly degraded. Compared to GRAPH-PROXY, when we protect all nodes which need to be shared, the average degradation is 1.69%, which is a reasonable tradeoff for scenarios where privacy is of utmost importance.

# E. Effect of GNN Depth

We explore the effect of GNN depth on test accuracy and costs on Pubmed dataset. As Fig.5 shows that the learning performance is robust while the communication cost and time increase with an increasing network depth. When using 1- layer GNN, the learned neighborhood information is less, and the over-smoothing problem [21], [45] occurs at 3-layer and above, resulting in slight degradation of accuracy.

# F. Effect of Embedding Selection

We select different layers of embeddings for proxy node search on Cora dataset and report the average time (ms) to search all proxy nodes once. The embeddings we choose to include the following: (1) GP-1: After the first layer’s forward propagation. (2) GP-2: After the first layer’s neighborhood aggregation. (3) GP-3: After the second layer’s forward propagation. (4) GP: After the second layer’s neighborhood aggregation. (5) GP-4: Concatenate GP-2 and GP. As shown in Fig.6, several choices are close in performance, the average difference between best and worst is 0.15%. Considering search time and performance jointly, the last layer’s final output embedding is a suitable choice.

# VI. CONCLUSION

In this paper, we study the communication efficiency of neighborhood information sharing in FGL. We propose to use local nodes as proxies to substitute external neighbors in neighborhood aggregation. And we present GraphProxy, a novel FGL framework that jointly considers embedding similarity and class correlation to find proxies and dynamically update proxies. Extensive evaluation on six real-world datasets shows that GraphProxy can significantly reduce communication cost while maintain model performance.

# VII. ACKNOWLEDGMENT

We thank the anonymous INFOCOM reviewers for their constructive comments. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No.61932016, No.62132018, “the Fundamental Research Funds for the Central Universities” WK2150110024, the University Synergy Innovation Program of Anhui Province under Grant GXXT-2022-049.

# REFERENCES

[1] V. Doshi, S. Mallick, and D. Y. Eun, “Competing epidemics on graphs - global convergence and coexistence,” in IEEE INFOCOM 2021.   
[2] W. Lin, Z. Gao, and B. Li, “Guardian: Evaluating trust in online social networks with graph convolutional networks,” in IEEE INFOCOM 2020.   
[3] M. Wang, L. Hui, Y. Cui, R. Liang, and Z. Liu, “xnet: Improving expressiveness and granularity for network modeling with graph neural networks,” in IEEE INFOCOM 2022.   
[4] Z. Xue, J. Du, X. Xu, X. Liu, J. Wang, and F. Kou, “Few-shot node classification via local adaptive discriminant structure learning,” Frontiers of Computer Science, 2023.   
[5] Z. Qian, C. Min, L. Lai, Y. Fang, G. Li, Y. Yao, B. Lyu, X. Zhou, Z. Chen, and J. Zhou, “GAIA: A system for interactive analysis on distributed graphs using a High-Level language,” in USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2021.   
[6] H. Lesfari and F. Giroire, “Nadege: When graph kernels meet network anomaly detection,” in IEEE INFOCOM 2022.   
[7] H. Liu, Y. Wang, Y. Ren, and Y. Chen, “Bipartite graph matching based secret key generation,” in IEEE INFOCOM 2021.   
[8] Z. Zhang, Z. Luo, and C. Wu, “Two-level graph caching for expediting distributed gnn training,” in IEEE INFOCOM 2023.   
[9] H. Xie, J. Ma, L. Xiong, and C. Yang, “Federated graph classification over non-iid graphs,” in NeurIPS, 2021.   
[10] T. Wang, L. Shen, Q. Fan, T. Xu, T. Liu, and H. Xiong, “Joint admission control and resource allocation of virtual network embedding via hierarchical deep reinforcement learning,” IEEE Transactions on Services Computing, 2023.   
[11] R. Liu, P. Xing, Z. Deng, A. Li, C. Guan, and H. Yu, “Federated graph neural networks: Overview, techniques and challenges,” arXiv preprint arXiv:2202.07256, 2022.   
[12] K. ZHANG, C. Yang, X. Li, L. Sun, and S. M. Yiu, “Subgraph federated learning with missing neighbor generation,” in NeurIPS, 2021.   
[13] H. Zhang, T. Shen, F. Wu, M. Yin, H. Yang, and C. Wu, “Federated graph learning–a position paper,” arXiv preprint arXiv:2105.11099, 2021.   
[14] X. Fu, B. Zhang, Y. Dong, C. Chen, and J. Li, “Federated graph machine learning: A survey of concepts, techniques, and applications,” ACM SIGKDD Explorations Newsletter, 2022.   
[15] J. Zhang, X. Cheng, W. Wang, L. Yang, J. Hu, and K. Chen, “FLASH: Towards a high-performance hardware acceleration architecture for cross-silo federated learning,” in USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2023.   
[16] R. Lei, P. Wang, J. Zhao, L. Lan, J. Tao, C. Deng, J. Feng, X. Wang, and X. Guan, “Federated learning over coupled graphs,” IEEE Transactions on Parallel and Distributed Systems (TPDS), 2023.   
[17] S. Liu, R. Ying, H. Dong, L. Li, T. Xu, Y. Rong, P. Zhao, J. Huang, and D. Wu, “Local augmentation for graph neural networks,” in International Conference on Machine Learning (ICML), 2022.   
[18] Z. Ying, D. Bourgeois, J. You, M. Zitnik, and J. Leskovec, “Gnnexplainer: Generating explanations for graph neural networks,” in Advances in neural information processing systems (NeurIPS), 2019.   
[19] D. Luo, W. Cheng, W. Yu, B. Zong, J. Ni, H. Chen, and X. Zhang, “Learning to drop: Robust graph neural network via topological denoising,” in Proceedings of the 14th ACM international conference on web search and data mining (WSDM), 2021.   
[20] D. Luo, W. Cheng, D. Xu, W. Yu, B. Zong, H. Chen, and X. Zhang, “Parameterized explainer for graph neural network,” in Advances in neural information processing systems (NeurIPS), 2020.   
[21] Y. Rong, W. Huang, T. Xu, and J. Huang, “Dropedge: Towards deep graph convolutional networks on node classification,” in International Conference on Learning Representations (ICLR), 2020.   
[22] F. Chen, P. Li, T. Miyazaki, and C. Wu, “Fedgraph: Federated graph learning with intelligent sampling,” IEEE Transactions on Parallel and Distributed Systems (TPDS), 2022.   
[23] B. Du and C. Wu, “Federated graph learning with periodic neighbour sampling,” in IEEE/ACM 30th International Symposium on Quality of Service (IWQoS), 2022.   
[24] M. Ramezani, W. Cong, M. Mahdavi, M. Kandemir, and A. Sivasubramaniam, “Learn locally, correct globally: A distributed algorithm for training graph neural networks,” in International Conference on Learning Representations (ICLR), 2022.   
[25] L. Peng, N. Wang, N. Dvornek, X. Zhu, and X. Li, “Fedni: Federated graph learning with network inpainting for population-based disease prediction,” IEEE Transactions on Medical Imaging, 2023.

[26] J. Baek, W. Jeong, J. Jin, J. Yoon, and S. J. Hwang, “Personalized subgraph federated learning,” in International Conference on Machine Learning (ICML), 2023.   
[27] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial intelligence and statistics (AISTATS), 2017.   
[28] Z. Wang, M. Song, Z. Zhang, Y. Song, Q. Wang, and H. Qi, “Beyond inferring class representatives: User-level privacy leakage from federated learning,” in IEEE INFOCOM 2019.   
[29] M. Tang and V. W. Wong, “An incentive mechanism for cross-silo federated learning: A public goods perspective,” in IEEE INFOCOM 2021.   
[30] B. Luo, X. Li, S. Wang, J. Huang, and L. Tassiulas, “Cost-effective federated learning design,” in IEEE INFOCOM 2021.   
[31] Z. Zhong, Y. Zhou, D. Wu, X. Chen, M. Chen, C. Li, and Q. Z. Sheng, “P-fedavg: Parallelizing federated learning with theoretical guarantees,” in IEEE INFOCOM 2021.   
[32] J. Perazzone, S. Wang, M. Ji, and K. S. Chan, “Communication-efficient device scheduling for federated learning using stochastic optimization,” in IEEE INFOCOM 2022.   
[33] P. Li, G. Cheng, X. Huang, J. Kang, R. Yu, Y. Wu, and M. Pan, “Anycostfl: Efficient on-demand federated learning over heterogeneous edge devices,” in IEEE INFOCOM 2023.   
[34] L. Cui, X. Su, Y. Zhou, and J. Liu, “Optimal rate adaption in federated learning with compressed communications,” in IEEE INFOCOM 2022.   
[35] L. Li, D. Shi, R. Hou, H. Li, M. Pan, and Z. Han, “To talk or to work: Flexible communication compression for energy efficient federated learning over heterogeneous mobile edge devices,” in IEEE INFOCOM 2021.   
[36] T. Castiglia, A. Das, S. Wang, and S. Patterson, “Compressed-vfl: Communication-efficient learning with vertically partitioned data,” in Proceedings of the 39th International Conference on Machine Learning (ICML), 2022.   
[37] J. Wang, L. Zhang, Y. Cheng, S. Li, H. Zhang, D. Huang, and X. Lan, “Tvfl: Tunable vertical federated learning towards communicationefficient model serving,” in IEEE INFOCOM 2023.   
[38] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” in International Conference on Learning Representations (ICLR), 2017.   
[39] W. Hamilton, Z. Ying, and J. Leskovec, “Inductive representation learning on large graphs,” in Advances in neural information processing systems (NeurIPS), 2017.   
[40] P. Velickovi ˇ c, G. Cucurull, A. Casanova, A. Romero, P. Li ´ o, and \` Y. Bengio, “Graph attention networks,” in International Conference on Learning Representations (ICLR), 2018.   
[41] C. Yang, Q. Wu, J. Wang, and J. Yan, “Graph neural networks are inherently good generalizers: Insights by bridging GNNs and MLPs,” in The Eleventh International Conference on Learning Representations (ICLR), 2023.   
[42] S. Suresh, V. Budde, J. Neville, P. Li, and J. Ma, “Breaking the limit of graph neural networks by improving the assortativity of graphs with local mixing patterns,” in Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining (SIGKDD), 2021.   
[43] Z. Gao, S. Bhattacharya, L. Zhang, R. S. Blum, A. Ribeiro, and B. M. Sadler, “Training robust graph neural networks with topology adaptive edge dropping,” arXiv preprint arXiv:2106.02892, 2021.   
[44] M. Adjeisah, X. Zhu, H. Xu, and T. A. Ayall, “Towards data augmentation in graph neural network: An overview and evaluation,” Computer Science Review, 2023.   
[45] D. Chen, Y. Lin, W. Li, P. Li, J. Zhou, and X. Sun, “Measuring and relieving the over-smoothing problem for graph neural networks from the topological view,” in AAAI, 2020.   
[46] T. Zhao, Y. Liu, L. Neves, O. Woodford, M. Jiang, and N. Shah, “Data augmentation for graph neural networks,” in AAAI, 2021.   
[47] M. Yuan, L. Zhang, X.-Y. Li, and H. Xiong, “Comprehensive and efficient data labeling via adaptive model scheduling,” in IEEE International Conference on Data Engineering (ICDE), 2020.   
[48] M.-H. Song, L. Zhang, M. Yuan, Z. Li, Q. Song, Y. Liu, and G. Zheng, “Cotel: Ontology-neural co-enhanced text labeling,” in Proceedings of the ACM Web Conference (WWW), 2023.