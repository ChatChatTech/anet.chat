# InFi: End-to-End Learning to Filter Input for Resource-Efficiency in Mobile-Centric Inference

Mu Yuan, Lan Zhang, Member, IEEE, Fengxiang He, Member, IEEE, Xueting Tong, Miao-Hui Song, Zhengyuan Xu, Senior Member, IEEE, and Xiang-Yang Li, Fellow, IEEE

Abstract—Mobile-centric AI applications have high requirements for the resource-efficiency of model inference. Input filtering is a promising approach to eliminate redundancy so as to reduce the cost of inference. Previous efforts have tailored effective solutions for many applications, but left two essential questions unanswered: (1) theoretical filterability of an inference workload to guide the application of input filtering techniques, thereby avoiding the trial-and-error cost for resource-constrained mobile applications; (2) robust discriminability of feature embedding to allow input filtering to be widely effective for diverse inference tasks and input content. To answer them, we first formulate the input filtering problem and theoretically compare the hypothesis complexity of inference models and input filters to understand the optimization potential. Then we propose the first end-to-end learnable input filtering framework that covers most state-of-the-art methods and surpasses them in feature embedding with robust discriminability. We design and implement InFi that supports different input modalities and mobile-centric deployments. Comprehensive evaluations confirm our theoretical results and show that InFi outperforms strong baselines in applicability, accuracy, and efficiency. InFi can achieve 8.5× throughput and save 95% bandwidth, while keeping over 90% accuracy, for a video analytics application on mobile platforms.

Index Terms—Input Filtering, Model Inference, Mobile Computing, Multimodal Data

# 1 INTRODUCTION

HE increased computing power of mobile devices and T the growing demand for real-time sensor data analytics have created a trend of mobile-centric artificial intelligence (AI) [2], [3], [4], [5]. It is estimated that over 80% of enterprise IoT projects will incorporate AI by 2022. The on-device inference of computer vision models brings us increasingly rich real-time AR applications on mobile devices [6]. A judicious combination of on-device and edge computing can analyze videos taken by drones in real-time [7]. The resource efficiency of model inference is critical for AI applications, especially for resource-limited mobile devices and latencysensitive tasks. However, many AI models with state-of-the-This article is a substantially extended and revised version of Yuan et al. [1], which appeared in the proceedings of the 28th Annual International Conference on Mobile Computing And Networking (ACM MobiCom ’22).

• Lan Zhang is the corresponding author.   
Lan Zhang is with the School of Computer Science and Technology and School of Data Science, University of Science and Technology of China, Hefei, China, and Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, Hefei, China.   
E-mail: zhanglan@ustc.edu.cn   
M. Yuan, Miao-Hui Song and Xiang-Yang Li are with the School of Computer Science and Technology, University of Science and Technology of China, Hefei, China.   
E-mail: ym0813@mail.ustc.edu.cn, songmiaohui@mail.ustc.edu.cn, xiangyangli@ustc.edu.cn   
Xueting Tong is with the Institute of Advanced Technology, University of Science and Technology of China, Hefei, China.   
E-mail: tongxueting@mail.ustc.edu.cn   
Fengxiang He is with JD Explore Academy, JD.com Inc., Beijing, China. E-mail: fengxiang.f.he@gmail.com   
Zhengyuan Xu is with the Key Laboratory of Wireless Optical Communications, Chinese Academy of Sciences, University of Science and Technology of China, Hefei, China.   
E-mail: xuzy@ustc.edu.cn

art accuracy [8], [9], [10] are too computationally intensive to perform high-throughput inference, even when they are offloaded to edge or cloud servers [11].

For resource-efficient inference, one direct and popular way is to eliminate the redundancy of the deep model itself via accelerating and compressing techniques [12], [13], [14], [15], [16], [17], [18]. In this work, we follow another series of approaches [19], [20], [21], [22], [23], [24] that attempt to filter the redundancy in the input data. Fig. 1 shows four examples of input redundancy in mobile-centric AI applications. We call this series of approaches input filtering and classify them into two categories: SKIP and REUSE. (1) SKIP methods [19], [24] aim to filter input data that will bring useless inference results, e.g., images without faces for a face detector (Fig. 1a) and audios without a valid command for a speech recognizer (Fig. 1b). FilterForward [19] trains a binary classifier and sets a threshold on classification confidence to filter input images. (2) REUSE methods [21], [22] attempt to filter input whose results can reuse the previous inference results, e.g., motion signals of the same action (Fig. 1c) and video frames with the same vehicle count (Fig. 1d). FoggyCache [21] maintains a cache of feature embedding and inference results of previous inputs and searches reusable results in the cache for newly arrived data. Input filtering usually works as a necessary prelude to inference for under-resourced mobile systems. Moreover, compared with model optimizations, input filtering provides more flexible trade-offs between accuracy and efficiency, e.g., FilterForward can adjust the threshold in SKIP and FoggyCache can adjust the cache size in REUSE. Although prior efforts have designed effective input filters for a range of applications, two important and challenging questions remain unanswered:

![](images/d0700c593e4c1c8a0acc2db3af8ad9437551096fb19723fe0d1c56029021b3d4.jpg)



![](images/73ead7f365f24042766907afa3a1ac119eb68e6421fc7d3103ac52e7436b7860.jpg)



(a) Face detection on mobile phones.   
(b) Speech recognition offloaded on the cloud.   
![](images/a96d8c2e028a32430ba793ae73e1840b0b36c0ef2342d18ae0ee869ec7c75188.jpg)



![](images/ae6335e6f5728ffabe2b41a90d5f9d0691618cf01ec78f3ba5822643828634c7.jpg)



(c) Human action recognition on smartbands.   
(d) Vehicle counting using drones and edges.   
Fig. 1: Input redundancy in mobile-centric AI applications. Gray squares indicate redundant inference results: (a) no detected face, (b) invalid recognized speech, (c) previous classification result can be reused, (d) latest count result can be reused.

1. Theoretical filterability analysis for the guidance of applying input filtering to mobile-centric inference: Not all inference workloads have the optimization potential by using input filtering. Sometimes, to achieve the required accuracy, a SKIP/REUSE filter is more costly than the original inference. Characterizing the conditions under which the filter has to cost more to be accurate is thus essential to input filtering. Previous efforts study the input filtering problem from an application-oriented perspective. They start from the observation of redundancy and propose bespoke input filtering solutions without further analyzing the relation between their inference workloads and input filters. Without theoretical guidance and explanation, though they delivered accurate and lightweight input filters for specific workloads, the trial-and-error process of designing input filters for other workloads is still very cumbersome and may fail next time, especially for resource-scarce mobile systems.

2. Robust feature discriminability for diverse tasks and modalities in mobile-centric inference: A discriminative feature representation [25] is critical to filtering performance since it directly determines the accuracy of making SKIP decisions and finding REUSABLE results. Recent work [20] shows that for different workloads, the discriminability of low-level features is different, e.g., the area feature works better for counting while the edge feature works better for detection. Most existing filtering methods leverage handcrafted features [20], [21], [22] or pre-trained neural networks as feature embedding [19], and implicitly assume that these features are sufficiently discriminative for the target workloads. However, mobile applications usually have high diversity in input content and inference tasks. The dependency on pre-trained or handcrafted features leads to unguaranteed discriminability to these diversities. Our experiments (§ 6.2) show that, for an action classification workload, neither a SKIP method using the pre-trained feature [19] nor a REUSE method using the handcrafted feature [21] can work effectively. The feature embedding should be obtained in a workload-agnostic and learnable manner, rather than tailored case by case.

To answer these questions, we first provide a generic formulation of the input filtering problem and conditions of valid filters. Then we theoretically define filterability and analyze the filterability of the two most common types of inference workloads (namely, classification and regression) by comparing the hypothesis complexity [26], [27] of the inference model and its input filter. Instead of designing bespoke solutions for narrowly-defined tasks, we propose the first end-to-end learnable framework which unifies both SKIP and REUSE approaches [19], [20], [21]. The end-toend learnability provides feature embedding with robust discriminability in a workload-agnostic manner, thus significantly broadening the applicability. Based on the unified framework, we design an input filtering system, named InFi, which supports both SKIP and REUSE functions. In addition to image, audio, and video inputs, InFi complements existing techniques in supporting text, sensor signal, and feature map inputs. Previous methods are typically designed for a certain deployment, e.g., inference offloading [20], [21]. InFi flexibly supports common deployments in mobile systems, including on-device inference, offloading, and model partitioning [28]. In summary, our main contributions are as follows:

•We formulate the input filtering problem and provide validity conditions of a filter. We present the analysis based on complexity comparisons between hypothesis families of inference workloads and input filters, which can guide and explain the application of input filtering techniques.

•We propose the first end-to-end learnable input filtering framework that unifies SKIP and REUSE methods. Our framework covers most existing methods and surpasses them in feature embedding with robust discriminability, thus supporting more input modalities and inference tasks.

•We design and implement an input filtering system InFi. Comprehensive evaluations on workloads with 8 input modalities, 14 inference tasks, and 3 types of mobile-centric deployments show that InFi has wider applicability and outperforms strong baselines in accuracy and efficiency. For a video analytics application on a mobile platform, InFi can achieve up to 8.5× throughput and save 95% bandwidth compared with the naive vehicle counting workload, while keeping over 90% accuracy.

# 2 INPUT FILTERING

This section formulates the input filtering problem and provides the conditions of a “valid” input filter for resourceefficient mobile-centric inference.

# 2.1 Problem Definition

An input filtering problem needs to determine what input is redundant and should be filtered for a given inference model. First, the definition of an input filtering problem is based on its target inference model. Let X , Y denote the input space and the label space of the target model, respectively. Define $c : \mathcal { X }  \mathcal { Y } ,$ , named the target concept [29], which provides the ground-truth label for each input. Then training a target model is to search for a function h from a hypothesis family [29] H using a set of training samples $S =$ $\{ ( \bar { x } _ { i } , y _ { i } ) \} _ { i = 1 } ^ { m } ,$ where $( x _ { 1 } , . . . , x _ { m } )$ are sampled independently from $\mathcal { X }$ with an identical distribution $\mathbf { \bar { \rho } } _ { \mathrm { ~ } }$ and $y _ { i } ~ = ~ c ( x _ { i } )$ . Using the above notations, we define the learning problem of the target inference model h by $( \mathcal { X } , \mathcal { Y } , c , \mathcal { H } , D , \overset { \triangledown } { S } )$ . Step 0 in Fig. 2 shows the original inference workflow of a trained model $h ,$ which takes input from X and returns an inference result $y \in \mathcal { V }$ .

![](images/11341e11ad0e7017be4278714255673a54feb01b1f0b1c511763c81a9513bc78.jpg)



Fig. 2: Overview of input filtering for inference workload.

Next, given a trained inference model $h ,$ its redundancy measurement function can be defined as:

Definition 2.1 (Redundancy Measurement). A redundancy measurement $f _ { h } : \mathcal { V } \to \mathcal { Z }$ of a model h is a function that takes only the output of h as input and returns a score that indicates whether the inference computation is redundant.

Such measurements are common in practice. For example, based on the output of a face detector the inference computation that returns no detected face is redundant and can be skipped, and we can set the score $z = 0 ;$ Otherwise, $z = 1$ . Formally, $y \mapsto 1 ( | y | > 0 )$ , where y is the output set of detected faces, 1(·) is the indicator function. For REUSE cases, if the inference result of an action classifier on a new query is the same as previously cached, the computation is redundant, and we can define $f _ { h } ( y ) \ : = \ : 1 ( y \notin \ : \dot { Y } _ { c a c h e d } )$ . Note that, this definition of redundancy measurement does not depend on ground-truth labels, since our focus is not the accuracy but to optimize the resource efficiency of a deployment-ready target model with trusted accuracy by eliminating its redundant inference. Step 1 in Fig. 2 shows how redundancy measurement works.

