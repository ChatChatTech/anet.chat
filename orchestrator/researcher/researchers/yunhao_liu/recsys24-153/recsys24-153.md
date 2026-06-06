# Utilizing Non-click Samples via Semi-supervised Learning for Conversion Rate Prediction

Jiahui Huang University of Science and Technology of China Hefei, Anhui, China hjh233@mail.ustc.edu.cn

Shanyang Jiang University of Science and Technology of China Hefei, Anhui, China yang12@mail.ustc.edu.cn

Lan Zhang∗ University of Science and Technology of China Hefei, Anhui, China zhanglan@ustc.edu.cn

Dongbo Huang Tencent Shanghai, China andrewhuang@tencent.com

Junhao Wang University of Science and Technology of China Hefei, Anhui, China junhaow@mail.ustc.edu.cn

Cheng Ding Tencent Shanghai, China kimding@tencent.com

Lan XuTencentShanghai, Chinalanxu@tencent.com

# ABSTRACT

Conversion rate (CVR) prediction is essential in recommender systems, facilitating precise matching between recommended items and users’ preferences. However, the sample selection bias (SSB) and data sparsity (DS) issues pose challenges to accurate prediction. Existing works have proposed the click-through and conversion rate (CTCVR) prediction task which models samples from exposure to “click and conversion” in entire space and incorporates multitask learning. This approach has shown efficacy in mitigating these challenges. Nevertheless, it intensifies the false negative sample (FNS) problem. To be more specific, the CTCVR task implicitly treats all the CVR labels of non-click samples as negative, overlooking the possibility that some samples might convert if clicked. This oversight can negatively impact CVR model performance, as empirical analysis has confirmed. To this end, we advocate for discarding the CTCVR task and proposing a Non-click samples Improved SemisupErvised (NISE) method for conversion rate prediction, where the non-click samples are treated as unlabeled. Our approach aims to predict their probabilities of conversion if clicked, utilizing these predictions as pseudo-labels for further model training. This strategy can help alleviate the FNS problem, and direct modeling of the CVR task across the entire space also mitigates the SSB and DS challenges. Additionally, we conduct multi-task learning by introducing an auxiliary click-through rate prediction task, thereby enhancing

∗Lan Zhang is the corresponding author.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

RecSys ’24, October 14–18, 2024, Bari, Italy

© 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 979-8-4007-0505-2/24/10

https://doi.org/10.1145/3640457.3688151

embedding layer representations. Our approach is applicable to various multi-task architectures. Comprehensive experiments are conducted on both public and production datasets, demonstrating the superiority of our proposed method in mitigating the FNS challenge and improving the CVR estimation. The implementation code is available at https://github.com/Hjh233/NISE.

# CCS CONCEPTS

• Information systems → Recommender systems; • Computing methodologies → Semi-supervised learning settings.

# KEYWORDS

Recommender Systems, Conversion Rate Prediction, False Negative Samples, Semi-supervised Learning

# ACM Reference Format:

Jiahui Huang, Lan Zhang, Junhao Wang, Shanyang Jiang, Dongbo Huang, Cheng Ding, and Lan Xu. 2024. Utilizing Non-click Samples via Semisupervised Learning for Conversion Rate Prediction. In 18th ACM Conference on Recommender Systems (RecSys ’24), October 14–18, 2024, Bari, Italy. ACM, New York, NY, USA, 10 pages. https://doi.org/10.1145/3640457.3688151

# 1 INTRODUCTION

Recommender systems are designed to offer customized contents that align with user preferences by effectively navigating extensive databases [10, 22, 32, 42]. These systems generally operate in two stages. First, a candidate generation model swiftly retrieves hundreds of potential items from the database using initial user data and predictive signals. Then, a ranking model refines these selections by evaluating and sorting the items based on engagement metrics such as click-through rates (CTR) [1, 25, 29] and post-click conversion rates (CVR) [11, 23, 33, 39, 40, 43]. Accurate predictions of CTR and CVR are thus essential to improve recommendation effectiveness, user experiences and financial outcomes for platforms [43]. In this work, we primarily focus on the task of CVR prediction.

![](images/34bf909ee40fcb56b0fd530232ed56c5602f4a46e54e2ae3def2172bc726295e.jpg)



Figure 1: Illustration of key challenges in CVR prediction: sample selection bias, data sparsity and false negative sample. The training space O comprises only clicked samples, while the inference space D encompasses all exposed samples.

Users’ behaviors typically follow the "exposure → click → conversion" sequence [23, 33, 40, 43], making the CVR prediction task inherently counterfactual. This characterization introduces three critical issues. i) Sample selection bias (SSB). Conventional CVR models trained in click space O encounter challenges when inferring in entire space D due to the missing not at random (MNAR) [24, 30] nature of exposed but non-click samples. The discrepancy in distribution between O and D results in a biased CVR model. ii) Data sparsity (DS). Clicked samples are notably sparse in comparison to exposed ones. For instance, in the Ali-CCP dataset , out of the 84 million exposed samples, only 3.4 million are clicked, making up just 4% of the total samples in D. Unlike CTR models trained on the entire space D, contending with limited training samples in O, CVR models are hard to be fitted [23]. iii) False negative sample (FNS) problem. Due to the counterfactual nature of CVR task, non-click samples may be treated as negative since conversions are unlikely without clicking. Yet, the absence of clicks does not necessarily imply a dislike for these items [40, 43]. Instead, it could be attributed to factors such as exposure or position bias [8], where users may be unaware of the presence of exposed items. Certain samples still have the potential to convert if clicked and these samples as addressed as false negative samples. As illustrated in Figure 1, addressing the above challenges is crucial for accurate CVR prediction.

To tackle the SSB and DS issues, Ma et al. [23] propose the Entire Space Multi-task Model (ESMM) by modeling CVR task across the entire space. They utilize auxiliary CTR and click-through & conversion rate (CTCVR) tasks to enhance estimation accuracy through feature representation transfer learning. To optimize the biased CVR estimator of ESMM, causal approaches such as inverse propensity weighting (IPW) [35] and doubly robust (DR) estimator [36] are introduced. Specifically, Multi-IPW [40] and ESCM2-IPS [33] assign a propensity score to each sample in O to weight the CVR error terms. Multi-DR [40] and ESCM -DR [33] add additional imputation models to predict errors and ensure unbiasedness when either imputation errors or learned propensities is accurate. To further address the SSB problem, Zhu et al. [43] propose a general framework involving a new counterfactual space N∗ where samples have opposite labels to their corresponding factual ones to directly debias in O ∪ N ∗.

Despite significant advances in this field, all previously mentioned methods leverage the auxiliary CTCVR task to mitigate the issues of SSB and DS. However, due to the counterfactual nature of the CVR task, the CTCVR task shares the same label space with the CVR task. We identify that the benefits of CTCVR task comes at the cost of treating all samples in N as negative in the CVR task, thereby exacerbating the FNS problem. To validate these concerns, we have conducted empirical analysis on a benchmark dataset, which corroborates the harmful impact of this approach.

To this end, we utilize a Non-click samples Improved SemisupErvised (NISE) method for conversion rate prediction, and discard the CTCVR task in the classical multi-task learning framework. This method models all samples in the entire space D, which inherits the merits from previous works to tackle the SSB and DS challenges. More importantly, instead of outright discarding the vast number of non-click samples or categorizing them as negative, we maintain them unlabeled and first predict the conversion probabilities for samples in non-click space N if they were clicked. Then, these probabilities are treated as pseudo-labels to facilitate the learning of CVR model in a semi-supervised manner. Furthermore, we incorporate an auxiliary CTR task and apply multi-task learning to enhance the representations of the embedding layer, taking advantage of the parameter transfer [23], During training, we adopt a dynamic task weight assignment mechanism to ensure a balanced and stable training process.

The contributions of this paper are summarized as follows:

• We conduct empirical analysis on the widely utilized CTCVR task. We identify that it could potentially aggravate the false negative sample problem because all exposed but non-clicked samples are implicitly treated as negative, thereby impairing the model’s CVR prediction performance.   
• Instead of utilizing the conventional CTCVR task, we treat the massive exposed yet non-click samples as unlabeled and innovatively devise a semi-supervised learning framework to predict their conversion rate. This entire space modeling strategy not only addresses the SSB and DS challenges but also mitigates the FNS problem.   
• To leverage the power of parameter transfer, we also introduce an auxiliary CTR task and conduct multi-task learning. The proposed approach can be seamless applied to various multi-task learning architectures, such as shared bottom, multi-experts and mixed-experts models.   
• Extensive experiments conducted on three real-world datasets validate the superiority of our approach over five state-ofthe-art (SOTA) baselines in predicting CVR. Specifically, we observed a 1.11% and 2.00% relative gain in AUC on two public datasets, and a 0.70% AUC gain on a production dataset.

