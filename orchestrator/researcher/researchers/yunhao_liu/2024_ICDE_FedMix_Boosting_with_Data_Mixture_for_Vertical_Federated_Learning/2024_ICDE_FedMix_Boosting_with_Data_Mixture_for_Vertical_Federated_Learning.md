# FedMix: Boosting with Data Mixture for Vertical Federated Learning

Yihang Cheng1, Lan Zhang12, Junyang Wang1, Xiaokai Chu3, Dongbo Huang3, Lan Xu3

1University of Science and Technology of China, Hefei, China

2Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, China

3Tencent, Shanghai, China

yihangcheng@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, iswangjy@mail.ustc.edu.cn

chuxiaokai@ict.ac.cn, andrewhuang@tencent.com, lanxu@tencent.com

Abstract—The need to safeguard data privacy and adhere to regulations such as GDPR creates data silos and has prompted the emergence and widespread adoption of techniques for distributed databases. To effectively explore the value of data across multiple organizations, techniques for data management, data analysis and data functionality from distributed databases have been proposed. Recently, Vertical Federated Learning (VFL) has become a solution with growing interests, which enables collaborative model training when data features are partitioned into multiple parts and are held by different parties. However, typical VFL methods heavily rely on private set intersection (PSI) to align data before training and only utilize aligned data for training. In this work, we provide a theoretical analysis to show that unaligned data actually contains valuable and rich features, and a thoughtful design that harnesses the potential of unaligned samples to significantly improve the performance of VFL models. Regrettably, many existing methods simply discard unaligned data, resulting in an irrecoverable loss of performance. To address this data sacrifice problem, we introduce the concept of data mixture, which enables the utilization of both aligned and unaligned data during training. Building upon the data mixture idea, we present FedMix, the first on-the-fly and distribution-agnostic framework designed to boost the performance of VFL models by leveraging unaligned data. A data seasoning approach is also designed to utilize auxiliary data lacking label information. Evaluations on diverse datasets under different settings demonstrate the effectiveness of the proposed FedMix compared with various SOTA approaches. FedMix achieves up to 15% model performance improvement and 30.5 hours time cost reduction.

# I. INTRODUCTION

In the modern digital era, data has become a critical asset for organizations. The ability to analyze and extract insights from data is key to driving business decisions, understanding consumer behavior, and enhancing operational efficiency. There are already numerous studies focusing on data management and mining [1, 30, 33, 24] in the centralized scenario. However, with regulations such as GDPR [38], the landscape of data management and analysis has significantly changed, giving rise to distributed databases characterized by multiple data silos across various organizations, in which the transfer of raw data is typically restricted. Consequently, the exploration of methods for data management, data analysis and data functionality from distributed databases in a privacy-preserving way without the exchange of local data has emerged as a pressing topic.

Lan Zhang is the corresponding author.

![](images/766e5258f824bdb274c99df72096d53d028f8e2bbd307989c7d30a709e2af246.jpg)



Fig. 1: A typical data distribution in VFL. A classic VFL training process leverages only the aligned data Ya, Da0 , Da1 (highlighted in the red square) but discards other data.

On the other hand, machine learning has been rapidly developed and gradually transformed from a simple target prediction tool into a powerful means of data analysis, capable of effectively uncovering the potential value in data. And, how to apply machine learning to distributed databases for data silos has become a growing area of interest for researchers [29, 45, 25, 16, 26]. Federated Learning (FL) [28], first proposed by Google in 2016, is one common technique in this area to enable collaborative model training without revealing any local data among parties. To accommodate different scenarios, the concept of FL is subsequently divided into three categories [27]: Horizontal Federated Learning (HFL), Vertical Federated Learning (VFL), and Federated Transfer Learning (FTL). Among them, VFL is designed for situations where data features are partitioned into multiple parts, each held by different parties. This mode can effectively break information silos and has been widely adopted in various industries, such as advertising [35] and finance [20].

Problem: data sacrifice. However, a typical VFL training process [48, 27, 41] requires parties to first perform private set intersection (PSI) [14] to find aligned data, i.e., data with aligned IDs, which significantly reduces the amount of usable data. As the example of typical data distribution in VFL in Fig. 1, only the aligned data Da0 and Da1 as well as the labels a can be utilized for training, and the rest of the data is discarded, though unaligned data usually contain rich valuable features. We refer to this problem as data sacrifice, as formally defined in Definition 1. Several methods have been proposed to mitigate this problem, which can be divided into two categories: (1) Data completion [19, 47, 43] is the most straightforward solution. Reconstruction techniques such as generative adversarial networks (GAN) [10] are applied to estimate missing features of unaligned data. After that, all data can be used in the training of VFL. (2) Extractor improvement [7, 12] leverages unsupervised learning methods like deep reconstruction-classification network (DRCN) [9] or autoencoder [14] to improve the performance of extractors (i.e. the bottom model) of each party. The training of VFL is then built on top of these extractors. We find that both data completion and extractor improvement require a preparing stage for either unaligned data reconstruction or the training of extractors. The preparing stage is extremely time-consuming, which takes 30% to 125% of the running time of the whole training stage as shown in Table V. Besides, those two methods are hard to apply in cases when the feature distribution is biased (see Fig. 8) or when the proportion of unaligned data is too large (see Fig. 9). In these cases, those two methods can only achieve 0.1% 3% performance improvement.

In this work, we aim to find a general on-the-fly solution for the data sacrifice problem to improve the performance of VFL models by leveraging unaligned data. To find such a solution, we need to answer three key questions:

1) Can unaligned data indeed enhance model performance? Quantitatively characterizing VFL model performance, particularly in relation to the influence of additional unaligned data, poses significant challenges. This work, to the best of our knowledge, presents the first attempt to provide a theoretical analysis of the contribution of unaligned data to the VFL model. Besides, previous methods addressing the data sacrifice problem have provided little theoretical guarantees.

2) How to incorporate unaligned data seamlessly into the VFL training process, eliminating the need for additional preparation? Existing methods necessitate an extra preparing stage, resulting in substantial extra time costs. Besides, they are difficult to achieve good performance when there is significant bias in feature distribution. Therefore, it is urgent to seek a more effective approach to directly utilize unaligned data in VFL training.

3) How to deal with the absence of label information for some unaligned data? Some unaligned data, especially in passive parties, do not come with label information, and we refer to them as the auxiliary data. Simply discarding them means missing out on opportunities for significant improvement, as shown by the results in Fig. 12 (an approximate 20% improvement in the overall performance). Therefore, we must also explore strategies for reconstructing label information.

New framework: FedMix. To tackle the above challenges and resolve the data sacrifice problem, a series of technical advancements are required. First, we formalize the data sacrifice problem and analyze the potential improvements that can be achieved with unaligned data. We provide a theoretical analysis of this problem and introduce Theorem 1, demonstrating that the inclusion of unaligned data in the VFL training results in a closer alignment of data distribution to the global distribution (from which all training data are sampled), and indeed improve the performance of the VFL model. This analysis serves as the cornerstone of our new framework FedMix. Second, we introduce the concept of data mixture and design a data mixer with two distinct random selection strategies. These innovations enable the efficient utilization of unaligned data during the VFL training process. Data mixture, as the core idea of our work, randomly and independently selects one sample to match each aligned sample and sums them with a weight-average parameter from Beta distribution. Specifically, the data mixer provides two random selection strategies to guide the collaborative selection of samples from the aligned and unaligned datasets within each party. Third, when dealing with auxiliary data lacking label information, we design a data seasoning technique to generate pseudo-labels for such data during the training of VFL and incorporate them into the unaligned dataset. This enables their utilization alongside the data mixer. We implement our theorybacked framework FedMix as a general on-the-fly solution to address the data sacrifice problem. Our extensive experiments, conducted on diverse datasets, various data distribution settings, ablation studies, and comparison with state-of-the-art methods, consistently demonstrate the superior performance of FedMix.

Contributions. We summarize the three key contributions of this work as follows:

• We present a theoretical analysis of the data sacrifice problem, and to the best of our knowledge, the first theoretical analysis of the potential improvement brought by unaligned data to the VFL model.

We introduce FedMix, the first on-the-fly and distributionagnostic framework designed to address the data sacrifice problem. Within FedMix, we propose an efficient data mixer based on the core idea of data mixture, along with a data seasoning approach, enabling the full utilization of unaligned and auxiliary data during the VFL training stage.

• We have implemented FedMix and conducted extensive evaluations on various datasets. Comparisons with state-of-theart methods show the superiority of FedMix in dealing with the data sacrifice problem, as it shows notable advantages in both model performance and time cost. Specifically, FedMix achieves up to 15% model performance improvement and a substantial reduction in time cost by 30.5 hours. Our experimental results, conducted across different data distribution settings, showcase the robustness of FedMix, with consistent performance improvements ranging from 3% to 16%. The ablation study confirms the significance of the two key modules within FedMix (data mixer and data seasoning), as they each contribute to improvements of 12% and 4%, respectively.

# II. RELATED WORK

Current work about the data sacrifice problem can be mainly divided into two categories: data completion and extractor improvement. Below we give a detailed description of them.

Data completion. The most straightforward way is to fill in missing features of unaligned data and treat them as normal data in later VFL training. FedCVT [19] computes the similarity between features in active and passive parties with scaled dotproduct attention [37] through aligned data, and then estimates the missing features for unaligned data based on the computed similarity score. FedMC [43] introduces a common projection space and unaligned data from different parties can be paired together if they are close to each other in the projection space. FedDA [47] trains a generative adversarial network (GAN) [10] on aligned data to directly generate the missing features. However, these methods heavily rely on a sufficient number of known features and aligned samples for estimation. Furthermore, they primarily focus on the two-party scenario for efficiency.

TABLE I: Comparison of our proposed FedMix and current methods designed for the data sacrifice problem. 

<table><tr><td>Method</td><td>Robust to Feature Dist.</td><td>Robust to Sample Dist.</td><td>Handling Unlabeled</td><td>Avoiding Extra Stage</td></tr><tr><td>Data completion [19, 43, 47]</td><td>✗</td><td>✗</td><td>✗</td><td>✗</td></tr><tr><td>Extractor imprv. [12, 2, 7]</td><td>✗</td><td>✗</td><td>√</td><td>✗</td></tr><tr><td>FedMix</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

TABLE II: Notation table. 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $c$ </td><td>Number of passive parties in VFL</td></tr><tr><td> $\mathcal{D}_{i}^{a}, \mathcal{Y}^{a}$ </td><td>Aligned data and label in party  $i$ </td></tr><tr><td> $\mathcal{D}_{i}^{u}, \mathcal{Y}_{i}^{u}$ </td><td>Unaligned data and label in party  $i$ </td></tr><tr><td> $\mathcal{D}_{i}^{aux}$ </td><td>Auxiliary data without label in party  $i$ </td></tr><tr><td> $\gamma_{i}$ </td><td>Ratio of unaligned and auxiliary data in party  $i$ </td></tr><tr><td> $\gamma$ </td><td>Ratio of unaligned and auxiliary data from global perspective</td></tr><tr><td> $d_{i}$ </td><td>Number of features in party  $i$ </td></tr></table>

Extractor improvement. Another way to utilize unaligned data is to train a better extractor (i.e. the bottom model of VFL) for local data representatives. FedHSSL [12] and SS-VFL [2] use autoencoder [21] and self-supervised learning to leverage contrastive learning to learn common representatives for each party. VFLFS [7] performs local representation learning for each party with a deep reconstruction-classification network (DRCN) [9]. Since the above local training process requires no other party to participate, it can make full use of aligned and unaligned data for a better representative extractor alone and apply it to the training of VFL later. However, if there are not enough features, the extractor cannot be trained well enough for VFL. Besides, the training of VFL continues to rely solely on aligned samples. This limitation hinders the potential for further performance enhancement, particularly in scenarios where the ratio of aligned data is low.

