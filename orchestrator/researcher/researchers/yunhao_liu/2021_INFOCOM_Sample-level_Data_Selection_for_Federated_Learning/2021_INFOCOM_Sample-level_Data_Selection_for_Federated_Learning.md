# Sample-level Data Selection for Federated Learning

Anran Li, Lan Zhang, Juntao Tan, Yaxuan Qin, Junhao Wang, Xiang-Yang Li

School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

Abstract—Federated learning (FL) enables participants to collaboratively construct a global machine learning model without sharing their local training data to the remote server. In FL systems, the selection of training samples has a significant impact on model performances, e.g., selecting participants whose datasets have erroneous samples, skewed categorical distributions, and low content diversity would result in low accuracy and unstable models. In this work, we aim to solve the exigent optimization problem that selects a collection of high-quality training samples for a given FL task under a monetary budget in a privacypreserving way, which is extremely challenging without visibility to participants’ local data and training process. We provide a systematic analysis of important data related factors affecting the model performance and propose a holistic design to privately and efficiently select high-quality data samples considering all these factors. We verify the merits of our proposed solution with extensive experiments on a real AIoT system with 50 clients, including 20 edge computers, 20 laptops, and 10 desktops. The experimental results validates that our solution achieves accurate and efficient selection of high-quality data samples, and consequently an FL model with a faster convergence speed and higher accuracy than that achieved by existing solutions.

# I. INTRODUCTION

How to get large enough high-quality datasets has become a common bottleneck of many machine learning models and AI applications. It is not only because collecting and labelling massive samples are very expensive, but also because the privacy concerns hindering data sharing in many areas, e.g., medicine and economics. FL enables multiple local sites to collaboratively train a machine learning model by iteratively exchanging model parameters between participants and a centralized server, meanwhile keeping their datasets private. For example, using FL, three hospitals can collaboratively build a deep learning model for analyzing tumor images while preserving the privacy of their patients. A series of previous efforts have been devoted to designing FL algorithms for diverse scenarios [1]–[4]. Besides the algorithm itself, the composition of training dataset also has a significant impact on the performance of an FL model. As we will show by the datadriven analysis in Section II, incorrect labels, unrepresentative samples, skewed categorical distributions, and low content diversity can all lead to severe model accuracy deterioration, unfortunately, which is very likely to happen in real FL systems.

Related work. There are a number of data selection methods proposed for centralized learning [5]–[11], while few work deal with the data selection problem for FL [12], [13]. Data selection methods for centralized learning can be divided into two branches. One branch [5], [6] focuses on proposing various quality dimensions, e.g., task relevancy and content diversity, and directly measure the quality of data samples to make selections. The other branch [7], [9]–[11] dynamically selects samples with greater importance to the model to compose training batches during the training process, in order to accelerate model convergence. The importance is usually quantified by the gradient norm or the loss of training samples [14], [15]. Those methods, however, cannot be directly applied to FL systems for the reasons that they require access to all training samples, which violates the privacy of participants in FL systems. Besides, directly calculating importance for each sample would cause unacceptable cost for participants with limited resources. Moreover, those methods cannot cope with the Non-IID problem [16], [17] or erroneous samples, and are very likely to give higher priority to erroneous samples, which usually have larger importance values (see Fig. 2(a)). As for data selection for FL, the most relevant work [12] proposes a method to distributedly select relevant data before training based on a benchmark model, without considering other data quality factors or the batch composition during training. Therefore, in FL scenarios, facing multiple private datasets belonging to different owners, how to select an optimal collection of training samples for a given FL task without accessing to participants’ local data and training process is an extremely exigent and challenging problem.

In this work, we consider a typical FL system, a server aims to train a target deep learning model with a given monetary budget. There are a collection of data owners, each of which possesses a number of labelled samples and is willing to participate in some FL tasks for a certain price. Our goal is to select a set of high-quality samples for the target task and pay their owners to participate in the model training under the budget in a privacy-preserving way. To this end, we need to address several critical challenges including:

1) How to privately measure samples’ quality and impacts on the global model, before and during training? We aim to select high-quality samples which have large positive influences on the global model. Hence we need to comprehensively and accurately quantify samples’ quality features that are relevant to the model performance, without accessing any local samples. We also need to quantify samples’ influences or importance on the model without accessing any local samples and training process. Such influences can only be obtained during the training, which further increases the difficulty.

2) How to achieve optimal selection considering multiple quality dimensions and the budget constraint, and how to dynamically select more important samples during training? Facing multiple quality dimensions, we need to select an optimal budget feasible collection of samples which is most likely to produce a model with high accuracy. It is nontrivial to solve this optimization that requires a good balance between different quality dimensions. During training, different training batch selection strategies lead to different model performances (see Section II-C), so an efficient importance aware batch selection method is also required. Specially, we consider a more realistic case that there are erroneous samples (e.g., samples with incorrect labels), which usually have large importance values, therefore we also need to carefully filter out erroneous samples in a privacy-preserving manner.

3) How to provide better privacy protection for both participants and the sever, and how to efficiently reduce the cost for data selection? In this work, for the participants, we try to protect not only the privacy of their local data, but also their local data distributions. Specially, we treat the target task of the server as a secret to irrelevant clients. The target task is usually considered as a public information in existing work, however, which may expose the interest or business plan of the server. Protecting the target task makes the client and data selection more challenging. Last but not least, participants in FL systems usually have limited resources [18], [19], which motivates us to reduce as much as possible computation and communication cost for quality measurement and data selection.

By addressing these challenges, our work makes the following main contributions:

• To the best of our knowledge, this is the first work presenting a systematical analysis of a series of main factors that influence the model performance in FL systems from the perspective of data, and addressing the training sample selection for an FL task considering all these factors, including samples’ categorical statistical homogeneity, content-level diversity, influences on the global model, and erroneous labels. We propose a holistic design to efficiently select high-quality samples while ensuring not only participants’ data privacy but also the server’s task privacy.

• We propose an efficient hierarchical sample selection mechanism, which selects first optimal clients and then their high quality samples. Before training, we use a private set intersection (PSI) based scheme to filter clients relevant to the target FL task. We design a homomorphic encryption (HE) based method to measure each client’s statistical homogeneity, and a data sketch and randomized response based method to estimate the content diversity of selected clients, which significantly reduces the cost. We solve the optimization to maximize both statistical homogeneity and content diversity of selected clients under the budget using a determinantal point process (DPP) based algorithm. During training, an erroneous-aware importance-based selection method is proposed to dynamically select important clients and samples for each iteration to accelerate model convergence.

• We evaluate our design via extensive experiments using two popular datasets on a real AIoT system with 50 clients. The experimental results demonstrate that when there are low-quality clients with statistical heterogeneous and lowdiversity data, training FL models with clients selected by our method reduces the average false rate for digit recognition

on MNIST from 16.73% to 8.5%, and for image recognition on CIFAR from 34.8% to 18.91%. Meanwhile, our sample selection method outperforms existing methods in terms of faster model convergence rate, higher accuracy and lower cost. When compared to three data selection methods for centralized training, for digit recognition on MNIST, our method saves 48.1%, 19.6%, 64.6% computation cost, and 50.3%, 20.5%, 66.8% communication cost; for image recognition on CIFAR, our method saves 38.0%, 17.6%, 55.3% computation cost, and 37.5%, 16.7%, 54.5% communication cost.

The rest of this paper is organized as follows. In Section II, we describe the problem and present our data driven analysis. The overview of our system is in Section III. Section IV and Section V give the detailed design of client selection and data sample selection. Comprehensive evaluations are introduced in Section VI. We conclude this work in Section VII.

# II. PROBLEM DEFINITION & DATA DRIVEN ANALYSIS

# A. Problem Definitions

