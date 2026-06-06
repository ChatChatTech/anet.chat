# KATN: Key Activity Detection via Inexact Supervised Learning

XUANKE YOU, University of Science and Technology of China, China LAN ZHANG∗, University of Science and Technology of China, China HAIKUO YU, University of Science and Technology of China, China MU YUAN, University of Science and Technology of China, China XIANG-YANG LI, University of Science and Technology of China, China

Leveraging sensor data of mobile devices and wearables, activity detection is a critical task in various intelligent systems. Most recent work train deep models to improve the accuracy of recognizing specific human activities, which, however, rely on specially collected and accurately labeled sensor data. It is labor-intensive and time-consuming to collect and label large-scale sensor data that cover various people, mobile devices, and environments. In production scenarios, on the one hand, the lack of accurately labeled sensor data poses significant challenges to the detection of key activities; on the other hand, massive continuously generated sensor data attached with inexact information is severely underutilized. For example, in an on-demand food delivery system, detecting the key activity that the rider gets off his/her motorcycle to hand food over to the customer is essential for predicting the exact delivery time. Nevertheless, the system has only the raw sensor data and the clicking “finish delivery” events, which are highly relevant to the key activity but very inexact, since different riders may click “finish delivery” at any time in the last-mile delivery. Without exact labels of key activities, in this work, we propose a system, named KATN, to detect the exact regions of key activities based on inexact supervised learning. We design a novel siamese key activity attention network (SAN) to learn both discriminative and detailed sequential features of the key activity under the supervision of inexact labels. By interpreting the behaviors of SAN, an exact time estimation method is devised. We also provide a personal adaptation mechanism to cope with diverse habits of users. Extensive experiments on both public datasets and data from a real-world food delivery system testify the significant advantages of our design. Furthermore, based on KATN, we propose a novel user-friendly annotation mechanism to facilitate the annotation of large-scale sensor data for a wide range of applications.

CCS Concepts: • Human-centered computing → Ubiquitous and mobile computing; • Computing methodologies → Machine learning.

Additional Key Words and Phrases: activity detection, inexact supervised learning, sensor data

# ACM Reference Format:

Xuanke You, Lan Zhang, Haikuo Yu, Mu Yuan, and Xiang-Yang Li. 2021. KATN: Key Activity Detection via Inexact Supervised Learning . Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 5, 4, Article 189 (December 2021), 26 pages. https://doi.org/ 10.1145/3494957

∗Corresponding author

Authors’ addresses: Xuanke You, yxkyong@mail.ustc.edu.cn, University of Science and Technology of China, China; Lan Zhang, zhanglan@ ustc.edu.cn, University of Science and Technology of China, China; Haikuo Yu, yhk7786@mail.ustc.edu.cn, University of Science and Technology of China, China; Mu Yuan, ym083@mail.ustc.edu.cn, University of Science and Technology of China, China; Xiang-Yang Li, xiangyangli@ustc.edu.cn, University of Science and Technology of China, China.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

© 2021 Association for Computing Machinery.

2474-9567/2021/12-ART189 \$15.00

https://doi.org/10.1145/3494957

# 1 INTRODUCTION

Activity detection is an essential but challenging task in various mobile and ubiquitous computing systems, e.g., smart healthcare systems [19][24] and smart home systems [2][21][20]. Through analysis of sensor signals, e.g., signals from Inertial Measurement Unit (IMU), in mobile devices or wearable devices, it recognizes what kind of activity the device holder is performing. A lot of efforts have been devoted to increasing the categories and accuracy of human activity detection based on IMU data. Existing methods usually train a classification model for human activities relying on a collection of accurately labeled IMU data [48][4][29][43][17]. However, the acquisition and annotation of IMU data are not only time-consuming and laborious, but also intractable. Unlike image data or audio data, IMU signals are much more difficult for humans to read and label directly[50] [49]. Therefore, it requires users to label the IMU data right before and after they perform specific activities or record the activities by video, causing unpleasant user experiences and expensive extra costs. Moreover, for large-scale applications, those classification models usually suffer a performance degradation due to the domain shift issue, which is caused by diverse devices, environments, and usage habits of different users[40]. On the other hand, we notice that, massive IMU data is being continuously generated, in company with user interaction events, e.g., clicking specific buttons. Those events are sometimes highly relevant to the activities we concern about and may act as unintended and inexact labels of the IMU data. Few work has explored the correlation between these user interactions and IMU data, leaving massive raw IMU data severely underutilized.

In this work, we aim to detect the exact regions (i.e., start and end time) of the target human activities in raw IMU data by leveraging relevant user interaction events as inexact labels, and introduce our design with a typical application scenario, i.e., the on-demand food delivery system [36]. In recent years, there is a fast increasing trend to obtain convenient and immediate food purchasing and delivery through the Internet. In on-demand food delivery scenarios, understanding riders’ behaviors is essential for improving the quality of service. One of the critical tasks is to determine the exact start and end time of the food delivery activity, i.e., when the rider gets off his/her motorcycle to hand over food to the customer and when he/she gets back on the motorcycle to leave. Based on these timestamps, a food delivery system can predict the exact delivery time for customers [54], assess the performance of delivery contracts, build maps and optimize path planning for riders, etc. To detect the key activity, e.g., food delivery activity, based on the IMU data of the user’s mobile phone is intractable due to multiple reasons:

First, the IMU data is unlabeled and the relevant interaction events are highly inexact. Moreover, the target key activity could be complex, i.e., it is composed of multiple flexible activities. For example, the food delivery activity is a complex activity. Each rider is supposed to click a “finish delivery” button around the time he/she hands over the food to the customer. However, due to diverse usage habits of different riders, the click action may happen at any time in the last-mile delivery, before parking, during handover, or after delivery as shown in Fig. 1. Thus, we can only figure out that there is a high probability that the rider gets on and off the motorcycle around the time of the click action. To tackle temporal uncertainty of self-reported labels in HAR, previous solutions based on machine learning usually follow a multi-instance learning (MIL) paradigm [53][8]. [1] augments the semi-Markov conditional random field model to improve prediction performance based on imprecise continuous-time observations of the target activity’s segment boundaries, while we can only obtain the timestamp of the click action in this work. [14] provides a method for perinatal stroke screening with only segment-level labels, which mainly focuses on recognizing trials with abnormal movements rather than precise regions of target activities in trials. [44] utilizes a deep model to calculate the correlation between local features and a global feature to distinguish regions of target activities. However, this model uses a single-view design, aiming to detect single activity, thus it performs poorly when the target activity is complex. Therefore, there still lacks an effective method to achieve accurate complex activity detection with only inexact labels.

Second, the IMU data is very noisy. Since a rider can use his/her phone freely during the delivery, e.g., to answer phone calls and read messages, besides the key activity, there are a variety of activities in the IMU data, which bring serious noises to the key activity detection.

Third, IMU data across different riders is highly diverse. Riders own diverse mobile phones equipped with different inertial sensors and have different device placement habits, which means mobile phones could be placed in the pockets, backpacks, and so on. Thus, detection models lacking good adaptability usually suffer from a domain-shift problem [9] [34] [52].

![](images/bd325c4c026a2f9884821c9a8f9f340dd09e0b1c141281fbe0acc9c1617ed295.jpg)



Fig. 1. Example IMU data during a food delivery.

To cope with these challenges, in this work, we propose a novel key activity detection system, named KATN, using only unlabeled raw IMU data and inexact user interaction events. The core idea of KATN is to train a coarse-grained classification deep model under the supervision of the inexact labels, and then interpret the behaviors of the deep model to locate the exact regions of the key activities. Specifically, we develop a deep learning model to obtain regions of target activity, especially for complex activities (e.g. food delivery), with only inexact labels from large segments of IMU data. A siamese key activity attention network (SAN) with multi-view attention perspectives is proposed to automatically extract and activate semantic and temporal features of each timestamp based on IMU data to obtain more precise regions of target activity. Moreover, we explore the potential of KATN and devise a novel user-friendly IMU data annotation mechanism. In the process of annotation, collectors only need to answer yes or no, which is easy for anyone with or without professional knowledge. It provides a new way to annotate large-scale IMU data for various applications. Our key contributions are summarized as follows:

• We propose a novel key activity detection system (KATN) to detect the exact regions (i.e., start and end time) of key activities with only raw IMU data and inexact labels. A siamese key activity attention network (SAN) is designed to automatically extract and activate semantic and temporal features of raw IMU data with multi-view attention perspectives. By measuring the temporal feature importance of SAN, exact start and end time of the key activity can be obtained by our exact time estimation method. Moreover, to deal with data diversity across users, we design a personal adaptation method for KATN by adding unbalanced sample weights during the training process.

• We evaluate our design on two public datasets and data collected from a real online food delivery system with various settings. We evaluate the performance of KATN when the key activity is a simple activity or complex activity. Moreover, we explore the impact of the difference between background activities and key activities, sampling frequency of raw data, and segment duration on the performance of key activity location. Extensive experiments demonstrate the superiority of KATN compared with several classic and timely methods.   
• Based on KATN, we design and evaluate a novel user-friendly IMU data annotation system. During the collection process, the annotator only needs to answer yes or no to roughly annotate the IMU data. And then the system can obtain annotated IMU data with different levels of purity. Compared with traditional annotation methods, our mechanism is friendly to anyone with or without professional knowledge. It provides a potential for large-scale IMU data annotation.

The reminder of this paper is organized as follows. Section 2 gives a brief review of the related work. Section 3 introduces the detailed design of KATN. Extensive experiments in Section 4 show visualization analysis and performance of our method. In Section 5, a novel user-friendly annotation mechanism is introduced and evaluated. Finally, we discuss the limitations of KATN and make a conclusion in Section 6 and Section 7.

# 2 RELATED WORK

# 2.1 Conventional Human Activity Recognition

