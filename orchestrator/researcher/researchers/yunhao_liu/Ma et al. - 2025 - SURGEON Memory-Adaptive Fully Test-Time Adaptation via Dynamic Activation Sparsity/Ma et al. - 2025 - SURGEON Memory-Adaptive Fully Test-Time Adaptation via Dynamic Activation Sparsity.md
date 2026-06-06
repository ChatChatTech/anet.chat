# SURGEON:

# Memory-Adaptive Fully Test-Time Adaptation via Dynamic Activation Sparsity

Ke Ma1,2 Jiaqi Tang3 Bin Guo1\* Fan Dang4 Sicong Liu1 Zhui Zhu2 Lei Wu1 Cheng Fang1 Ying-Cong Chen3 Zhiwen Yu1,5 Yunhao Liu2\* 1Northwestern Polytechnical University 2Tsinghua University 3The Hong Kong University of Science and Technology 4Beijing Jiaotong University 5Harbin Engineering University

Project Page: https://github.com/kadmkbl/SURGEON

# Abstract

Despite the growing integration of deep models into mobile terminals, the accuracy of these models declines significantly due to various deployment interferences. Testtime adaptation (TTA) has emerged to improve the performance of deep models by adapting them to unlabeled target data online. Yet, the significant memory cost, particularly in resource-constrained terminals, impedes the effective deployment of most backward-propagation-based TTA methods. To tackle memory constraints, we introduce SUR-GEON, a method that substantially reduces memory cost while preserving comparable accuracy improvements during fully test-time adaptation (FTTA) without relying on specific network architectures or modifications to the original training procedure. Specifically, we propose a novel dynamic activation sparsity strategy that directly prunes activations at layer-specific dynamic ratios during adaptation, allowing for flexible control of learning ability and memory cost in a data-sensitive manner. Among this, two metrics, Gradient Importance and Layer Activation Memory, are considered to determine the layer-wise pruning ratios, reflecting accuracy contribution and memory efficiency, respectively. Experimentally, our method surpasses the baselines by not only reducing memory usage but also achieving superior accuracy, delivering SOTA performance across diverse datasets, architectures, and tasks.

# 1. Introduction

In recent years, with the progression of artificial intelligence and Internet of Things (IoT) technologies, the integration of deep models into mobile terminals has become increasingly prevalent [26, 45]. However, due to various types of interference and distribution shifts [33] in deployment environments, such as changing weather conditions [34] and varying sensor parameters [18], the accuracy of deep models can significantly decline during inference.

![](images/82f74a67d6ef0101413ab77b476a9eedb3a07401bff35eb2f6b17d2146990f06.jpg)



Figure 1. The problem of memory-efficient TTA methods. (a) EcoTTA introduces meta networks to adapt the frozen backbone but requires modifications to the original training procedure to warm up these additional blocks. (b) MECTA establishes the updating criterion based on BN layers. (c) Our method, SURGEON prunes activations at layer-specific dynamic ratios without relying on specific architectures or modifications to the training procedure.

To address the aforementioned issue, test-time adaptation (TTA) [23, 39, 40] has emerged as an effective strategy to improve the performance of deep models by adapting them to unlabeled target data online. It proves to be particularly advantageous in situations where there is a significant disparity between the test and training data, or when real-time adaptation to fluctuating test environments is necessary. However, in some practical scenarios, the original training procedure cannot be modified due to concerns over privacy and the storage of training data. To address this, fully test-time adaptation (FTTA) has been proposed [31, 49] to allow deep models to adapt online without altering the original training procedure.

Nevertheless, memory cost becomes a major obstacle to deploying most backward-propagation-based TTA methods [3, 10, 28, 30, 47], particularly in memory-constrained terminals. In these methods, memory usage primarily arises from the storage of activations necessary for gradient calculation and weight updates during backpropagation (see §3.2). To address memory limitations in TTA, EcoTTA [37] is proposed as a solution where plug-and-play meta networks are designed additionally. Only these meta networks are updated while the backbone of the network is frozen during adaptation, effectively avoiding the memory usage of storing activations for the frozen layers. However, this approach necessitates modifications to the original training procedure for initializing the additional blocks, making it impractical to deploy in FTTA scenarios, as shown in Figure 1 (a). MECTA [16] has been introduced as a method suitable for FTTA, which effectively reduces memory cost at the batch, channel, and layer levels. However, as shown in Figure 1 (b), this method relies on Batch Normalization (BN) layers to establish the updating criterion, limiting its applicability to transformer-based architectures [29]. Therefore, previous methods have significant limitations regarding the training procedure or network architectures.

To deal with the above problem, we first declare the optimization goal, which is to achieve the optimal trade-off between minimizing memory cost and maximizing accuracy during adaptation. Upon deeper analysis, we find that the optimization bottleneck is the memory usage of activations that are cached for gradient calculation and weight updates during backpropagation (§ 3.2).

To this end, we propose SURGEON, an effective and easily deployable strategy for memory-efficient FTTA. It implements layer-wise pruning of activations across different layers during adaptation, without dependency on specific architectures or modifications to the original training procedure, as shown in Figure 1 (c). This strategy precisely controls the learning capacity and memory cost of different layers. Specifically, to determine the layer-wise activation pruning ratios, our method utilizes two key metrics: Gradient Importance (G) and Layer Activation Memory (M), which respectively characterize the accuracy contribution on the current data and the efficiency of activation memory usage. In contrast to existing techniques, such as layer freezing [21, 46] and methods employing a global static pruning ratio for activations [4, 17], our proposed dynamic activation sparsity offers greater adaptability in a data-sensitive manner. Experimentally, SURGEON achieves SOTA performance in both accuracy and memory cost compared to the baselines across diverse datasets, network architectures (convolution-based and transformer-based models), and tasks (image classification and semantic segmentation). Our contributions are as follows:

• We propose SURGEON for memory-adaptive fully testtime adaptation, which optimizes memory cost at each layer while maintaining comparable accuracy, without being constrained by specific architectures or modifications to the original training procedure.

• We propose a novel memory-efficient strategy, dynamic activation sparsity, which utilizes layer importance metrics that consider accuracy contribution and memory efficiency. This allows for more granular and flexible control over the learning ability and memory cost of different layers in dynamic FTTA scenarios.   
• Our method achieves SOTA performance in both accuracy and memory cost across a combination of different datasets, network architectures, and tasks.

# 2. Related Work

Memory-Efficient Fully Test-Time Adaptation To mitigate accuracy degradation caused by distribution shift, testtime adaptation (TTA) [3, 25, 28, 38, 47] adapts deep models to unlabelled data online. Recently, fully test-time adaptation (FTTA) has been developed, allowing the adaptation of pre-trained models [9] without modifying the original training procedure [31, 39, 49].

However, in resource-constrained terminals, the memory cost of backward propagation remains a major challenge for deployment [27, 32]. To address memory limitations in TTA, Song et al. propose EcoTTA [37], which enhances memory efficiency by updating plug-in meta networks while keeping the backbone frozen. However, it requires retraining the meta networks for several epochs using the training data before deployment, making it impractical for FTTA scenarios. Hong et al. introduce MECTA [16] to reduce memory usage by optimizing batch size, channels, and layers of adaptation without modifying the original training procedure. Specifically, it utilizes the statistics of BN layers to determine which subset of layers to update. However, MECTA’s reliance on specific layers limits its applicability to transformer-based architectures [29], which often lack BN layers. Our method significantly reduces the memory cost of FTTA while maintaining comparable accuracy improvements. Crucially, it does not rely on specific architectures or modifications to the training procedure, ensuring broader applicability.

Memory-Efficient Strategies for Backpropagation Existing works [2, 17, 41] have identified that significant adaptation memory cost mainly arises from storing activations for gradient calculation and weight updates during backpropagation. Therefore, the key to memory efficiency is reducing the memory usage of activations (see § 3.2).

