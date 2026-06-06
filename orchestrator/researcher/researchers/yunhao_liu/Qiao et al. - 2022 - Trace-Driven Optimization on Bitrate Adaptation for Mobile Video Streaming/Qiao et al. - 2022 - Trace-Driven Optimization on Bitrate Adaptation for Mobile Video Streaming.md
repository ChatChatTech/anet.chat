# Trace-driven Optimization on Bitrate Adaptation for Mobile Video Streaming

Chunyu Qiao, Member, IEEE, Gen Li, Member, IEEE, Qiang Ma, Member, IEEE, Jiliang Wang, Member, IEEE, Yunhao Liu, Fellow, IEEE, ACM

Abstract—Mobile video streaming occupies three-quarters of today’s cellular network traffic. The quality of mobile videos becomes increasingly important for video providers to attract more users. For example, they invest in network bandwidth resources and conduct adaptive bitrate techniques to improve video quality. Prior adaptive bitrate (ABR) algorithms perform well under given throughput traces on broadband and WiFi networks. They may perform poorly for mobile video streaming due to the high network dynamics of cellular networks. To study the properties of throughput traces under cellular networks, we collect 4G network throughput traces for over four months in two large cities, Beijing and Suzhou in China. We derive the environment-specific Markov property of throughputs in the dataset. Accordingly, we propose NEIVA, an environment identification based technique to adaptively predict future throughput for different types of environments. We also implement NEIVA and integrate it with the state-of-the-art ABR algorithm, model predictive control (MPC) approach in our testbed for experiments. By emulating mobile video streaming under throughput traces in our dataset, NEIVA achieves 20% − 25% improvement on throughput prediction accuracy comparing to baseline predictors. Meanwhile, NEIVA achieves 11% − 20% user QoE improvement over MPC with baseline predictors.

Index Terms—Cellular network measurement, environment-specific Markov property, throughput prediction, adaptive mobile video streaming

# 1 INTRODUCTION

W ITH the rapid development of cellular network tech-nology (e.g., 4G or 5G), more users watch Internet nology (e.g.,4G or 5G), more users watch Internet videos via cellular networks on mobile devices. According to Cisco’s report, mobile videos will generate more than three-quarters of mobile data traffic by 2021 [1]. Better system designs and effective video delivery techniques are desired for mobile videos to attract more users watching mobile videos [2], [3]. State-of-the-art ABR algorithms [4], [5], [6], [7] are proposed to improve user QoE by adaptively selecting video bitrate according to the network conditions. However, these studies mainly focus on broadband or WiFi networks, and the ABR algorithms may perform poorly under cellular networks. For example, the highly dynamic cellular network causes the ABR algorithms to choose an improper bitrate. Mobile videos under cellular network are more complicated for existing ABR algorithms because of 1) different network environments for mobile users, 2) the mobility of users when watching mobile videos, and 3) wild throughput fluctuations even in a specific network environment.

As the global average throughput of cellular network reached up to 13.2 M bps in 2018 [1], video-centric mobile applications became more and more popular, like short videos, live videos, and video on demand. Though mobile video streaming becomes increasingly popular, today’s video providers still conduct ABR algorithms [8], [9], [10] regardless of potential properties in cellular networks. Stateof-the-art ABR studies [4], [5], [6], [7] also mainly focus on broadband and WiFi. These ABR algorithms differ in strategies for video bitrate adaptation to network conditions. The difference comes from the main challenge in ABR algorithm design: adapting to various and dynamic network conditions (e.g., design efficient and accurate network models for throughput prediction) [5], [11], [12], [13].

When using cellular networks, the wild throughput fluctuation makes it ever challenging to give an accurate future throughput prediction [1]. To the best of our knowledge, there is little work done studying the properties of cellular networks for mobile videos, i.e., 4G or 5G technology in the real world and using potential insights to improve the quality of mobile video streaming. In mobile video streaming, the predicted throughput with a large error will affect the bitrate selection in the ABR algorithm and result in a wrong bitrate decision. We revisited state-of-the-art ABR algorithms under cellular network (e.g., 4G) and summarized performance issues as follows: 1) MPC [4] predicts network throughput by the harmonic mean of history throughputs and uses the expected future throughput for bitrate selection. But it suffers from low prediction accuracy when the network throughput fluctuates wildly over time, especially under cellular networks. 2) Cross session stateful predictor (CS2P) [5] approach finds global Markov property in broadband throughput of a short period. It utilizes global Markov property to improve the throughput prediction accuracy for broadband networks. 3) Oboe [7] uses a network modeling technique that segments the network trace as piecewise stationary processes. Though these studies achieve good performance for video quality under broadband or WiFi network, it remains to be proven whether the performance of the algorithms still holds under the cellular network.

To validate the performance of prior ABR algorithms under cellular networks, we collect cellular network traces on our own. We are also interested in studying the properties of throughput traces under cellular networks. To this end, we collect throughput traces for cellular networks (mostly 4G) over 4 months using mobile phones and open-source speed test codes [14]. By testing prior ABR algorithms in our dataset, we find that all the algorithms suffer from performance degradation (i.e., QoE sacrifice). The reason is mainly due to a big error in predicting future network throughput or state in cellular networks as compared to broadband and WiFi networks.

Specifically, we find that traditional network prediction techniques such as harmonic mean [4], global Markov property [5], and piecewise-stationary modeling [7] perform poorly in our dataset. An accurate throughput prediction technique is required for high-quality mobile video streaming. To improve the throughput prediction accuracy, we use time-series analysis to study the properties of throughput traces in our dataset. By making a scatter plot for throughput traces, we observe an important property of the cellular network, i.e., environment-specific Markov property. We find that once the network environment is identified (e.g., in the bus), the property of throughput traces is more Markov like and holds over time, which inspires us to use it for throughput prediction.

The environment-specific Markov property is evident. However, there are questions we need to consider before using it in adaptive mobile video streaming, like 1) how many types of network environment should be studied to characterize the property correctly and 2) at which level can we use the specific network environments (e.g., the environment-specific property may vary from user to user and location to location). To address the above questions, we make the following efforts. We conduct data collection on different types of environments. For example, we collect the throughput traces of indoor (laboratories, offices, bedrooms, dining halls), moving buses (about 20 different lines), and open air (streets, parks, playgrounds). 1 We conduct our data measurement over four months covering two cities, Beijing and Suzhou in China. We find that it is confusing to find a useful property when mixing all throughput traces. However, we observe the Markov property when considering a specific environment, and it does not have to be specified into a detailed location. For example, when we look at all throughput traces from a bus, the traces show Markov property that holds over time. Though we may get a more accurate Markov property if we focus on each line of the bus, it is not feasible in real video players. Thus we use the environment-specific Markov property at the level of indoor, moving bus, and open air.

Accordingly, we propose a technique named NEIVA that performs accurate future throughput prediction in cellular networks and incorporate state-of-the-art ABR algorithm MPC [4] for mobile video streaming. To use the environment-specific Markov property for throughput prediction in NEIVA, we take the following steps: 1) We train offline Markov model using throughput traces from each environment. 2) We identify which environment the video player belongs to (environment identification). 3) We use the Markov model of the identified environment in

1. For a specific environment, for example, though we did not count the number of streets, we measured across quite a number of different streets in our measurement.

<table><tr><td rowspan="2">Method</td><td colspan="2">Prediction error</td><td colspan="3">Performance on quality metrics</td></tr><tr><td>Median</td><td>Avg</td><td>AvgBit</td><td>Rebuf</td><td>BitSw</td></tr><tr><td>LS</td><td>26.2%</td><td>38.6%</td><td>3.6Mbps</td><td>0.38s</td><td>0.44Mbps</td></tr><tr><td>HM</td><td>21.1%</td><td>35.7%</td><td>3.6Mbps</td><td>0.36s</td><td>0.31Mbps</td></tr><tr><td>ARMA</td><td>17.4%</td><td>29.6%</td><td>3.7Mbps</td><td>0.41s</td><td>0.43Mbps</td></tr><tr><td>LASSO</td><td>17.7%</td><td>28.5%</td><td>3.8Mbps</td><td>0.50s</td><td>0.16Mbps</td></tr><tr><td>NEIVA</td><td>13.5%</td><td>22.7%</td><td>3.4Mbps</td><td>0.11s</td><td>0.24Mbps</td></tr></table>

TABLE 1: Summary of primary experiment results for NEIVA and existing methods. The prediction error is calculated by Equation 1. We directly show the performance of individual QoE components under mobile video streaming, i.e., average bitrate (AvgBit), average rebuffering time (Rebuf), and average bitrate switch (BitSw).

step 2 for future throughput prediction. When a video plays, NEIVA identifies the environment and uses the environment-specific Markov model for future throughput prediction. Then it executes the ABR algorithm for online bitrate selection. Concerning the accuracy of identification, we can assume that the server can acknowledge the environment information via the smart device’s location or user input. We also make an effort to identify the environment, relying purely on history throughput samples. Specifically, we train multi-layer perceptron (MLP) using parameters shown in Table 4, which achieves 72% identification accuracy on average.

