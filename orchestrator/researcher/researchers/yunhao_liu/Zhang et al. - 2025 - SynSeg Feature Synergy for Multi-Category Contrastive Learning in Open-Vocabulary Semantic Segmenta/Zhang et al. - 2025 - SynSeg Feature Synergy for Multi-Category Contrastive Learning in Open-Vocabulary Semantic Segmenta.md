# SynSeg: Feature Synergy for Multi-Category Contrastive Learning in End-to-End Open-Vocabulary Semantic Segmentation

Weichen Zhang1, Kebin Liu1\*, Fan Dang3, Zhui Zhu2, Xikai Sun2, Yunhao Liu1,2

1Global Innovation Exchange, Tsinghua University, Beijing, China

2Department of Automation, Tsinghua University, Beijing, China

3School of Software Engineering, Beijing Jiaotong University, Beijing, China

{weic zhang23, z-zhu22, sxk23}@mails.tsinghua.edu.cn,

{kebinliu2021, yunhao}@tsinghua.edu.cn, dangfan@bjtu.edu.cn

Semantic segmentation in open-vocabulary scenarios presents significant challenges due to the wide range and granularity of semantic categories. Existing weaklysupervised methods often rely on category-specific supervision and ill-suited feature construction methods for contrastive learning, leading to semantic misalignment and poor performance. In this work, we propose a novel weakly-supervised approach, SynSeg, to address the challenges. SynSeg performs Multi-Category Contrastive Learning (MCCL) as a stronger training signal with a new feature reconstruction framework named Feature Synergy Structure (FSS). Specifically, MCCL strategy robustly combines both intra- and inter-category alignment and separation in order to make the model learn the knowledge of correlations from different categories within the same image. Moreover, FSS reconstructs discriminative features for contrastive learning through prior fusion and semanticactivation-map enhancement, effectively avoiding the foreground bias introduced by the visual encoder. Furthermore, SynSeg is a lightweight end-to-end solution without using any mid-term output from large-scale pretrained models and capable for real-time inference. In general, SynSeg effectively improves the abilities in semantic localization and discrimination under weak supervision in an efficient manner. Extensive experiments on benchmarks demonstrate that our method outperforms state-of-the-art (SOTA) performance. Particularly, SynSeg achieves higher accuracy than SOTA baselines with a ratio from 6.9% up to 26.2%.

# 1. Introduction

Semantic segmentation is a fundamental task in computer vision that focuses on the classification of each pixel in an image with respect to semantic categories. This task has numerous practical applications, including autonomous driving [3, 44], medical image analysis [16, 18] and embodied intelligence [56]. However, due to the wide range and variability of object categories in the open vocabulary scenarios encountered in real-world tasks, traditional semantic segmentation methods with fixed categories are often insufficient.

To overcome these limitations, many Open Vocabulary Semantic Segmentation (OVSS) approaches have been developed recently [4, 11, 23, 27, 32, 47, 49, 50]. OVSS aims to segment any object category, including those not explicitly defined during training, enabling more flexible and scalable scene understanding. Training such OVSS systems typically requires large amounts of pre-annotated data at pixel level, while semantic annotation in open vocabulary scenarios is both costly and challenging [7, 13, 51]. Manual annotation leads to substantial human labor and is prone to the detrimental effects of poor-quality annotations. In contrast, weakly-supervised learning methods that incorporate semantic text cues into the semantic segmentation tasks via visual-text alignment techniques offer a compelling alternative.

Nevertheless, existing weakly-supervised OVSS solutions often fail to achieve satisfactory performance due to the lack of accurate and concrete supervisory signals. GroupViT [50] and VilSeg [27] are the earliest approaches in the field of OVSS and have paved the way for numerous subsequent studies [11, 22, 30, 52]. They introduce a simple image-text alignment architecture, which is shown in Fig. 1(a). Specifically, they operate by grouping local visual features and matching these clusters with text embeddings at test time to generate segmentation masks. However, during training, text embeddings are aligned with a global image representation rather than the detailed regionlevel features used during inference. This mismatch leads to a notable inconsistency between training and testing, which may impede the model’s ability to fully capture fine-grained

semantic details.

Some other approaches like TCL [4] improved on the above by introducing region-level visual-text alignment training objective, which is shown in Fig. 1(b). These methods leverage the directional cues provided by textual descriptions to jointly guide the regions’ segmentation in both training and testing process [32, 47]. These schemes work well in simple scenes with sparse targets. They, however, encounter a substantial limitation when applied to scenarios with dense targets which are common in real-word open vocabulary settings [1, 26]. This limitation comes from the fact that each segmentation region usually aligns to just one semantic category. And the loss functions in these solutions are usually designed in a category-specific way, focusing on only intra-category alignment. After all, in real-world scenes where multiple categories appear in close spatial proximity or even visually overlap with each other, intracategory alignment alone is insufficient to achieve strong semantic discrimination. Without a coordinated interplay of both intra- and inter-category alignment and separation mechanisms, the model struggles to disambiguate between overlapping or visually similar regions. As a result, this leads to the first challenge: existing OVSS methods lack explicit modeling of inter-category correlations during training, which limits their ability to distinguish semantically different targets in one image.

Moreover, as shown in Fig. 1(a) and (b), previous works typically rely on frozen, pre-trained vision encoders such as CLIP [34] to extract features for contrastive learning after the decoder. However, these features often exhibit limited discriminability in background regions, as the encoder is inherently biased toward salient foreground objects [11, 35]. Therefore, segmentation regions contaminated by background noise may still yield highly similar representations to clean regions. This hinders the rapid decline of the contrastive loss and reduces the overall learning efficiency. As a result, this leads to the second challenge: existing methods lack the ability to reconstruct representations that are well-suited for contrastive learning in openvocabulary semantic segmentation.

To address the two challenges above, our work introduces an innovative approach, SynSeg, for weaklysupervised open vocabulary semantic segmentation. Specifically, we propose a Multi-Category Contrastive Learning strategy, and a new feature reconstruction framework named Feature Synergy Structure.

Multi-Category Contrastive Learning (MCCL) provides a stronger weakly-supervised signal that introduces inter-category alignment and separation across multiple semantic categories, which is shown in Fig. 1(c). This training strategy constructs positive pairs between foreground features and their corresponding text embeddings, as well as negative pairs from foreground and background features belonging to the same class. Additionally, it forms positive pairs from background features of these semantic categories, for their backgrounds are often highly overlapped, and negative pairs from different semantic classes within the same image. Our method enhances the distinction between objects in semantic-dense scenarios. This enables the model to better distinguish attention maps corresponding to various objects, resulting in more precise semantic localization and segmentation.

