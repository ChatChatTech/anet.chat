# AppDNA: App Behavior Profiling via Graph-based Deep Learning

Shuangshuang Xue\*, Lan Zhang\*, Anran Li\*, Xiang-Yang Li\*, Chaoyi Ruan\*, Wenchao Huang\*  
\*University of Science and Technology of China

Abstract—Better understanding of mobile applications' behaviors would lead to better malware detection/classification and better app recommendation for users. In this work, we design a framework APPDNA to automatically generate a compact representation for each app to comprehensively profile its behaviors. The behavior difference between two apps can be measured by the distance between their representations. As a result, the versatile representation can be generated once for each app, and then be used for a wide variety of objectives, including malware detection, app categorizing, plagiarism detection, etc. Based on a systematic and deep understanding of an app's behavior, we propose to perform a function-call-graph-based app profiling. We carefully design a graph-encoding method to convert a typically extremely large call-graph to a 64-dimension fix-size vector to achieve robust app profiling. Our extensive evaluations based on 86,332 benign and malicious apps demonstrate that our system performs app profiling (thus malware detection, classification, and app recommendation) to a high accuracy with extremely low computation cost: it classifies 4024 (benign/malware) apps using around 5.06 second with accuracy about 93.07%; it classifies 570 malware's family (total 21 families) using around 0.83 second with accuracy 82.3%; it classifies 9,730 apps' functionality with accuracy 33.3% for a total of 7 categories and accuracy of 88.1% for 2 categories.

# I. INTRODUCTION

Millions of mobile applications (apps) have been developed to provide rich services ranging from news, weather, social communication and entertainment to serious businesses such as medical, fitness, finance. Google Play Store now hosts more than 2.8 million apps, and Apple Store hosts 2.2 million apps [1]. Especially, Android operating system dominates the smartphone market with a share of $86.8\%$ [2], but is also the most widely-attacked OS [3]. On average, several thousands of emerging apps are uploaded daily. The extraordinarily large amount and rich functionalities raised new interesting but challenging issues. Firstly, facing millions of apps, it is difficult for app markets to efficiently categorize and organize those apps in a proper way. We conducted an online survey including 224 respondents with diverse occupations. Of the respondents, $42.86\%$ were unsatisfied with the app categorization by the existing markets, and $49.55\%$ thought the keywords and descriptions provided by the markets were inconsistent to the functionalities of those apps. Secondly, the dramatic proliferation of apps makes it difficult for users to locate interested apps, which makes effective app recommendation urgently needed. Last but not the least, the increasing popularity of mobile devices and associated pecuniary benefits attract misbehaving developers, resulting in a big rise of malicious and plagiarized apps. Thus, malware and plagiarism detection have become an enduring focus of research in both industry and academia in recent years [4].

We notice that all these aforementioned issues require a deep and systematic understanding of apps' behaviors, an efficient way to profile different apps, as well as a method to measure the similarity between apps. Existing efforts analyzing app features and behaviors have two branches in general. The first branch of work conducts source code level analysis in a static or dynamic or mixed way, and provide various useful app analysis tools [5]–[8]. Each of those tools is dedicated to some specific tasks (most are related to vulnerabilities detection), e.g., detecting sensitive information leaks [7], permission misuse [6], and plagiarism [9]. Although they deliver fine-grained reports about specific tasks, they usually require high overhead. They provide neither a comprehensive profiling of an app nor a metric to measure the similarity between two apps. Moreover, many available tools fail to analyze some apps with complex structures and behaviors according to a survey [4]. The second branch of work extracts pre-defined features from apps, e.g., permissions requested by apps or the usage of specific API functions [10]. Some work define features on call graphs and API dependency graphs [11], [12]. Some recent work extract malware features during app execution using recurrent neural network (RNN) in a supervised way [13]. Then supervised learning model, e.g., SVM, Naive Bayes and deep belief network (DBN) [14], are applied on those features to perform binary classification for malware detection. Avoid fine-grained analysis, those machine learning based methods have improved malware classification efficiency. But the limitation lies in handcrafted task-specific features and lack of labeled training data. Both pre-defined and auto-extracted features are tailored for malicious behaviors, thus cannot comprehensively characterize diverse app behaviors. Besides, those methods use supervised learning, which relies on extensive labeled training data. However, towards different objectives like functionality categorization and plagiarism detection, available labeled training data is limited in both categories and quantity.

In this work, we aim to design a framework to automatically generate a compact representation for each app to comprehensively profile its behaviors. The behavior difference between two apps can be measured by the distance between their representations. As a result, the versatile representation can be generated once for each app, and then be used for a wide variety of objectives, including malware detection, app categorizing, plagiarism detection and so on. To achieve such an ambitious goal, our main idea is to leverage deep neural network to learn behavior feature representations from the corresponding function call graphs extracted from the apps in an unsupervised manner. We use function call graph (FCG) instead of inter-procedural control flow graph (ICFG), since FCG is concise and efficient to extract and store. In our experiments, we show that FCG reserves sufficient information about app's behaviors. As each behavior can be reflected in calling one or a series of system functions, apps possessing similar benign/malicious functionalities often have similar function call graphs or subgraphs, thus similar representations. However, we need to address several critical challenges to realize this idea.

First, although some recent work study deep learning on graphs, e.g., chemistry data and social networks [15], and graph embedding methods are proposed, for example, Node2vec [16], DeepWalk [17] and Skip-graph [18]. There are still many unexplored challenges in conducting deep learning on large-scale directed graphs like function call graphs. Feeding function call graphs into a neural network requires encoding graphs into vectors in a way preserving the function call relationships and function properties. The encoding should also be robust enough against evasion techniques like code reordering and function renaming. Specifically, our function call graphs have very shallow depth (most of them have less than 40 layers) and vary size number of nodes (as shown in Fig. 3). Instead of learning representations for just the nodes of the graph, our work focus on learning a feature representation for the whole graph. The above mentioned work can not be applied to our work. Second, many complex apps have hundreds of thousands of nodes in their function-call graphs, resulting in large-scale encoded vectors. Those large vectors are inefficient for tasks like large-scale malware detection and app functionality categorizing. Besides, app behaviors can be very complex and diverse. Towards a variety of objectives, we need to design a proper unsupervised learning model to generate a versatile and compact representation.