# 2 PRELIMINARIES

In this section, we begin by defining the focused problem in our paper. Then, we review representative methods in existing literature, laying the foundation for discussions in subsequent sections.

# 2.1 Problem Statement

This paper focuses on the conversion rate (CVR) prediction problem. We first present several important notations below. We denote $\mathcal { U } = \{ u _ { 1 } , u _ { 2 } , . . . , u _ { m } \}$ as the set of ?? users and ${ \cal T } = \{ i _ { 1 } , i _ { 2 } , \dots , i _ { n } \}$ as the set of ?? items. $\mathcal { D } = \mathcal { U } \times \mathcal { I }$ represents the entire space composed of all exposed user-item pairs. $x _ { u , i } \in \mathbb { R } ^ { d }$ is the feature vector of user ?? and item ?? and their interactions, with ?? denoting the feature dimension. $O = \{ ( u , i ) | o _ { u , i } = 1 , ( u , i ) \in \mathcal { D } \}$ and $\mathcal { R } = \{ ( u , i ) | r _ { u , i } = 1 , ( u , i ) \in \mathcal { D } \}$ represent click space and conversion space respectively, where $o _ { u , i } \in \{ 0 , 1 \}$ indicates whether user ?? clicks on item ?? and $r _ { u , i } \in \{ 0 , 1 \}$ indicates whether item ?? is converted by user ??. $N = \{ ( u , i ) | o _ { u , i } = 0 , ( u , i ) \in \mathcal { D } \}$ , on the other hand, represents the non-click space. $\mathbf { O } \in \mathbb { R } ^ { m \times n }$ and $\mathbf { R } \in \mathbb { R } ^ { m \times n }$ are click matrix and conversion matrix of users on items respectively.

With the above definitions, we formulate the target problem.

Problem 1 (CVR Prediction). Given user set U, item set I, exposure space D, feature vector set $\{ \boldsymbol { x } _ { u , i } \in \mathbb { R } ^ { d } | ( u , i ) \in \mathcal { D } \}$ , mapping function $f ( \cdot ) : \mathbb { R } ^ { d }  \mathbb { I }$ R and fully observed conversion matrix R, we seek to minimize the following ideal CVR loss

$$
\mathcal {L} _ {\text { ideal }} = \frac {1}{| \mathcal {D} |} \sum_ {(u, i) \in \mathcal {D}} e (r _ {u, i}, \hat {r} _ {u, i}) \tag {1}
$$

where $\hat { r } _ { u , i } = f ( x _ { u , i } )$ represents predicted converted probability, $e ( \cdot , \cdot ) i s$ the cross-entropy loss and $e ( r _ { u , i } , \hat { r } _ { u , i } ) = - r _ { u , i } \log { \hat { r } _ { u , i } } - ( 1 - r _ { u , i } ) \log ( 1 -$ $\hat { r } _ { u , i } )$ .

Nonetheless, it is unrealistic to obtain a fully observed R since the conversion labels in non-click space N remain unknown, and the naive way to train the CVR model is to optimize the following loss based on the observed conversion labels in click space O:

$$
\mathcal {L} _ {\text { naive }} = \frac {1}{| \mathcal {O} |} \sum_ {(u, i) \in \mathcal {O}} e (r _ {u, i}, \hat {r} _ {u, i}) = \frac {1}{| \mathcal {O} |} \sum_ {(u, i) \in \mathcal {D}} o _ {u, i} e (r _ {u, i}, \hat {r} _ {u, i}) \tag {2}
$$

Due to the missing not at random nature [24, 30], $\mathcal { L } _ { n a i v e }$ is not an unbiased estimator of $\mathcal { L } _ { i d e a l } \ [ 3 3 , 4 0 ]$ .

# 2.2 Existing CVR Prediction Methods

In this section, we provide a brief overview of representative and state-of-the-art approaches aimed at mitigating the SSB and DS problems. All methods utilize multi-task learning to enhance model training. We first introduce the general multi-task learning framework and then list debiasing methods in CVR prediction task.

The auxiliary CTR and CTCVR tasks are first introduced in [23]. The idea behind this is that both CTR and CTCVR tasks are trained with all the exposed samples in the entire space, thus SSB problem can be alleviated. Furthermore, by sharing parameters of the lookup table between CTR and CVR models, the DS issue can be mitigated. ESMM [23] adopts multi-task learning to enhance CVR modeling, with the multi-task loss function formulated as:

$$
\begin{array}{l} \mathcal {L} _ {E S M M} = \mathcal {L} _ {C T R} + \mathcal {L} _ {C T C V R} \\ = \frac {1}{| \mathcal {D} |} \sum_ {(u, i) \in \mathcal {D}} e (o _ {u, i}, \hat {o} _ {u, i}) \tag {3} \\ + \frac {1}{| \mathcal {D} |} \sum_ {(u, i) \in \mathcal {D}} e (o _ {u, i} \& r _ {u, i}, \hat {o} _ {u, i} \times \hat {r} _ {u, i}) \\ \end{array}
$$

where $\hat { o } _ { u , i }$ represents predicted clicked probability and $\hat { r } _ { u , i }$ is treated as an intermediate variable.

Subsequent works [33, 40, 43] adopt similar multi-task framework and augment it with an additional tailored CVR loss to further address the SSB problem.

2.2.1 Inverse Propensity Weighting (IPW) for CVR Prediction. Inverse propensity weighting [35] assigns weights to click samples to achieve an unbiased estimation of the ideal CVR loss. Typically, the probability $p ( o _ { u , i } = 1 )$ is regarded as the true propensity score, and the output of CTR model $\hat { o } _ { u , i }$ serves as an estimate [33, 40].

The loss function is formulated as:

$$
\mathcal {L} _ {I P W} = \frac {1}{| \mathcal {D} |} \sum_ {(u, i) \in \mathcal {D}} \frac {o _ {u , i} e (r _ {u , i} , \hat {r} _ {u , i})}{\hat {o} _ {u , i}} \tag {4}
$$

2.2.2 Doubly Robust (DR) for CVR Prediction. Doubly robust methods [36] combine error imputation based (EIB) models with inverse propensity weighting. If either the propensity score or the error imputation model is accurate, the DR estimator is unbiased [33, 40].

The loss function is formulated as:

$$
\mathcal {L} _ {D R} = \frac {1}{| \mathcal {D} |} \sum_ {(u, i) \in \mathcal {D}} [ \hat {e} _ {u, i} + \frac {o _ {u , i} (e (r _ {u , i} , \hat {r} _ {u , i}) - \hat {e} _ {u , i})}{\hat {o} _ {u , i}} ] \tag {5}
$$

2.2.3 Counterfactual Mechanism for CVR Prediction. Zhu et al. [43] propose a general debiasing framework DCMT, which introduces the concept of a counterfactual space for CVR task. In the training process, a counterfactual CVR tower is introduced to predict the counterfactual CVR scores and a counterfactual regularizer is incorporated as a soft constraint.

Specifically, for a factual sample $< ~ r _ { u , i } ~ = ~ 0 , o _ { u , i } ~ = ~ 0 , x _ { u , i } ~ >$ in non-click space N, its corresponding counterfactual sample is $< ~ r _ { u . i } ^ { * } ~ = ~ 1 , o _ { u . i } ~ = ~ d o ( o _ { u , i } ) ~ = ~ 1 , x _ { u , i } ~ > ,$ ∗ , where $^ { \ast } d o ^ { \ast }$ indicates the assumption that the sample is clicked. The total loss function is formulated as:

$$
\begin{array}{l} \mathcal {L} _ {D C M T} = \frac {1}{| \mathcal {D} |} \left(\sum_ {(u, i) \in O} \frac {e \left(r _ {u , i} , \hat {r} _ {u , i}\right)}{\hat {\sigma} _ {u , i}} + \sum_ {(u, i) \in \mathcal {N} ^ {*}} \frac {e \left(r _ {u , i} ^ {*} , \hat {r} _ {u , i} ^ {*}\right)}{1 - \hat {\sigma} _ {u , i}}\right) \tag {6} \\ + \frac {\lambda}{| \mathcal {D} |} \sum_ {(u, i) \in \mathcal {D}} | 1 - (\hat {r} _ {u, i} + \hat {r} _ {u, i} ^ {*}) | \\ \end{array}
$$

