# A drug information embedding method based on graph convolution neural network

Xiaoyi Feng1, Shaoliang Peng14∗, Fei Li2∗, Ying Xu1, XiangXiang Zeng1, Dong-Qing Wei3 and Yunhao Liu1

1College of Computer Science and Electronic Engineering, Hunan University, China

2Department of Biotechnology, Beijing Institute of Radiation Medicine, China

3Laboratory of Microbial Metabolism,

School of Life Sciences and Biotechnology,

and Joint Laboratory of International Cooperation in Metabolic and Developmental Sciences,

Ministry of Education, Shanghai Jiao Tong University,China

4Peng Cheng Lab, Shenzhen 518000, China

{fengxiaoyi,slpeng,hnxy}@hnu.edu.cn,pittacus@qq.com,xzeng@foxmail.com,dqwei@sjtu.edu.cn,dai.yangfan.548@s.kyushu-u.ac.jp

Abstract—New drug development is an extremely timeconsuming and high-risk process. [1]It has been widely valued by the biomedical industry to fully explore the new uses of existing drugs and reorientate them. [2]How to find drug disease with potential therapeutic relationship from a large number of unproven relationship pairs is the research focus of drug reorientation. With the help of machine learning model, we can improve the enrichment degree of potential drug disease relationship pairs, and reduce the false positive rate of prediction. In the past few years, a series of graph based convolutional network models have been developed to calculate the information latent feature representation of nodes and links. Researchers at home and abroad have done a lot of research on network embedding technology based on biomedical data, and have achieved a series of important research results. Among them, the research methods used can be divided into two categories: one is the traditional machine learning algorithm based on artificial feature extraction, the other is the method based on deep learning. For example, kipf and welling [3]proposed a new graph convolution network (GCN) with parts of existing models, DeepDR [4] and DTINet [5] based on node characteristics and their connections, which can be used for node classification. Aiming at the problem of imbalance of drug information data samples, the invention provides a drug relocation method based on deep learning multi-source heterogeneous network. In order to avoid the limitations of traditional feature extraction methods, such as highly dependent on the experience and knowledge of medical staff, strong subjectivity, consuming a lot of time and energy to complete, and extracting high-quality features with distinguishing features often exists In this paper, with the help of graph convolution encoder model and variational auto encoder neural network, we can automatically learn the characteristics of multi-source and heterogeneous drug low-dimensional network, and complete the drug relocation of drug disease association prediction.

Index Terms—drug information network; graph convolution neural network; network embedding; link prediction.

# I. INTRODUCTION

The process of drug research and development includes drug target identification and validation, generation of emerging

∗ Shaoliang Peng and Fei Li are Corresponding authors.

compounds and lead compounds, optimization and characterization of lead compounds, drug preparation and delivery, pharmacokinetics test and drug disposal, determination of candidate drugs, bioanalysis test and clinical trial [2]. Most drug molecules show therapeutic effects by interacting with target proteins in vivo, such as enzymes, ion channels, nuclear receptors and G-protein-coupled receptors. Therefore, the identification of drug target interaction (DTI) has become an important prerequisite in drug discovery, drug reorientation, multi pharmacology, side effect research, drug resistance and other related fields [6]. In the existing pharmacological data, only a small number of drug target combinations have been verified by experiments. For example, there are only about 10000 pairs of approved drug target interactions in drugbank, the authoritative data set in pharmaceutical field [7]. In addition to the known drug target interactions stored in various databases, there are also a large number of compounds that have not been prepared, and they may also be developed into new drugs. For example, although compounds included in the PubChem dataset. There are more than 96 million kinds of human proteins [8]. There are more than 160000 kinds of human proteins in UniProt data set [8], but only a small part of the interaction relationship has been found.

