# Enabling Flexible Resource Allocation in Mobile Deep Learning Systems

Chao Wu , Member, IEEE, Lan Zhang , Member, IEEE, Qiushi Li, Ziyan Fu, Wenwu Zhu , Fellow, IEEE, and Yaoxue Zhang , Senior Member, IEEE

Abstract—Deep learning provides new opportunities for mobile applications to achieve higher performance than before. Rather, the deep learning implementation on mobile device today is largely demanding on expensive resource overheads, imposes a significant burden on the battery life and limited memory space. Existing methods either utilize cloud or edge infrastructure that require to upload user data, however, resulting in a risk of privacy leakage and large data transfers; or adopt compressed deep models, nevertheless, downgrading the algorithm accuracy. This paper provides DeepShark, a platform to enable mobile devices with the ability of flexible resource allocation in using commercial-off-the-shelf (COTS) deep learning systems. Compared to existing approaches, DeepShark seeks a balanced point between time and memory efficiency by user requirements, breaks down sophisticated deep model into code block stream and incrementally executes such blocks on system-on-chip (SoC). Thus, DeepShark requires significantly less memory space on mobile device and achieves the default accuracy. In addition, all referred user data of model processing is handled locally, thus to avoid unnecessary data transfer and network latency. DeepShark is now developed on two COTS deep learning systems, i.e., Caffe and TensorFlow. The experimental evaluations demonstrate its effectiveness in the aspects of memory space and energy cost.

Index Terms—Deep learning system, flexible resource allocation, computation optimization, mobile device

# 1 INTRODUCTION

DEEP learning nowadays has achieved remarkable results. Such a significant success of deep learning enables us to envision an intriguing life that mobile devices are to become our brilliant assistants. There are continuous efforts devoted to process mobile user data, e.g., photos, leveraging existing deep learning systems. Those efforts provide users with high quality of experience and more intelligent applications such as albums classification. However, high quality deep learning models are often computation-intensive and hard to be applied on commercial offthe-shelf (COTS) mobile devices (due to constrained resource and limited battery life) [1]. As a result, existing cloud deep learning systems, e.g., Amazon Rekognition, usually require users to upload their personal data to remote machine for high quality inference processing. However, to upload all referred data to remote can lead to large data transfer [2] and potential privacy risks [3]. Using edge device though might address these two problems, it still demands significant time consumed to deliver data

(including deep model and user data) and thus result in inefficient system performance. A natural strategy is to run mobile deep learning system that mitigates both data transfer and privacy issues, however, leading to a long model inference time.

There are many efforts to make deep learning locally applicable and faster on COTS mobile devices [4], [5], [6]. Recently, SparseSep [7], DeepX [8], DeepMon [9] and Paddle [10] systematically demonstrate that deep learning on smartphone can be achieved by using compressed models. However, such an approach might downgrade algorithm accuracy with on average a loss of 10 percent, and even up to a loss of 15 percent [11]. Taken together, we debate an unanswered question that is it possible to achieve high quality deep learning on mobile devices but at a modest resource overhead? Moreover, we ask that can such high-quality deep learning implemented with flexible resource allocation so that user can decide if they want time efficiency or memory-usage efficiency?

Based on the intuitions, this paper explores the potential and possibility of running high quality deep learning on mobile devices. Here, we propose to implement resource efficient deep learning inference with the same accuracy as that can be achieved by a high-end server. Toward this goal, we present the design and implementation of a platform called DeepShark, to achieve the following points:

1. To keep away from unnecessary data transfer, all computation are conducted locally and no userrelated data transmission is required.

2. To benefit users with high quality mobile deep learning system, the existing deep learning models should be adopted directly without accuracy loss, and the energy overhead should be minimized.

![](images/40ccd26d28b1d885d88cd89652c8ec9be07d202df97d4660df645ee1826bad7d.jpg)



Fig. 1. The principle of a CNN based deep learning.

3. To achieve flexible resource allocation, a memory management is required. In addition, it should offer an adaptive trade-off between time and memoryusage efficiency.   
4. To maximize the reliability of DeepShark, we implement the platform compatible on top of COTS deep learning systems that provides easy programmability with a few lines of codes modification through our provided APIs.

More specifically, we propose to break down the deep learning inference process and execute them incrementally. That is, high quality deep learning model (original neural network unit) is broken down into small size of input-toexecute code blocks, which are then executed on system-onchip (SoC) in sequence. As the internals of existing deep learning system are complicated, e.g., TensorFlow has more than 650 thousand lines of codes (LoC) and complex algorithms, it takes us great engineering effort to implement the incrementally code execution design compatible and efficient for model inference with these existing systems.

We deployed DeepShark on a Samsung S5 smartphone as study case. On this basis, four most popular convolutional neural network (CNN) models (i.e., VGG, CaffeNet, GoogLeNet and AlexNet), that are originally unaffordable on smartphone, now can be carried out efficiently on mobile devices by using DeepShark. The evaluation results show that, in most cases, DeepShark only uses less than 300 MB RAM of smartphone, and can achieve an average 70 percent of memory consumption reduction for one-time trial image recognition. Compared to existing mobile deep learning system using compressed models, DeepShark can employ the sophisticated deep-inference without any accuracy loss, thus provide higher learning quality and offer more adaptive trade-offs between time and memory-usage efficiency. Moreover, DeepShark only costs as little as 0.2 percent energy, which is preferable for mobile users.

In summary, this paper makes following contributions:

A novel platform DeepShark is designed to enable high-quality deep learning on COTS mobile devices. The existing deep learning inference can be applied directly without accuracy loss and no user-related data uploading is needed. A series of lightweight methods are adopted to deal with potential operational issues such as automatically collecting garbage.   
DeepShark is now implemented as a platform with easily accessed API library. Facing practical issues across compatibility for diverse deep learning tools, we have made great effort to customize two sets of API toolkit for Caffe and TensorFlow. In addition, we also investigate the possibility of building Deep-Shark into Android as a static library for efficient API access.

![](images/b3e49c8705febeddaf618d32dd7f24af22fa0d74f5b4557086aebba166653c97.jpg)



Fig. 2. Memory used to perceive different inference accuracy with 3 famous deep models using TensorFlow.

DeepShark is deployed atop a variety of mainstream Android devices to comprehensively evaluate the system design. The evaluation results with four most popular deep learning models show the optimized resource overheads (70 percent of memory usage reduction) and great energy efficiency of our platform. It also benefits user with more flexible resource allocation opportunity if they would like to trade off time and memory-usage efficiency.

The rest of this paper is organized as follows. Section 2.1 identifies the challenges. Aiming for goals in Section 3, Section 4 presents system design and technical details in DeepShark. The deployment and evaluation are in Section 5, and discuss the extensibility of the system which might interest readers is in Section 6. Section 7 surveys the related studies and Section 8 concludes the work.

# 2 MOTIVATION AND CHALLENGES

This section analyzes the problems in existing mobile uses of deep learning and the challenges of our work.

# 2.1 Motivation

Deep learning system has achieved significant success in many application areas, e.g., image and speech recognition. Fig. 1 shows a convolutional neural network based deep learning procedure. Here, the CNN model is consists of multiple layers with over thousands of parameters. By going through all layers, raw input features (e.g., pixels of images) are converted into high-level features used for tasks such as classification [12]. Thus, both training and inference of neural network require great computing effort.

Though a significant amount of work, e.g., [1], [13], [14], have developed high quality deep learning systems that can scale to large models and datasets, there are usually limited performance on mobile devices. First, mobile devices usually are with constrained resource thus can only support lightweighted deep learning computation. For example, Fig. 2 explores the relationship of memory consumed to a specific quality (i.e., accuracy) of deep learning performance with three default TensorFlow models. We see the process of VGG deep learning model can consume over 3 GB memory, which reaches out of most popular mobile memory capacity. Second, today’s deep learning systems often require massive size of data for model training. However, such requirement is largely missing in practice as the limited storage space on mobile devices. To name a few, the size of imageNet 2012 training (resp. inference) dataset reaches 138 GB (resp. 13 GB) which might be far away from most COTS mobile devices’ storage capability. Third, there has very limited supports for flexibly resource allocation control on mobile devices particularly that are of different constrained resource. Last, Fig. 3 shows TensorFlow’s [15] real-time (in milliseconds) memory consumed to conduct a VGG model inference along different size of image sets. We see a significant memory consumption increase from 2.8 to 28.5 GB, which makes it challenging to obtain high performance deep learning on mobile devices locally. Thus, to obtain high quality deep learning services, users have to upload data (e.g., images and motion data) to cloud for collaborative computing [16]. Moreover, mobile users nowadays demand more adaptive and flexible tradeoffs so that they can decide if they want time efficiency or memory-usage efficiency [17].

![](images/40114f438eba30859622033a02bd3a2c0f7e49f49482db79c2bcc51062c8623f.jpg)



![](images/e2beb45f1814176157ec0cc94fe9ee523a6ee0c9521254e2eadc3a0ad095da98.jpg)



![](images/0c3c9ca7c307077624dd9727d8516579dc38dec87f1dd64d37473e4bf23c0672.jpg)



![](images/88a52bacb27a21708725e95144e55824ca2bdc32450cf6c060d259660bd27318.jpg)



![](images/34de6887aa21922c747c80d9ec72c8de58abdb9ec768ddbd7df21cd152ea4007.jpg)



Fig. 3. Memory used to different image batch size of deep-inference (default VGG-16 model) on TensorFlow.

# 2.2 Challenges and Practical Issues

We begin by studying the memory consumption on existing deep learning systems with different models, we begin by exploring their performance on COTS smartphones. Table 1 shows our measurement results of the memory usage for OS services and applications, and the rest available space atop 12 popular Android smartphones [18]. It depicts that most smartphones have less than 1.2 GB free space for third-party applications. Considering the measurement in Fig. 3, here it remains a great technical challenge to achieve the high quality (with default accuracy) deep learning on these smartphone with such limited resource, e.g., less than 1 GB of memory. In fact, the above resource-hungry issues are not these-phone-only. Even without further power measurement, we see the same behaviors of most other smartphones, e.g., iPhone 7, in using the same mobile apps. By checking their resource manager, we conclude that mobile devices today generally face the same resource-hungry: they can not afford high performance deep learning locally.

To address this challenge and enable DeepShark system implementation on smartphone, there needs to first answer the following questions:

1) How to reduce memory consumed to deep learning but keep a high performance?

