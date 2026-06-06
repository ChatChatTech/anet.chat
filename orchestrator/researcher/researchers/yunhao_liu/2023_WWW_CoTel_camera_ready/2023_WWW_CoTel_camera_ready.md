# CoTel: Ontology-Neural Co-Enhanced Text Labeling

Miao-Hui Song

songmiaohui@mail.ustc.edu.cn

University of Science and Technology of China

Hefei, China

Mu Yuan, Zichong Li, Qi Song

ym0813@mail.ustc.edu.cn

lzc123@mail.ustc.edu.cn

qisong09@ustc.edu.cn

University of Science and Technology of China

Hefei, China

# ABSTRACT

The success of many web services relies on the large-scale domainspecific high-quality labeled dataset. Insufficient public datasets motivate us to reduce the cost of data labeling while maintaining high accuracy in support of intelligent web applications. The rule-based method and the learning-based method are common techniques for labeling. In this work, we study how to utilize the rule-based and learning-based methods for resource-effective text labeling. We propose CoTel, the first ontology-neural co-enhanced framework for text labeling. We propose critical ontology extraction in the rule-based module and ontology-enhanced loss prediction in the learning-based module. CoTel can integrate explicit labeling rules and implicit labeling models and make them help each other to improve resource efficiency in text labeling tasks. We evaluate CoTel on both public datasets and real applications with three different tasks. With the same accuracy, CoTel can reduce 64.75% the time cost (a 2.84× speedup) and 62.07% labeling numbers of the baseline.

# KEYWORDS

text labeling, pseudo labeling, knowledge enhancement, active learning

# ACM Reference Format:

Miao-Hui Song, Lan Zhang, Mu Yuan, Zichong Li, Qi Song, and Yijun Liu, Guidong Zheng. 2023. CoTel: Ontology-Neural Co-Enhanced Text Labeling. In Proceedings of the ACM Web Conference 2023 (WWW ’23), May 1–5, 2023, Austin, TX, USA. ACM, New York, NY, USA, 10 pages. https: //doi.org/10.1145/3543507.3583533

∗Lan Zhang is the corresponding author.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

WWW ’23, May 1–5, 2023, Austin, TX, USA

© 2023 Copyright held by the owner/author(s). Publication rights licensed to ACM.

ACM ISBN 978-1-4503-9416-1/23/04. . . \$15.00

https://doi.org/10.1145/3543507.3583533

Lan Zhang∗

zhanglan@ustc.edu.cn

University of Science and Technology of China

Hefei, China

Institute of Artificial Intelligence

Hefei Comprehensive National Science Center

Hefei, China

Yijun Liu, Guidong Zheng

lyj\_mcfly@cmbchina.com

zhengguidong@cmbchina.com

China Merchants Bank

Shenzhen, China

# 1 INTRODUCTION

The large-scale labeled dataset is indispensable in web services, such as web information retrieval [16, 55], web recommendation systems [19, 22], web browsing [29, 36], etc. Typically, public datasets are insufficient for practical applications [27]. It is common that models trained on public datasets significantly degrade performance when migrating to a specific domain [4]. Typically, industrial applications train their model on their own data set to improve the quality of real-world services. However, it is expensive, labor-intensive, and time-consuming to obtain high-quality domainspecific datasets by manual labeling [54]. This motivates us to study how to reduce the cost of data labeling while achieving high accuracy.

As the outcome of ontology wisdom, domain-specific labeling rules can boost the performance of web applications. We did a survey in the data labeling department of a global bank and found that, for a new labeling task, they train annotators with labeling rules written in natural language. For example, to support intelligent Q&A in web customer service, they need to label question pairs [37]. In the training materials for annotators, there are rules like “a matched pair of questions must have the same date attribute”. Rule-based approaches are valued by the industry because of their interpretability and scalability [7, 43]. However, the rule-based methods are usually limited in their scope of coverage [7]. They are hard to adapt to a new domain [53] and require tedious manual labor [53].

Fortunately, the learning-based method can supplement these limitations. Learning based method can learn implicit semantics that is hard to be represented by logic rules [34]. For example, in the aforementioned training materials for annotators, we found requirements like “a matched pair of questions should be logical and consistent with meaning” that cannot be explicitly coded as a rule. But the learning-based method can help to learn representation. Fan et al. [15] show that learning-based methods are more effective than rule-based methods for checking similarities among user preferences and purchase histories on e-commerce platforms. However, the learning-based approach also has the limitation of requiring a large amount of labeled data for training [12, 59] and retraining for domain adaptation [7, 18].

![](images/c9e2882ca2f1ae0a3445458ec60f3e2aeaeca889a4031fe28503e56acfe5853d.jpg)



Figure 1: Overview of CoTel.

Both rule-based and learning-based methods have pros and cons, so extensive efforts have been devoted to designing the hybrid framework. According to the statistics [7], 67% of industrial information extraction is rule-based, 17% is learning-based, and 16% is the hybrid of both. Previous work [15] shows that the hybrid approaches can guarantee the correctness of order status on ecommerce platforms. In real-world applications, rule-based and learning-based methods are widely used for labeling but none is superb overall [15]. Hybrid approaches can take advantage of both methods.

Limitations. We classify the existing hybrid approaches into three categories. The first type [44] is a two-stage procedure that uses the rule-based method in the first stage and then uses the learning-based method. It is so naive that ignores the underlying correlation between the two methods, thus losing potential hidden optimization opportunities. The second series of approaches [6, 28, 30] measures the amount of information the sample contains by calculating the number of rules it covers. This method is suitable for datasets with large distinctions in the number of sample coverage (rules covered per sample). The last type [10, 13–15] aims to embed the learning-based model as a predicate in logic rules. This design broadens the representation scope of logic rules. However, if the annotation requirement cannot be formulated in the form of a logical rule, it still does not work.

With a design principle of combining rule-based (ontology) and learning-based (neuron) approaches, in this work, we aim to achieve high labeling accuracy while significantly reducing costs. And to address the limitations of existing work, we study how to improve labeling performance by ontology-neural co-enhancement. To achieve this goal, there are two challenges: (1) How to integrate explicit knowledge into query strategy? Effective query strategies need to measure the informativeness of unlabeled samples. The correlation between explicit knowledge in labeling rules and sample informativeness is unexplored. (2) How to leverage implicit neurons for rule generation? Learning-based labeling models optimize neurons by minimizing the prediction loss on training samples. The learned hidden parameters contain useful statistics for rule generation but only provide an implicit representation.

To tackle these challenges, we design both rule-based and learningbased labeling methods. As shown in Fig. 1, the rule-based module and the learning-based module are alternatively co-enhanced through ontology and neurons. We propose to extract critical ontologies and design a loss prediction approach with an extra ontology embedding. And we develop CoTel, the first ontology-neural CO-enhanced framework for TExt Labeling. Both the rule-based and learning-based modules in CoTel effectively reduce the labeling costs. We summarize the main contributions of this work as follows:

• We develop CoTel, the first ontology-neural co-enhanced framework for text labeling. CoTel integrates explicit labeling rules and implicit labeling models and improves resource efficiency in text labeling tasks.

• We design rule-based and learning-based methods for resourceeffective text labeling, in support of intelligent web applications. We propose critical ontology extraction in the rule-based module and ontology-enhanced loss prediction in the learning-based module.

• We conduct extensive evaluations of CoTel on both public datasets and real applications, which show the effectiveness of our ontology-neural co-enhanced design. Using the question-answering samples in a global bank’s production environment, experimental results show that CoTel outperforms existing labeling baselines. Under the same labeling budget, CoTel improves the labeling accuracy of the best baseline by 3.05%. With the same labeling accuracy, CoTel can reduce 64.75% the time cost (a 2.84× speedup) of the baseline.

This work does not raise any ethical issues.

# 2 RELATED WORK

# 2.1 Cost-Effective Data Labeling

There is a rich literature reducing the cost of data labeling, such as crowdsourcing [20], transfer learning [32, 47], and active learning [39]. Crowdsourcing refers to outsourcing the tasks of professional employees to other people in an open manner [20]. However, for data involving privacy or commercial secrets, it is not suitable to be labeled by amateurs in an open manner through crowdsourcing. Transfer learning aims to create high-performance models suitable for the target domain by transferring information from the source domain to avoid expensive data labeling costs [32, 47]. However, it is only applicable to those tasks which already have large labeled datasets or pre-trained models for the source domain. Active learning selects the most informative subset of samples to reduce labeling costs while still preserving high learning quality [39]. It is not limited by the availability of pre-trained models or labeled datasets in the source domain.

# 2.2 Ontology Schema

In the context of information science, an ontology defines a set of representations of discourse domains. Concept, property, and RDF (resource description framework) are three canonical representational primitives. Let $O \ = \ \{ C , P , R \}$ denote the ontology, where ??, ??, ?? refer to concepts, properties, and RDF1, respectively. For the intelligence Q&A service in a global bank, domain-specific concept nodes ?? represent the class of the fund, fund attributes, etc. Property ?? contains a set of edges that express the relation between two concept nodes. And $R = \{ ( c _ { i } , p , c _ { j } ) | c _ { i } , c _ { j } \in C , p \in P \}$ is the set of triple descriptors. For example, a triple (has\_fund\_manager, rdfs:subPropertyOf, has\_leader) (see Fig. 2b) represents that the concept has\_fund\_manager is a sub-property of the concept has\_leader. We visualize snapshots of ontology schemas used for two intelligent web services: user comment analysis (Fig. 2a) and customer service Q&A (Fig. 2b). A detailed description of datasets and tasks is given in Sec. 5.1.

![](images/594d23304e418a17c81b716616f91eb7567d1118b5ac317522d4495917e6ac95.jpg)



(a) Emotions of Web User Comments

![](images/82b3ad6a51fe1777a9952d285d5082bc3328d3b34cfac373b1054f4d988b4e39.jpg)



(b) Web Q&A for Customer Service in A Bank   
Figure 2: Ontology schemas of two tasks. (a) The hierarchical ontology schema of emotions built on web users’ online comments. (b) Example of ontology schema of a bank’s intelligent web Q&A for customer service.

# 2.3 Ontology-Enhanced Learning

There are many works [17, 49, 56] using ontology to enrich the priors and improve the performance of the target tasks. Parrott [33] proposes a three-level emotion hierarchy ontology to investigate how emotion influences social phenomena. Zhang et al. [56] propose an ontology-based context model to detect human emotional states for the wisdom web of things data cycle. To integrate ontology knowledge, Geng et al. [17] propose OntoZSL which uses ontological schema to enhance zero-shot learning in the web scenario. And Ye et al. [49] propose OntoPrompt which uses ontology-based knowledge injection to address knowledge missing issues in fewshot learning. For ontology-enhanced learning, it is critical to avoid negative knowledge that may lead to detrimental performance [49].

# 2.4 Hybrid Approach

The combination of rule-based and learning-based approaches is widely used in various scenarios, such as activity recognition [21, 44], entity enhancing [15], driver modeling [2], etc. For the entity enhancing task, Fan et al. [15] embed machine learning classifiers as predicates in logic rules to integrate learning-based and rule-based methods. On e-commerce platforms, previous work [7, 15] show that the rule-based method can be used as a supplement to machine learning models when checking the consistency of attributes with precise values, such as price. For the activity recognition task, inference rules are predefined by experts. The predefined activity categories are predicted by computing the logical entailment, while the remaining complex categories are predicted by learning-based approaches [44]. For the driver modeling task, Bhattacharyya et al. [2] propose a hybrid approach for modeling highway merging behavior. The logic rules determine whether to merge and the learning-based method determines when to merge.

Uniqueness. With this design principle, we present the first, to our best knowledge, rule-based and learning-based hybrid method for reducing the cost of text labeling. Furthermore, we design an ontology-neural co-enhanced framework that makes the rule-based and learning-based labeling methods work collaboratively.

# 3 PRELIMINARY

# 3.1 Rule Representation and Generation

To enable rule-based labeling, we use first-order logic (FOL) for rule representation [25] and use association rule generation mechanism [23]. FOL is a widely used knowledge representation language because of its simplicity and convenience [25]. There are four main types of FOL expressions: objects, attributes, relations, and functions [25]. Let $I = \{ I _ { 1 } , I _ { 2 } , . . . , I _ { m } \}$ denote a set of binary attributes, named items [1]. An association rule is defined in the form $X \Rightarrow Y$ , where ?? is the antecedent of the rule and ?? is the consequent of the rule [58]. $X , Y \subset I$ and $X \cap Y = \emptyset$ . This rule means that whenever ?? occurs in a dataset, then ?? occurs as well. The association rule can be used to model the correlations and co-occurrences between items [58]. There are two basic measures for association rules: support and confidence [23]. The support ?? is defined as the proportion of antecedent and consequent that occur together and the confidence ?? is defined as the conditional probability of the consequent given the antecedent [58]. Formally, given a rule $X \Rightarrow Y$ with support ?? and confidence $c , s ( X \Rightarrow Y ) = P ( X \cup Y )$ , $c ( X \Rightarrow Y ) = P ( Y | X )$ . For text labeling, we use association rule generation to generate labeling rules by finding the underlying correlations between ontologies and labels.

# 3.2 Learning-Based Pseudo-Labeling

Using a learning-based model (e.g., neural networks) to predict (pseudo labels) on unlabeled datasets is the learning-based pseudolabeling process. We define the learning-based model as the target model. The loss function [46] is critical for the effectiveness of learning the target model. A loss function is used to measure the difference between the model prediction $f _ { \theta } ( x )$ and the true label ?? . The typical learning objective has the following form: min?? $\begin{array} { r } { \frac { 1 } { N } \sum _ { i = 1 } ^ { N } L ( Y _ { i } , f _ { \theta } ( x _ { i } ) ) } \end{array}$ , where ?? is the number of training samples and ?? is a learnable parameter in the target model. Using gradient-based back-propagation algorithms, we can update the target model’s parameters to minimize the training loss. We illustrate the learning-based pseudo-labeling process using two scenarios as examples.

