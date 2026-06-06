# ENLD: Efficient Noisy Label Detection for Incremental Datasets in Data Lake

Xuanke You∗, Lan Zhang∗, Junyang Wang∗, Zhimin Bao†, Yunfei Wu† and Shuaishuai Dong†

∗University of Science and Technology of China, †Tencent Group

yxkyong@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, iswangjy@mail.ustc.edu.cn, {zhiminbao, marcowu, shuaidong}@tencent.com

Abstract—Due to the difficulty of obtaining high-quality data in real-world scenarios, datasets inevitably contain noisy labeled data, leading to inefficient data usage and poor model performance. Thus, noisy label detection is an important research topic. Previous efforts mainly focus on noisy label detection on specific datasets that have been collected. Some works select clean samples based on relations between representations during the training process; some works utilize confidence outputs of a pre-trained model for noisy label detection. However, how to perform efficient and fine-grained noisy label detection on constantly arriving datasets in a data lake with a large amount of inventory data has not been explored. The rapidly growing volume and changing distribution of data make conventional methods either incur large computation overhead due to repeated training or become increasingly ineffective on newly arriving data. To address these challenges, in this work, we propose a novel approach ENLD to perform efficient and accurate noisy label detection on incremental datasets. Our extensive experiments demonstrate that ENLD outperforms the next best method in both efficiency and accuracy, which achieves 3.65×-4.97× detection speedup and higher average f1 scores with various noise rate settings.

# I. INTRODUCTION

In recent years, deep learning has made great achievements in various academic and industrial fields, which usually rely on a large number of labeled datasets [1] [2]. However, in the real world, both amateurs and experts inevitably produce noisy labeled data [3]. Therefore, noisy label detection and learning with noisy data have attracted much attention.

In industry, ubiquitous data lakes or data platforms provide massive data for deep learning systems, which also pose a huge challenge to data quality management [4]. There are two mainstream approaches to deal with noise labels, robust architecture and sample selection. Robust architecture reduces the influence of noisy labels to obtain a deep model with better performance by proposing robust training methods, such as noisy adaptation layer [5] [6], loss correction [7] [8] and label refurbishment [9] [10]. Sample selection explicitly filters noisy labeled data considering the impact of samples on training loss or the softmax output of deep models. Compared with the robust architecture, it can obtain a clean dataset with stronger reusability. A widely adopted idea for sample selection is to use some selection metrics (e.g. loss tracking) on samples during multiple rounds of the training process, such as O2U-Net [11] and INCV [12]. Topofilter [13] proposes a graphbased method in the latent representational space to collect clean data and drop isolated data. Confident learning [14] designs a framework to filter noisy labeled data with directly estimated joint distribution of noisy labels and unknown true labels based on confidence outputs of the deep model which is trained on noisy datasets.

Previous work, however, focus on datasets that have been collected. But for real-world data lakes and platforms, new data usually arrive constantly. Many platforms need to constantly perform accurate and efficient label quality assessments on newly arriving data, such as crowdsourcing platforms and data trading platforms [15] [16] [17]. Directly adopting existing training-based methods, e.g., Topofilter [13] and other loss tracking methods [11] [12], to detect noisy labels in incremental data is difficult to achieve good performance due to the lack of sample diversity and unbalanced categories in the incremental dataset. But applying those methods to both the inventory dataset and incremental dataset leads to a huge computation overhead due to the excessive sample number of the inventory data. Besides, the noisy label detection model trained on the inventory dataset usually cannot well adapt to specific incremental datasets. Pretrain-based methods, like confident learning [14], have low computation overhead but poor performance of noisy label detection for incremental datasets due to the changing data distribution. How to achieve efficient and accurate noisy label detection on constantly arriving datasets in a data lake is still an unexplored problem.

In this work, we focus on efficient and adaptive noisy label detection on constantly arriving incremental datasets in a data lake with a large amount of inventory data, and address the following challenges:

(1) How to leverage the knowledge from massive inventory data and how to adapt to the unknown data distribution of incremental data? Incremental datasets usually only contain a small number of samples from a part of classes of the inventory data and have unbalanced class distributions. Using the incremental datasets only cannot achieve satisfactory noisy label detection. It is crucial to mine and establish associations between incremental datasets and the inventory data, as well as to select proper samples from the inventory data as contrastive samples to improve the detection performance and reduce the training cost. During the selection of contrastive samples, it is necessary to consider the data distribution of incremental datasets for better adaptivity.

(2) How to ensure efficiency and performance during performing continuous noisy label detection tasks? The platform will receive a large number of continuous noisy label detection tasks, each of which is time-consuming and computationally expensive. This requires our approach to be designed and implemented in a way that ensures both efficiency and performance.

Facing the above challenges, we propose a novel framework ENLD to efficiently perform noisy label detection on incremental datasets. The core idea of our design is to sample contrastive samples in inventory data, which greatly benefit identifying ambiguous samples in incremental datasets, and discover clean samples by majority voting through multiple fine-tuning processes. Specifically, ENLD is a two-stage framework. First, ENLD trains a general model and estimates the conditional probability of label mislabeling through inventory data. Then, ENLD conducts fine-grained noise label detection with contrastive sampling for specific incremental datasets, including multiple re-sampling and model fine-tuning. Our contributions are summarized as follows:

•We propose a novel framework ENLD to efficiently perform noisy label detection on incremental datasets. We consider label probabilities, output confidences of samples, and relationships between feature representations, and carefully design a set of techniques including contrastive sampling and fine-grained noisy label detection. ENLD achieves superior noisy label detection performance for newly arriving datasets, requiring only a small amount of fine-tuning.

•We analyze the rationality of the selected samples in contrastive sampling. Our analysis proves that the high-quality samples in inventory data that are close to the representations of ambiguous samples in incremental datasets can bring greater benefits to the training process. We also compare the influence of different sampling strategies on the fine-grained noise label detection in experiments.

•We extensively evaluate our framework on public datasets with various noise settings. Experiments demonstrate that our framework outperforms existing methods in both performance and efficiency for noisy label detection on incremental datasets. The average f1 score of ENLD achieves 0.9191 for EMNIST and 0.8194 for CIFAR100 for various noise settings, which outperforms the next best method, Topofilter. Compared with Topofilter, ENLD also achieves 4.09× and 3.65× detection speedup on average process time for EMNIST and CIFAR100, respectively. For a more complex classification task, Tiny-Imagenet, ENLD performs significantly better than the baseline methods. It achieves an average f1 score of 0.7297 while the average f1 score of Topofilter is only 0.6171, and achieves 4.97× detection speedup on average process time.

# II. RELATED WORK AND PRELIMINARIES

# A. Noisy Label Detection Methods

In noisy learning, recent works focus on methods of sample selection [18] [19], which attempts to first select clean samples in the dataset and train the DNN on the filtered cleaner dataset. Decouple [20] maintains two DNNs and selects clean samples for the model update by the difference in label predictions between two DNNs. MentorNet [21] completes sample selection through a collaborative learning method, in which the pre-trained mentor DNN guides the training of a student DNN, and the student receives clean samples with a high probability provided by the mentor. Co-teaching [22] maintains two DNNs, each DNN completes the selection of small loss samples and shares the results with another DNN for future training. Based on Co-teaching, Co-teaching Plus [23] integrates the disagreement strategy of Decouple. INCV [12] randomly splits the dataset into two parts and selects clean data through cross-validation. SELFIE [24] selects clean data by small-loss criteria and selective refurbishment of samples. [13] proposes a graph-based method in the latent representational space named Topofilter to collect clean data and drop isolated data. Confident learning [14] proposes a framework to filter noisy label data with directly estimated joint distribution of noisy label and unknown true label based on the softmax output of the deep model, which is trained on noisy datasets. However, previous works focus on collected datasets. It is not applicable to the scenario where noisy label detection needs to be performed repeatedly on the newly added datasets. In this work, we mainly focus on how to conduct efficient and accurate noisy label detection for incremental datasets.

# B. Sample Selection Strategy

ENLD involves a sample selection process in inventory data for incremental datasets during the training process, and there are also many data selection strategies used in active learning methods [25] and semi-supervised learning methods [26]. And in active learning, the information entropy and confidence are widely used metrics to measure the uncertainty of samples for current models. It means samples with large uncertainty will bring great benefits to the training of the current model. Methods [27] [28] adopt the uncertainty-based sampling strategies to select samples during the training process. Moreover, the samples with the highest confidence tend to be selected and given a pseudo label to participate in the training in semisupervised learning methods [29] [30] [31] and active learning methods [32]. In this work, we also conduct experiments on replacing different sampling strategies in the fine-grained noisy label detection method of ENLD to explore the impact of different sample selection strategies in Section V.

# III. PROBLEM AND MAIN IDEA

# A. Problem Description