Given the inference workload h and redundancy measurement $f _ { h } ,$ as Step 2 in Fig. 2, learning an input filter is defined as searching for a function g from a hypothesis family $\mathcal { G }$ using a set of training samples $S ^ { \prime } = \{ ( x _ { i } , \stackrel {  } { z _ { i } } ) \} _ { i = 1 } ^ { n } ,$ where $( x _ { 1 } , . . . , x _ { n } )$ are sampled independently with distribution $D ^ { \prime }$ and $z _ { i } ~ = ~ f _ { h } ( \hat { h ( } x _ { i } ) )$ ). This learning problem is denoted by $( \mathcal { X } , \mathcal { Z } , f _ { h } \circ h , \mathcal { G } , D ^ { \prime } , S ^ { \prime } ) ,$ , i.e., g’s target concept is the composite function of $f _ { h }$ and $h .$ .

Inference with an input filter. Once an input filter $g$ is trained, the inference workflow changes from Step 0 to Step 3 in Fig. 2. The input filter g becomes the entrance of the workload, which predicts the redundancy score z of each input x. If not redundant, the inference model h will be directly executed on the input.

# 2.2 Validity Conditions

After defining an input filter, we now give the conditions that a “valid” input filter needs to meet for resource-efficient mobile inference. The input filter is designed to balance the resource and accuracy: filtering more inputs can save more resources, but it also brings a higher risk of incorrect inference results.

Inference accuracy. With an input filter, the inference result y for input x is returned either by executing $h ( x )$ or applying $\hat { h } ( x )$ . Following previous work [19], [20], [21], the correctness of the result $y$ refers to its consistency with the exact inference result by $h ( x )$ , rather than the ground-truth label. An input filter’s inference accuracy Acc is defined as the ratio of correct results obtained by the inference workload with the filter.

Filtering rate. The filtering rate, denoted by $r ,$ is defined as the ratio of filtered inputs (i.e., the ratio of results obtained by applying $\hat { h } ) .$ , which is also an important performance metric considered in previous work [19], [20], [21].

Overall cost. The overhead of an inference workload with an input filter needs to take $^ { g , }$ h and $\hat { h }$ into consideration. Let $C ( \cdot )$ denote the cost of a certain function. For the cost of computation (e.g., runtime), the average cost per input changes from $C ( h )$ into $C ( g ) + ( 1 - r ) C ( h ) + r C ( \hat { h } )$ . The communication cost (e.g., bandwidth) depends on the deployment of the mobile-centric inference workload. Ondevice inference does not involve communication, while the overall bandwidth cost of offloading [19], [20] and model partitioning [28] deployments becomes the original cost multiplied by $( 1 - r ) < 1$ .

Based on the above metrics, we define an input filter as $" v a l i d "$ if it satisfies two conditions: 1) Accurate enough: $A c c > T _ { A c c } ,$ where $T _ { A c c }$ is the threshold of acceptable inference accuracy. 2) Reduced overhead: the overall cost with an input filter is lower. If we aim to reduce the computation cost, we need $( C ( g ) + ( 1 - r ) C ( h ) + r C ( \hat { h } ) ) / C ( \hat { h } ) < 1 _ { }$ i.e., $r ~ > ~ C ( g ) / ( C ( h ) - C ( \hat { h } ) ) ;$ If we aim to reduce the communication cost, we only need $r > 0$ .

# 3 FILTERABILITY ANALYSIS

As mentioned in Sec. 1, not all inference workloads have the optimization potential by using input filtering techniques. Given an inference workload in a mobile-centric AI application, is there a valid input filter? To answer this question, based on our formulation of the input filtering problem, we first define the filterability of an inference workload. Then we analyze filterability in three typical inference cases in SKIP settings and discuss uncovered cases.

# 3.1 Definition of Filterability

Given the learning problem $( \mathcal { X } , \mathcal { Y } , c , \mathcal { H } , D , S )$ of an inference model and the learning problem $( \mathcal { X } , \mathcal { Z } , f _ { h } \circ h , \mathcal { G } , D ^ { \prime } , S ^ { \prime } )$ of its input filter, to simplify the analysis, we make assumptions as follows: $( 1 ) \ { \tilde { D } } = D ^ { \prime } , { \mathrm { i . e . } }$ , the training samples follow the identical distribution; $( 2 ) \ S ^ { \prime } = \{ ( x _ { i } , z _ { i } ) \bar { \} } _ { x _ { i } \in S } , \mathrm { i . e . , }$ the two learning problems share the same inputs in their training samples. But they are supervised under different labels. The inference model h is supervised by $y _ { i } = c ( x _ { i } )$ , while the input filter $g$ is supervised by $z _ { i } = ( f _ { h } \circ h ) ( x _ { i } )$ . Our intuitive idea for filterability is that, if an inference workload is filterable, the learning problem of its input filter should have lower complexity than the learning problem of its inference model. Formally, we define filterability as follows:

Definition 3.1 (Filterability). Let Complex(·) denote the complexity measurement of a hypothesis family. We say that the inference workload is filterable, if $C o m p l e x ( \bar { \mathcal { G } } )$ $\leq C o m p l e x ( \mathcal { H } )$ , where $h \in \mathcal H$ and $( f _ { h } \circ h ) \in \mathcal { G }$ .

Since the hypothesis family cannot be determined based only on input and output spaces, we use the family of the input filter’s target concept $f _ { h } \circ h$ as G .

Now we can characterize the theoretically achievable accuracy and overhead of the input filter for a given inference model by leveraging computational learning theory [26]. It has been proven that the more complex the hypothesis family is, the worse the bounds of generalization error. On the other hand, the hypothesis complexity of neural networks has a positive correlation with the number of parameters. For example, let W, L denote the number of weights and the number of layers in a deep neural network. The VCdimension [30] (a measurement of the hypothesis complexity) is O(W L log(W ) [31]. In the case of the same layer structure, the more parameters the higher the inference overhead of neural networks. The generalization error bound and the number of parameters correspond to the accuracy and efficiency metrics in validity conditions (§ 2.2), respectively, although they are not strict quantification. Therefore, if an inference workload is filterable, whose input filter has lower hypothesis complexity, we are confident to obtain a valid filter with sufficiently high accuracy and lower overhead than the inference model. Next, we will analyze the complexities of the hypothesis family of inference workload h and its input filter g in different cases.

# 3.2 Low-Confidence Classification as Redundancy

Considering an inference workload, where the inference model is a binary classifier h that returns the classification confidence, and the redundancy measurement regards the classification result with a confidence lower than a threshold t as redundant, i.e., $f _ { h } ( y ) \ = \ \mathrm { s i g n } ( y \ > \ t )$ . Confidencebased classification is very common in mobile AI applications, such as speaker verification. We adopt the empirical Rademacher complexity [27], denoted by $\widehat { \Re } _ { S } ( \cdot )$ , as the complexity measurement, which derives the following generalization bounds [26]:

Theorem 1 (Rademacher complexity bounds). Let H be a family of hypothesis taking values in $\{ - 1 , + 1 \}$ . Then for any $\delta > 0$ , with probability at least $1 - \delta ,$ , the following holds for all $h \in \mathcal H$ :

$$
R (h) \leq \widehat {R} (h) + \widehat {\mathfrak {R}} _ {S} \mathcal {H}) + 3 \sqrt {\frac {\log (2 / \delta)}{2 m}}, \tag {1}
$$

where $R ( h )$ and $\widehat { R } ( h )$ denote the empirical and generalization errors, and m is the number of training samples.

This theorem shows that the higher a hypothesis family’s empirical Rademacher complexity, the worse the bounds of its generalization error. The classification confidence-based redundancy measurement creates two hyperplanes parallel to $h = 0 \colon$ : points between them are considered redundant, and points outside them are considered not redundant. Thus, the hypothesis family of the input filter’s target concept has the form: $\mathcal { G } = \{ \mathrm { s i g n } ( h ( x ) ( h ( \bar { x } ) + b ) ) \}$ , where $h \in \mathcal H$ and $b \in \mathbb { R }$ . Then we have proven the following lemma, which shows that the discussed inference workload is not filterable.

Lemma 2. Let H be a family of binary classifiers taking values in $\{ - 1 , + 1 \}$ }. For $\mathcal { G } = \dot { \{ \mathrm { s i g n } ( h ( h + b ) ) \} }$ } where $h \in$ $\mathcal { H } , b \in \mathbb { R } \colon$

$$
\widehat {\mathfrak {R}} _ {S} (\mathcal {G}) \geq \widehat {\mathfrak {R}} _ {S} (\mathcal {H}). \tag {2}
$$

Proof. By definition,

$$
\widehat {\mathfrak {R}} _ {S} (\mathcal {H}) = E _ {\sigma} [ \sup _ {h \in \mathcal {H}} (\frac {1}{m} \sum_ {i = 1} ^ {m} \sigma_ {i} h (x _ {i})) ]
$$

and

