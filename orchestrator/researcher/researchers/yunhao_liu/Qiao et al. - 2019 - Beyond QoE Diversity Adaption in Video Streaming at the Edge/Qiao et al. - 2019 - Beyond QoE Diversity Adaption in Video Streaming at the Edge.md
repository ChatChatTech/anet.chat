# Beyond QoE: Diversity Adaption in Video Streaming at the Edge

Chunyu Qiao $^{*}$ , Jiliang Wang $^{*}$ , Yunhao Liu $^{*}$ $^{\dagger}$

\*School of Software, Tsinghua University

$^{\dagger}$ Department of Computer Science and Engineering, Michigan State University

\*qiaocy16@mails.tsinghua.edu.cn, jiliangwang@tsinghua.edu.cn, †yunhao@greenorbs.com

Abstract—Adaptive bitrate (ABR) algorithms have been critical techniques for high quality-of-experience (QoE) Internet video delivery. Prior work designs ABR algorithms by conducting the overall QoE function of fixed parameters. However, the QoE of end users are diverse and video bitrate may be chosen in a misleading way when leaving out the diversity. State-of-the-art ABR algorithms like MPC, Pensieve utilize off-line modeling techniques and result in performance degradation for online QoE diversity adaption. To address this issue, we propose Elephanta, an online flexible ABR algorithm for edge users which incorporates (1) user QoE perception interface and (2) adaption algorithm with flexible parameters. To avoid overheads for updating parameters online, we model video streaming as a renewal system and formulate specific QoE function into flexible formats by setting constraints on corresponding QoE metrics. To validate parameter setting, we emulate Elephanta under 5 thousand throughput traces including FCC broadband, 3G HSDPA data set from the Internet and 4G/LTE data set collected by ourselves. Accordingly, we implement Elephanta in dash.js at client side for user test. Evaluation results show that Elephanta achieves QoE improvement by 21.1% over MPC, in part for its superior adaptability to QoE diversity.

Index Terms—QoE diversity, adaptive bitrate algorithms, video streaming

# I. INTRODUCTION

Video streaming has been the major traffic on the Internet. Cisco predicted the rise of the traffic up to 80% by the year 2019 [1]. Along with this, the demands on improving QoE have taken the front stage of video streaming. Because providing high QoE for video streaming will lead to a high rate of user engagement, while QoE decrease will result in user disengagement and loss of revenue [2]. At this moment, video providers are still making efforts to promote their service quality.

To serve for end users with different device types and heterogeneous networks, Dynamic Adaptive HTTP Streaming (DASH) has been the main video delivery technique and ABR algorithms are deployed for bitrate selection. Current video providers have a large number of video contents and users, e.g., YouTube has up to 1 billion of users all around the world, which results in enormous QoE diversity. Prior ABR algorithms take an overall fixed QoE format for concerns and have been proved well performed [3], [4], [5]. However, they may result in misleading bitrate selection for a specific client, e.g., a user with large screen requires high bitrate watching experience while ABR algorithm selects lower bitrate to avoid possible video rebuffering. Because QoE among users is diverse while the overall QoE function is just an estimation on average. Thus the algorithms may result in performance degradation under QoE diversity, for example, MPC suffers at least 20% QoE decrease on average in our experiment.

QoE diversity reflects on various preference to QoE metrics like average bitrate, rebuffering time and bitrate switch. To address the diversity, specific QoE functions should be utilized across different scenarios like video content, user preference, device type, etc [2], [6], [7]. For example, users have different preference on different QoE metrics across different scenarios. Users may have different interests on different kinds of videos, e.g., high bitrate on soccer ball matches for watching wonderful moments vs. fluent track (does not require high bitrate) for music shows. The difference may also come from devices of different screen sizes: users with small screens like smart phones tend to endure low bitrate, while users with TVs usually require watching with high bitrate for clear pictures.

Existing approaches suffer from dealing with QoE diversity in two folds: (1) Simple ABR algorithms experience straight forward bitrate selection and can not address it. (2) Predictive model and machine learning based approaches like MPC, Pensieve conduct fixed QoE function. These algorithms need to be modified to adapt to the diversity by conducting specific QoE functions. However, such modification induces more problems. On the one hand, off-line modification requires acknowledging specific QoE function of every user beforehand. On the other hand, online modification needs specific QoE function perception and leads to heavy re-computation cost for updating algorithm parameters.

To address this issue, we propose Elephanta, which formulates specific QoE function with flexible notions on corresponding metrics and accommodates ABR algorithm with online parameter updates.

As shown in Figure 1, DASH accommodates video server and heterogeneous clients for video delivery. To address diversity adaption, we incorporate QoE monitor and ABR controller in the video player at the edge. The QoE monitor percepts specific QoE functions by providing both several default metric schemes and online parameter tuning user interface. The ABR controller updates parameters according to the feedbacks from the monitor and select video bitrate accordingly. To avoid extra cost from parameter updates, ABR controller conducts QoE function with flexible parameter on different metrics online and accommodates a dynamic parametric ABR algorithm for efficient bitrate selection.

![](images/f7797feaa57f92f98afe66fc009adfaa072cb7d8300d54a8731abb75aed1a6fd.jpg)



Fig. 1. Overview of Elephant in DASH.

To online adapt to QoE diversity, Elephanta models video streaming as a renewal system $[8]$ which maps the parameters into corresponding problem constraints. In addition, for performance assurance, we formulate the problem as bitrate optimization with online adjustable constraints. Accordingly, we utilize an optimization algorithm to solve the problem.

We validate Elephanta design by using 5 thousand throughput traces of both an online data set [9], [10] (including eight months of 3G and broadband data) and two months of 4G/LTE data set collected by ourself under different environments (including campus, dormitory, office, moving bus, etc). In addition, we implement Elephanta in the reference DASH client implementation dash.js [11]. To evaluate its performance, we compare Elephanta with the following prior ABR algorithms: MPC [3], BOLA [4], BB [12] and Elastic [13]. The results show that Elephanta achieves $10\%$ average performance gain under fixed QoE function and outperforms MPC by $21.1\%$ under QoE diversity. We also invite several volunteers for online testing. Besides the default metric schemes, they can adapt their preference by adjusting constraint weights while watching video. The evaluation results present diverse preference for different metrics and Elephanta adaptively responses when a user changes his constraints to reflect his preference.

Processing at the edge, Elephanta adapts to QoE diversity online by updating parameters of specific QoE function and our contributions are as the following:

- To address performance degradation of prior work due to leaving out QoE diversity, we propose Elephanta, which models the video streaming as renewal system and formulates specific QoE function with flexible constraints. Elephanta provides client side monitor to percept change of parameters and utilizes an online parametric ABR algorithm accordingly.   
- We validate Elephanta design under 5K network throughput traces by conducting mahimahi video emulator [14]. We compare Elephanta with prior ABR algorithms, the evaluation results show that Elephanta achieves 21.1% QoE improvement than MPC on average.   
- We implement Elephant in dash.js [11] for online performance testing of specific QoE function perception

and online adjusting by volunteers, the results show that Elephant can effectively adapt to their changes.