We implement NEIVA in our testbed, i.e., HTTP based video emulator mahimahi [15] for video playback. We also incorporate NEIVA with state-of-the-art ABR algorithm MPC [4] for experiments. We evaluate the throughput prediction accuracy of the cellular network and the video quality in mobile video streaming, comparing to commonly used throughput predictors, i.e., Last Sample (LS), Harmonic Mean (HM [4]), Auto Regression Moving Average (ARMA [16]), and Lasso Regression (Lasso [17]). We summarize the result in Table 1. The result shows that NEIVA outperforms existing throughput predictors on average absolute prediction error by 20% − 25%. For the performance of NEIVA in adaptive mobile video streaming with MPC, NEIVA achieves minimal rebuffering time (0.11s per chunk) and gains 11% − 20% average QoE improvement. Since the bitrate of the video is discrete, such as 4M bps and 8M bps for two consecutive video chunks, the video bitrate selected by two predictors may be the same even if the values of the predicted throughput are different. This explains why the improvement of NEIVA on QoE is a bit smaller than throughput prediction accuracy. NEIVA takes a step for mobile video streaming, especially with the popular 4G and emerging 5G technologies, which indicates a broader space to deliver mobile videos in the future.

The remainder of the paper is organized as follows: Section 2 introduces the background of adaptive video streaming and revisits state-of-the-art ABR algorithms for mobile videos. Section 3 introduces the measurement of throughput trace under cellular networks and the analysis of prior work under the dataset. Section 4 presents the detail of NEIVA, including modeling and prediction techniques for mobile videos. Section 5 evaluates NEIVA’s performance on throughput prediction accuracy and video quality (QoE). Section 6 discusses the potential benefits of reinforcement learning-based ABR algorithm from NEIVA and deployment concerns for mobile video streaming. Section 7 lists some related works, and Section 8 concludes our work.

# 2 BACKGROUND AND MOTIVATION

# 2.1 Adaptive Video Streaming over Internet

Today’s internet videos are usually delivered over HTTP, like adaptive video streaming over HTTP (DASH) [8]. By delivering video via HTTP, DASH is compatible with heterogeneous networks (e.g., broadband network, WiFi, and cellular network) and edge devices (e.g., laptops, smart phones, and TVs). In DASH, the video is cut into chunks with the same time length, e.g., 4 seconds. Each video chunk is encoded into different bitrate copies and stored in a video server or content delivery network. When the video player plays a video, it requests a video chunk of selected bitrate one by one.

DASH is the referenced structure of adaptive video streaming since the video player can adaptively select video bitrate according to network conditions. However, the user QoE may be affected when the network is poor, such as the low bitrate video playback or video rebuffering.

ABR algorithms are widely used to select bitrate adaptively according to network conditions to ensure highquality internet adaptive video streaming. The basic idea of ABR algorithms is to balance the trade-off between video quality metrics, such as rebuffering time and average bitrate. Prior works usually use QoE metrics like average bitrate, rebuffering time, and bitrate switch [19], [20]. By formulating the QoE metrics into a quantified QoE function, the algorithms can optimize the overall user QoE [5], [7], [21].

# 2.2 Revisit State-of-the-art ABR Algorithms for Mobile Videos

Given prior excellent ABR algorithms, to the best of our knowledge, they are all designed towards broadband or WiFi network. MPC [4] uses a model predictive controlbased optimizing technique to select video bitrates, given the expectation of future network throughput. Though MPC uses a simple network throughput prediction method, i.e., harmonic mean, it significantly outperforms pilot techniques. Further, CS2P [5] and Oboe [7] take a step forward in video quality improvement by accurately capturing future network throughput states in ABR algorithms. Prior studies are designed towards WiFi or broadband network and do not keep up with good performance under the advanced cellular network, such as 4G or 5G network. For example, though the average throughput of the 4G network was 13.2 M bps in 2018 [1], the network dynamics are quite diverse across various environments.2 Even in a specific environment, the mobility of users may also raise violent throughput fluctuations. For example, for users who watch videos on the bus, the network conditions will frequently change with the bus moving and passengers getting on/off the bus (changing network condition).

Hence we are motivated to validate the performance of state-of-the-art ABR algorithms under cellular networks. A

2. For example, broadband and WiFi networks are usually used under indoor environment, while cellular network covers more complicated environments, like indoor, open air and moving vehicles.

<table><tr><td>trace amount</td><td>200</td><td>250</td><td>300</td><td>350</td><td>400</td><td>450</td><td>500</td></tr><tr><td> $T_{online}/T_{offline}$ </td><td>446</td><td>518</td><td>574</td><td>619</td><td>705</td><td>817</td><td>932</td></tr></table>

TABLE 2: Time cost comparison between CS2P and offline Markov model for throughput prediction.

simple way is directly downloading the open datasets of throughput traces from the Internet, like [22], [23], [24]. However, we find that the traces are not suitable for our study in that 1) the HSDPA dataset is collected along with a series of locations without timestamps [22], [23], 2) the broadband dataset mixes all throughput samples, which can not be separated into throughput traces [24]. Thus we collect throughput traces of the cellular network by ourselves and leave the detail of our dataset in the next section. We summarize our validation results of prior ABR algorithms in our dataset as follows:

Accuracy of network throughput prediction. Previous algorithms such as MPC [4] conduct simple prediction methods, i.e., last sample (LS) and harmonic mean (HM) with low network throughput prediction accuracy. In our dataset, the 50-percentile throughput prediction errors for HM and LS are above 20.0%, while the 75-percentile errors are above 39.0%.

Overheads for online data collection. While CS2P [5] achieves a better throughput prediction accuracy, it requires the server to collect network throughput traces online for the model update, which induces significant overheads. We compare the time cost (total time spent to predict future throughput) between the online model CS2P $\bar { T } _ { o n l i n e }$ (online trace collecting and model training) and the offline model $T _ { o f f l i n e }$ (offline training3). We set the number of collected traces increasing from 200 to 500. As shown in Table 2, the time cost of CS2P is about a hundred to thousand times higher than the offline model and still increases with an increasing number of throughput traces. We also observe that the global Markov property used in CS2P does not persist under cellular networks.

Effectiveness of network model. In the network state identification-based ABR approach, Oboe [7] proposes a piecewise-stationary model to capture future network state and optimize video quality accordingly. 4 The performance of Oboe is highly dependent on its network model. To evaluate its performance under cellular network, we utilize the reference technique in Oboe (change point detection [18], [26] and Augmented Dickey–Fuller test [27]) under our dataset.

As the upper plots in Figure 1 show, we present the examples of segmentation for stationary (trace A) and nonstationary (trace B) throughput traces of cellular network (selected from our dataset) in Oboe. Then we take the Augmented Dickey–Fuller test [27] to test the stationarity of each piecewise traces. In the example, they are both segmented into non-stationary piecewise traces, which is contrary to Oboe’s assumption. Further, we conduct similar tests for all cellular networks throughput traces in our dataset for

3. Offline trained model can be used directly in online throughput prediction.

4. It assumes network traces behave as piecewise stationary process: each network trace is in one specific network state, each of which can be identified according to the stationarity (a stationary process means its mean and variance remain unchanged over time [25]).

![](images/e81bd1e847562e53ffb2bdccf6bd99efb389c7a1757d8497d2131255d6e9bb16.jpg)



(a) Stationary trace

![](images/ee72e2c415cb5c1ffb0a637fc680799030118ae9e122357596d75fbbf4a8b914.jpg)



(b) Non-stationary trace   
Fig. 1: Example of piecewise stationary model segmenting a throughput trace of cellular network into pieces of stationary sub-traces. We conduct the Bayesian online change point detection technique to segment the traces. The bottom plot shows the probability $P ( r u n )$ over the current run length (or time since the last change point [18]) at each point of a network trace. Notice that the drops of solid red lines to the zero run-length correspond with the abrupt changes in the throughput. We denote the piecewise traces shown between the vertical red dotted lines in the top plots. By examining the sub-traces via the Augmented Dickey–Fuller test, we find that all piecewise sub-traces in figure (a) and (b) are non-stationary.

TABLE 3: Overview of our dataset. 

<table><tr><td rowspan="2">Test time rangeEnv. (test interval)</td><td colspan="3">SpeedTestMay 25 2018 to September 30 2018 $^{1}$ </td></tr><tr><td>indoor (5-10s)</td><td>open air (1-3s)</td><td>bus (1-2s)</td></tr><tr><td>Trace count</td><td>6249</td><td>742</td><td>670</td></tr><tr><td>5% DL</td><td>24.46</td><td>17.09</td><td>20.56</td></tr><tr><td>50% DL</td><td>15.07</td><td>5.77</td><td>7.28</td></tr><tr><td>95% DL</td><td>2.98</td><td>0.23</td><td>0.00</td></tr><tr><td>Avg. throughput</td><td>14.45</td><td>7.02</td><td>8.26</td></tr><tr><td>Std. deviation</td><td>6.61</td><td>6.19</td><td>6.10</td></tr><tr><td>Non-stationarity</td><td>35.89%</td><td>65.77%</td><td>59.10%</td></tr></table>

