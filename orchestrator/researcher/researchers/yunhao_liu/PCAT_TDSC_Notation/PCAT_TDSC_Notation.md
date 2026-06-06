# Functionality and Data Stealing by Pseudo-Client Attack and Target Defenses in Split Learning

Lan Zhang, Xinben Gao, Yaliang Li, Yunhao Liu

Abstract—Split learning (SL) aims to protect a client’s data by splitting up a neural network among the client and the server. Previous efforts have shown that a semi-honest server can conduct a model inversion attack. However, those attacks require the knowledge of the client network structure, and the performance deteriorates dramatically as the client network gets deeper (≥ 2 layers). In this work, we explore the attack in a more general and challenging situation where the client model is unknown and more complex. We unveil the inherent privacy leakage through a series of intermediate server models during SL, and propose a new attack on SL: Pseudo-Client ATtack (PCAT). To the best of our knowledge, this is the first attack for a semihonest server to steal clients’ functionality, reconstruct private inputs and labels without any knowledge about the clients’ network structure. Moreover, the attack is transparent to clients. Extensive experiments demonstrate that our attack outperforms previous works in scenarios involving more complex models and learning tasks, even in non-i.i.d. settings and confronted with conventional defensive measures. We further explore novel defense mechanisms to mitigate PCAT and improve our attack to counteract the potential defenses.

Index Terms—privacy attacks, privacy defenses, split learning

# I. INTRODUCTION

The last decade has seen the flourishing and widespread adoption of deep neural networks (DNNs). Split learning (SL) is an emerging learning paradigm proposed to enable a data owner with constrained computing resources or sensitive data to train a large model with a powerful server cooperatively [1]– [9]. It splits a DNN into a client model and a server model, and the client only needs to perform lightweight computations and output intermediate layer activations (named “smashed data”) instead of raw data. Since the server doesn’t have access to the client-side model and inputs, SL is considered to be capable of protecting the functionality of the client model and the privacy of inputs from stealing.

In many application areas, like healthcare and finance [10]– [13], the data and labels from clients can be valuable and sensitive, and AI services built on these data are often very lucrative. Therefore, attackers and even the server have a strong incentive to steal the sensitive data and functionality of the client model. In addition to the unauthorized acquisition of private data, the compromising of the client model serves as a substantial target for attack. Deviating from conventional

attacks that primarily aim at illicitly reconstructing model parameters, the focus has shifted towards a more feasible target – stealing model functionalities. It solely necessitates the attacker’s model to obtain functions similar to those of the target model rather than the need for alignment on the parameter level– for instance, executing identical classification tasks, accomplishing the same mapping, and so forth. In scenarios where a computation provider (the server) and a data provider (the client) collaborate to train a SL model for profit, stealing the functionality of the client model allows the server to get rid of the client and perform the inference on its own without sharing the revenue earned by the SL model. Some recent works [14]–[16] have presented a series of attacks on SL. Feature-space hijacking attack (FSHA) [16], [17] points out that the server can hijack clients to uncover private inputs, but this server is malicious since it completely disrupts the process of SL, making this attack detectable by clients [18]. Besides, the server can’t steal the functionality of the client model due to the damaged SL model. While instigating a malicious attack may have detrimental effects on a server’s reputation due to the potential of client detection, the server tends to play a semi-honest role. A semi-honest server, also referred to as an honest-but-curious server, can gather, preserve, and process all the data exposed to it while executing in strict adherence to the protocol throughout the execution. UnSplit [15] is the state-of-the-art attack designed for a semi-honest server, which requires the knowledge of client model structure and the smashed data to reconstruct the client model and raw inputs. It uses a coordinate gradient descent approach to search over the space consisting of all possible input values and client network’s parameters, which is too large to converge. Once the learning task and the client model become slightly complex, its performance deteriorates dramatically and the attack fails. As for label inference attack, UnSplit [15] only works under the strong assumption that the client top model has only one layers (see Tab. VIII). In short, for a semi-honest server, existing attacks on SL mainly based on the idea of model inversion, which requires the knowledge of the client model structure and could fail due to the large search space as the client model gets deeper and more complex. Therefore, how to effectively steal the functionality, inputs and labels of the client in an undetectable way, even if the client model’s structure is unknown and complex, is still an open question.

To explore the answer to this question, in this work, we propose a novel and widely effective attack paradigm — Pseudo-Client ATtack (PCAT), to steal the functionality and data from the client. As aforementioned, conventional attacks first obtain smashed data and client model structure, and then invert the client model. Differently, the effectiveness of PCAT is based on our insights that a well-trained server model itself can provide sufficient information to construct a pseudo-client model to steal client’s functionality by using very limited training samples, even without using the smashed data. Moreover, we discover that a series of intermediate server models during normal SL can provide extra knowledge to the pseudo-client model to gain closer functionality. With these insights, our main idea is that the server can take full use of the knowledge learned by evolving server models to train a pseudo-client model to gain a functionality as close to that of the real client as possible, whose structure can be completely different from that of the real client model. Hence, PCAT doesn’t require any knowledge about the real client model. The only assumption is that the server can obtain a small dataset of few samples for the same learning task from any public sources, whose size is orders of magnitude smaller than the private training set. Once the pseudo-client model learns a mapping from inputs to the feature space of smashed data, the server can transform the given smashed data back to raw inputs by learning a reverse mapping. It is also able to replace the top model by a pseudo-top model to infer private labels.

The experiments show that the functionality stealing attack is highly resistant to traditional defense such as DP [19] mechanisms. Therefore, we undertake an investigation into targeted defense mechanisms against PCAT. The crux of our functionality stealing attack is on the similarity between the input-label pairs of the attacker and the victim client, allowing the attacker obtain a functionality closed to the victim model’s. Our defense strategy involves the victim claiming a counterfeit learning task, resulting an inconsistency between the attacker’s and the victim’s learning tasks, breaking the similarity between their input-label pairs, and thwarting the attacker’s ability to steal the victim’s model’s functionality. Moreover, we should ensure the victim client can convert the inference made under the claimed learning task into an inference under the real learning task during the prediction phase. We employ two methods: a one-to-one mapping technique and an autoencoder approach for generating the claimed learning task. Our experimental results have demonstrated that our defense mechanism can significantly destroy the performance of attack while safeguarding the performance of the SL baseline.

Furthermore, we improves PCAT to maintain its effectiveness under this specific defense mechanism. To alleviate the constraints of the server’s top model on the learning task, we introduce a pseudo-top model in place of the real top model. This enables the pseudo-top model to map the inputs of the real top model to the label space that is known by the server.

The main contributions of this paper are summarized as follows:

New attack: We propose a novel pseudo-client attack on SL, which, to the best of our knowledge, is the first attack enabling a semi-honest server to achieve three goals — functionality stealing, input data reconstruction and labels inference, without any preknowledge about the client model. Compared with previous attacks on SL, our attack has the following advantages: 1) It is widely effective since it suits all variants of SL and doesn’t require any knowledge of the client model; 2) It is effective in cases with more complex tasks and client models; 3) It is hard to detect since it’s transparent to clients; 4) Our functionality stealing attack doesn’t require smashed data, thus it is robust even if clients use defensive mechanisms.

![](images/3e3b7a177bbbb34a8f54cf047e2428f47293660ca065da27de3589acf4604a25.jpg)  
Fig. 1. Three typical variants of SL [3], [4]. Our attack mechanism is effective against all three variants.

New insights: We provide the insights that a server model in SL contains rich private information, though it doesn’t have access to any private data directly. A trained server model can be utilized to construct a pseudo-client model to gain the functionality of the real client, even without using any smashed data. Moreover, a series of intermediate server models can “guide” the pseudo-client model to reach a better performance. Thus, on the basis of the insights, we design PCAT that significantly outperforms state-of-the-art attacks in three attack goals. Our successful attacks also reveal the high risk of leaking privacy through the server model in SL, even when the client model structure and smashed data are protected.

New results: We implement PCAT on various benchmark datasets and models to verify its effectiveness. The results show that the server can use a very small dataset to gain a pseudo-client model whose functionality is very close to the real client. Our attack is also robust to non-i.i.d. situations when the server lacks training samples of some classes, as well as traditional defences.

New defenses: We introduce two label transformation defenses targeted to thwart PCAT. Compared with traditional defense mechanisms like differential privacy, these defenses not only mitigate the reduction in the accuracy of the SL baseline but also counter basic PCAT effectively. Therefore, we further improve PCAT to counter these two defense mechanisms.

# II. PRELIMINARIES AND RELATED WORK

# A. Split Learning

As a rising paradigm of distributed machine learning [20], split learning (SL) [4], [6], [7] is proposed for resourceconstrained data owners by letting the powerful server undertake the majority of computation. In SL, the ML model (usually a neural network) is split into several parts. Without loss of generality, the model is partitioned to a server model $( f _ { s } )$ and a client model $( f _ { c } ) ,$ and the function of the whole model is $f = f _ { s } ( f _ { c } ( \cdot ) )$ . The client model is allocated to the data owners, and the server model is at the place concentrating sufficient computing power. During the overall training phase, the server should be oblivious to any private information of the client.

There are three typical settings for SL [3], [4], [7], as presented in Fig. 1. In the single-client setting, the client transmits smashed data $( f _ { c } ( X ) )$ and labels to the server, and the server computes loss and gradients. Then the server performs backward propagation and sends gradients back to the client. Receiving the gradients, the client performs backward propagation, and both the server and client update their weights. It iterates in this way until the model converges. For the multi-client setting, the clients take part in training in a round-robin sequence. Each client updates its local model from the last client before training. As for the U-shape setting, a top model is split out and assigned to clients to protect private labels and clients need to calculate the loss.

# B. Attacks on Split Learning

Currently, a significant amount of research is dedicated to investigating machine learning attacks [21]. In SL, recently, several attacks [14]–[16], [22] are designed for the server to reconstruct the clients’ raw inputs, model parameters and labels. In FSHA [16], a malicious server can hijack clients to leak essential features about their raw data. However, due to that the server changes the learning task and disrupts the learning process, the malicious behaviors can be detected by clients [18] and the attacker can not steal clients’ functionality. UnSplit [15] provides the state-of-the-art attack on SL based on the assumption that the server has the client’s model structure, and a semi-honest server can reconstruct the raw inputs and parameters of the clients’ model by utilizing the smashed data. Since both the model parameters and the inputs are unknown, the solution space could be too large to converge once the client’s model or the learning task becomes more complex. Therefore, in practice this attack can easily fail when any of the following situations occur: 1) the structure of the client model is unknown; 2) the client model has more than one layer; 3) the learning task is complex; 4) the smashed data is protected by defense mechanism like differential privacy [19]. When attacking the U-shape SL, both norm-based label-uncovering method [22] and UnSplit [15] use gradients information to reconstruct private labels. However, these two attacks are only effective for the imbalanced binary classification setting or the setting where the top model contains only one layer.

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