Facing the aforementioned challenges, we propose, design, and develop APPDNA with the following contributions:

- We propose a compact representation (only 64-dimension in our implementation) to comprehensively profile each app's behavior. The versatile representations can be used for various objectives, e.g., malware detection, malware family classification, and app functionality categorizing.   
- We design a novel method to encode function call graphs into vectors which well preserve graph structure and node properties. Our encoding is robust against various evasion techniques such as code reordering, function renaming.   
- We design a neural network based on autoencoder to learn the fix-size compact representation in an unsupervised way while minimizing behavior information loss. As a comparison, three supervised learning models are also designed and implemented.   
- We evaluate the performance of our proposed profile representation for different tasks with 86,332 apps. The results show that we achieve $93.07\%$ accuracy for mal

![](images/442ce485078cf980ecb5e7286509ca3bda86c06c794a205c99674b968eda8756.jpg)



Fig. 1. APPDNA framework to generate app profile.

ware detection, 82.3% accuracy for malware family classification, and 88.1% accuracy for app functionality categorizing with 2 categories. Our method can also be used for app plagiarism detection.

To the best of our knowledge, we're the first to learn task-agnostic representations from graphs in an unsupervised manner. The rest of the paper is organized as follows. We present the overview of our system design in Section II. We introduce the encoding method for call graph in Section III and the unsupervised deep learning model in Section IV. Comprehensive evaluations are conducted in Section V. We review related work in Section VI, and conclude the work in Section VII.

# II. SYSTEM OVERVIEW OF APPDNA

# A. Design Goal

Millions of apps with complex structures and highly diverse behaviors raise great challenges for a series of tasks, including app categorization, organization, recommendation, malware detection and plagiarism detection. Towards efficiently performing these tasks, we propose to generate a representation for each app to profile its behaviors with following features:

- Comprehensiveness: The representation should completely capture each app's diverse behaviors, including benign functional behaviors and malicious behaviors. As a result, such a versatile representation can be used for a wide range of tasks.   
- Similarity-preserving: Two apps with similar behaviors should have similar representations. Thus the representations can be directly used for app categorizing and plagiarism detection.   
- Compactness: The representation should be as compact as possible in order to achieve highly efficient computation, e.g., clustering and classification, when dealing with a huge number of apps.

# B. Design Overview

In this work, we propose a framework APPDNA with a series of carefully designed components to generate the desired profile representation for each app. We use a function call graph to capture each app's comprehensive behavior information, since app behaviors can be reflected in calling a series of system functions. Different from previous work, which manually define task-specific features on graphs, we propose to leverage unsupervised deep learning to automatically extract highly compact representations from function call graphs to meet the aforementioned three requirements. To address the challenging issue that feeding a directed graph into a neural network, we carefully design a graph encoding method to transfer a function call graph into a vector while preserving the function call relationship and function properties.

Fig. 1 presents the overview of our framework. Given an app, its profile representation is generated as follows:

1) Function call graph extraction: We use Soot [19] and FlowDroid [7] to extract function call graphs from apps.   
2) Graph encoding: Taking the function-call graph as input, our carefully designed encoding method transfers the graph into a vector. (See Section III.)   
3) Unsupervised representation learning: We feed encoded vectors of function call graphs into an autoencoder-based neural network to extract a compact profile representation for the app. (See Section IV.)

# III. FUNCTION CALL GRAPH ENCODING

Before feeding function call graphs into a neural network to obtain a highly compact representation, we need to transfer graphs into vectors. In this section, we present detailed design of our graph encoding mechanism preserving graph structures.

# A. Design Principle

The encoding mechanism should maintain complete function call relationships and function properties, as well as meet the following requirements.

- Uniqueness: A unique function call graph should have a unique encoded vector.   
- Preserving graph and subgraph similarity: Given two similar function call graphs, they should have similar encoded vectors; given two function graphs possessing similar subgraphs, their encoded vectors should have similar sub-vectors.   
- Robustness: Since our ultimate goal is to profile the behaviors of apps and compare their behaviors' similarity, the encoding method should be robust against benign and malicious modifications, which do not change the app's behavior, to the function graphs. Such modifications include identifier or function renaming, code reordering, junk code insertion, function outlining and inlining $^{1}$ .

# B. Function Call Graphs

The function call graph provides a sufficient description of an app's source code level behaviors. It is defined as

Definition 1 (Function Call Graph): Given an app, its function call graph is a directed graph $G = (V, E, L)$ , where:

\- The vertex set $V$ is a finite set of nodes with one-to-one mapping to the app's all functions, with a node $v \in V$ representing an app's function, including both

$^{1}$ Note that, some transformation attacks like dynamic code loading require dynamic analysis, which are out of the scope of this work.

![](images/c0e62f87b9f3e8f139cd219d8cb8ecadd63a116adecf99ec1da4d58aa16dc275.jpg)



Fig. 2. A simple example of function call graph(package names, return types, etc, are omitted). This call graph is extracted from a malware named Mania.

user defined functions and system functions (i.e., APIs). In the rest of this paper, we use "node" and "function" interchangeably;

- The edge set $E$ represents the call relationships among functions, where an edge from a node $v_{1}$ to a node $v_{2}$ indicates a call from the function represented by the node $v_{1}$ to the function represented by the node $v_{2}$ ;   
- $L$ is the set of labels for all nodes, where each label consists of a function's package name, class name, return type, function name, parameter types, and a counter recording how many times the function has been called. A label can represent a function uniquely.

Function call graph generation. We conduct static analysis on an apk file to extract the function call graph. Unlike Java programs, Android apps do not have a main function, instead comprise many entry points, that is, those methods are implicitly called by the Android framework. As a result, we use a Java optimization and analysis framework Soot [19] to extract function call graphs, and use FlowDroid [7] to create a dummy main method for the whole app. Fig. 2 gives a simple example of function call graph. Specifically, each call graph has one root node referred as "DummyMain" node. The root node's children nodes (i.e., entry nodes or entry functions) are all user defined functions. Note that, these entry functions are called at runtime without a fixed order [7].

