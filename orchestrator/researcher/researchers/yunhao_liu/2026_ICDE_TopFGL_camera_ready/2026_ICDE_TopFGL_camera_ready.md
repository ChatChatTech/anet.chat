# TopFGL: A Topology-Aware and Distribution-Agnostic Federated Learning Framework Tackling Topological Heterogeneity on Graph Data

Junyang Wang∗, Lan Zhang∗, Yihang Cheng∗, Mu Yuan†, Tianfu Wang∗, Zhihui Fu‡, Jun Wang§

∗ University of Science and Technology of China, Hefei, China

† The Chinese University of Hong Kong, Hong Kong SAR, China

‡ Shanghai Jiao Tong University, Shanghai, China

§ University of Luxembourg, Luxembourg

{iswangjy, yihangcheng, ym0813, tianfuwang}@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, {hzzhzzf, junwang.lu}@gmail.com

Abstract—While the modern internet generates graph data at an unprecedented scale, stringent privacy regulations like GDPR have fragmented it into silos, creating an urgent need for distributed learning paradigms. Federated Graph Learning (FGL) meets this demand, enabling collaborative training across graph silos. A core challenge for FGL is that the graphs among participants are topologically heterogeneous due to diverse sources and methods of structure collection, which leads to significant performance degradation. However, recent works tackling heterogeneity require clients to share class-wise intermediate information derived from local embeddings, which could increase risks of label and structure leakage. Moreover, they are often computationally expensive and narrowly tailored for a single type of heterogeneity, which hinders their applicability in efficiency-demanding and distribution-variant practical scenarios. To this end, we present TopFGL, the first topologyaware and distribution-agnostic framework to tackle heterogeneity without intermediate information sharing. TopFGL trains a topology learner in each client to learn local topological patterns, and globally aggregates all learners along with the main task models. We propose a multi-level topology extraction scheme to adapt to diverse distributions, along with a streamlined training pipeline that reduces redundant computations. Building upon the learners, we propose a server-side topological similarity-based aggregation algorithm to share similar optimization directions across clients. A client-side dual-model guided topology augmentation approach is also proposed to supplement neighborhood connections for topology-insufficient nodes, improving adaptability to imbalanced distributions. Experiments on 11 datasets with 3 topological distributions across 3 ∼ 100 client counts show that TopFGL achieves up to 5.6% accuracy improvement along with 50% time cost reduction compared to state-of-the-art baselines.

Index Terms—Distributed Graph Data Management, Topological Heterogeneity, Federated Graph Learning.

# I. INTRODUCTION

Graph-structured data, characterized by nodes and edges, effectively represents the complex relationships and interactions inherent in various domains [1–4]. In multiple real-world scenarios, graph data is collected by different companies or institutions [5–8]. However, the enactment of data privacy regulations like GDPR [9] and CCPA [10] prevents these entities from directly sharing their graphs, leading to the formation of numerous graph data silos. To jointly manage and leverage these siloed datasets, database researchers are motivated to develop privacy-preserving learning methods for distributed graphs. Recently, Federated Graph Learning (FGL) has emerged as a promising paradigm, enabling clients to train Graph Neural Networks (GNNs) on their local graphs while a server aggregates model updates from clients to build a unified model. Thus, FGL allows leveraging insights from multiple data silos while preserving the locality of the raw graph data.

Topological heterogeneity hinders FGL. Traditional federated learning approaches perform acceptably when the data are independent and identically distributed [11]. Unfortunately, in FGL, the graphs among clients are usually topologically heterogeneous due to diversified sources and methods of structure collection [12, 13]. Topological heterogeneity is reflected in the differences of community distributions [14, 15] and link patterns [16, 17] across distributed graphs. This causes clients to train local GNNs along divergent directions, leading to the collapse of model aggregation and resulting in a suboptimal global model. Furthermore, topological heterogeneity and the problem of missing links [14, 18] in FGL undermine the connectivity of local graphs. Clients with sparse graphs or imbalanced topological distributions often lack sufficient homogeneous edges to connect similar nodes together. The insufficient neighborhood information hinders message-passingbased GNNs from learning expressive embeddings, ultimately leading to unclear decision boundaries and undesirable classification performance. Therefore, a critical question for FGL is: How to resolve incompatible aggregation globally and enhance insufficient neighborhood information locally?

Limitations of existing works. Existing FGL approaches fall into two categories: federated model guidance and classwise knowledge-sharing. (1) Federated model guidance approaches [13–16] extract topological guidance from the basic federated GNN models for tackling heterogeneity. Since message-passing-based GNNs only encode topology as implicit signals, directly extracting topological guidance from the topology-unaware models cannot guarantee accuracy. (2) Class-wise knowledge-sharing approaches [18–21] extract class-wise intermediate information derived from local embeddings, and share it for data alignment or knowledge distillation.

TABLE I: Comparison of TopFGL and latest FGL frameworks. 

<table><tr><td>Frameworks</td><td>Graph Topology-Aware</td><td>Model Sharing Only</td><td>Adaptive to Diverse Distributions</td></tr><tr><td>Federated Model Guidance [13–16]</td><td>✗</td><td>√</td><td>✗</td></tr><tr><td>Class-wise Knowledge-Sharing [18–21]</td><td>√</td><td>✗</td><td>✗</td></tr><tr><td>TopFGL (ours)</td><td>√</td><td>√</td><td>√</td></tr></table>

However, recent studies have revealed that sharing embeddings can lead to label leakage [22] and structure leakage [23]. Consequently, addressing heterogeneity while preserving privacy is challenging. The database community urgently needs a framework that collaboratively learns topological guidance to tackle heterogeneity while avoiding the sharing of sensitive intermediate information.

Furthermore, existing FGL frameworks incur significant computational costs and exhibit limited adaptability across diverse topological distributions. In Fig. 1(a), we evaluate the computational efficiency of the latest FGL frameworks and find that most of them fail to balance model performance and computational costs. Additionally, they are often specialized to tackle a single type of heterogeneity. As revealed by the observations in Fig. 1(b), these approaches struggle to maintain effectiveness under varying topological distributions. Therefore, a computationally efficient FGL framework that is adaptive to diverse topological distributions is still lacking.

To address these challenges, we introduce TopFGL, a topology-aware and distribution-agnostic framework to tackle heterogeneity without intermediate information sharing. TopFGL trains a topology learner in each client to learn local topological patterns, and globally aggregates all learners along with the main task GNNs. Firstly, we construct a multi-level representation of local topologies for the topology learners by explicitly encoding both node-level properties and subgraphlevel embeddings. This rich representation enhances the adaptability to diverse distributions. Secondly, we identify that the topology learner and the main task GNN repetitively learn node semantic features, which incurs a significant computational redundancy. Motivated by this, we design a streamlined training pipeline that reuses low-dimensional representations from the main task GNN, thereby reducing the dimensionality of the learner and boosting overall computational efficiency.

Building upon the topology learners, we design two modules leveraging the learned topological knowledge to systematically address the heterogeneity issue. (1) To reconcile incompatible global aggregation, we reconstruct and align centered kernels [16, 24] from the learners on the server to evaluate local graph similarity. Based on this similarity, we perform compatible model aggregation to promote aligned optimization directions across clients with similar topological characteristics. (2) To supplement insufficient local neighborhood connections, we detect topology-deficient nodes in local structures, and construct k-nearest-neighbors graphs in the embedding space of topology learners to extract topological guidance for targeted local graph augmentation. This enables message-passing-based GNNs to gather richer neighborhood information, improving TopFGL’s adaptability on graphs with imbalanced topological distributions. Moreover, TopFGL is designed as an extensible framework, allowing for the integration of new algorithms in the future to leverage the topological guidance of the learners.

![](images/291c20acc174d0cf8b17892542c539cd86301377511f71d8b57d510966a94639.jpg)



50 150 250(a) Effectiveness vs. Efficiency

![](images/ce250c1f1e6de5436741b62ae5af5ab7c76bd0bac792809071e0bf8b53b7f32b.jpg)



(b) Adaptability   
Fig. 1: Performance on Coauthor-CS dataset with 20 clients. (a) Efficiency analysis of FGL frameworks. (b) Performance on graphs with two additional topological distributions. Detailed information about distributions is shown in Sec. IV-A.

Contributions. The contributions of this paper are four-fold:

• To our best knowledge, TopFGL is the first topology-aware and distribution-agnostic framework to tackle topological heterogeneity without intermediate information sharing.   
• We propose a multi-level explicit encoding scheme of local topologies, which empowers the learners to adapt to diverse distributions. We also propose a streamlined training pipeline that reuses semantic information learned by the main task GNNs to improve computational efficiency.   
• We develop a server-side topological similarity-based aggregation algorithm to share similar optimization directions across clients. We also design a client-side augmentation approach to supplement insufficient neighborhood connections, improving adaptability to imbalanced distributions.   
• Extensive experiments on 11 graph datasets under 3 topological distributions and up to 100 clients demonstrate the superiority of TopFGL. Compared to state-of-theart baselines, TopFGL achieves up to a 5.6% accuracy improvement while simultaneously reducing training time by 50%. Furthermore, TopFGL shows strong adaptability, achieving consistent performance gains on two particularly challenging distributions of up to 6.9% and 4.3%, respectively. Finally, ablation studies confirm the significant contributions of our server and client modules, which are responsible for up to 6.7% and 5.3% of the accuracy boost.

# II. PRELIMINARIES AND FORMALIZATION

Graph Neural Networks. A graph is denoted as $\mathcal { G } ^ { \mathrm { ~ ~ } } =$ $( \nu , \mathcal { E } , \mathcal { X } )$ , where V is the set of n nodes, E is the set of edges, which can also be represented by an adjacency matrix $\mathcal { A } \stackrel { \cdot } { \in } \{ 0 , 1 \} ^ { n \times n } . \ \mathcal { X } \in \mathbb { R } ^ { n \times f }$ is the node feature matrix, with each row representing a node’s f-dimensional feature. A GNN processes a node and its neighborhood as follows:

$$
h _ {i} ^ {l + 1} = \mathbf {U P D} (h _ {i} ^ {l}, \mathbf {A G G} (h _ {j} ^ {l} | j \in \Gamma_ {i})), \forall i \in \mathcal {V}, \tag {1}
$$

where l is the layer index, $h _ { i } ^ { l }$ is the node representation $( h _ { i } ^ { 0 }$ is the initial feature). UPD and AGG denote the update and the aggregation function. Γi is the neighborhood of node i.

Class-wise Edge Distribution. For each client $c \in { \mathcal { C } } .$ , we denote its edge distribution as $\mathcal { P } _ { c } \in \mathbb { R } ^ { Y \times Y }$ , where Y is the node class counts. $\mathcal { P } _ { c } ( i , j )$ represents the probability of an edge between nodes of class i and j. It is computed as:

$$
\mathcal {P} _ {c} (i, j) = \frac {\left| \left\{\left(u , v\right) \in \mathcal {E} _ {c} \mid y _ {u} = i , y _ {v} = j \right\} \right|}{\left| \mathcal {E} _ {c} \right|}, \tag {2}
$$

where $y _ { u }$ is the class label of node u. $\mathcal { P } _ { c }$ measures the classwise link patterns within the local graph $\mathcal { G } _ { c }$ of client c.

Topological Heterogeneity. We define topological heterogeneity as the discrepancy in edge distributions $\{ \mathcal { P } _ { c } \} _ { c \in \mathcal { C } }$ across clients. We first leverage the Jensen-Shannon Divergence (JSD) [25] to measure the pairwise heterogeneity between any two clients, and then the overall system heterogeneity can be defined as the average of all pairwise JSD values:

