# MLink: Linking Black-Box Models From Multiple Domains for Collaborative Inference

Mu Yuan , Lan Zhang , Member, IEEE, Zimu Zheng , Member, IEEE, Yi-Nan Zhang and Xiang-Yang Li , Fellow, IEEE

Abstract—The cost efficiency of model inference is critical to realworld machine learning (ML) applications, especially for delaysensitive tasks and resource-limited devices. A typical dilemma is: in order to provide complex intelligent services (e.g., smart city), we need inference results of multiple ML models, but the cost budget (e.g., GPU memory) is not enough to run all of them. In this work, we study underlying relationships among black-box ML models and propose a novel learning task: model linking, which aims to bridge the knowledge of different black-box models by learning mappings (dubbed model links) between their output spaces. We propose the design of model links which supports linking heterogeneous black-box ML models. Also, in order to address the distribution discrepancy challenge, we present adaptation and aggregation methods of model links. Based on our proposed model links, we developed a scheduling algorithm, named MLink. Through collaborative multi-model inference enabled by model links, MLink can improve the accuracy of obtained inference results under the cost budget. We evaluated MLink on a multi-modal dataset with seven different ML models and two real-world video analytics systems with six ML models and 3,264 hours of video. Experimental results show that our proposed model links can be effectively built among various black-box models. Under the budget of GPU memory, MLink can save 66.7% inference computations while preserving 94% inference accuracy, which outperforms multi-task learning, deep reinforcement learning-based scheduler and frame filtering baselines.

Index Terms—Model linking, multi-model inference.

# I. INTRODUCTION

M ULTI-MODEL inference workloads are increasinglyprevalent, e.g., smart speaker assistants [2], smart prevalent,e.g.，smartspeakerassistants[2],smart

Manuscript received 20 September 2022; revised 1 June 2023; accepted 5 June 2023. Date of publication 7 June 2023; date of current version 5 September 2023. This work was supported in part by the National Key R&D Program of China under Grant 2021YFB2900103, in part by China National Natural Science Foundation under Grants 61932016 and 62132018. This work was supported in part by CAAI-Huawei MindSpore Open Fund and “the Fundamental Research Funds for the Central Universities” under Grant WK2150110024. This article is a substantially extended and revised version of Yuan et al. which appeared in the proceedings of the 36th AAAI conference on artificial intelligence (AAAI ’22) [DOI: 10.1609/aaai.v36i9.21180]. Recommended for acceptance by M. Sugiyama. (Corresponding Authors: Lan Zhang; Xiang-Yang Li.)

Mu Yuan, Yi-Nan Zhang, and Xiang-Yang Li are with the School of Computer Science and Technology, University of Science and Technology of China, Hefei, Anhui 230026, China (e-mail: ym0813@mail.ustc.edu.cn; zhangyinan@mail.ustc.edu.cn; xiangyangli@ustc.edu.cn).

Lan Zhang is with the School of Computer Science and Technology, University of Science and Technology of China, Hefei, Anhui 230026, China, and also with Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, Hefei, Anhui 230039, China (e-mail: zhanglan@ustc.edu.cn).

Zimu Zheng is with the Edge Cloud Innovation Lab., Huawei Cloud, Shenzhen, Guangdong 518129, China (e-mail: zimu.zheng@huawei.com).

Digital Object Identifier 10.1109/TPAMI.2023.3283780

cities [3], drone-based video monitoring [4], multi-modal autonomous driving [5], etc. Besides the accuracy of the trained models, costs in the inference phase can become the bottleneck to the quality of services, especially for delay-sensitive tasks and resource-limited devices.

Towards cost-efficient inference, existing work explored various perspectives to achieve the resource-performance trade-offs. Multi-task learning and zipping [6], [7], [8], [9] can reduce the computing overheads by sharing neurons among different tasks; Model compression [10], [11], [12], [13] techniques attempt to eliminate parameters and connections not related to the inference accuracy; Inference reusing [14], [15] approaches aim to avoid the same or similar computations; Source filtering [16] methods try to transmit only necessary input data to backend ML models. Adaptive configuration [17] and multi-model scheduling [18] were proposed to make inference workloads adaptive to the dynamics of input content. We summarize them as answers to an interesting question:

How to obtain as accurate inference results as possible without the exact execution of ML models?

From this perspective, multi-task learning and model compression generates a lighter model for the same inference task(s) by pruning the original model(s). Inference reusing and source filtering techniques reuse previous inference results as the predicted results through analyzing the correlation between inputs. Based on the observation that, for some input data, the accuracy of expensive and cheap models is similar, adaptive configuration analyzes the input dynamics and predicts the inference results of expensive models by executing cheap ones. Adaptive multi-model scheduling predicts unnecessary inference results as empty using the executed models’ outputs as the hint information.

We address this problem from a novel perspective: linking black-box models. We were motivated by the insight that even ML models that are different in input modalities, learning tasks, architectures, etc., can share knowledge with each other, since ML models are prone to “overlearning” [19] and outputs of different models have semantic correlations [20]. If we can effectively bridge the knowledge among ML models, we can directly predict inference results of remaining models based on executed models’ outputs. If the cost of this prediction is low, it is promising to improve the resulting accuracy of inference results from all models under a limited cost budget, compared to the original workflow of standalone inference where results of unexecuted models cannot be obtained at all. Fig. 1 illustrates the transition from standalone inference to collaborative inference based on our proposed model linking approach. To realize this vision, the following three main challenges need to be solved:

![](images/746817d1520c7b3236abaa12e92d5c1ed687414fdd549de3898db6a6cc1a35c3.jpg)



Fig. 1. From standalone inference to multi-domain collaborative inference based on MLink. m1-m5 denotes ML models. Arrows refer to our proposed model links and blue dotted lines refer to the aggregation process of cross-domain model links.

1) How to build knowledge-level links among black-box and highly different ML models? In practice, deployed ML models could have different architectures and input modalities, and they could be developed by different programming languages and ML frameworks. The heterogeneity makes it challenging to design a general model of knowledge-level connections among ML models. On the other hand, model linking should be non-intrusive to the original inference system and require as little model information and code modification as possible. The black-box access of ML models bringing additional challenges to the design and implementation.   
2) How to adapt model links to dynamic data distribution on the $\hbar y ?$ Due to the dynamics of inputs, model linking faces an adaptation challenge similar to classical ML, namely domain adaptation [21]. Domain shift is typically caused by two factors, i.e., online dynamics of streaming content and differences in application scenarios. For example, running a computer vision model on video streams captured from different cameras or at different times faces distribution shifts [22].   
3) How to efficiently select models to be executed and models to be predicted? Given a set of ML models, after constructing model links among them, we need to select a proper subset of models to be executed under a certain cost budget, e.g., the allocatable GPU memory. Highly efficient model selection is critical to the cost-performance tradeoff, which is non-trivial due to its theoretical hardness.

In this paper, we first formalize the model linking task and propose the design of model links which supports linking heterogeneous black-box ML models. Then we present adaptation and aggregation methods of model links, covering both the online dynamics and cross-domain distribution shifts. And we develop a model link-based algorithm, named MLink, to schedule multi-model inference under a cost budget. We evaluated our designs on a multi-modality dataset with seven different ML models, covering five classes of learning tasks and three types of input modalities. Results show that our proposed model links can be effectively built among heterogeneous black-box models. We evaluated MLink on two real-world video analytics systems, one for the smart building and the other for city traffic monitoring, including six visual models and 3,264 hours of video from 58 cameras. Experimental results show that our online adaptive training methods effectively improves the performance than the vanilla offline training. And our aggregation approach achieves 7.9% higher average accuracy than the original model. Under the budget of GPU memory, MLink outperforms baselines (multi-task learning [8], deep reinforcement learning-based scheduler [18] and frame filtering [16]) and can save 66.7% inference computation while preserving 94% output accuracy.

# II. PROBLEM STATEMENT

In this section, we define the model linking task and the inference under budgets problem.