A typical FL scenario involves two types of entities: a server S and N clients $\{ \mathcal { C } _ { 1 } , \mathcal { C } _ { 2 } , \cdots , \mathcal { C } _ { N } \}$ . Each client $\mathcal { C } _ { k }$ possesses a local dataset $\mathcal { D } _ { k }$ and is willing to participate in some FL tasks for a price $b _ { k }$ , which could be money or credits. The server aims to coordinate clients to accomplish a given FL task for a as high accuracy as possible within a monetary or credit budget B. Due to the limited budget and some clients having poor-quality samples (with erroneous labels, skewed categorical distribution, or unacceptably low content diversity) or irrelevant data to this task, the server needs to select an optimal collection of samples from N clients for the model training. Taking a classification FL model as an example, an ideal client should have sufficient correctly labelled training data for all target categories, and for each category training samples should be statistically representative. The selected clients collaboratively train the target FL model using selected local samples and get their payments. We assume that all participants including the server are semi-honest, i.e., they follow the exact protocols of sample selection and FL but may be curious about others data.

# B. Design Goals

We design our system to achieve the following goals.

• Effectiveness: Given candidate samples from N clients, the selected collection of samples should produce a global FL model with higher accuracy and faster convergence speed than that trained with any other sample collections within the given budget B.

• Privacy protection: Our method should preserve privacy of clients’ local data and the server’s target task. The target task is very likely to reveal the secret of the task requester. As an example, a task to detect objects on roads implies that the company may start an automatic driving business. For each client, the local samples and their distributions should never be exposed to any other party, including the server. For the server, the target task should never be exposed to any irrelevant party who wasn’t selected for the FL task.

![](images/ff53d21b65c8ca92fd7dc46f617a235bc36d8147dfa11a08a6b5cb017c42c71d.jpg)



(a) Accuracy v.s. mislabeling ratio.

![](images/b64c47109a8e0c161ec17750d6f0a5636a455656b79707ca3e09bc0188fd5be4.jpg)



(b) Statistically heterogeneous data.

![](images/c5112b9a49e0f4924b12a2edc543c5a02487b71f0dedd269bce0e8368b309f16.jpg)



(c) Statistically heterogeneous data.

![](images/d5ba1ee8e9e3f535895d267a3d1b22fb52c9833d9fa14252381f432fc230e497.jpg)



(d) Different content diversity.

Fig. 1. Test accuracy of a residual network trained using CIFAR10 in different settings: (a) There are different proportions of erroneous data; (b) Each client has k random categories out of 10 categories; (c) Distribution of the training data is imbalanced between the first five categories and the last five categories; (d) The training data has different content diversity.   
![](images/3c1493bc91f759e505721cebd90d3748dbeb82f7e19af07e5689477de4f4dc15.jpg)



(a) Different selection strategies.

![](images/7e7029d60ed73fadb306b7167e8d20da6ae0749e649ba57dd31b9d9c2fd2f93d.jpg)



(b) Gradient norm updates of samples   
Fig. 2. Effect of sampling strategies: (a) Test accuracy of a residual network trained using CIFAR10 with different batch selection strategies; (b) Gradient norm updates of samples during FL training, here Sample 0 is an erroneous sample, Sample 1-3 are correct samples.

• Efficient Selection: Considering the restricted resources of local edges and mobile devices, the selection process should incur low extra computation and communication cost.

# C. Data Driven Analysis and Observations

Towards above goals, we conduct data driven analysis to explore the principles for selecting training samples in FL scenarios. We used the well-known image datasets CIFAR10 [20] as training data, which contains 50,000 images from 10 categories. We employed 10 clients to train a residual network [21] using a typical federated optimization algorithm FedSGD [1]. We divided the dataset into 100 shards of size 500, and assigned them to 10 clients (10 shards per client). The learning rate $\eta = 0 . 0 1$ , batch size $g = 1 0 ,$ , local epoch $E = 1 0$ . We tested accuracy of the global model on the hold-out test dataset of CIFAR10. Different from conventional FL systems, which usually treat each client and each sample equally, we vary the settings to answer the following questions.

1) How does each sample affect the model training? A series of previous work [7], [11] have shown that, in a large training dataset, there are usually a portion of unrepresentative samples making negligible contributions to the model convergence, which actually incur unnecessary computation cost for training. Some poor-quality or erroneous samples even have negative influences on the model training [22]. To demonstrate such negative influences, we manually created some erroneous samples in the training dataset by replacing their original labels with random labels from other categories. Let $r _ { m }$ be the ratio of mislabeled samples in all training samples. We randomly selected $r _ { m } \cdot 5 0$ , 000 samples equally from all clients or randomly from no more than 9 clients. Fig. 1(a) shows that the test accuracy of the global model decreases significantly as the ratio of mislabeled samples increases.

• Principle #1: The sample selection should prioritize representative samples and avoid erroneous ones.   
2) How does the categorical distribution of training data affect the model training? When the local training data is evenly distributed across all categories, we refer to it as a statistically homogeneous (or IID) setting, otherwise a statistically heterogeneous (or Non-IID) setting [16], [17], [23], [24]. The statistically heterogeneous training data with severe imbalance distributions among categories will result in low accuracy and unstable convergence. In Fig. 1(b), Non-IID (k) $( 1 ~ \leq ~ k ~ \leq ~ 1 0 )$ indicates that each client has samples from k random categories out of all ten categories. Even in the case Non-IID (8), there is still a huge accuracy loss compared with that in the IID setting. In Fig.1(c), although each client has samples from all categories, the number of samples in the first five categories is much lower than that in the last five categories. Both Fig. 1(b) and Fig.1(c) illustrate that the model performance obviously deteriorates as the imbalance degree increases.   
• Principle #2: The sample selection should prioritize clients whose data distributions are closer to the homogeneous distribution and avoid clients with missing categories.   
3) How does the content diversity of training samples affect the model training? We further look into the fact that even in the statistically homogeneous setting the content diversity of training samples has a non-negligible effect on the model. We randomly removed 30% (or 50%) samples from the original dataset and added the same amount of “new” samples, which were created by rotating the remaining samples by random angles smaller than 30 degree, to compose a dataset with a lower content diversity. In Fig. 1(d), although the categorical distributions of three datasets are almost identical, the decrease of content diversity leads to obvious accuracy loss.   
• Principle #3: The sample selection should try to maximize the content-level diversity of the selected training dataset.   
4) How does the batch sampling strategy affect the model training? Given the distribution of training data, using different strategies to sample training batches for local epochs will result in drastically different performances of FL models

[11]. We tried three typical sampling strategies in both clean data and noisy data settings: i) random sampling strategy, ii) gradient norm based importance sampling, and iii) loss based importance sampling. Random sampling strategy is widely used for FL. The last two importance sampling strategies are proposed for centralized learning [7], [9], here we extended them to FL scenarios. Fig. 2(a) presents that, in the clean data setting, different sampling strategies result in different convergence speeds and accuracy, and the loss based importance sampling is superior than the other two. In the noisy data setting, where 30% clients have 30% mislabeled samples, random sampling has better resistance to erroneous data, while both importance sampling strategies suffer from highly unstable training process and lower accuracy. The reason is that, erroneous samples have obviously larger losses and gradient norms than correct ones (Fig. 2(b)), therefore existing importance sampling strategies tend to select erroneous samples with higher probabilities.

• Principle #4: During training, a good sampling strategy should prioritize samples of greater importance but avoid erroneous samples which usually have abnormally large importance.

Given the same candidate training dataset, these observations reveal how sample selection dramatically changes the performance of FL, which motivates us to design an effective and privacy-preserving sample selection strategy for FL.

# III. MAIN IDEA AND SYSTEM OVERVIEW

# A. Main Idea

Following principles in Section II, we divide the data selection into two stages:

1) Before Training: The server selects an optimal collection of relevant clients (who possess data of the target categories) within the budget B to participate in the training, by prioritizing clients with higher category-level statistical homogeneity and content-level diversity, in a privacy preserving way.

Definition 1 (Statistical Homogeneity): Let Y be the set of target categories. Client $\mathcal { C } _ { k }$ has a dataset $\mathcal { D } _ { k } = \{ ( x _ { k } , y _ { k } ) \}$ , where each data $x _ { k }$ has a label $y _ { k } . ~ { \mathcal { D } } _ { k }$ follows a categorical distribution $q _ { k }$ . The uniform categorical distribution over  is $q _ { u } .$ . The statistical homogeneity of $\mathcal { D } _ { k }$ is defined as [17],

