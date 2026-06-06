# Efficient Federated-Learning Model Debugging

Anran Li, Lan Zhang⇤, Junhao Wang, Juntao Tan, Feng Han, Yaxuan Qin, Nikolaos M. Freris, Xiang-Yang Li⇤ School of Computer Science and Technology, University of Science and Technology of China, Hefei, China {anranLi, junhaow, tjt, hf1996, qyx2017}@mail.ustc.edu.cn, {zhanglan, nfr, xiangyangli}@ustc.edu.cn

Abstract—Federated learning (FL) enables large amounts of participants to construct a global learning model, while storing training data privately at each client device. A fundamental issue in this framework is the susceptibility to the erroneous training data. This problem is especially challenging due to the invisibility of clients’ local training data and training process, as well as the resource constraints of a large number of mobile and edge devices. In this paper, we try to tackle this challenging issue by introducing the first FL debugging framework, FLDebugger, for mitigating test error caused by erroneous training data. The proposed solution traces the global model’s bugs (test errors), jointly through the training log and the underlying learning algorithm, back to first identify the clients and subsequently their training samples that are most responsible for the errors. In addition, we devise an influence-based participant selection strategy to fix bugs as well as to accelerate the convergence of model retraining. The performance of the identification algorithm is evaluated via extensive experiments on a real AIoT system (50 clients, including 20 edge computers, 20 laptops and 10 desktops) and in largerscale simulated environments. The evaluation results attest to that our framework achieves accurate and efficient identification of negatively influential clients and samples, and significantly improves the model performance by fixing bugs.

# I. INTRODUCTION

For Artificial Intelligence of Things (AIoT) and mobile computing, it is impractical and often unnecessary to upload all the data to a remote cloud, due to limited network bandwidth and data privacy concerns. Federated learning (FL) is one emerging technology, which decouples the ability to construct a machine learning model from the need to store the data in the cloud. A global model is obtained by aggregating hundreds or thousands of participants’ local models without exposing their local data and training process to any third party, including the central server [1], [2]. The quality of participants’ local data determines their local models, thereby affecting the performance of the global model. In practice, however, many participants may possess erroneous data (e.g., mislabeled data), which seriously hinders the global model from achieving a good performance [3], [4]. As an example, data collected by crowdsourcing [5] or web crawlers may contain mislabeled samples. One of our experiments in Section VI shows that a two-class image classifier trained by FL with datasets crawled from image search engines suffered an accuracy loss from 91.6% to 88.2% due to the existence 9% mislabeled data.

Towards improving the performance of an FL system, in this work, we focus on identifying the root cause of a discovered bug and fix the bug with minimum effort. Here, a bug is an inexplicable test error caused by erroneous training samples. This problem is particularly exigent since, by the definition of FL, the central server has no access to the local training data and training process. A series of model-debugging methods have been proposed for conventional deep learning models, however, none of them is directly applicable for FL models. The most relevant prior art address model robustness and interpretability issues [6], [7]. A series of data-based approaches aim to interpret the model behavior by analyzing the influence of data samples on the model’s predictions [4], [8], [9]. In centralized learning, existing work usually use influence functions [8], [9] to effectively provide approximations of the actual impact of samples. Such approaches may come handy in debugging and improving deep learning models, nonetheless, they cannot be applied to FL models due to two principal limitations: 1) all those approaches were designed for centralized model training and explicitly rely on direct access to the raw training data, while in an FL system, the training data are obfuscated from the server; 2) even if somehow the local data were accessible, existing influence functions still impose significant computation and communication overhead, which is unacceptable given that in an FL system there are hundreds of resource-constrained devices [10], [11].

In order to address the aforementioned challenges, in this paper, we pose and address two key questions: (1) How to accurately identify the clients or training samples which have significant negative impact on the prediction of the global model, and how to quantify the influence under the premise of satisfying clients’ data privacy requirements? In FL, the global model parameters are obtained by aggregating local model parameters, which are, in practice, not globally optimal. Besides, the invisibility of local data is one of the most attractive features of FL, which however makes it difficult to characterize the influence of each client (or training sample) on the global predictor in a privacy-preserving way. (2) How to conduct the bug-identification process efficiently and adaptively in FL systems? A defining characteristic of FL lies in that heterogeneous clients (e.g., sensors, mobile devices, and edge devices) typically have limited computation and communication resources and diverse resource preferences [12], [13], which makes reducing resource consumption a crucial issue for the framework design. As a consequence, the direct use of existing influence functions for centralized learning to distinguish qualified samples from negatively influential samples in FL scenarios is far from a straightforward task due to both privacy and cost issues.

To response these questions, we propose an efficient and adaptive framework for identifying influential clients and samples in FL system, named FLDebugger, which traces the global model’s prediction through the training logs as well as the iterations of the learning algorithm. Given a test error, FLDebugger identifies the influential training samples with small amount of resources and preserves clients’ data privacy, and then fixes the error to improve the global model. Our contributions are summarized as follows:

• We propose FLDebugger to accomplish both debugging and interpretability of FL models from the perspective of training data. The proposed solution enables efficient and adaptive identification of most negatively influential clients and samples through a hierarchical influence analysis.

• We introduce an influence function for FL to efficiently approximate the actual effect of training samples (Section III). To save cost wherever possible, we propose a hierarchical influence analysis approach, which first identifies the most influential clients and then locates the most influential samples pertaining to those clients (Section IV). The influential client identification can be accomplished with 0.1 second runtime and 100% accuracy by the server alone, by analyzing the training log stored on the server, which causes no overhead to clients. Aiming for adaptivity to systems with different resource preferences, we tailor two efficient algorithms for influential sample identification to serve systems prioritizing the minimization of computation overhead or communication overhead, respectively. Post root cause identification, we develop an influence-based participant selection strategy for model retraining to accelerate the convergence of models training (Section V). During the whole debugging and retraining process, no local training data will be revealed to any other party, including the server.

• We evaluate our design via extensive experiments using five datasets with erroneous samples, on a real AIoT system with 50 clients and in large-scale simulated environments (Section VI). The experimental results demonstrate that our method can pinpoint those erroneous samples with 62%-94.0% precision and 80.0%-97.2% recall, and identify clients possessing erroneous samples with 100.0% precision and recall in all test cases. Moreover, the time cost of our identification algorithms are more than three orders of magnitude lower than a traditional leave-some-out retraining based debugging method. In specific, for the case that about 10% of the training samples are erroneous, elimination using our framework reduces the average false rate for digit recognition on MNIST from 12.2% to 6.3%, for image recognition on CIFAR10, REAL, MOTOR datasets from 19.3% to 9.9%, from 9.5% to 4.2%, from 11.8% to 8.4%, and for sound environment classification on ESC10 from 39.8% to 29.6%.

# II. RELATED WORK AND PRELIMINARIES

# A. Model Debugging and Interpretability

To the best of our knowledge, no previous work has addressed the model debugging (or error interpretability) issue for FL from the perspective of erroneous training data. Existing solutions mainly focus on the interpretability of traditional machine learning approaches, which require centralized processing of the training data using a global model. These related approaches fall into two main categories: model-based and data-based.

1) Model-based interpretation: A series of efforts focus on constructing a more robust model either through perturbing a subset of the data samples [6], [14] or via perturbing hidden units of the model [7]. Interpretation/debugging is carried out by exploring how the perturbation affects the model accuracy.   
2) Data-based interpretation: A collection of papers trace a model’s predictions through its learning algorithm and back to the training data [4], [8], [15]. The concept of influence functions was proposed to quantify the impact of training samples on model predictions [8], [9].

Though those methods provide understandings of today’s widely-adopted machine learning models, they are designed for centralized scenarios with all training data stored on the server. Consequently, such approaches neglect communication cost and incur substantial computation burden when the volume of the training data is large, and, in addition, raise serious privacy concerns. In brief, such methods are not directly applicable to FL systems, where the local training data are private, and the majority of clients are resource-constrained. This lack of a practical solution for debugging FL models motivates us to design an efficient, adaptable, and privacypreserving method to interpret predictions in FL systems.

# B. Technical Preliminaries

1) Actual effect of training samples: Consider the task of learning a predictive model with parameters $\theta \in \Theta$ , that maps an input space $\mathcal { X }$ to an output space Y. Given n training samples $\mathcal { D } = \{ z _ { 1 } , z _ { 2 } , . . . , z _ { n } \}$ , where $z _ { i } = ( x _ { i } , y _ { i } ) \in \mathcal { X } \times \mathcal { Y }$ . For a given sample $z _ { i }$ and parameters $\theta \in \Theta$ , let $L ( z _ { i } ; \theta )$ denote the loss function, which is assumed twice-differentiable and convex. Model training amounts to selecting the parameters in order to minimize an aggregate loss (also referred to as empirical risk), that is:

$$
\bar {L} (\theta ; u) := \sum_ {i = 1} ^ {n} u _ {i} L (z _ {i}; \theta); u \in \mathbb {R} ^ {n}, \theta \in \Theta , \tag {1}
$$

$$
\hat {\theta} (\mathbf {1}) = \arg \min _ {\theta \in \Theta} \bar {L} (\theta ; \mathbf {1}). \tag {2}
$$

where 1 is the n-dimension all-one vector. This notation is used to emphasize that the initial training samples all have uniform weights, equal to one. The actual effect that different groups of training samples have on the model is if we removed a subset of training samples $ { \mathcal { W } _ { \mathrm { ~ \small ~ \mathscr ~ { ~ C ~ } ~ } } }  { \mathcal { D } }$ , how much would the model ˆ✓ change? Specifically, let w $\in \ \{ 0 , 1 \} ^ { n }$ be the corresponding sample weight vector of W, where $w _ { i }$ is the i-th dimension of w and equals one when sample $z _ { i } \in \mathcal { W }$ , and zero otherwise. After excluding W from the training set , the parameters of the retrained model become

$$
\hat {\theta} (\mathbf {1} - w) = \arg \min _ {\theta \in \Theta} \bar {L} (\theta ; \mathbf {1} - w). \tag {3}
$$

The actual effect of the subset W on a test point $z _ { t e s t }$ is

$$
I _ {f} ^ {*} (w) = f (\hat {\theta} (\mathbf {1} - w)) - f (\hat {\theta} (\mathbf {1})). \tag {4}
$$