One approach is to incorporate additional plug-andplay blocks [13, 22, 44] into the network, updating only these blocks during adaptation while keeping the backbone frozen. The limitation of this approach in FTTA is the necessity of warming up the additional blocks using the training data. Besides, gradient checkpointing (GC) [6] is a straightforward approach that avoids storing activations for a subset of layers and instead recomputes them before gradient calculation. However, since it does not alter the gradient values, its accuracy in TTA scenarios is limited. Another similar approach is layer freezing, where only a subset of network layers is adapted while the rest completely skip gradient calculation and weight updates. To select updated layers, some methods still require training procedure modifications for contribution analysis [24] or additional policy networks [21], while others use fixed epoch intervals to progressively freeze layers [46] or freeze converged layers by analyzing outputs across epochs [1].

Recently, some works [4, 17] explore direct pruning of activations across all layers during adaptation. Compared to layer freezing, this activation sparsity strategy allows for finer adjustment of the memory cost via customized pruning ratios. However, existing methods use a global static sparsity, discarding the unique and varying accuracy contributions of different layers [20], thus leaving room for accuracy improvement in dynamic FTTA scenarios.

# 3. Preliminary

# 3.1. Problem Definition

In fully test-time adaptation (FTTA), we refer to the problem definition from previous works [39]. Let $M _ { W }$ denote the deep models trained on source training data $D _ { t r a i n } \ = \ \{ ( x , \dot { y } ) \sim p _ { s } \}$ with weights W , where x and y˙ represent the input and ground truth, respectively. The goal of FTTA is to adapt $M _ { W }$ to target test data $D _ { t e s t } =$ $\{ ( x ) \sim p _ { t } \}$ online in an unsupervised manner, mitigating performance degradation from distribution shifts $( p _ { s } \neq p _ { t } )$ . The target data distribution $p _ { t }$ can change over time. Additionally, compared to general TTA, modifying the original training procedure is not allowed in FTTA [31].

Generally, the adaptation procedure is implemented based on backward propagation after forward propagation on a test batch [3, 30, 47], as shown below,

$$
y = f _ {W _ {l}} \left(\dots f _ {W _ {2}} \left(f _ {W _ {1}} (x)\right) \dots\right), L = \mathcal {L} (y), \tag {1}
$$

$$
\Delta A _ {i} = \frac {\partial L}{\partial A _ {i}} = \frac {\partial L}{\partial A _ {i + 1}} \frac {\partial A _ {i + 1}}{\partial A _ {i}} = \frac {\partial L}{\partial A _ {i + 1}} W _ {i} ^ {T}, \tag {2}
$$

$$
\Delta W _ {i} = \frac {\partial L}{\partial W _ {i}} = \frac {\partial L}{\partial A _ {i + 1}} \frac {\partial A _ {i + 1}}{\partial W _ {i}} = A _ {i} ^ {T} \frac {\partial L}{\partial A _ {i + 1}},
$$

where Eq.(1) and Eq.(2) illustrate the forward propagation of a network with l layers and the backward propagation of a single linear layer without bias. The formulations for different layer types are provided in the Appendix for further details. Here, L denotes the loss (e.g., entropy minimization [12]), fW is the function of the i-th layer with weights $W _ { i } ,$ , and $A _ { i + 1 } = f _ { W _ { i } } ( A _ { i } ) = W _ { i } A _ { i }$ represents the activations (i.e., output) of the i-th layer.

# 3.2. Optimization Objective

Our optimization objective is to achieve the optimal balance between minimizing memory cost and maximizing accuracy improvement during FTTA, as shown in Eq. (3).

$$
\min \quad \alpha \cdot \text { Memory } - \beta \cdot \text { Accuracy }, \tag {3}
$$

where $\alpha$ and $\beta$ regulate the trade-off between memory usage and accuracy. When updating the i-th layer, activations $A _ { i } ,$ weights $W _ { i } ,$ gradients $\Delta A _ { i }$ and $\Delta W _ { i }$ are cached for backpropagation (see Eq. (2)). It has been found that the primary memory bottleneck is the activations, $A _ { i } ,$ , which can consume over 80% or even more of adaptation memory usage, as analyzed in the Appendix. Therefore, the key to memory efficiency is reducing the activation memory cost.

# 4. Methodology

Motivation To achieve the objective (Eq. (3)), we propose a novel memory-efficient strategy, dynamic activation sparsity. By pruning cached activations $A _ { i }$ at layer-specific and dynamic ratios in a data-sensitive manner, this strategy precisely regulates both activation memory consumption and weight gradients $\Delta W _ { i }$ (see Eq.(2)) during adaptation. This is motivated by the finding that different layers exhibit distinct activation usage and contribute variably to accuracy under changing data distributions [20]. Compared to using a global static activation pruning ratio [4, 17], dynamic activation sparsity accounts for inter-layer differences and offers greater adaptability to dynamic FTTA scenarios.

Overview Initially, to drive dynamic activation pruning across layers, it is essential to evaluate and prioritize the importance of each layer. In § 4.1, we introduce two metrics: Gradient Importance (G) and Layer Activation Memory (M) to evaluate layer importance in terms of accuracy contribution and memory efficiency, respectively. Based on this importance evaluation, layer-wise dynamic activation pruning ratios are determined, and the workflow for FTTA with dynamic activation sparsity is proposed in § 4.2. Ultimately, SURGEON effectively balances memory cost and accuracy in FTTA without relying on specific architectures or modifications to the original training procedure.

# 4.1. Evaluating Importance for Activation Pruning

Gradient Importance Inspired by ideas that different layers contribute unequally to adaptation under varying data distributions [20], implementing layer-specific dynamic activation pruning based on accuracy contribution can further enhance accuracy compared to global static pruning. To achieve this, we first need to quantify the accuracy contribution of different layers. Here, the weight gradients are utilized as the reference metric. The insight is that layers with larger gradients have a more significant influence on model predictions and loss reduction, indicating their potential to capture richer knowledge and achieve greater accuracy gains on the current data [11]. The gradient importance of the i-th layer is expressed by Eq. (4),

![](images/ddca543849f8044cf8fa7e299c24604e6a2e8735f8570ebde4cb7ca0a0ba685a.jpg)



Figure 2. SURGEON prunes activations at layer-specifc dynamic ratios in a data-sensitive manner during adaptation. In forward propagation, it prunes activations $( A _ { i } \to { \dot { A } } _ { i } )$ before caching them into memory. In backward propagation, these sparse activations are used to calculate the weight gradients ∆Wi (see Eq. (2)). By employing dynamic activation sparsity, SURGEON substantially reduces the memory cost of adaptation while maintaining comparable accuracy in dynamic FTTA scenarios.

$$
\Delta w _ {i} = \frac {\partial L}{\partial w _ {i}}, \quad G _ {i} = \sqrt {\frac {\sum_ {j = 1} ^ {N _ {i}} \left(\Delta w _ {j}\right) ^ {2}}{N _ {i}}}, \tag {4}
$$

where $\Delta w _ { j }$ refers to the weight gradients of the neuron $j$ in the i-th layer and $N _ { i }$ denotes the number of neurons. In Eq. (4), $G _ { i } ,$ , the average gradient of individual neurons within the i-th layer serves as the quantification metric for layer gradient importance, as it reflects the layer’s impact on loss reduction and accuracy contribution during adaptation.

Layer Activation Memory Importance Besides gradient importance, we further consider activation memory efficiency for layer importance evaluation, which is quantified by the size of activation $A _ { i }$ . This metric directly reflects the activation memory usage needed for updating layer weights $W _ { i }$ . Incorporating this metric for layer-wise pruning can further improve memory efficiency during adaptation. Eq. (5) shows the activation memory importance of the i-th layer,

$$
m _ {i} = \mathbf {s i z e} (A _ {i}), \quad M _ {i} = - \log \left(\frac {m _ {i}}{\sum_ {i = 1} ^ {l} m _ {i}}\right), \tag {5}
$$

where $m _ { i }$ denotes the size of the activations $A _ { i } ,$ and $M _ { i }$ is calculated using the logarithm of the ratio between $m _ { i }$ and the total activation size across all layers.

Combination of Importance Metrics Finally, we combine these two layer importance metrics as shown in Eq. (6),

$$
I _ {i} = \mathbf {N o r m} (M _ {i}) \times \mathbf {N o r m} (G _ {i}), \tag {6}
$$

