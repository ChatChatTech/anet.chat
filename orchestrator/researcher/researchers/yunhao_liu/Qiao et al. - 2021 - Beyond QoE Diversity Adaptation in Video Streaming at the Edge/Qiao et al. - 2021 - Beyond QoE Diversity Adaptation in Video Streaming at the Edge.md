# Beyond QoE: Diversity Adaptation in Video Streaming at the Edge

Chunyu Qiao , Student Member, IEEE, Jiliang Wang, Member, IEEE, and Yunhao Liu, Fellow, IEEE, ACM

Abstract— Adaptive bitrate (ABR) algorithms are critical techniques for high quality-of-experience (QoE) Internet video delivery. Early ABR algorithms conducting the overall QoE function of fixed parameters are limited by the fact that the QoE of end-users are diverse such that the video bitrate is often chosen in a misleading way. State-of-the-art ABR algorithms like MPC and Pensieve utilize offline modeling techniques and result in performance degradation for online QoE diversity adaptation. To address this issue, we propose Elephanta, an online ABR algorithm for edge users, which incorporates user QoE perception interface and adaptation algorithm with flexible parameters. In order to avoid overhead from updating parameters online, we model video streaming as a renewal system and formulate the specific QoE function into flexible formats by setting constraints on corresponding QoE metrics. To validate parameter settings, we emulate Elephanta under 1500 throughput traces, including FCC broadband, 3G HSDPA data set from the Internet, as well as the 4G/LTE data set we collect. Evaluation results show that Elephanta achieves QoE improvement of 7% over MPC and 3% over Pensieve under QoE diversity in part because of its superior adaptability to QoE diversity. We implemented Elephanta in dash.js at the client side for subjective experiments. We observed the diverse QoE preferences across users and 19/21 users (strongly) agree that Elephanta is responsive to parameter changes while watching videos.

Index Terms— QoE diversity, adaptive bitrate algorithms, video streaming.

# I. INTRODUCTION

N RECENT years, video streaming has been a crucial I topic within the Internet community. Along with this, the demands on improving the quality-of-experience (QoE) of video streaming have taken the front stage. Providing high QoE can significantly improve user engagement. On the other hand, if QoE decreases, it will cause user withdrawal and revenue loss [1]. Hence, video providers are making efforts to promote their service quality.

Presently, various kinds of video applications have become more and more popular, such as video on demand (Netflix [2]),

Manuscript received July 5, 2019; revised March 22, 2020, June 5, 2020, and September 4, 2020; accepted October 11, 2020; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor S. Rao. Date of publication October 29, 2020; date of current version February 17, 2021. This work was supported in part by the National Natural Science Foundation of China (NSFC) for Excellent Young Scholars under Grant 61722210, NSFC Grant 61932013, and NSFC Grant 61532012. (Corresponding author: Jiliang Wang.)

Chunyu Qiao and Jiliang Wang are with the School of Software, Tsinghua University, Beijing 100084, China (e-mail: tionry@163.com; jiliangwang@tsinghua.edu.cn).

Yunhao Liu is with the College of Global Innovation Exchange (GIX), Tsinghua University, Beijing 100084, China (e-mail: yunhaoliu@gmail.com).

Digital Object Identifier 10.1109/TNET.2020.3032416

short videos (TikTok [3]), and live videos (Douyu [4]). To serve end-users with different device types under heterogeneous networks, Dynamic Adaptive Streaming over HTTP (DASH) has been the main video delivery technique, with Adaptive bitrate (ABR) algorithms deployed for bitrate selection. Current video providers have a large number of video content and users. E.g., YouTube has up to 1 billion users all around the world, which means huge QoE diversity. Existing ABR algorithms often employ a fixed QoE format and have been proved to be well-performed [5]–[7]. However, they may incur misleading bitrate selection for a specific client. For example, a user with a large screen requires high bitrate viewing experience while the ABR algorithm selects lower bitrate to avoid possible video rebuffering. Since the QoE among users is diverse, while the overall QoE function is just an estimation on average, the algorithms may lead to performance degradation under QoE diversity. Indeed, in our experiment, the MPC suffers 15% of QoE degradation.

QoE diversity reflects on various preferences to QoE metrics like average bitrate, rebuffering time, and bitrate switch. Specific QoE functions should be utilized across different scenarios to address this diversity – considering video content, user preference, device type, etc. [1], [8], [9] In many cases, users have different preferences on different QoE metrics across different scenarios, or they may have different interests in different kinds of videos. E.g., high bitrate in soccer games for watching wonderful moments vs. fluent track (does not require high bitrate) for music shows. The difference may also come from devices of different screen sizes: users with small screens like smartphones tend to endure low bitrate, while users with TVs expect a high bitrate for clear pictures.

Existing approaches suffer from dealing with QoE diversity in two-fold: 1) Simple ABR algorithms conduct straightforward bitrate selection that cannot deal with QoE diversity within algorithms. 2) Predictive models and machine learningbased approaches like MPC [5], Pensieve [7] are conducted using a fixed QoE function, meaning that these algorithms need to be modified for them to adapt to diversity by conducting specific QoE functions. There are also natural ideas to use existing ABR algorithms for QoE diversity, such as (1) online adjusting QoE parameters in the algorithm according to user preference or (2) pre-computing all possible models offline and sending the right one to the client by user preference. However, on one side of the matter, online modification often needs the specific QoE function perception, which will lead to huge recomputation cost for updating parameters in complicated algorithms, like MPC [5] and Pensieve [7].

![](images/14c4b52ae2aac4fa496e6d909a6afed561912880519ba41e61d4124e7805d18e.jpg)



Fig. 1. Overview of Elephanta in DASH.

On the other hand, offline modification requires acknowledging specific QoE functions of every user beforehand. Even if we pre-compute all possible models at the server side, it will still introduce network latency to process bitrate selection at the client’s side, risking the chance of incurring extra offline computation cost for rerunning models as the QoE parameter change [5].

To adapt to QoE diversity effectively, we propose Elephanta, which formulates the specific QoE function with flexible notions on corresponding metrics and accommodates the ABR algorithm with online parameter updates.

As shown in Figure 1, DASH supplies video servers and heterogeneous clients for video delivery. To address the QoE diversity adaptation, we incorporate the QoE monitor and ABR controller in the video player at the edge. The QoE monitor percepts the specific QoE function by providing both multiple default metric schemes and user interfaces for online parameter tuning. The ABR controller updates the parameters according to feedback from the QoE monitor and selects the video bitrate accordingly. To avoid introducing extra cost from parameter updates, our ABR controller adopts the QoE function with flexible parameters on different metrics online and uses a dynamic parametric ABR algorithm for efficient bitrate selection.

Elephanta models video streaming as a renewal system [10], which maps the parameters into corresponding problem constraints for it to adapt to QoE diversity online. For performance assurance, we formulate the problem as bitrate optimization with online adjustable constraints. Accordingly, we utilize an optimization algorithm to solve the problem.

We validate the design of Elephanta by using 1500 throughput traces evenly from an online data set [11], [12] (including eight months of 3G and broadband data) and two months of 4 /LTE data set collected by the team under different environments (including campuses, dormitories, offices, and moving buses). We then implement Elephanta in the reference DASH client implementation dash.js [13]. To examine its performance, we compare Elephanta with state-of-the-art ABR algorithms: Pensieve [7], MPC [5], BOLA [6], BB [14], and Elastic [15]. The results show that Elephanta achieves 90% performance of MPC and Pensieve under fixed QoE function while outperforming MPC by 7% and Pensieve by 3% under QoE diversity in turn. Implemented in real video player dash.js, Elephanta can perform bitrate decisions in real-time to the change of QoE parameters.

We conduct subjective experiments by inviting 21 volunteers for online video viewing via Elephanta. The volunteers can adjust the QoE parameters (reflecting QoE diversity) by the interface provided by Elephanta while watching videos. Most of them agree that Elephanta is helpful and responsive to all interactions. 12 21 volunteers were willing to use the /interaction of Elephanta for their preferences, while 6 21 /of them were not. This is mainly due to the frustration encountered by users from the interactions. We learn from the results that it is better to provide multi-version ABR algorithms under QoE diversity for real users. For example, we can provide user interaction-based Elephanta or autotuning parameter-based Elephanta according to different video types so that the users can choose the type of Elephanta for convenience.

The organization of the remainder is as follows. Section IIpresents the background of video streaming and our motivation. Section  introduces modeling Elephanta and the IIIformulation of QoE diversity. Section  derives the algo-IVrithm design and analyzes penalty and constraint settings of Elephanta. Section  evaluates Elephanta under different Vnetworks and constraint settings. Section  discusses buffer V Ibehavior and real-world user preference. Section shows V IIrelated work on the QoE metrics and bitrate selection issues. Section concludes our work.

# II. BACKGROUND AND MOTIVATION

# A. Video Streaming at the Edge

Service of video streaming under P2P networks became popular among both academia and industry within recent years [16]–[18]. With the increasing types of devices for video plays, like TVs, mobile devices, and laptops, video streaming over HTTP has become a more popular technique for video services. Under the standard HTTP based video structure DASH shown in Figure 1, the video is stored in the content delivery network (CDN), with multiple copies encoded in different bitrate, examples being 4 , 8 , Mbps Mbpsand 10 . Each copy is divided into chunks of equal M bpslength. E.g., a 1-minute video can be segmented into 15 chunks, 4 seconds each. To play a video at the client’s side, the ABR controller of a video player requests video chunks with chunk number  and bitrate . Upon receiving the request, n rCDN responds with the corresponding video chunk, then the video player downloads and stores the chunk in the playback buffer for when it is needed to play. Such a process is compatible with different edge devices and has been widely deployed.

To provide high-quality video services, the following QoE metrics in video streaming are usually used to measure the video quality [1], [9]: 1) Average bitrate - the average bitrate level of a video session is positively related to the user QoE. 2) Rebuffering - this event occurs when the buffer of a video player is empty. Rebuffering is defined as the total time or occurrence times of rebuffering, which greatly decreases the user QoE, and 3) Bitrate switch - change of video bitrate level. The increase of bitrate switch causes video flicker effects and also decreases the QoE.

# B. QoE Driven ABR Algorithms

