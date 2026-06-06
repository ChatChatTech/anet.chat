# FedFAIM: A Model Performance-based Fair Incentive Mechanism for Federated Learning

Zhuan Shi, Lan Zhang, Member, IEEE, Zhenyu Yao, Lingjuan Lyu, Cen Chen, Li Wang, Junhao Wang, Xiang-Yang Li, Fellow, IEEE

Abstract—Federated Learning (FL) has emerged as a privacy-preserving distributed machine learning paradigm. To motivate data owners to contribute towards FL, research on FL incentive mechanisms is gaining great interest. Existing monetary incentive mechanisms generally share the same FL model with all participants regardless of their contributions. Such an assumption can be unfair towards participants who contributed more and promote undesirable free-riding, especially when the final model is of great utility value to participants. In this paper, we propose a Fairness-Aware Incentive Mechanism for federated learning (FedFAIM) to address such problem. It satisfies two types of fairness notion: 1) aggregation fairness, which determines aggregation results according to data quality; 2) reward fairness, which assigns each participant a unique model with performance reflecting his contribution. Aggregation fairness is achieved through efficient gradient aggregation which examines local gradient quality and aggregates them based on data quality. Reward fairness is achieved through an efficient Shapley value-based contribution assessment method and a novel reward allocation method based on reputation and distribution of local and global gradients. We further prove reward fairness is theoretically guaranteed. Extensive experiments show that FedFAIM provides stronger incentives than similar non-monetary FL incentive mechanisms while achieving a high level of fairness.

Index Terms—Federated Learning, Incentive Mechanism, Fairness.

# 1 INTRODUCTION

As computing applications become increasingly intertwined with our daily life, a gigantic amount of data are continuously generated which provides opportunities for learning-based intelligent services to emerge. To take advantage of these data through traditional machine learning, data from diverse users need to be consolidated into a centralized facility for training, incurring high computation and storage overhead and privacy risks. As societies become more aware of the necessity for data privacy protection, emerging laws such as the General Data Protection Regulation (GDPR) [1] explicitly specifies data to be stored where they are generated, leading to segregated data silos. To address these problems, federated learning (FL) [2], a privacy-preserving distributed machine learning paradigm, has been proposed and is rapidly gaining great interest. Many federated platforms have been developed and open-sourced (e.g., TensorFlow Federated (TFF) from Google and FATE from WeBank). Moreover, industries such as finance, insurance, telecommunications, healthcare, education, and urban computing are at the leading edge of adopting and benefiting from FL on a large scale.

Existing research on FL generally assumes that data owners are innately willing to participate in FL process and contribute their data honestly [3]–[6]. In practice, without properly designed incentives, data owners may be reluctant to participate, as participating in FL incurs both high computation/communication costs and potential privacy risks [7]–[9]. Moreover, data owners are autonomous agents, who can determine when, where and how to participate in FL. Faced with different compensation schemes from different federations, participants may adopt disparate training strategies, affecting the performance of FL models. Thus, it is important to design an effective incentive mechanism to encourage data owners to actively participate in FL.

These considerations have inspired research on FL incentive mechanism design, which can be divided into two major steps:

1) Contribution Assessment: In order to allocate proper incentives to participants, their contributions to the final model are usually evaluated first. Shapley value as a classic solution to evaluate contribution in cooperative game theory [10], [11] has been adopted by FL. However, it incurs exponential estimation overhead when training model on combinations of different participants. Several recent approaches [12]–[14] have been proposed to improve the efficiency of Shapley value estimation. Other alternative contribution evaluation methods are based on the similarity between parameters of local and global models [15], [16].   
2) Reward Allocation: Once participants’ contributions have been measured, a reward allocation scheme is adopted to distribute the incentive budget among them. Recent works leveraged game theory to design reward schemes for FL. In [17], a Stackelberg game was proposed to optimize the computational resource allocation among the participants and the budget allocation for rewarding them. In [15], a reward

scheme based on reputation and reverse auction theory was proposed in the federated setting, where the server selects and rewards participants by jointly considering their reputation and bids under a limited budget.

Existing incentive mechanisms for FL focus on motivating data owners through monetary rewards, which is mostly separate from the federated training process. By adopting existing FL model training approaches (e.g., FedAvg), all participants receive the same final FL model, regardless of their contributions. This disconnection between monetary rewards and the receipt of the final model can render the incentive schemes ineffectively, especially in case when the final global model is of significantly higher value compared to the monetary incentive budget. For example, several banks may want to collaboratively build a credit score predictor for small and medium enterprises. The performance of the final model may affect each bank’s market share, which could be worth billions. In such a situation, larger banks with more quality data may be reluctant to collaborate with small banks for fear of market share erosion. This dilemmic situation was defined as the FL free-rider problem [16], [18], which have started to explore allocating FL models with performance reflecting participants’ contributions to achieve collaborative fairness. Nevertheless, these works did not consider collaborative fairness during model aggregation. Moreover, their reward allocation schemes only consider the distribution of the global gradients while ignore the distribution of local gradients. These deficiencies make the allocated models difficult to accurately reflect the contribution of participants. There is still a lack of a non-monetary FL incentive mechanism that takes full account of fairness during the whole training process and can achieve a good tradeoff between model performance and fairness.

To address above issues and deliver incentives to FL participants via models with differentiating performance, we need to tackle the following three challenges:

1) Model updates from participants might be of erratic quality [19]. Due to the limited computation and communication resources, local models might be of low quality, which will negatively affect the aggregated model. Moreover, some participants might be free-riders who aim to benefit from the global model without really contributing, such as uploading randomly generated gradients at virtually cost. In addition, there might be malicious participants conducting poisoning attacks to influence the global model parameters leading to the failure of existing collaborative learning mechanism in [16], [18]. Thus it is imperative to filter out low-quality local gradients.

2) To determine the intermediate reward at each training round, participants’ contributions must be evaluated in real-time. However, existing methods, which are often based on the Shapley value due to its rationality and fairness properties, cannot satisfy such run-time requirement.

3) Achieving collaborative fairness in FL via contribution-based gradient allocation is fundamentally different from allocating monetary incentives. The key challenge here is to determine the allocated gradients for each participant while jointly considering his contribution, as well as the distribution of the local gradients and the global gradients at each round. Such allocation should not only accurately reflect the contribution of participants, but also achieve a good tradeoff between model performance and fairness.

To this end, we propose a Fairness-Aware Incentive Mech-

anism for federated learning (FedFAIM) to tackle the abovementioned challenges. It aims to provide stronger incentives for data owners who might be competitors to collaboratively train FL models by making the performance of allocated models more accurately reflect participants’ contributions. To this end, we first consider aggregation fairness, which weights the participants’ updates according to their data quality, thus making the global model more fairly reflective of contributions; furthermore, we consider reward fairness, which assigns models to participants based on their reputation as well as distribution of their local and global gradients.

1) FedFAIM consists of a novel gradients aggregation method which first conducts quality detection to filter out low-quality local gradients based on marginal loss measure, and then aggregates the local gradients by considering the quality of their model updates.   
2) FedFAIM further introduces a contribution measure based on the Shapley value, which takes the closeness between the local and the global gradients as the utility function. It measures per-round contributions which can be used to compute the intermediate rewards. We show that the method can be computed in linear time.   
3) The reward allocation mechanism of FedFAIM incorporates reputation (computed from the quality detection result and contribution measure) to determine the performance level of the model to be assigned for each participant. It then selects gradients with the corresponding quality from the global FL model jointly by the distribution of the local gradient and the global gradient to construct the FL model to be assigned to a given participant. We further prove our reward allocation mechanism is theoretically guaranteed under some conditions.

We conduct extensive experiments to examine the efficiency and effectiveness of proposed FedFAIM against the state-of-theart baselines on real-world datasets. For gradient aggregation, Fed-FAIM improves the accuracy of aggregated models and the convergence rate. For contribution measurement, FedFAIM outperforms other baselines in terms of the Pearson correlation coefficient with the actual Shapley values. Moreover, FedFAIM consumes the least computation time among all comparisons. For reward allocation, FedFAIM provides stronger incentives than other non-monetary incentive mechanism baselines, i.e., CFFL [18] and RFFL [16], while achieving a comparable level of fairness. To the best of our knowledge, FedFAIM is the first non-monetary incentive mechanism proposed for federated setting, which simultaneously achieves aggregation fairness and reward fairness. It is a promising approach to enable data owners who might be competitors to be properly motivated to collaboratively build models through federated learning.

# 2 PRELIMINARIES

# 2.1 Problem Description

We consider Horizontal Federated Learning (HFL) scenarios, in which the FL system consists of two main parties: participants (i.e. data owners) and the FL server. We denote the set of $N$ participants as $W = \{ 1 , 2 , . . . , N \}$ , and the private dataset belonging to participant i as $D _ { i }$ . In FL systems, models are trained across multiple rounds. In each training iteration t, instead of directly downloading the global model from the server as in conventional

TABLE 1: Notations 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $W$ </td><td>The set of participants</td></tr><tr><td> $N$ </td><td>The number of participants</td></tr><tr><td> $D_{i}$ </td><td>The local dataset of participant  $i$ </td></tr><tr><td> $u_{i}^{(t)}$ </td><td>The local gradient update from participant  $i$  at round  $t$ </td></tr><tr><td> $||u_{i}^{(t)}||$ </td><td>The vector length of  $u_{i}^{(t)}$ </td></tr><tr><td> $u_{G}^{(t)}$ </td><td>The global gradient at round  $t$ </td></tr><tr><td> $|u_{G}^{(t)}|$ </td><td>The set cardinality of  $u_{G}^{(t)}$ </td></tr><tr><td> $\mathcal{M}_{i}^{(t)}$ </td><td>The local model of participant  $i$  at round  $t$ </td></tr><tr><td> $\mathcal{M}_{G}^{(t)}$ </td><td>The global model at round  $t$ </td></tr><tr><td> $\mathcal{M}_{-i}^{(t)}$ </td><td>The global aggregated model at round  $t$  involving all but participant  $i$ </td></tr><tr><td> $\delta_{i}^{(t)}$ </td><td>The marginal loss of participant  $i$  at round  $t$ </td></tr><tr><td> $\delta$ </td><td>The loss threshold</td></tr><tr><td> $\Delta_{i}^{(t)}$ </td><td>The closeness between model parameter  $\mathcal{M}_{i}^{(t)}$  of participant  $i$  and the global model  $\mathcal{M}_{G}^{(t)}$  at round  $t$ .</td></tr><tr><td> $\gamma$ </td><td>The controlled parameter of the exponential function</td></tr><tr><td> $Q^{(t)}$ </td><td>The set of participants who passed quality detection at round  $t$ </td></tr><tr><td> $\alpha_{i}^{(t)}$ </td><td>The aggregation weight for participant  $i$  at round  $t$ </td></tr><tr><td> $\phi_{i}^{(t)}$ </td><td>The contribution of participant  $i$  in round  $t$ </td></tr><tr><td> $c_{i}^{(t)}$ </td><td>The cumulative contribution of participant  $i$  in round  $t$ </td></tr><tr><td> $z_{i}^{(t)}$ </td><td>The relative contribution of participant  $i$  in round  $t$ </td></tr><tr><td> $n_{i}^{pass}$ </td><td>The number of times  $i$  has passed quality detection so far</td></tr><tr><td> $n_{i}^{fail}$ </td><td>The number of times  $i$  has failed quality detection so far</td></tr><tr><td> $q_{i}^{(t)}$ </td><td>The impact of participant  $i$ &#x27;s quality detection results on his/her reputation at round  $t$ </td></tr><tr><td> $r_{i}^{(t)}$ </td><td>Participant  $i$ &#x27;s reputation at round  $t$ </td></tr><tr><td> $num_{i}^{(t)}$ </td><td>The number of gradients allocated to participant  $i$  at round  $t$ </td></tr><tr><td> $u_{*,i}^{(t)}$ </td><td>The allocated gradients for participant  $i$  at round  $t$ </td></tr></table>