Model Linking: Given a set of black-box ML models $F =$ $\{ f _ { i } \} _ { i = 1 } ^ { k }$ , where $f _ { i } : X _ { i } \to Y _ { i }$ Fis a function mapping the input to fi i fi Xi Yiits inference result. ML models can be highly heterogeneous, i.e., different input modalities, learning tasks, architectures, etc. We only assume that input spaces $\{ X _ { i } \} _ { i = 1 } ^ { k }$ are the same or Xi ialigned. The case that different models share the same input spaces is common, e.g., multi-task learning-based robotics [8], [9] and multimedia advertising [23]. The aligned input spaces typically exists in the context of multi-modal scenarios, e.g., multi-modality event detection [24] and visual speech synthesis [25]. In practice, synchronization in time can easily align inputs for many applications. Moreover, approaches such as spatial alignment of multi-view videos [26] and audio-visual semantic alignment [27] can be adopted for specific scenarios. We define model linking as a function $g _ { i j } : Y _ { i }  Y _ { j } ,$ , i.e., a mapping from the source model $f _ { i } { } ^ { \circ } \mathrm { s }$ output space to the target model $f _ { j } { ' } \mathrm { s }$ fi. Then the composite function $g _ { i j } \circ f _ { i } : X _ { i }  Y _ { j }$ can fjperform the inference computation of $f _ { j }$ gij fi Xi Yj. Correspondingly, $g _ { j i }$ links the knowledge of $f _ { i }$ into $g _ { j i } \circ f _ { j }$ .

fi gji fjMulti-source Model Links Ensemble: When the number of models $k \geq 3 .$ , for one target model $f _ { j }$ , there could be multiple k fjmodel links from different sources. Let $A \subseteq F$ denote the set of source models. Then for all $f _ { i } \in A , g _ { i j } \circ f _ { i }$ Fperforms the prediction task to $f _ { j } { ' }$ fi A gij fis inference outputs. The question that follows fjis, how do we determine the final prediction? From the ensemble learning perspective, $\{ g _ { i j } \circ f _ { i } \} _ { f _ { i } \in A }$ constitute a multi-expert gij fi f Amodel [28], which has the potential to perform better prediction with the multi-task & multi-modal representation [9], [25]. We define $h _ { A , j }$ as the ensemble model link from  to $f _ { j }$ . So the hinput of $h _ { A , j }$ is the set of predictions by $g _ { i j }$ Awhere $f _ { i } \in A$ . Note hA,jthat if  has only one element $f _ { i } .$ , then $h _ { A , j } = g _ { i j } \circ f _ { i }$ .

A fi hA,j gij fiMulti-Model Inference Under Budget: The model links can be utilized to achieve resource-performance trade-offs of multimodel inference workloads. Let $c ( \cdot )$ denote the cost of running a function, e.g., GPU memory or inference time. For resourcelimited devices (e.g., smartwatches and mobile phones) and delay-sensitive tasks (e.g., real-time video analytics and audio assistant), there are certain constraints on the total cost. We define  as the cost budget and aim to maximize the inference accuracy under that budget. Let $p ( h _ { A , j } )$ denote the performance p hA,jmeasure of the ensemble model link, which depends on the target model’s task. We assume the range of  is normalized into p[0,1]. For example, the performance measure can be accuracy for classification task and bounding box IoU for the detection task. Following previous efforts for optimizing the inference efficiency [16], [18], the performance measure the consistency between obtained results and exact inference outputs, instead of ground-truth labels. The multi-model inference under cost budget problem is formalized as:

$$
\begin{array}{l} \max _ {A \subseteq F} \overbrace {\left(\frac {1}{| F |} \left(\underbrace {\sum_ {f _ {i} \in A} 1} _ {\text { activated }} + \underbrace {\sum_ {f _ {j} \in F \backslash A} p (h _ {A , j})} _ {\text { predicted }}\right)\right)} ^ {\text { average   output   accuracy }} \\ s. t. \underbrace {\sum_ {f _ {i} \in A} c (f _ {i})} _ {\text { exact   inference }} + \underbrace {\sum_ {f _ {j} \in F \backslash A} c (h _ {A , j})} _ {\text { model   links }} \leq B. \end{array} \tag {1}
$$

Under the cost budget, the optimization problem aims to maximize the average performance of all models  by selecting an Factivated subset  to be executed. For ease of description, we Adefine the objective function as the output accuracy. Activated models do exact inference, so their performance scores are all 1. Models that are not activated only participate in constructing model links and will not be executed during the inference phase; instead, they are predicted by the activated models via ensemble model links. The cost of activated models is performing exact inference, while the cost of predicted models is from running model links. So the model links should be both accurate and lightweight to reduce the cost while preserving the quality of the multi-model inference workloads.

# III. BLACK-BOX MODEL LINKING

In this section, we discuss the motivation of linking black-box models and present the theoretical analysis, architecture design, ensemble and training methods of model links.

# A. Motivational Study

When training ML models for different tasks, the ideal representation learned by them should be independent and disentangled [29], i.e., each model only learns the semantics that just covers its objective task. However, due to the mismatched complexity of the data and the model, the machine learning process is prone to “overlearning” [19], which means that unintended semantics is encoded in the learned representation. Besides, there exist semantic correlations among outputs of different tasks and different models may pay attention to the same content, e.g., the same regions in images. For example, in Fig. 2(a), based on G-CAM [30], we plot the attention heatmaps of YOLO-V3 [31] object detector and ResNet50 [32] scene classifier on the same images, and their attention areas have much overlap. We experimented on the correlation between the overlap ratio of attention heatmaps and the performance of model linking. For example, from the scene classification model to the object detection model, as shown in Fig. 2(b), the accuracy of model links is obviously relevant with the overlap ratio $( ( M a p _ { s o u r c e } \land M a p _ { t a r g e t } ) / M a p _ { t a r g e t } )$ . To a certain extent, it M apsource M aptarget /M aptargetshows that the correlation learned by model links is similar with the semantic attention. The “overlearning” characteristic and underlying semantic correlations among outputs make mappings from the same or aligned input space to different output spaces transferable [20].

![](images/aaba2395b69d9535d00181d61207f0d017b968bda1a1c079c670fcc07387744f.jpg)



(a) Attention heatmaps of Object and Scene models.

![](images/9fdc98931debaf7bc2d65dcb224e1cab2fa82f884e30b07adc5e267d0e780e86.jpg)



(b) Scene-to-Object MLink accuracy vs.attention overlaps.   
Fig. 2. Inter-model semantic correlation.

# B. Black-Box Output Versus Intermediate Representation

A key design principle is that we only use the black-box output of the source model to for model linking. Existing work has shown that by fine-tuning the last few layers [33], the intermediate representation can be used to predict other different tasks. However, in real applications, we often have to deal with the deployed models, which only provide a black-box inference API. Compared with intermediate representation, the downstream black-box outputs do have weaker representation capability for general learning tasks. But recent work [18] shows that, given the same (or aligned) inputs, the executed models’ outputs are very effective hints for scheduling unexecuted models. The insight is that the correlation of black-box outputs between multiple tasks with the same input is more explicit and even stronger than the intermediate features. And our experimental results also show that, using the same amount of training data, black-box model linking achieves higher accuracy than a knowledge distillation approach (see Fig. 5) and a multi-task learning approach (see Table V). Considering the better practicality and satisfactory accuracy, we select black-box outputs rather than intermediate representations for linking ML models.

# C. Sample Complexity Analysis

Let $f \in { \mathcal { F } }$ denote task-specific parameters and  denote shared parameters across tasks. It has been proved that when the training data for  is abundant, to achieve bounded prediction herror on a new task only requires (F) sample complexity [34], Cwhere (·) is the complexity of a hypothesis family. Learning Ca model link $g _ { i j } \in \mathcal { G }$ from source model $f _ { i } \in \mathcal { F } _ { i }$ to the target $f _ { j } \in \mathcal { F } _ { j }$ gij fi iconstitutes a compound learning model $g _ { i j } \circ f _ { i \cdot } \mathrm { ~ A ~ }$ fj jlightweight design of model links can makes $C ( \mathcal G ) < C ( \mathcal F _ { j } )$ C < C jhold. Therefore, applying the above result, model linking can significantly reduce the sample complexity to $C ( { \mathcal { G } } )$ , compared with the $C ( \mathcal { F } _ { j } )$ Ccomplexity of learning the target model from C jscratch. This result is also confirmed by our experiments: effective model links can be learnt by a very small amount (e.g., 1%) of training samples (see Fig. 5).

# D. Model Link Architecture

Model links map between black-box models’ output spaces, so the output format determines the architecture. We classify output formats as the fixed-length vector and the variable-length sequence. These two types of outputs could cover most ML models. We propose four types of model link architectures based on best practices of similar learning tasks.

Vec-to-Vec: The model link maps from a vector-output source to a vector-output target. We use a ReLU-activated multilayer perception (MLP) for the vec-to-vec model link.

Seq-to-Vec: The model link maps from a sequence-output source to a vector-output target. We first use an embedding layer, which performs a matrix multiplication to transform the sequence into a fixed-size embedding. Then we use an LSTM [35] layer followed by an MLP to generate the vector output.

Vec-to-Seq: The model link maps from a vector-output source to a sequence-output target. We adopt the encoder-decoder framework, where an MLP serves as the encoder and the decoder consists of an embedding layer, an LSTM layer, an attention layer [36], and a fully-connected layer, in the forward order.

Seq-to-Seq: The model link maps from a sequence-output source to a sequence-output target. We adopt the sequence-tosequence framework [37], where an embedding layer followed by an LSTM layer serves as the encoder and the decoder is the same as the one in the vec-to-seq model link.

The output activation functions are determined by the learning task of the target model. Softmax is used for single-label classification, and sigmoid is used for multi-label classification and sequence prediction. Linear activation works with regression and localization tasks. In our implementation, the default number of hidden units is twice the length of the output dimension, which empirically achieved a good trade-off between effectiveness and efficiency.

# E. Ensemble of Multi-Source Links

The ensemble of multi-source model links has the potential to improve the prediction performance [38], since cross-task and cross-modal representation capabilities could be beneficial. For the target model $f _ { j }$ , given the set of sources , we multiply outputs of $g _ { i j }$ fjby trainable weights, where $f _ { i } \in A .$ A. The weighted prediction is then activated according to $f _ { j } { ' } \mathrm { s }$ learning task. The learned weights of $h _ { A , j }$ fjcan be used to ensemble model links hA,jfrom any subset of sources, i.e., $h _ { A ^ { \prime } , j } , A ^ { \prime } \subset A$ .

# F. Training

Classic knowledge distillation [10] suggests that soft-label supervisions are better for training the “student” model, since the “teacher” model’s outputs augment the hard-label space with relations among different classes. Our experimental results show that this empirical experience still holds in the proposed model linking setting. To train model links and the ensemble model, we collect  inference results $\{ \{ y _ { i } ^ { j } \} _ { j = 1 } ^ { k } \} _ { i = 1 } ^ { n }$ from  models on n yithe same or aligned inputs. Given ${ \bar { f } } _ { i } , f _ { j }$ i kas the source and the fi, fjtarget, respectively, the objective of training the model link $g _ { i j }$ is:

![](images/109510cf2266281401eb8655b6f8711785e1997ecdf517b91720b1bcee462830.jpg)



(a) Vehicle Counting vs.Person Counting

![](images/330a781c17c86dd9555bfeae217285ea4aa088afd1681dd8dcf3d4430875134c.jpg)



(b) Trafic Condition vs.Vehicle Counting   
Fig. 3. Distribution shifts among different time periods. The legend x-yk means the video clip from the xk-th frame to the yk-th frame.

$$
\min \sum_ {l = 1} ^ {n} \mathcal {L} _ {j} (g _ {i j} (y _ {i} ^ {l}), y _ {j} ^ {l}), \tag {2}
$$

where the loss function ${ \mathcal { L } } _ { j }$ depends the learning task of the target model $f _ { j }$ . Given $A , f _ { j }$ as the set of sources and the target, fj A, fjrespectively, the objective of training the ensemble model $h _ { A , j }$ is:

$$
\min \sum_ {i = l} ^ {n} \mathcal {L} _ {j} (h _ {A, j} (\{y _ {i} ^ {l} \} _ {f _ {i} \in A}), y _ {j} ^ {l}). \tag {3}
$$

Both model links and ensemble models are optimized via gradient descent. Note that if  has only one element $f _ { i } ,$ then the Aensemble simply fits as an identity layer and $h _ { A , j } = g _ { i j } \circ f _ { i }$ .

# IV. MODEL LINK ADAPTATION AND AGGREGATION

In this section, we present designs for online adaptive training of model links. And we discuss how to leverage model links for domain adaptation and propose an approach to aggregate cross-domain model links.

# A. Online Adaptive Training

Typically, ML algorithms focus on the general distribution of inputs. In contrast, real-world inputs (e.g., the video stream captured by a camera) feature a much narrower distribution which changes on the fly [22], [39]. In a video analytics system (see Section VI-B for detailed setup) where three models deployed (vehicle counting, person counting, and traffic condition classification), we analyzed the distribution shift over time. As shown in Fig. 3(a), given the same vehicle count, there is a big difference between the four time periods. And a similar difference also exists between the traffic condition classification and vehicle counting models (see Fig. 3(b)). Thus, a vanilla approach that utilizes the initial outputs to train model links results in serious performance degradation when serving online. And collecting samples that have a general enough distribution brings cold start problems. Thus we study the online training approaches for model linking.

![](images/b0881dfb872ef1b5c250d761a7cbd7ff05ce08d9b1fa5ea5a52edfaf8fd2dc79.jpg)



Fig. 4. Multi-task workflow on Hollywood2 dataset. It should be noted that the activated models are not fixed to these three models, but change dynamically.

Periodic Update. A simple way to adapt to the dynamics of inputs is periodically collecting samples to update model links, e.g., run all ML models for 50 frames every ten minutes and train model links using the additional 50 samples. Our experiments show that this approach is effective but lacks adaptability: it wastes computing resources to collect data during periods when updates are not necessary. Therefore, we propose the following adaptive method that actively selects samples for model link updating.

Adaptive Update. Specifically, we use the uncertainty threshold method [40] to decide which data to label (i.e., running both source and target models to obtain the pair of matched inference results). We utilize the canonical entropy uncertainty measurement that is applicable to both classification and regression models (the confidence is approximated by output variance) [41]. Besides uncertainty-based active policy, we adopt a loss prediction-based method [42]. The key idea is adding a neural network that takes the intermediate activation as input and predicts the sample loss. In principle, any active sampling approach is applicable to model linking. Our experimental results show that, given the same labeling budget, online adaptive approaches can further improve the periodic one, due to its ability to sample at more necessary times.

# B. Linking for Domain Adaptation

A long-standing problem of ML is that the model trained on the public dataset performs poorly on the target application data, namely domain shift. Unsupervised [43], semi-supervised [44], and supervised [33] approaches have been comprehensively studied towards domain adaptation. Under ground-truth supervision, our proposed model linking can also be used to adapt deployed black-box models to the target domain.

Linking to an Abstract Model Node. Under our model linking formalization, we first abstract a oracle model node that represents the ground-truth generator (usually human annotators). Next, we can build and train the model link from the deployed model (source domain) to the abstract model (target domain). Then we can execute both the original model and the trained model link for serving. Since we design the architecture of model links to be simple, a small collection of training samples are sufficient to obtain an effective model link. The approach works with the insight that: unlike general ML that focuses on understanding a general distribution, serving models in real-world applications only needs to fit a much narrower distribution.

Algorithm 1: Cross-Domain Aggregation.   
Input: K edges are indexed by k.

1 Cloud executes:
2 Initialize global model link weights $\Theta_{G,0}$ ;
3 for each round $t = 1, 2, \ldots$ do
4    for each edge k in parallel do
5 $\Delta\Theta_{L,k} \leftarrow \text{LocalUpdate}(k)$ ;
6    end
7 $\Theta_{G,t+1} \leftarrow \Theta_{G,t} + \frac{1}{K} \sum_{k} \Delta\Theta_{L,k}$ ;
8 end
9 Edge executes LocalUpdate(k):
10 Compute gradient vector $\Delta\Theta_{L,k}$ on local dataset;
11 Upload $\Delta\Theta_{L,k}$ to the cloud;

# C. Cross-Domain Aggregation

Let us consider a popular case where a cloud server holds ML models and deploys them to many edge devices for analyzing local data streams. Then an interesting question for our proposed model linking is: how to aggregate model links that are locally trained in these edge devices? Training model links avoids most privacy issues since it only needs the inference outputs of ML models, not requiring the raw sensory data. So a global model link can be trained by asking edges to send local inference results to the cloud server. However, although inference results are usually less sensitive than the raw data, in some highly privacy-sensitive scenarios, e.g., medical images in hospitals [45], it is not allowed to transmit local analytic results. Following the idea of federated learning [46] which was proposed to train a global model with distributed and private data, we propose to train a global model link by aggregating gradients of corresponding local model links during training. More specifically, let $g ^ { G }$ be a global model link with parameters $\Theta _ { G }$ gwhich is shared between local domains (e.g., edge devices). GInitially, the cloud server sends $g ^ { G }$ to every edge device. In a round, each edge device trains local model link $g ^ { L }$ and sends ggradients that are computed using local training samples to the cloud. Then the server aggregates local changes by averaging the collected gradients and updates $\Theta _ { G }$ . Algorithm 1 shows the detailed procedures executed on the edges and cloud. Apart from the benefit of better initialization, the global link can also be utilized to improve the domain adaptability [47] via fusing the local and global links by the same ensemble method presented in Section III-E.

# V. COLLABORATIVE MULTI-MODEL INFERENCE

In this section, we present a model link-based algorithm to schedule multi-model inference under a cost budget.

Let ${ \mathcal { F } } ( A )$ denote the average output accuracy, i.e.,

$$
\mathcal {F} (A) = \frac {1}{| F |} \left(\sum_ {f _ {i} \in A} 1 + \sum_ {f _ {j} \in F \backslash A} p (A, f _ {j})\right). \tag {4}
$$

Then we define the gain of activating one more model $f _ { i }$ as $\Delta ( A , f _ { i } ) = { \mathcal { F } } ( A \cup \{ f _ { i } \} ) - { \mathcal { F } } ( A )$ fi. Assuming that adding a A, fi A fi Asource of model link into the ensemble model will not decrease the performance: $p ( A \cup \{ f _ { i } \} , f _ { j } ) \geq p ( A , f _ { j } )$ , which is empirip Acally true [48]. Then $\Delta ( A , f _ { i } ) \ge 0 .$ p A, fj i.e., the objective function A, fiis nondecreasing. As for the submodularity, given $A _ { 1 } \subset A _ { 2 } \subset$ $F , f _ { i } \notin A _ { 2 }$ , we define $A _ { 1 } ^ { \prime } = A _ { 1 } \cup \{ f _ { i } \} , A _ { 2 } ^ { \prime } = A _ { 2 } \cup \{ f _ { i } \}$ A. Then F, fi / Awe have:

$$
\begin{array}{l} \Delta (A _ {2}, f _ {i}) - \Delta (A _ {1}, f _ {i}) = \frac {1}{| F |} \left\{(p (A _ {1}, j) - p (A _ {2}, j)) \right. \\ + \sum_ {f _ {j} \in A _ {2} \backslash A _ {1}, j \neq i} (p (A _ {1}, f _ {j}) - p (A _ {1} ^ {\prime}, f _ {j})) \\ + \sum_ {f _ {j} \in F \backslash A _ {2}, j \neq i} \left[ \underbrace {(p (A _ {2} ^ {\prime} , f _ {j}) - p (A _ {2} , f _ {j}))} _ {f _ {j} ^ {\prime} \text { s   gain   for } A _ {2}} \right. \\ \left. \left. - \underbrace {(p (A _ {1} ^ {\prime} , f _ {j}) - p (A _ {1} , f _ {j}))} _ {f _ {j} ^ {\prime} \text { s   gain   for } A _ {1}} \right] \right\}. \\ \end{array}
$$

Apparently, if the marginal gain of adding $f _ { j }$ into $A _ { 2 } , A _ { 1 }$ is diminishing, then $\Delta ( A _ { 2 } , f _ { i } ) - \Delta ( A _ { 1 } , f _ { i } ) \leq \bar { 0 , } \mathrm { i . e . }$ A , A., the objec-A , fi A , fitive function is submodular. But this property does not always hold. In our experiments, we observed two typical cases: 1) Dominance. The performance of the ensemble model approximately equals the best-performance source of model links. Let $f _ { i ^ { * } } = a r g m a x _ { f _ { i } \in A } p ( g _ { i j } )$ denote the source with maximal fi argmaxf Ap gijperformance. We observe that $p ( h _ { A , f _ { j } } ) \approx p ( g _ { i ^ { * } j } )$ , i.e., the best source dominates the ensemble performance. 2) Mutual assistance. The multi-source model links ensemble outperforms any single source. $\forall f _ { i } \in A , p ( h _ { A , f _ { j } } ) > p ( g _ { i j } )$ , i.e., sources of fi A, p hA,f > p gimodel links assist mutually. And in this case, $f _ { j } { } ^ { \dag } \mathrm { s }$ gain for $A _ { 2 }$ is possibly greater than its gain for $A _ { 1 } , A _ { 1 } \subset A _ { 2 } , { \mathrm { { i f } } } f _ { j }$ Acollaborates better with models in $A _ { 2 } \setminus A _ { 1 }$ .

A AActivation Probability. Solving (1) is NP-hard and the $( 1 -$ $e ^ { - 1 }$ )-approximation algorithm [55] needs partial-enumeration and requires $O ( n ^ { 5 } )$ computations of the objective function. The O noptimization is not a one-off process and should be executed online to fit the dynamics of the inference system. So we design a heuristic metric of activation probability, whose calculation only depends on the model links’ performance rather than ensemble models’. Given a model $f _ { i }$ , the activation probability considers fithree factors: 1) the average performance of model links from $f _ { i }$ to all the others, denoted by:

Algorithm 2: Collaborative Multi-Model Inference.   
Input : model set F, cost budget B
Output: inference results $y_{i}$ 1 For every $f_{i}, f_{j} \in F, i \neq j$ , train model links $g_{ij}$ ;

2 For every $f_{j} \in F$ , train ensemble model $h_{A_{j},j}$ , where $A_{j} = F \setminus \{f_{j}\}$ ;

3 for each period do

4    Profile activation probability $P_{i}$ for each $f_{i} \in F$ by (7);

5    Greedily select $A \leftarrow A \cup \{\arg\max_{f_{i} \in F \setminus A} (\mathcal{P}_{i})\}$ until reach the cost budget B;

6    Input x arrives;

7    for $f_{i} \in F$ do

8    if $f_{i} \in A$ then

9 $y_{i} \leftarrow f_{i}(x)$ ;

10    else

11 $y_{i} \leftarrow h_{A,i}(\{y_{j}\}_{f_{j} \in A})$ ;

12    end

13    end

14 end

$$
\mathcal {P} _ {i} ^ {1} = \frac {\sum_ {j \neq i} p (g _ {i j})}{| F | - 1}; \tag {5}
$$

2) the average performance of model links targeted to $f _ { i }$ from all the others, denoted by:

$$
\mathcal {P} _ {i} ^ {2} = \frac {\sum_ {j \neq i} p (g _ {j i})}{| F | - 1}; \tag {6}
$$

