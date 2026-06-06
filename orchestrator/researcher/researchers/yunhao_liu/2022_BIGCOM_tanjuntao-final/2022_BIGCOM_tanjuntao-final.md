# Residue-based Label Protection Mechanisms in Vertical Logistic Regression

Juntao Tan†, Lan Zhang†, Yang Liu‡, Anran Li†, and Ye Wu‡

†School of Computer Science and Technology, University of Science and Technology of China, Hefei, China ‡ByteDance Security Research Department, Bejing, China {tjt, anranLi}@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, {liuyang.fromthu, wuye.2020}@bytedance.com

Abstract—Federated learning (FL) enables distributed participants to collaboratively learn a global model without revealing their private data to each other. Recently, vertical FL, where the participants hold the same set of samples but with different features, has received increased attention. This paper first presents one label inference attack method to investigate the potential privacy leakages of the vertical logistic regression model. Specifically, we discover that the attacker can utilize the residue variables, which are calculated by solving the system of linear equations constructed by local dataset and the received decrypted gradients, to infer the privately owned labels. To deal with this, we then propose three protection mechanisms, e.g., additive noise mechanism, multiplicative noise mechanism, and hybrid mechanism which leverages local differential privacy and homomorphic encryption techniques, to prevent the attack and improve the robustness of the vertical logistic regression model. Experimental results show that both the additive noise mechanism and the multiplicative noise mechanism can achieve efficient label protection with only a slight drop in model testing accuracy, furthermore, the hybrid mechanism can achieve label protection without any testing accuracy degradation, which demonstrates the effectiveness and efficiency of our protection techniques.

Index Terms—Federated Learning, Homomorphic Encryption, Local Differential Privacy

# I. INTRODUCTION

The success of machine learning rests on the availability of massive amount of data. However, it limits machine learning’s capability to deal with applications where data has been isolated across different organizations and data privacy has been emphasized [1], [2], e.g., user’s private pictures and videos [3]–[5] captured by mobile phone as well as social relationships [6] should not be leaked during model training. Federated learning (FL) [7]–[10] is one emerging technology, which enables multiple parties to collaboratively train a machine learning model by iteratively exchanging model parameters between these parties and a centralized server, meanwhile keeping their datasets private. There are three types of FL methods according to the distribution of data, which are horizontal federated learning (HFL) [7], [11], vertical federated learning (VFL) [12], [13], and federated transfer learning (FTL) [14] respectively. HFL considers the scenario where each party has data with different sample IDs but shares many common features. Different from HFL, in VFL, multiple parties handle data with the same sample IDs, but each party has its own feature set. This is a common phenomenon in financial, e-commerce, and healthcare applications, e.g., two e-commerce companies and a bank which all serve clients from the same city can jointly learn a model by iteratively exchanging intermediate messages between each other to recommend personalized loans for clients based on their online shopping behaviours through VFL.

A series of previous efforts have been devoted to designing VFL algorithms, such as logistic regression [15], boosting tree [16] and neural network [17] via homomorphic encryption [18]–[20] or multi-party computation techniques [21]–[23], for diverse scenarios. Despite the wide applications, VFL has an inherent vulnerability that can be leveraged by an adversarial participant to conduct various malicious attacks, e.g., label inference attacks [12], [24], feature inference attacks [13] and sample ID attacks [25]. Specifically, for label inference attacks, Li et al. [12] proposes a label-uncovering method which uses the norm of the communicated gradients between the parties as well as a protection technique that perturbs the gradients randomly before communication. Besides, Chong et al. [24] discover that the bottom model structure and the gradient update mechanism of VFL can be exploited by a malicious participant to gain the power to infer the privately owned labels. For feature inference attacks, Luo et al. [13] presents several feature inference attack methods in the prediction stage of several VFL models, e.g., the linear model, the tree model, and the neural network model. Besides, the work [26] considers that an honest-but-curious adversary can infer private training data from the legitimately received information in the case of collusion between attacker and third party. Furthermore, for sample ID attacks, Yang et al. [25] proposes the notion of asymmetrical VFL and leverages the standard private set intersection protocol to achieve the asymmetrical ID alignment phase in an asymmetrical VFL system to protect sample IDs.

Though these methods can reveal a variety of VFL vulnerabilities, their assumptions are impractical in real VFL applications. For instance, the work [12] assumes that the categorical distribution of the training samples is unbalanced. Meanwhile, the work [13] assumes the attacker controls the whole trained VFL model parameters, which is contrary to the settings of the VFL protocol, and the attacking method in [26] can only work when one participant colludes with third party. To this end, in this paper, we focus on the vulnerability discovery and privacy protection of currently widely used vertical logistic regression protocol [15] without any impractical assumptions. Specifically, we discover that an attacker can construct a system of linear equations by its local dataset and the received decrypted gradients, to solve the residue variables and further to infer the private labels owned by other participant. This is a serious data privacy breach for the vertical federated learning system, so we propose three residue protection mechanisms, $e . g .$ , the additive noise mechanism, the multiplicative noise mechanism, and a hybrid mechanism that leverages local differential privacy and homomorphic encryption techniques simultaneously, to prevent such an attack. As a result, we can improve the robustness of the vertical logistic regression model.

The main contributions of this work are summarized as follows:

• We identify an effective label inference method that uses the calculated residue variables from the constructed linear system based on local datasets and the decrypted gradients to infer private labels, without actually decrypting the residues.   
• We propose two computation efficient residue protection mechanisms as well as a hybrid residue protection mechanism. These two computation efficient mechanisms utilize additive noise and multiplicative noise to mask residues respectively to achieve label protection, and they satisfy the property of -LDP in each training round. In addition, the hybrid residue protection mechanism uses the local differential privacy and homomorphic encryption methods to increase the batch size to protect private labels without any testing accuracy degradation.   
• We conduct extensive experiments on four public datasets to evaluate the three proposed residue protection mechanisms, and the results demonstrate that our protection techniques are both effective and efficient.

# II. BACKGROUND AND PRELIMINARIES

# A. Logistic Regression

The supervised machine learning aims to learn a mapping $f ( W ) = \mathcal { X } \to \mathcal { Y }$ from an input space X to an output space Y, where W is the model parameters. To be concrete, for a training dataset $T = \{ ( x _ { 1 } , y _ { 1 } ) , ( x _ { 2 } , y _ { 2 } ) , \cdot \cdot \cdot , ( x _ { N } , y _ { N } ) \}$ , the supervised machine learning tries to minimize the following loss function:

$$
\mathcal {L} = \frac {1}{N} \sum_ {i = 1} ^ {N} l (f (x _ {i}; \boldsymbol {W}), y _ {i}) + \lambda \Omega (\boldsymbol {W}),
$$

where $l ( \cdot )$ is the loss function and $\Omega ( \cdot )$ is the regularization term which is used to reduce model complexity in order to prevent overfitting, and λ represents regularization parameter, which controls the trade-off between the empirical loss and the regularization loss.

Logistic regression (LR) is a binary supervised machine learning model with output space $\mathcal { V } \in \{ 0 , 1 \}$ . In LR, the nonlinear mapping function is

$$
f (\pmb {W}) = \sigma (\pmb {W} ^ {T} \pmb {x}), \mathrm{where} \sigma (z) = \frac {1}{1 + e ^ {- z}},
$$

