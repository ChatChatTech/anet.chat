# Privacy-preserving Data Selection for Horizontal and Vertical Federated Learning

Lan Zhang, Anran Li, Hongyi Peng, Feng Han, Fan Huang, Xiang-Yang Li, Fellow, ACM & IEEE

Abstract—Federated learning (FL) enables distributed participants to collaboratively train a machine learning model without accessing to their local data. In FL systems, the selection of training samples has a significant impact on model performances, e.g., selecting participants whose datasets have low-quality samples and features would result in low accuracy and unstable models. In this work, we aim to solve the problem that selects a collection of high-quality training samples for a given FL task under a monetary budget. We propose a holistic design to efficiently select high-quality samples while preserve the privacy of participants’ local data and the server’s label set. We propose an efficient hierarchical sample selection mechanism to select relevant clients and their samples before training for horizontal federated learning (HFL). It uses the determinantal point process (DPP) to select both the statistical homogenous and content diverse clients and samples. Besides, we propose a private set intersection (PSI) based scheme to filter relevant features for the target VFL task. Finally, during training, an erroneous-aware importance based selection is proposed to dynamically select important clients and samples to accelerate model convergence. We verify the merits of our proposed solution with extensive experiments on a real AIoT system with 50 clients. The experimental results validate that our solution achieves accurate and efficient selection of high-quality data, and consequently an FL model with a faster convergence speed and higher accuracy.

Index Terms—Federated Learning, Feature Selection, Importance Sampling, Data Quality Assessment.

# 1 INTRODUCTION

The rapid development of networking technologies, such as mobile networks [1], [2], sensor networks and crowdsensing technologies [3], has made it possible to generate massive diverse data. Recently, how to acquire large enough highquality datasets, however, becomes a common bottleneck of many machine learning models and Artificial Intelligent (AI) applications. This is not only because collecting and labelling massive samples are very expensive, but also because the privacy concerns hindering data sharing in many fields, e.g., medicine and economics. Federated learning (FL) [4]–[6] as an emerging technology makes it possible to train a machine learning model by the distributed participants without accessing to their local data. There are two main types of FL methods according to the distribution of data, horizontal federated learning (HFL) [4], [5] and vertical federated learning (VFL) [7], [8]. HFL describes the scenario where different parties own data with different samples IDs but shares many common features so as to collaboratively learn a joint mapping from the feature space to the label space. In VFL, multiple parties handle data with the same samples IDs, but each party has its own feature set and only one party holds labels. In addition to the above design of FL algorithms for diverse scenarios, the composition of training dataset also has a significant impact on the performance of an FL model [9]. As we will show by the data-driven analysis in Section 3, incorrect labels, unrepresentative samples, skewed categorical distributions, noisy or irrelavant features and low content diversity can all lead to severe model accuracy deterioration in real FL applications.

In this work, we consider a typical FL system, a server in HFL or the active party in VFL aims to train a target deep learning model with a given monetary budget. There are a collection of data owners, each of which possesses a number of samples and is willing to participate in some FL tasks for a certain price. Our goal is to select a set of highquality samples and a set of high-quality features for the target FL task and pay their owners to participate in the model training under the budget in a privacy-preserving way. There are very few work to deal with the data selection [10], and the feature selection problem for FL [11]. The work [10] proposes a method to distributedly select relevant data before training based on a benchmark model. This work, however, neither considers other data quality factors, e.g., the Non-IID problem or erroneous samples [12], nor considers the dynamic importances of samples in the model training process [13]. The work [11] proposes a secure federated feature selection method to select features based on filter methods [14], with unacceptable communication overhead, and with an unreasonable assumption, e.g., the existence of a trusted third party in VFL setting. To address the aforementioned challenges, in this paper, we pose and address three key questions:

1) How to privately measure samples’ quality and impacts on the global model, before and during training? Our goal is to select high-quality samples that have large positive influences on the performance of global FL models. Therefore, we need to comprehensively and accurately quantify the sample quality scores and influence associated with the target model without accessing any local samples.

2) How to achieve optimal selection considering multiple quality dimensions and the budget constraint, and how to dynamically select more important samples during training? Facing multiple quality dimensions, we need to achieve an optimal balance between various quality dimensions and select an optimal budget feasible collection of samples which is most likely to produce a model with high accuracy. During training, different training batch compositions lead to different model performances (see Section 3.3), so an efficient importance aware batch selection method is required.

3) How to provide better privacy protection for both participants and the server, and how to efficiently reduce the cost for data selection? For local clients, we try to protect not only the privacy of their local data, but also their local data distributions. For the server in HFL, we treat the target task of the server as a secret to irrelevant clients, as the target task may expose the business plan. In addition, for the active party in VFL, its label set should never be exposed to any other party. Finally, participants in FL systems usually have limited resources [15], which motivates us to design a efficient quality measurement and data selection method.

By addressing these challenges, our work makes the following main contributions:

• We propose a holistic design for efficient selection of high-quality samples for both HFL and VFL settings that takes into account all those factors affecting model performance. The proposed method protects not only clients data privacy but also the server’s label set.

• We propose an efficient hierarchical sample selection scheme that first selects optimal clients and then their high quality samples. Before training, we use a private set intersection (PSI) based scheme to filter relevant clients. We solve the optimization problem of client selection by using a determinantal point process (DPP) based algorithm that maximizes both statistical homogeneity and content diversity. During training, an erroneous-aware importance-based selection method is proposed to dynamically select important clients and samples to accelerate model convergence. Compared to our conference version [16], we further explore a PSI based method to filter relevant features and propose an efficient feature selection method that utilizes HE and Gini impurity to securely select important features. Besides, we design a secure important sample selection method based on HE to accelerate model convergence for VFL.

• We evaluate our design via extensive experiments using two popular datasets on a real AIoT system with 50 clients. The experimental results illustrate that when there are low-quality clients, our method reduces the average false rate for training models on MNIST and CIFAR from 16.73% to 8.5%, and from 34.8% to 18.91%. Meanwhile, our sample selection method outperforms existing methods in terms of faster model convergence rate, higher accuracy and lower cost. When compared to three data selection methods for centralized training, our method saves up to 64.6%, 55.3% computation cost and 66.8%, 54.5% communication cost for training models on MNIST and CIFAR, respectively.

# 2 RELATED WORK

In our work, we focus on high-quality sample selection for HFL and high-quality feature selection for VFL before model training. Meanwhile, we study the dynamic important sample selection for both HFL and VFL settings.

# 2.1 Data selection

There are a number of data selection methods proposed for centralized learning [13], [17]–[20], while few work deal with the data selection problem for FL [10], [21].

# 2.1.1 Data selection for centralized learning

Data selection methods for centralized learning can be divided into two branches. One branch [17], [18] focuses on proposing various quality dimensions, e.g., task relevancy and content diversity, and directly measure the quality of data samples to make selections. The work [18] propose a framework to conduct large-scale datasets quality assessment incorporating both task-independent intrinsic quality and task-dependent contextual quality. The other branch [13], [20] dynamically selects samples with greater importances to the model to compose training batches during the training process, in order to accelerate model convergence. The importance is usually quantified by the gradient norm or the loss of training samples [22], [23]. For example, the work [20] proposes distance weighted sampling to select more informative and stable examples than traditional approaches examples. Those methods, however, cannot be directly applied to FL systems for the following reasons. 1) Those methods require access to training samples, which violates the privacy of participants in FL systems. 2) Directly calculating importance for each sample would cause unacceptable cost for participants with limited resources. 3) Those methods cannot cope with the Non-IID problem [12], [24] or erroneous samples, and are very likely to give higher priority to erroneous samples, which usually have larger importance values (see Fig. 2(a)).

# 2.1.2 Data selection for FL

Existing FL client selection works can be divided into two branches. One branch utilizes the client contribution evaluation results [25], e.g., calculated through Shapley values, to select clients and optimize the global model aggregation. The other branch proposes various statistical selection metrics, e.g., differences of model updates [26] and local losses [27], to calculate the metric values and make selections. However, these methods treat all samples from a selected client as equally important, which can lead to a waste of communication and computational resources when updating local models on unimportant samples.

As for data selection for FL, one category [10] proposes to distributedly select relevant data before FL training based on a benchmark model, without considering other data quality factors. The other category dynamically selects samples to compose local batch during training [28], [29]. These methods, however, either ignore the noise data or incurs large communication costs, which makes them inapplicable. Therefore, in FL scenarios, how to select an optimal collection of training samples for a given FL task without accessing to participants’ local data and training process is an extremely exigent and challenging problem.

# 2.2 Feature Selection

# 2.2.1 Feature selection for centralized learning

Feature selection plays a fundamental role in centralized machine learning tasks [30]–[32]. Feature selection methods can be divided into three categories: filter methods, wrapper methods and embedded methods. Filter methods attempt to remove irrelevant features prior to learning a model. They rank the features based on their importance scores calculated according to a specific criteria, e.g., F-statistics, Gini-impurity and mutual information [14], [32]. Wrapper methods leverage the outcomes of a model to determine the importance of individual features. They attempt to select a subset of features which can achieve the best performance by recomputing the model for each subset of features. However, as the number of subsets can be much large in the context of deep neural networks (DNN), wrapper methods are generally computationally expensive [33], [34]. Embedded methods reduce the computation overhead by learning the model while simultaneously selecting the subset of relevant features [31], [35], [36]. The least absolute shrinkage and selection operator is a well-known embedded feature selection method, whose objective is to minimize the loss while enforcing an $l _ { 1 }$ constraint on the weights of the features. Usually, filter methods have much less computational complexity compared to wrapper and embedded approaches, which make them more suitable for VFL settings.

# 2.2.2 Feature Selection for VFL

In VFL, there are only a few existing work on feature selection. Some work propose secure federated feature selection method based on F-statistical filtering measurements and multi-party computation [11]. However, these methods assume that there is a trusted third party to generate random matrices which is, however, impractical in real VFL systems. Besides, it would cause large communication overhead since the massive parameter are transferred between participants and the third trusted party. Other work [37], [38] propose the feature selection method by using a Gaussian stochastic dual-gate combined with a feature importance initialization method based on Gini impurity. However, they require extra parameters to be trained in the first layer of the model, resulting in overfitting to the training data, especially for deep neural networks with high-dimensional data. Thus, this lack of practical solution motivates us to design an efficient and secure feature selection method for VFL models.

# 3 DATA DRIVEN ANALYSIS

# 3.1 Problem Definitions

A typical FL scenario involves two types of entities: a server S and N clients $\{ \mathcal { C } _ { 1 } , \mathcal { C } _ { 2 } , \cdots , \mathcal { C } _ { N } \}$ . Each client $\mathcal { C } _ { k }$ possesses a local dataset $\mathcal { D } _ { k }$ and is willing to participate in some FL tasks for a price $b _ { k } ,$ , which could be money or credits. The server aims to coordinate clients to accomplish a given FL task for as high accuracy and efficiency as possible within a monetary or credit budget B. To achieve this goal, we first select high-quality clients and samples before training. Then, we dynamically select collections of samples from selected clients to speed up model convergence. The goal of the high-quality client selection before training can be defined as,

$$
\max V (\mathcal {Q}), \text {   s.t.,   } \sum_ {k \in \mathcal {Q}, \mathcal {Q} \subseteq [ N ]} b _ {k} \leq B. \tag {1}
$$

Here, Q is the index set of the selected clients, and V (Q) is the quality value of the selected clients, $e . g .$ , statistical homogeneity and content diversity, which are quantified in Definition 1 and 2, respectively. Further, due to the limited computation or communication resources and some clients having poor-quality or irrelevant samples (with erroneous labels, skewed categorical distribution, or unacceptably low content diversity) or poor-quality features for the VFL task, the server needs to select an optimal collection of samples and features from selected clients. Then, during model training, the selected clients collaboratively train the target FL model using dynamically selected local samples to speed up the model convergence, and finally get their payments.

Threat Model. We assume that all participants including the server are semi-honest. They follow the exact protocols of FL model training and data selection without tampering with it and they do not collude with one another. Nevertheless, they are curious about other’s private information and will try to infer as much as possible from the information received from the other participants. The semi-honest assumption is reasonable in our context since all participants have an incentive to learn a high-performance FL model.

# 3.2 Design Goals

We design our system to achieve the following goals.

• Effectiveness: Given candidate samples from N clients, the selected collection of samples should produce a global FL model with higher accuracy and faster convergence speed than that trained with any other sample collections within the given budget B.   
• Privacy protection: Our method should preserve privacy of not only the clients’ local data, the server’s target task for both HVL and VFL, but also the server’s label set in the VFL setting. Specifically, in both HFL and VFL settings, clients’ local samples and their distributions should never be exposed to any other party other than the data owner. Besides, the specific target task of the server should never be exposed to any irrelevant party who was not selected in the HFL setting. In addition, In the VFL setting, the label set of the server should never be exposed to any local clients.   
• Efficient selection: Considering the restricted resources of local edges and mobile devices, the selection process should incur low extra computation and communication cost.

# 3.3 Data Driven Analysis and Observations

