# ProxySampler: Proxy Informativeness Estimation for Efficient Data Selection in Active Learning

Miao-Hui Song

University of Science and Technology of China

Hefei, China

songmiaohui@mail.ustc.edu.cn

Mu Yuan

The Chinese University of Hong Kong

Hong Kong, China

muyuan@cuhk.edu.hk

# Abstract

Large-scale data analysis services require efficient periodic model updates to adapt to the possibly changing data distributions. Manually labeling all available samples for task model updates is infeasible for a large sample scale. Active learning technique is proposed to iteratively select subsets of the most informative samples for labeling. From our experience of applying active learning in a realworld video analysis system, we identify a previously overlooked bottleneck of time cost: data selection. Existing active learning methods select data by estimating informativeness (e.g., output confidence) over all unlabeled samples in each iteration. This data selection process can take up to 42% of the time cost of end-to-end model updates in our system (totals include the time for manual labeling, data selection, and model updates.). To address the time cost bottleneck caused by data selection, we propose a new idea: proxy informativeness estimation. We start with modeling the time cost of data selection, from which we identify three key factors: unit estimation cost, the number of samples for estimation, and the number of iteration rounds. The influence of the first two factors increases cumulatively with the number of iteration rounds. Correspondingly, we design a proxy estimator and a sample pooling method, respectively. Our proxy estimator is a lightweight neural network for direct informativeness estimation to replace the role of the high-cost task model, thus reducing the unit cost. And, our sample pooling method leverages historical estimation results to narrow the scope of sample candidates. Based on the above design, we develop ProxySampler, which can be integrated with various active learning approaches as a plug-in. Experimental results show

∗Lan Zhang is the corresponding author.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

CIKM ’25, Seoul, Republic of Korea

© 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM.

ACM ISBN 979-8-4007-2040-6/2025/11

https://doi.org/10.1145/3746252.3761315

Lan Zhang∗

University of Science and Technology of China

Hefei, China

Institute of Artificial Intelligence

Hefei Comprehensive National Science Center

Hefei, China

zhanglan@ustc.edu.cn

Yijun Liu

China Merchants Bank

Shenzhen, China

lyj\_mcfly@cmbchina.com

that integrating ProxySampler with state-of-the-art active learning methods can reduce the time cost by 53.6-83.3% (a 2.15-6.01× speedup) when achieving the same accuracy.

# CCS Concepts

• Computing methodologies → Active learning settings.

# Keywords

Active Learning, Data Labeling, Efficient Data Selection, Informativeness Estimation.

# ACM Reference Format:

Miao-Hui Song, Lan Zhang, Mu Yuan, and Yijun Liu. 2025. ProxySampler: Proxy Informativeness Estimation for Efficient Data Selection in Active Learning. In Proceedings of the 34th ACM International Conference on Information and Knowledge Management (CIKM ’25), November 10–14, 2025, Seoul, Republic of Korea. ACM, New York, NY, USA, 11 pages. https: //doi.org/10.1145/3746252.3761315

# 1 Introduction

Efficient periodic model updates are important in large-scale data analysis services because of the possibly changing data distributions [10, 22]. It is infeasible to label all available data for task model updates on a large scale. Active learning (AL) [21, 37] emerges as an important technique to iteratively select subsets for manual labeling, which are then used for model updates. In contrast to the one-time labeling idea, AL takes an iterative approach to select the most informative samples for the current model. This dynamic adaptation enhances the efficiency of labeling, which reduces laborintensive manual labeling while maintaining high performance.

• System observation: data selection becomes the bottleneck. We developed a real-time video analysis system in our university for campus security with 2529 cameras installed in public areas, generating millions of video frames daily. To adapt to the possible dynamic changes in data distribution on campus and ensure timely security incident detection, periodic updating of the detection models daily with newly generated videos is necessary [55]. Obviously, labeling all video frames is impractical [40]. So we applied a classic AL approach [24] in our labeling process. As shown in Fig. 1, the task model needs to estimate informativeness on all raw samples for data selection in each round. The highest informativeness samples are selected for manual labeling to update the task model in each round. The overall time cost involves manual labeling, data selection, and model updates. Fig. 2a shows the end-to-end time profiling of the re-identification task to achieve 65% task accuracy in our video systems. We found that the data selection procedure is too time-consuming (takes up to 42% overall time cost) and becomes the efficiency bottleneck. The same problem also occurs in another emotion recognition task as shown in Fig. 2b. To achieve 86% task accuracy, when using the CAL strategy [28], the data selection process accounts for 85% of the total time cost, while the manual labeling time cost accounts for 11.2% of the total time cost. The reason for time-consuming data selection is quite intuitive because existing AL methods [20, 32, 47] require the task model to predict all unlabeled data and select data by measuring informativeness based on these predictions of the task model. This process also repeats with the iteration of active learning. Therefore, given a large unlabeled dataset or a heavy task model, the iterative data selection process can easily dominate the cost in the AL process.

![](images/92166a6bc90a3086f2255b9c41171ed1a7ea5e367616cc1fd81f59fe0899ba39.jpg)



Figure 1: Original active learning workflow. Raw samples participate in informativeness estimation in each round of AL iteration, which leads to repeated and redundant feature embedding and informativeness measurement calculations.

• Cost modeling. So we can conclude that to enhance the efficiency of the large-scale active learning process, we need to reduce the time for data selection. To achieve this goal, we propose a new idea: proxy informativeness estimation. We start with modeling the time cost of the data selection process and identify three key factors: (1) unit estimation cost (composed of feature embedding cost and informativeness measure cost) [7, 52], (2) the number of samples for estimation [42, 45], and (3) the number of iteration rounds [1, 11]. The influence of the first two factors increases cumulatively with the number of iteration rounds. In this work, we focus on reducing the cost caused by the first two key factors.

• Design goals. Correspondingly, we have two primary design goals in pursuit of a time-efficient data selection. (1) Lightweight estimator and simplified measurement. The estimation process must be lightweight to reduce the unit estimation cost. As is evident, a lighter model translates to quicker predictions. And the complexity of informativeness measurement should be reduced. So we need a lightweight estimator with simplified measurement methods to replace the role of the high-cost task model in the original informativeness estimation process. (2) Narrowed candidates. From the cost model, the data selection cost is linearly positively related to

![](images/8f7b74d8fc18044b9a12514c25fbe2de6faff32e36b391ed0591b6ad00341051.jpg)



(a) Re-Identification.

![](images/c40df8a586fcaf1655e30370e3dc947d6623263cc1029d6c28efdc8237eb28a4.jpg)



(b) Emotion Recognition.

Figure 2: Overall time cost profiling (manual labeling, data selection, task model training).   
![](images/27c449957a7b1685c1b0d91394c88a7620fdcf3b13e81f11a9d94f0169116c0f.jpg)



![](images/56f7b3648f237f77143e1908584b6fd40b7fdec2a99d2faccef0c53c453bddef.jpg)



Figure 3: Comparison of using raw text inputs and pretrained embeddings to directly learn informativeness on the emotion recognition task.

the candidate samples involved. Our goal is to narrow the scope of sample candidates to address the issue caused by the large number of samples for estimation.

