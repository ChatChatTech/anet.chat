# Tagoram: Real-Time Tracking of Mobile RFID Tags to High Precision Using COTS Devices

Lei Yang\*, Yekui Chen\*, Xiang-Yang Li\*,†, Chaowei Xiao\*, Mo Li‡, Yunhao Liu\*

\*School of Software and TNLIST, Tsinghua University, China

$^{\dagger}$ Department of Computer Science, Illinois Institute of Technology, USA

$^{\ddagger}$ School of Computer Engineering, Nanyang Technological University, Singapore

young@tagsys.org, yekui@tagsys.org, xli@cs.iit.edu,

xiaocw11@mails.tsinghua.edu.cn, limo@ntu.edu.sg, yunhao@greenorbs.com

# ABSTRACT

In many applications, we have to identify an object and then locate the object to within high precision (centimeter- or millimeter-level). Legacy systems that can provide such accuracy are either expensive or suffering from performance degradation resulting from various impacts, e.g., occlusion for computer vision based approaches.

In this work, we present an RFID-based system, Tagoram, for object localization and tracking using COTS RFID tags and readers. Tracking mobile RFID tags in real time has been a daunting task, especially challenging for achieving high precision. Our system achieves these three goals by leveraging the phase value of the backscattered signal, provided by the COTS RFID readers, to estimate the location of the object. In Tagoram, we exploit the tag's mobility to build a virtual antenna array by using readings from a few physical antennas over a time window. To illustrate the basic idea of our system, we firstly focus on a simple scenario where the tag is moving along a fixed track known to the system. We propose Differential Augmented Hologram (DAH) which will facilitate the instant tracking of the mobile RFID tag to a high precision. We then devise a comprehensive solution to accurately recover the tag's moving trajectories and its locations, relaxing the assumption of knowing tag's track function in advance.

We have implemented the Tagoram system using COTS RFID tags and readers. The system has been tested extensively in the lab environment and used for more than a year in real airline applications. For lab environment, we can track the mobile tags in real time with a millimeter accuracy to a median of 5mm and 7.29mm using linear and circular track respectively. In our year-long large scale baggage sortation systems deployed in two airports, our results from real deployments show that Tagoram can achieve a centimeter-level accuracy to a median of 6.35cm in these real deployments.

# Categories and Subject Descriptors

# C.2 [Computer Systems Organization]: Computer Communications Networks

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

MobiCom'14, September 07-11, 2014, Maui, Hawaii, USA.

Copyright is held by the owner/author(s). Publication rights licensed to ACM.

ACM 978-1-4503-2783-1/14/09 ...\$15.00.

http://dx.doi.org/10.1145/2639108.2639111.

# Keywords

RFID; Tracking; Localization; DAH; Tagoram

# 1. INTRODUCTION

Radio Frequency IDentification (RFID) is a rapidly developing technology which uses RF signals for automatic identification of objects. One of its most promising applications is to track the mobile objects accurately. Many applications would benefit from higher tracking accuracy. For example, supermarkets can deeply mine the consumers' shopping habits by monitoring the items' trajectories. Similarly, it is useful to conduct automatic recognition of complex multi-player behaviors through the tagged football in a world-wide game. Plenty of new battery-free human-machine interactive device can be developed using the tags, like writing letters in the air by attaching a tag on a finger. Exact tracking information is also indispensable for some emerging RFID applications like automated customer checkout. Today's robots routinely replace human labor in assembly tasks. It has been of a great interest in both the robotics academic community and industry to enable robot search for a desired object, pick it up, fetch and delivery it from a assembly lines. These tasks require tracking the object to cm-level and even mm-level accuracy $[1]$ . Another typical application is the object sortation. Slightest tracking error may result in incorrect baggage sortation and delivery in airport. According to the report of our partner airline operator, Hainan Airline, over 90% of its baggage losses are due to the tracking and sorting error on the airport conveyors. In this paper, we target at the problem of tracking mobile RFID tags at high precision (cm- and mm-level), in order to meet the needs of challenging applications.

Existing RFID localization techniques cannot be directly applied due to the following reasons. First, to the best of our knowledge there are seldom reported approaches that can achieve high precision of localization accuracy, especially for mobile tags. Second, many RFID localization approaches (e.g., $[2–10]$ ) rely on pre-deployed reference tags for accurate calibration, which is infeasible for a tracking system spanning a long pipeline (e.g., the sortation line in the airport). Third, the mobile tag experiences fast-changing environment with non-ideal communication conditions such as multipath reflections of RF signals, varied orientation of tags, etc., which fail most existing localization techniques for their assumption on static communication environment.

In this paper, we design Tagoram, which exploits the phase value of received signal for real-time tracking of mobile tags with a high precision. We observe that the COTS RFID products support fine-grained resolution in detecting the phase of received RF signals, i.e., with accuracy $\approx$ 0.0015 radians. This accuracy offers an opportunity to locate the object with accuracy of millimeter-level displacement. Developing a practical system out of the basic principle, however, entails substantial challenges. First, the RF phase measurement is affected by the basic thermal noise at the receiver side, which results in the practically measured RF phase a random variable following Gaussian distribution. How to derive a definite and accurate tracking result from the indefinite phase measurement remains challenging. Second, the device diversity in phase measurement introduces extra phase shifts we call “diversity term”. Different RFID tags or readers have different diversity terms. Prior calibration of all tags and readers is impractical and computationally infeasible and we need to carefully sidestep the problem. Third, the fast changing environment makes the phase measurement a complex result mixing RF propagation through the line-of-sight (LOS) with the None LOS. It is hard to separate them and thus non-trivial to accurately derive the tag position. We propose a hologram based approach, called Tagoram, to tackle above challenges using COTS RFID tags and readers with a few physical antennas. We build an RF phase hologram with observations from different reader antennas and at different time of scan. To tackle the challenges of mobile tags, we assume the antennas moving to the opposite direction relative to the mobile tag. Such fictitious reader “mobility” offers individual RF phase observations from different positions relative to the tag, and they form an RF hologram as if they were obtained from a virtual antenna array. If the tag movement velocity and its moving track is known in advance, the positions of the antenna array relative to the tag can be determined. We can thus rely on the instant hologram to derive the initial position of the tag and thus precisely track the tag movement. In order to tackle previously identified challenges we further develop Differential Augmented Hologram (DAH) approach from the naive one. The details will be elaborated in §4. In §5, we then relax the assumption that we know the tag moving track in advance and devise a technique to accurately recover the tag movement from antenna observations. We first identify a series of candidate tag moving paths using the continuously estimated tag velocity from the antenna array. Then DAH is extended to identify the one with the highest likelihood of generating the observed RF phases. To enable real-time localization and tracking, we propose several techniques to speedup the computation of hologram.

Summary of results: We implement Tagoram using a COTS reader equipped with 4 antennas (see §6). We first conduct extensive testbed experiments in indoor environment with all communication irregularities and compare with RSS [2], OTrak [3], PinIt [6] and BackPos [9] in §7. The tags are attached to objects moving on different tracks. In our result, Tagoram achieves mm-level accuracy to a median of 5mm and 7.29mm under linear and circular track respectively using DAH, offering about 82×, 21×, 16× and 55× improvement compared to above four methods, in a controllable case where the track is known and without need of reference tags. Even in an uncontrollable case with 4 antennas, Tagoram can still achieve centimeter accuracy to a median error distance of 12.3cm. In addition, Tagoram adopts a strategy of incremental computation to generate the final hologram. Our experiment shows that it only takes about 2.5 seconds to get a high accuracy. For most of real time application, especially for the control of mechanical system like sorting or assembly system, it is within an acceptable level.

We then perform large scale trial studies in tracking RFID tagged baggages with real airport baggage sortation systems, presented in §8. We develop a customized device with multi-antenna equipped RFID reader, called TrackPoint. Ten TrackPoints are deployed for automatic baggage sortation in two of the busiest airports in China, Beijing Capital International Airport (BCIA T1) and Sanya Phoenix International Airport (SPIA). Long term pilot studies have been launched since January 2013. The trial studies have by far consumed 110,000 RFID tags. 12 billion traced records were collected during the study. In this practical application environment millions of baggages were conveyed and there exist various metal transport vehicles that create rich multipath signal reflections. The practical tracking results show that Tagoram achieves a centimeter-level accuracy to a median error distance of 6.35cm.

![](images/e1742741e836b75225fc40adc32e7bf629cb93ba67a15262ba26e1e2a5da52eb.jpg)



Figure 1: Backscatter communication

Contribution: To summarize, we made the following contributions: First, to best of our knowledge, Tagoram is the first system that can successfully limit the negative impact of the multipath phenomena and the phase measurement error (caused by thermal noise and tag diversity). Second, we design and implement the Tagoram system, purely based on COTS RFID products which makes the fast adoption and deployment possible. Third, we systematically evaluate the system under indoor environment and two sorting environment at two airports. As a result, Tagoram can provide real-time tracking of mobile tags with a high precision.