Given a large amount of inventory data (e.g. in a data lake) $I = \{ ( x _ { i } ^ { I } , \tilde { y } _ { i } ^ { I } ) \}$ with a number of classes and samples, the system needs to perform noisy label detection on incoming incremental datasets $D = \{ ( \bar { x } _ { i } ^ { D } , \tilde { y } _ { i } ^ { D } ) \}$ }. Here, iy˜ represents the observed label. y∗i represents the unknown true label. The noise label in both I and D is generated by a label probability transition matrix $T _ { i , j } ~ = ~ P ( \tilde { y } ~ = ~ j | ^ { * } ~ = ~ i )$ . It represents the probability of mislabeling between labels in manual experience. In the actual scenario, $D _ { i } { \mathrm { m a y } }$ be the dataset collected by the data platform or the dataset expected to obtain noisy label detection results from the data platform. The goal of our framework is to efficiently perform accurate noisy label detection on the incremental dataset. Important notations are summarized in Table. I.

TABLE I: Notation used in ENLD. 

<table><tr><td>Notation</td><td>Definition</td></tr><tr><td> $\tilde{y}$ </td><td>The observed label of the sample</td></tr><tr><td> $y^{*}$ </td><td>The true label of the sample</td></tr><tr><td> $I$ </td><td>The inventory data in the data platform</td></tr><tr><td> $D$ </td><td>The constantly arriving incremental datasets</td></tr><tr><td> $H$ </td><td>The high-quality samples in the inventory data</td></tr><tr><td> $A$ </td><td>The ambiguous samples in the incremental dataset</td></tr><tr><td> $\theta$ </td><td>The general deep model trained with the inventory data</td></tr><tr><td> $\theta'$ </td><td>The finetuned model for incremental datasets based on  $\theta$ </td></tr><tr><td> $M(x,\theta)$ </td><td>The confidence output of sample  $x$  by the deep model  $\theta$ </td></tr><tr><td> $\hat{M}(x,\theta)$ </td><td>The feature vector of sample  $x$  by the deep model  $\theta$ </td></tr><tr><td> $x_{i}^{L},\tilde{y}_{i}^{L}$ </td><td>The samples and observed labels in set  $L$ </td></tr></table>

# B. Main Idea

If we directly use the confidence outputs of a pre-trained general model on the incremental dataset to detect noisy samples, the performance is very dependent on the generalization ability of the general model trained by noisy labels, which often performs poorly on complex classification tasks. And previous training-based methods on the inventory dataset and incremental data will introduce a lot of computing overhead, which is not applicable to our scene as well.

To achieve requirements of high efficiency and accuracy, we expect to spend only a small amount of fine-tuning to achieve superior noisy label detection results for specific new datasets. Thus, we propose a two-stage framework for noisy label detection on incremental datasets, which maintains a general model and find-tune on different incremental datasets. Meanwhile, different incremental datasets have different data distributions and ambiguous samples for the general deep model. Here, ambiguous samples mean that their observed labels and predicted labels of the current model are inconsistent as defined in Definition. 1. The main idea of our work is to select high-quality contrastive samples for ambiguous samples in incremental datasets, and then finetune the model on specific data distribution to achieve accurate noisy label detection results. We consider label probabilities, output confidences, and feature representations of the current model to select contrastive samples which greatly benefit identifying ambiguous samples in incremental datasets in contrastive sampling.

# IV. FRAMEWORK OF ENLD

In this section, the detailed design and implementation of ENLD will be introduced. We will first describe the framework overview of ENLD, then contrastive sampling, fine-grained noisy label detection, and finally the model update.

# A. Framework Overview

We describe and introduce the framework overview of our proposed ENLD as shown in Algorithm 1 and Fig. 1. The platforms suitable for deploying the ENLD framework have a certain amount of inventory data, and incremental datasets with noise label detection requests arrive continuously. As for the platform, first, ENLD divides the inventory data I into $I _ { t }$ and $I _ { c }$ randomly. And then, ENLD initializes a general model θ with It and estimate the probability of P˜(y∗ = j|y˜ = i). $I _ { t }$ $\bar { \ell } y ^ { * } = j | \tilde { y } = i )$ After the initialization of ENLD, the noisy label detection of incremental data sets can be performed. For example, when an incremental dataset $D$ arrives, ENLD first performs contrastive sampling on current D to obtain an initial contrastive sample set C. Then a fine-grained noisy label detection method with re-sampling will be performed to obtain the selected clean part $S$ and noisy part N of D based on the general model θ. Moreover, during the noisy label detection process of incremental datasets, the system can also perform data selection for the inventory data. The platform can choose to update the general model and re-estimate the probability of $\tilde { P } ( y ^ { * } = j | \tilde { y } = i )$ .

# Algorithm 1 Framework of Efficient Noisy Label Detection (ENLD)

Input: the inventory data $I ~ = ~ \{ ( x _ { i } ^ { I } , \tilde { y } _ { i } ^ { I } ) \}$ , the incremental datasets $\{ D _ { i } \} _ { i = 1 } ^ { t }$ ,the parameter of contrastive samples sizek

Output: the noisy label detection result $S _ { i } .$ , $\ l _ { \ i } ^ { N }$

