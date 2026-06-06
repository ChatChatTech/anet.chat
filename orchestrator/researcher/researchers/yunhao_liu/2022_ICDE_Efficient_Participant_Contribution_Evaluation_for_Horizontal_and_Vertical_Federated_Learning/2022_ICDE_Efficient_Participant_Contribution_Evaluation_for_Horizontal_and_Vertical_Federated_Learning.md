# Efficient Participant Contribution Evaluation for Horizontal and Vertical Federated Learning

Junhao Wang, Lan Zhang∗, Anran Li, Xuanke You, Haoran Cheng

School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

{junhaow,anranLi,yxkyong,chr990315}@mail.ustc.edu.cn, {zhanglan}@ustc.edu.cn

Abstract—Federated Learning (FL) enables multiple participants to collaboratively train a model in a privacy-preserving way. The performance of the FL model heavily depends on the quality of participants’ local data, which makes measuring the contributions of participants an essential task for various purposes, e.g., participant selection and reward allocation. The Shapley value is widely adopted by previous work for contribution assessment, which, however, requires repeatedly leave-oneout retraining and thus incurs the prohibitive cost for FL. In this paper, we propose a highly efficient approach, named DIG-FL, to estimate the Shapley value of each participant without any model retraining. It’s worth noting that our approach is applicable to both vertical federated learning (VFL) and horizontal federated learning (HFL), and we provide concrete design for VFL and HFL. In addition, we propose a DIG-FL based reweight mechanism to improve the model training in terms of accuracy and convergence speed by dynamically adjusting the weights of participants according to their per-epoch contributions, and theoretically analyze the convergence speed. Our extensive evaluations on 14 public datasets show that the estimated Shapley value is very close to the actual Shapley value with Pearson’s correlation coefficient up to 0.987, while the cost is orders of magnitude smaller than state-of-the-art methods. When there are more than 80% participants holding low-quality data, by dynamically adjusting the weights, DIG-FL can effectively accelerate the convergence and improve the model accuracy.

# I. INTRODUCTION

The rapid development of Artificial Intelligence, and social networking applications is incurring enormous growth of the data generated at the network edge, which makes data privacy concerns particularly important [1], [2]. Federated learning (FL) is an emerging technology that allows multiple participants to collectively train a global machine learning model without exposing their local training data and training process. Based on how data is distributed among the participants in the feature and sample ID space, there are two widely adopted federated learning frameworks: vertical federated learning (VFL) and horizontal federated learning (HFL). The architectures of VFL and HFL systems are quite different by design. HFL applies to scenarios that participants share the same feature space, but have different samples, where the global model is obtained by aggregating local parameters of participants [3], [4], [5]. VFL applies to scenarios that participants share the same sample ID space but have different data features. VFL builds a global model by computing gradients with features

∗Lan Zhang is the corresponding author. CopyRight © 2022. International Conference on Data Engineering (www.icde.org). All rights reserved.

from participants in a privacy-preserving manner [3], [6], [7], [8], e.g., using encryption techniques.

In FL, the performance of the global model largely depends on the quality of local data. For example, when many participants possess non-IID (Independent and Identically Distributed) or erroneous data, it hinders the global model from achieving a good performance [9], [10], [11]. Therefore, it is essential to identify participants holding low-quality data, which is, however, intractable due to the invisibility of participants’ local data. This challenge drives us to explore an effective way to measure the contributions of participants in FL systems, which could bring multi-fold benefits: (1) It helps us to understand behaviors of FL models by tracing back to distributed training datasets; (2) It can localize lowquality participants and thus reduce their impact to mitigate performance degradation or avoid adversarial sample attacks; (3) During the training process, weights of participants can be adjusted according to their contributions so as to boost the model convergence; (4) For the commercial use of FL, fair credit/reward allocation for participants based on their contributions is needed.

Many efforts have been devoted to measuring contributions of training samples and participants in machine learning systems. For centralized machine learning, a series of approaches aim to interpret the model behavior by analyzing the influence of data samples on the model’s predictions [12], [13], [14]. However, they require access to training data, thus cannot be directly adopted by FL. Recently, Xue et al. [15] and Li et al. [16], [17] use the influence function-based method to measure the influence of participants in FL, which requires participants to calculate and upload their Hessian matrices or part of Hessian matrices. Applying those methods to calculate contribution requires exponential calculation of influence function, resulting in large extra overhead. Zhang et al. [18] simply use cosine distance between each participant’s gradient and the gradient of the final global model to measure participant contribution for HFL. All those methods do not use the Shapley value [19], hence they do not have the efficiency, symmetry, linearity, and null player properties. Moreover, they are only applicable to HFL, not to VFL. There are some prior arts leveraging the Shapley value to measure contributions of samples [20], [21] for centralized learning. However, applying those methods to FL requires repeatedly retraining the model, which imposes unacceptable computation and communication overhead, especially for resource-constrained devices[22]. Few work use the Shapley value to assess the contributions of participants in FL [23], [24]. For HFL, Song et al. [23] propose two methods to approximate the Shapley value without retraining model, which, however, still require to exponentially test model performance, and thus impose prohibitive computation cost. For VFL, Wang et al. [24] propose a method to estimate the Shapley value for an individual feature, which, however, introduces extra severe privacy risk since it needs to access and permutate the training data.

In this work, we aim to propose a highly efficient approach to accurately assess the Shapley value based contribution of each participant for both VFL and HFL. Obtaining the contribution assessment, we can design fair incentive mechanisms, localize low-quality participants or reweight participants to improve the model performance and convergence speed. Towards this ambitious goal, we need to answer the following challenging questions:

(1) How to accurately measure the contribution of each participant with minimal extra cost, which should be significantly smaller than the training cost? The Shapley value provides a principled way, which is characterized by a collection of desirable properties, to evaluate how important each participant is to the overall collaborative learning. Following the definition of the Shapley value, existing methods require exponentially retraining the model or testing model performance, which is prohibitively expensive for FL. Therefore, a desired approach should assess contributions to closely approximate the actual Shapley values with minimal extra cost.

(2) How to design a general approach applicable to both VFL and HFL, especially for VFL using different cryptography techniques? HFL and VFL have completely different architectures, and both of them have various frameworks across a wide range of applications [3], [6], [8]. It is non-trivial to design an approach applicable to various FL frameworks.

(3) How to respect participants’ data privacy when assessing their contributions? The invisibility of participants’ local data is the most attractive feature of FL. Therefore, we need to measure the impact of each participant in the training process without access to their local data. It is challenging, since exiting contribution measuring methods often require extra computation and transmission, which cause privacy risk.

To address these questions, we use Shapley value to measure the contribution of each participant, and first define the utility function as the change in loss on the validation dataset via leave-one-out model retraining. Then, we theoretically analyze the impact of each participant on global gradients and the utility function, and prove that the change in utility function caused by removing each participant satisfies additivity. Leveraging the additivity, we turn the exponential calculation of the Shapley value into the linear calculation. Moreover, we utilize the training logs to calculate an approximation of the actual Shapley value, which requires no extra model training or access to local data. Our proposed approach, named DIG-FL, can efficiently and accurately measure the contributions of participants for HFL and VFL. And protecting data privacy and security is a major issue for artificial intelligence applications [25], [26], [27]. We give the definition of privacy and analyze the privacy risks that our algorithm may have.

Our contributions are summarized as follows:

•We propose a novel approach DIG-FL to efficiently measure the Shapley value based contributions of participants for both HFL and VFL. We theoretically show that DIG-FL can accurately approximate the actual Shapley value using only training logs, which requires no extra model training or access to local data. We turn the exponential calculation of the Shapley value into the linear calculation, thus DIG-FL costs significantly smaller computation and communication cost than that of previous approaches. Besides, two of our algorithms for HFL and VFL do not introduce any additional privacy risk to FL systems.

•Based on the per-epoch contribution measured by DIG-FL, we design a participant reweight mechanism to improve the model training in terms of accuracy and convergence speed by dynamically adjusting the weights of participants. For both HFL and VFL, we theoretically analyze the convergence speed by using our reweight mechanism.

•We extensively evaluated our approach for HFL and VFL on 14 public datasets. For HFL, the evaluation results show that the estimated and the actual Shapley values are highly correlated, their Pearson’s correlation coefficient (PCC) is 0.968 on MNIST, 0.935 on CIFAR10, 0.952 on MOTOR and 0.833 on REAL. For VFL, we adopted a well-known FL framework [3], [28], as an example to test our approach in VFL systems. The estimated Shapley value and actual one match closely, with 0.987 PCC for vertical linear regression and 0.940 PCC for vertical logistic regression. Compared with conventional methods calculating the actual Shapley value, DIG-FL reduces computation cost by orders of magnitude, e.g., from $8 . 9 \times 1 0 ^ { 5 }$ s to $1 . 1 \times 1 0 ^ { 3 }$ s on MNIST for HFL, and from 76,584.7s to 13.77s on Seoul Bike Sharing Demand dataset [29] for VFL. Compared with state-of-the-art estimation methods, DIG-FL achieves better accuracy and consumes several orders of magnitude less cost. When there are more than 80% participants holding low-quality data, our reweight mechanism can effectively accelerate the convergence and improve the model accuracy from 67.7% to 95.3% on MNIST, from 70.9% to 89.9% on CIFAR10, from 55.2% to 86.5% on MOTOR and from 47.4% to 77.1% on REAL.

# II. PROBLEM AND MAIN IDEA

# A. Problem Description

In this work, our goal is to design an approach to efficiently and accurately assess the contribution of each participant for both HFL and VFL. We adopt the Shapley value as the metric due to its appealing properties and aim to accurately estimate the Shapley value with very constrained cost.

In HFL, each participant updates a local model with local training data, and a parameter server aggregates updates from all participants to train a global model. In VFL, there is usually a trusted third-party generating encryption key pairs. Each participant owns some features and a part of the complete model. All participants collaboratively train the complete model utilizing multiparty computation.

Before presenting our idea, we first provide a unified formalization of HFL and VFL. Given n participants ${ \mathcal { C } } =$ $\{ 1 , 2 , . . . , n \}$ and a server, model training starting from epoch 1 to epoch τ , in epoch t, participant i sends local update $\delta _ { t , i }$ to the server. The server collects $\boldsymbol { \Lambda _ { t } } ~ = ~ \{ \delta _ { t , 1 } , \delta _ { t , 2 } , . . . , \delta _ { t , n } \}$ , calculates the global gradient $\mathcal { G } _ { t } ,$ , and sends it to all participants. Each participant computes local update based on $\mathcal { G } _ { t }$ . This process continues to iterate until the model converges. For simplicity, we focus on the model training process and ignore the encryption details of VFL for now, and present the detailed VFL protocol in Sec.IV. We assume that at least one participant’s local data meet the quality standard of the learning task and the server holds a high-quality (e.g., errorfree and IID) validation dataset $\mathcal { D } ^ { v }$ to measure the performance of the global model. Note that, the volume of $\mathcal { D } ^ { v }$ is usually much smaller than that of the training data, therefore $\mathcal { D } ^ { v }$ is insufficient for model training but is easy to collect.