• Core idea. Following these goals, we present a new idea named proxy informativeness estimation and develop the ProxySampler for efficient data selection in active learning. We propose a proxy estimator and a sample pooling method respectively to achieve two design goals. For the first design goal, we propose one-time feature embedding and a directly lightweight informativeness measure for iterative data selection. Different from previous work [5, 44], which uses a proxy model to learn the original task, we propose to use a proxy model to learn informativeness directly. We theoretically demonstrate the feasibility of directly learning informativeness. We did the experiment and found that using the pre-trained embeddings, a lightweight neural network can effectively learn the informativeness measurement as shown in Fig 3. So we adopt a pretrained model to perform one-time feature embedding on the raw data to reduce unit feature embedding cost from Embed×Round# to Embed × 1. We employ a lightweight neural network, named proxy estimator, to directly learn the informativeness to reduce the unit informativeness measure cost in each round of iterations. For the second design goal, we observe that the high-informativeness samples change greatly in the next round, while the low-informativeness samples remain stable in the next round. Therefore, our sample pooling method uses the previous round estimation result to filter low-informativeness samples, thus effectively narrowing down sample candidates in the next round.

We summarize the main contributions of this work as follows:

• We identify a previously overlooked time overhead bottleneck in the large-scale active learning workflow. We introduce a new idea, direct proxy informativeness estimation, which directly learns informativeness to optimize two key factors in the data selection cost.

• We develop ProxySampler, the first proxy informativeness estimation framework for efficient data selection in active learning. We analyze the theoretical feasibility of directly learning the informativeness using a proxy estimator based on computational learning theory. Our proposed sample pooling method can further narrow the sample candidates down to ????, ?? < 1 in each round.   
• We conduct extensive evaluations of ProxySampler on public datasets and real video analysis systems with three different tasks and modalities. On 400,000 samples, to achieve the same accuracy, integrating ProxySampler with state-ofthe-art methods can reduce the time cost by 53.6-88.3% (a 2.15-6.01× speedup).

# 2 Related Work

• Active learning. Lots of work [6, 20, 47] focus on designing various AL strategies to obtain a subset of the most informative data. These methods can be categorized according to how the informativeness is measured [20]. The confidence-based methods calculate the informativeness by the least maximum output confidence [23, 24] or the margin confidence [35], etc. The clustering-based meth ods [6, 15] determine the informativeness through the distance between the samples and the centroid. These methods share one common aspect: they all require the task model to perform repetitive predictions and informativeness measurement on unlabeled samples during the informativeness estimation. Our ProxySampler aims to improve the efficiency of data selection in AL and is complementary to ever-evolving informativeness measurements.

• Input filtering. Filtering some data to avoid redundant computation is a common approach to accelerate the computation process [16, 48–50]. Infi [48] filters the data to eliminate input redundancy, reducing the cost of inference calculations. NoScope [17] identifies essential frames for object queries within the video database by employing task-specific difference detectors. Focus [14] utilizes a compressed CNN to index potential object classes to reduce query latency by clustering similar objects. To the best of our knowledge, ProxySampler is the first to adopt this idea to accelerate the active learning data selection process.

• Selection via proxy (SVP). Several efficient AL works [5, 9, 46] show that smaller models can be used for data selection when the larger models are in play. It usually uses dropping patches [26] or layers [51] or reducing the token resolution [4] to trade off the inference time and performance [8, 43]. In multi-modal learning, training a single smaller model in parallel [8] can efficiently select the most learnable sub-batch to reduce time cost. SVP [5] removes hidden layers from the target model, using smaller architectures and training for fewer epochs to provide signals for data selection.

Uniqueness. Although they are all based on the idea of using smaller models for data selection, our design is significantly different from existing works. The proxy models used in existing SVP works have the same learning objective as the task model, but our proxy estimator aims to learn informativeness directly.

# 3 Overview

This section first models the time cost of data selection in active learning (§ 3.1). Then we introduce the ProxySampler framework,

![](images/302395ceee34f93bb55342e6f89f580f572f868a47dcdce6a45477ef619cf74a.jpg)



Figure 4: Overview of ProxySampler framework. Feature embedding is performed only once. Then, a lightweight neural network called the proxy estimator directly predicts informativeness based on embeddings for data selection.

which consists of two key modules, respectively designed for the corresponding two cost factors (§ 3.2).

# 3.1 Cost Modeling

In each iteration of AL, we need to select a subset of unlabeled data for labeling. We found that this data selection process becomes the bottleneck of time cost when applying AL in our video analysis system. To understand the bottleneck, we started by modeling the time cost of data selection and obtained the formula as follows:

$$
\text { Cost } = \underbrace {\left(\text { Embed } + \text { Measure }\right)} _ {\text { Unit   Cost }} \times \text { Sample } \# \times \text { Round } \#. \tag {1}
$$

For existing AL approaches [37, 47], the Unit Cost is the time cost of evaluating an unlabeled sample for informativeness estimation. The informativeness estimation requires two key steps: embedding the raw data into the feature space using the task model and then measuring the informativeness based on these embeddings [6, 28, 47]. Therefore, we split the unit cost into feature embedding cost (denoted as Embed) and informativeness measure cost (denoted as Measure) as shown in Equation 1. Sample# and Rounds# are typically the number of all unlabeled samples and active learning rounds.

