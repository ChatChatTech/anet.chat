# DEEPREG: A Trustworthy and Privacy-Friendly Ownership Regulatory Framework for Deep Learning Models

Xirong Zhuang, Lan Zhang, Chen Tang, Yaliang Li

Abstract—Well-trained deep learning (DL) models are widely recognized as valuable intellectual property (IP) and have been extensively adopted. However, concerns regarding IP infringement emerge when these models are either privately sold to endusers or publicly released online. Unauthorized activities, such as redistributing privately purchased models or exploiting restricted open-source models for commercial gain, pose a significant threat to the interests of model owners. In this paper, we introduce DEEPREG, a trustworthy and privacy-friendly regulatory framework designed to address IP infringement within the realm of DL models, thereby nurturing a healthier development ecosystem. DEEPREG enables a designated third-party regulator to extract the fingerprint of the original model within a Trusted Execution Environment, as well as to verify suspect models utilizing solely the predicted label without probability. Specifically, we leverage the uniqueness of feature extractors in DL models to craft multiple synthetic inputs for a selected real input. The real input, along with its synthetic inputs, establishes a one-tomany relationship, thereby creating a unique fingerprint for the original model. Furthermore, we propose two distinct methods for suspect detection and piracy judgment. These methods analyze the responses from the model API upon feeding the fingerprint, ensuring a high level of confidence while preventing malicious accusations. Experimental results demonstrate that DEEPREG achieves 100% detection accuracy for pirated models, with zero false positives for irrelevant models.

Index Terms—Model regulation, model fingerprint, piracy detection, deep learning.

# I. INTRODUCTION

Deep learning (DL) techniques have achieved remarkable results in diverse applications [1], [2]. Since designing and training high-performance models requires significant upfront investment from model owners, encompassing the preparation of high-quality datasets and the allocation of considerable time and resources, well-trained DL models have been acknowledged as valuable intellectual property (IP) [3].

This research was supported in part by the National Key R&D Program of China 2021YFB2900103, in part by China National Natural Science Foundation with No. 61932016, in part by Science and Technology Tackling Program of Anhui Province with No.202423k09020016, in part by “the Fundamental Research Funds for the Central Universities” WK2150110024, and in part by the University Synergy Innovation Program of Anhui Province under Grant GXXT-2022-049. (Corresponding author: Lan Zhang.)

Xirong Zhuang, Lan Zhang and Chen Tang are with the School of Computer Science and Technology, University of Science and Technology of China, Hefei 230052, China (e-mail: xirongz@mail.ustc.edu.cn; zhanglan@ustc.edu.cn; chentang1999@mail.ustc.edu.cn). Lan Zhang is also with the Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, Hefei 230031, China.

Yaliang Li is with Alibaba Group, Bellevue, WA, USA, (e-mail: yaliang.li@alibaba-inc.com).

To fully exploit the value of DL models, model owners may privately sell them to end users for economic benefits, or publicly release them online to broaden their community impact [4]–[6]. In either case, model owners typically put usage restrictions on their models to prevent unauthorized activities such as redistributing purchased models to others or using publicly released models for commercial purposes. However, dishonest users, lured by the low risk and minimal consequences, may violate the agreed-upon restrictions and reap substantial profits from the illicit redistribution and redeployment of these models. The rampant IP infringement is further exacerbated by the absence of regulatory mechanisms for model ownership identification and piracy detection, which fail to deter fraudsters from misappropriating DL models.

Existing efforts for IP protection of DL models mainly fall into two categories: watermarking and fingerprinting. Model watermarking [7]–[11] involves embedding a secret into the original model’s internals during training. The model owner can then verify the existence of the exclusively known secret in a suspect model to claim ownership. However, this approach inevitably sacrifices the accuracy of a well-trained model due to the deliberate watermark embedding process, which is unacceptable for mission-critical tasks in domains like healthcare and traffic. Additionally, watermarking each original model to assert ownership is a separate and time-consuming process that requires additional training data and computational resources. In contrast, model fingerprinting [12]–[19] aims to extract the inherent characteristics from each originally trained model without any loss in accuracy. The fingerprint of a pirated model will be similar to that of the original model, but entirely different from that of an irrelevant model.

These fingerprinting techniques can be further categorized into white-box and black-box methods based on their verification requirements. White-box methods typically necessitate access to the structure and weights of suspect models to extract the fingerprint for verification. However, this approach is virtually impractical since the suspect is unlikely to willingly expose their models due to concerns about model security and future profits. Even if the suspect submits a model, the verifier cannot ensure the authenticity of the model, i.e., whether the submitted model is the same as the actually deployed model. The intangible and untraceable nature of DL models makes it challenging to ascertain their true source. Even with the intervention of judicial authorities, it is difficult to exercise a supervisory and review role.

The black-box methods only require querying the suspect model to obtain prediction results for different inputs, thus resolving the verification challenges faced by white-box methods. However, there are still several critical challenges that need to be addressed when applying model fingerprinting to ownership identification and piracy detection in the real world. Firstly, achieving both trustworthy and privacy-friendly ownership identification concurrently poses significant challenges. Existing methods [12]–[19] require a strong trust relationship between the regulator and the model owner. In these approaches, the regulator is either required to trust the fingerprint provided by the model owner, or the model owner must grant access to their original model and operational codes for direct fingerprint extraction by the regulator. However, granting full access to DL models can compromise the model owner’s IP. To the best of our knowledge, there is currently no methodology capable of extracting model fingerprints and conducting trusted verification while simultaneously safeguarding model confidentiality and ensuring data privacy protection. Secondly, the adversary could carry out unpredictable modifications to the original model before deploying it, causing difficulties in piracy detection of post-processed models. Most existing methods [14]–[17] rely on the retention of specific labels in the model’s output for verification, making it easy for adversaries to manipulate the number and labels of the output categories of the model to evade piracy detection. Moreover, adversaries can transfer the model to different tasks, resulting in significant changes to the inherent properties of the original model. Furthermore, certain online services only provide the top-1 predicted label without any probability information, rendering other probability-based methods [18], [19] ineffective for piracy detection. Thirdly, model fingerprints can only be used to detect piracy but cannot serve as definitive proof of ownership for infringement claims, as they can be forged by anyone. An attacker could potentially create a unique fingerprint extractable from the pirated model to counter-claim against the victim model’s ownership [20]. In such cases, the model owner lacks non-repudiation evidence to prevent fraudulent claims of ownership by the adversary.

To address these challenges, we propose an ownership regulatory framework called DEEPREG, which extracts the fingerprint of original models in a Trusted Executed Environment (TEE) and detects the infringement with only blackbox access, thus facilitating trustworthy ownership regulation under a practical threat model. DEEPREG enables privacypreserving ownership identification by leveraging confidential computing based on hardware enclaves; it supports wellfounded detection of suspect models through multiple iterations of prediction grounded on Bayes’ theorem [21]; it enables irrefutable piracy judgment by utilizing undetectable queries and hypothesis-test-guided verification.

Specifically, we propose a black-box model fingerprinting method to tackle the challenge posed by the limited information available from the top-1 predicted label. This method embeds a distinctive representation of the model’s unique characteristics into the input data. Utilizing the principles of transfer learning, we generate multiple synthetic inputs from a single real input to emulate similar feature maps, employing distinct feature extractors of the original model. These synthetic inputs are then paired with the real input, establishing a one-to-many relationship that constitutes the fingerprint of the original model. This method guarantees that despite any alterations to the categories, the pirated model will yield the same predicted labels as the original model. The matching rate for the fingerprint, calculated as the ratio of real-synthetic pairs that successfully match, is used to evaluate the potential piracy connection between the suspect model and the original model, facilitating suspect detection and piracy judgment. To ensure credible support in the event of disputes, the regulator’s enclave maintains a timestamped fingerprint extracted from the original model, linking it to the model owner’s identity. Furthermore, Bayes’ theorem is applied to encode and verify the matching rate intervals of model fingerprints through a systematic iterative process designed to pinpoint suspect models with significant confidence. Lastly, we introduce a hypothesis-testing-guided verification, using the shuffled and integrated registered fingerprint with public samples to ensure a dependable piracy judgment.

Our key contributions are as follows:

• We design DEEPREG, an ownership regulatory framework to resolve trust issues between regulatory authorities and model owners. It extracts the model fingerprint, registers the timestamped certificate within the TEE, and verifies suspect models through only the model API.   
• We propose a versatile fingerprint technique by crafting multiple synthetic inputs for a selected real input. The fingerprint can be verified in a highly compatible manner, as it only necessitates assessing the consistency of output labels for the real-synthetic pairs.   
• We devise an iterative verification process supported by Bayes’ theorem for suspect detection to ensure high confidence and hypothesis-test-guided verification using the registered fingerprint for piracy judgment to prevent malicious accusations.   
• Extensive evaluations on seven deep neural networks over ten datasets demonstrate the effectiveness, robustness, and generalizability of DEEPREG, achieving 100% detection accuracy for pirated models without false positives.

# II. PRELIMINARIES AND RELATED WORK

# A. Deep Neural Networks

A neural network is a function $F _ { \theta } ( \mathbf { x } ) = \mathbf { y }$ that accepts an input x $\in \mathbb { R } ^ { n }$ and, following a series of computations by model layers characterized by parameters θ, ultimately generates an output $\mathbf { y } \in \mathbb { R } ^ { m }$ . These computations are generally divided into two steps: feature extraction G(·) and output mapping C(·). In a typical classification task, the output of the network is often computed using the softmax function, which ensures that the output vector y satisfies $0 \leq y _ { i } \leq 1$ and $\textstyle \sum _ { i = 1 } ^ { m } y _ { i } = 1$ . The vector y is thus treated as a probability distribution, $\mathrm { i . e . , } y _ { i }$ is the probability that input x has class i, and the predicted label for input x is $l = \mathrm { a r g } \operatorname* { m a x } _ { i } y _ { i }$ .

# B. Trusted Executed Environment

The trusted execution environment (TEE) [22] constitutes a secure processing domain where code can be isolated from other segments of the operating system. It helps code and data loaded inside it to be protected with respect to confidentiality and integrity. Intel Software Guard Extensions (SGX) [23] is a prominent implementation of TEE to facilitate secure computation on an untrusted platform. SGX establishes a protected segment of memory address space called an enclave, where code execution is shielded against external attacks. This technology assures both the confidentiality and integrity of code and data within the enclave, even under the threat posed by potentially malicious operating systems, hypervisors, or BIOS. Besides, SGX enables a third-party owner to initiate remote attestation to verify the hash of an enclave’s initial code and data.

# C. Model Watermarking and Fingerprinting

Model watermarking [7]–[11] embeds the additional ownerspecific information into the original model during the model training phase, which potentially sacrifices the utility of the model. This information can later be extracted by the model owner using a predefined method during the verification phase, serving as proof of ownership. However, performing an additional embedding phase for each released model is a burdensome task, and no external party can verify the authenticity of the embedding process.

In contrast, model fingerprinting techniques [13]–[19] construct the fingerprint based on the inherent properties of the model, which can uniquely represent the model and be bound to the owner to prove the model’s ownership. These approaches do not require modifications to the original model since they do not embed any additional information into the model. MetaFinger [17] generates many shadow models with Deep Neural Network (DNN) augmentation as meta-data and optimizes some images by meta-training to ensure that only models derived from the protected model can recognize them. Their method requires a protracted process of joint optimization on an ensemble of positive and negative models, which is an unrealistic expectation for regulatory authorities. SAC [19] calculates the output correlation using wrongly predicted or augmented samples and distinguishes pirated models with a preset threshold. These methods relying on specific labels or output probabilities become ineffective when the output format of the suspect model has changed.

Zheng et al. [13] suggest the creation of a DNN fingerprint by associating the model’s distinctive parameters with the owner’s identity through random projection. Their method relies on side-channel analysis techniques to extract the model weights from the suspect model for computation. However, this method only applies to models deployed at the edge, where their side-channel leakage can be measured. Although they introduce a trusted third party to register the fingerprint before deployment, it still cannot prevent dishonest owners from falsely registering non-existent fingerprints. The third party only plays a role in recording and certifying the registration time, ensuring that any similar fingerprints registered by others afterward are invalidated. However, the trusted third party cannot verify whether the submitted fingerprints were genuinely generated using the designated method due to the lack of supervision over the fingerprint extraction process. As a result, a malicious model owner could fabricate numerous nonexistent fingerprints for registration, leading to the invalidation of legitimate fingerprint registrations for other models.

