# Toward Accurate and Efficient Model Integrity Verification against Dishonest Servers

CHEN TANG, University of Science and Technology of China, China

LAN ZHANG∗, University of Science and Technology of China, China and Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, China

XIRONG ZHUANG, University of Science and Technology of China, China

JUNYANG ZHANG, University of Science and Technology of China, China

XIAOJING YU, University of Science and Technology of China, China

XIANG-YANG LI, University of Science and Technology of China, China

With the rapid advancement of machine learning, deploying high-performance models for commercial AI services has become increasingly prevalent. However, dishonest servers may compromise these models by embedding backdoors or replacing them with low-precision versions, leading to degraded service quality and security risks. To address this, model integrity verification methods have emerged to detect such tampering. Yet, existing approaches often suffer from high false positive rates and significant computational overhead. This paper explores the impact of tampering on model decision boundaries, revealing that such attacks cause varying degrees of boundary shifts. We then define the sensitivity of decision boundaries and identify that samples near highly sensitive decision boundaries are especially effective for integrity verification. Based on this insight, we propose a novel verification method that leverages boundary shift magnitude to generate targeted verification samples. To further improve efficiency, we introduce an adaptive filtering mechanism that removes redundant samples without compromising detection accuracy. Extensive experiments demonstrate that our method detects various types of tampering—including fine-tuning, pruning, and backdoor injection—with 100% accuracy using only four verification samples across three models. Moreover, the method remains robust even when the verification strategy is known to the server.

CCS Concepts: • Security and privacy → Authorization; Authentication; Digital rights management; • Computing methodologies → Artificial intelligence.

Additional Key Words and Phrases: Model Copyright Protection, Model Integrity Verification, Model Decision Boundary Visualization

# ACM Reference Format:

Chen Tang, Lan Zhang, Xirong Zhuang, Junyang Zhang, Xiaojing Yu, and Xiang-Yang Li. 2026. Toward Accurate and Efficient Model Integrity Verification against Dishonest Servers. 1, 1 (March 2026), 18 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

∗Corresponding author.

Authors’ Contact Information: Chen Tang, University of Science and Technology of China, Hefei, Anhui Shi, China, chentang1999@mail.ustc.edu.cn; Lan Zhang, University of Science and Technology of China, Hefei, Anhui Shi, China and Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, Hefei, Anhui Shi, China, zhanglan@ustc.edu.cn; Xirong Zhuang, University of Science and Technology of China, Hefei, Anhui Shi, China, xirongz@mail.ustc.edu.cn; Junyang Zhang, University of Science and Technology of China, Hefei, Anhui Shi, China, zhangjunyang@mail.ustc.edu.cn; Xiaojing Yu, University of Science and Technology of China, Hefei, Anhui Shi, China; Xiang-Yang Li, University of Science and Technology of China, Hefei, Anhui Shi, China, xiangyangli@ustc.edu.cn.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

© 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.

Manuscript submitted to ACM

# 1 Introduction

Deep learning techniques have advanced rapidly in recent years, leading to significant achievements in various fields, such as image recognition and natural language processing. Many IT corporations now offer cloud-based or edge-based services for deep learning model deployment, commonly called Machine Learning as a Service (MLaaS) [5, 12, 22], to facilitate the automatic and convenient use of well-trained models. For instance, platforms like Google Cloud ML Engine [1], Microsoft Azure [2], and Amazon SageMaker [3] allow customers to customize their models to deploy them online or offline. Given the enormous potential of cloud-enabled MLaaS to transform the deployment of deep learning models, an increasing number of users opt to deploy their models in the cloud or edge, generating revenue by offering AI services.

A common assumption in existing research is that the deployment environment, whether in the cloud or on edge devices, is inherently trustworthy. However, this assumption does not hold in many real-world scenarios, where models are often deployed in untrusted environments, thereby exposing them to potential risks and security threats. Servers cannot guarantee the quality of model deployment services, and dishonest servers may illegally alter models through Trojan attacks[21] or backdoor attacks[7], or even replace them with poorer-performing models to save computational resources and storage, as shown in Fig.1. When a model is deployed either in the cloud—where the model owner typically has only black-box query access—or on edge devices—where the same model may be deployed to a vast number of devices—accurately and efficiently verifying whether the deployed model has been tampered with becomes particularly challenging.

Several studies [4, 13, 17, 18, 20, 25–27] have explored methods to verify the integrity of deployed models. The core intuition underlying these methods is that tampering with a model typically leads to shifts in its decision boundaries, which in turn alter the model’s predictions for inputs located near those boundaries. Accordingly, these approaches aim to generate verification samples that lie close to the decision boundary. During the integrity verification process, these samples are queried from the deployed model. If the resulting predictions deviate from the expected outputs, it provides evidence that the model may have been tampered with. A key advantage of this approach is that it allows the integrity of the deployed model to be verified using pre-generated verification samples, thereby avoiding the need for white-box access to the model. Although existing methods continuously optimize the design of verification samples to ensure they are as close as possible to the decision boundaries, there remains an inherent limitation at the design level: the direction and magnitude of decision boundary shifts are not fixed. This unpredictability leads to the occurrence of false positives in the integrity verification process. Specifically, if the decision boundary does not shift toward the region where verification samples lie, or if the extent of the shift is insufficient to cross those samples, the model’s outputs on these samples will remain unchanged, leading to verification failure. Furthermore, these methods require additional time for fine-tuning the model with verification samples or training a separate model to generate them, which further restricts their generalizability.

Fortunately, using decision boundary visualization techniques [24], we have observed the existence of sensitive decision boundaries. Here, sensitivity refers to the degree to which a model’s decision boundary shifts in response to tampering. A sensitive decision boundary exhibits significant and consistent shifts under various types of tampering, making it particularly suitable for integrity verification. Therefore, to address the limitations of existing approaches and achieve accurate and efficient integrity verification, the key lies in identifying these sensitive decision boundaries and generating verification samples near them. Achieving this goal is non-trivial and presents two key challenges: (1) It is difficult to identify sensitive decision boundaries and generate verification samples near them. First, there is also a lack of appropriate metrics to measure the sensitivity of decision boundaries. Second, high-dimensional decision spaces contain many decision boundaries, making identifying sensitive boundaries difficult. Finally, the diversity and complexity of models make it difficult to design a generalized solution. (2) Reducing redundant verification samples to achieve efficient verification is equally challenging. Even if sensitive decision boundaries are successfully identified, generated verification samples can lead to redundancy. For instance, verification samples generated near the same decision boundary are redundant because they have identical effects on integrity verification. However, there is no method that takes into account the avoidance of redundant verification samples in integrity verification, which leads to extra computational overhead.

![](images/16e1be80a8940a284d82df6e7d8c2dfa1d24eb59cc8519974fc5d51c1b233f39.jpg)



