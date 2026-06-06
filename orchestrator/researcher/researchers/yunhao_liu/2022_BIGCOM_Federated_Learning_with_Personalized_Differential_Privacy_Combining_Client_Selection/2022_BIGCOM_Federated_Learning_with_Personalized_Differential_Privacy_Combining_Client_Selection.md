# Federated Learning with Personalized Differential Privacy Combining Client Selection

Yunting Xie

School of Computer Science and Technology

University of Science and Technology of China

Hefei, China

yunting@mail.ustc.edu.cn

Lan Zhang

School of Computer Science and Technology

University of Science and Technology of China

Hefei, China

zhanglan@ustc.edu.cn

Abstract—Federated Learning(FL) enables clients to construct a global model collaboratively while protecting the security and privacy of clients’ datasets. Differential privacy(DP) is a common method to protect clients’ data privacy in FL. However, most of existing works assume the privacy needs of all clients are the same, which is rare in reality, making it difficult to apply their approaches to realistic scenarios. What’s more, existing works considering DP protection are not combined with client selection, which will result in clients with the same dataset quality but different added noise introduced by DP mechanism having the same chance of being selected, which is likely to harm model performance. In this work, we consider personalized DP(PDP) setting, i.e. each client has personal privacy need. We conduct a convergence analysis of FL with PDP and client selection. We find that for fast convergence and small bias, we prefer clients with high local loss and small added noise. Moreover, the influence of noise on the later stage of training is greater than that in the earlier stage. According to the analysis result, we propose a novel mechanism, containing a PDP mechanism combining sampling for small added noise while meeting the privacy needs of clients and a client selection mechanism with a novel metric score which considers the local loss and privacy needs of clients at the same time. Our experiments demonstrate that the performance of our mechanism is better than the baseline mechanism.

Index Terms—federated learning, personalized differential privacy, client selection

# I. INTRODUCTION

In recent years, the field of artificial intelligence is developing rapidly both in research and practical application. The success of these AI technologies depends on the support of the big data behind them. For example, Alpha Go, who defeated the top human Go players in 2016, used a total of 300,000 games as training data[1]. In practice, however, the vast amount of data is not held solely by one party. For example, for a rare disease, each hospital has very few case records, but the number of cases aggregated across multiple hospitals is very large. Meanwhile, the emphasis to data privacy and security has become a worldwide trend. For example, Facebook user data breach incident gets worldwide attention in 2018. For such issues, countries around the world have strengthened the legal protection of data privacy and data security. For example, the General Data Protection Regulation(GDPR)[2] enforced by European Union and Personal Information Protection Law of the People’s Republic of China[3] enforced by China. With the gradual improvement of relevant laws and regulations, companies gradually begin to pay more attention to user data privacy and security.

Federated learning[4; 5] was proposed in order to use multiparty data to jointly train the model while protecting the privacy and security of clients’ data. In federated learning setting, clients don’t send the origin datasets to server. Instead, Clients only send local model update to server in the training period. This is the key idea that federated learning can protect clients’ data. However, there are many works point out that uploading model parameters also exposes information about clients’ datasets [6; 7; 8]. Therefore, protecting user privacy is an important issue for federated learning.

Differential privacy(DP) is a common method for federated learning to protect clients’ data privacy. DP provides a rigorous privacy guarantee to clients’ data. At first, researchers focused on centralized DP setting, which assumes server is honest. For example in [9; 10], the proposed methods require server’s perturbation to protect clients’ datasets. However, centralized DP’s assumption of server is too strong to be applied in real scenarios. Therefore, local DP setting gets more attention due to the assumption of honest server is not required. The disadvantage of local DP compared to centralized DP is that it needs to add more perturbation to data. Works like [11; 12; 13] have proposed several local DP algorithms. However, these works still have shortcomings. For example, they assume that the privacy needs of all clients is same, which is rare in real scenarios. In reality, different people have different privacy needs. In the field of database, the concept of personalized differential privacy has been proposed[14; 15], which denotes every record in the database is owned by different users and the privacy need of it is personal. However, we care about different clients who own personal datasets have personal privacy needs in FL, which means this concept of PDP in database can’t be used in FL directly. Moreover, most of the existing works lack theoretical analysis on how DP mechanisms will affect the convergence of federated learning model. And existing work considering FL with DP are not combined with client selection. Large added noise have a large negative impact on the model effect. This will lead to clients with the same dataset quality but different added noise introduced by DP mechanism have the same chance of being selected.

In this work, we consider federated learning with personalized differential privacy setting, i.e. different clients have different privacy needs. Our work makes the following main contributions:

• We conduct a convergence analysis of federated learning with PDP and client selection. We find that for fast convergence and small bias, we prefer clients with large local loss and small noise added by PDP mechanism. What’s more, the influence of noise on the later stage of training is greater than that in the earlier stage.   
• We propose a novel FL mechanism according to convergence analysis results, containing a novel PDP mechanism and client selection with a new metric score. In PDP mechanism, we use sampling to reduce the added noise while meeting the personalized privacy needs of clients. Clients sample their datasets with a designed probability in each iteration. Then the perturbation on clients’ local update consists of two parts: sampling and adding noise. Thus the added noise will be reduced. Our metric score considers the local loss and privacy need of clients at the same time and balance the effect of them.   
• We evaluate our mechanism on MNIST dataset[16]. The experiment result shows that our PDP mechanism and client selection with score both have large positive effects on model. And our FL mechanism performs better than the baseline mechanism.

Organization. The rest of this paper is organized as follows. In Section II, we review related work. In Section III, we introduce background on FL and DP. In Section IV, we define personalized DP and analyze the convergence of FL with PDP and client selection. In Section V, we propose our FL mechanism with PDP combining client selection. In Section VI, we demonstrate our experimental results. In Section VII, we conclude the paper. A summary of main notations is provided in Table I.

# II. RELATED WORK

# A. Federated Learning

The concept of federated learning was first proposed by Google[4; 5]. The goal of federated learning is to build machine learning models based on multiple clients’ dataset while protecting the data privacy and date security of clients’ datasets at the same time. The main idea of how federated learning protects clients’ datasets is clients don’t send the origin datasets to server in the training periodinstead, they only upload local model updates. The most common used FL algorithm is FederatedAveraging[17]. The most common used FL optimization algorithm is FedSGD[17]. In each communication round, server distributes the global model to a fraction of clients. Clients train the global model based on their local datasets and get the local model. Then, clients send updated local models to server. Server aggregates the local models by weighted averaging.

# B. Federated Learning with Differential Privacy

Differential privacy mechanisms in federated learning mainly include mechanisms in centralized DP setting[9; 10] and in local DP setting[11; 12; 13].

Centralized DP setting. In centralized DP setting, we assume server is honest. [9] is the first work which introduces differential privacy into federated learning. In this work, authors proposed an algorithm for client side differential privacy preserving federated optimization. This algorithm protect clients’ data by perturbing global model by honest server. [10] further makes assumptions about the communication channels of server and clients, i.e. communication channels are not totally secure, and proposed NbAFL scheme that can satisfy the DP requirement by adding proper noisy perturbations at both the clients and the server.

Local DP setting. In local DP setting, we no longer assume server is honest, i.e. server may also pose a threat to clients’ data privacy, which is more closer to reality than centralized DP setting. [11] proposed LDP-Fed, a federated learning system with local DP guarantee. To reduce communication cost, [12] proposed COFEL, a federated learning system containing layer-based parameter selection and local differential privacy mechanism. In [13], authors proposed FedSel. The key idea of it is dimensions are not equally important. So this method selects Top-k dimensions according to their contributions.

The concept of personalized differential privacy has been proposed in the field of database[14; 15], which denotes the every record in the database is owned by different users and the privacy need of it is personal. However, this concept can’t be used in FL directly.

# C. Federated Learning with Client Selection

Some works assume that all clients participate in training in every iteration. However in practice, only a part of clients will participate in. Some work studies unbiased clients participation, where the contribution of clients is proportional to their local datasets size[18]. Another line of work uses biased clients participation. [19] presents convergence analysis of federated learning with biased client selection.

TABLE I: Summary of Main Notations 