# C. Main Idea for Encoding Function Call Graphs

A naive idea to encode a directed graph is using its adjacency matrix. Although an adjacency matrix preserves complete information of all edges, it cannot be adopted as the input of the neural network due to three reasons. First, since different apps possess different sets of functions (i.e., nodes), to support similarity measurement between apps, adjacency matrices should contain the same set of all possible nodes, which results in very large and sparse matrices. As shown in Fig. 3, 50% apps have more than 2000 nodes and 20% apps have more than 4000 nodes, and the largest app has about 14000 nodes; meanwhile 50% apps have more than 7000 edges and 20% apps have more than 16000 edges. To make these graphs's adjacency matrices comparable, it requires $14000 \times 14000$ matrices for all apps, while most of them are quite sparse. Second, function nodes have diverse labels, which are important for app behavior understanding. As a result, extra structures are needed to encode nodes' labels. However, learning a representation from multiple structures simultaneously is still a quite challenging issue. Third, adjacency matrices are not robust against aforementioned modifications, e.g., function renaming.

![](images/d79bfd85a1360e439027e92f1e7f36d0949250fa92ecf7944ffd53e8f3e4b485.jpg)



(a) Node number distribution.

![](images/ab4e8f90bdaa376157ef1535f89dc18c8ab91281cf90774394bf564b206f7468.jpg)



(b) Edge number distribution.   
Fig. 3. Node number and edge distributions of function call graphs extracted from apps of different years.

In this work, we propose a mechanism to traverse function call graphs and build an encoded vector simultaneously. Once a node $v_{i}$ is visited, its properties are encoded by a function $\text{Code}(\cdot)$ and concatenated to the vector. To preserve call relationships and node properties, as well as meet the principles outlined in Section III-A, it is essential to determine proper visiting order and encoding function $\text{Code}(\cdot)$ .

# D. Visiting Order

We can start the traverse from the root node (i.e., DummyMain), then visit all its descendant nodes in either depth-first or breadth-first order, both of which can preserve the call relationships. We only visit each node of the function call graph once. Such simple visiting method may not fully capture the app's behavior semantics. Our evaluations show that it achieves considerably good but unsatisfying accuracy for malware detection (Fig. 7). The key problem here is to determine the order to visit nodes in the same layer, which can influence sub-vectors' positions significantly. For example, it is important to determine the visiting order of the entry function nodes(introduced in Section III-B), which are called at runtime without a fixed order. So, we need a rule to fix the visiting order across different apps, in order to yield similar visited node sequence for different graphs with similar behaviors. Also, the visited node sequence should not be sensitive to modifications including function renaming, code reordering, junk code insertion, function outlining and inlining, etc.

Order of system functions. For a pair of system functions, we can order them by the lexicographical order of their function signatures (created from package name, class name, return type, function name, and parameter types), since signatures of system functions are stable and consistent across apps.

Order of user defined functions. However, all label components, e.g., package name and function name, of a user defined function can easily be modified by developers, which makes user defined functions the most labile factors for the encoding. So, the main challenge is to determine a stable order of two user defined functions. Our solution to this problem is based on the following two insights.

Insight 1: Despite the labile label of a user defined function, its behavior is performed by calling a series of system functions, which are stable and consistent across apps. For example, two functions SendThem() and threat() in Fig. 2 possess different labels, but perform the same behavior, i.e., calling system functions getDefault() and sendTextMessage(). As a result, we can use the sets of system functions called by user defined functions, referred to as each user defined function's system function set, to represent their behaviors as well as to determine their visiting order.

![](images/bab9a525b670d855d1bdc50b1798b30d3d755232560335e69d791d305382613c.jpg)



(a) Package count of packages called by user defined functions.

![](images/777c9266984619414e914a5a6bb4da79a3245900b28bebb3035b2d19af790108.jpg)



(b) Hybrid nodes affected by perturbing LastLayer nodes.   
Fig. 4. Function call statistics about our datasets.

Insight 2: Given a set of system functions, a developer may reorder their positions in the source code without changing the app's behavior. For example in Fig. 2, system functions getMessageBody() and getDisplayOriginatingAddress() can be called in any order, while both orders represent the same behavior. A developer can also change conditions (e.g., using if-else and switch-case structures) or use function outlining and inlining techniques to reorganize the code. As a result, our visiting order should not be sensitive to system functions' order within a set.

Based on these two insights, we propose a relatively stable order of user defined functions by their behaviors, i.e., the composition of their system function sets. We leverage the idea of majority voting, despite the different order of system functions in each set. Intuitively, if most system functions called by a user defined function A are in front of system functions called by another user defined function B, then A should be visited before B. In this way, package or function renaming and code reordering won't affect the ordering. Slight insertion or deletion of system functions will have little effect on the ordering.

Before we present the detail of our algorithm, we summarize some notations in Table I for the sake of simplicity.

TABLE I
NOTATIONS, ABBREVIATIONS AND EXAMPLES IN FIG. 2. 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $G$ </td><td>A function call graph.</td></tr><tr><td> ${\mathcal{F}}_{U}$ </td><td>User defined function, e.g.,SendThem() and run().</td></tr><tr><td> ${\mathcal{F}}_{S}$ </td><td>System function (APIs), e.g.,SendTextMessage() and getDefault().</td></tr><tr><td> $S\left( {\mathcal{F}}_{U}\right)$ </td><td>System function set of  ${\mathcal{F}}_{U}$  ,i.e., the set of system functions called by  ${\mathcal{F}}_{U}$  ,e.g., for threat(), its system function set if {getDefault(), SendTextMessage)}.</td></tr><tr><td> ${\mathcal{F}}_{LU}$ </td><td>LastLayerUserFunc, Last layer UserFunc, whose direct successor nodes are SysFuncs.</td></tr><tr><td> ${\mathcal{F}}_{HU}$ </td><td>HybridUserFunc, User function, whose direct successor nodes include both SysFuncs and UserFuncs.</td></tr><tr><td>Code(.)</td><td>Encoding function, generate a vector for the input.</td></tr></table>