where $M _ { i }$ and $G _ { i }$ are scaled to [0,1] using Max Normalization for uniformity. Finally, the layer importance indicator, $I _ { i } ,$ , integrates the accuracy contribution and memory efficiency during adaptation to inform decisions on determining layer-wise activation pruning ratios.

# 4.2. Workflow of Dynamic Activation Sparsity

Once we have evaluated the layer importance using the combined metric $I _ { i }$ via Eq. (6), the next step is to determine the activation pruning ratios across different layers. Eq. (7) illustrates the process of converting $I _ { i }$ into layer-wise pruning ratios at the current data batch t,

$$
p _ {i} ^ {t} = 1 - \frac {I _ {i} ^ {t}}{\max _ {i \in \{1 , 2 , \dots , l \}} \left(I _ {i} ^ {t}\right)}, \tag {7}
$$

where the activation pruning ratio $p _ { i } ^ { t }$ of the i-th layer is calculated as 1 minus the ratio of $I _ { i } ^ { t }$ to the maximum value of the importance indicators across all layers. Overall, SUR-GEON encourages assigning low pruning ratios to activations $A _ { i }$ when layer weights $W _ { i }$ have large gradients due to these layers’ significant accuracy contribution on current data. Conversely, it tends to assign high pruning ratios to activations $A _ { i }$ with large sizes to further enhance memory efficiency during adaptation.

Figure 2 illustrates the layer-specific dynamic activation pruning process during adaptation. In the forward propagation, the activation $A _ { i }$ is pruned and cached immediately after $A _ { i + 1 }$ is computed. In the backward propagation, the cached sparse activation ${ \dot { A } } _ { i }$ is then used to calculate the weight gradients $\Delta W _ { i }$ (see Eq. (2)).

Algorithm 1 FTTA with Dynamic Activation Sparsity   
Require: Network with $l$ layers and weights $\{W_i\}$ , test data with total $n$ batches.

1: for each batch $t \in \{1, 2, \ldots, n\}$ do

2: Calculate pruning ratios $\{p^t\}$ across all layers via an additional forward-backward process
// Forward Propagation

3: for $i \in \{1, 2, \ldots, l\}$ do

4: $A_i \leftarrow$ Get the input of the $i$ -th layer

5: $A_{i+1} \leftarrow$ Calculate the output of the $i$ -th layer

6: $\dot{A}_i \leftarrow$ Prune the activations $A_i$ with ratio $p_i^t$ 7: $\hat{A}_i, idx_i \leftarrow$ Decompose $\dot{A}_i$ into the non-zero elements and the index, and cache them into memory

8: end for

9: Calculate Loss
// Backward Propagation

10: for $i \in \{l, l-1, \ldots, 1\}$ do

11: $\dot{A}_i \leftarrow$ Reshape( $\hat{A}_i, idx_i$ )

12: $\Delta A_i, \Delta W_i \leftarrow$ Calculate the activation gradients and weight gradients via Eq. (2) using $\dot{A}_i$ 13: end for

14: Update the weights with weight gradients $\{\Delta W_i\}$ 15: end for

Algorithm Finally, we summarize the workflow of our methods in Algorithm 1. Following Jiang et al. [17], to genuinely reduce memory usage within the processors, we cache the pruned activations $\dot { A } _ { i }$ as two components (line 7): ${ \hat { A } } _ { i }$ and $i d x _ { i } . \hat { A } _ { i }$ is a one-dimensional vector that stores only the non-zero elements of ${ \dot { A } } _ { i } ,$ while idxi records their indices using 1 bit per element. In the backward propagation, the pruned activations $\dot { A } _ { i }$ are first reshaped (line 11) and then used for gradient calculation (line 12).

Memory Efficiency of Layer Importance Calculation Notably, before the adaptation process, an additional forward-backward process is required initially to calculate the importance metrics $G _ { i }$ and $M _ { i }$ (line 2). To reduce the memory cost of the additional process and ensure that it does not exceed the peak memory usage of the following adaptation process, we can use two effective strategies: (i) randomly sampling a small subset of the current data batch, and (ii) applying a high global static pruning ratio (e.g., 90%) to acitvations. Details can be seen in the Appendix.

# 5. Experiments

# 5.1. Experimental Settings

Datasets and Architectures We employ two downstream tasks: image classification and semantic segmentation. For image classification, we use CIFAR10-C, CIFAR100-C and ImageNet-C [15] as the out-of-distribution test data originating from 15 types of corruptions at the severity level 5. For the network architectures, we utilize WideResNet-28 [48] trained on CIFAR10, ResNeXt-29 [43] trained on CIFAR100, and ResNet-50 (AugMix) [14] trained on ImageNet, with all these pre-trained weights from RobustBench [9]. For semantic segmentation, we use ACDC [34] as the out-of-distribution test data, which contains images collected in four different conditions (i.e., rain, snow, fog, night). For the network architectures, we utilize ResNet-50 (from the backbone of DeeplabV3+ [5]) and transformer-based Segformer-B5 [42] both trained on Cityscapes [8], with pre-trained weights from RobustNet repository [7] and CoTTA repository [40], respectively.

Following CoTTA, we use the same test sequence for both image classification and semantic segmentation experiments. The test batch size is set to 200 for CIFAR, 64 for ImageNet, and for semantic segmentation, 2 for ResNet and 1 for Segformer. Further details on hyperparameters can be found in the Appendix.

Evaluation Metrics Following MECTA [16], we use three evaluation metrics: (i) Online Error (%), which is the average prediction error for each class in each domain. (ii) Mean Online Error (%), which is the average of all online errors across domains in the test sequence. (iii) Cache Size (MB), which indicates the average memory cost of all cached activations during adaptation, ignoring that of weights and gradients because they are linearly related to the number of parameters in the network.

Baselines We introduce the following TTA baselines for comparison with SURGEON. Source indicates the original network without any adaptation. BN-stat [35] only updates the running statistics (i.e., mean $\mu$ and deviation σ) of BN layers during adaptation. TENT [39] updates both the running statistics and the weights of BN layers via entropy minimization loss [12]. Full-Tuning [20] updates the entire network during adaptation. CoTTA [40] is a SOTA TTA method that utilizes weight-averaged and augmentation-averaged predictions, along with a stochastic restoration mechanism, to enhance its adaptation accuracy. EcoTTA [37] is a memory-efficient TTA method that introduces lightweight meta networks to adapt the frozen backbone, but it requires modifications to the original training procedure to warm up these additional blocks. MECTA [16] reduces the activation memory cost of TTA in the batch, channel, and layer, but relies on BN layers to build its updating criterion.

Compatibility We also aim to prove the compatibility of SURGEON, therefore following MECTA [16], we combine two plug-and-play TTA strategies. (i) Certaintybased Sample Selection (CSS) skips the backpropagation for samples with high entropy values in predictions, as these samples are considered to provide unreliable pseudo-labels, which can hurt adaptation performance [30]. (ii) Consistency Regularization (CR) involves adding the discrepancy between model predictions on original test data and augmented test data as regularization to the adaptation loss, aiming to enhance the robustness of pseudo-labels and the performance of unsupervised adaptation [36].

Table 1. Online error (%) and cache size (MB) for TTA on CIFAR-to-CIFAR-C with a batch size of 200. Results are obtained on WideResNet-28 for CIFAR10-C and ResNeXt-29 for CIFAR100-C. The best and second best scores are highlighted. “Original” refers to whether the method requires altering the original training procedure. 