Unlike previous methods, our framework necessitates only the model’s predicted label and is capable of identifying suspect models subjected to various alterations in model output formats. It employs TEE to resolve the trust issue between regulatory authorities and model owners, ensuring the authenticity of the fingerprint throughout both the generation and verification processes, thereby establishing a complete trust chain for model ownership regulation.

# III. PROBLEM DEFINITION

# A. Problem Statement

The regulation of ownership in the realm of DL models is a multi-party security game involving the model owner, the model user, and the regulator. Initially, the model owner dedicates substantial computing power and well-curated training data to develop models tailored for specific downstream tasks, crowning them as an inseparable part of their IP. In the current DL ecosystem, the model owner has the option to privately sell their models to end users or publicly release them online. However, dishonest users may unlawfully redistribute or redeploy these models, thereby infringing on the IP rights of the model owner. To counteract this issue, the model owner can entrust the regulator with providing model fingerprinting services for regulatory purposes. Such a service empowers the model owner to protect their IP rights through three stages: 1) Ownership Identification. The regulator extracts the fingerprint encoding the unique characteristics inherent to the original model M. 2) Suspect Detection. The model owner identifies a potentially infringing model S and submits its API to the regulator for piracy judgment. 3) Piracy Judgment. The regulator verifies the submitted API to determine whether the suspect model S is pirated from the original model M.

In this paper, we consider a practical scenario where the suspect model is deployed as a black box, concealing its internal configuration, including architecture and parameters, as well as training specifics, from users. To support a wide range of deployed models, we consider the model API outputs only the top-1 predicted label without probability information. This setting presents a significant challenge since the owner and the regulator can access very limited information from the model’s predictions. Nevertheless, it also makes our framework highly generalizable, as owners can still protect their IP even when they can only access the most basic APIs of suspect models.

# B. Threat Model

We consider potential threats and attacks from the perspective of each participant involved in the ownership regulation. We assume that the attacker could be a malicious model owner or user, or alternatively, a curious or disguised regulator.

Model owner side. We assume that the model owner can access specific model APIs normally. They may make substantial false claims about non-existent models to retain more forged fingerprints (T1). Additionally, they could exploit existing fingerprints to wrongfully accuse innocent parties who use irrelevant models (T2).

Model user side. We assume that the model user knows the fingerprinting method and gains access to partial training data. They may resell, redistribute, or redeploy the original model as a business service. To obscure the model’s true ownership, they could employ various post-processing techniques on the original model before deployment (T3). For the attack incentive to hold, we assume that the accuracy of post-processed models is not unduly compromised and the resource expenditure of postprocessing is reasonable. Typically, the attacker is motivated to respond to as many API queries as possible since more queries bring more profits. In efforts to evade piracy detection, attackers may pinpoint queries with underlying motives, providing manipulated responses accordingly (T4). Additionally, the model user may doubt or deny the authenticity of the fingerprinting services offered by the regulator (T5).

Regulator side. We assume that the regulator can access specific model APIs normally and hold similar public datasets. When the regulator attempts to identify a model’s ownership, there is a risk of disclosing confidential information, including the model’s code, weights, and parameters (T6). If attackers manage to impersonate the regulator, they can exploit the exposed information to unveil proprietary secrets of the model owner (T7). To be realistic, the regulator is presumed to possess only the access rights typical of a normal user concerning the suspect model, lacking the capability to directly probe or alter the model’s internal operations.

The considered scope of threat model. We assume that enclaves within the TEE are the only trustworthy components on each participant’s side, ensuring safety in terms of computation and memory footprint. The communication channel linking two enclaves is secured using RA-TLS [24], which leverages hardware-backed cryptographic keys housed within the TEE. Note that vulnerabilities to the underlying TEE, such as sidechannel attacks [25], [26], are out of scope for this paper.

# IV. DEEPREG DESIGN

# A. Design Goals

We design DEEPREG to achieve the following goals:

Non-forgeability (T1, T2) Our foremost goal is to thwart any attempts by attackers to fraudulently claim ownership, which could result in malicious accusations. DEEPREG should ensure the authenticity of each model undergoing ownership identification and the dependability of extracted fingerprints.

Non-repudiation (T3, T4, T5) The second goal is to furnish irrefutable proof of ownership. We aim to proactively identify the ownership of the original model and gather irrefutable evidence of infringement by the pirated model. DEEPREG should conduct covert forensics to prevent alerting the pirate, guaranteeing that the evidence remains factual and impartial.

Non-leakability (T6, T7) DEEPREG should protect the confidential information of the model owner. Data pertinent to the original model is processed exclusively on the owner’s device and not disclosed to external parties.

![](images/751683768c7ad25dbdd1245b803dcea344be8b496370a5aac266a60facecc2dd.jpg)



Fig. 1. Overall flow of DEEPREG.

# B. System Overview

Fig. 1 depicts the overall flow of DEEPREG. When a request to identify the ownership of model M is received, DEEPREG proceeds to extract the unique fingerprint of M within the model owner’s TEE. When the model owner identifies a suspect model S, DEEPREG undertakes the task of judging whether S is pirated from M using the model API. The regulatory process of DEEPREG is delineated into three stages:

1) Ownership Identification: DEEPREG crafts synthetic inputs designed to ensure that their feature maps, when processed by the feature extractor of the original model, closely resemble those of real inputs. As expected, these inputs will activate comparable outputs on the suspect model with the same feature extractor, thereby having a greater likelihood of receiving identical responses from the model API.   
2) Suspect Detection: The model owner engages in an iterative verification process to search for the suspect model S with extremely high confidence before submitting its API to the regulator. To prevent arbitrary false accusations, the model owner is required to submit the suspect API factually; otherwise, they will face penalties in the form of incrementally extended submit intervals and increased judgment expenses.   
3) Piracy Judgment: DEEPREG queries the API of the suspect model S with the registered fingerprint of the original model M and calculates the matching rate based on the responses obtained. Utilizing this matching rate, DEEPREG conclusively ascertains whether the suspect model S is a pirated derivative of the original model M.

# V. OWNERSHIP IDENTIFICATION

To achieve the ownership regulatory framework, we require an identification method that is compatible with various models and resilient to post-processing, serving as the infrastructure throughout the entire regulatory process. In this section, we delineate the motivation and design of the model fingerprinting method devised for DEEPREG.

# A. Fingerprint Design

1) Desiderata: The model fingerprint employed in the ownership regulation must fulfill the following criteria:

Use Compatibility (T3) The fingerprint should be applicable in a generalizable form to accommodate diverse modifications to the output format of the original model.

Collision Resistance (T2) The fingerprint should possess a discriminative nature, allowing it to effectively differentiate the original model from independently trained models.

Transfer Robustness (T3) The fingerprint should remain verifiable even when the original model is transferred to different domains. They should not be easily invalidated without causing an IP devaluation.

Identity Indiscernibility (T4) The fingerprint should have a distribution similar to normal inputs and contain authentic content, making them undetectable by anomaly detection.

2) Intuition: The optimization of the model training process utilizes stochastic elements, leading to diverse final neuron parameters, even in models independently trained from scratch for identical tasks. Consequently, the activations of these neurons are distinct, as are the activations of the feature extractor composed of these neurons. Importantly, varying feature extractors can generate unique feature maps for the same input, thereby enabling the generation of the distinctive fingerprint for the model. Given that the model’s functionality primarily relies on the feature representation for classification, if the inputs activate similar feature maps, they possess the potential to guide the model to produce the identical label [27]–[29], despite their ostensibly unrelated appearances. If we can craft synthetic inputs with feature maps closely resembling those of real inputs, the model will consistently produce the same labels through its classification layers. By utilizing input pairs derived from similar feature maps that share the same labels, we can effectively identify the model without being adversely impacted by alterations to the number and labels of output categories. In this way, we can overcome the challenge posed by modified black-box models, where fingerprint verification becomes problematic due to the changes in their output format.

3) Optimization Problem: We will formalize the methodology for fingerprint generation based on the aforementioned idea. Given an original model M with a feature extractor $\mathcal { G }$ and a real input x, our goal is to craft a synthetic input x′ that activates a feature map similar to that of the real input x, thereby yielding the identical output.

Definition 1 (Fingerprinting Pair). Suppose there is a pirated model P that incorporates the feature extractor $\mathcal { G }$ copied from the original model $\mathcal { M } ,$ along with newly trained classification layers C and an API $\mathcal { F } \left( \cdot \right)$ to access the pirated model ${ \mathcal { P } } _ { : }$ , which provides only the top-1 label as output. In this context, each real-synthetic pair $\langle { \pmb x } , { \pmb x } ^ { \prime } \rangle$ will activate similar outputs on the pirated model as $\begin{array} { r } { \mathcal { P } \left( \pmb { x } ^ { \prime } \right) = \mathcal { C } \left( \mathcal { G } \left( \pmb { x } ^ { \prime } \right) \right) \approx \mathcal { C } \left( \mathcal { G } \left( \pmb { x } \right) \right) = \mathcal { P } \left( \pmb { x } \right) } \end{array}$ , resulting in $\mathcal { F } \left( { \pmb x } ^ { \prime } \right) = \mathcal { F } \left( { \pmb x } \right)$ on the API. We refer to the input pair $\langle { \pmb x } , { \pmb x } ^ { \prime } \rangle$ as a fingerprinting pair.

Therefore, the generation of a fingerprinting pair can be formulated as an optimization problem as follows:

$$
\mathbf {x} ^ {\prime} = \underset {\mathbf {x}} {\arg \min} \| \mathcal {G} (\mathbf {x}) - \mathcal {G} \left(\mathbf {x} _ {1}\right) \| _ {2} + \lambda \| \mathbf {x} - \mathbf {x} _ {2} \| _ {2}, \tag {1}
$$

$$
\mathrm{s.t.} \mathbf {x} \in [ 0, 2 5 5 ] ^ {c \times w \times h}, \mathcal {F} (\mathbf {x} _ {1}) \neq \mathcal {F} (\mathbf {x} _ {2}),
$$

where $\mathcal { G } ( \cdot )$ and $\mathcal F ( \cdot )$ denote the feature extractor and predicted label of the original model, respectively, and λ represents the trade-off parameter. $\mathbf { X } _ { 1 }$ corresponds to the selected real input whose feature maps are employed for emulation purposes, $\mathbf { X } _ { 2 }$ corresponds to a randomly selected normal input whose predicted label differs from $\mathbf { X } _ { 1 } .$ , and $c ,$ w and h signify the number of channels, width, and height of the input, respectively. The former term ensures that the feature map extracted from the generated synthetic input is similar to the target feature map, while the latter term ensures that the synthetic input is indistinguishable from the real input.

![](images/00a300d8219a282fad36b32be4bada5219c04c5f7d7d67df0cc883cf5c6c1131.jpg)



Fig. 2. Details of synthetic inputs crafting.

For the constrained optimization problem Equation 1, we adopt the change-of-variables strategy [29], [30] by introducing a new variable w and setting

$$
\mathbf {x} = \frac {2 5 5}{2} (\tanh (\mathbf {w}) + 1). \tag {2}
$$

Given that $- 1 \le \mathrm { t a n h } ( \mathbf { w } ) \le 1$ , it consequently holds that $- 1 \leq \frac { 2 \mathbf { x } } { 2 5 5 } - 1 \leq 1$ , rendering $0 ~ \leq ~ \mathbf { x } ~ \leq ~ 2 5 5$ . Thus, the solution automatically satisfies the constraints, permitting the application of alternative optimization algorithms that do not inherently accommodate box constraints. For initial values of synthetic inputs with predicted labels differ from real inputs, the original problem Equation 1 can be converted to

$$
\mathbf {w} ^ {\prime} = \underset {\mathbf {w}} {\arg \min} \left\| \mathcal {G} \left(\frac {2 5 5}{2} (\tanh (\mathbf {w}) + 1)\right) - \mathcal {G} \left(\mathbf {x} _ {1}\right) \right\| _ {2} + \lambda \left\| \frac {2 5 5}{2} (\tanh (\mathbf {w}) + 1) - \mathbf {x} _ {2} \right\| _ {2}. \tag {3}
$$