As it is difficult to relieve the memory consumption from a very large amount to a smartphone affordable level (e.g., less than 1 GB). To achieve this, (i) we propose to break

TABLE 1 Memory Usage of 12 Android Smartphones 

<table><tr><td>Phone</td><td> $Sys.^{\dagger}$ </td><td>Free</td><td>Phone</td><td> $Sys.^{\dagger}$ </td><td>Free</td></tr><tr><td>Galaxy S6</td><td>2.1 GB</td><td>461 MB</td><td>OnePlus3</td><td>2.7 GB</td><td>3.3 GB</td></tr><tr><td>Asus Zenfone3</td><td>2.9 GB</td><td>940 MB</td><td>LG G3</td><td>1.2 GB</td><td>652 MB</td></tr><tr><td>Galaxy Note5</td><td>2.1 GB</td><td>548 MB</td><td>Nexus6P</td><td>1.8 GB</td><td>1.2 GB</td></tr><tr><td>Galaxy S7edge</td><td>2.4 GB</td><td>1.1 GB</td><td>Galaxy S7</td><td>2.4 GB</td><td>1.1 GB</td></tr><tr><td>Huawei Mate8</td><td>2.2 GB</td><td>637 MB</td><td>LeEco2</td><td>2.4 GB</td><td>1.1 GB</td></tr><tr><td>Redmi Note3</td><td>1.2 GB</td><td>689 MB</td><td>S5 LTE-A</td><td>1.4 GB</td><td>1.3 GB</td></tr></table>

y Used for either Android system services or pre-installed apps.

down a deep model into several code blocks. Afterwards, the inference of deep learning can be conducted by incrementally loading each code block from storage to RAM, and last processed on SoC. Moreover, (ii) we can remove code blocks that are not in use from memory to clear more space. By such mechanism, as Fig. 14 demonstrates, for all models, 90 percent of their code blocks are less than 501 KB in Caffe uses and 1 MB in TensorFlow uses. In few cases, the code block size can reach up to 500 MB. It shows the significance of the incremental code execution strategy.

Toward models implemented with existing deep learning tools, e.g, Caffe and TensorFlow, it requires great effort to properly break down the model and optimize the incremental code execution. Indeed, we went through all the source codes and algorithms of each learning tool, which is strenuous but with wonderful effect. Thus, we understand the internal of those tools, and then design a memory collection component to load a specific code block into memory but excluding others. By now, two memory collection components are implemented for Caffe and TensorFlow respectively. Over time, we are going to provide more memory collection support for other learning tools, e.g., MXNet.

2) How to support diverse deep learning tools and models with DeepShark platform?

There are diverse deep learning tools and models for various applications. Thus, in designing DeepShark, it is crucial to ensure the compatibility across tools and models, and transplanting different tools to our platform for general uses is non-trivial. To this end, we try to customize different sets of API libraries that are implemented in C, Java and Python and coupled with different tools’ source code. Then, DeepShark can be built as a static library for mobile OS, and thus any applications/tools can work with it by calling the customized system service.

3) How to offer adaptive trade-offs so that user can decide if they want time efficiency or memory-usage efficiency?

DeepShark provides a high-level abstraction (as Fig. 4 shows) interface of determining how trade-offs should be made in according to user pre-defined policies. The policies are consist of user behavior rules. Thus, in the current design, a policy is an ordered list of rules specifying what a trade-off is between time efficiency and memory-usage efficiency, e.g., “using no more than 800 MB RAM and multithreads (if applicable) to carry out VGG model inference with TensorFlow”. The DeepShark Manager then applies it to the whole process in according to the rules.

![](images/304abc228a3716c8ed2bdc5ddc2f594b304e385a21331dae85ea4919fcde0705.jpg)



Fig. 4. Brief architecture of DeepShark: Advanced deep learning tools (top) interact with the the API to underlying DeepShark manager (middle) that applies pre-trained model by loading from storage (bottom).

TABLE 2 Selected DeepShark API Functions in Our Developed Library 

<table><tr><td>API Functions</td><td>Description</td></tr><tr><td>public STATUS_ID MemUnit::setMemStatic()</td><td>Staticize block of memory, and returns a status code.</td></tr><tr><td>public STATUS_ID MemUnit::setMemActive(bool delete_cache)</td><td>Activate the current memory block, the incoming parameter determines whether to delete the cache and returns a status code.</td></tr><tr><td>public static STATUS_ID MemUnit::setMemCacheSize(size_t size)</td><td>Update the memory cache size.</td></tr><tr><td>public static STATUS_ID MemUnit::setLocalCacheSize(size_t size)</td><td>Update the local storage cache size.</td></tr><tr><td>public static STATUS_ID MemUnit::doGarbageCollection()</td><td>Staticizes the current memory block and returns the status code.</td></tr><tr><td>private bool MemUnit::isActive()</td><td>Check whether the current memory block is active, then return a boolean value.</td></tr><tr><td>private void MemUnit::setCacheObj(int obj_id)</td><td>Change cache path of the incoming object.</td></tr></table>

# 3 GOALS OF DEEPSHARK

DeepShark implements a platform to achieve flexible resource allocation in mobile deep learning systems with a focus on resource constrained scenarios. By incrementally executing code of deep learning with user-specific trade-offs, DeepShark aims to achieve benefits of no accuracy loss, few resource requirements and high extensibility for mobile users. Specifically, we elaborate them as follows.

(1) No Accuracy Loss. As aforementioned, large deep learning models can achieve high quality performance, i.e., high accuracy, but can often reach out of mobile memory capacity. Existing systems using compressed models to mitigate resource constraints but suffers from a loss of accuracy (about 10 percent) [7]. Contrastively, DeepShark targets at adopting large model directly with no accuracy loss even if the resource is limited available.   
(2) Low Resource Requirement. For low-energy, highly portable SoC that lacks GPU and has only less than 1 GB size of available (free) RAM (Table 1), DeepShark proposes to incrementally load the input-to-execute code blocks to make the large model execution feasible. Thus, the memory usage is optimized and the energy cost is minimized.   
(3) Extensibility. DeepShark aims to build an extensible platform that does not require large-scale code rewriting for any applications. DeepShark also provides easily accessed API library (Table 2), thus researchers/developers can simply execute deep learning process on smartphones through calling the

APIs. In addition, DeepShark also targets at offering adaptive trade-offs for users to decide if they want time efficiency or memory-usage efficiency.

Note that this paper does not target at any deep model training on smartphone. In practice, the training process is usually the most time consuming and computationally demanding task. In our experimental experience, it can take up to 78 hours to train CaffeNet model [19] with ImageNet Large Scale Visual Recognition Competition (ILSVRC) 2012 dataset (Section 5.1.1) [20] on a four Pascal architecture GTX 1080 GPUs equipped machine that we used in this paper. Today, most sophisticated deep learning models are pre-trained for commercial use. Thus, DeepShark focuses on the inference (testing) steps over mobile devices with pre-trained models, which was supposed to bring rich applications to users, but actually suffers from mobile resource constraints.

# 4 DEEPSHARK SYSTEM

This section presents design space of DeepShark.

# 4.1 Platform Architecture

Fig. 4 shows the overview of DeepShark’s architecture. It works as a toolkit for mobile deep learning systems. The inference of a deep learning model, applications and tools can interact with DeepShark through calling APIs, asking for incrementally loading code blocks in according to the principle of memory collection. Specifically, our system consists of the following components.

API Library. This implements the access interfaces and should be customized for every deep learning tools, e.g., Caffe and TensorFlow. In practice, the APIs often need to be compatible with application’s source code. For example, it calls the SyncedMemory class in Caffe case; but turns to the Tensor class when in TensorFlow case. DeepShark provides both Public and Private APIs to address efficient deep learning using a standard suite of tools (Table 2).

DeepShark Manager. The manager maintains a range of device-wide or user-specific available resources. For the former, DeepShark manager reads available memory space through “/proc/meminfo” command; while for the latter, user can determine the available memory and thus trade off time efficiency and memory-usage efficiency. Then, Deep-Shark efficiently dispatches processing tasks with available memory space, and coordinates deep learning process from integrated model to meet the target of incrementally code execution on SoC. With such manager, DeepShark can resource-efficientlly carry out the deep learning inference with pre-trained model. Specifically, with our design, memory requests from applications can be maintained (clean and collect) since we periodically check whether there is out-of-use memory space.

![](images/e29f1f0c8881ef6548e5eb8dc6f1a62721a6cd3b5c7b790e454c7536dbc7d912.jpg)



Fig. 5. An example workflow of the main execution in inference of deep model with DeepShark.

Cloud Server (Storage). The cloud server is used to pretrain deep neural network models, store the pre-trained results, and all referred image dataset in the training processes. In this paper, we deployed it on an NVIDIA DevBox machine [21], which has 4 GTX 1080 GPUs for both pretraining and caching deep neural network models.

# 4.2 Main Execution of Deep Model Inference

We now describe how DeepShark conduct deep model inference by elaborating on its main execution. In fact, with Android Java Native Interface (JNI) library [22], DeepShark demands no super-user (i.e., ROOT) privileges and can perfectly run atop application layer. It works between deep learning tools and SoC (which includes RAM). Fig. 5 shows the major steps for carrying out the main execution of Deep-Shark deep learning. Specifically, DeepShark overloads default system functions , which means there are no difference of API calling between existing methods, e.g., Tensor-Flow Android Inferences, and DeepShark. Thus, deep models, including neural network parameters and learning functions, are incrementally loaded from local/cloud storage and executed with the same APIs. Afterwards, the DeepShark manager invokes a set of calling methods as: (1) using memory request function, e.g., malloc() or new object(), to find available memory block and make them to be available by using setMemStatic() function. Then, (2) a setMemActive() method is called for (3) initialize memory block to cache data. Note that, if the loaded data is out of applied memory, a setMemCacheSize() method would be immediately invoked for memory request. Next, (4) input-to-execute codes (e.g., tensors and blobs) are copied to memory; and thus (5) which further be processed as input to SoC. Finally, (6) the manager calls garbage collection, which is also based on setMemStatic() function, to collect out-of-use memory.

![](images/36f90668dbcff47148269abdccc7a11558fa700ee7be9b24a467f4399431b4a2.jpg)



Fig. 6. Comparison of original deep learning execution and DeepShark’s incrementally code exection.

