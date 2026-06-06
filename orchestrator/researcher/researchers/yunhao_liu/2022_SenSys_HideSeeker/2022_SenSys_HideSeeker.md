# HideSeeker: Uncover the Hidden Gems in Obfuscated Images

Suyuan Liu1,2, Lan Zhang1,2, Haikuo Yu1,2, Jiahui Hou1,2, Kaiwen Guo1,2, Xiang-Yang Li1,2∗

1 School of Computer Science and Technology, University of Science and Technology of China

2 CAS Key Laboratory of Wireless-Optical Communications, USTC

{lsysue,yhk7786,kevinguo}@mail.ustc.edu.cn,{zhanglan,xiangyangli}@ustc.edu.cn,jhhou.cs@gmail.com

# ABSTRACT

A number of obfuscation technologies have been well established for on-device image privacy protection, including pixelation, blurring, scribbling, sticker-covering, and inpainting. Despite their remarkable resistance to human observation, recent studies find that some of them are vulnerable to attacks by neural network-based recognition methods. In this work, we reveal the risk of privacy re-disclosure post the protection. Given an obfuscation-protected image, the privacy information includes 1) where the obfuscated region is and 2) what the hidden privacy-related objects are. Thus we focus on uncovering categories of privacy-related objects to evaluate the effectiveness of obfuscation technologies. Under severe obfuscation, unfortunately, even powerful object recognition models can hardly infer the privacy information.

Inspired by the human observation process, we carefully craft a scheme, called HideSeeker, composed of feature-extraction, relationgraph-learning, and object-inference, to explore the contextual information of obfuscated regions and their relationships. HideSeeker can efficiently and effectively uncover the categories of hidden private objects in obfuscated images. We conduct comprehensive evaluations over two kinds of datasets containing 14206 images in total: laboratory-generated and publicly available obfuscated images. Our results demonstrate that HideSeeker successfully uncovers privacy-related objects with inference accuracy of up to 82 17%, and 77 72% on average no matter which obfuscation was . .applied, while the SOTA method can achieve an average accuracy of 42 3%. For images protected by inpainting, accuracy is improved .from 24 67% to 78 16%.

# CCS CONCEPTS

• Security and privacy → Usability in security and privacy; Privacy protections.

# ACM Reference Format:

Suyuan Liu1 2, Lan Zhang1 2, Haikuo Yu1 2, Jiahui Hou1 2, Kaiwen Guo1 2, Xiang-Yang Li1 2. 2022. HideSeeker: Uncover the Hidden Gems in Obfuscated Images. In The 20th ACM Conference on Embedded Networked Sensor Systems (SenSys ’22), November 6–9, 2022, Boston, MA, USA. ACM, New York, NY, USA, 14 pages. https://doi.org/10.1145/3560905.3568514

# 1 INTRODUCTION

In recent years, users’ demand for cloud storage and online sharing of photos has raised public concerns about image privacy protection [27, 36, 37, 45, 54]. Unfortunately, the networking between the camera and online services is always untrustworthy. As we show in Figure 1, once intercepted by an adversary during uploading, the photos may result in privacy leakage of sensitive information including location, social relationship, personal preference, etc. Figure 2(a) illustrates several images leaking various sensitive information.

![](images/abb56a33131c1f8e53d13212291487e91b264f5524ab5f25a46410184245c1ea.jpg)



Figure 1: As the first row shows, when users rely on in-cloud protection, the privacy infomation may be at risk of leakage during the uploading. As the second row shows, our scheme HideSeeker works as an evaluation of on-device obfuscation technologies before the user sharing their photos. It allows users to hide their privacy more carefully based on our evaluation results.

Thus a growing number of studies [5, 51, 56] have developed ondevice systems attempting to preserve users’ privacy information. Users can also manually edit their photos with various obfuscation technologies before uploading or sharing. The most commonly used obfuscation technologies include pixelization, blurring, scribbling, sticker-covering, and inpainting. As the examples in Figure 2(b) show, these technologies can hide the users’ private details from human eyes as expected. However, naturally it comes a question: how effective are these technologies resisting attacks by adversarial algorithms? Early works [24, 26] demonstrated how neural networks defeat pixelization and blurring under the assumption that the adversary has access to a set of unobfuscated images for training. These works are inspiring, while the assumption that the adversary has access to a user’s face set or the original images is almost infeasible. From a different perspective, we evaluate the effectiveness of obfuscation technologies to raise a call for attention to their vulnerabilities. Since that exploring too many details of users’ privacy goes against our intention, we consider uncovering only the categories of privacy-related objects. Even if the privacyrelated objects are completely obscured or covered, we can still effectively and efficiently infer their categories.

![](images/fc76eb37afd45775a69f1e9627cfc5501697e69ea3ced9169d41839168eb977d.jpg)

![](images/f2ac0ca319764bae35dbcc8ba5d280512959f59c74756e2a5f3ce480a2e8bddf.jpg)  
(b) User- obfuscated images for privacy protection   
Figure 2: Several privacy-sensitive images and the userobfuscated ones. (a) From the left to right we show privacy concerns such as location, on-screen information, personal preference, personal relationships, and social activities. (b) the user-obfuscated ones using techniques such as pixelization, blurring, scribbling, sticker-covering, and inpainting.

Given an obfuscated image to be uploaded or shared, we care about the following two questions: Where are the obfuscated regions? What are the hidden objects? Existing works on image manipulation detection and localization have addressed the first two problems through noise inconsistency [55], local anomaly [2, 41], and other approaches [1, 20, 40, 58]. This work focuses on discovering the categories of objects hidden in obfuscated regions and then is confronted with several challenges. The applied obfuscation may completely cover privacy-related objects, sometimes even beyond their outlines. When privacy-related objects are completely obscured by obfuscation methods, it is infeasible to infer them from their visible parts. Moreover, these obfuscation methods may lead to the invalidity of the original visual features. Among these obfuscation technologies, pixelization and blurring redistribute some pixels in the target region, while scribbling and sticker-covering overwrite the original image pixels with irrelevant color values or stickers. Particularly, inpainting not only paints away privacyrelated objects, but also hides the location of obfuscated regions from human eyes. Obviously it is impossible to accurately infer the hidden objects given a black block. Therefore, we can hardly rely on regional visual features for object detection of obfuscated images.

There are some researches committed to handling partial occlusion in object detection [21, 39, 57]. Compositional Convolutional Neural Networks (CompNets) [21] achieved remarkable results in classifying partially occluded objects. However, relying on the visual features of visible parts of occluded objects, CompNets lose their advantages on severely occluded images. We show experimentally that the accuracy of CompNets declines sharply when the privacy-related objects are completely occluded.

To alleviate the negative impact of obfuscation-interfered visual features, we design a scheme called HideSeeker. We explore the contextual information of obfuscated regions rather than the regional visual features to infer hidden objects. Following the intuition from human-eye observation, we define the contextual information as the scene and recognizable objects co-occurred with the obfuscated region. We learn a relation graph to model the semantic and spatial relationship between the obfuscated regions and their context. We apply Gated Graph Neural Networks [22] to infer privacy-related objects that may appear in the semantic context.

Additionally, there is a lack of privacy-protected image datasets. The existing privacy datasets such as PicAlert [48], VizWiz [16], VISPR [27] annotate the private images with privacy-related attributes. None of these datasets labels the private parts in images. We develop our laboratory-generated obfuscated images (LGOI) dataset for analysis and experimental evaluation. Furthermore, we evaluate our scheme on publicly-available obfuscated images crawled from social platforms. These images are obfuscated by users and therefore reflect users’ real privacy concerns. Through a series of experiments, we show that our method can uncover the hidden objects under obfuscation. Our results show that HideSeeker performs significantly better than the state-of-the-art occlusionrobust object detection models. Further evaluations show that our scheme has its potential to generalize across unknown obfuscation methods.

To summarize, we propose a novel scheme HideSeeker to measure the effectiveness of privacy protection by uncovering the hidden objects in obfuscated images. Since the original visual features in the obfuscated regions are completely occluded or obscured, we turn our attention to the context of obfuscated regions. In our scheme HideSeeker, we model the relationships between the obfuscated regions and their contextual information via a semantic and spatial relation graph. We evaluate HideSeeker on both laboratorygenerated and publicly available obfuscated image datasets with 14206 images in total. Our experimental results show the remarkable performance of HideSeeker with the accuracy of up to 82 17% .and 77 72% on average over five different obfuscation technologies. Previous method CompNets achieves an average accuracy of 42 3%, and our method is 35 42% better than this state-of-the-art method. .When the images are obfuscated by inpainting, our method is 63 49% .better than the previously best method CompNets, improving the accuracy from 24 67% to 78 16%. We evaluate the generalizability of HideSeeker by training on images obfuscated by one specific method and testing on images obfuscated by other methods. For 100 (10×10) such combinations, the accuracy differs at most 7% over different obfuscation types. This illustrates the potential of our scheme to generalize to unknown obfuscation technologies. In addition, we recruit 10 volunteers to discover the hidden objects in 1000 obfuscated images. The accuracy of HideSeeker is nearly twice higher than that of human-based observation for inpainted images.

The remainder of this article proceeds as follows. We formulate the problem in Section 2. The overview and design details of our proposed method are illustrated in Section 3. We report our experimental results in Section 4. In Section 5 we discuss the related work. We conclude the paper with the discussion of possible future work in Section 6.

# 2 PROBLEM FORMULATION

# 2.1 Protecting Images

As we can see in Figure 2(b), users occlude their privacy information in images through obfuscation technologies. From our observation, the widely used obfuscation technologies include:

• Pixelization: Pixelization, also known as mosaicing, divides the privacy region into square grids and applies median filtering to the pixel values within grids.   
• Blurring: Blurring performs Gaussian filtering on the pixel values in the target area.   
• Scribbling: Scribbling allows users to paint on the privacy regions for obfuscation.   
• Sticker-covering: Like image splicing, sticker-covering means pasting another image or part of it on the privacy regions.   
• Inpainting: Image inpainting models fill in the pixel values in the target region with a given mask based on the plausible context.