FL systems, we modify the learning process by allocating customized aggregated gradients to each participant. Each participant i then optimizes the allocated model on its local training data and sends the local gradients $u _ { i } ^ { ( t ) }$ to the FL server. Collecting all the local updates $\{ \bar { u } _ { i } ^ { ( t ) } \} _ { i = 1 } ^ { N }$ , the server aggregates them into global gradients $u _ { G } ^ { ( t ) }$ . It then measures each participant’s contribution and allocates the customized aggregated gradient $u _ { * i } ^ { ( t ) }$ to each participant i based on the reward mechanism. This training process is repeated until the model converges. The notations used in this paper are listed in Table 1 for ease of reference. Such modification of the FL training process allows participants to obtain different models whose performance reflecting their contributions.

Based on the above modification, we aim to design a fairnessaware incentive mechanism for federated learning systems to achieve both the aggregation fairness and reward fairness defined as follows:

Definition 1 (Aggregation Fairness). In a federated learning system, a participant’s local model update shall be given an aggregation weight corresponding to the quality of the local data he/she contributes to the training process.

Definition 2 (Reward Fairness). In a federated learning system, a participant shall receive a customized version of the aggregated model with performance corresponding to his/her contribution to the final model performance.

# 2.2 System Architecture

As illustrated in Fig. 1, our proposed FedFAIM is implemented in the FL sever, which is transparent to participants, thus our design can be easily adopted by existing FL systems. A Fed-FAIM enhanced HFL system consists of three main modules: Gradient Aggregation (GA), Contribution Assessment (CA) and Reward Allocation (RA). GA includes two submodules, Quality Detection and Aggregation Weight Calculation. There are also two submodules in RA, namely Reputation Calculation and Reward Calculation. The system works as follows:

![](images/864f30b3e7214ccc724aa01b4cf9b8d18b81e950d51a9f89f26b615c7aea1aaa.jpg)



Fig. 1: The FL system architecture for FedFAIM.

Step (1): In round t, participant i receives the version of the aggregated gradients allocated to him/her by the RA module of FedFAIM from the FL server, and updates the local model.

Step (2): Each participant i updates the local gradients ui $u _ { i } ^ { ( t ) }$ using the local training data $D _ { i }$ , and uploads $u _ { i } ^ { ( t ) }$ to the server.

Step (3): On the server side, receiving the the gradients sent by all participants, the Quality Detection submodule computes the marginal loss $\delta _ { i } ^ { ( t ) }$ (see Definition 3) for each participant i, and only accepts a local gradient $u _ { i } ^ { ( t ) } \operatorname { i f } \delta _ { i } ^ { ( t ) }$ is not less than a threshold δ .

Step (4): The sever then sends the marginal loss of all the participants who have passed quality detection to the Aggregation Weight Calculation submodule. It also sends the quality detection pass/fail counts of these participants to the Reputation Calculation submodule.

Step (5): After receiving the marginal loss information, the $\mathrm { A g \mathrm { - } }$ gregation Weight Calculation submodule aggregates the selected participants’ local gradients into the global gradient their marginal loss. Then, it sends all local gradien $u _ { G } ^ { ( t ) }$ G to $u _ { G } ^ { ( t ) }$ the CA module and the Reward Calculation submodule.

Step (6): After receiving the the local gradients and the aggregated global gradient, CA assesses each participant i’s perround contribution $\mathbf { \bar { \rho } } _ { c _ { i } } ( t )$ by using the mapping distance of the local gradient $u _ { i } ^ { ( t ) }$ to the aggregated global gradient $u _ { G } ^ { ( t ) }$ as the valuation function in Shapley value calculation. Then, it send s c(t) $c _ { i } ^ { ( t ) }$ for all i to the Reputation Calculation submodule.

Step (7): After receiving the quality detection results and all participants’ contributions, the Reputation Calculation submodule computes the reputation values and sends them to the Reward Calculation submodule. The Reward Calculation submodule determines the number of allocated gradients $n u m _ { i } ^ { ( t ) }$ for each participant i and selects $n u m _ { i } ^ { ( t ) }$ gradients from $u _ { G } ^ { ( t ) }$ uG based on the distribution of $u _ { i } ^ { ( t ) }$ and the global gradient vector $\bar { u } _ { G } ^ { ( t ) }$ , so as to form the allocated aggregated gradients u(t)∗i $u _ { * i } ^ { ( t ) }$ for i. Finally, it sends $u _ { * i } ^ { ( t ) }$ u∗i to i for the next round training.

# 3 GRADIENT AGGREGATION

The Gradient Aggregation module of FedFAIM consists of two parts: quality detection, and quality-aware weighted aggregation.

# 3.1 Quality Detection

The intuitive way to filter out low quality models is to determine if the loss of a local model exceeds a given loss threshold. However, it is difficult to determine this threshold as it needs to be continuously reduced as the local model performance improves over more training iterations. To resolve this issue, we adopt the marginal loss metric as inspired by [15].

At round t, we use $\mathcal { M } _ { G } ^ { ( t ) }$ to denote the global model obtained by aggregating all participants’ local models, and $M _ { - i } ^ { ( t ) }$ to denote the global model obtained by aggregating all but i’s local models. These models are obtained by treating all participants equally as we do not know their relative local model quality at this stage:

$$
\begin{array}{l} \mathcal {M} _ {G} ^ {(t)} = \mathcal {M} _ {G} ^ {(t - 1)} + \frac {1}{N} \sum_ {j} u _ {j} ^ {(t)}, \\ \mathcal {M} _ {- i} ^ {(t)} = \mathcal {M} _ {G} ^ {(t - 1)} + \frac {1}{N - 1} \sum_ {j \in W - \{i \}} u _ {j} ^ {(t)}. \tag {1} \\ \end{array}
$$

Definition 3 (Marginal Loss). Let ${ \mathbf { } } l ^ { ( t ) }$ and $l _ { - i } ^ { ( t ) }$ denote the loss of $\mathcal { M } _ { G } ^ { ( t ) }$ ) and M(t)−i $\mathcal { M } _ { - i } ^ { ( t ) }$ on the validation set, respectively. The marginal loss of participant i is defined as:

$$
\delta_ {i} ^ {(t)} = l _ {- i} ^ {(t)} - l ^ {(t)}. \tag {2}
$$

The larger the marginal loss $\delta _ { i } ^ { ( t ) }$ , the more important i’s local update is to the global model performance in round t.

The loss of the global model is expected to be reduced when a high quality local model is being aggregated. We use δ to denote the quality threshold and accept the local model of participant i when δ(t) $\delta _ { i } ^ { ( t ) } \geq \delta$ . We evaluate the test accuracy on the aggregated model when the threshold δ varies in Section.6.4.

Finally, we use $Q ^ { ( t ) }$ to record the set of participants who passed the quality detection in round t. Further, we use $n _ { i } ^ { p a s s }$ and $n _ { i } ^ { f a i l }$ ito denote the number of times participant i passed and failed quality detection, respectively.

# 3.2 Quality-Aware Weighted Aggregation

In each round t, local gradients that pass the quality detection are used to obtain the updated global gradient. The widely adopted approach for this purpose is Federated Averaging [6], [20] with the aggregation step as follows:

$$
u _ {G} ^ {(t)} = \frac {\sum_ {i} | D _ {i} | u _ {i} ^ {(t)}}{\sum_ {i} | D _ {i} |} \tag {3}
$$

where $| D _ { i } |$ is the amount of data used by participant i to train the local model.

However, FedAvg may not work in the following settings: (1)Assume there is one client has large amount but relatively low quality of the data. According to FedAvg, this client can get a not too small weight since the amount of data is large, which is unfair for an honest client who has good quality but relatively small amount of data. (2)Assume there is some malicious clients. They can falsify the data size. According to FedAvg, these clients may directly affect the weights in model aggregation.

To overcome the drawback of FedAvg, FedFAIM aggregates the local model updates considering the data quality. We use $\overline { { m } } _ { i } ^ { ( t ) }$ to denote the data quality of participant i in round $t ,$ which is computed based on his/her marginal loss. Intuitively, local gradients with larger marginal loss values shall receive higher weights. Therefore, in each round t, we use the exponential function with controlled parameter γ to determines the data quality of each participant i as:

$$
m _ {i} ^ {(t)} = \frac {\exp (\gamma \delta_ {i} ^ {(t)})}{\sum_ {i} (e x p (\gamma \delta_ {i} ^ {(t)}))}. \tag {4}
$$

To achieve aggregation fairness, FedFAIM determines the aggregation weight $\alpha _ { i } ^ { ( \stackrel { \triangledown } { t } ) }$ for participant i in round t by considering the quality of local data from each participant i as follows:

$$
\alpha_ {i} ^ {(t)} = \frac {m _ {i} ^ {(t)}}{\sum_ {i} m _ {i} ^ {(t)}} \tag {5}
$$

Finally, FedFAIM aggregates the selected local gradients into the global model in round t as follows:

$$
u _ {G} ^ {(t)} = \sum_ {i} \alpha_ {i} ^ {(t)} u _ {i} ^ {(t)} \tag {6}
$$