Given a set of user defined functions $S = \{\mathcal{F}_{Ui} | 0 < i \leq n\}$ that need to be ordered, each $\mathcal{F}_{Ui}$ has a set of called system functions, denoted as $S(\mathcal{F}_{Ui})$ . For each system function $\mathcal{F}_{Sj} \in S(\mathcal{F}_{Ui})$ , $\mathcal{F}_{Sj}.count$ denotes the number of times that the function $F_{Sj}$ is called by $F_{Ui}$ . To get the value of count for each $F_{Sj}$ , we collect all system functions for each user defined function and count their calling times. When there is a loop in the function-call-graph, we arbitrarily break the loop to get a approximate count value. For all system functions in the union set $\bigcup_{0<i\leq n}\mathcal{S}(\mathcal{F}_{Ui})$ , we order them by the lexicographical order, and give an index $Index(\mathcal{F}_{Sj})$ to each system function $F_{Sj}$ . Specifically, the index value here indicates priority, that is function with larger index is before those with smaller indices, Now, the priority of each user defined function $F_{Ui}$ is determined by the weighted sum of the system functions' priorities in $S(\mathcal{F}_{Ui})$ :

$$
\text { Priority } (\mathcal {F} _ {U i}) = \sum_ {\mathcal {F} _ {S j} \in \mathcal {S} (\mathcal {F} _ {U i})} \operatorname{Index} \left(\mathcal {F} _ {S j}\right) * \frac {\mathcal {F} _ {S j} . \text { count }}{\text { MaxCount }}, \tag {1}
$$

where MaxCount = max( $\mathcal{F}_{Sj}$ .count) for all $\mathcal{F}_{Sj} \in \bigcup_{0<i\leq n} S(\mathcal{F}_{Ui})$ , i.e., the maximal count number a system function has been called. Then we can order these user defined functions by their priorities. The detailed algorithm to order a set of user functions is summarized in Algorithm 1.

Algorithm 1 Order User Functions   
Input:
1: A set of user functions $S_{U} = \{F_{Ui} | 0 < i \leq n\}$ .
2: System function set $\mathcal{S}(\mathcal{F}_{Ui})$ for each user function $F_{Ui}$ .
Output: Ordered $S_{U}$ 3: function ORDER( $S_{U}$ )
4: $S_{S} \leftarrow \bigcup_{0<i \leq n} \mathcal{S}(\mathcal{F}_{Ui})$ 5: MaxCount $\leftarrow \max(\mathcal{F}_{Sj}.count)$ for all $F_{Sj} \in S_{S}$ 6: $P \leftarrow \{p_i = 0 | 0 < i \leq n\}$ 7: for each $F_{Ui}$ in $S_{U}$ do
8: $p_i = \text{Priority}(\mathcal{F}_{Ui}, S_s, MaxCount)$ 9: end for
10: $S_{U}.Sortby(p_i)$ 11: return $S_{U}$ 12: end function
13: function PRIORITY( $F_{Ui}, S_s, MaxCount$ )
14: $p = \sum_{\mathcal{F}_{Sj} \in \mathcal{S}(\mathcal{F}_{Ui})} Index(\mathcal{F}_{Sj}) * \frac{\mathcal{F}_{Sj}.count}{MaxCount}$ 15: return p
16: end function
17: function INDEX( $F_{Sj}, S_s$ )
18: ind $\leftarrow 0$ 19: for each $F_{Sk}$ in $S_s / F_{Sj}$ do
20: if $F_{Sj}.name > F_{Sk}.name$ then
21: ind++;
22: end if
23: return ind
24: end for
25: end function

# E. Encoding User-Defined Functions

When a node in the function-call graph is visited, its behavior are encoded into a small vector and concatenated to the graph vector $Code(G)$ . One naive method is to generate a hash value for the label (excluding the count) of every single system function. Then for a user defined function $F_{Ui}$ , its vector $Code(F_{Ui})$ is just the concatenation of values of all functions in $S(F_{Ui})$ , ordered by priorities. However, this will result in a very high-dimension $Code(G)$ considering the huge node size of G (See Fig. 3). On the other hand, if we generate only a single hash value for the set of system functions $\mathcal{S}(\mathcal{F}_{Ui})$ , the value will be too coarse-grained and sensitive to even slight modifications.

To achieve a reasonable trade off, we generate vector for each user defined function $F_{Ui}$ by grouping system functions in $S(\mathcal{F}_{Ui})$ by their package names. For each package group, we concatenate all its member system functions' labels (excluding the counts) in the lexicographic order to get a string, then apply a string hash function (e.g., BKDR) to yield one hash value for each group. Then $Code(\mathcal{F}_{Ui})$ is obtained by concatenating values of all package groups according to the lexicographical order of their package names. In this way, we greatly reduce the length of each user defined function's hash value while maintaining sufficient behavior information of the function as well as robustness of encoding. For user-defined functions, statistics on our collected apps in Fig. 4(a) show that more than 75% of HybridUserFunc $F_{HU}$ called system functions from at least two different packages.

# F. Graph Vector Generation

To put visiting order and encoding function together, we are ready to generate a vector $\text{Code}(G)$ for a function call graph. Given G, we traverse the graph in depth-first order or breadth-first order starting from the root node (dummyMain). For nodes in the same layer, their visiting order is determined by their priorities according to Algorithm 1. When a user defined function $F_{Ui}$ is visited, $\text{Code}(\mathcal{F}_{Ui})$ is generated according to Section III-E, and concatenated to $\text{Code}(G)$ . $\text{Code}(G)$ is generated when the traverse is completed.

# IV. REPRESENTATION LEARNING

With our graph encoding method, we obtain vectors generated from apps' function call graphs with little information loss. In this section, we design an unsupervised deep neural network based on autoencoder to take those vectors as input and output representations with consistent dimension satisfying three requirements in Section II-A.

# A. Unsupervised Deep learning

