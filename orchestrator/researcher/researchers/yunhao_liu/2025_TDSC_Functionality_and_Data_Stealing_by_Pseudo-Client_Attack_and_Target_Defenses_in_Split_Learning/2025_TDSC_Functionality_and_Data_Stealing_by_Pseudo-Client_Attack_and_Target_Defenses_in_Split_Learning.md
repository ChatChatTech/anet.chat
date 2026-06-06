# Functionality and Data Stealing by Pseudo-Client Attack and Target Defenses in Split Learning

Lan Zhang , Xinben Gao , Yaliang Li , and Yunhao Liu , Fellow, IEEE

Abstract—Split learning (SL) aims to protect a client’s data by splitting up a neural network among the client and the server. Previous efforts have shown that a semi-honest server can conduct a model inversion attack. However, those attacks require the knowledge of the client network structure, and the performance deteriorates dramatically as the client network gets deeper (≥ 2 layers). In this work, we explore the attack in a more general and challenging situation where the client model is unknown and more complex. We unveil the inherent privacy leakage through a series of intermediate server models during SL, and propose a new attack on SL: Pseudo-Client ATtack (PCAT). To the best of our knowledge, this is the first attack for a semi-honest server to steal clients’ functionality, reconstruct private inputs and labels without any knowledge about the clients’ network structure. Moreover, the attack is transparent to clients. Extensive experiments demonstrate that our attack outperforms previous works in scenarios involving more complex models and learning tasks, even in non-i.i.d. settings and confronted with conventional defensive measures. We further explore novel defense mechanisms to mitigate PCAT and improve our attack to counteract the potential defenses.

Index Terms—Privacy attacks, privacy defenses, split learning.

# I. INTRODUCTION

HE last decade has seen the flourishing and widespread adoption of deep neural networks (DNNs). Split learning (SL) is an emerging learning paradigm proposed to enable a data owner with constrained computing resources or sensitive data to train a large model with a powerful server cooperatively [1], [2], [3], [4], [5], [6], [7], [8], [9]. It splits a DNN into a client model and a server model, and the client only needs to perform lightweight computations and output intermediate layer activations (named “smashed data”) instead of raw data. Since the server doesn’t have access to the client-side model and inputs,

Manuscript received 18 October 2023; revised 10 March 2024; accepted 1 April 2024. Date of publication 15 April 2024; date of current version 16 January 2025. This work was supported in part by the National Key R&D Program of China under Grant 2021YFB2900103, in part by China National Natural Science Foundation under Grant 61932016, in part by “the Fundamental Research Funds for the Central Universities” under Grant WK2150110024. (Corresponding author: Lan Zhang.)

Lan Zhang and Xinben Gao are with the School of Computer Science and Technology, University of Science and Technology of China, Hefei 230026, China (e-mail: zhanglan@ustc.edu.cn; gxb1320276347@mail.ustc.edu.cn).

Yaliang Li is with the DAMO Academy, Alibaba Group, Bellevue, WA 98004 USA (e-mail: yaliang.li@alibaba-inc.com).

Yunhao Liu is with the Tsinghua University, Beijing 100080, China (e-mail: yunhao@tsinghua.edu.cn).

This article has supplementary downloadable material available at https://doi.org/10.1109/TDSC.2024.3387396, provided by the authors.

Digital Object Identifier 10.1109/TDSC.2024.3387396

SL is considered to be capable of protecting the functionality of the client model and the privacy of inputs from stealing.

In many application areas, like healthcare and finance [10], [11], [12], [13], the data and labels from clients can be valuable and sensitive, and AI services built on these data are often very lucrative. Therefore, attackers and even the server have a strong incentive to steal the sensitive data and functionality of the client model. In addition to the unauthorized acquisition of private data, the compromising of the client model serves as a substantial target for attack. Deviating from conventional attacks that primarily aim at illicitly reconstructing model parameters, the focus has shifted towards a more feasible target – stealing model functionalities. It solely necessitates the attacker’s model to obtain functions similar to those of the target model rather than the need for alignment on the parameter level– for instance, executing identical classification tasks, accomplishing the same mapping, and so forth. In scenarios where a computation provider (the server) and a data provider (the client) collaborate to train a SL model for profit, stealing the functionality of the client model allows the server to get rid of the client and perform the inference on its own without sharing the revenue earned by the SL model. Some recent works [14], [15], [16] have presented a series of attacks on SL. Feature-space hijacking attack (FSHA) [16], [17] points out that the server can hijack clients to uncover private inputs, but this server is malicious since it completely disrupts the process of SL, making this attack detectable by clients [18]. Besides, the server can’t steal the functionality of the client model due to the damaged SL model. While instigating a malicious attack may have detrimental effects on a server’s reputation due to the potential of client detection, the server tends to play a semi-honest role. A semi-honest server, also referred to as an honest-but-curious server, can gather, preserve, and process all the data exposed to it while executing in strict adherence to the protocol throughout the execution. UnSplit [15] is the state-of-the-art attack designed for a semi-honest server, which requires the knowledge of client model structure and the smashed data to reconstruct the client model and raw inputs. It uses a coordinate gradient descent approach to search over the space consisting of all possible input values and client network’s parameters, which is too large to converge. Once the learning task and the client model become slightly complex, its performance deteriorates dramatically and the attack fails. As for label inference attack, UnSplit [15] only works under the strong assumption that the client top model has only one layers (see Table VIII). In short, for a semi-honest server, existing attacks on SL mainly based on the idea of model inversion, which requires the knowledge of the client model structure and could fail due to the large search space as the client model gets deeper and more complex. Therefore, how to effectively steal the functionality, inputs and labels of the client in an undetectable way, even if the client model’s structure is unknown and complex, is still an open question.

To explore the answer to this question, in this work, we propose a novel and widely effective attack paradigm — Pseudo-Client ATtack (PCAT), to steal the functionality and data from the client. As aforementioned, conventional attacks first obtain smashed data and client model structure, and then invert the client model. Differently, the effectiveness of PCAT is based on our insights that a well-trained server model itself can provide sufficient information to construct a pseudo-client model to steal client’s functionality by using very limited training samples, even without using the smashed data. Moreover, we discover that a series of intermediate server models during normal SL can provide extra knowledge to the pseudo-client model to gain closer functionality. With these insights, our main idea is that the server can take full use of the knowledge learned by evolving server models to train a pseudo-client model to gain a functionality as close to that of the real client as possible, whose structure can be completely different from that of the real client model. Hence, PCAT doesn’t require any knowledge about the real client model. The only assumption is that the server can obtain a small dataset of few samples for the same learning task from any public sources, whose size is orders of magnitude smaller than the private training set. Once the pseudo-client model learns a mapping from inputs to the feature space of smashed data, the server can transform the given smashed data back to raw inputs by learning a reverse mapping. It is also able to replace the top model by a pseudo-top model to infer private labels.

The experiments show that the functionality stealing attack is highly resistant to traditional defense such as DP [19] mechanisms. Therefore, we undertake an investigation into targeted defense mechanisms against PCAT. The crux of our functionality stealing attack is on the similarity between the input-label pairs of the attacker and the victim client, allowing the attacker obtain a functionality closed to the victim model’s. Our defense strategy involves the victim claiming a counterfeit learning task, resulting an inconsistency between the attacker’s and the victim’s learning tasks, breaking the similarity between their input-label pairs, and thwarting the attacker’s ability to steal the victim’s model’s functionality. Moreover, we should ensure the victim client can convert the inference made under the claimed learning task into an inference under the real learning task during the prediction phase. We employ two methods: a one-to-one mapping technique and an autoencoder approach for generating the claimed learning task. Our experimental results have demonstrated that our defense mechanism can significantly destroy the performance of attack while safeguarding the performance of the SL baseline.

Furthermore, we improves PCAT to maintain its effectiveness under this specific defense mechanism. To alleviate the constraints of the server’s top model on the learning task, we introduce a pseudo-top model in place of the real top model. This enables the pseudo-top model to map the inputs of the real top model to the label space that is known by the server.

The main contributions of this paper are summarized as follows:

New attack: We propose a novel pseudo-client attack on SL, which, to the best of our knowledge, is the first attack enabling a semi-honest server to achieve three goals — functionality stealing, input data reconstruction and labels inference, without any preknowledge about the client model. Compared with previous attacks on ${ \mathrm { S L } } ,$ our attack has the following advantages: 1) It is widely effective since it suits all variants of SL and doesn’t require any knowledge of the client model; 2) It is effective in cases with more complex tasks and client models; 3) It is hard to detect since it’s transparent to clients; 4) Our functionality stealing attack doesn’t require smashed data, thus it is robust even if clients use defensive mechanisms.

New insights: We provide the insights that a server model in SL contains rich private information, though it doesn’t have access to any private data directly. A trained server model can be utilized to construct a pseudo-client model to gain the functionality of the real client, even without using any smashed data. Moreover, a series of intermediate server models can “guide” the pseudo-client model to reach a better performance. Thus, on the basis of the insights, we design PCAT that significantly outperforms state-of-the-art attacks in three attack goals. Our successful attacks also reveal the high risk of leaking privacy through the server model in SL, even when the client model structure and smashed data are protected.

New results: We implement PCAT on various benchmark datasets and models to verify its effectiveness. The results show that the server can use a very small dataset to gain a pseudo-client model whose functionality is very close to the real client. Our attack is also robust to non-i.i.d. situations when the server lacks training samples of some classes, as well as traditional defences.

New defenses: We introduce two label transformation defenses targeted to thwart PCAT. Compared with traditional defense mechanisms like differential privacy, these defenses not only mitigate the reduction in the accuracy of the SL baseline but also counter basic PCAT effectively. Therefore, we further improve PCAT to counter these two defense mechanisms.

# II. PRELIMINARIES AND RELATED WORK

# A. Split Learning

As a rising paradigm of distributed machine learning [20], split learning (SL) [4], [6], [7] is proposed for resourceconstrained data owners by letting the powerful server undertake the majority of computation. In SL, the ML model (usually a neural network) is split into several parts. Without loss of generality, the model is partitioned to a server model $( f _ { s } )$ and a client model $( f _ { c } )$ , and the function of the whole model is $f = f _ { s } ( f _ { c } ( \cdot ) )$ . The client model is allocated to the data owners, and the server model is at the place concentrating sufficient computing power. During the overall training phase, the server should be oblivious to any private information of the client.

There are three typical settings for SL [3], [4], [7], as presented in Fig. 1. In the single-client setting, the client transmits smashed data $( f _ { c } ( X ) )$ and labels to the server, and the server computes loss and gradients. Then the server performs backward propagation and sends gradients back to the client. Receiving the gradients, the client performs backward propagation, and both the server and client update their weights. It iterates in this way until the model converges. For the multi-client setting, the clients take part in training in a round-robin sequence. Each client updates its local model from the last client before training. As for the U-shape setting, a top model is split out and assigned to clients to protect private labels and clients need to calculate the loss.

![](images/c76a25251d2e658a26cd9fe1e1564a1f3e61315e8e746c5326389bdd371a7bdd.jpg)



Fig. 1. Three typical variants of SL [3], [4]. Our attack mechanism is effective against all three variants.

# B. Attacks on Split Learning

