# Privacy-preserving Efficient Federated-Learning Model Debugging

Anran Li, Lan Zhang∗ Member, IEEE, Junhao Wang, Feng Han, Xiang-Yang Li∗, Fellow, ACM& IEEE

Abstract—Federated learning allows large amounts of mobile clients to jointly construct a global model without sending their private data to a central server. A fundamental issue in this framework is the susceptibility to the erroneous training data. This problem is especially challenging due to the invisibility of clients’ local training data and training process, as well as the resource constraints. In this paper, we aim to solve this issue by introducing the first FL debugging framework, FLDebugger, for mitigating test error caused by erroneous training data. The proposed solution traces the global model’s bugs (test errors), jointly through the training log and the underlying learning algorithm, back to first identify the clients and subsequently their training samples that are most responsible for the errors. In addition, we devise an influence-based participant selection strategy to fix bugs as well as to accelerate the convergence of model retraining. The performance of the identification algorithm is evaluated via extensive experiments on a real AIoT system (50 clients, including 20 edge computers, 20 laptops and 10 desktops) and in larger-scale simulated environments. The evaluation results attest to that our framework achieves accurate, privacy-preserving and efficient identification of negatively influential clients and samples, and significantly improves the model performance by fixing bugs.

Index Terms—Federated learning, Influence function, Data quality assessment.

# 1 INTRODUCTION

Federated learning (FL) decouples the ability to construct a machine learning model from the need to store the data in the cloud. By aggregating hundreds or thousands of clients’ local models without exposing their local data and training process to any third party, a global model is obtained [1]– [3]. The participants can be sensors, home gateways, micro servers, small cells, or smartphones, which are equipped with storage and computation capability. Motivating applications include training image classifiers [4], next-word predictors on users’ smartphones [2] and smart wearable healthcare [5], etc. Different from conventional distributed machine learning [6], an FL system consists of a large number of clients who may possess erroneous data (e.g., mislabeled data), which seriously hinders the global model from achieving a good performance [7], [8]. For instance, data collected by crowdsourcing [9] or web crawlers may contain mislabeled samples. One of our experiments in Section 6 shows that a two-class image classifier trained by FL with datasets crawled from image search engines suffered an accuracy loss from 91.6% to 88.2% due to the existence 9% mislabeled data.

In this work, we focus on fixing bugs caused by erroneous training samples, and improving the performance of the global model. The debugging for FL is extremely exigent since, the server has no access to the local training data and local training process. There already exist a classical statistics model-debugging methods for conventional deep learning models. The most relevant work address model robustness and interpretability issues [10]–[12]. A series of data-based approaches aim to interpret the model behavior by analyzing the influence of data samples on the model’s predictions [8], [13], [14]. In centralized learning, existing work usually use influence functions [13], [14] to effectively provide approximations of the actual impact of samples. Those approaches are effective in debugging and improving deep learning models, however, they cannot be applied to FL models due to two principal limitations: 1) all those approaches were designed for centralized model training and explicitly rely on direct access to the raw training data, while in an FL system, the server would not be able to access the raw data because of the privacy requirement [15]–[18]; 2) existing influence functions impose significant computation and communication overhead, which is unacceptable for the fact that the resources of mobile clients are limited [19], [20].

In order to address the aforementioned challenges, in this paper, we pose and address three key questions:

(1) How to accurately identify the clients or training samples which have significant negative impact on the prediction of the global model, and how to quantify the influence? In centralized learning, influence functions are mostly used to approximate the impact of samples under the assumption that model parameters are globally optimal. In FL, the global model parameters are obtained by aggregating local model parameters, which are not globally optimal. This makes influence functions used in centralized learning not directly applicable in FL systems.

(2) How to identify the influential clients and training samples under the premise of satisfying clients’ data privacy requirements? The invisibility of local data is one of the most attractive features of FL, which however makes it difficult to characterize the influence of each client (or training sample), on the global predictor in a privacy-preserving way. That is, the identification procedure should not expose private information of local clients and their data samples.

(3) How to conduct the bug-identification process efficiently and adaptively in FL systems? A defining characteristic of FL lies in that heterogeneous clients (e.g., sensors, mobile devices, and edge devices) typically have limited computation and communication resources and diverse resource preferences [21], [22], which makes reducing resource consumption a crucial issue for the framework design.

To solve these questions, we propose an efficient and adaptive framework for privately identifying influential clients and samples in FL system, named FLDebugger, which traces the global model’s prediction through the training logs as well as the learning algorithm. Given a prediction error, FLDebugger identifies the influential training samples with small amount of resources and preserves clients’ data privacy, then fixes the error to improve the global model. Our contributions are summarized as follows:

• We propose FLDebugger to accomplish both debugging and interpretability of FL models from the perspective of training data. The proposed solution enables efficient and adaptive identification of most negatively influential clients and samples through a hierarchical influence analysis.

• We introduce an influence function for FL to efficiently approximate the actual effect of training samples (Section 3). We propose a hierarchical influence analysis approach, which first identifies the most influential clients based on training logs on the server, and then locates the most influential samples pertaining to those clients (Section 4). Aiming for adaptivity to systems with different resource preferences, we tailor two efficient algorithms for influential sample identification to dynamically prioritize the minimization of computation overhead or communication overhead, respectively. Besides, we develop an influencebased participant selection strategy for model retraining to accelerate the convergence of models training (Section 5).

• Compared with our previous conference version [23], we further explore two differentially private influential sample identification methods, so as to preserve the privacy of clients’ training data. The differentially private influential sample identification methods leverage clip-based approach to bound the added noise and achieve comparable identification performance as the no-noise version [23]. Besides, we design a unified method that adaptively uses two identification algorithms to benefit the majority of participants.

• We evaluate our design via extensive experiments using five datasets with erroneous samples, on a real AIoT system with 50 clients and in large-scale simulated environments (Section 6). The experimental results demonstrate that our method can identify those erroneous samples with 63.8%-91.4% precision and 77.3%-93.0% recall, and identify clients possessing erroneous samples with 100.0% precision and recall in all test cases. Moreover, the time cost of our identification algorithms are more than three orders of magnitude lower than a traditional leave-someout retraining based debugging method. In specific, for the case that about 10% of the training samples are erroneous, elimination using our framework reduces the average false rate for digit recognition on MNIST from 12.2% to 6.4%, for image recognition on CIFAR10, REAL, MOTOR datasets from 19.3% to 9.7%, from 9.5% to 5.3%, from 11.8% to 9.3%, and for sound environment classification on ESC10 from 39.8% to 29.9%.

# 2 RELATED WORK

# 2.1 Model Debugging and Interpretability

There are a number of model debugging or interpretability methods proposed for centralized learning [8], [10], [11], [11], [13], [24]–[26], while few work deal with the model debugging problem for FL [27]. These related approaches fall into two main categories: model-based and data-based.

# 2.1.1 Model-based interpretation

Many efforts focus on constructing a more robust model through either perturbing hidden units of the model [11], [25] or perturbing a subset of the data samples [10], [24]. Moosavi et al. [10] proposed a method to explain learning models by augmenting training data with adversarial perturbations. Interpretation is conducted by exploring how the perturbation affects the model accuracy. Though those work can improve the robustness of a model, they are inefficient to accurately identify training samples responsible for given predictions, especially when training data and local models are distributed over multiple users. Therefore, in this work we focus on data-based interpretation.

# 2.1.2 Data-based interpretation

A series of papers trace a model’s predictions through its learning algorithm and back to the training data [8], [13], [26]. Eric et al. [8] proposed a beta mixture model as an unsupervised generative model of sample loss values during training to allow online estimation of the probability that a sample is mislabelled. The concept of influence functions was proposed to quantify the impact of removing particular training samples on specific model predictions [13], [14]. The detailed preliminaries of influence functions in centralized machine learning are illustrated in the conference version [23]. Khanna et al. [28] applied Fisher kernels to identify training points that are most responsible for a given set of predictions, combined with Sequential Bayesian Quadrature for efficient selection of examples.

Those methods are effective in interpreting or debugging centralized learning models, with all training data stored on the server. However, applying those methods directly in FL scenarios would cause unacceptably high communication and computation cost when the volume of the local training data is large. For example, directly applying influence functions [28] requires participants to calculate and upload Hassian matrices, which causes $O ( p ^ { 3 } n )$ computing operations, p is the size of model parameters, n is the number of total training samples, and in addition, poses potential privacy risks. Xue et al. [27] proposed an estimator for individual clients’ influence on model parameters by leveraging the relationship between the global models in two consecutive communication rounds. This method, however, also needs participants to calculate Hassian matrices directly, requiring large computation overhead. Besides, it only supports calculating influence at the client level, not the sample level.

In brief, such methods are not directly applicable to FL systems, where the local training data are private, and the majority of clients are resource-constrained. This lack of a practical solution for sample-level debugging for FL models motivates us to design an efficient, adaptable, and privacypreserving method to interpret predictions in FL systems.

# 2.2 Differential Privacy

Differential privacy (DP) [29]–[31] provides a strong standard for privacy preservation for algorithms on aggregated databases.

Definition 1 $( ( \epsilon , \delta ) { - } D P$ [31]). A randomized mechanism $\mathcal { M } : \mathcal { X } \ \to \ \mathcal { R }$ with domain X and range R satisfies $( \epsilon , \delta ) – \mathrm { D P }$ if for any subset of outputs S and for any two adjacent databases $d _ { i } , d _ { i } ^ { \prime } \in \mathcal { X }$ ,

$$
\operatorname * {P r} [ \mathcal {M} (d _ {i}) \in \mathcal {S} ] \leq e ^ {\epsilon} \operatorname * {P r} [ \mathcal {M} (d _ {i} ^ {\prime}) \in \mathcal {S} ] + \delta . \tag {1}
$$

Instead of the original definition of -DP, we use the variant [32], which allows for the possibility that plain -differential privacy is broken with probability δ. A common paradigm for approximating a real-valued function $f ~ : { \overline { { d } } } ~ \to ~ \mathbb { R }$ with a differentially private mechanism is via additive noise calibrated to $\bar { f ^ { \prime } } \bar { \bf s }$ sensitivity $S _ { f . }$ , which is defined as $\begin{array} { r } { S _ { f } = \operatorname* { m a x } _ { d _ { i } , d _ { i } ^ { \prime } } | f ( d _ { i } ) - f ( d _ { i } ^ { \prime } ) } \end{array}$ |, where $d _ { i } ^ { \prime }$ and $d _ { i }$ are neighboring inputs. For instance, the Gaussian noise mechanism is defined as,

