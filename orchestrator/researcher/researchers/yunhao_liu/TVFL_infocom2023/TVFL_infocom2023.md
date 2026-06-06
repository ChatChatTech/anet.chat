# TVFL: Tunable Vertical Federated Learning towards Communication-Efficient Model Serving

Junhao Wang∗, Lan Zhang∗†, Yihang Cheng∗, Shaoang Li∗, Hong Zhang‡, Dongbo Huang‡, Xu Lan‡

∗ School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

† Institute of Dataspace, Hefei Comprehensive National Science Center, China

‡ Tencent, Shanghai, China

{junhaow,whcyh,lishaoa}@mail.ustc.edu.cn,{zhanglan}@ustc.edu.cn,{keyzhzhang,andrewhuang,lanxu}@tencent.com

Abstract—Vertical federated learning (VFL) enables multiple participants with different data features and the same sample ID space to collaboratively train a model in a privacy-preserving way. However, the high computational and communication overheads hinder the adoption of VFL in many resource-limited or delay-sensitive applications. In this work, we focus on reducing the communication cost and delay incurred by the transmission of intermediate results in VFL model serving. We investigate the inference results, and find that a large portion of test samples can be predicted correctly by the active party alone, thus the corresponding communication for federated inference is dispensable. Based on this insight, we theoretically analyze the “dispensable communication” and propose a novel tunable vertical federated learning framework, named TVFL, to avoid “dispensable communication” in model serving as much as possible. TVFL can smartly switch between independent inference and federated inference based on the features of the input sample. We further reveal that such tunability is highly related to the importance of participants’ features. Our evaluations on seven datasets and three typical VFL models show that TVFL can save 57.6% communication cost and reduce 57.1% prediction latency with little performance degradation.

# I. INTRODUCTION

There are two main categories of federated learning frameworks, horizontal federated learning (HFL) and vertical federated learning (VFL), based on the distribution of participants’ data in the feature space and sample ID space. In HFL, participants share the same feature space but have different sample IDs [1]–[7]; while in VFL, participants share the same sample ID space but have different data features [1], [8]–[10]. As VFL is being used in various businesses such as insurance assessment and financial risk control, the high computational and communication overheads of VFL hinder its adoption in many resource-limited or delay-sensitive applications, e.g., mobile computing and online advertising.

In this work, we focus on reducing communication cost and latency of VFL model serving. As shown in Fig. 1, in a typical VFL system, there are usually an active party who owns labels and a part of features and a passive party who owns only another part of features. Since samples and models are partitioned and distributed to two participants, they have to transmit a large amount of intermediate results (mainly the feature representations) during the federated inference process. Such a large communication overhead is unaffordable for some resource-limited devices, and can lead to a too long latency for many delay-sensitive applications. For example, in an online advertising system, an advertising company (the active party) can collaborate with an Internet company to train a more accurate ad recommendation model by VFL. However, millions of queries are generated per second during peak hours [11], [12] and the overall latency for each query, including audience identification, the VFL model inference and ad display, should be less than 100 ms [13]. Our experiments show that about 90% of the latency in the vertical linear models and vertical neural network models, and about 99% of the latency in vertical tree-based models come from the communication latency. Hence, reducing the communication cost and inference latency of VFL models is a strong requirement and a very challenging issue.

Though many previous efforts have been devoted to communication efficiency in FL systems, most of them focus on HFL. For HFL, a line of work reduce communication costs by restricting the number of participants [14]–[17]. Another line of work use compression techniques to reduce the total communication rounds between the server and participants [18]–[22]. Those approaches for HFL cannot be applied to VFL systems due to completely different learning paradigms. Recently, Castiglia et al. [23] propose Compressed Vertical Federated Learning (C-VFL) for communication-efficient training on vertically partitioned data. But it is only applicable to the VFL training phase, and cannot reduce the communication cost in the inference phase. SplitKD [11] utilizes the knowledge distillation technique to distill the knowledge from the VFL model to a local model and then uses the local model to make predictions, so as to save communication cost. But the local distilled model suffers from an obvious (about 9%) accuracy degradation.

There still lacks an effective approach to significantly reduce the communication overhead and inference latency of VFL model serving with negligible accuracy loss. To address this critical and challenging problem, we first investigate the inference results of VFL models and try to fully understand the return of the consumed communication costs. We find that a large portion of test samples can be predicted correctly by the active party alone, as shown in Table I. For example, for Census Income dataset DC, the prediction accuracy by the VFL model is 85.6%, while the independent prediction accuracy by the active party is 77.7%. It means that for 77.7% samples, the active party already has sufficient knowledge to make accurate predictions and there is no need to conduct federated inference with the passive party, so the corresponding 77.7% communication cost is completely unnecessary. We define this kind of communication as “dispensable communication”. If we can avoid “dispensable communication” in the inference stage, we can significantly reduce communication overhead and latency without sacrificing performance. Towards this ambitious goal, we need to answer three major questions:

![](images/e91921c33d4674a9b42895693c44de76a088efe45bac26ef5d9de0fbe1cfb77b.jpg)



Fig. 1. Online prediction serving in VFL system.

Question #1: Can the VFL system completely avoid the “dispensable communication” ?

Question#2: How to reduce the “dispensable communication” in the VFL system as much as possible with negligible accuracy degradation?

Question #3: What determines the extent to which communication overheads can be reduced?

For Question #1, we theoretically analyze the feasibility of VFL and prove that “dispensable communication” cannot be completely avoided in the VFL system. Fortunately, we can use an approximation algorithm to avoid a large portion of “dispensable communication”. Therefore, for Question #2, we propose a method to select the samples for which the active party cannot correctly predict alone. Moreover, leveraging this method, we design a model-agnostic tunable vertical federated learning framework, named TVFL, to cut down “dispensable communication” as much as possible with negligible accuracy degradation. For Question #3, we explore the influence of feature importance distribution on the tunability of TVFL. By randomly assigning features to the active party and passive party, and measuring their feature importance by SHAP [24], which is a well-known explainable machine learning technology, we find that the degree of communication savings using TVFL is positively correlated with the feature importance of the active party.

Our contributions are summarized as follows:

•A new problem: We point out the “dispensable communication” in VFL model serving and pose a new problem that how to avoid “dispensable communication” as much as possible with negligible accuracy degradation. This is a key challenge in reducing the communication cost and delay of VFL systems.

•A new VFL framework: We propose TVFL to smartly switch between local independent inference and vertical federated inference based on the features of the input sample, to reduce communication overhead and inference latency signif-

icantly. This framework is model-agnostic and can be applied to various VFL frameworks with different architectures.

•A new insight: We explore the influence of feature importance distribution on the tunability of TVFL, and find that the degree of communication savings using TVFL is positively correlated with the feature importance of the active party. The tunability of TVFL can be adopted as a new way to measure participants’ contributions.

•We evaluate our design via extensive experiments using both public and real-world datasets. And we implement the proposed framework TVFL on vertical logistical regression, vertical neural network, and vertical tree-based models. The experimental results demonstrate that our method can significantly reduce communication overhead and prediction latency, and there is only little accuracy degradation. For example, on vertical logistical regression, for the Sensorless drive diagnosis dataset, TVFL saves 57.6% communication cost and reduces 57.1% prediction latency while only reducing the accuracy by 2.9%.

# II. RELATED WORK AND PRELIMINARY

# A. Related Work

1) Communication Efficiency in Federated Learning: Much previous work has been devoted to communication efficiency of FL, but most of them focus on HFL. A series of work [14]–[17] restrict the number of participates to reduce communication costs, so that only a fraction of the local parameters are updated. Some work [25], [26] reduce the communication overhead by minimize model updates in the model training phase. Reisizadeh et al. [27] propose a decentralized and gradient-based optimization algorithm named QuanTimed-DSGD to reduce the participants’ delay and communication overhead. Tang et al. [28] design a framework of quantized decentralized training and two strategies, which outperform previous algorithms significantly for networks with both high latency and low bandwidth in terms of convergence rate and communication overhead. There are also many approaches [18]–[22] using compression techniques to reduce the total number of communication rounds between the server and the participants. However, all those methods are tailored for HFL and not applicable to VFL. Castiglia et al. [23] propose Compressed Vertical Federated Learning (C-VFL) for communication-efficient training on vertically partitioned data. But this approach is designed for the training stage and cannot reduce the overhead and delay of the inference stage.

Recently, SplitKD [11] utilizes the knowledge distillation technique [29] to distill the knowledge from the VFL model to a local model and then uses the local model to make predictions, so as to save communication cost. But the local distilled model suffers from an obvious (about 9%) accuracy degradation.

