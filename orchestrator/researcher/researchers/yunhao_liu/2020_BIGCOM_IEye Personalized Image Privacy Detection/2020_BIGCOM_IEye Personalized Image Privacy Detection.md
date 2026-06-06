# IEye: Personalized Image Privacy Detection

Rui Jiao

University of Science

and Technology of China

Hefei, China

ruijiao@mail.ustc.edu.cn

Lan Zhang

University of Science

and Technology of China

Hefei, China

zhanglan@ustc.edu.cn

Anran Li

University of Science

and Technology of China

Hefei, China

anranLi@mail.ustc.edu.cn

Abstract—Massive images are being shared via a variety of ways, such as social networking. The rich content of images raise a serious concern for privacy. A great number of efforts have been devoted to designing mechanisms for privacy protection based on the assumption that the privacy is well defined. However, in practice, given a collection of images it is usually nontrivial to decide which parts of images should be protected, since the sensitivity of objects is context-dependent and user-dependent. To meet personalized privacy requirements of different users, we propose a system IEye to automatically detect private parts of images based on both common knowledge and personal knowledge. Specifically, for each user's images, multi-layered semantic graphs are constructed as feature representations of his/her images and a rule set is learned from those graphs, which describes his/her personalized privacy. In addition, an optimization algorithm is proposed to protect the user's privacy as well as minimize the loss of utility. We conduct experiments on two datasets, the results verify the effectiveness of our design to detect and protect personalized image privacy.

Index Terms—Image privacy, Privacy definition, Privacy detection

# I. INTRODUCTION

With the popularity and rapid development of mobile devices, large amount of images are captured, shared and utilized. Without proper privacy protection, those images could cause unwanted disclosure of sensitive information and privacy violations.

A series of efforts have been devoted to addressing the concern of image privacy. Some social networking websites allow users to manually specify a set of coarse-grained privacy settings. Due to a lack of expertise, however, a large number of users find it is not easy to correctly configure the privacy settings [1], resulting in failures to achieve users' desired levels of privacy protection. To release the privacy setting burden from users, many automatic privacy detection and configuration methods have been proposed [2]–[9]. Those work have several limitations. First, some work rely on predefined privacy content, e.g., face and license plate number [2]. However, the incomplete pre-defined privacy list limits the detection and protection of diverse private content. Second, many work convert the image privacy detection issue into solving binary classification or multi-category classification problems [3]–[8] using machine learning methods. Those generic models cannot be adopted to deal with different users' personal images due to that their privacy settings and definitions vary. [9]. Third, though these methods can predict whether an image is privacy or not with high accuracy, those results are barely interpretable. They cannot explain why the image is privacy or which part of the image is privacy in a visualized way, which makes it difficult to understand the prediction results.

In this work, we design an automatic image privacy detection system IEye, which aims to provide personalized and interpretable privacy detection results to meet diverse privacy requirements of different users. Specifically, we conquer the following challenges (1) how to detect fine-grained privacy from a limited number of images with coarse-grained labels? Unlike public datasets, e.g., ImageNet or Flickr, it is very difficult to obtain private image datasets and more difficult to obtain private image datasets with fine-grained labels. Therefore, given only coarse-grained-labeled images, building a fine-grained privacy detection model remains a challenge. (2) how to learn a user's personalized privacy definition and make the privacy detection results interpretable? A user considers some image content as his/her privacy due to both common sense and his/her personal reasons. It is nontrivial to learn the implicit personal knowledge and design an interpretable predict model combining common and personal knowledge. (3) how to balance the privacy protection and the utility of images? Increasing the privacy protection level (i.e., hiding more information in images) usually reduces the utility of images. An efficient solution with a good tradeoff between privacy and utility is desired.

Contributions of this work can be summarized as follows. First, we propose a novel system IEye, which to the best of our knowledge is so far the first to investigate personalized image privacy in an interpretable way. Second, we propose to use knowledge graph to structurally represent image semantics, based on which a rule mining method is desinged to uncover personalized privacy definitions. Third, the tradeoff between privacy protection and image utility is reduced to a combinatorial optimization problem.

The rest of this paper is organized as follows. Section II introduces the related work about image privacy detection. In section III, we formally define the problem and illustrate the system overview. We describe the system design in detail in section IV. Section V reports the experimental results. Finally, we summarize our work and discuss the future work in section VI.

# II. RELATED WORK