In order to generate features for effective MCCL, we propose a feature reconstruction framework named Feature Synergy Structure (FSS). It generates category-aware features enhanced by attention maps. Unlike TCL’s method of incorporating textual features, we fuse the textual features with image features before generating segmentation proposals, forming a conditional visual vector. This vector encodes the semantic category indicated by the text, and when passed through a transformer decoder, it generates a semantic-activation map. After that, the semantic-activation map is thresholded to generate the final segmentation output.

From another perspective, the semantic-activation map produced by the transformer decoder can be interpreted as a class-specific attention map, representing a continuousvalued response that highlights the semantic relevance of each pixel to a given category. To obtain a synergy feature, we flatten the semantic-activation map and perform a matrix multiplication between it and the conditional visual vector. This step leverages the attention map to refine the conditional visual vector by emphasizing regions with high semantic relevance and suppressing less important regions, thereby producing a more discriminative feature representation. Such a synergy feature is ideal for MCCL: for we can reconstruct a set of synergy features for each semantic category present in the image, facilitating improved representation and more robust contrastive learning across multiple classes. Also, we avoid using visual encoder twice and reduce the foreground bias it introduces.

The solutions we propose effectively address the limitations of current weakly-supervised methods in OVSS and enhance segmentation performance. Our primary contributions include:

(1) We introduce a novel Multi-Category Contrastive Learning (MCCL) strategy that incorporates both intercategory and intra-category contrastive objectives, which provides a stronger weak-supervision signal for OVSS task.

(2) We propose a Feature Synergy Structure (FSS) to reconstruct semantic-aware features for effective contrastive learning instead of reusing pretrained visual encoders. The features are enhanced by attention maps, also referred to as semantic-activation maps, which emphasize semantically relevant regions while suppressing less informative areas.

(3) We implement and evaluate our proposed method,

![](images/d361bbc0e9e5a2c43c46fa6070dbdc8ded436bca45ffbd298c0e77c77ca81762.jpg)



(a) image-text alignment [50]

![](images/16e53e70fc13504122c8901501952e0f69f8f2835f4ae01f816ab10ede4cd4c7.jpg)



(b) region-text [4] / region-word alignment [47]

![](images/d5649657ae16a8e2aabd6b0c3e3e202605e8902de3c74089063077b48d902abf.jpg)



(c) Multi-category separation and alignment (Ours)   
Figure 1. Training paradigms comparison among previous works and ours. Prior approaches typically adopt either (a) image-text alignment or (b) region-text/region-word alignment, primarily emphasizing intra-category contrastive learning. In contrast, our novel paradigm (c) explicitly incorporates inter-category contrastive learning for improved discriminative capability. Also, our approach does not need to reconstruct training features from a pre-trained visual encoder.

SynSeg, across multiple OVSS evaluation datasets, achieving performance that surpasses state-of-the-art (SOTA) benchmarks.

# 2. Related Work

In this section, we will briefly present related works that serve as a motivation for our study.

# 2.1. Visual-Language Models

Vision-language models aim to bridge the gap between visual and textual modalities, enabling a broad range of multimodal tasks such as image-text retrieval [24, 34], image captioning [25, 53], open-vocabulary detection and recognition [20, 41, 45, 46], and multi-source semantic segmentation [9, 14]. Among these models, CLIP (Contrastive Language-Image Pretraining) [34] introduced a framework for joint visual and textual representation learning using contrastive learning on a large-scale dataset of image-text pairs. It aligns image and text embeddings in a shared feature space, enabling zero-shot tasks and fundamental abilities. BLIP (Bootstrapped Language-Image Pretraining) [25] enhances vision-language models with a multimodal encoder-decoder architecture and combined generative and contrastive objectives. Its bootstrapped selflearning improves performance across datasets, making it effective for tasks such as image captioning and visionlanguage understanding.

# 2.2. Weakly-Supervised OVSS Methods

In early OVSS works [27, 30, 50], textual information does not participate in the computation or generation of segmentation masks but only plays a role in the subsequent matching of mask proposals with candidate semantic labels. Multiple later works follow this structure and explore improvements in segmentation accuracy and semantic alignment precision [2, 6, 22, 49]. However, with such structure, the visual segmentation output remains unchanged regardless of the provided textual prompt. Furthermore, in the architectures based on the classic GroupViT [50], the number of output class token is fixed (e.g., 4 or 8), making it impossible to segment more semantic categories than this predefined limit. Since the text is not involved in the generation of mask proposals, and only a limited number of semantically irrelevant proposals are produced, this structure necessitates an additional step for global-level alignment, which in turn limits the overall learning efficiency. The inconsistency between region-level alignment during testing and global-level alignment during training also leads to poor performance in fine-grained segmentations.

TCL [4] performs a different structure firstly to partially incorporate text labels into the mask generation process and apply region-text alignment during training. Typically, this occurs at the final step, where each pixel feature is compared with text label embeddings to cluster and assign it to a candidate label, determining which pixels are highly correlated with the semantic information to produce the final segmentation result. This paradigm is followed by later works [32, 40, 43]. For example, CoDe [47] improves its work by introducing region-word alignment. In these works, the integration of textual information with the visual feature enables the mask proposal to refer to certain semantic more flexibly, thereby enhancing the granularity of segmentation alignment. However, This training approach mainly focuses on a single object or semantic category and does not exploit the relationships among different semantic objects within the same image.

Furthermore, these works typically feed segmentation results into the CLIP models [34] again to construct visual features for loss computing. Since the CLIP model is inherently biased toward salient foreground objects, its visual representations tend to be sparse and less discriminative in background regions [11, 35]. In OVSS, when segmentation predictions inadvertently include background noise—pixels that actually belong to other semantic categories—such sparse representations hinder the model’s ability to produce more accurate and precise segmentation regions. Due to CLIP’s limited capacity for representing background content, the visual features of noisy segmentation regions often remain highly similar to those of cleaner regions, which serve as the intended training targets. This leads to optimization bottlenecks of the loss functions’ decline that weaken the effectiveness of contrastive learning, both in terms of intra- and, if applicable, inter-category alignment and separation.