2) Model Inference Latency Optimization: In centralized machine learning, many work [30]–[34] use model pruning and quantization to reduce the enormous computational and memory overhead of deep neural networks and speed up the inference. There are also a lot of work using knowledge distillation to compress deep neural networks to improve inference speed [35]–[39]. Those techniques can be adopted to reduce the execution cost of participants’ local models. However, in VFL, more than 90% of the latency comes from communication. Those methods cannot reduce the significant communication overhead and latency caused by communication.

# B. Preliminary

VFL is designed for the scenario where participants datasets share the same sample ID space but differ in the feature space. VFL enables multiple participants to build of a global model by computing gradients with features from participants in a privacy-preserving manner, $\mathrm { e . g . }$ , using encryption techniques. We focus on a typical two-party VFL for classification tasks, where an active party holding the label and some features collaborates with a passive party who provides additional features to train a federated model. A denotes the passive party, who holds the dataset $\{ x _ { i } ^ { A } \} _ { i \in D _ { A } }$ , and B denotes the active party, who holds the datasets $\{ x _ { i } ^ { B } , y _ { i } \} _ { i \in D _ { B } }$ .

There are three typical VFL classification model:

(1) Vertical logistical regression model: In the vertical logistical regression model [40], [41], the passive party holds the local parameters $\theta _ { A }$ corresponding to the feature space of $[ x _ { i } ^ { A } ]$ , and the active party holds the local parameters $\theta _ { B }$ corresponding to the feature space of $[ x _ { i } ^ { B } ]$ . During the prediction stage, the passive party calculates the local result $\bar { \theta } _ { A } ^ { T } x ^ { A }$ and sends it to the active party. The active party receives the local result from the passive party and calculates the prediction result:

$$
y = \sigma (\theta_ {A} ^ {T} x ^ {A} + \theta_ {B} ^ {T} x ^ {B}) \tag {1}
$$

where $\sigma ( \mu ) = ( 1 + e ^ { \mu } ) ^ { - 1 }$

(2) Vertical neural network: Some work [11], [42], [43] propose vertical neural network by adopting a specific Twoparty Vertical SplitNN . The vertical neural network consists of the bottom model and the top model. Each party holds a bottom model, and the active party additionally holds a top model. In the prediction stage, the passive party calculates the output of his/her bottom model and sends it to the active party. The active party receives the output of the passive party’s bottom model and calculates the prediction result:

$$
y = g _ {B} (f _ {A} (x ^ {A}), f _ {B} (x ^ {B})), \tag {2}
$$

where $f _ { A } , \ f _ { B }$ denote the bottom models of the passive and active party,respectively, and $g _ { B }$ is the top model of the active party.

(3) Vertical tree-based model: In the vertical tree-based model, the active party has the tree structure, leaf node weights, and its dividing threshold, while the passive party only has the dividing threshold [44]. During the prediction stage, the active party looks for the corresponding features and thresholds of each tree node to divide, and if the threshold belongs to the passive party, the passive party performs dividing and sends the result to the active party.

Communication Cost for VFL Model Serving: When using all above models for online inference, for each arrived sample, the active party and passive party first need to perform a critical step PSI (Private Set Intersection) [45] to align the data sample ID. Then two parties need to transmit the intermediate results to complete the global model inference. For vertical logistic regressions, the intermediate result is $\theta _ { A } ^ { T } x ^ { A } ;$ ; for vertical neural network models, the intermediate result $f _ { A } ( x ^ { A } )$ is the output of the bottom model, which is the feature representation; for vertical tree models, the communication cost for the intermediate result is $n 2 ^ { h - 3 }$ , where n is the number of trees and h is the height of the tree. Since there could be millions of queries per hour in many online services, the communication caused by a large number of PSI operations and intermediate results transmissions incurs significant overhead and latency, which hinders the adoption of VFL in many resource-limited and delay-sensitive applications.

# III. PROBLEM DESCRIPTION AND MAIN IDEA

# A. Problem Description

VFL has shown a great potential in many cross-domain applications and has received increasing attention from a various organizations and companies. However, there is a severe challenge in applying it to an online services: as described in Sec.II-B, in the inference stage, making a prediction requires the active and passive parties to conduct ID alignment and communicate intermediate results, which causes significant communication cost and latency.

In this work, we aim to improve the quality of model prediction services for VFL by reducing the communication overhead and latency with negligible accuracy degradation. As described in Sec.II-B, we focus on a two-party VFL for classification tasks, which is the most common scenario in industry.

In the VFL system, the active party and the passive party cooperatively train the VFL model, i.e.:

$$
\arg \min _ {\theta_ {V F L}} \sum_ {i} \text { loss } (f (\theta_ {V F L}, [ x _ {i} ^ {A}, x _ {i} ^ {B} ]), y _ {i}), \tag {3}
$$

where loss $( f ( \theta _ { V F L } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] ) , y _ { i } )$ is the loss of data $[ x _ { i } ^ { A } , x _ { i } ^ { B } ]$ with label yi.

The active party holds the dataset $\{ x _ { i } ^ { B } , y _ { i } \} _ { i \in D _ { B } } .$ , and can also train an alone model $\theta _ { a l o n e }$ using his features:

$$
\arg \min _ {\theta_ {a l o n e}} \sum_ {i \in D _ {B}} \text { loss } (f (\theta_ {a l o n e}, x _ {i} ^ {B}), y _ {i}), \tag {4}
$$

where loss $( f ( \theta _ { a l o n e } , x _ { i } ^ { B } ) , y _ { i } )$ is the loss of data $x _ { i } ^ { B }$ with label yi in active party.

To understand the return of the communication cost, we investigate the performance of the alone model $\theta _ { a l o n e }$ and the VFL model $\theta _ { V F L }$ . Table I shows the results on seven datasets, where the details of dataset are presented in Sec.V-A1. From the results, we find that the VFL model $\theta _ { V F L }$ outperforms the alone model $\theta _ { a l o n e }$ . However, the alone model $\theta _ { a l o n e }$ can also make correct predictions on a large portion of test samples. For example, in the Census Income dataset $\mathcal { D } _ { C }$ ,

TABLE I ALONE MODEL V.S. VERTICAL FEDERATED MODEL. 

<table><tr><td>Dataset</td><td>TestAcc/Auc of  $\theta_{alone}$ </td><td>TestAcc/Auc of  $\theta_{VFL}$ </td><td> $\Delta Acc/Auc$ </td></tr><tr><td> $\mathcal{D}_{M}$ </td><td>89.0% ± 0.6%</td><td>98.4% ± 0.3%</td><td> $\Delta = +9.4\%$ </td></tr><tr><td> $\mathcal{D}_{FM}$ </td><td>81.7% ± 0.1%</td><td>88.6% ± 0.1%</td><td> $\Delta = +6.9\%$ </td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>77.7% ± 1.3%</td><td>85.6% ± 0.1%</td><td> $\Delta = +9.2\%$ </td></tr><tr><td> $\mathcal{D}_{L}$ </td><td>62.6% ± 0.9%</td><td>74.1% ± 0.5%</td><td> $\Delta = +11.5\%$ </td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>91.8% ± 0.1%</td><td>98.5% ± 0.2%</td><td> $\Delta = +6.7\%$ </td></tr><tr><td> $\mathcal{D}_{G}$ </td><td>67.8% ± 0.2%</td><td>83.2% ± 0.3%</td><td> $\Delta = +15.4\%$ </td></tr><tr><td> $\mathcal{D}_{Cr}$ </td><td>69.5% ± 0.9%</td><td>76.0% ± 1.2%</td><td> $\Delta = +6.5\%$ </td></tr></table>

TestAcc of the alone model $\theta _ { a l o n e }$ is 76.4%, which means that for 76.4% samples in the test dataset the active party has sufficient knowledge to make accurate predictions alone. Therefore, for samples that can be correctly predicted by the active party alone, the communication cost for their federated inference is a waste. We define the communication consumed by these samples as “dispensable communication”. Intuitively, if we can avoid “dispensable communication”, we can significantly reduce prediction communication overhead and latency without reducing prediction accuracy.

We denote the dataset with different output results from the alone model and the VFL model as $D ^ { d }$ , and the dataset with the same output results from the alone model and the VFL model as $D ^ { s }$ , where $D ^ { d } \cup D ^ { s } = D .$ , i.e.,

