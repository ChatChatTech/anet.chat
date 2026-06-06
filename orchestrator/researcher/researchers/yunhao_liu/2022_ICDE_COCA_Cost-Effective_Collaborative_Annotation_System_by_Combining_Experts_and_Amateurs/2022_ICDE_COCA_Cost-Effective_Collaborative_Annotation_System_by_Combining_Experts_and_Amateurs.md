# COCA: Cost-Effective Collaborative Annotation System by Combining Experts and Amateurs

Jiayu Lei, Zheng Zhang, Lan Zhang∗, Xiang-Yang Li

School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

{misslei,zzhang96}@mail.ustc.edu.cn, zhanglan03@gmail.com, xiangyangli@ustc.edu.cn

Abstract—Data annotation has been a key boost for the artificial intelligence. However, difficult tasks such as fine-grained classification need lots of labeled data to train a feasible model. On the one hand, using people who have expert knowledge on the datasets to annotate all data can be costly. On the other hand, amateurs are cheaper but not able to give precise labels. Related works like machine labeling need labeled data to start up. Crowd-Model labeling can hardly solve complex tasks like fine-grained classification. Lately, combining domain experts and cost-effective crowd to solve complex tasks has become an area of increasing interest in research and industry. However, most works rarely investigate the cost gap between experts and amateurs and see how it influences the final annotation cost. In this paper, we combine both experts and amateurs to build a cost-effective data annotation system called COCA. COCA annotates the target dataset from scratch and save costs by our annotation assignment strategy. Extensive evaluations show that when reaching the same precision, COCA can reach a lower cost than SOTA automatic labeling models when the ratio of expert price to amateur price is above a certain value.

Index Terms—Crowdsourcing, Data mining.

# I. INTRODUCTION

Data annotation is an essential step in data management process. For example, data labels can be used to construct indexes and thus enable data search and retrieval. Large-scale labeled data is a key boost for artificial intelligence and thus promote data mining. Therefore, cost-effective high-quality data annotation can be a practical building block of data management systems.

Existing annotation methods like machine labeling is effective when dealing with large-scale dataset which makes it a crucial component in an annotation system. However, it can’t annotate a dataset from scratch because it needs a labeled data or human-provided side information for training [1]. In the last few years, researchers find crowd-model collaboration an effective solution for large-scale data collection tasks [2]. For example, several works [3], [4], [5] use crowd-model combination to solve entity resolution tasks. But when it comes to complex tasks like fine-grained annotation, workers without domain-specific knowledge will be incompetent. Thus, several works [6], [7] investigate combining domain experts and regular crowd to solve complex tasks. While they consider the trade-off between accuracy and cost, they rarely consider the scenario where crowd can’t give a precise category guidance. In this paper, we consider the crowd as amateurs who can’t ∗Lan Zhang is the corresponding author.

give precise labels, and further explore the opportunities of combining experts, amateurs and machine learning models to fulfil a cost-effective annotation on complicated tasks like finegrained multi-classification.

Given the task of labeling a raw dataset from scratch, we have experts who have domain knowledge and can annotate precise category labels and amateurs who can only give annotations such as pairwise comparison. We can reasonably assume that experts are expensive and rare while amateurs are cheap and numerous [8]. Although all data should be given labels, it’s not necessary for them to be all given by experts. Our idea is that experts only label necessary data such as the first data sample of each category, and for each of the rest data, amateurs can label it just through a few pairwise comparisons. A machine learning model will assign the specific annotation tasks for experts and amateurs to assure the procedure go on smoothly. Through the collaboration of those three agents, finally each data of the raw dataset will be labeled. Therefore, we propose COCA, a cost-effective annotation system by combining experts, amateurs and machine learning models.

For a dataset which has n data and c categories. we have two cases:

• Base Case: All data are labeled by experts;   
• Best Case: Only the first data sample of each category is labeled by experts, all the other data are correctly labeled by one time pairwise comparison by amateurs.

We quantify the optimization space of our idea on CUB-200-2011 dataset in Fig. 1. The ratio of single time expert annotation price and single time amateur annotation price is k. We set single time expert annotation price as 1, therefore the price for single time amateur annotation price is 1/k. So we can calculate the total labeling cost for each case: $C _ { b a s e } = n ,$ $\begin{array} { r } { C _ { b e s t } = c + \frac { n - c } { k } } \end{array}$ . For CUB-200-2011, n = 11788, c = 200. We can see the labeling cost as a function of k for both cases in Fig 1. As k grows, the optimization space can be considerable. Compared to base case, best case can save about 50% cost when k = 2 and save around 90% cost as k increases to 10.

The cost saving ratio this idea can reach is considerable. The core challenges of building such a system are as follows:

• We start the annotation from scratch and don’t have any prior knowledge, i.e. we don’t have any labeled samples or pre-trained models on the target dataset. So at first, we don’t have any reference to decide the annotation tasks assigned for experts and amateurs;

![](images/68ae25350c6d573b4c8d44264f7e15983830834f1204c0b8c5762abea9dc0ee9.jpg)



Fig. 1. Base case and best case comparison

• We want experts to label the first data sample of each category, but since the lack of prior knowledge, it’s hard to know which data belonging to the new category;   
• It’s difficult to always assign same-category pairs to amateurs. Furthermore, amateurs can also make mistakes during annotation;   
• Since our machine learning models have no prior knowledge, we have to adjust the annotation assignment process according to its performance.

To solve those challenges, we make our collaborative annotation an iterative process so that we can gain labeled data through early annotation batches and make use of them in the later annotation batches. Furthermore, we adopt metric learning model [9] to play the part of machine learning model because it can minimize the intra-class distance and maximize the inter-class distance which can help pick similar data points for amateurs. We use a filtering method to help experts discover new categories and a category ranking strategy with an uncertainty-based data selection method to choose specific samples for experts and amateurs to annotate.

The main contributions of our work are as followings:

• We propose a new cost-effective annotation system framework which annotates the target dataset from scratch by combining experts, amateurs and machine learning models;   
• We design COCA to implement this framework which includes iterative annotation processes and annotation assignment strategy to coordinate three agents and save annotation costs;   
• Extensive evaluations show that when reaching the same precision, COCA can reach a lower cost than SOTA automatic labeling models when the ratio of expert price to amateur price is above a certain value.

This paper is structured as follows: After presenting related work, we define our problem and introduce our core ideas and workflow. Then, we describe our system design in details, followed by the experimental evaluation. We conclude with future research directions and final remarks.

# II. RELATED WORK

# A. Machine Labeling

Due to the time and effort of manual annotation, automatic image annotation (AIA) has been proposed since the late 1990s [1]. The most recent decade has witnessed the significant development of deep learning techniques, which enables deep features to solve AIA tasks. The deep-learning based AIA can be summarized in two approaches. First, robust visual features are generated by using convolution neural network (CNN) for image annotation [10]. Second, side information (such as semantic label relationships) is fully extracted through deep learning techniques for AIA [11]. For example, Mu Yuan et al. use multi model inference to give rich labels for datasets. And they further use deep reinforcement learning to select a subset of the models to execute without comprimising the recall rate of available labels. [12], [13].

Machine labeling does have much smaller computation costs compared to heavy labor. However, in order to achieve high accuracy on the target dataset, it needs large-scale high-quality labeled data from the same field for training. Thus, existing machine labeling methods cannot annotate a dataset of a new field from scratch. In this case, many seek to harness the human cognitive ability to efficiently address these issues [8].

# B. Crowd-Model Labeling

In the last few years, crowdsourcing has emerged as an effective solution for large-scale data collection tasks [2]. For example, Deng et al. design an interactive game to make crowd generate distinguishable templates to classify images [14]. And Drutsa et al. propose a general pipeline to efficiently collect crowd answers through public crowdsourcing marketplaces, which involves task decomposition, instruction and interface design, quality control, aggregation and pricing [15].

During the crowd-model labeling process, the cost control is critical, since the crowd workers can reach a very large scale. Tu et al. group the worker according to their annotation behaviors and selects samples for suitable groups to reduce the annotation cost [16]. Yang et al. use crowd to generate labeling rules which have a high coverage and accuracy on binary classification tasks like entity resolution and relation extraction [3]. Moreover, several works [4], [5] also investigate using crowd to cost-effectively solve entity resolution. Chai et al. define a partial order to propagate answers and a grouping technique to reduce the question amount [4]. Huang et al. use entity relationships to propagate labels and thus save costs [5].

Using crowd workers’ guidance, crowd-model labeling is a promising way to achieve an effective trade-off between the labeling accuracy and cost. But cheap regular crowd cannot handle complex tasks which require domain-specific knowledge. Scenarios like fine-grained classification challenge the existing crowd-model labeling approaches [17].

# C. Expert-Involved Labeling

Since human experts can provide highly accurate labeling guidance, some works explore annotation approaches that combine machine learning models and human experts. Beaugnon et al. use a hierarchical active learning method to help experts label intrusion detection datasets with a reduced workload [18]. Dai et al. propose a gradient-guided sampling method to guide the selection of tumor images for experts to annotate [19]. Li et al. propose a hybrid annotation framework. It firstly constructs taxonomy, and then gathers experts who have abundant time to label until no new knowledge can be obtained and the models performance reaches its peak [20].