We use the Adam optimizer [31], a gradient descent algorithm with a fast convergence rate at finding adversarial examples [30], to solve this problem. After obtaining the synthetic input $\mathbf { x } ^ { \prime } ,$ , we will assess whether $\mathcal { F } ( \mathbf { x } ^ { \prime } ) = \mathcal { F } ( \mathbf { x } _ { 1 } )$ for the candidate. Should this condition be met, $< { \bf x } _ { 1 } , { \bf x } ^ { \prime } >$ can then serve as a fingerprinting pair for the original model, otherwise $\mathbf { x } ^ { \prime }$ has to be discarded to generate a new one.

4) Selection Strategy: While the one-to-one input pair approach can adapt to modifications in the model’s output format, relying solely on a single chosen feature extractor may not sufficiently counteract pirates’ alterations to the model’s internal structure. Consequently, it becomes imperative to choose a range of feature extractors within the original model and create multiple synthetic inputs corresponding to each real input, thereby constructing a more robust fingerprint, as depicted in Fig. 2. To this end, DEEPREG selects $N$ real inputs and generates K synthetic inputs for each real input (in total, there are $N * ( K + 1 )$ ) inputs). When a real-synthetic input pair is fed into the suspect model, and if the count of synthetic inputs sharing the same predicted label as the real input meets or exceeds half of the total synthetic inputs $( i . e . , K / 2 )$ , this real-synthetic pair is deemed to be a match. The matching rate, defined as the proportion of matched real-synthetic pairs within a fingerprint, is utilized to ascertain the potential piracy relationship between the suspect model and the original model.

For optimal efficiency, DEEPREG must carefully select specific values of N and K for a given original model M that minimize the fingerprinting cost while concurrently adhering to the security demands. We denote this requirement as the cost requirement. Notably, both the computation and communication costs associated with each fingerprinting service are directly proportional to the number of selected real inputs $N$ and the number of synthetic inputs K generated for each real input. Therefore, DEEPREG faces a parameter optimization problem that necessitates simultaneously meeting the security and cost requirements.

We initiate our discussion with the security requirement. The pirate may successfully evade fingerprint verification under two distinct conditions: 1) by accurately determining the K positions of the feature extractors used for fingerprinting and subsequently conducting adversarial training at those precise locations in the pirated model, or 2) by correctly pinpointing NK synthetic inputs among all queries and responding distinctively to these queries. Without loss of generality, we further define these two potential scenarios mathematically.

Guessing the positions of the chosen feature extractors: For the sake of simplification, we assume that the pirate knows K and N . Considering the pirate’s limited capabilities and their intention to minimally impact the original model’s performance with reasonable time and effort, we assume that they will seek to alter the pirated model by speculating on the positions of the K feature extractors used for fingerprint generation. Let $E _ { K }$ denote the event where the pirate conducts adversarial training at all K designated positions of the pirated model, which has L possible positions for attack. Therefore, the probability $\mathrm { P r } [ E _ { K } ]$ that event $E _ { K }$ occurs is as follows:

$$
\operatorname * {P r} \left[ E _ {K} \right] = \binom {L} {K} ^ {- 1} = \frac {K ! (L - K) !}{L !}. \tag {4}
$$

Identifying the synthetic inputs among all queries: To further simplify, we assume that the pirate has been able to identify precisely $N K + N$ fingerprint queries from all queries. For successful evasion of fingerprint verification, they should perform normal inference for the N real inputs in the disorderly queries, and provide tampered results for the N K synthetic inputs, deviating from the original model’s outputs. Let $E _ { N }$ denote the event where the pirate’s chosen NK tampered inferences exactly align with the synthetic inputs. The probability Pr $[ E _ { N } ]$ of event $E _ { N }$ occurring is as follows:

$$
\operatorname * {P r} \left[ E _ {N} \right] = \binom {N K + K} {N K} ^ {- 1} = \frac {(N K) ! K !}{(N K + N) !}. \tag {5}
$$

Given that the pirate’s success depends on achieving one of these two conditions, combining Equation 4 and Equation $5 ,$ the probability $\mathrm { P r } _ { s }$ of the pirate’s success in evading fingerprint verification is as follows:

$$
\begin{array}{l} \operatorname * {P r} _ {s} = \operatorname * {P r} \left[ E _ {K} \cup E _ {N} \right] = \operatorname * {P r} \left[ E _ {K} \right] + \operatorname * {P r} \left[ E _ {N} \right] - \operatorname * {P r} \left[ E _ {K} \right] \times \operatorname * {P r} \left[ E _ {N} \right] \\ = \frac {K ! (L - K) !}{L !} + \frac {(N K) ! K !}{(N K + N) !} - \frac {K ! (L - K) ! (N K) ! K !}{L ! (N K + N)) !}. \tag {6} \\ \end{array}
$$

The security requirement states that Prs should be no more than $2 ^ { - \gamma }$ for any set of values for N and K selected by the regulator. Building on this requirement, another goal is to identify the optimal N and K that fulfill the cost requirement (i.e., resulting in the minimal expense for generating and verifying the model fingerprint). We denote a cost function $C o s t ( K , N ) = N ( K + 1 )$ , which represents the total cost of the fingerprinting service for each model. Specifically, the parameter optimization problem is required to uphold the security constraint $\mathrm { P r } _ { s } \ \le \ 2 ^ { - \gamma }$ , while endeavoring to minimize the cost function Cost(K, N). Therefore, the parameter optimization problem can be expressed as follows:

Algorithm 1: Searching optimized parameters   
Input: Original model: M
Security parameter: γ, Number of queries: Q
Output: Optimized parameters: $K^{*}, N^{*}$ $L \leftarrow \text{DetectExtractor}(M)$ ;
for K = 2 to L do
    for N = 1 to +∞ do
    if $N(K + 1) > Q$ or $\Pr(K, N, L) \leq 2^{-\gamma}$ then
    break;
    if $N(K + 1) \leq Q$ and $\text{Cost}(K, N) < C^{*}$ then $K^{*} \leftarrow k, N^{*} \leftarrow N, C^{*} \leftarrow \text{Cost}(K, N)$ ;
return $K^{*}, N^{*}$ ;

$$
\underset {N, K} {\arg \min} N (K + 1), \quad \text { s.t. } \quad \operatorname * {P r} _ {s} \leq 2 ^ {- \gamma}. \tag {7}
$$

To identify the optimal N and K that meet the security requirement while ensuring minimized yet adequate cost, we design a search algorithm (illustrated in Algorithm 1) based on the probability constraint and cost function. For a specific original model M, the goal is to identify an optimal pair $( K ^ { * } , N ^ { * } )$ that minimizes the cost function $C o s t ( K , N ) = N ( K + 1 )$ while satisfying the security requirement (i.e., $\mathrm { P r } _ { s } \ \le \ 2 ^ { - \gamma } )$ . In detail, for every possible value of K ranging from 2 to $L ,$ the search involves finding an N for a specified K until the smallest N meeting the security requirement is located (the total cost declines as N decreases). During this procedure, we continuously explore and update the optimal pair $( K ^ { * } , N ^ { * } )$ with the current pair (K, N ) if the latter offers more total cost savings than the former. The algorithm ultimately culminates in establishing the optimal pair that minimizes the total cost while upholding the security requirement. In cases where a query limit Q is imposed, Algorithm 1 can be employed to determine the optimal parameters under the constraint $N ( K { + } 1 ) \le Q$ , adapting to changes in API access restrictions.

Finally, we determine the K feature extractors within the internal structure of the original model. As summarized in prior research [27], [29], early model layers are known to extract more generic visual features from inputs, such as edges, points, and textures. Only if the synthetic inputs contain sufficient visual details and local patterns can they activate similar low-level features with the real inputs. In an extreme case, if we designate only the input layer as a feature extractor and utilize a real input to fabricate the synthetic input, the result tends to be a duplication of the real input. Such a setting is likely to elicit matched responses even from irrelevant models, thus failing to satisfy the desiderata for collision resistance in the model fingerprint. Conversely, the model’s deeper layers are responsible for extracting more complex and abstract features, such as intricate patterns, objects, and even conceptual elements, embodying the specialized knowledge acquired by the original model from its training data. Features from these deeper layers encapsulate insights into how the original model processes and refines information from inputs, making them crucial for generating distinctive fingerprints. Therefore, we strategically position feature extractors at random points within the original model structure, from the hidden layers following the input layer to just before the output layer, to thwart the pirate from predicting the selection pattern. Considering that the removal of more deep layers exerts a more pronounced effect on the model and concurrently heightens the challenge for the pirate to fine-tune the model, we use the normalized exponential function to assign the selection probability Pi to the middle layers of the original model with index i

$$
\mathrm{P} _ {i} = \frac {\mathrm{e} ^ {i}}{\sum_ {j = 2} ^ {l - 1} \mathrm{e} ^ {j}}, \tag {8}
$$

where l is the number of all model layers.

# B. Fingerprint Extraction

In DEEPREG, the fingerprinting and identification enclaves are designated to oversee the process of ownership identification. During the fingerprint extraction phase, we need to consider threats emanating from both the model owner (T1) and the regulator (T5-T7). In response to these threats, DEEPREG incorporates two design components rooted in confidential computing, which are applied during the execution of multiple enclaves across various devices, as shown in Fig. 3.

Fingerprint Certification. The fingerprinting enclave on the model owner’s side ensures that the fingerprint extracted from the original model is well-founded, while simultaneously protecting model confidentiality and data privacy. The procedure of fingerprinting the original model encompasses several steps: weight loading, extractor finalizing, real input selection, and synthetic input generation. Initially, the enclave loads the model weights to prevent any forging or tampering by the attacker, thereby safeguarding the integrity and trustworthiness of the process for the regulator (T1). Following this, the enclave finalizes K feature extractors based on our selection strategy in §V-A4. The diverse feature extractors selected through this strategy serve as a defense against malicious users who may attempt to manipulate the model’s internal structure to evade piracy detection.

To mitigate the risk of real input leakage, which could enable an attacker to conduct targeted adversarial training and thereby obscure feature map similarity, DEEPREG adopts a secure transmission approach RA-TLS [24]. The communication between the fingerprinting and identification enclaves is encrypted to prevent data exposure during transmission: encrypted data are sent and decrypted within a hardware enclave via a secure channel established after enclave attestation. Instead of selecting inputs from the unprotected memory of the model owner, DEEPREG covertly transmits real inputs from the regulator’s input pool to the model owner’s enclave through the secure transmission channel (T6). The enclave then proceeds to generate synthetic inputs from these selected real inputs, forming real-synthetic input pairs that constitute the model fingerprint, as elaborated in §V-A3. Upon the fingerprint extraction, the identification enclave on the regulator’s side timestamps the fingerprint and registers the fingerprint certificate bound with the model owner’s identity. The certificate serves as irrefutable proof of ownership in case of disputes. Even if an attacker manages to fabricate an alternative ownership proof from a pirated model, this proof cannot possess a certified timestamp that is chronologically earlier than that of the original creation (T5).

![](images/2892b218631fa64d4b266d811746d412364b3703b1f4a5176124e2bc34ce0181.jpg)



Fig. 3. DEEPREG framework.

Attestation and Scrutiny. To initiate a fingerprint certification request, the model owner should commence the enclave attestation procedure between the fingerprinting and identification enclaves. The remote attestation confirms the legitimacy of the enclave publisher, thus thwarting attempts by attackers to masquerade as the regulator (T7), and verifies the integrity of initial code and data contents, preventing attackers from tampering with the enclave and fabricating non-existent fingerprints (T1). In DEEPREG, both the model owner and regulator mutually perform enclave attestation to authenticate each other’s identities. Once initialized, the enclave’s execution is protected by the processor hardware and isolated from the operating system and other software. Given that the initial code of the fingerprinting enclave is transparent and subject to inspection by the model owner, they can ascertain that only the fingerprinting results are disclosed to the regulator during the process of ownership identification (T6). Moreover, public scrutiny of the identification enclave enables the model user to validate the integrity of their target regulator’s enclave. By combining this transparency with remote attestation, they can validate the authenticity of the ownership identification conducted by the regulator. Should the regulator attempt any unauthorized changes to the ownership identification procedure, the model user will immediately detect a compromise in the integrity of the certification by comparing it with the publicly scrutinized code. The timestamped fingerprint certificates preserved within the identification enclave are impervious to tampering or fabrication since the identification enclave must be subject to public scrutiny and remain immutable (T5). Note that these fingerprint certificates are implemented based on the standard cryptographic libraries (e.g., OpenSSL); therefore, allowing public scrutiny does not reveal the regulator’s secrets.