We adopt deep autoencoder learning algorithm [20] to learn the compact representation from unlabeled data. First, we briefly introduce autoencoder. An autoencoder is a feedforward neural network with an input layer, an output layer and one or more hidden layers. The output layer has the same number of nodes as the input layer. An autoencoder can be divided into two parts, the encoder and the decoder, defined as transitions $\Phi$ and $\Psi$ . Here $\Phi: X \rightarrow F$ , $\Psi: F \rightarrow X$ , where X is input. The training is conducted with backpropagation algorithm to find transitions $\Phi$ and $\Psi$

$$
\Phi , \Psi = \arg \min _ {\Phi , \Psi} | | X - (\Phi \cdot \Psi) X | | ^ {2}.
$$

By minimizing the reconstruction error $\left|\left|X-(\Phi\cdot\Psi)X\right|\right|^{2}$ of the network, the training process targets to make the output $X'$ similar to the original input X. In the training procedure, the reconstruction error could be squared error $L(x,x')=\left|\left|x-x'\right|\right|=\left|\left|x-\sigma'(W'(\sigma(Wx+b))+b')\right|\right|^{2}$ , where x is usually averaged over input training set.

![](images/ced0b34cfda48411573f090ee398264f41a3230d1ced58a53816233389916944.jpg)



Fig. 5. Our unsupervised learning model for finding compact representation.

Note that, in the feature space, if F has a lower dimensionality than the input space X, i.e., q < d, then the latent representation $f = \Phi(x)$ can be considered as a compressed representation of the input x. So the representation is that we need to generate in our task, which is a good profile representation of each app. There are many variations of autoencoder like sparse autoencoder, deep fully-connected autoencoder, deep convolutional autoencoder, etc. In our work, we build a fully-connected autoencoder with max-pooling layers to make the representation as compact as possible while minimize the reconstruction error. The pooling layers downsample the representation, and help to mitigate over-fitting by providing an abstracted form of the representation. They also reduce the computational cost by reducing the number of parameters to learn. Fig.5 presents the architecture of our model. Our model consists of two fully-connected layers and two pooling layers in encoding phase and four fully-connected layers in decoding phase. The unit number of each encoding layer is 5000, 1024, 256, 64, respectively. And we leveraged Adam Optimizer and Relu activation function during the training procedure. We tuned these parameters with a trade-off between the information loss and compactness and finally got parameters above. The learned representation of the input data is only 64-dimension, which can be adopted in various tasks including malware detection, malware family classification and functionality categorizing. All these tasks will be evaluated in our experiments in Section V.

# B. Supervised Deep learning

As a comparison, we also build and investigate three typical supervised deep learning models for our tasks and evaluate their effectiveness in our experiments.

Deep neural network(DNN). A DNN is a typically feedforward neural network with multiple hidden layers between the input and output layers. It can model complex non-linear relationships. We adopt a DNN with three hidden fully-connected layers, whose sizes are 1024, 512 and 64 respectively, and a softmax layer. The input layer has 5000 nodes, and the output representation is 64-dimension.

Convolutional Neural Network(CNN). Different from DNN, a CNN has convolution layers, which conduct convolution operation along the input data. A convolution layer is usually followed by a pooling layer, which progressively reduces the spatial size of the representation to reduce the amount of parameters and computation in the network, hence to also control overfitting. We adopt a CNN with three convolution layers, each followed by a max-pooling layer. The last pooling layer is fully connected to a softmax layer, where each node is for one class in the training data. With CNN, we expect to learn apps' encoded vectors for each location as the convolution window sliding over the input.

Long Short Term Memory (LSTM). We also investigate a Recurrent Neural Network (RNN), specifically LSTM, since LSTM is a natural architecture for dealing with sequences and achieves great success in areas like speech recognition and image captioning. We build the network with three-LSTM layers followed by a dense layer of softmax neurons for classification.

# V. EXPERIMENTS AND EVALUATION

In this section, we first measure the properties of our graph encoding method. Then we evaluate the performance of the app profile representation for different applications, including malware detection, malware family classification, app functionality classification, and app version detection. We collect a large number of app dataset 80,178 apps for our evaluations.

# A. Experiment Configuration

We employ FlowDroid [7] to build the model of Android component lifecycles and callback methods, and use Soot [19] to extract function call graph of each app. We build our autoencoder, DNN, CNN and LSTM models with TensorFlow 1.0.0. All training process and experiments are conducted on a server equipped with a 12-core i7 Intel CPU, 64G of RAM and 4 Titan X GPUs.

We collect 61,330 apps from AndroZoo (apps of different years), which have been tested to be benign by VirusTotal $^{2}$ . We also collect a malicious app dataset from VirusShare $^{3}$ and Drebin [10]. Table II gives the detail of our dataset.

TABLE II OVERVIEW OF OUR DATASETS. 

<table><tr><td>Category</td><td>Name</td><td>Samples</td></tr><tr><td rowspan="3">Benign</td><td>AndroZoo 2013</td><td>23397</td></tr><tr><td>AndroZoo 2014</td><td>28203</td></tr><tr><td>AndroZoo 15&amp;16</td><td>9730</td></tr><tr><td colspan="2">Total Benign:</td><td>61,330</td></tr><tr><td rowspan="3">Malware</td><td>VirusShare 2013</td><td>6028</td></tr><tr><td>VirusShare 2014</td><td>13724</td></tr><tr><td>Drebin</td><td>5250</td></tr><tr><td colspan="2">Total Malware:</td><td>25002</td></tr></table>

# B. Function Call Graph Encoding

Our encoding mechanism transfers function call graphs into vectors satisfying three requirements defined in SectionIII-A. As the encoding process is deterministic (except the loop-breaking procedure), a function call graph typically has a uniquely encoded vector. Here we evaluate the similarity-preserving (i.e., preserving graph and subgraph similarity) and robustness properties of our encoding mechanism, as well as compare different encoding strategies.

$^{2}$ VirusTotal: https://www.virustotal.com/zh-cn/

$^{3}$ VirusShare: https://virusshare.com/

![](images/e592b4ea23307eb9133895b334e1c2537d763dcd06e784e5cb4d2841be0e420b.jpg)



(a) Nodes/Edge count distance vs. DTW distance.