In recent years, more and more people are interested in learning from the similarity of drugs. For example, an inductive matrix completion method is proposed to combine multiple data sources and help predict the unknown link association [6]. A comprehensive label propagation algorithm considering high-order similarity is proposed to infer clinical side effects from multiple sources. The results of these preliminary studies show that the combined representation of multi-source heterogeneous data usually has higher information content and robustness to noise. These methods can be classified into four categories: nearest neighbor method, random walk based method, unsupervised method and multi-core learning method [7].

Although in the past studies, we have found that deep learning can play a huge role in the field of drug discovery, but the research also shows that multiple biological data sources are not a single linear structure relationship, and different data sources will bring a lot of problems worth considering, which brings a lot of major challenges: 1) the characteristics and embedding of data from different data sources The correlation importance of fruit is different. For example, the important proportion of structural similarity of drugs has a greater impact on the network embedding results than the similarity of indications of drugs [8]; 2) the side effects caused by the interaction between different drugs are also quite complex and nonlinear structures in all types of characteristics; 3) Due to the expensive clinical trials and lengthy experimental time, drug information data are often lack of labels, the amount of data is small, and there are a lot of noise in the data. These problems also bring great challenges to the deep learning prediction of drug relocation; 4) because the correlation between drug information is nonlinear, and the model is quite complex, it also brings considerable feasibility to explain the model Big challenge. In order to solve the above problems, this paper takes the characteristic data of each drug as a view, and uses the multi view graph automatic encoder (GAE) to learn how to fuse the multi-source heterogeneous drug similarity problem [8]. In multiple drug information networks, the model architecture used in this paper is to use GCN to fuse multisource heterogeneous data network, and then combined with the serial form of variational self encoder to realize the fusion of nonlinear heterogeneous data [3]. The purpose is to predict the relocation of drugs and make learning more interpretable and adaptive. Through such embedding, we learn drug similarity representations and use them to predict outcomes (e.g., drug diseases, targeted interactions). The proposed model not only improves the prediction performance, but also has the following advantages.

• Because of the expensive clinical trials, the high cost of obtaining labeled experimental data and the scarcity of labeled data, we use unlabeled data for the forward training and learning process of the model. In this paper, we use the graph convolution neural network model, whose reconstruction loss can be regarded as a regularization term. We can display the structure information of the simulated drug information network through the reconstruction process. In this model, we can use unlabeled data for effective network embedding learning process, and use the obtained low dimensional effective data for downstream link prediction, drug relocation and other tasks.

• In this paper, we combine graph convolution model with existing models deepDR and DTINet to propose a new framework of drug information network association prediction model.   
Due to the rarity of drug information and the existence of noise, we can reconstruct the low dimensional effective embedding of data through GCN encoder even in the case of data missing or noise. The method proposed in this paper inherits the advantages of self coding. It can deal

with data noise well and has strong robustness for the extracted data. For example, in the case of drug target interaction prediction, sometimes the invisible interaction may not indicate that there is no interaction. The proposed method effectively reduces the negative impact of these ”positive unlabeled” samples.

In this paper, a large number of experiments on real data sets show that the method is better than other most advanced algorithms in most evaluation indexes, and has a large margin.

# II. RELATED WORK

Our work proposes effective solutions to the problems of multi-source heterogeneous data sets with small sample size, sparse data and multi-source fusion. As far as we know, the methods so far can be summarized as follows. The nearest neighbor algorithm based on neighborhood prediction [9]. However, this method itself has some insurmountable problems. As mentioned above, most of the existing methods do not consider the transitivity of similarity and can only use first-order similarity to construct neighborhood features.