1: $\theta , \tilde { P } , I _ { t } , I _ { c } =$ model init(I);   
2: $H = \{ ( x , \tilde { y } ) \in I _ { c } :$ : argmax $M ( x , \theta ) = \tilde { \{ \} }$   
3: $S _ { c } = \varnothing ;$   
4: while $D _ { i }$ arrives do   
5: $H ^ { \prime } = \{ ( x , \tilde { y } ) \ : \ \tilde { y } \in l a b e l ( D _ { i } )$ and $( x _ { \tilde { y } ) } \in H \}$   
6: $A = \{ ( x , \tilde { y } ) \in D _ { i }$ : argmax $M ( x , \theta ) _ { \sharp } ^ { \flat } { \tilde { \upsilon } } \colon$   
7: C = contrastive sampling(A, $H ^ { \prime } , \tilde { P } , \tilde { k } , \tilde { \ell }$   
8: $S _ { i } , N _ { i } , S _ { c } ^ { \prime } = f i n e d \_ g r a i n e d \_ N L D ( C , \underline { { { D } } } _ { i } ^ { \prime } , \theta ) ;$   
9: $S _ { c } = S _ { c } \bigcup S _ { c } ^ { \prime } ;$   
10: θ, P , I ˜ t, Ic = model update(Sc, It, Ic); // Optional; $\theta , { \tilde { P } } , I _ { t } , I _ { c } = m o d e l \_ u p d a t e ( S _ { c } , I _ { t } , J _ { \xi } , I _ { \xi }$   
11: end while

# B. Model Initialization & Probability Estimation

In this part, the system needs to obtain a general model and estimate the probability of label mislabeling.

Model Initialization: First, we divide the inventory dataI into It and Ic uniformly and randomly. Here,I represents $I _ { t }$ $I _ { c }$ $\mathrm { H e r e } _ { { \mathscr I } _ { t } }$ the training set which is used to initialize and train a general model θ, and $I _ { c }$ is the candidate set for contrastive samples to accommodate special incremental datasets. In the system implementation, we use $I _ { t }$ to train the initialization model with the augmentation method Mixup [33]. Mixup randomly mixes the samples and labels with a Beta distribution for generalization performance as shown in Eq. 1 and Eq. 2, where $\lambda \sim B e t a ( \alpha , \alpha )$ . We set the parameter of the Beta distribution α = 0.2 in all experiments in Section V.

$$
\hat {x} = \lambda x _ {i} + (1 - \lambda) x _ {j} \tag {1}
$$

$$
\hat {y} = \lambda y _ {i} + (1 - \lambda) y _ {j} \tag {2}
$$

Probability Estimation: According to the assumptiony˜∗ = argmax $\tilde { p } ( \tilde { y } ; x , \theta )$ in [12], it means that the predicted label and the true label have the same distribution. We utilize the confidence output of the model M(x, θ) onIc and observed $M ( x , \theta ) ~ \mathrm { o p } _ { \pmb { f } _ { c } }$ label of each sample to estimate the joint distributionJ of true label $y ^ { * }$ and observed label y˜ as shown in Eq. 3 and Eq. 4. Here, $M ( x , \theta ) = ( o _ { 1 } , o _ { 2 } , . . . , o _ { l } )$ represents the softmax output of each class by deep model θ and the input sample x. $o _ { i }$ represents the confidence of class i and l represents the total categories of the classification task. And argmax $M ( x , \theta )$ represents the predicted label of the sample x.

![](images/f4e8848a7b7df2b567881ca6091f03c5fab74f68374db79d9e53ea831242c929.jpg)



Fig. 1: Overview of ENLD framework. Step 0: ENLD initializes a general model θ and estimated the conditional probability. Step 1& Step 2: ENLD performs fine-grained noisy label detection with contrastive sampling for each dataset when incremental datasets arrive. Optional Step: ENLD can choose to update the general model and re-estimate the conditional probability by the model update process. The dash line between the general deep model and candidate samples means that ENLD utilizes the general model to select high-quality samples from candidate samples for contrastive sampling.

$$
J _ {i, j} = \left| D _ {\tilde {y} = i, y ^ {*} = j} \right| \tag {3}
$$

$$
D _ {\tilde {y} = i, y ^ {*} = j} = \{x \in D _ {\tilde {y} = i}: \text { argmax } M (x, \theta) = j \} \tag {4}
$$

As shown in Eq. 5, we can estimate the conditional probability $\tilde { P } ( y ^ { * } = j | \tilde { y } = i )$ of observation labels and true labels through the estimated joint distribution J :

$$
\tilde {P} (y ^ {*} = j | \tilde {y} = i) = \frac {\tilde {P} (y ^ {*} = j , \tilde {y} = i)}{\tilde {P} (\tilde {y} = i)} = \frac {J _ {i , j}}{\sum_ {k} J _ {i , k}} \tag {5}
$$

Finally, we obtained the general model θ for fine-grained noisy label detection and the estimated conditional probabilities $\tilde { P }$ that will be used in the contrastive sampling method.

# C. High-quality and Ambiguous Samples

Definition 1. We define the samples with argmax $M ( x , \theta ) \neq$ y˜ in the incremental dataset D as the set of ambiguous samples A. And we define the samples with argmax $M ( x , \theta ) = \tilde { y }$ in the inventory data I as the set of high-quality samples H.

In this section, we introduce the definition of high-quality samples in inventory data and ambiguous samples in the incremental data as shown in Definition. 1 by the predicted label of the model θ and observed label. We define the sample in the incremental dataset D whose predicted label is inequal to the observed label as an ambiguous sample. We only sample contrastive samples for ambiguous samples rather than all samples in the incremental dataset in order to reduce the number of contrastive samples. And we define the sample in the inventory dataset $I _ { c }$ whose predicted label is equal to the observed label as a high-quality sample. In the subsequent comparative sampling process, we expect the selected sample in contrastive sampling to be a clean sample.

# D. Contrastive Sampling

In this section, we propose contrastive sampling to provide high-quality contrastive samples for the ambiguous samples in D. The core idea is to select contrastive samples with great training benefits for ambiguous samples in fine-tuning of finegrained noisy label detection. To achieve this goal, we expect to select samples that have proximate feature representations with the targeted ambiguous sample and have the same true labels as the ambiguous samples. For example, a sample with an observed label ’bowl’ in D is an ambiguous sample. Intuitively, selecting a clean sample with the label ’bowl’ and similar feature representations to finetune the general model is helpful to determine whether the ambiguous sample is a noise sample. We carry out theoretical and experimental analysis on this intuition.

As shown in Algorithm 1 and Algorithm 2, when the noisy label detection request of a new dataset arrives, contrastive sampling will be utilized to obtain an initial contrastive sampling set $C ,$ and then it will be performed repeatedly in the fine-grained noisy label detection method to update the set C during the training process. First, we give a hyperparameter k, which represents the size of contrastive samples $k | A |$ in each sampling process. For each ambiguous sample, we first determine the label according to the estimated probability $\tilde { P } .$ . According to Corollary 1, for a specific incremental dataset D, we only select contrastive samples in a subset $H ^ { \prime }$ in $I _ { c }$ which contains observed labels in $l a b e l ( D )$ . Here, $l a b e l ( D )$ represents the label set of D. Because, according to Corollary 1, the true label of a sample will be contained in label(D) with probability of $1 - ( 1 - P ( \stackrel {  } { y } = m | y ^ { * } = m ) ) ^ { | D ^ { m } }$ |. In practice, the probability of mislabeling $1 - P ( \tilde { y } = m | y ^ { * } = m )$ is usually low. Therefore, as long as there is a certain number of $D ^ { m }$ in the D, the true label m will have a great probability of being included in label(D). Here, $D ^ { m }$ represents samples in dataset $D$ whose true labels are class m. And then, for an ambiguous sample $x _ { i } ,$ we choose the k nearest samples in the high-

Algorithm 2 Contrastive Sampling

Input: the ambiguous samples of incremental dataset A, the high-quality samples of inventory data H, the estimated probability ${ \tilde { P } } ,$ parameter of contrastive samples size k, the general model θ

Output: the contrastive samples C   
1: $C = \emptyset;$ 2: $A = \{A_i\};$ 3: for $A_i$ in A do
4:    for $x_i$ in $A_i$ do
5: $j = random\_label(i, \tilde{P}, label(H'));$ 6: $C_i = k\_nearest(M(x_i, \theta), H_j, k);$ 7: $C = C \cup C_i;$ 8:    end for
9: end for
10: return C

![](images/d7e67e8bb050fca6e9e895145f1c017c733100f1f7bd2bc756579b3a8c6116ef.jpg)



Fig. 2: An example of contrastive sampling.

quality samples in inventory data by the output representations $\hat { M } ( x , \theta )$ in Euclidean distance as the contrastive samples $C _ { i }$ as shown in Eq. 7. $\hat { M } ( x , \theta ) = ( v _ { 1 } , v _ { 2 } . . . , v _ { c } )$ represents the feature output in front of softmax classifier layer by the deep model θ with the input sample x. Here, c represents the length of feature representations $\hat { M } ( x , \theta )$ .

Corollary 1. In an incremental dataset D, if samples of class $D ^ { m } = \{ ( x _ { i } , \tilde { y } _ { i } ) | y ^ { * } = m \}$ in D is collected uniformly from the true data distribution of class m. Then, the probability of class m not in label(D) is $( 1 - P ( \tilde { y } = m | y ^ { * } = m ) ) ^ { | D ^ { m } | } .$ .

Poof Sketch. According to the conditional probability $P ( \tilde { y } =$ $m | y ^ { * } = m )$ , the probability of mislabeling represents:

$$
\hat {P} = 1 - P (\tilde {y} = m | y ^ {*} = m) \tag {6}
$$

The probability of class m not in label(D) is equivalent to that all samples $D ^ { m }$ are mislabeled, and the probability is $( 1 - P ( \tilde { y } = \stackrel { \cdot } { m } | y ^ { * } = m ) ) ^ { | D ^ { m } | }$ .

$$
S (x _ {i}, x _ {j}) = | | \hat {M} (x _ {i}, \theta) - \hat {M} (x _ {j}, \theta) | | \tag {7}
$$

Finally, we obtain a contrastive sample set C for the ambiguous set A. According to Corollary 2, ideally, if the estimated probability $\tilde { P } ( y ^ { * } = i | \tilde { y } = k )$ is equal to the true probability $P ( y ^ { * } = i \vert \tilde { y } = k )$ , the label distribution $L ( C )$ of sampled contrastive set will be the same as the true label distribution $L ( A )$ of set A.

Corollary 2. (Ideal) $L ( C )$ represents the label distribution of set C. If the estimated probability $\tilde { P } ( y ^ { \ast } = i | \tilde { y } = k ) = P ( y ^ { \ast } =$ $i | \tilde { y } = k )$ , the sampled contrastive set satisfies $E ( L ( C ) ) =$ $L ^ { * } ( A )$ , where $P ( y ^ { * } = i | \tilde { y } = k )$ represents the true conditional probability and $L ^ { * } ( A )$ represents the true label distribution of set A.

Poof Sketch. According to the Algorithm 2, the expected label distribution of set C represents:

$$
E (L (C)) _ {i} = \sum_ {k} L (A) _ {k} \cdot \tilde {P} (y ^ {*} = i | \tilde {y} = k) \tag {8}
$$

According to the total probability theorem:

$$
L ^ {*} (A) _ {i} = \sum_ {k} L (A) _ {k} \cdot P (y ^ {*} = i | \tilde {y} = k) \tag {9}
$$

Thus, when $\tilde { P } ( y ^ { * } = i | \tilde { y } = k ) = P ( y ^ { * } = i | \tilde { y } = k )$ , we obtain $E ( L ( C ) ) _ { i } = L ^ { * } ( A ) _ { i }$ .

Moreover, we analyze the rationality of contrastive samples we select. First, we define the objective function of our model as min $l o s s _ { t e s t } ( \theta , A _ { t e s t } )$ . Here, $A _ { t e s t }$ is an unknown validation dataset that contains the same samples as the ambiguous set A and contains true labels rather than observed labels. As for $x _ { t e s t } = ( x _ { i } , y _ { i } ) \in A _ { t e s t } ,$ , the contribution of adding a contrastive sample $x ^ { I } = ( x _ { i } + \epsilon , y _ { i } )$ is shown in Definition 2. It means the loss gain of adding $x ^ { I }$ in epoch t on $x _ { t e s t }$ after training. According to the Corollary 3, if the gradient of loss function $\nabla _ { \theta _ { t } } l o s s ( \theta _ { t } , x )$ satisfies L Lipschitz smooth condition, the $\triangle I$ between adding $x ^ { I }$ and directly adding xtest will be less than $\alpha L | | \nabla _ { \theta _ { t - 1 } } l o s s ( \theta _ { t - 1 } , x _ { t e s t } ) | | \cdot | | \epsilon | |$ . It means adding correct contrastive samples with closer representations will bring greater benefits to the training process. This explains why we select the nearest samples as contrastive sampling in Algorithm 2.

Definition 2. $I = \{ ( x _ { i } ^ { I } , y _ { i } ^ { I } ) \}$ is the set of inventory data. $A = \{ ( x _ { i } ^ { A } , y _ { i } ^ { A } ) \}$ is the set of ambiguous data in the incremental dataset. $A _ { t e s t } = \{ ( x _ { i } , y _ { i } ) \}$ is the test set of correctly labeled data corresponding to A. The object function is min $l o s s _ { t e s t } ( \theta , A _ { t e s t } )$ .

Definition 3. The contribution of a sample x for each sample $x _ { t e s t } \in A _ { t e s t } ;$

$$
I (x, x _ {t e s t}) = \operatorname{loss} \left(\theta_ {t - 1}, x _ {t e s t}\right) - \operatorname{loss} \left(\theta_ {t}, x _ {t e s t}\right) \tag {10}
$$

Corollary 3. $\boldsymbol { x } _ { t e s t } = ( x _ { i } , y _ { i } )$ represents a sample in $A _ { t e s t } ,$ , and $x ^ { I } = ( x _ { i } + \epsilon , y _ { i } )$ represents a sample in the candidate set of constrasive samples. And $\triangle I ~ = ~ I ( x _ { t e s t } , x _ { t e s t } ) ~ -$ $I ( x ^ { I } , x _ { t e s t } )$ represents the contribution gap between adding $x ^ { I }$ and $x _ { t e s t } .$ . If the gradient of loss function $\nabla _ { \theta _ { t } } l o s s ( \theta _ { t } , x )$ satisfies Lipschitz Smooth condition, at epoch t, we get $\triangle I \leq$ $\boldsymbol { x } L | | \nabla _ { \theta _ { t - 1 } } l o s s ( \theta _ { t - 1 } , x _ { t e s t } ) | | \cdot | | \boldsymbol { \epsilon } | |$ .

Poof Sketch. At epoch t, with stochastic gradient descent after adding a sample x, the model will be updated as follows:

$$
\operatorname{loss} _ {\text { test }} = \operatorname{loss} \left(\theta_ {t}, A _ {\text { test }}\right) \tag {11}
$$

![](images/d1422fc5c0b93be3eb738c6d067fecd60bf28b11940a61b939987072976864ed.jpg)



(a) Noise Rate: 0.1

![](images/e9a469b012501835078c6bd9cad2674becf004a55ae64b5b8dedab7eb518f585.jpg)



(b) Noise Rate: 0.2

![](images/a734d5dfa737cc13c2d40ff98e37864e212940925578522bd50613dcf14917e5.jpg)



(c) Noise Rate: 0.3

![](images/aa71dd0982fc5d9e048f100fc6aa7c62723a6368f9823dbd8a8bd43714b0f35f.jpg)



(d) Noise Rate: 0.4   
Fig. 3: Evaluation loss of the validation set $D _ { t e s t }$ on incremental datasets of CIFAR100. Origin represents the original loss of general model θ. Random, Nearest-Only and Nearest-Related represent the loss after an epoch training by adding samples with true labels using different strategies.

$$
\theta_ {t} = \theta_ {t - 1} - \alpha \nabla_ {\theta} l o s s (\theta_ {t - 1}, x) \tag {12}
$$

Here, α is the learning rate. And the contribution of the sample x:

$$
I (x, x _ {t e s t}) = \text { loss } _ {\text { test }} (\theta_ {t - 1}, x _ {t e s t}) - \text { loss } _ {\text { test }} (\theta_ {t}, x _ {t e s t}) \tag {13}
$$

According to the Lagrange mean value theorem:

$$
\operatorname{loss} \left(\theta_ {t}, x _ {\text { test }}\right) = \operatorname{loss} \left(\theta_ {t - 1} - \alpha \nabla_ {\theta} \operatorname{loss} \left(\theta_ {t - 1}, x _ {i}\right), x _ {\text { test }}\right) \tag {14}
$$

$$
\begin{array}{l} \begin{array}{l} \text { loss } (\theta_ {t}, x _ {\text { test }}) = \text { loss } (\theta_ {t - 1}, x _ {\text { test }}) \\ \sum_ {i = 1} ^ {n} \left(0, \dots , (0, \dots)\right) \quad \sum_ {i = 1} ^ {n} \left(0, \dots , (0, \dots)\right) \end{array} \tag {15} \\ - \nabla_ {\theta_ {t - 1}} \text { loss } _ {\text { test }} (\theta_ {t - 1}, x _ {\text { test }}) \cdot \alpha \nabla_ {\theta_ {t - 1}} \text { loss } (\theta_ {t - 1}, x) \\ \end{array}
$$

Then we get:

$$
I (x, x _ {\text { test }}) = \alpha \nabla_ {\theta_ {t - 1}} \operatorname{loss} \left(\theta_ {t - 1}, x _ {\text { test }}\right) \cdot \nabla_ {\theta_ {t - 1}} \operatorname{loss} \left(\theta_ {t - 1}, x\right) \tag {16}
$$

And:

$$
\triangle I = I (x _ {t e s t}, x _ {t e s t}) - I (x ^ {I}, x _ {t e s t}) \tag {17}
$$

$$
\begin{array}{l} \triangle I \leq \alpha | | \nabla_ {\theta_ {t - 1}} l o s s (\theta_ {t - 1}, x _ {t e s t}) | | \\ \cdot \left| \left| \nabla_ {\theta_ {t - 1}} \operatorname{loss} \left(\theta_ {t - 1}, x _ {\text { test }}\right) - \nabla_ {\theta_ {t - 1}} \operatorname{loss} \left(\theta_ {t - 1}, x ^ {I}\right) \right| \right| \tag {18} \\ \end{array}
$$

According to the Lipschitz Smooth:

$$
\triangle I \leq \alpha L | | \nabla_ {\theta_ {t - 1}} \text { loss } (\theta_ {t - 1}, x _ {\text { test }}) | | \cdot | | \epsilon | | \tag {19}
$$

And we also conduct experiments to support this conclusion as shown in Fig. 3(a) ∼ Fig. 3(d). We set the general model θ as the initial training model for fine-tuning. $D _ { t e s t } = \{ ( x _ { t e s t } , y ^ { * } ) \}$ of D represents the validation set of noisy set in the incremental datasets. We add samples with true labels and train for an epoch to explore the impact of adding strategies on the contribution to the current model. Random represents adding $| D _ { t e s t } |$ samples with true label randomly from $I _ { c } .$ Nearest-Only represents adding $| D _ { t e s t } |$ | samples with closest representations to each $x _ { t e s t }$ from $I _ { c }$ and corresponding true labels. Nearest-Related represents adding $| D _ { t e s t } |$ samples with closest representations to each $x _ { t e s t }$ from $I _ { c }$ and true labels which are consistent with the true labels of

$x _ { t e s t } .$ . It can be concluded that the nearest strategy effectively enables the model to obtain adaptive training and the final loss on the validation set is significantly lower than the original loss and the loss of random sample selection. Compared with Nearest-Only, Nearest-Related is more likely to select samples that make greater contributions to the training process. And contrastive sampling is also a re-weighting process of sampled contrastive samples. Although contrastive sampling has sampled $k | A |$ times, the final sampled set C actually contains fewer samples than $k | A |$ . This is because some samples will be sampled more than once as shown in Fig. 2, which also indicates that these samples are more important for the current ambiguous sample set A. For example, a sample can be the contrastive sample for multiple ambiguous samples at the same time. The samples in the final sampled set C are equivalent to having different weights and then participate in the training process of fine-grained noisy label detection.

Implementation: Since constantly arriving datasets involves multiple k-nearest query operations, the original time complexity is $O ( c | A | | H ^ { \prime } | )$ . Thus, in implementation, we build KD-Tree structures for each category in H. KD-tree is a binary tree to organize vectors for more efficient nearest neighbor searching. This will reduce the time complexity of k-nearest operations to $O ( k | A | l o g | H ^ { \prime } | )$ . It improves the efficiency of the contrastive sampling that needs to be executed repeatedly.

# E. Fine-grained Noisy Label Detection

In this section, we introduce the fine-grained noisy label detection method in ENLD as shown in Algorithm 3. It mainly consists of the following four parts: (1) warming up process; (2) training and sample selection; (3) sample update and re-sampling; (4) data selection of inventory data. After contrastive samling, we can obtain an initial contrastive sample set C which is related to ambiguous samples in the incremental dataset. And the core idea of fine-grained noisy label detection is to fine-tune the general model on contrastive samples to select clean samples in incremental datasets. And the algorithm will adjust the representation and update the contrastive samples during the training process.

Algorithm 3 Fine-grained Noisy Label Detection

Input: the general model θ, the contrastive samples ${ \overline { { C , } } }$ the incremental dataset D, the candidate set of contrastive samples $I _ { c } ,$ the estimated probability ${ \tilde { P } } ,$ parameter of contrastive samples size $k ,$ the training iteration t and the step s in each iteration

Output: the clean set S and the noisy set N of the incremental dataset $D ,$ the selected clean samples $S _ { c }$ of $I _ { c }$

1: $S, N, S_c = \emptyset$ ;
2: $count_c = zeros(|D|)$ ;
3: $I' = \{(x, \tilde{y}) : \tilde{y} \in label(D) \text{ and } (x, \tilde{y}) \in I_c\}$ ;
4: $\theta' = warming\_up(\theta, C, validate = D)$ ;
5: for i in iteration do
6: $count = zeros(|D|)$ ;
7:    for s in step do
8: $\theta' = train(C, \theta')$ ;
9: $S_u = \{(x, \tilde{y}) : argmax M(x, \theta') = \tilde{y}, x \in D\}$ ;
10: $count = update(count, S_u)$ ;
11: $S_u = majority\_voting(count, S_u)$ ;
12: $S = S \cup S_u$ ;
13: $N = \{(x, \tilde{y}) | x \in D \text{ and } x \notin S\}$ ;
14:    end for
15: $A = \{(x, \tilde{y}) \in D : argmax M(x, \theta') \neq \tilde{y}\}$ ;
16: $H' = \{(x, \tilde{y}) \in I' : argmax M(x, \theta') = \tilde{y}\}$ ;
17: $count_c = update(count_c, H')$ ;
18: $S_c' = majority\_voting(count_c, H')$ ;
19: $S_c = S_c \cup S_c'$ ;
20: $C = contrastive\_sampling(A, H', \tilde{P}, k)$ ;
21: $C = C \cup S$ ;
22: end for
23: return $S, N, S_c$

Warming Up: At the first stage of the fine-grained noisy label detection, we utilize the initial contrastive sample set C and the incremental dataset D to train a better initialization model as shown in Algorithm 3. We use C to train the model θ for a given warming epoch number and verify the model on the incremental dataset D, and we selected the model with the highest validation accuracy during the warming up process.

Training and Sample Selection: There are two parameters to control the training process t and s. Here, t represents the total iterations of the training process and s represents the number of steps for training and clean sample selection in each iteration. In each iteration, we first initial a counting list and use it to count whether the predicted label in each step is equal to the observed label. In each step, we add the samples with more than $\lfloor \frac { s } { 2 } \rfloor + 1$ count times to the clean samples set $S .$ For example, if a sample with an observed label ’bowl’ in the incremental dataset is predicted as ’bowl’ by the deep model $\theta ^ { \prime }$ for more than $\lfloor { \frac { s } { 2 } } \rfloor + 1$ times after an iteration of finetuning, the sample will be selected as a clean sample. And then, with the updated model $\theta ^ { \prime } ,$ we update the ambiguous samples A and the high-quality samples $H ^ { \prime }$ together with the representations $\hat { M } ( x , \theta )$ . Finally, we perform contrastive sampling to obtain a new contrastive set $C$ and merge it with the selected set S to form a new $C$ to ensure the stability of the training process. Here, we expect to select samples in highquality samples as clean as possible, so we use the confidence output of θ to filter high-quality samples In practice, we filter the high-quality samples by average predicted probability $\begin{array} { r } { p ( y _ { x } ^ { f } = i ) \ge \frac { \sum _ { x } p ( y _ { x } ^ { \overline { { f } } } = i ) } { | \{ y _ { x } ^ { f } = i \} | } } \end{array}$ for cleaner contrastive samples. Here, $y _ { x } ^ { f }$ represents the predicted label argmax $M ( x , \theta )$ .

Sample Update and Re-sampling: In the end of each iteration, we utilize current model θ to update the ambiguous samples in D and the high-quality samples in $I ^ { \prime } .$ Then, the contrastive sampling method is called again to select contrastive samples for current ambiguous samples set A. Since the contrastive samples participate in the finetune training of fine-grained noisy label detection, the model will be more accurate in the selection of clean samples. The set of ambiguous samples in D will gradually decrease as shown in Fig. 13(b). We only use the current ambiguous samples set A to sample the contrastive samples, which can not only save the training cost by reducing the size of the contrastive samples, but also make the sampled contrastive samples more suitable for the current model and ambiguous samples.

Data Selection of Inventory Data: With the knowledge of noisy label detection on incremental datasets, we propose to select clean label $S _ { c }$ in each noisy label detection process for the model update of ENLD. We use the same counting method to count the number of times that each sample in the inventory data sample is determined to be a clean sample. In real scenarios, the inventory data usually serves multiple downstream tasks, so it is required that the selected samples of inventory data are as clean as possible. We adopt stringent clean data filter criteria as default for inventory data. Thus, we add the sample set $S _ { c } ^ { \prime }$ with t count times to the selected samples set $S _ { c }$ in each iteration.

# F. Model Update

After multiple noisy label detection tasks of incremental datasets, the system can choose to update the general model and re-estimate the probability. In this part, we introduce the model update process of ENLD as shown in Algorithm 4. ENLD utilizes the selected clean samples $S _ { c }$ in inventory data to update the model $\theta ^ { u }$ and validate the model on $I _ { t }$ to update the estimation probability $P .$ Instead, in the later stage, the original $I _ { t }$ is used as the candidate set $I _ { c }$ of contrastive samples. In Section ${ \mathrm { v } } ,$ we verify that model update does improve the generalization ability of the general model.

# V. EVALUATIONS

In this section, we introduce the evaluation results of our proposed framework ENLD and various compared methods with public datasets and various noise rate settings.

# A. Experimental Configuration

1) Datasets & Data Split: We use public image datasets, EMNIST [34], CIFAR100 [35] and Tiny-Imagenet [36]. We conduct three classification tasks, including a 26-categories

# Algorithm 4 Model Update

Input: the selected set $S _ { c }$ on $I _ { c } ,$ the inventory data $I _ { c }$ and $\overline { { I _ { t } } }$ Output: the updated model $\theta ^ { u }$ , the estimated probability $P ^ { u }$ , the updated $I _ { t } , I _ { c }$

1: $\theta ^ { u } = t r a i n ( S _ { c } ) ;$   
2: $I _ { t } , I _ { c } = s w a p ( I _ { t } , I _ { c } ) ;$   
3: $P ^ { u } = e v a l u a t e ( \theta ^ { u } , I _ { c } ) ;$   
4: return $\theta ^ { u } , P ^ { u } , I _ { t } , I _ { c }$

classification task on EMNIST letters with figure size (28, 28, 1) and a 100-categories classification task on CI-FAR100 with figure size (32, 32, 3) and a 200-categories classification task on Tiny-Imagenet with figure size (64, 64, 3). Firstly, We randomly divided each dataset into inventory data I and incremental dataset D according to the ratio of 2:1. As for EMNIST, we divide D into 10 unbalanced incremental datasets with 5 or 6 categories. As for CIFAR100, we divide D into 20 unbalanced incremental datasets with 10 categories. As for Tiny-Imagenet, we divide D into 20 unbalanced incremental datasets with 20 categories.

2) Asymmetric Noisy Label: To generate noisy labels, We corrupt the labels in our datasets with asymmetric noise, which is more realistic than symmetric (or uniform) noise. Asymmetric noise [3] means $\forall _ { i = j } T _ { i j } = 1 - \eta$ and $\exists _ { i \neq j , i \neq k , j \neq k } T _ { i j } >$ $T _ { i k }$ . In this work, we adopt the pair asymmetric noise (widely used in previous work), which means $\forall _ { i = j } T _ { i j } = 1 - \eta$ and $\exists _ { i \neq j } T _ { i j } = \eta$ . In our experiments, we adopt four noise rate settings $\eta \in \{ 0 . 1 , 0 . 2 , 0 . 3 , 0 . 4 \}$ .   
3) Metrics: In our experiments, we mainly focus on the performance and time cost of noise label detection on incremental datasets. As for performance, we focus on the precision, recall, and f1 score of the noisy label dataset $\tilde { D } _ { N } ^ { i }$ detected from the original dataset $D _ { i }$ And $D _ { N } ^ { i }$ represents the groundtruth of noisy label set in D. Thus, the precision metric is defined as $\begin{array} { r } { P = \frac { | D _ { N } ^ { i } \cap \tilde { D } _ { N } ^ { i } | } { | \tilde { D } _ { N } ^ { i } | } } \end{array}$ . The recall metric is defined as $\begin{array} { r } { R = \frac { | D _ { N } ^ { i } \cap \tilde { D } _ { N } ^ { i } | } { | D _ { N } ^ { i } | } } \end{array}$ . |D˜iN |The f1 score is defined as . |DiN | $\begin{array} { r } { F 1 = 2 \cdot \frac { P * R } { P + R } } \end{array}$

Time Cost: The cost time of performing noisy label detection on each incremental dataset, including the process time of each incremental dataset and the setup time. The process time represents the waiting time to obtain the noisy label detection results when a new dataset arrives. The setup time represents the time of system initialization, which mainly refers to the training time of model initialization before processing noise label detection requests in our experiments.

4) Baseline Methods: We compare methods of explicitly selecting clean samples or noise samples as the comparison method of noise label detection in recent years.

Default represents utilizing the general model θ to select the noisy label data by argmax $M ( x , \theta ) \neq \tilde { y }$ . Topofilter [13] utilizes the feature representation to construct KNN graphs and compute the largest connected component on each subgraph class by the class during a training process. Confident Learning [14] proposes a framework to filter noisy label data with directly estimated joint distribution of noisy label and unknown true label based on the softmax output of the deep model, which is pre-trained on noisy datasets. In our experiments, we utilize the general model θ trained onIt and validate on $\underline I _ { c }$ together with $D _ { i } .$ c. We report two methods in confident learning with the highest f1 score. Moreover, for a fair comparison, we perform Topofilter only on a subset of inventory dataI which is related to the label set of incremental datasetlabel(D ). $\mathsf { a s e } _ { \ell a b e l ( D _ { i } ) }$

i 5) Sampling Methods: We adjust the sample selection strategy in the fine-grained noisy label detection method in ENLD to analyze the impact of different strategies on the performance of noisy label detection on incremental datasets.

Random Policy: Random-ENLD uniformly and randomly selects samples in $I _ { c } ;$ Highest Confidence Policy: HCmax(M (x, θ)) according to outputs of current model inIc; ENLD selects samples (xi, y˜i) with highest confidence $( M ( x , \theta ) )$ $( \ v { x } _ { i _ { \widetilde { y } _ { i } } } )$ Least Confidence Policy: LC-ENLD selects samples(x , y˜ ) $\mathrm { s a m p l e s } _ { \left( x _ { i } , \tilde { y } _ { i } \right) }$ $^ { \mathrm { u } } { } _ { T _ { c } ; }$ i i with lowest confidence max(M(xi, θ)) according to outputs $\begin{array} { r } { m a x \big ( \underset { \mathbf { U } ( x _ { i } , \theta ) _ { 1 } } { \big ( } } \end{array}$ of current model in $I _ { c } ;$ Entropy Policy: Entropy-ENLD selected samples with highest entropy ofM(x, θ) according $^ \mathrm { o f } _ { M ( x , \theta ) }$ to outputs of current model inI ; Moreover, we also propose Pseudo-ENLD to select samples with highest confidence maxlabel $\left( M ( x , \theta ) \right)$ lace the observed labely˜ by a pseudo  by the current model $M ( x , \theta )$

6) Experiment Settings: Unless otherwise noted in our experiments, we use Resnet-110 [37] with universal crossentropy loss function in all of our experiments for various methods. To observe the generalization capability of ENLD, we also conduct experiments on Densenet-121 [38] and Resnet-164 [37] as shown in Section V-G. And we employ evaluations on the server with Inter(R) Xeon(R) CPU E5-2650 with 2.20GHz and Tesla P100 GPU. Unless otherwise noted in our experiments, we set the size of contrastive samplesk = 3, $\mathrm { s a m p l e g } _ { . } = 3 ,$ the training step $s = 5$ , and the warming up epoch equal to 2. We set the training iterationt = 5 for EMNIST and t = 17 for CIFAR100 and Tiny-Imagenet.

# B. Results of Incremental Noisy Label Detection

In this section, we compare the performance of various methods on incremental datasets of EMNIST, CIFAR100 and Tiny-Imagenet with various noise settings as shown in Fig. 4, Fig. 5 and Fig. 7. We demonstrate the cost time of noisy label detection on each incremental dataset as shown in Fig. 8 which contains both the setup time and process time. Default, Confident Learning, and ENLD have the same setup time of model initialization before performing noisy label detection for incremental datasets with 5438.2s for EMNIST, 18058.4s for CIFAR100, and 19716.7s for Tiny-Imagenet.

As shown in Fig. 4(c), Fig. 5(c) and Fig. 7(c), the trainingbased method, Topofilter, and ENLD, is obviously superior to the methods using only the confidence output of the general model, Default, Confident Learning methods (CL-1 and CL-2), but training process also brings additional computing overhead. Compared with the next-best method, Topofilter, ENLD achieves average f1 scores of 0.9191 for EMNIST and 0.8194 for CIFAR100 of various noise rate settings better than 0.9021 for EMNIST and 0.8139 for CIFAR100 of Topofilter. And as shown in Fig. 8, ENLD also improves the average process time of each incremental dataset by 4.09× for EMNIST and 3.65× for CIFAR100 compared with Topofilter. For a more complex classification task, Tiny-Imagenet, ENLD is significantly better than baseline methods in terms of performance and time cost. Compared with the next-best method, it achieves an average f1 score of 0.7297 better than 0.6171 of Topofilter and saves 4.97× process time. As for Default and CL methods, since there is no additional training process, the performance of its noise label detection depends very much on the initialized model. Therefore, when the classification task is relatively simple, such as EMNIST, the performance is better than that of CIFAR100 and Tiny-Imagenet when the data and classification are more complex. In summary, ENLD can efficiently and accurately obtain the noise label detection results of new arrival datasets compared with other baseline methods.

![](images/60514dad7c159810df22416ad9c0283d917fcd597d28add1fc53073168525fa3.jpg)



(a) Precision

![](images/a5ac991b64da2b7c8a624d485fea2cebce7856fcb4b7a924485e4671e0fd0bab.jpg)



(b) Recall

![](images/dc582c53fe8f2681608849bcb01265a710a60c9201da0b0fd22f6c8ac59cb2b3.jpg)



(c) F1 Score

Fig. 4: Performance of noisy label detection results with various detection methods on EMNIST. Average precision, recall and f1 score of 10 incremental datasets.   
![](images/8fed2dbbd492c9764a08bb3d5e137a0ccd42e5cbb57dba404178f4f21d0ed5af.jpg)



(a) Precision

![](images/47f1c2a79bdaac8509811cc41089fd62d9babaef5af9b577c10be3ec79537191.jpg)



(b) Recall

![](images/3bf2ef3fcf46813adc04d58c2e15bd638125c08fdd191baafe53cea8338e1cce.jpg)



(c) F1 Score

Fig. 5: Performance of noisy label detection results with various detection methods on CIFAR100. Average precision, recall and f1 score of 20 incremental datasets.   
![](images/8d0f3c3c1d415741f900553bf9bc399a5c503e687dbceb5253886950e1cf2382.jpg)



(a) Precision

![](images/e155cceed2525ade696634852ccbedc3988633e6dd0e16d702023e7fa5de3346.jpg)



(b) Recall

![](images/d8e0df6d681cc347550fc104a0814254683b777ab902a41267c86471b3907b1a.jpg)



(c) F1 Score   
Fig. 6: Performance of noisy label detection results with Densenet-121 and ResNet-164 on CIFAR100. Average precision, recall and f1 score of 20 incremental datasets.

# C. Training Process of ENLD

In this section, we demonstrate the noisy label detection process as shown in Fig. 9 when the noise rate is 0.1 ∼ 0.4 on CIFAR100. At the early stage of fine-grained noisy label detection, most samples are selected as noisy samples, so there is a high recall rate of noisy label detection. With the updating of the model and the re-sampling of the comparative samples, the precision and f1 score of noise label detection gradually increases while the recall slowly decreases. Finally, with the convergence of the method, the change tends to be gentle. In the case of low noise rate, the process of the finegrained noise detection process is relatively stable, resulting in a slow decline of label recall with the discovery of noise label data, and a large increase in the f1 score. However, when the noise rate is 0.4, the label recall will decrease greatly with the discovery of noisy samples, and the increase of the f1 score is small and tends to flatten quickly. Therefore, under different system requirements, the performance and process time can be balanced by setting training iterations t. In practice, for scenes with higher noise rates, smaller t can be selected to save the process time of fine-grained noisy label detection.

![](images/1822f906a3f63fad475e16903e8f3fa26be60de4e1c27fc39480c0db96479504.jpg)



(a) Precision

![](images/8b40acb6ed1ea40ad6a54aa7c9e68679a51b6f90e62f7d77ad203f131b8a7929.jpg)



(b) Recall

![](images/b66a2267989982bc33d837c5b9e9bd8b82fb8b19eb0f92204df269484b705791.jpg)



(c) F1 Score

Fig. 7: Performance of noisy label detection results with various detection methods on Tiny-Imagenet. Average precision, recall and f1 score of 20 incremental datasets.   
![](images/d7aa6ffa4e38cc809d80b0404a1688a86503f13aeb8278b9461b0eda51db4f4d.jpg)



(a) EMNIST

![](images/ee5f7033dcd0a88146685c5ee8449079f5c2337c00ab608b0720a3886feca3ce.jpg)



(b) CIFAR100

![](images/ff5a6256092f7a368ed7fb8afa927fa9771f3705573f76f698b614c09e19d83e.jpg)



(c) Tiny-Imagenet

Fig. 8: Setup time and process time cost of various methods on incremental datasts of datasets with various noise rate settings.   
![](images/cda99a470c1fbbf5121c5d8a3846d556cc1066f5eeb27652d0862cb1da5bbd27.jpg)



(a) 0.1

![](images/6d817d04784ebcdd8876a2a5f86f39d0a3865c33721443988de03ff20c4189df.jpg)



(b) 0.2

![](images/b3a49c6741bf6ce647184fea9400e1ef255e9254dfb453b69b10b0701668a32a.jpg)



(c) 0.3

![](images/5f440916c0f07147ca6b8279631469ed82afb24f8c416331dfc4da312bab8705.jpg)



(d) 0.4   
Fig. 9: Noisy label detection process of ENLD when the noise rate is 0.1∼0.4 on CIFAR100. Shaded regions indicate standard deviation over 20 incremental datasets.

# D. Results of Sample Selection Strategy

In this section, we compare the performance of utilizing various sample selection methods in the fine-grained noisy label detection method on incremental datasets of CIFAR100 with various noise settings 0.1∼0.4 as shown in Fig. 10. It can be concluded that the overall performance of original contrastive sampling is superior to other strategies for the noisy label detection tasks. Different from active learning, because the true label of the sample cannot be obtained, the gain of noisy label detection by adding the most uncertain sample of the current model selected by entropy and least confidence is low and close to the random policy. Compared with the entropy, least confidence, and random policy, the highest confidence policy, and pseudo policy have a higher probability to select cleaner samples or obtain clean labels, so they can provide a reference for the process of noise label detection. Therefore, its performance is obviously better than entropy, least confidence, and random policy.

# E. Model Update

In this section, we show the results of the model update process and data selection in ENLD. As shown in Table II, we demonstrate the validation accuracy on the entire set of incremental data and the other part of inventory data with original model θ and updated model θu by the data selection result $S _ { c }$ when the noise rate is 0.1∼0.4 on CIFAR100. With clean samples selected by multiple noisy label detection tasks on incremental datasets, the generalization performance of the updated model has been significantly improved compared with the original one.

![](images/3438695798fe2a122b7621dda29d2e56f9e36229e2c860586354ed6c56c44435.jpg)



(a) Precision

![](images/9daaf71c88c9409bc36f5bd5ee391d23ebb93d06be8d6209b998c3a730319d00.jpg)



(b) Recall

![](images/79a3a17bfb7731c20b356cce138ae8df85d0a9b072cfcc81e1e3bd1f2611bbb9.jpg)



(c) F1 Score

Fig. 10: Performance of noisy label detection results with various sample selection methods on CIFAR100. Average precision, recall and f1 score of 20 incremental datasets.   
![](images/734746d04765693dee11bd7ed294e347a38151376ebb607a6a6d319a14ebb9eb.jpg)



(a) Precision

![](images/5ce4715da717a19ad88a224ca652596fc287ccb6622540d835c374cea621fec5.jpg)



(b) Recall

![](images/ba3d733404766f028f9d9acd38a747ff5960b1b308d4ddcbbc42685e4349516a.jpg)



(c) F1 Score

Fig. 11: Performance of noisy label detection results with various hyperparameter settings on CIFAR100. Average precision, recall and f1 score of 20 incremental datasets.   
![](images/1821f46fc0abb74cab7ac9dc9a1641b50f39895c2904a39569992344a8631e2a.jpg)



Fig. 12: Average process time cost and average f1 score of hyperparameter settings on incremental datasets with CIFAR100 with various noise rate settings.

<table><tr><td>Noise Rate</td><td>0.1</td><td>0.2</td><td>0.3</td><td>0.4</td></tr><tr><td>Origin Model</td><td>58.93%</td><td>52.85%</td><td>45.08%</td><td>37.17%</td></tr><tr><td>Update Model</td><td>61.31%</td><td>57.06%</td><td>49.40%</td><td>37.23%</td></tr></table>

TABLE II: Validation accuracy on remaining data on CI-FAR100 by original model θ and updated model $\theta ^ { u }$ before and after the model update process.

# F. Hyperparameter Settings

In this part, we conduct experiments on various hyperparameter settings of contrastive samples size $k = \{ 1 , 2 , 3 , 4 \}$ as shown in Fig. 11 and Fig. 12. It can be concluded that the performance of fine-grained noisy label detection increases gradually with the number of samples sampled by contrastive sampling, which also consumes more process time generally. However, compared with the process time of k = 2 and k = 3, the average process time does not increase but decreases. This is because choosing a larger k represents that there will be more contrastive samples for each ambiguous sample, which will lead to faster convergence of the model in the finetune training process. We think that the difference between setting k = 2 and $k = 3$ becomes significant. This finally leads to the average process time of setting $k = 2$ higher than that of setting $k = 3 .$ . In our experiments, we choose a sampling size k = 3 with moderate performance and process time for all datasets and noise rate settings. Especially, Fig. 4(c), Fig. 5(c) and Fig. 7(c) show the f1 score of ENLD is slightly lower than that of the comparison method when the noise rate is 0.4. As shown in Fig. 11, increasing the sampling size can improve f1 scores when the noise rate is 0.4. Thus, we conduct experiments when $k \ = \ 4$ for each dataset. Finally, ENLD achieves average f1 scores of 88.06%, 73.86% and 72.62% for EMINST, CIFAR100 and Tiny-Imagenet, which are higher than 87.78%, 73.45% and 71.64% of the next best method, Topofilter. Therefore, we suggest that ENLD should choose a larger sampling size in the scene with a high noise rate.

# G. Different networks

To observe the generalization capability of ENLD, we also conduct experiments on ENLD and Topofilter with Densenet-121 and ResNet-164 on incremental datasets of CIFAR100 as shown in Fig.6(a). For different networks, ENLD achieves better performance than Topofilter and saves 2.46× and 2.64× process time for Densenet-121 and ResNet-164.

# H. Missing label cases

Missing label can be regarded as a special case of the noisy label. We carried out extensive experiments on ENLD to explore its ability to deal with missing labels. First, we randomly set 25%, 50% and 75% samples in incremental datasets of CIFAR100 as missing label data when the noise rate is 0.2. ENLD will give a pseudo label for each sample without the observed label in each step of fine-grained noisy label detection. Each sample without the observed label will obtain a final label by voting with pseudo labels. Fig. 13(a) shows the average f1 scores of the pseudo label and noisy label detection with different missing rates. It demonstrates that the higher the missing rate of the incremental dataset, the lower the performance of pseudo labels and noisy label detection.

![](images/b02def6a6d7030452aa8dd33f0fbe24ec773807d106e655943e960ea5661dc61.jpg)



(a) Performance

![](images/9e434adb0556f3830daced15ff912750e2e0ffe4b6238b30e362ee58c79007fb.jpg)



(b) Number of ambiguous samples   
Fig. 13: (a) Average f1 scores of the pseudo label and noisy label detection with different missing rates of incremental datasets when the noise rate is 0.2 on CIFAR100. (b) Numbers of ambiguous samples during the fine-grained noisy label detection process on incremental datasets on CIFAR100.

![](images/d1802fd8474c117ab849611752e717250d9ab329c062a78aac32bba2c66c458a.jpg)



(a) Performance

![](images/ddd1879033584c04ad6047ab9bc236ca72d000e9240e630f2b6c127713cbc212.jpg)



(b) Average Process Time   
Fig. 14: Ablation study results on ablation settings with various noise rate settings.

# I. Ablation Study

And we conduct ablation study on ENLD to figure out the importance of each part by removing each part of ENLD separately when the noise rate is 0.1∼0.4 on incremental datasets of CIFAR100. ENLD-Origin represents the original version of the ENLD method; Removing contrastive learning (ENLD-1), ENLD with randomly selected data from contrastive samples set, represents utilizing randomly chosen samples to update the model in each step instead of contrastive sampling; Removing majority voting (ENLD-2) represents update the clean set once the predicted label is equal to the observed one; without adding clean samples of the incremental dataset (ENLD-3), which means removing $C = C \cup S$ in fine-grained noisy label detection. And we also propose ENLD-4 by using $\ j \ = \ i$ directly instead of $j ~ = ~ r a n d o m \_ l a b e l ( i , \tilde { P } , l a b e l ( H ^ { \prime } ) )$ to query the nearest samples with the same observed label in the contrastive sampling method. As shown in Fig. 14, removing contrastive learning (ENLD-1) cause the overall performance of noise label detection to decline from 0.8139 to 0.6721 on the average f1 score. Therefore, contrastive learning is an essential part of ENLD. Removing majority voting (ENLD-2) means a more aggressive clean sample selection strategy. When the noise rate is low, the overall model is superior and the classification task is simple. A more aggressive clean sample selection strategy will bring a certain performance improvement. However, when the noise rate rises, removing majority voting will lead to greater randomness in the clean sample selection process, and the overall performance will be greatly reduced. Although without adding clean samples of incremental datasets during the training process (ENLD-3) reduces the process time of fine-grained noisy label detection to a certain extent, the performance is also greatly reduced due to the instability of its training process. As for ENLD-4, for the case of low noise rate 0.1, the strategy of directly selecting nearest samples that have the same observed label with ambiguous samples in contrastive sampling is better. However, for higher noise rates, such as 0.3 and 0.4, it is better to estimate the true labels of ambiguous samples according to the estimated conditional probability and then select highquality samples that have proximate representations.

# VI. CONCLUSION

In this work, we propose a novel framework ENLD to efficiently perform noisy label detection on incremental datasets, including the fine-grained noisy label detection method with contrastive sampling. The fine-grained noisy label detection method has the ability to achieve superior noisy label detection results for incremental datasets using only a small amount of fine-tuning, which involves label probabilities, output confidences, and relationships between the feature representations. The extensive experiments show the effectiveness of ENLD to perform noisy label detection on incremental datasets with various noise rate settings.

# VII. ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, and the Fundamental Research Funds for the Central Universities WK2150110024.

# REFERENCES

[1] M. M. Kamani, S. Farhang, M. Mahdavi, and J. Z. Wang, “Targeted datadriven regularization for out-of-distribution generalization,” in KDD ’20: The 26th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2020.   
[2] Y. Tang, F. Borisyuk, S. Malreddy, Y. Li, and S. Kirshner, “Msuru: Large scale e-commerce image classification with weakly supervised search data,” in the 25th ACM SIGKDD International Conference, 2019.   
[3] H. Song, M. Kim, D. Park, Y. Shin, and J.-G. Lee, “Learning from noisy labels with deep neural networks: A survey,” IEEE Transactions on Neural Networks and Learning Systems, 2022.   
[4] F. Nargesian, E. Zhu, R. J. Miller, K. Q. Pu, and P. C. Arocena, “Data lake management: challenges and opportunities,” Proceedings of the VLDB Endowment, vol. 12, no. 12, pp. 1986–1989, 2019.   
[5] S. Sukhbaatar, J. Bruna, M. Paluri, L. Bourdev, and R. Fergus, “Training convolutional networks with noisy labels,” arXiv preprint arXiv:1406.2080, 2014.   
[6] X. Xia, B. Han, N. Wang, J. Deng, J. Li, Y. Mao, and T. Liu, “Extended t: Learning with mixed closed-set and open-set noisy labels,” IEEE Transactions on Pattern Analysis and Machine Intelligence, 2022.   
[7] G. Patrini, A. Rozza, A. Krishna Menon, R. Nock, and L. Qu, “Making deep neural networks robust to label noise: A loss correction approach,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2017, pp. 1944–1952.   
[8] Y. Yao, T. Liu, B. Han, M. Gong, J. Deng, G. Niu, and M. Sugiyama, “Dual t: Reducing estimation error for transition matrix in labelnoise learning,” in Advances in Neural Information Processing Systems, H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin, Eds., vol. 33. Curran Associates, Inc., 2020, pp. 7260–7271.   
[9] S. E. Reed, H. Lee, D. Anguelov, C. Szegedy, D. Erhan, and A. Rabinovich, “Training deep neural networks on noisy labels with bootstrapping,” in International Conference on Learning Representations, 2015.   
[10] P. Chen, J. Ye, G. Chen, J. Zhao, and P.-A. Heng, “Beyond class-conditional assumption: A primary attempt to combat instancedependent label noise,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 35, no. 13, 2021, pp. 11 442–11 450.   
[11] J. Huang, L. Qu, R. Jia, and B. Zhao, “O2u-net: A simple noisy label detection approach for deep neural networks,” in Proceedings of the IEEE/CVF international conference on computer vision, 2019, pp. 3326– 3334.   
[12] P. Chen, B. B. Liao, G. Chen, and S. Zhang, “Understanding and utilizing deep neural networks trained with noisy labels,” in International Conference on Machine Learning. PMLR, 2019, pp. 1062–1070.   
[13] P. Wu, S. Zheng, M. Goswami, D. Metaxas, and C. Chen, “A topological filter for learning with label noise,” Advances in neural information processing systems, vol. 33, pp. 21 382–21 393, 2020.   
[14] C. Northcutt, L. Jiang, and I. Chuang, “Confident learning: Estimating uncertainty in dataset labels,” Journal of Artificial Intelligence Research, vol. 70, pp. 1373–1411, 2021.   
[15] L. Zhang, Y. Li, X. Xiao, X.-Y. Li, J. Wang, A. Zhou, and Q. Li, “Crowdbuy: Privacy-friendly image dataset purchasing via crowdsourcing,” in IEEE INFOCOM 2018-IEEE Conference on Computer Communications. IEEE, 2018, pp. 2735–2743.   
[16] M.-C. Yuen, I. King, and K.-S. Leung, “A survey of crowdsourcing systems,” in 2011 IEEE third international conference on privacy, security, risk and trust and 2011 IEEE third international conference on social computing. IEEE, 2011, pp. 766–773.   
[17] D. Hettiachchi, V. Kostakos, and J. Goncalves, “A survey on task assignment in crowdsourcing,” ACM Computing Surveys (CSUR), vol. 55, no. 3, pp. 1–35, 2022.   
[18] Y. Shen and S. Sanghavi, “Learning with bad training data via iterative trimmed loss minimization,” in International Conference on Machine Learning, 2019.

[19] H. Song, M. Kim, D. Park, and J. G. Lee, “Prestopping: How does early stopping help generalization against label noise?” 2019.   
[20] E. Malach and S. Shalev-Shwartz, “Decoupling ”when to update” from ”how to update”,” Advances in neural information processing systems, vol. 30, 2017.   
[21] J. Lu, Z. Zhou, T. Leung, L. J. Li, and F. L. Fei, “Mentornet: Learning data-driven curriculum for very deep neural networks on corrupted labels,” in ICML 2018, 2018.   
[22] B. Han, Q. Yao, X. Yu, G. Niu, M. Xu, W. Hu, I. Tsang, and M. Sugiyama, “Co-teaching: Robust training of deep neural networks with extremely noisy labels,” Advances in neural information processing systems, vol. 31, 2018.   
[23] X. Yu, B. Han, J. Yao, G. Niu, I. Tsang, and M. Sugiyama, “How does disagreement help generalization against label corruption?” in International Conference on Machine Learning. PMLR, 2019, pp. 7164–7173.   
[24] H. Song, M. Kim, and J. G. Lee, “Selfie: Refurbishing unclean samples for robust deep learning,” in Proceedings of the 36 th International Conference on Machine Learning, 2019.   
[25] P. Ren, Y. Xiao, X. Chang, P.-Y. Huang, Z. Li, B. B. Gupta, X. Chen, and X. Wang, “A survey of deep active learning,” ACM computing surveys (CSUR), vol. 54, no. 9, pp. 1–40, 2021.   
[26] J. E. Van Engelen and H. H. Hoos, “A survey on semi-supervised learning,” Machine Learning, vol. 109, no. 2, pp. 373–440, 2020.   
[27] T. He, X. Jin, G. Ding, L. Yi, and C. Yan, “Towards better uncertainty sampling: Active learning with multiple views for deep convolutional neural network,” in 2019 IEEE International Conference on Multimedia and Expo (ICME). IEEE, 2019, pp. 1360–1365.   
[28] N. Ostapuk, J. Yang, and P. Cudre-Mauroux, “Activelink: deep active ´ learning for link prediction in knowledge graphs,” in The World Wide Web Conference, 2019, pp. 1398–1408.   
[29] D.-H. Lee et al., “Pseudo-label: The simple and efficient semi-supervised learning method for deep neural networks,” in Workshop on challenges in representation learning, ICML, vol. 3, no. 2, 2013, p. 896.   
[30] W. Dong-DongChen and Z.-H. WeiGao, “Tri-net for semi-supervised deep learning,” in Proceedings of twenty-seventh international joint conference on artificial intelligence, 2018, pp. 2014–2020.   
[31] S. Qiao, W. Shen, Z. Zhang, B. Wang, and A. Yuille, “Deep co-training for semi-supervised image recognition,” in Proceedings of the european conference on computer vision (eccv), 2018, pp. 135–152.   
[32] K. Wang, D. Zhang, Y. Li, R. Zhang, and L. Lin, “Cost-effective active learning for deep image classification,” IEEE Transactions on Circuits and Systems for Video Technology, vol. 27, no. 12, pp. 2591–2600, 2016.   
[33] H. Zhang, M. Cisse, Y. N. Dauphin, and D. Lopez-Paz, “mixup: Beyond empirical risk minimization,” arXiv preprint arXiv:1710.09412, 2017.   
[34] G. Cohen, S. Afshar, J. Tapson, and A. Van Schaik, “Emnist: Extending mnist to handwritten letters,” in 2017 international joint conference on neural networks (IJCNN). IEEE, 2017, pp. 2921–2926.   
[35] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” 2009.   
[36] Y. Le and X. Yang, “Tiny imagenet visual recognition challenge,” CS 231N, vol. 7, no. 7, p. 3, 2015.   
[37] K. He, X. Zhang, S. Ren, and J. Sun, “Identity mappings in deep residual networks,” in European conference on computer vision. Springer, 2016, pp. 630–645.   
[38] G. Huang, Z. Liu, L. Van Der Maaten, and K. Q. Weinberger, “Densely connected convolutional networks,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2017, pp. 4700–4708.