Human activity recognition (HAR) aims to identify the specific high-level movement and action of a person based on raw sensor data. HAR is an important technology in many applications such as smart care[19][24], smart home[2][21][20], wireless sensing[48], and so on. In recent years, significant progress has been made for HAR in both conventional machine learning and deep learning. In conventional machine learning fields, many work focus on the deep understanding of relations between sensor signals and human activities [48][4][29], and some work design active learning-based models for HAR [20]. There are also some graph based methods that integrate new sensors out of the training phase[35]. When it comes to deep learning methods, lots of work employ deep architectures like CNN [43][13] and LSTM [17] to improve the recognition accuracy of human activities. In deep learning tasks, the attention mechanism mimics the cognitive attention of humans and is widely used for various purposes, e.g, enhancing the accuracy of the CNN classification model [42][23]. The attention mechanism has also been utilized in HAR task [32][47][28] and weakly labeled tasks[39][31]. HAR models still face lots of challenges when applied in real-world applications. To mitigate domain-shift problems between the training data and application scenarios, some work propose transfer learning based methods for cross-dataset activity recognition[34][11][35][22][12]. A series of work improve the robustness and adaptation of HAR models to cope with the diversity of activities in the real world [10][3][33]. All those aforementioned HAR work focus on the recognition of specific activities and most of them require training data with exact labels. In this work, however, we aim to detect the exact start and end time of target activities based on raw IMU data without exact labels.

# 2.2 Learning with Weakly Labeled Data

In practice, labeling IMU data is complicated and introduces inevitable noise, thus it is very time-consuming and laborious to obtain a large amount of accurately labeled IMU data. Various methods have been developed for reducing annotation uncertainty [26][1] and reducing label noise[5]. When only coarse-grained label data can be obtained, MIL is a widely used learning paradigm [53][8]. [14] designs an MIL method for perinatal stroke screening with only segment-level labels. However, it mainly focuses on recognizing trials with abnormal movements rather than inferring precise regions of target movements in trials. Besides, the method utilizes low-dimensional PCA to extract representations from raw signals of each window, leading to limitations in feature representation and portability. [44] utilizes a deep model to calculate complexity scores between local features and a global feature to distinguish regions of key activities. The single-view design of the model is only suitable for simple activities, resulting in poor performance when the target activity is complex. Deep learning based MIL methods have also been developed to automatically extract and activate features for other tasks with weakly labeled data, e.g., image processing [6] and sound event detection [46][30][38][25]. [51] designs a class activation mapping (CAM) framework to calculate heatmaps of image classification CNNs model through a global average pooling network. Recently, RCAM [6] involves three improvement measures on the global average pooling layer, weighted summation of feature maps and thresholds of heatmaps. TALNet [46] builds an instance-based MIL neural network for weakly labeled sound event detection, which utilizes sigmoid function to activate features at each timestamp to represent the frame-level probabilities and then aggregates them into bag-level probabilities by a linear softmax function. However, there is still a lack of method for accurate activity detection, especially for complex activities, given raw IMU data with only inaccurate labels. Our work follows the MIL paradigm and contributes to handling uncertainty in self-reported labels for both simple and complex key activities, in which temporal features of IMU data will be activated in different degrees with the guidance of coarse-grained labels.

# 3 DESIGN OF KATN

# 3.1 Problem and Main Idea

In this work, we aim to detect the accurate start and end time of the key activity (e.g., the food delivery activity), given raw IMU data and inexact labels (e.g., the user click action). Though deep learning model is a powerful tool to automatically extract meaningful features for activity detection, we cannot directly train a deep learning model to infer the region of the key activity due to the lack of training samples with accurately labeled start and end time. Our main idea is to leverage the inexact labels to train a two-class deep classifier, which infers whether a data segment contains the key activity or not, and trace the positive outputs of the deep classifier through its algorithm and back to the input data segments to understand why the classifier makes a positive inference. By interpreting the behaviors of the deep learning model, we can locate the exact region in the input data segment that causes a positive inference, so as to detect the start and end time of the key activity. To implement this idea, we propose a system KATN, which contains two main components: First, a siamese key activity attention network (SAN) is designed to learn the occurrence of the key activity in the raw IMU data using inexact labels; Second, an exact time estimation method is designed to transform the temporal feature importance scores of SAN into the exact start and end time.

We formally define our key activity detection problem with raw IMU data and inexact labels. We divide unlabeled IMU data into a collection of data segments $X = \{ x _ { i } \} _ { i = 1 } ^ { n }$ , and leverage occurrences of the highly relevant interaction event $( \mathbf { e . g . }$ X xi i, clicking the “finish delivery” button) as the segment-level inexact labels, which are $Y = \{ y _ { i } \} _ { i = 1 } ^ { n } . y _ { i } = 1$ indicates that the event happens during the period of segment $x _ { i } ,$ otherwise $y _ { i } = 0$ . Since Y yi i yithe key activity and the event are highly relevant, when $y _ { i } = 1 , x _ { i }$ xi yicontains the key activity with high probability. yi xiWe will discuss the impact of the length of data segments in Section 4.5. Our goal is to detect the exact start time and end time $P = \{ ( s _ { i } , \stackrel { - } { e _ { i } } ) \} _ { i = 1 } ^ { k }$ of key activities in given segments $\mathcal { T } = \{ x _ { i } | y _ { i } = 1 \} _ { i = 1 } ^ { k }$ .

# 3.2 System Overview

In this section, taking an on-demand food delivery system as an example, we introduce the workflow of KATN. As shown in Fig. 2, throughout the delivery process, the IMU data of riders’ mobile phones is continuously generated and collected to form the unlabeled dataset . Each rider may click the “finish delivery” button at any time in the Xlast-mile delivery, i.e., before or after he/she gets off the motorcycle to hand the food over to the customer. These click events with timestamps are collected as positive inexact labels $Y _ { p } = \{ y _ { i } = 1 \}$ , and the corresponding IMU data segments are positive samples $X _ { \mathcal { P } } = \{ x _ { i } | y _ { i } = 1 \}$ Yp yi. The rest data segments are considered as negative samples $X _ { n } = \{ x _ { i } | y _ { i } = 0 \}$ Xp xi yi. KATN takes collected IMU data segments and inexact labels as input, and follows three steps to detect the region of key activities, including (1) IMU data augmentation, (2) siamese key activity attention network and (3) exact time estimation. Moreover, based on KATN, we design a novel user-friendly IMU data annotation system as shown in Fig.17. During the collection process, the annotator only needs to answer yes or no to roughly annotate the IMU data. And then the system can obtain annotated IMU data with different levels of purity.

![](images/309e31def40890865bf041f0566d03d358eeac8261b0f02f57a3c3032734e682.jpg)



Fig. 2. System overview of KATN.

# 3.3 IMU Data Augmentation

Data augmentation is an important technique in deep learning, which transforms the data to increase diversity and cover unseen data. It can effectively alleviate the over-fitting problem and enhance the robustness of the model. We conduct IMU data augmentation by three methods (as shown in Eq. (1)), including two conventional methods (random rotation and random shift), and our proposed negative sample mixup (NSM) method.

$$
X, Y = \left(\text { Rotation } (X, Y), \text { Shift } (X, Y), \text { NSM } (X, Y)\right) \tag {1}
$$

# 3.3.1 Conventional Methods.

# 1) Random Rotation.

Since the placement of the mobile phone is arbitrary, the model should have the ability to learn the features with rotational invariance. As shown in Eq. (3) and Eq. (4), we randomly generate rotation matrices along three axes to rotate the IMU data, where ,  and  represent the rotation angles along x, y and z axes. Here, ,  and  are uniformly random from (0 2 ).

$$
\operatorname{Rotation} (X, Y) = R (X), Y \tag {2}
$$

$$
R (x _ {i}) = (x _ {i} ^ {0}, x _ {i} ^ {1}, x _ {i} ^ {2}) \left[ \begin{array}{c c c} 1 & 0 & 0 \\ 0 & \cos (\alpha) & - s i n (\alpha) \\ 0 & s i n (\alpha) & c o s (\alpha) \end{array} \right] \left[ \begin{array}{c c c} c o s (\beta) & 0 & s i n (\beta) \\ 0 & 1 & 0 \\ - s i n (\beta) & 0 & c o s (\beta) \end{array} \right] \left[ \begin{array}{c c c} c o s (\theta) & - s i n (\theta) & 0 \\ s i n (\theta) & c o s (\theta) & 0 \\ 0 & 0 & 1 \end{array} \right] \tag {3}
$$

$$
\alpha , \beta , \theta \in (0, 2 \pi) \tag {4}
$$

# 2) Random Shift.

Since the key activity could happen at any time of a data segment, the model should have the ability to learn features with cropping invariance. As shown in Eq. (5), $( X > > \gamma )$ conducts cycling shift augmentation

Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 5, No. 4, Article 189. Publication date: December 2021.

on , where  is uniformly random from the length of .

$$
\operatorname{Shift} (X, Y) = (X > > \gamma), Y \tag {5}
$$

3.3.2 Negative Sample Mixup. Based on the prior knowledge, the negative sample does not contain the key activity. We propose a negative sample mixup method to conduct additional data augmentation for better diversity of training data to alleviate model overfitting. We randomly mix up the raw data of negative samples by inserting random parts cropped from other negative samples as shown in Eq. (6). Here, $X ^ { \prime }$ represents random other negative samples and $C r o p ( X ^ { \prime } )$ will obtain random parts from $X ^ { \prime }$ X. Finally, we insert the (  ′) into the original data Crop X Xby the  function to compose mixed negative samples.

$$
N S M (X, Y) = \operatorname{Mix} \left(X, \operatorname{Crop} \left(X ^ {\prime}\right)\right), Y \tag {6}
$$

# 3.4 Siamese Key Activity Attention Network

![](images/0bf8cbadf66012ae915f2180e798cbcda0def5e65bff400da6a1494d463ece11.jpg)