ABR algorithms have been widely employed for video providers to select proper bitrate adaptively under dynamic networks, including Microsoft [19], Adobe [20], and Apple [21]. Recent years have witnessed the rapid emergence of ABR algorithm design.

An ABR algorithm is used to select video bitrate according to network dynamics at the client-side. Earlier studies focused on single QoE metrics. For example, they directly used the average bitrate as the QoE function and improved this metric by predicting future bandwidth [15], [22], [23]. Unfortunately, merely increasing the average bitrate may lead to a decrease in another metric, such as bitrate switch and rebuffering.

Hence, other methods are proposed for mixing multiple QoE metrics using predictive model-based techniques to optimize the QoE function [5], [7].

# C. Performance Degradation Under QoE Diversity

Current video providers serve a large number of users with different types of edge devices over a vast range of locations. Existing algorithms conduct an overall QoE function leaving out QoE diversity, which leaves a gap for ensuring high-quality service for every edge user. We take MPC [5] as an example for illustration.

MPC conducts parameters like rebuffering penalty $P _ { r e }$ and smooth penalty $P _ { s m }$ Pin the QoE function like Equation 1. In Pthis experiment, we denote QoE diversity by assuming that the parameters subject to Gaussian distribution $N ( \overline { { P } } _ { r e } , ( \mu \overline { { P } } _ { r e } ) ^ { 2 } )$ and $N ( \overline { { P } } _ { s m } , ( \bar { \mu } \overline { { P } } _ { s m } ) ^ { 2 } )$ , where $\mu$ N P , μPis a positive constant and N P , μP μpositively correlated with diversity. We test the performance of different groups of diversity. Each group contains a specific parameter combination $( P _ { r e } , P _ { s m } )$ , which are subject to $N ( \overline { { P } } _ { r e } , ( \mu \overline { { P } } _ { r e } ) ^ { 2 } )$ , $N ( \overline { { P } } _ { s m } , ( \mu \overline { { P } } _ { s m } ) ^ { 2 } )$ , respectively and N P , μPthe overall parameters $( \overline { { P } } _ { r e } , \overline { { P } } _ { s m } )$ P under the same network throughput traces.

The quantified QoE is calculated as $Q o E = A v g B i t r a t e -$ $P _ { r e } * R e b u f * P _ { s m } * B i t S w - P _ { j t } T _ { j t }$ oE, where $P _ { r e } , P _ { s m } , P _ { j t }$ P Rebuf P BitSw P T P , P , Pare non-negative constant penalty parameters corresponding to the bitrate switch, rebuffering time and join time, respectively. We set the join time as the constant in this experiment. We also set the overall parameters $( \overline { { P } } _ { r e } ~ = ~ 4$ and $\overline { { P } } _ { s m } ~ = ~ 1 )$ P Pand emulate network conditions under throughput traces introduced in Section $\mathrm { V } { - } \mathrm { A } . 1$ . For MPC under specific parameters where $P _ { r e }$ and $P _ { s m }$ are subject to $N ( 4 , ( 4 \mu ) ^ { 2 } )$ and $N ( 1 , \mu ^ { 2 } )$ , P P N , μ N , μwe use them to decide bitrate selection. While for MPC under overall parameters, we use the overall parameters to decide bitrate selection. We generate the specific parameters for each throughput trace to calculate QoE. To present the impact of QoE diversity, we calculate the QoE ratio of $Q o E _ { o v e r a l l } / Q o E _ { s p e c i f i c }$ for $\mu$ ranging from 0 1 to 0 9. The QoE /QoE μ . .results are shown in Figure 2. The findings are in two-fold: 1) The overall QoE of MPC degrades at up to 15% on average comparing to specific QoE functions, 2) When $\mu$ increases μ(QoE diversity increases), the performance ratio of overall MPC still decreases. For the largest , 0 9, the QoE ratio μ .drops to only 73% of specific QoE functions.

![](images/afac5b8c9aa4ee4c3360d78e0c2683f6fd837724c43070f7e857d94f589fbeb5.jpg)



Fig. 2. QoE ratio comparison of MPC under specific QoE parameters and overall QoE parameters. (µ is a constant linear coefficient on standard deviation of normal distribution, which is positively correlated to QoE diversity level.)

A way to adapt to QoE diversity online for existing ABR algorithms, like MPC, a natural idea is to change QoE parameters according to the QoE diversity (user preference). However, the specific QoE functions of users are elusive for servers. The users may be confused about how to represent their preferences by the parameters. Even if we assume that it is possible to capture the specific QoE functions online, the adaptation for parameter change of prior work will induce extra overheads. In other words, changing the QoE function will result in the re-computing of models or even re-deploying of video players. For example, MPC calculates an indexing table for a specific video offline beforehand, with minimal sizes up to hundreds of kB. Updating the parameters in specific QoE functions will lead to a recalculation of the indexing table. On the other hand, we may use MPC by offline numerating all MPC tables according to the user’s preference and send the right table to the user. But the process of sending MPC table between servers and clients will induce latency for bitrate decision in MPC. Thus, this may make MPC freeze for a while, and it will incur a non-trivial offline computation cost that may need to be rerun as the operating conditions (like QoE parameters) change [5].

# D. Introducing Renewal System

We introduce a renewal system for modeling QoE diversity in our study. The renewal system is extended from the slotted structure. E.g., the discrete-time queueing system. In a discrete-time queueing system, every integer time slot $t \in \{ 0 , 1 , 2 , \ldots \}$ contains a single random event ( ) and a single action ( ). The combination of $\alpha ( t )$ and $w ( t )$ generα t α t w tates a vector of attributes (penalties and rewards) for that slot. While in the renewal system, the frame durations are variables and can depend on the decisions made throughout the frame. An example of a renewal system stated in [10] is a wireless sensor network that is repeatedly used to perform sensing tasks [24]. Assuming that each new task starts immediately after the previous task is completed, the duration and the network resources used for each task will depend on the policy implemented for that task.

Concerning video streaming, the video player performs just like a renewal system where the task is to download video chunks. Each video chunk is requested when the previous one finishes downloading. The download time is decided by the policy. For example, the video bitrate is selected by the ABR algorithm according to the network condition.

# III. MODELING QoE DIVERSITY

# A. Video Streaming Model

In DASH, the video is segmented into  chunks containing n seconds in each video. Each chunk is encoded in Sdifferent bitrate levels, assuming that the size of bitrate $j$ is $s _ { j }$ $( 1 \leq j \leq m )$ .

j mWhen a connection is established, the video player will request chunks, one by one, with each having a specified bitrate. Assuming the video player requests nchunks, the downloaded video chunks are denoted as $c [ 0 ] , c [ 1 ] , c [ 2 ] , \cdot \cdot \cdot , c [ n - 1 ]$ . The download start time of chunk c , c , c , , c n[ ] is [ ]. The transmission time of downloading chunk $c [ i ]$ c i t ican be calculated as $T [ i ] = t [ i + 1 ] - t [ i ]$ c i. Denote [ ] as the T i t i t i π ipolicy for determining the bitrate selection of chunk [ ].

c iWhen a requested chunk has been downloaded, it will be stored in the video player’s buffer. A video chunk will be removed from the buffer as soon as it is played. To address bitrate selection effectively using buffer occupancy, we measure the video buffer by the total playtime of video chunks instead of sizes. The buffer occupancy is denoted as $b u f _ { \cdot }$ , bufwhich accommodates seconds of video. The buffer occupancy at time  is $b u f [ t ]$ . When $b u f [ t ] = 0 \mathrm { . }$ , there remains t buf t buf tno video chunk to play in the buffer, and rebuffering occurs. Intuitively, it indicates that the video player needs to wait for a chunk to be downloaded. When the buffer is full at time $( \mathrm { i . e . , } b u f [ t ] = b _ { m a x } )$ t, the player stops downloading the next buf t bchunk. Video chunks in the buffer are served in FCFS manner.

# B. Adaptation for QoE Diversity

To address the diversity of user QoE, we first discuss our understanding of the issue and why previous work does not address it.

In video streaming, it is challenging to define the QoE function as it is exactly in the real world. Previous work quantifies QoE by mixing video quality metrics such as a linear combination of average bitrate, rebuffering, bitrate switch and join time, shown as follows [5]:

$$
\begin{array}{l} Q o E = \frac {\sum_ {i = 0} ^ {n - 1} u (c [ i ])}{n} - P _ {s m} \frac {\sum_ {i = 0} ^ {n - 1} y _ {b s} (c [ i ])}{n} \\ - P _ {r e} \frac {\sum_ {i = 0} ^ {n - 1} y _ {r e} (c [ i ])}{n} - P _ {j t} T _ {j t} \tag {1} \\ \end{array}
$$

where $P _ { s m } , P _ { r e }$ and $P _ { j t }$ are non-negative constant parameters P , P Pcorresponding to bitrate switch, rebuffering time 1 and join time, respectively.

1We use both frequency of rebuffering and length in time of rebuffering in our experiment.

Though previous work tries to optimize the bitrate selection to maximize average QoE, there leaves a gap that conducting overall QoE function does not promise expected performance for a specific user. E.g., some users only care about rebuffering issues, while others prefer high average bitrates. Such diversity remains unsolved in prior models.

To satisfy the diversity issue, we are inspired to set constraints on corresponding metrics. However, solely satisfying the constraints on the metrics cannot achieve maximal QoE. Thus we define average bitrate as utility and transform the problem into bitrate optimization under constraints on the specific metrics.

Since join time usually occurs at the beginning of a video session, we will consider the following metrics in our paper: average bitrate, bitrate switch, and rebuffering. In addition, we introduce buffer occupancy for consideration. Previous work has shown that selecting bitrate according to buffer occupancy will improve QoE [14], [25]. The buffer occupancy is not directly related to QoE metrics. However, it can directly reflect the condition of video players. For small buffer occupancy, the video faces a chance of rebuffering, while large buffer occupancy, the video can play smoothly. We choose buffer occupancy as one constraint in Elephanta to control the bitrate selection. For example, the maintenance of low buffer occupancy makes Elephanta select a higher bitrate as soon as the network recovers from a low bandwidth state. However, it may raise a concern that constraining buffer occupancy will increase the risk of rebuffering. So we carefully conduct experiments on configuring the use of buffer occupancy, e.g., setting the buffer reservoir in later sections.