![](images/2a3b5bf6e39c930810cb04dced9ccf8648fc4a483a3be30b9c91f28f15565aaa.jpg)



Figure 2. The pipeline of SynSeg. It illustrates the proposed Feature Synergy Structure and Multi-Category Contrastive Learning framework. During training, FiLM [33] fusion module, transformer decoder and the projector stay trainable, while the CLIP [34] encoders stay frozen. The projector is here to make sure the feature vectors in an appropriate dimension for later use.

# 3. OVSS Based on Large Pretrained Models

Beyond the above weakly-supervised OVSS approaches, some works follow the training-free or inference-only paradigm [19, 23, 39]. These methods often depend on the powerful capabilities of the large-scale pretrained models by refining their mid-term outputs instead of end-to-end inference. Some other weakly supervised methods also fall under this paradigm [22, 54]. For example, ProxyCLIP [23] builds upon powerful pretrained segmentation models such as SAM [21] and DINO [17], while DPSeg [54] relies on Stable Diffusion [37] for visual prompting. We acknowledge the value of these explorations that leverage large pretrained models, however, they inevitably sacrifice lightweightness and efficiency.

To keep efficiency, we construct our method, SynSeg, in an end-to-end scheme without relying on any large pretrained models. We provide a simple comparison below in Table 1 to show the difference. The results are tested on an RTX 4090 GPU.

# 4. Approach

In this section, we present the overall pipeline design along with detailed descriptions of the key components.

<table><tr><td>Method</td><td>End-to-End</td><td>Param.</td><td>Lantency</td><td>FPS</td></tr><tr><td>SynSeg (Ours)</td><td>Yes</td><td>151M</td><td>14 ms</td><td>71</td></tr><tr><td>TCL</td><td>Yes</td><td>178M</td><td>13 ms</td><td>76</td></tr><tr><td>ProxyCLIP</td><td>No</td><td>243M</td><td>58 ms</td><td>17</td></tr><tr><td>DPSeg</td><td>No</td><td> $\sim 1.2B$ </td><td>-</td><td>-</td></tr></table>

Table 1. Comparison of model parameters and inference speed on different types of OVSS pipelines.

# 4.1. Overview of SynSeg

Our pipeline, named SynSeg, is illustrated in Fig. 2. The pre-trained CLIP [34] visual and textual encoders process the input image and text labels, respectively, to extract single-modal embeddings. These embeddings are then fused using a Feature-wise Linear Modulation (FiLM) [33] module. Specifically, the FiLM module contains a small learnable MLP that takes the text features as input and outputs channel-wise scaling and shifting parameters. These parameters are then directly applied to the visual features to generate the conditional visual vectors. Meanwhile, textual embeddings are stored as semantic feature vectors for intra-category alignment later.

During inference, the conditional visual features are passed through the decoder, generating semantic-activation maps, which are similar to class activation mapping (CAM) [55]. Then, the semantic-activation maps are thresholded to generate the final segmentation outputs. Besides CLIP encoders, SynSeg does not utilize any large pretrained models and follows an end-to-end paradigm, which enables efficient inference.

# 4.2. Multi-Category Contrastive Learning

We propose Multi-Category Contrastive Learning (MCCL) as weak supervision training objective tailored for OVSS scenarios. This strategy not only considers the intracategory correlation, but also introduces rich inter-category knowledge. Specifically, it integrates four loss functions as contrastive objectives that collaboratively and adversarially optimize semantic localization. Cosine similarity is used as the distance metric in the high-dimensional space for both positive and negative sample pairs. Note that we clip the cosine similarities into [0.005, 0.995], so the values remain positive.

Formally, for a given image I, let $\mathcal { C } _ { I } = \{ c _ { 1 } , c _ { 2 } , \ldots , c _ { N _ { I } } \}$ denote the set of $N _ { I }$ semantic categories (or object classes) present in the image, where $N _ { I }$ varies across different images. Through our model, for each category $c _ { i } \in \mathcal { C } _ { I }$ , we generate a pair of synergy feature vectors that correspond to the visual foreground and background regions guided by the semantic-activation map of $c _ { i }$ . These feature vectors are denoted as $f _ { c _ { i } }$ and ${ \bar { f } } _ { c _ { i } } .$ , respectively. The complete sets of foreground and background synergy features for image I can thus be expressed as:

$$
\mathcal {F} _ {I} = \{f _ {c _ {i}} \mid c _ {i} \in \mathcal {C} _ {I} \}, \quad \bar {\mathcal {F}} _ {I} = \{\bar {f} _ {c _ {i}} \mid c _ {i} \in \mathcal {C} _ {I} \}. \tag {1}
$$

To further integrate textual information, we leverage the CLIP text encoder to generate semantic feature vectors for the text prompts associated with the semantic categories, incorporating them into the Multi-Category Contrastive Learning framework:

$$
\mathcal {T} _ {I} = \left\{t _ {c _ {i}} = \mathrm{CLIP} _ {t} (c _ {i}) \mid c _ {i} \in \mathcal {C} _ {I} \right\} \tag {2}
$$

where $\mathrm { C L I P } _ { t } ( \cdot )$ denotes the CLIP text encoder, and $t _ { c _ { i } } \in$ Rd is the d-dimensional semantic embedding of category ci. $\mathbb { R } ^ { d }$ $c _ { i } .$ These semantic feature vectors serve as anchors for intracategory semantic alignment.

To encourage intra-category semantic alignment between the visual synergy features and the corresponding textual representations, we introduce the first loss function, $L _ { \mathrm { a l i g n } }$ . For a given image I, this loss maximizes the cosine similarity between each foreground synergy feature $f _ { c _ { i } } \in \mathcal { F } _ { I }$ and its corresponding semantic feature $t _ { c _ { i } } \in \mathcal { T } _ { I }$ , across all categories $c _ { i } \in \mathcal { C } _ { I }$ . The alignment loss is defined as:

$$
L _ {\text { align }} (\mathcal {F} _ {I}, \mathcal {T} _ {I}) = - \frac {1}{N _ {I}} \sum_ {c _ {i} \in \mathcal {C} _ {I}} \log \left(\text { sim } (f _ {c _ {i}}, t _ {c _ {i}})\right), \tag {3}
$$