Since privacy preservation is the most attractive feature of FL, our design should not introduce any extra privacy risks during measuring contributions. Specifically, for HFL, we assume semi-honest server and participants, which is a common setting in most HFL work ([3], [30] et al.). Here we define two levels of privacy: 1) level-1: no participant’s local training data is transmitted/exposed to any other parties; 2) level-2: except for the local model, which is necessary for HFL model training, no additional information is transmitted/exposed to any other parties. Both privacy definitions do not allow direct exposure of local training data. Level-2 privacy is more stringent than level-1 privacy, because level-1 privacy allows the transmission of intermediate computation results (e.g., Hessian matrix) other than the local model, but level-2 privacy does not. Conventional HFL systems usually meet the level-2 privacy definition. Sometimes, to achieve a higher privacy protection level, HFL can adopt techniques such as homomorphic encryption [31], differential privacy [32] or secret sharing [33] to mask local model. Those techniques can also be adopted by DIG-FL, but how to apply them is out of scope of this work. For VFL, as previous work ([6], [33], [34] et al.), we assume a trusted third-party responsible for key management and semi-honest participants. The privacy definition is that any party can learn nothing from other parties beyond what is revealed by his/her input and output.

# B. Main Idea

The Shapley value[19] is a broadly adopted solution concept in cooperative game theory to measure how each participant contributes to the overall cooperation. Given a coalitional game $( V , N )$ , where N is a set of n participants and $V ( \cdot )$ is a utility function defined as $V : 2 ^ { \bar { N } } \to \bar { \mathbb { R } }$ , the Shapley value of participant i is:

$$
\phi_ {i} (V) = \sum_ {S \subseteq N} \frac {| S | ! (n - | S | - 1) !}{n !} (V (S) - V (S \backslash \{i \})). \tag {1}
$$

![](images/12e83d049ca299249cc3ec5ae9c2d5119cdcf0abefd9841efc9689bb31ebd270.jpg)



Fig. 1. System overview of DIG-FL in HFL. The reweight mechanism step is optional, which can be performed when we aim to identify the negatively influential participants and adjust the weights to boost model convergence based on per-epoch contributions.

Here, $V ( \cdot )$ is the untility function, $V ( S )$ is the worth of coalition S, indicating the total expected surplus the member of $S$ can obtain by cooperation. The Shapley value can be interpreted as: when participant i joins a coalition S, he/she demands his/her marginal contribution $V ( S ) - V ( S \backslash \{ i \} )$ as a fair payoff, and then for each participant the payoff is the average of his/her marginal contribution over all possible coalitions.

Generally, the utility function is defined as the performance of the global model, that is, the loss of the global model on the validation dataset. The utility function of a coalition S is defined as:

$$
V (S) = \operatorname{loss} ^ {v} (\theta (\varnothing)) - \operatorname{loss} ^ {v} \left(\theta_ {\tau} (S)\right), \tag {2}
$$

where $\it { l o s s } ^ { v }$ is the loss function on the validation dataset, $\theta ( \emptyset ) \ = \ \theta _ { 0 }$ is the initial global model and $\theta _ { \tau } ( S )$ is the final global model trained by the coalition S. The marginal contribution of participant z joining in the coalition $S \setminus \{ z \}$ is $V ( S ) - V ( S { \bar { \backslash } } \{ z \} )$ ).

Directly applying Shapley value to the FL system requires the exponential calculation of the utility function change and marginal contribution. For example, to calculate the marginal contribution of participant i joining coalition $S ,$ the model needs to be trained twice, once with i and once without i. The calculation of the Shapley value requires iteratively calculating the marginal contribution. Some existing works ([20], [21] et al.) focus on reducing the number of repetitive training to reduce the cost in centralized learning. However, applying those methods to FL still requires repeatedly retraining the model, which imposes unacceptable computation and communication overhead, especially for resource-constrained devices [22]. Therefore, we aim to efficiently calculate Shapley value in a variety of FL systems, without model retraining.

The most critical question in our design is how to measure the changes in global model performance caused by participant(s) withdrawing from the FL system, without model retraining. Since the change of model performance essentially comes from the change of model parameters, we translate this question into how to measure the changes in global model’s parameters and gradients caused by participant(s) withdrawing, which is the impact of participant(s), without model retraining. To answer this question, we delve into the training process of FL and find the way to efficiently measure the impact of each participant. Then we model the utility function based on impacts of participants and propose to use only the training log (local gradients from all participants) to estimate the marginal contribution. DIG-FL uses the training log and the validation dataset to calculate perepoch contributions and aggregate them to approximate the actual Shapley value during the whole training process. The per-epoch contribution can be utilized for various purposes, such as dynamically reweighting participant, selecting optimal participant under a budget constraint, a fairer contributionbased payment, etc. In this work, we design a participant reweight mechanism to improve the model training in terms of accuracy and convergence speed.

Taking HFL as an example, Fig. 1 shows the overview of DIG-FL working in an HFL system. There are four main steps: 1) Participants update model using local training data and send local gradients to the server; 2) The server evaluates the contribution of each participant in each epoch, including impact measurement (Sec.II-C) and contribution calculation (Sec.II-D) ; 3) The server performs gradient aggregation to obtain the updated global model; 4) The server sends model updates to all participants. The reweight mechanism is optional, which can be enabled when we want to mitigate the negative influence of participants with low-quality training data. We will introduce the details of the reweight mechanism in Sec.II-F.

# C. Impact Measurement

We study the change in global model gradients and parameters due to removing a participant or a subset of participants in the training process for HFL and VFL.

1) For HFL: In epoch t, participant i updates the current global model $\theta _ { t - 1 }$ using local data to obtain the local model $\theta _ { t - 1 , i }$ and sends it to the server. The server aggregates local models from participants to obtain the global model $\begin{array} { r } { \theta _ { t } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \theta _ { t - 1 , i } } \end{array}$ . Let the local update of participant i be $\delta _ { t , i } = \theta _ { t - 1 } - \theta _ { t - 1 , i }$ . The server gets $\Lambda _ { t } = \{ \delta _ { t , 1 } , \delta _ { t , 2 } , . . . , \delta _ { t , n } \}$ , computes the global gradient $\begin{array} { r } { \mathcal G _ { t } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \bar { \delta } _ { t , i } } \end{array}$ i and update the global model $\theta _ { t } = \theta _ { t - 1 } - \mathcal { G } _ { t }$ . When participant z is removed in training process, at epoch t, the gradients $\mathcal { G } _ { t } ^ { - z }$ , change in gradients is $\Delta \mathcal { G } _ { t } ^ { - z } = \mathcal { G } _ { t } ^ { - z } - \mathcal { G } _ { t }$ and change in parameters is $\begin{array} { r } { \Delta \theta _ { t } ^ { - z } = \theta _ { t } ^ { - z } - \bar { \theta } _ { t } = - \sum _ { j = 1 } ^ { t } \Delta \mathcal { G } _ { j } ^ { - z } } \end{array}$ .

Lemma 1. For HFL, in epoch t, if the loss function is twice-differentiable, when participant z is removed, change in gradient is:

$$
\Delta \mathcal {G} _ {t} ^ {- z} = \mathcal {G} _ {t} ^ {- z} - \mathcal {G} _ {t} = - \frac {1}{n} \delta_ {t, z} + \alpha_ {t} \Omega_ {t} ^ {- z}, \tag {3}
$$

where $\begin{array} { r } { \Omega _ { t } ^ { - z } = H _ { \theta _ { t - 1 } } ( \sum _ { j = 1 } ^ { t - 1 } \Delta { \mathcal G } _ { j } ^ { - z } ) } \end{array}$ and $\alpha _ { t }$ is the learning rate at epoch t.

And the change satisfies additivity, that is, when a subset of participants S is removed, change in gradients is $\Delta \mathcal { G } _ { t } ^ { - S } =$ $\textstyle \sum _ { i \in S } \Delta \mathcal { G } _ { t } ^ { - i }$ .

Proof Sketch. We first study the change of model parameters and gradients after upweighting participant z by a small ε. We assume that the initialization model is $\theta _ { 0 } .$ . For HFL, at epoch t, the global gradient is

$$
\mathcal {G} _ {t} = \frac {1}{n} \sum \delta_ {t, i} = \alpha_ {t} \frac {1}{n} \sum \nabla l o s s (i, \theta_ {t - 1}), \tag {4}
$$

where ∇loss $( i , \theta _ { t - 1 } )$ is the local gradient calculated by participant i using the local data and global model $\theta _ { t - 1 }$ of the last epoch.

If upweight participant z by ε during the whole training, at epoch t, the global gradient is

$$
\begin{array}{l} \mathcal {G} _ {t} ^ {\varepsilon z} = \frac {1}{n} \sum_ {1} \delta_ {t, i} ^ {\varepsilon z} + \varepsilon \delta_ {t, i} ^ {\varepsilon z} \tag {5} \\ = \alpha_ {t} \frac {1}{n} \sum \nabla l o s s (i, \theta_ {t - 1} ^ {\varepsilon z}) + \alpha_ {t} \varepsilon \nabla l o s s (z, \theta_ {t - 1} ^ {\varepsilon z}), \\ \end{array}
$$

where $\theta ^ { \varepsilon z }$ is the global model after upweighting z by ε.

At epoch t, the change of global gradients is:

$$
\Delta \mathcal {G} _ {t} ^ {\varepsilon z} = \mathcal {G} _ {t} ^ {\varepsilon z} - \mathcal {G} _ {t} \tag {6}
$$

$$
= \alpha \varepsilon \nabla l o s s (z, \theta_ {t - 1}) + \alpha H _ {\theta_ {t - 1}} \Delta \theta_ {t - 1} ^ {\varepsilon z}.
$$

Since removing the participant z is equivalent to upweight-$\textstyle i n g \ z b y - { \frac { 1 } { n } }$ , we can linearly approximate the gradient change caused by removing z:

$$
\Delta \mathcal {G} _ {t} ^ {- z} = - \frac {1}{n} \delta_ {t, z} + \alpha H _ {\theta_ {t - 1}} (\sum_ {j = 1} ^ {t - 1} \Delta \mathcal {G} _ {j} ^ {- z}) \tag {7}
$$

Similarly, when removing a subset of participants $S ,$ the change in gradients is $\begin{array} { r } { \Delta \bar { \mathcal { G } } _ { t } ^ { - S } = \sum _ { i \in S } \bar { \Delta \bar { \mathcal { G } } _ { t } ^ { - i } } } \end{array}$ .

2) For VFL: The training data is vertically partitioned and the model is distributed. Each participant i owns feature $x _ { i }$ of training data and a local model $\theta _ { i } .$ . The label y of training data is owned by one participant or the trusted third-party. The training dataset is $\mathcal { D } \ = \ \{ ( X [ j ] , y [ j ] ) , 0 \ < \ j \ \leq \ m \}$ , where $X [ j ] = ( x _ { 1 } [ j ] , x _ { 2 } [ j ] , . . . , x _ { n } [ j ] ) ^ { \dagger } .$ . In epoch t, the global model is $\pmb { \theta } _ { t - 1 } = ( \theta _ { t - 1 , 1 } , \theta _ { t - 1 , 2 } , . . . , \theta _ { t - 1 , n } ) ^ { \top }$ , and participant i calculates the local result with the local parameters $\theta _ { t - 1 , \cdot }$ i and training data, which is $\delta _ { t , i } ~ = ~ f ( \theta _ { t - 1 , i } , x _ { i } )$ , and sends it to the trusted third-party. Aggregating local results $\Lambda _ { t } = \{ \delta _ { t , 1 } , \delta _ { t , 2 } , . . . , \delta _ { t , n } \}$ , the trusted third-party computes the global loss $L ( \delta _ { t , 1 } , \delta _ { t , 2 } , . . . , \delta _ { t , n } )$ where L is the loss function. To facilitate analysis, we can define loss as loss $\left( \pmb \theta _ { t } \right)$ . The global gradient is