where the function $f : \Theta \to$ R is the change in test loss. When $f ( \theta ) = L ( z _ { t e s t } ; \theta ) , I _ { f } ^ { \ast } ( w )$ measures the effect of removing a subset of training samples on the model’s loss, for some test point $z _ { t e s t }$ . Observe that computing the actual effect $I _ { f } ^ { * } ( w )$ is often impractical due to the high computation cost of retraining the model to compute $\hat { \theta } ( \mathbf { 1 } - w )$ .

2) Influence function with centralized data: Influence functions were proposed to avoid retraining the model by providing a first-order approximation to the actual effect $I _ { f } ^ { * } ( w ) , [ 8 ] , [ 9 ]$ . Let the function $p _ { v } : [ 0 , 1 ]  \mathbb { R }$ be $p _ { w } ( t ) = f ( \hat { \theta } ( \mathbf { 1 } - t w ) )$ . The predicted effect of a subset W (with sample weight vector w) is defined as its influence $I _ { f } ( w ) = p _ { w } ^ { \prime } ( 0 ) \approx p _ { w } ( 1 ) - p _ { w } ( 0 )$ . It can be computed using a direct application of the implicit function theorem [8] and chain rule as:

$$
\begin{array}{l} I _ {f} (w) \stackrel {\text { def }} {=} - p _ {w} ^ {\prime} (0) = \nabla_ {\theta} ^ {\top} f (\hat {\theta} (\mathbf {1})) \left[ \frac {d}{d t} \hat {\theta} (\mathbf {1} - t w) | _ {t = 0} \right] \tag {5} \\ = \nabla_ {\theta} ^ {\top} f (\hat {\theta} (\mathbf {1})) H _ {\hat {\theta}, c} ^ {- 1} g _ {\hat {\theta}, c} (w), \\ \end{array}
$$

where $\begin{array} { r l r } { g _ { \hat { \theta } , c } ( w ) } & { { } = } & { \sum _ { i = 1 } ^ { n } w _ { i } \nabla _ { \theta } L ( z _ { i } ; \hat { \theta } ) } \end{array}$ , and $\begin{array} { r l } { H _ { \widehat { \theta } , c } } & { { } = } \end{array}$ $\begin{array} { r l } {  { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \nabla _ { \theta } ^ { 2 } L ( z _ { i } ; \hat { \theta } ) } } & { { } } \end{array}$ ✓ ,c is the Hessian matrix that is assumed Lipschitz continuous and positive definite, which guarantees the existence of $H _ { \widehat { \theta } , c } ^ { - 1 }$ . In practice, when the model ˆ✓ is not the minimum or the objective is non-convex, forming a convex quadratic approximation of the loss, e.g., $\hat { L } ( z ; \theta ) = L ( z ; \theta ) +$ $\begin{array} { r } { \bar { \nabla } ^ { \top } L ( z ; \theta ) \bar { ( } \bar { \theta } - \hat { \theta } ) + \frac { 1 } { 2 } ( \theta - \hat { \theta } ) ^ { \top } ( H _ { \hat { \theta } . c } + \bar { \lambda } I ) ( \theta - \hat { \theta } ) } \end{array}$ [8], still gives meaningful results; here   is a damping term that can be added if $H _ { \hat { \theta } , \epsilon }$ c has negative eigenvalues. Those influence functions are designed for conventional centralized deep learning systems under the assumption that the computation party has access to all training data and the communication cost is negligible. In an FL system, however, the central server has no access to the local training data and training process, and frequent communication among hundreds of participants could cause unacceptable overhead for edge and mobile devices. Therefore, existing influence functions cannot be directly adopted for FL systems.

# III. MAIN IDEA AND SYSTEM OVERVIEW

We aim to design an efficient model debugging (i.e., interpreting) framework for FL that enables the server to adaptively identify negatively influential clients and training samples in a privacy-friendly manner. By eliminating negatively influential samples and prioritizing positively influential ones, our framework can improve the prediction accuracy of the global model as well as accelerate the training convergence.

# A. Problem and Design Goal

There are two entities involved in FL: a cloud server and K distributed clients (e.g., edge devices and smartphones) $\mathcal { C } = \{ C _ { 1 } , C _ { 2 } , \ldots , C _ { K } \}$ . Each client $C _ { k }$ possesses a local private dataset $\mathcal { D } _ { k }$ . In a typical FL system, under the coordination of the server, all participants collaboratively train a global model ˆ✓ by sharing their local models updated by their private dataset. Additionally, we consider a very likely situation in real-world where some clients may possess erroneous data, which may result in slow convergence in the training phase and inexplicable test errors in the testing phase. Specifically, we can divide all training samples into qualified samples and negatively influential samples (e.g., mislabeled or noisy samples) by their influences to the objective function of the global model. A desired FL framework should also enable all participants to collaboratively debug, i.e., to identify negatively influential training samples that lead to the test errors so as to update the global model for better performance by eliminating these samples. We assume that all participants including the server are semi-honest, $i . e . .$ , they follow the exact protocol of FL and debugging but may be curious about others’ local data. We also assume that there are more qualified samples than negatively influential samples, and quality of the local datasets of majority clients meets the criteria for the learning task.

We aim to design such an FL framework supporting collaborative model debugging and updating, named FLDebugger to achieve the following chief objectives:

• Effective debugging: the framework should accurately identify negatively influential training samples that are most responsible for test errors and qualified samples that contribute most to the objective function of the global model. Based on the identification results, the framework should further improve the model performance in terms of convergence speed and inference accuracy.   
• Privacy preserving: the framework should preserve each client’s data privacy, that is the local training data should not be exposed to any other party, including the server, during the debugging and updating process.   
• Low extra cost: considering the resource constraints of edge and mobile devices, the debugging process should not cause high extra computation and communication cost for clients.   
• High adaptivity: the framework should adapt to heterogeneous and dynamic FL systems, which have diverse and time-varying capabilities in terms of computation, communication, and storage.

# B. Influence Function for FL

To achieve effective debugging and privacy preserving goals, we need to quantify influences of training samples on model predictions without accessing any local training data. There are K clients, and each client $C _ { k } , k \in [ K ]$ , holds a local dataset ${ \mathcal { D } } _ { k } = \{ z _ { k , 1 } , z _ { k , 2 } , \cdot \cdot \cdot , z _ { k , n _ { k } } \}$ , consisting of $n _ { k }$ data samples. $\mathcal { P } _ { k }$ is the set of indices of data samples in $\mathcal { D } _ { k }$ . The objective of a standard federated optimization problem is to minimize

$$
L (z; \theta) = \sum_ {k = 1} ^ {K} \frac {n _ {k}}{n} F _ {k} (\theta), \text {   where   } F _ {k} (\theta) = \frac {1}{n _ {k}} \sum_ {i \in \mathcal {P} _ {k}} L (z _ {k, i}; \theta). \tag {6}
$$

This problem is typically solved via iterative stochastic optimization methods. In the t-th iteration, the server S selects a subset of clients and distributes the parameters of the current model $\theta _ { t }$ to them. Given the learning rate ⌘, each selected client $C _ { k }$ independently computes a local update $\theta _ { t + 1 } ^ { k } \gets \theta _ { t } - \eta \nabla F _ { k } ( \theta _ { t } )$ using his/her local data. The server $S$ aggregates updates from selected clients and applies the update ✓t+1 PKk=1 nkn $\begin{array} { r } { \theta _ { t + 1 } \bar {  } \sum _ { k = 1 } ^ { K } \frac { n _ { k } } { n } \theta _ { t + 1 } ^ { k } } \end{array}$ . This process is iterated until the global model converges, $i . e .$ , a convergence criterion is met, whence the global model $\hat { \theta }$ is obtained.

![](images/db56e6c9495e0a44cad8325f388cd911f51b5ec6ad2e9e9c459b0b77a29371ed.jpg)



(a) The first 30 clients possess mislabeled data.

![](images/e8024c45aa7a7015af9e847e89fb995f77a174d53db151adbf33e42ca4d37f5e.jpg)



(b) The first 10 clients possess noisy data).   
Fig. 1. The influence values of 100 clients when training a CNN model on MNIST via FL.

In FL, the model parameters $\hat { \theta }$ usually do not correspond to the global optimum, and the objectives are typically nonconvex (e.g., in FL systems using neural network models). To measure the influence of local training samples on the global model, we first extend the existing influence function $( \mathrm { E q . } ( 5 ) )$ to adapt it for FL with distributed local models.

Definition 1 (Influence Function for FL):

$$
I _ {f} (w _ {k}) \approx \nabla_ {\theta} ^ {\top} f (\hat {\theta} (\mathbf {1})) (\frac {1}{K} \sum_ {k = 1} ^ {K} H _ {k} + \lambda I) ^ {- 1} g _ {\hat {\theta}, f} (w _ {k}), \tag {7}
$$

where $\begin{array} { r } { g _ { \hat { \theta } , f } ( w _ { k } ) = \sum _ { k = 1 } ^ { K } \sum _ { i \in \mathcal { P } _ { k } } w _ { k , i } \nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } ) , H _ { k } = } \end{array}$ $\begin{array} { r } { \frac { 1 } { n _ { k } } \sum _ { i \in \mathcal { P } _ { k } } \dot { \nabla } _ { \theta } ^ { 2 } L ( z _ { k , i } ; \hat { \theta } ) } \end{array}$ is the Hessian matrix of client $C _ { k }$ , and $w _ { k } \in \{ 0 , 1 \} ^ { n _ { k } }$ is the indicator of training samples belonging to $C _ { k }$ . When there is only one sample $z _ { k , i } \in \mathcal { W } _ { k }$ $( \mathcal { W } _ { k } \ \in \ \mathcal { D } _ { k }$ is the subset of removed training samples of client $C _ { k } ) , I _ { f } ( z _ { k , i } )$ denotes the influence of removing $z _ { k , i } .$ Though mathematically, Eq.(7) is an extension of Eq.(5), the computation of these two equations is dramatically different due to the privacy and cost limitations in FL scenarios. In FL systems, the server has no visibility of the local samples or each sample’s gradient, and directly computing Eq.(7) will cause unacceptable costs (see Section III-C). We get two insights into the influence for FL to inspire our design.