![](images/6da90ca77afc65e2082a3102ca5455fe8a45d081cb9a95b76650dc7cae6e2f9c.jpg)



(b) Nodes/Edge proportion distance vs. DTW distance.   
Fig. 6. Graph distance of apps and corresponding DTW distance of graph encoded vectors.

Similarity preserving and Robustness. We use graph edit distance to measure similarity between graphs, and use dynamic time wrapping (DTW) to measure similarity between encoded vectors. The consistence of original graph edit distance and encoded DTW distance implies the similarity preserving property of our encoding method. Specifically we randomly choose 4000 apps from our dataset with diverse sizes. By randomly adding nodes (i.e., system functions) and edges (i.e., call relationship) to each app's function call graph, we obtain pairs of original graph and modified graph and generate original and modified encoded vectors for them correspondingly. Then we calculate both graph edit distance and DTW distance for each pair of original version and modified version. The average results for 4000 apps are presented in Fig. 6, which shows that the DTW distance is proportional to both node edit distance and edge edit distance. Our simulation results show that our encoding is robust against both node insertion and edge insertion attack: a small amount of inserted code (e.g., 200 functions) only causes slight change to the vector. Attacks such as renaming user defined functions, and reordering code won't change the encoded vectors. In our simulation, edge modification causes less fluctuation to the encoded vector while adding node causes larger fluctuation. The reason could be that adding an edge often does not introduce a new package for the called system functions, while adding a new system function at lower layer may introduce a new package, thus causing modifications of the encoded vector. Note that, adding a new system function from a new package often implies a behavior change by the function. Especially, if we add nodes in the layer user defined functions (i.e., $\mathcal{F}_{LU}$ ), this will lead to behavior changes to $\mathcal{F}_{HU}$ as shown in Fig. 4(b). To some extent, given two similar function call graphs, our encoding method can preserve their similarity effectively.

Different encoding strategies. With our carefully designed visiting order method detailed in Section III-D, we implement two encoding strategies which traverse the whole graph depth first (DFS) and breadth first (BFS), and we denote as DFS and BFS respectively. As comparison, we implement an encoding strategy which traverses the graph by DFS and order each same layer's user defined functions by their names' lexicographic, denoted by DFS\_byFunc. We also implement a DFS traverse (denoted as DFS\_NoOrder) that visits the functions at same layer randomly without using any ordering criteria. For 4000 randomly chosen apps, we encode them by four strategies, and evaluate different encoding strategies' effectiveness by using them for malware detection. Fig. 7 illustrates the recall and precision of four strategies. DFS, BFS and DFS\_byFunc achieve comparably high accuracy, and all of them significantly outperform the strategy without ordering. However, DFS\_byFunc is not robust to function renaming: its malware detection accuracy drops to around 1% when we randomly change the names of user defined functions (thus resulting in substantial perturbation of graph encoding vector). Among them, DFS performs the best as it approximately preserves the execution sequence. The results affirm the stability of our proposed encoding method. We use DFS for all reported experiment results in rest of this section.

Efficiency. In our implementation, extracting function call graph takes about 46.5 seconds for one app. Encoding a function call graph takes about 0.68s on average (1s when processing loops), and the average size of encoded vectors is 6341. It takes about 18 minutes to train the autoencoder model using 23397 samples from AndroZoo 2013 to achieve a minimal loss, while it takes 0.66s to produce 3507 apps' 64-dimension profile representations.

# C. Application Driven Evaluation

We generate the 64-dimension profile representations for all apps once, and use them for different applications.

Model training and metrics. For each task, we use 64-dimension app representations as input to train a target Support Vector Machine (SVM) classifier. We use 85% data as training set and the rest 15% as test set. For classification tasks, we use standard accuracy, precision, recall, and F-score = 2 · $\frac{precision \cdot score}{precision + recall}$ as metrics. For every experiment, we perform 5-fold across validation.

1) Malware Detection: We use the VirusShare 2013 and 2014 malware datasets, and AndroZoo 2013 and 2014 benign datasets as negative and positive samples, to evaluate the malware detection accuracy of our 64-dimension app representations. As shown in Table III, for the VirusShare 2013 and AndroZoo 2013 datasets, we classifies 4024 (benign/malware) apps using around 5.06 second with a 92% F-score and 93.07% accuracy. When we use datasets of 2013 as training data, and test the results on datasets 2014, we can still achieve 82% F-score and 85% accuracy. The accuracy degradation is caused by the malware evolution across years. Mixed all data together, the F-score is 89% and accuracy is 89.74%. Surprisingly, using only 64-dimension (one dimension is represented by one float) profile representation, we achieve such a high accuracy for malware detection. This affirms the power of our compact app profile representation.

TABLE III
MALWARE DETECTION ACCURACY FOR DIFFERENT YEARS' DATASETS. 

<table><tr><td>TestData</td><td>TrainData</td><td>Prcs</td><td>Recl</td><td>F-score</td><td>Accuracy</td></tr><tr><td>2013</td><td>2013</td><td>93%</td><td>92%</td><td>92%</td><td>93.07%</td></tr><tr><td>2014</td><td>2014</td><td>88%</td><td>85%</td><td>83%</td><td>85.00%</td></tr><tr><td>2014</td><td>2013</td><td>87%</td><td>84%</td><td>82%</td><td>84.18%</td></tr><tr><td>13 &amp; 14</td><td>13 &amp; 14</td><td>91%</td><td>90%</td><td>89%</td><td>89.74%</td></tr></table>

\- As introduced in Section IV-B, we also implement three supervised learning models to extract task-oriented representations, including DNN, CNN and RNN models as comparison. Here we use the malware detection task to measure different models' effectiveness. We tune all hyper parameters to achieve the best results. As shown in Fig. 8, for datasets of 2013, the accuracy for autoencoder is 93.07%, for DNN is 95%, for CNN is 90%, and for RNN is 67%. When testing datasets of 2014 on model trained by datasets of 2013, the accuracy for autoencoder is 84.18%, for DNN is 86%, for CNN is 84%, and for RNN is 61%. Among all models, supervised DNN performs the best, while our unsupervised autoencoder provides similar accuracy as CNN. As our encoded function call graph vectors contains less sequential information, which may cause the lower accuracy of RNN.

