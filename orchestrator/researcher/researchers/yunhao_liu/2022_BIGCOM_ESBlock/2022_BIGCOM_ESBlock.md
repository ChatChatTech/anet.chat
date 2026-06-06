# Expansion-Squeeze-Block: Linear Over-parameterization with Shortcut Connections to Train Compact Convolutional Networks

Linzhuo Yang

Computer Science Department

University of Science and Technology of China

Hefei, China

ustcylz@mail.ustc.edu.cn

Lan Zhang

Computer Science Department

University of Science and Technology of China

Hefei, China

zhanglan@ustc.edu.cn

Abstract—We propose a new structure called Expansion-Squeeze-Block by leveraging over-parameterization to train given compact neural networks. The structure expands the width of convolutional layers and adds shortcut connections for better performance without adding any nonlinearity. The expanded networks can be contracted back to the original format algebraically at inference time without loss of information. In addition, we introduce a new initialization method utilizing the weights of the pretrained original networks, which can further improve the accuracy. We evaluate our methods on CIFAR-100 and Tiny-ImageNet datasets to show their effectiveness. As evidenced by our experiments, Expansion-Squeeze-Block outperforms the baselines in most cases with average 0.81% improvements and 1.15% combined with our initialization method on CIFAR-100 and Tiny-ImageNet datasets. We also demonstrate the effectiveness of the partial expansion strategy by choosing the layers of the highest importance in VGG11-BN 0.5× and ResNet20. We can save on average 58.82% #MACs and 38.82% #Params than expanding all layers.

Index Terms—Deep Learning, CNN, Convolution, Overparameterization

# I. INTRODUCTION

The convolutional layer is a basic and critical module to build neural networks designed for computer vision tasks. No matter plain models like VGG [1], or complicated models with multi-branch structures such as Inception [2], [3], ResNet [4] and DenseNet [5], convolutional layer plays an important role to provide strong ability to capture the features of images. A convolutional layer could have many basic parameters, including input channels $C _ { \mathrm { i n } } .$ , output channels $C _ { \mathrm { o u t } }$ , kernel size k and others [6]. The channels of a convolutional layer, namely $C _ { \mathrm { i n } }$ and $C _ { \mathrm { o u t } }$ , have great influence on model’s performance. Usually, more channels could bring an increase to the model’s accuracy: WideResNet [7] gets a comparable result to ResNet with a shallower model by expanding the width of convolutional layers. These deep and wide networks are usually heavily over-parameterized, decreasing inference speed and occupying much more GPU memory resource.

Prune is an effective approach to reduce the complexity of models and achieve better time performance. Layer-prune [8] uses imprinting, which comes from the low-shot learning [9] method, to drop unnecessary layers, but can not bring many improvements to the accuracy of neural networks. Layer-Folding [10] removes some ReLU modules and fuse sequential convolutional layers to reduce the depth of models for decreasing the inference latency. Though larger fused kernels are beneficial for improving the accuracy of neural networks, the inference speed would be slower because 3 × 3 convolutional kernels are highly optimized.

Another way to increase the execution speed and optimize the memory occupation of GPU at inference time, is designing light-weight models by applying new operations to reduce the FLOPs such as depth-wise convolution in Xception [11] and MobileNet [12] [13], channel shuffle in ShuffleNet [14] [15], shift operation in ShiftNet [16], etc. The success of these lightweight models shows that compact neural networks are sufficient for many tasks. Unfortunately, it is hard to train a compact network from scratch, and as a consequence, designing strategies to train a given compact network becomes an important research topic.

ExpandNets [17] proposed expansion-and-extract block (CL-Expansion) to train compact neural networks with channel-expanding convolutional layers from scratch and extract back to original width at inference time, by replacing the 3×3 convolutional layers with consecutive 1×1-3×3-1×1 convolutional modules. The channels of the middle 3×3 convolutional layer can be changed by adjusting the expansion rate e to make the ability of models stronger. Though large amounts of parameters are added, the linearity of convolutional layers makes it possible to transform the sequential layers into one single 3×3 convolutional layer without any information loss. The contracted model has the same accuracy as the expanded networks while remains the same latency as the original neural networks before expansion. This over-parameterization approach, which can accelerate convergence speed and contribute to accuracy performance, is an alternative approach complementary to knowledge transfer. However, the CL-Expansion is a plain structure without shortcut connections. Thus we propose a new modified version of CL-Expansion called Expansion-Squeeze-Block (ES-Block), which adds a shortcut connection to utilize the benefits of the multi-branch architecture. We also move the padding parameter back to 3×3 convolutional layer to make the parameter settings more usual. Besides, because of the difficulty of training compact networks, the authors also introduced a method by initializing CL-Expansion with parameters from its nonlinear counterpart, which adds nonlinear activation functions between linear parts and is trained from scratch, to improve accuracy. However, the nonlinear counterpart is not guaranteed to be better than the linear one. And the models initialized by the weights of their nonlinear counterparts are also not guaranteed to have better accuracy than that of baselines. Furthermore, considering that the expanded layers have much more parameters, it is much more time-consuming to train a complete epoch compared with the original one when the model size is slightly larger, shown by Table I. Thus we propose a new initialization method by using the weights from the pretrained original neural networks, which is easier to train, to shorten the time for training.

We have the following summarized contributions:

• We propose Expansion-Squeeze-Block, a modified version of CL-Expansion, which adds shortcut connections. Moreover, we move the padding parameter to 3×3 convolutional layer, making parameter settings more similar to usual ones.   
• We introduce a new initialization method by utilizing the weights of convolutional layers in pretrained original neural networks to initialize the parameters of ES-Block, which saves much time without training the nonlinear counterparts of the expanded networks and bring more contributions to model performance.   
• We compute the norm of the pretrained models’ weights to evaluate the importance of each layer for selecting the most important layers to expand. This saves much time for training expanded networks.   
• We show the effectiveness of the proposed ES-Block structure and initialization method on CIFAR-100 [18] and Tiny-ImageNet datasets [19].

TABLE I MODEL COMPLEXITY OF ORIGINAL MODEL AND CL-EXPANSION ON CIFAR-100 

<table><tr><td rowspan="2">Model</td><td colspan="2">#MACs</td><td colspan="2">#Params</td></tr><tr><td>Baseline</td><td>CL*</td><td>Baseline</td><td>CL*</td></tr><tr><td>VGG11-BN 0.5×**</td><td>38.81M</td><td>663.69M</td><td>2.33M</td><td>39.30M</td></tr><tr><td>ResNet20</td><td>41.23M</td><td>693.197M</td><td>278.32K</td><td>4.81M</td></tr><tr><td>ShuffleNetV2 0.5×</td><td>11.52M</td><td>33.69M</td><td>444.29K</td><td>604.05K</td></tr><tr><td>MobileNet</td><td>47.271M</td><td>88.186M</td><td>3.309M</td><td>4.036M</td></tr><tr><td>MobileNetV2</td><td>94.721M</td><td>207.429M</td><td>2.412M</td><td>3.450M</td></tr></table>

∗CL is CL-Expansion strategy in [17].

∗∗VGG11-BN is a modified version which removes half of the channels.

# II. RELATED WORK

# A. Increasingly Complicated Models

Starting from AlexNet [20], Convolutional Neural Networks (CNN) have been a mainstream architecture to deal with computer vision tasks, showing the significance of convolutional layers. However, CNN have been increasingly complicated in the last few years, from shallow, thin, single-path to deep, wide, multi-path architectures.

From VGG [1], which deepens the depth of neural networks and raises the accuracy of ImageNet classification to above 70%, it is a common choice to design deep neural networks for better performance.