# 3 DISCUSSION ON NON-CLICK SAMPLES

In this section, we analyze the widely used CTCVR task and demonstrate its limitations with empirical evidence. Subsequently, we contend that non-click samples do not necessarily indicate disinterest, and appropriate utilization of these samples can be advantageous for CVR prediction.

# 3.1 Diving into the Auxiliary CTCVR Task

To address the data sparsity and sample selection bias problem, an auxiliary CTCVR task [23] is widely employed in the field of CVR prediction [33, 39, 40, 43]. This task models the transition of each item from exposure to "click and conversion", thus the training domain for CTCVR encompasses the entire space D. We define $t _ { u , i }$ and $\hat { t } _ { u , i }$ as the actual label and predicted probability of the CTCVR task, respectively. Specifically, $t _ { u , i } = 1$ signifies that the exposed item ?? is clicked and converted by user ??, whereas $t _ { u , i } = 0$ indicates that the item is either not clicked or clicked but not converted. The output probability of CTCVR task can be decomposed as follows,

Table 1: Performance Comparison of CVR Models Treating Non-Click Space (N) Samples as Negative vs. Unlabeled in Ali-CCP Dataset. 

<table><tr><td>Labels in N</td><td>AUC</td><td>Relative gain</td><td>KS</td><td>Relative gain</td></tr><tr><td>Negative</td><td>0.6357</td><td>-</td><td>0.1928</td><td>-</td></tr><tr><td>Unlabeled</td><td>0.6392</td><td>0.55%</td><td>0.1977</td><td>2.54%</td></tr></table>

$$
p (t _ {u, i} = 1 | x _ {u, i}) = p (o _ {u, i} = 1 | x _ {u, i}) \times p (r _ {u, i} = 1 | x _ {u, i}, o _ {u, i} = 1) \tag {7}
$$

which treats CVR prediction as an intermediate task.

For samples that are exposed and clicked, denoted by the click label $o _ { u , i } ~ = ~ 1$ , the CTCVR label $t _ { u , i } = o _ { u , i }$ ?????? $r _ { u , i }$ aligns with the CVR label. For exposed but not clicked samples, with $o _ { u , i } = 0 ;$ the CTCVR label is $t _ { u , i } = o _ { u , i }$ ?????? $r _ { u , i } = 0 .$ Because non-clicked samples are assigned a CTCVR label of 0, optimizing the CTCVR task means that the predicted CTCVR value for non-clicked samples should trend towards zero. Additionally, since the predicted CTCVR value is the product of the output probabilities of the CTR and CVR tasks, this optimization also pushes the predicted CVR value towards zero. Therefore, optimizing the CTCVR task effectively equates to assigning a CVR label of 0 to these non-clicked samples. Previously, the CVR model was trained exclusively in click space O since it was designed to model the "click → conversion" sequence, ignoring non-clicked samples. The introduction of the CTCVR task expands the training space from just O to entire space D, yet we argue it treats the CVR labels of non-click samples as negative. This could potentially influence the predictive performance of the CVR model, which we will discuss in the subsequent subsection.

# 3.2 Non-click ≠ Disinterest

Due to the sequential nature of the "exposure → click → conversion" process, conversion labels remain unknown for non-click samples in N. One straightforward idea is to exclude non-click samples from the training dataset. However, it has been shown to exhibit poor generalization ability since it significantly reduces training space [23]. Another idea is to treat these samples as negative, as adopted in many previous studies [4, 5, 17, 18]. However, the absence of clicks does not necessarily imply disinterest. Instead, it could be attributed to factors such as exposure or position bias [8], where users might even be unaware of the presence of exposed items. Personal user habits can also affect interaction patterns. For example, in an online Tencent recommender system, selected ads are recommended to users during the morning rush hour. However, some users rarely click on these ads because they prefer to focus on the content of their current browsing pages, such as news on current affairs. In such cases, non-click behaviors often result from a desire to avoid distractions rather than a lack of interest. If these non-click samples were to be clicked, there is still a possibility that they could eventually convert [40, 43]. Such samples are referred to as false negative samples.

To further support our argument, we conducted empirical analysis on the Ali-CCP dataset to show the harmfulness of treating all non-click samples directly as negative. The details of the dataset will be presented in Section 5.1.1. Two different methodologies are compared. In the first method, all samples in N were treated as negative, whereas in the second, these instances were classified as unlabeled and modeled using semi-supervised learning techniques, which will be illustrated in Section 4.1. As shown in Table 1, the results demonstrate that treating all samples as unlabeled leads to a performance improvement of 0.55%, which is significant given the massive traffic in industrial-level recommender systems.

Moreover, we argue that while CTR task is directly related to the content (ad creatives), CVR task relates more to the conversion funnel aspects (landing page, download/installation process/order smoothness), as well as the quality and competitive pricing of the product itself. Recognizing that products with high quality and competitive pricing might not attract clicks due to less appealing creatives but are likely to convert once clicked, we discard the widely adopted CTCVR task and decouple CTR and CVR tasks, treating them as relatively independent. This strategic separation also serves to mitigate the FNS problem by dissociating the strong correlation between CTR and CVR tasks.

Grounded in the analysis above, we propose a novel semi-supervised approach to more effectively leverage the non-click samples for CVR prediction, as will be elaborated in Section 4.

# 4 METHODOLOGY

In this section, we detail the designs of our Non-click samples Improved Semi-supErvised (NISE) method for conversion rate prediction. This approach allows us to model the CVR task directly across the entire space, effectively addressing the SSB and DS challenges while also mitigating the FNS problem. Additionally, we incorporate the CTR task to enhance multi-task learning. Moreover, a dynamic weighting strategy is proposed to ensure a balanced training process. The framework of NISE is illustrated in Figure 2.

![](images/a9e58e1f4afdb936ece6beff8e42e153ab1edd286dde54346b31e2e2d9f0c65f.jpg)



Figure 2: System Overview

# 4.1 Semi-supervised Non-click Samples Exploitation

In CVR prediction task, we propose to keep the unknown CVR labels unlabeled to prevent from exacerbating the FNS problem. Inspired by work [38], we first estimate the probabilities that non-click samples in N would convert if clicked. By treating these probabilities as pseudo-labels, we model the CVR prediction task across the entire space $\mathcal { D } _ { : }$ , associated with the following loss function:

$$
\mathcal {L} _ {C V R} = \frac {1}{| \mathcal {D} |} (\sum_ {(u, i) \in \mathcal {O}} e (r _ {u, i}, \hat {r} _ {u, i}) + \sum_ {(u, i) \in \mathcal {N}} e (w _ {u, i}, \hat {r} _ {u, i})) \tag {8}
$$

where $w _ { u , i }$ is the probability that the non-click item ?? will be converted by user ??.

In the first term, we compute the standard cross-entropy loss in click space using the ground truth labels. While in the second term, we utilize the predicted probabilities $w _ { u , i }$ as pseudo-labels to calculate the cross-entropy loss. If the predictions of $w _ { u , i }$ are accurate, this formulation serves as an unbiased estimate of the ideal loss. However, obtaining an accurate estimation of $w _ { u , i }$ remains challenging. Lacking access to additional supervised signals [39] or the means to collect a counterfactual dataset for training an additional label correction model [38], we opt to directly employ the core CVR prediction model to estimate these probabilities. Consequently, the loss in N is calculated as $\textstyle \sum _ { ( u , i ) \in N } e \bigl ( \hat { r } _ { u , i } , \hat { r } _ { u , i } \bigr )$ and the CVR loss across entire space simplifies to the following:

$$
\mathcal {L} _ {C V R} = \frac {1}{| \mathcal {D} |} (\sum_ {(u, i) \in \mathcal {O}} e (r _ {u, i}, \hat {r} _ {u, i}) + \sum_ {(u, i) \in \mathcal {N}} e (\hat {r} _ {u, i}, \hat {r} _ {u, i})) \tag {9}
$$

The intuition behind this loss term is that employing the model’s output as pseudo-labels causes the cross-entropy loss to degrade into the entropy of $\hat { r } _ { u , i }$ . Since entropy measures the uncertainty of random variables, during backpropagation, the model is encouraged to predict $\hat { r } _ { u , i }$ towards the boundaries, i.e. towards 0 or 1. This approach alleviates the FNS problem to some extent by identifying high-probability converting samples in N, rather than categorically treating them as negative.

# 4.2 Multi-task Learning Framework