where sim $\imath ( \cdot , \cdot )$ denotes the cosine similarity function, and $N _ { I } = | \mathcal { C } _ { I } |$ | is the number of semantic categories present in image I.

To enhance the quality of segmentation boundaries, we introduce the second loss function, $L _ { \mathrm { { c o n t } } }$ , which performs intra-category separation through contrastive learning between foreground and background regions of the same semantic category. For each category $c _ { i } \in \mathcal { C } _ { I }$ , this loss minimizes the cosine similarity between the corresponding foreground and background synergy feature vectors $f _ { c _ { i } } \in \mathcal { F } _ { I }$ and $\bar { f } _ { c _ { i } } \in \bar { \mathcal { F } } _ { I }$ . The contrastive loss is defined as:

$$
L _ {\text { cont }} (\mathcal {F} _ {I}, \bar {\mathcal {F}} _ {I}) = - \frac {1}{N _ {I}} \sum_ {c _ {i} \in \mathcal {C} _ {I}} \log \left(1 - \text { sim } (f _ {c _ {i}}, \bar {f} _ {c _ {i}})\right), \tag {4}
$$

where $N _ { I } = | \mathcal { C } _ { I } |$ is the number of categories in image I.

Inter-category alignment loss is set to limit the unlimited expansion of the foreground segmentation. It also aligns background synergy features corresponding to different categories within the same image, since background regions associated with different categories often exhibit spatial overlap. For a given image I, $L _ { \mathrm { b a c k } }$ maximizes the cosine similarity between all background synergy features $\bar { f } _ { c _ { i } } \in \bar { \mathcal { F } } _ { I }$ associated with each category $c _ { i } \in \mathcal { C } _ { I }$ . It is defined as:

$$
L _ {\text { back }} (\bar {\mathcal {F}} _ {I}) = - \frac {1}{N _ {I} ^ {\text { pair }}} \sum_ {c _ {j}, c _ {k} \in \mathcal {C} _ {I}} \log \left(\text { sim } (\bar {f} _ {c _ {j}}, \bar {f} _ {c _ {k}})\right) \tag {5}
$$

where $\bar { f } _ { c _ { j } } , \bar { f } _ { c _ { k } } \in \bar { \mathcal { F } } _ { I }$ are the background synergy features for categories $c _ { j }$ and $c _ { k }$ , and $N _ { I } ^ { \mathrm { p a i r } } = { N _ { I } } ^ { 2 }$ is the number of category pairs in image I.

To enhance the inter-category separation of individual semantic areas within the same image, we introduce the fourth loss function, $L _ { \mathrm { s e p } } ,$ as a key component of our Multi-Category Contrastive Learning framework. For a given image $I ,$ this loss minimizes the cosine similarity between foreground synergy features associated with different semantic categories, promoting inter-category feature disentanglement. It is formally defined as:

$$
L _ {\text { sep }} \left(\mathcal {F} _ {I}\right) = - \frac {1}{N _ {I} ^ {\text { pair }}} \sum_ {c _ {j}, c _ {k} \in \mathcal {C} _ {I}} \log \left(1 - \operatorname{sim} \left(f _ {c _ {j}}, f _ {c _ {k}}\right)\right), \tag {6}
$$

where $f _ { c _ { j } } , f _ { c _ { k } } \in \mathcal { F } _ { I }$ are the foreground synergy features corresponding to semantic categories $c _ { j }$ and $c _ { k }$ in image $I ,$ and $N _ { I } ^ { \mathrm { p a i r } } = { N _ { I } } ^ { 2 }$ denotes the number of category pairs in $\mathcal { C } _ { I }$ .

Based on the four loss functions described above, we define the total loss $L _ { \mathrm { t o t a l } }$ as a weighted sum of all components, with each term controlled by a corresponding hyperparameter $\lambda _ { 1 } , \lambda _ { 2 } , \lambda _ { 3 }$ , and $\lambda _ { 4 }$ . The total loss is given by:

$$
L _ {\mathrm{total}} = \lambda_ {1} L _ {\mathrm{align}} + \lambda_ {2} L _ {\mathrm{cont}} + \lambda_ {3} L _ {\mathrm{back}} + \lambda_ {4} L _ {\mathrm{sep}}. (7)
$$

The loss functions defined above constitute a weaklysupervised training framework that relies solely on RGB images and their associated category text labels. Our proposed MCCL provides a significantly richer and more informative weak supervision signal compared to existing contrastive learning approaches, which typically operate on intra-category manner only.

# 4.3. Feature Synergy Structure

In the training phase, we introduce a new feature reconstruction framework, named Feature Synergy Structure (FSS), inspired by CCAM [48]. Our focus is on the postdecoder reconstruction of features after the segmentation stage, and these reconstructed features are then fed into MCCL. In the other words, FSS generate background and foreground feature vectors for each semantic category in one pass which are suitable for the subsequent MCCL.

Rather than running the visual encoder a second time, we rely on FSS to perform this reconstruction.The semanticactivation maps, which are class-specific heat maps, represent the continuous per-pixel response strength to a given semantic category and can be considered as attention maps for feature enhancement. Instead of applying thresholding, the semantic-activation maps are flattened and subsequently fused with conditional visual features, which are first projected to a compatible dimension via a convolutional-layerbased projector. This fusion is performed through matrix multiplication to generate the synergy feature vectors. By flattening and weighting with semantic activation maps, the synergy vector emphasizes spatial regions with high semantic relevance, preserving contextual cues.

To ensure spatial-semantic consistency, the semanticactivation maps are duplicated and transposed such that each synergy feature vector corresponds to either the foreground or background region of the referred semantic category. Consequently, the synergy features can be separated into category-specific foreground and background representations, respectively. We can generate a set of foreground and background synergy features corresponding to each semantic category within a single image, which can provide richer and more diverse positive and negative sample pairs for effective MCCL later. This feature fusion mechanism enables the integration of semantic context and fine-grained visual cues, thereby enhancing the discriminative power and expressiveness of the learned representations.

Throughout the training process, only the FiLM fusion module, the projector, and the transformer decoder parameters are updated, while the CLIP visual and textual encoders remain frozen. This ensures the effective leverage of the rich features from the pre-trained visual language model.

# 5. Experiments

In this section, we describe the implementation details of our experiments and report the corresponding results.

# 5.1. Experiment Setup