The organization of the remainder is as follows. Section II presents the background of video streaming and our motivation. Section III introduces modeling Elephanta and formulation of QoE diversity. Section IV derives the algorithm design and analyzes penalty and constraints setting of Elephanta. Section V evaluates Elephanta under different networks and constraints setting. Section VI shows related work on the QoE metrics diversity and bitrate selection issues. Section VII concludes our work.

# II. BACKGROUND AND MOTIVATION

# A. Video Streaming at the Edge

With the increasing types of devices for video plays, e.g., TVs, mobile devices, laptops and etc, video streaming over HTTP has been an ideal candidate technique for video service. Under the standard HTTP based video structure DASH as shown in Figure 1, the video is stored in CDN, with multiple copies encoded in different bitrates, e.g., 4 Mbps, 8 Mbps and 10 Mbps. Each copy is segmented into chunks of equal length, e.g., a 1-minute video can be segmented into 15 chunks, each of 4 seconds. To play a video at the client side, the ABR controller of video player requests video chunks adaptively with chunk number n and bitrate r. Upon receiving the request, CDN responses with the corresponding video chunk, then the video player downloads the chunk and store in playback buffer for play. Such a process is compatible with different edge devices and has been successfully deployed widely.

To provide high QoE video service, QoE metrics in video streaming have been widely studied $[2]$ , $[7]$ , $[15]$ , $[16]$ , $[17]$ . For the concerns of correlation with QoE, the following metrics for video delivery have been the major QoE metrics $[3]$ : (1) average bitrate: the average bitrate level of a video session, which is positively related with video quality. (2) rebuffering: rebuffering event occurs when the buffer of video player is empty. Rebuffering can be calculated as the total time or occurrence times of rebuffering. Rebuffering decreases user QoE. (3) bitrate switching: change of video bitrate level. The increase of bitrate switch causes video flicker effects, and decreases QoE.

# B. QoE Driven ABR Nowadays

To select proper bitrate adaptively under dynamic networks, ABR algorithms has been widely deployed for video providers including Microsoft [18], Adobe [19], Apple [20] and etc. Recent years witness rapid emergence of ABR algorithms design.

The ABR algorithms are motivated for QoE promotion. Earlier approaches focus on single QoE metric, e.g., using average bitrate as the only metric in QoE function and improving average bitrate by predicting bandwidth $[13]$ , $[21]$ , $[22]$ . However, the QoE metrics are various and improving average bitrate may lead to decrease in another metric, such as bitrate switch and rebuffering.

![](images/e094cd1d84e2b1c9515115600667d72b24b41e8c1b51065339abd149ae659982.jpg)



Fig. 2. Performance comparison of MPC between specific QoE functions under QoE diversity and overall QoE function (leaving out QoE diversity). ( $\mu$ is a constant linear coefficient on standard deviation of normal distribution, which is positively correlated to QoE diversity level.)

Hence more approaches are proposed for mixing the multiple QoE metrics, including average bitrate, bitrate switch and rebuffering. These ABR algorithms conduct predictive model based techniques and the overall QoE function of fixed parameters on QoE metrics meanwhile $[3]$ , $[5]$ .

# C. Performance Degradation under QoE Diversity.

Current video providers serve for a large number of users with different types of edge devices over a vast range of locations. State-of-the-art algorithms conduct an overall QoE function leaving out QoE diversity, which leave a gap for ensuring high quality of service for every edge user. We take MPC [3] as an example for illustration.

MPC conducts parameters rebuffering penalty $P_{re}$ and smooth penalty $P_{sm}$ in QoE function. In this experiment we denote QoE diversity by assuming that the parameters subject to normal distribution $N(\overline{P}_{re}, (\mu\overline{P}_{re})^{2})$ and $N(\overline{P}_{sm}, (\mu\overline{P}_{sm})^{2})$ , where $\mu$ is a positive constant and positively correlated with diversity. We test the performance of different groups of diversity, each group contains the specific parameter combinations $(P_{re}, P_{sm})$ subject to $N(\overline{P}_{re}, (\mu\overline{P}_{re})^{2})$ , $N(\overline{P}_{sm}, (\mu\overline{P}_{sm})^{2})$ respectively and the overall parameter $(\overline{P}_{re}, \overline{P}_{sm})$ under the same network throughput traces. The QoE is calculated as $QoE_{linear}$ which is shown in MPC, denoted as $QoE_{linear} = AvgBitrate - P_{re} * Rebuf - P_{sm} * BitSw - \lambda_{s}T_{s}$ , where $P_{re}, P_{sm}, \lambda_{s}$ are non-negative constant penalty parameter corresponding to bitrate switch, rebuffering time and start up delay, respectively, the start up delay is constant in the experiment.

The result is shown in Figure 2. The overall QoE is calculated according to the results of the average bitrate and rebuffering time under the overall parameters $(\overline{P}_{re}, \overline{P}_{sm})$ . While the specific QoE is calculated under specific parameters $(P_{re}, P_{sm})$ . The findings are in two folds: (1) the overall QoE degrades at least 20% on average comparing to specific QoE functions, (2) when $\mu$ increases (QoE diversity becomes larger), the performance ratio of overall MPC still decreases. For the largest $\mu$ , 0.7, the QoE ratio drops to only 65% of specific QoE functions.

Thus the QoE diversity should be addressed for high service quality assurance. A straightforward idea is to change corresponding parameters in ABR algorithms according to the QoE diversity. However, such a solution induces two problems. (1) The specific QoE functions of edge users are elusive for servers. Even users may be confused how to represent their preference by the parameters. (2) Even assume that specific QoE function can be captured online, adaption for parameter change of prior work will induce huge overheads. Changing QoE function will result in re-computing of models and even re-deploying of video players. For example, MPC calculates an indexing table for a specific video off-line beforehand, with minimal sizes up to hundreds of KB. Updating the parameter in specific QoE function will lead to a recalculation of indexing table. This will induce huge overheads because each indexing table is determined by one of the combinations of QoE functions, network states, buffer levels and video bitrates.

# III. QoE DIVERSITY MODEL

We first present system model of our solution, Elephanta, which incorporates specific QoE parameter perception scheme and flexible problem function formulation. In addition, we transform bitrate selection in Elephanta as the penalty minimization problem in renewal system.

# A. Video Streaming Model

In DASH, the video is segmented into $n$ chunks, each of which contains $S$ seconds video. Each chunk is encoded in $m$ different bitrate levels. Assume the size of bitrate $j$ is $s_j$ ( $1 \leq j \leq m$ ).

When a connection is established, the video player will request chunks one by one, each with a specified bitrate. Assume the video player requests n chunks, the downloaded video chunks are denoted as $c[0]$ , $c[1]$ , $c[2]$ , $\cdots$ , $c[n-1]$ . The downloading start time of chunk $c[i]$ is t[i]. The downloading time of chunk $c[i]$ can be calculated as $T[i] = t[i+1] - t[i]$ . Denote $\pi[i]$ as the policy for determining the bitrate selection of chunk $c[i]$ .