Towards above goals, we conduct data driven analysis to explore the principles for selecting training samples in both HFL and VFL scenarios. For HFL, we used the well-known image datasets CIFAR10 [39] as training data, which contains 50,000 images from 10 categories. We employ 10 clients to train a residual network [40] using a typical federated optimization algorithm FedSGD [4]. We divide the dataset into 100 shards of size 500, and assigned them to 10 clients (10 shards per client). The learning rate η = 0.01, batch size $g = 1 0 ,$ , local epoch E = 10. We test accuracy of the global model on the hold-out test dataset of CIFAR10. For VFL, we use MADELON [41] and Iris [42] datasets as training data. The MADELON dataset consists of 5 informative features and 495 nuisance features, while the Iris dataset consists of 4 features. We employed two clients to train typical vertical neural networks [43], [42] for MADELON and Iris, respectively. Different from conventional FL systems, which usually treat each client, each sample or each feature equally, we vary the settings to answer the following questions.

![](images/455945dbe5577cbebad89b672fad84606d7a3950153e58c418fe99e15518e443.jpg)



(a) Accuracy vs. mislabeling ratios.

![](images/23646dc8ad89a036cdcd59acf0d740a877206e45c64062921c539f0c1a95ae57.jpg)



(b) Statistically heterogeneous data.

![](images/40e2bc032665738d72d7fbc6b51a35717a7675bee85bbebbb9e81c9fcdf980ae.jpg)



(c) Statistically heterogeneous data.

![](images/62bbe52ed158d30846e719047a7ebeb46a46748b18b0b3bc5be21b9aa829630e.jpg)



(d) Different content diversity.

Fig. 1. Test accuracy of a residual network trained using CIFAR10 in different settings: (a) There are different proportions of erroneous data; (b) Each client has k random categories out of 10 categories; (c) Distribution of the training data is imbalanced between the first five categories and the last five categories; (d) The training data has different content diversity.   
![](images/3233d8e3a0dadce564b4ebf77d8e17d0a02f9e8e1df0ac9999d40c434e2d3df1.jpg)



(a) Different selection strategies.

![](images/a9aaf501e094ea3a7c9cdbb6946680360baf933c0e2fdfe3a4051d3f511c441c.jpg)



(b) Gradient norm updates of samples

![](images/b8c5876ad2f460369ff19b541fb976ddc8e9fb7905c4ac662e106ae5f9a8a5ae.jpg)



(a) Accuracy vs. number of selected features.

![](images/e695198d0a0667c9f41a7c7bf218a747206940a353d51a04e589e481fbb17754.jpg)



(b) Accuracy vs. Gini scores of features   
Fig. 2. Effect of sampling strategies: (a) Test accuracy of a residual Fig. 3. (a) Test accuracy of a vertical neural network training using network trained using CIFAR10 with different batch selection strate- MADELON vs. number of selected features; (b) Test accuracy of a gies; (b) Gradient norm updates of samples during FL training, here vertical neural network training using Iris vs. Gini scores of features. Sample 0 is an erroneous sample, Sample 1-3 are correct samples.

1) How does each sample affect the HFL model training? A series of previous work [13], [20] have shown that, in a large training dataset, there are usually a portion of unrepresentative samples making negligible contributions to the model convergence, which actually incur unnecessary computation cost for training. Some poor-quality or erroneous samples even have negative influences on the model training [44]. To demonstrate such negative influences, we manually created some erroneous samples in the training dataset by replacing their original labels with random labels from other categories. Let $r _ { m }$ be the ratio of mislabeled samples in all training samples. We randomly selected rm ·50, 000 samples equally from all clients or randomly from no more than 9 clients. Fig. 1(a) shows that the test accuracy of the global model decreases significantly as the ratio of mislabeled samples increases.

• Principle #1: The sample selection should prioritize representative samples and avoid erroneous ones.   
2) How does the categorical distribution of training data affect HFL the model training? When the local training data is evenly distributed across all categories, we refer to it as a statistically homogeneous (or IID) setting, otherwise a statistically heterogeneous (or Non-IID) setting [45], [46].

The statistically heterogeneous training data with severe imbalance distributions among categories will result in low accuracy and unstable convergence. In Fig. 1(b), Non-IID (k) $( 1 \leq k \leq 1 0 )$ indicates that each client has samples from k random categories out of all ten categories. Even in the case Non-IID (8), there is still a huge accuracy loss compared with that in the IID setting. In Fig.1(c), although each client has samples from all categories, the number of samples in the first five categories is much lower than that in the last five categories. Both Fig. 1(b) and Fig.1(c) illustrate that the model performance obviously deteriorates as the imbalance degree increases.

• Principle #2: The selection should prioritize clients whose data distributions are closer to the homogeneous distribution and avoid clients with missing categories.

3) How does the content diversity of training samples affect the HFL model training? We further look into the fact that even in the statistically homogeneous setting the content diversity of training samples has a non-negligible effect on the model. We randomly removed 30% (or 50%) samples from the original dataset and added the same amount of “new” samples, which were created by rotating the remaining samples by random angles smaller than 30 degree, to compose a dataset with a lower content diversity. In Fig. 1(d), although the categorical distributions of three datasets are almost identical, the decrease of content diversity leads to obvious accuracy loss.

• Principle #3: The selection should try to maximize the content-level diversity of the selected training dataset.   
4) How does each sample feature affect the VFL model training? In VFL, large portion of unrepresentative or nuisance sample features of local clients prohibits the model from achieving a high performance. To demonstrate this, we

assign different numbers of nuisance features to the clients and train the VFL model on MADELON dataset. In Fig. 3(a), 10 : k indicates that, one of the client has 10 features consisting of 3 informative ones and 7 nuisance one, and the other client has k features consisting of 2 informative features and $k - 2$ ones. The result shows that as the the number of nuisance features increases, the test accuracy of the global VFL model decreases significantly. Further, we show that different features have different importance. We use individual features from Iris dataset to train the VFL model, and leverage Gini impurity scores to characterize the importance of features. From Fig. 3(b), we see that features of different importance, $e . g .$ ., different Gini scores, can train models with different test accuracy.

• Principle #4: The feature selection should try to minimize the Gini impurity scores of the selected samples.

5) How does the batch sampling strategy affect the model training? Given the distribution of training data, using different strategies to sample training batches for local epochs will result in drastically different performances of FL models [20]. We tried three typical sampling strategies in both clean data and noisy data settings: i) random sampling strategy, ii) gradient norm based importance sampling, and iii) loss based importance sampling. Random sampling strategy is widely used for FL. The last two importance sampling strategies are proposed for centralized learning [13], [19], here we extended them to FL scenarios. Fig. 2(a) presents that, in the clean data setting, different sampling strategies result in different convergence speeds and accuracy, and the loss based importance sampling is superior than the other two. In the noisy data setting, where 30% clients have 30% mislabeled samples, random sampling has better resistance to erroneous data, while both importance sampling strategies suffer from highly unstable training process and lower accuracy. The reason is that, erroneous samples have obviously larger losses and gradient norms than correct ones (Fig. 2(b)), therefore existing importance sampling strategies tend to select erroneous samples with higher probabilities.

• Principle #5: During training, the selection should prioritize samples of greater importance but avoid erroneous samples which usually have abnormally large importance.

Given the same candidate training dataset, these observations reveal how sample selection dramatically changes the performance of FL models, which motivates us to design an effective and privacy-preserving sample selection strategy for FL.

# 4 MAIN IDEA AND SYSTEM OVERVIEW

# 4.1 Main Idea

Following principles in Section 3, we divide the data selection into two stages:

# 4.1.1 Before Training

The server selects an optimal collection of relevant clients (who possess data of the target categories) within the budget B to participate in the training, by prioritizing clients with higher category-level statistical homogeneity and contentlevel diversity, in a privacy preserving way.

Definition 1 (Statistical Homogeneity). Let Y be the set of target categories. Client $\mathcal { C } _ { k }$ has a dataset $\mathcal { D } _ { k } = \{ ( x _ { k } , y _ { k } ) \}$ ,

where each data $x _ { k }$ has a label $y _ { k }$ . $\mathcal { D } _ { k }$ follows a categorical distribution $q _ { k }$ . The uniform categorical distribution over Y is $q _ { u } .$ . The statistical homogeneity of $\mathcal { D } _ { k }$ is defined as [24],

$$
\mu_ {k} = 2 - \sqrt {\sum_ {y \in \mathcal {Y}} | q _ {k} (y _ {k} = y) - q _ {u} (y _ {u} = y) | ^ {2}}, \tag {2}
$$

which measures the similarity between distributions $q _ { k }$ and $q _ { u }$ over Y.

A larger homogeneity will result in better model performance according to Principle #2.

Definition 2 (Content Diversity). Given a dataset D having M samples or M sub-collections of samples, let $v _ { i }$ be the content embedding vector of the i-th sample or i-th sub-collection of samples. The similarity function of two vectors is $S ( v _ { i } , v _ { j } )$ . The content diversity of D is defined as [47],

$$
\rho (\mathcal {D}) = 1 - \frac {\sum_ {i , j \in [ M ] , i \neq j} 2 S (v _ {i} , v _ {j})}{M (M - 1)}, \tag {3}
$$

A dataset with larger content diversity will result in better model performance according to Principle #3.

In this stage, to solve the optimization that simultaneously maximizes the statistical homogeneity and content diversity of the selected clients under the budget, we model this problem as a determinantal point process (DPP). To protect the privacy of clients data, we design an efficient privacy-preserving computation protocol based on homomorphic encryption, binary JL-transformation based data sketch, and randomized response.

# 4.1.2 During Training

The server dynamically selects collections of samples from selected clients to compose training batches for each epoch by prioritizing error-free important samples. According to Principle #1 and #5, we firstly need a proper metric to accurately estimate the importance/impact of each local sample to the global model, and then design an efficient strategy to select important correct samples and filter out erroneous ones that usually have abnormally large importance. In the whole process, for privacy of clients, we cannot access any local sample. To measure the importance of training samples, some methods have been proposed for centralized scenarios, which use the gradient norm, the gradient’s upper bound norm or the loss of a sample as metrics of importance [13], [19], [48], [49]. Those methods, however, cannot be directly applied to FL systems for the reasons that the server requires access to all training samples. In FL systems, both local data and local training process are invisible to any other parties including the server. In addition, those methods neglect the impact of erroneous samples and are very likely to give higher priority to erroneous samples than correct ones (see Fig. 2(a)).

Inspired by previous work in centralized scenarios [13], we use gradient upper bound norms as an importance metric. Different to those conventional methods, the gradient here is not the one of the loss with respect to the model parameter, but is its upper bound, the loss with respect to the pre-activation outputs of the last layer. Using upper bound norms is to reduce computation cost, because computing the conventional norm needs one forward and one backward pass through the network, while its upper bound only needs one forward, which still achieves sufficiently accurate estimations of samples’ importance but has lower cost than that of the backward.

1) For HFL: Here, we take a neural network classification task as an example, which is defined over a compact space $\mathcal { X }$ and a label space Y. There are N clients, each client $\mathcal { C } _ { k }$ has a local dataset ${ \mathcal { D } } _ { k } = \{ z _ { k , 1 } , z _ { k , 2 } , \cdot \cdot \cdot , z _ { k , n _ { k } } \}$ , where $z _ { k , i } = ( x _ { k , i } , y _ { k , i } ) \in \mathcal { X } \times \mathcal { Y } ^ { 1 }$ following the categorical distribution $\begin{array} { r } { q _ { k } . n = \sum _ { k = 1 } ^ { N } n _ { k } } \end{array}$ is the total number of all clients’ samples. Functions $f _ { k } ( \cdot ) , \mathcal { F } _ { k } ( \cdot )$ represent loss functions of an individual sample on $\mathcal { C } _ { k } { ' } \mathrm { s }$ local model, and all samples on client $\mathcal { C } _ { k } { } ^ { \prime } \mathrm { s }$ local model, $\mathcal { L } ( \cdot )$ represents loss function of the global model.The goal of a standard federated optimization problem is to find

$$
\theta^ {*} = \arg \min _ {\theta \in \Theta} \left\{\mathcal {L} (z; \theta) := \sum_ {k = 1} ^ {N} \frac {n _ {k}}{n} \mathcal {F} _ {k} (\theta) \right\}, \tag {4}
$$

$$
\text { where } \mathcal {F} _ {k} (\theta) = \frac {1}{n _ {k}} \sum_ {z _ {k, i} \in \mathcal {D} _ {k}} f _ {k} (z _ {k, i}; \theta)).
$$

This problem is solved via iterative stochastic optimization. In the t-th iteration, the server selects a subset of clients and distributes the model parameters $\theta _ { t }$ to them. Each selected client $\mathcal { C } _ { k }$ independently computes a local update $\theta _ { t + 1 } ^ { k } ~ = ~ \theta _ { t } ^ { k } - \eta \nabla \mathcal { F } _ { k } ( \boldsymbol { \theta } _ { t } ^ { \bullet } )$ with learning rate $\eta ,$ and sends $\eta \dot { \nabla } \mathcal { F } _ { k } ( \theta _ { t } )$ to the server. The server aggregates the updates and conducts the update $\theta _ { t + 1 } ~ = ~ \bar { \theta } _ { t } ^ { - } - \eta \nabla \mathcal { L } ( z ; \theta _ { t } )$ . This process is iterated until the global model converged to $\theta ^ { * } ,$ $e . g . ,$ , meeting a convergence criterion.