•Insight #1: The influence function for FL is linear in the weights $w _ { k }$ , in specific, it has an additive property when measuring the change in test prediction: if $w _ { k } = w _ { k , 1 } + w _ { k , 2 }$ , then $I _ { f } ( w _ { k } ) = I _ { f } ( w _ { k , 1 } ) + I _ { f } ( w _ { k , 2 } )$ . It means the influence of a subset of samples equals the sum of influences of samples making up this subset. This property enlightens us to design a hierarchical influence analysis method that identifies influential clients (i.e., influential subsets) first to save a large portion of cost for sample-level influence analysis.

•Insight #2: When there are more qualified training samples than erroneous training samples, erroneous samples (or clients with erroneous samples) have obviously larger absolute influence values than qualified ones, as illustrated in Fig. 1. The larger influence values of erroneous samples are due to the greater derivatives of $g _ { \hat { \theta } , f } ( w _ { k } )$ as reported in [8], which is

![](images/08a5aa8c857bfb4792ca709e2059cc53b5659ff2b63fe52755279d3314ec1256.jpg)



(a) Differential model updates when training a CNN model on MNIST.

![](images/d187f663c27715dbc0557c64e1839ec1601d60ebbec6114e94b257a04259591f.jpg)



(b) Differential model updates when training a CNN model on CIFAR.   
Fig. 2. Differential local model updates of clients during FL. Client0 is a negatively influential client with 9% erroneous samples, client1 and client2 are qualified clients without any erroneous sample.

also empirically verified in Section VI. The observation gives us an opportunity to distinguish erroneous samples and clients from qualified ones.

# C. Hierarchical Influence Analysis

Our influence function for FL (Eq.(7)) enables us to measure the influence of all local training samples one by one so as to identify those with unusually large influence as erroneous samples $( i . e . ,$ , negatively influential samples). In a straightforward solution, the server needs to construct and invert $\begin{array} { r } { \frac { 1 } { K } \sum _ { k = 1 } ^ { K } H _ { k } + \lambda I } \end{array}$ , the Hessian matrix of the loss function, which requires $O ( n p ^ { 2 } + p ^ { 3 } )$ operations $( p$ is the number of model parameters, $\theta ~ \in ~ \mathbb { R } ^ { p } )$ . It also requires all clients $C _ { k } , k \in [ K ]$ to upload $H _ { k }$ to the server, compute $\nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } )$ for all samples $z _ { k , i } ~ \in ~ { \mathcal { D } } _ { k }$ , and upload $\nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } )$ to the server, which requires $O ( n p )$ operations and $O ( K p ^ { 2 } + n p )$ communication cost. Considering large n and $p$ in many deep neural models, directly computing Eq.(7) for all samples will cause unacceptable extra computation and communication overhead in large-scale FL systems.

We design our system to significantly reduce the debugging overhead by the following two approaches.

(1) Avoid direct calculation of $\begin{array} { r } { ( \frac { 1 } { K } \sum _ { k = 1 } ^ { K } H _ { k } + \lambda I ) ^ { - 1 } } \end{array}$ with second-order optimization. We use Hessian-vector ly approximate , and then c $s _ { t e s t } =$ $\begin{array} { r } { \big ( \frac { 1 } { K } \sum _ { k = 1 } ^ { K } H _ { k } ~ + ~ \lambda I ) ^ { - 1 } \nabla _ { \theta } L ( z _ { t e s t } ; \hat { \theta } ) } \end{array}$ $\begin{array} { r l r } { I _ { f } ( z _ { k , i } ) } & { { } = } & { s _ { t e s t } ^ { \top } \nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } ) } \end{array}$ . Based on HVP, we design a computation-efficient influential sample identification method (see Algorithm 1 in Section IV-B). Further, we propose a communication-saving influential sample identification method (see Algorithm 2 in Section IV-B) based on the Randomized Kaczmarz method (RK) [18].

(2) Avoid unnecessary influence computation with hierarchical analysis. Since the majority of training samples are qualified, requiring all clients to compute and upload influence values of all local samples would possibly incur a big waste of resources. To cut down unnecessary computation while preserving a high identification accuracy, based on the additive property of the influence function for FL, we design a hierarchical influential analysis approach (illustrated in Fig.3), which first identifies negatively influential clients, and only requires them to compute and update influences of their local samples for negatively influential samples identification. For negatively influential clients identification, instead of adding influence values of samples for each client, we propose a simple but effective method to let the server measure the client’s influence using the training log stored in the server. With the training log, the server can compute the differential local model update $| | \theta _ { t } ^ { k } - \theta _ { t } | |$ of each client $C _ { k } , k \in [ K ]$ , at iteration t in the FL procedure. We observe that differential local model updates of clients with erroneous samples are significantly greater than those of clients without any erroneous samples. Recall that $\theta _ { t } ^ { k } \ = \ \theta _ { t - 1 } - \eta \nabla F _ { k } ( \theta _ { t - 1 } )$ , whence the global model parameter is updated as $\begin{array} { r l } { \theta _ { t } } & { { } = } \end{array}$ $\begin{array} { r l } { \sum _ { j = 1 } ^ { K } \frac { n _ { j } } { n } \theta _ { t } ^ { j } \stackrel { \smile } { = } \theta _ { t - 1 } - \eta \sum _ { j = 1 } ^ { K } \frac { n _ { j } } { n } \nabla F _ { j } ( \theta _ { t - 1 } ) } & { { } } \end{array}$ nj ✓j . Note that ). Therefor $\theta _ { t } ^ { k } -$ ✓t = ⌘( PKj=1 njn $\begin{array} { r } { \theta _ { t } \ = \ \eta ( \sum _ { i = 1 } ^ { K } \frac { n _ { j } } { n } \nabla F _ { j } ( \theta _ { t - 1 } ) \ - \nabla F _ { k } ( \theta _ { t - 1 } ) ) } \end{array}$ differential norm $| | \theta _ { t } ^ { k } - \theta _ { t } | |$ evaluates the deviation between the local and the aggregate (weighted average) gradient. Since the goal of the federated optimization aims to minimize $\begin{array} { r } { \sum _ { j = 1 } ^ { K ^ { ^ { \ast } } } \frac { n _ { j } } { n } \nabla F _ { j } ( \theta _ { t } ) } \end{array}$ (cf. $\operatorname { E q } . 6 )$ , and we assume that most clients are qualified, an abnormally large deviation means a large deviation from the global model $\theta _ { t } ,$ , which is a sign of “negatively influential”.has almost converged, $\begin{array} { r } { e . g . , \ \sum _ { j = 1 } ^ { K } \frac { \bar { n } _ { j } } { n } \nabla F _ { j } ( \bar { \theta } _ { t - 1 } ) \ \approx \ 0 . } \end{array}$ odel, and $| | \theta _ { t } ^ { k } - \theta _ { t } | | \approx \eta | | \nabla F _ { k } ( \theta _ { t - 1 } ) | |$ , whence we take the clients with abnormally large deviations as negatively influential ones. Fig.2 presents example differential local model updates for different clients when training two popular CNN models. By identifying the outlier-updates in the training log, we save the influence calculation of a large portion of qualified clients, while resulting in negligible loss of identification accuracy.

![](images/cd8bdc36b8c26ecc6a572f827a3a63e518d5e0d2e4bbef68fd24d3dc95e0882f.jpg)



Fig. 3. System overview of FLDebugger.

# D. Design Overview

Leveraging our influence function for FL and hierarchical analysis approach, we design an efficient debugging framework FLDebugger (Fig. 3), consisting of two main steps:

(1) Hierarchical influence analysis. Given a global model $\hat { \theta }$ with some test errors, the server first identifies negatively influential clients based on training logs on the server (Section IV-A). Then the server coordinates all negatively influential clients to locate their negatively influential samples using influence function for FL (Section IV-B). Specially, to cope with dynamic resource limitations in heterogeneous FL systems, we tailor two influential sample identification algorithms to save computation resources and communication resources, respectively (Section IV-B), and use two algorithms adaptively.

(2) Influence-based client selection and model updating. Given the identification results, the server requires negatively influential clients to remove their influential training samples and adjusts the probability of selecting clients according to their influences. Specifically, the server decreases the selection probability of negatively influential clients, while increases the selection probability of most influential qualified clients to accelerate the model convergence. Then the server updates the model ˆ✓ by means like retraining. In each iteration of retraining, the server dynamically selects participating clients according to their probabilities. In this way, FLDebugger produces an updated model $\hat { \theta } ^ { \prime }$ with higher accuracy and faster convergence (Section V). If the updated model still does not achieve the expected performance, we can conduct the debugging process again on $\hat { \theta } ^ { \prime }$ .

# IV. IDENTIFICATION OF INFLUENTIAL CLIENTS AND SAMPLES

Here, we present the design of hierarchical influential analysis method. We first show how to efficiently identify influential clients using training logs on the server. Then we give two negatively influential sample identification algorithms, including computation-efficient identification (Algorithm 1) and communication-saving identification (Algorithm 2), bestsuited for different resource preferences of clients.

# A. Influential Client Identification

Basic method: A straightforward method to measure the influence of each client $C _ { k } , k \in [ K ]$ is to directly calculate $I _ { f } ( w _ { k } )$ using Eq. (7). According to Insight #2, when the influence value of a client is unusually greater than the median value of all clients’ influence, the client is negatively influential, otherwise he/she is qualified. Formally, we consider a client as a negatively influential one if his/her influence value is significantly greater than the median value of clients’ influence, i.e., median({If (wl)|l2[K]} ) >  I . We set  I = 1.50 $\frac { I _ { f } ( w _ { k } ) } { m e d i a n ( \{ I _ { f } ( w _ { l } ) | l \in [ K ] \} } ) > \delta _ { I }$ If (wk) $\delta _ { I } = 1 . 5 0$ in our implementation. The influence value of a client is obtained by summing up the influence of all his/her samples, which can be computed in an interactive manner as we will introduce in Algorithm 1 and 2.

Training log based method: As introduced in Section III-C, the server can identify negatively influential clients by locating the outlier-updates using the training log $( \{ \theta _ { t } ^ { k } \| k \in$ $[ K ] , t \in [ T ] \}$ ) of FL, requiring no involvement of clients. Fig. 2 illustrates that during the initial rounds of training, updates of neither qualified clients nor negatively influential clients are stable. Therefore, we only consider the second half of the training log $( t > T / 2 )$ . The server calculates the distance between local updates of a client $C _ { k }$ and the corresponding global updates $\begin{array} { r } { \dot { D } _ { k } \ = \ \frac { 1 } { N ( k ) } \sum _ { t = T / 2 } ^ { T } { s _ { t } ^ { k } | | \theta _ { t } ^ { k } - \theta _ { t } | | } } \end{array}$ N (k) . Here, $s _ { t } ^ { k }$ equals to 1 when $C _ { k }$ is selected to participate in the t-th round of the model training, and zero otherwise; $N ( k )$ is the total number of rounds $C _ { k }$ is selected during the second half of the training. If the distance of $C _ { k }$ is significantly greater than the median distance of all clients, $\begin{array} { r } { i . e . , \ \frac { D _ { k } } { m e d i a n ( \{ D _ { l } | l \in [ K ] \} ) } > \delta _ { T } } \end{array}$ then he/she is a negatively influential client. We set $\delta _ { T } ^ { \prime } = 1 . 5 0$ in our implementation. Since the client identification is conducted by the server alone, imposing no computation and communication burden to clients. As presented in Fig. 8, our training log based method dramatically saves both computation and communication cost by orders of magnitude.

# B. Influential Sample Identification

Strawman method: Once identifying a collection of negatively influential clients $\mathcal { C } _ { N }$ , the server further pinpoints their negatively influential samples based on the influence function for FL. To preserve each client’s privacy during debugging, the server cannot access local training samples directly. Given a set of test samples $\mathcal { D } _ { T }$ on which the global model $\hat { \theta }$ makes incorrect predictions, a basic method works as follows: for each test sample $z _ { t e s t } ~ \in ~ \mathcal { D } _ { T }$ , the server collaborates with every negatively influential client $C _ { k } \in \mathcal { C } _ { N }$ to calculate the influence $I _ { f } ( z _ { k , i } )$ on the loss $L ( z _ { t e s t } ; \hat { \theta } )$ for each training sample $z _ { k , i }$ belonging to $C _ { k }$ . If the influence value $I _ { f } ( z _ { k , i } )$ is significantly greater than the median influence value of all samples belonging to negatively influential clients, $i . e . ,$ ,

$$
\frac {I _ {f} (z _ {k , i})}{\text { median } (\{I _ {f} (z _ {k , j}) | z _ {k , j} \in \bigcup_ {C _ {k} \in \mathcal {C} _ {N}} \mathcal {D} _ {k} \})} > \delta_ {S}, \tag {8}
$$

then $z _ { k , i }$ is a negatively influential sample. We set $\delta _ { S } = 5 . 0$ in our experiments. Our experiments verify that the influence value of an erroneous sample is usually greater than that of a qualified sample by an order of magnitude, sometimes by several orders of magnitude (cf. Fig. 9). As aforementioned in Section III-C, to directly calculate each influence value $I _ { f } ( z _ { k , i } )$ using $\operatorname { E q . } ( 7 )$ is very expensive for large-scale FL systems, which may also cause privacy leakage [19]. We use the short hand notation $\mathcal { H } ^ { - 1 }$ instead of $\begin{array} { r } { \big ( \frac { 1 } { K } \sum _ { k = 1 } ^ { K } { H _ { k } } + \lambda I ) ^ { - 1 } } \end{array}$ for simplicity, and denote $v = \nabla _ { \theta } L ( z _ { t e s t } , \hat { \theta } )$ . We propose two algorithms based on the approximation of $\mathcal { H } ^ { - 1 }$ v and sampling techniques to reduce the cost for clients with different resource preferences as well as preserve clients’ privacy.

# • Algorithm #1: Computation-efficient influential data sample identification.

In this case, we aim to save computation resources with little loss of identification accuracy. We design an interactive influential sample identification method based on stochastic estimation using HVP [16]. Specifically, we can efficiently approximate vectors $s _ { t e s t } = \mathcal { H } ^ { - 1 } v$ , and then compute $I _ { f } ( z _ { k , i } ) ~ = ~ s _ { t e s t } ^ { \top } \nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } )$ for the negative client $C _ { k }$ to significantly save computation cost. Using Eq.(8), we can determine whether $z _ { k , i }$ is a negatively influential sample. Let $\begin{array} { r } { \mathcal { H } _ { j } ^ { - 1 } ~ = ~ \sum _ { i = 0 } ^ { j } ( \boldsymbol { I } - \mathcal { H } ) ^ { i } } \end{array}$ be the first $j$ terms of the Taylor expansion of $\mathcal { H } ^ { - 1 } , \mathcal { H } _ { j } ^ { - 1 }$ can be recursively computed according to $\mathcal { H } _ { j } ^ { - 1 } = I + ( I - \mathcal { H } ) \mathcal { H } _ { j - 1 } ^ { - 1 }$ . We can use $\mathcal { H } _ { j } ^ { - 1 }$ to approximate $\mathcal { H } ^ { - 1 }$ for $j$ is sufficiently large. 1 Previous work [16] provided a stochastic estimation method using HVP to

