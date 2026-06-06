# Collaborative Deep Sensing by Dynamically Fusing Multiple Models

1 $^{st}$ Mengjing Liu

University of Science and Technology of China

Hefei, China

lmj123@mail.ustc.edu.cn

$2^{nd}$ Lan Zhang

University of Science and Technology of China

Hefei, China

zhanglan@ustc.edu.cn

$3^{rd}$ Daren Zheng

University of Science and Technology of China

Hefei, China

zdr123@mail.ustc.edu.cn

$4^{th}$ Xiangyang Li

University of Science and Technology of China

Hefei, China

xiangyangli@ustc.edu.cn

Abstract—Smart activity sensing has gained more and more attention with the development of sensing devices and recognition techniques. For multi-modal sensing scenarios like smart home, fusing results of multiple models brings opportunities to achieve more comprehensive and accurate recognition, as well as challenges to coordinate a collection of models under strict resource limitations. In this paper, we firstly model the multi-modal sensing problem with strict orthogonal resource constraints. Then, for scenarios with fixed and changeable resource limitations, we propose two online decision methods correspondingly to optimize recognition accuracy through dynamically selecting models and fusing their predictions, given a pre-trained model library. Specifically, by utilizing reward feedback based on an actor-critic scheme, we deal with fixed resources and accuracy optimization in one shot. Furthermore, for changeable resources, we decouple resource allocation and model evaluation to support model portability with comparable accuracy. Three types of sensing devices and nine recognition models have been investigated in our work. Experiments show that our method improves the recognition accuracy compared to that achieved by a single-modality model, and also achieves higher accuracy with less resource costs compared to the end-to-end multi-modal model.

Index Terms—Multi-modal Sensing, Human Action Recognition, Resource Constraints

# I. INTRODUCTION

Smart sensing is increasingly important in various scenarios fueled by the rapid development and wide adoption of smart sensing devices. In plentiful applications, such as smart home, human activity sensing is a fundamental but persistent hot problem. Recent studies have demonstrated a promising performance improvement by fusing predictions from multiple models $[1]$ . Meanwhile, most sensing applications requiring real time responses with limited computation resources also raise challenges for the adoption of multiple models $[2]$ .

With wearable [2] and non-intrusive [3] devices, existing works in the multi-modal sensing area can be divided into two categories: 1) accuracy targeted and 2) trade-off between accuracy and resource expenditure. The former focuses on improving the sensing accuracy under the assumption of sufficient computation resources. [4] investigates fusion at different stages of network and shows that late and hybrid fusion techniques are superior compared to early fusion techniques. [5] proposes a deep learning architecture with concatenated sensor streams input, which performs better compared to shallow classifiers, such as random forest and SVM. The latter takes resource constraints into account, like device occupation, energy consumption, etc. [6] presents a flexible selection of feature groups that allows the designer to choose an appropriate accuracy-energy trade-off for a specific target application, using wearable accelerometers. [7] shows that by adaptively choosing the appropriate sensor from device-free ultrasonic sensors and cameras, for the context, they can achieve up to 90% reduction in energy while maintaining comparable performance compared to a single sensor system. Possas et al. [8] develop a reinforcement learning model-free method to learn energy-aware policies with sensor and video data, which maximize the use of low-energy cost predictors with comparable accuracy.

Generally, for multi-modal human activity sensing, it is prospective to combine multiple models intelligently to improve recognition accuracy. However, in the works mentioned above, they only consider energy consumption qualitatively and ignore more strictly quantified resource constraints, like memory occupation and computation time delay. Besides, most existing works optimize the energy usage with subjectively good-enough accuracy. Moreover, in each work, only two models or two modalities have been investigated.

To fill the gap, in this paper, we take accuracy optimization as the target and consider strictly quantified resource constraints, with extended modalities and model number. Given a model library, we propose to optimize the recognition accuracy through online adaptively selecting and fusing multiple models with resource constraints. Within constraints, more modalities and models bring new opportunities to optimize accuracy, as well as challenges:

\- For online activity recognition, data is changing dynamically and difficult to forecast. It's knotty to quantify which model is helpful and which not for online dynamical data.

- With strict orthogonal resource constraints, it is difficult to select models which can recognize data correctly without exceeding resource limitations.   
- When the resource constraints are changeable, the online decision method is required to be transferable.

Facing these challenges, we firstly propose an online decision method to dynamically select models and decide their fusion weights. In order to handle the conflicts between resource limitations and accuracy optimization, we design a reward feedback mechanism with customized hyper parameters to update the online decision method. Furthermore, to support the portability of the method when resource limitations change, we design a transferable two step model selection method with comparable accuracy.

Our Frameworks are shown in Fig. 1, Fig. 2.

![](images/1fe0c6d67024a7fab4952e04521195048f4354e2bc74c2f86eac98f12b2de2c5.jpg)



Fig. 1: The one-shot actor-critic based online decision framework

![](images/ce33332652f7726b6e25077173cff4360ffa326c65a4ed9ba405cc41f9bde8ad.jpg)



Fig. 2: The two-step stacking based online decision framework.

Specifically, we make the following contributions:

- We model the resource constraints as an orthogonal rectangle knapsack problem and solve it by an approximate algorithm.   
- For fixed and changeable resources, we propose two frameworks to select and fuse models in model library for online data, respectively. An actor-critic based framework is proposed for fixed resources and updated by a novel reward function. And a stacking based framework is designed for changeable resources, which decouples the online model evaluation and resource allocation to support the portability of the method, with comparable performance.

\- Experiments show the effectiveness of our methods. Compared to single modality models, we achieve signif-

icant accuracy improvement. Compared to multi-modal end-to-end models, we also achieve higher accuracy, with lower resource consumption.

The rest of the paper is organized as follows. Related work is introduces in section II. Afterwards, in section III, we will give our problem definition in formulation. In section IV and section V, we will introduce our methods followed with the implementation and evaluation of our algorithm in section VI. Finally, we conclude our work in section V and list the references.

# II. RELATED WORK

# A. MULTI-MODAL SENSING

Works using multi-modal sensing to improve human activity recognition accuracy have been carried out recent years. Chen et al. [4] investigated fusion at different stages of network and showed that late and hybrid fusion techniques were superior compared to early fusion techniques. [5] proposed a deep learning architecture with concatenated sensor streams input, which performed better compared to shallow classifiers, such as random forest and SVM. In [9], they introduced a Sparsely-Gated Mixture-of-Experts layer (MoE), where a trainable gating network was designed to determine the sparse combination of these experts. [10] fused RGB and skeleton using their complementarity for action recognition. They enabled skeleton feature to guide on RGB feature, so that the important RGB information strongly related to the action was enhanced. [11] proposed different data augmentation and representation methods to handle RGB videos, skeleton stream and inertial sensor data and combined the three heterogeneous networks with a variety fusion methods. They achieved 4% higher accuracy than using each modality individually. [12] encoded multivariate signal sequences in an image and then classified them using an efficient CNN architecture, which improved the UTD-MHAD inertial baseline by +14.4%, the UTD-MHAD skeleton baseline by 1.13%. Those works mainly focus on improving accuracy under the assumption of sufficient computation resources.

# B. RESOURCE CONSTRAINTS

Human activity sensing works focus on resource constraints mainly in two aspects: time cost and energy consumption. [3] presented a real-time human activity recognition system based on video cameras via extracting body point features and training hidden Markov models. Their system operated at one frame per second. [13] developed a vision-based system that utilized a combined RGB and depth descriptor to classify hand gestures, where the feature extraction approximately takes 3 milliseconds for one frame. Other works take energy consumption into account. [6] presented a flexible selection of feature groups that allowed the designer to choose an appropriate accuracy-energy trade-off for a specific target application, using wearable accelerometers. [7] showed that by adaptively choosing the appropriate sensor from device-free ultrasonic sensors and cameras, for the context, they could achieve up to $90\%$ reduction in energy while maintaining comparable performance to a single sensor system. However, they only considered energy consumption qualitatively and ignored more strictly quantified resource constraints, like memory occupation and computation time delay.

# C. ONLINE DECISON

Traditional online decision method gives priority to multi-armed bandit problem(MAB). In the decision making process, agents make decisions based on observations of the world. The agent needs to make a sequence of decisions at time 1, 2, ..., T. At each time slot, given a set of k arms, the agent selects which arm to pull. Reward of the selected arm if obtained after pulling the arm, while rewards of other arms are unknown [14]. Extensions of MAB include contextual MAB, combinatorial MAB, cascading MAB and so on [15] [16] [17]. In our situation, the models or arms are fixed and data are dynamical, the combinatorial MAB in [16] is not suitable. In RL methods, the decision problem is modeled as a Markov process with states transitions. The agent observes state and makes decisions based on the current state. After interacting with environment by taking the actions, reward and next state are obtained and used to update the agent. RL based online decision methods are divided into two kinds: "1) value-based 2) policy-based". Extensions of RL include deep deterministic policy scheme [18], actor-critic [19], asynchronous advantage actor-critic [8], etc. Among them, deep Q learning can only deal with discrete action spaces, and actor-critic based methods can deal with continuous action spaces. [20] selected models and recognized image data for multiple times sequentially based on reinforcement learning. While in our work, each data will be recognized only once and models are selected by one shot.

# III. PROBLEM DEFINITION

In this section, we define the problem more formally. Before giving the definition, we firstly illustrate an elderly nursing scenario. Consider an old man living in a smart home equipped with multiple sensing devices, including smart phone, RFID and voice recorder, which collect time series sensing data of different modalities. By recognizing the man's actions within a short time delay, we can provide necessary help to the old man in time. Nevertheless, it's not feasible to deploy heavyweight models on mobile devices directly because of their resource limitations. Fortunately, by dynamically fusing pre-trained lightweight models with different properties, the effective action recognition under limited resource and time delay can be achieved.

Such a human activity recognition problem can be defined by a tuple $< M, X, A, R, P>$ , with:

- M: Set of modalities, including wireless radio frequency modality(RF), acoustical recording modality, and accelerator sensing modality.   
- $X$ : Set of sensing data $X = \{x_i, y_i\}_n$ . $x_i = (x_i^1, x_i^2, x_i^3)$ is the sensing segment of time $i$ , where $x_i^1, x_i^2, x_i^3$ are data of modality $M$ respectively. $y_i$ is the label of $x_i$ .

- $A$ : Set of pre-trained models $\{a_1, a_2, ..., a_m\}$ , where $a_i$ is a model with properties $(o_i, t_i)$ :   
$o_{i}$ : memory occupation of model $a_{i}$ . $o_{i} > 0$   
$t_{i}$ : time consumption of model $a_{i}$ for one recognition. $t_{i} > 0$ . We concentrate on time consumption in online phase. Time consumption of offline data preprocessing and model training is not considered.

\- $R$ : Resource constraint $R := (O, T)$ , where

O: the maximum memory limitation,

T: the maximum time delay limitation.

\- $P$ : Model selection and fusion policy. $P = (w_1, w_2, ..., w_m)$ , $w_i \in [0, 1]$ is the weight assigned to each model in $A$ . $w_i = 0$ means the model $a_i$ is not selected hence it will not be ran or allocated resources. $w_i > 0$ means the model is selected and will occupy memory and cost time. In the meanwhile, $w_i$ is the weight of model $a_i$ during model fusion.

We model the multi-modal sensing problem with resource constraints as a two-dimensional rectangle packing problem[21] as in Fig. 1. Each model is represented by a rectangle, of which the width is memory occupation and the height is time delay. The resource constraints $(O,T)$ is treated as a box where $O,T$ are the width and height of it, respectively. Our target is to maximize the prediction accuracy of policy $P$ , with the selected rectangles packed into the box without overlaps or rotations.

# IV. ACTOR-CRITIC BASED ONLINE DECISION METHOD

For each input sample, our expected output policy is a continuous multidimensional weight vector $P = (w_{1}, w_{2}, ..., w_{m})$ , where $w_{i} \in [0, 1]$ . On the one hand, the policy should satisfy constraints of time delay and memory occupation. The conflict between orthogonal resource constraints and accuracy optimization makes it difficult to find an acceptable policy. On the other hand, any policies that can satisfy these two constraints as well as obtain the correct prediction result are acceptable. Thus, the label of the policy is unattainable and not exclusive. So we handle the problem with an online decision method based on actor-critic in this section.

Generally, an online learning method is designed and optimized with afterward feedback. And the policy is adapted to the real time input to achieve accurate prediction. The overview of this method is shown in Fig. 1. State $s_i$ is extracted to represent multi-modal sensing data $x_i$ . Then we design an actor-critic scheme to get action $w_i$ , indicating which models to select and how to fuse their predictions. The actor-critic scheme is composed of two sub-networks, an actor network and a critic network. The actor network provides model selection $w_i$ referred to state $s_i$ . And the critic network evaluates the actor's output with a value $q_i$ , referred to $s_i$ and $w_i$ . The actor network's object is to get action with higher value $q_i$ . So we set the actor network's loss as the opposite number of the mean of estimated values from critic network. As for critic network, we choose the mean squared error of observed reward $r_i$ and estimated value $q_i$ as the loss, where $r_i$ is the reward obtained from environment after taking action $w_{i}$ . Specifically, we run models in model library referred to $w_{i}$ and get their predictions, which are fused by weighted average with weights $w_{i}$ to get final prediction. We inspect whether the models can be packed into the resource limitations and whether the final prediction is correct to obtain the reward $r_{i}$ . And reward is in return used to update actor-critic scheme. These designs are introduced in following subsections in detail.

# A. STATE

To preserve sufficient information to introduce the online decision, we define the state with three parts: RF signal, voice signal, and accelerator signal.

$$
s _ {i} = \left(s _ {r i}, s _ {v i}, s _ {a i}\right) \tag {1}
$$

Considering the time series data and contextual correlated samples, we use LSTM[22] in actor network to extract features from multiple sensing data streams. However, the sample rates of various raw sensing data are extremely high and quite different, which may lead to gradient vanishing of LSTM and unacceptable time and memory consumption. To avoid gradient vanishing and enable our method to work within strict consumption constraints, we design the data preprocessing with down sampling to fix sample amount of all modalities per second. The details of the data preprocessing are shown in Fig. 3.

![](images/9ce1ddce4eb830da64444bcc5aebfd0bb38b43b9c4550477f63815ea9a084600.jpg)



Fig. 3: The preprocessing of multi-modal sensing data. The sample rates of RF, acoustical data and accelerator data are 44100, 100, 20 samples per second, respectively. For the segments of all modalities, we firstly down sample the raw data to 20 samples per second. Then we padding the segments of different lengths to 160 samples and concatenate the segments of three modalities to get the multi-modal sensing stream.

Since some actions may not generate sound, we handle acoustical signals specially. When the max amplitude of an acoustical segment is less than a threshold $v_{min}$ , we assume the action in this segment didn't generate sound. So we use zero-padding as acoustical data to eliminate the noises' influence. Otherwise, we use LSTM to extract features from acoustical signal.