The proposed gradient aggregation approach of FedFAIM is summarized in Algorithm 1.

Algorithm 1: FedFAIM Gradient Aggregation   
Input: $u_{i}^{(t)}$ , $D_{i}$ , $Q^{(t)}$ , $\delta$ , $n_{i}^{pass}$ , $n_{i}^{fail}$ Output: $u_{G}^{(t)}$ , $n_{i}^{pass}$ , $n_{i}^{fail}$ 1 Initialize $Q^{(t)} := \emptyset$ 2 Calculate $l^{(t)}$ based on $\mathcal{M}_{G}^{(t)}$ ;

3 for each participant $i \in W$ do

4 Calculate $l_{-i}^{(t)}$ based on the global model $\mathcal{M}_{-i}^{(t)}$ ;

5 Calculate $\delta_{i}^{(t)}$ according to Eq. (2);

6 if $\delta_{i}^{(t)} \geq \delta$ then

7 $Q^{(t)} := Q^{(t)} \cup \{i\}$ ;

8 $n_{i}^{pass} + +$ ;

9 else

10 $n_{i}^{fail} + +$ ;

11 end

12 end

13 for each participant $i \in Q^{(t)}$ do

14 Calculate $m_{i}^{(t)}$ according to Eq. (4);

15 Calculate $\alpha_{i}^{(t)}$ according to Eq. (5);

16 end

17 Obtain $u_{G}^{(t)}$ according to Eq. (6);

18 return $u_{G}^{(t)}$ , $n_{i}^{pass}$ , $n_{i}^{fail}$

# 4 CONTRIBUTION ASSESSMENT

Different from the existing methods which measure the contribution of each participant after all the training rounds end, we propose a Shapley value-based contribution evaluation method which can assess per-round contribution by each participant with linear time complexity.

Definition 4 (Shapley Value). Given a coalitional game $( V , N )$ , where N is a set of N participants and $V ( \cdot )$ is a valuation function defined as $V : 2 ^ { N } \to \mathbb { R } ,$ the Shapley value of participant i is:

$$
\phi_ {i} = \frac {1}{N} \sum_ {S \subseteq \mathcal {N} \setminus \{i \}} \frac {V (S \cup \{i \}) - V (S)}{\binom {N - 1} {| S |}}. \tag {7}
$$

As we consider the gradient-based federated learning, $V ( S )$ is the valuation function of the gradients. From the perspective of statistical learning, an ideal valuation function of the gradients is their expected performance over the true data distribution. However, this is intractable in practice. A common empirical estimator is the performance on an auxiliary dataset.

As FedFAIM has filtered out potentially low quality gradients through quality detection, all the selected local gradients are expected to be valuable. The aggregated gradients involving all selected local gradients, uN , is expected to have the highest value. Therefore, we can leverage the cosine similarity between the local gradients and uN to approximate their valuation functions:

$$
V (i) = \left| \left| \boldsymbol {u} _ {i} ^ {(t)} \right| \right| \cos \left(\boldsymbol {u} _ {i} ^ {(t)}, \boldsymbol {u} _ {G} ^ {(t)}\right). \tag {8}
$$

Then, we can compute the marginal valuation function as follows:

$$
\begin{array}{l} V (S \cup \{i \}) - V (S) \\ = \left\| \boldsymbol {u} _ {S \cup \{i \}} ^ {(t)} \right\| \cos \left(\boldsymbol {u} _ {S \cup \{i \}} ^ {(t)}, \boldsymbol {u} _ {G} ^ {(t)}\right) - \left\| \boldsymbol {u} _ {S} ^ {(t)} \right\| \cos \left(\boldsymbol {u} _ {S} ^ {(t)}, \boldsymbol {u} _ {G} ^ {(t)}\right) \\ = \frac {\boldsymbol {u} _ {S \cup \{i \}} ^ {(t)} \cdot \boldsymbol {u} _ {G} ^ {(t)} - \boldsymbol {u} _ {S} ^ {(t)} \cdot \boldsymbol {u} _ {G} ^ {(t)}}{| | \boldsymbol {u} _ {G} ^ {(t)} | |} \\ = \frac {\left(\boldsymbol {u} _ {S} ^ {(t)} + \alpha_ {i} ^ {(t)} \boldsymbol {u} _ {i} ^ {(t)}\right) \cdot \boldsymbol {u} _ {G} ^ {(t)} - \boldsymbol {u} _ {S} ^ {(t)} \cdot \boldsymbol {u} _ {G} ^ {(t)}}{\left| \left| \boldsymbol {u} _ {G} ^ {(t)} \right| \right|} \tag {9} \\ = \frac {\alpha_ {i} ^ {(t)} \boldsymbol {u} _ {i} ^ {(t)} \cdot \boldsymbol {u} _ {G} ^ {(t)}}{| | \boldsymbol {u} _ {G} ^ {(t)} | |} \\ = \alpha_ {i} ^ {(t)} | | \boldsymbol {u} _ {i} ^ {(t)} | | \cos (\boldsymbol {u} _ {i} ^ {(t)}, \boldsymbol {u} _ {G} ^ {(t)}). \\ \end{array}
$$

Here α means the aggregation weight for participant i at round t.

According to Eq. (9), we find that $V ( \bar { S \cup \{ i \} } ) ^ { - } V ( S )$ does not change with the contents of set S. Thus, we do not need to traverse the exponential number of alternative sets of S. Combining Eq. (7) and Eq. (9), we can compute the contribution of participant i at round t $, \phi _ { i } ^ { ( t ) }$ , as:

$$
\begin{array}{l} \phi_ {i} ^ {(t)} = \frac {1}{N} \sum_ {S \subseteq N \backslash \{i \}} \frac {\alpha_ {i} ^ {(t)} | | \boldsymbol {u} _ {i} ^ {(t)} | | \cos (\boldsymbol {u} _ {i} ^ {(t)} , \boldsymbol {u} _ {G} ^ {(t)})}{\binom {N - 1} {| S |}} \tag {10} \\ = \alpha_ {i} ^ {(t)} | | \pmb {u} _ {i} ^ {(t)} | | \cos (\pmb {u} _ {i} ^ {(t)}, \pmb {u} _ {G} ^ {(t)}). \\ \end{array}
$$

From Eq. (10), we can conclude that calculating each participant i’s contribution at round t incurs $O ( | u _ { G } ^ { ( t ) } | )$ time complexity, which is much smaller than the actual Shapley value time complexity of $O ( 2 ^ { N } | u _ { G } ^ { ( t ) } | )$ .

# 5 REWARD ALLOCATION

In this section, we first describe the process of computing reputation by combining the contribution and quality detection results. Then, we describe reward allocation method which assigns the appropriate gradients to participants by jointly considering their reputation values and the distribution of their local gradients and that of the global gradients.

# 5.1 Reputation Calculation

Reputation is a commonly adopted metric to measure the reliability or trustworthiness of an entity in certain activities based on past behaviors [21]–[24]. Such a metric can smooth out the fluctuations in entity behaviours in individual observations in order to build a more objective picture of their behaviour patterns.

We calculate the reputation of each participant i based on his/her contribution and the number of times passing quality detection from round 1 to round t. Let $c _ { i } ^ { ( t ) }$ denote participant $i \mathrm { \ ' } _ { \mathrm { s } }$ cumulative contribution from round 1 to round t. It can be computed as:

$$
c _ {i} ^ {(t)} = \max \left(0, \sum_ {i = 1} ^ {t} \phi_ {i} ^ {(t)}\right). \tag {11}
$$

We define i’s relative contribution, $z _ { i } ^ { ( t ) }$ , based on the maximum observed contribution in the current round t:

$$
z _ {i} ^ {(t)} = \frac {c _ {i} ^ {(t)}}{\max _ {i} (c _ {i} ^ {(t)})}. \tag {12}
$$

Then, we consider how to reflect the impact of the quality detection on reputation. Inspired by [15], [25], we use the Gompertz function to reflect the impact of quality detection on reputation since it more appropriately models the trust in individual interactions. It is defined as follows:

$$
q _ {i} ^ {(t)} = a e ^ {b e ^ {c x _ {i} ^ {(t)}}} \tag {13}
$$

where a specifies the upper asymptote, b controls the displacement among the x axis, and c adjusts the growth rate of the function. The output of the function, denoted by $q _ { i } ^ { ( t ) }$ , is a number in the range of 0 and 1, and represents the impact of the quality detection. The input of the Gompertz function, denoted by $x _ { i } ^ { ( t ) }$ , needs to consider the historical quality detection results for each participant i. To ensure the range of reputation $q _ { i }$ is [0,1], we set a=1, b=-1, c=-5.5. The graph of function is shown in Figure.2.

![](images/74bd37740bf3920093dc6fd59955f287a668e14e89a910d375d99b203809e91d.jpg)



Fig. 2: Gompertz Function

$x _ { i }$ should consider the times of passing/failing the quality detection and we compute $x _ { i } ^ { ( t ) }$ as follows:

$$
x _ {i} ^ {(t)} = \frac {\beta n _ {i} ^ {\text { pass }} - (1 - \beta) n _ {i} ^ {\text { fail }}}{\beta n _ {i} ^ {\text { pass }} + (1 - \beta) n _ {i} ^ {\text { fail }}} \tag {14}
$$

where npi $n _ { i } ^ { p a s s }$ and nfi $n _ { i } ^ { f a i l }$ denote the number of times that participant i passing and failing quality detection, respectively. Compared with passing, failing needs more attention, so the weight $\beta$ of passing the detection ranges from (0, 0.5]. According to Figure.2 and Equation.(14), we can see that the initial and final stages of the curve grow slowly, while the middle stage grows rapidly. In this way, when a certain participant i fails the quality detection once or twice, the q value will not drop rapidly, so that i can still get a relatively good reward in the current round t.

Combining Eq. (12) and Eq. (13), the reputation of participant i in round t, r(ti $t , r _ { i } ^ { ( t ) } \in ( 0 , 1 ]$ , can be computed as follows:

$$
r _ {i} ^ {(t)} = q _ {i} ^ {(t)} z _ {i} ^ {(t)}. \tag {15}
$$

Algorithm 2: FedFAIM Reward Allocation   
Input: $u_i^{(t)}, u_G^{(t)}, \phi_i^{(t)}, n_i^{pass}, n_i^{fail}, \forall i \in W$ Output: $u_{*i}^{(t)}, \forall i \in W$ 1 Initialize $u_{*i}^{(t)} := \emptyset$ 2 for each participant $i \in W$ do
3 Calculate $c_i^{(t)}$ according to Eq. (11);
4 Calculate $z_i^{(t)}$ according to Eq. (12);
5 Calculate $x_i^{(t)}$ according to Eq. (14);
6 Calculate $q_i^{(t)}$ according to Eq. (13);
7 Calculate $r_i^{(t)}$ according to Eq. (15);
8 end
9 for each participant $i \in W$ do
10 Calculate $num_i^{(t)}$ according to Eq. (16);
11 for each gradient $u_{G,j}^{(t)} \in u_G^{(t)}$ do
12 Calculate $s_{i,j}^{(t)}$ according to Eq. (17);
13 Calculate $s_{G,j}^{(t)}$ according to Eq. (18);
14 Calculate $s_j^{(t)}$ according to Eq. (19);
15 end
16 Rank $u_{G,j}^{(t)}, \forall j$ in descending order of $s_j^{(t)}$ ;
17 Select the top $num_i^{(t)}$ gradients to form $u_{*,i}^{(t)}$ ;
18 Send $u_{*,i}^{(t)}$ to $i$ ;
19 end

# 5.2 Reward Calculation

To design a fairness reward allocation, a participant should be rewarded with a version of the model with performance reflecting his/her reputation. Our idea is to control the performance of the model through the number of important gradients from the aggregated model to be allocated to a participant. Therefore, the FedFAIM Reward Allocation module consists of two steps: 1) it determines the number of gradients num(t)i $n u m _ { i } ^ { ( t ) }$ to be assigned to each participant based on their reputation; and 2) it selects $\bar { n } u m _ { i } ^ { ( t ) }$ important gradients from the global gradient vector $u _ { G } ^ { ( t ) }$ .