On the other hand, GoogLeNet [21] and Inception models [2] [3], adopted multi-branch architectures, ResNet [4] proposed a simple two-branch structure, i.e. skip connection, and DenseNet [5] used a more complicated topology by adding connections between layers in different level. These multi-branch networks achieve better accuracy than single-path models with approximately the same amount of parameters.

Though deep neural networks can significantly benefit accuracy performance, they bring several difficulties during the training process, including exploding/vanishing gradients and degradation. WideResNet [7] expands the layer width of basic block modules in ResNet and decreases the depth correspondingly to get a tradeoff between width and depth.

With the increase of various topologies of structures and hyperparameters, it becomes more and more challenging to find the optimal one from numerous candidates for different tasks. Neural Architecture Search (NAS) [22]–[24] is proposed to generate more complicated CNN and get improved accuracy but at the costs of a vast amount of computing and human resources. The complicated architectures of models may also reduce the parallelism of computations and increase the latency of models at inference time. Some large models generated by NAS even cannot be trained on typical GPU devices, which limits the implementation and applications of NAS.

# B. Lightweight Neural Networks

In recent years, many lightweight models are designed to reduce the amount of computation such as MobileNet [12], [13], ResNext [25], Xception [11], etc. Some of them adopt depthwise convolutional layers to decrease FLOPs. However, researchers find out that in many conditions depthwise convolution is not as fast as expected, even slower than normal convolution operation because of insufficient support of frameworks and low computation/memory-access ratio. In ShuffleNet [14], [15], the authors discuss this problem and propose shuffle operation to decrease the amount of computation. While in ShiftNet [16], the authors proposes a shift operation, which is a zero-FLOPs operation, to replace normal convolution. Nevertheless, depthwise convolution is very efficient for devices without GPU or with low computation ability, such as mobile devices. The improved version MobileNetV3 [26] is newly proposed, which shows that the lightweight models are still promising in the future.

# C. Model Re-parameterization

Re-parameterization is a method recently investigated to improve the accuracy of neural networks with more parameters but can be fused back into the original format at inference time. It has been shown that over-parameterization, a form of re-parameterization, can speed up the convergence of training and improve generalization ability [27]–[29].

ExpandNets [17] widens the layers in neural networks at training time and contracts back to the original form, which is a component-level improvement. Extra 1 × 1 convolutional layers added for adjusting channels also increase the depth of neural networks. For small compact networks like SmallNet in [17], over-parameterization can make better leverage of GPU resources and achieve higher accuracy with nearly similar training time. However, it will cost much more time and GPU memory to train a slightly larger model such as ResNet20 [4] or MobileNet [12], [13]. The wider channels also increase the difficulty of the training process. The initialization method by using weights of the nonlinear counterparts of the expanded networks are time-consuming. It is worse that this initialization method is not guaranteed to be better than baselines.

A series of work from Ding et al., namely ACNet [30], Diverse Branch Block [31], RepVGG [32], RepMLP [33], add multi-branch architecture at training time and merge extra paths into main path at inference time. These works use the multi-branch architecture and remain the plain-model topology for fast inference speed. This series of research exploress the potential of re-parameterization from another angle of view.

Our proposed new structure based on convolution expansion modules in ExpandNets called Expansion-Squeeze-Block (ES-Block), combines the CL-Expansion with shortcut connections to increase the models’ ability of representing features and decrease the difficulty of training expanded convolutional layers. The newly introduced initialization method also saves much time without training the nonlinear counterparts of the expanded networks.

# D. Network Compression

Recently, network compression has been one of the most popular research topics in deep learning. It aims to reduce the number of parameters with little or even no loss of accuracy. Pruning [34], [35] is a commonly used method to remove the parameters, channels, and even layers of the most minor contribution to neural networks’ learning.

Layer prune [8] uses imprinting [9] to filter out the most least informative layers and deletes them from neural networks. Layer Folding [10] prunes removable ReLU layers to reduce the depth of neural networks and provides the ability to fuse sequential convolutional layers.

Though network compression reduces a network’s size, it is typically performed as a post-processing method, which generally can not provide additional benefits on neural networks’ training and improve accuracy performance. Conversely, our method can be complementary to these works by performing pruning after training the expanded networks.

# III. PRELIMINARY

In this section, we introduce some preliminary concepts about fusing linear layers, including the convolutional and batch normalization layers.

# A. Conv-Conv Fusion

TABLE II PART OF NOTATIONS USED IN THIS PAPER 

<table><tr><td>Notation</td><td>Meaning</td></tr><tr><td> $\mathbf{x}^{(i)}$ </td><td>Input of theithconvolutional layer.</td></tr><tr><td> $\mathbf{y}^{(i)}$ </td><td>Input of theithconvolutional layer.</td></tr><tr><td> $H_{\text{in}}^{(i)}, H_{\text{out}}^{(i)}$ </td><td>Height of theithconvolutional layer&#x27;s input and output.</td></tr><tr><td> $W_{\text{in}}^{(i)}, W_{\text{out}}^{(i)}$ </td><td>Width of theithconvolutional layer&#x27;s input and output.</td></tr><tr><td> $C_{\text{in}}^{(i)}, C_{\text{out}}^{(i)}$ </td><td>Number of input and output channels of theithconvolutional layer.</td></tr><tr><td> $K_{h}^{(i)}, K_{w}^{(i)}$ </td><td>The height and width of theithconvolutional layer&#x27;s kernel.</td></tr><tr><td> $\mathbf{W}^{(i)}$ </td><td>Weight of theithconvolutional layer.</td></tr><tr><td> $\mathbf{b}^{(i)}$ </td><td>Bias of theithconvolutional layer.</td></tr></table>

In [17], the authors introduced that the two consecutive convolutional layers can be fused into a single one. However, they did not show more details on how they are merged. In this section, we provide more derivation details about merging two consecutive convolutional layers. For two sequential con-$\in \mathbb { R } ^ { C _ { \mathrm { o u t } } ^ { ( i ) } \times C _ { \mathrm { i n } } ^ { ( i ) } \times K _ { h } ^ { ( i ) } \times K _ { w } ^ { ( i ) } }$ $\mathbf { W } ^ { ( i + 1 ) } \ \in \ \overline { { \mathbb { R } } } ^ { C _ { \mathrm { o u t } } ^ { ( i + 1 ) } \times C _ { \mathrm { i n } } ^ { ( i + 1 ) } \times K _ { h } ^ { ( i + 1 ) } \times K _ { w } ^ { ( i + 1 ) } }$ 1)×K(i+1)h ×K(i+1)w , $\mathbf { b } ^ { ( i ) } \in$ $\mathbb { R } ^ { C _ { \mathrm { o u t } } ^ { ( i ) } } , { \mathbf { b } } ^ { ( i + 1 ) } \in \mathbb { R } ^ { C _ { \mathrm { o u t } } ^ { ( i + 1 ) } }$ ) , b(i+1) ∈ RC(i+1)out , respectively, where $C _ { \mathrm { o u t } } ^ { ( i ) } = C _ { \mathrm { i n } } ^ { ( i + 1 ) }$ Cin Let x and y be the input and output, we have the following formula for the ith convolutional layer:

$$
\mathbf {y} _ {q, h _ {\text {out}} ^ {(i)}, w _ {\text {out}} ^ {(i)}} ^ {(i)} = \sum_ {p} \sum_ {k _ {h} ^ {(i)}} \sum_ {k _ {w} ^ {(i)}} \mathbf {W} _ {q, p, k _ {h} ^ {(i)}, k _ {w} ^ {(i)}} ^ {(i)} \mathbf {x} _ {p, h _ {\text {in}} ^ {(i)} + k _ {h} ^ {(i)}, w _ {\text {in}} ^ {(i)} + k _ {w} ^ {(i)}} ^ {(i)} + \mathbf {b} _ {q} ^ {(i)} \tag {1}
$$