Many recent work study automatic image privacy detection. Most of them convert the image privacy detection problem into a two-class [3]–[6] or a multi-class classification problem [7], [8]. Zerr et al. [4] are the first to consider the problem of privacy-aware image classification. They collected and labelled the dataset PicAlert used to study image privacy. They use a variety of visual and textual features, such as edge-direction coherence and SIFT, to train a SVM model. There are some studies following [4] and using the dataset of PicAlert to evaluate their approaches. Squicciarini et al. [10] use combinations of visual and metadata-derived features and achieve better prediction accuracy on PicAlert. Both [4] and [10] use the hand-crafted features. As deep learning models achieve remarkable results in the computer vision field, more and more work use deep learning models for image privacy detection [3], [6]–[9], [11]–[13]. Tonge et al. [6] use deep features to achieve better accuracy than those using hand-crafted features. Tran et al. [3] propose a method that utilizes hierarchical features including both objects and convolutional features in a deep learning model to detect image privacy. Yu et al. [7], [8] design a deep multiple instance learning algorithm to identify fine-grained privacy-sensitive object classes and events. All those methods focus on designing generic models for privacy detection.

Considering diverse privacy requirements of different users, some personalized image privacy detection methods [9], [11], [12] are proposed. Spyromitros et al. [9] develop personalized privacy classification models by utilizing small amounts of user feedbacks. Orekondy et al. [11] categorize personal information in images into 68 image attributes and consider a user's privacy preference to predict user specific privacy scores for images. Zhong et al. [12] propose a group-based personalized model which learns a set of typical privacy models and associates a given user with one of these groups. Although those methods use deep learning techniques to achieve effective image privacy detection, their black-box procedures make the detection results poorly interpretable. As a result, a personalized and interpretable image privacy detection method is urgently needed.

# III. SYSTEM OVERVIEW

# A. Problem Definition

In this work, given a collection of a user's images to be published, we aim to protect the user's personalized image privacy while retain the utility of images as much as possible. There are two steps: the first step is to detect privacy parts in images, including determining whether an image is privacy, locating the privacy area of the image and explaining the reason to the image owner; the second step is to protect privacy in images, that is to process images to maximize utility while protecting privacy.

Formally, given a set of users $\mathcal{U} = \{u_1, u_2, ..., u_U\}$ and each user $u_i \in \mathcal{U}$ has a personal image set $\mathcal{I}_{u_i} = \{im_{u_i}^1, im_{u_i}^2, ..., im_{u_i}^I\}$ . User $u_i$ 's dataset is

$$
\mathcal {D} _ {u _ {i}} = \{(x _ {u _ {i}} ^ {1}, y _ {u _ {i}} ^ {1}), (x _ {u _ {i}} ^ {2}, y _ {u _ {i}} ^ {2})..., (x _ {u _ {i}} ^ {I}, y _ {u _ {i}} ^ {I}) \}
$$

, where $x_{u_i}^i \in \mathcal{X}$ is the feature representation of image $im_{u_i}^i$ , $y_{u_i}^i \in \{0,1\}$ and $y_{u_i}^i = 1$ if $im_{u_i}^i$ is a private image, 0 otherwise. We use a rule set $\mathcal{R}_{u_i} = \{r_{u_i}^1, r_{u_i}^2, ..., r_{u_i}^R\}$ as the user $u_i$ 's personalized privacy definition (his/her rules to determine whether an image is privacy). The rule set $\mathcal{R}_{u_i}$ is learned from the user's dataset $\mathcal{D}_{u_i}$ and is used to predict new instances.

For privacy images detected in the previous step, we use an optimization function to get desensitized images as follow:

$$
\mathcal {O}: (\mathcal {X}, \mathcal {M}) \xrightarrow {\mathcal {F} _ {u _ {i}}} \mathcal {X} ^ {\prime}
$$

where $x \in X$ is the feature representation of the private image, $m \in M$ is the matched rule set by x, $f_{u_i} \in F_{u_i}$ is the quality evaluation function required by user $u_i$ and $x' \in X'$ is the feature representation of desensitized image.

# B. System Overview

The system overview is shown in Figure 1. A multi-layered semantic graph is firstly built as the feature representation of an image. We extract multiple visual semantic features of an image that are user-understandable and logically organize these features using a graph. And then a user's rule set is learned based on a set of graphs and used to detect private images by rule matching. These rules are the description of the user's privacy definition. Users can also add more personalized rules to their rule sets. We can judge whether an image is private, explain the reason and locate the privacy content by rule matching. Finally we design an optimization method to minimize the loss of utility while protecting image privacy. Users can also add personalized requirements for image utility.