Random Walk method: Inspired by word2vec [10] model in natural language processing, a method based on random walk [11] is developed to generate ”node sequence” through the random walk in the graph to learn the representation of nodes. Although the random walk method can deal with nonlinear data relationships, it can guarantee forward propagation learning in the absence of labeled data. However, because the random walk-based approach requires the use of a specific loss function model, it lacks flexibility in modeling for a specific problem [12].   
• The purpose of unsupervised method is to integrate multiple similar networks by constructing a fusion network based on an algorithm idea called iterative scaling. Feature ordering and feature variation are integrated into feature weights of weighted similarity fusion [13]. These unsupervised methods have good flexibility, but without any help from supervised learning, the reliability of the results calculated by the model is impossible to estimate.   
Multi-core learning (MKL) methods [14] have been further extended to network fusion tasks for processing multi-source heterogeneous data, but the existing methods are mostly limited to convex integrals.

# III. BACKGROUND

In the past few years, convolutional neural networks have developed rapidly, A considerable part of the development of graph convolution neural network has been applied to node representation, link prediction, embedded representation and other fields. For example, Kipf and Welling proposed a new graph convolutional network (GraphCNN) that learns node embeddings based on node features and their topological structure, which could be applied in node classification. Concretely, given an undirected graph with nodes feature X and adjacency matrix A, a multi-layer neural network is constructed on the graph with the following layer-wise propagation rule:

$$
H ^ {(l + 1)} = f \left(\widetilde {D} ^ {- \frac {1}{2}} \widetilde {A} \widetilde {D} ^ {- \frac {1}{2}} H ^ {(l)} W ^ {(l)}\right) \tag {1}
$$

where $\stackrel { \sim } { A } = A + I _ { N }$ is the adjacency matrix with added selfconnections, $D$ is a diagonal matrix such that $D _ { i i } = \Sigma _ { j } \tilde { A } _ { i j } ,$ $W ^ { ( l ) }$ is a layer-specific parameter matrix, $H ^ { ( l ) }$ is the node representation in the $l ^ { t h }$ layer, and f is an activation function (e.g. ReLU or sigmoid). Later, Schlichtkrull and Kipf extended GraphCNN and proposed a graph auto-encoder (GAE) using GraphCNN for both node classification and link prediction tasks. However, their model only reconstructs the edges, and cannot work on unseen data or link prediction. In the next experiment, we will perform further extension in terms of reconstructing both links and node low dimension embeddings representation and allowing for inductive link prediction.

# IV. METHOD

# A. Problem Definition

In this paper, we consider each type of drug feature as a view. For feature $\mathrm { ~ u ~ } \in \ \{ 1 , \cdots , \mathrm { T } \}$ , we construct a graph by modeling each drug as a node and the similarity between two nodes as an edge. We denote node feature embeddings as $Z ^ { ( u ) }$ and use similarity matrix $A ^ { ( u ) }$ to represent the pair-wise similarity between drugs on that view. Given T different views, the task of multi-view similarity integration is to derive an integrated node embedding Z and similarity matrix $A \in R ^ { n }$ ∗n across all views [8].

# B. Graph-based Methods

For each feature u, we set $\widetilde { A } ^ { ( u ) } = A ^ { ( u ) } + I _ { N }$ , and degree matrix $D _ { i i } ^ { ( u ) } = \Sigma _ { i } \tilde { A } _ { i i } ^ { ( u ) }$ .

We use a GraphCNN to encode the nodes in our graph:

$$
Z = f (X, \widehat {A}) = \sigma (\widehat {A} X W) \tag {2}
$$

After that, we decode the embedding back to the original feature space:

$$
X ^ {\prime} = f (Z, \widehat {A}) = \sigma (\widehat {A} Z W) \tag {3}
$$

For loss function, we use equation as blow:

$$
L = \sum \left\| X - X ^ {\prime} \right\| ^ {2} \tag {4}
$$

# V. BASED GCN ARCHITECTURE

# A. Model Architecture

