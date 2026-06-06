# Extensible Cross-Modal Hashing

Tian-yi Chen1 , Lan Zhang1,2 ∗ , Shi-cong Zhang1 , Zi-long Li3 and Bai-chuan Huang4

1School of Computer Science and Technology, University of Science and Technology of China, China

2School of Data Science, University of Science and Technology of China, China

3School of Information Science and Engineering, Northeastern University, China

4Department of Physics, University of California Berkeley, USA

wandero@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, zsc2016@mail.ustc.edu.cn, longzili@stumail.neu.edu.cn, huangbc1998@gmail.com

# Abstract

Cross-modal hashing (CMH) models are introduced to significantly reduce the cost of large-scale cross-modal data retrieval systems. In many realworld applications, however, data of new categories arrive continuously, which requires the model has good extensibility. That is the model should be updated to accommodate data of new categories but still retain good performance for the old categories with minimum computation cost. Unfortunately, existing CMH methods fail to satisfy the extensibility requirements. In this work, we propose a novel extensible cross-modal hashing (ECMH) to enable highly efficient and low-cost model extension. Our proposed ECMH has several desired features: 1) it has good forward compatibility, so there is no need to update old hash codes; 2) the ECMH model is extended to support new data categories using only new data by a well-designed “weak constraint incremental learning” algorithm, which saves up to 91% time cost comparing with retraining the model with both new and old data; 3) the extended model achieves high precision and recall on both old and new tasks. Our extensive experiments show the effectiveness of our design.

# 1 Introduction

With the rapid development of the Internet and smart devices, large amounts of data, such as texts, images and videos, are constantly being produced. Facing massive multi-modal data, efficient cross-modal information retrieval is badly needed in various big data applications. The main challenge of cross-modal retrieval is to solve the “media gap”, since every modality has its distinct feature space. To address this issue, a popular solution is to learn a correspondence which maps data of different modalities to vector representations in an intermediate common space and expresses the similarity among these data by their distances in the common space. Traditional statistical correlation analysis based methods, e.g., Canonical Correlation Analysis (CCA), map data from different modalities to a subspace where pairwise correlations between two modalities will be maximized. Those methods, however, incur high computation and storage cost because of the highdimensional float number vectors and the calculation of pairwise Euclidean distances. Recently, researchers introduce Cross-Modal Hashing (CMH) to significantly reduce the cost while retaining retrieval performance for large-scale crossmodal data [Bronstein et al., 2010; Zhen and Yeung, 2012; Wu et al., 2015; Lin et al., 2015]. It maps data into a common Hamming space and uses Hamming distance instead of Euclidean distance. The common space can be learned by a Deep Neural Network (DNN), which acts as a non-linear extension of CCA, in supervised manners [Chen et al., 2018; Zhang et al., 2014] or unsupervised manners [Shen et al., 2015; Wu et al., 2018]. CMH is now widely adopted for cross-modal data retrieval [Wang et al., 2016; Baltrusaitis et al., 2018].

CMH models achieve good performance in cross-modal retrieval tasks; however, in many real-world applications, new data of new categories comes continuously, which requires the system has extensibility. So the model should be updated to accommodate data of new categories but still retain good performance for the old categories, and the system should still be compatible with old hash codes. Unfortunately, existing CMH models lack extensibility. Fine-tuning the model using only new data suffers from a catastrophic forgetting that results in an accuracy decrease on old tasks [Li and Hoiem, 2018]. Retraining the whole model with both old and new data incurs an ever increasing large computation cost for training and updating the hash codes for all existing data, as well as a large storage cost for all old data, There are some incremental learning methods consider the extensibility problem [Joshi and Kulkarni, 2012], but most of which focus on classification tasks [Cortes and Vapnik, 1995; Guo et al., 2010]. The main techniques include adding new output dimensions for new tasks [Razavian et al., 2014] and applying regularization for old tasks [Hinton et al., 2015]. Those method cannot resolve the cross-modal hashing problem, since they continuously increase the dimension of the common feature space, thus the length of the hash code, whenever data of a new category comes.

In this work, we propose a novel extensible cross-modal hashing (ECMH) to empower the CMH models with good extensibility. To the best of our knowledge, this is the first work addressing the extensible cross-modal hashing problem.

![](images/96da2fa2b5cf938b9b5e9c437e5489c26f7d66bf14b26aac987938c293eaa19a.jpg)



Figure 1: ECMH framework.

Our proposed ECMH has several desired features for largescale cross-modal retrieval systems: 1) it is compatible with old hash codes, there is no need to increase the dimension of hash code or update old hash codes; 2) ECMH is extended to support new categories using only the new data by a welldesigned “weak constraint incremental learning” algorithm; 3) the extended model achieves high precision and recall in both old and new tasks, and the hash codes generated by the extended model has good forward compatibility with the old hash codes. These features of ECMH enables highly efficient and low-cost cross-modal data system extension.

# 2 ECMH

# 2.1 Problem Definition

