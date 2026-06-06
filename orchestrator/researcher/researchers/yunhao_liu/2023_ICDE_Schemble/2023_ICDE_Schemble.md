# Efficient Deep Ensemble Inference via Query Difficulty-dependent Task Scheduling

Zichong Li ∗, Lan Zhang∗† , Mu Yuan∗, Miaohui Song∗, Qi Song∗

∗ University of Science and Technology of China

† Institute of Artificial Intelligence, Hefei Comprehensive National Science Center

Hefei, China

lzc123@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, {ym0813, songmiaohui}@mail.ustc.edu.cn, qisong09@ustc.edu.cn

Abstract—Deep ensemble learning has been widely adopted to boost accuracy through combing outputs from multiple deep models prepared for the same task. However, the extra computation and memory cost it entails could impose an unacceptably high deadline miss rate in latency-sensitive tasks. Conventional approaches, including ensemble selection, focus on accuracy while ignoring deadline constraints, and thus cannot smartly cope with bursty query traffic and queries with different hardness. This paper explores redundancy in deep ensemble model inference and presents Schemble, a query difficulty-dependent task scheduling framework. Schemble treats ensemble inference progress as multiple base model inference tasks and schedules tasks for queries based on their difficulty and queuing status. We evaluate Schemble on real-world datasets, considering intelligent Q&A system, video analysis and image retrieval as the running applications. Experimental results show that Schemble achieves a 5× lower deadline miss rate and improves the accuracy by 30.8% given deadline constraints.

Index Terms—Ensemble learning, Deep learning, Efficient inference, Task scheduling

# I. INTRODUCTION

Deep learning techniques have been adopted in various data systems for data analysis and better service quality [1– 3]. Certain aspects, such as model architecture and training data [4], are essential for deep learning models to be accurate. In practice, however, the performance of an individual model is often limited by low-quality training data, inadequate architecture and hyperparameters. Ensemble learning [5] is proposed to combine decisions from multiple models, named base models, prepared for the same task, so as to improve the overall performance. Many efforts [6, 7] have been devoted to ensembling traditional machine learning models, such as XGBoost [6] and Randomforest [7]. There are also studies investigating the theoretical properties of ensemble learning. For example, Hansen and Salamon [8] proves that in the binary classification task, if the votes from the base models are independent of each other and have accuracies higher than random guesses, overall accuracy could approximate one as the ensemble size grows. Recently, there is a growing trend to ensemble deep learning models [1, 9–12]. They have gained significant improvement in a variety of tasks, including speech recognition [11], video analysis [1], disease diagnose [2], etc..

![](images/feaeb9a9c7444a0089e4d85f991b1523005cbd8b3b42d0357d1d554b1fff68ca.jpg)



(a) Query traffic and deadline miss rate at different time segment.

![](images/7f0d16f9807ef23ecaf1a7293649111656d3dd0e431a9c789e2857c80ea4e710.jpg)



(b) Performance of an ensemble model and the base models.   
Fig. 1: Performance of an example deep ensemble model (BiL-STM+RoBerta+Bert). (a) One-day query traffic and deadline miss rate of the deep ensemble model in a real intelligent Q&A system (text matching task). Deadlines are set to 100ms after query arrivals. (b) The performance comparison between the ensemble model and three base models.

Although deep ensemble techniques improve accuracy, such improvements come at a cost in terms of additional computational and memory overhead. We investigate the effects of deep ensemble inference on latency-sensitive tasks, and identify a problem that deep ensemble inference could easily lead to a high deadline miss rate, the ratio of queries that miss given deadlines. Fig. 1a presents a one-day query load recorded from a real intelligent Q&A system and the average deadline miss rate of a deep ensemble model at different time slots. The deadline miss rate strongly correlates to the query load and reaches 45% during the traffic burst. In online query systems, deadline misses would reduce customer satisfaction and even be fatal. For example, the auto-driving system [13] should respond to stochastic query traffic within very short delays, where deadline misses could lead to accidents and be lifethreatening.

Deadline misses are mainly due to the following reasons. Typically, to run an ensemble model, a system loads all its base models and executes them in parallel to reduce latency. Taking models for text matching as an example, Fig. 1b shows that the ensemble improves the accuracy but also incurs longer latency, which is slightly larger than the slowest base model. Hence, more complex structures and synchronous execution of base models lead to a higher deadline miss rate. Moreover, the required memory increases linearly with the ensemble size.

A single query will occupy all base models, i.e., a lot of memory, and let subsequent queries wait in the queue. Since many systems only provide limited resources [13–16], when a large number of queries arrive quickly, traditional execution of large deep ensemble models can cause severe queue blocking, resulting in a very high deadline miss rate.

In this work, we focus on deep ensemble inference for latency-sensitive tasks and propose a new execution mechanism to meet the deadlines of queries while maximizing the inference accuracy. We first explore the redundancy in deep ensemble inference by evaluating the performance of every combination of the base models in Fig. 1b on datasets from a real Q&A system. We discover that 78.3% of samples can be predicted correctly by any of the three base models if we take the ensemble’s outputs as the ground truth. Only less than 11% of samples require executing all three models to get correct predictions, which indicates a large number of redundant executions in deep ensemble inference. Existing practices eliminate the redundancy by shrinking ensemble size [17– 19] or dynamically selecting models based on input features [20, 21]. However, current approaches assume base models are run in serial and seek to control the cumulative runtime on offline tasks instead of response latency for online tasks. Thus, they fail to reduce the deadline miss rate effectively. Besides, most studies focus on traditional ML tasks whose input space’s dimension is much lower.

To eliminate redundant executions, we break down an ensemble inference into multiple base model inference tasks and dynamically schedule these tasks for each arriving query to meet its deadline. Scheduling includes choosing different combinations of base models for arriving queries and deciding the execution order of inference tasks. Intuitively, the harder the sample, the more base models are needed for ensembling. For example, on machine translation, the complete ensemble model can accurately translate long and complex sentences, but it is unnecessary to execute all base models for easy sentences such as ‘Thank you’. By scheduling fewer and faster models for easy samples, we could increase the system throughput and reduce the deadline miss rate with minor accuracy loss. For example, if there are three base models and two relatively easy queries, usually, the second query has to wait for the first one to finish. If we schedule the first model for the first query and the other two models for the second, we can process them simultaneously and get two results with significantly shorter delays. Based on the idea, we present Schemble, a query difficulty-dependent task scheduling framework for efficient deep ensemble inference, which accurately predicts query difficulty and schedules base model inference tasks accordingly.

Schemble addresses two core technical challenges. First, the input space’s dimension in deep learning is usually large; thus, it is very challenging to estimate the difficulty of input samples efficiently. To this end, we introduce discrepancy score to measure inputs’ difficulty by model outputs and train a lightweight network to predict discrepancy scores for newly arrived queries. Second, base model inference tasks need to be selected and scheduled in an online manner to maximize accuracy under deadline constraints. The huge search space of all possible selections of model sets and execution orders for all queries makes it non-trivial to determine the optimal scheduling plan. To cope with this, we break the online scheduling problem into local subproblems and design a nearoptimal dynamic programming-based algorithm. We conduct a theoretical analysis of the competitive ratio of the proposed algorithm. In summary, the main contributions are as follows.

• We identify a novel problem, i.e., efficient deep ensemble inference for latency-sensitive tasks, which maximizes the inference accuracy under deadline constraints for online queries through dynamically scheduling base model inference tasks. We explore input difficulty and analyze the scheduling problem’s complexity and optimality.   
• We present Schemble, a novel query difficulty-dependent task scheduling framework for efficient deep ensemble inference. We propose a new measurement for input difficulty and design a dynamic programming-based algorithm to achieve efficient inference with limited resources.   
• We evaluate Schemble on various applications, including text matching, video analysis and image retrieval, using both simulated and real-world query traces. Evaluation results show that Schemble achieves a 5× lower deadline miss rate and improves the accuracy by 30.8% given deadline constraints than the original ensemble in text matching task.

# II. RELATED WORK

We categorize related work as follows.

a) Static ensemble selection: Static method selects the same subset of models for inference on every query [18, 22, 23] to reduce model execution, without considering differences between the inputs. Caruana et al. [23] proposed a greedy algorithm that selects the model that could improve the overall accuracy most in every iteration until the resource limit is reached. Li et al. [18] theoretically analyzed relations between base model diversity and overall performance, and designed a diversity-regularized selection algorithm. Visentini et al. [22] introduced F-score to rank base models and select models with the highest scores. Static ensemble selection speeds up inference by reducing the ensemble size and could improve performance when bad models exist in the model pool. However, the ensemble size of deep ensembles (around 3) is much smaller than their traditional ensemble problems (50-200). In deep ensemble scenarios, static selection could be accomplished by greedy search at a low cost. Moreover, naively removing models from deep ensembles results in a bad trade-off between accuracy and computation overhead. It either brings huge accuracy losses with low deadline miss rates or minor accuracy losses with high miss rates.