Fig. 1. Integrity Verification Workflow.

To address the aforementioned challenges, we first employ decision boundary visualization techniques to systematically analyze the impact of model tampering on decision boundaries. Through this analysis, we observe that certain decision boundaries consistently exhibit significant shifts under various types and degrees of tampering. We refer to these as sensitive decision boundaries, and we define their sensitivity in terms of the magnitude of the boundary shift induced by tampering. Building on this insight, we propose a novel integrity verification method that is both accurate and efficient. Our approach identifies sensitive decision boundaries by quantifying their shift magnitude following tampering, using this metric to localize regions of highest sensitivity. Verification samples are then generated in the vicinity of these regions. Due to their proximity to highly sensitive boundaries, these samples are particularly responsive to even subtle forms of tampering, thereby enabling accurate integrity verification. To further improve verification efficiency, we design an adaptive filtering technique that eliminates redundant verification samples based on the distances between them. This approach ensures that each retained verification sample contributes uniquely and effectively to the integrity verification process, thereby maximizing both accuracy and computational efficiency. In addition, each verification sample is generated from a combination of three arbitrary data points. This design enables the pre-generation of a large set of unique verification samples, which can be made publicly available. As a result, any model user can perform on-demand integrity verification of the deployed model without requiring internal access, as illustrated in Fig.1.

In summary, our main contributions are three-fold:

(1) We explore the impact of model tampering on decision boundaries by visualizing these boundaries and observing that different regions exhibit varying degrees of sensitivity to tampering. Unlike previous works that focus on generating verification samples near decision boundaries, our approach emphasizes identifying and selecting

Manuscript submitted to ACM

sensitive decision boundaries—the regions most responsive to tampering. We demonstrate that targeting these sensitive areas is critical for accurate and reliable integrity verification.

(2) We design an integrity verification method that not only leverages the magnitude of decision boundary shifts to enhance verification accuracy but also ensures each verification sample is unique and indispensable. Our approach generates a large set of distinct verification samples, which can be made publicly available for any model user. This allows for on-demand integrity verification without requiring internal access to the deployed model, ensuring that users can perform real-time, reliable checks on the model’s integrity.   
(3) Experiments demonstrate that our method achieves 100% accuracy in integrity verification for tampered models, including those subjected to fine-tuning, pruning, or poisoning, using only 4 verification samples across three different model structures and datasets. Moreover, even if the server is aware of the integrity verification method and the publicly available verification samples, our analysis and experiments show that our scheme is robust to observation, noise addition, and adaptive attack strategies.

# 2 Related Work and Preliminary

In this section, we present existing works on integrity verification and point out their shortcomings. We then present decision boundary visualization techniques for exploring model decision boundaries to understand our design better.

# 2.1 Model Integrity Verification

Since 2018, various efforts have been designed to verify whether models deployed in the cloud have been tampered with, a process known as model integrity verification.

Trigger-based methods [4, 13, 17, 20] represent the earliest form of model integrity verification. These approaches embed special backdoor triggers into the model during training. After deployment, the presence of the expected backdoor behavior serves as an indicator of the model’s integrity.

More recent efforts have shifted toward boundary-based verification methods, which are grounded in the observation that model tampering typically causes shifts in decision boundaries. One of the early examples is [11], which formulates the construction of verification samples as an optimization problem and uses Taylor expansion techniques to generate them. Building on this, subsequent works [26, 27] fine-tune the model with specially crafted samples prior to deployment, ensuring that the verification samples lie close to decision boundaries and are thus more sensitive to tampering. To further improve the proximity of verification samples to decision boundaries, [18] proposed generating samples along the gradient direction of input data, aiming to approximate the normal vector of the boundary surface. In another approach, [25] suggested encoding inputs into a latent space and applying perturbations to generate verification samples near decision boundaries more effectively.

# 2.2 Decision Boundary Visualization

In fact, related works suffer from an obvious shortcoming: the inability to predict in advance the direction in which the decision boundary is shifted after the model is tampered with, makes it inevitable to generate false positives. An intuitive solution is to visualize the model decision boundary to find the shift pattern of the decision boundary after the model has been tampered with, and generate verification samples close to the shift direction based on this shift pattern.

In recent years, several works have explored the visualization of classification model decision boundaries[6, 10, 14, 24]. Somepalli et al.[24] propose to capture on-manifold model behavior to visualize decision boundaries. In their design, they first select a triplet $( x _ { 1 } , x _ { 2 } , x _ { 3 } ) \sim { \bf D } ^ { 3 }$ of i.i.d. images from the distribution D. Then they construct two vectors Manuscript submitted to ACM

$\upsilon _ { 1 } = x _ { 2 } - x _ { 1 } , \upsilon _ { 2 } = x _ { 3 } - x _ { 1 }$ , and generate an orthogonal coordinate system based on two vectors, which is $( v _ { 1 } , v _ { 2 } - p r o j _ { v _ { 1 } } v _ { 2 } )$ . Then they sample inputs using the following formula:

$$
\alpha \cdot \max (\boldsymbol {v} _ {1} \cdot \boldsymbol {v} _ {1}, | p r o j _ {\boldsymbol {v} _ {1}} \boldsymbol {v} _ {2} \cdot \boldsymbol {v} _ {1} |) \boldsymbol {v} _ {1} + \beta (\boldsymbol {v} _ {2} - p r o j _ {\boldsymbol {v} _ {1}} \boldsymbol {v} _ {2}) \tag {1}
$$

where $- 0 . 1 \leq \alpha , \beta \leq 1 . 1$ and sampled points are generated one by one along the direction of the horizontal coordinate. Finally, they draw decision boundaries based on the model’s outputs for these sampled inputs. In this way, the decision plane where the triplet $\left( x _ { 1 } , x _ { 2 } , x _ { 3 } \right)$ is located is visualized.

Utilizing the decision boundary visualization technique, we conducted an in-depth exploration of integrity verification based on the visualization results and designed an accurate and efficient integrity verification method, which is described below.

# 3 Problem Statement and Threat Model

# 3.1 Problem Statement

We consider a setting in which a model owner ?? trains an image classification model ?? and deploys it to a cloud or edge platform managed by a potentially untrusted service provider ??. The deployed model is denoted as ??′. Due to the lack of control over the deployment environment, ?? cannot guarantee that ??′ remains identical to the original model ?? after deployment.

The adversarial server ?? may tamper with the model ?? in the following ways: (1) embedding backdoors to enable targeted misclassification or other malicious behavior, or (2) replacing the model with a degraded version (e.g., a quantized or pruned model) to reduce computational or storage costs, while attempting to evade detection.