Trace number: each throughput trace consists of 100 continuous network throughput values.   
DL: downlink throughput (Mbps). 5%, 50%, 95% are percentiles.   
Non-stationarity: the proportion of non-stationary throughput traces.

Oboe. The result shows that after segmenting the original network trace into piecewise sub-traces, the proportion of non-stationary traces is 49.4% on average. This means that the piecewise-stationary model does not yield the property of the cellular network. And accordingly, though Oboe significantly improves video quality for broadband and WiFi networks, it may perform poorly under cellular networks for mobile videos.

As a result, the state-of-the-art ABR algorithms present poor performance under cellular networks. Existing work requires improvement concerning the properties of cellular networks to improve the quality of mobile videos, which is the purpose of this paper.

# 3 DATA AND PRELIMINARIES

# 3.1 Data Collection

Given the popular use of 4G and its rich share of cellular networks, 4G has put forward many video-based mobile applications. It becomes an ideal network medium for mobile video streaming. Thus we focus on collecting network throughput traces of the 4G network in our study.

The cellular network covers all kinds of environments, such as indoor locations, open air spaces, and mobile vehicles. To collect 4G throughput traces with environment information, we conduct client-side measurement (using mobile phones) rather than collect data from network providers or video players [28]. To this end, we introduce the program of open-source Speedtest code [14] and run it by Qpython [29] on mobile phones. In addition to the original use of Speedtest code, like measuring average throughput, we make some needful modifications for our data collection:

Modifying measurement intervals: we modify the function shell and set timers to download test samples with intervals ranging between 1-10 seconds.   
Reducing download time cost: to measure average network throughput, the original sample files of Speedtest is up to 4 (copies) ∗ 8 (files of different sizes). This may result in up to tens of seconds in the speed test for one time. Given that the video chunks in adaptive video streaming are usually requested in several seconds (like 4s), we reduce the sample files to 1 ∗ 3.   
Recording environment information: to collect information on the network environment, we record the environment type for each time of measuring the network throughput.   
Time series based trace collection: to fit our throughput traces with mobile video streaming, we test network speed one by one in a period. For example, we count every 100 continuous throughput samples with 10 seconds interval as one throughput trace.

We collect data across as many environments as we can. Specifically, we use mobile phones to test network throughput under environments including indoor (laboratories, offices, bedrooms), moving buses (about 20 different lines), and open air (streets, parks, playgrounds). We collect the throughput data for 4 months in two cities Suzhou and Beijing, China. We publish our collected network traces on a repository in GitHub, which is public and visible to anyone (the link is available at [30]).

![](images/f346534a4c05ba5a185e7d1a77b23ed0bd2c782393b28bae11f628da9a09bcec.jpg)



(a) Bus

![](images/3ef3b64671e8fce8f744ca3ef13ae7e51cc4d08bd70c311a71f03c2ad5bac6ce.jpg)



(b) Indoor

![](images/c69be3b99e6ff3cede0249c70b8af38377ab7acca8cf2155548bae67d153076e.jpg)



(c) Open air   
Fig. 2: Scattering plots of consecutive samples in throughput trace of 4G network under bus, indoor and open air, where red circles indicate similar network state (Markov property) for the inner points.

To validate our dataset, we first process the data by eliminating abnormal traces, such as traces with network failure or extremely high throughput points. After data preprocessing, we show the overview of our dataset in Table 3. We summarize the data properties for three high-level types of network environments, indoor, moving bus, and open air. We observe that the standard deviation of cellular network throughput is nearly the average throughput of open air and bus. This indicates that the throughput of cellular networks may drop to zero suddenly even it is normal at the last moment. The fluctuation of network throughput also reflects on the 5, 50, 95 percentile download throughput, e.g., ranging from 0.0M bps to 24.46M bps.

# 3.2 Data Analysis

Given the highly dynamic network throughput in our dataset, we conjecture that this is the main reason for the poor performance of prior studies under cellular networks. We use time series analysis to study the throughput traces and observe an important property, i.e., environmentspecific Markov property. The finding helps us to improve mobile video streaming, e.g., using accurate future throughput prediction.

# 3.2.1 environment-specific Markov property

To study the properties of throughput traces in our dataset, we make scatter plots for the throughput traces directly, with the x-axis denoting network throughput sample test at time T and y-axis test at time T + 1.

Observing scatter plots of different numbers of traces from the dataset, we do not see any significant property until we plot them by the environment. As shown in Figure 2, the property is quite related to the type of environment. We highlight some key points: 1) In the moving bus, the throughput is distributed evenly between 0M bps to 25M bps, following stateful behaviors (e.g., throughput ranges between 3-12M bps mostly transit within 3-12M bps). There is also possible network failing behavior such as throughput 0-23M bps transiting to 0M bps. 2) In indoor locations, the throughput is more likely centralized with high throughput, e.g., the throughput transits within several states between 14M bps and 25M bps. 3) While in the open air spaces, the states for open air range from 0M bps to 20M bps. The throughput tends to centralize at lower throughput (e.g., 0-8M bps) and transits in a narrow range.

![](images/2446fa38f70e35c38efa9fceecc6c22eeebfeedffd3a0c703d29c65c6ffdfc3a.jpg)



Fig. 3: The proportion of main class for a specific environment. The error bars represent the standard deviation for the value.

We call the stateful behavior of throughput traces under a specific network environment as environment-specific Markov property. As we randomly choose throughput traces from the dataset, we observe that the stateful Markov property presents similar patterns given a specific environment. Note that even though the throughput traces are collected in 4 months, the environment-specific Markov property persists over time.

# 3.2.2 Using environment-specific Markov property in mobile videos.

Given the environment-specific Markov property of cellular network throughput traces, we are motivated to use it to improve mobile video quality. But before that, we still have several straightforward questions to answer: 1) How many types of network environments should be studied so that we can say the property we find is general? 2) To what extent can we use the environment-specific Markov property, as the property may vary from user to user, location to location? 3) If we can use the property to predict future network states accurately, how can we integrate the property with video players as most of the video players do not capture environment information?

First, we collect throughput traces of cellular networks from the environments of indoor, moving bus, and open air. For each type of environment, we also conduct data measurement in different places, such as tens of bus lines, many different streets, and various indoor locations (offices, labs, family rooms, etc.). Though the real-world environment is diverse, our dataset covers the types of environments that support environment-specific property through numerical results.

For the second question, we would like to enumerate two cases of levels of the environment. 1) Low-level environments: specific to a user and location, the Markov property may be used to predict future network conditions more accurately. However, it is not feasible to deploy in video players for mobile video streaming, as it will require Markov model training and testing for every user and location. 2) High-level environments: it is feasible since we can train the Markov model over all data beforehand and use it online. But it leaves a questio of whether we can predict the network condition accurately or not. As we use the idea to predict future throughput under our dataset, we find that the prediction accuracy is lower than that of simple methods like the last sample method.

As we observe the environment-specific Markov property in Figure 2, we use the Markov property for throughput prediction in indoor, moving bus and open air, respectively. Using the environment-specific Markov property brings significant accuracy improvement over pilot predictors, as shown in Figure 8. We leave the detail of the test in Section 5 for readability and discuss the last question.

Given the environment-specific Markov property of cellular networks, we are going to discuss its feasibility in video players. Note that video players do not capture the environment information, but one method of doing this is getting the information via mobile users. However, it may annoy the user if the video player requires the user to feedback before watching videos. Hence we study whether we can identify the environment relying purely on network throughput traces. Since the Markov property of the cellular network is environment-specific, we are encouraged to use the property for environment identification. We use clustering algorithms k-means, birch, and hierarchical for throughput traces in our dataset. We calculate the proportion of the main class for throughput traces under a specific environment. The main class means that for a specific cluster, the majority of (more than 80%) traces are from the same environment. Furthermore, we check the network environment of each group manually and learn that the throughput traces under the same environment tend to be clustered into one group. As shown in Figure 3, the overall proportion of the main classes reaches up to 65%. It indicates that we can identify environments directly from network traces. Further in Section 4, we introduce a supervised learning algorithm for accurate online environment identification.

# 4 DESIGN OF NEIVA

To improve the quality of mobile videos using environmentspecific Markov property, we propose NEIVA, a technique that incorporates accurate throughput prediction with ABR algorithms. The design of NEIVA is divided into two stages, offline training and online predicting.

![](images/baad8886a75f4ad1f4c6519e180a1e06536bf10be10b05f198eb8327e152ecee.jpg)



Fig. 4: Overview of NEIVA.