Currently, a significant amount of research is dedicated to investigating machine learning attacks [21]. In SL, recently, several attacks [14], [15], [16], [22] are designed for the server to reconstruct the clients’ raw inputs, model parameters and labels. In FSHA [16], a malicious server can hijack clients to leak essential features about their raw data. However, due to that the server changes the learning task and disrupts the learning process, the malicious behaviors can be detected by clients [18] and the attacker can not steal clients’ functionality. UnSplit [15] provides the state-of-the-art attack on SL based on the assumption that the server has the client’s model structure, and a semi-honest server can reconstruct the raw inputs and parameters of the clients’ model by utilizing the smashed data. Since both the model parameters and the inputs are unknown, the solution space could be too large to converge once the client’s model or the learning task becomes more complex. Therefore, in practice this attack can easily fail when any of the following situations occur: 1) the structure of the client model is unknown; 2) the client model has more than one layer; 3) the learning task is complex; 4) the smashed data is protected by defense mechanism like differential privacy [19]. When attacking the U-shape SL, both norm-based label-uncovering method [22] and UnSplit [15] use gradients information to reconstruct private labels. However, these two attacks are only effective for the imbalanced binary classification setting or the setting where the top model contains only one layer.

As a summary, existing attacks on SL mainly based on the idea of model inversion, which inherently suffer from the large search space of both possible inputs and client model parameters. Therefore, those attacks are only effective on simple tasks and client models. In this work we consider a more general and challenging problem: how to steal the functionality and data of the client model in an oblivious way when the structure of the client model is unknown, tasks and client models are more complex, and the client may even use some defensive methods to protect the smashed data.

# III. GOAL AND MAIN IDEA

# A. Goals and Settings

In this work, we aim to design an attack mechanism on SL, which supports a semi-honest server to perform all three attacks in strict adherence to the protocol: 1) steal functionality of the client model; 2) reconstruct the client’s raw inputs; 3) infer labels of the client’s inputs. To make the attack mechanism widely effective, we design our mechanism to meet the following requirements.

(1) Minimal knowledge about the client model: the server knows the learning task but it doesn’t need to know the structure or hyper parameters of the client model. For the functionality stealing, the sever doesn’t even need to use the smashed data, thus existing defense to protect the smashed data doesn’t work.   
(2) Support more complex client models and tasks: existing methods [15], [22] support only simple tasks, like imbalanced binary classification and handwritten digits classification, and simple client models with only one layer. Differently, our mechanism should support more complex tasks, as well as deeper and wider client models.   
(3) Effective against three variants of SL: as shown in Fig. 1, there are three typical variants of SL. Our attack mechanism should be effective against all of them.   
(4) Transparent to the client: the server is semi-honest, and in the client’s view, the training process with an attack is indistinguishable from a normal training without an attack.

The assumptions for PCAT are that: 1) Both server and client are semi-honest, which follow the SL protocol, but the server is curious about the client’s model, inputs and labels. 2) The server doesn’t known anything bout the client model structure. 3) The server can collect a limited number of training samples (about 0.1%-5% of the private dataset, noted as $X _ { s e r v e r } )$ for the same learning task from public sources. As the default setting in SL protocols, the server and the client use the same optimizer.

# B. Insights and Main Ideas

To achieve aforementioned ambitious goals, the major challenge stems from the fact that the server does not know anything about the client model when conducting functionality stealing. This challenge makes all previous query based and model inversion based attacks inapplicable. Therefore, we turn to explore what the server model learns and whether it can be utilized to construct a pseudo-client model, whose functionality is very similar to the real client model. To find the answer, we start by investigating how to steal the functionality of a complete model, followed by the idea to steal the client model in SL.

# (1) Steal a Complete Model

![](images/96d64c76f07f2abfb3ee4035ce4877f979a93a0387f3c82e9fe1189ce7acb551.jpg)



Fig. 2. Two strategies to construct a pseudo model f which steals the functionality of the victim model F . F is trained on a large dataset $D a t a _ { \rfloor }$ L and f is trained on a small dataset DataS with the help of F . N is the total number of iterations during training and n $\in [ 0 , N ]$ . That is, $F ^ { n }$ denotes the model after n iterations and $\check { F } ^ { N }$ denotes the final model after training. Before calculating LKLDiv, we need to perform log(sof tmax(pred/τ )) and τ is temperature [23].

Considering a model with a sufficiently large dataset as the victim model, denoted by $F ,$ the functionality stealing attack tries to construct a knockoff model using a small dataset, denoted by ${ \widetilde { f } } ,$ which behaves very much like $F .$ . The most critical challenge is how to let F effectively teach $\widetilde { f }$ when the attacker has very limited training data.

Basic strategy: stealing after training. A basic solution is to train the victim model first, then let the victim model teach the knockoff model in the way of knowledge distillation [23]. As presented in Fig. 2(a) and (b), after training the victim model for N iterations on a large dataset, we obtain a well-trained model $F ^ { N }$ . Then the knockoff model $\widetilde { f }$ can be trained with the help of $F ^ { N }$ in the following way: in the nth iteration, the inputs $( X _ { i } ^ { n } )$ from a small dataset are fed to both models, and the learning targets of $\widetilde { f }$ are the output soft labels of $F ^ { N }$ rather than the hard labels. The loss function is

$$
\mathcal {L} _ {K L D i v} = K L D i v e r g e n c e L o s s \left(\text { soft } \left(\widetilde {\text { pred }} _ {i} ^ {n}\right), \text { soft } \left(\text { pred } _ {i} ^ {N}\right)\right), \tag {1}
$$

which is the KL divergence loss between the soft labels of two models.

By learning from the victim model, the performance of the knockoff model can often be obviously improved, e.g., from 73.52% to 82.06% in the handwritten digits classification task in Fig. 4(a), when the attacker has only 100 training samples (10 samples per class). However, there is still a significant gap from the performance of the victim model, which is 98.82%.

Our improved strategy: stealing while training. To further improve the performance of the knockoff model, we have the observation that a series of intermediate victim models during training can provide essential information, which can teach the knockoff model better than the final well-trained victim model does. Based on this observation, different from traditional knowledge distillation, we propose to steal the victim model while it is being trained. As illustrated in Fig. 2(c), in the nth iteration, taking the same inputs from the small dataset, the optimization objective of ${ \widetilde { f } } ^ { n }$ is to minimize the KL divergence loss between the output soft labels of two current models. Note that, $F ^ { n }$ also takes inputs from the large dataset, and its optimization objective remains the loss on the hard labels. In this way, both $F ^ { n }$ and ${ \widetilde { f } } ^ { n }$ are trained synchronously. $F ^ { n }$ evolves by using the large dataset, while ${ \widetilde { f } } ^ { n }$ uses a sequence of evolving targets to train itself. Although at the beginning, learning targets are not as accurate as the final target, actually the evolving learning targets can “guide” ${ \widetilde { f } } ^ { n }$ to converge more precisely to the final target. As plotted in Fig. 4(a) and (b), our stealing while training strategy increases the accuracy of the knockoff model to 88.44%, which is significantly higher than the basic stealing after training strategy.

![](images/b9a124e9f3e217500260728681c5591fb845f33afc70547b8ff0227557c1e933.jpg)



Fig. 3. Two strategies to steal the client model in SL. (a) shows training two SL models on small( $D a t a _ { S } )$ and large(DataL) datasets independently. (b) and (c) illustrate the strategies that train a pseudo-client model $\widetilde { f _ { c } }$ to steal the functionality of the victim client model $F _ { c } { ^ { - } }$ after and while training the server model, separately. $n \in [ 0 , N ] , F _ { s } ^ { N }$ denotes the final server model after SL and $F _ { s } ^ { n }$ denotes the intermediate server model after n iterations during the ${ \mathrm { S L } } , { \mathcal { F } }$ is the feature space of the smashed data. The red arrows indicate that under the restriction of $F _ { s } ^ { N }$ or $F _ { s } ^ { n }$ , the feature space of the pseudo-client’s outputs is learning to get closed to the feature space of the victim client’s outputs.

# (2) Steal a Client Model in Split Learning

The aforementioned strategies cannot be directly applied to steal a client model in SL. Different from stealing a complete model, to construct a pseudo-client model, we still need to address the following challenges: 1) the server cannot obtain the intermediate client models during training, but only knows all intermediate server models; 2) the server cannot obtain the inputs nor the output soft labels, and even the smashed data cannot be used as aforementioned in Section III-A; 3) the server cannot even feed samples from its small dataset to the client model, otherwise the client will be aware of the attack.

Facing these challenges, w.l.o.g., we further analyze the single-client SL. As illustrated in Fig. 3(a), the client model maps raw inputs X to a certain feature space $\mathcal { F }$ . Then the server model maps intermediate activation from this feature space to logits. The SL model trained on a large dataset, denoted by $F = F _ { s } ( F _ { c } ( \cdot ) )$ ), usually performs much better than the SL model trained on a small dataset, denoted by $f = f _ { s } ( f _ { c } ( \cdot ) )$ ). As shown in Fig. 4(c), with 60,000 training samples, the SL model achieves 99.18%, while the accuracy is only 51.33% with 10 training samples (1 sample per class). Since the server aims to construct a pseudo model with good performance, it must make full use of the knowledge in the client’s large dataset. Therefore, we propose to steal the functionality of the client model by using only the server model(s) trained on the client’s dataset and a small dataset from the server itself. As we will present below, such strategies work surprisingly well, even though the server does not know the structure or input of the client model and does not query the client or use the smashed data at all.

Our basic strategy for SL: stealing client after training server. As illustrated in Fig. 3(b), the server conducts the normal SL first. After N iterations, the input X is mapped to the feature space $\mathcal { F } ^ { N }$ by the victim client model $F _ { c } ^ { N }$ . The server model F N $\bar { F } _ { \mathrm { ~ s ~ } } ^ { N }$ s is well-trained and capable to convert the smashed data in $\overset { \circ } { \mathcal { F } ^ { N } }$ to logits. Now the server can connect a pseudo-client model $( \widetilde { f } _ { c } )$ to the trained server model $F _ { s } ^ { N }$ , and use its small dataset to train $( \widetilde { f } _ { c } )$ while fixing the parameters of $F _ { s } ^ { N }$ . The pseudo-client model actually maps inputs to another feature space $\widetilde { \mathcal { F } } ^ { N }$ . To steal the functionality of the victim client model $F _ { c } ^ { \bar { N } }$ , the training algorithm for the pseudo-client model should optimize its output smashed data as close to $\mathcal { F } ^ { N }$ as possible, so that the smashed data can be classified by the server model correctly. The detailed training algorithm is presented in Algorithm 1. Note that, it is not necessary for $\widetilde { f } _ { c }$ to have the same structure as the victim client model $( F _ { c } )$ , as long as it can learn the mapping from raw inputs the to feature space. The experimental results in Fig. 4(c) and (d) show that, this strategy can increase the accuracy of the server’s pseudo model from 51.33% to 83.05% when the server has only 10 samples.

![](images/61821aa5e7def8a3f6ffd74646669a65627af62a7339960bc3e7f7c46a877910.jpg)



![](images/6c3d12afbd9f6bd4c534d5ad3b367201638132d9b3b68ff2d5ac92db89f8c742.jpg)



![](images/916eecabfc6b0753fc34ac3c5be5378d48024ecffece468ed6105d7a198b6428.jpg)



![](images/904ca6a129c2cb8e1256df0a8dda5f1517d8a73f83a48e1021c9f6ca1b0396a7.jpg)



Fig. 4. Performance of victim models and pseudo models obtained by different strategies. It uses LeNet-5 on MNIST dataset. (a) and (b) show the performancewhen stealing a complete model after and while the training of the victim model. (c) and (d) show the performance when stealing a client model after and while the training of the server model in SL. The split layer is 2. MSELoss is calculated between the smashed data output by the client model and the pseudo-client model, which characterizes the difference between $\overbrace { \mathcal { F } ^ { N } }$ and $\mathcal { F } ^ { N }$ . 60000, 100 are the amounts of training samples.