$$
\left\{ \begin{array}{l l} f (\theta_ {a l o n e}, x _ {i} ^ {B}) = f (\theta_ {V F L}, [ x _ {i} ^ {A}, x _ {i} ^ {B} ]) & i \in D ^ {s} \\ f (\theta_ {a l o n e}, x _ {i} ^ {B}) \neq f (\theta_ {V F L}, [ x _ {i} ^ {A}, x _ {i} ^ {B} ]) & i \in D ^ {d}. \end{array} \right. \tag {5}
$$

![](images/3b5b2c5fbf7de0226f5ceec812a3bf75f436641605f42b25ada86567fdb191e4.jpg)



Fig. 2. Example of $D ^ { d }$ and $D ^ { s }$ .

As shown in Fig. 2, if the active party can independently determine whether a given sample belongs to dataset $D ^ { d }$ or dataset $D ^ { s }$ , for samples belonging to $D ^ { s } .$ , the active party can make predictions using the alone model $\theta _ { a l o n e }$ independently; for samples belonging to $D ^ { d } .$ , active and passive parties can use the VFL model $\theta _ { V F L }$ for prediction. In this way, we can avoid ”dispensable communication”, save communication overhead, and reduce latency without compromising prediction performance.

# B. Main Idea

In the previous subsection, we have analyzed that if we can avoid “dispensable communication” in the prediction stage of VFL, the communication cost and latency can be reduced without sacrificing performance. Here, we mainly discuss the following three major questions:

Question #1: Can VFL system completely avoid “dispensable communication” ?

Before answering this question, we first analyze the feasibility of VFL, that is, the performance of the VFL model $\theta _ { V F L }$ is greater than or equal to that of the alone model $\theta _ { a l o n e } .$ .

Lemma 1. Suppose that the passive party holds the dataset $\{ x _ { i } ^ { A } \} _ { i \in D _ { A } }$ , the active party holds the dataset $\{ x _ { i } ^ { B } , y _ { i } \} _ { i \in D _ { B } } .$ $\hat { p _ { \theta _ { V F L } } } ( y | \bar { [ x ^ { A } , x ^ { B } ] } )$ is the VFL model parameterized by $\theta _ { V F L }$ and $p _ { \theta _ { a l o n e } } ( y | x ^ { B } )$ is the alone model parameterized by $\theta _ { a l o n e }$ of active party. And denote the optimal model parameters as $\theta ^ { * }$ . Then, the standard error:

$$
\mathbb {R} _ {\text { standard }} (\theta_ {V F L} ^ {*}) \leq \mathbb {R} _ {\text { standard }} (\theta_ {\text { alone }} ^ {*}), \tag {6}
$$

where $\mathbb { R } _ { s t a n d a r d } ( \theta ) \ = \ \mathbb { E } _ { p _ { d } ( x ) } [ K L ( p _ { d } ( y | x ) | | ( p _ { \theta } ( y | x ) ) ]$ , and $p _ { d } ( y | x )$ is the data distribution and $K L ( P | | Q )$ denotes the KL divergence between two distributions P and Q.

Proof Sketch. For simplicity, we focus on the model training process and ignore the encryption details of VFL for now.

In vertical linear model [1], the passive party holds the $\{ x _ { i } ^ { A } \} _ { i \in D _ { A } }$ and model $\theta _ { A }$ , and the active party holds the $\{ x _ { i } ^ { B } , y _ { i } \} _ { i \in D _ { E } }$ and $\theta _ { B }$ . The VFl model parameters $\theta _ { V F L } =$ $[ \theta _ { A } , \theta _ { B } ] ;$ , where $\theta _ { A }$ and $\theta _ { B }$ is corresponding to the feature space $x _ { i } ^ { A }$ and $x _ { i } ^ { B }$ .

In vertical linear regression, the VFl model output $f ( \theta _ { V F L } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] ) = \theta _ { A } x _ { i } ^ { A } + \theta _ { B } x _ { i } ^ { B }$ , and the output of alone model $f ( \theta _ { a l o n e } , x _ { i } ^ { B } ) = \theta _ { B } x _ { i } ^ { B }$ . And in vertical Logistic regression, the VFl model output $f ( \theta _ { V F L } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] ) \stackrel { \textstyle = } { = } \sigma ( \theta _ { A } \bar { x _ { i } ^ { A } } + $ $\theta _ { B } x _ { i } ^ { B } )$ , and the output of alone model $f ( \theta _ { a l o n e } , x _ { i } ^ { B } ) ~ =$ $\sigma ( \theta _ { B } x _ { i } ^ { B } )$ , where σ is the sigmod function.

For the optimal alone model $\theta _ { a l o n e } ^ { * } ,$ we can construct its corresponding VFL model $\hat { \theta } _ { V F L } = [ \mathbf { 0 } , \theta _ { a l o n e } ] .$ . And for any data sample, $f ( \hat { \theta } _ { V F L } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] ) = f ( \ ' { \theta } _ { a l o n e } ^ { * } , x _ { i } ^ { \bar { B } } )$ .

Therefore, in vertical linear model, we can get:

$$
\mathbb {R} _ {s t a n d a r d} (\theta_ {V F L} ^ {*}) \leq \mathbb {R} _ {s t a n d a r d} (\hat {\theta} _ {V F L}) = \mathbb {R} _ {s t a n d a r d} (\theta_ {a l o n e} ^ {*}).
$$

The proof process in the vertical neural networks model is similar to the above process. For the optimal individual model $\theta _ { a l o n e } ^ { * } ,$ we can construct its corresponding VFL model $\hat { \theta } _ { V F L }$ set the model parameters of that part of $x _ { i } ^ { A }$ to 0. Such that for any data sample, $f ( \hat { \theta } _ { V F L } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] ) \stackrel {  } { = } f ( \theta _ { a l o n e } ^ { * } , x _ { i } ^ { B } )$ .

Next, we analyze whether the VFL system can completely avoid “dispensable communication”. This problem can be transformed into whether the active party can distinguish independently whether a data sample belongs to $D ^ { s }$ or $D ^ { d }$ .

As Eq. (3) and Eq. (4), VFL model $\theta _ { V F L }$ and alone model $\theta _ { a l o n e }$ are optimized by gradient descent, and we denote the optimal models parameters as $\theta _ { V F L } ^ { * }$ and $\theta _ { a l o n e } ^ { * } .$ . And, for any $i \in D$ :

$$
\left\{ \begin{array}{l l} f (\theta_ {a l o n e} ^ {*}, x _ {i} ^ {B}) = f (\theta_ {V F L} ^ {*}, [ x _ {i} ^ {A}, x _ {i} ^ {B} ]) & i \in D ^ {s} \\ f (\theta_ {a l o n e} ^ {*}, x _ {i} ^ {B}) \neq f (\theta_ {V F L} ^ {*}, [ x _ {i} ^ {A}, x _ {i} ^ {B} ]) & i \in D ^ {d} \end{array} \right. \tag {7}
$$

where $D ^ { d } \cup D ^ { s } = D$ . If there exists ideal model θ in active party, such that for any $i \in D , f ( \theta , x _ { i } ^ { B } ) = f ( \theta _ { V F L } ^ { * } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] )$ , then denote it as ˜θ.

We prove the ability of the active party to independently identify data samples belonging to $D ^ { s }$ or $D ^ { d }$ equivalent to obtaining ideal model ${ \tilde { \theta } } .$

For binary classification, label $y ~ \in ~ [ 0 , 1 ]$ , if the active party has the ability to obtain ${ \tilde { \theta } } ,$ and due to $f ( \tilde { \theta } , x _ { i } ^ { B } ) ~ =$ $f ( \theta _ { V F L } ^ { * } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] )$ ), then:

$$
\left\{ \begin{array}{l l} i \in D ^ {s} & f (\tilde {\theta}, x _ {i} ^ {B}) = f (\theta_ {a l o n e} ^ {*}, x _ {i} ^ {B}) \\ i \in D ^ {d} & f (\tilde {\theta}, x _ {i} ^ {B}) \neq f (\theta_ {a l o n e} ^ {*}, x _ {i} ^ {B}). \end{array} \right. \tag {8}
$$

That means that the active party can independently identify data samples belonging to $D ^ { s }$ or $D ^ { d }$ .

If the active party can divide $D ^ { s }$ and $D ^ { d }$ in D independently, then can construct ˜θ through $\theta _ { a l o n e } ^ { * } ,$ i.e.:

$$
f (\tilde {\theta}, x _ {i} ^ {B}) = \left\{ \begin{array}{l l} f (\theta_ {a l o n e} ^ {*}, x _ {i} ^ {B}) & i \in D ^ {s} \\ [ 0, 1 ] \setminus f (\theta_ {a l o n e} ^ {*}, x _ {i} ^ {B}) & i \in D ^ {d}. \end{array} \right. \tag {9}
$$

That means that the active party has the ability to obtain the ideal model ${ \tilde { \theta } } .$

For multi-class classification, we turn it into multiple binary classification 1v.s.all, and then the analysis process is similar to the above.

Above, we have proved the ability of the active party to independently identify data samples belonging to $D ^ { s }$ or $D ^ { d }$ is equivalent to obtaining ideal model ˜θ. Then, we analyze whether the active party can obtain the ideal model ${ \tilde { \theta } } .$

As illustrated in Lemma 1, there are two cases in VFL. In the case of $\mathbb { R } _ { s t a n d a r d } ( \theta _ { V F L } ^ { * } ) = \mathbb { R } _ { s t a n d a r d } ( \theta _ { a l o n e } ^ { * } )$ , the active party participation in VFL cannot improve model performance and accuracy, i.e., for any data sample:

$$
f (\theta^ {*}, x _ {i} ^ {B}) = f (\tilde {\theta}, x _ {i} ^ {B}) = f (\theta_ {V F L} ^ {*}, [ x _ {i} ^ {A}, x _ {i} ^ {B} ]). \tag {10}
$$

Then we can get $D ^ { s } = D$ and $D ^ { d } = \mathcal { D }$ .

In the case of $\mathbb { R } _ { s t a n d a r d } ( \theta _ { V E L } ^ { * } ) < \mathbb { R } _ { s t a n d a r d } ( \theta _ { a l o n e } ^ { * } )$ , for the active party, there is no ˜θ such that for any $\textit { i } \in \textit { D }$ , $f ( { \tilde { \theta } } , x _ { i } ^ { B } ) { = } ^ { \top } f ( \bar { \theta _ { V F L } ^ { * } } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] )$ .

In summary, the active party cannot independently identify a data sample belonging to $D ^ { s }$ or $D ^ { d }$ , which means that the VFL system cannot completely avoid “dispensable communication”.

Question #2: How to reduce “dispensable communication” in the VFL system as much as possible without degrading prediction performance?

In Question #1, we have analyzed that the active party cannot completely avoid the “dispensable communication”. Based on observations in experiments, we propose a method to select the samples for which the active party cannot make a correctly prediction alone, which can help a VFL system avoid “dispensable communication” as much as possible without degrading prediction performance or by a small amount.

Here we use the vertical linear model as an example to illustrate our main idea. For VFL model $\theta _ { V F L }$ , the prediction output $\hat { y } ~ = ~ \sigma ( W _ { A } x _ { i } ^ { A } + W _ { B } x _ { i } ^ { B } )$ , where σ is the Sigmod function. If $W _ { B } x _ { i } ^ { B } > \beta ,$ where $\beta$ is a huge value, the active party judges that the local result $W _ { A } x _ { i } ^ { A }$ of the passive party with a high probability will not have a great impact on the output of the model, which means that this sample has a high probability of belonging to $D ^ { s }$ and the active party can independently make prediction.

![](images/10d2cb98729456a640bfba0c941cc9b37ee8474897e3bfd0147b80e0f627966b.jpg)



(a) Marginal Hyperplanes.

![](images/9d9d768a32b05d5572b80fad6e9937becfe9130b32efd7c1337e7d45a8a8eec6.jpg)



(b) The red dots belong to $D ^ { d }$ and the green dots belongs to $D ^ { s }$ .   
Fig. 3. Example of our main Idea.

As shown in Fig. 3 (a), assume that the marginal hyperplane trained by his features is $M _ { a l o n e }$ and the marginal hyperplane of VFL model is $M _ { V F L }$ . The marginal hyperplanes $M _ { a l o n e }$ is $x \ = \ 5 .$ , for any sample, if $x ^ { B } \geq 5 ,$ , the inference result $\hat { y } = 1 ;$ else, the inference result $\hat { y } = 0$ . For the hyperplane of VFL model $M _ { V F L }$ , our goal is to find the dataset $D ^ { d }$ that alone model $\theta _ { a l o n e }$ and VFL model $\theta _ { V F L }$ output differently, which is the shaded part in Fig. 3 (a). For the active party, if $x ^ { B } > 1 0 0$ , then he can think that this sample has a high probability of belonging to $D ^ { s }$ , and alone model $\theta _ { a l o n e }$ has a high likelihood of giving correct results, which does not need to participate in VFL for inference.

Fig. 3 (b) shows experimental results in Iris dataset [46], where the red dot belongs to dataset $D ^ { d }$ and the green dot belongs to dataset $D ^ { s } .$ , the x-axis is the index of the data sample, and the y-axis is the output of the local results $W _ { B } x _ { i } ^ { B }$ . If we set threshold = 1.1, for any data sample, if $W _ { B } x _ { i } ^ { B } \ < \ t h r e s h o l d ,$ the active party and passive party cooperatively make prediction; and if $W _ { B } x _ { i } ^ { B } \geq t h r e s h o l d ,$ the active party independently predicts the sample. In this way, we can significantly reduce the communication overhead and prediction latency without reducing the prediction accuracy.

Due to the simplicity of linear models, we can use this method to select a threshold to filter, while for the NN and treebased models, we introduce a new model, the discriminator $\theta _ { D }$ , to help us divide $D ^ { s }$ and $D ^ { d }$ . Here the discriminator $\theta _ { D }$ is not used to judge whether a data sample belongs to $D ^ { s }$ or $D ^ { d }$ , but is used to map the data sample to onedimensional. Suppose the dataset is IID (independent and identically distributed), similar to Fig. 3 (b), we can set a threshold based on the results of the discriminator $\theta _ { D }$ on the training dataset.

Question #3: What determines the extent to which communication overheads can be reduced?

Unlike previous model inference acceleration technologies, we study and solve this problem from the data and feature perspective. We consider that not all data samples need VFL model for prediction. The core of our method is to judge whether the active party has sufficient knowledge to make accurate prediction for the data sample. To further explore the effect of feature distribution on our method, we use a well-known explainable machine technology SHAP [24] to calculate the importance of each feature, which is a gametheoretic approach to measure the influence of features on the output. By randomly assigning features to the active party and passive party, and measuring their feature importance, we find that the degree of communication savings using TVFL is positively correlated with the feature importance of the active party. The experimental results are in Sec.V-E.

![](images/3ea506c9ab52e6c6906766f8d55380386965ceae576b26603106a8aaaf3cb5ea.jpg)



(a) Training Stage.

![](images/9a94a346c1435a56ed0414fe5f0ed0b0b367fe56c1441c8bf8d345590dc36b42.jpg)



(b) Prediction Stage.   
Fig. 4. System Overview of TVFL.

# C. System Overview

Leveraging our main idea, we design the framework TVFL for reducing the communication overhead and latency to improve the quality of prediction serving in VFL. Taking vertical neural network as an example, Fig. 4 shows the overview of TVFL, consisting of three main steps:

(1) Training stage. As shown in Fig. 4 (a), compared to the typical VFL system, in TVFL, the active party needs to train two more models: the alone model $\theta _ { a l o n e }$ and discriminator $\theta _ { D }$ . Using his local features and label, the active party first trains $\theta _ { a l o n e } .$ . Then the active party constructs the labels $y _ { D } =$ ${ \cal I } ( f ( \theta _ { V F L } , [ x _ { i } ^ { A } , x _ { i } ^ { B } ] ) = = f ( \theta _ { a l o n e } , x _ { i } ^ { B } ) )$ ) of discriminator $\theta _ { D } ,$ where I is the indicator function. The details are in Sec. IV-A.

(2) Threshold selection. The setting of the threshold is a trade-off of performance and communication. We propose two selection methods: Basic selection method and Maximum gain selection method. In the Basic selection method, we traverse the output of the training dataset on discriminator $\theta _ { D }$ and select the largest as the threshold. Suppose the dataset is IID ( independent and identically distributed), we analyze the error bound of this method. However, if there is an outlier in the training data, which may cause the threshold to be substantial, it would lower the degree of communication cost savings. Therefore, we propose the Maximum gain selection method. In Eq.(12), we define the gain on the active party, which is the trade-off of the improvement in prediction performance and the number of communications, then choose the threshold that maximizes the gain on the training dataset. The details are in Sec. IV-B.

(3) Prediction stage. As shown in Fig. 4 (b), for any input of the samples to be predicted, the active party first uses the discriminator $\theta _ { D }$ and threshold to smartly switch between independent inference and federated inference based on the features of the input sample. If VFL model prediction is required, the active party and the passive party jointly

make prediction; if not, the active party makes prediction independently using alone model $\theta _ { a l o n e }$ . The details are in Sec. IV-C.

Also, TVFL is model-agnostic and does not involve the process of model training, which can be applied to various VFL frameworks with different architectures [1], [44], [47].

# IV. ALGORITHM

# A. Training stage of TVFL