The offline training process includes Markov model training from throughput traces in a specific environment and environment identifier training. For the online predicting process, NEIVA first identifies the environment type via history throughput samples. Then it uses the Markov model corresponding to the environment trained beforehand to predict future throughput when the video plays. Each time the video player requests a new video chunk, NEIVA selects an environment-specific model to predict future throughput and tells the ABR controller its prediction result.

One thing worth noting is that our data measurement and network modeling are both video streaming centric. For example, we collect time-series based throughput traces with 1 − 10 seconds interval, which is set according to the download time of each video chunk and is determined by the chunk size and network throughput. As ABR algorithms select video bitrate to fit network conditions, i.e., it keeps draining out rate of buffer comparable to buffer filling rate (video play vs. video download). The download time is usually close to the length of the chunk (e.g., 4s). By modeling the cellular network as environment-specific hidden Markov models, NEIVA is designed with ABR algorithms for mobile videos, rather than a general network throughput prediction technique.

# 4.1 Overview

We present an overview of NEIVA in Figure 4. We first look at the top part or offline training stage consisting of the following steps:

Data processing. As shown in the section on data analysis, we mentioned that the throughput traces generate stateful behaviors that can be used for throughput prediction. To fit throughput traces to the Markov property, we transform the throughput trace into a series of throughput pairs (feature extraction).   
Hidden Markov model (HMM) training. Given the distinct Markov property across environments, we use the processed data for HMM training for throughput traces of a specific environment, i.e., indoor, bus, and open air, respectively.   
Environment identifier training. Given the HMM models, it remains to be decided which model to use

![](images/da216eba9b25a9c962f441a0f503ccca5248daf0374c21d02f1866297e9f9bc9.jpg)



Fig. 5: Overview of HMM.

for online throughput prediction. For example, if a user watches a video on the bus with an HMM model trained from the indoor environment, the model will get even a worse throughput prediction result. To address the issue, we infer environments directly from throughput traces by a supervised classifier algorithm, e.g., multi-layer perceptron. The identifier is trained offline and used for online environment identification.

While at the online predicting stage, as shown in the bottom part in Figure 4, NEIVA integrates the Markov model and environment identifier as an online throughput predictor. NEIVA also incorporates its throughput predictor with state-of-the-art ABR algorithm for the video play: NEIVA first collects the network throughput samples when the user begins watching a video. For each video chunk to be selected, NEIVA infers the type of environment based on collected throughput samples. Then it selects the corresponding Markov model to predict future network throughput and sends the result to the ABR controller.

As the environment identifier of NEIVA requires several throughput samples (e.g., 10 samples) as input, it leads to the freezing of NEIVA at the beginning of the video. However, requiring several samples does not mean we should use a whole process of chunk download to get one throughput sample. We find that dash.js will periodically (tens of milliseconds) log intermediate throughput samples for each video chunk [7], [8]. We can directly use these throughput samples for environment identification. In this way, we can get enough throughput samples to startup NEIVA quickly after the video begins to play.

# 4.2 Data Processing

To utilize the stateful behaviors shown in Figure 2, we are inspired to transform the throughput into a sequential network throughput pair instead of raw throughput trace.

Formally, we denote the trace T races under a specific network environment as a time series sequence: the throughput $B _ { i }$ denotes the random variable of actual throughput $b _ { i } ,$ where $i \in \{ 1 , 2 , 3 , \dotsc , n - 1 \}$ , denotes the time sequence and $b _ { i }$ is a non-negative real number. In throughput prediction, we define the absolute prediction error as:

$$
\operatorname{Err} \left(\hat {b} _ {i}, b _ {i}\right) = \frac {\left| \hat {b} _ {i} - b _ {i} \right|}{b _ {i}} \tag {1}
$$

where $\hat { b } _ { i }$ denotes the predicted value of the actual throughput $b _ { i } , b _ { i } \geq 0$ (we set $b _ { i }$ to 0.01 to avoid dividing by zero in the equation).

![](images/3ff582efa6d37b4f6ff9d7aaa6eca2e32215799dffd20ccbea6516daa41b2a9f.jpg)



Fig. 6: Example of state transition in HMM.

Then a trace $T r a c e _ { s }$ is transformed into two dimension trace array $[ ( b _ { 0 } , b _ { 1 } ) , \dots , ( b _ { i } , b _ { i + 1 } ) ] .$ , where $\textit { i } \in$ $\{ 1 , 2 , 3 , \dotsc , n \dotsc 1 \}$ and the network throughput pair $( b _ { i } , b _ { i + 1 } )$ in the array can be mapped to the point on 2D throughput coordinates as shown in Figure 2.

# 4.3 HMM Training

In this section, we first introduce the HMM modeling technique for the throughput traces. The overview of HMM is shown in Figure 5. We assume that the network throughput pair $( b _ { i } , \bar { b } _ { i + 1 } )$ evolves with transition of hidden states ${ \bar { X } } _ { i } \ \in \ X ,$ , where $\mathcal { X } = \{ x _ { 1 } , x _ { 2 } , . . . , x _ { N } \}$ and i denotes the index of the hidden state. The random variable of $( b _ { i } , b _ { i + 1 } )$ is denoted as $P _ { i } = ( B _ { i } , B _ { i + 1 } )$ and the number of states $N = | { \mathcal { X } } |$ . Given the environment-specific Markov property, the stateful behavior of network throughput under the specific environment can be denoted as the hidden states in HMM. For example, the passengers on the bus share a bottleneck link and the change in the number of passengers generates stateful behaviors. Let $\mathcal { P }$ denotes the probability space. The hidden state behaves as a Markov chain in which the probability distribution of the current state only depends on the last state. For a hidden Markov state, it can be formulated as:

$$
\mathcal {P} (X _ {i} = x _ {i} | X _ {i - 1} = x _ {i - 1}, \dots , X _ {1} = x _ {1}) =
$$

$$
P (X _ {i} = x _ {i} | X _ {i - 1} = x _ {i - 1}) \tag {2}
$$

For the hidden state $X _ { i }$ , we assume the throughput pair random variable $P _ { i }$ follows joint Gaussian distribution (a common distribution assumption that is also used in previous works such as CS2P [5] and Oboe [7]):

$$
P _ {i} | X _ {i} \triangleq (B _ {i}, B _ {i + 1}) | X _ {i} = (b 1, b 2)
$$

$$
\sim (N (\mu_ {b _ {1}}, \sigma_ {b _ {1}} ^ {2}), N (\mu_ {b _ {2}}, \sigma_ {b _ {2}} ^ {2}))) \tag {3}
$$

Under the training dataset, a typical HMM training process is to solve the optimal transition matrix for the hidden states of number ${ \hat { N . } }$ Intuitively, the transition matrix represents the transition probability of the stateful points in Figure 2. As we transform the throughput traces into sequential point sets, HMM is trained to represent the hidden states’ value and transition probability among them. We show an example of a trained HMM with three states in Figure 6. Each state is represented by a mean throughput and variation. The arrow lines denote transition probability among the hidden states.

Given the hidden states number N, we conduct training with throughput traces under the same type of environment to learn HMM. Note that the number of hidden states N needs to be specified beforehand. This leaves a tradeoff to select an appropriate value of N . Smaller N means a simple model but may be insufficient to represent all the possible network behaviors. Larger N models result in more the hidden Markov states. However, it makes the model more complicated and even introduces over-fitting problems. Thus we experiment to find a suitable number of states and discuss it in the parameter configuration section.

Algorithm 1 Throughput Prediction   
Input: pretrained HMM, past throughput $b_{past} = [b_{lh}, \ldots, b_{i-1}]$ Output: predicted throughput $\hat{b}_{i}$ 1: function PREDICT( $b_{past}$ )

2: $\hat{b}_{i} \leftarrow 0$ 3: $s = CLF_{predict}(b_{past})$ 4: model = HMMs

5: $x_{cur} = model.infer(b_{past})$ 6: $\hat{b}_{i} = GetBandwidth(model, x_{cur})$ 7: return $\hat{b}_{i}$ 8: end function

9: function GETBANDWIDTH(model, $x_{cur}$ )

10: $\hat{b}_{i} \leftarrow 0$ 11: for i = 1 to N do

12: $x_{next} = model.state[i]$ 13: mean = model.mean[ $x_{next}$ ]

14: var = model.var[ $x_{next}$ ]

15: samplei = Sample(mean, var)

16: $b_{next} = model.transmat[x_{cur}][x_{next}] * sample_i$ 17: $\hat{b}_{i} = \hat{b}_{i} + b_{next}$ 18: end for

19: return $\hat{b}_{i}$ 20: end function

# 4.4 Predicting Future Throughput

Given a pre-trained HMM model, we can use it to predict future network throughput online. However, there is a question about how to select a specific model corresponding to the environment. From our earlier analysis in Section 3, our goal is to identify the environment directly from throughput traces. Thus we propose two steps for online throughput prediction: network environment identification and HMMbased future throughput prediction.