Training datasets. We use the public conceptual-12m (CC12M) [5] as training dataset. After using the NLP functions from the SpaCy library [15], nouns and noun phrases are extracted from these captions. Non-referential or irrelevant terms such as direction and unit nouns (e.g., southwest, pair, front) are filtered out, leaving meaningful text labels that provide weak supervision for the associated images. We resize the figures to the same pixel size of 224 × 224 for training.

Evaluating datasets. To evaluate the open vocabulary semantic segmentation performance of our method, we test it on five commonly used challenging datasets: PAS-CAL VOC (VOC) [12], Pascal Context (Context) [31], City Scapes (City) [8] , COCO Object (Object) and COCO Stuff (Stuff) [1, 26]. Also, it should be noted that evaluations on VOC and Object treat unlabeled regions as an explicit category background, whereas those on Context, Stuff and City focus solely on labeled categories.

Baselines. To provide a comprehensive comparison, we select not only the latest but also classical weaklysupervised learning methods as baselines. The eight representative baselines are listed below: GroupViT [50], ViewCo [36], CoCu [49], OVSegmentor, TCL [4], CoDe [47], MGCA [28] and S-Seg[22]. All baseline methods are assumed to use a pre-trained ViT-B/16 vision backbone for fair comparison, except S-Seg [22], which does not specify the type of vision model used in the inference stage. These methods may use extra training datasets such as CC3M [38], YFCC14M [42] and RedCaps12M [10].

Training Details. We use a pre-trained CLIP Vit-B/16 model as the encoder. The decoder follows the design of CLIPSeg [29] and is initialized with the pre-trained weights from CLIPseg. For training, we keep the encoder frozen and only the decoder and the FiLM fusion module remain trainable. All of the experiments are performed on an RTX 4090 GPU.

# 5.2. Main Results

We compare our proposed method, SynSeg, an end-toend lightweight solution against a range of classic and latest weakly-supervised open-vocabulary semantic segmentation approaches that rely on text annotations, across five widely-used benchmark datasets (Tab. 2). The table reports the mean Intersection-over-Union (mIoU) score for each method on individual datasets. The result in boldface achieves the best performance and the underlined result is the second best. SynSeg achieves the best overall performance, with an average mIoU of 38.7%, outperforming all baselines by a significant margin. Notably, our method sets a new state-of-the-art on four out of five datasets: VOC (62.2%), Context (41.8%), Object (34.9%), and City (30.9%). To better understand, SynSeg achieves higher segmentation accuracy than SOTA baselines with a ratio from 6.9% up to 26.2%.

# 5.3. Ablation Study

We examine the effectiveness of the four training objectives by evaluating the impact on segmentation performance of all four loss functions across three representative datasets: Context [31], Object [26] and Stuff [1]. The results, presented in Tab. 3, show that the combination of all four losses yields the best performance. Removing any single loss leads to a measurable drop in performance, underscoring the complementary contributions of each component in enhancing feature discrimination and segmentation quality. In particular, the inter-category separation loss $L _ { s e p }$ is the most prominent because the drop is the largest after it is removed.

<table><tr><td>Method</td><td>Publication</td><td>Training Datasets</td><td>VOC</td><td>Context</td><td>Object</td><td>Stuff</td><td>City</td><td>Avg.</td></tr><tr><td>GroupViT</td><td>CVPR 2022</td><td>CC3M+CC12M+RedCaps12M</td><td>50.4</td><td>23.4</td><td>27.5</td><td>15.3</td><td>11.1</td><td>25.5</td></tr><tr><td>ViewCo</td><td>ICLR 2023</td><td>CC12M+YFCC14M</td><td>52.4</td><td>23.0</td><td>23.5</td><td>-</td><td>-</td><td>-</td></tr><tr><td>CoCu</td><td>NeurIPS 2023</td><td>CC3M+CC12M+YFCC14M</td><td>51.4</td><td>-</td><td>22.7</td><td>15.2</td><td>22.1</td><td>-</td></tr><tr><td>OVSegmentor</td><td>CVPR 2023</td><td>CC12M</td><td>53.8</td><td>20.4</td><td>25.1</td><td>-</td><td>-</td><td>-</td></tr><tr><td>TCL</td><td>CVPR 2023</td><td>CC3M+CC12M</td><td>55.0</td><td>33.9</td><td>31.6</td><td>22.4</td><td>24.0</td><td>33.4</td></tr><tr><td>CoDe</td><td>CVPR 2024</td><td>CC3M+CC12M</td><td>57.7</td><td>30.5</td><td>32.3</td><td>23.9</td><td>28.9</td><td>34.7</td></tr><tr><td>S-Seg</td><td>CVPR 2025</td><td>CC3M+CC12M</td><td>53.2</td><td>27.2</td><td>30.3</td><td>-</td><td>-</td><td>-</td></tr><tr><td>MGCA</td><td>TMC 2025</td><td>CC3M</td><td>53.1</td><td>33.7</td><td>31.9</td><td>22.0</td><td>24.0</td><td>32.9</td></tr><tr><td>SynSeg (Ours)</td><td>-</td><td>CC12M</td><td>62.2</td><td>41.8</td><td>34.9</td><td>23.6</td><td>30.9</td><td>38.7</td></tr></table>

Table 2. Zero-shot semantic segmentation comparisons among weakly-supervised OVSS methods on five representative datasets. Bold indicates best performance; underlined values are second-best. Results are in mIoU (%), which higher is better.

![](images/51cf74730c4e938d0c37e47cfb4208bf9e05ffc3e192073547fec498a71c2306.jpg)



Figure 3. Visual effects of the semantic activation maps and segmentations under different thresholds.

# 5.4. Visual Effects

In this subsection, we present two types of visual examples to demonstrate the segmentation performance of our method, SynSeg, and also in comparison with existing baselines. The examples are selected from the Context dataset [31], as it is a common benchmark supported by all baseline methods.

<table><tr><td rowspan="2"> $L_{align}$ </td><td colspan="3">Loss</td><td colspan="3">MIoU(%)</td></tr><tr><td> $L_{cont}$ </td><td> $L_{back}$ </td><td> $L_{sep}$ </td><td>Context</td><td>Object</td><td>Stuff</td></tr><tr><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td><td>41.8</td><td>34.9</td><td>23.6</td></tr><tr><td>Yes</td><td>Yes</td><td>Yes</td><td>No</td><td>39.6</td><td>31.0</td><td>20.9</td></tr><tr><td>Yes</td><td>Yes</td><td>No</td><td>Yes</td><td>41.4</td><td>34.0</td><td>22.9</td></tr><tr><td>Yes</td><td>No</td><td>Yes</td><td>Yes</td><td>41.5</td><td>34.3</td><td>23.2</td></tr><tr><td>No</td><td>Yes</td><td>Yes</td><td>Yes</td><td>41.4</td><td>34.2</td><td>23.2</td></tr></table>