Here we give how to estimate the importance of a sample $z _ { k , i }$ based on the global model in the t-th iteration. For client $\mathcal { C } _ { k } , \theta _ { k } ^ { l } \in R ^ { m ^ { l } \times m ^ { l - 1 } }$ is the weight matrix for layer $l , m ^ { l }$ is the number of neural nodes of the l-th layer (in total L layers) of local model $\theta _ { k } ; \ \sigma$ is a Lipschitz continuous activation function, and $\alpha _ { k } ^ { l } \stackrel {  } { = } \theta _ { k } ^ { l } ( \beta _ { k } ^ { l - 1 } ) , \stackrel { \bullet } { \beta } _ { k } ^ { l - 1 } = \sigma ^ { l - 1 } ( \alpha _ { k } ^ { l - 1 } )$ .

Definition 3 (Sample Importance for HFL). The importance of a client $\mathcal { C } _ { k } \mathrm { \Delta } ^ { \prime }$ sample $z _ { k , i }$ to the global model in the t-th iteration is

$$
\lambda (z _ {k, i}, t) = \sqrt {\left| \sum_ {t , L} \beta_ {k , i} ^ {t , L} \nabla_ {\alpha_ {k , i} ^ {t , L}} \mathcal {L} (z _ {k , i} ; \theta_ {t}) \right| ^ {2}}, \tag {5}
$$

where βt,Lk,i , αt,Lk,i $\beta _ { k , i } ^ { t , L } , \alpha _ { k , i } ^ { t , L }$ are the input and output of the last layer (L-th) of sample $z _ { k , i }$ in the t-th iteration, respectively, and $\begin{array} { r c l } { { { \sum } _ { t , L } { \beta } ^ { L } } } & { { = } } & { { d \ddot { i } a g ( { \sigma } ^ { \prime L } ( \beta _ { 1 } ) , \cdots , { \sigma } ^ { \prime L } ( \beta _ { m _ { L } } ) ) , | { \dot { \sigma } } ^ { \prime } ( \beta ) | } } \end{array} \stackrel {  } { \leq }$ $\begin{array} { r } { \lambda , \mathcal { L } ( z ; \theta ) : = \sum _ { k = 1 } ^ { N } \frac { n _ { k } } { n } \mathcal { F } _ { k } ( \theta ) } \end{array}$ .

That is, the sample with larger gradient upper bound norm of the global loss with respect to the pre-activation outputs will have greater importance. However, as shown in Section 3.3 and Fig. 2(b), erroneous samples have significantly greater importance values than correct samples. Therefore, a client $\mathcal { C } _ { k }$ should avoid selecting samples whose importance values are outliers among that of majority samples. For example, in our experiment, we require $\lambda ( z _ { k , i } , t ) \leq$ $\begin{array} { r l } { \bar { \delta } _ { k } ^ { t } } & { { } ( e . g . } \end{array}$ , the median gradient norm of samples), where $\delta _ { k } ^ { \bar { t } } = 2 0 0 . 0$ in the CIFAR10 experiment. Specially, we notice

1. In real FL systems, a client $\mathcal { C } _ { k }$ is very likely to possess samples that don’t belong to any target categories, $\bar { i } . e . , \ \exists ( \stackrel { \cdot } { x } _ { k , i } , \stackrel { \cdot } { y } _ { k , i } ) , y _ { k , i } \ \stackrel { \cdot } { \notin } \ y$ . We will deal with this in Section 5.1.

that the importance metric has an additive property, hence the importance of a client can be measured by the summation of his/her samples’ importance.

Definition 4 (Client Importance for HFL). The importance of a client $\mathcal { C } _ { k }$ with dataset $\mathcal { D } _ { k }$ to the global model in the t-th iteration is

$$
\lambda (\mathcal {D} _ {k}, t) = \sum_ {z _ {k, i} \in \mathcal {D} _ {k}} \lambda (z _ {k, i}, t). \tag {6}
$$

After obtaining the importance of samples and filtering out erroneous ones, we can select samples by their importance for the next iteration. Let pt+1k,1 , $p _ { k , 1 } ^ { t + 1 } , \cdot \cdot \cdot , p _ { k , n _ { k } } ^ { t + \breve { 1 } }$ , p k,nk be the data sampling probability distribution of client $\mathcal { C } _ { k }$ in the $( t + 1 )$ - th iteration, pt+1 $p _ { k , i } ^ { t + 1 } \propto \lambda ( z _ { k , i } , t )$ . Similarly, we can also select clients by their importance, that is the probability to select a client Ck is P t+1k $\mathcal { C } _ { k }$ $P _ { k } ^ { t + 1 } \stackrel { \cdot } { \propto } \lambda ( \mathcal { D } _ { k } , t )$ k .

This additive property of importance enlightens us to design a hierarchical sample selection strategy during training, which selects important clients first to save a large portion of cost for sample-level importance analysis, then selects training samples only from selected clients.

2) For VFL: We consider the traditional VFL setting which is adopted by existing work [38], [50]. For a VFL task involving $N$ clients and a server $s ,$ each client $\mathcal { C } _ { k }$ owns a local dataset $\mathcal { D } _ { k } = \{ x _ { k , 1 } , x _ { k , 2 } , \cdot \cdot \cdot , x _ { k , n ^ { \prime } } \} \in \mathbb { R } ^ { n ^ { \prime } \times d _ { k } }$ , where $n ^ { \prime }$ is the size of matched samples $\mathrm { I D s } , d _ { k }$ is the feature size of each sample in $\mathcal { D } _ { k }$ . The server $s$ is the one owning the label set $\mathcal { V }$ . Each client $\mathcal { C } _ { k }$ learns a local embedding $e _ { k }$ via its local bottom model $\theta _ { k }$ . While, the server learns a global top model θ by concatenating local embeddings $e _ { k }$ from clients. Ideally, the goal of the VFL problem is to find,

$$
\theta^ {*} = \arg \min _ {\theta \in \Theta} \{\frac {1}{N} \sum_ {k = 1} ^ {N} \mathcal {L} (\theta ; e _ {k}; y _ {k}) \}, \tag {7}
$$

$$
\text { with } e _ {k} := f _ {k} ^ {v} (x _ {k, i}; \theta_ {k}), k \in [ N ],
$$

where $\mathcal { L } ( \cdot )$ represents loss function of the global model, and $f _ { k } ^ { v } ( \cdot )$ represents the local embedding function of client $\mathcal { C } _ { k } .$ This problem is solved via iterative stochastic optimization. Different from HFL, the parameters that will be exchanged between the server and local clients are ciphertexts of $\{ e _ { k } \}$ , and ciphertexts of gradients of loss $\{ \mathcal { L } ( \boldsymbol { \hat { \theta } } ; \boldsymbol { e _ { k } } ; \mathcal { V } ) \}$ } with respect to $\{ e _ { k } \}$ [43].

Consider that sample IDs are already matched, we estimate the importance of the i-th sample in the matched $\mathrm { I D s } , i \in [ n ^ { \prime } ] ,$ , in VFL based on the global model in the t-th iteration. Let $\theta ^ { l } \in R ^ { m ^ { l } \times m ^ { l - 1 } }$ be the weight matrix for layer $l ,$ $m ^ { l }$ is the number of neural nodes of the l-th layer (in total L layers) of the global top model θ; σ is a Lipschitz continuous activation function, and $\alpha _ { k } ^ { l } = \theta ^ { i } ( \beta ^ { l - 1 } ) , \beta ^ { \dot { l } - 1 } = \sigma ^ { l - 1 } ( \alpha ^ { l - 1 } )$ .

Definition 5 (Sample Importance for VFL). The importance of the i-th sample in the matched IDs, $i \in [ n ^ { \prime } ]$ , to the global model in the t-th iteration is

$$
\lambda (i, t) = \sqrt {| \sum_ {t , L} \beta_ {i} ^ {t , L} \nabla_ {\alpha_ {i} ^ {t , L}} \mathcal {L} (\theta_ {t} ; e _ {t} ; \mathcal {Y}) | ^ {2}},
$$

$$
\text { with } e _ {t} = (e _ {t} ^ {1} | | e _ {t} ^ {2} \dots | | e _ {t} ^ {N}), e _ {t} ^ {k} := f _ {k} ^ {v} (x _ {k, i}; \theta_ {t} ^ {k}), k \in [ N ], \tag {8}
$$

where $\beta _ { i } ^ { t , L } , \alpha _ { i } ^ { t , L }$ are the input and output of the last layer $( L -$ th) of the global model for the i-th sample in iteration $t ,$ and $\boldsymbol { e } _ { t } = ( e _ { t } ^ { 1 } | | e _ { t } ^ { 2 } \cdot \cdot \cdot | | e _ { t } ^ { N } )$ is the vector obtained by concatenating the vectors $e _ { t } ^ { 1 } , e _ { t } ^ { 2 } , \cdots , e _ { t } ^ { N }$ , together. The sample with larger gradient upper bound norm of the global loss with respect to the pre-activation outputs will have greater importance. Here, we assume that all clients selected before training participate in model training, that is, we consider that all clients are equally important in VFL model training.

# 4.2 Design Overview

As shown in Fig. 4, here we present the overview of our two stage (before and during training) and hierarchical (first clients then samples) data selection framework for both HFL and VFL.

1) Filtering relevant clients and samples: When an FL task arrives, the server first needs to filter clients who possess data of the target categories, and specific relevant samples. To meet the privacy goal in Section 3.2, we apply a private set intersection (PSI) based method for computing the intersection of each client’s label set and the target label set for HFL, and of each client’s sample set and the server’s sample set with the unique sample ID [51] for VFL. If the number of samples in the intersection set exceeds a minimum number for the target model, then the client is relevant.   
2) Client and feature selection before training: For HFL, the server further privately selects high-quality clients to maximize statistical homogeneity and content diversity under the budget constraint using the DPP based algorithm. While for VFL, the server and clients further securely selects important features with the proposed HE based method. Then the server coordinates selected clients to start the training.   
3) Dynamical sample selection during training: For each iteration $t , t \in [ T ]$ ] during training, the server selects a subset of most important samples to compose their training batches. For HFL, to save cost, instead of computing importance values of all samples for all clients, the server uses a simple but effective method to measure each client’s importance using the training updates $\theta _ { t - 1 } ^ { k } , k \in [ N ]$ on the server. $\mathrm { A }$ client $\mathcal { C } _ { k }$ whose local model has larger deviation from the global model $\theta _ { t - 1 } , i . e .$ , larger $| \theta _ { t - 1 } ^ { k } - \check { \theta } _ { t - 1 } |$ , has larger contribution, hence are more likely to be selected in this iteration. The selected clients locally select training samples using the erroneous-aware importance-based selection algorithm. For VFL, all clients select training samples using the effective importance-based selection algorithm.   
4) Model training: In each iteration, all selected clients train their local models on the selected samples, and the server aggregates clients’ updates to get the global update. The server repeats the process until achieving the optimal global model ${ \bar { \theta } } ^ { * }$ .

# 5 CLIENT SELECTION & FEATURE SELECTION

In this section, we present the detailed design of privacypreserving client selection before training, including how to filter clients relevant to the target task for both HFL and VFL, and how to privately select clients to maximize statistical homogeneity and content diversity within the budget using the DPP based algorithm for HFL. In addition, we illustrate how to securely select clients and their important features for VFL based on the HE method.

![](images/85315702c8154e966076a89d71bd8a892818c8c31363477dd34f166fb46ffc4d.jpg)



Fig. 4. System overview.

# 5.1 Filtering Relevant Clients and Samples

1) For HFL. Let the target FL task have a label set Y. The FL system has N candidate clients, and each client $\mathcal { C } _ { k }$ possess a dataset $\mathcal { D } _ { k }$ . The label set of $\mathcal { D } _ { k }$ is $\mathcal { V } _ { k } = \{ y _ { k } \vert ( x _ { k } , \hat { y _ { k } } ) \in \mathcal { D } _ { k } \}$ . A relevant client $\mathcal { C } _ { k }$ should satisfy $| \{ ( x _ { k } , y _ { k } ) | y _ { k } \in \mathcal { V } _ { k } \cap \mathcal { V } \} | >$ $\nu ,$ where ν is the required minimum number of training samples for the target model (e.g., 1, 000). Samples belonging to the categories in the intersection set are relevant to the task. To protect the client’s privacy ${ \mathcal { V } } _ { k }$ and the server’s privacy Y, we leverage a widely adopted PSI protocol [52] to allow server and clients to compute $y _ { k } \cap \mathcal { V }$ privately. 2) For VFL. Let $I D _ { \mathcal { S } }$ and $I D _ { k }$ denote the sample ID sets of the server $s$ and the client $\mathcal { C } _ { k } , k \in [ N ]$ ]. The server and clients use a widely adopted PSI-based sample match method [51] to obtain an ID intersection set $I D _ { S } \cap I D _ { k }$ . When the size of the intersection satisfies $\left| I D _ { S } \cap I D _ { k } \right| > \nu ,$ then the client $\mathcal { C } _ { k }$ is a relevant one, and samples with IDs in the intersection are relevant. Finally, for both HFL and VFL, each client only reports 1-bit information, $i . e .$ , whether or not he/she is relevant, to the server. The server learns which client has more than ν relevant samples, and all clients learn nothing from this process.

# 5.2 Client Selection for HFL

# 5.2.1 Homogeneity-aware Client Selection