$$
p \in \left[ 0, C _ {\text { in }} ^ {(i)}\right), \quad q \in \left[ 0, C _ {\text { out }} ^ {(i)}\right),
$$

$$
k _ {h} ^ {(i)} \in \left[ 0, K _ {h} ^ {(i)}\right), \quad k _ {w} ^ {(i)} \in \left[ 0, K _ {w} ^ {(i)}\right)
$$

$$
h _ {\text { in }} ^ {(i)} \in \left[ 0, H _ {\text { in }} ^ {(i)}\right), \quad h _ {\text { out }} ^ {(i)} \in \left[ 0, H _ {\text { out }} ^ {(i)}\right)
$$

$$
w _ {\text { in }} ^ {(i)} \in \left[ 0, W _ {\text { in }} ^ {(i)}\right), \quad w _ {\text { out }} ^ {(i)} \in \left[ 0, W _ {\text { out }} ^ {(i)}\right)
$$

The output of the iis similar as (1) where nal layer . $\mathbf { y } _ { r , h _ { \mathrm { o u t } } ^ { ( i + 1 ) } , w _ { \mathrm { o u t } } ^ { ( i + 1 ) } } ^ { ( i + 1 ) }$ $r \in \left\lceil 0 , C _ { \mathrm { o u t } } ^ { ( i + 1 ) } \right\rceil$

Because the convolutional layers are sequential, we have $\mathbf { x } ^ { ( i + 1 ) } = \mathbf { y } ^ { ( i ) }$ and $C _ { \mathrm { i n } } ^ { ( i + 1 ) } = C _ { \mathrm { o u t } } ^ { ( i ) }$ . Combined with (1), we can get:

$$
\begin{array}{l} \mathbf {y} _ {r, h _ {\text { out }} ^ {(i + 1)}, w _ {\text { out }} ^ {(i + 1)}} ^ {(i + 1)} = \sum_ {r} \sum_ {k _ {h} ^ {(i + 1)}} \sum_ {k _ {w} ^ {(i + 1)}} \mathbf {W} _ {r, q, k _ {h} ^ {(i + 1)}, k _ {w} ^ {(i + 1)}} ^ {(i + 1)} \\ \left(\sum_ {p} \sum_ {k _ {h} ^ {(i)}} \sum_ {k _ {w} ^ {(i)}} \mathbf {W} _ {q, p, k _ {h} ^ {(i)}, k _ {w} ^ {(i)}} ^ {(i)} \mathbf {x} _ {p, h _ {\mathrm{in}} ^ {(i)} + k _ {h}, w _ {\mathrm{in}} ^ {(i)} + k _ {w}} ^ {(i)} + \mathbf {b} _ {q} ^ {(i)}\right) + \mathbf {b} _ {r} ^ {(i + 1)} \\ q \in \left[ 0, C _ {\text { in }} ^ {(i + 1)}\right), \quad r \in \left[ 0, C _ {\text { out }} ^ {(i + 1)}\right), \\ k _ {h} = k _ {h} ^ {(i)} + k _ {h} ^ {(i + 1)}, \quad k _ {w} = k _ {w} ^ {(i)} + k _ {w} ^ {(i + 1)} \tag {2} \\ \end{array}
$$

According to (2), the weight and bias of new fused Conv layer is:

$$
\mathbf {W} _ {r, p, k _ {h}, k _ {w}} = \sum_ {q} \sum_ {p} \sum^ {h} \sum^ {w} \mathbf {W} _ {r, q, k _ {h} ^ {(i + 1)}, k _ {w} ^ {(i + 1)}} ^ {(i + 1)} \mathbf {W} _ {q, p, k _ {h} ^ {(i)}, k _ {w} ^ {(i)}} ^ {(i)}
$$

$$
\mathbf {b} _ {r} = \sum_ {q} \sum_ {p} \sum^ {h} \sum^ {w} \mathbf {W} _ {r, q, k ^ {(i + 1)}, k ^ {(i + 1)}} ^ {(i + 1)} \mathbf {b} _ {q} ^ {(i)} + \mathbf {b} _ {r} ^ {(i + 1)} \tag {4}
$$

The $\sum ^ { h }$ and $\sum ^ { w }$ stands for conditional summation P and P , respectively. $k _ { h } = k _ { h } ^ { \overline { { ( i ) } } } + k _ { h } ^ { ( i + 1 ) } k _ { w } = k _ { w } ^ { \overline { { ( i ) } } } + k _ { w } ^ { ( i + 1 ) }$

It is worth noting that (3) and (4) are only applicable on following conditions:

• Both of the sequential convolutional layers do not have padding.   
• If one convolutional layer has padding, it must be the first one.

![](images/455fa40921bdca17889945780e71ec566add620fc57655cba29573aacc89fe95.jpg)



Fig. 1. Illustration of fusing two 3×3 convolutional layers. The fused kernel’s size of two 3×3 convolutional layers is 5. We iterate the element of one kernel, multiply it with another one, and sum the result into the corresponding position of the fused one.

This is why that in ExpandNets [17], the authors move the padding parameter to the first $1 \times 1$ convolutional layer. However, $1 \times 1$ convolutional layer is a special case that can be fused into the second 3 × 3 convolutional layer even with padding parameter. From (3), the kernel size of new fused convolutional layer is $K = K ^ { ( i ) } + K ^ { ( i + 1 ) } - 1$ when $k ^ { ( i ) } \in \left[ 0 , K ^ { \left( i \right) } \right)$ and $k ^ { ( i + 1 ) } \in [ 0 , K ^ { ( i + 1 ) } )$ . As Fig. 1 shows, if we merge two 3×3 convolutional layers, e.g. $k ^ { ( i ) } = k ^ { ( i + 1 ) } = 3 .$ , the size of new fused kernel is $3 + 3 - 1 = 5$ . This property may lead to more parameters after fusing. But if one of the layers is $1 \times 1$ layer, the kernel size of fused layer will not become larger. So that $1 \times 1$ convolutional layers are used to changing the channels of feature maps before and after $3 \times 3$ convolutional layer.

Also, according to (3), no matter how large $C _ { \mathrm { o u t } } ^ { ( i ) } ~ \mathrm { o r } ~ C _ { \mathrm { i n } } ^ { ( i + 1 ) }$ is, the input and output channels of fused convolutional layer are not affected. Moreover, by applying fusion, the extra computation cost from expanding the width of the model (3) can be eliminated, but without decreasing the accuracy of the model.

# B. Multi-branch Conv fusion

In [32], the authors introduced how to merge two convolutional layers on different branches on specific conditions. This is possible because of the linearity of the convolutional layer. Suppose two 3×3 convolutional layers with weights $\mathbf { W } _ { 1 } , \mathbf { W } _ { 2 }$ and bias $\mathbf { b } _ { 1 } , \mathbf { b } _ { 2 }$ , respectively. The sum of this multi-branch structure is:

$$
\mathbf {y} = \left(\mathbf {W} _ {1} \mathbf {x} + \mathbf {b} _ {1}\right) + \left(\mathbf {W} _ {2} \mathbf {x} + \mathbf {b} _ {2}\right) \tag {5}
$$

The (5) can be easily transformed into the following fused format:

$$
\mathbf {y} = \left(\mathbf {W} _ {1} + \mathbf {W} _ {2}\right) \mathbf {x} + \left(\mathbf {b} _ {1} + \mathbf {b} _ {2}\right) \tag {6}
$$

We can sum the weights and biases to generate a new fused layer. If one branch is 1×1 convolutional layer, we can easily pad the kernel shape to $3 \times 3$ with zeros. If one branch is an identity connection like ResNet [4], we can use a $3 \times 3$ convolutional layer with identity kernel, which generates the output the same as the input.

# C. Conv-BN Fusion

It is a common method to fuse BN layer into previous convolutional layer for faster inference speed in many popular deep learning frameworks. Suppose x and y are the input and output of BN layer respectively, we have:

$$
\mathbf {y} = \gamma \frac {\mathbf {x} - \mu}{\sqrt {\sigma^ {2} + \epsilon}} + \beta \tag {7}
$$

$\mu$ and $\sigma ^ { 2 }$ are the mean and standard deviation of the input batch, respectively.  is a small constant for avoiding division by zero error. $\gamma$ and $\beta$ are parameters to learn from training. During the training process, $\mu , \sigma , \gamma , \beta$ will be updated after each batch and become constants when training is complete so that the BN layer can be fused into the previous convolutional layer.

Let W and b be the weight and bias, Wˆ and $\hat { \mathbf { b } }$ be the weight and bias after fusion. We have:

$$
\hat {\mathbf {W}} = \frac {\gamma}{\sqrt {\sigma^ {2} + \epsilon}} \mathbf {W}, \quad \hat {\mathbf {b}} = \beta - \gamma \frac {\mathbf {b} - \mu}{\sqrt {\sigma^ {2} + \epsilon}} \tag {8}
$$

From the (8), we can see that Conv layer after fusion is equivalent to the original Conv-BN layer sequence.

As for depthwise convolutional layers, it is similar to fuse together. We just need to apply the methods mentioned in this section group by group.

![](images/14599b67dcff6f4d64f1a85770a4d82ee92adc50438be390a044d60639e983a1.jpg)



(a) Normal CNN

![](images/4dba64bb82f0a5a03b3fcf29fce7f47b7a01097f30857616edf0d6d8996984b0.jpg)



(b) CNN-CL

![](images/250c3df3cc7314fd8b4f1d6b653c323ad12b25578d1773ff11db452f3242b545.jpg)



(c) CNN-ES   
Fig. 2. Comparison of different expansion architectures. s and p mean stride and padding parameters, respectively. Usually, 3×3 convolutional layer has stride and padding parameters, but CL-Expansion moves padding parameter to the first 1×1 convolutional layer, which is not the same as the common setting. Our ES-Block adds a shortcut connection and moves the padding parameter back to 3×3 convolutional layer.

# IV. EXPANSION-SQUEEZE-BLOCK

# A. Shortcut Connections

Since Inception [2], [3] and ResNet [4], multi-branch architectures have been known well to be beneficial to performance of networks. As for CL-Expansion, it expands the width of 3×3 convolutional layer, which increases not only the number of parameters but also the difficulty of training. Thus we add shortcut connection structure to improve the performance and decrease the hurdle of training. As Fig. 2 illustrates, ES-Block mainly consists of a main path and a shortcut connection. The main path of ES-Block has two 1 × 1 and one 3 × 3 convolutional layers, which is the same as CL-Expansion in [17]. We also make a minor modification to move the padding parameter back to the 3×3 convolutional layer, which makes the parameter setting more similar to the usual convolutional layer. The shortcut connection here is a ResNet-like structure. During the training, we use ES-Block to substitute each 3×3 convolutional layer in the networks. The first 1×1 convolutional layer expands the channels of the input features and the second one squeezes the width of the output, coming from $3 \times 3$ convolutional layer in the middle, to original size.

The expansion rate e determines the width of expanded convolutional layers. According to [17], we choose e = 4 as our default setting. By changing $e ,$ ES-Block is flexible to fit different accuracy requirements and constraints of hardware resources. Considering the computation cost, the number of channels in the convolutional layer of shortcut connection is the same as the original one.

All these structures can be merged back into the original 3×3 convolutional layer by following the method described in Section III. The batch normalization will bring extra bias if the original convolutional layer does not have bias. However, this bias can be moved into the consecutive batch normalization layer after the main path. If there is no batch normalization layer in the main path, we can omit the bias in shortcut connection too.

![](images/87a799710c0a4ba57820ff82f49bc9d6f40a4dba65c96f0a589191cd7d100041.jpg)  
(a) Identity

![](images/1a1dc4552342bc1d34f81f9680ef98bed5a20c965673215cf31eadcbae5097fb.jpg)  
(b) 1×1 conv

![](images/f4d0b744654103cf6492bf2140722c40b777d3eb7b23d7333df58c5f55f199c1.jpg)  
(c) 3×3 conv   
Fig. 3. Three different structures of shortcut connections. Structure (a) is the same as the residual connection in ResNet [4]. Structure (b) is used when $C _ { \mathrm { i n } } \neq C _ { \mathrm { o u t } }$ or stride $s \neq 1 .$ . Structure (c) is used when the shape of the output is not the same as the input. Considering the computation cost, we usually choose (a) or (b) as default settings. (c) is used when the original model is compact enough with little parameters. The number of input and output channels of the convolutional layer in shortcut connection is the same as that in the main path before expansion. All these structures can be contracted back to the format of the original networks.

# B. Initialization

The initialization is essential for training neural networks to get better accuracy. In [17], the authors tried to use the weights of simply trained nonlinear counterpart of the neural networks with the CL-Expansion module and achieve better results on some models. However, as Table I shows, it costs largely much time to train an expanded neural network than the original one, let alone to train it twice. Sometimes we may even get a worse result by using the weights of the nonlinear model. Thus we want a new method to initialize the expanded model

![](images/e55f71a3d300726c561357dc2838b1b6505901ec68d425aac4f47597d6ef9e48.jpg)



Fig. 4. Identity initialization for $3 \times 3$ convolutional layer with kernel $\breve { \mathbf W } \in \mathbb R ^ { 2 \times 2 \times \bar { 3 } \times 3 }$ . The block in kernel filled with dashed lines means that it is assigned with value 1, and other blank blocks are all set to 0. By this initialization method, the output of the convolutional layer, when padding parameter is one, is the same as the input so that we call it identity initialization. For 1 convolutional layer, it is similar to do such as work by removing the blank blocks around of the 3 × 3 kernel.

by utilizing the weights of the trained original one, which is much easier to train or download from the open-source repository. However, because of the two extra added 1 × 1 convolutional layers and channels in 3×3 convolutional layer in the middle, it is not possible to directly assign the weights of the original neural networks to the expanded one. We start from trying a method that we call identity initialization by assigning value 1 to the specific positions of 3×3 convolutional kernel, the output of which is the same as the input except that the expanded extra channels are all zeros. Fig. 4 shows the details of identity initialization for convolutional layers. We use the same assignment strategy for 1×1 convolutional layers. Therefore, the sequential layers will not make any change to the input. Based on this, we substitute the weights of $3 \times 3$ layer by that of the original network so that the output of the expanded module is the same as the original contracted one before the training. However, this method will leave most of the channel’s values to zero, which is not beneficial for training. Thus, we design the following modified version approach for better performance in practice.

![](images/ccef4a0c6e6f5978ed0955b8aeded23ead4cb46c2601a279a8864be3aa4e891b.jpg)