When a requested chunk has been downloaded, it will be stored in the video player's buffer. A video chunk will be removed from the buffer as soon as it is played. To effectively address bitrate selection by utilizing buffer occupancy, we measure video buffer by the total play time of video chunks instead of sizes. The buffer occupancy is denoted as $buf$ , which accommodates $b$ seconds of video. The buffer occupancy at time $t$ is $buf[t]$ . When $buf[t] = 0$ , there remains no video chunk to play in the buffer and rebuffering occurs. Intuitively, it indicates that the video player needs to wait a chunk to be downloaded. When the buffer is full at time $t$ , i.e. $buf[t] = b_{max}$ , the player stops downloading the next chunk. Video chunks in the buffer are served in FCFS manner.

# B. Adaption for QoE Diversity

To address the diversity of user QoE, we first discuss our understanding on the issue and why previous work does not address it.

In video streaming, it is challenging to define what QoE function exactly is. Previous work basically quantifies QoE by mixing video quality metrics, e.g., linear combination of average bitrate, rebuffering, bitrate switch and startup delay. Formulated as the following [3]:

$$
\begin{array}{l} Q o E = \frac {\sum_ {i = 0} ^ {n - 1} u (c [ i ])}{n} - \lambda \frac {\sum_ {i = 0} ^ {n - 1} y _ {b s} (c [ i ])}{n} \\ - \mu \frac {\sum_ {i = 0} ^ {n - 1} y _ {r e} (c [ i ])}{n} - \mu_ {s} T _ {s} \tag {1} \\ \end{array}
$$

Where $\lambda,\mu,\mu_{s}$ are non-negative constant corresponding to bitrate switch, rebuffering times and join time, respectively.

Although previous work tries to optimize the bitrate selection to maximize average QoE, there leaves a gap that conducting overall QoE function does not promise expected performance for a specific user. E.g., a user only cares about rebuffering issues while another prefers high average bitrate. Such diversity still remains unsolved under prior models.

To satisfy the diversity issue, we are inspired to set constraints on corresponding metrics. However, solely satisfying the constraints on the metrics cannot achieve maximal QoE. Thus we define average bitrate as utility and transform the problem into bitrate optimization under constraints on the specific metrics.

Since startup delay usually occurs at the beginning of a video session, we will take the following metrics into concerns in our paper: average bitrate, bitrate switch and rebuffering. In addition, we introduce another factor, buffer occupancy into concern. Previous work has shown that selecting bitrate according to buffer occupancy will improve QoE [12], [23]. We observe that buffer occupancy will affect the selection of average bitrate, e.g., a low buffer occupancy results in high average bitrate.

We use the terms penalty and utility to illustrate problem formulation. The penalties are defined as a function of corresponding metrics, including bitrate switch, rebuffering and buffer occupancy which are denoted as $y_{bs}$ , $y_{re}$ and $y_{bo}$ , respectively. We define average bitrate as utility, which is u. We denote the average utility, penalty of bitrate switch, rebuffering and buffer occupancy over n chunks as follows:

$$
\begin{array}{l} \overline {{u}} = \sum_ {i = 0} ^ {n - 1} \frac {u (c [ i ])}{n}, \overline {{y}} _ {b s} = \sum_ {i = 0} ^ {n - 1} \frac {y _ {b s} (c [ i ])}{n}, \overline {{y}} _ {r e} = \sum_ {i = 0} ^ {n - 1} \frac {y _ {r e} (c [ i ])}{n}, \\ \overline {{y}} _ {b o} = \sum_ {i = 0} ^ {n - 1} \frac {y _ {b o} (c [ i ])}{n}. \\ \end{array}
$$

Note that the diversity is reflected on different QoE metrics expectations, e.g., a user who prefers no rebuffering expects the penalty value as $\overline{y}_{re} = 0$ . Then we can write bitrate selection as the following:

![](images/9d93095d786c5347e4a996276e2f06ce574c1cf9358cb531fc67a8031b054ac8.jpg)



Fig. 3. A sequence of frames in renewal system, each frame's length (e.g., time) is determined by corresponding policy. The frames in system generate penalty and utility vectors, penalty as $p[0], p[1], p[2], \ldots$ , and utility as $u[0], u[1], u[2], \ldots$ respectively.

$$
\max \quad \overline {{u}} \tag {2}
$$

$$
s. t. \quad \overline {{y}} _ {b s} \leq c _ {b s}
$$

$$
\overline {{y}} _ {r e} \leq c _ {r e}
$$

$$
\overline {{y}} _ {b o} \leq c _ {b o}
$$

where $c_{bs}, c_{re}, c_{bo}$ are constraints on penalties of bitrate switch, rebuffering, and buffer occupancy.

Performance Objective: Elephant aims to achieve maximized utility while satisfying the constraints on penalties. The constraints $c_{l}$ represent the expected bounding of corresponding penalties, set of different constraint values denote QoE diversity. Hence the bitrate selection problem has been transformed into the utility optimization problem with penalty constraints.

# C. Flexible QoE Function Formulation

As we formulate bitrate selection into an optimization problem with constraints, we are motivated to solve the problem in an efficient way. Though the dynamic programming based approaches can be used to solve the problem $[24]$ , traditional dynamic programming based approaches require knowledge of future bandwidth which is unavailable in real world. Even if the future bandwidth could be predicted, such approaches will lead to a large state space to calculate the optimal bitrate and leaves large overheads for clients.

To address the issue, we formulate the problem into flexible format with renewal system for further optimization technique. Video chunks are downloaded one by one, which makes video streaming model an ideal candidate for renewal systems model.

As shown in Figure 3, a typical renewal system is comprised with sequential renewal frames, each frame is occurred one after the other with elapsed time $T[i]$ . The policy $\pi$ is to determine corresponding task of the current frame, e.g., select bitrate in video streaming, each task generates an penalty vector p and utility vector u. The goal is to maximize the overall utility utility under given constraints on penalties penalty. Such a characteristic can be utilized as bitrate selection problem in Elephanta, with several mild assumptions.

To formulate the bitrate selection problem, we relax our model slightly by making the following assumptions: (1) A new video chunk begins to download as soon as the previous one is downloaded unless the buffer is full or playback is aborted. The start and end time of chunk $c[i]$ can be regarded as frame $i$ . (2) When a video chunk downloading is aborted due to network failures, the player will request the same chunk of the other bitrate. The penalties of last failing request will be counted, i.e., the failed chunk will be regarded as a virtual video chunk. (3) When a video begins to play, the buffer level is empty, $buf[0] = 0$ . The penalties and utility generated in the system is finite and the time of downloading time $T[i] > 0$ .

As a result from the assumptions, Elephanta is modeled as a renewal system and each downloaded video chunk behaves as a frame. Accordingly, the policy $\pi[i] \in P$ in our system specifies the bitrate selection for chunk i. We denote P as the policy space for bitrate selection.

We define the utility $u[i]$ as negative penalty $y_0[i]$ in renewal system. Note that $y_0$ in renewal system as the minimization target, we define the utility of bitrate level as $-y_0$ . For each chunk i,

$$
y _ {0} [ i ] \triangleq - u [ i ] = - \phi (c [ i ]) \tag {3}
$$