To enable DEEPREG to adapt to models of varying scales without being constrained by the secure memory size of the TEE, we draw inspiration from Occlumency [32] and incorporate similar memory optimization techniques during the process of fingerprint extraction. For a given original model on the owner’s device, DEEPREG dynamically loads needed model weights layer by layer into the enclave to finalize feature extractors. When generating real-synthetic input pairs,

DEEPREG partitions convolutions into multiple matrix multiplications until the memory requirement is within the available memory space and promptly releases the stored feature maps once they have been used the pre-calculated number of times. Additionally, with the advent of CPUs supporting SGXv2, the memory capacity of enclaves can be expanded up to 512 GB [33]. Therefore, the memory limitations of TEE will not pose a barrier to the practical deployment of DEEPREG.

# VI. SUSPECT DETECTION

Another pivotal challenge in model ownership regulation involves discerning suspect models among numerous instances that offer only APIs without revealing their internal structures. In this section, we introduce an iterative verification methodology underpinned by Bayes’ theorem [21] for well-grounded detection of suspect models, thereby preventing erroneous accusations against innocent parties (T2).

# A. Prior Probability Table Construction

Owing to the unique characteristics of feature extractors, it is expected that the fingerprint will typically exhibit a higher matching rate on pirated models and a lower matching rate on irrelevant models. Nonetheless, in certain versions of pirated models and irrelevant models, there may occur an overlap between their matching rates. Inspired by the encoding method [16], we utilize Bayes’ theorem to encode and verify the fingerprint, thereby enhancing the confidence level for uncertain detection results by multiple iterations.

In light of the potential overlap interval, the matching rates are divided into three bins: [0, min), [min, max] and (max, 1], where min and max represent the lower and upper bounds of the overlap interval, respectively. Considering that the matching rate for a given positive suspect model invariably exceeds the range [0, min) and the matching rate for a given negative suspect model always remains below the range (max, 1], the middle interval [min, max] can be further segmented to diminish the number of iterations required in the detection process. This interval is divided into equal subintervals, ensuring uniformity in the range of each bin. With these segmented bins, a prior probability table correlating the matching rates to the original model can be established, facilitating the probability calculation for an unseen fingerprint.

Initially, the model owner constructs M suspect models, comprising $M _ { 1 }$ positive models and $M _ { 2 }$ negative models, derived from the original model using publicly available data from the same domain as the owner’s training dataset. Additionally, $Q$ sets of fingerprints are generated and assessed against each suspect model to ascertain the bounds of the matching rates. This procedure completes the construction of the frequency table, with rows denoting pre-determined matching rate intervals and columns indicating the suspect models, encompassing both positive and negative classifications. These preparatory measures are one-off activities, rendering the finalized prior probability table reusable for future suspect detection efforts. By pre-capturing a prior probability table for the matching rates of model fingerprints, the model owner can ascertain a confidence level to determine whether a suspect model is pirated from the original model.

# B. Iterative Verification

To improve the distinction between positive and negative suspect models, we adopt an iterative process for deriving the prediction with either extremely high confidence, signifying a strong likelihood of the suspect model being pirated, or extremely low confidence, pointing to a significant chance of the suspect model being innocent. As delineated in Algorithm 2, for a suspect model S, the model owner conducts the iterative verification process to compute a probability $P ,$ serving as the confidence level of the suspect model S being a pirated or altered version of the original model $\mathcal { M } .$ .

Under the detection criteria specified by the model owner and the submission guidelines imposed by the regulator, thresholds delineating the confidence level as either positive or negative are set at $\tau _ { p o s }$ and $\tau _ { n e g } .$ , respectively. If $P \ge \tau _ { p o s } , S$ is predicted to bear a resemblance to M with high confidence, and S is claimed to be a positive suspect model. The model owner is then advised to forward the API of this model to the regulator for conclusive piracy judgment. Conversely, if $P \leq \tau _ { n e g } , S$ is deemed unrelated to M with high confidence and thus categorized as a negative suspect model. In this case, the model owner should refrain from submitting the model API to the regulator, pending the identification of a positive suspect model, to avert potential regulatory penalties. In scenarios where $\tau _ { n e g } < P < \tau _ { p o s } .$ , the confidence level is insufficient to either confirm or refute that $s$ as a pirated copy of M. Consequently, another set of real inputs will be randomly selected to generate a new fingerprint from M. The newly generated fingerprint, together with the preceding ones, is employed to recalibrate the probability P . This iterative procedure continues until P falls into either $[ \tau _ { p o s } , 1 ]$ or $[ 0 , \tau _ { n e g } ]$ ].

Definition 2 (Matching Rate). Consider the fingerprint of M, comprising N fingerprinting pairs, represented as follows:

$$
f _ {\mathcal {M}} = \left\{\left\langle \boldsymbol {x} _ {i}, \left\{\boldsymbol {x} _ {i j} ^ {\prime} \right\} _ {j = 1} ^ {K} \right\rangle \right\} _ {i = 1} ^ {N}, \tag {9}
$$

where $ { \boldsymbol { { x } } } _ { i j } ^ { \prime }$ denotes the j-th synthetic input for the i-th real input xi. A fingerprinting pair is designated as a matched fingerprinting pair if at least half of its synthetic inputs yield the same response as the real input. Therefore, the matching rate of the fingerprint is calculated as $\frac { m } { N }$ , where

$$
m = \sum_ {i = 1} ^ {N} \mathbb {1} \left(\sum_ {j = 1} ^ {K} \mathbb {1} \left(\mathcal {S} \left(\boldsymbol {x} _ {i j} ^ {\prime}\right) = \mathcal {S} \left(\boldsymbol {x} _ {i}\right)\right) \geq \frac {K}{2}\right). \tag {10}
$$

Here, 1 (·) is the indicator function.

We regard the matching rate as a primary metric for quantifying the extent of alignment between the suspect model and the original model. Finally, P is calculated by applying the Bayes’ theorem [21]:

$$
P = p (p o s \mid \mathbf {r}) = \frac {p (p o s) p (\mathbf {r} \mid p o s)}{p (p o s) p (\mathbf {r} \mid p o s) + p (n e g) p (\mathbf {r} \mid n e g)}, \tag {11}
$$

where pos and neg signify the positive and negative classes, respectively, r is an interval vector $( r _ { 1 } , \dots , r _ { T } )$ and $r _ { i }$ indicates the interval of the matching rate for the i-th fingerprint.

Algorithm 2: Iterative verification process   
Input: Original model: M
Suspect model: S
Prior probability table: T
Output: Detection result
r ← ∅;
repeat
    f_M ← GenerateFingerprint(M);
    mr ← CalculateMatchingRate(S, f_M);
    r ← FindCorrespondingBin(mr);
    r.append(r);
    P ← CalculateProbability(T, r);
until $P \leq \tau_{neg}$ or $P \geq \tau_{pos}$ ;
if $P \geq \tau_{pos}$ then
    return True
else
    return False

Given that the matching rates across T fingerprints are independent, we can make the following derivation:

$$
p (\mathbf {r} \mid p o s) = p (r _ {1}, r _ {2}, \dots , r _ {T} \mid p o s) = \prod_ {i = 1} ^ {T} p \left(r _ {i} \mid p o s\right), \tag {12}
$$

which also applies to $p ( \mathbf { r } \mid n e g )$ .

Utilizing the prior probability table, which is based on predetermined intervals of matching rates with M suspect models (including $M _ { 1 }$ positive models and $M _ { 2 }$ negative models) crafted, Equation 11 can be simplified as follows:

$$
\begin{array}{l} P = \frac {\frac {M _ {1}}{M} \sum_ {j = 1} ^ {M _ {1}} \frac {1}{M _ {1}} p _ {j} (\mathbf {r} \mid \text {pos})}{\frac {M _ {1}}{M} \sum_ {j = 1} ^ {M _ {1}} \frac {1}{M _ {1}} p _ {j} (\mathbf {r} \mid \text {pos}) + \frac {M _ {2}}{M} \sum_ {j = 1} ^ {M _ {2}} \frac {1}{M _ {2}} p _ {j} (\mathbf {r} \mid \text {neg})} \tag {13} \\ = \frac {\sum_ {j = 1} ^ {M _ {1}} \prod_ {i = 1} ^ {T} p _ {j} (r _ {i} \mid p o s)}{\sum_ {j = 1} ^ {M _ {1}} \prod_ {i = 1} ^ {T} p _ {j} (r _ {i} \mid p o s) + \sum_ {j = 1} ^ {M _ {2}} \prod_ {i = 1} ^ {T} p _ {j} (r _ {i} \mid n e g)}, \\ \end{array}
$$

where $p _ { j } \left( r _ { i } \mid p o s \right)$ and $p _ { j } \left( r _ { i } \mid n e g \right)$ denote the probability of the matching rate falling within the interval $r _ { i }$ for the j-th positive suspect model and the j-th negative suspect model, respectively.

# VII. PIRACY JUDGMENT

Considering potential threats from the model user (T4, T5), DEEPREG enables a conclusive piracy judgment on the submitted APIs to provide irrefutable proof of ownership, which includes two steps: preparation of indistinguishable queries and the subsequent analysis of their responses.

# A. Query Preparation

Since we intentionally select the initial values for synthetic inputs from normal inputs and constrain their range of variation, synthetic inputs appear identical to normal inputs for suspects. However, unprocessed consecutive fingerprint queries will still exhibit obvious statistical characteristics due to their identical predicted labels. Once these queries are discernible to the suspect, they can evade the regulation by returning manipulated responses, which deviate from the genuine outputs for these specific inputs.

![](images/0d7290966f111d202662bb9374dfc4e97d2f6cd9e8729cbfdb06d906426935fa.jpg)



Fig. 4. Pre-processing of fingerprint samples.

To mitigate this issue, DEEPREG tailors the mix-and-check method [34], designed originally to force the malicious server to perform correct inference, to prevent deceived responses from the suspect. Initially, the regulator collects public samples with known computation results, which is feasible given the abundance of diverse public datasets suitable for various applications. Furthermore, DEEPREG creates multiple copies of a particular public sample and integrates public samples with actual query samples of the registered fingerprint, as shown in Fig. 4. These public samples are used to verify the model accuracy and computation correctness at the same time, forcing the suspect to perform inference correctly. Additionally, DEEPREG randomizes the order of these mixed samples before feeding them to the submitted API. After shuffling irregularly, the finalized queries comprise non-consecutive fingerprint samples and public samples, effectively eliminating any potential associative patterns between adjacent queries.

Suspect APIs, essentially designed for commercial services, rely on producing more high-quality responses to maximize profits. As suspects cannot distinguish between genuine customers and regulators, they must maintain the accuracy of their services for sustained revenue. Moreover, only a small fraction of data from public datasets, such as 100 out of 1.4 million images from ImageNet, is used to assess model accuracy and computation correctness. It is impractical for suspects to match every query against the vast entirety of public datasets, particularly as public samples may also include manually annotated data not in these datasets.

# B. Response Analysis

When obtaining inference results on the mixed queries from the suspect API, DEEPREG assesses the model accuracy and computation correctness on the public samples. Specifically, the model accuracy η is defined as the proportion of correct inferences on pre-collected public samples. When η exceeds a predefined normal threshold, the model accuracy is deemed satisfactory. In cases where responses from duplicate samples are inconsistent, it is inferred that the suspect has attempted to mislead the regulator with manipulated results. Only if both the model accuracy and computation correctness checks are successfully cleared, does DEEPREG proceed to compute the matching rate for fingerprint samples; otherwise, the process is terminated.

Furthermore, we develop a hypothesis-test-guided method for the regulator to render the piracy judgment process more robust. We hypothesize an extreme scenario where the suspect model S possesses no prior knowledge about the inputs, following the pre-processing of queries. S arbitrarily categorizes