Table 3. Ablation study on the training objectives.

We begin by presenting a qualitative example of semantic activation maps and the corresponding segmentation masks predicted by our model under multiple threshold settings, as illustrated in Fig. 3. The example involves five semantic categories: bicycle, car, person, grass, and tree. Unlike traditional OVSS where pixel-level predictions are mutually exclusive [4, 50], our semantic activation maps allow a single pixel to be activated by multiple categories simultaneously. This fits the nature in real-world environments, especially when the objects are physically entangled, for example, between the head and the person.

![](images/4a2e1674d349cd53a365e238f193869c9c18db36229f1ffb484e50475744b0dd.jpg)



Figure 4. Segmentation visual comparisons. The light blue regions indicate the segmentation predictions. The baselines’ results are visually compared with our method, SynSeg.

Also, we observe that the segmentation results remain visually consistent across a wide range of thresholds, nearly from 0.1 to 0.6, particularly for prominent object categories such as person and taxi. This indicates that the model has an accurate semantic localization ability so that it produces clear boundaries. Moreover, for less salient or texture-heavy classes like grass, where activation may be weaker or more diffused, the model still successfully captures the core regions while gracefully discarding noise at lower thresholds. This demonstrates the model’s ability to balance coarse and fine semantics through a unified representation framework.

In addition, we conduct visual comparisons between our method and existing methods. Our comparison includes weakly-supervised approaches GroupViT [50] and TCL [4], and a strong training-free baseline ProxyCLIP [23]. ProxyCLIP utilizes a large-scale pretrained Vision Foundation Model (VFM) DINO [17] for OVSS task. As shown in Fig. 4, our method consistently demonstrates more accurate semantic localization and finer-grained segmentation. The predicted segmentations from our model are better aligned with the object boundaries and exhibit fewer false positives.

In general, our segmentation results show superior performance in both salient and background categories. For salient objects such as bus, cat, and dog, our model produces tighter and more precise boundaries, with reduced over-segmentation compared to others which only Proxy-CLIP performs competitively. For background regions such as floor and road, our method significantly outperforms all baselines. ProxyCLIP tends to misclassify visually similar areas as background categories, while GroupViT and TCL often fail to produce coherent masks in these regions. These observations further demonstrate the robustness of our method.

# 6. Conclusion

We propose a novel approach, SynSeg, for end-to-end open-vocabulary semantic segmentation, integrating Feature Synergy Structure (FSS) with Multi-Category Contrastive Learning (MCCL). Our approach effectively addresses two key challenges in weakly-supervised OVSS: (1) the lack of explicit inter-category correlation injection during training, and (2) the absence of a suitable way of feature reconstruction tailored for contrastive learning. To address these issues, we introduced MCCL that constructs both intra- and inter-category contrastive learning to enhance the weakly-supervised signal. In addition, FSS generates category-aware features by fusing conditional visual embeddings with semanticactivation maps, enabling finer semantic representation for effective MCCL. Experiments on five benchmarks demonstrate the effectiveness of our method. SynSeg consistently outperforms existing weakly-supervised baselines in OVSS, achieving state-of-the-art performance.

# References

[1] Holger Caesar, Jasper Uijlings, and Vittorio Ferrari. Cocostuff: Thing and stuff classes in context. In 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 1209–1218, 2018. 2, 6   
[2] Kaixin Cai, Pengzhen Ren, Yi Zhu, Hang Xu, Jianzhuang Liu, Changlin Li, Guangrun Wang, and Xiaodan Liang. Mixreorg: Cross-modal mixed patch reorganization is a good mask learner for open-world semantic segmentation. In 2023 IEEE/CVF International Conference on Computer Vision (ICCV), pages 1196–1205, 2023. 3   
[3] Senay Cakir, Marcel Gauß, Kai Happeler, Yassine Ounajjar, ¨ Fabian Heinle, and Reiner Marchthaler. Semantic segmentation for autonomous driving: Model evaluation, dataset generation, perspective comparison, and real-time capability, 2022. 1   
[4] Junbum Cha, Jonghwan Mun, and Byungseok Roh. Learning to generate text-grounded mask for open-world semantic segmentation from only image-text pairs. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023. 1, 2, 3, 6, 8   
[5] Soravit Changpinyo, Piyush Sharma, Nan Ding, and Radu Soricut. Conceptual 12m: Pushing web-scale image-text pretraining to recognize long-tail visual concepts, 2021. 6   
[6] Jun Chen, Deyao Zhu, Guocheng Qian, Bernard Ghanem, Zhicheng Yan, Chenchen Zhu, Fanyi Xiao, Sean Chang Culatana, and Mohamed Elhoseiny. Exploring open-vocabulary semantic segmentation from clip vision encoder distillation only. In 2023 IEEE/CVF International Conference on Computer Vision (ICCV), pages 699–710, 2023. 3   
[7] Seokju Cho, Heeseong Shin, Sunghwan Hong, Anurag Arnab, Paul Hongsuck Seo, and Seungryong Kim. Cat-seg: Cost aggregation for open-vocabulary semantic segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 4113– 4123, 2024. 1   
[8] Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler, Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele. The cityscapes dataset for semantic urban scene understanding. In Proc. of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016. 6   
[9] Songhe Deng, Wei Zhuo, Jinheng Xie, and Linlin Shen. Qaclims: Question-answer cross language image matching for weakly supervised semantic segmentation. In Proceedings of the 31st ACM International Conference on Multimedia, pages 5572–5583, 2023. 3   
[10] Karan Desai, Gaurav Kaul, Zubin Aysola, and Justin Johnson. RedCaps: Web-curated image-text data created by the people, for the people. In NeurIPS Datasets and Benchmarks, 2021. 6   
[11] Zheng Ding, Jieke Wang, and Zhuowen Tu. Openvocabulary universal image segmentation with maskclip. In Proceedings of the 40th International Conference on Machine Learning. JMLR.org, 2023. 1, 2, 3   
[12] Mark Everingham, Luc Gool, Christopher K. Williams, John Winn, and Andrew Zisserman. The pascal visual object