$$
s _ {v i} = \left\{ \begin{array}{l l} s _ {v i} & \max (x _ {i} ^ {2}) > v _ {\text { min }} \\ \mathbf {0} & \text { otherwise } \end{array} \right. \tag {2}
$$

# B. ACTION

From the last activation layer of actor network, we acquire $\mu = (\mu_{1}, \mu_{2}, ..., \mu_{m})$ , where $\mu_{i} \in [0, 1]$ . $\mu_{i}$ is a continuous value indicating the preference of model i. Considering the resource limitations, models with lower preferences are rejected. We get action w from $\mu$ , indicating which models to run and how to fuse their results. w is generated by:

$$
\forall i, w _ {i} (s) = \left\{ \begin{array}{l l} \mu_ {i} & \mu_ {i} (x) > = \sigma \\ 0 & \mu_ {i} (x) <   \sigma \end{array} \right. \tag {3}
$$

$\sigma$ is a threshold in [0, 1]. $w_{i}$ equals to zero means model $m_{i}$ is not selected and will not join in the prediction and decision fusion procedures. $w_{i}$ larger than 0 means $m_{i}$ is selected, so that the demanding memory and time should be satisfied. And $w_{i}$ is designed as the weight of $m_{i}$ 's prediction in decision fusion.

# C. REWARD

Reward is significant in actor-critic scheme. It's used to update the actor network and critic network. Negative reward are assigned when the models selected by $w$ can not be scheduled within resource limitations or can not recognize data correctly. On the contrary, positive rewards are assigned.

For each selected model $a_{i}(w_{i}>0)$ , denote its prediction as $p_{i}=(p_{i}^{1},p_{i}^{2},...,p_{i}^{j})$ . We fuse their predictions referring to w with weighted average. The fusion result re:

$$
r e = \underset {j} {\arg \max} \sum_ {i} w _ {i} \cdot p _ {i} \tag {4}
$$

Denote whether the models can be scheduled within resource limitations by $\tilde{r}e$ :

$$
\tilde {r e} = \left\{ \begin{array}{l l} t r u e & r e = y \\ f a l s e & r e \neq y \end{array} \right. \tag {5}
$$

We utilize Steinberg's theorem [23] as a sufficient condition to judge whether the models can be scheduled within resource limitations. $\tilde{r}s$ is true if the condition in Steinberg's theory is satisfied, otherwise is false.

Theorem 1 (Steinberg's Theorem): For models with $w_{i} > 0$ , denoted as $\tilde{M}$ , if the following inequalities hold,

$o_{L} \leq O, t_{L} \leq T$ , and $2S_{L} \leq OT - (2o_{L} - O)_{+}(2t_{L} - T)_{+}$ , then it is possible to pack the models in to orthogonal resource constraints $(O, T)$ , where $o_{L} = \max_{m \in \tilde{M}} o_{m}, t_{L} = \max_{m \in \tilde{M}} t_{i}, S_{L} = \sum_{m \in \tilde{M}} o_{m} t_{m}$ , and $x_{+} = \frac{(x + |x|)}{2}$ .

According to Steinberg's theorem, reward $r$ depends on both $\tilde{r}e$ and $\tilde{r}s$ . Hyper parameters $\alpha_{1}, \alpha_{2}$ are used to quantify the influences of accuracy and resource limitations in model learning.

$$
r = \left\{ \begin{array}{l l} 1 & \tilde {r e} \wedge \tilde {r s} \\ - 1 & ! \tilde {r e} \wedge ! \tilde {r s} \\ - \alpha_ {1} & ! \tilde {r e} \wedge \tilde {r s} \\ - \alpha_ {2} & \tilde {r e} \wedge ! \tilde {r s} \end{array} \right. \tag {6}
$$

Algorithm 1 summarizes the framework.

Algorithm 1 Adaptively Select and Fuse Multiple Models Based on Actor-Critic   
Input: dataset X
Output: model selection w
1: Initialize actor, critic networks.
2: for t = 1 to T do
3:    for x ∈ X do
4:    Get state s from data x.
5:    μ ← actor(s) + noise
6:    Get action w ← piecewise(μ)
7:    q ← critic(s, w)
8:    Run models with wi > 0 and get predictions pi.
9:    Observe reward r.
10:    Store transition (s, w, r) in memory.
11:    Select bs transitions from memory randomly.
12:    actorloss ← $\frac{1}{bs} \sum_{bs} -q$ 13:    criticloss ← $\frac{1}{bs} \sum_{bs}(q - r)^{2}$ 14:    Update actor, critic using gradient descent
15:    end for
16: end for

# V. STACKING BASED ONLINE DECISION METHOD

In applications, memory and time constraints may be changeable. For instance, available memory of the device becomes smaller gradually since more applications are installed and the response delay requiring is tightened, etc. Since the actor and critic networks' parameters are resource correlated, we further propose a transferable method for changeable resource limitations. The method consists of two steps:

- Online evaluation: A sketch model is designed to evaluate the probability of each model in model library recognizing the data correctly. The input of the model is features extracted from sensing data, and output is a vector of probabilities in [0, 1].   
- Model scheduling: We select models and allocate resources through a rectangle knapsack, based on the correctness probabilities from online evaluation. The input of rectangle knapsack includes resources limitations, models' occupations, and probability vector from sketch model.

In our design, on the one hand, the sketch model is only related to the prediction results of models in the library, and is independent with resource occupations. On the other hand, the model scheduling is adaptive to changeable resource limitations. Therefore, such a design achieves the separation of resource allocation and model evaluation. The method is flexibly transferable to changeable resources. In the following, we will introduce the designs of sketch model and model scheduling in detail.

# A. ONLINE EVALUATION

To capture the temporal relation and contextually correlation of sensing data, we use LSTM to extract features from multimodal sensing data. We train a classifier consisted of three LSTM layers and a dense layer with all modality data and extract the last LSTM layer's output as features.

We pad the acoustical segments whose amplitude peaks are smaller than $v_{min}$ in the same way with equation 2.

To label the dataset, we run all models in the library to recognize data set X and get the predictions. For data $x_{i}$ , denote the prediction of model $a_{j}$ as $p_{ij}$ . So we obtain the predictions of the model library $\boldsymbol{p}_{\boldsymbol{i}} = (p_{i1}, p_{i2}, ..., p_{im})$ . Then we get the ground truth $g_{i} = (g_{i1}, g_{i2}, ..., g_{im})$ by:

$$
\forall j, g _ {i j} = \left\{ \begin{array}{l l} 1 & p _ {i j} = = y _ {i} \\ 0 & p _ {i j}! = y _ {i} \end{array} \right. \tag {7}
$$

We train a logistic regression model as the sketch model with features extracted by LSTM and labels obtained by Eq. 7. In online recognition, for data $x_{i}$ , the sketch model provides the probability of each model recognizing the data correctly as $g_{i}$ .

# B. MODEL SCHEDULING

After obtaining the probabilities $g_{i}$ , we model the schedule problem as a weighted rectangle knapsack problem. Given a set of rectangles $A = a_{j_{m}} := (o_{j}, t_{j})_{m}$ , each of which is associated with a profit $g_{j}$ , we expect to pack a subset of rectangles into a bigger rectangle $R := \{O, T\}$ to maximize the total profit. We use a weighted rectangle knapsack algorithm[21] to select packed models into orthogonal resource limitations, whose approximation ratio is $\frac{1}{3}$ . Then we fuse the predictions of selected models with weighted average referred to probabilities $g_{i}$ . The algorithm is summarized in Algorithm 2.

Algorithm 2 Two Step Online Model Fusion   
Input: sketch model $SM$ , data set $X$ , resource limitations $R = (O, T)$ , model occupations $A = \{(o_j, t_j)\}_m$ Output: prediction result $\tilde{y}$ 1: for all $x_i \in X$ do

2: Extract feature $f_i$ from data $x_i$ .

3: $g_i \leftarrow SM(f_i)$ 4: $\tilde{A}_i \leftarrow \text{RectangleKnapsack}(g_i, R, A)$ 5: for all $a_{ij} \in A_i$ do

6: run model $a_{ij}$ to get prediction $p_{ij} = (p_{ij}^1, p_{ij}^2, ..., p_{ij}^k)$ .

7: end for

8: $\tilde{y}_i = \arg \max_k \sum_{a_{ij} \in \tilde{A}_i} g_{ij} \cdot p_{ij,k}$ 9: end for

# VI. IMPLEMENTATION AND EVALUATION

In this section, we introduce experiments including experimental settings and result analysis.

# A. DATASET

We conduct experiments on a self-collecting and self-labeling human activity dataset in an office with multi-modal signals. The layout of the office is in Fig. 4.

We collect dataset about human activities with two device-free sensing devices and a wearable device: voice recorder, radio frequency identification device(RFID), and smart phone.

![](images/29eb7fd961fa7c4843e5f9aa7d55936df930c385014719fa12f7e48663f3040d.jpg)



Fig. 4: room layout and the locations of sensing devices.

When a person is taking actions, his body may rub objects or hit the ground etc and generate sound. In the meanwhile, the radio-frequency(RF) signals from the emitter will reflect on his body and finally reach the receiver. So we place the voice recorder on the floor beside the person to record acoustical signals. The receiver and emitter of RFID are placed on the floor in front of the person symmetrically to record RF signals. The acoustic signals are captured at 44100 samples per second. And RF signals are captures 20 samples per second. Totally, our dataset contains approximately 5 hours of continuous actions.

We collect data of 9 different activities:

- micro movements: people move their fingers or limbs slightly and don't move their bodies in most cases, like knock, bounce ball.   
- limb movements: people mainly move their arms or legs while their torso are almost kept still, like step, punch, clap.   
- torso movements: people move their torso while moving their arms or legs, like walk, jump, bow, squat.

We list the details of these actions in Table. I.

Besides, we deploy a data augmentation method to handle the data set. For RF and acoustical data (ACO), we add random white noise to original data. For accelerator data (ACC), we spin the data by a random angle less than $10^{\circ}$ for x, y, z axis.

# B. MODEL LIBRARY

We train models with single modality data of acoustical signals and RF signals respectively. For each modality, we train models with various machine learning algorithms include

- traditional machine learning models: like support vector machine, random forest and naive Bayes etc.   
- ensemble learning models: like xgBoost[24].   
- deep neural network models: like LSTM[22], which can capture temporal information.

The information of the models is in Table II.

<table><tr><td>movement range</td><td>action</td><td>detail</td><td>proportion</td></tr><tr><td rowspan="3">limb movements</td><td>step</td><td>a man stepping without moving, making slight sound with hitting the ground.</td><td>15%</td></tr><tr><td>punch</td><td>a man punching alone, almost silent.</td><td>8%</td></tr><tr><td>clap</td><td>a man clapping his hands, making clear sound</td><td>11%</td></tr><tr><td rowspan="4">body movements</td><td>walk</td><td>a man walking around, making slight sound.</td><td>4%</td></tr><tr><td>jump</td><td>a man jumping in place, making slight sound while hitting the ground.</td><td>15%</td></tr><tr><td>bow</td><td>a man bowing, almost silent.</td><td>5%</td></tr><tr><td>squat</td><td>a man squatting, almost silent.</td><td>5%</td></tr><tr><td rowspan="2">micro movements</td><td>knock</td><td>a man knock the ground with an empty bottle, making clear sound.</td><td>12%</td></tr><tr><td>bounce ball</td><td>a man bouncing ping pang ball with a wooden pat, making clear sound.</td><td>25%</td></tr></table>

TABLE I: We collect data about human actions of different movement ranges and different sound amplitudes. During data collection, two volunteers are involved, including a male and a female, of different figures.

<table><tr><td>modality</td><td>model</td><td>acc</td><td>mem(MB)</td><td>time(s)</td></tr><tr><td rowspan="3">RF</td><td>SVC</td><td>0.50</td><td>64</td><td>0.050</td></tr><tr><td>XGBoost</td><td>0.62</td><td>346</td><td>0.855</td></tr><tr><td>LSTM</td><td>0.69</td><td>1618</td><td>4.966</td></tr><tr><td rowspan="3">acoustical</td><td>SVC</td><td>0.59</td><td>118</td><td>0.085</td></tr><tr><td>XGBoost</td><td>0.79</td><td>393</td><td>0.793</td></tr><tr><td>LSTM</td><td>0.53</td><td>1618</td><td>5.413</td></tr><tr><td rowspan="3">accelerator</td><td>SVC</td><td>0.75</td><td>65</td><td>0.070</td></tr><tr><td>XGBoost</td><td>0.83</td><td>500</td><td>4.000</td></tr><tr><td>LSTM</td><td>0.85</td><td>1617</td><td>5.319</td></tr></table>

TABLE II: Model Library. End-to-end model with only one modality sensing data.

# C. BASELINE APPROACHES

Since different modality data may carry different information, it is possible that we can improve the recognition accuracy by directly training models with multiple modality data. So we train end-to-end models with multiple modalities simultaneously. This is called feature level fusion. For SVC and XGBoost, firstly we extract features[25] from different modality data. Then we concatenate features of different modalities to train end-to-end multi-modal models. Details are in Fig. 5.

For LSTM, we align, down sample and concatenate sensing streams of different modalities in the same way as in Fig. 3. Then we train LSTM classification model with the 160\*5 sensing sequences. The performances of multi-modal end-to-end models are in Table III.

![](images/fdde5d8dd34f5cfd0a6a46252c9162afeaa9bbaadcaf44a3f70418e911a2fc83.jpg)



Fig. 5: end-to-end multi-modal XGBoost

<table><tr><td>modalities</td><td>model</td><td>acc</td><td>mem(MB)</td><td>time(s)</td></tr><tr><td rowspan="2">RF+ acoustical</td><td>SVC</td><td>0.59</td><td>118</td><td>0.063</td></tr><tr><td>XGBoost</td><td>0.85</td><td>392</td><td>0.911</td></tr><tr><td rowspan="4">RF+ acoustical+ accelerator</td><td>XGBoost</td><td>0.85</td><td>316</td><td>1.69</td></tr><tr><td>LSTM</td><td>0.88</td><td>1617</td><td>4.209</td></tr><tr><td>Algorithm 1</td><td>0.90</td><td>500</td><td>4</td></tr><tr><td>Algorithm 2</td><td>0.90</td><td>750</td><td>6</td></tr></table>

TABLE III: The performances of end-to-end multi-modal models and our online methods.

# D. EXPERIMENTAL SETTINGS

We implement different model selection methods and compare their performances.

- theoretically optimal: For each data sample in $X$ , the recognition is correct as long as there is at least one model which predicts the sample correctly. And the accuracy calculated this way is the theoretically optimal result of the model library.   
- actor-critic based online selection method. We use our actor-critic based online method to select model combination and fuse predictions with different hyper parameters. We implement Algorithm 1 with different $\alpha_{1},\alpha_{2}$ to measure the influences of resource limitations and accuracy. The influence of $\alpha_{1},\alpha_{2}$ in reward is in Table IV.   
- stacking based online selection method: We use LSTM to extract features from all modalities and train a XGBoost model as sketch model to evaluate each model's correctness probabilities. Then we use rectangle knapsack to further select model combination under resource limitations. We implement Algorithm 2 under different resource constraints and analyze it's performance in Tab V.

<table><tr><td> $\alpha_1$ </td><td> $\alpha_2$ </td><td>training episodes</td><td>convergence value</td></tr><tr><td>0.8</td><td>0.5</td><td>25</td><td>0.81</td></tr><tr><td>0.5</td><td>0.5</td><td>20</td><td>0.72</td></tr><tr><td>0.5</td><td>0.5</td><td>40</td><td>0.65</td></tr></table>

TABLE IV: The influence of hyper parameters to the training episodes before convergence and the convergence value of mean reward each episode. When $\alpha_{1}=0.8$ and $\alpha_{2}=0.5$ the method has best performance, which is intuitive.

The performances of different selection and fusion methods are shown in Table V. As a result, when memory limitation is 500MB and time limitation is 4s, our actor-critic based method and stacking based method can reach 90% an 86% accuracy respectively. Compared to single models in model library, the accuracy improves over 10 percents. Compared to end-to-end models, whose best accuracy is 90%, with even larger resources of 1617MB and 4.2s. To summarize, our methods reach 86% and 90% accuracy with models whose accuracies are not higher than 79%. And our actor-critic based method reaches the same accuracy with end-to-end multi-modal model with much smaller resources.

Fig. 6 shows the average weight of each model being assigned by different methods. When resource limitations are compact, the actor-critic based decision method performs better than the stacking based method. In comparison, the stacking based method selects less accurate models with smaller resource demands, like RF SVC model and acoustical SVC model. Nevertheless the actor-critic based decision method prefers more accurate models even their resource demands are larger, like RF XGBoost model and acoustical XGBoost model. The actor-critic based online decision method performs better because it deals with resource limitations and accuracy optimization in one shot. However, in order to support portability for changeable resource constraints, the stacking based method decouple the correctness possibility estimation and possibility based resource allocation procedures. In online evaluation process, we obtain probabilities of each model recognizes data correctly individually. And in scheduling process, we expect to select models, the sum of whose probabilities are largest. However, the possibility of the models' prediction fusion result is correct is not equivalent to the sum of each model's correctness possibility.

$$
P (A) \neq \sum_ {a \in A} P (a) \tag {8}
$$

$P(a)$ denotes the possibility of model a recognize data correctly. $P(A)$ denotes the possibility of fusion result of models in A is correct. As a result, the accuracy decreases because of the inconsistency between the evaluation target and the knapsack target. The former actor-critic based online method can better deal with the trade off between accuracy target and resource limitations and make better use of limited resources. As a result it reaches higher accuracy.

<table><tr><td rowspan="2">method</td><td colspan="3">resources(MB, s)</td></tr><tr><td>(500, 4)</td><td>(750, 6)</td><td>(3000, 6)</td></tr><tr><td>Algorithm 1</td><td>0.90</td><td>0.91</td><td>0.91</td></tr><tr><td>Algorithm 2</td><td>0.86</td><td>0.90</td><td>0.91</td></tr><tr><td>optimal</td><td colspan="2">0.98</td><td>0.99</td></tr></table>

TABLE V: Accuracies of different selection method.

From our experiments, optimizing recognition accuracy by dynamically selecting and fusing multiple models is prospecting. And our methods can achieve higher accuracies than single modality models and end-to-end multi-modal models.

![](images/46d890bccdd3a01fcfea7b6ff1c06beb837274f82eb3610db1377332ba624308.jpg)



![](images/3c3088b5d92fdcfac6219f6a95ae37a01fe0cd6ec636a081b8994ac822484f85.jpg)



Fig. 6: The average weight of each model by different online decision methods. We compare the performance of two methods with resource limitations of $R = (500MB, 4s)$ and $R = (750MB, 6s)$ .

# VII. CONCLUSION

We propose two online decision methods to optimize recognition accuracy for a couple scenes, by dynamically selecting and fusing models from a model library, under orthogonal resource limitations. One is the actor-critic based method. We design a reward feedback mechanism to update the online decision model. By a specially designed reward function dealing with resource limitations and accuracy optimization in one shot, this method achieves much higher accuracy. The other is the stacking based method. We decouple the probability of models recognizing data correctly and resource allocation, so that the method is flexibly transferable with changeable resources. We test the methods' effectiveness on a sensing dataset of 9 human actions and 3 modalities. The result shows that our method improves the accuracy over 10 percents compared to single model in model library. Compared to end-to-end multi-modal models, we achieve higher accuracies with much lower resources.

# ACKNOWLEDGEMENT

The research is supported by National Key R&D Program of China 2017YFB1003003, National Natural Science Foundation of China with No. 61822209, No.61625205No. 61932016, No. 61751211, No. 61520106007, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002.

# REFERENCES

[1] Eunbyung Park, Xufeng Han, Tamara L Berg, and Alexander C Berg. Combining multiple sources of knowledge in deep cnns for action recognition. In 2016 IEEE Winter Conference on Applications of Computer Vision (WACV), pages 1–8. IEEE, 2016.   
[2] Narayanan C Krishnan and Diane J Cook. Activity recognition on streaming sensor data. Pervasive and mobile computing, 10:138–154, 2014.   
[3] Ahmad Jalal and Shaharyar Kamal. Real-time life logging via a depth silhouette-based human activity recognition system for smart home services. In 2014 11th IEEE International Conference on Advanced Video and Signal Based Surveillance (AVSS), pages 74–80. IEEE, 2014.   
[4] Sebastian Münzner, Philip Schmidt, Attila Reiss, Michael Hanselmann, Rainer Stiefelhagen, and Robert Dürichen. Cnn-based sensor fusion techniques for multimodal human activity recognition. In Proceedings of the 2017 ACM International Symposium on Wearable Computers, ISWC '17, page 158165, New York, NY, USA, 2017. Association for Computing Machinery.

[5] Valentin Radu, Nicholas D. Lane, Sourav Bhattacharya, Cecilia Mascolo, Mahesh K. Marina, and Fahim Kawsar. Towards multimodal deep learning for activity recognition on mobile devices. In Proceedings of the 2016 ACM International Joint Conference on Pervasive and Ubiquitous Computing: Adjunct, UbiComp '16, page 185188, New York, NY, USA, 2016. Association for Computing Machinery.   
[6] Atis Elsts, Niall Twomey, Ryan McConville, and Ian Craddock. Energy-efficient activity recognition framework using wearable accelerometers. Journal of Network and Computer Applications, 168:102770, 2020.   
[7] A. Sobti, M. Balakrishnan, and C. Arora. Multi-sensor energy efficient obstacle detection. In 2019 22nd Euromicro Conference on Digital System Design (DSD), pages 19–26, 2019.   
[8] Rafael Possas, Sheila Pinto Caceres, and Fabio Ramos. Egocentric activity recognition on a budget. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 5967–5976, 2018.   
[9] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. arXiv preprint arXiv:1701.06538, 2017.   
[10] Jianan Li, Xuemei Xie, Qingzhe Pan, Yuhan Cao, Zhifu Zhao, and Guangming Shi. Sgm-net: Skeleton-guided multimodal network for action recognition. Pattern Recognition, 104:107356, 2020.   
[11] Javed Imran and Balasubramanian Raman. Evaluating fusion of rgb-d and inertial sensors for multimodal human action recognition. Journal of Ambient Intelligence and Humanized Computing, 11(1):189–208, 2020.   
[12] Raphael Memmesheimer, Nick Theisen, and Dietrich Paulus. Gimme signals: Discriminative signal encoding for multimodal activity recognition. arXiv preprint arXiv:2003.06156, 2020.   
[13] Eshed Ohn-Bar and Mohan Manubhai Trivedi. Hand gesture recognition in real time for automotive interfaces: A multimodal vision-based approach and evaluations. IEEE transactions on intelligent transportation systems, 15(6):2368–2377, 2014.   
[14] Li Zhou. A survey on contextual multi-armed bandits. arXiv preprint arXiv:1508.03326, 2015.   
[15] Lihong Li, Wei Chu, John Langford, and Robert E Schapire. A contextual-bandit approach to personalized news article recommendation. In Proceedings of the 19th international conference on World wide web, pages 661–670. ACM, 2010.   
[16] Lijing Qin, Shouyuan Chen, and Xiaoyan Zhu. Contextual combinatorial bandit and its application on diversified online recommendation. In Proceedings of the 2014 SIAM International Conference on Data Mining, pages 461–469. SIAM, 2014.   
[17] Shuai Li, Baoxiang Wang, Shengyu Zhang, and Wei Chen. Contextual combinatorial cascading bandits. In ICML, volume 16, pages 1245-1253, 2016.   
[18] Timothy P Lillicrap, Jonathan J Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, and Daan Wierstra. Continuous control with deep reinforcement learning. arXiv preprint arXiv:1509.02971, 2015.   
[19] A. G. Barto, R. S. Sutton, and C. W. Anderson. Neuronlike adaptive elements that can solve difficult learning control problems. IEEE Transactions on Systems, Man, and Cybernetics, SMC-13(5):834–846, 1983.   
[20] M. Yuan, L. Zhang, X. Li, and H. Xiong. Comprehensive and efficient data labeling via adaptive model scheduling. In 2020 IEEE 36th International Conference on Data Engineering (ICDE), pages 1858-1861, 2020.   
[21] Klaus Jansen and Guochaun Zhang. On rectangle packing: maximizing benefits. In Proceedings of the fifteenth annual ACM-SIAM symposium on Discrete algorithms, pages 204–213. Society for Industrial and Applied Mathematics, 2004.   
[22] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural computation, 9(8):1735-1780, 1997.   
[23] A Steinberg. A strip-packing algorithm with absolute performance bound 2. SIAM Journal on Computing, 26(2):401–409, 1997.   
[24] Tianqi Chen and Carlos Guestrin. Xgboost: A scalable tree boosting system. In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining, pages 785–794, 2016.   
[25] Ning Xiao, Panlong Yang, Yubo Yan, Hao Zhou, and Xiang-Yang Li. Motion-fi: Recognizing and counting repetitive motions with passive wireless backscattering. IEEE International Conference on Computer Communications, 2018.