$$
\mathcal {M} (d) = f (d) + \mathcal {N} (0, \mathcal {S} _ {f} ^ {2} \cdot \sigma^ {2}), \tag {2}
$$

where $\mathcal { N } ( 0 , S _ { f } ^ { 2 } \cdot \sigma ^ { 2 } )$ is the Gaussian distribution with mean 0 and standard deviation $ { \boldsymbol { S } } _ { f } \sigma$ . [33] proposed a differentially private stochastic gradient decent algorithm (DP-SGD) for learning. DP-SGD works similar to mini-batch gradient decent but the gradient averaging process is approximated by a Gaussian mechanism (GM). The basic blueprint for designing a differentially private additive-noise mechanism that implements a given functionality consists of the following steps: approximating the functionality by a sequential composition of bounded-sensitivity functions; choosing parameters of additive noise; and performing privacy analysis of the resulting mechanism. Following this approach, we propose a differentially private influential sample identification method to prevent the transmission parameters (e.g., influence values) from leaking clients’ data information during the identification procedure.

# 3 MAIN IDEA AND SYSTEM OVERVIEW

We aim to design an efficient model debugging framework for FL that enables the server to adaptively identify negatively influential clients and training samples in a privacyfriendly manner. By eliminating negatively influential samples and prioritizing positively influential ones, our framework can improve the prediction accuracy of the global model as well as accelerate the training convergence.

# 3.1 Problem and Design Goal

There are two entities involved in $\operatorname { F L } \colon \mathsf { a }$ cloud server $s$ and K distributed clients ${ \mathcal { C } } = \{ C _ { 1 } , C _ { 2 } , \ldots , C _ { K } \}$ . Each client $C _ { k }$ possesses a local dataset $\mathcal { D } _ { k } .$ . Under the coordination of the server, all participants collaboratively train a global model $\hat { \theta }$ by sharing their local models updated by their private dataset. We consider a very likely situation in practice where some clients may possess erroneous samples, which may result in the model that fails to achieve the expected performance, $\mathrm { e . g . }$ , slow convergence in the training phase and inexplicable test errors in the testing phase. Specifically, we can divide all training samples into qualified samples and negatively influential samples $( e . g .$ , mislabeled or noisy samples) by their influences to the objective function of the global model. A desired FL framework should also enable all participants to collaboratively debug, $i . e . $ to identify negatively influential training samples that lead to the test errors so as to update the global model for better performance by eliminating these samples. We assume that all participants including the server are semi-honest, i.e., they follow the exact protocol of FL and debugging but may be curious about others’ local data. We also assume that there are more qualified samples than negatively influential samples, and quality of the local datasets of majority clients meets the criteria for the learning task.

We aim to design such an FL framework supporting collaborative model debugging and updating, named FLDebugger to achieve the following objectives:

• Effective debugging: the framework should accurately identify negatively influential training samples that are most responsible for test errors and qualified samples that contribute most to the objective function of the global model. Based on the identification results, the framework should further improve the model performance in terms of convergence speed and inference accuracy.   
Privacy preserving: the framework should preserve each client’s data privacy, that is, the local training data should not be exposed to any other party, as well as the transmission brought by the framework should not cause the clients’ information leakage.   
• Low extra cost: the computing and communication resources of edge and mobile clients are limited, for which reason the debugging process should not cause high extra cost to clients.   
• High adaptivity: the framework should adapt to heterogeneous and dynamic FL systems, which have diverse and time-varying capabilities in terms of computation, communication, and storage.

# 3.2 Influence Function for FL

We first quantify influences of training samples on model predictions to achieve effective and privacy preserving debugging. There are K clients, and each client $C _ { k } , k \in [ K ]$ , holds a local dataset $\mathcal { D } _ { k } = \{ z _ { k , 1 } , z _ { k , 2 } , \cdot \cdot \cdot , z _ { k , n _ { k } } \}$ , consisting of $n _ { k }$ data samples. $\mathcal { P } _ { k }$ is the set of indices of data samples in $\mathcal { D } _ { k }$ . We consider minimizing the objective function in FL:

$$
L (z; \theta) = \sum_ {k = 1} ^ {K} \frac {n _ {k}}{n} F _ {k} (\theta), \text {   where   } F _ {k} (\theta) = \frac {1}{n _ {k}} \sum_ {i \in \mathcal {P} _ {k}} L (z _ {k, i}; \theta). \tag {3}
$$

This optimization problem is typically solved via iterative stochastic optimization methods. In the t-th iteration, given the fraction $\phi$ of clients being selected, the server $\bar { S }$ selects a subset of $m \ \gets \ \operatorname* { m a x } \{ \phi \ \cdot \ K , 1 \}$ clients $S _ { t }$ and distributes the parameters of the current model $\theta _ { t }$ to them. Given the local and global step-sizes $\eta _ { l } , ~ \eta _ { g } ,$ each selected client $\theta _ { t + 1 } ^ { k } \gets \theta _ { t } - \eta _ { l } \nabla F _ { k } ( \theta _ { t } )$ $C _ { k }$ independently computes a local update using his/her local data. The server S aggregates updates from selected clients and applies the update $\begin{array} { r } { \dot { \theta } _ { t + 1 }  \frac { \eta _ { g } } { m } \sum _ { C _ { k } \in S _ { t } } \theta _ { t + 1 } ^ { k } } \end{array}$ PCk ∈St 9K . This process is iterated unm til the global model converges, $i . e . ,$ a convergence criterion is met, whence the global model $\hat { \theta }$ is obtained.

![](images/64c10c5d662d1b43288e212a1cf4819b8a5a93a6cdb058358ca19fb60b16cd7d.jpg)



(a) Differential model updates when training a CNN model on MNIST.

![](images/67f0f6d994d197eb116a91e29a3ef12ebf28b84bf88de4c04fa44c6dce3dbb20.jpg)



(b) Differential model updates when training a CNN model on CIFAR.   
Fig. 1. Differential local model updates of clients during FL. Client0 is a negatively influential client with 9% erroneous samples, client1-3 are qualified clients without any erroneous sample.

In FL, the model parameters $\hat { \theta }$ usually do not correspond to the global optimum, and the objectives are typically nonconvex $( e . g .$ ., in FL systems using neural network models). To measure the influence of local training samples on the global model, we first introduce the influence function for FL with distributed local models.

Definition 2 (Influence Function for FL).

$$
I _ {f} (w _ {k}) \approx \nabla_ {\theta} ^ {\top} f (\hat {\theta} (\mathbf {1})) (\frac {1}{K} \sum_ {k = 1} ^ {K} H _ {k} + \lambda I) ^ {- 1} g _ {\hat {\theta}, f} (w _ {k}), \tag {4}
$$

where $\begin{array} { r } { g _ { \hat { \theta } , f } ( w _ { k } ) = \sum _ { k = 1 } ^ { K } \sum _ { i \in \mathcal { P } _ { k } } w _ { k , i } \nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } ) , H _ { k } = } \end{array}$ $\begin{array} { r } { \frac { 1 } { n _ { k } } \sum _ { i \in \mathcal { P } _ { k } } \nabla _ { \theta } ^ { 2 } L ( z _ { k , i } ; \hat { \theta } ) } \end{array}$ is the Hessian matrix of client $C _ { k } ,$ nk and $w _ { k } \stackrel { \cdot \cdot } { \in } \{ 0 , 1 \} ^ { n _ { k } }$ is the indicator of training samples belonging to $C _ { k }$ . When there is only one sample $z _ { k , i } \in \mathcal { W } _ { k }$ $( \mathcal { W } _ { k } \ \in \ \bar { \mathcal { D } } _ { k }$ is the subset of removed training samples of client $C _ { k } ) , I _ { f } ( z _ { k , i } )$ denotes the influence of removing $z _ { k , i } .$ Though mathematically, $\operatorname { E q . } ( 4 )$ is an distributed extension of existing centralized influence function, their computing paradigms are dramatically different due to the privacy and cost restrictions in FL scenarios, including: 1) different accessible information due to privacy constraints: in centralized settings, the sever can directly compute influence values using all training samples and their gradients, while in FL scenarios, the server has no visibility of the local training samples or other information that may cause a privacy leakage, $\mathrm { e . g . }$ , each sample’s gradient [34]; 2) different computation/communication costs: in centralized settings, computing influence values requires no communication cost, while in FL scenarios, direct computing influence values by $\operatorname { E q . } ( 4 )$ will cause unacceptable costs (see details in Section 3.3); 3) FL systems also require the influence calculation to easily adapt to participants with diverse computation and communication capabilities. Meanwhile, when the model $\hat { \theta }$ is not the minimum or the objective is non-convex, forming a convex quadratic approximation of the loss, $e . g . , { \hat { L } } ( z ; \theta ) =$ $\begin{array} { r } { L ( z ; \theta ) + \bar { \nabla } ^ { \top } L ( z ; \theta ) ( \bar { \theta } - \hat { \theta } ) + \frac { 1 } { 2 } ( \theta - \hat { \theta } ) ^ { \top } ( H _ { k } + \lambda _ { k } I ) ( \theta - \hat { \theta } ) \ : [ 1 3 ] , } \end{array}$ still gives meaningful results; here $\lambda _ { k }$ is a damping term that can be added if $\breve { H _ { k } }$ has negative eigenvalues.

# 3.3 Hierarchical Influence Analysis