$$
\mathcal {H} _ {\text { pairwise }} = \frac {1}{\binom {| \mathcal {C} |} {2}} \sum_ {c, c ^ {\prime} \in \mathcal {C}, c <   c ^ {\prime}} \mathrm{JSD} (\mathbf {P} _ {c} \| \mathbf {P} _ {c ^ {\prime}}), \tag {3}
$$

where $\mathrm { J S D } ( \mathbf { P } _ { c } \| \mathbf { P } _ { c ^ { \prime } } ) = \textstyle { \frac { 1 } { 2 } } D _ { \mathrm { K L } } ( \mathbf { P } _ { c } \| \mathbf { M } ) + \textstyle { \frac { 1 } { 2 } } D _ { \mathrm { K L } } ( \mathbf { P } _ { c ^ { \prime } } \| \mathbf { M } )$ , with $\begin{array} { r } { \mathbf { M } = \frac { 1 } { 2 } ( \mathbf { P } _ { c } + \mathbf { P } _ { c ^ { \prime } } ) , D _ { \mathrm { K I } } } \end{array}$ is the Kullback-Leibler divergence.

Federated Learning (FL). FL coordinates training across clients in the set C. In each communication round, each client c uploads their local model $w _ { c }$ to the server. The server aggregates all models and distributes the global model $w _ { g l o b a l }$ to the clients. FedAvg [26] aggregates all models by:

$$
w _ {g l o b a l} = \frac {\sum_ {c \in \mathcal {C}} | \mathcal {V} _ {c} | w _ {c}}{\sum_ {c ^ {\prime} \in \mathcal {C}} | \mathcal {V} _ {c ^ {\prime}} |} \tag {4}
$$

# III. METHODOLOGY

In this section, we introduce TopFGL for heterogeneity federated graph learning. Our core idea is to employ topology learners on each client, designing them to adaptively learn topological patterns. This learned knowledge is then leveraged to systematically address topological heterogeneity through two key components: a server-side compatible aggregation module and a client-side topology augmentation module.

We structure the presentation as follows. First, we introduce the design of the topology learner. Sec. III-A details the adaptive topology extraction scheme to generate its input representations, and Sec. III-B presents its architecture and efficient training pipeline. Building upon the topology learner, Sec. III-C and Sec. III-D present the server-side aggregation module and client-side augmentation modules to address heterogeneity. Finally, we analyze the efficiency of TopFGL with respect to computation and communication in Sec. III-E. We connect the aforementioned modules via a data flow and present an overview of the TopFGL framework in Fig. 2.

# A. Adaptive Multi-level Topology Extraction

The critical role of topological information for GNN training is widely acknowledged within the database community [27–29]. Nevertheless, conventional GNNs embed topology implicitly via message-passing [30, 31], which hinders the extraction of the explicit topological guidance needed to mitigate heterogeneity challenges prevalent in FGL. To address this, we propose a topology learner tailored for FGL, tasked with learning explicit representations of topological structures. This learner operates on encoded topological information of nodes as its primary input, while also incorporating dimensionreduced features from the main task GNN as auxiliary information to enhance training. To effectively learn topological patterns and enhance adaptability to imbalanced distributions, we encode topology at two distinct levels: node-centric and subgraph-centric. These representations are then combined to form a comprehensive topological embedding for each node.

![](images/66a29dfb6e6e9add6e6eef58e6a09f402420a6c9bc0ddfa28baf939959b6a54f.jpg)



Fig. 2: Overview of our proposed TopFGL framework.

Node-level: Random Walk Embedding. To capture local topology from a node-centric perspective, we employ random walk-based embeddings to encode local neighborhood structures. However, generating such embeddings using traditional, exhaustive random walk approaches can be computationally intensive on large graphs. Addressing the need for efficiency, we specifically utilize Node2Vec [32] to compute these node embeddings. Node2Vec employs a sampling-based biased random walk strategy, which efficiently explores diverse neighborhoods within each client’s local graph in the FGL setting. We first train a Word2Vec model independently for each client, using node sequences generated by applying the Node2Vec procedure to their respective local graph data. The resulting Random Walk Embedding (RWE) for a local node i, denoted $h _ { i } ^ { R W E }$ , represents its node-centric local topological structure. Subgraph-level: Homogeneous Embedding. The heterogeneity in community distributions and link patterns across clients manifests locally as varying graph homogeneity levels [33, 34]. This local homogeneity thus serves as a key indicator of subgraph-level topological structure in FGL. To capture this, TopFGL encodes degree and jaccard similarity for nodes into a unified representation reflecting local structural homogeneity.

(1) Degree Similarity Embedding. Degree is a fundamental and computationally efficient topological property of nodes [12, 35]. Since degree measures the connectivity of a node, we leverage the similarity of degrees between nodes to assess local homogeneity. Thus, we define the degree similarity between a node i and its neighbor q as follows:

$$
S (i, q) = \frac {1}{1 + | d _ {i} - d _ {q} |}, \tag {5}
$$

where $d _ { i }$ is the degree of node i. This raw similarity score is then normalized to the range of the local graph, ensuring

![](images/8fad43bc1a99f50a178ff3da54f0bd3a9c3fe8b84777d1dadc73e7d8e336a997.jpg)



Fig. 3: Illustration of multi-level topology extraction process. consistent feature scaling within each client:

$$
S ^ {\prime} (i, q) = \frac {S (i , q) - S _ {m i n}}{S _ {m a x} - S _ {m i n}}, \tag {6}
$$

where $S _ { m a x }$ and $S _ { m i n }$ are the maximum and minimum values of $S ( i , q )$ within the local graph. Finally, we compute the average normalized similarity between node i and all its neighbors to serve as the degree similarity embedding of i:

$$
\mathbf {h} _ {i} ^ {\text { deg }} = \frac {1}{| \Gamma (i) |} \sum_ {q \in \Gamma (i)} S ^ {\prime} (i, q), \tag {7}
$$

where $\Gamma ( i )$ denotes the set of neighbors of node i.

(2) Jaccard Similarity Embedding. Jaccard similarity [36– 39] is widely utilized to measure the similarity between sets. In FGL, we leverage jaccard similarity to assess the neighborhood overlap between a node i and its neighbor q:

$$
J a c (i, q) = \frac {| \Gamma (i) \cap \Gamma (q) |}{| \Gamma (i) \cup \Gamma (q) |}, \tag {8}
$$

where $\Gamma ( i )$ is the neighbor set of node i, and | · | denotes set cardinality. Similarly to the process for degree similarity, we normalize this score based on the local graph’s range:

$$
J a c ^ {\prime} (i, q) = \frac {J a c (i , q) - J _ {m i n}}{J _ {m a x} - J _ {m i n}}, \tag {9}
$$

where $J _ { m a x }$ and $J _ { m i n }$ are the respective maximum and minimum Jaccard similarity values over the client’s local graph. Then, the Jaccard similarity embedding $\mathbf { h } _ { i } ^ { j a c }$ for node i is the average normalized similarity to its neighbors:

$$
\mathbf {h} _ {i} ^ {j a c} = \frac {1}{| \Gamma (i) |} \sum_ {q \in \Gamma (i)} J a c ^ {\prime} (i, q). \tag {10}
$$

We concatenate the degree and Jaccard similarity embeddings to form the node’s homogeneous embedding:

$$
\mathbf {h} _ {i} ^ {H E} = \mathbf {h} _ {i} ^ {d e g} \oplus \mathbf {h} _ {i} ^ {j a c}. \tag {11}
$$

Here, $\oplus$ denotes the concatenation operation. Finally, this homogeneous embedding is combined with the random walk embedding to yield the comprehensive topological embedding:

$$
\mathbf {h} _ {i} ^ {T} = \mathbf {h} _ {i} ^ {R W E} \oplus \mathbf {h} _ {i} ^ {H E}. \tag {12}
$$

This resulting embedding ${ \mathbf { h } } _ { i } ^ { T }$ serves as the input representation for node i when training the topology learner. Fig. 3 illustrates an example of this process, where we encode the graph structure from three distinct perspectives. This representation offers a dual advantage in effectiveness and efficiency:

![](images/2c02c0bc818052d09c32f92cf4cc7cae4ed262c84b615a4991a26a82e617cc2e.jpg)



Fig. 4: Efficient Local Training Pipeline. Green components align with standard GNN training. A gradient-detached copy of Embs. h is used for the topology learner. This design significantly reduces the size of graph conv. layer in learner.

• Effectiveness: The design of multi-level topology extraction is motivated by the need for precise topological guidance for FGL. While latest FGL frameworks [13–16] attempt to extract inter-client topological differences, their reliance on basic GNNs that merely use structure for message passing yields ambiguous topological signals. In contrast, by explicitly capturing multiple facets of local structure, our topological embedding allows the topology learner to directly model local topological distributions. This provides our TopFGL framework with more distinct guidance, laying a robust foundation for its two topology-aware modules.   
• Efficiency: The topological embedding ${ \mathbf { h } } _ { i } ^ { T }$ is derived solely from the static structure and can be pre-computed once with a computational complexity of $\mathcal { O } ( N + E )$ for subsequent reuse across numerous settings. Compared to basic approaches that use general graph structures for learning, the additional onetime cost of our initialization phase is negligible.

# B. Efficient Training of Topology Learners

Model Architecture. To efficiently capture topology, we construct the topology learner leveraging two graph convolutional layers [40], followed by a linear layer. Through the messagepassing inherent in convolutional layers, the learner aggregates topological knowledge derived from the input topological embeddings. This allows the resulting representations to capture shared topological patterns among interconnected nodes.

Semantic-aware Topology Learning. To help the learner better establish the mapping between topological patterns and the downstream task, a widely used approach is to incorporate node semantic information during its training [12, 21, 41]. A straightforward approach to achieve this involves concatenating raw node features with the topological embeddings. However, this often incurs significant computational cost due to the potentially high dimensionality of raw features.

Efficient Local Training Pipeline. To address these concerns, we propose an efficient way: reusing the low-dimensional representations learned by the main task GNN. As shown in Fig. 4, the main GNN follows its standard training procedure.

![](images/d7f4f148675c710355eb1d71c2b0bd030739685df0498027a50141a8122984c1.jpg)



Fig. 5: Overview of the two topology-aware modules in TopFGL framework.

Concurrently, the topology learner processes the topological embeddings through its graph convolutional layers. The resulting intermediate representations are then concatenated with the low-dimensional outputs extracted from the main task GNN. These combined embeddings then serve as the input to the final linear layer of the learner. To collaboratively learn topology, the learners are trained in a federated manner, sharing the same aggregation method as the main task GNNs.

This design ensures both the compatibility and efficiency of our framework. On one hand, by detaching the reused embeddings from the main GNN’s computational graph, we isolate the learner’s gradient flow. Consequently, the main task GNN’s training process aligns with standard GNN training, which ensures broad compatibility with various GNN architectures. On the other hand, reusing these embeddings minimizes the size of the topology learner’s graph convolutional layers. Our experiments in Tab. V demonstrate that the topology learner’s model size is merely 0.6% on average of the main task GNN’s, indicating the additional computational cost is negligible.

# C. Topological Similarity-Based Compatible Aggregation

Next, we introduce how topology learners are leveraged to resolve the incompatible global aggregation. In heterogeneous FGL, clients often train their local models along divergent optimization directions due to the topological heterogeneity across their local graphs. Consequently, naive aggregation methods like FedAvg can hinder the effective transfer of valuable knowledge among clients [14, 42, 43]. To address this, we propose a personalized aggregation scheme tailored for heterogeneous FGL. In this scheme, aggregation masks for the local GNNs are customized based on the inter-client topological similarity, which is inferred from their topology learners. The underlying rationale is that clients with similar local graph topologies likely navigate similar optimization landscapes [14, 43, 44]. This approach therefore aims to promote effective aggregation by preferentially aggregating models from clients exhibiting higher topological similarity.

