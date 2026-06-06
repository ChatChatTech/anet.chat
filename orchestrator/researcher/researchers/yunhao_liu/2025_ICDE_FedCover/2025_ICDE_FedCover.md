# FedEcover: Fast and Stable Converging Model-Heterogeneous Federated Learning with Efficient-Coverage Submodel Extraction

Juntao Liang1, Lan Zhang12, Xiangmou Qu3, Jun Wang4 1University of Science and Technology of China, Hefei, China 2Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, China 3Chongqing University, Chongqing, China 4University of Luxembourg, Luxembourg junliang@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, lokinko.cs@gmail.com, junwang.lu@gmail.com

Abstract—Federated learning (FL) has achieved favorable progress in addressing the data silo problem without compromising clients’ data privacy. In real-world scenarios, there are numerous low-capacity clients, i.e., devices with limited resources like computational power, storage and bandwidth, holding unique and valuable data. Yet the conventional model-homogeneous paradigm is unsuitable due to its uniform model demands on all clients. To effectively utilize the data from clients of various capacities for learning a well-performing global model, researchers have proposed submodel extraction-based partial training methods allowing clients to locally train heterogeneous submodels of different sizes. However, existing partial training methods are inadequate in terms of parameter space coverage efficiency and convergence stability, which adversely affects convergence rate and the final performance. In this work, we introduce FedEcover, a model-heterogeneous framework to learn a fast and stable converging global model in challenging scenarios with dual heterogeneity of data and client capacity. Specifically, our framework incorporates an efficient submodel extraction scheme applying a random sampling without replacement strategy and a step-size decay mechanism in the global aggregation process, to enable the global model fully leveraging the heterogeneous data distributed across capacity-heterogeneous clients. Experimental results on multiple models and datasets demonstrate that our framework outperforms existing submodel extraction-based partial training methods and model-homogeneous FedAvg in both convergence rate and converged performance of the global model.

Index Terms—federated learning, data heterogeneity, model heterogeneity, submodel extraction, convergence stability

# I. INTRODUCTION

Federated Learning (FL) [1] has emerged as a promising distributed machine learning paradigm that enables collaborative model training leveraging decentralized data while preserving data privacy. This framework facilitates the joint training of a shared global model through iterative parameter aggregation on a central server, where participating clients retain their private local datasets and only exchange model updates rather than raw data. The foundational modelhomogeneous paradigm, as exemplified by Federated Averaging (FedAvg) [1] and following works [2]–[6], assumes a uniform model architecture across all clients and the central server to enable parameter fusion through weighted averaging mechanisms. However, in real-world scenarios, there are numerous low-capacity clients [7], i.e., devices with limited computational capacity, memory constraints, and restricted bandwidth, etc. These clients often possess unique, nonredundant data distributions that are both non-independent and non-identically distributed (Non-IID) [8], [9], thus equally valuable for constructing comprehensive global models that capture real-world complexity [10]. The conventional modelhomogeneous approach imposes uniform model architectural requirements that frequently exceed the capabilities of lowcapacity participants. While downscaling the global model to accommodate resource-constrained clients offers a temporary solution, this strategy fundamentally compromises the theoretical maximum representational capacity of the federated system, thereby limiting its ability to learn complex patterns across heterogeneous data sources.

To effectively utilize the unique data from clients with varying capacities without compromising global models’ expressiveness, model-heterogeneous FL has emerged as a viable paradigm. Current model-heterogeneous solutions predominantly adopt two methodological branches: (a) knowledge sharing-based methods that transfer knowledge vectors across architecture-heterogeneous clients, and (b) submodel extraction-based methods enabling partial model training. Local models can thus be either custom-designed or adaptively derived from the global model through neural architecture operations, allowing dynamic adjustment of model footprints (encompassing computational, memory, and communication requirements) to align with individual device constraints.

While both approaches aim to address client capacity heterogeneity, they suffer from critical limitations that hinder practical deployment and global model performance. Knowledge sharing-based methods face practical constraints: they either depend on unrealistic assumptions about public/generated datasets or overemphasize local model enhancement compromising building high-performance global models, which is a primary objective in applications where large enterprises or institutions aim at learning a large global model for public services while maintaining users’ data privacy. Submodel-based methods, though compatible with the weighted averaging parameter aggregation mechanism, suffer from three fundamental flaws in practical scenarios: (a) suboptimal parameter space exploration due to static or non-optimal submodel selection strategies, limiting global model convergence rate and final performance; (b) neglect of structural consistency in modern architectures like residual [11] networks, where arbitrary submodel extraction disrupts critical feature propagation paths; (c) convergence instability under dual heterogeneity (involving both data distribution skew and model parameter variance) and even with partial client participation, rendering existing aggregation mechanisms ineffective.

To bridge these gaps, we propose FedEcover–a novel partial training framework featuring two core technical contributions from perspective of submodel extraction and parameter fusion respectively: (a) efficient submodel sampling with coverageaware and structure-aware randomization, ensuring comprehensive parameter space exploration as well as submodel diversity while maintaining device-specific capacity constraints; (b) aggregation with decaying step-size, specifically designed to stabilize convergence under dual heterogeneity. Specifically, to achieve both parameter space coverage efficiency and submodel diversity, which are essential for promoting convergence rate and final performance, we introduce replacement-free random sampling in submodel extraction. Furthermore, to address the convergence instability issue induced by dual heterogeneity as well as achieve fast convergence, we adopt an aggregation step-size decay mechanism that is not considered in existing submodel-based partial training works. Empirical validation through comprehensive experiments across multiple model architectures and datasets demonstrates FedEcover’s superiority over other existing partial training approaches and model-homogeneous baselines in both convergence and final accuracy performance.

Our main contributions in this work are summarized as follows:

• We propose a novel submodel extraction scheme that achieves high parameter space coverage efficiency and submodel diversity through random sampling without replacement, promoting convergence rate and final performance of the global model in scenarios with data heterogeneity and model heterogeneity.   
• We introduce a global aggregation step-size decay mechanism, validating its effectiveness on both data heterogeneity and model heterogeneity, overcoming the poor convergence stability issue exposed by all existing submodel extraction-based partial training methods.   
• We design a model-heterogeneous FL framework incorporating efficient submodel extraction and step-size decaying parameter aggregation, enabling fast and stable converging global model learning with heterogeneous data on capacity-heterogeneous clients. Thorough experimental evaluations show that our framework outperforms existing submodel extraction-based partial training methods and model-homogeneous FedAvg in both convergence rate and accuracy performance.

# II. RELATED WORK

A. Model-heterogeneous Federated Learning based on Knowledge Sharing

Existing approaches for model-heterogeneous FL through knowledge sharing can be categorized based on their knowledge transfer mechanisms. Public data-dependent methods like FedMD [12], FedDF [13], FedHKT [14] and FedAgg [15] employ knowledge distillation (KD) [16] on public datasets to align heterogeneous models. Nevertheless, their reliance on globally accessible data is impractical due to high-quality public data scarcity in real-world scenarios and that data synthesis on clients is costly and unrealistic because it relies on high-quality client models, which are not available at the start, while introduces privacy vulnerabilities. Representation learning methods like LG-FedAvg [17] and FedGH [18] adopt partial model sharing by splitting networks into local-private and global-shared components. However, their fixed architecture partitioning creates imbalanced representation learning between components. FedProto [19] and FedTGP [20] advance this by sharing only class prototypes, but their prototype alignment remain vulnerable to client-drift due to biased local updates under data heterogeneity. FedKTL [21] establishes a one-way knowledge pipeline from cloudbased generators to client models. This overlooks the bidirectional knowledge potential where client-specific insights could enhance global model capabilities through reciprocal learning. Our approach explicitly addresses these limitations by eliminating public/synthetic data dependencies through parameter aggregation mechanism. This also maintains efficient and privacy-preserving, for parameter containing more (while non-sensitive) information than representations (along with labels, which might be sensitive), as well as enabling bidirectional knowledge flow through collaborative client-server interactions.

B. Model-heterogeneous Federated Learning based on Submodel Extraction

Submodel extraction-based partial training methods suggest extracting smaller submodels for clients to train on their local data but face key challenges. (a) Structural constraints: the embedding matrix row extraction scheme proposed by Secure Federated Submodel Learning [22] is generality-limited beyond recommendation systems. DC-CCL [23] enforces tight cloud-device model coupling, preventing independent inference as neither submodel can function autonomously. (b) Training incompleteness and unevenness: HeteroFL [24] and FjORD [25] employ static submodel extraction, permanently excluding portions of the global parameter space from training on particular clients–a critical limitation for non-IID data where full parameter utilization is essential. While Federated Dropout [26] introduces randomness through neural unit sampling, its nonstrategic randomness cause uneven parameter training frequency. FedRolex [27] tries tp improve coverage through rolling window selection but suffers from rigid stepsize constraints that limit adaptive submodel expansion. (c)

Convergence limitations: As demonstrated by Zhou et al. [28], submodel diversity directly impacts convergence speed– a factor overlooked by existing methods that prioritize hardware constraints over training dynamics. Iterative pruning approaches [29], [30] focus on searching for ”lottery tickets” [31] models in parameter space but fail to optimize collaboratively learning with individual models on distributed data. Our framework focus on general functionally-dependent submodel extraction technique and innovates by introducing coverageaware, diversity-aware and structure-aware submodel sampling that maximizes parameter space utilization while incorporating step-size decaying aggregation to promote convergence speed as well as stability.