First, many recommendation algorithms for e-commerce platforms and web page browsing need to identify the preferences of users’ comments. Modern psychological theories of emotion propose the categorical psychological model with discrete basic emotions [33, 51]. So for text-based comments, we can label users’ emotions (or preferences) by learning emotion recognition models [40, 51]. Second, for the intelligent web Q&A for customer service in a bank, we need to label whether a question template matches a user query. We formulate this labeling task as a binary classification of question pairs, i.e., question matching [57]. Given a pair of questions, we can use a deep neural network to predict the matching pseudo label.

# 4 COTEL DESIGN

This section first presents an overview of the CoTel design $( \ S \ 4 . 1 )$ . Then rule-based module (§ 4.2) and learning-based module (§ 4.3) are presented in detail. And we explain how the two modules enhance each other for text labeling (§ 4.4).

# 4.1 Overview

Towards resource-effective labeling for text-based web applications, we propose a novel framework CoTel (ontology-neural COenhanced TExt Labeling) that consists of two main components: rule-based and learning-based modules. The end-to-end labeling task for CoTel is to assign a label to every samples in a given unlabeled dataset. As shown in Alg. 1, CoTel has a multi-round workflow in which two modules work alternately and co-enhance each other. In the learning-based module, we design an ontologyenhanced loss prediction model, named R-LossNet. R-LossNet guides the active sample selection for manual labeling and the selected samples will be used for the next round of rule generation. Formally, in the ??-th round, we define the unlabeled dataset as $U _ { n }$ and labeled dataset as $L _ { n } .$ Initially, we randomly select ?? samples for manual labeling. After that, CoTel first generates rules $R _ { n }$ based on currently labeled dataset and uses them to label unlabeled samples. These rules also derive critical ontologies $O _ { n } .$ Then CoTel uses manually labeled dataset $L _ { n }$ to train the target model $M _ { t a r g e t }$ and R-LossNet $M _ { R - L o s s N e t }$ . Note that, we do not leverage rule-labeled samples for training the target model, to avoid fitting issues caused by noise. Next, R-LossNet processes the unlabeled dataset and sorts samples by the order of their predicted loss values. CoTel selects ?? samples with the largest predicted loss for manual labeling. The above process repeats until reaching a certain cost budget (e.g., the number of manually labeled samples or time cost). In the end, CoTel uses the final-version target model to predict pseudo labels of the remaining unlabeled dataset.

We integrate explicit labeling rules and implicit labeling models into our CoTel and make them enhance each other to improve resource efficiency in text labeling tasks. We design critical ontology extraction in the rule-based module and ontology-enhanced loss prediction in the learning-based module.

# 4.2 Rule-Based Module

Through research on various text labeling tasks and communication with annotators working on the front line of the data labeling department, we found that: when a new labeling task comes, the annotators need to be trained. Typically, the training materials are some annotation rules written in natural language, provided by experts in related fields. Intuition tells us that there must be opportunities to save manual efforts in these labeling tasks. The

Algorithm 1: CoTel Algorithm   
Input:initial unlabeled dataset $U_{0}$ Result: manually labeled dataset $L_{n}$ , rule-labeled dataset $L_{n}^{R}$ , target model-labeled dataset $L_{n}^{M}$ 1 $L_{1}, U_{1} \leftarrow \text{Manual}(Random(U_{0}, K))$ ;

2 $n \leftarrow 1; // Initialization$ 3 repeat

4 $R_{n} \leftarrow \text{RuleGeneration}(L_{n})$ ;

5 $O_{n} \leftarrow R_{n}$ ;

6 $L_{n}^{R}, U_{n} \leftarrow R_{n}(U_{n}); // \text{Rule-Based Labeling}$ 7 $M_{target}, M_{R-LossNet} \leftarrow \text{Train}(L_{n}, O_{n})$ ;

8 $P_{loss} \leftarrow \{<u, M_{R-LossNet}(u, o) > |u \in U_{n}, o \in O_{n}\};$ 9 $n \leftarrow n + 1;$ 10 $L_{n}, U_{n} \leftarrow \text{Manual}(TopK(P_{loss})) ; // Active Sampling$ 11 until labeling cost reaches the budget;

12 $L_{n}^{M} \leftarrow M_{target}(U_{n})$ ;

13 return $L_{n}, L_{n}^{R}, L_{n}^{M}$

![](images/1680a31307f7edeb10044d287b06011940c4f8dfb3f0739e40ff3a93a81f6c14.jpg)



Figure 3: Workflow of the rule-based module. The ontology extraction component empowers the ontology-enhanced query strategy (§ 4.4).

challenge is how to transform human annotators’ labeling behaviors into automated program.

⊲ Insight-1: We can generate explicit labeling rules from the behavior of human annotators.

As shown in Fig. 3, the rule-based module in CoTel has three main functionalities: rule generation, rule labeling, and ontology extraction.

Rule generation. Given a text sample for labeling, we first extract items from words in the text. Recall that, items are binary attributes in FOL expressions. Then we formalize the rule-based labeling as a function that maps the set of items $I = \{ I _ { 1 } , . . . , I _ { m } \}$ to the predefined label space $Y = \{ y _ { 1 } , y _ { 2 } , . . . , y _ { k } \}$ .

Definition 1 (Labeling Rule). A labeling rule has the form:

$$
\left\{I _ {i} \wedge \dots \wedge I _ {j} \right\} \longrightarrow y, \tag {1}
$$

where $1 \leq i , j \leq$ ?? and $y \in Y .$ .

The antecedent (set of items) in the rule is the mixture of the ontology and properties of the input text. We can obtain the ontology schema (Fig. 2 shows two examples) from experts or existing works [51, 56]. For example, to label texts for the emotion recognition task, the antecedent can be some adjectives that express emotions. When we want to label whether a pair of questions match, the antecedent can be the date property (derived from the requirement in the annotators’ training material: “a matched pair of questions must have the same date attribute”). The consequent of the rule is a predefined label, e.g., the “happy” and “sad” emotions. Using manually labeled samples, denoted by $L _ { n } ,$ we can automatically generate explicit labeling rules. We use association rule generation to generate the set of rules $R _ { n }$ . Specifically, we adopt the canonical Apriori [23] algorithm for association rule generation. Our proposed method is not limited by rule mining algorithms and it also supports other rule generation algorithms. In this way, we obtain rules $R _ { n }$ available for text labeling.