# IV. SYSTEM DESIGN

# A. Feature Representation

We aim to design a feature representation that covers all privacy-related visual features. We divide these features into four categories. The first type is the basic entities in images like person and object. The second category is the properties of these basic entities, such as bareness and face score. The third category is the relationship between these basic entities, such as behavior, social relationships and spatial relationships. The fourth category consists of multiple basic entities or reflects the entire image content, such as number of person, scene and so on. So we build a graph G which fuses first three factors as the feature representation of an image. These factors are mapped to edges or nodes in the graph. In addition, a vector O is used to describe the fourth type of privacy factors. Therefore, the feature representation of an image is the combination of a graph G and a vector O, that is $X = [G, O]$ .

There are several advantages to using a graph as the description of an image. Firstly, it reduces the dimensions of the classifier because we manually select and filter visual features considering their relevance to privacy to avoid learning about knowledge that is not related to privacy. Secondly, the graph combines results of multiple learning models and build more logical associations. Thirdly, other knowledge can be integrated, not just the content of the image itself. And finally, since the nodes and edges of the graph are labeled, the calculation on the graph is simpler.

![](images/0978a54156d5c223a807f65dd561bba51319a9da46eceb26c4e8ec7adb84d296.jpg)



Fig. 1. System Overview

![](images/ae9779034d799c7c60935856cfe566292bbe148d8d03185550ab3acd8fa9a5bc.jpg)



Fig. 2. Feature Representation

Formally, we illustrate the feature representation $x_{i}$ of an image $im_{i}$ , which consists of a vector $O_{i}$ and a graph $G_{i}$ . The vector $O_{i}$ is used to represent the features that describe multiple entities or reflect the entire image content, which consists of four types features: time, location, number of person and scene. As for the graph $G_{i}$ , it's the feature representation in the form of Entity-Attribute-Relationship. It's an undirected two-layer graph $G(V,E)$ which consists of multiple types of nodes and multiple types of edges. The node set V of the graph G mainly contains two types of nodes, identifier node $v^{id}$ and attribute node $v^{a_{i}}$ . The identifier node $v^{id}$ uniquely identifies each entity in an image, such as a person or a dog. The attribute node $v^{a_{i}}$ describes the characteristics of the entity, such as bareness. In fact, nodes with different attributes are also different kinds of nodes. The edge set E also mainly contains two types. The first is the edge $e_{ij}^{id}$ between identifier node $v_{i}^{id}$ and identifier node $v_{j}^{id}$ , which describes the relationship between two entities, such as behavior or intimacy. The other is the edge $e_{ij}^{a_{k}}$ between identifier node $v_{i}^{id}$ and attribute node $v_{j}^{a_{k}}$ , which represents the value of the entity $v_{i}^{id}$ about the attribute $v_{j}^{a_{k}}$ . The example of feature representation of an image is as figure 2. In the section IV-D, we will briefly introduce the features in the feature representation.

# B. Privacy Definition

In the section IV-A, we have fused a variety of user-understandable features as feature representations of images. However, how they reflect the privacy in the images. Intuitively, if we say the specific person in the image causes it to be a private image, the person is mapped to the identifier node in the graph of feature representation. Other cases, such as multiple people or person being too naked, cause the image to be a private image, which can also be mapped to multiple nodes and edges in the feature representation. Therefore, image privacy is a substructure of feature representation in fact. The goal of our work is to design a personalized and interpretable privacy definition for users, so we use rules to define user image privacy as follows.

Definition 1: A user $u_i$ 's personal privacy definition is defined by a set of rules $\mathcal{R}_{u_i} = \{r_{u_i}^1, r_{u_i}^2, ..., r_{u_i}^R\}$ . Each rule $r_{u_i}^k$ is a description of user $u_i$ 's image privacy. $r_{u_i}^k$ is the substructure of feature representation $\mathcal{X}$ .

Since the feature representation is user-understandable and each rule is a substructure of the feature representation, the rules are also user-understandable. Therefore, the rules are interpretable for users. Given the user's dataset $D_{u_{i}}$ , we learn the user's rule set $R_{u_{i}}$ about private images. So the rules are also personalized for users.

Formally, the definition of rule $r$ is as follows:

$$
\oplus \leftarrow f _ {1} \wedge f _ {2} \wedge \dots \wedge f _ {L} \tag {1}
$$

