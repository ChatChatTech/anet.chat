# FedSDG-FS: Efficient and Secure Feature Selection for Vertical Federated Learning

Anran Li∗§, Hongyi Peng∗††§, Lan Zhang†∥, Jiahui Huang†, Qing Guo‡, Han Yu∗, Yang Liu¶ ∗Nanyang Technological University, Singapore, ††Alibaba-NTU Singapore Joint Research Institute & Alibaba Group †University of Science and Technology of China, China, ‡Center for Frontier AI Research (CFAR), A\*STAR, Singapore ¶Zhejiang Sci-Tech University, China, ∥Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, China

Abstract—Vertical Federated Learning (VFL) enables multiple data owners, each holding a different subset of features about largely overlapping sets of data sample(s), to jointly train a useful global model. Feature selection (FS) is important to VFL. It is still an open research problem as existing FS works designed for VFL either assumes prior knowledge on the number of noisy features or prior knowledge on the post-training threshold of useful features to be selected, making them unsuitable for practical applications. To bridge this gap, we propose the Federated Stochastic Dual-Gate based Feature Selection (FedSDG-FS) approach. It consists of a Gaussian stochastic dual-gate to efficiently approximate the probability of a feature being selected, with privacy protection through Partially Homomorphic Encryption without a trusted third-party. To reduce overhead, we propose a feature importance initialization method based on Gini impurity, which can accomplish its goals with only two parameter transmissions between the server and the clients. Extensive experiments on both synthetic and real-world datasets show that FedSDG-FS significantly outperforms existing approaches in terms of achieving accurate selection of high-quality features as well as building global models with improved performance.

Index Terms—Feature selection, vertical federated learning

# I. INTRODUCTION

Federated learning (FL) [1]–[5] is an emerging machine learning pardigm, which enables multiple data owners to jointly train a model by iteratively exchanging model parameters through an FL server, while preserving local data privacy. Based on the distribution of local data, there are two main categories of FL scenarios: 1) horizontal federated learning (HFL) and 2) vertical federated learning (VFL). Under HFL [6]–[8], data owners’ local datasets have little overlap in the sample space but large overlaps in the feature space. Under VFL [9]–[11], data owners’ local datasets have large overlaps in the sample space but little overlap in the feature space. VFL scenarios often arise in real applications [12], [13], e.g., an e-commerce company, a bank and a ride-sharing company can collaborate to build a model to identify potential financial fraudsters based on the multiple perspectives on people’s behaviour through VFL. The quality of data owners’ local features determines the effectiveness of their local models, thereby affecting the performance of the global VFL model. In practice, data owners can possess noisy features that are irrelevant to the learning task, or a large number of redundant features, which seriously impairs global model performance. As an example, one of our experiments in Section III-B shows that a two-class classifier trained by VFL with the real dataset suffered an accuracy loss from 82.6% to 54.2% due to the existence of noisy features.

To improve the performance of VFL systems, in this work, we focus on filtering noisy features and selecting important features. A number of feature selection methods have been proposed for centralized machine learning settings [14]–[16], while few work focused on VFL [17]. Feature selection methods for centralized machine learning can be divided into three categories: 1) filter methods calculate per-feature relevance scores based on statistical measures (e.g., Gini impurity) to filter features prior to learning a model [16], [18], [19]; 2) wrapper methods search for the optimal feature subset in large search spaces [20], [21]; and 3) embedded methods attempt to select subset of important features while simultaneously learn the model [15], [22], [23].

Existing FS works designed for VFL either assumes prior knowledge on the number of noisy features [17] or prior knowledge on the post-training threshold of useful features to be selected [24]. These assumptions make them unsuitable for practical VFL applications. The problem of feature selection in VFL settings remains open. To enable feature selection to be performed in VFL settings, the following key research questions need to be addressed. 1) How to accurately identify noisy features, and select a small number of important features to train an optimal global VFL model in a privacy-preserving manner? Existing FS methods require direct access to training samples, the training process and the labels simultaneously, which is not permitted in VFL. Besides, during VFL training, intermediate parameters are transmitted in ciphertexts [25], [26], which further increases the difficulty of feature selection. 2) How to conduct feature selection efficiently and adaptively in VFL settings? Existing FS methods require a large number of training iterations to select features, especially for high-dimensional data [15], [22]. Directly applying them in VFL will incur significant computation and communication overhead since each training round involves multiple encryption/decryption operations and intermediate parameter transfers.

To address the aforementioned questions and the limitations of existing works [17], [24], we propose the Federated

Stochastic Dual-Gate based Feature Selection (FedSDG-FS) approach. It is an embedded feature selection approach consisting of a feature importance initialization module and a secure important feature selection module. Its advantages are summarized as follows:

• Context-Awareness: FedSDG-FS can jointly perform feature selection and model training following the proposed stochastic dual-gate and Gini impurity-based feature importance initialization, thereby ensuring the selected features be to relevant to the context of the model.   
• Efficiency: The FedSDG-FS Gini impurity based feature importance initialization enables the global model to quickly filter out noisy features and select important ones, thus speeding up model training. The stochastic dualgates are designed to reduce the sizes of the embedding vectors, thereby saving communication costs.   
• Security: FedSDG-FS achieves secure feature selection and model training by leveraging partially homomorphic encryption (PHE) and the randomized mechanism. During the feature selection and model training process, neither data nor labels are exposed to any party other than their original owners.

We evaluate FedSDG-FS via extensive experiments using nine datasets including tabular data, images, texts and audios on a VFL system. The results show that it significantly outperforms existing approaches in terms of achieving accurate and secure selection of high-quality features to build high-performance VFL models. Taking MADELON dataset as an instance, the average test accuracy of FedSDG-FS is 27.0% higher than that of the best performing baseline with 47% fewer features required, and only half the communication cost.

# II. RELATED WORKS

Feature selection plays an important role in machine learning tasks. There are a number of feature selection methods proposed for centralized machine learning settings [14]–[16], while few works deal with feature selection in VFL [17].

# A. Feature Selection in Centralized Learning

Feature selection methods in centralized learning settings can be divided into three categories: 1) filter methods, 2) wrapper methods, and 3) embedded methods. Filter FS methods attempt to remove irrelevant features prior to learning a model. These methods filter features using relevance scores (e.g., Gini impurity) and mutual information, which are calculated based on statistical measures [14], [16], [18], [27]. Wrapper FS methods leverage the outcomes of a model to determine the importance of each feature. They attempt to select a subset of features which can achieve the best prediction performance. As the number of subsets can be very large in the context of deep neural networks, and a model need to be recomputed for each subset, wrapper methods are generally computationally expensive [20], [21], [28]. Embedded FS methods aim to select a subset of relevant features, while simultaneously learning the model [15], [22], [23]. The least absolute shrinkage and selection operator [23] is a well-known embedded FS method, whose objective is to minimize the loss while enforcing an l1 constraint on the weights of the features. Another recently proposed method [15] uses a continuously relaxed Bernoulli variable to conduct FS based on stochastic gates. However, this method requires a large number of parameters to be trained in the first layer, resulting in overfitting to the training data, especially for deep neural networks with high-dimensional data or when there are only a limited number of training samples available.

Since these methods are designed for centralized learning scenarios in which all training data are accessible, such approaches are not applicable to VFL which demands data privacy protection. In addition, they are also not optimized to reduce communication or computation costs when the volume of training data is large.

# B. Feature Selection in VFL

In VFL, there are only two works on feature selection (FS) [17], [29]. In [17], FS is performed with the filter method based on secure multi-party computation. However, since it performs VFL feature selection out of the context of the learning task, it can lead to inaccurate feature selection. Besides, it assumes that the number of noisy features is known in advance, and that there is a trusted third party for performing FS. These assumptions are unrealistic in practice. Further, it incur large communication overhead since a massive amount of parameters are transmitted between participants and the trusted third party. In [29] the embedded method combined the auto-encoder with $l _ { 2 }$ constraints on feature weights is used for FS. However, it suffers from shrinkage of the model parameters, and requires post-training threshold setting to determine the selected features [24]. The proposed FedSDG-FS approach addresses these limitations of the state of the art.

# III. PRELIMINARIES & PROBLEM DEFINITION

# A. Basic Setup of VFL

There are two types of entities involved in VFL: a server S and M clients $\mathcal { M } : = \{ 1 , 2 , \cdots , M \}$ . A dataset $U \ =$ $\{ U _ { 1 } , \cdots , U _ { M } \}$ of N samples, $\{ X , Y \} : = \{ x _ { n } , y _ { n } \} _ { n = 1 } ^ { N } ,$ is maintained by the M clients. Let $[ N ] ~ = ~ \{ 1 , 2 , \cdot \cdot \cdot , N \}$ . Each client m is associated with a unique set of features $\{ f _ { m , 1 } , \cdot \cdot \cdot , f _ { m , d _ { m } } \}$ , and owns sample $x _ { n , m } \in \mathbb { R } ^ { d _ { m } } , n \in [ N ]$ , where $x _ { n , m }$ is the m-th block of the n-th sample vector $\boldsymbol { x } _ { n } : = \left[ x _ { n , 1 } ^ { \top } , x _ { n , 2 } ^ { \top } , \cdot \cdot \cdot , x _ { n , M } ^ { \top } \right] ^ { \top }$ . Suppose there are c possible class labels, the n-th label $\bar { y } _ { n } ~ \in ~ [ c ]$ is stored by server S. Typically, a data owner, which holds both the feature and the class labels, can act as the “FL server”. It is referred to as the active party. Others which hold only features are referred to as the passive parties.