# 4.4.1 Network environment identification

We conduct an MLP classifier [31] to identify the type of environment. The identifier is trained by throughput traces selected in our dataset with three types of environments: indoor, bus, and open air. We denote the classifier trained in our dataset as CLF . When a video plays, NEIVA records the network throughput $b _ { i }$ where $i \in \{ 1 , 2 , \ldots , n \}$ . To decide the bitrate of a new video chunk each time, the identifier $C L F$ predicts the type of specific environment s directly from the throughput trace:

$$
s = C L F ([ b _ {1}, \dots , b _ {i} ]) \tag {4}
$$

# 4.4.2 Throughput prediction

Given the throughput data, CLF infers the specific environment s. Then NEIVA selects the specific HMM model HMMs for throughput prediction.

To avoid prediction accuracy degradation due to throughput staleness under cellular network [17], we utilize the latest throughput samples for throughput prediction. Let

![](images/2a354fd185340060464b540d5cc93da265c136138f4e62f941b1ceb4597955ed.jpg)



Fig. 7: Configuring hidden state number for specific HMM models in indoor environment, bus, and the open air spaces.

lh denotes the look-ahead steps towards history states for the hidden state inference. Given previous throughput data $b _ { i - l h } , \dots , b _ { i - 1 } ,$ , NEIVA first infers the current hidden state by the maximum likelihood estimate:

$$
x _ {c u r} = \arg \max _ {x \in \mathcal {X}} P (X _ {i} = x | b _ {i - l h}, \dots , b _ {i - 1}) \tag {5}
$$

Then NEIVA predicts the throughput $\hat { b } _ { i + 1 }$ by the first moment estimate from $x _ { c u r } .$

$$
\hat {b} _ {i + 1} = \sum_ {x \in \mathcal {X}} \mathcal {P} (X _ {i + 1} = x | x _ {c u r}) * S a m p l e (\mu_ {x}, \sigma_ {x} ^ {2}) \tag {6}
$$

where x denotes the possible hidden state of the next throughput function. $\hat { S } a m p l e ( \mu , \sigma ^ { 2 } )$ denotes the sample value from Gaussian distribution $N ( \mu , \sigma ^ { 2 } )$ .

The online prediction algorithm is shown in Algorithm 1, by which NEIVA infers the network environment from history throughput samples. Then it selects corresponding model $H \bar { M } \bar { M } _ { s }$ for hidden state inference according to Equation 5. Finally, NEIVA predicts future throughput by Equation 6.

# 4.5 Parameter Configuration

There are two parameter configuration problems to be solved before we can finish our design: 1) deriving the number of hidden states in HMM and 2) learning parameters of MLP based environment identifier.

# 4.5.1 Deriving number of hidden states

To find a suitable number of hidden states N in HMM training, we test several states according to their fitness. Specifically, given a network trace, we can calculate the score of fitness of each HMM on the dataset [32].

We set the test of N in {1, 2, · · · , 100} for each type of environment. The score of fitness over state number N is shown in Figure 7. We can see that the score increases when the number of states increase. However, the increase in score becomes slow when the number of states are more than 30. Note that a larger number of N indicates a more complicated model, so we choose N = 30 in our study.

# 4.5.2 MLP based environment identifier training

As shown in Figure 3, we find the commonly used clustering algorithms can divide traces of the same environment into one class. Given the algorithm is learned unsupervised, it is not suitable since we are going to infer the environment type online. Thus we are motivated to use supervised algorithms to identify specific environments directly from throughput traces.

TABLE 4: Neural network parameter of MLP. 

<table><tr><td>Parameter</td><td>value</td></tr><tr><td>Weight optimization solver</td><td>L-BFGS</td></tr><tr><td>Activation function</td><td>relu</td></tr><tr><td>Tolerance</td><td>1e-5</td></tr><tr><td>Hidden layer sizes</td><td>(10, 50, 40)</td></tr><tr><td>Overall accuracy</td><td>71.6%</td></tr></table>

We use a simple yet efficient supervised neural network algorithm, MLP classifier [31]. MLP trains with backpropagation and learns a non-linear function approximator with multiple hidden layers. As shown in Figure 2, the network throughput traces present distinct Markov property across different environments, which makes the set of throughput traces an ideal candidate for classification.

To achieve a good inference rate on environment type, we randomly select 2000 traces for training and testing. The dataset is partitioned into a train set of 70% data and 30% for the test set. We test the potential combination of parameters in MLP training. We find that by choosing threelayer neurons and relu as activation function, the MLP can well identify environment type. As shown in Table 4, we obtain 71.6% accuracy in our dataset. The overall accuracy of environment identification can be further improved in video players by collecting the location of mobile phones and using the data for more accurate environment inference. In this paper, we use the identifier trained directly from history throughput samples.

# 5 EVALUATION

In this section, we first evaluate the accuracy of throughput prediction between NEIVA and several commonly used predictors. Then we compare the performance of NEIVA and other baseline methods based on state-of-the-art ABR algorithm, MPC [4]. We evaluate two cases of NEIVA: 1) the type of environment is provided by users, and 2) using MLP based identifier for online inference on the type of environment. Given the 20% throughput prediction accuracy gain and the 11% video quality (QoE) improvement, NEIVA outperforms existing throughput based ABR algorithms.

# 5.1 Experiment Methodology

Experiment tools. We build our testbed to emulate mobile video plays under throughput traces of cellular networks. The following tools and open-source code packages are included:

• Mahimahi, HTTP-based video player [15].   
Python machine learning package sklearn for environment identification [33], [34].   
Python HMM learning package for Markov model training [32].

Metrics. To evaluate the performance of throughput prediction and video quality, we use the following metrics:

![](images/ac3a0ada29c38809369013ef61feb09f16ee68afed8f8445160b5e6887341dbe.jpg)



Fig. 8: Comparing absolute error of throughput prediction. The figure shows the cumulative distribution of prediction errors for all throughput traces in our dataset.

Absolute prediction error. We use absolute prediction error to denote the accuracy of throughput prediction, as shown in Equation 1.   
Quantified QoE score. To evaluate the overall video quality, i.e., quantified user QoE, MPC [4] has proposed a QoE function by combining the following video quality metrics linearly: average bitrate, rebuffering time and bitrate switch. We also use this linear format of QoE function for evaluation.

$$
\begin{array}{l} Q o E _ {a v g} = \sum_ {i = 1} ^ {n} \frac {\text { bitrate } [ i ]}{n} - \beta * \sum_ {i = 1} ^ {n} \frac {\text { rebuff } [ i ]}{n} \\ - \gamma * \sum_ {i = 1} ^ {n - 1} \frac {\left| \text {bitrate} [ i ] - \text {bitrate} [ i + 1 ] \right|}{n - 1} \tag {7} \\ \end{array}
$$

where bitrate[i] denotes the bitrate of video chunk i, rebuf f [i] denotes the rebuffering time, and β, γ denotes the weight on rebuffering and smoothness penalty, respectively. We set $\beta ~ = ~ 4 . 3 , ~ \gamma ~ = ~ 1$ in our experiment, same as the parameter setting in MPC [4].

Score of individual video quality metrics. In addition to evaluating the quantified user QoE, we also calculate the value of individual components in the QoE function defined in Equation 7.

Video parameters. We set the video parameters in Mahimahi as follows: The video from the DASH reference client shows that the video bitrate ranges from 250kbps to 15M bps [35]. In our experiment, we use the video bitrate (in kbps), including 900, 2250, 3600, 5400, 8000, and 12000. The video length is 192 seconds, and there are 48 video chunks in each bitrate. The packet payload portion for video chunk request is set to 95% and the link RTT is set to 80ms. In the experiment, we use throughput traces from the same environment for emulation.

Integrating throughput predictor with video player. In our experiment, we implement a throughput predictor in a video player with state-of-the-art ABR algorithm MPC [4]. When a video chunk is downloaded, the video player begins to use MPC to compute the expected QoE for the next video chunk. We first identify the environment via history throughput samples right before selecting a new video chunk each time. The video player selects the corresponding model to predict network throughput. The video player then sends the predicted value of throughput to the ABR controller.

![](images/496086a1b90cb7c98bf6519fab2efaee1f0df0c1213082ae1cebc074a6f0fe01.jpg)



Fig. 9: Comparing NEIVA with baseline throughput predictors on the average QoE. Average QoE values are shown for each predictor.

# 5.2 Throughput Prediction Accuracy

We first compare the accuracy of throughput prediction in NEIVA with commonly used predictors. Specifically, we choose the following approaches as baseline predictors: Last Sample (LS), Harmonic Mean [4] (HM) and machinelearning based approaches, Auto Regression Moving Average (ARMA), and Lasso Regression [17] (Lasso).