Summary. From the analysis of current works, we find their limitations in the ratio of known features and aligned data. We also notice that an extra preparing stage is required for both of them, which makes the training dramatically slow down. Our experiment results in Figs. 8 and 9 show only $0 . 2 \% \sim 2 \%$ improvement when the fraction of the number of features between the active and passive parties is 1 : 9 or

![](images/907f713ee6b58b93ec996bf5f5cd45886c67a8f26a5690378fa21cb7f2268f09.jpg)



Fig. 2: The workflow of VFL.

9 : 1, and 0.1% ∼ 1.5% when only $2 / 7$ of all data is aligned. Besides, an unaffordable time cost can be seen caused by the extra preparing stage from Table V. The comparison of current works and our framework FedMix (described in Section V) are listed in Table I. With FedMix, we can solve the data sacrifice problem during the training stage of VFL without worrying about a lack of known features or aligned data.

# III. PROBLEM FORMALIZATION

We first give the formalization of vertical federated learning. Based on that, we provide the definition of the data sacrifice problem. And finally, we describe our design scope and goals. Table II provides the key notations used throughout the paper for quick search.

# A. Vertical Federated Learning

A typical training process of VFL is done among several parties (one active party and c passive parties). Without loss of generality, let subscript 0 represent the active party and let subscript $1 \sim c$ represent each passive party. Each party i holds a dataset $\mathcal { D } _ { i }$ within its own feature space ${ \mathcal { F } } _ { i }$ (i.e. $\forall x _ { i } \in \mathcal { D } _ { i } , x _ { i } \sim \mathcal { F } _ { i } )$ .

Data alignment. The parties first find their aligned data by techniques such as private set intersection, so that the actual dataset in each party i used in VFL later is $\mathcal { D } _ { i } ^ { a }$ , which is a subset of $\mathcal { D } _ { i } ~ ( \mathcal { D } _ { i } ^ { a } \subseteq \mathcal { D } _ { i } )$ . Besides, the active party holds the corresponding labels ${ \mathcal { V } } ^ { a }$ for the aligned dataset $\mathcal { D } ^ { a } = \{ \mathcal { D } _ { i } ^ { a }$ : $0 \leq i \leq c \}$ .

VFL training. After finding the aligned dataset $\mathcal { D } ^ { a }$ and labels ${ \mathcal { V } } ^ { a }$ , the training of VFL starts. Referring to the workflow of VFL shown in Fig. 2, in every communication round:

1) First, each party i independently calculates the representatives of their aligned dataset $\mathcal { D } _ { i } ^ { a }$ with its bottom model: $r _ { i } ^ { a } = f _ { i } ( \theta _ { i } ; x _ { i } ^ { a } ) , x _ { i } ^ { a } \in \mathcal { D } _ { i } ^ { a }$ .   
2) Then, by collecting the representatives computed in all parties, the active party feeds them into a top model to output the prediction: $p ^ { a } = g ( \phi ; r _ { 0 } ^ { a } , r _ { 1 } ^ { a } , \cdot \cdot \cdot , r _ { c } ^ { a } )$ .   
3) And finally, the active party computes the loss function $l \ = \ L ( y ^ { a } , p ^ { a } ) , \bar { y } ^ { a } \ \in \ \mathcal { y } ^ { a }$ and performs backward gradient propagation to update top and bottom model parameters.

Target. VFL aims at training a joint model with the help of passive parties to achieve better performance, compared to training alone in the active party. And its target is to minimize the loss function below:

$$
\mathbb{E}(l) = \frac{1}{n}\sum_{\substack{x_{i}^{a}\in \mathcal{D}_{i}^{a}\\ y^{a}\in \mathcal{Y}^{a}}}L(y^{a},g(\phi ;f_{0}(\theta_{0};x_{0}^{a}),\dots ,f_{c}(\theta_{c};x_{c}^{a}))) \tag{1}
$$

If we do not care about the inner computation of the loss function, then Eq. (1) can be rewritten as:

$$
\mathbb {E} (l) = \frac {1}{n} \sum_ {\substack {x _ {i} ^ {a} \in \mathcal {D} _ {i} ^ {a} \\ y ^ {a} \in \mathcal {Y} ^ {a}}} H \left(\varphi ; y ^ {a}, x _ {0} ^ {a}, \dots , x _ {c} ^ {a}\right) \tag{2}
$$

where each set of $\{ x _ { 0 } ^ { a } , \cdot \cdot \cdot , x _ { c } ^ { a } , y ^ { a } \}$ represents the features and corresponding label of one sample, and $n = | \mathcal { D } _ { i } ^ { a } |$ denotes the size of the training dataset.

# B. Data Sacrifice Problem

Now we can formalize the data sacrifice problem. Notice that $\mathcal { D } _ { i } ^ { a } \subseteq \mathcal { D } _ { i }$ , so we define $\mathcal { D } _ { i } ^ { x } = \mathcal { D } _ { i } - \mathcal { D } _ { i } ^ { a }$ to be the unaligned and auxiliary dataset in party i (i.e. $\mathcal { D } _ { i } ^ { x } \overset { \cdot } { = } \mathcal { D } _ { i } ^ { u } \cup \mathcal { D } _ { i } ^ { a u x } )$ . And we further define a local data sacrifice rate $\gamma _ { i } = | \mathcal { D } _ { i } ^ { x } | / | \mathcal { D } _ { i } |$ and a global data sacrifice rate $\textstyle \gamma = \sum _ { i = 0 } ^ { c } | { \mathcal { D } } _ { i } ^ { x } | / | { \mathcal { D } } |$ , where $\textstyle { \mathcal { D } } = \bigcup _ { i = 1 } ^ { c } { \mathcal { D } } _ { i }$ is the total data collection which can be used for training. The local and global data sacrifice rate has the following relationship:

Lemma 1. Given one active party and c passive parties with local data sacrifice rates $\gamma _ { i } = | \mathcal { D } _ { i } ^ { x } | / | \mathcal { D } _ { i } | , 0 \leq i \leq c$ and the global data sacrifice rate $\textstyle \gamma = \sum _ { i = 0 } ^ { c } | \mathcal { D } _ { i } ^ { x } | / | \mathcal { D } |$ , then $\gamma _ { i } , 0 \leq i \leq$ c and $\gamma$ satisfies

$$
\sum_ {i = 0} ^ {c} \frac {1}{1 - \gamma_ {i}} = \frac {1}{1 - \gamma} + c
$$

Proof. Since $\begin{array} { r } { | \mathcal { D } | = | \mathcal { D } ^ { a } | + \sum _ { i = 0 } ^ { c } | \mathcal { D } _ { i } ^ { x } | , | \mathcal { D } _ { i } | = | \mathcal { D } _ { i } ^ { a } | + | \mathcal { D } _ { i } ^ { x } | } \end{array}$ and $n = | \mathcal { D } ^ { a } | = | \mathcal { D } _ { i } ^ { a } | , \forall i , 0 \leq i \leq c ,$ we have

$$
\frac {1}{1 - \gamma_ {i}} = \frac {1}{1 - | \mathcal {D} _ {i} ^ {x} | / | \mathcal {D} _ {i} |} = \frac {| \mathcal {D} _ {i} |}{| \mathcal {D} _ {i} | - | \mathcal {D} _ {i} ^ {x} |} = \frac {| \mathcal {D} _ {i} |}{| \mathcal {D} _ {i} ^ {a} |} = \frac {| \mathcal {D} _ {i} |}{n}
$$

$$
\begin{array}{l} \frac {1}{1 - \gamma} = \frac {1}{1 - \sum_ {i = 0} ^ {c} | \mathcal {D} _ {i} ^ {x} | / | \mathcal {D} |} = \frac {| \mathcal {D} |}{| \mathcal {D} | - \sum_ {i = 0} ^ {c} | \mathcal {D} _ {i} ^ {x} |} \\ = \frac {| \mathcal {D} |}{| \mathcal {D} ^ {a} |} = \frac {| \mathcal {D} |}{n} \\ \end{array}
$$

And $\begin{array} { r } { | \mathcal { D } | ~ = ~ | \mathcal { D } ^ { a } | + \sum _ { i = 0 } ^ { c } | \mathcal { D } _ { i } ^ { x } | ~ = ~ n + \sum _ { i = 0 } ^ { c } ( | \mathcal { D } _ { i } | - n ) ~ = ~ } \end{array}$ $\textstyle \sum _ { i = 0 } ^ { c } \left| { \mathcal { D } } _ { i } \right| - c n$ . Thus,

$$
\sum_ {i = 0} ^ {c} \frac {1}{1 - \gamma_ {i}} = \sum_ {i = 0} ^ {c} \frac {| \mathcal {D} _ {i} |}{n} = \frac {| \mathcal {D} | + c n}{n} = \frac {1}{1 - \gamma} + c
$$

![](images/c12c6a22865a0c5cfddc034850f32a5a138d023c82e8c57539189148a7aef661.jpg)

Here, the domain of $\gamma _ { i }$ and $\gamma$ is limited in [0, 1). This is a reasonable assumption, because if $\exists \gamma _ { i } = 1$ , party i has no aligned data and should not take part in VFL training.

Below we provide the formal definition of the data sacrifice problem:

Definition 1 (Data Sacrifice). We call that a data sacrifice problem happens in VFL training, if ∃ a party i, such that its local data sacrifice rate $\gamma _ { i } > 0$ , which also leads to global data sacrifice rate $\gamma > 0$ .

# C. Design Scope and Goals

We focus on model performance improvement with unaligned data during the training stage of VFL. Other potential training improvement techniques (i.e. selecting important parties [15] or features [3]) without unaligned data are out of the scope of this work.

We aim to solve the data sacrifice problem and answer the three key questions proposed in Section I. The first question is solved by our proof in Section IV of the effectiveness of adding unaligned data to the training stage of VFL. Based on the theoretical analysis, we propose FedMix in Section V with the following design goals for the remaining two questions:

1) A general on-the-fly solution with no limitation to data distribution. Current works require an extra preparing stage (which leads to extra time costs) and have strict requirements for data distribution. However, today’s model deployment deadline requirement and uncontrollable data flow ask for a general on-the-fly solution.   
2) A patch to utilize the auxiliary data. Since unaligned data, especially those in passive parties, usually contain no label information (i.e. the auxiliary data), an ideal solution should cover this common issue.

# IV. THEORETICAL ANALYSIS OF DATA SACRIFICE

To solve the data sacrifice problem in Definition 1, we should first carefully analyze how data sacrifice influences the performance of the VFL model.

Starting point: Solving the data sacrifice problem is equivalent to letting the distribution of the training dataset be close to the global distribution. Adding unaligned data to the training generates a better distribution profile of some features (depending on what features unaligned data has). The VFL model trained on a dataset with less bias from global distribution should have a better performance from intuition.

Lemma 2 introduced by Kumar et al. [23] provides us a theoretical approach to measure the potential performance difference between two distributions.

Lemma 2 ([23]). Given a function $h : X \times Y \to [ 0 , 1 ]$ , define its smoothed version as $\bar { h } ( x , y ) = \mathbb { E } _ { x ^ { \prime } \sim S ( x ) } [ H ( x ^ { \prime } , y ) ]$ . Then, $\forall \tilde { \mathcal { D } }$ such that $W _ { 1 } ^ { d } ( { \mathcal { D } } , \tilde { { \mathcal { D } } } ) \leq \epsilon .$ ,

$$
\left| \mathbb {E} _ {(x _ {1}, y _ {1}) \sim \mathcal {D}} [ \bar {h} (x _ {1}, y _ {1}) ] - \mathbb {E} _ {(x _ {2}, y _ {2}) \sim \tilde {\mathcal {D}}} [ \bar {h} (x _ {2}, y _ {2}) ] \right| \leq \psi (\epsilon)
$$