We use the terms penalty and utility to illustrate the problem formulation. The penalties are defined as functions of corresponding metrics, including bitrate switch, rebuffering, and buffer occupancy, denoted as $y _ { b s } , y _ { r e }$ and $y _ { b o } ,$ respectively. We y y ydefine average bitrate as utility, . We denote the average utiluity, penalty of bitrate switch, rebuffering and buffer occupancy over chunks as follows: $\overline { { u } } = \sum _ { i = 0 } ^ { n - 1 } \frac { u ( c [ i ] ) } { n } , \overline { { y } } _ { b s } = \sum _ { i = 0 } ^ { n - 1 } \frac { y _ { b s } ( c [ i ] ) } { n }$ , $\overline { { y } } _ { r e } = \sum _ { i = 0 } ^ { n - 1 } \frac { y _ { r e } ( c [ i ] ) } { n } , \overline { { y } } _ { b o } = \sum _ { i = 0 } ^ { n - 1 } \frac { y _ { b o } ( c [ i ] ) } { n } .$ bo i=0 i=0

Note that the diversity is reflected on different QoE metrics expectations, e.g., the penalty value $\overline { { y } } _ { r e }$ should be as small yas possible for a user who prefers no rebuffering. Then we can write the bitrate selection optimization problem as the following:

$$
\max \overline {{u}} \tag {2}
$$

$$
s. t. \overline {{y}} _ {b s} \leq c _ {b s}
$$

$$
\overline {{y}} _ {r e} \leq c _ {r e}
$$

$$
\overline {{y}} _ {b o} \leq c _ {b o}
$$

where $c _ { b s } , c _ { r e } , c _ { b o }$ are constraints on penalties of bitrate c , c , cswitch, rebuffering, and buffer occupancy.

Performance Objective: Elephanta aims to achieve maximized utility while satisfying the constraints on penalties. Constraint $c _ { l }$ represents the expected bounding of the corresponding penalty. Thus different constraint values can be used to denote QoE diversity. Till this point, the bitrate selection problem has transformed into the utility optimization problem with penalty constraints.

![](images/52f0e876c61d2911f4cc7572106f8bf2762cb46de45e09f5ea286f2b76d2e316.jpg)



Fig. 3. A sequence of frames in renewal system, each frame’s length $( \mathrm { e . g . }$ , time) is determined by corresponding policy. The frames in system generate penalty and utility vectors. Penalty as ${ \bf \bar { \Lambda } } _ { p [ 0 ] , p [ 1 ] , { p [ 2 ] , \dots } }$ . and utility as $u [ 0 ] , \bar { u } [ 1 ] , \bar { u [ 2 ] } , . . . ,$ , respectively.

# C. Flexible QoE Function Formulation

As we formulate bitrate selection into an optimization problem with constraints, we are motivated to solve the problem efficiently. Though the dynamic programming-based approaches can be used to solve the problem [26], they usually require knowledge of future bandwidth, which is unavailable in the real world. Even if the future bandwidth can be predicted, such approaches will lead to a large state space to calculate the optimal bitrate and leave large overheads for clients.

To address the issue, we formulate the problem into a flexible format under the renewal system model.

Video chunks are downloaded one by one, which makes video streaming model an ideal candidate for the renewal system model. As shown in Figure 3, a typical renewal system comprises sequential renewal frames. Each frame occurs one after another with elapsed time $T [ i ]$ . The policy  is to T i πdetermine the corresponding task of the current frame, e.g., selecting bitrate in video streaming, each task generates a penalty vector p and a utility vector u. The goal is to maximize the overall utility under given constraints on penalties.

To formulate the bitrate selection problem under the renewal system model, we relax our model slightly by making the following assumptions: 1) A video player begins to download a new video chunk as soon as the previous one is downloaded unless the buffer is full or playback is aborted. Frame  is iregarded as the start and end time of chunk [ ]. 2) When a c ivideo chunk downloading is aborted due to network failures, the player will request the same chunk of another bitrate. The penalties of the last failing request will be counted, i.e., the failed chunk will be regarded as a virtual video chunk. 3) When a video begins to play, the buffer level is empty, $b u f [ 0 ] = 0$ . The penalties and the utility generated in the bufsystem are finite, and the download time $T [ i ] > 0$ .

T i >As a result, Elephanta is modeled as a renewal system, and each video chunk behaves as a frame. Accordingly, the policy $\pi [ i ] \in \mathcal { P }$ in our system specifies the bitrate selection for chunk π i. We denote $\mathcal { P }$ as the policy space for bitrate selection.

We define the utility [ ] as negative penalty 0[ ] in the urenewal system. Note that $y _ { 0 }$ y idenotes penalty in the renewal ysystem. Therefore, we define the utility of bitrate level as $- y _ { 0 }$ . For each chunk i,

$$
y _ {0} [ i ] \triangleq - u [ i ] = - \phi (c [ i ]) \tag {3}
$$

Hence, we have the penalty vector $\pmb { y } ~ = ~ \left( y _ { 0 } , y _ { 1 } , y _ { 2 } , y _ { 3 } \right)$ where 0, 1, 2 and $y _ { 3 }$ y , y , y , ycorrespond to utility, rebuffering, bitrate switch, and buffer occupancy, respectively. We can also see that the download time for chunk is positive, and both the time and penalties $T [ i ]$ and $\mathbf { \nabla } y [ i ]$ iare finite for all policies $\pi \in { \mathcal { P } }$ .

πAccording to the average time and penalties defined in the renewal system, the average download time for a video session is ${ \overline { { T } } } .$ . For each chunk $i ,$ the policy $\pi [ i ]$ generates a penalty Tvector $\mathbf { y } [ i ] = ( y _ { 0 } [ i ] , y _ { 1 } [ i ] , y _ { 2 } [ i ] , y _ { 3 } [ i ] )$ π i. The average penalty is idefined as $\overline { { \mathbf { y } } } = ( \overline { { y } } _ { 0 } , \overline { { y } } _ { 1 } , \overline { { y } } _ { 2 } , \overline { { y } } _ { 3 } )$ ,.

y , y , y , yThe optimization of utility in Elephanta is the minimization of $y _ { 0 }$ in the renewal system. Hence, the problem formulation yin Equation (2) can be equally transformed into the following format:

$$
\min \frac {\overline {{y}} _ {0}}{\overline {{T}}}
$$

$$
s. t. \frac {\overline {{y}} _ {l}}{\overline {{T}}} \leq c _ {l}, \forall l \in \{1, \dots , 3 \}
$$

$$
\pi [ i ] \in \mathcal {P}, \forall i \in \{0, 1, 2, \dots , n - 1 \} \tag {4}
$$

where l $( l \in \{ 1 , \cdots , 3 \} )$ are constraints for average penalties c l , ,of rebuffering, bitrate switch, and buffer occupancy. The QoE diversity is reflected on the flexible constraints and now we finish modeling Elephanta.

# IV. ELEPHANTA DESIGN

# A. Renewal System-Based Optimization

We conduct drift-plus-penalty techniques [10] for algorithm design, which introduces virtual queues to select optimal bitrate.

The penalties in the renewal system correspond to the QoE metrics, denote

$$
\boldsymbol {y} = (y _ {1} [ i ], y _ {2} [ i ], y _ {3} [ i ]) = (y _ {b s} [ i ], y _ {r e} [ i ], y _ {b o} [ i ])
$$

To deal with constraints $c _ { l }$ for $l \in \{ 1 , 2 , 3 \}$ , define corresponding virtual queues $Z _ { l } [ i ] \ ( Z _ { l } [ 0 ] = 0 )$ , ,as follows:

$$
Z _ {l} [ i + 1 ] = \max \left[ Z _ {l} [ i ] + y _ {l} [ i ] - c _ {l} T [ i ], 0 \right] \tag {5}
$$

According to Equation (5), the Lyapunov function for chunk is defined as:

$$
L (\mathbf {Z} [ i ]) \triangleq \frac {1}{2} \sum_ {l = 1} ^ {L} Z _ {l} [ i ] ^ {2}
$$

where  denotes the number of constraints. In this case, $L = 3 .$ . LTherefore, the conditional Lyapunov drift is:

$$
\Delta (\mathbf {Z} [ i ]) \triangleq E \{L (\mathbf {Z} [ i + 1 ]) - L (\mathbf {Z} [ i ]) | \mathbf {Z} [ i ] \} \tag {6}
$$

The renewal system aims to minimize the drift-plus-penalty ratio. While in Elephanta, we have formulated the penalty as 0 and drift as $y _ { l } .$ y. To make our paper easy to follow, we directly yquote the conclusion from Section 7 2 in [10]. The Lyapunov drift in Equation (6) satisfies

$$
\Delta (\mathbf {Z} [ i ]) \leq B + \sum_ {l = 1} ^ {L} Z _ {l} [ i ] E \{\hat {y} (\pi [ i ]) - c _ {l} \hat {T} (\pi [ i ]) | \mathbf {Z} [ i ] \} \tag {7}
$$

where  is a finite constant. According to bounds assump-Btion in [10] (finite bounds of $E \{ \hat { T } ( \pi [ i ] ) ^ { 2 } | \pi [ i ] \ = \ \pi \}$ and

![](images/995eec7c867356353808e215d12630923514bb57d6337e70b0f9778c0ffe45f1.jpg)



Fig. 4. Work flow of Elephanta.

$E \{ \hat { y } _ { l } ( \pi [ i ] ) ^ { 2 } | \pi [ i ] = \pi \}$ exist for  and all $\pi \in { \mathcal { P } } )$ , B exists E y π i π i π land satisfies for all  and possible $Z [ i ] { : }$ :

$$
B \geq \frac {1}{2} \sum_ {l = 1} ^ {L} E \{(y _ {l} [ i ] - c _ {l} T [ i ]) ^ {2} | \mathbf {Z} [ i ] \} \tag {8}
$$

The drift-plus-penalty for chunk i thus satisfies:

$$
\begin{array}{l} \Delta (\mathbf {Z} [ i ]) + V E \{y _ {0} [ i ] | \mathbf {Z} [ i ] \} \leq B + V E \{\hat {y} _ {0} (\pi [ i ]) | \mathbf {Z} [ i ] \} \\ + \sum_ {l = 1} ^ {L} Z _ {l} [ i ] E \left\{\hat {y} _ {l} (\pi [ i ]) | \boldsymbol {Z} [ i ] \right\} - \sum_ {l = 1} ^ {L} c _ {l} Z _ {l} [ i ] E \left\{\hat {T} (\pi [ i ]) | \boldsymbol {Z} [ i ] \right\} \tag {9} \\ \end{array}
$$