classes (voc) challenge. Int. J. Comput. Vision, 88(2): 303–338, 2010. 6   
[13] Golnaz Ghiasi, Xiuye Gu, Yin Cui, and Tsung-Yi Lin. Scaling open-vocabulary image segmentation with image-level labels. In Computer Vision – ECCV 2022: 17th European Conference, Tel Aviv, Israel, October 23–27, 2022, Proceedings, Part XXXVI, page 540–557, Berlin, Heidelberg, 2022. Springer-Verlag.   
[14] Ruohao Guo, Liao Qu, Dantong Niu, Yanyu Qi, Wenzhen Yue, Ji Shi, Bowei Xing, and Xianghua Ying. Openvocabulary audio-visual semantic segmentation. In Proceedings of the 32nd ACM International Conference on Multimedia, page 7533–7541, New York, NY, USA, 2024. Association for Computing Machinery. 3   
[15] Matthew Honnibal and Ines Montani. spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing. To appear, 2017. 6   
[16] Alexander Jaus, Constantin Marc Seibold, Simon Reiß, Zdravko Marinov, Keyi Li, Zeling Ye, Stefan Krieg, Jens Kleesiek, and Rainer Stiefelhagen. Every component counts: Rethinking the measure of success for medical semantic segmentation in multi-instance segmentation tasks. Proceedings of the AAAI Conference on Artificial Intelligence, 39 (4):3904–3912, 2025. 1   
[17] Cijo Jose, Theo Moutakanni, Dahyun Kang, Federico ´ Baldassarre, Timothee Darcet, Hu Xu, Daniel Li, Marc ´ Szafraniec, Michael Ramamonjisoa, Maxime Oquab, Oriane¨ Simeoni, Huy V. Vo, Patrick Labatut, and Piotr Bojanowski. ´ Dinov2 meets text: A unified framework for image- and pixel-level vision-language alignment, 2024. 4, 8   
[18] Mithun Kumar Kar, Malaya Kumar Nath, and Debanga Raj Neog. A review on progress in semantic image segmentation and its application to medical images. SN Computer Science, 2(5):397, 2021. 1   
[19] Chanyoung Kim, Dayun Ju, Woojung Han, Ming-Hsuan Yang, and Seong Jae Hwang. Distilling spectral graph for object-context aware pen-vocabulary semantic segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2025. 4   
[20] Dahun Kim, Tsung-Yi Lin, Anelia Angelova, In So Kweon, and Weicheng Kuo. Learning open-world object proposals without learning to classify. IEEE Robotics and Automation Letters, 7(2):5453–5460, 2022. 3   
[21] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollar, and ´ Ross Girshick. Segment anything. In 2023 IEEE/CVF International Conference on Computer Vision (ICCV), pages 3992–4003, 2023. 4   
[22] Zihang Lai. Exploring simple open-vocabulary semantic segmentation, 2024. 1, 3, 4, 6   
[23] Mengcheng Lan, Chaofeng Chen, Yiping Ke, Xinjiang Wang, Litong Feng, and Wayne Zhang. Proxyclip: Proxy attention improves clip for open-vocabulary segmentation. In Computer Vision – ECCV 2024: 18th European Conference, Milan, Italy, September 29–October 4, 2024, Proceedings, Part LXVIII, page 70–88, Berlin, Heidelberg, 2024. Springer-Verlag. 1, 4, 8