![](images/065d67d808877f082a286f14a828f2c32fd2056cc284ad5ff2eb57a465c6b42b.jpg)



Fig. 7. Different encoding strategies' performance for malware detection.

![](images/419ff97e908c99bd7b1344ef661ceb515e36fd1e6aa3caf3d4195ff82ea989fe.jpg)



Fig. 8. Malware detection accuracy for different learning models.

![](images/a0a45cf93102b9c527d002d1b5e2262fb651caa32edc37b1baea81d358e21f79.jpg)



Fig. 9. Detection accuracy for the largest 21 malware families.

![](images/9f0b7e753a19bb992a011222deb4c22f97a9c3433e4baf9db20607b7017dee6b.jpg)



Fig. 10. Pair-wise distances of 9 apps' different versions.

2) Malware Family Classification: Usually malware belong to different families, and malware of the same family possess similar behaviors. Here we perform family classification on Drebin dataset, which provides labels of malware family. Fig. 9 presents the classification accuracy for the 21 largest families in the dataset. The average accuracy is 82.81%. For 8 families, their accuracy are above 90%. The accuracy for the 5th, 11th, and 15th families are relatively low could due to 1) their small sample sizes, or 2) malware being Downloaders. Overall, our app representation provides high accuracy results for malware classification.

3) Functionalities Classification: Our 64-dimension profile representations also contain rich information about apps' functionality, as a result can be used for functionality classification. We label 9,730 apps in AndroZoo 2015 and AndroZoo 2016 according to 7 categories in Google Play, including personalization, health\_and\_fitness, travel\_and\_local, books\_and\_reference, entertainment, communication, music\_and\_audio. We apply 7-class classification on their profile representations, and the average accuracy is $33.3\%$ . In order to better understand the results, we apply two-class classification on 3,576 apps from two categories (i.e., 2,486 music\_audio apps and 1,090 communication apps). As presented in Table IV, we achieve $64\%$ F-score and $74\%$ accuracy. We manually investigate the incorrectly classified apps, and remove 341 inappropriate apps who are mis-labeled or have multiple functionalities and retrain the model, the F-score is $84\%$ and the accuracy is $88.1\%$ . It's worth noting that, as reported in our online survey in Section I, in existing app markets, many apps are categorized incorrectly or inappropriately, which degrades the user experience as well as increases the difficulty for app recommendation. So, our app profile representations can be utilized for better app categorizing and recommendation.

TABLE IV
TWO FUNCTIONALITIES CLASSIFICATION: MUSIC& AUDIO VS COMMUNICATION. 

<table><tr><td>State</td><td>Precision</td><td>Recall</td><td>F-score</td><td>Accuracy</td></tr><tr><td>Original dataset</td><td>81%</td><td>74%</td><td>63%</td><td>74%</td></tr><tr><td>Cleaned dataset</td><td>90%</td><td>88%</td><td>84%</td><td>88.1%</td></tr></table>

4) App Version Detection.: Here, we use our app representations to analyze different versions of the same app. We collect 160 apk files, which are different versions of 9 different apps. We measure the pairwise DTW distances of their representations and present the results in Fig.10. The diagonal deep blue areas imply that, the DTW distance among different versions of the same app is significantly smaller than distances among different apps. That's because different versions of the same app possess similar code structures and behaviors with limited changes. So, our profile representation can also be used for tasks like app plagiarism detection.

# VI. RELATED WORK

Privacy-preserving has always been a vivid topic in research area [21]–[25]. Especially, mobile applications carry rich sensitive personal information has attracted great attention. There are many work focusing on Android application analysis, according to the difference of their approaches we roughly divide these work into two categories. One focuses on fine-grained behavior analysis in a way of static or dynamic or both of them. While the other one tries to extract features and then uses machine learning methods to do classification.

# A. Behaviour-based Analysis

Some techniques have been proposed to analyze Android application's behavior. For example, CHEX [8] aims to detect component hijacking vulnerabilities in Android applications. Many work [7], [26] have exercised data flow analysis to identify sensitive data leakage, and AppIntent [27] combines static and dynamic analysis to identify user unintended transmission of sensitive data. TriggerScope [28] focuses on the detection of logic bomb guarded potential malicious functionality. These studies have promoted the malware detection work and helped us learn the features of app's behavior. They can effectively detect certain maliciousness, but also need high overhead.

# B. Machine Learning-based Methods

Different with behavior-based detection, another line of work focuses on (manually) extracting useful features to classify benign and malicious app. For example, Drebin [10] has collected permission-based, sensitive API and network address as malware features and used machine learning techniques for automatically separating malicious and benign applications. [11] proposed function call graph based structure detection of android malware using machine learning. DroidSIFT [12] introduced weighted contextual API dependency graphs and used graph similarities as the feature vector for classification. AppContext [29] showed that app's behavior's context is an important feature to understand its behavior's properties.

As the features and classifiers are both important in contributing to classification results, our approach uses function call graph to express the application's behaviour, and leverages unsupervised deep learning to extract compact features to characterize its behavior.

# VII. CONCLUSION

In this work we propose APPDNA for efficient automatic app profiling using graph-based deep learning. We demonstrate its efficiency by studying its application for accurate and efficient malware detection, malware family classification, app functionality categorization and app version detection. We carefully design a considerably robust graph-encoding method to convert a function-call graph into a vector that preserves certain graph structural information and is robust to a range of transformation attacks. An autoencoder based unsupervised learning model is designed to transform the encoded vector into 64-dimension compact representation for each app. Our extensive experimental evaluations demonstrate that our design enables efficient training and prediction (with time less than 1.5ms per apk) while results in comparable high prediction/classification accuracy with previous studies.

# VIII. ACKNOWLEDGMENTS

Lan Zhang and Xiang-Yang Li are the contact authors. The research is partially supported by the National Key R&D Program of China 2017YFB1003000, China National Funds for Distinguished Young Scientists with No. 61625205, NSFC No. 61572281, No. 61472218, No. 61520106007, Key Research Program of Frontier Sciences, CAS, No. QYZDY-SSW-JSC002, NSF ECCS-1247944, and NSF CNS 1526638.