Multi-task learning (MTL) has proven effective in simultaneously learning multiple correlated tasks by sharing network parameter information across different tasks [2]. Given the strong correlation between CTR and CVR tasks, we construct a multi-task learning framework that includes an additional CTR prediction task, motivated by ESMM [23]. Specifically, the CVR model shares the same embedding lookup table with the CTR model, which maps largescale sparse input data to low-dimensional representation vectors. This shared use of bottom-layer modules benefits from transfer learning, enabling the learning of common feature representations across these two sequential tasks [23, 26]. The MTL training loss is expressed as follows:

$$
\begin{array}{l} \mathcal {L} _ {M T L} = \mathcal {L} _ {C T R} + \lambda \times \mathcal {L} _ {C V R} \\ = \frac {1}{| \mathcal {D} |} \sum_ {(u, i) \in \mathcal {D}} e (o _ {u, i}, \hat {o} _ {u, i}) + \tag {10} \\ \frac {\lambda}{| \mathcal {D} |} (\sum_ {(u, i) \in \mathcal {O}} e (r _ {u, i}, \hat {r} _ {u, i}) + \sum_ {(u, i) \in \mathcal {N}} e (\hat {r} _ {u, i}, \hat {r} _ {u, i})) \\ \end{array}
$$

where ?? is a hyper-parameter that controls the balance between these two tasks, and further details are explained in Section 4.3.

Algorithm 1: Utilizing Non-click Samples for CVR Prediction with Multi-task Learning.   
Input: training samples $\{(u,i)\in\mathcal{D}\}$ , click matrix $O\inR^{m\times n}$ , conversion matrix $R\inR^{m\times n}$ , training epoch e, learning rate $\eta$ , hyper-parameters $\alpha,\beta$ Output: CVR prediction model $\theta_{CVR}$ 1 Initialize CVR prediction model $\theta_{CVR}$ , CTR prediction model $\theta_{CTR}$ 2 for k=1 to e do

3    for training samples B in one batch do

4    Calculate $loss_{CVR}=$ 5 $\frac{1}{|\mathcal{B}|}(\sum_{(u,i)\in\mathcal{B},o_{u,i}=1}e(r_{u,i},\hat{r}_{u,i})+\sum_{(u,i)\in\mathcal{N},o_{u,i}=0}e(\hat{r}_{u,i},\hat{r}_{u,i}))$ ;

6    Calculate $loss_{CTR}=\frac{1}{|\mathcal{B}|}\sum_{(u,i)\in\mathcal{B}}e(o_{u,i},\hat{o}_{u,i})$ ;

7    Calculate weight = $\alpha\times\min\{\frac{loss_{CTR}}{loss_{CVR}},\beta\}$ ;

8    Calculate MTL loss

9 $loss_{MTL}=loss_{CTR}+weight\times loss_{CVR}$ ;

10 $\theta_{CVR}\leftarrow\theta_{CVR}-\eta\nabla_{\theta_{CVR}}loss_{MTL}$ ;

11 $\theta_{CTR}\leftarrow\theta_{CTR}-\eta\nabla_{\theta_{CTR}}loss_{MTL}$ ;

10 return trained CVR model $\theta _ { C V R }$

# 4.3 Dynamic Weighting Strategy

In practice, we observe that the training loss for CVR is consistently one to two orders of magnitude smaller than for CTR in the Ali-CCP dataset. This is likely due to the substantial difference in the size of positive samples: positive samples for the CVR task are only 0.5% of those in CTR task. Such a discrepancy in loss values can cause severe training imbalances, potentially allowing the CTR task to dominate training and hinder effective parameter updates for the CVR task, as highlighted in previous studies [9, 16].

While a universal hyper-parameter to balance the losses of CTR and CVR tasks offers a basic solution, it may be too coarse given the variability in positive sample sizes and loss values across different batches. To address this, we propose a more nuanced weighting strategy that dynamically assigns weights to each task based on their forward loss per batch, aiming for a balanced training process.

Specifically, we introduce two hyper-parameters, ?? and $\beta .$ For each mini-batch, we calculate the CVR and CTR losses during forward propagation. The weight is then calculated using the formula:

$$
w e i g h t = \alpha \times \min \{\frac {l o s s _ {C T R}}{l o s s _ {C V R}}, \beta \} \tag {11}
$$

The hyper-parameter ?? is used to adjust the relative magnitudes of CVR and CTR loss, while $\beta$ is introduced to prevent the weights from reaching excessively high values in cases where the CVR loss is extremely small, which could lead to instability during model training. Detailed training strategy is outlined in algorithm 1.

# 5 EVALUATION

We conduct extensive experiments to validate the effectiveness of our proposed method and address the following research questions:

RQ1: How does the proposed approach perform compared with representative or state-of-the-art baselines in CVR prediction.

RQ2: Does the proposed method still work when integrated into various multi-task learning frameworks?

Table 2: Comparisons of the evaluation results of the proposed model and baselines on public datasets. 

<table><tr><td rowspan="2">Backbone</td><td rowspan="2">Method</td><td colspan="3">Ali-CCP</td><td colspan="3">Kuaipure</td></tr><tr><td>AUC ↑</td><td>LogLoss ↓</td><td>KS ↑</td><td>AUC ↑</td><td>LogLoss ↓</td><td>KS ↑</td></tr><tr><td rowspan="6">MLP</td><td>ESMM</td><td>0.6287±0.0024</td><td>0.0113±0.0012</td><td>0.1874±0.0052</td><td>0.8431±0.0029</td><td>0.0719±0.0022</td><td>0.5558±0.0025</td></tr><tr><td>MMoE</td><td>0.6216±0.0025</td><td>0.0108±0.0014</td><td>0.1758±0.0043</td><td>0.8246±0.0034</td><td>0.0782±0.0029</td><td>0.5230±0.0061</td></tr><tr><td> $ESCM^2$ -IPS</td><td>0.6411±0.0023</td><td>0.0092±0.0018</td><td>0.2034±0.0032</td><td>0.8449±0.0018</td><td>0.0744±0.0011</td><td>0.5513±0.0017</td></tr><tr><td> $ESCM^2$ -DR</td><td>0.6182±0.0120</td><td>0.0119±0.0020</td><td>0.1700±0.0161</td><td>0.7986±0.0182</td><td>0.1144±0.0288</td><td>0.4661±0.0541</td></tr><tr><td>DCMT</td><td>0.6407±0.0024</td><td>0.0101±0.0011</td><td>0.2000±0.0056</td><td>0.8443±0.0018</td><td>0.0739±0.0033</td><td>0.5524±0.0070</td></tr><tr><td>NISE</td><td>0.6498±0.0038</td><td>0.0024±0.0001</td><td>0.2137±0.0068</td><td>0.8622±0.0021</td><td>0.0641±0.0005</td><td>0.5785±0.0023</td></tr><tr><td rowspan="6">DeepFM</td><td>ESMM</td><td>0.6306±0.0031</td><td>0.0094±0.0009</td><td>0.1874±0.0060</td><td>0.8496±0.0031</td><td>0.0695±0.0047</td><td>0.5618±0.0068</td></tr><tr><td>MMoE</td><td>0.6192±0.0025</td><td>0.0104±0.0019</td><td>0.1728±0.0032</td><td>0.8263±0.0058</td><td>0.0747±0.0038</td><td>0.5217±0.0111</td></tr><tr><td> $ESCM^2$ -IPS</td><td>0.6394±0.0023</td><td>0.0104±0.0003</td><td>0.1986±0.0025</td><td>0.8480±0.0038</td><td>0.0764±0.0061</td><td>0.5543±0.0108</td></tr><tr><td> $ESCM^2$ -DR</td><td>0.6003±0.0059</td><td>0.0131±0.0018</td><td>0.1452±0.0106</td><td>0.8037±0.1007</td><td>0.1233±0.0914</td><td>0.4863±0.1662</td></tr><tr><td>DCMT</td><td>0.6420±0.0005</td><td>0.0090±0.0011</td><td>0.2094±0.0028</td><td>0.8494±0.0024</td><td>0.0692±0.0072</td><td>0.5602±0.0051</td></tr><tr><td>NISE</td><td>0.6487±0.0016</td><td>0.0023±0.0001</td><td>0.2153±0.0065</td><td>0.8653±0.0013</td><td>0.0639±0.0017</td><td>0.5827±0.0030</td></tr><tr><td rowspan="6">DCNV2</td><td>ESMM</td><td>0.6280±0.0035</td><td>0.0096±0.0006</td><td>0.1855±0.0037</td><td>0.8423±0.0053</td><td>0.0751±0.0039</td><td>0.5547±0.0110</td></tr><tr><td>MMoE</td><td>0.6250±0.0031</td><td>0.0113±0.0017</td><td>0.1787±0.0027</td><td>0.8308±0.0040</td><td>0.0756±0.0046</td><td>0.5310±0.0086</td></tr><tr><td> $ESCM^2$ -IPS</td><td>0.6425±0.0014</td><td>0.0106±0.0010</td><td>0.2089±0.0031</td><td>0.8438±0.0028</td><td>0.0724±0.0019</td><td>0.5493±0.0054</td></tr><tr><td> $ESCM^2$ -DR</td><td>0.6208±0.0055</td><td>0.0120±0.0024</td><td>0.1758±0.0078</td><td>0.5889±0.0575</td><td>0.6490±0.2225</td><td>0.1396±0.0785</td></tr><tr><td>DCMT</td><td>0.6431±0.0034</td><td>0.0110±0.0011</td><td>0.2071±0.0058</td><td>0.8463±0.0031</td><td>0.0750±0.0036</td><td>0.5553±0.0057</td></tr><tr><td>NISE</td><td>0.6520±0.0044</td><td>0.0024±0.0001</td><td>0.2188±0.0077</td><td>0.8641±0.0016</td><td>0.0629±0.0011</td><td>0.5781±0.0039</td></tr></table>