where $x ^ { \prime } \sim S ( x )$ applies a randomized version of the input x sampled from a neighbor distribution S(x) around $x , \psi ( \cdot )$ is a concave increasing function, and $W _ { 1 } ^ { d } ( \cdot , \cdot )$ is the 1-Wasserstein distance between two distributions.

However, it is still hard to directly compute the 1-Wasserstein distance between two arbitrary distributions. So, inspired by Takatsu [34], we propose Lemma 3 to seek an upper bound of the 1-Wasserstein distance of two Gaussian distributions.

Lemma 3. Given two independent multivariate Gaussian distributions $G _ { 1 } = N ( \mu _ { 1 } , \Sigma _ { 1 } )$ and $G _ { 2 } = N ( \mu _ { 2 } , \Sigma _ { 2 } )$ on $\mathbb { R } ^ { d }$ , let $\lambda _ { k , 1 } , \cdots , \lambda _ { k , d }$ and $v _ { k , 1 } , \cdots , v _ { k , d }$ be the eigenvalues and corresponding eigenvectors of the covariance matrix $\Sigma _ { k }$ for $k \in \{ 1 , 2 \}$ . Then, the 1-Wasserstein distance of $G _ { 1 }$ and $G _ { 2 }$ is bounded by

$$
\begin{array}{l} W _ {1} ^ {d} (G _ {1}, G _ {2}) \leq \| \mu_ {1} - \mu_ {2} \| \\ + \sqrt {\sum_ {i = 1} ^ {d} \left[ \lambda_ {1 , i} + \lambda_ {2 , i} - 2 \sqrt {\lambda_ {1 , i} \lambda_ {2 , i}} \langle v _ {1 , i} , v _ {2 , i} \rangle \right]} \\ \end{array}
$$

Proof. From the triangle inequality for the 1-Wasserstein distance,

$$
\begin{array}{l} W _ {1} ^ {d} (G _ {1}, G _ {2}) \leq W _ {1} ^ {d} (G _ {1}, N (\mu_ {2}, \Sigma_ {1})) + W _ {1} ^ {d} (N (\mu_ {2}, \Sigma_ {1}), G _ {2}) \\ \leq \| \mu_ {1} - \mu_ {2} \| + W _ {1} ^ {d} (N (0, \Sigma_ {1}), N (0, \Sigma_ {2})) \\ \end{array}
$$

Now we consider another sequence of random variables $R _ { i } \sim N ( 0 , 1 ) , 1 \leq i \leq d ,$ then $\begin{array} { r } { S _ { k } = \sum _ { i = 1 } ^ { d } R _ { i } \sqrt { \lambda _ { k , i } } v _ { k , i } \sim } \end{array}$ $N ( 0 , \Sigma _ { k } ) , k \in \{ 1 , 2 \}$ . From the definition of the Wasserstein distance,

$$
W _ {1} ^ {d} (N (0, \Sigma_ {1}), N (0, \Sigma_ {2})) ^ {2} \leq (\mathbb {E} \| S _ {1} - S _ {2} \|) ^ {2} \leq \mathbb {E} (\| S _ {1} - S _ {2} \| ^ {2})
$$

Here,

$$
\begin{array}{l} \| S _ {1} - S _ {2} \| ^ {2} = \left\| \sum_ {i = 1} ^ {d} R _ {i} \left[ \sqrt {\lambda_ {1 , i}} v _ {1, i} - \sqrt {\lambda_ {2 , i}} v _ {2, i} \right] \right\| ^ {2} \\ = \sum_ {i = 1} ^ {d} R _ {i} ^ {2} \left\| \sqrt {\lambda_ {1 , i}} v _ {1, i} - \sqrt {\lambda_ {2 , i}} v _ {2, i} \right\| ^ {2} + \\ \sum_{\substack{1\leq i,j\leq d\\ i\neq j}}R_{i}R_{j}\Big\langle \sqrt{\lambda_{1,i}} v_{1,i} - \sqrt{\lambda_{2,i}} v_{2,i},\sqrt{\lambda_{1,j}} v_{1,j} - \sqrt{\lambda_{2,j}} v_{2,j}\Big\rangle \\ \end{array}
$$

Notice that in the above equation, $\begin{array} { r l } {  { \big \| \sqrt { \lambda _ { 1 , i } } v _ { 1 , i } - \sqrt { \lambda _ { 2 , i } } v _ { 2 , i } \big \| ^ { 2 } } } \end{array}$ and $\langle \sqrt { \lambda _ { 1 , i } } v _ { 1 , i } - \sqrt { \lambda _ { 2 , i } } v _ { 2 , i } , \sqrt { \lambda _ { 1 , j } } v _ { 1 , j } - \sqrt { \lambda _ { 2 , j } } v _ { 2 , j } \rangle$ are constant values. Since $R _ { i } \sim N ( 0 , 1 )$ , we have $\mathbb { E } ( R _ { i } ^ { 2 } ) = 1$ and $\mathbb { E } ( R _ { i } ) = 0$ . And $v _ { k , i } , 1 \leq i \leq d$ are orthogonal to each other for $k = \{ 1 , 2 \}$ . So,

$$
\begin{array}{l} \mathbb {E} (\| S _ {1} - S _ {2} \| ^ {2}) = \sum_ {i = 1} ^ {d} \left\| \sqrt {\lambda_ {1 , i}} v _ {1, i} - \sqrt {\lambda_ {2 , i}} v _ {2, i} \right\| ^ {2} \\ = \sum_ {i = 1} ^ {d} \left[ \lambda_ {1, i} + \lambda_ {2, i} - 2 \sqrt {\lambda_ {1 , i} \lambda_ {2 , i}} \langle v _ {1, i}, v _ {2, i} \rangle \right] \\ \end{array}
$$

Finally,

$$
\begin{array}{l} W _ {1} ^ {d} (G _ {1}, G _ {2}) \leq \| \mu_ {1} - \mu_ {2} \| + W _ {1} ^ {d} (N (0, \Sigma_ {1}), N (0, \Sigma_ {2})) \\ \leq \| \mu_ {1} - \mu_ {2} \| + \sqrt {\mathbb {E} (\| S _ {1} - S _ {2} \| ^ {2})} \\ = \| \mu_ {1} - \mu_ {2} \| + \sqrt {\sum_ {i = 1} ^ {d} \left[ \lambda_ {1 , i} + \lambda_ {2 , i} - 2 \sqrt {\lambda_ {1 , i} \lambda_ {2 , i}} \langle v _ {1 , i} , v _ {2 , i} \rangle \right]} \\ \end{array}
$$

![](images/1eb4dc0729c7413a6a2f57199374c8145975d77d7d3403bb07d651e3f0e7a923.jpg)

With the upper bound of the 1-Wasserstein distance of two Gaussian distributions, we can finally propose Theorem 1, which shows that by adding unaligned data to solve the data sacrifice problem can effectively improve the performance of the VFL model from the perspective of probability theory.

Theorem 1. Let the global distribution of d features be $G =$ $N ( \mu , \sigma ^ { 2 } ) ^ { d }$ . Suppose each party holds data of $d _ { i }$ unique features so that $\textstyle d = \sum _ { i = 0 } ^ { c } d _ { i }$ . Given a dataset (with distribution $G ^ { \prime } )$ of size n and a given probability $p ,$ there exists a dataset drawn from the same global distribution of size $m _ { p }$ such that under the probability $p ,$ the model trained with the new dataset (with distribution $\tilde { G } )$ has a tighter bound in Lemma 2.

Proof. Define $G = N ( \mu , \Sigma ) = N ( \mu , \sigma ^ { 2 } ) ^ { d } , G ^ { \prime } = N ( \mu ^ { \prime } , \Sigma ^ { \prime } ) =$ $N ( \mu ^ { \prime } , { \sigma ^ { \prime } } ^ { 2 } ) ^ { d }$ and $\tilde { G } ~ = ~ \tilde { N } ( \tilde { \mu } _ { 0 } , \tilde { \sigma } _ { 0 } ^ { \perp } ) ^ { d _ { 0 } } \times \cdots \times N ( \tilde { \mu } _ { c } , \tilde { \sigma } _ { c } ^ { 2 } ) ^ { d _ { c } }$ , respectively, on $\mathbb { R } ^ { d }$ . Since $\Sigma , \ \Sigma ^ { \prime }$ and Σ˜ are diagonal matrices, their covariance matrices have the same eigenvectors $( \langle v _ { 1 , i } , v _ { 2 , i } \rangle = 1$ , ∀i in Lemma 3). Thus, the 1-Wasserstein distance of G and $G ^ { \prime }$ is bounded by

$$
\begin{array}{l} W _ {1} ^ {d} (G, G ^ {\prime}) \leq \| \mu - \mu^ {\prime} \| + \sqrt {\sum_ {i = 0} ^ {c} d _ {i} (\sigma^ {2} + \sigma_ {i} ^ {2} - 2 \sigma \sigma^ {\prime})} \\ = \| \mu - \mu^ {\prime} \| + \sqrt {\sum_ {i = 0} ^ {c} d _ {i} (\sigma - \sigma^ {\prime}) ^ {2}} = \epsilon^ {\prime} \\ \end{array}
$$

Similarly, the 1-Wasserstein distance of G and $\tilde { G }$ is bounded by

$$
W _ {1} ^ {d} (G, \tilde {G}) \leq \| \mu - \tilde {\mu} \| + \sqrt {\sum_ {i = 0} ^ {c} d _ {i} (\sigma - \tilde {\sigma} _ {i}) ^ {2}} = \tilde {\epsilon}
$$

Next, we need to compare the relationship between $\epsilon ^ { \prime }$ and ˜. If we simply study from the perspective of expectation, due to no change in distribution, there would be the result $\mathbb { E } ( \epsilon ^ { \prime } ) = \mathbb { E } ( \tilde { \epsilon } )$ .

However, notice that the training data is sampled from the global distribution. So, $\mu ^ { \prime } \sim N ( \mu , \frac { \bar { \sigma } ^ { 2 } } { n } ) , ( n - 1 ) \frac { \sigma ^ { \prime 2 } } { \sigma ^ { 2 } } \sim \chi ^ { 2 } ( n - 1 )$ , and $\begin{array} { r } { \tilde { \mu _ { i } } \sim N ( \mu , \frac { \sigma ^ { 2 } } { n + m _ { n } } ) , ( n + m _ { p } - 1 ) \frac { \tilde { \sigma _ { i } } ^ { 2 } } { \sigma ^ { 2 } } \sim \chi ^ { 2 } ( n + m _ { p } - 1 ) } \end{array}$ σ2 Here, the variance of $\tilde { \mu _ { i } }$ and $\tilde { \sigma _ { i } }$ is smaller than $\mu ^ { \prime }$ and σ when $m _ { p } \geq 1$ . This prompts us to compare $\epsilon ^ { \prime }$ and ˜ from the perspective of probability theory.

As $m _ { p }$ grows large, $\tilde { \mu _ { i } }$ and $\tilde { \sigma _ { i } }$ tend to be closer and closer to μ and σ. At a certain point, given the probability $p ,$ there would be the result that $\| \mu - \tilde { \mu } \| < \| \mu - \mu ^ { \prime } \|$ and $| \sigma - \tilde { \sigma _ { i } } | < | \sigma - \sigma _ { i } ^ { \prime } |$ . $\mathbf { S } \mathbf { o } , \tilde { \epsilon } \le \epsilon ^ { \prime }$ in this case, which means that $W _ { 1 } ^ { d } ( G , { \tilde { G } } )$ has a tighter bound than $W _ { 1 } ^ { d } ( G , G ^ { \prime } )$ .

From Lemma 2, a tighter bound in the 1-Wasserstein distance also means a tighter bound for the model. □