Furthermore, Correia et al. mention the increasing need for solving complex tasks with the integration of human experts, crowd workers, and ML models [21]. Lee et al. use crowd to filter jobs on large number of trivial questions first and leave more difficult jobs for experts to relabel [22]. Similarly, Kutlu et al. leverage crowd to solve information retrieval problem by making experts annotate highly-ranked or lowest agreement documents and let crowd annotate the rest [6]. Mendez et al. design a forward loop (machine-crowdexperts) to increase label quality and model performance and a backward loop (machine-expert-crowd) to increase user engagement [23]. Nguyen et al. solve a citation screening problem. They fix the cost ratio between experts and amateurs as 100 and always query the lower cost labeler first and then pick the crowd-labeled items to ask experts [24]. Callaghan et al. design a human-machine framework for binary heart sound classification by incorporating answers from experts and crowd into a final classification [7]. Li et al. apply reinforcement learning on data labelling workflow and reach high accuracy on binary classification tasks [25]. Krivosheev et al. efficiently combine crowd and machine classifiers to screen items which satisfy a set of predicates. It firstly select classifiers which is better than random selection and then use them to set a prior probability for whether a filter applies to an item. In this way, they select the most promising pairs for crowd to get the decision cheaply and confidently and leave the difficult pairs for experts to annotate [26].

Those work either use crowd directly or combine regular crowd and experts to solve data collection tasks and save annotation costs, which, however, need crowd workers to provide precise category guidance (e.g., whether the queried sample belongs to a specific category or to classify the queried sample into a specific category). In this work, we consider scenarios like fine-grained image classification, where amateurs cannot provide such precise category guidance. Therefore, existing expert-involved labeling solutions cannot be applied straightly. Our work explores the opportunities of combining experts, amateurs and machine learning models to fulfil a cost-effective annotation on complicated tasks like fine-grained multi-classification.

# III. OVERVIEW

We consider the ability and cost differences of experts and amateurs to design a cost-effective annotation system through expert-crowd-machine collaboration.

# A. Definition

Let D denote the raw dataset, $D _ { u } ^ { t }$ and $D _ { l } ^ { t }$ denote the unlabeled and labeled dataset after t-batch annotation. Given $D \ = \ D _ { u } ^ { 0 }$ , Our goal is to combine experts, amateurs and machine learning models to produce $| D | = | D _ { l } ^ { t } |$ after t batch annotation and minimize annotation costs. The characteristics of three agents are listed as follows:

• Expert: The expert represents a person who has professional knowledge on D. For a given annotation task, experts can give precise labels. Given a data sample x, let $l _ { e } ( x )$ denote the expert annotation on x;

• Amateur: Amateurs are regular crowd in crowdsourcing platforms, and they often do not have professional knowledge on D. For example, crowdsourcing platforms such as Amazon Mechanical Turk and Datatang will hire part-time students or other people with spare time to do the labeling work. Although they can’t give a precise label, they have the cognitive ability to tell the differences of different samples or similarities of similar samples. Given data pair $( x , y )$ , let $l _ { a } ( x , y )$ denote the amateur annotation on pair $( x , y ) . \ l _ { a } ( x , y ) = 1$ if amateurs think data x and data y belong to the same category, otherwise $l _ { a } ( x , y ) = 0 ;$

• Machine Learning Model: Machine learning models have the ability of dealing with large-scale dataset. It can extract deep features to represent each data sample and perform metric learning and classification on the basis of those feature representations. In online scenarios such as online annotation, machine learning models can update their knowledge as the data comes, and thus improve its performance. But machine learning models need prelabeled data to start up, so it can’t work independently in an annotation system. The cost of computing resources it takes can be ignored compared to the high labor costs.

Table I shows symbol notations used in this paper.

# B. Core Ideas

The amateurs’ labeling form is to compare the similarity of two samples. It would be inefficient to randomly pick data pairs to compare. In order to explore the possibility of machine learning models picking similar data pairs for amateurs, we did a preliminary experiment. Considering that classification through pair comparison is similar to the KNN classification process, we use KNeighborsClassifier in sklearn.neighbors as our classification model and 10% data of CUB-200-2011 dataset as training data to do this experiment. For each data point, we record α $( 1 \leq \alpha \leq 1 0 )$ nearest neighbors generated by the classifier. We record their categories and check whether those categories contain the data point’s real category. From Table. II, we can see that even for a hard task like fine-grained classification, when the training set is only 10%, there is still a high chance for the nearest neighbors containing the same category as the data point, e.g. 52.1% when $\alpha = 5$ . So we find even at the beginning of the annotation phase, models can still give reliable instructions and amateurs may classify a data point through a few comparisons.

Since we involve amateurs into the annotation process, it’s necessary to test amateurs’ pairwise comparison ability. So we do a small live test on 24 volunteers (12 females and 12 males) who don’t have any prior knowledge either on CUB-200-2011 or bird species. We generate 400 pairs from CUB-200-2011 dataset, which contain all 200 categories. Specifically, it has 200 pairs that don’t belong to the same category and 200 pairs that belong to the same category. We allocate 20 pairs to each volunteer (some pairs may be assigned to more than one person) and collect their pairwise comparison results. The average accuracy of the comparisons is 91.25%, the average accuracy of correctly recognizing different-category pairs is 93% and the average accuracy of correctly recognizing samecategory pairs is 90%. So it’s fair for us to assume that amateurs can provide rather accurate feedbacks even on finegrained datasets like CUB-200-2011.

TABLE I SYMBOL NOTATIONS 

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $D$ </td><td>Raw dataset</td></tr><tr><td> $D_{u}^{t}$ </td><td>Set of unlabeled data at batch  $t$ </td></tr><tr><td> $D_{h}^{t}$ </td><td>Set of half-labeled data which have some wrong categories excluded but don’t have a precise label at batch  $t$ </td></tr><tr><td> $D_{l}^{t}$ </td><td>Set of labeled data at batch  $t$ </td></tr><tr><td> $E^{t}$ </td><td>Set of data that experts will annotate at batch  $t$ </td></tr><tr><td> $A^{t}$ </td><td>Set of data that amateurs will annotate at batch  $t$ </td></tr><tr><td> $R_{e}^{t}$ </td><td>Category rank for experts at batch  $t$ </td></tr><tr><td> $R_{a}^{t}$ </td><td>Category rank for amateurs at batch  $t$ </td></tr><tr><td> $F$ </td><td>Set of data which is likely from new categories</td></tr><tr><td> $M_{q_{i}}^{t}$ </td><td>Set of data which the machine learning model classified as category  $q_{i}$  ( $1 \leq i \leq l^{t-1}$ ) at batch  $t$ </td></tr><tr><td> $l^{t}$ </td><td>The amount of discovered categories at batch  $t$ </td></tr><tr><td> $accu^{t}$ </td><td>The ratio of similar data pairs to all data pairs at batch  $t$ </td></tr><tr><td> $ratio_{ae}^{t}$ </td><td>Ratio of amateur annotation amount to expert annotation amount at batch  $t$ </td></tr><tr><td> $n$ </td><td>Total amount of data points</td></tr><tr><td> $c$ </td><td>Total amount of categories</td></tr><tr><td> $k$ </td><td>The price ratio of experts to amateurs</td></tr><tr><td> $m$ </td><td>The unified maximum annotation amount of experts for each batch</td></tr></table>

The results of the preliminary experiments make it possible for amateurs to produce a labeled data at a lower cost than experts which achieve our goal of cost saving. To assure this happen, firstly we introduce metric learning model and make the annotation an iterative process so that the metric can be updated in an online fashion. Secondly, we use the metric to help us give a distance-based classification to the unlabeled data and further perform an annotation assignment strategy based on the machine classifications to make experts discover new categories and handle uncertain data points while amateurs annotate the similar data pairs found by machines. The annotation assignment consists of the following parts: a) Allocate the annotation amount for experts and amateurs; b) Rank discovered categories; c) Discover new categories; d) Allocate specified samples for experts and amateurs. Through above steps, we make experts label a small number of the dataset and amateurs label each of the rest data through a few comparisons. In this way, we can achieve our goal of cost saving.

# C. Workflow

At the beginning, we use the feature extractor to extract raw feature for each data point. Note that we don’t make any fine-tuning on the target dataset for the feature extractor. In the first batch (batch 0), we use clustering algorithm to form c clusters. For each cluster, we assume data x is closest to the center, and data y is closest to data x. We will let experts annotate data x and amateurs perform a pairwise comparison on data y and data x. After the clustering, $D _ { l } ^ { 0 }$ , $D _ { h } ^ { 0 }$ and $D _ { u } ^ { 0 }$ are formed. We will use $D _ { l } ^ { 0 }$ to train the metric learning model and update l0.