Considering a model with a sufficiently large dataset as the victim model, denoted by F , the functionality stealing attack tries to construct a knockoff model using a small dataset, denoted by ${ \widetilde { f } } ,$ which behaves very much like $F .$ The most critical challenge is how to let F effectively teach $\widetilde { f }$ when the attacker has very limited training data.

Basic strategy: stealing after training. A basic solution is to train the victim model first, then let the victim model teach the knockoff model in the way of knowledge distillation [23]. As presented in Fig. 2(a) and (b), after training the victim model for N iterations on a large dataset, we obtain a welltrained model $F ^ { N }$ . Then the knockoff model $\widetilde { f }$ can be trained with the help of $F ^ { N }$ in the following way: in the n-th iteration, the inputs $( X _ { i } ^ { n } )$ from a small dataset are fed to both models, and the learning targets of $\widetilde { f }$ are the output soft labels of $F ^ { N }$ rather than the hard labels. The loss function is

![](images/c62d9d38b4b960b5567cd10a2cbaec946d2a5182381ed68ace74205911415684.jpg)



Fig. 2. Two strategies to construct a pseudo model $\widetilde { f }$ which steals the functionality of the victim model F . F is trained on a large dataset DataL and f is trained on a small dataset DataS with the help of F . N is the total number of iterations during training and $\tilde { n } \in [ 0 , N ]$ . That is, $F ^ { n }$ denotes the model after n iterations and $F ^ { N }$ denotes the final model after training. Before calculating LKLDiv, we need to perform log(sof tmax(pred/τ )) and τ is temperature [23].

![](images/5ce2dea89a77fdaee6d9deb38e79cc74d9d8b6e72df096237dbdbe362ab7a0ac.jpg)



Fig. 3. Two strategies to steal the client model in SL. (a) shows training two SL models on small $D a t a _ { S } )$ and large $\boldsymbol { D a t a _ { L } } )$ datasets independently. (b) and (c) illustrate the strategies that train a pseudo-client model $\widetilde { f _ { c } }$ to steal the functionality of the victim client model $F _ { c } ^ { ' }$ after and while training the server model, separately. $n \in [ 0 , N ] , F _ { s } ^ { N }$ denotes the final server model after SL and $F _ { s } ^ { n }$ denotes the intermediate server model after n iterations during the SL. F is the feature space of the smashed data. The red arrows indicate that under the restriction of $F _ { s } ^ { N }$ or $F _ { s } ^ { n }$ , the feature space of the pseudo-client’s outputs is learning to get closed to the feature space of the victim client’s outputs.

$$
\mathcal {L} _ {K L D i v} = K L D i v e r g e n c e L o s s \left(\text { soft } \left(\widetilde {\text { pred }} _ {i} ^ {n}\right), \text { soft } \left(\text { pred } _ {i} ^ {N}\right)\right), \tag {1}
$$

which is the KL divergence loss between the soft labels of two models.

By learning from the victim model, the performance of the knockoff model can often be obviously improved, e.g., from 73.52% to 82.06% in the handwritten digits classification task in Fig. 4(a), when the attacker has only 100 training samples (10 samples per class). However, there is still a significant gap from the performance of the victim model, which is 98.82%.

Our improved strategy: stealing while training. To further improve the performance of the knockoff model, we have the observation that a series of intermediate victim models during training can provide essential information, which can teach the knockoff model better than the final well-trained victim model does. Based on this observation, different from traditional knowledge distillation, we propose to steal the victim model while it is being trained. As illustrated in Fig. 2(c), in the n-th iteration, taking the same inputs from the small dataset, the optimization objective of ${ \widetilde { f } } ^ { n }$ is to minimize the KL divergence loss between the output soft labels of two current models. Note that, $F ^ { n }$ also takes inputs from the large dataset, and its optimization objective remains the loss on the hard labels. In this way, both $F ^ { n }$ and ${ \widetilde { f } } ^ { n }$ are trained synchronously. $F ^ { n }$ evolves by using the large dataset, while ${ \widetilde { f } } ^ { n }$ uses a sequence of evolving targets to train itself. Although at the beginning, learning targets are not as accurate as the final target, actually the evolving learning targets can “guide” ${ \widetilde { f } } ^ { n }$ to converge more precisely to the final target. As plotted in Fig. 4(a) and Fig. 4(b), our stealing while training strategy increases the accuracy of the knockoff model to 88.44%, which is significantly higher than the basic stealing after training strategy.

Algorithm 1: Stealing Client after Training Server (Vanilla-PCAT)   
Data: Server's data: $(X_{server}, y_{server})$ , total epochs:
N

/* Initialize models    */ $F_s^N$ is a well-trained server model; $\widetilde{f}_c$ is randomly initialized;
while n < N do
    Randomly select $(X_i, y_i)$ from $(X_{server}, y_{server})$ ; $\widetilde{smashed} \leftarrow \widetilde{f}_c(X_i)$ ; $\widetilde{z} \leftarrow F_s(\widetilde{smashed})$ ; $\widetilde{\mathcal{L}} \leftarrow \mathcal{L}(\widetilde{z}, y_i)$ ; $\widetilde{\nabla}_{smashed} \leftarrow \text{compute\_gradient}(smashed, \widetilde{\mathcal{L}})$ ; $\widetilde{\nabla}_c \leftarrow \text{compute\_gradient}(\widetilde{f}_c, \widetilde{\nabla}_{smashed})$ ; $\widetilde{f}_c' \leftarrow \text{update\_weight}(\widetilde{f}_c, \widetilde{\nabla}_c)$ ;
    /* The weight of $F_s$ isn't updated.
    */ 
end

# (2) Steal a Client Model in Split Learning

The aforementioned strategies cannot be directly applied to steal a client model in SL. Different from stealing a complete model, to construct a pseudo-client model, we still need to address the following challenges: 1) the server cannot obtain the intermediate client models during training, but only knows all intermediate server models; 2) the server cannot obtain the inputs nor the output soft labels, and even the smashed data cannot be used as aforementioned in Section III-A; 3) the server cannot even feed samples from its small dataset to the client model, otherwise the client will be aware of the attack.

Facing these challenges, w.l.o.g., we further analyze the single-client SL. As illustrated in Fig. 3(a), the client model maps raw inputs X to a certain feature space F. Then the server model maps intermediate activation from this feature space to logits. The SL model trained on a large dataset, denoted by $F = F _ { s } ( F _ { c } ( \cdot ) )$ , usually performs much better than the SL model trained on a small dataset, denoted by $f = f _ { s } ( f _ { c } ( \cdot ) )$ . As shown in Fig. 4(c), with 60,000 training samples, the SL model achieves 99.18%, while the accuracy is only 51.33% with 10 training samples (1 sample per class). Since the server aims to construct a pseudo model with good performance, it must make full use of the knowledge in the client’s large dataset. Therefore, we propose to steal the functionality of the client model by using only the server model(s) trained on the client’s dataset and a small dataset from the server itself. As we will present below, such strategies work surprisingly well, even though the server does not know the structure or input of the client model and does not query the client or use the smashed data at all.

![](images/3b5872f25dbfd62cb289d792fe6f3151024cc56a8f01ea210d267a0bcf92c1c3.jpg)



![](images/415caa2bbc2c397ab38bdda66393325b165f3eb59d13da0989d1bad404387ed3.jpg)



![](images/b213dc9a119363e25e066a721b7819d869cc53b597f7299ab909602544b4bb0e.jpg)



![](images/d41caec34cc4916a6af5ed376afaec36299dfed9983d4d1d8a1d1c0db9e60512.jpg)



Fig. 4. Performance of victim models and pseudo models obtained by different strategies. It uses LeNet-5 on MNIST dataset. (a) and (b) show the performance when stealing a complete model after and while the training of the victim model. (c) and (d) show the performance when stealing a client model after and while the training of the server model in SL. The split layer is 2. MSELoss is calculated between the smashed data output by the client model and the pseudo-client model, which characterizes the difference between $\widetilde { \mathcal { F } } ^ { N }$ and $\mathcal { F } ^ { N }$ . 60000, 100 are the amounts of training samples.

Algorithm 2: Stealing Client while Training Server (PCAT)   
Data: Server's data: $(X_{server}, y_{server})$ , Client's data: $(X_{priv}, y_{priv})$ , epochs: $N$ /* Initiate models */ $F_s, F_c, \widetilde{f}_c$ are all randomly initialized and $F_c \neq \widetilde{f}_c$ ;

For the client:   
while n < N do
    Randomly select $(X_{j}, y_{j})$ from $(X_{priv}, y_{priv})$ ;
    Smashed $\leftarrow F_{c}(X_{j})$ ;
    send_to_server(Smashed, $y_{j}$ );
    recv_from_server( $\nabla_{Smashed}$ ); $\nabla_{c} \leftarrow \text{compute\_gradient}(F_{c}, \nabla_{Smashed})$ ; $F_{c}' \leftarrow \text{update\_weight}(F_{c}, \nabla_{c})$ ;
end

For the server:   
```txt
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
    ∇_Smashed ← compute_gradient(Smashed, L);
    ∇_c ← compute_gradient(f_c, ∇_Smashed);
    f_c ← update_weight(f_c, ∇_c);
    send_to_client(∇_Smashed);
    F_s' ← update_weight(F_s, ∇_s);
    // F_s updates weight using grad from SL.
end 
```

Our basic strategy for SL: stealing client after training server. As illustrated in Fig. 3(b), the server conducts the normal SL first. After N iterations, the input X is mapped to the feature space $\mathcal { F } ^ { N }$ by the victim client model $F _ { c } ^ { N }$ . The server model F Ns $\dot { F } _ { s } ^ { N }$ s is well-trained and capable to convert the smashed data in $\mathcal { F } ^ { N }$ to logits. Now the server can connect a pseudo-client model $( \widetilde { f } _ { c } )$ to the trained server model $F _ { s } ^ { N }$ , and use its small dataset to train $( \widetilde { f } _ { c } )$ while fixing the parameters of $F _ { s } ^ { N }$ . The pseudo-client model actually maps inputs to another feature space $\widetilde { \mathcal { F } } ^ { N }$ . To steal the functionality of the victim client model $F _ { c } ^ { N }$ , the training algorithm for the pseudo-client model should optimize its output smashed data as close to $\mathcal { F } ^ { N }$ as possible, so that the smashed data can be classified by the server model correctly. The detailed training algorithm is presented in Algorithm 1. Note that, it is not necessary for $f _ { c }$ to have the same structure as the victim client model $( F _ { c } )$ , as long as it can learn the mapping from raw inputs the to feature space. The experimental results in Fig. 4(c) and (d) show that, this strategy can increase the accuracy of the server’s pseudo model from 51.33% to 83.05% when the server has only 10 samples.