In practice, DeepShark’s implementation further solves the following technical issues: a) an optimization algorithm for memory management, b) a function to incrementally load input-to-execute codes and c) garbage collection.

# 4.3 Incrementally Function Execution by Code Blocks

To generate input-to-execute functions (the in Algo-Frithm 1) for DeepShark, it is important to study the internal of deep learning tools. This section takes TensorFlow as an example, while the mechanism can also work with other frameworks, which needs extra engineering efforts.

Algorithm 1. Heuristic Trade-Off Scheme   
Input: (1) a ranked linked list $\mathcal{F}$ of referred functions; (2) a DCG graph $G = (V,E)$ ; (3) manual-tuned threshold $\mathcal{L}$ .

Output: a final target set $\mathcal{S}$ of selected optimizing code blocks. $\mathcal{S} \leftarrow \phi$ $f \leftarrow \text{HEAD}(\mathcal{F})$ while $f \neq NULL$ do

    // Step 1

    if $f \notin \mathcal{S}$ and $f$ is not called by any functions in $\mathcal{S}$ then

    // Step 2 $T_f \leftarrow$ total execution time of the $f$ deep inference $I_f \leftarrow$ total data size of I/O in the $f$ deep inference

    if $\frac{I_f}{T_f} < \mathcal{L}$ then $\mathcal{S} \leftarrow \mathcal{S} + \{f\}$ // Step 3

    foreach $v \in V$ do

    if $e: v \xrightarrow{p} f \in E$ or $e: f \xrightarrow{p} v \in E$ then

    if $\sum_{i=0}^{n} p_i \leq P$ and $v \notin \mathcal{S}$ and $v$ is not called by any functions in $\mathcal{S}$ then $T_v \leftarrow$ total execution time of $v$ $I_v \leftarrow$ total data size of I/O in $v$ if $\frac{I_v}{T_v} < \mathcal{L}$ then $\mathcal{S} \leftarrow \mathcal{S} + \{v\}$ $f \leftarrow f \to next$ return $\mathcal{S}$

TensorFlow assembles the parameter data [23] of deep models into functions for inference. Specifically, the parameter data of TensorFlow consists of tensors [14], which are referred to the graph code and weight values. For example, as Fig. 6 illustrates, TensorFlow extracts the graph codes $( \mathrm { i . e . , ~ } f _ { i } )$ and weights (the Pi) from every tensor unit, and then loads them into the memory sequently. This is the most basic but crucial preliminaries for generating input-toexecute code block of deep learning inference (e.g., the T in Fig. 6) because TensorFlow consumes a mass of mobile memory resource, and thus lead to the resource constraint scenarios before all inference are finished. By studying the internals of deep learning inference, we find that only very a few of the tensors are required to support each convolutional operation inference or pooling operation inference [23]. Thus, DeepShark works through extracting tensors that referred by neural network operations instantaneously as the input-to-execute code block, which can not only keep the efficiency of learning process but also relieve resource overheads. In practice, DeepShark first records the key data, e.g., neural network size, neural network type and neural network parameters, of the generated tensors by overwriting the TensorFlow::DataManager::Record-Node() function. Then it staticizes all tensors to external storage, e.g., disk or cloud, by revising the API and thus only loads referred tensors into memory as code block. Finally, DeepShark calls the DeepShark::Allocator() (which overrides the TensorFlow::Allocator() class) to free out-of-use code block and load new ones for a next process. Indeed, DeepShark caches all tensors in the external storage to avoid parameters missing. Afterwards, Deep-Shark shifts the default deep learning inference principle from loading the multi-codes to only a single function with referred parameters. By doing this, the deep model inference on SoC is processed in an incremental process method.

# 4.4 Trade-Off Strategy with User-Specific Policy

This section details the trade-off scheme with user policy (in RAM limit), which utilizes profiling to select input-to-execute functions as incrementally executing targets as Section 4.3 depicts. To simplify the selection, given a function is selected as a target, all of its callee code blocks (v) would also be selected for optimization. DeepShark constructs a directed data communication graph (DCG), i.e., G V; E , to facilitate the selection. Each node $v \in V$ ¼ ð Þindicates every 2  input-to-execute code block, and an edge $e : v _ { 0 } { \overset { n } { \longrightarrow } } v _ { 1 } \in { \dot { E } }$ connects the code blocks $v _ { 0 }$ and $v _ { 1 }$ ! 2when there are p memory pages produced in $v _ { 0 }$ and accessed in $v _ { 1 }$ at runtime. Thus, if $v _ { 1 }$ is selected and fetched by the client and v will do the same, size of their whole memory pages $\textstyle \sum _ { i = 0 } ^ { n } p _ { i }$ now need ¼ to be counted on the client side till allocated RAM $( P ,$ preset by user policy) is exhausted. The initial target set is picked up by the logic of deep model, $\mathrm { i . e . }$ , the neural architecture including its callee functions. Then, Algorithm 1 shows the trade-off scheme in a heuristic manner. The input $\mathcal { F }$ is the ranked list of code block functions in the deep Fmodel on the calling logic. The output is the final selected target set. Each target function $f \in { \mathcal { F } }$ Swill entry three steps.

2 FIn the first step, DeepShark checks if $f _ { 0 }$ has been included in ${ \mathcal { S } } ,$ or called during the execution of any inference process Sin . If yes, DeepShark skips $f _ { 0 }$ and goes to the next target $f _ { 1 }$ Sin . Otherwise, it moves to the second step.

FIn the second step, DeepShark examines the I/O operations in f (including its callee functions) to seek if they are excessive in f with a manual-tuned threshold $\mathcal { L } \left( \mathcal { L } = 0 . 0 5 \right.$ in L L ¼this paper). If they are not excessive, f is included into $s$ and moves to the third step.

In the third step, DeepShark traverses each node $v \in V$ in G which is also connected with $f ,$ namely, $e : v { \overset { p } { \longrightarrow } } f \in E$ or $e : f { \overset { p } { \to } } v \in E$ . If the value of $\textstyle \sum _ { i = 0 } ^ { n } p _ { i }$ ! 2  is large than the avail-! 2able RAM limit $P ,$ ¼it indicates that function v should not be selected together with f to reduce potential RAM overfitting. Indeed, DeepShark also examines the I/O operations in v to further check if it works for selection. If yes, v would be included into . The selection process iterates until all of Sthe functions are examined.

# 4.5 Memory Management

# 4.5.1 Methodology

The aforementioned methodology of memory optimization is to collect out-of-use memory blocks that occupied by redundant codes as many as possible. In modern compiler principle, each code statement holds a pointer \*p which points to a specific memory block. The memory block can be used by a learning process or thread before the pointer \*p ending its life cycle. Thus, we can temporarily move the data in the memory block to external storage for resource optimization purpose. Algorithm 2 shows the pseudocode of the memory collection design. Specifically, the algorithm implementation is strenuous as it requires to make the memory management be coupled with existing tool’s source codes, and for that we have analyzed all the principle and design details of each tool. As study case, the rest of this section presents the customized implementation of memory management for Caffe and TensorFlow frameworks.

Algorithm 2. Memory Block Collection   
```cpp
foreach received pointer *p from memory do
    if MemUnit::isActive() is false then
    *p = MemUnit::setMemActive();
    MemUnit::setCachObj(*p);
    repeat
    read data;
    until size_of(*p) > data_size;
    if size_of(free cache) < max_size then
    MemUnit::setMemStatic();
    return true; 
```

# 4.5.2 Caffe Implementation

In this case, the memory management is implemented through the setMemStatic function:

```cpp
void SyncedMemory::setMemStatic() {
    if (!found_memId(memId)) return;
    synced_mem_mutex.lock();
    check_memId();
    if (!isStatic(memId)) {
    cpu_ptr_ = get_ptr(memId);
    setCacheObj(cpu_ptr_, get_filename(memId), size_);
    CaffeFreeHost(cpu_ptr_, cpu_malloc_use_cuda_, size_);
    make_static_bool(memId, true);
    }
    synced_mem_mutex.unlock();
} 
```

Note that, in our experience, the pointer used in Caffe are confusing, which requires additional lock functions to achieve the optimization.

# 4.5.3 TensorFlow Implementation

In this case, the memory management is implemented as:

```cpp
template <typename T>
void Buffer<T>::setMemStatic() const{
    if (!deepshark::is_static.count(memId)) {
    setCacheObj(data_, get_filename(memId), size())
    alloc_->Deallocate<T>(data_, elem_);
    data_ = nullptr;
    deepshark::is_static.erase(memId);
    }
} 
```

Now, DeepShark can use this interface to manually free memory space by checking every memory block ID, or delegate it to the garbage collection mechanism.

# 4.6 Garbage Collection

The inference of pre-trained models as described so far usually generates garbage [24]. Indeed, some of the obtained data will be out-of-use before the next calling. Thus, it can be cleared for saving memory space. To achieve this, Deep-Shark designs a garbage collection mechanism which can be either manually triggered by calling the doGarbageCollection() interface, or automatically invoked once a normal garbage collection has failed to free enough memory and the OS kernel is about to signal it is out of memory. Comparing to use setMemStatic() function in Section 4.5, the garbage collection interface does not require developer to provide the target memory ID and thus makes DeepShark to be more easy to use.

# 4.7 Analysis of the I/O Costs

To shape DeepShark’s I/O efficiency, this section analyzes it with a classic I/O model provided by [25]. Specifically, the I/O cost of a process is the number of block transfers from storage to memory. The complexity can be parameterized by the size (we denote as B) of memory block transfer, and stated in the unit of the data, i.e., each incrementally load code segment of deep model. An upper bound on the number of block transfers can be analyzed by considering the total size of data accessed divided by B, and then adding to this the number of non-sequential seeks. Given the total data size is N , as every data is cached only one time. To j jsimplify the analysis, we assume that N consists of multij jple B, and shards have equal sizes N . Given $Q _ { B } ( N )$ is the j j ð ÞI/O cost, we can find that it is almost linear in N =B, which j jis optimal because all data need to be accessed. In addition, since each data is accessed twice during one full pass over the deep learning algorithm. If both endpoints of a data transfer belong to the same layer, the data is read only once from storage; otherwise, it is read twice. In the common case, DeepShark requires M non-sequential disk seeks to load the data block from the M 1 data transfer for an exe-cution interval. Thus, the total number of non-sequential seeks has a cost of Q M2 . In practice, the number can be ð Þnot exact as the size of the data are generally not multiples of B. Given there is sufficient memory to cache all data for an execution interval a time, the I/O complexity can be bounded as: $\begin{array} { r } { \frac { 2 | N | } { B } \leq Q _ { B } ( N ) \leq \frac { 4 | N | } { B } + \Theta ( M ^ { 2 } ) } \end{array}$ As the number of