In the following batches (batch $\geq 1 ) ,$ , at the beginning of batch t, we use the latest metric to calculate the $l ^ { t - 1 _ { - } }$ dimension confidence vectors for each data point in $D _ { h } ^ { t - 1 }$ and $D _ { u } ^ { t - 1 }$ . According to confidence vectors, we use our annotation assignment strategy shown in IV-D to select $E ^ { t }$ and $A ^ { t } .$ . After experts and amateurs annotate $E ^ { t }$ and $A ^ { t } .$ , we will update $D _ { l } ^ { t } , ~ D _ { h } ^ { t } , ~ D _ { u } ^ { t }$ and $l ^ { t }$ . All the data experts annotated will be removed from $D _ { h } ^ { t - 1 }$ or $D _ { u } ^ { t - 1 }$ and added to $D _ { l } ^ { t }$ . The new categories they discover will be updated on lt. Data points which are considered similar to the reference data by amateurs will be removed from $D _ { h } ^ { t - 1 }$ or $D _ { u } ^ { t - 1 }$ and added to $D _ { l } ^ { t }$ . Data points which are considered dissimilar to the reference data by amateurs will be removed from $D _ { u } ^ { t - 1 }$ and added to $D _ { h } ^ { t }$ or updated in Dth. We use function Anno(Et, At, Dt−1l,h,u) $D _ { h } ^ { t }$ $E ^ { t } , A ^ { t } , D _ { l , h , u } ^ { t - 1 } )$ to denote annotation procedure at batch t. We continue this iterative annotation until $| D _ { l } | ~ = ~ | D |$ . We show the whole annotation process of COCA in Algorithm 1. And the overall workflow is shown in Fig. 2.

Algorithm 1 COCA   
Input: D, n, c, m;
Output: $D_{l}^{t}$ .
1: $t \leftarrow 0$ , $D_{l}^{0} \leftarrow \emptyset$ , $D_{h}^{0} \leftarrow \emptyset$ , $D_{u}^{0} \leftarrow D$ , $l^{0} \leftarrow 0$ ;
2: $E^{t}$ , $A^{t} = Clustering(Feature Extraction(D))$ ;
3: $D_{l,h,u}^{t}$ , $l^{t}$ , $accu^{t} \leftarrow Anno(E^{t}, A^{t}, D_{l,h,u}^{t})$ ;
4: while $|D| \neq |D_{l}^{t}|$ do
5: $t \leftarrow t + 1$ ;
6: Train Metric with $D_{l}^{t-1}$ ;
7: $E^{t}$ , $A^{t} = Assign(m, accu^{t-1}, l^{t-1}, D_{l,h,u}^{t-1})$ ;
8: $D_{l,h,u}^{t}$ , $l^{t}$ , $accu^{t} \leftarrow Anno(E^{t}, A^{t}, D_{l,h,u}^{t-1})$ ;
9: end while
10: return $D_{l}^{t}$ .

# IV. DESIGN

# A. Feature Extraction

The very first phase of our annotation procedure is to extract features for data points in D. For example, when D is image dataset like CUB-200-2011, we can use convolution neural networks as feature extractors. Feature extractors are only used at phase one. In the clustering phase, the raw features will be used to calculate the clustering result of D which helps COCA to select $E ^ { 0 } , A ^ { 0 }$ . In the annotation assignment phase, the metric learning model learns distance metric on the basis of the raw features and gives pseudo labels to $D _ { u } , D _ { h }$ .

TABLE II   
THE RATIO OF DATA AND AT LEAST ONE OF ITS α NEAREST NEIGHBORS BELONGING TO THE SAME CATEGORY 

<table><tr><td>α</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td></tr><tr><td>ratio</td><td>24.5%</td><td>36.0%</td><td>42.7%</td><td>47.6%</td><td>52.1%</td><td>56.1%</td><td>59.5%</td><td>62.2%</td><td>63.5%</td><td>63.9%</td></tr></table>

![](images/e386e20b981179884060e7d32d22a3573411f42ef0baa21baed373e656ac2510.jpg)



Fig. 2. Workflow of COCA.

In conclusion, feature extractors extract raw features for each data point in D. And in later phases, clustering and metric learning will be performed on the basis of those raw features.

# B. Clustering

In this phase, we will use the raw features generated by feature extractors and divide D into c clusters. Those c clusters are the very first classification result used as the reference for data selection. For each cluster, we select one data point which is nearest to the cluster center to form $E ^ { 0 }$ . This is because we want experts to identify more new categories. And then for each cluster, we will choose one data point which is nearest to expert annotated data point to form $A ^ { 0 }$ . This is because those pairs are more likely to be the same category so that amateurs may produce more labeled data.

The clustering phase can be considered as batch 0. After batch 0, experts will produce c labeled data. And if amateurs think a data pair is similar, they produce one labeled data $d _ { l } ^ { 0 }$ , otherwise they produce one half-labeled data $d _ { h } ^ { 0 }$ . We will use $D _ { l } ^ { 0 }$ to train metric learning model and begin phase three.

# C. Train Metric Learning Model

At batch t, the metric learning model will be trained on $D _ { l } ^ { t - 1 }$ . The learned metric will be used to calculate the confidence vector for each data point in $D _ { h } ^ { t - 1 }$ and $D _ { u } ^ { t - 1 }$ . Confidence vector will be a $l ^ { t - \bar { 1 } }$ -dimension vector which represents the confidence of the data point belonging to each found category. We denote the process of generating confidence vector as function $g e n C o n \ ' f ( D _ { l , u , h } ^ { t - 1 } )$ . Firstly, We calculate the average feature vector of each found category in $D _ { l } ^ { t - 1 }$ as its representative feature vector. Then for each data point in $D _ { h } ^ { t - 1 } , D _ { u } ^ { t - 1 }$ , we use the metric to calculate its distance to each category’s representative feature vector. We use sof tmax function on the negative value of those distances and generate the final confidence. Thus, the lower the confidence, the less similar the data point to labeled samples of the category. Then we select Et, At based on confidence vectors of $\bar { D } _ { h } ^ { t - 1 } , D _ { u } ^ { t - 1 }$ .

# D. Annotation Assignment

We have to consider the following components during annotation assignment process: a) Allocate the annotation amount for experts and amateurs; b) Rank discovered categories; c) Discover new categories; d) Allocate specified samples for experts and amateurs. The process of annotation assignment is shown in Fig. 3. We will illustrate the annotation assignment by a running example in the rest of this section.

![](images/afe5a4862d6a437d96d9e8cead89cc959cfa0c58c94757b80005a037deab704c.jpg)



Fig. 3. The process of annotation assignment.

Assume for each batch, $m = 6 4 . \mathrm { A t }$ batch $t - 1 , r a t i o _ { a e } ^ { t - 1 } =$ $1 0 , | A ^ { t - 1 } | = 5 0$ and amateurs think 30 pairs among those 50 pairs belong to the same category and 20 pairs don’t. Now we are at batch t of annotation process and prepare to generate $E ^ { t }$ and $A ^ { t } .$

1) Calculate $| E ^ { t } |$ and $\vert A ^ { t } \vert .$ Firstly, we count the amount of pairs amateurs think similar at batch $t - 1$ as correctt−1, which is 30. Then we can calculate $\mathit { a c c u } ^ { t - 1 }$ as $c o r r e c t ^ { t - 1 } / \vert A ^ { t - 1 } \vert ,$ , which is $\textstyle { \frac { 3 0 } { 5 0 } } = 0 . 6$ . We calculate $\lvert E ^ { t } \rvert$ and $\lvert A ^ { t } \rvert$ as follows:

$$
\left| E ^ {t} \right| = \lceil m * (1 - a c c u _ {t - 1}) \rceil = \lceil 6 4 * (1 - 0. 6) \rceil = 2 6 \tag {1}
$$

$$
\left| A ^ {t} \right| = r a t i o _ {a e} ^ {t - 1} * \left| E ^ {t} \right| = 1 0 * 2 6 = 2 6 0
$$

After the annotation of batch t, we shall update $\boldsymbol { r a t i o } _ { a e } ^ { t }$ so that batch $t + 1$ can calculate $\vert E ^ { t + 1 } \vert$ and $\vert A ^ { t + 1 } \vert$ . The value of $r a t i o _ { a e } ^ { t }$ is influenced by the current performance of amateurs and metric learning models. If $a c c u ^ { t } \geq a c c u ^ { t - 1 }$ , it means the learned metric performs well and amateurs can annotate more.

Otherwise, amateurs should annotate less. $\boldsymbol { r a t i o } _ { a e } ^ { t }$ is updated as follows.

$$
\text { ratio } _ {a e} ^ {t} = \left\{ \begin{array}{l l} \min (\text { maxval }, \text { ratio } _ {a e} ^ {t - 1} + 1), & \text { if   } \text { accu } _ {t} \geq \text { accu } _ {t - 1} \\ \max (\text { minval }, \text { ratio } _ {a e} ^ {t - 1} - 1), & \text { if   } \text { accu } _ {t} <   \text { accu } _ {t - 1} \end{array} \right. \tag {2}
$$

minval and maxval is upper and lower bounds of $r a t i o _ { a \epsilon }$ so that the amateur annotated amount won’t be so low which limits their potential of producing $d _ { l }$ or too high to cause unnecessary waste on comparing dissimilar pairs selected by a poor metric.

2) Rank Discovered Categories: In the category ranking part, we generate priority list of the discovered $l ^ { t - 1 }$ categories for amateurs and experts. We mainly consider two aspects in this procedure: a) Inter-category balance. We hope that during annotation process, labeled sample amount for each category is balanced so that metric learning model can have a better performance [27]; b) Intra-category variance. If for category $q _ { i } .$ , the variance of the feature vectors transformed by metric learning model is very large. It indicates that the metric learning model is not good at distinguishing qi. Thus, it’ll be better to ask experts rather than amateurs to annotate samples in $M _ { q _ { i } } ^ { t }$ . On the contrary, if the variance of the transformed feature vector is small, it means that metric learning model is good at distinguishing $q _ { i } .$ . Thus, let experts annotate samples in $M _ { q _ { i } } ^ { t }$ may lead to unnecessary overhead.

