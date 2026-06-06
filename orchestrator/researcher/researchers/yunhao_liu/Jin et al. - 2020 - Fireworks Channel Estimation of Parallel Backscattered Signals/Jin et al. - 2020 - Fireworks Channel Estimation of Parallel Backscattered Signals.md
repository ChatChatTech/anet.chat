# Fireworks: Channel Estimation of Parallel Backscattered Signals

Meng Jin $^{1}$ , Yuan He $^{1}$ , Chengkun Jiang $^{1}$ , Yunhao Liu $^{2,1}$

$^{1}$ School of Software and BNRist, Tsinghua University

$^{2}$ Department of Computer Science and Engineering, Michigan State University

{mengj,heyuan}@tsinghua.edu.cn,jck15@mails.tsinghua.edu.cn,yunhao@cse.msu.edu

# ABSTRACT

As the proliferation of backscatter-based applications, exploiting backscatter-based sensing becomes more important. Due to the requirement of accurate estimation of backscatter channels (phase and amplitude), which is often distorted when multiple signals collide with each other, existing works are generally limited to either parallel decoding of collided signals or with non-collided signals only. Motivated by our observation that a channel can be distorted during collisions, the movements of the ON-OFF Keying modulated signal still preserve channel properties of the respective tags, we propose the first approach to channel estimation of parallel backscattered signals, called Fireworks. We model the relationship between the channel and the signal moving trajectory in the In-phase and Quadrature (IQ) domain and implement this design in our lab. The results show that Fireworks is able to estimate up to five channels in parallel. When applied to the tracking application, Fireworks achieves 2\~4× improvement in the tracking accuracy, compared with the state-of-the-art approach.

# CCS CONCEPTS

\- Computer systems organization → Embedded systems; Redundancy; Robotics; • Networks → Network reliability.

# 1 INTRODUCTION

Due to its low cost and battery free feature, backscatter becomes an attractive and promising technology for IoT (Internet of Things). Today, we have seen a huge number of backscatter devices deployed in various industry scenarios, performing functions like warehouse management and supply chain monitoring $[11, 25, 37]$ . With the rapid progress in the area of wireless sensing, recent works propose to exploit the backscattered signals for sensing purposes. The potential applications span across a wide variety of scenarios, such as object tracking, motion recognition, environmental sensing, etc $[5, 12–14, 18, 24, 27, 28, 30, 33, 36, 38, 40–44, 46–48]$ . As the IoT technology gets proliferated, we expect to see more and more backscatter devices deployed in our daily life space.

In spite of the apparent need of backscatter based sensing, the efficiency of the backscatter channel to be used for sensing is far restricted. Backscatter based sensing requires accurate estimation of a backscatter channel in terms of phase and amplitude, which are key indicators of the target's state. When there are multiple targets to be sensed, inevitably their backscattered signals will collide frequently. Collision of signals will distort the backscatter channel, making it extremely difficult to recover the channel state. As a result, the state of arts is limited to either parallel decoding of collided signals $[10, 17, 26]$ or channel estimation with non-collided signals. To be more specific, parallel decoding merely recovers the coarse-grained signal state of each tag (i.e., the H or L state of the ON-OFF Keying modulated signal) which indicates the transmitted data, but can't obtain the fine-grained channel parameters, thus only works in parallel data transmission, rather than parallel sensing.

Based on the above discussion, we find a fundamental problem left unresolved: can we estimate the channel of parallel backscattered signals? Answer to this problem has great significance in real applications, such as real-time tracking of multiple moving objects. As we will analyze in the subsequent sections, whether channel estimation can be parallelized not only determines the sensing efficiency, but also affects the accuracy of sensing results.

Consider that many interference resolution methods are able to separate the collided signal, one may wonder: why not estimate channels directly based on the separated signal? For most interference resolution approaches, e.g. the MIMO based methods $[2, 21, 29, 34, 49]$ , channel parameters are the prerequisites for decoding the parallel transmitted signals. Without channel information, they cannot perform parallel decoding, not to mention channel estimation based on parallel decoding. Moreover, backscatter devices close to each other often suffer serious inter-tag interference, as is called inter-tag interference. The collided signal isn't the linear addition of the original backscattered signals. Consequently, although there have been some methods that can decode collided signals without channel information $[7, 17, 26]$ , they still can't obtain the channel parameters.

Channel estimation of parallel backscatter is indeed a daunting task, with the following critical challenges: First, a backscattering tag keeps flipping their states between H and L. The rate of flips is essentially determined by the encoding bit rate of the tag. When there are multiple colliding tags in the channel, the collided signal is highly dynamic and transfers among different combined states at an even higher rate. It is extremely difficult to find steady signal samples that reflects the channel parameters. Second, the above-mentioned inter-tag interference will further distort the collided signals and introduce uncontrollable estimation errors.

In order to tackle the above problems, we in this paper propose Fireworks, the first approach for channel estimation of parallel backscattered signals. The key insight of Fireworks is that although the state of the collided signal keeps changing, the resulting moving trajectory of the signal on the IQ (In-phase and Quadrature) domain is determined by and in turn reflects the channel parameters of the tags and the interference among them. Specifically, this insight attributes to the following observations:

- The OOK modulation conveys data by changing the carrier's amplitude. Such linear changes result in straight transition paths in the IQ domain, whose geometric properties (namely, direction and length) reflect the phase and amplitude of that tag's signal.   
- Due to the intrinsical clock drift and asynchronous communication, changes of the tags' coding state occur asynchronously. The whole moving trajectory of the collided signals actually connects

the respective transition paths of the tags. The channel parameters are therefore preserved in the geometric property of the whole trajectory.

\- The inter-tag interference occurs only when at least two tags are simultaneously in the reflecting state. The transition paths are the linear combination of the channels of different tags and inter-tag interference. By utilizing information contained by both the interfered and un-interfered transition paths, the channel estimation process can obtain plenty of constraints to control the estimation errors and produce accurate results.

Based on the above insight, we propose an Inter-tag Interference Aware (IIA) model that captures the exact transformation from the channel parameters to the trajectory of collided signals. We invert the above transformation by solving a global optimization problem, which minimizes the overall distance between the signal samples and the trajectory generated by the IIA model. Our contributions can be summarized as follows:

- We disclose the principle of inter-tag interference under parallel backscatter and propose the IIA model that describes the exact relationship between channel parameters and the geometric properties of the signal trajectory.   
- We present Fireworks, which produces accurate channel estimation through a global optimization process. To the best of our knowledge, Fireworks is the first approach for channel estimation of parallel backscattered signals.   
- We implement Fireworks and evaluate its performance with extensive experiments. The results demonstrate that Fireworks accurately estimates channel parameters of up to five parallel tags, with the mean errors of 0.054 rad. in phase and 0.0029 in amplitude. When applied to the backscatter based tracking application, Fireworks achieves 2\~4× improvement in tracking accuracy, compared with the state-of-the-art approach [46].

Roadmap. Section 2 and Section 3 respectively present the motivation and challenges of our work. In Sections 4 and 5, we elaborate on the underlying insight and the design of Fireworks. After discussion on several issues in Section 6, we present the evaluation results in Section 7. Section 8 discusses the related work. Section 9 concludes this work.

# 2 WHY TO PARALLELIZE CHANNEL ESTIMATION?

From the perspective of backscatter based sensing applications, we discuss the motivation of our work. We take target tracking as an example. A common approach of the existing works is to estimate the target's location according to the tag's channel parameters (i.e., phase and amplitude). In order to have accurate and continuous tracking of the target's location, the interval between two consecutive estimation should be sufficiently short. In other words, a sufficiently high rate of channel estimation is desired.

Fig. 1(a) compares the calculated trajectories of the letter "M" under different channel estimation rates. Apparently, we can see large deviation from the ground truth, when the channel estimation rate is relatively low. Since the channel estimation depends on the successful reception of the tag's signal, so the channel estimation rates of the tags equal to their individual reading rate (IRR). We first check the IRR of the commercial backscatter system that adopts the FSA (Framed Slotted ALOHA) protocol for tag interrogation. Then we show how parallel channel estimation can improve the channel estimation rate.

![](images/7b20635e7a3fee38dc85c6fe855babb01248fbffc34412bc0f3bf82f277a47b4.jpg)  
(a) Tracking with different IRR

![](images/be6c7ca61715fa91a8ea5a96dc9fa5693384affea2b0098eb96f22a8115205d4.jpg)