Algorithm 1: Stealing Client After Training Server (Vanilla-PCAT).   
Data: Server's data: $(X_{server},y_{server})$ , total epochs: $N$ /* Initialize models */ $F_s^N$ is a well-trained server model; $\widetilde{f}_c$ is randomly initialized;  
while $n < N$ do  
    Randomly select $(X_i,y_i)$ from $(X_{server},y_{server})$ ; $\widetilde{smashed} \leftarrow \widetilde{f_c}(X_i)$ ; $\widetilde{z} \leftarrow F_s(smashed)$ ; $\widetilde{\mathcal{L}} \leftarrow \mathcal{L}(\widetilde{z},y_i)$ ; $\widetilde{\nabla}_{smashed} \leftarrow \text{compute\_gradient}(smashed,\widetilde{\mathcal{L}})$ ; $\widetilde{\nabla}_c \leftarrow \text{compute\_gradient}(\widetilde{f}_c,\widetilde{\nabla}_{smashed})$ ; $\widetilde{f}_c' \leftarrow \text{update\_weight}(\widetilde{f}_c,\widetilde{\nabla}_c)$ ;  
    /* The weight of $F_s$ isn't updated. */  
end

Our advanced strategy for SL: stealing client while training server. Similar to the advanced strategy when stealing a complete model, we find that using a sequence of intermediate server models $F _ { s } ^ { n } , n \in [ 0 , N ]$ during SL, the server can train the pseudoclient model gradually to achieve better performance. In another words, the pseudo-client model can leverage a series of learning targets $\{ \bar { \mathcal { F } } ^ { 0 } , . . . , \mathcal { F } ^ { N } \}$ to steal the functionality more accurately. This strategy is feasible since the server knows the intermediate server model for every iteration. Fig. 4(c) testifies that using evolving server models can greatly improve the pseudo-client model’s accuracy, from 83.05% to 90.7% in our experiments. Fig. 4(d) further illustrates that the adversarial feature space $\widetilde { \mathcal { F } } ^ { N }$ is very close to the victim feature space $\mathcal { F } ^ { N }$ by this strategy. Note that, without the constraints from the well-trained server models, the feature space of smashed data in an independently trained pseudo model is quite far away from the victim feature space $\dot { \mathcal { F } } ^ { N }$ . Comparied with the basic strategy - stealing after training, this strategy leads to a narrow time window to perform the attack. However, saving the parameters of the server model in each iteration of the split learning baseline can extend the attack time window, accompanied with generating huge storage overhead.

Summaries: We have insights that a server model trained by standard SL can provide sufficient knowledge to train a well-performing pseudo-client model using very limited training samples; a series of intermediate server models during SL can significantly improve its accuracy. These insights not only inspire us to design a highly effective attack mechanism against SL, but also reveal the privacy threats posed by the server model in SL. Based on these insights, our main idea to steal the functionality of the client model is to train a pseudo-client model with any structure that can map inputs X to the target feature space $\dot { \mathcal { F } } ^ { N }$ . Once the pseudo feature space $\widetilde { \mathcal { F } } ^ { N }$ is sufficiently close to $\mathcal { F } ^ { N }$ , the pseudo-client model can take place of the victim client model. Then, using the pseudo-client model and smashed data of client’s inputs, the server can reconstruct the private inputs of the client by learning a reverse mapping, as well as infer their labels.

# IV. PSEUDO-CLIENT ATTACK

In this section, following our main idea, we present the detailed design of our attack mechanism, the Pseudo-Client ATtack (PCAT), on different variants of SL. The whole attack process is illustrated in Fig. 5. We also present some details that makes PCAT more effective.

![](images/e88068c86243293b97d9ba0e3d49b82e7be104cdc8979a3a87e5abd858cee4dc.jpg)



Fig. 5. Pseudo-client attack in two-part SL and U-Shape SL. The server constructs a pseudo-client mode $\widehat { f _ { c } } ^ { N }$ by the PCAT algorithm. $\mathrm { W i t h } \widetilde { \boldsymbol { f _ { c } } } ^ { N }$ , the server can perform inference without the involvement of the victim client. During the normal SL, the server stores smashed data (denoted as $X _ { s m a s h e d } )$ of the victim client. Using fc  , the server can train an reverse mapping $f ^ { - 1 }$ and reconstruct the client’s private inputs $X _ { p r i v }$ in two steps.

# A. Functionality Stealing

Algorithm 1 has already illustrated how to train a pseudoclient model after the server model has been trained in a normal SL. To further improve the performance of the pseudo-client model, our insights guide us to take full use of a series of intermediate server models. Specifically, the server initializes the pseudo-client model before the SL starts and then trains both pseudo and real client models simultaneously. For each iteration, the victim client performs its forward propagation and sends the smashed data and labels to the server. Then the server selects training samples from its own dataset with the same labels as those uploaded by the client, i.e., $y _ { s e r v e r } = y _ { p r i v } .$ , and feeds these samples into the pseudo-client model to obtain the smashed data. For both pseudo and victim client models, the server model takes their respective smashed data as input, performs forward propagation and calculates the loss, separately. For SL, the server computes the gradients of smashed data and sends the gradients back to the victim client. The victim client calculates the local gradients and updates the client model. For pseudo-client training, based on the loss, the server calculates the gradients of its own smashed data and the pseudo-client model, with which the pseudo-client model is updated. At the end of each iteration, the server model is updated using only the gradients from normal SL with the victim client. Algorithm 2 presents the details of the attack process. Since both the victim client model and the server model are updated based on only the gradients of normal SL, the whole training process is the same as a normal SL in the client’s view. Therefore, this attack is transparent to clients.

In multi-client SL, each client participates in a round-robin mode to train the client model, so all clients obtain the same client model after SL. From the server’s perspective, the evolution of the server and client model is the same as that in singleclient SL. Therefore, the server can apply PCAT to multi-client SL directly without any modification.

# B. Inputs Reconstruction

After stealing the functionality, the server obtains a pseudoclient model that maps inputs to a feature space of smashed data, which is very close to the real feature space in SL. Given smashed data from the victim client $( X _ { s m a s h e d } )$ , the server can reconstruct the private raw inputs $( X _ { p r i v } )$ by reversing the mapping. As presented in Fig. 5, we propose to reconstruct the client’s inputs using the following steps:

1) Train a reverse mapping $f ^ { - 1 } { : }$ : since the server has a few training samples, it can train a reverse mapping $f ^ { - 1 }$ to map smashed data from the feature space back to the input space. Specifically, the server maps raw training samples to smashed data by using the pseudo-client model, then trains $f ^ { - 1 }$ to map them back to raw inputs. The reverse mapping is composed of transposed convolution and upsample layers to transfer smashed data from low resolution to high resolution. The specific reverse mapping we use for every model splitting is shown in Appendix, available online.   
2) Coarse-grained reconstruction and fine-tuning: the server can feed $X _ { s m a s h e d }$ into $f ^ { - 1 }$ to obtain the reconstructed inputs $X _ { r e c } )$ . However, due to the insufficient training samples in server, $X _ { r e c }$ is usually coarse-grained. To achieve more precise reconstruction, we design a fine-tuning method which takes the coarse-grained $X _ { r e c }$ from $f ^ { - 1 }$ as inputs and the real smashed data $X _ { s m a s h e d }$ as learning targets. Towards the targets, the server optimizes and fine tunes $X _ { r e c }$ with fixed pseudo-client model $\widetilde { f } _ { c } ^ { N }$ , until the output smashed data of $\widetilde { f } _ { c } ^ { N }$ is close enough to $X _ { s m a s h e d } .$ In this way, we can obtain a more fine-grained reconstruction.

Note that, we steal the functionality of the client model in a totally different way from UnSplit, thus the input reconstruction is also different from UnSplit. Specifically, UnSplit adopts the client model structure and smashed data to search the client model parameters and inputs simultaneously. While PCAT first learns a pseudo-client model using only the server model and a small training dataset of the server, and then learns a reverse mapping with the server’s training data. The smashed data are used for fine-tuning. Since PCAT reconstructs the inputs after the pseudo-client model is well constructed, the search space is significantly smaller than that of the UnSplit. Our experiments verify that PCAT reconstructs raw inputs more precisely than UnSplit.

Algorithm 2: Stealing Client While Training Server (PCAT).   
Data: Server's data: $(X_{server},y_{server})$ , Client's data: $(X_{priv},y_{priv})$ , epochs: $N$ / $\star$ Initiate models $\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad$ $F_s,F_c,\widetilde{f}_c$ are all randomly initialized and $F_{c}\neq \widetilde{f}_{c}$ ;

For the client:   
while n < N do
    Randomly select $(X_{j}, y_{j})$ from $(X_{priv}, y_{priv})$ ;
    Smashed ← $F_{c}(X_{j})$ ;
    send_to_server(Smashed, $y_{j}$ );
    recv_from_server( $\nabla_{Smashed}$ ); $\nabla_{c} \leftarrow \text{compute\_gradient}(F_{c}, \nabla_{Smashed})$ ; $F_{c}' \leftarrow \text{update\_weight}(F_{c}, \nabla_{c})$ ;   
end

For the server:   
while n < N do
    recv_from_client(Smashed, y_j);
    Select X_i from X_server so that y_i = y_j
    // Align labels
    Smashed ← f_c(X_i);
    z ← F_s(Smashed);
    z ← F_s(Smashed);
    L ← L(z, y_i);
    L ← L(z, y_j);
    ∇_s ← compute_gradient(F_s, L);
    Smashed ← compute_gradient(Smashed, L);
    Smashed ← compute_gradient(Smashed, L);
    ∇_c ← compute_gradient(f_c, ∇_Smashed);
    f_c ← update_weight(f_c, ∇_c);
    send_to_client(∇_Smashed);
    F_s' ← update_weight(F_s, ∇_s);
    // F_s updates weight using grad from SL.   
end

# C. Attack on U-Shape Split Learning

In U-shape SL, as shown in Fig. 5, there are a bottom model $F _ { c }$ and a top model $F _ { t }$ placed on the client side. The server needs to train a pseudo-client model $\widetilde { f } _ { c }$ as well as a pseudo-top model $\widetilde { f } _ { t }$ . By using the same strategy in two-part SL (i.e., Algorithm 2), the server can obtain $\widetilde { f } _ { c } ^ { ~ N }$ and $\boldsymbol { \widetilde { f } } _ { t } ^ { N }$ and perform inference alone. With $\widetilde { f } _ { c } ^ { ~ N }$ , the private inputs of the client can also be reconstructed by the methods in Section IV-B.

Unlike two-part SL where clients send data labels to the server, in U-shape SL labels are considered as privacy and protected from the server by the top model. Since PCAT can construct a

![](images/e4ef45abe12dd8ca8dfd612934ca424a20e178de03fab177dd757add5a428c5b.jpg)



Fig. 6. Functionality gap between the pseudo model and the victim model, which is measured by the inference accuracy decrease of $\widetilde { F _ { s } ( f _ { c } ( \cdot ) ) }$ compared with $F _ { s } ( f _ { c } ( \cdot ) )$ . The experiment is performed on MNIST and CIFAR-10 dataset.The inference accuracy of the baseline $F _ { s } ( f _ { c } ( \cdot ) )$ is 99%/93.2% for MNIST/CIFAR-10.“Samples/Class” means the number of samples per class in the server’s dataset.

pseudo-top model to replace the real top model, the server can feed smashed data of the victim client to the pseudo-top model to infer their private labels.

# D. Other Details to Improve PCAT