For throughput traces of each type of environment, we use the predictors to predict future throughput based on the history sub-trace. For example, given the first half throughput values of one throughput trace (50 network throughput values), we use the predictors to predict the value of the 51st throughput. We process similar tests for all throughput traces in our dataset and calculate the absolute prediction error for every prediction result. As a result, we show the cdf of accuracy for all predictors in Figure 8. Compared with baseline predictors, NEIVA decreases at least 20% absolute prediction error on average. Specifically, the 75-percentile error of NEIVA is 27.0%, and the 50-percentile error is 13.5%.

# 5.3 Performance on Mobile Video Quality

# 5.3.1 NEIVA assisted with environment type feedback

As NEIVA provides accurate network throughput prediction of cellular networks, we are encouraged to evaluate its potential improvement for prior ABR algorithms in mobile video streaming. In this experiment, we implement one of the state-of-the-art ABR algorithms MPC [4] as the controller for video play. We first consider a situation where we can receive feedback on the type of environment from users. We choose 500 network traces from each type of environment for our experiment.

In addition to the original setting of MPC, we also implement the baseline predictors for comparison. We simulate the mobile video play under throughput traces from our dataset, controlled by MPC and a predictor implemented in our testbed. We calculate the average user QoE according to Equation 7 for video plays under each throughput trace. We plot the results into cdf on average QoE for each predictor, as shown in Figure 9. NEIVA achieves better average QoE over the baseline predictors, i.e., we calculate their overall QoE and NEIVA gained 11.3% − 20.0% improvement. Note that the predictor HM is used in the original MPC [4]. NEIVA significantly improves user QoE for mobile videos.

![](images/5efa66760a17f65ab39d45fd6d0c1fb518ab64b3cd07859c126f0da82236cb0c.jpg)



(a) Moving Bus

![](images/043875b95b543991a06f0f866d9f844b7823b22c91a21321e68a46c41217f369.jpg)



(b) Indoor

![](images/5fe5cf0901b43e2aa92359ac6e733381ca899c9518fdffa0019068c271460a5a.jpg)



(c) Open air   
Fig. 10: Comparing NEIVA with existing throughput predictors through the individual QoE metrics, i.e., average bitrate, rebuffering, smoothness (bitrate switch) for each type of environment. Error bars denote the standard deviation for the average value.

To study the performance of NEIVA in-depth, we calculate the value of individual components in the QoE function defined in Equation 7, i.e., average bitrate, rebuffering penalty, and smoothness penalty (bitrate switch). Given the assumption that the users give feedback on the type of environment, we simulate the experiments by using different types of environments. We calculate the average values of all video quality metrics, and the results are shown in Figure 10. From the result, we observe that NEIVA achieves a lower average bitrate compared to other predictors, which decreases user QoE. However, NEIVA significantly reduces the rebuffering penalty, especially for moving buses and open air. As the cellular network condition of indoor is more stable and sufficient, we observe the baseline predictors may poorly perform compared to NEIVA, but not that significantly. While in moving buses and open air, the throughput prediction error of baseline predictors becomes larger and results in more QoE decrease. Our method (NEIVA) performs well across all types of environments and improves average QoE by reducing the rebuffering penalty (time).

![](images/c42dd063fc0c62d78f4397f85e36163af71f08e2b351c58b86b073439aa544d0.jpg)



Fig. 11: Comparing online NEIVA to NEIVA with feedback of environment type, MPC and overall HMM. Normalized QoE score of each ABR algorithm is presented as bars in the figure. Error bars denote the standard deviation on the normalized QoE.

# 5.3.2 NEIVA with online environment identification

Since asking the user to input the type of environment may decrease the quality of experience of watching mobile videos, we are motivated to identify the type of environment directly from throughput traces. For the sake of comparison, we name it as NEIVA Online, integrating an environment identifier trained beforehand.

In the experiment, we implement an overall HMM that assumes the Markov property of cellular networks for all environment types (training all throughput traces in our dataset). We also compare MPC in the experiment and calculate the quantified QoE according to Equation 7. We normalize the scores for comparison, as shown in Figure 11. From the result, NEIVA Online outperforms MPC and overall HMM. While compared to NEIVA (with type of environment feedback), NEIVA Online achieves 86.8% − 99.7% performance for different types of environments. Even without feedback on environment type, NEIVA Online also outperforms MPC for mobile videos. But we still observe the performance gap between NEIVA Online and NEIVA with feedback on environment type. This limits the performance of NEIVA across different types of environments. However, NEIVA Online can perform better in real video players. For example, we can improve the accuracy of environment identification by incorporating a mobile phone’s location (in this paper, we only use network throughput trace for environment identification).

# 5.4 Performance comparison of NEIVA and existing predictors under HSDPA and Broadband dataset

We conduct additional experiments on the performance of NEIVA with existing predictors under HSDPA [22], [23] and broadband [24] dataset. We process the throughput traces by manually adding timestamps (e.g., 5s interval) to fit the format for emulation in Mahimahi [15]. We retrain NEIVA’s predictor using traces from HSDPA and broadband dataset and emulate existing methods for video play via Mahimahi.

The result is shown in Table 5. We observe that ARMA, LASSO, and NEIVA do not perform well under HSDPA and broadband datasets like they do in the 4G dataset shown in Table 1. It indicates that the throughput traces under HSDPA and broadband datasets do not present a useful pattern (even global Markov property) that benefits predicting future throughput. The result shows that the simple predictors, e.g., last sample (LS) and harmonic mean (HM), achieve high average bitrate and low rebuffering time. Since

TABLE 5: Performance of NEIVA under HSDPA and broadband dataset. 

<table><tr><td>Network</td><td>Method</td><td>AvgBit</td><td>Rebuf</td><td>BitSw</td></tr><tr><td rowspan="5">HSDPA</td><td>LS</td><td>0.41Mbps</td><td>0.35s</td><td>0.13Mbps</td></tr><tr><td>HM</td><td>0.41Mbps</td><td>0.36s</td><td>0.12Mbps</td></tr><tr><td>ARMA</td><td>0.41Mbps</td><td>0.36s</td><td>0.10Mbps</td></tr><tr><td>LASSO</td><td>0.42Mbps</td><td>0.38s</td><td>0.13Mbps</td></tr><tr><td>NEIVA</td><td>0.42Mbps</td><td>0.40s</td><td>0.15Mbps</td></tr><tr><td rowspan="5">Broadband</td><td>LS</td><td>2.91Mbps</td><td>0.43s</td><td>0.09Mbps</td></tr><tr><td>HM</td><td>2.91Mbps</td><td>0.44s</td><td>0.08Mbps</td></tr><tr><td>ARMA</td><td>2.91Mbps</td><td>0.44s</td><td>0.09Mbps</td></tr><tr><td>LASSO</td><td>2.92Mbps</td><td>0.46s</td><td>0.07Mbps</td></tr><tr><td>NEIVA</td><td>2.82Mbps</td><td>0.48s</td><td>0.14Mbps</td></tr></table>

we use network throughput along time in the HSDPA and broadband network dataset, i.e., mixing all throughputs, it would be better to use the simple throughput prediction rules. Given that NEIVA uses the environment-specific Markov property via measurements in the wild, it is a step to improving throughput prediction for mobile video streaming in cellular networks.

# 6 DISCUSSION

# 6.1 Validating NEIVA in Different Cities

In general, it would be ideal to train a model under a specific city and use it in the same city. We examine the generality of NEIVA in different cities, e.g., Suzhou and Beijing. Specifically, we train two predictors under throughput traces of Beijing (BJ) and Suzhou (SZ). Then we evaluate the prediction accuracy and average QoE of each predictor on throughput traces of the two cities. The result is shown in Figure 12.

Figure 12 (a) shows that a predictor does perform better on throughput traces from the same city, e.g., predictor BJ achieves lower average absolute prediction error in Beijing than predictor SZ. But the difference is not that significant (i.e., only a 0.3% difference in prediction error occurs when we use both in Suzhou). As shown in Figure 12 (b), the result indicates that we can generally use the environmentspecific Markov property in another city with little decrease in the average QoE. The property can be generalized to cities with similar network conditions. For example, the average network throughputs on buses in Beijing and Suzhou are 8.6 and 7.1M bps, respectively. While for a city with significant difference in the network to Beijing, i.e., a large difference in average network throughput, we can collect throughput traces and re-train NEIVA using throughput traces collected in that city. In this way, we can extend NEIVA to different cities.

# 6.2 Validating NEIVA with Traces Collected in Different Weeks

As shown in Figure 2, we observe that the Markov state is environment-specific and time persistent in cellular networks. In this section, we perform an additional experiment to examine the time persistent property in throughput prediction accuracy. Specifically, we train the predictor of NEIVA each week using indoor throughput traces from June to August. We evaluate the models on predicting future throughput for network traces collected in September and show the result in Figure 13. We observe that the average absolute prediction errors of models trained in different weeks are similar, e.g., ranging from 8% to 12%. The result validates that the environment-specific Markov property shown in Figure 2 is time persistent in throughput prediction.