Therefore, we intend to let experts label categories which have less sample amount and larger intra-category variance. And amateurs label categories which have less sample amount and smaller intra-category variance. Denote the amount of labeled samples of $q _ { i }$ in $\dot { D } _ { l } ^ { t - 1 }$ as $| q _ { i } |$ . The category ranking process is shown in Algorithm 2

Algorithm 2 Rank   
Input: $D_{l}^{t-1}$ , $l^{t-1}$ Output: $R_{e}^{t}$ , $R_{a}^{t}$ 1: numSum ← 0, stdSum ← 0

2: for i in $[1, l^{t-1}]$ do

3: numSum = numSum + |q_i|

4: $std_{q_i} = \frac{\sum_{j=1}^{|q_i|} distance(f_{ij}, \overline{f_i})}{|q_i|}$ 5: stdSum = stdSum + std_q_i

6: end for

7: numAvg = $\frac{numSum}{l^{t-1}}$ 8: stdAvg = $\frac{stdSum}{l^{t-1}}$ 9: for i in $[1, l^{t-1}]$ do

10: numrank_q_i = $\frac{|q_i|}{numAvg}$ 11: $stdrank_{q_i} = \frac{std_{q_i}}{stdAvg}$ 12: end for

13: $R_e^t \leftarrow ascendSort(numrank_{q_i} - stdrank_{q_i})$ 14: $R_a^t \leftarrow ascendSort(numrank_{q_i} + stdrank_{q_i})$ 15: return $R_e^t$ , $R_a^t$

Assume at batch t, we have so far discovered 3 categories $( l ^ { t - 1 } ~ = ~ 3 )$ , namely $q _ { 1 } , q _ { 2 } , q _ { 3 } .$ . In $D _ { l } ^ { t - 1 } , \ q _ { 1 }$ has 3 labeled samples, q2 has 6 labeled samples, q3 has 9 labeled samples. So the average sample number of the discovered categories numAvg will be $\begin{array} { r } { \frac { \sum _ { i = 1 } ^ { l ^ { t - 1 } } | q _ { i } | } { l ^ { t - 1 } } = \frac { 3 + 6 + 9 } { 3 } = 6 . } \end{array}$ - i=1 lt−1 3+6+9 = 6. And lt−1 numra $\begin{array} { r } { _ { l } k _ { q _ { 1 } } ~ = ~ \frac { | q _ { 1 } | } { n u m A v q } ~ = ~ \frac { 3 } { 6 } ~ = ~ 0 . 5 , } \end{array}$ $n u m r a n k _ { q _ { 2 } } ~ = ~ 1$ numran $k _ { q _ { 3 } } = 1 . 5 .$ .

Assume for $q _ { 1 } ,$ , the 3 labeled samples have features $f _ { 1 1 } =$ $( 2 , 3 , 4 , 1 )$ , $f _ { 1 2 } ~ = ~ ( 8 , 9 , 7 , 2 )$ , $f _ { 1 3 } ~ = ~ ( 2 0 , 3 , 4 , 3 )$ . We calculate the average feature of q1 as ${ \overline { { f _ { 1 } } } } ~ = ~ { \frac { f _ { 1 1 } + f _ { 1 2 } + f _ { 1 3 } } { 3 } } ~ =$ 3 $( 1 0 , 5 , 5 , 2 )$ , so the intra-category variance for $q _ { 1 }$ is $s t d _ { q _ { 1 } } =$ $\begin{array} { r } { \frac { \sum _ { j = 1 } ^ { | q _ { 1 } | } d i s t a n c e ( f _ { 1 j } , \overline { { f _ { 1 } } } ) } { | a _ { 1 } | } ~ = ~ \frac { 8 . 3 + 4 . 9 + 1 0 . 3 } { 3 } ~ = ~ 7 . 8 . } \end{array}$ |q1| 8.3+4.9+10.3 = 7.8. Here, we use 3 Euclidean distance as distance(), in the experiment, it will be the distance calculated by the metric learning model. In this way, assume we calculate $s t d _ { q _ { 2 } } = 4 . 2$ and $s t d _ { q _ { 3 } } = 6 . 5 .$ . We then calculate the average variance of discovered category stdAvg as stdq1 $\begin{array} { r } { \frac { s t d _ { q _ { 1 } } } { s t d A v g } = \frac { 7 . 8 } { 6 . 1 } \dot { = } 1 . 2 , } \end{array}$ $\begin{array} { r } { \frac { \sum _ { i = 1 } ^ { l ^ { t - 1 } } | s t d _ { q _ { i } } | } { l ^ { t - 1 } } = \frac { \mathbf { \bar { 7 } } . 8 + 4 . 2 + 6 . 5 } { 3 } = 6 . 1 } \end{array}$ - i=1 lt− lt−1 |stdqi | , stdran 7.8+4.2+6.5 = 6.1. So stdrankq = $\begin{array} { r } { k _ { q _ { 2 } } = \frac { 4 . 2 } { 6 . 1 } = 0 . 6 , } \end{array}$ 3 $s t d r a n k _ { q _ { 3 } } =$ $s t d r a n k _ { q _ { 1 } } =$ $\textstyle { \frac { 6 . 5 } { 6 . 1 } } = 1 . 1 .$ . For experts, the priority of categories is the ascending order of numran $k _ { q _ { i } } - s t d r a n k _ { q _ { i } }$ , so ${ R _ { e } ^ { t } = \{ q _ { 1 } , q _ { 2 } , q _ { 3 } \} }$ . For amateurs, the priority of categories is the ascending order of numran $\mathrm { \Delta } k _ { q _ { i } } + s t d r a n k _ { q _ { i } }$ , so ${ R } _ { a } ^ { t } = \{ q _ { 2 } , q _ { 1 } , q _ { 3 } \}$ .

3) Discover New Categories: After ranking the discovered categories, we will check whether $l ^ { t - 1 } = c .$ If not, we hope experts to discover new categories at batch t. The reason we don’t expect amateurs to do that is because:

If data x doesn’t belong to any of the found $l ^ { t - 1 }$ categories, it’s a new category. So when amateurs annotate, it will involve $l ^ { t - 1 }$ -time pairwise comparisons. And if $\mathrm { i t } ^ { \prime } \mathrm { s }$ indeed a new category, expert shall give the actual label for it. Thus, it introduces the extra $l ^ { t - \tilde { 1 } }$ -time pairwise comparisons cost compared to only using experts to discover new categories.

Therefore, we can reasonably require that, for data which may belong to a new category, we want experts to label them directly. Denote confidence vector of data x as $( p _ { q _ { 1 } } , p _ { q _ { 2 } } , p _ { q _ { 3 } } ) .$ , we show a way of finding data points which are more likely belonging to new categories in Algorithm 3.

Algorithm 3 Filter   
Input: $D_{h}^{t-1}$ , $D_{u}^{t-1}$ , $|E^{t}|$ , $l^{t-1}$ Output: $E^{t}$ 1: $F \leftarrow \emptyset$ 2: for i in $[1, l^{t-1}]$ do

3: margin $\leftarrow 0$ 4: for data x in $M_{q_{i}}^{t}$ do

5: margin = max(margin, 0.5 - $|p_{q_{i}} - 0.5|$ )

6: end for

7: for data x in $M_{q_{i}}^{t}$ do

8: if $p_{q_{i}} \leq margin$ then

9: $F \leftarrow F \cup \{x\}$ 10: end if

11: end for

12: end for

13: $E^{t} \leftarrow random(F, |E^{t}|)$ 14: return $E^{t}$

After genCon $f ( D _ { l , u , h } ^ { t - 1 } )$ , we get the confidence vector of $D _ { u } ^ { t - 1 } , D _ { h } ^ { t - 1 }$ l,u,h. For category q1, we add data whose confidence vector reaching largest value on $q _ { 1 }$ to $M _ { q _ { 1 } } ^ { t }$ . Assume $M _ { q _ { 1 } } ^ { t }$ 1 have samples $x _ { 1 } = ( 0 . 7 , 0 . 2 , 0 . 1 ) , x _ { 2 } = ( 0 . { \overset { . } { 5 } } 5 , 0 . 2 , 0 . 2 5 ) .$ , $x _ { 3 } =$ $( 0 . 4 , 0 . 3 , 0 . 3 )$ . We choose the maximum value of $0 . 5 - | p _ { q 1 } -$ 0.5| as margin for $M _ { q _ { 1 } } ^ { t }$ , which is $0 . 4 5$ in this case. If data $x$ in $M _ { q _ { 1 } } ^ { t }$ has $p _ { q _ { 1 } }$ smaller than this margin, then x is more likely to belong to a new category than actually belong to $q _ { 1 }$ compared to other data in $M _ { q _ { 1 } } ^ { \bar { t } }$ . We will add those data into candidate set $F$ and randomly pick $| E ^ { t } |$ samples from $F$ as $E ^ { t }$ . In this case, for $M _ { q _ { 1 } } ^ { t }$ , we will add $x _ { 3 }$ into $F .$ .