TABLE 3 Experiment Deep Models 

<table><tr><td>Image Dataset</td><td>ILSVRC2012</td><td>Source</td><td>[20]</td></tr><tr><td>Model</td><td>Source</td><td>Model</td><td>Source</td></tr><tr><td>VGG</td><td>[26]</td><td>CaffeNet</td><td>[19]</td></tr><tr><td>GoogLeNet</td><td>[27]</td><td>AlexNet</td><td>[28]</td></tr></table>

Pre-training with image dataset was done on NVIDIA DevBox.

non-sequential disk seeks are proportional to Q M2 , onerous I/O request will bring high latency.

# 4.8 Code Implementation

DeepShark provides mobile users with an optimal inference for state-of-the-art deep learning algorithms and a collection of reference models. We consider the platform to be a BSD-licensed static library with C, Java and Python APIs for running deep models efficiently on smartphone. By now, our Android based implementation consists of 3,800 lines of C code, 350 lines of Java code and 420 lines of Python code, including the libraries for Caffe and TensorFlow, the DeepShark manager and its upper layer interface. Up to now, it powers CNN (e.g., VGG), deep neural network (DNN), e.g., WaveNet, and recurrent neural network (RNN), e.g., SyntaxNet, deep learning models in vision, speech, and multimedia.

To study whether our code implementation can work on COTS smartphones, we have experimented it on Google Nexus 6 and 6P, Samsung Galaxy S4, S5 LTE-A, S7 edge and OnePlus3 smartphones that all have more than 1 GB free RAM and runs Android 4.0+.

# 5 EVALUATION

This section systematically summarizes results from a number of experiments to highlight the main benefits of Deep-Shark presented above, and present the comparison against existing system. Finally, this section is closed by analyzing overheads and the I/O latency.

# 5.1 Experimental Setup

# 5.1.1 Public Available Dataset and Deep Models

Ethics. Our experimental evaluations are mainly of image recognition tasks. Specifically, we consider a large publicly available image datasets from ImageNet web site, i.e., ILSVRC2012, which contains 10 million labeled images depicting over 10,000 object categories as training. For deep models, we take four most popular and publicly available CNN model as metrics: (1) VGG (the VGG team in the ILSVRC-2012 competition), (2) the CaffeNet (imageNet), (3) the GoogLeNet and (4) the AlexNet. Table 3 summarizes source link of both image dataset and deep models.

# 5.1.2 Hardware

As a study case, most of the experiments were performed on a Samsung Galaxy S5 LTE-A smartphone, with Snapdragon 805 SoC and 3GB memory. In practice, we can obtain similar experimental results of other smartphones.

Indeed, it is possible to measure a smartphone’s power by interposing Android BatteryInfo interfaces, however, today’s mobile devices often provide no way to obtain fine-grained energy measurements of any apps. In this paper, to precisely measure devices’ energy cost, we attach a hardware power meter [29] to the Samsung Galaxy S5 LTE-A smartphone with hijacked battery (as Fig. 7 shows) that provide the same performance as the normal battery to ensure valid evaluations in our work. Instead, they simply offers users an integer, e.g., “how much battery (in %) remains”, which is coarse-grained and usually unreliable. In addition, this power meter provides fine-grained measurements as it samples the current drawn from the battery with a frequency of 5 KHz and a mean error of less than 3 percent [29].

![](images/21f40a79a37fdc63c4912674c78c9b7f42f0ca1b54f9d3489be284e4d92ca2a9.jpg)



Fig. 7. The battery interface carved out from S5 LTE-A.

All experiments have pre-trained all models on an NVI-DIA DevBox [21]. As shown in Fig. 8, it has 4 GTX 1,080 GPUs with 8 GB of GDDR5X memory per GPU, 64 GB of main memory and a standard 512 GB NVMe SSD drive as well as three 7,200 rpm 3TB SATA 6 Gbps 3.5 hard drive in RAID5, and runs standard Ubuntu 14.04 LTS with factory settings. Filesystem caching was disabled to make executions with small and large input deep models comparable. For downloading data, we connect smartphone with DevBox in LAN through a Google OnHub AP with 1.1 Gbps bandwidth under 802.11ac channel. Moreover, to compare DeepShark with a distributed server performance, we also runs original Caffe and TensorFlow on DevBox. In a word, all the pre-training process are carried by the 4 GPUs, but all the experimental evaluations are executed on smartphone’s SoC or DevBox’s CPU (as comparison).

# 5.2 Scalability and Performance

This section exams whether DeepShark can conduct deep learning model inference with a performance of loss-free accuracy under resource constraints. For each experiment, at least 30 tests are conducted with persistent process. Table 4 shows the balanced performance of one-time trial image recognition process over S5 LTE-A’s SoC with two deep learning tools, i.e., Caffe and TensorFlow, to four representative test models. Comparatively, we also conduct original deep model inference on NVIDIA DevBox with an Intel i7-5930K CPU.

![](images/5dd798d0f483cc1afd6b39c88a7e6ab632e3b4a4bc43a07c019510e62e226a1e.jpg)



Fig. 8. NVIDIA DevBox for models’ pre-training.

# 5.2.1 Performance of One-Time Trial Inference

We first measure memory usage and wallclock time of single image recognition by using 4 popular CNN models as input metrics. The architecture and accuracy of each model studied in this work are all shown in Table 4. In addition, it also summarizes the geometric mean results of all the metrics. We can find a significant memory saving performance powered by DeepShark. In contrast to the original processes on DevBox, it on average benefits users with 500 MB+ memory reduction (which is 70 percent decrease than original performance), and even 2.4 GB decrease, to execute Caffe and TensorFlow tasks. Experimental results also show that all memory consumption are less than 300 MB in using Caffe, which, as analyzed before (Table 1), can be applied to most lower resource smartphones. We also explore the superior optimization performance to different deep tools. For example, DeepShark can reduce the memory use of Caffe VGG by a factor of 90 percent (1.7 GB), and achieve 92 percent (2.4 GB) for TensorFlow.

Table 4 also explores the time cost of each image recognition.1 By incremental inference of pre-trained model, Deep-Shark can process all code block executions in a very reasonable time. In most cases, it on average uses 51 seconds to conduct the Caffe’s image recognition inference; while a little more time of 3.5 minutes to process the TensorFlow deep learning computation.

Taken together, we summarize that DeepShark can provide high quality mobile experience for advanced deep learning. Moreover, the resource overheads of the whole process are affordable to most existing smartphones.

# 5.2.2 Performance of Large-scale Inference

Next, this section explores DeepShark in handling largescale learning computation. Similar to Section 5.2.1, we also evaluate the performance of memory usage and time consumption, but now it take a 1,000 batch size image recognition. By again using the four deep models and two deep tools as metrics, Fig. 9 shows peak values of memory usage in all computations. It shows that DeepShark has almost the same performance as in single image recognition above.

To further explore the time consumption of large-scale deep learning workload, we carry out latency measurements and plot the results in Fig. 10. We can see that Deep-Shark might take more time when comparing with original learning on powerful machine, i.e., DevBox. For example, in AlexNet experiments, the results indicate that Caffe uses 10 hours and TensorFlow costs 47 hours. As a result, it exhibits a factor of 64X time increase than original on DevBox, and indicates the inapplicability of DeepShark when the inference meets very large size of high quality deep learning. However, most mobile device uses of deep learning are applied with just a few (less than 10) requests, thus, Deep-Shark system can benefit real-life mobile users.

TABLE 4 Comparative Performance of High Quality Deep Model Inference on NVIDIA DevBox and Samsung Galaxy S5 LTE-A Phone to Execute One-Time Trial Image Recognition 

<table><tr><td>Application &amp; Model</td><td>Acc.</td><td>Para.</td><td>Architecture</td><td>Comparative result◇</td><td>DeepShark (S5 LTE-A)</td></tr><tr><td>Caffe &amp; CaffeNet</td><td>81.3%</td><td>60.95 M</td><td>c:5 +; p:3‡; fc:3 *</td><td>RAM: 776 MB; Time: 510 ms</td><td>RAM: 206 MB; Time: 39 s</td></tr><tr><td>Caffe &amp; GoogLeNet</td><td>89.2%</td><td>6.84 M</td><td>c:57 +; p:13‡; fc:1 *</td><td>RAM: 885 MB; Time: 930 ms</td><td>RAM: 271 MB; Time: 91 s</td></tr><tr><td>Caffe &amp; AlexNet</td><td>80.6%</td><td>60.95 M</td><td>c:5 +; p:3‡; fc:3 *</td><td>RAM: 805 MB; Time: 610 ms</td><td>RAM: 224 MB; Time: 27 s</td></tr><tr><td>Caffe &amp; VGG</td><td>90.2%</td><td>138.4 M</td><td>c:5 +; p:3‡; fc:3 *</td><td>RAM: 1.95 GB; Time: 2.67 s</td><td>RAM: 211 MB; Time: 47 s</td></tr><tr><td>TensorFlow &amp; CaffeNet</td><td>81.3%</td><td>60.95 M</td><td>c:5 +; p:3‡; fc:3 *</td><td>RAM: 1.2 GB; Time: 2.6 s</td><td>RAM: 525.75 MB; Time: 155 s</td></tr><tr><td>TensorFlow &amp; GoogLeNet</td><td>89.2%</td><td>6.84 M</td><td>c:57 +; p:13‡; fc:1 *</td><td>RAM: 260 MB; Time: 6.4 s</td><td>RAM: 80.72 MB; Time: 371 s</td></tr><tr><td>TensorFlow &amp; AlexNet</td><td>80.6%</td><td>60.95 M</td><td>c:5 +; p:3‡; fc:3 *</td><td>RAM: 1.2 GB; Time: 2.7 s</td><td>RAM: 536.32 MB; Time: 168 s</td></tr><tr><td>TensorFlow &amp; VGG</td><td>90.2%</td><td>138.4 M</td><td>c:5 +; p:3‡; fc:3 *</td><td>RAM: 2.7 GB; Time: 8.1 s</td><td>RAM: 538 MB; Time: 141 s</td></tr></table>