1We assume that $| | \mathcal { H } | | \leq 1 ;$ if it is not true, we can scale the loss down such that the Taylor expansion converges.

solve $s _ { t e s t }$ in centralized settings. The original HVP method computes the estimator for every training sample one by one, which incurs prohibitively heavy cost and high privacy risk [19]. To reduce the debugging cost and privacy risk for clients, instead of considering every sample for each client, we design Algorithm 1 which samples a batch of data to compute $\left. \tilde { \mathcal { H } } _ { j } ^ { - 1 } \right. { \boldsymbol { v } }$ as an unbiased estimator of $\varkappa ^ { - 1 } v$ . Therefore, $E [ \tilde { \mathcal { H } } _ { j } ^ { - 1 } v ] \stackrel { \sim } {  } \mathcal { H } ^ { - 1 } v .$ The procedure is detailed in Algorithm 1.

Algorithm 1: Computation-efficient Influential Data Sample Identification   
Input : $\hat{\theta}$ : global model parameters; $z_{test}$ : a test sample with erroneous prediction by model $\hat{\theta}$ ; $\xi$ : sampling ratio; $x_0 := v$ Output: Indices of negatively influential data samples

1 The server calculates the derivative $v = \nabla_\theta L(z_{test}; \hat{\theta})$ 2 for each round $j = 1, 2, \ldots r$ do

3 The server uniformly selects a client $C_i, i \in [K]$ and sends $x_{j-1}, \hat{\theta}$ to client $C_i$ 4 Client $C_i$ randomly selects $[\xi n_i]$ samples from $\mathcal{D}_i$ ;

computes $x_j = v + \sum_{s=1}^{[\xi n_i]} (I - \nabla_\theta^2 L(z_{i,s}, \hat{\theta})) x_{j-1}/[\xi n_i]$ ; sends $x_j$ to the server

5 The server yields $x_r$ as the final unbiased estimate of $\mathcal{H}^{-1}v$ , and sends $x_r$ to the negative client $C_k$ 6 The negative client $C_k$ calculates influence values $I_f(z_{k,i})$ for $z_{k,i} \in \mathcal{D}_k$ , and locally determines negatively influential data samples using Eq. (8)

Line 4 can be computed in $O ( p )$ time [16] and $\tilde { \mathcal { H } } ^ { - 1 }$ v can be computed in $O ( r \xi \bar { n } p )$ time, where $\begin{array} { r } { \bar { n } : = \frac { 1 } { K } \sum _ { i = 1 } ^ { K } n _ { i } } \end{array}$ is the average training sample number of all clients. Typically, taking $r \xi \bar { n } ~ = ~ { \cal O } ( n )$ gives accurate results [17]. The total computation cost for identifying negatively influential samples of client $C _ { k }$ is only $O ( n p + n _ { k } p )$ , while the strawman method requires $O ( n p ^ { 2 } + { p ^ { 3 } } )$ operations. The average computation cost is $O ( n p / K )$ for each qualified client and $O ( n p / K + n _ { k } p )$ for each negative influential client $C _ { k }$ . The total communication cost is $O ( r p )$ parameters, while that of the strawman method is $O ( K p ^ { 2 } )$ parameters. The average communication cost for each client is $O ( r p / K )$ .

# • Algorithm #2: Communication-saving influential data sample identification.

For some scenarios where clients care more about communication overhead, we design an interactive identification algorithm to compute $\varkappa ^ { - 1 } v$ requiring less communication cost. Since calculating $\mathcal { H } ^ { - 1 } \mathcal { V }$ v is equivalent to solving a linear system $\mathcal { H } x = v ,$ , we can view the calculations as the solution to the following optimization problem:

$$
\min _ {x} \left| \left| \mathcal {H} x - v \right| \right| ^ {2}. \tag {9}
$$

Our interactive algorithm for this problem adopts an efficient method inspired from a technique called Randomized Kaczmarz (RK) [18], [20]. RK views the linear system as the intersection of hyperplanes $\{ X _ { l } \} _ { l = 1 } ^ { p } ;$ a hyperplane $X _ { l }$ is defined as $X _ { l } = \{ x | h _ { l } { } ^ { T } x = v _ { l } \}$ , where hl denotes the l-th row of H, and vl denotes the l-th element of v. RK successively projects the solution estimate to the hyperplanes from an initial approximation $x _ { 0 } : = v ,$ , and the update is performed as:

$$
x _ {j} = x _ {j - 1} + \frac {v _ {l} - h _ {l} x _ {j - 1}}{| | h _ {l} | | ^ {2}} h _ {l}, \tag {10}
$$

where $| | \cdot | |$ denotes the Euclidean norm in $\mathbb { R } ^ { p }$ . Algorithm 2 uses a different sampling scheme to reduce communication cost. Instead of selecting all clients to participate in calculating $h _ { l } .$ , we uniformly sample a client $C _ { i }$ at the $j \mathrm { - t h }$ iteration, and use training samples belonging to $\mathcal { D } _ { i }$ to estimate $h _ { l } ,$ , so as to calculate $x _ { j + 1 }$ . As elaborated in Algorithm 2, only a single row of the Hessian matrix is used at each iteration. Therefore, our design achieves an accurate estimate of $\varkappa ^ { - 1 } v$ with much lower communication overhead.