which is the sigmoid function. And the loss function is

$$
\mathcal {L} = - \frac {1}{N} \sum_ {i = 1} ^ {N} y _ {i} \log (f (x _ {i})) + (1 - y _ {i}) \log (1 - f (x _ {i})) + \lambda \Omega (\boldsymbol {W}), \tag {1}
$$

where $\Omega ( W )$ can take the form of $L _ { 1 }$ norm or $L _ { 2 }$ norm of W . And gradients are computed as

$$
\frac {\partial \mathcal {L}}{\partial \boldsymbol {W}} = - \frac {1}{N} \sum_ {i = 1} ^ {N} (y _ {i} - f (x _ {i})) x _ {i}. \tag {2}
$$

For a trained model and a testing data sample $x _ { p r e d } .$ , we can get the probability of this sample being classified as positive as $f ( x _ { p r e d } ; W )$ .

# B. Homomorphic Encryption

Different from the conventional symmetric or asymmetric encryption, homomorphic encryption (HE) is a special kind of cryptosystem which can support arithmetic computation on ciphertext [18]–[20]. It can ensure that after decryption the computation result on the ciphertext is the same as the computation result on the plaintext.

Additive homomorphic encryption belongs to partially homomorphic cryptosystem, which can support computation on an logical circuit with infinite depth of addition gates, mainly has the following two properties,

$$
\left\langle m _ {1} \right\rangle \oplus \left\langle m _ {2} \right\rangle = \left\langle m _ {1} + m _ {2} \right\rangle
$$

$$
m _ {1} \star \left\langle m _ {2} \right\rangle = \left\langle m _ {1} \times m _ {2} \right\rangle
$$

where $\left. m _ { 1 } \right.$ and $\langle m _ { 2 } \rangle$ represents two ciphertexts, ⊕ stands for addition operation on ciphertext, and ? represents multiplication operation on ciphertext. When the result of the addition or multiplication operation on the ciphertext is decrypted, it is the same as the result of the operation on the plaintext.

# C. Local Differential Privacy

Differential privacy (DP) is a privacy-preserving technique that is used to obscure the output of an oracle. Local differential privacy (LDP) [27]–[29], compared with DP, the main difference is that the role to add noise is the owner of private data, not the central aggregator, which can further reduce the risk of privacy leakage.

We say that a randomized algorithm M satisfies -LDP if and only if for any input t and t0 in the input space, and for $t ^ { * }$ in the output space, we have:

$$
\operatorname * {P r} \left[ \mathcal {M} (t) = t ^ {*} \right] \leq e ^ {\epsilon} \cdot \operatorname * {P r} \left[ \mathcal {M} \left(t ^ {\prime}\right) = t ^ {*} \right],
$$

where $\mathrm { P r } [ \cdot ]$ denotes probability and  stands for privacy budget in the context of differential privacy. With a lower privacy budget, we can provide a stronger privacy guarantee.

# III. PROBLEM STATEMENT

In this section, we first introduce the system model of vertical federated learning in Sec.III-A. Then, in Sec.III-B, we discuss the adversary model. Finally, we give a formal definition of the research problem in Sec.III-C.

# A. System Model

In a vertical federated learning system, without loss of generality, we suppose there are two participants. One participant’s private dataset contains both features and labels, called Bob, being the active party, the other’s dataset contains only features, called Alice, being the passive party.

The private dataset of Alice can be represented as $\mathcal { D } _ { A } =$ $\{ x _ { 1 } ^ { A } , x _ { 2 } ^ { A } \cdot \cdot \cdot , x _ { N } ^ { A } \}$ , where $x _ { i } ^ { A } \in \mathcal { X } ^ { d ^ { A } }$ and $d ^ { A }$ is the number of Alice’s features. Bob’s private dataset is denoted as $\mathcal { D } _ { B } =$ $\{ ( x _ { 1 } ^ { B } , y _ { 1 } ) , ( x _ { 2 } ^ { B } , y _ { 2 } ) , \cdot \cdot \cdot , ( \bar { x } _ { N } ^ { B } , y _ { N } ) \}$ , where $x _ { i } ^ { B } \in \mathcal { X } ^ { d ^ { B } }$ and $d ^ { B }$ is the number of Bob’s features, and $y _ { i } \in \mathcal { V }$ , in our case of vertical logistic regression, $\mathcal { V } = \{ 0 , 1 \}$ .

Alice and Bob collaboratively train a vertical logistic regression model without the assistance of a trusted third party. We assume that the private set intersection (PSI) procedure before model training, which can be implemented via protocols in [30]–[32], has been completed. After model training, Alice and Bob will obtain the model parameters associated with its feature space, which are tively. For a given testing $W ^ { A } \in \mathbb { R } ^ { d ^ { A } }$ and W B $W ^ { B } \in \mathbb { R } ^ { d ^ { B } }$ ∈ R d B respec- and Bob can get the prediction result $\hat { y } = \overset { \triangledown } { f } ( x _ { p r e d } ^ { A } , x _ { p r e d } ^ { B } ; { W ^ { A } , W ^ { B } } )$ $( x _ { p r e d } ^ { A } , x _ { p r e d } ^ { B } )$ ) via a collaborative inference protocol [8], [15].

# B. Adversary Model

In the two-party vertical federated learning system, we assume that one party, the passive party Alice, is an honest-butcurious party. Alice strictly follows the collaborative training protocol, but she tries her best to infer some valuable information through intermediate messages. For example, Alice may want to infer Bob’s model parameters, features, and labels, etc. We do not assume Alice to be a malicious party because the goal of vertical federated learning is to get a better global model, if Alice tries to attack the collaborative protocol itself, then she will not get a model with good performance, and that is inconsistent with Alice’s goal.

The adversary model can be characterized by two aspects, which are adversary’s goal, adversary’s knowledge respectively.

• Adversary’s goal. In the vertical logistic regression setting, Alice’s goal is to infer the private labels of Bob’s dataset via the transferred intermediate messages.   
• Adversary’s knowledge. Alice’s knowledge about the system include 1) the private dataset $\mathcal { D } _ { A } ; 2 )$ feature space $\chi ^ { d _ { A } } ; 3 )$ number of her features $d ^ { A } \colon 4 )$ partial model parameters $W ^ { A }$ associated with $\chi ^ { d _ { A } }$ .

# C. Problem Formulation

For the widely used training protocol of vertical logistic regression, at each iteration, Bob chooses a mini-batch B and calculates the corresponding linear predictions, losses and gradients. Bob can compute residue as $r _ { i } = y _ { i } - f ( x _ { i } )$ and sends the encrypted form, which is $\left. r _ { i } \right.$ , to Alice. According to Eq.2 Alice can calculate encrypted gradients on the encrypted residue and update her model parameters via the gradient decrypted by Bob. For a more detailed description of the training protocol, please refer to [15].

After receiving the encrypted residue vector $\langle r \rangle$ and decrypted gradient $\pmb { g } ^ { A }$ on the current mini-batch B from Bob, Alice can construct the following equations:

$$
\left\{ \begin{array}{l l} X _ {1, 1} ^ {A} \langle r _ {1} \rangle + X _ {2, 1} ^ {A} \langle r _ {2} \rangle + \dots + X _ {\mathcal {B}, 1} ^ {A} \langle r _ {\mathcal {B}} \rangle & = g _ {1} \\ X _ {1, 2} ^ {A} \langle r _ {1} \rangle + X _ {2, 2} ^ {A} \langle r _ {2} \rangle + \dots + X _ {\mathcal {B}, 2} ^ {A} \langle r _ {\mathcal {B}} \rangle & = g _ {2} \\ & \vdots \\ X _ {1, d ^ {A}} ^ {A} \langle r _ {1} \rangle + X _ {2, d ^ {A}} ^ {A} \langle r _ {2} \rangle + \dots + X _ {\mathcal {B}, d ^ {A}} ^ {A} \langle r _ {\mathcal {B}} \rangle & = g _ {d ^ {A}} \end{array} \right. \tag {3}
$$

The linear equations in Eq.3 with $| B |$ unknowns and $d ^ { A }$ equations can be represented as a vectorized form as $( X _ { B } ^ { A } ) ^ { \mathsf { T } } \langle \pmb { r } \rangle =$ $\pmb { g } ^ { A }$ . Since in many practical applications, many companies and institutes have thousands of features and they prefer a small mini-batch size in order to get a faster convergence rate, so the number of Alice’s features is often larger than the mini-batch size, as a result, we can derive that

$$
\operatorname{rank} \left(\left(X _ {\mathcal {B}} ^ {A}\right) ^ {\top}\right) = \operatorname{rank} \left(\left(X _ {\mathcal {B}} ^ {A}\right) ^ {\top}, \boldsymbol {g} ^ {A}\right) = | \mathcal {B} |. \tag {4}
$$

Then the linear system in $\operatorname { E q . }$ has one and only one solution so that Alice can get the true values of residues by solving the linear system, without actually decrypting the ciphertext. And as mentioned before, in logistic regression model, the ground truth label $y _ { i }$ lies in the space of $\mathcal { V } = \{ 0 , 1 \}$ , the residue $r _ { i }$ is the subtraction of the ground truth label yi and predicted value of $x _ { i }$ , since we use sigmoid as activation function, we have $0 < f ( x _ { i } ) < 1$ . Then if Alice knows that $r _ { i } > 0$ , she can infer the ground truth label $y _ { i }$ equals 1, and if $r _ { i } < 0 .$ , she can get that the true label is 0. In such a scenario, Alice could steal Bob’s private label without even interrupting the training protocol, and this is a serious privacy breach for Bob.

So in this paper, we intend to leverage privacy-preserving techniques, especially local differential privacy and additive homomorphic encryption, to design residue protecting mechanisms to prevent Bob’s private label from being breached.

# IV. RESIDUE PROTECTING MECHANISMS

In Sec.III-C, we talk about that, by solving the linear equations, Alice can get the residues, and further she can infer Bob’s private labels. So in this section, we try to design residue protecting mechanisms to prevent label leakage. Specifically, in Sec.IV-A we introduce the additive noise mechanism and prove that it is -LDP. Then we provide another -LDP mechanism via multiplicative noise in Sec.IV-B. Finally, we devise a hybrid mechanism in Sec.IV-C, which leverages random response and additive homomorphic encryption, and it is proved performance-lossless.

# A. Additive Noise Mechanism $\mathcal { M } _ { a d d }$

In an additive noise mechanism, Bob tries to add wellcrafted noise to the original residue set, and sends the masked residue to Alice so to make it hard for her to infer the groundtruth value.

For any $r _ { i } , \ r _ { j }$ in residue set R, we have $- 1 < r _ { i } < 1$ and $- 1 < r _ { j } < 1$ , so the $L _ { 1 }$ sensitivity of function $f ( r ) = r$ on set R is $\begin{array} { r } { \Delta = \operatorname* { m a x } _ { r _ { i } , r _ { j } \in R } \left\| r _ { i } - r _ { j } \right\| _ { 1 } = 2 } \end{array}$ . Then the additive noise mechanism can be written as

$$
\mathcal {M} _ {a d d} (r) = r + \mathrm{Lap} \left(\frac {2}{\epsilon}\right), \tag {5}
$$

where Lap(·) represents Laplace distribution. This mechanism satisfies -LDP and we can prove it as

$$
\begin{array}{l} \frac {\operatorname* {P r} \left[ \mathcal {M} _ {a d d} \left(r _ {i}\right) = z \right]}{\operatorname* {P r} \left[ \mathcal {M} _ {a d d} \left(r _ {j}\right) = z \right]} = \frac {\exp \left(- \frac {\epsilon | z - r _ {i} |}{\Delta}\right)}{\exp \left(- \frac {\epsilon | z - r _ {j} |}{\Delta}\right)} \\ = \exp \left(\frac {\epsilon (| z - r _ {i} | - | z - r _ {j} |)}{\Delta}\right) \tag {6} \\ \leq \exp \left(\frac {\epsilon | r _ {i} - r _ {j} |}{\Delta}\right) \\ \leq \exp (\epsilon). \\ \end{array}
$$

So by leveraging additive mechanism $\mathcal { M } _ { a d d }$ , Bob can send the masked residue to Alice without any encryption, this can help improve the training efficiency compared with the original two-party training protocol in [15]. And the privacy of residue is guaranteed by the privacy budget . The impact of the additive noise on the global model accuracy and AUC score is evaluated in Sec.V-B.

# B. Multiplicative Noise Mechanism $\mathcal { M } _ { m u l t }$

In the multiplicative noise mechanism, Bob generates noise from a Laplace distribution and multiplies it with the residue to get $\mathcal { M } _ { m u l t }$ . By defining two clipping methods cl $\mathrm { i p } _ { 1 }$ and cli $\cdot \mathtt { P } _ { 2 }$ , we can prove that $\mathcal { M } _ { m u l t }$ is -LDP. We give a more detailed explanation below.

Firstly, we define the first clipping method as

$$
\operatorname{clip} _ {1} (r) = \left\{ \begin{array}{l l} b _ {1}, & | r | \leq b _ {1}, \\ r, & \text { otherwise } \end{array} \right. \tag {7}
$$

where $b _ { 1 }$ is the clipping bound of ${ \mathsf { c l i p } } _ { 1 }$ . In this way, we can ensure that the $L _ { 1 }$ sensitivity of function $\begin{array} { r } { f ( r ) = ~ \frac { 1 } { r } } \end{array}$ on the residue set R is $\begin{array} { r } { \Delta = \operatorname* { m a x } _ { r _ { i } , r _ { j } \in R } \left\| \frac { 1 } { r _ { i } } - \frac { 1 } { r _ { j } } \right\| _ { 1 } = \frac { 2 } { b _ { 1 } } } \end{array}$ .

Then, the second clipping method is defined as

$$
\operatorname{clip} _ {2} \left(\mathcal {M} _ {\text { mult }} (r)\right) = \left\{ \begin{array}{l l} b _ {2}, & \left| \mathcal {M} _ {\text { mult }} (r) \right| \geq b _ {2}, \\ \mathcal {M} _ {\text { mult }} (r), & \text { otherwise } \end{array} \right. \tag {8}
$$

where $b _ { 2 }$ is the clipping bound of ${ \mathsf { c l i p } } _ { 2 }$ . So we can derive our multiplicative mechanism as the following

$$
\mathcal {M} _ {\text { mult }} (r) = r \cdot \mathrm{Lap} \left(\frac {2 b _ {2}}{b _ {1} \epsilon}\right). \tag {9}
$$

Still, we can prove that Eq.9 satisfies -LDP as

$$
\begin{array}{l} \frac {\operatorname * {P r} [ \mathcal {M} _ {m u l t} (r _ {i}) = z ]}{\operatorname * {P r} [ \mathcal {M} _ {m u l t} (r _ {j}) = z ]} = \frac {\exp \left(- \frac {\epsilon | \frac {z}{r _ {i}} |}{b _ {2} \Delta}\right)}{\exp \left(- \frac {\epsilon | \frac {z}{r _ {j}} |}{b _ {2} \Delta}\right)} \\ = \exp \left(\frac {\epsilon (| \frac {z}{r _ {j}} | - | \frac {z}{r _ {i}} |)}{b _ {2} \Delta}\right) \tag {10} \\ \leq \exp \left(\frac {\epsilon | z |}{b _ {2}}\right) \\ \leq \exp (\epsilon). \\ \end{array}
$$

So Bob can use this mechanism to protect the residues and avoid the time-consuming encryption operation at each iteration. Still, the privacy of residues is guaranteed by privacy budget . In Sec.V-C, we evaluate the impact of parameters $b _ { 1 }$ and $b _ { 2 }$ on the global model performance, we also provide the comparison between $\mathcal { M } _ { a d d }$ and $\mathcal { M } _ { m u l t }$ .

# C. Hybrid Mechanism $\mathcal { M } _ { h y b r i d }$ based on LDP and HE

In previous Sec.IV-A and Sec.IV-B, we have talked about how Bob can obtain an -LDP mechanism via additive and multiplicative noise. The $\mathcal { M } _ { a d d }$ and $\mathcal { M } _ { m u l t }$ mechanisms are computational efficient because there are no encryption and decryption operations in it, but the extra noise can decrease the model performance. So in this section, we propose a hybrid mechanism $\mathcal { M } _ { h y b r i d } .$ , which leverages random response and additive homomorphic encryption to implement a lossless training protocol, which means that the global model accuracy and AUC score are the same as the one obtained from the conventional centralized model training.

1) Training Protocol of $\mathcal { M } _ { h y b r i d } .$ Table I shows the details of the training protocol, which is based on random response [33] and additive homomorphic encryption. The protocol shows just one iteration of a training algorithm, usually, in practical application, such a protocol is often iterated many times to get a model with good performance.

Concretely, in Step 1, we use random response to obscure items in indicator vector m with probability $\textstyle p = { \frac { e ^ { \epsilon } } { 1 + e ^ { \epsilon } } }$ e to be unchanged and with probability $1 - p$ to be flipped. To this end, we can prove that the random response mechanism is -LDP [34]. Furthermore , in order to prevent Bob’s private label from being breached, the parameters in Step 1 need to satisfy the requirements in Eq.11,

$$
\left\{ \begin{array}{l} d ^ {A} <   L _ {R R} = q | S | p + (1 - q) | S | (1 - p) <   | S | \\ 0 <   q <   \frac {1}{2} \\ \frac {1}{2} <   p <   1 \end{array} \right. \tag {11}
$$

where $q$ is the fraction of the number of 1s in the origin m, and $L _ { R R }$ is the number of 1s in the obscured vector $R R ( m )$ . These requirements can guarantee that Alice can’t establish the relationship between training samples and residues, so Bob’s private labels are protected. More detailed security analysis is provided in Sec.IV-C2.

TABLE I TRAINING PROTOCOL OF HYBRID MECHANISM $\mathcal { M } _ { h y b r i d }$ BASED ON RANDOM RESPONSE AND ADDITIVE HOMOMORPHIC ENCRYPTION 

<table><tr><td>Steps</td><td>Active party Bob</td><td>Passive party Alice</td><td>Transmitted messages from Bob to Alice</td></tr><tr><td>Step 0</td><td>Generate paillier [19] key pairs and send public key to Alice.</td><td>Receive public key.</td><td>public key</td></tr><tr><td>Step 1</td><td>Choose subset S with indices B from dataset X $^{B}$  and generate a binary indicator vector m with the same length as S. Set q|S| items of m to 1 and the rest to 0 randomly, and send the output of random response which is RR(m), and indices B to Alice.</td><td>Calculate partial linear prediction as l $^{A}$  = X $_{B}^{A}$ W $^{A}$ RR(m) and send it back to Bob.</td><td>RR(m), B</td></tr><tr><td>Step 2</td><td>Calculate partial linear prediction as l $^{B}$  = X $_{B}^{B}$ W $^{B}$ RR(m) locally and receive l $^{A}$  from Alice, combine l $^{A}$  and l $^{B}$  and then compute loss and residue r according to Eq.1. Select 0 &lt; k ≤ |S| non-zeros items from r to get r $_{1}$ , and set all other items to 0 to get r $_{2}$ , then encrypt r $_{1}$  ∪ r $_{2}$  and send it to Alice.</td><td>Compute encrypted gradient as ⟨g $^{A}$ ⟩ = -1/|B|(X $_{B}^{A}$ )T⟨r $_{1}$  ∪ r $_{2}$ ⟩, then use noise ξ to mask the gradient and send ⟨g $^{A}$  + ξ⟩ back to Bob.</td><td>⟨r $_{1}$  ∪ r $_{2}$ ⟩</td></tr><tr><td>Step 3</td><td>First, decrypt the encrypted masked gradient and sent g $^{A}$  + ξ to Alice and second, compute gradient as g $^{B}$  = -1/|B|(X $_{B}^{B}$ )T(r $_{1}$  ∪ r $_{2}$ ) locally and use g $^{B}$  to update parameter W $^{B}$ .</td><td>Remove the mask ξ to get the true gradient g $^{A}$  and then use it to update parameter W $^{A}$ .</td><td>g $^{A}$  + ξ</td></tr></table>

The parameter setting of the protocol and the detailed training time comparison among $\mathcal { M } _ { a d d } , \mathcal { M } _ { m u l t } , \mathcal { M } _ { h y b r i d }$ ,and the baseline protocol in [15] is given in Sec.V-D.

2) Security Analysis: The training protocol and the corresponding transmitted messages are shown in Table I. Since in our adversary model we assume Alice to be an honest-butcurious attacker, she can only infer the private data of Bob via these transmitted messages. Below we prove that all these messages are safe to transmit.

Step 1. The private indicator vector m is obscured via the random response mechanism, which is -LDP, then the privacy of m is guaranteed by privacy budget . So with probability p closer to $\frac { 1 } { 2 }$ we can provide a stronger privacy-preserving mechanism on m. To this end, Alice can not know which samples are involved in the current mini-batch, so she can not establish the linear equations like $\operatorname { E q . }$ , which means that she can not directly steal private labels via equation solving.

Step 2. The residue set $r _ { 1 } \cup r _ { 2 }$ is encrypted via paillier public key, since Alice has no private key , she can not infer residue values directly via ciphertext decryption.

Step 3. Bob sends the decrypted masked gradient to Alice and she can obtain the true gradient after removing the mask. Due to the constraints in Eq.11 which is that the number of 1s in the obscured indicator vector is larger than the number of Alice’s features, so Alice can only construct a linear system with unknowns more than equations, which means that she can not get the residue value by solving linear equations.

Furthermore, because parameter k which is the size of set $\mathbf { \Delta } _ { \mathbf { r } _ { 1 } }$ is unknown to Alice, she can not know either the actual minibatch size or which samples the mini-batch consists of. The only way Alice can construct the ground truth linear system successfully is by first enumerating all possibilities of minibatch size and then enumerating all combinations of samples to form a mini-batch with that size. Because on average the time complexity of solving a system of linear equations with n unknowns is $\scriptstyle { \mathcal { O } } ( n ^ { 2 } )$ , the time complexity of the problem Alice tries to solve (finding the ground truth linear equations) is given by

$$
\begin{array}{l} \sum_ {k = 1} ^ {L _ {R R}} k ^ {2} \binom {L _ {R R}} {k} = L _ {R R} (L _ {R R} + 1) 2 ^ {L _ {R R} - 2} \tag {12} \\ = \mathcal {O} (L _ {R R} ^ {2} 2 ^ {L _ {R R}}). \\ \end{array}
$$

The complexity of this problem is even higher than many conventional problems with exponential complexity, so we assume that if Alice’s computation resources are limited, and $L _ { R R }$ is large enough, Alice can not find the ground truth linear equations, so Bob’s private labels are being well protected.

# V. EXPERIMENTS

In this section, we first introduce the dataset information and our vertical federated learning system in Sec.V-A. Then in Sec.V-B, under different privacy budgets, we evaluate the impact of additive noise on the global model performance. Next, in Sec.V-C, how clipping bounds $b _ { 1 }$ and $b _ { 2 }$ affect the global model is validated. We also compare the performance of $\mathcal { M } _ { a d d }$ and $\mathcal { M } _ { m u l t }$ under the same privacy budget. Finally, in Sec.V-D, we give the setting of parameters in our hybrid training protocol and assess the performance of $\mathcal { M } _ { h y b r i d }$ . The training time comparison among $\mathcal { M } _ { a d d } , \mathcal { M } _ { m u l t } , \mathcal { M } _ { h y b r i d }$ ,and baseline protocol in [15] is also presented.

# A. Experimental Setup

1) Datasets: We evaluate the effectiveness of the three proposed mechanisms via four different datasets which are breast-cancer1, sklearn-digits2, census-income3, give-mesome-credit4, respectively. We summarize the characteristics of these four datasets in Table III.

TABLE II GLOBAL MODEL PERFORMANCE COMPARISON BETWEEN $\mathcal { M } _ { a d d }$ AND $\mathcal { M } _ { m u l t }$ 

<table><tr><td>Dataset</td><td>Metrics</td><td>Baseline</td><td colspan="4"> $\mathcal{M}_{add}$ </td><td colspan="4"> $\mathcal{M}_{mult}$ </td></tr><tr><td>—</td><td>—</td><td>—</td><td> $\epsilon = 0.01$ </td><td> $\epsilon = 0.1$ </td><td> $\epsilon = 1$ </td><td> $\epsilon = 10$ </td><td> $\epsilon = 0.01$ </td><td> $\epsilon = 0.1$ </td><td> $\epsilon = 1$ </td><td> $\epsilon = 10$ </td></tr><tr><td rowspan="2">breast-cancer</td><td>Acc</td><td>97.37</td><td>83.33</td><td>87.72</td><td>92.10</td><td>94.74</td><td>87.72</td><td>89.47</td><td>92.98</td><td>95.61</td></tr><tr><td>Auc</td><td>99.87</td><td>87.52</td><td>95.84</td><td>98.92</td><td>99.43</td><td>95.90</td><td>96.79</td><td>97.78</td><td>99.21</td></tr><tr><td rowspan="2">sklearn-digits</td><td>Acc</td><td>91.11</td><td>63.33</td><td>77.50</td><td>89.17</td><td>90.83</td><td>77.50</td><td>79.17</td><td>85.00</td><td>89.72</td></tr><tr><td>Auc</td><td>96.66</td><td>63.02</td><td>86.99</td><td>95.84</td><td>96.72</td><td>86.36</td><td>85.90</td><td>89.71</td><td>96.14</td></tr><tr><td rowspan="2">census-income</td><td>Acc</td><td>82.69</td><td>63.43</td><td>71.35</td><td>80.89</td><td>82.06</td><td>63.77</td><td>63.32</td><td>69.77</td><td>79.45</td></tr><tr><td>Auc</td><td>88.79</td><td>66.72</td><td>75.85</td><td>85.95</td><td>88.76</td><td>75.57</td><td>76.88</td><td>83.45</td><td>87.74</td></tr><tr><td rowspan="2">give-me-some-credit</td><td>Acc</td><td>85.56</td><td>71.24</td><td>77.44</td><td>82.77</td><td>85.54</td><td>63.15</td><td>69.51</td><td>71.91</td><td>88.14</td></tr><tr><td>Auc</td><td>81.15</td><td>70.50</td><td>76.97</td><td>79.24</td><td>81.08</td><td>65.21</td><td>71.16</td><td>76.61</td><td>81.44</td></tr></table>

Specifically, (1) breast-cancer: It contains 569 samples and each sample has 30 numerical features. It is used to predict whether a person has breast cancer or not. (2) sklearn-digits: The original sklearn-digits dataset consists of 1,797 gray-scale images with a size of 8×8 and is for multi-label classification task. We first flatten image into a vector of size 64, then we group images with an odd label into one class and all others into another class, so that we can train a binary classifier. (3) census-income: This dataset contains 48,842 samples and each sample is composed of 14 categorical and numerical features. We do feature engineering on it and finally get a dataset with 81 features, and it is used to predict whether a person could make \$50K a year. (4) give-me-some-credit: There are 150,000 samples and each one with a feature size of 10. It is used to predict whether a financial institution will loan money to a person.

TABLE III DATASETS CHARACTERISTICS 

<table><tr><td>Dataset</td><td># Samples</td><td># Features</td><td>Task</td></tr><tr><td>breast-cancer</td><td>569</td><td>30</td><td rowspan="4">Binary Classification</td></tr><tr><td>sklearn-digits</td><td>1,797</td><td>64</td></tr><tr><td>census-income</td><td>48,842</td><td>81</td></tr><tr><td>give-me-some-credit</td><td>150,000</td><td>10</td></tr></table>

2) Vertical Federated Learning System: We deploy the two parties Alice and Bob on two cloud machines with memory size 64GB. The two parties use remote procedure call framework, $\tt g R P C$ , to communicate with each other across the Internet, and use open-source package python-paillier