on NVIDIA DevBox with 64GB RAM in total; þ convolution layers; z pooling layers; ? fully connected layers.

# 5.2.3 Adaptive Trade-Offs between Time and Memory-Usage

DeepShark towards an adaptive trade-off between time and memory-usage efficiency. To this end, it allows user to set up a memory capacity for executing deep learning inference only. In practice, such diverse flexible trade-offs can be discrete as existing deep neural network parameters, e.g., Caffe blobs and TensorFlow tensors, have a basic file size, which is actually determined by the adopted neural network architecture. For example, Caffe requires at least 144 MB memory capacity to conduct a VGG inference and TensorFlow requires at least 295 MB memory capacity for the same process. To conduct our knowledge under this scenario, by fitting curves with measurement results, Fig. 11 measures the time efficiency performance along different memory-usage from 144 to 297 MB (for DeepShark on Caffe) and from 295 to 475 MB (for DeepShark on TensorFlow). We observe that by enabling more memory capacity for a VGG model inference, e.g, allowing 180 and 260 MB memory capacity respectively, DeepShark with Caffe can provide more flexible trade-offs for users to determine if they want time efficiency or memory-usage efficiency. Fig. 11 also shows a same performance in using DeepShark with Tensor-Flow. On the other hand, we see that the time usage in Fig. 11 exhibit sudden drops and a stepwise trend rather than a linear one as memory usage increases. This is because that the file size of parameters such as blob and tensor are discrete and loaded into memory by blocks. In practice, a parameter with small file size consumes fewer time than large file size parameters. The difference could be significant and thus lead to the sudden drop phenomenon.

![](images/94e22b16957fdd8862c815c1844532b0a14e4badde484db2652a348f6a398106.jpg)  
Fig. 9. Memory use of batch-size = 1000 image recognition by Deep-Shark and the original approach (DevBox).

![](images/53ffb4b9bda29b64eb9796f4094ac41ef3c59a1a564d30504303cad90f1a45ed.jpg)



Fig. 10. Time used to batch-size = 1000 inference with DeepShark to default.

Indeed, the 300 MB memory capacity limit in Caffe and VGG based experiments are still very strict as most popular smartphone nowadays can provide as much as 1 GB space to obtain higher time efficiency. Thus, when the memory capacity becomes larger, DeepShark will carry out deep learning inference to a fast mode, e.g., 407 s (295 MB) comparing to 31 s (475 MB) in the VGG and TensorFlow experiments.

# 5.3 Comparison to Existing Deep Learning Systems

We are not aware of any other system that can not only provide high quality deep learning inference as DeepShark on just a smartphone, but also offer adaptive trade-offs so that user can decide if they want time efficiency or memoryusage efficiency. To get flavor of the performance of our proposed system, this section compares performance among (i) DeepShark, (ii) existing cloud-based distributed deep learning system, e.g., DistBelief [1], SINGA [30] and DL4J on Spark [31], which utilizes cloud resource for processing default neural network models, and (iii) using compressed model on mobile devices, e.g., DeepMon [9], Paddle [10] and Caffe2, that only support a few neural networks for a specific tool. Table 5 and and Table 6 show the comparison results with 100+ repeatable experiments S5 LTE-A smartphone or the NVIDIA DevBox machine. As study case, we respectively employ compressed models, i.e., ResNet50, ResNet101, VGG-M-128, VGG-M-1024 and VGG-16, and default models, i.e., ResNet152, VGG-M-2048 and VGG-19 neural models, atop the mentioned three systems. Note that some neural network models might not be processed as tool incompatibility or resource insufficient. In addition, the accuracy of each deep model performs the same on the compatible deep learning system. For example, ResNet50 holds an accuracy of 93.3 percent on Paddle, DeepMon, Caffe2, DistBelief and DeepShark. Their significance and performance are evaluated with next three baselines.

![](images/c6e35bbef6624882bb5928783e4f5850c8ad8e3a23b8cfabb2dec2f63337ab24.jpg)



Fig. 11. Performance of adaptive trade-offs between time and memoryusage efficiency in VGG inference.

TABLE 5 Comparison Among Accuracy, Wallclock Time and Memory-Usage Efficiency of DeepShark and State-of-the-Art Systems on Mobile Device (S5 LTE-A for the Study Case) and on Cloud Server (NVIDIA DevBox) 

<table><tr><td rowspan="3" colspan="2">Category</td><td colspan="8">Wallclock time usage of whole deep inference/Memory consumed to execute the deep inference</td></tr><tr><td colspan="5">Compressed models (batch-size = 1)</td><td colspan="3">Default models (batch-size = 1)</td></tr><tr><td>ResNet50</td><td>ResNet101</td><td>VGG-M-128</td><td>VGG-M-1024</td><td>VGG-16</td><td>ResNet152</td><td>VGG-M-2048</td><td>VGG-19</td></tr><tr><td rowspan="3">Mobile only</td><td>Paddle</td><td>30.3 s/385 MB</td><td>56.7 s/585 MB</td><td>-</td><td>-</td><td> $\times_{sup}$ </td><td> $\times_{sup}$ </td><td> $-\times_{sup}$ </td><td> $\times_{sup}$ </td></tr><tr><td>DeepMon</td><td>-</td><td>-</td><td>33.5 s/1,324 MB</td><td>36.7 s/1,396 MB</td><td> $\times_{sup}$ </td><td> $-\times_{sup}$ </td><td> $\times_{sup}$ </td><td> $\times_{sup}$ </td></tr><tr><td>Caffe2</td><td>9.6 s/463 MB</td><td>17.3 s/734 MB</td><td>-</td><td>-</td><td> $\times_{sup}$ </td><td>23.0 s/995 MB</td><td>-</td><td>×</td></tr><tr><td rowspan="3">Using cloud</td><td>DistBelief</td><td>9.2 s/385 MB</td><td>10.0 s/585 MB</td><td>-</td><td>-</td><td>-</td><td>10.1 s/801 MB</td><td>-</td><td>-</td></tr><tr><td>SINGA</td><td>-</td><td>-</td><td>28.4 s/1,324 MB</td><td>30.0s/1,396 MB</td><td>-</td><td>-</td><td>31.2 s/1,477 MB</td><td>-</td></tr><tr><td>DL4J</td><td>-</td><td>-</td><td>-</td><td>-</td><td>49.6 s/2,195 MB</td><td>-</td><td>-</td><td>51.5 s/2,278 MB</td></tr><tr><td rowspan="5">Deep Shark</td><td>No limit</td><td>30.4 s/385 MB</td><td>56.8 s/585 MB</td><td>33.5 s/1,324MB</td><td>36.6 s/1,396 MB</td><td> $\times_{sup}$ </td><td>99.9 s/801 MB</td><td>40.8 s/1,477MB</td><td> $\times_{sup}$ </td></tr><tr><td>150 MB</td><td>40.0 s/150 MB</td><td>79.9 s/150 MB</td><td> $\times_{inf}$ (288 MB)</td><td> $\times_{inf}$ (288 MB)</td><td> $\times_{inf}$ (392 MB)</td><td>133.4 s/150 MB</td><td> $\times_{inf}$ (288 MB)</td><td> $\times_{inf}$ (392 MB)</td></tr><tr><td>300 MB</td><td>34.3 s/300 MB</td><td>71.7 s/300 MB</td><td>56.3 s/300 MB</td><td>63.8 s/297 MB</td><td> $\times_{inf}$ (392 MB)</td><td>123.3s/300 MB</td><td>69.8 s/297 MB</td><td> $\times_{inf}$ (392 MB)</td></tr><tr><td>500 MB</td><td>33.5 s/342 MB</td><td>62.8 s/500 MB</td><td>45.0 s/500 MB</td><td>48.4 s/500 MB</td><td>112.6s/500 MB</td><td>117.0s/500 MB</td><td>54.1 s/500 MB</td><td>114.9 s/500 MB</td></tr><tr><td>1 GB</td><td>33.5 s/342 MB</td><td>62.1 s/535 MB</td><td>36.3 s/526 MB</td><td>39.6 s/540 MB</td><td>90.3s/1 GB</td><td>107.6s/744 MB</td><td>44.0 s/564 MB</td><td>92.6 s/1 GB</td></tr></table>

The “-” indicates the neural network is not supported by the tools. The “ sup” indicates the available RAM is insufficient for deep inference and the $^ { \prime \prime } \times _ { i n f } ^ { } { } ^ { \prime \prime }$ indicates the allocated RAM space is less than the smallest memory usage for deep models.

Effectiveness of RAM Allocation. Table 5 depicts an interesting phenomenon that the memory usage of DeepShark could sometimes be less than the overall memory size for each deep model when the available RAM size is sufficient. For example, ResNet50 needs 385 MB memory with no RAM limit. Given a limit of memory resources (500 MB or 1 GB). However, the memory usage is only 342 MB rather than 385 MB. Similarly, as for VGG-M-128 or VGG-M-1024 model in 1 GB RAM limit. As a result, memory is not fully utilized. This is because, to carry out each deep inference with different models, DeepShark requires a smallest memory consumption (denoted in $\times _ { i n f }$ in Table 5) for the most basic operations. Given a scenario of $\times _ { i n f }$ is larger than the system allocated memory space (denoted in $\times _ { \mathit { s u p } } ) _ { . }$ , Deep-Shark cannot work under this situation. Meanwhile, each deep model holds a maximal memory use, when the allocated RAM space is larger than such maximal use, there appears a scenario of memory is not fully utilized. Indeed,

TABLE 6 Network Data Transmission Time within Experiments of Table 5 

