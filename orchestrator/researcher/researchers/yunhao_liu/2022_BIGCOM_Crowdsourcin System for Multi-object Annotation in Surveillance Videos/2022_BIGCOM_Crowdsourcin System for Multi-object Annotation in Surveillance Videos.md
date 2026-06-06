# Crowdsourcing System for Multi-object Annotation in Surveillance Videos

Zheng Zhang⇤†, Zixin Zhao⇤‡, Lan Zhang⇤‡, Xiangyang Li⇤‡

⇤LINKE Lab, University of Science and Technology of China

†School of Data Science, University of Science and Technology of China

‡School of Computer Science and Technology, the CAS Key Laboratory of Wireless-optical Communications,

University of Science and Technology of China

Email:zzhang96@mail.ustc.edu.cn, zhaozx20@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, xiangyangli@ustc.edu.cn

Abstract—The collection and labeling of data is a laborintensive task and this has given rise to a large market for data crowdsourcing transactions. While there are many publicly available video datasets, task-specific data is still scarce and requires Customized annotation services are required. Even with many excellent auxiliary models and tools, video annotation is still a lengthy and time-consuming task. To address these challenges, this paper provides a new and effective annotation method in which the annotator no longer just provides annotations, but also plays the role of a reviewer to review the annotation results of other annotators. This method focuses on surveillance video data, in addition, it also supports adding additional custom tasks (e.g., action tagging, person relationship recognition, video summarization, etc.). And in this paper we mainly consider the additional custom temporal action annotation task. In this paper, we develop rules for filtering frames or segments that need to be re-labeled based on the temporal information of the model inference results and rely on the correlation between target and time to determine the task relevance, and asynchronously assign the task to different annotators for and dynamically portray the ability of the annotators while annotation is in progress, so as to allocate tasks to achieve annotation and mutual review of annotators. We have experimentally demonstrated that this method can reduce costs and improve labeling accuracy.

Index Terms—Object annotation, tracking, task assignment

# I. INTRODUCTION

Nowadays, with the development of deep learning, multiobject tracking has been widely applied in real scenes. Good models require high quality data. Therefore, video annotation of multi-target tracking is very important. Several models [1] [2] [3] already exist that can handle many simple tasks, such as hallway and park. In complex tasks, due to dense crowds and comp the effect of models is not enough. Therefore, training and evaluation of these multi-object detection and tracking models require a large amount of ground truth data.

Video devices pervade every corner of life, becoming an important source of information. It is an important problem that how to get information rapidly from video data. Multi-object tracking algorithms have developed rapidly in recent years, from modeling matching algorithm, association hypothesis algorithm, kernel correlation filtering algorithm, detection-based algorithm to the current deep learning algorithm. However, in order to better achieve the purpose of extracting correct information, manual annotation is still needed.

![](images/8860aeafd4218791c7516e2f5f463c5313ef939ff780f2e271538515c6d44e36.jpg)



Fig. 1. Nowadays, semi-automatic video annotation mainly uses relevant models to produce results first, and then the worker changes or supplements the results.

Data collection and annotation has always been a timeconsuming and inefficient task, especially for video data. There are two main reasons: (1) most of the SOTA models have many parameters and require a lot of data, and (2) there are many annotation forms for video annotation, which are far higher than the complexity of image annotation, and there are very few annotation tools available for different forms. Some existing annotation tools, such as Labelme, VoTT and so on, require workers to annotate frame by frame. Therefore, it is necessary to reduce the complexity of video annotation. Some work considers the model aspect, using few-shot learning to train the model to reduce the amount of data. Some work considers the annotation process aspect, training some auxiliary models or modifying annotation process to reduce the burden of labeling, as shown in fig.1. There is also work to optimize the task assignment method and assign difficult tasks to the most suitable person to annotate them.

Our scene is a crowd video annotation task. The challenge of this problem is that video annotation is a time-consuming and labor-intensive work. With different tasks, the annotation forms are different, and the accuracy of the annotation result of the workers cannot be measured. In the previous video annotation, one worker focus on one video, and tasks were independent. When reviewers check each worker’s results, they must also re-watch the video to judge whether the result is qualified. This not only requires the reviewer to be sensitive to errors, but also requires the workers to accept the task of re-annotating the video. There are many subtasks in video annotation, such as centroid(assign an identity to each object), bounding box(cover objects with rectangular frames), trajectory(ensure that the rectangle always follows the corresponding object) and so on. Because these subtasks are all from one video, they are independent. Based on this feature, we set up a task assignment mechanism including annotation and review.

In this paper, we apply this method to the actual scene. Our background is surveillance video analysis in AIoT(Artificial Intelligence & Internet of Thing). The task is to analyze the state of each person at each moment in the classroom or in the office. The existing public data sets can not satisfy the training of action models in specific scenarios. Therefore, we need to customize video annotation tasks according to the actual requirements of the project to obtain data sets that meet the requirements of the training model. In addition, the frames in classrooms and offices are relatively single, and the proportion of special time needed to be annotated is not large. The special actions need to be annotated are sparsely distributed throughout the video, so it is very expensive to annotate frame by frame.

In all, our contributions can be summarized as follows:

• Analyze the performance of existing multi-target tracking models in the surveillance screen from a real project and common additional tasks, we treat temporal action recognition as an additional task, use multiple multi-target tracking models to reason about video data, and with the goal of finding errors in model inference results that need to be manually corrected and constructing reliable We propose a task discovery mechanism for multi-objective tracking models and additional customized tasks with the goal of finding errors in model inference results that require manual correction and constructing reliable golden tasks. We propose a task discovery mechanism for multi-objective tracking models and additional customized tasks, and analyze the cost share of constructing golden tasks in crowdsourcing.

• Establishes a mechanism for calculating and updating the ability of the annotator relying on the golden task, and analyzes the association relationship between each task We propose an assignment algorithm based on associated tasks, and analyze how our improvement can replace the The annotation audit work is analyzed.   
• Integrating task discovery and task assignment to introduce the overall multi-objective crowdsourcing annotation approach of our process. Additional tasks are divided into pure annotation and active learning approaches, and custom tasks are discussed to train while annotating the available models.   
Verified that our task discovery mechanism has high filtering accuracy on public datasets, while targeting gold task constructed for our own classroom dataset is also highly accurate. We also demonstrate the clear advantage of our method is clearly superior in association tasks, and