The best results are highlighted in bold and the best baselines are underlined. ↑ means the higher the metric the better while ↓ indicates the lower the metric the better.

RQ3: How does the dynamic weighting strategy perform compared to alternative ones?

RQ4: How does each component contribute to the framework.

RQ5: How do hyper-parameters influence the performance of NISE.

RQ6: How does negative sampling influence the model performance of SOTA baselines and our method.

# 5.1 Experimental Setup

5.1.1 Datasets. To evaluate the prediction performance of our proposed NISE method and other baselines, we conduct comprehensive experiments on both public and production dataset collected from industrial platforms.

• Public dataset: The Ali-CCP (Alibaba Click and Conversion Prediction) dataset [23] is a benchmark dataset for conversion rate prediction, collected from traffic logs in Taobao platform. KuaiRand-Pure is an unbiased sequential recommendation dataset [13] collected from the recommendation logs of the video-sharing mobile app, Kuaishou.

• Production dataset: The production dataset is collected from traffic logs in Tencent platform.

The statistics of three datasets are shown in Table 3.

Table 3: Statistics of experimental datasets 

<table><tr><td>Dataset</td><td>#Feature</td><td>#Exposure</td><td>#Click</td><td>#Conversion</td></tr><tr><td>Ali-CCP</td><td>33</td><td>84M</td><td>3.4M</td><td>18k</td></tr><tr><td>KuaiPure</td><td>41</td><td>1.4M</td><td>0.7M</td><td>22k</td></tr><tr><td>Production</td><td>20</td><td>2.3M</td><td>130k</td><td>51k</td></tr></table>

Table 4: Comparisons of the evaluation results of the proposed model and baselines on production datasets. 

<table><tr><td rowspan="2">Method</td><td colspan="3">Production</td></tr><tr><td>AUC ↑</td><td>LogLoss ↓</td><td>KS ↑</td></tr><tr><td>ESMM</td><td> $\underline{0.8120\pm 0.0010}$ </td><td> $\underline{0.0867\pm 0.0001}$ </td><td> $0.4971\pm 0.0011$ </td></tr><tr><td>MMoE</td><td> $0.7923\pm 0.0156$ </td><td> $0.0905\pm 0.0027$ </td><td> $0.4720\pm 0.0181$ </td></tr><tr><td> $ESCM^{2}-IPS$ </td><td> $0.8107\pm 0.0012$ </td><td> $0.0869\pm 0.0001$ </td><td> $0.4951\pm 0.0023$ </td></tr><tr><td> $ESCM^{2}-DR$ </td><td> $0.7314\pm 0.0381$ </td><td> $0.4713\pm 0.0695$ </td><td> $0.3687\pm 0.0547$ </td></tr><tr><td>DCMT</td><td> $0.8106\pm 0.0010$ </td><td> $0.0868\pm 0.0001$ </td><td> $\underline{0.4972\pm 0.0019}$ </td></tr><tr><td>NISE</td><td> $\underline{0.8172\pm 0.0039}$ </td><td> $\underline{0.0861\pm 0.0001}$ </td><td> $\underline{0.5037\pm 0.0014}$ </td></tr></table>

The best results are highlighted in bold and the best baselines are underlined. ↑ means the higher the metric the better while ↓ indicates the lower the metric the better.

5.1.2 Evaluation Metrics. Following previous works, we primarily use the AUC score (Area Under the ROC Curve) and Logloss to evaluate the CVR prediction performance. It has been widely recognized that even a 0.1% increase in the AUC score is significant. Additionally, we calculate and report the KS (Kolmogorov-Smirnov) score score to assess the model’s ability to discriminate between positive and negative samples.

5.1.3 Backbone Models. We choose three classical models as backbone models for classification2:

• MLP: the fully connected neural networks.

• DeepFM [14]: a model that combines the factorization machines and deep neural networks to emphasize both low and high order feature interactions.   
• DCNV2 [34]: a model that utilizes cross layers to learn explicit feature interactions and combines deep neural networks to learn implicit interactions.

5.1.4 Comparison Baselines. Following [43], we compare our method with five baseline models in three groups described as follows: (i) Parallel MTL Baselines: ESMM [23]; (ii) Multi-gate MTL Baselines: MMoE [22] (iii) Causal Baselines: ESCM2-IPW [33], ESCM2-DR [33] and DCMT [43].

5.1.5 Implementation Details. We implement all methods using a public recommendation library3. The hyper-parameters are uniformly set to ensure a fair comparison across all experiments. For both the Ali-CCP and Kuaipure datasets, the embedding dimension for each categorical feature is set to 16. In terms of architecture, for all three backbones, the MLP tower dimensions are set at [160, 80] for the Ali-CCP dataset and [512, 256, 128, 64] for the Kuaipure dataset. For the MMoE model, we configure 8 experts. The PLE model incorporates 4 shared experts and 4 task-specific experts. Following [38], we use the stacked structure and one cross-layer for DCNV2 model. Adam [19] is used as the default optimizer and the learning rate is set to be 1e-3 with weight decay being 1e-5. The batch size is set to be 2048 for all methods. Early stopping is applied to prevent overfitting. We repeat each experiment five times on a single NVIDIA 3090 GPU and report the average results.

# 5.2 Overall Performance (RQ1)

In Table 2, we present the model performance of NISE and other strong baselines across two benchmark datasets. The results demonstrate that NISE consistently outperforms SOTA methods in terms of AUC, LogLoss, and KS metrics with various backbone models. Specifically, in the Ali-CCP dataset where only 0.02% of samples are converted, NISE exhibits an average relative AUC score improvement of 1.11% compared to SOTA methods. Similarly, in the Kuaipure dataset with 1.57% converted samples, NISE achieves an average relative AUC score improvement of 2.00% compared to SOTA methods, indicating a significant performance improvement. We attribute the performance boost to the utilization of massive non-click samples from a semi-supervised perspective. This approach aids in identifying high-probability converting samples within the non-click space, effectively mitigating the FNS problem. This utilization enhances the model’s ability to recognize potential positives that previous methods might overlook, thereby increasing accuracy and robustness. Among the strong baselines, ESCM2- IPS and DCMT stand out, both leveraging the inverse propensity weighting strategy. We posit that the efficacy of this strategy partly stems from its emphasis on assigning greater weight to the loss of CVR, thereby achieving a more balanced training process as mentioned in Section 4.2. However, it’s worth noting that ESCM2-DR exhibits instability during training, a phenomenon also pointed out in prior research [43]. The evaluation results in production dataset are shown in Table 4 with similar observations with Table 2. NISE surpasses the top-performing baseline method by 0.70% in terms of relative improvement in AUC.

# 5.3 Generalization Ability Analysis (RQ2)

In this section, we assess the NISE framework across various prevalent multi-task learning (MTL) architectures to evaluate its generalization capabilities. These architectures include the shared bottom model (ESMM [23]), the multi-experts model (MMoE [22]), and the mixed-experts model (PLE [32]).

As illustrated in Table 5, integrating NISE into these widely adopted MTL frameworks leads to significant performance gains. Specifically, we record AUC improvements of 3.65% for the Ali-CCP dataset and 2.91% for the Kuaipure dataset. These consistent enhancements in CVR model predictions significantly demonstrate the effectiveness of the NISE approach when integrated into various MTL architectures, highlighting its robustness and adaptability in enhancing predictive accuracy across different settings.