Our advanced strategy for SL: stealing client while training server. Similar to the advanced strategy when stealing a complete model, we find that using a sequence of intermediate server models $F _ { s } ^ { n } , \ n \ \in \ [ 0 , N ]$ during SL, the server can train the pseudo-client model gradually to achieve better performance. In another words, the pseudo-client model can leverage a series of learning targets $\left\{ \begin{array} { l }  { \mathcal { F } } ^ { 0 } , \ldots , { \mathcal { F } } ^ { N } \right\} \end{array}$ to steal the functionality more accurately. This strategy is feasible since the server knows the intermediate server model for every iteration. Fig. 4(c) testifies that using evolving server models can greatly improve the pseudo-client model’s accuracy, from 83.05% to 90.7% in our experiments. Fig. 4 (d) further illustrates that the adversarial feature space $\widetilde { \mathcal { F } } ^ { N }$ is very close to the victim feature space $\mathcal { F } ^ { N }$ by this strategy. Note that, without the constraints from the well-trained server models, the feature space of smashed data in an independently trained pseudo model is quite far away from the victim feature space $\bar { \mathcal { F } } ^ { N }$ . Comparied with the basic strategy - stealing after training, this strategy leads to a narrow time window to perform the attack. However, saving the parameters of the server model in each iteration of the split learning baseline can extend the attack time window, accompanied with generating huge storage overhead.

Summaries: We have insights that a server model trained by standard SL can provide sufficient knowledge to train a wellperforming pseudo-client model using very limited training samples; a series of intermediate server models during SL can significantly improve its accuracy. These insights not only inspire us to design a highly effective attack mechanism against SL, but also reveal the privacy threats posed by the server model in SL. Based on these insights, our main idea to steal the functionality of the client model is to train a pseudoclient model with any structure that can map inputs X to the target feature space $\dot { \mathcal { F } } ^ { N }$ . Once the pseudo feature space $\widetilde { \mathcal { F } } ^ { N }$ is sufficiently close to $\mathcal { F } ^ { N }$ , the pseudo-client model can take place of the victim client model. Then, using the pseudoclient model and smashed data of client’s inputs, the server can reconstruct the private inputs of the client by learning a reverse mapping, as well as infer their labels.

![](images/09507c085a7826a5dce899a035cd857a33c07cc985a7ebbefb3dca30ece22123.jpg)



Fig. 5. Pseudo-client attack in two-part SL and U-Shape SL. The server constructs a pseudo-client model $\widetilde { f _ { c } } ^ { N }$ by the PCAT algorithm. With $\widetilde { f _ { c } } ^ { N }$ , the server can perform inference without the involvement of the victim client. During the normal SL, the server stores smashed data (denoted as $X _ { s m a s h e d } )$ of the victim client. Using $\widetilde { f _ { c } } ^ { N }$ , the server can train an reverse mapping $f ^ { - 1 }$ and reconstruct the client’s private inputs $X _ { p r i v }$ in two steps.

# IV. PSEUDO-CLIENT ATTACK

In this section, following our main idea, we present the detailed design of our attack mechanism, the Pseudo-Client ATtack (PCAT), on different variants of SL. The whole attack process is illustrated in Fig. 5. We also present some details that makes PCAT more effective.

# A. Functionality Stealing

Algorithm 1 has already illustrated how to train a pseudoclient model after the server model has been trained in a normal SL. To further improve the performance of the pseudoclient model, our insights guide us to take full use of a series of intermediate server models. Specifically, the server initializes the pseudo-client model before the SL starts and then trains both pseudo and real client models simultaneously. For each iteration, the victim client performs its forward propagation and sends the smashed data and labels to the server. Then the server selects training samples from its own dataset with the same labels as those uploaded by the client, i.e., $y _ { s e r v e r } = y _ { p r i v } ,$ and feeds these samples into the pseudoclient model to obtain the smashed data. For both pseudo and victim client models, the server model takes their respective smashed data as input, performs forward propagation and calculates the loss, separately. For SL, the server computes the gradients of smashed data and sends the gradients back to the victim client. The victim client calculates the local gradients and updates the client model. For pseudo-client training, based on the loss, the server calculates the gradients of its own smashed data and the pseudo-client model, with which the pseudo-client model is updated. At the end of each iteration, the server model is updated using only the gradients from normal SL with the victim client. Algorithm 2 presents the details of the attack process. Since both the victim client model and the server model are updated based on only the gradients of normal ${ \mathrm { S L } } ,$ , the whole training process is the same as a normal SL in the client’s view. Therefore, this attack is transparent to clients.

In multi-client SL, each client participates in a roundrobin mode to train the client model, so all clients obtain the same client model after SL. From the server’s perspective, the evolution of the server and client model is the same as that in single-client SL. Therefore, the server can apply PCAT to multi-client SL directly without any modification.

# B. Inputs Reconstruction

After stealing the functionality, the server obtains a pseudoclient model that maps inputs to a feature space of smashed data, which is very close to the real feature space in SL. Given smashed data from the victim client $( X _ { s m a s h e d } )$ , the server can reconstruct the private raw inputs $( X _ { p r i v } )$ by reversing the mapping. As presented in Fig. 5, we propose to reconstruct the client’s inputs using the following steps:

(1) Train a reverse mapping $f ^ { - 1 } \colon$ since the server has a few training samples, it can train a reverse mapping $f ^ { - 1 }$ to map smashed data from the feature space back to the input space. Specifically, the server maps raw training samples to smashed data by using the pseudo-client model, then trains $f ^ { - 1 }$ to map them back to raw inputs. The reverse mapping is composed of transposed convolution and upsample layers to transfer smashed data from low resolution to high resolution. The specific reverse mapping we use for every model splitting is shown in Appendix.   
(2) Coarse-grained reconstruction and fine-tuning: the server can feed $X _ { s m a s h e d }$ into $f ^ { - 1 }$ to obtain the reconstructed inputs( $X _ { r e c } )$ . However, due to the insufficient training samples in server, $X _ { r e c }$ is usually coarse-grained. To achieve more precise reconstruction, we design a fine-tuning method which takes the coarse-grained $X _ { r e c }$ from $f ^ { - 1 }$ as inputs and the real smashed data $X _ { s m a s h e d }$ as learning targets. Towards the targets, the server optimizes and fine tunes $X _ { r e c }$ with fixed pseudo-client model $\overrightharpoon { f } _ { c } ^ { N }$ , until the output smashed data of $\widetilde { f } _ { c } ^ { N }$ is close enough to $X _ { s m a s h e d } .$ . In this way, we can obtain a more fine-grained reconstruction.   
Note that, we steal the functionality of the client model in a totally different way from UnSplit, thus the input reconstruction is also different from UnSplit. Specifically, UnSplit adopts the client model structure and smashed data to search the client model parameters and inputs simultaneously. While PCAT first learns a pseudo-client model using only the server model and

![](images/fcc5b876cbad2fc9cce81de73637007319c65a816006947be2237bb00eacb1f4.jpg)



Fig. 6. Functionality gap between the pseudo model and the victim model, which is measured by the inference accuracy decrease of $F _ { s } ( \widetilde { f _ { c } } ( \cdot ) )$ compared with $F _ { s } ( f _ { c } ( \cdot ) )$ . The experiment is performed on MNIST and CIFAR-10 dataset.The inference accuracy of the baseline $F _ { s } ( f _ { c } ( \cdot ) )$ is 99%/93.2% for MNIST/CIFAR-10.“Samples/Class” means the number of samples per class in the server’s dataset.

![](images/a7b08791e31349bde72fe39c95c215df6fb37aa3765247e01622c83ea74dd0ee.jpg)



Fig. 7. Inference accuracy of the pseudo model $F _ { s } ( \widetilde { f _ { c } } ( \cdot ) )$ by skipping batches in the early training. The experiment is performed on MNIST dataset, where the server has one sample per class. The pink and light blue lines denote the test accuracy and loss of SL baseline in the first epoch. The black dots mean the final test accuracy of $F _ { s } ( \widetilde { f _ { c } } ( \cdot ) )$ ) if $\widetilde { f _ { c } }$ starts to train from a certain batch idx.

a small training dataset of the server, and then learns a reverse mapping with the server’s training data. The smashed data are used for fine-tuning. Since PCAT reconstructs the inputs after the pseudo-client model is well constructed, the search space is significantly smaller than that of the UnSplit. Our experiments verify that PCAT reconstructs raw inputs more precisely than UnSplit.

# C. Attack on U-Shape Split Learning

In U-shape SL, as shown in Fig. 5, there are a bottom model $F _ { c }$ and a top model $F _ { t }$ placed on the client side. The server needs to train a pseudo-client model $\widetilde { f } _ { c }$ as well as a pseudotop model $\widetilde { f } _ { t } .$ . By using the same strategy in two-part SL (i.e., Algorithm 2), the server can obtain $\widetilde { f } _ { c } ^ { \ N }$ and $\boldsymbol { \widetilde { f } } _ { t } ^ { N }$ and perform inference alone. With $\widetilde { f } _ { c } ^ { ~ N }$ , the private inputs of the client can also be reconstructed by the methods in Section IV-B.

Unlike two-part SL where clients send data labels to the server, in U-shape SL labels are considered as privacy and protected from the server by the top model. Since PCAT can construct a pseudo-top model to replace the real top model, the server can feed smashed data of the victim client to the pseudo-top model to infer their private labels.

# D. Other Details to Improve PCAT

1) Aligning labels: When attacking two-part SL by Algorithm 2, the server aligns labels of the training samples for the pseudo and victim client models, i.e., to make $y _ { s e r v e r } = y _ { p r i v } .$ For the attack on U-shape SL, due to the invisibility of the client’s labels, the server randomly selects $X _ { s e r v e r }$ for each iteration. We measure the functionality of the pseudoclient model with and without label alignment. Fig. 6 shows that the inference accuracy gap between the pseudo model $F _ { s } ( \widetilde { f _ { c } } ( \cdot ) )$ and the victim model $F _ { s } ( f _ { c } ( \cdot ) )$ is only 1.09%/1.95% with/without label alignment on MNIST and 6.01%/9.06% on CIFAR-10, when there are 25/100 samples per class in the server’s dataset. The results testify that PCAT can steal the functionality of the victim model with high accuracy; and label alignment can increase the pseudo-client model’s accuracy. We believe the reason is that the gradients of pseudo and victim client models depend in their respective inputs and labels. Aligned training samples can make the gradients of two client models closer, thus the optimization directions of $F _ { s }$ and $\ddot { f _ { c } }$ are more consistent.

2) Late start: In the early stages of SL, since the victim model hasn’t started to converge, the unstable server model could guide the pseudo-client model to a wrong direction. Thus, the pseudo-client model can skip some batches in the early stages to avoid being misled and gain a better performance. The experiment results in Fig. 7 show that a proper late start can improve the performance of the pseudo model. For example, when the pseudo model training starts from the 100-th batches, the inference accuracy can be raised from 89.57% to 91.05%. But the training should not start too late, otherwise the victim model has already begun to converge and the pseudo model will miss a portion of guidance information. The server should starts to train the pseudo-client model at the time when the test accuracy of the victim model starts to rise and the loss starts to fall. Note that, even if the start time is not optimal, the pseudo-client model still performs better than that trained after the SL is over (i.e., the pseudoclient model trained by using vanilla-PCAT).