![](images/3d9a430b6f9a9cf34366c41d77d95b393753393dfba3ca2ec75f575320fe146e.jpg)



(a) Throughput prediction

![](images/754ae7c10f0c0ce77783c206088977af9c0ff59554dc1ec4dc7f1414ea797606.jpg)



(b) Video emulation   
Fig. 12: Comparison of performance between NEIVA’s predictors trained under traces in Beijing (BJ) and Suzhou (SZ). Results of average absolute prediction error in throughput prediction and average user QoE in video emulation are shown in figure (a) and (b). We use 4G traces collected on moving buses from the two cities and evaluate the performance of the predictors on traces in the two cities for space validation tests. Error bars show 95% confidence intervals.

On one hand, collecting throughput traces online introduces additional overhead at the server like computing the network throughput for clients all the time. We also need to ask a user to input his environment information for the server to label throughput traces, which is inconvenient. On the other hand, using more recent throughput traces does not promise a significant performance improvement in the cellular network. The result indicates that in mobile video streaming, we do not have to collect network traces online to achieve potential prediction accuracy improvement. It suggests that we can directly use the model trained using throughput traces collected in the last 3 months for good prediction accuracy.

# 6.3 Potential Environment Transition

Environment transition detection is a part of the throughput prediction. Every time the player requires a new chunk, NEIVA will first identify the environment through the previous throughput samples. Once NEIVA detects that the environment has changed, it will select the corresponding HMM model to predict the throughput. In most cases, the environment should remain the same during the period of watching a mobile video. Even considering the situation of potential environment transition, we can identify the environment periodically and thus change the corresponding prediction model while detecting the change of environment. The video player can also provide user interfaces for the user to select the environment, which addresses the issue though it requires extra user action.

Usually, the environment may not change so fast among indoor locations, moving buses, and open air spaces. However, when the environment lasts for a few seconds, it will result in the wrong selection of the prediction model. For example, we collect throughput samples of the indoor environment online, but the environment quickly transitions to the outdoor. Using the indoor environment samples does

![](images/fa031962398eb1acb43d645666af72e8642bc38a251a362d4035f46e05e9c847.jpg)



Fig. 13: Average prediction errors of models trained under throughput traces collected in weeks from June to August. In our dataset, each model is evaluated in one month traces collected in September. The labels on the x-axis denotes the week number starting from June and the error bars show 95% confidence intervals.

not match the outdoor environment and results in wrong throughput predictions. Generally speaking, the rapid environment change will make all history throughput based methods less effective, including 1) simple methods like last sample and harmonic mean, and 2) model-based methods like NEIVA, CS2P [5], and Oboe [7] because they all use history throughput samples to model the future network state or directly for throughput prediction. However, NEIVA can recover to the right environment quickly since it can collect intermediate throughputs in a short time for environment inference.

# 6.4 Can NEIVA be beneficial for ABR algorithms which do not rely on throughput prediction?

There are a rich number of ABR algorithms proposed for adaptive video streaming, like video buffer-based [36] and throughput-based ABR algorithms [4], [5]. Though the buffer-based ABR does not rely on throughput prediction, it has been proven that the throughput prediction can help improve ABR algorithms [5], [7]. By incorporating one of the state-of-the-art ABR algorithms MPC, NEIVA provides better quality for mobile videos. However, we are also interested in whether NEIVA is beneficial for other state-ofthe-art ABR algorithms or not. For example, we find that the reinforcement learning-based ABR algorithm Pensieve [6] does not rely on future throughput, though it uses history network throughput as input.

Given the excellent performance of Pensieve, we are encouraged to study if NEIVA can benefit Pensieve under cellular networks or not. Like MPC, we implement Pensieve into our testbed using the source code provided by the authors [37]. The input of model training in Pensieve does not contain throughput prediction, and so we cannot directly integrate NEIVA with Pensieve. To study potential improvements, we use the basic idea from NEIVA, i.e., considering a specific environment for Pensieve. Specifically, we first retrain the model of Pensieve using the throughput traces in our dataset. Then we retrain Pensieve using throughput traces under each type of environment (specific models under indoor, moving bus, and open air). We keep the parameters used in Pensieve unchanged to compare the performance of specific models with the retrained model.

TABLE 6: Performance of Pensieve: specific models vs. retrained model. 

<table><tr><td>Metric score</td><td>Specific models</td><td>Retrained model</td></tr><tr><td>Average bitrate</td><td>1.247</td><td>1.130</td></tr><tr><td>Rebuffering</td><td>-0.121</td><td>-0.086</td></tr><tr><td>Bitrate switch</td><td>-0.245</td><td>-0.442</td></tr></table>

We calculate the average scores of video quality metrics 5 of specific models and the retrained model. The result is shown in Table 6. We observe that the average QoE score of specific models is 0.881 (sum of the individual metric scores), and that of the retrained model is 0.602. We conjecture that the improvement can be explained by the different Markov properties of each type of environment. While Oboe [7] finds similar improvement on Pensieve in different ranges of network throughput, e.g., models trained from 0 − 3M bps and 3 − 6M bps will outperform models trained from $0 \mathrm { ~ - ~ } 6 M b p s ,$ , our finding (i.e., the different Markov property of the cellular network), improves stateof-the-art ABR algorithms. Meanwhile, NEIVA’s low cost of computation makes it suitable for deployment in mobile devices for video bitrate selection in real-time.

# 7 RELATED WORK

Video quality metrics: The metrics of video quality have been widely used in recent studies to quantify user QoE. Metrics such as video rebuffering, average bitrate, rendering quality, bitrate switch, and video flickering that can be perceived by users are proved to impact user QoE significantly [19] [38]. While in studies of ABR algorithms, the commonly used quality metrics are rebuffering, average bitrate, and bitrate switch that can be objectively calculated so as to quantify user QoE [4], [6], [7]. Our work also uses the quality metrics, considering a linear combination of quantifying user QoE and individual scores to evaluate the performance of ABR algorithms.

Measurement on Network Throughput Traces: Several approaches that use packet-level probing to estimate the available bandwidth and the capacity of internet paths (e.g., [39], [40]). CS2P [5] collects network throughput traces measured by the video server, which does not require path information like trace route, while we collect throughput traces of cellular networks with mobile phones. This might be slightly different from measuring throughput from video players. However, our measurement can reflect the property of cellular networks for mobile videos in that 1) we set the throughput testing interval relevant to the requesting interval of video chunks (1 − 10 seconds), and 2) we record environment information that can not be measured by the video player.

Throughput prediction in ABR algorithms: Throughput prediction has been proven to be necessary for the performance of ABR algorithms in adaptive video streaming [5], [7], [21]. Prior studies like MPC and BOLA [4], [41] conduct simple throughput prediction methods, such as moving average and harmonic mean. CS2P [5], on the other

5. The score is calculated from the value of the quality metrics multiplied by weights, as shown in Equation 7.

hand, proposes a hidden Markov-based model to cluster clients at the server-side and uses it to improve throughput prediction. Cellscope [17] conducts Lasso regression for throughput prediction in cellular networks. Oboe [7] models network throughputs as piecewise-stationary processes. It tunes the parameter in ABR algorithms according to the network state inferred under its model. Our work follows prior studies on improving throughput prediction accuracy and performance (QoE) of ABR algorithms for mobile video streaming.

# 8 CONCLUSION

In this paper, we deal with adaptive bitrate optimization issues for the increasingly popular mobile video streaming under cellular networks. To study advanced cellular networks under mobile video streaming, we collect 4G network traces from two cities in China for 4 months. From the dataset, we observe the environment-specific Markov property that persists over time. Accordingly, we propose NEIVA to improve throughput prediction accuracy by training the predictor with HMM under specific environments. We integrate NEIVA with state-of-the-art ABR algorithm MPC in our testbed for evaluation. The results show that NEIVA achieves 20% − 25% throughput prediction accuracy gain over baseline predictors and 11% − 20% QoE improvement over MPC. Given the rapid development of cellular network technology (4G and 5G) and the increasing popularity of video-based mobile applications, NEIVA is an advancement in ABR techniques for mobile video streaming.

# 9 ACKNOWLEDGMENTS

This work was supported in part by the National Natural Science Foundation of China (NSFC) for Excellent Young Scholars under Grant 61722210, NSFC Grant 61932013, and NSFC Grant 61532012. (Corresponding author: Jiliang Wang)

# REFERENCES