The rest of the paper is organized as follows. We present the background and preliminary studies in §2. The main design of Tagoram is overviewed in §3. We present the details of Tagoram for controlled moving trajectory using DAH in §4 and uncontrolled trajectory in §5. The implementation of Tagoram is described in §6 and evaluated in §7 and §8. We review the related work in §9 and conclude our work in §10.

# 2. BACKGROUND

Passive RFID system communicates using a backscatter radio link. The tags, no battery equipped, purely harvest energy from the reader's signal. Fig. 1 illustrates a conceptual diagram of the backscatter communication between a reader and a passive tag. The wireless signal from the reader's antenna induces a voltage on the tag's antenna and the radiated wave makes its way back to the reader's antenna, induces a voltage, and therefore produces a signal that can be detected: a backscatter signal. The tag modulates its data on the backscatter signals using ON-OFF keying through changing the impedance on its antenna. A COTS reader is usually connected to 4 directional antennas. These antennas transmit signals alternatively in exclusive time-slots to avoid the reader collision. The tag orientation is defined as the angle between the reader antenna's polarization direction and the tag's antenna.

RF phase: The RF phase is a common parameter supported by COTS readers. Suppose $d$ is the distance between the reader antenna and the tag, the signal traverses a total distance of $2d$ back and forth in backscatter communication. Besides the RF phase rotation over distance, the reader's transmitter, the tag's reflection characteristic, and the reader's receiver circuits will all introduce some additional phase rotations, denoted as $\theta_T$ , $\theta_{TAG}$ and $\theta_R$ respectively. The total phase rotation [11] output by the reader can be expressed as