Assume that the passive party holds the features $\{ x _ { i } ^ { A } \} _ { i = 1 } ^ { N }$ the active party holds the features $\{ x _ { i } ^ { B } \} _ { i = } ^ { N }$ 1 and label $\{ y _ { i } \} _ { i = 1 } ^ { N } .$ In a typical VFL system, passive party and active party collaboratively train a VFL model $\theta _ { V F L }$ based on the training dataset $\{ [ x _ { i } ^ { A } , \bar { x } _ { i } ^ { B } ] , y _ { i } \} _ { i = 1 } ^ { N }$ . And the active party can train a ialone model $\theta _ { a l o n e }$ i=1based on his own data $\{ x _ { i } ^ { B } , y _ { i } \} _ { i = 1 } ^ { N }$ .

Our method does not involve the process of VFL model training and can be applied to any VFL model, so we will not repeat the specific details of VFL model training here. Algorithm 1 presents the training method of TVFL.

Algorithm 1: Training method.   
1 Input: Initializes the alone model $\theta_{alone}$ , discriminator $\theta_D$ and VFL model $\theta_{VFL}$ .
2 The active party and passive party train the VFL model $\theta_{VFL}$ .
3 The active party trains the alone model $\theta_{alone}$ using his features and label.
4 Divide the training dataset $D_{train}$ into two parts: $D_{train}^1$ and $D_{train}^2$ .
5 Construct the labels of the discriminator on the dataset $D_{train}^1$ : $y_D = I(f(\theta_{AB}, [x^A, x^B]) == f(\theta_{alone}, x^B))$ .
6 for each epoch $t \leftarrow 1,..,\tau$ do
7    for each batch do
8 $loss_D = 0$ 9    for $i \in Batch$ do
10 $\lfloor loss_D + = loss(f(\theta_D, x_i^B], y_D)$ ;
11    The active party updates discriminator: $\theta_D \leftarrow \theta_D - \alpha \nabla_{\theta_D} loss_D$ .

As shown in Algorithm 1, compared to the typical VFL system, the active party needs to train two more models: the alone model the training $\theta _ { a l o n e }$ and into: minat and $\theta _ { D }$ Random, where deis traused to train the discriminator $D _ { t r a i n } ^ { 1 }$ $\theta _ { D }$ and $D _ { t r a i n } ^ { 2 }$ $D _ { t r a i n } ^ { 2 }$ train  is used to select $D _ { t r a i n } ^ { 1 }$ threshold in Sec. IV-B, which is to ensure that the trained discriminator $\theta _ { D }$ and $D _ { t r a i n } ^ { 2 }$ are independent of each other. Then the active party train the the alone model $\theta _ { a l o n e }$ using his own features and label and constructs the label of the discriminator $y _ { D } = I ( f ( T _ { A B } , [ x ^ { A } , x ^ { B } ] ) = = f ( T _ { a l o n e } , x ^ { B } ) )$ , where I is the indicator function. Finally, the active party independently trains the discriminator $\theta _ { D }$ model.

# B. Threshold Selection

In the Sec. IV-A, we show the training method of the discriminator $\theta _ { D }$ . The training dataset of discriminator $\theta _ { D }$ is an imbalanced binary dataset. For example, as shown in Table I, about 9% of the samples on average, the output of $\theta _ { a l o n e }$ and model $\theta _ { V F L }$ are different, which means that the ratio of positive and negative samples in the training dataset of the discriminator $\theta _ { D }$ is $1 : 1 0$ . And based on the conclusion in Sec. III-B, it is not accurate to directly use the result of the discriminator $\theta _ { D }$ to judge whether a sample to be predicted input into $\theta _ { a l o n e }$ or $\theta _ { V F L }$ . Hence, we set a threshold and judge whether a sample to be predicted input into $\theta _ { a l o n e }$ or $\theta _ { V F L }$ by the threshold during the prediction stage.

We split the training dataset into two parts: $D _ { t r a i n } ^ { 1 }$ and $D _ { t r a i n } ^ { 2 } .$ where D1train i $D _ { t r a i n } ^ { 1 }$ s used to train the discriminator $\theta _ { D }$ and D2train $D _ { t r a i n } ^ { 2 }$ is used to select threshold. The reason is to ensure that the discriminator The active party can obtain the $\theta _ { D }$ model and $D _ { t r a i n } ^ { s }$ $D _ { t r a i n } ^ { 2 }$ train and $D _ { t r a i n } ^ { d }$ are independent. during the training stage by the Eq.(5). We can set the threshold based on the result of the training dataset $D _ { t r a i n } ^ { 2 }$ on the discriminator $D _ { t r a i n } ^ { d } \cap D _ { t r a i n } ^ { 2 }$ to judge in the prediction stage. We propose two methods for selecting the threshold:

Basic selection method: Traverse the $D _ { t r a i n } ^ { d } \cap D _ { t r a i n } ^ { 2 }$ and select the largest output of discriminator $\theta _ { D }$ as the threshold.

$$
\text { threshold } = \max \{f (\theta_ {D}, x _ {i} ^ {B}) \} _ {i \in (D _ {\text { train }} ^ {d} \cap D _ {\text { train }} ^ {2}).} \tag {11}
$$

Suppose the dataset is IID (independent and identically distributed), the probability that a sample belonging to $D ^ { \dot { d } }$ is incorrectly classified as $D ^ { s }$ is $2 ^ { - | D _ { t r a i n } ^ { 2 } | }$ using this threshold, which means that the average of reduced accuracy is $m 2 ^ { - | D _ { t r a i n } ^ { 2 } | }$ , where m is the number of prediction data samples. However, if there is an outlier in the training data, which may cause the threshold to be substantial, it would reduce the degree of communication cost savings. Therefore, we propose the Maximum gain selection method.

Maximum gain selection method: In the typical VFL system, for each sample, the active party needs to make prediction with the passive party during the prediction stage cooperatively, which means that the active party uses 100% of the communication to improve the prediction performance. We denote the communication as T and performance gain as P . Here we use the improved prediction accuracy compared with model $\theta _ { a l o n e }$ as $P ,$ and use the percentage of required communication samples as T . We can define the gain of the active party as:

$$
G = \rho_ {1} P - \rho_ {2} T, \tag {12}
$$

where $\rho _ { 1 }$ and $\rho _ { 2 }$ is the coefficient of $P$ and T .

As gorit 2, we can traverse $D _ { t r a i n } ^ { d } \cap D _ { t r a i n } ^ { 2 }$ n ∩ D2tr to find the threshold that maximizes the gain of the active party. The coefficients $\rho _ { 1 }$ and $\rho _ { 1 }$ are determined according to the specific needs of different scenarios. Here we give a general setting: $\begin{array} { r } { \rho _ { 1 } ~ = ~ \frac { | ( D _ { t r a i n } ^ { 2 } ) | } { | D _ { t r a i n } ^ { d } \cap D _ { t r a i n } ^ { 2 } | } } \end{array}$ and $\rho _ { 2 } = 1$ . In this setting, when the train trainthreshold is minimum, all data samples are input to $\theta _ { a l o n e } ,$ which means that the active party makes prediction independently without performance improvement and communication overhead, and $G = 0$ . When the threshold is maximum, all data samples are input to $\theta _ { V F L }$ , which is the traditional VFL, and $\begin{array} { r } { G = \frac { | D _ { t r a i n } ^ { 2 } | } { | D _ { t r a i n } ^ { d } \cap D _ { t r a i n } ^ { 2 } | } | D _ { t r a i n } ^ { d } \cap D _ { t r a i n } ^ { 2 } | - | D _ { t r a i n } ^ { 2 } | = 0 . } \end{array}$ .

Algorithm 2: Maximum gain selection method.   
1 Input: $D_{train}^{d}$ , $D_{train}^{2}$ and the discriminator $\theta_{D}$ . The coefficient $\rho_{1}$ and $\rho_{2}$ .
2 Outputs = {f( $\theta_{D}, x_{i}^{B}$ ), i} $_{i\in(D_{train}^{d}\cap D_{train}^{2})}$ ;
3 $G_{best} = 0$ .
4 for $i \in (D_{train}^{d} \cap D_{train}^{2})$ do
5 temp = Outputs $_{i,0}$ ;
6 for $j \in (D_{train}^{d} \cap D_{train}^{2})$ do
7 output = Outputs $_{j,0}$ ;
8 index = outputs $_{j,1}$ ;
9 if output ≤ temp then
10 t = t + 1;
11 if index ∈ $D_{train}^{d}$ then
12 p = p + 1;
13 T = $\frac{t}{|D_{train}^{2}|}$ , and P = $\frac{p}{|D_{train}^{2}|}$ ;
14 G = $\rho_{1}P - \rho_{2}T$ ;
15 if G > G $_{best}$ then
16 threshold = temp;
17 G $_{best}$ = G;   
18 Output: the selected threshold.