# 5.4 Weighting Strategy Comparison (RQ3)

Various weighting strategies are proposed in multi-task learning scenarios, such as dynamic task prioritization (DTP) loss in [16] and dynamic weight average (DWA) strategy in [20]. To validate the effectiveness of our proposed dynamic weighting strategy, we conduct experiments on Ali-CCP dataset using three backbones. As shown in Table 6, NISE outperforms both DTP and DWA by a large margin. DTP employs the AUC per batch to gauge the difficulty of a task. However, the weights allocated to each task are nearly equal since the AUCs for CTR and CVR tasks are similar, leading to CTR dominance. DWA assigns weights based on changes in loss between two epochs. However, compared to the ratio of the losses, the ratio of the changes in losses is closer to 1. Additionally, both tasks are assigned equal weights of 1 in the initial two epochs, maintaining CTR’s dominance early in training.

# 5.5 Ablation Study (RQ4)

In this section, we aim to identify the crucial components of our proposed method and implement three variants of NISE on Ali-CCP dataset:

• NISE-1: To validate the effectiveness of multi-task training, we train a single CVR model across the entire space.   
• NISE-2: To investigate the effectiveness of the introduction of non-click samples, we model the CVR task in click space O using the naive loss in Equation 2.   
• NISE-3: To explore the effectiveness of weighting mechanism, we omit the assignment of weights per batch, and instead directly using the addition of CTR and CVR loss as the final multi-task loss.

As illustrated in Figure 3, the performance of NISE-1 experiences a notable decline, underscoring the importance of multi-task learning. Including the CTR task in training is beneficial for learning better representations in the embedding layer, which occupies a significant proportion of the model parameters. The performances of NISE-2 and NISE-3 exhibit similar trends, with a relative AUC drop of 1.5%. The absence of consideration for non-click samples results in a much smaller training space for the CVR task. Direct discarding numerous negative and potential positive samples leads to significant information loss. Furthermore, given the observation that CVR loss is considerably smaller than that of CTR, the absence of the dynamic weighting strategy leads to severe training imbalance, resulting in poor performance of the CVR model.

Table 5: Overall performance improvement by applying NISE to various multi-task learning architectures. 

<table><tr><td rowspan="2">MTL architecture</td><td rowspan="2">Method</td><td colspan="3">Ali-CCP</td><td colspan="3">Kuaipure</td></tr><tr><td>AUC ↑</td><td>LogLoss ↓</td><td>KS ↑</td><td>AUC ↑</td><td>LogLoss ↓</td><td>KS ↑</td></tr><tr><td rowspan="3">Shared bottom</td><td>ESMM</td><td>0.6287±0.0024</td><td>0.0113±0.0012</td><td>0.1874±0.0052</td><td>0.8431±0.0029</td><td>0.0719±0.0022</td><td>0.5558±0.0025</td></tr><tr><td>NISE</td><td>0.6498±0.0038</td><td>0.0024±0.0001</td><td>0.2137±0.0068</td><td>0.8622±0.0021</td><td>0.0641±0.0005</td><td>0.5785±0.0023</td></tr><tr><td>Gain</td><td>3.36%</td><td>78.76%</td><td>14.03%</td><td>2.27%</td><td>10.84%</td><td>4.08%</td></tr><tr><td rowspan="3">Multi-experts</td><td>MMoE</td><td>0.6216±0.0025</td><td>0.0108±0.0014</td><td>0.1758±0.0043</td><td>0.8246±0.0034</td><td>0.0782±0.0029</td><td>0.5230±0.0061</td></tr><tr><td>NISE</td><td>0.6468±0.0026</td><td>0.0023±0.0001</td><td>0.2137±0.0048</td><td>0.8535±0.0059</td><td>0.0702±0.0031</td><td>0.5722±0.0040</td></tr><tr><td>Gain</td><td>4.05%</td><td>78.70%</td><td>21.56%</td><td>3.50%</td><td>10.23%</td><td>9.41%</td></tr><tr><td rowspan="3">Mixed-experts</td><td>PLE</td><td>0.6207±0.0016</td><td>0.0112±0.0011</td><td>0.1764±0.0029</td><td>0.8413±0.0034</td><td>0.0731±0.0014</td><td>0.5461±0.0068</td></tr><tr><td>NISE</td><td>0.6449±0.0004</td><td>0.0023±0.0001</td><td>0.2088±0.0035</td><td>0.8661±0.0040</td><td>0.0649±0.0018</td><td>0.5826±0.0024</td></tr><tr><td>Gain</td><td>3.90%</td><td>79.46%</td><td>18.37%</td><td>2.95%</td><td>11.2%</td><td>6.68%</td></tr></table>

↑ means the higher the metric the better while ↓ indicates the lower the metric the better.

Table 6: Comparisons of different weighting strategies on Ali-CCP dataset. 

<table><tr><td rowspan="2">Backbone</td><td rowspan="2">Method</td><td colspan="3">Ali-CCP</td></tr><tr><td>AUC ↑</td><td>LogLoss ↓</td><td>KS ↑</td></tr><tr><td rowspan="3">MLP</td><td>DTP</td><td>0.6244±0.0032</td><td>0.0022±0.0001</td><td>0.1762±0.0050</td></tr><tr><td>DWA</td><td>0.6340±0.0035</td><td>0.0022±0.0001</td><td>0.1890±0.0056</td></tr><tr><td>NISE</td><td>0.6498±0.0038</td><td>0.0024±0.0001</td><td>0.2137±0.0068</td></tr><tr><td rowspan="3">DeepFM</td><td>DTP</td><td>0.6269±0.0025</td><td>0.0022±0.0001</td><td>0.1811±0.0043</td></tr><tr><td>DWA</td><td>0.6325±0.0028</td><td>0.0021±0.0001</td><td>0.1865±0.0043</td></tr><tr><td>NISE</td><td>0.6487±0.0016</td><td>0.0023±0.0001</td><td>0.2153±0.0065</td></tr><tr><td rowspan="3">DCNV2</td><td>DTP</td><td>0.6233±0.0024</td><td>0.0022±0.0001</td><td>0.1746±0.0037</td></tr><tr><td>DWA</td><td>0.6337±0.0023</td><td>0.0022±0.0001</td><td>0.1902±0.0036</td></tr><tr><td>NISE</td><td>0.6520±0.0044</td><td>0.0024±0.0001</td><td>0.2188±0.0077</td></tr></table>

![](images/cf3f8a6f811f225ac3f8aa238c8a4255e97fd16d2af9f0281ae26006a65f382c.jpg)



(a) AUC with different backbones.

![](images/40ac9f14b327da2ce1a07a16b172cbb979db9a95ca5b0224ee0f47db0c73a9d5.jpg)



(b) KS with different backbones.   
Figure 3: Ablation study on Ali-CCP.

# 5.6 Hyper-parameter Study (RQ5)

In this section, we explore how the hyper-parameters ?? and ?? affect our model’s prediction performance on Ali-CCP.

As is shown in Figure 4(a), when fixing the value of ??, the AUC score undergoes significant changes with different choices of ??.

![](images/5ea2f4c01e16e11dec9cd7d928e9621012ed3f5523a4542cdb43c98a630d37c1.jpg)



(a) AUC and KS with different value of ?? and fixed ?? = 50

![](images/cb7a3a6b65352ed334538838213c470686b2df71857d1f0d3728a07fb030f10b.jpg)



(b) AUC and KS with different value of ?? and fixed ?? = 1   
Figure 4: Hyper-parameter analysis on Ali-CCP.

Too small value of ?? will make CTR task dominate in the multitask learning process, while too large value of ?? also deteriorates CVR model performance. We presume it could be attributed to the fact that the labels for the CTR task are accurate across the entire space, whereas for the CVR task, most labels remain unknown. If too much attention is allocated to the CVR task, the potential benefit of parameter transfer introduced by the CTR task diminishes, leading to poorer learned representations. When fixing ??, similar observations are shown in Figure 4(b) with various value of ??: a low ?? leads to training imbalances, while a high ?? overly prioritizes the CVR task, diminishing the CTR task’s contributions.

# 5.7 Negative sampling vs Non-sampling (RQ6)