<table><tr><td>K</td><td>number of clients (k ∈ {1,...,K})</td></tr><tr><td> $C_k$ </td><td>client k</td></tr><tr><td> $D_k$ </td><td>client k&#x27;s local dataset</td></tr><tr><td> $F(\cdot)$ </td><td>global objective function</td></tr><tr><td> $F_k(\cdot)$ </td><td>client k&#x27;s local objective function</td></tr><tr><td> $\pi$ </td><td>client selection mechanism</td></tr><tr><td>w</td><td>model parameter vector</td></tr><tr><td>m</td><td>number of chosen clients</td></tr><tr><td> $\mathcal{S}(\cdot)$ </td><td>set of chosen clients</td></tr><tr><td> $p_k$ </td><td>fraction of data at client k</td></tr><tr><td> $q_k$ </td><td>sampling probability of client k</td></tr><tr><td> $\beta_1, \beta_2$ </td><td>parameters of score</td></tr><tr><td>C</td><td>clipping value</td></tr><tr><td> $\epsilon_k$ </td><td>personalized differential privacy budget of client k</td></tr><tr><td> $\epsilon_{ts}$ </td><td>threshold of privacy budget</td></tr><tr><td> $\tau$ </td><td>number of local epochs</td></tr><tr><td>T</td><td>number of global iterations (t ∈ {1,...,T})</td></tr></table>

# III. PRELIMINARIES

In this section, we will present preliminaries on federated learning and personalized differential privacy.

# A. Federated Learning

Consider a general federated learning setting with one server and K clients. Client $C _ { k }$ owns a local dataset $D _ { k }$ , where $k \in$ $\{ 1 , 2 , . . . , K \}$ . The goal of server is to learn a model based on K clients’ datasets. Formally, the goal of server is to find the parameter w that minimizes the empirical risk:

$$
F (w) = \sum_ {k = 1} ^ {K} p _ {k} F _ {k} (w)
$$

where $F _ { k }$ is the local objective function of client $C _ { k } , p _ { k } =$ P K |D | , |Dk| is the size of Dk. $\frac { | D _ { k } | } { \sum _ { k = 1 } ^ { K } | D _ { k } | } , | D _ { k } |$ |Dk| $D _ { k }$

Inspired by [19], we consider client selection algorithm as a map from global model w to chosen clients set. We denote the client selection algorithm as $\pi ,$ the chosen clients set as $S ( \pi , w )$ .

The training process of federated learning usually contains following steps (we take the t-th iteration for example):

• Step 1. Client selection. According to the global model of the t − 1-th iteration $\overline { { w } } ^ { t - 1 }$ and client selection algorithm π, the server selects the clients $S ( \pi , \overline { { w } } ^ { t - 1 } )$ who will participate in the the t-th iteration.   
• Step 2. Distribute global model. Server send the t−1-th iteration global model $\overline { { w } } ^ { t - 1 }$ to the chosen clients. If this is the first round, the server initializes a global model $\overline { { w } } ^ { 0 }$ and sends it to the chosen clients.   
• Step 3. Local model training. The chosen clients update their local model $\boldsymbol { w } _ { k } ^ { t }$ using $\overline { { w } } ^ { t - 1 }$ by FedSGD based on their local datasets $D _ { k }$ . After the local training is complete, the chosen clients upload the updated local model $w _ { k } ^ { t }$ to server.   
• Step 4. Local model aggregation. The server collects the uploaded local models and aggregates them in the following way:

$$
\overline {{w}} ^ {t} = \sum_ {k = 1} ^ {m} p _ {k} w _ {k} ^ {t}
$$

where pk = $\begin{array} { r } { p _ { k } = \frac { | D _ { k } | } { \sum _ { k = 1 } ^ { K } | D _ { k } | } , | D _ { k } | } \end{array}$ is the size of $D _ { k }$ .

These steps will be repeated until a preset number of iterations is reached or the global model converges.

Then we introduce two metrics which were defined in [19].

# Definition 1. (Local-Global Objective Gap[19])

For the global optimum $w ^ { * } \ = \ \arg \operatorname* { m i n } _ { w } F ( w )$ and local optimum $w _ { k } ^ { * } = { a r g m i n } _ { w } F _ { k } ( w )$ , the local-global objective gap is defined as:

$$
\Gamma \triangleq F ^ {*} - \sum_ {k = 1} ^ {K} p _ {k} F _ {k} ^ {*} = \sum_ {k = 1} ^ {K} p _ {k} (F _ {k} (w ^ {*}) - F _ {k} (w _ {k} ^ {*})) \geq 0
$$

Γ reflects the degree of data heterogeneity, which is independent of the client selection algorithm. Large Γ indicates high data heterogeneity.

# Definition 2. (Selection Skew[19])

For any $k \in \mathcal S ( \pi , w )$ ,

$$
\rho (\mathcal {S} (\pi , w), w ^ {\prime}) = \frac {\mathbb {E} [ \frac {1}{m} \sum_ {k \in \mathcal {S} (\pi , w)} (F _ {k} (w ^ {\prime}) - F _ {k} ^ {*}) ]}{F (w ^ {\prime}) - \sum_ {k = 1} ^ {K} p _ {k} F _ {k} ^ {*}} \geq 0
$$

This metric reflects the skew of client selection algorithm $\pi .$ . We can notice that $\rho ( \boldsymbol { S } ( \boldsymbol { \pi } , \boldsymbol { w } ) , \boldsymbol { w } ^ { \prime } )$ is related to w and $w ^ { \prime } ,$ which may change during the training process. For the convenience of the analysis, we define $\begin{array} { r } { \overline { { \rho } } \triangleq \operatorname* { m i n } _ { w , w ^ { \prime } } S ( \pi , w ) , w ^ { \prime } ) } \end{array}$ , $\widetilde { \rho } \triangleq \operatorname* { m a x } _ { w } S ( \pi , w ) , w ^ { * } )$ .

# B. Differential Privacy

In this subsection, we will present the traditional differential privacy definition and introduce the traditional DP mechanism.

# Definition 3. (Differential Privacy[20])

A randomized mechanism M with domain X is $( \epsilon , \delta ) \cdot$ - differential private if for all $S \subseteq R a n g e ( { \mathcal { M } } )$ and for any two adjacent databases $D , D ^ { \prime } \in { \mathcal { X } }$ ,

$$
P r [ \mathcal {M} (\mathcal {D}) \in \mathcal {S} ] \leq e ^ {\epsilon} P r [ \mathcal {M} (\mathcal {D} ^ {\prime}) \in \mathcal {S} ] + \delta
$$

where $D , D ^ { \prime }$ are adjacent databases, i.e. $D \subset D ^ { \prime } { \mathrm { a n d } } | D ^ { \prime } | =$ $| D | + 1$ (or vice versa).

Gaussian mechanism[20] is commonly used to guarantee $( \epsilon , \delta ) \ / – \mathrm { D P }$ . In Gaussian mechanism, a Gaussian noise ${ \mathcal { N } } ( 0 , \sigma ^ { 2 } )$ is added to the parameter you want to protect. We choose $\sigma \geq c \Delta f / \epsilon$ , where $\epsilon \in ( 0 , 1 )$ , c is a constant satisfies $c ^ { 2 } \geq$ $2 l n ( 1 . 2 5 / \sigma )$ and $\Delta f$ is the sensitivity of function f , i.e. $\Delta f =$ $m a x _ { D , D ^ { \prime } } \| f ( D ) - f ( D ^ { \prime } ) \|$ .

In differential privacy, a small  indicates that client has high privacy needs. In Gaussian mechanism, a small  leads to a large σ, which means the added Gaussian noise will have large variance. Therefore, with high possibility, the added noise will be large, which may hurt the utility of function $f .$ .

# IV. THEORETICAL ANALYSIS

In this section, we present the problem definition of this work in detail firstly.To facilitate convergence analysis, we present a basic personalized differential privacy mechanism. Based on this mechanism, we will perform convergence analysis on federated learning with personalized differential privacy and client selection, investigate the impact of personalized differential privacy and client selection mechanisms on the convergence of federated learning, and derive important theoretical results of this work.

# A. Problem definition

We consider a federated learning setting with one server and K clients. Client $C _ { k }$ owns a local dataset $D _ { k }$ and has a personal privacy budget $\epsilon _ { k }$ for the whole training period, where $k \in \{ 1 , 2 , . . . , K \}$ . The training process is the same as III-A. The goal of this work is to improve the model convergence performance while meeting the PDP requirements defined as follows:

# Definition 4. (Personalized Differential Privacy(PDP))

A randomized mechanism $\mathcal { M } : \mathcal { X } \ :  \ : \mathcal { R }$ with domain X and range R satisfies personalized differential privacy, $i f f o r$ all measurable sets ${ \mathcal { S } } \subseteq { \mathcal { R } } ,$ , for every client k and any two adjacent databases $D _ { k } , D _ { k } ^ { \prime } \in \mathcal { X }$ of client k,

$$
P r [ \mathcal {M} (\mathcal {D} _ {k}) \in \mathcal {S} ] \leq e ^ {\epsilon_ {k}} P r [ \mathcal {M} (\mathcal {D} _ {k} ^ {\prime}) \in \mathcal {S} ] + \delta
$$

where $k \in \{ 1 , 2 , . . . , K \}$ .

Compared with traditional DP, PDP pays more attention on clients’ personalized privacy needs. In PDP setting, every client $C _ { k }$ has a personalized $( \epsilon _ { k } , \delta )$ -differential privacy need.

# B. Assumptions

First, we will present the assumption of global objective function $F ( \cdot )$ and local objective function $F _ { k } ( \cdot )$ .

Assumption IV.1. (µ − strongly convex)

For all v and w, $\begin{array} { r } { F _ { k } ( v ) \geq F _ { k } ( w ) + ( v - w ) ^ { T } \nabla F _ { k } ( w ) + \frac { \mu } { \lambda } \| v - } \end{array}$ $w \| _ { 2 } ^ { 2 } ,$ , where $k \in \{ 1 , 2 , . . . , K \}$ .

Assumption IV.2. (L − smooth)

For all v and w, $\begin{array} { r } { F _ { k } ( v ) \leq F _ { k } ( w ) + ( v - w ) ^ { T } \nabla F _ { k } ( w ) + \frac { L } { 2 } \| v - } \end{array}$ $w \| _ { 2 } ^ { 2 } ,$ , where $k \in \{ 1 , 2 , . . . , K \}$ .

Assumption IV.3. For the mini-batch $\xi _ { k }$ that uniformly sampled from local dataset $D _ { k }$ , $\begin{array} { r c l } { { \mathbb { E } [ g _ { k } ( w _ { k } , \xi _ { k } ) ] } } & { { = } } & { { \nabla F _ { k } ( w _ { k } ) } } \end{array}$ , $\begin{array} { r } { \mathbb { E } \| g _ { k } ( w _ { k } , \xi _ { k } ) - \nabla F _ { k } ( w _ { k } ) \| ^ { 2 } \ \leq \ \alpha ^ { 2 } , } \end{array}$ where $g _ { k } ( w _ { k } , \xi _ { k } ) =$ 1|ξk| Pξ∈ξk ∇Fk(wk, ξ), k ∈ {1, 2, ..., K }. $\begin{array} { r } { \frac { 1 } { | \xi _ { k } | } \sum _ { \xi \in \xi _ { k } } \nabla F _ { k } ( w _ { k } , \xi ) , k \in \{ 1 , 2 , . . . , K \} } \end{array}$

Assumption IV.4. $\mathbb { E } \| g _ { k } ( w _ { k } , \xi _ { k } ) \| ^ { 2 } \ \leq \ G ^ { 2 }$ , where $k \_ \in$ $\{ 1 , 2 , . . . , K \}$

# C. A basic PDP mechanism

For the convenient of theoretical analysis, we will design a basic PDP mechanism first. We use Gaussian mechanism to satisfy clients’ personalized differential privacy needs. For client $C _ { k }$ , before adding noise to the local model, we will use a clipping mechanism. Assuming that the clipping value is $C ,$ we can ensure $\| w _ { k } \| \leq C$ Then, the local training process of client $C _ { k }$ is:

$$
w _ {k} = \arg \min _ {w} F _ {k} (w, D _ {k}) = \frac {1}{| D _ {k} |} \sum_ {i = 1} ^ {| D _ {k} |} \arg \min _ {w} F _ {k} (w, D _ {k, i})
$$

where $D _ { k , i }$ is the i-th data of local dataset $D _ { k }$ .

According to the definition, the sensitivity $\begin{array} { r } { \Delta w _ { k } = \frac { 2 C } { | D _ { k } | } } \end{array}$ |Dk To satisfy PDP with $T$ aggregations, before uploading updated local model to server, client $C _ { k }$ needs to add Gaussian noise $n _ { k } \sim \mathcal N ( 0 , \sigma _ { k } ^ { 2 } )$ to local model $w _ { k }$ , where $\begin{array} { r } { \sigma _ { k } = \frac { c T \Delta w _ { k } } { \epsilon _ { k } } } \end{array}$ cT ∆wk , k ∈ k $\{ 1 , 2 , . . . , K \}$ .

We index the local SGD epochs with t. In each iteration, every client trains local model for τ epochs. Now let’s define the local model update process of client $C _ { k }$ .

Then when t + 1 mod $\tau \neq 0 ,$ ,

$$
w _ {k} ^ {t + 1} = w _ {k} ^ {t} - \eta_ {t} g _ {k} (w _ {k} ^ {t}, \xi_ {k} ^ {t})
$$

When t + 1 mod $\tau = 0 ,$ ,

$$
w _ {k} ^ {t + 1} = \frac {1}{m} \sum_ {i \in S ^ {t}} (w _ {i} ^ {t} - \eta_ {t} g _ {i} (w _ {i} ^ {t}, \xi_ {i} ^ {t}) + \boldsymbol {n} _ {i} ^ {t}) \triangleq \overline {{w}} ^ {t + 1}
$$

where $\boldsymbol { n } _ { i } ^ { t }$ is the Gaussian noise added by client $C _ { i } , \overline { { w } } ^ { t + 1 }$ denotes the global model.

For the convenience of analysis, we define a virtual global update rule:

$$
\overline {{w}} ^ {t + 1} = \overline {{w}} ^ {t} - \eta_ {t} \cdot \frac {1}{m} \sum_ {k \in S ^ {t}} g _ {k} (w _ {k} ^ {t}, \xi_ {k} ^ {t}) + \frac {1}{\tau} \sum_ {k \in S ^ {t}} \boldsymbol {n} _ {k} ^ {t}
$$

In virtual global update rule, we assume that the global model $\overline { { w } } ^ { t }$ is updated in each local training epoch, i.e., the server aggregates the local model updates of the chosen clients in each local training epoch. To balance the impact of the personalized differential privacy mechanism in this virtual global update rule, we assume that the chosen clients distribute the added noise from the personalized differential privacy mechanism evenly across τ local training epochs.

# D. Convergence Analysis

In this subsection, we analyze the convergence performance of federated learning with client selection and personalized differential privacy. We want to explore how DP parameters  and client selection mechanism affect the convergence performance of federated learning model.

Using Assumption IV.2 we can get the following lemma:

Lemma IV.1. $F _ { k }$ is L-smooth, then for optimal local model $w _ { k } ^ { * }$ and any local model $w _ { k } ,$ ,

$$
\left\| \nabla F _ {k} (w _ {k}) \right\| ^ {2} \leq 2 L \left(F _ {k} (w _ {k}) - F _ {k} \left(w _ {k} ^ {*}\right)\right)
$$

Proof.

$$
F _ {k} (w _ {k} ^ {*}) - F _ {k} (w _ {k}) \leq - \frac {1}{2 L} \| \nabla F _ {k} (w _ {k} ^ {*}) - \nabla F _ {k} (w _ {k}) \| ^ {2}
$$

$$
+ \nabla F _ {k} (w _ {k} ^ {*}) ^ {T} (w _ {k} ^ {*} - w _ {k})
$$

$$
\frac {1}{2 L} \| \nabla F _ {k} (w _ {k} ^ {*}) - \nabla F _ {k} (w _ {k}) \| ^ {2} \leq F _ {k} (w _ {k}) - F _ {k} (w _ {k} ^ {*})
$$

$$
+ \nabla F _ {k} (w _ {k} ^ {*}) ^ {T} (w _ {k} ^ {*} - w _ {k})
$$

$$
\left\| \nabla F _ {k} \left(w _ {k}\right) - \nabla F _ {k} \left(w _ {k} ^ {*}\right) \right\| ^ {2} \leq 2 L \left(F _ {k} \left(w _ {k}\right) - F _ {k} \left(w _ {k} ^ {*}\right)\right)
$$