![](images/8952e735609e4988c47fb9484b152b46fa423df8083f4da2a2dc253ba69aece9.jpg)



(a) ResNet34 on ImageNet

![](images/63f670e888268f076880c36057e2096250e891d6fb629cf695348fea34feb1e0.jpg)



(b) VGG16 on ImageNet

![](images/859d0843fda6831eb7c9137210b7a59368aacbdd270c978e456def22e9ac2374.jpg)



(c) MobileNetV2 on ImageNet   
Fig. 5. Matching rate for various suspect models across 100 fingerprints of original models trained on ImageNet. Positive suspect models (labeled as “Positive”) are post-processed models with various modifications to the original model, while negative suspect models (labeled as “Negative”) comprise irrelevant models with different architectures or independently trained, including ResNet34, ResNet50, VGG16, VGG19, MobileNetV2, DenseNet121, and DenseNet169.

the input space into c classes, which we call an irrelevant model. To assess the likelihood of getting expected matching on the fingerprinting pairs, we establish the following of fingethe API $\bar { \mathcal { F } } \left( \cdot \right) , \left\{ \left. \mathbf { x } _ { i } , \left\{ \mathbf { x } _ { i j } ^ { \prime } \right\} _ { j = 1 } ^ { K } \right. \right\} _ { i = 1 } ^ { N }$ and nD $\left\{ \left. y _ { i } , \left\{ y _ { i j } ^ { \prime } \right\} _ { j = 1 } ^ { K } \right. \right\} _ { i = 1 } ^ { N }$ , we , we i=make the following hypothesis:

$H _ { 0 } : S$ is an irrelevant model.

$H _ { 1 } : S$ is not an irrelevant model.

Under the hypothesis, we can establish a sufficient condition to reject the null hypothesis $H _ { 0 }$ with a pre-determined significance value α.

Theorem 1. Given the c-class classification suspect model S in top-1 label exposure, a fingerprinting statistical hypothesis $( H _ { 0 } , \ H _ { 1 }$ , as well as the significance value $\alpha ) ,$ the size of matched fingerprinting pairs sufficient to reject the null hypothesis $H _ { 0 }$ with the significance value α is $\lceil \log _ { z } \beta \rceil$ , where $\begin{array} { r } { z = \binom { K } { K / 2 } \left( \frac { 1 } { c } \right) ^ { \frac { K } { 2 } } a n d \beta = \frac { \alpha } { \binom { N } { \lceil N / 2 \rceil } } . } \end{array}$

Proof. See Appendix A.

Theorem 1 implies that if the size of matched fingerprinting pairs is larger than a threshold, the regulator can reject the null hypothesis $H _ { 0 }$ at the significance level α with the registered fingerprint of the original model. In other words, the regulator can make the final judgment that the suspect model is pirated from the original model with $1 - \alpha$ confidence when the size of matched fingerprinting pairs within the fingerprint is large enough. According to Theorem 1, we can find that when c increases, we will get a lower bound of the size of matched fingerprinting pairs. This suggests that learning tasks with more classes tend to have a smaller requirement for the number of fingerprinting pairs successfully matched. We set a strict significance level $\alpha = 0 . 0 1$ to increase confidence in the piracy judgment. Given a fingerprint with $N = 1 0$ and $K = 4$ , we can calculate the threshold values $\lceil \log _ { z } \beta \rceil$ of 4 and 2 for suspect models with 10 classes and 100 classes, respectively.

In DEEPREG, only model owners who have passed ownership identification are granted the right to accuse suspect models to regulators. To deter them from indiscriminately submitting suspect APIs to make malicious accusations, DEEP-REG incorporates a penalty mechanism for submissions that fail the judgment process. This ensures the legitimacy of the accusations and averts the squandering of regulatory resources. If the suspect API provided by the model owner does not meet the criteria set by the regulator, DEEPREG deems the accusation unsuccessful. As a punishment, the model owner faces restrictions on their right to make further accusations, leading to delays and increased costs for subsequent accusations. Notably, the waiting period and judgment expenses escalate significantly with each successive failure, ultimately resulting in disqualification. Therefore, unfounded accusations against innocent models not only obstruct their legitimate right to protect their models but also harm their interests.

# VIII. EVALUATION

We evaluate the effectiveness, robustness, and generalizability of DEEPREG with various DL models. We also assess the total runtime of DEEPREG in practice and analyze the impact of different settings on its detection performance.

# A. Experimental Setup

We have implemented DEEPREG based on PyTorch and Intel SGXv1. For actual deployment, we utilize a Linux laptop with an Intel Core i5-7300HQ CPU, an NVIDIA GTX 1060 GPU, and 8 GB RAM on the model owner’s side. On the regulator’s side, we employ a Linux server equipped with an Intel Xeon E5-2650 CPU, an NVIDIA TITAN X GPU, and 128GB RAM. We use a total of five image classification datasets including CIFAR-10, CIFAR-100 [35], Tiny-ImageNet [36], Flowers-102 [37] and MNIST [38]. Several well-known DNNs, including VGG [39], ResNet [40], MobileNet [41] and DenseNet [42] are evaluated. We set the trade-off parameter $\lambda = 0 . 1$ , the security parameter $\gamma = 1 5 .$ , the number of synthetic inputs generated for each real input $K \ = \ 4$ , the number of fingerprinting pairs $N ~ = ~ 1 0$ , the detection thresholds $\tau _ { p o s } = 0 . 9 5$ and $\tau _ { n e g } = 0 . 0 5$ , and the significance value $\alpha = 0 . 0 1$ .

Three well-trained DNNs for ImageNet [43] from the opensourced model zoo [44] are used as the original models: VGG16, ResNet34, and MobileNetV2. Pirated models are derived by post-processing these original models for the same application or adapting them through transfer learning for different applications. The post-processing techniques considered in this paper include fine-tuning (FT), adversarial training (AT), feature extraction (FE), and weight pruning (WP). For FT, we update all the parameters of the model for ten epochs. For AT, the model undergoes retraining with an augmented dataset that includes slightly modified versions of the original inputs. For FE, the last b blocks of the model are removed, excluding the output layer. For WP, the p fraction of model weights with the smallest absolute values are pruned.

TABLE I TRUE POSITIVE RATE AND FALSE POSITIVE RATE FOR THE PIRACY JUDGMENT OF SUSPECT MODELS. 

<table><tr><td rowspan="2">Model</td><td colspan="3">DeepReg</td><td colspan="3">SAC [19]</td><td colspan="3">MetaFinger [17]</td><td colspan="3">DNN FP [13]</td></tr><tr><td>CIFAR-10</td><td>CIFAR-100</td><td>TinyImagenet</td><td>CIFAR-10</td><td>CIFAR-100</td><td>TinyImagenet</td><td>CIFAR-10</td><td>CIFAR-100</td><td>TinyImagenet</td><td>CIFAR-10</td><td>CIFAR-100</td><td>TinyImagenet</td></tr><tr><td>ResNet34</td><td>100% / 0%</td><td>100% / 0%</td><td>100% / 0%</td><td>100% / 25%</td><td>100% / 50%</td><td>86% / 63%</td><td>93% / 11%</td><td>93% / 10%</td><td>93% / 10%</td><td>99% / 1%</td><td>99% / 1%</td><td>99% / 1%</td></tr><tr><td>VGG16</td><td>100% / 0%</td><td>100% / 0%</td><td>100% / 0%</td><td>86% / 50%</td><td>71% / 50%</td><td>75% / 63%</td><td>90% / 8%</td><td>92% / 10%</td><td>94% / 10%</td><td>99% / 3%</td><td>99% / 3%</td><td>99% / 3%</td></tr><tr><td>MobileNetV2</td><td>100% / 0%</td><td>100% / 0%</td><td>100% / 0%</td><td>100% / 13%</td><td>100% / 38%</td><td>100% / 50%</td><td>91% / 13%</td><td>94% / 13%</td><td>96% / 14%</td><td>98% / 3%</td><td>98% / 3%</td><td>98% / 3%</td></tr></table>

TABLE II MATCHING RATE RANGE AND AVERAGE MATCHING RATE FOR SUSPECT MODELS AFTER TRANSFERRING TO DIFFERENT TASKS. 

<table><tr><td>Type</td><td colspan="2">Models</td><td>CIFAR-10 → MNIST</td><td>CIFAR-100 → Flowers-102</td></tr><tr><td rowspan="8">Positive</td><td rowspan="5">FE</td><td>FT</td><td>[0.80, 0.89], 0.8500</td><td>[0.70, 0.83], 0.7814</td></tr><tr><td>AT</td><td>[0.69, 0.78], 0.7457</td><td>[0.65, 0.76], 0.6986</td></tr><tr><td>b=1</td><td>[0.81, 0.88], 0.8529</td><td>[0.75, 0.82], 0.7871</td></tr><tr><td>b=2</td><td>[0.74, 0.90], 0.8286</td><td>[0.76, 0.83], 0.7900</td></tr><tr><td>b=3</td><td>[0.71, 0.85], 0.7971</td><td>[0.66, 0.77], 0.7100</td></tr><tr><td rowspan="3">WP</td><td>p=0.1</td><td>[0.80, 0.89], 0.8543</td><td>[0.71, 0.82], 0.7814</td></tr><tr><td>p=0.2</td><td>[0.79, 0.88], 0.8514</td><td>[0.71, 0.82], 0.7786</td></tr><tr><td>p=0.3</td><td>[0.81, 0.89], 0.8471</td><td>[0.68, 0.82], 0.7700</td></tr><tr><td rowspan="8">Negative</td><td colspan="2">ResNet18</td><td>[0.21, 0.31], 0.2443</td><td>[0.05, 0.11], 0.0771</td></tr><tr><td colspan="2">ResNet34</td><td>[0.13, 0.28], 0.2057</td><td>[0.02, 0.08], 0.0457</td></tr><tr><td colspan="2">ResNet50</td><td>[0.16, 0.27], 0.2143</td><td>[0.01, 0.03], 0.0271</td></tr><tr><td colspan="2">VGG16</td><td>[0.13, 0.22], 0.1857</td><td>[0.06, 0.16], 0.0957</td></tr><tr><td colspan="2">VGG19</td><td>[0.13, 0.22], 0.1629</td><td>[0.01, 0.03], 0.0171</td></tr><tr><td colspan="2">MobileNetV2</td><td>[0.24, 0.38], 0.2900</td><td>[0.00, 0.03], 0.0100</td></tr><tr><td colspan="2">DenseNet121</td><td>[0.14, 0.27], 0.2071</td><td>[0.06, 0.11], 0.0871</td></tr><tr><td colspan="2">DenseNet169</td><td>[0.25, 0.41], 0.3200</td><td>[0.03, 0.07], 0.0486</td></tr></table>

# B. Effectiveness

This experiment assesses the ability to distinguish between pirated models and irrelevant models using generated fingerprints. To simulate adversaries utilizing transfer learning to alter the output of pirated models, we initially transfer these original models to the CIFAR-10 and CIFAR-100 datasets, respectively, thereby giving them different output formats (i.e., different numbers of categories and label names). Furthermore, four post-processing techniques (FT, AT, FE, WP) can be applied to these models with modified output formats. We evaluate the matching rate range and average matching rate for various suspect models, as illustrated in Fig. 5. We use 10 fingerprinting pairs as a fingerprint, and for each suspect model, we generate 100 different fingerprints for testing purposes. The results indicate that there is a significant gap in the matching rates of various original models’ fingerprints between positive suspect models and negative suspect models. This disparity is attributed to the strategic selection of model-specific feature extractors and the embedding of paired information during the fingerprint extraction process. As shown in Table I, DEEPREG achieves 100% detection accuracy for pirated models and produces no false positives for irrelevant models.

Besides collision resistance, we further investigate the statistical features of generated inputs to assess the identity indiscernibility of the model fingerprint. We profile the distribution of pixel values for the fingerprints of original models with different architectures and compare them with selected normal inputs, as shown in Fig. 6. It can be observed that the synthetic inputs within the fingerprint achieve a high level of similarity with normal inputs in terms of pixel statistics. Moreover, Fig. 7 shows the similarity distribution between synthetic inputs and corresponding normal inputs for 1000 fingerprinting pairs, further corroborating the indistinguishability between the generated synthetic inputs and normal inputs.