finally done for action recognition tasks.

# II. RELATED WORK

# A. Multi-object tracking

Multiple Object Tracking has received increasing attentions which aims to identify and track objects in videos. Object detection, feature extraction/motion prediction, affinity and association are four usual components in MOT algorithm [4]. In the object detection stage, different detectors including Faster R-CNN [5], SSD [6] and YOLO series of detector [7], [8] have been studied. Yu et al [9] demonstrates that high quality detection could keep final MOT algorithm performance even with simple tracking algorithms. As for feature extraction, deep learning models have shown their strong power in extracting distinguishable features and are widely adopted. Wang et al. [10] first presented autoencoder network in their MOT algorithm. Affinity means measure distance between different tracklets. Milan et al [11] utilized RNN to compute affinity which is the first end-to-end affinity computation approach. Zhu et al [12] employed Temporal Attention Network to calculate weight of the features before fed into BiLSTM. Association is another key component. Traditional methods like Hungarian algorithm has shown promising effect. Recently, deep learning models has been adopted to improve association performance [4]. Bidirectional GRU RNN [13] and deep multi-layer perceptron [14] have been explored to decide where to split tracklets.

# B. Semi-automatic Annotation

There is a vast amount of video data generated in daily life. To better understand video content, video annotation is unavoidable. Video annotation tools could relief human from labor-intensive work and reduce cost, thus has promising future [15]. iVAT [16] featuring high flexibility has three annotation modules: manual, semi-automatic and automatic. It employs Open Computer Vision library as the CV algorithm. ViTBAT [17] is another video annotation tool that provides both low-level tracking for individual tracking and highlevel behavior recognition. It is implemented on MATLAB and has its own Computer Vision toolbox. VATIC [18] is a crowdsourcing platform that aims to provide high quality label for complex videos. It is flexible to extend its actions by allowing user to have more than one attributes. BeaverDam [19] is suitable for frame-by-frame box annotations. Compared to initial VATIC [18], it needs less setting up time.

# C. Task assignment

Heterogeneous task assignment means assigning different task types to different workers. There are two main steps in task assignment including worker performance evaluation and potential gain maximization. [20] Ho and Vaughan [21] proposed a task assignment strategy using online primal-dual framework. Mo et al. [22] aimed at maximizing the amount of tasks allocated within a given budget. Mavridis et al. [23] evaluated performance of workers through a distance measure between worker skills and the skills needed for tasks and then tried to distribute specialized tasks to workers with fewer skills first. Kumai et al. [24] considered the problem where single task could be assigned to a group of workers. Shi et al. [25] propose a bayesian probabilistic model named Gaussian Latent Topic Model(GLTM) to mine the latent topics of numerical tasks based on workers’ behaviors and to estimate workers’ topic-level reliability. In this scenario, they proposed three strategy to group workers considering skill balance and worker re-assignments.

![](images/7fec1a1edac6b18e84343ed11dccdcd49074562b77abd12023d998319c19b2e3.jpg)



Fig. 2. Our overall annotation process. The part of tasks discovery is described in sectionIII-C, and the part of tasks assignment is in III-D.

# III. METHOD

We adopt [26] as an inspiration for our method. This work presents a semi-automatic solution for fast moving object annotation. The target tracking annotation task is divided into several subtasks and a rule-based decision fusion scheme is used to automatically generate annotations in the case of manually generated annotation results. However, this work does not consider multi-target scenarios and does not support customization of additional tasks.

Here we divide a video annotation task into several subtasks, such as object centroids C, bounding boxes B, trajectories T and additional customization sub-tasks A.

# A. Workers definition

There are n workers $U = \{ u _ { 1 } , u _ { 2 } , \cdots , u _ { n } \}$ for annotation tasks. Let $u _ { i } = [ u _ { i c } , u _ { i t } , u _ { i b } , u _ { i a } ]$ represents the abilities of the ith worker. $u _ { i c }$ represents the ability of the ith worker to generate object centroids. In the same way, $u _ { i t } , u _ { i b }$ and $u _ { i a }$ represent the abilities of the ith worker to generate bounding boxes, trajectories and additional results.

Subtasks are delivered in batches, and workers are assigned subtasks in each epoch. It should be noted that workers should be assigned to golden tasks sometimes to determine their abilities for the tasks. Golden tasks are tasks that already have a completely correct answer and are usually given to the annotator to complete at the beginning of the annotation process, and the annotator’s ability is evaluated by the completion of the annotation. It is difficult to determine the abilities of workers with a small number of golden tasks alone, and

TABLE I SYMBOL NOTATIONS 

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td>D</td><td>Raw data</td></tr><tr><td>U</td><td>The set of n workers</td></tr><tr><td>T</td><td>The set of customized tasks</td></tr><tr><td> $N_t$ </td><td>The number of objects in frame t</td></tr><tr><td> $S_{cid}(t)$ </td><td>Subtask of centroid at the time point t</td></tr><tr><td> $S_{bbox}(t)$ </td><td>Subtask of bounding box at the time point t</td></tr><tr><td> $S_{track}^{P}(t_1,t_2)$ </td><td>Subtask of objects P&#x27;s trajectory at the period [ $t_1,t_2$ ]</td></tr><tr><td> $S_{act}^{P}(t_1,t_2)$ </td><td>Subtask of object p&#x27;s action state at the period [ $t_1,t_2$ ]</td></tr><tr><td> $\epsilon_c$ </td><td>The ratio of centroid errors</td></tr><tr><td> $u_{ic},u_{ib},u_{it},u_{ia}$ </td><td>The ability of the ith worker</td></tr><tr><td>NGT</td><td>The set of near golden tasks</td></tr><tr><td>FV</td><td>The set of finished tasks</td></tr><tr><td>AT</td><td>The set of tasks that will be annotated</td></tr></table>