[24] Junnan Li, Ramprasaath Selvaraju, Akhilesh Gotmare, Shafiq Joty, Caiming Xiong, and Steven Chu Hong Hoi. Align before fuse: Vision and language representation learning with momentum distillation. In Advances in Neural Information Processing Systems, pages 9694–9705. Curran Associates, Inc., 2021. 3   
[25] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. BLIP: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In Proceedings of the 39th International Conference on Machine Learning, pages 12888–12900. PMLR, 2022. 3   
[26] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar, and C. Lawrence´ Zitnick. Microsoft coco: Common objects in context. In Computer Vision – ECCV 2014, pages 740–755, Cham, 2014. Springer International Publishing. 2, 6   
[27] Quande Liu, Youpeng Wen, Jianhua Han, Chunjing Xu, Hang Xu, and Xiaodan Liang. Open-world semantic segmentation via contrasting and clustering vision-language embedding. In Computer Vision – ECCV 2022: 17th European Conference, Tel Aviv, Israel, October 23–27, 2022, Proceedings, Part XX, page 275–292, Berlin, Heidelberg, 2022. Springer-Verlag. 1, 3   
[28] Yajie Liu, Pu Ge, Guodong Wang, Qingjie Liu, and Di Huang. Multi-grained contrastive learning for textsupervised open-vocabulary semantic segmentation. ACM Trans. Multimedia Comput. Commun. Appl., 21(3), 2025. 6   
[29] Timo Luddecke and Alexander Ecker. Image segmenta- ¨ tion using text and image prompts. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 7086–7096, 2022. 6   
[30] Huaishao Luo, Junwei Bao, Youzheng Wu, Xiaodong He, and Tianrui Li. Segclip: patch aggregation with learnable centers for open-vocabulary semantic segmentation. In Proceedings of the 40th International Conference on Machine Learning. JMLR.org, 2023. 1, 3   
[31] Roozbeh Mottaghi, Xianjie Chen, Xiaobai Liu, Nam-Gyu Cho, Seong-Whan Lee, Sanja Fidler, Raquel Urtasun, and Alan Yuille. The role of context for object detection and semantic segmentation in the wild. In 2014 IEEE Conference on Computer Vision and Pattern Recognition, pages 891– 898, 2014. 6, 7   
[32] Jishnu Mukhoti, Tsung-Yu Lin, Omid Poursaeed, Rui Wang, Ashish Shah, Philip H.S. Torr, and Ser-Nam Lim. Open vocabulary semantic segmentation with patch aligned contrastive learning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 19413–19423, 2023. 1, 2, 3   
[33] Ethan Perez, Florian Strub, Harm de Vries, Vincent Dumoulin, and Aaron Courville. Film: visual reasoning with a general conditioning layer. In Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence and Thirtieth Innovative Applications of Artificial Intelligence Conference and Eighth AAAI Symposium on Educational Advances in Artificial Intelligence. AAAI Press, 2018. 4   
[34] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry,

Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. In Proceedings of the 38th International Conference on Machine Learning, pages 8748–8763. PMLR, 2021. 2, 3, 4   
[35] Yongming Rao, Wenliang Zhao, Guangyi Chen, Yansong Tang, Zheng Zhu, Guan Huang, Jie Zhou, and Jiwen Lu. Denseclip: Language-guided dense prediction with contextaware prompting. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2022. 2, 3   
[36] Pengzhen Ren, Changlin Li, Hang Xu, Yi Zhu, Guangrun Wang, Jianzhuang Liu, Xiaojun Chang, and Xiaodan Liang. Viewco: Discovering text-supervised segmentation masks via multi-view semantic consistency. In The Eleventh International Conference on Learning Representations, 2023. 6   
[37] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bjorn Ommer. High-resolution image ¨ synthesis with latent diffusion models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 10684–10695, 2022. 4   
[38] Piyush Sharma, Nan Ding, Sebastian Goodman, and Radu Soricut. Conceptual captions: A cleaned, hypernymed, image alt-text dataset for automatic image captioning. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 2556–2565, Melbourne, Australia, 2018. Association for Computational Linguistics. 6   
[39] Yuheng Shi, Minjing Dong, and Chang Xu. Harnessing vision foundation models for high-performance, training-free open vocabulary segmentation. arXiv preprint arXiv:2411.09219, 2024. 4   
[40] Wenfang Sun, Yingjun Du, Gaowen Liu, Ramana Kompella, and Cees G. M. Snoek. Training-free semantic segmentation via llm-supervision. CoRR, abs/2404.00701, 2024. 3   
[41] Shiyu Tang, Zhaofan Luo, Yifan Wang, Lijun Wang, Huchuan Lu, Weibo Su, and Libo Liu. Lovd: Large-andopen vocabulary object detection. In Proceedings of the 32nd ACM International Conference on Multimedia, page 9321–9329, New York, NY, USA, 2024. Association for Computing Machinery. 3   
[42] Bart Thomee, David A. Shamma, Gerald Friedland, Benjamin Elizalde, Karl Ni, Douglas Poland, Damian Borth, and Li-Jia Li. Yfcc100m: the new data in multimedia research. Commun. ACM, 59(2):64–73, 2016. 6   
[43] Haoxiang Wang, Pavan Kumar Anasosalu Vasu, Fartash Faghri, Raviteja Vemulapalli, Mehrdad Farajtabar, Sachin Mehta, Mohammad Rastegari, Oncel Tuzel, and Hadi Pouransari. Sam-clip: Merging vision foundation models towards semantic and spatial understanding. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops, pages 3635–3647, 2024. 3   
[44] Li Wang, Dong Li, Han Liu, JinZhang Peng, Lu Tian, and Yi Shan. Cross-dataset collaborative learning for semantic segmentation in autonomous driving. Proceedings of the AAAI Conference on Artificial Intelligence, 36(3):2487– 2494, 2022. 1

[45] Zirui Wang, Jiahui Yu, Adams Wei Yu, Zihang Dai, Yulia Tsvetkov, and Yuan Cao. SimVLM: Simple visual language model pretraining with weak supervision. In International Conference on Learning Representations, 2022. 3   
[46] Zishuo Wang, Wenhao Zhou, Jinglin Xu, and Yuxin Peng. Sia-ovd: Shape-invariant adapter for bridging the imageregion gap in open-vocabulary detection. In Proceedings of the 32nd ACM International Conference on Multimedia, page 4986–4994, New York, NY, USA, 2024. Association for Computing Machinery. 3   
[47] Ji-Jia Wu, Andy Chia-Hao Chang, Chieh-Yu Chuang, Chun-Pei Chen, Yu-Lun Liu, Min-Hung Chen, Hou-Ning Hu, Yung-Yu Chuang, and Yen-Yu Lin. Image-text codecomposition for text-supervised semantic segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 26794–26803, 2024. 1, 2, 3, 6   
[48] Jinheng Xie, Jianfeng Xiang, Junliang Chen, Xianxu Hou, Xiaodong Zhao, and Linlin Shen. C2am: Contrastive learning of class-agnostic activation map for weakly supervised object localization and semantic segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 989–998, 2022. 6   
[49] Yun Xing, Jian Kang, Aoran Xiao, Jiahao Nie, Shao Ling, and Shijian Lu. Rewrite caption semantics: Bridging semantic gaps for language-supervised semantic segmentation. In Advances in Neural Information Processing Systems, 2023. 1, 3, 6   
[50] Jiarui Xu, Shalini De Mello, Sifei Liu, Wonmin Byeon, Thomas Breuel, Jan Kautz, and Xiaolong Wang. Groupvit: Semantic segmentation emerges from text supervision. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 18134–18144, 2022. 1, 3, 6, 8   
[51] Jilan Xu, Junlin Hou, Yuejie Zhang, Rui Feng, Yi Wang, Yu Qiao, and Weidi Xie. Learning open-vocabulary semantic segmentation models from natural language supervision. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 2935–2944, 2023. 1   
[52] Muyang Yi, Quan Cui, Hao Wu, Cheng Yang, Osamu Yoshie, and Hongtao Lu. A simple framework for textsupervised semantic segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 7071–7080, 2023. 1   
[53] Pengchuan Zhang, Xiujun Li, Xiaowei Hu, Jianwei Yang, Lei Zhang, Lijuan Wang, Yejin Choi, and Jianfeng Gao. Vinvl: Revisiting visual representations in vision-language models. In 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 5575–5584, 2021. 3   
[54] Ziyu Zhao, Xiaoguang Li, Linjia Shi, Nasrin Imanpour, and Song Wang. Dpseg: Dual-prompt cost volume learning for open-vocabulary semantic segmentation. In 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 25346–25356, 2025. 4   
[55] Bolei Zhou, Aditya Khosla, Agata Lapedriza, Aude Oliva, and Antonio Torralba. Learning deep features for discriminative localization. In 2016 IEEE Conference on Computer

Vision and Pattern Recognition (CVPR), pages 2921–2929, 2016. 4   
[56] C¸ agrı Kaymak and Ays¸eg ˘ ul Uc¸ar. A brief survey and an ¨ application of semantic image segmentation for autonomous driving, 2018. 1