3) the cost of $f _ { i } , \ \mathrm { i . e . , } \ c ( f _ { i } )$ . Then we design the activation fiprobability as follows:

$$
\mathcal {P} _ {i} = \frac {1 + \mathcal {P} _ {i} ^ {1} - \mathcal {P} _ {i} ^ {2}}{w c (f _ {i})}, \tag {7}
$$

where the weight  can be determined by the following norwmalization. By regularizing the range into 0 to 1, we have (1 + $1 - 0 ) / ( w \operatorname* { m i n } _ { i } ( c ( f _ { i } ) ) = 1 , \operatorname { i . e . , } w = 2 / \operatorname* { m i n } _ { i } ( c ( f _ { i } ) )$ . This ac-/ w i c fi w / i c fitivation probability can be regarded as an coefficient that are positively correlated with the gain of the objective function when selecting a ML model.

Periodic Re-Selection: Due to the content dynamics, the optimal subset of activated models may change over time. But adapting to such dynamics brings additional overheads of loading and unloading ML models. So we propose to periodically re-select activated models. At the beginning of each period, we use a small proportion (e.g., 1%) of the data for profiling the prediction performance of model links. Then we update ML models’ activation probabilities and re-select models to be loaded during the current period. By reasonably setting the period length and the proportion of data used for profiling, we can amortize the overheads of loading/unloading ML models to negligible.

TABLE I SUMMARY OF ML MODELS USED ON HOLLYWOOD2 DATASET 

<table><tr><td>Task Class</td><td>ML Model</td><td>Input Modality</td><td>Output Format</td><td>Metric</td></tr><tr><td>Single-Label Classification</td><td>Gender Classification [49]</td><td>Audio</td><td>2-D Softmax Labels</td><td>Accuracy</td></tr><tr><td>Multi-Label Classification</td><td>Action Classification [50]</td><td>Video</td><td>12-D Softmax Labels</td><td>mAP</td></tr><tr><td>Localization</td><td>Face Detection [51]Person Detection [31]</td><td>ImageImage</td><td>4-D Bounding Boxes</td><td>IoU</td></tr><tr><td>Regression</td><td>Age Prediction [52]</td><td>Image</td><td>1-D Scalar</td><td>MAE</td></tr><tr><td>Sequence Generation</td><td>Image Captioning [53]Speech Recognition [54]</td><td>ImageAudio</td><td>Variable-Length Text</td><td>WER</td></tr></table>

Algorithm 2 shows the workflow of integrating MLinks with multi-model inference workloads. Initially, we train pairwise model links and ensemble models. During each period, we first calculate the activation probability by running all models on data for profiling. Then we select greedily w.r.t. activation probability under the cost budget. In the serving phase, activated models do exact inference while the others’ outputs will be predicted by the model link ensemble of activated sources.

# VI. EVALUATION

# A. Implementation

We implemented our designs in Python based on TensorFlow 2.0 [56] as a pluggable middleware for inference systems .1 We tested the integration on programs implemented with Tensor-Flow [56], PyTorch [57] and MindSpore [58], with only dozens of lines of code modification, which shows the ease of use of MLink.

# B. Experiment Setup

We evaluated our designs on a multi-modal dataset and two real-world video analytics systems.

Multi-Modal Dataset and ML Models: We used the Hollywood2 video dataset [59]. To obtain aligned inputs for multimodal models, we selected the 30th frame and extracted audio data from each video. We deployed seven pre-trained ML models that cover five classes of learning tasks: single-label and multilabel classification, object localization, regression, and sequence generation. And they have different model architectures, input modalities and output formats. To evaluate the performance of model links, we used task-specific metrics, including accuracy, mean average precision (mAP), intersection over union (IoU) of the bounding box, mean absolute error (MAE), and word error rate (WER). Table I summarizes information of these ML models. Fig. 4 illustrates the multi-task workflow on the Hollywood2 dataset.

Smart Building and City Traffic Monitoring Systems: We evaluated MLink on two real-world video analytics systems. 1) Smart

building. To support applications including automatic air conditioning and lighting, abnormal event monitoring, and property security, three ML models were deployed: OpenPose [60]-based person counting, ResNet50 [32]-based action classification [61], and YOLOV3 [31]-based object counting. We collected two days (one weekday and one weekend) of video frames from all 58 cameras (1 frame per minute). We use an edge server with one NVIDIA 2080Ti GPU. 2) Traffic monitoring. On a city-scale video analytics platform with over 20,000 cameras, three AI models were deployed for traffic monitoring: OpenPose [60]- based person counting, ResNet50 [32]-based traffic condition classification [62], and YOLOV3 [31]-based vehicle counting. We selected 10 cameras at the road intersections and collected two days (one weekday and one weekend) of frames (1 FPS). We used five servers, each with four NVIDIA T4 GPUs.

Baselines: We introduce the naive standalone inference and three strong alternative resource-performance trade-off approaches as baselines. 1) Standalone: running models independently. 2) MTL: We adopt a multi-task learning architecture [8] that consists of a global feature extractor shared by all tasks and task-specific output branches. We use ResNet50 [32] to implement the feature extractor and fully-connected layers for task-specific outputs. We initialize the ResNet50 feature extractor with weights pretrained on ImageNet [63] and connect three output branches for person counting, action/traffic classification, and object/vehicle counting tasks, on smart building/traffic monitoring testbeds. The MTL models are trained under the supervision of exact inference results of corresponding models. 3) Reducto [16]: a frame filtering approach. For each model, Reducto first computes the feature difference of successive frames. If the feature difference is lower than a threshold, it filters out the current frame and reuses the latest inference output. We tested four types of low-level features as proposed in Reducto and selected the one that has the best performance. 4) DRLS (Deep Reinforcement Learning-based Scheduler) [18]: a multimodel scheduling approach. DRLS trains a deep reinforcement learning agent to predict the next model to execute on the given data, based on the observation of executed models’ outputs.

# C. Black-Box Model Linking

Sensitivity to the Size of Training Data: The original training and test splits in Hollywood2 dataset contain 823 video clips (around 48%) and 884 video clips, respectively. To test the performance of the model linking with different sizes of training data, we further randomly sampled four subsets of training data with 1%, 5%, 10%, 20% ratios, with respect to the total dataset. We trained pairwise model links with the RMSprop [64] optimizer and the same hyper-parameters (0.01 learning rate, 100 epochs, 32 batch size). As a fair comparison, we adopt a knowledge distillation [10] method for some target models (Action, Age, Gender) where the student model has two convolutional layers. We repeated the experiments three times and reported the mean and standard deviation of performance. As shown in Fig. 5, using all training data, the Caption-to-Action model link can achieve 31.7% mAP. And the model links between the two detection models, Face-to-Person and Person-to-Face model links, achieve 59% and 32% IoU, respectively. Even with very limited training samples, 1%, some model links achieve high performance. The model link from Face to Gender achieves 92.1% accuracy. And for model links Gender-to-Age model achieves 3.0 MAE. Compared with student models trained via knowledge distillation on the target models, model links achieves higher prediction performance, especially when the amount of training data is small. But for speech recognition and video caption models, model links targeted to them cannot be effectively built and have around one WER score.