b) Dynamic ensemble selection(DES): DES method selects different models subsets dynamically based on the inputs features [20, 21, 24], similar to our idea. They stated that base models specialize in different regions in the input space, which is called models’ preferences. They proposed methods to learn models’ preferences to select models with higher credibility (more likely to output a correct prediction) for each input. The dynamicity enables DES to be more flexible than the static selection. DES reduces the total computation overhead on a perquery level. However, existing works on DES did not address the high deadline miss rate problem for two main reasons. Firstly, the objectives of these works are not the deadline miss rate but the accuracy or the offline cumulative runtime. They only select models based on the current query’s features. We must take arrival times and queuing status into account when selecting models to lower the miss rate effectively. Secondly, the base models they considered are mostly traditional ML models and shallow networks, whose preferences are simple and could be nicely captured by simple ML algorithm. The deep learning models in our problem possess much more complicated preference space that varies significantly with random seeds. DES methods couldn’t capture deep models’ preferences and thus result in vast accuracy losses.

Besides static and dynamic ensemble selection, some works on aggregation mechanisms such as Gating [25, 26] could also be employed to select models for execution. Gating is a popular technique used in Mixture of Expert (MoE) [26] that utilizes neural network gates to aggregate base models’ outputs. An extra gating network is trained to output a scalar weight for each base model to average models’ predictions. By learning to assign large weights to credible base models, Gating achieves better performance than uniform averaging. We could select a subset of models for execution by thresholding the gating weights. As a straightforward solution that also applies neural networks for selection, we discuss the difference between Gating and our method in SectionV-C and compare them thoroughly in the experiments.

Some other studies designed machine learning serving systems with optimization on ensemble inference [27, 28]. For example, Crankshaw et al. [28] introduced a module to monitor changes in data distribution and modify the ensemble model adaptively. Lee et al. [27] provided an excellent platform for deploying and maintaining multiple models. These works focus on stability and accuracy rather than per-instance latency. Therefore, we refer to them as orthogonal works.

# III. PRELIMINARY

We start with basic terminology and the inference pipeline of a deep ensemble model.

# A. Deep ensemble inference

A typical deep ensemble consists of multiple deep learning models and an aggregation module. The deep learning models, also called the base models in the ensemble, perform inference on samples and output predictions. The aggregation module combines all predictions to gain better results. Fig. 2a displays an inference pipeline of a deep ensemble with three base models. Before serving, we deploy all base models on the server waiting for query inference tasks. Each model executes one task at a time and maintains its own queue to store pending tasks. The user could send queries to the system asking for inference results. In a general ensemble inference pipeline, one query assigns an inference task to each base model, and models execute the tasks in parallel. The aggregation module would collect their predictions after all models finish the inference. Under the resource limit that we can not deploy more base models, we would get a high deadline miss rate when lots of queries arrive in a short period due to queue blocking. Note that the execution time of the aggregation module is neglectable compared to the base models’ inference.

![](images/98bf54256df5d7781aef4db566f2f29076c8ef83479bfefa7579ee25f4ca2384.jpg)



(a) Generic pipeline

![](images/c8de484505b87674097ab5a4fa42afefb4bcb3f53492aabdf5968e7797b7f81d.jpg)



(b) Pipeline with static selection   
![](images/5ff3cab61ef41cbf2d8b94d7f3c58f0c05ccdf3418a9cf3c33324cb9cfe58f95.jpg)



(c) Pipeline with DES

![](images/84a3fdb1f074ad3b5430ad11641e4e289c23c0994f80306ae8dbc37b47e048c6.jpg)



(d) Pipeline with Gating   
Fig. 2: Deep ensemble inference pipeline and piplines with existing approaches

# B. Ensemble selection

As discussed in Section II, existing works aim to reduce computational overheads of the ensemble by statically and dynamically selecting subsets of models for execution. We further describe and illustrate how their approaches modulate the pipeline with figures.

Static ensemble selection selects the same subset of models for all queries. Thus, we could spare memory by deleting unchosen models and utilize the memory with replicas of the chosen models. Fig. 2b displays the inference pipeline with static selection that chooses model 1 and model 2. A replica of model 2 is deployed to harness the remaining memory. In practice, thanks to the small ensemble size of the deep ensemble, we are able to find an optimal deployment plan for static selection by greedy search.

Dynamic ensemble selection (DES) selects subsets of models based on input features. Hence, we still need to deploy all base models on the server. DES learns models’ preferences, measured by competence score, to determine which subset of models could give accurate predictions on the current query. In general, DES algorithms consist of three steps. First, during the training phase, a clustering method is applied to divide the input space into several regions. Then the algorithm estimates a competence score for each model in each region, representing how credible the model is. Existing works utilize models’ accuracy profiling in the region [20], probabilistic models [29], or even neural networks to calculate the score [21]. At the inference phase, the arrived query will trigger a selection mechanism to choose a subset of models based on the estimated competence scores in the region where the query belongs. The query would then assign inference tasks to the subset of models DES selects, as shown in Fig. 2c.

The gating method [25] is similar to DES, except that it directly employs neural networks to learn models’ preferences, which is called the gating network. The gating network takes the query as the input and outputs a scalar weight for each base model. During the training phase, the gating network’s parameter is optimized by approximating the weighted average of all base models’ predictions to the ground truth labels. The gating network would learn to assign large weights to credible models for each query. In the inference phase, we select subsets of models by filtering models with low gating weights, as shown in Fig. 2d.

While the static method is inflexible and results in bad trade-offs, other existing approaches select subsets of models dynamically, similar to our idea. However, they ignore two main problems. First, preferences of deep learning models are hard to capture. As we will show in section V-C, preferences of deep learning models are complicated and have a huge variance. Learning it with a lightweight neural network resembles approximating a high-variance noise. Also, DES applied clustering which does not adapt well to high-dimensional inputs. To cope with it, instead of learning base models’ preferences, we proposed to distinguish between inputs with different difficulties. Second, they ignore the task scheduling problem. They both select models only based on the current query features, regardless of the queuing status (previous arrivals). For example, assume there is a pending query and model A has the highest credibility on it. Existing approaches assign tasks to model A even when its queue is long. Our framework aims to select models taking queuing status into account with a task scheduling algorithm to achieve a better trade-off between computational overhead and accuracy.

# IV. METHOD OVERVIEW

Consider a typical deep ensemble inference system with multiple base models, as shown in Fig. 3. The original pipeline executes all base models for each arrived query, resulting in severe deadline misses. We aim to reduce the deadline miss rate through dynamically scheduling1 inference tasks for queries. The proposed framework, Schemble, executes base models based on query difficulty and queuing status. Schemble maintains an extra query buffer and adds three components to the original pipeline. The query buffer stores queries that arrive when all base models are busy. While existing approaches select model subsets immediately after query arrival, the extra buffer enables Schemble to select a little later to adapt to the arrival of subsequent queries. The Discrepancy Score Prediction module and the Task Scheduler module process queries in the query buffer and offer an execution plan. Once there are idling models, the scheduler will send query inference tasks to the base models according to the plan. The

![](images/6a355840991229e16f057d1b7bc48bc41fa5e5907b275163ca8e9d2478af2ea5.jpg)



Fig. 3: The original ensemble inference pipeline (black) and the new inference pipeline with Schemble (red)

Missing Value Filling module fills up the missing outputs of unexecuted models for final aggregation. The functions of the added modules are summarized as follows:

• Discrepancy Score prediction: This module applies an efficient neural network to predict queries’ difficulty measured by the discrepancy score. Paired with offline accuracy profiling, it estimates the accuracy of different combinations of base models on the current query.   
• Task Scheduler: This module schedules inference tasks for queries based on the estimated accuracy of model combinations and queuing status. It maximizes estimated inference accuracy and ensures queries are completed by their deadlines.   
• Missing Value Filling: This module handles the missing values of models that are not executed, ensuring that the aggregation module could work properly.

# V. DISCREPANCY SCORE PREDICTION

We first define a novel metric, discrepancy score, for measuring query difficulty using base models’ outputs and the ensemble’s outputs. Since models’ outputs are unavailable before the models’ execution, we train a lightweight neural network to predict newly arrived queries’ difficulty. We then conduct offline accuracy profiling on historical data to obtain the performance of all model subsets on queries with different hardness. This module estimates queries’ discrepancy scores and combines them with the profiling table to construct the reward function for subsequent inference task scheduling.

# A. Discrepancy Score

There are a number of definitions of sample difficulty in the literature [30, 31]. For example, Carlini et al. [30] proposed to use the distance to the decision boundary measured by an adversarial example attack as the measurement. Jiang et al. [31] analyzed the consistency score, which characterizes the expected accuracy for a held-out instance given training sets of varying sizes. However, these metrics require either retraining multiple models or running model inference multiple times, introducing huge computation overhead to generate difficulty labels. Ensemble agreement [30] is a metric that quite fits our problem. It ranks samples’ difficulty based on the agreement within the ensemble, as measured by the symmetric KLdivergence between base models’ outputs. Since the inference results of historical queries could be recorded at a low cost, we could directly calculate the ensemble agreement score. However, problems remain in this metric.