Step 1: Computing the number of assigned gradients. Based on the notion of Reward Fairness (Definition 2), the number of assigned gradients can be computed as follows:

$$
\operatorname{num} _ {i} ^ {(t)} = \frac {r _ {i} ^ {(t)}}{\max _ {i} r _ {i} ^ {(t)}} | \boldsymbol {u} _ {G} ^ {(t)} |. \tag {16}
$$

Note tha t r(t) $r _ { i } ^ { ( t ) } \in ( 0 , 1 ]$ . The participant with highest reputation receives the entirety of the global model.

Step 2: Selecting the corresponding number of gradients. For each i, FedFAIM selects num(t)i $\hat { \mathbf { \chi } } _ { i } ^ { ( t ) }$ important gradients from the global gradient vector $u _ { G } ^ { ( t ) }$ . To measure the importance of each gradient entry uG,j $u _ { G , j } ^ { ( t ) }$ in the global gradient vector $u _ { G } ^ { ( t ) }$ , We define two scores s(t)i,j $s _ { i , j } ^ { ( t ) }$ an d $s _ { G , j } ^ { ( t ) }$ .

The larger the absolute value of u(t)i,j , t $s _ { i , j } ^ { ( t ) }$ si,j is determined by the distribution of the local gradient $u _ { i , j } ^ { ( t ) }$ he more score participant i $u _ { i } ^ { ( t ) }$ .

can obtain from the global gradient u(t)G,j . $u _ { G , j } ^ { ( t ) }$ Based on this intuition, $s _ { i , j } ^ { ( t ) }$ can be computed as:

$$
s _ {i, j} ^ {(t)} = \frac {\left| u _ {i , j} ^ {(t)} \right|}{\sum_ {j} \left| u _ {i , j} ^ {(t)} \right|}. \tag {17}
$$

$s _ { G , j } ^ { ( t ) }$ s G,j is determined by the distribution of the global gradient $u _ { G } ^ { ( t ) }$ . The larger the absolute value of u(t)G,j , $u _ { G , j } ^ { ( t ) }$ the higher its influence is on the performance of the global model. Based on this intuition, the s G,j $s _ { G , j } ^ { ( t ) }$ can be computed as:

$$
s _ {G, j} ^ {(t)} = \frac {\left| u _ {G , j} ^ {(t)} \right|}{\sum_ {j} \left| u _ {G , j} ^ {(t)} \right|}. \tag {18}
$$

Let $s _ { j } ^ { ( t ) }$ ) be the overall score for each gradient entry u(t)G,j b $u _ { G , j } ^ { ( t ) }$ in global gradient vector $u _ { G } ^ { ( t ) }$ . It can be computed as:

$$
s _ {j} ^ {(t)} = s _ {i, j} ^ {(t)} \times s _ {G, j} ^ {(t)}. \tag {19}
$$

Finally, for each participant $i ,$ FedFAIM ranks the gradient entries u G,j $u _ { G , j } ^ { ( \bar { t } ) }$ in the global gradient vector ${ \pmb u } _ { G } ^ { ( t ) }$ in descending order of their $s _ { j } ^ { ( t ) }$ s scores, and selects the top num(t)i gradients to form the assigned gradient vector u(t)∗i $u _ { * i } ^ { ( t ) }$ for i in round t. The FedFAIM reward allocation method is summarized in Algorithm 2.

# 5.3 Reward Fairness Guarantee