(b) IRR under different tag population   
Figure 1: Impact of IRR on sensing applications.

In the FSA protocol, the reader divides time into K slots, and each tag randomly picks a slot to reply. Since the tags are not coordinated at this phase, some of them may collide in reply. We denote the reading capacity of the reader as M, which means the reader can read up to M colliding tags in one slot. Then, if we have N tags, the throughput (successful readouts per slot) of the system will be:

$$
T h (M, N) = \sum_ {R = 1} ^ {M} R \binom {N} {R} \left(\frac {1}{K}\right) ^ {R} \left(1 - \frac {1}{K}\right) ^ {N - R} \tag {1}
$$

So the number of slots required to collect N tags can be estimated by $S(M, N) = \lceil \frac{N}{Th(M, N)} \rceil$ . Now, if the mean duration of each slot is $\tau$ , the entire inventory cost can be calculated by $\tau_{0} + \tau \cdot S(M, N)$ , where $\tau_{0}$ denotes the start-up cost [22]. Then the IRR is given by:

$$
I R R (M, N) = \frac {1}{\tau_ {0} + \tau \cdot S (M , N)}. \tag {2}
$$

According to our measurement result, we have $\tau_{0} = 19ms$ and $\tau = 0.5ms$ . Assume that the reader can always select the optimal K under different reading capacity M based on Eq. (1), we can get the IRR under different tag populations, as shown in Fig. 1(b).

Figure 1(b) shows that in FSA protocol (M = 1), IRR significantly drops with the increased number of tags. Such inherent conflict between the capacity of sensing and IRR precludes the feasibility of many sensing applications [22, 31, 47]. For example, in automated factories, a 30Hz IRR is required to monitor the fast moving and rotating items on the production line [12, 13]. According to Fig. 1(b), however, such an IRR is achieved only when the number of targets is lower than 10. That is unlikely on the production line, where dozens of items are processed in the communication range of the reader. Similarly, in Tagbeat [47], a 40Hz IRR is required to estimate the frequency of a 100Hz vibration source. That actually means Tagbeat works only when there are 1\~2 vibration sources, as indicated by Fig. 1(b). But the number of vibrating sources is often much more than that in real-world scenarios. Note that Fig. 1(b) shows the ideal case where the reader can always select the optimal slot number K. The IRR will be even lower in practice, as shown in many existing studies [22].

The above dilemma can be mitigated if parallel channel estimation is enabled. Fig. 1(b) tells that increasing the reading capacity M significantly increases the IRR and thus the channel estimation rate. Although the reading capacity M cannot increase infinitely due to the limited channel bandwidth, improving the channel estimation rate still has great significance for RFID based sensing applications. For a system with M = 5, when 70 tags coexist in one environment, the channel estimation rate can be kept as high as 30Hz. This means that we can track the movement of more than 70 targets concurrently. Similarly, we can keep a 40Hz channel estimation rate when the number of tags reaches 30, which means that we can sense the vibration frequency of 30 vibration sources concurrently. Such a capacity is sufficient and attractive for many real applications. Motivated by the need of high capacity of sensing, we continue to study the feasibility and the solution for parallel channel estimation.

![](images/821bc5b4abe05227e131e875fc2f80c126c3ae97eb79d0aa0a997d8efbd28e48.jpg)  
Figure 2: Visualization of tag's signal in IQ domain.

# 3 PRELIMINARIES

In this section, we first briefly introduce parallel backscatter. Then we discuss the challenges in estimating the channel parameters from parallel backscattered signals.

# 3.1 Parallel backscatter

The wireless channel describe how a signal changes as it propagates from transmitter to receiver. The transmitted signal is denoted by $S_{0}$ . The received signal S is given by:

$$
S = h \cdot S _ {0} \tag {3}
$$

where $h = \alpha e^{\mathrm{j}\delta}$ denotes the channel, and $\alpha$ and $\delta$ denote the channel parameters amplitude and phase, respectively.

Observed in the IQ domain, the theoretical representation of the signal is a single point (as shown in Fig. 2(a)), whose location is determined by the channel parameters. Specifically, the length and direction of the signal vector $\vec{S}$ correspond to $\alpha$ and $\delta$ of the signal, respectively.

When only one tag is transmitting, there are two channels: i) the channel between the reader and the tag, where the reader A transmits a carrier wave $S_{0}$ and the tag T responds its data $s(t)$ by reflecting the carrier wave using OOK modulation; ii) the channel between the reader and the background reflectors. Here we abstract the background reflections as from a virtual point B, according to the linear addition principle of signals. The received signal at the reader can be expressed by:

$$
S (t) = s (t) \cdot h _ {T} \cdot S _ {0} (t) + h _ {B} \cdot S _ {0} (t) \tag {4}
$$

where $s(t) = 0$ or 1 depends on the encoded bits. $h_T$ and $h_B$ respectively denote the channels along the round-trips $A \to T \to A$ and $A \to B \to A$ .

The representation of the received signal in the IQ domain is determined by the channels of both sources of reflections:

$$
\overrightarrow {S} (t) = \overrightarrow {S} _ {B} + s (t) \cdot \overrightarrow {S} _ {T} \tag {5}
$$

Eq. (5) tells that due to the OOK modulation, the signal is theoretically present at two points (Fig. 2(b)), respectively corresponding to the silence (L) and the reflecting states of the tag (H). By subtracting the L-state from the H-state signal, we can remove the background reflection and derive the vector that denotes the channel of the tag.

When N tags transmit simultaneously, the IQ domain representation of the signal is determined by the channels of all the tags:

$$
\overrightarrow {S} (t) = \overrightarrow {S} _ {B} + \sum_ {i = 1} ^ {N} s _ {i} (t) \cdot \overrightarrow {S} _ {T _ {i}} \tag {6}
$$

where $s_{i}(t)$ denotes the state of Tag $T_{i}$ . In this case, the collided signal theoretically form $2^{N}$ points, each representing a combined state of the N tags. Fig. 2(c) shows an example with two tags. The $2^{2} = 4$ points represent the four combined states of the tags, namely LL, HL, LH, and HH.

In collision cases, a pair of points whose corresponding states differ from each other in only one tag's state (e.g., LL and HL) is called neighboring points. That tag's channel is characterized by the vector connecting the two neighboring points. In the N-tag collision case, each tag will have N equivalent vectors, as shown by the example with 2\~4 tags in Fig. 2(d).

The existing parallel decoding approaches $[17, 26]$ are able to identify the combined state of each point, so that the data sequence of each tag (i.e., $s_{i}(t)$ ) is obtained. Based on the identified points, one can find the N pairs of neighbour points for each tag. Provided that the relative locations of all the paired points are known, the channel parameters of the tags can be accordingly estimated.

# 3.2 Challenges in parallel channel estimation

Discussion in the previous subsection presents an ideal case of channel estimation of parallel backscatter. The real-world signals induce a series of critical challenges, as detailed in this subsection.

We start from a simple case with one tag, as shown in Fig. 3(a). Due to the noise, the signal samples belonging to the same state form a cluster rather than a single point. Meanwhile, due to the hardware constraint on the tag, a tag's state transition lasts for a short period rather than completes instantaneously, leaving transitional samples along the transition paths. The noises and the transitional samples obscure the locations of the signal states. Fortunately, due to the Gaussian distribution of the noise and the relatively long dwell time on each state, we can still pinpoint the locations of the states by finding the density peaks of the samples, as shown in Fig. 3(a).

Things totally change when it comes to the multi-tag collision case. The distribution of the signal samples will become dispersed and largely deviated from the theoretical locations, due to the fast-varying property of the collided signal and the inter-tag interference among the tags.

![](images/b946b9de82343730f7fc2ab98a86d0c09c4797dec43af9c7e59d8f14a4cbf034.jpg)



(a) One tag

![](images/cbc03f7e401945d0b428ccfd25573e39828f2b9df7bc78ed6bed985b372a2ba1.jpg)



(b) Three tags

![](images/e76f982b0de0711dcdd922f8b5e1f07f3a938e70a7d68d217d8a8a02c874fb32.jpg)



(c) Three tags with inter-tag interference

Figure 3: Practical IQ domain representation of tags' signal.   
![](images/3181fd58cca09c24df1ea5d23d44e230610069f2765d56cd4805d4120a59de80.jpg)