$$
\begin{array}{l} \mathcal {G} _ {t} \stackrel {{d e f}} {{=}} \alpha_ {t} \nabla l o s s (\boldsymbol {\theta} _ {t - 1}) \\ = \alpha_ {t} \left(\frac {\partial l o s s (\boldsymbol {\theta} _ {t - 1})}{\partial \theta_ {t - 1 , 1}},..., \frac {\partial l o s s (\boldsymbol {\theta} _ {t - 1})}{\partial \theta_ {t - 1 , n}}\right) ^ {\top}, \\ \end{array}
$$

where $\alpha _ { t }$ is the learning rate at epoch t.

If for any $x _ { i } , ~ f ( 0 , x _ { i } ) ~ \equiv ~ 0 .$ , then when the model is initialized to 0, removing the participant z is equivalent to not updating the local model of z in each epoch. That means the local output of participant z is always 0, which does not affect the calculation of loss or the training of the model.

After removing the participant z, the global model is $\pmb { \theta } ^ { - z } \overset { d e f } { = } ( \theta _ { 1 } ^ { - z } , . . . , \theta _ { z } ^ { - z } \equiv 0 , . . . , \theta _ { n } ^ { - z } ) ^ { \top }$ , and the global loss is loss $( \pmb { \theta } _ { t - 1 } ^ { - z } )$ . The global gradient is

$$
\begin{array}{l} \mathcal {G} _ {t} ^ {- z} = \alpha_ {t} d i a g (\vec {v} _ {z}) \nabla l o s s (\pmb {\theta} _ {t - 1} ^ {- z}) \\ = \alpha_ {t} d i a g (\vec {v} _ {z}) \left(\frac {\partial l o s s (\boldsymbol {\theta} _ {t - 1} ^ {- z})}{\partial \theta_ {t , 1}},..., \frac {\partial l o s s (\boldsymbol {\theta} _ {t - 1} ^ {- z})}{\partial \theta_ {t , n}}\right) ^ {\top}, \\ \end{array}
$$

where ${ \vec { v } } _ { z } = ( v _ { 1 } , . . . , v _ { j } , . . . , v _ { n } ) , { \mathrm { i f } } \ j = z , $ , then $v _ { j } = 0 ,$ , otherwise $v _ { j } = 1$ . The change in gradients is $\Delta \mathcal { G } _ { t } ^ { - z } = \mathcal { G } _ { t } ^ { - z }$ z −Gt and change in parameters is $\Delta \bar { \theta _ { t } ^ { - z } } = \theta _ { t } ^ { - z } - \theta _ { z } = - \sum _ { j = 1 } ^ { t } \Delta \mathcal { G } _ { j } ^ { - z }$ .

Lemma 2. For VFL, in epoch t, if the loss function is twicedifferentiable, when participant z is removed, the change in gradients is:

$$
\Delta \mathcal {G} _ {t} ^ {- z} = \mathcal {G} _ {t} ^ {- z} - \mathcal {G} _ {t} = - (E - d i a g (\vec {v} _ {z})) \mathcal {G} _ {t} - \alpha_ {t} \Omega_ {t} ^ {- z}, \tag {8}
$$

where $\begin{array} { r } { \Omega _ { t } ^ { - z } = d i a g ( \vec { v } _ { z } ) H _ { ( \theta _ { t - 1 } ) } ( \sum _ { j = 1 } ^ { t - 1 } \Delta \mathcal { G } _ { j } ^ { - z } ) } \end{array}$ and E is the identity matrix.

And the change satisfies additivity, namely, when a subset of participants S is removed, the change in gradients is:

$$
\Delta \mathcal {G} _ {t} ^ {- S} = \sum_ {i \in S} \Delta \mathcal {G} _ {t} ^ {- i}. \tag {9}
$$

Proof Sketch. We assume that the initialized model is $\begin{array} { r } { \pmb \theta _ { 0 } = \mathbf 0 . } \end{array}$ .

At epoch t, the change in gradients is:

$$
\begin{array}{l} \Delta \mathcal {G} _ {t} ^ {- z} = \mathcal {G} _ {t} ^ {- z} - \mathcal {G} _ {t} \\ = \alpha_ {t} \operatorname{diag} \left(\vec {v} _ {z}\right) \nabla \text { loss } \left(\boldsymbol {\theta} _ {t - 1} ^ {- z}\right) - \alpha_ {t} \nabla \text { loss } \left(\boldsymbol {\theta} _ {t - 1}\right) \\ \approx - (E - \operatorname{diag} (\vec {v} _ {z})) \mathcal {G} _ {t} \tag {10} \\ - \alpha_ {t} d i a g (\vec {v} _ {z}) H _ {\left(\boldsymbol {\theta} _ {t - 1}\right)} \sum_ {i = 1} ^ {t - 1} \Delta \mathcal {G} _ {i} ^ {- z}. \\ \end{array}
$$

In particular, when epoch is 1,

$$
\Delta \mathcal {G} _ {1} ^ {- z} = - (E - d i a g (\vec {v} _ {z})) \mathcal {G} _ {1}. \tag {11}
$$

Similarly, when a subset of participants S is removed, the change in gradients is $\begin{array} { r } { \Delta \mathcal { G } _ { t } ^ { - \bar { S } } = \sum _ { i \in S } \Delta \mathcal { G } _ { t } ^ { - i } } \end{array}$ . □

For HFL and VFL, Lemma 1 and Lemma 2 illustrate how to measure the impact of each participant on model parameters and gradients.

# D. Contribution Calculation

Based on the impact of each participant on model parameters and gradients, we can measure the impact of the participant on the loss of the validation dataset $\mathcal { D } ^ { v }$ , that is the impact on the utility function.

Lemma 3. For HFL and VFL, when the participant $z \textit { i s }$ removed, the change in utility function is

$$
\Delta V ^ {- z} = \sum_ {t = 1} ^ {\tau} \nabla l o s s ^ {v} (\theta_ {t - 1}) \Delta \mathcal {G} _ {t} ^ {- z}. \tag {12}
$$

And the change of utility function satisfies additivity, that is, when a set of participants S is removed, the change in utility function $\begin{array} { r } { \Delta \dot { V } ^ { - \dot { S } } = \dot { \sum _ { i \in S } } \Delta V ^ { - i } . } \end{array}$ ∆V −i.

Lemma 3 shows how to measure the impact of each participant on the utility function. Due to its additivity, we can reduce the exponential complexity of calculating the Shapley value to linear complexity and utilize the training log and the Hessian matrix of the loss to estimate the actual contribution. For HFL and VFL, the Shapley value of participant i is

$$
\begin{array}{l} \phi_ {i} = \sum_ {\substack {S \subseteq \mathcal {C} \\ \tau}} \frac {V (S) - V (S \setminus \{i \})}{n \binom {n - 1} {| S |}} \tag{13} \\ = - \sum_ {t = 1} ^ {\tau} \nabla l o s s ^ {v} (\theta_ {t - 1}) \Delta \mathcal {G} _ {t} ^ {- i}. \\ \end{array}
$$

At epoch t, the per-epoch contribution of participant i is

$$
\begin{array}{l} \phi_ {t, i} = - \nabla \text { loss } ^ {v} (\theta_ {t - 1}) \Delta \mathcal {G} _ {t} ^ {- i} \tag {14} \\ = \nabla l o s s ^ {v} (\theta_ {t - 1}) K _ {t, i} + \alpha_ {t} \nabla l o s s ^ {v} (\theta_ {t - 1}) \Omega_ {t} ^ {- i} \\ \end{array}
$$

and where in VFL $\begin{array} { r } { d i a g ( \vec { v } _ { i } ) H _ { ( \pmb { \theta } _ { t - 1 } ) } ( \sum _ { i = 1 } ^ { t - 1 } \Delta \mathcal { G } _ { j } ^ { - i } ) } \end{array}$ $\begin{array} { r } { \Omega _ { t } ^ { - i } = H _ { \theta _ { t - 1 } } ( \dot { \sum } _ { i = 1 } ^ { t - 1 } \dot { \Delta { g _ { j } } ^ { - i } } ) } \end{array}$ ${ \cal K } _ { t , i } ~ = ~ - ( { \cal E } ~ - ~ d i a g ( \vec { v } _ { i } ) ) { \cal \mathcal G } _ { t }$ − i, and in HFL . $K _ { t , i } = - \textstyle \frac { 1 } { n } \delta _ { t , i }$ and $\begin{array} { r l } { \Omega _ { t } ^ { - i } } & { { } = } \end{array}$

And the contribution of participant i in the whole training process is

$$
\phi_ {i} = \sum_ {t = 1} ^ {\tau} \phi_ {t, i}. \tag {15}
$$

# E. Complexity Analysis and Further Optimization

With the aforementioned two steps, DIG-FL enables us to highly efficiently calculate the contribution of each participant for both HFL and VFL. The per-epoch contribution of participant z at epoch t mainly consists of two terms: ∇los $\ s ^ { v } ( \theta _ { t - 1 } ) K _ { t , z }$ and $\alpha _ { t } \nabla l o s s ^ { v } ( \theta _ { t - 1 } ) \Omega _ { t } ^ { - z }$ .

For calculating the first term loss $^ { v } ( \theta _ { t - 1 } ) K _ { t , z }$ , the server needs $O ( \tau n p )$ operations, while participants do not need any additional computation or communication. For directly calculating the second term $\alpha _ { t } \nabla l o s s ^ { v } ( \theta ) \Omega _ { t } ^ { - z }$ , the server needs to construct $H _ { \theta } ,$ , the Hessian matrix of the loss function, which requires $O ( \tau n p ^ { 2 } )$ operations (p is the number of model parameters). All participants need to calculate G and upload $H _ { \theta }$ and G to the server, which requires $O ( \tau p ^ { 2 } )$ operations and $O ( \tau p ^ { 2 } )$ communication cost. Considering τ and $p$ could be large in many deep learning tasks, directly computing Eq.(14) and Eq.(15) could cause large extra computation and communication overhead. To reduce the cost, we explore the magnitude of the first and second terms and notice that the second term is much smaller than the first one due to the small coefficient α, i.e., the learning rate. After ignoring the second term, let the contribution of participant i at epoch t be:

$$
\hat {\phi} _ {t, i} = \nabla l o s s ^ {v} (\theta_ {t - 1}) K _ {t, i}. \tag {16}
$$

Our experiential results in Sec.V-B (Fig.2 and Table II) show that $\dot { \phi } _ { t , i }$ i and $\phi _ { t , i }$ i are very close, and the error caused by ignoring the second term is within 5%. Therefore, in practice, we can achieve a significantly more efficient and fairly accurate approximation of the actual contribution by computing φˆt,i.

Optimization for HFL. Based on the above analysis, for HFL, we design two calculation methods for different application scenarios. The first method is suitable for scenarios that require high estimation accuracy, for example, the participants are several companies. The second method is suitable for scenarios where resources are severely limited, for example, the participants are personal devices or end devices.

(1)Interactive contribution evaluation. Avoid direct calculation of $H _ { \theta _ { t - 1 } }$ with second-order optimization. We use Hessian-vector products (HVP) [35], [36] to efficiently calculate $\Omega _ { t } ^ { - z }$ which requires O(τ np) operations, and then compute los $\cdot s ^ { v } ( \theta _ { t - 1 } ) \Omega _ { t } ^ { - z }$ .   
(2)Resource-saving contribution evaluation. In the calculation process, we take the $\widehat { \phi } _ { t , i }$ which ignores the second term − $\cdot \alpha _ { t } \nabla l o s s ^ { v } ( \theta _ { t - 1 } ) \Omega _ { t } ^ { - z }$ as the contribution. At this time, only the server needs to operate $O ( \tau n p )$ , without any additional communication and calculation overhead, and the contribution of each participant can be calculated.

