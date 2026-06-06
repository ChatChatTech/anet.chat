# AppDNA: Profiling App Behavior via Deep-Learning Function Call Graphs

Anran Li∗, Shuangshuang Xue∗, Xiang-Yang Li∗, Fellow, ACM, Lan Zhang∗, Member, IEEE, Jianwei Qian† ∗ University of Science and Technology of China † Illinois Institute of Technology

Abstract—The growing number and diversity of applications make malware detection and app recommendation for users more challenging. In this work, we design a framework APPDNA to automatically generate a compact representation for each app to comprehensively profile its behaviors. The versatile representation can be generated once for each app, and then be used for a wide variety of objectives, including malware detection, app categorization and app version detection, etc. We propose to conduct a function-call-graph-based app profiling scheme based on a comprehensive and deep understanding of an app’s behaviors. We design a graph-encoding method to convert a large function call graph to a 64-dimensional fixed length vector to achieve robust app profiling. Our extensive evaluations on 86,332 apps demonstrate that our approach performs app profiling with high accuracy and low computation cost: it takes about 46.5 seconds for one app to extract its function call graph; 0.68 seconds to encode a function call graph; it classifies all 4,024 (benign/malware) apps in around 5.06 seconds with accuracy about 93.07%; it classifies all 570 malicious apps’ family (21 families in total) in around 0.83 seconds with accuracy 82.3%; it classifies 9,730 apps’ functionality into 2 categories with accuracy 88.1% or into 7 categories with accuracy 33.3%.

Index Terms—Malware detection, App profiling, Graph embedding, Deep learning.

# 1 INTRODUCTION

A Large number of mobile applications have been developedto provide rich services ranging from news, weather, so- to provide rich services ranging from news,weather, social communication and entertainment to medical, fitness and finance. Application markets are playing an important role in the popularity of Android devices and driving the economy of Android applications. Google Play Store now hosts more than 2.8 million apps, and Apple Store hosts 2.2 million apps [1]. The considerable quantity and rich app applications, being big data, have raised new interesting and challenging issues though. Firstly, ubiquitous Android phones has become a worthwhile target for attacks on users’ privacy-sensitive data. Different kinds of Android malware have been found and one of the main threats is privacy infringement [2], i.e., exposing users’ sensitive information such as location information, contact data, images, and SMS messages to attackers. Secondly, for threat measurement and defense planning, it is also crucial to differentiate malware of different families (e.g., malware family classification). Thirdly, it is difficult for application markets to categorize the large quantities of apps. We conducted an online survey among 224 respondents with diverse occupations, 53.13% of whom use Android phones and 38.83% use iOS phones. Of the respondents, 42.86% were unsatisfied with the app categorization by the existing markets, and 49.55% thought the keywords and descriptions provided by the markets were inconsistent to the functionalities of those apps. Finally, the rapid proliferation of apps makes it difficult for users to locate apps of interest. Thus, effective app recommendation is very imperative [3].

To address the aforementioned issues, we require a deep and comprehensive understanding of apps’ behaviors, an efficient way to profile different apps, as well as an effective method to measure the similarity between apps. In the literature, there are mainly two branches toward analyzing app features and behaviors. The first branch conducts fine-grained behavior analysis based on source code in a static, dynamic or mixed way. Dynamic analysis methods require adequate test runs to achieve appropriate code coverage, which is the main challenge to comprehensively understand apps’ behaviors [4]. Static analysis methods can achieve relatively high code coverage, but it cannot deal with inherent limitations like reflection, dynamic loading and native code [5]–[7]. The second branch focuses on extracting pre-defined features from apps. For instance, DroidAPIMiner [8] extracts relevant features at API level and leverages KNN to detect malware apps. Authors of Drebin [9] collected permission-based, sensitive API and network address as malware features. Some recent works extract malware features during app execution using recurrent neural network (RNN) in a supervised way [10]. Then supervised learning model, e.g., SVM, Naive Bayes, and deep belief network, are applied on these features to detect malware. Although these methods are efficient in malware detection, their limitations include handcrafted taskspecific features and dependence on manually labeled training data. Both pre-defined and auto-extracted features cannot comprehensively characterize diverse app behaviors as a result of being tailored for malicious behaviors. In addition, those methods use supervised learning, which relies on extensive labeled training data. However, towards different objectives like functionality categorization and plagiarism detection, available labeled training data is limited in both categories and quantity.

We propose a framework to automatically generate a compact representation for each app to comprehensively profile its behaviors. Apps with similar behaviors, such as benign/malicious functionalities, have similar representations too. The versatile feature representation can be generated once for each app, and then be used for various objectives, including malware detection, malware family detection, app categorization, and plagiarism detection. We leverage deep neural network to learn behavior feature representations from the corresponding function call graphs (FCG) in an unsupervised manner. The function call graph of an app is generated through static analysis (using tool of Soot and Flowdroid). Previous works have shown that FCG is sufficient for representing an app’s behaviors and more efficient to generate and store than other function graphs like inter-procedural control flow graph [11]–[13] (see details in Section 6).

To make app feature learning efficient and effective, we need to address the following critical challenges. First, though some graph-based learning works were proposed (e.g, Node2vec [14], DeepWalk [15], Skip-graph [16]), large-scale directed graphs like function call graphs still remain to be explored. Existing efforts focus on single large-scale social network embedding [17] or small graph analysis [18], ignoring large-scale graphs with significant differences in size. Second, the methods for encoding graphs should preserve the function call relationships and function properties. Meanwhile, the encoding should be robust enough to evasion techniques like code reordering and function renaming. Third, app behaviors can be very complex and diverse, so it is exceedingly challenging to generate a both versatile and compact representation applicable to a variety of objectives. Finally, we must profile apps in an unsupervised learning mode to avoid the time-consuming manual labor.

To the best of our knowledge, we are the first to learn taskagnostic representations from graphs in an unsupervised manner. We design APPDNA with the following contributions:

• We propose an autoencoder based neural network to learn the fix-sized compact representation of apps in order to comprehensively profile app behavior in an unsupervised way. The versatile representations can be used for various objectives, e.g., malware detection, malware family classification, and app functionality categorization. As a comparison, we further design three supervised learning models and implement four benchmarks to show the superiority of APPDNA.   
• We design a novel method to encode function call graphs into vectors which well preserve graph structure and node properties. Our encoding method is robust to various evasion techniques such as code reordering and function renaming (see details in Section 3.4-3.6).   
• Compared with our previous conference version [19], we further explore two dimension reduction methods to compress large encoded vectors so as to reduce both computation and storage overhead. We also employ five different hashing methods as the building block of our framework and analyze their differences.   
• We conduct extensive experiments using 119, 275 apps to demonstrate that our system performs app profiling with high accuracy and low computation cost. The results show that with one representation for each app, we achieve 93.07% accuracy for malware detection, 82.3% accuracy for malware family classification, and 88.1% accuracy for app functionality categorization with 2 categories. We achieve 88% accuracy for extremely large apps’ malware detection. It takes about 46.5 seconds for one app to extract its function call graph; 0.68 seconds to encode a function call graph and it takes 0.66 seconds to produce 3,507 apps’ 64-dimensional profile representations. (see details in Section 6.7) Additionally, we evaluate how varying the number of hash codes bits affects the performance (see details in Section 6.6).

![](images/b039a73b80f59af2ab8355fcd05f5e649cf8382cd7563b4e1c5896a9d66119e4.jpg)



Fig. 1. APPDNA framework to generate app profile.

APPDNA works as the DNA of an app, which determines the particular behavior of every app, and is responsible for characterizing whether it is malware, its malicious family and functional category. The rest of the paper is organized as follows. The overview of our system design is presented in Section 2. We introduce the encoding method for call graph in Section 3, technologies of dimension reduction or large vectors compression in Section 4 and the unsupervised deep learning model in Section 5. Comprehensive evaluation results are reported in Section 6. We discuss some open issues and findings in Section 7, review existing android application analysis and graph-based learning problem in Section 8, and conclude the work in Section 9.

# 2 SYSTEM OVERVIEW OF APPDNA

# 2.1 Design Goal

Millions of apps with complex structures and highly diverse behaviors raise great challenges for a series of tasks, including app categorization, organization, recommendation, malware detection, and plagiarism detection. Towards efficiently performing these tasks, we propose to generate a task-agnostic representation for each app to profile its behaviors with following requirements.

• Comprehensiveness: The representation should systematically capture each app’s diverse behaviors. Thus, the versatile representation can be used for various tasks, including malware detection, malware family classification, and app functionality categorization.   
• Similarity-preserving: The distance between the representation of apps should be strongly correlated to their behavior similarity. Thus, two apps that have similar behaviors should have similar representations.   
• Compactness: The representation should be as compact as possible in order to achieve highly efficient storage and computation, e.g., clustering and classification, when dealing with large amount of apps.

# 2.2 Design Overview

In this work, we propose a framework APPDNA with four designed components to generate the desired profile representation for each app. We use a function call graph to capture each app’s comprehensive behavior information, since app behaviors can be reflected in calling a series of system functions. Then, we leverage unsupervised deep learning to automatically extract compact representations based on function call graphs. The compact representations should satisfy the three requirements mentioned in Section 2.1. To feed a directed graph into a neural network, we propose a graph encoding method to transfer a function call graph into a feature vector while preserving the function calling relationship and function properties. To deal with large encoded vectors, we conduct dimension reduction and further cutting to yield inputs of smaller size for the neural network (see Section 4).

Fig. 1 presents the overview of our framework. Given an app, its profile representation is generated by the following steps:

1) Function call graph extraction: Soot [20] and FlowDroid [21] are used to extract a function call graph from the app (see Section 3.2).   
2) Graph encoding: Taking the function call graph as input, our designed encoding method transfers the graph into a vector (see Section 3.3).   
3) Dimension Reduction: The graph encoded vector’s size varies considerably, so we conduct dimension reduction for those extremely large encoded vectors (reaching a threshold value $\beta ,$ thus optional) to reduce computation overhead and storage overhead (see Section 4).   
4) Unsupervised representation learning: We feed encoded vectors of function call graphs into an autoencoder-based neural network to extract a compact profile representation for the app (see Section 5).

# 3 FUNCTION CALL GRAPH ENCODING

Before feeding function call graphs into a neural network to obtain a highly compact representation, we need to transfer graphs into vectors. In this section, we present the concrete design of our graph encoding mechanism that preserves graph structures.

# 3.1 Design Principle

The encoding mechanism should maintain complete function call relationships and function properties, as well as meet the following requirements.

• Uniqueness: A unique function call graph should have a unique encoded vector.   
• Preserving graph and subgraph similarity: Given two similar function call graphs, they should have similar encoded vectors; given two function graphs possessing similar subgraphs, their encoded vectors should have similar sub-vectors.   
• Robustness: Since our ultimate goal is to profile the behaviors of apps and compare their behaviors’ similarity, the encoding method should be robust against benign and malicious modifications, which do not change the apps’ behaviors, to the function graphs. Such modifications include identifier or function renaming, code reordering, junk code insertion, function outlining and inlining 1 (see details in Section 6.2).

# 3.2 Function Call Graphs

The function call graph (FCG) provides a sufficient description of an app’s source code level behaviors. There are other two alternatives: Control flow graph (CFG) and Interprocedural Control flow graph (ICFG). We leverage FCG instead of CFG and ICFG for two reasons. Firstly, FCG’s structure is quite simpler than CFG or ICFG and more efficient to extract and store. Secondly, FCG reserves sufficient information about the app’s behaviors which

1. Note that, some transformation attacks like dynamic code loading require dynamic analysis, which are out of the scope of this work.

![](images/7c39748277391fafa9908b864c95e5bf863952fd30f59c6f5d10c80596462afd.jpg)



Fig. 2. A simple example of function call graph (package names, return types, etc, are omitted). This call graph is extracted from a malicious app named Mania.

can be reflected by a series of system function calls (see details in Section 6). The definition of FCG is as follows.

Definition 1 (Function Call Graph). Given an app, its function call graph is a directed graph $G = ( V , E , L )$ , where:

• The vertex set V is a finite set of nodes, each $v \in V$ representing one of the app’s functions, including both userdefined functions and system functions (i.e., API). In the rest of this paper, we use “node” and “function” interchangeably;   
• The edge set $E$ represents the call relationships among functions, where a directed edge $( v _ { 1 } , v _ { 2 } )$ indicates a call from the function represented by the node $v _ { 1 }$ to the function represented by the node $v _ { 2 } ;$   
• L is the set of labels for all nodes, where each label consists of a function’s package name, class name, return type, function name, parameter types, and a counter recording how many times the function has been called. A label can represent a function uniquely.

Function call graph generation. We conduct static analysis on an apk file to extract the function call graph. Unlike Java programs, Android apps don’t have a main function, instead contain many entry points, that is, those methods are implicitly called by the Android framework. As a result, we use a Java optimization and analysis framework Soot [20] to extract function call graphs, and use FlowDroid [21] to create a dummy main function for the whole app. Fig. 2 gives a simple example of function call graph2. Specifically, each call graph has one root node referred as “DummyMain” node. The root node’s children nodes (i.e., entry nodes or entry functions) are all user-defined functions. Note that these entry functions are called at runtime without a fixed order [21].

# 3.3 Main Idea for Encoding Function Call Graphs

A naive idea to encode a directed graph is using its adjacency matrix. Although an adjacency matrix preserves complete information of all edges, it cannot be adopted as the input of the neural network for three reasons. First, since different apps possess different sets of functions (i.e., nodes), to support similarity measurement between apps, adjacency matrices should contain the same set of all possible nodes, which results in very large and sparse matrices. As shown in Fig. 3, 50% apps have more than 2000 nodes and 20% apps have more than 4000 nodes, and the largest app has about 14000 nodes; meanwhile 50% apps have more than 7000 edges and 20% apps have more than 16000 edges. To feed these adjacency matrices into neural network,

2. For simplicity of expression, the two nodes labeled sendTextMessage() in Fig. 2, are actually the same node and represent the same system function.

![](images/ebdbffc3a26b8b26e54f057b73044ae2f13e8bb86d9b43a7b34609d6f62d0cda.jpg)



(a) Node number distribution.

![](images/6a78c5992706306e4c54b414aa3bf3e729205f732fdc41dc3e8a9ac5b3e7fa9c.jpg)



(b) Edge number distribution.   
Fig. 3. The cumulative distribution (CDF) of the number of nodes and edges of function call graphs of different years.

zero padding should be applied first as the result of fixed-size inputs being needed. Thus, it requires 14000 × 14000 matrices for all apps, while most of them are quite sparse. Second, function nodes have diverse labels, which are important for app behaviors understanding. As a result, extra models are needed to encode nodes’ labels. However, learning a representation from multiple models simultaneously is still a quite challenging issue. Third, adjacency matrices are not robust against the aforementioned modifications, e.g., function renaming. Therefore, the adjacency matrix does not meet the robustness requirements.

In this work, we propose a mechanism to traverse function call graphs and build an encoded vector simultaneously. Once a node vi is visited, its properties are encoded by a function Code(·) and concatenated to the vector. To preserve call relationships and node properties, as well as meet the principles outlined in Section 3.1, it is essential to determine a proper visiting order and encoding function Code(·).

# 3.4 Visiting Order

Depth-first search and breadth-first search methods can be used in generating graph encoded vectors. We start the traversal from the root node (i.e., DummyMain) and then visit all its descendant nodes (visit once for each node) in either depth-first search or breadth-first search manners. There are two issues that need to be noticed. Firstly, we need to determine the order to visit nodes in the same layer, which can influence sub-vectors’ positions significantly. For example, it is important to determine the visiting order of the entry function nodes (introduced in Section 3.2), which are called at runtime without a fixed order. So, we design a rule to fix the visiting order across different apps, in order to yield similar visited node sequences for graphs with similar behaviors. Secondly, the visited node sequence should not be sensitive to modifications including identifier or function renaming, code reordering, junk code insertion, and function outlining and inlining.

There are two types of functions, system function and userdefined function, each of which requires a visiting order. For system functions, we order them by the lexicographical order of their function signatures (created from package name, class name, return type, function name, and parameter types), since signatures of system functions are stable and consistent across apps. For userdefined functions, as all label components, e.g., package name and function name, of a user-defined function can easily be modified by developers, getting fixed-order encoded vectors for them is challenging. We propose the solution based on following two insights.

Insight 1: Despite the labile label of a user-defined function, its behavior is performed by calling a series of system functions, which are stable and consistent across apps. For example, two functions SendT hem() and threat() in Fig. 2 possess different labels, but perform the same behavior, i.e., calling system functions $g e t D e f a u l t ( )$ and sendT extM essage(). As a result, we can use the sets of system functions called by each userdefined function, referred to as system function set, to represent its behaviors as well as to determine the visiting order for all the user-defined functions.

![](images/ef1e116f0e0b6b4f61ad020c2a32ba245b85af12ed89d9abb51482ac3e7a1ca8.jpg)



(a) Package count of packages called by user-defined functions.

![](images/7455942f5616ce0bc6ea4ed3e2daf73789f2f9748c5eb2a7e240fe5d857f9aa8.jpg)



(b) Hybrid nodes affected by perturbing Last-layer nodes. obfcount: the number of nodes added to the last layer.   
Fig. 4. Function call statistics about our datasets.

Insight 2: Given a set of system functions, a developer may reorder their positions in the source code without changing the app’s behavior. For example in Fig. 2, system functions getMessageBody() and getDisplayOriginatingAddress() can be called in any order, while both orders represent the same behavior. A developer can also change conditions (e.g., using if-else and switch-case structures) or use function outlining and inlining techniques to reorganize the code. As a result, our visiting order should not be sensitive to system functions’ order within a set.

Based on these two insights, we propose a relatively stable visiting order of user-defined functions by their behaviors, i.e., the composition of their system function sets. We leverage the idea of majority voting, despite the different order of system functions in each set. Specifically, given two user-defined functions A and B in the same layer, A should be visited before B if most system functions called by A are ranked before system functions called by B. In this way, package or function renaming and code reordering would not affect the ordering. Slight insertion or deletion of system functions would have little effect on the ordering.

Before we present the details of our algorithm, we list the frequently used notations in Table 1 for clarity.

TABLE 1 Notations, abbreviations, and examples in Fig. 2. 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $G$ </td><td>A function call graph.</td></tr><tr><td> $\mathcal{F}_{U}$ </td><td>User-defined function, UserFunc, e.g.,SendThem() and run().</td></tr><tr><td> $\mathcal{F}_{S}$ </td><td>System function (API), SysFunc, e.g.,SendTextMessage() and getDefault().</td></tr><tr><td> $\mathcal{S}(\mathcal{F}_{U})$ </td><td>System function set of  $\mathcal{F}_{U}$ , i.e., the set of system functions called by  $\mathcal{F}_{U}$ , e.g., for threat(), its system function set is {getDefault(), SendTextMessage()}.</td></tr><tr><td> $\mathcal{F}_{SU}$ </td><td>SecondLayerUserFunc, Second layer UserFunc(i.e., entry functions), whose parent node is “DummyMain”.</td></tr><tr><td> $\mathcal{F}_{LU}$ </td><td>LastLayerUserFunc, Last layer UserFunc, whose direct successor nodes are SysFuncs.</td></tr><tr><td> $\mathcal{F}_{HU}$ </td><td>HybridUserFunc, User function, whose direct successor nodes include both SysFuncs and UserFuncs.</td></tr><tr><td>Code(·)</td><td>Encoding function, generates a vector for the input.</td></tr></table>