Figure 4: $T_{t}$ and $T_{d}$ under different $N$ .

3.2.1 Fast variation of signal. Fig. 3(b) shows an example of three tags. Since all the tags keep flipping their states, the collided signal frequently transfers among different combined states, as shown by the state sequence in Fig. 3(b)-top. This leads to a fast-moving signal in the IQ domain. To visually illustrate such mobility, we extract a $2\mu s$ segment from the sequence and plot its IQ domain trajectory in Fig. 3(b)-bottom. We can see that even in such a short period, the signal trajectory can go through the entire area of signal samples. Therefore, the signal samples aren't concentrated explicitly on any cluster area, making it difficult to pinpoint the location of any signal state.

For better understanding of the above phenomenon, we theoretically analyse the signal's expected dwell time in the cluster areas and along the transition paths. Suppose there are $N$ tags and the frequency of state flip for every tag is $B\mathrm{Hz}$ . If the duration of one flip is $\tau_{f}$ ( $\tau_{f} \approx 0.2\mu s$ ), then in one second, the time spent on state transition is $T_{t} = N \cdot B \cdot \tau_{f}$ , while the time for the signal to dwell on clusters is $T_{d} = 1 - N \cdot B \cdot \tau_{f}$ . Fig. 4 compares $T_{t}$ and $T_{d}$ under different number of tags ( $N$ ) and different tag bitrates (we assume the tags use FM0 code, so the bitrare will be $B/2$ ). With more and more tags transmitting simultaneously, the dwell time on clusters becomes shorter and shorter. This phenomenon becomes more apparent under a higher bitrate. In the extreme case where 4\~5 tags transmit at 640Kbps, the signal keeps transferring among different states and seldom stays on any state. The density-based channel estimation (mentioned in the previous subsection) doesn't work in the case of parallel backscattered signals.

3.2.2 Inter-tag interference. Recall that the tag transmit signal by reflecting the signal it receives. When two nearby tags transmit simultaneously, one tag will reflect not only the carrier wave from the reader, but also the signal from the other tag. Such an additional source of reflection leads to non-linear addition of the signal from the two tags, which further alters the locations of the signal samples.

Fig. 3(c) shows the collided signal of three tags with $10\mathrm{cm}$ spacing to each other. In the figure, we plot the signal vectors that correspond to one tag. The figure shows that due to the inter-tag interference, the signal vectors of the same tag aren't consistent with each other in either length (amplitude) or direction (phase). We cannot figure out the exact channel parameters of this tag based on such distorted signal vectors.

Note that although the inter-tag interference occurs only between nearby tags (with a distance lower than 15cm in our experiment), it is still necessary to mitigate the inter-tag interference. In many RFID based sensing applications, the tags are located close together. For example, in some tracking systems, such as pipeline monitoring [12, 13] and luggage tracking [46], the targets are closely located. Moreover, in some orientation tracking applications [44], we need to deploy a tag array on a target to infer its orientation. In the above cases, the distance among the tags is usually lower than 10cm. Some novel HCI applications also require to deploy a set of tags on one target. For example, the RFID glove [45] attaches a tag on every finger to achieve fine-grained gesture recognition. Another example is the RFID based touch sensing and surface shape sensing applications, where an array of RFID tags is deployed to emulate a virtual keyboard [27] or a surface sensor [15, 23]. In these cases, the distance between tags is usually lower than 1cm. In general, the above examples show that mitigating the inter-tag interference is essential to many RFID based sensing applications.

# 4 INSIGHT OF FIREWORKS

Fireworks's primary objective is to accurately extract channels of each tag from the fast moving and largely distorted collision signal. To achieve this objective, Fireworks is based on the observation that although the IQ domain location of the collided signal keeps changing, the way how the signal moves is deterministic. The geometric properties of the moving trajectory of the signal is indeed determined by both the channels of the tags and the interference among the tags. So, instead of relying on the exact location of the signal states (which is difficult to obtain in practice), we can extract the channels directly from signal moving trajectory.

In this section, we first reveal the relationship between the signal trajectory and the channel parameters, and then present the understanding on how the inter-tag interference affects such relationship.

![](images/27faff2397952190566548b922429add22db375f70a85b76237142982a121a3f.jpg)



(a) One tag

![](images/ea4ebf735b3535c319ae7a260ac6cef451c1f39ae040704c3a31ab928aaf13af.jpg)



(b) Two tags   
Figure 5: Theoretical trajectory of tags' signal.

# 4.1 Signal trajectory

We start with the trajectory of one tag's signal. Recall that the signal of a tag has two states, and the tag flips its state by changing the amount of energy it reflects. So if we denote the fraction of energy that the tag reflects by $\gamma(t)$ (termed by reflecting scale), the flip of the tag's state can be viewed as the variation of $\gamma(t)$ between 0 and 1, where $\gamma(t) = 0$ or 1 indicates the $L$ or $H$ state of the signal. We can see that during the flipping process, the tag only changes the signal's amplitude while the phase is fixed, as shown in Fig. 5(a). No matter whether the amplitude changes uniformly or not, the transition path of the signal will always be a straight path, whose geometric properties (i.e., length and the direction) exactly capture the amplitude and phase of the signal.

Considering the goal of parallelizing the channel estimation, one may wonder: are the above properties of signal trajectory preserved under collisions? The answer is yes. Specifically, in the collision cases, although all the tags keep flipping their states, the flips of different tags usually interleave with each other. This is caused by the intrinsic asynchronism of the tags, e.g., different response delay and different clock drifts across tags $[10, 17, 26]$ . As a result, the whole trajectory of the collided signal is a simple connection of the transition paths of individual tags. The geometric properties of each path still reflect the channels of the corresponding flipping tag.

As an example, Fig. 5(b) illustrates the trajectory of the signal from two tags. In the figure, the four red points denote the locations of the combined states, and the four solid lines denote the transition paths of the signal. In this case, the signal trajectory can be approximated to a parallelogram, where the two pairs of parallel edges represent the channels of the two tags. The irregular trajectories (denoted by the dash lines) are caused by occasional alignment of the flips of two tags. Different aligning pattern (e.g., different starting time or different transition speed of the two tags) will lead to different shapes of the paths between two certain states.

In summary, we have the follow observation:

Observation 1. When multiple tags transmit in parallel, the trajectory of the signal is represented as a transition graph, defined by TG = (S, V), which is an end-to-end connection of the transition paths of individual tags. Here, S is the collection of the $2^{N}$ combined states. V is the collection of the transition paths. The length and direction of each path respectively capture the phase and amplitude of the corresponding tag.

![](images/75dad1e094092fa431f0fb6b48dfb851bf7e3c1f14b22e1588cf42238d0e323e.jpg)



Figure 6: Signal propagation with inter-tag interference.

# 4.2 Understanding the inter-tag interference

The previous subsection discloses the relationship between the signal trajectory and the channels of the tags. This subsection follows to examine how the inter-tag interference affects the relationship. We first consider a simple case with two tags, as shown by Fig. 6. In this case, besides the basic signals mentioned in Sec. 3.1, there are two additional sources of signals: the signals transiting along the paths $A \to T_1 \to T_2 \to A$ and the paths $A \to T_2 \to T_1 \to A$ .

We find that both the two interfering signals experience twice reflections, i.e., by $T_{1}$ and $T_{2}$ . This reveals an interesting fact: the inter-tag interference between two tags occurs only when both the two tags are in their reflecting state (namely the H state). To understand the impact of inter-tag interference on the signal trajectory, we can treat the interfered signal as if it is transmitted from a virtual signal source, which also flips between two states: silence and reflecting. Specifically, it reflects the signal only when both the corresponding two tags are in the reflecting states. Then, according to the principle of signal propagation and reflecting [35], the fraction of energy this virtual source reflects (denoted as $\gamma_{INT}(t)$ ) is given by the reflecting scale of the corresponding two tags: $\gamma_{INT}(t) = \gamma_{T_{1}}(t) \cdot \gamma_{T_{1}}(t)$ . Then, the trajectory of the collided signal can be viewed as a linear combination of the channels of the three reflection sources and their reflecting factors:

$$
\overrightarrow {S} (t) = \overrightarrow {S _ {B}} + \gamma_ {T _ {1}} (t) \overrightarrow {S _ {T _ {1}}} + \gamma_ {T _ {2}} (t) \overrightarrow {S _ {T _ {2}}} + \gamma_ {T _ {1}} (t) \gamma_ {T _ {2}} (t) \overrightarrow {S _ {I N T}} \tag {7}
$$