Our influence function for FL enables us to measure the influence of all local training samples one by one so as to identify those with unusually large influence as erroneous samples (i.e., negatively influential samples). In a straightforward solution, the server needs to construct and invert $\begin{array} { r } { \frac { 1 } { K } \sum _ { k = 1 } ^ { K } H _ { k } + \lambda I , } \end{array}$ the Hessian matrix of the loss function, which requires $O ( n p ^ { 2 } + p ^ { 3 } )$ operations $( \theta \ \in \ \mathbb { R } ^ { p } )$ . It also requires all clients $C _ { k } , k \in [ K ]$ to upload Hk to the server, compute $\nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } )$ for all samples $z _ { k , i } \in \mathcal { D } _ { k } ,$ , and upload $\nabla _ { \boldsymbol { \theta } } \bar { L } ( z _ { k , i } ; \hat { \boldsymbol { \theta } } )$ to the server, which requires $O ( n p )$ operations and $O ( K p ^ { 2 } + n p )$ communication cost. Considering large n and p in deep neural models, directly computing Eq.(4) for all samples will cause unacceptable computation and communication overhead in large-scale FL systems.

We design our system to significantly reduce the debugging overhead by the following two approaches.

(1) Avoid direct calculation of $\begin{array} { r } { \big ( \frac { \hat { 1 } } { K } \sum _ { k = 1 } ^ { K } H _ { k } + \lambda I ) ^ { - 1 } } \end{array}$ with second-order optimization. We use Hessian-vector ly approximate , and then c $s _ { t e s t } =$ $\begin{array} { r } { \dot { ( } \frac { 1 } { K } \sum _ { k = 1 } ^ { K } H _ { k } ~ + ~ \lambda I ) ^ { - 1 } \nabla _ { \theta } L ( z _ { t e s t } ; \hat { \theta } ) } \end{array}$ $I _ { f } ( z _ { k , i } ) ~ = ~ s _ { t e s t } ^ { \top } \nabla _ { \theta } L ( z _ { k , i } ; \hat { \theta } )$ . Based on HVP, we design a computation-efficient influential sample identification method (see Algorithm 1 in Section 4.2). Further, we propose a communication-saving influential sample identification method (see Algorithm 2 in Section 4.2) based on the Randomized Kaczmarz method (RK) [37].

(2) Avoid unnecessary influence computation with hierarchical analysis. Since the majority of training samples are qualified, requiring all clients to compute and upload influence values of all local samples would incur a big waste of resources. To decrease unnecessary computation while preserving a high identification accuracy, based on the additive property of the influence function for FL, we design a hierarchical influential analysis approach (illustrated in Fig.2), which first identifies negatively influential clients, and only requires them to compute and update influences of their local samples for negatively influential samples identification. For negatively influential clients identification, instead of adding influence values of samples for each client, we propose a simple but effective method to let the server measure the client’s influence using the training log stored in the server. With the training log, the server can compute the differential local model update defined as the distance between the local model and the global model, $\mathrm { e . g . } , \lvert \lvert \theta _ { t } ^ { k } - \theta _ { t } \rvert \rvert$ of client $C _ { k } , k \in [ K ] .$ , at iteration $t , t \in [ T ]$ in the FL procedure. We observe that differential local model updates of clients with erroneous samples are significantly greater than those of clients without any erroneous samples (see details in Section III-C in [23]). Fig.1 presents example differential local model updates for different clients when training two popular CNN models. By identifying the outlier-updates in the training log, we save the influence calculation of a large portion of qualified clients, while resulting in negligible loss of identification accuracy.

# 3.4 Design Overview

Leveraging our influence function for FL and hierarchical analysis approach, we design an efficient and privacypreserving debugging framework FLDebugger (Fig. 2), consisting of two main steps:

(1) Hierarchical influence analysis. Given a global model ˆθ with some test errors, the server first identifies negatively influential clients based on training logs on the server. Then the server coordinates all negatively influential clients to locate their negatively influential samples using influence function for FL and differential privacy mechanism. Specially, to cope with dynamic resource limitations in heterogeneous FL systems, we tailor two privacy-preserving influential sample identification algorithms to save computation resources and communication resources, respectively, and use two algorithms adaptively.

![](images/a546395ca83c7cfa259b40da6ed86401e18f8343d0bb83f5807400c63ee0bb67.jpg)



Fig. 2. System overview of FLDebugger.

(2) Influence-based client selection and model updating. Given the identification results, the server requires negatively influential clients to remove their influential samples and selects clients to participate in model retraining according to their selection probabilities. Specifically, the server decreases the selection probability of negatively influential clients, while increases that of most influential qualified clients to accelerate the model convergence. In this way, FLDebugger produces an updated model $\hat { \theta } ^ { \prime }$ with higher accuracy and faster convergence. If the updated model still does not achieve the expected performance, we can conduct the debugging process again on $\hat { \theta } ^ { \prime }$ .

# 4 IDENTIFICATION OF INFLUENTIAL CLIENTS AND SAMPLES

Here, we present the design of hierarchical influential analysis method. We first show how to efficiently identify influential clients using training logs on the server. Then we give two negatively influential sample identification algorithms (Algorithm 1, 2), best-suited for different resource preferences of clients. In addition, we design one unified method for adaptive use of these two algorithms.

# 4.1 Influential Client Identification

Training log based method: The server can identify negatively influential clients by locating the outlier-updates using the training log $( \{ \theta _ { t } ^ { \check { k } } \| k \ \in \ [ \check { K } ] , t \ \in \ [ T ] \} )$ of ${ \mathrm { F L } } ,$ requiring no involvement of clients (see Section 3.3). Fig. 1 illustrates that during the initial rounds of training, updates of neither qualified clients nor negatively influential clients are stable. Therefore, we only consider the second half of the training log $( t > T / 2 )$ . The server calculates the distance between local updates of a client $C _ { k }$ and the corresponding global updates $\begin{array} { r } { \mathrm { ~  ~ \tilde { ~ } { ~ D ~ } ~ } = \frac { 1 } { N ( k ) } \sum _ { t = T / 2 } ^ { T } \ d s s _ { t } ^ { k } | | \theta _ { t } ^ { k } - \theta _ { t } | | } \end{array}$ . Here, $s _ { t } ^ { \bar { k } }$ equals to 1 when $C _ { k }$ is selected to participate in the tth round of the model training, and zero otherwise; $N ( k )$ is the total number of rounds $C _ { k }$ is selected during the second half of the training. If the distance of $C _ { k }$ is significantly greater than the median distance of all clients, $i . e . , ~ { \frac { D _ { k } } { m e d i a n ( \{ D _ { l } \| l \in [ K ] \} ) } } ~ > ~ \delta _ { T }$ i.e. , median({Dl|l∈[K]}) > δT , it is a negatively influential Dk client. We set $\bar { \delta _ { T } } ~ \stackrel { . } { = } ~ 1 . 5 0$ in our implementation. Since the client identification is conducted by the server alone, imposing no computation and communication burden to clients. As presented in Fig. 6, our training log based method dramatically saves both computation and communication cost by orders of magnitude.

# 4.2 Influential Sample Identification

• Algorithm #1: Differentially private computationefficient influential data sample identification.