Each client m learns a local embedding $h _ { m }$ parameterized by $\theta _ { m } \in \Theta$ that maps a high-dimensional vector $x _ { n , m } \in \mathbb { R } ^ { d _ { m } }$ into a low-dimensional one $h _ { n , m } : = h _ { m } ( \theta _ { m } ; x _ { n , m } ) \in \mathbb { R } ^ { \underline { { d _ { m } } } }$ with $\underline { { d } } _ { m } \ll d _ { m }$ . The server S learns the prediction yˆn parameterized by the top model $\theta _ { 0 } : = \{ w _ { 1 } , \cdot \cdot \cdot , w _ { M } , \alpha _ { 0 } \} \in \Theta$ , $w _ { m } \in \mathbb { R } ^ { \underline { { d _ { m } } } } , m \in [ M ]$ , where $\{ w _ { 1 } , \cdot \cdot \cdot , w _ { M } \}$ are parameters of the interactive layer which concatenates embedding vectors $h _ { n , 1 } , \cdots , h _ { n , M }$ in a weighted manner. α0 denotes the parameters of the succeeding layers of the top model connected to the interactive layer. Ideally, the objective of VFL is to minimize,

![](images/673105de4174c51c857808a8479c68d8080f79b69bfe7b4196c9aa8ca0835188.jpg)



(a) Accuracy and model size vs. number of participating features

![](images/8bac699a4aa565d0dd3b64e29524c5aa2c4a9f8c4fdba08931025aa96b091714.jpg)



(b) Accuracy vs. number of participating features   
Fig. 1. Test accuracy and model size of vertical neural networks training using (a) the dataset ARECENE with redundant features; (b) the dataset MADELON with noisy features.

$$
\begin{array}{l} R (\boldsymbol {\theta}) := \mathbb {E} _ {X, Y} L \left(h \left(\theta_ {0}, h _ {n, 1}, \dots , h _ {n, M}\right); y _ {n}\right) \tag {1} \\ \text { with } h _ {n, m} := h _ {m} (\theta_ {m}; x _ {n, m}), m \in [ M ] \\ \end{array}
$$

where $\pmb { \theta } : = \{ \theta _ { i } \} _ { i = 0 } ^ { M }$ denotes the global model, which consists of M local models $\theta _ { 1 } , \cdots , \theta _ { M }$ and the top model $\theta _ { 0 } ,$ and $L ( \cdot ; \cdot )$ is the loss function. This problem can be solved via iterative stochastic optimization. In the t-th iteration, the server receives embedding vectors $\{ h _ { n , m } ^ { t } \} _ { m = 1 } ^ { M }$ from M clients. It then calculates and sends the gradients of the loss w.r.t. $h _ { n , m } ^ { t }$ to all clients. Upon receiving the gradients, client m updates the local model to obtain $\theta _ { m } ^ { t + 1 }$ . Then, client m randomly selects a datum $x _ { n , m } ,$ , calculates $h _ { n , m } ^ { t + 1 }$ using $\theta _ { m } ^ { t + 1 }$ , and uploads it to the server. This process is repeated until the global model converges (i.e., a convergence criterion is met). To ensure that neither data nor labels can be obtained or inferred by any other party, the above iterative training must be conducted in a privacy-preserving manner.

# B. Motivating Examples

Here, we perform data driven analysis to demonstrate the necessity of feature selection in VFL. We illustrate this from two aspects: 1) many clients may possess a large number of redundant features, which results in a low quality and very complex global model; and 2) some clients can possess noisy or task irrelevant features which reduce global model performance. Specifically, we use datasets ARCENE [30] and MADELON [31] as training data to investigate the two observations. ARCENE contains 2,400 instances with 7,000 informative but redundant features. MADELON contains 4,400 instances with 5 informative features and 480 noisy features. We employ two clients, A and B, and a server to jointly train neural networks [25] based on these two datasets via VFL.

To illustrate aspect 1), we assign different numbers of features of ARCENE to client B, while assigning 100 fixed features to client A to train the VFL network. The results in Fig 1(a) show that, as the number of redundant features increases, the test accuracy of the global model decreases slightly, while the model size grows rapidly. To illustrate aspect 2), we assign different numbers of noisy features from the MADELON dataset to client B, while assigning 10 fixed features to client A to train the VFL models. The results are shown in Fig. 1(b), where 10 : k indicates that, A owns 10 features (i.e., 3 informative features and 7 noisy features), and B owns k features (i.e., 2 informative features and (k − 2) noisy features). The result shows that as the number of noisy features increases, the test accuracy of the global VFL model decreases significantly. These results show that an efficient and privacy-preserving feature selection method is urgently needed for VFL.

# C. Problem Formulation

In a typical VFL system, under the coordination of the server S, all participants train a global model by transferring their local embedding vectors trained using their local datasets. Additionally, we consider a situation in practice in which some clients possess a large number of noisy features or redundant features. This may result in a low-performance and extremely complex global model. Specifically, we can divide all features into qualified important features and negatively influential features, e.g., noisy features or redundant features, by their effects to the objective of the global model. A desired VFL framework should enable all participants to jointly train a simple global model with a small number of important features, while eliminating negatively influential features. The goal of feature selection in VFL is to simultaneously select a subset of features, and construct a global model θˆ with the objective by minimizing the risk,

$$
\begin{array}{l} R (\boldsymbol {\theta}, s) := \mathbb {E} _ {X, Y} L (h (\theta_ {0}, h _ {n, 1}, \dots , h _ {n, M}); y _ {n}) \\ \text { with } h _ {n, m} := h _ {m} (\theta_ {m}; x _ {n, m} \odot s _ {m}), m \in [ M ], \\ \end{array}
$$

where $s _ { m } = \{ 0 , 1 \} ^ { d _ { m } }$ is the vector of indicator variables, and $s _ { m , i } , i \in [ d _ { m } ]$ are Bernoulli variables which indicate whether or not the i-th feature of client m is selected. We assume that all participants are semi-honest. They follow the exact protocol of VFL and feature selection, but are curious about others’ private information.

# IV. THE PROPOSED FedSDG-FS APPROACH

In this section, we first present the system architecture of FedSDG-FS. Then, we illustrate the key technique to enable feature selection to be performed jointly with model training under VFL settings. Finally, we present the details of the FedSDG-FS algorithms.

# A. System Overview

FedSDG-FS consists of two modules (as shown in Fig. 2):

1) Feature Importance Initialization before Training. To save feature selection costs, local clients first securely initialize feature importance based on Gini impurity and PHE, in cooperation with the server prior to the model training.   
2) Important Feature Selection during Training. After feature importance initialization, the server coordinates clients to select important features, while training the VFL model for improved performance. Specifically, to fulfil the requirement that neither data nor labels can be obtained or inferred by any other party other than their original owners, we propose

![](images/11d19d5ada39145ada6e36ac0562b07bb1fd6cab2341977c63425b4ae81df58b.jpg)



Fig. 2. System overview of FedSDG-FS. ⃝1 Send encrypted embeddings, $\textcircled{2}$ send encrypted gradients.

a secure FS approach which includes forward propagation for secure feature selection, and backward propagation for secure feature selection, based on the proposed stochastic dualgate, PHE and the randomized noise mechanism. In this way, FedSDG-FS determines the selected features and produces an optimal global model $\hat { \theta }$ with higher accuracy and fast convergence.

# B. Stochastic Dual-Gates for VFL

To achieve accurate feature selection while simultaneously training the global model in VFL, we need to dynamically quantify the influence of features on the global model during training, and increase the probability of selection for highly influential features. In VFL, local embedding vectors are transferred to the server, where the size of embedding vectors affects the communication cost. To reduce communication overhead in feature selection, we first introduce stochastic dual-gates for VFL to efficiently approximate the probabilities of features and embedding vectors being selected. We reexpress Eq. (2) into minimizing the $l _ { 0 }$ constrained risk:

$$
\begin{array}{l} R (\boldsymbol {\theta}, s, q) := \mathbb {E} _ {X, Y} L (h (\theta_ {0}, g _ {n, 1}, \dots , g _ {n, M}); y _ {n}) \\ + \lambda \sum_ {m} \left(| s _ {m} | _ {0} + | q _ {m} | _ {0}\right) \tag {3} \\ \end{array}
$$

where $h _ { n , m } : = h _ { m } \mathopen { } \mathclose \bgroup \left( \theta _ { m } ; x _ { n , m } \odot s _ { m } \aftergroup \egroup \right) , g _ { n , m } = h _ { n , m } \odot q _ { m } , q _ { m } =$ $\{ 0 , 1 \} ^ { \underline { { d } } _ { m } }$ is the vector of indicator variables, where $q _ { m , i } , i \in$ $[ d _ { m } ]$ are Bernoulli variables and indicate whether or not the ith dimension of embedding $h _ { n , m }$ is selected for global model training. λ is a weighting factor for the regularization. The $l _ { 0 }$ norm penalizes the number of non-zero entries in the vectors $s _ { m } , q _ { m }$ , thus encourages sparsity in the final estimates. Notice that $l _ { 0 }$ norm induces no shrinkage on the actual values of the parameters, which is in contrast to $l _ { 1 }$ regularization [23].