1https://scikit-learn.org/stable/modules/generated/breast-cancer   
2https://scikit-learn.org/stable/modules/generated/load-digits   
3http://archive.ics.uci.edu/ml/datasets/Census+Income   
4https://www.kaggle.com/c/GiveMeSomeCredit   
5https://github.com/grpc/grpc

[35] to implement Paillier cryptosystem. In our system, we allocate all features to Alice and only labels to Bob, so that we can evaluate the impact of extra noise on global model performance under such an extreme case, that’s because all gradients will be affected by the extra noise.

# B. Evaluation of $\mathcal { M } _ { a d d }$

Table II shows the accuracy and AUC score of the global model under different privacy budget , and the validation results of a model which is trained in a centralized manner are also presented as a baseline. For all four datasets, we can see that the model performance decreases as we decrease $\epsilon ,$ this is in line with what we talk about in Sec.IV-A, since in mechanism $\mathcal { M } _ { a d d } .$ we use a Laplace distribution $\mathrm { L a p } ( \textstyle { \frac { 2 } { \epsilon } } )$ with variance $2 ( \textstyle { \frac { 2 } { \epsilon } } ) ^ { 2 }$ to generate noise, a smaller  means that we ensure a stronger privacy guarantee for residue, but we get a noise distribution with larger variance, which affects the integrity of residue set and further the performance of the global model.