Entailment calculation for rule labeling. Once rules $R _ { n }$ are generated, we can use them for text labeling by calculating the entailment in FOL. Intuitively, the entailment means that if a sample satisfies the antecedent (set of items) of a rule, it also fulfills the consequent (label) of the rule.

Definition 2 (Applicable Rule). A labeling rule $\{ I ^ { \prime } \to y \} , I ^ { \prime } \subseteq \mathbb { 1 }$ is applicable to the text ?? if

$$
\forall I _ {i} \in I ^ {\prime}, I _ {i} \in x. \tag {2}
$$

We define the samples labeled by their applicable rules as $L _ { n } ^ { R } .$

# 4.3 Learning-Based Module

Except for rules that can be explicitly represented, there are still some requirements are hard to be represented in the FOL structure. Fortunately, deep neural networks (DNNs) achieve state-of-the-art performance in learning representation for many tasks [16, 29]. So we are motivated to integrate a learning-based model into our labeling pipeline as a supplement to the rules. However, these deep models typically require a large number of training samples. The challenge is how to efficiently utilize learning-based models for our text labeling tasks, with a key goal to reduce the labeling cost.

⊲ Insight-2: We can learn implicit labeling models from textlabel samples annotated by human.

Active learning. To reduce data labeling costs, active learning (AL) [39] is a widely used technique. It selects the most informative samples from the unlabeled dataset and queries for manual labeling. The core of active learning is the query strategy. Uncertainty-based query strategy [26, 39] is simple and widely applied. But for complex tasks, such as Named Entity Recognition [5] and relation extraction [54], the uncertainty measurement needs to be redefined case by case [31]. We expect a task-agnostic framework for general text labeling tasks, so we present a loss prediction-based query strategy.

Loss prediction. DNNs learn to optimize parameters by minimizing a loss function [35]. Although learning-based models could have different loss functions, their loss value is a task-agnostic scalar. Therefore, we choose loss as the measurement for the informativeness of unlabeled samples. Previous work [42, 48, 50] in computer vision have experimentally evaluated the effectiveness of the AL query strategy based on predicted loss values. “\*-+They employ a lightweight loss prediction model in the target model and select samples with the highest predicted loss values as informative samples [24, 48]. Following this design principle, we present the first loss prediction module for the text labeling tasks to get a general and task-agnostic query strategy.

LossNet design. Given a neural network target model, we attach a lightweight regression branch, named LossNet, for loss prediction. Given a sample ??, the target model $M _ { t a r g e t }$ predicts the pseudo label $\hat { y } = M _ { t a r g e t } ( x )$ . LossNet’s inputs consist of multiple middle layers (denoted by ?? ) in the target model. With the ground truth label ?? of ?? given by the human annotator, the target loss can be calculated by ${ l } _ { t } ~ = ~ L _ { t a r q e t } ( y , \hat { y } )$ . The specific formulation of $L _ { t a r g e t }$ depends on the labeling task (e.g., binary cross-entropy for binary classification). The target loss $l _ { t }$ is the ground-truth of the loss prediction branch. The loss-prediction loss is calculated by $l _ { l } = L _ { l o s s } ( l _ { t } , M _ { L o s s N e t } ( f ( x ) ) )$ , where $L _ { l o s s }$ is a common loss function in existing work [50]. The end-to-end loss is a combination of two loss functions $L _ { t a r g e t }$ and $L _ { l o s s } { \mathrm { : } }$

$$
\begin{array}{l} \mathcal {L} = l _ {t} + \lambda \cdot l _ {l} \\ = L _ {\text { t   a   r   g   e   t }} \left(y, M _ {\text { t   a   r   g   e   t }} (x)\right) + \lambda \cdot L _ {\text { l   o   s   s }} \left(l _ {t}, M _ {\text { L   o   s   s   N   e   t }} (f (x))\right), \tag {3} \\ \end{array}
$$

where ?? is a hyper-parameter. In our experiments, we follow the parameter setting of previous work [24, 48] and choose ?? = 1. A key design is how to select the middle layers in the shared block to get the features for loss prediction. Typically, we can divide the target model into feature extraction block and task prediction block [32, 60]. The feature extraction block learns a general embedding of the objects and the task prediction block learns the task-specific behaviors [60]. Therefore, we propose to select layers from both two blocks. Then we concatenate their outputs as the input for loss prediction. Details about layer selection in specific tasks are presented in implementation configurations (§ 5.1).

# 4.4 Ontology-Neural Co-Enhancement

The proposed two labeling modules work independently. To take full advantage of both rule-based and learning-based labeling, the challenge is how to make these heterogeneous labeling agents work collaboratively. We will introduce how rules can help active learning (critical ontology extraction & ontology-based loss prediction) and how learning can help rule generation (neural-enhanced rule generation).

⊲ Insight-3: We can make the explicit labeling rules and implicit labeling models help each other.

Critical ontology extraction. In addition to directly labeling text by generated rules, we can also extract ontologies that will boost the performance of the learning-based module in CoTel. The inherent interpretability of a rule is attributed to the fact that it explicitly gives a clear and direct semantic relationship between antecedent and consequent. From the generated rules we find that, in the same task, the antecedents of the rules are usually composed of ontologies with the same grammatical category. Therefore, we regard the grammatical category that occurs most frequently in the rule antecedent as the critical grammatical category. The ontologies with the critical grammatical category in text are defined as critical ontology. These critical ontologies play an important role in the rule-based method as they represent the features most concerned. And we use critical ontologies as guidance for the learning-based module (§ 4.4).

![](images/e8b776f85504637614047ff5b01903d80a79e09a28bac28b4df9cb3e40964572.jpg)



Figure 4: Pipeline of ontology-enhanced pseudo-labeling.

Ontology-based loss prediction. We observe that there are some hints in generated rules that can help the active learning module to select informative samples. As introduced in aforementioned, we can derive critical ontologies from rules. As shown in Fig. 4, to integrate the knowledge of critical ontologies into the learning-based module, we first use the feature extraction block in the target model to generate the embedding $( e m b _ { O } )$ of critical ontologies. Then we concatenate this embedding with the original features from selected middle layers as the new input for loss prediction. Formally, this ontology-enhanced loss prediction branch, named R-LossNet, is defined as $M _ { R - L o s s N e t } ( [ f ( x ) , e m b _ { O } ] )$ ). So the new loss-prediction loss function is:

$$
l _ {R l} = L _ {\text { loss }} (l _ {t}, M _ {R - \text { LossNet }} ([ f (x), e m b _ {O} ])). \tag {4}
$$

Therefore, the end-to-end loss function is $\mathcal { L } _ { R } = l _ { t } + \lambda \cdot l _ { R l }$ . R-LossNet shares the same training mechanism as LossNet. The upper part of Fig. 4 shows the pipeline of our ontology-enhanced R-LossNet. Experimental results (§ 5.3) show that the integrated critical ontologies bring significant improvement to the loss learning.