where different transition paths can be viewed as different combinations of the channels of the tags and the inter-tag interferences, as shown in Fig. 7(a). Eq. (7) indicates that: i) the deviation of state $HH$ (where $\gamma_{T_1}(t) = \gamma_{T_2}(t) = 1$ ) from its original position actually represents the signal vector of the inter-tag interference $\overrightarrow{S_{INT}}$ ; ii) the two trajectories $LL \to HL$ and $LL \to LH$ ( $\gamma_{INT} = \gamma_{T_1}(t) \cdot \gamma_{T_2}(t) = 0$ ) are free from the inter-tag interference.

Then let's consider the $N$ -tag collision case. In this case, the trajectory of the collided signal is determined by the channels of both the $N$ tags and the interferences among every $2 \sim N$ tags. The number of interfering paths can be estimated as $N_{int} = \sum_{i=2}^{N} \binom{N}{i}$ . Due to the serious signal attenuation, the amplitude of the signal reflected for more than twice (e.g., the signal traveling from $A \to T_1 \to T_2 \to T_N \to A$ in Fig. 6) will decay to nearly zero. This is demonstrated in our experiment result later. As a result, we can approximate the number of interferences as $M \approx \binom{N}{2}$ , then the trajectory of the collided signal can be modeled as:

![](images/dfb597fc9a9a424f2d1a313ab796c9bdcb9c939536ae03e530bb92579606f70c.jpg)



![](images/564a8d7cc186a68c99427c1cf6d2566ec5e95c5f196fd947eb292a749907c981.jpg)



Figure 7: The theoretical trajectory of the interfered signal: (a) Two tags; (b) Three tags.

$$
\overrightarrow {S} (t) = \overrightarrow {S _ {B}} + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} (t) \overrightarrow {S _ {T _ {i}}} + \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} \gamma_ {T _ {i}} (t) \gamma_ {T _ {j}} (t) \overrightarrow {S _ {I N T} ^ {(i , j)}} (8)
$$

where $S_{INT}^{(i,j)}$ ( $i \neq j$ ) denotes the inter-tag interference between each two tags $T_i$ and $T_j$ . A three-tag example is shown in Fig. 7(b). According to Eq. (8), we have the following observation:

Observation 2. When N mutually-interfering tags transmit in parallel, the collided signal forms a distorted transition graph, termed as DTG. In the DTG, different transition paths can be viewed as different combinations of the channels of the tags and the interferences.

We conduct an experiment to practically observe how the inter-tag interference affects the geometric properties of the signal trajectory. Specifically, we let three tags transmit packets periodically with their own schedule. Then the collisions randomly occur due to the different transmission schedules of the tags. Fig. 8 shows the signals received in both the single-tag cases and collision cases.

Signals in the single-tag transmission cases (shown in Fig. 8(a)-(c)) show the signal trajectories of the three tags. The $\overrightarrow{LH}$ vectors in these three figures show the signal vectors of the three tags (i.e., $\overrightarrow{S_{T_1}}$ , $\overrightarrow{S_{T_2}}$ , and $\overrightarrow{S_{T_3}}$ ). In the two-tag collision cases shown in Fig. 8(d)-(f), the deviations of the HH clusters indicate the channels of the inter-tag interferences between each pair of the tags, denoted by $\overrightarrow{S_{INT}^{(1,2)}}$ , $\overrightarrow{S_{INT}^{(1,3)}}$ , and $\overrightarrow{S_{INT}^{(2,3)}}$ . Fig. 8(g) shows the signal trajectory of the three-tag collision case. We can see that the geometry of the signal trajectory is exactly the combinations of the channel of every tag (i.e., $\overrightarrow{S_{T_1}}$ , $\overrightarrow{S_{T_2}}$ , and $\overrightarrow{S_{T_3}}$ ) and the interference between every pair of tags (i.e., $\overrightarrow{S_{INT}^{(1,2)}}$ , $\overrightarrow{S_{INT}^{(1,3)}}$ , and $\overrightarrow{S_{INT}^{(2,3)}}$ ). This also proves that the signal reflected for more than twice can be ignored. For example, the location of the state HHH (where $\gamma_{T_1} = \gamma_{T_2} = \gamma_{T_3} = 1$ ) is exactly a linear addition of all the tags' channels and all the inter-tag interferences.

In summary, we have obtained a transform between the channels of the tags and the geometric properties of the signal trajectory. Based on this knowledge, we can make accurate estimation of the channels directly from the collision.

# 5 THE DESIGN OF FIREWORKS

This section elaborates on the design of Fireworks.

A naive solution is to extract the un-interfered paths by extracting only the un-interfered signal samples. Then the length and

![](images/818cdc6e3045ef5b6ff6dacfa56ca5ebfcec9c694cb02f0587b4565df510f920.jpg)



Figure 8: The practical trajectory of the signal from one tag ((a)-(c)), two tags ((d)-(f)), and three tags ((g)).

direction of the un-interfered paths characterize the tags' channels. However, the number of the un-interfered samples decreases exponentially with the number of tags. For each tag, only $\frac{1}{2^{N-1}\cdot N}$ of the signal samples can be used to extract its channel. Consider that the backscatter signal usually exhibits low SNR, using such small fraction of samples will lead to excessively high estimation error.

Based on the insight presented in the previous section, our idea is to translate the channel estimation problem to a global optimization process: we can obtain the optimal channel estimation by finding the DTG that best fits the observed signal samples. As we have discussed in Sec. 4.2, geometric properties of different transition paths are determined by a linear combination of the channels of different tags and the inter-tag interferences. By utilizing information contained in all the transition paths, the optimization process can obtain plenty of constraints to control the estimation errors and produce accurate results.

In the following of this section, we first mathematically formalize the Inter-tag Interference Aware (IIA) model, which transforms the channel parameters to the property of the signal trajectory. Then we introduce the global optimization process to perform the estimation.

# 5.1 The IIA Model

Suppose we have N tags $T = \{T_{1}, ..., T_{N}\}$ , for each tag $T_{i}$ , its channel parameters can be represented by a 2-tuple $P_{T_{i}} = (\alpha_{T_{i}}, \delta_{T_{i}})$ . The channel of the interference between each pair of tags $T_{i}$ and $T_{j}$ is represented by $P_{INT}^{(i,j)} = (\alpha_{INT}^{(i,j)}, \delta_{INT}^{(i,j)})$ . The signal trajectory is represented by a set of points whose locations are denoted by $(I, Q)$ . We now present the mathematical formulations of the transform between a set of 2-tuples $P = \{P_{T}, P_{INT}\}$ and the IQ domain trajectory of the samples.

![](images/6d4e5312aca9b5689e81e063f471c37ff7b6f871be6a00983e0b6077062496e3.jpg)



Figure 9: Fitting the DTG to the samples.

![](images/835e762e96aad131163ee7a4c8ea824ec83f3f61d0e4039954a94ef1524ec232.jpg)



(a)

![](images/80ceba8741e28fb8a767dcb406159acf0cb05d6d9b311c35e021697658143013.jpg)



(b)

![](images/ece09101f833df66f0a8614888bf71e0509b8f6a5f303519416cbcfa4f96c669.jpg)



(c)   
Figure 10: Coarse-to-fine searching: (a) Ranges of the channel parameters; (b) $R(\mathrm{S}_{\mathrm{est}}, \mathrm{S}_{\mathrm{obs}})$ under different phase and amplitude of $T_{1}$ ; (c) $R(\mathrm{S}_{\mathrm{est}}, \mathrm{S}_{\mathrm{obs}})$ under different phase and amplitude of the interference between $T_{1}$ and $T_{2}$ .

In the single tag case, the signal's trajectory is given by:

$$
I (\gamma_ {T}) = \alpha_ {B} \cdot c o s (\delta_ {B}) + \gamma_ {T} \cdot \alpha_ {T} \cdot c o s (\delta_ {T})
$$

$$
Q \left(\gamma_ {T}\right) = \alpha_ {B} \cdot \sin \left(\delta_ {B}\right) + \gamma_ {T} \cdot \alpha_ {T} \cdot \sin \left(\delta_ {T}\right) \tag {9}
$$

the channel of the background reflection $(\alpha_{B}, \delta_{B})$ is simplified as constant value.

