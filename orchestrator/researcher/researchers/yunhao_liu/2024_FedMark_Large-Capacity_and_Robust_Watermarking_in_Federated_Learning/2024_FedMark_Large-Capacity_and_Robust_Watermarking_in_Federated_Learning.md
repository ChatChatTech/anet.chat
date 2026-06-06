# FedMark: Large-Capacity and Robust Watermarking in Federated Learning

Lan Zhang∗†, Chen Tang†, Huiqi Liu†, Haikuo Yu†, Xirong Zhuang†, Qi Zhao†, Lei Wang, Wenjing Fang and Xiang-Yang Li†

†University of Science and Technology of China, Hefei, China

{chentang1999, liuhuiqi, yhk7786, xirongz, zq2020}@mail.ustc.edu.cn

Abstract—Machine learning models are increasingly recognized as valuable intellectual property (IP), prompting the development of a range of watermarking techniques aimed at safeguarding the IP of these models. However, in the context of federated learning (FL) models involving multiple owners, such as the participants in FL model training, conventional techniques designed for single-owner models prove ineffective due to limitations in their capacity and robustness. Few work has explored how to effectively embed watermarks to FL models for multiple-owners, which is non-trivial, especially when the number of owners is large. To fill this gap, we first analyze the capacity of existing watermarking methods. Second, we propose FedMark, a general large-capacity watermarking mechanism for FL, which leverages the Bloom Filter to achieve conflict-free watermarking of a large number of participants. Moreover, we propose a secret-sharing-based verification method to improve the watermarking robustness against false positives caused by Bloom Filter. Finally, comprehensive experiments show that our design can support over 150 participants to embed watermarks while the model accuracy varies within 1%, and is robust to non-independent identical distributed data, different participant selection rates, model modifications, permutation attacks, scaling attacks and forging attacks.

Index Terms—federated learning, watermarking, bloom filter

# I. INTRODUCTION

With machine learning models generating tremendous value across a wide range of industries, it has become a consensus that well-designed models represent crucial intellectual property (IP) for their creators. Since 2017, there has been a proliferation of work focusing on the protection of model IP in centralized learning scenarios [1]–[11]. Federated Learning (FL) [12] is a decentralized machine learning framework that allows multiple participants to jointly train models without explicitly sharing data. Since FL provides a practical solution to connect data silos in a privacy-preserving way, it has been widely adopted in various fields. There is no doubt that the FL model itself is also a valuable IP of participants, who contribute their data to the model training to obtain a better model or make a profit. However, there has been little exploration of how to prove that multiple subjects have contributed to the training of the FL model and have corresponding rights to the model.

Model watermarking [13] is a promising way to prove ownership of a model. However, most watermarking efforts ∗Lan Zhang (zhanglan@ustc.edu.cn) is the corresponding author.

are designed for centralized learning and only support single participant to embed a watermark. FedIPR [14], the only existing watermarking solution for FL with multiple owners simply applies a watermarking scheme from the centralized learning scenario to the FL scenario, however, is constrained to support only a limited number (<40) of participants.

In the real-world FL systems, it is noteworthy that these systems frequently involve a substantial number of participants, often exceeding 50 participants [15]. This observation underscores the inadequacy of the existing watermarking mechanisms in addressing the requirements of many real FL systems. There is still a lack of understanding of models’ watermark capacity and large-capacity watermarking mechanisms for FL systems. Here, watermark capacity is defined as the maximum number of successfully embedded watermarks that satisfy the following two conditions: 1) negligible impact of watermark embedding on model accuracy, i.e., the degradation of model accuracy is less than a threshold δ, e.g. 1%; 2) sufficiently high watermark detection rate, i.e., the watermark detection rate is above a threshold , e.g. 95%.

However, designing a large-capacity and robust watermarking mechanism for FL poses significant challenges, encountering three key challenges. (1) Watermarks embedded in local models may vanish or conflict in the global model during model aggregation. Participants cannot directly embed their watermarks into the global model, but only into their local models. During the FL model training, the aggregation (e.g., average) of multiple local models may cancel their watermarks in the global model, especially when the embedding positions of different watermarks have collisions. (2) Limited global model parameters naturally constrain the number of embedded watermarks. Since each participant embeds his/her watermark in a collision-free position into the model to avoid conflicts among watermarks, the total bits of the watermark grow linearly with the number of participants. Consequently, the watermark capacity is constrained by the number of global model parameters. Therefore, the number of global model parameters limits the watermark capacity. (3) Watermarks for FL models are vulnerable to various attacks. Since an FL model is trained and owned by multiple subjects, it gives an attacker more chance to sabotage or forge the watermark. Besides, the server should be semi-honest and not collect any participants’ watermarking information.

To address the aforementioned challenges, we firstly provide theoretical proof regarding the feasibility of embedding a substantial number of watermarks in the global model by adopting a strategy of locally embedding watermarks. Building upon this conceptual foundation, we elucidate the limitations inherent in current FL watermarking methodologies. Specifically, embedding watermarks directly in different positions in a model results in constrained watermark capacity due to finite parameters. Conversely, embedding watermarks in the same position leads to limited capacity owing to watermark conflicts. To address this issue, we propose FedMark, a largecapacity and robust FL watermark embedding mechanism, which leverages the Bloom Filter to enable a large number of participants(≥ 150) to embed their watermarks with 100% watermark detection rate while has a negligible impact (<1%) on the model accuracy. This innovative mechanism employs multiple hash functions to hash the watermarks, thereby reducing the number of parameters occupied by each watermark, which effectively overcomes the limitation imposed by limited parameters. Moreover, the hash values of distinct watermarks are sparsely distributed, contributing to the efficient control of the probability of position collision among watermarks and thereby mitigating watermark conflicts. Ultimately, we design a secret-sharing-based verification method that shares the embedding matrix of each participant as a secret to other participants to prevent false positives that may arise from the Bloom Filter.

Our main contributions are three-fold, as follows:

• We theoretically prove the feasibility of embedding a large number of watermarks into the global model via embedding watermarks locally.   
• We identify the bottlenecks for embedding a large number of watermarks in an FL model: limited parameters and watermark conflicts. Subsequently, we propose FedMark, a large-capacity and robust FL watermark embedding mechanism to address these bottlenecks. Besides, we design a secret sharing-based verification method to enhance the robustness of FedMark against false positives.   
• Comprehensive experiments show that the watermark capacity of FedMark can achieve more than 150, which fulfills the needs of many real FL systems. Moreover, FedMark hides watermarks well and does not change the statistical characteristics of the model parameters. The watermarks are robust to non-independent identical distributed data, different participant selection rates, model modifications, and various attacks, including permutation attacks, scaling attacks and forging attacks.

The rest of the paper is as follows. §II provides the preliminary and surveys related work. §III conduct the capacity analysis to identify the limitations in existing methods. Problem definition, threat model and the design of FedMark is described in §IV. §V provides the secret-sharing-based verification method to improve the robustness of FedMark against false positives. §VI evaluate the capacity, secrecy and robustness of FedMark. Finally, §VII concludes this paper, discusses the limitations and future work.

# II. PRELIMINARY AND RELATED WORK

# A. Centralized Model Watermarking

Since 2017, a series of efforts have been devoted to protecting IP of a machine learning model by embedding a watermark into the model [13]. Those works fall into two main categories: model parameters-based watermarking and model behaviorbased watermarking.

1) Model Parameters-based Watermarking: This class of watermarking schemes construct a mapping between the watermark and model parameters. The first watermarking method is proposed by Uchida et al. [1]. In their work, the watermark is embedded into one of the convolution layers by building a mapping between convolution layer’s parameters W and a T -bit watermark $b \in \{ 0 , 1 \} ^ { T }$ . Here, we review some details of [1] for a better understanding of our analysis and design. In [1], the convolution layer parameters are denoted by $W \in$ $\mathbb { R } ^ { S \times \bar { S } \times D \times L }$ , where S is the size of the convolution filter, D is the depth of input to the convolution layer and L is the number of filters. To remove the arbitrariness in the order of filters, the mean of W over L filters is calculated as $\begin{array} { r } { \overline { { W } } = \frac { 1 } { L } \sum _ { l = 0 } ^ { L - 1 } W _ { l } . } \end{array}$ . Then W is flattened to obtain w $\in \mathbb { R } ^ { M } ( M = \beth \ast \ b { S } \ast \ b { D } )$ , and a derivation matrix $\boldsymbol { X } \in \mathbb { R } ^ { M \times T }$ is randomly generated, in which each element is independently drawn from the standard normal distribution $\mathcal { N } ( 0 , 1 )$ . Finally, the target of embedding the watermark b is to make $s ( w * X ) = b$ hold by adding an additional embedding loss term $E _ { R } ( w , b )$ into the loss function, which is defined as:

$$
E _ {R} (w, b) = - \sum_ {j = 0} ^ {T - 1} (b _ {j} * \log (b _ {j} ^ {\prime}) + (1 - b _ {j}) * \log (1 - b _ {j} ^ {\prime})), \tag {1}
$$

where $b ^ { \prime } = s ( w * X )$ is the extract watermark and $b _ { j } ^ { \prime }$ is its j-th bit. $s ( x ) = \left\{ { 1 , \ : i f \ : x \geq 0 } \right.$ , is the step function to simplify the mapping. In the verification stage, the watermark detection rate d is defined as: $\begin{array} { r } { d \ = \ \frac { 1 } { T } d _ { 1 } ( b , b ^ { \prime } ) } \end{array}$ , where $d _ { 1 }$ is the $L _ { 1 } -$ distance. If the watermark detection rate d is above a default threshold , verification passes; otherwise, verification fails.

Subsequently, a series of methods have been proposed to improve the watermark robustness [3], [5]–[9], [16], [17]. All those work are designed for the centralized scenario with a single owner. They cannot be directly applied to FL models with multiple owners due to the watermark vanishing effect during model aggregation and possible conflicts among different owners’ watermarks.

2) Model Behavior-based Watermarking: This class of watermarking schemes [18] trigger a model’s unique behaviors (e.g., pre-defined outputs) as watermarks. Those efforts are usually task-specific and poorly generalized. In this work, we focus on the model parameters based watermarking and leave the capacity of model behavior based watermarking as our future work.

# B. FL Model Watermarking

Recently, IP protection for FL models has been attracting increasing attention. There have been three watermarking methods for FL. Atli et al. [19] assume that the FL model has only one owner, i.e., the server, who can directly embeds one watermark into the global model. Li et al. [20] propose to encode the watermarking images and upload them to the server, allowing the server to decode and subsequently embed these images into the global model. Both approaches operate under the assumption of a trusted server, receiving all watermarking information, rendering them impractical for FL scenarios involving semi-honest servers. In this work, we assume the server is semi-honest, and the most relevant work is FedIPR [14], which directly applies the watermarking method for centralized models [1], [21] to FL models. However, a notable limitation of their approach is the lack of consideration for the crucial issue of watermarking capacity. Indeed, their method only supports a limited number of participants (fewer than 40) for watermark embedding, falling short of the requirements for numerous real-world FL systems. Additionally, it exhibits vulnerability to various attacks, including forging and watermark overwriting attacks.

In summary, we aim to design the first large-capacity and robust watermarking mechanism for real-world FL systems, where the server is semi-honest and does not collect any extra information while participants only need to embed watermarks into their local models. We need to address the challenges raised by limited model parameters and possible watermark conflicts of multiple local models, as well as various attacks.

# III. CAPACITY ANALYSIS

In this section, we model the parameters-based embedding of multiple watermarks in an FL model and analyze the bottlenecks of watermark capacity.

To better illustrate the limitations of the centralized watermarking method in FL models, before understanding the watermarking capacity of FL models, we first analyze the centralized watermarking approach and obtain the following lemma:

Lemma 1. ∀ $w \in \mathbb { R } ^ { M } \backslash \{ \mathbf { 0 } \}$ and $b \in \{ 0 , 1 \} ^ { T } , \exists X \in \mathbb { R } ^ { M \times T }$ , $s . t . ~ s ( w * X ) = b .$ .