With Theorem 1, we find the essence of potential performance improvement brought by solving the data sacrifice problem. Using the unaligned data which is ignored by the typical VFL training process leads to a closer data distribution compared to the global distribution which we may never know. As for a VFL model which trains on both aligned and unaligned data, it is more likely to perform better on the global data distribution.

![](images/ec82e8a99829780682117f5210187c3d41d9a7c3dd58fb1afb43f5266d46fa43.jpg)



Fig. 3: The overview of FedMix.

![](images/7f1638c13ec556932afe1d28006e6135b81bfac4e90e1b113326ab6b9b412436.jpg)  
Fig. 4: Data mixture.

# V. FRAMEWORK

# A. Overview

Backed by Theorem 1, we can now pay attention to the design of our new framework FedMix to solve the data sacrifice problem. FedMix consists of two main modules: a data mixer and a data seasoning.

The data mixer provides the fundamental function to mix the unaligned data with the aligned data to form a data mixture, which can be sent into the VFL model for training without worrying about the missing features of the unaligned data.   
• The data seasoning, on the other hand, is a patch to deal with the unaligned data without label information. It leverages semi-supervised learning to generate pseudo-labels for them and put them into the training stage, which is then taken over by the data mixer.

The overview of FedMix is shown in Fig. 3. Below we provide the details of the two modules.

# B. Data Mixer

Since the unaligned data is what other parties do not have, to utilize the unaligned data, the most important thing is to take care of the missing features which ought to be on other parties. As discussed in Section II, current works need an extra preparing stage before the training stage of VFL to achieve data completion or extractor improvement. We want a general on-the-fly solution during the training stage of VFL instead.

Inspiration: mixup. Mixup [46] is a widely-used data augmentation technique in centralized learning. It is primarily designed to train a more robust model with the same training dataset. Its idea is that during the training process, for each batch of data, the model randomly selects another batch Output : One mixed data produced by the data mixer.

Algorithm 1: Data Mixer   
Input : The number of passive parties c, the beta distribution parameter $\beta$ , the chosen random selection strategy, the number of features $d_{0}, \cdots, d_{c}$ in each party and the total number of features d. (AP: the active party)

Data : The aligned $\mathcal { D } _ { i } ^ { a }$ and unaligned $\mathcal { D } _ { i } ^ { u }$ datasets, and the corresponding label information $\mathcal { V } ^ { a } , \mathcal { V } _ { i } ^ { u }$ on each party $i , 0 \leq i \leq c .$

1 DataMixer:   
2 All parties choose one common aligned sample
3 foreach party i do
4    selects the features $x_{i}^{a} \in D_{i}^{a}$ of this sample
5 AP selects the label $y^{a} \in Y^{a}$ of this sample
6 All parties share $\alpha \sim Beta(\beta, \beta)$ 7 foreach party i do
8    selects $x_{i}^{\prime}, y_{i}^{\prime}$ based on strategy
9    computes $\tilde{x}_{i} = \alpha x_{i}^{a} + (1 - \alpha) x_{i}^{\prime}$ 10 AP computes $\tilde{y} = \alpha y^{a} + (1 - \alpha) \sum_{i=0}^{c} \frac{d_{i}}{d} \cdot y_{i}^{\prime}$ 11 return $\{\tilde{x}_{0}, \cdots, \tilde{x}_{c}; \tilde{y}\}$

of data and applies weighted-average on their features and corresponding labels to form a new batch. This strategy encourages the model to behave linearly in-between training data. However, mixup is applied only among the original training dataset, rather than between the training dataset and another dataset (i.e. the unaligned dataset in our setting). Inspired by mixup, we aim to design a mixing approach between the aligned and unaligned data in VFL.

Data mixture. We propose a new idea called data mixture to efficiently mix the aligned and unaligned data during the training stage of VFL. For every aligned sample $x _ { i } ^ { a } \in \mathcal { D } _ { i } ^ { a }$ which has the same label $y ^ { a } \in \mathcal { V } ^ { a }$ , each party i applies one of three random selection strategies (see next paragraph) to select another sample $x _ { i } ^ { \prime }$ and corresponding label $y _ { i } ^ { \prime }$ from all available samples. Suppose the feature space ${ \mathcal { F } } _ { i }$ in party i has $d _ { i }$ features and there are $\textstyle d = \sum _ { i = 0 } ^ { c } d _ { i }$ features in total. Then, similar to mixup, we choose a random weight-average parameter $\alpha \sim B e t a ( \beta , \beta )$ , where $\beta$ is a hyperparameter, and apply it to mix these samples:

$$
\tilde {x} _ {i} = \alpha x _ {i} ^ {a} + (1 - \alpha) x _ {i} ^ {\prime} \tag {3}
$$

$$
\tilde {y} = \alpha y ^ {a} + (1 - \alpha) \sum_ {i = 0} ^ {c} \frac {d _ {i}}{d} \cdot y _ {i} ^ {\prime} \tag {4}
$$

After that, $\{ \tilde { x } _ { i } : 0 \leq i \leq c \}$ as well as y˜ will be sent into VFL for training. In this way, the unaligned data in all parties is seamlessly integrated into the training stage of VFL. Fig. 4 describes how data mixture works.

Random selection strategies. Data mixture guides us about how to mix the aligned and unaligned data during the training stage of VFL. However, there is still a lack of what random selection strategy should be chosen. Here we provide two strategies as illustrated in Fig. 5:

![](images/59d6fe8e5a95bf8cb27c210ce31e6cf5b60d972e51357b829e50b16d6c597792.jpg)



Fig. 5: An example of two random selection strategies.   
![](images/665c3cfebb154f693a6092a2a306951d9789e4a4479acf9ccfe24ae17410c89c.jpg)



Fig. 6: Generation of pseudo-label.

• One and Aligned (OA). For each aligned sample, we only let one random party j to select an unaligned sample $x _ { j } ^ { \prime } \in \mathcal { D } _ { j } ^ { u } , y _ { j } ^ { \prime } \in \mathcal { V } _ { j } ^ { u }$ , while other parties separately select another aligned sample $\check { x } _ { i } ^ { \prime } \in { \mathcal { D } } _ { j } ^ { a } , y _ { i } ^ { \prime } \in \mathcal { Y } _ { i } ^ { a } , \forall i , 0 \leq i \leq c , i \neq j$ . Notice that we do not need $\boldsymbol { x } _ { i } ^ { \prime }$ to be the features of the same sample. They are independently selected by each party. This is a simple strategy with little modification of the original mixup. VFL can benefit from the unaligned data, but the improvement is not impressive due to the conservative usage of unaligned data.   
• Full at a Time (FT). Different from OA, FT requires all parties to independently select an unaligned sample $x _ { i } ^ { \prime } \in$ $\mathcal { D } _ { i } ^ { u } \cup \mathcal { D } _ { i } ^ { a } , y _ { i } ^ { \prime } \in \mathcal { Y } _ { i } ^ { u } \cup \mathcal { Y } ^ { a } , \forall i , 0 \leq i \leq c .$ This is the aggressive strategy, aiming to maximize the usage of unaligned data while preserving the robustness of the VFL model $( x _ { i } ^ { \prime }$ may still be selected among aligned data).

Compared to OA, the VFL model can train more times on the unaligned data with FT in a given total number of communication rounds, which will finally lead to a better VFL model, as shown in Table VI. However, OA is naturally more suitable for data seasoning as we will describe in Section V-C and requires less time for training.

Discussion about the data mixer algorithm (Algorithm 1). By choosing one proper random selection strategy and applying it to data mixture, we have the first module of FedMix: the data mixer. Before VFL, all parties share a proper random selection strategy and the beta distribution parameter β. During the training stage of VFL, every time the VFL model requires a sample for training, all parties run the data mixer to generate a mixed sample. Specifically, all parties first select one common aligned sample $\{ x _ { 0 } ^ { a } , \cdot \cdot \cdot , x _ { c } ^ { a } ; y ^ { a } \}$ . Then, each party i applies the chosen random selection strategy to find $\{ x _ { i } ^ { \prime } , y _ { i } ^ { \prime } \}$ . And finally, they use the same random $\alpha \in B e t a ( \beta , \beta )$ to generate $\{ \tilde { x } _ { 0 } , \cdots , \tilde { x } _ { c } ; \tilde { y } \}$ with Eqs. (3) and (4). With the data mixer, the parties can seamlessly put their unaligned data into the

Algorithm 2: Data Seasoning   
Input : The target auxiliary sample $x_{j}^{aux}$ in the auxiliary dataset $D_{j}^{aux}$ in party j and the number of passive parties c. (AP: the active party)

Output : The pseudo-label of $x_{j}^{aux}$ .

Data : The aligned datasets $D_{i}^{a}$ and the corresponding label $Y^{a}$ on each party $i, 0 \leq i \leq c$ .

1 DataSeasoning ( $j, x_{j}^{aux} \in D_{j}^{aux}$ ):
2    Parties except j choose one common aligned sample
3    foreach party $i \neq j$ do
4    selects the features $x_{i}^{a} \in D_{i}^{a}$ of this sample
5    AP selects the label $y^{a} \in Y^{a}$ of this sample
6    pred = model( $\{x_{i}^{a} | i \neq j\} \cup \{x_{j}^{aux}\}$ )
7 $p_{1}, p_{2} = top2(pred)$ 8    if $p_{1} \neq y^{a}$ then
9    return False
10    else
11    return $p_{2}$

training of VFL on their control. And this achieves the first design goal as we mention in Section III-C.

# C. Data Seasoning

While the data mixer aims to apply data mixture to solve the data sacrifice problem, there still remains one question: missing label information. It is quite common that there remains some data, especially those in passive parties, have no label information stored in the active party. We call them the auxiliary data. However, data mixture requires labels for the auxiliary data to properly mix with aligned data, which drives us to come up with a method to deal with the auxiliary data without label information.

Inspiration: semi-supervised learning. Semi-supervised learning (SSL) [42] has been a standard technique for unlabeled data. A basic SSL contains four main steps: initialization on labeled data, generation of pseudo-label for unlabeled data, expansion of dataset, and continuous training on the expanded dataset. In this way, SSL gradually groups data with similar feature distribution into the same label and enhances the model performance with a better boundary. However, in our scenario, the missing features of unaligned data make it impossible to directly apply SSL.

Generation of pseudo-label. The difficulty lies in how to find the most possible pseudo-label for unaligned data even if they lack some features. Recall that data mixture can mix the aligned and unaligned data. More importantly, the label is also mixed so that the VFL model should output a mixed prediction in the middle of the labels. Suppose we want to generate pseudo-label for $x _ { j } ^ { a u x } \in { \mathcal { D } } _ { j } ^ { a u x }$ in party j. We let every other party select features $x _ { i } ^ { a } , i \neq j$ of one aligned sample. Then $\{ x _ { i } ^ { a } | i \neq j \} \cup \{ x _ { j } ^ { a u x } \}$ are sent to the VFL model for prediction. One of the top two labels should belong to the true label of the aligned sample, while the other can be considered as the pseudo-label of the unaligned sample. We describe the generation in Fig. 6.

Algorithm 3: FedMix   
Input : The number of passive parties c.
Output : The trained VFL model parameters.
Data : The aligned $(\mathcal{D}^{a}, \mathcal{Y}^{a})$ , unaligned $(\mathcal{D}_{i}^{u}, \mathcal{Y}_{i}^{u})$ and auxiliary $D_{i}^{aux}$ datasets on each party i.
1 FedMix:
2 initialize the VFL model parameters
3 share the number of features $d_{0}, \cdots, d_{c}$ in each party and the total number of features d
4 share the random selection strategy
5 share the beta distribution parameter $\beta$ 6 share the starting point $T^{*}$ of Algorithm 2
7 foreach communication round t do
8 if $t \geq T^{*}$ then
9    foreach party j do
10    foreach $x_{j}^{aux} \in D_{j}^{aux}$ do
11    p = DataSeasoning( $j, x_{j}^{aux}$ )
12    if $p \neq False$ then
13 $D_{j}^{u} = D_{j}^{u} \cup \{x_{j}^{aux}\}$ 14 $Y_{j}^{u} = Y_{j}^{u} \cup \{p\}$ 15 $D_{j}^{aux} = D_{j}^{u}/\{x_{j}^{aux}\}$ 16    foreach batch generated by Algorithm 1 do
17    update the VFL model parameters
18 return the final VFL model parameters