We aim to save computation resources with little loss of identification accuracy as well as protecting clients’ training data. We design an influential sample identification method based on stochastic estimation using HVP [35] and differential privacy. With Algorithm 1 in our previous version [23], a client directly transmits the mean value of Hessian matrices (second-order gradients) of $\lceil \xi _ { 1 } n _ { i } \rceil$ randomly selected samples, which may incur privacy risk according to the latest result that the training data can be inferred through gradients of batch data [38]. To protect the privacy of gradients, we can introduce randomness to the estimator $\scriptstyle x _ { j } ,$ , i.e., the result of each iteration in the identification process. Specifically, we mask $x _ { j }$ via a differentially private mechanism with a additive noise calibrated to $x _ { j } \mathrm { ' s }$ sensitivity $\begin{array} { r } { S _ { x } . \ S _ { x } = \operatorname* { m a x } _ { z _ { i , g } , z _ { i , a } ^ { \prime } } | x _ { j } ( z _ { i , g } ) - x _ { j } ( z _ { i , g } ^ { \prime } ) | } \end{array}$ , where $z _ { i , g }$ and $z _ { i , g } ^ { \prime }$ are neighboring inputs, $i \in [ K ] , g \in [ \lceil \xi _ { 1 } n _ { i } \rceil ]$ . For instance, the Gaussian noise mechanism is defined as $\mathcal { M } ( z _ { i , g } ) = x _ { j } ( z _ { i , g } ) + \mathcal { N } ( 0 , \mathcal { S } _ { x } ^ { 2 } \cdot \sigma _ { 1 } ^ { 2 } )$ , where $\mathcal { N } ( 0 , S _ { x } ^ { 2 } \cdot \sigma _ { 1 } ^ { 2 } )$ is the Gaussian distribution with mean 0 and standard deviation $S _ { x } \sigma _ { 1 }$ . Unfortunately, since there is no prior bounds of $x _ { j } ( z _ { i , g } )$ , the noise added would be too large (because the noise is selected according to the worst-case analysis), which would destroy the utility of the influential sample identification. To cope with this issue, we leverage a clip based approach to bound the value of $x _ { j } ,$ , so as to bound the noise and achieve comparable identification performance as the no-noise version in [23]. Algorithm 1 outlines our method for differentially private influential sample identification. In each iteration of calculating the estimator, the randomly selected client $C _ { i }$ firstly computes $x _ { j } ( z _ { i , g } )$ using its local randomly selected data samples (line 6). Secondly, the client $C _ { k }$ clips the $l _ { 2 }$ norm of each $x _ { j } ( z _ { i , g } )$ to scale it down, and adds noise $\mathcal { N } ( 0 , \sigma _ { 1 } ^ { 2 } U _ { 1 } ^ { 2 } I )$ to protect privacy (line 7-8). Then the client $C _ { k }$ calculates the influence value for each sample to locally determine the influential samples (line 9-10).

Algorithm 1 can be proved to preserve differential privacy. Since we clip each $x _ { j } ( z _ { i , g } )$ in $l _ { 2 }$ norm with a clipping threshold $U _ { 1 } , ~ i . e . ,$ replacing $x _ { j } ( z _ { i , g } )$ by $\tilde { x } _ { j } ( z _ { i , g } ) ~ =$ $\begin{array} { r } { { \dot { { x } } } _ { j } ( { \dot { { z } } } _ { i , g } ) / \operatorname* { m a x } \lbrace 1 , \frac { | | { { x } } _ { j } ( { { z } } _ { i , g } ) | | _ { 2 } } { { { U } } _ { 1 } } \rbrace } \end{array}$ , this clipping ensures that $| | \tilde { x } _ { j } ( z _ { i , g } ) | | _ { 2 } \leq U _ { 1 }$ , therefore $x _ { j } ( z _ { i , g } )$ is differentially private. For each round, we set $U _ { 1 }$ to the median of the norms of the estimators $x _ { j } ( z _ { i , g } )$ . Accordingly, the noise is bounded by $U _ { 1 }$ . For the Gaussian noise, if we choose $\sigma _ { 1 }$ to be $\begin{array} { r } { \sqrt { 2 \log \frac { 1 . 2 5 } { \delta _ { 1 } } } / \epsilon _ { 1 . } } \end{array}$ then by standard augment [31], each round is $( \epsilon _ { 1 } , \delta _ { 1 } ) – \mathrm { D P }$

Line 5-6 can be computed in $O ( p )$ time [35] and $\tilde { \mathcal { H } } ^ { - 1 } v$ can be computed in $O ( r _ { 1 } \xi _ { 1 } \bar { n } p )$ time, where $\textstyle { \bar { n } } : = { \frac { 1 } { K } } \sum _ { i = 1 } ^ { K }$ ni is the average training sample number of all clients. Typically, taking $r \xi _ { 1 } \bar { n } = { \cal { O } } ( \bar { n } )$ gives accurate results [36]. Thus, the computation complexity of Algorithm 1 is $O ( n p )$ , while the communication complexity is $O ( r _ { 1 } p )$ . The total computation cost for identifying negatively influential samples of client $C _ { k }$ is only $\bar { O } ( n \bar { p } + \bar { n } _ { k } p )$ , while the strawman method requires $O ( n p ^ { 2 } + p ^ { 3 } )$ operations. The average computation cost is $O ( n p / K )$ for each qualified client and $O ( n \bar { p } / K + n _ { k } p )$ for each negative influential client $C _ { k }$ . The total communication cost is $\bar { O } ( r p )$ parameters, while that of the strawman method is $O ( K p ^ { 2 } )$ parameters. The average communication cost for each client is $O ( r p / K )$ .

Algorithm 1: Differentially Private Computationefficient Influential Data Sample Identification   
Input : $\hat{\theta}$ : global model parameters; $z_{test}$ : a test sample with erroneous prediction by model $\hat{\theta}$ ; $\xi_1$ : sampling ratio; $x_0 := v$ ; $\sigma_1$ : noise scale

Output: Indices of negatively influential data samples

1 The server calculates the derivative $v = \nabla_\theta L(z_{test}; \hat{\theta})$ 2 for each round $j = 1, 2, \ldots r_1$ do

3 The server uniformly selects a client $C_i$ , $i \in [K]$ and sends $x_{j-1}$ , $\hat{\theta}$ to client $C_i$ ;

4 Client $C_i$ randomly selects $[\xi_1 n_i]$ samples from $\mathcal{D}_i$ 5 for each $g \in [\lceil \xi_1 n_i \rceil]$ do

6 Client $C_i$ computes $x_j(z_{i,g}) = v + (I - \nabla_\theta^2 L(z_{i,g}, \hat{\theta})) x_{j-1}(z_{i,g})$ 7 $U_1 = median(\{x_j(z_{i,g})\}_{g \in [\lceil \xi_1 n_i \rceil]})$ 8 $\tilde{x}_j \leftarrow \frac{1}{[\lceil \xi_1 n_i \rceil]} \{\sum_g x_j(z_{i,g}) / \max\{1, \frac{||x_j(z_{i,g})||_2}{U_1}\} + \mathcal{N}(0, \sigma_1^2 U_1^2 I)\} // \text{clip } x_j(z_{i,g})$ , and add noise

9 Client $C_i$ sends $\tilde{x}_j$ to the server

10 The server yields $\tilde{x}_{r_1}$ as the final unbiased estimate of $\mathcal{H}^{-1}v$ , and sends $\tilde{x}_{r_1}$ to the negative client $C_k$ 11 The negative client $C_k$ calculates influence values $I_f(z_{k,i})$ for $z_{k,i} \in \mathcal{D}_k$ , and locally determines negatively influential data samples using Eq.8 in [23]

• Algorithm #2: Differentially private communicationsaving influential data sample identification.

For some scenarios where clients care more about communication overhead, we design an interactive identification algorithm to compute $\mathcal { H } ^ { - 1 } \dot { \mathcal { \tau } }$ v requiring less communication cost. Since calculating $\varkappa ^ { - 1 } v$ is equivalent to solving a linear system $\mathcal { H } x = v ,$ we can view the calculations as the solution to the following optimization problem:

$$
\min _ {x} \left\| \mathcal {H} x - v \right\| ^ {2}. \tag {5}
$$

We solve this problem with one communication-saving interactive method (see Algorithm 2 in [23]) based on Randomized Kaczmarz (RK) [37], [39]. RK successively projects the solution estimate to the hyperplanes from an initial approximation, and update the estimation.

However, the direct transmission of the estimator $h _ { l }$ may incur privacy risk [38]. Similar to Algorithm 1, we leverage a differential privacy mechanism to protect the estimator $h _ { l } ,$ as well as to avoid adding excess noises. Algorithm 2 presents the main idea of our differentially private communication-saving influential sample identification. In each iteration of calculating ${ \tilde { h } } _ { l } ,$ the randomly selected client $C _ { k }$ firstly computes $h _ { l } ( z _ { i , g } )$ using its local randomly selected data samples (line 6). Secondly, client $C _ { k }$

clips the $l _ { 2 }$ norm of each $h _ { l } ( z _ { i , g } )$ to scale it down, and adds noise (line 7-8). Then the client $C _ { k }$ calculates the influence value for each sample to locally determine the influential data samples (line 10-11). Similar to Algorithm 1, Algorithm 2 can be proved to preserve differential privacy. When we choose $\sigma _ { 2 }$ to be the Gaussian noise $\begin{array} { r } { \sqrt { 2 \log \frac { 1 . 2 5 } { \delta _ { 2 } } } / \epsilon _ { 2 } , } \end{array}$ each round is $( \epsilon _ { 2 } , \delta _ { 2 } ) { \tt - D P } .$

The computation complexity of Algorithm 2 is $O ( n p )$ , while the communication complexity is $O ( r _ { 2 } p ) , r _ { 2 } = O ( K )$ . The total computation cost for identifying negatively influential samples of client $C _ { k }$ is $O ( n p + n _ { k } p )$ , while the strawman method requires $O ( n p ^ { 2 } + \bar { p ^ { 3 } } )$ operations. The average computation cost of each qualified client is $O ( n p / K )$ and $O ( n \mathbf { \hat { p } } / K + n _ { k } p )$ for a negatively influential client $C _ { k }$ . The total communication cost is $O ( K p )$ parameters, while that of the strawman method is $O ( K p ^ { 2 } )$ parameters. The average communication cost for each client is $O ( p )$ .

Algorithm 2: Differentially Private Communicationsaving Influential Data Sample Identification   
Input : $\hat{\theta}$ : model parameters; $z_{test}$ : a test point with error prediction by model $\hat{\theta}$ ; $\xi_{2}$ : sampling ratio; $\sigma_{2}$ : noise scale

Output: Indices of negatively influential data samples

1 The server calculates the derivative $v = \nabla_{\theta} L(z_{test}, \hat{\theta})$ 2 for each round $j = 1, 2, \ldots, r_{2}$ do

3 The server randomly selects l from the set $\{1, 2, \cdots, p\}$ ; uniformly selects a client $C_{i}, i \in [K]$ ,
    and sends $l, x_{j-1}, \hat{\theta}$ to client $C_{i}$ ;

4 Client $C_{i}$ randomly selects $[\xi_{2} n_{i}]$ samples from $D_{i}$ ;
5 for each $g \in [\left[\xi_{2} n_{i}\right]]$ do

6 Client $C_{i}$ calculates $h_{l}(z_{i,g})$ using the sample $z_{i,g}$ 7 $U_{2} = median(\{h_{l}(z_{i,g})\}_{g \in [\left[\xi_{2} n_{i}\right]]})$ 8 $\tilde{h}_{l} \leftarrow \frac{1}{\left[\xi_{2} n_{i}\right]} \left\{ \sum_{g} h_{l}(z_{i,g}) / \max\{1, \frac{| |h_{l}(z_{i,g})| | _{2}}{U_{2}}\} + \mathcal{N}(0, \sigma_{2}^{2} U_{2}^{2} I)\} // clip h_{l}(z_{i,g})$ , and add noise

9 Client $C_{i}$ computes $\tilde{x}_{j+1}$ using Eq.10 in [23], and sends $\tilde{x}_{j+1}$ to the server

10 The server yields estimator $\tilde{x}_{r_{2}}$ ; sends $\tilde{x}_{r_{2}}$ to the negative client $C_{k}$ 11 Client $C_{k}$ calculates influence values $I_{f}(z_{k,i})$ for $z_{k,i}$ , and locally determines negatively influential samples using Eq.8 in [23]

Adaptive use of identification algorithms. As FL systems are heterogeneous and dynamic, participants have time-varying capabilities in terms of computation and communication. We design one algorithm that utilizes Algorithm 1 or Algorithm 2 adaptively. Algorithm 3 outlines the adaptive use of Algorithm 1 or Algorithm 2. In each round $j \in [ 1 , r _ { 3 } ]$ of identification, the server first estimates the required computation and communication resources $R _ { 1 } , R _ { 2 }$ for calculating $x _ { j }$ . Then the server randomly selects one client $C _ { k }$ satisfying the resource requirements. The client $C _ { k }$ decides to use Algorithm 1 or Algorithm 2 according to his/her resource consumption preferences, e.g., if his/her computation resource is sufficient to calculate $\scriptstyle x _ { j } ,$ then he/she conducts Algorithm 1, otherwise Algorithm 2. In this way, our design can adapt to systems with various resource constraints and benefit the majority of clients. The computation complexity of Algorithm 3 is ${ \dot { O } } ( n p )$ , while the communication complexity is O(min{r1, r2}p).

Algorithm 3: Adaptive Use of Computation-efficient Identification Algorithm and Communication-saving Identification Algorithm   
Input : $\hat{\theta}$ : model parameters; $z_{test}$ : a test point with error prediction by model $\hat{\theta}$ ; $R_{1}$ , $R_{2}$ : required resources; $R_{l1}$ , $R_{l2}$ : local estimated resources

Output: Indices of negatively influential data samples

1 The server calculates the derivative $v = \nabla_{\theta} L(z_{test}, \hat{\theta})$ 2 for each round $j = 1, 2, \ldots, r_{3}$ do

3 The server randomly selects l from the set
    {1, 2, $\cdots$ , p}; uniformly selects a client $C_{i}, i \in [K]$ ;
    sends l to client $C_{i}$ ;

4 if $R_{l1} < R_{1}$ then

5 Client $C_{i}$ randomly selects $[\xi_{1} n_{i}]$ samples from $D_{i}$ ; computes $\tilde{x}_{j}$ with line 5-8 of Algorithm 1

6 else if $R_{l2} < R_{2}$ then

7 Client $C_{i}$ calculates $\tilde{h}_{l}$ with line 5-9 of Algorithm
    2, and calculates $\tilde{x}_{j}$ using Eq.10 in [23]

8 The server yields estimator $\tilde{x}_{r_{3}}$ ; sends $\tilde{x}_{r_{3}}$ to negative client $C_{k}$ 9 Client $C_{k}$ calculates influence values $I_{f}(z_{k,i})$ for $z_{k,i}$ , and locally determines negatively influential samples using Eq.8 in [23]

# 5 PARTICIPANT SELECTION AND MODEL UPDAT-ING

With the identification results, the server can coordinate clients to update the model, $e . g .$ , retraining, for achieving better performance. Negative clients remove negatively influential training samples from model retraining. With the remaining samples, FL is conducted to produce a new model $\hat { \theta } ^ { \prime } .$ Specially, we propose an influence-based client selection strategy to dynamically select clients to participate in the next iteration of model training according to their influence in the current iteration. Since nearly all negatively influential samples have been removed, a larger influence value of a qualified sample indicates a greater potential contribution to the model. Based on the additive properties of influence function for FL, in an iteration $t ,$ we assign clients with larger influence on the current global model $\theta _ { t }$ higher probabilities to be selected in the next iteration $t + 1$ . As introduced in Section 4.1, we can use the training log to measure clients’ influence efficiently. Therefore, the server retrains the model as follows: K clients have equal initial selection probability $P _ { 1 } ^ { 1 } = P _ { 1 } ^ { 2 } = \cdot \cdot \cdot = P _ { 1 } ^ { K }$ ; in the tth iteration, the server selects m clients (forming a client set $S _ { t } )$ according to their current selection probabilities $\{ P _ { t } ^ { 1 } , \dot { P _ { t } ^ { 2 } } , \cdots , P _ { t } ^ { K } \}$ to get the global model $\theta _ { t }$ and update each client’s selection probabilities to

$$
P _ {t + 1} ^ {k} = \frac {n _ {k} | | \theta_ {t} ^ {k} - \theta_ {t} | |}{\sum_ {C _ {k} \in S _ {t}} n _ {k} | | \theta_ {t} ^ {k} - \theta_ {t} | |} \times \sum_ {C _ {k} \in S _ {t}} P _ {t} ^ {k}. \tag {6}
$$

By involving more positively influential clients into the model retraining, the benefit of our strategy is two-fold: 1) it helps the $\hat { \theta } ^ { \prime }$ achieve higher accuracy; 2) it speeds up the convergence of model training. The details of the retraining process are presented in Algorithm 4. The convergence results are concretely analyzed in Appendix.