Given a set of user-defined functions $S = \{ \mathcal { F } _ { U i } | 0 < i \leq$ $n \}$ that need to be sorted, each $\mathcal { F } _ { U i }$ has a set of called system functions, denoted as $\mathcal { S } ( \mathcal { F } _ { U i } )$ . For each system function $\mathcal { F } _ { S j } ~ \in$ ${ \cal S } ( \mathcal { F } _ { U i } ) , \mathcal { F } _ { S j }$ .count denotes the number of times that the function $\mathcal { F } _ { S j }$ is called by $\mathcal { F } _ { U i }$ . To get the value of count for each ${ \mathcal { F } } _ { S j }$ , we collect all system functions for each user-defined function and count their calling times. When there is a loop in the function-callgraph, we arbitrarily break the loop to get an approximate count value. For all system functions in the union set $\bigcup \ S ( \mathcal { F } _ { U i } )$ , 0<i≤n we order them by the lexicographical order, and give an index Index $( \mathcal { F } _ { S j } )$ to each system function $\mathcal { F } _ { S j }$ . Specifically, the index value here indicates priority, that is function with larger index is before those with smaller indices, Now, the priority of each userdefined function $\mathcal { F } _ { U i }$ is determined by the weighted sum of the system functions’ priorities in $\mathcal { S } ( \mathcal { F } _ { U i } )$ :

$$
\text { Priority } \left(\mathcal {F} _ {U i}\right) = \sum_ {\mathcal {F} _ {S j} \in \mathcal {S} \left(\mathcal {F} _ {U i}\right)} \operatorname{Index} \left(\mathcal {F} _ {S j}\right) * \frac {\mathcal {F} _ {S j} . \text { count }}{\text { MaxCount }}, \tag {1}
$$

where $M a x C o u n t \ = \ \operatorname* { m a x } ( \mathcal { F } _ { S j } . c o u n t )$ for all ${ \mathcal { F } } _ { S j } \in$ $\bigcup \ S ( \mathcal { F } _ { U i } )$ , i.e., the maximal count number a system function $0 < i \leq n$ has been called. Then, we can order these user-defined functions by their priorities. The detailed algorithm to order a set of user functions is summarized in Algorithm 1.

Algorithm 1 Visiting Order of User-Function   
Input:
1: A set of user functions $S_{U} = \{F_{Ui} | 0 < i \leq n\}$ .
2: System function set $\mathcal{S}(\mathcal{F}_{Ui})$ for each user function $F_{Ui}$ .
Output: Ordered $S_{U}$ 3: function ORDER( $S_{U}$ )
4: $S_{S} \leftarrow \bigcup_{0<i \leq n} \mathcal{S}(\mathcal{F}_{Ui})$ 5: MaxCount $\leftarrow \max(\mathcal{F}_{Sj}.count)$ for all $F_{Sj} \in S_{S}$ 6: $P \leftarrow \{p_{i} = 0 | 0 < i \leq n\}$ 7: for each $F_{Ui}$ in $S_{U}$ do
8: $p_{i} = \text{Priority}(\mathcal{F}_{Ui}, S_{S}, MaxCount)$ 9: end for
10: $S_{U}.Sortby(p_{i})$ 11: return $S_{U}$ 12: end function
13: function PRIORITY( $F_{Ui}, S_{S}, MaxCount$ )
14: $p = \sum_{\mathcal{F}_{Sj} \in \mathcal{S}(\mathcal{F}_{Ui})} Index(\mathcal{F}_{Sj}, S_{S}) * \frac{\mathcal{F}_{Sj}.count}{MaxCount}$ 15: return p
16: end function
17: function INDEX( $F_{Sj}, S_{S}$ )
18: ind $\leftarrow 0$ 19: for each $F_{Sk}$ in $S_{s}/F_{Sj}$ do
20: if $F_{Sj}.name > F_{Sk}.name$ then
21: ind++;
22: end if
23: return ind
24: end for
25: end function

# 3.5 Expressing API’s Behavior by Encoding Its Signature

The function call graph reserves sufficient information about an app’s behaviors which are combined with nodes’ behaviors, and each node’s behavior can be reflected in its calling system function set. When a node is visited, its behavior is encoded into a vector and concatenated to the graph vector $C o d e ( G )$ . The first problem we face is how to transform a node’s behavior into a vector. We propose to use the string hash function to transform system functions’ behaviors into vectors. Since a system function is uniquely determined by its signature which consists of five parts: package name, class name, return type, method name, and parameter types. Each part of the signature has its meaning in representing function’s behavior semantic. For example, the package name provides a high-level abstraction of API’s behavior, which shows its effectiveness in malware detection [22]. The class name and method name have a more fine-grained behavior meaning than package name, such as sendT extMessage() being obviously used to send a SMS. The return type and parameter types are effective in expressing the data flows among APIs’ [21], [23], which are important properties of API’s behavior.

Therefore, to figure out which part of the signature is effective in expressing $\mathbf { A P I } ^ { \ } \mathbf { s }$ behaviors, we need to answer whether it is appropriate to encode the whole signature or just some parts of it. Our later experimental results in Fig. 5 show that, in the application of malware detection, hashing the whole signature produces the highest accuracy. And the hash of the whole signature can also be applied to other objectives well.

# 3.6 Encoding User-defined Functions

When a node in the function call graph is visited, its behaviors are encoded into a vector and concatenated to the graph vector Code(G).

For system function, we adopt the method to generate a hash value for the label (e.g., the system function signature, excluding the count) of each system function. For user-defined function ${ \mathcal { F } } _ { U i }$ , there are two problems to consider. Firstly, we can generate the vector $C o d e ( \mathcal { F } _ { U i } )$ for $\mathcal { F } _ { U i }$ by concatenating values of all functions in $\mathcal { S } ( \mathcal { F } _ { U i } )$ , ordered by priorities. However, this will result in a very high-dimension $C o d e ( G )$ considering the large number of nodes of G (See Fig. 3). Secondly, we can generate the vector $C o d e ( \mathcal { F } _ { U i } )$ for $\mathcal { F } _ { U i }$ by only a single hash value for the set of system functions $\boldsymbol { S } ( \mathcal { F } _ { U i } )$ . However, the value would be too coarse-grained and sensitive to even slight modifications.

Thus, to achieve a reasonable trade-off, we generate vector $C o d e ( \mathcal { F } _ { U i } )$ for each user-defined function $\mathcal { F } _ { U i }$ by grouping system functions in $\mathcal { S } ( \mathcal { F } _ { U i } )$ by their package names. For each package group, we concatenate all its member system functions’ labels (excluding the counts) in the lexicographic order to get a string, then apply a string hash function (e.g., BKDR) to yield one hash value for each group. Then $C o d e ( \mathcal { F } _ { U i } )$ is obtained by concatenating values of all package groups according to the lexicographical order of their package names. In this way, we greatly reduce the length of each user-defined function’s hash value while maintaining sufficient behavior information of the function as well as robustness of encoding. For user-defined functions, statistics on our collected apps in Fig. 4(a) show that more than 75% of HybridUserFunc $\mathcal { F } _ { H U }$ called system functions from at least two different packages. And we adopt 32-bit to represent hash codes, and in Section 6.6, we evaluate how varying the number of bits affect the performance including accuracy and storage.

# 3.7 Graph Vector Generation

To put visiting order and encoding function together, we are ready to generate a vector $C o d e ( G )$ for a function call graph. Given G, we traverse the graph in depth-first order or breadthfirst order starting from the root node (dummyMain). For nodes in the same layer, their visiting order is determined by their priorities according to Algorithm 1. When a user-defined function $\mathcal { F } _ { U i }$ is visited, $C o d e ( \mathcal { F } _ { U i } )$ is generated according to Section 3.6, and concatenated to Code(G). Code(G) is generated when the traverse is completed. We show the detailed steps of graph vector generation in Algorithm 2.

![](images/b4abf0ee4a3538b71e32016473d652cbb1de0cd4284bedab95a58630c41d8422.jpg)



Fig. 5. The accuracy of malware detection for different hash strings.

![](images/510869d33756d82faf9fffea42c1b981ad6606342c1648bae12e3295eb7f5ac9.jpg)



Fig. 6. The accuracy of malware detection for different number of hash code bits.

Algorithm 2 Generate the encoded vector for an app   
Input: A set of entry functions $App = \{ \mathcal{F}_{SUi} | 0 < i \leq n \}$ .

1: System function set $\mathbb{S}_S(\mathcal{F}_U)$ and UserFunc set $\mathbb{S}_U(\mathcal{F}_U)$ , called by each UserFunc $\mathcal{F}_U \in App$ .

Output: Vector of App.

2: function CODE(App)

3:    vector = ∅

4:    App = ORDER(App)

5:    for $\mathcal{F}_{U_i} \in App$ in descending order do

6:    vector.joint (Code $\mathcal{F}_{U_i}$ )

7:    end forreturn vector

8: end function

9: function CODE( $\mathcal{F}_U$ )