Local Graph Similarity Recovering. To facilitate personalized aggregation, we leverage the received topology learners on the server to estimate inter-client graph similarity. First, we construct a common probe graph, denoted as ${ \mathcal { G } } ^ { R }$ . The graph is generated with a random structure and node features sampled from a normal distribution. It is then fed as input into each of the received topology learners $\{ w _ { 1 } ^ { t } , w _ { 2 } ^ { t } , . . . , w _ { C } ^ { t } \}$ from clients. This yields a set of output representations $\{ \breve { E } _ { 1 } ^ { t } , E _ { 2 } ^ { t } , . . . , E _ { C } ^ { t } \}$ , where $E _ { c } ^ { t }$ is the output of topology learner $w _ { c } ^ { t }$ for the input ${ \mathcal { G } } ^ { R }$ . Next, we employ Centered Kernel Alignment (CKA) [24] to quantify the similarity between the output representations of pairs of topology learners. CKA is known for its effectiveness in measuring the similarity between neural network representations, even under different initializations. The rationale here is that by feeding the same input $( { \mathcal { G } } ^ { R } )$ to different learners, the similarity between their outputs can be used to assess the similarity between the learners themselves [14]. This learner similarity, in turn, reflects the similarity among the underlying local graph data topologies used to train these learners.

Personalized Aggregation. Based on these similarities, we perform personalized aggregation to compute tailored model $w _ { i } ^ { p }$ for each client i. This is achieved by taking a weighted average of all received local models $\{ w _ { 1 } , w _ { 2 } , . . . , w _ { C } \}$ , where the weights are determined by the normalized similarity between the learner outputs of client i and others:

$$
w _ {i} ^ {p} = \sum_ {j = 1} ^ {C} \alpha_ {i j} w _ {j} \quad \text { where } \quad \alpha_ {i j} = \frac {\mathbf {C K A} (E _ {i} ^ {t} , E _ {j} ^ {t})}{\sum_ {k = 1} ^ {C} \mathbf {C K A} (E _ {i} ^ {t} , E _ {k} ^ {t})}. \tag {13}
$$

Here, $\alpha _ { i j }$ represents the aggregation weight client i assigns to the model $w _ { j }$ from client j. The overall workflow is illustrated in Fig. 5(b). The server inputs a random graph to each client’s learner. The resulting embeddings are then used to compute inter-client similarities via CKA, which in turn determine the aggregation weights for each client’s personalized model. For example, when performing CKA, clients with similar topologies (blue circles in CKA part of Fig. 5(b)) receive higher aggregation weights from each other than from dissimilar ones (the blue and yellow circles). In contrast, extracting similarity from basic GNNs that only implicitly encode topology would lead to poor differentiation (e.g., the yellow and green circles).

Algorithm 1 TopFGL Server-side   
1: for each communication round $t = 1, 2, \ldots, T$ do
2: if $t \leq T \cdot r^{warm}$ then /* warm up stage */
3: Aggregate all local GNNs by Eq. (4);
4: Aggregate all local topology learners by Eq. (4);
5: else /* topological similarity-based aggregation */
6: Generate random graph $G^{R}$ ;
7: Obtain outputs $E^{t}$ from topology learners;
8: for each local GNN $w = w_{1}, w_{2}, \ldots, w_{C}$ do
9: Aggregate GNNs for w by Eq. (13);
10: end for
11: for each local learner $w^{t} = w_{1}^{t}, w_{2}^{t}, \ldots, w_{C}^{t}$ do
12: Aggregate learners for $w^{t}$ by Eq. (13);
13: end for
14: end if
15: end for

Our approach enhances client privacy by avoiding the need to share raw graph data or sensitive embeddings. Furthermore, the learners are trained on a combined representation of explicit topological embeddings and semantic features to capture local characteristics. This CKA-based aggregation then yields similarity masks that reflect both the topological resemblance and semantic aspects of each client’s graph.

Server-side Pipeline. The calculation of personalized aggregation masks relies on the topology learners. However, the learners are not yet well-trained early in the training process, leading to potentially inaccurate aggregation masks. To address this initial instability, TopFGL incorporates a warm-up stage that employs standard FedAvg to aggregate both the GNNs and the topology learners. The overall server-side procedure is detailed in Alg. 1. During each communication round, after the warm-up stage, the server receives the GNNs and topology learners from all clients. TopFGL performs topological similarity-based aggregation for each local model.

# D. Dual-model Guided Topology Augmentation

Finally, we propose the local graph augmentation module. The topology of each local graph plays a critical role, since GNNs propagate messages along the topology, bringing similar nodes closer together and pushing dissimilar nodes farther apart [45–47]. However, imbalanced topological distributions and missing links are prevalent challenges in FGL [14, 18, 48]. These issues severely undermine local graph connectivity, leaving clients with insufficient neighborhood information that hinders effective message-passing in GNNs. To address this, we leverage insights from main task GNN and topology learner to perform local augmentation. Specifically, our approach involves two steps: first, we identify topology-insufficient nodes by comparing the predictions from the two models. Second, we discover latent neighbors for these nodes within the learner’s embedding space and leverage these relationships to generate augmented structures. An example of this two-step design is shown in Fig. 6. We now proceed to detail the two steps.

![](images/ce6d0c2d110400aad96129fac5e2632128076e36434ce84d69b8bb18a3978b83.jpg)



Fig. 6: An example of the proposed topology augmentation approach. In step 1, we identify the topology-insufficient nodes $\hat { \mathcal { V } } ^ { \hat { T } I } \left( n _ { - 1 } , n _ { + 1 } \right)$ , and $n _ { + 3 } )$ . In step 2, we select augmented structures $\mathcal { E } ^ { A \dot { U } G }$ based on $\mathcal { V } ^ { T I }$ and the LCC results $\bar { \mathcal { E } } ^ { L C C }$ .

Topology-insufficient Node Detection. The first step is to identify nodes whose related topological structures are insufficient for GNN to learn distinct representations. We refer to them as topology-insufficient nodes. To detect such nodes, we employ a comparative approach, contrasting the predictions from the main task GNN (M, primarily leveraging semantic features via message-passing) with those from the topology learner $( \mathcal { M } ^ { T L }$ , incorporating both semantic features and explicit topological embeddings). The underlying rationale is straightforward. A discrepancy between the predictions for the same node can only arise from the key difference: the explicit topological information available to $\dot { \mathcal { M } } ^ { T L }$ . We therefore infer that this extra information provided critical clarifying signals, which were absent or insufficiently captured by M when relying solely on the original graph topology. Such nodes are thus deemed topology-insufficient. Therefore, we define the set of topology-insufficient nodes $\mathcal { V } ^ { T I }$ as follows:

$$
\mathcal {V} ^ {T I} = \{i \in \mathcal {V} \mid \hat {y} _ {i} ^ {T L} \neq \hat {y} _ {i} \}, \tag {14}
$$

where $\hat { y } _ { i } ^ { T L }$ and $\hat { y } _ { i }$ are the predicted labels for node i obtained from $\dot { \mathcal { M } } ^ { T L }$ and M, respectively. This set $\mathcal { V } ^ { T I }$ constitutes the candidate pool targeted for local graph augmentation.

Local Topology Augmentation. In the second step, we leverage the topology learner $( \mathcal { M } ^ { T L } )$ to generate augmented edges. The rationale is that its learned embedding space reflects topological similarities, informed by knowledge aggregated across clients. Our core idea is to identify reliable node relationships from this space to enhance the original local graph $( \mathcal { G } ^ { O } )$ . Specifically, we first utilize $\mathcal { M } ^ { T L }$ to obtain embeddings for all local nodes. Based on the proximity of these embeddings computed via KDTree, we construct a K-Nearest Neighbors (KNN) graph $\mathcal { G } ^ { K } ~ = ~ ( \nu , \mathcal { E } ^ { K } )$ , which serves as an initial blueprint of the learned topological relationships. To distill the most robust connections, we refine it by extracting its Largest Connected Component (LCC) [49, 50]:

$$
\mathcal {G} ^ {\mathrm{LCC}} = (\mathcal {V} ^ {\mathrm{LCC}}, \mathcal {E} ^ {\mathrm{LCC}}) = \mathbf {L C C} (\mathcal {G} ^ {K}). \tag {15}
$$

This LCC-based refinement is crucial for two reasons. First, it distills the learned topology by filtering out potentially noisy or less significant connections from the KNN graph. Second, it helps prevent excessive augmentation by focusing only on the most robust structural patterns [51]. The final set of augmentation edges, $\mathcal { E } ^ { A u g }$ , is then selected from this refined component $( \mathcal { G } ^ { \mathrm { L C C } } )$ . To ensure the augmentation is targeted, an edge $e = ( i , j )$ from $\mathcal { G } ^ { \mathbf { L C C } }$ is included in $\mathcal { E } ^ { A u g }$ only if both of its endpoints belong to the topology-insufficient nodes:

TABLE II: Static Information of Experimental Datasets. 

<table><tr><td>Dataset</td><td># Nodes</td><td># Edges</td><td># Features</td><td># Classes</td><td>Class types</td><td>Average Degree</td><td>Description</td></tr><tr><td>CiteSeer</td><td>3,327</td><td>9,104</td><td>3,703</td><td>6</td><td>domain</td><td>2.74</td><td>citation network</td></tr><tr><td>Cora</td><td>2,708</td><td>10,556</td><td>1,433</td><td>7</td><td>domain</td><td>3.90</td><td>citation network</td></tr><tr><td>PubMed</td><td>19,717</td><td>88,648</td><td>500</td><td>3</td><td>domain</td><td>4.50</td><td>citation network</td></tr><tr><td>CoraFull</td><td>19,793</td><td>126,842</td><td>8,710</td><td>70</td><td>domain</td><td>6.41</td><td>citation network</td></tr><tr><td>Coauthor-CS</td><td>18,333</td><td>163,788</td><td>6,805</td><td>15</td><td>field</td><td>8.93</td><td>co-authorship graph</td></tr><tr><td>Amazon-Photo</td><td>7,650</td><td>238,162</td><td>745</td><td>8</td><td>category</td><td>31.13</td><td>co-purchase graph</td></tr><tr><td>Amazon-Computers</td><td>13,752</td><td>491,722</td><td>767</td><td>10</td><td>category</td><td>35.76</td><td>co-purchase graph</td></tr><tr><td>Coauthor-Physics</td><td>34,493</td><td>495,924</td><td>8,415</td><td>5</td><td>field</td><td>14.38</td><td>co-authorship graph</td></tr><tr><td>Ogbn-Arxiv</td><td>169,343</td><td>2,315,598</td><td>128</td><td>40</td><td>areas</td><td>13.67</td><td>citation network</td></tr><tr><td>Penn94</td><td>41,554</td><td>2,724,458</td><td>4814</td><td>2</td><td>gender</td><td>65.56</td><td>social network</td></tr><tr><td>Pokec</td><td>1,632,803</td><td>30,622,564</td><td>65</td><td>2</td><td>gender</td><td>27.32</td><td>social network</td></tr></table>

Algorithm 2 TopFGL Client-side   
1: for each client $c = 1, 2, \ldots, C$ do /* before training */
2: Initialize topological embedding $h_{i}^{T}$ by Eqs. (5 ~ 12);
3: end for
4: for each communication round $t = 1, 2, \ldots, T$ do
5:    for each client $c = 1, 2, \ldots, C$ do
6:    Update topology learner and GNN;
7:    Locally train GNN and learner for l epochs;
8:    if $t\%(T \cdot r^{aug}) == 0$ then /* augmentation */
9:    Obtain candidate node set by Eq. (14);
10:    Construct KNN graph;
11:    Obtain the aug. structure by Eqs. (15, 16);
12:    Check the overfitting risk;
13:    Update local graph structure;
14:    end if
15:    Communicate the two models to server;
16:    end for
17: end for