Fig. 3. Structure of siamese key activity attention network (SAN).

As shown in Fig. 3, SAN is composed of three parts: shared feature extraction layers, siamese activity attention layers including a discriminative activity attention network  and a detailed activity attention network , DiNand classifiers. The detailed design of each part will be introduced in Section 3.4.1 ∼ Section 3.4.4.

3.4.1 Feature Extraction. Taking augmented IMU data as input, SAN takes two steps to extract both semantic features and temporal features of IMU data, including shared feature extraction and local feature extraction. The shared feature extraction layers are shared by two siamese networks  and .  and  have their own local feature extraction layers.

Shared Feature Extraction Layers: Convolutional Neural Networks (CNN) [27] is a widely-used feature extractor for both image and time-series data. In shared feature extraction layers, the input data is firstly fed into a Conv1D layer with a size of $3 2 \times 4 0$ , where 32 is the number of convolution kernels and 40 is the size of the time window for convolution kernels. And then, a max-pooling layer is adopted to reduce peacekeeping and expand the receptive field. The Conv1D and max-pooling layers extract semantic features of IMU data in the time window. Both the convolution and max pooling operations are performed along the time axis, so as to align extracted features with the timeline.

Local Feature Extraction Layers: Besides the shared feature extraction layers,  and  have their own DiN DeNlocal feature extraction layers. The first part of local feature extraction layers contains a Conv1D layer and a max-pooling layer, which are the same as those in the shared feature extraction layers. Considering that even human behaviors with the same semantic feature may have different meanings and importance in different contexts, the second part is designed to extract temporal features of human activities. For example, the same behavior stopping the motorcycle should have different importance when it happens at the red light and before getting off the motorcycle to hand the food over to the customer. Long Short-Term Memory (LSTM)[18] addresses the long-term and short-term dependency problem through purpose-built memory cells. Bidirectional LSTM (Bi-LSTM) unit[16] constructs LSTM layers in both directions after concatenation as shown in Eq. (7) and Eq. (8), which produces a more robust feature representation with both previous and subsequent information. SAN utilizes a Bi-LSTM layer with $3 2 \times 2$ kernels to extract temporal features after the convolution and max pooling operations.

$$
B (\boldsymbol {x}) = \operatorname{concat} \left(\overrightarrow {\mathrm{h}} _ {t}, \overleftarrow {\mathrm{h}} _ {t}\right) \tag {7}
$$

$$
\overrightarrow {\mathrm{h}} _ {t} = \overrightarrow {L S T M _ {F}} (\overrightarrow {\mathrm{h} _ {T - 1}}, \mathrm{x} _ {t}), \overleftarrow {\mathrm{h}} _ {t} = \overleftarrow {L S T M _ {B}} (\overleftarrow {\mathrm{h} _ {T - 1}}, \mathrm{x} _ {t}), \tag {8}
$$

After shared and local feature extraction layers, for each timestamp, we get a feature vector of IMU data, which contains both semantic and temporal features. The feature of a data segment is composed of a series of feature vectors of its timestamps.

3.4.2 Siamese Activity Attention Networks. The attention mechanism was proposed to improve feature extraction by adding weights to representations in neural machine translation [7], where each weight represents the focus of the model on the corresponding feature. Attention weights of each feature are calculated by fitting the feature itself into the weight through a global fully connected layer[41]. Eq.(9) shows the calculation process of our attention module, where  represents the attention layer and  denotes a fully connected layer activated by the σ fReLU function.  is the temporal feature for a given data segment after feature extraction layers. The softmax vfunction tends to choose one and will get sharpened values, however, we expect to cover the full time period of target activity. Thus, sigmoid function $\scriptstyle { \frac { 1 } { 1 + e ^ { - x } } }$ is adopted instead of softmax in the original attention as mentioned ein 4.4. Here, the attention weight  of temporal features is represented as $A t t = s i g m o i d ( f ( \pmb { v } ) )$ .

$$
\sigma (\boldsymbol {v}) = \operatorname{sigmoid} (f (\boldsymbol {v})) * \boldsymbol {v} \tag {9}
$$

As described in Section 3.4.1, we obtain the feature vector for each timestamp after feature extraction layers. With inexact labels, we can train SAN to classify whether the input data segment contains the key activity. After the training process, we propose to trace those feature vectors that contribute the most to the positive output. And for multi-view attention perspectives, we design a siamese attention mechanism, which consists of a discriminative activity attention network  and a detailed activity attention network .

3.4.3 Discriminative Activity Attention Network. We aim to design the attention values of to represent the DiNmost discriminate part of the key activity. Based on the fact that there is no key activity in negative samples, we introduce a loss  as shown in Eq. (10), which restrains the activation of attention value by limiting the LossNvariance of attention values of negative samples. Here, represents the attention values of the attention layer of , and $Y [ i ]$ is the label of data segment $x _ { i } ,$ , where $Y [ i ] = 0$ is a negative label, and $Y [ i ] = 1$ is a positive label as shown in Eq. (11). In other words, the activated attention value will be more discriminative by adding to the loss function of .

$$
\operatorname{Loss} _ {N} = \sum \widetilde {Y [ i ]} \sqrt {\frac {1}{n} \sum_ {j = 1} ^ {n} \left(\operatorname{Att} _ {D} ^ {j} \left(x _ {i}\right) - \overline {{\operatorname{Att} _ {D} \left(x _ {i}\right)}}\right) ^ {2}} \tag {10}
$$