Notice that, $\nabla F _ { k } ( w _ { k } ^ { * } ) = 0$ . This completes the proof.

![](images/a350ed937c79818c73453eea0a1f3c6eda6875fe259f11d5f4f82b4ea084222e.jpg)

Lemma IV.1 shows that under Assumption IV.2, there exists an upper bound on $\| \nabla F _ { k } ( w _ { k } ) \| ^ { 2 }$ associated with $F _ { k } ( w _ { k } ^ { * } )$ , which will help us to restrict $\| \dot { \nabla } \ddot { F } _ { k } ( w _ { k } ) \| ^ { 2 }$ in the convergence analysis that follows. In the next lemma, we will restrict the expected mean difference between the global model and the local model.

Lemma IV.2. (Expected average difference between global and local model) In the tth epoch, the expected average difference between global and local model can be upperbounded by:

$$
\frac {1}{m} \mathbb {E} [ \sum_ {k \in S ^ {t}} \| \overline {{w}} ^ {t} - w _ {k} ^ {t} \| ^ {2} ] \leq 1 6 \eta_ {t} ^ {2} \tau^ {2} G ^ {2} + (4 \eta_ {t} ^ {2} \tau + \frac {1}{\tau}) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

Proof.

$$
\frac {1}{m} \sum_ {k \in S ^ {t}} \| \overline {{w}} ^ {t} - w _ {k} ^ {t} \| ^ {2}
$$

$$
= \frac {1}{m} \sum_ {k \in S ^ {t}} \| \frac {1}{m} \sum_ {k ^ {\prime} \in S ^ {t}} w _ {k ^ {\prime}} ^ {t} + \frac {1}{\tau} n _ {k ^ {\prime}} ^ {t} - w _ {k} ^ {t} \| ^ {2}
$$

$$
\leq \frac{1}{m^{2}}\sum_{\substack{k\neq k^{\prime}\\ k,k^{\prime}\in S^{t}}}\| w_{k^{\prime}}^{t} + \frac{1}{\tau} n_{k^{\prime}}^{t} - w_{k}^{t}\|^{2} + \frac{1}{\tau}\sum_{k\in S^{t}}\| n_{k}^{t}\|^{2}
$$

$$
\leq \frac{\eta_{t_{0}}^{2}\tau}{m^{2}}\sum_{\substack{k\neq k^{\prime}\\ k,k^{\prime}\in S^{t}}}\sum_{i = t_{0}}^{t_{0} + \tau -1}\| g_{k^{\prime}}(w_{k^{\prime}}^{i},\xi_{k^{\prime}}^{i}) - g_{k}(w_{k}^{i},\xi_{k}^{i})\|^{2}
$$

$$
+\frac{\eta_{t_{0}}^{2}\tau}{m}\sum_{\substack{k\neq k^{\prime}\\ k,k^{\prime}\in S^{t}}}\| n_{k^{\prime}}^{t}\|^{2} + \frac{1}{\tau}\sum_{k\in S^{t}}\| n_{k}^{t}\|^{2}
$$

$$
= \frac{\eta_{t_{0}}^{2}\tau}{m^{2}}\sum_{\substack{k\neq k^{\prime}\\ k,k^{\prime}\in S^{t}}}\sum_{i = t_{0}}^{t_{0} + \tau -1}\| g_{k^{\prime}}(w_{k^{\prime}}^{i},\xi_{k^{\prime}}^{i}) - g_{k}(w_{k}^{i},\xi_{k}^{i})\|^{2}
$$

$$
+ \frac {\eta_ {t _ {0}} ^ {2} \tau (m - 1)}{m} \sum_ {k \in S ^ {t}} \| n _ {k ^ {\prime}} ^ {t} \| ^ {2} + \frac {1}{\tau} \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

$$
\leq 1 6 \eta_ {t} ^ {2} \tau^ {2} G ^ {2} + (4 \eta_ {t} ^ {2} \tau + \frac {1}{\tau}) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

where $\eta _ { t }$ is non-increasing and $\eta _ { t _ { 0 } } \leq 2 \eta _ { t }$ .

![](images/4882023b5cf83c225e8fcd9f94774974a5d54a1eb9dd29eb4438fbe56f4167db.jpg)

Lemma IV.2 reveals the upper bound between global and local model in the tth epoch. Then, we will bound the difference between global model in the t-th epoch $\overline { { w } } ^ { t }$ and optimal global model $w ^ { * }$ .

Lemma IV.3. Assume that in each epoch, m clients are chosen. Then we have:

$$
\mathbb {E} \| \overline {{w}} ^ {t} - w ^ {*} \| ^ {2} \leq \frac {1}{m} \mathbb {E} [ \sum_ {k \in S ^ {t}} \| w _ {k} ^ {t} - w ^ {*} \| ^ {2} ] + \frac {1}{m \tau} \mathbb {E} [ \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2} ]
$$

Proof.

$$
\begin{array}{l} \mathbb {E} \| \overline {{w}} ^ {t} - w ^ {*} \| ^ {2} = \mathbb {E} [ \| \frac {1}{m} \sum_ {k \in S ^ {t}} (w _ {k} ^ {t} + \frac {1}{\tau} n _ {k} ^ {t} - w ^ {*}) \| ^ {2} ] \\ \leq \frac {1}{m} \mathbb {E} [ \sum_ {k \in S ^ {t}} \| w _ {k} ^ {t} - w ^ {*} + \frac {1}{\tau} n _ {k} ^ {t} \| ^ {2} ] \\ \leq \frac {1}{m} \mathbb {E} [ \sum_ {k \in S ^ {t}} \| w _ {k} ^ {t} - w ^ {*} \| ^ {2} ] \\ + \frac {1}{m \tau} \mathbb {E} [ \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2} ] \\ \end{array}
$$

![](images/81064310e489d8770ca9f49b5fbfdf18fb3f570f085b2a70495a10c714d28519.jpg)

Using lemma IV.1, IV.2, IV.3, we can get the following theorem.

Theorem 1. (Convergence with fixed learning rate) Under assumptions IV.1 to IV.4, with fixed learning rate $\eta \quad \leq$ min $\textstyle { \bigl \{ } { \frac { 1 } { 2 \mu A _ { 1 } } } , { \frac { 1 } { 4 L } } { \bigr \} }$ , the error after T epochs of federated learning

with client selection and personalized differential privacy is bounded as follows:

$$
\begin{array}{l} F (\overline {{w}} ^ {T}) - F ^ {*} \leq (1 - \eta \mu A _ {1}) ^ {T} (\frac {L}{\mu} (F (\overline {{w}} ^ {0}) - F ^ {*}) \\ - \frac {L \eta A _ {2} + 2 L \Gamma (\widetilde {\rho} - \overline {{\rho}})}{2 \mu A _ {1}}) \\ + \frac {L \eta A _ {2}}{2 \mu A _ {1}} + \frac {L \Gamma (\widetilde {\rho} - \overline {{\rho}})}{\mu A _ {1}} \\ + A _ {3} \sum_ {i = 0} ^ {T} (1 - \eta \mu A _ {1}) ^ {T - i} \sum_ {k \in S ^ {i}} \| n _ {k} ^ {i} \| ^ {2} \\ \end{array}
$$

where $\begin{array} { r } { A _ { 1 } \ = \ 1 + \frac { 3 } { 8 } \overline { { \rho } } , \ A _ { 2 } \ = \ 3 2 \tau ^ { 2 } G ^ { 2 } + \frac { \alpha ^ { 2 } } { m } + 6 \overline { { \rho } } L \Gamma , \ A _ { 3 } \ = } \end{array}$ $\begin{array} { r } { 4 L \tau \eta ^ { 2 } - \frac { L \mu } { 2 m \tau } \eta + \frac { \tilde { L } } { \tau } . } \end{array}$ .

Proof. See appendix A.

![](images/812d46e8704690673fb5d4b0b3ebc87614bee8d8d6a83aa179de4e03b8573ed9.jpg)