$$
\widehat {\mathfrak {R}} _ {S} (\mathcal {G}) = E _ {\sigma} [ \sup _ {h \in \mathcal {H}, b \in \mathbb {R}} (\frac {1}{m} \sum_ {i = 1} ^ {m} \sigma_ {i} \mathrm{sign} (h (x _ {i}) (h (x _ {i}) + b)) ],
$$

where Rademacher variables $\sigma _ { i } \in \{ - 1 , + 1 \}$ . Fixing $b = 2 ,$

$$
\begin{array}{l} \widehat {\mathfrak {R}} _ {S} (\mathcal {G}) \geq E _ {\sigma} [ \sup _ {h \in \mathcal {H}, x _ {i} \in S} (\frac {1}{m} \sum_ {i = 1} ^ {m} \sigma_ {i} \mathrm{sign} (h (x _ {i}) (h (x _ {i}) + 2)) ] \\ = E _ {\sigma} [ \sup _ {h \in \mathcal {H}, x _ {i} \in S} (\frac {1}{m} \sum_ {i = 1} ^ {m} \sigma_ {i} \mathrm{sign} (h (x _ {i})) ] = \widehat {\mathfrak {R}} _ {S} (\mathcal {H}), \\ \end{array}
$$

where we used the fact that sign $( h ( x _ { i } ) + 2 ) \equiv 1$ .

![](images/6df0d175cab35b778464894d409fa48fd91ddb410231cec29ae18bc76ba0b882.jpg)

Multi-class classifiers can be treated as a set of confidence scoring functions, one for each class. The above lemma can also be applied to derive that multi-class classifiers using such a confidence-based redundancy measurement are not filterable either.

# 3.3 Class Subset as Redundancy

Considering the inference model h as a multi-class monolabel classifier and $\mathcal { V } ~ = ~ \{ y _ { 1 } , . . . , y _ { l } \}$ . Then its hypothesis family H has the form: $\mathcal { H } = \{ \operatorname* { m a x } ( h _ { 1 } , . . . , h _ { l } ) : h _ { i } \in \mathcal { H } _ { i } , i \in$ $[ 1 , l ] \}$ , where $h _ { i }$ returns the probability of the i-th class. The redundancy measurement checks whether the predicted class belongs to a specific subset, i.e., $f _ { h } ( y ) = 1 \bar { ( y } \in \mathcal { V } ^ { \prime } )$ , where $y ^ { \prime } \subseteq \mathcal { y }$ . It is common in mobile applications to select only a subset of labels for use. For example, when deploying a pre-trained common object detector [32] on a drone for traffic monitoring, we only care about the labels of vehicles and pedestrians, while considering other labels like animals and trees as redundancy. With the class subset-based redundancy measurement, the hypothesis family of the input filter’s target concept has the form: $\mathcal { G } = \{ \operatorname* { m a x } ( h _ { i } ) : y _ { i } \ \dot { \in } Y ^ { \prime } \}$ . We have proven the following lemma, which shows that the discussed inference workload is filterable:

Lemma 3. Let $\mathcal { H } _ { 1 } , . . . , \mathcal { H } _ { l }$ be l hypothesis sets in $\mathbb { R } ^ { \chi } , l \geq 1$ and let $\mathcal { H } = \{ \operatorname* { m a x } ( h _ { 1 } , . . . , h _ { l } ) : \ : \hat { h } _ { i } \in \mathcal { H } _ { i } , i = 1 , . . . , l \}$ . For $\mathcal { G } = \{ \operatorname* { m a x } ( h _ { i } ) : i \in J \}$ , where $J \subseteq \{ 1 , . . . , l \}$ :

$$
\widehat {\mathfrak {R}} _ {S} (\mathcal {G}) \leq \widehat {\mathfrak {R}} _ {S} (\mathcal {H}). \tag {3}
$$

Proof. For any $j = 1 , . . . , l \colon$

$$
\begin{array}{l} \widehat {\mathfrak {R}} _ {S} (\mathcal {H}) = \frac {1}{m}   E [ \sup _ {\sigma} \sigma_ {i} \max _ {h _ {k} \in \mathcal {H} _ {k}} (h _ {k} (x _ {i})) ] \\ \geq \frac {1}{m} \underset {\sigma} {E} [ \sup _ {x _ {i} \in S} \sigma_ {i} \max _ {j \in J} (h _ {j} (x _ {i})) ] = \widehat {\mathfrak {R}} _ {S} (\mathcal {G}). \\ \end{array}
$$

The equation holds only if the max-value scoring function is in the selected subset for all $x _ { i } \in S _ { }$ , which means that without loss of inference accuracy, the optimal filterable ratio in the data is 0. Except in this extreme case, we can think that the complexity of learning the input filter is strictly lower.

# 3.4 Regression Bound as Redundancy

Considering a bounded regression model $h ,$ whose outputs are bounded by $M \ \in \ \mathbb { R }$ that $| h ( x ) - c ( x ) | \leq M$ (recall that c is the target concept) for all $x \in X$ . The redundancy measurement checks whether the returned value is larger than a threshold, i.e., $f _ { h } ( y ) = 1 ( y > T )$ . As an example, face authentication on mobile devices usually requires the coordinates of the detected face to be within the specified range. Then learning the target concept of the input filter becomes learning a regression model whose outputs are bounded by T , where $T < M$ . We also adopt the empirical Rademacher complexity and have the following theorem [26]:

Theorem 4. Let $p \geq 1$ and $\mathcal { H } = \{ x \mapsto | h ( x ) - c ( x ) | ^ { p } : h \in$ $H \}$ . Assume that $| h ( x ) - c ( x ) | \leq M$ for all $x \in X$ and $h \in H$ . Then the following inequality holds: $\widehat { \mathfrak { R } } _ { S } ^ { \bullet } ( \mathcal { H } ) \leq p M ^ { p - 1 } \widehat { \mathfrak { R } } _ { S } ( H )$ .

Since $M > T ,$ , this theorem shows that the upper bound of ${ \widehat { \Re } } _ { S } ( { \mathcal { G } } )$ is tighter than the upper bound of $\hat { \mathfrak { R } } _ { S } ( \mathcal { H } )$ . So we can be confident that the bounded regression inference workload discussed is filterable.

# 3.5 Discussions

Other inference tasks. Classification and regression are the most common inference tasks, and the three redundancy measurements discussed are widely adopted [19], [33], [34]. However, there are some inference tasks that are challenging to measure the hypothesis complexity, like reinforcement learning [35] and structured learning [36]. Besides, their redundancy measurements are typically ill-defined. We believe that our problem formalization and analysis approach are general, based on which we will analyze the filterability of other tasks in future work.

Characteristics of REUSE. For the REUSE approach, we cannot determine the hypothesis family of the input filter’s target concept. Here we only give one necessary condition: the inference result is discrete or can be discretized. For example, classification and counting models return discrete outputs. But continuous localization coordinates of detection models cannot be reused directly unless reusing detection results with high IoU are regarded as correct, which is equivalent to discretizing the outputs.

# 4 FRAMEWORK

In this section, we first propose a novel input filtering framework that unifies SKIP and REUSE approaches. Then we discuss how existing approaches are covered by our framework and their limitations. Finally, we present the key design, end-to-end learnability, and advantages it brings.

![](images/15e5068b2e43697e57a2120c6d498529275d546c50bd0f723a9fb6dd318148a2.jpg)



Fig. 3: Unified and end-to-end learnable framework for both SKIP and REUSE input filtering.

# 4.1 SKIP as REUSE

We unify SKIP and REUSE approaches based on the idea that:

SKIP equals to REUSE the NONE output $o f h ( \vec { 0 } )$ .

Suppose we have an all-zero input ⃗0 and apparently its inference result can be interpreted as NONE. Then given a new input x, if it is similar to ⃗0 in the feature space, we can REUSE the cached NONE result, i.e., we SKIP the inference computation. The key to reuse is to measure the semantic similarity between the current input and previously cached ones. However, it is difficult to accurately measure semantic similarity directly based on the raw input. As Step 1 in Fig. 3 illustrated, our framework first computes the feature embedding of each raw input. Taking a pair of inputs $x , x ^ { \prime } ,$ then our framework applies a difference function d on their corresponding embeddings $\boldsymbol { e } , \boldsymbol { e } ^ { \prime }$ and feeds the result into a classifier that predicts a single scalar z. Under this framework, for SKIP, we fix $x ^ { \prime }$ as an all-zero input ${ \vec { 0 } } ,$ then the process degenerates to a binary classification task that takes x as input and returns the prediction z. In this way, our framework unifies SKIP and REUSE approaches, with only a difference in interpretation of the value z. For REUSE, we interpret z as the distance between two inputs. For SKIP, we interpret z as the probability that input x is not redundant.

# 4.2 Inference with an Input Filter

For the inference phase, as shown in Step 2 in Fig. 3, SKIP and REUSE filters only differ in the inputs of the difference function d. (1) SKIP: Inference with a SKIP filter is the same as serving a binary classifier. We can set a threshold on the predicted redundancy score z to determine whether to skip. (2) REUSE: Inference with a REUSE filter needs to maintain a key-value table, where a key is a feature embedding and its value is the corresponding inference result. For an arrived input x, the trained feature embedding network returns its embedding e and the distances z between e and cached keys are computed by the difference function d and the trained classifier. Then we can leverage classification algorithms, e.g., KNN, to obtain the reusable cached results.

# 4.3 Sub-Instance Approaches

Here we explain how our framework covers three state-ofthe-art input filtering methods [19], [20], [21] that will be used for comparison in our evaluations.

Sub-instance1: FilterForward (FF) [19] is a SKIP method for image input. FF uses a pre-trained MobileNet’s intermediate output as the feature embedding. Then it trains a “micro-classifier” that consists of convolution blocks to make the binary decision for filtering.

Sub-instance 2: FoggyCache (FC) [21] is a REUSE method for image and audio input. FC uses low-level features (SIFT for image, MFCC for audio) and applies localitysensitive hashing (LSH) for embedding. Then FC uses L2 norm as the difference function and applies KNN to get the reusable inference results from previously cached ones.

Sub-instance 3: Reducto [20] is a variant of the SKIP method for video input. It measures low-level features (pixel, edge, corner, area) differences between successive frames. If they are similar enough, Reducto skips the current frame and returns the latest result. Formally, let x be the current frame and x′ be the previous frame. Reducto defines $d ( e , e ^ { \prime } ) ~ = ~ ( e - e ^ { \prime } ) / e ^ { \prime } .$ , where $\boldsymbol { e } , \boldsymbol { e } ^ { \prime }$ are low-level features of $x , x ^ { \prime } .$ . It uses a threshold function as the classifier, i.e., $1 ( d ( e , e ^ { \prime } ) > T )$ .

# 4.4 End-to-end Learnability

To obtain features with robust discriminability for diverse data modalities and inference tasks in mobile applications, a key design principle of our framework is end-to-end learnability. End-to-end learning system casts complex processing components into coherent connections in deep neural networks [37] and optimizes itself by applying gradientbased back-propagation algorithms all through the networks. Deep end-to-end models have shown state-of-the-art performance on various tasks including autonomous driving [38] and speech recognition [39]. As aforementioned, a main component of our unified framework is to measure the semantic similarity between two inputs. To make our framework end-to-end learnable, we leverage the metric learning paradigm, whose goal is to learn a task-specific distance function on two objects. The metric learning paradigm turns the fixed difference function d (e.g., Euclidean distance and L2 norm) used by existing methods into an end-to-end learnable network. Within the metric learning paradigm, we adopt Siamese network structure [40] for feature embedding to support two inputs and flexible input modalities. The Siamese network uses the same weights while working on two different inputs to compute comparable output vectors, and has been successfully applied in face verification [41], pedestrian tracking [42], etc. We can flexibly implement the Siamese feature embedding by incorporating different neural network blocks to learn modality-specific features in an end-to-end manner, instead of tailoring handcrafted or pre-trained feature modules. Our experimental results show that the end-to-end learned features have robust discriminability to diverse inference workloads in mobile-centric AI applications.

# 5 DESIGN OF INFI

Based on our input filtering framework, in this section, we present the concrete design of InFi (INput FIlter), which supports both SKIP and REUSE functions, named InFi-Skip and InFi-Reuse. The design of InFi has four key components: feature embedding, classifier, training mechanism, and inference algorithm. We also discuss diverse deployments of InFi in AI applications on mobile, edge, and cloud devices.

# 5.1 Feature Networks for Diverse Input Modalities in Mobile-Centric AI

InFi supports filtering inference workloads with six typical input modalities in mobile applications: text, image, video, audio, sensor signal, and feature map. We develop a collection of modality-specific feature networks as building blocks for learning feature embedding. Our major consideration in designing these feature networks is resource efficiency on mobile devices.

Text modality $( g _ { t e x t } )$ . Text is tokenized into a sequence of integers, where each integer refers to the index of a token. We adopt the word-embedding layer to map the sequence to a fixed-length vector by a transformation matrix and use a densely connected layer with a Sigmoid activation to learn the text features.

Image modality $( g _ { i m a g e } ) _ { \cdot }$ . We use depth-wise separable convolution [43], denoted by SepConv, to learn visual features. SepConv is a parameter-efficient and computationefficient variant of the traditional convolution which performs a depth-wise spatial convolution on each feature channel separately and a point-wise convolution mixing all output channels. Then we build residual convolution blocks [44] ConvRes as follows:

$$
\operatorname{ConvStep} (x) = L N (\operatorname{SepConv} (\operatorname{ReLU} (x))),
$$

$$
c _ {1} (x) = \text { ConvStep } (x), c _ {2} (x) = \text { ConvStep } (c _ {1} (x)),
$$

$$
\operatorname{ConvRes} (x) = \operatorname{MaxPool2D} \left(c _ {2} (x)\right) + \operatorname{ConvStep} (x),
$$

where ReLU denotes the rectified linear unit, $L N$ denotes the layer normalization and M axP ool2D denotes the 2D max-pooling layer. Finally, we build the image feature network with two residual blocks followed by a global maxpooling layer and a Sigmoid-activated dense layer.

Video modality $( g _ { v i d e o } ) .$ For video modality, we need to represent not only the spatial but also the temporal features. Given a window of frames, we stack one residual block for each frame and then concatenate their resulting feature maps. Except for the first residual block, the video feature network performs the same operation as the image feature network.

Audio modality $( g _ { a u d i o } )$ . We consider audio inputs in the form of either a 1D waveform or a 2D spectrogram and use the same structure as image feature networks to learn features from audio.

Sensor signal and feature map modality $( g _ { v e c } )$ . Motion sensors are widely used in mobile devices and play a key role in many smart applications, e.g., gyroscope for augmented reality [45] and accelerator for activity analysis [46]. Feature maps refer to the intermediate outputs of deep models and need to be transmitted in workloads that involve model partitioning [28]. We consider these two types of input as a vector with a fixed shape and use two densely connected layers to learn the feature embedding from the flattened vector.

Flexible support for input modalities. Our design provides flexible support for diverse input modalities in mobile-centric AI applications. We can easily integrate a modality-specific neural network from advanced machine learning research as the feature network block into our framework, so as to learn feature embeddings in an endto-end way.

![](images/b7ce17cc5219c474ef333655b53c544f9ec5175ea2ca273ab5fb10ee8a3a96ca.jpg)



Fig. 4: Extend input filtering to multi-modal and multi-task workloads. $x ^ { 1 } , x ^ { \dot { 2 } } , x ^ { 3 }$ represents three input modalities.

# 5.2 Task-Agnostic Classifier

Each feature network $g _ { m o d a l i t y } ,$ where modality belongs to {text, image, video, audio, vec}, takes x as input and outputs the embedding emb. We add a dropout layer after the last dense layer of feature networks to reduce overfitting. Following the previous design of Siamese network [40], we use the absolute difference as the function d. Let emb1, emb2 denote the embedding outputs of two inputs $x _ { 1 } , x _ { 2 }$ . The classifier is defined as $\begin{array} { r } { g _ { c l s } = \sigma ( \sum _ { j } w _ { j } | e m b _ { 1 } ^ { ( j ) } - e m b _ { 2 } ^ { ( j ) } | + b ) } \end{array}$ where $e m b ^ { ( j ) }$ denotes the j-th element in the embedding vector and σ is the Sigmoid function. To sum up, the input filter function $g : \ x \ \to \ z$ can be defined as $g ( x ) = ( g _ { c l s } \circ g _ { m o d a l i t y } ) ( x )$ . With proper implementation, the modality of input data can be automatically detected without manually setting.

# 5.3 Multi-Task Extension

The above design is described for single-task workloads, however, it is common to concurrently run multiple AI models in real applications. We will show that the design of InFi can be flexibly extended to multi-modal and multitask inference workloads.

Multi-modality single-task. Multi-modal learning aims to learn AI models given multiple inputs with different modalities, which is receiving increasing attention in areas such as autonomous driving [47]. Our designs of modalityspecific feature networks and task-agnostic classifier naturally support multi-modal extension: For each modality mod ∈ {text, image, video, audio, vec}, we build the corresponding feature network $g _ { m o d }$ to learn its embedding. Then we concatenate the resulting embeddings and feed it to the classifier $g _ { c l s }$ .

Single-modality multi-task. It is common to deploy multiple AI models to analyze the same input, e.g., detecting vehicles and classifying traffic conditions on the same video stream. For input filtering, we simply extend the length of the last dense layer in the classifier $_ { g _ { c l s } , }$ , one dimension per task. Existing work on multi-task learning [48] demonstrates that the cross-task representation improves learning performance. Formally, given t tasks, it has been proven that the sample complexity needed [49] is as follows:

$$
\text { Complex } (g _ {\text { mod }}) + t \cdot \text { Complex } (g _ {\text { cls }}). \tag {4}
$$

That is, we can save $( t - 1 ) { \cdot } C o m p l e x ( g _ { m o d } )$ sample complexity, compared with learning a filter for each task separately. And our experimental results (Fig. 14) also show that the cross-task representation is beneficial for input filtering.

Multi-modality multi-task. Considering a general case where we need to filter inputs for multi-modality and multitask workloads, we can combine the above two extensions, as shown in Fig. 4: For each input modality, we build the corresponding feature network and concatenate the resulting embeddings; And for each task, we build a multidimension classifier, one dimension per task, which takes the concatenated embedding as input. Compared with the naive way that deploys independent InFi for different inference workloads, our proposed extension saves computation and leverages potential advantages of cross-task and crossmodality representation.

# 5.4 End-to-End Training

InFi-Skip and InFi-Reuse share the same model architecture, but have different formats of training data. 1) Learning an InFi-Skip filter uses the same paradigm as training a binary classifier. Thus its training samples are $( x _ { i } , f _ { h } ( \breve { h } ( x _ { i } ) ) ) _ { i = 1 } ^ { n }$ and we use the binary cross-entropy loss function. In practice, we can use the original training set of h or data collected during serving h. Since $f _ { h }$ only depends on the inference result, the supervision labels can be collected automatically. 2) InFi-Reuse filters are trained using the contrastive loss [50] with a margin parameter of one. Given a set of input and their discrete inference results, the redundancy measurement is defined as the distance metric between a pair of inputs. Formally, a training sample consists of a pair of inputs and their distance label $( x _ { i } , x _ { j } , 1 ( y _ { i } \neq y _ { j } ) )$ . We can optimize all trainable parameters end-to-end, using standard back-propagation algorithms.

Online active update. Unlike benchmark datasets, the distribution of real-world inputs, e.g., the video streams captured by surveillance cameras, is much narrower and changes online [51]. In a video-based vehicle counting application (see Sec. 6.1 for detailed setup), we explored the shifted distribution of frames over wall-clock time. As shown in Fig. $5 \mathsf { a } ,$ the vehicle count varies with time. There are two distinct count peaks in the morning and evening and the nighttime results remain stable at low values. We noticed that the captured frames switched between infrared (IR) and RGB images when the lighting condition changed. The RGB-IR technology provides day and night vision capability for cameras and is supported by popular commercial sensors. We split all frames into infrared and RGB subsets and plot their distribution over the number of detected vehicles in Fig. 5b. We can see a clear difference in the distribution. Therefore, a vanilla offline training policy that selects initial samples (e.g., frames in the first hour) for training the input filter results in sub-optimal performance quickly. To overcome the poor adaptability of offline training, we adopt the least confidence [52] strategy to actively select samples for updates on the fly. Existing work [53] proved that the sample complexity of active learning is asymptotically smaller than passive learning. Specifically, we set a period length and a sampling ratio β%. Then we execute the input filter on all inputs within a period and select β% samples with the least confidence $( | \bar { g ( x ) } - 0 . 5 | )$ ). For InFi-Reuse, we treat 1 − θ as the confidence score. Our experimental results (Fig. 15) show that, given the same budget for the number of training samples, this active strategy significantly outperforms the offline one.