However, as the optimization of hard feature selection with binary masks suffers from high variance, we propose a secure Gaussian-based continuous relaxation for the Bernoulli variables for VFL. We approximate each element of $s _ { m } , q _ { m }$ to clipped Gaussian random variables parameterized by $\mu _ { m } , \omega _ { m }$ as $s _ { m , i } = \operatorname* { m a x } ( 0$ , min $( 1 , \mu _ { m , i } + \rho _ { m , i } ) ) , q _ { m , j } =$ max(0, min(1, ωm,j + γm,j)), where $\rho _ { m , i } , \gamma _ { m , j }$ are drawn from ${ \mathcal { N } } ( 0 , \sigma ^ { 2 } )$ , and $\mu _ { m , i } , \omega _ { m , j }$ can be learned during VFL training. Under the continuous relaxation, the regularization term in Eq. (3) is simply the sum of the probabilities that $\begin{array} { r } { \sum _ { i \in [ d _ { m } ] } P ( s _ { m , i } > 0 ) + \sum _ { j \in [ d _ { m } ] } P ( q _ { m , j } > 0 ) } \end{array}$ , and can be calculated by $\begin{array} { r } { \sum _ { i \in [ d _ { m } ] } \Phi ( \frac { \hat { \mu _ { m , i } } } { \sigma } \overline { { \Big ) \ + \ \sum _ { j \in [ d _ { m } ] } \Phi ( \frac { \omega _ { m , j } } { \sigma } ) } } } \end{array}$ , where $\Phi ( \cdot )$ is the cumulative distribution function (CDF) of the standard Gaussian distribution. By employing the continuous distribution, we can thus transform Eq. (3) into the following:

![](images/93fef917b0a00d6a51954b2d588548f6466781fef47d00028e0a91e853398ec0.jpg)



![](images/bd7a084ff44085dcc3a49058eb2f66d7ea5cb4f3646adfedc7f6fd4d5b153040.jpg)



(a) Ratio of the same selected fea- (b) Comparison of the original gate tures by stochastic gate and Gini method and FedSDG-FS impurity   
Fig. 3. Example motivation of FedSDG-FS design. The vertical neural network is trained on the dataset MADELON.

$$
\begin{array}{l} R (\boldsymbol {\theta}, \mu , \omega) := \mathbb {E} _ {X, Y} L (h (\theta_ {0}, g _ {n, 1}, \dots , g _ {n, M}); y _ {n}) \\ + \lambda \left(\sum_ {m, i} \Phi \left(\frac {\mu_ {m , i}}{\sigma}\right) + \sum_ {m, j} \Phi \left(\frac {\omega_ {m , j}}{\sigma}\right)\right). \tag {4} \\ \end{array}
$$

To optimize the objective of Eq. (4), we first differentiate it with respect to $\mu _ { m } , \omega _ { m }$ . However, since the loss L of the global model is calculated and stored at the server S, client m performs the differentiation using chain rules [32] based on the Monte Carlo sampling gradient estimator, e.g., for $\mu _ { m } \colon$

$$
\frac {1}{C} \sum_ {i \in [ C ]} \left[ \frac {\partial L _ {n}}{\partial g _ {n , m}} \cdot \frac {\partial g _ {n , m}}{\partial s _ {m}} \cdot \frac {\partial s _ {m , i}}{\partial \mu_ {m , i}} \right] + \lambda \frac {\partial}{\partial \mu_ {m}} \Phi \left(\frac {\mu_ {m}}{\sigma}\right) \tag {5}
$$

where C is the number of Monte Carlo samples. The calculation of gradient of estimator for $\omega _ { m }$ is similar to Eq. (5). Thus, we can update $\mu _ { m } , \omega _ { m }$ via stochastic gradient descent.

Updating the parameters and conducting the above operations require access to all local training samples or training process, which are, however, obfuscated from any third party including the server. In addition, directly applying the stochastic gates to the clients’ inputs would require a large number of parameters to be trained $( e . g . , \ \mu _ { m } , \ m \ \in \ [ M ] )$ , which slows down the convergence of the global model, and incurs significant computation and communication overhead, especially for high-dimension features.

To address this challenge, we propose an efficient and secure feature selection framework, FedSDG-FS, which leverages Gini impurity for VFL to initialize the importance of individual features to facilitate feature selection. Then important features and significant local embeddings can be selected by the proposed stochastic dual gates, enhanced with PHE and the randomized noisy mechanism for privacy preservation. To illustrate the motivation of the importance initialization, we make the following empirical observations. Firstly, as illustrated in Fig. 3(a), there can be a large ratio of the same features being selected by the Gini impurity [14] and by the stochastic gates in some training rounds. Secondly, Gini impurity initialization can speed up feature selection (Fig. 3(b)). Moreover, the reason that Gini impurity cannot be directly used for feature selection is that it cannot take into account the specific VFL models and has no prior knowledge of the number of important features to select. The feature importance initialization step can be accomplished by FedSDG-FS through two parameter transmissions with two encryption/decryption operations on the server based on Gini impurity and PHE, which significantly improves efficiency and privacy preservation. In this way, we can achieve efficient and secure feature selection as well as construct the global VFL model with high inference accuracy and fast convergence.

Algorithm 1: Feature Importance Initialization for VFL   
Input : Server S, clients m
Output: Initialized feature importance
1 Server S
2 Generate an indicator matrix A, $\llbracket A\rrbracket \leftarrow Enc(A)$ 3 Send $\llbracket A\rrbracket$ to all clients
4 Client m
5 Induce a partition $U_{m,1} \cup U_{m,2} \cup \cdots \cup U_{m,b}$ of $U_{m}$ 6 Calculate $\llbracket p_{m,k}\rrbracket \leftarrow \sum_{a \in I(U_{m,i})}\llbracket A\rrbracket_{a,k}/|U_{m,i}|$ 7 Calculate $\llbracket p_{m,k}\rrbracket^{2}$ with the protocol in [33]
8 $\llbracket G(U_{m,i})\rrbracket \leftarrow 1 - \sum_{k \in [c]}\llbracket p_{m,k}\rrbracket^{2}$ 9 $\llbracket G(f_{m,j})\rrbracket \leftarrow \sum_{i=1}^{c} \frac{|U_{m,i}|}{|U_{m}|} \cdot \llbracket G(U_{m,i})\rrbracket$ 10 Send $\llbracket G(f_{m,j})\rrbracket, j \in [d_{m}]$ to the server
11 Server S
12 $G(f_{m,j}) \leftarrow Dec(\llbracket G(f_{m,j})\rrbracket)$ 13 Send $G(f_{m,j}), j \in [d_{m}]$ to client m
14 Client m
15 Initialize $\mu_{m,j} \propto \frac{1}{G(f_{m,j})}$ 16 Return feature importance initialization $\mu_{m,j}, j \in [d_{m}]$

# C. Feature Importance Initialization

M clients have a set $U = \{ U _ { 1 } , \cdots , U _ { M } \}$ of N samples, and the corresponding c class labels are stored at the server. For client m, if the j-th feature $f _ { m , j }$ is a discrete feature that can assume b values, then it induces a partition $U _ { m , 1 } \cup \cdots \cup U _ { m , b }$ of the set $U _ { m }$ in which $U _ { m , i }$ is the set of instances with the i-th value for $f _ { m , j } .$ The Gini impurity of $U _ { m , i }$ is defined as $\begin{array} { r } { G ( U _ { m , i } ) = 1 - \bar { \sum } _ { k \in [ c ] } p _ { m , k } ^ { 2 } } \end{array}$ , where $p _ { m , k }$ is the probability of a randomly selected instance from $U _ { m , i }$ belonging to the k-th class. The Gini score of feature $f _ { m , j }$ is calculated as G(fm,j ) = Pi∈[b] m $\begin{array} { r } { G ( f _ { m , j } ) = \sum _ { i \in [ b ] } \frac { | U _ { m , i } | } { | U _ { m } | } \cdot G ( U _ { m , i } ) } \end{array}$ |Um,i||U | · G(Um,i), where G(fm,j ) measures $G ( f _ { m , j } )$ the likelihood of a randomly selected instance being misclassified. If $f _ { m , j }$ is a feature with continuous values, then $G ( f _ { m , j } )$ is defined as the weighted average of the Gini impurities of a set of discrete feature values. We use the Paillier as the PHE method which supports homomorphic addition of two ciphertexts and homomorphic multiplication between a plaintext and a ciphertext. The calculation of $p _ { m , k }$ requires collaboration between client m and the server. Thus, we design an efficient and secure collaborative calculation protocol.