# III. PROBLEM FORMALIZATION

FL involves a server and a set of clients to jointly train a global model without exposing and sharing clients’ own data. Let P denotes the set of total N clients with local datasets $\mathcal { D } =$ $\{ \mathcal { D } _ { 1 } , \mathcal { D } _ { 2 } , \cdot \cdot \cdot , \mathcal { D } _ { N } \}$ . FL trains a global model with parameter space $\theta _ { g }$ by conducting clients’ local training and on-cloud aggregation alternately. The global objective can be viewed as:

$$
\min _ {\theta_ {g}} \mathcal {L} (\theta_ {g}, \mathcal {D}) \tag {1}
$$

where $\mathcal { L }$ is the loss function of a specific task.

Denote the global model parameters and client $i \gamma _ { \mathrm { s } }$ local model parameters in round t by $\theta _ { g } ^ { ( t ) }$ and θ(t) $\theta _ { i } ^ { ( t ) }$ respectively. Let $\mathcal { P } ^ { ( t ) }$ represent the set of clients participating in federated training in round t. It can either be the full set or a subset of all clients depending on different scenarios, i.e., $\mathcal { P } ^ { ( t ) } \subseteq \mathcal { P }$ . In model-heterogeneous FL (we consider submodel-based methods and aim at learning an effective global model utilizing heterogeneous data distributed on capacity-heterogeneous clients in this work), clients train submodels of different sizes according to their own capacities. We consider a global model architecture $\mathcal { M } _ { g }$ with L hidden layers, where layer $l \in \{ 1 , \cdots , L \}$ contains $n _ { g , l }$ neurons.

Definition 1 (Client Capacity Profile). For client $i \in \mathcal P$ , we formalize its computational capacity as a normalized constraint coefficient $c _ { i } \in ( 0 , 1 ]$ , reflecting the maximum proportion of neurons it can maintain per hidden layer relative to $\mathcal { M } _ { g }$ . This coefficient synthesizes multiple resource dimensions:

$$
c _ {i} := \min (\frac {R _ {i} ^ {c o m p}}{R _ {g} ^ {c o m p}}, \frac {R _ {i} ^ {m e m}}{R _ {g} ^ {m e m}}, \frac {R _ {i} ^ {c o m m}}{R _ {g} ^ {c o m m}}, \frac {R _ {i} ^ {o t h e r}}{R _ {g} ^ {o t h e r}})
$$

where $R _ { i } ^ { \{ c o m p , m e m , c o m m , o t h e r \} }$ denote client i’s available compute cycles, memeory, communication bandwidth, and other factors, respectively, with $R _ { g } ^ { \{ \cdot \} }$ representing the corresponding resource demands of the full global model.

At the start of round t, client i’s local model $\theta _ { i } ^ { ( t ) }$ is instantiated via a capacity-aware neuron sampling:

$$
\theta_ {i} ^ {(t)} \leftarrow \bigcup_ {l = 1} ^ {L} \{\mathbf {W} _ {g, l} ^ {(t)} [ S _ {i, l}, S _ {i, l - 1} ] | S _ {i, l} \subset \{1, \dots , n _ {g, l} \} \} \tag {2}
$$

where $S _ { i , l }$ denotes the index set of extracted neurons in layer l and satisfies $| S _ { i , l } | = \frac { \bf \epsilon } { \bf \epsilon } | c _ { i } n _ { g , l } { \bf j . \partial W } _ { g , l } ^ { ( t ) }$ g,l represents the global weight matrix. The extraction maintains layer-wise connectivity: $S _ { i , l - 1 }$ determines the input features for layer l. The generation of index set $S _ { i , l }$ and the overall submodel extraction process is abstracted into a subroutine:

$$
\theta_ {i} ^ {(t)} \leftarrow \text { SubmodelExtraction } (\theta_ {g} ^ {(t)}, c _ {i}) \tag {3}
$$

Then participating clients train their submodels in parallel with their own private data as follows:

$$
\theta_ {i} ^ {(t)} \leftarrow \theta_ {i} ^ {(t)} - \eta_ {i} \nabla \mathcal {L} (\theta_ {i} ^ {(t)}, \mathcal {B} _ {i, k}), \text {   for   } k = 1, 2, \dots , K _ {i} \tag {4}
$$

where $\eta _ { i }$ is the local learning rate, $\boldsymbol { B } _ { i , k }$ is the batch sampled from $\mathcal { D } _ { i }$ at the k-th step of local training, and $K _ { i }$ is the number of local training steps. After local training, client i gets the updated parameter s ˆθ(t $\dot { \hat { \theta } } _ { i } ^ { ( t ) }$ ). When all selected clients finish local training, they upload their updated parameters to the cloud and the server aggregates them to update the global model.

In conventional model-homogeneous FL, the aggregation process can be viewed as follows:

$$
\theta_ {g} ^ {(t + 1)} = \sum_ {i \in \mathcal {P} ^ {(t)}} p _ {i} \hat {\theta} _ {i} ^ {(t)}, \text {   s.t.   } 0 \leq p _ {i} \leq 1, \sum_ {i \in \mathcal {P} ^ {(t)}} p _ {i} = 1 \tag {5}
$$

where $p _ { i }$ represents the weight of client i in the aggregation process, and there are various weight allocation strategies. In this work, we assume by default that all clients have equal weight. Different from the direct weighted averaging in (5), the aggregation for model-heterogeneous FL is more fine-grained with another subroutine:

$$
\theta_ {g} ^ {(t + 1)} \leftarrow \underset {i \in \mathcal {P} ^ {(t)}} {\text { HeteroAgg }} (\hat {\theta} _ {i} ^ {(t)}) \tag {6}
$$

In particular, our implementations for SubmodelExtraction and HeteroAgg will be illustrated in IV-A and IV-B respectively.

# IV. PROPOSED FRAMEWORK

The effectiveness of submodel training can be validated by the success of conventional dropout technique [32]: with dropout as regularization, a different sub-network is trained at each step and this promotes the generalization and performance of the full model. Our base idea is to train adaptivesize submodels on different clients so that we can leverage decentralized data to optimize the overall global model parameter space. As Fig. 1 shows, for each client, the server extract an adaptive proportion of neurons in each hidden layer, and combine corresponding parameters into a submodel. In this section, we present our model-heterogeneous FL framework named FedEcover, involving two main subroutines, i.e., SubmodelExtraction and HeteroAgg. We will illustrate them in IV-A and IV-B respectively and finally summarize our overall framework in IV-C.

![](images/f34615585e3fe7901b90066d955185ceddd3ca57b5bc7f30ff79f80c3493cd66.jpg)



Fig. 1: An overview of model-heterogeneous FL framework based on submodel extraction. Local models of different sizes are submodels extracted layer by layer from the global model.

# A. Coverage-aware and Structure-aware Submodel Extraction

1) Coverage-aware Randomization: For submodel training, we have three significant objectives: (a) comprehensive exploration of the global parameter space, i.e., broader coverage of the global parameter space and more frequent updates to specific parameters can contribute positively to the convergence of the global model; (b) coordinated parameter updates through distributed collaboration, i.e., different parts of the global parameter space should be evenly trained by each client as much as possible, so that the overall global parameters can better fit the local data of each client; and (c) submodel diversity, i.e., diverse combinations of different neurons, is encouraged for its regularizing effects similar as model ensemble.

Based on a comprehensive consideration of the aforementioned aspects, we propose a novel coverage-aware submodel extraction scheme illustrated in Fig. 2. Particularly, FedEcover maintains a buffer of unused neurons’ (e.g., features for linear layer, channels for convolution layer, etc) indices for each layer of the global model on the cloud server. Denote layer buffers for a global model having L layers by $B = \{ B _ { 1 } , B _ { 2 } , \cdot \cdot \cdot , B _ { L } \}$ , where $B _ { l }$ represents the buffer of layer l, tracking available neurons’ indices of layer l. At the start of each round, for each client in sequence, the server randomly selects a certain proportion (according to the client’s capacity) of neuron indices from the unused ones remained in the buffer, layer by layer. After each selection, the selected neuron indices are removed from the buffer. A buffer would be refilled when exhausted so this process of random sampling without replacement keeps going. For each layer, the selected neuron indices are used to extract corresponding parameter elements, which are combined as a smaller parameter matrix to become a layer for the submodel. In implementation, for the weight parameter, we extract input indices corresponding to the previous layer’s selected neuron indices and output indices corresponding to the current layer’s selected neuron indices. And for the bias parameter, we extract elements corresponding to the current layer’s selected neuron indices. Detailed steps of SubmodelExtraction are illustrated in Algorithm 1. This scheme guarantees uniform parameter coverage–each neuron participates in training before reuse while maintains strict adherence to $c _ { i }$ constraints, and explore the global parameter space with diverse submodel through stochastic sampling.

![](images/61c320e6d1ab60ff793cb535201681cd160b90139cc31b04ef1ac04e6a88f0c8.jpg)