Fig. 5. Illustration of initializing expanded $3 \times 3$ layer. The original 3×3 has kernel W ∈ R2×2×3×3. We set expansion rate $e = 4$ and get an expanded layer with kernel $\mathbf { W } ^ { \prime } \in \mathbb { R } ^ { 8 \times 8 \times 3 \times \mathbf { \dot { 3 } } }$ . The white block in the figure means zero value initially. We firstly initialize them by kaiming-uniform [36], which is default initialization method in PyTorch framework (we omit this process in the figure). Then we copy the weights from pretrained original model to assign the expanded layer. For example, we copy the weights to overwrite the first 2 channels of the first 2 kernel group (one kernel group generates one channel of the output features). For a layer with bias, we also copy the bias to the first 2 channels.

1) Initialization of normal convolutional layer: We use a original $3 \times 3$ convolutional layer with kernel W $\in$ $\mathbb { R } ^ { C _ { \mathrm { { i n } } } \times \mathbf { \breve { C } _ { \mathrm { { o u t } } } } \times 3 \times 3 }$ as example. With expansion $e ,$ the expanded layer has new kernel $\mathbf { \dot { W } } ^ { \prime } \in \mathbb { R } ^ { e C _ { \mathrm { i n } } \times e C _ { \mathrm { o u t } } \times 3 \times 3 }$ . Suppose the initial value of weights are all zeros, we first use the default initialization method, e.g. kaiming-uniform, in PyTorch framework to initialize the weights of expanded layer. Then we copy the weights from the origial pretrained layer and assign them to the corresponding position. As algorithm 1 describes, for a channel of the pretrained weight $W [ i , j , : , : ]$ , we use them to assign the weights of the expanded layer $W ^ { \prime } [ i , j , : , : ]$ , which are at the same position. If the layer has bias, we also set the bias of the ith channel $b ^ { \prime } [ i ]$ with b[i]. The Fig. 5 shows an example when setting input and output channels $C _ { \mathrm { i n } } = C _ { \mathrm { o u t } } = 2$ and expansion rate $e = 4 .$ .

For $1 \times 1$ convolutional layer, we simply assign the weights with kaiming-uniform initialization method, which is the same

Algorithm 1: Init convolutional layer with pretrained weights   
Input: Old and new convolutional layer old, new
Result: New convolutional layer new initialized by weight of old
Data: Input channels $C_{in}$ , output channels $C_{out}$ , kernel W, bias b, group G

1 Function InitConv3x3 (old, new):
2    kaimingInit(new.W)
3    for $i \in [0, old.C_{out})$ do
4    for $j \in [0, old.C_{in})$ do
5    new.W[i, j, :, :] ← old.W[i, j, :, :]
6    end
7    end
8    if old has bias b then
9    for $i \in [0, old.C_{out})$ do
10    new.b[i] ← old.b[i]
11    end
12    end

13

14 Function InitDWConv3x3 (old, new):
15    group ← old.G
16    kaimingInit(new.W)
17 $G_{in}^{old}$ ← int (old. $C_{in}$ /group)
18 $G_{out}^{old}$ ← int (old. $C_{out}$ /group)
19 $G_{out}^{new}$ ← int (new. $C_{out}$ /group)
20    planes ← min( $G_{in}^{old}, G_{out}^{old}$ )
21    for $i \in [0, group)$ do
22    for $j \in [0, planes)$ do
23    new.W[i · $G_{out}^{new}, j, :, :$ ] ← old.W[i, j, :, :]
24    end
25    end
26    if old has bias b then
27    fill new.b with zero
28    for $i \in [0, group)$ do
29    new.b[i · $G_{out}^{new}$ ] ← old.W[i]
30    end
31    end

32

33 Function InitConv1x1 (conv):
34    kaimingInit(conv.W)

35

36 Function InitDWConv1x1 (conv):
37    kaimingInit(conv.W)

![](images/56dfd5999a7d98d3cf8aaf87e4ae9073f6e252c9ff1738046d0595d71abdf5f9.jpg)



Fig. 6. Illustration of initializing expanded depthwise 3 × 3 convolutional layer. The orignal $3 \times 3$ has $C _ { \mathrm { i n } } ^ { \mathrm { ~ - ~ } } = \mathrm { ~ C _ { o u t } ~ = ~ 2 ~ }$ and group $G = 2 ,$ which means the kernel $\mathbf { W } \in \mathbb { R } ^ { 2 \times 1 \times \dddot { 3 } \times 3 }$ . When set expansion rate e = 4 without changing group G, we get an expanded layer with $\mathrm { \bar { \it C } _ { i n } } =  { \cal C } _ { \mathrm { o u t } } = 8$ and kernel $\mathbf { W } ^ { \prime } \in \mathbb { R } ^ { \breve { 8 } \times 4 \times 3 \times \breve { 3 } }$ . The initialization of depthwise convolutional layer is a little different from initializing general one because of the difference between depthwise and normal convolution operation. We firstly initialize the expanded kernel with kaiming-uniform (we omit this process in the figure), then we copy the 2 channels of pretrained weights to the corresponding position. The bias initialization is similar to that of the weight.

2) Initialization of depthwise convolutional layer: For depthwise convolutional layer, we still follow the same strategy. However, due to the difference between the depthwise and normal convolution, we need to make a little modification to remain the identity property. Fig 6 shows the details of this process. Suppose the original kernel has G groups, which is the same as the number of input channels $C _ { \mathrm { i n } }$ . After expansion, though the number of input and output channels increased, the group is still the same as the original layer. Thus there is only one channel of each group in the expanded layer coming from the pretrained original model. The jth channel of the original model is copied to the jth channel of the jth group, as shown in Fig 6.

# C. Evaluation of Layer Importance

Because training expanded networks will be very timeconsuming, we consider selecting some layers of more importance to expand to decrease the training time. Many prune works [37], [38] use weight norm to evaluate the layer importance and prune the layers with smallest scores. For a convolutional layer with kernel $\mathbf { W } ~ \in ~ \mathbb { R } ^ { C _ { \mathrm { { i n } } } \times C _ { \mathrm { { o u t } } } \times 3 \times 3 }$ , th e weight norm of this layer is computed by (9).

$$
\text { weight - norm } (\mathbf {W}) = \frac {1}{C _ {\text { out }}} \sum_ {i = 1} ^ {C _ {\text { out }}} \| \mathbf {W} [ i,:,: ] \| _ {2} \tag {9}
$$

We sort the weight norm and choose the first k layers with highest scores to expand.

In this section, we demonstrate the effectiveness of our initialization method on image classification task.

We denote the expansion strategy in ExpandNets [17] by CL, and ours by ES. We firstly use small networks [17] to study our approach on CIFAR-100 [18] dataset. Then we show that our method can improve the results of other compact networks ResNet20 [4], ShuffleNetV2 0.5× [15] on CIFAR-100 and Tiny-ImageNet datasets [19].

We also report how different initialization method affects the final results of models. We use Uniform to stand for default initialization method, i.e. kaiming-uniform, in PyTorch [6] framework, Normal for kaiming-normal. In [17], the authors use the trained nonlinear counterpart of the expanded network to initialize the model, which we call Nonlinear. Moreover, we use Pretrained to denote our method utilizing the trained original network for initialization.

# A. Experimental setup

For CIFAR-100 [18] and Tiny-ImageNet [19], we use some compact networks to show the effectiveness of our approach, including SmallNet, which is the same as one in [17], VGG11- BN 0.5×, ResNet20 and ShuffleNetV2 0.5×. To evaluate our proposed ES-Block, we compare it with the expansion strategy CL in [17] and baselines of the original model. The expansion rate e is set to 4 by default, which is a good balance between accuracy and computation cost mentioned in [17]. It is important to train deep neural networks with a proper initialization method. We report the final results of the models to demonstrate the effect of different initialization methods. We use stochastic gradient descent (SGD) with a learning rate of 0.1, momentum of 0.9, and weight decay of 0.0001 to train networks for 200 epochs using a batch size of 128 and apply OneCycleLR scheduler to adjust the learning rate during the training process if no extra explanation.