Algorithm 4: Federated Training with Influence-based Participant Selection   
Input : K clients $\{C_{1},\ldots,C_{K}\}$ have corresponding datasets $\{D_{1},\ldots,D_{K}\}$ and initial selection probability $\{P_{1}^{1},\ldots,P_{1}^{K}\}$ ; B is the local minibatch size, E is the number of local epochs, $\eta_{l},\eta_{g}$ are the local and global step-sizes, and $\phi$ is the fraction of clients being selected

Output: Global model $\hat{\theta}'$ 1 Server initializes $\theta_{0}$ 2 for each round $t=\{1,2,\cdots,T\}$ do

3 $m\leftarrow\max(\phi\cdot K,1)$ 4 $S_{t}\leftarrow m$ clients selected based on selection probabilities $\{P_{t}^{1},\ldots,P_{t}^{K}\}$ 5    for each client $C_{k}\in S_{t}$ in parallel do

6 $\theta_{t+1}^{k}\leftarrow LocalModelUpdate(k,\theta_{t})$ 7 $\theta_{t+1}\leftarrow\frac{\eta_{g}}{m}\sum_{C_{k}\in S_{t}}\theta_{t+1}^{k} // update global model$ 8    for each client $C_{k}\in S_{t}$ do

9 $P_{t+1}^{k}=\frac{n_{k}||\theta_{t}^{k}-\theta_{t}||}{\sum_{C_{k}\in S_{t}}n_{k}||\theta_{t}^{k}-\theta_{t}||}\times\sum_{C_{k}\in S_{t}}P_{t}^{k} // update selection probability$ 10    Normalize( $[P_{t+1}^{1},P_{t+1}^{2},\ldots,P_{t+1}^{K}]$ )

11 LocalModelUpdate( $k,\theta_{0}^{k}$ ): // run on client k

12 $B\leftarrow$ (split $D_{k}$ into batches of size B)

13 for each local epoch e from 1 to E do

14    for batch $b\in B$ do

15 $\theta_{e}^{k}\leftarrow\theta_{e-1}^{k}-\eta_{l}\nabla F_{k}(\theta_{e-1}^{k};b)$

![](images/bf51e392331361cf7a9240283eda9fcbd53a89b28f3efbe94b4e524771f2b98d.jpg)



Fig. 3. System deployment.

# 6 EVALUATIONS

Here, we first demonstrate the vulnerability of FL models to negatively influential samples. Then, we measure the effectiveness of our influence function for FL to approximate the actual effect of samples. We evaluate our hierarchical influential client and sample identification algorithms. Finally, we show that our participant selection strategy can help the server to obtain an improved global model with higher accuracy and faster convergence speed.

# 6.1 System Deployment

We implemented FLDebugger and deployed it on a real AIoT system with one server and 50 clients, including 20 edge nodes, 20 laptops and 11 desktops, as presented in Fig. 3. We use one desktop worked as the server and let other 10 desktops work as clients. All devices were connected via Wi-Fi. To further investigate the performance of

![](images/9e08db7909b91a45aa0cf43b067dc711b3c9c673b9be5fa4019239aef1bfc93b.jpg)



Fig. 4. Predicted differences in loss of data samples of $\mathcal { D } _ { M } ^ { m }$ using Eq. 4 v.s. actual differences in loss.

![](images/ec240add6671824ad58e5e6a9b67d83319336eeed556c364986cec4591591486.jpg)



Fig. 5. Influence values of data samples of Dm using Algorithm 1.

![](images/9ec4579155b9b41e2bda7a5cfeb92383106dfca36ab96fdbc54346b458879587.jpg)



(a) Computation cost.

![](images/8e7320b6c9185e0c701c1fc044edaf247a96709787c84e4430331b7dafd6098d.jpg)



(b) Communication cost.   
Fig. 6. Cost for identifying negatively influential clients using two variants of the basic method and the training log based method.

FLDebugger in large-scale FL systems, we also deployed it in a simulated environment with up to 1,000 clients, where each client is an independent asynchronous thread.

# 6.2 Experimental Configuration

# 6.2.1 Datasets and Deep leaening models

As presented in in Table I of [23], we used five datasets in two modalities (images and audio), includes two public image datasets MNIST [40], CIFAR10 [41], one public audio dataset ESC10 [42], and two datasets collected by crawling images from two image search engines (BaiduImage and BingImage) in real-world scenarios. The specific description of datasets are illustrated in the previous version [23]. We have implemented the typical federated optimization algorithm FedSGD [1] and five popular deep learning models (see Table 1). In those model training, we randomly select clients with fraction $\phi = 0 . 6$ in every iteration. We run federated learning until a pre-specified test accuracy is reached (98.0% for $\mathcal { D } _ { M } ,$ , 90.5% for $\mathcal { D } _ { C }$ , 90.5% for $\mathcal { D } _ { R } ^ { m }$ , 88.2% for $\mathcal { D } _ { O } ^ { m }$ and 88.75% for $\mathcal { D } _ { E } ) .$ , or a maximum number of iterations has elapsed. Meanwhile, we measure the impacts of mislabeled and noisy samples on those models (see Fig. 5 of [23]).

# 6.3 Influence Function for FL v.s. Leave-some-out Retraining

To investigate the accuracy of using our influence function for FL to approximate the actual effect of removing training samples and leave-some-out retraining, we compare the predicted differences in loss $( I _ { f } )$ and the actual differences in loss $( I _ { f } ^ { * } )$ . We train the FedAVG-MNIST model on the original dataset $\mathcal { D } _ { M }$ in the IID setting. We randomly picked an erroneously-classified test point $z _ { t e s t }$ as the error data. For each $C _ { k }$ with 1,200 training points, we calculated $I _ { f } ( D _ { k } )$ using Algorithm 1 with $\sigma _ { 1 } = \mathrm { { } } \bar { 4 } , \delta _ { 1 } = 1 0 ^ { - 5 }$ and the actual change in test loss $I _ { f } ^ { * } ( { \mathcal { D } } _ { k } )$ after removing $C _ { k }$ and retraining, with the results summarized in Fig. 4. The influence values

![](images/64dfa59ed9d507fecc853b9615a1b3ffbe6d0fda7de6818bb92db1349c14c179.jpg)



(a) Computation cost.

![](images/bb23f3643cbf1246c730494ded8304ff3adc8f0e27a0b17e2acb0164345e8316.jpg)



(b) Communication cost.   
Fig. 7. Computation and communication cost for identifying negatively influential data samples for each client.