When $N$ tags transmit in parallel, the signal trajectory is commonly determined by the channels of all the tags:

$$
I (\gamma) = \alpha_ {B} \cdot \cos \left(\delta_ {B}\right) + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} \cdot \alpha_ {T _ {i}} \cdot \cos \left(\delta_ {T _ {i}}\right) \tag {10}
$$

$$
Q (\gamma) = \alpha_ {B} \cdot s i n (\delta_ {B}) + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} \cdot \alpha_ {T _ {i}} \cdot s i n (\delta_ {T _ {i}})
$$

where the set $\gamma=\{\gamma_{T_{1}},\ldots,\gamma_{T_{N}}\}$ denotes the reflecting scale of the tags. Recall that the signal's transition is usually caused by the flip of only one tag. So we should set a constraint on the reflecting scales of the tags as: at any time, there exist at most one tag $T_{i}$ , whose reflecting scale satisfies $\gamma_{T_{i}}\in(0,1)$ .

When the inter-tag interferences are taken into account, the signal trajectory can be expressed by:

$$
I (\gamma) = \alpha_ {B} \cdot c o s (\delta_ {B}) + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} \cdot \alpha_ {T _ {i}} \cdot c o s (\delta_ {T _ {i}}) +
$$

$$
\sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} \gamma_ {T _ {i}} \gamma_ {T _ {j}} \cdot \alpha_ {I N T} ^ {(i, j)} \cdot c o s (\delta_ {I N T} ^ {(i, j)})
$$

$$
Q (\gamma) = \alpha_ {B} \cdot s i n (\delta_ {B}) + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} \cdot \alpha_ {T _ {i}} \cdot s i n (\delta_ {T _ {i}}) +
$$

$$
\sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} \gamma_ {T _ {i}} \gamma_ {T _ {j}} \cdot \alpha_ {I N T} ^ {(i, j)} \cdot s i n (\delta_ {I N T} ^ {(i, j)})
$$

Eq. (11) is a mathematical representation of DTG, which defines the IIA model that transforms the channel parameters of the tags and the interferences to the property of the signal's trajectory.

# 5.2 Graph fitting

In this section, we describe how we solve the optimization problem that inversely transforms the property of the signal trajectory to channel parameters. Specifically, let $S_{\mathrm{obs}}$ denote the IQ domain samples, where $\mathrm{S}_{\mathrm{obs}}(i)=(I(i),Q(i))$ is the location of sample i. $\mathrm{S}_{\mathrm{est}}(\mathbf{P})$ denotes the constructed DTG based on the IIA model (Eq. (11)). Fig. 9 gives an example of $S_{obs}$ and $S_{est}$ in a three-tag collision case. To obtain the optimal channel estimations, we need to compute:

$$
\mathbf {P} ^ {*} = \arg \min _ {\mathbf {P}} \sum R (\mathrm{S} _ {\text { est }} (\mathbf {P}), \mathrm{S} _ {\text { obs }}). \tag {12}
$$

where $R(\bullet)$ captures the overall distance between the generated DTG and the observed samples, which quantifies the goodness-of-fitting of $S_{est}$ under a given set of channel parameters P. Clearly, $R(\bullet)$ will be minimized when we get the optimal channel estimation.

However, we may meet two problems: i) $S_{\mathrm{est}}(\bullet)$ is a multivalued piecewise function. In order to accurately quantify the overall distance between $S_{obs}$ and $S_{est}$ , we should first match each sample to the correct path, as shown in Fig. 9. ii) the optimization problem is non-convex. In order to avoid the local-optimal problem, we should have a good initialization for the searching process. In the following, we introduce our searching method which is designed to solve these problems.

5.2.1 Mapping a sample to the correct path. We solve this problem by utilizing the result of parallel decoding $[10, 17, 26]$ . Recall that the parallel decoding method can obtain the state sequence (i.e., $s(t)$ in Eq. 4) of each tag from the parallel transmitted signals. Thus we can get the flip sequence of each tag (i.e., the time points when each tag flips its state) and finally get the transition sequence of the collided signal (i.e., a sequence of time points that denotes the start and end of each state transition). As a result, the samples that belong to different transition paths are separated.

5.2.2 Coarse-to-fine searching. Now, we focus on how to search for the optimal estimation of the channels. To avoid the local-optimal problem, we design a coarse-to-fine searching method that first performs a coarse estimation of the channels, which provides an appropriate initial point for the searching. Then we approach the optimal estimation by using the gradient-descent algorithm. Here we use the three-tag collision case in Fig. 10 as a example to introduce the searching method.

Coarse-grained estimation. The tags' channels can be initialized based on the $N$ interference-free trajectories using segmented regression. Consider that the noise level (i.e., the radius of the signal cluster) is limited, the error range of this coarse-grained estimation is limited, as marked in the subfigure of Fig. 10(a). Fig. 10(b) shows $R(\mathrm{S}_{\mathrm{est}}, \mathrm{S}_{\mathrm{obs}})$ under different channel parameters of $T_{1}$ , given certain channels of $T_{2}, T_{3}$ , and the inter-tag interferences. As shown in the figure, the coarse-grained channel estimation of $T_{1}$ locates in the neighbourhood of the global minima.

The channels of the interference between each pair of tags can be initialized based on the signal trajectory that contains the signal of only these two tags (e.g., the quadrilaterals that include the all-L state, as marked in Fig. 10 (a)). We take the estimation of $\overrightarrow{S_{INT}^{(1,2)}}(t)$ as an example. Given the coarse-grained estimation of the channels of $T_{1}$ and $T_{2}$ , we can recover the theoretical trajectory of these two tags, which presents as a parallelogram, as shown by Fig. 10(a). The deviation of state HHL (which is obtained by comparing the theoretical and practical trajectories) gives a coarse-grained estimation of $\overrightarrow{S_{INT}^{(1,2)}}(t)$ . Fig. 10 (c) shows the residual value under different channel parameters of $T_{1}$ .

![](images/717af0bbb64f403cae8dda85743bd6169d9270af4fa43482a20585e547445562.jpg)



Figure 11: Channel estimation error v.s. tag number.

![](images/39f09499e3cf6942b0ff8e739b1398dada0a0db7296402312bda16a28adfb272.jpg)



Figure 12: Explanation of the error diversity.

Note that the channels of the tags and interferences only determine the geometric property of the signal. To best fit the DTG to the signal samples, we should also estimate the channel parameters of the background reflection, which determine the displacement of the signal from the $(0,0)$ position. That can be easily estimated by using the signals sampled when there is not any tag transmitting.

Fine-grained estimation. In this process, we first generate the DTG based on the coarse-grained estimation of the channels, and then repeatedly adjust the channel estimation according to the residual value, until the power of the residual converges.

# 6 DISCUSSION

Computation overhead and latency. The computation overhead of Fireworks mainly lies the gradient-descent searching algorithm. Suppose the number of the signal samples is $n_{s}$ , the number of tags is N and the number of searching iterations is I, the computation complexity for the searching process can be estimated as $O(2(N + \binom{N}{2}) \cdot n_{s} \cdot I)$ . In the design of Fireworks, we have $n_{s} \leq 1000$ . Our experimental results in Sec. 7 show that the maximum capacity of Fireworks is N = 5, under which the required number of iterations I is usually not more than 6.

We can further decrease the computation overhead using the Mini-Batch Gradient Descent. By using this method, the complexity can be decreased to $O(2(N + \binom{N}{2}) \cdot b \cdot I)$ , where b is the batch size and typically we have $b \ll n_{s}$ . When implemented on an USRP N210 connected to a PC with a 3.6GHz CPU and a 16G memory, Fireworks takes $640 \sim 850\mu s$ to resolve the channels of the tags when N = 5. So, Fireworks can be used for online processing.

Coverage. The coverage of Fireworks is mainly determined by the platform it uses. The current implementation of Fireworks uses WISP tags. So, the coverage of Fireworks is limited to the communication range of WISP (i.e., 1.5m\~2m). We expect that when implemented on platforms with higher communication range (such as COTS RFID tags or other long-range sensing systems [25]), Fireworks will have higher coverage.