$$
\mathcal {E} ^ {A u g} = \{e = (i, j) \in \mathcal {E} ^ {\mathbf {L C C}} \mid i \in \mathcal {V} ^ {T I} \text {   and   } j \in \mathcal {V} ^ {T I} \}. \tag {16}
$$

This augmentation is thus highly targeted, focusing on connecting pairs of topology-insufficient nodes. We then add these edges $\mathcal { E } ^ { A u g }$ to $\mathcal { G } ^ { O }$ , which allows the main task GNN to benefit from the topological insights captured by the topology learner. We illustrate the augmentation module in detail in Fig. 5(a).

To maintain efficiency, this augmentation process is not performed in every communication round but periodically at regular intervals. Furthermore, to prevent excessive modification of the original graph structure (and thus avoid potential overfitting), a control mechanism is employed: after generating $\mathcal { E } ^ { A u g }$ , if the total number of augmented edges exceeds a certain threshold (e.g., 50% of the original edge count |E|), edges are randomly pruned from $\mathcal { E } ^ { A u g }$ . This pruning is weighted by the distance between the endpoints in the topology learner’s embedding space, such that edges connecting farther apart nodes have a higher probability of being removed.

Client-side Pipeline. The overall client-side procedure is detailed in Alg. 2. Each client begins by locally training its GNN and topology learner on its local graph. At periodic intervals, clients execute an additional augmentation step.

# E. Efficiency Analysis

In this section, we analyze the computation and communication complexity of TopFGL. Without loss of generality, we consider training on GCN, where N and E are node and edge counts. Let $f ,$ h and y be the feature, hidden layer, and label dimensions. For local training, the computational complexity of standard FGL training is $\mathcal { O } ( N f h + E f )$ [19]. The communication complexity for the aggregation is $\mathcal { O } ( T C h ( f + h + y ) )$ , where T denotes the total communication rounds.

Computational Complexity. Let $f ^ { t }$ and $h ^ { t }$ denote the dimensions of the topological embeddings and the hidden layer of the topology learners, respectively. The computational complexity of the local training phase in TopFGL is $\mathcal { O } ( N ( f h + f ^ { t } h ^ { t } ) +$ $E ( f + f ^ { t } ) )$ . Since it typically holds that $h ^ { t } \ \leq \ f ^ { t } \ \ll \ f$ (owing to the lightweight nature of the topology learners), this complexity closely aligns with that of standard GCN training. The complexity of local graph augmentation is O(N log N), primarily involving the construction of a KNN graph utilizing KDTree. On the server side, let $N ^ { R }$ denote the number of nodes in the random graph. Since the random graph serves only as a probe, typically $N ^ { R } \ \ll \ N$ . The complexity of computing pairwise CKA similarities between the $C$ clients to generate personalized masks is $\mathcal { O } ( C ^ { 2 } y ^ { 2 } N ^ { R } )$ .

Communication Complexity. Collaborative training of topology learners incurs an additional complexity of $\mathcal { O } ( T C ( h ^ { t } ( f ^ { t } +$ $h ^ { t } { + } y ) { + } y ^ { 2 } ) ,$ ), which is negligible due to the lightweight design.

# IV. EXPERIMENTS

In this section, we evaluate TopFGL on various real-world graph datasets to answer the following research questions:

• RQ1: How does TopFGL compare to SOTA baselines on classification performance and computational efficiency?

TABLE III: Accuracy (%) ± standard deviation on various datasets. The best results are in bold, the second-best are underlined. 

<table><tr><td>Cli.</td><td>Method</td><td>CiteSeer</td><td>Cora</td><td>PubMed</td><td>CoraFull</td><td>CS</td><td>Photo</td><td>Computers</td><td>Physics</td><td>Arxiv</td><td>Penn94</td></tr><tr><td rowspan="8">10</td><td>Local</td><td>63.7 ± 0.5</td><td>79.6 ± 0.6</td><td>82.9 ± 0.2</td><td>59.9 ± 0.2</td><td>88.7 ± 0.1</td><td>90.1 ± 0.2</td><td>87.6 ± 0.2</td><td>93.9 ± 0.1</td><td>69.4 ± 0.1</td><td>69.4 ± 0.1</td></tr><tr><td>FedAvg</td><td>69.2 ± 0.4</td><td>80.9 ± 0.3</td><td>86.0 ± 0.1</td><td>59.2 ± 0.2</td><td>87.6 ± 0.9</td><td>65.2 ± 0.4</td><td>63.8 ± 0.1</td><td>95.2 ± 0.3</td><td>62.5 ± 0.2</td><td>69.2 ± 0.2</td></tr><tr><td>FedProx</td><td>68.9 ± 0.3</td><td>78.5 ± 2.2</td><td>86.8 ± 0.1</td><td>59.4 ± 0.2</td><td>87.8 ± 0.9</td><td>52.9 ± 0.7</td><td>62.2 ± 0.2</td><td>95.3 ± 0.1</td><td>60.6 ± 0.4</td><td>70.1 ± 0.2</td></tr><tr><td>GCFL+</td><td>67.6 ± 0.6</td><td>81.0 ± 0.6</td><td>84.8 ± 0.2</td><td>59.2 ± 0.2</td><td>87.6 ± 0.9</td><td>66.5 ± 2.9</td><td>73.1 ± 4.3</td><td>94.4 ± 0.2</td><td>62.5 ± 0.2</td><td>69.8 ± 0.6</td></tr><tr><td>FedStar</td><td>57.6 ± 0.8</td><td>76.6 ± 0.8</td><td>83.3 ± 0.3</td><td>55.6 ± 0.4</td><td>87.5 ± 0.2</td><td>86.9 ± 0.4</td><td>83.9 ± 0.2</td><td>93.2 ± 0.2</td><td>67.5 ± 0.1</td><td>68.2 ± 0.3</td></tr><tr><td>FED-PUB</td><td>65.7 ± 0.2</td><td>81.9 ± 0.3</td><td>85.0 ± 0.2</td><td>62.1 ± 0.2</td><td>90.7 ± 0.1</td><td>92.4 ± 0.1</td><td>89.0 ± 0.1</td><td>94.6 ± 0.1</td><td>69.8 ± 0.1</td><td>71.0 ± 0.1</td></tr><tr><td>FedGTA</td><td>70.3 ± 0.3</td><td>81.7 ± 0.2</td><td>86.6 ± 0.1</td><td>63.0 ± 0.1</td><td>90.8 ± 0.1</td><td>91.9 ± 0.1</td><td>85.4 ± 0.1</td><td>95.5 ± 0.1</td><td>66.8 ± 0.1</td><td>71.4 ± 0.1</td></tr><tr><td>AdaFGL</td><td>68.5 ± 0.6</td><td>83.6 ± 0.4</td><td>86.1 ± 0.2</td><td>62.8 ± 0.3</td><td>92.0 ± 0.1</td><td>90.6 ± 0.1</td><td>85.3 ± 0.5</td><td>95.2 ± 0.1</td><td>64.3 ± 0.2</td><td>73.0 ± 0.1</td></tr><tr><td></td><td>TopFGL</td><td>72.3 ± 0.9</td><td>85.9 ± 0.8</td><td>87.7 ± 0.6</td><td>64.7 ± 0.3</td><td>93.8 ± 0.3</td><td>92.8 ± 0.5</td><td>91.5 ± 0.5</td><td>96.2 ± 0.2</td><td>74.8 ± 0.4</td><td>78.6 ± 2.5</td></tr><tr><td rowspan="8">20</td><td>Local</td><td>59.5 ± 0.6</td><td>77.3 ± 0.2</td><td>82.2 ± 0.2</td><td>57.7 ± 0.3</td><td>87.5 ± 0.1</td><td>89.1 ± 0.3</td><td>87.3 ± 0.2</td><td>93.9 ± 0.2</td><td>69.5 ± 0.1</td><td>63.6 ± 0.2</td></tr><tr><td>FedAvg</td><td>68.8 ± 0.1</td><td>78.3 ± 1.7</td><td>86.3 ± 0.1</td><td>52.9 ± 0.5</td><td>84.7 ± 1.6</td><td>68.9 ± 1.7</td><td>72.4 ± 0.8</td><td>94.8 ± 0.1</td><td>59.1 ± 0.7</td><td>67.1 ± 0.2</td></tr><tr><td>FedProx</td><td>70.3 ± 0.3</td><td>72.2 ± 1.2</td><td>87.0 ± 0.1</td><td>53.4 ± 0.5</td><td>85.1 ± 1.6</td><td>49.9 ± 3.9</td><td>64.6 ± 1.3</td><td>94.8 ± 0.1</td><td>56.0 ± 1.1</td><td>67.6 ± 0.2</td></tr><tr><td>GCFL+</td><td>68.4 ± 0.6</td><td>79.7 ± 0.7</td><td>85.8 ± 0.1</td><td>52.9 ± 0.5</td><td>84.7 ± 1.6</td><td>70.4 ± 1.7</td><td>73.9 ± 0.6</td><td>94.9 ± 0.1</td><td>59.1 ± 0.8</td><td>66.6 ± 0.4</td></tr><tr><td>FedStar</td><td>56.3 ± 1.0</td><td>70.7 ± 1.3</td><td>81.6 ± 0.3</td><td>52.8 ± 0.2</td><td>85.7 ± 0.4</td><td>86.1 ± 0.4</td><td>83.3 ± 0.4</td><td>92.6 ± 0.1</td><td>66.9 ± 0.2</td><td>63.1 ± 0.3</td></tr><tr><td>FED-PUB</td><td>68.1 ± 0.4</td><td>78.9 ± 0.2</td><td>84.9 ± 0.3</td><td>59.8 ± 0.2</td><td>89.8 ± 0.1</td><td>91.0 ± 0.3</td><td>88.7 ± 0.2</td><td>94.5 ± 0.1</td><td>70.2 ± 0.1</td><td>66.9 ± 0.1</td></tr><tr><td>FedGTA</td><td>71.7 ± 0.2</td><td>81.7 ± 0.2</td><td>87.0 ± 0.1</td><td>61.4 ± 0.1</td><td>90.6 ± 0.1</td><td>91.8 ± 0.1</td><td>83.5 ± 0.7</td><td>95.5 ± 0.1</td><td>66.3 ± 0.1</td><td>70.6 ± 0.1</td></tr><tr><td>AdaFGL</td><td>67.2 ± 0.3</td><td>81.0 ± 0.4</td><td>86.9 ± 0.2</td><td>60.8 ± 0.1</td><td>89.8 ± 0.1</td><td>90.7 ± 0.2</td><td>85.5 ± 0.1</td><td>95.3 ± 0.1</td><td>63.5 ± 0.1</td><td>70.4 ± 0.2</td></tr><tr><td></td><td>TopFGL</td><td>76.8 ± 1.2</td><td>86.9 ± 0.7</td><td>88.8 ± 0.6</td><td>63.8 ± 0.8</td><td>92.5 ± 0.5</td><td>92.4 ± 0.4</td><td>89.3 ± 0.8</td><td>95.8 ± 0.3</td><td>72.0 ± 0.6</td><td>72.4 ± 1.9</td></tr></table>

• RQ2: Can TopFGL maintain robust adaptability across different topological distributions and various client counts?   
• RQ3: How do the main modules and key hyperparameters influence TopFGL’s performance?

# A. Experimental Setup

Datasets and Partitioning. We evaluate TopFGL and all baselines on multiple graph datasets, including the regularscale graphs Cora, CiteSeer, and PubMed [52]; the mediumscale graphs CoraFull, Coauthor CS and Physics [53], Amazon Photo and Computers [53]; the large-scale datasets Penn94 [54], Ogbn-Arxiv [55] and Pokec [54]. The detailed information of datasets is shown in Tab. II. Following the setup in [14, 15, 20, 56], we randomly sample 20% of the nodes for training, 40% for validation, and 40% for testing.