For VFL, each participant only holds a part of the complete model and data, and the intermediate results are transmitted to each other under encryption, which makes it impossible to calculate the Hessian matrix of model parameters. Therefore, in VFL, we also take the $\hat { \phi } _ { t , i }$ as the contribution.

# F. DIG-FL based Reweight Mechanism

DIG-FL is able to efficiently calculate both the per-epoch contribution and accumulative contribution of each participant during the training process for HFL and VFL. Such ability can bring a variety of new improvements to federated learning, including optimal participant selection under budget constraint, a fairer contribution-based payment mechanism, dynamic participant reweighting, etc. Here we present how to utilize DIG-FL to dynamic reweight participants to boost the convergence of FL. Participants with low contributions usually possess low-quality data (e.g., mislabeled samples and adversarial samples), which hinders the global model from achieving convergence [10]. Through the contribution from DIG-FL, we can identify the negatively influential participants and adjust the weights of participants during training which can reduce the negative impact of participants to boost model convergence.

In epoch t, the server calculates per-epoch contributions of all participants $\boldsymbol { \phi } _ { t } = \{ \phi _ { t , 1 } , \phi _ { t , 2 } , . . . , \phi _ { t , n } \}$ , and then rectifies $\phi _ { t , \cdot }$ i to get the non-negative weight of participant i and normalizes weights of all participants:

$$
\omega_ {t, i} = \frac {\max (\phi_ {t , i} , 0)}{\sum_ {i} ^ {n} \max (\phi_ {t , i} , 0)}. \tag {17}
$$

Applying these weights to local updates from participants, the server obtains reweighted updates:

$$
\tilde {\Delta} _ {t} = \left\{\omega_ {t, 1} \delta_ {t, 1}, \omega_ {t, 2} \delta_ {t, 2}, \dots , \omega_ {t, n} \delta_ {t, n} \right\}. \tag {18}
$$

Using $\tilde { \Delta } _ { t }$ instead of $\Delta _ { t } ,$ , the server calculates the adjusted global gradient $\tilde { \mathcal { G } } _ { t } ( \mathcal { C } )$ and updates the global model.

In Sec.III-C and Sec.IV-D, we theoretically analyze the convergence speed of DIG-FL based reweight mechanism for HFL and VFL.

# III. DIG-FL FOR HFL

In this section, we show how to apply our approach DIG-FL in HFL without local training data being revealed to any other party, including the server. And we give two methods suitable to calculate contribution for resource-sufficient and resourceconstrained situations. In addition, we show DIG-FL based reweight mechanism how to adjust weights of participants and theoretically analyze the convergence speed in HFL.

# A. HFL Protocol

For HFL, in epoch t, participant i updates the current global model $\theta _ { t - 1 }$ using local data to obtain the local model $\theta _ { t - 1 , i }$ and sends it to the server. Let the local update of participant i be $\delta _ { t , i } = \theta _ { t - 1 } - \theta _ { t - 1 , i }$ . The server gets $\Delta _ { t } = $ $\{ \delta _ { t , 1 } , \delta _ { t , 2 } , . . . , \delta _ { t , n } \}$ . According to Lemma 1 and Eq.14, the contribution of participant i at epoch t is:

$$
\begin{array}{l} \phi_ {t, i} = - \nabla l o s s ^ {v} (\theta_ {t - 1}) \Delta \mathcal {G} _ {t} ^ {- i} \\ = \frac {1}{n} \nabla l o s s ^ {v} (\theta_ {t - 1}) \delta_ {t, i} - \alpha_ {t} \nabla l o s s ^ {v} (\theta_ {t - 1}) \Omega_ {t} ^ {- i}, \tag {19} \\ \end{array}
$$

where $\alpha _ { t }$ is the learning rate at epoch t and,

$$
\Omega_ {t} ^ {- i} = H _ {\theta_ {t - 1}} (\sum_ {j = 1} ^ {t - 1} \Delta \mathcal {G} _ {j} ^ {- i}). \tag {20}
$$

Algorithm 1: Interactive contribution evaluation.   
1 The server initializes global model $\theta_0$ and sends it to all participants.  
2 for each epoch $t \leftarrow 1, 2, \ldots, \tau$ do  
3 The server calculates the derivative $v = \nabla loss^v (\theta_{t-1})$ .  
4 for each participant $i \leftarrow 1, 2, \ldots, n$ do  
5 Load global model $\theta_{t-1}$ ;  
6 Calculate $\Omega_t^{-i} = \hat{H}_{\theta_{t-1}} (\sum_{j=1}^{t-1} \Delta \mathcal{G}_j^{-i})$ and update $\theta_t$ with local data to get local model $\theta_{t,i}$ ;  
7 Send local model $\theta_{t,i}$ and $\hat{H}_{\theta_{t-1}} (\sum_{j=1}^{t-1} \Delta \mathcal{G}_j^{-i})$ and to the server.  
8 Recorde $\Delta \mathcal{G}_t^{-i} = -\frac{1}{n} \delta_{t,z} - \alpha_t \Omega_t^{-i}$ .  
9 The server receives all local models $\{\theta_{t,1}, \theta_{t,2}, \ldots, \theta_{t,n}\}$ and $\hat{H}_{\theta_{t-1}} (\sum_{j=1}^{t-1} \Delta \mathcal{G}_j^{-i})$ .  
10 Then, the server calculates $\phi_{t,i}$ use Eq.(19) for each participant.  
11 The server obtains and sends the global model $\theta_t$ to all participants.  
12 The server calculates the whole Shapley value using Eq.(15).

# •Algorithm #1: Interactive contribution evaluation.

The cost of calculating contribution is mainly concentrated in the Hessian matrix $H _ { \theta }$ . In this case, we design an interactive contribution evaluation method based on stochastic estimation using HVP [35]. Specifically, at epoch t, we can efficiently calculate vectors $\begin{array} { r l } { \Omega _ { t } ^ { - i } } & { { } = } \end{array}$ $\begin{array} { r } { \bar { H } _ { \theta _ { t - 1 } } ( \sum _ { i = 1 } ^ { t - 1 } \Delta \mathcal { G } _ { i } ^ { - i } ) } \end{array}$ , and then compute $\nabla l o s s ^ { v } ( \theta _ { t - 1 } ) \dot { \Omega } _ { t } ^ { - i } =$ ∇loss $^ { v } (  { \boldsymbol { \theta } } _ { t - 1 } )  { \boldsymbol { H } } _ { \theta _ { t - 1 } } ( \sum _ { i = 1 } ^ { t - 1 } \Delta  { \boldsymbol { \mathcal { G } } } _ { i } ^ { - i } )$ ∇ t, and finally compute $\phi _ { t , i }$ for each participant. The original HVP method computes the result for every participant one by one, which incurs prohibitively heavy cost and high privacy risk [37]. We let each participant calculate locally $\begin{array} { r } { \tilde { \hat { H } } _ { \boldsymbol { \theta } _ { t - 1 } } ( \sum _ { i = 1 } ^ { \bar { t } - 1 } \Delta \mathcal { G } _ { i } ^ { - i } ) } \end{array}$ and server calculates $\begin{array} { r } { E [ \hat { H } _ { \boldsymbol { \theta } _ { t - 1 } } ( \sum _ { i = 1 } ^ { t - 1 } \Delta \mathcal { G } _ { i } ^ { - i } ) } \end{array}$ ] as an unbiased estimator of $H _ { \theta _ { t - 1 } } ( \sum _ { i = 1 } ^ { t - 1 } \Delta \mathcal { G } _ { i } ^ { - i } )$ =1 G . The detail is in Algorithm 1.

•Algorithm #2: Resource-saving contribution evaluation.

In the case of limited resources, we ignore the smaller term $- \alpha \nabla l o s s ^ { v } ( \theta _ { t - 1 } ) \Omega _ { t } ^ { - i }$ . Then, at epoch t, the contribution of participant i is $\begin{array} { r } { \phi _ { t , i } \approx \frac { 1 } { n } \nabla l o s s ^ { v } ( \theta _ { t - 1 } ) \delta _ { t , z } } \end{array}$ . At this time, only the server needs to perform the operation of $O ( n p )$ , without any additional communication and calculation overhead, and the contribution of each participant can be calculated. The procedure is detailed in Algorithm 2.

Algorithm 2: Resource-saving contribution evaluation.   
1 The server initializes global model $\theta_0$ and sends it to participants.  
2 for each epoch $t \leftarrow 1,2,\ldots,\tau$ do  
3 The server calculates the derivative $v = \nabla loss^v (\theta_{t-1})$ .  
4 for each participant $i \leftarrow 1,2,\ldots,n$ do  
5 Load global model $\theta_{t-1}$ ;  
6 Update $\theta_t$ with local data to get local model $\theta_{t-1,i}$ ;  
7 Send local model $\theta_{t-1,i}$ to the server.  
8 The server receives all local models $\{\theta_{t-1,1},\theta_{t-1,2},\ldots,\theta_{t-1,n}\}$ ;  
9 The server calculates the $\phi_{t,i} \approx \frac{1}{n}\nabla loss^v (\theta_{t-1})\delta_{t,z}$ for each participant;  
10 The server obtains and sends the global model $\theta_t$ to all participants.  
11 The server calculates the whole Shapley value using Eq.(15).

# B. Privacy Analysis

For Algorithm #1, using local data, each participant i computes local model $\theta _ { t , i }$ and $\begin{array} { r } { \hat { H } _ { \boldsymbol { \theta } _ { t - 1 } } ( \sum _ { i = 1 } ^ { t - 1 } \Delta \mathcal { G } _ { j } ^ { \dot { - } i } ) } \end{array}$ and sends them to the server. The server performs aggregation and sends the global model to participants. No local training data is transmitted/exposed to any other parties. Hence, Algorithm #1 meets the level-1 privacy definition in Sec. II-A. Especially, compared with conventional HFL, which uploads only local model, Algorithm #1 requires each participant to additionally send the mean value of the Hessian matrix to the server. There are some recent works using gradients to recover the original data [38], [39], but no work has successfully recovered the original data using Hessian matrix. What can be inferred from the mean value of the Hessian matrix is still an open problem, therefore transmitting it may introduce an additional privacy risk in the future. Algorithm #2 uses training logs to conduct contribution measurement. As conventional HFL, participants only uploads local models. No local training data is uploaded or accessed by other parties, and no extra transmission is required. Hence, Algorithm #2 meets the level-2 privacy definition in Sec. II-A.

# C. DIG-FL based Reweight Mechanism for HFL

The server reweights global gradient according to per-epoch contribution:

$$
\tilde {\mathcal {G}} _ {t} (\mathcal {C}) = \sum_ {i = 1} ^ {n} \omega_ {t, i} \delta_ {t, i}. \tag {21}
$$

The server obtains the global model:

$$
\theta_ {t} = \theta_ {t - 1} - \tilde {\mathcal {G}} _ {t} (\mathcal {C}) = \theta_ {t} - \sum_ {i = 1} ^ {n} \omega_ {t, i} \delta_ {t, i}. \tag {22}
$$

Let the server possess a validation dataset, we prove that the HFL algorithm with our DIG-FL based reweight mechanism can make the loss function on the validation dataset monotonically decrease and analyze the convergence rate, which is $O ( l o g { \frac { 1 } { \epsilon ^ { 2 } } } )$ .