$$
\widetilde {Y [ i ]} = \left\{ \begin{array}{l l} 0, & i f Y [ i ] = 1 \\ 1, & i f Y [ i ] = 0 \end{array} \right. \tag {11}
$$

uses a Multilayer Perceptron (MLP) layer with the softmax activation as the classifier. The loss function DiNof  is the sum of and as shown in Eq. (12), where  is the weight of , is the classic DiN LossH LossNcross entropy loss function (see Eq. (13)).

$$
\operatorname{Loss} _ {D} = \operatorname{Loss} _ {H} + \lambda * \operatorname{Loss} _ {N} \tag {12}
$$

$$
\operatorname{Loss} _ {H} = \mathcal {H} (y, p (y | x, \theta)) = - \sum y \log p (y | x, \theta) \tag {13}
$$

3.4.4 Detailed Activity Attention Network. In order to get the accurate region of the key activity, it is not enough to only detect the discriminative part, but also important to detect the remaining less discriminative part of the key activity. We aim to design the attention values of  to represent the details of the key activity. To solve DeNthis problem, we propose an Alpha-Mask of Discriminative Part Attention (AMDP) mechanism as shown in Eq. $\left( 1 4 \right) \sim { \mathrm { E q . ~ } } \left( 1 6 \right)$ . The core idea of the AMDP mechanism is masking the activated attention weights of  to DiNmake  ignore what  has learned and focus on learning the details from the rest features of the target key DeNactivity. Here, $A t t _ { E } ^ { ' }$ DiNin Eq. (14) denotes the original output of the attention operation in . With $s i g n _ { \alpha } ( A t t _ { D } )$ Ein Eq.(15), the attention values $A t t _ { D }$ of  that are greater than  will be activated. The (·) function $\left( \mathrm { E q . } ( 1 4 ) \right)$ AttD DiNmasks attention values of  that are in accord with $s i g n _ { \alpha } ( A t t _ { D } )$ α h to ignore those features that  has learned.

$$
A t t _ {E} = h (A t t _ {E} ^ {\prime} - s i g n _ {\alpha} (A t t _ {D})) \tag {14}
$$

$$
\operatorname{sign} _ {\alpha} \left(\operatorname{Att} _ {D}\right) = \left\{ \begin{array}{l l} 0, & \text { if   } \operatorname{Att} _ {D} <   \alpha \\ 1, & \text { if   } \operatorname{Att} _ {D} > = \alpha \end{array} \right. \tag {15}
$$

$$
h (x) = \left\{ \begin{array}{l l} x, & \text { if   } x > 0 \text {   and   } x <   1 \\ 0, & \text { if   } x <   = 0 \\ 1, & \text { if   } x > = 1 \end{array} \right. \tag {16}
$$

utilizes the same MLP classifier as , and the loss function is $L o s s _ { E } = L o s s _ { H }$ . Our design enables DeN DiNto learn more than the most discriminative features.

These two networks  and  play complementary roles by paying attention to extracted features from DiN DeNmultiple views. Finally, we merge both the discriminative part and the detailed part to figure out the accurate region of the key activity.

# 3.5 Exact Time Estimation

In this section, we design a method to calculate the accurate start and end time of the key activity. First, given a data segment $x _ { i } ,$ , we propose an importance score to measure the impact of the extracted feature for each xitimestamp on the model inference result. As shown in $\operatorname { E q . } ( 1 7 )$ , the importance score $Z _ { t }$ of the feature for each Zttimestamp  is defined as its contribution to the positive output class. Here,  represents the length of features at teach timestamp. $a _ { t }$ krepresents the attention weight of the feature at timestamp  and  represents the weight between the feature unit and the positive unit in the classifier layer. And then, we normalize the temporal feature importance score  according to Eq. (18).

$$
Z _ {t} = \sum_ {i = t k} ^ {t k + k} w _ {t} ^ {i} (a _ {t} v _ {t} ^ {i}) = \sum_ {i = t k} ^ {t k + k} w _ {t} ^ {i} \sigma (\boldsymbol {v}) _ {t} ^ {i} \tag {17}
$$

$$
Z = \frac {\text { maximum } (Z , 0)}{\text { max } (Z)} \tag {18}
$$

Second, we obtain two collections of temporal feature importance scores $Z _ { D }$ and $Z _ { E }$ from  and respectively. As presented in Alg.1, we merge multi-view importance scores $Z _ { D }$ Dand $Z _ { E }$ ZEto obtain $Z _ { M }$ DeN. We use a threshold  to filter large importance scores in $Z _ { M }$ D E Mto form the candidate set . We take the offset of the first (last) importance score in C as the start (end) position $S ^ { \prime } \left( E ^ { \prime } \right)$ of the key activity. We use the normalize function in Eq. (19) to transform $S ^ { \prime }$ S Eand  ′ into the actual start time  and end time  of the key activity, where  is the size of the output importance scores and  is the time length of the data segment.

Algorithm 1 Exact Time Estimation   
Require:
The temporal feature importance scores of SAN's networks: $Z_{D}$ , $Z_{E}$ ;
A hyperparameter to filter importance scores: $\delta$ Parameters for time normalization: L and M
Ensure:
The start time and end time: S and E
1: $Z_{M} = Z_{D} + Z_{E}$ ;
2: $Z_{M} = \frac{Z_{M}}{\max(Z_{M})}$ ; // // Normalize $Z_{M}$ into 0 to 1
3: C = {};
4: for index in length( $Z_{M}$ ) do
5: if $Z_{M}[index] > \delta$ then
6: C.append(index);
7: end if
8: end for
9: $S' = C[0]$ ;
10: $E' = C[-1]$ ;
11: S, E = normalize( $S', E', L, M$ );
12: return S, E;

$$
(S, E) = \text { normalize } (S ^ {\prime}, E ^ {\prime}, L, M) = (\frac {M}{L} S ^ {\prime}, \frac {M}{L} E ^ {\prime}) \tag {19}
$$

# 3.6 Personal Adaptation

In real-world intelligent systems, the IMU data could be highly diverse across users with different devices and usage habits. To alleviate the domain-shift issue, we proposed a personal adaptation method to improve time estimation accuracy for different users. For a user, our method adds weights to the loss function to increase the proportion of his/her personal samples during the training process. By Eq.(20) and Eq.(21), we increase the weight of the target user in the loss calculation, where  represents the weight matrix,  represents the data set of the target user, and $\beta$ Wis a hyperparameter between 0 to 1 for adjusting the weight.

Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 5, No. 4, Article 189. Publication date: December 2021.

$$
L o s s _ {W} = W (L o s s _ {D} + L o s s _ {E}) \tag {20}
$$

$$
W _ {i} = \left\{ \begin{array}{l l} \beta , & i f x _ {i} \in A \\ 1 - \beta , & i f x _ {i} \notin A \end{array} \right. \tag {21}
$$

Experiment results in Section 4.5 testify that our personal adaptation method can effectively improve the inference accuracy of the target user’s key activities.

# 3.7 Model Training Process and Inference of KATN

As shown in Fig. 2, the workflow of KATN involves both model training and model inference. Alg. 2 gives the model training process and Alg. 3 gives the model inference process. Given the training dataset  with inexact labels , we first conduct the data augmentation as described in Section 3.3. The personal adaptation is an optional Yoperation, which requires the personal dataset  and the parameter $\beta .$ SAN is initialized with hyperparameters A and , and then trained with the augmented dataset ${ \bar { X } } ^ { \prime }$ β. Given the SAN trained by Alg. 2 and samples for λ α Xinference, Alg. 3 is executed to estimate the exact start and end time of the key activity in each sample. For each sample to be inferred, we input it into the SAN and obtain the temporal feature importance scores $Z _ { D }$ and $Z _ { E } .$ . Finally, we calculate the start and end times of key activities by the exact time estimation method. The ZEimplementation details of SAN will be introduced in Section 4.4.

Algorithm 2 Model Training Process   
Require:
The training dataset X with inexact labels Y
Number of training epochs: k
Hyperparameters of SAN: $\alpha$ and $\lambda$ Personal adaptation parameters:
To perform personal adaptation or not, flag
The collection of samples for personal adaptation, A
Personal adaptation hyperparameter, $\beta$ Ensure:
The trained model $\theta$ 1: $Loss = Loss_{D} + Loss_{E}$ ;
2: $X' = Augmentation(X)$ ;
3: $W = ones(X')$ ; //Initial W, all weights of samples are equal
4: $Loss = Personal\_Adaptation(Loss, flag, \beta, X', A, W)$ //Optional
5: $\theta = SAN\_init(\alpha, \lambda)$ ;
6: for i from 1 to k do
7: $\theta.fit(Loss, X')$ 8: end for
9: return $\theta$ ;

# 4 EVALUATIONS OF KATN

In this section, we evaluate the performance of our proposed KATN via extensive experiments on public datasets and data traces from a real on-demand food delivery system.

Algorithm 3 Model Inference Process   
Require:
Samples for inference: I
The trained model: $\theta$ Exact time estimation hyperparameters: L, M and $\delta$ Ensure:
Regions of Key Activity: P
1: $P = []$ 2: for $x \in I$ do
3: $Z_{D}, Z_{E} = Get\_Temporal\_Feature\_Importance(\theta, x)$ 4: $S, E = Exact\_Time\_Estimation(Z_{D}, Z_{E}, L, \theta, \delta)$ 5: $P.append([S, E])$ 6: end for
7: return P;

# 4.1 Evaluation Datasets

In our experiments, we adopt two public datasets and one dataset from a real on-demand food delivery system, which contains IMU data and the clicking “finish delivery” events from riders’ mobile phones.

Public Datasets: We adopt two public datasets: Shoaib Dataset (SHO) [37] and The University of Sussex-Huawei Locomotion (SHL) [15][45]. For both datasets, the sensor data are collected from mobile phones in various placements. The SHO dataset is composed of labeled accelerometer data from 10 users as they performed daily activities such as walking, jogging, climbing stairs, sitting, and standing with various phone placements like pocket, wrist, upper arm and belt. The SHL dataset contains human activities like stilling, running, walking, biking and etc., with various placements of mobile phones. In our experiments, we use these labeled datasets to evaluate KATN in different settings, including simple key activities and complex key activities. For simple key activity settings, denoted by ( ) − , a positive sample contains the key activity  and the noise activity . A N A NFor example, Run-Walk means Run is the key activity and Walk is the noise activity. For complex key activity settings, denoted by ( ) − , a positive sample contains the key activity ( ) and the noise activity A, B, C N A, B, C, where the key activity ( ) is a complex activity composed of three activities. ( ) − Rand means the N A, B,C A, Bnoisy activity can be a random activity other than activities  and . Unless otherwise noted, the sampling A Bfrequency of accelerometer data is 50Hz frequency and the length of the data segment is 1 minute. Moreover, in each experimental setting, the proportion of training positive samples, training negative samples and test positive samples is 6:6:4.

Riders’ Data from an On-demand Food Delivery System (ROFD): This ROFD dataset comprises 7-day IMU data and clicking “finish delivery” events from nine riders’ mobile phones in real on-demand food delivery scenarios. To obtain the ground truth, each rider wore a camera on his/her chest to record videos of food delivery processes during the 7 days. According to the videos from their body-worn cameras, it cost us a lot of manpower to label the true start and end time of key activities, namely getting on (and off) the motorcycle before (and after) the handover of food, in the IMU data. By default, the IMU data is divided into five-minute data segments. A data segment with a clicking “finish delivery” event is a positive sample, otherwise it is a negative sample. In total, we get 928 positive samples and 2860 negative samples. We randomly selected 528 positive samples and 286 negative samples as the training data, and used the rest 400 positive samples as the test data. Note that, the sampling frequency of the accelerometer data is only 10Hz due to the battery consumption requirement in the real system.

Therefore, each five-minute data segment contains 3,000 timestamps, i.e., the input size of the deep model is 3000 × 3, where 3 represents three axes of the accelerometer.

# 4.2 Evaluation Metrics

In this work, our goal is to reduce the difference between the estimated start and end time of the key activity $P = \{ ( p _ { s } ^ { i } , p _ { e } ^ { i } ) | x _ { i } \in \mathcal { I } \}$ and the groudtruth $G = \{ ( g _ { s } ^ { i } , g _ { e } ^ { i } ) | x _ { i } \in \mathcal { I } \}$ . Thus, we use the following two metrics to P ps, pe xi Gmeasure the performance of estimation methods.

# 1) IoU (>X%) Accuracy.

The intersection over union (IoU) between $g ^ { i }$ and $p ^ { i }$ is defined in Eq. (23), which is widely used in the д pobject detection field. We use IoU accuracy to measure the relative accuracy of the estimated interval. As shown in Eq. (22) and Eq. (24), IoU (>X%) accuracy is the proportion of test samples whose IoU is greater than X%. As usual, when the IoU between the estimated region and groundtruth region is greater than 50%, we regard the estimation as accurate.

$$
\text { IoU } (> \mathrm{X} \%) \text { Accuracy } = \frac {\sum_ {x _ {i} \in \mathcal {I}} Z (\mathrm{I} _ {i} , X \%)}{| \mathcal {I} |} \tag{22}
$$

$$
\mathrm{I} _ {i} = \operatorname{IoU} (g ^ {i}, p ^ {i}) = \frac {(g _ {s} ^ {i} , g _ {e} ^ {i}) \cap (p _ {s} ^ {i} , p _ {e} ^ {i})}{(g _ {s} ^ {i} , g _ {e} ^ {i}) \cup (p _ {s} ^ {i} , p _ {e} ^ {i})} \tag {23}
$$

$$
Z \left(\mathrm{I} _ {i}, X \%\right) = \left\{ \begin{array}{l l} 1, & \text {if} \mathrm{I} _ {i} \geq X \% \\ 0, & \text {if} \mathrm{I} _ {i} <   X \% \end{array} \right. \tag{24}
$$

# 2) Time Offset.

We use the time offset to measure the absolute error of the estimation as shown in Eq. (25) and Eq. (26). Meanwhile, we use the 25%, 50% and 75% percentile of time offsets  to describe the distribution.

$$
T = \text { Time\_Offset } = \{(s _ {i} = | g _ {s} - p _ {s} |, e _ {i} = | g _ {e} - p _ {e} |) \mid g \in G, p \in P \} \tag {25}
$$

$$
\text { Average\_Time\_Offset } = \frac {\sum s _ {i} + \sum e _ {i}}{2 | P |} \tag {26}
$$

# 4.3 Methods for Comparison

We compare KATN with different classic and state-of-the-art model structures. We implement an attention based method (ACN) for HAR, an instance-based method (TALNet) for sound event detection, and a global average pooling based method (RCAM) for comparison. Those methods are listed as below:

1) ACN[44] is a weakly labeled HAR model, which calculates complexity scores between local features and a global feature of the trained model to distinguish different regions. The complexity scores of each timestamp are obtained by the dot product between the output of the last CNN layer and the output of the fully connected layer.   
2) TALNet[46] builds an instance-based MIL neural network for weakly labeled sound event detection, which utilizes sigmoid function to activate features at each timestamp to represent the frame-level probabilities and then aggregates them into bag-level probabilities by a linear softmax function. After the model is trained, a value of 0 to 1 will be obtained at each timestamp to represent the instance probability and we utilize it to infer the regions of the key activity.

Table 1. Implementation Details of SAN.  and  have the same network structure, here we only present the network structure of . 

<table><tr><td>Layer Name</td><td>Output Shape</td><td>Parameter</td><td>Description</td></tr><tr><td>input(InputLayer)</td><td>(1, 3000, 3)</td><td>-</td><td>Input layer</td></tr><tr><td>conv1d (Conv1D)</td><td>(1, 3000, 32)</td><td>size = (32, 40)</td><td rowspan="2">Shared Feature Extraction</td></tr><tr><td>max_pooling1d (MaxPooling1D)</td><td>(1, 1500, 32)</td><td>size = (1, 2)</td></tr><tr><td>conv1d (Conv1D)</td><td>(1, 1500, 32)</td><td>size = (64, 40)</td><td rowspan="3">Local Feature Extraction</td></tr><tr><td>max_pooling1d (MaxPooling1D)</td><td>(1, 300, 32)</td><td>size = (1, 5)</td></tr><tr><td>bidirectional (Bidirectional)</td><td>(1, 300, 64)</td><td>size = 32</td></tr><tr><td>attention_vec(Dense)</td><td>(300, 1)</td><td>hidden = 1000</td><td rowspan="2">Siamese Attention Layers</td></tr><tr><td>attention_output(Reshape)</td><td>(300, 64)</td><td>-</td></tr><tr><td>flatten (Flatten)</td><td>(38400)</td><td>-</td><td rowspan="2">Classifier</td></tr><tr><td>output (Dense, Softmax)</td><td>(2)</td><td>-</td></tr></table>

3) RCAM[6] is a global average pooling based method, which proposes three simple but robust techniques including thresholded average pooling, negative weight clamping, and percentile as a standard for thresholding.

For a fair comparison, we utilize  for key region selection that makes the above methods perform best in δthe average time offset metric. All methods use the same training data and test data of various settings. We implemented methods for comparison using the same CNN feature extraction layers of IMU data introduced in Section 3.4.1.

# 4.4 Implementation Details

In KATN, we implement S-SAN, a single-layer network structure of SAN, and SAN with both  and DiN DeNstructures. When the key activity is simple, S-SAN is sufficient to infer the target activity, while for complex activities or realistic events in practice, SAN can better locate the target key activity with temporal features of multiple perspectives. Here, we introduce the implementation details of SAN. Taking the 5-minute data segment with a 10Hz sampling frequency as an example, the input size of SAN is (3000, 10, 3). Table. 1 gives the implementation details of each layer of SAN. For the attention layer, we utilize the sigmoid function $\displaystyle \frac { 1 } { 1 + e ^ { - x } }$ eto activate attention values rather than the softmax function. After the model is trained, the flatten layer and the output layer with softmax function are utilized to evaluate the temporal feature importance scores on each timestamp. And then, the temporal feature importance vector with a size of (300 1) will be inputted into the exact time estimation method to infer the exact start and end time. Hyper-parameter settings of  and $\beta$ will be discussed in Section 4.5.

# 4.5 Results

1) Visualization Results and Analysis.

We visualize the output values of the importance scores and the true start and end time of the key activity in different settings. When the key activity is simple, e.g., (Run)-Walk, the S-SAN method can learn the region

Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 5, No. 4, Article 189. Publication date: December 2021.

of the key activity well, as shown in Fig. 4. However, when the target key activity becomes more complex, only partial activated features of target regions are utilized by the classifier to make inferences. Thus, the conventional single view attention network like ACN and S-SAN will only focus on partial features and can’t capture the complete key activity well, resulting in inaccurate region inference. As an example in Fig. 5, where the activities are (Still, Run, Still)-Ride, ACN and S-SAN only activate the attention on the most discriminative part (i.e., Run activity only) in the key activity and fails to detect the whole parts; While, our design of SAN can detect both the discriminative part and the detailed part, achieving more accurate results as shown in Fig. 5. And Fig. 6 demonstrates the calculation process of importance score $Z _ { M }$ in SAN which is composed of $Z _ { D }$ of DiN and $Z _ { E }$ in DeN.

![](images/0dfa60d012ab85e05ba7d6f1c7c1cfc1d77223d84253f114a9ba3356031a61b2.jpg)



(a) Before training.

![](images/b2c36113699e3da168498fb175da30fe2045871aaa9a3c9d8a9a2dfeece05364.jpg)



(b) After training.   
Fig. 4. Untrained vs Trained: Visualization of importance score of S-SAN when the key activity is simple, e.g., (Run)-Walk. Here, the red line and black line represent the start time and end time of the key activity.

![](images/1f300b7a37966c83279341c95a601762f7c6575c309a1cf8bc11323b62b6730b.jpg)



(a) Complexity score of ACN.

![](images/aa256b6926b54f4b50c47abaf5e66f6ca2f944d6e929fabbc4e21b7b5d1b719b.jpg)



(b) Importance score of S-SAN.

![](images/c583bfa61ea720a2b8681e780042e3f2345858dcaa90153c75e050573eefbf6c.jpg)



(c) Importance score of SAN.   
Fig. 5. Visualization of importance scores when the key activity is complex, e.g., (Still, Run, Still)-Ride. Here, the red line and blue line represent the start time and end time of the key activity. The black line and green line represent the time of activity switching in the complex activity.

# 2) Evaluation on Public Datasets.

In this part, we conduct two groups of comparative experiments for simple key activities and complex key activities, respectively.

![](images/80bb7055f21e1b9b3b70667e69b6df3aa21c8ea004a4932ddc4493f494b12cb4.jpg)  
Fig. 6. Importance score $Z _ { M }$ of SAN is composed of $Z _ { D }$ from  and $Z _ { E }$ from  after nomarlization, $\mathrm { { e . g . , } }$ (Still, Run, Still)-Ride.

When the key activity is simple: As for simple key activities, we conduct experiments on every pair of key and noise activities on SHL dataset, like (Run)-Walk, (Run)-Still, (Run)-Ride, (Ride)-Still, (Walk)-Still and (Walk)-Ride. We first sample 1000 pairs of 10s segments from raw data and calculate the Dynamic Time Warping (DTW) distances between each pair of key activity and noise activity. Then we analyze the correlation between the DTW distances and the average time offset of KATN’s detection results. As shown in Fig. 7 and Fig. 8, the performance varies with different combinations of key activity and noise activity. When the DTW distance between two activities is large, which means the two activities are quite different, e.g., (Run)-Walk and (Run)-Riding, the average time offset is relatively small; When the DTW distance between two activities is small, which means the two activities are similar, e.g., (Ride)-Still and (Walk)-Ride, the time offset is relatively larger. According to Fig. 8, the Pearson’s Correlation Coefficient between normalized average DTW distance and average time offset is -0.905. It can be concluded that the inference ability of the key activity regions is inversely proportional to the DTW distance between the key activity and noise activity. Fig. 9a \~Fig.9f show the IoU accuracy of KATN and ACN on various simple key activities and KATN achieves obliviously higher IoU accuracy than ACN in most cases.

When the key activity is complex: In a real system, key activities are often complex activities composed of more than one single activity, e.g., food delivery. The regions of complex key activities are much more difficult to locate than simple ones as shown in visualization results. For complex activity settings, we consider (Still, Run, Still)-Ride on the SHL dataset and (Downstairs, Jog)-Rand on the SHO dataset. As shown in Fig. 10 and Fig.11, KATN with SAN significantly outperforms other methods, which achieves 2.09s average time offset and a 97 88% IoU( 50%) accuracy in (Still, Run, Still)-Ride, and achieves 2.82s . >average time offset and a 94 68% IoU( 50%) accuracy in (Downstairs, Jog)-Rand. It can be concluded that . >when the activity is complex, discriminative activation is not sufficient for complex key activity location whether the noise activity consists of a single or random activity. As described in Section 3, the design of SAN contains hyper-parameters  of $L o s s _ { D }$ in  and  of AMDP in . Thus, we conduct experiments λ LossD DiN α DeNin the complex activity setting (e.g. (Still, Run, Still)-Ride) to explore hyper-parameter settings.  is used λto adjust DiN’s attention to the discriminative part of target activity, and  represents the proportion of α in the entire task as shown in Fig.12a and Fig.12b. We can figure out that when $\lambda \in ( 0 . 1 , 1 )$ and  is DiNrelatively large (larger than 0.7), KATN with SAN has a good performance.

# 3) Evaluation on ROFD Dataset.

We evaluate methods on the ROFD dataset from a real on-demand food delivery system as described in Section 4.1 and present results in Table 2. KATN with SAN ( =0.1, =0.98) obtains 83.0% IoU(>50%) accuracy and 17.80s average time offset, which significantly outperforms the 64.5%∼71.3% IoU accuracy

![](images/489012412352ab302a3024315162882cb022c43f535ae6a7abee2eb5750de4d9.jpg)



Fig. 7. Average time offset and average DTW distance on SHL Dataset with simple key activity settings by KATN.

![](images/889a79843de7abd83635168a55bcabdc461935748237f045a2fda0b2876c1245.jpg)



Fig. 8. Normalized average time offset and average DTW distance on SHL Dataset with simple key activity settings. The Pearson’s Correlation Coefficient is -0.905.

![](images/05210aa08ecc4aa449d7bba12e38e6946ef346f6100e63a008e5fc83f5a06838.jpg)



(a) (Run)-Walk.

![](images/3f6b4a97578d9c61731358448e68b8db63320c57a7b2bc20b4fb783225722021.jpg)



(b) (Run)-Still

![](images/b71c719f40440c7e074deee9ae794bf3e528d8b1d2cca737086259bb3392a0f7.jpg)



(c) (Run)-Riding.

![](images/6c049411a32a16e39fb54f4d8dcd84bdd9aeb80091d41aa3938e1658d9b3dbcf.jpg)



(d) (Riding)-Still.

![](images/eb05af3e9340040ce4aa54974e1eee566301b9bdaf011834b5c6457a2e67ee0b.jpg)



(e) (Walk)-Still.

![](images/3cd223b5f92e1c86c3b04cac573da31e543f05b53654cd7246bd423f75dfef2d.jpg)



(f ) (Walk)-Riding.   
Fig. 9. IoU (>X%) accuracy on SHL dataset in simple activity settings by ACN and KATN with S-SAN.

![](images/0b90b0c9ecb0793c396242e014f2c0aff8fb08796f0602cc41e2aa55102b33fc.jpg)



Fig. 10. Performance of different methods with the complex activity setting, (Still, Run, Still)-Ride, on SHL dataset.

![](images/bc816c61a9d1d3c5cf9509692a4346d5f3498199e194ac5f30968f1571645dfc.jpg)



Fig. 11. Performance of different methods with the complex activity setting, (Downstairs, Jog)-Rand, on SHO dataset.

and 25.38s∼32.25s average time offset of other methods. Fig. 15 illustrates the distribution of average time offsets by KATN on ROFD dataset, where most of the time offsets are less than 20s.

4) Impact of Sampling Frequency and Segment Length.

In this part, we evaluate the impact of different sampling frequencies and segment lengths on the key activity localization task. Here, we use the (Run)-Walk data of the SHL dataset for the experiments. Fig. 13 shows that the sampling frequency of IMU data has a great influence on the performance. When the sampling frequency is $1 0 \mathrm { H z } ,$ the IoU(>50%) accuracy is 88.80% and the average time offset is 4.3s. As the sampling frequency increases to 50Hz, KATN achieves 97.72% IoU(>50%) accuracy and 1.3s average time offset due to the reason that richer features can be captured with a higher sampling frequency. Fixing the sampling frequency to 50Hz, Fig. 14 illustrates that the IoT(>50%) accuracy of KATN drops from 97.72% to 94.74% when the segment length changes from 1min to 3min. The reason is that the longer the data segment, the more noise activities it contains and the more parameters need to be trained, which increases the difficulty for key activity localization.

![](images/c10569db155b741102f98ac6e6d940c115a110287717bc5753733a42f43d7637.jpg)



(a) Average time offset with various  settings ( = 0 8).

![](images/1e469ed9f20b68fdaed0235fbea7389e6c941ef52efb65334c8e0934e6754c5c.jpg)



(b) Average time offset with various  settings ( = 0 1).

Fig. 12. Experiments on hyperparameter study in the complex activity setting, (Still,Run,Still)-Ride.   
Table 2. Performance of different methods on the ROFD Dataset. P is the acronym of percentile. 

<table><tr><td>Methods</td><td>IoU(&gt;50%) Accuracy</td><td>IoU(&gt;80%) Accuracy</td><td>Average Offset(s)</td><td>25% P</td><td>50% P</td><td>75% P</td></tr><tr><td>ACN</td><td>64.5%</td><td>42.3%</td><td>32.25</td><td>5.85</td><td>19.17</td><td>51.49</td></tr><tr><td>TALNet</td><td>67.8%</td><td>47.0%</td><td>25.38</td><td>5.19</td><td>10.85</td><td>31.00</td></tr><tr><td>RCAM</td><td>71.3%</td><td>42.1%</td><td>29.13</td><td>7.30</td><td>16.98</td><td>41.33</td></tr><tr><td>KATN</td><td>83.0%</td><td>57.5%</td><td>17.80</td><td>5.07</td><td>9.87</td><td>20.40</td></tr></table>

![](images/e29300cac6de7401624878d6af264fbf1ebec6889b65357a49c8484b36c18bff.jpg)



Fig. 13. Time offset & IoU (>50%) accuracy by KATN with various sampling frequencies. The segment length is 1 minutes.

![](images/376e4ba141f67307456c2940b25bc3706d93a678ff315f6ab128a35c0f5c4014.jpg)



Fig. 14. Time offset & IoU (>50%) accuracy of KATN with various segment lengths. The sampling frequency is 50Hz.

Table 3. Experiments of ablation study via KATN with SAN on the ROFD dataset. 

<table><tr><td>Method</td><td>IoU(&gt;50%) Accuracy</td><td>IoU(&gt;80%) Accuracy</td><td>Average Offset(s)</td></tr><tr><td>KATN</td><td>83.0%</td><td>57.5%</td><td>17.80</td></tr><tr><td>Removing negative sample mixup</td><td>81.0%</td><td>54.5%</td><td>19.38</td></tr><tr><td>Removing  $Loss_{N}$ , equal to  $\lambda = 0$ </td><td>78.8%</td><td>54.3%</td><td>19.85</td></tr><tr><td>Removing network  $DeN$ </td><td>74.3%</td><td>51.8%</td><td>21.97</td></tr></table>

# 5) Personal Adaptation.

We propose a method for personal adaptation as described in Section 3.6. To compare the model performance before and after personal adaptation on the test data of the corresponding rider, we conduct experiments on three riders’ data from ROFD dataset separately $( \beta = 0 . 7 )$ and give the mean performance. As shown β .in Fig. 16, compared with the nonadaptive version, our personal adaptation strategy decreases the time offsets as well as increases the IoU accuracy significantly. It can be concluded that appropriately increasing the proportion of a user’s data in training can neither destroy the diversity of data but also enhances the personalization capabilities of the model.

# 6) Ablation Study.

We conduct an ablation study of KATN with SAN on ROFD dataset to figure out the importance of each part by removing each component separately. As shown in Table. 3, we measure the effect of: (1) without negative sample mixup; (2) without , or $\lambda = 0 ;$ (3) without network , or without siamese structure. LossN λ DeNWe can figure out that  and  have a significant impact on the model performance. And negative LossN DeNsample mixup can also increase the diversity of data for better performance.

![](images/6cd1a7749bd6d205da94877fdc115d31cef0bcfb6b34cd43e6b4409a15134149.jpg)



Fig. 15. Distribution of average time offsets on the ROFD dataset via KATN.

![](images/c4b636b0bfe10f0c719bba908f5e6abafb99e451800ad1afd237694369afd4a6.jpg)



Fig. 16. Original Method vs Personal Adaptation (when $\beta = 0 . 7 )$ .

![](images/46ae2b42f85a8ba89e5f8f71552587c2603821ced06704e3c0344d1ad3a38c10.jpg)



Fig. 17. A user-friendly IMU annotation system.

# 5 USER-FRIENDLY IMU DATA ANNOTATION

In this section, we leverage our proposed technology to build a novel user-friendly IMU Data annotation system. Unlike audio and video data, IMU data is difficult for human to annotate directly. There are usually two traditional ways to label IMU data: (1) the user clicks the start and end buttons in a data collection application right before and after he/she performs specific activities. (2) a user needs to film specific activities by a body-worn camera or surveillance camera when he/she is collecting the IMU data, and then align the video with the IMU data to label the IMU data. These two methods are cumbersome and need well-trained data collectors, therefore they are not practical to label large-scale IMU data.

We propose a novel user-friendly IMU data annotation system based on KATN, which only requires data collectors to answer the yes or no and then obtains the clean labeled IMU data of target activities. As shown in Fig. 17, if we need a large amount of IMU data of the upstairs activity, the annotation system will send fuzzy questions like ’Have you climbed the stairs recently?’ to data collectors of the system. Collectors only need to answer yes or no to this question, which is easy for anyone with or without professional knowledge. And then, the system trains KATN with collectors’ data segments and the corresponding inexact labels. The label is positive if the answer is yes, otherwise the label is negative. Finally, we can estimate the exact region of the target activity, and then obtain the labeled IMU data with the trained KATN and a data cleaning method. Our annotation mechanism effectively saves human effort for labeling IMU data and increases the efficiency of large-scale IMU data annotation.

Data Cleaning Method: The system sends fuzzy activity questions about whether the target activity has happened recently to data collectors. For data segment  with an answer “Yes”, KATN infers the region $r _ { i } = ( s , e )$ xi ri s, eof the target activity, where ,  represent the start time and end time of the activity, respectively. Since different s edata requesters have different requirements for the cleanliness of the labeled data, we appropriately cut the beginning and the end of the region according to a cleanliness parameter , and obtain cleaned $r _ { \lambda } ^ { i }$ according λto Alg. 4. We utilize ( ), ( ) and  ( ) values to evaluate the annotated data as shown in $\operatorname { E q . } ( 2 7 ) \sim \operatorname { E q . } \ ( 2 8 )$ puri, where $G = \{ g _ { i } \}$ antity λ validate λ represents the groudtruth of key activity regions.

$$
P u r i t y (\lambda) = \frac {\sum (r _ {\lambda} ^ {i} \cap g _ {i})}{\sum r _ {\lambda} ^ {i}} \quad , g _ {i} \in G, r ^ {i} \in R _ {\lambda} \tag {27}
$$

Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 5, No. 4, Article 189. Publication date: December 2021.

Algorithm 4 Data Cleaning Method   
Require:
    Region set from KATN: R
    r = (s, e) ∈ R, r.s and r.e represent start time and end time of the region
    Filter threshold: T
    Cleanliness: λ

Ensure:
    Cleaned labeled data, $R_{\lambda}$ 1: $R_{\lambda} = [ ]$ ;
2: for $r \in R$ do
3: if r.e - r.s > T then
4: $M = (r.e - r.s)\lambda$ ;
5: clean_r = (r.s + M, r.e - M);
6: $R_{\lambda}.append(clean_r)$ ;
7: end if
8: end for
9: return $R_{\lambda}$ ;

$$
\text { Quantity } (\lambda) = \sum r _ {\lambda} ^ {i} \tag {28}
$$

$$
\text { Validate } (\lambda) = \text { Quantity } (\lambda) \text { Purity } (\lambda) \tag {29}
$$

We validate our annotation mechanism for an upstairs activity collection task on the SHO dataset with a 50Hz sampling frequency. For positive samples, we randomly mixed upstairs activities (10∼30s) with random activities including walk, jog, sit, stand, and downstairs to form 1-minute data segments. For negative samples, data segments are composed of random activities except upstairs. There are 400 positive samples and 400 negative samples in total. In our simulated annotation task, each query can obtain one sample with an inexact label (i.e., yes or no). As shown in Fig. 18 , when the total number of queries increases from 200 to 800, IoU (>50%) accuracy increases from 72.00% to 95.75%. Fig. 19 also shows that the IoU accuracy improves with more queries, especially when the number of queries grows from 200 to 400. The reason is that more queries bring more coarse-grained labeled data segments for training KATN, thus improve the inference accuracy of KATN. Fig. 20a ∼ Fig. 20c demonstrate the performance of the data cleaning method with different numbers of queries and different (from 0 to 0.5), where the threshold  = 20. In all cases, larger  can effectively increase the purity to about $9 7 \% ,$ T λmeanwhile decreases the quantity and validate values. For example, when there are 800 queries, the purity grows from 90.81% to 97.34% and the validate data decreases from 7162s to 2922s. Therefore, our data cleaning method can significantly improve the cleanliness of the labeled data. With the data cleaning method, we can adjust and select the appropriate hyperparameters to meet the requirements for the quantity and purity of inexactly annotated IMU data.

# 6 DISCUSSION

In this section, we discuss the limitations of this work and potential future work.

Scope of Applications: Our method is suitable for various key activity detection scenarios where cheap and inexact labels can be obtained, such as the click button events in the on-demand food delivery system and the answers to the fuzzy questions in the annotation system. There are many other forms of inexact labels. For example, in an on-demand taxi system, the actual time of passengers getting in the car is a kind of key information. The driver clicking the “passenger has arrived” button can be used as the inexact label of the key activity. Once there is a strong correlation between a coarse-grained event and the key activity, we can utilize the coarse-grained event as the inexact label. And then, the IMU data around inexact labels can be considered as positive samples, while the data from other time periods can be considered as negative samples. Finally, KATN can be trained on such a dataset to infer the exact region of the key activity.

![](images/8ed1a491e20c7e03ef05b3ad1db98c9754342a08e452287464f81c244ccba36a.jpg)



Fig. 18. Time offset & IoU (>50%) accuracy with different numbers of queries.

![](images/c68ab4ebe2c822f0f78ce3d098ef5d2167146cb7b92560c79565f048cf850ee5.jpg)



Fig. 19. IoU (>X%) accuracy with different numbers of queries.

![](images/ca23a4c606138381aff4e025a937f56926865f6c2ed3c5f8fee7fa0326098660.jpg)



(a) 200 Queries.

![](images/495bdb0cdd78acb9abf4940fa4fac3dbb9fce947f224a7ae2e6487676b8f1342.jpg)



(b) 400 Queries.

![](images/7240e7fa3a14a669f6d069804817eb7f552dd46446515438eca12cda896e1a0b.jpg)



(c) 800 Queries.   
Fig. 20. Purity, quantity and validate values with parameter  from 0 to 0.5,  = 20.

Limitation of the Method: Our design has three limitations: First, the precision of our estimated start and end time is limited by the granularity of temporal features before the classifier. In our future work, we will explore different sizes of CNN kernels to achieve a more precise time estimation. Second, the current design can not deal with multi-modal IMU data very well, thus multi-modal data can only be simply stacked in the input layer. In the future, we will explore a more efficient fusion method for multi-modal IMU data. Third, the exact time estimation method is mainly designed for only one key activity in the data segment. If multiple activities occur closely, our method needs to be extended to divide the temporal feature importance scores by methods like using a sliding window or a clustering algorithm.

User-Friendly Crowdsourcing Annotation System: Our user-friendly annotation mechanism provides a potential for large-scale labeling of IMU data. At present, we only validate the mechanism via simulations on public datasets. In the future, we will implement this design in a real crowdsourcing system to evaluate its effectiveness and generality when there are a large number of participants and diverse target activities.

# 7 CONCLUSION

It is quite laborious and difficult to collect and label IMU data of human activities, and also intractable to detect the exact start and end time of activities. In this paper, we propose a key activity detection system (KATN) using only raw IMU data with inexact information. A siamese key activity attention network (SAN) is designed to extract temporal features of IMU data with multi-view attention perspectives. By interpreting behaviors of SAN, KATN can accurately locate regions of key activities. Comprehensive experiments demonstrate that KATN has superior power in the key activity detection task for IMU data. Moreover, to explore other applications of our technology, we design and evaluate a novel user-friendly IMU data annotation mechanism that provides a potential for large-scale IMU data annotation.

# ACKNOWLEDGMENTS

Lan Zhang is the corresponding author. The research is supported by National Key R&D Program of China 2018YFB0803400, China National Natural Science Foundation with No. 61822209, No. 61932016, No. 61625205, No. 62132018, Key Research Program of Frontier Sciences, CAS, No. QYZDY-SSW-JSC002.

# REFERENCES

[1] Roy Adams and Benjamin M Marlin. 2018. Learning Time Series Segmentation Models from Temporally Imprecise Labels.. In UAI. 135–144.   
[2] Mussab Alaa, Aws Alaa Zaidan, Bilal Bahaa Zaidan, Mohammed Talal, and Miss Laiha Mat Kiah. 2017. A review of smart home applications based on Internet of Things. Journal of Network and Computer Applications 97 (2017), 48–65.   
[3] Bandar Almaslukh, A. M. Artoli, and J. Al-Muhtadi. 2018. A Robust Deep Learning Approach for Position-Independent Smartphone-Based Human Activity Recognition. Sensors (Basel, Switzerland) 18 (2018).   
[4] D. Anguita, A. Ghio, L. Oneto, X. Parra, and Jorge Luis Reyes-Ortiz. 2012. Human Activity Recognition on Smartphones Using a Multiclass Hardware-Friendly Support Vector Machine. In IWAAL.   
[5] Gentry Atkinson and Vangelis Metsis. 2021. TSAR: a Time Series Assisted Relabeling Tool for Reducing Label Noise. (2021).   
[6] Wonho Bae, Junhyug Noh, and Gunhee Kim. 2020. Rethinking Class Activation Mapping for Weakly Supervised Object Localization. In European Conference on Computer Vision. Springer, 618–634.   
[7] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. 2014. Neural machine translation by jointly learning to align and translate. arXiv preprint arXiv:1409.0473 (2014).   
[8] Marc-André Carbonneau, Veronika Cheplygina, Eric Granger, and Ghyslain Gagnon. 2018. Multiple instance learning: A survey of problem characteristics and applications. Pattern Recognition 77 (2018), 329–353.   
[9] Youngjae Chang, Akhil Mathur, Anton Isopoussu, Junehwa Song, and Fahim Kawsar. 2020. A systematic study of unsupervised domain adaptation for robust human-activity recognition. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 4, 1 (2020), 1–30.   
[10] Youngjae Chang, Akhil Mathur, Anton Isopoussu, Junehwa Song, and Fahim Kawsar. 2020. A Systematic Study of Unsupervised Domain Adaptation for Robust Human-Activity Recognition. 4, 1 (2020). https://doi.org/10.1145/3380985   
[11] Yiqiang Chen, Jindong Wang, Meiyu Huang, and Han Yu. 2019. Cross-position activity recognition with stratified transfer learning. Pervasive and Mobile Computing 57 (04 2019). https://doi.org/10.1016/j.pmcj.2019.04.004   
[12] Y. Chen, Zhongtang Zhao, Shuangquan Wang, and Z. Chen. 2012. Extreme learning machine-based device displacement free activity recognition model. Soft Computing 16 (2012), 1617–1625.   
[13] Mariella Dimiccoli, Juan MarÃŋn Vega, and Edison Thomaz. 2018. Mitigating Bystander Privacy Concerns in Egocentric Activity Recognition with Deep Learning and Intentional Image Degradation. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 1 (01 2018), 1–18. https://doi.org/10.1145/3161190

Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 5, No. 4, Article 189. Publication date: December 2021.

[14] Yan Gao, Yang Long, Yu Guan, Anna Basu, Jessica Baggaley, and Thomas Ploetz. 2019. Towards reliable, automated general movement assessment for perinatal stroke screening in infants using wearable accelerometers. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 3, 1 (2019), 1–22.   
[15] Hristijan Gjoreski, Mathias Ciliberto, Lin Wang, Francisco Javier Ordonez Morales, Sami Mekki, Stefan Valentin, and Daniel Roggen. 2018. The university of sussex-huawei locomotion and transportation dataset for multimodal analytics with mobile devices. IEEE Access 6 (2018), 42592–42604.   
[16] Alex Graves, Navdeep Jaitly, and Abdel-rahman Mohamed. 2013. Hybrid speech recognition with deep bidirectional LSTM. In 2013 IEEE workshop on automatic speech recognition and understanding. IEEE, 273–278.   
[17] Yu Guan and Thomas Plötz. 2017. Ensembles of Deep LSTM Learners for Activity Recognition Using Wearables. Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 1, 2 (2017). https://doi.org/10.1145/3090076   
[18] Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long short-term memory. Neural computation 9, 8 (1997), 1735–1780.   
[19] Yu-Jin Hong, Ig-Jae Kim, Sang Chul Ahn, and Hyoung-Gon Kim. 2010. Mobile health monitoring system based on activity recognition using accelerometer. Simulation Modelling Practice and Theory 18, 4 (2010), 446–455.   
[20] H M Sajjad Hossain, Md Abdullah Al Hafiz Khan, and Nirmalya Roy. 2017. Active learning enabled activity recognition. Pervasive and Mobile Computing 38 (2017), 312 – 330. https://doi.org/10.1016/j.pmcj.2016.08.017 Special Issue IEEE International Conference on Pervasive Computing and Communications (PerCom) 2016.   
[21] H M Sajjad Hossain, Md Abdullah Al Hafiz Khan, and Nirmalya Roy. 2018. DeActive: Scaling Activity Recognition with Active Deep Learning. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 2 (07 2018), 1–23. https: //doi.org/10.1145/3214269   
[22] Derek Hao Hu, Vincent Wenchen Zheng, and Qiang Yang. 2011. Cross-domain activity recognition via transfer learning. Pervasive and Mobile Computing 7, 3 (2011), 344 – 358. https://doi.org/10.1016/j.pmcj.2010.11.005 Knowledge-Driven Activity Recognition in Intelligent Environments.   
[23] J. Hu, L. Shen, and G. Sun. 2018. Squeeze-and-Excitation Networks. In 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition. 7132–7141. https://doi.org/10.1109/CVPR.2018.00745   
[24] Manfred Huber, Gergely Zaruba, Nicholas Burns, and Kathryn Daniel. 2017. SmartCare: An introduction. 394–400. https://doi.org/10. 1109/PERCOMW.2017.7917595   
[25] Qiuqiang Kong, Changsong Yu, Yong Xu, Turab Iqbal, Wenwu Wang, and Mark D. Plumbley. 2019. Weakly Labelled AudioSet Tagging With Attention Neural Networks. IEEE/ACM Transactions on Audio, Speech, and Language Processing 27, 11 (2019), 1791–1802. https://doi.org/10.1109/TASLP.2019.2930913   
[26] Hyeokhyen Kwon, Gregory D Abowd, and Thomas Plötz. 2019. Handling annotation uncertainty in human activity recognition. In Proceedings of the 23rd International Symposium on Wearable Computers. 109–117.   
[27] Yann LeCun, Koray Kavukcuoglu, and Clément Farabet. 2010. Convolutional networks and applications in vision. In Proceedings of 2010 IEEE international symposium on circuits and systems. IEEE, 253–256.   
[28] Haojie Ma, Wenzhong Li, Xiao Zhang, Songcheng Gao, and Sanglu Lu. 2019. AttnSense: Multi-level Attention Mechanism For Multimodal Human Activity Recognition.. In IJCAI. 3109–3115.   
[29] Andrea Mannini and Angelo Sabatini. 2010. Machine Learning Methods for Classifying Human Physical Activity from On-Body Accelerometers. Sensors (Basel, Switzerland) 10 (02 2010), 1154–75. https://doi.org/10.3390/s100201154   
[30] Brian McFee, Justin Salamon, and Juan Pablo Bello. 2018. Adaptive Pooling Operators for Weakly Labeled Sound Event Detection. IEEE/ACM Transactions on Audio, Speech, and Language Processing 26, 11 (2018), 2180–2193. https://doi.org/10.1109/TASLP.2018.2858559   
[31] Koichi Miyazaki, Tatsuya Komatsu, Tomoki Hayashi, Shinji Watanabe, Tomoki Toda, and Kazuya Takeda. 2020. Weakly-supervised sound event detection with self-attention. In ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 66–70.   
[32] Vishvak S Murahari and Thomas Plötz. 2018. On attention models for human activity recognition. In Proceedings of the 2018 ACM International Symposium on Wearable Computers. 100–103.   
[33] N. D. Nguyen, Duong Trong Bui, P. H. Truong, and Gu-Min Jeong. 2018. Position-Based Feature Selection for Body Sensors regarding Daily Living Activity Recognition. J. Sensors 2018 (2018), 9762098:1–9762098:13.   
[34] Xin Qin, Yiqiang Chen, Jindong Wang, and Chaohui Yu. 2019. Cross-dataset activity recognition via adaptive spatial-temporal transfer learning. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 3, 4 (2019), 1–25.   
[35] Vitor F. Rey and Paul Lukowicz. 2017. Label Propagation: An Unsupervised Similarity Based Method for Integrating New Sensors in Activity Recognition Systems. Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 1, 3, Article 94 (Sept. 2017), 24 pages. https: //doi.org/10.1145/3130959   
[36] Arianna Seghezzi and Riccardo Mangiaracina. 2020. On-demand food delivery: investigating the economic performances. International Journal of Retail & Distribution Management (2020).   
[37] Muhammad Shoaib, Stephan Bosch, Ozlem Durmaz Incel, Hans Scholten, and Paul JM Havinga. 2014. Fusion of smartphone motion sensors for physical activity recognition. Sensors 14, 6 (2014), 10146–10176.

[38] Ting-Wei Su, Jen-Yu Liu, and Yi-Hsuan Yang. 2017. Weakly-supervised audio event detection using event-specific Gaussian filters and fully convolutional networks. In 2017 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). 791–795. https://doi.org/10.1109/ICASSP.2017.7952264   
[39] Eu Wern Teh, Mrigank Rochan, and Yang Wang. 2016. Attention Networks for Weakly Supervised Object Localization.. In BMVC. 1–11.   
[40] Yunus Emre Ustev, Ozlem Durmaz Incel, and Cem Ersoy. 2013. User, device and orientation independent human activity recognition on mobile phones: Challenges and a proposal. In Proceedings of the 2013 ACM conference on Pervasive and ubiquitous computing adjunct publication. 1427–1436.   
[41] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. arXiv preprint arXiv:1706.03762 (2017).   
[42] F. Wang, M. Jiang, C. Qian, S. Yang, C. Li, H. Zhang, X. Wang, and X. Tang. 2017. Residual Attention Network for Image Classification. In 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 6450–6458. https://doi.org/10.1109/CVPR.2017.683   
[43] Jindong Wang, Yiqiang Chen, Shuji Hao, Xiaohui Peng, and Lisha Hu. 2017. Deep Learning for Sensor-based Activity Recognition: A Survey. Pattern Recognition Letters 119 (07 2017). https://doi.org/10.1016/j.patrec.2018.02.010   
[44] Kun Wang, Jun He, and Lei Zhang. 2019. Attention-based convolutional neural network for weakly labeled human activities’ recognition with wearable sensors. IEEE Sensors Journal 19, 17 (2019), 7598–7604.   
[45] Lin Wang, Hristijan Gjoreski, Mathias Ciliberto, Sami Mekki, Stefan Valentin, and Daniel Roggen. 2019. Enabling reproducible research in sensor-based transportation mode recognition with the Sussex-Huawei dataset. IEEE Access 7 (2019), 10870–10891.   
[46] Yun Wang, Juncheng Li, and Florian Metze. 2019. A comparison of five multiple instance learning pooling functions for sound event detection with weak labeling. In ICASSP 2019-2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 31–35.   
[47] Ming Zeng, Haoxiang Gao, Tong Yu, Ole J Mengshoel, Helge Langseth, Ian Lane, and Xiaobing Liu. 2018. Understanding and improving recurrent networks for human activity recognition by continuous attention. In Proceedings of the 2018 ACM International Symposium on Wearable Computers. 56–63.   
[48] Fusang Zhang, Niu Kai, Jie Xiong, Beihong Jin, Tao Gu, Yuhang Jiang, and Daqing Zhang. 2019. Towards a Diffraction-based Sensing Approach on Human Activity Recognition. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 3 (03 2019), 1–25. https://doi.org/10.1145/3314420   
[49] Liyue Zhao, Gita Sukthankar, and Rahul Sukthankar. 2011. Incremental relabeling for active learning with noisy crowdsourced annotations. In 2011 IEEE Third International Conference on Privacy, Security, Risk and Trust and 2011 IEEE Third International Conference on Social Computing. IEEE, 728–733.   
[50] Liyue Zhao, Gita Sukthankar, and Rahul Sukthankar. 2011. Robust active learning using crowdsourced annotations for activity recognition. In Workshops at the Twenty-Fifth AAAI Conference on Artificial Intelligence.   
[51] B. Zhou, A. Khosla, A. Lapedriza, A. Oliva, and A. Torralba. 2016. Learning Deep Features for Discriminative Localization. In 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2921–2929. https://doi.org/10.1109/CVPR.2016.319   
[52] Zhijun Zhou, Yingtian Zhang, Xiaojing Yu, Panlong Yang, Xiang-Yang Li, Jing Zhao, and Hao Zhou. 2020. XHAR: Deep Domain Adaptation for Human Activity Recognition with Smart Devices. In 2020 17th Annual IEEE International Conference on Sensing, Communication, and Networking (SECON). IEEE, 1–9.   
[53] Zhi-Hua Zhou. 2018. A brief introduction to weakly supervised learning. National science review 5, 1 (2018), 44–53.   
[54] Lin Zhu, Wei Yu, Kairong Zhou, Xing Wang, Wenxing Feng, Pengyu Wang, Ning Chen, and Pei Lee. 2020. Order Fulfillment Cycle Time Estimation for On-Demand Food Delivery. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2571–2580.