where  is a constant variable.

VThus the drift-plus-penalty bound of video chunk  is given iby the right-hand-side of Equation (9). To maximize the utility overtime in Equation (2), i.e., minimizing average yin Equation (4), we are inspired to minimize the bound for policy $\pi [ i ]$ . It has been proven in [10] that the optimal policy π i[ ] can be chosen according to Equation (9) by minimizing π ithe following ratio:

$$
\mathcal {G} [ i ] = \frac {E \{V \hat {y} _ {0} (\pi [ i ]) + \sum_ {l = 1} ^ {L} Z _ {l} [ i ] \hat {y} _ {l} (\pi [ i ]) | \boldsymbol {Z} [ i ] \}}{E \{\hat {T} (\pi [ i ]) | \boldsymbol {Z} [ i ] \}} \tag {10}
$$

Policy [ ] specifies optimal bitrate by selecting the bitrate, π iwhich minimizes the value of Equation (10) among all available bitrates for chunk .

iThe workflow of Elephanta is shown in Figure 4. Elephanta utilizes buffer occupancy and bandwidth prediction for the next video chunk selection. To calculate the expected bandwidth for the next video chunk, Elephanta utilizes the average download time from a horizon of several past chunks. Based on the constraint settings, Elephanta calculates driftplus-penalty value according to Equation (10) for all the bitrates of the next chunk. Then Elephanta downloads the optimal bitrate and updates the buffer occupancy when the chunk is downloaded.

The detail of the algorithm design is shown in Algorithm 1. The specific QoE functions can be updated by adjusting the corresponding parameter . Elephanta avoids extra computaαtion for parameter updates when the QoE function changes. The overhead is to maintain the virtual queues Z and calculate $\mathcal { G } [ i ]$ times (number of bitrates) for each chunk selection.

Algorithm 1 Bitrate Selection Under QoE Diversity   
1: initialize virtual queues $Z_{bs}$ , $Z_{re}$ , $Z_{bo}$ ;
penalty functions for bitrate switch $y_{bs}$ , rebuffering $y_{re}$ ,
buffer occupancy $y_{bo}$ according to Equation (11), (12)
and (13);
all available bitrates r for the video;
utility function $y_{0}$ according to Equation (14);
constraints for penalties $c_{bs}$ , $c_{re}$ , $c_{bo}$ ;
set i = 0, default QoE function parameters $\alpha_{1}, \alpha_{2}, \alpha_{3}$ ;
2: while i < n do
3: calculate penalties $y_{bs}[i]$ , $y_{re}[i]$ , $y_{bo}[i]$ for all bitrates;
4: select bitrate $r^{*}$ for chunk i that minimizes G[i] according to Equation (10);
5: download chunk c[i] with bitrate $r^{*}$ ;
6: calculate $Z_{bs}[i+1]$ , $Z_{re}[i+1]$ , $Z_{bo}[i+1]$ using Equation (5)
7: update buffer occupancy, virtual queues $Z_{bs}$ , $Z_{re}$ , $Z_{bo}$ ;
8: $i = i + 1$ 9: update $\alpha_{1}, \alpha_{2}, \alpha_{3}$ ;
10: end while

# B. Penalty and Utility Formulation

Note that the definition of QoE metrics may vary, and so Elephanta gives an example definition of penalties and utility, respectively.

$$
y _ {b s} [ i ] = \alpha_ {1} * e ^ {| c [ i ] - c [ i - 1 ] |} \tag {11}
$$

$$
y _ {r e} [ t ] = \alpha_ {2} * [ 1 - I (b u f (t)) ] \tag {12}
$$

$$
y _ {b o} [ t ] = \alpha_ {3} * b u f (t) \tag {13}
$$

$$
u [ i ] = \ln (s [ i ]) \tag {14}
$$

where $I ( x ) = 1$ when $x \ > \ 0 _ { ; }$ , otherwise, $I ( x ) = 0 ;$ is I x x > I xchunk index, [ ] is the chunk bitrate of , and $b u f ( t )$ is c i ibuffer occupancy at time . All the parameters $\alpha _ { 1 } , \ \alpha _ { 2 }$ t, and $\alpha _ { 3 }$ t α αare weighted on penalties and can be adjusted according αto QoE diversity. The characteristic eliminates the effects of parameter , so we set $V = 1$ .

V VElephanta chooses the penalty of bitrate switch as an exponential function Equation (11). The penalty generated by adjacent chunks increases significantly when the bitrate changes violently, hence Elephanta keeps conservative bitrate switch. Elephanta counts rebuffering rate as the penalty in Equation (12), i.e., the number of rebuffering events. The penalty of buffer occupancy is defined as a linear function of buffer occupancy ( ). To calculate utility $u [ i ]$ comparable to penalties, we define it as a logarithmic function of the size of chunk .

iElephanta sets constraints for bitrate switch, rebuffering, and buffer occupancy by adjusting 1, 2, and 3. Large weight α α αresults in a small penalty. For example, a larger $\alpha _ { 1 }$ generates αa larger penalty of bitrate switch. Thus, to satisfy constraint $\overline { { y } } _ { b s } \leq c _ { b s }$ , the value of $| c [ i ] - c [ i - 1 ] |$ tends to be small.

c c i c iWe analyze the performance of Elephanta under a sample video. The video is encoded in 10 bitrate levels with 20 minutes video length. Each chunk has a length of 4 seconds. In Elephanta, the penalty and utility functions are defined as Equation (11), (12), (13), and (14). We set the initial constraint of each penalty as the expected upper bound in the renewal system. The default constraints are as follows: $c _ { b s } =$ $\begin{array} { r } { \frac { e ^ { m } } { T _ { s u p } } , c _ { r e } = \frac { 1 } { T _ { s u p } } , c _ { b o } = \frac { b _ { m a x } } { T _ { s u p } } } \end{array}$ Tsup em Tsup Tsup , where $\begin{array} { r } { T _ { s u p } = \operatorname* { m i n } \left( \frac { s [ m ] } { s [ 1 ] } , B u f \right) } \end{array}$ , c , c T , Bufdenotes the upper bound of expected download time and $m = 1 0$ .

![](images/4c599aa130af0e22ae884e5ceb98d7a5d795d292bb778e3b01c2d157b8794b0e.jpg)



(a)

![](images/7a83ad16b192d699248a15bf836c12b102d0d7e31b965410d698f34c5ab46875.jpg)



(b)

![](images/ef5db95567592b1ed14402351c320bcee9a55724715aa576235fc0fab4418c49.jpg)



(c)

![](images/930b74b1842fde79974ae2f5e754e11d55d8d5e6e78ec336be36fb3380f6ddd2.jpg)



(d)   
Fig. 5. Performance comparison between BMS and BOLA. Figure (a) shows cumulative buffer stability (buffer st.) with time; Figure (b) shows bitrate selection of video chunk; Figure (c) shows cumulative bitrate switch (buffer sw.) for video chunks; Figure (d) shows buffer occupancy with time.

TABLE I COMPARISON FOR DIFFERENT FORMATS OF BITRATE SWITCH 

<table><tr><td>Function Format</td><td>AvgBitrate</td><td>BitrateSw</td><td>Rebuf</td></tr><tr><td> $|c[i] - c[i-1]|$ </td><td>7.2</td><td>400</td><td>0</td></tr><tr><td> $ln\{|c[i] - c[i-1]| + 1\}$ </td><td>7.3</td><td>697</td><td>0</td></tr><tr><td> $e^{|c[i] - c[i-1]|}$ </td><td>7.2</td><td>154</td><td>0</td></tr></table>

The calculation of average bitrate (AvgBitrate), bitrate switch (BitrateSw), rebuffering events (Rebuf) is as follows:

$$
A v g B i t r a t e = \frac {\sum_ {i = 0} ^ {n - 1} c [ i ]}{n} \tag {15}
$$

$$
B i t r a t e S w = \sum_ {i = 1} ^ {n - 1} | c [ i ] - c [ i - 1 ] | \tag {16}
$$

$$
R e b u f = \sum_ {t} r e [ t ] \tag {17}
$$

where $r e [ t ] = 1$ if $b u f ( t ) = 0$ and $f ( t - 1 ) > 0$ when $t > 0 ;$ re t; otherwise, $r e [ t ] = 0 .$ .

# C. Verifying Different Penalty Formats

The definition of penalty and utility functions may be diverse in the real world. To analyze the sensitivity of definitions, we take the bitrate switch as an example. Besides the penalty function in Equation (11), we also test two other kinds of penalty functions of bitrate switch. The results are shown in Table I. From the results, the different formats of penalty result in different performances of QoE metrics. The exponential function achieves the lowest bitrate switch, while the logarithmic function holds the largest bitrate switch. The results show that bitrate switch varies among different definitions, depending on the gradient of the function.

# D. Buffer Occupancy vs. Buffer Instability

Buffer occupancy of the video player has been an important factor in improving adaptive video streaming [14], [25]. In [14], buffer occupancy is used directly to control bitrate selection. While BOLA [6] uses buffer instability as the optimization target. We revisit the use of buffer stability in BOLA and compare its performance to buffer occupancy. In our experiment, the video is segmented into 300 chunks, each of which is four seconds. Each chunk is stored in 10 copies of different bitrate $b [ 1 ] , b [ 2 ] , \cdots , b [ 1 0 ]$ . The buffer size is b , b , , b60 seconds. We measure the buffer occupancy as the time length of chunks in the buffer. The buffer occupancy at time is denoted as $b u f ( t )$ t, where  is the time since play. We meabuf t tsure the bitrate of chunk  as $c [ i ] \in \{ b [ 1 ] , b [ 2 ] , \cdot \cdot \cdot , b [ 1 0 ] \}$ $( 1 \leq i \leq 3 0 0 )$ .