Lemma 4. Suppose the loss function on the validation dataset $\boldsymbol { l o s s ^ { v } ( \theta ) }$ is Lipschitz-smooth with constant $L ,$ and the modulus of local update $| | \delta _ { t , i } | |$ | has an upper bound δ. Let the learning rate $\alpha _ { t }$ satisfy $\begin{array} { r } { \alpha _ { t } \leq \frac { 2 } { L \delta ^ { 2 } } } \end{array}$ . The validation loss always monotonically decreases, i.e.,

$$
\operatorname{loss} ^ {v} \left(\theta_ {t + 1}\right) \leq \operatorname{loss} ^ {v} \left(\theta_ {t}\right). \tag {23}
$$

And,

$$
\min _ {1 \leq t \leq \tau} | | \nabla l o s s ^ {v} (\theta_ {t}) | | \leq \frac {\xi}{\sqrt {\tau}}, \tag {24}
$$

where ξ is a constant independent of the convergence process.

# IV. DIG-FL FOR VFL

Here, we first show how to apply DIG-FL to VFL by designing a VFL protocol. Then we give a privacy-preserving participant contribution calculation method based on encryption methods. Finally, we present DIG-FL based reweight mechanism for dynamically reweighting participants in training and theoretically validating its higher convergence speed.

# A. VFL Protocol

For VFL, there are usually a trusted third-party and n participants ${ \mathcal C } = \{ 1 , 2 , . . . , n \}$ . The trusted third-party generates and distributes encryption key pairs. The training data is vertically partitioned and thus the model is distributed. Participant i owns feature $x _ { i }$ of training data and a local model $\theta _ { i }$ . The label y of training data is owned by one participant or the trusted thirdparty. The training dataset is $\bar { \mathcal { D } } = \{ ( X [ i ] , y [ i ] ) , 0 < i \leq m \}$ , where $X [ i ] = ( x _ { 1 } [ i ] , x _ { 2 } [ i ] , . . . , x _ { n } [ i ] ) ^ { \top }$ and the global model is $\pmb \theta = ( \theta _ { 1 } , \bar { \theta _ { 2 } } , . . . , \theta _ { n } \bar { ) } ^ { \top }$ . Model training starts from epoch 1, and in epoch t, participant i calculates the local result with the local parameters and training data, which is $\delta _ { t , i } = f ( \theta _ { t - 1 , i } , x _ { i } )$ , and sends it to the trusted third-party.

To protect the data privacy of participants, the training is usually carried out on ciphertexts. Our design can easily apply to various VFL systems. Here we first ignore the details of encryption and present the general method to compute contributions and weights, and then give a concrete example in Sec.IV-B.

At epoch t, the global gradient:

$$
\mathcal {G} _ {t} = \alpha_ {t} \left(\frac {\partial l o s s (\boldsymbol {\theta} _ {t - 1})}{\partial \theta_ {t - 1 , 1}},..., \frac {\partial l o s s (\boldsymbol {\theta} _ {t - 1})}{\partial \theta_ {t - 1 , n}}\right) ^ {\top}. \tag {25}
$$

The per-epoch contribution of participant i is:

$$
\begin{array}{l} \phi_ {t, i} = - \nabla \text {loss} ^ {v} \left(\theta_ {t - 1}\right) \Delta \mathcal {G} _ {t} ^ {- i} \tag {26} \\ = \nabla l o s s ^ {v} (\theta_ {t - 1}) ((E - d i a g (\vec {v} _ {i})) \mathcal {G} _ {t} + \alpha_ {t} \Omega_ {t} ^ {- i}), \\ \end{array}
$$

where $\begin{array} { r c l } { \Omega _ { t } ^ { - i } } & { = } & { d i a g ( \vec { v } _ { z } ) H _ { ( \pmb { \theta } _ { t - 1 } ) } ( \sum _ { j = 1 } ^ { t - 1 } \Delta \mathcal { G } _ { j } ^ { - i } ) } \end{array}$ and $\begin{array} { r l } { \vec { v } _ { i } } & { { } = } \end{array}$ $( v _ { 1 } , . . . , v _ { j } , . . . , v _ { n } ) , { \mathrm { i f } } \ j = i , v _ { j } = 0 ,$ , else $v _ { j } = 1$ .

And as aforementioned in Sec.II-E, we ignore the second term when calculating contribution. The contribution of participant i at epoch t is:

$$
\phi_ {t, i} = \nabla l o s s ^ {v} (\boldsymbol {\theta} _ {t - 1}) (E - d i a g (\vec {v} _ {z})) \mathcal {G} _ {t}. \tag {27}
$$

# B. Running Example Protocol

There are different VFL frameworks in industry and academia, e.g., [3], [6], [8]. Here we adapt the well-known vertical linear regression proposed by [3] a running example to show how to adapt our approach in VFL.

For vertical linear regression, participant 1 owns local model $\theta _ { 1 }$ , local data $x _ { 1 }$ and label $y ;$ participant 2 owns local model $\theta _ { 2 }$ and local $x _ { 2 } ;$ and the trusted third-party generates key pairs. They jointly train a linear regression model $\pmb { \theta } = ( \theta _ { 1 } , \theta _ { 2 } ) ^ { \top }$ . The training data is $\mathcal { D } = \{ ( X [ i ] , y [ i ] ) , 0 < i \leq m \}$ , and the validation data is $\mathcal { D } ^ { v } = \{ ( X [ i ] , y [ i ] ) , 0 < i \leq m ^ { v } \}$ , where $X [ i ] = ( x _ { 1 } [ i ] , x _ { 2 } [ 2 ] ) ^ { \top }$ .

To apply DIG-FL to this training process, firstly, participants calculate ∇loss(θ) = ( ∂loss , ∂loss ) $\begin{array} { r } { \nabla l o s s ( \pmb { \theta } ) = ( \frac { \partial l o s s } { \partial \theta _ { 1 } } , \frac { \partial l o s s } { \partial \theta _ { 2 } } ) } \end{array}$ ∂θ1 ∂θ2 under the privacy framework of [3], which uses additive homomorphic encryption, denoted as [[·]]. Specifically, we have

$$
l o s s (\boldsymbol {\theta}) = \sum_ {\mathcal {D}} (\theta_ {1} x _ {1} + \theta_ {2} x _ {2} - y) ^ {2}, \tag {28}
$$

where loss is the loss function on the training data, and

$$
\frac {\partial l o s s}{\partial \theta_ {i}} = 2 \sum_ {\mathcal {D}} (\theta_ {1} x _ {1} + \theta_ {2} x _ {2} - y) x _ {i}. \tag {29}
$$

Letting $u _ { 1 } = \theta _ { 1 } x _ { 1 } , u _ { 2 } = \theta _ { 2 } x _ { 2 }$ , the encrypted gradient is

$$
[ [ \frac {\partial l o s s}{\partial \theta_ {i}} ] ] = [ [ 2 \sum_ {\mathcal {D}} (u _ {1} + u _ {2} - y) x _ {i} ] ]. \tag {30}
$$

Let $[ [ d ] ] = [ [ u _ { 1 } - y ] ] + [ [ u _ { 2 } ] ]$ , then the process of calculating ∂loss $\frac { \partial l o s \dot { s } } { \partial \theta _ { 1 } }$ ∂θ1 and $\frac { \partial l o s s } { \partial \theta _ { 2 } }$ usually includes the following five steps:

1) The trusted third-party creates a key pair and sends the public key to participant 1 and 2.   
2) Participant 1 computes $[ [ u _ { 1 } - y ] ]$ and sends it to participant 2.   
3) Participant 2 computes [[u2]] and [[d]], and sends [[d]] to participant 1.   
4) Participant 1 initializes $M _ { 1 }$ , computes $[ [ \frac { \partial l o s s } { \partial { \theta _ { 1 } } } ] ]$ and sends $[ [ \frac { \partial l o s s } { \partial \theta _ { 1 } } + M _ { 1 } ] ]$ ∂loss to the trusted third-party; participant 2 [ ∂θ1 initializes $M _ { 2 }$ , computes $[ [ \frac { \partial l o s s } { \partial { \theta _ { 2 } } } ] ]$ [ ∂θ2 and sends $[ [ \frac { \partial l o s s } { \partial { \theta _ { 2 } } } ~ +$ [ ∂loss + ∂θ2 $M _ { 2 } ] ]$ to the trusted third-party.   
5) The trusted third-participant 1, and pts, sends to to part $\frac { \partial l o s s } { \partial \theta _ { 1 } } + M _ { 1 }$ to $\frac { \partial l o s s } { \partial \theta _ { 2 } } + M _ { 2 }$ ∂θ2

To prevent the trusted third-party to learn information from participant 1 or participant 1 in this process, participants can hide their intermediate results (gradients) by adding encrypted random masks $M _ { 1 }$ and $M _ { 2 }$ .

And $\begin{array} { r } { \mathcal { G } ( \{ 1 \} ) \overset { d e f } { = } ( E - d i a g ( \vec { v } _ { 1 } ) ) \nabla l o s s ( \pmb { \theta } ) = ( \frac { \partial l o s s } { \partial \theta _ { 1 } } , 0 ) ^ { \top } } \end{array}$ and $\begin{array} { r } { \mathcal { G } ( \{ 2 \} ) \overset { d e f } { = } ( E - d i a g ( \vec { v } _ { 2 } ) ) \nabla l o s s ( \theta ) = ( 0 , \frac { \partial l o s s } { \partial \theta _ { 2 } } ) ^ { \top } } \end{array}$ ∂θ2

Secondly, following the same steps of calculating $\overleftarrow { \nabla } l o s s ( \pmb \theta )$ , participants calculate the validation gradient $\nabla l o s s ^ { v } ( { \pmb \theta } )$ under the privacy framework of [3].

The complete training process is shown in Algorithm 3.

Algorithm 3: DIG-FL for Vertical Linear Regression   
1 Participant 1 initializes local model $\theta_{0,1}$ and participant 2 initializes local model $\theta_{0,2}$ . The trusted third-party $P$ creates an encryption key pair and sends the public key to participants.  
2 for each round $t \leftarrow 1,2,\ldots,\tau$ do  
3 Jointly calculate $\mathcal{G}_t(\{1\})$ and $\mathcal{G}_t(\{2\})$ .  
4 Jointly calculate the validation gradient $\nabla loss^v(\theta_t)$ .  
5 Jointly calculates the shapley values $\phi_t = \{\phi_{t,1},\phi_{t,2}\}$ using Eq.(27);  
6 Participants update local models.  
7 The third-party calculates the Shapley value using Eq.(15).

We can also apply DIG-FL to various VFL frameworks including [6], [8] and we will present evaluations in Sec.V.

# C. Privacy Analysis

Algorithm #3 uses the vertical linear regression proposed by [3] as an example to show how to apply DIG-FL to VFL. According to the security analysis in [3], during the training process itself, any party can learn nothing from other parties beyond what is revealed by his/her own input and output. In addition to training model, Algorithm #3 needs participants to cooperatally compute $\mathcal { G } _ { t } ( \{ 1 \} ) , \mathcal { G } _ { t } ( \{ 2 \} )$ , and $\nabla l o s s ^ { v } ( \theta _ { t } )$ to estimate shapley values. During the calculation, since participants add encrypted random masks to hind their gradients, the trusted third-party can not infer or learn any information from participants [40]. Secondly, since the intermediate results transmitted are all encrypted by Paillier with key length 1024, participant 1 can only get its own gradients. That is not enough for participant 1 to learn or infer any information from participant 2, due to the inability of solving n equations in more than n unknowns[41]. Similarly, participant 2 can not learn any information from participant 1. At the end of Algorithm #3, participant 1 or participant 2 obtain the model parameters associated only with its own features. Therefore, Algorithm #3 meet the privacy definition in Sec.II-A.

# D. DIG-FL based Reweight Mechanism for VFL

The trusted third-party reweights participants and gets the tuned global gradient:

$$
\tilde {\mathcal {G}} _ {t} = \left(\omega_ {t, 1} \frac {\partial l o s s}{\partial \theta_ {t , 1}}, \omega_ {t, 2} \frac {\partial l o s s}{\partial \theta_ {t , 2}},..., \omega_ {t, n} \frac {\partial l o s s}{\partial \theta_ {t , n}}\right) ^ {\top}. \tag {31}
$$

And the updated model is $\pmb { \theta } _ { t } = \pmb { \theta } _ { t - 1 } - \alpha \tilde { \mathcal { G } } _ { t }$ .

Let the there is a validation dataset, under some conditions, we prove that VFL algorithms with DIG-FL based reweight mechanism can make the loss function of the validation dataset converge to the critical point and we also theoretically prove its sub-liner convergence rate.

Lemma 5. Suppose the validation loss function $l o s s ^ { v } ( \theta )$ is Lipschitz-smooth with constant L, and the gradient of training data has an upper bound δ. Let the learning rate $\alpha _ { t }$ satisfies $\begin{array} { r } { \alpha _ { t } \ \leq \ \frac { 2 } { L n \delta ^ { 2 } } } \end{array}$ , where n is the number of participant. Then, the validation loss always monotonically decreases, i.e.,

$$
l o s s ^ {v} (\theta_ {t + 1}) \leq l o s s ^ {v} (\theta_ {t}). \tag {32}
$$

And,

$$
\min _ {1 \leq t \leq \tau} | | \nabla l o s s ^ {v} (\theta_ {t}) | | \leq \frac {\xi}{\sqrt {\tau}}, \tag {33}
$$

where $\xi$ is a constant independent of the convergence process.

# V. EVALUATIONS

In this section, by experiments, we demonstrate the rationality of omitting the second term in Sec.II-E. Then we measure the effectiveness of DIG-FL approximating the actual Shapley value. In addition, we verify the superiority of our work by comparing with existing methods. Finally, we show that DIG-FL based reweight mechanism really can improve the global model with higher accuracy and faster convergence speed.

# A. Experimental Configuration

1) Datasets: For HFL, we use two public image datasets MNIST and CIFAR10, and two crawled datasets to test our methods in real-world scenarios. The crawled datasets include: a) MOTOR: it consists of 11,000 images from two classes: motorcycle and non-motorcycle; b) REAL: there are 110,000 images crawled by using 10 keywords including Banana, Bowl, Bread, Crab, Elephant, Frog, House, Pig, Rabbit, and Snail. For VFL, we used ten public tabular datasets. Details of these datasets are presented in Table I. For each dataset, we first randomly extracted 10% of the training data as the validation dataset, and distributed the remaining training data to the participants.