If the required privacy strength is not that high, $e . g . , \epsilon =$ 10, from Table II we can see that on dataset breast-cancer, sklearn-digits, census-income, and give-me-some-credit, when compared with the baseline, the accuracy of the global model only decrease 0.026, 0.003, 0.006, and 0.0001, which is really small, and the AUC score of global model merely decrease 0.004, -0.0006, 0.0003, 0.0003, which means that in sklearndigits dataset, the additive noise could even improve the AUC score. We presume that since the variance of the added noise is small, the additive noise has little negative impact on the integrity of the residue set, and in contrast, it improves the robustness of the global model.

# C. Evaluation of $\mathcal { M } _ { m u l t }$

As mentioned in Sec.IV-B, we multiply the residue by Laplace noise with a variance $2 \big ( \frac { 2 b _ { 2 } } { b _ { 1 } \epsilon } \big ) ^ { 2 }$ , which is determined by $b _ { 1 } , b _ { 2 }$ , and  together. So in this section, we investigate the impact of these parameters on the global model performance separately.

![](images/a6bea3b31b79f1bb40d39b2c82e89632907e1750f5bec66771417faae78607ed.jpg)



(a) breast-cancer

![](images/ebc4872beff3d5714bece43306b2e42df7d46b125417f2a54d172eac34b31b14.jpg)