<table><tr><td rowspan="2">Datasets</td><td rowspan="2">Methods</td><td rowspan="2">Original</td><td colspan="14">Time Stamp</td><td>Mean (%) ↓</td><td rowspan="2">Cache (MB) ↓</td></tr><tr><td>Gauss.</td><td>Shot</td><td>Impul.</td><td>Defoc.</td><td>Glass</td><td>Moti.</td><td>Zoom</td><td>Snow</td><td>Frost</td><td>Fog</td><td>Brigh.</td><td>Contr.</td><td>Elast.</td><td>Pixel.</td><td>Jpeg</td></tr><tr><td rowspan="14">CIFAR10-C</td><td>Source [48]</td><td>✕</td><td>72.3</td><td>65.7</td><td>72.9</td><td>46.9</td><td>54.3</td><td>34.8</td><td>42.0</td><td>25.1</td><td>41.3</td><td>26.0</td><td>9.3</td><td>46.7</td><td>26.6</td><td>58.5</td><td>30.3</td><td>43.5</td></tr><tr><td>BN-stat [35]</td><td>✕</td><td>28.3</td><td>26.0</td><td>36.2</td><td>12.6</td><td>34.9</td><td>13.9</td><td>12.0</td><td>17.5</td><td>17.6</td><td>14.9</td><td>8.2</td><td>13.0</td><td>23.5</td><td>19.5</td><td>27.2</td><td>20.4</td></tr><tr><td>Full Tuning [20]</td><td>✕</td><td>26.8</td><td>22.5</td><td>30.9</td><td>12.0</td><td>31.4</td><td>14.0</td><td>12.0</td><td>17.3</td><td>16.5</td><td>15.6</td><td>9.8</td><td>13.3</td><td>21.5</td><td>16.9</td><td>22.5</td><td>18.9</td></tr><tr><td>TENT [39]</td><td>✕</td><td>26.1</td><td>21.3</td><td>29.6</td><td>11.8</td><td>30.6</td><td>13.9</td><td>11.6</td><td>17.1</td><td>16.4</td><td>15.9</td><td>9.5</td><td>13.6</td><td>22.2</td><td>17.3</td><td>21.9</td><td>18.6</td></tr><tr><td>CoTTA [40]</td><td>✕</td><td>24.3</td><td>21.3</td><td>26.6</td><td>11.6</td><td>27.6</td><td>12.2</td><td>10.3</td><td>14.8</td><td>14.1</td><td>12.4</td><td>7.5</td><td>10.6</td><td>18.3</td><td>13.4</td><td>17.3</td><td>16.2</td></tr><tr><td>EcoTTA [37]</td><td>√</td><td>23.5</td><td>18.5</td><td>26.1</td><td>11.4</td><td>29.3</td><td>14.1</td><td>11.5</td><td>15.7</td><td>14.4</td><td>13.6</td><td>8.6</td><td>12.1</td><td>19.4</td><td>15.2</td><td>19.6</td><td>16.8</td></tr><tr><td>MECTA [16]</td><td>✕</td><td>28.5</td><td>20.6</td><td>28.8</td><td>15.4</td><td>32.3</td><td>15.7</td><td>12.4</td><td>19.8</td><td>16.4</td><td>15.9</td><td>8.7</td><td>14.5</td><td>22.0</td><td>19.2</td><td>22.5</td><td>19.5</td></tr><tr><td>+EATA [30]</td><td>√</td><td>27.1</td><td>19.0</td><td>27.3</td><td>15.6</td><td>31.2</td><td>15.7</td><td>12.3</td><td>18.5</td><td>15.9</td><td>15.1</td><td>9.2</td><td>14.0</td><td>20.6</td><td>18.0</td><td>20.6</td><td>18.6</td></tr><tr><td>SURGEON</td><td>✕</td><td>27.0</td><td>22.8</td><td>31.3</td><td>11.8</td><td>31.0</td><td>13.2</td><td>10.9</td><td>16.0</td><td>15.0</td><td>13.8</td><td>8.1</td><td>11.7</td><td>20.6</td><td>16.2</td><td>22.8</td><td>18.1</td></tr><tr><td>+CSS</td><td>✕</td><td>26.9</td><td>22.6</td><td>31.1</td><td>11.8</td><td>30.8</td><td>13.0</td><td>10.9</td><td>16.1</td><td>15.0</td><td>13.9</td><td>8.2</td><td>11.5</td><td>20.3</td><td>16.0</td><td>21.8</td><td>18.0</td></tr><tr><td>+CSS &amp; CR</td><td>✕</td><td>25.7</td><td>21.1</td><td>28.6</td><td>11.9</td><td>28.4</td><td>13.0</td><td>10.8</td><td>15.3</td><td>14.2</td><td>13.6</td><td>8.2</td><td>11.7</td><td>18.2</td><td>14.3</td><td>18.7</td><td>16.9</td></tr><tr><td>SURGEON (BN)</td><td>✕</td><td>26.5</td><td>21.6</td><td>29.9</td><td>12.0</td><td>30.3</td><td>13.5</td><td>10.9</td><td>15.4</td><td>14.5</td><td>13.9</td><td>8.4</td><td>11.7</td><td>21.0</td><td>15.2</td><td>22.2</td><td>17.8</td></tr><tr><td>+ CSS</td><td>✕</td><td>26.0</td><td>21.1</td><td>29.4</td><td>11.9</td><td>30.2</td><td>13.4</td><td>10.9</td><td>15.6</td><td>14.9</td><td>14.5</td><td>8.3</td><td>12.4</td><td>20.8</td><td>15.3</td><td>21.0</td><td>17.7</td></tr><tr><td>+ CSS &amp; CR</td><td>✕</td><td>25.3</td><td>20.0</td><td>27.4</td><td>12.0</td><td>28.0</td><td>13.7</td><td>11.11</td><td>15.4</td><td>14.3</td><td>14.1</td><td>8.2</td><td>11.8</td><td>19.2</td><td>13.5</td><td>18.7</td><td>16.8</td></tr><tr><td rowspan="14">CIFAR100-C</td><td>Source [43]</td><td>✕</td><td>73.0</td><td>68.0</td><td>39.4</td><td>29.4</td><td>54.1</td><td>30.8</td><td>28.8</td><td>39.5</td><td>45.8</td><td>50.3</td><td>29.5</td><td>55.1</td><td>37.2</td><td>74.7</td><td>41.2</td><td>46.5</td></tr><tr><td>BN-stat [35]</td><td>✕</td><td>42.3</td><td>40.9</td><td>43.3</td><td>27.7</td><td>41.9</td><td>29.8</td><td>27.9</td><td>35.1</td><td>35.0</td><td>41.7</td><td>26.3</td><td>30.3</td><td>35.6</td><td>33.4</td><td>41.3</td><td>35.5</td></tr><tr><td>Full Tuning [20]</td><td>✕</td><td>40.7</td><td>36.0</td><td>37.7</td><td>26.8</td><td>38.2</td><td>29.5</td><td>27.6</td><td>34.3</td><td>33.3</td><td>40.2</td><td>28.0</td><td>33.0</td><td>35.3</td><td>32.7</td><td>40.5</td><td>34.3</td></tr><tr><td>TENT [39]</td><td>✕</td><td>41.0</td><td>37.0</td><td>38.4</td><td>25.9</td><td>37.8</td><td>28.1</td><td>25.7</td><td>32.4</td><td>31.8</td><td>37.4</td><td>25.2</td><td>29.2</td><td>32.8</td><td>29.9</td><td>38.9</td><td>32.8</td></tr><tr><td>CoTTA [40]</td><td>✕</td><td>40.1</td><td>37.7</td><td>39.7</td><td>26.9</td><td>38.0</td><td>27.9</td><td>26.4</td><td>32.8</td><td>31.8</td><td>40.3</td><td>24.7</td><td>26.9</td><td>32.5</td><td>28.3</td><td>33.5</td><td>32.5</td></tr><tr><td>EcoTTA [37]</td><td>√</td><td>40.7</td><td>38.1</td><td>41.2</td><td>26.4</td><td>41.1</td><td>28.6</td><td>26.5</td><td>32.8</td><td>31.9</td><td>38.9</td><td>24.8</td><td>28.6</td><td>33.5</td><td>29.7</td><td>37.2</td><td>33.3</td></tr><tr><td>MECTA [16]</td><td>✕</td><td>42.9</td><td>39.4</td><td>41.3</td><td>29.9</td><td>42.2</td><td>29.2</td><td>26.8</td><td>36.2</td><td>33.9</td><td>42.8</td><td>25.0</td><td>32.8</td><td>34.7</td><td>32.7</td><td>38.1</td><td>35.2</td></tr><tr><td>+EATA [30]</td><td>√</td><td>43.4</td><td>39.6</td><td>41.2</td><td>30.4</td><td>43.1</td><td>29.5</td><td>27.9</td><td>37.5</td><td>34.4</td><td>41.6</td><td>25.6</td><td>32.8</td><td>35.2</td><td>33.1</td><td>38.6</td><td>35.5</td></tr><tr><td>SURGEON</td><td>✕</td><td>41.7</td><td>38.4</td><td>39.9</td><td>26.3</td><td>38.5</td><td>28.3</td><td>25.9</td><td>32.4</td><td>31.8</td><td>38.9</td><td>25.1</td><td>29.1</td><td>32.7</td><td>29.9</td><td>37.8</td><td>33.1</td></tr><tr><td>+CSS</td><td>✕</td><td>41.1</td><td>37.2</td><td>38.6</td><td>26.2</td><td>37.2</td><td>28.0</td><td>25.5</td><td>31.5</td><td>30.3</td><td>36.8</td><td>25.0</td><td>27.9</td><td>31.2</td><td>28.0</td><td>35.5</td><td>32.1</td></tr><tr><td>+CSS &amp; CR</td><td>✕</td><td>41.1</td><td>36.9</td><td>38.4</td><td>26.2</td><td>36.6</td><td>27.9</td><td>25.4</td><td>31.2</td><td>30.0</td><td>36.9</td><td>24.9</td><td>27.9</td><td>31.2</td><td>27.7</td><td>35.0</td><td>31.8</td></tr><tr><td>SURGEON (BN)</td><td>✕</td><td>41.6</td><td>38.1</td><td>40.1</td><td>26.3</td><td>38.6</td><td>28.0</td><td>25.6</td><td>32.5</td><td>31.6</td><td>37.4</td><td>24.5</td><td>28.0</td><td>32.3</td><td>29.3</td><td>38.2</td><td>32.8</td></tr><tr><td>+ CSS</td><td>✕</td><td>40.4</td><td>35.8</td><td>38.3</td><td>26.2</td><td>37.1</td><td>27.9</td><td>25.2</td><td>31.8</td><td>30.7</td><td>35.1</td><td>25.0</td><td>27.3</td><td>31.5</td><td>28.7</td><td>37.3</td><td>31.8</td></tr><tr><td>+ CSS &amp; CR</td><td>✕</td><td>40.3</td><td>35.6</td><td>38.1</td><td>26.4</td><td>36.7</td><td>28.1</td><td>25.5</td><td>31.2</td><td>30.0</td><td>35.6</td><td>24.8</td><td>27.2</td><td>31.3</td><td>28.2</td><td>36.1</td><td>31.7</td></tr></table>