$$
\mu_ {k} = 2 - \sqrt {\sum_ {y \in \mathcal {Y}} | q _ {k} (y _ {k} = y) - q _ {u} (y _ {u} = y) | ^ {2}}, \tag {1}
$$

which measures the similarity between distributions $q _ { k }$ and $q _ { u }$ over Y.

A larger homogeneity will result in better model performance according to Principle #2.

Definition 2 (Content Diversity): Given a dataset D having M samples or M sub-collections of samples, let $v _ { i }$ be the content embedding vector of the i-th sample or i-th subcollection of samples. The similarity function of two vectors is $S ( v _ { i } , v _ { j } )$ . The content diversity of D is defined as [25],

$$
\rho (\mathcal {D}) = 1 - \frac {\sum_ {i , j \in [ M ] , i \neq j} 2 S (v _ {i} , v _ {j})}{M (M - 1)}, \tag {2}
$$

A dataset with larger content diversity will result in better model performance according to Principle #3.

In this stage, to solve the optimization that simultaneously maximizes the statistical homogeneity and content diversity of the selected clients under the budget, we model this problem as a determinantal point process (DPP). To protect the data and distribution privacy of all clients, we design an efficient privacy-preserving computation protocol based on homomorphic encryption, binary JL-transformation based data sketch, and randomized response.

2) During Training: The server dynamically selects collections of samples from selected clients to compose training batches for each epoch by prioritizing error-free important samples. According to Principle #1 and #4, we firstly need a proper metric to accurately estimate the importance/impact of each local sample to the global model, and then design an efficient strategy to select important correct samples and filter out erroneous ones that usually have abnormally large importance. In the whole process, for privacy of clients, we cannot access any local sample.

To measure the importance of training samples, some methods have been proposed for centralized scenarios, which use the gradient norm, the gradient’s upper bound norm or the loss of a sample as metrics of importance [7]–[10]. Those methods, however, cannot be directly applied to FL systems for the reasons that the server requires access to all training samples. In FL systems, both local data and local training process are invisible to any other parties including the server. In addition, those methods neglect the impact of erroneous samples and are very likely to give higher priority to erroneous samples than correct ones (see Fig. 2(a)).

Here, we take a classification task as an example, which is defined over a compact space  and a label space . There are N clients, each client $\mathcal { C } _ { k }$ has a local dataset $\mathcal { D } _ { k } =$ $\{ z _ { k , 1 } , z _ { k , 2 } , \cdot \cdot \cdot , z _ { k , n _ { k } } \}$ , where $z _ { k , i } ~ = ~ ( x _ { k , i } , y _ { k , i } ) ~ \in ~ \mathcal { X } \times \mathcal { Y }$

1 following the categorical distribution $q _ { k } . \ U _ { k }$ is the set of indices of samples in $\begin{array} { r } { \mathcal { D } _ { k } . \ : n = \sum _ { k = 1 } ^ { N } n _ { k } } \end{array}$ is the total number of all clients’ samples. Functions $f _ { k } , F _ { k }$ represent loss functions of an individual sample on $\mathcal { C } _ { k } \mathrm { { ^ { 2 } s } }$ local model, and all samples on client $\mathcal { C } _ { k } { } ^ { \mathrm { ~ \tiny ~ \backslash ~ } } \mathrm { ~ s ~ }$ local model,  represents loss function of the global model.The goal of a standard federated optimization problem is to find

$$
\theta^ {*} = \arg \min _ {\theta \in \Theta} \left\{\mathcal {F} (z; \theta) := \sum_ {k = 1} ^ {N} \frac {n _ {k}}{n} F _ {k} (\theta) \right\}, \tag {3}
$$

$$
\text { where } F _ {k} (\theta) = \frac {1}{n _ {k}} \sum_ {i \in U _ {k}} f _ {k} (z _ {k, i}; \theta)).
$$

This problem is solved via iterative stochastic optimization. In the t-th iteration, the server selects a subset of clients and distributes the current model parameters $\theta _ { t }$ to them. Each selected client $\mathcal { C } _ { k }$ independently computes a local update $\theta _ { t + 1 } ^ { k } ~ = ~ \theta _ { t } ^ { k } - \eta \nabla F _ { k } ( \bar { \theta _ { t } } )$ with learning rate $\eta ,$ and sends

1In real FL systems, a client $\mathcal { C } _ { k }$ is very likely to possess samples that don’t belong to any target categories, $i . e . , \exists ( x _ { k , i } , y _ { k , i } ) , y _ { k , i } \notin \mathcal { V }$ . We will deal with this in Section IV-A.

$\eta \nabla F _ { k } ( \theta _ { t } )$ to the server. The server aggregates the updates from all selected clients and conducts the update $\theta _ { t + 1 } =$ $\theta _ { t } - \eta \nabla \mathcal { F } ( z ; \theta _ { t } )$ . This process is iterated until the global model converged to ✓⇤, e.g., meeting a convergence criterion.

To measure the importance of local training samples on the global model in each iteration, inspired by previous work in centralized scenarios [7], we use gradient upper bound norms as an importance metric. Different to those conventional methods, the gradient here is not the one of the loss with respect to the model parameter $\sqrt { | \nabla _ { \theta _ { t } } \mathcal { F } ( z _ { k , i } , \theta _ { t } ) | ^ { 2 } }$ , but is its upper bound, the loss with respect to the pre-activation outputs of the last layer. Using upper bound norms is to reduce computation cost, because computing the conventional norm needs one forward and one backward pass through the network, while its upper bound only needs one forward, which still achieves sufficiently accurate estimations of samples’ importance but has lower cost than that of the backward. Here we give how to estimate the importance of a sample $z _ { k , i }$ based on the global model in the t-th iteration. $\theta ^ { l } \in R ^ { \bar { m _ { l } } \times m _ { l - 1 } }$ is the weight matrix for layer $l , m _ { l }$ is the number of neural nodes of the l-th layer (in total L layers);   is a Lipschitz continuous activation function, and $\beta ^ { 0 } \stackrel { \cdot } { = } x , \alpha ^ { l } = \theta ^ { l } ( \beta ^ { \bar { l } - 1 } ) , \beta ^ { l } = \sigma ^ { l } ( \alpha ^ { l } )$ .

Definition 3 (Sample Importance for FL): The importance of a client $\mathcal { C } _ { k } \mathrm { ~ } ^ { \prime } s$ sample $z _ { k , \mathrm { i } }$ i to the global model in the t-th iteration is

$$
\lambda (z _ {k, i}, t) = \sqrt {\left| \sum_ {t , L} \beta_ {k , i} ^ {t , L} \nabla_ {\alpha_ {k , i} ^ {t , L}} \mathcal {F} (z _ {k , i} ; \theta_ {t}) \right| ^ {2}}, \tag {4}
$$

where $\beta _ { k , i } ^ { t , L } , \alpha _ { k , i } ^ { t , L }$ are the input and output of the last layer (L-th) of sample $z _ { k , i }$ in the t-th iteration, respectively, $\begin{array} { r c l } { { \sum _ { t , L } \beta ^ { L } } } & { { = } } & { { d i a g ( \sigma ^ { \prime L } ( \beta _ { 1 } ) , \cdots , \sigma ^ { \prime L } ( \beta _ { m _ { L } } ) ) , | \bar { \sigma ^ { \prime } } ( \beta ) | } } \end{array} \overset { < } { \leq }$ $\begin{array} { r } { \lambda , \mathcal { F } ( z ; \theta ) : = \sum _ { k = 1 } ^ { N } \frac { n _ { k } } { n } F _ { k } ( \theta ) } \end{array}$