4) Allocate Specified Samples for Experts and Amateurs: Since amateurs don’t have to discover categories, $A ^ { t }$ will be derived according to ${ R } _ { a } ^ { t } ~ ( \{ q _ { 2 } , q _ { 1 } , q _ { 3 } \} )$ . For each $q _ { i }$ , we choose $\textstyle \bigl \lceil \frac { | A ^ { t } | } { | R _ { a } ^ { t } | } \bigr \rceil = \bigl \lceil \frac { 2 6 0 } { 3 } \bigr \rceil = 8 7$ pairs in M tq . If |M tq | ≤ 87, we will simply choose $\vert M _ { q _ { i } } ^ { t } \vert$ pairs.

According to the uncertainty-based sampling in active learning [28], label the most uncertain samples will improve the model performance. We use information entropy [29] to measure the uncertainty. The information entropy of data x is:

$$
S = - \sum_ {i = 1} ^ {l ^ {t - 1}} p _ {q _ {i}} * \ln p _ {q _ {i}} \tag {3}
$$

For amateurs, we have to determine the reference category to perform pairwise comparison. Assume reference category is $q _ { z } , \mathrm { i f }$ sample x belongs to $q _ { z } , \Delta S = S - 0 = S ,$ , otherwise, $\Delta S = S - \bar { S } ^ { ' }$ . We calculate $S ^ { ' }$ as follows:

$$
a ^ {\prime} = - \sum_ {i = 1, i \neq z} ^ {l ^ {t - 1}} p _ {q _ {i}} \tag {4}
$$

$$
S ^ {'} = - \sum_ {i = 1, i \neq z} ^ {l ^ {t - 1}} \frac {p _ {q _ {i}}}{a ^ {\prime}} * \ln \frac {p _ {q _ {i}}}{a ^ {\prime}}
$$

For reference category $q _ { z } , E ( \Delta S )$ is as follows:

$$
\begin{array}{l} E (\Delta S) = p _ {q _ {z}} S + (1 - p _ {q _ {z}}) \left(S - S ^ {\prime}\right) \\ = S - \left(1 - p _ {q _ {z}}\right) S ^ {\prime} \tag {5} \\ = - p _ {q _ {z}} \ln p _ {q _ {z}} - (1 - p _ {q _ {z}}) \ln (1 - p _ {q _ {z}}) \\ \end{array}
$$

We will choose category $q _ { z }$ which maximizes $E ( \Delta S )$ as the reference category for x, i.e. $q _ { z }$ satisfies

$$
\underset {1 \leq z \leq l ^ {t - 1}} {\arg \max} (p _ {q _ {z}} S + (1 - p _ {q _ {z}}) (S - S ^ {\prime})) \tag {6}
$$

If $q _ { z }$ satisfies Equ. $6 , q _ { z }$ also satisfies:

$$
\underset {1 \leq z \leq l ^ {t - 1}} {\arg \min} \quad | p _ {q _ {z}} - 0. 5 | \tag {7}
$$

We can prove that if $q _ { z }$ satisfies Equ. $7 , p _ { q _ { z } }$ is the largest value in confidence vector of sample x.

Theorem 1. For a confidence vector $( p _ { q _ { 1 } } , p _ { q _ { 2 } } , . . . , p _ { q _ { l } t - 1 } ) , p _ { q _ { z } }$ is the largest value in the confidence vector $i f \ p _ { q _ { z } }$ satisfies arg min $1 { \le } z { \le } l ^ { t - 1 } \quad \left| p _ { q _ { z } } - 0 . 5 \right|$ |.

Proof. Suppose there is a value $p _ { q _ { j } }$ satisfied $p _ { q _ { j } } ~ > p _ { q _ { z } }$ , we have:

$$
\left| p _ {q _ {j}} - 0. 5 \right| \geq \left| p _ {q _ {z}} - 0. 5 \right|
$$

$$
p _ {q _ {j}} ^ {2} - p _ {q _ {j}} \geq p _ {q _ {z}} ^ {2} - p _ {q _ {z}} \tag {8}
$$

$$
p _ {q _ {j}} ^ {2} - p _ {q _ {z}} ^ {2} \geq p _ {q _ {j}} - p _ {q _ {z}}
$$

$$
p _ {q _ {j}} + p _ {q _ {z}} \geq 1
$$

Because $\begin{array} { r } { \sum _ { i = 1 } ^ { l ^ { t - 1 } } p _ { q _ { i } } \ = \ 1 , \ p _ { q _ { j } } \ + \ p _ { q _ { z } } \ = \ 1 . \ q _ { j } \ } \end{array}$ lt−1 also satisfies arg min $1 { \le } j { \le } l ^ { t - 1 } \quad \ | p _ { q _ { j } } - 0 . 5 |$ . Therefore, we prove that, for sample $x ,$ its reference category is the category corresponding to the maximum confidence. □

Algorithm 4 Assign   
Input: m, $accu^{t-1}$ , $l^{t-1}$ , $D_{l}^{t-1}$ , $D_{u}^{t-1}$ , $D_{h}^{t-1}$ Output: $E^{t}$ , $A^{t}$ 1: $|E^{t}| = m * (1 - accu^{t-1})$ 2: $|A^{t}| = ratio_{ae} \times |E^{t}|$ 3: $R_{e}^{t}$ , $R_{a}^{t} = Rank(D_{l}^{t-1}, l^{t-1})$ 4: if $l^{t-1} < c$ then

5: $E^{t} = Filter(D_{h}^{t-1}, D_{u}^{t-1}, |E^{t}|, l^{t-1})$ 6: else

7: for category $q_{i}$ in $R_{e}^{t}$ do

8: if $M_{q_{i}} \neq \emptyset$ then

9: sort $M_{q_{i}}$ in ascending order by $|p_{q_{i}} - 0.5|$ 10: pick top min( $|\frac{E^{t}}{|R_{e}^{t}}|$ , $|M_{q_{i}}|$ ) data join $E^{t}$ 11: end if

12: end for

13: end if

14: for category $q_{i}$ in $R_{a}^{t}$ do

15: if $M_{q_{i}} \neq \emptyset$ then

16: sort $M_{q_{i}}$ in ascending order by $|p_{q_{i}} - 0.5|$ 17: pick top min( $|\frac{A^{t}}{|R_{a}^{t}}|$ , $|M_{q_{i}}|$ ) data join $A^{t}$ 18: end if

19: end for

20: return $E^{t}$ , $A^{t}$

As a result, data in $M _ { q _ { i } } ^ { t }$ will have $q _ { i }$ as their reference category. According to ${ R } _ { a } ^ { t } = \{ q _ { 2 } , q _ { 1 } , q _ { 3 } \}$ , we firstly check $q _ { 2 }$ . In $M _ { q _ { 2 } } ^ { t }$ , the reference category is q2. We rank samples in $M _ { q _ { 2 } } ^ { t }$ according to their $E ( \Delta S )$ , which is equivalent to sorting them in the ascending order of $| p _ { q _ { 2 } } - 0 . 5 |$ . We will select top 87 data in the sorted sequence of $M _ { q _ { 2 } } ^ { t }$ and set the reference category as $q _ { 2 }$ to form 87 pairs. We repeat this procedure on $q _ { 1 } , q _ { 3 }$ and finally add at most 261 pairs to $A ^ { t }$ .

For experts, if ${ l ^ { t - 1 } < c , E ^ { t } }$ will be selected according to F rather than $R _ { e } ^ { t }$ . Otherwise, we will select $E ^ { t }$ according to $R _ { e } ^ { t }$ $( \{ q _ { 1 } , q _ { 2 } , q _ { 3 } \} )$ . For each $q _ { i }$ , we choose $\begin{array} { r } { \lceil \frac { | E ^ { t } | } { | R _ { e } ^ { t } | } \rceil = \lceil \frac { 2 6 } { 3 } \rceil = 9 } \end{array}$ data in $M _ { q _ { i } } ^ { t }$ . Then we sort samples in $M _ { q _ { i } } ^ { t }$ in the ascending order of $| p _ { q 2 } - 0 . 5 |$ and add top 9 data in the sorted sequence to $E ^ { t }$ . We repeat this procedure on $q _ { 2 } , q _ { 3 }$ , and finally add at most 27 data to $E ^ { t }$ . The annotation assignment in batch $t \ ( t \geq 1 )$ ) is shown in Algorithm 4.

After annotation assignment, experts and amateurs annotate $E ^ { t }$ and $A ^ { t }$ respectively. $D _ { l } ^ { t } , D _ { h } ^ { t }$ and $D _ { u } ^ { t }$ will be updated according to the annotation result. If $| D _ { l } ^ { t } | = | D |$ , the annotation process completes, otherwise, we will start batch $t + 1$ .

# V. EXPERIMENT

In the following sections, we are gonna verify our system performance from three aspects: a) The efficiency of system components, including the stability of our system when changing feature extractors, the efficiency of our annotation assignment strategy and the impact of minval and maxval; b) Compare COCA with SOTA automatic labeling models; c) The ability of COCA generalizing to different annotation tasks. Since the main goal of COCA is to save annotation cost, we set our metric as SavedRate. Assume after the annotation process, the total expert annotated amount is $n _ { e } ,$ the total amateur annotated amount is $n _ { a } .$ SavedRate is calculated as follows:

$$
\text { SavedRate } = \frac {n - (n _ {e} + \frac {n _ {a}}{k})}{n} \tag {9}
$$