Ensemble agreement is initially proposed for ensembles of homogeneous models. However, deep ensembles often contain heterogeneous base models whose accuracy and output distributions differ from each other. Models with lower accuracy are more likely to induce disagreement, which causes problems the ensemble agreement metric cannot address. Assume we have three binary classifiers; the first classifier is less accurate than the other two. Intuitively, a sample getting outputs ‘1,0,1’ is more difficult than one with outputs ‘0,1,1’. However, the ensemble agreement metric cannot distinguish between them. Moreover, deep networks are discovered to be poorly calibrated [32], which means the outputs probability associated with the predicted class label does not align with its ground truth correctness likelihood. It thus brings in large differences between base models’ output distributions and would significantly affect the KL-divergence, leading to meaningless agreement scores. To cope with these problems, we propose the discrepancy score to better measure difficulty with deep ensembles. Following the idea of the ensemble agreement, the discrepancy score of sample x is defined as follows:

$$
D i s (x) = \frac {1}{m} \sum_ {k = 1} ^ {m} [ N o r m _ {x} (d (f (x; \theta_ {k}), E (x; \theta_ {1},..., \theta_ {m}))) ] \tag {1}
$$

where $f ( x ; \theta _ { k } )$ is the output of the $k ^ { t h }$ base model and $E ( x ; \theta _ { 1 } , . . . , \theta _ { m } )$ is the ensemble’s output. d is the function measuring distance between models’ predictions. We use the JS-divergence to measure the distance between probabilistic distributions in classification tasks, similar to the ensemble agreement metric [30]. For regression tasks, we employ the Euclidean distance.

The expression calculates the average of the normalized distances between the base models’ outputs and the ensemble’s outputs. It ensures the base models give the same predictions as the ensemble when the score approximates zero. Under this condition, executing fewer base models for easy samples with low discrepancy scores would not incur accuracy loss. This may not be the case for the ensemble agreement metric, because the aggregation module may output differently even if the base models’ outputs are identical. In addition, we add normalization in the expression to eliminate the effect of different accuracy of base models. Base models with lower accuracy are more likely to give incorrect outputs and thus have larger distances to the ground truth on average. Hence, intuitively, getting a large distance on a low-accuracy model does not contribute to the sample’s difficulty as much as getting the same distance on a high-accuracy model. As in the example mentioned above, directly summing up distances would implicitly amplify the impact of low-accuracy models. Therefore, we normalize the distances of every base model before averaging them to diminish the contribution of inaccurate models and keep all distances at the same scale. Towards the various output distributions, we apply temperature scaling [32], an efficient yet effective post-processing calibration method, on classifiers’ outputs. After temperature scaling, base models’ distributions will accord with their correctness likelihood and not affect the distance scores.

![](images/50068762e7dfe64ab8a5f4948fb33b4dcfc68f65336cea656404f0dfa3d7ebe6.jpg)



![](images/db5e21f77f3d21640b2d624fe57416001f20ca81a8625452474a2dde5099eefd.jpg)



(a) Distribution of the discrepancy (b) Relation between the discrepancy score on three real-world datasets score and models’ accuracy   
Fig. 4: Experimental analysis on discrepancy score

# B. Analyze Discrepancy Score

From the definition, samples with larger discrepancy scores get more diverse outputs from the base models. Executing fewer models for these complex samples is more likely to get results that differ from the original ensemble. Thus, more models should be executed for them to keep high accuracy. On the contrary, easy samples with smaller discrepancy scores get similar outputs from the base models. Choosing fewer models or even a single model for them could get results the same as the ensemble. The discrepancy score accords with our intuition that easy samples require less computation.

To further demonstrate, Fig. 4 displays the distribution of the discrepancy scores of samples from three real-world datasets. The results show that a great proportion of samples possess a low discrepancy score around zero. We then divide the datasets into multiple bins by discrepancy scores and calculate the accuracy of different combinations of base models in each bin to see the relation between the discrepancy score and the model combinations’ accuracy. Note that since this paper focuses on the efficiency of ensemble inference, we refer to the ensemble’s outputs as the ground truth. Fig. 4b presents the results of the text matching dataset. We could observe that easy samples get high accuracy on all model combinations (over 90%), while hard samples show larger error rates with small model subsets. The observation implies that huge redundancy could be eliminated with minor accuracy loss by executing fewer models for easy samples and more for hard ones. More details on experimental settings and ensemble models used could be found in Section VIII.

# C. Predict Discrepancy Score

We utilize a neural network to predict discrepancy scores of newly arrived queries. We generate training data from historical inference results and define the networks to take queries as inputs and generate two outputs. The first is a prediction of the original task, and the second is the estimated discrepancy score. For example, the prediction network in the text matching task outputs a matching probability and a discrepancy score prediction. We train the network with the following weighted loss function:

$$
\text { Loss } (\text { label }, \text { dis }, \text { output } _ {1}, \text { output } _ {2}) =
$$

$$
l (l a b e l, o u t p u t _ {1}) + \lambda M S E (d i s, o u t p u t _ {2}) \tag {2}
$$

where λ is a hyperparameter; We set 0.2 in the experiments. We regard the ensemble’s output as the label. dis is the ground truth discrepancy score. $o u t p u t _ { 1 }$ and $o u t p u t _ { 2 }$ are outputs from the prediction network. l is a proper loss function for the original task, and $M S E$ is the mean square error. We found that adding the original task label into the loss function could improve the prediction of the discrepancy score, which we believe is because sample difficulty is closely related to what we expect to derive from the sample. Note that output1 will not be used during the inference phase.

Specific network architectures are designed according to the task and the input modality. We develop two feature networks to predict discrepancy scores for two modalities: text and image. Our primary consideration in designing these networks is time efficiency since the extra computation could be critical. For text inputs, we convert text to vectors using pretrained word2vec [33] and adopt an efficient text matching model MV-LSTM [34] to generate the matching label. We concatenate the final outputs with intermediate outputs from the LSTM layer and use a densely connected layer to map them to the discrepancy score. As for images, we employ a pretrained MobileNet [35] as the feature extractor and finetune the model on the specific tasks. An additional densely connected layer is trained to map the final outputs and the intermediate outputs to the discrepancy score. Outputs from the last convolutional layer are used as the intermediate outputs.