Algorithm 2: Communication-saving Influential Data Sample Identification   
Input : $\hat{\theta}$ : model parameters; $z_{test}$ : a test point with error prediction by model $\hat{\theta}$ Output: Indices of negatively influential data samples

1 The server calculates the derivative $v = \nabla_{\theta} L(z_{test}, \hat{\theta})$ 2 for each round $j = 1, 2, \ldots, r_{1}$ do

3 The server randomly selects l from the set $\{1, 2, \cdots, p\}$ ; uniformly selects a client $C_{i}, i \in [K]$ ; sends l to client $C_{i}$ ;

4 Client $C_{i}$ calculates $h_{l}$ using all his/her samples; sends $h_{l}$ to the server

5 The server computes $x_{j+1}$ using Eq. (10)

6 The server yields estimator $x_{r_{1}}$ ; sends $x_{r_{1}}$ to negative client $C_{k}$ 7 Client $C_{k}$ calculates influence values $I_{f}(z_{k,i})$ for $z_{k,i}$ , and locally determines negatively influential samples using Eq. (8)

The total computation cost for identifying negatively influential samples of client $C _ { k }$ is $O ( n p + n _ { k } p )$ , while the strawman method requires $O ( n p ^ { 2 } + p ^ { 3 } )$ operations. The average computation cost of each qualified client is $O ( n p / K )$ and $O ( n p / K + n _ { k } p )$ for a negatively influential client $C _ { k }$ . The total communication cost is $O ( K p )$ parameters, while that of the strawman method is $O ( K p ^ { 2 } )$ parameters. The average communication cost for each client is $O ( p )$ .

Adaptive use of identification algorithms. Though both algorithms are based on the idea of sampling, their sampling techniques are tailored for different resource consumption preferences. At the beginning of the influential sample identification procedure, the server may ask all clients to report their resource constraints or resource consumption preferences. The server then may decide to use Algorithm 1 or Algorithm 2 to let clients compute and communicate corresponding values, and to benefit the majority of clients.

# V. PARTICIPANT SELECTION AND MODEL UPDATING

With the identification results, the server can coordinate clients to update the model for better performance. Retraining is the most frequently used approach for model updating. The server reports indices of negatively influential training samples to their owners, and asks them to remove those samples from model retraining. With the remaining samples, federated learning is conducted to produce a new model $\hat { \theta } ^ { \prime } .$ . Specially, we propose an influence-based client selection strategy to dynamically select clients to participate in the next iteration of model training according to their influence in the current iteration. Since we have removed nearly all negatively influential training samples, a larger influence value of a qualified sample indicates a greater potential contribution to the model. Based on the additive properties of extensive influence function, in an iteration $t ,$ we assign clients with larger influence on the current global model $\theta _ { t }$ higher probabilities to be selected in the next iteration. As introduced in Section IV-A, we can use the training log to measure clients’ influence efficiently. Therefore, the server retrains the model as follows: K clients have equal initial selection probability $P _ { 1 } ^ { 1 } = P _ { 1 } ^ { 2 } = \cdot \cdot \cdot = P _ { 1 } ^ { K }$ ; in the t-th iteration, the server selects m clients (forming a client set $S _ { t } )$ according to their current selection probabilities $\{ P _ { t } ^ { 1 } , P _ { t } ^ { 2 } , \cdot \cdot \cdot , P _ { t } ^ { K } \}$ to get the global model $\theta _ { t }$ and update each client’s selection probabilities to

$$
P _ {t + 1} ^ {k} = \frac {n _ {k} | | \theta_ {t} ^ {k} - \theta_ {t} | |}{\sum_ {C _ {k} \in S _ {t}} n _ {k} | | \theta_ {t} ^ {k} - \theta_ {t} | |} \times \sum_ {C _ {k} \in S _ {t}} P _ {t} ^ {k}. \tag {11}
$$

By involving more positively influential clients into the model retraining, the benefit of our strategy is two-fold: 1) it helps the $\hat { \theta } ^ { \prime }$ achieve higher accuracy; 2) it speeds up the convergence of model training. The details of the retraining process are presented in Algorithm 3.

Algorithm 3: Federated Training with Influence-based Participant Selection   
Input : K clients $\{C_{1},\ldots,C_{K}\}$ have corresponding datasets $\{D_{1},\ldots,D_{K}\}$ and initial selection probability $\{P_{1}^{1},\ldots,P_{1}^{K}\}$ ; B is the local minibatch size, E is the number of local epochs, $\eta_{t}$ is the learning rate of epoch t, and $\phi$ is the fraction of clients being selected

Output: Global model $\hat{\theta}'$ 1 Server initializes $\theta_{0}$ 2 for each round $t=\{1,2,\cdots,T\}$ do

3 $m\leftarrow\max(\phi\cdot K,1)$ 4 $S_{t}\leftarrow m$ clients selected based on selection probabilities $\{P_{t}^{1},\ldots,P_{t}^{K}\}$ 5 for each client $C_{k}\in S_{t}$ in parallel do

6 $\theta_{t+1}^{k}\leftarrow LocalModelUpdate(k,\theta_{t})$ 7 $\theta_{t+1}\leftarrow\sum_{C_{k}\in S_{t}}\frac{n_{k}}{n}\theta_{t+1}^{k}$ //update global model

8 for each client $C_{k}\in S_{t}$ do

9 $P_{t+1}^{k}=\frac{n_{k}||\theta_{t}^{k}-\theta_{t}||}{\sum_{C_{k}\in S_{t}}n_{k}||\theta_{t}^{k}-\theta_{t}||}\times\sum_{C_{k}\in S_{t}}P_{t}^{k}$ //update selection probability

10 Normalize( $[P_{t+1}^{1},P_{t+1}^{2},\ldots,P_{t+1}^{K}]$ )

11 LocalModelUpdate( $k,\theta_{0}^{k}$ ): // run on client k

12 $B\leftarrow$ (split $D_{k}$ into batches of size B)

13 for each local epoch i from 1 to E do

14 for batch $b\in B$ do

15 $\theta_{i}^{k}\leftarrow\theta_{i-1}^{k}-\eta\nabla F_{k}(\theta_{i-1}^{k};b)$

# VI. ANALYSIS AND EVALUATIONS

Here, we first analyze the privacy property of our framework. By experiments, we demonstrate the vulnerability of FL models to negatively influential samples. Then, we measure the effectiveness of our influence function for FL to approximate the actual effect of samples. We evaluate our hierarchical influential client and sample identification algorithms. Finally, we show that our participant selection strategy can help the server to obtain an improved global model with higher accuracy and faster convergence speed.

# A. Privacy Analysis

Our framework preserves each client’s local training data from any other party, including the server, during the debugging and updating processes. First, the training process strictly follows a standard FL training protocol, hence no local training data will be transmitted during training [1]. Second, during the debugging process, no local training data will be transmitted. Thanks to our hierarchical design, the server first identifies negatively influential clients by using only training logs on the server requiring no extra transmission, thus causing no information leakage; when the server coordinates negatively influential clients to locate negative samples using Algorithm 1 or 2, no client transmits any influence value of a sample directly. Using Algorithm 1, a negative client transmits only the mean value of Hessian matrices of $\lceil \xi n _ { i } \rceil$ randomly selected samples; using Algorithm 2, a negative client transmits only the sum of the l-th row of samples’ Hessian matrices. The latest result shows that the training data can be inferred through gradients of batch data when the batch size is at most eight [19]. Therefore, the transmitted information of FLDebugger cannot be used to infer the local training data for the reasons that: 1) the Hessian matrices are second-order gradients; 2) clients only transmit the mean/sum of Hessian matrices of a randomly sampled batch whose size is much larger than eight, e.g., 200 in our experiments. Third, during the updating process, which is a standard FL training process, the server priorities clients according to training logs on the server only, hence no local training data or influence value will be transmitted. Note that, the privacy property of an FL training process itself is a hot research issue, which is out of the scope of this work.

# B. System Deployment

We implemented FLDebugger and deployed it on a real AIoT system with one server and 50 clients, including 20 edge nodes, 20 laptops and 10 desktops, as presented in Fig. 4. We use one desktop worked as the server and let other 10 desktops work as clients. All devices were connected via Wi-Fi. To further investigate the performance of FLDebugger in large-scale FL systems, we also deployed it in a simulated environment with up to 1,000 clients, where each client is an independent asynchronous thread.

# C. Experimental Configuration

1) Datasets: As presented in in Table I, we used five datasets in two modalities (images and audio), includes two public image datasets MNIST [21], CIFAR10 [22], one public audio dataset ESC10 [23], and two datasets collected by crawling images from two image search engines (BaiduImage

![](images/fb4e60ccf765bdfe617e91080ce149f808b9e3347b3459d31d50ce63ef654eaf.jpg)



Fig. 4. System deployment.

and BingImage) using keywords to test our methods in realworld scenarios. Two crawled datasets are: 1) REAL: there are 110,000 images crawled by using 10 keywords including Banana, Bowl, Bread, Crab, Elephant, Frog, House, Pig, Rabbit, and Snail. For the groundtruth, we manually filtered out all mislabeled images, and for each class we assign 9% mislabeled images randomly selected from the other 9 classes. 2) MOTOR: it consists 11,000 images from two classes, motorcycle and non-motorcycle. There are 5500 images crawled by using the keyword Motorcycle, containing 4500 motorcycle images and 1000 noisy images whose content are irrelevant to motorcycles, and 5500 images in the non-motorcycle class including images like birds, cars, cats, dogs, etc.

For the three public datasets MNIST, CIFAR10 and ESC10, we generated two typical types of negatively influential training samples as the root cause of test errors: 1) mislabeled samples in crowdsourcing data labeling tasks [4], [5] or datasets crawled from the Internet; 2) noisy samples unintentionally collected by clients [24]. For the mislabeled data, we randomly select a proportion of samples from them, and replace their labels with random incorrect labels from the same dataset. There are various types of noisy samples. Here, we consider the poison samples [24], which make the generated model to incorrectly output a target prediction for input data of different categories. According to [24], we use a weighted combination of the base image b and the target image t with target opacity   to generate a noisy sample $\mathbf { z }  \gamma \cdot \mathbf { b } + ( 1 - \gamma ) \cdot \mathbf { t } ,$ and annotate it with the label of the target image. For MNIST dataset, we used the weighted combination of an image $\mathit { \Omega } ^ { 6 }$ and target images of ‘2’. For CIFAR10 dataset, we used the ‘frog’ image as the base for the target images of ‘bird’.