While leveraging all non-click samples and conducting multi-task learning can significantly enhance CVR model performance, it also results in substantially higher computational costs. Therefore, we evaluate the impact of negative sampling versus non-sampling on model performance using the Ali-CCP dataset. We experiment by randomly sampling ${ \frac { 1 } { 2 4 } } , { \frac { 1 } { 1 2 } } , { \frac { 1 } { 4 } }$ , and $\begin{array} { l } { { \frac { 1 } { 2 } } } \end{array}$ of the non-click samples in N , and compare the results with a non-sampling strategy.

Surprisingly, almost all methods show an increase followed by a decrease in performance as the proportion of sampled non-click samples increases. This pattern suggests that negative sampling can, up to a certain point, simultaneously improve the model’s predictive ability and reduce training costs compared to the nonsampling strategy. We hypothesize that as the number of selected non-click samples initially increases, the data sparsity issue within the model is substantially alleviated, benefiting the CVR model from the enhanced dataset. However, as the proportion of sampled non-click samples continues to rise, SOTA methods may encounter more severe class imbalance issues, as an increasing number of nonclick samples are treated as negative. Furthermore, our proposed method may face challenges due to the growing imbalance between labeled and unlabeled data, leading to increased uncertainty and a consequent degradation in model performance.

![](images/a612c91139f3dd8720ed411a871ee88b70bc52ed9fe7e8ea3021fff066e89405.jpg)



(a) AUC with different sampling ratios

![](images/b7c2e85b04827e7cb4b210c2c18de8f8b3e0bdc2a5098bc09838572af26ba53b.jpg)



(b) KS with different sampling ratios   
Figure 5: Comparison of negative sampling and nonsampling strategies on Ali-CCP.

# 6 RELATED WORK

# 6.1 Multi-Task Learning for CVR Prediction

Due to the inherent similarity between click-through rate (CTR) and conversion rate (CVR) predictions and the sequential pattern of users’ behaviors, CTR models are widely employed in CVR task. Ma et al. [23] first proposed an entire space multi-task model (ESMM) in which they incorporated post-view click-through&conversion rate (CTCVR) as an auxiliary task with CTR task to alleviate sample selection bias and data sparsity problems in CVR prediction. Wen et al. [39] then proposed post-click behavior decomposition to leverage extra purchase-related actions as supervised signals. However, the estimates of ESMM for CVR prediction were found to be higher than the ground truth [33, 40]. Additionally, ESMM overlooked the causal effect of ?????????? → ???????????????????? and exhibited the potential in dependence priority (PIP) problem. To address the above problems and obtain an unbiased CVR estimation, causal inference methods [7, 31, 36] have been adopted. This involved combining inverse propensity weighting (IPW) and doubly robust (DR) methods with a multi-task learning framework [33, 40], regulating CVR predictions through a counterfactual risk minimizer. Dai et al. [11] further introduced a generalized doubly robust learning framework and proposed DR-BIAS and DR-MSE to balance the bias and variance term of DR estimator, achieving better generalization performance. Despite these improvements, existing causal inference methods primarily conducted debiasing in click space. Zhu et al. [43] addressed this limitation by introducing the concept of counterfactual samples in the non-click space. They proposed a counterfactual mechanism to directly debias in the entire space, predicting factual CVR and counterfactual CVR in respective spaces.

# 6.2 False Negatives in Recommender Systems

The prevalence of false negative samples presents a significant challenge in recommender systems, particularly in scenarios where models are trained using implicit user feedback, such as clicks or watches. In these cases, observed interactions are labeled as positive, while unobserved ones are typically labeled as negative. Existing training approaches can be broadly categorized into two types: the first type involves sampling negative instances from unobserved interactions [12, 27, 28, 41], and the second type treats all missing data as negative [5, 6, 17]. Both approaches, however, grapple with the challenge of mislabeling potential positive samples as negative, exacerbated by exposure or position bias [8, 15, 37], which can compromise the accuracy and robustness of the model.

In the realm of sequential recommendation, Liu et al. [21] introduce UFNRec, which identifies false negative samples based on higher prediction scores in successive rounds and subsequently reverses the labels of these samples for model training. In the context of CVR prediction, where samples may take a considerable time to convert, delayed feedback [3] can lead to incorrect negative labels as well. To address this, Wang et al. [38] developed a label correction method that predicts the probability of an unobserved sample being a false negative, thereby aiming to achieve an unbiased estimate of the oracle loss. Moreover, self-selection bias can also contribute to false negative samples in CVR tasks. Previous studies [40, 43] have shown that factors such as exposure position can influence whether items are clicked. Non-click items that might otherwise convert if clicked are often overlooked. Despite the significant impact of these biases, the issue of false negative samples in CVR prediction has not yet been thoroughly examined.

# 7 CONCLUSION

In this paper, we introduce NISE, a novel approach for conversion rate prediction. While previous methods focus on addressing the SSB and DS problems, we further tackle the FNS challenge, which emerges from potential positive samples in the expansive non-click space. We argue that previously proposed CTCVR task treat the CVR labels for non-click samples as negative, compromising the model’s robustness. NISE differentiates itself by treating all nonclick samples as unlabeled and using the generated conversion probabilities as pseudo-labels for semi-supervised learning. The addition of a CTR task and a dynamic loss assigning strategy further enhance representation learning and ensure a balanced training process. Experimental results on both public and production datasets validate the effectiveness of our approach.

Despite its advancements, NISE has limitations that pave the way for future research. While negative sampling is promising for enhancing performance and reducing computational costs as observed in Section 5.7, its integration into multi-task learning frameworks for CVR prediction remains a challenge. Furthermore, the reliance on possibly biased prediction probabilities as soft labels introduces potential inaccuracies, highlighting the need for advanced semisupervised learning techniques and additional supervised signals to improve training effectiveness.

# ACKNOWLEDGMENTS

Lan Zhang is the corresponding author. This research was supported by the China National Natural Science Foundation with No. 61932016 "the Fundamental Research Funds for the Central Universities" WK2150110024, and Tencent Marketing Solution Rhino-Bird Focused Research Program.

# REFERENCES