# REFERENCES

[1] "Number of apps available in march 2017," https://goo.gl/eCmQsv.   
[2] "Smartphone os market share," https://goo.gl/zKLJ2G.   
[3] "Mobile threats," https://goo.gl/9Otynw.   
[4] B. Reaves, J. Bowers, S. A. Gorski III, O. Anise, R. Bobhate, R. Cho, H. Das, S. Hussain, H. Karachiwala, N. Scaife et al., “\* droid: Assessment and evaluation of android application analysis tools,” ACM Computing Surveys (CSUR), vol. 49, no. 3, p. 55, 2016.   
[5] X. Wei, L. Gomez, I. Neamtiu, and M. Faloutsos, "Profiledroid: multilayer profiling of android applications," in MobiCom. ACM, 2012, pp. 137-148.   
[6] X. Cui, J. Wang, L. C. Hui, Z. Xie, T. Zeng, and S.-M. Yiu, "Wechecker: efficient and precise detection of privilege escalation vulnerabilities in android apps," in WiSec. ACM, 2015.

[7] S. Arzt, S. Rasthofer, C. Fritz, E. Bodden, A. Bartel, J. Klein, Y. Le Traon, D. Octeau, and P. McDaniel, "Flowdroid: Precise context, flow, field, object-sensitive and lifecycle-aware taint analysis for android apps," ACM SIGPLAN Notices, vol. 49, no. 6, pp. 259–269, 2014.   
[8] L. Lu, Z. Li, Z. Wu, W. Lee, and G. Jiang, "Chex: statically vetting android apps for component hijacking vulnerabilities," in CCS. ACM, 2012, pp. 229–240.   
[9] C. Gibler, R. Stevens, J. Crussell, H. Chen, H. Zang, and H. Choi, "Adrob: Examining the landscape and impact of android application plagiarism," in MobiSys. ACM, 2013.   
[10] D. Arp, M. Spreitzenbarth, M. Hubner, H. Gascon, K. Rieck, and C. Siemens, "Drebin: Effective and explainable detection of android malware in your pocket." in NDSS, 2014.   
[11] H. Gascon, F. Yamaguchi, D. Arp, and K. Rieck, "Structural detection of android malware using embedded call graphs," in Workshop on AISec. ACM, 2013, pp. 45–54.   
[12] M. Zhang, Y. Duan, H. Yin, and Z. Zhao, "Semantics-aware android malware classification using weighted contextual api dependency graphs," in CCS. ACM, 2014, pp. 1105-1116.   
[13] R. Pascanu, J. W. Stokes, H. Sanossian, M. Marinescu, and A. Thomas, "Malware classification with recurrent networks," in ICASSP. IEEE, 2015, pp. 1916-1920.   
[14] Z. Yuan, Y. Lu, Z. Wang, and Y. Xue, "Droid-sec: deep learning in android malware detection," in ACM SIGCOMM Computer Communication Review, vol. 44, no. 4. ACM, 2014, pp. 371–372.   
[15] M. e. Niepert, "Learning convolutional neural networks for graphs," in ICML. ACM, 2016.   
[16] A. Grover and J. Leskovec, "node2vec: Scalable feature learning for networks," in Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2016, pp. 855-864.   
[17] B. Perozzi, R. Al-Rfou, and S. Skiena, "Deepwalk: Online learning of social representations," in Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2014, pp. 701–710.   
[18] J. B. Lee and X. Kong, "Skip-graph: Learning graph embeddings with an encoder-decoder model," 2016.   
[19] "Soot," https://sable.github.io/soot/.   
[20] G. E. Hinton and R. R. Salakhutdinov, "Reducing the dimensionality of data with neural networks," Science, vol. 313, no. 5786, pp. 504-507, 2006.   
[21] J. Qian, F. Han, J. Hou, C. Zhang, Y. Wang, and X.-Y. Li, "Towards privacy-preserving speech data publishing," in INFOCOM. IEEE, 2018.   
[22] J. Qian, X.-Y. Li, C. Zhang, and L. Chen, "De-anonymizing social networks and inferring private attributes using knowledge graphs," in Computer Communications, IEEE INFOCOM 2016-The 35th Annual IEEE International Conference on. IEEE, 2016, pp. 1-9.   
[23] X.-Y. Li, C. Zhang, T. Jung, J. Qian, and L. Chen, "Graph-based privacy-preserving data publication," in Computer Communications, IEEE INFOCOM 2016-The 35th Annual IEEE International Conference on. IEEE, 2016, pp. 1–9.   
[24] L. Zhang, X.-Y. Li, K. Liu, T. Jung, and Y. Liu, "Message in a sealed bottle: Privacy preserving friending in mobile social networks," IEEE Transactions on Mobile Computing, vol. 14, no. 9, pp. 1888–1902, 2015.   
[25] X.-Y. Li and T. Jung, "Search me if you can: privacy-preserving location query service," in INFOCOM, 2013 Proceedings IEEE. IEEE, 2013, pp. 2760-2768.   
[26] W. Enck, P. Gilbert, S. Han, V. Tendulkar, B.-G. Chun, L. P. Cox, J. Jung, P. McDaniel, and A. N. Sheth, "Taintdroid: an information-flow tracking system for realtime privacy monitoring on smartphones," TOCS, vol. 32, no. 2, p. 5, 2014.   
[27] Z. Yang, M. Yang, Y. Zhang, G. Gu, P. Ning, and X. S. Wang, "Appintendent: Analyzing sensitive data transmission in android for privacy leakage detection," in CCS. ACM, 2013, pp. 1043-1054.   
[28] Y. Fratantonio, A. Bianchi, W. Robertson, E. Kirda, C. Kruegel, and G. Vigna, "Triggerscope: Towards detecting logic bombs in android applications," in SP. IEEE, 2016.   
[29] W. Yang, X. Xiao, B. Andow, S. Li, T. Xie, and W. Enck, "Appcontext: Differentiating malicious and benign mobile app behaviors using context," in ICSE, vol. 1. IEEE, 2015, pp. 303–313.