Both pixelization and blurring perform a linear function to pixel values of privacy-related objects. Users can determine the parameters of functions such as pixelization grid size and Gaussian kernel size to maintain a balance between utility and privacy requirements. Considering the aesthetics of the obfuscated image, some users scribble on privacy-related objects or cover them with stickers. Both of them replace the original pixel values with new pixel values that are unrelated to them. Inpainting was introduced to simultaneously fill regions with surrounding information [3]. Traditional approaches deal with inpainting based on structure and texture synthesis [4]. Recent studies demonstrate that Generative Adversarial Network (GAN) is helpful for inpainting [7, 13, 34, 44].

Moreover, we consider the case that the obfuscation completely obscures or covers privacy-related objects, sometimes even going beyond their outlines. Thus the obfuscation minimizes the information a viewer can get about privacy-related objects.

# 2.2 Threat Model

We are more concerned about the resistance of obfuscation technologies against algorithms instead of that against human observation. We assume that the adversary has a set of publicly available unobfuscated images, such as the image dataset MS COCO [23] so that he can learn associations between objects and scenes. Besides, the adversary has access to a set of obfuscated images. For example, the adversary can collect user-obfuscated images from public social platforms.

We also assume that the adversary has the ability to detect and classify recognizable objects and scenes in images. More significantly, the adversary is able to localize the obfuscated regions with the help of image manipulation detection and localization models.

# 2.3 Problem Formulation

We illustrate the scenario where our proposed scheme works in Figure 1. On-device privacy protection for photos is always encouraged to alleviate privacy leakage risks in networking. To challenge the effectiveness of obfuscation-based protection, we uncover the categories of privacy-related objects hidden in obfuscated regions. When our scheme successfully infers the privacy information in the input image, we strongly suggest users hide their private information more carefully until the images escape our inference.

Given an obfuscated image, we assume there are $N _ { p }$ obfuscated Npregions, and each region only contains one object. Because of the obfuscation, we can hardly extract the original visual features of privacy-related objects for classification, thus we exploit the visual information outside the obfuscated regions in the image to infer the categories. Formally, we denote the visual information in the image as V and compute the probability of each object class that may be obfuscated in a given image. We infer the category of the hidden object as the object class with the highest probability:

$$
l ^ {p} = \arg \max _ {c \in C} P (c \mid \mathcal {V}), \tag {1}
$$

where C denotes the set of object classes. The symbols and their descriptions are listed in Table 1.

Table 1: Notations and symbols used in this paper. 

<table><tr><td colspan="2">Indices</td></tr><tr><td> $N_p$ </td><td>number of obfuscated regions.</td></tr><tr><td> $N_o$ </td><td>number of recognizable objects.</td></tr><tr><td colspan="2">Variables</td></tr><tr><td>H,W</td><td>size of the image.</td></tr><tr><td>F</td><td>=  $\{F^p, F^o, F^s\} = \{\{f_i^p\}_{i=1}^{N_p}, \{f_j^o\}_{j=1}^{N_o}, \{f^s\}\}$ , a set of visual features corresponding to the obfuscated regions, recognizable objects, and the scene.</td></tr><tr><td>B</td><td>=  $\{B^p, B^o\} = \{\{b_i^p\}_{i=1}^{N_p}, \{b_j^o\}_{j=1}^{N_o}\}$ , a set of bounding boxes corresponding to the locations of obfuscated regions and recognizable objects.</td></tr><tr><td>L</td><td>=  $\{L^o, L^s\} = \{\{l_j^o\}_{j=1}^{N_o}, l^s\}$ , a set of predicted labels corresponding to the categories of recognizable objects and the scene.</td></tr><tr><td colspan="2">Parameters</td></tr><tr><td> $\alpha^p$ </td><td>a weight used to control visual features in obfuscated nodes.</td></tr><tr><td> $W^e$ </td><td>=  $\{W^v, W^d, W^i, W^\theta\}$ , parameters of region-region edges.</td></tr><tr><td> $W^z, U^z$ </td><td>parameters of update gate.</td></tr><tr><td> $W^r, U^r$ </td><td>parameters of reset gate.</td></tr><tr><td>W,U</td><td>parameters of node propagation with update gate and reset gate.</td></tr><tr><td> $W^a, U^a$ </td><td>parameters of attention mechanism.</td></tr></table>

# 3 OUR APPROACH

# 3.1 Overview of Our System HideSeeker

Inspired by [24], which claimed that some neural networks for image classification have the potential to defeat pixelization and blurring, we design a scheme, called HideSeeker, to discover the privacy information hidden by obfuscation technologies including but not limited to these two methods. Given an image partially protected by obfuscation technologies, such as pixelization, blurring, scribbling, sticker-covering, and inpainting, our approach localizes the obfuscated privacy regions and infers the categories of hidden objects within the privacy region. As illustrated in Figure 3,

![](images/e594072780a4ce294620f14f77ddb3544fa5149896bca01435cbdbc4462cca3c.jpg)



Figure 3: An overview of our scheme HideSeeker for hidden object inference. HideSeeker is composed of 1) Visual Information Extraction, 2) Relation Graph Learning, and 3) Hidden Object Inference.

HideSeeker consists of three modules:Visual Information Extraction, Relation Graph Learning, and Hidden Objects Inference.

Visual Information Extraction: First, we expect to extract the contextual information of the hidden objects. We observe that the visual information of the image can be semantically classified into three types: obfuscated regions, recognizable objects, and the scene. Since all obfuscation technologies invariably leave traces of image manipulation, we draw support from image manipulation detection and localization models to localize obfuscated regions. We define the recognizable objects and the scene as the context of obfuscated regions. Object detection models are applied to extract regional features and detect recognizable objects. Besides, We use the visual features of the whole image as a representation of the scene.

Relation Graph Learning: Second, we construct a graph $G =$ G⟨ ⟩, where the node set  models the representations of obfuscated regions and their context and the edge set  models the Esemantic and spatial relationships between them. For the three types of visual information we focus on, we define node sets of obfuscated region nodes, recognizable object nodes and a scene node, respectively. Furthermore, we define the edges differently according to the relationship between different node sets.

Hidden Objects Inference: Finally, we infer the probability of an object class obfuscated based on the constructed relation graph for the image. We apply graph neural networks to learn the representation of obfuscated region nodes by aggregating of contextual information from their neighborhood iteratively. The aggregation and update of the node representations are guided by Gate Recurrent Unit [22]. Moreover, we aggregate attention mechanism into graph neural network to learn the latent relationships between obfuscated regions, objects and the scene.

# 3.2 Visual Information Extraction

In this module, we obtain all the visual information that can be observed from the obfuscated image. As for the visual information needed, we are inspired by the human observation of privacyprotected images. When viewing a obfuscation-protected image on a social platform, one’s gaze tends to focus on the obfuscated regions because of the visual inconsistencies or semantical anomalies compared to other regions. If wondering what is protected, the viewer will attempt to observe the contextual information of obfuscated regions displayed in the image and the relationships between them, and infer the categories of hidden objects with prior knowledge. Take the second image of Figure 2(b) as an example, one can easily localize the blurred regions at the first sight, that is, the region marked by the red box. Apart from that, we can recognize a keyboard and a display device on a desk. We can infer that the photo was most likely taken in an office. Despite the blurring, one can figure out that the blurred privacy-related object on a desk in an office may be a laptop.

Following this intuition, our proposed method first finds the obfuscated regions and extracts the regional visual features of them. The contextual information of the hidden objects are concretized as three types: obfuscated regions, recognizable objects, and the scene. The obfuscation technologies modify or replace the pixel values of privacy-related objects. Consequently, we can hardly rely on traditional object detection models to extract the original visual features for the classification. The methods based on region proposals often perform poorly compared with that on unobfuscated images. However, we view the obfuscation as a means of forgery for the original images. Recent studies have explored the detection and localization of image manipulation following the clues such as visual inconsistencies [20, 40], local anomalies [41], noise patterns [55, 58], etc. We expect to apply an image manipulation detection and localization model with great generalizability across different obfuscation technologies. With the help of ManTra-Net [41], we have the binary mask $\in \mathbb { R } ^ { H \times W }$ , where $m _ { i j } \in M$ is defined as:

$$
m _ {i j} = \left\{ \begin{array}{l l} 1, & \text { the   pixel   at   position } (i, j) \text { is   predicted   as   obfuscated; } \\ 0, & \text { otherwise. } \end{array} \right. \tag {2}
$$

To distill the locations of obfuscated regions, we cluster $m _ { i j }$ mijby the distance between pixels. The masked pixels in the same obfuscated region tend to have closer distance than that of other regions. For each pixel clustering, we take the minimum bounding box that can include the clustered pixels as the location of the obfuscated region. The locations of obfuscated regions are denoted as $B ^ { p } = \{ b _ { 1 } ^ { \bar { p } } , . . . , b _ { N _ { p } } ^ { p } \}$ , where the superscript  is short for “privacy-related”. Additionally, the regional visual feature $f _ { i } ^ { p } \in F ^ { p }$ fi Fis extracted from a fully-connected (FC) layer after the regions-ofinterest (ROI) pooling layer in Faster RCNN [30] according to the bounding box $\mathbf { \bar { \boldsymbol { b } } } _ { i } ^ { p } \in \bar { \boldsymbol { B ^ { p } } }$ .

Apart from privacy-related objects hidden in obfuscated regions, there are some other recognizable objects that may be the reason why the user shares an image or why the user obfuscates a region. Thanks to the remaining visual features, we can easily detect and recognize these objects with object detection models. We apply Faster RCNN [30], an off-the-shelf object detection model, for the detection and classification of recognizable objects. For the object o , we extract visual feature $f _ { i } ^ { o }$ as we do for obfuscated regions. i fiWe refer to the classification and bounding box regression results by object detectors as the category $l _ { i } ^ { o } \in L ^ { o }$ and location $b _ { i } ^ { o } \in B ^ { o }$ of recognizable objects, respectively.

According to [36], the scene of an image is often linked to certain private information. For example, the private information involved in the images taken on the “street" is likely to be related to $\mathbf { \tilde { c } a r " }$ or “person". Therefore, we take the scene as a potential indicator of privacy-related objects. For the scene s, we seek to learn the global feature of the image as a representation. We describe the scene by the visual feature derived from the last convolutional layer of the pretrained ResNet-50 [17] on the Places365 dataset [53]. The Places365 dataset contains nearly 1.8 million images from 365 scene categories.