![](images/aefe7f7150cee822c526aeeaf06910b86c9219cb79d964830d05254466cb34d7.jpg)



![](images/eed4ebe662bb5b2460c5cfc45b5b156ec62721aef83aba24f92bb0f7ae8a1e4d.jpg)



![](images/2131940a75c658dae3361d0792eb6e45b382c6e1dbec53f2f98893f7256f60bb.jpg)



![](images/e30e07afc7924028d7ad44db8fafb9cc6a1a3d0eb1692133b56e13a863866f1c.jpg)



(c) Target: Person   
(d) Target: Gender   
Fig. 5. Performance of model links from different source models on four targets. KD-Student: student model trained via knowledge distillation on the target model.

Model Link Ensemble: For one target model, we have built multiple model links from different source models. Then we trained the ensemble models with all sources, using the same optimizer as model links and same hyper-parameters. Table III shows the results on five target models, both model links and ensemble models were trained using all training samples (48% ratio). The model link ensemble outperforms every single source model. We can see there are two typical cases: dominance and mutual assistance. For Action, Face, Person targets, the Caption, Person, Face sources dominate the ensemble performance, respectively. But for Age and Gender targets, source models mutually assist and achieve performance improvement by the ensemble.

TABLE II IOU SCORES OF MODEL LINKS TARGETED TO THE PERSON MODEL AND THE PEARSON CORRELATIONS 

<table><tr><td>Source</td><td>Action</td><td>Age</td><td>Face</td><td>Gender</td></tr><tr><td>IoU (%)</td><td>39.4 (±0.1)</td><td>38.9 (±0.1)</td><td>58.5 (±1.3)</td><td>39.0 (±0.1)</td></tr><tr><td>Corr.</td><td>0.123</td><td>0.042</td><td>0.244</td><td>-0.053</td></tr></table>

![](images/bb8e82f41bb1bd77635fda7d28f3e8c8183aacd97d796672e6e6c7b08a66b945.jpg)

![](images/f274daa16b37e0c3ba157ddb0573fd97aa0f1985eefc700ca12e74ca8b837bd1.jpg)

![](images/343b3c7e872da5dfe209b805fd9da065a464fac3ca15ceb30c24479ce00566d1.jpg)

![](images/c92bee4951e34d1327ad42c94627e4ff69338dca3d6f53cfe5fae1f3a6878b01.jpg)

![](images/afe7f6171577df5b486525e9213288ad536aa5063fa6de0788ea81a2c8d0ebe3.jpg)



Fig. 6. Online Training. Vehicle-to-Person MLink. Images correspond to boxed points in red and show times where the distribution significantly changed.

Correlation Quantification: We calculated the Pearson correlation coefficients between inference outputs of different models on the training split. For single-label and multi-label classification models, we used the index with the highest confidence as the label. For localization models, we checked whether the bounding box is empty, and assign 0 or 1 as the label. We used the regression scalar as the label and skipped the two sequence generation models. Table II shows the results of model links targeted to the Person model, and we can see a positive correlation between the model link performance and the Pearson correlation coefficient.

Discussions: To explore the limitations of MLink, we consider cross-domain semantic segmentation tasks on Cityscapes [65] and GTAV [66] datasets. We deployed the DeepLabV3Plus [67] model pre-trained on Cityscapes and ran it on GTAV images. Then we trained model links that map model predictions to ground-truth masks. Experimental results show that model linking is not effective in this case: the accuracy of remapped predictions degrades by around 10%. The first reason is the large output space of pixel-level segmentation tasks. Learning to calibrate predictions on two million (1052\*1914) pixels is difficult. The second reason is that our vec-to-vec design (fully-connected layers) is task-agnostic. We did not use down-sampling and up-sampling convolutional neural network architecture, which is the best practice for the semantic segmentation task.

# D. Online MLink Training

We evaluated our proposed online training approach for model linking on the traffic monitoring application. For the model link from the vehicle counting source model to the person counting target model, Fig. 6 shows the segment-level (one segment per hour) accuracy on one camera of different training approaches. We set the ratio of training samples as 1%. The

TABLE III DOMINANCE AND MUTUAL ASSISTANCE CASES IN MODEL LINK ENSEMBLE. COLUMN TITLES ARE SOURCE MODELS AND ROW TITLES ARE TARGET MODELS. THE DOMINANT SOURCE’S PERFORMANCE IS IN BOLD 

<table><tr><td>Target \ Source</td><td>Action</td><td>Age</td><td>Caption</td><td>Face</td><td>Gender</td><td>Person</td><td>Speech</td><td>Ensemble</td></tr><tr><td>Action mAP(%)</td><td>-</td><td>12.8(±1.3)</td><td>29.7(±1.4)</td><td>10.1(±1.3)</td><td>9.3(±0.3)</td><td>9.9(±1.2)</td><td>8.5(±3.1)</td><td>30.8(±1.1)</td></tr><tr><td>Face IoU(%)</td><td>11(±1.3)</td><td>11.2(±1.0)</td><td>0 (±0)</td><td>-</td><td>10.3(±0.9)</td><td>31.9(±0.3)</td><td>0 (±0)</td><td>32.2(±0.2)</td></tr><tr><td>Person IoU(%)</td><td>39.4(±0.1)</td><td>38.9(±0.1)</td><td>0(±0)</td><td>58.5(±1.3)</td><td>39.0(±0.1)</td><td>-</td><td>0(±0)</td><td>59.2(±1.2)</td></tr><tr><td>Age MAE</td><td>3.04(±0.01)</td><td>-</td><td>3.02(±0.01)</td><td>3.07(±0.02)</td><td>3.0(±0.01)</td><td>3.03(±0.01)</td><td>3.0(±0.01)</td><td>2.98(±0)</td></tr><tr><td>Gender Acc.(%)</td><td>92(±0.1)</td><td>92.1(±0.2)</td><td>92(±0.1)</td><td>92.1(±0.1)</td><td>-</td><td>92(±0.1)</td><td>92(±0.1)</td><td>92.3(±0)</td></tr></table>

TABLE IV DOMAIN ADAPTATION PERFORMANCE COMPARISON ON OFFICE-HOME. MLINK ACHIEVES HIGHER MEAN ACCURACY THAN UNSUPERVISED APPROACH (SDAT) AND COMPARABLE PERFORMANCE WITH THE SEMI-SUPERVISED ONE (CLDA) 

<table><tr><td>Method</td><td>A-&gt;C</td><td>A-&gt;P</td><td>A-&gt;R</td><td>C-&gt;A</td><td>C-&gt;P</td><td>C-&gt;R</td><td>P-&gt;A</td><td>P-&gt;C</td><td>P-&gt;R</td><td>R-&gt;A</td><td>R-&gt;C</td><td>R-&gt;P</td><td>Avg.</td></tr><tr><td>Source</td><td></td><td>87.9</td><td></td><td></td><td>89.9</td><td></td><td></td><td>96.7</td><td></td><td></td><td>95.0</td><td></td><td>92.3</td></tr><tr><td>Shift</td><td>46.9</td><td>65.2</td><td>71.8</td><td>49.0</td><td>60.9</td><td>63.5</td><td>53.6</td><td>44.1</td><td>73.3</td><td>61.9</td><td>47.9</td><td>76.1</td><td>59.5</td></tr><tr><td>SDAT [43]</td><td>58.2</td><td>77.1</td><td>82.2</td><td>66.3</td><td>77.6</td><td>76.8</td><td>63.3</td><td>57.0</td><td>82.2</td><td>74.9</td><td>64.7</td><td>86.0</td><td>72.2</td></tr><tr><td>CLDA [44]</td><td>63.4</td><td>81.4</td><td>81.3</td><td>70.5</td><td>80.9</td><td>80.3</td><td>72.4</td><td>63.9</td><td>82.2</td><td>76.7</td><td>66.0</td><td>87.6</td><td>75.5</td></tr><tr><td>MLink</td><td>69.2</td><td>85.3</td><td>80.3</td><td>59.8</td><td>77.1</td><td>71.4</td><td>62.9</td><td>64.2</td><td>80.1</td><td>69.7</td><td>66.1</td><td>86.1</td><td>72.6</td></tr></table>

Offline Init approach uses the first 1% samples for training the model link and does not update it for the following data. Experimental results show that due to the limited distribution of training samples, Offline Init approach returns 1% accuracy <on 26 segments and 6.3% accuracy on average. Our proposed Online Periodic significantly improves the average accuracy to 70.2% and Online Uncertainty-Based brings an additional 3.3% improvement. Our loss prediction-based approach outperforms the others and achieves 74.7% average accuracy.

# E. MLink Adaptation and Aggregation