Specifically, the server first generates an indicator matrix A with a size of $N \times c ,$ where $A _ { n , k } = 1$ indicates the category of the n-th sample is k; otherwise, $A _ { n , k } = 0$ . Then, the probability $p _ { m , k }$ can be calculated as $\begin{array} { r } { p _ { m , k } = \sum _ { a \in I ( U _ { m , i } ) } A _ { a , k } / | U _ { m , i } | } \end{array}$ for client $m ,$ , where $I ( U _ { m , i } )$ denotes the index set of instances from $U _ { m , i } .$ To prevent the private label information from being leaked, the server encrypts the matrix A, and sends [[A]] to all clients. Then, client m calculates the probability $\begin{array} { r } { \mathbb { \bar { [ { p _ { m , k } } ] } } ~ = ~ \sum _ { a \in I ( U _ { m , i } ) } \mathbb { [ } A ] \mathbb { ] } _ { a , k } / | U _ { m , i } | } \end{array}$ and uses the protocol in [33] to compute the square of $[ [ p _ { m , k } ] ]$ as follows. Firstly, client m generates a random value r and computes $[ [ u _ { m , k } ] ] =$ $[ [ p _ { m , k } + r ] ]$ , such that $p _ { m , k } ^ { 2 }$ equals $u _ { m , k } ^ { 2 } - 2 u _ { m , k } \cdot r + r ^ { 2 }$ and $[ - 2 u _ { m , k } \cdot r + r ^ { 2 } ]$ can be locally computed by the client. Then, client m sends $[ [ u _ { m , k } ] ]$ to the server. The server decrypts it, computes and sends $\mathbb { [ } u _ { m , k } ^ { 2 } ]$ to client m. Finally, the client computes $[ [ p ^ { 2 } ] ] = [ [ u _ { m , k } ^ { 2 } - 2 u _ { m , k } \cdot r + r ^ { 2 } ] ]$ . After calculating $[ [ p ^ { 2 } ] ]$ , client m calculates the Gini impurity $\mathbb { [ } G ( f _ { m , j } ) ]$ of feature $f _ { m , j }$ , and sends them to the server. The server then decrypts them, and assigns larger initial importance values to features with smaller Gini values. During this process, only the server learns the Gini scores of client m’s features, while other parties learn nothing. The main steps are shown in Algorithm 1.

# D. Secure Important Feature Selection

1) Forward Propagation on Clients: Client m randomly selects a private datum (or mini-batch) $x _ { n , m }$ , and calculates the indicator $s _ { m , i }$ for each feature $f _ { m , i } , ~ i \in [ d _ { m } ]$ . Then, it calculates the embedding vector $h _ { n , m }$ using the local model $\theta _ { m }$ and the masked embedding $g _ { h , m } ~ = ~ h _ { n , m } \odot q _ { m }$ , and encrypts it with PHE to obtain $[ { g } _ { n , m } ] = E n c ( { g } _ { n , m } )$ , which is sent to the server. 2) Forward Propagation on the Server: After receiving the encrypted embedding $[ [ g _ { n , m } ] ]$ , the server calculates the weighted vector $[ [ z _ { n , m } ] ] \ = \ [ [ g _ { n , m } ] ] \odot w _ { m } ,$ , and performs the forward propagation of the top model. Since the non-linear activation function on the top model cannot be calculated on the encrypted data, the weighted vector $\mathbb { I } z _ { n , m } ]$ should be sent back to client m for decryption. However, sending the weighted vector directly without any protection would leak the prediction to the client (e.g., client m can use the activation prediction pair $\left( z _ { n , m } , g _ { n , m } \right)$ to infer activation values and weights of the top model). To prevent this, the server adds random noises $\epsilon _ { s }$ on $\mathbb { I } z _ { n , m } ]$ , and sends $[ [ z _ { n , m } + \epsilon _ { s } ] ]$ to client m. Then, client m decrypts the noisy weighted sum $[ \boldsymbol { z } _ { n , m } + \boldsymbol { \epsilon } _ { s } ]$ , and sends $z _ { n , m } + \epsilon _ { s }$ to the server. Finally, the server removes the noise and computes the activation for the next layer. The process repeats until the final layer is reached.

Another problem is that the server holds both $w _ { m }$ and $z _ { n , m } ,$ and can easily infer $h _ { n , m }$ via linear regression. To avoid this, the server should use the noisy weight $\widetilde { w } _ { m }$ to calculate the weighted vector $[ [ \widetilde { z } _ { n , m } ] ] \gets [ [ g _ { n , m } ] ] \odot \widetilde { w } _ { m }$ , where $\widetilde { w } _ { m } = w _ { m } +$ $\epsilon _ { a c c } , \epsilon _ { a c c }$ is generated by the client. The forward propagation for secure feature selection is shown in Algorithm 2.

3) Backward Propagation on the Server: To update the global model, two gradients need to be computed first, the loss gradients w.r.t. the weight of the interactive layer $\frac { \partial L _ { n } } { \partial w _ { m } }$ ∂wm , and the embedding vector $\frac { \partial L _ { n } } { \partial g _ { n , m } }$ ∂gn,m ∂Ln . Since these two gradients are linear transformations of either $g _ { n , m } \ \mathrm { o r } \ w _ { m }$ , both the server and client m can derive what they want to acquire via regression. To this end, we design the following secure backward propagation method.