![](images/bb4724437d5a60acaf7d00c910f822873c4a7e899bf59874ea8d1e675c903082.jpg)



(a) One-day trace of vehicle count.

![](images/73c5cbd781b327c7762a69d772746ee3a1ef07ebee024c18b7b3b2c4134c1479.jpg)



(b) CDF of vehicle count on infrared and RGB frames.

Fig. 5: Distribution shifts in online video streams. (b) The means of the distributions are given inside parentheses.   
Algorithm 1: Inference with an InFi Filter   
input: input source src, redundancy threshold T, cache size s, KNN parameter K, homogeneity threshold $\theta_{T}$ 1 def InFiSkip(src):
2    while $x \leftarrow \text{read}(src)$ do
3    if $g(x) > T$ then
4 $y \leftarrow \text{inference}(x)$ ;
5    else
6 $y \leftarrow \text{None}$ ;
7    end
8    end
9 def InFiReuse(src):
10    Initialize empty cache;
11    while $x \leftarrow \text{read}(src)$ do
12    if Len(cache) < s then
13 $y \leftarrow \text{inference}(x)$ ;
14 $cache[g_{modality}(x)] \leftarrow y$ ;
15    else
16 $y, \theta \leftarrow HKNN(cache, g_{modality}(x), g_{cls}, K)$ ;
17    if $\theta < \theta_{T}$ then
18 $y \leftarrow \text{inference}(x)$ ;
19    replace (cache, $\{g_{modality}(x) : y\}$ );
20    end
21    end
22    end

# 5.5 Inference Phase

After training an InFi filter, we integrate it into the original inference workload using Algorithm. 1.

InFi-Skip. We set a redundancy threshold for InFi-Skip to determine whether to skip the current input. And if we skip the input, InFi-Skip will return a NONE result, whose interpretation depends on the redundancy measurement in specific applications. For example, NONE means no face detected in face detection, zero vehicles in vehicle counting application, meaningless speech in speech recognition, etc.

InFi-Reuse. To reuse previous inference results, we need to maintain a cache whose entry is a key-value pair of an input embedding and its inference results. Following the previous RESUE approach [21], we adopt K-Nearest Neighbors (KNN) algorithm to reuse cached results. But it is possible that a new input is not similar to any cached entries, i.e., a cache miss. We adopt the Homogenized KNN (H-KNN) [21] algorithm to handle this problem, which calculates a homogeneity score θ of the found K nearest neighbors and sets a threshold $\theta _ { T }$ on the homogeneity score to detect the cache miss. Then we can replace entries using policies like least frequently used (LFU), denoted by replace in Algorithm 1. Different from the original KNN that typically uses Euclidean distance, which is non-parametric, we set the distance measurement as the trained $g _ { c l s }$ . We denote HKNN(cache, emb, $g _ { c l s } , K )$ as the H-KNN function which returns the majority inference result y of K nearest neighbors of emb in cache.keys using the $g _ { c l s }$ to calculate the distance between embeddings, and computes θ. We focus on taking the advantage of end-to-end learnability, and other subtle optimization opportunities such as cache warm-up are out of the scope of this work.

# 5.6 Mobile-Centric Deployments

Unlike existing work tailored for specific deployment, e.g., inference offloading [19], [20], [21], InFi supports diverse mobile-centric deployments: (1) On-device: both inference model and input filter are deployed on one device; (2) Offloading: the input filter is deployed on one device, and the inference model is deployed on another device. (3) Model Partitioning (MP) [28]: the inference model is partitioned across two devices, and the input filter is deployed with the first part. MP is a promising approach to collaboratively make use of the computing resources of mobile and edge devices [54], [55] and better protect the privacy of mobile data [56]. For MP deployment, the filter’s input is the feature map, so existing filtering approaches [19], [20], [21] cannot be applied. Due to the support of feature map modality, InFi is the first input filter that can be applied in model partitioning workloads. Note that InFi is not limited to systems with a single mobile and edge node. For example, training one filter per server, or changing one filter’s binary classifier into a multi-category one (one bit per server), InFi-Skip can be used in the multi-tenancy context [19].

# 6 EVALUATION

# 6.1 Implementation and Configurations

We implemented InFi 1 in Python. We build all feature networks and classifiers with TensorFlow 2.4. The learning rate is set as 0.001, the batch size is 32, and the number of training epochs is 20. In the text feature network, the output dimension of the embedding layer is 32. For image, video, and audio feature networks, we use 32 and 64 convolution kernels in the two residual blocks. We use 128 units in the first dense layer in vector feature networks. The last dense layer of all feature networks has 200 units and 0.5 dropout probability.

TABLE 1: Datasets and Inference Workloads 

<table><tr><td>Dataset</td><td>Modality</td><td>Inference Task</td></tr><tr><td rowspan="4">Hollywood2</td><td>Video Clip</td><td>Action Classification (AC)</td></tr><tr><td>Image</td><td>Face Detection (FD)Pose Estimation (PE)Gender Classification (GC)</td></tr><tr><td>Audio</td><td>Speech Recognition (SR)</td></tr><tr><td>Text</td><td>Named Entity Recognition (NER)Sentiment Classification (SC)</td></tr><tr><td>ESC-10</td><td>Audio</td><td>Anomaly Detection (AD)</td></tr><tr><td>UCI HAR</td><td>Motion Signal</td><td>Activity Recognition (HAR)</td></tr><tr><td>MoCap</td><td>Motion Signal</td><td>User Identification (UI)</td></tr><tr><td>DeepSig</td><td>Radio Signal</td><td>Modulation Recognition (MR)</td></tr><tr><td>WiFiHAR</td><td>WiFi CSI</td><td>Activity Recognition (WAR)</td></tr><tr><td rowspan="2">City Traffic</td><td>Video Stream</td><td>Vehicle Counting (VC)</td></tr><tr><td>Feature Map</td><td>Vehicle Counting (VC-MP)</td></tr></table>

Datasets and inference models. To evaluate InFi’s wide applicability, we choose 14 inference workloads that cover 8 input modalities and three deployments (see Tab. 1). Seven datasets are used: (1) We reprocessed a standard video dataset, Hollywood2 [57], to create four different input modalities: video clip, image, audio, and text. An action classification model [58] is deployed on the original video clips. Images are sampled from the video clips and a face detection [59], a pose estimation [60], and a gender classification [59] models are deployed. Audio is extracted from each video clip and we deploy a speech recognition model [39]. Text is the caption generated on sampled images by an image captioning model [61]. A named entity recognition model (spaCy [62]) and a sentiment classification model [63] are deployed. (2) We use the ESC-10 dataset [64] for audio anomaly detection and deploy an transformer-based model [65]. (3) We use the UCI HAR dataset [46] for motion signal-based human activity recognition and deploy an LSTM-based model. (4) We use the MoCap dataset [66] for training a motion signal-based user identification (12 users) model, using an LSTM-based architecture, and deploying it as the inference workload. (5) We use the DeepSig dataset [67] and deploy a ResNetbased model for modulation recognition of radio signals. (6) We use the WiFiHAR dataset [68] for activity recognition and deploy an LSTM-based model. (7) We collected a video dataset, named City Traffic, from a real city-scale video analytics platform. We collected 48 hours of videos (1FPS) from 10 cameras at road intersections and deploy YOLOv3 re-implemented with TensorFlow 2.0 to count the number of vehicles in video frames. All deployed inference models load publicly released pre-trained weights. And we split each dataset for training and testing by 1:1 (Hollywood2 and UCI HAR are split randomly, while City Traffic is split by time on each camera).