Hence we have the penalty vector $\boldsymbol{y} = (y_{0}, y_{1}, y_{2}, y_{3})$ where $y_{0}$ , $y_{1}$ , $y_{2}$ and $y_{3}$ correspond to utility, rebuffering, bitrate switch and buffer occupancy, respectively. We can also see that the downloaded time for chunk i is positive and both the time and penalties $T[i]$ , $y[i]$ are finite constants for all policies $\pi \in P$ .

According to average time and penalties defined in renewal system. The average download time for a video session is $\overline{T}$ . For each chunk $i$ , the policy $\pi[i]$ generates a penalty vector $\mathbf{y}[i] = (y_0[i], y_1[i], y_2[i], y_3[i])$ . The chunk average penalty is defined as $\bar{\mathbf{y}} = (\overline{y}_0, \overline{y}_1, \overline{y}_2, \overline{y}_3)$ .

The optimization of utility in Elephanta is the minimization of $y_{0}$ in renewal system. Hence the problem formulation in equation 2 can be equally transformed into the following format:

$$
\min \quad \frac {\overline {{y}} _ {0}}{\overline {{T}}} \tag {4}
$$

$$
s. t. \quad \frac {\overline {{y}} _ {l}}{\overline {{T}}} \leq c _ {l}, \forall l \in \{1, \dots , 3 \}
$$

$$
\pi [ i ] \in \mathcal {P}, \forall i \in \{0, 1, 2,..., n - 1 \}
$$

where $c_{l}$ ( $l \in \{1, \cdots, 3\}$ ) are constraints for average penalties of rebuffering, bitrate switch and buffer occupancy. The QoE diversity is reflected on the flexible constraints and now we finish modeling Elephanta.

# IV. ELEPHANTA DESIGN

In this section, we derive the adaption algorithm of Elephant from QoE diversity model and compare Elephant with prior work.

# A. Renewal System based Optimization

We conduct drift-plus-penalty techniques [8] for algorithm design, which introduces virtual queues to select optimal bitrate.

The penalties in renewal system are corresponding to the QoE metrics, denote

$$
\boldsymbol {y} = (y _ {1} [ i ], y _ {2} [ i ], y _ {3} [ i ]) = (y _ {b s} [ i ], y _ {r e} [ i ], y _ {b o} [ i ])
$$

![](images/5e4cd587fcc72ab4354ce5e2c69a3baaedda05ba780540c4250029105c79256e.jpg)



Fig. 4. Work flow of Elephant

To deal with constraints $c_l$ for $l \in \{1,2,3\}$ , define corresponding virtual queues $Z_l[i]$ ( $Z_l[0] = 0$ ), as follows:

$$
Z _ {l} [ i + 1 ] = \max \left[ Z _ {l} [ i ] + y _ {l} [ i ] - c _ {l} T [ i ], 0 \right] \tag {5}
$$

According to equation (5), the Lyapunov function for chunk $i$ is defined as:

$$
L (\mathbf {Z} [ i ]) \triangleq \frac {1}{2} \sum_ {l = 1} ^ {L} Z _ {l} [ i ] ^ {2}
$$

Where $L$ denotes the number of constraints, here $L = 3$ . Then conditional Lyapunov drift is:

$$
\Delta (\mathbf {Z} [ i ]) \triangleq E \{L (\mathbf {Z} [ i + 1 ]) - L (\mathbf {Z} [ i ]) | \mathbf {Z} [ i ] \} \tag {6}
$$

The renewal system aims to minimize the drift-plus-penalty ratio. While in Elephanta, we have formulated the penalty as $y_{0}$ and drift as $y_{l}$ . To make our paper easy to follow, here we quote the conclusion from Chapter 7.2 in [8]. The drift-plus-penalty for chunk i satisfies the following formulation:

$$
\Delta (\mathbf {Z} [ i ]) + V E \{y _ {0} [ i ] | \mathbf {Z} [ i ] \} \leq B + V E \{\hat {y} _ {0} (\pi [ i ]) | \mathbf {Z} [ i ] \}
$$

$$
+ \sum_ {l = 1} ^ {L} Z _ {l} [ i ] E \{\hat {y} _ {l} (\pi [ i ]) | \boldsymbol {Z} [ i ] \} - \sum_ {l = 1} ^ {L} c _ {l} Z _ {l} [ i ] E \{\hat {T} (\pi [ i ]) | \boldsymbol {Z} [ i ] \} \tag {7}
$$

Where $V$ is a constant variable, $B$ is a finite constant. According to bounds assumption in [8] (finite bounds of $E\{\hat{T}(\pi[i])^2|\pi[i] = \pi\}$ and $E\{\hat{y}_l(\pi[i])^2|\pi[i] = \pi\}$ exist for $l$ and all $\pi \in \mathcal{P}$ ), B exists and satisfies for all $i$ and possible $Z[i]$ :

$$
B \geq \frac {1}{2} \sum_ {l = 1} ^ {L} E \{(y _ {l} [ i ] - c _ {l} T [ i ]) ^ {2} | \mathbf {Z} [ i ] \} \tag {8}
$$

Thus the drift-plus-penalty bound of video chunk $i$ is given by the right-hand-side of equation (7). To maximize the utility overtime as in equation (2), i.e., minimize average $\overline{y}$ in equation (4), we are inspired to minimize the bound for policy $\pi[i]$ . It has been proved in [8] that the optimal policy $\pi[i]$ can be chosen according to equation (7) by minimizing the following ratio:

$$
\mathcal {G} [ i ] = \frac {E \{V \hat {y} _ {0} (\pi [ i ]) + \sum_ {l = 1} ^ {L} Z _ {l} [ i ] \hat {y} _ {l} (\pi [ i ]) | \boldsymbol {Z} [ i ] \}}{E \{\hat {T} (\pi [ i ]) | \boldsymbol {Z} [ i ] \}} \tag {9}
$$

Policy $\pi[i]$ specifies optimal bitrate, by selecting the bitrate which minimizes the value of equation (9) among all available bitrate for chunk i.

The flow of Elephanta is shown in Figure 4. Elephanta utilizes buffer occupancy and bandwidth prediction for the next video chunk selection. To calculate the expected bandwidth for next chunk, Elephanta utilizes the average downloading time from a horizon of several past chunks. Based on the constraints setting, Elephanta calculates drift-plus-penalty value equation (9) for all the bitrates of next chunk. Then Elephanta downloads the optimal bitrate and updates the buffer occupancy when the chunk is downloaded.

The detail of the algorithm design is shown in Alg. 1. The specific QoE functions can be updated by adjusting corresponding parameter $\alpha$ . Elephant avoids extra computation for parameter updates when QoE function changes. The overhead is to maintain the virtual queues Z and calculate $G[i]$ m times (number of bitrates) for each chunk selection.

Algorithm 1 Bitrate Selection under QoE Diversity   
1: initialize virtual queues $Z_{bs}$ , $Z_{re}$ , $Z_{bo}$ ;
penalty functions for bitrate switch $y_{bs}$ , rebuffering $y_{re}$ ,
buffer occupancy $y_{bo}$ according to equations (10), (11)
and (12);
utility function $y_{0}$ according to equation (13);
constraints for penalties $c_{bs}$ , $c_{re}$ , $c_{bo}$ ;
set i = 0, default QoE function parameters $\alpha_{1}, \alpha_{2}, \alpha_{3}$ ;