Fig. 2: Submodel extraction for one layer in FedEcover. (a) At round j, a high-capacity client $i _ { j , 1 }$ randomly choose four neurons first, then a low-capacity client $i _ { j , 2 }$ choose two neurons left in the buffer; (b) at round $j + 1$ , the buffer is refilled first. Then two low-capacity clients sample nonoverlapping neurons in the buffer; (c) at round $j + 2 ,$ one highcapacity client $i _ { j + 2 , 1 }$ first choose the two neurons remained in the buffer. After the buffer is refilled, client $i _ { j + 2 , 1 }$ continue sampling two more needed neurons from the newly refilled ones, non-overlapping with the already chosen neurons a, b. Then one low-capacity client $i _ { j + 2 , 2 }$ randomly choose two neurons from those remained in the buffer.

2) Structural Consistency Preservation: Residual connections constitute essential computation pathways for modern architectures (e.g., in ResNet [11], Transformer [33]). However, prior submodel extraction research [24]–[27] as well as related analysis built on them [28], [30], [34], [35] did not give comprehensive consideration on the impact of residual connection to the submodel extraction procedure. Let ${ \mathcal { F } } _ { l } ( x )$ denote layer l’s transformation in a residual block, and the original desired mapping is:

Algorithm 1 SubmodelExtraction   
Input: global model $\theta_{g}$ , client capacity $c_{i}$ , buffer $B = \{B_{1}, \cdots, B_{L}\}$ Output: submodel $\theta_{i}$ , submodel unit indices $S_{i}$ , updated buffer $\hat{B}$ 1: for $l = 1, 2, \cdots, L$ do

2: $n_{i,l} = c_{i} \cdot n_{g,l}$ 3: $S_{i,l} = \emptyset$ 4: if layer l has no residual connection with a former layer then

5: if $|B_{l}| < n_{i,l}$ then

6: $S_{i,l} = B_{l}$ 7: Refill the buffer $B_{l}$ with $n_{g,l}$ indices

8: end if

9: Randomly select $n_{i,l} - |S_{i,l}|$ indices from $B_{l} - S_{i,l}$ and add them to $S_{i,l}$ 10: else

11: Find the former layer f of residual connection

12: $S_{i,l} \leftarrow S_{i,f}$ 13: end if

14: $\hat{B}_{l} \leftarrow B_{l} - S_{i,l}$ 15: end for

16: Extract corresponding parameter elements according to $S_{i} = \{S_{i,1}, S_{i,2}, \cdots, S_{i,L}\}$ and construct a submodel $\theta_{i}$ with extracted elements layer by layer

17: return $\theta_{i}, S_{i} = \{S_{i,1}, \cdots, S_{i,L}\}, \hat{B} = \{\hat{B}_{1}, \cdots, \hat{B}_{L}\}$

$$
\mathcal {H} _ {l} (x) = \mathcal {F} _ {l} (x) + x \tag {7}
$$

As showed in Fig. 3a-b, static and rolling schemes maintain the consistency because of their naturally aligned design. But for the original design of naive random scheme in Federated Dropout [26], the arbitrary index selection $( S _ { i , l } ~ \neq ~ S _ { i , l - 1 } )$ catastrophically disrupts the element-wise addition in (7). This creates parameter-level semantic mismatch during aggregation, ultimately corrupting model semantics. For example, in Fig. 3c, one submodel trains residual connections: $\{ b 1 + a 3 , d 1 + b 3 , f 1 + e 3 \}$ on local data but the actual residual connections aggregated on the server is $\{ a 1 + a 3 , b 1 +$ $b 3 , \cdot \cdot \cdot , f 1 { + } f 3 \}$ , which is not aligned with the locally trained ones. This causes invalid training, i.e., the performance of the global model obtained through such aggregation does not improve with rounds, because the semantics of the aggregated parameters are incorrect. Simply but effectively, FedEcover solves this by enforcing structural consistency constraints with:

$$
S _ {i, l} = S _ {i, f} \forall \text { residual - connected   layers } l, f \tag {8}
$$

as visualized in Fig. 3d. This structural awareness maintains submodel training semantic correctness.

3) Scaling Module: The number of neurons in each hidden layer of a submodel is only a proportion of that of the global model. This may cause deviation in numerical magnitude. Following established practices [24], [27], for a client with

![](images/b3156660deba5eb85b2fc1f3e8a07bf1e43eb3e3ccdb6bb2147ce05906c2b2c3.jpg)



Fig. 3: Illustration of residual connection consistency of existing submodel extraction schemes.

capacity $c _ { i } .$ , we add a scaling module after each hidden layer, numerically amplifying the output of each hidden layer to $\frac { 1 } { c _ { i } }$ times its original value.

# B. Sparse Aggregation with Global Step-size Decay

Building on prior sparse aggregation frameworks [24], [26]– [28], we formulate parameter updates through client-specific submodel participation. For each global parameter ${ \bf w } _ { g }$ , its update derives exclusively from clients possessing it in their submodels. Specifically, the value of the global parameter ${ \bf w } _ { g }$ is updated as the average of the corresponding values of the client models that include this parameter in the current round:

$$
\mathbf {w} _ {g} ^ {(t + 1)} = \frac {1}{| \mathcal {P} _ {\mathbf {w} _ {g}} ^ {(t)} |} \cdot \sum_ {i \in \mathcal {P} _ {\mathbf {w} _ {g}} ^ {(t)}} \hat {\mathbf {w}} _ {i} ^ {(t)} \tag {9}
$$

where $\mathcal { P } _ { \mathbf { w } _ { g } } ^ { ( t ) } \subset \mathcal { P } ^ { ( t ) }$ represents the subset of clients having the parameter ${ \bf w } _ { g }$ in their submodels during round t.

While this enables the parameter aggregation of model heterogeneity, it introduces amplified client drift due to two compounding factors–data heterogeneity inherent in FL and structural heterogeneity where parameters receive updates from varying client subsets. In addition to data heterogeneity, submodel heterogeneity also creates non-stationary update distributions. For instance, when only a few clients have the parameter ${ \bf w } _ { g }$ in their submodels due to parameter sampling, the global ${ \bf w } _ { g }$ becomes reliant on the updates from these clients, which may be insufficient or biased, leading to a suboptimal update direction for the global model. This bias can intensify convergence instability and degrade global model performance.

To address this, we introduce a global aggregation stepsize decay (GSD) mechanism, which is not considered in prior partial training methods [24]–[28]. We adapt the aggregation process as:

$$
\theta_ {g} ^ {(t + 1)} = \theta_ {g} ^ {(t)} + \eta_ {g} ^ {(t)} \cdot \sum_ {i \in \mathcal {P} ^ {(t)}} p _ {i} \Delta \hat {\theta} _ {i} ^ {(t)} \tag {10}
$$

Algorithm 2 HeteroAgg   
Input: global model $\theta_{g}$ , a set of client models $\theta = \{\theta_{1}, \cdots\}$ , a set of client submodel neuron indices $S = \{S_{1}, \cdots\}$ , global aggregation step-size $\eta_{g}$ Output: updated global model $\theta_{g}$ 1: for $l = 1, 2, \cdots, L$ do

2: Initialize both parameter numerical value change accumulator $\Delta\theta$ and client weight accumulator W with all zero values

3: for $i = 0, 1, \cdots, |\theta| - 1$ do

4: Add numerical values of parameters change in $\theta_{i} - \theta_{g}$ to corresponding positions of $\Delta\theta$ according to indices in $S_{i,l}$ 5: Add 1 to corresponding positions of W according to indices in $S_{i,l}$ 6: end for

7: end for

8: $\Delta\theta \leftarrow \frac{\Delta\theta}{W} // Normalization$ 9: $\theta_{g} \leftarrow \theta_{g} + \eta_{g} \cdot \Delta\theta$ 10: return $\theta_{g}$

where η(t)g $\eta _ { g } ^ { ( t ) }$ is the global aggregation step-size, determining how aggressively the global model incorporates information from heterogeneous submodels. We extend the conventional aggregation (equivalent to $\eta _ { g } ~ \equiv ~ 1 )$ by introducing timedependent step-size control, providing a mechanism to control the extent to which newly acquired updates from clients influence the global model. By decaying the aggregation step-size with rounds, GSD encourages: (a) in early aggregation stages, the global model quickly incorporates updates from diverse submodels and accelerates knowledge integration with a large step-size, fostering rapid performance improvements; (b) in later stages, when submodel heterogeneity lead to severe client drift, GSD suppresses noise from biased updates caused by sparse parameter participation through reduced $\eta _ { g } .$ , stabilizing the convergence. The aggregation process incorporating $\eta _ { g }$ is contained in Algorithm 2, while the details of GSD are presented in Algorithm 3.

# C. FedEcover

1) Overall Framework: Based on Algorithm 1 and Algorithm 2, we have our overall model-heterogeneous FL framework, depicted in Algorithm 3. In each round, the server applies Algorithm 1 to extract and submodels distribute them to clients according to their device capacities. After participating clients locally train submodels on their decentralized data in parallel, the server applies Algorithm 2 to aggregate parameters from heterogeneous submodels. Before starting the next round, the server applies the global aggregation step-size decay designed for stable convergence.

2) Communication Cost and Privacy Leakage Analysis: Protecting data privacy is one of the main motivations behind FL research, while reducing communication overhead is the original intent behind local multiple-step training algorithms, starting with FedAvg [1]. In our FedEcover framework, layer