Discussion about the data seasoning algorithm (Algorithm 2). Data seasoning can be considered as a patch to the data mixer algorithm to let the VFL model use the auxiliary dataset. Assume that the VFL model is already trained on the aligned and unaligned data with the data mixer. Then, our data seasoning algorithm generates pseudo-labels for the auxiliary data in each party. After that, these pseudo-labeled auxiliary data can join in the unaligned data together with the aligned data to form a larger training dataset. Finally, the VFL model continues to update its parameters upon it to achieve better model performance. Here, we notice the similarity between the generation of pseudo-label and the OA random selection strategy in Section V-B. Thus, in practice, we can simultaneously perform data seasoning as well as OA in one go, which indirectly increases the speed of the training of VFL compared to FT. Our experiment results in Table VI show the same discovery. By effectively handling the auxiliary data in each party, we achieve the second design goal in Section III-C.

# D. Complexity Analysis of FedMix

By combining the data mixer algorithm and the data seasoning algorithm, we form our new framework FedMix in Algorithm 3 for a general on-the-fly solution to the data sacrifice problem. We now provide the complexity analysis of FedMix below. We first define three atomic operations of any

TABLE III: Complexity Analysis. 

<table><tr><td>Atomic Operation</td><td>Total Cost in Vanilla</td><td>Extra Cost in FedMix</td><td>Approx. Ratio of Extra Cost</td></tr><tr><td>Sample Selection</td><td> $T|\mathcal{D}^{a}|$ </td><td> $T|\mathcal{D}^{a}| + \sum_{j=1}^{c} |\mathcal{D}_{j}^{aux}|$ </td><td> $1 + c/T$ </td></tr><tr><td>Forward Propagation</td><td> $T|\mathcal{D}^{a}|$ </td><td> $\sum_{j=1}^{c} |\mathcal{D}_{j}^{aux}|$ </td><td> $c/T$ </td></tr><tr><td>Backward Propagation</td><td> $T|\mathcal{D}^{a}|$ </td><td>0</td><td>0</td></tr></table>

TABLE IV: Datasets in experiments. 

<table><tr><td>Dataset</td><td>Description</td><td colspan="2">Classification Task</td><td>Size</td></tr><tr><td> $\mathcal{D}_{D}$ </td><td>DefaultCredit [44]</td><td rowspan="2">Binary</td><td>30,000×</td><td>23</td></tr><tr><td> $\mathcal{D}_{T}$ </td><td>Criteo [36]</td><td>600,000×</td><td>39</td></tr><tr><td> $\mathcal{D}_{F}$ </td><td>FashionMNIST [40]</td><td rowspan="2">Multiclass</td><td>70,000×</td><td>784</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>Cifar10 [22]</td><td colspan="2">60,000×3,072</td></tr></table>

VFL training protocol: sample selection, forward propagation and backward propagation. For convenience, we consider a VFL training task with an aligned dataset $\mathcal { D } ^ { a }$ over $T$ communication rounds in total. And the batch size is set to be 1.

For the Vanilla VFL training protocol, each aligned sample should be selected once per communication round. Then, the model performs forward and backward propagation on it. Thus, the number of each atomic operation would be $T | \mathcal { D } ^ { a } |$ .

For FedMix, each aligned sample would pair with one unaligned sample in $\mathcal { D } _ { j } ^ { u }$ by Algorithm 1, which leads to $T | \mathcal { D } ^ { a } |$ extra operations on sample selection over $T$ communication rounds. Besides, each auxiliary sample in $\mathcal { D } _ { j } ^ { a u x }$ would go through Algorithm 2 for its pseudo-label, which adds extra $\textstyle \sum _ { j = 1 } ^ { c } | { \mathcal { D } } _ { j } ^ { a u { \bar { x } } } |$ operations on sample selection and forward prop-a c aux =1 |D |agation. Thus, FedMix introduces extra $\begin{array} { r } { T | \mathcal { D } ^ { a } | + \sum _ { j = 1 } ^ { c } | \mathcal { D } _ { j } ^ { a u x } | } \end{array}$ operations on sample selection and $\textstyle \sum _ { j = 1 } ^ { c } | D _ { j } ^ { a u x } |$ =1  on forward propagation.

If we denote the average size of auxiliary datasets as $| \overline { { \mathcal { D } ^ { a u x } } } |$ , then cj=1 $\begin{array} { r } { \sum _ { j = 1 } ^ { c } | \mathcal { D } _ { j } ^ { a u x } | ~ = ~ \hat { c } | \overline { { \mathcal { D } ^ { a u x } } } | } \end{array}$ . Notice that in most cases, $c \ll T$ but $| \overline { { { \cal D } ^ { a u x } } } | \approx | { \cal D } ^ { a } | . \mathrm { \ S o }$ , $\begin{array} { r } { \sum _ { j = 1 } ^ { c } | \mathcal { D } _ { j } ^ { a u x } | \Big / T | \mathcal { D } ^ { a } | \approx c / T } \end{array}$ . We compare the costs of three atomic operations between Vanilla and FedMix in Table III. We find a relatively large increase in sample selection, a relatively small increase in forward propagation, and no increase in backward propagation. However, since selecting one sample $( { \mathrm { i . e . } }$ sending an ID string of that sample) requires little computation and communication cost, the extra cost in sample selection is affordable. Besides, $c \ll T$ so that the extra cost in forward propagation is also acceptable.

# VI. EXPERIMENTS

# A. Setup

Datasets. To obtain comprehensive evaluation results, we use both tabular and image datasets (Table IV) for binary or multiclass classification tasks to evaluate FedMix. (1) Default-Credit $( { \mathcal { D } } _ { D } , [ 4 4 ] )$ . This dataset contains information on default payments, demographic factors, credit data, history of payment, and bill statements of 30 thousand credit card clients with 23 features. We consider it as a small dataset for the binary classification task. (2) Criteo $( \mathcal { D } _ { T } , [ 3 6 ] )$ . This is a classic dataset used to predict ad click-through rates, which is an important metric for a company to decide where to put advertisements. It has 600 thousand samples of 39 features in total and is considered to be a more challenging dataset for the binary task. (3) FashionMNIST $( { \mathcal { D } } _ { F } ,$ [40]). This dataset serves as a direct drop-in replacement for the MNIST dataset of fashion clothes with 70 thousand samples of $2 8 \times 2 8 = 7 8 4$ features. It is the normal dataset for the multiclass task. (4) CIFAR10 (DC , [22]). The images in this dataset are colored and much harder to classify, with 60 thousand samples of $3 \times 3 2 \times 3 2 = 3 0 7 2$ features. It is the difficult dataset for the multiclass task.

![](images/1cf7c5948292a3af11d105e4fd1657a38c9b7c9ba2b9a6a802ecb78a78889ecd.jpg)



(a) DD

![](images/1e49b588d97a8717bc6182febf513e1b19e51c1176c63e7db3d5f342e5b3347c.jpg)



(b) DT

![](images/157daf52cb51050576267d592762f2445a9768c0edf6aefac9d1b4fca91eb103.jpg)



(c) DF

![](images/437639ea5b7bcf2706f8bb0f6a8994d9f16b4131d15944d32b7dc036a3b3f471.jpg)



(d) DC   
Fig. 7: The performance change of the VFL model during training on four datasets.

TABLE V: The time cost of each stage and the communication size in VFL on four datasets. Note that Vanilla and FedMix have no preparing stage, so the time cost of the training stage is also the total time cost. 

<table><tr><td rowspan="2"></td><td colspan="2">Vanilla</td><td colspan="4">FedDA</td><td colspan="4">VFLFS</td><td colspan="2">FedMix</td></tr><tr><td>Total</td><td>Size</td><td>Preparing</td><td>Training</td><td>Total</td><td>Size</td><td>Preparing</td><td>Training</td><td>Total</td><td>Size</td><td>Total</td><td>Size</td></tr><tr><td> $\mathcal{D}_D$ </td><td>0.8h</td><td>2.58GB</td><td>1.2h</td><td>1.9h</td><td>3.1h</td><td>3.83GB</td><td>1.5h</td><td>1.2h</td><td>2.7h</td><td>2.58GB</td><td>2.3h</td><td>2.62GB</td></tr><tr><td> $\mathcal{D}_T$ </td><td>53.4h</td><td>43.83GB</td><td>36.5h</td><td>57.7h</td><td>94.2h</td><td>63.75GB</td><td>41.7h</td><td>54.1h</td><td>95.8h</td><td>43.83GB</td><td>65.2h</td><td>44.05GB</td></tr><tr><td> $\mathcal{D}_F$ </td><td>1.1h</td><td>5.75GB</td><td>0.9h</td><td>2.4h</td><td>3.3h</td><td>8.32GB</td><td>0.7h</td><td>2.3h</td><td>3.0h</td><td>5.75GB</td><td>2.6h</td><td>5.91GB</td></tr><tr><td> $\mathcal{D}_C$ </td><td>15.3h</td><td>5.36GB</td><td>10.5h</td><td>18.0h</td><td>28.5h</td><td>7.98GB</td><td>11.5h</td><td>16.7h</td><td>28.2h</td><td>5.36GB</td><td>21.5h</td><td>5.57GB</td></tr></table>

Metrics. We evaluate the performance of VFL models with both performance and time-cost metrics depending on the type of the dataset. For binary classification datasets $\mathcal { D } _ { D }$ and $\mathcal { D } _ { T } ,$ , we use AUC (Area Under the ROC Curve) to eliminate interference from imbalance. For multi-classification datasets $\mathcal { D } _ { F }$ and $\mathcal { D } _ { C }$ , we use ACC (Accuracy) to quantify the model performance. In addition to the performance metrics, we also measure the time cost and communication size of the whole training to check the efficiency of different methods.

Baselines. Based on our study of current research on the data sacrifice problem in Definition 1, we consider one borderline and two state-of-the-art methods for comparison: (1) Vanilla. This is the original VFL method without any modification. It serves as the baseline to show the borderline which trains with only the aligned data. (2) FedDA [47]. It represents Data completion which generates missing features for unaligned data so that they can be put into VFL. (3) VFLFS [7]. It stands for Extractor improvement which performs local representation learning and then serves it as the bottom model of VFL.

Model Setup. In order to show that FedMix is not restricted by specific model structures, we conduct experiments on different bottom models based on the task of datasets. Multilayer perceptron (MLP) [32] is applied as the bottom model for two binary classification tasks $\mathcal { D } _ { D } , \mathcal { D } _ { T }$ . Convolutional neural network (CNN) [8] is used for $\mathcal { D } _ { F }$ . ResNet-18 [11] is employed as a powerful feature extractor for $\mathcal { D } _ { C }$ .

Parameter Setup. For the model structures above, in our experiments, we put two fully-connected layers for MLP, two convolutional layers for CNN and two residential block layers for ResNet-18 as the bottom model, respectively. Besides, we add two more fully-connected layers as the top model for all tasks. Without a specific statement, we conduct experiments on the active party with one passive party and have the following hyperparameter settings: 100 preparing epochs for FedDA and VFLFS, 500 VFL training epochs, 128 batch size with the Adam optimizer for backward propagation. The sample distribution of each dataset is controlled by setting $\lambda _ { 0 } = \lambda _ { 1 } = 1 / 2$ . And the features are evenly divided and held by the active and passive parties. The data seasoning algorithm of FedMix starts at the 300th communication round.