calculated using Algorithm 2 are quite similar to that in Fig. 4. We observe that the influence scores estimated by our methods are increasing with larger actual differences in loss. Moreover, the predicted influences and actual changes in loss are correlated, with a 0.60 Pearson’s Correlation Coefficients. For a collection of randomly generated influences, the coefficient is around 0. Therefore, our influence function for FL can be adopted to efficiently estimate the actual effect of training samples.

# 6.4 Identify Negative Clients and Samples

First, we train different models using dirty training datasets according to the settings in Table 1. When the global model training is completed, for each test point $z _ { t e s t }$ of interest $( e . g . \mathrm { ~ }$ , test data that is misclassified), we proceed to identify negatively influential clients/samples that are “responsible” for these bugs. Specifically, we use three indicators to characterize the effectiveness of the debugging methods: 1) accuracy: the ratio of the number of clients/samples that are correctly identified to the total clients/samples; 2) precision: the ratio of the number of identified erroneous clients/samples to the total identified erroneous clients/samples; 3) recall: the ratio of the number of identified erroneous clients/samples to the total truly erroneous clients/samples. In addition, we use two indicators to characterize the efficiency of the debugging methods: 1) communication cost: sizes (MB) of parameters transmitted by local clients and the server; 2) computation cost: time (s) it takes for clients to calculate influence values. In our experiment, we set $\sigma _ { 1 } , \sigma _ { 2 } = 4 , \delta _ { 1 } , \delta _ { 2 } = 1 0 ^ { - 5 }$ , and compute values of $\epsilon _ { 1 } , \epsilon _ { 2 } ,$ , respectively. We achieve $( 1 . 2 1 , 1 0 ^ { - 5 } ) – \mathrm { D P }$ for both Algorithm 1, 2.

TABLE 1 Experiment settings for training different models. $r _ { m } / r _ { n }$ is the ratio of mislabeled/noisy training samples. NI-clients are negatively influential clients having mislabeled/noisy samples. 

<table><tr><td>Model</td><td>Dataset</td><td> $r_m$  or  $r_n$ </td><td>#Clients</td><td>#NI-clients</td></tr><tr><td>FedAVG-MNIST [43]</td><td> $\mathcal{D}_M^m$ </td><td> $r_m = 9\%$ </td><td>50</td><td>15</td></tr><tr><td>FedAVG-MNIST [43]</td><td> $\mathcal{D}_M^n$ </td><td> $r_n = 10\%$ </td><td>50</td><td>15</td></tr><tr><td>FedAVG-CIFAR [41]</td><td> $\mathcal{D}_C^m$ </td><td> $r_m = 9\%$ </td><td>50</td><td>15</td></tr><tr><td>FedAVG-CIFAR [41]</td><td> $\mathcal{D}_C^n$ </td><td> $r_n = 10\%$ </td><td>15</td><td>3</td></tr><tr><td>FedAVG-REAL [41]</td><td> $\mathcal{D}_B^m$ </td><td> $r_m = 9\%$ </td><td>10</td><td>3</td></tr><tr><td>FedAVG-MOTOR [41]</td><td> $\mathcal{D}_O^m$ </td><td> $r_m = 9\%$ </td><td>10</td><td>3</td></tr><tr><td>FedAVG-ESC [44]</td><td> $\mathcal{D}_E^m$ </td><td> $r_m = 9\%$ </td><td>4</td><td>1</td></tr></table>

# 6.4.1 Identifying negatively influential clients

We identify negatively influential clients in all seven settings in Table 1. Two methods are used to identify negatively influential clients: the basic method and the training log based method (see Section 4.1).

![](images/60d222a1670c168340962bb16250e864de058d09a1c40a7f6a439a815667ce96.jpg)



(a) Average difference v.s. sigma.

![](images/4401597a8099d0e5da8d8ce1afcb495dcf43cb116e3f10e85e4900ffd3a61d0c.jpg)



(b) Average difference v.s. $\mathrm { e p - }$ silon.

Fig. 8. Average difference between the estimated influence and the actual effect v.s. different noise levels.   
![](images/45965e5882d0cf451deac25cf7a602f113ed525214458b5b82a06caa9290de92.jpg)



(a) Test accuracy.

![](images/c665f508db1177a600692979806aa5147626cf96cfd7d05ab589fe8c717155c8.jpg)



(b) Time cost.   
Fig. 9. Accuracy of different retrained models and cost for retraining.

Accuracy. There are two variants of the basic method, which respectively adopts Algorithm 1 and Algorithm 2 to compute the influence values of training samples, and get each client’s influence value by adding up influence values of its samples. For both variants, we set the threshold $\delta _ { I } = 1 . 5 0$ , and accuracy, precision and recall for identifying clients who have mislabeled or noisy samples are all 100%. The results also prove the effectiveness of our influence function for FL. For the training log based method, we set the threshold $\delta _ { T } ~ = ~ 1 . 5 0$ , and the identification accuracy, precision and recall are all 100% too.

Efficiency. Fig. 6 gives the cost of two variants of the basic method as well as the training log based method. Our training log based method dramatically saves both computation and communication costs by orders of magnitude. As an example, for model FedAVG-CIFAR trained on DmC , the runtime of the training log method is only 0.1 s, while the runtime of two basic methods are 1118.1 s and 1309.7 s; the training log based method requires no communication since the training log is stored on the server, while the communication cost of two basic methods are 209.3 MB and 89.7 MB.

# 6.4.2 Identifying negatively influential data samples

We identify negatively influential samples for negatively influential clients in settings in Table 1 using Algorithm 1, Algorithm 2 and Algorithm 3.

Accuracy. The influence values of samples calculated using Algorithm 1 are plotted in Fig. 5. For comparison, the influence values calculated using Algorithm 1 of our previous version [23] are plotted in Fig.9 (a). The influence values calculated using Algorithm 2, 3 are quite similar to that in Fig. 5. The results show that most dirty (mislabeled and noisy) samples have obviously greater influence values than clean ones, which are quite similar to that of Algorithm

TABLE 2 Performance of different algorithms for identifying influential data samples on different datasets. 

<table><tr><td>Dataset</td><td>Algorithm</td><td>Accuracy</td><td>Precision</td><td>Recall</td></tr><tr><td rowspan="3"> $\mathcal{D}_{M}^{m}$ </td><td>Algorithm 1</td><td>90.2%</td><td>89.0%</td><td>91.6%</td></tr><tr><td>Algorithm 2</td><td>92.0%</td><td>93.1%</td><td>89.2%</td></tr><tr><td>Algorithm 3</td><td>90.8%</td><td>91.1%</td><td>90.2%</td></tr><tr><td rowspan="3"> $\mathcal{D}_{M}^{n}$ </td><td>Algorithm 1</td><td>92.5%</td><td>91.4%</td><td>90.3%</td></tr><tr><td>Algorithm 2</td><td>90.8%</td><td>89.1%</td><td>91.6%</td></tr><tr><td>Algorithm 3</td><td>91.3%</td><td>90.2%</td><td>90.8%</td></tr><tr><td rowspan="3"> $\mathcal{D}_{C}^{m}$ </td><td>Algorithm 1</td><td>83.8%</td><td>70.7%</td><td>77.3%</td></tr><tr><td>Algorithm 2</td><td>85.4%</td><td>72.5%</td><td>79.6%</td></tr><tr><td>Algorithm 3</td><td>84.2%</td><td>71.6%</td><td>79.0%</td></tr><tr><td rowspan="3"> $\mathcal{D}_{C}^{n}$ </td><td>Algorithm 1</td><td>87.9%</td><td>79.0%</td><td>89.1%</td></tr><tr><td>Algorithm 2</td><td>86.9%</td><td>78.1%</td><td>88.7%</td></tr><tr><td>Algorithm 3</td><td>86.2%</td><td>77.5%</td><td>88.0%</td></tr><tr><td rowspan="3"> $\mathcal{D}_{R}^{m}$ </td><td>Algorithm 1</td><td>83.8%</td><td>71.1%</td><td>81.1%</td></tr><tr><td>Algorithm 2</td><td>83.7%</td><td>70.8%</td><td>80.6%</td></tr><tr><td>Algorithm 3</td><td>84.2%</td><td>70.6%</td><td>82.1%</td></tr><tr><td rowspan="3"> $\mathcal{D}_{O}^{m}$ </td><td>Algorithm 1</td><td>82.6%</td><td>63.8%</td><td>78.6%</td></tr><tr><td>Algorithm 2</td><td>81.2%</td><td>65.7%</td><td>80.2%</td></tr><tr><td>Algorithm 3</td><td>81.7%</td><td>63.9%</td><td>79.0%</td></tr><tr><td rowspan="3"> $\mathcal{D}_{E}^{m}$ </td><td>Algorithm 1</td><td>81.3%</td><td>72.3%</td><td>93.0%</td></tr><tr><td>Algorithm 2</td><td>74.2%</td><td>71.6%</td><td>90.5%</td></tr><tr><td>Algorithm 3</td><td>75.6%</td><td>72.0%</td><td>91.8%</td></tr></table>

1, 2 of [23]. We set the thresholds $\delta _ { S }$ in Eq.8 of [23] equal to 5.0 for the three algorithms. As shown in Table 2, accuracy and recall of are similar, and about 90% on $\mathcal { D } _ { M } ^ { m } , ~ \mathcal { D } _ { M } ^ { n }$ . On $\mathcal { D } _ { C } ^ { m } , \mathcal { D } _ { R } ^ { m }$ and $\mathcal { D } _ { O } ^ { m } ,$ precision is around 70% and 60%, while accuracy and recall remain about 80%. On $\mathcal { D } _ { E } ^ { m }$ , accuracy and precision are around 70%, while recall remains above 90%. In all cases, our proposed differentially private identification algorithms achieve fairly high accuracy, which are comparable to that of Algorithm 1, 2 in [23]. Moreover our algorithms can preserve the privacy of clients.