TABLE I Datasets. 

<table><tr><td>Task</td><td>Dataset</td><td>Size</td><td>Description</td></tr><tr><td rowspan="4">HFL</td><td> $\mathcal{D}_{M}$ </td><td>70,000</td><td>MNIST [42]</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>60,000</td><td>CIFAR10 [43]</td></tr><tr><td> $\mathcal{D}_{O}$ </td><td>11,000</td><td>MOTOR [16]</td></tr><tr><td> $\mathcal{D}_{R}$ </td><td>110,000</td><td>REAL [16]</td></tr><tr><td rowspan="10">VFL</td><td> $\mathcal{D}_{B}$ </td><td>506*14</td><td>Boston house-prices [29]</td></tr><tr><td> $\mathcal{D}_{D}$ </td><td>442*11</td><td>Diabetes [29]</td></tr><tr><td> $\mathcal{D}_{Wq}$ </td><td>4898*12</td><td>Wine quality [29]</td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>17379*15</td><td>Seoul bike sharing Demand [29]</td></tr><tr><td> $\mathcal{D}_{Ca}$ </td><td>20641*9</td><td>California house-prices [44]</td></tr><tr><td> $\mathcal{D}_{I}$ </td><td>150*5</td><td>Iris dataset [29]</td></tr><tr><td> $\mathcal{D}_{W}$ </td><td>173*14</td><td>Wine dataset [29]</td></tr><tr><td> $\mathcal{D}_{Bc}$ </td><td>569*31</td><td>Breast cancer dataset [29]</td></tr><tr><td> $\mathcal{D}_{Cc}$ </td><td>30000*23</td><td>Default of credit card clients [29]</td></tr><tr><td> $\mathcal{D}_{A}$ </td><td>48842*15</td><td>Adult dataset [29]</td></tr></table>

2) Deep learning models: For HFL, we implemented the typical federated optimization algorithm FedSGD [4] and four popular deep learning models, namely HFL-CNN-MNIST, HFL-CNN-CIFAR, HFL-CNN-MOTOR and HFL-CNN-REAL for image classification. For VFL, we implemented two models, namely a vertical linear regression model VFL-LinReg [3] and a vertical logistical regression model VFL-LogReg [3].   
3) Metrics: We test our framework DIG-FL from two aspects: accuracy and cost. The accuracy is quantified by Pearson’s Correlation Coefficient (PCC) between the estimated Shapley value of DIG-FL and actual Shapley value. The cost includes computation cost and communication cost. Computation cost is quantified by the time(s) that algorithm runs and

communication cost is quantified by the amount of data(MB) that the server interacts with the participants.

# B. Error of Ignoring the Second Term

In Sec.II-E, we propose to ignore the second term α∇lossv(θ)Ω when calculating the contribution to save resources. Then we test the error of ignoring the second term on 14 datasets for HFL and VFL.

![](images/0a068aa68fc3434b3af43814a82c2249205d518bd1e20465712042288f68a625.jpg)



(a) per-epoch contribution for HFL.

![](images/747493d0a3a29f6dd33988bce70566015729bef76ac2c92376d0ae771c75330c.jpg)



(b) per-epoch contribution for VFL.   
Fig. 2. φ is the whole contirbution, while $\hat { \phi }$ is the contribution ignoring the second term.

TABLE II The error of ignoring the second term. 

<table><tr><td>Model</td><td>Dataset</td><td> $\phi$ </td><td> $\hat{\phi}$ </td><td> $|\frac{\phi-\hat{\phi}}{\phi}|$ </td></tr><tr><td>HFL-CNN-MNIST</td><td> $\mathcal{D}_{M}$ </td><td>2.771</td><td>2.786</td><td>0.54%</td></tr><tr><td>HFL-CNN-CIFAR</td><td> $\mathcal{D}_{C}$ </td><td>7.094</td><td>7.306</td><td>2.98%</td></tr><tr><td>HFL-CNN-MOTOR</td><td> $\mathcal{D}_{O}$ </td><td>5.81</td><td>6.09</td><td>4.82%</td></tr><tr><td>HFL-CNN-REAL</td><td> $\mathcal{D}_{R}$ </td><td>3.709</td><td>3.888</td><td>4.82%</td></tr><tr><td rowspan="5">VFL-LinReg</td><td> $\mathcal{D}_{B}$ </td><td>0.367</td><td>0.376</td><td>2.45%</td></tr><tr><td> $\mathcal{D}_{D}$ </td><td>0.250</td><td>0.255</td><td>2.00%</td></tr><tr><td> $\mathcal{D}_{Wq}$ </td><td>0.195</td><td>0.196</td><td>0.51%</td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>0.459</td><td>0.477</td><td>3.92%</td></tr><tr><td> $\mathcal{D}_{Ca}$ </td><td>0.262</td><td>0.261</td><td>0.38%</td></tr><tr><td rowspan="5">VFL-LogReg</td><td> $\mathcal{D}_{I}$ </td><td>0.343</td><td>0.347</td><td>1.16%</td></tr><tr><td> $\mathcal{D}_{W}$ </td><td>0.104</td><td>0.109</td><td>4.81%</td></tr><tr><td> $\mathcal{D}_{Bc}$ </td><td>0.0649</td><td>0.0665</td><td>2.47%</td></tr><tr><td> $\mathcal{D}_{Cc}$ </td><td>0.0498</td><td>0.0475</td><td>4.62%</td></tr><tr><td> $\mathcal{D}_{A}$ </td><td>0.194</td><td>0.195</td><td>0.52%</td></tr></table>

Fig. 2 and Table II show that, for HFL and VFL, the error caused by ignoring the second term is within 5%, which is acceptable.

# C. DIG-FL v.s. Actual Shapley Value

We compare the Shapley value estimated by DIG-FL with the actual Shapley value. The actual Shapley value is computed by performing 2n retraining (n is the number of participants) and using Eq.(2) as the utility function.

1) For HFL: On the four public datasets MNIST, CIFAR10, MOTOR, REAL, we generated two typical types of lowcontribution participants: 1) participant holds mislabeled data; 2) participant holds nonIID data. We set m as the number of low-contribution participants. With mislabeled data, we first evenly distributed $\mathcal { D } _ { M } \mathrm { ~ ( ~ } \mathcal { D } _ { C } , \mathcal { D } _ { O }$ and $\mathcal { D } _ { R } )$ to n participants, and then for m out of n participants, we replaced the labels of 50% (or 30%) of their training samples with random incorrect labels from the same dataset. With nonIID data, we divided images into shards of different categories. We evenly assigned shards from all categories (i.e., IID data) to n−m participants, and for the rest m participants we randomly assigned them incomplete categories of shards (i.e., non-IID data with only 1 to 9 categories out of 10 categories). For $\mathcal { D } _ { M } , n = 1 0$ and m varied from 0 to 9; for $\mathcal { D } _ { C } , \mathcal { D } _ { O }$ and $\mathcal { D } _ { R } , n = 5$ and m varied from 0 to 4.

![](images/7e01eba9db8711676101097b0b0957e394c9bea5c5d2cbb2b8ed87800a670d09.jpg)



(a) HFL-CNN-CIFAR

![](images/49de162ca88e33670af10c10f4769570de2b5dc4b194c78e451ddfe5db0c15cc.jpg)



(b) HFL-CNN-MOTOR

![](images/a74e34a41aba30186dd642b3bc8baef8a7de87ff68f91460cd65c8d44f664bee.jpg)



(c) Computation cost

![](images/e80a7f428033e41ff67a8cdc866b02a44f1d2a7fe6fe38e72f898af1e682b24a.jpg)



(d) Communication cost

Fig. 3. Accuracy and cost of estimating Shapley values by DIG-FL and computing actual Shapley value for HFL.   
![](images/c6eb8c906d3b64cec75c163ce47bfddc6d4021e2d88f2f844bc1ba9ee9a5df42.jpg)



(a) HFL-CNN-CIFAR

![](images/447b63e020d1855a665e3668fb5f696c06608699f1233fe91d0f3785ba3febde.jpg)



(b) HFL-CNN-MOTOR

![](images/d33e049f44cf4b7d5135960371ed502f42b755dc96e1c52539fb4a0cf2d05ebb.jpg)



(c) Computation cost

![](images/406ef752f2e75403029dc3bf57f64327a4fa137afa1f23ab6e191a42e96f4613.jpg)



(d) Communication cost   
Fig. 4. DIG-FL v.s. TMC-shapley, GT-shapley, MR and IM in HFL.

![](images/de73149e742b150459d49297f44cbc455a5987998cee106cbdf42d2610e4cefb.jpg)



(a) VFL-LinReg

![](images/6d62f556d85d28a535178882c5168c8586f4d54c3ba1ad04a643e32f2e22d741.jpg)



(b) VFL-LogReg