From the cost formula, when the task model is large (e.g., deep neural networks with billions of parameters), the unit cost can be very expensive since it involves the inference of the task model. And when the informativeness measurement is complex (e.g., KNNbased AL strategy with the complexity of ??2), the unit cost is also very expensive. On the other hand, when the volume of unlabeled samples is big (e.g., millions of images), the data selection overhead is prohibitive even for small task models. The influence of these two factors (unit cost and Sample#) also increases cumulatively with the active learning rounds. We focus on reducing the cost caused by these two key factors in this work.

# 3.2 ProxySampler Framework

To address the efficiency bottleneck caused by data selection in active learning, we propose the ProxySampler framework, which consists of two main modules: proxy estimator and sample pooling. Fig. 4 gives an overview of the ProxySampler framework.

![](images/287aec360c12b523ac60684e5c4e7191ae729432507d2730550f08e6b2254bd7.jpg)



(a) Unstable High Info.

![](images/02191860e0e4623e3750fc4576470a5ba8757421d7aa19253552e550fa180c03.jpg)



(b) Stable Low Info.   
Figure 5: Informativeness (Info.) changes on emotion recognition task with the Conf. strategy.

• Proxy estimator: removable feature embedding. As illustrated in Sec 3.1, the same sample requires repetitive embedding and measurement in each round, which takes up a large proportion of time. To mitigate the cost of repetitive embedding and measurement, we experimentally explored using the pre-trained embedding model for one-time embedding and direct informativeness prediction. Specifically, for a text-based emotion recognition task, we use a pre-trained BERT model [41] to get the embedding of text inputs. Then we connect four fully connected layers after the embedding to predict the informativeness directly. As a baseline, we also implement a prediction model that takes the raw text as input, using four identical fully connected layers. The blue line in Fig. 3 shows the loss and Mean Absolute Error (MAE) of the prediction model. We can conclude that using the pre-trained embeddings, a lightweight neural network can directly learn the informativeness measurement. So we propose to leverage a pre-trained model to perform one-time feature embedding on raw data, and we use a lightweight neural network, called proxy estimator, to directly predict informativeness based on embeddings. Then the data selection cost formula is rewritten as follows:

$$
\text { Cost } = \text { Embed } \times \text { Sample } \# \times 1 + \text { Simplify(Measure) } \times \text { Sample } \# \times \text { Round } \#.
$$

This one-time extraction design can save the time cost of repetitive and redundant feature embedding from Embed×Sample#×Round# to Embed × Sample# × 1. Similarly, by directly predicting informativeness, the computational complexity of strategies with $O ( n ^ { 2 } )$ 号 measurement can be reduced to $O ( n )$ . We denote this reduction as ???????????? ?? ??(·). These savings in data selection overhead can effectively save end-to-end time costs (see Sec. 6.5).

With the estimation result of the proxy estimator, we select a subset of samples with the highest predicted informativeness for annotation and updating the task model. The training and updating of the proxy estimator rely on the supervision of the target informativeness calculated by the task model (see Sec. 4.2).

• Direct informativeness prediction reduces computational complexity. Given ?? unlabeled samples in an iteration, existing active learning strategies require either ?? (??) or $O ( n ^ { 2 } )$ informativeness measurement operations. Prediction-based strategies (e.g., confidence-based [23, 25] and loss-based [39, 47]) require ?? (??) operations. Informativeness measurement in clustering-based strategies [6, 29] and KNN-based strategies [28, 31] has a computational complexity of $O ( n ^ { 2 } )$ . Our design of directly predicting informativeness reduces this complexity from $O ( n ^ { 2 } )$ to ?? (??) in each iteration, where ?? is the number of samples. This reduction exists during each round of data selection.

Table 1: Comparison of our proposed ProxySampler with ablation methods and efficient AL methods $\left( q < 1 \right)$ . 

<table><tr><td></td><td>Compute Complex.</td><td>Light. Esti.</td><td>Reduced Candi.</td><td>Direct Res.</td></tr><tr><td>Prediction-based AL</td><td> $n$ </td><td>✕</td><td>✕</td><td>✕</td></tr><tr><td>Clustering-based AL</td><td> $n^{2}$ </td><td>✕</td><td>✕</td><td>✕</td></tr><tr><td>SVP [5]/ASVP [44]</td><td> $n / n^{2}$ </td><td>✕</td><td>✕</td><td>✕</td></tr><tr><td>AL+Proxy</td><td> $n$ </td><td>✕</td><td>✕</td><td>✕</td></tr><tr><td>AL+Proxy+Pooling (AL+PROXYSAMPLER)</td><td> $qn$ </td><td>✕</td><td>✕</td><td>✕</td></tr></table>

• Sample pooling: observed changes in informativeness. Correspondingly, for the Sample# factor, we design a sample pooling module to narrow down sample candidates for informativeness estimation. It can further narrow the sample candidates scale down to ????, where ?? is a constant less than 1. To discover opportunities to reduce sample candidates, we explored the informativeness changes between two consecutive rounds. We did experiments on a text-based emotion recognition task [34] using 6809 samples. We plot the informativeness changes between two iterations in Fig. 5. We first sort the samples in descending order of their informativeness in the second round, as shown by the red line. To display the changes in informativeness, we draw 100 samples with the highest informativeness in Fig. 5a and 100 samples with the lowest informativeness in Fig. 5b. The blue line represents the informativeness of the corresponding samples in the 3rd round. We can see that the high-informativeness samples change greatly in the next round, while the low-informativeness samples remain stable.

Therefore, our sample pooling module filters out samples that have low predicted informativeness in the previous round. It narrows the sample candidates for the proxy estimator to predict, thus further reducing the overall data selection cost. Determining the specific number of samples selected for informativeness estimation involves many configurations, such as annotation and training time costs. We will introduce detailed designs in Sec. 5.1.

The cost of informativeness estimation is influenced by the number of task model parameters (we need a lightweight estimation process, denoted as “Light. Esti.”), the number of sample candidates (we aim to reduce candidates, denoted as “Reduced Candi.” ), and the necessity for post-calculation based on the model output (we want to directly get the estimation results, denoted as “Direct Res.”). Our proxy estimator enables lightweight estimation and can directly get the informativeness estimation results. Our design of sample pooling enables reduced sample candidate numbers for efficient data selection. Tab. 1 compares the effects of our designs with existing AL strategies and existing efficient AL works [5, 44].

# 4 Proxy Estimator

This section first studies the feasibility of directly learning informativeness based on computational learning theory (§ 4.1). Then we introduce detailed designs of our proxy estimator module (§ 4.2).

# 4.1 Feasibility Analysis

• Feasibility definition. Although our empirical analysis indicates that using a proxy estimator to predict informativeness is promising, it remains unclear whether this approach is theoretically feasible. In other words, beyond empirical effectiveness, we need a principled criterion to judge whether informativeness can be learned in a simpler way through proxy estimation. Following the previous work [48], we introduce the concept of feasibility for proxy estimation. We say that: the proxy estimation is feasible if the hypothesis complexity of the proxy estimator is lower than that of the original informativeness estimation. Here, hypothesis complexity can be measured in terms of standard complexity measures in computational learning theory [2] (e.g., Rademacher complexity [18]). This definition captures the intuition that if the proxy estimator requires a strictly simpler hypothesis class, then learning informativeness through the proxy estimator is more efficient.

![](images/5615e3d43a9de3a69ad85415ba6f924e9f1753c1f4268d1feddb3007c23bd803.jpg)



Figure 6: Illustration of proxy informativeness estimation task.

To formally prove the feasibility of the learning informativeness directly, we need to make the following problem definition. Let ?? and ?? denote the input and output space of the task model, respectively. Let $h : X \to Y$ denote the task model. We define $c : Y  I$ as the informativeness measurement that maps the task model’s output to informativeness. Then, the original informativeness estimation task can be formulated as ?? (ℎ(??)). For different active learning cases, $h ( x ) \ ( \mathrm { i . e . , } y )$ has a different strategy-specific representation. For example, in the least confidence active learning strategies, ?? represents the output confidence of the task model. As for loss-prediction active learning strategies [47], ?? represents the intermediate features of the task model. Our proxy estimator aims to directly map the input to informativeness, denoted by $p : X  I .$ . The learning target can be formulated as a composite function: ?? ◦ℎ. Fig. 6 illustrates the relation between our proxy informativeness estimation task and the original informativeness estimation.

In our analysis, we use Rademacher Complexity [18] as the complexity measure for a hypothesis family. Rademacher complexity quantifies the richness of a class of real-valued functions concerning a specified probability distribution, which is defined by:

Definition 4.1 (Empirical Rademacher Complexity). Let ?? be a family of functions mapping from ?? to [??, ??] and $S = ( z _ { 1 } , z _ { 2 } , \dots , z _ { m } )$ a fixed sample of size ?? with elements in ?? . Then, the empirical Rademacher complexity of ?? w.r.t. the sample ?? is defined as [30]:

$$
\widetilde {\mathcal {R}} _ {S} (G) = \mathbb {E} _ {\sigma} \left[ \sup _ {g \in G} \frac {1}{m} \sum_ {i = 1} ^ {m} \sigma_ {i} g (z _ {i}) \right], \tag {2}
$$

where $\boldsymbol { \sigma } = ( \sigma _ { 1 } , \sigma _ { 2 } , \ldots , \sigma _ { m } ) ^ { T }$ , with ???? is indenpendent uniform random variables taking values in $\{ - 1 , + 1 \}$ . The random variables ???? are called Rademacher variables.

• Feasibility proof. Following typical active learning setting [37], we consider a multi-class classification task model and we adopt the least confidence [24] for informativeness measurement. Let $\mathcal { F } _ { 1 } \ldots \mathcal { F } _ { l }$ denote a set of ?? hypothesis in $\mathbb { R } ^ { X }$ , Then, the hypothesis

![](images/74c387553c3d5ec70ccf1e87c34898e29888becefae6ce0e87fd30713cffa563.jpg)



![](images/b14ba3407853f6437deb0c0adb3311162f39ae52978933b5ef4157c275d52368.jpg)



Figure 7: Performance comparison of the proxy estimator between using the ML model and the neural network model.

family of the origin informativeness estimation task is defined by:

$$
\mathcal {H} = \left\{h _ {1} + \dots + h _ {l}: h _ {i} \in \mathcal {F} _ {i}, i \in [ 1, l ] \right\}, l \geq 2. \tag {3}
$$

For the least confidence active strategy, the proxy estimator directly learns the maximum confidence value of the task model’s output. Then the hypothesis family of the proxy task is defined by:

$$
\mathcal {P} = \left\{\max \left\{h _ {1}, \dots , h _ {l} \right\}: h _ {i} \in \mathcal {F} _ {i}, i \in [ 1, l ] \right\}, l \geq 2. \tag {4}
$$

According to the formulas of P and H above, we have the following lemma:

Lemma 4.2 (Proxy Estimator Feasibility). For the multi-class classification task model and least confidence active learning strategy, using a proxy estimator is feasible, formally:

$$
\widetilde {\mathcal {R}} _ {S} (\mathcal {P}) \leq \widetilde {\mathcal {R}} _ {S} (\mathcal {H}) \tag {5}
$$

Proof.

$$
\widetilde {\mathcal {R}} _ {S} (\mathcal {H}) = \mathbb {E} _ {\sigma} \left[ \sup _ {h _ {i} \in \mathcal {F} _ {i}} \frac {1}{m} \sum_ {i = 1} ^ {m} \sigma_ {i} \left\{h _ {1} (x _ {i}) + \dots + h _ {l} (x _ {i}) \right\} \right] \tag {6}
$$

$$
= \sum_ {j = 1} ^ {l} \mathbb {E} _ {\sigma} \left[ \sup _ {h _ {j} \in \mathcal {F} _ {j}} \frac {1}{m} \sum_ {i = 1} ^ {m} \sigma_ {i} h _ {1} (x _ {i}) \right] = \sum_ {j = 1} ^ {l} \widetilde {\mathcal {R}} _ {S} (\mathcal {F} _ {j}). \tag {7}
$$

The Eq.7 holds because sup(??+??) = sup ??+sup ?? if $A + B = \left\{ a + b \ \right|$ $a \in A , b \in B \}$ . According to an existing theorem [30], we have:

$$
\widetilde {\mathcal {R}} _ {S} (\mathcal {G}) \leq \sum_ {j = 1} ^ {l} \widetilde {\mathcal {R}} _ {S} (\mathcal {F} _ {j}),
$$

Where $\mathcal { G } = \{ m a x \left\{ h _ { 1 } , \ldots , h _ { l } \right\} : h _ { i } \in \mathcal { F } _ { i } , i \in [ 1 , l ] \} .$

Therefore,

$$
\widetilde {\mathcal {R}} _ {S} (\mathcal {P}) \leq \sum_ {j = 1} ^ {l} \widetilde {\mathcal {R}} _ {S} (\mathcal {F} _ {j}) = \widetilde {\mathcal {R}} _ {S} (\mathcal {H}).
$$

The above lemma indicates that directly estimating informativeness would simplify the original informativeness measurement task. Therefore, our proposed new idea is theoretically feasible.

# 4.2 Informativeness Learning

• One-time embedding and lightweight measurement. During the iterative AL process, the same sample requires redundant reembedding for informativeness re-estimation in each round of data selection. By analyzing the cost formula, we conducted experiments and found that a lightweight neural network can directly learn the informativeness measurement using pre-trained embeddings. Therefore, we propose to use a pre-trained model to perform onetime feature embedding offline to reduce the unit embedding cost from Embed × Round# to Embed × 1. We further reduce the unit measuring cost by employing a lightweight neural network (proxy estimator) to directly predict informativeness. For the iterative data selection process in AL, we only need to run the lightweight proxy estimator on stored embedding data in each round.

![](images/902cda21c1442b5f9a2cf22a04cde667e5c900bc8dff08742c10fe7f21cf841f.jpg)



Figure 8: Illustration of active learning with three pipelines and without pipelining.

• Update of the proxy estimator. The task model is updated in each round of active learning. Its informativeness of samples will change, so the proxy estimator also needs to be updated. We propose to maintain an appropriately sized 1 validation dataset for proxy estimator updates. Note that the ground truth (target informativeness) of the validation dataset used to train the proxy estimator is computed by the task model. Therefore, it does not introduce additional manual labeling costs. After getting the labeled data $L _ { n }$ in round ??, we first train the task model $M _ { n }$ on $L _ { n } .$ Next, we use the updated task model $M _ { n + 1 }$ to calculate the target informativeness on the validation dataset. Then, we use the new target informativeness to update the proxy estimator. Note that although the validation set introduces constant times of task model inference operations, our proxy estimator still uniformly reduces the complexity associated with ?? down to ?? (??).

• Architecture of the proxy estimator. We want the proxy estimator to be lightweight. We empirically tried the traditional machine learning (ML) models, such as the linear regression model and support vector machine (SVM), on the topic classification task with the BADGE strategy. We show the training loss and MAE (mean average error) using different ML models as proxy estimators in Fig. 7. We can see that the linear regression model and the SVM model cannot fit the training set. We analyze that it is because the input of the proxy estimator is the embeddings extracted by the pre-trained model, which is static. However, the informativeness of each sample changes dynamically. Therefore, it is difficult for traditional ML models to learn the complex mapping relationship. Fortunately, previous research [47] shows that the training loss of a sample can be predicted using a lightweight neural network model attached to the task model. So we try to exploit the neural network to learn informativeness as shown by the red lines in Fig. 7. We can see that the neural network model can learn informativeness. Thus, our proxy estimator uses the neural network to learn the informativeness directly. We further experimentally verify the effectiveness of the proxy estimator in Fig. 3 and Fig. 10. For details of the proxy estimator architecture, please refer to Sec. 6.

# 5 Sample Pooling

# 5.1 Narrowing Sample Candidates

• Informativeness-guided pooling. Based on the observation that low-informativeness samples remain low-informativeness in the next round while high-informativeness samples do the opposite, we propose to narrow the sample candidates by no longer performing redundant estimation on low-informativeness samples at each iteration. Specifically, in each round of active learning, we drop out a $( 1 - q )$ ratio of samples with the lowest informativeness, where $0 < q \leq 1$ . Our experimental results show that discarding these low-information samples can further improve efficiency (34-45% improvement compared to only using the proxy estimator) without compromising the learning performance. Formally, given ?? unlabelled samples, the number of samples our proxy estimator needs to predict in round ?? is $N q ^ { \mathrm { m i n } ( n , N _ { 0 } ) }$ , where ??0 is an empirically pre-defined constant (e.g., 10 ∼ 30 for 400,000 samples in our experiments) for the maximum number of rounds for our pooling operations. The setting of $N _ { 0 }$ is to avoid too few sample candidates, as it can lead to a significant degradation in learning performance.

• Determining ??. The principle for determining ?? comes from the advantage of our ProxySampler: it enables pipelining. For the vanilla active learning methods, the next-round data selection must wait for the completion of task model training. This dependency disables job overlapping and causes stalls. Our proxy estimator removes the data selection’s dependency on the task model, therefore, ProxySampler supports pipelining. Fig. 8 illustrates the comparison of active learning with and without pipelining. To fully utilize pipelines, it is optimal to have a balanced workload among stages in the pipeline [12]. Therefore, we determine the value of ?? according to the following equation:

$$
q = \min \left(1, \sqrt [ N _ {0} ]{\frac {K T _ {a} + n K T _ {t}}{N T _ {e}}}\right), \tag {8}
$$

where ?? is the number of samples selected to label in each round, $T _ { a } , T _ { t } , T _ { e }$ denote the unit time cost of annotation, training, and proxy estimator prediction for one sample. This equation is derived by making the data selection time equal to the labeling plus training:

$$
\text { For   round } n, \underbrace {T _ {e} N q ^ {\min (n , N _ {0})}} _ {\text { Data   Selection }} = \underbrace {K T _ {a}} _ {\text { Manual   Labeling }} + \underbrace {n K T _ {t}} _ {\text { Training }}.
$$

Using this equation and the $q \leq 1$ condition, we can derive Eq. 8.

• Sample pooling in pipelines. For ?? -parallel pipelining, in round ??, we divide the sample candidates into ?? parts, denoted as $U _ { n } ^ { w } , w \in [ 1 , W ]$ . Then, we use the proxy estimator ???????????? to predict informativeness on $U _ { n } ^ { w }$ and get their informativeness estimation results, denoted as $P ^ { w }$ . For each pipeline, we select top-$( K / W )$ highest informativeness samples for manual labeling. These samples will be added to the labeled dataset. At the same time, the $\big ( ( 1 - q ) N q ^ { \mathrm { m i n } ( n , N _ { 0 } ) } \big ) / W$ samples with the lowest predicted informativeness are selected to drop out.

# 6 Experiments

# 6.1 Experiment Setup

6.1.1 Datasets. We evaluate ProxySampler on both the public datasets and the real campus video analysis system. The evaluation contains 3 different datasets involving 3 different tasks and two modalities. (1) Emotion [34], a dataset designed for text-based emotion recognition on Twitter, consists of 416,809 data with six emotion labels. We randomly split the dataset into 400,000 for training, 10,000 for validation, and 6,809 for testing. (2) Campus-Reid, an image dataset for re-identification task. The original data from video frames consists of 2422 images involving 215 people. We leverage this data to construct a dataset containing 94,976 pairs. We randomly divide the dataset into 84,976 for training, 3,000 for validation, and 7,000 for testing. (3) AGnews [54], a dataset for the news topic classification task. We randomly split 1000 news items from the training dataset for validation. Therefore, we use 119,000 for training, 1000 for validation, and 7,600 for testing.

![](images/e560a215763417f4563ac999da2213deba0dfb4da6ffba3c26aa6f139cebd2cd.jpg)



(a) Emotions Recognition

![](images/197a0c8d80d2ebdaf9bec86ca7b7e8e659cbf195917c70c0ba14c8bbc210a73d.jpg)



(b) Topic Classification

![](images/d949119b5a8ff97c24d4f531bb344e2405196fb19f23c05cf7753c14dd3a1dbd.jpg)



(c) Re-Identification

Figure 9: Performance of the task model integrated with ProxySampler compared to other state-of-the-art efficient active learning on different tasks using different strategies under different time budgets.   
![](images/e6447e074e897726038292edbe0b490530dc89dbcae637fa946d59f5705007f2.jpg)



(a) Top-100 recall.

![](images/21c8b5ed448995f203a558e11eebb9591b0f1d8f37af44798c499549f5070f8f.jpg)



(b) Top-50% recall.   
Figure 10: Top-K recall in the proxy estimator predictions for the emotion recognition task with Conf. strategy.

6.1.2 Baselines. We compare the performance of ProxySampler integrated with four active learning approaches with existing baselines of efficient active learning approaches.

(1) Active learning approaches. We integrate ProxySampler with four active learning approaches as baselines, one classic AL method, and three recent approaches. (a) Conf. [24]: The confidencebased strategy selects samples with the lowest prediction confidence; (b) BADGE [3]: It uses clustering techniques on gradient embeddings to group similar samples together. Then, it selects samples farthest from their centroid. (c) CAL [28]: It selects samples with the highest mean divergence, focusing on those whose predictive probability significantly differs from their ?? neighbors in the labeled dataset. (d) CounterAL [6]: It first selects partial samples with the highest variability as candidates. Then it selects samples from the candidates nearest to the centroid of each cluster.   
(2) Efficient active learning approaches. We compare the performance of integrating with ProxySampler and the other two

![](images/b08755cb5de327d19cf3a5ab56934c4c7ed830194b3da6ca7bc1cf0aa32d4bf3.jpg)



(a) Emotion recognition task with CAL strategy.

![](images/b46962f45fe21fb305fb372200a0b033551ed4b08820adffbd7b87e85a37bc09.jpg)



(b) Re-identification task with Conf. strategy.   
Figure 11: Time cost profiling of model update, proxy estimator update, and data selection on different tasks.

Table 2: The end-to-end time cost given the same task accuracy threshold. The speed-up is in bold. 

<table><tr><td colspan="5">Emotion Recognition</td></tr><tr><td>Acc. (%)</td><td>60</td><td>70</td><td>75</td><td>80</td></tr><tr><td>CAL (min)</td><td>373</td><td>668</td><td>742</td><td>965</td></tr><tr><td>SVP (min)</td><td>248</td><td>442</td><td>557</td><td>806</td></tr><tr><td>ASVP (min)</td><td>225</td><td>335</td><td>450</td><td>733</td></tr><tr><td>CAL+PROXYSAMPLER (min)</td><td>49</td><td>73</td><td>85</td><td>122</td></tr><tr><td>Speed-up</td><td>4.59</td><td>4.58</td><td>5.29</td><td>6.01</td></tr></table>

efficient active learning approaches. (a) SVP [5]: It removes hidden layers from the target model, using smaller architectures and training for fewer epochs to provide signals for data selection. (b) ASVP [44]: It maintains the alignment between the pre-trained feature and the task model during the fine-tuning.

6.1.3 Evaluation methodology and metrics. It is crucial for data analysis services to update the task model efficiently. We utilize task model accuracy and end-to-end time as evaluation metrics. It is important to note that ProxySampler focuses on accelerating the data selection process. It can be integrated with various active learning approaches as a plug-in. Therefore, the baselines include the original active learning approach without using ProxySampler and other existing efficient active learning studies. We compare task model accuracy under different labeling time budgets.   
6.1.4 Implementation details. We implemented ProxySampler in Python 3.7 using TensorFlow 2.4, and our code is available here 2.

![](images/b400467a125d85a1536145ce5188a031b4953c1b85be094be3cc9df6c2f82edb.jpg)



(a) Re-identification task.

![](images/520d2e5f014f059c26dece15dae66b57a3131249829d096357aff11be44af8cd.jpg)



(b) Emotion recognition task.   
Figure 12: Analysis of ?? and validation dataset size.

For all datasets, we randomly select 50 samples as labeled data to start with and add 50 samples in each AL round. Based on the experience from previous works [40, 47], the width and depth of the additional neural network model do not have a significant impact on the prediction of sample training loss. So we uniformly use a small number of dense layers for the proxy estimator. For text tasks, the layer dimensions are 128, 64, 32, and 1, respectively; for image tasks, two 1024-d vectors are concatenated and passed through layers of 1024, 256, 128, and 1, respectively. For task models, we use BERT [19]/ RoBERTa [27]/ GPT2 [33] for text-based tasks and MobileNet [13] for image-based tasks. For all experiments, we use a server that runs Ubuntu 16.04.5 with one NVIDIA Tesla P100 GPU and 12 Intel Xeon CPUs.

# 6.2 Overall Performance Comparison

6.2.1 Overall performance of the task model. In order to explore the gain in accuracy that comes from integrating the ProxySampler, we draw the accuracy of the task model with and without ProxySampler under different time budgets. We also compare ProxySampler with SOTA studies on efficient active learning. Fig. 9 shows the accuracy of three active learning strategies (Conf., CAL, Counter.) integrated with the ProxySampler on Emotion and Campus-Reid datasets under different end-to-end time budgets. The manual labeling time in the experiment was simulated using the test results of five student volunteers. Experimental results show that integrating the ProxySampler can make the task model have significant performance improvement on both tasks. Specifically, for the emotion recognition task with the Conf. strategy, with the 180-minute budget, integrating ProxySampler can achieve 80% accuracy, which is 13% higher than the Conf. baseline. These results show that the integration of ProxySampler effectively improves the accuracy gain of the task model and demonstrates the general applicability of ProxySampler to various active learning strategies.

6.2.2 Overall time speed-up. On the other hand, to better explore the performance gains brought by the ProxySampler, we report the end-to-end time cost and speedup with the ProxySampler to achieve different task model accuracy thresholds with different strategies on different tasks. Table 2 illustrates that integrating ProxySampler can provide speedups of 2.15-6.01 × on all baselines for all accuracy thresholds. For example, to achieve an 80% accuracy threshold in the emotion recognition task with the CAL strategy, the SOTA baseline requires 733 minutes, while integrating ProxySampler only needs 122 minutes, resulting in a 6.01× speedup and saving 83.3% in time costs. The acceleration results show that our ProxySampler design can effectively accelerate the end-to-end

![](images/a10add7a9e614969a65ed0f0f7397f875869cad553acc58ebdd1e0d7cb246999.jpg)



(a) Overall performance under different time budgets.

![](images/21ab8245d5e2c4202bfca73636b6e8633dec5dd4214bc5d234025cb2d7354a37.jpg)  
(b) Time profiling of end-to-end time cost (86% task accuracy).   
Figure 13: The impact of using different feature extractors on integrating ProxySampler with the BADGE strategy for the topic classification task.

time of active learning in large-scale scenarios to better support data analytics applications. This also verifies the effectiveness of our cost modeling analysis for data selection.

# 6.3 Effectiveness of the proxy estimator

6.3.1 Estimation consistency for high-informativeness samples. In the data selection process, we select the highest predicted informativeness samples by proxy estimator for manual labeling. To evaluate whether the proxy estimator can also predict target highinformativeness samples as high-informativeness, we trained the proxy estimator on 2000 samples and tested it on 6809 samples. We compared the predicted informativeness distributions on two groups: (1) top target-informativeness samples (top 100 and top 50%) and (2) all test samples. As shown in Fig. 10a and Fig. 10b, the orange histogram (group 1) is skewed toward the higher part of the blue histogram (group 2), indicating that the proxy estimator assigns higher predicted informativeness to truly informative samples. In particular, it successfully recalls 76% of the top-50% target-informativeness samples. This consistency shows that the proxy estimator can effectively identify high-informativeness samples at significantly reduced computational cost.

6.3.2 Lightweightness of proxy estimator. To show the lightweightness of our proxy estimator design, we report the time costs of updating the proxy estimator and running the proxy estimator for data selection in Fig 11. As a reference, we also report the costs of training the task model. For emotion recognition and reidentification tasks, we set the target accuracy of the task model as 86% and 66%, respectively. Experimental results show that our proxy estimator only takes 648/232 seconds for these two tasks, which is only 19.4%/7.8% of the time for updating the task model. These results show that our proxy estimator design can greatly trade-off learning performance and time overhead in active learning. It effectively replaces the role of the high-cost task model in the original informativeness estimation process.

# 6.4 Hyperparameter Analysis

6.4.1 Hyperparameter ??. To verify the impact of different ?? on time efficiency, we verified the trade-off between time cost and task accuracy under different ??. In Fig 12a, we set $q = \{ 0 . 0 1 , 0 . 0 5 , 0 . 1 , 0 . 2 \}$ in the re-identification task with the Conf. strategy. We plot the result of the same configuration without using the sample pooling method, denoted as the black line for comparison. We can conclude that removing the low-informativeness samples can reduce the overall time cost when achieving the target task accuracy.

![](images/47182a6c593d1e1b9efdc1685d94e3f4b6e51a1507f57ca9bfe255d94d9eeff7.jpg)



(a) Emotions Recognition

![](images/842fc009da1b22faa8c62b738026bf0d8b729f4a7ac12bc37ebd0ed5bf208abe.jpg)



(b) Emotions Recognition

![](images/dddf7476293210e9a9a477f3f0c0363864c140a3fe652d6936f635295cb6d311.jpg)



(c) Re-Identification

![](images/f3d69ded0f1fbc823c72524b019e13dad4c1f5f413539f834bce5a59b95d0a2c.jpg)



(d) Re-Identification   
Figure 14: Ablation study by comparing task model accuracy on different tasks with and without the proxy estimator module and the sample pooling module.

6.4.2 Impact of different feature extractors. To demonstrate the impact of using different feature extractors on the proxy estimator, we show the overall performance of integrating the ProxySampler with the BADGE strategy under different time budgets on the AG news dataset using BERT [19]/ RoBERTa [27]/ GPT2 [33] as the feature extractor in Fig 13a. Achieving 86% accuracy takes 136/126/116 minutes with BERT/GPT2/RoBERTa, showing a time-saving variation within 7.3%. This suggests ProxySampler’s effectiveness is robust across different extractors. To further study the impact of using different feature extractors on the end-to-end time cost, we illustrate the time profiling of using the BADGE strategy on the topic classification task in Fig. 13b. The end-to-end time cost consists of manual labeling (“Manual”), data selection (“Select”), and task model update (“Training”). Although the selection of extractors has a slight impact on the total time, they all significantly reduce the selection time, reducing the end-to-end cost by 50.9%–58.2%.

6.4.3 Hyperparameter size of validation dataset. To verify the impact of the size of the validation dataset on the overall time cost, we explored the overall time cost of the emotion recognition task using the Conf. strategy under different sizes of validation datasets in Fig 12b. We set ??????\_???????? = {1000, 3000, 5000, 7000, 9000} for comparison. We can see that the size of the validation dataset does not have much impact on the end-to-end time cost. This is because the additional time required for the validation dataset is small, accounting for only about 4.5% of the overall time cost.

# 6.5 Ablation Study

6.5.1 Removing the proxy estimator. Removing the proxy estimator from ProxySampler only activates the sample pooling module (orange line in Fig. 14). Experiments show that the proxy estimator significantly accelerates the process of reaching the target accuracy. For instance, in the emotion recognition task with CAL, achieving 80% accuracy takes 329 minutes without the estimator, but only 122 minutes with it—a 2.7× speedup (62.9% time saved). This demonstrates that the proxy estimator notably improves overall efficiency by accelerating data selection.

6.5.2 Removing the sample pooling module. Removing the sample pooling module from the ProxySampler results in only the proxy estimator module being active (blue line in Fig. 14). Comparisons on two tasks show that this leads to notable performance drops. In the re-identification task with the Conf. strategy, reaching 65% accuracy

takes 213 minutes without sample pooling, whereas integrating with the ProxySampler takes 140 minutes, saving 34.3% of the overall time cost. This shows that narrowing candidate samples via sample pooling effectively reduces overall time by 34.3–45%.

The proxy estimator and sample pooling can function independently or jointly to further reduce time and cost in large-scale AL.

# 7 Discussion

Dependence on pre-training. Most existing AL methods [36, 38] rely on pre-trained models, assuming that the distribution of pretraining data is consistent with the target data. This dependency implicitly introduces additional information from the pre-training corpus. However, the effectiveness of these methods decreases when there is a significant distribution gap between the pre-training data and the current task. [53]. Mitigating this dependence on pretraining while still ensuring effective informativeness estimation remains an important direction for future research.

Backbone network size. In our approach, the absolute runtime of ProxySampler inevitably increases with the size of the backbone network model. However, as the size of the backbone network increases, the relative optimization gain achieved by ProxySampler over the original pipeline will also be larger. In ultra-large-scale settings with strict latency constraints, scaling down the backbone might be necessary. However, this may hinder the effectiveness of learning informativeness, resulting in performance degradation. Therefore, for large-scale resource-constrained scenarios, it is crucial to balance the efficiency of the backbone network and the effectiveness of learning informativeness.

# 8 Conclusion

This paper identified that the time overhead in large-scale active learning is bottlenecked by the data selection process. We presented ProxySampler, a general informativeness estimation framework for efficient data selection in active learning. In future work, we plan to extend it to speech data, graph-structured inputs, and scenarios with extreme class imbalance.

# Acknowledgments

This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 62441228, Science and Technology Tackling Program of Anhui Province, No.202423k09020016.

# GenAI Usage Disclosure

Following ACM’s Authorship Policy and ACM policies, in this paper, we did not use GenAI to generate text, code, data, tables, or images.

# References

[1] Naoki Abe, Bianca Zadrozny, and John Langford. 2006. Outlier detection by active learning. In Proceedings of the 12th ACM SIGKDD international conference on Knowledge discovery and data mining. 504–509.   
[2] Martin HG Anthony and Norman Biggs. 1997. Computational learning theory. (1997).   
[3] Jordan T Ash, Chicheng Zhang, Akshay Krishnamurthy, John Langford, and Alekh Agarwal. 2019. Deep Batch Active Learning by Diverse, Uncertain Gradient Lower Bounds. In International Conference on Learning Representations.   
[4] Lucas Beyer, Pavel Izmailov, Alexander Kolesnikov, Mathilde Caron, Simon Kornblith, Xiaohua Zhai, Matthias Minderer, Michael Tschannen, Ibrahim Alabdulmohsin, and Filip Pavetic. 2023. Flexivit: One model for all patch sizes. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 14496–14506.   
[5] Cody Coleman, Christopher Yeh, Stephen Mussmann, Baharan Mirzasoleiman, Peter Bailis, Percy Liang, Jure Leskovec, and Matei Zaharia. [n. d.]. Selection via Proxy: Efficient Data Selection for Deep Learning. In International Conference on Learning Representations.   
[6] Xun Deng, Wenjie Wang, Fuli Feng, Hanwang Zhang, Xiangnan He, and Yong Liao. 2023. Counterfactual active learning for out-of-distribution generalization. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 11362–11377.   
[7] Liat Ein Dor, Alon Halfon, Ariel Gera, Eyal Shnarch, Lena Dankin, Leshem Choshen, Marina Danilevsky, Ranit Aharonov, Yoav Katz, and Noam Slonim. 2020. Active learning for BERT: an empirical study. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP). 7949– 7962.   
[8] Talfan Evans, Nikhil Parthasarathy, Hamza Merzic, and Olivier J Henaff. 2024. Data curation via joint example selection further accelerates multimodal learning. arXiv preprint arXiv:2406.17711 (2024).   
[9] Talfan Evans, Shreya Pathak, Hamza Merzic, Jonathan Schwarz, Ryutaro Tanno, and Olivier J Henaff. 2023. Bad students make great teachers: Active learning accelerates large-scale visual understanding. arXiv preprint arXiv:2312.05328 (2023).   
[10] Abolfazl Farahani, Sahar Voghoei, Khaled Rasheed, and Hamid R Arabnia. 2021. A brief review of domain adaptation. Advances in data science and information engineering: proceedings from ICDATA 2020 and IKE 2020 (2021), 877–894.   
[11] Weijie Fu, Meng Wang, Shijie Hao, and Xindong Wu. 2018. Scalable active learning by approximated error reduction. In Proceedings of the 24th ACM SIGKDD international conference on knowledge discovery & data mining. 1396–1405.   
[12] John L Hennessy and David A Patterson. 2011. Computer architecture: a quantitative approach. Elsevier.   
[13] Andrew G Howard. 2017. Mobilenets: Efficient convolutional neural networks for mobile vision applications. arXiv preprint arXiv:1704.04861 (2017).   
[14] Kevin Hsieh, Ganesh Ananthanarayanan, Peter Bodik, Shivaram Venkataraman, Paramvir Bahl, Matthai Philipose, Phillip B Gibbons, and Onur Mutlu. 2018. Focus: Querying large video datasets with low latency and low cost. In 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18). 269–286.   
[15] Sheng-Jun Huang, Rong Jin, and Zhi-Hua Zhou. 2010. Active learning by querying informative and representative examples. Advances in neural information processing systems 23 (2010).   
[16] Daniel Kang, Peter Bailis, and Matei Zaharia. [n. d.]. BlazeIt: Optimizing Declarative Aggregation and Limit Queries for Neural Network-Based Video Analytics. Proceedings of the VLDB Endowment 13, 4 ([n. d.]).   
[17] Daniel Kang, John Emmons, Firas Abuzaid, Peter Bailis, and Matei Zaharia. 2017. NoScope: Optimizing Neural Network Queries over Video at Scale. Proceedings of the VLDB Endowment 10, 11 (2017).   
[18] Michael J Kearns and Umesh Vazirani. 1994. An introduction to computational learning theory. MIT press.   
[19] Jacob Devlin Ming-Wei Chang Kenton and Lee Kristina Toutanova. 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In Proceedings of NAACL-HLT. 4171–4186.   
[20] Yeachan Kim and Bonggun Shin. 2022. In Defense of Core-set: A Density-aware Core-set Selection for Active Learning. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 804–812.   
[21] Ksenia Konyushkova, Raphael Sznitman, and Pascal Fua. 2017. Learning active learning from data. Advances in neural information processing systems 30 (2017).   
[22] Hyunsung Lee, Sungwook Yoo, Dongjun Lee, and Jaekwang Kim. 2023. How Important is Periodic Model update in Recommender System?. In Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval. 2661–2668.