That is, the sample with larger gradient upper bound norm of the global loss with respect to the pre-activation outputs will have greater importance. However, as shown in Section II-C and Fig. 2(b), erroneous samples have significantly greater importance values than correct samples. Therefore, a client $\mathcal { C } _ { k }$ should avoid selecting samples whose importance values are outliers among that of majority samples. For example, in our experiment, we require $\lambda ( z _ { k , i } , t ) \le \delta _ { k } ^ { t }$ (e.g., the median gradient norm of samples), where $\delta _ { k } ^ { t } = 2 0 0 . 0$ in the CIFAR10 experiment. Specially, we notice that the importance metric has an additive property, hence the importance of a client can be measured by the summation of his/her samples’ importance.

Definition 4 (Client Importance for FL): The importance of a client $\mathcal { C } _ { k }$ with dataset $\mathcal { D } _ { k }$ to the global model in the t-th iteration is

$$
\lambda (\mathcal {D} _ {k}, t) = \sum_ {i \in U _ {k}} \lambda (z _ {k, i}, t). \tag {5}
$$

After obtaining the importance of samples and filtering out erroneous ones, we can select samples by their importance for the next iteration. Let pt+1 , · $p _ { k , 1 } ^ { t + 1 } , \cdot \cdot \cdot , \stackrel { \cdot } { p _ { k , n _ { k } } ^ { t + 1 } }$ , pk,n be the data sampling probability distribution of client $\mathcal { C } _ { k }$ in the (t + 1)-th iteration, $\overline { { p } } _ { k , i } ^ { t + 1 } \ \propto \ \dot { \lambda } ( z _ { k , i } , t )$ p k,i . Similarly, we can also select clients by

![](images/f44448c8a71050834f00086198f5f659d5274ca18d06b12312998c2c35e968c5.jpg)



Fig. 3. System overview.

their importance, that is the probability to select a client $\mathcal { C } _ { k }$ is $P _ { k } ^ { t + 1 } \propto \bar { \lambda } ( \mathcal { D } _ { k } , t )$ .

This additive property of importance enlightens us to design a hierarchical sample selection strategy during training, which selects important clients first to save a large portion of cost for sample-level importance analysis, then selects training samples only from selected clients.

# B. Design Overview

As shown in Fig. 3, here we present the overview of our two stage (before and during training) and hierarchical (first clients then samples) data selection framework for FL.

1) Filter relevant clients: When an FL task arrives, the server first needs to filter clients who possess data of the target categories by computing the intersection of each client’s label set and the target label set. If the number of samples in the intersection set exceeds a minimum number for the target model, then the client is relevant. To meet the privacy goal in Section II-B, we apply a private set intersection (PSI) method for client filtering (Section IV-A).   
2) Client selection before training: From relevant clients, the server further privately selects high-quality clients to maximize statistical homogeneity and content diversity under the budget constraint using the DPP based algorithm (Section IV-B). Then the sever coordinates selected clients to start the training.   
3) Dynamical client selection and sample selection: During the training, for each iteration $t , t \in [ T ]$ , the server selects a subset of most important clients and then selects their important samples to compose their training batches. To save cost, instead of computing importance values of all samples for all clients, we propose a simple but effective method for the server to measure each client’s importance using the training updates $\theta _ { t - 1 } ^ { k } , k \ \in \ [ N ]$ on the server. A client $\mathcal { C } _ { k }$ whose local model has larger deviation from the global model $\theta _ { t - 1 } , i . e .$ , larger $| \theta _ { t - 1 } ^ { k } - \theta _ { t - 1 } |$ , has larger contribution, hence are more likely to be selected in this iteration. The selected clients locally select training samples using the erroneousaware importance-based selection algorithm (Section V).   
4) Model training: In each iteration, all selected clients train their local models on the selected samples, and the server aggregates clients’ updates to get the global update. The server repeats the process until achieving the optimal global model $\theta ^ { * }$ .

# IV. CLIENT SELECTION

In this section, we present the detailed design of privacypreserving client selection before training, including how to filter clients relevant to the target task, and how to privately select clients to maximize statistical homogeneity and content diversity within the budget using the DPP based algorithm.

# A. Filter Relevant Clients and Samples

Let the target FL task have a label set . The FL system has N candidate clients, and each client $\mathcal { C } _ { k }$ possess a dataset $\mathcal { D } _ { k }$ . The label set of $\mathcal { D } _ { k }$ is $\mathcal { V } _ { k } = \{ y _ { k } \vert ( x _ { k } , y _ { k } ) \in \mathcal { D } _ { k } \}$ . To perform this task, the server first filters relevant clients. A relevant client $\mathcal { C } _ { k }$ should satisfy $| \{ ( x _ { k } , y _ { k } ) | y _ { k } \in \mathcal { V } _ { k } \cap \mathcal { V } \} | > \nu .$ where $\nu$ is the required minimum number of training samples for the target model (e.g., 1, 000). Samples belonging to the categories in the intersection set are relevant to the task. To protect the client’s privacy ${ \mathcal { V } } _ { k }$ and the server’s privacy Y, we leverage a widely adopted PSI protocol [26] to allow server and clients to compute $y _ { k } \cap \mathcal { V }$ privately. Then each client only reports 1 bit information, $i . e .$ , whether or not he/she is relevant, to the server. The server and each client learn the labels in their intersection set and server also learns which client has more than ⌫ relevant samples. They learn nothing else from this process. Any other party learns nothing at all.

# B. Client Selection

Given relevant clients whose index set is $[ N ^ { \prime } ] \subset [ N ]$ , each client posts a price $b _ { k }$ for this task. The server needs to select a set of high-quality clients within the budget B. Let $\mathcal { Q }$ be the set of indices of selected clients, we aims to solve the optimization problem

$$
\max V (\mathcal {Q}), \text {   s.t.,   } \sum_ {k \in \mathcal {Q}, \mathcal {Q} \subseteq [ N ^ {\prime} ]} b _ {k} \leq B. \tag {6}
$$

Here, $V ( { \mathcal { Q } } )$ is the quality value of the selected clients. According the principles in Section II-C, we consider two quality metrics of clients, statistical homogeneity and content diversity. In the rest of this subsection, we first introduce how to select clients according to two metrics respectively, and then how to adopt two metrics simultaneously.

1) Homogeneity-aware Client Selection: Taking statistical homogeneity as the quality metric of a client, we have $V _ { \mu } ( \mathcal { Q } ) \ = \ \Sigma _ { k \in \mathcal { Q } } \mu _ { k }$ . To solve $\mathrm { E q . 6 , }$ the server first needs to calculate $\mu _ { k } , k \ \in \ [ N ^ { \prime } ]$ according to Definition 1. The server generates a uniform categorical distribution $q _ { u }$ over the target categories . For each relevant client $\mathcal { C } _ { k } .$ , let his/her intersection label set be $\mathcal { T } _ { k } = \mathcal { V } _ { k } \cap \mathcal { V }$ . Note that, since we only allow server and each client $\mathcal { C } _ { k }$ to learn $\mathit { T } _ { k } , \ q _ { u }$ is still the server’s secret to some relevant clients, whose intersection set $\mathcal { T } _ { k } \subset \mathcal { V }$ . For each client the categorical distribution $q _ { k }$ of his/her dataset is also private. To compute $\mu _ { k }$ privately, we transform Eq.1 into the equation

$$
\begin{array}{l} \mu_ {k} = 2 - \left(\sum_ {y \in \mathcal {I} _ {k}} | q _ {k} (y _ {k} = y) - q _ {u} (y _ {u} = y) | ^ {2} \right. \\ + \sum_ {y \in \mathcal {Y} \backslash \mathcal {I} _ {k}} ^ {y \in \mathcal {I} _ {k}} | q _ {k} (y _ {k} = y) - q _ {u} (y _ {u} = y) | ^ {2}) ^ {1 / 2}. \tag {7} \\ \end{array}
$$