Differential privacy analysis. One attractive feature of our differentially private identification is the small difference between the estimated influence and the actual one, which is consistent with the theoretical argument that differentially private training generalizes well [45]. To demonstrate this, we first calculate differences between the influence values without DP mechanism (using Algorithm 1 in [23]) and the influence values with DP mechanism (using Algorithm 1) under different noises levels (e.g., different $\sigma _ { 1 } )$ . The results are shown in Fig. 8(a), which shows that as noise increases, the average differences also increase, that is, the approximating error gets larger. Meanwhile, we conducted influential sample identification and found that the identification accuracy still stays above 89.0% when $\sigma _ { 1 }$ varies from 5 to 35. The results show that though larger DP noises increase the approximating errors of influence values, they have low impacts on the identification accuracy, since the influence difference caused by erroneous data is much larger. In addition, we depict the differences for different $( \epsilon _ { 1 } , \delta _ { 1 } )$ privacy values in Fig. 8(b). In this figure, each curve corresponds to the influence differences for a fixed $\delta _ { 1 } ,$ as it varies between $1 0 ^ { - 5 }$ and $1 0 ^ { - 2 }$ . For example, the average difference is 0.02 for $\epsilon _ { 1 } = 0 . 4 0 , \delta _ { 1 } = 1 0 ^ { - 5 }$ . By adjusting the noise distribution, we can balance the approximating accuracy and the privacy protection level.

Efficiency. Fig. 7 gives the average cost for each client using different methods to identify negative samples of $\mathcal { D } _ { M } ^ { m } , ~ \mathcal { D } _ { C } ^ { m } , ~ \mathcal { D } _ { R } ^ { m } , ~ \mathcal { D } _ { O } ^ { m } , ~ \mathcal { D } _ { E } ^ { m }$ . The costs of the leave-someout retraining method are too expensive to be practical, while the costs of Algorithm 1, 2, 3 are orders of magnitude lower, $e . g ,$ less than 0.052%, 0.060%, 0.056% for $\mathcal { D } _ { M } ^ { m }$ . In all five scenarios, Algorithm 1 has a smaller computation cost, which saves 21.3%/8.0%, 15.0%/7.3%, 14.0%/6.8%, 25.4%/12.8%, 13.8%/5.1% computational cost compared with those of Algorithm 2/3; while Algorithm 3 saves 65.7%/8.0%, 60.8%/8.6%, 52.6%/9.2%, 46.2%/8.1%, 32.1%/10.2% communication cost compared with those of Algorithm 1/2, respectively. In all cases, our differentially private identification methods (Algorithm 1, 2) achieve efficient identification, where the computation cost is comparable to that of Algorithm 1, 2 in [23] and the communication cost is the same as that of Algorithm 1, 2 in [23]. Meanwhile, compared with Algorithm 1 and 2, our adaptive identification method (Algorithm 3) achieves comparable computation cost, while saves much communication cost.

![](images/4f3093eccd66168b0f03cc3bb3b068836c305a1f1f286fae1935707622fb80df.jpg)



(a) Accuracy for different mislabeling ratios.

![](images/a730331ef360a5514c2baef4d11dc7cb8c6b4ce73aeee7794fdb48041a387b18.jpg)



(b) Accuracy for different Non-IID scenarios.

![](images/0d3926a8bf34ee4e125d532dc14b11f82533b2abbde16ff9bac78c1752159076.jpg)



(c) Computation time (s).

![](images/023804bbf88fc70f9d709693933c70631922c662be30594346bc70c7b3f34739.jpg)



(d) Communication cost (MB).

Fig. 10. Accuracy and cost for identifying negatively influential samples for a large number of clients.   
![](images/97d65999a1ab7b41da6a7194d9ed8cd769a74a36877b4a16413d1303e8a90f5f.jpg)



(a) Accuracy.

![](images/256ab8225a07c1800875dc5861c20abd22dc7c396655f53819a40b160d5766b0.jpg)



(b) Precision.

![](images/09b42bfbce13925897573dd8a4c6d7609b3758cedbdd52fa2561c755724267f7.jpg)



(c) Recall.

![](images/e0d99584d7d90441be5bc519110af75d11560957620bfcfb35b21ce0c2bd5478.jpg)



(d) F-score.

Fig. 11. Sample identification performance for a large number of clients.   
![](images/82e1ef54d351f9f650f0d384b39aa9df4efbbd0811b870860858d1d722325784.jpg)



(a) Computation cost.

![](images/57030cdd04965e0533c727e6e4434d1c2dc5a0b1f9712acbf99da12efa3d4342.jpg)



(b) Communication cost.   
Fig. 12. Cost for identifying negatively influential clients using our training log based method and the existing Fed-influence [27] method.

# 6.5 Influence-based Participant Selection and Retraining

After identifying negatively influential clients and samples, clients remove negatively influential samples and retrain the four FL models. Here we compare the random participant selection strategy with negatively influential clients and samples (dirty-random) with random participant selection after removing negatively ones (clean-random) and our influence-based participant selection strategy (cleanalgorithm4). Specifically, we use the early stopping strategy to keep track of the prediction accuracy tested on the hold-out test dataset, i.e., we terminate the procedure when the accuracy stops increasing for 10 epochs in a row. Fig. 9 shows that by removing the identified negatively influential samples, all models achieve clearly better test accuracy, which is increased (from 87.8% to 93.65% on $\mathcal { D } _ { M } ^ { m }$ , from 80.7% to 90.3% on $\mathcal { D } _ { C } ^ { m } ,$ , from 90.5% to 94.7% on $\mathcal { D } _ { R } ^ { m } .$ , from 88.2% to 90.7% on $\mathcal { D } _ { O } ^ { m }$ and from 60.2% to 70.1% on $\mathcal { D } _ { E } ^ { m } )$ . Compared with the random participant selection strategy (clean-random), our influence-based participant selection strategy (clean-algorithm4) achieves higher test accuracy as well as faster convergence speed. The retraining time with random participant selection is 172.3s, 7040.5s, 76760.0s, 14800.0s, 8660.0s on five tasks, while 154.6s, 6665.0s, 75951.2s, 13910.0s, 8236.1s for our participant selection. Furthermore, we conduct influential sample identification and model retraining under different mislabeling ratios.

# 6.6 Comparison with Centralized Baselines

We compare our design with state-of-the-art works for both centralized learning and federated learning. For centalized learning, we consider Bootstrap-BMM [8], INCV [26], Fisher-kernel [28] and our Algorithm 1 and 2 applied in centralized scenarios, named Alg1-centralized and Alg2-centralized, to identify mislabeled samples on dataset Dm. Table 3 shows that our identification methods achieve higher F-score than exiting works. For federated learning, we use one client-level model debugging method Fedinfluence [27] and our training log based method to identify negatively influential clients. For both methods, the accuracy, precision and recall for identifying clients who have mislabeled samples are all 100%. Fig. 12 gives the cost of the identification. Our training log based method dramatically saves both computation and communication costs by orders of magnitude. The results show that our methods achieve high identification accuracy with very little overhead, thus significantly outperform existing work.

TABLE 3 Performance for identifying mislabeled samples on dataset DmC $( r _ { m } = 1 0 \% )$ in centralized scenarios. 

<table><tr><td>Methods</td><td>Precision</td><td>Recall</td><td>F-score</td></tr><tr><td>Alg1-centralized</td><td>72.1%</td><td>78.4%</td><td>74.4%</td></tr><tr><td>Alg2-centralized</td><td>74.0%</td><td>80.1%</td><td>77.0%</td></tr><tr><td>Bootstrap-BMM [8]</td><td>47.3%</td><td>92.3%</td><td>62.2%</td></tr><tr><td>INCV [26]</td><td>48.1%</td><td>80.0%</td><td>60.1%</td></tr><tr><td>Fisher-kernel [28]</td><td>60.2%</td><td>78.0%</td><td>67.9%</td></tr></table>

# 6.7 Large-scale Simulation

To further illustrate the scalability of our proposed differentially private identification, we also conduct large-scale simulations for dataset DmM with 100 to 1,000 clients, where each client is an independent asynchronous thread. Fig. 11 shows that as the number of clients increases from 100 to 1,000, the sample identification accuracy gradually declines from 91.8%/91.0% to 72.0%/76.0%, precision declines from 87.0%/89.0% to 56.0%/60.0%, recall declines from 84.4%/86.0% to 65.0%/64.0%, and F-score ( 2·precision·recallprecision+recall ) precision+recall) declines from 85.7%/87.5% to 60.2%/61.9% for Algorithm 1/Algorithm 2. The results are similar to that of Algorithm 1/Algorithm 2 in [23]. The reason is that with less samples for each client, the performance of FL models is decreasing, which makes the erroneous training data not the only primary cause of test errors. Therefore, it is more difficult to distinguish erroneous samples from other influential samples. Fig. 10(c) and Fig. 10(d) give total computation cost and communication cost to identify negative samples of DmM . It show that the computational cost of identification is linear with the number of data samples, so when the number of training samples is fixed, it barely changes, while the communication cost increases linearly with the number of clients. We further evaluate the system performance under scenarios with different mislabeling ratio samples or different data distributions. Fig. 10(a) shows that the identification accuracy of our algorithms remains high (above 82%) as the mislabeling ratio increases to 0.4. We also evaluate our algorithms in different Non-IID scenarios. The results are shown in Fig. 10(b), where the fewer categories of training data possessed by each client, the lower identification accuracy of two algorithms. The reason is that, in severe Non-IID scenarios, unbalanced training data distribution seriously affects the model accuracy, making the influence of mislabeled/noisy samples less obvious.

# 7 CONCLUSIONS

To the best of our knowledge, we propose the first framework to accomplish both debugging and interpretability of FL models from the perspective of training data. A hierarchical design is developed to firstly identify negatively influential clients and then locate negatively influential samples with around 90% accuracy. Three algorithms are provided to adapt to scenarios with different resource constraints. We carefully design these algorithms to preserve privacy of local training data and transmitted parameters. Our influence analysis algorithms can be further tailored to detect malicious clients with poison training data. We also utilize our client influence measurements for selecting clients to participate in the model retraining, which facilitates the model training in terms of higher accuracy and faster convergence. This strategy could also benefit the training of a wide range of FL models.

# ACKNOWLEDGMENT

Lan Zhang and Xiang-Yang Li are the corresponding authors. The research is supported by National Key R&D Program of China 2018YFB0803400, China National Natural Science Foundation with No. 61822209, No.61625205, No. 61932016, No. 62132018, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002. This work was partially supported by Tencent Marketing Solution Rhino-Bird Focused Research Program.