[23] David D Lewis. 1995. A sequential algorithm for training text classifiers: Corrigendum and additional data. In Acm Sigir Forum, Vol. 29. ACM New York, NY, USA, 13–19.   
[24] David D Lewis and William A Gale. [n. d.]. A Sequential Algorithm for Training Text Classifiers. In SIGIR’94: Proceedings of the Seventeenth Annual International ACM-SIGIR Conference on Research and Development in Information Retrieval, organised by Dublin City University. Springer, 3–12.   
[25] Mingkun Li and Ishwar K Sethi. 2006. Confidence-based active learning. IEEE transactions on pattern analysis and machine intelligence 28, 8 (2006), 1251–1261.   
[26] Yanghao Li, Haoqi Fan, Ronghang Hu, Christoph Feichtenhofer, and Kaiming He. 2023. Scaling language-image pre-training via masking. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 23390–23400.   
[27] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. Roberta: A robustly optimized bert pretraining approach. arXiv preprint arXiv:1907.11692 (2019).   
[28] Katerina Margatina, Giorgos Vernikos, Loïc Barrault, and Nikolaos Aletras. 2021. Active Learning by Acquiring Contrastive Examples. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing. 650–663.   
[29] Steven McElwee. 2017. Active learning intrusion detection using k-means clustering selection. In SoutheastCon 2017. IEEE, 1–7.   
[30] Mehryar Mohri, Afshin Rostamizadeh, and Ameet Talwalkar. 2018. Foundations of machine learning. MIT press.   
[31] Daniel Carlos Guimarães Pedronette, Ying Weng, Alexandro Baldassin, and Chaohuan Hou. 2019. Semi-supervised and active learning through manifold reciprocal kNN graph for image retrieval. Neurocomputing 340 (2019), 19–31.   
[32] Fengchao Peng, Chao Wang, Jianzhuang Liu, and Zhen Yang. 2021. Active learning for lane detection: A knowledge distillation approach. In Proceedings of the IEEE/CVF International Conference on Computer Vision. 15152–15161.   
[33] Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. 2019. Language Models are Unsupervised Multitask Learners. (2019).   
[34] Elvis Saravia, Hsien-Chi Toby Liu, Yen-Hao Huang, Junlin Wu, and Yi-Shin Chen. 2018. Carer: Contextualized affect representations for emotion recognition. In Proceedings of the 2018 conference on empirical methods in natural language processing. 3687–3697.   
[35] Tobias Scheffer, Christian Decomain, and Stefan Wrobel. 2001. Active hidden markov models for information extraction. In International symposium on intelligent data analysis. Springer, 309–318.   
[36] Christopher Schröder and Gerhard Heyer. 2024. Self-Training for Sample-Efficient Active Learning for Text Classification with Pre-Trained Language Models. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing. 11987–12004.   
[37] Burr Settles. 2009. Active learning literature survey. (2009).   
[38] Artem Shelmanov, Vadim Liventsev, Danil Kireev, Nikita Khromov, Alexander Panchenko, Irina Fedulova, and Dmitry V Dylov. 2019. Active learning with deep pre-trained models for sequence tagging of clinical and biomedical texts. In 2019 IEEE international conference on bioinformatics and biomedicine (BIBM). IEEE, 482–489.   
[39] Megh Shukla and Shuaib Ahmed. 2021. A mathematical analysis of learning loss for active learning in regression. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 3320–3328.   
[40] Miao-Hui Song, Lan Zhang, Mu Yuan, Zichong Li, Qi Song, Yijun Liu, and Guidong Zheng. 2023. CoTel: Ontology-Neural Co-Enhanced Text Labeling. In Proceedings of the ACM Web Conference 2023. 1897–1906.   
[41] Tensorflow. 2020. preprocessing. https://tfhub.dev/tensorflow/bert\_en\_uncased \_preprocess/3.   
[42] Sudheendra Vijayanarasimhan and Kristen Grauman. 2014. Large-scale live active learning: Training object detectors with crawled data and crowds. International journal of computer vision 108 (2014), 97–114.   
[43] Junyang Wang, Lan Zhang, Junhao Wang, Mu Yuan, Yihang Cheng, Qian Xu, and Bo Yu. 2024. GraphProxy: Communication-efficient federated graph learning with adaptive proxy. In IEEE INFOCOM 2024-IEEE Conference on Computer Communications. IEEE, 2179–2188.   
[44] Ziting Wen, Oscar Pizarro, and Stefan Williams. 2024. Feature Alignment: Rethinking Efficient Active Learning via Proxy in the Context of Pre-trained Models. In Transactions on Machine Learning Research (TMLR).   
[45] Shitao Xiao, Zheng Liu, Yingxia Shao, Tao Di, Bhuvan Middha, Fangzhao Wu, and Xing Xie. 2022. Training large-scale news recommenders with pretrained language models in the loop. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 4215–4225.   
[46] Sang Michael Xie, Hieu Pham, Xuanyi Dong, Nan Du, Hanxiao Liu, Yifeng Lu, Percy S Liang, Quoc V Le, Tengyu Ma, and Adams Wei Yu. 2024. Doremi: Optimizing data mixtures speeds up language model pretraining. Advances in Neural Information Processing Systems 36 (2024).   
[47] Donggeun Yoo and In So Kweon. 2019. Learning loss for active learning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 93–102.