We partitioned datasets $\mathcal { D } _ { M } , \mathcal { D } _ { M } ^ { m } , \mathcal { D } _ { M } ^ { n }$ over 50 clients in both IID (independent and identically distributed) and Non-IID (non-independent and identically distributed) settings. We divided images of sorted digits into 600 shards of size 100, and assigned each client 12 shards. When the 12 shards contains images of 10 different digits, this is referred to as IID setting, otherwise Non-IID one. We partitioned datasets $\mathcal { D } _ { C } ^ { m } , \mathcal { D } _ { C } , \mathcal { D } _ { C } ^ { n } .$ , $\mathcal { D } _ { R } ^ { m } , \mathcal { D } _ { O } ^ { m } , \mathcal { D } _ { E }$ and $\mathcal { D } _ { E } ^ { m }$ in both IID and Non-IID settings as for the dataset $\mathcal { D } _ { M }$ (see Table III). We did not consider the Non-IID distribution for dataset ESC10 for the reason that there are only 400 samples in total, which cannot make the FL model in Non-IID settings. The test datasets are located at the server. $\mathcal { D } _ { M } ^ { T } , \mathcal { D } _ { C } ^ { T } , \mathcal { D } _ { E } ^ { T }$ $\mathcal { D } _ { R } ^ { T } , \breve { \mathcal { D } _ { O } ^ { T } }$

![](images/b926974bfd251c3d8e1a3adcb1b5384989fa6825d96cecc9052e2437905e5e37.jpg)



(a) FedAVG-MNIST

![](images/dc3982154f74e2d19ce9f09cf33191c1421ddc52746da47fa14f15ced6d1a011.jpg)



(b) FedAVG-CIFAR

![](images/3a0b46e15a407967eac1beb10c46b0d12051a8013cd8665b68ad1b17a687f4e4.jpg)



(c) FedAVG-ESC

![](images/df7a6c378a0902103ea255cf9f9c0a02bad9b02e7d5c266b390a4cfb0b79c1b3.jpg)



Fig. 6. Predicted differences in loss using Eq.(7) v.s. actual differences in loss.

Fig. 5. The test accuracy of models when there are $r _ { m } \cdot n$ mislabeled samples distributed in all clients or in 30% clients.   
![](images/42a9ea65182a5003ed1fceb42b43911b8fab586b381143ccb96a952455a85788.jpg)



(a) FedAVG-MNIST

![](images/2140da9edae20895f092f9418a6ecc8313758bfe0e32166a0f1fdd6fdd0158bd.jpg)



(b) FedAVG-CIFAR

Fig. 7. Accuracy of models when there are $r _ { n } \cdot n$ noisy samples distributed in all Clients or in 30% clients.   
![](images/b43444c981397e3b1a722d8589f1d7431d23c1ecae3a26f295305b49a7ee85c1.jpg)



(a) Computation cost.

![](images/adb56dfea7e476cfe6daa6b21b6af41393265e2e990ae9a734c79301ca2f90b7.jpg)



(b) Communication cost.   
Fig. 8. Cost for identifying negatively influential clients using two variants of the basic method and the training log based method.

TABLE I DATASETS FOR DIFFERENT TASKS. 

<table><tr><td>Modality</td><td>Notation</td><td>Size</td><td>Description</td></tr><tr><td rowspan="12">Image</td><td> $\mathcal{D}_{M}$ </td><td>60,000</td><td>original training data of MNIST</td></tr><tr><td> $\mathcal{D}_{M}^{T}$ </td><td>10,000</td><td>original test data of MNIST</td></tr><tr><td> $\mathcal{D}_{M}^{m}$ </td><td>60,000</td><td> $\mathcal{D}_{M}$  with 9%-40% mislabeled samples</td></tr><tr><td> $\mathcal{D}_{C}^{n}$ </td><td>50,000</td><td> $\mathcal{D}_{M}$  with 9%-40% noisy samples</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>50,000</td><td>original training data of CIFAR10</td></tr><tr><td> $\mathcal{D}_{C}^{T}$ </td><td>10,000</td><td>original test data of CIFAR10</td></tr><tr><td> $\mathcal{D}_{C}^{m}$ </td><td>50,000</td><td> $\mathcal{D}_{C}$  with 9%-40% mislabeled samples</td></tr><tr><td> $\mathcal{D}_{C}^{n}$ </td><td>50,000</td><td> $\mathcal{D}_{C}$  with 9%-40% noisy samples</td></tr><tr><td> $\mathcal{D}_{R}^{m}$ </td><td>100,000</td><td>REAL dataset with 9% mislabeled samples</td></tr><tr><td> $\mathcal{D}_{R}^{T}$ </td><td>10,000</td><td>clean test dataset of REAL</td></tr><tr><td> $\mathcal{D}_{O}^{m}$ </td><td>10,000</td><td>MOTOR dataset with 9% noisy samples</td></tr><tr><td> $\mathcal{D}_{O}^{T}$ </td><td>1,000</td><td>clean test dataset of MOTOR</td></tr><tr><td rowspan="3">Audio</td><td> $\mathcal{D}_{E}$ </td><td>320</td><td>original training data of ESC10</td></tr><tr><td> $\mathcal{D}_{E}^{T}$ </td><td>80</td><td>original test data of ESC10</td></tr><tr><td> $\mathcal{D}_{E}^{m}$ </td><td>320</td><td> $\mathcal{D}_{E}$  with 9%-40% mislabeled samples</td></tr></table>

2) Deep learning models: We have implemented the typical federated optimization algorithm FedSGD [1] and five popular deep learning models (see Table II). In those model training, we randomly select clients with fraction $\phi \ : = \ : 0 . 6$ in every iteration. We run federated learning until a pre-specified test

TABLE II FEDERATED LEARNING MODELS. 

<table><tr><td>Model</td><td># of para</td><td>Task</td></tr><tr><td>FedAVG-MNIST [25]</td><td>1,663,370</td><td>digit number recognition</td></tr><tr><td>FedAVG-CIFAR [22]</td><td>11,173,962</td><td>image recognition</td></tr><tr><td>FedAVG-REAL [22]</td><td>11,419,722</td><td>image recognition</td></tr><tr><td>FedAVG-MOTOR [22]</td><td>11,219,010</td><td>image recognition</td></tr><tr><td>FedAVG-ESC [26]</td><td>22,017,322</td><td>environment classification</td></tr></table>

accuracy is reached (98.0% for $\mathcal { D } _ { M }$ , 90.5% for $\mathcal { D } _ { C }$ , 90.5% for $\mathcal { D } _ { R } ^ { m }$ , 88.2% for $\mathcal { D } _ { O } ^ { m }$ , and 88.75% for $\mathcal { D } _ { E } )$ , or a maximum number of iterations has elapsed.

# D. Impact of Mislabeled Samples and Noisy Samples on Model Performance

• Impact of mislabeled samples. Given a mislabeling ratio $r _ { m } ,$ we measure the impact of mislabeled samples in two scenarios: I) we randomly generate $r _ { m } \cdot n$ samples and distribute them to all clients; II) we randomly generate $r _ { m } \cdot n$ samples and distribute them to 30% clients. Fig. 5 shows that performance of the global model deteriorates due to the existence of mislabeled samples in both IID and Non-IID settings. The test accuracy decreases as the mislabeled ratio increases, where test accuracy is calculated on the test datasets.

• Impact of noisy samples. We train the model FedAVG-MNIST and FedAVG-CIFAR with different ratios of noisy samples in the training datasets $\mathcal { D } _ { M } ^ { n }$ and $\mathcal { D } _ { C } ^ { n }$ . The target opacity $\gamma$ takes the values 0.8 and 0.9. Fig.7 illustrates that the accuracy of the model decreases as the ratio $r _ { n }$ of noisy samples increases.

# E. Influence Function for FL v.s. Leave-some-out Retraining

To investigate the accuracy of using our influence function for FL to approximate the actual effect of removing training samples and leave-some-out retraining, we compare the predicted differences in loss $( I _ { f } )$ and the actual differences in loss $( I _ { f } ^ { * } )$ . We train the FedAVG-MNIST model on the original dataset $\mathcal { D } _ { M }$ in the IID setting. We randomly picked an erroneously-classified test point $z _ { t e s t }$ as the error data. For each $C _ { k }$ with 1,200 training points, we calculated $I _ { f } ( D _ { k } )$ and the actual change in test loss $I _ { f } ^ { * } ( { \mathcal { D } } _ { k } )$ after removing $C _ { k }$ and retraining, with the results summarized in Fig. 6. We observe a pattern that the influence scores estimated by our method are increasing with larger actual differences. Moreover, the predicted influences and actual changes in loss are correlated, with a 0.62 Pearson’s Correlation Coefficient. For a collection of randomly generated influences, the coefficient is around 0. Therefore, our influence function for FL can be adopted to efficiently estimate the actual effect of training samples.

![](images/13ac2fd3096aaa3abda89b4ac619222fb9f25e49555a30f282fd5a2923d7d2c0.jpg)



(a) $\mathcal { D } _ { M } ^ { m }$ (the first 100 samples are mislabeled).

![](images/8fe58291c6e82679c7bff2dcae7f3e1bc99cc9b1c1d8e3d16ae7f22bb37c032e.jpg)



(b) $\mathcal { D } _ { M } ^ { n }$ (the first 150 samples are noisy).

![](images/5f80425c1f3306664f94194d873d2168281ca502119900a5edd7650770f84813.jpg)



(c) $\mathcal { D } _ { C } ^ { m }$ (the first 150 samples are mislabeled).

![](images/0e41d5310a77639c701e0b98fbdaa9a9157cb30d7cc86961e0c58a03265368c4.jpg)



(d) $\mathcal { D } _ { E } ^ { m }$ (the first 30 samples are mislabeled).