where $\oplus$ is the target class $c_{i} \in C$ . The right part of the logical implication symbol $\leftarrow$ is the rule body, which is a conjunction of logical literal $f_{k}$ , where the conjunction symbol $\wedge$ represents the logical relationship 'and'. Each literal $f_{k}$ is a boolean expression that verifies the instance of the property. L is the number of logical literals in the rule body, indicating the length of the rule. The semantic meaning of such a rule is:

$$
I F f _ {1} \text {   and   } f _ {2} \text {   and   ...   and   } f _ {L} \text {   THEN   Class } = \oplus \tag {2}
$$

In order to learn such rule set $R_{u_{i}}$ from user dataset $D_{u_{i}}$ , There are three machine learning methods to choose from: decision tree, random forest and rule learning. Decision tree is a method based on attribute testing. After the decision tree is constructed, a rule can be formed by traversing the path formation from the root node to the leaf node. Random forest is an ensemble learning method based on decision tree, which combines multiple decision trees. As for rule learning, it is a learning method based on attribute values and it can directly learn the rules in the form of formula 1. Compared to decision trees and random forests, it can learn fewer rules, so it has a more concise description for the user's privacy definition. So we use rule learning to learn user privacy rules. Since the feature representation contains a graph, we use [14] to convert the relational representation into the propositional representation and then apply RIPPER [15] to learn user's rule set. RIPPER's generalization performance exceeds many decision tree algorithms, and the learning speed is faster than most decision tree algorithms. After learning the user's rule set, we can use it to detect privacy image as algorithm 1.

Algorithm 1 Personalized Privacy Image Detection   
Input: Image: $im_{i}$ , Rule set: $R_{ui}$ Output: Result: $p_{i}$ , Rule: $R_{im_{i}}$ 1: $p_{i} = 0$ , $R_{im_{i}} = \phi$ 2: $x_{i}$ =featureExtraction( $im_{i}$ )

3: for each $r_{u_{i}}$ in $R_{u_{i}}$ do

4: if Matched( $x_{i}, r_{u_{i}}$ ) then

5: $p_{i} = 1$ , $R_{im_{i}} = R_{im_{i}} \cup r_{u_{i}}$ 6: end if

7: end for

8: return $p_{i}$ , $R_{im_{i}}$

# C. Privacy and Utility

We use the rule set $\mathcal{R}_{u_i}$ to detect the user $u_i$ 's privacy images. Once the image is judged to be private, it is intuitive to filter it directly. However, considering the utility of images, we can make appropriate modifications to the private images to ensure the utility while protecting the privacy. The rule matched to the image is the privacy description of the image. When the rule contains the feature in vector $O$ , it describes the privacy of entire image content, so we filter out private image directly. And when the rule is the substructure of graph $G$ , we don't have to filter out the image directly and we can modify the node to break the rule match for privacy protection. Our goal is to minimize the modifications.

For a private image $im_{i}$ , we can get a matched rule $R_{im_{i}}$ . For each rule $r_{im_{i}}^{k}$ , we define an associated node set $V_{i}^{k}$ which consists of the identifier nodes that contained in the rule or connected to the edges contained in the rule. We combine all the associated node sets of the matched rules into a privacy node set $V_{i}^{R}$ without duplicate nodes as follows:

$$
\mathcal {V} _ {i} ^ {\mathcal {R}} = \mathcal {V} _ {i} ^ {1} \cup \mathcal {V} _ {i} ^ {2} \cup \dots \cup \mathcal {V} _ {i} ^ {R} \tag {3}
$$

By this way, we can reduce this problem to a combinatorial optimization problem that is choosing a node set $V_{i}^{p}$ from the associated node set $V_{i}^{R}$ . The node set $V_{i}^{p}$ needs to satisfy the minimum loss of image utility, and the image feature representation after removing these nodes no longer match any privacy rules. The formal description is as follows:

$$
\min \sum_ {v _ {j} \in \mathcal {V} _ {i} ^ {p}} f (v _ {j}) \text {   s.t.   } \bigcup_ {v _ {i} \in \mathcal {V} _ {i} ^ {p}} c (v _ {j}) = \mathcal {R} _ {i m _ {i}} \tag {4}
$$

where $f$ is the value evaluation function of node $v_{j}$ and $c$ is the association function that return a rule set that the rule's associated node set contain $v_{j}$ . By this way, we can find the nodes with the least utility loss and locate their position in the image. Therefore, we can carry out subsequent privacy protection operations on these areas, such as blur or mosaic.

# D. Visual and Semantic Features