For heterogeneous graph partitions, we employ the METIS algorithm [57], which is widely used to construct topologically heterogeneous distributed graphs in FGL scenarios [6, 14, 15, 20, 56]. Additionally, to assess the adaptability of TopFGL against diverse, realistic heterogeneous distributions, we introduce two specific configurations beyond the basic heterogeneous partitioning: NV. Heterogeneity: Node Sharing and View Redundancy Heterogeneity. This setup features node overlap, allowing the same real-world entity (node) to be partially represented in the datasets of multiple clients. It models scenarios where data silos hold fragmented and overlapping information [14, 58], requiring GNNs to reconcile differing local topological views for shared nodes. IS. Heterogeneity: Intrinsic Structural Signal Heterogeneity. This setup directly manipulates the graph’s intrinsic structure before partitioning. By removing a portion of homogeneous edges (connecting same-labeled nodes) while preserving all heterogeneous edges, we generate a global graph with reduced topological homogeneity. Clients thus receive partitions where connectivity and label similarity are weakened. This simulates graphs deviating from topological homogeneity assumptions, amplifying existing data distribution heterogeneity across clients.

Baselines. For the FL methods, we selected Local [40], FedAvg [26] and FedProx [59]. For the graph-level FGL methods, we chose GCFL+ [13] and FedStar [12]. We kept their algorithm and changed the classification head of GNN to the node classification version. We also compared with three node-level personalized FGL frameworks, including a popular baseline FED-PUB [14], the state-of-the-art baseline FedGTA [20] and the latest baseline AdaFGL [15]. For FedGTA, we utilized the official implementation, which employs the GAMLP model [60] within its optimization. We executed each baseline 5 times with different random seeds and report the mean and standard deviation of the results.

Implementation Details. We utilize GCN [40] for the network of all baselines, with the hidden layer dimension set to 128. The Adam optimizer [61] is employed with a learning rate of $1 0 ^ { - 2 }$ and weight decay of $1 0 ^ { - 8 }$ . Federated graph learning is performed over 100 communication rounds across all datasets. We set local epochs to 2 by default, increasing this to 4 for the CoraFull, Photo, and Computers datasets to ensure proper convergence. By default, the warm-up ratio is set to 0.3, the number of augmentations to 3, and the number of neighbors (k) for KNN to 8. For the topology learner, the dimensions of the random walk embedding, homogeneous embedding and hidden layer are set to 8, 2 and 8, respectively. Experiments ran on a system equipped with an Intel Xeon Gold 5420+ CPU (4.10GHz), 512GB of RAM, the GPU is NVIDIA A40 48GB. The system ran Ubuntu 22.04 with CUDA 12.2.

# B. Effectiveness and Efficiency Analysis (RQ1)

Performance on Various Datasets. We present the performance of TopFGL and baselines in Tab. III. Results show that

![](images/95ad09d74118a76d77b8371ca1e2fb9fbbda1a0515bd8a26458a3ca0df71d5a3.jpg)  
Fig. 8: Comparison of computational efficiency with existing FGL frameworks. The x-axis represents training time (s), while the y-axis represents test accuracy (%). Better performance is closer to the top-left (↖) region.

TABLE IV: Accuracy (%) and training time (h) on Pokec dataset. OOM: Out of memory. OOT: Out of time (10h). 

<table><tr><td rowspan="2">Method</td><td colspan="2">20 Clients</td><td colspan="2">50 Clients</td><td colspan="2">100 Clients</td></tr><tr><td>Acc.</td><td>Time</td><td>Acc.</td><td>Time</td><td>Acc.</td><td>Time</td></tr><tr><td>Local</td><td>56.42</td><td>0.06</td><td>56.89</td><td>0.08</td><td>57.19</td><td>0.08</td></tr><tr><td>FedAvg</td><td>56.01</td><td>0.08</td><td>54.68</td><td>0.10</td><td>55.33</td><td>0.10</td></tr><tr><td>FedProx</td><td>53.29</td><td>0.08</td><td>52.80</td><td>0.10</td><td>52.41</td><td>0.10</td></tr><tr><td>GCFL</td><td>55.96</td><td>0.08</td><td>54.74</td><td>0.10</td><td>55.40</td><td>0.11</td></tr><tr><td>FedStar</td><td>--</td><td>OOT</td><td>--</td><td>OOT</td><td>--</td><td>OOT</td></tr><tr><td>FED-PUB</td><td>57.97</td><td>0.18</td><td>60.23</td><td>0.41</td><td>59.94</td><td>0.79</td></tr><tr><td>FedGTA</td><td>59.87</td><td>3.21</td><td>58.82</td><td>3.58</td><td>59.01</td><td>4.82</td></tr><tr><td>AdaFGL</td><td>OOM</td><td>--</td><td>OOM</td><td>--</td><td>58.95</td><td>7.76</td></tr><tr><td>TopFGL</td><td>62.30</td><td>0.41</td><td>62.34</td><td>0.44</td><td>61.21</td><td>0.47</td></tr></table>

TopFGL significantly outperforms all baselines, achieving up to 5.6% performance improvement over the strongest baselines FedGTA and AdaFGL. Traditional FL methods, FedAvg and FedProx, face performance degradation in heterogeneous FGL scenarios due to incompatible global knowledge aggregation. Graph-level FGL methods, GCFL+ and FedStar, exhibit moderate performance gains due to their attempts to identify and differentiate the topological characteristics across clients. Personalized FGL methods, FED-PUB, FedGTA, and AdaFGL, achieve better performance by reconciling incompatible topology knowledge from multiple clients. TopFGL achieves the best performance, thanks to its two topology-aware modules to systematically tackle topological heterogeneity.

Performance on Large-scale Graph Dataset. As shown in Tab. IV, we evaluate TopFGL and all baselines on the Pokec dataset, comparing their test accuracy and training time. Experimental results reveal that most baselines underperform on this large-scale graph. Traditional FL methods exhibit performance degradation, with both FedGTA and FED-PUB achieving suboptimal results. In contrast, TopFGL consistently delivers optimal performance while incurring lower computational costs. Specifically, with 20 clients, TopFGL surpasses the SOTA method by achieving a 2.4% improvement in accuracy while requiring only 12.8% of the training time, showing a 7× speedup. These findings highlight TopFGL’s significant potential for federated training on large-scale graphs.

TABLE V: Communication cost (GB) in FGL with 20 clients. Size: Model size (KB) on a single client. 

<table><tr><td rowspan="3">Datasets</td><td rowspan="2" colspan="2">FedAvg</td><td colspan="6">TopFGL</td></tr><tr><td colspan="2">main GNN</td><td colspan="2">Learner</td><td colspan="2">Total</td></tr><tr><td>Size</td><td>Comm.</td><td>Size</td><td>Comm.</td><td>Size</td><td>Comm.</td><td>Size</td><td>Comm.</td></tr><tr><td>Pokec</td><td>99.0</td><td>0.378</td><td>99.0</td><td>0.378</td><td>0.4</td><td>0.002</td><td>99.4</td><td>0.380</td></tr><tr><td>Arxiv</td><td>149.2</td><td>0.569</td><td>149.2</td><td>0.569</td><td>7.3</td><td>0.028</td><td>156.5</td><td>0.597</td></tr><tr><td>PubMed</td><td>316.5</td><td>1.207</td><td>316.5</td><td>1.207</td><td>0.4</td><td>0.002</td><td>316.9</td><td>1.209</td></tr><tr><td>Photo</td><td>441.5</td><td>1.684</td><td>441.5</td><td>1.684</td><td>0.7</td><td>0.003</td><td>442.2</td><td>1.687</td></tr><tr><td>Computer</td><td>453.5</td><td>1.730</td><td>453.5</td><td>1.730</td><td>0.8</td><td>0.003</td><td>454.3</td><td>1.733</td></tr><tr><td>Cora</td><td>785.0</td><td>2.995</td><td>785.0</td><td>2.995</td><td>0.6</td><td>0.002</td><td>785.6</td><td>2.997</td></tr><tr><td>CiteSeer</td><td>1919.5</td><td>7.322</td><td>1919.5</td><td>7.322</td><td>0.6</td><td>0.002</td><td>1920.1</td><td>7.324</td></tr><tr><td>Penn94</td><td>2473.5</td><td>9.436</td><td>2473.5</td><td>9.436</td><td>0.4</td><td>0.002</td><td>2473.9</td><td>9.438</td></tr><tr><td>CS</td><td>3475.1</td><td>13.256</td><td>3475.1</td><td>13.256</td><td>1.4</td><td>0.005</td><td>3476.5</td><td>13.261</td></tr><tr><td>Physics</td><td>4275.0</td><td>16.308</td><td>4275.0</td><td>16.308</td><td>0.5</td><td>0.002</td><td>4275.5</td><td>16.310</td></tr><tr><td>CoraFull</td><td>4455.3</td><td>16.996</td><td>4455.3</td><td>16.996</td><td>21.3</td><td>0.081</td><td>4476.6</td><td>17.077</td></tr></table>

Communication Efficiency. Tab. V presents the minor additional communication cost introduced by TopFGL. Thanks to the lightweight design of topology learner, the global aggregation required for this model is efficient and scalable.

TABLE VI: Accuracy (%) ± standard deviation of all methods on graphs with intrinsic structural signal heterogeneity. 

<table><tr><td rowspan="3">Method</td><td colspan="4">CoraFull Dataset</td><td colspan="4">Coauthor-CS Dataset</td></tr><tr><td colspan="2">Weakened 30%</td><td colspan="2">Weakened 60%</td><td colspan="2">Weakened 30%</td><td colspan="2">Weakened 60%</td></tr><tr><td>10 Clients</td><td>20 Clients</td><td>10 Clients</td><td>20 Clients</td><td>10 Clients</td><td>20 Clients</td><td>10 Clients</td><td>20 Clients</td></tr><tr><td>Local</td><td>52.65 ± 0.14</td><td>51.10 ± 0.10</td><td>43.51 ± 0.07</td><td>40.66 ± 0.20</td><td>83.79 ± 0.21</td><td>81.73 ± 0.09</td><td>78.12 ± 0.20</td><td>73.24 ± 0.14</td></tr><tr><td>FedAvg</td><td>54.83 ± 0.44</td><td>50.25 ± 1.26</td><td>46.38 ± 0.14</td><td>45.66 ± 0.31</td><td>88.90 ± 0.14</td><td>85.86 ± 0.29</td><td>84.34 ± 0.17</td><td>83.55 ± 0.07</td></tr><tr><td>FedProx</td><td>55.17 ± 0.39</td><td>50.79 ± 1.14</td><td>46.62 ± 0.08</td><td>46.40 ± 0.12</td><td>88.93 ± 0.19</td><td>85.94 ± 0.25</td><td>84.35 ± 0.15</td><td>83.56 ± 0.15</td></tr><tr><td>GCFL+</td><td>54.82 ± 0.43</td><td>50.24 ± 1.26</td><td>46.39 ± 0.17</td><td>45.69 ± 0.29</td><td>88.90 ± 0.14</td><td>85.85 ± 0.28</td><td>84.35 ± 0.17</td><td>83.55 ± 0.07</td></tr><tr><td>FedStar</td><td>47.30 ± 0.55</td><td>44.21 ± 0.49</td><td>37.84 ± 0.06</td><td>34.60 ± 0.26</td><td>81.99 ± 0.18</td><td>79.05 ± 0.16</td><td>75.69 ± 0.44</td><td>69.38 ± 0.42</td></tr><tr><td>FED-PUB</td><td>55.17 ± 0.10</td><td>53.62 ± 0.17</td><td>46.96 ± 0.14</td><td>44.24 ± 0.09</td><td>87.31 ± 0.11</td><td>85.86 ± 0.09</td><td>82.65 ± 0.12</td><td>80.59 ± 0.10</td></tr><tr><td>FedGTA</td><td>56.86 ± 0.02</td><td>54.72 ± 0.04</td><td>49.90 ± 0.08</td><td>46.04 ± 0.09</td><td>88.66 ± 0.03</td><td>89.33 ± 0.07</td><td>86.89 ± 0.06</td><td>86.55 ± 0.02</td></tr><tr><td>AdaFGL</td><td>56.19 ± 0.12</td><td>54.07 ± 0.37</td><td>49.29 ± 0.27</td><td>44.79 ± 0.37</td><td>89.47 ± 0.07</td><td>87.57 ± 0.16</td><td>86.66 ± 0.06</td><td>84.65 ± 0.23</td></tr><tr><td>TopFGL</td><td>59.36 ± 0.67</td><td>58.97 ± 0.44</td><td>53.12 ± 0.44</td><td>50.32 ± 0.77</td><td>92.12 ± 0.46</td><td>90.59 ± 0.63</td><td>87.99 ± 0.58</td><td>88.86 ± 0.81</td></tr></table>