golden tasks can cause additional costs. So we can rely on models to produce near-golden tasks that are cost-free and efficient which will be explained in section III-C.

Therefore, the system will give the worker a annotation task that may involve multiple tasks. However, it is likely that the worker, while expecting to make money, doesn’t have a high quality of task answers, for example, he is more inclined to complete the quantity of tasks rather than the quality. We will assign tasks in Section III-D according to the abilities of different annotators.

# B. Tasks definition

We give each sub-task a rule to determine whether it passes or not. The ratio of successful tasks to total tasks was used to describe the ability of the worker. We represent all kinds of subtasks as $S _ { f o r m } ( t )$ , and t means the time point or period of the video. We use ByteTrack [1] as the auxiliary model.

a) Centroid: Correctly match the ID with the target to ensure that the target corresponds to the correct ID in each frame. In the process of annotation, we mainly face the following problems: (1)Id-object mix-up, object tagged with another Id; (2)The object has no id. Each subtask gives the worker a frame and asks him to match each object in the frame with the previously assigned ID. If there is a target that has not appeared before, it needs to be assigned a new ID. We take the proportion of the IDs correctly marked by the annotator to the total number of objects in the frame as a value $S _ { c i d } ( t ) \in 0 , 1$ to judge whether the subtask is successful or not:

$$
S _ {c i d} (t) = I \left\{\frac {\text { CorrectID } (t)}{N _ {t}} > 1 - \epsilon_ {c} \right\} \tag {1}
$$

$\epsilon _ { c }$ is the hyperparameter for adjusting task delivery requirements, and the same is true below. The worker’s ability is defined by the percentage of tasks he has completed:

$$
u _ {i c} = \frac {\sum_ {t = 1} ^ {T} S _ {c i d} (t)}{T} \tag {2}
$$

b) Bounding box: Correctly wrap each object in a rectangular box and make sure the edges of the object fit the edges of the rectangle. In the process of annotation, we mainly face the following problems: (1)Bounding box inconsistency, the rectangle does not fit the object; (2)Bounding box shifting, the rectangle is the same size as the object, but it is offset. We take the IoU (Intersection over Union) to judge whether the subtask is successful or not:

$$
S _ {b b o x} (t) = I \left\{I O U (t) > 1 - \epsilon_ {b} \right\} \tag {3}
$$

Note that the IoU here computes all rectangles in a frame:

$$
I o U (t) = \frac {\sum_ {n = 1} ^ {N _ {t}} B _ {n} \cap G T _ {n}}{\sum_ {n = 1} ^ {N _ {t}} B _ {n} \cup G T _ {n}} \tag {4}
$$

Just like $u _ { i c } ,$ , the worker’s ability of bounding box is defined by the percentage of tasks he has completed:

$$
u _ {i b} = \frac {\sum_ {t = 1} ^ {T} S _ {b b o x} (t)}{T} \tag {5}
$$

c) Trajectory: Make sure the object is tracked from appearance to disappearance. In the process of annotation, we mainly face the following problems: (1) The trajectory terminated early or late, while the object is still in the frame, the rectangle and Id accompanying him has disappeared; (2)The trajectory is fragmented, it doesn’t track the object continuously, which is intermittent. However, these problems can also be discovered in the stage of centroid and bounding box, provided that these frames are identified as key frames. So the subtask is focus on the trajectory of single object throughout the period $[ t _ { 1 } , t _ { 2 } ]$ . We take AOS in the period $[ t _ { 1 } , t _ { 2 } ]$ to judge whether the subtask is successful or not. AOS is the average value of overlap scares (IOU) in a period:

$$
A O S _ {P} (t _ {1}, t _ {2}) = \frac {\sum_ {t = t 1} ^ {t 2} \sum_ {p = 1} ^ {| P |} \frac {B _ {p} (t) \cap G T _ {p} (t)}{B _ {p} (t) \cup G T _ {p} (t)}}{| t _ {2} - t _ {1} |} \tag {6}
$$

$$
S _ {t r a c k} ^ {P} (t _ {1}, t _ {2}) = I \left\{A O S _ {P} (t _ {1}, t _ {2}) > 1 - \epsilon_ {t} \right\} \tag {7}
$$

$$
u _ {i t} = \frac {\sum_ {p = 1} ^ {P} S _ {t r a c k} ^ {P} (0 , T)}{P} \tag {8}
$$

d) Additional task: In addition to object tracking, there may be other forms of annotation, depending on the information required by the model. Here we use sequential action recognition as an additional task for analysis. Sequence action recognition mainly needs to annotate the start and end time of the action and the category of the action. Therefore, the key frame is the start and end time of the action, which is subjective. For example, when we annotate the class of playing phone, it can be counted from taking out the phone or looking down at the screen. Whether the task is completed is judged by whether others recognize the correct behavior state of the object when labeling some frames in the video clip. We annotate additional tasks without the participation of the existing model, and requiring the worker to manually annotate from scratch. Sequence action annotation, like trajectory, is also required to annotate entire video clips, rather than single frames like bounding box and centroid.

$$
S _ {a c t} ^ {P} (t _ {1}, t _ {2}) = I \left\{W Q _ {p} (t _ {1}, t _ {2}) > 1 - \epsilon_ {a} \right\} \tag {9}
$$

WQ (Weighted Query) is questioning with weights. We consider that the start and end times of actions are ambiguous, and the closer the start and end times are, the more likely the state will be negated by other annotators, but it does not necessarily mean that the annotation is wrong.

$$
W Q _ {P} = \sum_ {p = 1} ^ {| P |} \frac {\int_ {t _ {1}} ^ {t _ {2}} w _ {t _ {1} , t _ {2}} (t) I (\text { query } (p , t)) d t}{\int_ {t _ {1}} ^ {t _ {2}} w _ {t _ {1} , t _ {2}} (t) d t} / | P | \tag {10}
$$