![](images/6b0a43fcbd2e9f85702abe6872399366db251946ab56c9740f428341e1318335.jpg)  
(a) ResNet34

![](images/3e64c0e99e8958ed1075deeba3a84b9daeaaec43b3f9847b30336920b21ddddc.jpg)  
(b) VGG16

![](images/083fa9e5e1f9bd58e0bfd766fd310b72503e523e627c96e33bd95685b73823ca.jpg)  
(c) MobileNetV2

Fig. 6. The distribution of pixel values of the first ten fingerprinting pairs of original models with three architectures. The left half of each violin plot represents the normal input, while the right half represents the synthetic input.   
![](images/b89870e4f6a99237cdac3aa6b6ad399d6b5f07c829e607d1e712cb0743347338.jpg)  
(a) ResNet34

![](images/f6b4acb31f9f74bab29384dbe4919e1f356e5e0811e38d4dcdf0070da3ed7cbb.jpg)  
(b) VGG16

![](images/22d0732e6a7e162cd5c9e189aec9336a9c0e8e133bbc6263b91b24aef87af5bf.jpg)  
(c) MobileNetV2   
Fig. 7. The similarity distributions between synthetic inputs and corresponding normal inputs. We use cosine similarity to quantify the similarity between two inputs, with values closer to 1 indicating greater closeness.

To better understand the practical effects of the generated fingerprints, we also exhibit some examples of 1-to-4 fingerprinting pairs, as shown in Fig. 8. Subfigures 8a, 8b, and 8c correspond to the fingerprinting pair for original models trained on ImageNet: ResNet34, VGG16, and MobileNetV2, respectively. On the left side is the selected real input, on the upper right side are randomly selected normal inputs, and on the lower right side are generated synthetic inputs. Due to Equation 1, the synthetic inputs generated from normal inputs still retain their authentic content after undergoing the optimization process. Besides, we can observe that as the block number increases, meaning the chosen feature extractor is closer to the input, the generated synthetic inputs become more similar in detail to the selected real input. The ability of synthetic inputs to closely resemble normal inputs in terms of content and statistics characteristics ensures that any attempts to detect fingerprint queries from the regulator become nearly impossible, strengthening the non-repudiation of DEEPREG.

# C. Robustness

In addition to post-processing in tasks with similar classes, we evaluate the matching rate of the fingerprint when the original model was transferred to different tasks. As shown in Table II, taking VGG16 as an example, we transfer the original models from the CIFAR-100/CIFAR-10 datasets to the Flowers-102/MNIST datasets, respectively. The original VGG16 models are trained to classify objects of multiple categories, while the transferred models are trained to classify objects within a specific domain, namely flowers and handwritten digits. The results demonstrate that even after transferring the original model to different domains, the proposed model fingerprint still distinctly characterizes the uniqueness of the original model. As the matching rates of fingerprints between positive and negative suspect models exhibit significant separation, they can effectively differentiate irrelevant models with different architectures or independently trained. It confirms that the model fingerprint maintains its effectiveness in identifying and distinguishing pirated models from irrelevant models, even after domain transfer.

![](images/bb7723b75b013b0460dbb640ff90602c89ddc1fffd032611392a47fc78303ea3.jpg)  
Fig. 8. Examples of 1-to-4 fingerprint pairs for image classification models.

Furthermore, we evaluate the robustness of DEEPREG against adaptive attacks where the adversary knows the proposed fingerprinting method. We assume a worst-case scenario in which the adversary gains access to 20% of the original training data. Under this scenario, two types of adaptive attacks are considered: the adaptive detector and the adaptive classifier. The former employs a threshold-based detection method that uses leaked samples to distinguish synthetic samples from normal samples, relying on detection criteria of input similarity. The latter involves a DNN-based classifier that performs binary classification on the leaked samples.

For threshold-based adaptive attacks, we compute the Structural Similarity Index Measure (SSIM) and Learned Perceptual Image Patch Similarity (LPIPS) between synthetic and normal samples as evaluation metrics for input similarity. As shown in Table III, the experimental results demonstrate a high similarity, with a mean SSIM of 0.96 and LPIPS of 0.07. To conclude, it is impractical to distinguish synthetic samples from normal samples using the threshold in terms of perceived or perceptual similarity. For DNN-based adaptive attacks, we employed leaked fingerprint samples and a ConvNeXt [45]

TABLE III INPUT SIMILARITY BETWEEN THE SYNTHETIC SAMPLES AND NORMAL SAMPLES FOR THE THRESHOLD-BASED DETECTOR. 

<table><tr><td>Datasets</td><td>CIFAR-10</td><td>CIFAR-100</td><td>Tiny-ImageNet</td><td>ImageNet-1K</td></tr><tr><td>Models</td><td>ResNet50 [46]</td><td>EfficientNetV2 [47]</td><td>Swin-L [48]</td><td>ViT-L [49]</td></tr><tr><td>SSMI</td><td>0.97</td><td>0.97</td><td>0.95</td><td>0.93</td></tr><tr><td>LPIP</td><td>0.08</td><td>0.08</td><td>0.07</td><td>0.05</td></tr></table>

TABLE IV PERFORMANCE OF THE ADAPTIVE CLASSIFIER. 

<table><tr><td>Datasets</td><td>CIFAR-10</td><td>CIFAR-100</td><td>Tiny-ImageNet</td><td>ImageNet-1K</td></tr><tr><td>Models</td><td>ResNet50 [46]</td><td>EfficientNetV2 [47]</td><td>Swin-L [48]</td><td>ViT-L [49]</td></tr><tr><td>Detection Rate</td><td>21.2% / 3.4%</td><td>21.8% / 3.7%</td><td>35.8% / 14.6%</td><td>46.4% / 18.4%</td></tr><tr><td>Service Accuracy</td><td>98.3% → 94.9%</td><td>92.3% → 88.9%</td><td>91.3% → 78.0%</td><td>85.9% → 70.1%</td></tr></table>

network to train a binary classifier designed to detect whether the current input belongs to the fingerprint samples before the pirated model makes a prediction. If the input is classified as a synthetic sample, the API returns an incorrect prediction; otherwise, it returns the correct result. Table IV presents the detection rate of this classifier for synthetic samples and the misidentification rate for normal samples, as well as the impact on the accuracy of the API service.

On the CIFAR-10 and CIFAR-100 datasets, due to the relatively low resolution of the input images, the differences between synthetic and normal samples are minimal. The adaptive classifier can only differentiate about 20% of the synthetic samples and return incorrect predictions. Our fingerprint method effectively resists such adaptive attacks, and DEEPREG maintains 100% detection accuracy for pirated models. On the Tiny-ImageNet and ImageNet-1K datasets, the detection rate of the adaptive classifier for synthetic samples increases, approaching random guessing (50%). In these cases, DEEPREG can still identify all pirated models by increasing the number of iterative rounds in the process of suspect detection. However, the attackers’ increased identification of synthetic samples comes at the cost of misclassifying normal samples. Even a 15% false positive rate causes a significant drop in the API’s service accuracy, from 91% to 78%. The demonstrated indistinguishability forces attackers to abandon detection efforts, as they cannot reliably identify synthetic samples, which is thwarted by the one-to-many fingerprint design and mix-and-check method, nor can they treat all queries as fingerprint queries without causing unacceptable service degradation, undermining profitability.

# D. Comparison

This section compares DEEPREG with the state-of-the-art model fingerprinting methods [13], [17], [19] and analyzes its total runtime in practice. Table V lists these methods and compares their verification requirement, detection accuracy, fingerprint size, time cost, suspect detection capability, and ownership traceability. We can observe that DEEPREG only requires the model’s predicted labels for verification, which is the easiest condition to meet among all methods. This also enables DEEPREG to have the capability for suspect detection across different applications and output formats. We define the “Detection Accuracy” as the percentage of correctly detected pirated models and the “False Positive Rate” as the percentage of irrelevant models that are incorrectly judged. DEEPREG is the only method that can achieve 100% detection accuracy for pirated models, with zero false positives for irrelevant models, as shown in Table V. Besides, the fingerprint size of 50 images is much smaller than other methods based on output probabilities [17], [19] since these methods require 100 images as the fingerprint data points in their experiments. The compact fingerprint reduces the storage requirement for registered model fingerprints and the transmission cost associated with ownership identification and verification. For the verification time of the method [13], our evaluation is conducted with direct access to the weights of the suspect model. However, in practical use, it is necessary first to employ side-channel attacks to analyze the weights of the suspect model, which is a time-consuming and unstable process. Moreover, DEEPREG features a dedicated stage for suspect detection, where many challenging models that have undergone significant modifications and cannot be accurately judged by other methods can ultimately yield wellsubstantiated results. Based on suspect detection and combined with ownership traceability, DEEPREG can provide irrefutable evidence for the model owner, leaving no escape for pirates.

TABLE V COMPARISON WITH MODEL FINGERPRINTING METHODS. 

<table><tr><td>Method</td><td>DeepReg</td><td>SAC [19]</td><td>MetaFinger [17]</td><td>DNN FP [13]</td></tr><tr><td>Requirement</td><td>Predicted label</td><td>Output Probability</td><td>Output Probability</td><td>Side-Channel Information</td></tr><tr><td>Detection Accuracy</td><td>100%</td><td>91%</td><td>93%</td><td>99%</td></tr><tr><td>False Positive Rate</td><td>0%</td><td>44%</td><td>11%</td><td>2%</td></tr><tr><td>Fingerprint Size</td><td>50 images</td><td>100 images</td><td>100 images</td><td>800 bytes</td></tr><tr><td>Time Cost (Gen. / Verif.)</td><td>61 s / 2 s</td><td>15 s / 32 s</td><td>3233 s / 211 s</td><td>6 s / 3 s</td></tr><tr><td>Suspect Detection</td><td>√</td><td>✗</td><td>✗</td><td>✗</td></tr><tr><td>Ownership Traceability</td><td>√</td><td>✗</td><td>✗</td><td>√</td></tr></table>

![](images/96c46cb7a3063b63716cb802dfecd567dca58b6b85750e4b95e51dc2441fbe22.jpg)



Fig. 9. Total runtime of DEEPREG for various models.

After the actual deployment, we evaluate the total runtime of DEEPREG for various models, as depicted in Fig. 9. The results indicate that the total runtime escalates with the increase in model size. Since the fingerprint extraction during ownership identification occurs within the model owner’s TEE, it constitutes the majority of the runtime. In contrast, during the suspect detection stage, the model owner can generate and verify model fingerprints outside the TEE, significantly reducing the runtime. The piracy judgment stage, which involves only the pre-processing of fingerprint samples and the analysis of query results, requires minimal runtime and is unaffected by the model size.

# E. Generalizability

To demonstrate the generalizability of DEEPREG, we extend our experiments to include models from other modalities, such as graph, text, audio, and video, as presented in Table VI.

For graph recognition, we conduct experiments on the Scientific Collaboration Dataset (COLLAB) [50] with Graph Neural Networks (GNN) [51]. COLLAB is a scientific collaboration dataset comprising 5,000 graphs categorized into three classes. We employ 5 GNN layers in GIN with 64

TABLE VI DETECTION ACCURACY FOR PIRATED MODELS FROM VARIOUS MODALITIES. 

<table><tr><td>Tasks</td><td>Graph Recognition</td><td>Natural Language Processing</td><td>Speech Recognition</td><td>Video Recognition</td></tr><tr><td>Datasets</td><td>COLLAB [50]</td><td>SST-5 [52]</td><td>SCD [55]</td><td>UCF101 [57]</td></tr><tr><td>Models</td><td>GNN [51]</td><td>BERT [54]</td><td>RNN [56]</td><td>CNN+LSTM [58]</td></tr><tr><td>Accuracy</td><td>100%</td><td>100%</td><td>100%</td><td>100%</td></tr></table>

![](images/d4ba0a5b8c168ed7dac875547c51b54d3770035bebcbc28c85a54f17e1bd3bc2.jpg)



(a) Graph Recognition

![](images/b79997d735e91224c30eebd7b8bbea4265795a3246ecc7bbcccb1020c6c4e222.jpg)



(b) Natural Language Processing

![](images/62759edb8089e745f24ca838eaa842aa6414cefa382fc0862185cbc2a09b9e5e.jpg)