From above theorem, we can know that for faster convergence, we need a large $A _ { 1 }$ , which means we need a large ${ \overline { { \rho } } } .$ Notice that $0 ~ < ~ 1 - \eta \mu A _ { 1 } ~ < ~ 1$ , then when $t ~  ~ \infty$ , the first term, i.e. $( 1 ~ { \stackrel { . . } { - } } ~ \eta \mu A _ { 1 } ) ^ { T } ( \textstyle { \frac { L } { \mu } } ( F ( { \overline { { w } } } ^ { 0 } ) ~ -$ $\begin{array} { r } { F ^ { * } ) \ : - \ : \frac { L \eta A _ { 2 } + 2 L \Gamma ( \widetilde { \rho } - \overline { { \rho } } ) } { 2 \mu A _ { 1 } } ) } \end{array}$ , goes to 0. Thus when considering bias, we only need to care about LηA2 + $\begin{array} { r } { \frac { L \eta A _ { 2 } } { 2 \mu A _ { 1 } } ~ + ~ \frac { L \Gamma ( \widetilde { \rho } - \overline { { \rho } } ) } { \mu A _ { 1 } } } \end{array}$ and $\begin{array} { r } { A _ { 3 } \sum _ { i = 0 } ^ { T } ( 1 - \eta \mu A _ { 1 } ) ^ { T - i } \sum _ { k \in S ^ { i } } \| n _ { k } ^ { i } \| ^ { 2 } . } \end{array}$ .

$$
\begin{array}{l} f i r s t \_ t e r m = \frac {L \eta (3 2 \tau^ {2} G ^ {2} + \frac {\alpha^ {2}}{m} + 6 \overline {{\rho}} L \Gamma)}{2 \mu (1 + \frac {3}{8} \overline {{\rho}})} + \frac {L \Gamma (\widetilde {\rho} - \overline {{\rho}})}{\mu (1 + \frac {3}{8} \overline {{\rho}})} \\ \leq \frac {4 L \eta (3 2 \tau^ {2} G ^ {2} + \frac {\alpha^ {2}}{m})}{3 \mu \overline {{\rho}}} + \frac {8 L \eta L \Gamma}{\mu} + \frac {8 L \Gamma}{3 \mu} (\frac {\widetilde {\rho}}{\overline {{\rho}}} - 1) \\ \end{array}
$$

From previous work [19], we know that ${ \frac { \widetilde { \rho } } { \overline { { \rho } } } } - 1$ is close to 0. Thus for small bias, we need a large ${ \overline { { \rho } } } .$

For the second term $\begin{array} { r } { A _ { 3 } \sum _ { i = 0 } ^ { T } ( 1 - \eta \mu A _ { 1 } ) ^ { T - i } \sum _ { k \in S ^ { i } } \| n _ { k } ^ { i } \| ^ { 2 } . } \end{array}$ negligible. As the training progresses, the influence of the noise term will gradually increase.

# V. MECHANISM DESIGN

From Theorem 1, we find that for fast convergence and small bias, we need to reduce $\overline { \rho }$ and reduce the added noise introduced by PDP mechanism. Through this observation, in this section, we propose a mechanism that combines client selection and PDP protection. The two novel parts of this mechanism is client selection and PDP mechanism with sampling.

# A. Client Selection

From above analysis, we know that we need to select clients with large $\overline { { \rho } }$ and small added noise. Using this insight, we can choose clients with large local loss $F _ { k } ( w )$ and large privacy parameter . However we may face such problem: there is one client $C _ { i }$ with small local loss and large $\epsilon _ { i } ,$ and another client $C _ { j }$ with large local loss and small $\epsilon _ { j } ,$ , which client should we choose?

From Theorem 1, we know that the effect of added noise on bias increases exponentially with epoch t. Thus to solve the above problem, we define a new metric to select clients. The score of client $C _ { k }$ in the t-th iteration is:

Algorithm 1: Federated Learning with Personalized DP and Client Selection

Input: iteration T, initialized global parameters $\overline{w}^{0}$ , $\epsilon_{k}$ of k clients, chosen clients number m

Output: chosen client set $S^{t+1}$ 1 for t in range(T) do

2 server send $\overline{w}^{t-1}$ to all clients

3 server receive $\{score_{k}\}$ from all clients

4 $S^{t} \leftarrow m$ clients with largest score

    /* local training part */

5 for $C_{k}$ in $S^{t}$ do

6 $w_{k}^{t} \leftarrow \overline{w}_{k}^{t-1}$ 7 $\xi_{k} \leftarrow sample D_{k}$ with $q_{k}$ 8 for e in range( $\tau$ ) do

9 $\lfloor w_{k}^{t} \leftarrow w_{k}^{t} - \eta_{t} g_{k}(w_{k}^{t}, \xi_{k}^{t})$ /* Clipping */

10 $w_{k}^{t} \leftarrow w_{k}^{t} / \max(1, \frac{\|w_{k}^{t}\|}{C})$ /* Adding local noise */

11 $w_{k}^{t} \leftarrow w_{k}^{t+1} + n_{k}^{t}$ 12 $\overline{w}^{t} \leftarrow \frac{1}{m} \sum_{k \in S^{t}} w_{k}^{t}$

$$
\operatorname{score} _ {k} ^ {t} = \operatorname{rank} \left(F _ {k} \left(\overline {{w}} ^ {t}\right)\right) + \beta_ {1} ^ {\lfloor (T - t) / \beta_ {2} \rfloor} \operatorname{rank} \left(\epsilon_ {k}\right)
$$

where $r a n k ( \cdot )$ refers to the sorting position from small to large, $\beta _ { 1 }$ and $\beta _ { 2 }$ are constants satisfy $0 < \beta _ { 1 } < 1 , \beta _ { 2 } \geq 1$ , T is the total number of training epochs.

For balancing the effect of local loss part and privacy part, we use rank to present their importance. $\beta _ { 1 }$ and $\beta _ { 2 }$ are two parameters we need to set in advance. They control the influence factor of the noise part. Small $\beta _ { 1 }$ means the noise part in the late training is much more important than in the early training. $\beta _ { 2 }$ makes the coefficient of privacy gradually become smaller in stages as the iteration increases.

# B. Personalized DP Mechanism containing Sampling

We use $\epsilon _ { t s }$ to denote the threshold of privacy parameter. For client $C _ { k } ,$ , if $\epsilon _ { k } / T < \epsilon _ { t s } ,$ , the privacy need of $C _ { k }$ so high that may have a great negative impact on model. Later in the experimental results, we show that part of clients with extreme high privacy needs will hurt the performance of model. Thus to reduce added noise of such clients, we introduce sampling technique.

Theorem 2. (Personalized DP Mechanism containing Sampling) To ensure PDP with T iterations, every chosen client $C _ { k }$ sample his data with probability $q _ { k }$ in each iteration, where

$$
q _ {k} = \min \{\frac {e ^ {\epsilon_ {k} / T} - 1}{e ^ {\epsilon_ {t s}} - 1}, 1 \}.
$$

Then, a Gaussian noise $n _ { k } \sim \mathcal N ( 0 , \sigma _ { k } ^ { 2 } )$ is added to local model $w _ { k } ,$ , where $\begin{array} { r } { \sigma _ { k } = \frac { c T \Delta w _ { k } } { \epsilon _ { t s } } , k \in \{ 1 , 2 , . . . , K \} } \end{array}$ cT ∆wk , k ∈ {1, 2, ..., K }. ts

Proof. When $\epsilon _ { k } \geq \epsilon _ { t s } .$ , this mechanism is equivalent to the Gaussian mechanism. Thus it satisfies PDP.

When $\epsilon _ { k } < \epsilon _ { t s }$ , we suppose the adjacent databases $D _ { k }$ and $D _ { k } ^ { \prime }$ differ by only one data x, i.e. $D _ { k } ^ { \prime } = D _ { k } \cup \{ x \}$ . We use GM to denote Gaussian mechanism, SP to denote sampling.