Table 2. Online error (%) and cache size (MB) for TTA on Cityscapes-to-ACDC. Results are obtained on ACDC using DeeplabV3+ and Segformer-B5. The best and second best scores are highlighted. 

<table><tr><td rowspan="3">Architectures</td><td rowspan="3">Methods</td><td colspan="16">Time Stamp→</td><td rowspan="3">Mean (%) ↓</td><td rowspan="3">Cache (MB) ↓</td></tr><tr><td colspan="4">1</td><td colspan="4">4</td><td colspan="4">7</td><td colspan="4">10</td></tr><tr><td>Fog</td><td>Night</td><td>Rain</td><td>Snow</td><td>Fog</td><td>Night</td><td>Rain</td><td>Snow</td><td>Fog</td><td>Night</td><td>Rain</td><td>Snow</td><td>Fog</td><td>Night</td><td>Rain</td><td>Snow</td></tr><tr><td rowspan="8">DeeplabV3+</td><td>Source [5]</td><td>38.6</td><td>82.4</td><td>47.3</td><td>53.9</td><td>38.6</td><td>82.4</td><td>47.3</td><td>53.9</td><td>38.6</td><td>82.4</td><td>47.3</td><td>53.9</td><td>38.6</td><td>82.4</td><td>47.3</td><td>53.9</td><td>55.6</td><td>301</td></tr><tr><td>BN-stat [35]</td><td>57.5</td><td>73.1</td><td>55.2</td><td>57.8</td><td>57.5</td><td>73.1</td><td>55.2</td><td>57.8</td><td>57.5</td><td>73.1</td><td>55.2</td><td>57.8</td><td>57.5</td><td>73.1</td><td>55.2</td><td>57.8</td><td>60.9</td><td>301</td></tr><tr><td>Full Tuning [20]</td><td>57.0</td><td>72.5</td><td>53.3</td><td>55.5</td><td>52.8</td><td>72.1</td><td>50.8</td><td>54.4</td><td>54.7</td><td>74.5</td><td>52.8</td><td>56.9</td><td>57.6</td><td>77.0</td><td>55.7</td><td>59.6</td><td>59.4</td><td>9974</td></tr><tr><td>TENT [39]</td><td>57.4</td><td>73.0</td><td>54.8</td><td>57.3</td><td>55.7</td><td>72.2</td><td>53.1</td><td>55.8</td><td>54.6</td><td>71.7</td><td>51.9</td><td>54.8</td><td>53.8</td><td>71.3</td><td>51.2</td><td>54.2</td><td>58.9</td><td>4646</td></tr><tr><td>CoTTA [40]</td><td>38.7</td><td>84.0</td><td>47.3</td><td>53.8</td><td>38.8</td><td>84.1</td><td>47.3</td><td>53.9</td><td>38.8</td><td>84.1</td><td>47.3</td><td>53.9</td><td>38.8</td><td>84.1</td><td>47.3</td><td>53.9</td><td>56.0</td><td>9974</td></tr><tr><td>MECTA [16]</td><td>56.9</td><td>75.2</td><td>52.0</td><td>55.2</td><td>54.5</td><td>74.1</td><td>50.3</td><td>53.8</td><td>53.1</td><td>74.0</td><td>50.1</td><td>53.4</td><td>53.1</td><td>74.0</td><td>50.1</td><td>53.4</td><td>58.2</td><td>1354</td></tr><tr><td>SURGEON</td><td>51.6</td><td>72.5</td><td>51.8</td><td>54.0</td><td>48.7</td><td>71.7</td><td>48.1</td><td>50.9</td><td>47.1</td><td>71.7</td><td>46.9</td><td>49.4</td><td>46.7</td><td>72.0</td><td>46.6</td><td>49.0</td><td>54.7</td><td>1403</td></tr><tr><td>SURGEON (BN)</td><td>51.7</td><td>72.4</td><td>51.9</td><td>54.0</td><td>47.7</td><td>70.9</td><td>48.2</td><td>50.0</td><td>46.4</td><td>70.8</td><td>47.2</td><td>49.2</td><td>45.6</td><td>71.1</td><td>47.5</td><td>49.2</td><td>54.4</td><td>1300</td></tr><tr><td rowspan="4">Segformer-B5</td><td>Source [42]</td><td>30.9</td><td>59.7</td><td>40.3</td><td>42.2</td><td>30.9</td><td>59.7</td><td>40.3</td><td>42.2</td><td>30.9</td><td>59.7</td><td>40.3</td><td>42.2</td><td>30.9</td><td>59.7</td><td>40.3</td><td>42.2</td><td>43.3</td><td>380</td></tr><tr><td>CoTTA [40]</td><td>29.1</td><td>58.8</td><td>37.6</td><td>40.3</td><td>29.1</td><td>59.0</td><td>37.3</td><td>40.3</td><td>29.1</td><td>59.0</td><td>37.2</td><td>40.3</td><td>29.2</td><td>59.0</td><td>37.2</td><td>40.3</td><td>41.4</td><td>2793</td></tr><tr><td>MECTA [16]</td><td>30.9</td><td>59.8</td><td>40.0</td><td>42.6</td><td>33.1</td><td>63.1</td><td>41.1</td><td>45.7</td><td>35.2</td><td>66.5</td><td>46.0</td><td>48.2</td><td>37.3</td><td>69.4</td><td>47.1</td><td>51.0</td><td>47.2</td><td>380</td></tr><tr><td>SURGEON</td><td>30.9</td><td>59.7</td><td>40.0</td><td>42.2</td><td>30.4</td><td>59.1</td><td>39.1</td><td>41.7</td><td>30.0</td><td>58.7</td><td>38.3</td><td>41.3</td><td>29.7</td><td>58.3</td><td>37.9</td><td>41.0</td><td>42.2</td><td>380</td></tr></table>