<table><tr><td>Category</td><td></td><td>ResNet50</td><td>ResNet101</td><td>VGG-M-128</td><td>VGG-M-1024</td><td>VGG-16</td><td>ResNet152</td><td>VGG-M-2048</td><td>VGG-19</td></tr><tr><td rowspan="3">Mobile only</td><td>Paddle</td><td>4.1 s (13.5%)</td><td>6.4 s (11.3%)</td><td>-</td><td>-</td><td>×</td><td>×</td><td>- ×</td><td>×</td></tr><tr><td>DeepMon</td><td>-</td><td>-</td><td>12.4 s (37.0%)</td><td>12.7 s (34.6%)</td><td>×</td><td>- ×</td><td>×</td><td>×</td></tr><tr><td>Caffe2</td><td>4.2 s (43.8%)</td><td>7.4 s (42.9%)</td><td>-</td><td>-</td><td>×</td><td>9.2 s (39.9%)</td><td>-</td><td>×</td></tr><tr><td rowspan="3">Using cloud</td><td>DistBelief</td><td>3.7 s (40.2%)</td><td>6.8 s (68.0%)</td><td>-</td><td>-</td><td>-</td><td>8.9 s (88.1%)</td><td>-</td><td>-</td></tr><tr><td>SINGA</td><td>-</td><td>-</td><td>13.4 s (47.2%)</td><td>13.6 s (45.4%)</td><td>-</td><td>-</td><td>15.2 s (47.8%)</td><td>-</td></tr><tr><td>DL4J</td><td>-</td><td>-</td><td>-</td><td>-</td><td>20.3 s (40.9%)</td><td>-</td><td>-</td><td>20.0 s (38.9%)</td></tr><tr><td rowspan="5">DeepShark</td><td>No limit</td><td>3.6 s (11.8%)</td><td>7.3 s (12.9%)</td><td>11.4 s (34.1%)</td><td>14.2 s (38.8%)</td><td>×</td><td>8.7 s (8.7%)</td><td>14.7 s (36.1%)</td><td>×</td></tr><tr><td>150 MB</td><td>3.6 s (9.0%)</td><td>7.3 s (9.2%)</td><td>×</td><td>×</td><td>×</td><td>8.7 s (6.5%)</td><td>×</td><td>×</td></tr><tr><td>300 MB</td><td>3.6 s (10.5%)</td><td>7.3 s (10.2%)</td><td>11.4 s (20.2%)</td><td>14.2 s (22.3%)</td><td>×</td><td>8.7 s (7.1%)</td><td>14.7 s (21.1%)</td><td>×</td></tr><tr><td>500 MB</td><td>3.6 s (10.7%)</td><td>7.3 s (11.6%)</td><td>11.4 s (25.3%)</td><td>14.2 s (29.4%)</td><td>22.5 s (20.0%)</td><td>8.7 s (7.5%)</td><td>14.7 s (27.2%)</td><td>22.6 s (19.7%)</td></tr><tr><td>1 GB</td><td>3.6 s (10.7%)</td><td>7.3 s (11.8%)</td><td>11.4 s (31.4%)</td><td>14.2 s (35.9%)</td><td>22.5 s (24.9%)</td><td>8.7 s (8.1%)</td><td>14.7 s (33.4%)</td><td>22.6 s (24.5%)</td></tr></table>

Similarly, the “-” indicates the neural network is not supported by the tools. The “ ” indicates a resource insufficient scenario.

![](images/5bfafed09fdc3a73d6bb96996f34ea65d94a74a1a2950dd81b8d8b58238b2a30.jpg)  
Fig. 12. Data consumptions of testing process under Caffe and four deep models.

![](images/586a803fb1d20e49b92920cff580f8809f1c4076935f1e51a3dd9b0add6a36c4.jpg)  
Fig. 13. Data consumptions of testing process under TensorFlow and four deep models.

DeepShark is designed to seek the most balanced points between a deep inference’s smallest memory consumption and maximal memory use. As Table 5 explored.

Efficiency between Time and Memory Usage. Tables 5 and 6 compare the time for system processing (including deep inference, I/O cost and network communication), single data transmission time and memory-usage efficiency performance among all the baselines respectively. Table 5 shows the increase of time and RAM consumed to more complex neural networks for all the metrics and benchmarks. For example, all of the three deep learning systems use more time and memory space to execute inference with a VGG-M-1,024 model than a ResNet50 model. Specifically, with high-end server, cloud-based systems such as DistBelief can provide the most quick inference experience than using compressed models on mobile devices and Deep-Shark. Comparing to the resource constraint scenario, e.g., ResNet101 model inference on Paddle and DeepShark, there brings an acceptable performance gap (less than 1 minute). Moreover, DeepShark preserves the same time and memory-usage efficiency as existing mobile systems.

Trade-Offs between Time and Memory Usage. Table 5 also shows the significance of DeepShark than existing mobile system, i.e., enabling users to make trade-offs between time and memory usage. For instance, DeepShark allows mobile device to only consume 150 MB RAM to execute the ResNet50, ResNet101 and ResNet152 neural models, which can neither be supported by Paddle, DeepMon nor Caffe2 with such RAM limit. However, such benefits are obtained by sacrificing time efficiency, e.g., to finish a ResNet101 model inference, it costs DeepShark 79.7 s with 150 MB RAM limit but only 62.1 s if the RAM limit are set up to 1 GB, and further 56.8 s when there are no RAM bounds. All the mentioned results have included the time consumption for deep model transmission (7.3 s). Thus, DeepShark can provide more flexible experience than state-of-the-art systems in executing local deep learning inference.

Extensibility. DeepShark provides easy programmability to work with Caffe and TensorFlow. For example, the default VGG-M series models cannot work with Paddle system but can be handled by DeepShark efficiently. Note that in resource insufficient scenarios, e.g., VGG-16 model with 150 MB RAM limit, DeepShark would not be able to finish the process task till a higher resource limit is given. In fact, these benefits are coming with a cost of pre-modified API toolkits for diverse deep learning systems.

# 5.4 Data Usage

DeepShark consumes data quota from loading data from storage. Specifically, two category of storage: (i) deep models are cached in smartphone’s (local) storage; (ii) deep models are downloaded from cloud storage with WiFi or cellular network.

# 5.4.1 I/O Requests and Code Block Size

This section first compares the I/O requests and deep tool’s input-to-execute code block size with DeepShark’s system log. Figs. 12 and 13 depict the real-time package size (i.e., input-to-execute code blocks) of each I/O request with four neural network models (i.e., CaffeNet, GoogLeNet, AlexNet and VGG), on Caffe and TensorFlow. For this experiment, we monitor the data consumption on a Samsung S5 LTE-A device by reading the proc files with SyncedMemory:: cpu\_data() (for Caffe) and Tensorflow::Tensor:: data() interfaces once per times to request data package and monitor the data usage for DeepShark. We set the frequency of periodic measurements according to each data cap. On this basis, Fig. 14 summarizes all data in cumulative probability distribution (CDF). It depicts that over 90 percent of Caffe (TensorFlow) package size are less than 501 KB (1 MB). We also observe that model with more finegrained convolution layers is significantly I/O busy. For instance, GoogLeNet has 57 convolution layers and requests as much as 3,695 times of Caffe I/O and 1,442 times of TensorFlow I/O. Contrarily, AlexNet, which has only 5 convolution layers, requests less than 500 times of I/O.

![](images/32660723fdd2239367d328fd8c95e5059eb07a6cd5243cb86051a393d09a11a6.jpg)



Fig. 14. Deep tool’s code block size distribution.

TABLE 7 Comparison of the Data Transfer and Storage Usage for Cloud Deep Learning System and DeepShark 

<table><tr><td rowspan="2">Model</td><td colspan="2">Caffe Storage</td><td colspan="2">TensorFlow Storage</td></tr><tr><td>Ours</td><td>Cloud/Edge</td><td>Ours</td><td>Cloud/Edge</td></tr><tr><td>CaffeNet</td><td>233 MB</td><td>879 MB</td><td>232 MB</td><td>2.71 GB</td></tr><tr><td>GoogLeNet</td><td>52 MB</td><td>1.08 GB</td><td>26 MB</td><td>411 MB</td></tr><tr><td>AlexNet</td><td>233 MB</td><td>922 MB</td><td>232 MB</td><td>2.75 GB</td></tr><tr><td>VGG</td><td>233 MB</td><td>875 MB</td><td>233 MB</td><td>2.71 GB</td></tr></table>

# 5.4.2 Data Transfer and Storage on Mobile Device

To investigate the data transfer and storage consumption on mobile devices by using different (our proposed Deep-Shark and cloud/edge) deep learning systems, Table 7 shows the storage usage on top of different deep tools, deep models and system access. We see that the Deep-Shark approach significantly decrease size of data transfer and storage usage on mobile devices. For example, Caffe and TensorFlow only transmit 52 and 26 MB cellular data and then store them locally for the whole inference of GoogLeNet. As comparison, in the cloud/edge approach, Caffe totally uses 1.08 GB storage space. Moreover, in very extreme case, e.g., running large deep models such as VGG, both Caffe and TensorFlow use more than 2.7 GB storage space. This is because that the cloud/edge approach demands mobile deep learning system hold a copy of referred data including training dataset and inference dataset (i.e., user data). DeepShark breaks down the model into code blocks locally and thus requires only a few records of each dataset. Thus, DeepShark consumes fewer storage space than cloud method.

# 5.5 Performance of Energy Overheads

In DeepShark most of the energy overheads are cost by the computation over SoC. To explore the energy usage of using DeepShark to conduct high quality deep model inference on smartphone, this section employs the above models and applications as metrics again and find that more convolution layer model can significantly be energy-consuming (Fig. 15). In particular, to carry out an image recognition with VGG (GoogLeNet, AlexNet), DeepShark on average costs S5 LTE-A phone an energy of 70 mJ (320 mJ, 149 mJ) and 397 mJ (1,304 mJ, 927 mJ) when using Caffe and

![](images/97cc0de4c680bb52f28de0e5f5665c725f9954a65eb66e17e03ea9de38de4c27.jpg)



Fig. 15. Energy consumed to use DeepShark and cloud.

TABLE 8 Time Overheads (in Seconds) of DeepShark and SoC to Different I/O Media and Neural Network Models 

<table><tr><td colspan="2"></td><td>CaffeNet</td><td>GoogLeNet</td><td>AlexNet</td><td>VGG</td></tr><tr><td rowspan="2">NVMe</td><td>DeepShark</td><td>1.50</td><td>1.01</td><td>1.51</td><td>1.86</td></tr><tr><td>SoC</td><td>135.56</td><td>363.27</td><td>153.16</td><td>112.62</td></tr><tr><td rowspan="2">SATA</td><td>DeepShark</td><td>16.95</td><td>12.52</td><td>17.03</td><td>20.87</td></tr><tr><td>SoC</td><td>135.30</td><td>367.69</td><td>156.54</td><td>112.93</td></tr><tr><td rowspan="2">eMMC</td><td>DeepShark</td><td>16.26</td><td>3.49</td><td>16.31</td><td>22.49</td></tr><tr><td>SoC</td><td>138.74</td><td>367.51</td><td>151.69</td><td>118.51</td></tr></table>