$$
\begin{array}{l} P r [ \mathcal {M} (\mathcal {D} _ {k} ^ {\prime}) \in \mathcal {S} ] \\ = \sum_ {Z \subseteq D _ {k}} q _ {k} \operatorname * {P r} [ S P (D _ {k}) = Z ] \operatorname * {P r} [ G M (Z \cup \{x \}) \in \mathcal {S} ] \\ + \sum_ {Z \subseteq D _ {k}} (1 - q _ {k}) P r [ S P (D _ {k}) = Z ] P r [ G M (Z) \in \mathcal {S} ] \\ \leq \sum_ {Z \subseteq D _ {k}} q _ {k} P r [ S P (D _ {k}) = Z ] e ^ {\epsilon_ {t s}} P r [ G M (Z) \in \mathcal {S} ] \\ + (1 - q _ {k}) \operatorname * {P r} [ \mathcal {M} (\mathcal {D} _ {k}) \in \mathcal {S} ] + \delta \\ = (1 - q _ {k} + e ^ {\epsilon_ {t s}} q _ {k}) \operatorname * {P r} [ \mathcal {M} (\mathcal {D} _ {k}) \in \mathcal {S} ] + \delta \\ = e ^ {\epsilon_ {k} / T} \operatorname * {P r} [ \mathcal {M} (\mathcal {D} _ {k}) \in \mathcal {S} ] + \delta \\ \end{array}
$$

Now we complete the proof.

![](images/fba63abd703d5b814952537272f6cd789e0247174501315687ab8066d4c9557c.jpg)

Algorithm 1 outlines our proposed federated learning mechanism with personalized DP and client selection. This algorithm reduces added noise by introducing other forms of perturbation.

# VI. EXPERIMENTS

# A. Experiment Conguration

We evaluate our proposed mechanism by using federated optimization algorithm FedSGD[17] and deep learning model FedAVG-CNN-MNIST[21]. We conduct our experiments on MNIST[16], which is a handwritten digit recognition dataset containing 60,000 training examples and 10,000 test examples. The size of each image in the dataset is $2 8 \times 2 8$ . We set clients number $K = 1 0$ . Each client owns 6000 samples, where 5460 examples of one class, and 60 examples of each of the other nine classes.For other parameters, we set clipping value $C =$ 1, epsilon threshold $\epsilon _ { t s } = 0 . 1$ , rank metric parameter $\beta _ { 1 } =$ $0 . 9 , \ \beta _ { 2 } = 1 0$ , chosen clients number $m = 5 ,$ , total iterations $T = 5 0$ , epoch number $\tau = 5 ,$ privacy parameter $\delta = 0 . 0 0 1$ .

![](images/bea233656fea81463f8857ca16941d4c277cfbb1341fd66254b88fb483bdd59a.jpg)



Fig. 1: Training loss with different privacy distribution.

![](images/06ad82337cd873d07a449b4ccf5387df59f9a7d97ece5b024db3237dd9c6dc17.jpg)



Fig. 2: Training loss with different mechanism.

# B. Performance on Different Privacy Distributions

In Fig.1, we set different client privacy budgets. We sample clients’ privacy budget $\epsilon _ { k }$ with Gaussian distribution ${ \mathcal { N } } ( \mu , \sigma ^ { 2 } )$ . We choose same µ and different σ to represent different privacy distributions. A large σ represents there are more clients with high privacy needs. From the result we can know that, part of clients with extreme high privacy needs will hurt the performance of the model.

# C. Performance on Different Mechanisms

Result is shown in Fig.2. We set the privacy budget  of 10 clients as [0.5, 0.5, 0.5, 0.5, 10, 10, 10, 10, 100, 100]. To eliminate random effects, we run this experiment 3 times and report average results. From the result, we can find that PDP mechanism containing sampling and client selection with score are both perform well. The proposed mechanism with these two improvements performs best among these four mechanisms.

# VII. CONCLUSION

In this work, we mainly focus on federated learning with personalized differential privacy and client selection. We conduct a convergence analysis of this setting, and propose a novel mechanism according to the analysis results. The two main insights of this novel mechanism are: (1) we prefer clients with large local loss and small added noise (2) the influence of noise added by PDP mechanism on the later stage of training is greater than that in the earlier stage.

The privacy budget allocation for clients in our mechanism is very simple. We just allocation them equally according to training iterations. This is likely to affect the performance of the mechanism. As a future work, it is of great interest to analyze the impact of privacy budget allocation mechanism on convergence.

# ACKNOWLEDGMENT