10:    if $\mathcal{F}_U$ is LastLayerUserFunc : then

11: $\mathcal{S}_S(\mathcal{F}_U) \leftarrow \mathbb{S}_S(\mathcal{F}_U)$ return $HASH\mathcal{S}_S(\mathcal{F}_U)$ 12:    else if $\mathcal{F}_U$ is HybridUserFunc : then

13: $\mathcal{F}_{U0} = \mathbb{S}_S(\mathcal{F}_U)$ 14:    add $\mathcal{F}_{U0}$ into $\mathbb{S}_U(\mathcal{F}_U)$ 15: $\mathbb{S}_U(\mathcal{F}_U) = ORDER(\mathbb{S}_U(\mathcal{F}_U))$ 16: $\mathcal{S}(\mathcal{F}_U) \leftarrow \bigcup_{\mathcal{F}_{U_i} \in \mathbb{S}_U(\mathcal{F}_U)} \mathbb{S}_S(\mathcal{F}_{U_i})$ 17:    vector.joint (CallHASH $\mathcal{S}(\mathcal{F}_U)$ )

18:    for $\mathcal{F}_{U_i} \in \mathbb{S}_U(\mathcal{F}_U)$ in descending order do

19:    vector.joint (Code $\mathcal{F}_{U_i}$ )

20:    end for

21:    end ifreturn vector

22: end function

23: function $HASH(\mathcal{S}(\mathcal{F}_U))$ 24:    vector = ∅

25: $S_{\mathcal{F}_S} = GroupBy PakistanName(\mathcal{S}(\mathcal{F}_U))$ 26: $S_{\mathcal{F}_S} = OrderBy PakistanName(S_{\mathcal{F}_S})$ 27:    for each group ∈ $S_{\mathcal{F}_S}$ in descending order do

28:    groupSignature ← concatenating all system functions' (in the group ) labels in lexicographic order.

29:    vector.joint (groupSignature.hashcode)

30:    end forreturn vector

31: end function

After obtaining the vectors by the graph encoding algorithm elaborated in Section 3, we found that the size of the encoded vector varies considerably, from 10 to 50,000 which was shown in Fig. 7. When the vector’s size is below the threshold value $\beta ,$ we apply the proposed autoencoder network to learn its representation directly (proposed in Section 5). Otherwise, we apply dimension reduction methods first (proposed in Section 4) and leverage the representation learning algorithm (proposed in Section 5) to generate the App DNA.

# 4 DIMENSIONALITY REDUCTION

High-dimensional vectors will cause huge storage and computation overhead in the process of learning (see Section 5). In this section, we further explore methods to reduce the size of large encoded vectors before the representation learning phase. We consider two vector compression methods, including multiple correspondence analysis (MCA) [24] and further vector cutting. MCA is a generalization of principal component analysis when variables are categorical. We will illustrate them below and analyze their performances in Section 6.

# 4.1 Multiple Correspondence Analysis (MCA)

MCA is proposed to detect underlying structures in a dataset constructed from categorical data and represent data as points in a low-dimensional Euclidean space [24]. We perform MCA by applying the CA algorithm to the indicator matrix [25]. An indicator matrix is an individuals × variables matrix, where the rows represent individuals and the columns are dummy variables representing categories of the variables. By calculating the chisquare distance between different categories of the variables and between the individuals, we can find associations between variables. These associations are then represented graphically as ”maps”, which eases the interpretation of the structures in the data.

The distribution of apps’ sizes is illustrated in Fig.7. There are about 80% apps in year 2013 with sizes over 5,000 and nearly 100% apps with sizes below 20,000. We apply MCA to those vectors with sizes ranging from 5,000 to 20,000. To obtain fixed size vectors, for vectors whose dimensions are greater than 20,000, we crop them to 20,000-dimension ones; for vectors whose dimensions are lower than 20,000, we applying zero padding to enlarge them to 20,000-dimension ones. Then we normalize all 20,000-dimension vectors and compress them using MCA to get vectors with lower dimensions (e.g., 3,734 dimensions in our implementation). Finally, we feed compressed vectors into the neural network to learn large apps’ profiles.

# 4.2 Further Vector Cutting

We further leverage further vector cutting with modifying slightly graph embedding procedure to achieve dimensionality reduction. We manually analyze those large vectors (i.e., whose length is larger than 5,000) and obtain the causes of large vectors generation. There are two aspects. Firstly, the app itself is big enough (Especially the app of recent years), which generates its large call function graph and corresponding large encoded vector. Secondly, several nodes in one call graph have the same succeeding nodes, which are encoded into one vector multiple times resulting the large vector. For example, as shown in Fig. 9, nodes $A , B , \cdots , N$ have the same succeeding node $Q ,$ and $Q$ has called other functions $a , b , \cdots , n$ . When we conduct DF S or BF S traverse, we will visit node $Q$ several times, and thus $Q$ is encoded several times inducing the large vector. We can see that the encoded vectors who have large length usually contain large redundant information. Thus, we propose to embed the node only once even though it’s a successor to multiple nodes and being visited several times.

Our experimental results show that we can reduce the length of 10% vectors from [5,000, 20,000] to [10, 5, 000] and there is no vector whose length is larger than 20,000 after reduction (see Fig 10). In addition, we also show that this method performs well in malware detection (see Section 6.4.2), which verifies the preservation of app behavior information.

![](images/1eca5d12342788cbe5b6550cd7de498717de3c3827290e309f20813ccb292de1.jpg)



Fig. 7. Vector size distribution.

![](images/a6717c1cc647d1744e4ab62c7d255ae02ae30278fa6c7e524c984630c47aed3e.jpg)



Fig. 8. Dimensionality distribution & information loss with PCA.

![](images/da0cd83663ce4d5c79341396202f2f9138f5f063be15fc4eac9796e71d9d3212.jpg)



Fig. 9. The idea of further vector cutting.   
![](images/c846cc9a84204aa3c77c1cbd9e07a4117021a31bb24d4bf94dc89c083aec368e.jpg)



Fig. 10. Further vector cutting effectiveness.

# 5 REPRESENTATION LEARNING

After obtaining encoded vectors from function call graphs, we feed these vectors into unsupervised model to obtain the compact representations. In this section, we design an unsupervised deep neural network based on autoencoder to take those vectors as input and output representations which satisfy the three requirements proposed in Section 2.1. Meanwhile, we also design three supervised models to extract task-oriented representations, including deep neural network (DNN), convolutional neural network (CNN) and long short term memory (LSTM) models as comparison.

# 5.1 Unsupervised Deep Learning

We adopt the deep autoencoder learning algorithm [26] to learn the compact representation from unlabeled data. An autoencoder is a feedforward neural network with an input layer, an output layer and one or more hidden layers. The output layer has the same number of nodes as the input layer. An autoencoder can be divided into two parts, the encoder and the decoder, defined as transitions Φ and Ψ. Here Φ : $X \to F , \Psi : F \to X$ , where X is the input. The training is conducted with backpropgation algorithm to find transitions Φ and Ψ

$$
\Phi , \Psi = \arg \min _ {\Phi , \Psi} | | X - (\Phi \cdot \Psi) X | | ^ {2}.
$$

By minimizing the reconstruction error $\vert \vert X - ( \Phi \cdot \Psi ) X \vert \vert ^ { 2 }$ of the network, the training process targets to make the output $X ^ { \prime }$ similar to the original input X. Considering a simple case with only one hidden layer, the encoder stage takes the input $x \in R ^ { d } = X$ and maps it to $f \in R ^ { q } = F _ { \mathrm { { : } } }$ , where $f = \Phi ( x ) = \sigma ( W x + b )$ , where f is referred to as latent representation, σ is an elementwise activation function such as a rectified linear unit or a sigmoid function, and W is a weight matrix and b is a bias vector. After encoding, the decoder maps f to the reconstruction x0 with the same number of nodes of x, and $x ^ { \prime } = \sigma ^ { \prime } ( W ^ { \prime } z + b ^ { \prime } )$ . In the training procedure, the reconstruction error could be squared error ${ \cal L } ( x , \bar { x ^ { \prime } } ) ~ = ~ | | x - x ^ { \prime } | | ~ = ~ | | x - \sigma ^ { \prime } ( W ^ { \prime } ( \sigma ( W x + \hat { b ) } ) + b ^ { \prime } ) | | ^ { 2 }$ , where x is usually averaged over input training set.

Note that, in the feature space, if F has a lower dimensionality than the input space $X , e . g . , q < d ,$ then the latent representation $f = \Phi ( x )$ can be considered as a compressed representation of the input x. So the representation is what we need in our task, which is a good profile representation of each app. There are many variations of autoencoder like sparse autoencoder [27], deep fullyconnected autoencoder and deep convolutional autoencoder. In our work, we build a fully-connected autoencoder with two fullyconnected layers with dropout technique and max-pooling layers to make the representation as compact as possible while minimize the reconstruction error. The dropout-layer is used to prevent overfitting in learning which was implemented with L2-regularization. The pooling layers have two uses here. Firstly, using pooling layers can down-sample the representation, and help to mitigate over-fitting by providing an abstract form of the representation. Secondly, they can reduce the computational cost by reducing the spatial dimension and the number of parameters to learn.

![](images/21ae6ee2a75b75d75aaa8ed43ecb96306730c9ecdce0d54159a2a3d219e4c93c.jpg)



Fig. 11. Our unsupervised learning model for finding compact representation.