# V. IMPLEMENTATIONS

To demonstrate the effectiveness and practicality of PCAT, we implemented PCAT for a variety of learning tasks and models, as well as different settings of split learning.

# A. Datasets and Models

We implemented PCAT for the following cases with different popular models and benchmark datasets, which cover situations where the models and tasks are simple or complex.

<table><tr><td></td><td>Dataset</td><td>Model</td><td>Param</td><td>Complexity</td></tr><tr><td>1</td><td>MNIST</td><td>LeNet-5</td><td>61.5K</td><td>Low</td></tr><tr><td>2</td><td>CIFAR-10</td><td>VGG16</td><td>14.6M</td><td>Medium</td></tr><tr><td>3</td><td>Tiny-Imagenet</td><td>MobileNet</td><td>28.5M</td><td>High</td></tr></table>

Table I. The settings for all cases and their complexity comparison.

# B. Data Processing

We assume that the server’s and the client’s datasets should be prepared for the same learning task. We consider two typical cases: 1) the server’s dataset is a subset of the client’s private dataset, i.e., $X _ { s e r v e r } \subset X _ { p r i v } ; 2 )$ the server’s dataset has no intersection with the client’s private dataset, i.e., $X _ { s e r v e r } \bigcap X _ { p r i v } = \varnothing$ .

For training, we randomly divide the training set of each benchmark dataset into a public dataset $X _ { p u b }$ and a private dataset $X _ { p r i v }$ , and $X _ { p u b } \colon X _ { p r i v } = 1 \colon 9 . \mathrm { ~ } X _ { p r i v }$ is allocated to victim clients as the training set of the split learning. $X _ { p u b }$ is a public dataset that the server can retrieve some samples from it to compose its training set $X _ { s e r v e r } $ . If not specified, we make $X _ { s e r v e r }$ and $X _ { p r i v }$ i.i.d. We will also analyze the effectiveness of PCAT in non-i.i.d. cases. To evaluate the generalizability of PCAT, we also let the server use datasets( $X _ { d i f } )$ very different from $X _ { p r i v } .$ . In our ablation study, $X _ { d i f }$ is a subset of Imagenet [24] while $X _ { p r i v }$ is from CIFAR-10. The samples in $X _ { d i f }$ have the same labels as the labels in CIFAR-10. For testing, we use the original testing sets to evaluate models.

# C. Model Splitting

We adopt LeNet-5 [25], VGG16 [26], MobileNet [27] to validate the effectiveness of our attack. We consider various model splitting strategies, as shown in Fig. 8. For two-part split learning, each model split into 2 parts. We split MobileNet from 1 to 4 layers to show that PCAT is robust to the cases that client’s model is extreme complex. For U-shape split learning, the client has one or two bottom layers and one or two top layers, while the intermediate layers are allocated to the server.

![](images/273371d9a59405c45183844ee43d84fee83dbc580b41b7dc36f0a88ca07175ed.jpg)



Fig. 8. Model splitting strategies. We omit batchnorms and ReLU in VGG16 and MobileNet.

# VI. EXPERIMENTAL RESULTS

Based on the implementation in Sec. V, we conduct comprehensive experiments to demonstrate the effectiveness of PCAT on three attack goals in Sec. III-A, including stealing the functionality of the client model, reconstructing the private inputs, and inferring the labels. The results of successful attacks on different models and datasets testify the broad applicability of PCAT.

# A. Functionality Stealing

# (1) PCAT for Two-part SL

In i.i.d. settings. We first launch our pseudo-client attack in the case that $X _ { s e r v e r }$ and $X _ { p r i v }$ are i.i.d. and $X _ { s e r v e r } ~ \subset ~ X _ { p r i v }$ . We split each model from layer 2 to

<table><tr><td rowspan="2"></td><td colspan="3">Pseudo client</td><td rowspan="2">Victim client</td></tr><tr><td>Simple</td><td>Same</td><td>Complex</td></tr><tr><td>Model</td><td></td><td></td><td></td><td></td></tr><tr><td>Acc(%)</td><td>73.60</td><td>97.17</td><td>97.13</td><td>99.06</td></tr><tr><td>MSE</td><td>0.387</td><td>0.133</td><td>0.141</td><td>0</td></tr></table>

Table II. Performance of PCAT on MNIST, when the pseudo-client model has simpler, the same, or more complex structures than the client. The server has 5 samples per class.

make the client model more complex. For MNIST, CIFAR-10 and Tiny ImageNet, the server has 5, 250, and 10 training samples per class. Fig. 9 shows the performance of the pseudo model constructed by PCAT and Vanilla-PCAT on three datasets. Both vanilla-PCAT and PCAT effectively steal the functionality of the client model. When the server trains a complete model independently using only its own data $X _ { s e r v e r }$ , its accuracy is only 63.38%, 74.16%, and 13.62% on three datasets, respectively. With the same dataset $X _ { s e r v e r } ,$ Vanilla-PCAT achieves 91.67%, 85.62%, and 69.8% accuracy, respectively. PCAT further increases the inference accuracy to 96.89%, 89.48%, and 73.46%, which are very close to the performance of the victim SL model. Vanilla-PCAT converges faster than PCAT, because its training is directly guided by the well-trained server model. Though converging slower, PCAT achieves much better accuracy because of the guidance of evolving server models, which drives the output feature space of the pseudo-client model closer to that of the victim client model.

Intuitively, the more samples the server has, the better performance PCAT can achieve. Fig. 10 illustrates the intuition. On MNIST, when the sample number for each class increases from 1 to 25, the accuracy achieved by PCAT grows from 90.77% to 97.91%. On CIFAR-10, when the sample number for each class increases from 10 to 250, the accuracy achieved by PCAT grows from 49.03% to 89.42%. On Tiny ImageNet [28], when the sample number for each class increases from 1 to 25, the accuracy achieved by PCAT grows from 45.40% to 77.11%. Compared with the size of the private dataset, which are 54000, 45000, and 90000, (5400, 4500, 450 samples per class) respectively, PCAT requires only a small number of training samples to effectively steal the functionality. And surprisingly, PCAT can achieve a fairly good attack on LeNet-5 even if there is only 1 sample per class.

# In non-i.i.d. settings.

Now we consider a more common situation that the dataset of the server lacks samples of some classes. In Fig. 11, (a) and (b) illustrate the cases that the server lacks one class of samples, e.g., the digit “3” in MNIST and class “deer” (labeled “4”) in CIFAR-10. When the server independently trains a complete model, the model cannot recognize the missing class at all, and the accuracy of related classes also drops significantly. Vanilla-PCAT can recognize most samples in the missing class and achieve 78.91%/51.5% accuracy on MNIST/CIFAR-10, but there is still an obvious gap with the 99.11%/95.2% (on MNIST/CIFAR-10) baseline. PCAT significantly mitigates the effect of the missing class and achieves 94.95%/70.2% accuracy on MNIST/CIFAR-10. Moreover, the overall performance of PCAT is very close to the SL baseline.

![](images/ed1082de6bdfa98b6f32cce5627428806482a2cc836f1c0addc28ae902c13066.jpg)



![](images/9470a713b93b066f085a427927f0566cd66f6386b5d68c2222daf8450954a038.jpg)



![](images/fb474709797f3a0cd7e77c04bc315287c4434e042e723895c069b09a8682a74c.jpg)



Fig. 9. Performance of the pseudo model constructed by PCAT on three datasets. For MNIST, CIFAR-10 and Tiny ImageNet, the server has 5, 250 and 10 training samples per class, respectively. $X _ { s e r v e r } \subset X _ { p r i v }$ and all models split from layer2. Independent training means the server training a complete model using only its own data Xserver. SL baseline is the victim model trained on $X _ { p r i v }$ . The MSELoss represents the distance between the real feature space and the pseudo feature space.

![](images/36b4cd849fc3afa74385e9c07dd7b0b14fff2de6035ca2993ab13a4431b3c18d.jpg)



![](images/2be9d6c604164087c0d93d82e528aa0dda1785601d36e597e76158e2752e0a5c.jpg)



![](images/f5b0881ee96ba9e0979f282181bbfa02af3c1357f053cbfbbe16d410e0a83008.jpg)



Fig. 10. Performance of PCAT changes with the number of training samples owned by the server. All models split from layer2 and $X _ { s e r v e r } \subset X _ { p r i v } .$   
![](images/1a3e7579cbb8ad79d168feccfabf4f595b16c9ee13b059274675e4ae3f601ac2.jpg)



![](images/b955c46ccaec853367a84a5e29cbe3fd45ffd42e94088cc8fcdcd13f3ecede71.jpg)



![](images/be6f15e46780d35615d05d32af4e044699ac3268a4fa820690d044331193f0b4.jpg)



![](images/3170a57733b436014b69e23b3aba082f4816ad79e6afad88652f316fc1b4b449.jpg)



Fig. 11. Performance of PCAT in non-i.i.d. settings on MNIST/CIFAR-10. (a) and (b) show the accuracy gap when $X _ { s e r v e r }$ lacks one class (“3”/“4” for MNIST/CIFAR-10). (c) and (d) present accuracy changing with the amounts of classes in Xserver.

<table><tr><td rowspan="2"></td><td colspan="4">Pseudo client</td><td rowspan="2">Victim client</td></tr><tr><td>Simple</td><td>Same</td><td>Complex</td><td>Other</td></tr><tr><td rowspan="3">Model</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>MaxPoolConv2d</td><td>MaxPoolConv2d</td><td>MaxPoolConv2d</td><td>ResBlock</td><td>MaxPoolConv2d</td></tr><tr><td>MaxPoolConv2d</td><td>MaxPoolConv2d</td><td>MaxPoolConv2d</td><td>ResBlock</td><td>MaxPoolConv2d</td></tr><tr><td>Acc(%)</td><td>87.54</td><td>88.90</td><td>88.35</td><td>84.96</td><td>93.20</td></tr><tr><td>MSE</td><td>0.0279</td><td>0.0134</td><td>0.0166</td><td>0.0511</td><td>0</td></tr></table>

Table III. Performance of PCAT on CIFAR-10, when the structure of the pseudo-client model is simpler, the same, more complex than the victim client model, or even use other elementary structure. The server has 250 samples per class.

(c) and (d) further analyze how the overall accuracy affected by the number of missing classes in the server’s dataset. Compared with independent training, PCAT is much more robust to non-i.i.d. datasets. On MNIST, The accuracy of PCAT is still over 90% even if 4 classes are missing. On CIFAR-10, PCAT can use only 3 classes to achieve the same performance as Vanilla-PCAT with 9 classes. We think that the reason behind the surprising result is that a subset of classes can represent the mapping functionality of the client model.