TABLE III TOP-1 ACCURACY(%) OF SMALLNET WITH DIFFERENT INITIALIZATION METHOD ON CIFAR-100 DATASET . 

<table><tr><td>Model</td><td>Initialization</td><td>CIFAR-100</td></tr><tr><td>SmallNet</td><td>Uniform</td><td>43.80 ± 0.67</td></tr><tr><td>SmallNet-CL</td><td>Uniform</td><td>43.74 ± 0.57</td></tr><tr><td>SmallNet-ES</td><td>Uniform</td><td>44.35 ± 0.41</td></tr><tr><td>SmallNet</td><td>Normal</td><td>43.70 ± 0.25</td></tr><tr><td>SmallNet-CL</td><td>Normal</td><td>44.06 ± 0.34</td></tr><tr><td>SmallNet-ES</td><td>Normal</td><td>44.15 ± 0.38</td></tr><tr><td>SmallNet-CL</td><td>Nonlinear*</td><td>45.23 ± 0.13</td></tr><tr><td>SmallNet-ES</td><td>Uniform-Pretrained</td><td>45.60 ± 0.21</td></tr><tr><td>SmallNet-CL</td><td>Nonlinear**</td><td>45.45 ± 0.12</td></tr><tr><td>SmallNet-ES</td><td>Normal-Pretrained</td><td>45.83 ± 0.36</td></tr></table>

∗Nonlinear counterpart is trained with kaiming-uniform initialization.

∗∗Nonlinear counterpart is trained with kaiming-normal initialization.

# B. Results

We first validate our proposed structure and initialization method on SmallNet [17]. From Table III, we show that our ES-block utilizing shortcut connection combined with expansion strategy brings a 0.55% increase on top-1 accuracy while CL-Expansion is even lower than the baseline. The shortcut used in SmallNet is a 3×3 convolutional layer with a batch normalization layer because the shape of the input is not the same as the output.

Then we use different methods to initialize the weights of models to see how they affect the final results. The composite initialization, like Uniform-Pretrained, means that we first use kaiming-uniform to initialize the weights, and then use the weights of the pretrained model to overwrite as described in Section IV. We can see that our ES-Block also outperforms the CL-Expansion with different initialization methods. Using ES-Block combined with Pretrained initialization, we can get a highest 2.03% improvement compared with the baseline. In addition, Table III indicates that our initialization method Pretrained is also better than Nonlinear with an average 0.36% increase. In consideration of the time cost of training a nonlinear counterpart of expanded networks, our initialization is much more time-saving.

TABLE IV TOP-1 ACCURACY(%) ON CIFAR-100 AND TINY-IMAGENET DATASET. 

<table><tr><td>Model</td><td>Initialization</td><td>CIFAR-100</td><td>Tiny-ImageNet</td></tr><tr><td>VGG11-BN 0.5×</td><td>Uniform</td><td>64.47</td><td>44.34</td></tr><tr><td>VGG11-BN 0.5×-CL</td><td>Uniform</td><td>63.67</td><td>44.96</td></tr><tr><td>VGG11-BN 0.5×-ES</td><td>Uniform</td><td>67.25</td><td>47.07</td></tr><tr><td>VGG11-BN 0.5×-CL</td><td>Nonlinear</td><td>61.99</td><td>42.49</td></tr><tr><td>VGG11-BN 0.5×-CL</td><td>Pretrained</td><td>63.40</td><td>44.52</td></tr><tr><td>VGG11-BN 0.5×-ES</td><td>Pretrained</td><td>65.76</td><td>47.39</td></tr><tr><td>ResNet20</td><td>Normal</td><td>67.03</td><td>46.35</td></tr><tr><td>ResNet20-CL</td><td>Normal</td><td>68.58</td><td>45.76</td></tr><tr><td>ResNet20-ES</td><td>Normal</td><td>68.91</td><td>46.64</td></tr><tr><td>ResNet20-CL</td><td>Nonlinear</td><td>67.39</td><td>43.86</td></tr><tr><td>ResNet20-CL</td><td>Pretrained</td><td>69.16</td><td>45.80</td></tr><tr><td>ResNet20-ES</td><td>Pretrained</td><td>69.54</td><td>47.09</td></tr><tr><td>ShuffleNetV2 0.5×</td><td>Uniform</td><td>67.18</td><td>49.98</td></tr><tr><td>ShuffleNetV2 0.5×-CL</td><td>Uniform</td><td>67.22</td><td>49.73</td></tr><tr><td>ShuffleNetV2 0.5×-ES</td><td>Uniform</td><td>67.52</td><td>49.93</td></tr><tr><td>ShuffleNetV2 0.5×-CL</td><td>Nonlinear</td><td>65.08</td><td>48.74</td></tr><tr><td>ShuffleNetV2 0.5×-CL</td><td>Pretrained</td><td>68.68</td><td>49.91</td></tr><tr><td>ShuffleNetV2 0.5×-ES</td><td>Pretrained</td><td>67.62</td><td>50.79</td></tr></table>

Because the SmallNet is a plain toy model, we then evaluate our method on other complicated models. We choose VGG11- BN 0.5×, which is also a plain model that modified from VGG11-BN [1] by removing half of the channels to make it more compact, ResNet20 [4], which has identity connections, and ShuffleNet 0.5× [14], [15], which uses depthwise convolutional layer shortcut connections. These candidates cover some typical architectures of neural networks, making the results more representative. For ResNet20, the parameters settings are the same as that mentioned at Section V-A. The shortcut connection of ES-Block in ResNet20 consists of a 1 × 1 convolutional layer and a batch normalization layer because it has better performance than other structures. For ShuffleNet, we use an identity shortcut in ShuffleNet or a depthwise 1×1 convolutional layer with batch normalization layer if $C _ { \mathrm { i n } } \neq C _ { \mathrm { o u t } }$ or stride $s \neq 1$ considering the computation cost. For simplicity, we use Pretrained in Table IV to stand for Uniform-Pretrained or Normal-Pretrained.

From Table IV, it is indicated that for a plain model like VGG, ES-Block can bring 2.78% and 2.73% improvement on CIFAR-100 and Tiny-ImageNet, respectively. For ResNet20, the ES-Block can also bring benefits on accuracy. It can bring 0.33% and 0.88% increase on CIFAR-100 and Tiny-ImageNet than ResNet-CL. With Pretrained initialization, the accuracy can be better. ResNet-CL is even worse than baseline on the Tiny-ImageNet dataset. For ShuffleNet, ES-Block gives a 0.34% improvement on CIFAR-100. Though both ES-Block and CL-Expansion are worse than baseline on Tiny-ImageNet, with Pretrained initialization method, the accuracy of ES-Block is 0.66% higher than baseline.

The results show that ES-Block is an effective alternative, at least a complement, to CL-Expansion, especially for plain models like VGG. Interestingly, Pretrained initialization method can be beneficial to both ES-Block and CL-Expansion with higher accuracy than baselines only except VGG on CIFAR-100, which indicates that it is very promising to explore effective initialization methods. Besides, our Pretrained method needs not to train a nonlinear counterpart of the expanded models which is very time-consuming as Table I shows. Though the topology of the original model is not the same as that after expansion at first view, it is essentially the same because the expanded model can be contracted to the original one without any information loss. It is worth noting that in some cases, CL-Expansion with our initialization method is better than ES-Block. This is might because the topology of CL-Expansion is more similar to that of the original model compared with ES-Block, and we have no special initialization strategy for shortcut connections in ES-Block. The more underlying reason might be that, in these cases, the overlap between initialization value got by our method and the final value after training is smaller than that of CL-Expansion [39], [40]. It is still a open problem to find the optimal initialization method for a given neural network.