Algorithm 3 FedEcover   
Input: client set P, client local datasets $D = \{D_{1}, \cdots, D_{N}\}$ , client capacities $c = \{c_{1}, \cdots, c_{N}\}$ , initial global aggregation step-size $\eta_{g}^{(0)}$ , decay coefficient $\gamma$ , total rounds T, decay stop rounds $T_{ds}$ , decay interval rounds $T_{di}$ Output: Collaboratively learned global model $\theta_{g}^{(T)}$ Server Executes

1: Initialize $\theta_{g}^{(0)}$ , buffer $B^{(0)} = \{B_{1}^{(0)}, B_{2}^{(0)}, \cdots, B_{L}^{(0)}\}$ 2: for round $t = 0, 1, \cdots, T - 1$ do

3: Sample a client subset $\mathcal{P}^{(t)}$ from P

4: for client $i \in \mathcal{P}^{(t)}$ do

5: $\theta_{i}^{(t)}, S_{i}^{(t)}, B^{(t)} \leftarrow \text{SubmodelExtraction}(\theta_{g}^{(t)}, c_{i}, B^{(t)})$ 6: Send $\theta_{i}^{(t)}$ to client i

7: end for

8: for client $i \in \mathcal{P}^{(t)}$ in parallel do

9: $\hat{\theta}_{i}^{(t)} \leftarrow \text{LocalTrain}(\theta_{i}^{(t)}, \mathcal{D}_{i})$ 10: Send $\hat{\theta}_{i}^{(t)}$ to server

11: end for

12: $\hat{\theta}^{(t)} = \{\hat{\theta}_{1}^{(t)}, \cdots, \hat{\theta}_{|\mathcal{P}^{(t)}}^{(t)}\}$ , $S^{(t)} = \{S_{1}^{(t)}, \cdots, S_{|\mathcal{P}^{(t)}}^{(t)}\}$ 13: $\theta_{g}^{(t+1)} \leftarrow \text{HeteroAgg}(\theta_{g}^{(t)}, \hat{\theta}^{(t)}, S^{(t)}, \eta_{g}^{(t)})$ 14: if $t < T_{ds}$ and $t \mod T_{di} = 0$ then

15: $\eta_{g}^{(t+1)} \leftarrow \gamma \cdot \eta_{g}^{(t)} // Global aggregation step-size decay$ 16: end if

17: end for

18: return $\theta_{g}^{(T)}$

buffers are maintained on the cloud and communication overhead is composed solely of submodel parameters transmission (clients’ capacities implicitly encompass their abilities to bear the overhead of parameter transmission); layer buffers and neuron indices for sparse aggregation contain no sensitive information about clients’ local data. Thus our framework does not introduce additional communication cost or components that may lead to data privacy breaches compared to basic FL framework.

# V. COMPARATIVE ANALYSIS

Existing submodel extraction methodologies predominantly adopt three schemes, each presenting distinct limitations when analyzed through the perspectives of parameter space coverage efficiency and collaborative optimization.

Static submodel extraction. Following the implementation in HeteroFL [24] and FjORD [25], this scheme deterministically assigns fixed parameter subspaces to clients based on capacity tiers. Formally, for client i with capacity $c _ { i } ,$ , the neuron indices at layer l remain invariant across rounds:

$$
S _ {i, l} = \left\{k \in \mathbb {N} \mid 0 \leq k <   \left\lfloor c _ {i} \cdot n _ {g, l} \right\rfloor \right\} \tag {11}
$$

This rigid allocation induces structural bias in parameter updates–clients persistently update parameters in subspaces $\{ 0 , 1 , \cdots , \lfloor c _ { i } \cdot n _ { g , l } \rfloor - 1 \}$ , while parameters beyond $\lfloor c _ { i } \cdot n _ { g , l } \rfloor$ remain stagnant for low-capacity clients. In typical FL scenarios dominated by low-capacity devices, this architecture leads to systematic under-optimization of critical model regions.

Rolling submodel extraction. This sequential paradigm employs deterministic sliding windows:

$$
S _ {i, l} ^ {(t)} = \{(t + k) \bmod n _ {g, l} \mid 0 \leq k <   \lfloor c _ {i} \cdot n _ {g, l} \rfloor \} \tag {12}
$$

Theoretically complete coverage requires $\mathcal { O } ( n _ { g , l } )$ rounds– prohibitively expensive for large-scale models. More critically, the fixed sliding step creates artificial parameter coupling, as adjacent neurons are persistently co-selected. This undermines the benefits of submodel diversity, as non-adjacent parameter interactions remain under-explored during training.

Naive random submodel extraction. Pioneered by Federated Dropout [26], this approach employs independent random sampling per layer:

$$
S _ {i, l} \sim \text { Uniform } (\{0,..., n _ {g, l} - 1 \}, \lfloor c _ {i} \cdot n _ {g, l} \rfloor) \tag {13}
$$

While enhancing submodel diversity through combinatorial randomness across layers, the memoryless sampling process suffers from non-uniform coverage frequency–the probability of specific parameters being neglected follows a Bernoulli process, creating coverage frequency gaps that persist across rounds. This violates the ergodic principle essential for global model convergence.

# A. Theoretical Analysis on Coverage Efficiency

FedEcover encourages different clients to train submodels corresponding to different parts of the global parameter space while train all parameters with even frequencies. Considering both perspectives comprehensively, we study parameter space coverage efficiency of our method and compare it with other submodel extraction schemes.

We start with a single layer with n neurons and we sample k neurons per time. We study the expected number of rounds for each neuron to be chosen at least m times. A client with capacity $c _ { i }$ extracts a $c _ { i }$ proportion of neurons. Suppose the expected value of client capacity distribution is c, for a layer with n neurons, the expected extracted number of neurons per sampling (one client corresponds to one sampling) is $k =$ $\overline { { c } } \cdot n$ . Suppose d clients participate per round, then we have the following results:

Static: all neurons getting selected at least m times requires full-capacity clients to be selected at least m times. Suppose the full-capacity clients account for $r _ { f }$ proportion in the system. The expeted number of full-capacity clients per round is d · $r _ { f }$ and it would need expected $\frac { m } { d \cdot r _ { f } }$ d·rf rounds. With $0 < r _ { f } < \bar { c } < 1$ , we have $\begin{array} { r } { { \frac { m } { d \cdot r _ { f } } } > { \frac { m } { d \cdot \bar { c } } } } \end{array}$ d·rf .

Rolling: the rolling window moves forward a fixed step (default to 1) per round and cycles once every n rounds. After completing a full cycle, each neuron is selected $d \cdot n \cdot { \bar { c } }$ times. When m is an integer multiple of $n ,$ , the expected needed number of rounds is $\begin{array} { r } { { \frac { m } { d \cdot n \cdot \overline { { c } } } } \cdot n = { \frac { m } { d \cdot \overline { { c } } } } } \end{array}$ . However, this estimation holds only when m is a multiple of n. When $m \ < \ n$ , the number of selected times for each neuron will be quite uneven because the rolling window has not completed a full cycle.

Naive random: based on Lemma 1, the expected number of sampling times for all neurons to be selected at least m times with a probability no less than q is $\begin{array} { r } { \lambda \cdot \frac { n } { k } \cdot ( m + \ln \frac { n } { 1 - q } ) } \end{array}$ where $1 < \lambda < 2$ . By approximately let $k = \overline { { c } } \cdot n$ , the expected number of rounds is $\begin{array} { r } { { \frac { \lambda } { d \cdot { \overline { { c } } } } } ( m + \ln { \frac { n } { 1 - q } } ) } \end{array}$

FedEcover: the expected number of rounds is m · nd·n·c $\begin{array} { r } { m \cdot \frac { n } { d \cdot n \cdot \overline { { c } } } = } \end{array}$ $\frac { m } { d \cdot \overline { { c } } }$ with no extra assumptions.

The above analysis is based on a single layer but it can directly reflects the coverage efficiency for the global parameter space because these submodel extraction schemes are all performed layer by layer. Our analysis shows that the submodel extraction scheme adopted in FedEcover has the best parameter space coverage efficiency in terms of both order of magnitude and constant terms.

Lemma 1. Given n elements, randomly sample k elements with replacement each time, then the expected number of sampling times required for all elements to be selected at least m times with a probability no less than q is $\begin{array} { r } { \mathcal { O } \big ( \frac { n } { k } \cdot ( m + l n \frac { n } { 1 - q } \big ) \big ) } \end{array}$ .

Proof. Suppose sampling k elements with replacement each time for t times. For each element, t Bernoulli trials [36] with a probability of $\textstyle p = { \frac { k } { n } }$ of getting selected are performed. Let