To exploit adding information in the similarity graph, we use GCN to extract mutual relation between entities. Given the $K _ { u }$ dimension feature $p _ { i }$ of drug $u _ { i }$ ,the features $\{ p _ { i 1 } , p _ { i 2 } \ldots , p _ { i k } \}$ of $u _ { i } \mathbf { s }$ connected drug $\{ u _ { i 1 } , u _ { i 2 } \ldots , u _ { i k } \}$ and the corresponding normalized similarity weight $4 ( u ) _ { i , i 1 } , A ( u ) _ { i , i 2 } , . . . , A ( u ) _ { i , i k }$ , we could get the d dimension embedding $\tilde { p } _ { i }$ of drug $u _ { i }$ as:

$$
\tilde {p} _ {i} = \sigma \left(\widetilde {A} (u) _ {i, p} p _ {i} + \sum_ {j = 1} ^ {k} \widetilde {A} (u) _ {i, i j} p _ {i j}\right) W _ {(u)} \tag {5}
$$

![](images/de888b585ac0f03ab5a2ca2ab1adec7d1bf9a545d080e33389658f671271bf2a.jpg)



Fig. 1: the model architecture of GCN. The input data are adjacency matrix and characteristic matrix of biomedical information network. By calculating hierarchy, we could get the Low dimension embedded representation vector. And the final representation vector is obtained by concatenate operation.

where $W _ { ( u ) }$ is the learned parameter to project the combined features into new space and σ is the non-linear activation function, such as Relu or Sigmoid. Similarly, given $K _ { v }$ dimension feature $q _ { i }$ of disease or protein vi, we could get the embedding $q _ { i }$ for disease or protein $v _ { i }$ as:

$$
\tilde {q} _ {j} = \sigma \left(\widetilde {A} (v) _ {j, j} q _ {j} + \sum_ {i = 1} ^ {k} \widetilde {A} (v) _ {j, j i} q _ {j i}\right) W _ {(v)} \tag {6}
$$

where $\mathrm { W ( v ) }$ is the learned parameter for disease or proteins GCN component. Given the drug features matrix $P$ and disease or protein features matrix $Q ,$ we could get their embeddings from GCN as:

$$
\widetilde {P} = \sigma (\widetilde {A} (u) p W _ {(u)})
$$

$$
\widetilde {Q} = \sigma (\widetilde {A} (v) Q W _ {(v)}) \tag {7}
$$

Where $\widetilde { P }$ and $\widetilde { Q }$ are the new representation of diseases or protein and drug respectively. Once we get the embeddings, we could get the preference matrix S as:

$$
S = \operatorname{clip} \left(\widetilde {P} \widetilde {Q} ^ {T}\right) \tag {8}
$$

where $c l i p ( \mathbf { x } )$ is the clip function to make the value of the elements stay in [ 0, 1]. the $i _ { t h }$ row in $S$ represents the preference score of disease $u _ { i }$ . In reality, we could test only the top-k drugs for a specific target, which would save a lot of time. And new verified associations could also be added as labels in our model to improve the overall accuracy.

# B. Based GCN Model Validation

1) Drug disease prediction model based on GCN: In this part, we will introduce in detail how to verify the effectiveness of representation by learning low dimensional vector representation learned from GCN model. Mainly, we will focus on two parts. We will explain the validity of GCN based drug repositioning model (DeepDR) [4] and GCN based drug protein link prediction model (DTINet) [1]. DeepDR is a novel deep learning framework to uncover the potential associations between drugs and diseases. Theoretically, deepDR is superior to the existing drug repositioning methods as we adopt a multi-modal deep autoencoder (MDA) [15] to capture complex topological patterns across different data sources. Further, deepDR is able to preserve the non-linear network structure by applying multiple layers of non-linear functions. It also complements the sparse ratings with drug features, as feeding side information into the same VAE [16] increases the number of samples for training, which also acts like a pre-training step. Specifically, drugCdisease associations and drug features are different sources of information, both are information with drugs, so they can be encoded and decoded collectively through the same inference network and generation network. On the basis of DeepDR, we take the data in the data preprocessing stage as the input data of GCN model. Through the training of GCN model, we can get the low dimensional representation of drug information. In DeepDR, it trains the low-dimensional embedding representation of drug information through autoencoder, we replace it with GCN model, use the low-dimensional vector representation obtained as the input data of DeepDR, in cVAE part, through the 5 fold cross validation, use AUC and AUPR as the performance evaluation index of the model, compared the results with Deep-DR model, through experimental verification, the embedding learned through GCN model is better than the original model.