These methods are suitable for scenarios where accuracy is used to quantify model performance. Similar algorithms can be designed for other scenarios using methods such as auc/recall to quantify model performance.

# C. Prediction stage of TVFL

Fig. 4 (b) gives an overview of the prediction stage for TVFL.

Algorithm 3: Tunable prediction serving.   
1 Input: The alone model $\theta_{alone}$ , discriminator $\theta_D$ , VFL model $\theta_{VFL}$ , and threshold.  
2 if $f(\theta_D, x^B) > threshold$ then  
3 $\lfloor p = f(\theta_{alone}, x^B)$ 4 else  
5 $\lfloor p = f(\theta_{VFL}, [x^A, x^B])$ 6 Output: the prediction result $p$ .

As shown in Algorithm 3, for any sample input to be predicted, the active party first uses the discriminator $\theta _ { D }$ to determine whether the input sample needs VFL model $\theta _ { V F L }$ prediction. If VFL model prediction is required, the active party and the passive party jointly make a prediction, if not, the active party predicts using alone model $\theta _ { a l o n e }$ independently.

# V. EVALUATIONS

# A. Experimental Configuration

1) Datasets: We use both public and real-world datasets to evaluate our methods. For MNIST and Fashion-MNIST datasets, we evenly split each image into two halves and assign them to the active party and passive party, respectively. Moreover, for the other four real-world tabular datasets, we assign 50% of the features to the active party and passive party, respectively, and extract 20% - 30% as the test dataset. Furthermore, we also use a well-known CTR benchmark dataset from Criteo [48]. We randomly sample 600, 000 data samples from it and manually partition its features to simulate a VFL data set to test our framework TVFL on a real-world advertising recommendation system. The datasets details are summarized in Table II.

TABLE II DATASETS. 

<table><tr><td>Dataset</td><td>Size</td><td>Description</td></tr><tr><td> $\mathcal{D}_{M}$ </td><td>70,000</td><td>MNIST dataset [49]</td></tr><tr><td> $\mathcal{D}_{FM}$ </td><td>70,000</td><td>Fashion MNIST dataset [50]</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>48,842*81</td><td>Census income dataset [46]</td></tr><tr><td> $\mathcal{D}_{L}$ </td><td>50,000*23</td><td>Large Movie Review Dataset [51]</td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>58,509*49</td><td>Sensorless drive diagnosis dataset [46]</td></tr><tr><td> $\mathcal{D}_{G}$ </td><td>150,000*10</td><td>Give me some credit dataset [52]</td></tr><tr><td> $\mathcal{D}_{Cr}$ </td><td>600,000*39</td><td>Criteo dataset [48]</td></tr></table>

2) Vertical federated learning models: We have implemented three typical models, namely a vertical logistical regression model VFL-LogReg [1], a vertical neural network VFL-NN, and a vertical tree model SecureBoost [44].   
3) Metrics: We evaluate our framework from three aspects: model performance, communication overhead, and inference latency. For the two-class imbalanced dataset $( D _ { G } )$ and CTR dataset $D _ { C r } )$ , we quantify the model performance with the area under the curve of the test dataset (TestAuc). For other datasets, we quantify the model performance with the accuracy of the test dataset (TestAcc). The communication overhead is quantified by the amount of data (MB) that the active party interacts with the passive party during the prediction stage. The inference latency is the average consumed time from when a predicted sample is generated to when the predicted result is given.   
4) Baselines: We compare our work with two typical baselines: $\theta _ { V F L }$ and $\theta _ { a l o n e }$ . As Eq.(3), $\theta _ { V F L }$ is the VFL model, which is trained by the active party and passive party collaboratively. And as $\mathrm { E q . } ( 4 ) , \theta _ { a l o n e }$ is a centralized machine learning model, which is trained by the active party with his features and labels independently. As described in Sec. IV-B, we propose two threshold selection method, TVFL (basic) means TVFL system using basic selection method and TVFL (MaxGain) means TVFL system using Maximum gain selection method.   
5) Benchmark: Li et al. [11] propose Split Knowledge Distillation (SplitKD) schema to avoid cross-silo serving on vertical neural network in advertising systems. SplitKD utilizes the knowledge distillation method to distill the knowledge of the VFL model to the local model and then uses the local

model to make predictions in the prediction stage. Using seven datasets, we compare our framework with the benchmark method SplitKD [11] on VFL-NN.

# B. Evaluation on vertical logistical regression

We have implemented the vertical logistical regression model VFL-LogReg [1], and test our method in five realworld tabular datasets $\mathcal { D } _ { C } , \mathcal { D } _ { L } , \mathcal { D } _ { S } , \mathcal { D } _ { G }$ and $\mathcal { D } _ { C r }$ .

![](images/2e6ff5b89dbdca18c9db59da18d4387a1209a182e183cff4778fb68b1cc781f1.jpg)



(a) Communication Cost.

![](images/a937ac7797b18c1edd068fc5c5e695c12e34fdb5426a0570cc83eb3521102a2b.jpg)



(b) Latency.   
Fig. 5. Efficiency comparison on vertical logistical regression.

Fig. 5 shows the efficiency comparison between TVFL and typical VFL. Fig. 5 (a) and (b) depict the TVFL significantly saves communication overhead and reduce prediction latency during the prediction stage. And as shown in Table III, the prediction performance of TVFL (basic) and TVFL (MaxGain) is very close to the typical VFL $\theta _ { V F L }$ , much larger than the local alone model $\theta _ { a l o n e } .$ . For example, on dataset $D _ { S }$ , the TestACC of VFL is $9 1 . 7 \% \pm 0 . 3 \%$ , but the communication overhead and prediction latency are 34.7 MB and 200.2 ms, while the TestACC of TVFL (MaxGain) is 88.8% ± 0.1%, the communication overhead and prediction Latency are 14.7 MB and 86.4 ms. That is, TVFL (MaxGain) saves the communication cost of 57.6% and reduces the prediction latency of 57.1% while only reducing the accuracy by 2.9%.

TABLE III PREDICTION PERFORMANCE ON VERTICAL LOGISTICAL REGRESSION. 

<table><tr><td>Dataset</td><td> $\theta_{alone}$ </td><td> $\theta_{VFL}$ </td><td>TVFL (Basic)</td><td>TVFL (MaxGain)</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>76.4% ± 0.1%</td><td>85.2% ± 0.1%</td><td>85.0% ± 0.2%</td><td>84.6% ± 0.1%</td></tr><tr><td> $\mathcal{D}_{L}$ </td><td>63.8% ± 0.7%</td><td>73.5% ± 0.2%</td><td>73.5% ± 0.2%</td><td>71.6% ± 0.7%</td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>68.4% ± 0.4%</td><td>91.7% ± 0.3%</td><td>91.7% ± 0.3%</td><td>88.8% ± 0.1%</td></tr><tr><td> $\mathcal{D}_{G}$ </td><td>64.7% ± 0.2%</td><td>78.1% ± 0.5%</td><td>78.1% ± 0.1%</td><td>72.8% ± 1.0%</td></tr><tr><td> $\mathcal{D}_{Cr}$ </td><td>60.4% ± 0.7%</td><td>70.1% ± 0.8%</td><td>70.1% ± 0.7%</td><td>69.2% ± 0.6%</td></tr></table>

# C. Evaluation on vertical neural network

We have implemented the vertical neural network model VFL-NN, and evaluate our method in seven datasets.

Fig. 6 (a) and (b) show that TVFL can significantly save communication overhead and reduce prediction latency on VFL-NN. And as shown in Table IV, the prediction performance of TVFL (basic) and TVFL (MaxGain) is very close to the typical VFL $\theta _ { V F L }$ , much larger than the local alone model $\theta _ { a l o n e }$ . For example, on dataset $D _ { F M }$ , TVFL (MaxGain) saves the communication cost from 48.8 MB from 16.4 MB and reduces prediction latency from 201.6 ms to 57.6 ms, while only reducing the accuracy from 88.6% ± 0.1% to 86.8% ± 0.2%.

# D. Evaluation on vertical tree-based model

Similar to VFL-LogReg and VFL-NN, on the vertical treebased model, TVFL can significantly reduce the prediction communication overhead and latency with the tiny reduction in prediction accuracy. As experimental results presented in Fig. 7 and Table V, TVFL reduces the prediction accuracy by only 2.2% on average, while reducing the communication overhead and prediction latency by 47.3%.

![](images/bc8ac6e66caecfdebeda24c997f3cb7db6c7a777d734a46494c94a7e6fd1e9ac.jpg)



(a) Communication Cost.

![](images/c98e6e414fa475cd03a62e0810e4fd12fe4b0c294cfbbc4be5218bc7e022bf32.jpg)