# 5.2. Evaluation Comparison

SURGEON on CIFAR-C As shown in Table 1, Source and BN-stat avoid storing activations for backpropagation, so their cache size reflects forward propagation cost, tied to the most memory-intensive layer in the network [16]. However, these two baselines also exhibit limited accuracy. Although Full-Tuning and CoTTA achieve relatively higher accuracy improvements, they also consume the highest memory for storing activations of all layers for backpropagation. TENT reduces memory usage by only updating BN layers, but it still occupies a significant amount of memory. EcoTTA efficiently reduces memory cost during adaptation while preserving comparable accuracy via introducing meta networks. However, it necessitates modifications to the original training process, limiting its applicability to FTTA. MECTA achieves a more significant reduction in activation memory usage, but this comes at the cost of diminished accuracy gains. For a fair comparison, we create two versions of SURGEON: one that updates all layers of the network and another that only updates BN layers as SURGEON (BN). Both versions exhibit outstanding performance in memory reduction and accuracy.

![](images/442afc93e97bde4b8b341148897ae7fcc624c9256280292983b7f1baa568be4e.jpg)



(a) WideResNet-28

![](images/ab16bca3384b74382bdaa113bb9083039adcf975a423c9b240402cabcf21069c.jpg)



(b) ResNeXt-29

![](images/77efa655c7fdacc11af098ae406b51837cf56df60192c9241182371bedbb0be6.jpg)



(c) DeeplabV3+   
Figure 3. Mean online error (%) under different global static pruning ratios for TTA on three convolutional networks. The pruning ratio of SURGEON refers to a global static pruning ratio that yields an equivalent cache size.

Table 3. Mean online error (%) and cache size (MB) for TTA with different layer importance metrics. “w/o $G + M ^ { \prime \prime }$ is the TTA method using Full Tuning and “Ours” is SURGEON with the original design of I (Eq. (6)). 

<table><tr><td rowspan="2">Strategies</td><td colspan="2">WideResNet-28</td><td colspan="2">ResNeXt-29</td><td colspan="2">DeeplabV3+</td></tr><tr><td>Mean (%) ↓</td><td>Cache (MB) ↓</td><td>Mean (%) ↓</td><td>Cache (MB) ↓</td><td>Mean (%) ↓</td><td>Cache (MB) ↓</td></tr><tr><td>w/o G + M</td><td>18.9</td><td>3697</td><td>34.3</td><td>5403</td><td>59.4</td><td>9974</td></tr><tr><td>w/o G</td><td>20.3 (1.4 ↑)</td><td>1568 (57.6% ↓)</td><td>34.0 (0.3 ↓)</td><td>2396 (55.7% ↓)</td><td>56.5 (2.9 ↓)</td><td>2385 (76.1% ↓)</td></tr><tr><td>w/o M</td><td>17.8 (1.1 ↓)</td><td>704 (81.0% ↓)</td><td>32.8 (1.5 ↓)</td><td>1108 (79.5% ↓)</td><td>54.8 (4.6 ↓)</td><td>1596 (84.0% ↓)</td></tr><tr><td>Ours</td><td>18.1 (0.8 ↓)</td><td>325 (91.2% ↓)</td><td>33.1 (1.2 ↓)</td><td>820 (84.8% ↓)</td><td>54.7 (4.7 ↓)</td><td>1403 (85.9% ↓)</td></tr></table>

Table 4. Mean online error (%), cache size (MB) and GFLOPs (per sample) for TTA on ImageNet-to-ImageNet-C. Results are obtained on ResNet-50 (AugMix). “Original” refers to whether the method requires altering the original training procedure. 

<table><tr><td>Methods</td><td>Original</td><td>Mean (%) ↓</td><td>Cache (MB) ↓</td><td>GFLOPs ↓</td></tr><tr><td>Source [14]</td><td>✗</td><td>74.4</td><td>196</td><td>4.1</td></tr><tr><td>BN-stat [35]</td><td>✗</td><td>60.5</td><td>196</td><td>4.1</td></tr><tr><td>TENT [39]</td><td>✗</td><td>55.2(1.2)</td><td>2714</td><td>8.2</td></tr><tr><td>CoTTA [40]</td><td>✗</td><td>54.4 (3.8)</td><td>5317</td><td>103.7</td></tr><tr><td>EcoTTA (K=5) [37]</td><td>√</td><td>54.2 (2.5)</td><td>1503</td><td>10.1</td></tr><tr><td>NECTA [16]</td><td>✗</td><td>70.1 (10.5)</td><td>651</td><td>8.2</td></tr><tr><td>+ EATA [30]</td><td>√</td><td>64.4 (5.7)</td><td>648</td><td>8.5</td></tr><tr><td>SURGEON</td><td>✗</td><td>55.5 (2.6)</td><td>1125</td><td>13.4</td></tr><tr><td>+ CSS</td><td>✗</td><td>55.3 (3.9)</td><td>1084</td><td>13.4</td></tr><tr><td>+ CSS &amp; CR</td><td>✗</td><td>54.2 (2.9)</td><td>2201</td><td>18.0</td></tr><tr><td>SURGEON (BN)</td><td>✗</td><td>55.2 (1.4)</td><td>912</td><td>9.7</td></tr><tr><td>+ CSS</td><td>✗</td><td>54.6 (2.0)</td><td>907</td><td>9.8</td></tr><tr><td>+ CSS &amp; CR</td><td>✗</td><td>53.9 (1.8)</td><td>1834</td><td>14.2</td></tr></table>

SURGEON on ImageNet-C Following CoTTA [40], we average and report the results over ten diverse corruption sequences for the ImageNet-to-ImageNet-C experiments. As shown in Table 4, while MECTA achieves advantages in cache reduction and computational efficiency, it offers

![](images/04445e2db9c70f4a19adbd272f05f77fe5b48bfe557a193abd91d4776a96f6c9.jpg)



Figure 4. Visualization of normalized importance metrics. Experiments are implemented using WideResNet-28 on CIFAR10-C.

limited accuracy improvement. Both EcoTTA and SUR-GEON strike a great balance between accuracy and overhead. However, our method can be directly applied to FTTA without altering the model’s original training procedure.

SURGEON on ACDC The evaluation of semantic segmentation is depicted in Table 2. Interestingly, all the chosen TTA baselines fail to surpass the accuracy of Source on DeeplabV3+. This could potentially be attributed to the intricate nature of pixel-level prediction tasks and inaccurate pseudo-labels for adaptation, which may result in substantial error accumulation during TTA [19]. For Segformer-B5, CoTTA achieves the highest accuracy but incurs a substantial activation memory cost. MECTA fails to improve accuracy during adaptation because it is designed based on

Table 5. Performance on Jetson Xavier NX. The experiments are conducted using ResNeXt-29 on CIFAR-100-C. GFLOPs and Latency refer to the number of 109 floating-point operations and the time required to process a batch during FTTA. 

<table><tr><td>Methods</td><td>Mean (%) ↓</td><td>Cache (MB) ↓</td><td>GFLOPs ↓</td><td>Latency (ms) ↓</td></tr><tr><td>BN-stat [35]</td><td>44.0</td><td>8.0</td><td>8.4</td><td>25.4</td></tr><tr><td>TENT [39]</td><td>41.9</td><td>109.0</td><td>16.3</td><td>65.6</td></tr><tr><td>CoTTA [40]</td><td>37.5</td><td>216.0</td><td>259.2</td><td>522.6</td></tr><tr><td>EcoTTA [37]</td><td>39.6</td><td>42.0</td><td>19.1</td><td>80.4</td></tr><tr><td>MECTA [16]</td><td>38.2</td><td>22.8</td><td>16.4</td><td>66.5</td></tr><tr><td>GC [6]</td><td>45.2</td><td>62.1</td><td>29.3</td><td>118.2</td></tr><tr><td>SURGEON</td><td>37.8</td><td>22.4</td><td>28.3</td><td>117.4</td></tr><tr><td>SURGEON (BN)</td><td>37.9</td><td>19.9</td><td>18.5</td><td>78.8</td></tr></table>