Specifically, the server first calculates the following gradients: $\begin{array} { r } { \mathbb { [ \frac { \partial L _ { n } } { \partial w _ { m } } ] } , \frac { \partial \widetilde { L } _ { n } } { \partial g _ { n , m } } , \frac { \partial L _ { n } } { \partial \alpha _ { 0 } } } \end{array}$ ∂wm ∂gn,m , ∂Ln∂α . If the server updates [[wm]] by $[ [ w _ { m } ] ]$ [[wm]] = wm − ηm[[ ∂wm ]] $\begin{array} { r l r } { \mathbb { \left[ w _ { m } \right] } } & { { } = } & { w _ { m } - \eta _ { m } \mathbb { I } \frac { \partial L _ { n } } { \partial w _ { m } } \mathbb { I } } \end{array}$ ∂Ln , this would result in two encrypted quantities in calculating the weighted vector $z _ { n , m } =$ $[ [ w _ { m } ] ] [ g _ { n , m } ]$ , which is incompatible with PHE. To avoid this, the server needs to send $[ \frac { \dot { \sigma } L _ { n } } { \partial w _ { m } } ]$ ∂wm to client $m ,$ , and receive the decrypted gradient ∂Ln∂wm back. However, sending [[ ∂Ln∂wm ]] $\frac { \partial L _ { n } } { \partial w _ { m } }$ dwm $[ [ \frac { \partial L _ { n } } { \partial w _ { m } } ] ]$ [L directly to client m would leak information about both parties, because the server holds $\frac { \partial L _ { n } } { \partial z _ { n , m } }$ and client m holds $h _ { n , m }$ . Thus, ∂zn,m both the server and client m need to add random noises to the encrypted gradient of weights $\frac { \partial L _ { n } } { \partial z _ { n , m } }$ ∂Ln∂z before sending them to n,m the other party, and update the parameters (see lines 4-10 of Algorithm 3). Note that the noise $\epsilon _ { s }$ generated by the server can be removed when the gradient $\frac { \partial  { \widetilde { L } } _ { n } } { \partial w _ { m } }$ ∂wm ∂Ln still contains noise,

Algorithm 2: Forward Propagation for Secure Feature Selection   
Input : M clients with N samples $\{x_{n}, y_{n}\}_{n=1}^{N}$ , $x_{n,m} \in R^{d_m}$ Output: Global model $\hat{\theta}$ , indicator vector $\{s_m\}_{m=1}^M$ 1 Initialize model $\theta_0 := \{\alpha_0, w_1, w_2, \cdots, w_M\}$ , $\{\theta_i\}_{i=1}^M$ , noise $\epsilon_{acc}$ ; initialize $\mu_m$ with Algorithm 1, $\omega_m \in R^{d_m}$ 2 Client m, $m \in [M]$ 3 Select datum (or data mini-batch) $x_{n,m}$ 4 Sample $\rho_{m,i}, \gamma_{m,j} \sim \mathcal{N}(0, \sigma^2)$ , $i \in [d_m]$ , $j \in [\underline{d_m}]$ 5 Compute $s_{m,i} = \max(0, \min(1, \mu_{m,i} + \rho_{m,i}))$ 6 $q_{m,j} = \max(0, \min(1, \omega_{m,j} + \gamma_{m,j}))$ 7 $R_m = \sum_{i \in [d_m]} \Phi\left(\frac{\mu_{m,i}}{\sigma}\right) + \sum_{j \in [\underline{d}_m]} \Phi\left(\frac{\omega_{m,j}}{\sigma}\right)$ 8 $h_{n,m} \leftarrow h_m(\theta_m; x_{n,m} \odot s_m), g_{n,m} = h_{n,m} \odot q_m$ 9 $[[g_{n,m}]] \leftarrow Enc(g_{n,m})$ , sends $[[g_{n,m}]]$ to the server

10 Server S

11 Calculate the noisy weight $\widetilde{w}_m \leftarrow w_m + \epsilon_{acc}$ , $m \in [M]$ 12 Compute $[[\widetilde{z}_{n,m}]] \leftarrow [[g_{n,m}]] \cdot \widetilde{w}_m$ 13 Add random noise $[[\widetilde{z}_{n,m} + \epsilon_s]] \leftarrow [[\widetilde{z}_{n,m}]] + \epsilon_s$ 14 Send $[[\widetilde{z}_{n,m} + \epsilon_s]]$ to client m

15 Client m, $m \in [M]$ 16 $\widetilde{z}_{n,m} + \epsilon_s \leftarrow Dec([[\widetilde{z}_{n,m} + \epsilon_s])$ 17 Remove noise $z_{n,m} + \epsilon_s \leftarrow \widetilde{z}_{n,m} + \epsilon_s - \epsilon_{acc} g_{n,m}$ 18 Send $z_{n,m} + \epsilon_s$ to the server

19 Server S

20 Remove noise $z_{n,m} \leftarrow z_{n,m} + \epsilon_s - \epsilon_s$ 21 Compute $L_n \leftarrow L(h(\alpha_0, z_{n,1}, \cdots, z_{n,M}); y_n)$ 22 Return the loss $L_n$

where $\begin{array} { r } { \frac { \partial \widetilde { L } _ { n } } { \partial w _ { m } } = \frac { \partial L _ { n } } { \partial w _ { m } } - \frac { \epsilon _ { m } } { \eta _ { 0 } } } \end{array}$ ∂Ln ϵm . With $\frac { \partial \widetilde { L } _ { n } } { \partial w _ { m } }$ ∂Ln , the server updates the ∂wm ∂wm η0 ∂wm weights as $\begin{array} { r } { \widetilde { w } _ { m } ^ { t + 1 } = w _ { m } ^ { t } - \eta ( \frac { \partial L _ { n } } { \partial w _ { m } } - \frac { \epsilon _ { m } } { \eta _ { 0 } } ) = w _ { m } ^ { t + 1 } + \epsilon _ { m } . } \end{array}$ wt+m = w tm − η( ∂w ∂Ln ϵm η0 = wt+1 + ϵm.

It can be observed that the noise $\epsilon _ { m }$ will accumulate in weights $w _ { m }$ in each iteration. If we take the accumulated noise as $\begin{array} { r } { \dot { \epsilon } _ { a c c } = \sum _ { m = 1 } ^ { M } \sum _ { i = 1 } ^ { t } \epsilon _ { m } ^ { i } } \end{array}$ , the true weights used in forward and backward propagation should be $w _ { m } ^ { \overline { { { t } } } + 1 } = \widetilde { w } _ { m } ^ { t + 1 } - \epsilon _ { a c c } .$ eTo perform the correct forward operation, client m needs to remove the noise by subtracting $g _ { n , m } \epsilon _ { a c c }$ from the noisy weighted vector $\widetilde { z } _ { n , m }$ . Similarly, the extra noise should be added to $\frac { \partial \widetilde { L } _ { n } } { \partial g _ { n , m } }$ ∂gn,m , and removed before backpropagation by client m. To achieve this, client m needs to send the encrypted noise $[ [ \epsilon _ { a c c } ] ]$ to the server, and the server calculates the true gradient via $\begin{array} { r } { \mathbb { \bar { \mathbb { I } } } _ { \partial g _ { n , m } } ^ { - } \mathbb { I } = \frac { \partial \widetilde { L } _ { n } } { \partial g _ { n , m } } - \mathbb { \bar { \mathbb { I } } } \epsilon _ { a c c } \mathbb { I } \cdot \frac { \partial L _ { n } } { \partial z _ { n , m } } } \end{array}$ ∂gn,m ∂Len∂g − [[ϵacc]] · ∂Ln∂z , n,m and sends the encrypted gradient $\mathbb { I } _ { \partial g _ { n , m } } ^ { \partial L _ { n } } \big ] \|$ to the client m. ∂gn,m

4) Backward Propagation on Clients: The client m first decrypts the gradient $\Big [ \frac { \breve { \partial } L _ { n } } { \partial g _ { n , m } } \Big ] \Big ]$ [[ ∂gn,m received from the server. Then, it updates the local model $\ddot { \theta } _ { m }$ and the variable $\mu _ { m } , \omega _ { m }$ . In this way, model update and feature selection can be accomplished simultaneously. The entire secure backpropagation approach is detailed in Algorithm 3.

Algorithm 3: Backward Propagation for Secure Feature Selection   
Input : Loss $L_{n}$ on the server, target $\{y_{n}\}_{n=1}^{N}$ , learning rates $\eta_{0}$ , $\eta_{m}$ Output: Global model $\hat{\theta}$ , indicator vector $s_{m}, q_{m}, m \in [M]$ 1 Server S

2 Compute the gradients $\left[\frac{\partial L_{n}}{\partial w_{m}}\right] \leftarrow \frac{\partial L_{n}}{\partial z_{n,m}} \cdot \left[g_{n,m}\right]$ , $\frac{\partial \widetilde{L}_{n}}{\partial g_{n,m}} \leftarrow \frac{\partial L_{n}}{\partial z_{n,m}} \cdot \widetilde{w}_{m}, \frac{\partial L_{n}}{\partial \alpha_{0}}$ 3 Add noise $\left[\frac{\partial L_{n}}{\partial w_{m}} + \epsilon_{s}\right] \leftarrow \left[\frac{\partial L_{n}}{\partial w_{m}}\right] + \epsilon_{s}$ 4 Send $\left[\frac{\partial L_{n}}{\partial w_{m}} + \epsilon_{s}\right]$ to client m

5 Client $m \in [M]$ 6 $\frac{\partial L_{n}}{\partial w_{m}} + \epsilon_{s} \leftarrow Dec\left(\left[\frac{\partial L_{n}}{\partial w_{m}} + \epsilon_{s}\right]\right)$ 7 Add noise $\frac{\partial \widetilde{L}_{n}}{\partial w_{m}} + \epsilon_{s} \leftarrow \frac{\partial L_{n}}{\partial w_{m}} + \epsilon_{s} - \frac{\epsilon_{m}}{\eta_{0}}$ 8 Encrypt noise $\left[\epsilon_{acc}\right] \leftarrow Enc(\epsilon_{acc})$ 9 Accumulate noise $\epsilon_{acc} \leftarrow \epsilon_{acc} + \epsilon_{m}$ 10 Send $\frac{\partial \widetilde{L}_{n}}{\partial w_{m}} + \epsilon_{s}$ , and $\left[\epsilon_{acc}\right]$ to the server

11 Server S

12 Remove noise $\frac{\partial \widetilde{L}_{n}}{\partial w_{m}} \leftarrow \frac{\partial \widetilde{L}_{n}}{\partial w_{m}} + \epsilon_{s} - \epsilon_{s}$ 13 Update $\theta_{0} = \{w_{1}, \cdots, w_{m}, \alpha_{0}\}$ : $\widetilde{w}_{m} \leftarrow \widetilde{w}_{m} - \eta_{0} \frac{\partial \widetilde{L}_{n}}{\partial w_{m}}, \alpha_{0} \leftarrow \alpha_{0} - \eta_{0} \nabla_{\alpha_{0}} L_{n}$ 14 Remove noise $\left[\frac{\partial L_{n}}{\partial g_{n,m}}\right] \leftarrow \frac{\partial \widetilde{L}_{n}}{\partial g_{n,m}} - \left[\epsilon_{acc}\right] \cdot \frac{\partial L_{n}}{\partial z_{n,m}}$ 15 Send $\left[\frac{\partial L_{n}}{\partial g_{n,m}}\right]$ to client m

16 Client $m \in [M]$ 17 $\frac{\partial L_{n}}{\partial g_{n,m}} \leftarrow [Dec\left(\left[\frac{\partial L_{n}}{\partial g_{n,m}}\right]\right)$ 18 Calculate $\frac{\partial L_{n}}{\partial \mu_{m}}, \frac{\partial L_{n}}{\partial \omega_{m}}, \frac{\partial L_{n}}{\partial \theta_{m}}$ 19 Update $\mu_{m} \leftarrow \mu_{m} - \eta_{m}\left(\frac{\partial L_{n}}{\partial \mu_{m}} + \lambda\frac{\partial R_{m}}{\partial \mu_{m}}\right)$ 20 $\omega_{m} \leftarrow \omega_{m} - \eta_{m}\left(\frac{\partial L_{n}}{\partial \mu_{m}} + \lambda\frac{\partial R_{m}}{\partial \omega_{m}}\right), \theta_{m} \leftarrow \theta_{m} - \eta_{m} \frac{\partial L_{n}}{\partial \theta_{m}}$ 21 Return the global model $\theta = \{\theta_{m}\}_{m=0}^{M}$ .

# E. Convergence Analysis

We present convergence results for FedSDG-FS through two steps. First, we show that there is an equivalence between our proposed $l _ { 0 }$ constrained optimization for feature selection and optimization over Bernoulli distribution through Mutual Information (MI). Then, we present the convergence results of the gradient decent methods for optimizing the $l _ { 0 }$ constrained optimization. Without loss of generality, we only consider the bottom level stochastic gates here. The goal of feature selection is to find the subset of features Q that has the highest MI with the target variable Y . We can then formulate the task as selecting $Q$ such that the MI I(·) between $X _ { Q }$ and Y is maximized:

$$
\max _ {Q} I (X _ {Q}, Y) \quad s. t. \quad | Q | = k. \tag {6}
$$

Then, under the mild assumption that there exists an optimal subset of indices $Q ^ { * }$ , the equation above is equivalent to

$$
\max _ {\mathbf {0} \leq \pi \leq 1} I (X \odot \tilde {Q}; Y) \quad s. t. \quad \sum_ {i} \mathbb {E} \left[ \tilde {Q} _ {i} \right] \leq k, \tag {7}
$$

where $\tilde { Q }$ are independently sampled from the Bernoulli distribution with parameter π. Then, we can rewrite this constrained optimization problem as a penalty optimization problem, which is the same as Eq. (3):

$$
R = \min L (X \odot \tilde {Q}; Y) + \lambda | \tilde {Q} | \tag {8}
$$

So far, we have proved the equivalence between the proposed $l _ { 0 }$ constrained optimization and the selection of the optimal feature subset. Next, we give the convergence results of the $l _ { 0 }$ constrained optimization for feature selection.

Assumption 1. The gradient $\frac { \partial R ( \theta ) } { \partial \theta _ { 0 } }$ is K-Lipschitz continuous, and $\frac { \partial R ( \pmb \theta ) } { \partial \theta _ { m } } , m \in [ M ]$ is $K _ { m } – I$ ipschitz continuous.

Theorem 1. Under Assumption 1, and the assumption that $R ( \theta )$ is ρ-strongly convex, if $\begin{array} { r } { \eta ^ { t } ~ = ~ \frac { 1 } { \rho \operatorname* { m i n } _ { m } ( t + T _ { 0 } ) } } \end{array}$ with the constant $T _ { 0 } > 0$ . Then the convergence rate is $\mathcal { O } ( 1 / T )$ .

Time and storage coity of the algorithm is $\begin{array} { r } { \mathcal { O } ( \frac { K | | \theta _ { 0 } - \hat { \theta } | | ^ { 2 } } { 2 \epsilon } ) , \epsilon = \frac { 1 } { 2 ( \eta ^ { t } + \eta _ { m } ^ { t } ) T } ( | | \theta _ { 0 } - \frac { } { } } \end{array}$ ${ \hat { \theta } } | | ^ { 2 } )$ . The storage complexity is $\mathcal { O } ( \left| \theta \right| + \left| s \right| + \left| q \right| )$ , where $| \cdot |$ denotes the parameter size, and the communication cost is $\mathcal { O } \left( \vert q \vert ^ { \underline { { K \vert \vert \theta _ { 0 } - ^ { * } \hat { \theta } \vert \vert ^ { 2 } } } } \right)$ .

# V. EXPERIMENTAL EVALUATION

# A. Experiment Configuration

1) Datasets. We use 9 datasets with 4 types of data: tabular data, images, texts and audios. These include 2 synthetic datasets, MADELON [31] and FRIEDMAN [34]; and 7 realworld datasets, ARCENE [30], BASEHOCK [35], RELATHE [35], PCMAC [35], GISETTE [36], COIL20 [37] and ISOLET [38]. The synthetic datasets are derived from the feature selection challenge [31], where MADELON consists of 5 informative features, 15 redundant features constructed by linear combinations of those 5 informative features, and 480 noisy features, while FRIEDMAN consists of 5 informative and 995 noisy features. For the real-world datasets, most of them are collected from the ASU feature selection database online [35]. The descriptions of all datasets are listed in Table I. We employ two clients in our settings, where we divide features into two parts randomly for every dataset, and assign each part to clients A and B. The labels are located in the server. For the text, image and audio datasets, we divide the features randomly by rows for the clients.

TABLE I DESCRIPTION OF DATASETS FOR EMPIRICAL EVALUATIONS 

<table><tr><td>Dataset</td><td>Features</td><td>Train size</td><td>Test size</td><td>Classes</td><td>Type</td></tr><tr><td>MADELON</td><td>500</td><td>2,000</td><td>2,400</td><td>2</td><td>Tabular</td></tr><tr><td>FRIEDMAN</td><td>1,000</td><td>750</td><td>250</td><td>2</td><td>Tabular</td></tr><tr><td>ARCENE</td><td>10,000</td><td>1,400</td><td>600</td><td>2</td><td>Tabular</td></tr><tr><td>BASEHOCK</td><td>7,862</td><td>1,594</td><td>398</td><td>2</td><td>Text</td></tr><tr><td>RELATHE</td><td>4,322</td><td>2,320</td><td>2,088</td><td>2</td><td>Text</td></tr><tr><td>PCMAC</td><td>3,289</td><td>1,554</td><td>388</td><td>2</td><td>Text</td></tr><tr><td>GISETTE</td><td>5,000</td><td>5,600</td><td>1,400</td><td>2</td><td>Image</td></tr><tr><td>COIL20</td><td>1,024</td><td>1,008</td><td>432</td><td>20</td><td>Image</td></tr><tr><td>ISOLET</td><td>617</td><td>1,248</td><td>312</td><td>26</td><td>Audio</td></tr></table>

2) VFL Models. We have implemented the typical logistic regression model for VFL [39] on FRIEDMAN, and neural networks for VFL [25] on the other 8 datasets (see Table II). We run VFL models until a pre-specified test accuracy is reached, or a maximum number of iterations has elapsed. In addition, training the dual-gates until convergence may sometimes cause overfitting of the model, where we set the cutoff value of the variables and perform early stopping. We use the Paillier as the PHE method. We use the Adam optimizer, and set learning rate $\eta = 0 . 0 3$ , batch size $b = 1 2 8$ , weight factor $\lambda = 0 . 1$ . We test the accuracy of the global model on the hold-out test datasets. We build our VFL models with Flower 0.19.0 [40] and Pytorch 1.8.1 [41]. All the experiments are performed on Ubuntu 16 operating system equipped with a 12-core i7 Intel CPU, 64G of RAM and 4 Titan X GPUs.

TABLE II SETTINGS FOR TRAINING DIFFERENT VFL MODELS. 

<table><tr><td>Model</td><td># of parameters</td><td>Task</td></tr><tr><td>VFLNN-MADELON</td><td>130,552</td><td>Two-class classification</td></tr><tr><td>VFLLR-FRIEDMAN</td><td>130,501</td><td>Regression</td></tr><tr><td>VFLNN-ARCENE</td><td>1,030,552</td><td>Cancer detection</td></tr><tr><td>VFLNN-BASEHOCK</td><td>516,752</td><td>Text classification</td></tr><tr><td>VFLNN-RELATHE</td><td>462,752</td><td>Text classification</td></tr><tr><td>VFLNN-PCMAC</td><td>359,452</td><td>Text classification</td></tr><tr><td>VFLNN-GISETTE</td><td>530,552</td><td>Digit number recognition</td></tr><tr><td>VFLNN-COIL20</td><td>109,360</td><td>Face image recognition</td></tr><tr><td>VFLNN-ISOLET</td><td>93,476</td><td>Letter-name recognition</td></tr></table>

# B. Evaluating Gini Impurity for VFL

Firstly, we evaluate the effectiveness of our Gini impurity metric (FedSDG-FS-gini) designed for feature importance initialization in FedSDG-FS by comparing the test accuracy of the global models to the other three filtering based feature selection strategies, SFFS [17], random FS, and all features participating (allFeatures). We select different numbers of features (i.e., k features with the smallest Gini scores), and assign them to the two clients. Since those datasets differ in both the number of features and the number of noisy features. Thus, we select features from each dataset in similar proportions and round the numbers of selected features. We perform 5-fold cross validation and report the average $R ^ { 2 }$ scores, test accuracy and standard deviations in Fig. 4. Here, the $R ^ { 2 }$ score is defined as $\begin{array} { r } { R ^ { 2 } \ = \ 1 - \ \frac { \sum _ { n \in [ N ] } ( y _ { n } - \tilde { y _ { n } } ) ^ { 2 } } { \sum _ { n \in [ N ] } ( y _ { n } - \bar { y } ) } } \end{array}$ Pn∈[N](yn−yˆn)2 Pn∈[N](yn−y¯) , where y¯ = 1N Pn∈[N ] yn, $\begin{array} { r } { \bar { y } \ = \ \frac { 1 } { N } \sum _ { n \in [ N ] } y _ { n } , } \end{array}$ and $y _ { n } , \hat { y } _ { n }$ are the true target and predicted target of the nth sample, respectively. The results show that FedSDG-FSgini achieves higher test accuracy and $R ^ { 2 }$ scores than other strategies. Specifically, the average test accuracy and $R ^ { 2 }$ scores of FedSDG-FS-gini are 28.71%/ 123.8%, 29.69%/ 70.3%, 12.85%/ 3.4% higher than that of random, allFeatures and SFFS for MADELON and FRIEDMAN, respectively. Meanwhile, the standard deviations are relative small, e.g., with 1.22% and 4.3% smaller than that of SFFS for MADELON and FRIEDMAN. Besides, the reason why some of the test accuracy in Fig 4. is less than 50% is that there are noisy features irrelevant to the learning task and a large number of redundant features possessed by local clients, samples with very similar or the same features may have completely opposite labels.

![](images/4d4333c7ad9f6eeb363d904e87baea8b709b09fbe0958ca774b1077ff72655d5.jpg)



(a) VFLNN-MADELON

![](images/11c10a3301aeddb0d595a4c93f44feadb1bcd737bb5502aec73f432480308f39.jpg)



(b) VFLLR-FRIEDMAN   
Fig. 4. Test accuracy and $R ^ { 2 }$ scores vs. number of selected features on synthetic datasets.

![](images/4379a13514d62f459a3d3de3f93a7df847f3c060f23bceea1d124cbc2fb8278f.jpg)  
(a) VFLNN-ARCENE

![](images/6353cda6e379acd7227fd516f1eea4331f498fca81d5ba799261b07f62ce401e.jpg)



(b) VFLNN-GISETTE   
Fig. 5. Test accuracy vs. number of selected features by training models for 20 rounds.

![](images/e44df28b4544d80a3e83d36cba8ff3e80fcef9f5a476d08ed34e196db6d10c66.jpg)



(a) VFLNN-ARCENE

![](images/d5291a1f74c78e2be2ffedfb0da1c1fdef994423f8b7f8f35c7b8833eb9266f6.jpg)



(b) VFLNN-GISETTE

![](images/6c3007e12e4154695b352fdfb1814f94460e0b463dae2b90c97665026ec7901c.jpg)



(c) VFLNN-ARCENE

![](images/ff016e896b80eab71d3abe6123667fbde4c2599a8d894392dd8e27876080203d.jpg)



(d) VFLNN-GISETTE   
Fig. 6. Test accuracy and number of selected features during model training of original gate selection method and FedSDG-FS.

# C. Evaluating Important Feature Selection

After feature importance initialization, FedSDG-FS proceeds to select important features using the stochastic dualgates. We now evaluate our FedSDG-FS method compared to other baselines, all features participating (allFeatures), SFFS, VFLFS [24], and the original gate based method which has neither gates of the embedding vectors nor importance initialization (original-Gate), using various datasets. For fair comparison, we implement VFLFS [24] without the part that makes use of the non-overlapping samples. Further, we extend a filter feature selection method MS-GINI [14] based on Gini impurity in VFL settings to compare with FedSDG-FS. We perform 5-fold cross validation and report average accuracy.

1) Precision. We use precision to measure the accuracy of FedSDG-FS, which calculates the proportion of correctly selected informative features over all selected features. For FedSDG-FS and the original gate method, we train VFLNN-MADELONE until the model converges, and determine the important features. For SFFS and MS-GINI, we calculate the F-statistics and Gini impurity of each individual feature, respectively, and select different numbers of informative features. The results are shown in Fig 7. It can be observed that FedSDG-FS and the original gate method achieve much higher precision than allFeatures, SFFS, MS-GINI, and FedSDG-FS achieves the highest precision. This illustrates that reducing the sizes of embedding vectors does not degrade the model accuracy. For example, the average precision scores of different number settings of FedSDG-FS are 13% and 76% higher than the original gate method and SFFS, respectively. As the number of selected features increases, the precision of SFFS and MS-GINI decreases dramatically, while the presicion decreases slightly for the FedSDG-FS and original gate methods, which demonstrates the effectiveness of FedSDG-FS without knowing the number of features to be selected.