2: while i < n do   
3: calculate penalties $y_{bs}[i]$ , $y_{re}[i]$ , $y_{bo}[i]$ for all bitrates;   
4: select bitrate $r^*$ for chunk $i$ that minimizes $\mathcal{G}[i]$ according to equation (9);   
5: download chunk $v_{ir^{*}}$ ;   
6: calculate $Z_{bs}[i + 1], Z_{re}[i + 1], Z_{bo}[i + 1]$ using equation (5)   
7: update buffer occupancy, virtual queues $Z_{bs}, Z_{re}, Z_{bo}$ ;   
8: $i = i + 1$   
9: update $\alpha_{1},\alpha_{2},\alpha_{3}$ ;   
10: end while

# B. Penalty and Utility Formulation

Note that definition on QoE metrics may be various, Elephant gives an example definition of penalties and utility respectively.

$$
y _ {b s} [ i ] = \alpha_ {1} * e ^ {| c [ i ] - c [ i - 1 ] |} \tag {10}
$$

$$
y _ {r e} [ t ] = \alpha_ {2} * [ 1 - I (b u f (t)) ] \tag {11}
$$

$$
y _ {b o} [ t ] = \alpha_ {3} * b u f (t) \tag {12}
$$

$$
u [ i ] = l n (s [ i ]) \tag {13}
$$

where $I(x) = 1$ when x > 0, otherwise, $I(x) = 0$ ; i is chunk index, c[i] is the chunk bitrate of i, and $buf(t)$ is buffer occupancy at time t. All the parameters $\alpha_{1}$ , $\alpha_{2}$ and $\alpha_{3}$ are flexible weights for each penalty which can be adjusted according to QoE diversity. The characteristic eliminates the affects of parameter $V$ , thus we set $V = 1$ .

Elephanta chooses the penalty of bitrate switch as an exponential function equation (10). The penalty generated by adjacent chunks increases significantly when the bitrate changes violently, hence Elephanta keeps conservative bitrate switch. Elephanta counts rebuffering times as the penalty in equation (11), specifically number of rebuffering events. The penalty of buffer occupancy as a linear function of buffer occupancy $buf(t)$ . To calculate utility u[i] comparable to penalties, it is defined as a logarithmic function of the size of chunk i.

Elephanta sets constraints for bitrate switch, rebuffering and buffer occupancy by adjusting $\alpha_{1}$ , $\alpha_{2}$ and $\alpha_{3}$ . Large weight results in small penalty. Take $\alpha_{1}$ for example, a larger $\alpha_{1}$ generates a larger penalty of bitrate switch. Thus to satisfy constraint $\overline{y}_{bs} \leq c_{bs}$ , the value of $|c[i] - c[i-1]|$ tends to be small.

We analyze the performance of Elephanta under a sample video. The video length is of 20 minutes and encoded in 10 bitrate levels. Each chunk has a length of 4 seconds. In Elephanta, the penalties and utility function are defined as equations (10), (11), (12) and (13). We set the initial constraints of each penalty following the expected upper bound in renewal system. The default constraints are as follows: $c_{bs} = \frac{e^m}{T_{sup}}$ , $c_{re} = \frac{1}{T_{sup}}$ , $c_{bo} = \frac{b_{max}}{T_{sup}}$ , where $T_{sup} = \min\left(\frac{s[m]}{s[1]}, Buf\right)$ denotes the upper bound of expected download time and $m = 10$ .

The calculation of average bitrate (AvgBitrate), bitrate switch (BitrateSw), rebuffering events (Rebuf) is as follows:

$$
\text { AvgBitrate } = \frac {\sum_ {i = 0} ^ {n - 1} c [ i ]}{n} \tag {14}
$$

$$
\text { BitrateSw } = \sum_ {i = 1} ^ {n - 1} | c [ i ] - c [ i - 1 ] | \tag {15}
$$

$$
\text { Rebuf } = \sum_ {t} r e [ t ] \tag {16}
$$

where $re[t] = 1$ if $buf(t) = 0$ and $buf(t - 1) > 0$ when $t > 0$ ; otherwise, $re[t] = 0$ .

# C. Verifying Different Penalty Formats

TABLE I COMPARISON FOR DIFFERENT FORMATS OF BITRATE SWITCH. 

<table><tr><td>Function Format</td><td>AvgBitrate</td><td>BitrateSw</td><td>Rebuf</td></tr><tr><td> $|c[i] - c[i-1]|$ </td><td>7.2</td><td>400</td><td>0</td></tr><tr><td> $ln\{|c[i] - c[i-1]| + 1\}$ </td><td>7.3</td><td>697</td><td>0</td></tr><tr><td> $e^{|c[i] - c[i-1]|}$ </td><td>7.2</td><td>154</td><td>0</td></tr></table>

The definition of penalties and utility function may be various in real world. To analyze the sensitivity of definitions, we take bitrate switch as an example. Besides the penalty function in equation (10), we also test two other kinds of penalty functions of bitrate switch. The result is shown in Table I. From the result, the different formats of penalty result in QoE metrics variance. Exponential function achieves lowest bitrate switch while logarithmic function holds the largest bitrate switch. The result shows that bitrate switch varies among different definition and depends on the gradient of function.

# V. EVALUATION

# A. Implementation in DASH

We implement Elephanta in dash.js [11], a reference video player client implementation of DASH. Besides, we make modifications to fit dash.js to our model, the implementation of Elephanta can be found at [25]. The DASH video player checks buffer occupancy every second to decide if current bitrate should be changed. This implies bitrate selection will happen when a video chunk is being downloaded, and lead to bitrate execution delay or even re-downloading previous chunks. Thus, we modified the source code to ensure that bitrate decision function is executed only when the former chunk finished downloading.

Elephanta provides QoE perception interfaces by adjustable parameters on corresponding metrics which is visible to users. Elephanta monitors the change of parameters when the video plays. Once detecting the parameter updates, QoE monitor sends the newest parameter to ABR controller, then ABR controller selects the target bitrate of next chunk and sends the request to video servers.

To adapt to QoE diversity, we set three flexible constraint weights $w_{bs}, w_{re}, w_{bo}$ for bitrate switch, rebuffering and buffer occupancy. The constraint weights range from 0% to 100%. Those weights are initialized by video players and can be adjusted by users. Accordingly, $\alpha_{1}, \alpha_{2}$ and $\alpha_{3}$ are updated as follows: $\alpha_{1} = w_{bs} * \alpha_{1}, \alpha_{2} = w_{re} * \alpha_{2}, \alpha_{3} = w_{bo} * \alpha_{3}$ .

# B. Experiment Settings

In the experiment, we evaluate Elephanta in Google Chrome (version 71.0.3578.98, 64 bit) and control network bandwidth by setting rules in the console. The video we choose is four seconds per chunk with 10 bitrates. We choose penalties of buffer occupancy, rebuffering and utility as in equation (14), (15) and (16). We set the default constraints $c_{bs}$ , $c_{re}$ , $c_{bo}$ as 1. Default weights $w_{bs}$ , $w_{re}$ , $w_{bo}$ are set to 100% except explicitly pointed out.