In a typical cross-modal data retrieval application, suppose we already have an old dataset with $N _ { o }$ cross-modal data pairs, e.g., image-text pairs, which can be represented by $\bar { \mathcal { D } } _ { o } = \{ \bar { ( } x _ { o } ^ { i } , y _ { o } ^ { i } ) \bar { , } 0 < i \bar { \leq } N _ { o } \}$ here the subscript $\because \mathrm { o } ^ { \prime \prime }$ is the abbreviation $\mathrm { f o r } \ddot { \cdots } \mathrm { o l d } . \dot { \overline { { \mathbf { \Gamma } } } }$ With this dataset, through cross-modal hashing we can train a deep hash function $h ( \bar { \mathcal { D } } ; \theta _ { o } )$ with parameters $\theta _ { o }$ for old tasks (e.g., image-text pairs of animals), that hashes two-modal data into a set of unified hash codes $\mathcal { C } _ { o \mid \theta _ { o } } ~ = ~ \{ - 1 , + 1 \} ^ { M \times L }$ . Here L is the length of the hash code, and M is the number of instances. When there comes a set of new cross-modal data pairs $\mathcal { D } _ { n } ~ = ~ \{ ( x _ { n } ^ { i } , y _ { n } ^ { i } ) , 0 ~ <$ < $i \ \leq \ N _ { n } \}$ for new tasks (e.g., image-text pairs of scenes), where the subscript $\ " _ { \mathrm { ~ n ~ } } \cdot $ is the abbreviation for “new”, ECMH mainly focuses on the extensibility issue of the hash function. Specifically, ECMH aims to update parameters $\theta _ { o }$ to new parameters $\theta _ { n }$ to satisfy the following requirements: 1) we don’t need to update old codes $\mathcal { C } _ { o } ; 2 )$ we don’t need to increase the hash code length $L ; 3 )$ we update the hash function $h ( \mathcal { D } ; \theta _ { o } )$ using only the new dataset ${ \bar { \mathcal { D } } } _ { n } ; 4 )$ the hash codes $\mathcal { C } _ { n | \theta _ { n } }$ of the new dataset generated by the updated hash function $h ( D ; \theta _ { n } )$ achieve good performance on both old and new tasks. These features of ECMH enables highly efficient and low-cost cross-modal data system extension with a precision guarantee.

# 2.2 Design Overview

As shown in Figure 1, the model of ECMH consists of two deep hashing networks for images and texts, named INet and TNet respectively. With the old dataset $\mathcal { D } _ { o } ,$ , we can train the model to obtain old parameters $\theta _ { o }$ . When the new dataset $\mathcal { D } _ { n }$ comes, the process of updating parameters to $\theta _ { n }$ includes three stages. Stage 1 is warm-up that initializes new word vectors of new tasks; Stage 2 is generating codes $\mathcal { C } _ { n | \theta _ { o } }$ for the new dataset using the old parameters $\theta _ { o } ;$ Stage 3 updates the model using the new dataset according to our proposed objective function Eq.(1).

# 2.3 Deep Feature Learning and Warm-up

Most existing deep hashing networks for texts support only fixed vocabulary size, which makes them incompetent to handle out-of-vocabulary (OOV) words in the newly arriving data. To address this issue, we adopt Deep Averaging Network (DAN) [Iyyer et al., 2015]as TNet, and initialize new word vectors of new tasks in Stage 1. Specifically, we freeze all old parameters except those of the embedding layer of TNet and then fine-tune the embedding layer for new word vectors. Through TNet, each raw text $y ^ { i }$ is firstly encoded into a 2000-dimensional sentence vector and then embedded into an L-dimensional hash code. INet can be any deep hashing network for images. In our implementation, INet is adapted from VGG-19 [Simonyan and Zisserman, 2015] by only modifying the number of hidden units in the last FC layers to generate L-dimensional hash codes Moreover, for both INet and TNet we apply the hyperbolic tangent function (tanh) to normalize output to $( - 1 , 1 )$ range to accelerate the model convergence. Let $h ^ { x } ( X ; \theta )$ denote INet, and $h ^ { y } ( Y ; \theta )$ denote TNet. INet/TNet produces a deep representation for each image/text. Thus, given a cross-modal dataset, the matrices of deep representations of images and texts are $F$ and G respectively. The generated hash code $\begin{array} { r } { \mathcal { C } = s i g n ( F + G ) } \end{array}$ . Since ECMH will update the old parameters $\theta _ { o }$ to $\theta _ { n } .$ , there will be two versions of F and G. We use a subscript n $\lvert \theta _ { o }$ to indicate the deep representations of data for new task generated with old parameters $\theta _ { o } ,$ , and so on.

# 2.4 Objective Function of ECMH

It is nontrivial to accommodate the new parameters $\theta _ { n }$ to both new and old tasks in a way satisfying the aforementioned requirements. A traditional fine-tuning method using only data for new tasks suffers the catastrophic forgetting effect, leading to deteriorating performance on old tasks. The core idea of ECMH is performing selective learning considering the cross-modal agreement of both deep representations generated with old parameters (in Step 2) and new parameters (in Step 3). Specifically, if the generated deep representations of an image-text pair have the same values on some dimensions, these “agreed” dimensions should be excluded from updating. The objective function of ECMH is designed to find “agreement” that does not need to change and keep it, meanwhile find “disagreement” and try to reach “agreement.” As the following equation, the objective function is composed of three loss functions:

$$
\min _ {\mathcal {C}, \theta_ {t} ^ {x}, \theta_ {t} ^ {y}} \mathcal {L} = \mathcal {L} _ {d} + \mathcal {L} _ {c} + \mathcal {L} _ {h} \tag {1}
$$

$$
s. t. \mathcal {C} \in \{- 1, 1 \} ^ {M \times L}
$$

The novel self-taught distillation loss $\mathcal { L } _ { d }$ is proposed to keep those “agreed” dimensions unchanged according to deep representations generated with old parameters, which ensures the performance of the updated model on old tasks. The common space learning loss $\mathcal { L } _ { c }$ and hash function learning loss $\mathcal { L } _ { h }$ work together to minimize “disagreement” of deep representations generated with updated parameters, which improve the performance of the updated model on new tasks. In the rest of this section, we introduce the detailed design of three loss functions.