To counter such threats, the model owner ?? performs an integrity verification procedure to determine whether the deployed model ??′ has been altered. As ?? only has black-box access to ??′, the verification is performed solely based on input-output queries. Prior to deployment, ?? generates a set of verification samples $\mathcal { V } = \{ x _ { i } \} _ { i = 1 } ^ { N }$ 1 using a dataset ??, which may originate from the training set, the test set, or any task-relevant data. The expected predictions of these samples are denoted as $P _ { e } = \{ y _ { i } \} _ { i = 1 } ^ { N }$ , produced by the original model ??.

Integrity verification is conducted in two steps:

• Step 1: Verification Sample Generation. Given the model ?? and a dataset ??, the model owner generates a set of verification samples V along with their expected predictions $P _ { e }$ .   
• Step 2: Black-box Integrity Verification. After model deployment, the model owner queries the deployed model ??′ with V, collects the returned predictions $P _ { m } .$ , and compares them with $P _ { e }$ .

Decision Rule: I $: P _ { m } = P _ { e }$ , the integrity verification passes, indicating the model has not been tampered with. Otherwise, if $P _ { m } \neq P _ { e }$ , the model is considered compromised.

To ensure practical applicability, an integrity verification method should satisfy the following requirements:

(1) Accuracy: The method must reliably detect any tampering of the deployed model;   
(2) Efficiency: The overhead of generating verification samples and performing verification should be minimal;   
(3) Sparsity: A small number of verification samples should suffice for successful verification;   
(4) Instantaneity: Verification should be feasible at any time after deployment;   
(5) Robustness: The method should be resistant to evasion techniques or countermeasures employed by a malicious server.

# 3.2 Threat Model

We assume the server ??, which hosts the deployed model ??′, is malicious and may actively attempt to modify the model. The adversary’s objectives include (but are not limited to):

• Injecting backdoors into the model to cause malicious or unintended predictions on specific inputs;   
• Substituting the original model with a computationally cheaper (e.g., low-precision) variant to save costs, while maintaining similar behavior on general queries to avoid detection.

We consider a strong adversarial model in which the attacker has the following capabilities:

• Verification Awareness: The attacker is aware of the integrity verification framework, including the methodology and process;   
• Sample Knowledge: The verification samples V are assumed to be publicly known or observable by the adversary;   
• Evasion Strategies: The attacker may attempt to adaptively modify the tampered model to maintain correct outputs on V, thereby evading detection.

The model owner ?? is honest but has only black-box access to the deployed model ??′, meaning the owner can only observe outputs to submitted queries without access to internal model parameters, gradients, or architecture. The owner aims to determine whether ??′ has been altered by comparing the outputs $P _ { m }$ with the pre-computed labels $P _ { e } .$

# 4 Explore Integrity Verification

In this section, we utilize the decision boundary visualization method [24] to analyze the deficiencies of the existing efforts and summarize the patterns of the decision boundaries’ shift.

# 4.1 Decision Boundaries Visualization

Current methods are grounded in the intuition of generating verification samples near the decision boundary. When the model is tampered with, the decision boundary shifts, causing the model’s outputs for these verification samples to change, thereby indicating that the model has been tampered with. We leverage the decision boundary visualization technique as a tool to visualize the differences in model decision boundaries before and after tampering. This allows us to identify the deficiencies of existing methods and explore how to design an integrity verification method that overcomes the limitations of current methods.

Specifically, we used three datasets: MNIST [19], CIFAR-10 and CIFAR-100 [15], three model structures: AlexNet [16], VGG16 [23] and ResNet34 [9]. We trained two sets of models and visualized their decision boundaries. Each set of models comprised four models: the source model, the fine-tuned model (fine-tuning for 50 epochs), the pruned model (with 40% of the source model’s parameters pruned), and the poisoned model (with a backdoor inserted into 10 samples). Fig.2 is the decision boundary visualization results. And we have the following observations:

•Observation #1: Model tampering leads to shifts in model decision boundaries.

As shown in the first line of Fig.2, fine-tuning, pruning, and poisoning models result in shifts in model decision boundaries, which proves that generating verification samples near the decision boundary to verify the model integrity is reasonable. If the decision boundary is shifted significantly, the model’s output for these verification samples near the decision boundary will change, thus indicating that the model has been tampered with.

•Observation #2: Different positions of the decision boundary exhibit varying shift distances.

Manuscript submitted to ACM

![](images/8fc1b6e706c64ae6a3d461c066b055b2026efe0cc0e2791932ef3a72dbd6e605.jpg)



(a) AlexNet with MNIST

![](images/ac6ee5f61844d7f965c5ba5f64cb34bae36c639ad650536824021bb07d98cbc4.jpg)



(b) VGG16 with CIFAR-10

![](images/e2de694ef87d54df431814fd7754824eda62e93a4eed3a3a9c7e51ab88ca1589.jpg)



(c) ResNet34 with CIFAR-100   
Fig. 2. Model decision boundary visualization results before and after different model tampering. Different colors represent different decision regions, with black specifically indicating the regions where decisions have changed. The first row displays the decision boundary visualization for the source model and the various modified models, while the second row illustrates the differences in the decision regions between the source model and the modified models.

As shown in the second line of Fig.2, not all decision boundaries are shifted significantly after the model is tampered with. This means that if the generated verification samples are close to a decision boundary with a small shift distance, the model’s output may remain unchanged, which can lead to false positives in integrity verification.

However, existing methods only consider how to generate verification samples near model decision boundaries efficiently. This oversight means that integrity verification can fail when the generated verification samples are close to decision boundaries with smaller shift magnitudes. The lack of consideration for the shift magnitude directly leads to false positives in integrity verification methods. While generating more verification samples might reduce false positives, it would undoubtedly increase the verification overhead.

•Observation #3: Some portions of the decision boundary consistently shift by relatively large distances, while others shift by relatively small distances.

Fortunately, we also observe the above pattern, i.e., the shifts in part of the decision boundaries at the same positions tend to be consistent in relative magnitude when faced with different types of model tampering. That is, some positions always shift by a relatively small amount, while some always shift by a relatively large amount, regardless of the type of model tampering.

This motivates us to identify regions of the decision boundary that are highly sensitive to model tampering and to generate verification samples near them. To capture this, we introduce the concept of decision boundary sensitivity, which characterizes the relative magnitude of boundary shifts under various types of tampering. Regions that exhibit large shifts are defined as sensitive decision boundaries, while those with minimal change are deemed insensitive.

By quantifying sensitivity across the decision boundary, we can selectively generate verification samples near the most sensitive regions. This ensures that even minor tampering leads to observable changes in model predictions, thereby enabling accurate and reliable integrity verification.

# 5 Integrity Verification

In this section, we design an accurate and efficient integrity verification method. This method first precisely quantifies the sensitivity of different decision boundaries. Then it generates verification samples close to the most sensitive boundaries while reducing redundant samples, thereby achieving low verification overhead and high accuracy in integrity verification. Additionally, integrity verification can be performed at any time after the verification samples are generated.