(c) Speech Recognition   
Fig. 10. Examples of 1-to-4 fingerprint pairs for models across different tasks.

hidden units per layer, and all multilayer perceptrons consist of 2 layers. For natural language processing, we conduct experiments on the Stanford Sentiment Treebank dataset (SST-5) [52] with Bert [53]. We follow the settings in [54] and use a 24-layer BERT network, with 1024 hidden units and 16 self-attention heads. For speech recognition, we conduct experiments on the Speech Commands Dataset (SCD) [55] with Recurrent Neural Network (RNN) [56]. We utilize a 2-layer RNN with 128 hidden units for the experiment. For video recognition, we conduct experiments on the UCF YouTube Action dataset (UCF101) [57] with the combination of Convolutional Neural Network (CNN) and Long Short-Term Memory (LSTM) networks [58]. We employ an original ImageNet pre-trained ResNet50 as the CNN feature extractor and train an LSTM network on top of it.

To better understand the fingerprints corresponding to models from different modalities, we present examples of 1-to-4 fingerprinting pairs for these tasks, as shown in Fig. 10. The experimental results show that DEEPREG achieves excellent detection accuracy across different modalities of pirated models, and is not easily affected by changes in the dataset categories or model architectures. Since our method ensures that input pairs have similar feature spaces after passing through a specific feature extractor, when the original model is applied to other domains, the identical subsequent processing structures are likely to produce the same output labels.

![](images/d4e31d5fe02c7c933f34214d37293f2365b95f88b86e7e0b3d1c0b508e3cdb8a.jpg)



(a) Impact of position

![](images/6d211bc4e7e3ad40a385f933da38d2d244be7f5cc952c29567fe7da8bf6710ec.jpg)



(b) Impact of number

Fig. 11. Impact of different feature extractors. Position index B indicates the removal of the last B blocks from the original model, where a higher value implies that the chosen feature extractor is situated closer to the input.   
![](images/59106e3bba84ff6237e00c2ace925907908abc344e53c93111004b6018fd9f37.jpg)



(a) K = 4

![](images/0a2f7fb198d54b79866a7671d0f29b28b916641077bfbf5fae8c77d19a74f556.jpg)



(b) $K = 6$

Fig. 12. Impact of the number of fingerprinting pairs.   
![](images/6cfbd9b408589f3d71b2fd68bdf63fd20e00403c5d81db0075bd598d0bd5c980.jpg)



(a) # Iterations

![](images/d025f6cb072b550e5f1220e2fa8a34af43d26e4870e522c6bde331515259cf23.jpg)



(b) Detection Rate   
Fig. 13. Impact of detection thresholds.

# F. Extra Analysis

To further investigate the effectiveness of DEEPREG, we conduct extensive analysis to scrutinize the influence of different settings on its detection performance. By varying the architecture and dataset of suspect models, we can simultaneously assess the robustness of DEEPREG. For convenience, suspect models are denoted by the nomenclature model dataset type, incorporating the abbreviations: C10 (CIFAR-10), C100 (CIFAR-100), Tiny (Tiny-ImageNet), R34 (ResNet34), V16 (VGG16), M (MobileNetV2), P (Positive), and N (Negative). For example, R34 C10 P denotes pirated models derived from ResNet34 trained on ImageNet and applied within the CIFAR-10 application, whereas R34 C10 N signifies irrelevant models unrelated to the original model ResNet34 within the CIFAR-10 application.

Impact of chosen feature extractors. We examine the impact of the location and quantity of chosen feature extractors on the efficacy of our fingerprinting method. Experiments are performed to explore variations in the position and number of feature extractors (i.e., B and K) from 1 to 6, as shown in Fig. 11. As the chosen feature extractor is positioned closer to the input, the fingerprinting pairs activate similar features that can adapt to a wider variety of modifications to the original model, continuously increasing the fingerprint’s matching rate on pirated models. However, synthetic inputs generated by feature extractors closer to the input end will be more similar in detail to the selected real inputs, leading to an increased matching rate of the fingerprint on irrelevant models as well. In Fig. 11b, we observe that the margin between the matching rates of positive and negative suspect models improves and tends to stabilize as K increases, which indicates that a suitable number of feature extractors effectively captures the complex inherent characteristics of the original model.

Impact of fingerprinting pairs. We further study the impact of the number of fingerprinting pairs (i.e., N ) on the fingerprinting method. Fig. 12 presents the average matching rate when the number of fingerprinting pairs grows, with the number of feature extractors K = 4 and $K = 6$ . As is shown, across all applications, the matching rate for pirated models slightly improves and eventually stabilizes as N increases, with this trend being more pronounced when $K \ = \ 6 .$ . It demonstrates that our method maintains high performance with different settings for the parameters N and K.

Impact of detection thresholds. The thresholds for suspect detection, $\tau _ { p o s }$ and $\tau _ { n e g }$ , are pivotal in modulating both the number of iterations required and the detection rate. To elucidate their impact on detection performance, we conduct experiments by varying $\tau _ { p o s }$ from 0.80 to 0.99, corresponding to a change in $\tau _ { n e g }$ from 0.20 to 0.01, as depicted in Fig. 13. To construct the prior probability table, we set the bins of matching rates as [0,0.4), (0.4,0.45), [0.45,0.5), [0.5,0.55), [0.55,0.6), [0.6,1.0], maintaining an equal number of suspect models for both types $M _ { 1 } = M _ { 2 } = 8$ . We observe that as $\tau _ { p o s }$ increases and $\tau _ { n e g }$ decreases, DEEPREG requires more iterations during the suspect detection stage to ensure outputting a probability $P$ that meets the condition. If we employ more lenient thresholds (e.g., $\tau _ { p o s } = 0 . 8 0$ and $\tau _ { n e g } = 0 . 2 0 $ ), DEEPREG may not be able to detect all pirated models and could mistakenly identify a minor fraction of irrelevant models.

# IX. DISCUSSION

# A. Absence of a Fully Trusted Regulator

The envisioned application scenario for DEEPREG is as a government-operated tool for regulating model ownership, analogous to patent applications and infringement lawsuits, with patent offices and courts serving as trusted third parties. By incorporating auxiliary technologies such as blockchain and smart contracts, the design of DEEPREG can be extended to decentralized or adversarial environments. In this context, each model owner operates as a node in the blockchain, while smart contracts can act as regulators responsible for ownership identification and piracy judgment. The automated, transparent, and tamper-proof nature of smart contracts ensures comprehensive and immutable records on the blockchain, eliminating the possibility of collusion between parties, as all actions are publicly verifiable and traceable.

# B. Deployment in Case of a TEE Fault

To ensure the secure execution of fingerprinting codes on untrusted remote devices while maintaining trusted results, the identification process in DEEPREG can be packaged into a Docker container, providing an isolated and verifiable execution environment [59]–[62]. The container is cryptographically signed to verify its integrity. Before execution, the remote device validates the signature using a public key, ensuring authenticity and preventing tampering. Once verified, the container runs with runtime integrity checks to detect any unauthorized modifications. Additionally, comprehensive logging captures operational data and anomalies for post-execution validation. This layered approach, comprising code signing, signature verification, execution isolation, runtime monitoring, and logging, collectively ensures secure and reliable execution on untrusted devices.

# X. CONCLUSION

In this paper, we design an ownership regulatory framework for model ownership. It resolves the trust issue between regulatory authorities and model owners, ensuring the authenticity of the fingerprint during its generation and verification processes. Utilizing our highly compatible fingerprinting method, we propose two separate methods for suspect detection and piracy judgment, ensuring that the submitted APIs by model owners have sufficient confidence and that the final judgment is impartial and irrefutable. Since our method ensures that input pairs have similar feature spaces, when the original model is applied to other downstream tasks, the identical subsequent processing structures are likely to produce similar observation results, and DEEPREG only needs to modify the specific matching metrics to be applicable.

# APPENDIX A PROOF OF THEOREM 1

Proof. For a c-class model S whose response is only the top-1 predicted label $( { \mathrm { i . e . ~ } } y = \arg \operatorname* { m a x } _ { i } S ( \mathbf { x } ) _ { i } )$ , define

$$
p _ {k} = \int_ {\mathbf {x} \in \mathcal {X}} \Pr \left(\arg \max _ {i} \mathcal {S} (\mathbf {x}) _ {i} = = k\right), \forall k \in [ 1, 2, \dots , c ],
$$

where X refers to the input space. Suppose the regulator generates N fingerprinting pairs $\left\{ \left. \mathbf { x } _ { i } , \left\{ \mathbf { x } _ { i j } ^ { \prime } \right\} _ { j = 1 } ^ { K } \right. \right\} _ { i = 1 } ^ { N ^ { - } }$ with a set osponses $\mathbf { x } _ { i }$ and receives N pairs of re-, among which M pairs satisfy $\left\{ \left. y _ { i } , \left\{ y _ { i j } ^ { \prime } \right\} _ { j = 1 } ^ { K } \right. \right\} _ { i = 1 } ^ { N }$ ,among which M pairs satisfy $\begin{array} { r } { \sum _ { j = 1 } ^ { K } \mathbb { 1 } \stackrel { \cdot \cdot } { ( f ( x _ { i j } ^ { \prime } )  } = f ( x _ { i } ) \stackrel { \cdot \cdot } { ) } \ge \frac { K } { 2 } } \end{array}$ . For convenience of expresresponses to the front of the N fingerprinting pairs.

Since we intentionally select the initial values for synthetic inputs from normal inputs that categorically differ from real inputs, there is no direct correlation between real and synthetic inputs. If $s$ is an irrelevant model, the probability of each synthetic input generating a matched response with the real input is ${ \begin{array} { l } { { \underline { { \underline { { 1 } } } } } } \end{array} } ( { \mathrm { i } } . { \mathrm { e } } .$ , random chance). Therefore, the probability of the event occurring

$$
\begin{array}{l} P = \operatorname * {P r} \left(\left\{\left\{y _ {i j} ^ {\prime} \right\} _ {j = 1} ^ {K} \right\} _ {i = 1} ^ {N} \mid \left\{\left\langle \mathbf {x} _ {i}, \left\{\mathbf {x} _ {i j} ^ {\prime} \right\} _ {j = 1} ^ {K} \right\rangle \right\} _ {i = 1} ^ {N}, \left\{y _ {i} \right\} _ {i = 1} ^ {N}, \mathcal {S}\right) \\ = \binom {N} {M} \prod_ {i = 1} ^ {M} \prod_ {j = 1} ^ {K} P _ {y _ {i j} ^ {\prime}} \prod_ {k = M + 1} ^ {N} \prod_ {l = 1} ^ {K} P _ {y _ {k l} ^ {\prime}} \\ \leq \binom {N} {M} \prod_ {i = 1} ^ {M} \prod_ {j = 1} ^ {K} P _ {y _ {i j} ^ {\prime}} = \binom {N} {M} \prod_ {i = 1} ^ {M} \binom {K} {K / 2} P _ {y _ {i}} ^ {\frac {K}{2}} \\ = \binom{N}{M} \left(\binom{K}{K / 2} \left(\frac {1}{c}\right) ^ {\frac {K}{2}}\right) ^ {M} \leq \binom{N}{\lceil N / 2 \rceil} \left(\binom{K}{K / 2} \left(\frac {1}{c}\right) ^ {\frac {K}{2}}\right) ^ {M}. \\ \end{array}
$$

Finally, let $\begin{array} { r } { \left( { \bf \Phi } _ { \lceil N / 2 \rceil } ^ { N } \right) \left( \left( { \bf \Phi } _ { K / 2 } ^ { K } \right) \left( \frac { 1 } { c } \right) ^ { \frac { K } { 2 } } \right) ^ { M } \leq \alpha . } \end{array}$  K2  M , we can derive that

$$
M \geq \log_ {\binom {K} {K / 2} \left(\frac {1}{c}\right) ^ {\frac {K}{2}}} \frac {\alpha}{\binom {N} {\lceil N / 2 \rceil}}. \tag {14}
$$

Let $z = \binom { K } { K / 2 } \left( \textstyle { \frac { 1 } { c } } \right) ^ { \frac { K } { 2 } }$ and $\begin{array} { r } { \beta = \frac { \alpha } { \binom { N } { \lceil N / 2 \rceil } } . } \end{array}$ if $M \geq \log _ { z } \beta \ ( M$ is a positive integer), we can prove that $P \leq \alpha .$ , i.e., reject the null hypothesis $H _ { 0 }$ to conclude that $s$ is not an irrelevant model, and hence make a final judgment.