$$
\left\{ \begin{array}{l} \theta = \left(\frac {2 \pi}{\lambda} \times 2 d + c\right) \bmod 2 \pi \\ c = \theta_ {T} + \theta_ {R} + \theta_ {T A G} \end{array} \right. \tag {1}
$$

where $\lambda$ is the wavelength. The term c is called diversity term, which is related to the hardware characteristics. The phase is a periodic function with period $2\pi$ radians which repeats every $\lambda/2$ in the distance of backscatter communication. Most modern COTS RFID readers, e.g. ImpinJ R420 [12], are able to report the $\theta$ as a phase difference of transmitted and received signal. One RF phase estimate is output each time a tag that is successfully interrogated, depending on the individual antenna and channel. A typical UHF reader has 16 channels working at $920 \sim 926$ MHz ISM band. Thus, the resolution can be achieved 0.0015 radians in theory, thereby offering $\approx 320mm * 0.0015/(4 \times 3.14) = 0.038mm$ ranging resolution $^{1}$ . Such ultra-high resolution makes the RF phase an attractive indicator for mm-level localization and tracking.

Challenges and empirical studies: (i) The phase estimate is derived from the received signal where the thermal noise from reader receiver is always present, leading to measurement errors. We conduct an empirical studies over 100 tags with environment temperature from $0^{\circ}$ to $40^{\circ}\mathrm{C}$ , various frequencies $(920\sim 926\mathrm{MHz})$ including 16 channels, and RSS from -70 to -30dbm (different orientations). One set of the results measured at the $5^{th}$ channel is depicted in Fig. 2(a). These experiments suggest that the phase measurement results contain random errors, following a typical Gaussian distribution with a standard deviation of 0.1 radians. In the following sections, we will consider the phase measurement as a Gaussian random variable instead of an accurate value. (ii) To validate the existence of tag's diversity on RF phase. We place 70 tags at a same position in turn. Each tag is interrogated for 100 times and the average value is reported in Fig. 2(b). We observe that the measured phase values are distributed among $0.3007\sim 5.8438$ radians. Such an observation suggests that the tag's diversity takes impact on phase measurement and cannot be ignored in practice. We also perform the Kolmogorov-Smirnov test (KS-test) to study their predictability. These values pass the test to be verified over a uniform distribution with 0.5 significant level, which means that the tag diversity is hard to infer. In summary, both the thermal noise and tag diversity challenge the phase measurement and further affect the tracking accuracy, which were not fully studied previously.

# 3. TAGORAM OVERVIEW

Tagoram is an RFID-based practical tracking system towards mobile objects. As a running example, we mainly present the system in the context of conveyor or assembly task. Tagoram's technique applies to a variety of tracking applications, including robot manipulation.

# 3.1 Scope

Ultra-low cost of UHF tags (5-10 cents each) become the preferred choice of many industry applications. Following the common practices, we concentrate on the tracking of UHF tags in this paper. Today's COTS readers have an operating range of around $10m$ [12]. In this work, we focus on locating and tracking mobile tags that are not moving at a high speed. As presented in [13]

![](images/e2e103894146f6dba74a6bddf11a8dca1171ea7de4bdce132261f9de5df3bf0e.jpg)



(a) Phase distribution

![](images/de4014109de78fc3ca084370f5eccdae9986be66d0bbef47acf4cca70a43f2fd.jpg)



(b) Tag diversity   
Figure 2: Empirical studies on measured RF phase. (a) The phase obeys a Gaussian distribution. (b) The diversity takes an impact on measured phase.

(we had similar observations in our experiments) the system suffers from serious packet loss when the tag moves with a high speed, resulting that the tag even cannot be interrogated. Thus, our system considers the case where tags move with a relative low speed.

# 3.2 Problem Definition

We consider the mobile RFID tag tracking applications, where the tags move within a surveillance region monitored by M RF antennas, denoted as $A = \{A_{1}, A_{2}, \cdots, A_{M}\}$ , with known locations. These antennas are connected to the same reader and scheduled at different time slots in a round robin approach [14]. For brevity, we use $A_{m}$ to indicate the $m^{th}$ antenna as well as its coordinate. Our approach is mainly presented in 2D surveillance region, but it can be easily extended to 3D space (discussed later in §4.3). The surveillance plane is divided into grids, with W rows and L columns. Suppose the reader has taken N rounds of antennas schedule, there are total $M \times N$ phase measurements so far. Formally, we use a matrix $\Theta$ to denote these measurements.

$$
\Theta = \left( \begin{array}{c c c} \theta_ {1, 1} & \dots & \theta_ {1, N} \\ \vdots & \vdots & \vdots \\ \theta_ {M, 1} & \dots & \theta_ {M, N} \end{array} \right) \tag {2}
$$

The element $\theta_{m,n}$ denotes the $n^{th}$ phase value measured by the $m^{th}$ antenna. Besides the measured values, we also record the time stamps when the phases are measured:

$$
\mathbf {T} = \left( \begin{array}{c c c} t _ {1, 1} & \dots & t _ {1, N} \\ \vdots & \vdots & \vdots \\ t _ {M, 1} & \dots & t _ {M, N} \end{array} \right) = t _ {0} + \left( \begin{array}{c c c} \Delta_ {1, 1} & \dots & \Delta_ {1, N} \\ \vdots & \vdots & \vdots \\ \Delta_ {M, 1} & \dots & \Delta_ {M, N} \end{array} \right) \tag {3}
$$

The element $t_{m,n}$ is the time that the tag is interrogated for $n^{th}$ time by the $m^{th}$ antenna. The time matrix T is normalized based on the time $t_{0}$ . No constraint is put on choice of $t_{0}$ and we always choose the time when the tag is firstly interrogated as the base time, i.e. $t_{0} = \min\{t_{m,n}\}$ , throughout this paper. The $\Delta_{m,n}$ is the time difference, i.e. $\Delta_{m,n} = (t_{m,n} - t_{0})$ . We formally define the tracking problem as follows:

![](images/476c650a081ab5f50bd695549211dd78a9c5fa33ccf18f41e34ebd71153c8331.jpg)



Figure 3: Virtual antenna matrix. The target tag moves from right to left. Total 8 virtual antennas are constructed.

PROBLEM 1. Given $\Theta$ , $\mathbf{T}$ and $\mathcal{A}$ , how to find the tag's trajectory coordinates, i.e. $\{f(t_{1,1}), f(t_{1,2}), \cdots, f(t_{M,N})\}$ , at an arbitrary interrogated time? Here $f(t)$ is the time-dependent trajectory function outputting the tag's coordinate at time $t$ .

The trajectory is a function of time series indicating the trace that a moving object follows through space, which emphasizes the time-space relationship. To avoid the confusion of relevant concept, we define another term, track, indicating the path along which the tag might move. The track is a geometric function, which may formulate a close-loop conveyor belt, a passageway through the building, or a highway based on the road. The track function may be composed by a complex piecewise function but irrelevant to time.

# 3.3 Solution

In this paper, we propose a holistic system, Tagoram, to address the instant tag tracking problem. Tagoram decomposes it into two stages.

\- Controllable Case: First, we consider a simplified case where the tags move along a known track with a constant speed. This case mostly occurs at a conveyor belt or assembly line where the objects are conveyed by a predefined track. Then the trajectory function can be expressed as:

$$
f (t) = f (t _ {0}) + \int_ {t _ {0}} ^ {t} \vec {V} (t) d t \tag {4}
$$

where $\vec{V}(t)$ is the speed function. Note the trajectory function may follow a more complex model but it can be always abstracted as the above equation. The $f(t_0)$ is termed as the initial position where the tag is interrogated at time $t_0$ . As long as the tag's position at time $t_0$ is estimated, its location at an arbitrary time $t$ can be inferred using Equation 4 in combination with the track function. Thus, the main task in this case is to locate the tag's initial position $f(t_0)$ . We present our solution in §4.

\- Uncontrollable Case: We then consider a general case where no prior knowledge about the tag's moving track is known by our system. Thanks to the highly efficient anti-collision capability, the tag can be observed at a high frequency. We approximate its irregular and unpredictable trajectory at run time by exploiting the differentials between consecutive phase values. Then we use the approach introduced in §5 to identify a set of potential trajectories and converting the problem of selecting the optimal trajectory into a task in first stage.

![](images/35bf2ceca28cc85f6d97958a8e94b7471daa2e795cbcc139d7b20e7b4fff5557.jpg)



(a) Waves reinforced

![](images/c0835f5c7bbb97a43eb8c57cdbabaae91353acc9cd609eed85289ab38d9de58f.jpg)



(b) Waves canceled out   
Figure 4: Superimposing the observations from different antennas.

# 4. MOVEMENT WITH KNOWN TRACK

In this section, we discuss the first case in context of conveyor or assembly with known track function and constant speed $\vec{V}(t)$ to find out the mobile tag's trajectory.

# 4.1 Using Virtual Antenna Matrix

As the tag is moving along a trajectory, M physical antennas will interrogate the tag at n different time slots $\{t_{m,1}, t_{m,2}, \cdots, t_{m,n}\}$ . Instead of viewing the tag moves along the known track function, we view each antenna moves in the opposite direction, while the tag stays at a fixed position $f(t_{0})$ without any motion. Thus the collected phase values $\Theta$ is assumed to be collected by a virtual antenna matrix A, denoted as:

$$
\mathbf {A} = \left( \begin{array}{c c c} A _ {1, 1} & \dots & A _ {1, N} \\ \vdots & \vdots & \vdots \\ A _ {M, 1} & \dots & A _ {M, N} \end{array} \right) \tag {5}
$$

where the virtual antenna $A_{m,n}$ is derived from real antenna $A_{m}$ and its relative coordinate to the tag is calculated by:

$$
A _ {m, n} = A _ {m} - \vec {V} \times \Delta_ {m, n} \tag {6}
$$

All of virtual antennas in $\{A_{m,1},\cdots,A_{m,n}\}$ have the same diversity term c. Fig. 3 illustrates an example where the moving tag is interrogated 4 times by two antennas. The tag is firstly interrogated in position $f(t_{0})$ at time $t_{1,1}$ where $t_{0}=t_{1,1}$ . Total 8 virtual antennas are constructed. The virtual antenna $A_{1,1}$ coincides with the real antenna $A_{1}$ .

# 4.2 RF Hologram

The tag's mobility offers individual RF phase observations from these different directions using antenna matrix. The surveillance plane is partitioned into $W \times L$ grids at $mm$ level (less than $1cm$ ). For each grid, we use its centroid as its coordinate. We build an RF hologram with observations from these antennas with different time of scan to derive the $f(t_0)$ . The RF hologram is a likelihood exhibition using an image to display the likelihood that how a partitioned grid in tag's motion plane is likely to be the initial position. We start our technique by presenting a naive straightforward hologram solution and then present techniques that can address the negative impacts of thermal noise and device diversity.

Naive Hologram: Let $h(X, A)$ be the theoretical phase value emitted from antenna $A$ and reflected at grid $X$ . Ignoring the diversity term, $h(X, A)$ can be defined as follows:

$$
h (X, A) = \frac {4 \pi}{\lambda} | X A | \bmod 2 \pi \tag {7}
$$

![](images/9382d152496657cf34535261db999535c3b0f3ca564b0f0bc1d6f4b51efe5398.jpg)



![](images/fe7d70835be874e34c3c4563a69b429b485bc00db61dcd5ffc402d0d402f2103.jpg)



(a) Naive Hologram

![](images/994230c3c90a8e8083bc8c15f0630e00544b5ffa941bed40e5c6571a13b1b3af.jpg)



![](images/3ca502234857a2f0373cf4f087c9db284c7faf99a6230778c8671a22a22068cf.jpg)



(b) Augmented Hologram

![](images/b9fe4ec1cc2223c23c66370d5a7ae3a552575a01a3ceddb08fff3d4110f54764.jpg)



![](images/6957d0d8321eb27736fb96be3e09a2e71a9ca2cf6b9ea79b729c6f035d2220f3.jpg)



(c) Differential Augmented Hologram   
Figure 5: RF Hologram. The RF hologram is an image exhibiting the likelihood that how a partitioned grid is likely to be the initial position. The ground truth is highlighted with plus notation. Three columns show the three kinds of holograms using both 2D image and 3D mesh.

where $|\cdot|$ measures the Euclidean distance between position $A$ and $X$ . An RF Hologram $\mathbf{I}$ is expressed as following image:

$$
\mathbf {I} = \left( \begin{array}{c c c} x _ {1, 1} & \dots & x _ {1, L} \\ \vdots & \vdots & \vdots \\ x _ {1, W} & \dots & x _ {W, L} \end{array} \right) \tag {8}
$$

The image has a resolution of $W \times L$ , in which each pixel $x_{w,l} \in I$ is mapped to a partitioned grid $X_{w,l}$ . The naive hologram is defined as follows.

DEFINITION 1 (NAIVE HOLOGRAM). The naive hologram is an image in which the pixel value $x_{w,l}$ , indicating the likelihood that the corresponding grid $X_{w,i}$ is the initial position, is calculated by

$$
x _ {w, l} = \left| \sum_ {m = 1} ^ {M} \sum_ {n = 1} ^ {N} S (X _ {w, l}, A _ {m, n}, \theta_ {m, n}) \right| \tag {9}
$$

where $S(X, A, \theta) = e^{\mathbf{J}(h(X, A) - \theta)}$ . The term J denotes the imaginary number and the term $e^{J\theta}$ represents a complex exponential signal with unit amplitude.

The pixel value is the amplitude of the summed waves. A key point here is that all measured phase values are viewed to originate from the same initial position as we use a virtual antenna matrix. If the grid X is the initial position, the theoretical phase value equals to the measured one. The vector of the signal $e^{\mathbf{J}(h(X,A)-\theta)}$ will be close to the real axis at positive direction as $h(X,A)-\theta$ approaches 0. All observations from different antennas add up for each other, as shown in Fig. 4(a). Otherwise, when X is not the initial position, $h(X,A)-\theta$ will take a value in $[0,2\pi]$ . Different $S(X,A,\theta)$ will cancel each other, resulting in the final superimposing of these values $\sum_{m,n}S(X,A_{m,n},\theta_{m,n})$ at a low level, as shown in Fig. 4(b).

To illustrate RF hologram in details, an experimental study is performed where two antennas are placed aside the belt and one tag moves through the surveillance plane (detailed methodology is described in §7). In our experiment, a tag is interrogated 220 times by 2 antennas when the tag is moving within the range of the reader, and therefore a virtual antenna matrix with size of $2 \times 220$ are built. The ground truth of initial position is $f(t_0) = (108, 68)$ . The naive hologram and its corresponding 3D-mesh structure are shown in Fig. 5(a). Here light colors denote lower amplitude values. Note that the likelihood is normalized in all figures. From the figure, we can see that at the positions close to the target location $f(t_0)$ , the sum grows as the signals constructively add up to each other. On the other hand, at the positions away from to the $f(t_{0})$ the signals superimpose at random phase angles and the sum is significantly lower. The hologram I suggests a likelihood function of tag being at every possible grid. An RF hologram leverages the statistical correlation to find the optimal solution instead of pursuing accurate analytical solution that might not exist in practice.

Augmented Hologram: We define Peek-Signal-to-Noise-Ratio (PSNR) for a pixel in the hologram:

$$
P S N R (x _ {w, l}) = \frac {x _ {w , l}}{\sum_ {i = 1} ^ {W} \sum_ {j = 1} ^ {L} x _ {i , j}}
$$

Obviously, a pixel with higher PSNR suggests a higher probability that the initial position is at the corresponding grid. In practice, due to the thermal noise, it is hard to catch the exact initial position with the maximum PSNR. As shown in Fig. 5(a), the pixel (122, 35) with maximum PSNR deviates from the ground truth about $358mm$ away. We have to consider all pixels whose PSNRs are greater than a predefined threshold as possible candidate locations. The size of the candidate group determines the tracking error. As Fig. 5(a) depicts, the hologram cannot give distinctive result about the initial position. There exists a large continuous region with relatively high PSNRs.

In naive RF hologram, the amplitudes of signal $e^{\mathbf{J}(h(X,A)-\theta)}$ are uniformly set to one because the measured amplitude, i.e. RSS, is notably distorted as a result of the severe multipath environment. As aforementioned, the measured phase $\theta_{m,n}$ , affected by the thermal noise, is a random variable that follows a typical Gaussian distribution i.e. $\theta_{m,n} \sim \mathcal{N}(\mu,\sigma)$ . Suppose the tag is at $X_{w,l}$ , its phase expectation measured by antenna $A_{m,n}$ is $h(X_{w,l}, A_{m,n})$ , thereby, $h(X_{w,l}, A_{m,n}) - \theta_{m,n} \sim \mathcal{N}(0,\sigma)$ . The standard deviation $\sigma$ is caused by the receiver's thermal noise being irrelevant to the distance. Based on the experiments presented in §2, we adopt $\sigma = 0.1$ in following sections. To reduce the impact of receiver's thermal noise, we propose Augmented Hologram (AH) by assigning a virtual amplitude $\|S\|$ .

DEFINITION 2 (AH). The augmented hologram is an image in which the pixel value $x_{w,l}$ is calculated by

$$
x _ {w, l} = \left| \sum_ {m = 1} ^ {M} \sum_ {n = 1} ^ {N} \| S (X _ {w, l}, A _ {m, n}, \theta_ {m, n}) \| S (X _ {w, l}, A _ {m, n}, \theta_ {m, n}) \right| \tag {10}
$$

$$
w h e r e \left\{ \begin{array}{l} \| S (X, A, \theta) \| = 2 \times F (| h (X, A) - \theta |; 0, 0. 1) \\ F (x; \mu , \sigma) = \frac {1}{\sigma \sqrt {2 \pi}} \int_ {x} ^ {\infty} \exp \left(- \frac {(t - \mu) ^ {2}}{2 \sigma^ {2}}\right) d t \end{array} \right.
$$

and $F(x;\mu,\sigma)$ is the cumulative probability function of Gaussian distribution $\mathcal{N}(\mu,\sigma)$ .

The assigned amplitude $\|S(X_{w,l}, A_{m,n}, \theta_{m,n})\|$ is the cumulative probability that the measured phase is emitted from $A_{m,n}$ and backscattered at grid $X_{w,l}$ . Doing so enhances the amplitude of these waves with higher probability and weakens others. In effect, those pixels whose measured phase values are very close to theoretical values, are augmented in the hologram. Fig. 5(b) depicts the augmented hologram using the same observed data as those in Fig. 5(a). We see that AH breaks up the large continuous region that has higher PSNRs into several points and reinforces the initial position.

Differential Augmented Hologram: From the augmented hologram, we find that there still exist some candidate positions with higher PSNR, distributed around the ground truth. These few spots make the tracking error around 200mm. We believe these ambiguities are caused by the device diversity across different antennas. The measured phase $\theta$ equals to $h(X, A) + c$ . Assume tag's initial position is at grid T, then

$$
S (X, A, \theta) = e ^ {\mathbf {J} (h (X, A) - (h (T, A) + c))}
$$

In theory, the maximum amplitude should happen when X = T. In practice, the energy is spread across grids X that $h(X, A) = h(T, A) + c$ . As each antenna takes a different impact on the c, the uncalibrated $\theta$ violates our basic assumption that the phase measured by each virtual antenna would originate from the initial position. To eliminate such influence caused by the diversity term, we further propose Differential Augmented Hologram (DAH) redefining a new virtual signal S.

DEFINITION 3 (DAH). The differential augmented hologram is an image in which the pixel value is calculated by

$$
x _ {w, l} = \left| \sum_ {m = 1} ^ {M} \sum_ {n = 1} ^ {N} \| \mathbb {S} (X _ {w, l}, A _ {m, n}, \theta_ {m, n}) \| \mathbb {S} (X _ {w, l}, A _ {m, n}, \theta_ {m, n}) \right| \tag {11}
$$

where

$$
\left\{ \begin{array}{l} \mathbb {S} (X _ {w, l}, A _ {m, n}, \theta_ {m, n}) = e ^ {\mathbf {J} \theta_ {d i f}} \\ \| \mathbb {S} (X _ {w, l}, A _ {m, n}, \theta_ {m, n}) \| = 2 \times F (| \theta_ {d i f} |; 0, 0. 1 \times \sqrt {2}) \\ \theta_ {d i f} = (h (X _ {w, l}, A _ {m, n}) - \theta_ {m, n}) - (h (X _ {w, l}, A _ {m, 1}) - \theta_ {m, 1})) \end{array} \right.
$$

The virtual signal $e^{\mathbf{J}\theta_{\mathrm{dif}}}$ is constructed using the difference of phase difference. We reconstruct the virtual signal $\mathbb{S}$ . Note that $(h(X_{w,l},A_{m,n}) - \theta_{m,n}) - (h(X_{w,l},A_{m,1}) - \theta_{m,1}) = (h(X_{w,l},A_{m,n}) - (h(T,A_{m,n}) + c)) - (h(X_{w,l},A_{m,1}) - (h(T,A_{m,1}) + c)) = h(X_{w,l},A_{m,n}) - h(T,A_{m,n}) + h(T,A_{m,1}) - h(X_{w,l},A_{m,1})$ . A key observation here is that the diversity term $c$ is eliminated through subtracting the measured phase difference from the theoretical difference between the $A_{m,n}$ and $A_{m,1}$ . Since each row of virtual antennas $A_{m,n}$ is derived from a same physical antenna $A_{m}$ and each row of phase measurements $\theta_{m,n}$ are taken by the same antenna $A_{m}$ , so the subtraction is treated differently for different rows. For each row, we choose the first virtual antenna as the calibration base. In addition, the $\theta_{\mathrm{dif}}$ introduces subtraction of two random variables, $\theta_{m,n}$ and $\theta_{m,1}$ . Notice that $(h(X_{w,l},A_{m,n}) - \theta_{m,n})\sim \mathcal{N}(0,\sigma)$ and $(h(X_{w,l},A_{m,1}) - \theta_{m,1})\sim \mathcal{N}(0,\sigma)$ , then $\theta_{dif}\sim \mathcal{N}(0,\sqrt{2}\times \sigma)$ , so we set the $\sigma$ of cumulative probability function to $0.1 \times \sqrt{2}$ instead of 0.1. In addition, another benefit from phase difference is able to eliminate the impact of doppler effect, because $\theta_{m,1} \sim \theta_{m,n}$ almost contains the equal phase deviation caused by the doppler effect, during a small sampling interval. Fig. 5(c) shows that the correct initial position has an extremely intensive PSNR that approximately exceeds $2\times$ than those in other pixels. The error can be reduced to within 10mm.

# 4.3 Achieving Realtime Tracking

The computations involved in deriving DAH may introduce much overhead, thus jeopardize the real time tracking capability. The problem will be more severe for applications where the tracking in the 3D space rather than a 2D plane. Suppose the reader's read zone is approximately considered as a cuboid with a size of $W \times L \times H$ , the reader's read zone is partitioned into $H$ planes, each of which has a size of $W \times L$ . The extracted initial position located in the grid which related pixel has the higher PSNR among $H$ holograms. Compared with 2D scenario, the computations required are increased thousands of times for 3D scenario.

# 4.3.1 Hashtable on Phase

Reviewing the 2D-hologram in Fig. 5(c), we find that the majority of pixels have low PSNR values (blue) in hologram, where the related computations are not necessary. It can reduce computation time if these pixels are ignored. In fact, given a measured phase $\theta_{m,n}$ , we can find out a group of arcs originated from antenna $A_{m,n}$ , across which the grid X meets $h(X, A_{m,n}) = \theta_{m,n}$ , called as candidate grid. Obviously, the initial position definitely do not locate in non-candidate grids. This inspires us to find a way of quickly releasing these candidate grids and ignoring others for saving computations. We implement the idea using a hashtable.

Hashtable construction: Assume the antennas locate at origin first and address this issue later, we traverse each grid X within the read zone, calculate the phase $\theta$ emitting from origin and backscattered at X, and hash the grid to the phase table. A COTS reader supports 0.00015 radians phase resolution where the reported phase is encoded with 12 bits, so each phase table contains $2^{12} = 4096$ entries.

Applying: When applying, the antenna's coordinate $A_{m,n}$ as well as its measured phase $\theta_{m,n}$ are input. Using $\lambda_{m,n}$ and $\theta_{m,n}$ can obtain a set of candidate grids from the hashtable, i.e. $C_{m,n} = \{X|h(X,0) = \theta_{m,n}\}$ . However, due to the thermal noise, the measured phase vibrates with a standard deviation of $\sigma$ radians. To tolerate the vibration, all grids whose calculated phase within $[\theta_{m,n} - \sigma, \theta_{m,n} + \sigma]$ should be all fetched and merged, i.e. $C_{m,n} = \{X||h(X,0) - \theta_{m,n}| \leq \sigma\}$ . The hashtable is built on the assumption that the antenna locates at origin while the antenna is at $A_{m,n}$ in practice. We must translate the origin to $A_{m,n}$ . It is equivalent to translating the selected grids by a vector of $A_{m,n}$ , i.e. $X + \vec{A}_{m,n}$ , i.e. $C_{m,n} = \{X + \vec{A}_{m,n}||h(X,0) - \theta_{m,n}| \leq \sigma\}$ . In theory, the initial position must be inside the common intersected grid of these candidate sets. However, there might not exist a common intersection among them at all because of multipath effect, i.e. $\bigcap_{i=1,j=1}^{M,N} C_{m,n} = \emptyset$ . Hence, all candidate grids which are included at least three candidate sets should be involved in the hologram generation.

The hashtable reduces the computations from two aspects: First, the majority of grids are non-candidate and can be ignored. Second, our experiments show that 70% of computation time are consumed to resolve Euclidean distance in $h(X, A)$ . The hashtable makes this part of computation not needed any more. Our evaluations show that the hashtable reduces 60% of computations.

![](images/459c7ef86ea0981079b7380cf3d43fba1d134f0f45fd534b7012fe04381d0a7f.jpg)



Figure 6: Modeling tag's movement. Each antenna estimates a tag's radial velocity component along the direction between them.

# 4.3.2 Incremental Generation

It appears that the entire hologram is generated once enough phase measurements are collected. Actually, the generation is an incremental process. The sum in Eqn. (12) can be decomposed into a superimpose of $M \times N$ sub-holograms. Correspondingly, the computation can be decomposed into many time windows every time a read is collected. Usually, the tag is interrogated about 30 times per second so that the time window equals 0.03s, which is long enough to generate a sub-hologram. Therefore, our approach is able to guarantee the realtime object tracking at second level.

# 5. MOVEMENT WITH UNKNOWN TRACK

In this section, we relax the assumption that tag's track function is known in prior. Tagarom deals with the unpredictable movement with the following two steps:

- Fitting tag's trajectory: Tagoram acquires the phase measured by $M$ antennas from different directions to fit tag's trajectory every round of antenna scheduled.   
- Selecting the optimal trajectory: Tagoram utilizes the DAH to evaluate all fitted trajectories and selects the optimal one corresponding to the pixel with maximum PSNR.

Below we describe these two steps in detail.

# 5.1 Fitting Tag's Trajectory

A tag can be interrogated for about 30 times per second in COTS RFID system [12] while the most advanced automatic sorting system [15] supports a maximum conveyor velocity of $274.8mm / s$ . On average, the tag moves about $274.8 * \frac{1}{30} = 9.16mm$ , which is far less than half a wavelength of available channel ( $\approx 160mm$ ). This feature motivates us to estimate the tag's radical speed through the phase difference of two adjacent reads. As illustrated in Fig. 6, the tag's displacement $\Delta d$ during two adjacent reads $\theta_{m,n}$ and $\theta_{m,n+1}$ for antenna $A_m$ can be approximated using Eq. (1):

$$
\Delta d = \left\{ \begin{array}{l l} \frac {\theta_ {m , n + 1} - \theta_ {m , n}}{4 \pi} \times \lambda , & | \theta_ {m, n} - \theta_ {m, n + 1} | <   \pi \\ \frac {(2 \pi - \theta_ {m , n} + \theta_ {m , n + 1})}{4 \pi} \times \lambda , & \theta_ {m, n} - \theta_ {m, n + 1} \geq \pi \\ \frac {\theta_ {m , n + 1} - \theta_ {m , n} - 2 \pi}{4 \pi} \times \lambda , & \theta_ {m, n} - \theta_ {m, n + 1} \leq - \pi \end{array} \right. \tag {12}
$$

Note that since above equation has taken a phase difference for given $m^{th}$ antenna, the antenna dependent diversity term has been naturally eliminated. On the other hand, $\Delta d \ll |f(t_{m,n}) - A_{m}|$ , then it is reasonable to approximate tag's displacement along the radical direction i.e. $A_{m} \to f(t_{m,n})$ , equal to $\Delta d$ . Further, the radical instant speed $\widehat{V}_{m,n}$ can be estimated as follows:

$$
\left\{ \begin{array}{l} \widetilde {V} _ {m, n} \approx \frac {\Delta d}{t _ {m , n + 1} - t _ {m , n}} \\ \angle \widetilde {V} _ {m, n} \approx \angle (f (t _ {n}) - A _ {m}) \end{array} \right. \tag {13}
$$

$\angle X$ is the vector $X$ 's direction, defined as the angle with $x$ -axis. For completeness, we give an applicable upper band on the tag's speed, $160mm/0.033s = 484.9mm/s$ .

Speed chain: There are m real antennas monitoring the surveillance region, so we can estimate m instant radical speeds every round of antenna schedule. The displacement between any two adjacent reads is so small that we simply model the tag's movement during a round as a uniform linear motion. The entire trajectory can be well approximated by a piecewise linear curve. As shown in Fig. 6, let $\vec{V}_{n}$ denote the tag's real speed during the $n^{th}$ round, and $\vec{V}_{m,n}$ be the radical speed measured by the $m^{th}$ antenna during the $n^{th}$ round. Actually, $\vec{V}_{m,n}$ is the instant projection of $\vec{V}_{n}$ at direction of $A_{m} \rightarrow f(t_{m,n})$ , namely:

$$
| \vec {V} _ {m, n} | = | \vec {V} _ {n} | \cos (\angle \vec {V} _ {n} - \angle \vec {V} _ {m, n}) \tag {14}
$$

Above equation has two unknown parameters, the tag's speed magnitude $|\vec{V}_n|$ and direction $\angle \vec{V}_n$ . In theory, given two arbitrary estimated radical speeds in different directions, both parameters can be solved. Usually, a typical COTS RFID system supplies $M \geq 3$ antennas in practice, which yields $\binom{M}{2}$ resolutions. So we adopt fitting method to estimate the two parameters. The problem is formalized as follows:

$$
\min \left| V _ {m, n} - \widetilde {V} _ {m, n} \right| \underset {\sim} {\sim} \underset {\sim} {\sim} \underset {\sim} {\sim} \underset {\sim} {\sim} \tag {15}
$$

subject to: $\{(\widetilde{V}_{1,n},\angle\widetilde{V}_{1,n}),\cdots,(\widetilde{V}_{M,n},\angle\widetilde{V}_{M,n})\}$

We adopt the nonlinear least squares to estimate the tag's instant speed $\vec{V}_n$ in $n^{th}$ schedule, and use the GaussNewton method which is based on a linear approximation of the objective function in the neighborhood of parameter vector. We start with an initial approximation of the parameter vector and iteratively update this parameter vector until it converges to a local minimum of an objective function. When every round of antenna scheduling ends, a group of measurements are obtained and the tag's speed during this schedule can be fitted. Since we have $N$ schedules for now, the output is actually a chain of tag's speeds:

$$
\mathcal {V} = \{\vec {V} _ {1}, \dots , \vec {V} _ {N} \}
$$

Trajectory function: We segment tag's trajectory into a serials of uniform linear movements in each round. The trajectory can be obtained using following recursive equation:

$$
f (t _ {n}) = f (t _ {n - 1}) + (t _ {n} - t _ {n - 1}) \cdot \vec {V} _ {n} = f (t _ {0}) + \sum_ {k = 1} ^ {n} (t _ {k} - t _ {k - 1}) \cdot \vec {V} _ {k} \tag {16}
$$

where $\vec{V}_k\in \mathcal{V}$ . As long as we know the initial position $f(t_0)$ , the tag's trajectory can be recursively inferred. Note that the optimized method, such as Kalman filter [10], can be utilized to address the measurement noise, which is not discussed in this paper due to the space limit.

# 5.2 Selecting the Optimal Trajectory

Although the trajectory can be approximately calculated through Eqn. (16), there still exists an unknown parameter $f(t_{0})$ , namely the initial position. Given an arbitrate $f(t_{0})$ , either way Tagoram can fit a trajectory. Choosing different grid as initial position may result in a different speed chain and further produce different trajectory. Which is the optimal one that most approaches the ground truth? We leverage the DAH to answer this question. Being similar to track the initial position in §4, we assume $f(t_{0}) = X_{w,l}$ and fit a trajectory $f_{w,l}$ . There are total $W \times L$ candidate trajectories. We superimpose all phase measurements along $f_{w,l}$ to $f_{w,l}(t_{0})$ as the same process as tracking initial position using DAH. Our rational behind is that if the fitted trajectory approaches the ground truth, the superimposed amplitude at initial position should reach the maximum among $W \times L$ trajectories. Eventually, the trajectory with high maximum PSNR is selected as the optimal one.

![](images/eef51532906206898b2e1bc0e9994dce34d7df1136d03e06263799603a0f473b.jpg)



(a) Linear Track

![](images/9072aa7436baf73e091f541ffa3c3f3dd2a46e251c9f63c02a7cd3ade2ce9b5e.jpg)



(b) Circular Track   
Figure 7: Experiment setups

# 6. IMPLEMENTATION

We build Tagoram using ImpinJ [12] reader and Alien EPC Gen-2 UHF RFIDs [16]. The system is evaluated both in our lab and a long-term pilot study.

Hardware: We adopt an ImpinJ Speedway modeled R420 reader without any hardware or firmware modification. The reader supports four directional antennas at most, being compatible with EPC Gen2 standard. The whole RFID system operates in the 920 \~ 926 MHz band with frequency hopping. The size of antenna is $225mm \times 225mm \times 40mm$ . The reader is connected to host through the wireless network (TCP/IP). It has local clock and attaches a timestamp for each tag read. We adopt the timestamp provided by the reader instead of the received time as the timing measurement to calculate the phase values, in order to eliminate the influence of network latency. Four reader antennas with circular polarization manufactured by Yeon technology [17] are employed to provide $\geq 8dBic$ gain in two directions. Two types of tags from Alien Corp [16], modeled $2 \times 2 Inlay$ and Squiggle Inlay, are employed. Both of them are employed in our lab experiment and pilot study.

Software: We adopt LLRP protocol $[18]$ to communicate with the reader. ImpinJ reader extends this protocol for supporting the phase report. We adjust the configuration of reader to immediately report reading whenever tag is detected. The software is implemented using Java. In lab experiment, we run the software at a Lenovo PC, which equips Intel(R) Celeron CPU G530 at 2.4 GHz and 2G memory. In our pilot study, it runs at an industrial computers with Atom 1.66GHz, 2G memory, and 16G SSD.

# 7. MICROBENCHMARK

We start with microbenchmark experiments in a testbed environment at our lab with regard to two cases, controllable and uncontrollable case, compared with other methods.

# 7.1 Evaluation in controllable case

We emulate a mobile object via a toy train on which a tag is attached, moving at a constant speed of 0.176m/s on a track. Because an arbitrate track can be decomposed into pieces of linear and arc-shaped tracks in practice, we mainly focus on two basic tracks here.

Linear Track: Two antennas are separated in both sides of the track, as shown in Fig. 7(a). Their distances to the track are $670mm$ and $710mm$ respectively. The width of belt is $1300mm$ . Both the tag's $x$ -axis and $y$ -axis are going to be calculated. Observe that in this testing scenario, the accuracy along $x$ -axis (i.e., track direction) is more important.

Circular Track: We employ a circular track and an RF antenna to measure the accuracy for nonlinear track, as shown in Fig. 7(b). The track's internal diameter is $540mm$ . The distance, from the track's center to the antenna, equals $4000mm$ for accuracy comparison and varies from $1000mm$ to $15000mm$ when discussing its impact on accuracy.

To capture the ground truth with high-accuracy, we install a camera above the track. When the tag is firstly interrogated, the system immediately trigger the camera to take a snapshot on the train, from which the initial position can be identified. When calculating, both tag and antennas are treated as points located in their centroids.

# 7.1.1 Accuracy among different methods

First, we present the accuracy compared with other four localization methods under a controllable environment. We repeat the experiments using five methods over 100 measurements. Fig. 8 plots the final results in which the accuracy is exhibited in x-axis, y-axis and the combination of them. This figure shows the accuracy achieved by RSS, OTrack, PinIt, BackPos and DAH.

RSS: The difference between the RSSs of a pair of tags is used as an indicator for their spatial distance as in past work [2]. Based on the RSS distance, the nearest neighbors of the target tag are identified. The reference tags are deployed aside the track. The RSS scheme has a combined error distance of $600mm$ , suffering from the high variation in behavior across tags, like the antenna gain and tag's orientation.

OTrack: [3] designed a method to determine baggage order via the changes of RSS and read rate. This method focuses on the object sequence conveyed, so there is no result along y-axis. OTrack has a median error distance of 150mm, 75% reduction as compared to the RSS-based scheme.

PinIt: PinIt [6] uses synthetic aperture radar (SAR) created via antenna motion to extract the multipath profiles for each tag, and leverages the reference tags to locate the target tag as same way as RSS based methods. PinIt achieves a mean error distance of 120mm, agreed with the report in [6], using 10 reference tags separated 130mm apart. PinIt is not appropriate in mobile context, because the fast-changing environment violates the tag's multipath profile at every moment, even the movement is very small. In addition, it is not practical to deploy a large number of reference tags on conveyor or assembly line. Even so, their locations become unknown when moving.

BackPos: BackPos [9] is a phase based method, which introduces the technique of hyperbolic positioning in RFID localization. It obtains a mean combined error distance of 400mm and a standard deviation of 200mm. BackPos is anchor-free but sacrifices the area of feasible region.

DAH: Using linear track, our method DAH has a median error distance of 5mm, 13mm and 14mm in x-axis, y-axis and combined dimension, outperforming RSS, OTrack, PinIt and BackPos by 43×, 11×, 8.5× and 28× respectively. This significant improvement is due to the careful consideration of thermal noise and device diversity. The accuracies along the x-axis always are better than y-axis among all methods except OTrack. This is because the tag moves along x-axis providing a relatively larger displacement than y-axis. This verifies that the tag's mobility can improve the tracking accuracy. Since the DAH leverages the statistical results from different directions, its track accuracy is rather stable as well, i.e. standard deviation ≈ 2mm. Fig. 9 plots the CDFs of error measured using the circular track. DAH has a mean error distance of 4.14mm, 4.98mm and 7.29mm in x-axis, y-axis and combined dimension, outperforming others by $82\times$ , $21\times$ , $16\times$ and $55\times$ respectively. Apparently, the accuracy of DAH in circular track is better than that of linear track. In this situation, the accuracies along the x-axis and y-axis perform equally well, because the tag takes almost the same displacement along two dimensions.

![](images/c5a6a682aabfb30d83a9a0604eccc54f4627a561d903a06e95d3d08003fab375.jpg)



Figure 8: Accuracy comparison

![](images/133f28da0519e0b4891c83465c15b7fc789ddce67e33bd42bb2d5552e0afcb35.jpg)



Figure 9: Tracking in circular track

![](images/66c4cc7c209f5439409b323d0eae7f870775b4976db7d774b905407930acdfee.jpg)



Figure 10: Different holograms

![](images/1c2031b170c2f474d2e98854e5b32b4413ff31237b4ef9d0b8cd81712205c367.jpg)



Figure 11: Impact of frequency

![](images/1ff6dce2252183dde5dc1a8447ff447123bfb0c82d1a68e405950044a761f830.jpg)



Figure 12: Impact of orientation

![](images/39d6c46f6b8126ec6d8be1db0b1c6539469b912080f7a760fe989aa48ca2282a.jpg)



Figure 13: Impact of distance

Summary: DAH is able to achieve mm-level accuracy and reliable performance using COTS RFID products under a controllable environment. Our method DAH outputs a significant improvement on the accuracy from three aspects. First, DAH carefully deals with the influences caused by the thermal noise and device diversity. To best of our knowledge, we are the first to address these two issues. Other phase based methods, like PinIt and BackPos, have to perform a set of calibration experiments firstly to eliminate the diversity. However, it is infeasible to do calibrations in practice, especially when confronting thousands of tags, like the baggage sortation in airport. Second, we observe the opportunity that the tag's mobility can help the reader measure its phase from various directions. Most of preview schemes focus on stationary instead of mobile tags, ignoring this important observation. Lots of measurements from different directions can statistically reduce the influence of multipath effect, because the unexpected and unordered wave propagation through NLOS will canceled out for each other, while even a small number of LOS propagations can reinforce amplitudes at initial position. Third, the DAH has ability to eliminate the influences from the Doppler effect, because the similar impacts taken by the Doppler effect during a short interval $t_{m,1} \sim t_{m,n}$ are subtracted by the difference operations of DAH, i.e. $(\theta_{m,n} - \theta_{m,1})$ .

# 7.1.2 Accuracy among different holograms

Next we compare the tacking results among NH, AH and DAH using linear track. Fig. 10 shows their error distances. As we can see, NH has a mean accuracy of 600mm and a standard deviation of 100mm. AH overcomes the deviation coming from the thermal noise and reduces 60% deviation. DAH further removes the influence of device diversity. Its 90th percentile is 18mm, and 99th is 25mm. These experiments fully demonstrate the effectiveness of DAH.

# 7.1.3 Realtime performance

The realtime is an important metric in tracking applications. Next, we investigate Tagoram's delay performance in finding the tag's localization.

Read time. Tagoram takes an incremental process to generate hologram. Once receiving a read from the reader, Tagoram produces an intermediate hologram and superimposes it to the last one. The final hologram is released after enough reads received. So we firstly measure the time taken for generating an intermediate hologram. The results are shown in Fig. 17(a). The read time is the interval during which the reader interrogates two consecutive reads. It is an upper bound which should be taken for producing an intermediate result. The median read time is 33ms. Any computation exceeds this bound might affect the realtime feature.

We can see that the time consumed for a hologram of $10^{3} \times 10^{3}$ resolution without optimization, has a median of 118ms, which far exceeds than $3 \times$ readtime bound. More worse, the time rises several fold as the resolution increases. The generation with optimization using hashtable always keeps a low time cost compared with read time, achieving a median of 25ms even the resolution is up to $10^{5} \times 10^{5}$ . In fact, the main overhead for optimized method is to load the hash table from disk and perform the operation of set intersection, both of which are weakly relevant to the hologram resolution.

Accuracy vs. Realtime. Tagoram outputs the initial position after collecting enough reads. The question here is how many reads are needed to obtain an accurate result? Fig. 17(b) plots the relationship between accuracy and realtime. The result shows that the accuracy tends towards stability when more than 120 reads are collected. Thus, it is reasonable to output a position result after received 120 reads.

Summary: With regard of the time taken for incremental generation, Tagoram needs $120 \times 25ms = 2500ms$ in total for hologram calculation. We believe 2.5 seconds of delay is within an acceptable level for major realtime applications, especially for the control of mechanical system, like conveyor or robot arm. It is worth to note that the real-time partially depends on the efficiency of RFID's anti-collision algorithm.

![](images/9cfe73b440bb41fdec75b11f6ad19dbc2b7e43d73a780181f1c263ff8a2c882f.jpg)



Figure 14: Top view of the track

![](images/c401fdae7cf9375f1092e25e8d573be3227a9e017d29245802340d2a957f46e2.jpg)



Figure 15: Estimated speed

![](images/c17b1959cfb6fdba842269df8a61b9c36fb812df158ca4634d9818675271f1e7.jpg)



Figure 16: Fitted trajectory

![](images/dd14c1a8c58d840e7b9b8773d0f08915910f6dfa1e1a1e9570a1aa1b2cea8b94.jpg)



(a) Read time

![](images/3df05a113f2ae5e1617613084018f461ecd39a8d2401825e506749e24e5db3ea.jpg)



(b) Stability   
Figure 17: Incremental generation

# 7.1.4 Impacts of Parameters

Impact of frequency: A UHF reader hops between 16 channels in the 920 \~ 926 MHz ISM band in China. We look at whether the frequency has impacts on the accuracy of DAH. Fig. 11 plots the accuracy for 16 channels. The results show that DAH is irrelevant to frequency. In fact, it is well known that there exists frequency selective fading in wireless communication. Frequency hopping can help improve the connectivity between reader and tag. Impact of orientation: The tag orientation is defined as the angle between the reader antenna's polarization direction and the tag's antenna as shown in Fig. 1. To measure its influence on our tracking accuracy, we adjust the orientation from 0° to 360° and plot the accuracy in Fig. 12. As expected, the result almost remains a same level. Impact of distance: Fig. 13 shows the accuracy with varying distance from 1m to 12m using circular track. As we can see, its 50th percentile is 9mm, and 90th percentile is 17mm. DAH does not exhibit clear correlation with the distance. Thus, the distance is not a crucial factor affecting DAH's accuracy. Especially, a mean error distance of 5mm can be obtained, when placing the antenna at distance of 12m (22× than displacement the tag takes). In fact, it is more reasonable to model the antenna as a point locating at is centroid when it keeps far away from tag. Summary: These extensive experiment results verify that Tagoram's accuracy is preserved over frequency, orientation and distance changes.

# 7.2 Evaluation in uncontrollable case

We then study the tacking accuracy in a uncontrollable case where the track function is not known in advance. In the experiment, the tag moves along an irregular track, as shown in Fig. 14. Four antennas are deployed around the surveillance region and their coordinates are ( $\pm2000mm$ , $\pm2000mm$ ). Fig. 14 shows a snapshot of the track and the moving toy train. We collect 5 minutes data in total during which the tag moves about 10 laps anticlockwise.

The first step is to estimate the speed chain using the tag's phase values measured by the four antennas. The estimated speed results are shown in Fig. 15. To display the vector clearly in the figure, the speed is magnified by $1000 \times$ , so the speed unit is $mm/s$ . We can see that the estimation has a better effect in the smooth part than the curve part, because we assume the tag takes a linear uniform motion during a schedule window. The estimated speed has a mean of 210.2mm/s while the ground truth speed is 212mm/s. The result is extremely accurate, which demonstrates the effectiveness of Tagoram. Fig. 16 illustrates the final fitted trajectory. In our experiment, the tag's position is produced when every 200 reads are collected. Tagoram achieves a median of 12.3cm accuracy with a standard deviation of 5cm.

# 8. PILOT STUDY

We are collaborating with the Hainan Airline to conduct a RFID-Assisted Sortation System, called TagAssist. The ultimate goal of TagAssist is to pursue a guarantee for the passengers, “Never lose your baggage!” To achieve this goal, TagAssist introduces the RFID technology to conduct automatic baggage tracking and checking services for the goal of eliminating baggage losses. Our design and implementation address many practical issues, while in this discussion, we mainly focus on one key issue that how to accurately track tag on a conveyor system?

We have instrumented our system in two airports, BCIA T1 and SPIA, both of which employ the manual sortation. When the passenger checks in, the agent pulls up the passenger's itinerary on the computer and prints out one or more RFID tags to attach to each pieces of passenger's baggages. To reduce the cost, tens of thousands of baggages enter conveyor system to be transported by a shared conveyor system every day in an airport, resulting that the baggages from different check-in counters are mixed together. It needs human power to separate these baggages according to their flight numbers. The sorting task is finished in the sortation carousel. The sortation carousel is composed of a circularly conveyor used to buffer the baggage, like the baggage claim in arrival hall (see Fig. 18(a)). The baggages are buffered in the carousel until being sorted. It is common to see that the baggages are “thrown” on top of each other in practice.

The sorters, each of who is in charge of sorting a flight of bag-gages, stand by the carousel along the conveyor. His mission is to find out and carry the target baggages from the carousel to the carriage (see Fig. 18(b)). It is an error-prone step for the sorter to pick an expected one out of packs of baggages. To help improve the sorting accuracy and efficiency, we built four large screens (see Fig. 18(e)), to show the tracked baggages' trajectories, assisting the sorters to find out their baggages. In the screen, the baggage carousel is proportionally displayed, where there are lots of small squares in representation of baggages. The baggages from different flights are filled with different colors. With the help of baggage visualization and accurately tracking, the sorter can quickly and clearly catch sight of the bags which he is responsible for, and fast position the baggages when searching them. Therefore, the real-time tracking with high accuracy is necessary, especially in rush hours.

The conveyor system comprises a huge mechanical network and could be hundreds of meters long. It is impossible to deploy hundreds of readers along the conveyor belt for full coverage. So we design and customize a tracking device, called as TrackPoint (see Fig. 18(c)). It composes of one RFID reader and three RF antennas (see Fig. 18(d)), placed across the conveyor. When a tag is passing through the TrackPoint, it is interrogated repeatedly by the reader and tracked using Tagoram with DAH. These devices has been deployed both in BCIA T1 and SPIA, the real industry environment since January 2013. The system has been running for over a year. Each deployment contains 5 TrackPoints (across the conveyor belts), 4 visualization screens (aside the carousels), and 22 RFID Printers (on check-in counters). So far, the study totally consumed 110,000 RFID tags involving 53 destination airports, 93 air lines, and 1,094 flights. We collected 12 billions of RFID reads from TrackPoints. Each read including EPC, RSS, phase and timestamp information.

![](images/0186844843aa374ac0607bd69af2bbd216ef8b9dfa05c80b58e7f276ecad7c14.jpg)



(a) Carousel

![](images/1c625ecfa2f23d20c3bdb58a8fc88924fac6f8fdceb5918eb3802c33ca001859.jpg)



(b) Sorting behavior

![](images/dce47a0eb56a3b90d394c4941acea87f1d7a389febdfe6416e2542a673e2cfbb.jpg)



(c) TrackPoint

![](images/7a403d5d274df1c33037abf5718e85a654ed2f310655f9ef6bd0a583f06b7cc4.jpg)



(d) Components

![](images/23536399e1079e97897576ce6d834f55bd10341c5f094ecd4f2eaaf200409ed5.jpg)



(e) Visualization

Figure 18: Pictures taken from airport. (a) The baggages are conveyed from the check-in counters to the sortation carousel. (b) The sorting behavior is to find and pick the baggages from the carousel to carriages. (c) A TrackPoint is deployed across the conveyor belt. (d) The main components inside the TrackPoint. (e) A screen to show each tag's trajectory assisting the sorters to find their targets.   
![](images/2c7a4a740ccbd0c8d433510e03769b20fb5f436ac7cadd80a82f76624209e750.jpg)



(a) Accuracy

![](images/19ce8add414119086efb3d748eec397256d83247ff92993902ee0f0d935b0fdd.jpg)



(b) Efficiency   
Figure 19: Tracking effectiveness

# 8.1 Tracking Accuracy

Tracking baggages on the conveyor system is a controllable case where the DAH algorithm is adopted. Since the positions of TrackPoints and conveyor velocity are fixed and known in advance, we exactly know how long should the baggage is conveyed from one TrackPoint to another. If the tracking accuracy is precise, this inferred distance should concentrate on the ground truth. So we measure the tracking accuracy by comparing two consecutive tracked distances between two consecutive TrackPoints for a same baggage with the theoretical values. The accuracy is shown in Fig. 19(a) We find Tagoram achieves a median accuracy of 63.5mm. Its 80th percentile is 150mm and 90th percentile is 200mm. Compared with the results in microbenchmark, the main source affecting the tracking accuracy comes from the versatile environment.

# 8.2 Tracking Efficiency

The sortation workspace contains a circularly conveyor for buffering baggages. The baggages will continue to be transported circularly until being sorted. The accurate tracking can help the sorters

![](images/489dad4c7e0a77a37442c9e2a56905b224987e345f9c25b93edc2128e8bfde9f.jpg)



(a) Multipath

![](images/0d3e00ebcbd188c3605c22b9632dc6575ce696362740e881034a1a045859ce23.jpg)



(b) Accuracy   
Figure 20: Tracking robustness to multipath

quickly and correctly find out the target baggages and reduces the unavailing movements. So we employ movement distance of baggage taken on the carousel as a metric to indirectly evaluate the tracking efficiency. Fig. 19(b) shows the moved distance before the baggage is sorted, which decreases about 30% after using Tagoram. This indicates our system indeed enable sorting activities much more efficient.

# 8.3 Tracking Robustness

In practical wireless communication conditions, especially the indoor environments, the signal propagation along NLOS introduces multipath effects which challenges the accuracy in accurate phase measurements. In NLOS, the signals bounce off walls and other objects and arrive at the reader's receivers from multiple directions. We project the received signals into different directions ( $0^{\circ} \sim 180^{\circ}$ ) using the method in [6] to visually display the interference situation. The top four cases occurred are plotted in Fig. 20(a) and their corresponding tracking accuracies are illustrated in Fig. 20(b). In the first case C1, there exist three obvious propagation paths from $140^{\circ}$ , $115^{\circ}$ and $90^{\circ}$ . The localization accuracy is 19mm without much affect. But the accuracy is indeed influenced a little as the number of paths increase. C4 has the most complex environment where there are more than 7 propagation paths and the direction of $20^{\circ}$ and $140^{\circ}$ almost has the same amplitude as ground truth. Even under such serious situation, the accuracy still holds under 60mm. This shows that Tagoram has strong tolerance to multipath effect.

# 9. RELATED WORK

Fine-grained RFID localization has been well studied. These approaches can be classified into three categories.

RSS based methods: Early work on RFID localization is based on RSS. The RSS of reference tags deployed at known positions are recorded and used to locate the target tags $[2–5,19]$ . However, RSS is not a reliable location indicator, especially for UHF tags, which is highly relevant to the tag's orientation and antenna gain [4]. In mobile environment, the orientation cannot be known.

Phase based methods: There is a growing interest in using phase information to locate tags. These methods can be divided into two categories, AoA (Angle of Arrival) and SAR (synthetic aperture). AoA locates the tag by measuring the phase difference between the received signals at different antennas, $[5, 7, 8]$ . The major challenges for these methods are to deal with NLOS. SAR methods are firstly used in Radar system for both object localization and terrain imaging with help of antenna array $[1, 6, 20, 21]$ . PinIt $[6]$ employs a moved antenna to measure the multipath profiles of reference tags at known positions and locates the target tag. The technique of PinIt is further applied in robot object manipulation $[1]$ . The merit of PinIt is able to locate tag in NLOS environment. However, it needs to deploy dense reference tags in advance. Miesen et al. $[20]$ also employ the moving antenna to construct SAR and find out tag's location with naive hologram. Parr $[21]$ extends the technique proposed in $[20]$ in mobile context to determine whether a tag moves along a supposed trajectory. While Tagoram employs tag's mobility to generate Inverse SAR-style antenna array, it significantly differs from previous work in that it focuses on tracking mobile tag in mm-level while dealing with both thermal noise and device diversity. Besides, Tagoram is able to track the mobile tag under uncontrollable case in which the trajectory function is unknown.

Proximity based methods: The last type of localization technique is based on proximity $[22–27]$ . This approach relies on dense deployment of antenna. When the target tag enters in the radio range of an antenna, its location is assumed to be the same as this receiver. Liu et al. present a new communication system that enables two battery-free devices to communicate using ambient RF as the only source of power. which might open a new tracking technique among tags within few centimeter $[25]$ .

# 10. CONCLUSION

In this work we present Tagoram for real-time tracking of mobile RFID tags using Commercial Off-The-Shelf (COTS) RFID tags and readers, to a high precision (cm- and mm-level). A key innovation is to build a differential augmented hologram using the phase values collected from physical antennas, and to leverage the tag mobility to construct a virtual antenna array. Tagoram can pinpoint the tag position to an accuracy of a few centimeter, providing the necessary precision for many novel applications, such as object grasping by robot. The system Tagoram not only has been tested and used in practical applications, but also will open up a wide range of exciting opportunities due to its instant tracking and extremely high accuracy.

# 11. ACKNOWLEDGMENT

This research is partially supported by NSFC under Grant No. 61190110 and NSFC CERG-61361166009. The research of Xiang-Yang Li is partially supported by NSF CNS-1035894, NSF ECCS-1247944, NSF ECCS-1343306, National Natural Science Foundation of China under Grants No. 61170216, No. 61228202. The research of Mo Li is supported from Singapore MOE AcRF Tier 1 grant RG17/13, and Nanyang Assistant Professorship (NAP) grant M4080738.020 of NTU. We thank all the reviewers and shepherds for their valuable comments and helpful suggestions.

# 12. REFERENCES

[1] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus, “Rf-compass: robot object manipulation using rfids,” in Proc. of ACM MobiCom, 2013.   
[2] L. Ni, Y. Liu, Y. Lau, and A. Patil, “Landmarc: Indoor location sensing using active rfid,” Wireless networks, 2004.   
[3] L. Shangguan, Z. Li, Z. Yang, M. Li, and Y. Liu, “Otrack: Order tracking for luggage in mobile rfid systems,” in Proc. of IEEE INFOCOM, 2013.   
[4] J. D. Griffin and G. D. Durgin, “Complete link budgets for backscatter-radio and rfid systems,” IEEE Antennas and Propagation Magazine, vol. 51, no. 2, pp. 11–25, 2009.   
[5] C. Hekimian-Williams, B. Grant, X. Liu, Z. Zhang, and P. Kumar, "Accurate localization of rfid tags using phase difference," in Proc. of IEEE RFID, 2010.   
[6] J. Wang and D. Katabi, “Dude, where’s my card?: Rfid positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.   
[7] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie, "New measurement results for the localization of uhf rfid transponders using an angle of arrival (aoa) approach," in Proc. of IEEE RFID, 2011.   
[8] P. V. Nikitin, R. Martinez, S. Ramamurthy, H. Leland, G. Spiess, and K. Rao, “Phase based spatial identification of uhf rfid tags,” in Proc. of IEEE RFID, 2010.   
[9] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu, “Anchor-free backscatter positioning for rfid tags with high accuracy,” in Proc. of IEEE INFOCOM, 2014.   
[10] S. Sarkka, V. V. Viikari, M. Huusko, and K. Jaakkola, “Phase-based uhf rfid tracking with nonlinear kalman filtering and smoothing,” IEEE Sensors Journal, vol. 12, no. 5, pp. 904–910, 2012.   
[11] ImpinJ, “Speedway revolution reader application note: Low level user data support,” in Speedway Revolution Reader Application Note, 2010.   
[12] “Impinj, Inc,” http://www.impinj.com/.   
[13] P. Zhang, J. Gummeson, and D. Ganesan, “Blink: A high throughput link layer for backscatter communication,” in Proc. of ACM MobiSys, 2012.   
[14] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, “Season: Shelving interference and joint identification in large-scale rfid systems,” in Proc. of IEEE INFOCOM, 2011.   
[15] “Dematic,” http://www.dematic.com/linear-sorters.   
[16] “Alien,” http://www.alientechnology.com/tags.   
[17] “Yeon,” http://www.yeon.com.tw/.   
[18] EPCglobal, “Low level reader protocol (llrp),” 2010.   
[19] G. Li, D. Arnitz, R. Ebelt, U. Muehlmann, K. Witrisal, and M. Vossiek, “Bandwidth dependence of cw ranging to uhf rfid tags in severe multipath environments,” in Proc. of IEEE RFID.   
[20] R. Miesen, F. Kirsch, and M. Vossiek, “Holographic localization of passive uhf rfid transponders,” in Proc. of IEEE RFID, 2011.   
[21] A. Parr, R. Miesen, and M. Vossiek, “Inverse sar approach for localization of moving rfid tags,” in Proc. of IEEE RFID, 2013.   
[22] W. Zhu, J. Cao, Y. Xu, L. Yang, and J. Kong, “Fault-tolerant rfid reader localization based on passive rfid tags,” in Proc. of IEEE INFOCOM, 2012.   
[23] Y. Liu, L. Chen, J. Pei, Q. Chen, and Y. Zhao, “Mining frequent trajectory patterns for activity monitoring using radio frequency tag arrays,” in Proc. of IEEE PerCom, 2007.   
[24] Y. Guo, L. Yang, B. Li, T. Liu, and Y. Liu, “Rollcaller: User-friendly indoor navigation system using human-item spatial relation,” 2014.   
[25] V. Liu, A. Parks, V. Talla, S. Gollakota, D. Wetherall, and J. R. Smith, “Ambient backscatter: Wireless communication out of thin air,” in Proc. of ACM SIGCOMM, 2013.   
[26] Y. Zheng and M. Li, “P-mti: Physical-layer missing tag identification via compressive sensing,” in Proc. of IEEE INFOCOM, 2013.   
[27] L. Yang, Y. Qi, J. Fang, and et al., “Frogeye: Perception of the slightest tag motion,” in Proc. of IEEE INFOCOM, 2014.