$$
x _ {i j} = \left\{ \begin{array}{l l} 1, & \text { if   } i \text {-th element get selected in } j \text {-th sampling} \\ 0, & \text { otherwise } \end{array} \right.
$$

Let $X _ { i }$ be the number of times that element i gets selected, then $\begin{array} { r } { \boldsymbol { X } _ { i } ~ = ~ \sum _ { j = 1 } ^ { t } \boldsymbol { x } _ { i j } } \end{array}$ . And we have $\begin{array} { r l } { \mathbb { E } [ X _ { i } ] { \ } = } & { { } \frac { t k } { n } } \end{array}$ . With Chernoff bound [37], we have

$$
\operatorname * {P r} [ X _ {i} <   (1 - \delta) \mathbb {E} [ X _ {i} ] ] <   \exp (- \frac {\delta^ {2} \mathbb {E} [ X _ {i} ]}{2})
$$

$\begin{array} { r } { ( 1 - \delta ) \mathbb { E } [ X _ { i } ] = m , \mathrm { i . e . , ~ } \delta = 1 - \frac { m n } { t k } } \end{array}$

Pr[all n elements get selected at least m times]

= 1 − Pr[exists one element selected less than m times]   
$\geq 1 - n \cdot \mathbf { P r } [ X _ { i } < m ]$ (union bound [38])   
$\geq 1 - n \cdot \mathbf { e x p } ( - \frac { \delta ^ { 2 } t k } { 2 n } ) \ ( \mathbf { C h e r n o f f \ b o u n d } )$

We require all n elements to be selected at least m times with a probability no less than q, then we need $\textstyle 1 - n \cdot \exp \bigl ( - \frac { \delta ^ { 2 } t k } { 2 n } \bigr ) \geq q$ δ 2 tk ) ≥ q . And with $\begin{array} { r } { \delta = 1 - \frac { m n } { t k } } \end{array}$ mntk , we have

$$
(1 - \frac {m n}{t k}) ^ {2} \cdot \frac {t k}{2 n} \geq \ln {\frac {n}{1 - q}}
$$

$$
\frac {t k}{2 n} + \frac {m ^ {2} n}{2 t k} - (m + \ln \frac {n}{1 - q}) \geq 0
$$

Considering $t \geq m$ for all possible k, We can solve the inequality and get $\begin{array} { r } { t \geq \lambda \cdot \frac { n } { k } \cdot ( m + \ln \frac { n } { 1 - q } ) } \end{array}$ , where $1 < \lambda < 2$ , i.e., $\begin{array} { r } { t = \mathcal { O } \big ( \frac { n } { k } \cdot ( m + \ln \frac { n ^ { - } } { 1 - q } ) \big ) } \end{array}$ .

![](images/70a654297c606ae579c4fad3e612c634559920909e21316f3107ba9d80dab433.jpg)



(a) Static

![](images/7070302d2af840064b5d6dc676b20a8a0d30f6bbdac7ac9d58ad1f07939b08f4.jpg)



(b) Rolling

![](images/d84a09aa02e5113161df267fe14fdef872964b2379f67f32fe0b16fb01e7db63.jpg)



(c) Naive random

![](images/ed03a18ca7278a8eb45915a3da560a1a83c0d6efe7969e2e4530e94bf443b82e.jpg)



(d) FedEcover   
Fig. 4: Neuron selection count (difference from the mean) comparison of different submodel extraction schemes. The y-axis represents the difference between the selection count of a neuron and the average selection count of all neurons in that layer. The example layer has 2048 neurons and the statistics are from a real run of our large-client-amount experiment using CNN on FEMNIST.

# B. Empirical Results and Analysis

Our coverage-aware scheme illustrated in Fig. 2 fundamentally addresses limitations on parameter coverage evenness exposed by existing submodel extraction schemes through bufferbased cyclic random sampling ensuring strict uniform coverage frequency across parameters. The server-managed buffer system guarantees each parameter receives equal attention within finite rounds, while the random combinatorial selections emulate implicit model ensembling–a property theoretically shown to enhance generalization [39].

The experimental results in Fig. 4 quantitatively validate the superiority of FedEcover in achieving balanced parameter space coverage. For a fully-connected layer with 2048 neurons, we observe that: (a) static scheme exhibits severe polarization (Fig. 4a), where lower-indexed neurons are over-selected (positive deviations), while higher-indexed neurons remain entirely untrained (negative deviations). This aligns with our theoretical analysis of structural bias, confirming that fixed subspaces systematically exclude critical parameters from optimization. (b) rolling scheme (Fig. 4b) demonstrates periodic deviation patterns, reflecting artificial parameter coupling. Adjacent neurons share synchronized selection frequencies, creating localized overfitting regions (peaks) and under-trained valleys. (c) naive random scheme (Fig. 4c) reduces polarization but introduces obvious stochastic coverage frequency gaps, violating the ergodic principle–some neurons are neglected due to memoryless sampling, while others are redundantly selected. (d) FedEcover (Fig. 4d) achieves near-optimal uniformity, with deviations tightly bounded within [−1, +1]. The buffer-based cyclic sampling eliminates long-tail neglect and ensures all neurons receive statistically equal attention across rounds while preserving combinatorial diversity.

# VI. EXPERIMENTS

# A. Setup

1) Datasets and Models: We evaluate our method on four popular image datasets in federated learning. The first three– CIFAR-10 and CIFAR-100 [40] using a CNN with three 3 × 3 convolutional layers and one fully-connected layer, and Tiny ImageNet [41] using a ResNet-18 [11] (implemented in torchvision [42] with batch normalization replaced by static BN)–simulate synthetic Non-IID client data. Moreover, we also experiment on a realistic dataset FEMNIST from the LEAF project [43] using a CNN composed of two convolutional layers and two linear layers. For all datasets, training samples are distributed across clients, while test/validation sets serve as the global test set for evaluating the global model’s performance.

2) Regime Configuration: To demonstrate the effectiveness of model-heterogeneous FL utilizing larger models and the adaptability to real-world scenarios, we conduct experiments on both small-client-amount all-participating regime and largeclient-amount sampling-participating regime. In small-clientamount all-participating regime, we set the number of clients as 10 and all clients participate in the federated aggregation in one round. In large-client-amount sampling-participating regime, 1) for three synthetic datasets, we set the number of clients as 100 and randomly sample only 20% to participate in one round; 2) for the realistic FEMNIST datasets, there are 3237 native clients and we sample 10 clients to participate in one round.   
3) Data Heterogeneity: Similar to previous works [4], [6], we apply the Dirichlet distribution to generate non-IID data partitions among clients. Specifically, for each class cls, we sample a proportion distribution $q _ { c l s } \sim D i r _ { N } ( \alpha )$ , where DirN (α) is the Dirichlet distribution with a concentration parameter α (0.5 by default in our experiments) and N is the total number of clients in the FL system. This results in clients having unbalanced numbers of samples across different classes, as Fig. 5 shows. In addition to the synthetic non-IID data generation, we also introduce the realistic FEMNIST dataset, which is inherently non-IID and naturally exhibits data heterogeneity due to its collection from real-world users. This provides a more practical scenario for evaluating our method.   
4) Model Heterogeneity: In large-client-amount regime, we use a diverse set of client capacities: {1.0, 0.75, 0.5, 0.25, 0.1}.The mapping between client capacity and the proportion of clients is as follows: 1.0: 5%, 0.75: 10%, 0.5: 15%, 0.25: 20%, 0.1: 50%. This configuration reflects the fact that lowcapacity devices are more common and affordable. In small-

![](images/dabbb098414ff05210916e9c11cb6e5151ccade46c9da0fb9c998a915ed9bd7d.jpg)  
(a) CIFAR-10

![](images/259234d9bb09d5d64ac2fae4b215cb829ebd886b7c6d854bcb286d68e265a80d.jpg)  
(b) CIFAR-100

![](images/192fe0a2e5e99e0e4df6c110be367d6cc4066cf342541ed58d8e477adcee599b.jpg)



(c) Tiny ImageNet   
Fig. 5: Synthetic non-IID data distributions applying $D i r _ { 1 0 } ( 0 . 5 )$ on three datasets. Each color represents a client and the length of the color bar reflects the number of samples.

TABLE I: Local epochs for different regimes. ”Small” represents 10-clients-all-participating regime while ”Large” represents 100-clients-sampling for synthetic data and 3237-clientssampling for FEMNIST. 

<table><tr><td>Regime</td><td>CIFAR-10</td><td>CIFAR-100</td><td>Tiny ImageNet</td><td>FEMNIST</td></tr><tr><td>Small</td><td>2</td><td>5</td><td>10</td><td>\</td></tr><tr><td>Large</td><td>5</td><td>10</td><td>10</td><td>3</td></tr></table>

client-amount regime, we use a less diverse client capacity set: 1.0, 0.5, 0.1. The mapping between client capacity and the proportion of clients is 1.0: 10%, 0.5: 40%, 0.1: 50%. In both regimes, a client with capacity c has a submodel whose neuron number is a proportion c of the global model for each hidden layer.

5) Evaluation Metrics and Baselines: We evaluate the global model’s classification accuracy and convergence on balanced global test sets across all datasets. These test sets reflect the overall data distribution and assess generalization. We compare FedEcover with submodel extraction-based partial training FL methods: HeteroFL [24], Federated Dropout (FD-m) [26] with residual connection consistency correction (Fig. 3), and FedRolex [27]. Additionally, we compare with homogeneous FedAvg [1] using the lowest-capacity model across all clients and the server, highlighting the benefits of leveraging larger models on capable clients and the server. To highlight the superiority of our approach, we even further enhanced the compared methods by incorporating the GSD mechanism (which was not originally part of their designs).

6) Hyperparameters: For fair comparison, all methods share the same hyperparameters. The optimizer used is Adam [44]. For local training, we apply random horizontal flipping for CIFAR-10 and CIFAR-100, and random horizontal flipping with random cropping for Tiny ImageNet. The initial global aggregation step-size is set to 1.0 by default. The common hyperparameter settings for section VI-B and VI-C are as follows: Dirichelet α = 0.5, communication rounds = 300, local batch size = 64, local learning rate = 0.001, local weight decay = 0.0001, GSD coefficient γ = 0.9, GSD stop rounds $T _ { d s } = 2 0 0 , \mathrm { G S D }$ interval rounds $T _ { d i } = 1 0$ . Different hyperparameters are summarized in Table I.