Taking statistical homogeneity as the quality metric of a client, we have $V _ { \mu } ( \mathcal { Q } ) = \operatorname { \bar { \Sigma } } _ { k \in \mathcal { Q } } \mu _ { k }$ . Without loss of generality, we assume that the first $N ^ { \prime }$ clients are relevant ones. To solve Eq.1, the server first needs to calculate $\mu _ { k } , k \in \ N ^ { \prime }$ according to Definition 1. The server generates a uniform categorical distribution $q _ { u }$ over the target categories Y. For each relevant client ${ \mathcal { C } } _ { k } ,$ let his/her intersection label set be $\mathcal { T } _ { k } = \mathcal { V } _ { k } \cap \mathcal { V }$ . Note that, since we only allow server and each client $\mathcal { C } _ { k }$ to learn $\mathit { T } _ { k } , \ q _ { u }$ is still the server’s secret to some relevant clients, whose intersection set $\mathcal { T } _ { k } \subset \mathcal { V } .$ . For each client the categorical distribution $q _ { k }$ of his/her dataset is also private. To compute $\mu _ { k }$ privately, we transform Eq.2 into the equation

$$
\begin{array}{l} \mu_ {k} = 2 - \left(\sum_ {y \in \mathcal {I} _ {k}} | q _ {k} (y _ {k} = y) - q _ {u} (y _ {u} = y) | ^ {2} \right. \\ + \sum_ {y \in \mathcal {Y} \backslash \mathcal {I} _ {k}} | q _ {k} (y _ {k} = y) - q _ {u} (y _ {u} = y) | ^ {2}) ^ {1 / 2}. \tag {9} \\ \end{array}
$$

The server can compute the second summation in the parentheses by itself, because when $y \in \mathcal { V } \setminus \mathcal { T } _ { k }$ we have $\bar { { q } } _ { k } ( y _ { k } \ = \ y ) \ = \ 0$ . For the first summation over $\mathcal { T } _ { k } ,$ , we leverage an efficient secure two-party computation protocol based on the homomorphic encryption of BGN [53] to let the server and clients jointly calculate this part using the server’s public key. Then, only the server learns each relevant client’s statistical homogeneity $\mu _ { k } ,$ while other parties learn nothing. Now the server can solve the optimization problem (Eq. 1) by greedily choosing clients with the largest $\hat { \mu } _ { k } / b _ { k } , k \in [ \hat { N } ^ { \prime } ]$ until the budget B runs out.