# 3.3 Relation Graph Learning

For each image, we describe the image with a relation graph Glearned from the extracted visual information. This module aims to construct a graph representing semantic and spatial relationships between the obfuscated regions and their contextual information. We formulate the relation graph as $G = \langle V , E \rangle$ , where the nodes in G V , E represent visual information from visual information extraction Vmodule and the edges in  represent the polysemantic relation-Eships between them. The relation graph learning is described in Algorithm 1. Since we extract three types of semantics that include obfuscated regions, recognizable objects, and the scene, we define node sets $V = \{ V ^ { p } , V ^ { o } , V ^ { s } \}$ corresponding to them respectively:

V V ,V ,VRecognizable object nodes $V ^ { o } ;$ : We detect and classify objects Vthat co-occur with the obfuscated regions. Through the object detector Faster RCNN, we can obtain the predicted categories and locations of recognizable objects. Each object is defined as a recognizable node $\boldsymbol { v } \in V ^ { o }$ . Then we concatenate the category labels, v Vbounding boxes as well as the regional visual features as the node representations of recognizable object nodes: $\mathbf { x } ^ { o } = [ f ^ { o } \parallel l ^ { o } \parallel b ^ { o } ]$ .

Obfuscated region nodes $V ^ { p } ;$ Each node $\boldsymbol { v } \in V ^ { p }$ l bdenotes an V v Vobfuscated region in the image. We obtain the location of the region represented by the bounding boxes and the regional visual features derived from object detectors and incorporate them into the node representation $\mathbf { x } ^ { p }$ . In our experiment, when the obfuscation method is scribbling, sticker-covering or inpainting, the regional visual features contribute less to hidden object inference than we expected and might cause a negative effect conversely. Thus we introduce weights to balance the visual and spatial representations. The node representations of obfuscated region nodes are defined as: $\mathbf { x } ^ { p } = $ $[ \bar { \alpha ^ { p } } \cdot f ^ { p } \parallel 0 \parallel b ^ { p } ]$ , where $\alpha ^ { p }$ is a hyperparameter to represent the importance of the regional visual features and 0 is the padding added to ensure that the obfuscated region node representation has the same dimension as the recognizable object node representation.

Algorithm 1: The relation graph learning.   
Input: The extracted visual information V.
Output: Relation graph G = <V, E>
1 F, L, B ← V;
// Feature set: F = {F^p, F^o, F^s}; Label set:
    L = {L^o, L^s}; Bounding box set: B = {B^p, B^o}.
2 V^p ← ∅; V^o ← ∅; V^s ← ∅;
3 E ← ∅;
// Create graph node representations.
4 N_p ← |B^p|; N_o ← |B^o|; N_s ← 1; N ← N_p + N_o + N_s;
5 for i ← 1 to N_p do
6    x_i^p ← InitializeNodeRepresentations(f_i^p, b_i^p);
7    V^p ← V^p ∪ {x_i^p};
8 end
9 for j ← 1 to N_o do
10    x_j^o ← InitializeNodeRepresentations(f_j^o, l_j^o, b_j^o);
11    V^o ← V^o ∪ {x_j^o};
12 end
13 x^s ← InitializeNodeRepresentations(f^s, l^s);
14 V^s ← {x^s};
// Learn edge representations.
15 for each node pair (u, v) do
16    if both u, v are region nodes then
17    vis_uv ← ComputeNodeVisualSimilarity(f_u, f_v);
18    spa_uv ← ComputeNodeSpatialRelationship(b_u, b_v);
19    e_u→v ←LearnEdgeRepresentation(vis_uv, spa_uv);
20    E ← E ∪ {e_u→v};
21    end
22 else if one of u, v is a region node and another is the scene node then
23    e_u→v ←ComputeCooccurProbability(l_u, l_v);
24    E ← E ∪ {e_u→v};
25    end
26 end
27 return G = <V, E>;

Scene node $V ^ { s } ; V ^ { s }$ only contains one node that represents the description of the scene. The node representation of the scene node consists of the visual feature and classification results from the vvisual information extraction module. We represent the scene node $\mathbf { x } ^ { s }$ as the concatenation: $\mathbf { x } ^ { s } = [ f ^ { s } \parallel l ^ { s } \parallel \mathbf { 0 } ]$ , where 0 is the padding to keep the same dimension as other nodes.

Each directed edge $e _ { u  v }$ from a node  to a node  denotes the eu v u vinfluence of on . In our graph, we refer to obfuscated region nodes u vand recognizable object nodes collectively as region nodes. We compute semantic and spatial relationship between regions as the edges between region nodes. However, the relationships between the scene and regions are quite different from that between regions. After all, we cannot compute the spatial relationship between a desk and an office. Therefore, we define three types of edges:

Edges between the scene node and region nodes: There are empirical correlations between scenes and objects. For instance, it is more likely to see swimming rings or parasols on the beach than in the kitchen, while there is little chance that a micro-wave oven appears on the street. Consequently, we count the two-way co-

![](images/97c8b6f432cc079aa9dafd56cb75f3dcdfaf95977d45e7e289a30fde8f6a09da.jpg)



Figure 4: The co-occurrence information of objects and scenes, where the x-axis denotes possible scenes, and y-axis denotes possible objects. The entry in the Table represents the estimated probability that an object appearing in a scene. The larger the probability, the darker color here.

occurrence frequencies of objects and scenes from the obfuscated images we generate under laboratory conditions. As Figure 4 shows, we calculate the probability of each object appearing in different scenes along with the probability of each scene containing different objects by:

$$
P (\mathbf {s} | \mathbf {o}) = \frac {P (\mathbf {s} , \mathbf {o})}{P (\mathbf {o})}, \quad P (\mathbf {o} | \mathbf {s}) = \frac {P (\mathbf {s} , \mathbf {o})}{P (\mathbf {s})},
$$

where  (s o) is approximated by the co-occurrence frequency of P ,object o and scene s, and  (s) and  (o) are respectively the cooccurrence frequency of object o and scene s. For a recognizable object node  and the scene node , their relationship is measured u vby probability of co-occurrence. Thus we define the weight of the edge from  to  as

$$
e _ {u \rightarrow v} = P (v | u) \tag {3}
$$

Edges between region nodes: If both the nodes  and  are reu vgion nodes, we learn the semantic and spatial relationship between and for their edge representation. Two objects of the same cateu vgory are more closely connected than that of different categories. We calculate the visual similarity to measure the semantic relationship of two regions, specifically the cosine similarity of the visual feature $f _ { u }$ and $\begin{array} { r } { f _ { v } { : \mathrm { v i s } _ { u v } } = \frac { f _ { u } f _ { v } ^ { \top } } { \| f _ { u } \| \cdot \| f _ { v } \| } } \end{array}$ . As for the spatial relationship u v uv fu fvbetween node  and , we consider the distance, area overlap, and u vangle of regions  and . We calculate the Euclid distance between utwo centers of regions $( [ x _ { u } , y _ { u } ] , [ x _ { v } , y _ { v } ] )$ as the distance between them: dis $\mathrm { t } _ { u v } = \| b _ { u } - b _ { v } \| _ { 2 }$ u ,yu , xv ,yv. Intersection over Union (IoU) $\mathrm { i o u } _ { u v }$ of uv bu bv uvtwo region proposals (See the illustration in Figure 5(b)) is a measurement of area overlap. We calculate theta = arctan $\big ( \frac { y _ { u } - y _ { v } } { x _ { u } - x _ { v } } \big )$ uv xu xvfor the angle. Combining the semantic and spatial relationships between region nodes, we get the representation of edge  to  as:

$$
e _ {u \rightarrow v} = \mathbf {W} ^ {v} \mathrm{vis} _ {u v} + \mathbf {W} ^ {d} \mathrm{dist} _ {u v} + \mathbf {W} ^ {i} \mathrm{iou} _ {u v} + \mathbf {W} ^ {\theta} \mathrm{theta} _ {u v}, (4)
$$

where $\mathbf { W } ^ { v } , \mathbf { W } ^ { d } , \mathbf { W } ^ { i }$ , and $\mathbf { W } ^ { \theta }$ are the parameters to balance the , ,weights of semantic and spatial relationships.

![](images/6016632a2529ea12a3264e88459ef5793d3c33fc70dd9aedfc6b41aff53bdec6.jpg)  
(a) Unobfuscated image

![](images/1e49576d29cc941efa23b25aaefe37fa27ac7d59c487203af8495c06a2276f37.jpg)



(b) Spatial relationship between regions   
Figure 5: The spatial relationship between two objects including the distance, angle, and IoU of the corresponding bounding boxes of these two objects.

Algorithm 2: The hidden object inference.   
Input: A related graph $G = \langle V, E \rangle$ for I.
Output: Predicted label set of hidden objects C.

1 $C \leftarrow \emptyset$ ;

2 for $t \leftarrow 1$ to T do

3    for each $v \in V$ do

4    if t = 1 then

5 $h_{v}^{(0)} \leftarrow x_{v}$ ; // Initialize the node state with node representation.

6 $NBR(v) \leftarrow \text{IdentifyNeighborhoodNodes}(v, E)$ ;

7    end

8 $\widetilde{\mathbf{x}}_{v}^{(t)} \leftarrow \text{AggregateNodeStates}(\mathbf{h}_{NBR(v)}^{(t-1)})$ ;