TABLE II: Global top-1 test accuracy (%) comparison under 10-clients-all-participating regime. ”+” in the upper right of the method name indicates GSD enhancements applied. 

<table><tr><td>Method</td><td>CIFAR-10</td><td>CIFAR-100</td><td>Tiny ImageNet</td></tr><tr><td> $FedAvg^+$ </td><td>59.63 ± 0.38</td><td>33.38 ± 0.11</td><td>21.79 ± 0.08</td></tr><tr><td> $HeteroFL^+$ </td><td>62.31 ± 0.18</td><td>24.41 ± 0.14</td><td>15.79 ± 0.12</td></tr><tr><td> $FedRolex^+$ </td><td>68.55 ± 0.60</td><td>29.47 ± 2.07</td><td>18.41 ± 0.24</td></tr><tr><td> $FD-m^+$ </td><td>74.53 ± 0.30</td><td>38.55 ± 0.55</td><td>25.90 ± 0.14</td></tr><tr><td>FedEcover</td><td>75.25 ± 0.28</td><td>41.64 ± 0.26</td><td>26.84 ± 0.13</td></tr></table>

TABLE III: Global top-1 test accuracy (%) comparison under large-client-amount sampling-participating regime. ”+” in the upper right of the method name indicates GSD enhancements applied. 

<table><tr><td>Method</td><td>CIFAR-10</td><td>CIFAR-100</td><td>Tiny ImageNet</td><td>FEMNIST</td></tr><tr><td> $FedAvg^+$ </td><td>60.35 ± 0.17</td><td>26.07 ± 0.22</td><td>16.06 ± 0.15</td><td>73.43 ± 0.21</td></tr><tr><td> $HeteroFL^+$ </td><td>55.52 ± 0.85</td><td>16.45 ± 0.38</td><td>13.44 ± 0.41</td><td>78.43 ± 0.40</td></tr><tr><td> $FedRolex^+$ </td><td>65.16 ± 0.62</td><td>28.35 ± 0.59</td><td>19.45 ± 0.59</td><td>78.06 ± 0.48</td></tr><tr><td> $FD-m^+$ </td><td>69.70 ± 0.26</td><td>35.56 ± 0.23</td><td>24.27 ± 0.30</td><td>78.12 ± 0.29</td></tr><tr><td>FedEcover</td><td>70.40 ± 0.23</td><td>36.16 ± 0.19</td><td>24.60 ± 0.18</td><td>78.86 ± 0.29</td></tr></table>

# B. Global Model Accuracy

We comprehensively evaluate the global model’s classification performance across three synthetic datasets (CIFAR-10, CIFAR-100, Tiny ImageNet) and a realistic dataset (FEM-NIST, in large-client-amount regime), comparing our FedEcover framework with four state-of-the-art baselines enhanced by GSD. We report the global model’s mean top-1 accuracy of the last 100 rounds, with standard derivation statistics. As shown in Tables II and III, FedEcover consistently achieves superior performance across all evaluation scenarios, demonstrating remarkable adaptability to both controlled and realworld environments.

First, the performance hierarchy shifts dramatically as task complexity and system heterogeneity intensify. While $\mathrm { F e d A v g } ^ { + }$ maintains baseline functionality on simpler CIFAR-10 (59.63-60.35%), HeteroFL+ collapses by 8.97-9.62% on CIFAR-100 and 6.00-8.35% on Tiny ImageNet compared to $\mathrm { F e d A v g } ^ { + }$ , revealing fundamental limitations in handling model heterogeneity. Second, FedRolex+ exhibits regime-

![](images/b84716ba89eb68eae4825d7fb00bc6e70d3e324f7715ac19fffbcdb89f3c3224.jpg)



(a) CIFAR-10

![](images/561aff373a6ba5da2d95d0c418106bdd1baaa023007333aa508fcc2dec4458f9.jpg)



(b) CIFAR-100

![](images/da3c36b741562b5767a4631a13d13817357c47e2bada56d1003350a5f25e1c9f.jpg)



(c) Tiny ImageNet

Fig. 6: Global top-1 test accuracy in different communication rounds under small-client-amount all-participating regime.   
![](images/37c16be9b5302af6a7c1129485865df7487b7e35878710122e881cb48522f74d.jpg)



(a) CIFAR-10

![](images/e222aaf5bd3327e0fb0a105855cada0ef220791d052c1684b615e5759f0ecd9e.jpg)



(b) CIFAR-100

![](images/4b10277bef55bc1e966a53b909837aba6b1f93566002c514675a5e5ecb1b0232.jpg)



(c) Tiny ImageNet

![](images/3112e41a6f886da19b10270a3314ba47b3b858db34b6b8819e42b6f5a9febfb4.jpg)



(d) FEMNIST   
Fig. 7: Global top-1 test accuracy in different communication rounds under large-client-amount sampling-participating regime.

TABLE IV: The number(speedup) of communication rounds needed for different methods to achieve the same accuracy as the converged mean accuracy of FedAvg under 10-clientsall-participating regime. ”\” indicates that this method never reaches the target value. ”+” in the upper right of the method name indicates GSD enhancements applied.

<table><tr><td>Method</td><td>CIFAR-10</td><td>CIFAR-100</td><td>Tiny ImageNet</td></tr><tr><td> $FedAvg^{+}$ </td><td>250(1.00×)</td><td>124(1.00×)</td><td>109(1.00×)</td></tr><tr><td> $HeteroFL^{+}$ </td><td>14(17.86×)</td><td>\</td><td>\</td></tr><tr><td> $FedRolex^{+}$ </td><td>15(16.67×)</td><td>\</td><td>\</td></tr><tr><td> $FD-m^{+}$ </td><td>12(20.83×)</td><td>13(9.54×)</td><td>7(15.57×)</td></tr><tr><td>FedEcover</td><td>10(25.00×)</td><td>11(11.27×)</td><td>5(21.80×)</td></tr></table>

TABLE V: The number(speedup) of communication rounds needed for different methods to achieve the same accuracy as the converged mean accuracy of FedAvg under large-clientamount sampling-participating regime. ”\” indicates that this method never reaches the target value. ”+” in the upper right of the method name indicates GSD enhancements applied.

<table><tr><td>Method</td><td>CIFAR-10</td><td>CIFAR-100</td><td>Tiny ImageNet</td><td>FEMNIST</td></tr><tr><td> $FedAvg^{+}$ </td><td>205(1.00×)</td><td>94(1.00×)</td><td>205(1.00×)</td><td>138(1.00×)</td></tr><tr><td> $HeteroFL^{+}$ </td><td>\</td><td>\</td><td>\</td><td>59(2.34×)</td></tr><tr><td> $FedRolex^{+}$ </td><td>104(1.97×)</td><td>176(0.53×)</td><td>91(2.25×)</td><td>65(2.12×)</td></tr><tr><td> $FD-m^{+}$ </td><td>29(7.07×)</td><td>24(3.92×)</td><td>28(7.32×)</td><td>65(2.12×)</td></tr><tr><td>FedEcover</td><td>29(7.07×)</td><td>19(4.95×)</td><td>21(9.76×)</td><td>49(2.82×)</td></tr></table>

dependent effectiveness–though keeps its advantages compared to the FeadAvg+ on all datasets under the large-clientamount regime, it performs poorly under the small-clientamount all-participating regime. Third, our method achieves dual dominance: FedEcover not only surpasses FD-m+ by 0.43-3.09% absolute accuracy across all synthetic benchmarks, but also demonstrates enhanced stability through smaller standard deviations. The inclusion of FEMNIST–a realistic dataset with natural non-IID characteristics–further validates FedEcover’s practical value. As shown in the extended results, FedEcover attains 78.86% accuracy in large-client scenarios, outperforming all the other methods.

# C. Global Model Convergence

To comprehensively validate the convergence superiority of our proposed method, we present comparative analysis of global model accuracy change along with communication rounds across diverse datasets and participation regimes, as illustrated in Fig. 6 (small-client-amount all-participating) and Fig.7 (large-client-amount sampling-participating), as well as overall speedup performance showed in Tables IV and V. Notably, FedEcover demonstrates advantages in both convergence speed and stability, outperforming baseline and state-of-the-art approaches.

Under the small-client-amount regime (Fig. 6), FedEcover achieves the fastest accuracy improvement across all datasets. While submodel-based methods generally surpass FedAvg+ on CIFAR-10, their performance diverges substantially on complex datasets: HeteroFL+ and FedRolex+ exhibit sluggish convergence on CIFAR-100 and Tiny ImageNet, failing to match FedAvg+’s final accuracy. In contrast, FedEcover maintains a steep accuracy trajectory and outperform all the other methods, attaining 5.8-15.6% higher converged accuracy than FedAvg+ while requiring 90% fewer communication rounds (Table IV). The superiority of FedEcover maintains under the large-client-amount regime (Fig. 7), where we extend our evaluation to include the realistic FEMNIST dataset. FedEcover consistently achieves the highest convergence rate and stability across CIFAR-10, CIFAR-100, Tiny ImageNet and FEMNIST. It eliminates the early-stage performance dip observed in FedRolex+ while accelerating convergence by 0.7-2.4× compared to FD-m+ (Table V). Notably, FedEcover achieves the best convergence performance while maintaining the best final accuracy improvements, demonstrating efficiency-accuracy synergy.