Fig. 11 presents the architecture of APPDNA. It consists of two fully-connected layers and two pooling layers in encoding phase and four fully-connected layers in decoding phase. The learned representation of the input data is only 64-dimensional, which can be adopted in various tasks including malware detection, malware family classification, and functionality categorization. All these tasks will be evaluated in our experiments in Section 6.

# 5.2 Supervised Deep Learning

Furthermore, when there are sufficient labelled data, supervised models can be applied on the encoded vectors to learn taskoriented compact representations. As a comparison, we also build and investigate three typical supervised deep learning models for our tasks and evaluate their effectiveness in our experiments.

Multi-Layer Perceptrons (MLPs) A MLP is a typical feedforward neural network with multiple hidden layers between the input and output layers. It can model complex non-linear relationships. We adopt a DNN with three hidden fully-connected layers, whose sizes are 1024, 512 and 64 respectively, and a softmax layer. The input layer has 5000 nodes, and the output representation is 64- dimension.

Convolutional Neural Network (CNN). A convolution layer is usually followed by a pooling layer, which progressively reduces the spatial size of the representation to reduce the amount of parameters and computation in the network, hence to prevent overfitting. We adopt a CNN with three convolution layers, each followed by a max-pooling layer. The last pooling layer is fully connected to a softmax layer, where each node is for one class in the training data. With CNN, we expect to learn apps’ encoded vectors for each location as the convolution window sliding over the input.

Long Short Term Memory (LSTM). We also investigate a Recurrent Neural Network (RNN), specifically LSTM [28], since LSTM is a natural architecture for dealing with sequences and achieves great success in areas like speech recognition and image captioning. We build the network with three-LSTM layers followed by a dense layer of softmax neurons for classification.

# 6 EXPERIMENTS AND EVALUATION

In this section, we firstly give an illustration of experiment configurations in Section 6.1. Then we analyze the properties of our graph encoding method in Section 6.2, including similaritypreserving, robustness analysis and different encoding strategies comparison. Then evaluate the app profile representations for moderate sized vectors (with length in [10, 5,000]) and large sized vectors (with length in [5,000, 20,000]). The representations are generated by the unsupervised deep learning model and are used for different applications, including malware detection, malware family classification, app functionality classification, and version detection (see in Section 6.3 and 6.4). Further, we compare existing machine learning-based malware detection methods with the APPDNA in Section 6.5. And evaluate how varying the number of hash code bit affects the performance in Section 6.6. Finally, we give an illustration on APPDNA’s run-time analysis in Section 6.7. We collect a large number of apps (80,178 apps in total) for our evaluations.

# 6.1 Experiment Configuration

We employ FlowDroid [21] to build the model of Android component lifecycles and callback methods, and use Soot [20] to extract the function call graph of each app. We build our autoencoder, DNN, CNN and LSTM models with TensorFlow 1.0.0. All training process and experiments are conducted on a server equipped with a 12-core i7 Intel CPU, 64G of RAM and 4 Titan X GPUs.

We collect 61,330 apps from AndroZoo (apps of different years), which have been tested to be benign by VirusTotal 3. We also collect a malicious app dataset from VirusShare4 and Drebin [9]. Table 2 gives the detail of our dataset.

TABLE 2 Overview of our datasets. 

<table><tr><td>Category</td><td>Name</td><td>#Samples</td></tr><tr><td rowspan="4">Benign</td><td>AndroZoo 2013</td><td>23397</td></tr><tr><td>AndroZoo 2014</td><td>28203</td></tr><tr><td>AndroZoo 2015</td><td>12353</td></tr><tr><td>AndroZoo 2016</td><td>10320</td></tr><tr><td colspan="2">Total Benign:</td><td>74,273</td></tr><tr><td rowspan="5">Malware</td><td>VirusShare 2013</td><td>6028</td></tr><tr><td>VirusShare 2014</td><td>13724</td></tr><tr><td>VirusShare 2015</td><td>10000</td></tr><tr><td>VirusShare 2016</td><td>10000</td></tr><tr><td>Drebin</td><td>5250</td></tr><tr><td colspan="2">Total Malware:</td><td>45002</td></tr></table>

3. VirusTotal: https://www.virustotal.com/zh-cn/   
4. VirusShare: https://virusshare.com/

![](images/f927e86341c233fbefc9a3e3e247b112f9e30169b016fd7b07638f0f62f5c4af.jpg)



(a) Nodes/Edge count distance vs. DTW distance.

![](images/b07c60bc94db41e1b895e1a8af53f83489fda210fcda068762091af3e39e92cc.jpg)



(b) Nodes/Edge proportion distance vs. DTW distance.

Fig. 12. Graph distance of apps and corresponding DTW distance of graph encoded vectors.

# 6.2 Function Call Graph Encoding

Our encoding mechanism transfers function call graphs into vectors satisfying three requirements defined in Section 3.1. As the encoding process is deterministic (except the loop-breaking procedure), a function call graph typically has a uniquely encoded vector. Here we evaluate the similarity-preserving (e.g., preserving graph and subgraph similarity) and robustness properties of our encoding mechanism, as well as compare different encoding strategies.

Similarity-preserving and Robustness. We use graph edit distance to measure similarity between graphs, and use dynamic time wrapping (DTW) [29] to measure similarity between encoded vectors. The nearly linear relationship between the original graph edit distance and the encoded DTW distance verifies the similarity preserving property of our encoding method. Specifically, we randomly choose 4,000 apps from our dataset with diverse sizes. By randomly adding nodes (i.e., system functions) and edges (i.e., call relationship) to each app’s function call graph, we obtain pairs of original graphs and modified graphs and generate original and modified encoded vectors for them correspondingly. Then we calculate both graph edit distance and DTW distance for each pair of original version and modified version. The average results for 4,000 apps are presented in Fig. 12, which shows that the DTW distance is proportional to both node edit distance and edge edit distance. And this linear relationship is a verification of robustness against both node insertion and edge insertion. From Fig. 12(a), we can conclude that edge modification causes less fluctuation to the encoded vector than node modification causing (as a result of smaller slope of the edge modification’s simulated polyline than that of the node modification’ simulated polyline). The reason could be that adding an edge often does not introduce a new package for the called system functions, while adding a new system function at lower layer may introduce a new package, thus causing modifications of the encoded vector. Note that, adding a new system function from a new package often implies a behavior change by the function. Especially, if we add nodes in the layer user defined functions $( i . e . , \mathcal { F } _ { L U } )$ , this will lead to behavior changes to $\mathcal { F } _ { H U }$ as shown in Fig. 4(b). In addition, attacks such as renaming user defined functions, and reordering code would not change the encoded vectors. Thus, the DTW remains constant with graph distance changing which is another verification of the framework’s robustness.

Different encoding strategies comparison. For our graph encoding method, there are two alternative strategies to traverse the whole graph, depth-first search (DFS) and breadth-first search (BFS). As comparison, we implement an encoding strategy which traverses the graph by DFS and encodes the user defined function by function names directly, denoted as DFS byFunc. We also implement a DFS traverse (denoted as DFS NoOrder) that visits the functions at same layer randomly without using any ordering criteria. For 4,000 randomly chosen apps, we encode them by four strategies, and evaluate different encoding strategies’ effectiveness by using them for malware detection. Fig. 13 illustrates the recall and precision of four strategies. DFS, BFS and DFS byFunc achieve comparably high accuracy, and all of them significantly outperform the strategy without ordering. However, DFS byFunc is not robust to function renaming: its malware detection accuracy drops to around 1% when we randomly change the names of user defined functions (thus resulting in substantial perturbation of graph encoded vector). Among them, DFS performs the best as it approximately preserves the execution sequence. These results affirm the stability of our proposed encoding method. We use DFS for all reported experiment results in rest of this section.

# 6.3 Application Driven Evaluation

The dimensions of the encoded vectors of apps in our dataset vary significantly, shown in Fig. 7. We here consider those encoded vectors with sizes below 5,000, taking 80% of the total data. The high dimensional encoded vectors are evaluated in Section 6.4.

We generate the 64-dimensional profile representations once, and use them for different applications. As we mentioned in Section 5.1, our model consists of two fully-connected layers with dropout and two pooling layers in encoding phase and four fully-connected layers in the decoding phase. Specifically, the unit number of each encoding layer is 5000, 1024, 256, 64, respectively. For a further step, we add another three fullyconnected layers with 32, 16, 8 nodes, respectively. However, the reconstruction error of the input to the proposed autoencoder increased. So to balance the reconstruction accuray of the input and the representation compactness, we adopt the above four layers structure to construct our model and thus take 64 as the final representation dimension. We leveraged Adam Optimizer and Relu activation function during the training procedure.

Model training and metrics. For each task, we use 64-dimension app representations as input to train a target Support Vector Machine (SVM) classifier. We use 85% data as training set and the rest 15% as test set. For classification tasks, we use standard accuracy, precision, recall, and F-score = 2 · precision·recallprecision+recall precision+reecall as metrics. For each experiment, we perform 5-fold cross validation.

# 6.3.1 Malware Detection

We use the VirusShare 2013, 2014, 2015 and 2016 malware datasets, and AndroZoo 2013, 2014, 2015 and 2016 benign datasets as negative and positive samples, to evaluate the malware detection accuracy of our 64-dimension app representations. As shown in Table 3, for the VirusShare 2013 and AndroZoo 2013 datasets, we classify 4024 (benign/malware) apps using around 5.06 seconds with a 92% F-score and 93.07% accuracy. When we use datasets of 2013 as training data, and test the results on datasets 2014, we can still achieve 82% F-score and 85% accuracy. The accuracy degradation is caused by the malware evolution across years. Mixed all data together, the F-score is 89% and accuracy is 89.74%. Furthermore, for the VirusShare 2015, 2016 and Drebin 2015, 2016, we achieve 87.47% and 86.50% accuracy respectively. Surprisingly, using only 64-dimension (one dimension is represented by one float) profile representation, we achieve such a high accuracy for malware detection. This affirms the power of our compact app profile representation.