Generalization of Fireworks. Consider that the fundamental insight underlying Fireworks stems from special characteristics of the OOK modulated signal, so Fireworks theoretically generalizes to any tag platforms that uses OOK modulation. Fireworks has different performance gains when implemented on different platforms, depending on the protocol the platform uses. For the protocols that allow the collision among tags (e.g., the laissez-faire approach introduced in $[10]$ ), a 5-tag capacity can improve the individual channel estimation rate by 5 times. Note that in our implementation, such performance gain is achieved on WISP rather than the COTS RFID tags, because the latter usually adopts a collision avoiding protocol.

Why parallelization is preferred. Consider that the tags do not use their bandwidth efficiently, one may wonder why not just use a denser modulation (e.g., QAM) or a higher bitrate to get a higher channel estimation rate. It seems a simple solution, but the fact is that using denser modulation or higher bitrate would increase the complexity and the energy consumption of the tags. This goes against the original design intent of the RFID system. This is why Fireworks chooses to parallelize the transmissions of the tags.

# 7 EVALUATION

# 7.1 Experiment settings

Hardware: The reader side of Fireworks is built based on the USRP N210 software radio with UBX RF daughterboards and 900 MHz antennas. By default, the ADC sampling rate of the reader is set at 20MHz. Since the collision pattern of the COTS RFID tags is hard to control, the tag side of Fireworks is built on programmable WISP tags in our experiment.

Methodology: In the experiment, the reader transmits a carrier wave and the tags response simultaneously by reflecting back this signal. After receiving the collided signal, the reader extracts channels of the tag(s) using Fireworks. We conduct two groups of experiments to evaluate Fireworks's performance in two aspects: i) whether Fireworks can accurately extract the channels of the colliding tags; and ii) how Fireworks improves the performance of the backscatter based sensing applications.

![](images/f81d4f91d1a4865d4697a51999a27a23649fbe024f98436ce580ff4d952bcf36.jpg)



Figure 13: Channel estimation error v.s. SNR.

# 7.2 Channel estimation accuracy

In this experiment, we evaluate the accuracy of channel estimation under different influencing factors. Specifically, we adjust the number of tags, the tag-reader distance D (which leads to different signal SNR), the tag spacing d, and the bitrate of the tags to evaluate how these factors affect the performance of Fireworks. By default, we have $D = 50cm$ (the corresponding signal SNR is about 15dB) and $d = 10cm$ .

We treat the channel obtained in the non-collision TDMA scenario as the real value. Specifically, for each setting, we conduct experiments under both collision scenario and TDMA scenario. The estimation error is calculated as the difference between the values obtained under these two scenarios.

We compare Fireworks with a baseline method which first uses FlipTracer $[17]$ , a state-of-the-art parallel decoding method, to identify the combined state of each signal cluster on the IQ domain, then extracts the channel of each tag based on the centers (i.e., the density peaks) of the clusters (we term this baseline method as FlipTracer in the following of this paper.)

Performance under different number of tags. In this experiment, we let 2\~5 tags transmit simultaneously, the estimation error under different number of tags are shown in Fig. 11(a) and (b). We have the following findings:

\- With the increased number of tags, the mean error of both the two methods increase due to the aggravated interference among tags. For example, the phase error of FlipTracer increases from 0.3\~0.7 rad to 0.6\~1.4 rad when the number of tags increases from 2 to 5. Compared with FlipTracer, Fireworks does not suffer obvious performance degradation. Specifically, in the 5-tag case, the mean error of phase estimation is 0.135 rad, which is almost one magnitude lower than that of FlipTracer. Its mean error of phase and amplitude estimation across all the parallelism levels are 0.054 rad. and 0.0029, respectively. Such a high accuracy is achieved due to Fireworks's ability to compensate the inter-tag interference.

\- For FlipTracer, the tag number not only increases the mean error of channel estimation, but also the error variation. This is due to the increased moving frequency of the collided signal when more tags transmit simultaneously. While, Fireworks is almost

![](images/57db771c41550d3756ad6af2440d78936c523d32294ff4e91aeb2fa15725d7d1.jpg)



(a) Phase error of FlipTracer

![](images/0596889f47b2269a88bb29fc8d773d4f8287c49e0bcbb8e431585806b313650d.jpg)



(b) Phase error of Fireworks

![](images/3ef9f6027ac1d147996c9a254d2b9e9b1b9fa7793a8520a0ecc260d6a897de79.jpg)



(c) Amplitude error of FlipTracer

![](images/8e800577ca7636e7eaab30dc062fc03bb540be30f1ddad83228c71c4827a2472.jpg)



(d) Amplitude error of Fireworks   
Figure 14: Channel estimation error under different tag numbers and SNRs.

not affected by the increased number of tags since it extract the channels directly based on the moving trajectory of the signal.

\- There is also a interesting observation that different tags suffer quit different levels of channel estimation error. In addition, even for the same tag, it suffers different levels of errors in phase and amplitude estimation. For example, in the five-tag case, Tag $T_{3}$ exhibit a relative low phase error while a high amplitude error. Indeed, this is caused by the diversity in the phase difference between the tags' signal and the interference signal, as shown by Fig. 12. Specifically, when the phase difference approaches to zero (e.g., $S_{T_1}$ and $S_{INT}$ in Fig. 12), the interference have the maximal impact on the amplitude of the tag signal while have the minimal impact on the phase value. When the phase difference approaches to $\pi / 2$ (e.g., $S_{T_2}$ and $S_{INT}$ ), the situation is reversed.

Performance under different signal SNR. In this experiment, we use three tags. The tag-reader distance changes from 30cm to 100cm, and the corresponding signal SNR decreases from 15dB to 5dB. The performance under different SNRs are shown in Fig. 13. This two figures tell that:

- A surprising observation is that the mean error of FlipTracer slightly decreases with the decreased SNR. For example the phase error range of FlipTracer increase from 0.3\~0.6 rad to 0.3\~1.2 rad when the SNR increases from 5dB to 20dB. This is indeed due to the aggravated inter-tag interference when the signal power is high. In contract, Fireworks is not so sensitive to the SNR due to its ability to compensate the inter-tag interference.   
- For both the two methods, the error variance of the phase estimation increase with the decreased signal SNR. This is because that the low SNR will amplify the phase error.

As a summarize, Fig. 14 shows the performance of Fireworks and FlipTracer under different tag numbers and SNRs. Clearly, for both methods, their performance is more sensitive to the tag number. Fireworks consistently outperforms FlipTracer at all the cases.

Performance under different inter-tag distances. The inter-tag distance d is an important factor which determines the intensity of inter-tag interference. In this experiment, we use 3 tags and change d from 3cm to 15cm. The experiment result is shown in Fig. 15. As expected, the performance of FlipTracer degrades significantly with the decreased d. Fireworks consistently outperforms

![](images/62888296cbc691b0e07695449d9ce72b81e2cee0b220b2195456bf615fb7d8a5.jpg)



Figure 15: Impact of $d$ .

![](images/cc309c4b3a8431aeb273b3d87c99580693352d7085b80c9b0a4a865d3071cb67.jpg)



Figure 16: Impact of Bitrate.

![](images/479e58b238e06f3508ef2bd970036bdc6f60b48ea0b2345abc1be7dcd5515c91.jpg)



Figure 17: Recovered trajectories by the two methods.

FlipTracer at all distances. Specifically, even when the inter-tag distance is only 3cm, Fireworks incurs only a 0.03 rad median error in phase estimation and a 0.005 median error in amplitude estimation.

Performance under different bitrates. Besides the number of the tags, tags' bitrate is also an important factor which determines how fast the signal moves on the IQ domain. So in this experiment, we observe how different bitrates of the tags affect the performance of Fireworks and FlipTracer. Again, we use three tags and the bitrate of the tags change from 100Kbps to 500Kbps. Since the WISP platforms currently support only a 256Kbps bitrate, we conduct simulations to see the performance of the two methods with 500 Kbps bitrate. The result is shown in Fig. 16. We find that for both the two methods, the bitrate more affects the error variance of channel estimation. Compared with FlipTracer, Fireworks is more robust to the high bitrate because it is designed to estimate the channels of the tags directly from the moving trajectory of the collided signal.

# 7.3 Sensing accuracy

In this section, we use target tracking as an example to evaluate how Fireworks improves the performance of the backscatter based sensing applications. In the experiment, we let the tags move together along different tracks. Three antennas are deployed around the three corners of the $100 \times 150 \, cm^{2}$ surveillance region. To avoid the interference between them, we set them to different frequencies.
We compare the performance of two tracking methods:

- Tagoram. Tagoram is a state-of-the-art tracking method which is able to reconstruct the moving trajectory of a tag based on the phase measurements of its signal. In Tagoram, the tags are required to transmit sequentially based on the FSA protocol.   
- Tagoram+Fireworks. In this method, the tags are allowed to transmit simultaneously. Specifically, the reader first use Fireworks to recover the channel parameters of all the tags from the parallel transmitted signal. The recovered channels are then used by Tagoram for tracking.

Trajectory accuracy In the experiment, we let three tags move simultaneously along trajectories with different shapes (a line trajectory and a circle trajectory) and of different letters, like the cases shown in Fig. 17. The movement along each trajectory is completed within 1.5 second. Fig. 17 shows an example of the recovered trajectories. The trajectories in gray are the ground truths, while the blue and red ones are the estimates of Tagoram and Tagoram+Fireworks, respectively. As seen, Tagoram+Fireworks accurately reconstructs not only the relatively straight segments but also the curved strokes, while the trajectories of Tagoram deviate significantly from the ground truths, especially for the trajectories with higher complexity. This is due to the sharply reduced sampling rate of Tagoram when three tags transmit simultaneously.

![](images/db6d84030048d7dad19bedf7b34a5a8fee4395267ddf72ca07cbea78257ce7ad.jpg)



Figure 18: CDF of trajectory error.

We repeat the above experiment for 20 times. Figure 18 shows the CDF of the trajectory errors for Tagoram and Tagoram+Fireworks. Here the trajectory error is calculated as the Procrustes distance between the recovered trajectory and the ground truth. As shown by the figure, the median error of Tagoram+Fireworks is 1.1 cm and the 90th percentile is 1.5 cm. For Tagoram, the median error is 3.6 cm and the 90th percentile is 4.5 cm. With Fireworks, the tracing accuracy of Tagoram can be improved by almost 3×.

Performance under different numbers of tags. In this experiment, we change the number of tags from 1 to 4. Under each tag number, we let the tags move along the trajectories shown in Fig. 17 for 20 times. The CDF of the trajectory errors for Tagoram and Tagoram+Fireworks are shown in Fig. 19.

The figure shows that Fireworks+Tagoram significantly outperforms Tagoram especially with more tags. This is owning to the high sampling rate of Fireworks. Specifically, when there is only one tag, the sampling rate of Tagoram is about 57Hz. In this case, the Fireworks+Tagoram only slightly outperforms Tagoram. When there are two tags, the sampling rate of Tagoram decreases to 39Hz. As a result, the median error of Tagoram increases to 1.7cm and the 90th percentile increases to 2.6cm. While, for Fireworks+Tagoram, its median error and 90th percentile are 1cm and 1.4cm, outperforming Tagoram by almost 2×.

![](images/4c36728981f70ea23e5cc8eac4d7b8e5dcdd44834a57b96bd5c3df313c5e6dca.jpg)



(a) One tag

![](images/d2affc161e3d7a5307546f1e7cf7e6af50e1bf39199f58e481e4fc25132dd7f3.jpg)



(b) Two tags

![](images/126c8be248e30d60d8dec0e18c2c68b7d4bb2be96767c9d98a59746b5bc5682d.jpg)



(c) Three tags

![](images/93b9fc3f6b5ac1fbf75cc3332e2a6d9a2a100e2a293233db98029b3445ba9ea0.jpg)



(d) Four tags

Figure 19: CDF for tracking error with different numbers of simultaneous tags.   
![](images/7c4d876ad8e9c386e31404d76e8f3946c187129040a3a5baa23b8368365dd285.jpg)



(a) Low complexity: Line

![](images/162aa3fad6d2a1efd1701559b3c51c052ed9b4649b2610908d962f23c45ec0d4.jpg)



(b) Medium complexity: Circle

![](images/8ed25c18a9180a291c3683561e53fa9c244d2fc37cfabeb51207f9259ea8e489.jpg)



(c) Low complexity: Letters   
Figure 20: CDF for tracking error of trajectories with different complexities.

When the number of tags increases to four, the median error of Tagoram+Fireworks is 1.3cm and the 90th percentile is 1.5cm. No significant performance degradation is observed compared with the two-tag case. While for Tagoram, its median error increases to 5.1cm and the 90th percentile increases to 6cm. Fireworks can improve the performance of Tagoram by 4× in the four-tag case.

Performance for trajectories with different complexities. The complexity of the trajectory is also an important factor that affects the performance of the tracking systems. First, since the movement along all the trajectories are completed within the same time length (1.5 second), different complexities of the trajectories means different moving speeds. In addition, trajectories that have more curved strokes or sharp corners (e.g., letter 'M') usually lead to higher tracking difficulty. So we divide the test shapes into three groups according to the complexity of their trajectories. The CDF of the trajectory errors of Tagoram and Tagoram+Fireworks for different groups of trajectories are shown in Fig. 20.

By comparing the three figures, we can see that the improvement that brought by Fireworks is more obvious with complex trajectory. Specifically, Tagoram's median tracing accuracy for the trajectories with high, medium, and low complexities are 1.1cm, 2.5cm, and 3.2cm, respectively. While after combined with Fireworks, its accuracy increased to 0.7cm, 1.0cm, and 1.2cm, which means 1.5×, 2.5×, and 2.7× performance improvements, respectively.

# 8 RELATED WORK

Many works have been proposed to process parallel transmitted signals. The best known group of methods are the MIMO-based technologies $[2, 29, 34]$ . Specifically, they model the received signal as a linear combination of the channels of the transmitters and the symbols they transmit. Then given the known channel parameters, the symbols transmitted by each transmitter can be obtained using

matrix inversion methods. Note that in these works, the channels of the transmitters are considered as prior known, so these works cannot be used in our scenario where the channels should be estimated directly from parallel transmitted signals.

Some works are able to separate the parallel transmitted signal without the channel information. An typical example is Successive Interference Cancelation (SIC) [7]. However, SIC requires significant difference in the SNR of the colliding signals, hence it only applies to limited scenarios. Methods like ZigZag [6] and mZig [20] decode the collision base on the assumption that the collision is a linear addition result of the colliding signals, which is however not the case of backscatter transmission.

Recently, many methods are designed to decode the parallel transmitted backscatter signals $[1, 3, 4, 8–10, 16, 17, 19, 26, 32, 39]$ . We have seen inspiring progress in this area in recent years. Specifically, LF-Backscatter $[10]$ , BiGroup $[26]$ , and FlipTracer $[17]$ can decode the collided signals by exploiting the spatial and/or temporal characteristics of signals' combined states. The latest proposal Hubble $[16]$ further improves the practical usability of the parallel backscatter technology, achieving a 5-tag parallelism under relatively weak SNR (signal to noise ratio). However, all of the above methods just able to recover the coarse-grained signal state of each tag, but cannot obtain the fine-grained channel parameters.

Compared with the above parallel decoding methods, Fireworks deepens the level of signal processing and extracts the channel parameters of backscattered signals, which are blurred by inter-tag interference and fast-moving property of the signal. Given the empowered signal processing capacities of Fireworks, we can support many emerging IoT applications, especially those multi-target sensing applications with real-time requirement.

# 9 CONCLUSIONS

When a wireless channel is used for sensing application, accuracy and efficiency are two equally important and mutually influencing factors, but the latter is often overlooked. This paper studies the backscatter based sensing from a new angle, namely channel estimation of parallel backscattered signals. With an eye on the increasingly dense deployment of backscatter based IoT devices, how to make them work together as efficiently as possible is clearly a significant issue. Our proposal Fireworks is the first approach that enables channel estimation of parallel backscattered signals. Instead of measuring any deterministic signal state, Fireworks estimates the channels according to the characteristics of signal movement in the IQ domain. Fireworks makes accurate channel estimation and indeed enhances the efficiency and accuracy of backscatter based sensing applications. In our future work, we plan to integrate Fireworks into more sensing applications and systems. We will also explore the multi-antenna approach on the reader, which potentially further increases the capacity of parallel channel estimation.

# ACKNOWLEDGMENT

This work was supported in part by National Key R&D Program of China No. 2017YFB1003000, National Natural Science Fund of China No.61772306 and No.61902213.

# REFERENCES