Performance of different pseudo-client model structures. In PCAT, the server does not know the structure of the victim client model, and only knows learning task and its input and output formats. It can adopt any structure that works for the task as the pseudo-client model. We evaluate PCAT in cases that the structure of pseudo-client model is simpler or more complex than the victim client model. Table II presents the performance with different variants of pseudo-client model on MNIST. We also consider the situation that convolution layers are replaced by ResBlock [29] on CIFAR-10 [30] and present the results in Table III. Both tables show that when the pseudoclient model has the same structure as the victim model, it achieves the best performance. A more complex pseudo-client model can achieve almost the same performance as the same structure does, while two simpler structures suffer performance degradation to different degrees. We think the reason is that the simpler the model, the less qualified to learn the behaviors of the victim client model. Therefore, in practice, a more complex pseudo model has a higher chance to successfully steal the functionality of a SL model.

<table><tr><td>Datasets</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Methods</td><td>UnSplit [15]</td><td>PCAT</td><td>UnSplit [15]</td><td>PCAT</td></tr><tr><td>SL Baseline</td><td>98.00</td><td>99.00</td><td>71.00</td><td>93.20</td></tr><tr><td>split layer = 1</td><td>93.75</td><td>98.75</td><td>43.69</td><td>91.10</td></tr><tr><td>split layer = 2</td><td>63.3</td><td>96.79</td><td>22.12</td><td>78.57</td></tr></table>

Table IV. Comparison on functionality stealing performance (Acc: %) with UnSplit [15]. In PCAT, the attacker has 5 samples per class from $X _ { p r i v }$ in MNIST and 50 samples per class from $X _ { p r i v }$ in CIFAR-10

<table><tr><td colspan="6">MNIST</td></tr><tr><td>Samples / Class</td><td>1</td><td>2</td><td>5</td><td>10</td><td>25</td></tr><tr><td>Acc(%)</td><td>72.30</td><td>84.27</td><td>91.83</td><td>93.27</td><td>96.98</td></tr><tr><td colspan="6">CIFAR-10</td></tr><tr><td>Samples / Class</td><td>10</td><td>25</td><td>50</td><td>100</td><td>250</td></tr><tr><td>Acc(%)</td><td>36.31</td><td>65.42</td><td>76.16</td><td>82.56</td><td>93.28</td></tr></table>

Table V. Functionality stealing results of U-Shape PCAT. It is on MNIST/CIFAR-10 with bottom layer2, top layer2/layer1 and $X _ { s e r v e r } \subset X _ { p r i v } .$

Comparison with previous work. We compare PCAT with the most related work UnSplit [15], which is the SOTA method for a semi-honest server to steal the functionality of the client model and reconstruct the raw inputs and labels. The main difference is that UnSplit requires the server to know the structure of the victim client model while PCAT treats the victim client as a black box. Table IV compares their ability to steal functionality. PCAT significantly outperforms UnSplit in all cases with different models, datasets and splitting strategies. For example, on MNIST, when the client has two layers, the accuracy of UnSplit is only 63.3%, while PCAT achieves 96.79%. On CIFAR-10, with a more complex model, the accuracy of UnSplit is only 22.12%, while PCAT achieves 78.57%.

(2) PCAT for U-Shape SL As illustrated in implementation in Sec. V, we also implement a U-Shape LeNet-5/VGG16 split learning on MNIST/CIFAR-10, which has two bottom layers and two/one top layers on the client side. We use PCAT to successfully steal the functionality of the U-Shape split learning model. Results in Table V show that U-Shape PCAT achieves 96.98%/93.28% accuracy when there are 25/250 samples per class in the server’s dataset. Hence, PCAT can be applied to attack a wide range of split learning, including two-part SL and U-shape SL.

# B. Input Data Reconstruction

After stealing the functionality of the victim client model, following the method in Section IV-B, the server can reconstruct the private inputs of the client. We present our reconstruction results for two-part split learning on Tiny-ImageNet and compare them with UnSplit in Table VI. Obviously, the images reconstructed by our method are much more informative and clearer than those reconstructed by UnSplit.

We also make quantitative analysis of reconstruction result of PCAT and UnSplit by calculating the SSIM [31] index between reconstructed images and the groundtruth. The comparison is shown in Fig. 12. Obviously under the same condition, PCAT can reconstruct raw inputs with much higher similarity. Especially, when the client model and the learning task are complex, e.g., the client model has two layers from VGG16 on CIFAR-10, UnSplit almost fails to reconstruct the input images, while our method can still reconstruct the input images with fairly good clearness.

<table><tr><td></td><td colspan="3">UnSplit</td><td colspan="3">PCAT</td></tr><tr><td>truth</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>layer1</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>layer2</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>layer3</td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

Table VI. Comparison of data reconstruction on Tiny-ImageNet between UnSplit [15] and PCAT.   
![](images/36f309bc4714ddd2674f2eefbcb11f0c474e2f2a63ed88f286d9745b0dfe19d5.jpg)



Fig. 12. The cdf curves of ssim [31] index between reconstruction results and ground truth on CIFAR-10 testsets, which shows that PCAT can recover private inputs with much more structural similarity.

We also evaluate our input reconstruction method for Ushape split learning and non-i.i.d. setting. The results are shown in Fig. 13. For U-shape learning, our method can also clearly reconstruct the private inputs. More importantly, in the non-i.i.d. setting, though the server lacks samples of some classes, it can still reconstruct the inputs of the unknown classes. This is a serious privacy breach since the server steals the data it has never seen before from the client.

# C. Label Inference

Based on the pseudo-client model, we conduct label inference attack on U-shape split learning on MNIST/CIFAR-10 Datasets. As shown in Table VII, PCAT achieves high accuracy in label inference, which is 98.23%/93.23% when the server has 25/250 samples per class. Also, we compare PCAT with UnSplit [15] in label inference in Table VIII. When the top model has one layer, the inference accuracy of PCAT is 98.82%/93.42%, which is slightly lower than Unsplit. But, when the top model becomes more complex, e.g. having two layers, the inference accuracy of UnSplit severely drops to 9.1%/8.1%, while PCAT still achieves a high accuracy (96.58%/92.57%). Therefore, PCAT is more robust to various split learning models.

# D. Against traditional defensive mechanisms

Differential privacy can provide a rigorous mathematical privacy guarantee [32], making it a widely adopted privacy protection approach in Split learning. To be more specific, when the victim client receives gradients from the server, it will add Laplacian noise under $\mathrm { D P s }$ guarantee. Thus, the client can protect its model and the next smashed data sent to the server. The results are shown in Table. IX: though the accuracy of baseline decreases as the noise becomes larger, the accuracy gap between the baseline and pseudo-client is steady at a certain level. Based on the results we can conclude that DP is not effective against our attack.

ground truth   
![](images/ae0796ff99abc41c32baafc265f0f2b61f0d8768566d2ba8de04360f02de8b60.jpg)



U-Shape PCAT   
![](images/299f0458233e433be961c034aafdfd52a029ebe5f67d7dabc51648380f55da48.jpg)



Non-i.i.d.   
![](images/b29b75e2882119f3b43505bed5469cdbd68ac620a8b865b1f183a2ba7411a747.jpg)



Fig. 13. Data reconstruction results on MNIST and CIFAR-10 in noni.i.d. and U-shape cases. For U-Shape split learning, the server has 5/20 (MNIST/CIFAR-10) samples per class from $X _ { p r i v } ,$ , with bottom layer = 1 and top layer = 2. For the non-i.i.d. case, split layer = 1; the server lacks samples from class “3”/ “deer” (MNIST/CIFAR-10) and has 5/20 samples from $X _ { p r i v }$ for each other class, but it can still reconstruct the missing classes accurately. 

<table><tr><td colspan="6">MNIST</td></tr><tr><td>Samples / Cls</td><td>1</td><td>2</td><td>5</td><td>10</td><td>25</td></tr><tr><td>Acc(%)</td><td>82.65</td><td>94.42</td><td>96.58</td><td>96.89</td><td>98.23</td></tr><tr><td colspan="6">CIFAR-10</td></tr><tr><td>Samples / Cls</td><td>10</td><td>25</td><td>50</td><td>100</td><td>250</td></tr><tr><td>Acc(%)</td><td>19.29</td><td>89.10</td><td>92.83</td><td>93.08</td><td>93.23</td></tr></table>

Table VII. Label inference accuracy of PCAT on U-shape split learning. It is implemented on MNIST/CIFAR-10 with bottom layer2 and top layer2/layer1. $X _ { s e r v e r } \subset X _ { p r i v } .$

# VII. TARGET DEFENSES

Given the failure of traditional defensive mechanisms in countering our attack, we try to seek potential defenses against our attack. We posit that the success of Pseudo-Client Attack can be attributed to the similarity in learning tasks and datasets between the pseudo-client and the victim client. This allows their jointly owned server model to generate comparable gradients under similar input-output pairs, enabling the pseudoclient to steal the functionality of the real client. To counteract such attacks, we propose that the victim client could claim an inconsistent learning task to the server, thereby rendering the input-output pairs incongruous and preventing the generation of similar gradients. This would prevent the pseudo-client from stealing functionality of the victim client and, hence, thwart this attack.

However, since the split learning baseline trains the learning task claimed by the victim client, rather than the actual learning task it aims to train, it is vital to examine how to design the claimed learning task given the real learning task. If these two tasks are unrelated at all, the victim client would learn nothing related to its actual learning task from split learning. Therefore, we propose that the claimed learning task should be correlated to the real learning task, such that it can be easily converted to the inference in the real learning task from the one in the claimed learning task through a simple mapping, thus the victim client can guarantee that the real learning task is well-trained from split learning while cotraining the claimed learning task with the server.

<table><tr><td>Datasets</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Methods</td><td>UnSplit</td><td>PCAT</td><td>UnSplit</td><td>PCAT</td></tr><tr><td>top layer = 1</td><td>100.0</td><td>98.82</td><td>100.0</td><td>93.42</td></tr><tr><td>top layer = 2</td><td>9.1</td><td>96.58</td><td>8.1</td><td>92.57</td></tr></table>

Table VIII. Comparison on label inference accuracy(%) with UnSplit [15]. In PCAT, the attacker has 5/100 samples per class from $X _ { p r i v }$ in MNIST/CIFAR-10.

<table><tr><td colspan="5">MNIST</td></tr><tr><td>σ</td><td>+∞</td><td>70</td><td>60</td><td>50</td></tr><tr><td>Baseline Acc(%)</td><td>99.00</td><td>94.10</td><td>90.79</td><td>84.71</td></tr><tr><td>PCAT Acc(%)</td><td>97.31</td><td>91.12</td><td>88.66</td><td>80.84</td></tr><tr><td>Acc(%) Gap</td><td>1.69</td><td>2.98</td><td>2.13</td><td>3.87</td></tr><tr><td colspan="5">CIFAR-10</td></tr><tr><td>σ</td><td>+∞</td><td>200</td><td>100</td><td>50</td></tr><tr><td>Baseline Acc(%)</td><td>93.20</td><td>85.18</td><td>80.17</td><td>73.17</td></tr><tr><td>PCAT Acc(%)</td><td>86.50</td><td>77.45</td><td>71.14</td><td>68.34</td></tr><tr><td>Acc(%) Gap</td><td>6.70</td><td>7.73</td><td>9.03</td><td>4.83</td></tr></table>