Neural-enhanced rule generation. On the other hand, our learning-based module actively selects samples for manually labeling $\left( L _ { n } \right)$ . As shown in Fig. 4, we can obtain samples with pseudo labels $( L _ { n } ^ { M } )$ predicted by the target model. To improve the reliability of pseudo labels, we filter samples with a threshold of the prediction confidence, i.e., ?????? ?? (??ˆ) > ?? where ?? is the confidence threshold. Then we merge the manually labeled samples with high-confidence pseudo-labeled samples for rule re-generation. The lower part in Fig. 4 shows the workflow of the neural-enhanced rule generation.

Discussions. Cotel can work on text labeling because of its grammatical structure. There are existing works [41, 52] in the visual area to improve image classification based on scene graphs. Cotel can use the rules in scene graphs to exploit the potential of improving the efficiency of labeling.

# 5 EVALUATION

We implemented CoTel 2 in Python 3.7 by TensorFlow 2.4. This section presents the evaluation of CoTel on three different text labeling tasks that are important to support intelligent web applications, i.e., question matching for customer service Q&A, emotion recognition for web recommendation and itent classification for web search query.

# 5.1 Experiment Setup

Datasets. We evaluate CoTel on both public datasets and question pairs collected from a global bank’s intelligent customer service system. (1) Emotion [38], a dataset for the text-based emotion recognition task from Twitter, which plays an important role in support of web recommendation [19, 22, 38]. It provides six basic emotion labels in English. We randomly select 500 samples as the initially labeled dataset. In each round of the active learning process, we add 100 samples to the labeled dataset. (2) BankQM , a dataset of 30,000 pairs of questions and matching labels in the form of $\{ ( q 1 , q 2 ) , l a b e l \}$ . To support intelligent customer service in a global bank, question matching techniques are employed to return answers from a database of question-to-answer records. The efficiency and quality of question matching labeling are critical for this web service. In our experiments, we initially randomly select 1000 samples for manual annotators to label and select 500 samples in each round using active query strategies. (3) hate\_speech18 [9], a dateset labeled as containing hate speech or not. We randomly select 1000 samples from each category of hate and no-hate for experiments. We initially randomly select 100 samples and then query 100 samples in each round of active learning.

Target models. Recall that we define the learning-based pseudolabeling model as the target model. (1) For the emotion recognition and intent classification tasks, we fine-tuned two dense layers based on a pre-trained BERT model [11, 45] implemented by Tensor-Flow Hub. (2) For the question matching task, we trained an ICE model [57] which consists of two main blocks: embedding block and classification block. The embedding block is built with bidirectional LSTM [8] and the classification block has only fully-connected layers.

R-LossNet configurations. Our proposed R-LossNet (§ 4.4) needs to configure the connected hidden layers and ontology embedding. (1) For the BERT-based model used in the emotion recognition task and intent classification task, we choose the second last layer of the target model. (2) For the ICE model used in the question matching task, we choose two hidden layers from the classification block: the first and the second last dense layers. These two layers represent the learned embedding and task-specific features for classification, respectively. For all tasks, we use the identical target model for ontology embedding. And to minimize the computational costs, we implement the loss prediction module using lightweight dense layers.

Baselines. We employ three baselines for comparison. (1) Random: Randomly select ?? samples for manual labeling in each sampling round; (2) Conf [39]: Select ?? samples with the lowest prediction confidence for manual labeling in each sampling round; (3) LossNet [50]: Select ?? samples with the highest predicted loss for manual labeling in each sampling round.

Device. For all experiments, we use a server that runs Ubuntu 20.04.1 with one NVIDIA GTX 1080 Ti GPU and 12 Intel Core i7-5930K CPUs.

# 5.2 Overall Performance

Evaluation Methodology and Metrics. We evaluate the end-toend labeling accuracy of CoTel on the three tasks, under different budgets of labeling efforts and time cost. Both labeling efforts and time costs are major concerns. The labeling efforts refer to the number of manually labeled samples. The time cost refers to the end-to-end labeling time to get the labeled dataset. CoTel includes five main time costs: manual labeling time, target model’s training / prediction / sampling time, and rule generation and labeling time. Manual labeling time refers to the time for human annotators.

![](images/868f726b3b89f8ed8902dea5fdd7c5ac74081867cb8029bda2b91f2b43af41a8.jpg)



(a) Emotion Recognition

![](images/4bddbb2d1f66cfdd876b07fa04151daca63956e8c804dde1a0cf2a8ac4bec3dc.jpg)



(b) Question Matching   
Figure 5: Comparison of end-to-end labeling accuracy on two tasks.

Labeling efforts as the cost. As shown in Fig. 5, CoTel outperforms baselines in every round of labeling on all tasks. Specifically, for emotion recognition, in the 15th round (1500 samples), CoTel achieves 91.25% accuracy which is 5.6% / 4.25% / 3.05% higher than Random / Conf / LossNet baselines, respectively. And for question matching, in the 7th round (4500 samples), CoTel achieves 97.38% accuracy which is 6.7% / 4.4% / 2.45% higher than Random / Conf / LossNet baselines, respectively. And for intent classification, in the 5th round (600 samples), CoTel achieves 83.2% accuracy which is 7.3% / 4.0% / 3.5% higher than Random / Conf / LossNet baselines, respectively. On the other hand, we report the required labeling effort for achieving a certain accuracy target in Fig. 6. Experimental results show that CoTel significantly decreases the labeling efforts when achieving the same target accuracy. And for question matching (Fig. 6b), given the 98% accuracy target, CoTel requires 5500 samples, which is 18.3% of the total dataset. Compared with Random / Conf / LossNet baselines that require 14,500 / 12,000 / 7,500 samples, CoTel saves 62% / 54.17% / 26.67% labeling efforts, respectively. The numbers of labeled samples when the advantage disappears are as follows. For emotion recognition, the LossNet / Conf / Random baselines’ numbers are 3400 / 3700 / 5400. For question matching, the LossNet / Conf / Random baselines’ numbers are 12,500/15,000/19,000.

Time as the cost. In real-world labeling pipelines, like the question matching task for the web Q&A application, the time cost is a critical metric. We invited 10 people who work in the data labeling department for speed estimation of manual labeling. And results show that it takes 8 seconds on average for an annotator to label a pair of questions. We use this time cost (8s per sample) in the following reported results. For the target model’s costs, we configure a batch size of 32 and 15 epochs per sampling round. We set the target accuracy as 98%. Note that, since the public dataset has already been labeled and we cannot accurately estimate their annotators’ labeling speed, we only consider the question matching task. As shown in Fig. 7a, CoTel significantly reduces the end-to-end time

![](images/b975481f614f5b51535e57dd4ce6d38685707edb381136453bbc4628d3d13beb.jpg)



(a) Emotion Recognition

![](images/10a00b06ada028fab15054a06ac2334eb86e1cd0ee0df26e882f5e7d16c43a65.jpg)



(b) Question Matching