[1] O. Abari, D. Vasisht, D. Katabi, and A. Chandrakasan. Caraoke: An e-toll transponder network for smart cities. In MobiCom, 2018.   
[2] N. Anand, R. E. Guerra, and E. W. Knightly. The case for uhf-band mu-mimo. In MobiCom, 2014.   
[3] C. Angerer, R. Langwieser, and M. Rupp. Rfid reader receivers for physical layer collision recovery. IEEE Transactions on Communications, 58(12):3526–3537, 2010.   
[4] A. Bletsas, J. Kimionis, A. G. Dimitriou, and G. N. Karystinos. Single-antenna coherent detection of collided fm0 rfid signals. IEEE Transactions on Communications, 60(3):756–766, 2012.   
[5] A. Dhekne, M. Gowda, Y. Zhao, H. Hassanieh, and R. R. Choudhury. Liquid: A wireless liquid identifier. In MobiSys, 2018.   
[6] S. Gollakota and D. Katabi. Zigzag decoding: Combating hidden terminals in wireless networks. In SIGCOMM, 2008.   
[7] D. Halperin, T. Anderson, and D. Wetherall. Taking the sting out of carrier sense: Interference cancellation for wireless lans. In MobiCom, 2008.   
[8] M. Hessar, A. Najafi, and S. Gollakota. Netscatter: Enabling large-scale backscatter networks. In NSDI, 2019.   
[9] P. Hu, P. Zhang, and D. Ganesan. Leveraging interleaved signal edges for concurrent backscatter. In HotWireless, 2014.   
[10] P. Hu, P. Zhang, and D. Ganesan. Laissez-faire: Fully asymmetric backscatter communication. In SIGCOMM, 2015.   
[11] E. Ilie-Zudor, Z. Kemény, F. V. Blommestein, L. Monostori, and A. V. D. Meulen. A survey of applications and requirements of unique identification systems and rfid techniques. Elsevier Computers in Industry, 62(3):227–252, 2011.   
[12] C. Jiang, Y. He, S. Yang, J. Guo, and Y. Liu. 3d-omnitrack: 3d tracking with cots rfid systems. In IPSN, 2019.   
[13] C. Jiang, Y. He, X. Zheng, and Y. Liu. Orientation-aware rfid tracking with centimeter-level accuracy. In IPSN, 2018.   
[14] W. Jiang, C. Miao, F. Ma, S. Yao, Y. Wang, Y. Yuan, H. Xue, C. Song, X. Ma, D. Koutsonikolas, W. Xu, and L. Su. Towards environment independent device free human activity recognition. In MobiCom, 2018.   
[15] H. Jin, J. Wang, Z. Yang, S. Kumar, and J. Hong. Wish: Towards a wireless shape-aware world using passive rfids. In MobiSys, 2018.   
[16] M. Jin, Y. He, X. Meng, D. Fang, and X. Chen. Parallel backscater in the wild: When burstiness and randomness play with you. In MobiCom, 2018.   
[17] M. Jin, Y. He, X. Meng, Y. Zheng, D. Fang, and X. Chen. Fliptracer: Practical parallel decoding for backscatter communication. In MobiCom, 2017.   
[18] B. Kellogg, V. Talla, and S. Gollakota. Bringing gesture recognition to all devices. In NSDI, 2014.   
[19] R. Khasgiwale, R. Adyanthaya, and D. Engels. Extracting information from tag collisions. In RFID, 2009.   
[20] L. Kong and X. Liu. mzig: Enabling multi-packet reception in zigbee. In MobiCom, 2015.

[21] K. C.-J. Lin, S. Gollakota, and D. Katabi. Random access heterogeneous mimo networks. In SIGCOMM, 2011.   
[22] Q. Lin, L. Yang, H. Jia, C. Duan, and Y. Liu. Revisiting reading rate with mobility: Rate-adaptive reading in cots rfid system. In CoNEXT, 2017.   
[23] J. Liu, X. Chen, S. Chen, X. Liu, Y. Wang, and L. Chen. Tagsheet: Sleeping posture recognition with an unobtrusive passive tag matrix. In INFOCOM, 2019.   
[24] Z. Luo, Q. Zhang, Y. Ma, M. Singh, and F. Adib. 3d backscatter localization for fine-grained robotics. In NSDI, 2019.   
[25] Y. Ma, N. Selby, and F. Adib. Drone relays for battery-free networks. In SigComm, 2017.   
[26] J. Ou, M. Li, and Y. Zheng. Come and be served: Parallel decoding for cots rfid tags. In MobiCom, 2015.   
[27] S. Pradhan, E. Chai, K. Sundaresan, and L. Qiu. Rio: A perspective rfid-based touch gesture interface. In MobiCom, 2017.   
[28] S. Pradhan, E. Chai, K. Sundaresan, S. Rangarajan, and L. Qiu. Konark: A rfid based system for enhancing in-store shopping experience. In MobiSys, 2017.   
[29] H. Rahul, S. Kumar, and D. Katabi. Megamimo: Scaling wireless capacity with user demands. In SIGCOMM, 2012.   
[30] L. Shangguan, Z. Yang, A. Liu, Z. Zhou, and Y. Liu. Relative localization of rfid tags using spatial-temporal phase profiling. In NSDI, 2015.   
[31] L. Shangguan, Z. Zhou, and K. Jamieson. Enabling gesture-based interactions with objects. In MobiSys, 2017.   
[32] D. Shen, G. Woo, D. P. Reed, A. B. Lippman, and J. Wang. Efficient and reliable low-power backscatter networks. In RFID, 2009.   
[33] S. Manzari, C. Occhiuzzi, S. Nawale, A. Catini, C. D. Natale, and G. Marrocco. Polymer-doped uhf rfid tag for wireless-sensing of humidity. In RFID, 2012.   
[34] S. Sur, I. Pefkianakis, X. Zhang, and K.-H. Kim. Practical mu-mimo user selection on 802.11ac commodity networks. In MobiCom, 2016.   
[35] D. Tse and P. Viswanath. Fundamentals of Wireless Communication. Cambridge University Press, 2005.   
[36] C. Wang, L. Xie, W. Wang, T. Xue, and S. Lu. Moving tag detection via physical layer analysis for large-scale rfid systems. In INFOCOM, 2016.   
[37] G. Wang, H. Cai, C. Qian, J. Han, X. Li, H. Ding, and J. Zhao. Hu-fu: Towards replay-resilient rfid authentication. In MobiCom, 2018.   
[38] J. Wang, O. Abari, and S. Keshav. Rfid hacking for fun and profit. In MobiCom, 2018.   
[39] J. Wang, H. Hassanieh, D. Katabi, and P. Indyk. Efficient and reliable low-power backscatter networks. In SIGCOMM, 2012.   
[40] J. Wang and D. Katabi. Dude, where's my card? rfid positioning that works with multipathand non-line of sight. In SIGCOMM, 2013.   
[41] J. Wang, D. Vasisht, and D. Katabi. Rf-idraw: Virtual touch screen in the air using rf signals. In SIGCOMM, 2014.   
[42] J. Wang, J. Xiong, X. Chen, H. Jiang, R. K. Balan, and D. Fang. Tagscan: Simultaneous target imaging and material identification with commodity rfid devices. In MobiCom, 2017.   
[43] J. Wang, J. Xiong, H. Jiang, X. Chen, and D. Fang. D-watch: Embracing "bad" multipaths for device-free localization with cots rfid devices. In MobiSys, 2018.   
[44] T. Wei and X. Zhang. Gyro in the air: Tracking 3d orientation of batteryless internet-of-things. In MobiCom, 2016.   
[45] L. Xie, C. Wang, A. X. Liu, J. Sun, and S. Lu. Multi-touch in the air: Concurrent micromovement recognition using rf signals. IEEE/ACM Transactions on Networking, 26(1):231–244, 2017.   
[46] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu. Tagoram: real-time tracking of mobile rfid tags to high precision using cots devices. In MobiCom, 2014.   
[47] L. Yang, Y. Li, Q. Lin, X.-Y. Li, and Y. Liu. Making sense of mechanical vibration period with sub-millisecond accuracy using backscatter signals. In MobiCom, 2016.   
[48] L. Yang, Q. Lin, X.-Y. Li, T. Liu, and Y. Liu. See through walls with cots rfid system! In MobiCom, 2015.   
[49] W. Zhou, T. Das, L. Chen, K. Srinivasan, and P. Sinha. Basic: Backbone-assisted successive interference cancellation. In MobiCom, 2016.