Algorithm 1: DPP-based Client Selection for HFL before Training   
Input : Server S, the budget B, $N'$ clients $\{C_{1},\cdots,C_{N'}\}$ declaring the price $\{b_{1},\cdots,b_{N'}\}$ Output: The index set of selected clients

1 for each client $C_{k}, k \in [N']$ do

2    Calculates $\mu_{k}$ with Eq. 2, and calculates $H_{k}$ using noisy content sketches (Section 5.2.2), and sends them to the server

3 The server initializes $Q \leftarrow$ an arbitrary client's index

4 while $\sum_{C_{k} \in Q} b_{k} < B$ do

5    The server finds client $C_{k}$ who maximizes $\frac{(\Pi_{i \in Q \cup \{k\}} \mu_{i}^{2}) \det(S_{Q \cup \{k\}}) - (\Pi_{i \in Q} \mu_{i}^{2}) \det(S_{Q})}{b_{k}}, k \in [N']$ $Q \leftarrow Q \cup \{k\}, [N'] \leftarrow [N'] \setminus k$ 7 Return the index set Q of the selected clients

# 5.2.2 Diversity-driven Client Selection

Taking content diversity as the quality metric of a client, we have $\begin{array} { r } { \mathbf { \tilde { V } } _ { \rho } ( \mathcal { Q } ) = \rho ( \mathcal { D } ) } \end{array}$ , where $\begin{array} { r } { \hat { \mathcal { D } } ^ { \setminus } = \bigcup _ { k \in \mathcal { Q } } \mathcal { D } _ { k } } \end{array}$ . According to Definition 2, we need to first generate content embedding vectors of samples. Similar to existing work [17], [18], [54], we let each client use a general deep learning model $( e . g $ VGG-16 [55]) to generate a content embedding vector for each sample. However, those work require direct access to all embedding vectors, which violates client’s privacy. Besides, when the total number of samples is large, the complexity of $\operatorname { E q } . 3$ is very high. To address these issues, we propose an efficient privacy-preserving content diversity computation method, which sketches each client’s dataset by a low-dimensional vector based on JL-transformation [56] and protects the privacy of each sample using a random response mechanism.

• Dataset content sketch. Each client $\mathcal { C } _ { k } , k \in \mathcal { Q }$ locally generates content embedding vectors $\phi _ { k } = \{ \phi _ { k , i } | z _ { k , i } \in \mathcal { D } _ { k } \}$ for all relevant samples using a general deep learning model, where each embedding vector $\phi _ { k , i } ~ \in ~ \bar { \mathbb { R } } ^ { L _ { \phi } } . ~ L _ { \phi }$ is 512 in our implementation. To further encode nk Lϕ-dimensional vectors into one low-dimensional vector, the server selects a projection matrix $\boldsymbol { w } \in \mathbb { R } ^ { l _ { \phi } \times L _ { \phi } }$ , where $l _ { \phi } < L _ { \phi } ,$ , and sends it to all relevant clients. Each client $\mathcal { C } _ { k }$ locally compute the $l _ { \phi ^ { - } }$ dimensional projection vector $h ( \phi _ { k , i } ) = \mathrm { \dot { s i g n } } ( \mathrm { \boldsymbol { \dot { w } } } \cdot \phi _ { k , i } )$ for each sample $\phi _ { k , i }$ . In particular, when each entry of w is generated independently from $\mathcal { N } ( 0 , 1 )$ , with $l _ { \phi } \dot { > } \frac { 1 } { \epsilon ^ { 2 } }$ lognk it with high probability achieves at most ϵ distortion for $n _ { k }$ samples of client $\mathcal { C } _ { k } \ [ 5 7 ]$ . The distortion caused by this projection reduces the accuracy of diversity but also protect

the privacy of embedding vector to a certain extend. Then the sketch of dataset $\mathcal { D } _ { k }$ is $\begin{array} { r } { H _ { k } = \sum _ { z _ { k , i } \in \mathcal { D } _ { k } } h ( \phi _ { k , i } ) } \end{array}$ .

• Permanent randomized response. To further protect the existence of each sample, we use a widely adopted randomized response mechanism [58] to generate a noisy representation $\hat { h } ( \phi _ { k , i } )$ of each projection vector $h ( \phi _ { k , i } )$ . Specifically, we add noises as follows:

$$
\hat {h} (\phi_ {k, i}) [ j ] = \left\{ \begin{array}{l l} 1, & \text { with   probability } \frac {f}{2} \\ 0, & \text { with   probability } \frac {f}{2} \\ h (\phi_ {k, i}) [ j ], & \text { with   probability } 1 - f. \end{array} \right. \tag {10}
$$

Here $\hat { h } ( \phi _ { k , i } ) [ j ]$ is the $j { \cdot } \mathrm { t h }$ bit of $\hat { h } ( \phi _ { k , i } )$ , and $0 < j \le l _ { \phi }$ $f$ is a user-defined parameter to control the level of privacy. $\hat { h } ( \phi _ { k , i } )$ is generated once and used for all FL tasks to save computation cost, and more importantly, to avoid privacy leakage caused by multiple queries. Then each client uses the noisy projection vectors to generate a noisy sketch $\begin{array} { r } { \hat { H } _ { k } = \sum _ { z _ { k , i } \in \mathcal { D } _ { k } } \hat { h } ( \phi _ { k , i } ) } \end{array}$ and reports it to the server for content diversity measurement. It is proved that this randomized response satisfies $\epsilon _ { \infty }$ -differential privacy where $\begin{array} { r } { \epsilon _ { \infty } = 2 l _ { \phi } \ln ( \frac { 1 - \frac { 1 } { f / 2 } } { f / 2 } ) } \end{array}$ . In this way, we prevent any other party including the server to learn the existence of any sample with confidence.

Given the noisy content sketch of each client, the similarities between two clients’ datasets $\mathcal { D } _ { k }$ and $\mathcal { D } _ { j }$ is defined as $\begin{array} { r } { S _ { k j } = \frac { \hat { H } _ { k } { \cdot } \hat { H } _ { j } } { | \hat { H } _ { k } | | \hat { H } _ { j } | } } \end{array}$ Skj = j . Then, the server can calculate the diversity value using noisy content sketches from all relevant clients with Eq.(3), which significantly reduces the computation cost of the content diversity by several orders of magnitude. The optimal solution to maximize the diversity value function is by greedily choosing the next client who has the minimum similarity to the currently selected clients.

# 5.2.3 DPP-based Client Selection

When we aim to select clients with high homogeneity and diversity, we convert the client selection problem into a DPP problem. A DPP is a random process used to model particles with repulsive interactions, which prohibits co-occurrences of highly correlated states [59]. This property makes DPP suited to select client with homogeneous distributed categories and avoiding highly similar clients.

Each client $\mathcal { C } _ { i } , i \in [ N ^ { \prime } ]$ is featured by its data statistical homogeneity $\mu _ { i } ,$ and similarities $S _ { i j }$ to other clients $\begin{array} { r } { \begin{array} { l } { \mathcal { C } _ { j } , j \ \in \ \mathsf { \Gamma } [ \breve { N ^ { \prime } } ] \ \backslash \ \backslash \ } \end{array} } \end{array}$ With $\mu _ { i } ~ > ~ 0 , 0 ~ \leq ~ \bar { S } _ { i j } ~ \leq ~ 1$ , we define a positive-semidefinite kernel $A _ { [ N ^ { \prime } ] } ~ = ~ [ A _ { i j } ] _ { i , j \in [ N ^ { \prime } ] } ,$ where $A _ { i j } ~ = ~ \mu _ { i } \mu _ { j } S _ { i j }$ . Then the probability of selecting clients Q is $P _ { A } ( \mathcal { Q } )$ , which is the determinant of $A _ { \mathcal { Q } } , i . e . ,$ $P _ { A } ( \mathcal { Q } ) = d e t ( A _ { \mathcal { Q } } )$ . We give one example to illustrate the implicit meaning of the determinantal probability measure with a subset $\mathcal { Q } = \{ i , j \}$ ,

$$
P _ {A} (\mathcal {Q}) \propto \left| \begin{array}{c c} A _ {i i} & A _ {i j} \\ A _ {j i} & A _ {j j} \end{array} \right| = \left| \begin{array}{c c} \mu_ {i} ^ {2} & \mu_ {j} \mu_ {i} S _ {i j} \\ \mu_ {i} \mu_ {j} S _ {i j} & \mu_ {j} ^ {2} \end{array} \right|. \tag {11}
$$

The diagonal entries are computed without a similarity term because the similarity to itself is always one. The determinant increases when the homogeneity increases and the similarity decreases, thus the DPP-based selection tends to choose clients with homogeneous distributed categories while avoiding highly similar clients simultaneously.

Algorithm 2: HE-based Client and Feature Selection for VFL before Training   
Input : Server S, the budget B, $N'$ clients $\{C_{1},\cdots,C_{N'}\}$ declaring the price $\{b_{1},\cdots,b_{N'}\}$ Output: The index set of selected clients and features

1 The server generates an indicator matrix $\Gamma$ , $[\Gamma] \leftarrow Enc(\Gamma)$ , sends $[\Gamma]$ to all clients

2 for each client $C_{k}, k \in [N']$ do

3 Induce a partition $U_{k,1} \cup U_{k,2} \cup \cdots \cup U_{k,c}$ of $D_{k}$ .

4 Calculates $[p_{k,o}]$ of a random selected instance from $U_{k,s}$ with $[\Gamma]$ , and calculates $[p_{k,o}]^{2}$ with the method from [60].

5 $[G(U_{k,s})] \leftarrow 1 - \sum_{k=1}^{|Y|}[p_{k,o}]^{2}$ 6 $[G(F_{k,j})] \leftarrow \sum_{s=1}^{c} \frac{|U_{k,s}|}{n} \cdot [G(U_{k,s})]$ 7 Sends $[G(F_{k,j})]$ to the server

8 The server initializes a client index set $Q \leftarrow \varnothing$ , and a feature index set $Q_{k} \leftarrow \varnothing$ of client $k, k \in [N']$ 9 while $\sum_{C_{k} \in Q} b_{k} < B$ do

10 $G(F_{k,j}) \leftarrow Dec([G(F_{k,j})])$ , identifies features whose $G(F_{k,j}) < \tau$ , and put their indexes into $Q'_{k}$ 11 The server finds client $C_{k}$ who maximizes

12 $\frac{\sum_{i=1}^{d_{k}} I[G(F_{k,j}) > \tau]}{b_{k}}, k \in [N']$ 13 Return the index set Q of the selected clients, and $Q'_{k}$ of the selected features for $k \in Q$ .

The value function is $\begin{array} { r c l } { { V _ { d } ( \mathcal { Q } ) } } & { { = } } & { { \operatorname* { d e t } ( A _ { \mathcal { Q } } ) } } \end{array}$ , where $\mathrm { d e t } ( A _ { \mathcal { Q } } ) = \Pi _ { i \in \mathcal { Q } } \mu _ { i } ^ { 2 } \mathrm { d e t } ( S _ { \mathcal { Q } } ) , S _ { \mathcal { Q } } = [ S _ { i j } ] _ { i , j \in \mathcal { Q } } .$ . Given $N ^ { \prime }$ relevant clients, each client $\mathcal { C } _ { k }$ has a declared price $b _ { k } ,$ the optimization problem is NP-hard because all possible subsets have to be examined. We adopted one simple greedy algorithm to approximate the optimal solution with an approximation ratio of ${ \frac { 8 } { 9 } } + \epsilon _ { 1 } ,$ and convert it into a log-submodular problem [59]. To this end, our algorithm iteratively adds k to the result collection Q if $\mathcal { C } _ { k }$ maximizes $P _ { A } ( \mathcal { Q } \cup \mathbf { \dot { \{ k \} } } )$ ) among the remaining clients. The main steps are summarized in Algorithm 1.

# 5.3 Client Selection & Feature Selection for VFL

After samples IDs are matched, each relevant client ${ \mathcal { C } } _ { k } ,$ $k \in N ^ { \prime }$ owns a local dataset $\mathcal { D } _ { k } \in \mathbb { R } ^ { n ^ { \prime } \times d _ { k } }$ , where $n ^ { \prime }$ is the size of matched samples IDs, $d _ { k }$ is the feature size of each sample in $\mathcal { D } _ { k }$ . The server S is the one owning the label set Y. Here, we take the Gini score as the importance metric of individual features. The features whose Gini values are below a threshold are considered to be important ones.

Client $\mathcal { C } _ { k }$ induces a partition $U _ { k , 1 } \cup \tilde { U _ { k , 2 } } \cup \cdots \cup U _ { k , c }$ of $\mathcal { D } _ { k }$ in which $U _ { k , s }$ is the set of instances that have the s-th value of feature $F _ { k , j }$ . The Gini impurity $U _ { k , s }$ is defined as $\begin{array} { r } { G ( U _ { k , s } ) = 1 - \sum _ { k \in [ C ] } p _ { m , k } ^ { 2 } , } \end{array}$ where $p _ { m , k }$ is the probability of a randomly selected instance from $U _ { k , s }$ that belongs to the s-th class. The Gini score of feature $F _ { k , j }$ is calculated as G(Fk,j ) = Pi∈[c] |Uk,s||Um| $\begin{array} { r } { G ( F _ { k , j } ) = \sum _ { i \in [ c ] } \frac { | U _ { k , s } | } { | U _ { m } | } \cdot G ( U _ { k , s } ) } \end{array}$ · G(Uk,s), where G(Fk,j ) mea- $G ( F _ { k , j } )$ sures the likelihood of a randomly selected instance being misclassified. If $F _ { k , j }$ is a feature with continuous values,

then $G ( F _ { k , j } )$ is defined as the weighted average of the Gini impurities of a set of discrete feature values. Then, we have $\begin{array} { r } { \hat { V _ { g } ( Q ) } = \sum _ { k \in \mathcal { Q } } \sum _ { i = 1 } ^ { d _ { k } } I [ G ( F _ { k , j } ) > \tau ] , } \end{array}$ , where  equals $I [ G ( F _ { k , j } ) > \tau ]$ $G ( F _ { k , j } )$ $G ( F _ { k , j } ) > \tau ,$ otherwise 0. We use the Paillier as the PHE method which supports homomorphic addition of two ciphertexts and homomorphic multiplication between a plaintext and a ciphertext. We design an efficient and secure collaborative calculation protocol, which is shown in Algorithm 2.

Specifically, the server first S generates an indicator matrix Γ with size of $n ^ { \prime } \times | \mathcal { V } | ,$ in which $\Gamma _ { i j }$ indicates whether the category of the i-th sample is $j$ for $i \in [ n ^ { \prime } ] .$ , $j \in [ | \mathcal { V } | ]$ ]. That is, if the category of the i-th sample is $j ,$ then $\Gamma _ { i j }$ equals one, otherwise zero. Then, the probability $p _ { m }$ ,k , $k \in [ \bar { | } \mathcal { V } | ]$ of a random selected instance from $U _ { k , s }$ can be calculated by $\begin{array} { r } { p _ { m , k } = \sum _ { i \in I ( U _ { k , s } ) } \Gamma _ { i k } / | U _ { k , s } | } \end{array}$ after $\mathcal { C } _ { k } .$ , where $I ( U _ { k , s } )$ denotes the index set of instances from $U _ { k , s } .$ . In ${ \mathrm { V F L } } ,$ however, Γ cannot be transmitted in plaintext, because the information of the original labels will be expose directly to client $\mathcal { C } _ { k } .$ . To this end, the server S generates a pair of public and private keys for homomorphic encryption, and encrypts the matrix Γ with the public key. The server sends the encrypted matrix [[Γ]] to all clients. Then, client $\mathcal { C } _ { k }$ calculates the probability $[ [ p _ { m , k } ] ]$ with [[Γ]], and calculates the square of $[ \bar { p } _ { m , k } ]$ with one existing solution from [60]. In addition, client k calculates the Gini impurity $\mathbb { E } ( F _ { k , j } ) ]$ of feature $F _ { k , j }$ and sends them to the server. After receiving them, the server decrypts them with the private key to obtain $\{ G ( F _ { k , j } ) \}$ , and identifies those features whose Gini scores are greater than τ . After this computation, only the server learns the importance of each relevant client’s features, while other parties learn nothing. Now the server can solve the optimization problem $( \mathrm { E q . ~ } 1 )$ by greedily choosing the clients with the largest $\textstyle \sum _ { i = 1 } ^ { d _ { k } } \tilde { I } [ G ( \bar { F } _ { k , j } ) > \bar { \tau _ { \rfloor } } / b _ { k } , k \in \bar { [ N ^ { \prime } ] }$ until the budget B runs out.

The total computation cost of Algorithm 2 of each client is $O ( 1 )$ operations due to multiple addition and multiplication operations, and the communication cost is $O ( n ^ { \prime } | \hat { \mathcal { V } } | )$ . $\begin{array} { r } { 1 ) ) + \sum _ { k = 1 } ^ { N ^ { \prime } } d _ { k } ^ { 2 } ) } \end{array}$ computation cost is  operations [11] and $\begin{array} { r } { O ( n ^ { \prime } ( | \mathcal { V } | + \sum _ { k = 1 } ^ { N ^ { \prime } } ( d _ { k } + } \end{array}$ is $\begin{array} { r } { O ( s i z e (  { \left\| \Gamma \right\| } ) + \frac { \sum _ { k = 1 } ^ { K } d _ { k } } { K } \cdot s i z e (  { \left\| G ( F _ { k , j } ) \right\| } ) ) } \end{array}$ PKk=1 dkK · size([[G(Fk,j )]])) where size([[Γ]]), K size $\big ( \mathbb { f } G ( F _ { k , j } ) \big ] \big )$ ) denote sizes of [[A]] and $\big [ G ( F _ { k , j } ) \big ] \big ]$ .

# 6 DYNAMICAL SAMPLE SELECTION

In this section, we present the detailed design of the effective importance-aware dynamic sample selection, to further improve the model performance and reduce the training overhead for both HFL and VFL. In addition, we prove the convergence of the proposed method.

1) For HFL: Given selected high-quality clients whose index set is $\begin{array} { r } { \mathcal { Q } \subset [ N ^ { \prime } ] , | \mathcal { Q } | = K , } \end{array}$ in each training iteration t, ζ-fraction of important clients are selected and then their important samples are used for training. A straightforward method to measure the importance of each client $\breve { \mathscr { C } } _ { k } , k \in [ K ]$ is to calculate $\lambda ( \mathcal { D } _ { k } , t )$ using Eq.6 and obtain client selection distribution $P _ { k } ^ { t } , k \in [ K ]$ . This method, however, can be very computationally expensive, which requires $O ( n s )$ (s is the number of model parameters $\theta \in \mathbb { R } ^ { s } ,$ n is the number of total samples) operations in each iteration. n and s are usually large in federated deep learning tasks. To reduce the cost, for dynamic client selection, we propose a simple but effective method to update the probability $P _ { k } ^ { t }$ based on the training updates $( i . e . , \dot { \theta } _ { t } ^ { k } , \theta _ { t } )$ stored in the server. Specifically, in the t-th iteration, the server selects m clients according to their current selection probabilities $\{ P _ { 1 } ^ { t } , \cdots , P _ { K } ^ { t } \}$ updated using the following equation

Algorithm 3: HFL with Importance-based Sample Selection   
Input : K clients $\{C_{1},\cdots,C_{K}\}$ have datasets $\{D_{1},\ldots,D_{K}\}$ and initial client selection probability $\{P_{1}^{1},\ldots,P_{K}^{1}\}$ , E is the number of local epochs, $\eta$ is the learning rate, and $\zeta$ is the fraction of clients being selected

Output: Global model $\theta^{*}$ 1 Server initializes $\theta_{0}$ 2 for each round $t=\{1,2,\cdots,T\}$ do

3 $m\leftarrow\max(\zeta\cdot K,1)$ 4 $M_{t}\leftarrow m$ clients selected based on selection probabilities $\{P_{1}^{t},\ldots,P_{K}^{t}\}$ 5 for each client $C_{k}\in M_{t}$ in parallel do

6 $\theta_{t+1}^{k}\leftarrow LocalModelUpdate(k,\theta_{t})$ 7 $\theta_{t+1}\leftarrow\sum_{C_{k}\in M_{t}}\frac{n_{k}}{n}\theta_{t+1}^{k} // update global model$ 8 for each client $C_{k}\in M_{t}$ do

9 $P_{k}^{t+1}=\frac{n_{k}||\theta_{t}^{k}-\theta_{t}||}{\sum_{C_{k}\in M_{t}}n_{k}||\theta_{t}^{k}-\theta_{t}||} // update client selection probability$ 10 Function LocalModelUpdate $(k,\theta_{t})$ :

11 Calculates $\lambda(z_{k,i},t-1),p_{k,i}^{t-1},i\in[U_{k}]$ using Eq.5,

12 $\theta_{0}^{k}=\theta_{t}$ 13 for each local epoch j from 1 to E do

14 $\gamma_{k}^{j}\leftarrow g$ data samples selected with $\{p_{k,1}^{t-1},\cdots,p_{k,n_{k}}^{t-1}\}$ from $D_{k}$ , and $\lambda(z_{k,j},t-1)<\delta_{k}^{t-1}$ 15 Return global model $\theta_{T}$ .

$$
P _ {k} ^ {t} = \frac {n _ {k} | \theta_ {t - 1} ^ {k} - \theta_ {t - 1} |}{\sum_ {\mathcal {C} _ {k} \in M _ {t - 1}} n _ {k} | \theta_ {t - 1} ^ {k} - \theta_ {t - 1} |}, \tag {12}
$$

where $M _ { t - 1 }$ is the set of m clients selected in the $t - 1 \mathrm { - } \mathrm { t h }$ iteration. That is, we assign clients with larger influences on the current global model $\theta _ { t - 1 }$ higher probabilities $P _ { k } ^ { t }$ to be selected in the t-th iteration. Then for each selected client $\mathcal { C } _ { k }$ in round t, it calculates the importance $\lambda ( z _ { k , i } , t -$ 1) for all samples $z _ { k , i } \in \mathcal { D } _ { k }$ according to Eq.5, and selects local samples with $\begin{array} { r } { \lambda ( z _ { k , i } , t - 1 ) \le \delta _ { k } ^ { t - 1 } } \end{array}$ according to $p _ { k , i } ^ { t } \propto$ $\lambda ( z _ { k , i } , t - 1 )$ . The details of the HFL with importance based dynamic data selection are presented in Algorithm 3.

2) For VFL: Given selected high-quality clients whose index set is $\mathcal { Q } \subset [ N ^ { \prime } ] , | \mathcal { Q } | = K$ , in each iteration $t , g$ important samples are dynamically selected as the batch for training. As illustrated in Section 4.1.2, the sample importance for VFL can be quantified as the gradient upper bound norm of the global loss with respect to the pre-activation outputs. Thus, we select samples with the probability $p _ { i } ^ { t } \propto \lambda ( i , \hat { t } - 1 )$ for $i \in [ n ^ { \prime } ]$ . We present our VFL with importance-based sample selection based on HE to preserve privacy for all participants [43]. Specifically, $n ^ { \prime }$ samples have equal initial

Algorithm 4: VFL with Importance-based Sample Selection   
Input : K clients $\{C_{1},\cdots,C_{K}\}$ with datasets $\{D_{1},\ldots,D_{K}\}$ , an initial ID set $G_{1}$ , and a noise set $\{\epsilon_{1,acc},\cdots,\epsilon_{K,acc}\}$ with initial values of zero, $\eta$ is the learning rate