(b) sklearn-digits

![](images/0726e505520e89c8cbd6358699472490b9be0db8c3e10069b7c0e823573af30c.jpg)



(c) census-income

![](images/9f4ce36f2946c19875036003e69957ba8773e42b17b1be7d4c50db369cd54652.jpg)



(d) give-me-some-credit

Fig. 1. Global model performance w.r.t. b1, where we fix $b _ { 2 } = 1 0$ and $\epsilon = 1 0 .$ .   
![](images/57df1788470ef621b0ad2e159c9aff122a7bd2c1b3aa60f40736a2a76cf14d89.jpg)



(a) breast-cancer

![](images/f524f5684ec8a45a668e519515b955cb87e8f6537dc3b2ce2db2f920458b127c.jpg)



(b) sklearn-digits

![](images/2cfb81c66ef39df831e5501c72a8300aa86a3cc65afb22f56588b722e093d1e3.jpg)



(c) census-income

![](images/1610945aae67a0ce831ce08d9225fcdb142e46eabfe0414bc57e218092f85393.jpg)



(d) give-me-some-credit

Fig. 2. Global model performance w.r.t. b2, where we fix $b _ { 1 } = 0 . 1$ and $\epsilon = 1 0 .$ .   
![](images/1584629b8b38af59c0ee3a5b9a1d325b2853b83534305f93d01321d28ea73dd2.jpg)



(a) breast-cancer

![](images/f8bc030f88f6f1865668aa07c82315bcbd37cbdc0c4254856d26041e0232f6d0.jpg)



(b) sklearn-digits

![](images/088f6260cdbb40a96d2a1ad5bf95736afa0a6bfe7b811827419c4827e5c91e2d.jpg)



(c) census-income

![](images/1aff066651821259ed014e5507d19b650e5b331fc9bb66050fd29afcc6d73275.jpg)



(d) give-me-some-credit   
Fig. 3. Global model performance w.r.t. , where we fix $b _ { 1 } = 0 . 1$ and $b _ { 2 } = 1 0 .$ .

1) Impact of clipping bound $b _ { 1 } .$ We fix both $b _ { 2 }$ and  to 10 and vary $b _ { 1 }$ from $2 ^ { - 6 } \ \mathrm {  t o } \ 2 ^ { 0 }$ to observe its impact. Fig.1 shows the accuracy and AUC score of the global model under different $b _ { 1 }$ . We observe that the trend in all four datasets is the same, and that is both the model accuracy and AUC score first increase and then decrease with $b _ { 1 }$ . We think the reason behind this is:

• With a small $b _ { 1 }$ although we have less possibility to trigger clipping method in Eq.7, but the $L _ { 1 }$ sensitivity calculated on residue set is big, so the variance of the multiplicative noise is large and we will trigger clipping method in $\operatorname { E q . }$ with high possibility. As a result, many residue items will be mapped to $b _ { 2 }$ by $\mathcal { M } _ { m u l t }$ , which are not informative enough for model training.   
• With a large $b _ { 1 }$ although the variance of the noise is not large, many residue items will be clipped to $b _ { 1 }$ , which causes the loss of integrity of the original residue set, and this is also not good for model training.

So we can draw a conclusion that there is a trade-off between the integrity of the original residue set and the variance of noise. Both a small $b _ { 1 }$ and a large $b _ { 1 }$ are not good enough to train a good global model. There exists an optimal

$b _ { 1 }$ between the small one and the large one, and this explains why the curve in Fig.1 increases first and then decreases with $b _ { 1 }$ .   
2) Impact of clipping bound $b _ { 2 } { \mathrm { : } }$ Similarly, we fix $b _ { 1 } = 0 . 1$ and $\epsilon = 1 0$ and vary $b _ { 2 }$ from 0.001 to 1,000 to observe its effect on global model performance. Fig.2 shows that model accuracy and AUC score also increase first and then decrease with $b _ { 2 } .$ . As in Sec.V-C1, we also give the reason as below:

• With a small $b _ { 2 }$ although the variance of noise is small, there is a high probability that the output of $\mathcal { M } _ { m u l t }$ will trigger the clipping method in Eq.8, which causes the information loss of residue set. As a result, the accuracy and AUC score are not high.

• A large $b _ { 2 }$ results in a large noise variance, and the original residue set with each item $- 1 < r < 1$ is mapped to a new set composed of very large items which cause the loss of model accuracy and AUC score, though these large items trigger Eq.8 with a low probability.

So we also draw a conclusion that there is a trade-off between the noise variance and the integrity of the new residue set after $\mathcal { M } _ { m u l t }$ , and this trade-off is controlled by parameter $b _ { 2 } .$ . Both a small $b _ { 2 }$ and a large $b _ { 2 }$ cause the loss of model performance severely.

TABLE IV TRAINING TIME (SECONDS) COMPARISON AMONG Madd, Mmult, Mhybrid AND [15] 