(b) Latency.

![](images/6a16d5c5259e8396db62161aec15775ae6aae9cc82c1b3f1c1bb141c66aa59b3.jpg)



(a) Communication Cost.

![](images/be7d65ca814902a9410ed3091785df8903b79466f4974337cbb48fdf697db2c0.jpg)



(b) Latency.

Fig. 6. Efficiency comparison on vertical neural network.   
![](images/7503c88a2660541134983cb2c41d69ab50d8d61a3f0f0584e42309aa71f7030a.jpg)



$D _ { M }$

![](images/f0d2e0321250d60bb77d7f797e8e19e456212e567d1203f38407c715302a1c19.jpg)



(b) DC

Fig. 7. Efficiency comparison on vertical tree-based model.   
![](images/1bc6efacfea0e697a56a816c2be304bfd184170c0d8e1142af6ebe1745d23efc.jpg)



(c) DS

![](images/25c17f29e4f88f83d1bf63358653ebe159441150dbbd3a7328ddd00fb9120036.jpg)



(d) $D _ { L }$

TABLE IV   
PREDICTION PERFORMANCE ON VERTICAL NEURAL NETWORK. 

<table><tr><td>Dataset</td><td> $\theta_{alone}$ </td><td> $\theta_{VFL}$ </td><td>TVFL (Basic)</td><td>TVFL (MaxGain)</td></tr><tr><td> $\mathcal{D}_{M}$ </td><td>89.0% ± 0.6%</td><td>98.4% ± 0.3%</td><td>98.4% ± 0.5%</td><td>95.6% ± 0.4%</td></tr><tr><td> $\mathcal{D}_{FM}$ </td><td>81.7% ± 0.1%</td><td>88.6% ± 0.1%</td><td>88.6% ± 0.1%</td><td>86.8% ± 0.2%</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>77.7% ± 1.3%</td><td>85.6% ± 0.1%</td><td>85.6% ± 0.2%</td><td>85.0% ± 0.1%</td></tr><tr><td> $\mathcal{D}_{L}$ </td><td>62.6% ± 0.9%</td><td>74.1% ± 0.5%</td><td>74.1% ± 0.5%</td><td>72.6% ± 0.1%</td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>91.8% ± 0.1%</td><td>98.5% ± 0.2%</td><td>98.5% ± 0.2%</td><td>96.9% ± 0.2%</td></tr><tr><td> $\mathcal{D}_{G}$ </td><td>67.8% ± 0.2%</td><td>83.2% ± 0.3%</td><td>83.1% ± 0.2%</td><td>77.9% ± 0.4%</td></tr><tr><td> $\mathcal{D}_{Cr}$ </td><td>69.5% ± 0.9%</td><td>76.0% ± 1.2%</td><td>76.0% ± 1.2%</td><td>74.7% ± 1.3%</td></tr></table>

TABLE V PREDICTION PERFORMANCE ON VERTICAL TREE-BASED MODEL. 

<table><tr><td>Dataset</td><td> $\theta_{alone}$ </td><td> $\theta_{VFL}$ </td><td>TVFL (Basic)</td><td>TVFL (MaxGain)</td></tr><tr><td> $\mathcal{D}_C$ </td><td>76.3%</td><td>85.3%</td><td>85.2% ± 0.1%</td><td>84.0% ± 0.1%</td></tr><tr><td> $\mathcal{D}_L$ </td><td>64.8%</td><td>73.6%</td><td>73.5% ± 0.1%</td><td>70.2% ± 0.2%</td></tr><tr><td> $\mathcal{D}_S$ </td><td>90.0%</td><td>96.9%</td><td>96.9% ± 0.2%</td><td>95.7% ± 0.1%</td></tr><tr><td> $\mathcal{D}_G$ </td><td>71.3%</td><td>85.7%</td><td>85.7% ± 0.1%</td><td>82.6% ± 0.2%</td></tr><tr><td> $\mathcal{D}_{Cr}$ </td><td>66.8%</td><td>74.7%</td><td>74.6% ± 0.1%</td><td>73.3% ± 0.6%</td></tr></table>

# E. Effect of feature distribution

To further explore the effect of feature distribution on our method, we use SHAP [24] to calculate the importance of each feature of the active party.

We randomly assign 5%, 10%, 15%, ..., 95% of features to the active party, and calculate their importance by SHAP, then calculate the degree of saved communication by TVFL. We set the random seed = 0, 1, 2 and repeat the above experiment three times. Due to space limitations, here we only present the results of two datasets $D _ { M } , D _ { C } , D _ { S }$ and $D _ { L }$ , and the other two datasets have similar results. As shown in Fig. 8, the experiment result shows an apparent positive correlation between the feature importance of the active party and the communication saved.

# F. Comparison with Benchmark Method

Using seven datasets, we compare our framework with the benchmark method SplitKD [11] on VFL-NN. As shown in

re importance. TABLE VI COMPARISON WITH BENCHMARK METHOD ON VERTICAL NEURAL NETWORK. 

<table><tr><td>Dataset</td><td> $\theta_{alone}$ </td><td>TVFL (Basic)</td><td>TVFL (MaxGain)</td><td>SplitKD</td></tr><tr><td> $\mathcal{D}_{M}$ </td><td>89.0% ± 0.6%</td><td>98.4% ± 0.5%</td><td>95.6% ± 0.4%</td><td>90.0% ± 0.7%</td></tr><tr><td> $\mathcal{D}_{FM}$ </td><td>81.7% ± 0.1%</td><td>88.6% ± 0.1%</td><td>86.8% ± 0.2%</td><td>82.3% ± 0.3%</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>77.7% ± 1.3%</td><td>85.6% ± 0.2%</td><td>85.0% ± 0.1%</td><td>78.1% ± 0.6%</td></tr><tr><td> $\mathcal{D}_{L}$ </td><td>62.6% ± 0.9%</td><td>74.1% ± 0.5%</td><td>72.6% ± 0.1%</td><td>63.2% ± 0.5%</td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>91.8% ± 0.1%</td><td>98.5% ± 0.2%</td><td>96.9% ± 0.2%</td><td>92.0% ± 0.2%</td></tr><tr><td> $\mathcal{D}_{G}$ </td><td>67.8% ± 0.2%</td><td>83.1% ± 0.2%</td><td>77.9% ± 0.4%</td><td>67.9% ± 0.3%</td></tr><tr><td> $\mathcal{D}_{Cr}$ </td><td>69.5% ± 0.9%</td><td>76.0% ± 1.2%</td><td>74.7% ± 1.3%</td><td>70.1% ± 0.8%</td></tr></table>

Table VI, the prediction performance of our method is much more excellent than the splitKD. Compared to our method, the local distilled model suffers from an obvious (about 8.5%) accuracy degradation.

# VI. CONCLUSION

In this paper, we focus on reducing the communication cost and latency incurred by transmitting intermediate results in VFL model predictions. We find that a large portion of test samples can be predicted correctly by the active party alone, thus the corresponding communication for VFL inference is dispensable. Based on this insight, we theoretically analyze the “dispensable communication” and propose TVFL to smartly switch between local independent inference and vertical federated inference based on the features of the input sample, which can reduce communication overhead and inference latency significantly with negligible accuracy degradation. Furthermore, we explore the influence of feature importance distribution on the tunability of TVFL, and find that the degree of communication savings using TVFL is positively correlated with the feature importance of the active party.

# VII. ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, and ”the Fundamental Research Funds for the Central Universities” WK2150110024. This work was partially supported by Tencent Marketing Solution Rhino-Bird Focused Research Program.

# REFERENCES