![](images/5d85534a899479171fbaa0e9cd9e9815a15b91deb1c05be1cf0abacd95620c36.jpg)



Fig. 3. Verification samples generation method workflow.

# 5.1 Approach Design

The workflow of our design is shown in Fig.3, which includes three key phases: 1) Identification: identifying sensitive parts of the decision boundaries and generating verification samples along them; 2) Measurement: measuring the shift distance as an indicator of sensitivity at different positions along these sensitive decision boundaries; 3) Filtration: adaptive filtering out redundant verification samples based on the distance between them. This approach allows us to efficiently obtain sparse yet highly accurate samples for instant verification of the deployed model’s integrity, as detailed below.

# 5.2 Identification Phase

Based on observation 2, sensitive decision boundaries are biased towards shifting under model tampering. Therefore, we identify sensitive decision boundaries by observing whether decision boundaries change after a slight model modification.

Specifically, we first modify the model ?? to obtain ?? modified models $\{ M _ { i } \} _ { i = 1 } ^ { t }$ . Note that we only slightly modify the model ??, e.g., fine-tuning 10 epochs, pruning 10% of the parameters. This is crucial because when the model is heavily modified, most of the decision boundaries are shifted, making it impossible to identify sensitive ones. Then, to visualize the decision boundaries of both the original model ?? and the modified variants $\{ M _ { i } \} _ { i = 1 } ^ { t }$ , we randomly select three data points from the dataset to span a 2D decision plane. Following the methodology in [24], we establish an orthogonal coordinate system on this plane using two basis vectors derived from the selected points. Any location within this plane can thus be uniquely represented and queried. Finally, the decision boundaries are rendered by evaluating and mapping the models’ outputs across a dense grid of points sampled from this plane. Based on the visualization results of the same decision plane for models ?? and $\{ M _ { i } \} _ { i = 1 } ^ { t } .$ , we identify sensitive decision boundaries that shift in all decision planes. The whole process corresponds to steps 1-3 in phase 1 of Fig.3 (?? = 1 in the figure), and the portions within the red box are identified as sensitive decision boundaries because this part of the decision boundary produces significant shifts after model tampering.

In addition, we remove sensitive decision boundaries that randomly shift to both sides and only retain those that shift consistently to one side. This is because when we generate a verification sample on one side of a sensitive decision boundary, shifting the decision boundary to the opposite side will not change the model’s output for this sample, Manuscript submitted to ACM

thereby failing integrity verification. Considering that decision boundary visualization involves generating sample points sequentially along the horizontal axis, we take such a strategy to generate the verification samples V:

• When the sensitive decision boundary shifts to the left (as shown in Case 1 of phase 1 in Fig.3), we search for sample points from the left side of the decision boundary of ?? that satisfy the following conditions as a verification sample ?? and add it to V:

$$
M (\boldsymbol {x}) \neq M _ {i} (\boldsymbol {x}), M \left(\boldsymbol {x} _ {+ 1}\right) = M _ {i} \left(\boldsymbol {x} _ {+ 1}\right), f o r i \in [ 1,.., t ], \tag {2}
$$

where $x _ { + 1 }$ indicates the next sample point along the horizontal direction of ??. The generated verification samples are shown in Case 1 of phase 1 in Fig.3.

• When the sensitive decision boundary shifts to the right (as shown in Case 2 of phase 1 in Fig.3), we search for sample points from the right side of the decision boundary of ?? that satisfy the following conditions as a verification sample ?? and add it to V:

$$
M (\boldsymbol {x}) \neq M _ {i} (\boldsymbol {x}), M (\boldsymbol {x} _ {- 1}) = M _ {i} (\boldsymbol {x} _ {- 1}), f o r i \in [ 1,.., t ], \tag {3}
$$

where $x _ { - 1 }$ indicates the previous sample point along the horizontal direction of ??. The generated verification samples are shown in Case 2 of phase 1 in Fig.3.

• When the sensitive decision boundary is shifted to both sides, we skip it.

Using this strategy to generate verification samples can guarantee that the samples are closest to sensitive decision boundaries, which are biased towards shifting to only one side. As soon as the model is tampered with, the model’s outputs for these samples change immediately, and the model can be instantly identified as having been tampered with.

# 5.3 Measurement Phase

However, we found that the large number of sensitive decision boundaries generated an excessive number of verification samples. To address this, we designed a metric to measure the sensitivity of decision boundaries, identifying the most sensitive areas and generating verification samples accordingly, defined as follows.

On a visualized decision plane, we define the sensitivity based on the displacement of the decision boundary under perturbation. However, as the precise direction and angle of the boundary shift are non-trivial to determine analytically, we employ the Horizontal Shift Distance $( d _ { i } )$ as an effective estimator, as shown in phase 2 of Fig.3. For a specific verification sample ?? located near the original decision boundary, its horizontal shift distance $d _ { i }$ is formally defined as:

$$
d _ {i} = \arg \min _ {d} [ M (\boldsymbol {x} + d * \boldsymbol {v} _ {\boldsymbol {h}}) = M _ {i} (\boldsymbol {x} + d * \boldsymbol {v} _ {\boldsymbol {h}}) ], \tag {4}
$$

where $_ { x }$ is the verification sample near the decision boundary, ${ \boldsymbol { v } } _ { h }$ is a unit vector along the horizontal axis, and $d _ { i }$ captures the shortest distance along the horizontal scanline required to encounter a change in the model’s decision logic. The overall sensitivity ?? of the decision boundary at the point ?? is calculated as the mean horizontal shift distance across ?? sampled points:

$$
s = \frac {1}{N} \sum_ {i = 1} ^ {N} d _ {i}. \tag {5}
$$

The metric ?? effectively reflects the boundary’s vulnerability. In our workflow, we rank the decision boundaries based on their calculated sensitivities and retain only the verification samples corresponding to the top-?? most sensitive

Manuscript submitted to ACM

boundaries. This prioritization ensures that the verification set remains compact while capturing the most critical decision-making fluctuations.

# 5.4 Filtration Phase

However, we still encounter a substantial number of redundant verification samples due to some highly sensitive decision boundaries being close to each other. When the model is tampered with, these decision boundaries are shifted in the same direction, causing the model outputs for these verification samples to change identically. Consequently, these samples have the same effect on integrity verification and are, therefore, redundant. We propose an adaptive filtering method to address this redundancy, as shown in phase 3 of Fig.3.

The core objective is to ensure that the final verification set V covers diverse sensitive regions without clustering samples that react identically to model tampering. The process is structured as a greedy selection algorithm:

(1) Initial Selection: Let $C = \{ x _ { 1 } , x _ { 2 } , \ldots , x _ { m } \}$ be the set of candidate verification samples, ranked in descending order of their point-wise sensitivity ??. We initialize the final verification set $\mathcal { V } = \{ x _ { t o p } \}$ , where $\boldsymbol { x } _ { t o p }$ is the sample with the highest sensitivity.   
(2) Iterative Pruning: For each subsequent sample $x _ { i } \in C$ (following the sensitivity ranking), we calculate its Euclidean distance to all existing samples in $_ \mathrm { ~  ~ }$ .   
(3) Distance-based Admission: A sample $x _ { i }$ is added to V if and only if it satisfies:

$$
\min _ {\boldsymbol {v} \in \mathcal {V}} | \boldsymbol {x} _ {i} - \boldsymbol {v} | _ {2} > \delta \tag {6}
$$

where ?? is an empirical spatial threshold. Samples failing this criterion (represented by the purple markers in Fig.3, Phase 3) are discarded as redundant. In this way, redundant samples are removed, leaving only sparse verification samples for integrity verification.

# 5.5 Verification

In the verification phase, we query these verification samples to the deployed model $M ^ { \prime }$ and compare the result of returned predictions with those of the model ??. If any of the predictions differ, we treat that the deployed model has been tampered with. That is,

$$
r e s = \sum_ {\boldsymbol {x} \in \mathcal {V}} | M (\boldsymbol {x}) - M ^ {\prime} (\boldsymbol {x}) |. \tag {7}
$$

If ?????? $\neq 0 ,$ the verification fails, indicating that the deployed model has been tampered with.

# 5.6 Computational Complexity Analysis

To evaluate the efficiency of the proposed framework, we analyze the computational complexity across all phases, categorized into generation and verification, as shown in Table 1.

• Identification: Requires $( t + 1 ) \cdot G ^ { 2 }$ model inference passes to visualize the decision boundaries on a $G \times G$ grid for ?? modified models. The complexity is $O ( t \cdot G ^ { 2 } )$ .   
• Measurement: For ?? candidate samples and ?? models, the complexity is $O ( m \cdot N \cdot L )$ , where ?? is the average search depth along the horizontal scanline to find $d _ { i } .$ .   
• Filtration: Sorting ?? candidates takes $O ( m \log m )$ , and the greedy distance-based pruning takes $O ( m \cdot | \mathcal { V } | )$ .

Manuscript submitted to ACM

• Verification: This phase only requires ?? queries $( k \ = \ | \mathcal V | )$ to the deployed model ??′, resulting in ?? (??) complexity.

Table 1. Summary of Computational Complexity 

<table><tr><td>Phase</td><td>Main Operation</td><td>Complexity</td></tr><tr><td>Identification</td><td>Grid-based Inference</td><td> $O(t \cdot G^{2})$ </td></tr><tr><td>Measurement</td><td>Scanline Search</td><td> $O(m \cdot N \cdot L)$ </td></tr><tr><td>Filtration</td><td>Sorting &amp; Pruning</td><td> $O(m \log m + m|\mathcal{V}|)$ </td></tr><tr><td>Verification</td><td>Sample Querying</td><td> $O(k)$ </td></tr></table>

In summary, the Identification Phase $( O ( t \cdot G ^ { 2 } ) )$ and Measurement Phase $\left( O ( m \cdot N \cdot L ) \right)$ are performed offline without real-time constraints. The grid resolution ?? is a user-defined hyperparameter, allowing a flexible trade-off between boundary precision and generation speed. Moreover, the search step ?? in the measurement phase is intrinsically tied to $G ,$ ensuring the search space remains bounded. The Filtration Phase maintains a low overhead because the final verification set $_ \textmd { ‰}$ is intentionally kept sparse. Pruning ?? candidates down to a small constant ?? involves a simple greedy distance check, which is computationally negligible. The Online Verification is decoupled from the grid resolution $G ,$ requiring only ?? (??) inference passes $( k \ll G ^ { 2 } ) .$ . This ensures that once the samples are generated, the integrity check is near-instantaneous upon model deployment.

# 5.7 Performance Analysis

We further illustrate the superiority of our scheme compared to existing work in the following aspects:

5.7.1 The design principle is intuitive: Existing work works on generating samples near decision boundaries. However, there are many decision boundaries in the decision space, and exactly which decision boundary to choose to generate verification samples near it is not considered in the existing work. Intuitively, not every decision boundary is appropriate, and our visual observation of decision boundaries confirms this conclusion. Therefore, in order to achieve the most accurate integrity verification possible, choosing the most appropriate decision boundary is the key to integrity verification. Our scheme’s design core lies in finding the most appropriate decision boundaries to generate verification samples.   
5.7.2 A suitable metric is designed: We design the average shift distance of the model’s decision boundary as the sensitivity of the decision boundary. We aim to identify the most suitable decision boundary for generating verification samples. Although this sensitivity is an empirical value, it is just a scale reflecting the relative size of the shift distances of different decision boundaries. It will not have any effect on identifying the most sensitive decision boundaries.   
5.7.3 A sufficient number of verification samples can be generated: In practice, the model owner is not required to keep the generated verification samples confidential. By varying the sampling points, a substantial number of verification samples can be pre-generated. This approach facilitates the construction of multiple, independent sets of verification samples, thereby strengthening the robustness and reliability of the integrity verification mechanism.   
5.7.4 Integrity verification is low overhead: Related works require increasing the number of verification samples to ensure the accuracy of integrity verification. Instead, we generate the most suitable verification samples, only a few are required to achieve accurate integrity verification. Moreover, our scheme does not bring additional model training overhead when generating verification samples as in related work.

![](images/cf56a6368e9dac2e2bb89bb0993919d2e4748a6729912a260e87e4f2363a41f2.jpg)



(a)

![](images/0470f4d75bad46776b1ebc52903348928107e646755ff2220e588625541606a0.jpg)



(b)

![](images/8ff4a1d594e8508416f18d80009634cfde2936e573c4cf11a01c865f68b3d334.jpg)



(c)

![](images/7be1b07eaa29966808f914c463132f96959b189dbaf2ce64b2df6385d88fbc78.jpg)



Fig. 4. The number of valid verification samples generated by our method (blue lines), PublicCheck (orange lines, PC for short), Trigger-based (red lines), and DeepAuth (purple lines) across different models and various forms of model tampering. A is short for AlexNet, V is short for VGG16, R is short for ResNet34, which imply that the model structure is AlexNet, VGG16 or ResNet34, respectively.

# 6 Experiments

In this section, we conducted extensive experiments on various models to demonstrate our method’s accuracy, efficiency, sparsity, and robustness.

# 6.1 Experiments Setup