In this section, we briefly introduce the visual and semantic features used by our method.

Face Recognition: We use a python-based open-source face recognition library [16]. It has an accuracy of 99.38% on the Labeled Faces in the Wild benchmark. It is used to identify the person in the images.

SIFT and Color Histogram: They are both usually used to detect image similarity. In this work, we use them to identify objects in the images approximately.

Semantic Segmentation: Semantic segmentation method Yolov2 [17] is used to get the locations and classes of the objects in the images. They are the class attributes of entities.

Bareness: The YCbCr-based pornographic image detection method is used to describe the bareness feature. It expresses the degree of exposure by calculating the proportion of the person's skin color. It is the bareness attribute of person.

Intimacy: We count the number of simultaneous occurrences of two entities in the dataset as their intimacy.

Scene Recognition: The CNN model ResNet152 trained by Places365 can recognize 365 kinds of scenes and each scene is also mapped to an indoor or outdoor scene.

Metadata: The time and location information contained in the metadata of the images is what we need.

# V. EVALUATION

We evaluated our approach on two datasets. The first is PicAlert dataset published by zerr et al. [4]. We use a subset of PicAlert, which contains 17,189 public images and 5,299 private images. PicAlert is crawled from the image posted by flicker and labelled by multiple people voting, which does not properly reflect personalized privacy. Therefore, we collected another dataset, which totally has 8744 images of 20 users. Each user provides more than 200 images from their own camera and labels these images as "private" or "public" in accordance with their privacy standards. Finally, there are 4621 private images and 4123 public images. We call the dataset PPP. Both datasets are divided into training set and test set and 10-fold cross-validation is performed.

We compare our method IEye with several baseline methods including manual feature SIFT and deep feature.

SIFT: The work of [4], [10], [18] all researched the performance of SIFT in the classification of privacy images. It has better performance than other visual feature such as color histograms and edge-direction coherence vector etc. [4], [10]. For SIFT, we construct a vocabulary of visual words using BOVW approach and train with SVM model for privacy image detection.

![](images/f4973c8a092b538f0468e0221b1de7a69d6af3e384b340ff3534acc0bd184c21.jpg)



(a) Accuracy of privacy image detection on dataset PicAlert and PPP

![](images/3dc2cb3093da1b1e3f023aa306605d8c68b2d4d2c65229225ad40b4eb4af7cf9.jpg)



(b) Precision of privacy image detection on dataset PicAlert and PPP

![](images/ca773f8487940e9344c3adebf1f90dfab8a687353ff71672c3b6d09afe6b427b.jpg)



(c) Recall of privacy image detection on dataset PicAlert and PPP

![](images/6f719184cc2819e06213e0387dd77e5fd0b28a83a371b75428ddf0359785d7be.jpg)



(d) F1-measure of privacy image detection on dataset PicAlert and PPP   
Fig. 3. Performance (accuracy, precision, recall and f1-measure) of privacy image detection on dataset PicAlert and PPP for different methods.

Deep Feature [13]: Deep learning features are extracted from pre-trained deep networks AlexNet, VGG16 and ResNet152 and the dimensions of these features are all 1000. And then SVM model is trained using these features.

The validation results are shown in Figure 3, which shows the results of different baseline methods and our method IEye on two datasets PicAlert and PPP. For picAlert, we train a unified model to predict the privacy image and calculate its prediction results. Furthermore, we train a model for each user in PPP dataset to predict privacy images and use the weighted average method to obtain the prediction result based on the number of each user's images. For picAlert dataset, the accuracy of our method is $78.7\%$ , which performs better than the manual feature SIFT, however, not better than the deep features. As for PPP dataset, the accuracy of our method is $83.5\%$ , which is better than SIFT and deep feature. PicAlert is a generic dataset and its amount is much larger than each user's dataset in PPP. The validation results show that our method is comparable with the deep features on general privacy image detection and our method performs better on small sample datasets and is more suitable for personalized privacy image detection. In addition, since we leverage the form of rule sets, our model is interpretable for the detection results, which is not available in other methods.

# VI. CONCLUSION

In this work, we design a personalized fine-grained and interpretable image privacy detection method and a privacy protection scheme with minimum utility loss. Experimental results show that our method achieves better performance on personalized privacy image detection than that using handcrafted features and deep features. With the development of computer vision technology, more advanced feature representations will further improve the efficiency and interpretability of our method. In addition, privacy leakages caused by the relationship between multiple images or multiple datasets will considered in our future work.