Training a neural network to predict scores for ensemble selection is similar to the Gating method [25] which also trains a neural network. Hence, we illustrate why predicting discrepancy scores is more applicable than the Gating method by experimental analysis. The main difference between our method and Gating is that we apply neural networks to learn query difficulty, while Gating aims to learn models’ preferences. The gating network takes the query as the input and outputs a weight for each model, indicating how accurate that model will be, which is equivalent to learning whether each model is correct on the current query. Notice that the discrepancy score computes the average distances between all base models’ outputs and the ensemble’s outputs. Take the ensemble’s outputs as the ground truth; if the distance between the base model $\theta _ { k } \mathrm { { ' s } }$ output and the ensemble’s is small enough, the base model $\theta _ { k }$ must be correct. Therefore, in some sense, the gating network is trying to estimate whether $d ( f ( x ; \theta _ { k } ) , E ( x ; \theta _ { 1 } , \dots , \theta _ { m } ) )$ is large for every k.

As previous works [36] discovered, deep models suffer from high variance. Random initialization could result in diverse model weights even with the same architecture and data. Thus the preference space of deep models is often complicated and hard to capture. To demonstrate our points, we conduct experiments on a public image dataset CIFAR100 [37]. We apply six popular image classification models and average them to obtain an ensemble. Fig. 5 shows the correlation coefficients between models’ preferences with different architectures and random seeds. Preference of model $\theta _ { k }$ refers to the vector $[ d ( f ( x _ { 1 } ; \theta _ { k } ) , E ( x _ { 1 } ) ) , \dots , d ( f ( x _ { n } ; \theta _ { k } ) , E ( x _ { n } ) ) ]$ ]. The discrepancy score computed from the ensemble is added to the table for comparison. We observe that the preferences of models are poorly consistent between different architectures and random seeds, indicating that preference space is random and complicated. Moreover, Gating has to learn the preferences of all base models to conduct selection, adding another layer of difficulty to the learning task. Conversely, the discrepancy score shows a much stronger correlation under different random seeds, which means it gets a relatively stable ranking between samples. Plus, we only predict one score representing the difficulty of the sample instead of the complicated preferences of multiple models. Therefore, we believe that predicting discrepancy scores requires a smaller model capacity than learning models’ preferences and thus could better solve our problem.

![](images/9d3a1e59ecc70300f8a38baf6dc4b015435ecbdbf6c207c70a39b8dce1c922a7.jpg)



Fig. 5: Correlation coefficients between models’ preferences and the discrepancy scores. Diagonal scores between an architecture and itself show the correlation of preferences for the same architecture trained with different random seeds. The diagonal score on the discrepancy score refers to the correlation of ensemble models trained with different seeds. $V , R e ^ { 1 8 } , R e ^ { 1 0 1 } , D , I , R n ^ { 5 0 }$ , Dis stand for VGG16, Resnet18, Resnet101, Densenet121, Inceptionv3, Renext50 and the discrepancy scores, respectively.

# D. Model Combination Accuracy Profiling

Having obtained the difficulty predictions of queries, we now build the bridge between the discrepancy score and the model inference task scheduling. Same as Section V-B, we divide the historical data into multiple bins based on the discrepancy score to profile the accuracy of different combinations of base models. Discrepancy score would primarily affect the accuracy gain as shown in Fig. 4b. With the profile, the scheduler could choose appropriate model combinations for each query according to the discrepancy score by maximizing accuracy rewards.

As mentioned earlier, the ensemble size of deep ensembles is usually small. Accuracy profiling could be performed at a low cost. However, we also provide a solution for cases where the ensemble size grows and the profiling progress brings huge computation overhead. For such cases, we profile the accuracy of model combinations of size less than three and estimate accuracy for other combinations by the marginal reward function. We denote the accuracy of model combination $\{ m _ { 1 } , . . . , m _ { k } \}$ on the $i ^ { t h }$ bin as $U ( i , \{ m _ { 1 } , . . . , m _ { k } \} )$ . We apply the following expression to estimate the accuracy.

$$
\begin{array}{l} U (i, \{m _ {1}, \dots , m _ {k + 1} \}) = U (i, \{m _ {1}, \dots , m _ {k} \}) \\ + \gamma_ {k} \frac {1}{k} \sum_ {q = 1} ^ {k} [ U (i, \{m _ {q}, m _ {k + 1} \}) - U (i, \{m _ {q} \}) ] \tag {3} \\ \end{array}
$$

Models are sorted by their accuracy, and $\gamma _ { k }$ is the diminishing factor of marginal reward that could be estimated by profiling accuracy. We show that the estimated accuracy could approximate true accuracy nicely in extensive experiments [38].

# VI. TASK SCHEDULER

Treating the ensemble inference progress as multiple base model inference tasks, this module schedules tasks for arrived queries based on their difficulty and decides the tasks execution order. Since we execute base models in parallel, we refer to the tasks execution order as the order of inference tasks of the same model. The scheduled tasks for a query constitute the execution of a small ensemble. The goal is to ensure that as many samples can be inferred accurately before their deadlines. We use the profiled accuracy as the reward function for executing model combinations. A scheduling algorithm is designed to address the trade-off between inference accuracy and deadline misses by maximizing cumulative rewards.

# A. Scheduling Problem

The problem addressed in this module is choosing a model subset for each query and scheduling the inference tasks so that the cumulative rewards are maximized. The unit of the scheduling is a base model inference task. A deadline is assigned at each query arrival, denoting the time by which the query must be processed. Deadlines appear as a constraint that queries completed after the deadlines are considered missed and incorrect, thus get 0 rewards. Deep network execution is non-preemptive, but the execution time is approximately constant. We could estimate the completion time of tasks beforehand to see whether they could meet the deadline. To be generalized, we do not pose distribution assumptions on query arrival times. Future arrival times and deadlines are unknown, which makes the scheduling problem an online scheduling problem. Mathematically:

Let $\{ q _ { 1 } , \ldots , q _ { n } \}$ be the arriving queries. $q _ { i }$ arrives at time $r _ { i }$ with deadline $d _ { i }$ . Rewards $U _ { i , s _ { i } }$ that $q _ { i }$ could gain from model sets $s _ { i }$ is estimated by profiling in the Discrepancy score prediction module, where $\bar { s _ { i } } ~ \in ~ S ~ \bar { = } ~ \{ [ s ^ { ( 1 ) } , \ldots , \bar { s ^ { ( m ) } } | s ^ { k } ~ \in$ $\{ 0 , 1 \} ]$ is an indicator vector for model set. $s _ { i } ^ { k } = 1$ indicates that model set $s _ { i }$ contains model k. m is the total number of base models. The schedule decides two outputs: model inference tasks for each query and the tasks execution order. We use $x ( i )$ to denote the model set scheduled for $q _ { i }$ . To keep the expression simple, explicit expression of execution order is omitted and we use $C _ { i } ^ { x }$ to denote completion time of $q _ { i }$ The mathematical formulation of the optimization problem is:

$$
\max _ {x} \sum_ {i} 1 _ {C _ {i} ^ {x} <   d _ {j}} U _ {i, x (i)} \tag {4}
$$

The indicator function ensures that only queries processed by the deadline get the rewards. We assume that the utility function $U _ { i , s _ { i } }$ i satisfies the law of diminishing marginal utility.

Assumption 1 (Diminishing marginal utility). $U _ { i , s ^ { \prime } } - U _ { i , s } \geq$ $U _ { i , s ^ { \prime \prime } } - U _ { i , s ^ { \prime } } \geq 0 ,$ , where $s ^ { \prime }$ and $s ^ { \prime \prime }$ contain one more model than s and $s ^ { \prime }$ respectively.

The assumption is consistent with human intuition and experiment results, under which we could infer that $U _ { i , x } \geq $ $\textstyle \sum _ { k } s ^ { ( k ) } / m$ , since the maximum utility is 1.

# B. Scheduling Algorithm

The scheduling problem is similar to the knapsack problem [39], especially the deterministic non-linear equality fractional knapsack (NEFK) problem [40, 41]. They both aim to maximize a non-linear utility function with resource constraints. Specifically, we optimize the non-linear rewards function constructed in accuracy profiling under constraints on query completion time. However, our deadline constraints are related to the scheduling order and the completion time of multiple models. We have to consider the execution time of models chosen for the query as well as inference tasks assigned ahead of it to calculate the completion time of queries. Hence, it’s intractable to formulate our deadline constraints as linear inequalities (or equalities) as in the NEFK problem. Therefore, we design a dynamic programming-based algorithm to solve the problem and express its competitive ratio relative to a clairvoyant scheduler (scheduler that accesses information of all future queries).

As the query traffic is unpredictable, we simplify the online scheduling problem to multiple local subproblems which are scheduling tasks for queries in the query buffer at each moment. The mathematical form of the subproblem is the same as the online problem (4), but with the restriction of arrival time removed since we only focus on queries that have already arrived.

To begin with, we assume model sets for queries are already chosen (i.e., tasks are fixed) and decide the execution order of the inference tasks. Since base models maintain their own task buffer, there is no strict restriction on the execution order of two queries (e.g., model A processes query 1 ahead of query 2, while model B processes query 2 first). This fact significantly increases the search space of the scheduling order. However, we prove that adding a restriction on the queries execution order does not degrade the scheduling performance (see detailed proofs in [38]).

Theorem 1. For every schedule x, there exists a schedule that has consistent query order achieving the same or better performance.

By forcing queries to be processed in a strict order, we only need to determine the processing order of queries. However, scheduling with deadlines and rewards is still an NP-hard problem [42]. Luckily, we could prove that Earliest Deadline First (EDF) [43] is the best schedule policy under the assumption that the model subsets for queries are fixed and it is possible to schedule them without deadline misses (the scheduled model subsets are feasible).

Theorem 2. If inference tasks for all queries are fixed and the scheduled tasks are feasible, Earliest Deadline First is the optimal schedule policy (could complete all queries before deadlines).

The proof is omitted due to length limits; detailed proofs could be found in [38]. Therefore, we take EDF as the underlying execution order and apply a dynamic programming-based algorithm to solve the local subproblem.

Algorithm 1 Dynamic Programming Scheduling Algorithm
Input: Base models inference time $\{T_k\}_{k=1,\dots,m}$ ; Available query set $\{q_i\}_{i=1\dots N}$ ; Utility matrix $\{U_{i,s}\}_{i=1,\dots,N;s\in S}$ ; Base models' remained execution time $\{t_k^{(0)}\}_{k=1\dots m}$ Output: Near optimal Scheduling plan $Comb_{N,u^*}$ ; Near optimal utilities $u^*$ ;
1: for $i \in [1,\dots,N]$ do
2: Initialize $Comb_{i,0}$ as empty list (not choosing any model)
3: Initialize $Time_{i,0}$ as base models remained execution time
4: end for
5: for $i \in [1,\dots,N]$ do
6: for $u \in [\delta,2\delta,\dots,i^{(\delta)}]$ do
7: for $s \in S$ do
8: $u' \leftarrow u - U_{i,s}$ 9: $T_s \leftarrow$ Inference time of combination s
10: if $Time_{i-1,u'} + T_s$ meet the deadline then
11: Combine s with elements in $Comb_{i-1,u'}$ and insert them to $Comb_{i,u}$ 12: Insert $Time_{i-1,u'} + T_s$ to $Time_{i,u}$ 13: end if
14: end for
15: Prune redundant solutions in $Comb_{i,u}$ based on $Time_{i,u}$ 16: end for
17: end for
18: return $Comb_{N,u}, \forall u \in [\delta,2\delta,\dots,N^{(\delta)}]$ ;

The algorithm is presented in Alg. 1. Initially, we quantize the reward function to shrink the problem size significantly [44]. All rewards $U _ { i , x }$ are measured in multiples of some basic increment δ. We denote $\lfloor U _ { i , x } / \delta \rfloor \delta$ as $\bar { U } _ { i , x } ^ { ( \delta ) }$ for simplicity. Since we plan to process queries in EDF order, we index queries in the queue according to their deadlines $d _ { i } ,$ such that $d _ { 1 } ~ \le ~ d _ { 2 } ~ \le ~ \dots ~ \le ~ d _ { N }$ . The algorithm would output a model set $s _ { i }$ for each query and ensures that their inference tasks are completed before the deadlines. Dynamic programming formulation maintains a two-dimensional table, where one dimension represents the number of considered tasks, $i \in { 1 , \dots , N }$ , and the other represents the quantized total rewards, $u \in \{ \delta , 2 \delta , \dotsc , N ^ { ( \delta ) } \}$ . Each cell contains the solutions to a sub-subproblem, that is, selecting model sets for the first i tasks that could attain exactly u reward in total. We use $C o m b _ { i , u }$ to denote the solutions in cell $( i , u )$ . For every i, the algorithm iterates through all possible model sets and updates the corresponding cells. $T i m e _ { i , u }$ will record solutions’ execution time to ensure the current schedule meets deadlines in recursions. A pruning operation is involved in every iteration to save computation and keep solutions in every cell optimal. More specifically, $C o m b _ { i , u }$ will be pruned by deleting solutions whose time cost on all models is greater than another solution. The best schedule plan could be determined by visiting cell $C o m b _ { N , u ^ { * } }$ that is non-empty with the largest $u ^ { * }$ . Since we quantize the rewards to facilitate scheduling, the dynamic programming algorithm is not optimal for the unquantized local scheduling problem, but it achieves a nearoptimal solution. Similar to [44], we could proof that the above algorithm is a $( 1 - \epsilon )$ approximation of the optimal one, defining $\delta = \frac { \epsilon } { m N }$ (see detailed proofs in [38]).

Theorem 3. Alg. 1 is a 1 − ϵ approximation of the optimal local scheduling with $\delta = \epsilon / N$ .

We could derive an online scheduling algorithm with Alg. 1 solving the local scheduling problem at each moment. We proceed to show that it has a good competitive ratio relative to the clairvoyant scheduler, following the proof in [45] (see detailed proofs in [38]). The clairvoyant scheduler is defined as the optimal scheduler with complete knowledge of future arrival and maximizing the total rewards.

Theorem 4. The online scheduling algorithm that applies Alg. 1 to solve local subproblems is 2m-competitive.

# VII. FILLING MISSING VALUE

Previous modules select an appropriate subset for every query and determine the execution order. Lastly, we illustrate how we handle the missing model outputs after subsets selection. The goal of filling is to ensure the aggregation model works properly even if some models’ outputs are missing. We do not want the missing part to affect the aggregation of outputs we have gained. We provide three methods to cope with the missing values; each corresponds to an aggregation method.

• (Weighted) Voting: Base models’ outputs vote for the final decision. We minimize the impact of the missing values by simply keeping them out of the vote.   
• (Weighted) Averaging: Base models’ outputs are multiplied by weights and summed to produce the final decision. We set the weights of the missing outputs to 0 and reweight the valid outputs.   
• Stacking: Base models’ outputs are input to a metaclassifier which is trained to aggregate decisions. We apply KNN to find the most similar output files from a set of full inference results of historical data. We fill up

the missing value with the weighted average of the model outputs of the top k most similar output files, using their distances to the target as the weights.

There are several advantages of using KNN for filling: KNN can fill multiple missing values simultaneously with low computation cost; KNN makes no assumptions on the distribution of models’ outputs and, therefore, can fit in different tasks. However, the k-value can only be chosen using human experience. Our experiments show that Schemble is robust to varied k parameters.

# VIII. EXPERIMENTAL EVALUATION

Using three real-life datasets which cover text and image modalities, we conduct experiments to evaluate the effectiveness and efficiency of our algorithms for text matching, vehicle counting and image retrieval tasks.

# Experiment Setting. We use the following setting.

Datasets. We use three real-life datasets, correspond to three different tasks. (1) Text matching: The text matching dataset is collected from a global bank’s intelligent Q&A system. The service system receives customers’ question and returns answers by matching the questions with candidates in the database. We conduct experiments with the ensemble deployed in the real-world system, consisting of three deep text matching models (Bert [46], Roberta [47], BiLSTM [48]) and an aggregation model (XGBoost [6]). The performance of the deep ensembles and the base models are shown in Fig. 1b. We record a one-day query trace that contains more than 130,000 queries to simulate the traffic. Each sample consists of two questions, one from the customer and the other from the database, and a label representing whether the two questions map to the same answer. (2) Vehicle counting: UA-DETRAC [49], which is a real-world video dataset consisting of 10 hours of videos captured at 24 different locations, is used. Since ensembling of object detection models has been shown effective [50], we deployed three object detection models (EfficientDet-0 [51], Yolov5l6 [52], YoloX [53]) to count the vehicles in video frames. The weighted average is used as the aggregation module. (3) Image retrieval: We apply the R1M [54] dataset, which contains more than 1 million distractor images, as the database. We use the DELG [55] model with two different architectures to construct the deep ensemble. The weighted average is used as the aggregation module. The performance of the deep ensembles and the base models involved could be found in [38].

Algorithms. We implement Schemble and compare it with the following baseline algorithms.

• Original: Original deep ensemble inference pipeline that executes all base models on every query.   
• Static: Statically select a subset of models and deploy replicas of chosen models to utilize resources. We choose the best subset by greedy search since the ensemble size is small.   
• Dynamic Ensemble Selection (DES): We apply the SOTA DES algorithm Fire-DES++ [24] that dynamically selects

models for queries based on its features. For a fair comparison, a pretrained feature extractor is applied to extract low-level features from high-dimensional inputs.   
• Gating: We select models by thresholding the gating weights. The same network architecture as the discrepancy score prediction model in Schemble was applied as the gating network.   
• Schemble(ea): The proposed framework using the ensemble agreement as the difficulty measurement.   
• Schemble: The proposed framework.

Query traffic and evaluation metric. Deep ensembles should respond to stochastic and bursty query traffic. For the text matching task, we use the recorded one-day query trace to evaluate our framework’s effectiveness towards bursty traffics. Deadlines are set as constant since we treat all customers the same. For the vehicle counting task, we simulate query traffic by the Poisson process with a constant arrival rate. Each query arrives with a predefined deadline associated with its cameras to simulate locations with different priorities. Deadlines for each camera are sampled randomly from the uniform distribution. For the image retrieval task, we simulate query traffic by the Poisson process with a constant arrival rate and assign constant deadlines to all queries.

We consider a query to miss its deadline if the scheduler fails to run any model inference task for it by the deadline. Otherwise, we consider that the query is processed and return a valid result. We compute the accuracy and deadline miss rate for different baselines. Queries that miss their deadline are considered incorrect. We refer to results from the original deep ensemble as the ground truth since our focus is not on improving accuracy but on optimizing the resource efficiency of the ensemble with trusted accuracy.

Implementation. We deploy the algorithms on a machine powered by an NVIDIA Tesla P100 GPU, a 12-core Xeon E5- 2650 v4 CPU, and 32 GB memory. Schemble is implemented in Python. All deep learning models are built using either Tensorflow [56] or Pytorch [57]. All model inference tasks are executed on GPU, and queries are sent to the server through RPC.

Base models are implemented with separate inference interfaces and have their own tasks buffer. If a query arrives when there are idling models, the scheduler would directly assign the query to the idling model without running the DP scheduling algorithm. Otherwise, the query will wait in the extra query buffer described in Section IV. The Discrepancy Score Prediction module deployed on GPU processes queries in the extra query buffer and predicts their discrepancy scores. We store the estimated discrepancy scores with the query. The task scheduler then collects queue status from base models’ task buffers and takes query information(discrepancy scores, deadlines, arrival time) from the query buffer as the inputs. The scheduling algorithm selects model sets for all queries and determines which query to process next. We execute the algorithm again whenever there is a new arrival to produce a better execution plan. In addition, the scheduler won’t assign selected inference tasks to the corresponding models’ immediately after the algorithm execution. Instead, it waits until there are idling models, because there may be new arrival during the waiting time. Waiting for the possible arrival is beneficial to an efficient execution plan. The waiting will not affect the latency since the tasks will be assigned to the models as soon as there are idling ones. We execute the scheduling process on the CPU as scheduling within GPU is pretty restrictive.

Experiment Results. We next report our findings. For more experiments, please refer to the full version [38].

Exp-1: Overall Performance. We first evaluate Schemble in terms of accuracy and deadline miss rate (DMR) on three tasks. We manually change the deadline constraint to simulate different deadline requirements. Worth mentioning that all deadlines assigned are larger than the time delay of the slowest model in the ensemble, in which case deadline misses will only result from queue blocking. We allow rejection for all baselines, which means queries that have an estimated completion time exceeding their deadlines would be rejected.

The evaluation results are presented in Fig. 6, Fig. 7 and Fig. 8. Tab. I shows the average accuracy and deadline miss rate under different deadline constraints. On average, Schemble increases the accuracy by 30.8% and reduces the deadline miss rate by 33.5% compared to the original pipeline on the text matching task. Schemble clearly outperforms other methods in terms of accuracy on all datasets, reducing the deadline miss rate significantly. Schemble gets the second lowest DMR on the image retrieval dataset since there are only two base models and choosing one model for all queries achieves the lower bound of DMR. Note that the accuracy and the deadline miss rate show opposite patterns because we treat the missed queries as incorrect samples. Minor differences still exist because the accuracy of the processed queries between baselines differs. The improvement of Schemble comes from two reasons: 1) dynamic model execution allows more flexible scheduling. Schemble chooses model sets according to the current queuing status to effectively lower the deadline miss rate, while other baselines execute models merely based on input features. The static selection shows comparable performance with Gating and better accuracy than DES. We observe that Gating and DES select identical model sets for most queries, which induces a waste of resources. Gating often executes the fastest model, reducing the miss rate but having low accuracy; DES tends to execute the model with the highest accuracy, producing accurate results, but the miss rate is high. 2) Schemble treats inputs differently based on the estimated discrepancy score. As analyzed in Section V-B, our design explores and harnesses inputs’ difficulty, while other baselines focus more on which model could output the correct result. Their approach cannot distinguish between inputs in the deep ensemble case because of the high dimension of the input space and the high variance of models’ preferences. In addition, we add the Schemble(ea) baseline to see how our novel difficulty measurement outperforms the existing metric. Schemble(ea) achieves a comparable deadline miss rate since it also employs the task scheduler. However, it gets a lower accuracy since the ensemble agreement metric could not effectively distinguish inputs.

![](images/e177b6eb610115b1218f021ed4aa67173583f3e5bd7eaecf7ca8dc5806d6678c.jpg)



(a) Accuracy

![](images/738309ab31e29663551ea10842eb1438fd8cff1f1b34ce65d7c9c81bfd513bba.jpg)



(b) Deadline Miss Rate

Fig. 6: Comparison between baselines on text matching under different deadlines   
![](images/a202413a0e3a35a63011e69349ef9b6bbe1fc9c8e92701afdd57caa8cab2958b.jpg)



(a) Accuracy

![](images/38dadffd52fa5b190635f110e59e0778b4d92634fb1eee53bb91760cce3e6020.jpg)



(b) Deadline Miss Rate   
Fig. 7: Comparison between baselines on vehicle counting under random deadlines with different means.

Exp-2: Latency. When evaluating the deadline miss rate, we allow rejection for all baselines. We skip the query when its estimated completion time exceeds the deadline. However, all queries have to be processed eventually in some scenarios. We force every query to be processed and report the latency and accuracy in Tab. II. Schemble achieves 500x lower mean latency than the original pipeline while keeping over 97% accuracy on text matching task. Compared with other baselines, Schemble obtained the lowest P95 latency and max latency. Though Gating gains the smallest mean latency, it results in a larger accuracy loss. Schemble gets less significant improvement on latency in the other two tasks, which is because the simulated traffic is stabler and the ensemble size of the image retrieval task is smaller. In this part of the experiments, Schemble aims to achieve a better trade-off between the accuracy and the latency instead of achieving the best performance on both metrics. To show that our results are significant, we display the results with two metrics as the axis in Fig. 11 and define the objective function $c = 1 0 0 * A c c - \lambda$ ∗ Latency as the weighted sum of the latency and the accuracy. The weight λ implies the relative importance of the latency metric. A larger objective indicates a better trade-off. The curves $\begin{array} { r } { ( A c c = \frac { \bar { \lambda } } { 1 0 0 } L a \dot { t } e n c y + \frac { 1 } { 1 0 0 } c ) } \end{array}$ in Fig. 11 show objectives functions with two different weights. Methods on the same curve achieve the same objective. Moving the curves upwards increases the objectives. We could observe that our method achieves the best trade-off between all baselines under an extensive range of weights ([0.056, 210]). Only when the weights go extreme ((−∞, 0.056)∩(210, ∞)), i.e. customers almost just care about one metric, our method achieves the second best performance. For trade-off results on other datasets, please refer to [38].

![](images/427a485b51920dc57ec928596e01996a1ab2c72546653d93fb0c4652deb0eaef.jpg)



(a) mAP

![](images/ccad2a65ad8fb85ec934135ba48d9444ccdcdd0cb49c62735ed031498da13cae.jpg)



(b) Deadline Miss Rate   
Fig. 8: Comparison between baselines on image retrieval under different deadlines.

TABLE I: Comparison of average Accuracy (Acc) and Deadline Miss Rate(DMR) performance among different deadline constraints between baselines on three tasks: TM (Text Matching), VC (Vehicle Counting), IR (Image Retrieval) 

<table><tr><td></td><td colspan="2">TM</td><td colspan="2">VC</td><td colspan="2">IR</td></tr><tr><td></td><td>Acc</td><td>DMR</td><td>Acc</td><td>DMR</td><td>mAP</td><td>DMR</td></tr><tr><td>Original</td><td>60.4</td><td>39.6</td><td>57.0</td><td>43.0</td><td>47.3</td><td>52.7</td></tr><tr><td>Static</td><td>84.8</td><td>12.3</td><td>69.4</td><td>26.9</td><td>74.1</td><td>11.8</td></tr><tr><td>DES</td><td>66.2</td><td>30.7</td><td>56.4</td><td>39.6</td><td>55.7</td><td>35.2</td></tr><tr><td>Gating</td><td>85.3</td><td>8.0</td><td>60.5</td><td>23.0</td><td>58.1</td><td>32.8</td></tr><tr><td>Schemble(ea)</td><td>87.6</td><td>6.8</td><td>73.3</td><td>16.3</td><td>75.0</td><td>14.5</td></tr><tr><td>Schemble</td><td>91.2</td><td>6.1</td><td>80.4</td><td>15.4</td><td>78.4</td><td>14.3</td></tr></table>

Fig. 9 shows how latency and accuracy vary in different time segments. Schemble, Static and Gating successfully eliminate the latency burst while Gating gets an even lower latency. We could see from Fig. 9b that compared methods show a stable accuracy when the load changes. Schemble better adapts to the varying traffic by taking queue status into consideration. When the traffic is light, Schemble utilizes three models for inference. It selects fewer models to keep the latency under control during the bursty period.

Exp-3: Distribution of Discrepancy Scores The distribution of the queries’ discrepancy scores is closely related to the performance of our framework. In previous experiments, we sample the queries randomly from the real-world datasets. In this part, we sample data based on their true discrepancy scores and observe how different scores distributions affect baselines’ performance. We alter the distribution of queries’ discrepancy scores to be normal distribution and gamma distribution with different means; standard variance and scale are set to 0.03 and 1, respectively. A new baseline Schemble(t) is considered, which is Schemble without the discrepancy score prediction module, to see the contribution of the first module. Schemble(t) assign all queries with identical discrepancy scores. We fix deadline constraints to be 105ms and present the accuracy and the processed accuracy (accuracy without the missed queries) in Fig. 10. We do not present the deadline miss rates because they practically remain the same under different distributions.

![](images/1f064364928b70006ce055e167b0de70f7be22aecf795a937c17ba340b9061e2.jpg)



(a) Latency

![](images/624c47c198cec627ce12f4721f49c7a0637db8566f5cffbeaccc4085a22c81b2.jpg)



(b) Accuracy

Fig. 9: Latency and accuracy on one-day query traffic of text matching task   
![](images/993d745143392af719a6a1b61e232a0dcd7822de35fe6f84b4a901c63cc03016.jpg)



(a) Accuracy

![](images/63b227d1a196fb93a9d9ff27e18215d2b29aa5e26b837203a83b7354b5f1e0e5.jpg)



(b) Processed Accuracy   
Fig. 10: Accuracy and Processed Accuracy of baselines under normal distribution and gamma distribution with various means

Results show an obvious decreasing trend since harder examples get lower accuracy. Schemble outperforms all other methods in terms of accuracy except Schemble(t) and achieves the second highest processed accuracy. We observe that as the mean of the distribution grows, Schemble gets a larger improvement, which is counterintuitive since harder queries lead to lesser optimization opportunity. We believe it is owing to the task scheduler which can adaptively execute more models when there are extra resources, while other methods select regardless of the queue.

We observe that when the mean of the distribution is extreme (i.e the queries are all very easy or very hard), Schemble(t) gets a comparable processed accuracy with Schemble. We think it’s because Schemble can’t distinguish inputs effectively when they are of similar difficulty. In such case, Schemble(t) achieves a higher accuracy since it gets a lower deadline miss rate with its lower computation overhead. When the mean of the distribution is in the middle area, Schemble could better explore the difference between queries difficulty and gets better accuracy. More results applying uniform distribution and normal distribution with larger variance could be found in [38].

Exp-4: Task Scheduler. Schemble applies a DP-based algorithm to solve the online scheduling problem. This part compares the proposed scheduling algorithm with several naive and traditional approaches. Besides, as mentioned in Section VI-B, we can address different trade-offs by tuning the quantization step δ in Alg. 1. We display the performance of Alg. 1 with different hyperparameter δ. With the first module fixed, the following scheduling algorithms are compared.

TABLE II: Comparison of Accuracy (Acc) and various Latency metrics (Mean, P95, Max) between baselines on three tasks 

<table><tr><td></td><td colspan="4">Text Matching</td><td colspan="4">Vehicle Counting</td><td colspan="4">Image Retrieval</td></tr><tr><td rowspan="2"></td><td rowspan="2">Acc(%)</td><td colspan="3">Latency(s)</td><td rowspan="2">Acc(%)</td><td colspan="3">Latency(s)</td><td rowspan="2">mAP(%)</td><td colspan="3">Latency(s)</td></tr><tr><td>Mean</td><td>P95</td><td>Max</td><td>Mean</td><td>P95</td><td>Max</td><td>Mean</td><td>P95</td><td>Max</td></tr><tr><td>Original</td><td>100.0</td><td>50.5</td><td>97.7</td><td>99.5</td><td>100.0</td><td>8.4</td><td>20.9</td><td>22.5</td><td>100.0</td><td>104.9</td><td>195.3</td><td>205.1</td></tr><tr><td>Static</td><td>96.9</td><td>0.11</td><td>0.23</td><td>0.64</td><td>95.0</td><td>0.12</td><td>0.31</td><td>0.90</td><td>85.0</td><td>0.57</td><td>1.33</td><td>2.24</td></tr><tr><td>DES</td><td>96.9</td><td>8.2</td><td>24.5</td><td>34.2</td><td>95.5</td><td>3.5</td><td>7.2</td><td>12.5</td><td>86.8</td><td>3.50</td><td>20.1</td><td>28.0</td></tr><tr><td>Gating</td><td>93.0</td><td>0.08</td><td>0.15</td><td>0.49</td><td>90.0</td><td>0.11</td><td>0.33</td><td>0.67</td><td>85.3</td><td>0.60</td><td>1.69</td><td>4.56</td></tr><tr><td>Schemble(ea)</td><td>96.5</td><td>0.13</td><td>0.17</td><td>0.37</td><td>94.7</td><td>0.17</td><td>0.33</td><td>0.44</td><td>89.3</td><td>0.69</td><td>1.73</td><td>2.59</td></tr><tr><td>Schemble</td><td>97.2</td><td>0.10</td><td>0.14</td><td>0.33</td><td>96.2</td><td>0.15</td><td>0.28</td><td>0.43</td><td>91.2</td><td>0.65</td><td>1.58</td><td>2.35</td></tr></table>

![](images/8183e59116647e21a09316f0f1f2ddea4952596b3be881c72cf4ef308fecdc2c.jpg)



![](images/4be3a3d18f11f85d3120a6f6d24c3f7e6700226f3a8f656226aec1a67f6de632.jpg)



Fig. 11: Curves of the trade-off Fig. 12: Accuracy comparison between the latency and the ac- between scheduling algorithms curacy of baselines with different under different deadlines on text weights. matching task

• Greedy+EDF/FIFO/SJF: Take EDF/FIFO/SJF as the execution order. Greedily select the model set with the highest rewards that could complete by the deadline for every query. EDF/FIFO/SJF executes the query with the earliest deadline/earliest arrival time/smallest estimated discrepancy score first.   
• $D P _ { \delta = 0 . 1 / 0 . 0 1 / 0 . 0 0 1 } \colon$ The purposed scheduling algorithm with different quantization step δ.

Results are shown in Fig. 12. DP algorithm with $\delta \ =$ 0.01 achieves the best performance. Our method shows little improvement when the deadline constraint is small. As it increases, DP gets higher accuracy than Greedy algorithms with different execution orders since there is a larger room for task scheduling. Greedy algorithms select the model set with the highest rewards, regardless of the remaining samples in the queue. Therefore, it will incur deadline misses more easily when queries arrive quickly. By increasing δ to 0.1, DP gets more efficient but provides a scheduling plan with smaller cumulative rewards; thus a slight drop in accuracy occurs. Theoretically, Alg. 1 could output results closer to the optimal plan when we reduce δ to 0.001. However, the execution time of the Dynamic programming algorithm will increase linearly as the table size is multiplied by 10. With the extra time affecting the inference, $\mathrm { D P } ( \delta = 0 . 0 0 1 )$ shows a high deadline miss rate and thus low accuracy.

Exp-5: Computation and Resource efficiency. Schemble introduces extra computation and memory cost in two parts, the neural network in discrepancy score prediction and the DP algorithm for task scheduling. All experiments presented above have taken the additional overhead into account. This part presents the overhead of our scheduling framework separately.

![](images/305d9c18ef98fc03b6000e92d7060901d9a618b02cda3089d4ef52a3f97738c7.jpg)



Fig. 13: Latency and memory footprint of Schemble and the deep ensemble on NVIDIA Tesla P100 GPU.

We test the latency and memory footprint of the discrepancy prediction network on GPU to compare with the deep ensemble. Fig. 13 shows that the extra network cost only 6.5% runtime and 0.4-2% memory of the ensemble.

Worth mentioning that two modules process queries in the query buffer, in which case the discrepancy score prediction and the scheduling could be run in parallel with base model inference tasks.

# IX. CONCLUSION

In this paper, we discuss the impact of query difficulty and study the task scheduling problem for deep ensemble inference. We present Schemble to reduce the deadline miss rate while maintaining high accuracy. Schemble distinguishes between queries with different hardness through a novel difficulty measurement that adapts to heterogeneous deep ensembles. We solve the online scheduling problem with a dynamic programming-based algorithm solving local subproblems and prove that the performance of the global online algorithm is also guaranteed. Extensive evaluations on three real-world datasets show that Schemble could handle unpredictable traffic nicely, ensuring queries meet their deadlines and achieving better inference accuracy.

# ACKNOWLEDGMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, No. 62132018. This work was partially supported by ”the Fundamental Research Funds for the Central Universities” WK2150110024. We thank Junjie Wen, Guidong Zheng, Shiding Fu, Yijun Liu and Gaofeng Zhao from the AI Lab of China Merchants Bank for data collection and insightful suggestions to improve this work.

# REFERENCES

[1] M. A. Ganaie, M. Hu, M. Tanveer, and P. N. Suganthan, “Ensemble deep learning: A review,” CoRR, 2021.   
[2] N. An, H. Ding, J. Yang, R. Au, and T. F. A. Ang, “Deep ensemble learning for alzheimer’s disease classification,” J. Biomed. Informatics, 2020.   
[3] C. Liu, L. Zhang, Z. Liu, K. Liu, X. Li, and Y. Liu, “Lasagna: towards deep hierarchical understanding and searching over mobile sensing data,” in MobiCom. ACM, 2016, pp. 334–347.   
[4] J. Lei, Z. Zhang, L. Zhang, and X.-Y. Li, “Coca: Cost-effective collaborative annotation system by combining experts and amateurs,” in ICDE. IEEE, 2022.   
[5] T. G. Dietterich et al., “Ensemble learning,” The handbook of brain theory and neural networks, 2002.   
[6] T. Chen and C. Guestrin, “Xgboost: A scalable tree boosting system,” in KDD, 2016.   
[7] L. Breiman, “Random forests,” Mach. Learn., 2001.   
[8] L. K. Hansen and P. Salamon, “Neural network ensembles,” TPAMI, 1990.   
[9] H. Suk, S. Lee, and D. Shen, “Deep ensemble learning of sparse regression models for brain disease diagnosis,” Medical Image Anal., 2017.   
[10] X. Zhang and D. Wang, “A deep ensemble learning method for monaural speech separation,” TASLP, 2016.   
[11] L. Deng and J. C. Platt, “Ensemble deep learning for speech recognition,” in INTERSPEECH, 2014.   
[12] M. Yuan, L. Zhang, and X. Li, “Mlink: Linking black-box models for collaborative multi-model inference,” in AAAI. AAAI Press, 2022, pp. 9475–9483.   
[13] S. Liu, L. Liu, J. Tang, B. Yu, Y. Wang, and W. Shi, “Edge computing for autonomous driving: Opportunities and challenges,” Proc. IEEE, 2019.   
[14] S. Tuli, N. Basumatary, S. S. Gill, M. Kahani, R. C. Arya, G. S. Wander, and R. Buyya, “Healthfog: An ensemble deep learning based smart healthcare system for automatic diagnosis of heart diseases in integrated iot and fog computing environments,” FGCS, 2020.   
[15] M. Yuan, L. Zhang, X. Li, L. Yang, and H. Xiong, “Adaptive model scheduling for resource-efficient data labeling,” ACM Trans. Knowl. Discov. Data, vol. 16, no. 4, pp. 71:1–71:22, 2022.   
[16] M. Yuan, L. Zhang, F. He, X. Tong, and X. Li, “Infi: end-toend learnable input filter for resource-efficient mobile-centric inference,” in MobiCom. ACM, 2022, pp. 228–241.   
[17] G. Mart´ınez-Munoz and A. Su ˜ arez, “Pruning in ordered bagging ´ ensembles,” in ICML, 2006.   
[18] N. Li, Y. Yu, and Z. Zhou, “Diversity regularized ensemble pruning,” in ECML/PKDD (1), 2012.   
[19] G. Tsoumakas, I. Partalas, and I. P. Vlahavas, “An ensemble pruning primer,” in Applications of Supervised and Unsupervised Ensemble Methods, ser. Studies in Computational Intelligence, 2009.   
[20] A. H. Ko, R. Sabourin, and A. de Souza Britto Jr., “From dynamic classifier selection to dynamic ensemble selection,” Pattern Recognit., 2008.   
[21] R. M. O. Cruz, R. Sabourin, G. D. C. Cavalcanti, and T. I. Ren, “META-DES: A dynamic ensemble selection framework using meta-learning,” CoRR, 2018.   
[22] I. Visentini, L. Snidaro, and G. L. Foresti, “Diversity-aware classifier ensemble selection via f-score,” Inf. Fusion, 2016.   
[23] R. Caruana, A. Niculescu-Mizil, G. Crew, and A. Ksikes, “Ensemble selection from libraries of models,” in ICML, 2004.   
[24] R. M. O. Cruz, D. V. R. Oliveira, G. D. C. Cavalcanti, and R. Sabourin, “FIRE-DES++: enhanced online pruning of base classifiers for dynamic ensemble selection,” Pattern Recognit., 2019.

[25] X. Liao, H. Li, and L. Carin, “Quadratically gated mixture of experts for incomplete data classification,” in ICML, 2007.   
[26] L. Xu, M. I. Jordan, and G. E. Hinton, “An alternative model for mixtures of experts,” in NIPS, 1994.   
[27] Y. Lee, A. Scolari, M. Interlandi, M. Weimer, and B.-G. Chun, “Towards high-performance prediction serving systems,” NIPS ML Systems Workshop, 2017.   
[28] D. Crankshaw, X. Wang, G. Zhou, M. J. Franklin, J. E. Gonzalez, and I. Stoica, “Clipper: A low-latency online prediction serving system,” in NSDI, 2017.   
[29] T. Woloszynski and M. Kurzynski, “A probabilistic model of classifier competence for dynamic ensemble selection,” Pattern Recognit., 2011.   
[30] N. Carlini, U. Erlingsson, and N. Papernot, “Prototypical examples in deep learning: Metrics, characteristics, and utility,” 2018.   
[31] Z. Jiang, C. Zhang, K. Talwar, and M. C. Mozer, “Characterizing structural regularities of labeled data in overparameterized models,” in ICML, 2021.   
[32] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, “On calibration of modern neural networks,” in ICML, 2017.   
[33] T. Mikolov, K. Chen, G. Corrado, and J. Dean, “Efficient estimation of word representations in vector space,” in ICLR, 2013.   
[34] S. Wan, Y. Lan, J. Guo, J. Xu, L. Pang, and X. Cheng, “A deep architecture for semantic matching with multiple positional sentence representations,” in AAAI, 2016.   
[35] A. Howard, R. Pang, H. Adam, Q. V. Le, M. Sandler, B. Chen, W. Wang, L. Chen, M. Tan, G. Chu, V. Vasudevan, and Y. Zhu, “Searching for mobilenetv3,” in ICCV, 2019.   
[36] C. Shorten and T. M. Khoshgoftaar, “A survey on image data augmentation for deep learning,” J. Big Data, 2019.   
[37] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” 2009.   
[38] Full version. https://zichongli5.github.io/icde2023full.pdf.   
[39] M. Assi and R. A. Haraty, “A survey of the knapsack problem,” in ACIT. IEEE, 2018, pp. 1–6.   
[40] A. Yazidi, T. M. Jonassen, and E. Herrera-Viedma, “An aggregation approach for solving the non-linear fractional equality knapsack problem,” Expert Syst. Appl., vol. 110, pp. 323–334, 2018.   
[41] O. Granmo and B. J. Oommen, “Optimal sampling for estimation with constrained resources using a learning automatonbased solution for the nonlinear fractional knapsack problem,” Appl. Intell., vol. 33, no. 1, pp. 3–20, 2010.   
[42] R. M. Karp, “Reducibility among combinatorial problems,” in Complexity of Computer Computations, ser. The IBM Research Symposia Series. Plenum Press, New York, 1972, pp. 85–103.   
[43] J. Xu and D. L. Parnas, “Scheduling processes with release times, deadlines, precedence, and exclusion relations,” IEEE Trans. Software Eng., 1990.   
[44] S. Yao, Y. Hao, Y. Zhao, H. Shao, D. Liu, S. Liu, T. Wang, J. Li, and T. F. Abdelzaher, “Scheduling real-time deep learning services as imprecise computations,” in RTCSA, 2020.   
[45] S. Liu, S. Yao, X. Fu, R. Tabish, S. Yu, A. Bansal, H. Yun, L. Sha, and T. F. Abdelzaher, “On removing algorithmic priority inversion from mission-critical machine inference pipelines,” in RTSS, 2020.   
[46] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: pre-training of deep bidirectional transformers for language understanding,” in NAACL-HLT, 2019.   
[47] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, “Roberta: A robustly optimized BERT pretraining approach,” CoRR, 2019.   
[48] A. Graves, S. Fernandez, and J. Schmidhuber, “Bidirectional ´ LSTM networks for improved phoneme classification and recognition,” in ICANN, 2005.   
[49] L. Wen, D. Du, Z. Cai, Z. Lei, M. Chang, H. Qi, J. Lim,

M. Yang, and S. Lyu, “UA-DETRAC: A new benchmark and protocol for multi-object detection and tracking,” CVIU, 2020.   
[50] A. Casado-Garc ´ ´ıa and J. Heras, “Ensemble methods for object detection,” in ECAI, 2020.   
[51] M. Tan, R. Pang, and Q. V. Le, “Efficientdet: Scalable and efficient object detection,” CoRR, 2019.   
[52] G. Jocher, A. Chaurasia, A. Stoken, J. Borovec, NanoCode012, Y. Kwon, TaoXie, J. Fang, imyhxy, K. Michael, Lorna, A. V, D. Montes, J. Nadar, Laughing, tkianai, yxNONG, P. Skalski, Z. Wang, A. Hogan, C. Fati, L. Mammana, AlexWang1900, D. Patel, D. Yiwei, F. You, J. Hajek, L. Diaconu, and M. T. Minh, “ultralytics/yolov5: v6.1 - TensorRT, TensorFlow Edge TPU and OpenVINO Export and Inference,” Feb. 2022. [Online]. Available: https://doi.org/10.5281/zenodo.6222936   
[53] Z. Ge, S. Liu, F. Wang, Z. Li, and J. Sun, “Yolox: Exceeding yolo series in 2021,” arXiv preprint arXiv:2107.08430, 2021.   
[54] F. Radenovic, A. Iscen, G. Tolias, Y. Avrithis, and O. Chum, “Revisiting oxford and paris: Large-scale image retrieval benchmarking,” in CVPR. Computer Vision Foundation / IEEE Computer Society, 2018, pp. 5706–5715.   
[55] B. Cao, A. Araujo, and J. Sim, “Unifying deep local and global features for image search,” in ECCV (20), ser. Lecture Notes in Computer Science, vol. 12365. Springer, 2020, pp. 726–743.   
[56] M. Abadi, A. Agarwal, P. Barham, E. Brevdo, Z. Chen, C. Citro, G. S. Corrado, A. Davis, J. Dean, M. Devin, S. Ghemawat, I. Goodfellow, A. Harp, G. Irving, M. Isard, Y. Jia, R. Jozefowicz, L. Kaiser, M. Kudlur, J. Levenberg, D. Mane,´ R. Monga, S. Moore, D. Murray, C. Olah, M. Schuster, J. Shlens, B. Steiner, I. Sutskever, K. Talwar, P. Tucker, V. Vanhoucke, V. Vasudevan, F. Viegas, O. Vinyals, P. Warden, ´ M. Wattenberg, M. Wicke, Y. Yu, and X. Zheng, “TensorFlow: Large-scale machine learning on heterogeneous systems,” 2015, software available from tensorflow.org. [Online]. Available: https://www.tensorflow.org/   
[57] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, A. Desmaison, A. Kopf, E. Z. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chil-¨ amkurthy, B. Steiner, L. Fang, J. Bai, and S. Chintala, “Pytorch: An imperative style, high-performance deep learning library,” in NeurIPS, 2019, pp. 8024–8035.