To demonstrate the effectiveness of our method, we conducted experiments on three types of model tampering: finetuning, pruning, and poisoning. These experiments were performed using three datasets, MNIST, CIFAR-10, and CIFAR-100, as well as three model structures, AlexNet, VGG16, and ResNet34. We utilized the MNIST, CIFAR-10, and CIFAR-100 datasets to train three models, AlexNet, VGG16, and ResNet34, which were subsequently treated as models deployed to the cloud for integrity verification. All experiments were conducted on a Linux Server with 4 Tesla P100 GPUs and implemented with PyTorch 1.5 using Python 3.7.

# 6.2 Accuracy Evaluation

We compared the accuracy of our method against two advanced integrity verification methods, Trigger-based [27], DeepAuth [18] and PublicCheck[25], which served as baselines. We then evaluated the accuracy of our method in comparison to baseline methods.

Since the results are not generalizable when using a small number of verification samples for integrity verification, we randomly generated 100 verification samples for each method to evaluate which method is the most accurate thoroughly. Specifically, instead of assessing whether the methods can detect tampering with the model, we focus on comparing which method produces more valid verification samples. A valid verification sample is one where the model’s output changes after the model has been tampered with. The greater the number of valid verification samples, the higher the probability that integrity verification can be performed accurately.

For our method, we first fine-tuned the model with 5 epochs and pruned 10% of the parameters to obtain two modified models. We then visualized the decision boundaries of five different regions of the model’s decision space, generating 20 verification samples for each region. In this way, we generated 100 verification samples for each model. For Trigger-based, DeepAuth, and PublicCheck, we generated 100 verification samples for each model separately, based on their respective source code.

Manuscript submitted to ACM

Subsequently, we evaluated the accuracy of model integrity under different tampering methods, including fine-tuning, pruning, and poisoning, as described below:

• Fine-tuning: we fine-tune the model with training data using two approaches:

– Different epochs: Fine-tuning the model’s fully connected layer for 2, 5, 7, 10, 15, and 20 epochs;   
– Different amounts of parameters: Fine-tuning various parts of the model, including the fully connected layer (denoted as fc), the fully connected layer and 1 convolutional layer (fc1), the fully connected layer and 2 convolutional layers (fc2), the fully-connected layer and 3 convolutional layers (fc3), the entire model (fe);

• Pruning [8]: pruning ??% (from 20% to 90%) of the model parameters;

• Poisoning [7]: poisoning ??% (from 5% to 30%) of the training data of the model.

We verified the integrity of these tampered models with the generated verification samples, the results of which are described below:

6.2.1 Fine-tuning. Fig.4(a) and Fig.4(b) illustrate the results of fine-tuning with different epochs and varying amounts of parameters across different models. We observe that, regardless of the model or fine-tuning strategy chosen, the number of valid verification samples generated by our method significantly exceeds that of the baseline methods. Specifically, the average number of valid samples produced by our method is around 90. Notably, even when fine-tuning the full set of parameters for the VGG model, where the effective number of samples drops slightly to 78, our method still far outperforms the other two methods, which generate only 48 and 14 effective samples, respectively. This shows that our method can achieve high accuracy in verifying whether the model is fine-tuned or not.

6.2.2 Pruning. As shown in Fig.4(c), our method consistently generates a higher number of valid verification samples compared to the baselines. Notably, at a pruning rate of 20%, the results for AlexNet and ResNet34 are relatively lower, with only 55 and 49 valid samples, respectively, as this level of pruning has minimal impact on the model’s performance. When pruning 30%-70% of the parameters, our method significantly outperforms the baselines. At higher pruning rates of 80%-90%, the number of valid verification samples becomes comparable across all three methods, as the model has been substantially tampered with. In summary, our method can achieve high accuracy in verifying whether the model is pruned or not.

6.2.3 Poisoning. As shown in Fig.4(d), our method outperforms the baselines across the board. At a poisoning rate of 5%, the number of effective validation samples for VGG and ResNet34 is 65 and 53, respectively, due to the minimal impact on the model. However, as the poisoning rate increases, the number of effective validation samples generated by our method exceeds 80, demonstrating its superior performance. That is, our method can achieve high accuracy in verifying whether the model is poisoned or not.

In summary, our method consistently yields the highest number of valid verification samples across various models and tampering scenarios, indicating superior integrity verification accuracy. Furthermore, the lower number of valid verification samples in other methods highlights the previously mentioned shortcoming: the neglect of decision boundary shift magnitude, which results in false positives.

# 6.3 Efficiency

We compare the time efficiency of our method with that of the baselines across three model structures and three datasets. The time overhead includes verification sample generation and model integrity verification. In the verification

Manuscript submitted to ACM

Table 2. Comparison of the average time costs (sec). 

<table><tr><td colspan="4">(a) Verification sample generation</td><td colspan="4">(b) Integrity verification</td></tr><tr><td>Models</td><td>AlexNet</td><td>VGG16</td><td>ResNet34</td><td>Models</td><td>AlexNet</td><td>VGG16</td><td>ResNet34</td></tr><tr><td>Trigger-based</td><td>4500</td><td>18500</td><td>6000</td><td>Trigger-based</td><td>7</td><td>11</td><td>9</td></tr><tr><td>DeepAuth</td><td>5500</td><td>20000</td><td>7200</td><td>DeepAuth</td><td>7</td><td>11</td><td>9</td></tr><tr><td>PublicCheck</td><td>3600</td><td>14200</td><td>5200</td><td>PublicCheck</td><td>7</td><td>11</td><td>9</td></tr><tr><td>Ours</td><td>850</td><td>3000</td><td>1200</td><td>Ours</td><td>7</td><td>11</td><td>9</td></tr></table>

Table 3. Success rate of integrity verification with different numbers of verification samples across different models. 

<table><tr><td>Number of Verification Samples</td><td>AlexNet</td><td>VGG13</td><td>ResNet18</td></tr><tr><td>1</td><td>96 ± 4</td><td>88 ± 12</td><td>86 ± 14</td></tr><tr><td>2</td><td>98 ± 2</td><td>92 ± 1</td><td>94 ± 6</td></tr><tr><td>3</td><td>100 ± 0</td><td>94 ± 1</td><td>97 ± 3</td></tr><tr><td>4</td><td>100 ± 0</td><td>100 ± 0</td><td>100 ± 0</td></tr><tr><td>5</td><td>100 ± 0</td><td>100 ± 0</td><td>100 ± 0</td></tr><tr><td>6</td><td>100 ± 0</td><td>100 ± 0</td><td>100 ± 0</td></tr><tr><td>7</td><td>100 ± 0</td><td>100 ± 0</td><td>100 ± 0</td></tr><tr><td>8</td><td>100 ± 0</td><td>100 ± 0</td><td>100 ± 0</td></tr></table>