Devices. All of our experiments are conducted with Py-Torch [31] on a cluster of Ubuntu 16.04 servers. Each server is equipped with a 48-core Intel(R) Xeon(R) CPU E5-2650 v4 @ 2.20GHz processor and Nvidia Tesla P100 PCIe 16GB GPU. Servers communicate with each other using Gigabit Ethernet (about 836 Mbit/s).

# B. Overall Performance

Model performance. In model performance, we plot the changes in performance with respect to the corresponding communication rounds. As depicted in Fig. 7, experimental results demonstrate that FedMix effectively boosts the performance with at most 15% improvement of the VFL model in different datasets with different model structures. There are three main observations:

A distinct improvement with all three methods compared to Vanilla in $\mathcal { D } _ { D }$ and $\mathcal { D } _ { T } .$ . A simple MLP model structure makes the corresponding GAN and autoencoder easy to learn the representatives of features, so that the performance can be greatly improved. The performance gap between FedMix and FedDA is caused by the utilization of auxiliary data, which GAN in FedDA cannot use. And the gap between FedMix and VFLFS can be explained by the data used in the training stage of VFL, where VFLFS uses aligned data only.

![](images/2341887b848b86504412fedbd5df7fc24b171e7d28a47941619d33cc3f5f5620.jpg)



(a) DD

![](images/d7cd3314f15e9980e7c5f14dd71dd28c47974f4f02160eeeeacbb356a8c4c741.jpg)



(b) DT

![](images/03af79d4766354cba3e088040067d4941fa148a9a2b107b6ec88d9fd245a757b.jpg)



(c) DF

![](images/e6e4274275b52516c5789a9f6af801fbdff24e74105ea3401c7efaa1994ae38b.jpg)



(d) DC

Fig. 8: The performance of the VFL model under different feature distribution settings on four datasets. (AP: the active party)   
![](images/153f26f191d8a6bb950dac329c72829f938209281fe40af068debd9900d18476.jpg)



(a) DD

![](images/2b06215fdf6e8fc53208e77b47e8344df85eff4e747a9760db8eab151ccbe294.jpg)



(b) DT

![](images/34b8b2b2cb14ce4a4e2b692356e5c96b52c92e2b3c9e42c0cbab6ad428bd6c61.jpg)



(c) DF

![](images/5331fa9aef1c619ff4d81fde503d69291e3656255ddc39bdf9b48ee7bfb71fb8.jpg)



(d) DC   
Fig. 9: The performance of the VFL model under different sample distribution settings on four datasets.

A huge improvement with FedMix compared to FedDA or VFLFS in $\mathcal { D } _ { F }$ . We find that neither FedDA nor VFLFS has any improvement compared to Vanilla in $\mathcal { D } _ { F }$ (with less than 1% improvement). A reasonable explanation is that FedDA may suffer from mode collapse and cannot properly generate generalized features for unaligned data. And, VFLFS is again dragged by the training with aligned data only, which tends to be similar to the behavior of Vanilla. However, FedMix can let the original unaligned data with data mixture directly take part in the training of VFL. And the auxiliary data also enhances the VFL model. The data mixer and the data seasoning together make the VFL model robust and able to learn better from unaligned and auxiliary data.

Robustness with FedMix but overfitting with VFLFS in DC. We find a surprising result that VFLFS begins to drop after about 250 communication rounds in DC with the ResNet-18 model structure. We can infer from this training result that without enough aligned data, VFLFS cannot train a good autoencoder as the bottom model of VFL. Thus, VFLFS still heavily relies on the aligned data to get a well-performed VFL model during training. But for a large model structure with a small aligned training dataset, it is easy to overfit, which would finally lead to this experiment result. On the contrary, FedMix uses data mixture for robustness and makes full use of all aligned, unaligned and auxiliary data. So FedMix is able to maintain good VFL model performance without overfitting.

The quality evaluations provide us a clear understanding about the scope of application of different methods, demonstrating the effectiveness of FedMix in different datasets under different model structures, with better usage of unaligned and auxiliary data, and great robustness.

Time cost. FedMix aims to use unaligned and auxiliary data during the training stage of VFL instead of an extra preparing stage like FedDA or VFLFS. Thus, the time cost of VFL is also what we should focus on. We separately measure the time cost of the preparing stage and the training stage and sum them up to get the total time cost for each method. Table V shows the results on different datasets corresponding to Fig. 7. Our findings of the results are as follows:

FedMix has a great total time cost reduction compared to FedDA and VFLFS. The preparing stage of FedDA and VFLFS significantly increases the total time cost. It may take up to 55% of the total time cost according to the model structure and data amount. It may not be a good idea to spend so much time on the preparing stage, especially considering the potential little performance boost later in the training stage such as Fig. 7(c). On the other hand, FedMix starts the VFL training stage directly without any preparing stage, therefore reducing 0.4h  30.5h time cost.

• FedMix has a slight time cost increase in the training stage compared to other methods. We notice that the time cost of the training stage in FedMix is slightly larger than other methods. This is due to the extra utilization of unaligned and auxiliary data in each communication round as analyzed in Section V-D. Referring to the training time cost of FedDA, which also uses the unaligned data during the training stage, FedMix would be still a little slower (with 0.4h  7.5h more time cost), since we introduce the auxiliary data at the second half of the total communication rounds. This slight time cost increase is worthwhile since FedMix can actually improve the VFL model performance in different datasets as shown in Fig. 7.

Communication size. Besides, we also analyze the extra communication size introduced by FedMix in Table V. We find out that compared to FedDA, FedMix requires less communication cost to achieve better VFL model performance. The reason why VFLFS has the same communication cost as Vanilla is that the preparing stage of VFLFS is done in each party itself without any communication. However, the extra communication cost introduced by FedMix is actually very small (about $0 . 5 \% \sim 4 \% )$ , which is consistent with our complexity analysis in Section V-D.

TABLE VI: Comparison of different random selection strategies. 

<table><tr><td rowspan="2"></td><td colspan="2"> $\mathcal{D}_D$ </td><td colspan="2"> $\mathcal{D}_T$ </td><td colspan="2"> $\mathcal{D}_F$ </td><td colspan="2"> $\mathcal{D}_C$ </td></tr><tr><td>Performance</td><td>Time Cost</td><td>Performance</td><td>Time Cost</td><td>Performance</td><td>Time Cost</td><td>Performance</td><td>Time Cost</td></tr><tr><td>Vanilla</td><td>83.3%</td><td>0.8h</td><td>74.0%</td><td>53.4h</td><td>86.8%</td><td>1.1h</td><td>44.3%</td><td>15.3h</td></tr><tr><td>OA</td><td>87.6%</td><td>2.0h</td><td>75.5%</td><td>56.7h</td><td>88.4%</td><td>2.3h</td><td>55.3%</td><td>18.7h</td></tr><tr><td>FT</td><td>88.1%</td><td>2.3h</td><td>75.6%</td><td>65.2h</td><td>89.7%</td><td>2.6h</td><td>59.5%</td><td>21.5h</td></tr></table>

![](images/dae922060ffa27e143d4f45ed131bc73d4361dac2c9787ccf444af822c8b46df.jpg)



Fig. 10: Effect of β.

![](images/58b5fc42d117b9e2ee82d45e695074700df2801c50187d812f3d2a1eb72a91bf.jpg)



Fig. 11: Effect of $T ^ { * }$ .

![](images/79dd92f0b1eb0f60a518aacd52561ea31fd527a6f5ba5f2c90d7dde40365dfa5.jpg)



![](images/b61b9d05b9a99817c1569c0c397042b295f528d8dbb15129f16fea7e3bed0dd7.jpg)



Fig. 12: Effect of data mixer Fig. 13: Comparison on the (DM) and data seasoning (DS). multi-passive-party scenario.

# C. Data Distribution

Feature distribution. To analyze the effect of different feature distributions, we conduct experiments with five different settings, each with 0.1, 0.3, 0.5, 0.7, 0.9 feature proportion of the active party. The results are shown in Fig. 8.

The VFL model with the best performance of FedMix appears when each party holds the same number of features. This is in line with our expectations. The data mixer is generally not affected by different feature distributions, since from Eq. (4), the labels of the party with fewer features would have less influence on the mixed label. However, the data seasoning would be affected because fewer features would lead to inaccurate predictions during semi-supervised learning.   
FedMix is robust and outperforms other methods in all feature distribution settings. When the feature distribution begins to bias, all methods have a performance drop. However, FedMix can still maintain relatively high performance with 3% ∼ 10% improvement compared to Vanilla. In comparison, FedDA and VFLFS have a significant performance drop with only 0.1%  1% improvement when the feature distribution is unbalanced between the active and passive parties.

Sample distribution. Different sample distributions also have a great effect on the VFL model performance. We set $\gamma _ { i } , i \in \{ 0 , 1 \}$ to be the same in $\{ 1 / 6 , 1 / 3 , 1 / 2 , 2 / 3 , 5 / 6 \}$ , and the corresponding γ computed by Lemma 1 is fallen into $\{ 2 / 7 , 1 / 2 , 2 / 3 , 4 / 5 , 1 0 / 1 1 \}$ . Our experiment results in Fig. 9 show the changes in the performance of the VFL model relative to γ. As γ increases (i.e. the proportion of unaligned and auxiliary data becomes large), the performance of the VFL model decreases as expected. However, we notice that when γ is too big, FedDA and VFLFS cannot contribute to the VFL

model anymore, with only $1 \% \sim 3 \%$ improvement compared to Vanilla. The poor GAN in FedDA and the training with only aligned data in VFLFS severely affect the performance of the VFL model. On the contrary, FedMix can still have up to 16% accuracy improvement in dataset $\mathcal { D } _ { C }$ under the setting $\gamma = 1 0 / 1 1$ , highlighting our superiority.

# D. Ablation Study

Data mixer. The data mixer will be affected by different random selection strategies as well as the hyperparameter $\beta .$

1) Random selection strategy. Different random selection strategies may lead to different model behaviors. To study the potential effect, we conduct experiments with the proposed two random selection strategies on the four datasets and list the results in Table VI.   
FT outperforms OA in all settings. Within a fixed number of total communication rounds, FT can utilize unaligned data twice as OA, since FT combines unaligned data from both the active party and the passive party. This finding tells us that training with the data mixer actually makes the VFL model focus more on the inner feature relationship in one party (rather than the inner feature relationship between parties) to the corresponding label information.   
OA is faster than FT. This is caused by our design of the generation of pseudo-label, as described in Section V-C. OA can be performed together with the data seasoning, while FT has to use two separate steps. With the findings above, we recommend using FT in most situations for better VFL model performance. But if there is a large number of auxiliary data, a possible choice would be OA for less time cost.   
2) β for data mixture. This hyperparameter for data mixture is the same as the original Mixup, which also has similar results as shown in Fig. 10. The training with a large β slightly outperforms others (with only $0 . 2 \% \sim 2 \%$ improvement). A large $\beta$ means that data mixture prefers the intermediate result of mixing two samples (with similar weights between samples). Due to little difference in performance among different β, we recommend simply setting $\beta = 1$ where $B e t a ( \beta , \beta )$ results in a uniform distribution between zero and one.

TABLE VII: Generalizability experiments on datasets over different model structures compared with more baseline models. 