TABLE 3 Malware detection accuracy for datasets in different years. 

<table><tr><td>TestData</td><td>TrainData</td><td>Prcs</td><td>Recl</td><td>F-score</td><td>Accuracy</td></tr><tr><td>2013</td><td>2013</td><td>93%</td><td>92%</td><td>92%</td><td>93.07%</td></tr><tr><td>2014</td><td>2014</td><td>88%</td><td>85%</td><td>83%</td><td>85.00%</td></tr><tr><td>2014</td><td>2013</td><td>87%</td><td>84%</td><td>82%</td><td>84.18%</td></tr><tr><td>13 &amp; 14</td><td>13 &amp; 14</td><td>91%</td><td>90%</td><td>89%</td><td>89.74%</td></tr><tr><td>2015</td><td>2015</td><td>89%</td><td>86%</td><td>88%</td><td>87.47%</td></tr><tr><td>2016</td><td>2016</td><td>88%</td><td>85%</td><td>86%</td><td>86.50%</td></tr></table>

As introduced in Section 5.2, we also implement three supervised learning models to extract task-oriented representations, including MLP, CNN and RNN models as comparison. Here we use the malware detection task to measure different models’ effectiveness. Fig. 14 presents the results. For dataset of 2013, the accuracy for autoencoder is 93.07%, for MLP is 95%, for CNN is 90%, and for RNN is 67%. When testing datasets of 2014 on model trained by datasets of 2013, the accuracy for autoencoder is 84.18%, for MLP is 86%, for CNN is 84%, and for RNN is 61%. Among all models, supervised MLP performs the best, while our unsupervised autoencoder provides similar accuracy as CNN. And the lower accuracy of RNN most probably means that the call function gragh encoding is not suitable for RNN which makes use of sequential information.

# 6.3.2 Malware Family detection

Usually malware belong to different families, and malware of the same family possess similar behaviors. Here we perform family classification on Drebin dataset, which provides labels for malware family. Fig. 15 presents the classification accuracy for the 21 largest families (which are widely used in many other works [9], [30]) in the dataset. The average accuracy is 82.81%. For 8 families, their accuracy is higher than 90%. The accuracy of the 5th, 11th, and 15th families is relatively low which could due to 1) their small sample sizes, or 2) malware being Downloaders. Overall, our app representation provides high accuracy results for malware family classification.

# 6.3.3 Functionality categorization

To further demonstrate the proposed app’s profile system feasibility, we conducted functionality categorization using apps’ 64-dimension representations. We categorized 9,730 benign android apps from AndroZoo 2015 and AndroZoo 2016 into 7 functionality groups in Google Play, including personalization, health and fitness, travel and local, books and reference, entertainment, communication, music and audio. We apply the 7- class classification on their profile representations, and the average accuracy is 33.3%, which is much lower than that of malware identification and malware family classification. The reasons can be as the following. Firstly, there are many cross-functionality apps, which means that some apps may have multiple categories which make the classifier confused. For example, an app from category of books and reference, whose package name is “com.quran.labs.androidquran” 5, provides some functionalities like share with friends, search and audio, which also appeared at category entertainment meanwhile. Secondly, there’re a variety of apps in the same functionality category which makes apps in the same functionality have little overlap, thus make some representations of apps cannot distinguish well.

5. https://play.google.com/store/apps/details?id=com.quran.labs.androidquran

![](images/4407bccbdaa619d11bc358e299a8df6086eb5511d1c72cce84b4e1ad225df6ee.jpg)



Fig. 13. Malware detection accuracy for different encoding strategies.

![](images/86c652ae1b9387c454f202c3db342d0ea16f574c8784b7712684c6d3bca2fd88.jpg)



Fig. 14. Malware detection accuracy for different learning models.

![](images/59f97bf84e0f91bc21db82872186e90379d0fb1846c6bda65528a7cd9c869b3e.jpg)



Fig. 15. Detection accuracy for the largest 21 malware families.

![](images/96347c578d975e624e2b760291a3a6ee2e7e5c63f96aa54e0649ae6249604d7b.jpg)



Fig. 16. Pair-wise distances of 9 apps’ different versions.

In order to better understand the results, we apply classification on 3,576 apps from two categories (i.e., 2,486 music audio apps and 1,090 communication apps). As presented in Table 4, we achieve 64% F-score and 74% accuracy. We manually investigate the incorrectly classified apps, and find that some of them are incorrectly labeled. We remove 341 inappropriate apps who are mis-labeled or who have multiple-functionalities and retrain the model, the F-score is 84% and the accuracy is 88.1%. In the future work, we consider adding some additional supplementary information, such as function’s parameter value and APIs’ permission information to better categorize and recommend apps according to their functionalities.

TABLE 4 Two functionalities classification: music & audio vs communication. 

<table><tr><td>State</td><td>Precision</td><td>Recall</td><td>F-score</td><td>Accuracy</td></tr><tr><td>Original dataset</td><td>81%</td><td>74%</td><td>63%</td><td>74%</td></tr><tr><td>Cleaned dataset</td><td>90%</td><td>88%</td><td>84%</td><td>88.1%</td></tr></table>

# 6.3.4 Version detection

Here, we use our app representations to analyze different versions of the same app. We collect 160 apk files, which are different versions of 9 different apps. We measure the pairwise DTW distances of their representations and present the results in Fig. 16. The diagonal deep blue areas imply that, the DTW distance among different versions of the same app is significantly smaller than distances among different apps. This is because different versions of the same app possess similar code structures and behaviors with limited changes. So, our profile representation can be used for tasks like app version detection. Similarly, our profile representation can also be applied to plagiarism detection which was based on similar code detection [31]. We will consider this issue in our future work.

# 6.4 Large Encoded Vectors Evaluation

Here, we perform dimension reduction for large encoded vectors to reduce the storage and computation overhead.

# 6.4.1 Multiple Correspondence Analysis

As presented in Section 4, we compressed vectors using MCA, which reduced the storage space from 26,9623MB to 1938MB, and reduced the autoencoder training time from 1972.67s to 702.23s. The results are shown in Table 5. From Table 5, we can see that using MCA dimensionality reduction technology, we can save about 26,7685MB storage overhead and 1270.44s calculation overhead. Table 6 shows the performances of malware detection for large apps from different years using different vector compression methods. Compared with medium sized apps, the drop in malware detection accuracy is mainly due to the information loss in dimension reduction procedure. Meanwhile, the accuracy of malware detection for 2014 apps is lower than that of 2013 ones. It is mainly because of the unbalanced distribution of positive and negative samples from year 2014.

TABLE 5 Comparison of calculation and storage overhead before and after dimension reduction using MCA method. 

<table><tr><td></td><td>storage cost (MB)</td><td>calculation cost (s)</td></tr><tr><td>Before</td><td>26,9623</td><td>1972.67</td></tr><tr><td>After</td><td>1,938</td><td>702.23</td></tr></table>

# 6.4.2 Further Vector Cutting

We evaluate the effectiveness of one alternative method, further vector cutting, to compress large encoded vectors before training the classifier. The effectiveness of dimension reduction is shown in Fig. 10, which shows that almost all compressed vectors have size below 20,000. We conduct malware detection on those compressed vectors and obtain an 88% accuracy which is comparable to that using MCA method.

TABLE 6 Malware detection performances for large apps by using different reduction methods (I: Multiple Correspondence Analysis; II: Further Vector Cutting). 

<table><tr><td></td><td>TestData</td><td>TrainData</td><td>Prcs</td><td>Recl</td><td>F-score</td><td>Accuracy</td></tr><tr><td rowspan="3">I</td><td>2013</td><td>2013</td><td>87%</td><td>84%</td><td>85%</td><td>86.95%</td></tr><tr><td>2014</td><td>2014</td><td>82%</td><td>81%</td><td>81%</td><td>81.49%</td></tr><tr><td>13 &amp; 14</td><td>13 &amp; 14</td><td>84%</td><td>85%</td><td>85%</td><td>85.65%</td></tr><tr><td rowspan="3">II</td><td>2013</td><td>2013</td><td>88%</td><td>87%</td><td>88%</td><td>87.65%</td></tr><tr><td>2014</td><td>2014</td><td>81%</td><td>80%</td><td>80%</td><td>80.78%</td></tr><tr><td>13 &amp; 14</td><td>13 &amp; 14</td><td>83.2%</td><td>84%</td><td>83%</td><td>84.59%</td></tr></table>

# 6.5 Comparison with Related Work

We consider the following three machine learning based malware detection baseline algorithms.

• Struc [30]: It proposed a method for malware detection based on function call graphs embeddings with an explicit feature map inspired by a linear-time graph kernel.   
• DroidSIFT [32]: It proposed a semantic-based approach that classifies Android malware via dependency graphs, which is resistant to bytecode-level transformation.

We conducted malware detection using these two algorithms and APPDNA on our dataset from 2013. The accuracy and efficiency (average run time for each app) results are shown in Table 7. We can clearly see that, compared with those two methods, APPDNA can achieve higher accuracy in less time. Meanwhile, APPDNA can achieve good performance in many other applications, including malware family detection, functionality categorization and version detection, while those two cannot.

TABLE 7 Malware detection accuracy comparison on year 2013 dataset. 