iMeanwhile, based on the recorded bandwidth and bitrates, we design a simple bitrate maximization selection (BMS) method. Given expected future bandwidth from the last chunk , BMS chooses the largest bitrate of the next video chunk i+1 with expected buffer occupancy $b u f _ { t _ { i + 1 } } > 0$ . We measure i buf >bitrate and bitrate switch for all chunks. The rebuffering and buffer instability is counted in every second while playing the video.

Figure 5 (a) shows the buffer stability comparison of BOLA and BMS. We can see that both BOLA and BMS can achieve high stability. BOLA achieves slightly high stability than BMS since buffer stability is the optimization target of BOLA. Figure 5 (b) shows the bitrate comparison. We can see that BMS achieves a higher bitrate than BOLA for most of the time. The average bitrate of BMS is 12 6% higher than BOLA. .Figure 5 (c) shows the bitrate switch comparison. We can see that BMS achieves a lower bitrate switch than BOLA for most of the time. On average, the bitrate switch of BMS is 72 9% .lower than BOLA. Figure 5 (d) shows the buffer occupancy comparison. We can see that BOLA has two rebuffering events, and BMS has no rebuffering events. However, we find that BMS has a much lower buffer occupancy than BOLA most of the time, which also explains why BMS has a higher average bitrate.

TABLE II CHARACTERISTICS OF NETWORK THROUGHPUT TRACES, AVERAGE BANDWIDTH AND STANDARD DEVIATION (Mbps) IN OUR EXPERIMENTS 

<table><tr><td>Network type</td><td>Avg.</td><td>Std.</td></tr><tr><td>4G/LTE</td><td>10.03</td><td>7.56</td></tr><tr><td>Broadband</td><td>7.51</td><td>8.23</td></tr><tr><td>HSDPA</td><td>2.00</td><td>1.05</td></tr></table>

From the results, we can see that QoE metrics on bitrate switch and average bitrate can still be improved. The buffer instability of BOLA did not gain better QoE metrics, while the buffer occupancy of BMS remained low in the calculation. We conclude that buffer occupancy is important for QoE improvement than buffer instability.

# V. EVALUATION

In this section, we experimentally evaluate Elephanta by subjective tests from real users and emulation-based tests under real-world throughput traces. The results answer the following questions: 1) Can Elephanta address QoE diversity well in the real video player? 2) How does Elephanta perform compared to existing ABR algorithms? 3) How do users watch videos via Elephanta for their preferences, and are they confused, or do they feel annoyed by the potential adjustment?

# A. Experiment Setup

We begin with experiment settings in our experiments, including 1) network throughput traces, 2) video parameters, 3) configuration of ABR algorithms, and 4) definition of quantized QoE under diversity.

# 1) Input Parameters:

Network traces: We collect real-world network bandwidth traces from the Internet, including eight months 3 /HSDPA [11] and broadband network Gtraces (FCC) [12]. To get sufficient 4  data for G/LT Eevaluation, we measure the network traces on our own. Table II shows the characteristics of throughput traces.

Video parameters: For emulation-based video playback experiments, we use the “Envivio-Dash3” video from the DASH-246 JavaScript reference client. The video is encoded with 6 bitrate levels {300 kbps, 750 kbps, 1200 kbps, 1850 kbps, 2850 kbps, and 4300 kbps}, which corresponds to video modes in {240, 360, 480, 720, 1080, and 1440} p. The video consists of 48 chunks, each with 4 seconds length. For experiments of watching videos using real video player dash.js, we use another video from DASH (Big Buck Bunny), which ranges from 254 kbps to 14931 kbps. Specifically, we use bitrate levels for real player evaluation in the algorithm, approximating video chunk size by its length multiplying its bitrate level. While in the emulation, we use real video sizes that are known beforehand to calculate the expected video chunk

![](images/6855e0593653dd2fa028f20e21ab480c6cce7febd0404eca7809e5d453a4a72a.jpg)



Fig. 6. Video chunk size of the sample video Big Buck Bunny in dash.

download time in the algorithm. As shown in Figure 6, the standard size is calculated by the corresponding bitrate level and time length. The difference between the real size and standard size is not big, but using the real size can help predict expected download time a bit better.

2) Algorithms and QoE Metrics: We compare existing ABR algorithms in our experiment:

Elastic, a rate-based algorithm [15] that selects the maximal bitrate under expected future bandwidth, e.g., predicting future bandwidth using the bandwidth from the last video chunk.   
BB, we use the buffer-based algorithm [14] and set the buffer reservoir as 6 and the cushion length as 30 . s sSpecifically, BB will select the lowest bitrate if the buffer occupancy is below 6s and select the highest bitrate if it is larger than 36 .   
s BOLA, a buffer-based ABR that maximizes average bitrate and buffer stability, proposed by Spiteri et al. [6].   
• MPC [5], incorporating buffer occupancy and future bandwidth prediction to select bitrate that maximizes QoE in expectation of all states for the 5 future video chunks. Specifically, we use Robust MPC in our experiment. Robust MPC uses harmonic mean to predict future bandwidth considering the max prediction error seen in the past 5 video chunks.   
Pensieve, a reinforcement learning-based approach. We use the code provided by the author [7]. We re-train the model under our dataset and QoE parameter settings for evaluation.

We calculate quantized QoE under diversity using the function: $Q o E = A v g B i t r a t e - P _ { r e } * R e b u f - P _ { s m } * B i t r a t e S w$ . The QoE AvgBitrate P Rebuf P BitrateSwAvgBitrate and BitrateSw are calculated in  , correspond-M bpsing to bitrate levels in the videos (constant bitrate). However, Rebuf is calculated in rebuffering rate for real video player evaluation and time length (second) for emulation. We use two types of settings in the experiments: specific and overall parameters.

• For the overall parameter setting, we set $P _ { r e } = 4$ and $P _ { s m } = 1$ P, which means the penalty of 1 second Prebuffering corresponds to penalty of 4   bitrate switch.   
• For the specific parameter setting, we assume the parameters $P _ { r e }$ and $P _ { s m }$ obey Gaussian distribution $N ( \lambda , ( \mu \lambda ) ^ { 2 } )$ P P, which represents user QoE diversity.

For the calculation of the specific QoE, we set $\lambda = 4$ for $P _ { r e }$ and $\lambda = 1$ for $P _ { s m }$ λ(this is the same for overall P λ Pparameter settings, representing an average value on the parameter). We use the parameter $\mu$ to denote different μlevel of QoE diversity. Intuitively, a large value of $\mu$ μindicates large QoE diversity. In our experiment, we use ranging from 0 to 0 9.

μ .3) Choosing Video Player and Equipment Setting:

We use Mahimahi [27] to emulate network conditions under the throughput trace dataset and video playback in the experiments on comparing the performance for the ABR algorithms. We implement and re-construct the code of existing ABR algorithms in python 3. We run the emulation experiments with python 3 5 4 on Windows . .10 1 operating system, with CPU Intel(R) Core(TM) .i5-6200U @ 2.30GHz 2.40 GHz.   
• We implement Elephanta in $d a s h . j s$ for evaluating the performance of Elephanta on adapting QoE diversity and subjective experiments. We publish Elephanta as a web page on a Linux server (Ubuntu 16.04.6 LTS). The online version of Elephanta can be accessed at [28].

# B. Implementation in dash.js

We implement Elephanta in dash.js [28], a reference video player client implementation of DASH. Besides, we make modifications to fit dash.js to our model. The implementation of Elephanta can be found at [29]. The DASH video player checks buffer occupancy every second to decide if the current bitrate should be changed. It means that bitrate selection will happen when a video chunk is being downloaded and lead to bitrate execution delay or even re-downloading of previous chunks. We modify the source code to ensure that the bitrate decision function is executed only when the former chunk finishes downloading.

Elephanta provides QoE perception interfaces by adjustable parameters on corresponding metrics that are visible to users. Elephanta monitors the change of parameters when the video plays. Once detecting the parameter updates, the QoE monitor sends the new parameters to the ABR controller, then the ABR controller selects the target bitrate of the next chunk and sends the request to the video servers.

To adapt to QoE diversity, we set three flexible constraint weights $w _ { b s } , w _ { r e } , w _ { b o }$ for bitrate switch, rebuffering and buffer w , w , woccupancy. The constraint weights range from 0% to 100%. The weights are initialized by the video player and can be adjusted by users while watching videos. Accordingly, 1, 2 and $\alpha _ { 3 }$ are updated as follows: $\alpha _ { 1 } = w _ { b s } * \alpha _ { 1 } , \alpha _ { 2 } = w _ { r e } * \alpha _ { 2 } ,$ , $\alpha _ { 3 } = w _ { b o } * \alpha _ { 3 }$ .

w αWe set the default constraints $c _ { b s } , \ c _ { r e } , \ c _ { b o }$ as 1. Default weights $w _ { b s } , w _ { r e } , w _ { b o }$ c c care set to 100% unless explicitly pointed w w wout. We use a linear function for penalty of bitrate switch, as shown in Table I. We believe Elephanta can be easily used in future versions since the total modifications are no more than 500 lines of JavaScript code.

The evaluation is performed in the following aspects: First, we show the details of how Elephanta adapts to QoE diversity and real user evaluation in a real video player. Second,

TABLE III QoE METRICS UNDER QoE DIVERSITY 

<table><tr><td> $(\alpha_1, \alpha_2, \alpha_3)$ </td><td>AvgBitrate</td><td>BitrateSw</td><td>Rebuf</td><td>AvgBuf</td></tr><tr><td>(0, 0, 1)</td><td>6.9</td><td>4.42</td><td>2</td><td>5.6</td></tr><tr><td>(0, 1, 0)</td><td>6.1</td><td>4.50</td><td>0</td><td>8.5</td></tr><tr><td>(0, 1, 1)</td><td>6.6</td><td>4.56</td><td>0</td><td>6.3</td></tr><tr><td>(1, 0, 0)</td><td>5.6</td><td>1.39</td><td>0</td><td>10.1</td></tr><tr><td>(1, 0, 1)</td><td>6.9</td><td>3.58</td><td>2</td><td>5.4</td></tr><tr><td>(1, 1, 0)</td><td>6.6</td><td>3.12</td><td>0</td><td>6.1</td></tr><tr><td>(1, 1, 1)</td><td>6.8</td><td>4.41</td><td>0</td><td>6.0</td></tr></table>

TABLE IV QoE FUNCTION SCHEMES 