1) Aligning Labels: When attacking two-part SL by Algorithm 2, the server aligns labels of the training samples for the pseudo and victim client models, i.e., to make $y _ { s e r v e r } =$ $y _ { p r i v } .$ . For the attack on U-shape SL, due to the invisibility of the client’s labels, the server randomly selects $X _ { s e r v e r }$ for each iteration. We measure the functionality of the pseudo-client model with and without label alignment. Fig. 6 shows that the inference accuracy gap between the pseudo model $F _ { s } ( \widetilde { f } _ { c } ( \cdot ) )$ ) and the victim model $F _ { s } ( f _ { c } ( \cdot ) )$ is only 1.09%/1.95% with/without label alignment on MNIST and 6.01%/9.06% on CIFAR-10, when there are 25/100 samples per class in the server’s dataset. The results testify that PCAT can steal the functionality of the victim model with high accuracy; and label alignment can increase the pseudo-client model’s accuracy. We believe the reason is that the gradients of pseudo and victim client models depend in their respective inputs and labels. Aligned training samples can make the gradients of two client models closer, thus the optimization directions of $F _ { s }$ and $\widetilde { f _ { c } }$ are more consistent.

2) Late Start: In the early stages of SL, since the victim model hasn’t started to converge, the unstable server model could guide the pseudo-client model to a wrong direction. Thus, the pseudo-client model can skip some batches in the early stages to avoid being misled and gain a better performance. The experiment results in Fig. 7 show that a proper late start can improve the performance of the pseudo model. For example, when the pseudo model training starts from the 100th batches, the inference accuracy can be raised from 89.57% to 91.05%. But the training should not start too late, otherwise the victim model has already begun to converge and the pseudo model will miss a portion of guidance information. The server should starts to train the pseudo-client model at the time when the test accuracy of the victim model starts to rise and the loss starts to fall. Note that, even if the start time is not optimal, the pseudo-client model still performs better than that trained after the SL is over (i.e., the pseudo-client model trained by using vanilla-PCAT).

![](images/7a782fdfa5ec82a134e1941b7b9f5da8d0fb7496ed01ecaf9d873363eca87e7a.jpg)



Fig. 7. Inference accuracy of the pseudo model $F _ { s } \widetilde { ( f _ { c } ( \cdot ) ) }$ by skipping batches in the early training. The experiment is performed on MNIST dataset, where the- - server has one sample per class. The pink and light blue lines denote the test accuracy and loss of SL baseline in the first epoch. The black dots mean the final test accuracy of $\widetilde { F _ { s } ( f _ { c } ( \cdot ) ) }$ if $\widetilde { f _ { c } }$ starts to train from a certain batch idx.

TABLE I SETTINGS FOR ALL CASES AND THEIR COMPLEXITY COMPARISON 

<table><tr><td></td><td>Dataset</td><td>Model</td><td>Param</td><td>Complexity</td></tr><tr><td>1</td><td>MNIST</td><td>LeNet-5</td><td>61.5K</td><td>Low</td></tr><tr><td>2</td><td>CIFAR-10</td><td>VGG16</td><td>14.6M</td><td>Medium</td></tr><tr><td>3</td><td>Tiny-Imagenet</td><td>MobileNet</td><td>28.5M</td><td>High</td></tr></table>

# V. IMPLEMENTATIONS

To demonstrate the effectiveness and practicality of PCAT, we implemented PCAT for a variety of learning tasks and models, as well as different settings of split learning.

# A. Datasets and Models

We implemented PCAT for the following cases with different popular models and benchmark datasts shown in Table I, which cover situations where the models and tasks are simple or complex.

# B. Data Processing

We assume that the server’s and the client’s datasets should be prepared for the same learning task. We consider two typical cases: 1) the server’s dataset is a subset of the client’s private dataset, i.e., $X _ { s e r v e r } \subset X _ { p r i v } ; 2 )$ the server’s dataset has no intersection with the client’s private dataset, i.e., $X _ { s e r v e r } \bigcap X _ { p r i v } = \varnothing$ .

For training, we randomly divide the training set of each benchmark dataset into a public dataset $X _ { p u b }$ and a private dataset $X _ { p r i v } .$ , and $X _ { p u b } : X _ { p r i v } = 1 : 9 . \ X _ { p r i v }$ is allocated to victim clients as the training set of the split learning. $X _ { p u b }$ is a public dataset that the server can retrieve some samples from it to compose its training set $X _ { s e r v e r }$ . If not specified, we make $X _ { s e r v e r }$ and $X _ { p r i v }$ i.i.d. We will also analyze the effectiveness of PCAT in non-i.i.d. cases. To evaluate the generalizability of PCAT, we also let the server use datasets $( X _ { d i f } )$ very different from $X _ { p r i v }$ . In our ablation study, $X _ { d i f }$ is a subset of Imagenet [24] while $X _ { p r i v }$ is from CIFAR-10. The samples in $X _ { d i f }$ have the same labels as the labels in CIFAR-10. For testing, we use the original testing sets to evaluate models.

![](images/02687eba3046dbdf5f1049a82e8be3edc5b997610f5c688a09091c4a9f4ef67f.jpg)



Fig. 8. Model splitting strategies. We omit batchnorms and ReLU in VGG16 and MobileNet.

# C. Model Splitting

We adopt LeNet-5 [25], VGG16 [26], MobileNet [27] to validate the effectiveness of our attack. We consider various model splitting strategies, as shown in Fig. 8. For two-part split learning, each model split into 2 parts. We split MobileNet from 1 to 4 layers to show that PCAT is robust to the cases that client’s model is extreme complex. For U-shape split learning, the client has one or two bottom layers and one or two top layers, while the intermediate layers are allocated to the server.

# VI. EXPERIMENTAL RESULTS

Based on the implementation in Section V, we conduct comprehensive experiments to demonstrate the effectiveness of PCAT on three attack goals in Section III-A, including stealing the functionality of the client model, reconstructing the private inputs, and inferring the labels. The results of successful attacks on different models and datasets testify the broad applicability of PCAT.

# A. Functionality Stealing

# (1) PCAT for Two-part SL

In i.i.d. settings. We first launch our pseudo-client attack in the case that $X _ { s e r v e r }$ and $X _ { p r i v }$ are i.i.d. and $X _ { s e r v e r } \subset X _ { p r i v } .$ We split each model from layer 2 to make the client model more complex. For MNIST, CIFAR-10 and Tiny ImageNet, the server has 5, 250, and 10 training samples per class. Fig. 9 shows the performance of the pseudo model constructed by PCAT and Vanilla-PCAT on three datasets. Both vanilla-PCAT and PCAT effectively steal the functionality of the client model. When the server trains a complete model independently using only its own data $X _ { s e r v e r } .$ , its accuracy is only 63.38%, 74.16%, and 13.62% on three datasets, respectively. With the same dataset $X _ { s e r v e r } ,$ Vanilla-PCAT achieves 91.67%, 85.62%, and 69.8% accuracy, respectively. PCAT further increases the inference accuracy to 96.89%, 89.48%, and 73.46%, which are very close to the performance of the victim SL model. Vanilla-PCAT converges faster than PCAT, because its training is directly guided by the well-trained server model. Though converging slower, PCAT achieves much better accuracy because of the guidance of evolving server models, which drives the output feature space of the pseudo-client model closer to that of the victim client model.

![](images/7fa90a2a68feddb7fcee6514b1837dc9802672c21e6ae9c90354648a746f44f8.jpg)  
Fig. 9. Performance of the pseudo model constructed by PCAT on three datasets. For MNIST, CIFAR-10 and Tiny ImageNet, the server has 5, 250 and 10 training samples per class, respectively. $X _ { s e r v e r } \subset X _ { p r i v }$ and all models split from layer2. Independent training means the server training a complete model using only its own data Xserver. SL baseline is the victim model trained on $X _ { p r i v }$ . The MSELoss represents the distance between the real feature space and the pseudo feature space.

![](images/49f8c398a160cc39389b509e790af856364991679f10e4c9e686750aa0fb875e.jpg)  
Fig. 10. Performance of PCAT changes with the number of training samples owned by the server. All models split from layer2 and $X _ { s e r v e r } \subset X _ { p r i v } .$

Intuitively, the more samples the server has, the better performance PCAT can achieve. Fig. 10 illustrates the intuition. On MNIST, when the sample number for each class increases from 1 to 25, the accuracy achieved by PCAT grows from 90.77% to 97.91%. On CIFAR-10, when the sample number for each class increases from 10 to 250, the accuracy achieved by PCAT grows from 49.03% to 89.42%. On Tiny ImageNet [28], when the sample number for each class increases from 1 to 25, the accuracy achieved by PCAT grows from 45.40% to 77.11%. Compared with the size of the private dataset, which are 54000, 45000, and 90000, (5400, 4500, 450 samples per class) respectively, PCAT requires only a small number of training samples to effectively steal the functionality. And surprisingly, PCAT can achieve a fairly good attack on LeNet-5 even if there is only 1 sample per class.

In non-i.i.d. settings.

Now we consider a more common situation that the dataset of the server lacks samples of some classes. In Fig. 11(a), and (b) illustrate the cases that the server lacks one class of samples, e.g., the digit “3” in MNIST and class “deer” (labeled $^ { \bullet } 4 ^ { \prime \prime } )$ in CIFAR-10. When the server independently trains a complete model, the model cannot recognize the missing class at all, and the accuracy of related classes also drops significantly. Vanilla-PCAT can recognize most samples in the missing class and achieve 78.91%/51.5% accuracy on MNIST/CIFAR-10, but there is still an obvious gap with the 99.11%/95.2% (on MNIST/CIFAR-10) baseline. PCAT significantly mitigates the effect of the missing class and achieves 94.95%/70.2% accuracy on MNIST/CIFAR-10. Moreover, the overall performance of PCAT is very close to the SL baseline.

(c) and (d) further analyze how the overall accuracy affected by the number of missing classes in the server’s dataset.

![](images/1ab8434b6ad6290607c79efcdc1513695833928fe62933cb9dcc1329b3d452da.jpg)  
Fig. 11. Performance of PCAT in non-i.i.d. settings on MNIST/CIFAR-10. (a) and (b) show the accuracy gap when $X _ { s e r v e r }$ lacks one class $( ^ { 6 6 } 3 ^ { 9 } ) ^ { 6 6 } 4 ^ { 9 }$ for MNIST/CIFAR-10). (c) and (d) present accuracy changing with the amounts of classes in Xserver.

TABLE II PERFORMANCE OF PCAT ON MNIST, WHEN THE PSEUDO-CLIENT MODEL HAS SIMPLER, THE SAME, OR MORE COMPLEX STRUCTURES THAN THE CLIENT 

<table><tr><td rowspan="2"></td><td colspan="3">Pseudo client</td><td rowspan="2">Victim client</td></tr><tr><td>Simple</td><td>Same</td><td>Complex</td></tr><tr><td>Model</td><td></td><td></td><td></td><td></td></tr><tr><td>Acc(%)</td><td>73.60</td><td>97.17</td><td>97.13</td><td>99.06</td></tr><tr><td>MSE</td><td>0.387</td><td>0.133</td><td>0.141</td><td>0</td></tr></table>

The server has 5 samples per class.

Compared with independent training, PCAT is much more robust to non-i.i.d. datasets. On MNIST, The accuracy of PCAT is still over 90% even if 4 classes are missing. On CIFAR-10, PCAT can use only 3 classes to achieve the same performance as Vanilla-PCAT with 9 classes. We think that the reason behind the surprising result is that a subset of classes can represent the mapping functionality of the client model.

Performance of different pseudo-client model structures. In PCAT, the server does not know the structure of the victim client model, and only knows learning task and its input and output formats. It can adopt any structure that works for the task as the pseudo-client model. We evaluate PCAT in cases that the structure of pseudo-client model is simpler or more complex than the victim client model. Table II presents the performance with different variants of pseudo-client model on MNIST. We also consider the situation that convolution layers are replaced by ResBlock [29] on CIFAR-10 [30] and present the results in Table III. Both tables show that when the pseudo-client model has the same structure as the victim model, it achieves the best performance. A more complex pseudo-client model can achieve almost the same performance as the same structure does, while two simpler structures suffer performance degradation to different degrees. We think the reason is that the simpler the model, the less qualified to learn the behaviors of the victim client model. Therefore, in practice, a more complex pseudo model has a higher chance to successfully steal the functionality of a SL model.