Domain Adaptation on a Public Dataset. We used Office-Home dataset [68] to evaluate the domain adaptation performance of model links. The dataset contains images on four domains: Art (A), Clip Art (C), Product (P) and Real World (R). The splits of training and test data contain 7728 and 7860 images, respectively. As the baseline, we trained ResNet50 [32] classifiers separately by all training samples in each domain. Tested on the same domain (marked as Source), these models achieve 87.9%, 89.9%, 96.7%, and 95.0% accuracy scores, respectively. When adopting these model to different domains (marked as Shift), they suffer significant performance degradation due to domain shift and the average accuracy drops severely from 92.3% to 59.5%. Using 10% randomly sampled data from the training split in the target domain, we trained model links from ResNet50 in the source domain to the target domain. For comparison, we tested two state-of-the-art approaches of domain adaptation: an unsupervised SDAT [43] and a semi-supervised CLDA [44]. The detailed results are shown in Table IV. Using all target-domain images in the unsupervised / semi-supervised way, SDAT / CLDA improves the average accuracy to 72.2% / 75.5%. Using only 10% of target-domain training samples and treating ResNet50 as a black box, model links achieve 72.6% average accuracy. The results show that model links can cost-effectively mitigate the effect of domain shift and improve the adaptability of black-box ML models.

![](images/a3344f7584c0ec799087ae2e5d7b85197ca94ba95c689aefe5bcdad490f35b6d.jpg)



(a) Gym Domain

![](images/2db43e55d285ec5bc8bad2446caf2ded79d339892a26fb6ba13426a412cd852c.jpg)



(b) Smart Building Overall   
Fig. 7. Domain adaptation performance on smart building. Three domains.

Domain Adaptation on Real-World Applications. As introduced in Section VI-B, the three models developed for the smart building application were initially trained by public datasets. Among them, the action classifier suffered the most serious performance degradation when applied to the videos captured in the building. We divide the 58 cameras into three real scenarios: Gym (G), Hall (H), and Office (O), with 11, 25, and 22 cameras, respectively. And we collected 2000 images in each scenario and manually labeled the human actions. The labeled data were split into training and test subsets with 1000 images for each. The test accuracy of the pre-trained action classifier in Gym, Hall, and Office are only 67.5%, 73.9%, and 83.5%, respectively. Using the pre-trained action classifier’s outputs and the ground-truth labels, we trained model links using the different number of samples (100, 200, 500, 1000). In comparison, we adopt a classifier fine-tuning method [69] that freezes parameters of the feature extractor in the pre-trained model and retrains the classifier. Fig. 7(a) plots the accuracy tested on the Gym domain, where fine-tuned classifier achieves 66.1% accuracy while the model link significantly outperforms it with 88.1% accuracy using only 200 training samples. As presented in Fig. 7(b), with 90% fewer training samples, model links still increase the label accuracy by up to 20.7% and outperform fine-tuned classifier by at least 7.85% on average accuracy improvement of the pre-trained model. The reason is that fine-tuning works in high-dimensional feature space, which is so complex that limited training samples cannot tune it to fit the target domain. But model links focus on the adaptation relations that have much lower dimensions.

![](images/87b5c9100cac172fef3943d5e2a02084e2a8642bb48b590a330f4be06ac5ad73.jpg)



(a） Model Link AggregationTested on Office Domain

![](images/593dae4a8445cbef9022a45831045fd34be01a4e81f777bc413a34d9fb7fcc08.jpg)



(b) Local-Global Fusion Tested on Gym Domain   
Fig. 8. Model link aggregation and fusion performance on smart building with three domains (G for Gym, H for Hall, and O for Office).

Cross-Domain Aggregation. We used three smart building scenarios to evaluate the global model links trained by aggregating cross-domain local model links. Taking one scenario as the target domain and the other two as the source domains, we aggregate local model links trained on source domains into the global model link. For the action classification, Fig. 8(a) plots the label accuracy of local and global model links in the Office scenario using different number of samples for training. Directly applying the local model link trained in Gym (or Hall) to Office can improve the accuracy of the original model from 77.8% to 86.2% (or 88.3%). By applying the global model link that was aggregated from Gym and Hall (G+H), the label accuracy achieves 90.2%. On average, the global model links from the other two domains bring a 7.85% improvement in accuracy to the target domain, without using any sample in the target domain.

Local-Global Fusion: We evaluated the effect of fusing local and global model links on the smart building system. For the action classification model, Fig. 8(b) shows the accuracy tested on the Gym domain from which we can see that fusing the local model link (marked as G) and other domains (O, H, O+H) improves the accuracy up to 6% accuracy than only using the Gym domain data. For overall results on all three domains, on average, aggregating cross-domain model links brings an additional 1.1% improvement in accuracy.

Cross-Task Fusion. Then we trained model links from the other two models, object counting (Object) and person counting (Person) models, to the action classifier (Action). And we tested the impact of fusing these links sourced from cross-task models. Fig. 9 plots the label accuracy of model links with fused weights trained by the different number of training samples in the smart building application. The model links fused from multiple sources significantly outperform the single-source model links. Compared with the “Action” model link, fusing links from three cross-task models can improve the accuracy by up to 4.1%.

# F. Video Analytics With Model Links

We test MLink on 48-hour videos of 58 cameras in a smart building system and 48-hour videos of 10 cameras on a city traffic monitoring platform. We leveraged the first 10% in time of data for training model links and ensembles. We set the period length as one hour and use initial 1% data for profiling activation probabilities. For the counting models, the output accuracy is calculated by checking whether the absolute error of the predicted number is less than 0.5. The time costs of each ML model were the average inference time offline profiled by the training data. In the smart building system, the action/person/object models cost 30/44/60 ms per frame. In the traffic monitoring system, the traffic/person/vehicle models cost 55/66/70 ms per frame. The GPU memory costs of each ML model were the peak usage: 4.6 GB for person counting, 1.5 GB for action/traffic classification, and 3.7 GB for object/vehicle counting. We set the budget as the maximal GPU memory allocated for ML Bmodels to evaluate how MLink improves the resource efficiency of multi-model inference. We treat every ML model’s output accuracy equally and report their average output accuracy. Under GPU memory budget, the baseline “Standalone” simply selects the model with minimal average time cost. We repeated the scheduling experiments three times and reported the results in Table V. Since the standard deviations are small ( 0 1), we < .did not present them for simplicity. In both systems, MLink outperforms alternatives in output accuracy. Compared with “Standalone”, in the smart building system, MLink saves 66.7% inference executions, while preserving 94.1% output accuracy.

![](images/16e298ece0ee385bd0553712918f5f6512c1a9edc656018a944f33855cf5cbd4.jpg)



Fig. 9. Cross-task model link fusion on the smart building application with Action as the target task.

TABLE VCOMPARISONS OF MLINK, MTL, REDUCTO, DRLS, AND STANDALONEMETHODS ON TWO VIDEO ANALYTICS SYSTEMS

<table><tr><td rowspan="2">Method</td><td colspan="2">Building (5/9GB Mem.)</td><td colspan="2">City (5/9GB Mem.)</td></tr><tr><td>Acc. (%)</td><td>Time (ms)</td><td>Acc. (%)</td><td>Time (ms)</td></tr><tr><td>Standalone</td><td>33.3/66.7</td><td>30/74</td><td>33.3/66.7</td><td>55/121</td></tr><tr><td>MTL</td><td>53.3</td><td>32.8</td><td>61.3</td><td>32.5</td></tr><tr><td>DRLS</td><td>45.7/81.3</td><td>58.7/107</td><td>39.5/77.6</td><td>102/188</td></tr><tr><td>Reducto</td><td>91.8/96.9</td><td>45.7/89</td><td>84.1/95.3</td><td>64/127</td></tr><tr><td>MLink</td><td>94.1/97.9</td><td>39.3/84</td><td>94/97.4</td><td>62/125</td></tr></table>

Scalability. We did simulations to test the scheduling performance when the number of models is large. Fig. 10 shows the comparisons of Standalone, MLink, and optimal schedules on two simulated cases. In order to simulate normal and relatively extreme conditions of model linking, we generated performances of model links among 10 models and their costs with the normal distribution (0.5 mean, 0.2 std) and beta distribution (0.5 alpha, 0.5 beta), respectively. And we set the ensemble gain fixed as 0.02. Both the optimal and standalone schedules are found by brute-force enumeration. Experimental results show that MLink achieves near-optimal scheduling results and significantly outperforms the standalone baseline.

![](images/5b57127c25f1c0ff9ba2efa94897112f4223a41e6fc8ad524812f0932cd18d27.jpg)



(a) Normal Distribution

![](images/06df1c341658f00fe182e4795f033d08895e9ff5838102b5f43319bbaff265b7.jpg)



(b) Beta Distribution

Fig. 10. Simulation results of scheduling 10 models.   
![](images/9969c3476e0962aa286e7465afac888cd844288aa6f11d10ee7eb0b7b56f4fd9.jpg)



Fig. 11. MLink’s overheads on servers and mobile phones.

Overheads of MLink. In MLink, model link’s training and inference actions have good concurrency and efficiency. We tested concurrent model link training and inference with input and output length randomly set from 1 to 100. The average training time per process decreases to less than one second with more than 20 concurrent training processes. And given 100 concurrent processes with one million samples to inference, the overall latency is only around one minute. We deployed MLink on four different devices (a cloud server, an edge server, a laptop, and a mobile phone) and tested its latency and memory footprint. As shown in Fig. 11, MLink only introduces negligible additional overheads. We also tested the communication overhead of aggregating model links of action classification models. For the 3-client case, the overall communication cost is 88\*3 (server broadcast) + 88\*3 (client update) = 528 bytes per sample. We set the batch size as 32, which translates into a communication cost of 16.5 KB per training step.

# VII. RELATED WORK

Multi-Task Learning and Zipping. One straightforward way to optimize multiple standalone ML models is multi-task learning [7], [8], [9] and zipping [6]. By sharing the same backbone neural networks among different tasks, multi-task models can provide richer inference results than standalone models under the same cost budget. However, multi-task learning approaches lack flexibility and scalability, i.e., we need to tailor multi-task solutions case by case and re-design once the set of tasks change. In contrast, although there exists parameter redundancy between different black-box ML models, MLink approach can be flexibly extended. And experiments show that the accuracy of model linking is higher when given a small amount of training data.

Knowledge Distillation. Following the taxonomy in the recent survey [70], knowledge distillation has three main sources of knowledge: 1) response [10], [71]: the output of the “teacher” model; 2) feature [72]: the intermediate feature maps; 3) relation [73]: the relations of feature maps. Mutual distillation [74], [75] was proposed to train an ensemble of “student” models and let them learn from each other mutually. Cross-task distillation [76] was proposed to train a “student” model by a “teacher” model pre-trained for another task. Model linking is complementary to knowledge distillation, i.e., model links can be built among distilled “student” models.