![](images/ab66ff0aa59501a5bae0496393b8e50278f94039752ec43e91a657077824f248.jpg)



(a) HeteroFL

![](images/c6a98d4ba4227ded681fbdec1f63caab9da6c74ad86de1588cf6575e8575e8b9.jpg)



(b) FedRolex

![](images/4807b290eb9ed1a1436f05702d8c5badc130d4211978e21f3d7b3790bba04c94.jpg)



(c) FD-m

![](images/13a3cfcd69bfe8e0351c0d601b04a84df160db0dea52a30eae2d408aec1a7d33.jpg)



(d) FedEcover

Fig. 8: Global top-1 test accuracy comparison between w/ GSD and w/o GSD on CIFAR-100 (IID) under large-client-amount sampling-participating regime. Each subfigure shows the difference between using GSD and not using GSD of one method.   
![](images/3f2efce5e2a8c5b96887daf7fd96e7e0ebe72c60f592f8dc233f9537892b2714.jpg)



(a) small-client-amount

![](images/0ed0ad81826ab63289bb9afae868b21567953cce5d28540ec65f7fe169b5a216.jpg)



(b) large-client-amount   
Fig. 9: Converged accuracy and speedup of different methods on CIFAR-100 with varying degrees of data heterogeneity (two regimes). Lines represent accuracy and bars represent speedup. There is no bar for a method if the method has never reached the converged accuracy of FedAvg.

# D. Performance Robustness Analysis under Varying Degrees of Data Heterogeneity

To systematically evaluate algorithmic robustness under diverse degrees of statistical heterogeneity, we conduct controlled experiments with four distinct Dirichlet allocation parameter values α = {0.2, 0.5, 1.0, 5.0}, where decreasing α values (from 5.0 to 0.2) progressively intensify the heterogeneity of data partitioning across clients. The comprehensive comparative analysis presented in Fig. 9 reveals that FedEcover maintains outperforming the other methods in terms of both converged accuracy and speedup in most cases, demonstrating FedEcover’s enhanced adaptability to statistical heterogeneity through its innovative submodel extraction scheme and aggregation mechanism, suggesting its practical value for real-world federated learning deployments where data heterogeneity is an inherent characteristic.

# E. Ablation and Hyperparameter Studies

Effectiveness of coverage-aware submodel extraction. In previous results (VI-B, VI-C, VI-D), among all submodel extraction-based partial training methods (HeteroFL, FedRolex, FD-m, FedEcover) adopting the same settings, we have relatively consistent comparison results: FedEcover > FD-m > FedRolex > HeteroFL, in terms of both accuracy improving rate and converged accuracy. The results empirically confirm the contribution of higher parameter space coverage efficiency due to our proposed submodel extraction scheme to enhancing the performance of the global model.

Addressing model heterogeneity: a data-homogeneityablated perspective. While prior works [24], [26], [27] leave client drift caused by model heterogeneity underexplored, our IID-condition experiments (Fig. 8) isolate the impact of model heterogeneity, conclusively demonstrating GSD’s unique capability to stabilize convergence even in data-homogeneous settings. As Fig. 8 demonstrated, even with IID data, model heterogeneity alone induces significant oscillations, while GSD reduces oscillation magnitude significantly and enable the global model to converge steadily.

Effectiveness of global aggregation step-size decay (GSD). To rigorously evaluate the standalone impact of GSD across diverse frameworks, we compare the convergence behaviors of the five methods (FedAvg, HeteroFL, FedRolex, FD-m, and our FedEcover) between with and without GSD. As depicted in Fig. 10 and Fig. 11, GSD consistently enhances global model convergence by mitigating oscillations induced by the compounded effects of data heterogeneity and submodel heterogeneity. This ablation analysis demonstrates that GSD’s contribution is orthogonal to algorithmic innovations in local training, establishing it as an essential component for harmonizing cross-client updates in heterogeneous environments. Notably, GSD acts as a lightweight yet pivotal module that dynamically adjusts the influence of local updates during aggregation. In early phases, it prioritizes rapid knowledge integration by amplifying update contributions, thereby accelerating initial performance gains. As federated training progresses, GSD systematically attenuates the aggregation step size, effectively suppressing the destabilizing variance introduced by heterogeneous submodels. This mechanism ensures robust convergence across all evaluated methods. Its ability to decouple convergence stability from framework-specific designs validates GSD as a universal solution for federated scenarios requiring adaptive aggregation control.

![](images/fff6edeb563050f18eae8e69081455d11af9dfc8e845e38ccf935552bd963b43.jpg)



(a) FedAvg

![](images/30bf314781f475ca799a44c992b76d16eef546f7d1a8c48743d07f0a3fea8b61.jpg)



(b) HeteroFL

![](images/9af4f95030c3d60dc573566caa67071883bac3c2c486152d426339268b2a19cc.jpg)



(c) FedRolex

![](images/61abfa981a89cd4c00a82c2c5ef7f75ec0b67d89c4da8205b4aac4221b94d192.jpg)



(d) FD-m

![](images/9d77fa6110233d63dfa0524500affbad696c0274994030a9a929dc8a9f9b531f.jpg)



(e) FedEcover

Fig. 10: Global top-1 test accuracy comparison between w/ GSD and w/o GSD on CIFAR-100 (α = 0.5) under small-clientamount all-participating regime. Each subfigure shows the difference between using GSD and not using GSD of one method.   
![](images/140cae980fd13b68a6e2d2267a5153f5b1c47ef07adbc91ddb503ab803a7beee.jpg)



(a) FedAvg

![](images/7a9bc31dfde7447a4b537930d6998e94e5296e126fcd89c40380b3ec9bb7d3c7.jpg)



(b) HeteroFL

![](images/9134aae83274f3e21c3c2add047c0194c277aec5d2d53426a55311b6bc1d2762.jpg)



(c) FedRolex

![](images/ab77d8ee922fe51ce7ab7f63f42f10238bb9fe90b0515010d1d710fbe9627a7f.jpg)



(d) FD-m

![](images/8eb584cc7a9346531ef8d5959fda4b1893459a9bf8be40d6a1f16aa18f84ff47.jpg)



(e) FedEcover   
Fig. 11: Global top-1 test accuracy comparison between w/ GSD and w/o GSD on CIFAR-100 (α = 0.5) under large-clientamount sampling-participating regime. Each subfigure shows the difference between using GSD and not using GSD of one method.

![](images/93513572c2a23c75b9d7e184592547bc9e744f1ed51ce0c046c93bc29ad8e677.jpg)



(a) Stop rounds $T _ { d s } = 1 0 0$

![](images/5a42f5ae53d90b9070b2648cc78e802d585d5e42e8803e9d8118a5493792b7d6.jpg)



(b) Stop rounds $T _ { d s } = 2 0 0$   
Fig. 12: Converged accuracy and speedup of different methods on CIFAR-100 (100 clients) with varying γ of GSD. Lines represent accuracy and bars represent speedup. There is no bar for a method if the method has never reached the converged accuracy of FedAvg. Dotted lines represent accuracy of corresponding method w/o GSD.

Hyperparameter sensitivity analysis. We provide a systematic empirical analysis regarding the sensitivity of GSD to relevant hyperparameters (e.g., decay coefficient γ, stop rounds $T _ { d s } )$ in Fig. 12. GSD exhibits robust performance across different values of $\gamma$ and $T _ { d s } \mathrm { : }$ FedEcover maintains stable performance, with no more than 2% accuracy variation across all combinations of hyperparameter values. In most cases, all frameworks achieve accuracy improvements compared to their non-GSD baselines (dotted lines), regardless of γ. Moreover, FedEcover shows its superiority by consistently achieving the best accuracy improvements and creditable speedups performance across different hyperparameter values.

# VII. CONCLUSION

In this work, we propose FedEcover, an effective modelheterogeneous FL framework to address the challenges of data heterogeneity and client capacity heterogeneity. To promote convergence rate and final performance, FedEcover develops an efficient submodel extraction scheme adopting random sampling without replacement with layer buffers, achieving comprehensive parameter space coverage and submodel diversity. The global aggregation step-size decay mechanism further stabilizes convergence under dual heterogeneity. Experiments demonstrate FedEcover’s superiority across various benchmarks. While our current implementation focuses on conventional neural networks, the architecture-agnostic principles of coverage-aware submodel extraction and adaptive aggregation could extend to more architectures with specialized indexing strategies to achieve structural consistency, which presents an interesting direction for future exploration. This generality positions FedEcover as a versatile framework for heterogeneous federated learning scenarios.

# ACKNOWLEDGMENT

Lan Zhang and Jun Wang are the corresponding authors. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 62441228, Science and Technology Tackling Program of Anhui Province, No.202423k09020016.

# REFERENCES