TABLE IIIPERFORMANCE OF PCAT ON CIFAR-10, WHEN THE STRUCTURE OF THEPSEUDO-CLIENT MODEL IS SIMPLER, THE SAME, MORE COMPLEX THAN THEVICTIM CLIENT MODEL, OR EVEN USE OTHER ELEMENTARY STRUCTURE

<table><tr><td rowspan="2"></td><td colspan="4">Pseudo client</td><td rowspan="2">Victim client</td></tr><tr><td>Simple</td><td>Same</td><td>Complex</td><td>Other</td></tr><tr><td rowspan="4">Model</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Acc(%)</td><td>87.54</td><td>88.90</td><td>88.35</td><td>84.96</td><td>93.20</td></tr><tr><td>MSE</td><td>0.0279</td><td>0.0134</td><td>0.0166</td><td>0.0511</td><td>0</td></tr></table>

The server has 250 samples per class.

TABLE IV COMPARISON ON FUNCTIONALITY STEALING PERFORMANCE (ACC: %) WITH UNSPLIT [15] 

<table><tr><td>Datasets</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Methods</td><td>UnSplit [15]</td><td>PCAT</td><td>UnSplit [15]</td><td>PCAT</td></tr><tr><td>SL Baseline</td><td>98.00</td><td>99.00</td><td>71.00</td><td>93.20</td></tr><tr><td>split layer = 1</td><td>93.75</td><td>98.75</td><td>43.69</td><td>91.10</td></tr><tr><td>split layer = 2</td><td>63.3</td><td>96.79</td><td>22.12</td><td>78.57</td></tr></table>

In PCAT,the attacker has 5 samples per class from $X _ { p r i \nu }$ in MNIST and 50 samples per class from $X _ { p r i \nu }$ in CIFAR-10.   
The bold value means a better performance than UnSplit.

Comparison with previous work. We compare PCAT with the most related work UnSplit [15], which is the SOTA method for a semi-honest server to steal the functionality of the client model and reconstruct the raw inputs and labels. The main difference is that UnSplit requires the server to know the structure of the victim client model while PCAT treats the victim client as a black box. Table IV compares their ability to steal functionality. PCAT significantly outperforms UnSplit in all cases with different models, datasets and splitting strategies. For example, on MNIST, when the client has two layers, the accuracy of UnSplit is only 63.3%, while PCAT achieves 96.79%. On CIFAR-10, with a more complex model, the accuracy of UnSplit is only 22.12%, while PCAT achieves 78.57%.

(2) PCAT for U-Shape SL As illustrated in implementation in Section V, we also implement a U-Shape LeNet-5/VGG16 split learning on MNIST/CIFAR-10, which has two bottom layers and two/one top layers on the client side. We use PCAT to successfully steal the functionality of the U-Shape split learning model. Results in Table V show that U-Shape PCAT achieves 96.98%/93.28% accuracy when there are 25/250 samples per class in the server’s dataset. Hence, PCAT can be applied to attack a wide range of split learning, including two-part SL and U-shape SL.

TABLE V FUNCTIONALITY STEALING RESULTS OF U-SHAPE PCAT 

<table><tr><td colspan="6">MNIST</td></tr><tr><td>Samples / Class</td><td>1</td><td>2</td><td>5</td><td>10</td><td>25</td></tr><tr><td>Acc(%)</td><td>72.30</td><td>84.27</td><td>91.83</td><td>93.27</td><td>96.98</td></tr><tr><td colspan="6">CIFAR-10</td></tr><tr><td>Samples / Class</td><td>10</td><td>25</td><td>50</td><td>100</td><td>250</td></tr><tr><td>Acc(%)</td><td>36.31</td><td>65.42</td><td>76.16</td><td>82.56</td><td>93.28</td></tr></table>

It is on MNIST/CIFAR-10withbottom layer2,toplayer2/layer1and $X _ { s e r v e r }$ $\subset X _ { p r i v } .$

TABLE VI COMPARISON OF DATA RECONSTRUCTION ON TINY-IMAGENET BETWEEN UNSPLIT [15] AND PCAT 

<table><tr><td></td><td colspan="3">UnSplit</td><td colspan="3">PCAT</td></tr><tr><td>truth</td><td><img src="images/3a9ba00f717ef4533b54fe4a2a87c289fd462688054ad5a2aab10966925fe73b.jpg"/></td><td><img src="images/ca54a9f31d5c349cdccfe75b0d03a438ec2c759b2c2bda45793d6c264fea4dce.jpg"/></td><td><img src="images/78c06f8e2739e68467fcc3cb6e97bdc8a8978a289daf10a73123d43e70ee63e0.jpg"/></td><td><img src="images/7f65103b4839a111da67f49b809ddf4f1e3d7430ff951e44c8edbe3a1731d2ff.jpg"/></td><td><img src="images/cda492d3a7fb9ae7b1463841ff8136d133f1e87a870698032eaac2991617b4df.jpg"/></td><td><img src="images/2b692a9b59e477f1674a0c0ff392ed2827b7afa3b301abd35756151d3d5c6fb4.jpg"/></td></tr><tr><td>layer1</td><td><img src="images/03282f051c34aaa435624aca0ff05355430c82f4be12939361118812958bd87c.jpg"/></td><td><img src="images/049797cb8271f637860c936d152cdfbb3757465863bd7018b8edde123d275180.jpg"/></td><td><img src="images/1a8156bb16985fcb0da89584333a8e43c3a1ed7e4fa9cfae33644fe3d0428eb8.jpg"/></td><td><img src="images/4292b6839a77d21879dd9d31fa943e3d929ee95dbceca530af05d44af522c247.jpg"/></td><td><img src="images/25456fe30eaafbd676ccea55c3869688f66872c025836dae4fc35e9e09b784a8.jpg"/></td><td><img src="images/e6100cc339614f974f80ba317ddb8f6dad6fdc1b6b0f7381cbd74da14afebf0e.jpg"/></td></tr><tr><td>layer2</td><td><img src="images/210384b8ce2121f02815ba3f6b2064a2efec45ebbe3deff889d108a5eeec3a39.jpg"/></td><td><img src="images/850bdfa158103249a0de503ff646fcfa0c17ca2c2127d197e65229a0443a72fd.jpg"/></td><td><img src="images/8e05ad8cb386d03862f52b1bd5b5d8465c8a80e13f4df9615f365c3165e2beef.jpg"/></td><td><img src="images/640ae3428daa18f7ce3867427774179ee39ddc47ec243c531d5a8c3241236ea1.jpg"/></td><td><img src="images/43b16fc9232d558951ea8a0dee694953c2e8f0418de38bb450608e6ed6453af7.jpg"/></td><td><img src="images/9b829d616db10d697e0dcb9f38bb9bb5bede39a43d5280dc75c8aef96fcd1a90.jpg"/></td></tr><tr><td>layer3</td><td><img src="images/8b8deb546a105a0cd6785ccb196bfc45f0210b030d17e323add48dbcc04ffca8.jpg"/></td><td><img src="images/f25c0fccd6c6d31ef46f88f2a95e55a95364f1109158de04daefbddbda563272.jpg"/></td><td><img src="images/d30452dd5df801631cafb6f083237bd38936fdb409da0b3f44420529f88303cc.jpg"/></td><td><img src="images/c8cbc7f51bdb38bc3721461ecaba3ca280ce031d21f1a758477eca6a621d44a6.jpg"/></td><td><img src="images/0320649c581bc3a3f0c9c49ecee96559b9c0a15957ff00ff98eb5ec6c5901856.jpg"/></td><td><img src="images/c3465b5c19d2ce4a5cf5129b3a51118d84517e8206cbe27a6d89f9cb7ca39d82.jpg"/></td></tr></table>

# B. Input Data Reconstruction

After stealing the functionality of the victim client model, following the method in Section IV-B, the server can reconstruct the private inputs of the client. We present our reconstruction results for two-part split learning on Tiny-ImageNet and compare them with UnSplit in Table VI. Obviously, the images reconstructed by our method are much more informative and clearer than those reconstructed by UnSplit.

We also make quantitative analysis of reconstruction result of PCAT and UnSplit by calculating the SSIM [31] index between reconstructed images and the groundtruth. The comparison is shown in Fig. 12. Obviously under the same condition, PCAT can reconstruct raw inputs with much higher similarity. Especially, when the client model and the learning task are complex, e.g., the client model has two layers from VGG16 on CIFAR-10, UnSplit almost fails to reconstruct the input images, while our method can still reconstruct the input images with fairly good clearness.

We also evaluate our input reconstruction method for U-shape split learning and non-i.i.d. setting. The results are shown in Fig. 13. For U-shape learning, our method can also clearly reconstruct the private inputs. More importantly, in the non-i.i.d. setting, though the server lacks samples of some classes, it can still reconstruct the inputs of the unknown classes. This is a serious privacy breach since the server steals the data it has never seen before from the client.

![](images/957228a8620377cf713e13e428a96dc7d04a532e5441bc677429f2c008c4fed3.jpg)



Fig. 12. Cdf curves of ssim [31] index between reconstruction results and ground truth on CIFAR-10 testsets, which shows that PCAT can recover private inputs with much more structural similarity.

![](images/72e1d65cffcb8e0da0ca8b5056d382ab18f7f1f4a49df412f100a0ea96def3ca.jpg)



Fig. 13. Data reconstruction results on MNIST and CIFAR-10 in non-i.i.d. and U-shape cases. For U-Shape split learning, the server has 5/20 (MNIST/CIFAR-10) samples per class from $\dot { X } _ { p r i v } ,$ with bottom layer = 1 and top layer = 2. For the non-i.i.d. case, split layer = 1; the server lacks samples from class “3”/ “deer” (MNIST/CIFAR-10) and has 5/20 samples from $\dot { X _ { p r i v } }$ for each other class, but it can still reconstruct the missing classes accurately.

TABLE VII LABEL INFERENCE ACCURACY OF PCAT ON U-SHAPE SPLIT LEARNING 

<table><tr><td colspan="6">MNIST</td></tr><tr><td>Samples / Cls</td><td>1</td><td>2</td><td>5</td><td>10</td><td>25</td></tr><tr><td>Acc(%)</td><td>82.65</td><td>94.42</td><td>96.58</td><td>96.89</td><td>98.23</td></tr><tr><td colspan="6">CIFAR-10</td></tr><tr><td>Samples / Cls</td><td>10</td><td>25</td><td>50</td><td>100</td><td>250</td></tr><tr><td>Acc(%)</td><td>19.29</td><td>89.10</td><td>92.83</td><td>93.08</td><td>93.23</td></tr></table>

It is implemented on MNIST/CIFAR-10 with botom layer2 and top layer2/layer1. Xseruer $\subset X _ { p r i v } .$

# C. Label Inference

Based on the pseudo-client model, we conduct label inference attack on U-shape split learning on MNIST/CIFAR-10 Datasets. As shown in Table VII, PCAT achieves high accuracy in label inference, which is 98.23%/93.23% when the server has 25/250 samples per class. Also, we compare PCAT with UnSplit [15] in label inference in Table VIII. When the top model has one layer, the inference accuracy of PCAT is 98.82%/93.42%, which is slightly lower than Unsplit. But, when the top model becomes more complex, e.g., having two layers, the inference accuracy of UnSplit severely drops to 9.1%/8.1%, while PCAT still achieves a high accuracy (96.58%/92.57%). Therefore, PCAT is more robust to various split learning models.

TABLE VIII COMPARISON ON LABEL INFERENCE ACCURACY(%) WITH UNSPLIT [15] 