sample generation phase, the time overhead for baselines includes both the generation of verification samples and the fine-tuning of the model using these samples. Among these, fine-tuning the model represents the primary time overhead. In contrast, our method is fine-tune-free, resulting in significant time savings. As shown in Tab.2, our method exhibits lower time overhead than the baselines for generating verification samples across different models. In the model integrity verification phase, although the query time for the same number of verification samples is consistent across methods, our approach benefits from having more valid verification samples within the same size of the verification samples. Consequently, given the same verification accuracy, our method requires fewer verification samples, thus achieving lower verification overhead.

# 6.4 Sparsity

To illustrate the sparsity of our approach, we calculated the success rate of integrity verification when generating different numbers of verification samples across three model structures and three datasets. The success rate is defined as the accuracy achieved when performing multiple integrity verification across various models. Specifically, for each model, we generate 1-8 verification samples 10 times to perform integrity verification on 25 tampered models generated in the accuracy evaluation. Among them, the verification samples generated were different each time. The results are shown in Tab.3. When generating 3 verification samples, our method achieves a success rate of over 90% across three model structures. Furthermore, with just 4 verification samples, our method achieves a 100% success rate, demonstrating that our approach can perform accurate integrity verification with minimal verification overhead (only querying 4 samples).

# 6.5 Robustness

In this section, we analyze potential strategies that a dishonest server might employ to circumvent the integrity verification process, thereby demonstrating the robustness of our proposed scheme.

Manuscript submitted to ACM

![](images/dd5e74037fda06aee420257dde904df8af8afeb2d6c363fc43e3ee06f0e7f38c.jpg)



Fig. 5. Schematic of the strategy for mixing normal query and verification samples. The normal query samples are from the CIFAR10 dataset, and the verification samples are obtained by sampling on a model with VGG16 as the model structure and CIFAR10 as the training data.

Given that the verification samples are publicly accessible, a dishonest server may attempt to distinguish them from regular query samples. To this end, the server could adopt the following strategy:

6.5.1 Observational Attacks. Verification samples, being artificially constructed, are inherently distinguishable from normal query images. A dishonest server may attempt to bypass integrity verification by observing and identifying whether a given query image is part of the normal workload or a verification sample. In particular, when multiple verification samples are queried simultaneously, such behavior becomes more apparent and easier to detect.

To mitigate this risk, we adopt the strategy proposed in [28], which involves mixing verification samples with normal queries. Specifically, for each verification sample, we select nine normal query images, mix them together, and randomize their order. The resulting batch of ten images is then submitted as a query.

This approach ensures that verification samples are sparsely and randomly distributed among normal query images, thereby increasing the difficulty and computational cost for a malicious server attempting to identify them through visual or statistical observation. As illustrated in Fig. 5, although verification samples may still exhibit observable differences from normal samples, the mixing and shuffling process effectively obscures their presence, significantly reducing the likelihood of successful detection.

6.5.2 Random Noise. Assuming that a dishonest server is aware of the presence of verification samples within the query set, it may attempt to invalidate the integrity verification process by introducing random noise into the input images.

To evaluate the robustness of our verification mechanism under such an attack, we test the performance of verification samples after the addition of varying levels of random Gaussian noise. Specifically, for each model evaluated in Section 6.2, we generate four verification samples and test them against 25 tampered models. Gaussian noise with a mean of 0 and standard deviations of 0.01, 0.05, 0.1, 0.5, and 1 is added to each verification sample. The results of these experiments are presented in Table 4.

Experimental results demonstrate that, across three model architectures and three datasets, our verification samples maintain 100% accuracy in detecting integrity violations, even after the addition of Gaussian noise at various intensity levels. These findings confirm the robustness of our approach, indicating that randomly injecting noise into verification samples does not compromise the effectiveness of integrity verification.

Table 4. Impact of Adding Gaussian Noise on Integrity Verification. 

<table><tr><td></td><td>σ=0.01</td><td>σ=0.05</td><td>σ=0.1</td><td>σ=0.5</td><td>σ=1</td></tr><tr><td>AlexNet</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td></tr><tr><td>VGG16</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td></tr><tr><td>ResNet34</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td><td>25(100%)</td></tr></table>

Table 5. Performance on the trained classifier to classify the verification samples and the normal samples. 

<table><tr><td></td><td>AlexNet</td><td>VGG16</td><td>ResNet34</td></tr><tr><td>Verification samples</td><td>4% (4/100)</td><td>6% (6/100)</td><td>2% (2/100)</td></tr><tr><td>Normal samples</td><td>99% (99/100)</td><td>98% (98/100)</td><td>99% (99/100)</td></tr></table>

6.5.3 Adaptive Attack. A more challenging scenario arises when a malicious server has obtained a subset of the verification samples and attempts to train a classifier to distinguish verification samples from normal query images.

To assess the feasibility of such an attack, we generate 100, 200, and 500 verification samples for AlexNet, VGG16, and ResNet34, respectively, based on the complexity of their model architectures. For each case, an equal number of normal query images are mixed in to train a binary classifier aimed at distinguishing between verification and normal samples. We then construct an independent evaluation set comprising 100 verification samples and 100 normal query images per model to test the classifier’s performance. The results are presented in Table 5.

Across all model structures, the classifiers exhibit poor performance, consistently failing to distinguish verification samples from normal samples. In most cases, both types of inputs are classified as normal queries. This suggests that verification samples do not share distinguishable or consistent features that differentiate them from normal samples, rendering such classification-based detection ineffective.

Moreover, an attacker might attempt to exploit knowledge of the verification sample generation process by finetuning the deployed model or checking whether any of the queried images match previously observed verification samples in an effort to identify or replicate them.

However, these strategies are highly impractical. Verification samples are generated by sampling near the decision boundary determined by three randomly selected data points in the input space. Due to the vast number of potential data point combinations and the high complexity of the decision space, it is computationally infeasible to enumerate all possible verification samples. Additionally, fine-tuning the model using a large number of verification samples is likely to cause significant degradation in the model’s overall performance, further disincentivizing such attempts.

In conclusion, our analysis and experimental results demonstrate that, even when verification samples are accessible to the server and the integrity verification framework is known, it remains highly challenging for the server to accurately identify the verification samples using any practical or cost-effective strategy.

# 7 Conclusion

In this work, we propose a novel integrity verification method that leverages decision boundary sensitivity as an indicator, inspired by insights from the visualization of decision boundaries under various model tampering scenarios. Furthermore, we introduce an adaptive filtering strategy to reduce verification overhead, enhancing the practicality of the approach. Extensive experimental evaluations demonstrate that the proposed method achieves both high accuracy and efficiency, offering a robust and cost-effective solution for model integrity verification.

Manuscript submitted to ACM

# Acknowledgments