BN layers, of which Segformer has only one, highlighting its limitations when applied to transformer-based architectures. Notably, the cache size reported for MECTA and SURGEON is the same as Source due to their forward propagation’s activation memory usage exceeding that of backpropagation.

Summary The above evaluation demonstrates that our method, SURGEON, effectively balances memory cost and accuracy for FTTA without relying on specific architectures or modifications to the original training procedure. SURGEON achieves a significant improvement in accuracy, as the layer-specific dynamic activation sparsity encourages adaptation in layers with higher accuracy contribution while suppressing unnecessary updates in less critical layers, thereby reducing error accumulation [20].

# 5.3. Empirical Study

Effectiveness of Dynamic Activation Sparsity To demonstrate the effectiveness of dynamic activation sparsity, we compare SURGEON with the method utilizing global static sparsity [4, 17]. Figure 3 presents TTA accuracy under different global pruning ratios and reports pruning ratios of SURGEON using the value of the global pruning ratio that produces equal activation memory cost. The results demonstrate that SURGEON achieves higher accuracy under the same cache size compared to static activation sparsity, as layer-wise dynamic sparsity captures the varying learning abilities of different layers to acquire knowledge and their different contribution to accuracy gains in a data-sensitive manner.

Effectiveness of Metric Components To evaluate the impact of G (Eq.(4)) and M (Eq.(5)) as components of I on the overall performance of SURGEON, we record the accuracy and cache size by gradually removing each of the two metrics, as shown in Table 3. From the results, it is evident that the combination of G and M for determining layer-specific sparsity ratios achieves a state-of-the-art balance between memory cost and accuracy during FTTA. To more intuitively observe the impact of metric components, we visualize the normalized importance metrics using WideResNet-28 on CIFAR10-C, as shown in Figure 4. We can see that the first few layers within each block exhibit higher gradient importance values, indicating their greater contribution to accuracy. Additionally, The activation memory importance of deeper layers is slightly higher than that of shallow layers, as their activation size is typically smaller (see Eq. (5)) due to downsampling. Finally, the metric I (i.e., “Ours”) takes into account both the accuracy contribution and activation memory efficiency for informed decisions about pruning activations.

Analysis of Real-world Evaluation We also evaluate the methods by deploying them on Jetson XAVIER NX1. The results are obtained using ResNeXt-29 on CIFAR-100-C with a test batch size of 8, as shown in Table 5. Besides, in both the baselines (except MECTA) and our method, we calibrate the source and target statistics for BN layers to mitigate unreliable statistic estimation under small batch sizes [35]. SURGEON randomly selects a sample for layer importance calculation (§ 4.2). From the results, we observe that, our method achieves comparable accuracy and optimal cache reduction compared to the baselines, while maintaining acceptable computational costs and latency. Meanwhile, we incorporate gradient checkpointing (GC) [6] for comparison. Following the setup [16], GC treats each residual block as the minimal unit. Notably, GC does not alter activations for gradient calculation but temporarily discards them. In constrast, our dynamic activation sparsity reduces activation memory and improves accuracy by precisely regulating both activation memory consumption and weight gradients across layers during FTTA.

# 6. Conclusion

This paper presents SURGEON, a method aimed at reducing memory cost in FTTA while maintaining comparable accuracy, independent of specific architectures or alterations to the original training process. Considering interlayer differences, SURGEON leverages a novel dynamic activation sparsity strategy that prunes activations at layerspecific and adaptive ratios in a data-sensitive manner, precisely regulating both activation memory consumption and weight gradients across different layers during adaptation. Experimental results show that SURGEON achieves SOTA balance between accuracy and memory across various datasets, architectures and tasks. This research is expected to promote the robust deployment of deep models on resource-constrained devices in changing environments.

Acknowledgements. This work was supported by the National Science Fund for Distinguished Young Scholars (No.62025205), the National Natural Science Foundation of China (No.62472354, No.62302259, No.62432008), and Guangzhou-HKUST(GZ) Joint Funding Program (Grant No.2023A03J0008), Education Bureau of Guangzhou Municipality.

# References

[1] Andrea Bragagnolo, Enzo Tartaglione, and Marco Grangetto. To update or not to update? neurons at equilibrium in deep models. Advances in neural information processing systems, 35:22149–22160, 2022. 3   
[2] Han Cai, Chuang Gan, Ligeng Zhu, and Song Han. Tinytl: Reduce memory, not parameters for efficient on-device learning. Advances in Neural Information Processing Systems, 33:11285–11297, 2020. 2   
[3] Dian Chen, Dequan Wang, Trevor Darrell, and Sayna Ebrahimi. Contrastive test-time adaptation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 295–305, 2022. 1, 2, 3   
[4] Joya Chen, Kai Xu, Yuhui Wang, Yifei Cheng, and Angela Yao. Dropit: Dropping intermediate tensors for memoryefficient dnn training. In 2023 International Conference on Learning Representations, 2023. 2, 3, 8   
[5] Liang-Chieh Chen, Yukun Zhu, George Papandreou, Florian Schroff, and Hartwig Adam. Encoder-decoder with atrous separable convolution for semantic image segmentation. In Proceedings of the European conference on computer vision (ECCV), pages 801–818, 2018. 5, 6   
[6] Tianqi Chen, Bing Xu, Chiyuan Zhang, and Carlos Guestrin. Training deep nets with sublinear memory cost. arXiv preprint arXiv:1604.06174, 2016. 2, 8   
[7] Sungha Choi, Sanghun Jung, Huiwon Yun, Joanne T Kim, Seungryong Kim, and Jaegul Choo. Robustnet: Improving domain generalization in urban-scene segmentation via instance selective whitening. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 11580–11590, 2021. 5   
[8] Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler, Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele. The cityscapes dataset for semantic urban scene understanding. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 3213–3223, 2016. 5   
[9] Francesco Croce, Maksym Andriushchenko, Vikash Sehwag, Edoardo Debenedetti, Nicolas Flammarion, Mung Chiang, Prateek Mittal, and Matthias Hein. Robustbench: a standardized adversarial robustness benchmark. NeurIPS 2021 Datasets and Benchmarks Track, 2021. 2, 5   
[10] Mario Dobler, Robert A Marsden, and Bin Yang. Robust ¨ mean teacher for continual and gradual test-time adaptation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 7704–7714, 2023. 1   
[11] Utku Evci, Trevor Gale, Jacob Menick, Pablo Samuel Castro, and Erich Elsen. Rigging the lottery: Making all tickets