<table><tr><td>Scheme</td><td> $(\alpha_1, \alpha_2, \alpha_3)$ </td><td>AvgBitrate</td><td>BitrateSw</td><td>Rebuf</td><td>AvgBuf</td></tr><tr><td>HR</td><td>(0.6, 0.1, 0.6)</td><td>7.2</td><td>4.04</td><td>2</td><td>4.5</td></tr><tr><td>Smooth</td><td>(1, 1, 0.2)</td><td>6.73</td><td>4.41</td><td>0</td><td>7.2</td></tr><tr><td>Balance</td><td>(1, 0.3, 0.5)</td><td>6.9</td><td>4.54</td><td>1</td><td>6.1</td></tr></table>

we conduct emulation experiments of Elephanta comparing it to prior ABR algorithms under fixed QoE function and QoE diversity.

# C. Real Video Player Evaluation

1) QoE Diversity Driven Adaptation: We provide three kinds of constraints bitrate switch (BitrateSw), rebuffering (Rebuf), and buffer occupancy (Buf) by default. A user can set constraint weights $\alpha _ { 1 } , \alpha _ { 2 }$ , and $\alpha _ { 3 }$ from 0 to 100% according α α αto his preference. We show the performance of Elephanta for several kinds of constraint combinations $( \alpha _ { 1 } , \alpha _ { 2 } , \alpha _ { 3 } )$ .

α , α , αWe record the average bitrate, bitrate switch, rebuffering times, and average buffer occupancy for each constraint setting. Detailed results are summarized in Table III, which shows that different combinations result in different network performances. In our experiment, the QoE metrics are effectively controlled by corresponding constraints:

• When $\alpha _ { 1 }$ is 1, the bitrate switch is 29 9% lower than $\alpha _ { 1 } = 0$ αon average.   
α• When $\alpha _ { 2 }$ is 1, no rebuffering occurs on average while αrebuffering occurs 1 33 times when $\alpha _ { 2 } = 0$ .   
• When $\alpha _ { 3 }$ . αis 1, the average bitrate is 11 5% higher than $\alpha _ { 3 } = 0$ α .. Intuitively, the bitrate level is 0 7 higher.

The constraints of Elephanta can be set according to QoE diversity. To intuitively show how to set the constraints, we take a specific scenario like watching a football video replay and recommend constraint settings for different users. As shown in Table IV, we set different groups of constraints across users for comparison. Elephanta performs well for the following different groups of users: High Resolution (HR). Users usually require high-quality frames that capture wonderful moments. We can set constraints with low buffer occupancy, low rebuffering, and no bitrate switch. Smooth. For a user who requires fluent moments. The video is more likely to be played with no rebuffering. Balance. The users may tend to watch the video with little or no bitrate switch for a no flickering experience.

2) Online QoE Perception and Adaptation: We show the demo page of Elephanta, which supports adjusting constraints online. The volunteer can change his preference by adjusting the constraints while watching the video.

TABLE V SUBJECTIVE EXPERIMENTS BY INVITING 21 VOLUNTEERS WATCH ONLINE VIDEOS IN DASH.JS USING ELEPHANTA 

<table><tr><td>Questions</td><td>Strongly Disagree</td><td>Disagree</td><td>Neutral</td><td>Agree</td><td>Strongly Agree</td></tr><tr><td>1.1 Elephant auto is helpful.</td><td>0</td><td>2</td><td>6</td><td>10</td><td>3</td></tr><tr><td>1.2 Elephant auto is responsive to network dynamics.</td><td>1</td><td>1</td><td>0</td><td>8</td><td>11</td></tr><tr><td>2.1 The interaction is helpful.</td><td>0</td><td>2</td><td>4</td><td>8</td><td>7</td></tr><tr><td>2.2 Elephant is responsive to your interaction when watching video.</td><td>0</td><td>2</td><td>0</td><td>12</td><td>7</td></tr><tr><td>2.3 The interaction via Elephant can reflect your preference.</td><td>0</td><td>2</td><td>3</td><td>9</td><td>7</td></tr><tr><td>2.4 Elephant with interaction is better for you than Elephant auto.</td><td>2</td><td>4</td><td>5</td><td>5</td><td>5</td></tr><tr><td>2.5 You would like to do the interaction for preference.</td><td>3</td><td>3</td><td>3</td><td>7</td><td>5</td></tr><tr><td>2.6 You would like to set different weights for different video types.</td><td>1</td><td>3</td><td>2</td><td>3</td><td>12</td></tr></table>

![](images/1fe777741d1c0204a115e578d79798e5895facf05f1765f4936b911986bbd9bb.jpg)



(a)

![](images/2234280ff7719435f1f8ca902a94933e2fa0aca5db00d6148d6e0ee2185838ab.jpg)



(b)

![](images/f27319a9866719be8d5eddf8e7c307f4668a37106a52d79cd932bfa8a8e47941.jpg)



(c）  
Fig. 7. Example of online QoE function tuning and perception. (a) The buffer occupancy constraint weight is high and the video plays at low buffer occupancy with a high bitrate. (b) The bitrate switch constraint weight is high. The bitrate maintains at a low level. Meanwhile, buffer occupancy goes high. (c) Rebuffering and buffer occupancy weights are set high. The video plays fluently with no rebuffering and keeps a low buffer occupancy.

As shown in Figure 7, we record the bitrate and buffer occupancy to show how well Elephanta adapts to QoE diversity online. We take one video track for illustration. The volunteer has three different choices of QoE preference: 1) The user wants to watch a high bitrate video. Thus he sets the constraint weight of buffer occupancy higher than other constraints. 2) The user aims to reduce the bitrate switch. The user increases the constraint weight of the bitrate switch. 3) The user changes the rebuffering constraint to high and sets a medium constraint for buffer occupancy to get fluent video streaming. The diagram shows that the constraints on metrics take effects as soon as they are changed.

3) Subjective Experiment From Real Users: We conduct online experiments by inviting 21 volunteers for watching videos via Elephanta and existing ABR algorithms implemented in dash.js [13], i.e., BB [14] and BOLA [6]. Specifically, we provide Elephanta auto (we adjust the parameters automatically in the algorithm) and Elephanta with interaction (online parameter adjustment) in the experiments. We provide the reference video (Big Buck Bunny) from Akamai in the experiment (contains 10 bitrates, 250 to 15 @ 4 ) kbps M bps Kand show the bitrate of the video on the screen like in Figure 7. The code is available in an open repository at [28]. Considering the complexity of evaluating subjective feelings from the volunteers, we do not ask them to give quantified scores on QoE and QoE diversity. Rather, we invite them to give scores for several questions we asked them before the experiment. The volunteers are required to watch videos using the ABR algorithms and provide scores to the questions after viewing all the videos. We summarize the questions and the scores in Table V.

We obtain the following insights to understand adaptation to QoE diversity for real users.

The effectiveness of Elephanta. We provide two versions of Elephanta in the online experiment and ask the

volunteers to give scores on them, comparing them to pilot ABR algorithms in dash.js. For Elephanta auto, we provide preset constraints. While for Elephanta with interaction, one can adjust the QoE parameters when watching videos. From the result in Table V, 19 21 /volunteers agreed that Elephanta is responsive to network dynamics, and the interaction is responsive. While 13 21 and 15 21 of them think Elephanta is helpful, / /compared to pilot ABR algorithms and video viewing experiences in daily life. We also ask volunteers who disagree or feel neutral on questions 1 1 and 2 1 for . .potential improvement. Several volunteers said the video could stall even when the bitrate shown on the screen is the lowest (which we conjecture is mainly due to poor network conditions). While others indicated that they did not care whether the video is played under ABR or fixed bitrate strategy. These answers reflect the complexity of the user’s preference and implicate the diverge demands of users for video viewing. We believe the results can help both researchers and video providers promote video delivery strategy under QoE diversity, e.g., providing both ABR and fixed bitrate strategies in video players.

User’s changing preference in video viewing. We provide interfaces for volunteers adjusting the parameter in Elephanta while watching videos. And they give scores on questions 2 2 and 2 3 in Table V. 19 21 of volunteers . . /agree that Elephanta is responsive to the interaction, and 16 21 of them (strongly) agree that the interaction can /reflect their preferences.   
User’s willingness to conduct interaction in Elephanta. We also ask the volunteers whether they would like to use different parameter settings to fit their preferences. As shown in question 2 4 in Table V, most of them .(15 21) tend to set different parameters for different types of videos. This is mainly due to the strong impact of the

![](images/e6cb404c8150aa06078b919e65b02842b38e95b4d170332772e3b1e8cd5ff35e.jpg)



4G/LTE dataset

![](images/720cef96f846f58f54002a005d446f3d5ba1d99c04550d0f29e97fdd26edfcb2.jpg)



FCC broadband dataset

![](images/e154015c6f8033bbe78c0441c890d7b31c696685e5adb30e700651f486f40dc9.jpg)



Norway HSDPA dataset   
Fig. 8. Comparing Elephanta to existing ABR algorithms with overall parameter QoE function on 4G/LTE, broadband and 3G/HSDPA networks.

TABLE VI COMPARISON OF AVERAGE QoE BETWEEN ELEPHANTA (ELE.) AND EXISTING ABR ALGORITHMS UNDER THE FIXED QoE FUNCTION (OVERALL PARAMETERS) 

<table><tr><td>Network</td><td>BB</td><td>Elastic</td><td>BOLA</td><td>MPC</td><td>Pensieve</td><td>Ele.</td></tr><tr><td>4G</td><td>3.01</td><td>3.17</td><td>3.47</td><td>3.68</td><td>3.87</td><td>3.73</td></tr><tr><td>HSDPA</td><td>0.03</td><td>0.31</td><td>0.49</td><td>0.93</td><td>1.09</td><td>0.58</td></tr><tr><td>Broadband</td><td>1.59</td><td>1.43</td><td>1.76</td><td>2.31</td><td>2.36</td><td>1.94</td></tr></table>

video types on the user’s engagement [1]. E.g., users tend to watch live videos in high bitrate.

Potential annoyance from user interaction. We compare two versions of Elephanta in the experiment, and the results to question 2 4 are shown in Table V. 10 21 of . /them would like to use Elephanta with interaction, while 6 21 of them would like to use Elephanta auto mainly to avoid the interaction that irritates them. It implicates that to deal with QoE diversity, e.g., using Elephanta, it’s better to provide two versions of ABR. One can adapt QoE parameters to different videos, while the other provides an interface for users to adjust the parameters online.