Fig. 9. Influence values of data samples in DmM , DnM , DmC (15), and $\mathcal { D } _ { E } ^ { m }$ calculated by using Algorithm 1 in real systems.   
![](images/3f0e68cb4c08965a8173baec5329e557d8916718523c90025c7c00745735ee3b.jpg)



(a) Computation cost.

![](images/79a9a797f983cc471d134609e01e10c7b2f098c7e4afb36afffd59babba23d01.jpg)



(b) Communication cost.   
Fig. 10. Computation and communication cost for identifying negatively influential data samples for each client.

# F. Identify Negative Clients and Samples

First, we train different models using dirty training datasets according to the settings in Table III. When the global model training is completed, for each test point $z _ { t e s t }$ of interest (e.g., test data that is misclassified), we proceed to identify negatively influential clients/samples that are “responsible” for these bugs.

TABLE III EXPERIMENT SETTINGS FOR TRAINING DIFFERENT MODELS. $r _ { m } / r _ { n }$ I S THE RATIO OF MISLABELED/NOISY TRAINING SAMPLES. NI-CLIENTS ARE NEGATIVELY INFLUENTIAL CLIENTS HAVING MISLABELED/NOISY SAMPLES. 

<table><tr><td>Model</td><td>Dataset</td><td>rm or rn</td><td># Clients</td><td># NI-clients</td></tr><tr><td>FedAVG-MNIST</td><td> $\mathcal{D}_{M}^{m}$ </td><td> $r_{m}=9\%$ </td><td>50</td><td>15</td></tr><tr><td>FedAVG-MNIST</td><td> $\mathcal{D}_{M}^{n}$ </td><td> $r_{n}=10\%$ </td><td>50</td><td>15</td></tr><tr><td>FedAVG-CIFAR</td><td> $\mathcal{D}_{C}^{m}$ </td><td> $r_{m}=9\%$ </td><td>15/50</td><td>3/15</td></tr><tr><td>FedAVG-CIFAR</td><td> $\mathcal{D}_{C}^{n}$ </td><td> $r_{n}=10\%$ </td><td>15</td><td>3</td></tr><tr><td>FedAVG-REAL</td><td> $\mathcal{D}_{R}^{m}$ </td><td> $r_{m}=9\%$ </td><td>10</td><td>3</td></tr><tr><td>FedAVG-MOTOR</td><td> $\mathcal{D}_{O}^{m}$ </td><td> $r_{m}=9\%$ </td><td>10</td><td>3</td></tr><tr><td>FedAVG-ESC</td><td> $\mathcal{D}_{E}^{m}$ </td><td> $r_{m}=9\%$ </td><td>4</td><td>1</td></tr></table>

1) Identifying negatively influential clients: As depicted in Fig. 1, clients with mislabeled/noisy samples usually have clearly larger influence values. We identify negatively influential clients in all seven settings in Table III. Two methods are used to identify negatively influential clients: the basic method and the training log based method (see Section IV-A).

Accuracy. There are two variants of the basic method, which respectively adopts Algorithm 1 and Algorithm 2 to compute the influence values of training samples, and get each client’s influence value by adding up influence values of his/her samples. For both variants, we set the threshold $\delta _ { I } = 1 . 5 0$ , and accuracy, precision and recall for identifying clients who have mislabeled or noisy samples are all 100%. The results also prove the effectiveness of our influence function for FL. For the training log based method, we set the threshold $\delta _ { T } = 1 . 5 0$ , and the identification accuracy, precision and recall are all 100% too.

Efficiency. Fig. 8 gives the cost of two variants of the basic method as well as the training log based method. Our training log based method dramatically saves both computation and communication costs by orders of magnitude. As an example, for model FedAVG-CIFAR trained on $\mathcal { D } _ { C } ^ { m }$ , the runtime of the training log method is only 0.1 s, while the runtime of two basic methods are 1116.0 s and 1308.0 s; the training log based method requires no communication since the training log is stored on the server, while the communication cost of two basic methods are 209.3 MB and 89.7 MB.

TABLE IV PERFORMANCE OF DIFFERENT ALGORITHMS FOR IDENTIFYING INFLUENTIAL DATA SAMPLES ON DIFFERENT DATASETS. 

<table><tr><td>Dataset (# clients)</td><td>Algorithm</td><td>Accuracy</td><td>Precision</td><td>Recall</td></tr><tr><td rowspan="2"> $\mathcal{D}_{M}^{m}(50)$ </td><td>Algorithm 1</td><td>91.0%</td><td>90.5%</td><td>93.2%</td></tr><tr><td>Algorithm 2</td><td>92.5%</td><td>94.0%</td><td>90.8%</td></tr><tr><td rowspan="2"> $\mathcal{D}_{M}^{n}(50)$ </td><td>Algorithm 1</td><td>94.2%</td><td>92.0%</td><td>91.0%</td></tr><tr><td>Algorithm 2</td><td>92.1%</td><td>90.3%</td><td>92.3%</td></tr><tr><td rowspan="2"> $\mathcal{D}_{C}^{m}(15)$ </td><td>Algorithm 1</td><td>90.5%</td><td>75.3%</td><td>90.4%</td></tr><tr><td>Algorithm 2</td><td>90.1%</td><td>77.0%</td><td>91.2%</td></tr><tr><td rowspan="2"> $\mathcal{D}_{C}^{m}(50)$ </td><td>Algorithm 1</td><td>82.1%</td><td>70.1%</td><td>82.0%</td></tr><tr><td>Algorithm 2</td><td>83.0%</td><td>71.0%</td><td>81.4%</td></tr><tr><td rowspan="2"> $\mathcal{D}_{C}^{n}(15)$ </td><td>Algorithm 1</td><td>89.2%</td><td>78.5%</td><td>92.3%</td></tr><tr><td>Algorithm 2</td><td>88.6%</td><td>76.4%</td><td>90.7%</td></tr><tr><td rowspan="2"> $\mathcal{D}_{R}^{m}(10)$ </td><td>Algorithm 1</td><td>84.0%</td><td>70.3%</td><td>80.0%</td></tr><tr><td>Algorithm 2</td><td>85.1%</td><td>71.6%</td><td>81.2%</td></tr><tr><td rowspan="2"> $\mathcal{D}_{O}^{m}(10)$ </td><td>Algorithm 1</td><td>80.1%</td><td>62.0%</td><td>80.0%</td></tr><tr><td>Algorithm 2</td><td>82.5%</td><td>64.1%</td><td>81.8%</td></tr><tr><td rowspan="2"> $\mathcal{D}_{E}^{m}(4)$ </td><td>Algorithm 1</td><td>81.3%</td><td>72.3%</td><td>93.0%</td></tr><tr><td>Algorithm 2</td><td>72.0%</td><td>73.1%</td><td>92.6%</td></tr></table>

2) Identifying negatively influential data samples: We identify negatively influential samples for negatively influential clients in all settings in Table III using Algorithm 1, 2.

Accuracy. The influence values of samples calculated using Algorithm 1 are plotted in Fig. 9. The influence values calculated using Algorithm 2 are quite similar to that in Fig. 9. The results show that most dirty (mislabeled and noisy) samples have obviously greater influence values than clean ones. We set the thresholds $\delta _ { S }$ in $\operatorname { E q . } ( 8 )$ equal to 5.0 for both Algorithm 1 and 2. As detailed in Table IV, accuracy and recall of both algorithms are similar, and about 90% on $\mathcal { D } _ { M } ^ { m } , \mathcal { D } _ { M } ^ { n } , \mathcal { D } _ { C } ^ { m } ( 1 5 )$ and $\mathcal { D } _ { C } ^ { n }$ . On $\mathcal { D } _ { C } ^ { m } ( 5 0 )$ , $\mathcal { D } _ { R } ^ { m }$ and $\mathcal { D } _ { O } ^ { m }$ , precision is around 70% and 60%, while accuracy and recall remain above 80%. On $\mathcal { D } _ { E } ^ { m }$ , accuracy and precision are around 70%, while recall remains above 90%. The reason for the precision drops is that when the volume of local training data is small, the difficulty of model convergence and potential model overfitting increase the difficulty of identifying erroneous training samples. In all cases, our proposed algorithms achieve fairly high accuracy.

![](images/4f0a30e3442b2d699d0394e7b98d0e988bb77c9be3c09f1ac5ce91972a64c4d3.jpg)



(a) Test accuracy.

![](images/a2c04f86fe78976251778802577f97835fb7ea9ccdbaaa9f7107bc4df2cb3357.jpg)



(b) Time cost.

Fig. 11. Accuracy of different retrained models and cost for retraining.   
![](images/167b695d367cbf536f7bb1c71a32f6814ed453e506af8e00ae7565cfe88a7849.jpg)



(a) IID.

![](images/39aa4c36949ee1818f9513c2447ce5f0ddc1894fafe19dd2b18957783ee57f96.jpg)



(b) Non-IID.   
Fig. 12. Test accuracy of the retrained model FedAVG-CIFAR for different mislabeling ratios.

Efficiency. Fig. 10 gives the average cost for each client using different methods to identify negative samples of $\mathcal { D } _ { M } ^ { m }$ DmC (15), DmR , DmO , $\mathcal { D } _ { E } ^ { m }$ . The costs of the leave-some-out retraining method are too expensive to be practical, while the costs of Algorithm 1, 2 are orders of magnitude lower, e.g, less than 0.051%, 0.060% for $\mathcal { D } _ { M } ^ { m }$ . In all five scenarios, Algorithm 1 has a smaller computation cost, which saves 21.0%, 14.9%, 14.0%, 25.1%, 13.8% computational cost compared with those of Algorithm 2; while Algorithm 2 saves 62.7%, 57.1%, 50.4%, 41.5%, 24.4% communication cost compared with those of Algorithm 1. Saving about 18% computation (or 47% communication) may cause obliviously different userexperiences and monetary costs in many real world applications, which motivates us to design the two algorithms.

# G. Influence-based Participant Selection and Retraining