In DASH, videos are mostly encoded with variant bitrate (VBR). The large variance will affect performance when the real size of a chunk is quite different with the corresponding bitrate chunk size $[26]$ , $[12]$ . E.g. the real size of a chunk indexed with bitrate 5 may be smaller than the chunk of bitrate 4, in such situation the bitrate selection will be wrong and decrease the performance of algorithms.

In our experiment, each bitrate's chunk size are given an average value, as the expected size of corresponding chunk. In Figure 6, a bitrate video chunk's given size is nearly equal to the chunk's real size. Moreover, the low variance among chunk sizes show that the chunk's real size is with the same sort to the bitrate.

TABLE II
QOE METRICS UNDER QOE DIVERSITY. 

<table><tr><td> $(\alpha_1, \alpha_2, \alpha_3)$ </td><td>AvgBitrate</td><td>BitrateSw</td><td>Rebuf</td><td>AvgBuf</td></tr><tr><td>(0, 0, 1)</td><td>6.9</td><td>4.42</td><td>2</td><td>5.6</td></tr><tr><td>(0, 1, 0)</td><td>6.1</td><td>4.50</td><td>0</td><td>8.5</td></tr><tr><td>(0, 1, 1)</td><td>6.6</td><td>4.56</td><td>0</td><td>6.3</td></tr><tr><td>(1, 0, 0)</td><td>5.6</td><td>1.39</td><td>0</td><td>10.1</td></tr><tr><td>(1, 0, 1)</td><td>6.9</td><td>3.58</td><td>2</td><td>5.4</td></tr><tr><td>(1, 1, 0)</td><td>6.6</td><td>3.12</td><td>0</td><td>6.1</td></tr><tr><td>(1, 1, 1)</td><td>6.8</td><td>4.41</td><td>0</td><td>6.0</td></tr></table>

We compare Elephanta with prior ABR algorithms including MPC [3], BOLA [4], BB [12] and Elastic [13].

The evaluation is performed in the following aspects: First, we collect network traces and emulate Elephant comparing to prior ABR algorithms under fixed QoE function. Second, we show how Elephant adapts to QoE diversity in detail. Finally, we study the specific metric performance of Elephant under QoE diversity with prior algorithms.

# C. QoE Diversity Driven Adaption.

We provide three kinds of constraints bitrate switch (BitrateSw), rebuffering (Rebuf) and buffer occupancy (Buf) by default. Users can set constraint weights $\alpha_{1}$ , $\alpha_{2}$ and $\alpha_{3}$ from 0 to 100% according to his preference. We show the performance of Elephanta for kinds of constraint combinations ( $\alpha_{1}$ , $\alpha_{2}$ , $\alpha_{3}$ ) and provide several suggested QoE function schemes.

We record the average bitrate, bitrate switch, rebuffering times and average buffer occupancy for each constraints setting, detailed results are summarized in Table II. It has been shown that different combinations result in different network performance. In our experiment, the QoE metrics are effectively controlled by corresponding constraints:

- When $\alpha_{1}$ is 1, the bitrate switch is $29.9\%$ lower than $\alpha_{1} = 0$ on average.   
- When $\alpha_{2}$ is 1, no rebuffering occurs on average while rebuffering occurs 1.33 times when $\alpha_{2} = 0$ .   
- When $\alpha_{3}$ is 1, the average bitrate is $11.5\%$ higher than $\alpha_{3} = 0$ . Intuitively, the bitrate level is 0.7 higher.

The constraints of Elephanta can be set according to QoE diversity. To intuitively show how to set the constraints, we take a specific scenario for example that watching football video replay and recommend constraints setting for different users. As shown in Table III, we set different groups of constraints across users for comparison. Elephanta performs well for the following different groups of users: High Resolution (HR). Users usually require high quality of frames that captures the wonderful moments, we can set constraints with low buffer occupancy, low rebuffering and no bitrate switch. Smooth. For a user who requires fluent moments, the video is more likely to be played with no rebuffering. Balance. The users may tend to watch the video with little or no bitrate switch for a no flickering experience.

![](images/4f3095df3739709ccc07059ed8d59bdbf4344b5ed46de39f0c347556921ab52a.jpg)



(a)

![](images/d0cf107249cf94a7dcda925e91ceb6fb1604f298ab4a6daa903d83149815c1c4.jpg)



(b)

![](images/72e32457e743995d81cfb7301a6f72d6b40ba47e4fadb2123f802633658c8da0.jpg)



(c)   
Fig. 5. Example for online QoE function tuning and perception. (a) The buffer occupancy constraints weight is high and the video plays at low buffer occupancy with a high bitrate. (b) The bitrate switch constraints weight is high. The bitrate maintains at a low level. Meanwhile, buffer occupancy goes high. (c) Rebuffering and buffer occupancy weights are set high. The video plays fluently with no rebuffering, and keeps a low buffer occupancy.

![](images/d0200a4d6faa7583450fde3738f1d1654f3aec46080916901175177b8ecd95f4.jpg)



Fig. 6. Video chunk size of the sample video.

TABLE III
QOE FUNCTION SCHEMES. 

<table><tr><td>Scheme</td><td> $(\alpha_1, \alpha_2, \alpha_3)$ </td><td>AvgBitrate</td><td>BitrateSw</td><td>Rebuf</td><td>AvgBuf</td></tr><tr><td>HR</td><td>(0.6, 0.1, 0.6)</td><td>7.2</td><td>4.04</td><td>2</td><td>4.5</td></tr><tr><td>Smooth</td><td>(1, 1, 0.2)</td><td>6.73</td><td>4.41</td><td>0</td><td>7.2</td></tr><tr><td>Balance</td><td>(1, 0.3, 0.5)</td><td>6.9</td><td>4.54</td><td>1</td><td>6.1</td></tr></table>

# D. Online QoE Perception and Adaption

We show the demo page of Elephanta which supports adjusting constraints online. The volunteer can change her preference by adjusting the constraints while watching the video.

As shown in Figure 5, we record the bitrate and buffer occupancy to show how well Elephanta adapts to QoE diversity online. We take one video track for illustration. The volunteer has three different stages of QoE preference: (1) the user wants to watch a high bitrate video. Thus he sets the constraint weight of buffer occupancy higher than other constraints; (2) the user aims to reduce bitrate switch. The user increases the constraint weight of bitrate switch; (3) the user changes rebuffering constraint to high and sets a medium constraint for buffer occupancy to get fluent video streaming. The diagram shows that the constraints on metrics take effects as soon as changed.

# E. Collecting Real World Network Traces.

To validate the design of Elephanta, we collect real world network's bandwidth traces from Internet, including

TABLE IV
4G NETWORK TRACES SUMMARY (JUNE TO JULY, 2018). 