<table><tr><td>Dataset</td><td># Alice&#x27;s Features</td><td>Batch Size</td><td> $L_{RR}$ </td><td> $\mathcal{M}_{add}(s)$ </td><td> $\mathcal{M}_{mult}(s)$ </td><td>[15](s)</td><td> $\mathcal{M}_{hybrid}(s)$ </td><td>ratio</td></tr><tr><td>breast-cancer</td><td>30</td><td>16</td><td>40</td><td>3.5</td><td>3.5</td><td>554.2</td><td>957.4</td><td>1.73</td></tr><tr><td>sklearn-digits</td><td>64</td><td>32</td><td>70</td><td>5.6</td><td>5.7</td><td>2,415.8</td><td>4,142.5</td><td>1.71</td></tr><tr><td>census-income</td><td>81</td><td>32</td><td>90</td><td>100.5</td><td>101.8</td><td>74,049.6</td><td>131,299.8</td><td>1.77</td></tr><tr><td>give-me-some-credit</td><td>10</td><td>8</td><td>15</td><td>1,374.3</td><td>1,402.1</td><td>88,321.9</td><td>113,761.6</td><td>1.29</td></tr></table>

Notice that on dataset census-income and give-me-somecredit, when $b _ { 2 } ~ = ~ 1$ the AUC score is even higher than baseline, we presume this is also because the extra noise improves the model robustness as Sec.V-B.

3) Impact of : Fig.3 shows the model accuracy and AUC score w.r.t. privacy budget from $2 ^ { - 4 }$ to $2 ^ { 3 }$ on four datasets, where we set $b _ { 1 } = 0 . 1$ and $b _ { 2 } = 1 0$ respectively. Similarly, we see a trade-off between model utility and privacy strength, where with a smaller  we provide a stronger privacy guarantee for residue, but the performance of the global model is worse.

4) Comparison with $\mathcal { M } _ { a d d } \mathrm { : }$ In this section, we compare the performance of the two mechanisms $\mathcal { M } _ { a d d }$ and $\mathcal { M } _ { m u l t }$ under the same privacy budget. The noise variance in $\mathcal { M } _ { a d d }$ is only determined by $\epsilon ,$ but in $\mathcal { M } _ { m u l t }$ , it is determined by $\epsilon ,$ $b _ { 1 } ,$ and $b _ { 2 }$ together. So after searching for many combinations of $b _ { 1 }$ and $b _ { 2 } ,$ only the best model accuracy and AUC score of $\mathcal { M } _ { m u l t }$ we found are reported in Table II, and we get two main observations from it:

• When  is small, the performance of $\mathcal { M } _ { m u l t }$ is better than ${ \mathcal { M } } _ { a d d } .$ . For example, when $\epsilon = 0 . 0 1$ both model accuracy and AUC score in $\mathcal { M } _ { m u l t }$ are higher than that in $\mathcal { M } _ { a d d }$ on datasets breast-cancer, sklearn-digits, and census-income. Also, when $\epsilon = 0 . 1$ , the accuracy in $\mathcal { M } _ { m u l t }$ on breast-cancer and sklearn-digits dataset is higher than $\mathcal { M } _ { a d d }$ . We think this is because the noise variance in $\mathcal { M } _ { a d d }$ is really large, the original value in the residue set is overwhelmed by such noise. But in $\mathcal { M } _ { m u l t }$ due to the clipping method in $\mathrm { E q . 8 , }$ the item in the obscured residue set is no larger than that in ${ \mathcal { M } } _ { a d d } .$ so the model performance is better.   
• When  is large, $\mathcal { M } _ { a d d }$ performs better than $\mathcal { M } _ { m u l t }$ , which is because the noise variance in $\mathcal { M } _ { a d d }$ is small and the impact of the extra noise on model performance is negligible. But in $\mathcal { M } _ { m u l t }$ , due to the constraints of two clipping bounds $b _ { 1 }$ and $b _ { 2 } .$ , there is a large loss of integrity of residue set so that the model performance is worse.

Therefore, users can choose to use $\mathcal { M } _ { a d d }$ or $\mathcal { M } _ { m u l t }$ according to their privacy budget. We empirically enumerate different $b _ { 1 }$ and $b _ { 2 }$ to find the best model performance, how to search for the optimal clipping bounds is out of scope in this paper, we leave it for future research.

# D. Evaluation of $\mathcal { M } _ { h y b r i d }$

As mentioned in Sec.IV-C, the training protocol of $\mathcal { M } _ { h y b r i d }$ is not only secure but also lossless, because we set the residue of samples that are not in the ground-truth mini-batch to zero, these samples have no impact on the gradient. At each iteration, the gradient is kept intact so the global model performance is lossless when compared with the centralized one. Since these samples are also used during model training, which can cause the increase of protocol running time. So in this section, we investigate how much extra training time does $\mathcal { M } _ { h y b r i d }$ bring when compared with conventional protocol in [15].

Table IV shows the setting of key parameters and the corresponding training time on four datasets. In all cases, the number of Alice’s features is larger than the batch size, if we train vertical LR model via protocol in [15], Bob’s private labels are leaked. So we set $L _ { R R }$ larger than the number of Alice’s features in $\mathcal { M } _ { h y b r i d }$ such that Bob’s label is protected. The last column shows the ratio of the computation time of $\mathcal { M } _ { h y b r i d }$ to that of the protocol in [15], we observe that although we set $L _ { R R }$ larger than the number of Alice’s features which is equivalent to enlarge mini-batch size at each iteration, the ratio does not exceed 1.8 times on all four datasets, and this overhead is acceptable.

We also observe that the training time of $\mathcal { M } _ { a d d }$ and $\mathcal { M } _ { m u l t }$ is much less than $\mathcal { M } _ { h y b r i d }$ and the protocol in [15], the reason is that there are no encryption, decryption, addition on ciphertext and multiplication on ciphertext operations in these two mechanisms, but the disadvantages are that the extra noise decreases the model performance. So depending on users’ requirements, if they need a performance-lossless protocol, then $\mathcal { M } _ { h y b r i d }$ is a good choice, or else if they prefer an efficient protocol, then it’s suitable to choose either $\mathcal { M } _ { a d d }$ or $\mathcal { M } _ { m u l t }$ .

# VI. CONCLUSION

In this paper, we first present one label inference attack method to reveal the vulnerability of the widely used training protocol of vertical logistic regression. It shows that the attacker can utilize the residue variables to infer the privately owned labels. Then, we propose three residue protection mechanisms, $e . g .$ ., additive noise mechanism, multiplicative noise mechanism, and the hybrid mechanism which leverages LDP and HE techniques, to prevent the attack and improve the robustness of the vertical logistic regression model. Finally, we conduct comprehensive experiments to evaluate the effectiveness and efficiency of these three mechanisms. The results show that both the additive noise mechanism and the multiplicative noise mechanism can achieve efficient label protection with only a minor decrease of model performance in the case that the privacy budget is relatively high, and the hybrid mechanism can achieve label protection without any model accuracy degradation. In addition, the computation overhead of the hybrid mechanism is no more than 1.8 times that of the widely used vertical LR training protocol in [15], which is usually acceptable in practice .

# ACKNOWLEDGEMENT

Lan Zhang is the corresponding author. This research is supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, No. 62132018, No. 61822209, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002. This work was partially supported by“the Fundamental Research Funds for the Central Universities”.