# ACKNOWLEDGMENT

This research is supported by the National Key RD Program of China 2017YFB1003003, NSF China under Grants No. 61822209, 61932016, 61751211, China National Funds for Distinguished Young Scientists with No.61625205, the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] M. Madejski, M. Johnson, and S. M. Bellovin, “A study of privacy settings errors in an online social network,” in Pervasive Computing and Communications Workshops (PERCOM Workshops), 2012 IEEE International Conference on. IEEE, 2012, pp. 340–345.   
[2] A. Frome, G. Cheung, A. Abdulkader, M. Zennaro, B. Wu, A. Bissacco, H. Adam, H. Neven, and L. Vincent, “Large-scale privacy protection in google street view,” in Computer Vision, 2009 IEEE 12th International Conference on. IEEE, 2009, pp. 2373–2380.   
[3] L. Tran, D. Kong, H. Jin, and J. Liu, “Privacy-cnh: A framework to detect photo privacy with convolutional neural network using hierarchical features.” in AAAI, 2016, pp. 1317–1323.   
[4] S. Zerr, S. Siersdorfer, J. Hare, and E. Demidova, “Privacy-aware image classification and search,” in Proceedings of the 35th International ACM SIGIR Conference on Research and Development in Information Retrieval, ser. SIGIR ’12. New York, NY, USA: ACM, 2012, pp. 35–44.   
[5] D. Buschek, M. Bader, E. von Zezschwitz, and A. De Luca, Automatic Privacy Classification of Personal Photos. Cham: Springer International Publishing, 2015, pp. 428–435.   
[6] A. K. Tonge and C. Caragea, “Image privacy prediction using deep features.” in AAAI, 2016, pp. 4266–4267.   
[7] J. Yu, B. Zhang, Z. Kuang, D. Lin, and J. Fan, “ipr Privacy: image privacy protection by identifying sensitive objects via deep multi-task learning,” IEEE Transactions on Information Forensics and Security, vol. 12, no. 5, pp. 1005–1016, 2017.   
[8] J. Yu, Z. Kuang, B. Zhang, W. Zhang, D. Lin, and J. Fan, “Leveraging content sensitiveness and user trustworthiness to recommend fine-grained privacy settings for social image sharing,” IEEE Transactions on Information Forensics and Security, vol. 13, no. 5, pp. 1317–1332, 2018.   
[9] E. Spyromitros-Xioufis, S. Papadopoulos, A. Popescu, and Y. Kompatsiaris, “Personalized privacy-aware image classification,” in Proceedings of the 2016 ACM on International Conference on Multimedia Retrieval. ACM, 2016, pp. 71–78.   
[10] A. C. Squicciarini, C. Caragea, and R. Balakavi, “Analyzing images’ privacy for the modern web,” in Proceedings of the 25th ACM conference on Hypertext and social media. ACM, 2014, pp. 136–147.   
[11] T. Orekondy, B. Schiele, and M. Fritz, “Towards a visual privacy advisor: Understanding and predicting privacy risks in images,” in 2017 IEEE International Conference on Computer Vision (ICCV). IEEE, 2017, pp. 3706–3715.   
[12] H. Zhong, A. Squicciarini, D. Miller, and C. Caragea, “A group-based personalized model for image privacy classification and labeling,” in Proceedings of the 26th International Joint Conference on Artificial Intelligence. AAAI Press, 2017, pp. 3952–3958.   
[13] A. Tonge and C. Caragea, “Image privacy prediction using deep neural networks,” arXiv preprint arXiv:1903.03695, 2019.   
[14] N. Lavrač and P. A. Flach, “An extended transformation approach to inductive logic programming,” ACM Transactions on Computational Logic (TOCL), vol. 2, no. 4, pp. 458–494, 2001.   
[15] W. W. Cohen, “Fast effective rule induction,” in Machine Learning Proceedings 1995. Elsevier, 1995, pp. 115–123.   
[16] A. Geitgey and J. Nazario, “Face recognition,” En ligne]. Disponible sur: https://github.com/ageitgey/face\_recognition, 2017.   
[17] J. Redmon and A. Farhadi, “YOLO9000: better, faster, stronger,” CoRR, vol. abs/1612.08242, 2016. [Online]. Available: http://arxiv.org/abs/1612.08242   
[18] A. Squicciarini, C. Caragea, and R. Balakavi, “Toward automated online photo privacy,” ACM Transactions on the Web (TWEB), vol. 11, no. 1, p. 2, 2017.