# D. Video Emulation-Based Evaluation

To compare Elephanta with prior ABR algorithms, we conduct Mahimahi emulator [27] and network throughput traces from the real world for evaluation.

1) Performance Under Fixed QoE Function: We first set Elephanta with a fixed notion of parameters in the QoE function to compare the performance. In our experiment, the parameters of Elephanta are set as $\alpha _ { 1 } = 1 . 5 , \alpha _ { 2 } = 0 . 8 .$ and $\alpha _ { 3 } = 0 . 6$ α . α .. We choose 500 throughput traces evenly from α .the dataset and emulate video playback under the network traces with overall parameters $( P _ { r e } = 4$ and $P _ { s m } = 1 )$ in P Pthe ABR algorithms. We also use the overall parameters to calculate the average QoE. The result is shown in Figure 8. From the results, we observe that Elephanta outperforms BOLA, BB, and Elastic, but it performs poorly compare to MPC and Pensieve. We also list the average QoE comparison in Table VI. The results show that Elephanta outperforms BB, Elastic, and BOLA across all network types. But for broadband and HSDPA dataset, Elephanta performs poorly compare to Pensieve and MPC. From the results in Table VI, Elephanta achieves 90% performance of (Robust) MPC in overall when using overall parameters $( \mu = 0 )$ .

![](images/3b9efad24cde2985b2a4802a87095b02cf4cd5c3d081111d4680c3c969957bdd.jpg)



Fig. 9. QoE improvement of Elephanta over existing ABR algorithms under QoE diversity, µ ranges 0 to 0.9.

2) Performance Under QoE Diversity: We also conduct experiments on the performance of baseline ABR algorithms (BOLA, MPC, and Pensieve) over different levels of $\mu$ (QoE μdiversity). We randomly select 500 throughput traces from each network type. We use specific parameters to calculate average QoE, where $\mu$ ranges uniformly from 0 1 to 0 9. μ . .For bitrate selection in ABR algorithms, we use specific parameters for Elephanta, while for others, we use overall parameters.

The result is shown in Figure 10. Given less diversity on user QoE $( { \mathrm { e . g . , ~ } } \mu ~ \leq ~ 0 . 1$ in our experiment), Elephanta μ .does not achieve better average QoE than MPC and Pensieve. However, both MPC and Pensieve suffer average QoE decrease when $\mu$ increases, while Elephanta does not. From the result, we observe that Elephanta outperforms MPC and Pensieve when $\mu \geq 0 . 2$ .

μ .We also aggregate average QoE results with $\mu$ $\{ 0 . 0 , 0 . 1 , \cdot \cdot \cdot , 0 . 9 \}$ . For the evaluation of each $\mu ,$ μ we also . , . , , . μchose 500 network traces for each network type listed in Table II. We show the cdf plot of QoE improvement for Elephanta over baseline ABR algorithms, as shown in Figure 9. Given that we include QoE results under $\mu = 0 ;$ , μElephanta outperforms MPC in 60% network traces, and achieves QoE improvement by 7% over MPC and 3% over Pensieve. We believe Elephanta can adapt well to network changes to achieve maximal QoE across all levels of QoE diversity.

![](images/7d785605dc2d922a5fa1d612753429aedb4df6c5e1a16b103c8d94d99f27e5b9.jpg)



Fig. 10. Average QoE comparison with existing ABR algorithms under different levels of QoE diversity.

# E. Takeaways

We summarize several takeaways from our evaluation results.

• By implementing Elephanta with real video player dash.js, Elephanta can effectively decide video bitrate according to QoE diversity.   
• By emulating network throughput traces, the average QoE of Elephanta achieves 90% of MPC with fixed QoE weights (overall parameters). When QoE diversity is high, e.g., $\mu \geq 0 . 2$ , Elephanta outperforms all existing ABR μ .algorithms. As a result, Elephanta outperforms MPC by 7% and Pensieve by 3% QoE for $\mu$ ranging from 0 to 0 9.   
.• By subjective experiments, we provide 21 volunteers with Elephanta for online video viewing. Given most of them agree that Elephanta is helpful and responsive, 12 21 volunteers are willing to conduct the interaction of /Elephanta for their preferences, while 6 21 of them are /not. We also acknowledge from the result that providing multi-versions of ABR algorithms may benefit in a realworld deployment. For example, we can provide user interaction-based Elephanta or auto-tuning parameterbased Elephanta according to different video types.

# VI. DISCUSSION

Given the evaluation results, there are several questions on Elephanta that remain to be discussed like 1) How do individual components QoE metrics behave in existing ABR algorithms under QoE diversity? 2) By constraining on buffer occupancy, will Elephanta face more risks in rebuffering? 3) To what degree do users’ preferences diverge in the real world?

# A. Performance of Individual QoE Components

To further study the ABR performance of individual QoE components under QoE diversity, we take extensive experiments on the specific QoE metrics for Elephanta, Pensieve, BOLA, and MPC. We randomly select 1000 throughput traces as test sets from HSDPA, broadband, and 4 data set. We take the experiments on the whole test set under each QoE diversity parameter $\mu ,$ ranging equally from 0 1 to 0 7.

![](images/cffb6a762a664a7acd350447c10942c26ebb89b673f7a71dd7b33372d30934ca.jpg)



Fig. 11. Comparing Elephanta to MPC and Pensieve across individual QoE metrics. Average values of individual QoE metrics of each ABR algorithm are listed. Error bars denote the standard deviation on the normalized value.

![](images/c2ce7d72422122aba47f6dfb620d02f2d9e504e87d1875df5c01c6992a117672.jpg)



Fig. 12. An example of buffer behavior with network changes of ABR algorithms.

μ . .The result is shown in Figure 11. The average QoE values of Elephanta, BOLA, Robust MPC, and Pensieve are 2 80 2 16 2 57, and 2 54. From the rebuffering value, we can . , . , . .learn that BOLA experiences a large rebuffering penalty, and thus results in significant loss of QoE. However, the other ABR algorithms achieve low rebuffering values. Specifically, Elephanta achieves the highest average bitrate and lowest rebuffering value with little smoothness penalty increase.

# B. Buffer Behavior

We find Elephanta may experience more rebuffering time if we set the constraint on buffer occupancy in the experiments. To make an in-depth study of the buffer behavior, we take the experiment on comparing changes of buffer occupancy of BOLA, MPC, Pensieve, and Elephanta. We plot the bandwidth and buffer occupancy against the time of the ABR algorithms, as shown in Figure 12. Under the given network trace, Elephanta achieves the largest QoE value (higher average bitrate) over other ABR algorithms. From the buffer occupancy, we can see Elephanta performs the lowest average buffer occupancy. At time 120 , when the network srecovers, Elephanta controls the buffer occupancy at a lower level by selecting a higher bitrate. Considering a situation where the bandwidth is too low, we can set a reservoir for buffer occupancy to avoid rebuffering for sudden bandwidth drops (this is also an important technique in buffer-based ABR, like BB [14]). For example, we use the idea in Elephanta and set the reservoir buffer as 8 seconds for the experiment. Though the buffer occupancy of Elephanta deceases when the network drops suddenly at time 140 to 160 , it avoids unnecessary rebuffering.

![](images/9db00d8be8e53f3247c799a3ac0f97a2964427035a706c97f406ac955ce7c98c.jpg)



Fig. 13. QoE diversity among volunteers.

The buffer occupancy is necessary for us to control the average bitrate in our design. Intuitively, a low constraint on buffer occupancy will drive the algorithm to select a higher bitrate, while a higher constraint will not. Given the diversity of user QoE, some users may want to watch extremely high bitrate videos (a low constraint on the buffer), while others may accept to watch a video with high bitrate (but not the highest). Without constraining buffer occupancy, the algorithm will select a video bitrate that is a bit lower to avoid potential rebuffering and bitrate switch. It cannot deal with QoE diversity, such as a user who wants to watch a video with extremely high bitrate and is patient with video caching (for instance, waiting 1 min for video rebuffering). We believe constraining buffer occupancy helps us to deal with more situations regarding user preference.

# C. Diversity Real Users’ Preference

To evaluate the QoE diversity among different users, we generate three tracks of the same video under three QoE schemes, i.e., $( \alpha _ { 1 } , \alpha _ { 2 } , \alpha _ { 3 } )$ from {(1 1 0) (0 1 1) (1 0 1)}. α , α , α , , , , , , , ,We invite seven volunteers to watch the video tracks and give scores for each video track. The result of the overall scores is shown in Figure 13. We observe that preference on video tracks is quite different across volunteers. Given that the results implicate huge diversity for users’ preferences in the real world, we believe Elephanta takes a step in helping the user adjust his QoE preference online for better video viewing experience.

# VII. RELATED WORK

# QoE Metrics Study

The metrics affecting QoE in video streaming have been widely studied recently. The user-perceived video quality, such as buffering ratio, average bitrate, join time and rendering quality impacts user engagement and watching time [1]. Other quality metrics, such as the flicker effect, shows a negative correlation to viewing experience [30]. Some previous works attempt to infer QoE and capture QoE diversity. In [8], it measures user-viewing activities and utilizes the data to correlate into QoE function. In [31], a system for television programs is proposed for recording user preference.

# Exploiting ABR Algorithms

The performance of ABR algorithms can significantly impact user engagement [32]. Adaptive video streaming suffers from network diversity. Previously, the approaches take average bitrate as the sole factor in QoE function and promote average bitrate by predicting future bandwidth [15], [22], [23]. However, the bandwidth is difficult to predict due to various network congestions and capacities [25], [33]–[36]. To avoid QoE loss caused by inaccurate bandwidth prediction, buffer occupancy has been introduced for design. The idea is to determine the bitrate for different levels of buffer occupancy, like [14]. Another approach, BOLA [6], selects bitrate for different users based on a QoE function of a fixed weight of video buffer instability and average bitrate. Further, predictive model-based methods have become popular in recent years. MPC [5] conducts a model predictive control technique to formulate the QoE maximization problem and indexing table for efficient bitrate selection. Pensieve [7] designs the ABR algorithm from experience by utilizing modern reinforcement learning. These ABR algorithms conduct overall fixed QoE functions and result in a QoE decrease in the context of QoE diversity. To bridge the gap, our work provides QoE diversity perception schemes for edge clients by user-engaged parameter adjustment. The monitor detects a change of QoE function online and sends the feedback to the ABR controller for optimal bitrate selection.