Output: Global model $\theta^{*}$ for each round $t=\{1,2,\cdots,T\}$ do

    for each client $C_{k}, k\in[K]$ do $\gamma_{k}^{t}\leftarrow g$ data samples with IDs from $G_{1}$ $e_{k}\leftarrow f_{k}^{v}(\gamma_{k}^{t};\theta_{t}^{k}), k\in[N],[[e_{k}]]\leftarrow Enc(e_{k})$ Sends $[[e_{k}]]$ to the server

    Server do

    Initializes $\theta_{0},\{w_{1},\cdots,w_{K}\}$ $[[e_{k}^{\prime}]]\leftarrow [[e_{k}]]\otimes w_{k}$ , adds random noise $[[e_{k}^{\prime}+\epsilon_{s}^{t}]]\leftarrow \epsilon_{s}^{t}\oplus [[e_{k}^{\prime}]], sends [[e_{k}^{\prime}+\epsilon_{s}^{t}]]$ to client $C_{k}, k\in[K]$ for each client $C_{k}, k\in[K]$ do $e_{k}^{\prime}+\epsilon_{s}^{t}\leftarrow Dec([e_{k}^{\prime}+\epsilon_{s}^{t}])$ Generates random noise $\epsilon_{k}^{t},\epsilon_{k,acc}\leftarrow \epsilon_{k,acc}+\epsilon_{k}^{t}$ Calculates $e_{k}^{\prime}+\epsilon_{s}^{t}+e_{k}\epsilon_{k,acc}$ , sends it to the server

    Server do $e_{k}^{\prime}+e_{k}\epsilon_{k,acc}\leftarrow e_{k}^{\prime}+\epsilon_{s}^{t}+e_{k}\epsilon_{k,acc}-\epsilon_{s}^{t},$ $e\leftarrow(e_{1}^{\prime}+e_{1}\epsilon_{k,acc}||\cdots||e_{K}^{\prime}+e_{K}\epsilon_{k,acc})$ $\delta_{k}\leftarrow\nabla_{e_{k}}L(\theta;e;\mathcal{Y}),[\delta_{k}e_{k}+\epsilon_{s}^{t}]\leftarrow Enc(\delta_{k}e_{k}+\epsilon_{s}^{t})$ Sends $[[\delta_{k}e_{k}+\epsilon_{s}^{t}]$ to client $C_{k}, k\in[K]$ for each client $C_{k}, k\in[K]$ do $\delta_{k}e_{k}+\epsilon_{s}^{t}\leftarrow Dec([[\delta_{k}e_{k}+\epsilon_{s}^{t}]]), calculates$ $\delta_{k}e_{s}+\epsilon_{s}^{t}+\epsilon_{k}^{t}/\eta,[[\epsilon_{k,acc}]]\leftarrow \epsilon_{k,acc}$ Sends $\delta_{k}e_{s}+\epsilon_{s}^{t}+\epsilon_{k}^{t}/\eta,[[\epsilon_{k,acc}]]$ to the server

    Server do $[[\delta_{k}^{\prime}]]\leftarrow Enc(\delta_{k}(w_{k}+\epsilon_{k,acc}))$ Calculates $\lambda(i,t), p_{i}^{t}$ using Eq.8 $G_{t}\leftarrow g$ IDs selected with $\{p_{1}^{t-1},\cdots,p_{n'}^{t-1}\}$ from $[n']$ Sends $[[\delta_{k}^{\prime}]], G_{t}$ to client $C_{k}, k\in[K]$ $w_{k}\leftarrow w_{k}\eta(\delta_{k}e_{k}+\epsilon_{s}\epsilon_{k}^{t}/\eta-\epsilon_{s}),$ $\theta_{t}= \theta_{t-1}+\eta\nabla_eL(\theta;e;\mathcal{Y}) // update global model$ for each client $C_{k}, k\in[K]$ do $\delta_{k}^{\prime}\leftarrow Dec([[\delta_{k}^{\prime}]]), calculates \nabla_\theta_k\delta_k^{\prime}$ Return global model $\theta_T$ .

selection probability $p _ { 1 } ^ { 1 } = p _ { 2 } ^ { 1 } = \cdot \cdot \cdot p _ { n ^ { \prime } } ^ { 1 } ,$ in the t-th iteraaccording to the selection probabilities tion, the server selects $g$ IDs (forming a sample ID set $\{ p _ { 1 } ^ { t - 1 } , \cdot \cdot \cdot , p _ { n ^ { \prime } } ^ { t - 1 } \}$ . To $G _ { t } )$ prevent local embedding $e _ { k }$ from being leaked, client $\mathcal { C } _ { k }$ generates a random noise $\epsilon _ { k } ^ { t } ,$ and adds up these noises to obtain $\epsilon _ { k , a c c }$ . Meanwhile, the server generates random noise $\epsilon _ { s }$ to prevent clients from accumulating activation prediction pairs to infer the weights of the global model on the server. Finally, client $\mathcal { C } _ { k }$ removes the injected noise $\epsilon _ { k } ^ { t }$ by the accumulated noise $\epsilon _ { k , a c c } ,$ and the server removes the noise $\epsilon _ { s } ^ { t }$ before it updates wk, $k \in [ K ] , t \in [ T ]$ . The details of the VFL with importance based dynamic data selection are presented in Algorithm 4.

# 7 EVALUATIONS

In this section, we measure the effectiveness of our proposed quality-driven client selections, including homogeneityaware selection, diversity-driven selection and DPP-based selection. Then, we show that our dynamical sample selection improve the global model to achieve a higher accuracy and faster convergence rate.

# 7.1 System Deployment

We implemented and deployed our data selection methods on a real AIoT system with one server and 50 clients, including 20 edge nodes, 20 laptops and 11 desktops (see details in Table 1). We used one desktop worked as the server and let other 10 desktops work as clients. All devices are connected by Wi-Fi. We leverage different types of devices in our implementation to represent the practical heterogeneous FL setting where different types of devices have different computation and communication resources. Implementing our sample selection algorithm in such a heterogeneous setting can better demonstrate the robustness and the superiority of our algorithm.

TABLE 1 System Deployment. 

<table><tr><td>Devices</td><td>#</td><td>Information</td></tr><tr><td>Edge node</td><td>20</td><td>Intel i7-6700 CPU, 16G RAM, Tesla P4/T4 GPUs</td></tr><tr><td>Desktop</td><td>20</td><td>Intel i7 CPU, 64G RAM, 4 Titan X GPUs</td></tr><tr><td>Laptop</td><td>11</td><td>Intel i7 CPU, 16G RAM</td></tr></table>

# 7.2 Experiment Configuration

# 7.2.1 Datasets

For HFL, we constructed two types (error-free and erroneous) of training datasets on MNIST [61] and CIFAR10 [39] for different tasks (see details in Table 2). We employ 50 clients in our setting. The test datasets $\mathcal { D } _ { M } ^ { T } , ~ \mathcal { D } _ { C } ^ { T }$ were located at the server. For VFL, we use two synthetic datasets, MADELON [41] and FRIEDMAN [62]; and three real-world datasets, LSVT [63], SPEED [64] and ARCENE [65]. MADELON consists of 5 informative features, 15 redundant features constructed by linear combinations of those 5 informative features, and 480 noisy features, while FRIEDMAN consists of 5 informative and 995 noisy features. The descriptions of datasets are listed in Table 2 and Table 3. We employ two clients, where we divide features into two parts randomly for every dataset, and assign each part to each client. The labels are located in the server.

# 7.2.2 Deep Learning Models

For HFL, we implemented the typical federated optimization algorithm FedSGD [4] and two popular deep learning models, HFL-MNIST (a CNN network [66] for digit number recognition) and HFL-CIFAR (a residual network [40] for image recognition). For VFL, we implemented the typical logistic regression model VFL-FRIED for VFL [67] on FRIEDMAN, and four neural networks for VFL VFL-MADELON, VFL-LSVT, VFL-SPEED and VFL-ARCENE [43] on the other four datasets. We run federated learning until a pre-specified test accuracy is reached (e.g., 98.0% for $\mathcal { D } _ { M }$ and 92.5% for $\mathcal { D } _ { C } )$ , or a maximum number of iterations have elapsed. We test the accuracy of the global model on the test datasets. We build our VFL models with Flower 0.19.0 [68] and Pytorch 1.8.1.

TABLE 2 Datasets for different HFL tasks. 

<table><tr><td>Type</td><td>Notation</td><td>Size</td><td>Description</td></tr><tr><td rowspan="4">Training</td><td> $\mathcal{D}_{M}$ </td><td>60,000</td><td rowspan="4">original training data of MNIST $\mathcal{D}_{M}$  40% mislabeled samplesoriginal training data of CIFAR $\mathcal{D}_{C}$  with 30% mislabeled samples</td></tr><tr><td> $\mathcal{D}_{M}^{m}$ </td><td>60,000</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>50,000</td></tr><tr><td> $\mathcal{D}_{C}^{m}$ </td><td>50,000</td></tr><tr><td rowspan="2">Testing</td><td> $\mathcal{D}_{M}^{T}$ </td><td>10,000</td><td rowspan="2">original test data of MNISToriginal test data of CIFAR</td></tr><tr><td> $\mathcal{D}_{C}^{T}$ </td><td>10,000</td></tr></table>

TABLE 3 Datasets for different VFL tasks. 

<table><tr><td>Dataset</td><td>Features</td><td>Train size</td><td>Test size</td><td>Classes</td><td>Type</td></tr><tr><td>MADELON</td><td>500</td><td>2,000</td><td>2,400</td><td>2</td><td>Tabular</td></tr><tr><td>FRIEDMAN</td><td>1,000</td><td>750</td><td>250</td><td>2</td><td>Tabular</td></tr><tr><td>LSVT</td><td>309</td><td>100</td><td>26</td><td>2</td><td>Multivariate</td></tr><tr><td>SPEED</td><td>122</td><td>6702</td><td>1676</td><td>2</td><td>Tabular</td></tr><tr><td>ARCENE</td><td>10,000</td><td>1,400</td><td>600</td><td>2</td><td>Tabular</td></tr></table>

# 7.3 Quality-driven Client Selection for HFL

We first evaluate the proposed three quality-driven client selection methods, homogeneity-aware, diversity-driven and DPP-based methods (see details in Section 5). We partitioned datasets $\mathcal { D } _ { M } , \mathcal { D } _ { C }$ over 50 clients with five different statistical homogeneity and content diversity settings. In the first setting, 10 IID and 40 Non-IID (k) clients, here k is randomly selected from 1 to 9; each client has the same amount of data; for each client, we randomly removed 50%-90% samples and add the same amount of samples transformed from remaining samples (see in Section 3.3). We repetitively increased the number of IID clients by 5 and reduced the proportion of transformed samples by 10% for four times to compose the dataset in the other four settings. For the declared prices, we considered two commonly used models, identical price and normally distributed price. The mean value of normal distribution equals to the identical price, which is set to 1.0 for each sample, and the variance is 0.2. Then the declared price of each client is the summation of all his/her samples’ prices. The budget is set to 24, 000, 20, 000 for $\mathcal { D } _ { M } , ~ \bar { \mathcal { D } } _ { C }$ . We selected clients by three selection methods in five settings. Compared with directly calculating content diversity using embedding vectors, our sketch based method reduce the time cost from 68.60h and 57.56h to 102.71s and 383.82s for $\mathcal { D } _ { M } , \mathcal { D } _ { C } .$ , respectively.

We trained various models on selected clients. The test accuracy for $\mathcal { D } _ { M } ^ { T }$ and $\mathcal { D } _ { C } ^ { T }$ is shown in Fig. 5, which shows that our three privacy-preserving quality-driven client selection methods all outperform the commonly used random client selection. Specially, for diversity-driven client selection, we compare the method using only content sketch and the one using sketch and randomized response. To achieve differential privacy for each sample, though the randomized response introduces some noises to the content sketch, it still has obviously higher accuracy than that of the random selection. Our DPP-based method performs best in all cases and settings due to the fact that it considers both quality dimensions simultaneously. For example, in setting 5, the DPP-based methods can reduce the average false rate for digit recognition on MNIST from 17.75%, 16.73%, to 8.5%, 6.8%, and for image recognition on CIFAR from 36.8%, 34.8% to 18.96%, 18.91%, in identical price setting and normally distributed price setting respectively.

![](images/26bced43d50d2ec85d6411450d9e3c7ec7b3eb412fef294878a8bdcf7b8dadae.jpg)



(a) HFL-MNIST, identical price.

![](images/c8a24532ff9f0ebed8e4709ffc28fedecb72eb2222428922817814a07f1df730.jpg)



(b) HFL-MNIST, distributed price.

![](images/5662eb93c624b8aeafe746b149218e066b8a38dcdf1d0050acf09c26135a1f15.jpg)



(c) HFL-CIFAR, identical price.

![](images/ed0815abb394af453e55bb5f21fe859c13b1a0169640ed2abb6328be0221dc5c.jpg)



(d) HFL-CIFAR, normly distributed price.

Fig. 5. Test accuracy for training HFL-MNIST and HFL-CIFAR models on clients having data samples with different statistical homogeneity and content diversity in different declared price models. The X-coordinate indicates setting 1-5.   
![](images/7d9b847f6d5269939e5cdd9d77266b48acbfc005800f2e84da31498db7b5a036.jpg)



(a) HFL-MNIST, DM.

![](images/07850a2f1ca94b4361834b8a69f8ff1ccc286edf3acae61c87d64bee6f245ec9.jpg)



(b) HFL-CIFAR, DC.

![](images/bebd500876803b1cb238ce74f5b2459f7cde75077ad1a57d469f586cb50197e8.jpg)



(c) HFL-MNIST, DmM.

![](images/b0d633472a8005e6c2fae2e5ee4fe4d40cdcca5b5317f840f000c4986a8143ee.jpg)



(d) $\mathrm { H F L - C I F A R } , \mathcal { D } _ { C } ^ { m }$ .

Fig. 6. Test accuracy against training time for training various models on on clean datasets and erroneous dataset with different sampling methods. Here “updates-upper” indicates selecting first clients using Eq. 12 and then samples using $\mathsf { E q . } 5 .$ .   
![](images/9d7a178eed88b22f78d5e9a08db286c7dc47615699ad1e588b2b44b2226745c9.jpg)



(a) Computation cost (s).

![](images/41898fa90d82832dccabbc2e0c17b4861a83815dd28786853e82b4023f784d5b.jpg)



(b) Communication cost (MB).

![](images/f5fdea32a7218cd41af19924d9a6294dc0a697e776ea5eb3e13c30273829569d.jpg)



(a) MADELON.

![](images/ef169fd78964a428c8bba9d4be490817fa6a7a393f2aade4e30aae21c6e89449.jpg)



(b) LSVT.   
Fig. 7. Computation and communication cost for training HFL-MNIST and HFL-CIFAR models on clean datasets DM , DC until the test accuracy reaches 98.0% for $\mathcal { D } _ { M }$ and 85.0% for $\mathcal { D } _ { C }$ with different sampling methods.   
Fig. 8. Test accuracy against training rounds for training VFL models on datasets MADELON and LSVT with different sampling methods. Here “updates-upper” indicates selecting samples using Eq.8.

# 7.4 Feature Selection for VFL

We compare our Gini impurity-based feature selection method against state-of-art baselines, 1) random: it performs random feature selection; 2) allFeatures: it performs feature selection with all features participating; 3) SFFS [11]: it performs feature selection with the filter method based on secure multi-party computation. We employ one client $\mathbf { A } ,$ and one server ${ \dot { S } } ,$ and assign different numbers of features to them to train different VFL models. The results are shown in Fig. 9. Here, the $R ^ { 2 }$ score is defined as R2 = 1 − Pn∈[N](yn−yˆn)2 , $\begin{array} { r } { R ^ { 2 } = 1 - \frac { \sum _ { n \in [ N ] } ( y _ { n } - \bar { y } _ { n } ) ^ { 2 } } { \sum _ { n \in [ N ] } ( y _ { n } - \bar { y } ) } } \end{array}$ Pn∈[N](yn−y¯) where y¯ = 1N Pn∈[N] yn, and $\begin{array} { r } { \bar { y } = \frac { 1 } { N } \sum _ { n \in [ N ] } y _ { n } , } \end{array}$ $y _ { n } , \hat { y } _ { n }$ are the true target and predicted target of the n-th sample, respectively. The results show that our Gini-based feature selection method achieves higher test accuracy and $R ^ { 2 }$ scores than other strategies. Further, as more features are selected, the test accuracy decreases because more noisy and redundant features are included.