<table><tr><td>Scenario</td><td>Avg (Mbps)</td><td>Std.</td><td>Test points (K)</td></tr><tr><td>Indoor</td><td>10.26</td><td>4.98</td><td>283</td></tr><tr><td>Bus</td><td>8.58</td><td>4.58</td><td>48</td></tr><tr><td>Street</td><td>9.81</td><td>3.98</td><td>21</td></tr></table>

eight months 3G/HSDPA [9] and broadband network traces (FCC) [10].

In addition, we measure 4G/LTE network traces on our own. We modify the speedtest source code $[27]$ and implement the test code into mobile phones. The measurement environment includes indoor (laboratory, office, dormitory, class room), bus, street (urban area, park and etc). We measure the download bandwidth every 1 to 10 seconds equally, and collect 100 test points as one bandwidth trace. We conduct two months 4G/LTE traces in our evaluation, characteristic of the data is shown in Table IV.

# F. Elephanta vs. Prior ABR Algorithms

To compare Elephanta with prior ABR algorithms, we conduct mahimahi emulator [14] and real world traces for evaluation.

1) Performance under Fixed QoE Function: We choose the following ABR algorithms for performance evaluation: (1) Elastic [13], bandwidth based approach for bitrate selection; (2) BB [12], buffer based approaches for bitrate selection; (3) BOLA [4], recent near-optimal buffer based approaches, the supreme algorithm in DASH.

We first set Elephanta with fixed notion of parameters in QoE function to compare the performance. In our experiment, the parameters of Elephanta are set as $\alpha_{1}=1.5$ , $\alpha_{2}=0.8$ , $\alpha_{3}=0.6$ . The quantified QoE metrics are calculated as a result of average bitrate, rebuffering time and bitrate switch: $QoE=\overline{u}-\alpha_{1}\overline{y}_{bs}-\alpha_{2}\overline{y}_{re}$ . As shown in Figure 7, Elephanta achieves nearly 10% QoE improvement than existing algorithms, specifically, outperforms BOLA by 14.1%, 8.6%, 6.5% in 4G, FCC broadband and HSDPA dataset respectively.

2) Performance under QoE Diversity.: To evaluate the performance of Elephant on QoE diversity, we compare Elephant over MPC with overall parameters $\overline{P}_{rb}, \overline{P}_{sm}$ . We randomly choose 1000 traces from FCC broad band HSDPA and 4G dataset. Each trace is emulated 3500 times with flexible parameter QoE functions. The parameters subject to normal distribution $N(\overline{P}_{rb}, (\mu\overline{P}_{rb})^{2})$ , $N(\overline{P}_{sm}, (\mu\overline{P}_{sm})^{2})$ , where $\mu$ ranges uniformly from 0.1 to 0.7.

![](images/ed8a7370b4beff0ee8fd98c5022fd951919123a505e1ceb15479d760db945dde.jpg)



4G/LTE dataset

![](images/f0e9ff93fb14f6cce8a59de3905ea1d23d54146997c7892e08b99f2e30e3c729.jpg)



FCC broadband dataset

![](images/d4cd3635bb6106e9f4806a01183862d36f720edb574825e6c1769cbc376b8105.jpg)



Norway HSDPA dataset   
Fig. 7. Comparing Elephant with existing ABR algorithms on 4G/LTE, broadband and 3G/HSDPA networks.

![](images/3f0cd325fd92a93af24487410f3ea08e3ef0958b6c40f06bd8ec8a3c6110198e.jpg)



Fig. 8. QoE improvement of Elephant over MPC with overall parameter QoE function.

TABLE V
QOE METRIC SCORES UNDER QOE DIVERSITY. 

<table><tr><td>Metric scores</td><td>MPC</td><td>BOLA</td><td>Elephanta</td></tr><tr><td>AvgBitrate</td><td>3.62</td><td>3.50</td><td>3.35</td></tr><tr><td>Rebuff</td><td>-2.70</td><td>-1.04</td><td>-0.11</td></tr><tr><td>BitrateSw</td><td>-0.15</td><td>-2.15</td><td>-0.57</td></tr><tr><td>Average QoE</td><td>5.04</td><td>4.38</td><td>6.11</td></tr></table>

The result is shown in Table V, MPC selects higher bitrate and results in larger rebuffering time while BOLA gets both large rebuffering time and bitrate switch. Elephant shows QoE improvement on rebuffering and bitrate switch with little average bitrate reduction. Because the change of $P_{rb}$ , $P_{sm}$ will affect the optimal bitrate selection.

Comparing to MPC, Figure 8 shows that Elephanta improves QoE in nearly 80% sessions and average QoE improvement achieves up to 21.1%. The reasons are in that: (1) when considering QoE diversity, the overall MPC decreases QoE due to leaving out specific QoE functions. (2) Elephanta can efficiently adapt to flexible QoE parameters by adjusting corresponding QoE metrics.

# VI. RELATED WORK

QoE metrics study. The metrics affecting QoE in video streaming have been widely studied recently. The user perceived video quality such as buffering ratio, average bitrate, join time and rendering quality impact their engagement and watching time [2]. Other quality metric such as flicker effects has been shown negative correlation to watching experience [17].

Some other work attempts to infer QoE and capture the QoE diversity. In [6], it measures user-viewing activities and utilize the data to correlate into QoE function. In [28], a system for television program is proposed for recording user preference determinations.

Exploiting ABR algorithms. The performance of ABR algorithms can significantly impact user engagement $[29]$ . Adaptive video streaming suffers from network diversity, in early stages, the approaches take average bitrate as the only factor in QoE function and promote average bitrate by predicting future bandwidth $[13]$ , $[21]$ , $[22]$ . However, the bandwidth is hard to be accurately predicted due to various network congestions and capacities $[23]$ , $[30]$ , $[31]$ , $[32]$ .

To avoid QoE loss caused by inaccurate bandwidth prediction, buffer occupancy has been introduced for design. The idea is to determine the bitrate for different levels of buffer occupancy, like $[12]$ . Another approach, BOLA $[4]$ selects bitrate for different users based on a QoE function of fixed weight of video buffer instability and average bitrate.

Further, predictive model based methods have come into the front. MPC $[3]$ conduct model predictive control technique to formulate QoE maximization problem and indexing table for efficient bitrate selection. Pensieve $[5]$ designs the ABR algorithm from experience by utilizing modern reinforcement learning.

# VII. CONCLUSION

Promoting the quality of experience for every end user in video streaming has raised more and more attention. Prior work has improved QoE under the context of overall user QoE function definition and optimization methods. However, prior work fails to effectively address QoE diversity in that (a) most algorithms conduct a fixed overall notion of QoE function and result in low QoE (b) lack of an efficient online QoE optimization algorithm for specific QoE functions. To address the issue, we propose Elephanta, which conducts online QoE function perception schemes and online flexible adaption algorithm for QoE diversity. We implement Elephanta in the reference DASH client implementation dash.js [11] and the evaluation results show that Elephanta outperforms MPC by 21.1% on average QoE for the superior adaptability to QoE diversity.

# VIII. ACKNOWLEDGMENTS

This work is in part supported by National Natural Science Fund China for Excellent Young Scholars (No. 61722210), NSFC key program No. 61532012, NSFC No. 61572277, 61529202.

# REFERENCES