Devices and deployments. We use an edge server with one NVIDIA 2080Ti GPU and three mobile platforms: (1) NVIDIA JETSON TX2, (2) XIAOMI Mi 5, and (3) HUAWEI WATCH. All device-independent metrics are tested on the edge. For vehicle counting, we test three deployments: on-

TABLE 2: Filtering rate (%) @ 90% inference accuracy of SKIP methods. 

<table><tr><td>Method</td><td>FD</td><td>PE</td><td>GC</td><td>AC</td><td>VC</td><td>AD</td><td>WAR</td></tr><tr><td>FF</td><td>0</td><td>14.5</td><td>0.0</td><td>0.0</td><td>48.0</td><td>/</td><td>/</td></tr><tr><td>Reducto</td><td>/</td><td>/</td><td>/</td><td>/</td><td>48.6</td><td>/</td><td>/</td></tr><tr><td>InFi-Skip</td><td>36.1</td><td>18.9</td><td>33.1</td><td>56.0</td><td>66.5</td><td>75.4</td><td>11.6</td></tr><tr><td>Optimal</td><td>64.8</td><td>34.4</td><td>71.8</td><td>91.2</td><td>77.7</td><td>86.8</td><td>31.1</td></tr><tr><td>Method</td><td>SR</td><td>NER</td><td>HAR</td><td>UI</td><td>SC</td><td>VC-MP</td><td>MR</td></tr><tr><td>InFi-Skip</td><td>44.1</td><td>26.8</td><td>91.2</td><td>72.4</td><td>22.5</td><td>70.7</td><td>40.9</td></tr><tr><td>Optimal</td><td>59.9</td><td>34.4</td><td>91.8</td><td>79.8</td><td>63.8</td><td>77.7</td><td>59.9</td></tr></table>

TABLE 3: Filtering rate @ 90% inference accuracy of REUSE methods.

<table><tr><td>Method</td><td>GC</td><td>AC</td><td>HAR</td><td>SC</td><td>VC-MP</td><td>VC</td></tr><tr><td>FC</td><td>66.1%</td><td>13.2%</td><td>/</td><td>/</td><td>/</td><td>59.4%</td></tr><tr><td>InFi-Reuse</td><td>98.8%</td><td>32.1%</td><td>98.3%</td><td>43.4%</td><td>95.0%</td><td>91.1%</td></tr></table>

device, offloading, and model partitioning (see Sec. 5.6).

Baselines. We adopt three strong baselines: FilterForward (FF) [19], Reducto [20], and FoggyCache (FC) [21]. See Sec. 4.3 for details of baselines. For workloads with no existing method presented (to our best knowledge), we tested a method dubbed Low-level that first computes lowlevel embedding for inputs (MFCC for audio, Bag-of-Words for text, raw data for motion signal and feature map). Then Low-level uses K-nearest neighbors vote (K=10) for both SKIP and REUSE cases. We also deployed YOLOv3- tiny [12] model for vehicle counting and a lightweight pose estimation model [13] to compare input filtering and model compression techniques.

# 6.2 Inference Accuracy vs. Filtering Rate

First, we test two device-independent metrics (inference accuracy and filtering rate) on the ten inference workloads. We adjust the confidence threshold in FF, Reducto, and InFi-Skip, and the ratio of cached inputs in FC and InFi-Reuse, from 0 to 1 with 0.01 interval.

Redundancy measurements. (1) SKIP: For FD (PE), outputs with no detected face (person keypoints) are redundant. For GC (SC), outputs with classification confidence less than a threshold, CONF (0.9), are redundant. For AC, outputs that are not in a subset of classes, Sub, are redundant. For SR, outputs with the number of recognized words less than a threshold, N, are redundant. For NER, outputs without entity label “PERSON” are redundant. For HAR, outputs that are not “LAYING” are redundant. For UI, outputs that do not belong to the first 6 users are redundant. For AD, outputs that are not in {“Cry, Sneeze, Firing”} (anomaly events) are redundant. For MR, we randomly select half of the radio modulation types as redundant. For WAR, outputs with “NO PERSON” are redundant. For VC and VC-MP, outputs with zero count are redundant. (2) REUSE: Experimental results show that cache miss happens rarely, so the homogeneity threshold is set as 0.5. We regard inputs that hit the cache as redundant. For the VC (-MP), since we have 86K images from each camera, a fixed cache ratio can lead to serious inefficiency in the KNN algorithm. We fix the cache size as 1000 and reinitialize the cache every

![](images/bd2c5249c699cf4858ac8b3142726da91bee791a676ba241786c96e75b7cfcf6.jpg)



(a) Pose Estimation

![](images/9db30398020490ed7a8bd5ccb8fc941289197c8cbae5a92b2d0483bb66559eba.jpg)



(b) Face Detection   
Fig. 6: Comparison between FF and InFi-Skip filters on visual detection workloads.

![](images/e478dbd2e78d6ef51a99c59553226f3904083270f26a2aa48440fc60cee3b3e2.jpg)



(a) AC (2 Classes)

![](images/f1042a9fa820dd7faca4e1320f99c33f8b815dbfc952a24c1577bf94c9fe4171.jpg)



(b) AC (8 Classes)   
Fig. 8: InFi-Skip filters on action classification workloads with 2/8 selected classes in the subset.

![](images/6423187a470478d5a79f0d5826c1430c907e01d064ad5ca682bcbe5861773a64.jpg)



(a) SR (N=0)

![](images/935467878b2db67408e016574de490bdb7f0915e71751b36363316577dbdfdd6.jpg)



(b) SR (N=2)   
Fig. 7: InFi-Skip filters on speech recognition workloads. N is the minimal number of recognized words.

![](images/dea4eb36283139bf791abe07685c296bc6324bf733ef461d9de7f23e26b1ff9b.jpg)



(a) HAR (L=LAYING)

![](images/bd2b50fce67feefc7fe899f429e58bae885bee156946c6845dfc0e3900b1d1b9.jpg)



(b) HAR Reuse   
Fig. 9: InFi filters on HAR inference workloads. R denotes the ratio of training samples used. The “Random” case labels each input randomly.

5000 frames. For other inference workloads, we set a fixed cache size according to the cache ratio.

Overview of results. Tab. 2 and Tab. 3 summarize the results of the SKIP and REUSE methods. Following related work [20], we report the filtering rates at 90% inference accuracy. The optimal results are computed by (1-0.9)+rN where rN denotes the ratio of redundant inputs in the test dataset. Results show that InFi-Skip outperforms FF and Reducto on all 10 workloads with significantly higher filtering rates and wider applicability. Similarly, InFi-Reuse significantly outperforms FC on all 6 applicable workloads. InFi-Skip can filters 18.9%-91.2% inputs and InFi-Reuse can filters 32.1%-98.8% inputs, while keeping more than 90% inference accuracy. For all workloads, Low-level method cannot achieve 90% inference accuracy unless no input is filtered (i.e. 0.0% filtering rate), and we omit these results in the tables.

Feature discriminability. By comparing FF and InFi on FD, PE, GC, and AC workloads, we evaluate the discriminability of our end-to-end learned features. As shown in Fig. 6, FF works on the pose estimation workload, but not on the face detection workload. The “Worst” case is calculated by r = 1 − Acc. The reason may be that there is a “person” label in the ImageNet dataset, so the pre-trained feature embedding in FF is discriminative for determining whether there is a human pose. However, on other tasks (e.g., FD, GC, and AC), the pre-trained features are not discriminative and FF can only provide two extreme filtering policies: either filtering all input or filtering nothing, which is useless in practice. On the contrary, InFi-Skip learns feature embedding with robust discriminability and performs well on all four workloads. With over 90% inference accuracy, InFi-Skip can filter 18.9% and 36.1% inputs for PE and FD workloads, respectively.

Transferability. One interesting question is, how transferable is the trained filter to workloads with a looser or tighter redundancy measurement? We set the minimal number of recognized words, N, as 0 and 2 and train two InFi-Skip filters. Then we test the two filters on two test sets with different N. As shown in Fig. 7, the performance of InFi-Skip (N=2) is close to InFi-Skip (N=0) when tested with N=0, however, the performance of InFi-Skip (N=0) is apparently worse when tested with N=2. An intuitive explanation is that the learned feature with a looser redundancy measurement covers the one with a tighter redundancy measurement, while the opposite is not true.

Sensitivity to class subset size. For the class-subset redundancy measurement, we set different subset sizes to test the sensitivity. As shown in Fig. 8, for action classification workload, setting a smaller class subset brings more redundant samples. And InFi-Skip robustly provides smooth accuracy-efficiency trade-off curves in both cases, which significantly outperforms FF (only two extreme points are provided).

Sensitivity to training size. We further divide training splits into sets with different sizes. As shown in Fig. 9, using only 10% samples from the training set, InFi can still achieve near-optimal performance on HAR workload. Let R denote the ratio of training samples used for training. When achieving over 95% inference accuracy, InFi-Skip (R=1) filters 86.4% inputs while InFi-Skip (R=0.1) still filters 81.1%. For high-accuracy reuse, the impact of training size is relatively greater. When filtering 90% inputs, InFi-Reuse (R=1) can achieve 95.9% inference accuracy, while the accuracy of InFi-Reuse (R=0.1) decreases to 88.1%.

![](images/d9f61f1302cfc1dfdcfa7f0f3004a3a75d77402a470e616bd74fd0111589972c.jpg)



(a) NDense=200, EmbLen=128

![](images/9f2f2a6bbb21fe4191e1c4ab4e61f3d8d3129a4191848d8727a9b576196966d5.jpg)



(b) Model Complexity   
Fig. 10: InFi-Skip on UI workload. NDense is the number of dense units. EmbLen is the length of embedding.

![](images/101864570660e75973748cf3a86753526ae7a55902c44170bf6d81a33f46d52d.jpg)



(a) SKIP Methods

![](images/e359a763dcaa8687516ca13b4708bb0459f85d07f6ac450a02cd6328de51ea43.jpg)



(b) REUSE Methods   
Fig. 12: Comparisons of filters on VC and VC-MP.

![](images/9622acb6dd736dfaa82b4eb5d545fbb7cd0334f2f8034fa18ffe327d55f5f314.jpg)



(a) Gender Classification

![](images/2202a7a514392d395c19ce3f7110213639101c3d575c2ce892c87e9e7c0bfce6.jpg)



(b) Action Classification   
Fig. 11: Comparison of FC and InFi-Reuse on visual classification workloads. K is the parameter in KNN.

![](images/0243449b7854dbf61b13cf9a62e6ae8fdf53404a5f575d2a489ff1a92a958d01.jpg)



(a) Modulation Recognition

![](images/b8c90e750cfa00b9fdb3dfbfe3577e963b91a6496c12ba27fd154ae8d24dfc6e.jpg)



(b) WiFi Action Recognition   
Fig. 13: InFi-Skip on on MR and WAR workloads.

Sensitivity to model complexity. To explore the relationship between the complexity and performance of input filters, we trained InFi-Skip filters for the UI workload using the different lengths of embedding (1, 16, 32, 64, 128, 256) and the number of dense units (1, 100, 200, 400) in the classifier. And we measure the performance by the maximum filtering rate when achieving 90% inference accuracy. As shown in Fig. 10b, except for extreme cases (e.g., single dense or embedding unit), the filtering performance is relatively robust.