<table><tr><td>Metric</td><td>Struc</td><td>DroidSIFT</td><td>APPDNA</td></tr><tr><td>Accuracy</td><td>89.2%</td><td>93.0%</td><td>93.1%</td></tr><tr><td>Run time</td><td>52.3s</td><td>175.8s</td><td>47.8s</td></tr></table>

# 6.6 Hash Code Bits Analysis

As we mentioned in Section 3.6 that, we apply a string hash function, specifically the BKDR method to generate encoded vectors. Each dimension of the hash code is represented by one int (with 32 bits). We evaluate how varying the number of bits affects the preformance of malware detection by performing 32-bit, 24- bit, 16-bit and 8-bit, respectively. The result is shown in Fig. 6. We can see that as the number of bits increases, the accuracy increases. Therefore, we apply the int (with 32 bits) represents one vector dimension finally.

# 6.7 Run Time Analysis

As illustrated in Section 6.1 that, all training process (including autoencoder, MLP, CNN and LSTM models) and experiments are conducted on a server equipped with a 12-core i7 Intel CPU, 64G of RAM and 4 Titan X GPUs. The procedure of extracting function call graph using Soot [20] takes about 46.5 s for one app. Encoding a function call graph takes about 0.68 s on average (around 1 s when processing loops), and the average size of encoded vectors is 6,341 bits. It takes about 18 minutes to train the autoencoder model using 23,397 samples from AndroZoo 2013, while it takes 0.66 s to produce 3,507 apps’ 64-dimensional profile representations.

# 7 DISCUSSION

Evasion. Learning-based detection is subject to poisoning attacks. To confuse a training system, an adversary can poison the benign dataset by introducing clean apps bearing ambiguity features. In our case, the attacker may add some useless APIs to an application. Once such samples are accepted by the training dataset, these APIs may significantly affect the encoded vectors and cannot extract the proper features to do profiling tasks. To alleviate this, we carefully design a relatively robust encoding method as we detailed in Section 3. And our experimental results (shown in Fig. 12) reveal that the amount of modification in graph (measured by DTW) results in proportional distance in encoded vector, which shows that the encoding method is robust against both node insertion and edge insertion attacks (see details in Section 6.2). Considering malicious app with dead code, when the proportion of dead code is small, it won’t significantly change the encoding vector of an app. How to deal with the dead code and “live” call, however, is still a challenging issue for existing call graph extraction methods. Advances in call graph extraction technology will bring benefits to our approach. How to defend against those kinds of attacks is also one of our future work.

Transformation attacks. As we use purely static method to extract function call graphs, it suffers from the inherent limitations of static code analysis. The false negative may be caused by bytecode programs that do not bear significant API-level behaviors, such as exploits or downloaders. Our method is resilient towards typical local obfuscation techniques, such as instruction reordering, branch inversion or the renaming of packages and identifiers. As we have encoded all levels’ functions to cover all API-level behavior, our design retains similar accuracy even under the function inlining and outlining attacks. However, it’s worth noting that function inlining and outlining can be used to hide the call graph structure. In the extreme case, this allows implementing a functionality with only a single function or as many functions (some functions do not call any meaningful APIs) as possible. Thus, this kind of extreme case may lead to the encoded vector size extremely large. The optimization of our encoding methods for this problem is left to our future work. Another case that attacker may hide malicious functionality within existing functions, without introducing new nodes on the graph. We may detect this kind of maliciousness when the added number of functions affects the visiting priority (defined in Equation 1), otherwise, we need more detailed analysis which is left to our future work.

Future work. Note that in our design, we use the set of system functions called by a user defined function to abstract its behavior semantics. Although simple and efficient, it did not fully capture the behavior semantics when the execution order or the number of calls to the system functions implies a specific semantics of the function. In future design, we could incorporate this ordering and the number of calls for function call graph encodings. Another line of work for future research is to design a systematic encoding method for graph-based deep learning that can detect, classify, and even count the certain structural properties of a graph.

# 8 RELATED WORK

# 8.1 Android Application Analysis

We divide the android application analysis methods into two categories. One focuses on fine-grained behavior analysis of app in a way of static or dynamic or both of them. The other tries to extract some pre-defined features and leverage machine learning methods to do classification.

Behavior-based Analysis. Dynamic analysis methods require many test runs to reach appropriate code coverage, which is a main challenge to achieve comprehensive evaluation of apps’ behaviors [4], [33]. Static analysis methods can achieve relatively high code coverage but there are limitations such as reflection, dynamic loading and native code, which cannot be solved properly. Moreover, due to the Android platform’s feature, providing precise modeling of the runtime execution (interaction with Android framework) is difficult. Existing works [7], [21], [34]–[36] have exercised data flow analysis to identify sensitive data leakage, and AppIntent [37] combines static and dynamic analysis to identify user unintended transmission of sensitive data. According to the work [38], existing available fine-grained analysis tools had suffered from significant issues ranging from lack of maintenance to the inability to produce functional output for applications for known vulnerabilities.

Machine Learning Based Methods. Another line of work focuses on (manually) extracting useful features to classify benign and malicious app. The work DroidAPIMiner [8] conducted a thorough analysis to extract relevant features at API level and uses KNN [39] as the classifier. Authors of Drebin [9] collected permissionbased, sensitive API and network addresses as malware features and used machine learning to automatically separate malicious and benign applications. Another work Droid-Sec [40] has extracted from 200 features of both static analysis and dynamic analysis of each Android app, and then apply the deep learning technique to classify the malware from normal apps. Authors of [41] proposed to use system API-call sequences and investigate the effectiveness of CNN, LSTM and n-gram SVM in classification of Android applications. The limitations of these works lie in the need for handcrafted task-specific features and large number of labeled training data which was limited in practical applications.

# 8.2 Graph-based Learning

Graph neural networks (GNNs) [42] are deep learning based methods that operate on graph domain. The first attempts to generalize neural network of graphs are Scarselli et al. [43] which combined recursive neural networks and random walk models. This work remained practically unnoticed and has recently discovered by a recent work [44]. The work [44] modified to use gated recurrent units and modern optimization techniques and then extended to output sequences such as problems with program verification. Authors of node2vec [14] propose node2vec, an efficient scalable algorithm for node feature learning that efficiently optimizes a novel network-aware. They design a flexible neighborhood sampling strategy to smoothly interpolate between BFS and DFS and extend to pairs of nodes edge-based prediction tasks. Deepwalk [15] leverages truncated random walk to learn nodes’ latent representations in graphs and then uses these representations to work on multi-label network classification tasks. Different from their work which learns the embedding of each node, our work focused on learning the embedding for the whole graph. Besides, these direct embedding methods cannot deal with graphs with varying sizes, which is just the property of the extracted call graph. Further, for one benign app, we can convert it into a malicious one by intentionally changing the calling order of its code function. GNNs, however, propagate on each node respectively, ignoring the input order of nodes. That is to say, the output of GNNs is invariant for the input order of nodes [42]. Thus it makes GNNs not suitable for our apps’ call graphs. Considering the above all, we proposed a simple but peculiar encoding method that can perform order sensitive traverse for directed graphs of varying sizes (see details in Section 3).

# 9 CONCLUSION

In this work, we propose APPDNA for efficient automatic app profiling using graph-based deep learning. We demonstrate its efficiency by studying its application in accurate and efficient malware detection, malware family classification, app functionality categorization, verison detection, and potentially plagiarism detection. We carefully design a considerably robust graph encoding method to convert a function call graph into a compact vector that preserves graph structural information and is robust to a range of transformation attacks. An autoencoder based unsupervised learning model is designed to transform the encoded vector into 64-dimension compact representation for each app. Our extensive experimental evaluations demonstrate that our design enables more efficient training and prediction than previous approaches (in less than 1.5 ms per apk) and comparable high classification accuracy.

# ACKNOWLEDGMENT

The research is partially supported by National Key R&D Program of China 2018YFB080340, China National Funds for Distinguished Young Scientists with No.61625205, China National Natural Science Foundation with No. 61751211, No. 61520106007, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002.

# REFERENCES