Redundancy Filtering. Filtering redundant computation or communication is a promising way toward cost-efficient inference. Yuan et al. [18] proposed a reinforcement learning-based scheduler for multi-model data labeling tasks, which leverages the executed models’ outputs as the hint information to schedule remaining models. DNNs-aware video streaming [77] was proposed to compress the pixels less related with inference accuracy for communication-efficient inference. FoggyCache [14] reuses cached inference results by adaptive hashing input values. Our proposed MLink scheduler optimizes the cost-efficiency in a novel and more direct way: predict inference results of unexecuted ML models by executed models’ outputs.

# VIII. CONCLUSION

In this work, we propose to link black-box ML models and present the designs of model links and a collaborative multi-model inference algorithm. The comprehensive evaluations show the effectiveness of black-box model linking and the superiority of the MLink compared to other alternative methods. We summarize limitations and future work as follows: 1) When the semantic correlations between source and target models are low, model linking has poor output accuracy. 2) When the number of joined models is very large, pairwise model linking will become unpractical. So we will study how to smartly select models to build model links in the future.

# REFERENCES

[1] M. Yuan, L. Zhang, and X.-Y. Li, “Mlink: Linking black-box models for collaborative multi-model inference,” in Proc. AAAI Conf. Artif. Intell., 2022, pp. 9475–9483. [Online]. Available: https://ojs.aaai.org/index.php/ AAAI/article/view/21180   
[2] F. Bentley, C. Luvogt, M. Silverman, R. Wirasinghe, B. White, and D. Lottridge, “Understanding the long-term use of smart speaker assistants,” in Proc. ACM Interactive Mobile Wearable Ubiquitous Technol., vol. 2, no. 3, pp. 1–24, 2018.   
[3] L. Duan, Y. Lou, S. Wang, W. Gao, and Y. Rui, “AI-oriented large-scale video management for smart city: Technologies, standards, and beyond,” IEEE MultiMedia, vol. 26, no. 2, pp. 8–20, Second Quarter 2019.

[4] N. Dilshad, J. Hwang, J. Song, and N. Sung, “Applications and challenges in video surveillance via drone: A brief survey,” in Proc. IEEE Int. Conf. Inf. Commun. Technol. Convergence, 2020, pp. 728–732.   
[5] D. Feng et al., “Deep multi-modal object detection and semantic segmentation for autonomous driving: Datasets, methods, and challenges,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 3, pp. 1341–1360, Mar. 2021.   
[6] X. He, Z. Zhou, and L. Thiele, “Multi-task zipping via layer-wise neuron sharing,” in Proc. 32nd Int. Conf. Neural Inf. Process. Syst., 2018, pp. 6019–6029.   
[7] V. Sanh, T. Wolf, and S. Ruder, “A hierarchical multi-task approach for learning embeddings from semantic tasks,” in Proc. AAAI Conf. Artif. Intell., 2019, pp. 6949–6956.   
[8] M. Crawshaw, “Multi-task learning with deep neural networks: A survey,” 2020, arXiv: 2009.09796.   
[9] Y. Zhang and Q. Yang, “A survey on multi-task learning,” IEEE Trans. Knowl. Data Eng., vol. 34, no. 12, pp. 5586–5609, Dec. 2022.   
[10] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” 2015, arXiv:1503.02531.   
[11] S. Liu, Y. Lin, Z. Zhou, K. Nan, H. Liu, and J. Du, “On-demand deep model compression for mobile devices: A usage-driven model selection framework,” in Proc. 16th Annu. Int. Conf. Mobile Syst., Appl., Serv., 2018, pp. 389–400.   
[12] M. Goldblum, L. Fowl, S. Feizi, and T. Goldstein, “Adversarially robust distillation,” in Proc. AAAI Conf. Artif. Intell., 2020, pp. 3996–4003.   
[13] H. Bai, J. Wu, I. King, and M. Lyu, “Few shot network compression via cross distillation,” in Proc. AAAI Conf. Artif. Intell., 2020, pp. 3203–3210.   
[14] P. Guo, B. Hu, R. Li, and W. Hu, “FoggyCache: Cross-device approximate computation reuse,” in Proc. 24th Annu. Int. Conf. Mobile Comput. Netw., 2018, pp. 19–34.   
[15] L. Ning, H. Guan, and X. Shen, “Adaptive deep reuse: Accelerating CNN training on the fly,” in Proc. IEEE 35th Int. Conf. Data Eng., 2019, pp. 1538–1549.   
[16] Y. Li, A. Padmanabhan, P. Zhao, Y. Wang, G. H. Xu, and R. Netravali, “Reducto: On-camera filtering for resource-efficient real-time video analytics,” in Proc. Annu. Conf. ACM Special Int. Group Data Commun. Appl. Technol. Archit. Protoc. Comput. Commun., 2020, pp. 359–376.   
[17] J. Jiang, G. Ananthanarayanan, P. Bodik, S. Sen, and I. Stoica, “Chameleon: Scalable adaptation of video analytics,” in Proc. Conf. ACM Special Int. Group Data Commun., 2018, pp. 253–266.   
[18] M. Yuan, L. Zhang, X.-Y. Li, and H. Xiong, “Comprehensive and efficient data labeling via adaptive model scheduling,” in Proc. IEEE 36th Int. Conf. Data Eng., 2020, pp. 1858–1861.   
[19] C. Song and V. Shmatikov, “Overlearning reveals sensitive attributes,” in Proc. Int. Conf. Learn. Representations, 2020.   
[20] C. Tan, F. Sun, T. Kong, W. Zhang, C. Yang, and C. Liu, “A survey on deep transfer learning,” in Proc. Int. Conf. Artif. Neural Netw., Springer, 2018, pp. 270–279.   
[21] M. Wang and W. Deng, “Deep visual domain adaptation: A survey,” Neurocomputing, vol. 312, pp. 135–153, 2018.   
[22] R. T. Mullapudi, S. Chen, K. Zhang, D. Ramanan, and K. Fatahalian, “Online model distillation for efficient video inference,” in Proc. IEEE/CVF Int. Conf. Comput. Vis., 2019, pp. 3573–3582.   
[23] M. Yuan, L. Zhang, Z. Wu, and D. Zheng, “High-quality activity-level video advertising,” in Proc. IEEE/ACM 28th Int. Symp. Qual. Service, 2020, pp. 1–10.   
[24] M. Elhoseiny, J. Liu, H. Cheng, H. Sawhney, and A. Elgammal, “Zero-shot event detection by multimodal distributional semantic embedding of videos,” in Proc. 30th AAAI Conf. Artif. Intell., 2016, pp. 3478–3486.   
[25] T. Baltrušaitis, C. Ahuja, and L.-P. Morency, “Multimodal machine learning: A survey and taxonomy,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 41, no. 2, pp. 423–443, Feb. 2019.   
[26] J. Black, T. Ellis, and P. Rosin, “Multi view image surveillance and tracking,” in Proc. IEEE Workshop Motion Video Comput., 2002, pp. 169–174.   
[27] J. Wang, Z. Fang, and H. Zhao, “AlignNet: A unifying approach to audiovisual alignment,” in Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis., 2020, pp. 3309–3317.   
[28] S. E. Yuksel, J. N. Wilson, and P. D. Gader, “Twenty years of mixture of experts,” IEEE Trans. Neural Netw. Learn. Syst., vol. 23, no. 8, pp. 1177–1193, Aug. 2012.   
[29] R. D. Hjelm et al., “Learning deep representations by mutual information estimation and maximization,” in Proc. Int. Conf. Learn. Representations, 2019. [Online]. Available: https://openreview.net/forum?id=Bklr3j0cKX