9 $\mathbf{h}_{v}^{(t)} \leftarrow \text{MessagePassing}(\widetilde{\mathbf{x}}_{v}^{(t)}, \mathbf{h}_{v}^{(t-1)})$ ;

10    end

11 end

12 for each $v \in V^{p}$ do

13 $l_{v}^{p} \leftarrow \text{Classifier}(\mathbf{h}_{v}^{T})$ ;

14 $C \leftarrow C \cup \{l_{v}^{p}\}$ ;

15 end

16 return C;

# 3.4 Hidden Object Inference

Based on the relation graph for each image, we infer the categories of privacy-related objects hidden in obfuscated regions. We expect to learn the probability distribution of hidden object classes given the scene and recognizable objects in an image. We describe our algorithm in Algorithm 2.

Graph Neural Network (GNN) [32] can help describe the representations of hidden objects based on their neighborhood by means of iterative message passing between nodes. We define the node state of  for the -th iteration step as $\mathbf { h } _ { v } ^ { ( t ) }$ . We initiate the node state as:

$$
\mathbf {h} _ {\upsilon} ^ {(0)} = \mathbf {x} _ {\upsilon}. \tag {5}
$$

In an iteration step, the node state of  is updated by aggregating its node representation $\mathbf { x } _ { v }$ vand the states and representations of its vneighborhood nodes. The propogation can be defined as:

$$
\mathbf {h} _ {\upsilon} ^ {(t)} = \mathbf {f} (\mathbf {x} _ {\upsilon}, \mathbf {x} _ {\mathrm{NBR} (\upsilon)}, \mathbf {h} _ {\upsilon} ^ {(t - 1)}, \mathbf {h} _ {\mathrm{NBR} (\upsilon)} ^ {(t - 1)}), \tag {6}
$$

where $\mathbf { f } \left( \cdot \right)$ is a parametric function, and NBR( ) denotes the neighborhood nodes of .

Some works have demonstrated that Graph Convolutional Neural Networks (GCNs) are helpful to graph reasoning in object detection [19, 43]. They used graphs to describe the relationship between regions and applied GCNs to learn the latent visual representations of regions of interest. Nevertheless, if GCNs are applied in our scenario, the problem we are going to confront is that the states of obfuscated regions may negatively affect the learning of other nodes. Following to Gated Graph Neural Network (GGNN) [22], we introduce Gated Recurrent Unit [10] to control the negative effect of obfuscated region nodes on recognizable object nodes through reset gate while updating the states of obfuscated region nodes with messages collected from other nodes through update gate.

For each propagation step, node  aggregates node representations as $\widetilde { \mathbf { x } } _ { v }$ from its neighborhood nodes $v \in \mathrm { N B R } ( v )$ according to vthe adjacency matrix representations of graph:

$$
\widetilde {\mathbf {x}} _ {v} ^ {(t)} = E _ {: v} ^ {\top} \left[ \begin{array}{c c} \mathbf {h} _ {1} ^ {(t - 1)} & \dots \mathbf {h} _ {| V |} ^ {(t - 1)} \end{array} \right], \tag {7}
$$

where $E _ { : v }$ is the representations of ingoing edges related to node E v. The node states are updated as $\mathbf { z } _ { v } ^ { t }$ and reset as $\mathbf { r } _ { v } ^ { t }$ in the -th propogation step:

$$
\mathbf {z} _ {\upsilon} ^ {t} = \sigma \left(\mathbf {W} ^ {z} \widetilde {\mathbf {x}} _ {\upsilon} ^ {(t)} + \mathbf {U} ^ {z} \mathbf {h} _ {\upsilon} ^ {(t - 1)}\right), \tag {8}
$$

$$
\mathbf {r} _ {\upsilon} ^ {t} = \sigma \left(\mathbf {W} ^ {r} \widetilde {\mathbf {x}} _ {\upsilon} ^ {(t)} + \mathbf {U} ^ {r} \mathbf {h} _ {\upsilon} ^ {(t - 1)}\right),
$$

where $\mathbf { W } ^ { z }$ , Uz , $\mathbf { W } ^ { r }$ and $\mathbf { U } ^ { r }$ are learnable parameters in the update gate and reset gate respectively,  indicates the sigmoid function. σWe update the node state of  by $\mathrm { \bf z } _ { v } ^ { t }$ and $\mathbf { r } _ { v } ^ { t }$ with the activation of tanh function:

$$
\widetilde {\mathbf {h}} _ {v} ^ {(t)} = \tanh \left(\mathbf {W} \cdot \widetilde {\mathbf {x}} _ {v} ^ {(t)} + \mathbf {U} \left(\mathbf {r} _ {v} ^ {t} \odot \mathbf {h} _ {v} ^ {(t - 1)}\right)\right), \tag {9}
$$

$$
\mathbf {h} _ {\upsilon} ^ {(t)} = (1 - \mathbf {z} _ {\upsilon} ^ {t}) \odot \mathbf {h} _ {\upsilon} ^ {(t - 1)} + \mathbf {z} _ {\upsilon} ^ {t} \odot \widetilde {\mathbf {h}} _ {\upsilon} ^ {(t)},
$$

where ⊙ is element-wise multiplication.

In addition, we observed a phenomenon that some objects are more strongly associated with each other. For example, a person is more likely to be defined as private because of his social relationship with another person who are present at the same event than because of a fire hydrant on the street. We attach an attention mechanism to measure the contribution of other nodes to obfuscated region node representations. Our attention mechanism is a little bit different from Graph Attention Networks (GAT) [38]. We calculate the relevance between the obfuscated region node  ∈ $V ^ { p }$ and its neighborhood nodes as the attention coefficient:

$$
\widetilde {e} _ {u \rightarrow v} = \mathbf {f} _ {a} \left(\left[ \mathbf {W} ^ {a} \cdot \mathbf {h} _ {u} \| \mathbf {U} ^ {a} \cdot \mathbf {h} _ {v} \right]\right), \tag {10}
$$

$$
\alpha_ {u \rightarrow v} = \sigma (\text { LeakyReLU } (\widetilde {e} _ {u \rightarrow v})).
$$

where [· ∥ ·] means a concatenation of the obfuscated region node and one of its neighborhood node $v \in \mathrm { N B R } ( u ) , \mathbf { f } _ { a } ( \cdot )$ u is a non-linear afunction that map the concatenation of high-dimension node states to a real number, is the sigmoid function for activation. To this σend, we collect the states of their neighborhood nodes and weight them with attention coefficients before concatenation:

$$
\mathbf {h} _ {v} ^ {\prime} = \left\| _ {u \in \mathrm{NBR} (v)} \alpha_ {u \rightarrow v} \mathbf {h} _ {u}. \right. \tag {11}
$$

The recognition of hidden objects in obfuscated regions comes down to the node classification problem. Finally the final states and node representations are used for classification:

$$
o _ {i} = \mathbf {g} (\mathbf {h} _ {i} ^ {\prime}, \mathbf {x} _ {i}), \tag {12}
$$

where g(·) is the classifier and implemented with a softmax function in our experiments.

# 4 EVALUATIONS

In this section, we demonstrate a series of experiments to analyze the performance of our proposed approach. We first construct a laboratory-generated image dataset to fill the gap of obfuscated image datasets. We investigate several approaches that may be helpful to hidden object inference and compare our performance with them. Moreover, we evaluate HideSeeker on publicly available user-obfuscated images we crawled from social platforms.

# 4.1 Datasets

In order to take into account both the data generated in the laboratory environment and the user-obfuscated images, we use two datasets to evaluate our scheme.

Publicly available obfuscated images (ITIP): There is a lack of public image datasets where privacy-related objects are obfuscated or labeled. In order to raise users’ concerns about the privacy re-disclosure of their obfuscation-protected images, we collected privacy-protected images that users publicly post on public social platforms and annotated them with obfuscated regions, scenes, and hidden objects. We also collect some obfuscated images from volunteers whose annotations are labeled by themselves. We name the dataset the “I Thought I Protected" (ITIP) image dataset. In statistics, our ITIP dataset contains total of 1476 images with 45 privacy-related object classes. Among them, there are 260 images with the image owners’ annotations. We show the distribution of the most common 26 privacy-related objects in Figure 6.

![](images/0dc3116a52521573177cd0a0a132de57fc4ce106acb39e12a2dde69310395e98.jpg)



Privacy-related object categories   
Figure 6: The distribution of privacy-related object categories in our ITIP dataset.

Laboratory-generated obfuscated images (LGOI): For larger scale experiments, we generate a dataset based on MS COCO [23] for our evaluation. In our implementation, we randomly select one or more objects in an image as privacy-related objects for each image, and we obfuscate them with five privacy protection technologies. We illutrate some examples from LGOI dataset in Figure 7. To specify the privacy-related object classes to be obfuscated, we match COCO’s 80 object classes with the private classes in our ITIP dataset and select four most privacy-related classes: “person", “car", “laptop", “cell phone".

![](images/18f5ef8ecb4b917cce08b5e4f1f6cb69b2c0fb2e289cc1b88429730f0bb3102f.jpg)  
Figure 7: Some samples from LGOI dataset. (a) shows examples of pixelization with four different grid sizes including 4×4, 9×9, 16 × 16, 25 × 25. (b) shows examples of blurring with Gaussian kernel size set to  = 7,  = 31. The images in (c) are obfuscated k kby either black blocks or white blocks. (d) shows an image where the privacy-related objects are covered with stickers, and (e) shows an example of inpainting. All the original images of these samples are demonstrated for reference.