![](images/07f227b2d65d4597cb1bec7d10accc755b3235a686985daab7b6702bb76202d0.jpg)



Fig. 2: GCN model integrates the preprocess stage dataset by DeepDR to obtain the low dimension vector representation of biomedical information network, low-dimensional features are then extracted from the middle layer of GCN model. Then we use a collective variational autoencoder (cVAE) by DeepDR to predict potential associations between drugs and diseases. Drug features and known (clinically reported or approved) drugCdisease interactions are encoded and decoded collectively by the same inference network and generation network.

2) Drug protein prediction model based on GCN: In this part, we will introduce a model called DTINet [1], which is used to predict drug-target link associations. On the basis of this model, we would verify the effectiveness of graph convolution network by changing the structure of dense layer in DTINet into GCN layer. DTINet is a new nonlinear end-

![](images/b8811eb23d328f326bc4a2a0e7a56f91e6d11cb97ba74352f40f2caff0bd850c.jpg)



Fig. 3: GCN model for DTINet dataset. The GCN model is used to calculate the low dimensional vector representation of biomedical information network, and the matrix operation is combined with the ground truth for comparison training.

to-end learning model, which integrates diverse information from heterogeneous network data and automatically learns topology-preserving representations of drugs and targets to facilitate DTI prediction. For drug individual networks and protein individual networks, we apply GCN model for extracting the vector representations of low dimension for biomedical nodes. By getting drug and protein embedding representations, we apply projection matrix for unlabeled drug-target link associations combined with the ground truth data.

# VI. EXPERIMENTS

In this segment, we will demonstrate all the details of the experiment for settings and results. Otherwise, we will display the outcomes of experiments for the evaluation of our method and other baselines.

# A. Dataset and Features

1) silico drug repositioning data resource of DeepDR: In our first experiment, we use the database of DeepDR, which is open source data from two commonly used databases: DrugBank [17] and repoDB [18]. Chemical name, generic name or commercial name of each drug were standardized by Medical Subject Headings (MeSH) and Unified Medical Language System (UMLS) vocabularies [19] and further converted to DrugBank ID from the DrugBank database (v4.3). Generic name for each disease was annotated by MeSH. In addition, 6677 clinically reported drugCdisease pairs connecting 1519 drugs and 1229 diseases were further collected for building predictive deep learning models. For the external validation set, we assembled the most recent drugCdisease associations from the ClinicalTrials.gov database (https://clinicaltrials.gov/), by excluding existing pairs in the abovementioned DrugBank [17] and repoDB [18] databases.

2) DTI database: We adopted the datasets that were curated in our previous study, which included six individual drug/protein related networks: drugCprotein interaction and drugCdrug interaction networks [interactions were extracted from Drugbank Version 3.0 [20]], the proteinCprotein interaction network [interactions were extracted from the HPRD database Release 9 [21]], drugCdisease association and proteinCdisease association networks [associations were extracted from the Comparative Toxicogenomics Database [22]] and the drug-side-effect association network [associations were extracted from the SIDER database Version 2 [23]].

TABLE I: dataset of DeepDR. 

<table><tr><td>Node</td><td>Count</td><td>Edge</td><td>Count</td></tr><tr><td>Drug</td><td>1,519</td><td>Drug-Protein</td><td>6,744</td></tr><tr><td>Protein</td><td>1,025</td><td>Drug-Drug</td><td>290,836</td></tr><tr><td>Disease</td><td>1,519</td><td>Drug-Disease</td><td>6,677</td></tr><tr><td>Side-effect</td><td>12,904</td><td>Drug-Side-effect</td><td>382,041</td></tr><tr><td>Total</td><td>16,677</td><td>Total</td><td>686,298</td></tr></table>