Table IX. The functionality performance of PCAT against the SL with differential privacy [19] defense. It is performed on MNIST/CIFAR-10, with split layer2/layer1. The server obtains 5/100 samples per class and   
$X _ { s e r v e r } \subset X _ { p r i v }$

Fig. 14 illustrates how the victim client’s defense works. The labels of samples from train set and test set of the victim client’s private dataset, corresponding to the real learning task, are denoted as $y _ { p r i v }$ and $y _ { t e s t }$ respectively. To safeguard the real learning task, the victim client devises the claimed learning task, wherein each sample is labeled yˆ. During the SL training process, $y _ { p r i v }$ is transformed into yˆ through the designed mapping, and the victim client sends $\hat { y }$ instead of $y _ { p r i v }$ to the server, who is unaware of the defense mechanism employed by the victim client. Consequently, from the server’s viewpoint, the victim client’s objective is to train $\hat { y } ,$ but the server’s dataset input-output pairs $( X _ { s e r v e r } , ~ y _ { s e r v e r } )$ are incompatible with $( X _ { p r i v } , \hat { y } )$ . The relationship between $y _ { p r i v }$ and $\hat { y }$ is established by the victim client, and the server is oblivious to the mapping relationship between them. In the inference phase, the server transmits the model output pred to the victim client, who can convert $\hat { y }$ to $y _ { t e s t }$ , the prediction under the real learning task, by applying the inverse mapping. As the server is unaware of the inverse mapping, it can only infer $y _ { t e s t }$ directly from pred, which is unlikely to be accurate.

Inspired by the label transformation idea introduced in [33], which is designed to defend gradient inversion attack in Vertical Federated Learning, we design two distinct label transformation (namely label encoding and decoding) mechanisms to thwart pseudo-client attack. These mechanisms encompass a one-to-one mapping defense as well as an autoencoder based defense.

# A. One-to-one Mapping Defense

Discrete labels are used as an example in this study. There is a one-to-one mapping between the label $y _ { p r i v }$ in the real learning task and the label $\hat { y }$ in the claimed learning task. Additionally, $\hat { y }$ can be converted back to the real label by means of an inverse one-to-one mapping. As illustrated in Fig. 16, all samples with the real label ’3’ are labeled as $\ ' 4 '$ following one-to-one mapping. Consequently, different labels are assigned to the same sample on the victim client and server sides after the labels are mapped. Subsequently, the victim client transmits yˆ to the server for split learning training. During the inference phase, the victim client inputs a sample that requires inference with the server, following which the server delivers the inference result of this sample to the victim client. The victim client receives the inference and maps it back to the real label to obtain the correct inference result. For instance, in the context of Fig. 16, upon receiving the inference outcome of ’4’, the client can obtain the accurate inference of ’3’ through the inverse mapping.

![](images/0770d3cd35f8fb0f7c6b3f1531f7b8b05f654d96f040bfb3f7e22ff0a9f9c6dc.jpg)



Fig. 14. Defense against PCAT. The legends are the same as that in Fig. 5. yˆ represents the labels of the claimed learning task. 

<table><tr><td>Attack</td><td colspan="2">PCAT</td><td colspan="2">improved PCAT</td></tr><tr><td>Acc(%)</td><td>Baseline</td><td>Pseudo</td><td>Baseline</td><td>Pseudo</td></tr><tr><td></td><td colspan="4">MNIST</td></tr><tr><td>No defense</td><td>98.82</td><td>96.56</td><td>98.86</td><td>96.51</td></tr><tr><td>One2One Mapping</td><td>98.87</td><td>66.03</td><td>98.76</td><td>96.16</td></tr><tr><td>Autoencoder Based</td><td>97.93</td><td>10.00</td><td>97.87</td><td>80.44</td></tr><tr><td></td><td colspan="4">CIFAR-10</td></tr><tr><td>No defense</td><td>92.74</td><td>82.57</td><td>92.91</td><td>82.68</td></tr><tr><td>One2One Mapping</td><td>92.66</td><td>57.91</td><td>92.99</td><td>82.32</td></tr><tr><td>Autoencoder Based</td><td>88.59</td><td>10.00</td><td>88.23</td><td>58.96</td></tr></table>

Table X. We compare the functionality stealing results of PCAT and imporved PCAT under three cases. Through the results we find that under one-to-one mapping defense and autoencoder based defense, the accruacy of PCAT drops drasticly while improved PCAT still works effectively.

For the attacker, unaware of the victim client’s label transformations, it still employs the original labels of its dataset to launch the attack. Upon completing the attack, it proceeds to perform inference on the basic learning task of the its dataset. Thus, we rely on the inference accuracy of the server’s and the pseudo-client’s model on the basic learning task as the metric for assessing the efficacy of the attack. As demonstrated in Table X, the one-to-one mapping defense remarkably diminishes the accuracy of the attack while effectively safeguarding the split learning baseline model’s performance. To be more specific, the attack performance of PCAT in each dataset drops 30.53%/24.66% while the split learning baseline’s accuracy remains the same.

# B. Autoencoder Based Defense

The one-to-one mapping defense is a straightforward and efficient mechanism. However, it remains unclear whether an adversary could reconstruct the mapping by leveraging their prior knowledge of the dataset and the smashed data. To address this concern, we have explored more intricate encoding strategies. Specifically, we have employed an autoencoder to encode the labels of the real learning task, thereby minimizing the need for manual setting procedures. During the inference phase, the victim client decodes the received inference result using the corresponding decoder to obtain the inference under the real learning.

In the following equations, $y _ { i } , \widehat { y _ { i } } , \widetilde { y _ { i } }$ denotes the labels in the true learning task, the encoded labels and decoded labels respectively.

$$
y _ {i} \in \left\{y _ {1}, y _ {2},..., y _ {n} \right\} \tag {2}
$$

$$
\widehat {y _ {i}} \in \{\widehat {y _ {1}}, \widehat {y _ {2}},..., \widehat {y _ {n}} \} \tag {3}
$$

$$
\widetilde {y} _ {i} \in \{\widetilde {y} _ {1}, \widetilde {y} _ {2}, \dots , \widetilde {y} _ {n} \} \tag {4}
$$

$$
\widehat {y} _ {i} = \operatorname{Enc} \left(y _ {i}\right), \quad \widetilde {y} _ {i} = \operatorname{Dec} \left(\widehat {y} _ {i}\right) \tag {5}
$$

Despite encoding the actual labels, our encoder and decoder still function as one-to-one mappings, and thus do not fundamentally differ from the previous method. Our defense strategy aims to prevent the server from gathering any basic information about the learning task through the collected labels. Specifically, the server will remain unaware of whether the victim client’s learning task is classification, or even how many classes are contained in the task. Furthermore, even if the server obtain the statistics of the labels received from the victim client, it will not be able to correctly label the data the same as the data in the victim client. To aid in visualizing our approach, the OneHot labels of 10 classes are represented by 10 black points in a two-dimensional space. The twodimensional space is divided into 10 different regions with different colors. All the points in the same region can be decoded to the same class.

To disrupt the one-to-one mapping between the labels of the real learning task and the claimed learning task, we employ a technique whereby a random point is selected from the region in the coding space that corresponds to the class of the sample. This point’s vector is used as the label for the sample sent to the server. The learning task for the victim client is to ensure that the output of the sample is as close as possible to the corresponding code. Since models generally output samples of the same class to the same region in the coding space, the victim client can decode the model output sent from the server to infer the predicted sample in the real learning task.

However, in this mechanism, the labels are spread across the entire coding space, which can lead to confusion for the model when dealing with samples that fall at the intersection of multiple regions. This ultimately results in a lower accuracy for the split learning baseline. To address this issue, we attempt to reduce the coding space as much as possible, without allowing the attacker to obtain any learning task information through statistical analysis of the labels.

To achieve this, we utilize the Welzl algorithm to determine the minimum covering circle of the codes that correspond to all OneHot vectors. We then calculate the minimum Euclidean distance between these codes and the center of the minimum covering circle to obtain the inner radius of the ring, which defines the minimum covering region.

To minimize the ring area, it is desirable for each corresponding encodings of all OneHot vectors to have a similar Euclidean distance to the center of the minimum covering circle. However, computing the minimum covering circle incurs significant cost during autoencoder training iterations. To address this issue, we incorporate the variance of Euclidean distances between encoded OneHot vectors into the loss function. The hyperparameter α adjusts the balance between $\mathcal { L } _ { v a r }$ and the basic loss function $\mathcal { L } ( y , \widetilde { y } )$ for the given learning task. By adding $\mathcal { L } _ { v a r }$ to the loss function, we can ensure that not only do the codes corresponding to all OneHot vectors have the similar distance to the center of the minimum covering circle, but also that the distances between these codes are similar as well. Thus, the areas corresponding to each class in the coding space are made similar.

![](images/d46dd0faa1c800e8fb71dc638c2e43165456cd17e900bd6288ac10892f1603d0.jpg)



(a)

![](images/89cd297babf332d3d3adecfd1e76958873e09e4506cfcfe35a218205f7ddc36b.jpg)



(b)

![](images/ba35ca94199af6b9e82e21ff4a5867bf347a782260d1e59df29bc531e60489af.jpg)



(c)

![](images/5d1b00bb962f122083dc7778f9cfd69a18b704e37b1b803a2dd18846d296362f.jpg)



(d)

![](images/e12db54bc46eb51cbe1d598f7fef3b06aa01683160ecf4fcc2445ca3ec09140e.jpg)



(e)

Fig. 15. The visualizations of 2D and 3D coding spaces. (a) illustrates the 2D coding space of the vanilla autoencoder and (b) minimizes the area of (a) by using minimum covering ring. Correspondingly, (c) presents the coding space of the autoencoder with customized loss function and (d) is the area of minimum covering ring of (c). (e) is the 3D coding space of a minimum covering spheric shell.   
![](images/4d137d460e42248bae949496b871b81253a30400f2fe041784c7119ee0407ff1.jpg)



Fig. 16. An example of one-to-one mapping defense and inverse mapping. $y _ { p r i v }$ denotes the labels of the real learning task of the SL baseline and yˆ represents the labels of the claimed learning task.

$$
\forall i, j \in [ 1, n ] \quad a n d \quad i <   j, \quad d i s t _ {i j} = \| \widehat {y _ {j}} - \widehat {y _ {i}} \| _ {2} \tag {6}
$$

$$
\mathcal {L} _ {v a r} = D (d i s t _ {1 2},..., d i s t _ {i j},..., d i s t _ {(n - 1) n}), \quad 1 \leq i <   j \leq n \tag {7}
$$

$$
\mathcal {L} = \alpha \mathcal {L} (y, \widetilde {y}) + (1 - \alpha) \mathcal {L} _ {\text { var }} \tag {8}
$$