TensorFlow, respectively. Note that the performance gap could be varied in according to the neural network architecture. Meanwhile, it only costs 153 and 608 mJ to conduct the CaffeNet model. Considering that the fully-charged energy of S5 LTE-A phone is 39 kJ. Thus, it only costs S5 LTE-A users less than 0.2 percent energy for every image recognition. As comparison, Fig. 15 also shows each benchmark’s energy cost by using the cloud deep learning system (here we use DL4J on the DevBox machine). We can see that by moving the computation workload from mobile device to the cloud, there brings a significant energy saving (on average 82 percent) in only conducting data transmission. Nevertheless, the cloud method imposes a heavy burden on data transfer efficiency as its size can be increased by 10.4X, as we illustrate in Section 5.4. Moreover, with better hardware (SoC, battery and network) support, DeepShark can achieve better performance. For example, in our experience, DeepShark provides the users more energy saving benefit as it support another three thoundand image recognition processes, when using Nexus 6 phone, which has Snapdragon 805 SoC and a fully-charged energy of 42 kJ.

Over time, with the development of either deep applications or deep models upgrade, the performance of Deep-Shark can be further improved.

# 5.6 I/O Latency

Last, this section studies how to mitigate the I/O bottlenecks in DeepShark. Table 8 shows the break-down of time consumed to I/O exchanges in a single image recognition with S5 LTE-A phone connecting to different hard drives on DevBox when running TensorFlow applications Note that we disable asynchronous I/O for the test, and actual time can be slightly less than shown in the plot. In practice, the tests are repeated by using only one thread for all processes. We consider the three cloud storage media as metrics: (i) NVMe SSD, which reaches 3.5 GB/sec read speed, (ii) SATA SSD, which holds an ability of 540 MB/sec read speed and (iii) eMMC hard drive, which has 98 MB/sec read speed. We profile the executing time of DeepShark and smartphone SoC itself for comprehensive efficiency evaluation. This is because the I/O efficiency of SoC is unnegligible when in frequency I/O requesting scenarios (as Section 5.4.1 illustrates) [32].

For DeepShark performance evaluation, we find that DeepShark runs on high-end COTS smartphones that with NVMe storage, e.g., iPhone 7 Plus, Google Pixel and Samsung Galaxy S8, consume 1.5 s on average to carry out all the data processing. In normal case, i.e., smartphones with eMMC or SATA-like storage media such as Samsung A7, DeepShark is able to saturate the whole data processing in less than 20 seconds. We summarize that I/O bottleneck can impact our system’s efficiency slightly and DeepShark is friendly to most COTS mobile devices. For SoC itself performance evaluation, we find that it is free of the storage media but very relevant to the architecture of neural network models. For example, given a specific SoC (Snap-Dragon 805 in this experiment), it consumes about 136 s to process CaffeNet with all storage media. There comes the same performance in GoogLeNet, AlexNet and VGG scenarios. Moreover, we observe that SoC take the most share (93.26 percent) of wall-clock time in a single image recognition task.

TABLE 9 Latency and Memory Consumed to Process Speech and Plaintext on DeepShark and TensorFlow 

<table><tr><td>Model</td><td>DeepShark</td><td>TensorFlow</td></tr><tr><td>WaveNet</td><td>4.62 s/7.1 MB</td><td>4.53 s/7.6 MB</td></tr><tr><td>SyntaxNet</td><td>3.10 s/64.1 MB</td><td>2.26 s/80.1 MB</td></tr></table>

Taken together, we can summarize that I/O bottleneck can impact our system’s efficiency slightly and DeepShark is friendly to most COTS mobile devices. However, the performance can be seriously constraint by mobile device SoC itself. We are looking forward to the emerging miniaturization techniques that already developed nanometer-level processors and sensors to integrate more powerful SoC into new-generation mobile devices which toward low I/O overheads.

# 6 DISCUSSION

With DeepShark, existing deep learning on mobile devices can use the developed technique to relieve the resourcehungry performance. This section discuss potential performance of DeepShark in scenarios that might interest readers.

# 6.1 DeepShark for More Neural Networks

DeepShark mainly trades time for energy and resource overheads. For applications that originally require long execution time, such as speech and plaintext recognition, Deep-Shark will further increase their execution times. In this section, we discuss how DeepShark performs in heavy workloads of speech and plaintext deep learning processes. Specifically, we also employ WaveNet [33] and Syntax-Net [34] as case study. As comparison, we run the same cases on TensorFlow. Table 9 shows their performance results. TensorFlow shows the average memory of 7.6 and 80.1 MB in WaveNet and SyntaxNet processes respectively. Here, DeepShark benefits comes up to 20 percent of memory footprint reduction, significantly reducing unnecessary recalculation of convolution operations. We noticed that the latency in using DeepShark increase was slightly ( 700 ms) more than that of TensorFlow. As expected, DeepShark performs well in processing either speech or natural language neural networks. As future work, we will keep on improving the latency efficiency of our system.

# 6.2 DeepShark in Mobile Sensing

Mobile sensing has been an intensely active area of interest, with many techniques and end-to-end systems developed, e.g., DeepEar [35]. DeepShark is primarily designed for vision based deep learning. Rather, we have also explored how DeepShark work for mobile sensing such as audio sensing (see the WaveNet related experiments in Section 6.3). Accompanying any future experiments with Deep-Shark will be a close investigation into the use of even larger-scale datasets and advanced neural network models of mobile sensing. Prior work in deep learning has shown the benefits of integrating increasingly larger amounts of training data; for example, speech models have been trained using thousands of hours of audio data [35]. It is also interesting to further develop DeepShark toward some specific mobile sensing scenarios like invisible light based face recognition, we leave it as future work.

# 6.3 Who Might Use DeepShark

In practice, mobile application can often be time sensitive, however, our proposed technique extends inference time from the order of seconds to minutes. To show the significance of DeepShark, here we demonstrate several realworld mobile application cases. First, within a face recognition application, e.g., automatically unlock screen, Deep-Shark makes mobile devices to incrementally extend user database on the backend with fewer resource (energy and memory) overheads. Second, DeepShark enables effectiveness deep learning systems on top of low-end IoT devices. Third, DeepShark is naturally designed with the time-insensitive applications, e.g., albums classification, which makes our proposed technique more significant. Taken together, these factors mean the potentials in designing DeepShark atop COTS deep learning system is applicable here.

# 7 RELATED WORK

This section reviews work closely related to DeepShark, this includes the significance of deep learning on mobile devices and deep neural network model compression for resource constraint scenarios.

Deep Learning on Mobile Devices. Lane et al. took significant first steps toward the real-time execution of deep learning on mobile devices [8], [35]. DeepEar [35] showed the feasibility of running entire DNNs for audio sensing applications on low-power mobile DSPs. DeepX [8] then enabled the execution of deep learning on mobile devices by splitting computations across multiple processors. Deep-Sense [36] presented early evidence that using a GPU could help improve the latency of deep learning computations. DeepShark extends that work by providing many more optimizations, a full implementation, and extensive evaluation. Glimpse [37] leverages the cloud to enable real-time object detection and tracking and MCDNN project [38] executed deep learning algorithms across mobile devices and clouds. DeepShark shares a high-level concept with Deep-Mon [9] (about re-using the computation resource), Deep-Shark’s caching technique relieves the intermediate partial results after processing convolutional layers, enabling much more fine-grained sharing of computation resource across the entire mobile device.

Deep Neural Network Model Compression. Model compression for deep neural networks has achieved significant results (e.g., SINGA [30], Tencent Mariana [39] and SparseSep [7]) in recent years due to the imperative demand on running deep learning models in resource constraint scenarios. In general, deep neural network model compression techniques can be classified into two categories. The first is focused on compressing pre-trained large networks. For instance, Han et al. [40] proposed a network pruning method to identify important connections in the deep neural network and removes all the unimportant connections whose weights are lower than a threshold. The second is focused on designing and training small networks directly. For example, Iandola et al. [41] proposed a squeeze layer that only has 1x1 filters to re-design the network architecture. The generated smart network achieves AlexNet-level accuracy with 50x fewer parameters.

# 8 CONCLUSION

This paper presents DeepShark, a novel platform which allows flexible resource allocation in COTS mobile deep learning systems. DeepShark trades off system efficiency between time consumption and memory uses. To this end, we proposed incremental inference mechanism through code block execution, which does not lead to any accuracy loss and is friendly to resource constraint environment. By implementing Deep-Shark with Caffe and TensorFlow frameworks, the experiments exam DeepShark’s efficiency, good extensibility and original deep learning experience. We also evaluate the system overheads and limitations of current DeepShark system. As future work, we are going to design new interfaces to make it work with more deep models and learning frameworks.

# ACKNOWLEDGMENTS

We thank the anonymous reviewers for valuable and insightful comments. This work is supported by National Key R&D Program of China under Grants No. 2017YFB1003003, NSF China under Grants No. 61572281 and Tsinghua University Initiative Scientific Research Program under Grants No. 20161080066.

# REFERENCES

[1] J. Dean, G. Corrado, R. Monga, K. Chen, M. Devin, M. Mao, A. Senior, P. Tucker, K. Yang, Q. V. Le, et al., “Large scale distributed deep networks,” in Proc. 25th Int. Conf. Neural Inf. Process. Syst., 2012, pp. 1223–1231.   
[2] S. Shi, Q. Wang, P. Xu, and X. Chu, “Benchmarking state-of-theart deep learning software tools,” in Proc. 7th Int. Conf. Cloud Comput. Big Data, 2016, pp. 99–104.   
[3] Q. Zhang, L. T. Yang, Z. Chen, P. Li, and M. J. Deen, “Privacy-preserving double-projection deep computation model with crowdsourcing on cloud for big data feature learning,” IEEE Internet Things J., vol. 5, no. 4, pp. 2896–2903, Aug. 2018.   
[4] J. Ba and R. Caruana, “Do deep nets really need to be deep?” in Proc. 27th Int. Conf. Neural Inf. Process. Syst., 2014, pp. 2654–2662.   
[5] Y. Sun, X. Wang, and X. Tang, “Deep learning face representation from predicting 10,000 classes,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2014, pp. 1891–1898.   
[6] S. Han, H. Mao, and W. J. Dally, “Deep compression: Compressing deep neural network with pruning, trained quantization and huffman coding,” arXiv preprint arXiv:1510.00149, 2015.   
[7] S. Bhattacharya and N. D. Lane, “Sparsification and separation of deep learning layers for constrained resource inference on wearables,” in Proc. 14th ACM Conf. Embedded Netw. Sensor Syst. CD-ROM, 2016, pp. 176–189.