Besides, for LSVT dataset, we calculated the Gini score of each feature, then split the features with the smallest 50 feature Gini scores into two parts to assign them to client A and the server. Then we randomly select 25, 75, 175, 275 features from the remaining ones to the client, respectively, and train the VFL model. The distributions of features of datasets SPEED and ARCENE are similar to that of dataset LSVT. Note that as the number of features assigned to client A increases, the number of nuisance features also increases, since the number of informative features is fixed. We perform 5-fold cross validation and report the average test accuracy, and model parameters vs. the number of selected features that the model uses. The results are presented in Table 4. We can see that the model trained with the features selected based on Gini scores achieves higher test accuracy than that of the model trained with randomly selected features. Meanwhile, as the number of randomly selected feature increases, the amount of model parameters increases significantly, which result in high computation overhead during model training. In addition, we present the communication cost of each client for Gini-based feature selection and various VFL models training in Table 5. The results show that the communication cost is much small and acceptable in training various VFL models. Therefore, we conclude that our method can achieve a more accurate model with a small number of features and a small amount of communications.

![](images/611117b28fc5fb01a9465505668921a89dea266fa7bbe6340d19fcb0f85d1742.jpg)



(a) VFLNN-MADELON

![](images/4bea3c73da0a345eb2c20e81cab462189cf5470275e75ec2015077e33fb18b36.jpg)



(b) VFLLR-FRIEDMAN   
Fig. 9. Test accuracy and $R ^ { 2 }$ scores vs. number of selected features on synthetic datasets.

TABLE 4 Test accuracy for training different datasets on VFL tasks. 

<table><tr><td>Dataset</td><td># Features</td><td>Test Accuracy</td><td>Standard Deviation</td><td># Parameters</td></tr><tr><td rowspan="5">LSVT</td><td>25</td><td>85.34%</td><td>1.66%</td><td>60,601</td></tr><tr><td>50</td><td>86.68%</td><td>3.65%</td><td>150,601</td></tr><tr><td>100</td><td>84.68%</td><td>2.68%</td><td>350,601</td></tr><tr><td>200</td><td>83.34%</td><td>3.0%</td><td>550,601</td></tr><tr><td>300</td><td>84.02%</td><td>1.36%</td><td>750,601</td></tr><tr><td rowspan="5">SPEED</td><td>10</td><td>84.72%</td><td>0.27%</td><td>18,049</td></tr><tr><td>40</td><td>85.62%</td><td>0.40%</td><td>19,969</td></tr><tr><td>60</td><td>84.54%</td><td>0.46%</td><td>21,249</td></tr><tr><td>80</td><td>84.96%</td><td>0.48%</td><td>22,529</td></tr><tr><td>110</td><td>84.94%</td><td>0.35%</td><td>24,449</td></tr><tr><td rowspan="5">ARCENE</td><td>100</td><td>83.60%</td><td>1.67%</td><td>60,601</td></tr><tr><td>1000</td><td>80.20%</td><td>1.48%</td><td>150,601</td></tr><tr><td>3000</td><td>80.60%</td><td>1.67%</td><td>350,601</td></tr><tr><td>5000</td><td>81.80%</td><td>1.48%</td><td>550,601</td></tr><tr><td>7000</td><td>81.40%</td><td>1.67%</td><td>750,601</td></tr></table>

TABLE 5 Communication cost for feature selection and VFL model training. 

<table><tr><td>Model</td><td>Gini selection (MB)</td><td>Model training (GB)</td></tr><tr><td>VFL-MADELON</td><td>0.41</td><td>0.29</td></tr><tr><td>VFL-FRIED</td><td>0.79</td><td>0.19</td></tr><tr><td>VFL-LSVT</td><td>0.24</td><td>0.06</td></tr><tr><td>VFL-SPEED</td><td>0.14</td><td>0.98</td></tr><tr><td>VFL-ARCENE</td><td>7.82</td><td>2.73</td></tr></table>

# 7.5 Dynamical Sample Selection

For HFL: We compare our upper bound norm based importance selection to other four state-of-the-art data selection strategies, random, loss based, and gradient norm based. Here we considered two typical FL scenarios, a crowd-sourced scenario with many clients and an enterprise cooperation scenario with two clients. For the first scenario, the model HFL-MNIST were trained on $\mathcal { D } _ { M } , \mathcal { D } _ { M } ^ { m }$ assigned to 50 clients, and 40 clients are selected for each iteration. For the second scenario, the model HFL-CIFAR were trained on $\mathcal { D } _ { C } , \mathcal { D } _ { C } ^ { m }$ assigned to 2 clients. To avoid selecting erroneous samples, the thresholds $\delta _ { k } ^ { t }$ was set to 10.0, 200.0 for $\mathcal { D } _ { M } ^ { m } , \mathcal { D } _ { C } ^ { m }$ , which is determined by detecting the outlier of upper bound norms of all samples (see Fig. 3.1 for an example). Fig. 6 shows that our method using both model updates and upper bound norm outperforms all other methods in terms both accuracy and convergence speed in all scenarios. In Fig. 6(a) and Fig. 6(b), where the datasets are clean, the loss based method achieves lower but comparable performance with our method. But in Fig. 6(c) and Fig. 6(d), where the datasets contains erroneous samples, the performance of loss based and gradient norm based methods deteriorate significantly, while our method still achieves high accuracy and stable convergence. On datasets $\mathcal { D } _ { M } ^ { m } , \mathcal { D } _ { C } ^ { m }$ , the test accuracy are 94.0%, 79.88% for random sampling, 91.8%, 56.02% of loss based sampling, 93.5%, 66.08% of gradient norm sampling, and 98.4%, 86.34% of our method. We present the computation and communication cost for training two models in Fig. 7. On $\mathcal { D } _ { M } .$ , our method saves 48.1%, 19.6%, 64.6% computation cost, and 50.3%, 20.5%, 66.8% communication cost compared to random, loss based and gradient based methods. On ${ \mathcal { D } } _ { C } ,$ our method saves 38.0%, 17.6%, 55.3% computation cost, 37.5%, 16.7%, 54.5% communication cost compared to those three methods.

For VFL: We evaluate the effectiveness of our dynamical sample selection for VFL (see details in Section 6). We compare our upper bound norm based on importance selection to the random sample selection method on two datasets, MADELON and LSVT. We divide the features into two parts, and assign them to the client and the server, and train the VFL model. The test accuracy against training rounds is shown in Fig. 8. The results demonstrate that our method using upper bound norm outperforms the random selection in terms both accuracy and convergence speed.

# 8 CONCLUSION

To the best of our knowledge, we propose the first effective and privacy-preserving sample selection solution for both HFL and VFL to obtain models with high accuracy and fast convergence speed when there are low-quality data. Our solution considers multiple factors that influence the model performance and both the clients’ data privacy and the server’s task privacy. To reduce the cost for data selection, we propose a set of novel techniques to first selects highquality clients before training and then dynamically selects clients and their samples with greater importance to the global model. Our experiments on a real AIoT system show that our design outperforms existing solutions in terms of higher model accuracy, faster convergence speed, and lower computation and communication cost.

# ACKNOWLEDGMENT

Lan Zhang is the corresponding authors. This research was supported by the National Key R&D Program of China 2021YFB2900103, National Natural Science Foundation of China with No.61932016, No.62132018, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002. This work was partially supported by “the Fundamental Research Funds for the Central Universities” WK2150110024, and Tencent Marketing Solution Rhino-Bird Focused Research Program.

# REFERENCES

[1] Q. L. C. M. X. S. Libing WU, Rui ZHANG, “A mobile edge computing-based applications execution framework for internet of vehicles,” Frontiers of Computer Science, vol. 16, no. 5, p. 165506, 2022.

[2] J. Z. T. Z. L. C. L. C. Yuya CUI, Degan ZHANG, “Multi-user reinforcement learning based task migration in mobile edge computing,” Frontiers of Computer Science, vol. 18, no. 4, p. 184504, 2024.   
[3] X. G. X. H. X. Z. Jian AN, Siyuan WU, “A blockchain-based framework for data quality in edge-computing-enabled crowdsensing,” Frontiers of Computer Science, vol. 17, no. 4, p. 174503, 2023.   
[4] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial Intelligence and Statistics, 2017, pp. 1273–1282.   
[5] M. Hu, P. Zhou, Z. Yue, Z. Ling, Y. Huang, A. Li, Y. Liu, X. Lian, and M. Chen, “Fedcross: Towards accurate federated learning via multi-model cross-aggregation,” in 2024 IEEE 40th International Conference on Data Engineering (ICDE). IEEE, 2024, pp. 2137–2150.   
[6] G. Wang, H. Guo, A. Li, X. Liu, and Q. Yan, “Federated iot interaction vulnerability analysis,” in 2023 IEEE 39th International Conference on Data Engineering (ICDE). IEEE, 2023, pp. 1517–1530.   
[7] Y. Hu, D. Niu, J. Yang, and S. Zhou, “Fdml: A collaborative machine learning framework for distributed features,” in Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2019, pp. 2232–2240.   
[8] J. Tan, L. Zhang, Y. Liu, A. Li, and Y. Wu, “Residue-based label protection mechanisms in vertical logistic regression,” in 2022 8th International Conference on Big Data Computing and Communications (BigCom). IEEE, 2022, pp. 356–364.   
[9] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. M. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 372–383.   
[10] T. Tuor, S. Wang, B. J. Ko, C. Liu, and K. K. Leung, “Data selection for federated learning with relevant and irrelevant data at clients,” arXiv preprint arXiv:2001.08300, 2020.   
[11] F. Pan, D. Meng, Y. Zhang, H. Li, and X. Li, “Secure federated feature selection for cross-feature federated learning,” 2020.   
[12] F. Sattler, S. Wiedemann, K.-R. Muller, and W. Samek, “Robust and ¨ communication-efficient federated learning from non-iid data,” IEEE transactions on neural networks and learning systems, 2019.   
[13] A. Katharopoulos and F. Fleuret, “Not all samples are created equal: Deep learning with importance sampling,” arXiv preprint arXiv:1803.00942, 2018.   
[14] L. Song, A. Smola, A. Gretton, J. Bedo, and K. Borgwardt, “Feature selection via dependence maximization.” Journal of Machine Learning Research, vol. 13, no. 5, 2012.   
[15] S. Wang, T. Tuor, T. Salonidis, K. K. Leung, C. Makaya, T. He, and K. Chan, “When edge meets learning: Adaptive control for resource-constrained distributed machine learning,” in IEEE IN-FOCOM 2018-IEEE Conference on Computer Communications. IEEE, 2018, pp. 63–71.   
[16] A. Li, L. Zhang, J. Tan, Y. Qin, J. Wang, and X.-Y. Li, “Samplelevel data selection for federated learning,” in IEEE INFOCOM 2021-IEEE Conference on Computer Communications. IEEE, 2021, pp. 1–10.   
[17] L. Zhang, Y. Li, X. Xiao, X.-Y. Li, J. Wang, A. Zhou, and Q. Li, “Crowdbuy: Privacy-friendly image dataset purchasing via crowdsourcing,” in IEEE INFOCOM 2018-IEEE Conference on Computer Communications. IEEE, 2018, pp. 2735–2743.   
[18] A. Li, L. Zhang, J. Qian, X. Xiao, X.-Y. Li, and Y. Xie, “Todqa: Efficient task-oriented data quality assessment,” in 2019 15th International Conference on Mobile Ad-Hoc and Sensor Networks (MSN). IEEE, 2019, pp. 81–88.   
[19] I. Loshchilov and F. Hutter, “Online batch selection for faster training of neural networks,” arXiv preprint arXiv:1511.06343, 2015.   
[20] C.-Y. Wu, R. Manmatha, A. J. Smola, and P. Krahenbuhl, “Sampling matters in deep embedding learning,” in Proceedings of the IEEE International Conference on Computer Vision, 2017, pp. 2840– 2848.   
[21] L. Pu, X. Chen, R. Yun, X. Yuan, P. Zhou, and J. Xu, “Cocktail: Cost-efficient and data skew-aware online in-network distributed machine learning for intelligent 5g and beyond,” arXiv preprint arXiv:2004.00799, 2020.   
[22] J. Byrd and Z. Lipton, “What is the effect of importance weighting in deep learning?” in International Conference on Machine Learning, 2019, pp. 872–881.   
[23] A. Raj, C. Musco, and L. Mackey, “Importance sampling via local sensitivity,” in International Conference on Artificial Intelligence and Statistics, 2020, pp. 3099–3109.