# C. Analysis of Complexity

TABLE V MODEL COMPLEXITY ANALYSIS ON CIFAR-100. 

<table><tr><td>Model</td><td>#Params</td><td>#MACs</td><td>Epoch Time</td></tr><tr><td>SmallNet</td><td>20.90K</td><td>508.66K</td><td>3.52s</td></tr><tr><td>SmallNet-CL</td><td>117.40K</td><td>8.08M</td><td>4.80s</td></tr><tr><td>SmallNet-ES</td><td>123.49K</td><td>8.57M</td><td>5.92s</td></tr><tr><td>VGG11-BN 0.5×</td><td>2.33M</td><td>38.81M</td><td>5.02s</td></tr><tr><td>VGG11-BN 0.5×-CL</td><td>39.04M</td><td>659.24M</td><td>44.01s</td></tr><tr><td>VGG11-BN 0.5×-ES</td><td>39.30M</td><td>663.69M</td><td>46.07s</td></tr><tr><td>ResNet20</td><td>278.32K</td><td>41.23M</td><td>8.58s</td></tr><tr><td>ResNet20-CL</td><td>4.54M</td><td>688.32M</td><td>41.00s</td></tr><tr><td>ResNet20-ES</td><td>4.81M</td><td>693.197M</td><td>42.25s</td></tr><tr><td>ShuffleNetV2 0.5×</td><td>444.29K</td><td>11.52M</td><td>28.68s</td></tr><tr><td>ShuffleNetV2 0.5×-CL</td><td>603.93K</td><td>33.57M</td><td>97.57s</td></tr><tr><td>ShuffleNetV2 0.5×-ES</td><td>604.05K</td><td>33.69M</td><td>99.33s</td></tr></table>

We evaluate the complexity of models on NVIDIA P100 GPU. Table V shows the complexity of networks with different structures. It is evident that over-parameterization will increase the MACs and parameters much more than the original models. Our ES-Block is slightly heavy than CL-Expansion, which is trivial compared to over-parameterization, but with better results on some conditions. The epoch time shows that training expanded networks is very time-consuming, especially for models with depthwise convolutional layers. This highlights the importance of our Pretrained initialization method by utilizing the weights of pretrained original models, which are easier to train or get from open-source resources.

# D. Partly Expansion

Because of the long time to train expanded networks, we introduce a method by using weight norm to evaluate the importance of each layer and choose the first k layers with highest importance scores to expand for decreasing the training time. We test our method with VGG11-BN 0.5× and ResNet20 on CIFAR-100 dataset. We also compare our strategy with a naive expansion strategy by layer order.

There are totally 8 and 19 convolutional layers in VGG11- BN 0.5× and ResNet20. From Fig. 7, we can see that, by partly expansion, we can save much time without or with little accuracy loss. It is interesting to see that partly expansion strategy not only reduces training time but also improves the accuracy in some cases. Choosing about first 13 important layers to expand is a good choice compared with expanding all of them. Compared with naive layer order expansion strategy, our method can get a better accuracy. If we choose the top 3 layers in VGG with highest scores to expand, we can have a 0.12% accuracy increase and save 68.29% #MACs and 46.03% #Params than expanding all convolutional layers on CIFAR-100 dataset. For ResNet20, we can choose the top 9 layers to get the same accuracy result with 49.35% less #MACs and 31.60% less #Params. The results show that it is a good strategy to choose some layers with the highest importance to expand rather than expanding all of them.

# VI. CONCLUSION

We have introduced a new structure called Expansion-Squeeze-Block by leveraging over-parameterization to train a given compact neural network. The structure combines expansion and shortcut connections for better performance without adding any nonlinearity. The expanded networks can be contracted back to the original format algebraically at inference time without loss of information. From the experiments, we showed that ES-Block is a good alternative, at least a complement, to CL-Expansion [17], especially for plain models. In addition, we have shown that our new initialization method utilizing the weights of pretrained original networks can be a good initialization strategy for training expanded networks with different expanding strategies such as CL-Expansion. It is better than Nonlinear strategy with better performance and stability and, most importantly, much time-saving. The success of the initialization method and partly expansion strategy also motivate us to explore effective initialization schemes and evaluation method of layer importance further in the future.

# ACKNOWLEDGMENT

This research is supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, No. 62132018, No. 61822209, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002. This work was partially supported by the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” in ICLR, 2015.   
[2] C. Szegedy, V. Vanhoucke, S. Ioffe, J. Shlens, and Z. Wojna, “Rethinking the inception architecture for computer vision,” in CVPR. IEEE Computer Society, 2016, pp. 2818–2826.   
[3] C. Szegedy, S. Ioffe, V. Vanhoucke, and A. A. Alemi, “Inception-v4, inception-resnet and the impact of residual connections on learning,” in AAAI. AAAI Press, 2017, pp. 4278–4284.   
[4] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in CVPR. IEEE Computer Society, 2016, pp. 770–778.   
[5] G. Huang, Z. Liu, L. van der Maaten, and K. Q. Weinberger, “Densely connected convolutional networks,” in CVPR. IEEE Computer Society, 2017, pp. 2261–2269.   
[6] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, A. Desmaison, A. Kopf, E. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang, J. Bai, and S. Chintala, “Pytorch: An imperative style, high-performance deep learning library,” in Advances in Neural Information Processing Systems 32, H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alche-Buc, ´ E. Fox, and R. Garnett, Eds. Curran Associates, Inc., 2019, pp. 8024–8035. [Online]. Available: http://papers.neurips.cc/paper/ 9015-pytorch-an-imperative-style-high-performance-deep-learning-library. pdf   
[7] S. Zagoruyko and N. Komodakis, “Wide residual networks,” in BMVC. BMVA Press, 2016.   
[8] S. Elkerdawy, M. Elhoushi, A. Singh, H. Zhang, and N. Ray, “To filter prune, or to layer prune, that is the question,” in ACCV (3), ser. Lecture Notes in Computer Science, vol. 12624. Springer, 2020, pp. 737–753.   
[9] H. Qi, M. Brown, and D. G. Lowe, “Low-shot learning with imprinted weights,” in CVPR. Computer Vision Foundation / IEEE Computer Society, 2018, pp. 5822–5830.   
[10] A. B. Dror, N. Zehngut, A. Raviv, E. Artyomov, R. Vitek, and R. J. Jevnisek, “Layer folding: Neural network depth reduction using activation linearization,” CoRR, vol. abs/2106.09309, 2021.   
[11] F. Chollet, “Xception: Deep learning with depthwise separable convolutions,” in CVPR. IEEE Computer Society, 2017, pp. 1800–1807.   
[12] A. G. Howard, M. Zhu, B. Chen, D. Kalenichenko, W. Wang, T. Weyand, M. Andreetto, and H. Adam, “Mobilenets: Efficient convolutional neural networks for mobile vision applications,” CoRR, vol. abs/1704.04861, 2017.   
[13] M. Sandler, A. G. Howard, M. Zhu, A. Zhmoginov, and L. Chen, “Mobilenetv2: Inverted residuals and linear bottlenecks,” in CVPR. Computer Vision Foundation / IEEE Computer Society, 2018, pp. 4510– 4520.   
[14] X. Zhang, X. Zhou, M. Lin, and J. Sun, “Shufflenet: An extremely efficient convolutional neural network for mobile devices,” in CVPR. Computer Vision Foundation / IEEE Computer Society, 2018, pp. 6848– 6856.   
[15] N. Ma, X. Zhang, H. Zheng, and J. Sun, “Shufflenet V2: practical guidelines for efficient CNN architecture design,” in ECCV (14), ser. Lecture Notes in Computer Science, vol. 11218. Springer, 2018, pp. 122–138.   
[16] B. Wu, A. Wan, X. Yue, P. H. Jin, S. Zhao, N. Golmant, A. Gholaminejad, J. Gonzalez, and K. Keutzer, “Shift: A zero flop, zero parameter alternative to spatial convolutions,” in CVPR. Computer Vision Foundation / IEEE Computer Society, 2018, pp. 9127–9135.