We set the grid size of pixelization as 4 × 4, 9 × 9, 16 × 16, and 25 × 25. The examples in Figure 7(a) show that the larger the grid size is, the less original pixel values are retained, thus the heavier the privacy protection is intuitively. Similarly, the Gaussian kernel size for blurring is set to 7 and 31, which describes the smoothness of pixel values in the obfuscated region. In Figure 7(b) we can see that the Gaussian kernel with smaller size generates less blury images. As for scribbling, painting the entire target region into a entire color block can achieve a better effect in covering the privacyrelated objects compared with random strokes, thus we manipulate images with black and white blocks to simulate users’ scribbling. We randomly select one of several emojis as stickers and put them onto the target regions for sticker-covering-based obfuscation. Our LGOI dataset consists of 12730 images. The number of images in each class is shown in the Table 2.

Table 2: The number of images for each privacy-related object category in our LGOI dataset. 

<table><tr><td>Category</td><td>person</td><td>car</td><td>laptop</td><td>cell phone</td></tr><tr><td>Num</td><td>2808</td><td>3406</td><td>2992</td><td>3524</td></tr></table>

# 4.2 Implementation Details

In Visual Information Extraction module, we mentioned that three semantics we extracted: obfuscated regions, recognizable objects,

and the scene. With regard to detection and localization of obfuscated regions, the generalizability to various image manipulation types is considered as significant as performance. To this end, we apply Mantra-Net [41] for obfuscated regions localization. Our experiment settings follow [41], setting the patch size to 256 × 256. Figure 8(c) shows some qualitative results of image manipulation detection and localization.

We detect recognizable objects via Faster RCNN [30] pretrained on COCO with 80 classes of objects. Besides, the regional visual features of obfuscated regions and recognizable objects are extracted from the FC layer after ROI pooling in the Faster RCNN. Since there’s no ground truth about the scene of the image, the scene is classified by the pretrained ResNet-50 [17] on the scene classification dataset Places365 [53]. According to [53], ResNet-50 can achieve 55 93% for Top-1 accuracy and 85 76% for Top-5. The .dimension of scene features  is 2048.

FWe train our scheme on our LGOI dataset and adopt cross entropy loss as our loss function and SGD as the optimizer. We set the learning rate = 0 001. Our method is implemented with PyTorch.

lr .Evaluation metrics. Our proposed scheme focuses on uncovering categories of hidden objects. With the localization of obfuscated regions mostly relying on the image manipulation detection models, we adopt the accuracy of classification as our evaluation metric.

# 4.3 Objective Comparisons

Baselines. We know the object detection model Faster RCNN [30] is powerful and robust to light occlusion. CompNets [21] strengthen the robustness of Faster RCNN as to partial object occlusion. Thus we compare our performance with Faster RCNN as well as Comp-Nets. We retrain their networks on our LGOI dataset for comparison. In addition, recent studies have developed several great models to deal with image blurring or low-resolution problems. The image blurring they handled includes the Gaussian blurring we applied in image privacy protection, and the low-resolution images can be referred pixelized images. NAFNet [9] has been proven to achieve the state-of-the-art results in image restoration tasks such as image deblurring, image denoising, and image super-resolution. Therefore, we also apply NAFNet to recover blurred and pixelized images before them being input to object detection models. Some experimental settings are as follows:

![](images/5f3b53193d1a366a3be2a011477ccee50d9fe0d6879e754bb20af382b6113e25.jpg)



Figure 8: Sample results of HideSeeker. The first and the second row shows the original images and their obfuscated ones. The third row shows the binary mask predicted by the image manipulation localization model. The last row demonstrates our inference results, where the red boxs outline the obfuscated regions with the predicted categories and corresponding confidence probabilities beside.

• Faster RCNN [30]: For the training, we finetune Faster RCNN on our LGOI dataset. ResNet-50 [17] is used as the backbone network, and the hyperparameters follow [30]. For the testing, since we are concerned about the inference of hidden objects, the proposals whose IoU with the ground truth bounding box is greater than 0.3 are counted.   
• CompNets [21]: The CompNets is pretrained on COCO. According to [21], we initialize the compositional model parameters $\{ \{ \mu _ { k } \} , \{ \mathcal { A } _ { y } \} \}$ via image clustering and unsuperkvisely learn the parameters of occluder models $\{ \beta _ { 1 } , . . . , \beta _ { n } \}$ β , ..., βnfor each obfuscation type. We also follow the original work and set the number of mixture components to $M = 4 ,$ with the mixing weights of $\gamma _ { 1 } = 0 . 1 , \gamma _ { 2 } = 5 , \gamma _ { 3 } = 1$ .   
γ . ,γ ,γ• NAFNet [9] before Faster RCNN: The image restoration model NAFNet stacks 36 blocks in an U-Net architecture and is claimed to be effective for various image restoration tasks. We retrain NAFNet from scratch on our LGOI dataset which is prepared following structure of the training datasets in [9]. We resize the training images to 256 × 256 and set the batch size as 32.

Comparisons with Baselines. In Table 3, we present our inference accuracy compared with three baseline methods. The performance of HideSeeker differs slightly on different obfuscation technologies. The best accuracy reaches 82 17% and is achieved on the blurred images with Gaussian kernel size set to 7. Our average accuracy over all obfuscation technologies can reach 77 72%. Faster RCNN achieves the average accuracy of 44 67% with the highest accuracy of 66 38%. The accuracy of CompNets has a sharp dip on severe obfuscated images, with an average accuracy of 42 31%. For images whose qualities are recovered with image restoration works such as image deblurring and super-resolution, we can see that the accuracy of object detection by Faster RCNN is only at most 30 20%. The performance of image restoration is far from our expectations when it is applied to heavily blurred images. One can note that HideSeeker outperforms Faster RCNN, even when the obfuscated images are restored by NAFNet. Our performance also exceeds occluded object detection models such as CompNets regardless of the obfuscation technologies and parameters.

When the manipulation trace features cover the original visual features of the object. Faster RCNN fails to propose the obfuscated regions based on visual features. Likewise, it is hard for CompNets to infer the categories of hidden objects without any clues since the objects are 100% occluded rather than partially occluded. Image restoration is expected to improve the accuracy of Faster RCNN in recognizing privacy-related objects. However, NAFNet deblurs the whole image instead of obfuscated regions. As a result, the restoration is strongly affected by the proportion of the obfuscated regions. We test the impact of the ratio of the obfuscated area to the total area of the image and the results are shown in Figure 9. The highest accuracy 51 85% is achieved when the obfuscated area is about 70%-80% of the total image and is overtaken by our scheme HideSeeker. The performance drops sharply when almost the whole image is obfuscated, because it relies on the recognizable parts of the image for inference.

![](images/32619a1ef19aa4af421ff4c333547ed9c3cd1912923abd29ab77b8b383c298c4.jpg)



Figure 9: The accuracy of HideSeeker on images with different obfuscation area ratios compared with the performance of Faster RCNN on images restored by NAFNet.

We observe that under different obfuscation technologies, the accuracy of our scheme differs by at most 7%. We get the worst accuracy on the sticker-covering dataset, which agrees with to our claim that stickers result in interference for hidden object inference based on visual features. Since our method has a minimal association with visual features of obfuscated regions, our results may be affected by locally anomal pixel gradients. By contrast, the performance of Faster RCNN and CompNets on different obfuscation technologies is significantly different. Compared with the pixelization and blurring dataset, the accuracy of Faster RCNN and CompNets drops heavily by 56 95% on other obfuscation datasets. .One explanation is that both two methods encounter difficulties modeling the visual features of privacy-related regions obfuscated by scribbling or stickers.

Table 3: Experiment results of various approaches on LGOI dataset. 

<table><tr><td rowspan="2">Obfuscation type</td><td colspan="4">Pixelization</td><td colspan="2">Blurring</td><td colspan="2">Scribbling</td><td rowspan="2">Sticker-covering</td><td rowspan="2">Inpainting</td></tr><tr><td>4 × 4</td><td>9 × 9</td><td>16 × 16</td><td>25 × 25</td><td>k = 7</td><td>k = 31</td><td>blackout</td><td>whiteout</td></tr><tr><td>Faster RCNN [30]</td><td>61.59%</td><td>66.38%</td><td>64.85%</td><td>58.52%</td><td>65.55%</td><td>64.38%</td><td>13.35%</td><td>13.28%</td><td>29.38%</td><td>9.43%</td></tr><tr><td>CompNets [21]</td><td>61.14%</td><td>54.06%</td><td>52.37%</td><td>51.34%</td><td>68.47%</td><td>30.67%</td><td>27.11%</td><td>25.88%</td><td>27.34%</td><td>24.67%</td></tr><tr><td>NAFNet [9]</td><td>5.88%</td><td>16.86%</td><td>21.96%</td><td>29.02%</td><td>30.20%</td><td>21.21%</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>HideSeeker</td><td>76.83%</td><td>76.98%</td><td>76.86%</td><td>77.38%</td><td>82.17%</td><td>78.24%</td><td>77.42%</td><td>76.71%</td><td>76.43%</td><td>78.16%</td></tr></table>

As shown in Table 4, our scheme achieves 78 82% accuracy on .average on the ITIP dataset which is a bit better than that of LGOI dataset. Furthermore, we train HideSeeker on the images that are annotated by volunteers and test it on the images that are obfuscated and annotated by the same user. This evaluation achieve 76.14% accuracy. From our observations, we infer that in publicly available obfuscated image dataset, the privacy-related objects obfuscated by users are more closely related to their contextual information than those we randomly select in LGOI. Therefore, the contextual information has a better effect in hidden object inference on ITIP dataset.

Table 4: Average inference accuracy of HideSeeker test on different datasets. 

<table><tr><td>Dataset</td><td>LGOI</td><td>ITIP</td><td>User-annotated images</td></tr><tr><td>Accuracy</td><td>77.72%</td><td>78.82%</td><td>76.13%</td></tr></table>

Generalizability. To evaluate the generalizability of our scheme to various obfuscation technologies, we train it on images generated by one of the obfuscation technologies and test its performance on images obfuscated by other methods. As one can infer in Table 5, when our proposed scheme is applied to a new obfuscation type without retraining or finetuning, there is no significant drop of the inference accuracy. The accuracy of our scheme trained with images processed by a specific obfuscation on different obfuscation technologies only differs at most 5%. The performance of our scheme reaches the highest on images obfuscated by blurring with the Gaussian kernel set to 7, no matter the obfuscation technologies used to process the training images.