[1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial intelligence and statistics. PMLR, 2017, pp. 1273– 1282.   
[2] T. Li, A. K. Sahu, M. Zaheer, M. Sanjabi, A. Talwalkar, and V. Smith, “Federated optimization in heterogeneous networks,” Proceedings of Machine learning and systems, vol. 2, pp. 429–450, 2020.   
[3] S. P. Karimireddy, S. Kale, M. Mohri, S. Reddi, S. Stich, and A. T. Suresh, “Scaffold: Stochastic controlled averaging for federated learning,” in International conference on machine learning. PMLR, 2020, pp. 5132–5143.   
[4] Q. Li, B. He, and D. Song, “Model-contrastive federated learning,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2021, pp. 10 713–10 722.   
[5] M. Mendieta, T. Yang, P. Wang, M. Lee, Z. Ding, and C. Chen, “Local learning matters: Rethinking data heterogeneity in federated learning,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2022, pp. 8397–8406.   
[6] Z. Li, T. Lin, X. Shang, and C. Wu, “Revisiting weighted aggregation in federated learning with neural networks,” in International Conference on Machine Learning. PMLR, 2023, pp. 19 767–19 788.   
[7] W. Y. B. Lim, N. C. Luong, D. T. Hoang, Y. Jiao, Y.-C. Liang, Q. Yang, D. Niyato, and C. Miao, “Federated learning in mobile edge networks: A comprehensive survey,” IEEE communications surveys & tutorials, vol. 22, no. 3, pp. 2031–2063, 2020.   
[8] Y. Wang, Y. Tong, Z. Zhou, R. Zhang, S. J. Pan, L. Fan, and Q. Yang, “Distribution-regularized federated learning on non-iid data,” in 2023 IEEE 39th International Conference on Data Engineering (ICDE). IEEE, 2023, pp. 2113–2125.   
[9] Z. Jiang, Y. Xu, H. Xu, Z. Wang, and C. Qiao, “Clients help clients: Alternating collaboration for semi-supervised federated learning,” in 2024 IEEE 40th International Conference on Data Engineering (ICDE). IEEE, 2024, pp. 1847–1860.   
[10] Y. Mei, P. Guo, M. Zhou, and V. Patel, “Resource-adaptive federated learning with all-in-one neural composition,” Advances in Neural Information Processing Systems, vol. 35, pp. 4270–4284, 2022.   
[11] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.   
[12] D. Li and J. Wang, “Fedmd: Heterogenous federated learning via model distillation,” arXiv preprint arXiv:1910.03581, 2019.   
[13] T. Lin, L. Kong, S. U. Stich, and M. Jaggi, “Ensemble distillation for robust model fusion in federated learning,” Advances in neural information processing systems, vol. 33, pp. 2351–2363, 2020.   
[14] Y. Deng, J. Ren, C. Tang, F. Lyu, Y. Liu, and Y. Zhang, “A hierarchical knowledge transfer framework for heterogeneous federated learning,” in IEEE INFOCOM 2023-IEEE Conference on Computer Communications. IEEE, 2023, pp. 1–10.   
[15] Z. Wu, S. Sun, Y. Wang, M. Liu, B. Gao, Q. Pan, T. He, and X. Jiang, “Agglomerative federated learning: Empowering larger model training via end-edge-cloud collaboration,” in IEEE INFOCOM 2024- IEEE Conference on Computer Communications. IEEE, 2024, pp. 131– 140.   
[16] G. Hinton, “Distilling the knowledge in a neural network,” arXiv preprint arXiv:1503.02531, 2015.   
[17] P. P. Liang, T. Liu, L. Ziyin, N. B. Allen, R. P. Auerbach, D. Brent, R. Salakhutdinov, and L.-P. Morency, “Think locally, act globally: Federated learning with local and global representations,” arXiv preprint arXiv:2001.01523, 2020.   
[18] L. Yi, G. Wang, X. Liu, Z. Shi, and H. Yu, “Fedgh: Heterogeneous federated learning with generalized global header,” in Proceedings of the 31st ACM International Conference on Multimedia, 2023, pp. 8686– 8696.   
[19] Y. Tan, G. Long, L. Liu, T. Zhou, Q. Lu, J. Jiang, and C. Zhang, “Fedproto: Federated prototype learning across heterogeneous clients,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 36, 2022, pp. 8432–8440.   
[20] J. Zhang, Y. Liu, Y. Hua, and J. Cao, “Fedtgp: Trainable global prototypes with adaptive-margin-enhanced contrastive learning for data and model heterogeneity in federated learning,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 38, 2024, pp. 16 768– 16 776.

[21] ——, “An upload-efficient scheme for transferring knowledge from a server-side pre-trained generator to clients in heterogeneous federated learning,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2024, pp. 12 109–12 119.   
[22] C. Niu, F. Wu, S. Tang, L. Hua, R. Jia, C. Lv, Z. Wu, and G. Chen, “Secure federated submodel learning,” arXiv preprint arXiv:1911.02254, 2019.   
[23] Y. Ding, C. Niu, F. Wu, S. Tang, C. Lyu, and G. Chen, “Dc-ccl: Devicecloud collaborative controlled learning for large vision models,” arXiv preprint arXiv:2303.10361, 2023.   
[24] E. Diao, J. Ding, and V. Tarokh, “Heterofl: Computation and communication efficient federated learning for heterogeneous clients,” arXiv preprint arXiv:2010.01264, 2020.   
[25] S. Horvath, S. Laskaridis, M. Almeida, I. Leontiadis, S. Venieris, and N. Lane, “Fjord: Fair and accurate federated learning under heterogeneous targets with ordered dropout,” Advances in Neural Information Processing Systems, vol. 34, pp. 12 876–12 889, 2021.   
[26] S. Caldas, J. Konecny, H. B. McMahan, and A. Talwalkar, “Expanding ˇ the reach of federated learning by reducing client resource requirements,” arXiv preprint arXiv:1812.07210, 2018.   
[27] S. Alam, L. Liu, M. Yan, and M. Zhang, “Fedrolex: Modelheterogeneous federated learning with rolling sub-model extraction,” Advances in neural information processing systems, vol. 35, pp. 29 677– 29 690, 2022.   
[28] H. Zhou, T. Lan, G. P. Venkataramani, and W. Ding, “Every parameter matters: Ensuring the convergence of federated learning with dynamic heterogeneous models reduction,” Advances in Neural Information Processing Systems, vol. 36, 2024.   
[29] Y. Jiang, S. Wang, V. Valls, B. J. Ko, W.-H. Lee, K. K. Leung, and L. Tassiulas, “Model pruning enables efficient federated learning on edge devices,” IEEE Transactions on Neural Networks and Learning Systems, vol. 34, no. 12, pp. 10 374–10 386, 2022.   
[30] B. Nader, H. Jiahui, Z. Hui, and L. Xin, “Adaptive federated dropout: Improving communication efficiency and generalization for federated learning,” in Proceedings of the IEEE Conference on Computer Communications Workshops, Vancouver, BC, Canada, 2021, pp. 10–13.   
[31] J. Frankle and M. Carbin, “The lottery ticket hypothesis: Finding sparse, trainable neural networks,” arXiv preprint arXiv:1803.03635, 2018.   
[32] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, “Dropout: A simple way to prevent neural networks from overfitting,” Journal of Machine Learning Research, vol. 15, no. 56, pp. 1929–1958, 2014. [Online]. Available: http://jmlr.org/papers/v15/srivastava14a.html   
[33] A. Vaswani, “Attention is all you need,” Advances in Neural Information Processing Systems, 2017.   
[34] G. Cheng, Z. Charles, Z. Garrett, and K. Rush, “Does federated dropout actually work?” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2022, pp. 3387–3395.   
[35] D. Guliani, L. Zhou, C. Ryu, T.-J. Yang, H. Zhang, Y. Xiao, F. Beaufays, and G. Motta, “Enabling on-device training of speech recognition models with federated dropout,” in ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2022, pp. 8757–8761.   
[36] Wikipedia contributors, “Bernoulli trial — Wikipedia, the free encyclopedia,” https://en.wikipedia.org/w/index.php?title=Bernoulli trial& oldid=1233613455, 2024, [Online; accessed 28-October-2024].   
[37] , “Chernoff bound — Wikipedia, the free encyclopedia,” https://en. wikipedia.org/w/index.php?title=Chernoff bound&oldid=1243402280, 2024, [Online; accessed 28-October-2024].   
[38] , “Boole’s inequality — Wikipedia, the free encyclopedia,” https://en.wikipedia.org/w/index.php?title=Boole%27s inequality& oldid=1244809845, 2024, [Online; accessed 28-October-2024].   
[39] L. Wan, M. Zeiler, S. Zhang, Y. Le Cun, and R. Fergus, “Regularization of neural networks using dropconnect,” in International conference on machine learning. PMLR, 2013, pp. 1058–1066.   
[40] K. Alex, “Learning multiple layers of features from tiny images,” https://www. cs. toronto. edu/kriz/learning-features-2009-TR. pdf, 2009.   
[41] mnmoustafa and M. Ali, “Tiny imagenet,” https://kaggle.com/ competitions/tiny-imagenet, 2017, kaggle.   
[42] T. maintainers and contributors, “Torchvision: Pytorch’s computer vision library,” https://github.com/pytorch/vision, 2016.   
[43] S. Caldas, S. M. K. Duddu, P. Wu, T. Li, J. Konecnˇ y, H. B. McMahan, \` V. Smith, and A. Talwalkar, “Leaf: A benchmark for federated settings,” arXiv preprint arXiv:1812.01097, 2018.

[44] D. P. Kingma, “Adam: A method for stochastic optimization,” arXiv preprint arXiv:1412.6980, 2014.