[8] N. D. Lane, S. Bhattacharya, P. Georgiev, C. Forlivesi, L. Jiao, L. Qendro, and F. Kawsar, “DeepX: A software accelerator for low-power deep learning inference on mobile devices,” in Proc. 15th ACM/IEEE Int. Conf. Inf. Process. Sensor Netw., 2016, pp. 1–12.   
[9] L. N. Huynh, Y. Lee, and R. K. Balan, “DeepMon: Mobile GPUbased deep learning framework for continuous vision applications,” in Proc. 15th Annu. Int. Conf. Mobile Syst. Appl. Serv., 2017, pp. 82–95.   
[10] Paddle- PArallel Distributed Deep LEarning, (2017). [Online]. Available: https://github.com/PaddlePaddle/Paddle   
[11] J. Xue, J. Li, and Y. Gong, “Restructuring of deep neural network acoustic models with singular value decomposition,” in Proc. Annu. Conf. Int. Speech Commun. Assoc., 2013, pp. 2365–2369.   
[12] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “ImageNet classification with deep convolutional neural networks,” in Proc. 25th Int. Conf. Neural Inf. Process. Syst., 2012, pp. 1097–1105.   
[13] Y. Jia, E. Shelhamer, J. Donahue, S. Karayev, J. Long, R. Girshick, S. Guadarrama, and T. Darrell, “Caffe: Convolutional architecture for fast feature embedding,” in Proc. 22nd ACM Int. Conf. Multimedia, 2014, pp. 675–678.   
[14] M. Abadi, P. Barham, J. Chen, Z. Chen, A. Davis, J. Dean, M. Devin, S. Ghemawat, G. Irving, M. Isard, et al., “Tensorflow: A system for large-scale machine learning,” OSDI, vol. 16, pp. 265– 283, 2016.   
[15] TensorFlow is an open source software library for machine intelligence, (2016). [Online]. Available: https://www.tensorflow.org   
[16] G. E. Hinton, S. Osindero, and Y.-W. Teh, “A fast learning algorithm for deep belief nets,” Neural Comput., vol. 18, no. 7, pp. 1527–1554, 2006.   
[17] S. Kosta, A. Aucinas, P. Hui, R. Mortier, and X. Zhang, “ThinkAir: Dynamic resource allocation and parallel execution in the cloud for mobile code offloading,” in Proc. IEEE INFOCOM, 2012, pp. 945–953.   
[18] Antutu report: Top 10 popular smartphones around the world, Q3 2016, (2016). [Online]. Available: http://www.antutu.com/en/ view.shtml?id=8293   
[19] BVLC CaffeNet model, (2012). [Online]. Available: https://github. com/BVLC/caffe/tree/master/models/bvlc\_reference\_caffenet   
[20] DATASET image, (2012). [Online]. Available: http://net.org/ challenges/LSVRC/2012/   
[21] NVIDIA DIGITS DevBox, (2016). [Online]. Available: https:// developer.nvidia.com/devbox   
[22] Java native interface, (2016). [Online]. Available: https:// developer.android.com/training/articles/perf-jni.html   
[23] Y. LeCun, Y. Bengio, and G. Hinton, “Deep learning,” Nature, vol. 521, no. 7553, pp. 436–444, 2015.   
[24] M. S. Gordon, D. A. Jamshidi, S. Mahlke, Z. M. Mao, and X. Chen, “COMET: Code offload by migrating execution transparently,” in Proc. 10th USENIX Conf. Operating Syst. Des. Implementation, 2012, pp. 93–106.   
[25] A. Aggarwal, J. Vitter, et al., “The input/output complexity of sorting and related problems,” Commun. ACM, vol. 31, no. 9, pp. 1116–1127, 1988.   
[26] ILSVRC-2014 model (VGG team) with 16 weight layers, (2014). [Online]. Available: https://gist.github.com/ksimonyan/ 211839e770f7b538e2d8#file-readme-md   
[27] BVLC GoogleNet model, (2014). [Online]. Available: https:// github.com/BVLC/caffe/tree/master/models/bvlc\_googlenet   
[28] BVLC AlexNet model, (2014). [Online]. Available: https://github. com/BVLC/caffe/tree/master/models/bvlc\_alexnet   
[29] Monsoon power monitor, (2016). [Online]. Available: https:// www.msoon.com/LabEquipment/PowerMonitor/   
[30] B. C. Ooi, K.-L. Tan, S. Wang, W. Wang, Q. Cai, G. Chen, J. Gao, Z. Luo, A. K. Tung, Y. Wang, et al., “SINGA: A distributed deep learning platform,” in Proc. 23rd ACM Int. Conf. Multimedia, 2015, pp. 685–688.   
[31] Paddle- PArallel distributed deep LEarning, (2017). [Online]. Available: https://github.com/PaddlePaddle/Paddle   
[32] H. Kim and S. Ahn, “BPLRU: A buffer management scheme for improving random writes in flash storage,” in Proc. 6th USENIX Conf. File Storage Technol., 2008, pp. 1–14.   
[33] A. V. D. Oord, S. Dieleman, H. Zen, K. Simonyan, O. Vinyals, A. Graves, N. Kalchbrenner, A. W. Senior, and K. Kavukcuoglu, “WaveNet: A generative model for raw audio,” SSW, pp. 125, 2016.   
[34] C. Alberti, D. Andor, I. Bogatyy, M. Collins, D. Gillick, L. Kong, T. Koo, J. Ma, M. Omernick, S. Petrov, et al., “SyntaxNet models for the CoNLL 2017 shared task,” arXiv preprint arXiv:1703.04929, 2017.

[35] N. D. Lane, P. Georgiev, and L. Qendro, “DeepEar: Robust smartphone audio sensing in unconstrained acoustic environments using deep learning,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., 2015, pp. 283–294.   
[36] L. N. Huynh, R. K. Balan, and Y. Lee, “DeepSense: A GPU-based deep convolutional neural network framework on commodity mobile devices,” in Proc. Workshop Wearable Syst. Appl., 2016, pp. 25–30.   
[37] T. Y.-H. Chen, L. Ravindranath, S. Deng, P. Bahl, and H. Balakrishnan, “Glimpse: Continuous, real-time object recognition on mobile devices,” in Proc. 13th ACM Conf. Embedded Netw. Sensor Syst., 2015, pp. 155–168.   
[38] S. Han, H. Shen, M. Philipose, S. Agarwal, A. Wolman, and A. Krishnamurthy, “MCDNN: An approximation-based execution framework for deep stream processing under resource constraints,” in Proc. 14th Annu. Int. Conf. Mobile Syst. Appl. Serv., 2016, pp. 123–136.   
[39] Y. Zou, X. Jin, Y. Li, Z. Guo, E. Wang, and B. Xiao, “Mariana: Tencent deep learning platform and its applications,” Proc. VLDB Endowment, vol. 7, no. 13, pp. 1772–1777, 2014.   
[40] S. Han, J. Pool, J. Tran, and W. Dally, “Learning both weights and connections for efficient neural network,” in Proc. 28th Int. Conf. Neural Inf. Process. Syst., 2015, pp. 1135–1143.   
[41] F. N. Iandola, S. Han, M. W. Moskewicz, K. Ashraf, W. J. Dally, and K. Keutzer, “SqueezeNet: Alexnet-level accuracy with 50x fewer parameters and <0.5 mb model size,” arXiv preprint arXiv:1602.07360, 2016.

![](images/d7fb5b9cf7b1a284cfa18a5c5bd618517930d14a7a39db36058d137b9a3188d1.jpg)



Chao Wu received the BEng degree in software engineering from Southeast University, Nanjing, China, in 2012, and the PhD degree from the Department of Computer Science and Technology, Tsinghua University, Beijing, China, in 2017. He is now a postdoc in Tsinghua University. His research interests include mobile computing, edge computing and networked systems with a focus on operating system principle, performance optimization, architecture design. He is a member of the IEEE.

![](images/323fa04fc9bcefaffbdd7d0ea91cee35aedbc273b00dee833be84d65800d610f.jpg)



Lan Zhang received the bachelor’s degree from the School of Software, Tsinghua University, China, in 2007, and the PhD degree from the Department of Computer Science and Technology, Tsinghua University, China, in 2014. She is currently an assistant professor with the School of Computer Science and Technology, USTC. Her research interests span social networks, privacy, secure multiparty computation and mobile computing, etc. She is a member of the IEEE.

![](images/3dde9a9338139e2316e1578fccb93f35ce7ae3a4afa429dc9118688c8adcd4f8.jpg)



Qiushi Li received the BEng degree from the University of Electronic Science and Technology of China, in 2017, and is currently working toward the PhD degree in the Department of Computer Science and Technology, Tsinghua University, Beijing, China. His research interests include mobile computing systems and applications.

![](images/c80a56e1f3027e42a70969f7c09f99927474562af53ff82ad128c14da21caeae.jpg)



Ziyan Fu received the BEng degree from the University of Electronic Science and Technology of China, in 2017, and is currently working toward the PhD degree in the Department of Computer Science and Technology, Tsinghua University, Beijing, China. His research interests include mobile applications and distributed systems.

![](images/c9047a67f75bd7bcff11fa3fabd378acbdf2290a43e0ec63bb53a1489e2a8e04.jpg)



Wenwu Zhu received the PhD degree from the New York University Polytechnic School of Engineering, New York, NY, in 1996. He is currently a professor with the Computer Science Department of Tsinghua University, Beijing, China. His current research interests include multimedia cloud computing, social media computing, multimedia big data, and multimedia communications and networking. He has been serving as EiC for the IEEE Transactions on Multimedia since Jan. 1, 2017. He is a fellow of the IEEE.

![](images/e9332946dd8166aad5bb34c1eb5593002cb66de6752bea298968fd33821b67b6.jpg)



Yaoxue Zhang received the BS degree from the Northwest Institute of Telecommunication Engineering, China, and the PhD degree in computer networking from Tohoku University, Japan, in 1989. He is currently a professor with the Computer Science Department of Tsinghua University, Beijing, China. He was a visiting professor of Massachusetts Institute of Technology and University of Aizu, in 1995 and 1998. His major research interests include computer networking, operating systems, ubiquitous computing. He is a senior member of the IEEE.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.