Figure 6: Trade-off between labeling efforts and labeling accuracy on two tasks.   
![](images/6c663899357ad50f90c832eb0aa24dbd51bcebbeb86916cb5bb6b599ef47d752.jpg)



(a) End-to-end Time Cost

![](images/21a7ff41b075af0cc3fb1d49d61a55b6e5ca1816359240fb79971bfd11bc52c8.jpg)



(b) Time Profiling of CoTel.   
Figure 7: Time costs on labeling the question matching task with a target of 98% accuracy. (a) “Model” denotes the sum of target model’s and rule-based module’s time costs.

Table 1: Labeling accuracy given the same time cost on question matching task. The best accuracy is in bold. The gain compared to the best baselines is in red. 

<table><tr><td>Time (hour)</td><td>Random</td><td>Conf</td><td>LossNet</td><td>CoTEL</td></tr><tr><td>6</td><td>88.75</td><td>90.00</td><td>91.91</td><td>94.23 (+2.32)</td></tr><tr><td>12</td><td>91.01</td><td>93.39</td><td>95.84</td><td>97.88 (+2.04)</td></tr><tr><td>20</td><td>93.18</td><td>96.61</td><td>98.77</td><td>99.41 (+0.64)</td></tr></table>

cost of text labeling. Moreover, compared with manual labeling, the additional costs brought by CoTel only account for 3.84% of the time. Specifically, Random requires 34.7 hours to achieve the target labeling accuracy. Compared with Random, Conf reduces 6.3 hours of time cost and LossNet further reduces 12.1 hours. CoTel outperforms all baselines and requires only 12.69 hours, saving 3.57 hours compared with the best baseline LossNet. We also test the time profiling of CoTel’s modules (see Fig. 7b). Results show that CoTel spent a total of 1690s and the training time of the target model accounts for the largest proportion (62.9%).

On the other hand, we report the labeling accuracy achieved by different approaches, given the same budget of time cost in Tab. 1. CoTel outperforms baselines with all time budgets. For example, given 6 hours, Random can only achieve 88.75% accuracy and Conf / LossNet improves it to 90.0% / 91.91%, respectively. CoTel achieves 94.23% labeling accuracy, 2.32% higher than the best baseline.

![](images/ae298335a342b17add95c3c22c717b404d1ca7ac06bfa7d43eb455e3c96af7e5.jpg)



(a) Emotion Recognition

![](images/7e5b96e387e5da2176a17c8176eb94bf12b0839960589fa5797d3d4ca63f6222.jpg)



(b) Question Matching

Figure 8: The gain of different query strategies in terms of labeling accuracy on two tasks.   
![](images/bd713904411c9129844f3df12ed0634cbb70d10ca0b8acff3ba25f19841023ec.jpg)



(a) Loss prediction accuracy on intent classification task.

![](images/2114da273e4c068e1a1518849e0282c1270af471af07a455f64ace4c43ce90d1.jpg)



(b) Pearson Coefficient on emotion recognition task.   
Figure 9: Effectiveness of the loss prediction module.

# 5.3 Micro-Benchmarks

Query strategy. To evaluate the performance of the query strategies singly, we integrate Random, Conf, and LossNet baselines with our proposed rule-based labeling module (denoted by w/ RuL). Fig. 8 shows the corresponding between the labeling effort reduction and the labeling accuracy gain. The values of reduction and gain are compared with the Random w/ RuL approach. Experimental results show that our proposed R-LossNet outperforms all baselines. And for emotion recognition, we get the largest accuracy gain when the labeling reduction factor is around 90% (see Fig. 8a). For question matching, the peak of accuracy gains is at around 80% reduction of labeling effort (see Fig. 8b).

Loss ranking accuracy. We adopt loss ranking accuracy [50] (Loss Acc) as the evaluation metric of the loss prediction module. Given a pool of samples, the loss prediction module sorts them by predicted loss values. If the predicted rank equals the true rank between two samples, this metric considers true. As shown in Fig. 9a, our proposed R-LossNet improves the loss ranking accuracy. It indicates that ontology-based knowledge help to improve the accuracy of the loss prediction. On the overall trend, the loss ranking accuracy increases with the number of labeled samples.

Correlation. Following related work [50], we visualize the Pearson coefficient [3] between predicted loss and target loss as the number of labeled data increases. For the emotion recognition task, we evaluate the correlations on 2000 samples and plot them in Fig. 9b. We can find that the predicted loss becomes more correlated with the target loss with the increase of labeled samples. And our proposed R-LossNet has a better loss-prediction performance compared to LossNet. We conclude that our proposed ontology enhancement effectively improves loss learning, thus achieving higher labeling accuracy in the active process.

![](images/6372d3372ae1c7bac18ca624b2dabe1d95c1d9dc6911ac0ed757ed73e19df66d.jpg)



(a) Emotion Recognition

![](images/25aef6fc9bbcfbb8f8332a0e6c40cb814aba8ad7290385d389ff8798a008a5cb.jpg)



(b) Question Matching   
Figure 10: Comparison of labeling accuracy on two tasks with and without the rule-based module.

# 5.4 Ablation Study

Removing the learning-based module. Removing the learningbased module from CoTel results in a single rule-based labeling approach. For the emotion recognition task, in the 25th round, generated rules can filter 14.75% of unlabeled samples, and the accuracy of these rules is 98.64%. For the question matching task, in the 20th round, rules (provided by annotators) can filter 12.6% of unlabeled samples, and the accuracy of these rules is 99.12%. In summary, only using our rule-based approach achieves high accuracy (98.64% and 99.12%) but the amount of samples that can be covered is limited (14.75% and 12.6%). The results illustrate the need to supplement the rules with a learning-based module.

Removing the rule-based module. When removing the rulebased module from CoTel, only the learning-based module is in play. We compare our method with Random, Conf, and LossNet baselines. As shown in Fig. 10, the dashed lines represent the labeling accuracy only using learning-based methods and the solid lines represent combined rule-and-learning-based methods. Experimental results show that removing the rule-based module brings non-negligible performance degradation on both tasks. Also, the worse the baseline’s performance, the more gain this rule-based module brings. And the gain decreases as the number of labeled samples increases. For emotion recognition, combining the rulebased module can improve the accuracy by 0.5% to 1.45%. And for question matching, the combination brings 0.8% to 1.85% accuracy improvement.

# 6 CONCLUSION AND FUTURE WORK

This paper studies how to make ontology (rule-based method) and neural (learning-based method) co-enhanced to improve the cost efficiency of text labeling. We leverage previously ignored optimization opportunities to improve resource efficiency in text labeling tasks. In the future, we plan to extend CoTel to labeling tasks with more data modalities, like multimedia and knowledge graph.

# ACKNOWLEDGMENTS

This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, and “the Fundamental Research Funds for the Central Universities” WK2150110024.

# REFERENCES