TABLE II: dataset of DTINet. 

<table><tr><td>Node</td><td>Count</td><td>Edge</td><td>Count</td></tr><tr><td>Drug</td><td>708</td><td>Drug-Protein</td><td>1,923</td></tr><tr><td>Protein</td><td>1,512</td><td>Drug-Drug</td><td>10,036</td></tr><tr><td>Disease</td><td>5,603</td><td>Drug-Disease</td><td>199,214</td></tr><tr><td>Side-effect</td><td>4,192</td><td>Drug-Side-effect</td><td>80,164</td></tr><tr><td>-</td><td>-</td><td>Protein-Protein</td><td>7,363</td></tr><tr><td>-</td><td>-</td><td>Protein-Protein</td><td>1,596,745</td></tr><tr><td>Total</td><td>12,015</td><td>Total</td><td>1,895,445</td></tr></table>

# B. Experiment Setting

1) Proposed Model: We implement the proposed model with Pytorch and trained using Adam with learning rate 0.001. For GCN model, we have two layers of GCN and for the units of each layer, which are namely 500,100, and 500. We apply 5-fold cross-validation for our experiment.

2) Adjustment of super parameters: for parameters α and $\beta ,$ we tested the performance of their combination tests, the numbers we choose for experiment are namely (1,5,10,15,20) for α, and (0.1,0.3,0.5,3,6,9) for β. And the units of the model we choose (1000,700,500). After testing the result, we found that it performed better when α, β and layer are namely 20, 0.5, 500.

# C. Baselines

In addition, we implemented the following baselines for comparison;

1) DTINet: The DTINet has effective performance results in processing multi-source heterogeneous network data. It can learn the low-dimensional network representation of characteristic data, and then apply induction matrix [24]to make prediction.

2) KBMF: The nuclearized Bayesian matrix decomposition method [25] can utilize multiple side information sources and can be widely used in the task of recommendation system.

3) RF: Random forest [26] represents a collection of decision trees, which are grown from bootstrap samples of the training data without pruning, and make predictions based on majority votes of the ensemble trees.

4) SVM: Support Vector Machine (SVM) [27]is a class of supervised learning that classifies data in binary manner, generalized linear classifier. Its decision boundary is maximummargin hyperplane that solves the learning sample.

5) RWR: Random walk with restart [28], a network diffusion algorithm, which is useful in measuring the proximity between two nodes of a network.

6) Katz: The Katz measure is a graph-based method for finding node similarity to a given node by computing how many different path lengths exist between the pair.

# D. Performance Evaluation

In this part, we show the result of our model compared with the baseline methods. The evaluation criterions we choose are AUC and AUPR. The area under the receiver operating characteristic curve (AUROC) and the area under the precisionCrecall curve (AUPR) were utilized to evaluate the overall performance. In our experiment, we found that for GCN model, after training, we gain the optimal embedding matrix for input data of cVAE. During the 5-fold crossvalidation, we randomly selected a subset of 20% of the clinically reported drugCdisease pairs and a matching number of randomly sampled unknown pairs as the test set, and the remaining 80% clinically reported drugCdisease pairs with same number of randomly sampled unknown pairs were used to train the model. For experiment result, we found that our model perform better that other baselines, we found that our model showed high accuracy (AUROC 0.924 and AUPR 0.933) in 5-fold cross validation, outperforming with the DeepDR(AUROC 0.908 and AUPR 0.923) and the stateof-the-art methods: DTINet (AUROC 0.862 and AUPR 0.892), KBMF (AUROC 0.791 and AUPR 0.826), RF (AUROC 0.783 and AUPR 0.805), SVM (AUROC 0.771 and AUPR 0.778), RWR (AUROC 0.708 and AUPR 0.734) and Katz (AUROC 0.724 and AUPR 0.741).