winners. In International conference on machine learning, pages 2943–2952. PMLR, 2020. 3   
[12] Yves Grandvalet and Yoshua Bengio. Semi-supervised learning by entropy minimization. Advances in neural information processing systems, 17, 2004. 3, 5   
[13] Junxian He, Chunting Zhou, Xuezhe Ma, Taylor Berg-Kirkpatrick, and Graham Neubig. Towards a unified view of parameter-efficient transfer learning. In 2022 International Conference on Learning Representations, 2022. 2   
[14] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 770–778, 2016. 5, 7   
[15] Dan Hendrycks and Thomas Dietterich. Benchmarking neural network robustness to common corruptions and perturbations. In 2019 International Conference on Learning Representations, 2019. 5   
[16] Junyuan Hong, Lingjuan Lyu, Jiayu Zhou, and Michael Spranger. Mecta: Memory-economic continual test-time model adaptation. In 2023 International Conference on Learning Representations, 2023. 2, 5, 6, 7, 8   
[17] Ziyu Jiang, Xuxi Chen, Xueqin Huang, Xianzhi Du, Denny Zhou, and Zhangyang Wang. Back razor: Memoryefficient transfer learning by self-sparsified backpropagation. Advances in Neural Information Processing Systems, 35: 29248–29261, 2022. 2, 3, 5, 8   
[18] Muhammed Kocabas, Chun-Hao P Huang, Joachim Tesch, Lea Muller, Otmar Hilliges, and Michael J Black. Spec: ¨ Seeing people in the wild with an estimated camera. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 11035–11045, 2021. 1   
[19] Jungsoo Lee, Debasmit Das, Jaegul Choo, and Sungha Choi. Towards open-set test-time adaptation utilizing the wisdom of crowds in entropy minimization. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 16380–16389, 2023. 7   
[20] Yoonho Lee, Annie S Chen, Fahim Tajwar, Ananya Kumar, Huaxiu Yao, Percy Liang, and Chelsea Finn. Surgical finetuning improves adaptation to distribution shifts. In 2023 International Conference on Learning Representations, 2023. 3, 5, 6, 8   
[21] Sheng Li, Geng Yuan, Yue Dai, Youtao Zhang, Yanzhi Wang, and Xulong Tang. Smartfrz: An efficient training framework using attention-based layer freezing. In 2023 International Conference on Learning Representations, 2023. 2, 3   
[22] Dongze Lian, Daquan Zhou, Jiashi Feng, and Xinchao Wang. Scaling & shifting your features: A new baseline for efficient model tuning. Advances in Neural Information Processing Systems, 35:109–123, 2022. 2   
[23] Jian Liang, Ran He, and Tieniu Tan. A comprehensive survey on test-time adaptation under distribution shifts. International Journal of Computer Vision, pages 1–34, 2024. 1   
[24] Ji Lin, Ligeng Zhu, Wei-Ming Chen, Wei-Chen Wang, Chuang Gan, and Song Han. On-device training under 256kb memory. Advances in Neural Information Processing Systems, 35:22941–22954, 2022. 3

[25] Chenxi Liu, Lixu Wang, Lingjuan Lyu, Chen Sun, Xiao Wang, and Qi Zhu. Deja vu: Continual model generalization for unseen domains. In 2023 International Conference on Learning Representations, 2023. 2   
[26] Sicong Liu, Bin Guo, Ke Ma, Zhiwen Yu, and Junzhao Du. Adaspring: Context-adaptive and runtime-evolutionary deep model compression for mobile applications. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, 5(1):1–22, 2021. 1   
[27] Sicong Liu, Bin Guo, Cheng Fang, Ziqi Wang, Shiyan Luo, Zimu Zhou, and Zhiwen Yu. Enabling resource-efficient aiot system with cross-level optimization: A survey. IEEE Communications Surveys & Tutorials, 2023. 2   
[28] Yuejiang Liu, Parth Kothari, Bastien Van Delft, Baptiste Bellot-Gurlet, Taylor Mordan, and Alexandre Alahi. Ttt++: When does self-supervised test-time training fail or thrive? Advances in Neural Information Processing Systems, 34: 21808–21820, 2021. 1, 2   
[29] Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, and Baining Guo. Swin transformer: Hierarchical vision transformer using shifted windows. In Proceedings of the IEEE/CVF international conference on computer vision, pages 10012–10022, 2021. 2   
[30] Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Yaofo Chen, Shijian Zheng, Peilin Zhao, and Mingkui Tan. Efficient testtime model adaptation without forgetting. In 2022 International conference on machine learning, pages 16888–16905. PMLR, 2022. 1, 3, 5, 6, 7   
[31] Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Zhiquan Wen, Yaofo Chen, Peilin Zhao, and Mingkui Tan. Towards stable test-time adaptation in dynamic wild world. In 2023 International Conference on Learning Representations, 2023. 1, 2, 3   
[32] Shuaicheng Niu, Chunyan Miao, Guohao Chen, Pengcheng Wu, and Peilin Zhao. Test-time model adaptation with only forward passes. In Proceedings of the 41st International Conference on Machine Learning, pages 38298– 38315, 2024. 2   
[33] Sinno Jialin Pan and Qiang Yang. A survey on transfer learning. IEEE Transactions on knowledge and data engineering, 22(10):1345–1359, 2009. 1   
[34] Christos Sakaridis, Dengxin Dai, and Luc Van Gool. Acdc: The adverse conditions dataset with correspondences for semantic driving scene understanding. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 10765–10775, 2021. 1, 5   
[35] Steffen Schneider, Evgenia Rusak, Luisa Eck, Oliver Bringmann, Wieland Brendel, and Matthias Bethge. Improving robustness against common corruptions by covariate shift adaptation. Advances in neural information processing systems, 33:11539–11551, 2020. 5, 6, 7, 8   
[36] Kihyuk Sohn, David Berthelot, Nicholas Carlini, Zizhao Zhang, Han Zhang, Colin A Raffel, Ekin Dogus Cubuk, Alexey Kurakin, and Chun-Liang Li. Fixmatch: Simplifying semi-supervised learning with consistency and confidence. Advances in neural information processing systems, 33:596– 608, 2020. 6

[37] Junha Song, Jungsoo Lee, In So Kweon, and Sungha Choi. Ecotta: Memory-efficient continual test-time adaptation via self-distilled regularization. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 11920–11929, 2023. 2, 5, 6, 7, 8   
[38] Yu Sun, Xiaolong Wang, Zhuang Liu, John Miller, Alexei Efros, and Moritz Hardt. Test-time training with selfsupervision for generalization under distribution shifts. In International conference on machine learning, pages 9229– 9248. PMLR, 2020. 2   
[39] Dequan Wang, Evan Shelhamer, Shaoteng Liu, Bruno Olshausen, and Trevor Darrell. Tent: Fully test-time adaptation by entropy minimization. In 2021 International Conference on Learning Representations, 2021. 1, 2, 3, 5, 6, 7, 8   
[40] Qin Wang, Olga Fink, Luc Van Gool, and Dengxin Dai. Continual test-time domain adaptation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 7201–7211, 2022. 1, 5, 6, 7, 8   
[41] Qipeng Wang, Mengwei Xu, Chao Jin, Xinran Dong, Jinliang Yuan, Xin Jin, Gang Huang, Yunxin Liu, and Xuanzhe Liu. Melon: Breaking the memory wall for resource-efficient on-device machine learning. In Proceedings of the 20th Annual International Conference on Mobile Systems, Applications and Services, pages 450–463, 2022. 2   
[42] Enze Xie, Wenhai Wang, Zhiding Yu, Anima Anandkumar, Jose M Alvarez, and Ping Luo. Segformer: Simple and efficient design for semantic segmentation with transformers. Advances in neural information processing systems, 34: 12077–12090, 2021. 5, 6   
[43] Saining Xie, Ross Girshick, Piotr Dollar, Zhuowen Tu, and ´ Kaiming He. Aggregated residual transformations for deep neural networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 1492–1500, 2017. 5, 6   
[44] Li Yang, Adnan Siraj Rakin, and Deliang Fan. Rep-net: Efficient on-device learning via feature reprogramming. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 12277–12286, 2022. 2   
[45] Zheng Yang, Xu Wang, Jiahang Wu, Yi Zhao, Qiang Ma, Xin Miao, Li Zhang, and Zimu Zhou. Edgeduet: Tiling small object detection for edge assisted autonomous mobile vision. IEEE/ACM Transactions on Networking, 2022. 1   
[46] Geng Yuan, Yanyu Li, Sheng Li, Zhenglun Kong, Sergey Tulyakov, Xulong Tang, Yanzhi Wang, and Jian Ren. Layer freezing & data sieving: missing pieces of a generic framework for sparse training. Advances in Neural Information Processing Systems, 35:19061–19074, 2022. 2, 3   
[47] Longhui Yuan, Binhui Xie, and Shuang Li. Robust testtime adaptation in dynamic scenarios. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 15922–15932, 2023. 1, 2, 3   
[48] Sergey Zagoruyko and Nikos Komodakis. Wide residual networks. In Proceedings of the British Machine Vision Conference 2016, 2016. 5, 6   
[49] Bowen Zhao, Chen Chen, and Shu-Tao Xia. Delta: degradation-free fully test-time adaptation. In 2023 International Conference on Learning Representations, 2023. 1, 2