As Definition.2 in Section.2 shows, We consider that an agent who contributes higher-quality gradients over the entire training process should eventually be rewarded with converged model parameters closer to that of the server. We use reputation $r _ { i } ^ { ( t ) }$ ri to measure the overall data quality and contribution of participant i from round 1 to round t and use the loss Function $F$ to measure the performance of the model parameters. Then we show that reward fairness could be guaranteed under some conditions on model parameter $\mathcal { M } _ { G } ^ { ( t ) }$ and loss function $F$ In Theorem.1. In detail, we prove that if participant i has higher reputation $r _ { i } ^ { ( t ) }$ and his model parameters M (t−1)i $\dot { M } _ { i } ^ { ( t - 1 ) }$ closer to that of server than participant $i ^ { \prime }$ in round t− 1 is at least 2max $\{ | | u _ { * , i } ^ { ( t ) } | | , | | u _ { * , i ^ { ' } } ^ { ( t ) } | | \}$ |, , participant i could be assigned with model parameter M(t)i i $\mathcal { M } _ { i } ^ { ( t ) }$ n round t which incurs smaller training loss.

Theorem 1. Let $\Delta _ { i } ^ { ( t ) } : = | | \mathcal { M } _ { G } ^ { ( t ) } - \mathcal { M } _ { i } ^ { ( t ) } | |$ . Suppose that $\mathcal { M } _ { G } ^ { ( t ) }$ is near to a stationary point of $\bar { F } f o r t \in \mathbb { Z } ^ { + }$ and some regularity r(t) conditions on F hold. For all $r _ { i } ^ { ( t ) } \geq r _ { i ^ { \prime } } ^ { ( t ) }$ r 0 , and $\Delta _ { i ^ { \prime } } ^ { ( t - 1 ) } - \Delta _ { i } ^ { ( t - 1 ) } \geq$ $i , i ^ { \prime } \in W$ 2max and t, if reputation $\{ | | u _ { * i } ^ { ( t ) } | | , | | u _ { * i ^ { ' } } ^ { ( t ) } | | \}$ , then $F ( \dot { \mathcal { M } } _ { i } ^ { ( t ) } ) \leq F ( \mathcal { M } _ { i ^ { \prime } } ^ { ( t ) } )$ .

Proof 1. Our proof contains two steps.

Step 1: we first prove $\Delta _ { i ^ { \prime } } ^ { ( t ) } \geq \Delta _ { i } ^ { ( t ) }$ > according to the condition $\Delta _ { i ^ { \prime } } ^ { ( t - 1 ) } - \Delta _ { i } ^ { ( t - 1 ) } \geq$ 2max $\{ | | u _ { * , i } ^ { ( t ) } | | , | | u _ { * , i ^ { ' } } ^ { ( t ) } | | \}$ |u ∗,i| .

According to the definition, we can get that

$$
\Delta_ {i} ^ {(t)} = | | \mathcal {M} _ {G} ^ {(t)} - \mathcal {M} _ {i} ^ {(t)} | |
$$

$$
\Delta_ {i} ^ {(t - 1)} = \left| \left| \mathcal {M} _ {G} ^ {(t - 1)} - \mathcal {M} _ {i} ^ {(t - 1)} \right| \right| \tag {20}
$$

$$
\mathcal {M} _ {i} ^ {(t)} = \mathcal {M} _ {i} ^ {(t - 1)} + u _ {*, i} ^ {(t)}
$$

According to the (20) and triangle inequality, we can get that:

$$
\Delta_ {i} ^ {(t)} \leq \Delta_ {i} ^ {(t - 1)} + | | u _ {*, i} ^ {(t)} | | \tag {21}
$$

Similarly, we can get that

$$
\Delta_ {i ^ {\prime}} ^ {(t - 1)} \leq \Delta_ {i ^ {\prime}} ^ {(t)} + | | u _ {*, i ^ {\prime}} ^ {(t)} | | \tag {22}
$$

2max From the condition (t−1) i ∆(t−1) i ≥ $\{ | | u _ { * , i } ^ { ( t ) } | | , | | u _ { * , i ^ { ' } } ^ { ( t ) } | | \}$ ||u , we have

$$
\begin{array}{l} \Delta_ {i ^ {\prime}} ^ {(t - 1)} - \Delta_ {i} ^ {(t - 1)} \geq 2 \max _ {(t)} \left\{\left| \left| u _ {*, i} ^ {(t)} \right| \right|, \left| \left| u _ {*, i ^ {\prime}} ^ {(t)} \right| \right| \right\} \tag {23} \\ \geq | | u _ {*, i} ^ {(t)} | | + | | u _ {*, i ^ {\prime}} ^ {(t)} | | \\ \end{array}
$$

Rearranging (23), we can get

$$
\Delta_ {i ^ {\prime}} ^ {(t - 1)} - \left| \left| u _ {*, i ^ {\prime}} ^ {(t)} \right| \right| \geq \Delta_ {i} ^ {(t - 1)} + \left| \left| u _ {*, i} ^ {(t)} \right| \right| \tag {24}
$$

Combining (21), (22) and (24), we have

$$
\begin{array}{l} \Delta_ {i ^ {\prime}} ^ {(t)} \geq \Delta_ {i ^ {\prime}} ^ {(t - 1)} - | | u _ {*, i ^ {\prime}} ^ {(t)} | | + | | u _ {G} ^ {(t)} | | \\ \geq \Delta_ {i} ^ {(t - 1)} + | | u _ {*, i} ^ {(t)} | | + | | u _ {G} ^ {(t)} | | \tag {25} \\ \geq \Delta_ {i} ^ {(t)} \\ \end{array}
$$

Step 2: we prove $F ( \mathcal { M } _ { i } ^ { ( t ) } ) \leq F ( \mathcal { M } _ { i ^ { \prime } } ^ { ( t ) } )$ according to $\Delta _ { i ^ { \prime } } ^ { ( t ) } \geq$ ∆(t)i a ${ \Delta } _ { i } ^ { ( t ) }$ nd some regularity conditions of the loss function $F ( )$ .

Following the idea of [26], we assume $F ( )$ is both L-smooth and µ-strongly convex with $L \leq \mu$ . We first recall the respective definitions of these two concepts below.

Definition 5 (L-Smooth F). If F is L-smooth, then $\forall m , m ^ { ' } \in \mathcal { M }$

$$
F (m) \leq F (m ^ {\prime}) + \nabla F (m ^ {\prime}) ^ {T} (m - m ^ {\prime}) + \frac {L}{2} | | m - m ^ {\prime} | | ^ {2}.
$$

Definition 6 (µ-Strongly Convex F ). If F is µ-strongly convex, then $\forall m , m ^ { ' } \in \mathcal { M }$

$$
F (m) \geq F (m ^ {\prime}) + \nabla F (m ^ {\prime}) ^ {T} (m - m ^ {\prime}) + \frac {\mu}{2} | | m - m ^ {\prime} | | ^ {2}.
$$

From L-smoothness, we have

$$
F \left(\mathcal {M} _ {* i} ^ {(t)}\right) \leq \underbrace {F \left(\mathcal {M} _ {G} ^ {(t)}\right) + \nabla F \left(\mathcal {M} _ {G} ^ {(t)}\right) ^ {T} \left(\mathcal {M} _ {* i} ^ {(t)} - \mathcal {M} _ {G} ^ {(t)}\right) + \frac {L}{2} \left(\Delta_ {i} ^ {(t)}\right) ^ {2}} _ {R _ {L}}. \tag {26}
$$

From µ-Strongly, we have

$$
F \left(\mathcal {M} _ {i ^ {\prime}} ^ {(t)}\right) \geq \underbrace {F \left(\mathcal {M} _ {G} ^ {(t)}\right) + \nabla F \left(\mathcal {M} _ {G} ^ {(t)}\right) ^ {T} \left(\mathcal {M} _ {i ^ {\prime}} ^ {(t)} - \mathcal {M} _ {G} ^ {(t)}\right) + \frac {\mu}{2} \left(\Delta_ {i ^ {\prime}} ^ {(t)}\right) ^ {2}} _ {R _ {\mu}}. \tag {27}
$$

Therefore, we can get that

$$
\begin{array}{l} R _ {L} - R _ {\mu} \\ = \underbrace {\nabla F (\mathcal {M} _ {G} ^ {(t)}) ^ {T} (\mathcal {M} _ {i} ^ {(t)} - \mathcal {M} _ {i ^ {\prime}} ^ {(t)})} _ {R _ {1}} + \underbrace {\frac {1}{2} (L (\Delta_ {i} ^ {(t)}) ^ {2} - \mu (\Delta_ {i ^ {\prime}} ^ {(t)}) ^ {2})} _ {R _ {2}}. \tag {28} \\ \end{array}
$$

From the previous justification and assumption, $L \leq \mu$ and $\Delta _ { i } ^ { ( t ) } \leq \Delta _ { i ^ { \prime } } ^ { ( t ) }$ ≤ ∆(t)0 , i we have

$$
R _ {2} = \frac {1}{2} (L (\Delta_ {i} ^ {(t)}) ^ {2} - \mu (\Delta_ {i ^ {\prime}} ^ {(t)}) ^ {2}) \leq \frac {L}{2} ((\Delta_ {i} ^ {(t)}) ^ {2} - (\Delta_ {i ^ {\prime}} ^ {(t)}) ^ {2}) \leq 0. \tag {29}
$$

Now we formalize $\mathcal { M } _ { G } ^ { ( t ) }$ being near to a stationary point by specifying an upper bound on the gradient

$$
\left| \left| \nabla F \left(\mathcal {M} _ {G} ^ {(t)}\right) \right| \right| \leq \frac {L \left| \left(\Delta_ {i} ^ {(t)}\right) ^ {2} - \left(\Delta_ {i ^ {\prime}} ^ {(t)}\right) ^ {2} \right|}{2 \left| \left| \mathcal {M} _ {i} ^ {(t)} - \mathcal {M} _ {i ^ {\prime}} ^ {(t)} \right| \right|}. \tag {30}
$$

According to Cauchy-Schwarz inequality, we can get

$$
\begin{array}{l} \left| R _ {1} \right| = \left| \nabla F \left(\mathcal {M} _ {G} ^ {(t)}\right) ^ {T} \left(\mathcal {M} _ {i} ^ {(t)} - \mathcal {M} _ {i ^ {\prime}} ^ {(t)}\right) \right| \tag {31} \\ \leq | | \nabla F (\mathcal {M} _ {G} ^ {(t)}) | | \times | | \mathcal {M} _ {i} ^ {(t)} - \mathcal {M} _ {i ^ {\prime}} ^ {(t)} | | \\ \end{array}
$$

Combining (30) and (31), we can get that

$$
\begin{array}{l} \left| R _ {1} \right| \leq \frac {L \left| \left(\Delta_ {i} ^ {(t)}\right) ^ {2} - \left(\Delta_ {i ^ {\prime}} ^ {(t)}\right) ^ {2} \right|}{2} \tag {32} \\ \leq | R _ {2} | \\ \end{array}
$$

According to (32) and $R _ { 2 } \leq 0 ,$ , we have $R _ { 1 } + R _ { 2 } \leq 0 \quad$ . Thus $R _ { L } - R _ { \mu } \leq 0$ and $R _ { L } \leq R _ { \mu }$ .

Therefore, according to (26) and (27), we obtain $F ( \mathcal { M } _ { i } ^ { ( t ) } ) ~ \le$ $R _ { L } \leq R _ { \mu } \leq F ( \mathcal { M } _ { i ^ { \prime } } ^ { ( t ) } )$ .

# 6 EXPERIMENTAL EVALUATION

In this section, we first describe our experiment settings, then evaluate our gradient aggregation, contribution assessment and reward allocation methods by comparing with the state-of-the-art approaches.

# 6.1 Datasets

We perform our experiments on datasets from two domains: (1) image classification datasets, including MNIST [27] and CIFAR10 [28]. (2) text classification datasets, including Stanford sentiment treebank (SST) [29]. MNIST consists of 60,000 training samples and 10,000 test samples. CIFAR10 consists of 50,000 training samples and 10,000 test samples. SST consists of 8040 training samples and 3815 test samples. For each dataset, we randomly extracted 1% of the training data as the validation dataset to be stored in the FL server. In order to evaluate the effectiveness of the methods in realistic settings, we investigate four different data splits considering uniform distribution, dataset sizes and class numbers as well as noisy label on all the three datasets.

Uniform(UNI). We include the simplest setting of the uniform/homogeneous data partition among participants on all three datasets. In this setting, all participants own the same number of randomly partitioned samples from the datasets and the participants are expected to achieve comparable test accuracy after convergence.

Imbalanced Dataset Size (IMDS). We randomly partition 10,000 MNIST samples into 20 data silos (i.e. participants). The 20 participants own {50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950} samples, respectively. We randomly partition 5,000 CIFAR10 samples among 10 participants. The 10 participants own {100, 200, 300, 400, 500, 500, 600, 700, 800, 900} samples, respectively. We randomly partition 11855 SST samples into 10 data silos. The 10 participants own {100, 350, 600, 850, 1100, 1271, 1521, 1771, 2021, 2271} samples, respectively. In this way, each participant has a different number of samples, with the first having the smallest dataset and the last having the largest.

Imbalanced Class Number (IMCN). MNIST and CIFAR10 dataset each contains 10 classes. For MNIST, the 20 participants own {1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10} classes of samples, respectively. For CIFAR10, the 10 participants own {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} classes of samples, respectively. For SST, the 10 participants own {1, 1, 2, 2, 3, 3, 4, 4, 5, 5} classes of samples, respectively. Note under this setting, all participants have the same dataset size, but different number of classes. In this way, each participant has a different number of class, with the first having the least number of classes and the last having the most.

TABLE 2: Test Accuracy of our aggregation method on all four datasets in different data splits when δ varies 

<table><tr><td></td><td colspan="4">MNIST</td><td colspan="4">CIFAR</td><td colspan="4">SST</td></tr><tr><td>δ</td><td>UNI</td><td>IMDS</td><td>IMCN</td><td>NOISY</td><td>UNI</td><td>IMDS</td><td>IMCN</td><td>NOISY</td><td>UNI</td><td>IMDS</td><td>IMCN</td><td>NOISY</td></tr><tr><td>-0.01</td><td>96.91</td><td>97.30</td><td>86.84</td><td>95.44</td><td>70.48</td><td>69.08</td><td>74.48</td><td>71.98</td><td>65.67</td><td>63.08</td><td>61.08</td><td>59.28</td></tr><tr><td>-0.03</td><td>96.83</td><td>97.08</td><td>86.21</td><td>94.17</td><td>70.44</td><td>68.28</td><td>74.50</td><td>71.33</td><td>65.62</td><td>62.79</td><td>61.23</td><td>58.87</td></tr><tr><td>-0.05</td><td>96.90</td><td>96.74</td><td>85.74</td><td>94.20</td><td>70.47</td><td>68.21</td><td>74.45</td><td>71.42</td><td>65.66</td><td>62.38</td><td>60.89</td><td>58.29</td></tr><tr><td>-0.08</td><td>96.84</td><td>96.71</td><td>81.94</td><td>93.98</td><td>70.41</td><td>68.04</td><td>73.91</td><td>71.29</td><td>65.60</td><td>62.19</td><td>60.82</td><td>58.14</td></tr><tr><td>-0.10</td><td>96.78</td><td>96.48</td><td>81.91</td><td>93.39</td><td>70.39</td><td>66.96</td><td>73.82</td><td>70.58</td><td>65.71</td><td>62.11</td><td>60.01</td><td>57.65</td></tr></table>

![](images/b4e314c6b4ec57571015e3d12e8d08dcd80cf5100cfebcd73e56385e033607db.jpg)



(a) UNI

![](images/29eecc9e58d5b93ee5c49c9cc960d3ee6d143a703963eef4966d3c4df0c21ee2.jpg)



(b) IMDS

![](images/edbb6f99a3ed76e76dd451e2012bbf2f054d3eef847d0bae3d53bcf0f50dd635.jpg)



(c) IMCN

![](images/d9bf06b5790d6941d4fe93d8ad26a23868f4a6f83fe447c8de5242da2c2a3cd1.jpg)



(d) NOISY

Fig. 3: Test accuracy of different gradient aggregation Methods on MNIST in different data splits.   
![](images/c57891dacc79dee72d9d9c39488e5b1a622e9bfc66a6daaea8eff173d4137a45.jpg)



(a) UNI

![](images/a5ebd069892d53ac4c5649eded173db29e39fce70926962e791a9d32470b45b6.jpg)



(b) IMDS

![](images/ddb8bc90bd91e38a0bf7de5ef879734eb7dfd98772d1c9240686085bf930cf0c.jpg)



(c) IMCN

![](images/3d24b224825d1aad629445ad245f4dc005038acd41a7d3cff113eb5c4c9caa7d.jpg)



(d) NOISY

Fig. 4: Test accuracy of different gradient aggregation methods on CIFAR10 in different data splits.   
![](images/0fecce5b8dd219277f2830b3d297054f3233de7dbec2095e9a3b6a8ac93322f2.jpg)



(a) UNI

![](images/4ce034f4e52c139242fc97717e8ca7ac5058e900393e86f8bcbbc4d4a62b38e4.jpg)



(b) IMDS

![](images/48360c5bd999114384cfaa06f75a9175999d755acdc96e2f3c9e3a0ee921abde.jpg)



(c) IMCN

![](images/b398b1c796a73776530accb92c8ee28edb74e5490f85e0a5926937c268a27169.jpg)



(d) NOISY   
Fig. 5: Test accuracy of different gradient aggregation methods on SST in different data splits.

Noisy Labels (NOISY). We incorporate incorrect labels into the datasets. For MNIST, the 20 participants are set to own {95%, 90%, 85%, 80%, 75%, 70%, 65%, 60%, 55%, 50%, 45%, 40%, 35%, 30%, 25%, 20%, 15%, 10%, 5%, 0%} incorrect labels, respectively. For CIFAR10, the 10 participants are set to own {90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%, 0%} incorrect labels, respectively. For SST, the 10 participants are set to own {90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%, 0%} incorrect labels, respectively. In this way, each participant has a different percentage of incorrect labels, with the first participant having the most and the last participant having the least.

Base Models and Hyperparameters. We implement a typical federated optimization algorithm FedSGD [20] and three deep learning models: a standard 2-layer CNN model for MNIST [30], a standard 3-layer CNN for CIFAR-10 [31] and a text embedding CNN for SST [29]. We explore the effect on the test accuracy of the aggregation model when δ varies from -0.01 to -0.1 in section.6.4 and set the loss threshold as δ = −0.01. We controlled parameter γ = 0.1 and Gompertz function parameters as a = 1, b = −1, c = −5.5, β = 0.2.

![](images/c32a42867941643b820cc5af5325ef823e577e6f2b21545590a86cb7960ec63a.jpg)



![](images/4a16aca6a2b9d163e21a00e0eb24bd84dbd2b2902c41e11249d3553abe2604f9.jpg)



![](images/7f10eff1a0e75e302b82ed30dd95e5926af30b7eb511aa8d50dd3336eff9ec56.jpg)



Fig. 6: Running time of different contribution assessment methods on all datasets in different data splits.

# 6.2 Comparison Baselines

We compare the FedFAIM gradient aggregation method with three baselines: FedAvg [20], FairAvg [32] and FedQD [15]. FedAvg determines the aggregation weights based on the sizes of local datasets. FairAvg assigns equal weights to all participants. FedQD determines the aggregation weights based on the loss of local model .

We compare the FedFAIM contribution assessment method with three baselines: CI [13], TMC-Shapley [12], GTB [14] and COS-SIM [16]. CI proposes a contribution index to evaluate the contribution of each participant by reconstructing models using the intermediate FL model updates. TMC-Shapley adopts the sample methods and focuses on improving the computational efficiency. GTB-shapley proposes a repertoire of efficient algorithms for approximating the Shapley value. COS-SIM introduces an additive error to approximate Shapley value without relying on an auxiliary dataset. [15] also proposes a method which assesses each participant’s contribution. The key idea is to calculate the difference between local models and the final model. However, it measures each participant’s contribution after all training rounds end and could not be applied to our intermediate reward. Therefore, we do not compare our method with [15].

We compare the FedFAIM reward allocation method with four baselines: Standalone, FedAvg [20], CFFL [18] and RFFL [16]. Under Standalone, participants train their models only using their respective local datasets. FedAvg allocates the same model for all participants without regard to their contributions. CFFL uses model accuracy as the contribution index. RFFL proposed a novel metric to assess contribution. Under these two approaches, each participant receives a final model with performance reflecting his/her contribution.

# 6.3 Evaluation Metrics

• Test Accuracy: We use test accuracy as the performance metric for gradient aggregation and reward allocation.   
• Running Time: We use running time to compare the efficiency of the contribution assessment methods.   
• Pearson Correlation Coefficient: We use Pearson Correlation Coefficient (PCC) with actual Shapley value as the metric to measure the performance of the contribution assessment methods. It is computed as follows:

$$
P C C = \frac {\sum_ {i} (x _ {i} - \overline {{{x}}}) (y _ {i} - \overline {{{y}}})}{s _ {x} s _ {y}} \tag {33}
$$

where $x _ { i }$ and $y _ { i }$ represent participant i’s actual Shapley value and the estimated contribution by a given method, respectively. $s _ { x }$ and $s _ { y }$ are the respective corrected standard deviations.

• Jain’s Fairness Index: We use Jain’s Fairness Index (JFI) to measure the fairness of the reward allocation methods, which is calculated as:

$$
J F I = \frac {(\sum_ {i} \frac {x _ {i}}{z _ {i}}) ^ {2}}{N \sum_ {i} (\frac {x _ {i}}{z _ {i}}) ^ {2}} \tag {34}
$$

where $x _ { i }$ and $z _ { i }$ are the test accuracy of the model allocated to i and i’s actual Shapley value, respectively.

# 6.4 Experiment Results for Gradient Aggregation

We first explore how the test accuracy of the FedFAIM aggregation method changes when the loss threshold δ varies from -0.01 to -0.1 (-0.01, -0.03, -0.05, -0.08, -0.10). We record the result in Table.2. It can be observed that the test accuracy has no obvious change when δ varies. Therefore we set the loss threshold $\delta = - 0 . 0 1$ in the following experiments.

Then for both datasets, we compare the test accuracy of gradient aggregation method and plot the results in Fig. 3, Fig. 4 and Fig.5. It can be observed that FedFAIM achieves the similar performance under UNI but performance in other three heterogeneous data splits. Among the baselines, FedDQ outperforms both FairAvg and FedAvg in all the three data splits. FairAvg and FedAvg achieved similar performance under IMCN and NOISY conditions, but FedAvg outperforms FairAvg under IMDS conditions since it considers the effect of dataset size. As FedFAIM has filtered out potentially low quality gradients and block malicious participants through quality detection, all the selected local gradients are expected to be valuable. The aggregated gradients involving all selected local gradients, uN , is expected to have the highest value. Therefore, compared to other model aggregation methods, FedFAIM can enhance model accuracy and boost the convergence, thus achieving better aggregation fairness.

# 6.5 Experiment Results for Contribution Assessment

For both datasets, we compare FedFAIM with four baselines: CI, TMC-Shapley, GTB and COS-SIM in terms of the Pearson Correlation Coefficient with the actual Shapley value and the running time. The results are shown in Table. 3 and Fig. 6. We observe that under all settings, FedFAIM achieves the highest PCC and the least running time among all the baselines. First, FedFAIM leverages the cosine similarity between the local gradients and the global gradients in each round, which is a direct approximation to the actual Shapley value. However, in comparison, TMC-Shapley and GTB work based on sampling random permutations of the set of participants and CI reconstructs approximately the models on different combinations of the datasets. Based on the process of computing Shapley value, these algorithms avoid a large number of repeated training through sampling and partial training. However, this process also causes a decrease in the accuracy of the assessment of participants contribution. COS-SIM improves its accuracy through introducing an additive error to approximate Shapley value, but this method does not filter out potentially low quality local gradients which could make the contribution estimation less accurate. In addition, FedFAIM achieves the least running time since we only need to calculate the inner products and the modulus of local and global gradients, which takes linear asymptotic running time, as can be seen in section 4. However, methods based on sampling may take up to exponential running time since different combinations of datasets are required to be trained and evaluated. We hope this provides some explanations.

![](images/e78658b6277806404674d3ea21095dee8a17b5f82ef349023f4705ac67824868.jpg)



(a) UNI

![](images/b664a916f6d2613489849ba5fb0cda777deeea9966b16758b9537b107482a436.jpg)



(b) IMDS

![](images/d6db570d732d58f678552270f436b3626cbab46c61ccd799bf154b771bf230bc.jpg)



(c) IMCN

![](images/5fae566f32532b34fb1bc6397f3845d3bbd1961e0abaf9530a6405b3f2e41fdc.jpg)



(d) NOISY

Fig. 7: Test accuracy of different reward allocation methods on MNIST in different data splits for all participants.   
![](images/fe73f39b216e138c1c5f0f8c4db65e6761028f4392ddcd22bf173cc823d0de1c.jpg)



(a) UNI

![](images/dab9193b77895aec15676f1461bd2b2163ab73f4c317cf2ae0bcab9260760f2f.jpg)



(b) IMDS

![](images/95e90bc3fed95787f74fc2f31cc762c7560f41ee16180955b0b952bfe2ecf846.jpg)



(c) IMCN

![](images/d8ae9d7d664807bbacb0a1c1e80e185889cdaf11b965fc9df73f238960517b69.jpg)



(d) NOISY

Fig. 8: Test accuracy of different reward allocation methods on CIFAR10 in different data splits for all participants.   
![](images/e95f2d2ebdeb7fd2c266df6fd6fd2d42cdffcb86a824320180b8c2ceb9a2afe2.jpg)



(a) UNI

![](images/78b0d926591e5c9db8b3266e021e1b7fb3dbe2bf459c314d66f642722070bd1e.jpg)



(b) IMDS

![](images/36450901c01df2e38730328a37ae6ae165f94144b541600b6b7f6f2cc36bf575.jpg)



(c) IMCN

![](images/667c77e8d070fe8287523973c910411bac669c1048f7adc70647237294dc2224.jpg)



(d) NOISY   
Fig. 9: Test accuracy of different reward allocation methods on SST in different data splits for all participants.

# 6.6 Experiment Results for Reward Allocation

For both datasets, we compare the test accuracy of each participant’s final allocated model and Jain’s Fairness Index. The results are shown in Fig. 7 , Fig. 8, Fig. 9, and Table. 4. It can be observed that under all experiment settings, participants with larger datasets, more classes and less noisy labels generally receive more accurate models. All methods achieve lower test accuracy than FedAvg under all conditions, since FedAvg assigns the same global model in each training round to all participants without regard to their contributions, enabling all of them to achieve the highest test accuracy. Standalone achieves the lowest accuracy among all comparison approaches. This shows that participants can receive positive utility by joining federated learning, even if the performance of final models they receive depends on their contributions.

TABLE 3: The Pearson Correlation Coefficient with the actual Shapley value 

<table><tr><td>Setting</td><td>FedFAIM</td><td>CI</td><td>TMC-Shapley</td><td>GTB</td><td>COS-SIM</td></tr><tr><td>MNIST-UNI</td><td>0.991</td><td>0.982</td><td>0.989</td><td>0.977</td><td>0.984</td></tr><tr><td>MNIST-IMDS</td><td>0.966</td><td>0.922</td><td>0.913</td><td>0.908</td><td>0.942</td></tr><tr><td>MNIST-IMCN</td><td>0.960</td><td>0.918</td><td>0.911</td><td>0.902</td><td>0.921</td></tr><tr><td>MNIST-NOISY</td><td>0.959</td><td>0.945</td><td>0.938</td><td>0.902</td><td>0.914</td></tr><tr><td>CIFAR-UNI</td><td>0.983</td><td>0.975</td><td>0.971</td><td>0.973</td><td>0.986</td></tr><tr><td>CIFAR-IMDS</td><td>0.926</td><td>0.872</td><td>0.866</td><td>0.854</td><td>0.858</td></tr><tr><td>CIFAR-IMCN</td><td>0.925</td><td>0.891</td><td>0.884</td><td>0.876</td><td>0.911</td></tr><tr><td>CIFAR-NOISY</td><td>0.919</td><td>0.878</td><td>0.866</td><td>0.852</td><td>0.886</td></tr><tr><td>SST-UNI</td><td>0.973</td><td>0.941</td><td>0.933</td><td>0.919</td><td>0.923</td></tr><tr><td>SST-IMDS</td><td>0.857</td><td>0.843</td><td>0.817</td><td>0.801</td><td>0.83</td></tr><tr><td>SST-IMCN</td><td>0.871</td><td>0.847</td><td>0.821</td><td>0.868</td><td>0.852</td></tr><tr><td>SST-NOISY</td><td>0.864</td><td>0.847</td><td>0.817</td><td>0.808</td><td>0.811</td></tr></table>

As the participants receive different models, we analyze the performance of the models received by each participant in relation to their contributions. Under FedFAIM, participants generally receive better performing models than under CFFL and RFFL as these two approaches do not consider aggregation fairness and ignore the distribution of local gradients when allocating the reward. In addition, the participant who contributes the most receives a model with closest performance to FedAvg under FedFAIM. As indicated by JFI values, FedFAIM achieves comparable level of fairness with CFFL and RFFL, which are much fairer than FedAvg. The results show that FedFAIM is capable of distinguishing participants contributions and assigning them with appropriate models in a highly fair manner, while providing participants with stronger incentives (i.e., better model performance) than CFFL and RFFL.

TABLE 4: Jain’s Fairness Index (%) 

<table><tr><td>Setting</td><td>FedAvg</td><td>CFFL</td><td>RFFL</td><td>FedFAIM</td></tr><tr><td>MNIST-UNI</td><td>92.37</td><td>94.9</td><td>93.47</td><td>95.21</td></tr><tr><td>MNIST-IMDS</td><td>55.35</td><td>67.51</td><td>68.14</td><td>67.04</td></tr><tr><td>MNIST-IMCN</td><td>51.42</td><td>93.56</td><td>92.27</td><td>92.95</td></tr><tr><td>MNIST-NOISY</td><td>50.89</td><td>89.44</td><td>89.69</td><td>88.96</td></tr><tr><td>CIFAR-UNI</td><td>94.68</td><td>96.71</td><td>95.86</td><td>95.98</td></tr><tr><td>CIFAR-IMDS</td><td>71.26</td><td>81.37</td><td>80.78</td><td>80.12</td></tr><tr><td>CIFAR-IMCN</td><td>66.82</td><td>93.57</td><td>92.86</td><td>92.89</td></tr><tr><td>CIFAR-NOISY</td><td>65.12</td><td>94.91</td><td>94.17</td><td>93.91</td></tr><tr><td>SST-UNI</td><td>91.03</td><td>92.83</td><td>92.74</td><td>92.54</td></tr><tr><td>SST-IMDS</td><td>58.45</td><td>69.13</td><td>68.08</td><td>68.03</td></tr><tr><td>SST-IMCN</td><td>54.37</td><td>86.44</td><td>87.69</td><td>86.35</td></tr><tr><td>SST-NOISY</td><td>53.81</td><td>88.92</td><td>89.23</td><td>87.94</td></tr></table>

# 7 RELATED WORK

Incentive mechanisms for FL can be broadly divided into two categories: 1) monetary incentive mechanisms, and 2) non-monetary incentive mechanisms [33].

Monetary incentive mechanisms for FL generally assume that the data owners (i.e., participants of FL model training) and the users of the final FL models are two separate groups, i.e., data owners do not directly use the final FL model. Thus, those incentive mechanisms focusing on providing monetary rewards to data owners aim to motivate them to contribute more high quality data to FL model training. Song et al. [13] proposed RRAFL to select and pay data owners, which provides an FL incentive mechanism based on reputation and reverse auction. Sarikaya et al. [17] models the interaction between the FL server (i.e. the model user) and participants as a Stackelberg game with the aim of improving the FL model performance by optimizing the commitment of local computational resources as well as the allocation of the incentive budget. [34], [35] applied contract theory [36] to design an efficient incentive mechanism to attract more participants with high data quality to join FL. Zhan et al. [37] proposed a deep reinforcement learning based incentive mechanism to determine the optimal pricing strategy for the FL server and the optimal training strategies for participants. This category of researches benefits heavily from incentive mechanism research results in economics and related disciplines. As they assume that the data owners care more about monetary rewards, they generally freely share the intermediate FL models and the final FL model among the data owners during FL training iterations.

When the participants of FL are also the end users of the final FL models, competition might exist among data owners under HFL settings. The FL training process which shares the same model to all participants without regards to their contributions has been shown to cause breakdown of collaboration since monetary incentive is no longer a strong motivator. Non-monetary incentive mechanisms such as [16], [18], which assign each participant a different model in each training iteration with performance reflecting his/her contribution, is starting to emerge. Nevertheless, they did not consider collaborative fairness during model aggregation. In addition, their reward allocation schemes only consider the distribution of the global model’s gradients but neglect the distribution of each participant’s local gradients. The lack of consideration for the collaborative fairness during aggregation and the local gradients can make it difficult for the assigned model to accurately reflect each participant’s contribution, thus weakening the incentives.

FedFAIM belongs to the category of non-monetary FL incentive mechanisms and aims to provider stronger incentives to FL participants via allocating fairer and more accurate models. Since our design is compatible with current prevailing server-client FL framework, compared with pure decentralized approaches [16], [18], FedFAIM can be more easily adopted by existing FL systems.

# 8 CONCLUSIONS

In this paper, we proposed a unique fairness-aware incentive mechanism for federated learning - FedFAIM - which satisfies aggregation fairness and reward fairness. To the best of our knowledge, it is the first non-monetary FL incentive mechanism which allows intermediate participant contribution assessment to influence the FL model aggregation process, and jointly considers the relationship between each participant’s local model gradient distribution with that of the global aggregated model when assigning model gradients as rewards to them. Further, we prove that reward fairness could be theoretically guaranteed. Extensive experiments show that FedFAIM provides stronger incentives in terms of overall model performance compared to similar nonmonetary FL incentive mechanisms while achieving a high level of fairness. It holds promising potential to enable collaborative FL model training among data owners with competitive relationships to be sustained.

# ACKNOWLEDGMENT

Lan Zhang and Xiang-Yang Li are the corresponding authors. The research is supported by National Key R&D Program of China 2018YFB0803400, China National Funds for Distinguished Young Scientists with No. 61625205, China National Natural Science Foundation with No. 61822209, No. 62132018, No. 61932016, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002, The University Synergy Innovation Program of Anhui Province with No. GXXT-2019-024.

# REFERENCES

[1] M. Magdziarczyk, “Right to be forgotten in light of regulation (eu) 2016/679 of the european parliament and of the council of 27 april 2016 on the protection of natural persons with regard to the processing of

personal data and on the free movement of such data, and repealing directive 95/46/ec,” in 6th INTERNATIONAL MULTIDISCIPLINARY SCIENTIFIC CONFERENCE ON SOCIAL SCIENCES AND ART SGEM 2019, 2019, pp. 177–184.   
[2] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” ACM Transactions on Intelligent Systems and Technology (TIST), vol. 10, no. 2, pp. 1–19, 2019.   
[3] Y. Chen, L. Su, and J. Xu, “Distributed statistical machine learning in adversarial settings: Byzantine gradient descent,” Proceedings of the ACM on Measurement and Analysis of Computing Systems, vol. 1, no. 2, pp. 1–25, 2017.   
[4] R. Shokri and V. Shmatikov, “Privacy-preserving deep learning,” in Proceedings of the 22nd ACM SIGSAC conference on computer and communications security, 2015, pp. 1310–1321.   
[5] N. H. Tran, W. Bao, A. Zomaya, M. N. Nguyen, and C. S. Hong, “Federated learning over wireless networks: Optimization model design and analysis,” in IEEE INFOCOM 2019-IEEE Conference on Computer Communications. IEEE, 2019, pp. 1387–1395.   
[6] S. Wang, T. Tuor, T. Salonidis, K. K. Leung, C. Makaya, T. He, and K. Chan, “When edge meets learning: Adaptive control for resourceconstrained distributed machine learning,” in IEEE INFOCOM 2018- IEEE Conference on Computer Communications. IEEE, 2018, pp. 63– 71.   
[7] C. Song, T. Ristenpart, and V. Shmatikov, “Machine learning models that remember too much,” in Proceedings of the 2017 ACM SIGSAC Conference on computer and communications security, 2017, pp. 587– 601.   
[8] Z. Wang, M. Song, Z. Zhang, Y. Song, Q. Wang, and H. Qi, “Beyond inferring class representatives: User-level privacy leakage from federated learning,” in IEEE INFOCOM 2019-IEEE Conference on Computer Communications. IEEE, 2019, pp. 2512–2520.   
[9] A. Creswell, T. White, V. Dumoulin, K. Arulkumaran, B. Sengupta, and A. A. Bharath, “Generative adversarial networks: An overview,” IEEE Signal Processing Magazine, vol. 35, no. 1, pp. 53–65, 2018.   
[10] L. S. Shapley, 17. A value for n-person games. Princeton University Press, 2016.   
[11] R. B. Myerson, Game theory. Harvard university press, 2013.   
[12] A. Ghorbani and J. Zou, “Data shapley: Equitable valuation of data for machine learning,” in International Conference on Machine Learning. PMLR, 2019, pp. 2242–2251.   
[13] T. Song, Y. Tong, and S. Wei, “Profit allocation for federated learning,” in 2019 IEEE International Conference on Big Data (Big Data). IEEE, 2019, pp. 2577–2586.   
[14] R. Jia, D. Dao, B. Wang, F. A. Hubis, N. Hynes, N. M. Gurel, B. Li, ¨ C. Zhang, D. Song, and C. J. Spanos, “Towards efficient data valuation based on the shapley value,” in The 22nd International Conference on Artificial Intelligence and Statistics. PMLR, 2019, pp. 1167–1176.   
[15] J. Zhang, Y. Wu, and R. Pan, “Incentive mechanism for horizontal federated learning based on reputation and reverse auction,” in Proceedings of the Web Conference 2021, 2021, pp. 947–956.   
[16] X. Xu and L. Lyu, “Towards building a robust and fair federated learning system,” arXiv preprint arXiv:2011.10464, 2020.   
[17] Y. Sarikaya and O. Ercetin, “Motivating workers in federated learning: A stackelberg game perspective,” IEEE Networking Letters, vol. 2, no. 1, pp. 23–27, 2019.   
[18] L. Lyu, X. Xu, Q. Wang, and H. Yu, “Collaborative fairness in federated learning,” in Federated Learning. Springer, 2020, pp. 189–204.   
[19] X. Zhang, F. Li, Z. Zhang, Q. Li, C. Wang, and J. Wu, “Enabling execution assurance of federated learning at untrusted participants,” in IEEE INFOCOM 2020-IEEE Conference on Computer Communications. IEEE, 2020, pp. 1877–1886.   
[20] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial Intelligence and Statistics. PMLR, 2017, pp. 1273– 1282.   
[21] J. Kang, Z. Xiong, D. Niyato, D. Ye, D. I. Kim, and J. Zhao, “Toward secure blockchain-enabled internet of vehicles: Optimizing consensus management using reputation and contract theory,” IEEE Transactions on Vehicular Technology, vol. 68, no. 3, pp. 2906–2920, 2019.   
[22] Y. Liu, K. Li, Y. Jin, Y. Zhang, and W. Qu, “A novel reputation computation model based on subjective logic for mobile ad hoc networks,” Future Generation Computer Systems, vol. 27, no. 5, pp. 547–554, 2011.   
[23] J. Kang, R. Yu, X. Huang, M. Wu, S. Maharjan, S. Xie, and Y. Zhang, “Blockchain for secure and efficient data sharing in vehicular edge computing and networks,” IEEE Internet of Things Journal, vol. 6, no. 3, pp. 4660–4670, 2018.

[24] X. Huang, R. Yu, J. Kang, Z. Xia, and Y. Zhang, “Software defined networking for energy harvesting internet of things,” IEEE Internet of Things Journal, vol. 5, no. 3, pp. 1389–1399, 2018.   
[25] K. L. Huang, S. S. Kanhere, and W. Hu, “On the need for a reputation system in mobile phone based sensing,” Ad Hoc Networks, vol. 12, pp. 130–149, 2014.   
[26] X. Xu, L. Lyu, X. Ma, C. Miao, C. S. Foo, and B. K. H. Low, “Gradient driven rewards to guarantee fairness in collaborative machine learning,” Advances in Neural Information Processing Systems, vol. 34, 2021.   
[27] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.   
[28] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” 2009.   
[29] Y. Chen, “Convolutional neural network for sentence classification,” Master’s thesis, University of Waterloo, 2015.   
[30] Y. LeCun, B. Boser, J. Denker, D. Henderson, R. Howard, W. Hubbard, and L. Jackel, “Handwritten digit recognition with a back-propagation network,” Advances in neural information processing systems, vol. 2, 1989.   
[31] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification with deep convolutional neural networks,” Advances in neural information processing systems, vol. 25, pp. 1097–1105, 2012.   
[32] U. Michieli and M. Ozay, “Are all users treated fairly in federated learning systems?” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2021, pp. 2318–2322.   
[33] P. Kairouz, H. B. McMahan, B. Avent, A. Bellet, M. Bennis, A. N. Bhagoji, K. Bonawitz, Z. Charles, G. Cormode, R. Cummings, R. G. D’Oliveira, H. Eichner, S. E. Rouayheb, D. Evans, J. Gardner, Z. Garrett, A. Gascn, B. Ghazi, P. B. Gibbons, M. Gruteser, Z. Harchaoui, C. He, L. He, Z. Huo, B. Hutchinson, J. Hsu, M. Jaggi, T. Javidi, G. Joshi, M. Khodak, J. Konen, A. Korolova, F. Koushanfar, S. Koyejo, T. Lepoint, Y. Liu, P. Mittal, M. Mohri, R. Nock, A. zgr, R. Pagh, M. Raykova, H. Qi, D. Ramage, R. Raskar, D. Song, W. Song, S. U. Stich, Z. Sun, A. T. Suresh, F. Tramr, P. Vepakomma, J. Wang, L. Xiong, Z. Xu, Q. Yang, F. X. Yu, H. Yu, and S. Zhao, “Advances and open problems in federated learning,” Foundations and Trends in Machine Learning, vol. 14, no. 1-2, pp. 1–210, 2021.   
[34] D. Ye, R. Yu, M. Pan, and Z. Han, “Federated learning in vehicular edge computing: A selective model aggregation approach,” IEEE Access, vol. 8, pp. 23 920–23 935, 2020.   
[35] J. Kang, Z. Xiong, D. Niyato, S. Xie, and J. Zhang, “Incentive mechanism for reliable federated learning: A joint optimization approach to combining reputation and contract theory,” IEEE Internet of Things Journal, vol. 6, no. 6, pp. 10 700–10 714, 2019.   
[36] P. Bolton and M. Dewatripont, Contract theory. MIT press, 2004.   
[37] Y. Zhan, P. Li, Z. Qu, D. Zeng, and S. Guo, “A learning-based incentive mechanism for federated learning,” IEEE Internet of Things Journal, vol. 7, no. 7, pp. 6360–6368, 2020.

![](images/9117d8933da70084a162727dcf32b828831c30d3e6c78961ec3a20345908d9d8.jpg)



Zhuan Shi is currently a Ph.D student in the Department of Computer Science and Technology, University of Science and Technology of China, China. He received his B.S. degree in Soochow University in 2017. His research interests include mechanism Design, crowdsourcing and federated learning.

![](images/d1a5b713809cb1a4c217de9b340b8d8f70eafbd3ac5386ffb8ae09e3e788a41d.jpg)



Lan Zhang (Member, IEEE) is currently a Professor at the School of Computer Science and Technology, at University of Science and Technology of China. She received her Bachelor degree and Ph.D degree from Tsinghua University, China. Her research interests include mobile computing, privacy protection, and data sharing and trading

![](images/e043a8deec1fd57b175139638dbfb189e32e0b69d487085493751f63b71306d4.jpg)



Zhenyu Yao is currently a junior undergraduate in University of Liverpool. His research interests include federated learning, incentive mechanism and distributed system.

![](images/28b5390d2c87d26c0c5928661960fb72a93400d1bad017f6ecaa96f5eaaf7f94.jpg)



Lingjuan Lyu is currently a senior research scientist and team leader in Sony AI. She received her Ph.D. degree from the University of Melbourne in 2018. She was a winner of the IBM Fellowship program (50 winners Worldwide) and contributed to various professional activities. Her current research interest is trustworthy AI. She has publications in NeurIPS, ICLR, AAAIIJCAI, etc. Her paper won several best paper awards in top venues.

![](images/575e411ca5c8fbbed352b4f5978a76e04fc30c64afa280dabf41d1cb5646e88d.jpg)



Cen Chen is currently an associate professor at the School of Data Science and Engineering (DaSE), East China Normal University (ECNU), China. She received the Ph.D. degree from the School of Information Systems, Singapore Management University in 2017. She was a visiting scholar at Carnegie Mellon University from 2015 to 2016. She has published 40+ papers in top international conferences and journals, such as WWW, AAAI, IJCAI, SIGIR, INFOCOM, etc. Her current research interests include privacy-

preserving machine learning and NLP applications.

![](images/ce21ec86c38bfd4c68b847c4f004869eb177b623e4ef8753aadc3923fb6d26f0.jpg)



Li Wang is currently an Algorithm Expert at AI Department, Ant Financial. He got his master degree in Computer Science and Technology at Shanghai Jiao Tong University in 2010. His research mainly focuses on privacy preserving machine learning, transfer learning, graph representation, and distributed machine learning.

![](images/f10d1d1575f823dc26687693749db3132d56a58fc8ccf8118c2a4dcebe5ea359.jpg)



Junhao Wang is a Master student in Computer Science at University Of Science and Technology Of China. He received his B.E. degree in Computer Science and Technology from Xian Jiaotong University, China, in 2019. His research interests include robustness and safety in federated learning.

![](images/c7ebe397b367d38f3cc5b893ea2467062f53c0f282463bdd4d9e4942a5ddc35f.jpg)



Xiang-Yang Li (Fellow, IEEE) received the bachelors degree from the Department of Computer Science and the second bachelors degree from the Department of Business Management, Tsinghua University, P.R. China, both in 1995, and the MS and PhD degrees from the Department of Computer Science, University of Illinois at UrbanaChampaign, Champaign, Illinois, 2000, 2001, respectively. He is currently a professor and executive dean at the School of Computer Science and Technology, University of Science

and Technology of China, Hefei, China. He is an ACM Fellow. He was a professor with the Illinois Institute of Technology, Chicago, Illinois. His research interests include wireless networking, mobile computing, security and privacy, cyber physical systems, and data sharing. He has won several best paper awards and Best Demo Award.