![](images/81af874e6be9a4d3e00480cfc221d720e59b5be3280c2df70c7622b6b4e709a1.jpg)



(a) VGG11-BN 0.5× accuracy(%) on CIFAR-100

![](images/4d2b53be0d06bbdc0ef878ce49f13c87305ffb1b73b8999a4724957d8beac597.jpg)



(b) VGG11-BN 0.5× #MACs

![](images/adc42b2e5e85ff5a013bfe094f75f57944c01b85c04bbfed1ca14ec0ae732320.jpg)



(c) VGG11-BN 0.5× #Params

![](images/e8fda8fa7a6081c5c66efc54f9a1572f492da49e920161bcc4160755f6b61ad0.jpg)



(d) ResNet20 accuracy(%) on CIFAR-100

![](images/56eb19a1b17afe684895246d70411e44af67405450bc0a8f9d4192588a569483.jpg)



(e) ResNet20 #MACs

![](images/a94902074bcdccc3c8b00157aec38a196a7c9d9b5cbe4c1ff1815b7fe30c3aee.jpg)



(f) ResNet20 #Params   
Fig. 7. Accuracy and complexity analysis of partly expansion strategy. (a) and (d) is the accuracy of VGG11-BN 0.5× and ResNet20 on CIFAR-100 with different number of expanded layers. (b) and (e) shows the #MACs of the models, (c) and (f) shows the #Params, respectively. We can see that expanded all of the convolutional layers is not the best choice in some cases. It is better to choose the layers with highest importance scores to expand to make a good trade-off between accuracy and computation cost. We also compare our strategy with a naive expansion strategy by layer order.

[17] S. Guo, J. M. Alvarez, and M. Salzmann, “Expandnets: Linear overparameterization to train compact convolutional networks,” in NeurIPS, 2020.   
[18] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” 2009.   
[19] Y. Le and X. Yang, “Tiny imagenet visual recognition challenge,” CS 231N, vol. 7, no. 7, p. 3, 2015.   
[20] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification with deep convolutional neural networks,” in NIPS, 2012, pp. 1106– 1114.   
[21] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. E. Reed, D. Anguelov, D. Erhan, V. Vanhoucke, and A. Rabinovich, “Going deeper with convolutions,” in CVPR. IEEE Computer Society, 2015, pp. 1–9.   
[22] B. Zoph, V. Vasudevan, J. Shlens, and Q. V. Le, “Learning transferable architectures for scalable image recognition,” in CVPR. Computer Vision Foundation / IEEE Computer Society, 2018, pp. 8697–8710.   
[23] E. Real, A. Aggarwal, Y. Huang, and Q. V. Le, “Regularized evolution for image classifier architecture search,” in AAAI. AAAI Press, 2019, pp. 4780–4789.   
[24] C. Liu, B. Zoph, M. Neumann, J. Shlens, W. Hua, L. Li, L. Fei-Fei, A. L. Yuille, J. Huang, and K. Murphy, “Progressive neural architecture search,” in ECCV (1), ser. Lecture Notes in Computer Science, vol. 11205. Springer, 2018, pp. 19–35.   
[25] S. Xie, R. B. Girshick, P. Dollar, Z. Tu, and K. He, “Aggregated residual ´ transformations for deep neural networks,” in CVPR. IEEE Computer Society, 2017, pp. 5987–5995.   
[26] A. Howard, R. Pang, H. Adam, Q. V. Le, M. Sandler, B. Chen, W. Wang, L. Chen, M. Tan, G. Chu, V. Vasudevan, and Y. Zhu, “Searching for mobilenetv3,” in ICCV. IEEE, 2019, pp. 1314–1324.   
[27] Z. Allen-Zhu, Y. Li, and Y. Liang, “Learning and generalization in overparameterized neural networks, going beyond two layers,” in NeurIPS, 2019, pp. 6155–6166.   
[28] Z. Allen-Zhu, Y. Li, and Z. Song, “A convergence theory for deep learning via over-parameterization,” in ICML, ser. Proceedings of Machine Learning Research, vol. 97. PMLR, 2019, pp. 242–252.   
[29] S. Arora, N. Cohen, and E. Hazan, “On the optimization of deep networks: Implicit acceleration by overparameterization,” in ICML, ser. Proceedings of Machine Learning Research, vol. 80. PMLR, 2018, pp. 244–253.   
[30] X. Ding, Y. Guo, G. Ding, and J. Han, “Acnet: Strengthening the kernel skeletons for powerful CNN via asymmetric convolution blocks,” in ICCV. IEEE, 2019, pp. 1911–1920.

[31] X. Ding, X. Zhang, J. Han, and G. Ding, “Diverse branch block: Building a convolution as an inception-like unit,” in CVPR. Computer Vision Foundation / IEEE, 2021, pp. 10 886–10 895.   
[32] X. Ding, X. Zhang, N. Ma, J. Han, G. Ding, and J. Sun, “Repvgg: Making vgg-style convnets great again,” in CVPR. Computer Vision Foundation / IEEE, 2021, pp. 13 733–13 742.   
[33] X. Ding, C. Xia, X. Zhang, X. Chu, J. Han, and G. Ding, “Repmlp: Re-parameterizing convolutions into fully-connected layers for image recognition,” arXiv preprint arXiv:2105.01883, 2021.   
[34] M. Figurnov, A. Ibraimova, D. P. Vetrov, and P. Kohli, “Perforatedcnns: Acceleration through elimination of redundant convolutions,” in NIPS, 2016, pp. 947–955.   
[35] H. Li, A. Kadav, I. Durdanovic, H. Samet, and H. P. Graf, “Pruning filters for efficient convnets,” in ICLR (Poster). OpenReview.net, 2017.   
[36] K. He, X. Zhang, S. Ren, and J. Sun, “Delving deep into rectifiers: Surpassing human-level performance on imagenet classification,” in ICCV. IEEE Computer Society, 2015, pp. 1026–1034.   
[37] J. Luo, J. Wu, and W. Lin, “Thinet: A filter level pruning method for deep neural network compression,” in ICCV. IEEE Computer Society, 2017, pp. 5068–5076.   
[38] M. Lin, R. Ji, Y. Wang, Y. Zhang, B. Zhang, Y. Tian, and L. Shao, “Hrank: Filter pruning using high-rank feature map,” in CVPR. Computer Vision Foundation / IEEE, 2020, pp. 1526–1535.   
[39] Y. Tian, T. Jiang, Q. Gong, and A. S. Morcos, “Luck matters: Understanding training dynamics of deep relu networks,” CoRR, vol. abs/1905.13405, 2019.   
[40] J. Frankle and M. Carbin, “The lottery ticket hypothesis: Finding sparse, trainable neural networks,” in ICLR. OpenReview.net, 2019.