[30] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, “Grad-CAM: Visual explanations from deep networks via gradientbased localization,” Int. J. Comput. Vis., vol. 128, no. 2, pp. 336–359, 2020.   
[31] J. Redmon and A. Farhadi, “Yolov3: An incremental improvement,” 2018, arXiv: 1804.02767.   
[32] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2016, pp. 770–778.   
[33] Y. Guo, H. Shi, A. Kumar, K. Grauman, T. Rosing, and R. Feris, “SpotTune: Transfer learning through adaptive fine-tuning,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2019, pp. 4805–4814.   
[34] N. Tripuraneni, M. Jordan, and C. Jin, “On the theory of transfer learning: The importance of task diversity,” in Proc. Adv. Neural Inf. Process. Syst., 2020, pp. 7852–7862.   
[35] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural Comput., vol. 9, no. 8, pp. 1735–1780, 1997.   
[36] D. Bahdanau, K. H. Cho, and Y. Bengio, “Neural machine translation by jointly learning to align and translate,” in Proc. 3rd Int. Conf. Learn. Representations, 2015.   
[37] I. Sutskever, O. Vinyals, and Q. V. Le, “Sequence to sequence learning with neural networks,” in Proc. Adv. Neural Inf. Process. Syst., 2014, pp. 3104–3112.   
[38] Z. Shen, Z. He, and X. Xue, “Meal: Multi-model ensemble via adversarial learning,” in Proc. AAAI Conf. Artif. Intell., 2019, pp. 4886–4893.   
[39] Z. Li, J. Ye, M. Song, Y. Huang, and Z. Pan, “Online knowledge distillation for efficient pose estimation,” in Proc. IEEE/CVF Int. Conf. Comput. Vis., 2021, pp. 11 740–11 750.   
[40] B. Settles, “Active learning literature survey,” University of Wisconsin-Madison Department of Computer Sciences, Science, vol. 10, no. 3, pp. 237–304, 1995.   
[41] D. J. MacKay, “Information-based objective functions for active data selection,” Neural Comput., vol. 4, no. 4, pp. 590–604, 1992.   
[42] D. Yoo and I. S. Kweon, “Learning loss for active learning,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2019, pp. 93–102.   
[43] H. Rangwani, S. K. Aithal, M. Mishra, A. Jain, and V. B. Radhakrishnan, “A closer look at smoothness in domain adversarial training,” in Proc. Int. Conf. Mach. Learn., PMLR, 2022, pp. 18 378–18 399.   
[44] A. Singh, “CLDA: Contrastive learning for semi-supervised domain adaptation,” in Proc. Adv. Neural Inf. Process. Syst., vol. 34, pp. 5089–5101, 2021.   
[45] D. Ng, X. Lan, M. M.-S. Yao, W. P. Chan, and M. Feng, “Federated learning: A collaborative effort to achieve better medical imaging models for individual sites that have small labelled datasets,” Quantitative Imag. Med. Surg., vol. 11, no. 2, 2021, Art. no. 852.   
[46] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” ACM Trans. Intell. Syst. Technol., vol. 10, no. 2, pp. 1–19, 2019.   
[47] D. Peterson, P. Kanani, and V. J. Marathe, “Private federated learning with domain adaptation,” 2019, arXiv: 1912.06733.   
[48] Z.-H. Zhou, Ensemble Methods: Foundations and Algorithms. Boca Raton, FL, USA: CRC, 2012.   
[49] A. Kumar, “Pygender-voice,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/abhijeet3922/PyGender-Voice   
[50] D. Tran, L. Bourdev, R. Fergus, L. Torresani, and M. Paluri, “Learning spatiotemporal features with 3D convolutional networks,” in Proc. IEEE Int. Conf. Comput. Vis., 2015, pp. 4489–4497.   
[51] S. I. Serengil and A. Ozpinar, “LightFace: A hybrid deep face recognition framework,” in Proc. Innov. Intell. Syst. Appl. Conf., 2020, pp. 23–27.   
[52] G. Levi and T. Hassner, “Age and gender classification using convolutional neural networks,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. Workshops, 2015, pp. 34–42.   
[53] G. Wang, “Image captioning,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/DeepRNN/image\_captioning   
[54] Mozilla, “DeepSpeech,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/mozilla/DeepSpeech   
[55] M. Sviridenko, “A note on maximizing a submodular set function subject to a knapsack constraint,” Operations Res. Lett., vol. 32, no. 1, pp. 41–43, 2004.   
[56] TensorFlow, “TensorFlow,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/tensorflow/tensorflow   
[57] PyTorch, “PyTorch,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/pytorch/pytorch   
[58] MindSpore, “MindSopre,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/mindspore-ai/mindspore   
[59] M. Marszalek, I. Laptev, and C. Schmid, “Actions in context,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2009, pp. 2929–2936.

[60] Z. Cao, G. H. Martinez, T. Simon, S. Wei, and Y. A. Sheikh, “OpenPose: Realtime multi-person 2D pose estimation using part affinity fields,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 43, no. 1, pp. 172–186, Jan. 2021.   
[61] M. Olafenwa, “Action-Net,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/OlafenwaMoses/Action-Net   
[62] M. Olafenwa, “Traffic-Net,” 2021, Accessed: Aug. 01, 2021. [Online]. Available: https://github.com/OlafenwaMoses/Traffic-Net   
[63] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, “ImageNet: A large-scale hierarchical image database,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2009, pp. 248–255.   
[64] T. Tieleman and G. Hinton, “Lecture 6.5-rmsprop: Divide the gradient by a running average of its recent magnitude,” Coursera Neural Netw. Mach. Learn., vol. 4, no. 2, pp. 26–31, 2012.   
[65] M. Cordts et al., “The cityscapes dataset,” in Proc. CVPR Workshop Future Datasets Vis., 2015.   
[66] S. R. Richter, V. Vineet, S. Roth, and V. Koltun, “Playing for data: Ground truth from computer games,” in Proc. Eur. Conf. Comput. Vis., ser. LNCS, B. Leibe, J. Matas, N. Sebe, and M. Welling, Eds., Springer, 2016, pp. 102– 118.   
[67] L.-C. Chen, Y. Zhu, G. Papandreou, F. Schroff, and H. Adam, “Encoderdecoder with atrous separable convolution for semantic image segmentation,” in Proc. Eur. Conf. Comput. Vis., 2018, pp. 801–818.   
[68] H. Venkateswara, J. Eusebio, S. Chakraborty, and S. Panchanathan, “Deep hashing network for unsupervised domain adaptation,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2017, pp. 5385–5394.   
[69] B. Chu, V. Madhavan, O. Beijbom, J. Hoffman, and T. Darrell, “Best practices for fine-tuning visual classifiers to new domains,” in Proc. Eur. Conf. Comput. Vis., Springer, 2016, pp. 435–442.   
[70] J. Gou, B. Yu, S. J. Maybank, and D. Tao, “Knowledge distillation: A survey,” Int. J. Comput. Vis., vol. 129, pp. 1789–1819, 2021.   
[71] J. Ba and R. Caruana, “Do deep nets really need to be deep?,” in Proc. Adv. Neural Inf. Process. Syst., 2014, pp. 2654–2662.   
[72] D. Chen et al., “Cross-layer distillation with semantic calibration,” in Proc. AAAI Conf. Artif. Intell., 2021, pp. 7028–7036.   
[73] N. Passalis, M. Tzelepi, and A. Tefas, “Heterogeneous knowledge distillation using information flow modeling,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2020, pp. 2339–2348.   
[74] Y. Zhang, T. Xiang, T. M. Hospedales, and H. Lu, “Deep mutual learning,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2018, pp. 4320–4328.   
[75] A. Yao and D. Sun, “Knowledge transfer via dense cross-layer mutualdistillation,” in Proc. Eur. Conf. Comput. Vis., Springer, 2020, pp. 294–311.   
[76] H.-J. Ye, S. Lu, and D.-C. Zhan, “Distilling cross-task knowledge via relationship matching,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2020, pp. 12 396–12 405.   
[77] X. Xie and K.-H. Kim, “Source compression with bounded DNN perception loss for IoT edge computer vision,” in Proc. 25th Annu. Int. Conf. Mobile Comput. Netw., 2019, pp. 1–16.

![](images/9a40d50c0bdac1f5b1c8f1964c8b66db829cfa04e9d73a234eec52ac6e5863ff.jpg)



Lan Zhang (Member, IEEE) received the bachelor’s and PhD degrees from Tsinghua University, China. She is currently a professor with the School of Computer Science and Technology, University of Science and Technology of China. Her research interests include mobile computing, privacy protection, and data sharing and trading.

![](images/bfa8b07b207ebe0ff27b456da1eab88e7f71fb67388e14631142410dd57047a4.jpg)



Zimu Zheng (Member, IEEE) received the BEng degree from the South China University of Technology and the PhD degree from Hong Kong Polytechnic University. He is currently a head research engineer with Huawei Cloud. He has received several awards for outstanding technical contributions in Huawei. He also received the Best Paper Award of ACM e-Energy and the Best Paper Award of ACM BuildSys in 2018. His research interest lies in edge intelligence, multitask learning, and AIoT.

![](images/f2b89be539915a6c6f541a42b0cf9beb1aa25a52f72b929aa627bf161643f619.jpg)



Yi-Nan Zhang received the bachelor’s degree from North Eastern University, China. He is currently working toward the master’s degree with the School of Computer Science and Technology of China. His research interests include knowledge reasoning and multi models inference.

![](images/0a526240f21882604363a2259ad4fddd1b424705b2d0e4c397fdf3713a547465.jpg)



Mu Yuan received the bachelor’s degree in computer science and technology from USTC. He is currently working toward the PhD degree with the School of Computer Science and Technology, University of Science and Technology of China (USTC). His research interests include model inference and network systems.

![](images/97fd62e10cbc2d2cc49466f7ffd30fd63444be981c468dfaa21b3b67248003ff.jpg)



Xiang-Yang Li (Fellow, IEEE) received the bachelor’s degree from the Department of Computer Science from Tsinghua University, China, in 1995, the MS and PhD degrees from the Department of Computer Science, University of Illinois at Urbana-Champaign, in 2000 and 2001 respectively. He is a professor and executive dean with the School of Computer Science and Technology, USTC. He is an ACM fellow (2019), and an ACM distinguished scientist (2014). He was a full professor with Computer Science Department of IIT and co-chair of ACM

China Council. His research interests include Artificial Intelligence of Things (AIOT), privacy and security of AIOT, and data sharing and trading.