The research is partially supported by Quantum Science and Technology-National Science and Technology Major Project (QNMP) 2021ZD0302900 and China National Natural Science Foundation with No. 92567301, 62441228, 62132018, 62231015, Science and Technology Tackling Program of Anhui Province, No.202423k09020016, Pioneer and Leading Goose R&D Program of Zhejiang, 2023C01029, and 2023C01143.

# References

[1] 2023. http://cloud.google.com/ml-engine/.   
[2] 2023. https://azure.microsoft.com/.   
[3] 2023. https://aws.amazon.com/sagemaker/.   
[4] Yossi Adi, Carsten Baum, Moustapha Cisse, Benny Pinkas, and Joseph Keshet. 2018. Turning your weakness into a strength: Watermarking deep neural networks by backdooring. In 27th USENIX security symposium (USENIX Security 18). 1615–1631.   
[5] Daniel Crankshaw, Xin Wang, Guilio Zhou, Michael J Franklin, Joseph E Gonzalez, and Ion Stoica. 2017. Clipper: A {Low-Latency} online prediction serving system. In 14th USENIX Symposium on Networked Systems Design and Implementation (NSDI 17). 613–627.   
[6] Alhussein Fawzi, Seyed-Mohsen Moosavi-Dezfooli, Pascal Frossard, and Stefano Soatto. 2018. Empirical study of the topology and geometry of deep networks. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 3762–3770.   
[7] Tianyu Gu, Kang Liu, Brendan Dolan-Gavitt, and Siddharth Garg. 2019. Badnets: Evaluating backdooring attacks on deep neural networks. IEEE Access 7 (2019), 47230–47244.   
[8] Song Han, Jeff Pool, John Tran, and William Dally. 2015. Learning both weights and connections for efficient neural network. Advances in neural information processing systems 28 (2015).   
[9] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. 2016. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition. 770–778.   
[10] Warren He, Bo Li, and Dawn Song. 2018. Decision boundary analysis of adversarial examples. In International Conference on Learning Representations.   
[11] Zecheng He, Tianwei Zhang, and Ruby Lee. 2019. Sensitive-sample fingerprinting of deep neural networks. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 4729–4737.   
[12] Ehsan Hesamifard, Hassan Takabi, Mehdi Ghasemi, and Rebecca N Wright. 2018. Privacy-preserving machine learning as a service. Proceedings on Privacy Enhancing Technologies (2018).   
[13] Hengrui Jia, Christopher A Choquette-Choo, Varun Chandrasekaran, and Nicolas Papernot. 2021. Entangled watermarks as a defense against model extraction. In 30th USENIX security symposium (USENIX Security 21). 1937–1954.   
[14] Hamid Karimi, Tyler Derr, and Jiliang Tang. 2019. Characterizing the decision boundary of deep neural networks. arXiv preprint arXiv:1912.11460 (2019).   
[15] A. Krizhevsky and G. Hinton. 2009. Learning multiple layers of features from tiny images. Handbook of Systemic Autoimmune Diseases 1, 4 (2009).   
[16] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E Hinton. 2012. Imagenet classification with deep convolutional neural networks. Advances in neural information processing systems 25 (2012), 1097–1105.   
[17] Yingjie Lao, Peng Yang, Weijie Zhao, and Ping Li. 2022. Identification for deep neural network: Simply adjusting few weights!. In 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 1328–1341.   
[18] Yingjie Lao, Weijie Zhao, Peng Yang, and Ping Li. 2022. DeepAuth: A DNN Authentication Framework by Model-Unique and Fragile Signature Embedding. In Thirty-Sixth AAAI Conference on Artificial Intelligence, AAAI 2022, Thirty-Fourth Conference on Innovative Applications of Artificial Intelligence, IAAI 2022, The Twelveth Symposium on Educational Advances in Artificial Intelligence, EAAI 2022 Virtual Event, February 22 - March 1, 2022. AAAI Press, 9595–9603.   
[19] Yann LeCun, Léon Bottou, Yoshua Bengio, and Patrick Haffner. 1998. Gradient-based learning applied to document recognition. Proc. IEEE 86, 11 (1998), 2278–2324.   
[20] Suyoung Lee, Wonho Song, Suman Jana, Meeyoung Cha, and Sooel Son. 2022. Evaluating the robustness of trigger set-based watermarks embedded in deep neural networks. IEEE Transactions on Dependable and Secure Computing 20, 4 (2022), 3434–3448.   
[21] Yingqi Liu, Shiqing Ma, Yousra Aafer, Wen-Chuan Lee, Juan Zhai, Weihang Wang, and Xiangyu Zhang. 2018. Trojaning attack on neural networks. In 25th Annual Network And Distributed System Security Symposium (NDSS 2018). Internet Soc.   
[22] Mauro Ribeiro, Katarina Grolinger, and Miriam AM Capretz. 2015. Mlaas: Machine learning as a service. In 2015 IEEE 14th international conference on machine learning and applications (ICMLA). IEEE, 896–902.   
[23] Karen Simonyan and Andrew Zisserman. 2015. Very deep convolutional networks for large-scale image recognition. In 3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings.   
[24] Gowthami Somepalli, Liam Fowl, Arpit Bansal, Ping Yeh-Chiang, Yehuda Dar, Richard Baraniuk, Micah Goldblum, and Tom Goldstein. 2022. Can neural nets learn the same model twice? investigating reproducibility and double descent from the decision boundary perspective. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 13699–13708.

Manuscript submitted to ACM

[25] Shuo Wang, Sharif Abuadbba, Sidharth Agarwal, Kristen Moore, Ruoxi Sun, Minhui Xue, Surya Nepal, Seyit Camtepe, and Salil S. Kanhere. 2023. PublicCheck: Public Integrity Verification for Services of Run-time Deep Models. In 44th IEEE Symposium on Security and Privacy, SP 2023, San Francisco, CA, USA, May 21-25, 2023. IEEE, 1348–1365.   
[26] Zhaoxia Yin, Heng Yin, and Xinpeng Zhang. 2022. Neural network fragile watermarking with no model performance degradation. In 2022 IEEE International Conference on Image Processing (ICIP). IEEE, 3958–3962.   
[27] Renjie Zhu, Ping Wei, Sheng Li, Zhaoxia Yin, Xinpeng Zhang, and Zhenxing Qian. 2021. Fragile neural network watermarking with trigger image set. In Knowledge Science, Engineering and Management: 14th International Conference, KSEM 2021, Tokyo, Japan, August 14–16, 2021, Proceedings, Part I 14. Springer, 280–293.   
[28] Xirong Zhuang, Lan Zhang, Chen Tang, and Yaliang Li. 2024. DEEPREG: A Trustworthy and Privacy-Friendly Ownership Regulatory Framework for Deep Learning Models. IEEE Transactions on Information Forensics and Security (2024).