# REFERENCES

[1] B. McMahan, E. Moore, and Ramage, “Communication-efficient learning of deep networks from decentralized data,” in ICML, 2017.   
[2] A. Hard, K. Rao, R. Mathews, and Ramaswamy, “Federated learning for mobile keyboard prediction,” DeepAI, 2018.   
[3] K. Bonawitz, H. Eichner, W. Grieskamp, D. Huba, A. Ingerman, V. Ivanov, C. Kiddon, J. Konecny, S. Mazzocchi, H. B. McMahan et al., “Towards federated learning at scale: System design,” arXiv preprint arXiv:1902.01046, 2019.   
[4] H. B. McMahan, E. Moore, D. Ramage, S. Hampson et al., “Communication-efficient learning of deep networks from decentralized data,” arXiv preprint arXiv:1602.05629, 2016.   
[5] Y. Chen, J. Wang, C. Yu, W. Gao, and X. Qin, “Fedhealth: A federated transfer learning framework for wearable healthcare,” arXiv:1907.09173, 2019.   
[6] M. Abadi, A. Agarwal, P. Barham, E. Brevdo, Z. Chen, C. Citro, G. S. Corrado, A. Davis, J. Dean, M. Devin et al., “Tensorflow: Large-scale machine learning on heterogeneous distributed systems,” arXiv:1603.04467, 2016.   
[7] S. Mehnaz and E. Bertino, “Privacy-preserving real-time anomaly detection using edge computing,” in IEEE ICDE, 2020, pp. 469– 480.   
[8] E. Arazo, D. Ortego, and Albert, “Unsupervised label noise modeling and loss correction,” in ICML, 2019.   
[9] P. Cheng, X. Lian, and Chen, “Prediction-based task assignment in spatial crowdsourcing,” in IEEE ICDE, 2017, pp. 997–1008.   
[10] S. M. Moosavi Dezfooli and A. Fawzi, “Deepfool: A simple and accurate method to fool deep neural networks,” in CVPR, 2016, pp. 2574–2582.   
[11] M. T. Ribeiro and S. Singh, “Why should I trust you?: Explaining the predictions of any classifier,” in ACM SIGKDD, 2016, pp. 1135– 1144.   
[12] J. Li, W. Monroe, and D. Jurafsky, “Understanding neural networks through representation erasure,” arXiv preprint arXiv:1612.08220, 2016.   
[13] P. W. Koh and P. Liang, “Understanding black-box predictions via influence functions,” in ICML, 2017, pp. 1885–1894.   
[14] P. W. W. Koh and Ang, “On the accuracy of influence functions for measuring group effects,” in NIPS, 2019, pp. 5254–5264.   
[15] L. Zhang, T. Jung, K. Liu, and X.-Y. Li, “Pic: Enable large-scale privacy preserving content-based image search on cloud,” IEEE TPDS, vol. 28, no. 11, pp. 3258–3271, 2017.   
[16] Y. Liu and J. Han, “Rumor riding: anonymizing unstructured peerto-peer systems,” IEEE TPDS, vol. 22, no. 3, pp. 464–475, 2010.   
[17] L. Zhang, X.-Y. Li, and K. Liu, “Cloak of invisibility: Privacyfriendly photo capturing and sharing system,” IEEE TMC, vol. 18, no. 11, pp. 2488–2501, 2018.

[18] L. Zhang, X.-Y. Li, K. Liu, T. Jung, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in mobile social networks,” IEEE Transactions on Mobile Computing, vol. 14, no. 9, pp. 1888– 1902, 2014.   
[19] B. Fang and X. Zeng, “NestDNN: Resource-aware multi-tenant ondevice deep learning for continuous mobile vision,” in Mobicom, 2018, pp. 115–127.   
[20] S. Wang and T. Tuor, “When edge meets learning: Adaptive control for resource-constrained distributed machine learning,” in INFOCOM, 2018.   
[21] G. Castellano and Esposito, “A distributed orchestration algorithm for edge computing resources with guarantees,” in INFOCOM, 2019.   
[22] S. Wang, T. Tuor, and Salonidis, “Adaptive federated learning in resource constrained edge computing systems,” in IEEE Journal on Selected Areas in Communications, 2019, pp. 1205–1221.   
[23] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. M. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” in 2021 37th International Conference on Data Engineering (ICDE), 2021.   
[24] A. Datta and S. Sen, “Algorithmic transparency via quantitative input influence: Theory and experiments with learning systems,” in IEEE S&P, 2016, pp. 598–617.   
[25] P. Adler, C. Falk, S. A. Friedler, T. Nix, G. Rybeck, C. Scheidegger, and Smith, “Auditing black-box models for indirect influence,” Knowledge and Information Systems, vol. 54, no. 1, pp. 95–122, 2018.   
[26] P. Chen, B. Liao, and G. Chen, “Understanding and utilizing deep neural networks trained with noisy labels,” in ICML, 2019.   
[27] Y. Xue, C. Niu, Z. Zheng, S. Tang, C. Lv, F. Wu, and G. Chen, “Toward understanding the influence of individual clients in federated learning,” in AAAI, 2021.   
[28] R. Khanna, B. Kim, J. Ghosh, and S. Koyejo, “Interpreting black box predictions using fisher kernels,” in The 22nd International Conference on Artificial Intelligence and Statistics. PMLR, 2019, pp. 3382–3390.   
[29] C. Dwork, F. McSherry, K. Nissim, and A. Smith, “Calibrating noise to sensitivity in private data analysis,” in Theory of cryptography conference. Springer, 2006, pp. 265–284.   
[30] C. Dwork, “A firm foundation for private data analysis,” Commun. ACM, no. 1, p. 8695, 2011.   
[31] C. Dwork, A. Roth et al., “The algorithmic foundations of differential privacy.” Foundations and Trends in Theoretical Computer Science, vol. 9, no. 3-4, pp. 211–407, 2014.   
[32] C. Dwork and Kenthapadi, “Our data, ourselves: Privacy via distributed noise generation,” in EUROCRYPT 2006, ser. Lecture Notes in Computer Science, May 2006.   
[33] M. Abadi, A. Chu, I. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar, and L. Zhang, “Deep learning with differential privacy,” in Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security, 2016, pp. 308–318.   
[34] L. Zhu, Z. Liu, , and S. Han, “Deep leakage from gradients,” in Annual Conference on Neural Information Processing Systems (NeurIPS), 2019.   
[35] B. A. Pearlmutter, “Fast exact multiplication by the hessian,” in Neural computation, 1994, pp. 147–160.   
[36] N. Agarwal, B. Bullins, and E. Hazan, “Second-order stochastic optimization in linear time,” stat, vol. 1050, p. 15, 2016.   
[37] T. Strohmer and R. Vershynin, “A randomized kaczmarz algorithm with exponential convergence,” Journal of Fourier Analysis and Applications, vol. 15, no. 2, pp. 262–278, 2009.   
[38] L. Zhu, Z. Liu, and S. Han, “Deep leakage from gradients,” in Advances in Neural Information Processing Systems, 2019, pp. 14 747– 14 756.   
[39] A. Zouzias and N. M. Freris, “Randomized extended kaczmarz for solving least squares,” SIAM Journal on Matrix Analysis and Applications, vol. 34, no. 2, pp. 773–793, 2013.   
[40] Y. LeCun, “The mnist database,” http://yann.lecun.com/exdb/ mnist/.   
[41] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” Citeseer, Tech. Rep., 2009.   
[42] K. J. Piczak, “Esc: Dataset for environmental sound classification,” in the 23rd ACM MM, 2015, pp. 1015–1018.   
[43] Y. LeCun, L. Bottou, Y. Bengio, P. Haffner et al., “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.   
[44] B. Zhu, C. Wang, and Liu, “Learning environmental sounds with multi-scale convolutional neural network,” in IJCNN. IEEE, 2018, pp. 1–8.

[45] R. Bassily and K. Nissim, “Algorithmic stability for adaptive data analysis,” in Proceedings of the forty-eighth annual ACM symposium on Theory of Computing, 2016, pp. 1046–1059.

![](images/7c8026bbe8ce64c221efc1ff5380b2ffce96df98cd89c2be252efb6bb3052fa6.jpg)



Anran Li is a Ph.D candidate in the Department of Computer Science and Technology, University of Science and Technology of China, China. She received her B.S. degree in Anhui University of Science and Technology in 2016. Her research interests include data quality assessment, federated learning and mobile computing.

![](images/f35b08a2e6ae903748358f8bc1291007de5f0ebc80df6951bd778961362fc40a.jpg)



Lan Zhang is currently a Professor at the School of Computer Science and Technology, at University of Science and Technology of China. She received her Bachelor degree and Ph.D degree from Tsinghua University, China. Her research interests include mobile computing, privacy protection, and data sharing and trading.

![](images/26b191d5cb8a2d8bf64f57edf7f2248ee62f121b67f32d345f1a1796ff40e195.jpg)



Junhao Wang is a Master student in Computer Science at University Of Science And Technology Of China. He received his B.E. degree in Computer Science and Technology from Xian Jiaotong University, China, in 2019. His research interests include robustness and safety in federated learning.

![](images/a086fa7f2d0e3fd3d7bf45d8ec9dcc8c0e3fa7d04eefb264e3d27e05585c2a88.jpg)



Feng Han is a Ph.D. candidate in Computer Science at University of Science and Technology of China. He received his B.E. degree in Information Security from University of Science and Technology of China, in 2017. His research interests include privacy and security issues in data analysis.

![](images/d33e920c28dae7964599eb360b7a489511fddaa3dbbe14aab2aeefcb30010d0c.jpg)



Xiang-Yang Li is currently a Full Professor and the Executive Dean of the School of Computer Science and Technology, University of Science and Technology of China, Hefei, China. He is an IEEE/ACM Fellow. He received the bachelor degree from the Department of Computer Science, the bachelor degree from the Department of Business Management, Tsinghua University, in 1995, and the Ph.D. degree from the University of Illinois at UrbanaChampaign. His research interests include wireless networking/mobile com-

puting/RFID, privacy and security, cyber-physical systems and IoT, social computing, and interdisciplinary research.