[1] Deepak Agarwal, Rahul Agrawal, Rajiv Khanna, and Nagaraj Kota. 2010. Estimating rates of rare events with multiple hierarchies through scalable log-linear models. In Proceedings of the 16th ACM SIGKDD international conference on Knowledge discovery and data mining. 213–222.   
[2] Rich Caruana. 1997. Multitask learning. Machine learning 28 (1997), 41–75.   
[3] Olivier Chapelle. 2014. Modeling delayed feedback in display advertising. In Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining. 1097–1105.   
[4] Chong Chen, Weizhi Ma, Min Zhang, Chenyang Wang, Yiqun Liu, and Shaoping Ma. 2023. Revisiting negative sampling vs. non-sampling in implicit recommendation. ACM Transactions on Information Systems 41, 1 (2023), 1–25.   
[5] Chong Chen, Min Zhang, Chenyang Wang, Weizhi Ma, Minming Li, Yiqun Liu, and Shaoping Ma. 2019. An efficient adaptive transfer neural network for socialaware recommendation. In Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval. 225–234.   
[6] Chong Chen, Min Zhang, Yongfeng Zhang, Yiqun Liu, and Shaoping Ma. 2020. Efficient neural matrix factorization without sampling for recommendation. ACM Transactions on Information Systems (TOIS) 38, 2 (2020), 1–28.   
[7] Jiawei Chen, Hande Dong, Yang Qiu, Xiangnan He, Xin Xin, Liang Chen, Guli Lin, and Keping Yang. 2021. AutoDebias: Learning to debias for recommendation. In Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval. 21–30.   
[8] Jiawei Chen, Hande Dong, Xiang Wang, Fuli Feng, Meng Wang, and Xiangnan He. 2023. Bias and debias in recommender system: A survey and future directions. ACM Transactions on Information Systems 41, 3 (2023), 1–39.   
[9] Zhao Chen, Vijay Badrinarayanan, Chen-Yu Lee, and Andrew Rabinovich. 2018. Gradnorm: Gradient normalization for adaptive loss balancing in deep multitask networks. In International conference on machine learning. PMLR, 794–803.   
[10] Paul Covington, Jay Adams, and Emre Sargin. 2016. Deep neural networks for youtube recommendations. In Proceedings of the 10th ACM conference on recommender systems. 191–198.   
[11] Quanyu Dai, Haoxuan Li, Peng Wu, Zhenhua Dong, Xiao-Hua Zhou, Rui Zhang, Rui Zhang, and Jie Sun. 2022. A generalized doubly robust learning framework for debiasing post-click conversion rate prediction. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 252–262.   
[12] Jingtao Ding, Yuhan Quan, Quanming Yao, Yong Li, and Depeng Jin. 2020. Simplify and robustify negative sampling for implicit collaborative filtering. Advances in Neural Information Processing Systems 33 (2020), 1094–1105.   
[13] Chongming Gao, Shijun Li, Yuan Zhang, Jiawei Chen, Biao Li, Wenqiang Lei, Peng Jiang, and Xiangnan He. 2022. KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos. In Proceedings of the 31st ACM International Conference on Information & Knowledge Management. 3953–3957.   
[14] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, and Xiuqiang He. 2017. DeepFM: a factorization-machine based neural network for CTR prediction. arXiv preprint arXiv:1703.04247 (2017).   
[15] Huifeng Guo, Jinkai Yu, Qing Liu, Ruiming Tang, and Yuzhou Zhang. 2019. PAL: a position-bias aware learning framework for CTR prediction in live recommender systems. In Proceedings of the 13th ACM Conference on Recommender Systems. 452–456.   
[16] Michelle Guo, Albert Haque, De-An Huang, Serena Yeung, and Li Fei-Fei. 2018. Dynamic task prioritization for multitask learning. In Proceedings of the European conference on computer vision (ECCV). 270–287.   
[17] Xiangnan He, Hanwang Zhang, Min-Yen Kan, and Tat-Seng Chua. 2016. Fast matrix factorization for online recommendation with implicit feedback. In Proceedings of the 39th International ACM SIGIR conference on Research and Development in Information Retrieval. 549–558.   
[18] Yifan Hu, Yehuda Koren, and Chris Volinsky. 2008. Collaborative filtering for implicit feedback datasets. In 2008 Eighth IEEE international conference on data mining. Ieee, 263–272.   
[19] Diederik P Kingma and Jimmy Ba. 2014. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 (2014).   
[20] Shikun Liu, Edward Johns, and Andrew J Davison. 2019. End-to-end multi-task learning with attention. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 1871–1880.   
[21] Xiaoyang Liu, Chong Liu, Pinzheng Wang, Rongqin Zheng, Lixin Zhang, Leyu Lin, Zhijun Chen, and Liangliang Fu. 2023. UFNRec: Utilizing False Negative Samples for Sequential Recommendation. In Proceedings of the 2023 SIAM International Conference on Data Mining (SDM). SIAM, 46–54.   
[22] Jiaqi Ma, Zhe Zhao, Xinyang Yi, Jilin Chen, Lichan Hong, and Ed H Chi. 2018. Modeling task relationships in multi-task learning with multi-gate mixture-ofexperts. In Proceedings of the 24th ACM SIGKDD international conference on knowledge discovery & data mining. 1930–1939.   
[23] Xiao Ma, Liqin Zhao, Guan Huang, Zhi Wang, Zelin Hu, Xiaoqiang Zhu, and Kun Gai. 2018. Entire space multi-task model: An effective approach for estimating post-click conversion rate. In The 41st International ACM SIGIR Conference on

Research & Development in Information Retrieval. 1137–1140.   
[24] Benjamin Marlin, Richard S Zemel, Sam Roweis, and Malcolm Slaney. 2012. Collaborative filtering and the missing at random assumption. arXiv preprint arXiv:1206.5267 (2012).   
[25] H Brendan McMahan, Gary Holt, David Sculley, Michael Young, Dietmar Ebner, Julian Grady, Lan Nie, Todd Phillips, Eugene Davydov, Daniel Golovin, et al. 2013. Ad click prediction: a view from the trenches. In Proceedings of the 19th ACM SIGKDD international conference on Knowledge discovery and data mining. 1222–1230.   
[26] Yabo Ni, Dan Ou, Shichen Liu, Xiang Li, Wenwu Ou, Anxiang Zeng, and Luo Si. 2018. Perceive your users in depth: Learning universal user representations from multiple e-commerce tasks. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 596–605.   
[27] Steffen Rendle and Christoph Freudenthaler. 2014. Improving pairwise learning for item recommendation from implicit feedback. In Proceedings of the 7th ACM international conference on Web search and data mining. 273–282.   
[28] Steffen Rendle, Christoph Freudenthaler, Zeno Gantner, and Lars Schmidt-Thieme. 2012. BPR: Bayesian personalized ranking from implicit feedback. arXiv preprint arXiv:1205.2618 (2012).   
[29] Matthew Richardson, Ewa Dominowska, and Robert Ragno. 2007. Predicting clicks: estimating the click-through rate for new ads. In Proceedings of the 16th international conference on World Wide Web. 521–530.   
[30] Yuta Saito, Suguru Yaginuma, Yuta Nishino, Hayato Sakata, and Kazuhide Nakata. 2020. Unbiased recommender learning from missing-not-at-random implicit feedback. In Proceedings of the 13th International Conference on Web Search and Data Mining. 501–509.   
[31] Tobias Schnabel, Adith Swaminathan, Ashudeep Singh, Navin Chandak, and Thorsten Joachims. 2016. Recommendations as treatments: Debiasing learning and evaluation. In international conference on machine learning. PMLR, 1670– 1679.   
[32] Hongyan Tang, Junning Liu, Ming Zhao, and Xudong Gong. 2020. Progressive layered extraction (ple): A novel multi-task learning (mtl) model for personalized recommendations. In Proceedings of the 14th ACM Conference on Recommender Systems. 269–278.   
[33] Hao Wang, Tai-Wei Chang, Tianqiao Liu, Jianmin Huang, Zhichao Chen, Chao Yu, Ruopeng Li, and Wei Chu. 2022. Escm2: Entire space counterfactual multitask model for post-click conversion rate estimation. In Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval. 363–372.   
[34] Ruoxi Wang, Rakesh Shivanna, Derek Cheng, Sagar Jain, Dong Lin, Lichan Hong, and Ed Chi. 2021. Dcn v2: Improved deep & cross network and practical lessons for web-scale learning to rank systems. In Proceedings of the web conference 2021. 1785–1797.   
[35] Xuanhui Wang, Michael Bendersky, Donald Metzler, and Marc Najork. 2016. Learning to rank with selection bias in personal search. In Proceedings of the 39th International ACM SIGIR conference on Research and Development in Information Retrieval. 115–124.   
[36] Xiaojie Wang, Rui Zhang, Yu Sun, and Jianzhong Qi. 2019. Doubly robust joint learning for recommendation on data missing not at random. In International Conference on Machine Learning. PMLR, 6638–6647.   
[37] Xiaojie Wang, Rui Zhang, Yu Sun, and Jianzhong Qi. 2021. Combating selection biases in recommender systems with a few unbiased ratings. In Proceedings of the 14th ACM International Conference on Web Search and Data Mining. 427–435.   
[38] Yifan Wang, Peijie Sun, Min Zhang, Qinglin Jia, Jingjie Li, and Shaoping Ma. 2023. Unbiased Delayed Feedback Label Correction for Conversion Rate Prediction. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 2456–2466.   
[39] Hong Wen, Jing Zhang, Yuan Wang, Fuyu Lv, Wentian Bao, Quan Lin, and Keping Yang. 2020. Entire space multi-task modeling via post-click behavior decomposition for conversion rate prediction. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval. 2377–2386.   
[40] Wenhao Zhang, Wentian Bao, Xiao-Yang Liu, Keping Yang, Quan Lin, Hong Wen, and Ramin Ramezani. 2020. Large-scale causal approaches to debiasing post-click conversion rate estimation with multi-task learning. In Proceedings of The Web Conference 2020. 2775–2781.   
[41] Weinan Zhang, Tianqi Chen, Jun Wang, and Yong Yu. 2013. Optimizing top-n collaborative filtering via dynamic negative item sampling. In Proceedings of the 36th international ACM SIGIR conference on Research and development in information retrieval. 785–788.   
[42] Guorui Zhou, Xiaoqiang Zhu, Chenru Song, Ying Fan, Han Zhu, Xiao Ma, Yanghui Yan, Junqi Jin, Han Li, and Kun Gai. 2018. Deep interest network for click-through rate prediction. In Proceedings of the 24th ACM SIGKDD international conference on knowledge discovery & data mining. 1059–1068.   
[43] Feng Zhu, Mingjie Zhong, Xinxing Yang, Longfei Li, Lu Yu, Tiehua Zhang, Jun Zhou, Chaochao Chen, Fei Wu, Guanfeng Liu, et al. 2023. DCMT: A Direct Entire-Space Causal Multi-Task Framework for Post-Click Conversion Estimation. arXiv preprint arXiv:2302.06141 (2023).