TABLE VII: Average per-client time for topological embedding initialization. 

<table><tr><td>Scenario</td><td>CiteSeer</td><td>PubMed</td><td>CS</td><td>Physics</td></tr><tr><td>10 Clients</td><td>0.33 s</td><td>1.08 s</td><td>1.18 s</td><td>2.33 s</td></tr><tr><td>20 Clients</td><td>0.18 s</td><td>0.51 s</td><td>0.61 s</td><td>1.52 s</td></tr></table>

Computational Efficiency. Fig. 8 shows the comparison of computational efficiency across various datasets. TopFGL shows the most favorable trade-off, achieving a 5.6% accuracy improvement along with a significant reduction of 50.0% training time compared to SOTA methods on the Penn94 dataset. While FedAvg, FedStar, GCFL, and FedProx achieve faster training, they fail to deliver satisfactory classification performance. FED-PUB improves accuracy but incurs significant cost. AdaFGL and FedGTA achieve better performance through personalized approaches, but their personalized approaches also reduce computational efficiency. TopFGL shows an optimal balance between computational efficiency and accuracy. Finally, Tab. VII reports the one-time cost of initializing the topological embeddings before training.

# C. Adaptability Analysis (RQ2)

Adaptability on Graphs with NV. Heterogeneity. As shown in Tab. VIII, we test TopFGL and all baselines on graphs with node sharing and view redundancy heterogeneity. Local, FedAvg, and FedStar struggle to achieve acceptable performance, while FED-PUB, AdaFGL, and FedGTA perform better by capturing the difference in local topology and adapting to heterogeneity. TopFGL shows the best adaptability by effectively learning topology patterns and leveraging learned knowledge to empower its two key modules to tackle heterogeneity.

Adaptability on Graphs with IS. Heterogeneity. To evaluate TopFGL on graphs with weakened topological homogeneity, we classified the edges into homogeneous and heterogeneous categories, retained all heterogeneous edges, and removed 30% or 60% of the homogeneous edges. We show the results in Tab. VI. Since GNNs rely on homogeneous edges for neighborhood aggregation [33, 34, 62], existing methods experience performance degradation. While AdaFGL and FedGTA show suboptimal performance, TopFGL achieves the best adaptability, with up to 4.3% performance improvement. This is attributed to its dual-model guided augmentation process, which enriches the neighborhood connections of local nodes.

TABLE VIII: Accuracy (%) ± standard deviation on graphs with node sharing and view redundancy heterogeneity. 

<table><tr><td>Client Count</td><td>Method</td><td>Cora</td><td>CS</td><td>Physics</td></tr><tr><td rowspan="8">10 C.</td><td>Local</td><td>73.08 ± 0.27</td><td>86.84 ± 0.12</td><td>93.83 ± 0.05</td></tr><tr><td>FedAvg</td><td>75.44 ± 0.68</td><td>90.66 ± 0.19</td><td>94.96 ± 0.06</td></tr><tr><td>FedProx</td><td>75.14 ± 1.54</td><td>90.73 ± 0.19</td><td>95.02 ± 0.08</td></tr><tr><td>GCFL+</td><td>76.99 ± 1.53</td><td>90.67 ± 0.20</td><td>94.88 ± 0.10</td></tr><tr><td>FedStar</td><td>69.49 ± 0.97</td><td>85.61 ± 0.18</td><td>93.47 ± 0.17</td></tr><tr><td>FED-PUB</td><td>78.15 ± 0.35</td><td>89.67 ± 0.06</td><td>94.78 ± 0.03</td></tr><tr><td>FedGTA</td><td>77.44 ± 0.04</td><td>90.56 ± 0.07</td><td>95.50 ± 0.06</td></tr><tr><td>AdaFGL</td><td>79.44 ± 0.25</td><td>90.59 ± 0.10</td><td>95.64 ± 0.07</td></tr><tr><td></td><td>TopFGL</td><td>84.37 ± 1.31</td><td>94.16 ± 0.65</td><td>96.46 ± 0.14</td></tr><tr><td rowspan="8">20 C.</td><td>Local</td><td>76.13 ± 0.50</td><td>86.01 ± 0.07</td><td>92.25 ± 0.11</td></tr><tr><td>FedAvg</td><td>74.59 ± 0.50</td><td>84.74 ± 0.84</td><td>94.21 ± 0.04</td></tr><tr><td>FedProx</td><td>73.50 ± 0.92</td><td>85.12 ± 0.94</td><td>94.24 ± 0.06</td></tr><tr><td>GCFL+</td><td>76.33 ± 0.55</td><td>84.74 ± 0.85</td><td>93.95 ± 0.04</td></tr><tr><td>FedStar</td><td>72.53 ± 0.61</td><td>83.49 ± 0.12</td><td>91.96 ± 0.13</td></tr><tr><td>FED-PUB</td><td>78.50 ± 0.26</td><td>89.48 ± 0.06</td><td>93.97 ± 0.03</td></tr><tr><td>FedGTA</td><td>79.21 ± 0.04</td><td>89.82 ± 0.04</td><td>94.56 ± 0.01</td></tr><tr><td>AdaFGL</td><td>77.95 ± 0.47</td><td>89.95 ± 0.16</td><td>94.83 ± 0.05</td></tr><tr><td></td><td>TopFGL</td><td>86.13 ± 1.29</td><td>92.72 ± 0.16</td><td>95.94 ± 0.18</td></tr></table>

Adaptability to Various Client Counts. Fig. 9 shows the model performance alongside the topological heterogeneity score $\mathcal { H } _ { p a i r w i s e }$ for each client partitioning. Experimental results demonstrate that TopFGL consistently outperforms SOTA baselines FedGTA and AdaFGL across all measured levels of heterogeneity. Notably, the performance advantage of TopFGL becomes more pronounced as the heterogeneity score increases. For instance, on the Cora dataset, as $\mathcal { H } _ { p a i r w i s e }$ increases from 0.62 (3 clients) to 0.70 (20 clients), TopFGL’s accuracy improvement over FedGTA grows from 1.2% to 5.3%. This leads to a practical guideline: users should especially prioritize TopFGL when dealing with distributed graph data measured to have high topological heterogeneity.

![](images/9b07b561b799e1058770057eebdf945e3b77ed964e1cbbfea187ef9139354e0c.jpg)  
Fig. 9: Performance under various client counts. The bars (right y-axis) quantify the topological heterogeneity Hpairwise.

![](images/23b762d9ef438a9a2f45594b4c7b3c80878cb6f7c5f9eb1253fd421b7fd7a41b.jpg)  
(a) CoraFull

![](images/7b63c7d8002a2c66b828add4c9e9af6b30cc414ad38ceb4ffc467bbb989e9eac.jpg)



(b) Coauthor-CS   
Fig. 10: Ablation study of two key modules in TopFGL.

# D. Ablation Study (RQ3)

Effectiveness of Two Key Modules in TopFGL. We investigate the importance of the topological similarity-based aggregation module and local graph topology augmentation module on CoraFull and Coauthor-CS datasets with various client count settings. Specifically, the two key modules are individually removed from TopFGL, while keeping other settings unchanged. We compare the following variations: (1) Base: Includes neither module, equivalent to FedAvg. (2) Only Agg.: Uses only the topological similarity-based aggregation module. (3) Only Aug.: Uses only the local graph topology augmentation module. (4) TopFGL: Includes all modules.

The results presented in Fig. 10 underscore the essential contribution of both modules. In particular, local graph augmentation is crucial in heterogeneous FGL. Since TopFGL enables clients to collaboratively learn topology patterns, some clients with extremely imbalanced distributions could recover performance through the dual-model guided enhancement process. Topological similarity-based aggregation also plays a key role, facilitating compatible aggregation among clients and becoming more important with a larger number of clients.

Effectiveness of CKA Utilized in Aggregation Module. To validate our choice of CKA for the aggregation module, we evaluated several alternative similarity measures: Cosine Similarity (Cos.), Euclidean Distance (Eu.), Maximum Mean Discrepancy (Mmd.), and Frechet Inception Distance (Fid.). ´ The results in Tab. IX show that CKA delivered the best performance, especially on CoraFull, which is attributed to its ability to capture similarity in high-dimensional embeddings.

# E. Sensitivity Analysis (RQ3)

Number of Neighbors in KNN. We investigate the impact of the neighbors number k used for constructing KNN graph

![](images/f5ac2da9c775f4b62e86481e65476506eba744632456bd03d450263378dd6b8d.jpg)



![](images/0353de640aca5ffe6a7058b99bcafd0261a9c59ed5c91ada305d050efa2d17e6.jpg)



Fig. 11: Sensitivity analysis of dimensions in topology learner.

TABLE IX: Accuracy (%) ± standard deviation of various similarity measures within the personalized aggregation module. 

<table><tr><td rowspan="2">Metric</td><td colspan="2">PubMed</td><td colspan="2">CoraFull</td></tr><tr><td>10 Clients</td><td>20 Clients</td><td>10 Clients</td><td>20 Clients</td></tr><tr><td>Cos.</td><td> $87.50 \pm 0.53$ </td><td> $\underline{88.71 \pm 0.61}$ </td><td> $58.96 \pm 0.48$ </td><td> $\underline{56.19 \pm 0.71}$ </td></tr><tr><td>Eu.</td><td> $87.32 \pm 0.65$ </td><td> $88.40 \pm 0.60$ </td><td> $\underline{59.13 \pm 0.30}$ </td><td> $56.10 \pm 0.88$ </td></tr><tr><td>Mmd.</td><td> $85.28 \pm 1.63$ </td><td> $85.34 \pm 2.98$ </td><td> $59.06 \pm 0.34$ </td><td> $54.55 \pm 1.84$ </td></tr><tr><td>Fid.</td><td> $\underline{87.59 \pm 0.53}$ </td><td> $88.69 \pm 0.64$ </td><td> $58.86 \pm 0.43$ </td><td> $\underline{56.19 \pm 1.06}$ </td></tr><tr><td>CKA.</td><td> $\underline{87.66 \pm 0.59}$ </td><td> $\underline{88.80 \pm 0.61}$ </td><td> $\underline{64.73 \pm 0.27}$ </td><td> $\underline{63.84 \pm 0.76}$ </td></tr></table>

in augmentation. The results in Fig. 12 (a), (b) show that the overall performance remains relatively stable across different values of k, demonstrating the robustness of our augmentation method to k. This suggests that our subsequent filtering steps effectively utilize the structural information provided by the KNN graph, mitigating sensitivity to the initial number of neighbors. Thus, we set k = 8 for the main experiments.