[48] Mu Yuan, Lan Zhang, Fengxiang He, Xueting Tong, and Xiang-Yang Li. 2022. Infi: end-to-end learnable input filter for resource-efficient mobile-centric inference. In Proceedings of the 28th Annual International Conference on Mobile Computing And Networking. 228–241.   
[49] Mu Yuan, Lan Zhang, Xiang-Yang Li, and Hui Xiong. 2020. Comprehensive and efficient data labeling via adaptive model scheduling. In 2020 IEEE 36th International Conference on Data Engineering (ICDE). IEEE, 1858–1861.   
[50] Mu Yuan, Lan Zhang, Xuanke You, and Xiang-Yang Li. 2023. PacketGame: Multi-Stream Packet Gating for Concurrent Video Inference at Scale. In Proceedings of the ACM SIGCOMM 2023 Conference. 724–737.   
[51] Minjia Zhang and Yuxiong He. 2020. Accelerating training of transformer-based language models with progressive layer dropping. Advances in neural information

processing systems 33 (2020), 14011–14023.

[52] Ruoyu Zhang, Yanzeng Li, Yongliang Ma, Ming Zhou, and Lei Zou. 2023. LLMaAA: Making Large Language Models as Active Annotators. In The 2023 Conference on Empirical Methods in Natural Language Processing.   
[53] Wenyu Zhang, Li Shen, and Chuan-Sheng Foo. 2023. Rethinking the role of pre-trained networks in source-free domain adaptation. In Proceedings of the IEEE/CVF International Conference on Computer Vision. 18841–18851.   
[54] Xiang Zhang, Junbo Jake Zhao, and Yann LeCun. 2015. Character-level Convolutional Networks for Text Classification. In NIPS.   
[55] Bin Zhao, Li Fei-Fei, and Eric P Xing. 2011. Online detection of unusual events in videos via dynamic sparse coding. In CVPR 2011. IEEE, 3313–3320.