# Agreement Matrix and Similarity Matrix.

First, we introduce two measurement matrices. $A _ { \alpha }$ is the Agreement Matrix with a threshold $\alpha ,$ which records the cross-modal agreement of $F _ { n | \theta _ { c } }$ and $G _ { n | \theta _ { o } }$ , i.e., matrices of deep representations generated with old parameters. $A _ { \alpha }$ could be defined as:

$$
A _ {\alpha} [ i, j ] = \left\{ \begin{array}{l l} 1, & \text { sign } (F _ {n | \theta_ {o}} [ i, j ]) = \text { sign } (G _ {n | \theta_ {o}} [ i, j ]), \\ & | F _ {n | \theta_ {o}} [ i, j ] | > \alpha , | G _ {n | \theta_ {o}} [ i, j ] | > \alpha \\ 0, & \text { others } \end{array} \right. \tag {2}
$$

The threshold α ensures the agreement is not too weak since a small absolute value of the representation indicates low confidence and mutability.

The Similarity matrix S is defined as:

$$
S [ i, j ] = \left\{ \begin{array}{l l} 1, & d _ {i} \text {   shares   at   least   one   label   with   } d _ {j} \\ 0, & d _ {i}, d _ {j} \text {   don't   share   label. } \end{array} \right. \tag {3}
$$

where d represents an image or a text in the dataset.

# Self-taught Distillation Loss.

The novel self-taught distillation loss is to maintain the performance of the updated model on old tasks. The underlying assumption is that if the output with $\theta _ { n }$ and $\theta _ { o }$ follow a similar probability distribution, the models with $\theta _ { n }$ and $\theta _ { o }$ have similar performance. Given a cross-modal data pair, the agreement matrix $A _ { \alpha }$ acts as a selector that samples the dimensions which should be unchanged within its output for this input data, while $\left( \mathbf { 1 } - A _ { \alpha } \right)$ samples the dimensions that should be changed. Then utilizing the old representations $F _ { n | \theta _ { o } } , G _ { n | \theta _ { o } }$ , the self-taught distillation loss is defined as

$$
\begin{array}{l} \mathcal {L} _ {d} = \lambda_ {d} \left(\| A _ {\alpha} \circ \left(F _ {n \mid \theta_ {n}} - F _ {n \mid \theta_ {o}}\right) \| _ {F} ^ {2} \right. \tag {4} \\ + \left\| A _ {\alpha} \circ \left(G _ {n | \theta_ {n}} - G _ {n | \theta_ {o}}\right) \right\| _ {F} ^ {2}). \\ \end{array}
$$

F is the Frobenius norm of a matrix, and is the Hadamard ||·|| product. Suppose $F _ { n } \in \mathbb { R } ^ { M \times L }$ , then $\begin{array} { r } { \lambda _ { d } = \frac { 1 } { M \times L ^ { 2 } } } \end{array}$ serves as the scaling factor.

# Common Space Learning.

The common space learning loss $\mathcal { L } _ { c }$ is utilized to construct the common space by forcing the model to generate similar hash codes for semantically similar instances and vice versa. The similarity of instances is defined as Eq. (3), and the similarity of deep representations is defined as:

$$
\Delta = \left(\left(\mathbf {1} - A _ {\alpha}\right) \circ F _ {n \mid \theta_ {n}}\right) G _ {n \mid \theta_ {n}} ^ {T} \tag {5}
$$

$$
s. t. F _ {n | \theta_ {n}}, G _ {n | \theta_ {n}} \in \mathbb {R} ^ {M \times L}
$$

As mentioned above, $\left( \mathbf { 1 } - A _ { \alpha } \right)$ samples the disagreed dimensions and then we can calculate the similarity of deep representations on these disagreed dimensions. We define S to represent the sum of all elements in a matrix for simplicity. By minimizing the term $\| ( \mathbf { 1 } - S ) \circ \Delta \| _ { S }$ , we can reduce the similarity between dissimilar instances. Minimizing the term $\| S \circ ( l o \bar { g } ( 1 + e ^ { \Delta } ) - \Delta ) \| _ { S }$ maximizes the similarity between similar instances. Combining both terms as below, we get the loss function for common space learning:

$$
\mathcal {L} _ {c} = \lambda_ {c} (\| (1 - S) \circ \Delta \| _ {S} + \| S \circ (l o g (1 + e ^ {\Delta}) - \Delta) \| _ {S}). \tag {6}
$$

Here the scaling factor $\lambda _ { c }$ is $\frac { 1 } { M ^ { 2 } \times L }$ . There could be other possible choices of $L _ { c } ,$ as long as they obey the core idea.

# Hash Functions Learning.

The hash function learning loss is defined as:

$$
\mathcal {L} _ {h} = \lambda_ {h} \left(\| (1 - A) \circ (\beta \mathcal {C} - F _ {n | \theta_ {n}}) \| _ {F} ^ {2} \right. \tag {7}
$$

$$
+ \left\| (1 - A) \circ (\beta \mathcal {C} - G _ {n | \theta_ {n}}) \right\| _ {F} ^ {2})
$$

The scaling factor λh is 1M2 L . $\lambda _ { h }$ $\frac { 1 } { M ^ { 2 } \times L }$ This loss is similar to that of previous work like DCMH [Jiang and Li, 2017] and SSAH [Li et al., 2018], except for the hash code smoothing factor $\beta .$ Since the output of TNet and INet are rescaled to the range (−1, 1) by tanh, the $\mathcal { C } \in \{ - 1 , 1 \} ^ { M \times L }$ will be too intense to be the targeted hash codes. In practice, we observe that this issue results in a great disparity between the average of $F _ { n | \theta _ { n } }$ and $G _ { n | \theta _ { n } }$ . Some efforts assign weights to each modality and partially solve the problem. Rather than tweaking the weights, our solution smoothes the targeted hash code  with $\beta$ to reduce the difference significantly. This design helps prevent overfitting when training the old model.

# 2.5 Optimization

The optimization process of ECMH including the following steps: training old model for old tasks, warm up the TNet for new vocabulary and extending the model for new tasks. Like most previous solutions, we adopt an alternating strategy in every step to solve the non-convex objective function iteratively.

As presented in Algorithm 1, the core algorithm is designed to train the model according to the objective function defined in Eq. 1. Firstly, we fix parameter ${ \bar { \theta } } ^ { y }$ of TNet and hash codes . A mini-batch of images is sampled from the whole train set to update $\theta ^ { x }$ . Then $\overleftarrow { \theta ^ { x } }$ and  are fixed. A mini-batch of texts is sampled to update $\theta ^ { y } .$ . These first two steps utilize the stochastic gradient descent (SGD) [Bottou, 2010] with the back-propagation (BP) algorithm to update the network parameters. Finally, we fix $\theta ^ { x }$ and $\theta ^ { y }$ and update C through the following equation:

Algorithm 1 Core Algorithm   
Require: Image set X, text set Y, similarity matrix S, agreement matrix $A_{\alpha}$ , old representations $F_{n|\theta_{o}}$ , $G_{n|\theta_{o}}$ , old parameters $\theta_{o}^{x}$ , $\theta_{o}^{y}$ , mini-batch size m, learning rate $\mu$ .   
Ensure: Parameters $\theta _ { n } ^ { x } , \theta _ { n } ^ { y }$ of INet and TNet.

1: Initialize: iter $\leftarrow \lceil Sizeof(X) / m\rceil$ , $(\theta_n^x,\theta_n^y)\leftarrow (\theta_o^x,\theta_o^y)$ 2: repeat
3:    for 1, ..., iter do
4:    Sample a mini-batch $\mathcal{M}$ with $m$ images from $X$ .
5:    F $\leftarrow h^{x}(\mathcal{M};\theta_{n}^{x})$ 6:    Update $\theta_{n}^{x}$ by SGD with BP:
7: $\theta_{n}^{x} \leftarrow \theta_{n}^{x} - \mu \nabla_{\theta_{n}^{x}}(\mathcal{L}_{d}(F_{n|\theta_{n}},F_{n|\theta_{o}}) + \mathcal{L}_{c}(F_{n|\theta_{n}},G_{n|\theta_{n}},S) + \mathcal{L}_{h}(F_{n|\theta_{n}},\mathcal{C}))$ 8:    end for
9:    for 1, ..., iter do
10:    Sample a mini-batch $\mathcal{M}$ with $m$ images from $Y$ .
11:    G $\leftarrow h^{y}(\mathcal{M};\theta_{n}^{y})$ 12:    Update $\theta_{n}^{y}$ by SGD with BP:
13: $\theta_{n}^{y} \leftarrow \theta_{n}^{y} - \mu \nabla_{\theta_{n}^{y}}(\mathcal{L}_{d}(G_{n|\theta_{n}},G_{n|\theta_{o}}) + \mathcal{L}_{c}(G_{n|\theta_{n}},F_{n|\theta_{n}},S) + \mathcal{L}_{h}(G_{n|\theta_{n}},\mathcal{C}))$ 14:    end for
15:    Update $\mathcal{C}$ by Eq. (8).
16: until Convergence

Algorithm 2 Extending Model for New Tasks   
Require: Image set $X_{n}$ and text set $Y_{n}$ for new tasks, similarity Matrix S, mini-batch size m, learning rate $\mu$ , parameters $\theta_{o}^{x}, \theta_{o}^{y}$ of the to-be-extended model.
Ensure: Parameters $\theta_{n}^{x}, \theta_{n}^{y}$ of INet and TNet.
1: Initialize: iter $\leftarrow \lceil Sizeof(X)/m \rceil, (\theta_{n}^{x}, \theta_{n}^{y}) \leftarrow (\theta_{o}^{x}, \theta_{o}^{y})$ 2: Freeze $\theta_{n}^{x}, \theta_{n}^{y}$ except for the embedding layer. ▷ Warm-up
3: $F_{n|\theta_{o}} \leftarrow h^{x}(X_{n}; \theta_{o}^{x})$ 4: Learn $\theta_{n}^{y}$ by the Core Algorithm.
5: Unfreeze $\theta_{n}^{x}, \theta_{n}^{y}$ except for CNN layers. ▷ Extending
6: Calculate $A_{\alpha}$ by the Eq. (2).
7: $G_{n|\theta_{o}} \leftarrow h^{y}(Y_{n}; \theta_{o}^{y})$ 8: Learn $\theta_{n}^{x}, \theta_{n}^{y}$ by the Core Algorithm.

$$
\mathcal {C} = \operatorname{sign} (F + G) \tag {8}
$$

Leveraging the core algorithm as the main component, we train the model for old tasks and extend the model for new tasks as follows. We can easily adapt the core algorithm to train the model for old tasks by setting $A _ { \alpha }$ to an all-zero matrix since we have no pre-knowledge of the agreement matrix and no dimension needs to stay unchanged when training a model from scratch. In extending a model, the first thing is to ”warm-up” the new word vectors on the new tasks. We freeze all parameters but the embedding layer in TNet and train the network using the core algorithm. Then, we unfreeze all FC layers and start extending. The process is in Algorithm 2.

# 3 Experiment

# 3.1 Datasets and Experiment Setting

In our experiments, we adopt two popular datasets with image-text pairs. The MIRFLICKR-25k dataset [Huiskes and Lew, 2008] contains 25,000 image-text pairs collected from Flickr. For a fair comparison, we reduce the number of instances to 20,015 following the experiment protocols given in DCMH [Jiang and Li, 2017]. Each text is represented by a 1386-dimensional BoW vector and the corresponding image is rescaled to a (224, 224, 3) RGB tensor. We also adopt the MSCOCO-2014 dataset [Lin et al., 2014] for its high-quality annotations. There are 55% of the images in MSCOCO labeled with “person”, which makes the new tasks too similar to the original ones. In this case, all methods perform well when extending on the original MSCOCO dataset. To evaluate our design in more general scenarios, we remove all “person” images and obtain a dataset with 36,869 instances. Each image is rescaled to (224, 224, 3) and annotated with at most ten words. Unlike some previous work, we conduct the evaluation in a more stringent condition that the validation set does not contain any training data. In experiments using MIRFLICKR-25k, 10,015 instances are randomly chosen as the train set, and the rest 10000 are used for validation, namely 2000 for the query and 8000 for the database. In experiments using MSCOCO, 16,869 randomly chosen instances are used for training, and the rest 5000 and 15000 instances are used as query and database, respectively.

For old tasks and new tasks, further we split each training/validation dataset into two parts by categories of labels. There are many ways to divide categories into old and new ones. Without loss of generality, we consider two extension cases.

Super-Category Extension. Super-categories, such as “Animal” and “Vehicle”, contain quite different concepts, while sub-categories, such as “Dog”, “Cat”, “Bike” and $\ "  \mathrm { C a r } ^ { \prime \prime }$ , may have similar concepts, which makes extension for new super-categories is more challenging. In MSCOCO, we divide data by their super-categories and use about 20,000 instances of super-categories“Animal”, “Appliance”, and “Indoor” as new tasks to extend the model trained by the data of the rest super-categories. Following the definition in MSCOCO, in Flickr25k, ”Animal, People, Plant, Water, Transport, Sky, Food” are super-categories, and the rest are sub-categories. Similarly, we use about 8,000 instances of super-categories “People” and “sky” as new tasks.

Sub-Category Extension. In Flickr25k, we randomly select 6 sub-categories with 8,200 instances as new tasks. In MSCOCO, 16 sub-categories with 12000 instances are selected as new tasks. All images of new categories will only be used in the extending stage to make sure that they are totally new (sharing zero label with the old training images) for the model.

Implementation Details. We implement ECMH via $\mathrm { P y } .$ - torch. We set all learning rate to 1.5 and decrease it by 5% every 100 steps. α is set to the range of [0.1, 0.15] and $\beta$ is set to 0.5. Batch size is fixed to 500. All experiments are conducted on a server with 4 TITAN X GPUs.

Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence (IJCAI-19) 

<table><tr><td rowspan="2" colspan="2"></td><td colspan="2">Flickr_Sub</td><td colspan="2">Flickr_Super</td><td colspan="2">COCO_Sub</td><td colspan="2">COCO_Super</td></tr><tr><td> $T \rightarrow I$ </td><td> $I \rightarrow T$ </td><td> $T \rightarrow I$ </td><td> $I \rightarrow T$ </td><td> $T \rightarrow I$ </td><td> $I \rightarrow T$ </td><td> $T \rightarrow I$ </td><td> $I \rightarrow T$ </td></tr><tr><td rowspan="3">Retrieve Old Codes</td><td>Old Model</td><td>0.7366</td><td>0.7130</td><td>0.7605</td><td>0.7296</td><td>0.4101</td><td>0.4099</td><td>0.4777</td><td>0.4743</td></tr><tr><td>Fine-tuning</td><td>0.7114</td><td>0.6918</td><td>0.6960</td><td>0.6699</td><td>0.3967</td><td>0.4055</td><td>0.4312</td><td>0.4650</td></tr><tr><td>ECMH</td><td>0.7394</td><td>0.7058</td><td>0.7557</td><td>0.7181</td><td>0.4178</td><td>0.4342</td><td>0.4916</td><td>0.4789</td></tr><tr><td rowspan="5">Old Tasks</td><td>Joint-DCMH</td><td>0.6543</td><td>0.6644</td><td>0.6434</td><td>0.6558</td><td>0.4004</td><td>0.3067</td><td>0.4134</td><td>0.3155</td></tr><tr><td>Joint-SSAH</td><td>0.6597</td><td>0.6896</td><td>0.6579</td><td>0.6842</td><td>0.4333</td><td>0.3810</td><td>0.4160</td><td>0.3835</td></tr><tr><td>Joint-ECMH</td><td>0.6712</td><td>0.7145</td><td>0.6593</td><td>0.7043</td><td>0.4898</td><td>0.4052</td><td>0.4808</td><td>0.4263</td></tr><tr><td>Fine-tuning</td><td>0.6284</td><td>0.6731</td><td>0.5729</td><td>0.5984</td><td>0.4618</td><td>0.3707</td><td>0.4002</td><td>0.3403</td></tr><tr><td>ECMH</td><td>0.6557</td><td>0.7002</td><td>0.6279</td><td>0.6763</td><td>0.4930</td><td>0.4155</td><td>0.4450</td><td>0.4426</td></tr><tr><td rowspan="5">New Tasks</td><td>Joint-DCMH</td><td>0.7899</td><td>0.7384</td><td>0.8267</td><td>0.7556</td><td>0.4016</td><td>0.3664</td><td>0.3433</td><td>0.3328</td></tr><tr><td>Joint-SSAH</td><td>0.7738</td><td>0.7387</td><td>0.7837</td><td>0.7495</td><td>0.4302</td><td>0.4295</td><td>0.3923</td><td>0.4128</td></tr><tr><td>Joint-ECMH</td><td>0.8051</td><td>0.7707</td><td>0.8369</td><td>0.7922</td><td>0.4907</td><td>0.4896</td><td>0.4402</td><td>0.4522</td></tr><tr><td>Fine-tuning</td><td>0.8067</td><td>0.7416</td><td>0.8201</td><td>0.6781</td><td>0.5136</td><td>0.5228</td><td>0.4426</td><td>0.4483</td></tr><tr><td>ECMH</td><td>0.7958</td><td>0.7464</td><td>0.7839</td><td>0.7190</td><td>0.4948</td><td>0.4951</td><td>0.4221</td><td>0.4427</td></tr><tr><td rowspan="5">All Tasks</td><td>Joint DCMH</td><td>0.7414</td><td>0.6947</td><td>0.7418</td><td>0.6939</td><td>0.3358</td><td>0.3267</td><td>0.3363</td><td>0.3300</td></tr><tr><td>Joint SSAH</td><td>0.7322</td><td>0.7097</td><td>0.7318</td><td>0.7091</td><td>0.3836</td><td>0.3973</td><td>0.3858</td><td>0.3994</td></tr><tr><td>Joint-ECMH</td><td>0.7737</td><td>0.7375</td><td>0.7736</td><td>0.7378</td><td>0.4274</td><td>0.4335</td><td>0.4356</td><td>0.4403</td></tr><tr><td>Fine-tuning</td><td>0.7416</td><td>0.6975</td><td>0.6697</td><td>0.6379</td><td>0.4165</td><td>0.4217</td><td>0.3927</td><td>0.3955</td></tr><tr><td>ECMH</td><td>0.7569</td><td>0.7191</td><td>0.7336</td><td>0.6926</td><td>0.4437</td><td>0.4422</td><td>0.4223</td><td>0.4334</td></tr></table>

Table 1: MAP of different methods on different tasks. The best MAP of each task is highlighted in bold.

![](images/02adbacd901c0ceafa35f04c87c6165fb9e9ac0031cd34a5ac1cc6d13d12bc90.jpg)  
Figure 3: MAP during train- Figure 4: MAP of ECMH ing process. and Fine-tuning.

# 3.2 Methods for Comparison

Since there is no existing work directly addressing the extensible cross-modal hashing issue, we compare our proposed ECMH with two most relevant state-of-the-art cross-modal hashing methods DCMH [Jiang and Li, 2017] and SSAH [Li et al., 2018] by extending them in a joint-training manner. That is, when new data comes, we train ECMH, DCMH and SSAH using both old and new data and refer to these models as Joint-ECMH, Joint-DCMH and Joint-SSAH respectively. They provide the upper bound of precision and recall in all tasks. We also compare ECMH with a model trained in a traditional fine-tuning way. That is we first train an ECMH model using old data then directly fine-tune parameters using new data without considering agreement of old codes. All image networks utilize CNN layers of VGG-19 pretrained on ImageNet dataset. We use identical training set and validation set for all these methods and report their best results.

In the following experiments, we use the Mean Average Precision (MAP) and the precision-recall (PR) curve to evaluate different methods.

# 3.3 Training Efficiency

Figure 3 shows the MAP variation during the training phase of ECMH and DCMH. Due to the tanh activation function which rescales the output to (−1, 1) and the light-head TNet, our proposed ECMH achieves an about three times faster convergent speed than DCMH. We further compare the time consumption of ECMH and JointECMH, as shown in Table 2, ECMH significantly reduces time cost for the model extension for new tasks. As an example, in Super-Category Ex-

<table><tr><td></td><td>JointECMH</td><td>ECMH_old</td><td>ECMH_new</td></tr><tr><td>COCO_Super</td><td>5507</td><td>737</td><td>1833</td></tr><tr><td>COCO_Sub</td><td>5117</td><td>1010</td><td>912</td></tr><tr><td>Flickr_Super</td><td>3416</td><td>731</td><td>312</td></tr><tr><td>Flickr_Sub</td><td>3605</td><td>727</td><td>1229</td></tr></table>

Table 2: Training runtime (sec) for JointECMH and ECMH for old tasks and new tasks.

tension case, ECMH saves about 91% runtime to extend the model for new tasks using Flickr dataset and saves about 67% runtime using the MSCOCO dataset.

# 3.4 Performance on Different Tasks

We illustrate MAP of different methods in all cases in Table 1 and PR curves using the Flickr dataset in Figure 2. We omit the PR curves using the MSCOCO dataset due to space limitation, whose performance is similar to that of the Flickr dataset. “T→I” indicates “using texts to query images” and so on.

Forward Compatibility. The forward compatibility is measured by the effectiveness of retrieving old hash codes generated by old models using new hash codes generated by new models. As shown in Table 1, on the Flickr25k dataset, thanks to the design of our loss functions, ECMH achieves almost the same MAP (with a less than 1.1% decrease) as that of directly using the old model. Fine-tuning, however, suffers from a much larger up to 6.5% decrease. Surprisedly, on the MSCOCO dataset, our method achieves even better MAP (up to 2.4% increase) than the old model while Finetuning still has a significant up to 11.3% decrease. The first column in Figure 2 also presents that our method has similar PR curves as the old model and significantly outperforms Fine-tuning. The results reveal that our method can not only provide good forward computability of hash codes, but also utilize new data to further improve the performance on old tasks in some cases.

Current Performance on Old Tasks. In this evaluation, we use old data as query data and combine old and new data as the database. Table 1 shows that, on the whole, three jointtraining models using both old and new data have better MAP than ECMH and Fine-tuning using only new data. Among three joint-training models, joint-ECMH achieves significant better MAP than joint-DCMH and joint-SSAH in all cases. When extending models using only new data, ECMH outperforms Fine-tuning in all cases. In the worst case, i.e., Super-Category Extension on Flickr25k, Fine-Tuning has an 11.0% MAP decrease comparing with Joint-ECMH, while ECMH only has a 3.0% decrease and still achieves comparable performance to other joint training methods. The first column in Figure 2 further illustrates that in the worst case, ECMH has a much better PR curve than Fine-tuning. The result reveals that our method significantly relieves the catastrophic forgetting on old tasks and gets better old-task performance.

![](images/4763d543bf7d451d6bc4c36411393eca60ac0076020c2c7355e8bd10cd5bdea2.jpg)



(a) I T: retrieve old code.

![](images/5abc414cd09e30f280eeef522697b57df6d58fe16343df69a81f00b254b668e7.jpg)



(b) I T: old tasks.

![](images/ebf2ad92530928fb5b67ba348ed2d4687ed80493b547d4a86d4cc9c0e61fb5ba.jpg)



(c) I T: new tasks.

![](images/c0a0013f1b4dbde6e604b6d3454918adc2ccb2dac29dc55a0c4578b41a38b15b.jpg)



(d) I T: all tasks.

![](images/93eaafe594f56a7228536c851aa7e090077e2192b33bb6eacde1766a64bbfdc3.jpg)



(e) T I: retrieve old code.

![](images/b114d1bd43855e256b19a39ea6ef2d525eb8cc45a32c04a6873a1e85c9647f8c.jpg)



(f) T I: old tasks.

![](images/deb774aa46ab707535ba021650c3d074aa03875e83a60506596273d4ac5da739.jpg)



(g) T I: new tasks

![](images/194d0c7cbcbf1a70a02dbbf52f439ba7e47ce912688861203cb2d48a13c2dc9a.jpg)



(h) T I: all tasks.

![](images/599f4c669f0aaf94c8c36d9a75e37b216ce41cf6a770495f157743395801eebd.jpg)



(i) I T: retrieve old code.

![](images/e8757d7bfe89af4080161393b49c0f4ce0ad3fa45e85af56559a4abe03ed19d5.jpg)



(j) I→T: old tasks.

![](images/77e08671d748ee090b846442da9e05738cef522741319ecd2095a719a259d452.jpg)



(k) I→T: new tasks.

![](images/fbf1fcf6ad65d6d0cb4b9eae6287144917c9232f9afd40a05645bdff7bb31901.jpg)



(l) I T: all tasks.

![](images/01b885159672b220dfb218c12b6686cc4f0b0645bae51e309651504fdee1ab93.jpg)



(m) T→I: retrieve old code.

![](images/f14a050b98fcdbafe9765fe9037e2227f224ec36d80add437b8d640aed65fec3.jpg)



(n) T→I: old tasks.

![](images/951bc04cac2869f09b5a6e636d86a46eeaeb8c692c3984c51e93969885417560.jpg)



(o) T→I: new tasks.

![](images/bd010a4fc1194c2cac77894a647a6f5f6c140c68c9c16e13994f710b930aeb52.jpg)



(p) T→I: all tasks.   
Figure 2: Precision-recall curve of different methods on different tasks using the Flickr dataset. Figure (a) to Figure (h) are evaluated in the Sub-Category Extension case, and Figure (i) to Figure (p) are evaluated in the Super-Category Extension case. The code length is 64.

Current Performance on New Tasks. In this evaluation, we use new data as query data and combine new and old data as the database. The MAP results are in the third row (new tasks) in Table 1 and PR curves are shown in the third column in Figure 2. Since Fine-tuning update models only for new tasks, as expected, it achieves the best performance in many cases (see both Table 1 and Figure 2). ECMH has a comparable performance to Fine-tuning with an up to 2.7% decrease on the MSCOCO dataset. On the Flickr25k dataset, ECMH even has better performance on the image-query-text tasks.

The Overall Performance. Combining both new data and old data as the query data, we evaluate the overall performance of the new model. Both Table 1 and Figure 2 proves that, among three joint-training models, joint-ECMH achieves significant better MAP than joint-DCMH and joint-SSAH in all cases; and when using only new data, ECMH outperforms Fine-tuning in all cases. In the worst case (Super-Category Extension on Flickr25k), ECMH has a 6.1% MAP decrease than joint-ECMH, while Fine-tuning has a 13.5% MAP decrease. In Sub-Category Extension on MSCOCO, ECMH performs even better than all jointtraining methods. This result indicates that although our self-taught distillation slightly limits the performance on new tasks, it preserves the most crucial knowledge which renders it possible to get a model as good as a jointly trained one.

# Acknowledgments

This work is supported by the National Key R&D Program of China 2017YFB1003003, NSF China under Grants No. 61822209, 61751211, 61572281, 61520106007, and the Fundamental Research Funds for the Central Universities.

# References

[Baltrusaitis et al., 2018] Tadas Baltrusaitis, Chaitanya Ahuja, and Louis-Philippe Morency. Multimodal machine learning: A survey and taxonomy. IEEE Transactions on Pattern Analysis and Machine Intelligence, 41:423–443, 2018.   
[Bottou, 2010] Leon Bottou. Large-scale machine learn- ´ ing with stochastic gradient descent. In Yves Lechevallier and Gilbert Saporta, editors, Proceedings of COMP-STAT’2010, pages 177–186, Heidelberg, 2010. Physica-Verlag HD.   
[Bronstein et al., 2010] Michael M. Bronstein, Alexander M. Bronstein, Fabrice Michel, and Nikos Paragios. Data fusion through cross-modality metric learning using similarity-sensitive hashing. IEEE Computer Society Conference on Computer Vision and Pattern Recognition, pages 3594–3601, 2010.   
[Chen et al., 2018] Zhen-Duo Chen, Wan-Jin Yu, Chuan-Xiang Li, Liqiang Nie, and Xin-Shun Xu. Dual deep neural networks cross-modal hashing. In AAAI Conference on Artificial Intelligence, pages 274–281, 2018.   
[Cortes and Vapnik, 1995] Corinna Cortes and Vladimir Vapnik. Support-vector networks. Mach. Learn., 20(3):273–297, September 1995.   
[Guo et al., 2010] Gongde Guo, J Huang, and Lifei Chen. Knn model based incremental learning algorithm. Pattern Recognition and Artificial Intell., 23:701–707, 10 2010.   
[Hinton et al., 2015] Geoffrey Hinton, Oriol Vinyals, and Jeffrey Dean. Distilling the knowledge in a neural network. In arXiv: Machine Learning, 2015.   
[Huiskes and Lew, 2008] Mark J Huiskes and Michael S Lew. The mir flickr retrieval evaluation. In Proceedings of the 1st ACM international conference on Multimedia information retrieval, pages 39–43. ACM, 2008.   
[Iyyer et al., 2015] Mohit Iyyer, Varun Manjunatha, Jordan Boyd-Graber, and Hal Daume III. Deep unordered com- ´ position rivals syntactic methods for text classification. In Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 1681–1691. Association for Computational Linguistics, July 2015.   
[Jiang and Li, 2017] Q. Jiang and W. Li. Deep cross-modal hashing. In 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 3270–3278, July 2017.   
[Joshi and Kulkarni, 2012] Prachi Joshi and Parag Kulkarni. Incremental learning: Areas and methods-a survey. volume 2, page 43. Academy & Industry Research Collaboration Center (AIRCC), 2012.   
[Li and Hoiem, 2018] Zhizhong Li and Derek Hoiem. Learning without forgetting. pages 614–629, 2018.   
[Li et al., 2018] Chao Li, Cheng Deng, Ning Li, Wei Liu, Xinbo Gao, and Dacheng Tao. Self-supervised adversarial hashing networks for cross-modal retrieval. IEEE/CVF

Conference on Computer Vision and Pattern Recognition, pages 4242–4251, 2018.

[Lin et al., 2014] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar, and C. Lawrence Zitnick. Microsoft coco: Com- ´ mon objects in context. In David Fleet, Tomas Pajdla, Bernt Schiele, and Tinne Tuytelaars, editors, Computer Vision – ECCV 2014, pages 740–755, Cham, 2014. Springer International Publishing.

[Lin et al., 2015] K. Lin, H. Yang, J. Hsiao, and C. Chen. Deep learning of binary hash codes for fast image retrieval. In 2015 IEEE Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), pages 27–35, June 2015.

[Razavian et al., 2014] A. S. Razavian, H. Azizpour, J. Sullivan, and S. Carlsson. Cnn features off-the-shelf: An astounding baseline for recognition. In 2014 IEEE Conference on Computer Vision and Pattern Recognition Workshops, pages 512–519, June 2014.

[Shen et al., 2015] Fumin Shen, Chunhua Shen, Qinfeng Shi, Anton van den Hengel, Zhenmin Tang, and Heng Tao Shen. Hashing on nonlinear manifolds. IEEE Transactions on Image Processing, 24:1839–1851, 2015.

[Simonyan and Zisserman, 2015] K. Simonyan and A. Zisserman. Very deep convolutional networks for large-scale image recognition. In international conference on learning representations, 2015.

[Wang et al., 2016] Jun Wang, Wei Liu, Sanjiv Kumar, and Shih-Fu Chang. Learning to hash for indexing big data a survey. arXiv: Learning, 104:34–57, 2016.

[Wu et al., 2015] Botong Wu, Qiang Yang, Wei-Shi Zheng, Yizhou Wang, and Jingdong Wang. Quantized correlation hashing for fast cross-modal search. In Proceedings of the 24th International Conference on Artificial Intelligence, IJCAI’15, pages 3946–3952. AAAI Press, 2015.

[Wu et al., 2018] Gengshen Wu, Zijia Lin, Jungong Han, Li Liu, Guiguang Ding, Baochang Zhang, and Jialie Shen. Unsupervised deep hashing via binary latent factor models for large-scale cross-modal retrieval. In IJCAI, pages 2854–2860, 7 2018.

[Zhang et al., 2014] Peichao Zhang, Wei Zhang, Wu-Jun Li, and Minyi Guo. Supervised hashing with latent factor models. In Proceedings of the 37th international ACM SIGIR conference on Research & development in information retrieval, pages 173–182. ACM, 2014.

[Zhen and Yeung, 2012] Yi Zhen and Dit-Yan Yeung. A probabilistic model for multimodal hash function learning. In Proceedings of the 18th ACM SIGKDD international conference on Knowledge discovery and data mining, pages 940–948. ACM, 2012.