Number of Augmentations. Fig. 12 (c), (d) illustrates the sensitivity to the number of local augmentations during training. We observe a significant performance improvement as the number of augmentations initially increases. Subsequently, further increasing this value yields less pronounced gains, indicating diminishing returns. While performing augmentation frequently could be beneficial for addressing heterogeneity, it also increases computational cost. Therefore, we set the number of graph augmentations to 3 in main experiments.

Dimensions in Topology Learner. We evaluated the sensitivity to the dimensions of the input RW embedding and the hidden layer on the PubMed dataset. The results in Fig. 11 show that the learner exhibits remarkable robustness even at low dimensions. This validates our lightweight design principle, which enhances efficiency while preserving performance. Accordingly, we set both dimensions to 8 in main experiments.

![](images/15401dc53129c3103539e984c7109021fc6b7572c23b0aadbe49e13a835a6fd1.jpg)



(a) k - CS

![](images/70c6b7380f03e0dd02d02471520d8317041e962e742e9e8b0d2f547da525aa76.jpg)



(b) k - Physics

![](images/bbd512e83f2de40f2de467a3379e9c917f5c6fb9a42e994e1860247a2a5b0924.jpg)



(c) Num. of Aug. - CS

![](images/d5f5d2b35ca4ec8752c5ca95d119d082855244fb07562b36d93f4abbfa2723ca.jpg)



(d) Num. of Aug. - Physics   
Fig. 12: Results of sensitivity analysis on the Coauthor-CS and Physics datasets with various client count settings.

# V. RELATED WORK

Recent FGL studies can be categorized into graph-level and subgraph-level works. Graph-level FGL focuses on the graph classification task. GCFL [13] proposes gradient-based client clustering to address heterogeneity. FedStar [12] proposes multichannel GNNs for structural learning. FGGP [63] captures domain information by clustering prototypes. Subgraph-level FGL focuses on node classification and link prediction, which can be further divided into two categories: federated model guidance and class-wise knowledge-sharing.

Federated Model Guidance. Existing works have investigated leveraging federated trained basic GNNs to tackle topological heterogeneity. FED-PUB [14] infers local topology similarity from the similarity of GNN outputs on the server. FGSSL [16] employs the global GNN to guide local contrastive learning. AdaFGL [15] trains the basic GNN as a global knowledge extractor, and designs additional personalized rounds to extract homogeneous and heterogeneous knowledge for guidance of local optimization. These methods directly extract topological signals from topology-unaware basic GNNs lacking effectiveness guarantees. TopFGL is the first subgraph-level FGL framework that attempts to explicitly encode local topologies to train lightweight topology learners, which provide unambiguous guidance to tackle topological heterogeneity.

Class-wise Knowledge-Sharing. Recent research has focused on sharing local class-wise intermediate information to tackle heterogeneity. FedSage [18] trains missing neighbor generators through client information exchange for local graph enhancement. ProtoFGL [64] shares local prototypes for knowledge distillation. FedTAD [21] requires clients to share classwise reliability derived from local topologies and embeddings to perform knowledge distillation. FedSpray [19] requires clients to share class-wise structure proxies and align them. FedGTA [20] requires clients to share local smoothing confidence and mixed moments of neighbor features to perform similarity-based aggregation. These works achieve robustness to heterogeneity but inevitably sacrifice graph data privacy. TopFGL introduces a new privacy-effectiveness trade-off via topology learner, offering an efficient and adaptive alternative.

# VI. DISCUSSION AND FUTURE WORK

Support for Structure Updates. TopFGL requires only a one-time initialization when the structure is static. In dynamic scenarios where the structure evolves, the need to frequently update topological embeddings introduces additional computational cost. Fortunately, TopFGL is extensible to incorporating dynamic structure encoding approaches, such as detecting and updating only changed parts [27, 65, 66], or directly modeling the temporal evolution of structural embeddings [3, 4, 67]. These methods are orthogonal to TopFGL, allowing it to seamlessly integrate them without altering its core components.

Limitations. Our CKA-based aggregation measures similarity by providing all topology learners with an identical random probe graph rather than using shared local intermediate information. Consequently, the effectiveness of TopFGL relies on the valuable local topological knowledge learned by the topology learners. However, this strong emphasis on topology also frames the applicability of our framework. The performance of TopFGL may diminish in scenarios where the graph structure is noisy or detrimental to representation learning; in such cases, methods that prioritize semantic feature similarities might be more effective [16, 20]. While extensive experiments have validated the overall performance and effectiveness of the aggregation module, a theoretical analysis would further enhance its completeness, which we leave for future work.

Further Evaluation on link prediction. Since the core design of TopFGL via the topology learner is fundamentally taskagnostic, standard graph learning tasks like link prediction can naturally benefit from the learned expressive node embeddings. However, there still lacks thorough investigation on mature and standardized approaches for partitioning graphs to create the necessary topological heterogeneity for link prediction task, which could be a promising direction for future FGL studies.

# VII. CONCLUSION

In this paper, we address key limitations of existing FGL works that tackle topological heterogeneity, including the need to share sensitive information, high computational costs, and narrow adaptability. We propose TopFGL, a topologyaware and distribution-agnostic framework that tackles these challenges by leveraging lightweight topology learners. Empowered by a multi-level topology extraction scheme and an efficient training pipeline, TopFGL adaptively learns local topological patterns. This knowledge drives two key modules that systematically tackle heterogeneity: a server-side compatible aggregation scheme and a client-side structural augmentation approach. Extensive experiments demonstrate the effectiveness, efficiency and adaptability of proposed TopFGL.

# VIII. ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 62441228, Science and Technology Tackling Program of Anhui Province, No.202423k09020016.

# IX. AI-GENERATED CONTENT ACKNOWLEDGEMENT

All content in this paper was written by the authors. No AI tools were used in the creation of this manuscript.

# REFERENCES

[1] Jana Vatter, Ruben Mayer, and Hans-Arno Jacobsen. “The evolution of distributed systems for graph neural networks and their origin in graph processing and deep learning: A survey”. In: ACM Computing Surveys 56.1 (2023), pp. 1–37.   
[2] Junliang Yu, Hongzhi Yin, Jundong Li, Qinyong Wang, Nguyen Quoc Viet Hung, and Xiangliang Zhang. “Self-supervised multi-channel hypergraph convolutional network for social recommendation”. In: Proceedings of the web conference 2021. 2021, pp. 413–424.   
[3] Yuanyuan Xu, Wenjie Zhang, Ying Zhang, Maria Orlowska, and Xuemin Lin. “TimeSGN: Scalable and Effective Temporal Graph Neural Network”. In: 2024 IEEE 40th International Conference on Data Engineering (ICDE). IEEE. 2024, pp. 3297–3310.   
[4] Minbo Ma, Jilin Hu, Christian S Jensen, Fei Teng, Peng Han, Zhiqiang Xu, and Tianrui Li. “Learning time-aware graph structures for spatially correlated time series forecasting”. In: 2024 IEEE 40th International Conference on Data Engineering (ICDE). IEEE. 2024, pp. 4435–4448.   
[5] Johes Bater, Gregory Elliott, Craig Eggen, Satyender Goel, Abel Kho, and Jennie Rogers. “SMCQL: Secure querying for federated databases”. In: arXiv preprint arXiv:1606.06808 (2016).   
[6] Zhen Wang, Weirui Kuang, Yuexiang Xie, Liuyi Yao, Yaliang Li, Bolin Ding, and Jingren Zhou. “Federatedscope-gnn: Towards a unified, comprehensive and efficient package for federated graph learning”. In: Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 2022, pp. 4110–4120.   
[7] Qiying Pan and Yifei Zhu. “FedWalk: Communication Efficient Federated Unsupervised Node Embedding with Differential Privacy”. In: Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. KDD ’22. Washington DC, USA: Association for Computing Machinery, 2022, pp. 1317–1326.   
[8] Zhuoning Guo, Duanyi Yao, Qiang Yang, and Hao Liu. “HiFGL: A Hierarchical Framework for Cross-silo Cross-device Federated Graph Learning”. In: Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. KDD ’24. Barcelona, Spain: Association for Computing Machinery, 2024, pp. 968–979.   
[9] General Data Protection Regulation GDPR. “General data protection regulation”. In: Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (2016).   
[10] Preston Bukaty. The california consumer privacy act (ccpa): An implementation guide. IT Governance Ltd, 2019.   
[11] Zhen Qin, Shuiguang Deng, Mingyu Zhao, and Xueqiang Yan. “FedAPEN: Personalized Cross-silo Federated Learning with Adaptability to Statistical Heterogeneity”. In: Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. KDD ’23. Long Beach, CA, USA: Association for Computing Machinery, 2023, pp. 1954–1964. ISBN: 9798400701030.   
[12] Yue Tan, Yixin Liu, Guodong Long, Jing Jiang, Qinghua Lu, and Chengqi Zhang. “Federated learning on non-iid graphs via structural knowledge sharing”. In: Proceedings of the AAAI conference on artificial intelligence. Vol. 37. 8. 2023, pp. 9953–9961.   
[13] Han Xie, Jing Ma, Li Xiong, and Carl Yang. “Federated Graph Classification over Non-IID Graphs”. In: Advances in Neural Information Processing Systems. Ed. by M. Ranzato, A. Beygelzimer, Y. Dauphin, P.S. Liang, and J. Wortman Vaughan. Curran Associates, Inc., 2021.   
[14] Jinheon Baek, Wonyong Jeong, Jiongdao Jin, Jaehong Yoon, and Sung Ju Hwang. “Personalized subgraph federated learning”. In: International conference on machine learning. PMLR. 2023, pp. 1396–1415.   
[15] Xunkai Li, Zhengyu Wu, Wentao Zhang, Henan Sun, Ronghua Li, and Guoren Wang. “AdaFGL: A New Paradigm for Federated Node Classification with Topology Heterogeneity”. In: 2024 IEEE 40th International Conference on Data Engineering (ICDE) (2024).   
[16] Wenke Huang, Guancheng Wan, Mang Ye, and Bo Du. “Federated graph semantic and structural learning”. In: Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence. 2023.   
[17] Han Xie, Li Xiong, and Carl Yang. “Federated Node Classification over Graphs with Latent Link-type Heterogeneity”. In: Proceedings of the ACM Web Conference 2023. WWW ’23. Austin, TX, USA, 2023.