[24] Y. Zhao, M. Li, L. Lai, N. Suda, D. Civin, and V. Chandra, “Federated learning with non-iid data,” arXiv preprint arXiv:1806.00582, 2018.   
[25] J. Wang, L. Zhang, and H. Cheng, “Efficient participant contribution evaluation for horizontal and vertical federated learning,” in 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 2022, pp. 911–923.   
[26] H. Wang, Z. Kaplan, D. Niu, and B. Li, “Optimizing federated learning on non-iid data with reinforcement learning,” in IEEE IN-FOCOM 2020-IEEE Conference on Computer Communications. IEEE, 2020, pp. 1698–1707.   
[27] F. Lai, X. Zhu, H. V. Madhyastha, and M. Chowdhury, “Oort: Efficient federated learning via guided participant selection,” in 15th {USENIX} Symposium on Operating Systems Design and Implementation ({OSDI} 21), 2021, pp. 19–35.   
[28] A. Li, L. Zhang, J. Wang, F. Han, and X.-Y. Li, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, vol. 33, no. 10, pp. 2291–2303, 2021.   
[29] A. Li, Y. Cao, J. Guo, H. Peng, Q. Guo, and H. Yu, “Fedcss: Joint client-and-sample selection for hard sample-aware noise-robust federated learning,” Proceedings of the ACM on Management of Data, vol. 1, no. 3, pp. 1–24, 2023.   
[30] X. Li, R. Dowsley, and M. De Cock, “Privacy-preserving feature selection with secure multiparty computation,” ICML 2021, 2021.   
[31] Y. Yamada, O. Lindenbaum, S. Negahban, and Y. Kluger, “Feature selection using stochastic gates,” in International Conference on Machine Learning. PMLR, 2020, pp. 10 648–10 659.   
[32] J. Chen, M. Stern, and M. I. Jordan, “Kernel feature selection via conditional covariance minimization,” NeurIPS 2017, 2017.   
[33] D. Roy, K. S. R. Murty, and C. K. Mohan, “Feature selection using deep neural networks,” in 2015 International Joint Conference on Neural Networks (IJCNN). IEEE, 2015, pp. 1–6.   
[34] M. M. Kabir, M. M. Islam, and K. Murase, “A new wrapper feature selection approach using neural network,” Neurocomputing, vol. 73, no. 16-18, pp. 3273–3283, 2010.   
[35] Y. Li, C.-Y. Chen, and W. W. Wasserman, “Deep feature selection: theory and application to identify enhancers and promoters,” Journal of Computational Biology, vol. 23, no. 5, pp. 322–336, 2016.   
[36] M. Hu, Y. Cao, A. Li, Z. Li, C. Liu, T. Li, M. Chen, and Y. Liu, “Fedmut: Generalized federated learning via stochastic mutation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 38, no. 11, 2024, pp. 12 528–12 537.   
[37] A. Li, H. Peng, L. Zhang, J. Huang, Q. Guo, H. Yu, and Y. Liu, “Fedsdg-fs: Efficient and secure feature selection for vertical federated learning,” arXiv preprint arXiv:2302.10417, 2023.   
[38] A. Li, J. Huang, J. Jia, H. Peng, L. Zhang, L. A. Tuan, H. Yu, and X.-Y. Li, “Efficient and privacy-preserving feature importancebased vertical federated learning,” IEEE Transactions on Mobile Computing, no. 01, pp. 1–17, 2023.   
[39] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” semanticscholar, 2009.   
[40] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.   
[41] I. Guyon, S. Gunn, A. Ben-Hur, and G. Dror, “Result analysis of the nips 2003 feature selection challenge,” Advances in neural information processing systems, vol. 17, 2004.   
[42] “Iris,” https://archive.ics.uci.edu/ml/datasets/iris.   
[43] Y. Zhang and H. Zhu, “Additively homomorphical encryption based deep neural network for asymmetrically collaborative machine learning,” arXiv preprint arXiv:2007.06849, 2020.   
[44] J. Luo, X. Wu, Y. Luo, Y. Huang, Y. Liu, and Q. Yang, “Real-world image datasets for federated learning,” arXiv:1910.11089, 2019.   
[45] Y. Cheng, L. Zhang, and A. Li, “Gfl: Federated learning on noniid data via privacy-preserving synthetic data,” in 2023 IEEE International Conference on Pervasive Computing and Communications (PerCom). IEEE, 2023, pp. 61–70.   
[46] S. P. Karimireddy, S. Kale, M. Mohri, S. J. Reddi, S. U. Stich, and A. T. Suresh, “Scaffold: Stochastic controlled averaging for federated learning,” arXiv preprint arXiv:1910.06378, 2019.   
[47] T. Wu, L. Chen, P. Hui, C. J. Zhang, and W. Li, “Hear the whole story: Towards the diversity of opinion in crowdsourcing markets,” Proceedings of the VLDB Endowment, vol. 8, no. 5, pp. 485–496, 2015.

[48] G. Alain, A. Lamb, C. Sankar, A. Courville, and Y. Bengio, “Variance reduction in sgd by distributed importance sampling,” arXiv: Machine Learning, 2015.   
[49] T. Schaul, J. Quan, I. Antonoglou, and D. Silver, “Prioritized experience replay,” arXiv preprint arXiv:1511.05952, 2015.   
[50] O. Li, J. Sun, X. Yang, W. Gao, H. Zhang, J. Xie, V. Smith, and C. Wang, “Label leakage and protection in two-party split learning,” arXiv preprint arXiv:2102.08504, 2021.   
[51] “Federatedai/fate,” https://github.com/FederatedAI/FATE, 2021.   
[52] R. Agrawal, A. Evfimievski, and R. Srikant, “Information sharing across private databases,” in Proceedings of the 2003 ACM SIGMOD international conference on Management of data, 2003, pp. 86–97.   
[53] J. Yuan and S. Yu, “Privacy preserving back-propagation neural network learning made practical with cloud computing,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 1, pp. 212–221, 2014.   
[54] T. Wu, L. Chen, P. Hui, C. Jason, and Z. W. Li, “Hear the whole story: Towards the diversity of opinion in crowdsourcing markets.”   
[55] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” arXiv preprint arXiv:1409.1556, 2014.   
[56] C. Biswas, D. Ganguly, D. Roy, and U. Bhattacharya, “Privacy preserving approximate k-means clustering,” in Proceedings of the 28th ACM International Conference on Information and Knowledge Management, ser. CIKM ’19. Association for Computing Machinery, 2019, p. 1321–1330.   
[57] L. Jacques, J. N. Laska, P. T. Boufounos, and R. G. Baraniuk, “Robust 1-bit compressive sensing via binary stable embeddings of sparse vectors,” IEEE Transactions on Information Theory, vol. 59, no. 4, pp. 2082–2102, 2013.   
[58] L. Erlingsson, V. Pihur, and A. Korolova, “Rappor: Randomized aggregatable privacy-preserving ordinal response,” 2014.   
[59] A. Kulesza and B. Taskar, Determinantal Point Processes for Machine Learning. IEEE, 2012.   
[60] Z. Erkin, M. Franz, J. Guajardo, S. Katzenbeisser, I. Lagendijk, and T. Toft, “Privacy-preserving face recognition,” in International symposium on privacy enhancing technologies symposium. Springer, 2009, pp. 235–253.   
[61] “The mnist database of handwritten digits,” http://yann.lecun. com/exdb/mnist/.   
[62] J. H. Friedman, “Multivariate adaptive regression splines,” The annals of statistics, vol. 19, no. 1, pp. 1–67, 1991.   
[63] A. Tsanas, M. A. Little, C. Fox, and L. O. Ramig, “Objective automatic assessment of rehabilitative speech treatment in parkinson’s disease,” IEEE Transactions on Neural Systems and Rehabilitation Engineering, vol. 22, no. 1, pp. 181–190, 2013.   
[64] R. Fisman, S. S. Iyengar, E. Kamenica, and I. Simonson, “Gender differences in mate selection: Evidence from a speed dating experiment,” The Quarterly Journal of Economics, vol. 121, no. 2, pp. 673–697, 2006.   
[65] “Arcene,” https://archive.ics.uci.edu/ml/datasets/Arcene.   
[66] Y. LeCun, L. Bottou, Y. Bengio, P. Haffner et al., “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.   
[67] S. Hardy, W. Henecka, H. Ivey-Law, R. Nock, G. Patrini, G. Smith, and B. Thorne, “Private federated learning on vertically partitioned data via entity resolution and additively homomorphic encryption,” arXiv preprint arXiv:1711.10677, 2017.   
[68] Flower, “Flower: A friendly federated learning framework,” Public online, 2022. [Online]. Available: https://flower.dev/

![](images/3cc0870d97c8c56c1459583bff4e4928ca47342d36b7141c545a90992d6920da.jpg)



Lan Zhang is currently a Professor at the School of Computer Science and Technology, University of Science and Technology of China. She received her Ph.D degree and Bachelor degree from Tsinghua University, China. Her research interests include mobile computing, privacy protection, and data sharing and trading.

![](images/38723d11862b9102e35052e222108f280e2564088f823d661a59a29b799faf0e.jpg)



Anran Li is a Postdoctoral Associate at the Department of Biomedical Informatics & Data Science, School of Medicine at Yale University. She received her Ph.D. degree from the School of Computer Science and Technology, University of Science and Technology of China, China. Her research interests mainly focus on data quality assessment, federated learning and medical large language models.

![](images/ca5f89029c7a33c9518da857f249c59e115eb49f18c8e4dbb5ca8fcd9fad0182.jpg)



Hongyi Peng is a Ph.D. candidate of Alibaba Talent Programme in the School of Computer Science and Engineering, Nayang Technological University, Singapore. He received his Bachelor of Engineering degree from Nanyang Technological University in 2019 and Master of Science degree from the National University of Singapore in 2020. His research interests include federated learning and data analysis.

![](images/469bec437c0a9ec3540a34e2f94dea073634f013097f09b588ef3d354592c01c.jpg)



Feng Han received his Ph.D. degree in Computer Science at University of Science and Technology of China. He received his Bachelor degree in Information Security from University of Science and Technology of China, in 2017. His research interests include privacy and security issues in data analysis.

![](images/f3bebaa8f154be7dcde6093c83ceaeaf58fe7e391eabbbc9565f14206d8bf045.jpg)



Fan Huang is now a researcher in Tencent, Shanghai, China. His research interests include federated learning, deep learning, recommender systems and etc. Before joining Tencent, he recieved Bachelor degree in Software Engineering from Beihang University in 2018, and Master of Software Engineering degree from Tsinghua University in 2021.

![](images/bdc9b4c313e854bba9d8bd8ac71bd64da89bc69aa75bdb090eb7574eaafe3907.jpg)



Xiang-Yang Li is currently a Full Professor and the Executive Dean of the School of Computer Science and Technology, University of Science and Technology of China, Hefei, China. He is an IEEE/ACM Fellow. He received the bachelor degree from the Department of Computer Science, the bachelor degree from the Department of Business Management, Tsinghua University, in 1995, and the Ph.D. degree from the University of Illinois at Urbana–Champaign. His research interests include wireless network-

ing/mobile computing/RFID, privacy and security, cyber-physical systems and IoT, social computing, and interdisciplinary research.