# VII. CONCLUSION

In this study, we discuss a deep learning framework combined with GCN. We found that GCN model could play an effective role in potential link prediction and network embedding. For database from DeepDR, we use the pretraining drug features as the input data of GCN, due to the DDI network, we would calculate the topological structure of drug information through GCN model, by forward and reverse calculation, we gain the optimized model structure to catch the low dimensional network representation. It is proved that the low dimensional network representation of drug, calculated by GCN, could perform better than existing models in potential drug-disease prediction. Also, we did experiments to confirm that GCN could keep effectiveness in DTI database for drug and target prediction. With the development of society, the real-world network will become more complex [29]. How to effectively gather different types of information to assist the learning of representation vector, make it more reasoning and distinctive, and reduce the complexity of the whole model is still an open problem to be studied in the future.

![](images/5f64e9763a3ed9947c49bce8780b4a70f6e25ddf765afa67db263b742b3d3263.jpg)



(a) AUROC   
![](images/9886bc03d0180658e4bf1234b4f9a2f19c73a59a0be956c15bccf342636b49ef.jpg)



(b) AUPR   
Fig. 4: Experiment on DeepDR dataset. The experiments show that the low dimensional vector representation obtained by GCN can improve AUC and AUPR as DeepDR. Compared with other baseline models, the results show that GCN could perform better.

# ACKNOWLEDGMENT

This work was supported by National Key R&D Program of China 2017YFB0202602, 2018YFC0910405, 2017YFC1311003, 2016YFC1302500, 2016YFB0200400, 2017YFB0202104; NSFC Grants U19A2067, 61772543, U1435222, 61625202, 61272056; The Funds of Peng Cheng Lab, State Key Laboratory of Chemo/Biosensing and Chemometrics; the Fundamental Research Funds for the Central Universities, and Guangdong Provincial Department of Science and Technology under grant No. 2016B090918122.

# REFERENCES

[1] C. Peng, W. Xiao, P. Jian, and Z. Wenwu, “A survey on network embedding,” IEEE Transactions on Knowledge and Data Engineering, vol. PP, no. 99, pp. 1–1, 2017.   
[2] B. krlj, J. Kralj, J. Konc, M. Robnik-ikonja, and N. Lavra, “Deep node ranking: an algorithm for structural network embedding and end-to-end classification,” 2019.   
[3] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” 2016.   
[4] X. Zeng, S. Zhu, X. Liu, Y. Zhou, and F. Cheng, “deepdr: a networkbased deep learning approach to in silico drug repositioning,” Bioinformatics, vol. 35, no. 24, pp. 5191–5198, 2019.