Sensitivity to K in KNN. The parameter K in KNN affects the classification accuracy. We vary K from 1 to 20 and test the REUSE filters’ performance. As shown in Fig. 11, on GC workload, InFi-Reuse is robust to varied K parameters, while FC suffers serious performance degradation. For example, with 90% inference accuracy, FC (K=5) can filter 68.4% inputs, while FC (K=1) can only filter 27.3% which is slightly higher than the random guess (20%). On the contrary, InFi-Reuse (K=1,5) can all achieve a 94.3% filtering rate with more than 95% inference accuracy. For the AC workload, the results show that the handcrafted feature SIFT is not discriminative, and all tested K parameters lead to similar performance with random labeling. InFi-Reuse can learn an action-related discriminative feature, it can filter 18.6% inputs and keep more than 90% inference accuracy (K=10).

Comparisons on VC(-MP) workloads. Unlike other datasets, the video frames arrive in time order rather than randomly. For VC-MP, we partition the YOLOv3 model to mobile-side (the first 39 layers) and edge-side (the rest layers). As shown in Fig. 12, InFi outperforms FF, Reducto, and FC, and also is the only applicable method for the VC-MP workload. With over 90% inference accuracy, InFi-Skip achieves 66.5% filtering rate, while FF and Reducto achieve 48.0% and 48.6%, respectively; InFi-Reuse filters 31.7% more inputs than FC when K=10. The results show the superiority of end-to-end learned features over handcrafted and pretrained ones.

Mobile-featured modalities. Radio signals and WiFi CSI (channel side information) are featured modalities for mobile AI applications. Fig. 13 shows the experimental results of applying InFi on two mobile-featured tasks: radio modulation recognition and WiFi CSI-based action recognition. Note that, existing methods cannot be applied to both tasks. With 90% target accuracy, InFi-Skip saves 40.9% and 11.6% computations for MR and WAR workloads, respectively.

Multi-task extension. In Sec. 5.3, we present how to extend InFi to multi-task workloads. We use the Hollywood2 dataset and corresponding inference tasks to evaluate the multi-task extension of InFi-Skip. First, we select three inference tasks on image modality: FD, GC, and PE. We build InFi-Skip filters using a single task, two tasks, and three tasks and evaluate their performance on each task. As shown in Fig. 14a, the multi-task filter outperforms singletask ones on all three tasks, improving the filtering rate up to 7.6% (for the GC task) when achieving 90% inference accuracy. Next, we select three inference tasks on different modalities: PE on images, NER on texts, and SR on audio. And we build InFi-Skip filters using a single modality, two modalities, and three modalities and evaluate them. As shown in Fig. 14b, fusing these multi-modality tasks into one filter results in a slight decrease in the filtering rate. But note that the overall efficiency is improved due to the shared parameters among different tasks.

Online active update. To evaluate the active strategy for online adaptation of InFi, we select the VC workload and compare three training methods: (1) Offline: selects the first 10% frames of a day to train; (2) Periodic: selects the first

![](images/6c06534c2ca40e8f52072c0e3fc9a6448ed6582db180a5c9c41703cf83e1e7d8.jpg)



(a) Single-Modality Multi-Task

![](images/cf55f47236e41f00d5384d8890f41fc711fe15a46ab4bb5ed298ce0baf4d0e19.jpg)



(b) Multi-Modality Multi-Task

Fig. 14: Comparison of single-task and multi-task InFi-Skip. The plus sign denotes joint training using multiple tasks.   
![](images/85df7cfc9506907e48e71328715c2b0b99180de9b7fb32c8df6e1f7a339ad01b.jpg)



Fig. 15: Active update of InFi-Skip on VC workload. The two successive frames, one infrared and one RGB, corresponds to the boxed time segment.

10% frames of each hour to train and update; (3) Active: see Sec. 5.4. For a fair comparison, we set the same threshold (0.5) for the three methods. As shown in Fig. 15, our proposed active strategy significantly improves the online adaptability of InFi-Skip. The offline policy’s performance seriously degrades when the input distribution changes, mainly because the frames change from infrared to RGB images. On average, the offline policy achieves only 56.4% inference accuracy. The periodic update policy alleviates this problem to some extent, improving the average accuracy to 87.0%, but still suffers from performance fluctuations. The active strategy’s performance only drops at the 7th time segment, as it does not see any RGB images before that. And the active strategy effectively selects informative samples to fit the new distribution and performs accurate filtering robustly. On average, our active policy achieves 94.8% inference accuracy, which is 38.4% higher than the offline policy.

# 6.3 Filterability

In Sec. 3, we compare the hypothesis complexity of the inference and filter models. Let “Conf.>T” denote the lowconfidence classification case (§ 3.2), “Class Subset” denote the redundant class subset case (§ 3.3), and “Reg.>T” denote the bounded regression case (§ 3.4). GC and SC belong to the “Conf.>T” case, where T is 0.9. AC, NER, and HAR belong to the “Class Subset” case, where AC selects 2 action labels, NER selects the “PERSON” label, and HAR

![](images/06e59f9d416208459a06a8c4d5aa021cef3bd1deb0125720e04a7e4abd9b3230.jpg)



Fig. 16: Comparison of filterable and non-filterable cases.

![](images/c49e289877a3614910c2d578d966556ddf2cb2214e8c83ffaccbba99fd43e961.jpg)



Fig. 17: Latency and energy costs of InFi (image modality) and MobileNetV1 on mobile platforms.

selects the “LAYING” label. FD, PE, and VC(MP) belong to the ‘Reg.>T” case, where T is 0. SR is a sequence-tosequence model, which cannot perfectly fit any of these three cases. We compute the ratio of the resulting filtering rate to the optimal filtering rate at 90% inference accuracy to compare the filterability of different cases. From a practical perspective, we evaluate the overall throughput with and without InFi-Skip filters. As shown in Fig. 16, the “Conf.>T” case in which we proved that the filter’s complexity is not less than the inference model achieves obviously lower filtering ratio (0.41 median), while other cases in which we proved that the filter tends to be less complex achieve apparently higher ratios (0.71/0.78 medians). On the other hand, the overall throughput improved by InFi-Skip filters on filterable cases is more significant than the non-filterable cases. In the non-filterable cases, GC and SC, InFi achieves around 1.3× throughput, while in the filterable cases, it can improve the throughput up to 5.92× and achieves 1.8 and 2.25 medians for regression and subset-class cases, respectively. These results show the guiding significance of our proven filterability in real applications.

# 6.4 Computation and Resource Efficiency

As we discussed in Sec. 2.2, a “valid” filter should be both accurate and lightweight. The above results have shown that InFi can filter a significant amount of inputs while keeping accurate inference. In the training phase, InFi (image modality) takes around 710 ms per batch (batch size is 32) and requires 5337 MB GPU memory which most commercial GPUs can meet. InFi for other input modalities requires far fewer resources, e.g., InFi (vector) tasks 3 ms per batch and needs only 435 MB memory. We test the latency and energy in the inference phase on mobile platforms. As a fair comparison, we chose the TFLite-optimized MobileNetV1, which is one of the most efficient CNNs on mobile devices. As shown in Fig. 17, on three mobile platforms, InFi with the image feature network costs only 12-25% runtime of

MobileNetV1. The average energy costs of InFi are 14.4/79.7 mJ per frame, which are much lower than MobileNetV1 (410.4/803.8 mJ per frame) on the phone/smartwatch. We implement InFi with MindSpore and the results show that InFi’s low-energy consumption and low-latency execution do not depend on the implementation framework.

On-device online update. Based on the Chaquopy library, we tested the overhead of training on a mobile phone (XIAOMI Mi 5) and a smartwatch (HUAWEI WATCH). We randomly generated images with the shape (224, 224, 3) and set the batch size as 16. For InFi (image modality), experiments show that it takes around 20 s and 50 s per batch to online update weights on the phone and the watch, respectively. And for NVIDIA JETSON TX2, training the input filter with the same configurations takes around 1s per batch.

# 6.5 Different Mobile-centric Deployments

Now we evaluate the overall performance of inference workloads in real systems with three ways of deployments.

Vehicle counting. First, we consider the vehicle counting workload: 1) on-device: InFi (image) and YOLOv3 model on TX2; 2) offload: InFi (image) on TX2 and YOLOv3 model on edge; 3) model partitioning (MP): first 39 layers (10 convolution blocks) of YOLOv3 and InFi (feature map) on TX2, rest of YOLOv3 on the edge server. The average throughput of the YOLOv3 model on TX2 and edge is 3.2 FPS and 22.0 FPS, respectively. For MP deployment, the edge-side model serves 24.5 FPS. We report the average throughput and the bandwidth saving of using InFi-Skip and InFi-Reuse, with over 90% inference accuracy, in Tab. 4. As a fair comparison, we test the throughput of YOLOv3- tiny [12] model, a compressed version for YOLOv3. The inference accuracy of YOLOv3-tiny is only 67.9% which does not meet the 90% target. Breaking down the overheads, InFi’s inference costs around 3 ms per frame, and the average latency of KNN is 6 ms per frame with K=10 and cache size=1000. Achieving over 90% inference accuracy, InFi-Skip improves the throughput to 9.3/55.2/39.0 FPS for on-device/offload/MP deployments, respectively. Apparently, in vehicle counting workloads, there are more filtering opportunities for InFi-Reuse. InFi-Reuse improves the throughput to 27.2/77.2/46.0 FPS for these three deployments. Except for the on-device deployment that does not involve cross-device data transmission, InFi-Skip / InFi-Reuse also save 66.5% / 91.1% and 70.7% / 95.0% bandwidth for offloading and MP workloads. Unlike YOLOv3- tiny which trades a significant and fixed loss of accuracy for efficiency, InFi provides a flexible trade-off between the inference accuracy and overheads.

Pose estimation. Second, we evaluate the pose estimation workload: 1) on-device: InFi (image) and OpenPose model on TX2; 2) offload: InFi (image) on TX2 and Open-Pose model on edge; 3) model partitioning (MP): first 39 layers (10 convolution blocks) of OpenPose and InFi (feature map) on TX2, rest of OpenPose on the edge server. Also, we test the throughput of OpenPose-light [13] model, a lightweight version of OpenPose. Experimental results are shown in Tab. 5. Similar to the vehicle counting workload, the lightweight model cannot achieve our target 90% inference accuracy, although its throughput boosts significantly.

TABLE 4: Throughput (FPS) / Bandwidth saving (%) of vehicle counting workloads. Acc. denotes inference accuracy, compared with vehicle count results of YOLOv3. 

<table><tr><td>Workload</td><td>YOLOv3</td><td>InFi-Skip</td><td>InFi-Reuse</td><td>YOLOv3-tiny</td></tr><tr><td>Acc. (%)</td><td>100</td><td>90.3</td><td>90.5</td><td>67.9</td></tr><tr><td>On-device</td><td>3.2/-</td><td>9.3/-</td><td>27.2/-</td><td>20.4/-</td></tr><tr><td>Offloading</td><td>22.0/-</td><td>55.2/66.5</td><td>77.2/91.1</td><td>225.3/-</td></tr><tr><td>MP</td><td>24.5/-</td><td>39.0/70.7</td><td>46.0/95.0</td><td>230.4/-</td></tr></table>

TABLE 5: Throughput (FPS) / Bandwidth saving (%) of pose estimation workloads. 

<table><tr><td>Workload</td><td>OpenPose</td><td>InFi-Skip</td><td>OpenPose-light</td></tr><tr><td>Inference Accuracy (%)</td><td>100</td><td>90.1</td><td>76.5</td></tr><tr><td>On-device</td><td>15.4/-</td><td>18.0/-</td><td>28.1/-</td></tr><tr><td>Offloading</td><td>27.7/-</td><td>31.5/18.9</td><td>98.5/-</td></tr><tr><td>MP</td><td>29.2/-</td><td>33.1/20.2</td><td>102.4/-</td></tr></table>

InFi-Skip can flexibly balance the inference accuracy and throughput. For example, for the on-device deployment, the throughput improves to 1.17× after using InFi-Skip and the inference accuracy keeps over 90%.