# VIII. CONCLUSION

Promoting the quality of experience for every end-user in video streaming has raised more and more attention. Prior work has improved QoE under the context of overall user QoE function definition and optimization methods. However, prior works fail to address QoE diversity effectively in that 1) most algorithms conduct a fixed overall notion of QoE function and result in low QoE, 2) lack of an efficient online QoE optimization algorithm for specific QoE functions. To address the issue, we propose Elephanta, which conducts online QoE function perception schemes and online flexible adaptation algorithm for QoE diversity. By emulating under 1500 throughput traces, Elephanta achieves 3% and 7% QoE improvement over Pensieve and MPC, respectively. We also implement Elephanta in real video player dash.js [13]. Accordingly, we take subjective experiments from volunteers whereby most of them agree that Elephanta is helpful and responsive. We also acknowledge that 12 21 volunteers are willing to /conduct the interaction of Elephanta for their preferences, while 6 21 of them are not. It suggests that it is better /to provide a multi-version of Elephanta for all users. For example, we can provide a user interaction-based Elephanta or auto-tuning parameter-based Elephanta according to different video types.

# REFERENCES

[1] F. Dobrian et al., “Understanding the impact of video quality on user engagement,” ACM SIGCOMM Comput. Commun. Rev., vol. 41, no. 4, pp. 362–373, Aug. 2011.   
[2] Netflix. Netflix. Accessed: 2017. [Online]. Available: https://www. netflix.com/   
[3] Douyin. Douyin. Accessed: 2019. [Online]. Available: https://www. douyin.com/   
[4] Douyu. Douyu. Accessed: 2019. [Online]. Available: https://www. douyu.com   
[5] X. Yin, A. Jindal, V. Sekar, and B. Sinopoli, “A control-theoretic approach for dynamic adaptive video streaming over HTTP,” ACM SIGCOMM Comput. Commun. Rev., vol. 45, no. 4, pp. 325–338, 2015.   
[6] K. Spiteri, R. Urgaonkar, and R. K. Sitaraman, “BOLA: Near-optimal bitrate adaptation for online videos,” in Proc. IEEE INFOCOM-35th Annu. IEEE Int. Conf. Comput. Commun., Apr. 2016, pp. 1–9.   
[7] H. Mao, R. Netravali, and M. Alizadeh, “Neural adaptive video streaming with pensieve,” in Proc. Conf. ACM Special Interest Group Data Commun., Aug. 2017, pp. 197–210.   
[8] R. K. P. Mok, E. W. W. Chan, X. Luo, and R. K. C. Chang, “Inferring the QoE of HTTP video streaming from user-viewing activities,” in Proc. 1st ACM SIGCOMM Workshop Meas. Up Stack, 2011, pp. 31–36.   
[9] S. S. Krishnan and R. K. Sitaraman, “Video stream quality impacts viewer behavior: Inferring causality using quasi-experimental designs,” IEEE/ACM Trans. Netw., vol. 21, no. 6, pp. 2001–2014, Dec. 2013.   
[10] M. J. Neely, “Stochastic network optimization with application to communication and queueing systems,” Synth. Lectures Commun. Netw., vol. 3, no. 1, pp. 1–211, Jan. 2010.   
[11] P. Halvorsen. Hsdpa Dataset. Accessed: Feb. 1, 2018. [Online]. Available: http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/   
[12] F. C. Commission. (2017). Fcc Dataset. [Online]. Available: https:// www.fcc.gov/reports-research/reports/measuring-broadband-america   
[13] (2017). Dash-Industry-Forum. [Online]. Available: https://github. com/Dash-Industry-Forum/dash.js   
[14] T.-Y. Huang, R. Johari, N. McKeown, M. Trunnell, and M. Watson, “A buffer-based approach to rate adaptation: Evidence from a large video streaming service,” ACM SIGCOMM Comput. Commun. Rev., vol. 44, no. 4, pp. 187–198, 2015.   
[15] L. De Cicco, V. Caldaralo, V. Palmisano, and S. Mascolo, “ELASTIC: A client-side controller for dynamic adaptive streaming over HTTP (DASH),” in Proc. 20th Int. Packet Video Workshop, Dec. 2013, pp. 1–8.   
[16] Y. He and Y. Liu, “VOVO: VCR-oriented video-on-demand in largescale peer-to-peer networks,” IEEE Trans. Parallel Distrib. Syst., vol. 20, no. 4, pp. 528–539, Apr. 2009.   
[17] H. Guo, K.-T. Lo, Y. Qian, and J. Li, “Peer-to-peer live video distribution under heterogeneous bandwidth constraints,” IEEE Trans. Parallel Distrib. Syst., vol. 20, no. 2, pp. 233–245, Feb. 2009.   
[18] A. P. C. da Silva, E. Leonardi, M. Mellia, and M. Meo, “Chunk distribution in mesh-based large-scale P2P streaming systems: A fluid approach,” IEEE Trans. Parallel Distrib. Syst., vol. 22, no. 3, pp. 451–463, Mar. 2011.   
[19] Microsoft. (2017). Microsoft Smooth Streaming. [Online]. Available: https://www.iis.net/downloads/microsoft/smooth-streaming   
[20] Adobe. (2017). Adobe Http Dynamic Streaming. [Online]. Available: http://www.adobe.com/products/hds-dynamic-streaming.html   
[21] Apple. (2017). Apple Http Live Streaming. [Online]. Available: https://developer.apple.com/streaming/   
[22] Z. Li et al., “Probe and adapt: Rate adaptation for HTTP video streaming at scale,” IEEE J. Sel. Areas Commun., vol. 32, no. 4, pp. 719–733, Apr. 2014.   
[23] J. Jiang, V. Sekar, and H. Zhang, “Improving fairness, efficiency, and stability in HTTP-based adaptive video streaming with festive,” IEEE/ACM Trans. Netw., vol. 22, no. 1, pp. 326–340, Feb. 2014.   
[24] S. Eswaran, A. Misra, F. Bergamaschi, and T. L. Porta, “Utility-based bandwidth adaptation in mission-oriented wireless sensor networks,” ACM Trans. Sensor Netw., vol. 8, no. 2, pp. 1–26, 2012.   
[25] X. K. Zou et al., “Can accurate predictions improve video streaming in cellular networks?” in Proc. 16th Int. Workshop Mobile Comput. Syst. Appl., 2015, pp. 57–62.   
[26] D. P. Bertsekas, Dynamic Programming and Optimal Control, vol. 1, no. 2. Belmont, MA, USA: Athena Scientific, 1995.

[27] R. Netravali et al., “Mahimahi: Accurate record- and-replay for HTTP,” in Proc. USENIX Annu. Tech. Conf., 2015, pp. 417–429.   
[28] C. Qiao. (2020). Elephanta Online Test. [Online]. Available: https:// github.com/tionry/OnlineTestElephanta   
[29] C. Qiao. (2019). Elephanta Implementation. [Online]. Available: https:// github.com/tionry/Elephanta-dash.js   
[30] P. Ni, R. Eg, A. Eichhorn, C. Griwodz, and P. Halvorsen, “Flicker effects in adaptive video streaming to handheld devices,” in Proc. 19th ACM Int. Conf. Multimedia, 2011, pp. 463–472.   
[31] L. K. Ismail, A. N. Gogoi, and Y. Stupak, “Television program recording with user preference determination,” U.S. Patent 6 614 987, Sep. 2, 2003.   
[32] A. Balachandran, V. Sekar, A. Akella, S. Seshan, I. Stoica, and H. Zhang, “Developing a predictive model of quality of experience for Internet video,” ACM SIGCOMM Comput. Commun. Rev., vol. 43, no. 4, pp. 339–350, Sep. 2013.   
[33] T.-Y. Huang, N. Handigol, B. Heller, N. McKeown, and R. Johari, “Confused, timid, and unstable: Picking a video streaming rate is hard,” in Proc. ACM Conf. Internet Meas. Conf. (IMC), 2012, pp. 225–238.   
[34] K. Winstein, A. Sivaraman, and H. Balakrishnan, “Stochastic forecasts achieve high throughput and low delay over cellular networks,” in Proc. 10th USENIX Symp. Netw. Syst. Des. Implement., 2013, pp. 459–471.   
[35] Y. Zaki, T. Pötsch, J. Chen, L. Subramanian, and C. Görg, “Adaptive congestion control for unpredictable cellular networks,” ACM SIGCOMM Comput. Commun. Rev., vol. 45, no. 4, pp. 509–522, Sep. 2015.   
[36] Y. U. Kun, C. Bao, and L. I. Xing, “Internet path performance measurements using Web servers,” Qinghua Daxue Xuebao/J. Tsinghua Univ., vol. 54, no. 4, pp. 474–479, 2014.

![](images/e89572471948d17d1d97363b5314a199e6dd1a9c63361866d73e239e21dbfb40.jpg)



Chunyu Qiao (Student Member, IEEE) received the B.E. degree in software engineering from Tsinghua University, China, where he is currently pursuing the Ph.D. degree. His research interests include adaptive video streaming, user QoE study, network measurement, and big data analysis.

![](images/5bcc115e5862f8718ccd8801f107bee8c6ad019f7a0ef4301f03de983efc5110.jpg)



Jiliang Wang (Member, IEEE) received the B.E. degree in computer science and technology from the University of Science and Technology of China and the Ph.D. degree in computer science and engineering from The Hong Kong University of Science and Technology. He is currently an Associate Professor with the School of Software and TNLIST, Tsinghua University, China. His research interests include wireless and sensor networks, the Internet of Things, and mobile computing.

![](images/e561daed017608c96b404eb87839d8ece351eb008a51859204742c142df586cf.jpg)



Yunhao Liu (Fellow, IEEE) received the B.S. degree in automation from Tsinghua University, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is currently the Dean of GIX, Tsinghua University, and also a Faculty Member of CSE, MSU. His research interests include AIOT, RFID, sensor networks, and pervasive computing. He is a Fellow of the ACM.