2) Learning Accuracy. We compare FedSDG-FS with others by training different VFL models and evaluating the test accuracy of the global models, and the ratios of selected features. The results are shown in Table III. It can be observed that FedSDG-FS achieves the highest test accuracy using the fewest features in almost all datasets. Taking MADELON as an example, the average test accuracy of FedSDG-FS is 0.3%, 33.6%, 27.0%, 47.2%, 50.2% higher than the four methods; while the ratio of selected features is 0.02, 0.97, 0.47, 0.47, 0.47 less than them. In some cases where there are small number of noisy features, and having little negative impact on the model, using all features results the higher accuracy. Nevertheless, FedSDG-FS can still achieve comparable test accuracy with fewer features. To further validate the proposed methods, we conducted experiments with five clients and ten clients. Two example results are presented in Table IV, which show that FedSDG-FS achieves the highest test accuracy using the fewest features in most cases. For the only case where FedSDG-FS performs second best in terms of accuracy, our accuracy 99.5% is very close to the best accuracy 99.8%, while FedSDG-FS use about 20% fewer features.

![](images/491dc814c304503fe567d4f1d5a40ea7a752240ffaa2e821cfc525c51bc554b7.jpg)



Fig. 7. Precision of different methods on MADELON.

![](images/59d8fd6443fcd62044afc0d3e2e84d49884df2609b7ab669ace0e719eb5ce92c.jpg)