Natural language processing workloads. Third, we test two NLP workloads, NER and SC, with different deployments. Note that, model partitioning is not applicable to our NER workload due to black-box APIs. As shown in Tab. 6, InFi-Skip effectively improves throughput and saves 22.5% and 26.8% offloading communication for the two tasks, respectively.

# 7 RELATED WORK

Frame filtering. NoScope [24] trains task-specific difference detectors to choose necessary frames for object queries in the video database. FilterForward [19] leverages MobileNet and trains a binary micro-classifier on the intermediate output of a selected layer to determine whether to transmit the input image to the server with the offloaded model. Reducto [20] performs on-device frame filtering by thresholding the difference of low-level features between successive frames. Through elaborate selection for different tasks, lowlevel features can efficiently and accurately measure the difference.

Inference caching. Potluck [22] stores and shares inference results between augmented reality applications. It dynamically tunes the threshold of input similarity and manages cache based on the reuse opportunities. Foggy-Cache [21] is more general and can be applied to both image and audio inputs. It designs adaptive LSH and homogenized KNN algorithms to address practical challenges in inference caching. Instead of caching the final inference results, DeepCache [69] stores the intermediate feature maps to achieve more granular reuse. For object recognition, Glimpse [23] maintains a cache of video frames on mobile devices. It uses cached results to perform on-device object tracking and sends only trigger frames to the server with offloaded recognition model.

Approaches tailored for specific pipelines. Focus [70] is designed for querying detected objects in a video database and uses compressed CNN to index possible object classes at ingest stage and reduces the query latency by clustering similar objects. Blazeit [71] develops neural networks-based methods to optimize approximate aggregation queries of detected objects in video databases. Focusing on object detection in video streams, Chameleon [72] proposes to adaptively select a suitable pipeline configuration including the resolution and frame rate of videos, backbone neural networks for inference, etc. Elf [11] is designed for mobile video analytics where the input data is pre-processed by a lightweight on-device model and then offloaded in parallel to multiple servers with the same subsequent inference functionality.

TABLE 6: Throughput (QPS) / Bandwidth saving (%) of two NLP workloads. 

<table><tr><td>Workload</td><td>NER</td><td>NER+InFi-Skip</td><td>SC</td><td>SC+InFi-Skip</td></tr><tr><td>Acc. (%)</td><td>100</td><td>90.2</td><td>100</td><td>90.0</td></tr><tr><td>On-device</td><td>24.3/-</td><td>33.2/-</td><td>27.9/-</td><td>36.0/-</td></tr><tr><td>Offloading</td><td>133.2/-</td><td>181.9/26.8</td><td>60.2/-</td><td>77.7/22.5</td></tr><tr><td>MP</td><td>N/A</td><td>N/A</td><td>62.5/-</td><td>82.0/24.1</td></tr></table>

Our proposed input-filtering framework unifies the frame filtering and inference caching approaches. And we complement existing work in theoretical analysis and flexible supports for more input modalities and deployments.

# 8 CONCLUSION

In this paper, we study the input filtering problem and provide theoretical results on complexity comparisons between the hypothesis families of inference models and their input filters. We propose the first end-to-end learnable framework that unifies both SKIP and REUSE methods and supports multiple input modalities and deployments. We design and implement an input filter system InFi based on our framework. Comprehensive evaluations confirm our proven results and show that InFi has wider applicability and outperforms strong baselines on accuracy and efficiency.

# ACKNOWLEDGMENTS

This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, No. 62132018. This work is partially sponsored by CAAI-Huawei MindSpore Open Fund and “the Fundamental Research Funds for the Central Universities” WK2150110024.

# REFERENCES

[1] M. Yuan, L. Zhang, F. He, X. Tong, and X.-Y. Li, “Infi: Endto-end learnable input filter for resource-efficient mobile-centric inference,” in The 28th Annual International Conference On Mobile Computing And Networking (MobiCom ’22), 2022.   
[2] C. Liu, L. Zhang, Z. Liu, K. Liu, X. Li, and Y. Liu, “Lasagna: Towards deep hierarchical understanding and searching over mobile sensing data,” in Proceedings of the 22nd Annual International Conference on Mobile Computing and Networking, ser. MobiCom ’16. New York, NY, USA: Association for Computing Machinery, 2016, p. 334–347.

[3] A. N. Mazumder, J. Meng, H.-A. Rashid, U. Kallakuri, X. Zhang, J.-S. Seo, and T. Mohsenin, “A survey on the optimization of neural network accelerators for micro-ai on-device inference,” IEEE Journal on Emerging and Selected Topics in Circuits and Systems, vol. 11, no. 4, pp. 532–547, 2021.   
[4] E. Li, L. Zeng, Z. Zhou, and X. Chen, “Edge ai: On-demand accelerating deep neural network inference via edge computing,” IEEE Transactions on Wireless Communications, vol. 19, no. 1, pp. 447–457, 2019.   
[5] X. Wang, Y. Han, C. Wang, Q. Zhao, X. Chen, and M. Chen, “In-edge ai: Intelligentizing mobile edge computing, caching and communication by federated learning,” IEEE Network, vol. 33, no. 5, pp. 156–165, 2019.   
[6] D. Chatzopoulos, C. Bermejo, Z. Huang, and P. Hui, “Mobile augmented reality survey: From where we are to where we go,” IEEE Access, vol. 5, pp. 6917–6950, 2017.   
[7] J. Wang, Z. Feng, Z. Chen, S. George, M. Bala, P. Pillai, S.-W. Yang, and M. Satyanarayanan, “Bandwidth-efficient live video analytics for drones via edge computing,” in 2018 IEEE/ACM Symposium on Edge Computing (SEC). IEEE, 2018, pp. 159–173.   
[8] G. Ghiasi, Y. Cui, A. Srinivas, R. Qian, T.-Y. Lin, E. D. Cubuk, Q. V. Le, and B. Zoph, “Simple copy-paste is a strong data augmentation method for instance segmentation,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2021, pp. 2918–2928.   
[9] A. Bulat, J. Kossaifi, G. Tzimiropoulos, and M. Pantic, “Toward fast and accurate human pose estimation via soft-gated skip connections,” in 2020 15th IEEE International Conference on Automatic Face and Gesture Recognition (FG 2020). IEEE, 2020, pp. 8–15.   
[10] H. Jiang, P. He, W. Chen, X. Liu, J. Gao, and T. Zhao, “Smart: Robust and efficient fine-tuning for pre-trained natural language models through principled regularized optimization,” in Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, 2020, pp. 2177–2190.   
[11] W. Zhang, Z. He, L. Liu, Z. Jia, Y. Liu, M. Gruteser, D. Raychaudhuri, and Y. Zhang, “Elf: accelerate high-resolution mobile deep vision with content-aware parallel offloading,” in Proceedings of the 27th Annual International Conference on Mobile Computing and Networking, 2021, pp. 201–214.   
[12] P. Adarsh, P. Rathi, and M. Kumar, “Yolo v3-tiny: Object detection and recognition using one stage improved model,” in 2020 6th International Conference on Advanced Computing and Communication Systems (ICACCS). IEEE, 2020, pp. 687–694.   
[13] D. Osokin, “Real-time 2d multi-person pose estimation on cpu: Lightweight openpose,” in ICPRAM 2019-Proceedings of the 8th International Conference on Pattern Recognition Applications and Methods, 2019, pp. 744–748.   
[14] Z. Sun, H. Yu, X. Song, R. Liu, Y. Yang, and D. Zhou, “Mobilebert: a compact task-agnostic bert for resource-limited devices,” in Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, 2020, pp. 2158–2170.   
[15] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, “Mobilenetv2: Inverted residuals and linear bottlenecks,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2018, pp. 4510–4520.   
[16] M. Tan, B. Chen, R. Pang, V. Vasudevan, M. Sandler, A. Howard, and Q. V. Le, “Mnasnet: Platform-aware neural architecture search for mobile,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2019, pp. 2820–2828.   
[17] S. Han, H. Shen, M. Philipose, S. Agarwal, A. Wolman, and A. Krishnamurthy, “Mcdnn: An approximation-based execution framework for deep stream processing under resource constraints,” in Proceedings of the 14th Annual International Conference on Mobile Systems, Applications, and Services, 2016, pp. 123–136.   
[18] Y. He, J. Lin, Z. Liu, H. Wang, L.-J. Li, and S. Han, “Amc: Automl for model compression and acceleration on mobile devices,” in Proceedings of the European conference on computer vision (ECCV), 2018, pp. 784–800.   
[19] C. Canel, T. Kim, G. Zhou, C. Li, H. Lim, D. G. Andersen, M. Kaminsky, and S. Dulloor, “Scaling video analytics on constrained edge nodes,” in Proceedings of Machine Learning and Systems, A. Talwalkar, V. Smith, and M. Zaharia, Eds., vol. 1, 2019, pp. 406–417.   
[20] Y. Li, A. Padmanabhan, P. Zhao, Y. Wang, G. H. Xu, and R. Netravali, “Reducto: On-camera filtering for resource-efficient realtime video analytics,” in Proceedings of the Annual Conference of the ACM Special Interest Group on Data Communication on the

Applications, Technologies, Architectures, and Protocols for Computer Communication, ser. SIGCOMM ’20. New York, NY, USA: Association for Computing Machinery, 2020, p. 359–376.   
[21] P. Guo, B. Hu, R. Li, and W. Hu, “Foggycache: Cross-device approximate computation reuse,” in Proceedings of the 24th Annual International Conference on Mobile Computing and Networking, 2018, pp. 19–34.   
[22] P. Guo and W. Hu, “Potluck: Cross-application approximate deduplication for computation-intensive mobile applications,” in Proceedings of the Twenty-Third International Conference on Architectural Support for Programming Languages and Operating Systems, 2018, pp. 271–284.   
[23] T. Y.-H. Chen, L. Ravindranath, S. Deng, P. Bahl, and H. Balakrishnan, “Glimpse: Continuous, real-time object recognition on mobile devices,” in Proceedings of the 13th ACM Conference on Embedded Networked Sensor Systems, 2015, pp. 155–168.   
[24] D. Kang, J. Emmons, F. Abuzaid, P. Bailis, and M. Zaharia, “Noscope: Optimizing neural network queries over video at scale,” Proceedings of the VLDB Endowment, vol. 10, no. 11, 2017.   
[25] Y. Wen, K. Zhang, Z. Li, and Y. Qiao, “A discriminative feature learning approach for deep face recognition,” in European conference on computer vision. Springer, 2016, pp. 499–515.   
[26] M. Mohri, A. Rostamizadeh, and A. Talwalkar, Foundations of machine learning. MIT press, 2018.   
[27] M. J. Kearns, U. V. Vazirani, and U. Vazirani, An introduction to computational learning theory. MIT press, 1994.   
[28] L. Zhou, H. Wen, R. Teodorescu, and D. H. Du, “Distributing deep neural networks with containerized partitions at the edge,” in 2nd USENIX Workshop on Hot Topics in Edge Computing (HotEdge 19), 2019.   
[29] L. Valiant, Probably Approximately Correct: Nature’s Algorithms for Learning and Prospering in a Complex World. Basic Books (AZ), 2013.   
[30] V. Vapnik and A. Y. Chervonenkis, “On the uniform convergence of relative frequencies of events to their probabilities,” Theory of Probability & Its Applications, vol. 16, no. 2, pp. 264–280, 1971.   
[31] N. Harvey, C. Liaw, and A. Mehrabian, “Nearly-tight vcdimension bounds for piecewise linear neural networks,” in Conference on learning theory. PMLR, 2017, pp. 1064–1068.   
[32] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollar, and C. L. Zitnick, “Microsoft coco: Common objects in ´ context,” in European conference on computer vision. Springer, 2014, pp. 740–755.   
[33] M. Yuan, L. Zhang, X.-Y. Li, and H. Xiong, “Comprehensive and efficient data labeling via adaptive model scheduling,” in 2020 IEEE 36th International Conference on Data Engineering (ICDE). IEEE, 2020, pp. 1858–1861.   
[34] M. Yuan, L. Zhang, X.-Y. Li, L.-Z. Yang, and H. Xiong, “Adaptive model scheduling for resource-efficient data labeling,” ACM Trans. Knowl. Discov. Data, vol. 16, no. 4, jan 2022.   
[35] Y. Duan, C. Jin, and Z. Li, “Risk bounds and rademacher complexity in batch reinforcement learning,” in International Conference on Machine Learning. PMLR, 2021, pp. 2892–2902.   
[36] C. Cortes, V. Kuznetsov, M. Mohri, and S. Yang, “Structured prediction theory based on factor graph complexity,” Advances in Neural Information Processing Systems, vol. 29, pp. 2514–2522, 2016.   
[37] T. Glasmachers, “Limits of end-to-end learning,” in Asian Conference on Machine Learning. PMLR, 2017, pp. 17–32.   
[38] A. Prakash, K. Chitta, and A. Geiger, “Multi-modal fusion transformer for end-to-end autonomous driving,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2021, pp. 7077–7087.   
[39] D. Amodei, S. Ananthanarayanan, R. Anubhai, J. Bai, E. Battenberg, C. Case, J. Casper, B. Catanzaro, Q. Cheng, G. Chen et al., “Deep speech 2: End-to-end speech recognition in english and mandarin,” in International conference on machine learning. PMLR, 2016, pp. 173–182.   
[40] G. Koch, R. Zemel, R. Salakhutdinov et al., “Siamese neural networks for one-shot image recognition,” in ICML deep learning workshop, vol. 2. Lille, 2015.   
[41] Y. Taigman, M. Yang, M. Ranzato, and L. Wolf, “Deepface: Closing the gap to human-level performance in face verification,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2014, pp. 1701–1708.   
[42] L. Leal-Taixe, C. Canton-Ferrer, and K. Schindler, “Learning by ´ tracking: Siamese cnn for robust target association,” in Proceedings