# 4.4 Subjective Comparisons

Most of the obfuscation technologies can be easily detected by humans, as we can see in Figure 7, except for inpainting. Inpainting Table 5: Generalizability of our scheme to various obfuscation technologies. Here rows denote training data produced by different obfuscation technologies (see Table. 3), and columns denote testing data producted by obfuscation technologies with 10 parameters. Each entry denotes the inference accuracy using corresponding training and testing data sets.

<table><tr><td>0.76</td><td>0.76</td><td>0.76</td><td>0.75</td><td>0.78</td><td>0.76</td><td>0.75</td><td>0.75</td><td>0.75</td><td>0.76</td></tr><tr><td>0.77</td><td>0.76</td><td>0.76</td><td>0.76</td><td>0.79</td><td>0.76</td><td>0.76</td><td>0.76</td><td>0.74</td><td>0.77</td></tr><tr><td>0.77</td><td>0.76</td><td>0.76</td><td>0.76</td><td>0.78</td><td>0.76</td><td>0.75</td><td>0.75</td><td>0.76</td><td>0.76</td></tr><tr><td>0.77</td><td>0.76</td><td>0.77</td><td>0.77</td><td>0.78</td><td>0.76</td><td>0.77</td><td>0.76</td><td>0.76</td><td>0.77</td></tr><tr><td>0.75</td><td>0.75</td><td>0.74</td><td>0.74</td><td>0.81</td><td>0.77</td><td>0.74</td><td>0.74</td><td>0.74</td><td>0.77</td></tr><tr><td>0.77</td><td>0.77</td><td>0.77</td><td>0.76</td><td>0.80</td><td>0.78</td><td>0.77</td><td>0.76</td><td>0.77</td><td>0.77</td></tr><tr><td>0.75</td><td>0.76</td><td>0.76</td><td>0.75</td><td>0.78</td><td>0.75</td><td>0.76</td><td>0.76</td><td>0.74</td><td>0.77</td></tr><tr><td>0.76</td><td>0.76</td><td>0.75</td><td>0.75</td><td>0.79</td><td>0.76</td><td>0.75</td><td>0.76</td><td>0.75</td><td>0.76</td></tr><tr><td>0.76</td><td>0.77</td><td>0.77</td><td>0.76</td><td>0.79</td><td>0.76</td><td>0.75</td><td>0.75</td><td>0.76</td><td>0.77</td></tr><tr><td>0.77</td><td>0.76</td><td>0.76</td><td>0.76</td><td>0.79</td><td>0.77</td><td>0.77</td><td>0.76</td><td>0.75</td><td>0.78</td></tr></table>

models learn to fill in the target regions with surrounding pixels, thus inpainting can maintain the visual consistency of obfuscated regions with other regions in the image and fool the human eyes. To compare the performance of our approach with the ability of humans to infer the privacy-related objects hidden by obfuscation technologies, we conduct a series of subjective experiments.

We recruit 10 volunteers to infer the categories of the hidden objects in given images. Each participant views 100 obfuscated images, with 10 images for each parameter of each obfuscation technology. All the images are randomly chosen from our LGOI dataset.

For each participant, we display the images one by one and inform him/her of the corresponding obfuscation technology and the parameter. In addition, we provide a candidate list of privacyrelated object classes for participants to choose. Without knowing the location of the obfuscated regions, participant are asked to indicate the categories of hidden objects in each images themselves. We accept random selection in cases where participants have difficulty identifying categories.

We show the accuracy of volunteers inferring the obfuscated privacy-related objects in Figure 10. We find that humans can achieve 78 4% accuracy on average. Consistent with our knowledge, .on images processed by obfuscated methods such as pixelization with the grid size less than 25, blurring with kernel size 7, humans are better at inferring hidden objects than our approach. However, when we set a larger parameter of pixelization or blurring, which means a heavier obfuscation, our scheme achieves almost the same performance as human-eye observation. We also observe that the ability of humans inference of objects removed by inpainting falls way behind. Volunteers find it much harder to localize the obfuscation since deep-learning-based inpainting models smooth the boundaries between obfuscated regions and their neighborhood.

![](images/908a95b882a1bfd183c4117c053d54a78e02c0c880e3cbc5323ef9d35c532e9d.jpg)



Figure 10: Inference accuracy of HideSeeker and human observation.

# 4.5 Ablation Studies

We conduct the ablation studies on LGOI dataset to discuss the effectiveness of different parts in our three-stage inference.

Simple baseline. In our simple baseline, we extract the contextual information as defined in Section 3.2. We tried to sum or concatenate the extracted features of recognizable objects and scenes. We apply two fully-connection layers followed by the Softmax function as the classifier. The results listed in Table 6 show the accuracy of the simple baseline. We find that concatenating the contextual features can achieve 70 11% accuracy, which slightly outperforms .the learning by the sum of contextual features. Our HideSeeker is a further improvement of the aggregation of extracted contextual information based on the concatenation.

Table 6: Comparison results of simple baseline and graphbased inference. 

<table><tr><td>Aggregation</td><td>Sum</td><td>Concatenation</td><td>Relation graph</td></tr><tr><td>Accuracy</td><td>69.64%</td><td>70.11%</td><td>77.72%</td></tr></table>

Impact of image manipulation localization. To measure the impact of the performance of image manipulation detection and localization on our hidden object inference results, we compare the accuracy of our method based on the ManTra-Net [41] localization results and that based on the ground truth location of obfuscated regions. The comparison results are shown in Figure 11. Compared with that of using image manipulation detection to localize the unobfuscated region, the accuracy of hidden object inference is higher if we know the ground-truth location. It is consistent across different types of obfuscation. As we expected, the performance is slightly affected by the detection and localization of obfuscated regions. Particularly, suppose the image manipulation detection model fails to localize the obfuscated regions correctly. In that case, we will learn a graph with the relation between obfuscated region nodes and their context nodes offset from the real one, resulting in unreliable classification results.

Impact of attention layer. We use an attention layer to learn and enforce the potential relationship between obfuscated region nodes and their neighborhood nodes. We test the impact of the attention layer in hidden object inference by comparing the accuracy of our scheme with and without the attention layer. The results are shown in Table 7. From the results we conclude that attention layer does help our scheme to achieve a better performance.

![](images/c358ae1f955c541bdf0207383e71f5b4590195f713f5c75dd464cb11adce51cf.jpg)



Figure 11: Comparison results of using location predicted by image manipulation localization and using ground truth location for inference.

Table 7: Comparison results of graph-based inference with and without attention layer. 

<table><tr><td></td><td>w/o attention layer</td><td>with attention layer</td></tr><tr><td>Accuracy</td><td>77.51%</td><td>77.51%+0.21%</td></tr></table>

Impact of region-scene co-occurrence. We introduce the cooccurrence of objects and scenes from LGOI dataset for edge representations in Relation Graph Learning module. To test the impact of external knowledge, we compare the accuracy of defining the region-scene relationship in hidden object inference as a boolean value indicating co-occurrence and as co-occurrence probability. The results are shown in Table 8. The co-occurrence probability of regions and scenes increases the accuracy by 1 46%. The results verify our intuition that the relationships between regions and scenes do have a great contribution to hidden object inference.

Table 8: Impact of introducted object-scene co-occurrence probability for region-scene edge representation. 

<table><tr><td>Edge of region-scene</td><td>defined as 1</td><td>defined as P(o|s)</td></tr><tr><td>Accuracy</td><td>76.26%</td><td>76.26%+1.46%</td></tr></table>

# 4.6 System Performance

We propose HideSeeker to evaluate the effectiveness of obfuscation technologies before the photos are sent into untrusted channels. We deploy the scheme on mobile phones and evaluate the processing time for a single image. We implement our system on Android and test it on a Huawei P10 and a virtual Pixel 5. For comparison, we also evaluate the processing time of HideSeeker deployed on an Edge Server. This Server is equipped with an Intel Xeon E5- 2650 CPU and four NVIDIA Tesla P100 GPUs. The average runtime costs of HideSeeker deployed on the server and mobile devices are illustrated in Table 9. We can see that HideSeeker infers the categories of user-obfuscated objects in images within 1.8 seconds on average for each image.

Table 9: Average processing time of HideSeeker deployed on an Edge Server and Android devices including virtual Pixel 5 and Huawei P10. 

<table><tr><td>Device</td><td>Overall</td><td>Graph learning</td><td>Inference</td><td></td></tr><tr><td>Edge Server</td><td>533.4</td><td>290.8</td><td>32.2</td><td>(ms)</td></tr><tr><td>Pixel 5</td><td>642.3</td><td>60.7</td><td>228.5</td><td>(ms)</td></tr><tr><td>Huawei P10</td><td>1756.8</td><td>163.5</td><td>834.2</td><td>(ms)</td></tr></table>

# 4.7 Summary

In summary, our experimental results demonstrate the risk of privacy re-disclosure in image obfuscation technologies by the accuracy of discovering and classifying the hidden objects. Objectively, our approach outperforms several methods that may be used to discover privacy-related objects hidden in obfuscated images by a large margin. Furthermore, we demonstrate that our scheme has the generalizability to various obfuscation technologies. We recruited 10 volunteers to observe 1000 obfuscated images for hidden objects and our results show that our scheme is comparable to human-eye observations as to half of the obfuscation technologies we tested. Particularly, our scheme can uncover the hidden privacy information that human eye cannot discover when the image is obfuscated by inpainting.

In addition, we implement our system on mobile devices and evaluate the processing time cost. We can infer the privacy-related objects in an obufscated image within two seconds on a mobile phone.

# 5 RELATED WORK

# 5.1 Image Privacy Protection