Fig. 8. Communication cost for 100 samples.

TABLE III TEST ACCURACY OF MODELS TRAINED WITH FEATURES SELECTED. 

<table><tr><td>Datasets</td><td colspan="6">Test Accuracy (%) / Ratio of Selected Features</td></tr><tr><td></td><td>allFeatures</td><td>SFFS</td><td>MS-GINI</td><td>VFLFS</td><td>original-Gate</td><td>FedSDG-FS</td></tr><tr><td>MADELON</td><td>52.0/ 1.0</td><td>65.6/ 0.5</td><td>72.2/ 0.5</td><td>51.0/ 0.5</td><td>98.9/ 0.05</td><td>99.2/ 0.03</td></tr><tr><td>ARCENE</td><td>80.1/ 1.0</td><td>95.0/ 0.5</td><td>87.5/ 0.5</td><td>70.1/ 0.5</td><td>97.4/ 1.0</td><td>99.8/ 0.58</td></tr><tr><td>BASEHOCK</td><td>99.7/ 1.0</td><td>99.1/ 0.5</td><td>98.5/ 0.5</td><td>94.4/ 0.5</td><td>99.5/ 0.48</td><td>99.9/ 0.3</td></tr><tr><td>RELATHE</td><td>95.5/ 1.0</td><td>87.2/ 0.5</td><td>92.1/ 0.5</td><td>86.5/ 0.5</td><td>99.7/ 0.71</td><td>99.8/ 0.41</td></tr><tr><td>PCMAC</td><td>97.6/ 1.0</td><td>79.34/ 0.5</td><td>90.2/ 0.5</td><td>86.11/ 0.5</td><td>99.1/ 0.66</td><td>98.7/ 0.45</td></tr><tr><td>GISETTE</td><td>99.1/ 1.0</td><td>99.0/ 0.5</td><td>98.0/ 0.5</td><td>50.2/ 0.5</td><td>99.3/ 0.81</td><td>99.5/ 0.53</td></tr><tr><td>COIL20</td><td>96.4/ 1.0</td><td>65.6/ 0.5</td><td>94.8/ 0.5</td><td>72.2/ 0.5</td><td>91.2/ 1.0</td><td>97.5/ 0.71</td></tr><tr><td>ISOLET</td><td>98.0/ 1.0</td><td>92.7/ 0.5</td><td>91.4/ 0.5</td><td>71.4/ 0.5</td><td>93.2/ 1.0</td><td>96.7/ 0.75</td></tr></table>

TABLE IV TEST ACCURACY OF MODELS TRAINED WITH FEATURES SELECTED. 

<table><tr><td>Datasets</td><td colspan="6">Test Accuracy (%) / Ratio of Selected Features</td></tr><tr><td colspan="7">5 Clients</td></tr><tr><td></td><td>allFeatures</td><td>SFFS</td><td>MS-GINI</td><td>VFLFS</td><td>original-Gate</td><td>FedSDG-FS</td></tr><tr><td>ARCENE</td><td>85.8/ 1.0</td><td>92.2/ 0.5</td><td>92.0/ 0.5</td><td>71.0/ 0.5</td><td>98.2/ 1.0</td><td>99.7/ 0.59</td></tr><tr><td>RELATHE</td><td>97.6/ 1.0</td><td>84.8/ 0.5</td><td>92.7/ 0.5</td><td>86.1/ 0.5</td><td>99.8/ 0.69</td><td>99.5/ 0.45</td></tr><tr><td colspan="7">10 Clients</td></tr><tr><td></td><td>allFeatures</td><td>SFFS</td><td>MS-GINI</td><td>VFLFS</td><td>original-Gate</td><td>FedSDG-FS</td></tr><tr><td>ARCENE</td><td>91.0/ 1.0</td><td>94.0/ 0.5</td><td>92.7/ 0.5</td><td>82.0/ 0.5</td><td>98.6/ 1.0</td><td>99.2/ 0.56</td></tr><tr><td>RELATHE</td><td>97.5/ 1.0</td><td>85.6/ 0.5</td><td>93.6/ 0.5</td><td>85.7/ 0.5</td><td>99.5/ 0.68</td><td>99.8/ 0.44</td></tr></table>

3) Stability. We evaluate the stability of FedSDG-FS from two aspects, 1) test accuracy of the global model with different numbers of selected features, and 2) test accuracy at different training rounds. We illustrate the test accuracy of models VFLNN-ARCENE and VFLNN-GISETTE by training them for 20 rounds with different numbers of features in Fig. 5. The results show that compared to SFFS, the original based method and FedSDG-FS both achieve much higher test accuracy. The performance of FedSDG-FS has little variation in all cases. Then, we calculate the test accuracy of the two models in different training rounds, and plot them in Fig. 6(a) and Fig. 6(b). The results show that FedSDG-FS and the original gate method achieve comparably high test accuracies at different training rounds, while FedSDG-FS is more stable (i.e., the test accuracy of global model drops 2.8% in the 80-th round for FedSDG-FS and 17.9% for the original gate method). The analysis results of test accuracy on other models with different numbers of selected features and at different training rounds are similar to that of VFLNN-ARCENE, VFLNN-GISETTE.

4) Efficiency. Finally, we evaluate the efficiency of FedSDG-FS from two aspects: 1) the speed of the feature importance initialization, and 2) communication saving during model prediction. Firstly, we calculate the number of selected features in different rounds of training VFLNN-ARCENE and VFLNN-GISETTE (Fig. 6(c) and Fig. 6(d)). The results show that with importance initialization, the models can quickly filter out noisy features and select important ones, thus speeding up model training. Secondly, we compare the prediction communication overhead of those models of FedSDG-FS, allFeatures and the original gate method. Fig. 8 shows the average communication cost of each method to select features. The communication cost of FedSDG-FS is more than 50% lower than that of the other methods (e.g., 53.2%, 54.7% lower for datasets ARCENE and GISETTE). The efficiency analysis clearly demonstrated the advantages of the feature importance initialization module of FedSDG-FS.