[1] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” TIST, 2019.   
[2] H. B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in AISTATS, 2017.   
[3] A. Li, L. Zhang, J. Tan, Y. Qin, J. Wang, and X.-Y. Li, “Sample-level data selection for federated learning,” in IEEE INFOCOM 2021-IEEE Conference on Computer Communications. IEEE, 2021, pp. 1–10.   
[4] Z. Shi, L. Zhang, Z. Yao, L. Lyu, C. Chen, L. Wang, J. Wang, and X.-Y. Li, “Fedfaim: A model performance-based fair incentive mechanism for federated learning,” IEEE Transactions on Big Data, 2022.   
[5] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. M. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 372–383.   
[6] J. Wang, L. Zhang, A. Li, X. You, and H. Cheng, “Efficient participant contribution evaluation for horizontal and vertical federated learning,” in 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 2022, pp. 911–923.   
[7] A. Li, L. Zhang, J. Wang, F. Han, and X.-Y. Li, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, vol. 33, no. 10, pp. 2291–2303, 2021.   
[8] Y. Hu, D. Niu, J. Yang, and S. Zhou, “Fdml: A collaborative machine learning framework for distributed features,” in SIGKDD, 2019.   
[9] Q. Zhang, C. Wang, H. Wu, C. Xin, and T. V. X. Phuong, “Gelu-net: A globally encrypted, locally unencrypted deep neural network for privacypreserved learning,” in IJCAI, 2018.   
[10] Y. Zhang and H. Zhu, “Additively homomorphical encryption based deep neural network for asymmetrically collaborative machine learning,” ArXiv, vol. abs/2007.06849, 2020.   
[11] W. Li, Q. Xia, J. Deng, H. Cheng, J. Liu, K. Xue, Y. Cheng, and S. Xia, “Semi-supervised cross-silo advertising with partial knowledge transfer,” ArXiv, vol. abs/2205.15987, 2022.   
[12] J. Shen, B. Orten, S. C. Geyik, D. Liu, S. Shariat, F. Bian, and A. Dasdan, “From 0.5 million to 2.5 million: Efficiently scaling up realtime bidding,” IEEE International Conference on Data Mining, 2015.   
[13] S. Yuan, J. Wang, and X. Zhao, “Real-time bidding for online advertising: measurement and analysis,” ArXiv, vol. abs/1306.6542, 2013.   
[14] T. Nishio and R. Yonetani, “Client selection for federated learning with heterogeneous resources in mobile edge,” ICC 2019 - 2019 IEEE International Conference on Communications (ICC), pp. 1–7, 2019.   
[15] J. Xu and H. Wang, “Client selection and bandwidth allocation in wireless federated learning networks: A long-term perspective,” IEEE Transactions on Wireless Communications, 2021.   
[16] Y. J. Cho, J. Wang, and G. Joshi, “Client selection in federated learning: Convergence analysis and power-of-choice selection strategies,” ArXiv, vol. abs/2010.01243, 2020.   
[17] T. T. Anh, N. C. Luong, D. T. Niyato, D. I. Kim, and L.-C. Wang, “Efficient training management for mobile crowd-machine learning: A deep reinforcement learning approach,” IEEE Wireless Communications Letters, vol. 8, pp. 1345–1348, 2019.   
[18] A. Reisizadeh, A. Mokhtari, H. Hassani, A. Jadbabaie, and R. Pedarsani, “Fedpaq: A communication-efficient federated learning method with periodic averaging and quantization,” ArXiv, vol. abs/1909.13014, 2020.   
[19] M. M. Amiri, D. Gund ¨ uz, S. R. Kulkarni, and H. V. Poor, “Federated ¨ learning with quantized global model updates,” ArXiv, 2020.   
[20] N. Shlezinger, M. Chen, Y. C. Eldar, H. V. Poor, and S. Cui, “Federated learning with quantization constraints,” IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020.   
[21] D. Rothchild, A. Panda, E. Ullah, N. Ivkin, I. Stoica, V. Braverman, J. E. Gonzalez, and R. Arora, “Fetchsgd: Communication-efficient federated learning with sketching,” in ICML, 2020.   
[22] S. Li, Q. Qi, J. Wang, H. Sun, Y. Li, and F. R. Yu, “Ggs: General gradient sparsification for federated learning in edge computing\*,” IEEE International Conference on Communications (ICC), 2020.   
[23] T. Castiglia, A. Das, S. Wang, and S. Patterson, “Compressed-vfl: Communication-efficient learning with vertically partitioned data,” in ICML, 2022.   
[24] S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” ArXiv, vol. abs/1705.07874, 2017.

[25] M. Kamp, L. Adilova, J. Sicking, F. Huger, P. Schlicht, T. Wirtz, and ¨ S. Wrobel, “Efficient decentralized deep learning by dynamic model averaging,” in ECML/PKDD, 2018.   
[26] H. T. Nguyen, V. Sehwag, S. Hosseinalipour, C. G. Brinton, M. Chiang, and H. V. Poor, “Fast-convergent federated learning,” IEEE Journal on Selected Areas in Communications, vol. 39, pp. 201–218, 2021.   
[27] A. Reisizadeh, H. Taheri, A. Mokhtari, H. Hassani, and R. Pedarsani, “Robust and communication-efficient collaborative learning,” in NeurIPS, 2019.   
[28] H. Tang, S. Gan, C. Zhang, T. Zhang, and J. Liu, “Communication compression for decentralized training,” in NeurIPS, 2018.   
[29] G. E. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” ArXiv, vol. abs/1503.02531, 2015.   
[30] S. Han, H. Mao, and W. J. Dally, “Deep compression: Compressing deep neural network with pruning, trained quantization and huffman coding,” arXiv: Computer Vision and Pattern Recognition, 2016.   
[31] G. Huang, S. Liu, L. van der Maaten, and K. Q. Weinberger, “Condensenet: An efficient densenet using learned group convolutions,” in CVPR, 2018.   
[32] Y. He, X. Zhang, and J. Sun, “Channel pruning for accelerating very deep neural networks,” IEEE International Conference on Computer Vision (ICCV), 2017.   
[33] C. Zhu, S. Han, H. Mao, and W. J. Dally, “Trained ternary quantization,” ArXiv, vol. abs/1612.01064, 2017.   
[34] S. K. Esser, J. L. McKinstry, D. Bablani, R. Appuswamy, and D. S. Modha, “Learned step size quantization,” ArXiv, 2020.   
[35] J. Gou, B. Yu, S. J. Maybank, and D. Tao, “Knowledge distillation: A survey,” ArXiv, vol. abs/2006.05525, 2021.   
[36] L. Yu, V. O. Yazici, X. Liu, J. van de Weijer, Y. Cheng, and A. Ramisa, “Learning metrics from teachers: Compact networks for image embedding,” in CVPR, 2019.   
[37] F. Tung and G. Mori, “Similarity-preserving knowledge distillation,” in ICCV, 2019.   
[38] S. Ahn, S. X. Hu, A. C. Damianou, N. D. Lawrence, and Z. Dai, “Variational information distillation for knowledge transfer,” in CVPR, pp. 9155–9163, 2019.   
[39] B. Heo, M. Lee, S. Yun, and J. Y. Choi, “Knowledge transfer via distillation of activation boundaries formed by hidden neurons,” in AAAI, 2019.   
[40] S. Hardy, W. Henecka, H. Ivey-Law, R. Nock, G. Patrini, G. Smith, and B. Thorne, “Private federated learning on vertically partitioned data via entity resolution and additively homomorphic encryption,” ArXiv, vol. abs/1711.10677, 2017.   
[41] J. Tan, L. Zhang, Y. Liu, A. Li, and Y. Wu, “Residue-based label protection mechanisms in vertical logistic regression,” In 2022 38th IEEE International Conference on Data Engineering (ICDE), 2022.   
[42] I. Ceballos, V. Sharma, E. Mugica, A. Singh, A. Roman, P. Vepakomma, and R. Raskar, “Splitnn-driven vertical partitioning,” ArXiv, vol. abs/2008.04137, 2020.   
[43] P. Vepakomma, O. Gupta, T. Swedish, and R. Raskar, “Split learning for health: Distributed deep learning without sharing raw patient data,” ArXiv, vol. abs/1812.00564, 2018.   
[44] K. Cheng, T. Fan, Y. Jin, Y. Liu, T. Chen, and Q. Yang, “Secureboost: A lossless federated learning framework,” IEEE Intelligent Systems, vol. 36, pp. 87–98, 2021.   
[45] C. Dong, L. Chen, and Z. Wen, “When private set intersection meets big data: an efficient and scalable protocol,” Proceedings of the 2013 ACM SIGSAC conference on Computer & communications security, 2013.   
[46] D. Dua and C. Graff, “UCI machine learning repository,” 2017. [Online]. Available: http://archive.ics.uci.edu/ml   
[47] K. Bonawitz, V. Ivanov, B. Kreuter, A. Marcedone, H. B. McMahan, S. Patel, D. Ramage, A. Segal, and K. Seth, “Practical secure aggregation for privacy-preserving machine learning,” Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, 2017.   
[48] CriteoLabs, “The criteo dataset for kaggle display advertising challenge,” https://labs.criteo.com/2014/02/download-dataset/.   
[49] Y. LeCun, “The mnist database,” http://yann.lecun.com/exdb/mnist/.   
[50] H. Xiao, K. Rasul, and R. Vollgraf. (2017) Fashion-mnist: a novel image dataset for benchmarking machine learning algorithms.   
[51] A. L. Maas, R. E. Daly, P. T. Pham, D. Huang, A. Y. Ng, and C. Potts, “Learning word vectors for sentiment analysis,” in Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies, 2011.   
[52] Kaggle, https://www.kaggle.com/datasets.