[5] W. Fangping, H. Lixiang, X. An, J. Tao, and Z. Jianyang, “Neodti: Neural integration of neighbor information from a heterogeneous network for discovering new drug-target interactions,” Bioinformatics, 2018.   
[6] J. Zhou, G. Cui, Z. Zhang, C. Yang, Z. Liu, L. Wang, C. Li, and M. Sun, “Graph neural networks: A review of methods and applications,” 2018.   
[7] P. Goyal and E. Ferrara, “Graph embedding techniques, applications, and performance: A survey,” Knowledge Based Systems, vol. 151, no. JUL.1, pp. 78–94, 2017.   
[8] T. Ma, C. Xiao, J. Zhou, and F. Wang, “Drug similarity integration through attentive multi-view graph auto-encoders,” 2018.   
[9] M. Niepert, M. Ahmed, and K. Kutzkov, “Learning convolutional neural networks for graphs,” 2016.   
[10] T. Mikolov, K. Chen, G. Corrado, and J. Dean, “Efficient estimation of word representations in vector space,” Computer ence, 2013.   
[11] S. Lee, S. Song, M. Kahng, D. Lee, and S. Lee, “Random walk based entity ranking on graph for multidimensional recommendation,” pp. 93– 100, 2011.   
[12] W. L. Hamilton, R. Ying, and J. Leskovec, “Representation learning on graphs: Methods and applications,” 2017.   
[13] B. Hu, Y. Fang, and C. Shi, “Adversarial learning on heterogeneous information networks,” in The 25th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD ’19), 2019.   
[14] M. Gonen and E. Alpaydin, “Multiple kernel learning algorithms,” Journal of Machine Learning Research, vol. 12, pp. 2211–2268, 2011.   
[15] G. Vladimir, B. Meet, and B. Richard, “deepnf: Deep network fusion for protein function prediction,” Bioinformatics, 2018.   
[16] Y. Chen and M. De Rijke, “A collective variational autoencoder for top-n recommendation with side information,” pp. 3–9, 2018.   
[17] D. S. Wishart, Y. D. Feunang, A. C. Guo, E. J. Lo, A. Marcu, J. R. Grant, T. Sajed, D. Johnson, C. Li, Z. Sayeeda et al., “Drugbank 5.0: a major update to the drugbank database for 2018,” Nucleic Acids Research, vol. 46, 2018.   
[18] A. S. Brown and C. J. Patel, “A standard database for drug repositioning,” Scientific Data, vol. 4, no. 1, pp. 170 029–170 029, 2017.   
[19] H. Wang, F. Azuaje, O. Bodenreider, and J. Dopazo, “Gene expression correlation and gene ontology-based similarity: an assessment of quantitative relationships,” Proceedings of the ... IEEE Symposium on Computational Intelligence in Bioinformatics and Computational Biology. IEEE Symposium on Computational Intelligence in Bioinformatics and Computational Biology, vol. 2004, p. 25, 2004.   
[20] C. Knox, V. Law, T. Jewison, P. Liu, S. Ly, A. Frolkis, A. Pon, K. Banco, C. Mak, V. Neveu et al., “Drugbank 3.0: a comprehensive resource for omics research on drugs,” Nucleic Acids Research, vol. 39, pp. 1035– 1041, 2011.   
[21] T. S. Keshava Prasad, R. Goel, K. Kandasamy, S. Keerthikumar, S. Kumar, S. Mathivanan, D. Telikicherla, R. Raju, B. Shafreen, and A. Venugopal, “Human protein reference database2009 update,” Nuclc Acids Research, vol. 37, no. Database, p. D767, 2009.   
[22] A. P. Davis, C. J. Grondin, K. Lennonhopkins, C. Saracenirichards, D. Sciaky, B. L. King, T. C. Wiegers, and C. J. Mattingly, “The comparative toxicogenomics database’s 10th year anniversary: update 2015,” Nucleic Acids Research, vol. 43, pp. 914–920, 2015.   
[23] M. Kuhn, I. Letunic, L. J. Jensen, and P. Bork, “The sider database of drugs and side effects,” Nucleic Acids Research, vol. 44, pp. 1075–1079, 2016.   
[24] Natarajan, Nagarajan, Dhillon, Inderjit, and S., “Inductive matrix completion for predicting genecdisease associations.” Bioinformatics, 2014.   
[25] M. Gonen and S. Kaski, “Kernelized bayesian matrix factorization,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 36, no. 10, pp. 2047–2060, 2014.   
[26] T. K. Ho, “The random subspace method for constructing decision forests,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 20, no. 8, pp. 832–844, 1998.   
[27] C. Cortes and V. Vapnik, “Support-vector networks,” Machine Learning, vol. 20, no. 3, pp. 273–297, 1995.   
[28] H. Tong, C. Faloutsos, and J. Pan, “Fast random walk with restart and its applications,” pp. 613–622, 2006.   
[29] M. Henaff, J. Bruna, and Y. Lecun, “Deep convolutional networks on graph-structured data,” Computer ence, 2015.