<table><tr><td>Datasets</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Methods</td><td>UnSplit</td><td>PCAT</td><td>UnSplit</td><td>PCAT</td></tr><tr><td>top layer = 1</td><td>100.0</td><td>98.82</td><td>100.0</td><td>93.42</td></tr><tr><td>top layer = 2</td><td>9.1</td><td>96.58</td><td>8.1</td><td>92.57</td></tr></table>

In PCAT,the attacker has 5/100 samples per class from $X _ { p r i v }$ in MNIST/CIFAR-10.   
The bold value means a better performance than UnSplit.

TABLE IX FUNCTIONALITY PERFORMANCE OF PCAT AGAINST THE SL WITH DIFFERENTIAL PRIVACY [19] DEFENSE 

<table><tr><td colspan="5">MNIST</td></tr><tr><td>σ</td><td>+∞</td><td>70</td><td>60</td><td>50</td></tr><tr><td>Baseline Acc(%)</td><td>99.00</td><td>94.10</td><td>90.79</td><td>84.71</td></tr><tr><td>PCAT Acc(%)</td><td>97.31</td><td>91.12</td><td>88.66</td><td>80.84</td></tr><tr><td>Acc(%) Gap</td><td>1.69</td><td>2.98</td><td>2.13</td><td>3.87</td></tr><tr><td colspan="5">CIFAR-10</td></tr><tr><td>σ</td><td>+∞</td><td>200</td><td>100</td><td>50</td></tr><tr><td>Baseline Acc(%)</td><td>93.20</td><td>85.18</td><td>80.17</td><td>73.17</td></tr><tr><td>PCAT Acc(%)</td><td>86.50</td><td>77.45</td><td>71.14</td><td>68.34</td></tr><tr><td>Acc(%) Gap</td><td>6.70</td><td>7.73</td><td>9.03</td><td>4.83</td></tr></table>

It isperformed on MNIST/CIFAR-10,with split layer2/layer1. The server obtains 5/10osamples per classand XseruerCXpriu

# D. Against Traditional Defensive Mechanisms

Differential privacy can provide a rigorous mathematical privacy guarantee [32], making it a widely adopted privacy protection approach in Split learning. To be more specific, when the victim client receives gradients from the server, it will add Laplacian noise under $\mathrm { D P } ^ { \prime } \mathbf { s }$ guarantee. Thus, the client can protect its model and the next smashed data sent to the server. The results are shown in Table IX: though the accuracy of baseline decreases as the noise becomes larger, the accuracy gap between the baseline and pseudo-client is steady at a certain level. Based on the results we can conclude that DP is not effective against our attack.

# VII. TARGET DEFENSES

Given the failure of traditional defensive mechanisms in countering our attack, we try to seek potential defenses against our attack. We posit that the success of Pseudo-Client Attack can be attributed to the similarity in learning tasks and datasets between the pseudo-client and the victim client. This allows their jointly owned server model to generate comparable gradients under similar input-output pairs, enabling the pseudo-client to steal the functionality of the real client. To counteract such attacks, we propose that the victim client could claim an inconsistent learning task to the server, thereby rendering the input-output pairs incongruous and preventing the generation of similar gradients. This would prevent the pseudo-client from stealing functionality of the victim client and, hence, thwart this attack.

However, since the split learning baseline trains the learning task claimed by the victim client, rather than the actual learning task it aims to train, it is vital to examine how to design the claimed learning task given the real learning task. If these two tasks are unrelated at all, the victim client would learn nothing related to its actual learning task from split learning. Therefore, we propose that the claimed learning task should be correlated to the real learning task, such that it can be easily converted to the inference in the real learning task from the one in the claimed learning task through a simple mapping, thus the victim client can guarantee that the real learning task is well-trained from split learning while co-training the claimed learning task with the server.

![](images/79f843e669d35a57cc911ade64d4e502c17d0772be3b9b77e2ae260ac5e2147d.jpg)



![](images/c1c8a286ed4e959306f6b83a272817e5c8d62533553fefbe45b6ee3fa77a7ce4.jpg)



![](images/67f33c7a81b4b279fee17817a28492b5ec7ecc49245cd63c511973db55fcb725.jpg)



Fig. 14. Defense against PCAT. The legends are the same as that in Fig. 5. yˆ represents the labels of the claimed learning task.

Fig. 14 illustrates how the victim client’s defense works. The labels of samples from train set and test set of the victim client’s private dataset, corresponding to the real learning task, are denoted as $y _ { p r i v }$ and $y _ { t e s t }$ respectively. To safeguard the real learning task, the victim client devises the claimed learning task, wherein each sample is labeled $\hat { y } .$ . During the SL training process, $y _ { p r i v }$ is transformed into $\hat { y }$ through the designed mapping, and the victim client sends $\hat { y }$ instead of $y _ { p r i v }$ to the server, who is unaware of the defense mechanism employed by the victim client. Consequently, from the server’s viewpoint, the victim client’s objective is to train $\hat { y } ,$ , but the server’s dataset inputoutput pairs $( X _ { s e r v e r } , y _ { s e r v e r } )$ are incompatible with $( X _ { p r i v } , \hat { y } )$ . The relationship between $y _ { p r i v }$ and $\hat { y }$ is established by the victim client, and the server is oblivious to the mapping relationship between them. In the inference phase, the server transmits the model output pred to the victim client, who can convert $\hat { y }$ to $y _ { t e s t } .$ , the prediction under the real learning task, by applying the inverse mapping. As the server is unaware of the inverse mapping, it can only infer $y _ { t e s t }$ directly from pred, which is unlikely to be accurate.

Inspired by the label transformation idea introduced in [33], which is designed to defend gradient inversion attack in Vertical Federated Learning, we design two distinct label transformation (namely label encoding and decoding) mechanisms to thwart pseudo-client attack. These mechanisms encompass a one-toone mapping defense as well as an autoencoder based defense.

# A. One-to-One Mapping Defense

Discrete labels are used as an example in this study. There is a one-to-one mapping between the label $y _ { p r i v }$ in the real learning task and the label $\hat { y }$ in the claimed learning task. Additionally, $\hat { y }$ can be converted back to the real label by means of an inverse one-to-one mapping. As illustrated in Fig. 16, all samples with the real label $\because 3 ^ { \cdot }$ are labeled as $\ ' 4 '$ following one-to-one mapping. Consequently, different labels are assigned to the same sample on the victim client and server sides after the labels are mapped. Subsequently, the victim client transmits yˆ to the server for split learning training. During the inference phase, the victim client inputs a sample that requires inference with the server, following which the server delivers the inference result of this sample to the victim client. The victim client receives the inference and maps it back to the real label to obtain the correct inference result. For instance, in the context of Fig. 16, upon receiving the inference outcome of ’4’, the client can obtain the accurate inference of ’3’ through the inverse mapping.

![](images/7781e70d19288d98d052cee9cb5b0b5092dc1a9df598204214ffdc725a9b1813.jpg)



(a)

![](images/2668d608ca8f5593064fbc2712820b21df4dd39e10a17ec808c0a814e552d7bc.jpg)



(b)

![](images/28558eaf696e7007349948abc9033346f5a48df6e9616c0de52e311858793167.jpg)



（C）

![](images/63dba58c99b4783b0d6922c8b852879e146e3fd447358b5bba0910d145066a66.jpg)



(@)

![](images/6ab0dbc50fb63380b67ff3e574c95a0684974d111476cd7f6fd61d4303bb1b7e.jpg)