[1] “Number of apps available in leading app stores as of march 2017,” https://www.statista.com/statistics/276623/number-of-apps-available-inleading-app-stores/.   
[2] A. P. Felt, M. Finifter, and Chin, “A survey of mobile malware in the wild,” in Proceedings of the 1st ACM workshop on Security and privacy in smartphones and mobile devices. ACM, 2011, pp. 3–14.   
[3] B. Liu, D. Kong, L. Cen, N. Z. Gong, H. Jin, and H. Xiong, “Personalized mobile app recommendation: Reconciling app functionality and user privacy preference,” in WSDM. ACM, 2015, pp. 315–324.   
[4] X. Zeng, D. Li, W. Zheng, and Xia, “Automated test input generation for android: are we really there yet in an industrial case?” in Proceedings of the 2016 24th ACM SIGSOFT International Symposium on Foundations of Software Engineering. ACM, 2016, pp. 987–992.   
[5] S. Yovine and G. Winniczuk, “Checkdroid: a tool for automated detection of bad practices in android applications using taint analysis,” in Proceedings of the 4th International Conference on Mobile Software Engineering and Systems. IEEE Press, 2017, pp. 175–176.   
[6] R. Bonett, K. Kafle, K. Moran, A. Nadkarni, and D. Poshyvanyk, “Discovering flaws in security-focused static analysis tools for android using systematic mutation,” arXiv preprint arXiv:1806.09761, 2018.   
[7] A. Continella, Y. Fratantonio, M. Lindorfer, A. Puccetti, A. Zand, and Kruegel, “Obfuscation-resilient privacy leak detection for mobile apps through differential analysis,” in Proceedings of the ISOC Network and Distributed System Security Symposium (NDSS), 2017, pp. 1–16.   
[8] Y. Aafer, W. Du, and H. Yin, “Droidapiminer: Mining api-level features for robust malware detection in android,” in International Conference on Security and Privacy in Communication Systems. Springer, 2013, pp. 86–103.   
[9] D. Arp, M. Spreitzenbarth, M. Hubner, H. Gascon, K. Rieck, and C. Siemens, “Drebin: Effective and explainable detection of android malware in your pocket.” in NDSS, 2014.   
[10] R. Pascanu, J. W. Stokes, H. Sanossian, M. Marinescu, and A. Thomas, “Malware classification with recurrent networks,” in ICASSP. IEEE, 2015, pp. 1916–1920.   
[11] X. Hu, T.-c. Chiueh, and K. G. Shin, “Large-scale malware indexing using function-call graphs,” in CCS. ACM, 2009, pp. 611–620.   
[12] S. Shang, N. Zheng, J. Xu, M. Xu, and H. Zhang, “Detecting malware variants via function-call graph similarity,” in 2010 5th International Conference on Malicious and Unwanted Software. IEEE, 2010, pp. 113–120.   
[13] J. Kinable and O. Kostakis, “Malware classification based on call graph clustering,” Journal in computer virology, vol. 7, no. 4, pp. 233–245, 2011.   
[14] A. Grover and J. Leskovec, “node2vec: Scalable feature learning for networks,” in Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2016, pp. 855–864.   
[15] B. Perozzi and R. Al-Rfou, “Deepwalk: Online learning of social representations,” in Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2014, pp. 701–710.   
[16] J. B. Lee and X. Kong, “Skip-graph: Learning graph embeddings with an encoder-decoder model,” 2016.   
[17] D. Liben-Nowell and J. Kleinberg, “The link-prediction problem for social networks,” Journal of the American society for information science and technology, vol. 58, no. 7, pp. 1019–1031, 2007.   
[18] N. Shervashidze, P. Schweitzer, E. J. v. Leeuwen, K. Mehlhorn, and K. M. Borgwardt, “Weisfeiler-lehman graph kernels,” Journal of Machine Learning Research, vol. 12, no. Sep, pp. 2539–2561, 2011.   
[19] S. Xue, L. Zhang, A. Li, X.-Y. Li, C. Ruan, and W. Huang, “Appdna: App behavior profiling via graph-based deep learning,” in IEEE INFOCOM 2018. IEEE, 2018, pp. 1475–1483.   
[20] “Soot,” https://sable.github.io/soot/.

[21] S. Arzt, S. Rasthofer, C. Fritz, E. Bodden, A. Bartel, J. Klein, Y. Le Traon, D. Octeau, and P. McDaniel, “Flowdroid: Precise context, flow, field, object-sensitive and lifecycle-aware taint analysis for android apps,” Acm Sigplan Notices, vol. 49, no. 6, pp. 259–269, 2014.   
[22] E. Mariconti, L. Onwuzurike, P. Andriotis, and E. De Cristofaro, “Mamadroid: Detecting android malware by building markov chains of behavioral models,” arXiv preprint, 2016.   
[23] S. Rasthofer, S. Arzt, and E. Bodden, “A machine-learning approach for classifying and categorizing android sources and sinks.” in NDSS, 2014.   
[24] M. Greenacre and J. Blasius, Multiple correspondence analysis and related methods. Chapman and Hall/CRC, 2006.   
[25] M. Greenacre, Correspondence analysis in practice. Chapman and Hall/CRC, 2017.   
[26] G. E. Hinton and R. R. Salakhutdinov, “Reducing the dimensionality of data with neural networks,” Science, vol. 313, no. 5786, pp. 504–507, 2006.   
[27] A. Ng, “Sparse autoencoder,” CS294A Lecture notes, vol. 72, no. 2011, pp. 1–19, 2011.   
[28] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural computation, vol. 9, no. 8, pp. 1735–1780, 1997.   
[29] S. Salvador and P. Chan, “Toward accurate dynamic time warping in linear time and space,” Intelligent Data Analysis, vol. 11, no. 5, pp. 561– 580, 2007.   
[30] H. Gascon, F. Yamaguchi, D. Arp, and K. Rieck, “Structural detection of android malware using embedded call graphs,” in Workshop on AISec. ACM, 2013, pp. 45–54.   
[31] X. Chen, B. Francia, M. Li, B. Mckinnon, and A. Seker, “Shared information and program plagiarism detection,” IEEE Transactions on Information Theory, vol. 50, no. 7, pp. 1545–1551, 2004.   
[32] M. Zhang, Y. Duan, H. Yin, and Z. Zhao, “Semantics-aware android malware classification using weighted contextual api dependency graphs,” in CCS. ACM, 2014, pp. 1105–1116.   
[33] S. R. Choudhary, A. Gorla, and A. Orso, “Automated test input generation for android: Are we there yet?(e),” in Automated Software Engineering (ASE), 2015 30th IEEE/ACM International Conference on. IEEE, 2015, pp. 429–440.   
[34] Z. Yang and M. Yang, “Leakminer: Detect information leakage on android with static taint analysis,” in Software Engineering (WCSE), 2012 Third World Congress on. IEEE, 2012, pp. 101–104.   
[35] F. e. Wei, “Amandroid: A precise and general inter-component data flow analysis framework for security vetting of android apps,” in CCS. ACM, 2014, pp. 1329–1341.   
[36] W. Enck, P. Gilbert, and S. e. Han, “Taintdroid: an information-flow tracking system for realtime privacy monitoring on smartphones,” TOCS, vol. 32, no. 2, p. 5, 2014.   
[37] Z. e. Yang, “Appintent: Analyzing sensitive data transmission in android for privacy leakage detection,” in CCS. ACM, 2013, pp. 1043–1054.   
[38] B. Reaves, J. Bowers, S. A. Gorski III, and Anise, “\* droid: Assessment and evaluation of android application analysis tools,” ACM Computing Surveys (CSUR), vol. 49, no. 3, p. 55, 2016.   
[39] M.-L. Zhang and Z.-H. Zhou, “Ml-knn: A lazy learning approach to multi-label learning,” Pattern recognition, vol. 40, no. 7, pp. 2038–2048, 2007.   
[40] Z. Yuan, Y. Lu, Z. Wang, and Y. Xue, “Droid-sec: deep learning in android malware detection,” in ACM SIGCOMM Computer Communication Review, vol. 44, no. 4. ACM, 2014, pp. 371–372.   
[41] R. Nix and J. Zhang, “Classification of android apps and malware using deep neural networks,” in Neural Networks (IJCNN), 2017 International Joint Conference on. IEEE, 2017, pp. 1871–1878.   
[42] J. Zhou, G. Cui, Z. Zhang, C. Yang, Z. Liu, and M. Sun, “Graph neural networks: A review of methods and applications,” arXiv preprint arXiv:1812.08434, 2018.   
[43] M. Gori, G. Monfardini, and F. Scarselli, “A new model for learning in graph domains,” in Neural Networks, 2005. IJCNN’05. Proceedings. 2005 IEEE International Joint Conference on, vol. 2. IEEE, 2005, pp. 729–734.   
[44] Y. Li, D. Tarlow, M. Brockschmidt, and R. Zemel, “Gated graph sequence neural networks,” arXiv preprint arXiv:1511.05493, 2015.

![](images/8b5d0a6021395114a4bd619e9f00f4961f656414911082ec9948a4a8c51f1281.jpg)



Anran Li is a Ph.D student in the Department of Computer Science and Technology, University of Science and Technology of China, China. She received her B.S. degree in Anhui University of Science and Technology in 2016. Her research interests include representation learning for graph-structured data, deep learning and data quality assessment.

![](images/090fc4109aea6f283323f1bd352834ff93bbc0e5cd9ca76f9d39839e63d7b05d.jpg)



Shuangshuang Xue is a Ph.D student in the Department of Computer Science and Technology, University of Science and Technology of China, China. She received her B.E. degree in Computer Science and Technology from Anhui University, China, in 2015. Her research interests include software security, mechanism design and data trading.

![](images/3c5edd52817fe801eef79447ff456ffb5b435b5c0b8e136ea68a7e4a5a373147.jpg)



Chicago, USA.

Xiang-Yang Li is currently a Full Professor and the Executive Dean of the School of Computer Science and Technology, University of Science and Technology of China, Hefei, China. He is an IEEE/ACM Fellow. He received the bachelor degree from the Department of Computer Science, the bachelor degree from the Department of Business Management, Tsinghua University, in 1995, and the Ph.D. degree from the University of Illinois at Urbana Champaign. He was a Full Professor with the Illinois Institute of Technology,

![](images/a5a022b556ce7360bd953a217a8559d5b70d91edc7ed60dc0994dff6a08641c4.jpg)



Lan Zhang is currently a research professor at the School of Computer Science and Technology, at University of Science and Technology of China. She received her Bachelor degree (2007) in School of Software at Tsinghua University, China, and her Ph.D. degree (2014) in the department of Computer Science and Technology, Tsinghua University, China. Her research interests span mobile computing, privacy protection, and data understanding.

![](images/1cabfc55f256eb73be2dc5a185ce4026608fd217eedd8d3c31b41ff8f2fe6978.jpg)



Jianwei Qian is a Ph.D. candidate in Computer Science at Illinois Institute of Technology, USA. He received his B.E. degree in Computer Science and Technology from Shanghai Jiao Tong University, China, in 2015. His research interests include privacy and security issues in big data and social networking.