Proof. For any w $\in \mathbb { R } ^ { M } \backslash \{ \mathbf { 0 } \} , b \in \{ 0 , 1 \} ^ { T }$ , we aim to find a suitable $\boldsymbol { X } \in \mathbb { R } ^ { M \times T }$ to make $s ( w * X ) = b$ hold, where $s ( x ) = { \left\{ \begin{array} { l l } { 1 , ~ i f ~ x \geq 0 , } \\ { 0 , ~ e l s e , } \end{array} \right. }$ is the step function.

$\mathrm { C o n s i d e r } \ w = \left[ w _ { 1 } \quad . . . \quad w _ { M } \right] , \ b = \left[ b _ { 1 } \quad . . . \quad b _ { T } \right] ,$

$$
X = \left[ \begin{array}{c c c c} X _ {1 1} & X _ {1 2} & \dots & X _ {1 T} \\ X _ {2 1} & X _ {2 2} & \dots & X _ {2 T} \\ \dots & \dots & \dots & \dots \\ X _ {M 1} & X _ {M 2} & \dots & X _ {M T} \end{array} \right], \tag {2}
$$

let $X _ { i } = \left[ X _ { 1 i } \quad \dots \quad X _ { M i } \right] ^ { \prime }$ , then $X = \left\lceil X _ { 1 } \quad \ldots \quad X _ { T } \right\rceil$ , and

$$
s (w * X) = b \iff s (w * X _ {j}) = b _ {j}, f o r j \in [ 1, \dots , T ]. \tag {3}
$$

Let

$$
\hat {b _ {j}} = \left\{ \begin{array}{l} 1, i f b _ {j} = 1, \\ - 1, i f b _ {j} = 0, \end{array} \right. \tag {4}
$$

then when $\hat { b _ { j } } = 1 , s ( w * X _ { j } ) = b _ { j } = 1$

$$
\Rightarrow s (w * X _ {j}) = 1 \Rightarrow w * X _ {j} > 0 \Rightarrow w * X _ {j} * \hat {b _ {j}} > 0;
$$

when $\hat { b _ { j } } = { - 1 , s ( w * X _ { j } ) } \mathop { = } b _ { j } = 0$

$$
\Rightarrow s (w * X _ {j}) = 0 \Rightarrow w * X _ {j} <   0 \Rightarrow w * X _ {j} * \hat {b _ {j}} > 0.
$$

Therefore, $s ( w * X ) = b$ is equivalent to T linear inequalities:

$$
w * X _ {j} * \hat {b _ {j}} > 0, \text {   for   } j \in [ 1,..., T ]. \tag {5}
$$

The existence of X that makes $\operatorname { E q . } ( 5 )$ hold for each j can be simply proved by standard linear optimization [22, Section 1.5]. □

Based on Lemma 1, we have:

•Conclusion #1: For any model, we can always generate suitable embedding matrix X to make $s ( w * X ) = b$ hold, i.e., the watermark b can be successfully embedded into the model.

Through conclusion #1, we prove that the watermarking method [1] is theoretically feasible. However, in practice, X is generated before the model is trained and w is obtained by heuristic search during training, then w and b may not satisfy the mapping $s ( w * X ) = b$ after training. Therefore, Uchida [1] proposed to add an embedding loss term (1) into the loss function to make $s ( w * X ) = b$ hold. Even though, there is still a risk of watermark embedding failure $( \mathrm { i . e . }$ , the watermark detection rate less than  or the degradation of model accuracy higher than δ) due to inappropriate settings, such as the length of w, which has an important impact on watermark embedding, as analyzed below.

Since training the model is an optimization problem, we model embedding a watermark in the model as adding a constraint $s ( w * X ) = b$ to the optimization. For fixed X and $b ,$ the constraint is $s ( w * X ) = b$ equivalent to $T$ linear inequalities with M unknowns, as we proved in Lemma 1. When reducing the length of w, M gets smaller, then the inequality constraint becomes stronger, which makes searching for a suitable w more difficult or even impossible. Therefore, we have:

•Conclusion #2: In practice, to successfully embed a given watermark b, the length of w should be sufficiently long. Otherwise, it is difficult or even impossible to find a suitable w, resulting in a high probability of embedding failure.

Conclusion #1 and #2 show that it is feasible to embed a watermark into a model, but the watermark requires sufficient space (i.e., model parameters) to be successfully embedded.

Now we are ready to analyze the watermark capacity for FL models. Suppose there are K participants involved in FL. For each participant $p _ { k }$ and his/her watermark $b _ { k }$ , the target of watermarking is to make $s ( w _ { k } ^ { G } * X _ { k } ) = b _ { k }$ hold, where $w _ { k } ^ { G }$ is part of the global model’s flattened convolution layers’ parameters, which indicates where the watermark of $p _ { k }$ is embedded in the global model. $X _ { k }$ is the embedding matrix of $p _ { k }$ . However, participants of FL cannot embed their watermarks into the global model directly, but only into their local models, that is, $s ( w _ { k } ^ { L } * X _ { k } ) = b _ { k }$ , where $w _ { k } ^ { L }$ is the same part of flattened convolution layers’ parameters in $\boldsymbol { p _ { k } } ^ { \prime } \mathbf { s }$ local model. Following theorem illustrates that each local watermark $b _ { k }$ can theoretically be embedded into the global model.

Theorem 1. $\mathcal { I } w _ { k } ^ { L } , w _ { k } ^ { G } \in \mathbb { R } ^ { M } \backslash \{ \mathbf { 0 } \}$ and $b _ { k } \in \{ 0 , 1 \} ^ { T } , \exists X _ { k } \in$ $\mathbb { R } ^ { M \times T }$ , s.t. $s ( w _ { k } ^ { L } * X _ { k } ) = b _ { k }$ and $s ( w _ { k } ^ { G } * X _ { k } ) = b _ { k }$ .

Proof. The target is to find a suitable $X _ { k }$ to make $s ( w _ { k } ^ { L } \ast$ $X _ { k } ) = b _ { k }$ and $s ( w _ { k } ^ { G } * X _ { k } ) = b _ { k }$ hold simultaneously.

Constructing a suitable $X _ { k }$ is similar to the proof of Lemma 1. Let $\hat { b _ { k j } } = \left\{ { \begin{array} { l } { 1 , ~ i f ~ b _ { k j } = 1 , } \\ { - 1 , ~ i f ~ b _ { k j } = 0 . } \end{array} } \right.$ then $s ( w _ { k } ^ { L } * X _ { k } ) = b _ { k }$ is , equivalent to

$$
w _ {k} ^ {L} * X _ {k j} * \hat {b _ {k j}} > 0, f o r j \in [ 1, 2,..., T ]. \tag {6}
$$

and $s ( w _ { k } ^ { G } * X _ { k } ) = b _ { k }$ is equivalent to

$$
w _ {k} ^ {G} * X _ {k j} * \hat {b _ {k j}} > 0, f o r j \in [ 1, 2,..., T ]. \tag {7}
$$

The existence of $X _ { k }$ that makes $\operatorname { E q . } ( 6 )$ and (7) hold simultaneously can be proved by standard linear optimization [22, Section 1.5]. □

Theorem 1 illustrates that suitable embedding matrix $X _ { k }$ can be found to make $s ( w _ { k } ^ { L } * X _ { k } ) = b _ { k }$ and $s ( w _ { k } ^ { \bar { G } } * X _ { k } ) = b _ { k }$ hold, i.e., the watermark $b _ { k }$ can be successfully embedded into the global model. Since each participant’s embedding matrix is different, Theorem 1 can be directly generalized to K participants, that is,

$\begin{array} { r l r l } { \cdot } & { { } \forall } & { \{ w _ { k } ^ { L } \} _ { k = 0 } ^ { K - 1 } , \{ w _ { k } ^ { G } \} _ { k = 0 } ^ { K - 1 } } & { { } \in } & { \mathbb { R } ^ { M } \backslash \{ \mathbf { 0 } \} } \end{array}$ $\left\{ b _ { k } \right\} _ { k = 0 } ^ { K - 1 } \in \{ 0 , 1 \} ^ { T } , \ \exists \ \left\{ \tilde { X _ { k } } \right\} _ { k = 0 } ^ { K - 1 } , \ \tilde { s . t . } \ \forall k , s ( w _ { k } ^ { L } * \tilde { X _ { k } } ) = b _ { k }$ and $s ( w _ { k } ^ { G } * X _ { k } ) = b _ { k }$ .

$\{ b _ { k } \} _ { k = 0 } ^ { K - 1 }$

First consider $b _ { 0 } , w _ { 0 } ^ { L } , w _ { 0 } ^ { G }$ , from Theorem 1, we know that ∃X0 to make $s ( w _ { 0 } ^ { L } * X _ { 0 } ) = b _ { 0 }$ and $s ( w _ { 0 } ^ { G } * X _ { 0 } ) = b _ { 0 }$ hold.

Then consider b1, wL1 , wG1 , from Theorem 1, we know that $\exists X _ { 1 }$ to make $s ( w _ { 1 } ^ { L } * X _ { 1 } ) = b _ { 1 }$ and $s ( w _ { 1 } ^ { G } * X _ { 1 } ) = b _ { 1 }$ hold.

Finally consider $b _ { K - 1 } , w _ { K - 1 } ^ { L } , \underline { { { w } } } _ { K - 1 } ^ { G } ,$ , from Theorem 1, we know that $\exists X _ { K - 1 }$ to make $s ( w _ { K - 1 } ^ { L } \ast X _ { K - 1 } ) = b _ { K - 1 }$ and $s ( w _ { K - 1 } ^ { G } \ast X _ { K - 1 } ) = b _ { K - 1 }$ hold.

s(wK−1 ∗ XK−1) = bK−1 That is, ∀ {wLk }K−1k=0 , {wGk }K−1k=0 K−1 T K−1 $\mathrm { ~  ~ { ~ \hat { ~ } { ~ i ~ s ~ } ~ } ~ } \forall \quad \{ w _ { k } ^ { L } \} _ { k = 0 } ^ { K - 1 } , \{ w _ { k } ^ { G } \} _ { k = 0 } ^ { K - 1 } \quad \in \quad \mathbb { R } ^ { M } \backslash \{ { \bf 0 } \}$ and $\{ b _ { k } \} _ { k = 0 } ^ { K - 1 } \in \{ 0 , 1 \} ^ { T } , \exists ^ { \circ } \{ { \check { X } } _ { k } \} _ { k = 0 } ^ { K - 1 ^ { \circ } } , \{ \mathrm { ~ s . t . ~ } \forall k , s ( w _ { k } ^ { L } \ast \check { X } _ { k } ) = b _ { k }$ Kand $\ddot { s ( w _ { k } ^ { G } * X _ { k } ) } = b _ { k }$ . □

Corollary 1 illustrates that watermarks of K participants can be successfully embedded into both the local and global model. Then we have following conclusion:

•Conclusion #3: For any FL model with K participants, there exist suitable embedding parameters $\{ X _ { k } \} _ { k = 0 } ^ { \bar { K } - 1 }$ , which allow multiple local watermarks to be embedded into the global model.

Conclusion #3 shows that embedding multiple watermarks into the FL model is theoretically feasible. However, it is hard to achieve in practice. First of all, $X _ { k }$ is generated by each participant prior to training, while $w _ { k } ^ { L }$ and $w _ { k } ^ { G }$ are searched during training. Then we further identify capacity bottlenecks for multiple watermark embedding in real FL systems for two typical cases: embedding watermarks in different positions and embedding watermarks in the same position. For the first case, FedIPR [14] asks different participants to embed watermarks in different positions of the FL model. Such a method has the following limitations: (1) embedding multiple watermarks into different positions is difficult to achieve, as participants are usually reluctant to negotiate embedding positions with each other, since exposing the embedding position makes the watermark more vulnerable to various attacks; (2) according to Conclusion #2, for each participant, $w _ { k }$ must be sufficiently long for successful embedding, but the total number of model parameters is limited, which naturally constraints the watermark capacity. For the second case, when participants embed watermarks into the same position, the constraint is equivalent to T linear inequalities with M unknowns for each participant. As the participant number K increases, the total number of constraints $K * T$ becomes larger, making conflicts among watermarks happen more frequently, leading to embedding failures.

•Conclusion #4: For FL, when the number of participants increases, embedding watermarks into different positions leads to limited capacity due to limited model parameters, while embedding watermarks into the same position leads to limited capacity due to watermark conflicts.

As a conclusion of this section, our analyses reveal the bottlenecks for embedding a large number of watermarks in an FL model: limited parameters and watermark conflicts. In the following sections, we will propose a novel mechanism FedMark, which can significantly address above bottlenecks.

# IV. WATERMARK EMBEDDING OF FEDMARK

# A. Problem Definition and Threat Model

We consider typical horizontal FL scenarios1 with K participants and a server S. The server S only provides the standard model aggregation service, no additional operations are required. The target of each participant $p _ { k }$ is to obtain a global model with his/her watermark $b _ { k }$ successfully embedded, that is, the watermark has negligible impact on the model accuracy and the watermark detection rate $d _ { k }$ is above a threshold . Since both participants and the server aim to train a global model with good performance, as most existing work [15], [23], we assume all participants and the server are semi-honest. They will not launch any malicious attacks, but are curious about other participants’ watermarks.

Meantime, there may exist some external malicious attackers with the goal of falsely claiming the ownership of a watermarked model and using the model illegally. They achieve their goal by corrupting participants’ watermarks in the FL model or forging a watermark to pass the verification.

Our goal is to design a watermark embedding mechanism for horizontal FL, which can successfully embed the watermarks of a large number of participants (e.g., more than one hundred participants) and is robust against various attacks, $\mathrm { e . g . }$ , permutation attack, scaling attack, and forging attack.

Algorithm 1: FedMark.   
Input: N hash functions are indexed by n; C is the selection rate for selecting a certain percentage of participants in each epoch. K is the number of participants; $w_{k}$ are the flattened local parameters to embed the watermark of participant k; $\eta$ is the learning rate; W are model parameters, $W_{t}$ is model parameters of round t, $W_{t}^{k}$ is $p_{k}$ 's local model parameters of round t.

Client Initialize:
for each participant $p_{k}$ do
    initialize $B_{k}, X_{k}, b_{k}$ for each $n = 0, 1, ..., N - 1$ do
    add $hash_{n}(b_{k})$ to $B_{k}$ end
end

Server executes:
initialize $W_{0}$ for each global round t do $m \leftarrow max(C * K, 1)$ $S_{t} \leftarrow (\text{random set of } m \text{ participants})$ for each participant $p_{k} \in S_{t}$ in parallel do $W_{t+1}^{k} \leftarrow \text{ClientUpdate}(k, W_{t})$ end $W_{t+1} \leftarrow \frac{1}{m} \sum_{k=1}^{m} W_{t+1}^{k}$ end

ClientUpdate(k, W): // Run on participant k
for each local epoch do
    for each batch do $E(W) \leftarrow E_{0}(W) + \lambda \sum_{j \in B_{k}} log(s(w_{k}X_{k})[j])$ $W \leftarrow W - \eta \nabla E(W)$ end
end

return W to server

# B. Embedding Mechanism of FedMark

We propose FedMark to enable embedding a large number of watermarks in an FL model. Given K participants’ watermarks $\{ b _ { k } \} _ { k = 0 } ^ { K - 1 } \in \{ 0 , 1 \} ^ { T }$ , instead of embedding each Filter [24] to embed hash values of each watermark into the corresponding positions in the convolutional layers. Compared with other hash functions, Bloom Filter is extremely space efficient, which can dramatically reduce the number of parameters occupied by each watermark. Besides, sparsely and randomly distributed hash values of different watermarks can hide the position of each watermark well, and effectively control the probability of position collision among watermarks. In this way, FedMark breaks two bottlenecks mentioned in Conclusion #4 in Section III and significantly enlarges the watermark capacity.

The workflow of FedMark is illustrated in Fig.1. For initialization, FedMark selects N common hash functions for the Bloom Filter, which maps each watermark $b _ { k }$ to N integers $( N \ll T , T$ is the length of the watermark). The range of watermark embedding positions should also be determined, which can be the whole convolutional layers by default or part of the convolutional layers’ parameters by negotiation. Each $p _ { k }$ determines his/her embedding matrix $X _ { k }$ and watermark $b _ { k } .$ . When the training and watermarking starts, $p _ { k }$ first uses these N hash functions to hash $b _ { k }$ , and records N result integers into a list $B _ { k } . \mathrm { N e x t } , p _ { k }$ extracts parameters within the range of watermark embedding positions, calculates the mean of these parameters over filters and flattens the result to obtain $w _ { k } .$ Finally, by updating the model parameters during training, $p _ { k }$ constructs a mapping between $w _ { k }$ and $\boldsymbol { B } _ { k } ,$ , which satisfies

$$
s (w _ {k} * X _ {k}) [ j ] = 1, \quad f o r j \in \mathcal {B} _ {k}. \tag {8}
$$

To obtain both a well-performing model and a successfully embedded watermark, for $p _ { k }$ , the loss function of his/her local model is defined as:

$$
E (W) = E _ {0} (W) + \lambda E _ {R} (w _ {k}, b _ {k}), \tag {9}
$$

$$
E _ {R} (w _ {k}, b _ {k}) = - \sum_ {j} [ b _ {k j} \log (b _ {k j} ^ {\prime}) + (1 - b _ {k j}) \log (1 - b _ {k j} ^ {\prime}) ],
$$

$$
b _ {k j} ^ {\prime} = s (w _ {k} * X _ {k}) [ j ], b _ {k j} = 1, f o r j \in \mathcal {B} _ {k}. \tag {10}
$$

$E _ { 0 } ( W )$ is the original learning task loss function, $W$ is total model parameters. $E _ { R } ( w _ { k } , b _ { k } )$ is the embedding loss term to embed $b _ { k } . \ : b _ { k j }$ is the j-th bit of $b _ { k } . \lambda$ is an adjustable parameter.

Each participant trains his/her local model with loss function (9) in the training phase, and uploads the model parameters to the server. The server updates the global model by aggregating model parameters in a standard way [25] , and distributes the updated model to participants. Participants and the server continue this process until the end of training. The formal algorithm of FedMark is shown in Algorithm 1.

In the verification phase, the detection rate of the watermark $b _ { k }$ is

$$
d _ {k} = \frac {1}{N} \sum_ {j = \mathcal {B} _ {k} [ 0 ]} ^ {\mathcal {B} _ {k} [ N - 1 ]} s (w _ {k} * X _ {k}) [ j ]. \tag {11}
$$

Verification passes if $d _ { k } \geq \epsilon .$ , which means that $p _ { k }$ has the ownership of the FL model; Otherwise, verification fails.

# C. Performance Analysis

We analyze the capacity, secrecy and computational cost of FedMark, and show FedMark has the following advantages.

1. Significantly larger watermark capacity: Leveraging Bloom Filter, FedMark allows a long watermark $( \mathrm { e . g . , } T \mathrm { ~ = ~ }$ 256) to be embedded into N parameters $( { \bf e . g . } , \ N \ = \ 9 )$ . In this way, FedMark dramatically reduces the number of parameters required for each watermark, as well as the number of constraints. Moreover, the random and sparse hash values greatly reduce the possibility of collisions among different watermarks. Therefore, FedMark achieves a significantly large watermark capacity.

In more detail, we perform a qualitative analysis of watermark capacity in FL scenarios, considering limited parameters and watermark conflicts.

![](images/d6e9bd776bf0e4c262d1dc6839e26c76c70117773968481a006d3e6e2dd12a6c.jpg)



Fig. 1. Workflow of FedMark.

FedIPR [14] embeds watermarks into different positions, which is equivalent to adding

$$
s (w _ {k} ^ {G} * X _ {k}) = b _ {k}, \tag {12}
$$

to the learning task. For each participant, (12) is equivalent to $T$ inequalities as we proved in Lemma 1. The number of total constraints added by all participants is $T * K$ . In addition, the number of model parameters limits the maximum capacity to $\frac { \overline { { | w | } } } { | w _ { k } ^ { G } | }$ where w are total flattened convolution layers’ kparameters. In FedMark, the constraints for each participant become:

$$
s (w _ {k} ^ {G} * X _ {k}) [ j ] = 1, \text {   for   } j \in \mathcal {B} _ {k}. \tag {13}
$$

The number of constraints reduces from $T * K$ to $N * K$ . Typically, N is set to $\begin{array} { r } { 0 . 7 * \frac { | s ( w _ { G } * X _ { k } ) | } { r } } \end{array}$ [26] to efficiently use the space of Bloom Filter. Taking $\stackrel { \wedge } { T } = 2 5 6 , \stackrel { \cdot } { \vert } s ( w _ { G } \ast X _ { k } ) \stackrel { \cdot } { \vert } = 2 5 6 ,$ , $K = 2 0$ as an example, each watermark only occupies $N =$ 9 parameters instead of 256 parameters, and the number of constraints decreases from 5120 to 180. Since FedMark is very space efficient and $N * K$ constraints are mush easier to meet, the model parameters are used more efficiently for watermark embedding and the watermark capacity significantly increases.

Moreover, when FedMark is not utilized, each participant k aims to satisfy the condition $s ( w _ { k } ^ { G } * X _ { k } ) = b _ { k }$ . According to the analysis in the proof of Lemma 1, (5) shows that

$$
s (w _ {k} ^ {G} * X _ {k}) = 1, \quad \text { for   } j \in [ 1,..., T ] \tag {14}
$$

$$
\Longleftrightarrow w _ {k} ^ {G} * X _ {k j} * \hat {b _ {j}} > 0, \text {   for   } j \in [ 1,..., T ]. \tag {15}
$$

The equality $w _ { k } ^ { G } \ast X _ { k j } \ast \hat { b _ { j } } > 0$ involves M unknowns, and $s ( w _ { k } ^ { G } \ast X _ { k } ) = \ddot { b _ { k } }$ is equivalent to T inequalities. Therefore, the number of total inequalities is $T * K$ , where K is the number of participants. According to the property of inequalities, when $M \geq T * K$ , solutions definitely exist for these inequalities. Therefore, in order to successfully embed all the watermarks into the global model, M should be set to a sufficient length. Otherwise, watermarks have a high probability conflicts when $M \leq T * K$ .

However, when FedMark is utilized, each participant k aims to satisfy the condition (13). According to the analysis in the proof of Lemma 1, (5) shows that:

$$
s (w _ {k} ^ {G} * X _ {k}) [ j ] = 1, \quad \text { for   } j \in \mathcal {B} _ {k} \tag {16}
$$

$$
\Longleftrightarrow w _ {k} ^ {G} * X _ {k j} * \hat {b _ {j}} > 0, \text {   for   } j \in \mathcal {B} _ {k}. \tag {17}
$$

Since $X _ { j }$ and $\hat { b _ { j } }$ are fixed and $w _ { k } ^ { G } \in \mathbb { R } ^ { M }$ , the equality $w _ { k } ^ { G } \ast \check { X _ { k j } } \ast \hat { b _ { j } } > 0$ involves M unknowns, and (16) is equivalent to N inequalities, where N is the length of $\boldsymbol { B } _ { k }$ . Therefore, the number of total inequalities is $N * K$ . According to the property of inequalities, when $M \geq N * K$ , solutions definitely exist for these inequalities. However, when $N \ll T$ , it becomes significantly easier to satisfy $M \geq N * K$ , thus mitigating watermark conflicts and substantially increasing the watermark capacity.

2. Better protection of watermarks: In contrast to previous methods that embed watermarks into long and consecutive segments of parameters, in FedMark, each participant secretly embeds his/her watermark into a few randomly scattered bits. For each watermark, only its owner $p _ { k }$ knows $b _ { k } , \ B _ { k }$ (the embedding positions) and $X _ { k }$ . This makes it significantly more difficult for a curious party or an attacker to guess the exact positions and content of a watermark, thus reducing the success rate of corrupting participants’ watermarks.

More specifically, the server only receives local model updates from participants. By observing the parameter changes between different rounds, it is difficult for the server to distinguish a few scattered parameter changes caused by watermark embedding from a large number of parameter changes caused by the learning task itself. Hence, the server can hardly infer watermark embedding positions. It is even harder for the server to infer a watermark $b _ { k } .$ , since $b _ { k }$ is protected by N hash functions and a secret transformation $X _ { k }$ . For a participant curious about other participants’ watermarks, he/she only receives the aggregated global model from the server. Due to the model averaging operation, he/she has less accurate information than the server, therefore less likely to infer any watermark information of other participants. For attackers, they have no clue where watermarks are embedded, so it is difficult to successfully sabotage watermarks.

3. Smaller computational cost: In previous work, for each participant, when computing the watermark embedding loss, the computational cost in each epoch is the total dimension of b, i.e., T . With our proposed loss function $\operatorname { E q . } ( 9 )$ , this cost reduces from T to $N \ ( \mathrm { e . g . \ 2 5 6 \ }  \ 9 )$ , which greatly saves the computational cost of watermark embedding for each participant.

If participants only need a large-capacity watermark embedding mechanism to verify their ownership, FedMark is sufficient to meet their requirements. However, an attacker can still leverage the false positives of Bloom Filter to generate a watermark and fake an embedding matrix to pass the verification once the FL model is leaked(called forging attack). Therefore, we design a secret sharing-based watermark verification method in the next section to make FedMark robust to false positives.

# V. SECRET SHARING-BASED VERIFICATION

In this section, we propose a watermark verification mechanism based on the secret sharing mechanism [26] to improve the robustness of FedMark against false positives.

# A. Verification Method

We treat each participant’s embedding matrix $X _ { k }$ as his/her secret to share with other participants via Shamir’s Secret Sharing [26]. Each participant $p _ { k }$ generates $\mathbf { a } ~ t ~ ( t < K )$ order polynomial $f _ { k } ,$ , where coefficients are randomly generated and the constant term is $X _ { k }$ . Then for other $K - 1$ participants, $p _ { k }$ randomly generates $\{ x _ { j } \} _ { j \neq k }$ and sends $( x _ { j } , f _ { k } ( x _ { j } ) )$ to $p _ { j }$ . In this way, each secret $X _ { k }$ is split, and distributed to other $K - 1$ participants. Meantime, each participant receive $K - 1$ secret shares from other participants. By the property of secret sharing, secrets from any t participants can be used to reconstruct the polynomial $f _ { k } ( x )$ , and obtain the secret $X _ { k }$ by calculating $f _ { k } ( 0 )$ .

In the verification phase, when a participant $p _ { k }$ wants to prove his/her ownership, he/she needs to prove: (1) His/her embedding matrix $X _ { k }$ can be reconstructed by t participants; (2) The detection rate of the watermark extracted by $X _ { k }$ is above the threshold . He/she will pass the verification only if both conditions are met. This verification process can be carried out in a distributed manner by K participants, or coordinated by a trusted authority. The formal algorithm is shown in Algorithm 2.

# B. Security Analysis

First, sharing the embedding parameter $X _ { k }$ does not divulge any watermark information. Each participant does not share the watermark $b _ { k }$ , and other participants only obtain secret shares of $X _ { k }$ . Even if more than t curious participants collude and reconstruct $X _ { k }$ and calculate $s ( w { * } X )$ , they still do not know $B _ { k }$ (i.e., the actual embedding positions of $\boldsymbol { b } _ { k } )$ , nor can they infer $b _ { k } .$ . In detail, the number of possible embedding positions (i.e., parameters) is $\mid s ( w _ { k } * X _ { k } ) \mid$ |, while the number of actual embedding positions is N. There are $| s ( w _ { k } * X _ { k } ) | - N$ bits of $s ( w * X )$ that are either 0 or 1. Since X is generated by the normal distribution, we can assume that half of bits are 1. That is, there are N + |s(wk∗Xk)|−N = N+|s(wk∗Xk)| $\begin{array} { r } { \dot { N } + \frac { | s ( w _ { k } * X _ { k } ) | - N } { 2 } = \frac { N + | s ( w _ { k } * X _ { k } ) | } { 2 } } \end{array}$ 2 2 bits that are 1. Guessing the correct watermark positions is to choose the right N bits from N+|s(wk∗Xk)| bits. Taking $\frac { N + | s ( w _ { k } * X _ { k } ) | } { 2 }$ $| s ( w _ { k } * X _ { k } ) | = 2 5 6$ and $N = 2 0$ as an example, the probability is less than $\frac { 1 } { 1 0 ^ { 2 0 } }$ , which implies that it is almost impossible for other participants to guess the correct watermark information.

Algorithm 2: Secret Sharing-based Verification.   
Input: X is the embedding matrix to share.
/* take participant k as an example */
Preparation: Share Secret $X_{k}$ initialize $f(x) = a_{t-1}x^{t-1} + \ldots + a_{1}x + X_{k}$ for j = 0, 1, ..., K - 1 and $j \neq k$ do
    randomly generate $x_{j}$ send $(x_{j}, f(x_{j}))$ to participant $p_{j}$ end

Verification:
Step 1: prove the $X_{k}$ can be reconstructed
select t participants
initialize $f(x) = a_{t-1}x^{t-1} + \ldots + a_{2}x^{2} + a_{1}x + s$ for each participant j = 0, 1, ..., t - 1 do
    substitutes $(x_{j}, f(x_{j}))$ into $f(x)$ to obtain $a_{t-1}x_{j}^{t-1} + \ldots + a_{2}x_{j}^{2} + a_{1}x_{j} + s = f(x_{j})$ end
solve above t linear equations to obtain $f(x)$ if $X_{k} = f(0)$ then
    Step 1 verification success
end
Step 2: prove the watermark can be detected
Calculate the watermark detection rate d through Eq.(11)
if $d > \epsilon$ then
    Step 2 verification success
end
if both of the two steps are verified successfully then
    verification success
else
    verification failure
end

Second, the verification process is resistant to false positives. If an attacker leverages the false positives of Bloom Filter to forge X and b to steal the model ownership, he/she can not pass the first step of the verification. He/she can only attack successfully if he/she corrupts more than t participants, which greatly increases the cost and difficulty for the attack. In real systems, as long as the number of dishonest participants is less than t, the attacker still cannot pass the verification. Usually, when the majority of participants are semi-honest, we can set $\begin{array} { r } { t > \frac { K } { 2 } } \end{array}$ to achieve robust verification. Moreover, if an attacker uploads forged $( x , f ( x ) )$ to corrupt the verification of a valid participant $p _ { k }$ , he/she can be detected as a malicious party, since $p _ { k }$ knows all his/her own shared secret.

![](images/1ea99f389695df146bcf6ab48fd4ef4aa8bcd76337fc6a1157bb88bb8b277de4.jpg)



(a) AlexNet with CIFAR-10

![](images/bb9e199b6c60e2cab1dceac4d04da4c57b72472b2654e27adae664617f2398ad.jpg)



(b) ResNet18 with CIFAR-100   
Fig. 2. Capacity comparison between FedMark and FedIPR.

# VI. EXPERIMENTS

We conducted extensive experiments on various models to demonstrate the capacity, secrecy and robustness of FedMark. Although experiments are conducted on convolution neural networks, FedMark is applicable to other types of networks by omitting the step of calculating the mean of selected parameters over filters.

# A. Experiments Setup

In all experiments, we use SGD with cross-entropy loss for training. We set the learning rate to 0.1 for CIFAR-10, 0.01 for CIFAR-100 [27] and TinyImageNet [28], momentum to 0.9, local minibatch size to 16, local epoch to 2, length of watermark b to 256, and global epoch to 200. The parameter λ is set to 0.5 and the verification threshold  is set to 0.95. The training dataset are split equally to each participant for local training, while the test dataset are used to evaluate the accuracy of the global model. Experiments were conducted on a Linux Server with 4 Tesla P100 GPUs and implemented with PyTorch 1.5 using Python 3.7.

# B. Capacity Evaluation

We demonstrate that FedMark supports a large number of participants to successfully embed watermarks from the following aspects. Note that, the secret sharing-based verification method does not affect the watermark capacity.

Watermarking v.s. model performance. To show the applicability of FedMark to various FL systems, we implemented FedMark using seven of the most popular networks, including: AlexNet [29], ResNet18 [30] , VGG13 [31], MobileNetv2 [32], Inceptionv3 [33], DenseNet [34] and WideResNet [35]. In practical federated learning systems, simpler model structures tend to involve fewer participants, while more complex model structures tend to engage multiple participants. Consequently, we designed varying participant numbers for each model structure based on its complexity. For each network, we utilized CIFAR-10, CIFAR-100, and tiny-ImageNet datasets to train FL models with a substantial number of participants and assessed model accuracy both with and without embedding watermarks. Table I demonstrates that, across all these networks, FedMark successfully embeds a significant number (ranging from 30 to 150) of watermarks with a negligible impact (<1%) on model accuracy.

![](images/96f1babdd6f4cd212792666a646be0aec86c6b013ee19c1c53c1af195f5f2c33.jpg)



(a) AlexNet with CIFAR-10

![](images/c7eb2b77a2b3293a48434754850b8007f734a48abe378a80dea1101faa674b61.jpg)



(b) ResNet18 with CIFAR-100   
Fig. 3. Weights distribution with/without embedding watermarks.

Capacity compared with other methods. We embeded as many watermarks into the model as possible to measure the watermark capacity of FedMark and FedIPR [14](FedIPR is the only existing solution), and calculate the worst detection rate for all embedded watermarks, since a practical watermarking method should ensure that all participants’ watermarks are embedded and detectable. In Fig.2, the worst watermark detection of FedMark is always 100% in both two networks. Therefore, FedMark significantly outperform FedIPR by increasing the capacity from 12 to 150 for AlexNet, and from 36 to 150 for ResNet18. Theoretically, FedMark can successfully embed much more than 150 watermarks in these two networks. But when K exceeds 150, the size of X becomes very large and will takes up too much memory for many resource-limited devices; meanwhile the amount of training data allocated to each participant will be too small. Therefore, we did not try further for the case with more than 150 participants. The capacity of 150 is already sufficient for many FL systems.

Watermarks embedding position v.s. performance. We consider embedding watermarks into different positions of AlexNet trained by CIFAR-10 dataset and ResNet18 trained by CIFAR-100 dataset. When embedding into multi-convolution layers, we embeded watermarks into the first third, middle third and last third of the total convolution parameters of AlexNet and ResNet18, respectively. When embedding into a single convolution layer, we embeded watermarks into different layers of AlexNet and ResNet18. Table II shows that embedding positions have little impact on the model accuracy and no impact on the watermark detection rate. The worst watermark detection rate remains 100% in call cases.

Parameter choose v.s. performance We evaluated the effect of different values of hyperparameters on watermark embedding and model performance.

1) λ choose: first, we conducted an assessment of the impact of varying values of λ on watermark embedding, employing both AlexNet with CIFAR-10 and ResNet18 with CIFAR-100 datasets. The results of these evaluations are presented in Table III. When λ was set to small values, we found that watermarks failed to embed, $\mathbf { e . g . , \ } \lambda = 0 . 0 1 , 0 . 0 5$ in AlexNet and $\lambda ~ = ~ 0 . 0 1$ in ResNet18. However, as the value of λ increased, the successful embedding of watermarks become faster. Moreover, in all experiments, watermark embedding did not have a significant impact on model performance. Based on the empirical evidence derived from our experiments, we recommend setting λ to 0.5 or 1 during watermark embedding.

TABLE I   
MODEL ACCURACY(%) WITH (AND WITHOUT) EMBEDDING WATERMARKS. K IS THE NUMBER OF FL PARTICIPANTS. 

<table><tr><td rowspan="2">Dataset</td><td colspan="7">Accuracy with (without) embedding watermarks</td></tr><tr><td>AlexNet(K=30)</td><td>VGG13(K=50)</td><td>MobileNetv2(K=60)</td><td>ResNet18(K=80)</td><td>Inceptionv3(K=100)</td><td>DenseNet(K=120)</td><td>WideResnet(K=150)</td></tr><tr><td>CIFAR-10</td><td>87.97(88.31)</td><td>89.4(89.81)</td><td>90.25(90.21)</td><td>91.98(91.47)</td><td>90.22(90.38)</td><td>91.89(92.14)</td><td>93.23(93.14)</td></tr><tr><td>CIFAR-100</td><td>61.79(62.15)</td><td>64.31(64.87)</td><td>65.52(64.68)</td><td>72.98(73.11)</td><td>74.81(74.76)</td><td>73.12(73.58)</td><td>74.92(75.15)</td></tr><tr><td>TinyImageNet</td><td>39.82(40.02)</td><td>43.22(44.03)</td><td>50.33(50.21)</td><td>50.88(50.67)</td><td>51.72(51.92)</td><td>51.11(50.91)</td><td>52.66(52.42)</td></tr></table>

TABLE II MODEL ACCURACY (%) AND WORST WATERMARK DETECTION RATE FOR DIFFERENT EMBEDDING POSITIONS. 

<table><tr><td colspan="7">(a)Accuracy(%)</td></tr><tr><td rowspan="3">Network</td><td colspan="6">Embedding position</td></tr><tr><td colspan="3">multi-convolution layers</td><td colspan="3">a single convolution layer</td></tr><tr><td>First 1/3</td><td>Middle 1/3</td><td>Last 1/3</td><td>conv 2/conv 5</td><td>conv 3/conv 7</td><td>conv 4/conv 9</td></tr><tr><td>AlexNet</td><td>85.24</td><td>84.98</td><td>86.07</td><td>85.63</td><td>85.45</td><td>85.22</td></tr><tr><td>ResNet18</td><td>69.06</td><td>68.89</td><td>69.13</td><td>68.93</td><td>68.76</td><td>69.17</td></tr><tr><td colspan="7">(b)Worst watermark detection rate(%)</td></tr><tr><td rowspan="3">Network</td><td colspan="6">Embedding position</td></tr><tr><td colspan="3">multi-convolution layers</td><td colspan="3">a single convolution layer</td></tr><tr><td>First 1/3</td><td>Middle 1/3</td><td>Last 1/3</td><td>conv 2/conv 5</td><td>conv 3/conv 7</td><td>conv 4/conv 9</td></tr><tr><td>AlexNet</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr><tr><td>ResNet18</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr></table>

TABLE III EFFECT OF DIFFERENT VALUES OF λ ON WATERMARK EMBEDDING.   
(a) AlexNet with CIFAR-10 

<table><tr><td> $\lambda$ </td><td>0.01</td><td>0.05</td><td>0.1</td><td>0.5</td><td>1</td></tr><tr><td>Epochs</td><td>fail</td><td>fail</td><td>141</td><td>76</td><td>44</td></tr><tr><td colspan="6">(b) ResNet with CIFAR-100</td></tr><tr><td> $\lambda$ </td><td>0.01</td><td>0.05</td><td>0.1</td><td>0.5</td><td>1</td></tr><tr><td>Epochs</td><td>fail</td><td>134</td><td>107</td><td>65</td><td>41</td></tr></table>

2) M choose: second, we proceeded to evaluate the influence of varying values of M on watermark embedding, employing both AlexNet with CIFAR-10 and ResNet18 with CIFAR-100 datasets. The results of these assessments are presented in Table IV. As we discussed in Sec.3, when M was set to small values, such as M = 1000, 1500 in AlexNet, watermarks failed to embed. However, as the value of M increased, the successful embedding of watermarks become faster. Moreover, in all experiments, watermark embedding did not have a significant impact on model performance. Based on the empirical insights from our experiments, we recommend establishing a minimum threshold of M at 2000 during the watermark embedding process.

Model scale v.s. performance We evaluated the effect of different model scale on watermark embedding using two dataset: CIFAR-10 and CIFAR-100, three model structures: AlexNet, VGG13, ResNet18. This evaluation involved 50 participants. When using CIFAR-10, watermarks detection rates of AlexNet, VGG13, ResNet18 achieve to 100% using 141,128 and 92 epochs respectively. And when using CIFAR-100, watermarks detection rates of AlexNet, VGG13, ResNet18 achieve to 100% using 160, 145 and 107 epochs respectively. Therefore, the larger the size of the model, the faster the watermarks can be successfully embedded.

TABLE IV EFFECT OF DIFFERENT VALUES OF M ON WATERMARK EMBEDDING.   
(a) AlexNet with CIFAR-10 

<table><tr><td>M</td><td>1000</td><td>1500</td><td>2000</td><td>2500</td><td>3000</td></tr><tr><td>Epochs</td><td>fail</td><td>fail</td><td>141</td><td>112</td><td>78</td></tr><tr><td colspan="6">(b) ResNet with CIFAR-100</td></tr><tr><td>M</td><td>1000</td><td>1500</td><td>2000</td><td>2500</td><td>3000</td></tr><tr><td>Epochs</td><td>156</td><td>127</td><td>107</td><td>62</td><td>35</td></tr></table>

# C. Secrecy Evaluation

Our analyses in Section IV-C and Section V-B have shown that FedMark can protect watermark information well. Here we further prove this by experiments. We compute the statistical characteristics of AlexNet with CIFAR-10 and ResNet18 with CIFAR-100, respectively, with and without embedding watermarks. Fig.3 shows that the distributions of model parameters are the same with and without embedding watermarks. Hence, it presents a considerable challenge for both curious and malicious parties to distinguish whether a model is embedded with watermarks, and even more difficult to infer the precise positions of watermarks.

# D. Robustness

We show that FedMark is robust to different settings in real FL systems, as well as to various attacks.

Robust to non-iid data. In real FL systems, it is common for participants’ datasets to exhibit non-iid distribution. To assess the performance of FedMark under such conditions, we conducted experiments by shuffling all the data and randomly allocating varying amounts of data to 50 participants to achieve non-iid data distribution. Specifically, we compute the watermark detection rate and the model accuracy using AlexNet trained by CIFAR-10 dataset and ResNet18 trained by CIFAR-100 dataset under non-iid data distribution. Table V is the results. For participants with only 1%-2% of the training data, the watermark detection rate falls below 100%, yet remains notably high at greater than 97.14%. Conversely, when participants possess more than 2% of the training data, the watermark detection rate consistently achieves 100%. Thus, FedMark demonstrates robustness in scenarios where the training data exhibits non-iid distribution.

Robust to different participant selection rate. In FL systems, the server typically employs a random selection process, choosing a fixed percentage of participants in each round [36]. Taking 50 participants as an example, Fig.4 depicts the watermark detection rate at various participant selection rates. For AlexNet, when the selection rate falls below 0.5, the watermark detection rate experiences a slight decrease. This phenomenon can be attributed to the simple structure of AlexNet and the limited training epochs each participant undergoes. However, in all other instances, the watermark detection rate for both AlexNet and ResNet consistently reaches 100%. These results underscore the efficacy of FedMark in maintaining effectiveness across diverse participant selection rates.

![](images/9309931281b631dbb100a0132000becc8200029da1d0e909d9f9e63fe6754868.jpg)



(a) CIFAR-10

![](images/897e3809528609bc023a326dd99e13fcb7af2004a961962e9fc208c499857df3.jpg)



(b) CIFAR-100   
Fig. 4. Watermark detection rate against different participant selection rates.

TABLE V WATERMARK DETECTION RATE AND MODEL ACCURACY WHEN TRAINING DATA IS NON-IID DISTRIBUTED.   
(a)Watermark Detection Rate(%) 

<table><tr><td rowspan="2">Network</td><td colspan="6">Participant with different percentages of training data</td></tr><tr><td>1%</td><td>2%</td><td>5%</td><td>10%</td><td>20%</td><td>40%</td></tr><tr><td>AlexNet</td><td>97.14</td><td>99.58</td><td>100</td><td>100</td><td>100</td><td>100</td></tr><tr><td>ResNet18</td><td>99.12</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr><tr><td colspan="7">(b)Accuracy(%)</td></tr><tr><td>AlexNet</td><td>86.11</td><td>86.26</td><td>85.72</td><td>85.44</td><td>86.02</td><td>86.44</td></tr><tr><td>ResNet18</td><td>68.78</td><td>68.25</td><td>69.19</td><td>68.79</td><td>69.12</td><td>69.04</td></tr></table>

Robust to model fine-tuning. We assess the impact of model fine-tuning on both the model performance and watermark detection rate. For each network, we conduct training for 200 epochs, incorporating the watermark embedding loss. Subsequently, we fine-tune the network for an additional 50 epochs without the watermark embedding loss. Here, since the watermark embedding position is private, the fine-tuning strategy we take is to fine-tune all layers of the model. The results in Table VI demonstrate that the watermark detection rate consistently remains at 100% after fine-tuning. These experimental findings reveal that, after fine-tuning, the watermark detection rate maintains at 100% for both AlexNet with CIFAR-10 and ResNet18 with CIFAR-100. Consequently, FedMark exhibits robustness in the face of model fine-tuning.

Robust to model pruning. Pruning [37] is a usual way to address model redundancy. We prune AlexNet trained by CIFAR-10 dataset and ResNet18 trained by CIFAR-100 dataset with watermarks and measure the watermarks detection rates. Fig.5 shows that even after pruning about 90% of model parameters, the embedded watermarks are still detectable. Therefore, FedMark is robust against pruning.

Robust to permutation attacks. An attacker may change the convolution filters’ order to affect the order of the model parameters to make the valid watermarks undetectable. In FedMark, w in Eq.(8) is not affected by changing the filters’ order, because w is obtained by taking the average value of the number of filters after selecting the convolution layers’ parameters. That is, our mechanism is robust to permutation attacks.

![](images/7894606362c458d3b6b650722995066c58ac5da93a5e846c3379e370eb4297e1.jpg)



(a) AlexNet with CIFAR-10

![](images/936cf610eeb390270d645071215713afd091957f999ca6032983f560643fbc07.jpg)



(b) ResNet18 with CIFAR-100   
Fig. 5. Model accuracy and watermark detection rates for different pruning rates.

TABLE VI MODEL ACCURACY(%) AND WORST WATERMARK DETECTION RATES(%) BEFORE AND AFTER FINE-TUNING. THERE ARE 50 PARTICIPANTS.   
(a) AlexNet with CIFAR-10 

<table><tr><td></td><td>Accuracy(%)</td><td>Detection Rate(%)</td></tr><tr><td>Normal</td><td>85.42</td><td>N/A</td></tr><tr><td>Embedded</td><td>85.89</td><td>100</td></tr><tr><td>Fine-tuning</td><td>85.61</td><td>100</td></tr><tr><td colspan="3">(b) ResNet18 in CIFAR-100</td></tr><tr><td>Normal</td><td>78.05</td><td>N/A</td></tr><tr><td>Embedded</td><td>77.72</td><td>100</td></tr><tr><td>Fine-tuning</td><td>77.52</td><td>100</td></tr></table>

Robust to scaling attacks. An attacker may multiply the weights of the edges entering a neuron by a factor $\phi > 0$ and multiply all the edges going out from this neuron by $\frac { 1 } { \phi }$ to make the watermark undetectable. When the weights are multiplied or divided by a factor $\phi > 0 .$ , the signs of parameters will not change, and the watermark detection rates Eq.(11) will not change either. Therefore, FedMark is robust against scaling attacks.

Robust to forging attacks According to the analysis in Sec.V-B, after adopting the secret sharing-based verification method, FedMark is robust against forging attacks. Even if some malicious participants are willing to help the attacker, as long as we take $t ~ > ~ \frac { K } { 2 }$ , such an attack cannot succeed if majority participants are semi-honest, which provides sufficient security for participants’ IP.

# VII. CONCLUSION AND FEATURE WORK

In this work, we analyze why applying watermarking method in centralized scenarios directly to FL models suffers from limited capacity. We propose FedMark, a watermarking mechanism for a large-number of participants in horizontal FL. In addition, we improve the robustness of our mechanism by a secret sharing-based verification method. Our comprehensive experiments show that FedMark provides a practical watermarking solution for real FL systems.

We leave the following challenging issues as our future work. First, the model watermarking method is not robust to model distillation, which means that the attacker can remove the watermark by data-free distillation [38]. Moreover, the proposed mechanism is not suitable for vertical FL models, which still needs to explore. Next, the size of embedding matrix X for each participant is $M \ast T$ , which means that when the number of participants becomes large, X will increasingly be very large, taking up too much memory. In addition, the participants are malicious in practical, rather than assuming that the participants are semi-honest as in this paper. In this case, A malicious participant will infer the watermarking information of other participants through multiple rounds of model parameters, and influence the watermark embedding of other participants by saturating the Bloom Filter during the local training phase.

# ACKNOWLEDGMENT

The research is partially supported by National Key R&D Program of China under Grant No. 2021ZD0110400, 2021YFB2900103, Innovation Program for Quantum Science and Technology 2021ZD0302900 and China National Natural Science Foundation with No. 62132018, 62231015, 61932016, ”Pioneer” and ”Leading Goose” R&D Program of Zhejiang”, 2023C01029, and 2023C01143, ”the Fundamental Research Funds for the Central Universities” WK2150110024.

# REFERENCES

[1] Y. Uchida, Y. Nagai, S. Sakazawa, and S. Satoh, “Embedding watermarks into deep neural networks,” in Proceedings of the ACM on International Conference on Multimedia Retrieval. ACM, 2017, pp. 269–277.   
[2] Y. Adi, C. Baum, M. Cisse, B. Pinkas, and J. Keshet, “Turning your weakness into a strength: Watermarking deep neural networks by backdooring,” in 27th USENIX Security Symposium (USENIX Security 18), 2018, pp. 1615–1631.   
[3] L. Fan, K. W. Ng, and C. S. Chan, “Rethinking deep neural network ownership verification: embedding passports to defeat ambiguity attacks,” in Proceedings of the 33rd International Conference on Neural Information Processing Systems, 2019, pp. 4714–4723.   
[4] H. Jia, C. A. Choquette-Choo, V. Chandrasekaran, and N. Papernot, “Entangled watermarks as a defense against model extraction,” in 30th USENIX Security Symposium (USENIX Security 21), 2021, pp. 1937– 1954.   
[5] L. Fan, K. W. Ng, C. S. Chan, and Q. Yang, “Deepip: Deep neural network intellectual property protection with passports,” IEEE Transactions on Pattern Analysis & Machine Intelligence, 2021.   
[6] T. Wang and F. Kerschbaum, “RIGA: covert and robust white-box watermarking of deep neural networks,” in WWW ’21: The Web Conference 2021, Virtual Event / Ljubljana, Slovenia, April 19-23, 2021, J. Leskovec, M. Grobelnik, M. Najork, J. Tang, and L. Zia, Eds. ACM / IW3C2, 2021, pp. 993–1004.   
[7] F. Li, S. Wang, and Y. Zhu, “Fostering the robustness of white-box deep neural network watermarks by neuron alignment,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2022, Virtual and Singapore, 23-27 May 2022. IEEE, 2022, pp. 3049–3053.   
[8] A. Bansal, P. Chiang, M. J. Curry, R. Jain, C. Wigington, V. Manjunatha, J. P. Dickerson, and T. Goldstein, “Certified neural network watermarks with randomized smoothing,” in International Conference on Machine Learning, ICML 2022, 17-23 July 2022, Baltimore, Maryland, USA, ser. Proceedings of Machine Learning Research, vol. 162. PMLR, 2022, pp. 1450–1465.   
[9] P. Lv, P. Li, S. Zhang, K. Chen, R. Liang, H. Ma, Y. Zhao, and Y. Li, “A robustness-assured white-box watermark in neural networks,” IEEE Trans. Dependable Secur. Comput., vol. 20, no. 6, pp. 5214–5229, 2023.

[10] Y. Lao, P. Yang, W. Zhao, and P. Li, “Identification for deep neural network: Simply adjusting few weights!” in 38th IEEE International Conference on Data Engineering, ICDE 2022, Kuala Lumpur, Malaysia, May 9-12, 2022. IEEE, 2022, pp. 1328–1341. [Online]. Available: https://doi.org/10.1109/ICDE53745.2022.00104   
[11] S. Lee, W. Song, S. Jana, M. Cha, and S. Son, “Evaluating the robustness of trigger set-based watermarks embedded in deep neural networks,” IEEE Trans. Dependable Secur. Comput., vol. 20, no. 4, pp. 3434–3448, 2023.   
[12] J. Konecnˇ y, H. B. McMahan, F. X. Yu, P. Richt \` arik, A. T. Suresh, and ´ D. Bacon, “Federated learning: Strategies for improving communication efficiency,” CoRR, vol. abs/1610.05492, 2016.   
[13] Y. Li, H. Wang, and M. Barni, “A survey of deep neural network watermarking techniques,” Neurocomputing, vol. 461, pp. 171–193, 2021.   
[14] B. Li, L. Fan, H. Gu, J. Li, and Q. Yang, “Fedipr: Ownership verification for federated deep neural network models,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 45, no. 4, pp. 4521– 4536, 2022.   
[15] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” ACM Transactions on Intelligent Systems and Technology (TIST), vol. 10, no. 2, pp. 1–19, 2019.   
[16] J. Zhang, D. Chen, J. Liao, W. Zhang, G. Hua, and N. Yu, “Passportaware normalization for deep model protection,” Advances in Neural Information Processing Systems, vol. 33, pp. 22 619–22 628, 2020.   
[17] H. Liu, Z. Weng, and Y. Zhu, “Watermarking deep neural networks with greedy residuals,” in International Conference on Machine Learning. PMLR, 2021, pp. 6978–6988.   
[18] S. Lee, W. Song, S. Jana, M. Cha, and S. Son, “Evaluating the robustness of trigger set-based watermarks embedded in deep neural networks,” IEEE Transactions on Dependable and Secure Computing, 2022.   
[19] B. G. Atli, Y. Xia, S. Marchal, and N. Asokan, “Waffle: Watermarking in federated learning,” in 40th International Symposium on Reliable Distributed Systems, SRDS 2021, Chicago, IL, USA, September 20-23, 2021. IEEE, 2021, pp. 310–320.   
[20] F.-Q. Li, S.-L. Wang, and A. W.-C. Liew, “Towards practical watermark for deep neural networks in federated learning,” CoRR, vol. abs/2105.03167, 2021.   
[21] E. Le Merrer, P. Perez, and G. Tredan, “Adversarial frontier stitching ´ for remote neural network watermarking,” Neural Computing and Applications, vol. 32, no. 13, pp. 9233–9244, 2020.   
[22] M. Artin, Algebra. Pearson Prentice Hall, 2011. [Online]. Available: https://books.google.com/books?id=S6GSAgAAQBAJ   
[23] V. Mothukuri, R. M. Parizi, S. Pouriyeh, Y. Huang, A. Dehghantanha, and G. Srivastava, “A survey on security and privacy of federated learning,” Future Generation Computer Systems, vol. 115, pp. 619–640, 2021.   
[24] B. H. Bloom, “Space/time trade-offs in hash coding with allowable errors,” Communications of the ACM, vol. 13, no. 7, pp. 422–426, 1970.   
[25] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial intelligence and statistics. PMLR, 2017, pp. 1273– 1282.   
[26] A. Shamir, “How to share a secret,” Communications of the ACM, vol. 22, no. 11, pp. 612–613, 1979.   
[27] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” University of Toronto, 2009.   
[28] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, “Imagenet: A large-scale hierarchical image database,” in 2009 IEEE conference on computer vision and pattern recognition. Ieee, 2009, pp. 248–255.   
[29] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification with deep convolutional neural networks,” Advances in neural information processing systems, vol. 25, pp. 1097–1105, 2012.   
[30] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition. IEEE Computer Society, 2016, pp. 770–778.   
[31] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” in 3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings, 2015.   
[32] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, “Mobilenetv2: Inverted residuals and linear bottlenecks,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2018, pp. 4510–4520.

[33] C. Szegedy, V. Vanhoucke, S. Ioffe, J. Shlens, and Z. Wojna, “Rethinking the inception architecture for computer vision,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 2818–2826.   
[34] G. Huang, Z. Liu, L. van der Maaten, and K. Q. Weinberger, “Densely connected convolutional networks,” in 2017 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2017, Honolulu, HI, USA, July 21-26, 2017. IEEE Computer Society, 2017, pp. 2261–2269.   
[35] S. Zagoruyko and N. Komodakis, “Wide residual networks,” in Proceedings of the British Machine Vision Conference 2016, BMVC 2016, York, UK, September 19-22, 2016. BMVA Press, 2016.   
[36] B. Luo, W. Xiao, S. Wang, J. Huang, and L. Tassiulas, “Tackling system and statistical heterogeneity for federated learning with adaptive client sampling,” in IEEE Conference on Computer Communications, 2022, pp. 1739–1748.   
[37] A. See, M.-T. Luong, and C. D. Manning, “Compression of neural machine translation models via pruning,” in Proceedings of the 20th SIGNLL Conference on Computational Natural Language Learning, CoNLL 2016, Berlin, Germany, August 11-12, 2016. ACL, 2016, pp. 291–301.   
[38] G. Fang, J. Song, C. Shen, X. Wang, D. Chen, and M. Song, “Data-free adversarial distillation,” CoRR, vol. abs/1912.11006, 2019.