Where $I ( q u e r y ( p , t ) )$ represents whether the action state of target p in the tth frame is recognized or not, and $w _ { t _ { 1 } , t _ { 2 } } ( t )$ is represented as a function that first increases and then decreases so that it remains approximately 0 at the starting position, with larger values towards the middle, such as the following two functions.

$$
w _ {t _ {1}, t _ {2}} (t) = \left\{ \begin{array}{l l} R e L U (t - t _ {1}) & \text { if } t \leq (t _ {1} + t _ {2}) / 2 \\ R e L U (t _ {2} - t) & \text { if } t > (t _ {1} + t _ {2}) / 2 \end{array} \right. \tag {11}
$$

$$
w _ {t _ {1}, t _ {2}} (t) = - (t - t _ {1}) (t - t 2) \quad i f t \in (t _ {1}, t _ {2}) \tag {12}
$$

Since all subtasks come from the same video, these subtasks are not independent of each other, but overlap with each other.

![](images/ca0a0282630712866d2431b455d28aa584c966bad1346211911ed07d982287f4.jpg)



Fig. 3. The difference between the model results and the groundtruth in time period $t _ { 0 }$ to $t _ { 1 8 } .$ The light green circle is the starting position of the object, the light red circle is the ending position of the object. The purple line segment is the time period when the action occurs, and the line is horizontal when the object moves according to the real trajectory. Some tracking error types described in Section III-B.

For example, the bounding box task is related to the trajectory task. If the frame of object p disappears or is offset in the area, it also means that the trajectory of object p also also offset.

$$
S _ {b b o x} (t _ {2}) \cap S _ {t r a c k} ^ {p} (t _ {1}, t _ {3}) \neq \varnothing \quad t _ {1} \leqslant t _ {2} \leqslant t _ {3} \tag {13}
$$

A worker’s annotation actually accomplishes two subtasks simultaneously. Based on this feature, we assign related tasks to different workers in task assignment, actually annotation and review respectively.

The system needs to analyze the degree of association of each round of tasks and use the degree of association between the current task and the completed tasks of the annotator to filter the suitable annotators. The value of association is judged by the duration of the task and the objectives involved in the task.

The correlation between tasks can be represented by the following function, $\alpha \in [ 0 , 1 ]$ :

$$
C o r r (S _ {f o r m} ^ {P _ {1}} (t _ {1}), S _ {f o r m} ^ {P _ {2}} (t _ {2})) =
$$

$$
\alpha T S (t _ {1}, t _ {2}) + (1 - \alpha) P S (P _ {1}, P _ {2}) \tag {14}
$$

$T S ( t _ { 1 } , t _ { 2 } )$ denotes temporal correlation, which indicates the degree of temporal overlap between two tasks, with increasing frame spacing between the two tasks, and decreasing similarity. Since tasks are divided into time period tasks and time frame tasks, T S has the following three cases:

$$
T S (t _ {1}, t _ {2}) = m a x \left\{1 - \frac {| t _ {1} - t _ {2} |}{f p s}, 0 \right\} \tag {15}
$$

$$
T S ([ t _ {1}, t _ {2} ], [ t _ {3}, t _ {4} ]) = \frac {\max \left\{\min \left\{t _ {2} , t _ {4} \right\} - \max \left\{t _ {1} , t _ {3} \right\} , 0 \right\}}{\max \left\{t _ {2} , t _ {4} \right\} - \min \left\{t _ {1} , t _ {3} \right\}} \tag {16}
$$

$$
T S (t _ {1}, [ t _ {2}, t _ {3} ]) =
$$

$$
\frac {\max \left\{\min \left\{t _ {1} + f p s , t _ {3} \right\} - \max \left\{t _ {1} - f p s , t _ {2} \right\} , 0 \right\}}{\max \left\{t _ {1} + f p s , t _ {3} \right\} - \min \left\{t _ {1} - f p s , t _ {2} \right\}} \tag {17}
$$

$P S ( P _ { 1 } , P _ { 2 } )$ indicates the proportion of identical targets contained in each frame to the total number of targets appearing in the two frames:

$$
P S (P _ {1}, P _ {2}) = \frac {P _ {1} \cap P _ {2}}{P _ {1} \cup P _ {2}} \tag {18}
$$

# C. Tasks discovery

Obviously the current models can not meet the delivery of annotation tasks, but a large number of intermediate results can be produced. As fig 3, using these intermediate results can help us find divergence frames in the absence of ground truth, so we can quickly extract which frames and preiods might need to be reannotated.

<table><tr><td>frame id</td><td>object id</td><td>left x</td><td>top y</td><td>width</td><td>height</td><td>confidence</td></tr><tr><td>0</td><td>1</td><td>1102.34</td><td>482.43</td><td>209.78</td><td>297.1</td><td>0.9</td></tr><tr><td>0</td><td>2</td><td>794.12</td><td>1120.69</td><td>481.65</td><td>509.48</td><td>0.88</td></tr><tr><td>0</td><td>3</td><td>1401.55</td><td>581.64</td><td>241.9</td><td>345.51</td><td>0.87</td></tr><tr><td>0</td><td>4</td><td>1580.08</td><td>498.48</td><td>171.91</td><td>271.24</td><td>0.85</td></tr><tr><td>0</td><td>5</td><td>1209.67</td><td>772.48</td><td>305.94</td><td>452.88</td><td>0.83</td></tr><tr><td>0</td><td>6</td><td>870.85</td><td>419.65</td><td>151.92</td><td>258.03</td><td>0.82</td></tr><tr><td>0</td><td>7</td><td>16.56</td><td>783.65</td><td>178.42</td><td>404.62</td><td>0.81</td></tr><tr><td>0</td><td>8</td><td>1800.46</td><td>989.17</td><td>441.92</td><td>475.88</td><td>0.8</td></tr><tr><td>0</td><td>9</td><td>659.38</td><td>707.75</td><td>217.22</td><td>372.1</td><td>0.8</td></tr><tr><td>0</td><td>10</td><td>908.39</td><td>583.95</td><td>204.24</td><td>339.34</td><td>0.78</td></tr><tr><td>0</td><td>11</td><td>574.76</td><td>542.72</td><td>151.26</td><td>309.7</td><td>0.76</td></tr><tr><td>0</td><td>12</td><td>390</td><td>625.95</td><td>195.35</td><td>336.14</td><td>0.75</td></tr><tr><td>1</td><td>1</td><td>1101.57</td><td>482.64</td><td>209.53</td><td>296.81</td><td>0.89</td></tr><tr><td>1</td><td>2</td><td>797.24</td><td>1120</td><td>476.9</td><td>504.36</td><td>0.86</td></tr><tr><td>1</td><td>3</td><td>1401.75</td><td>581.95</td><td>241.09</td><td>344.36</td><td>0.87</td></tr><tr><td>1</td><td>4</td><td>1576.84</td><td>497.85</td><td>175.17</td><td>276.31</td><td>0.85</td></tr><tr><td>1</td><td>5</td><td>1207.22</td><td>768.33</td><td>308.24</td><td>456.7</td><td>0.84</td></tr><tr><td>1</td><td>6</td><td>872.96</td><td>420.18</td><td>147.65</td><td>250.55</td><td>0.83</td></tr><tr><td>1</td><td>7</td><td>18.62</td><td>783.67</td><td>177.02</td><td>401.38</td><td>0.79</td></tr><tr><td>1</td><td>8</td><td>1803.04</td><td>990.48</td><td>437.51</td><td>471.14</td><td>0.81</td></tr><tr><td>1</td><td>9</td><td>669.77</td><td>706.25</td><td>219</td><td>374.25</td><td>0.8</td></tr><tr><td>1</td><td>10</td><td>907.75</td><td>584.75</td><td>197.94</td><td>329.11</td><td>0.79</td></tr><tr><td>1</td><td>11</td><td>577.87</td><td>544.14</td><td>148.45</td><td>303.71</td><td>0.75</td></tr><tr><td>1</td><td>12</td><td>388.54</td><td>626</td><td>198.25</td><td>341.15</td><td>0.76</td></tr><tr><td>2</td><td>1</td><td>1101.66</td><td>483.23</td><td>208.95</td><td>296.08</td><td>0.89</td></tr><tr><td>2</td><td>2</td><td>794.84</td><td>1118.87</td><td>482.26</td><td>510.09</td><td>0.86</td></tr><tr><td>2</td><td>3</td><td>1400.69</td><td>579.85</td><td>243.53</td><td>347.97</td><td>0.87</td></tr></table>

Fig. 4. Results from ByteTrack

• New object detected: When the model detects a new object, it may be that the object that has left before reappears in the frame. ByteTrack, for example, only keeps 30 frames of the missing object. It could also be that the objects of frame t are matching the trajectory of frame t   1 incorrectly.

• The number of objects changes: The number of objects in frame t is inconsistent with the number of objects. It may be that the object leaves or reappears in the frame, or it may be that the model makes a wrong judgment and identifies other categories as objects or fails to identify the original objects.   
• The assignment cost increases rapidly: The objects $\left\{ b b o x _ { 1 } , b b o x _ { 2 } , \cdot \cdot \cdot , b b o x _ { N _ { t } } \right\}$ detected in frame t have too much cost when assigning with the trajectories $\left\{ t r a c k _ { 1 } , t r a c k _ { 2 } , \cdot \cdot \cdot , t r a c k _ { N _ { t - 1 } } \right\}$ of frame t   1. We use assignment cost matrix $\mathcal { C } _ { t } \in \dot { \mathbb { R } } ^ { \dot { N } _ { t } ^ { \prime } , N _ { t - 1 } }$ with entries

$$
c _ {t} ^ {i j} = \sqrt {(x _ {b b o x _ {i}} - \hat {x} _ {t r a c k _ {j}}) ^ {2} + (y _ {b b o x _ {i}} - \hat {y} _ {t r a c k _ {j}}) ^ {2}} \tag {19}
$$

defined by [26] representing the cost of assigning bounding box i to trajectory j at frame t is computed.

• Multiple bounding boxes overlap too much: Overlapping objects cause id confusion, and the error persists thereafter.

• Other strategies: For example, the objects detected by the model are not displayed due to low confidence, or there are conficts between workers’ annotated results.

In addition, in section III-A we have said that golden tasks defined in advance is very costly and not effective. So we can rely on the results of model inference to produce near-golden tasks, which are cost-free and efficient. The specific approach is to find the periods with little difference in model inference results, and hide some information that needs to be annotated, and give those results to the workers for re-annotating, so as to compare the differences between the model’s results and workers’ results to judge the abilities of workers. The parts with large temporal difference in model inference results were assigned to workers as annotation tasks. Therefore, the annotator still participates in the annotation of all video. At the same time, workers also determined their abilities and completed the annotation tasks.

# D. Tasks assignment

After completing the abilities assessment of the workers, we choose Kuhn-Munkres (KM) algorithm to assign workers and tasks. The KM algorithm is a $\bar { O } ( | V | ^ { 3 } )$ algorithm that can be used to find maximum-weight match in bipartite graphs. A bipartite graph can be represented by an adjacency matrix, where the weights of edges are the entries. Let the worker i be labeled $A [ i ]$ , and sub-task j be labeled $B [ j ]$ . The weight of edge between vertices worker i and sub-task j is $w [ i , j ]$ . We use the ith worker’s ability to do the corresponding sub-task j to determine the weight. In other words, if the jth sub-task is bounding box, the weight is $u _ { i b }$ .

We assume that the workers’ behavior is consistent, that is, the truth value of their hidden abilities $U = \{ u _ { 1 } , u _ { 2 } , \cdots , u _ { n } \}$ is constant. Ideally, each task should be assigned to the worker with the best ability to do it, while the task is reviewed by the person with the second best ability. In fact, annotation and review are the same job, but for different objects. The review task is to review the annotation results of workers and the annotation task is to review the inference outputs of the model. So there is no need to tell the worker whether the task he is reviewing comes from another worker or a model.

Algorithm 1 Our workflow   
Input: Raw video D, required customized tasks Form, Budget, Annotators U;
Output: Annotated video results $R_{finished}$ .
1: EstimateAbilityMatrix ← ones(|U|, |T|), i ← 0, FV ← {}; 
2: $R_{temp} = Model(D)$ ;
3: while i < epoch and Budget > 0 do
4:    NGT, AT = Discover( $R_{temp}$ , FV);
5:    for $NGT_{batch}$ , $AT_{batch}$ in each batch do
6:    Calculate the abilities of each annotator for each task A from EstimateAbilityMatrix;
7:    M ← AssociateTaskAssign( $NGT_{batch}$ , $AT_{batch}$ )
8:    Budget, EstimateAbilityMatrix, $R_{temp}$ = WorkerAnnotate(EstimateAbilityMatrix, M)
9:    FV = FV ∪ $\{NGT_{batch}, AT_{batch}\}$ 10:    end for
11:    i ← i + 1
12: end while
13: return $R_{finished} = R_{temp}$

# IV. EXPERIMENTS

We implemented the proposed video annotation method and conduct some experiments on two self-collected human behavior datasets and the publicly available dataset MOT. Our self-collected dataset consists of two scenarios (classroom and office) by Hikvision cameras with the resolution of 1920 1080. The example of our surveillance dataset is shown in figure.5

MOT (Multiple Object Tracking) is a series of datasets specifically designed for multi-object tracking. It contains MOT17, MOT20 and so on. The MOT17 training set contains 15948 frames with 1638 object trajectories. There are 336891 bounding boxes in total.

In this section, we have done the simulation experiments, so as to get the results of our method on the real dataset. Our experiment is divided into two parts, one is task discovery module, the other is task assignment module.

# A. Experimental Setup

Since it is a simulation experiment, we do not have enough workers to annotate all datasets. Therefore, we randomly generate the abilities value of workers, and approach it with multiple annotation results. The ability of each workers is initialized by $u _ { i } = [ 1 , 1 , 1 , 1 ]$ . If the values set too low, such as 0.5, the algorithm will find a value above 0.5 and keep assigning the tasks to the worker while ignoring other abilities of him. Near golden tasks were used to estimate the abilities of workers, and the effectiveness of our tasks assignments was judged by the expectation number of success tasks.

![](images/f4d76fa0c5e832a4ca2a21b8db89f164fbd8e629bd11c15b953601e3db707d18.jpg)



(a) Classroom

![](images/23943e2e8c0ba7742acda39bd0f85489eb52ec83186e8165c88b097689b477fb.jpg)



(b) Office   
Fig. 5. Example of our surveillance dataset

TABLE II NUMBER OF DIVERGENT FRAMES WITH CHANGING NUMBER OF IDS 

<table><tr><td>fps</td><td>5</td><td>15</td><td>20</td><td>25</td></tr><tr><td>YOLOV5+DeepSORT</td><td>47</td><td>30</td><td>24</td><td>19</td></tr><tr><td>YOLOX+ByteTrack</td><td>33</td><td>21</td><td>21</td><td>16</td></tr></table>

TABLE III TASK DISCOVERY RESULTS IN CLASSROOM BY YOLOX+BYTETRACK 

<table><tr><td>Subtasks</td><td>NGT</td><td>Errors rate</td><td>AT</td><td>Errors rate</td></tr><tr><td>Bounding box</td><td>216</td><td>2.8%</td><td>43</td><td>93%</td></tr><tr><td>Centroid</td><td>75</td><td>2.7%</td><td>17</td><td>82.3%</td></tr><tr><td>Trajectory</td><td>47</td><td>14.9%</td><td>79</td><td>96.2%</td></tr></table>

TABLE IV TASK DISCOVERY RESULTS IN OFFICE BY YOLOX+BYTETRACK 

<table><tr><td>Subtasks</td><td>NGT</td><td>Errors rate</td><td>AT</td><td>Errors rate</td></tr><tr><td>Bounding box</td><td>102</td><td>6.86%</td><td>51</td><td>92.2%</td></tr><tr><td>Centroid</td><td>57</td><td>12.28%</td><td>7</td><td>100%</td></tr><tr><td>Trajectory</td><td>32</td><td>12.9%</td><td>79</td><td>96.2%</td></tr></table>

# B. Performance of our algorithm

Through the discovery task approach described in the previous section, we did a correlation analysis of the model inference results.

From Table.II for different fps, we find that the number of divergent frames for the ID variation increases with the fps decreases gradually. In practical scenarios, due to bandwidth and latency requirements, it is often necessary to run models at low fps. Many data annotation methods also annotate low frame rate data to save annotation cost. However, annotating high fps images allows us to customize the frame rate and expand the scope of data usage.This is why we use a frame rate of 25 fps. Therefore, in this paper, we mainly use the surveillance video data with fps of 25.

![](images/1b5c9aff8e2893f88cbad04151c37d5c0db8a08ed77b494d16e5159fab9efdd5.jpg)



(a) Match cost per frame

![](images/cb212932b8d6696805f67d646ed7205c0fd678a08209331f3abc7ebd28da4196.jpg)



(b) IoU per frame   
Fig. 6. The distribution of match cost and IoU per frame in the 80-second office data

Figure.6 shows the distribution of match cost and IoU per frame in the 80-second office data, with the track before and after frames track and target match cost in a perfectly correct video should appear in an approximately smooth form, while Our experiments show that the match cist is unstable even in surveillance video with a frame rate of 25 fps. The number of labeled tasks can be selected according to the sensitivity requirements of the task. In addition, the IoU per frame is also an import aspect of concern, as high IoU or sudden changes in consecutive frames are where errors can occur. The region of sudden IoU changes in Figure.6(b) and the wave area in Figure.6(a) have overlap periods.

Table III,IV and VI show the performance of the task discovery methods on the corresponding datasets. The statistics the actual error rates of the generated near-golden tasks versus the labeled tasks are presented. NGT and AT are extracted by using the tasks discovery method described in section III-C. It can be seen that the error rate of extracted NGT is significantly lower than AT. The high error rate of AT and the high accuracy rate of NGT prove the effectiveness of our task discovery method.

The annotators $U = \{ u _ { 1 } , \cdots , u _ { 1 0 } \}$ obtains the annotation task V by analyzing the model inference results through the task discovery method. We randomly select U tasks per batch to be given to the annotator for annotation, and after assigning the same near golden task to calculate the annotator capability value, we use the above three methods to assign the annotation tasks and calculate the similarity of the tasks assigned to each annotator.

Due to the memory capacity of the annotators, it is not fair to use the same videos for the experiment, so we selected a randomly intercepted office video in which three nonoverlapping video clips were randomly selected for labeling Note. The specific information is shown in TableVII.

From TableVII, it can be seen that the tasks assigned to each annotator still have a high relevance at random assignment. Each number in the table is the average relevance of the tasks assigned to the annotators.

Note that $\alpha \ = \ 0 . 7 .$ , because the set of people has no major changes in the office video, the objects’ bounding box overlap is very high, so we mainly focus on the temporal correlation. The similarity of unrelated task assignments is high, because according to the ability of the labeled personnel, each time they are assigned the same nature of work, there is a greater correlation between them. And the association task assignment proposed in this paper enables annotators to avoid being assigned to tasks with high association with the annotated tasks.

TABLE V RELEN 

<table><tr><td>Method</td><td> $u_1$ </td><td> $u_2$ </td><td> $u_3$ </td><td> $u_4$ </td><td> $u_5$ </td><td> $u_6$ </td><td> $u_7$ </td><td> $u_8$ </td><td> $u_9$ </td><td> $u_{10}$ </td></tr><tr><td>Random</td><td>0.433</td><td>0.557</td><td>0.349</td><td>0.640</td><td>0.463</td><td>0.593</td><td>0.495</td><td>0.527</td><td>0.396</td><td>0.320</td></tr><tr><td>Independent assign</td><td>0.725</td><td>0.733</td><td>0.511</td><td>0.567</td><td>0.437</td><td>0.613</td><td>0.673</td><td>0.794</td><td>0.752</td><td>0.764</td></tr><tr><td>Dependent assign</td><td>0.477</td><td>0.361</td><td>0.429</td><td>0.281</td><td>0.291</td><td>0.213</td><td>0.238</td><td>0.411</td><td>0.390</td><td>0.457</td></tr></table>

TABLE VI TASK DISCOVERY RESULTS IN MOT17 BY YOLOX+BYTETRACK 

<table><tr><td>Subtasks</td><td>NGT</td><td>Errors rate</td><td>AT</td><td>Errors rate</td></tr><tr><td>Bounding box</td><td>77</td><td>7.8%</td><td>172</td><td>95.9%</td></tr><tr><td>Centroid</td><td>26</td><td>11.5%</td><td>105</td><td>82.7%</td></tr><tr><td>Trajectory</td><td>18</td><td>11.1%</td><td>103</td><td>90.3%</td></tr></table>

TABLE VII THE INFORMATION OF UNLABELED VIDEO 

<table><tr><td>Video</td><td>Duration</td><td>fps</td><td>|V|</td><td>Method</td></tr><tr><td>Office1</td><td>240</td><td>25</td><td>141</td><td>Random</td></tr><tr><td>Office2</td><td>231</td><td>25</td><td>105</td><td>Independent Assign</td></tr><tr><td>Office3</td><td>257</td><td>25</td><td>173</td><td>Dependent Assign</td></tr></table>

Due to the correlation between the assigned tasks, we use the last time the information of each target was modified after TableVIII shows the annotation error rate, and it should be noted that the tasks assigned here are the results of multiple rounds of discovery. The final annotation results after task discovery.

# V. CONCLUSION

In this paper, we design a multi-object annotation system for customizable tasks of surveillance video. This work is used to server surveillance video analysis in AIoT. We take advantage of the correlation of time and objects in the video data to assign related tasks to different workers, so as to achieve the purpose of mutual review. Our customization tasks are suitable for both semi-automatic annotation and purely manual annotation. Experiments show that our method is better than the methods that do not consider inter-task relevance without knowing the workers’ true ability. This paper achieves a crowdsourced multi-object annotation process through a collaborative approach in which annotators work together to achieve the goals of saving tagging time, labor costs, and reduce or replace the work of reviewers.

TABLE VIII ERROR RATE STATISTICS OF ANNOTATION RESULTS 

<table><tr><td>Subtasks</td><td>Random</td><td>Independent Assign</td><td>Dependent Assign</td></tr><tr><td>Bounding box</td><td>12.7%</td><td>7.9%</td><td>6.7%</td></tr><tr><td>Centroid</td><td>0%</td><td>5.0%</td><td>3.3%</td></tr><tr><td>Trajectory</td><td>5.3%</td><td>7.2%</td><td>2.4%</td></tr><tr><td>Action</td><td>4.3%</td><td>2.3%</td><td>2.7%</td></tr></table>

# VI. ACKNOWLEDGMENT

The research is partially supported by National Key RD Program of China 2018YFB0803400 National Key RD Program of China under Grant No. 2021ZD0110400 , China National Natural Science Foundation with No. 62132018 , Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002The University Synergy Innovation Program of Anhui Province with No. GXXT-2019-024.

# REFERENCES

[1] Y. Zhang, P. Sun, Y. Jiang, D. Yu, Z. Yuan, P. Luo, W. Liu, and X. Wang, “Bytetrack: Multi-object tracking by associating every detection box,” arXiv preprint arXiv:2110.06864, 2021.   
[2] Y. Du, Y. Song, B. Yang, and Y. Zhao, “Strongsort: Make deepsort great again,” 02 2022.   
[3] J. Cao, X. Weng, R. Khirodkar, J. Pang, and K. Kitani, “Observationcentric sort: Rethinking sort for robust multi-object tracking,” 2022. [Online]. Available: https://arxiv.org/abs/2203.14360   
[4] G. Ciaparrone, F. Luque Sanchez, S. Tabik, L. Troiano, R. Tagliaferri, ´ and F. Herrera, “Deep learning in video multi-object tracking: A survey,” Neurocomputing, vol. 381, p. 61–88, Mar 2020. [Online]. Available: http://dx.doi.org/10.1016/j.neucom.2019.11.023   
[5] S. Ren, K. He, R. Girshick, and J. Sun, “Faster r-cnn: Towards real-time object detection with region proposal networks,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 39, no. 6, pp. 1137– 1149, 2017.   
[6] W. Liu, D. Anguelov, D. Erhan, C. Szegedy, S. E. Reed, C. Fu, and A. C. Berg, “SSD: single shot multibox detector,” CoRR, vol. abs/1512.02325, 2015. [Online]. Available: http://arxiv.org/abs/1512.02325   
[7] J. Redmon and A. Farhadi, “Yolo9000: Better, faster, stronger,” in 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 6517–6525.   
[8] ——, “Yolov3: An incremental improvement,” arXiv preprint arXiv:1804.02767, 2018.   
[9] F. Yu, W. Li, Q. Li, Y. Liu, X. Shi, and J. Yan, “POI: multiple object tracking with high performance detection and appearance feature,” CoRR, vol. abs/1610.06136, 2016. [Online]. Available: http://arxiv.org/abs/1610.06136   
[10] L. Wang, N. T. Pham, T.-T. Ng, G. Wang, K. L. Chan, and K. Leman, “Learning deep features for multiple object tracking by using a multitask learning strategy,” in International Conference on Image Processing, 2014.

[11] A. Milan, S. H. Rezatofighi, A. R. Dick, K. Schindler, and I. D. Reid, “Online multi-target tracking using recurrent neural networks,” CoRR, vol. abs/1604.03635, 2016. [Online]. Available: http://arxiv.org/abs/1604.03635   
[12] J. Zhu, H. Yang, N. Liu, M. Kim, W. Zhang, and M.-H. Yang, “Online multi-object tracking with dual matching attention networks,” in Computer Vision – ECCV 2018, V. Ferrari, M. Hebert, C. Sminchisescu, and Y. Weiss, Eds. Cham: Springer International Publishing, 2018, pp. 379–396.   
[13] C. Ma, C. Yang, F. Yang, Y. Zhuang, Z. Zhang, H. Jia, and X. Xie, “Trajectory factory: Tracklet cleaving and re-connection by deep siamese bigru for multiple object tracking,” in 2018 IEEE International Conference on Multimedia and Expo (ICME), 2018, pp. 1–6.   
[14] H. Kieritz, W. Hubner, and M. Arens, “Joint detection and online multiobject tracking,” in 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2018.   
[15] E. Gaur, V. Saxena, and S. K. Singh, “Video annotation tools: A review,” in 2018 International Conference on Advances in Computing, Communication Control and Networking (ICACCCN), 2018.   
[16] S. Bianco, G. Ciocca, P. Napoletano, and R. Schettini, “An interactive tool for manual, semi-automatic and automatic video annotation,” Computer Vision and Image Understanding, vol. 131, pp. 88–99, 2015, special section: Large Scale Data-Driven Evaluation in Computer Vision. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S1077314214001544   
[17] T. A. Biresaw, T. Nawaz, J. Ferryman, and A. I. Dell, “Vitbat: Video tracking and behavior annotation tool,” in 2016 13th IEEE International Conference on Advanced Video and Signal Based Surveillance (AVSS), 2016, pp. 295–301.   
[18] C. Vondrick, D. Patterson, and D. Ramanan, “Efficiently scaling up crowdsourced video annotation,” Int. J. Comput. Vision, vol. 101, no. 1, p. 184–204, jan 2013. [Online]. Available: https://doi.org/10.1007/s11263-012-0564-1   
[19] A. Shen, “Beaverdam: Video annotation tool for computer vision training labels,” Master’s thesis, EECS Department, University of California, Berkeley, Dec 2016. [Online]. Available: http://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-193.html   
[20] D. Hettiachchi, V. Kostakos, and J. Goncalves, “A survey on task assignment in crowdsourcing,” ACM Comput. Surv., vol. 55, no. 3, feb 2022. [Online]. Available: https://doi.org/10.1145/3494522   
[21] C.-J. Ho and J. W. Vaughan, “Online task assignment in crowdsourcing markets,” in Proceedings of the Twenty-Sixth AAAI Conference on Artificial Intelligence, ser. AAAI’12. AAAI Press, 2012, p. 45–51.   
[22] K. Mo, E. Zhong, and Q. Yang, “Cross-task crowdsourcing,” in Proceedings of the 19th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, ser. KDD ’13. New York, NY, USA: Association for Computing Machinery, 2013, p. 677–685. [Online]. Available: https://doi.org/10.1145/2487575.2487593   
[23] P. Mavridis, D. Gross-Amblard, and Z. Miklos, “Using hierarchical skills ´ for optimized task assignment in knowledge-intensive crowdsourcing,” in Proceedings of the 25th International Conference on World Wide Web. Republic and Canton of Geneva, CHE: International World Wide Web Conferences Steering Committee, 2016, p. 843–853. [Online]. Available: https://doi.org/10.1145/2872427.2883070   
[24] K. Kumai, M. Matsubara, Y. Shiraishi, D. Wakatsuki, J. Zhang, T. Shionome, H. Kitagawa, and A. Morishima, “Skill-and-stress-aware assignment of crowd-worker groups to task streams,” in Sixth AAAI Conference on Human Computation and Crowdsourcing, 2018.   
[25] Z. Shi, S. Jiang, L. Zhang, Y. Du, and X.-Y. Li, “Crowdsourcing system for numerical tasks based on latent topic aware worker reliability,” in IEEE INFOCOM 2021 - IEEE Conference on Computer Communications, 2021, pp. 1–10.   
[26] N. M. AL-Shakarji, E. Ufuktepe, F. Bunyak, H. Aliakbarpour, G. Seetharaman, and K. Palaniappan, “Semi-automatic system for rapid annotation of moving objects in surveillance videos using deep detection and multi-object tracking techniques,” in 2020 IEEE Applied Imagery Pattern Recognition Workshop (AIPR), 2020, pp. 1–6.