In the two-dimensional coding space illustrated in Fig. 15, the incorporation of the $\mathcal { L } _ { v a r }$ loss function results in a reduction in the area of the minimum covering ring. Furthermore, the areas of the corresponding regions for each class become more homogeneous. A similar trend is observed in the threedimensional coding space, as depicted in Fig. 15. Here, the minimum covering sphere is characterized by an outer radius of 0.1457 and an inner radius of 0.1372. This approach can be extended to coding spaces of varying dimensions without loss of generality.

# VIII. IMPROVEMENT OF PCAT

Given that modifying the learning task can effectively defend against PCAT, we aimed to improve the PCAT mechanism to enable it to attack regardless of whether the victim client adopts our proposed defense. Our idea is to have the attacker keep their dataset unchanged from the original learning task and remove the constraint of the server model’s top layer. To achieve this, we use a pseudo-top model to map the input space of the server model’s top layer to the server’s learning task label space. Specifically, as illustrated

![](images/cd22a11f9b6af7f631492904d6aec42131b4c1b00daf09341562f32be5983e2a.jpg)



Fig. 17. Improved pseudo-client attack in SL. Since we do not know whether the client adopts the defense $( y _ { p r i v } \neq \hat { y } )$ or not, we consider two cases $( y _ { p r i v } = \hat { y }$ and $y _ { p r i v } \neq \hat { y } )$ in parallel. In the case of $y _ { p r i v } = \hat { y } _ { \mathrm { : } }$ , it is the same as pseudo-client attack. In the case of $y _ { p r i v } \neq \hat { y } ,$ the server initializes several pairs of $\widetilde { f _ { c } } ^ { n }$ and $\widetilde { f _ { s 1 } } ^ { n }$ and select the best one according to the train loss after attack.

in Fig. 17, we divided the server model $F _ { s }$ into one layer of top model $F _ { s 1 }$ and the remaining part model $F _ { s 2 }$ . As the server is unaware of whether the victim client has adopted our defense strategy, we designed our attack mode to be capable of targeting both cases in parallel.

First we assume $y _ { p r i v } = \hat { y }$ , which indicates that the client has not adopted our proposed defense and the actual learning task of split learning is consistent with the learning task known by the server. In this case, our attack mode remains unchanged as described in Sec. IV-A and illustrated in Fig. 17, where the pseudo-client shares the $F _ { s 1 }$ and $F _ { s 2 }$ models with the victim client (i.e. the entire server model).

Meanwhile we assume $y _ { p r i v } \ \ne \ \hat { y } _ { : }$ , which implies that the client has adopted the defense method of modifying the learning task and the actual learning task of split learning baseline is inconsistent with the learning task known by the server. To handle this scenario, the server generates multiple parallel pseudo-clients $\widetilde { f } _ { c }$ and pseudo-top models $\widetilde { f _ { s 1 } }$ before starting the split learning baseline. Here, $\widetilde { f _ { c } }$ is the same as the case without defensive measures, and $\stackrel { \sim } { f _ { s 1 } }$ is consistent with the structure of $F _ { s 1 }$ , but the model parameters are inconsistent.

After generating the pseudo-client and pseudo-top models, the SL baseline and the attack start simultaneously. In each iteration, the victim client performs forward propagation and sends the smashed data and the label of the sample corresponding to the claimed learning task to the server. The server then randomly selects the training samples owned by the server without label alignment and feeds the selected samples to the pseudo-client for forward propagation. When the server receives the smashed data and labels from the victim client and pseudo-client, it performs forward propagation in $F _ { s 2 } .$ , then performs forward propagation and calculates the loss in the real top model $F _ { s 1 }$ and the pseudo-top model $\widetilde { f _ { s 1 } }$ , respectively, and then performs back propagation. Except for the pseudo-client and pseudo-top models, which use the gradients produced by the pseudo training samples for weight updates, the remaining models use the gradients produced by the split learning baseline for weight updates. Since different pseudo-client and pseudo-top model pairs can achieve different performance, we can select the best pair based on the training loss of pseudo samples. More explanation is presented in Sec. IX-B

![](images/10fc2c16567fae91d859d2a7a5da51076ff9870074bb57195e96bf61fc7509ce.jpg)



(a) MNIST

![](images/797fe5c6ede552683dc0f211347fe07b329ec888c7a1f8d5d1ab32b54f0cc920.jpg)



(b) CIFAR-10   
Fig. 18. The accuracy of baseline and pseudo-client when adding different Gaussian noise to the smashed data.

The improved PCAT mechanism is similar to the U-Shape PCAT, with the only difference being that in the improved PCAT, the top model of split learning baseline is on the server side, and the loss value is calculated by the server. In contrast, in the U-Shape PCAT, the top model of split learning baseline is on the real client side, and the loss is calculated by the client to protect the label. Going further, we can conclude that under U-Shape PCAT, our proposed defense will fail.

To validate the efficacy of improved PCAT, we conducted experiments on MNIST, CIFAR-10. The settings of our experiments, as discussed in Sec. V, remains consistent with the previous experiments, wherein 10/100 samples of each class are employed as the server dataset for MNIST and CIFAR-10, respectively. Further, we set $X _ { s e r v e r } \ \in \ { \cal X } _ { p r i v } ,$ split layer = 2, and top layer = 1. Our experimental findings in Table X demonstrate that the improved PCAT outperforms the basic PCAT in both one-to-one mapping defense and autoencoder base defense. Specifically, under one-to-one mapping defense, the attack accuracy improved significantly from 66.03%/57.91% to 96.16%/82.32%. Similarly, under autoencoder based defense, the attack accuracy increased from 10.00%/10.00% to 80.44%/58.96%.

# IX. DISCUSSION

# A. Adding Noise

Our original intention was to protect the privacy of the victim client by adding Gaussian noise to the smashed data. However, we are surprised to discover that adding moderate amounts of Gaussian noise does not prevent PCAT, but rather enhanced the ability of the pseudo-client to steal the functionality of the victim client. To improve the accuracy of stealing client functionality, we propose that the server add noise to the smashed data. When the client sends smashed data to the server, the server adds Gaussian noise and then feeds it to the server model for forward propagation. It should be noted that adding noise to the smashed data of the split learning baseline causes a slight decrease in convergence speed and final accuracy, thus breaking the semi-honest rule. However, since the victim client cannot anticipate the convergence speed and final accuracy of the model, appropriately added noise is still difficult to detect.

![](images/863b5f3753e7cce4714519ec077e44a9e27b0007badc637998f2123b5d093d71.jpg)



![](images/de28486635176d46b46b65fa302735f78a3f2542a12621890d9e70172f1a56ae.jpg)



![](images/88466f4e8aa1d9d84e1c548514114fb4a072fce4e9379e669e981bab539b66b6.jpg)

![](images/aa0a5a3679a0e9e09b716c47a774d563de661b63e3dbbfe2518491c5bcf951d6.jpg)

![](images/74528214bcd78e5621c11f2ae33e84b168a81a880c813d70a2860ff6145cd9fe.jpg)

![](images/62ca05de97877b033e4139974a7fe40e8f96922cf8da6fb31bf363195253881f.jpg)  
(a)   
Fig. 19. (a) illustrates the space evolution of smashed data in U-shape PCAT. It can be categorized into two cases: one where the smashed data of the pseudo-client get closed to the smashed data of the victim client, and the other where the smashed data of the pseudo-client move away from that of the victim client. The four test methods are depicted in (b), and their corresponding outcomes are presented in Table XI

We conducted experiments on two datasets, MNIST and CIFAR-10, adding Gaussian noise with zero mean and varying variance to the smashed data. The variance is represented by the X-axis. Results showed that adding Gaussian noise slightly degraded the accuracy of the split learning baseline, but appropriate noise enabled the pseudo-client to steal closer functionality. Specifically, on the MNIST dataset, the pseudoclient accuracy improved from 88.44% to 90.48% when the smashed data added noise variance was 1.0. On the CIFAR-10 dataset, the pseudo-client accuracy improved from 74.75% to 76.05% when the smashed data added noise variance was 0.2, as shown in Fig. 18.

B. Phenomenon in U-Shape PCAT 

<table><tr><td>Acc(%)</td><td> $\tilde{f}_{c}, F_{s}, \tilde{f}_{t}$ </td><td> $F_{c}, F_{s}, F_{t}$ </td><td> $\tilde{f}_{c}, F_{s}, F_{t}$ </td><td> $F_{c}, F_{s}, \tilde{f}_{t}$ </td><td>Loss</td></tr><tr><td> $\tilde{\mathcal{F}} \approx \mathcal{F}$ </td><td>95.85</td><td>98.79</td><td>98.35</td><td>97.02</td><td>0.002</td></tr><tr><td> $\tilde{\mathcal{F}} \neq \mathcal{F}$ </td><td>75.41</td><td>98.96</td><td>0.05</td><td>0.79</td><td>0.005</td></tr></table>

Table XI. Four test results in two cases. We can find that if ${ \widetilde { \mathcal { F } } } \neq { \mathcal { F } } ,$ the accuracy of the pseudo-client is lower than that in the case $\tilde { \mathcal { F } } \approx \mathcal { F } .$ .   
Moreover, we can’t splice a pseudo-top and a victim client (or a pseudo-client and a victim top) together.

In Sec. III-B, we illustrate how the server steals the model functionality of the victim client in two-party split learning. We observe that the output feature space of the pseudo-client model gradually approaches that of the victim client due to the constraint of the server model. Without this constraint, the output feature space of the pseudo-client model would be far from that of the victim client. We further investigate how the feature space of smashed data changes in U-Shape split learning. As shown in Fig. 19, since the model is divided into three parts, two feature spaces, denoted by $\mathcal { F } _ { 1 }$ and ${ \mathcal { F } } _ { 2 } .$ , are formed. Correspondingly, the smashed data feature spaces on the pseudo-client side are denoted by $\widetilde { \mathcal { F } _ { 1 } }$ and $\widetilde { \mathcal { F } _ { 2 } }$ .

We discover that when stealing the victim client and top model, the constraint of the server model causes the changes of feature spaces in two possible ways. The first is similar to twoparty split learning, in which $\widetilde { \mathcal { F } _ { 1 } }$ and $\widetilde { \mathcal { F } _ { 2 } }$ gradually approach $\underset { - } { \mathcal { F } } _ { 1 }$ and $\underset { - } { \mathcal { F } _ { 2 } }$ under the constraint of the server. In the other way, $\mathcal { F } _ { 1 }$ and $\mathcal { F } _ { 2 }$ are far away from $\mathcal { F } _ { 1 }$ and $\mathcal { F } _ { 2 }$ .