Due to limited resource on mobile devices, online photo sharing and cloud storage services allow users to outsource their photo management, and also bring to urgent requirements of image privacy protection. Several works [33, 45] automatically detect the privacy information in uploaded photos and recommend the bestmatching privacy settings for image sharing. Privacy-preserving photo sharing and searching systems [49, 50] allow users to share their photos with privacy preserved from unauthorized users, and also provide solutions to secure image search. Besides, the privacy protection is also considered during the transaction of large-scale image dataset [52].

In cloud video surveillance system, Du et al. [14] developed a system to determine and detect privacy-related objects satisfying both security and privacy requiremnts. Encryption [29, 35] are also well studied for users’ privacy protection. Moreover, Zhou et al. [54] developed an automatic system to filter, track, and pixelize irrelevant faces in video streaming.

# 5.2 Attacks against Image Obfuscation

Image obfuscation technologies such as pixelization and blurring are widely used as privacy protection [6, 56]. Researchers have devoted some efforts to measuring the effectiveness of these technologies or elaborating on attacks to call attention to security concerns. Newton et al. [25] discussed the push-pull between face de-identification and face recognition methods. Oh et al. [26] furtherly proposed a face recognition system indicating that despite the presence of obfuscation, individuals’ identities can be inferred through pose and clothing. For screenshots of documents, Hill et al. [18] decoded character sequences with Hidden Markov Models and used the Viterbi algorithm in HMMs for inference. Their results show that their algorithm can recover the names and other sensitive text redacted by pixelizarion and blurring. McPherson et al. [24] showed that despite partially removing sensitive information to certain parts of the image obfuscation technologies retain the image’s basic structure and appearance, thus allowing the neural networks to have the opportunity to identify faces.

Cavedon et al. [8] described an attack against the anonymization of videos through pixelization. They reconstruct the image to make them easier for the human eyes to recognize. In addition to well-known obfuscation technologies like pixelization and blurring, some other researchers have studied visual tasks under the consistence of image degradation including lens distortions [28] and low resolution [31].

Furthermore, image restoration efforts such as image deblurring [9, 11, 47] are taken to improve the visual quality of lowresolution images. Because of their performance in restoring image details from pixelization and blurring, we can also refer to these works as attacks on image obfuscation. Different from [18, 24, 25], image deblurring focuses on the super-resolution of the whole image instead of uncovering hidden information. In the terms of image restoration tasks, Zamir et al. [47] learned a multi-stage architecture MPRNet, where earlier stages extract multi-scale contextualized features and the last stage generates spatially accurate outputs. The very recent work [9] proposed NAFNet where the nonlinear activation functions such as Sigmoid, ReLU are replaced by multiplication or removed. Their applications include image denoising and deblurring.

# 5.3 Object Detection Under Occlusion

According to Fawzi and Frossard [15], the accuracy of deep neural network-based classifiers degrades with partial occlusion. Regularizations on DCNNs have been explored to realize robust object classification under occlusion [12, 42]. Moreover, several recent works [21, 39] have proposed compositional networks to detect partially occluded objects, applying a differentiable generative compositional layer instead of the fully-connected head in DCNN which represents objects as compositions of parts. Since these works assume there is only one occluded object in an image. Yuan et al. [46] extended their generative model to include multiple objects, further located erroneous segmentations, and estimated the occlusion order. Nonetheless, they can only be applied to partial occlusion, and cannot be used for uncovering objects which are completely occluded for their poor regional visual features.

# 6 DISCUSSIONS AND CONCLUSION

Our approach can be affected by the performance of models for computer vision tasks, including object detection, image manipulation detection and localization, and scene classification. We demonstrated in Figure 11 that the localization of obfuscated region reduces the accuracy with an average loss of 0.39%.

On the other hand, our inference of hidden objects depends on the contextual information of obfuscated regions. Our scheme may fail when (1) there is no recognizable object left in the image; (2) the proportion of obfuscation area exceeds 80% of the image. In the first case, without any clue about surrounding objects, we can only rely on the classification of the scene and the possible objects that are strongly related to the scene. As Figure 9 shows, obfuscation of large area seriously affects our inference. When more than 80% of the image are manipulated or occluded, it is difficult to classify the scene accurately. Thus we can hardly model the contextual information of the hidden objects.

In this work, to explore the privacy leakage risk of obfuscationprotected images, we design an effective and efficient method to uncover categories of the hidden objects in obfuscated images. The original visual features of objects are severely occluded or manipulated by obfuscation technologies, resulting in the inability of object detection algorithms to identify them by extracting visual features. We resolve this challenge by intergrating contextual information of the hidden objects through a semantic and spatial relation graph.

Several interesting tasks remain as future work, including processing 1) images without recognizable objects, 2) images with extremely large obfuscated areas. We also plan to extend our study to uncover the hidden objects in protected videos.

# 7 ACKNOWLEDGEMENTS

Xiang-Yang Li is the corresponding author. The research is partially supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 62132018, No. 61932016, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002, The University Synergy Innovation Program of Anhui Province with No. GXXT-2019-024, "the Fundamental Research Funds for the Central Universities" WK2150110024, and CAAI-Huawei MindSpore Open Fund.

# REFERENCES

[1] Jawadul H. Bappy, Cody Simons, Lakshmanan Nataraj, B. S. Manjunath, and Amit K. Roy-Chowdhury. 2019. Hybrid LSTM and EncoderâĂŞDecoder Architecture for Detection of Image Forgeries. IEEE Transactions on Image Processing 28 (2019), 3286–3300.   
[2] Belhassen Bayar and Matthew C. Stamm. 2018. Constrained Convolutional Neural Networks: A New Approach Towards General Purpose Image Manipulation Detection. IEEE Transactions on Information Forensics and Security 13 (2018), 2691–2706.   
[3] Marcelo Bertalmío, Guillermo Sapiro, Vicent Caselles, and Coloma Ballester. 2000. Image inpainting. Proceedings of the 27th annual conference on Computer graphics and interactive techniques (2000).   
[4] Marcelo Bertalmío, Luminita A. Vese, Guillermo Sapiro, and S. Osher. 2003. Simultaneous structure and texture image inpainting. 2003 IEEE Computer Society Conference on Computer Vision and Pattern Recognition, 2003. Proceedings. 2 (2003), II–707.   
[5] Yohan Beugin, Quinn K. Burke, Blaine Hoak, Ryan Sheatsley, Eric Pauley, Gang Tan, Syed Rafiul Hussain, and Patrick Mcdaniel. 2022. Building a Privacy-Preserving Smart Camera System. Proceedings on Privacy Enhancing Technologies 2022 (2022), 25 – 46.   
[6] Cheng Bo, Guobin Shen, Jie Liu, Xiangyang Li, Yongguang Zhang, and Feng Zhao. 2014. Privacy.tag: privacy concern expressed and respected. Proceedings of the

12th ACM Conference on Embedded Network Sensor Systems (2014).   
[7] Chenjie Cao and Yanwei Fu. 2021. Learning a Sketch Tensor Space for Image Inpainting of Man-made Scenes. 2021 IEEE/CVF International Conference on Computer Vision (ICCV) (2021), 14489–14498.   
[8] Ludovico Cavedon, Luca Foschini, and Giovanni Vigna. 2011. Getting the Face Behind the Squares: Reconstructing Pixelized Video Streams. In WOOT.   
[9] Liangyu Chen, Xiaojie Chu, X. Zhang, and Jian Sun. 2022. Simple Baselines for Image Restoration. ArXiv abs/2204.04676 (2022).   
[10] Kyunghyun Cho, Bart van Merrienboer, ÃĞaglar GülÃğehre, Dzmitry Bahdanau, Fethi Bougares, Holger Schwenk, and Yoshua Bengio. 2014. Learning Phrase Representations using RNN EncoderâĂŞDecoder for Statistical Machine Translation. In EMNLP.   
[11] Sung-Jin Cho, Seoyoun Ji, Jun-Pyo Hong, Seung-Won Jung, and Sung-Jea Ko. 2021. Rethinking Coarse-to-Fine Approach in Single Image Deblurring. 2021 IEEE/CVF International Conference on Computer Vision (ICCV) (2021), 4621–4630.   
[12] Terrance Devries and Graham W. Taylor. 2017. Improved Regularization of Convolutional Neural Networks with Cutout. ArXiv abs/1708.04552 (2017).   
[13] Qiaole Dong, Chenjie Cao, and Yanwei Fu. 2022. Incremental Transformer Structure Enhanced Image Inpainting with Masking Positional Encoding. ArXiv abs/2203.00867 (2022).   
[14] Haohua Du, Linlin Chen, Jianwei Qian, Jiahui Hou, Taeho Jung, and Xiangyang Li. 2020. PatronuS: A System for Privacy-Preserving Cloud Video Surveillance. IEEE Journal on Selected Areas in Communications 38 (2020), 1252–1261.   
[15] Alhussein Fawzi and Pascal Frossard. 2016. Measuring the effect of nuisance variables on classifiers. In BMVC.   
[16] Danna Gurari, Qing Li, Chi Lin, Yinan Zhao, Anhong Guo, Abigale Stangl, and Jeffrey P. Bigham. 2019. VizWiz-Priv: A Dataset for Recognizing the Presence and Purpose of Private Visual Information in Images Taken by Blind People. 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2019), 939–948.   
[17] Kaiming He, X. Zhang, Shaoqing Ren, and Jian Sun. 2016. Deep Residual Learning for Image Recognition. 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR) (2016), 770–778.   
[18] Steven Hill, Zhimin Zhou, Lawrence K. Saul, and Hovav Shacham. 2016. On the (In)effectiveness of Mosaicing and Blurring as Tools for Document Redaction. Proceedings on Privacy Enhancing Technologies 2016 (2016), 403 – 417.   
[19] Hanzhe Hu, Jiayuan Gu, Zheng Zhang, Jifeng Dai, and Yichen Wei. 2018. Relation Networks for Object Detection. 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition (2018), 3588–3597.   
[20] Xuefeng Hu, Zhihan Zhang, Zhenye Jiang, Syomantak Chaudhuri, Zhenheng Yang, and Ramakant Nevatia. 2020. SPAN: Spatial Pyramid Attention Network forImage Manipulation Localization. ArXiv abs/2009.00726 (2020).   
[21] Adam Kortylewski, Ju He, Qing Liu, and A. Yuille. 2020. Compositional Convolutional Neural Networks: A Deep Architecture With Innate Robustness to Partial Occlusion. 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2020), 8937–8946.   
[22] Yujia Li, Daniel Tarlow, Marc Brockschmidt, and Richard S. Zemel. 2016. Gated Graph Sequence Neural Networks. CoRR abs/1511.05493 (2016).   
[23] Tsung-Yi Lin, Michael Maire, Serge J. Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, and C. Lawrence Zitnick. 2014. Microsoft COCO: Common Objects in Context. In ECCV.   
[24] Richard McPherson, R. Shokri, and Vitaly Shmatikov. 2016. Defeating Image Obfuscation with Deep Learning. ArXiv abs/1609.00408 (2016).   
[25] Elaine M. Newton, Latanya Sweeney, and Bradley A. Malin. 2005. Preserving privacy by de-identifying face images. IEEE Transactions on Knowledge and Data Engineering 17 (2005), 232–243.   
[26] Seong Joon Oh, Rodrigo Benenson, Mario Fritz, and Bernt Schiele. 2016. Faceless Person Recognition: Privacy Implications in Social Media. ArXiv abs/1607.08438 (2016).   
[27] Tribhuvanesh Orekondy, Bernt Schiele, and Mario Fritz. 2017. Towards a Visual Privacy Advisor: Understanding and Predicting Privacy Risks in Images. 2017 IEEE International Conference on Computer Vision (ICCV) (2017), 3706–3715.   
[28] Yanting Pei, Yaping Huang, Qi Zou, Hao Zang, Xingyuan Zhang, and Song Wang. 2018. Effects of Image Degradations to CNN-based Image Classification. ArXiv abs/1810.05552 (2018).   
[29] Fei Peng, Xiao wen Zhu, and Min Long. 2013. An ROI Privacy Protection Scheme for H.264 Video Based on FMO and Chaos. IEEE Transactions on Information Forensics and Security 8 (2013), 1688–1699.   
[30] Shaoqing Ren, Kaiming He, Ross B. Girshick, and Jian Sun. 2015. Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks. IEEE Transactions on Pattern Analysis and Machine Intelligence 39 (2015), 1137–1149.   
[31] Michael S. Ryoo, Brandon Rothrock, Charles Fleming, and Hyun Jong Yang. 2017. Privacy-Preserving Human Activity Recognition from Extreme Low Resolution. In AAAI.   
[32] Franco Scarselli, Marco Gori, Ah Chung Tsoi, Markus Hagenbuchner, and Gabriele Monfardini. 2009. The Graph Neural Network Model. IEEE Transactions on Neural Networks 20 (2009), 61–80.