# REFERENCES

[1] P. Voigt and A. Von dem Bussche, “The eu general data protection regulation (gdpr),” A Practical Guide, 1st Ed., Cham: Springer International Publishing, vol. 10, no. 3152676, pp. 10–5555, 2017.   
[2] S. C. of the National People’s Congress, “Personal information protection law of the people’s republic of china,” 2021. [Online]. Available: https://gkml.samr.gov.cn/nsjg/bgt/202111/t20211105 336460.html   
[3] L. Zhang, X.-Y. Li, K. Liu, C. Liu, X. Ding, and Y. Liu, “Cloak of invisibility: Privacy-friendly photo capturing and sharing system,” IEEE Transactions on Mobile Computing, vol. 18, no. 11, pp. 2488–2501, 2018.   
[4] L. Zhang, T. Jung, K. Liu, X.-Y. Li, X. Ding, J. Gu, and Y. Liu, “Pic: Enable large-scale privacy preserving content-based image search on cloud,” IEEE Transactions on Parallel and Distributed Systems, vol. 28, no. 11, pp. 3258–3271, 2017.   
[5] H. Du, L. Chen, J. Qian, J. Hou, T. Jung, and X.-Y. Li, “Patronus: A system for privacy-preserving cloud video surveillance,” IEEE Journal on Selected Areas in Communications, vol. 38, no. 6, pp. 1252–1261, 2020.   
[6] L. Zhang, X.-Y. Li, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in social networks,” in 2013 IEEE 33rd International Conference on Distributed Computing Systems. IEEE, 2013, pp. 327–336.   
[7] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial intelligence and statistics. PMLR, 2017, pp. 1273– 1282.   
[8] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” vol. 10, no. 2, pp. 1–19, 2019.   
[9] A. Li, L. Zhang, J. Tan, Y. Qin, J. Wang, and X.-Y. Li, “Sample-level data selection for federated learning,” in IEEE INFOCOM 2021-IEEE Conference on Computer Communications. IEEE, 2021, pp. 1–10.   
[10] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. M. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 372–383.   
[11] A. Li, L. Zhang, J. Wang, F. Han, and X. Li, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, 2021.   
[12] O. Li, J. Sun, X. Yang, W. Gao, H. Zhang, J. Xie, V. Smith, and C. Wang, “Label leakage and protection in two-party split learning,” arXiv preprint arXiv:2102.08504, 2021.

[13] X. Luo, Y. Wu, X. Xiao, and B. C. Ooi, “Feature inference attack on model predictions in vertical federated learning,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 181–192.   
[14] Y. Liu, Y. Kang, C. Xing, T. Chen, and Q. Yang, “A secure federated transfer learning framework,” IEEE Intelligent Systems, vol. 35, no. 4, pp. 70–82, 2020.   
[15] S. Yang, B. Ren, X. Zhou, and L. Liu, “Parallel distributed logistic regression for vertical federated learning without third-party coordinator,” arXiv preprint arXiv:1911.09824, 2019.   
[16] K. Cheng, T. Fan, Y. Jin, Y. Liu, T. Chen, D. Papadopoulos, and Q. Yang, “Secureboost: A lossless federated learning framework,” IEEE Intelligent Systems, vol. 36, no. 6, pp. 87–98, 2021.   
[17] Y. Zhang and H. Zhu, “Additively homomorphical encryption based deep neural network for asymmetrically collaborative machine learning,” arXiv preprint arXiv:2007.06849, 2020.   
[18] A. Acar, H. Aksu, A. S. Uluagac, and M. Conti, “A survey on homomorphic encryption schemes: Theory and implementation,” ACM Computing Surveys (Csur), vol. 51, no. 4, pp. 1–35, 2018.   
[19] P. Paillier, “Public-key cryptosystems based on composite degree residuosity classes,” in International conference on the theory and applications of cryptographic techniques. Springer, 1999, pp. 223–238.   
[20] C. Fontaine and F. Galand, “A survey of homomorphic encryption for nonspecialists,” EURASIP Journal on Information Security, vol. 2007, pp. 1–10, 2007.   
[21] A. C.-C. Yao, “How to generate and exchange secrets,” in 27th Annual Symposium on Foundations of Computer Science (sfcs 1986). IEEE, 1986, pp. 162–167.   
[22] L. Zhang, X.-Y. Li, Y. Liu, and T. Jung, “Verifiable private multiparty computation: ranging and ranking,” in 2013 Proceedings IEEE INFOCOM. IEEE, 2013, pp. 605–609.   
[23] T. Jung, X.-Y. Li, and M. Wan, “Collusion-tolerable privacy-preserving sum and product calculation without secure channel,” IEEE Transactions on Dependable and secure computing, vol. 12, no. 1, pp. 45–57, 2014.   
[24] C. Fu, X. Zhang, S. Ji, J. Chen, J. Wu, S. Guo, J. Zhou, and A. Liu, “Label inference attacks against vertical federated learning,” in 31st USENIX Security Symposium (USENIX Security 22), 2022.   
[25] Y. Liu, X. Zhang, and L. Wang, “Asymmetrical vertical federated learning,” arXiv preprint arXiv:2004.07427, 2020.   
[26] H. Weng, J. Zhang, F. Xue, T. Wei, S. Ji, and Z. Zong, “Privacy leakage of real-world vertical federated learning,” arXiv preprint arXiv:2011.09290, 2020.   
[27] T. T. Nguyen, X. Xiao, Y. Yang, S. C. Hui, H. Shin, and J. Shin, ˆ “Collecting and analyzing data from smart device users with local differential privacy,” arXiv preprint arXiv:1606.05053, 2016.   
[28] Q. Ye and H. Hu, “Local differential privacy: Tools, challenges, and opportunities,” in International Conference on Web Information Systems Engineering. Springer, 2020, pp. 13–23.   
[29] N. Wang, X. Xiao, Y. Yang, J. Zhao, S. C. Hui, H. Shin, J. Shin, and G. Yu, “Collecting and analyzing multidimensional data with local differential privacy,” in 2019 IEEE 35th International Conference on Data Engineering (ICDE). IEEE, 2019, pp. 638–649.   
[30] M. Chase and P. Miao, “Private set intersection in the internet setting from lightweight oblivious prf,” in Annual International Cryptology Conference. Springer, 2020, pp. 34–63.   
[31] B. Pinkas, T. Schneider, and M. Zohner, “Faster private set intersection based on {OT} extension,” in 23rd USENIX Security Symposium (USENIX Security 14), 2014, pp. 797–812.   
[32] H. Chen, Z. Huang, K. Laine, and P. Rindal, “Labeled psi from fully homomorphic encryption with malicious security,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, 2018, pp. 1223–1237.   
[33] S. L. Warner, “Randomized response: A survey technique for eliminating evasive answer bias,” Journal of the American Statistical Association, vol. 60, no. 309, pp. 63–69, 1965.   
[34] C. Dwork and A. Roth, “The algorithmic foundations of differential privacy.” Found. Trends Theor. Comput. Sci., vol. 9, no. 3-4, pp. 211– 407, 2014.   
[35] C. Data61, “Python paillier library,” https://github.com/data61/ python-paillier, 2013.