# A. Parameter Setting

Dataset. Considering our setting, we choose fine-grained dataset as our experiment dataset, including Stanford Dogs [30], CUB-200-2011 [31]. Obviously, few people can give the precise label of a dog or a bird. However, numerous people can tell whether two images belong to the same category. Specific information is shown in Table. III. ”Train” represents the number of images in the training set, ”Test” represents the number of images in the testing set.

TABLE III DATASET SETTING 

<table><tr><td>Name</td><td>c</td><td>n</td><td>Train</td><td>Test</td></tr><tr><td>Stanford Dogs</td><td>120</td><td>20580</td><td>12000</td><td>8580</td></tr><tr><td>CUB-200-2011</td><td>200</td><td>11788</td><td>5994</td><td>5794</td></tr></table>

Metric Learning Model. We use Large Margin Nearest Neighbor (LMNN) [9] as our metric learning model in the experiment. Since pairwise comparison is similar to nearest neighbor classification and the accuracy of the classification largely depends on the metric used to calculate the distance. LMNN uses Mahalanobis distance metric to optimize K nearest neighbor classification. The goal of Mahalanobis distance metric is to ensure certain amount (3 in our setting) of nearest neighbors always belong to the same category as the data point, and samples of different categories are separated by a large margin.

Feature Extractors. In Section III-C, we use a feature extractor to extract raw features, and perform clustering and metric learning on the basis of these features. In the experiment, we use Mobile Net, VGG16, and ResNet50 in keras.applications as feature extractors. We remove the classification layer of those networks, and use the Global Average Pooling layer in keras.layers to convert the w × h × c tensor output by last layer of the network into a $1 \times 1 \times c$ tensor as the final feature. Finally We obtain 512-dimension feature on VGG16, 1024-dimension feature on Mobile Net and 2048- dimension feature on ResNet50.

k. In our assumption, the price of single time expert annotation and amateur annotation is different. In section I, we discuss about the impact of k on the annotation cost. In the experiment, k ranges from 1 to 50.

Baselines. To verify the efficiency of our expert-based data selection, We choose random selection and existing uncertainty-based data selection methods, namely a) BvSB [32], which selects the samples which has the smallest gap between two highest confidence; b) Least Confidence [33], which selects samples which has the smallest highest confidence; c) Maximum Entropy [34], which selects samples with the largest entropy. To verify the efficiency of Algorithm 4, we further design three baselines for comparison. And we compare the system performance with automatic labeling method using SOTA fine-grained classification models, namely TransFG [35], API-Net [36], GAP+ [37] and PMG [38]. The cost of automatic labeling methods is calculated as the cost of expert annotating the training set.

# B. Efficiency of System Components.

1) Feature Extractor: Feature extractor is an essential and basic tool in our method. Since the feature extractors may vary in real applications, so it’s necessary to verify the impact of different feature extractors on COCA. To some extent, it can also verify the efficiency of introducing metric learning model.

We use three different feature extractors on CUB-200-2011 dataset, namely Mobile Net, VGG16, and ResNet50. Note that all these three networks have only be pre-trained on ImageNet which is a different domain compared to CUB-200- 2011 dataset. Fig. 4 shows the result of the SavedRate when finishing annotation on CUB-200-2011.

![](images/cb5944127ed8bf9a1f559555db758add233345fec4e0ba35c37f423d3c436515.jpg)



Fig. 4. SavedRate generated by three feature extractors on the CUB-200- 2011 dataset.

We use a red horizontal line to mark SavedRate = 0. which is the SavedRate when using experts to annotate the whole dataset. We can see from Fig. 4 that when k is smaller than a certain value, namely 2.8 for ResNet50, 3 for VGG16 and 3.6 for Mobile Net, our method can’t save cost because the average amateur annotated times on each amateur annotated sample may exceed k which finally cause the total cost exceeds n. As k grows, the SavedRate will grow and tend to be stable at a level around 70%.

Besides, we can also observe that the performance of these three feature extractors is very similar. Under the feature extractors of different complexity and features of different dimensions, COCA can save cost steadily. The reason is likely to be the use of metric learning models. Like said in section IV, metric learning model is to learn the metric distance function for a specific task, so the choice of feature extractor has little effect on COCA. Since ResNet50 has the best overall performance, we will use ResNet50 as our feature extractor to complete the following experiments.

2) Annotation Assignment: In our work, an efficient annotation assignment method is the key to saving cost. We choose four common baseline methods for expert-based data selection, namely Random, BvSB, Least Confidence and Maximum Entropy. 30%, 50% , 90% and 100% in Table IV means $\frac { | D _ { l } | } { | D | }$ . Values in those columns are the proportion of expert annotated data to all data.

TABLE IV $\textstyle { \frac { N _ { e } } { n } }$ Ne UNDER DIFFERENT DATA SELECTION METHODS 

<table><tr><td>Methods</td><td>30%</td><td>50%</td><td>90%</td><td>100%</td></tr><tr><td>Random</td><td>3.52%</td><td>7.93%</td><td>19.08%</td><td>25.94%</td></tr><tr><td>BvSB</td><td>3.32%</td><td>8.09%</td><td>18.54%</td><td>25.57%</td></tr><tr><td>Least Confidence</td><td>3.44%</td><td>7.76%</td><td>21.56%</td><td>28.50%</td></tr><tr><td>Maximum Entropy</td><td>3.49%</td><td>10.15%</td><td>27.60%</td><td>33.22%</td></tr><tr><td>COCA</td><td>2.74%</td><td>7.19%</td><td>17.64%</td><td>23.34%</td></tr></table>

Besides verifying the expert-based data selection, we introduce three reasonable and popular assignment methods for comparision: a) Random, which randomly selects samples for experts and amateurs; b) Entropy-based, which selects samples with largest entropy for experts and smallest entropy for amateurs; c) Confidence-based, which selects samples with least confidence for experts and highest confidence for amateurs. Assume after the annotation process, the total amount of expert annotated data is $n _ { e } ,$ , the total amount of amateur annotated data is $n _ { a } .$ . We compare $n _ { e } , n _ { a }$ of COCA and the above three baselines when annotating all 11,788 images in CUB-200- 2011. The results are shown in Table V.

TABLE V $n _ { e } , n _ { a }$ UNDER DIFFERENT ANNOTATION ASSIGNMENT METHODS 

<table><tr><td>Methods</td><td> $n_e$ </td><td> $n_a$ </td></tr><tr><td>Random</td><td>3391</td><td>34968</td></tr><tr><td>Entropy-Based</td><td>5147</td><td>58857</td></tr><tr><td>Confidence-Based</td><td>3802</td><td>40622</td></tr><tr><td>COCA</td><td>2840</td><td>29028</td></tr></table>

According to Table IV and Table V, COCA outperforms all the other annotation assignment methods by significantly reducing both expert annotation amount and amateur annotation amount. Therefore COCA can save significant labour costs.

3) Impact of minval and maxval: Since we set minval and maxval parameters for $r a t i o _ { a e } ,$ we now explore their impact on SavedRate.

![](images/e8a072641b07002a857c361dcca3a2abe5ab3730afc42ec2bcdf54e4e871df58.jpg)



Fig. 5. SavedRate on the CUB-200-2011 dataset under different combinations of (minval, maxval).

Larger maxval increases the trust of amateurs with high accuracy, and vice versa. Smaller minval increases the punishment for amateurs with low accuracy, and vice versa. We consider the following (minval, maxval) combinations: (1, 5), (5, 10), (10, 15). Fig 5 shows the SavedRate when finishing annotation on CUB-200-2011. As k increases, the SavedRate of larger (minval, maxval) combinations grows faster and gets higher. It indicates that when experts are much more expensive than amateurs and amateurs are accurate in pairwise comparisons, giving amateurs more opportunities to label will help save costs. In Section V-B, we use the simulated amateurs, who have 100% accuracy in pairwise comparisions, to verify the efficiency of system components, hence we set (minval, maxval) to (10,15). In Section V-C, when using the real amateurs from a crowdsourced platform, we set (minval, maxval) for CUB-200-2011 to (1,3) and (minval, maxval) for Stanford Dogs to (1,5).

# C. Advantages over Automatic Labeling

In this section, for the amateur annotation, we use both simulated and real amateurs to verify the performance of COCA. We let the simulated amateurs always give the correct pairwise comparison result, and we set (minval, maxval) to (10,15). we recruited 124 real amateurs from a public crowdsourcing data annotation platform, named Datatang, to conduct pairwise comparisions on Stanford dogs and CUB-200-2011 datasets. The real amateurs consist of 89 males and 35 females, whose ages range from 20 to 40. They don’t have any prior knowledge on bird or dog species. The price for each pairwise comparison is 0.1\$. For real amateurs, we set (minval, maxval) for CUB-200-2011 to (1,3), (minval, maxval) for Stanford Dog to (1,5). For experts, we assume they always give the correct answers.