![](images/462ad6f52891943d7be679ca4e18d185b0b288edd1285592df13246bca1532fb.jpg)



(c) Computation cost

![](images/0ccdd5c84dc6aab39c987834f6804b63d5d3624af7d91ddc9b64bac10fa7bf83.jpg)



(d) Communication cost   
Fig. 5. DIG-FL v.s. TMC-shapley and GT-shapley in VFL.

Fig. 3 (a) and (b) depict the Shapley values estimated by DIG-FL and the corresponding actual values of all participants in all cases (with different m). The results show that the estimated Shapley values are very close to the actual values, with 0.968 Pearson’s Correlation Coefficient (PCC) on MNIST, 0.935 PCC on CIFAR10, 0.952 PCC on MOTOR and 0.833 PCC on REAL. Participants with high-quality (errorfree and IID) data have obviously greater Shapley values than participants with mislabeled or nonIID data.

More importantly, Fig. 3 (c) and (d) show that DIG-FL dramatically saves computation cost by orders of magnitude, e.g., from $8 . 9 \times 1 0 ^ { 5 }$ to $1 . 1 \times 1 0 ^ { 3 }$ on MNIST, and does not cause any communication overhead. Therefore, DIG-FL can accurately and highly efficiently estimate the Shapley value.

2) For VFL: The detailed experiment settings and results are presented in Table III. The results show that the Shapley values estimated by DIG-FL and the actual Shapley values are very close, achieving 0.987 average PCC for VFL-LinReg and 0.940 average PCC for VFL-LogReg. Moreover, compared with computing the actual Shapley values, DIG-FL dramatically reduces the time cost by orders of magnitude in all cases. For example, DIG-FL reduced the time cost from 76,584.7 to 13.77 seconds on $\mathcal { D } _ { S }$ , while the PCC is 0.998.

# TABLE III

Settings and performance of DIG-FL for VFL. n is the number of participants, and PCC is between the estimated Shapley value and the actual value. $T _ { D I G - F L } ( s )$ and $T _ { A c t u a l } ( s )$ are time cost of DIG-FL and calculating the actual Shapley value, respectively.

<table><tr><td>Model</td><td>Dataset</td><td>n</td><td>PCC</td><td> $T_{DIG-FL}$ </td><td> $T_{Actual}$ </td></tr><tr><td rowspan="5">VFL-LinReg</td><td> $\mathcal{D}_B$ </td><td>13</td><td>0.978</td><td>1.09</td><td>3802.73</td></tr><tr><td> $\mathcal{D}_D$ </td><td>10</td><td>0.986</td><td>1.032</td><td>462.66</td></tr><tr><td> $\mathcal{D}_{Wq}$ </td><td>11</td><td>0.987</td><td>1.68</td><td>1279.1</td></tr><tr><td> $\mathcal{D}_S$ </td><td>14</td><td>0.998</td><td>13.77</td><td>76584.7</td></tr><tr><td> $\mathcal{D}_{Ca}$ </td><td>8</td><td>0.984</td><td>7.02</td><td>643.05</td></tr><tr><td rowspan="5">VFL-LogReg</td><td> $\mathcal{D}_I$ </td><td>4</td><td>0.981</td><td>0.132</td><td>1.23</td></tr><tr><td> $\mathcal{D}_W$ </td><td>13</td><td>0.941</td><td>1.482</td><td>3485.81</td></tr><tr><td> $\mathcal{D}_{Bc}$ </td><td>15</td><td>0.954</td><td>3.93</td><td>21120.25</td></tr><tr><td> $\mathcal{D}_{Cc}$ </td><td>11</td><td>0.921</td><td>60.73</td><td>44406.34</td></tr><tr><td> $\mathcal{D}_A$ </td><td>14</td><td>0.901</td><td>20.07</td><td>120028.81</td></tr></table>

3) DIG-FL v.s. Actual Shapley Value for each epoch: The above subsections compare the estimated and actual Shapley values for the entire training process. Here, we further investigate them for each epoch. For HFL, in each epoch, we use model performance improvement caused by the gradient sent by each participant to the server as the utility function of the actual Shapley value. A participant leaving the FL system is equivalent to ignoring his/her uploaded gradient when the server performs aggregation. As mentioned in Sec. V-C1, we generated three typical types of participants: 1) participant holding high-quality data; 2) participant holding mislabeled data; 3) participant holding non-IID data, on four datasets MNIST, CIFAR10, MOTOR, REAL. For all datasets, we set the number of participants to 5, one of which holds non-IID data and one holds mislabeled data. During the training, once some participants leave, the rest participants and the server continuously train the model. For VFL, each participant owns some features and a part of the complete model. Once a participant leaves, the structure of the model will change, therefore the rest participants cannot continue the model training or inference. So we only present the Shapley values for each epoch in the HFL scenario. Fig. 6 depicts that, for all epochs, our estimated Shaley values are very close to the actual shaley values for three types of participants on four datasets. It also shows that participants with high-quality (error-free and IID) data have greater Shapley values than that of participants with mislabeled data, participants with non-IID data have the smallest Shapley values. In each epoch, the communication cost for calculating the actual and estimated Shapley values are the same, but the computation cost for the actual value is $2 ^ { n }$ times higher than that for our estimated value, which is similar to Fig. 3 (c).

![](images/4c1a0bdad6e237335a4143feef926c377a144f6509da366de244527f02b063f5.jpg)



(a) MNIST

![](images/358f433124452fd1934eafb4f5049975c872505c46716f2483468294f16e559f.jpg)  
(b) CIFAR

![](images/b922e0121aa7c3a718d93eeca15a0744d02019e0c44f51ee45b9b655280fa1af.jpg)



(c) MOTOR

![](images/6969df843fa571ace9e7725595d217e458617133d9843fd0fec436b7ceff3c84.jpg)



(d) REAL   
Fig. 6. DIG-FL v.s. Actual Shapley Value for each epoch. Lines with dots are for the actual Shapley values. Lines with stars are for the estimated Shapley values. The colors indicate types of participants. Red, yellow and green mean participants holding high-quality, mislabelled and non-IID data, respectively.

# D. Comparison with Benchmark Methods

For centralized learning, there exists two state-of-the-art methods for calculating the Shapley value: (1) Truncated Monte Carlo Shapley (TMC-shapley) [20]; (2) GT-shapley [21]. which proposes a repertoire of efficient algorithms for approximating the Shapley value. We apply these methods to HFL and VFL. Adopting the same settings in their work, we set the rounds of retraining for TMC-shapley to $n ^ { 2 }$ log n and GT-shapley to $n ( \log n ) ^ { 2 } $ , where n is the number of participants. For HFL, Song et al. [23] propose the method Multi-Rounds Reconstruction based Algorithm (MR). Zhang et al. [18] use the local model update projected onto the finally global model to measure contribution(IM). For VFL, to the best of our knowledge, no method can be applied to various horizontal federated learning frameworks to measure contributions. Therefore, we compare DIG-FL with four methods for calculating the Shapley value in HFL and two methods in VFL. The datasets and models are the same as in Sec. V-C.

1) Comparison with benchmark methods in HFL: we compare DIG-FL with four methods: TMC-shapley, GT-shapley, MR and IM for calculating the Shapley value.

Fig. 4 (a) and (b), and Table IV show that DIG-FL achieves better estimation accuracy, and the average PCC between estimated Shapley values and the actual Shapley values is 0.922 for DIG-FL, 0.860 for TMC-shapley, 0.826 for GTshapley and 0.832 for MR. Fig. 4 (c) and (d) show that DIG-FL

TABLE IV PCC between Shapley values estimate by different methods and the actual Shapley values in HFL. 

<table><tr><td>Datasets</td><td>DIG-FL</td><td>TMC-shapley</td><td>GT-shapley</td><td>MR</td><td>IM</td></tr><tr><td>MNIST</td><td>0.968</td><td>0.917</td><td>0.865</td><td>0.912</td><td>0.681</td></tr><tr><td>CIFAR</td><td>0.935</td><td>0.903</td><td>0.874</td><td>0.776</td><td>0.673</td></tr><tr><td>MOTOR</td><td>0.852</td><td>0.816</td><td>0.753</td><td>0.778</td><td>0.319</td></tr><tr><td>REAL</td><td>0.833</td><td>0.802</td><td>0.822</td><td>0.857</td><td>0.213</td></tr></table>

dramatically saves computation cost by orders of magnitude, and does not cause any communication overhead.

2) Comparison with benchmark methods in VFL: we compare DIG-FL with two methods: TMC-shapley, GT-shapley for calculating the Shapley value.

TABLE V PCC between Shapley values estimate by different methods and the actual Shapley values in VFL. 

<table><tr><td>Model</td><td>Dataset</td><td>DIG-FL</td><td>TMC-shapley</td><td>GT-shapley</td></tr><tr><td rowspan="5">VFL-LinReg</td><td> $\mathcal{D}_{B}$ </td><td>0.978</td><td>0.994</td><td>0.912</td></tr><tr><td> $\mathcal{D}_{D}$ </td><td>0.986</td><td>0.987</td><td>0.936</td></tr><tr><td> $\mathcal{D}_{Wq}$ </td><td>0.987</td><td>0.994</td><td>0.971</td></tr><tr><td> $\mathcal{D}_{S}$ </td><td>0.994</td><td>0.996</td><td>0.974</td></tr><tr><td> $\mathcal{D}_{Ca}$ </td><td>0.983</td><td>0.995</td><td>0.983</td></tr><tr><td rowspan="5">VFL-LogReg</td><td> $\mathcal{D}_{I}$ </td><td>0.981</td><td>0.987</td><td>0.986</td></tr><tr><td> $\mathcal{D}_{W}$ </td><td>0.941</td><td>0.873</td><td>0.862</td></tr><tr><td> $\mathcal{D}_{Bc}$ </td><td>0.954</td><td>0.892</td><td>0.853</td></tr><tr><td> $\mathcal{D}_{Cc}$ </td><td>0.921</td><td>0.958</td><td>0.863</td></tr><tr><td> $\mathcal{D}_{A}$ </td><td>0.901</td><td>0.896</td><td>0.829</td></tr></table>

Fig. 5 (a) and (b) show that DIG-FL achieves better estimation accuracy. Table V shows PCC between estimated Shapley values and the actual Shapley value on 10 datasets , and the average is 0.963 for DIG-FL, 0.957 for TMC-shapley and 0.917 for GT-shapley. Fig. 5 (c) and (d) illustrate that DIG-FL significantly outperforms two existing methods in both computation and communication costs, reducing cost by orders of magnitude.

# E. Effect of Reweight Mechanism

When all participants hold high-quality data, the global model converges well. In this case, it is unnecessary to reweight participants. To evaluate the effect of DIG-FL based reweight mechanism, as aforementioned in Sec. V-C, we consider two settings: 1)Non-IID setting: we use two datasets MNIST and CIFAR10 and let some participants hold non-IID data. 2)Mislabeled setting: we use two datasets MOTOR and REAL and let some participants hold mislabeled data. We use the classic federated optimization algorithm FedSGD [4] as a baseline.

![](images/aec961a31021bef8bd96457d93a29a8cc513245d9b86dcfb21abbe7aebe9aca2.jpg)



(a) TestACC of CIFAR

![](images/654f7246b0201f89aa6d49aade7ec144ac45c893ad815dd0fe98aa56de4f3573.jpg)



(b) Loss of CIFAR

![](images/21a90883eaf8580b9cee1c2ea6b250053aa99433e07f948af856280414ed57bb.jpg)



(c) TestAcc of MOTOR