We confirm this phenomenon through the experiment in Fig. 19, and the results are shown in Table XI, with two rows representing the test results in each scenario. From the results, we can see that when $\widetilde { \mathcal { F } } \approx \mathcal { F }$ , the accuracy of the model stolen by the pseudo-client is lower than that in the $\widetilde { \mathcal { F } } \neq \mathcal { F }$ case. Meanwhile, if the pseudo-client and the victim top model are spliced on the server at the same time, or the victim client and the pseudo-top model are spliced on the server at the same time, the spliced model can still maintain high accuracy when $\widetilde { \mathcal { F } } \approx \mathcal { F }$ . However, if $\widetilde { \mathcal { F } } \neq \mathcal { F }$ , the accuracy of the spliced model will drastically decrease.

Therefore, when we conduct improved PCAT, we can’t avoid the $\widetilde { \mathcal { F } } \neq \mathcal { F }$ case. The solution we deal with is initializing several pairs of pseudo-client and pseudo-top, we select the pair with the least training loss and this pair can achieve the highest accuracy.

# X. CONCLUSIONS

In this work, we propose a novel pseudo-client attack (PCAT) mechanism on various SL models. PCAT enables a semi-honest server to conduct functionality stealing, input data reconstruction and label inference without knowing the structure of the victim client model. We implemented PCAT for rich models, tasks and settings. Comprehensive experiments demonstrate that PCAT works effectively for rich models, tasks and settings. The whole attack process is transparent to the client, which thus reveals a serious privacy risk of SL. We also investigate a targeted defense and improve our attack to be robust to such defense. There remains some open problems for the future work. For example, we have discovered that there exist two potential paths for the feature space evolution in ushape PCAT. To eliminate one of these paths, we will perform further investigation on U-shape PCAT.

# ACKNOWLEDGMENTS

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, “the Fundamental Research Funds for the Central Universities” WK2150110024.

# REFERENCES

[1] S. Abuadbba, K. Kim, M. Kim, C. Thapa, S. A. C¸ amtepe, Y. Gao, H. Kim, and S. Nepal, “Can we use split learning on 1d CNN models for privacy preserving training?,” in ASIA CCS ’20: The 15th ACM Asia Conference on Computer and Communications Security, Taipei, Taiwan, October 5-9, 2020 (H. Sun, S. Shieh, G. Gu, and G. Ateniese, eds.), pp. 305–318, ACM, 2020.   
[2] J. Kim, S. Shin, Y. Yu, J. Lee, and K. Lee, “Multiple classification with split learning,” in SMA 2020: The 9th International Conference on Smart Media and Applications, Jeju, Republic of Korea, September 17 - 19, 2020, pp. 358–363, ACM, 2020.   
[3] W. Y. B. Lim, J. S. Ng, Z. Xiong, D. Niyato, C. Leung, C. Miao, and Q. Yang, “Incentive mechanism design for resource sharing in collaborative edge learning,” CoRR, vol. abs/2006.00511, 2020.   
[4] P. Vepakomma, O. Gupta, T. Swedish, and R. Raskar, “Split learning for health: Distributed deep learning without sharing raw patient data,” CoRR, vol. abs/1812.00564, 2018.

[5] A. Singh, P. Vepakomma, O. Gupta, and R. Raskar, “Detailed comparison of communication efficiency of split learning and federated learning,” CoRR, vol. abs/1909.09145, 2019.   
[6] O. Gupta and R. Raskar, “Distributed learning of deep neural network over multiple agents,” J. Netw. Comput. Appl., vol. 116, pp. 1–8, 2018.   
[7] M. G. Poirot, P. Vepakomma, K. Chang, J. Kalpathy-Cramer, R. Gupta, and R. Raskar, “Split learning for collaborative deep learning in healthcare,” CoRR, vol. abs/1912.12115, 2019.   
[8] P. Vepakomma, A. Singh, O. Gupta, and R. Raskar, “Nopeek: Information leakage reduction to share activations in distributed deep learning,” in 20th International Conference on Data Mining Workshops, ICDM Workshops 2020, Sorrento, Italy, November 17-20, 2020 (G. D. Fatta, V. S. Sheng, A. Cuzzocrea, C. Zaniolo, and X. Wu, eds.), pp. 933–942, IEEE, 2020.   
[9] J. Ryu, D. Won, and Y. Lee, “A study of split learning model,” in 16th International Conference on Ubiquitous Information Management and Communication, IMCOM 2022, Seoul, Korea, Republic of, January 3-5, 2022, pp. 1–4, IEEE, 2022.   
[10] W. N. Price and I. G. Cohen, “Privacy in the age of medical big data,” Nature medicine, vol. 25, no. 1, pp. 37–43, 2019.   
[11] N. Christin and R. Safavi-Naini, “Financial cryptography and data security,” in 18th International Conference, Springer, 2014.   
[12] K. Abouelmehdi, A. Beni-Hssane, H. Khaloufi, and M. Saadi, “Big data security and privacy in healthcare: A review,” Procedia Computer Science, vol. 113, pp. 73–80, 2017.   
[13] P. Jain, M. Gyanchandani, and N. Khare, “Big data privacy: a technological perspective and review,” Journal of Big Data, vol. 3, pp. 1–25, 2016.   
[14] Z. He, T. Zhang, and R. B. Lee, “Model inversion attacks against collaborative inference,” in Proceedings of the 35th Annual Computer Security Applications Conference, ACSAC 2019, San Juan, PR, USA, December 09-13, 2019 (D. Balenson, ed.), pp. 148–162, ACM, 2019.   
[15] E. Erdogan, A. Kupc¸ ¨ u, and A. E. C¸ ic¸ek, “Unsplit: Data-oblivious ¨ model inversion, model stealing, and label inference attacks against split learning,” IACR Cryptol. ePrint Arch., p. 1074, 2021.   
[16] D. Pasquini, G. Ateniese, and M. Bernaschi, “Unleashing the tiger: Inference attacks on split learning,” in CCS ’21: 2021 ACM SIGSAC Conference on Computer and Communications Security, Virtual Event, Republic of Korea, November 15 - 19, 2021 (Y. Kim, J. Kim, G. Vigna, and E. Shi, eds.), pp. 2113–2129, ACM, 2021.   
[17] G. Gawron and P. Stubbings, “Feature space hijacking attacks against differentially private split learning,” CoRR, vol. abs/2201.04018, 2022.   
[18] E. Erdogan, A. Kupc¸ ¨ u, and A. E. C¸ ic¸ek, “Splitguard: Detecting and ¨ mitigating training-hijacking attacks in split learning,” IACR Cryptol. ePrint Arch., p. 1080, 2021.   
[19] M. Abadi, A. Chu, I. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar, and L. Zhang, “Deep learning with differential privacy,” in Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security, CCS ’16, (New York, NY, USA), p. 308–318, Association for Computing Machinery, 2016.   
[20] D. F. H. W. Y. Z. Z. Z. C. C. X. L. Haibo MI, Kele XU, “Collaborative deep learning across multiple data centers,” SCIENCE CHINA Information Sciences, vol. 63, no. 8, pp. 182102–, 2020.   
[21] H. Chen, Y. Zhang, Y. Cao, and J. Xie, “Security issues and defensive approaches in deep learning frameworks,” Tsinghua Science and Technology, vol. 26, no. 6, pp. 894–905, 2021.   
[22] O. Li, J. Sun, X. Yang, W. Gao, H. Zhang, J. Xie, V. Smith, and C. Wang, “Label leakage and protection in two-party split learning,” CoRR, vol. abs/2102.08504, 2021.   
[23] G. E. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” CoRR, vol. abs/1503.02531, 2015.   
[24] J. Deng, W. Dong, R. Socher, L. Li, K. Li, and L. Fei-Fei, “Imagenet: A large-scale hierarchical image database,” in 2009 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR 2009), 20-25 June 2009, Miami, Florida, USA, pp. 248–255, IEEE Computer Society, 2009.   
[25] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” Proc. IEEE, vol. 86, no. 11, pp. 2278– 2324, 1998.   
[26] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” in 3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings (Y. Bengio and Y. LeCun, eds.), 2015.   
[27] A. G. Howard, M. Zhu, B. Chen, D. Kalenichenko, W. Wang, T. Weyand, M. Andreetto, and H. Adam, “Mobilenets: Efficient convolutional neural

networks for mobile vision applications,” CoRR, vol. abs/1704.04861, 2017.   
[28] G. X. Jiayu Wu, Qixiang Zhang, “Tiny imagenet challenge.” http: //cs231n.stanford.edu/reports/2017/pdfs/930.pdf, 2021.   
[29] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in 2016 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2016, Las Vegas, NV, USA, June 27-30, 2016, pp. 770–778, IEEE Computer Society, 2016.   
[30] A. Krizhevsky, G. Hinton, et al., “Learning multiple layers of features from tiny images,” 2009.   
[31] Z. Wang, A. Bovik, H. Sheikh, and E. Simoncelli, “Image quality assessment: from error visibility to structural similarity,” IEEE Transactions on Image Processing, vol. 13, no. 4, pp. 600–612, 2004.   
[32] C. Dwork and A. Roth, “The algorithmic foundations of differential privacy,” Found. Trends Theor. Comput. Sci., vol. 9, no. 3-4, pp. 211– 407, 2014.   
[33] T. Zou, Y. Liu, Y. Kang, W. Liu, Y. He, Z. Yi, Q. Yang, and Y.-Q. Zhang, “Defending batch-level label inference and replacement attacks in vertical federated learning,” IEEE Transactions on Big Data, 2022.

# XI. BIOGRAPHY SECTION

![](images/a90e65867870a3b2857fa60004992de30d3e96e5dc6f0362512f033e781a6c40.jpg)



Lan Zhang is currently a professor in the School of Computer Science and Technology, University of Science and Technology of China. She received her bachelor’s degree and Ph.D. degree from Tsinghua University, China. Her research interests span mobile computing, privacy protection, data sharing and trading.

![](images/0ffffdacb32264e822d8f5d76d71bacd75b990a4cd8c9b28fb76d48dc3444dd2.jpg)



Xinben Gao received the BS degree in information security from School of the Gifted Young, University of Science and Technology of China, Hefei, China, in 2022. She is currently working toward the MS degree in computer science and technology from University fo Science and Technology of China. Her research interests include privacy attack and protection in distributed machine learning.

![](images/6756a00ae47410e8de080f381e3d6bdd83c69cd198cd0bf04c0622b9075fae61.jpg)



Yaliang Li received the Ph.D. degree from the Department of Computer Science and Engineering at SUNY Buffalo in 2017. He is a research scientist at DAMO Academy, Alibaba Group. Before that he worked as a research scientist at Baidu Research, and a senior researcher at Tencent Medical AI Lab. He is broadly interested in machine learning and data mining with a focus on knowledge graph, question answering, automated machine learning, and more recently federated learning.

![](images/f29a3570311be95aa25e9f99f077da61cfbfad6be4935031a43ef76988376c60.jpg)



Yunhao Liu Professor at Automation Deapartment and Dean of the GIX in Tsinghua University. Yunhao received his BS degree in Automation Department from Tsinghua University, an MS and a Ph.D. degree in Computer Science and Engineering in Michigan State University, USA. He is a fellow of ACM and IEEE.