# REFERENCES

[1] Y. Zeng et al., “Aspect-level sentiment analysis based on semantic heterogeneous graph convolutional network,” Front. Comput. Sci., vol. 17, no. 6, p. 176340, 2023.   
[2] Q. Yuan et al., “Mmco: using multimodal deep learning to detect malicious traffic with noisy labels,” Front. Comput. Sci., vol. 18, no. 1, p. 181809, 2024.   
[3] M. Xue, Y. Zhang, J. Wang, and W. Liu, “Intellectual property protection for deep learning models: Taxonomy, methods, attacks, and evaluations,” IEEE Trans. Artif. Intell., vol. 3, no. 6, pp. 908–923, 2021.   
[4] M. Wang, X. Yin, and J. Hu, “Cancellable deep learning framework for EEG biometrics,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 3745–3757, 2024.   
[5] M. Son et al., “An open-source deep learning model for predicting effluent concentration in capacitive deionization,” Sci. Total Environ., vol. 856, p. 159158, 2023.   
[6] Q. Yang and Y. Zheng, “Deepear: Sound localization with binaural microphones,” IEEE Trans. Mobile Comput., 2022.   
[7] B. Darvish Rouhani et al., “Deepsigns: An end-to-end watermarking framework for ownership protection of deep neural networks,” in Proc. Int. Conf. Archit. Support Program. Lang. Oper. Syst., 2019, pp. 485– 497.   
[8] Y. Adi et al., “Turning your weakness into a strength: Watermarking deep neural networks by backdooring,” in Proc. USENIX Secur. Symp., 2018, pp. 1615–1631.   
[9] Y. Li et al., “Move: Effective and harmless ownership verification via embedded external features,” arXiv:2208.02820, 2022.   
[10] G. Hua et al., “Unambiguous and high-fidelity backdoor watermarking for deep neural networks,” IEEE Trans. Neural Netw. Learn. Syst., vol. 35, no. 8, pp. 11 204–11 217, 2024.   
[11] S. Shao et al., “Explanation as a watermark: Towards harmless and multi-bit model ownership verification via watermarking feature attribution,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2025.   
[12] T. Dong et al., “Rai2: Responsible identity audit governing the artificial intelligence.” in Proc. Netw. Distrib. Syst. Secur. Symp., 2023.   
[13] Y. Zheng, S. Wang, and C.-H. Chang, “A dnn fingerprint for nonrepudiable model ownership identification and piracy detection,” IEEE Trans. Inf. Forensics Security, vol. 17, pp. 2977–2989, 2022.   
[14] Z. Peng et al., “Fingerprinting deep neural networks globally via universal adversarial perturbations,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2022, pp. 13 430–13 439.   
[15] X. Cao et al., “Ipguard: Protecting intellectual property of deep neural networks via fingerprinting the classification boundary,” in Proc. ACM Asia Conf. Comput. Commun. Secur., 2021, pp. 14–25.   
[16] S. Wang et al., “Fingerprinting deep neural networks-a deepfool approach,” in Proc. IEEE Int. Symp. Circuits Syst., 2021, pp. 1–5.   
[17] K. Yang et al., “Metafinger: Fingerprinting the deep neural networks with meta-training,” in Proc. Int. Jt. Conf. Artif. Intell., 2022.   
[18] X. Pan et al., “Metav: A meta-verifier approach to task-agnostic model fingerprinting,” in Proc. ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, 2022, pp. 1327–1336.

[19] J. Guan, J. Liang, and R. He, “Are you stealing my model? sample correlation for fingerprinting deep neural networks,” in Proc. Adv. Neural Inf. Process. Syst., vol. 35, 2022, pp. 36 571–36 584.   
[20] J. Liu et al., “False claims against model ownership resolution,” in Proc. USENIX Secur. Symp., 2024, pp. 6885–6902.   
[21] J. Joyce, “Bayes’ Theorem,” in Stan. Encycl. Philos., 2021.   
[22] Introduction to trusted execution environment: Arm’s trustzone. Accessed Sep. 1, 2024. [Online]. Available: https://blog.quarkslab.com /introduction-to-trusted-execution-environment-arms-trustzone.html   
[23] Intel Corp. Intel software guard extensions. Accessed Sep. 1, 2024. [Online]. Available: https://www.intel.com/content/www/us/en/architec ture-and-technology/software-guard-extensions.html   
[24] T. Knauth et al., “Integrating remote attestation with transport layer security,” arXiv:1801.05863, 2018.   
[25] J. Van Bulck et al., “Foreshadow: Extracting the keys to the intel sgx kingdom with transient out-of-order execution,” in Proc. USENIX Secur. Symp., 2018, pp. 991–1008.   
[26] Z. Chen et al., “Voltpillager: Hardware-based fault injection attacks against intel sgxenclaves using the svid voltage scaling interface,” in Proc. USENIX Secur. Symp., 2021, pp. 699–716.   
[27] Y. Yao et al., “Latent backdoor attacks on deep neural networks,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2019, pp. 2041– 2055.   
[28] L. Shen et al., “Backdoor pre-trained models can transfer to all,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2021, pp. 3141–3158.   
[29] Y. Chen et al., “Teacher model fingerprinting attacks against transfer learning,” in Proc. USENIX Secur. Symp., 2022, pp. 3593–3610.   
[30] N. Carlini and D. Wagner, “Towards evaluating the robustness of neural networks,” in Proc. IEEE Symp. Secur. Privacy, 2017, pp. 39–57.   
[31] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” arXiv:1412.6980, 2014.   
[32] T. Lee et al., “Occlumency: Privacy-preserving remote deep-learning inference using sgx,” in Proc. Annu. Int. Conf. Mobile Comput. Netw., 2019, pp. 1–17.   
[33] Intel Corp. 3rd gen intel® xeon® scalable processors brief. Accessed Sep. 1, 2024. [Online]. Available: https://www.intel.com/content/www/ us/en/products/docs/processors/xeon/3rd-gen-xeon-scalable-processor s-brief.html   
[34] C. Dong et al., “Fusion: Efficient and secure inference resilient to malicious server and curious clients,” arXiv:2205.03040, 2022.   
[35] A. Krizhevsky et al., “Learning multiple layers of features from tiny images,” 2009.   
[36] Y. Le and X. Yang, “Tiny imagenet visual recognition challenge,” CS 231N, vol. 7, no. 7, p. 3, 2015.   
[37] M.-E. Nilsback and A. Zisserman, “Automated flower classification over a large number of classes,” in Proc. Indian Conf. Comput. Vis. Graph. Image Process., Dec. 2008.   
[38] Y. LeCun et al., “Learning algorithms for classification: A comparison on handwritten digit recognition,” Neural Netw.: Stat. Mech. Perspect., vol. 261, no. 276, p. 2, 1995.   
[39] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2016, pp. 770–778.   
[40] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” arXiv:1409.1556, 2014.   
[41] M. Sandler et al., “Mobilenetv2: Inverted residuals and linear bottlenecks,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2018, pp. 4510–4520.   
[42] F. Iandola et al., “Densenet: Implementing efficient convnet descriptor pyramids,” arXiv:1404.1869, 2014.   
[43] J. Deng et al., “Imagenet: A large-scale hierarchical image database,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2009, pp. 248– 255.   
[44] S. Marcel and Y. Rodriguez, “Torchvision the machine-vision package of torch,” in Proc. ACM Int. Conf. Multimedia, 2010, pp. 1485–1488.   
[45] Z. Liu et al., “A convnet for the 2020s,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2022, pp. 11 976–11 986.   
[46] R. Wightman, H. Touvron, and H. Jegou, “Resnet strikes back: An ´ improved training procedure in timm,” arXiv:2110.00476, 2021.   
[47] M. Tan and Q. Le, “Efficientnetv2: Smaller models and faster training,” in Proc. Int. Conf. Mach. Learn. PMLR, 2021, pp. 10 096–10 106.   
[48] K. He et al., “Masked autoencoders are scalable vision learners,” arXiv:2111.06377, 2021.   
[49] E. Huynh, “Vision transformers in 2022: An update on tiny imagenet,” arXiv:2205.10660, 2022.   
[50] P. Yanardag and S. Vishwanathan, “Deep graph kernels,” in Proc. ACM SIGKDD Int. Conf. Knowl. Discov. Data Min., 2015, pp. 1365–1374.

[51] K. Xu, W. Hu, J. Leskovec, and S. Jegelka, “How powerful are graph neural networks?” arXiv:1810.00826, 2018.   
[52] R. Socher et al., “Recursive deep models for semantic compositionality over a sentiment treebank,” in Proc. Conf. Empir. Methods Nat. Lang. Process., 2013, pp. 1631–1642.   
[53] J. Devlin et al., “Bert: Pre-training of deep bidirectional transformers for language understanding,” in Proc. NAACL-HLT, vol. 1, 2019, p. 2.   
[54] M. Munikar et al., “Fine-grained sentiment classification using bert,” in Proc. Artif. Intell. Transform. Bus. Soc., vol. 1. IEEE, 2019, pp. 1–5.   
[55] P. Warden, “Speech commands: A dataset for limited-vocabulary speech recognition,” arXiv:1804.03209, 2018.   
[56] D. C. De Andrade et al., “A neural attention model for speech command recognition,” arXiv:1808.08929, 2018.   
[57] K. Soomro, “Ucf101: A dataset of 101 human actions classes from videos in the wild,” arXiv:1212.0402, 2012.   
[58] J. Yue-Hei Ng et al., “Beyond short snippets: Deep networks for video classification,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2015, pp. 4694–4702.   
[59] W. Luo et al., “Container-IMA: A privacy-preserving integrity measurement architecture for containers,” in Proc. Int. Symp. Res. Attacks, Intrusions, and Defenses, Sep. 2019, pp. 487–500.   
[60] M. De Benedictis and A. Lioy, “Integrity verification of docker containers for a lightweight cloud environment,” Futur. Gener. Comput. Syst., vol. 97, pp. 236–246, 2019.   
[61] Y. Shen et al., “Docker container hardening method based on trusted computing,” J. Phys.: Conf. Ser., vol. 1619, no. 1, p. 012014, 8 2020.   
[62] W. Li et al., “Tcec: Integrity protection for containers by trusted chip on iot edge computing nodes,” IEEE Sens. J., pp. 1–1, 2024.

![](images/c092ca79d3d04762feb358597616e16c033965de23677c216588a95a4b09298d.jpg)



Xirong Zhuang received the B.S. degree in computer science and technology from the College of Computer and Data Science, Fuzhou University, China, in 2021. He is currently working toward the Ph.D. degree with the School of Computer Science and Technology, University of Science and Technology of China, China. His research interests include AI security, privacy protection, and confidential computation.

![](images/1b2bbce898e8f51f940e519ef79770974aacb7da6ac9f1f08c9c6866ad68547c.jpg)



Lan Zhang received the bachelor’s degree from the School of Software, and the Ph.D. degree from the Department of Computer Science and Technology, Tsinghua University, China, in 2007 and 2014, respectively. She is currently a professor with the School of Computer Science and Technology, University of Science and Technology of China. Her research interests include AIoT, privacy protection, mobile computing, etc.

![](images/375ad85f59561050a174c808800392f7c1d78f9a817412620c869536a2892110.jpg)



Chen Tang received the B.S. degree in mathematics and applied mathematics from the XiDian University, China, in 2020. He is currently working toward the Ph.D. degree with the School of Computer Science and Technology, University of Science and Technology of China, China. His research interests include model copyright protection, model fingerprinting and model watermarking.

![](images/2864440e29d7794971f9f09aa62c7b4985d06f7d047168aab351d140c6e5e3ce.jpg)



Yaliang Li received the Ph.D. degree from the Department of Computer Science and Engineering at SUNY Buffalo in 2017. He is a research scientist at Tongyi Lab, Alibaba Group. Before that, he worked as a research scientist at Baidu Research and a senior researcher at Tencent Medical AI Lab. He is broadly interested in machine learning and data mining with a focus on knowledge graph, question answering, automated machine learning, federated learning, and more recently multi-agent system.