[18] Ke Zhang, Carl Yang, Xiaoxiao Li, Lichao Sun, and Siu Ming Yiu. “Subgraph Federated Learning with Missing Neighbor Generation”. In: Advances in Neural Information Processing Systems. Ed. by M. Ranzato, A. Beygelzimer, Y. Dauphin, P.S. Liang, and J. Wortman Vaughan. Vol. 34. Curran Associates, Inc., 2021, pp. 6671–6682.   
[19] Xingbo Fu, Zihan Chen, Binchi Zhang, Chen Chen, and Jundong Li. “Federated graph learning with structure proxy alignment”. In: Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 2024, pp. 827–838.   
[20] Xunkai Li, Zhengyu Wu, Wentao Zhang, Yinlin Zhu, Rong-Hua Li, and Guoren Wang. “FedGTA: Topology-Aware Averaging for Federated Graph Learning”. In: Proceedings of the VLDB Endowment 17.1 (2023), pp. 41–50.   
[21] Yinlin Zhu, Xunkai Li, Zhengyu Wu, Di Wu, Miao Hu, and Rong-Hua Li. “FedTAD: Topology-aware Data-free Knowledge Distillation for Subgraph Federated Learning”. In: Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI-24. Ed. by Kate Larson. Main Track. International Joint Conferences on Artificial Intelligence Organization, Aug. 2024, pp. 5716–5724.   
[22] Yige Liu, Yiwei Lou, Yang Liu, Yongzhi Cao, and Hanpin Wang. “Label leakage in vertical federated learning: A survey”. In: Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence. 2024, pp. 8160–8169.   
[23] Pengyu Qiu, Xuhong Zhang, Shouling Ji, Tianyu Du, Yuwen Pu, Jun Zhou, and Ting Wang. “Your labels are selling you out: Relation leaks in vertical federated learning”. In: IEEE Transactions on Dependable and Secure Computing 20.5 (2022), pp. 3653–3668.   
[24] Simon Kornblith, Mohammad Norouzi, Honglak Lee, and Geoffrey Hinton. “Similarity of neural network representations revisited”. In: International conference on machine learning. PMLR. 2019.   
[25] J. Lin. “Divergence measures based on the Shannon entropy”. In: IEEE Transactions on Information Theory (1991).   
[26] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. “Communication-efficient learning of deep networks from decentralized data”. In: Artificial intelligence and statistics. PMLR. 2017, pp. 1273–1282.   
[27] Chaoyi Chen, Dechao Gao, Yanfeng Zhang, Qiange Wang, Zhenbo Fu, Xuecang Zhang, Junhua Zhu, Yu Gu, and Ge Yu. “NeutronStream: A Dynamic GNN Training Framework with Sliding Window for Graph Streams”. In: Proc. VLDB Endow. (2023).   
[28] Xunkai Li, Meihao Liao, Zhengyu Wu, Daohan Su, Wentao Zhang, Rong-Hua Li, and Guoren Wang. “LightDiC: A Simple Yet Effective Approach for Large-Scale Digraph Representation Learning”. In: Proceedings of the VLDB Endowment 17.7 (2024), pp. 1542–1551.   
[29] Henan Sun, Xunkai Li, Zhengyu Wu, Daohan Su, Rong-Hua Li, and Guoren Wang. “Breaking the Entanglement of Homophily and Heterophily in Semi-supervised Node Classification”. In: 2024 IEEE 40th International Conference on Data Engineering (ICDE). IEEE Computer Society. 2024, pp. 2379–2392.   
[30] Nian Liu, Xiao Wang, Lingfei Wu, Yu Chen, Xiaojie Guo, and Chuan Shi. “Compact graph structure learning via mutual information compression”. In: Proceedings of the ACM web conference 2022. 2022.   
[31] Hui Xu, Liyao Xiang, Femke Huang, Yuting Weng, Ruijie Xu, Xinbing Wang, and Chenghu Zhou. “Grace: Graph self-distillation and completion to mitigate degree-related biases”. In: Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 2023, pp. 2813–2824.   
[32] Aditya Grover and Jure Leskovec. “node2vec: Scalable feature learning for networks”. In: Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining. 2016.   
[33] Wen-Zhi Li, Chang-Dong Wang, Hui Xiong, and Jian-Huang Lai. “Homogcl: Rethinking homophily in graph contrastive learning”. In: Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 2023, pp. 1341–1352.   
[34] Jiong Zhu, Yujun Yan, Lingxiao Zhao, Mark Heimann, Leman Akoglu, and Danai Koutra. “Beyond homophily in graph neural networks: Current limitations and effective designs”. In: Advances in neural information processing systems 33 (2020), pp. 7793–7804.   
[35] Qiying Pan, Yifei Zhu, and Lingyang Chu. “Lumos: Heterogeneityaware federated graph learning over decentralized devices”. In: 2023 IEEE 39th International Conference on Data Engineering (ICDE). IEEE. 2023, pp. 1914–1926.

[36] Sujoy Bag, Sri Krishna Kumar, and Manoj Kumar Tiwari. “An efficient recommendation generation using relevant Jaccard similarity”. In: Information Sciences 483 (2019), pp. 53–64.   
[37] Jiaxin Bai, Yicheng Wang, Tianshi Zheng, Yue Guo, Xin Liu, and Yangqiu Song. “Advancing Abductive Reasoning in Knowledge Graphs through Complex Logical Hypothesis Generation”. In: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). Ed. by Lun-Wei Ku, Andre Martins, and Vivek Srikumar. Bangkok, Thailand: Association for Computational Linguistics, Aug. 2024.   
[38] Suphakit Niwattanakul, Jatsada Singthongchai, Ekkachai Naenudorn, and Supachanun Wanapu. “Using of Jaccard coefficient for keywords similarity”. In: Proceedings of the international multiconference of engineers and computer scientists. Vol. 1. 6. 2013, pp. 380–384.   
[39] Komang Rinartha and Wayan Suryasa. “Comparative study for better result on query suggestion of article searching with MySQL pattern matching and Jaccard similarity”. In: 2017 5th International Conference on Cyber and IT Service Management (CITSM). IEEE. 2017.   
[40] Thomas N. Kipf and Max Welling. “Semi-Supervised Classification with Graph Convolutional Networks”. In: 5th International Conference on Learning Representations, ICLR 2017, Toulon, France, April 24-26, 2017, Conference Track Proceedings. OpenReview.net, 2017.   
[41] Vijay Prakash Dwivedi, Anh Tuan Luu, Thomas Laurent, Yoshua Bengio, and Xavier Bresson. “Graph Neural Networks with Learnable Structural and Positional Representations”. In: International Conference on Learning Representations. 2022.   
[42] Wonyong Jeong and Sung Ju Hwang. “Factorized-fl: Personalized federated learning with parameter factorization & similarity matching”. In: Advances in Neural Information Processing Systems 35 (2022).   
[43] Jaehong Yoon, Wonyong Jeong, Giwoong Lee, Eunho Yang, and Sung Ju Hwang. “Federated continual learning with weighted inter-client transfer”. In: International Conference on Machine Learning. PMLR. 2021, pp. 12073–12086.   
[44] Manoj Ghuhan Arivazhagan, Vinay Aggarwal, Aaditya Kumar Singh, and Sunav Choudhary. “Federated learning with personalization layers”. In: arXiv preprint arXiv:1912.00818 (2019).   
[45] Yanqiao Zhu, Yichen Xu, Feng Yu, Qiang Liu, Shu Wu, and Liang Wang. “Graph contrastive learning with adaptive augmentation”. In: Proceedings of the web conference 2021. 2021, pp. 2069–2080.   
[46] Dongsheng Luo, Wei Cheng, Wenchao Yu, Bo Zong, Jingchao Ni, Haifeng Chen, and Xiang Zhang. “Learning to Drop: Robust Graph Neural Network via Topological Denoising”. In: Proceedings of the 14th ACM International Conference on Web Search and Data Mining. WSDM ’21. 2021, pp. 779–787.   
[47] Tong Zhao, Yozen Liu, Leonardo Neves, Oliver Woodford, Meng Jiang, and Neil Shah. “Data augmentation for graph neural networks”. In: Proceedings of the aaai conference on artificial intelligence. 2021.   
[48] Xingbo Fu, Binchi Zhang, Yushun Dong, Chen Chen, and Jundong Li. “Federated graph machine learning: A survey of concepts, techniques, and applications”. In: ACM SIGKDD Explorations Newsletter 24.2 (2022), pp. 32–47.   
[49] U Kang, Mary McGlohon, Leman Akoglu, and Christos Faloutsos. “Patterns on the connected components of terabyte-scale graphs”. In: 2010 IEEE International Conference on Data Mining. IEEE. 2010.   
[50] Vibhor Rastogi, Ashwin Machanavajjhala, Laukik Chitnis, and Anish Das Sarma. “Finding connected components in map-reduce in logarithmic rounds”. In: 2013 IEEE 29th International Conference on Data Engineering (ICDE). 2013, pp. 50–61.   
[51] Pengxiang Wu, Songzhu Zheng, Mayank Goswami, Dimitris Metaxas, and Chao Chen. “A topological filter for learning with label noise”. In: Advances in neural information processing systems 33 (2020).   
[52] Zhilin Yang, William Cohen, and Ruslan Salakhudinov. “Revisiting semi-supervised learning with graph embeddings”. In: International conference on machine learning. PMLR. 2016, pp. 40–48.   
[53] Oleksandr Shchur, Maximilian Mumme, Aleksandar Bojchevski, and Stephan Gunnemann. “Pitfalls of graph neural network evaluation”. In: ¨ arXiv preprint arXiv:1811.05868 (2018).   
[54] Derek Lim, Felix Hohne, Xiuyu Li, Sijia Linda Huang, Vaishnavi Gupta, Omkar Bhalerao, and Ser Nam Lim. “Large scale learning on non-homophilous graphs: New benchmarks and strong simple methods”. In: Advances in neural information processing systems 34 (2021), pp. 20887–20902.   
[55] Weihua Hu, Matthias Fey, Marinka Zitnik, Yuxiao Dong, Hongyu Ren, Bowen Liu, Michele Catasta, and Jure Leskovec. “Open graph

benchmark: Datasets for machine learning on graphs”. In: Advances in neural information processing systems 33 (2020), pp. 22118–22133.   
[56] Xunkai Li, Yinlin Zhu, Boyang Pang, Guochen Yan, Yeyu Yan, Zening Li, Zhengyu Wu, Wentao Zhang, Rong-Hua Li, and Guoren Wang. “Openfgl: A comprehensive benchmarks for federated graph learning”. In: Proceedings of the VLDB Endowment (2025).   
[57] George Karypis. “METIS: Unstructured graph partitioning and sparse matrix ordering system”. In: Technical report (1997).   
[58] Kun Guo, Yutong Fang, Qingqing Huang, Yuting Liang, Ziyao Zhang, Wenyu He, Liu Yang, Kai Chen, Ximeng Liu, and Wenzhong Guo. “Globally Consistent Federated Graph Autoencoder for Non-IID Graphs.” In: IJCAI. 2023, pp. 3768–3776.   
[59] Tian Li, Anit Kumar Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, and Virginia Smith. “Federated optimization in heterogeneous networks”. In: Proceedings of Machine learning and systems 2 (2020).   
[60] Wentao Zhang, Ziqi Yin, Zeang Sheng, Yang Li, Wen Ouyang, Xiaosen Li, Yangyu Tao, Zhi Yang, and Bin Cui. “Graph attention multi-layer perceptron”. In: Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 2022, pp. 4560–4570.   
[61] Diederik P Kingma and Jimmy Ba. “Adam: A method for stochastic optimization”. In: arXiv preprint arXiv:1412.6980 (2014).   
[62] Wei Jin, Xiaorui Liu, Xiangyu Zhao, Yao Ma, Neil Shah, and Jiliang Tang. “Automated Self-Supervised Learning for Graphs”. In: International Conference on Learning Representations. 2022.   
[63] Guancheng Wan, Wenke Huang, and Mang Ye. “Federated graph learning under domain shift with generalizable prototypes”. In: Proceedings of the AAAI Conference on Artificial Intelligence. 2024.   
[64] Baiqi Li, Yedi Ma, Yufei Liu, Hongyan Gu, Zhenghan Chen, and Xinli Huang. “Federated Learning on Distributed Graphs Considering Multiple Heterogeneities”. In: ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE. 2024, pp. 5140–5144.   
[65] Wenchao Yu, Wei Cheng, Charu C Aggarwal, Kai Zhang, Haifeng Chen, and Wei Wang. “Netwalk: A flexible deep embedding approach for anomaly detection in dynamic networks”. In: Proceedings of the 24th ACM SIGKDD international conference on knowledge discovery & data mining. 2018, pp. 2672–2681.   
[66] Rakshit Trivedi, Mehrdad Farajtabar, Prasenjeet Biswal, and Hongyuan Zha. “Dyrep: Learning representations over dynamic graphs”. In: International conference on learning representations. 2019.   
[67] Giang Hoang Nguyen, John Boaz Lee, Ryan A Rossi, Nesreen K Ahmed, Eunyee Koh, and Sungchul Kim. “Continuous-time dynamic network embeddings”. In: Companion proceedings of the the web conference 2018. 2018, pp. 969–976.