1) Cost Comparison of Different k under the Same Precision: We compare the cost of COCA with automatic labelling when reaching the approximately equal annotation precision. Here, we adopt the SOTA fine-grained classification models as the baseline automatic labelling method. The split of training set and testing set on two datasets is shown in Table. III. We get the precision of those models on the test set [35], [36], [37]. We further calculate the precision of the whole dataset by $\begin{array} { r } { p r e c i s i o n _ { C U B } = \frac { 5 9 9 4 + 5 7 9 4 * p } { 1 1 7 8 8 } } \end{array}$ , precision $\cdot D o g s \ =$ 11788 12000+8580∗p . The final precision is shown in Table. VI. $\frac { 1 2 0 0 0 + 8 5 { \dot { 8 } } 0 * p } { \sim \sim \sim \sim \sim }$ $\frac { \mathrm { ) 0 + 8 5 8 0 \ast } p } { \mathrm { 2 0 5 8 0 } }$ 20580

For the annotation cost of the SOTA models, we use the price of experts annotating the whole training dataset. For the annotation cost of COCA, we use $\begin{array} { r } { n _ { e } + \frac { n _ { a } } { k } } \end{array}$ . We will compare our cost under different k when we reaches the same precision as the SOTA models.

TABLE VI THE BASELINE MODELS’ PRECISION ON DATASETS 

<table><tr><td>Models</td><td>Stanford Dogs</td><td>CUB-200-2011</td></tr><tr><td>TransFG</td><td>96.7%</td><td>95.9%</td></tr><tr><td>API-Net</td><td>95.9%</td><td>95%</td></tr><tr><td>GAP+</td><td>94.7%</td><td>92.4%</td></tr></table>

![](images/afbc81f487f13fb95c4c3f8cb6561607482051954b5391520059f1ed8ac051cc.jpg)



(a) Simulated amateur.

![](images/ec62ac853a716b29ff813301a228b019e83240a1e8a5c30ceb462629647975f1.jpg)



(b) Real amateur.

Fig. 6. Cost of COCA and the SOTA models at precision 96.7% over different k on the Stanford Dogs dataset.   
![](images/58f1b6551820e862446ea4fd4c00a3c221521cb26baebf6d5f85ef5322d8aae8.jpg)



(a) Simulated amateur.

![](images/5accce22d3835e98e6e829c4ab245feeb30edfbfe98c31321aaa628d445780fe.jpg)



(b) Real amateur.   
Fig. 7. Cost of COCA and the SOTA models at precision 95.9% over different k on the CUB-200-2011 dataset.

We compare the cost for different k when the annotation precision is the same as SOTA models, i.e. TrandFG, API-Net, GAP+. Fig. 6 and Fig. 7 illustrate results for both simulated and real amateurs. The results show that COCA can save cost in both simulated and real-world scenarios when k is above a certain threshold, which is 2.5 and 6 for Stanford Dogs, 8.3 and 38.7 for CUB-200-2011. COCA performs better in the simulated scenarios, since real amateurs can make mistakes during annotation. The wrong $d _ { l }$ they produce affect the metric learning models, leading to a larger k threshold. k threshold for Stanford Dogs is smaller than that for CUB-200-2011, which indicates that metric learned on Stanford Dogs can better capture the inter-class discrimination and intra-class similarity than it does on CUB-200-2011. Moreover, amateurs can distinguish dog species better than bird species. It’s probably because dogs of different species are more commonly seen in daily life and on Internet.

2) Precision Comparison of Different k under the Same Cost: After comparing the cost under the same precision, we now compare the precision under the same cost. We set the cost to what it would cost experts to annotate $1 0 \% * n , 2 0 \% * n ,$ $3 0 \% * n , 4 0 \% * n , 5 0 \% * n$ data. We use PMG and TransFG as the baseline networks. Noted that, among all SOTA models, TransFG reaches the highest precision on the test set of both Stanford Dogs and CUB-200-2011. Fig. 8 and Fig. 9 show the results of this experiment. ra,sa in the legend means real amateurs and simulated amateurs respectively.

![](images/e988e9d84bb03a41dae7f8a74b9006e40c74d7742b09158588893d02e943ac1c.jpg)



Fig. 8. Precision under the same cost compared to PMG and TransFG on the Stanford Dogs dataset. Here ra, sa mean real amateurs and simulated amateurs, respectively.

![](images/6814dfd4c01c3fda6cf99cbcce50dd352a1918b245819f081e3a24f44acec38d.jpg)



Fig. 9. Precision under the same cost compared to PMG and TransFG on the CUB-200-2011 dataset. Here, ra, sa mean real amateurs and simulated amateurs, respectively.

As shown in Fig. 8, using the Stanford Dogs dataset, for simulated amateurs, COCA reaches higher precision than PMG when $k ~ = ~ 4 0$ at $1 0 \% * n$ cost. The precision of COCA reaches 100% when cost $\geq 2 0 \% * n$ and $k \geq 3 0 .$ , which obviously outperform both PMG and TransFG. For real amateurs, when cost ≥ 40% ∗ n and $k \geq 3 0$ , the precision of COCA outperforms both PMG and TransFG.

As shown in Fig. 9, using the CUB-200-2011 dataset, for simulated amateurs, COCA reaches higher precision than PMG when $k \geq 3 0$ at 30% cost. The precision of COCA is 100% when cost $\geq 3 0 \% * n$ and $k \geq 4 0$ . For real amateurs, the precision is approximately the same as the SOTA models when cost $\geq 4 0 \% * n$ and $k \geq 3 0$ , and it outperforms both SOTA models when k = 40 at 50% ∗ n cost. In real life, design such SOTA models can also bring high labor cost of trail-and-error experiments. Using COCA, we can reach comparable precision under relatively limited budget.

# D. Generalization to Different Annotation Task

The above sections have verified COCA on fine-grained image datasets. To further investigate COCA’s potential of generalizing to other annotation tasks, we will verify COCAs performance on audio and text datasets in this section.

For audio dataset, we use UrbanSound8K. The dataset contains 8732 labeled sound excerpts (≤ 4s) of urban sounds from 10 categories. For text dataset, we use Stanford Sentiment Treebank. The dataset consists of 11,855 single sentences extracted from movie reviews. Each phrase is labelled as either negative, somewhat negative, neutral, somewhat positive or positive. The corpus with all 5 labels is referred to as SST-5 or SST fine-grained.

We use the SOTA models [39], [40] on these tasks as baselines, and compare the cost when COCA reaches the same precision (calculated like Section V-C1). For audio COCA uses 3072-dimension mfcc feature extracted by librosa.feature; for text COCA uses 765-dimension feature extracted by BERT. Table. VII lists the train, validation and test splits for all models and Fig. 10 shows the comparison results. Compared to SOTA classification models, COCA can save cost when k is above a small threshold, which is 3 for UrbanSound8K and 3.6 for Stanford Sentiment Treebank. The results prove that COCA can be well adapted to different annotation fields.

TABLE VII THE BASELINE MODELS’ PRECISION ON DATASETS 

<table><tr><td>Models</td><td>Train+Validation</td><td>Test</td><td>Accuracy</td></tr><tr><td>SB-CNN(aug)</td><td>7858</td><td>874</td><td>97.9%</td></tr><tr><td>RoBERTa-large+Self-Explaining</td><td>9645</td><td>2210</td><td>92.3%</td></tr></table>

![](images/25e97f4d13bbe507b6c2eeebe78af6af14e485631422f9b32fda598c1ac2538c.jpg)



(a) UrbanSound8K.

![](images/77e4da5f62b951bde87b42565c550630a278dacfdb806cf4c5be088d0d5ac69f.jpg)



(b) SST-5.   
Fig. 10. Cost of COCA and the SOTA models at precision 97.9% and 92.3% over different k on the UrbanSound8K dataset and the SST-5 dataset.

# VI. DISCUSSION AND FUTURE WORK

In the experiment, we find that metric learning can perform steadily under the features extracted by different feature extractors. However, those feature extractors are all pre-trained on ImageNet, which has more dog categories than birds. As a result, COCA’s performance on Stanford Dogs is better than CUB-200-2011. But even if ImageNet is a very different dataset from CUB-200-2011 and Stanford Dogs, COCA can still save annotation cost on Stanford Dogs and CUB-200- 2011. It indicates that it’s not necessary for the feature extractors to be pre-trained on the target dataset, instead, it only needs to be pre-trained on off-the-shelf labeled datasets related to the target dataset. In this paper, ”related” means having common coarse-grained categories such as ImageNet and Stanford Dogs all have dog categories. It reminds us that dynamically adjust the features during the annotation process may lead to a better performance.

In this paper, we mainly discuss about the possibility of a cost-effective annotation system through multi-agent collaboration. We further implement COCA and give definitions about experts, amateurs and machine learning models in III-A. But the characteristics of the agents may change according to specific annotation scenarios. For example, in the medical image annotation scenario, amateurs may perform coarsegrained screening such as selecting the area which contains cancer cells before experts perform further classification. Moreover, we use LMNN as the machine learning model in our experiment, but it can also be changed to other metric learning models or other machine learning models according to the annotation needs. It will be interesting to explore different combinations of collaborative agents in the future.

# VII. CONCLUSION

In this paper, we propose a new framework of a costeffective annotation system which considers different cost ratios and annotates the dataset from scratch by combining experts, amateurs and machine learning models. We present an implementation of this framework called COCA. Extensive experiment on fine-grained datasets Stanford Dogs and CUB-200-2011 with both simulated and real amateurs shows that COCA is robust to different feature extractors and have efficient uncertainty-based annotation assignment strategies. Remarkably, when using SOTA fine-grained classification models as baseline automatic labeling method, COCA can outperform them when k is above a certain value. Moreover, COCA can also perform effectively on audio and text datasets, which shows COCA’s potential of generalizing to different annotation tasks.