<table><tr><td>Dataset</td><td>Structure</td><td>Vanilla</td><td>FedDA</td><td>VFLFS</td><td>STFL</td><td>VFedTrans</td><td>FedMix</td></tr><tr><td>Breast Cancer</td><td>MLP</td><td>90.91%</td><td>93.02%</td><td>92.74%</td><td>92.92%</td><td>92.33%</td><td>93.55%</td></tr><tr><td>MIMIC III</td><td>SecureBoost</td><td>79.40%</td><td>80.55%</td><td>80.92%</td><td>80.77%</td><td>80.42%</td><td>82.14%</td></tr><tr><td>Diabetes</td><td>SecureBoost</td><td>71.41%</td><td>72.66%</td><td>71.79%</td><td>72.46%</td><td>72.35%</td><td>73.61%</td></tr><tr><td>Avazu</td><td>Wide &amp; Deep</td><td>73.64%</td><td>74.13%</td><td>73.81%</td><td>74.16%</td><td>74.26%</td><td>74.53%</td></tr></table>

Data seasoning. The data seasoning aims to utilize the auxiliary data during the training stage of VFL. However, we should carefully choose when to start generating pseudolabel. Here, the experiment results with different T ∗ 200, 250, 300, 350, 400 in Fig. 11 gives us some advice. Due to underfitting at the beginning of the training, the VFL model cannot generate accurate pseudo-label for auxiliary data, which may even harm the performance instead. As T ∗ increases, the performance of the VFL model gradually grows as well. But when $T ^ { * }$ is larger than 350, the performance of the VFL model begins to drop. The reason behind this situation is that there are not enough communication rounds remaining for the VFL model to fit on the auxiliary data. Thus, under the assumption that the VFL model can converge at the total communication rounds T , we recommend letting T ∗ be in the range between 0.5T to 0.7T according to our experiment results.

Collaboration. After analyzing the hyperparameter settings in the data mixer and the data seasoning, we now show that both of them indeed contribute to the performance of the VFL model in Fig. 12. The experiments include the performance comparison among three settings: with only the data mixer, with only the data seasoning, and with both of them. From the results, all of these three settings improve the performance of the VFL model compared to baseline. This confirms the functionality of the two modules in FedMix. And with both of the two modules, the performance is even better, which shows that they are complementary with each other. But the power of the data mixer (contributing to 80% of the improvement) is much bigger than the data seasoning. So in practice, we may choose whether to use the auxiliary data to further improve the performance of the VFL model with extra training time cost.

# E. Multi-passive-party Scenario

From the results in Fig. 13, in the multi-passive-party scenario (with four passive parties), FedMix still outperforms FedDA and VFLFS in both performance (with 3% 4% improvement) and time cost (with 0.9h 2.3h reduce) metrics. The performance gap is even bigger, since in the multi-passiveparty scenario, the number of features each party holds is fewer. Thus, it will be harder for FedDA to generate features in other parties and for VFLFS to train a good extractor (i.e. similar to the results in Fig. 8). However, since FedMix makes the VFL model focus on the inner feature relationship as described in Section VI-D, the performance of the VFL model does not have a great decrease.

# F. Generalizability Study

To further demonstrate the generalizability of FedMix, we conduct experiments on more datasets (Breast Cancer [49], MIMIC III [17], Diabetes [18] and Avazu [39]) over different model structures (MLP, SecureBoost [5] and Wide & Deep Model [4]), and compare the performance with more baseline methods (FedDA, VFLFS, STFL [6] and VFedTrans [13]). From the results in Table VII, FedMix outperforms all other methods with about 0.89% 2.74% improvement on different datasets over different model structures.

# VII. LIMITATION AND FUTURE WORK

We propose FedMix to mix aligned, unaligned as well as auxiliary data to improve the performance of the VFL model during the training stage of VFL. However, there is still an obvious increase in time cost compared to Vanilla as shown in Table V, which is discussed in Section V-D. When the amount of auxiliary data or the number of parties increases without limitation, FedMix can still gradually become slow due to the semi-supervised learning in the data seasoning. We will continue to seek the solution to the data sacrifice problem with stable time complexity.

# VIII. CONCLUSION

There has been a growing interest in distributed databases to better utilize data in different organizations. In this paper, we focus on a common problem in such distributed scenarios called data sacrifice and provide a general on-the-fly solution to it. We first provide a detailed theoretical analysis to show that unaligned and auxiliary data indeed have the potential to improve the performance of VFL. Besides, we observe the limitations of existing methods in time-cost and data distribution settings. Based on our discovery, we propose data mixture to effectively mix the aligned and unaligned data during the training stage of VFL with two random selection strategies. To handle the auxiliary data without label information, we leverage semi-supervised learning to generate pseudo-label for them. The two modules above form our novel framework FedMix to effectively and efficiently solve the data sacrifice problem. Extensive evaluations on different datasets, different data distribution settings, ablation study, and comparison with state-of-the-art methods show the superiority and generalizability of FedMix.

# ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, “the Fundamental Research Funds for the Central Universities” WK2150110024, the University Synergy Innovation Program of Anhui Province under Grant GXXT-2022-049, Tencent Marketing Solution Rhino-Bird Focused Research Program.

# REFERENCES

[1] Divyakant Agrawal, Amr El Abbadi, and Shiyuan Wang. “Secure and privacy-preserving database services in the cloud”. In: 29th IEEE International Conference on Data Engineering, ICDE 2013, Brisbane, Australia, April 8-12, 2013. Ed. by Christian S. Jensen, Christopher M. Jermaine, and Xiaofang Zhou. IEEE Computer Society, 2013, pp. 1268– 1271. DOI: 10.1109/ICDE.2013.6544921. URL: https://doi.org/10.1109/ ICDE.2013.6544921.   
[2] Timothy Castiglia, Shiqiang Wang, and Stacy Patterson. “Self-Supervised Vertical Federated Learning”. In: Workshop on Federated Learning: Recent Advances and New Challenges (in Conjunction with NeurIPS 2022). 2022.   
[3] Timothy Castiglia, Yi Zhou, Shiqiang Wang, Swanand Kadhe, Nathalie Baracaldo, and Stacy Patterson. “LESS-VFL: Communication-Efficient Feature Selection for Vertical Federated Learning”. In: International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA. Ed. by Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett. Vol. 202. Proceedings of Machine Learning Research. PMLR, 2023, pp. 3757–3781. URL: https : / / proceedings . mlr . press / v202 / castiglia23a.html.   
[4] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishi Aradhye, Glen Anderson, Greg Corrado, Wei Chai, Mustafa Ispir, Rohan Anil, Zakaria Haque, Lichan Hong, Vihan Jain, Xiaobing Liu, and Hemal Shah. “Wide & Deep Learning for Recommender Systems”. In: Proceedings of the 1st Workshop on Deep Learning for Recommender Systems, DLRS@RecSys 2016, Boston, MA, USA, September 15, 2016. Ed. by Alexandros Karatzoglou, Balázs Hidasi, Domonkos Tikk, Oren Sar Shalom, Haggai Roitman, Bracha Shapira, and Lior Rokach. ACM, 2016, pp. 7–10. DOI: 10.1145/ 2988450.2988454. URL: https://doi.org/10.1145/2988450.2988454.   
[5] Kewei Cheng, Tao Fan, Yilun Jin, Yang Liu, Tianjian Chen, Dimitrios Papadopoulos, and Qiang Yang. “SecureBoost: A Lossless Federated Learning Framework”. In: IEEE Intell. Syst. 36.6 (2021), pp. 87–98. DOI: 10.1109/MIS.2021.3082561. URL: https://doi.org/10.1109/MIS. 2021.3082561.   
[6] Kai-Fung Chu and Lintao Zhang. “Privacy-Preserving Self-Taught Federated Learning for Heterogeneous Data”. In: CoRR abs/2102.05883 (2021). arXiv: 2102.05883. URL: https://arxiv.org/abs/2102.05883.   
[7] Siwei Feng. “Vertical federated learning-based feature selection with non-overlapping sample utilization”. In: Expert Syst. Appl. 208 (2022), p. 118097. DOI: 10.1016/J.ESWA.2022.118097. URL: https://doi.org/10. 1016/j.eswa.2022.118097.   
[8] Kunihiko Fukushima and Sei Miyake. “Neocognitron: A new algorithm for pattern recognition tolerant of deformations and shifts in position”. In: Pattern Recognit. 15.6 (1982), pp. 455–469. DOI: 10.1016/0031- 3203(82)90024-3. URL: https://doi.org/10.1016/0031-3203(82)90024-3.   
[9] Muhammad Ghifary, W. Bastiaan Kleijn, Mengjie Zhang, David Balduzzi, and Wen Li. “Deep Reconstruction-Classification Networks for Unsupervised Domain Adaptation”. In: Computer Vision - ECCV 2016 - 14th European Conference, Amsterdam, The Netherlands, October 11-14, 2016, Proceedings, Part IV. Ed. by Bastian Leibe, Jiri Matas, Nicu Sebe, and Max Welling. Vol. 9908. Lecture Notes in Computer Science. Springer, 2016, pp. 597–613. DOI: 10.1007/978-3- 319-46493-0\_36. URL: https://doi.org/10.1007/978-3-319-46493-0\_36.   
[10] Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron C. Courville, and Yoshua Bengio. “Generative Adversarial Nets”. In: Advances in Neural Information Processing Systems 27: Annual Conference on Neural Information Processing Systems 2014, December 8-13 2014, Montreal, Quebec, Canada. Ed. by Zoubin Ghahramani, Max Welling, Corinna Cortes, Neil D. Lawrence, and Kilian Q. Weinberger. 2014, pp. 2672– 2680. URL: https : / / proceedings . neurips . cc / paper / 2014 / hash / 5ca3e9b122f61f8f06494c97b1afccf3-Abstract.html.   
[11] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. “Deep Residual Learning for Image Recognition”. In: 2016 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2016, Las Vegas, NV, USA, June 27-30, 2016. IEEE Computer Society, 2016, pp. 770–778. DOI: 10.1109/CVPR.2016.90. URL: https://doi.org/10.1109/CVPR.2016. 90.   
[12] Yuanqin He, Yan Kang, Jiahuan Luo, Lixin Fan, and Qiang Yang. “A Hybrid Self-Supervised Learning Framework for Vertical Federated Learning”. In: CoRR abs/2208.08934 (2022). DOI: 10.48550/ARXIV.