[33] Anna Cinzia Squicciarini, Dan Lin, Smitha Sundareswaran, and Joshua Wede. 2015. Privacy Policy Inference of User-Uploaded Images on Content Sharing Sites. IEEE Transactions on Knowledge and Data Engineering 27 (2015), 193–206.   
[34] Roman Suvorov, Elizaveta Logacheva, Anton Mashikhin, Anastasia Remizova, Arsenii Ashukha, Aleksei Silvestrov, Naejin Kong, Harshith Goka, Kiwoong Park, and Victor S. Lempitsky. 2022. Resolution-robust Large Mask Inpainting with Fourier Convolutions. 2022 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) (2022), 3172–3182.   
[35] Xianhao Tian, Peijia Zheng, and Jiwu Huang. 2021. Robust Privacy-Preserving Motion Detection and Object Tracking in Encrypted Streaming Video. IEEE Transactions on Information Forensics and Security 16 (2021), 5381–5396.   
[36] Ashwini Tonge and Cornelia Caragea. 2019. Dynamic Deep Multi-modal Fusion for Image Privacy Prediction. The World Wide Web Conference (2019).   
[37] Lam Tran, Deguang Kong, Hongxia Jin, and Ji Liu. 2016. Privacy-CNH: A Framework to Detect Photo Privacy with Convolutional Neural Network using Hierarchical Features. In AAAI.   
[38] Petar Velickovic, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro LioâĂŹ, and Yoshua Bengio. 2018. Graph Attention Networks. ArXiv abs/1710.10903 (2018).   
[39] Angtian Wang, Yihong Sun, Adam Kortylewski, and A. Yuille. 2020. Robust Object Detection Under Occlusion With Context-Aware CompositionalNets. 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2020), 12642–12651.   
[40] Junke Wang, Zuxuan Wu, Jingjing Chen, Xintong Han, Abhinav Shrivastava, Ser-Nam Lim, and Yu-Gang Jiang. 2022. ObjectFormer for Image Manipulation Detection and Localization. ArXiv abs/2203.14681 (2022).   
[41] Yue Wu, Wael AbdAlmageed, and P. Natarajan. 2019. ManTra-Net: Manipulation Tracing Network for Detection and Localization of Image Forgeries With Anomalous Features. 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2019), 9535–9544.   
[42] Mingqing Xiao, Adam Kortylewski, Ruihai Wu, Siyuan Qiao, Wei Shen, and Alan Loddon Yuille. 2020. TDAPNet: Prototype Network with Recurrent Top Down Attention for Robust Object Classification under Partial Occlusion. In ECCV Workshops.   
[43] Hang Xu, Chenhan Jiang, Xiaodan Liang, and Zhenguo Li. 2019. Spatial-Aware Graph Relation Network for Large-Scale Object Detection. 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2019), 9290–9299.   
[44] Jiahui Yu, Zhe L. Lin, Jimei Yang, Xiaohui Shen, Xin Lu, and Thomas S. Huang. 2018. Generative Image Inpainting with Contextual Attention. 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition (2018), 5505–5514.   
[45] Jun Ye Yu, Baopeng Zhang, Zheng Kuang, Dan Lin, and Jianping Fan. 2017. iPrivacy: Image Privacy Protection by Identifying Sensitive Objects via Deep Multi-Task Learning. IEEE Transactions on Information Forensics and Security 12 (2017), 1005–1016.   
[46] Xiaoding Yuan, Adam Kortylewski, Yihong Sun, and Alan Loddon Yuille. 2021. Robust Instance Segmentation through Reasoning about Multi-Object Occlusion. 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2021), 11136–11145.   
[47] Syed Waqas Zamir, Aditya Arora, Salman Hameed Khan, Munawar Hayat, Fahad Shahbaz Khan, Ming-Hsuan Yang, and Ling Shao. 2021. Multi-Stage Progressive Image Restoration. 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2021), 14816–14826.   
[48] Sergej Zerr, Stefan Siersdorfer, Jonathon S. Hare, and Elena Demidova. 2012. Privacy-aware image classification and search. In SIGIR ’12.   
[49] Lan Zhang, Taeho Jung, Cihang Liu, Xuan Ding, Xiangyang Li, and Yunhao Liu. 2015. POP: Privacy-Preserving Outsourced Photo Sharing and Searching for Mobile Devices. 2015 IEEE 35th International Conference on Distributed Computing Systems (2015), 308–317.   
[50] Lan Zhang, Taeho Jung, Kebin Liu, Xiangyang Li, Xuan Ding, Jiaxi Gu, and Yunhao Liu. 2017. PIC: Enable Large-Scale Privacy Preserving Content-Based Image Search on Cloud. IEEE Transactions on Parallel and Distributed Systems 28 (2017), 3258–3271.   
[51] Lan Zhang, Xiangyang Li, Kebin Liu, Cihang Liu, Xuan Ding, and Yunhao Liu. 2019. Cloak of Invisibility: Privacy-Friendly Photo Capturing and Sharing System. IEEE Transactions on Mobile Computing 18 (2019), 2488–2501.   
[52] Lan Zhang, Yannan Li, Xiang Xiao, Xiangyang Li, Junjun Wang, Anxin Zhou, and Qiang Li. 2018. CrowdBuy: Privacy-friendly Image Dataset Purchasing via Crowdsourcing. IEEE INFOCOM 2018 - IEEE Conference on Computer Communications (2018), 2735–2743.   
[53] Bolei Zhou, Àgata Lapedriza, Aditya Khosla, Aude Oliva, and Antonio Torralba. 2018. Places: A 10 Million Image Database for Scene Recognition. IEEE Transactions on Pattern Analysis and Machine Intelligence 40 (2018), 1452–1464.   
[54] Jizhe Zhou and Chi-Man Pun. 2021. Personal Privacy Protection via Irrelevant Faces Tracking and Pixelation in Video Live Streaming. IEEE Transactions on Information Forensics and Security 16 (2021), 1088–1103.   
[55] Peng Zhou, Xintong Han, Vlad I. Morariu, and Larry S. Davis. 2018. Learning Rich Features for Image Manipulation Detection. 2018 IEEE/CVF Conference on

Computer Vision and Pattern Recognition (2018), 1053–1061.

[56] Hanwei Zhu, Songzeng Fan, Xiyu Wang, and Sid Chi-Kin Chau. 2020. Privacy-Preserving Camera-based Monitoring and Tracking System for Parking Spaces. Proceedings of the 7th ACM International Conference on Systems for Energy-Efficient Buildings, Cities, and Transportation (2020).

[57] H. Zhu, Peng Tang, and A. Yuille. 2019. Robustness of Object Recognition under Extreme Occlusion in Humans and Computational Models. In CogSci.

[58] Longhao Zhuo, Shunquan Tan, Bin Li, and Jiwu Huang. 2022. Self-Adversarial Training Incorporating Forgery Attention for Image Forgery Localization. IEEE Transactions on Information Forensics and Security 17 (2022), 819–834.