[1] Rakesh Agrawal, Tomasz Imieliński, and Arun Swami. 1993. Mining association rules between sets of items in large databases. In Proceedings of the 1993 ACM SIGMOD international conference on Management of data. 207–216.   
[2] Raunak Bhattacharyya, Soyeon Jung, Liam A Kruse, Ransalu Senanayake, and Mykel J Kochenderfer. 2021. A Hybrid Rule-Based and Data-Driven Approach to Driver Modeling Through Particle Filtering. IEEE Transactions on Intelligent Transportation Systems (2021).   
[3] Richard Boddy and Gordon Smith. 2009. Statistical methods in practice: for scientists and technologists. John Wiley & Sons.   
[4] Tingting Cai, Zhiyuan Ma, Hong Zheng, and Yangming Zhou. 2021. NE–LP: normalized entropy-and loss prediction-based sampling for active learning in Chinese word segmentation on EHRs. Neural Computing and Applications 33, 19 (2021), 12535–12549.   
[5] Haw-Shiuan Chang, Shankar Vembu, Sunil Mohan, Rheeya Uppaal, and Andrew McCallum. 2020. Using error decay prediction to overcome practical issues of deep active learning for named entity recognition. Machine Learning 109, 9 (2020), 1749–1778.   
[6] Huizhong Chen, Andrew Gallagher, and Bernd Girod. 2012. Describing clothing by semantic attributes. In Computer Vision–ECCV 2012: 12th European Conference on Computer Vision, Florence, Italy, October 7-13, 2012, Proceedings, Part III 12. Springer, 609–623.   
[7] Laura Chiticariu, Yunyao Li, and Frederick R. Reiss. 2013. Rule-Based Information Extraction is Dead! Long Live Rule-Based Information Extraction Systems!. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Seattle, Washington, USA, 827–832. https://aclanthology.org/D13-1079   
[8] Zhiyong Cui, Ruimin Ke, Ziyuan Pu, and Yinhai Wang. 2018. Deep bidirectional and unidirectional LSTM recurrent neural network for network-wide traffic speed prediction. arXiv preprint arXiv:1801.02143 (2018).   
[9] Ona de Gibert, Naiara Perez, Aitor García-Pablos, and Montse Cuadros. 2018. Hate Speech Dataset from a White Supremacy Forum. In Proceedings of the 2nd Workshop on Abusive Language Online (ALW2). Association for Computational Linguistics, Brussels, Belgium, 11–20. https://doi.org/10.18653/v1/W18-5102   
[10] Ting Deng, Wenfei Fan, Ping Lu, Xiaomeng Luo, Xiaoke Zhu, and Wanhe An. 2022. Deep and Collective Entity Resolution in Parallel. In 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 2060–2072.   
[11] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805 (2018).   
[12] Majigsuren Enkhsaikhan, Wei Liu, Eun-Jung Holden, and Paul Duuring. 2021. Auto-labelling entities in low-resource text: a geological case study. Knowledge and Information Systems 63 (2021), 695–715.   
[13] Wenfei Fan. 2022. Big graphs: challenges and opportunities. Proceedings of the VLDB Endowment 15, 12 (2022), 3782–3797.   
[14] Wenfei Fan, Ziyan Han, Yaoshu Wang, and Min Xie. 2022. Parallel Rule Discovery from Large Datasets by Sampling. In Proceedings of the 2022 International Conference on Management of Data. 384–398.   
[15] Wenfei Fan, Ping Lu, and Chao Tian. 2020. Unifying logic rules and machine learning for entity enhancing. Science China Information Sciences 63, 7 (2020), 1–19.   
[16] Chenchen Feng, Yu He, Shiyang Wen, Guojun Liu, Liang Wang, Jian Xu, and Bo Zheng. 2022. DC-GNN: Decoupled Graph Neural Networks for Improving and Accelerating Large-Scale E-commerce Retrieval. In Companion Proceedings of the Web Conference 2022. 32–40.   
[17] Yuxia Geng, Jiaoyan Chen, Zhuo Chen, Jeff Z Pan, Zhiquan Ye, Zonggang Yuan, Yantao Jia, and Huajun Chen. 2021. OntoZSL: Ontology-enhanced zero-shot learning. In Proceedings of the Web Conference 2021. 3325–3336.   
[18] Daniele Di Grandi. 2022. ProbQL: A Probabilistic Query Language for Information Extraction from PDF Reports and Natural Language Written Texts. Master’s thesis.   
[19] Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 2017. Neural collaborative filtering. In Proceedings of the 26th international conference on world wide web. 173–182.   
[20] Jeff Howe et al. 2006. The rise of crowdsourcing. Wired magazine 14, 6 (2006), 1–4.   
[21] Mostafa S Ibrahim, Srikanth Muralidharan, Zhiwei Deng, Arash Vahdat, and Greg Mori. 2016. A hierarchical deep temporal model for group activity recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition. 1971–1980.   
[22] Houye Ji, Junxiong Zhu, Chuan Shi, Xiao Wang, Bai Wang, Chaoyu Zhang, Zixuan Zhu, Feng Zhang, and Yanghua Li. 2021. Large-scale comb-k recommendation. In Proceedings of the Web Conference 2021. 2512–2523.   
[23] T Karthikeyan and N Ravikumar. 2014. A survey on association rule mining. International Journal of Advanced Research in Computer and Communication Engineering 3, 1 (2014), 2278–1021.   
[24] Ildoo Kim, Younghoon Kim, and Sungwoong Kim. 2020. Learning loss for testtime augmentation. Advances in Neural Information Processing Systems 33 (2020),