[1] Cisco, “Cisco visual networking index: Forecast and trends, 2017–2022 white paper,” Feb, 2019, White Paper.   
[2] Y. Wu and G. Cao, “Videomec: a metadata-enhanced crowdsourcing system for mobile videos,” in Acm/ieee International Conference on Information Processing in Sensor Networks, 2017.   
[3] A. Bentaleb, B. Taani, A. C. Begen, C. Timmerer, and R. Zimmermann, “A survey on bitrate adaptation schemes for streaming media over http,” Communications Surveys and Tutorials, IEEE, vol. 21, no. 1, pp. 562–585, 2019.   
[4] X. Yin, A. Jindal, V. Sekar, and B. Sinopoli, “A control-theoretic approach for dynamic adaptive video streaming over http,” in ACM SIGCOMM Computer Communication Review, vol. 45, no. 4. ACM, 2015, pp. 325–338.   
[5] Y. Sun, “Cs2p: Improving video bitrate selection and adaptation with data-driven throughput prediction,” in Proceedings of the 2016 ACM SIGCOMM Conference. ACM, 2016, pp. 272–285.   
[6] H. Mao, R. Netravali, and M. Alizadeh, “Neural adaptive video streaming with pensieve,” in Proceedings of the Conference of the ACM Special Interest Group on Data Communication. ACM, 2017, pp. 197–210.   
[7] Z. Akhtar, “Oboe: auto-tuning video abr algorithms to network conditions,” in Proceedings of the 2018 Conference of the ACM Special Interest Group on Data Communication. ACM, 2018, pp. 44–58.   
[8] DASH, “DASH industry forum,” http://dashif.org/, 2017.   
[9] Adobe, “Adobe http dynamic streaming,” http://www.adobe. com/products/hds-dynamic-streaming.html, 2017.

[10] Microsoft, “Microsoft smooth streaming,” https://www.iis.net/ downloads/microsoft/smooth-streaming, 2017.   
[11] T.-Y. Huang, “Confused, timid, and unstable: picking a video streaming rate is hard,” in Proceedings of the 2012 Internet Measurement Conference. ACM, 2012, pp. 225–238.   
[12] K. Winstein, “Stochastic forecasts achieve high throughput and low delay over cellular network.” in NSDI, vol. 1, no. 1, 2013, pp. 2–3.   
[13] Y. Zaki, “Adaptive congestion control for unpredictable cellular network,” in ACM SIGCOMM Computer Communication Review, vol. 45, no. 4. ACM, 2015, pp. 509–522.   
[14] Sivel, “speedtest-cli,” https://github.com/sivel/speedtest-cli, May, 2018.   
[15] R. Netravali, A. Sivaraman, S. Das, A. Goyal, K. Winstein, J. Mickens, and H. Balakrishnan, “Mahimahi: Accurate record-and-replay for http.” in USENIX Annual Technical Conference, 2015, pp. 417– 429.   
[16] Q. He, C. Dovrolis, and M. Ammar, “On the predictability of large transfer tcp throughput,” Computer Networks, vol. 51, no. 14, pp. 3959–3977, 2007.   
[17] P. Iyer, “Mitigating the latency-accuracy trade-off in mobile data analytics systems,” in Proceedings of the 24th Annual International Conference on Mobile Computing and Networking. ACM, 2018, pp. 513–528.   
[18] “Bayesian changepoint detection.” https://github.com/ hildensia/bayesian changepoint detection, November, 2018.   
[19] F. Dobrian, “Understanding the impact of video quality on user engagement,” in ACM SIGCOMM Computer Communication Review, vol. 41, no. 4. ACM, 2011, pp. 362–373.   
[20] Z. Li, “Toward a practical perceptual video quality metric,” The Netflix Tech Blog, vol. 6, 2016.   
[21] X. K. Zou, “Can accurate predictions improve video streaming in cellular network?” in Proceedings of the 16th International Workshop on Mobile Computing Systems and Applications. ACM, 2015, pp. 57–62.   
[22] H. Riiser, P. Vigmostad, C. Griwodz, and P. Halvorsen, “Commute path bandwidth traces from 3g networks: analysis and applications,” in Proceedings of the 4th ACM Multimedia Systems Conference, 2013, pp. 114–118.   
[23] “Hsdpa dataset,” http://home.ifi.uio.no/paalh/dataset/ hsdpa-tcp-logs/, May, 2018.   
[24] “Fcc measuring broadband america,” https://www.fcc.gov/ actual-area-data, May, 2018.   
[25] H. Pishro-Nik, “Introduction to probability, statistics, and random processes,” 2016.   
[26] R. P. Adams and D. J. MacKay, “Bayesian online changepoint detection,” arXiv preprint arXiv:0710.3742, 2007.   
[27] W. A. Fuller, “Introduction to statistical time series,” Technometrics, vol. 20, no. 2, pp. 211–211, 1996.   
[28] Y. U. Kun, C. Bao, and L. I. Xing, “Internet path performance measurements using web servers,” Qinghua Daxue Xuebao/journal of Tsinghua University, vol. 54, no. 4, pp. 474–479, 2014.   
[29] QuseitLab, “Python on android,” http://www.qpython.com/, May, 2018.   
[30] C. Qiao, “Open dataset of throughput traces in cellular network.” https://github.com/tionry/4GData, May, 2020.   
[31] F. Pedregosa and G. Varoquaux, “Scikit-learn: Multi-layer perceptron,” https://scikit-learn.org/dev/modules/neural networks supervised.html, November, 2018.   
[32] S. Lebedev, “hmmlearn,” https://github.com/hmmlearn/ hmmlearn, November, 2018.   
[33] P. et al., “Scikit-learn: Machine learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.   
[34] L. B. et al., “API design for machine learning software: experiences from the scikit-learn project,” in ECML PKDD Workshop: Languages for Data Mining and Machine Learning, 2013, pp. 108–122.   
[35] “Dash reference page,” https://reference.dashif.org/dash. js/nightly/samples/dash-if-reference-player/index.html, November, 2018.   
[36] T.-Y. Huang, R. Johari, N. McKeown, M. Trunnell, and M. Watson, “A buffer-based approach to rate adaptation: Evidence from a large video streaming service,” in ACM SIGCOMM Computer Communication Review, vol. 44, no. 4. ACM, 2014, pp. 187–198.   
[38] P. Ni, R. Eg, A. Eichhorn, C. Griwodz, and P. Halvorsen, “Flicker effects in adaptive video streaming to handheld devices,” in

[37] Pensieve, “Neural model training,” https://github.com/ hongzimao/pensieve, November, 2018. Proceedings of the 19th ACM international conference on Multimedia. ACM, 2011, pp. 463–472.   
[39] “Pathchar,” http://www.caida.org/tools/utilities/others/ pathchar/, November, 2018.   
[40] N. Hu, L. E. Li, Z. M. Mao, P. Steenkiste, and J. Wang, “Locating internet bottlenecks: Algorithms, measurements, and implications,” in ACM SIGCOMM Computer Communication Review, vol. 34, no. 4. ACM, 2004, pp. 41–54.   
[41] K. Spiteri, R. Urgaonkar, and R. K. Sitaraman, “Bola: Near-optimal bitrate adaptation for online videos,” in IEEE INFOCOM 2016-The 35th Annual IEEE International Conference on Computer Communications. IEEE, 2016, pp. 1–9.

![](images/a1cb460716670f74cbccc189b6c5147c2946a0d3af6629546734e6e25d118cca.jpg)



Chunyu Qiao (Member, IEEE) received the B.E. degree in software engineering from Tsinghua University, China, where he is currently pursuing the Ph.D. degree. His reserch interests include adaptive video streaming, quality of experience, network measurement and big data analysis.

![](images/15d4ca7b5aa96882afec09837b567cdf7f251466272e9150b9c4c1b907e36bd0.jpg)



Gen Li (Member, IEEE) received the B.E. degree in software engineering from Tsinghua University, China, where he is currently pursuing the master degree.

![](images/33825cc483e277a8bddfd6b59d15c8d0f956715c45aa8449daa27f48cb8c6ab4.jpg)



Qiang Ma (Member, IEEE) received his BS degree in Department of Computer Science and Technology from Tsinghua University, China, in 2009, and Ph.D. degree in Department of Computer Science and Engineering at the Hong Kong University of Science and Technology in 2013. He is now an assistant researcher in Tsinghua University. His research interests include sensor networks, mobile computing and data privacy.

![](images/46b214d627960a1e02972e14afe75a8ee83a7a36003beadb5120c456463848f6.jpg)



Jiliang Wang (Member, IEEE) is currently an associate professor in School of Software and TNLIST, Tsinghua University, P.R.China. His research interests include wireless and sensor networks, Internet of Things, and mobile computing. Jiliang Wang received his B.E. degree in Computer Science and Technology from University of Science and Technology of China and his Ph.D. degree in Computer Science and Engineering from Hong Kong University of Science and Technology, respectively.

![](images/b0c1c3a96d500e888cf20ba8cddb774dea35798e84921f90c41ca396c8fb1069.jpg)



Yunhao Liu (Fellow, IEEE) received the B.S. degree in automation from Tsinghua University, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is currently the Dean of GIX, Tsinghua University, and also a faculty member of CSE at MSU (no pay leave). His research interests include AIOT, RFID, sensor networks and pervasive computing. He is a Fellow of the IEEE and

ACM.