This research is supported by the National Key RD Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, No. 62132018, No. 61822209, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002. This work was partially supported by the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. Van Den Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam, M. Lanctot et al., “Mastering the game of go with deep neural networks and tree search,” nature, vol. 529, no. 7587, pp. 484–489, 2016. I   
[2] P. Voigt and A. Von dem Bussche, “The eu general data protection regulation (gdpr),” A Practical Guide, 1st Ed., Cham: Springer International Publishing, vol. 10, p. 3152676, 2017. I   
[3] L. Determann, Z. J. Ruan, T. Gao, and J. Tam, “Chinas draft personal information protection law,” Journal of Data Protection & Privacy, vol. 4, no. 3, pp. 235–259, 2021. I   
[4] J. Konecnˇ y, H. B. McMahan, D. Ramage, and \` P. Richtarik, “Federated optimization: Distributed ma- ´ chine learning for on-device intelligence,” arXiv preprint arXiv:1610.02527, 2016. I, II-A   
[5] J. Konecnˇ y, H. B. McMahan, F. X. Yu, P. Richt\` arik, A. T.´ Suresh, and D. Bacon, “Federated learning: Strategies for improving communication efficiency,” arXiv preprint arXiv:1610.05492, 2016. I, II-A   
[6] M. Fredrikson, S. Jha, and T. Ristenpart, “Model inversion attacks that exploit confidence information and basic countermeasures,” in Proceedings of the 22nd ACM SIGSAC conference on computer and communications security, 2015, pp. 1322–1333. I   
[7] J. Geiping, H. Bauermeister, H. Droge, and M. Moeller, ¨ “Inverting gradients–how easy is it to break privacy in federated learning?” arXiv preprint arXiv:2003.14053, 2020. I   
[8] L. Zhu and S. Han, “Deep leakage from gradients,” in Federated learning. Springer, 2020, pp. 17–31. I   
[9] R. C. Geyer, T. Klein, and M. Nabi, “Differentially private federated learning: A client level perspective,” arXiv preprint arXiv:1712.07557, 2017. I, II-B   
[10] K. Wei, J. Li, M. Ding, C. Ma, H. H. Yang, F. Farokhi, S. Jin, T. Q. Quek, and H. V. Poor, “Federated learning with differential privacy: Algorithms and performance analysis,” IEEE Transactions on Information Forensics and Security, vol. 15, pp. 3454–3469, 2020. I, II-B   
[11] S. Truex, L. Liu, K.-H. Chow, M. E. Gursoy, and W. Wei, “Ldp-fed: Federated learning with local differential privacy,” in Proceedings of the Third ACM International Workshop on Edge Systems, Analytics and Networking, 2020, pp. 61–66. I, II-B   
[12] Z. Lian, W. Wang, and C. Su, “Cofel: Communicationefficient and optimized federated learning with local differential privacy,” in ICC 2021-IEEE International Conference on Communications. IEEE, 2021, pp. 1– 6. I, II-B   
[13] R. Liu, Y. Cao, M. Yoshikawa, and H. Chen, “Fedsel: Federated sgd under local differential privacy with top-

k dimension selection,” in International Conference on Database Systems for Advanced Applications. Springer, 2020, pp. 485–501. I, II-B   
[14] Z. Jorgensen, T. Yu, and G. Cormode, “Conservative or liberal? personalized differential privacy,” in 2015 IEEE 31St international conference on data engineering. IEEE, 2015, pp. 1023–1034. I, II-B   
[15] H. Li, L. Xiong, Z. Ji, and X. Jiang, “Partitioning-based mechanisms under personalized differential privacy,” in Pacific-asia conference on knowledge discovery and data mining. Springer, 2017, pp. 615–627. I, II-B   
[16] Y. LeCun, “The mnist database of handwritten digits,” http://yann. lecun. com/exdb/mnist/, 1998. I, VI-A   
[17] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial intelligence and statistics. PMLR, 2017, pp. 1273–1282. II-A, VI-A   
[18] X. Li, K. Huang, W. Yang, S. Wang, and Z. Zhang, “On the convergence of fedavg on non-iid data,” arXiv preprint arXiv:1907.02189, 2019. II-C   
[19] Y. J. Cho, J. Wang, and G. Joshi, “Client selection in federated learning: Convergence analysis and power-of-choice selection strategies,” arXiv preprint arXiv:2010.01243, 2020. II-C, III-A, 1, 2, IV-D   
[20] C. Dwork, A. Roth et al., “The algorithmic foundations of differential privacy.” Found. Trends Theor. Comput. Sci., vol. 9, no. 3-4, pp. 211–407, 2014. 3, III-B   
[21] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278– 2324, 1998. VI-A   
[22] C. Dwork, F. McSherry, K. Nissim, and A. Smith, “Calibrating noise to sensitivity in private data analysis,” in Theory of cryptography conference. Springer, 2006, pp. 265–284.   
[23] H. Du, L. Chen, J. Qian, J. Hou, T. Jung, and X.-Y. Li, “Patronus: A system for privacy-preserving cloud video surveillance,” IEEE Journal on Selected Areas in Communications, vol. 38, no. 6, pp. 1252–1261, 2020.   
[24] T. Jung, X.-Y. Li, and M. Wan, “Collusion-tolerable privacy-preserving sum and product calculation without secure channel,” IEEE Transactions on Dependable and secure computing, vol. 12, no. 1, pp. 45–57, 2014.   
[25] Z. Jiang, J. Zhao, X.-Y. Li, J. Han, and W. Xi, “Rejecting the attack: Source authentication for wi-fi management frames using csi information,” in 2013 Proceedings IEEE INFOCOM. IEEE, 2013, pp. 2544–2552.   
[26] L. Lu, Y. Liu, and X.-Y. Li, “Refresh: Weak privacy model for rfid systems,” in 2010 Proceedings IEEE INFOCOM. IEEE, 2010, pp. 1–9.   
[27] L. Zhang, X.-Y. Li, K. Liu, T. Jung, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in mobile social networks,” IEEE Transactions on Mobile Computing, vol. 14, no. 9, pp. 1888–1902, 2014.   
[28] L. Zhang, X.-Y. Li, K. Liu, C. Liu, X. Ding, and Y. Liu,

“Cloak of invisibility: Privacy-friendly photo capturing and sharing system,” IEEE Transactions on Mobile Computing, vol. 18, no. 11, pp. 2488–2501, 2018.   
[29] L. Zhang, T. Jung, K. Liu, X.-Y. Li, X. Ding, J. Gu, and Y. Liu, “Pic: Enable large-scale privacy preserving content-based image search on cloud,” IEEE Transactions on Parallel and Distributed Systems, vol. 28, no. 11, pp. 3258–3271, 2017.   
[30] J. Han and Y. Liu, “Rumor riding: Anonymizing unstructured peer-to-peer systems,” in Proceedings of the 2006 IEEE International Conference on Network Protocols. IEEE, 2006, pp. 22–31.   
[31] L. Zhang, X.-Y. Li, Y. Liu, and T. Jung, “Verifiable private multi-party computation: ranging and ranking,” in 2013 Proceedings IEEE INFOCOM. IEEE, 2013, pp. 605–609.   
[32] A. Li, L. Zhang, J. Wang, F. Han, and X. Li, “Privacypreserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, 2021.   
[33] F. Han, L. Zhang, H. Feng, W. Liu, and X. Li, “Scape: Scalable collaborative analytics system on private database with malicious security,” in IEEE ICDE 2022-IEEE International Conference on Data Engineering. IEEE, 2022.

# APPENDIX

A. Proof of Theorem 1

Proof.

$$
\begin{array}{l} \| \overline {{w}} ^ {t + 1} - w ^ {*} \| ^ {2} = \| \overline {{w}} ^ {t} - \eta_ {t} \overline {{g}} ^ {t} + \sum_ {k \in S ^ {t}} n _ {k} ^ {t} - w ^ {*} \| ^ {2} \\ \leq \| \overline {{w}} ^ {t} - \eta_ {t} \overline {{g}} ^ {t} - w ^ {*} - \frac {\eta_ {t}}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}) \\ + \frac {\eta_ {t}}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}) \| ^ {2} + \| \sum_ {k \in S ^ {t}} n _ {k} ^ {t} \| ^ {2} \\ = \| \overline {{{w}}} ^ {t} - w ^ {*} \| ^ {2} + B _ {1} + B _ {2} + B _ {3} + B _ {4} \\ \end{array}
$$

where:

$$
B _ {1} = - 2 \eta_ {t} \left\langle \overline {{w}} ^ {t} - w ^ {*}, \frac {1}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}) \right\rangle
$$

$$
B _ {2} = 2 \eta_ {t} \left\langle \overline {{w}} ^ {t} - w ^ {*} - \frac {\eta_ {t}}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}), \frac {1}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}) - \overline {{g}} ^ {t} \right\rangle
$$

$$
B _ {3} = \eta_ {t} ^ {2} \| \frac {1}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}) \| ^ {2}
$$

$$
B _ {4} = \eta_ {t} ^ {2} \| \frac {1}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}) - \overline {{g}} ^ {t} \| ^ {2} + \| \sum_ {k \in S ^ {t}} n _ {k} ^ {t} \| ^ {2}
$$

We will bound $B _ { 1 } , B _ { 2 } , B _ { 3 } , B _ { 4 }$ respectively. We bound $B _ { 1 }$ first.

$$
B _ {1} = - 2 \eta_ {t} \left\langle \overline {{w}} ^ {t} - w ^ {*}, \frac {1}{m} \sum_ {k \in S ^ {t}} \nabla F _ {k} (w _ {k} ^ {t}) \right\rangle
$$

$$
= - \frac {2 \eta_ {t}}{m} \sum_ {k \in S ^ {t}} \left\langle \overline {{w}} ^ {t} - w _ {k} ^ {t}, \nabla F _ {k} (w _ {k} ^ {t}) \right\rangle
$$

$$
- \frac {2 \eta_ {t}}{m} \sum_ {k \in S ^ {t}} \left\langle w _ {k} ^ {t} - w ^ {*}, \nabla F _ {k} (w _ {k} ^ {t}) \right\rangle
$$

$$
\leq \frac {1}{m} \sum_ {k \in S ^ {t}} \| \overline {{w}} ^ {t} - w _ {k} ^ {t} \| ^ {2} + \frac {\eta_ {t} ^ {2}}{m} \sum_ {k \in S ^ {t}} \| \nabla F _ {k} (w _ {k} ^ {t} \| ^ {2}
$$

$$
- \frac {2 \eta_ {t}}{m} \sum_ {k \in S ^ {t}} \left\langle w _ {k} ^ {t} - w ^ {*}, \nabla F _ {k} (w _ {k} ^ {t}) \right\rangle
$$

$$
\leq \frac {1}{m} \sum_ {k \in S ^ {t}} \| \overline {{w}} ^ {t} - w _ {k} ^ {t} \| ^ {2} + \frac {2 L \eta_ {t} ^ {2}}{m} \sum_ {k \in S ^ {t}} F _ {k} (w _ {k} ^ {t}) - F _ {k} ^ {*}
$$

$$
- \frac {2 \eta_ {t}}{m} \sum_ {k \in S ^ {t}} [ (F _ {k} (w _ {k} ^ {t}) - F _ {k} (w ^ {*})) + \frac {\mu}{2} \| w _ {k} ^ {t} - w ^ {*} \| ^ {2} ]
$$

$$
\leq 1 6 \eta_ {t} ^ {2} \tau^ {2} G ^ {2} + (4 \eta_ {t} ^ {2} \tau + \frac {1}{\tau}) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

$$
- \frac {\eta_ {t} \mu}{m} \sum_ {k \in S ^ {t}} \| w _ {k} ^ {t} - w ^ {*} \| ^ {2} + \frac {2 L \eta_ {t} ^ {2}}{m} \sum_ {k \in S ^ {t}} \left(F _ {k} \left(w _ {k} ^ {t}\right) - F _ {k} ^ {*}\right)
$$

$$
- \frac {2 \eta_ {t}}{m} \sum_ {k \in S ^ {t}} (F _ {k} (w _ {k} ^ {t}) - F _ {k} (w ^ {*}))
$$

Because of the unbiased gradient, $\mathbb { E } [ B _ { 2 } ] = 0$ . Then, we bound $B _ { 3 }$ .

$$
B _ {3} = \frac {\eta_ {t} ^ {2}}{m} \sum_ {k \in S ^ {t}} \| \nabla F _ {k} (w _ {k} ^ {t} \| ^ {2} \leq \frac {2 L \eta_ {t} ^ {2}}{m} \sum_ {k \in S ^ {t}} (F _ {k} (w _ {k} ^ {t}) - F _ {k} ^ {*})
$$

Last, we bound $B _ { 4 }$

$$
B _ {4} = \eta_ {t} ^ {2} \mathbb {E} [ \| \sum_ {k \in S ^ {t}} \frac {1}{m} (g _ {k} (w _ {k} ^ {t}, \xi_ {k} ^ {t}) - \nabla F _ {k} (w _ {k} ^ {t}) \| ^ {2} ] \leq \frac {\eta_ {t} ^ {2}}{m} \alpha^ {2}
$$

Now, we use $B _ { 1 } , B _ { 2 } , B _ { 3 } , B _ { 4 }$ to bound $\lVert \overline { { \boldsymbol { w } } } ^ { t + 1 } - \boldsymbol { w } ^ { * } \rVert ^ { 2 }$ .

$$
\mathbb {E} [ \| \overline {{w}} ^ {t + 1} - w ^ {*} \| ^ {2} ]
$$

$$
\leq (1 - \eta_ {t} \mu) \mathbb {E} [ \| \overline {{w}} ^ {t} - w ^ {*} \| ^ {2} ] + 1 6 \eta_ {t} ^ {2} \tau^ {2} G ^ {2}
$$

$$
+ (4 \eta_ {t} ^ {2} \tau + \frac {1}{\tau} - \frac {\eta_ {t} \mu}{m \tau}) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2} + \frac {\eta_ {t} ^ {2} \alpha^ {2}}{m} + B _ {5}
$$

where:

$$
B _ {5} = \frac {4 L \eta_ {t} ^ {2}}{m} \sum_ {k \in S ^ {t}} (F _ {k} (w _ {k} ^ {t}) - F _ {k} ^ {*})
$$

$$
- \frac {2 \eta_ {t}}{m} \mathbb {E} [ \sum_ {k \in S ^ {t}} (F _ {k} (w ^ {t}) - F _ {k} (w ^ {*})) ]
$$

Let’s bound $B _ { 5 }$

$$
B _ {5} \leq 1 6 \eta_ {t} ^ {2} \tau^ {2} G ^ {2} + (4 \eta_ {t} ^ {2} \tau + \frac {1}{\tau}) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

$$
- \nu_ {t} (1 - \eta_ {t} L) \overline {{\rho}} (\mathbb {E} [ F (\overline {{w}} _ {k} ^ {t}) ] - \sum_ {k = 1} ^ {K} p _ {k} F _ {k} ^ {*}) + 2 \eta_ {t} \widetilde {\rho} \Gamma
$$

$$
\leq 1 6 \eta_ {t} ^ {2} \tau^ {2} G ^ {2} + (4 \eta_ {t} ^ {2} \tau + \frac {1}{\tau}) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

$$
- \frac {3 \eta_ {t} \mu \overline {{\rho}}}{8} \mathbb {E} [ \| \overline {{w}} _ {k} ^ {t} - w ^ {*} \| ^ {2} ] - 2 \eta_ {t} \overline {{\rho}} \Gamma + 6 \eta_ {t} ^ {2} \overline {{\rho}} L \Gamma + 2 \eta_ {t} \widetilde {\rho} \Gamma
$$

$$
= - \frac {3 \eta_ {t} \mu \overline {{\rho}}}{8} \mathbb {E} [ \| \overline {{w}} _ {k} ^ {t} - w ^ {*} \| ^ {2} ] + 2 \eta_ {t} \Gamma (\widetilde {\rho} - \overline {{\rho}})
$$

$$
+ \eta_ {t} ^ {2} (6 \overline {{\rho}} L \Gamma + 1 6 \tau^ {2} G ^ {2}) + (4 \eta_ {t} ^ {2} \tau + \frac {1}{\tau}) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

Then, we use $B _ { 5 }$ to bound $\lVert \overline { { \boldsymbol { w } } } ^ { t + 1 } - \boldsymbol { w } ^ { * } \rVert ^ { 2 }$ .

$$
\mathbb {E} \left[ \left\| \overline {{w}} ^ {t + 1} - w ^ {*} \right\| ^ {2} \right] \leq \left(1 - \eta_ {t} \mu \left(1 + \frac {3 \bar {\rho}}{8}\right)\right) \mathbb {E} \left[ \left\| \overline {{w}} ^ {t} - w ^ {*} \right\| ^ {2} \right]
$$

$$
+ \eta_ {t} ^ {2} (3 2 \tau^ {2} G ^ {2} + \frac {\alpha^ {2}}{m ^ {2}} + 6 \overline {{\rho}} L \Gamma) + 2 \eta_ {t} \Gamma (\widetilde {\rho}
$$

$$
\left. - \bar {\rho}\right) + \left(8 \eta_ {t} ^ {2} \tau + \frac {2}{\tau} - \frac {\eta_ {t} \mu}{m \tau}\right) \sum_ {k \in S ^ {t}} \| n _ {k} ^ {t} \| ^ {2}
$$

Now we have bounded the expected difference of global model between the t-th epoch and the t + 1-th epoch. We assume that the learning rate is fixed, i.e. $\eta _ { t } = \eta$ . We define $\Delta _ { t } =$ $\mathbb { E } [ \lVert \overline { { w } } ^ { t } - w ^ { * } \rVert ^ { 2 } ]$ Then by reduction, we can get:

$$
\Delta_ {t} \leq (1 - \eta \mu (1 + \frac {3}{8} \overline {{\rho}})) ^ {t} (\Delta_ {0}
$$

$$
- \frac {\eta (3 2 \tau^ {2} G ^ {2} + \frac {\sigma^ {2}}{m} + 6 \overline {{\rho}} L \Gamma) + 2 \Gamma (\widetilde {\rho} - \overline {{\rho}})}{\mu (1 + \frac {3}{8} \overline {{\rho}})}
$$

$$
+ \frac {\eta (3 2 \tau^ {2} G ^ {2} + \frac {\sigma^ {2}}{m} + 6 \overline {{\rho}} L \Gamma)}{\mu (1 + \frac {3}{8} \overline {{\rho}})} + \frac {2 \Gamma (\widetilde {\rho} - \overline {{\rho}})}{\mu (1 + \frac {3}{8} \overline {{\rho}})} + (8 \tau \eta^ {2}
$$

$$
\left. - \frac {\mu}{m \tau} \eta + \frac {2}{\tau}\right) \sum_ {i = 0} ^ {t} \left(1 - \eta \mu \left(1 + \frac {3}{8} \bar {\rho}\right)\right) ^ {t - i} \sum_ {k \in S ^ {i}} \| n _ {k} ^ {i} \| ^ {2}
$$

Notice that $\begin{array} { r } { \Delta _ { t } \leq \frac { 2 } { \mu } ( F ( \overline { { w } } ^ { t } ) - F ^ { * } ) } \end{array}$ , and L-smoothness, we have:

$$
F (\overline {{w}} ^ {t}) - F ^ {*}
$$

$$
\leq (1 - \eta \mu (1 + \frac {3}{8} \overline {{\rho}})) ^ {t} (\frac {L}{\mu} (F (\overline {{w}} ^ {0}) - F ^ {*})
$$

$$
- \frac {L (\eta (3 2 \tau^ {2} G ^ {2} + \frac {\sigma^ {2}}{m} + 6 \overline {{\rho}} L \Gamma) + 2 \Gamma (\widetilde {\rho} - \overline {{\rho}}))}{2 \mu (1 + \frac {3}{8} \overline {{\rho}})}
$$

$$
+ \frac {L \eta (3 2 \tau^ {2} G ^ {2} + \frac {\sigma^ {2}}{m} + 6 \overline {{\rho}} L \Gamma)}{2 \mu (1 + \frac {3}{8} \overline {{\rho}})} + \frac {L \Gamma (\widetilde {\rho} - \overline {{\rho}})}{\mu (1 + \frac {3}{8} \overline {{\rho}})} + (4 L \tau \eta^ {2}
$$

$$
\left. - \frac {L \mu}{2 m \tau} \eta + \frac {L}{\tau}\right) \sum_ {i = 0} ^ {t} \left(1 - \eta \mu \left(1 + \frac {3}{8} \bar {\rho}\right)\right) ^ {t - i} \sum_ {k \in S ^ {i}} \| n _ {k} ^ {i} \| ^ {2}
$$

Now we complete the proof.

□