4163–4174.   
[25] Hector J Levesque. 1986. Knowledge representation and reasoning. Annual review of computer science 1, 1 (1986), 255–287.   
[26] David D Lewis. 1995. A sequential algorithm for training text classifiers: Corrigendum and additional data. In Acm Sigir Forum, Vol. 29. ACM New York, NY, USA, 13–19.   
[27] Jia Li and Dandan Song. 2022. Uncertainty-aware Pseudo Label Refinery for Entity Alignment. In Proceedings of the ACM Web Conference 2022. 829–837.   
[28] Roberto Lourenco Jr, Adriano Veloso, Adriano Pereira, Wagner Meira Jr, Renato Ferreira, and Srinivasan Parthasarathy. 2014. Economically-efficient sentiment stream analysis. In Proceedings of the 37th international ACM SIGIR conference on Research & development in information retrieval. 637–646.   
[29] Yun Ma, Dongwei Xiang, Shuyu Zheng, Deyu Tian, and Xuanzhe Liu. 2019. Moving deep learning into web browser: How far can we go?. In The World Wide Web Conference. 1234–1244.   
[30] Mariane Moreira, Jefersson A dos Santos, and Adriano Veloso. 2014. Learning to rank similar apparel styles with economically-efficient rule-based active learning. In Proceedings of International Conference on Multimedia Retrieval. 361–368.   
[31] Vu-Linh Nguyen, Mohammad Hossein Shaker, and Eyke Hüllermeier. 2022. How to measure uncertainty in uncertainty sampling for active learning. Machine Learning 111, 1 (2022), 89–122.   
[32] Sinno Jialin Pan and Qiang Yang. 2009. A survey on transfer learning. IEEE Transactions on knowledge and data engineering 22, 10 (2009), 1345–1359.   
[33] W Gerrod Parrott. 2001. Emotions in social psychology: Essential readings. psychology press.   
[34] Andrew Pavlo, Erik Paulson, Alexander Rasin, Daniel J Abadi, David J DeWitt, Samuel Madden, and Michael Stonebraker. 2009. A comparison of approaches to large-scale data analysis. In Proceedings of the 2009 ACM SIGMOD International Conference on Management of data. 165–178.   
[35] Samira Pouyanfar, Saad Sadiq, Yilin Yan, Haiman Tian, Yudong Tao, Maria Presa Reyes, Mei-Ling Shyu, Shu-Ching Chen, and Sundaraja S Iyengar. 2018. A survey on deep learning: Algorithms, techniques, and applications. ACM Computing Surveys (CSUR) 51, 5 (2018), 1–36.   
[36] Yuanyuan Qiao, Yuewei Wu, Fan Duo, Wenhui Lin, and Jie Yang. 2019. Siamese neural networks for user identity linkage through web browsing. IEEE transactions on neural networks and learning systems 31, 8 (2019), 2741–2751.   
[37] Minghui Qiu, Liu Yang, Feng Ji, Wei Zhou, Jun Huang, Haiqing Chen, W Bruce Croft, and Wei Lin. 2018. Transfer Learning for Context-Aware Question Matching in Information-seeking Conversations in E-commerce. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers). 208–213.   
[38] Elvis Saravia, Hsien-Chi Toby Liu, Yen-Hao Huang, Junlin Wu, and Yi-Shin Chen. 2018. CARER: Contextualized Affect Representations for Emotion Recognition. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, 3687– 3697. https://doi.org/10.18653/v1/D18-1404   
[39] Burr Settles. 2009. Active learning literature survey. (2009).   
[40] Shadi Shaheen, Wassim El-Hajj, Hazem Hajj, and Shady Elbassuoni. 2014. Emotion recognition from text based on automatically generated rules. In 2014 IEEE International Conference on Data Mining Workshop. IEEE, 383–392.   
[41] Sahand Sharifzadeh, Sina Moayed Baharlou, and Volker Tresp. 2021. Classification by attention: Scene graph classification with prior knowledge. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 35. 5025–5033.   
[42] Megh Shukla and Shuaib Ahmed. 2021. A mathematical analysis of learning loss for active learning in regression. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 3320–3328.   
[43] Firdaus Solihin and Indra Budi. 2018. Recording of law enforcement based on court decision document using rule-based information extraction. In 2018 International Conference on Advanced Computer Science and Information Systems (ICACSIS). IEEE, 349–354.   
[44] Abdul Syafiq Abdull Sukor, Ammar Zakaria, Norasmadi Abdul Rahim, Latifah Munirah Kamarudin, Rossi Setchi, and Hiromitsu Nishizaki. 2019. A hybrid approach of knowledge-driven and data-driven reasoning for activity recognition in smart homes. Journal of Intelligent & Fuzzy Systems 36, 5 (2019), 4177–4188.   
[45] Iulia Turc, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. Well-Read Students Learn Better: On the Importance of Pre-training Compact Models. arXiv preprint arXiv:1908.08962v2 (2019).   
[46] Qi Wang, Yue Ma, Kun Zhao, and Yingjie Tian. 2022. A comprehensive survey of loss functions in machine learning. Annals of Data Science 9, 2 (2022), 187–212.   
[47] Karl Weiss, Taghi M Khoshgoftaar, and DingDing Wang. 2016. A survey of transfer learning. Journal of Big data 3, 1 (2016), 1–40.   
[48] Xing Wu, Cheng Chen, Mingyu Zhong, Jianjia Wang, and Jun Shi. 2021. COVID-AL: The diagnosis of COVID-19 with deep active learning. Medical Image Analysis 68 (2021), 101913.   
[49] Hongbin Ye, Ningyu Zhang, Shumin Deng, Xiang Chen, Hui Chen, Feiyu Xiong, Xi Chen, and Huajun Chen. 2022. Ontology-enhanced Prompt-tuning for Fewshot Learning. In Proceedings of the ACM Web Conference 2022. 778–787.

[50] Donggeun Yoo and In So Kweon. 2019. Learning loss for active learning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 93–102.   
[51] Samira Zad and Mark Finlayson. 2020. Systematic evaluation of a framework for unsupervised emotion recognition for narrative text. In Proceedings of the First Joint Workshop on Narrative Understanding, Storylines, and Events. 26–37.   
[52] Baoquan Zhang, Shanshan Feng, Xutao Li, Yunming Ye, Rui Ye, Chen Luo, and Hao Jiang. 2022. Sgmnet: Scene graph matching network for few-shot remote sensing scene classification. IEEE Transactions on Geoscience and Remote Sensing 60 (2022), 1–15.   
[53] Dell Zhang and Wee Sun Lee. 2003. Question classification using support vector machines. In Proceedings of the 26th annual international ACM SIGIR conference on Research and development in informaion retrieval. 26–32.   
[54] Hong-Tao Zhang, Min-Lie Huang, and Xiao-Yan Zhu. 2012. A unified active learning framework for biomedical relation extraction. Journal of Computer Science and Technology 27, 6 (2012), 1302–1313.

[55] Lirong Zhang, Hideo Joho, and Hai-Tao Yu. 2022. Semantic Modelling of Document Focus-Time for Temporal Information Retrieval. In Companion Proceedings of the Web Conference 2022. 896–902.   
[56] Xiaowei Zhang, Bin Hu, Jing Chen, and Philip Moore. 2013. Ontology-based context modeling for emotion recognition in an intelligent web. World Wide Web 16, 4 (2013), 497–513.   
[57] Xu Zhang, Yifeng Li, Wenpeng Lu, Ping Jian, and Guoqiang Zhang. 2020. Intra-Correlation Encoding for Chinese Sentence Intention Matching. In Proceedings of the 28th International Conference on Computational Linguistics. 5193–5204.   
[58] Qiankun Zhao and Sourav S Bhowmick. 2003. Association rule mining: A survey. Nanyang Technological University, Singapore 135 (2003).   
[59] Binggui Zhou, Guanghua Yang, Zheng Shi, and Shaodan Ma. 2022. Natural language processing for smart healthcare. IEEE Reviews in Biomedical Engineering (2022).   
[60] Fuzhen Zhuang, Zhiyuan Qi, Keyu Duan, Dongbo Xi, Yongchun Zhu, Hengshu Zhu, Hui Xiong, and Qing He. 2020. A comprehensive survey on transfer learning. Proc. IEEE 109, 1 (2020), 43–76.