(e）  
Fig. 15. Visualizations of 2D and 3D coding spaces. (a) illustrates the 2D coding space of the vanilla autoencoder and (b) minimizes the area of (a) by using minimum covering ring. Correspondingly, (c) presents the coding space of the autoencoder with customized loss function and (d) is the area of minimum covering ring of (c). (e) is the 3D coding space of a minimum covering spheric shell.

![](images/0f054a71dc754cda495bc47f08d5c3fde1e0ee38848c0bf1547c0141df09097f.jpg)



Fig. 16. Example of one-to-one mapping defense and inverse mapping. ypriv denotes the labels of the real learning task of the SL baseline and yˆ represents the labels of the claimed learning task.

For the attacker, unaware of the victim client’s label transformations, it still employs the original labels of its dataset to launch the attack. Upon completing the attack, it proceeds to perform inference on the basic learning task of the its dataset. Thus, we rely on the inference accuracy of the server’s and the pseudo-client’s model on the basic learning task as the metric for assessing the efficacy of the attack. As demonstrated in Table X, the one-to-one mapping defense remarkably diminishes the accuracy of the attack while effectively safeguarding the split learning baseline model’s performance. To be more specific, the attack performance of PCAT in each dataset drops 30.53%/24.66% while the split learning baseline’s accuracy remains the same.

# B. Autoencoder Based Defense

The one-to-one mapping defense is a straightforward and efficient mechanism. However, it remains unclear whether an adversary could reconstruct the mapping by leveraging their prior knowledge of the dataset and the smashed data. To address this concern, we have explored more intricate encoding strategies. Specifically, we have employed an autoencoder to encode the labels of the real learning task, thereby minimizing

TABLE X WE COMPARE THE FUNCTIONALITY STEALING RESULTS OF PCAT AND IMPORVED PCAT UNDER THREE CASES 

<table><tr><td>Attack</td><td colspan="2">PCAT</td><td colspan="2">improved PCAT</td></tr><tr><td>Acc(%)</td><td>Baseline</td><td>Pseudo</td><td>Baseline</td><td>Pseudo</td></tr><tr><td></td><td colspan="4">MNIST</td></tr><tr><td>No defense</td><td>98.82</td><td>96.56</td><td>98.86</td><td>96.51</td></tr><tr><td>One2One Mapping</td><td>98.87</td><td>66.03</td><td>98.76</td><td>96.16</td></tr><tr><td>Autoencoder Based</td><td>97.93</td><td>10.00</td><td>97.87</td><td>80.44</td></tr><tr><td></td><td colspan="4">CIFAR-10</td></tr><tr><td>No defense</td><td>92.74</td><td>82.57</td><td>92.91</td><td>82.68</td></tr><tr><td>One2One Mapping</td><td>92.66</td><td>57.91</td><td>92.99</td><td>82.32</td></tr><tr><td>Autoencoder Based</td><td>88.59</td><td>10.00</td><td>88.23</td><td>58.96</td></tr></table>

Through the results we find that under one-to-one mapping defense and autoencoder based defense，the accruacy of PCAT drops drasticly while improved PCAT still works effectively.

the need for manual setting procedures. During the inference phase, the victim client decodes the received inference result using the corresponding decoder to obtain the inference under the real learning.

In the following equations, $y _ { i } , \widehat { y _ { i } } , \widetilde { y _ { i } }$ denotes the labels in the true learning task, the encoded labels and decoded labels respectively.

$$
y _ {i} \in \left\{y _ {1}, y _ {2}, \dots , y _ {n} \right\} \tag {2}
$$

$$
\widehat {y _ {i}} \in \{\widehat {y _ {1}}, \widehat {y _ {2}}, \dots , \widehat {y _ {n}} \} \tag {3}
$$

$$
\widetilde {y} _ {i} \in \{\widetilde {y} _ {1}, \widetilde {y} _ {2}, \dots , \widetilde {y} _ {n} \} \tag {4}
$$

$$
\widehat {y} _ {i} = \operatorname{Enc} \left(y _ {i}\right), \quad \widetilde {y} _ {i} = \operatorname{Dec} \left(\widehat {y} _ {i}\right). \tag {5}
$$

Despite encoding the actual labels, our encoder and decoder still function as one-to-one mappings, and thus do not fundamentally differ from the previous method. Our defense strategy aims to prevent the server from gathering any basic information about the learning task through the collected labels. Specifically, the server will remain unaware of whether the victim client’s learning task is classification, or even how many classes are contained in the task. Furthermore, even if the server obtain the statistics of the labels received from the victim client, it will not be able to correctly label the data the same as the data in the victim client. To aid in visualizing our approach, the OneHot labels of 10 classes are represented by 10 black points in a two-dimensional space. The two-dimensional space is divided into 10 different regions with different colors. All the points in the same region can be decoded to the same class.

To disrupt the one-to-one mapping between the labels of the real learning task and the claimed learning task, we employ a technique whereby a random point is selected from the region in the coding space that corresponds to the class of the sample. This point’s vector is used as the label for the sample sent to the server. The learning task for the victim client is to ensure that the output of the sample is as close as possible to the corresponding code. Since models generally output samples of the same class to the same region in the coding space, the victim client can decode the model output sent from the server to infer the predicted sample in the real learning task.

However, in this mechanism, the labels are spread across the entire coding space, which can lead to confusion for the model when dealing with samples that fall at the intersection of multiple regions. This ultimately results in a lower accuracy for the split learning baseline. To address this issue, we attempt to reduce the coding space as much as possible, without allowing the attacker to obtain any learning task information through statistical analysis of the labels.

To achieve this, we utilize the Welzl algorithm to determine the minimum covering circle of the codes that correspond to all OneHot vectors. We then calculate the minimum Euclidean distance between these codes and the center of the minimum covering circle to obtain the inner radius of the ring, which defines the minimum covering region.

To minimize the ring area, it is desirable for each corresponding encodings of all OneHot vectors to have a similar Euclidean distance to the center of the minimum covering circle. However, computing the minimum covering circle incurs significant cost during autoencoder training iterations. To address this issue, we incorporate the variance of Euclidean distances between encoded OneHot vectors into the loss function. The hyperparameter α adjusts the balance between $\mathcal { L } _ { v a r }$ and the basic loss function $\mathcal { L } ( y , \widetilde { y } )$ for the given learning task. By adding $\mathcal { L } _ { v a r }$ to the loss function, we can ensure that not only do the codes corresponding to all OneHot vectors have the similar distance to the center of the minimum covering circle, but also that the distances between these codes are similar as well. Thus, the areas corresponding to each class in the coding space are made similar.

$$
\forall i, j \in [ 1, n ] \text {   and   } i <   j, \text {   dist } _ {i j} = \| \widehat {y} _ {j} - \widehat {y} _ {i} \| _ {2} \tag {6}
$$

$$
\mathcal {L} _ {v a r} = D (d i s t _ {1 2}, \dots , d i s t _ {i j}, \dots , d i s t _ {(n - 1) n}), \quad 1 \leq i <   j \leq n \tag {7}
$$

$$
\mathcal {L} = \alpha \mathcal {L} (y, \widetilde {y}) + (1 - \alpha) \mathcal {L} _ {\text { var }}. \tag {8}
$$

In the two-dimensional coding space illustrated in Fig. 15, the incorporation of the $\mathcal { L } _ { v a r }$ loss function results in a reduction in the area of the minimum covering ring. Furthermore, the areas of the corresponding regions for each class become more homogeneous. A similar trend is observed in the three-dimensional coding space, as depicted in Fig. 15. Here, the minimum covering sphere is characterized by an outer radius of 0.1457 and an inner radius of 0.1372. This approach can be extended to coding spaces of varying dimensions without loss of generality.

![](images/cc8692c33fb89b08efc7a1d8e6e6961aaeb4e73f452e2683bd6d4217ef69f916.jpg)



Fig. 17. Improved pseudo-client attack in SL. Since we do not know whether the client adopts the defense $( y _ { p r i v } \neq \hat { y } )$ or not, we consider two cases $( y _ { p r i v } =$ yˆ and $y _ { p r i v } \neq \hat { y } ,$ ) in parallel. In the case of $y _ { p r i v } = \hat { y }$ , it is the same as pseudoclient attack. In the case of $y _ { p r i v } \neq \hat { y }$ , the server initializes several pairs of $\widetilde { f _ { c } } ^ { r }$ and $\widetilde { f _ { s 1 } } ^ { n }$ and select the best one according to the train loss after attack.

# VIII. IMPROVEMENT OF PCAT

Given that modifying the learning task can effectively defend against PCAT, we aimed to improve the PCAT mechanism to enable it to attack regardless of whether the victim client adopts our proposed defense. Our idea is to have the attacker keep their dataset unchanged from the original learning task and remove the constraint of the server model’s top layer. To achieve this, we use a pseudo-top model to map the input space of the server model’s top layer to the server’s learning task label space. Specifically, as illustrated in Fig. 17, we divided the server model $F _ { s }$ into one layer of top model $F _ { s 1 }$ and the remaining part model $F _ { s 2 }$ . As the server is unaware of whether the victim client has adopted our defense strategy, we designed our attack mode to be capable of targeting both cases in parallel.

First we assume $y _ { p r i v } = \hat { y }$ , which indicates that the client has not adopted our proposed defense and the actual learning task of split learning is consistent with the learning task known by the server. In this case, our attack mode remains unchanged as described in Section IV-A and illustrated in Fig. 17, where the pseudo-client shares the $F _ { s 1 }$ and $F _ { s 2 }$ models with the victim client (i.e., the entire server model).

Meanwhile we assume $y _ { p r i v } \neq \hat { y }$ , which implies that the client has adopted the defense method of modifying the learning task and the actual learning task of split learning baseline is inconsistent with the learning task known by the server. To handle this scenario, the server generates multiple parallel pseudo-clients $\widetilde { f } _ { c }$ and pseudo-top models $\widetilde { f _ { s 1 } }$ before starting the split learning baseline. Here, $\widetilde { f } _ { c }$ is the same as the case without defensive measures, and $\widetilde { f _ { s 1 } }$ is consistent with the structure of $F _ { s 1 }$ , but the model parameters are inconsistent.

After generating the pseudo-client and pseudo-top models, the SL baseline and the attack start simultaneously. In each iteration, the victim client performs forward propagation and sends the smashed data and the label of the sample corresponding to the claimed learning task to the server. The server then randomly selects the training samples owned by the server without label alignment and feeds the selected samples to the pseudo-client for forward propagation. When the server receives the smashed data and labels from the victim client and pseudo-client, it performs forward propagation in $F _ { s 2 }$ , then performs forward propagation and calculates the loss in the real top model $F _ { s 1 }$ and the pseudo-top model $\widetilde { f _ { s 1 } }$ , respectively, and then performs back propagation. Except for the pseudo-client and pseudo-top models, which use the gradients produced by the pseudo training samples for weight updates, the remaining models use the gradients produced by the split learning baseline for weight updates. Since different pseudo-client and pseudo-top model pairs can achieve different performance, we can select the best pair based on the training loss of pseudo samples. More explanation is presented in Section IX-B

The improved PCAT mechanism is similar to the U-Shape PCAT, with the only difference being that in the improved PCAT, the top model of split learning baseline is on the server side, and the loss value is calculated by the server. In contrast, in the U-Shape PCAT, the top model of split learning baseline is on the real client side, and the loss is calculated by the client to protect the label. Going further, we can conclude that under U-Shape PCAT, our proposed defense will fail.

To validate the efficacy of improved PCAT, we conducted experiments on MNIST, CIFAR-10. The settings of our experiments, as discussed in Section V, remains consistent with the previous experiments, wherein 10/100 samples of each class are employed as the server dataset for MNIST and CIFAR-10, respectively. Further, we set $X _ { s e r v e r } \in X _ { p r i v }$ , split layer = 2, and top layer = 1. Our experimental findings in Table X demonstrate that the improved PCAT outperforms the basic PCAT in both one-to-one mapping defense and autoencoder base defense. Specifically, under one-to-one mapping defense, the attack accuracy improved significantly from 66.03%/57.91% to 96.16%/82.32%. Similarly, under autoencoder based defense, the attack accuracy increased from 10.00%/10.00% to 80.44%/58.96%.

# IX. DISCUSSION

# A. Adding Noise

Our original intention was to protect the privacy of the victim client by adding Gaussian noise to the smashed data. However, we are surprised to discover that adding moderate amounts of Gaussian noise does not prevent PCAT, but rather enhanced the ability of the pseudo-client to steal the functionality of the victim client. To improve the accuracy of stealing client functionality, we propose that the server add noise to the smashed data. When the client sends smashed data to the server, the server adds Gaussian noise and then feeds it to the server model for forward propagation. It should be noted that adding noise to the smashed data of the split learning baseline causes a slight decrease in convergence speed and final accuracy, thus breaking the semi-honest rule. However, since the victim client cannot anticipate the convergence speed and final accuracy of the model, appropriately added noise is still difficult to detect.

We conducted experiments on two datasets, MNIST and CIFAR-10, adding Gaussian noise with zero mean and varying variance to the smashed data. The variance is represented by the X-axis. Results showed that adding Gaussian noise slightly degraded the accuracy of the split learning baseline, but appropriate noise enabled the pseudo-client to steal closer functionality. Specifically, on the MNIST dataset, the pseudo-client accuracy improved from 88.44% to 90.48% when the smashed data added noise variance was 1.0. On the CIFAR-10 dataset, the pseudo-client accuracy improved from 74.75% to 76.05% when the smashed data added noise variance was 0.2, as shown in Fig. 18.

![](images/a8406a504967e60b2f13b8129f2213d00caae92c29b513b44d1f126c420e3ca3.jpg)



(a)MNIST

![](images/ce558b9562e9ff4446ae879cea1d99defab8ee15e5494d9ce6d7b13e1e7d275e.jpg)



(b) CIFAR-10

Fig. 18. Accuracy of baseline and pseudo-client when adding different Gaussian noise to the smashed data.   
![](images/7970bb0a0b48c8aa02aa00fd209c0c69525474376367756c567a21470458e16d.jpg)



(a)

![](images/d53cb60a74dd673d7d7bcc98984a9af58d865ea4f31167c9a5053314087d2b49.jpg)



![](images/684edd8d0f97ec1b58cf8b553aee9d9294b7ce2e21bb6c6f54357df8df429417.jpg)

![](images/d079478d2078ae15e352b2bd704e8f4c94e7c0e1bdc04fe176ca92fa52f73fbd.jpg)

![](images/d28b639c0054e870caa3be9306eda28753cddf3bf3f1978a1cbf4c91c96d17ee.jpg)

![](images/a9e4507ba5a6dfac6e8d69532fd24facc082c81288e6d888819434c24f4c919d.jpg)  
Fig. 19. (a) illustrates the space evolution of smashed data in U-shape PCAT. It can be categorized into two cases: one where the smashed data of the pseudoclient get closed to the smashed data of the victim client, and the other where the smashed data of the pseudo-client move away from that of the victim client. The four test methods are depicted in (b), and their corresponding outcomes are presented in Table XI.

# B. Phenomenon in U-Shape PCAT

In Section III-B, we illustrate how the server steals the model functionality of the victim client in two-party split learning. We observe that the output feature space of the pseudo-client model gradually approaches that of the victim client due to the constraint of the server model. Without this constraint, the output feature space of the pseudo-client model would be far from that of the victim client. We further investigate how the feature space of smashed data changes in U-Shape split learning. As shown in Fig. 19, since the model is divided into three parts, two feature spaces, denoted by $\mathcal { F } _ { 1 }$ and ${ \mathcal { F } } _ { 2 } .$ are formed. Correspondingly, the smashed data feature spaces on the pseudo-client side are denoted by $\widetilde { \mathcal { F } _ { 1 } }$ and $\widetilde { \mathcal { F } _ { 2 } }$ .

We discover that when stealing the victim client and top model, the constraint of the server model causes the changes of feature spaces in two possible ways. The first is similar to two-party split learning, in which $\widetilde { \mathcal { F } _ { 1 } }$ and $\widetilde { \mathcal { F } _ { 2 } }$ gradually approach ${ \mathcal { F } } _ { 1 }$ and $\mathcal { F } _ { 2 }$ under the constraint of the server. In the other way, $\widetilde { \mathcal { F } _ { 1 } }$ and $\bar { \mathcal { F } } _ { 2 }$ are far away from $\mathcal { F } _ { 1 }$ and $\mathcal { F } _ { 2 }$ .

TABLE XI FOUR TEST RESULTS IN TWO CASES 

<table><tr><td>Acc(%)</td><td> $\tilde{f}_{c}, F_{s}, \tilde{f}_{t}$ </td><td> $F_{c}, F_{s}, F_{t}$ </td><td> $\tilde{f}_{c}, F_{s}, F_{t}$ </td><td> $F_{c}, F_{s}, \tilde{f}_{t}$ </td><td>Loss</td></tr><tr><td> $\tilde{\mathcal{F}} \approx \mathcal{F}$ </td><td>95.85</td><td>98.79</td><td>98.35</td><td>97.02</td><td>0.002</td></tr><tr><td> $\tilde{\mathcal{F}} \neq \mathcal{F}$ </td><td>75.41</td><td>98.96</td><td>0.05</td><td>0.79</td><td>0.005</td></tr></table>

We can find that if $\tilde { \mathcal { F } } \neq \mathcal { F } ,$ the accuracy of the pseudo-client is lower than that in the case $\widetilde { \mathcal { F } } \approx \mathcal { F } ,$ .Moreover,we can’t splicea pseudo-top and a victim client (or a pseudo-client and a victim top) together.

We confirm this phenomenon through the experiment in Fig. 19, and the results are shown in Table XI, with two rows representing the test results in each scenario. From the results, we can see that when $\widetilde { \mathcal { F } } \approx \mathcal { F }$ , the accuracy of the model stolen by the pseudo-client is lower than that in the $\widetilde { \mathcal { F } } \neq \mathcal { F }$ case. Meanwhile, if the pseudo-client and the victim top model are spliced on the server at the same time, or the victim client and the pseudo-top model are spliced on the server at the same time, the spliced model can still maintain high accuracy when $\widetilde { \mathcal { F } } \approx \mathcal { F }$ . However, if $\widetilde { \mathcal { F } } \neq \mathcal { F }$ , the accuracy of the spliced model will drastically decrease.

Therefore, when we conduct improved PCAT, we can’t avoid the $\widetilde { \mathcal { F } } \neq \mathcal { F }$ case. The solution we deal with is initializing several pairs of pseudo-client and pseudo-top, we select the pair with the least training loss and this pair can achieve the highest accuracy.

# X. CONCLUSION

In this work, we propose a novel pseudo-client attack (PCAT) mechanism on various SL models. PCAT enables a semi-honest server to conduct functionality stealing, input data reconstruction and label inference without knowing the structure of the victim client model. We implemented PCAT for rich models, tasks and settings. Comprehensive experiments demonstrate that PCAT works effectively for rich models, tasks and settings. The whole attack process is transparent to the client, which thus reveals a serious privacy risk of SL. We also investigate a targeted defense and improve our attack to be robust to such defense. There remains some open problems for the future work. For example, we have discovered that there exist two potential paths for the feature space evolution in u-shape PCAT. To eliminate one of these paths, we will perform further investigation on U-shape PCAT.

# REFERENCES

[1] S. Abuadbba et al., “Can we use split learning on 1D CNN models for privacy preserving training?,” in Proc. 15th ACM Asia Conf. Comput. Commun. Secur., Taipei, Taiwan, H. Sun, S. Shieh, G. Gu, and G. Ateniese, Eds., 2020, pp. 305–318.   
[2] J. Kim, S. Shin, Y. Yu, J. Lee, and K. Lee, “Multiple classification with split learning,” in Proc. 9th Int. Conf. Smart Media Appl., Jeju, Republic of Korea, 2020, pp. 358–363.   
[3] W. Y. B. Lim et al., “Incentive mechanism design for resource sharing in collaborative edge learning,” 2020, arXiv:2006.00511.   
[4] P. Vepakomma, O. Gupta, T. Swedish, and R. Raskar, “Split learning for health: Distributed deep learning without sharing raw patient data,” 2018, arXiv:1812.00564.   
[5] A. Singh, P. Vepakomma, O. Gupta, and R. Raskar, “Detailed comparison of communication efficiency of split learning and federated learning,” 2019, arXiv:1909.09145.   
[6] O. Gupta and R. Raskar, “Distributed learning of deep neural network over multiple agents,” J. Netw. Comput. Appl., vol. 116, pp. 1–8, 2018.

[7] M. G. Poirot, P. Vepakomma, K. Chang, J. Kalpathy-Cramer, R. Gupta, and R. Raskar, “Split learning for collaborative deep learning in healthcare,” 2019, arXiv:1912.12115.   
[8] P. Vepakomma, A. Singh, O. Gupta, and R. Raskar, “NoPeek: Information leakage reduction to share activations in distributed deep learning,” in Proc. 20th Int. Conf. Data Mining Workshops, Sorrento, Italy, G. D. Fatta, V. S. Sheng, A. Cuzzocrea, C. Zaniolo, and X. Wu, Eds., 2020, pp. 933–942.   
[9] J. Ryu, D. Won, and Y. Lee, “A study of split learning model,” in Proc. 16th Int. Conf. Ubiquitous Inf. Manage. Commun., Seoul, Republic of Korea, 2022, pp. 1–4.   
[10] W. N. Price and I. G. Cohen, “Privacy in the age of medical Big Data,” Nature Med., vol. 25, no. 1, pp. 37–43, 2019.   
[11] N. Christin and R. Safavi-Naini, “Financial cryptography and data security,” in Proc. 18th Int. Conf. Financial Cryptogr. Data Secur., 2014, pp. 99–118.   
[12] K. Abouelmehdi, A. Beni-Hssane, H. Khaloufi, and M. Saadi, “Big data security and privacy in healthcare: A review,” Procedia Comput. Sci., vol. 113, pp. 73–80, 2017.   
[13] P. Jain, M. Gyanchandani, and N. Khare, “Big data privacy: A technological perspective and review,” J. Big Data, vol. 3, pp. 1–25, 2016.   
[14] Z. He, T. Zhang, and R. B. Lee, “Model inversion attacks against collaborative inference,” in Proc. 35th Annu. Comput. Secur. Appl. Conf., San Juan, PR, USA, D. Balenson, Ed., 2019, pp. 148–162.   
[15] E. Erdogan, A. Küpçü, and A. E. Çiçek, “UnSplit: Data-oblivious model inversion, model stealing, and label inference attacks against split learning,” in Proc. 21st Workshop Privacy Elect. Soc., New York, NY, USA, 2022, p. 115–124.   
[16] D. Pasquini, G. Ateniese, and M. Bernaschi, “Unleashing the tiger: Inference attacks on split learning,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Virtual Event, Republic of Korea, Y. Kim, J. Kim, G. Vigna, and E. Shi, Eds., 2021, pp. 2113–2129.   
[17] G. Gawron and P. Stubbings, “Feature space hijacking attacks against differentially private split learning,” 2022, arXiv:2201.04018.   
[18] E. Erdogan, A. Küpçü, and A. E. Çiçek, “SplitGuard: Detecting and mitigating training-hijacking attacks in split learning,” in Proc. 21st Workshop Privacy Elect. Soc., New York, NY, USA, 2022, p. 125–137.   
[19] M. Abadi et al., “Deep learning with differential privacy,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., New York, NY, USA, 2016, pp. 308–318.   
[20] H. Mi et al., “Collaborative deep learning across multiple data centers,” SCIENCE CHINA Inf. Sci., vol. 63, no. 8, 2020, Art. no. 182102.   
[21] H. Chen, Y. Zhang, Y. Cao, and J. Xie, “Security issues and defensive approaches in deep learning frameworks,” Tsinghua Sci. Technol., vol. 26, no. 6, pp. 894–905, 2021.   
[22] O. Li et al., “Label leakage and protection in two-party split learning,” 2021, arXiv:2102.08504.   
[23] G. E. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” 2015, arXiv:1503.02531.   
[24] J. Deng, W. Dong, R. Socher, L. Li, K. Li, and L. Fei-Fei, “ImageNet: A large-scale hierarchical image database,” in Proc. IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recognit., Miami, Florida, USA, 2009, pp. 248–255.   
[25] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” in Proc. IEEE, vol. 86, no. 11, pp. 2278–2324, Nov. 1998.   
[26] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” in Proc. 3rd Int. Conf. Learn. Representations, Y. Bengio and Y. LeCun, Eds., San Diego, CA, USA, 2015.   
[27] A. G. Howard et al., “MobileNets: Efficient convolutional neural networks for mobile vision applications,” 2017, arXiv:1704.04861.   
[28] J. Wu, Q. Zhang, and G. Xu, “Tiny ImageNet challenge,” 2021. [Online]. Available: http://cs231n.stanford.edu/reports/2017/pdfs/930.pdf   
[29] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., Las Vegas, NV, USA, 2016, pp. 770–778.   
[30] A. Krizhevsky and G. Hinton, “Learning multiple layers of features from tiny images,” Comput. Sci. Univ. Toronto, Canada, Tech, Rep., 2009. [Online]. Available: https://www.cs.utoronto.ca/∼kriz/learning-features-2009-TR.pdf   
[31] Z. Wang, A. Bovik, H. Sheikh, and E. Simoncelli, “Image quality assessment: From error visibility to structural similarity,” IEEE Trans. Image Process., vol. 13, no. 4, pp. 600–612, Apr. 2004.   
[32] C. Dwork and A. Roth, “The algorithmic foundations of differential privacy,” Found. Trends Theor. Comput. Sci., vol. 9, no. 3/4, pp. 211–407, 2014.   
[33] Y. Liu et al., “Batch label inference and replacement attacks in black-boxed vertical federated learning,” 2021, arXiv:2112.05409.

![](images/f89a6b03be4d8373a45d2732c5caa7607e2b7aa08080058c8dffac1bc14466fe.jpg)



Lan Zhang received the bachelor’s and PhD degrees from Tsinghua University, China. She is currently a professor with the School of Computer Science and Technology, University of Science and Technology of China. Her research interests span mobile computing, privacy protection, data sharing and trading.

![](images/c12a2b241613e70f238d6c4b374d0cb55056151ca2a433897c958cbe8ba52754.jpg)



Yaliang Li received the PhD degree from the Department of Computer Science and Engineering, SUNY Buffalo, in 2017. He is a research scientist with DAMO Academy, Alibaba Group. Before that he worked as a research scientist with Baidu Research, and a senior researcher with Tencent Medical AI Lab. He is broadly interested in machine learning and data mining with a focus on knowledge graph, question answering, automated machine learning, and more recently federated learning.

![](images/9424f67ef34bb6e0d2fde9396bc27ee64bd899829efb8c6f7d5e09ddd70fc785.jpg)



Xinben Gao received the BS degree in information security from the School of the Gifted Young, University of Science and Technology of China, Hefei, China, in 2022. She is currently working toward the MS degree in computer science and technology from the University of Science and Technology of China. Her research interests include privacy attack and protection in distributed machine learning.

![](images/16cd45a972376b4c016c5f6f241cf01bb5caa30ba3a9ea6f63b68f800b94d776.jpg)



Yunhao Liu (Fellow, IEEE) received the BS degree from Automation Department, Tsinghua University, and the MS and PhD degree in computer science and engineering from Michigan State University. He is professor with Automation Deapartment and dean of the GIX with Tsinghua University. He is a fellow of ACM.