of the IEEE Conference on Computer Vision and Pattern Recognition Workshops, 2016, pp. 33–40.   
[43] F. Chollet, “Xception: Deep learning with depthwise separable convolutions,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2017, pp. 1251–1258.   
[44] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.   
[45] I. Indrawan, I. Bayupati, and D. P. S. Putri, “Markerless augmented reality utilizing gyroscope to demonstrate the position of dewata nawa sanga.” International Journal of Interactive Mobile Technologies, vol. 12, no. 1, 2018.   
[46] D. Anguita, A. Ghio, L. Oneto, X. Parra, J. L. Reyes-Ortiz et al., “A public domain dataset for human activity recognition using smartphones.” in Esann, vol. 3, 2013, p. 3.   
[47] A. Prakash, K. Chitta, and A. Geiger, “Multi-modal fusion transformer for end-to-end autonomous driving,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2021, pp. 7077–7087.   
[48] A. Maurer, M. Pontil, and B. Romera-Paredes, “The benefit of multitask representation learning,” Journal of Machine Learning Research, vol. 17, no. 81, pp. 1–32, 2016.   
[49] N. Tripuraneni, M. Jordan, and C. Jin, “On the theory of transfer learning: The importance of task diversity,” Advances in Neural Information Processing Systems, vol. 33, pp. 7852–7862, 2020.   
[50] R. Hadsell, S. Chopra, and Y. LeCun, “Dimensionality reduction by learning an invariant mapping,” in 2006 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR’06), vol. 2. IEEE, 2006, pp. 1735–1742.   
[51] R. T. Mullapudi, S. Chen, K. Zhang, D. Ramanan, and K. Fatahalian, “Online model distillation for efficient video inference,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2019, pp. 3573–3582.   
[52] D. D. Lewis and J. Catlett, “Heterogeneous uncertainty sampling for supervised learning,” in Machine learning proceedings 1994. Elsevier, 1994, pp. 148–156.   
[53] M.-F. Balcan, S. Hanneke, and J. W. Vaughan, “The true sample complexity of active learning,” Machine learning, vol. 80, no. 2, pp. 111–139, 2010.   
[54] J. Liu and Q. Zhang, “Code-partitioning offloading schemes in mobile edge computing for augmented reality,” Ieee Access, vol. 7, pp. 11 222–11 236, 2019.   
[55] X. Tian, J. Zhu, T. Xu, and Y. Li, “Mobility-included dnn partition offloading from mobile devices to edge clouds,” Sensors, vol. 21, no. 1, p. 229, 2021.   
[56] S. A. Osia, A. S. Shamsabadi, S. Sajadmanesh, A. Taheri, K. Katevas, H. R. Rabiee, N. D. Lane, and H. Haddadi, “A hybrid deep learning architecture for privacy-preserving mobile analytics,” IEEE Internet of Things Journal, vol. 7, no. 5, pp. 4505–4518, 2020.   
[57] M. Marszałek, I. Laptev, and C. Schmid, “Actions in context,” in IEEE Conference on Computer Vision & Pattern Recognition, 2009.   
[58] A. Tran and L.-F. Cheong, “Two-stream flow-guided convolutional attention networks for action recognition,” in The IEEE International Conference on Computer Vision Workshop (ICCVW), 2017.   
[59] S. I. Serengil and A. Ozpinar, “Lightface: A hybrid deep face recognition framework,” in 2020 Innovations in Intelligent Systems and Applications Conference (ASYU). IEEE, 2020, pp. 23–27.   
[60] Z. Cao, G. Hidalgo Martinez, T. Simon, S. Wei, and Y. A. Sheikh, “Openpose: Realtime multi-person 2d pose estimation using part affinity fields,” IEEE Transactions on Pattern Analysis and Machine Intelligence, 2019.   
[61] K. Xu, J. Ba, R. Kiros, K. Cho, A. Courville, R. Salakhudinov, R. Zemel, and Y. Bengio, “Show, attend and tell: Neural image caption generation with visual attention,” in International conference on machine learning. PMLR, 2015, pp. 2048–2057.   
[62] M. Honnibal, I. Montani, S. Van Landeghem, A. Boyd et al., “spacy: Industrial-strength natural language processing in python,” 2020.   
[63] Y. Kim, “Convolutional neural networks for sentence classification,” in Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP). Doha, Qatar: Association for Computational Linguistics, Oct. 2014, pp. 1746–1751.   
[64] K. J. Piczak, “ESC: Dataset for Environmental Sound Classification,” in Proceedings of the 23rd Annual ACM Conference on Multimedia. ACM Press, pp. 1015–1018.   
[65] Y. Gong, Y.-A. Chung, and J. Glass, “AST: Audio Spectrogram Transformer,” in Proc. Interspeech 2021, 2021, pp. 571–575.

[66] A. Gardner, J. Kanno, C. A. Duncan, and R. Selmic, “Measuring distance between unordered sets of different sizes,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2014, pp. 137–143.   
[67] T. J. O’Shea, T. Roy, and T. C. Clancy, “Over-the-air deep learning based radio signal classification,” IEEE Journal of Selected Topics in Signal Processing, vol. 12, no. 1, pp. 168–179, 2018.   
[68] A. Zhuravchak, O. Kapshii, and E. Pournaras, “Human activity recognition based on wi-fi csi data-a deep neural network approach,” Procedia Computer Science, vol. 198, pp. 59–66, 2022.   
[69] M. Xu, M. Zhu, Y. Liu, F. X. Lin, and X. Liu, “Deepcache: Principled cache for mobile deep vision,” in Proceedings of the 24th Annual International Conference on Mobile Computing and Networking, 2018, pp. 129–144.   
[70] K. Hsieh, G. Ananthanarayanan, P. Bodik, S. Venkataraman, P. Bahl, M. Philipose, P. B. Gibbons, and O. Mutlu, “Focus: Querying large video datasets with low latency and low cost,” in 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18), 2018, pp. 269–286.   
[71] D. Kang, P. Bailis, and M. Zaharia, “Blazeit: Optimizing declarative aggregation and limit queries for neural network-based video analytics,” Proceedings of the VLDB Endowment, vol. 13, no. 4.   
[72] J. Jiang, G. Ananthanarayanan, P. Bodik, S. Sen, and I. Stoica, “Chameleon: scalable adaptation of video analytics,” in Proceedings of the 2018 Conference of the ACM Special Interest Group on Data Communication, 2018, pp. 253–266.

![](images/15050d7c113325de054de7ca78f6620c6878485e90300f9a2cc035e800f86816.jpg)



Xueting Tong is a master’s candidate at the Institute of Advanced Technology, University of Science and Technology of China. She received a bachelor’s degree in Computer Science and technology from Henan University. Her research interests include model reasoning and optimization.

![](images/628c73ca13b2fb328b37db973c9befa65ac460cdb51063404ca0846db686147f.jpg)



Miao-Hui Song is a master student at the School of Computer Science and Technology, University of Science and Technology of China. She received a bachelor’s degree in computer science and technology from Chongqing University. Her research interests include active learning and data-labeling systems.

![](images/493a859d7f23d14ec625c472bcd281c43827a26178c876d952fde2d6ed22c6de.jpg)



Mu Yuan is a Ph.D. candidate at the School of Computer Science and Technology, University of Science and Technology of China (USTC). He received a bachelor’s degree in computer science and technology from USTC. His research interests include model inference and network systems.

![](images/f1c2d019c1aefda508f3e45e222073c6010e37e37b34823a9ccd333334ca472d.jpg)



Lan Zhang is currently a Professor at the School of Computer Science and Technology, University of Science and Technology of China. She received her Ph.D degree and Bachelor degree from Tsinghua University, China. Her research interests include mobile computing, privacy protection,and data sharing and trading.

![](images/e92badb2a0a540c6efd4ecbbb406d25ee40066ab491c9650368f2d770a793fe2.jpg)



Zhengyuan Xu received his B.S. and M.S. degrees from Tsinghua University, China, and Ph.D. degree from Stevens Institute of Technology, USA. He was a tenured full professor at University of California at Riverside and later at Tsinghua University before he joined University of Science and Technology of China (USTC). He was Founding Director of the multi-campus Center for Ubiquitous Communication by Light (UC-Light), University of California, and Founding Director of Wireless-Optical Communications Key Laboratory of Chinese Academy of Sciences. He was a distinguished expert and chief scientist of the National Key Basic Research Program of China. His research focuses on Petahertz communications, optical wireless communications, mobile networking, artificial intelligence, wireless big data, sensing, ranging and localization. He has published over 400 international journal and conference papers, and co-authored a book titled Visible Light Communications: Modulation and Signal Processing which has been selected by IEEE Series on Digital & Mobile Communication and published by Wiley-IEEE Press. He has been on the Elsevier annual list of Most Cited Chinese Researchers since 2014. He has served as an Associate Editor for different IEEE/OSA journals and was a Founding Co-Chair of IEEE Workshop on Optical Wireless Communications in 2010.

![](images/26e74eee8006607dfd2f761eba4f3c49bac65a41b0bcc04437a19ac0d711d59b.jpg)



Fengxiang He received his BSc in statistics from University of Science and Technology of China, MPhil and PhD in computer science from the University of Sydney. He is currently algorithm scientist at JD Explore Academy leading its trustworthy AI team. His research interest is in the theory and practice of trustworthy AI, including deep learning theory, privacy-preserving ML, algorithmic game theory, and decentralized learning. He publish in prominent venues, including ICML, NeurIPS, ICLR, CVPR, and ICCV. He is the area chair of prestigious conferences, AISTATS, BMVC, and ACML. He is the leading author of several standards.

![](images/d3dc53e6f40a51f26d10612d656141be9fd52433ba80b7b8a3757daf2388f373.jpg)



Xiang-Yang Li (Fellow, IEEE) is a professor and Executive Dean at School of Computer Science and Technology, USTC. He is an ACM Fellow (2019), IEEE fellow (2015), an ACM Distinguished Scientist (2014). He was a full professor at Computer Science Department of IIT and co-Chair of ACM China Council. Dr. Li received M.S. (2000) and Ph.D. (2001) degree at Department of Computer Science from University of Illinois at Urbana-Champaign. He received a Bachelor degree at Department of Computer Science from Tsinghua University, P.R. China, in 1995. His research interests include Artificial Intelligence of Things (AIOT), privacy and security of AIOT, and data sharing and trading.