# ACKNOWLEDGMENT

Lan Zhang is the corresponding author. The research is supported by National Key RD Program of China 2018YFB0803400China National Natural Science Foundation with No. 61822209No. No.61625205, No. 62132018, No. 61932016, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002.

# REFERENCES

[1] Cheng, Qimin, Zhang, Qian, Fu, Peng, Tu, Conghuan, Li, and Sen, “A survey and analysis on automatic image annotation,” Pattern Recognition, 2018.   
[2] J. Muhammadi, H. R. Rabiee, and S. A. Hosseini, “A unified statistical framework for crowd labeling,” Knowl. Inf. Syst., vol. 45, no. 2, pp. 271–294, 2015. [Online]. Available: https://doi.org/10.1007/s10115- 014-0790-7   
[3] J. Yang, J. Fan, Z. Wei, G. Li, T. Liu, and X. Du, “Cost-effective data annotation using game-based crowdsourcing,” Proceedings of the VLDB Endowment, vol. 12, no. 1, pp. 57–70, 2018.   
[4] C. Chai, G. Li, J. Li, D. Deng, and J. Feng, “Cost-effective crowdsourced entity resolution: A partial-order approach,” in Proceedings of the 2016 International Conference on Management of Data, 2016, pp. 969–984.

[5] J. Huang, W. Hu, Z. Bao, and Y. Qu, “Crowdsourced collective entity resolution with relational match propagation,” in 2020 IEEE 36th International Conference on Data Engineering (ICDE).   
[6] M. Kutlu, T. McDonnell, A. Sheshadri, T. Elsayed, and M. Lease, “Mix and match: collaborative expert-crowd judging for building test collections accurately and affordably,” arXiv preprint arXiv:1806.00755, 2018.   
[7] W. Callaghan, “A human-machine framework for the classification of phonocardiograms,” Master’s thesis, University of Waterloo, 2018.   
[8] G. Li, J. Wang, Y. Zheng, and M. J. Franklin, “Crowdsourced data management: A survey,” IEEE Transactions on Knowledge and Data Engineering, vol. 28, no. 9, pp. 2296–2319, 2016.   
[9] K. Q. Weinberger and L. K. Saul, “Distance metric learning for large margin nearest neighbor classification,” Journal of Machine Learning Research, vol. 10, no. 1, pp. 207–244, 2009.   
[10] M. B. Mayhew, B. Chen, and K. S. Ni, “Assessing semantic information in convolutional neural network representations of images via image annotation,” in IEEE International Conference on Image Processing, 2016.   
[11] J. Jin and H. Nakayama, “Annotation order matters: Recurrent image annotator for arbitrary length image tagging,” IEEE, 2017.   
[12] M. Yuan, L. Zhang, X.-Y. Li, and H. Xiong, “Comprehensive and efficient data labeling via adaptive model scheduling,” in 2020 IEEE 36th International Conference on Data Engineering (ICDE). IEEE, 2020, pp. 1858–1861.   
[13] M. Yuan, L. Zhang, X.-Y. Li, L.-Z. Yang, and H. Xiong, “Adaptive model scheduling for resource-efficient data labeling,” ACM Trans. Knowl. Discov. Data, vol. 16, no. 4, jan 2022. [Online]. Available: https://doi.org/10.1145/3494559   
[14] J. Deng, J. Krause, and F. Li, “Fine-grained crowdsourcing for finegrained recognition,” in IEEE Conference on Computer Vision and Pattern Recognition, 2013.   
[15] A. Drutsa, V. Fedorova, D. Ustalov, O. Megorskaya, E. Zerminova, and D. Baidakova, “Crowdsourcing practice for efficient data labeling: Aggregation, incremental relabeling, and pricing,” in SIGMOD/PODS ’20: International Conference on Management of Data, 2020.   
[16] J. Tu, G. Yu, C. Domeniconi, J. Wang, and X. Zhang, “Active multilabel crowd consensus,” CoRR, vol. abs/1911.02789, 2019. [Online]. Available: http://arxiv.org/abs/1911.02789   
[17] M. Gong, Y. Sun, and L. He, “A social network engaged crowdsourcing framework for expert tasks,” in 2019 IEEE 23rd International Conference on Computer Supported Cooperative Work in Design (CSCWD). IEEE, 2019, pp. 249–254.   
[18] A. Beaugnon, P. Chifflier, and F. Bach, “Ilab: An interactive labelling strategy for intrusion detection,” in International Symposium on Research in Attacks, Intrusions, and Defenses. Springer, 2017, pp. 120– 140.   
[19] C. Dai, S. Wang, Y. Mo, K. Zhou, E. Angelini, Y. Guo, and W. Bai, “Suggestive annotation of brain tumour images with gradient-guided sampling,” in International Conference on Medical Image Computing and Computer-Assisted Intervention. Springer, 2020, pp. 156–165.   
[20] Z. Li, Y. Yu, T. Wang, G. Yin, X. Mao, and H. Wang, “Haf: a hybrid annotation framework based on expert knowledge and learning technique,” Science China Information Sciences, vol. 65, no. 1, pp. 1–3, 2022.   
[21] A. Correia, S. Jameel, H. Paredes, B. Fonseca, and D. Schneider, “Hybrid machine-crowd interaction for handling complexity: Steps toward a scaffolding design framework,” in Macrotask Crowdsourcing. Springer, 2019, pp. 149–161.   
[22] W. Lee, C. H. Huang, C. W. Chang, M. K. D. Wu, K. T. Chuang, P. A. Yang, and C. C. Hsieh, “Effective quality assurance for data labels through crowdsourcing and domain expert collaboration,” in 21st International Conference on Extending Database Technology, EDBT 2018.   
[23] A. E. Mendez M ´ endez, M. Cartwright, and J. P. Bello, “Machine-crowd- ´ expert model for increasing user engagement and annotation quality,” in Extended Abstracts of the 2019 CHI Conference on Human Factors in Computing Systems, 2019, pp. 1–6.   
[24] A. T. Nguyen, B. C. Wallace, and M. Lease, “Combining crowd and expert labels using decision theoretic active learning,” in Third AAAI conference on human computation and crowdsourcing, 2015.   
[25] K. Li, G. Li, Y. Wang, Y. Huang, Z. Liu, and Z. Wu, “Crowdrl: An endto-end reinforcement learning framework for data labelling,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE).

[26] E. Krivosheev, F. Casati, M. Baez, and B. Benatallah, “Combining crowd and machines for multi-predicate item screening,” Proceedings of the ACM on Human-Computer Interaction, vol. 2, no. CSCW, pp. 1–18, 2018.   
[27] D. Masko and P. Hensman, “The impact of imbalanced training data for convolutional neural networks,” 2015.   
[28] B. Settles, Active Learning. Active Learning, 2012.   
[29] C. E. Shannon, “A mathematical theory of communication,” ACM SIGMOBILE mobile computing and communications review, vol. 5, no. 1, pp. 3–55, 2001.   
[30] A. Khosla, B. Y. Nityananda Jayadevaprakash, and L. Fei-Fei, “Novel dataset for fine-grained image categorization,” IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2011.   
[31] “Caltech-ucsd birds 200,” California Institute of Technology, 2010.   
[32] A. J. Joshi, F. Porikli, and N. Papanikolopoulos, “Multi-class active learning for image classification,” in IEEE Conference on Computer Vision and Pattern Recognition, 2009.   
[33] B. Settles, “Active learning literature survey,” 2009.   
[34] D. D. Lewis, “A sequential algorithm for training text classifiers: Corrigendum and additional data,” SIGIR Forum, vol. 29, no. 2, p. 1319, Sep. 1995.   
[35] J. He, J. Chen, S. Liu, A. Kortylewski, C. Yang, Y. Bai, C. Wang, and A. L. Yuille, “Transfg: A transformer architecture for fine-grained recognition,” CoRR, vol. abs/2103.07976, 2021.   
[36] P. Zhuang, Y. Wang, and Y. Qiao, “Learning attentive pairwise interaction for fine-grained classification,” CoRR, vol. abs/2002.10191, 2020.   
[37] W. Luo, X. Yang, X. Mo, Y. Lu, L. S. Davis, J. Li, J. Yang, and S. Lim, “Cross-x learning for fine-grained visual categorization,” CoRR, vol. abs/1909.04412, 2019.   
[38] R. Du, D. Chang, A. K. Bhunia, J. Xie, Y. Song, Z. Ma, and J. Guo, “Fine-grained visual classification via progressive multi-granularity training of jigsaw patches,” CoRR, vol. abs/2003.03836, 2020.   
[39] Z. Sun, C. Fan, Q. Han, X. Sun, Y. Meng, F. Wu, and J. Li, “Selfexplaining structures improve NLP models,” CoRR, vol. abs/2012.01786, 2020. [Online]. Available: https://arxiv.org/abs/2012.01786   
[40] J. Salamon and J. P. Bello, “Deep convolutional neural networks and data augmentation for environmental sound classification,” IEEE Signal Process. Lett., vol. 24, no. 3, pp. 279–283, 2017. [Online]. Available: https://doi.org/10.1109/LSP.2017.2657381