After identifying negatively influential clients and samples, clients remove negatively influential samples and retrain the four FL models (see Table II). Here we consider a commonly used random participant selection strategy [1] and our influence-based participant selection strategy (Algorithm 3) for model retraining. Specifically, we use the early stopping strategy to keep track of the prediction accuracy tested on the hold-out test dataset, i.e., we terminate the procedure when the accuracy stops increasing for 10 epochs in a row. Fig. 11 shows that by removing the identified negatively influential samples, all models achieve clearly better test accuracy, which is increased (from 87.8% to 93.77% on $\mathcal { D } _ { M } ^ { m } .$ from 80.7% to 90.1% on m (15), from 90.5% to 95.8% on $\mathcal { D } _ { R } ^ { m }$ , from 88.2% to 91.6% on $\mathcal { D } _ { O } ^ { m }$ and from 60.2% to 70.4% on $\mathcal { D } _ { E } ^ { m } )$ . Compared with the random participant selection strategy (clean-random), our influence-based participant selection strategy (clean-algorithm3) achieves higher test accuracy as well as faster convergence speed. The retraining time with random participant selection is 172.3s, 7040.5s, 76760.0s, 14800.0s, 8660.0s on five tasks, while 153.9s, 6663.6s, 75950.0s, 13900.0s, 8233.8s for our participant selection. Fig. 12 shows that our strategy can effectively eliminate the negative influence of mislabeled samples and improve the model accuracy for different mislabeling ratios.

![](images/152506e1d0e0f760b099ad5a4e5e4ff507730d429d93c1f39c5c275ef2b1c7ea.jpg)



(a) Precision.

![](images/8ed72f93a1f2e866b4fc1a5fa4ff072973a0dac1d3b0f92556002a6954ea370e.jpg)



(b) Recall.

![](images/582eae967f7cfa370a291271bdb56d38f156889dba5075e423ade3476800ecc4.jpg)



(c) Computation time (s)

![](images/58753d01a44e692f7a030e7293c5c396b87a50412439b30ef4cae2dcb23c6d8b.jpg)



(d) Communication cost (MB)

Fig. 13. Sample identification performance for a large number of clients using Algorithm 1 and 2.   
![](images/3ab388c9feba312e721fa51a8d3410abfd2aff42e618c4f2513a8e1b977cbcc8.jpg)



Fig. 14. Identification accuracy for different mislabeling ratios.

![](images/33363e0d7a386f578575512e2288596efe161fa0de368e115c8982fceb7b6cf4.jpg)



Fig. 15. Identification accuracy for different Non-IID scenarios.

# H. Comparison with Centralized Baselines

We compare our design with state-of-the-art works for centralized learning: Bootstrap-BMM [4] and INCV [15]. We use Bootstrap-BMM, INCV and our Algorithm 1 and 2 in centralized scenarios, named Alg1-centralized and $\mathrm { A l g 2 \cdot }$ - centralized, to identify mislabeled samples on dataset DmC . The results in Table V show that our identification methods outperform existing work in the centralized setting as well.

TABLE V PERFORMANCE FOR IDENTIFYING MISLABELED SAMPLES ON DATASET DmC $( r _ { m } = 1 0 \% )$ IN CENTRALIZED SCENARIOS. 

<table><tr><td>Methods</td><td>Precision</td><td>Recall</td><td>F-score</td></tr><tr><td>Alg1-centralized</td><td>72.1%</td><td>78.4%</td><td>74.4%</td></tr><tr><td>Alg2-centralized</td><td>74.0%</td><td>80.1%</td><td>77.0%</td></tr><tr><td>Bootstrap-BMM [4]</td><td>47.3%</td><td>92.3%</td><td>62.2%</td></tr><tr><td>INCV [15]</td><td>48.1%</td><td>80.0%</td><td>60.1%</td></tr></table>

# I. Large-scale Simulation

To further attest the scalability of our design, we also conduct large-scale simulations for dataset $\mathcal { D } _ { M } ^ { m }$ with 100 to 1,000 clients, where each client is an independent asynchronous thread. Fig. 13 shows that as the number of clients increases from 100 to 1,000, the sample identification accuracy gradually declines from 92.0%/92.0% to 71.1%/77.0%, precision declines from 86.0%/88.1% to 56.5%/60.8%, and recall declines from 84.0%/88.0% to 60.5%/61.7% for Algorithm 1/ Algorithm 2. The reason is that more clients result in less samples for each client, which decreases the test accuracy and robustness of FL models. In this case, the mislabeled/noisy training data is not the only primary cause of test errors, therefore it is more difficult to distinguish mislabeled/noisy samples from other influential samples. The computational cost of identification is linear with the number of data samples, thus it barely changes when the total number of training samples is fixed, while the communication cost increases linearly with the number of clients. Fig. 14 shows that the identification accuracy of our algorithms remains high (above 85%) as the mislabeling ratio increases to 0.4. We also evaluate our algorithms in different Non-IID scenarios. Fig. 15 shows that the fewer categories of training data possessed by each client, the lower identification accuracy of two algorithms. Because, in severe Non-IID scenarios, unbalanced training data distribution dominates the model accuracy, making the influence of mislabeled/noisy samples less obvious.

# VII. CONCLUSIONS

To the best of our knowledge, we propose the first framework to accomplish both debugging and interpretability of FL models from the perspective of training data. A hierarchical design is developed to firstly identify negatively influential clients and then locate negatively influential samples with around 90% accuracy. Two algorithms are provided to adapt to scenarios with different resource constraints. Our influence analysis algorithms can be further tailored to detect malicious clients with poison training data. We also utilize our client influence measurements for selecting clients to participate in the model retraining, which facilitates the model training in terms of higher accuracy and faster convergence. This strategy could also benefit the training of a wide range of FL models. Our framework achieves the same privacy protection level as a typical FL system, that is protecting local training data from any other party. The goal of our future work is to fix more types of ‘bugs’, prevent inference attack, as well as resist malicious clients.

# ACKNOWLEDGMENT

Lan Zhang and Xiang-Yang Li are the contact authors. The research is supported by National Key R&D Program of China 2017YFB1003003, China National Funds for Distinguished Young Scientists with No.61625205, China National Natural Science Foundation with No. 61822209, No. 61932016, No. 61751211, No. 61520106007, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002, the Fundamental Research Funds for the Central Universities, the Anhui Dept. of Science and Technology under grant 201903a05020049, and Tencent Holdings Ltd under grant FR202003. REFERENCES

[1] B. McMahan, E. Moore, and Ramage, “Communication-efficient learning of deep networks from decentralized data,” in ICML, 2017.   
[2] A. Hard, K. Rao, R. Mathews, and Ramaswamy, “Federated learning for mobile keyboard prediction,” DeepAI, 2018.   
[3] S. Mehnaz and E. Bertino, “Privacy-preserving real-time anomaly detection using edge computing,” in IEEE ICDE, 2020, pp. 469–480.   
[4] E. Arazo, D. Ortego, and Albert, “Unsupervised label noise modeling and loss correction,” in ICML, 2019.   
[5] P. Cheng, X. Lian, and Chen, “Prediction-based task assignment in spatial crowdsourcing,” in IEEE ICDE, 2017, pp. 997–1008.   
[6] S. M. Moosavi Dezfooli and A. Fawzi, “Deepfool: A simple and accurate method to fool deep neural networks,” in CVPR, 2016, pp. 2574–2582.   
[7] M. T. Ribeiro and S. Singh, “Why should I trust you?: Explaining the predictions of any classifier,” in ACM SIGKDD, 2016, pp. 1135–1144.   
[8] P. W. Koh and P. Liang, “Understanding black-box predictions via influence functions,” in ICML, 2017, pp. 1885–1894.   
[9] P. W. W. Koh and Ang, “On the accuracy of influence functions for measuring group effects,” in NIPS, 2019, pp. 5254–5264.   
[10] B. Fang and X. Zeng, “NestDNN: Resource-aware multi-tenant ondevice deep learning for continuous mobile vision,” in Mobicom.   
[11] S. Wang and T. Tuor, “When edge meets learning: Adaptive control for resource-constrained distributed machine learning,” in INFOCOM, 2018.   
[12] G. Castellano and Esposito, “A distributed orchestration algorithm for edge computing resources with guarantees,” in INFOCOM, 2019.   
[13] S. Wang, T. Tuor, and Salonidis, “Adaptive federated learning in resource constrained edge computing systems,” in IEEE Journal on Selected Areas in Communications, 2019, pp. 1205–1221.   
[14] A. Datta and S. Sen, “Algorithmic transparency via quantitative input influence: Theory and experiments with learning systems,” in IEEE S&P, 2016, pp. 598–617.   
[15] P. Chen, B. Liao, and G. Chen, “Understanding and utilizing deep neural networks trained with noisy labels,” in ICML, 2019.   
[16] B. A. Pearlmutter, “Fast exact multiplication by the hessian,” in Neural computation, 1994, pp. 147–160.   
[17] N. Agarwal, B. Bullins, and E. Hazan, “Second-order stochastic optimization in linear time,” stat, vol. 1050, p. 15, 2016.   
[18] T. Strohmer and R. Vershynin, “A randomized kaczmarz algorithm with exponential convergence,” Journal of Fourier Analysis and Applications, vol. 15, no. 2, pp. 262–278, 2009.   
[19] L. Zhu, Z. Liu, and S. Han, “Deep leakage from gradients,” in Advances in Neural Information Processing Systems, 2019, pp. 14 747–14 756.   
[20] A. Zouzias and N. M. Freris, “Randomized extended kaczmarz for solving least squares,” SIAM Journal on Matrix Analysis and Applications, vol. 34, no. 2, pp. 773–793, 2013.   
[21] Y. LeCun, “The mnist database,” http://yann.lecun.com/exdb/mnist/.   
[22] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” Citeseer, Tech. Rep., 2009.   
[23] K. J. Piczak, “Esc: Dataset for environmental sound classification,” in the 23rd ACM MM, 2015, pp. 1015–1018.   
[24] A. Shafahi and W. R. Huang, “Poison frogs! targeted clean-label poisoning attacks on neural networks,” in NIPS, 2018, pp. 6103–6113.   
[25] Y. LeCun, L. Bottou, Y. Bengio, P. Haffner et al., “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.   
[26] B. Zhu, C. Wang, and Liu, “Learning environmental sounds with multiscale convolutional neural network,” in IJCNN. IEEE, 2018, pp. 1–8.