2208.08934. arXiv: 2208.08934. URL: https://doi.org/10.48550/arXiv. 2208.08934.   
[13] Chung-ju Huang, Leye Wang, and Xiao Han. “Vertical Federated Knowledge Transfer via Representation Distillation for Healthcare Collaboration Networks”. In: Proceedings of the ACM Web Conference 2023, WWW 2023, Austin, TX, USA, 30 April 2023 - 4 May 2023. Ed. by Ying Ding, Jie Tang, Juan F. Sequeda, Lora Aroyo, Carlos Castillo, and Geert-Jan Houben. ACM, 2023, pp. 4188–4199. DOI: 10.1145/ 3543507.3583874. URL: https://doi.org/10.1145/3543507.3583874.   
[14] Bernardo A. Huberman, Matthew K. Franklin, and Tad Hogg. “Enhancing privacy and trust in electronic communities”. In: Proceedings of the First ACM Conference on Electronic Commerce (EC-99), Denver, CO, USA, November 3-5, 1999. Ed. by Stuart I. Feldman and Michael P. Wellman. ACM, 1999, pp. 78–86. DOI: 10.1145/336992.337012. URL: https://doi.org/10.1145/336992.337012.   
[15] Jiawei Jiang, Lukas Burkhalter, Fangcheng Fu, Bolin Ding, Bo Du, Anwar Hithnawi, Bo Li, and Ce Zhang. “VF-PS: How to Select Important Participants in Vertical Federated Learning, Efficiently and Securely?” In: Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022. Ed. by Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh. 2022. URL: http://papers.nips.cc/paper\_ files/paper/2022/hash/0e1a2388cd2f78069f4d048d935cb218-Abstract-Conference.html.   
[16] Zhida Jiang, Yang Xu, Hongli Xu, Zhiyuan Wang, Chunming Qiao, and Yangming Zhao. “FedMP: Federated Learning through Adaptive Model Pruning in Heterogeneous Edge Computing”. In: 38th IEEE International Conference on Data Engineering, ICDE 2022, Kuala Lumpur, Malaysia, May 9-12, 2022. IEEE, 2022, pp. 767–779. DOI: 10. 1109/ ICDE53745. 2022. 00062. URL: https:// doi. org/ 10. 1109/ ICDE53745.2022.00062.   
[17] Alistair E.W. Johnson, Tom J. Pollard, Lu Shen, Li-wei H. Lehman, Mengling Feng, Mohammad Ghassemi, Benjamin Moody, Peter Szolovits, Leo Anthony Celi, and Roger G. Mark. “MIMIC-III, a freely accessible critical care database”. In: Scientific Data 3.1 (May 2016). ISSN: 2052-4463. DOI: 10 . 1038 / sdata . 2016 . 35. URL: http : //dx.doi.org/10.1038/sdata.2016.35.   
[18] Michael Kahn. Diabetes. DOI: 10.24432/C5T59G. URL: https://archive. ics.uci.edu/dataset/34.   
[19] Yan Kang, Yang Liu, and Xinle Liang. “FedCVT: Semi-supervised Vertical Federated Learning with Cross-view Training”. In: ACM Trans. Intell. Syst. Technol. 13.4 (2022), 64:1–64:16. DOI: 10.1145/3510031. URL: https://doi.org/10.1145/3510031.   
[20] Yan Kang, Yang Liu, Yuezhou Wu, Guoqiang Ma, and Qiang Yang. “Privacy-preserving Federated Adversarial Domain Adaption over Feature Groups for Interpretability”. In: CoRR abs/2111.10934 (2021). arXiv: 2111.10934. URL: https://arxiv.org/abs/2111.10934.   
[21] Mark A. Kramer. “Nonlinear principal component analysis using autoassociative neural networks”. In: AIChE Journal 37.2 (Feb. 1991), pp. 233–243. ISSN: 1547-5905. DOI: 10.1002/aic.690370209. URL: http://dx.doi.org/10.1002/aic.690370209.   
[22] Alex Krizhevsky, Geoffrey Hinton, et al. “Learning multiple layers of features from tiny images”. In: (2009).   
[23] Aounon Kumar, Alexander Levine, Tom Goldstein, and Soheil Feizi. “Provable Robustness against Wasserstein Distribution Shifts via Input Randomization”. In: The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023. OpenReview.net, 2023. URL: https://openreview.net/pdf?id=HJFVrpCaGE.   
[24] Lingli Li, Hongzhi Wang, Jianzhong Li, and Hong Gao. “A survey of uncertain data management”. In: Frontiers Comput. Sci. 14.1 (2020), pp. 162–190. DOI: 10.1007/S11704-017-7063-Z. URL: https://doi.org/ 10.1007/s11704-017-7063-z.   
[25] Qinbin Li, Yiqun Diao, Quan Chen, and Bingsheng He. “Federated Learning on Non-IID Data Silos: An Experimental Study”. In: 38th IEEE International Conference on Data Engineering, ICDE 2022, Kuala Lumpur, Malaysia, May 9-12, 2022. IEEE, 2022, pp. 965–978. DOI: 10. 1109/ ICDE53745. 2022. 00077. URL: https:// doi. org/ 10. 1109/ ICDE53745.2022.00077.   
[26] Xianfeng Liang, Shuheng Shen, Enhong Chen, Jinchang Liu, Qi Liu, Yifei Cheng, and Zhen Pan. “Accelerating local SGD for non-IID data using variance reduction”. In: Frontiers Comput. Sci. 17.2 (2022), p. 172311. DOI: 10.1007/S11704-021-1018-0. URL: https://doi.org/10. 1007/s11704-021-1018-0.

[27] Yang Liu, Yan Kang, Tianyuan Zou, Yanhong Pu, Yuanqin He, Xiaozhou Ye, Ye Ouyang, Ya-Qin Zhang, and Qiang Yang. “Vertical Federated Learning”. In: CoRR abs/2211.12814 (2022). DOI: 10.48550/ARXIV. 2211.12814. arXiv: 2211.12814. URL: https://doi.org/10.48550/arXiv. 2211.12814.   
[28] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Agüera y Arcas. “Communication-Efficient Learning of Deep Networks from Decentralized Data”. In: Proceedings of the 20th International Conference on Artificial Intelligence and Statistics, AISTATS 2017, 20-22 April 2017, Fort Lauderdale, FL, USA. Ed. by Aarti Singh and Xiaojin (Jerry) Zhu. Vol. 54. Proceedings of Machine Learning Research. PMLR, 2017, pp. 1273–1282. URL: http : / / proceedings.mlr.press/v54/mcmahan17a.html.   
[29] Xupeng Miao, Xiaonan Nie, Yingxia Shao, Zhi Yang, Jiawei Jiang, Lingxiao Ma, and Bin Cui. “Heterogeneity-Aware Distributed Machine Learning Training via Partial Reduce”. In: SIGMOD ’21: International Conference on Management of Data, Virtual Event, China, June 20- 25, 2021. Ed. by Guoliang Li, Zhanhuai Li, Stratos Idreos, and Divesh Srivastava. ACM, 2021, pp. 2262–2270. DOI: 10.1145/3448016. 3452773. URL: https://doi.org/10.1145/3448016.3452773.   
[30] Chaoyue Niu, Zhenzhe Zheng, Fan Wu, Xiaofeng Gao, and Guihai Chen. “Trading Data in Good Faith: Integrating Truthfulness and Privacy Preservation in Data Markets”. In: 33rd IEEE International Conference on Data Engineering, ICDE 2017, San Diego, CA, USA, April 19-22, 2017. IEEE Computer Society, 2017, pp. 223–226. DOI: 10.1109/ICDE. 2017.80. URL: https://doi.org/10.1109/ICDE.2017.80.   
[31] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Z. Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. “PyTorch: An Imperative Style, High-Performance Deep Learning Library”. In: Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada. Ed. by Hanna M. Wallach, Hugo Larochelle, Alina Beygelzimer, Florence d’Alché-Buc, Emily B. Fox, and Roman Garnett. 2019, pp. 8024–8035. URL: https : / / proceedings . neurips . cc / paper / 2019 / hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html.   
[32] David E Rumelhart, Geoffrey E Hinton, Ronald J Williams, et al. Learning internal representations by error propagation. 1985.   
[33] Supreeth Shastri, Vinay Banakar, Melissa Wasserman, Arun Kumar, and Vijay Chidambaram. “Understanding and Benchmarking the Impact of GDPR on Database Systems”. In: Proc. VLDB Endow. 13.7 (2020), pp. 1064–1077. DOI: 10.14778/3384345.3384354. URL: http://www. vldb.org/pvldb/vol13/p1064-shastri.pdf.   
[34] Asuka Takatsu. On Wasserstein geometry of the space of Gaussian measures. 2008. DOI: 10 . 48550 / ARXIV. 0801 . 2250. URL: https : //arxiv.org/abs/0801.2250.   
[35] Ben Tan, Bo Liu, Vincent W. Zheng, and Qiang Yang. “A Federated Recommender System for Online Services”. In: RecSys 2020: Fourteenth ACM Conference on Recommender Systems, Virtual Event, Brazil, September 22-26, 2020. Ed. by Rodrygo L. T. Santos, Leandro Balby Marinho, Elizabeth M. Daly, Li Chen, Kim Falk, Noam Koenigstein, and Edleno Silva de Moura. ACM, 2020, pp. 579–581. DOI: 10.1145/ 3383313.3411528. URL: https://doi.org/10.1145/3383313.3411528.   
[36] Jean-Baptiste Tien, joycenv, and Olivier Chapelle. Display Advertising Challenge. 2014. URL: https://kaggle.com/competitions/criteo-displayad-challenge.

[37] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. “Attention is All you Need”. In: Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA. Ed. by Isabelle Guyon, Ulrike von Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman Garnett. 2017, pp. 5998–6008. URL: https : / / proceedings . neurips . cc / paper / 2017 / hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html.   
[38] Paul Voigt and Axel von dem Bussche. The EU General Data Protection Regulation (GDPR). Springer International Publishing, 2017. ISBN: 9783319579597. DOI: 10 . 1007 / 978 - 3 - 319 - 57959 - 7. URL: http : //dx.doi.org/10.1007/978-3-319-57959-7.   
[39] Steve Wang and Will Cukierski. Click-Through Rate Prediction. 2014. URL: https://kaggle.com/competitions/avazu-ctr-prediction.   
[40] Han Xiao, Kashif Rasul, and Roland Vollgraf. “Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning Algorithms”. In: CoRR abs/1708.07747 (2017). arXiv: 1708.07747. URL: http://arxiv. org/abs/1708.07747.   
[41] Liu Yang, Di Chai, Junxue Zhang, Yilun Jin, Leye Wang, Hao Liu, Han Tian, Qian Xu, and Kai Chen. “A Survey on Vertical Federated Learning: From a Layered Perspective”. In: CoRR abs/2304.01829 (2023). DOI: 10.48550/ARXIV.2304.01829. arXiv: 2304.01829. URL: https://doi.org/10.48550/arXiv.2304.01829.   
[42] Xiangli Yang, Zixing Song, Irwin King, and Zenglin Xu. “A Survey on Deep Semi-Supervised Learning”. In: IEEE Trans. Knowl. Data Eng. 35.9 (2023), pp. 8934–8954. DOI: 10.1109/TKDE.2022.3220219. URL: https://doi.org/10.1109/TKDE.2022.3220219.   
[43] Yitao Yang, Xiucai Ye, and Tetsuya Sakurai. “Multi-View Federated Learning with Data Collaboration”. In: ICMLC 2022: 14th International Conference on Machine Learning and Computing, Guangzhou, China, February 18 - 21, 2022. ACM, 2022, pp. 178–183. DOI: 10.1145/ 3529836.3529904. URL: https://doi.org/10.1145/3529836.3529904.   
[44] I-Cheng Yeh. Default of credit card clients. 2009. DOI: 10.24432/ C55S3H. URL: https://archive.ics.uci.edu/dataset/350.   
[45] Binhang Yuan, Cameron R. Wolfe, Chen Dun, Yuxin Tang, Anastasios Kyrillidis, and Chris Jermaine. “Distributed Learning of Fully Connected Neural Networks using Independent Subnet Training”. In: Proc. VLDB Endow. 15.8 (2022), pp. 1581–1590. DOI: 10.14778/3529337.3529343. URL: https://www.vldb.org/pvldb/vol15/p1581-wolfe.pdf.   
[46] Hongyi Zhang, Moustapha Cissé, Yann N. Dauphin, and David Lopez-Paz. “mixup: Beyond Empirical Risk Minimization”. In: 6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings. OpenReview.net, 2018. URL: https : / / openreview. net / forum?id=r1Ddp1-Rb.   
[47] JianFei Zhang and YuChen Jiang. “A Data Augmentation Method for Vertical Federated Learning”. In: Wireless Communications and Mobile Computing 2022 (Jan. 2022). Ed. by Amr Tolba, pp. 1–16. ISSN: 1530- 8669. DOI: 10.1155/2022/6596925. URL: http://dx.doi.org/10.1155/ 2022/6596925.   
[48] Hangyu Zhu, Haoyu Zhang, and Yaochu Jin. “From Federated Learning to Federated Neural Architecture Search: A Survey”. In: CoRR abs/2009.05868 (2020). arXiv: 2009.05868. URL: https://arxiv.org/abs/ 2009.05868.   
[49] Matjaz Zwitter and Milan Soklic. Breast Cancer. 1988. DOI: 10.24432/ C51P4M. URL: https://archive.ics.uci.edu/dataset/14.