The server can compute the second summation in the parentheses by itself, because when $y \in \mathcal { V } \backslash \mathcal { T } _ { k }$ we have $q _ { k } ( y _ { k } = y ) =$ 0. For the first summation over $\mathcal { T } _ { k }$ , we leverage an efficient secure two-party computation protocol based on the homomorphic encryption of BGN [27] to let the server and each client jointly calculate this part using the server’s public key. After this computation, only the server learns each relevant client’s statistical homogeneity $\mu _ { k }$ , while other parties learn nothing. Now the server can solve this optimization problem by greedily choosing clients with the largest $\mu _ { k } / b _ { k } , k \in [ N ^ { \prime } ]$ until the budget B runs out.

2) Diversity-driven Client Selection: Taking content diversity as the quality metric of a client, we have $V _ { \rho } ( \mathcal { Q } ) = \rho ( \mathcal { D } )$ , where $\textstyle { \mathcal { D } } = \bigcup _ { k \in { \mathcal { Q } } } { \mathcal { D } } _ { k }$ . According to Definition 2, we need to first generate content embedding vectors of samples. Similar to existing work [5], [6], [28], we let each client use a general deep learning model (e.g, VGG-16 [29]) to generate a content embedding vector for each sample. However, those work require direct access to all embedding vectors, which violates client’s privacy. Besides, when the total number of samples is large, the complexity of Eq.2 is very high. To address these issues, we propose an efficient privacy-preserving content diversity computation method, which sketches each clients dataset by a low-dimensional vector based on JLtransformation [30] and protects the privacy of each sample using a random response mechanism.

a) Dataset content sketch.: Each client $\mathcal { C } _ { k } , k \in \mathcal { Q }$ locally generates content embedding vectors $\phi _ { k } = \{ \phi _ { k , i } | i \in [ U _ { k } ] \}$ for all relevant samples using a general deep learning model, where each embedding vector $\phi _ { k , i } ~ \in ~ \mathbb { R } ^ { L _ { \phi } } . ~ L _ { \phi }$ is 512 in our implementation. To further encode nk L -dimensional vectors into one low-dimensional vector, the server selects a projection matrix $w \in \mathbb { R } ^ { l _ { \phi } \times L _ { \phi } }$ , where $l _ { \phi } < L _ { \phi }$ , and sends it to all relevant clients. Each client $\mathcal { C } _ { k }$ locally compute the $l _ { \phi } .$ -dimensional projection vector $h ( \phi _ { k , i } ) = \mathrm { s i g n } ( w \cdot \phi _ { k , i } )$ for each sample $\phi _ { k , i }$ . In particular, when each entry of w is generated independently from $\mathcal { N } ( 0 , 1 )$ , with $\begin{array} { r } { l _ { \phi } > \frac { 1 } { \epsilon ^ { 2 } } \mathrm { l o g } n _ { k } } \end{array}$ it with high probability achieves at most ✏ distortion for $n _ { k }$ samples of client $\mathcal { C } _ { k }$ [31]. The distortion caused by this projection reduces the accuracy of diversity but also protect the privacy of embedding vector to a certain extend. Then the sketch of dataset $\mathcal { D } _ { k }$ is $\begin{array} { r } { H _ { k } = \sum _ { i \in [ U _ { k } ] } h \big ( \phi _ { k , i } \big ) } \end{array}$ .

b) Permanent randomized response.: To further protect the existence of each sample, we use a widely adopted randomized response mechanism [32] to generate a noisy representation $\hat { h } ( \phi _ { k , i } )$ of each projection vector $h ( \phi _ { k , i } )$ . Specifically, we add noises as follows:

$$
\hat {h} (\phi_ {k, i}) [ j ] = \left\{ \begin{array}{l l} 1, & \text { with   probability } \frac {f}{2} \\ 0, & \text { with   probability } \frac {f}{2} \\ h (\phi_ {k, i}) [ j ], & \text { with   probability } 1 - f. \end{array} \right. \tag {8}
$$

Here $\hat { h } ( \phi _ { k , i } ) [ j ]$ is the $j \mathrm { - t h }$ bit of $\hat { h } ( \phi _ { k , i } )$ , and $0 < j \leq l _ { \phi } . \ f$ is a user-defined parameter to control the level of privacy. $\displaystyle \ddot { h } ( \phi _ { k , i } )$ is generated once and used for all FL tasks to save computation cost, and more importantly, to avoid privacy leakage caused by multiple queries. Then each client uses the noisy projection vectors to generate a noisy sketch $\begin{array} { r } { \hat { H } _ { k } = \sum _ { i \in [ U _ { k } ] } \hat { h } ( \phi _ { k , i } ) } \end{array}$ and reports it to the server for content diversity measurement. It is proved that this randomized response satisfies $\epsilon _ { \infty }$ -differential privacy where $\begin{array} { r } { \epsilon _ { \infty } = 2 l _ { \phi } \ln ( \frac { 1 - \dot { f } / 2 } { f / 2 } ) } \end{array}$ 1. In this way, we prevent any other party including the server to learn the existence of any sample with confidence.

Algorithm 1: DPP-based Client Selection   
Input : Server S, the budget B, $N'$ clients $\{C_{1},\cdots,C_{N'}\}$ declaring the price $\{b_{1},\cdots,b_{N'}\}$ Output: The index set of selected clients
1 for each client $C_{k}, k \in [N']$ do
2    Calculates $\mu_{k}$ with Eq. 1, and calculates $H_{k}$ using noisy content sketches (Section IV-B2), and sends them to the server
3 The server initializes $Q \leftarrow$ an arbitrary client's index
4 while $\sum_{C_{k} \in Q} b_{k} < B$ do
5    The server finds client $C_{k}$ who maximizes
6 $\frac{(\Pi_{i \in Q \cup \{k\}} \mu_{i}^{2}) \det(S_{Q \cup \{k\}}) - (\Pi_{i \in Q} \mu_{i}^{2}) \det(S_{Q})}{b_{k}}, k \in [N']$ 7 Return the index set Q of the selected clients

Given the noisy content sketch of each client, the similarities between two clients’ datasets $\mathcal { D } _ { k }$ and $\mathcal { D } _ { j }$ is defined as $S _ { k j } =$ $\frac { \hat { H } _ { k } { \cdot } \hat { H } _ { j } } { \vert \hat { H } _ { k } \vert \vert \hat { H } _ { j } \vert }$ Now the server can calculate the diversity value function using noisy content sketches from all relevant clients according to Eq.2, which significantly reduces the computation cost of the content diversity by several orders of magnitude. The optimal solution to maximize the diversity value function is by greedily choosing the next client who has the minimum similarity to the currently selected clients.

3) DPP-based Client Selection: When we consider both statistical homogeneity and content diversity, we convert the client selection problem into a DPP problem. Each client $\mathcal { C } _ { i } , i \in [ N ^ { \prime } ]$ is featured by its data statistical homogeneity $\mu _ { i } ,$ and similarities $S _ { i j }$ to other clients $\mathcal { C } _ { j } , j ~ \in ~ [ N ^ { \prime } ] ~ \backslash ~ i .$ . With $\mu _ { i } ~ > ~ 0 , 0 ~ \leq ~ S _ { i j } ~ \leq ~ 1$ , we define a positive-semidefinite kernel $A _ { [ N ^ { \prime } ] } ~ = ~ [ A _ { i j } ] _ { i , j \in [ N ^ { \prime } ] }$ , where ${ \cal A } _ { i j } \ = \ \mu _ { i } \mu _ { j } S _ { i j }$ . Then the probability of selecting clients  is $\overset { \cdot } { P } _ { A } ( \mathcal { Q } )$ , which is the determinant of $A _ { \mathcal { Q } }$ , i.e., $P _ { A } ( \mathcal { Q } ) = d e t ( A _ { \mathcal { Q } } )$ . We give one example to illustrate the implicit meaning of the determinantal probability measure with a subset $\mathcal { Q } = \{ i , j \}$ ,

$$
P _ {A} (\mathcal {Q}) \propto \left| \begin{array}{c c} A _ {i i} & A _ {i j} \\ A _ {j i} & A _ {j j} \end{array} \right| = \left| \begin{array}{c c} \mu_ {i} ^ {2} & \mu_ {j} \mu_ {i} S _ {i j} \\ \mu_ {i} \mu_ {j} S _ {i j} & \mu_ {j} ^ {2} \end{array} \right|. \tag {9}
$$

The diagonal entries are computed without a similarity term because the similarity to itself is always one. The determinant increases when the homogeneity increases and the similarity decreases, thus the DPP-based selection tends to choose clients with homogeneous distributed categories while avoiding highly similar clients simultaneously.

The value function is $V _ { d } ( \mathcal { Q } ) = \operatorname* { d e t } ( A _ { \mathcal { Q } } )$ , where $\operatorname* { d e t } ( A _ { \mathcal { Q } } ) =$ $\Pi _ { i \in \mathcal { Q } } \mu _ { i } ^ { 2 } \operatorname* { d e t } ( S _ { \mathcal { Q } } ) , S _ { \mathcal { Q } } = [ S _ { i j } ] _ { i , j \in \mathcal { Q } }$ . Given $N ^ { \prime }$ relevant clients,

Algorithm 2: FL with Importance-based Sample Selection   
Input : K clients $\{C_{1},\cdots,C_{K}\}$ have datasets $\{D_{1},\ldots,D_{K}\}$ and initial client selection probability $\{P_{1}^{1},\ldots,P_{K}^{1}\}$ , E is the number of local epochs, $\eta$ is the learning rate, and $\zeta$ is the fraction of clients being selected

Output: Global model $\theta^{*}$ 1 Server initializes $\theta_{0}$ 2 for each round $t=\{1,2,\cdots,T\}$ do

3 $m\leftarrow\max(\zeta\cdot K,1)$ 4 $M_{t}\leftarrow m$ clients selected based on selection probabilities $\{P_{1}^{t},\ldots,P_{K}^{t}\}$ 5 for each client $C_{k}\in M_{t}$ in parallel do

6 $\theta_{t+1}^{k}\leftarrow LocalModelUpdate(k,\theta_{t})$ 7 $\theta_{t+1}\leftarrow\sum_{C_{k}\in M_{t}}\frac{n_{k}}{n}\theta_{t+1}^{k} // update global model$ 8 for each client $C_{k}\in M_{t}$ do

9 $P_{k}^{t+1}=\frac{n_{k}||\theta_{t}^{k}-\theta_{t}||}{\sum_{C_{k}\in M_{t}}n_{k}||\theta_{t}^{k}-\theta_{t}||} // update client selection probability$ 10 Function LocalModelUpdate( $k,\theta_{t}$ ):
11 Calculates $\lambda(z_{k,i},t-1),p_{k,i}^{t-1},i\in[U_{k}]$ using Eq.4, $\theta_{0}^{k}=\theta_{t}$ 12 for each local epoch j from 1 to E do

13 $\gamma_{k}^{j}\leftarrow g$ data samples selected with $\{p_{k,1}^{t-1},\cdots,p_{k,n_{k}}^{t-1}\}$ from $D_{k}$ , and $\lambda(z_{k,j},t-1)<\delta_{k}^{t-1}$ 14 $\theta_{j}^{k}\leftarrow\theta_{j-1}^{k}-\eta\nabla F_{k}(\theta_{j-1}^{k};\gamma_{k}^{j})$

each client $\mathcal { C } _ { k }$ has a declared price $b _ { k }$ , the optimization problem is NP-hard because all possible subsets have to be examined. We adopted one simple greedy algorithm to approximate the optimal solution with an approximation ratio of [33 $\frac { 8 } { 9 } + \epsilon _ { 1 }$ , and convert it into a log-submodular problemhis end, our algorithm iteratively adds k to the result collection $\mathcal { Q }$ if $\mathcal { C } _ { k }$ maximizes $P _ { A } ( \mathcal { Q } \cup \{ k \} )$ among the remaining clients. The main steps are summarized in Algorithm 1.

# V. DYNAMICAL SAMPLE SELECTION

Given selected high-quality clients whose index set is $\mathcal { Q } \subset$ $[ { \cal N } ^ { \prime } ] , | \mathcal { Q } | = K$ , to further improve the model performance and reduce the training overhead, in each training iteration t, ⇣-fraction of important clients are selected and then their important samples are used for training. A straightforward method to measure the importance of each client $\mathcal { C } _ { k } , k \in [ K ]$ is to calculate $\lambda ( \mathcal { D } _ { k } , t )$ using $\operatorname { E q } . 5$ and obtain client selection distribution $P _ { k } ^ { t } , k \in [ K ]$ . This method, however, can be very computationally expensive, which requires $O ( n s )$ (s is the number of model parameters $\theta \in \mathbb { R } ^ { s }$ , n is the number of total samples) operations in each iteration. n and s are usually large in federated deep learning tasks. To reduce the cost, for dynamic client selection, we propose a simple but effective method to update the probability $P _ { k } ^ { t }$ based on the training updates $( i . e . , \ \theta _ { t } ^ { k } , \theta _ { t } )$ stored in the server. Specifically, in the t-th iteration, the server selects m clients according to their current selection probabilities $\{ P _ { 1 } ^ { t } , \cdots , P _ { K } ^ { t } \}$ updated using the following equation

$$
P _ {k} ^ {t} = \frac {n _ {k} \left| \theta_ {t - 1} ^ {k} - \theta_ {t - 1} \right|}{\sum_ {\mathcal {C} _ {k} \in M _ {t - 1}} n _ {k} \left| \theta_ {t - 1} ^ {k} - \theta_ {t - 1} \right|}, \tag {10}
$$

where $M _ { t - 1 }$ is the set of m clients selected in the t 1-th iteration. That is, we assign clients with larger influence on the current global model $\theta _ { t - 1 }$ higher probabilities $P _ { k } ^ { t }$ to be selected in the t-th iteration. Then for each selected client $\mathcal { C } _ { k }$ in round t, it calculates the importance $\lambda ( z _ { k , i } , t - 1 )$ for all samples $z _ { k , i } \in \mathcal { D } _ { k }$ according to Eq.4, and selects local samples with $\lambda ( z _ { k , i } , t - 1 ) \leq \delta _ { k } ^ { t - 1 }$ according to $p _ { k , i } ^ { t } \propto \lambda ( z _ { k , i } , t - 1 )$ . The details of the FL with importance based dynamic data selection are presented in Algorithm 2.

# VI. EVALUATIONS

In this section, we measure the effectiveness of our proposed quality-driven client selections, including homogeneity-aware selection, diversity-driven selection and DPP-based selection. Then, we show that our dynamical sample selection improve the global model to achieve a higher accuracy and faster convergence rate.

# A. System Deployment

We implemented and deployed our data selection methods on a real AIoT system with one server and 50 clients, including 20 edge nodes, 20 laptops and 11 desktops (see details in Table I). We used one desktop worked as the server and let other 10 desktops work as clients.

TABLE I SYSTEM DEPLOYMENT. 

<table><tr><td>Devices</td><td>#</td><td>Information</td></tr><tr><td>Edge node</td><td>20</td><td>Intel i7-6700 CPU, 16G RAM, Tesla P4/T4 GPUs</td></tr><tr><td>Laptop</td><td>20</td><td>Intel i7 CPU, 64G RAM, 4 Titan X GPUs</td></tr><tr><td>Desktop</td><td>11</td><td>Intel i7 CPU, 16G RAM</td></tr></table>

# B. Experiment Configuration

1) Datasets: We constructed two types (error-free and erroneous) of training datasets on MNIST [34] and CIFAR10 [20] for different tasks (see details in Table II). The test datasets $\mathcal { D } _ { M } ^ { T } , \mathcal { D } _ { C } ^ { T }$ were located at the server.   
2) Deep Learning Models: We implemented the typical federated optimization algorithm FedSGD [1] and two popular deep learning models, FedAVG-CNN-MNIST (a CNN network [35] for digit number recognition) and FedAVG-CNN-CIFAR (a residual network [21] for image recognition). We run federated learning until a pre-specified test accuracy is reached (98.0% for $\mathcal { D } _ { M }$ and 92.5% for $\mathcal { D } _ { C } )$ , or a maximum number of iterations have elapsed.

TABLE II DATASETS FOR DIFFERENT TASKS. 

<table><tr><td>Type</td><td>Notation</td><td>Size</td><td>Description</td></tr><tr><td rowspan="4">Training</td><td> $\mathcal{D}_{M}$ </td><td>60,000</td><td>original training data of MNIST</td></tr><tr><td> $\mathcal{D}_{M}^{m}$ </td><td>60,000</td><td> $\mathcal{D}_{M}$  40% mislabeled samples</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>50,000</td><td>original training data of CIFAR</td></tr><tr><td> $\mathcal{D}_{C}^{m}$ </td><td>50,000</td><td> $\mathcal{D}_{C}$  with 30% mislabeled samples</td></tr><tr><td rowspan="2">Testing</td><td> $\mathcal{D}_{M}^{T}$ </td><td>10,000</td><td>original test data of MNIST</td></tr><tr><td> $\mathcal{D}_{C}^{T}$ </td><td>10,000</td><td>original test data of CIFAR</td></tr></table>

# C. Quality-driven Client Selection

We first evaluate the proposed three quality-driven client selection methods, homogeneity-aware, diversity-driven and DPP-based methods (see details in Section IV). We partitioned datasets $\mathcal { D } _ { M } , \mathcal { D } _ { C }$ over 50 clients with five different statistical homogeneity and content diversity settings. In the first setting, 10 IID and 40 Non-IID (k) clients, here k is randomly selected from 1 to 9; each client has the same amount of data; for each client, we randomly removed 50%-90% samples and add the same amount of samples transformed from remaining samples (see in Section II-C). We repetitively increased the number of IID clients by 5 and reduced the proportion of transformed samples by 10% for four times to compose the dataset in the other four settings. For the declared prices, we considered two commonly used models, identical price and normally distributed price. The mean value of normal distribution equals to the identical price, which is set to 1.0 for each sample, and the variance is 0.2. Then the declared price of each client is the summation of all his/her samples’ prices. The budget is set to 24, 000, 20, 000 for $\mathcal { D } _ { M } , \mathcal { D } _ { C }$ . We selected clients by three selection methods in five settings. Compared with directly calculating content diversity using embedding vectors, our sketch based method reduce the time cost from 68.60h and 57.56h to 102.71s and 383.82s for $\mathcal { D } _ { M } , \mathcal { D } _ { C } .$ , respectively. We trained FedAVG-CNN-MNIST and FedAVG-CNN-CIFAR models on selected clients. The test accuracy for $\mathcal { D } _ { M } ^ { T }$ and $\mathcal { D } _ { C } ^ { T }$ is shown in Fig. 4, which shows that our three privacy-preserving quality-driven client selection methods all outperform the commonly used random client selection. Specially, for diversity-driven client selection, we compare the method using only content sketch and the one using sketch and randomized response. To achieve differential privacy for each sample, though the randomized response introduces some noises to the content sketch, it still has obviously higher accuracy than that of the random selection. Our DPP-based method performs best in all cases and settings due to the fact that it considers both quality dimensions simultaneously. For example, in setting 5, the DPP-based methods can reduce the average false rate for digit recognition on MNIST from 17.75, 16.73%, to 8.5%, 6.8%, and for image recognition on CIFAR from 36.8%, 34.8% to 18.96%, 18.91%, in identical price setting and normally distributed price setting respectively.

# D. Dynamical Sample Selection

We compare our upper bound norm based importance selection to other four state-of-the-art data selection strategies, random, loss based, and gradient norm based. Here we considered two typical FL scenarios, a crowd-sourced scenario with many clients and an enterprise cooperation scenario with two clients. For the first scenario, the model FedAVG-CNN-MNIST were trained on $\mathcal { D } _ { M } , \mathcal { D } _ { M } ^ { m }$ assigned to 50 clients, and 40 clients are selected for each iteration. For the second scenario, the model FedAVG-CNN-CIFAR were trained on DC, DmC assigned to 2 clients. To avoid selecting erroneous samples, the thresholds $\delta _ { k } ^ { t }$ was set to 10.0, 200.0 for $\mathcal { D } _ { M } ^ { m } , \mathcal { D } _ { C } ^ { m }$ , which is determined by detecting the outlier of upper bound norms of all samples (see Fig. II-A for an example). Fig. 5 shows that our method using both model updates and upper bound norm outperforms all other methods in terms both accuracy and convergence speed in all scenarios. In Fig. 5(a) and Fig. 5(b), where the datasets are clean, the loss based method achieves lower but comparable performance with our method. But in Fig. 5(c) and Fig. 5(d), where the datasets contains erroneous samples, the performance of loss based and gradient norm based methods deteriorate significantly, while our method still achieves high accuracy and stable convergence. On datasets DmM , DmC , the test accuracy are 94.0%, 79.88% for random sampling, 91.8%, 56.02% of loss based sampling, 93.5%, 66.08% of gradient norm sampling, and 98.4%, 86.34% of our method. We present the computation and communication cost for training two models in Fig. 6. On $\mathcal { D } _ { M }$ , our method saves 48.1%, 19.6%, 64.6% computation cost, and 50.3%, 20.5%, 66.8% communication cost compared to random, loss based and gradient based methods. On ${ \mathcal { D } } _ { C } .$ , our method saves 38.0%, 17.6%, 55.3% computation cost, 37.5%, 16.7%, 54.5% communication cost compared to those three methods.

![](images/18d83e593f3b5ab4a65d72b124903c3cdd5e77267174c542e31d9006e590923f.jpg)



(a) FedAVG-CNN-MNIST, identical price.

![](images/a27f8d49489d58510a0802674883e012df049e790e02243c538693f4709d1766.jpg)



(b) FedAVG-CNN-MNIST, normly distributed price.

![](images/ff3c89031686dc0206dcae12d3f8776dd1c17d68f403efe3796e00f440132307.jpg)



(c) FedAVG-CNN-CIFAR, identical price.

![](images/9da602d0e8ae3d609fea094382557b34ec259d0d38f7ba1f4cc125e04ed3222f.jpg)



(d) FedAVG-CNN-CIFAR, normly distributed price.

Fig. 4. Test accuracy for training FedAVG-CNN-MNIST and FedAVG-CNN-CIFAR models on clients having data samples with different statistical homogeneity and content diversity in different declared price models. The X-coordinate indicates setting 1-5.   
![](images/683ccb1158a752e7e67a17913fb1321441b9560d9ba84e19321e97b869b6cce8.jpg)



(a) FedAVG-CNN-MNIST, DM.

![](images/383b2ba26c5907447b5d32840631233364f5d85751f081fc9f0cd53f19ca6179.jpg)



(b) FedAVG-CNN-CIFAR, DC.

![](images/6290cc5a52e78436690df707075cec0176d481fedf314b33b9d3eb419584c8ff.jpg)



(c) FedAVG-CNN-MNIST, DmM.

![](images/d0059b3abf99c6e1ad6a8dc229d90c0890504b0a36459f060252a2272c458666.jpg)



(d) FedAVG-CNN-CIFAR, DmC .

Fig. 5. Test accuracy against training time for training FedAVG-CNN-MNIST and FedAVG-CNN-CIFAR models on on clean datasets and erroneous dataset with different sampling methods. Here “updates-upper” indicates selecting first clients using Eq. 10 and then samples using Eq.5.   
![](images/023983a4a9cbc0ceb7491c8dab87019772088968fed0f37d5ba5ceabe3509a1c.jpg)



(a) Computation cost (s).

![](images/bdf52ff1e529fafc80223ede10d8a1c070443dc9acf9d13286d093995e634f05.jpg)



(b) Communication cost (MB).   
Fig. 6. Computation and communication cost for training FedAVG-CNN-MNIST and FedAVG-CNN-CIFAR models on clean datasets $\mathcal { D } _ { M } , \mathcal { D } _ { C }$ until the test accuracy reaches 98.0% for $\mathcal { D } _ { M }$ and 85.0% for $\mathcal { D } _ { C }$ with different sampling methods.

# VII. CONCLUSION

To the best of our knowledge, we propose the first effective and privacy-preserving sample selection solution for FL to obtain models with high accuracy and fast convergence speed when there are low-quality or even erroneous data. Our solution considers multiple factors that influence the model performance and both the clients’ data privacy and the server’s task privacy. To reduce the cost for data selection, we propose a set of novel techniques to first selects highquality clients before training and then dynamically selects clients and their samples with greater importance to the global model. Our experiments on a real AIoT system show that our design outperforms existing solutions in terms of higher model accuracy, faster convergence speed, and lower computation and communication cost.

# VIII. ACKNOWLEDGMENTS

Lan Zhang and Xiang-Yang Li are the contact authors. The research is supported by National Key R&D Program of China 2017YFB1003003, National Natural Science Foundation of China with No. 61822209, No.61625205No. 61932016, No. 61751211, No. 61520106007, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002, the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial Intelligence and Statistics, 2017, pp. 1273–1282.   
[2] J. Konecnˇ y, H. B. McMahan, F. X. Yu, P. Richt \` arik, A. T. Suresh, and ´ D. Bacon, “Federated learning: Strategies for improving communication efficiency,” arXiv preprint arXiv:1610.05492, 2016.   
[3] A. Hard, K. Rao, R. Mathews, S. Ramaswamy, F. Beaufays, S. Augenstein, H. Eichner, C. Kiddon, and D. Ramage, “Federated learning for mobile keyboard prediction,” arXiv preprint arXiv:1811.03604, 2018.   
[4] K. Bonawitz, H. Eichner, W. Grieskamp, D. Huba, A. Ingerman, V. Ivanov, C. Kiddon, J. Konecny, S. Mazzocchi, H. B. McMahan et al., “Towards federated learning at scale: System design,” arXiv preprint arXiv:1902.01046, 2019.   
[5] L. Zhang, Y. Li, X. Xiao, X.-Y. Li, J. Wang, A. Zhou, and Q. Li, “Crowdbuy: Privacy-friendly image dataset purchasing via crowdsourcing,” in IEEE INFOCOM 2018-IEEE Conference on Computer Communications. IEEE, 2018, pp. 2735–2743.   
[6] A. Li, L. Zhang, J. Qian, X. Xiao, X.-Y. Li, and Y. Xie, “Todqa: Efficient task-oriented data quality assessment,” in 2019 15th International Conference on Mobile Ad-Hoc and Sensor Networks (MSN). IEEE, 2019, pp. 81–88.   
[7] A. Katharopoulos and F. Fleuret, “Not all samples are created equal: Deep learning with importance sampling,” arXiv preprint arXiv:1803.00942, 2018.   
[8] G. Alain, A. Lamb, C. Sankar, A. Courville, and Y. Bengio, “Variance reduction in sgd by distributed importance sampling,” arXiv: Machine Learning, 2015.   
[9] I. Loshchilov and F. Hutter, “Online batch selection for faster training of neural networks,” arXiv preprint arXiv:1511.06343, 2015.   
[10] T. Schaul, J. Quan, I. Antonoglou, and D. Silver, “Prioritized experience replay,” arXiv preprint arXiv:1511.05952, 2015.   
[11] C.-Y. Wu, R. Manmatha, A. J. Smola, and P. Krahenbuhl, “Sampling matters in deep embedding learning,” in Proceedings of the IEEE International Conference on Computer Vision, 2017, pp. 2840–2848.   
[12] T. Tuor, S. Wang, B. J. Ko, C. Liu, and K. K. Leung, “Data selection for federated learning with relevant and irrelevant data at clients,” arXiv preprint arXiv:2001.08300, 2020.   
[13] L. Pu, X. Chen, R. Yun, X. Yuan, P. Zhou, and J. Xu, “Cocktail: Cost-efficient and data skew-aware online in-network distributed machine learning for intelligent 5g and beyond,” arXiv preprint arXiv:2004.00799, 2020.   
[14] J. Byrd and Z. Lipton, “What is the effect of importance weighting in deep learning?” in International Conference on Machine Learning, 2019, pp. 872–881.   
[15] A. Raj, C. Musco, and L. Mackey, “Importance sampling via local sensitivity,” in International Conference on Artificial Intelligence and Statistics, 2020, pp. 3099–3109.   
[16] F. Sattler, S. Wiedemann, K.-R. Muller, and W. Samek, “Robust and ¨ communication-efficient federated learning from non-iid data,” IEEE transactions on neural networks and learning systems, 2019.   
[17] Y. Zhao, M. Li, L. Lai, N. Suda, D. Civin, and V. Chandra, “Federated learning with non-iid data,” arXiv preprint arXiv:1806.00582, 2018.   
[18] S. Wang, T. Tuor, T. Salonidis, K. K. Leung, C. Makaya, T. He, and K. Chan, “When edge meets learning: Adaptive control for resourceconstrained distributed machine learning,” in IEEE INFOCOM 2018- IEEE Conference on Computer Communications. IEEE, 2018, pp. 63– 71.   
[19] G. Castellano, F. Esposito, and F. Risso, “A distributed orchestration algorithm for edge computing resources with guarantees,” in IEEE IN-FOCOM 2019-IEEE Conference on Computer Communications. IEEE, 2019, pp. 2548–2556.   
[20] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” semanticscholar, 2009.   
[21] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.   
[22] J. Luo, X. Wu, Y. Luo, Y. Huang, Y. Liu, and Q. Yang, “Real-world image datasets for federated learning,” arXiv:1910.11089, 2019.   
[23] X. Li, K. Huang, W. Yang, S. Wang, and Z. Zhang, “On the convergence of fedavg on non-iid data,” arXiv preprint arXiv:1907.02189, 2019.

[24] S. P. Karimireddy, S. Kale, M. Mohri, S. J. Reddi, S. U. Stich, and A. T. Suresh, “Scaffold: Stochastic controlled averaging for federated learning,” arXiv preprint arXiv:1910.06378, 2019.   
[25] T. Wu, L. Chen, P. Hui, C. J. Zhang, and W. Li, “Hear the whole story: Towards the diversity of opinion in crowdsourcing markets,” Proceedings of the VLDB Endowment, vol. 8, no. 5, pp. 485–496, 2015.   
[26] R. Agrawal, A. Evfimievski, and R. Srikant, “Information sharing across private databases,” in Proceedings of the 2003 ACM SIGMOD international conference on Management of data, 2003, pp. 86–97.   
[27] J. Yuan and S. Yu, “Privacy preserving back-propagation neural network learning made practical with cloud computing,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 1, pp. 212–221, 2014.   
[28] T. Wu, L. Chen, P. Hui, C. Jason, and Z. W. Li, “Hear the whole story: Towards the diversity of opinion in crowdsourcing markets.”   
[29] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” arXiv preprint arXiv:1409.1556, 2014.   
[30] C. Biswas, D. Ganguly, D. Roy, and U. Bhattacharya, “Privacy preserving approximate k-means clustering,” in Proceedings of the 28th ACM International Conference on Information and Knowledge Management, ser. CIKM 19. Association for Computing Machinery, 2019, p. 13211330.   
[31] L. Jacques, J. N. Laska, P. T. Boufounos, and R. G. Baraniuk, “Robust 1- bit compressive sensing via binary stable embeddings of sparse vectors,” IEEE Transactions on Information Theory, vol. 59, no. 4, pp. 2082– 2102, 2013.   
[32] L. Erlingsson, V. Pihur, and A. Korolova, “Rappor: Randomized aggregatable privacy-preserving ordinal response,” 2014.   
[33] A. Kulesza and B. Taskar, Determinantal Point Processes for Machine Learning. IEEE, 2012.   
[34] “The mnist database of handwritten digits,” http://yann.lecun.com/exdb/ mnist/.   
[35] Y. LeCun, L. Bottou, Y. Bengio, P. Haffner et al., “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.