[1] Cisco, “Cisco visual networking index: Forecast and methodology,” https://www.cisco.com/c/en/us/solutions/collateral/service-provider/visual-networking-index-vni/complete-white-paper-c11-481360.html, 2017.   
[2] F. Dobrian, V. Sekar, A. Awan, I. Stoica, D. Joseph, A. Ganjam, J. Zhan, and H. Zhang, “Understanding the impact of video quality on user engagement,” in ACM SIGCOMM Computer Communication Review, vol. 41, no. 4. ACM, 2011, pp. 362–373.   
[3] X. Yin, A. Jindal, V. Sekar, and B. Sinopoli, “A control-theoretic approach for dynamic adaptive video streaming over http,” in ACM SIGCOMM Computer Communication Review, vol. 45, no. 4. ACM, 2015, pp. 325–338.   
[4] K. Spiteri, R. Urgaonkar, and R. K. Sitaraman, “Bola: Near-optimal bitrate adaptation for online videos,” in IEEE INFOCOM 2016-The 35th Annual IEEE International Conference on Computer Communications. IEEE, 2016, pp. 1–9.   
[5] H. Mao, R. Netravali, and M. Alizadeh, “Neural adaptive video streaming with pensieve,” in Proceedings of the Conference of the ACM Special Interest Group on Data Communication. ACM, 2017, pp. 197–210.   
[6] R. K. Mok, E. W. Chan, X. Luo, and R. K. Chang, “Inferring the qoe of http video streaming from user-viewing activities,” in Proceedings of the first ACM SIGCOMM workshop on Measurements up the stack. ACM, 2011, pp. 31–36.   
[7] S. S. Krishnan and R. K. Sitaraman, “Video stream quality impacts viewer behavior: inferring causality using quasi-experimental designs,” IEEE/ACM Transactions on Networking, vol. 21, no. 6, pp. 2001–2014, 2013.   
[8] M. J. Neely, “Stochastic network optimization with application to communication and queueing systems,” Synthesis Lectures on Communication Networks, vol. 3, no. 1, pp. 1–211, 2010.   
[9] P. Halvorsen, “Hsdpa dataset,” http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/, accessed: 2018.2.1.   
[10] F. C. Commission., “Fcc dataset,” https://www.fcc.gov/reports-research/reports/measuring-broadband-america, 2017.   
[11] Dash-Industry-Forum, “dash.js,” https://github.com/Dash-Industry-Forum/dash.js, 2017.   
[12] T.-Y. Huang, R. Johari, N. McKeown, M. Trunnell, and M. Watson, “A buffer-based approach to rate adaptation: Evidence from a large video streaming service,” ACM SIGCOMM Computer Communication Review, vol. 44, no. 4, pp. 187–198, 2015.

[13] L. De Cicco, V. Caldaralo, V. Palmisano, and S. Mascolo, “Elastic: a client-side controller for dynamic adaptive streaming over http (dash),” in 2013 20th International Packet Video Workshop. IEEE, 2013, pp. 1–8.   
[14] R. Netravali, A. Sivaraman, S. Das, A. Goyal, K. Winstein, J. Mickens, and H. Balakrishnan, “Mahimahi: Accurate record-and-replay for http.” in USENIX Annual Technical Conference, 2015, pp. 417–429.   
[15] Y. Chen, K. Wu, and Q. Zhang, “From qos to qoe: A tutorial on video quality assessment,” IEEE Communications Surveys & Tutorials, vol. 17, no. 2, pp. 1126–1165, 2015.   
[16] R. K. Sitaraman, “Network performance: Does it really matter to users and by how much?” in 2013 Fifth International Conference on Communication Systems and Networks (COMSNETS). IEEE, 2013, pp. 1–10.   
[17] P. Ni, R. Eg, A. Eichhorn, C. Griwodz, and P. Halvorsen, “Flicker effects in adaptive video streaming to handheld devices,” in Proceedings of the 19th ACM international conference on Multimedia. ACM, 2011, pp. 463–472.   
[18] Microsoft, “Microsoft smooth streaming,” https://www.iis.net/downloads/microsoft/smooth-streaming, 2017.   
[19] Adobe, “Adobe http dynamic streaming,” http://www.adobe.com/products/hds-dynamic-streaming.html, 2017.   
[20] Apple, “Apple http live streaming,” https://developer.apple.com/streaming/, 2017.   
[21] Z. Li, X. Zhu, J. Gahm, R. Pan, H. Hu, A. C. Begen, and D. Oran, "Probe and adapt: Rate adaptation for http video streaming at scale," IEEE Journal on Selected Areas in Communications, vol. 32, no. 4, pp. 719–733, 2014.   
[22] J. Jiang, V. Sekar, and H. Zhang, “Improving fairness, efficiency, and stability in http-based adaptive video streaming with festive,” IEEE/ACM Transactions on Networking (ToN), vol. 22, no. 1, pp. 326–340, 2014.   
[23] X. K. Zou, J. Erman, V. Gopalakrishnan, E. Halepovic, R. Jana, X. Jin, J. Rexford, and R. K. Sinha, “Can accurate predictions improve video streaming in cellular networks?” in Proceedings of the 16th International Workshop on Mobile Computing Systems and Applications. ACM, 2015, pp. 57–62.   
[24] D. P. Bertsekas and etc, Dynamic programming and optimal control. Athena scientific Belmont, MA, 1995, vol. 1, no. 2.   
[25] C. Qiao, “Elephanta implementation,” https://github.com/tionry/Elephanta-dash.js, 2019.   
[26] T. Zhang, F. Ren, W. Cheng, X. Luo, R. Shu, and X. Liu, “Modeling and analyzing the influence of chunk size variation on bitrate adaptation in dash,” in IEEE INFOCOM 2017-IEEE Conference on Computer Communications. IEEE, 2017, pp. 1–9.   
[27] Sivel, "Speedtest cli," https://github.com/sivel/speedtest-cli.   
[28] L. K. Ismail, A. N. Gogoi, and Y. Stupak, “Television program recording with user preference determination,” Sep. 2 2003, uS Patent 6,614,987.   
[29] A. Balachandran, V. Sekar, A. Akella, S. Seshan, I. Stoica, and H. Zhang, "Developing a predictive model of quality of experience for internet video," in ACM SIGCOMM Computer Communication Review, vol. 43, no. 4. ACM, 2013, pp. 339–350.   
[30] T.-Y. Huang, N. Handigol, B. Heller, N. McKeown, and R. Johari, "Confused, timid, and unstable: picking a video streaming rate is hard," in Proceedings of the 2012 internet measurement conference. ACM, 2012, pp. 225-238.   
[31] K. Winstein, A. Sivaraman, and H. Balakrishnan, “Stochastic forecasts achieve high throughput and low delay over cellular networks,” in Presented as part of the 10th {USENIX} Symposium on Networked Systems Design and Implementation ( $\{NSDI\}$ 13), 2013, pp. 459–471.   
[32] Y. Zaki, “Adaptive congestion control for unpredictable cellular networks,” in ACM SIGCOMM Computer Communication Review, vol. 45, no. 4. ACM, 2015, pp. 509–522.