![](images/a04bd1d9bd4a4d99d82597cb92300a722fe195c9c2c986ade3667deac628ea26.jpg)



(d) Loss of MOTOR   
Fig. 7. The effect of reweight mechanism on model convergence.

Due to space limitations, here we only present the results of two datasets CIFAR10 and MOTOR, which are similar to the results on MNIST and REAL, respectively. Fig. 7 (a) and (c) show that, without reweight, the performance of the global model severely deteriorates as the proportion of participants holding non-IID or mislabeled data increases. DIG-FL based reweight mechanism can significantly mitigate the negative impact of low-quality participants, so as to obviously improve the test accuracy and boosts the model convergence. For example, on CIFAR10, when four out of five participants have non-IID data, our reweight mechanism raises the test accuracy from 70.9% to 89.9%. on MOTOR, when four out of five participants have mislabeled data, the reweight mechanism raises the test accuracy from 55.2% to 86.5%. As shown in Figs. 7 (b) and (d), the reweight mechanism also obliviously boosts and stabilizes the model convergence.

# VI. RELATED WORK AND PRELIMINARIES

# A. Impact based on Influence Function

Influence function is a classic technique from robust statistics [13], which tells us how the model parameters change by upweighting a training point by an infinitesimal amount. In centralized deep learning, a collection of works use influence functions to interpret model behaviors and trace predictions back to the training data [12], [13]. Some methods proceed to assign importance weights to training samples so as to improve the performance of deep learning models [45], [14], [46]. Those methods are designed for centralized learning and cannot be adopted by FL due to two main reasons: first, they require access to the training data, while the local data in FL is invisible; second, influence functions require expensive second derivative calculations for each data point, which is unaffordable for many FL systems.

Recently, Xue et al. [15] and Li et al. [16] use influence function to understand the influence of individual participants in HFL, which still needs participants to calculate and upload their Hessian matrices or part of Hessian matrices. Applying these methods to calculate contribution requires exponentially calculation of influence function, thus resulting in large extra computation and communication overhead. Moreover, all those influence function based methods are only applicable to HFL, not to VFL.

# B. Contribution based on Shapley Value

Shapley Value [19] distributes cooperation benefits fairly by considering the contributions of each participant. It defines a unique distribution among the participants of the total surplus generated by the coalition and has many appealing properties, such as fairness, rationality, symmetry, and linearity.

In the machine learning area, the most recent work focus on reducing the cost of computing the Shapley value. Ghorbani et al.[20] propose a Shapley value based approach to quantify the contributions of training data points to a deep learning model, and design two methods to reduce computation cost, namely Truncated Monte Carlo Shapley and Gradient Shapley. Jia et al.[21] develop a repertoire of sample-based techniques for estimating the Shapley values of data points. Though those methods make efforts to improve the efficiency, they still require repeated leave-one-out model retraining to calculate the Shapley value and thus will impose prohibitively expensive computation and communication cost for FL systems.

There are few works [24], [23] using the Shapley value to measure contributions of participants for FL. For HFL, Song et al.[23] propose two methods One-Rounds Reconstruction based Algorithm(OR) and Multi-Rounds Reconstruction based Algorithm (MR). The second method calculates contributions in each training round and then aggregates them to get the final result without retraining the model. But it needs to exponentially test model performance, and thus imposes expensive computation cost. For VFL, Wang et al.[24] propose a method to measure participants’ contribution. However, it needs to access and permutate the features of all participants, which introduces extra severe privacy risk.

# VII. CONCLUSION

In this work, we propose an approach DIG-FL to measure the contribution of each participant, by estimating his/her Shapley value, for both HFL and VFL with minimal extra cost. We theoretically show that DIG-FL can accurately approximate the actual Shapley value using only training logs. In addition, we propose a DIG-FL based reweight mechanism to train more robust FL models when there is a large portion of participants possessing non-IID or mislabeled data. Our approach can be adopted to locate adversarial training data, optimal participant selection under budget constraint, or design fairer incentive/payment mechanisms for FL applications.

# VIII. ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research is supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61822209, No. 61932016, No. 62132018. This work was partially supported by Tencent Marketing Solution Rhino-Bird Focused Research Program.

# REFERENCES

[1] J. Han and Y. Liu, “Rumor riding: Anonymizing unstructured peer-topeer systems,” IEEE Transactions on Parallel and Distributed Systems, vol. 22, pp. 464–475, 2011.   
[2] L. Zhang, T. Jung, K. Liu, X. Li, X. Ding, J. Gu, and Y. Liu, “Pic: Enable large-scale privacy preserving content-based image search on cloud,” IEEE Transactions on Parallel and Distributed Systems, vol. 28, pp. 3258–3271, 2017.   
[3] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” TIST, 2019.   
[4] B. McMahan, E. Moore, and Ramage, “Communication-efficient learning of deep networks from decentralized data,” in ICML, 2017.   
[5] K. Muhammad, Q. Wang, D. O’Reilly-Morgan, E. Tragos, B. Smyth, N. Hurley, J. Geraci, and A. Lawlor, “Fedfast: Going beyond average for faster training of federated recommender systems,” in SIGKDD, 2020.   
[6] Y. Hu, D. Niu, J. Yang, and S. Zhou, “Fdml: A collaborative machine learning framework for distributed features,” in SIGKDD, 2019.   
[7] B. Gu, Z. Dang, X. Li, and H. Huang, “Federated doubly stochastic kernel learning for vertically partitioned data,” in SIGKDD, 2020.   
[8] Y. Liu, Y. Kang, X. wei Zhang, L. Li, Y. Cheng, T. Chen, M. Hong, and Q. Yang, “A communication efficient collaborative learning framework for distributed features,” arXiv:Learning, 2019.   
[9] Y. Zhao, M. Li, L. Lai, N. Suda, D. Civin, and V. Chandra, “Federated learning with non-iid data,” arXiv preprint arXiv:1806.00582, 2018.   
[10] A. Shafahi and W. R. Huang, “Poison frogs! targeted clean-label poisoning attacks on neural networks,” in NIPS, 2018.   
[11] S. Mehnaz and E. Bertino, “Privacy-preserving real-time anomaly detection using edge computing,” in IEEE ICDE, 2020, pp. 469–480.   
[12] P. W. Koh and P. Liang, “Understanding black-box predictions via influence functions,” in ICML, 2017.   
[13] R. D. Cook and S. Weisberg, Residuals and influence in regression. New York: Chapman and Hall, 1982.   
[14] M. Ren, W. Zeng, B. Yang, and R. Urtasun, “Learning to reweight examples for robust deep learning,” in ICML, 2018.   
[15] Y. Xue, C. Niu, Z. Zheng, S. Tang, C. Lv, F. Wu, and G. Chen, “Toward understanding the influence of individual clients in federated learning,” in AAAI, 2021.   
[16] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” ICDE, 2021.   
[17] J. W. F. H. X.-Y. L. Anran Li, Lan Zhang, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, 2021.   
[18] J. Zhang, Y. Wu, and R. Pan, “Incentive mechanism for horizontal federated learning based on reputation and reverse auction,” Proceedings of the Web Conference 2021, 2021.   
[19] L. S. Shapley, “A value for n-person games,” 1988.   
[20] A. Ghorbani and J. Zou, “Data shapley: Equitable valuation of data for machine learning,” in ICML, 2019.   
[21] R. Jia, D. Dao, B. Wang, F. A. Hubis, N. Hynes, N. M. Gurel, B. Li, ¨ C. Zhang, D. Song, and C. Spanos, “Towards efficient data valuation based on the shapley value,” in AISTATS, 2019.   
[22] S. Wang, “When edge meets learning: Adaptive control for resourceconstrained distributed machine learning,” in INFOCOM, 2018.   
[23] T. Song, Y. Tong, and S. Wei, “Profit allocation for federated learning,” in Big Data, 2019.   
[24] G. Wang, C. X. Dang, and Z. Zhou, “Measure contribution of participants in federated learning,” in Big Data, 2019.   
[25] L. Zhang, X. Li, K. Liu, C. Liu, X. Ding, and Y. Liu, “Cloak of invisibility: Privacy-friendly photo capturing and sharing system,” IEEE Transactions on Mobile Computing, vol. 18, pp. 2488–2501, 2019.   
[26] L. Zhang, X. Li, K. Liu, T. Jung, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in mobile social networks,” IEEE Transactions on Mobile Computing, vol. 14, pp. 1888–1902, 2015.   
[27] L. Zhang, X. Li, Y. Liu, and T. Jung, “Verifiable private multi-party computation: Ranging and ranking,” 2013 Proceedings IEEE INFOCOM, pp. 605–609, 2013.   
[28] W. A. Department, “Federated ai technology enabler,” Website, 2020, https://github.com/FederatedAI/FATE.   
[29] D. Dua and C. Graff, “UCI machine learning repository,” 2017. [Online]. Available: http://archive.ics.uci.edu/ml   
[30] V. Mothukuri, R. M. Parizi, S. Pouriyeh, Y. ping Huang, A. Dehghantanha, and G. Srivastava, “A survey on security and privacy of federated learning,” Future Gener. Comput. Syst., vol. 115, pp. 619–640, 2021.

[31] L. T. Phong, Y. Aono, T. Hayashi, L. Wang, and S. Moriai, “Privacypreserving deep learning via additively homomorphic encryption,” IEEE Transactions on Information Forensics and Security, vol. 13, pp. 1333– 1345, 2018.   
[32] R. Shokri and V. Shmatikov, “Privacy-preserving deep learning,” Allerton, pp. 909–910, 2015.   
[33] K. Bonawitz, V. Ivanov, B. Kreuter, A. Marcedone, H. B. McMahan, S. Patel, D. Ramage, A. Segal, and K. Seth, “Practical secure aggregation for privacy-preserving machine learning,” in CCS, 2017, pp. 1175–1191.   
[34] S. Hardy, W. Henecka, H. Ivey-Law, R. Nock, G. Patrini, G. Smith, and B. Thorne, “Private federated learning on vertically partitioned data via entity resolution and additively homomorphic encryption,” ArXiv, vol. abs/1711.10677, 2017.   
[35] B. A. Pearlmutter, “Fast exact multiplication by the hessian,” in Neural computation, 1994, pp. 147–160.   
[36] N. Agarwal, B. Bullins, and E. Hazan, “Second-order stochastic optimization in linear time,” stat, vol. 1050, p. 15, 2016.   
[37] L. Zhu, Z. Liu, and S. Han, “Deep leakage from gradients,” in Advances in Neural Information Processing Systems, 2019, pp. 14 747–14 756.   
[38] B. Hitaj, G. Ateniese, and F. Perez-Cruz, “Deep models under the gan: ´ Information leakage from collaborative deep learning,” Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, 2017.   
[39] L. Zhu, Z. Liu, and S. Han, “Deep leakage from gradients,” in NeurIPS, 2019.   
[40] W. Du, Y. S. Han, and S. Chen, “Privacy-preserving multivariate statistical analysis: Linear regression and classification,” in SDM, 2004.   
[41] G. Si-yang, “Privacy preserving association rule mining in vertically partitioned data,” Journal of Computer Applications, 2006.   
[42] Y. LeCun, “The mnist database,” http://yann.lecun.com/exdb/mnist/.   
[43] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” Citeseer, Tech. Rep., 2009.   
[44] Kaggle, https://www.kaggle.com/datasets.   
[45] P. Zhao and T. Zhang, “Stochastic optimization with importance sampling for regularized loss minimization,” in ICML, 2015.   
[46] A. Vahdat, “Toward robustness against label noise in training deep discriminative neural networks,” in NIPS, 2017.