# VI. CONCLUSIONS

In this work, we proposed an efficient and secure vertical federated learning feature selection framework to select important features in VFL settings. We first designed a Gaussian stochastic dual-gates for clients’ inputs to efficiently approximate the probability of a feature being selected. Then, we incorporated PHE and randomized noise mechanism into stochastic dual-gates to achieve secure feature selection. To reduce overhead, we proposed a feature importance initialization method based on Gini impurity and PHE, which can be accomplished through only two parameter transmissions, and two encryption/decryption operation on the server. Experiment results show that FedSDG-FS significantly outperforms existing approaches in terms of achieving more accurate selection of high-quality features and building global models with better performance. FedSDG-FS achieves the privacy protection goal, e.g., during the entire feature selection and model training process, neither data nor labels will be acquired or inferred by any party other than their original owners.

# ACKNOWLEDGMENTS

Han Yu is the corresponding author. This research is supported by Nanyang Technological University (NTU), under SUG Grant (020724-00001); the National Research Foundation, Prime Ministers Office, National Cybersecurity R&D Program (No. NRF2018NCR-NCR005-0001), NRF Investigatorship NRF-NRFI06-2020-0001; the National Research Foundation, Singapore and DSO National Laboratories under the AI Singapore Programme (AISG Award No: AISG2- RP-2020-019); Alibaba Group through Alibaba Innovative Research (AIR) Program and Alibaba-NTU Singapore Joint Research Institute (JRI) (Alibaba-NTU-AIR2019B1), NTU, Singapore; the RIE 2020 Advanced Manufacturing and Engineering Programmatic Fund (No. A20G8b0102), Singapore; NTU Nanyang Assistant Professorship, Future Communications Research & Development Programme (FCP-NTU-RG-2021-014), the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, and “the Fundamental Research Funds for the Central Universities” WK2150110024.

# REFERENCES

[1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial intelligence and statistics. PMLR, 2017, pp. 1273– 1282.   
[2] Y. Hu, D. Niu, J. Yang, and S. Zhou, “Fdml: A collaborative machine learning framework for distributed features,” in Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2019, pp. 2232–2240.   
[3] Q. Yang, Y. Liu, Y. Cheng, Y. Kang, T. Chen, and H. Yu, “Federated learning,” Synthesis Lectures on Artificial Intelligence and Machine Learning, vol. 13, no. 3, pp. 1–207, 2019.   
[4] J. Wang, L. Zhang, A. Li, X. You, and H. Cheng, “Efficient participant contribution evaluation for horizontal and vertical federated learning,” in 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 2022, pp. 911–923.   
[5] A. Li, L. Zhang, J. Wang, F. Han, and X.-Y. Li, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, vol. 33, no. 10, pp. 2291–2303, 2021.   
[6] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. M. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 372–383.   
[7] W. Zhuang, Y. Wen, and S. Zhang, “Joint optimization in edgecloud continuum for federated unsupervised person re-identification,” in Proceedings of the 29th ACM International Conference on Multimedia, 2021, pp. 433–441.   
[8] A. Li, L. Zhang, J. Tan, Y. Qin, J. Wang, and X.-Y. Li, “Sample-level data selection for federated learning,” in IEEE INFOCOM 2021-IEEE Conference on Computer Communications. IEEE, 2021, pp. 1–10.   
[9] Y. Liu, Y. Kang, L. Li, X. Zhang, Y. Cheng, T. Chen, M. Hong, and Q. Yang, “A communication efficient vertical federated learning framework,” Unknown Journal, 2019.   
[10] T. Chen, X. Jin, Y. Sun, and W. Yin, “Vafl: a method of vertical asynchronous federated learning,” arXiv preprint arXiv:2007.06081, 2020.   
[11] J. Tan, L. Zhang, Y. Liu, A. Li, and Y. Wu, “Residue-based label protection mechanisms in vertical logistic regression,” arXiv preprint arXiv:2205.04166, 2022.   
[12] PowerFL, “Angel powerfl,” https://data.qq.com/powerfl/.   
[13] FATE, “Fate-federated-ai,” https://github.com/FederatedAI/DOC-CHN.   
[14] X. Li, R. Dowsley, and M. De Cock, “Privacy-preserving feature selection with secure multiparty computation,” ICML 2021, 2021.   
[15] Y. Yamada, O. Lindenbaum, S. Negahban, and Y. Kluger, “Feature selection using stochastic gates,” in International Conference on Machine Learning. PMLR, 2020, pp. 10 648–10 659.   
[16] J. Chen, M. Stern, M. J. Wainwright, and M. I. Jordan, “Kernel feature selection via conditional covariance minimization,” NeurIPS 2017, 2017.   
[17] F. Pan, D. Meng, Y. Zhang, H. Li, and X. Li, “Secure federated feature selection for cross-feature federated learning,” 2020.   
[18] L. Song, A. Smola, A. Gretton, J. Bedo, and K. Borgwardt, “Feature selection via dependence maximization.” Journal of Machine Learning Research, vol. 13, no. 5, 2012.   
[19] P. A. Estevez, M. Tesmer, C. A. Perez, and J. M. Zurada, “Normalized ´ mutual information feature selection,” IEEE Transactions on neural networks, vol. 20, no. 2, pp. 189–201, 2009.   
[20] D. Roy, K. S. R. Murty, and C. K. Mohan, “Feature selection using deep neural networks,” in 2015 International Joint Conference on Neural Networks (IJCNN). IEEE, 2015, pp. 1–6.   
[21] M. M. Kabir, M. M. Islam, and K. Murase, “A new wrapper feature selection approach using neural network,” Neurocomputing, vol. 73, no. 16-18, pp. 3273–3283, 2010.   
[22] Y. Li, C.-Y. Chen, and W. W. Wasserman, “Deep feature selection: theory and application to identify enhancers and promoters,” Journal of Computational Biology, vol. 23, no. 5, pp. 322–336, 2016.   
[23] C. Hans, “Bayesian lasso regression,” Biometrika, vol. 96, no. 4, pp. 835–845, 2009.   
[24] C. Louizos, M. Welling, and D. P. Kingma, “Learning sparse neural networks through l0 regularization,” arXiv preprint arXiv:1712.01312, 2017.   
[25] Y. Zhang and H. Zhu, “Additively homomorphical encryption based deep neural network for asymmetrically collaborative machine learning,” arXiv preprint arXiv:2007.06849, 2020.

[26] K. Cheng, T. Fan, Y. Jin, Y. Liu, T. Chen, D. Papadopoulos, and Q. Yang, “Secureboost: A lossless federated learning framework,” IEEE Intelligent Systems, vol. 36, no. 6, pp. 87–98, 2021.   
[27] L. Song, A. Smola, A. Gretton, K. M. Borgwardt, and J. Bedo, “Supervised feature selection via dependence estimation,” in Proceedings of the 24th international conference on Machine learning, 2007, pp. 823–830.   
[28] G. I. Allen, “Automatic feature selection via weighted kernels and regularization,” Journal of Computational and Graphical Statistics, vol. 22, no. 2, pp. 284–299, 2013.   
[29] S. Feng, “Vertical federated learning-based feature selection with nonoverlapping sample utilization,” Expert Systems with Applications, p. 118097, 2022.   
[30] J. Thomas, “Mass spectrometric data.” [Online]. Available: https: //www.openml.org/d/41157   
[31] I. Guyon, S. Gunn, A. Ben-Hur, and G. Dror, “Result analysis of the nips 2003 feature selection challenge,” Advances in neural information processing systems, vol. 17, 2004.   
[32] A. Miller, N. Foti, A. D’Amour, and R. P. Adams, “Reducing reparameterization gradient variance,” Advances in Neural Information Processing Systems, vol. 30, 2017.   
[33] Z. Erkin, M. Franz, J. Guajardo, S. Katzenbeisser, I. Lagendijk, and T. Toft, “Privacy-preserving face recognition,” in International symposium on privacy enhancing technologies symposium. Springer, 2009, pp. 235–253.   
[34] J. H. Friedman, “Multivariate adaptive regression splines,” The annals of statistics, vol. 19, no. 1, pp. 1–67, 1991.   
[35] A. state university, “Feature selection datasets,” Public online, 2010. [Online]. Available: https://jundongl.github.io/scikit-feature/OLD/ datasets old.html   
[36] U. machine learning repository, “Handwritten digit recognition problem.” [Online]. Available: https://archive.ics.uci.edu/ml/datasets/ Gisette   
[37] C. University, “Image classification task.” [Online]. Available: https: //www.cs.columbia.edu/CAVE/software/softlib/coil-20.php   
[38] U. machine learning repository, “Letter-name classification task.” [Online]. Available: https://archive.ics.uci.edu/ml/datasets/isolet   
[39] S. Hardy, W. Henecka, H. Ivey-Law, R. Nock, G. Patrini, G. Smith, and B. Thorne, “Private federated learning on vertically partitioned data via entity resolution and additively homomorphic encryption,” arXiv preprint arXiv:1711.10677, 2017.   
[40] Flower, “Flower: A friendly federated learning framework,” Public online, 2022. [Online]. Available: https://flower.dev/   
[41] Pytorch, “Pytorch,” Public online, 2022. [Online]. Available: https: //pytorch.org/