# Parallel Backscatter: Channel Estimation and Beyond

Meng Jin, Member, IEEE, ACM, Yuan He , Senior Member, IEEE, Member, ACM, Chengkun Jiang, Student Member, IEEE, ACM, and Yunhao Liu, Fellow, IEEE, ACM

Abstract— As backscatter-based IoT applications get proliferated, how to exploit backscattered signals for efficient sensing becomes a significant issue. Backscatter-based sensing requires accurate estimation of a backscatter channel (phase and amplitude), which is distorted when multiple signals collide with each other. As a result, the state of the arts is limited to either parallel decoding of collided signal or channel estimation with clean signal. Motivated by the need of high sensing capacity, we in this article present Fireworks, the first approach for channel estimation of parallel backscattered signals. The insight of Fireworks is that although the channel is distorted due to collision, the movements of the ON-OFF Keying modulated signal still preserve the channel properties of the respective tags. By modeling the relationship between the channels and the signal’s moving trajectory in the IQ domain, one can make accurate estimation of the channels directly from the collision. We address practical problems of Fireworks, such as the high computing complexity and the compatibility with the commercial MAC protocol, and implement Fireworks. The results show that Fireworks is able to estimate the channels of up to five tags in parallel. When applied to the tracking application, Fireworks achieves 2∼4× improvement in the tracking accuracy, compared with the state-of-the-art approach.

Index Terms— Backscatter, wireless sensing, channel estimation, parallel transmission.

# I. INTRODUCTION

D UE to its low cost and battery free feature, backscatterbecomes a promising technology for IoT (Internet of becomesa promising technology for IoT (Internet of Things). Today, we have seen a huge number of backscatter devices deployed in various scenarios, performing functions like warehouse management and supply chain monitoring [1]–[3]. With the rapid progress in the area of wireless sensing, recent works propose to exploit the backscattered signals for sensing purposes. The potential applications span across a wide variety of scenarios, such as localization, tracking, motion recognition, etc [4]–[20].

In spite of the apparent need of backscatter-based sensing, the efficiency of the backscatter channel to be used for sensing

Manuscript received March 22, 2020; revised November 2, 2020 and December 27, 2020; accepted January 28, 2021; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor B. Shrader. This work was supported in part by the National Key R&D Program of China under Grant 2017YFB1003000 and in part by the National Natural Science Fund of China under Grant 61772306 and Grant 61902213. (Corresponding author: Yuan He.)

The authors are with the School of Software and BNRist, Tsinghua University, Beijing 100084, China (e-mail: he@greenorbs.com).

Digital Object Identifier 10.1109/TNET.2021.3058977

is far restricted. Backscatter-based sensing requires accurate estimation of a backscatter channel in terms of phase and amplitude, which are key indicators of the target’s state. When there are multiple targets to be sensed, inevitably their backscattered signals will collide frequently. Collision of signals will distort the backscatter channel, making it extremely difficult to recover the channel state.

Based on the above discussion, we find a fundamental problem: can we estimate the channel of parallel backscattered signals? Answer to this problem has great significance in real applications. For example, in automated factories, the trajectories of objects on the production lines should be tracked simultaneously. In some novel HCI (Human Computer Interaction) applications, an array of RFID tags is deployed to emulate a virtual keyboard [7], where simultaneous sensing of all the tags’ states is clearly a critical component of these systems. As we will analyze in Sec. II-A, whether channel estimation can be parallelized not only determines the sensing efficiency, but also affects the accuracy of sensing results.

Considering that many interference resolution methods are able to separate the collided signal, one may wonder: why not estimate channels directly based on the separated signal? For most interference resolution approaches, e.g. the MIMO based methods [21]–[25], channel parameters are the prerequisites for decoding the parallel transmitted signals. Without channel information, they cannot perform parallel decoding, not to mention channel estimation based on parallel decoding. Moreover, backscatter devices often suffer serious mutual interference, as is called inter-tag interference. As a result, the collided signal isn’t the linear addition of the original backscattered signals. Consequently, although there have been some methods that can decode collided signals without channel information [26]–[28], they still cannot obtain the channel parameters.

Channel estimation of parallel backscatter is indeed a daunting task, with the following critical challenges: First, a backscattering tag keeps flipping their states between H and L. The rate of flips is essentially determined by the encoding bit rate of the tag. When there are multiple colliding tags in the channel, the collided signal is highly dynamic and transfers among different combined states at an even higher rate. It is extremely difficult to find steady signal samples that reflect the channel parameters. Second, the above-mentioned inter-tag interference will further distort the collided signals and introduce uncontrollable estimation errors.

In order to tackle the above problems, we in this article propose Fireworks, the first approach for channel estimation of parallel backscattered signals. The key insight of Fireworks is that although the state of the collided signal keeps changing, the resulting moving trajectory of the signal on the IQ (In-phase and Quadrature) domain is determined by and in turn reflects the channel parameters of the tags and the interference among them. Specifically, this insight attributes to the following observations:

• The geometric properties (i.e., direction and length) of a tag’s transition path between two states reflect the phase and amplitude of that tag’s signal.   
• The relationship between signal’s geometric properties and tag’s channel parameters are preserved after collision.   
• Inter-tag inference can be separated from tags’ signal in the signal trajectory.

Based on the above insight, we propose an Inter-tag Interference Aware (IIA) model that captures the exact transformation from the channel parameters to the trajectory of collided signals. To extract the channels from the signals, we invert the above transformation by solving a global optimization problem, which minimizes the overall distance between the signal samples and the trajectory generated by the IIA model. Our contributions can be summarized as follows:

We disclose the principle of inter-tag interference under parallel backscatter and propose the IIA model that describes the exact relationship between channel parameters and the geometric properties of the signal trajectory.   
Based on the IIA model, we present a parallel channel estimation approach named Fireworks, and address several challenges to make it a useable approach, such as the high computing complexity and the compatibility with the commercial MAC protocol.   
We implement Fireworks and evaluate its performance with extensive experiments. The results show that Fireworks accurately estimates channel parameters of up to five parallel tags, with the mean errors of 0.054 rad. in phase and 0.0029 in amplitude. When applied to the tracking application, Fireworks achieves 2∼4× improvement in tracking accuracy, compared with a state-of-the-art approach [12].

Roadmap. Section II presents the motivation and challenges of our work. In Sections III, IV and V, we elaborate on the insight and the design of Fireworks. We present the evaluation results in Section VI. Section VII discusses the related work. Section VIII concludes this work.

# II. PARALLEL BACKSCATTER

# A. Why to Parallelize Channel Estimation?

We use target tracking as an example to show how our work benefits backscatter-based sensing applications. A tag’s moving trajectory is estimated by accumulating the changes in tag’s channel parameters (i.e., phase and amplitude). In achieving accurate trajectory recovery, the interval between two consecutive channel estimation should be sufficiently short. In other words, a sufficiently high rate of channel estimation is desired.

TABLE I NOTATIONS 

<table><tr><td> $N_{all}$ </td><td>The number of tags</td></tr><tr><td>N</td><td>The number of colliding tags</td></tr><tr><td>M</td><td>The number of tags the reader is capable to resolve</td></tr><tr><td>K</td><td>Frame-size or total number of slots</td></tr><tr><td> $\alpha_x$ </td><td>The signal amplitude of x</td></tr><tr><td> $\delta_x$ </td><td>The signal phase of x</td></tr><tr><td> $S_x$ </td><td>Signal from x</td></tr><tr><td> $s_x$ </td><td>Signal state of x</td></tr></table>

![](images/db0dadb626a48d3cf5ef6549420abd006b6d7446477ec823e8b3a2a62910c6e0.jpg)



(a) Tracking with different IRR

![](images/a1353cee3aee76d00d0120ae49bbbcd4b5a7571a510c24dbe8b17543dd0326a9.jpg)



(b) IRR under different tag population   
Fig. 1. Impact of IRR on sensing applications.

Fig. 1(a) compares the calculated trajectories of a letter “M” under different channel estimation rates. We can see large deviation from the ground truth when the channel estimation rate is low. Since channel estimation depends on the successful reception of a tag’s signal, so channel estimation rate of a tag equals to its individual reading rate (IRR). We first check the IRR of the commercial backscatter system that adopts the FSA (Framed Slotted ALOHA) protocol for tag interrogation. Then we show how parallel channel estimation improves the channel estimation rate.

In the FSA protocol, the reader divides time into K slots, and each tag randomly picks a slot to reply. Since the tags are not coordinated, they may collide in reply. We denote the reading capacity of the reader as M , which means the reader can read up to M colliding tags in one slot. Then, if we have $N _ { a l l }$ tags, the throughput (successful readouts per slot) of the system will be:

$$
T h (M, N _ {a l l}) = \sum_ {N = 1} ^ {M} N \binom {N _ {a l l}} {N} \left(\frac {1}{K}\right) ^ {N} \left(1 - \frac {1}{K}\right) ^ {N _ {a l l} - N} \tag {1}
$$

Note that Eq. (1) is used to express the throughput of a RFID system when the reading capacity is M . To simplify the expression, some detailed restrictions in the EPC protocol (e.g., one tag is not allowed to response multiple times in one session), which do not affect the throughput of the system, are not considered in Eq. (1).

Based on Eq. (1), the number of slots required to collect $N _ { a l l }$ tags can be estimated by $\begin{array} { r } { S ( M , N _ { a l l } ) \stackrel { { } } { = } \lceil \frac { N _ { a l l } } { T h ( M , N _ { a l l } ) } \rceil } \end{array}$ . ( ) =If the duration of a slot is τ , the entire inventory cost can be calculated by $\Lambda ( M , N _ { a l l } ) = \tau _ { 0 } + \tau \cdot S ( M , N _ { a l l } )$ , where $\tau _ { 0 }$ Λ( ) = + ( )is the start-up cost [29], including the time cost for tasks like broadcasting the SELECT command, synchronization, and clearing history states. Then the IRR is given by:

![](images/0556d4a6355a4e63a9dc9eaf3e7227dfb50bdea13dafa96ebc0936afe1c3f432.jpg)



Fig. 2. Visualization of tag’s signal in IQ domain.

$\begin{array} { r } { I R R ( M , N _ { a l l } ) = \frac { 1 } { \Lambda ( M , N _ { a l l } ) } } \end{array}$ . According to our measurement ( )result, we have $\tau _ { 0 } ~ \dot { = } ~ 1 9 m s$ and $\tau = 0 . 5 m s$ . Assume that = 19 = 0 5the reader can always select the optimal K based on Eq. (1), we can get the IRR under different $N _ { a l l }$ , as shown in Fig. 1(b).

Figure 1(b) shows that when $M \ = \ 1$ , IRR significantly = 1drops with the increased number of tags. This precludes many sensing applications [11], [29], [30]. For example, in automated factories, a 30Hz IRR is required to monitor the fast moving items on the pipeline [14], [15]. According to Fig. 1(b), however, such an IRR is achieved only when the number of targets is lower than 10, which is unlikely on the pipeline. That means Tagbeat works only when there are 1∼2 vibration sources, which is obviously insufficient in realworld scenarios. Note that Fig. 1(b) shows the ideal case where the reader can always select the optimal slot number K. The IRR will be even lower in practice, as shown in many existing studies [29].

The above dilemma can be mitigated with parallel channel estimation. Fig. 1(b) tells that increasing the reading capacity M significantly increases the IRR and thus the channel estimation rate. For a system with $M = 5$ , when 70 tags coexist = 5in one environment, the channel estimation rate can be kept as high as 30Hz. This means that we can track the movement of more than 70 targets concurrently. Such a capacity is sufficient and attractive for many real applications. Motivated by the need of high capacity of sensing, we continue to study the feasibility and the solution for parallel channel estimation.

# B. Understanding Parallel Backscatter

The wireless channel describes how a signal changes as it propagates from transmitter to receiver. The transmitted signal is denoted by $S _ { 0 }$ . The received signal S is given by:

$$
S = h \cdot S _ {0} \tag {2}
$$

where $h = \alpha e ^ { \mathbf { j } \delta }$ denotes the channel, and α and δ denote the =channel parameters amplitude and phase, respectively.

Observed in the IQ domain, the theoretical representation of the signal is a single point (as shown in Fig. 2(a)), whose location is determined by the channel parameters. Specifically, the length and direction of the signal vector $\vec { S }$ correspond to α and δ of the signal, respectively.

When only one tag is transmitting, there are two channels: i) the channel between the reader and the tag, where the reader A transmits a carrier wave $S _ { 0 }$ and the tag $T$ responds its data $s ( t )$ by reflecting the carrier wave using OOK modulation; ( )ii) the channel between the reader and the background reflectors. Here we abstract the background reflections as from a virtual point $B ,$ according to the linear addition principle of signals. The received signal at the reader can be expressed by:

$$
S (t) = s (t) \cdot h _ {T} \cdot S _ {0} (t) + h _ {B} \cdot S _ {0} (t) \tag {3}
$$

where $s ( t ) = 0$ or  depends on the encoded bits. $h _ { T }$ and ( ) = 0 1hB respectively denote the channels along the round-trips $A  T  A$ and $A  B  A$ .

The representation of the received signal in the IQ domain is determined by the channels of both sources of reflections:

$$
\overrightarrow {S} (t) = \overrightarrow {S} _ {B} + s (t) \cdot \overrightarrow {S} _ {T} \tag {4}
$$

Eq. (4) tells that due to the OOK modulation, the signal is theoretically present at two points (Fig. 2(b)), respectively corresponding to the silence (L) and the reflecting (H) states of the tag. By subtracting the L-state from the H -state signal, we can remove the background reflection and derive the vector that denotes the channel of the tag.

When there are N tags, the IQ domain representation of the signal is determined by the channels of all the tags:

$$
\overrightarrow {S} (t) = \overrightarrow {S} _ {B} + \sum_ {i = 1} ^ {N} s _ {i} (t) \cdot \overrightarrow {S} _ {T _ {i}} \tag {5}
$$

where $s _ { i } ( t )$ denotes the state of Tag $T _ { i }$ . In this case, the col-( )lided signal theoretically form $2 ^ { N }$ points, each representing a combined state of the N tags. Fig. 2(c) shows an example with two tags. The $2 ^ { 2 } = 4$ points represent the four combined 2 = 4states of the tags, namely LL, HL, LH, and HH.

In collision cases, a pair of points whose corresponding states differ from each other in only one tag’s state is called neighboring points (e.g., LL and $H L )$ . That tag’s channel is characterized by the vector connecting the two points. In the N -tag collision case, each tag will have N equivalent vectors, as shown by the example with 2∼4 tags in Fig. 2(d).

The existing parallel decoding approaches [27], [28] are able to identify the combined state of each point, so that the data sequence of each tag $\operatorname { ( i . e . , } \ s _ { i } ( t ) \ )$ is obtained. Based on the ( )identified points, one can find the N pairs of neighbour points for each tag. Provided that the relative locations of all the paired points are known, the channel parameters of the tags can be accordingly estimated.

# C. Challenges in Parallel Channel Estimation

The previous subsection presents an ideal case of parallel backscatter. The real-world signals induce a series of critical challenges, which we will empirically show in this section.1

We start from a simple case with one tag, as shown in Fig. 3(a). Due to the noise, the signal samples belonging to the same state form a cluster rather than a single point. Meanwhile, we can also see some signal samples lie between the two clusters. This is caused by the signal’s imperfect

1The experiment results in this section are collected from WISP tags. Due to the page limitation, the signals from other platforms (e.g., commercial tags) are omitted since they exhibit similar results.

![](images/1fe53113a2ff043f4fb0c02cfb302cefb1accd2d52b6bb8a0c606ed919664348.jpg)



(a)

![](images/bbb77f70bb03da1c19ce8e90058e5322b724b0fcb469705bc26371af501ea914.jpg)



(b)

Fig. 3. Received signal: (a) one tag; (b) three tags.   
![](images/79f81171b3e194ece5cec69798c6ff7ebb534caa4c556854603b4c5fdec89683.jpg)



(a) Low SNR

![](images/00005da27695734bf5e38ab5a75a02800313f746cd153ffc8ad496769d4b989a.jpg)



(b) High SNR   
Fig. 4. How SNR affect the phase measurement accuracy.

and non-instantaneous transitions between different states. The noises and the transitional samples obscure the locations of the signal states. Ideally, we can pinpoint the location of a state by averaging locations of the samples on that state. The subfigure in Fig. 3(a) shows the density distribution of the samples on the H state. As we can see, most samples are concentrated in the center area, which indicates the location of the state.

Things totally change when it comes to the multi-tag collision case. In this case, the distribution of the signal samples will become dispersed and largely deviated from the theoretical locations, due to the fast-varying property of the collided signal and the inter-tag interference among the tags.

1) Fast Variation of Signal: Fig. 3(b) shows an example of three tags. Since all the tags keep flipping their states, the collided signal frequently transfers among different combined states, as shown by the state sequence in Fig. 3(b)-top. This leads to a fast-moving signal in the IQ domain. To visually illustrate such mobility, we extract a 2μs segment from the sequence and plot its IQ domain trajectory in Fig. 3(b)-bottom. We can see that the signal trajectory can go through the entire area of signal samples even in such a short period. We also show the density distribution of the samples in Fig. 3(b). As we can see, the samples aren’t concentrated on any cluster area, making it difficult to pinpoint the location of any signal state.

This phenomenon is caused by signal’s short dwell time in cluster areas. Suppose there are N tags and the frequency of state flip for every tag is BHz. Our measurement result shows that the duration of one flip is $\tau _ { f } \approx 0 . 2 \mu s$ , then in one second, the time spent on state transition is $T _ { t } = \boldsymbol { N } \cdot \boldsymbol { B } \cdot \boldsymbol { \tau _ { f } }$ , while the =time for the signal to dwell on clusters is $T _ { d } = 1 - N \cdot B \cdot \tau _ { f }$ . = 1With more tags transmitting simultaneously, the dwell time on clusters becomes shorter. For example, when $N \ = \ 4$ tags transmit at 640Kbps $( B = 1 . 2 8 \mathrm { M H z } )$ = 4, the signal keeps = 1 28transferring among different states and seldom stays on any state $( T _ { d }$ approaches 0). So when the number of tags increases, we cannot collect enough samples to pinpoint the location of each state. According to the law of large numbers, given a certain noise level $\sigma$ (signal’s standard deviation on IQ domain), the position error e will be inversely proportional to the number of samples $n _ { c }$ as:

![](images/a775aa95900234dfd14b512cc9ee2fda1771f5874cb4b02467e8cacfc2bb348e.jpg)



(a) Two tags

![](images/bf8bbb0f75b1b7ebc58045e25e0abc4ae43f702a629233f1414828510c1d9e4f.jpg)



(b) Three tags   
Fig. 5. Signal distortion caused by inter-tag interference.

$$
e \propto \frac {\sigma}{\sqrt {n _ {c}}} \tag {6}
$$

The above problem becomes more serious with decreased SNR (Signal-Noise Ratio). Specifically, with the decreased signal SNR, the standard deviation of the samples’ locations increases and the distance between clusters decreases. This on one hand increases the error range (as shown by Eq. (6)). On another hand, a shorter distance between clusters will amplify the state position error, resulting in higher phase error, as shown by Fig. 4. Our experiments in Section VI show that when the SNR of the signal is 5 dB, the average based state positioning method may lead to 1.2 rad. phase estimation error.

2) Inter-Tag Interference: Recall that the tag transmits signal by reflecting the signal it receives. When two nearby tags transmit simultaneously, one tag will reflect not only the carrier wave from the reader, but also the signal from the other tag. Such an additional source of reflection leads to non-linear addition of the signal from two tags, which alters the locations of the signal samples. Fig. 5(a) and Fig. 5(b) show the collided signal of two and three tags, where tags are located with 10 cm spacing to each other. The figures show that due to the inter-tag interference, the signal vectors of the same tag aren’t consistent with each other in either length (amplitude) or direction (phase). We cannot figure out the exact channel parameters of this tag based on such distorted signal vectors.

Note that although the inter-tag interference occurs only between nearby tags (e.g., with a distance lower than 15cm), it is still necessary to mitigate the inter-tag interference, because many RFID based sensing applications involve closely located tags. For example, in pipeline monitoring [14], [15] and luggage tracking [12], the targets are closely located on the conveyor. Some HCI applications, like RFID glove [31] and RFID keyboards [7], deploy a set of closely located (≤ cm) tags on one target. Therefore, mitigating the inter-tag 1interference is important to many RFID sensing applications.

# III. INTUITION UNDERLYING FIREWORKS

Fireworks’s target is to extract channel of each tag from the fast-moving and largely distorted collision signal. To achieve this, Fireworks leverages the observation that although the

![](images/18b072812d7cc77a80cee68dc7f9b9c22296994496e25c39525b11d5d8bf9237.jpg)



(a) One tag

![](images/cc935e1e7473633d2a74f8f5a7ac31d25b4b49d7c6d7ab269d5a38b8d93963f3.jpg)



(b) Two tags   
Fig. 6. Theoretical trajectory of tags’ signal.

IQ domain location of the collided signal keeps changing, the way how the signal moves is deterministic. The geometric properties of the moving trajectory are determined by the channels of the tags and the inter-tag interferences. So, instead of relying on the exact locations of the signal, we can extract the channels directly from signal’s moving trajectory.

# A. Signal Trajectory

We start with the trajectory of one tag’s signal. Recall that the signal of a tag has two states, and the tag flips its state by changing the amount of energy it reflects. So if we denote the fraction of energy that the tag reflects by $\gamma ( t )$ (termed by ( )reflecting scale), the flip of the tag’s state can be viewed as the variation of $\gamma ( t )$ between 0 and 1, where $\gamma ( t ) = 0$ o r ( ) ( ) = 0 1indicates the L or H state of the signal. We can see that during the flipping process, the tag only changes the signal’s amplitude while the phase is fixed, as shown in Fig. 6(a). No matter whether the amplitude changes uniformly or not, the transition path of the signal will always be a straight path, whose geometric properties (i.e., length and the direction) exactly capture the amplitude and phase of the signal.

Considering the goal of parallel channel estimation, one may wonder whether the above properties of signal trajectory are still preserved under collisions. Indeed, in the collision cases, although all the tags keep flipping their states, the flips of different tags usually interleave with each other. This is caused by the intrinsic asynchronism of the tags, e.g., different response delay and different clock drifts across tags [27], [28], [32]. So, the whole trajectory of the collided signal is a simple connection of the transition paths of individual tags. Properties of each path still reflect the channels of the corresponding flipping tag.

As an example, Fig. 6(b) illustrates the trajectory of the signal from two tags. The four red points denote the locations of the combined states, and the four solid lines denote the transition paths. In this case, the signal trajectory can be approximated to a parallelogram, where the two pairs of parallel edges represent the channels of the two tags. The irregular trajectories (denoted by the dash lines) are caused by occasional aligned flips of two tags. Different aligning pattern (e.g., different starting time or different transition speed of the two tags) will lead to different shapes of the paths.

# B. Understanding the Inter-Tag Interference

The previous subsection discloses the relationship between the signal trajectory and the channels of the tags. This subsection examines how the inter-tag interference affects the relationship. We first consider a simple case with two tags, as shown by Fig. 7. In this case, besides the basic signals mentioned in Sec. II-B, there are two additional sources of signals: the signals transiting along the paths $A \  \ T _ { 1 } \ $ $T _ { 2 }  A$ and the paths $A  T _ { 2 }  T _ { 1 }  A$ .

![](images/74ebc058bb0576fb0ed5d0cde926d4e4e4ec0087113cdb64f6b644779f2c1ebb.jpg)



Fig. 7. Signal propagation with inter-tag interference.

We find that both the two interfering signals experience two reflections, i.e., by $T _ { 1 }$ and $T _ { 2 } .$ . This reveals an interesting fact: the inter-tag interference between two tags occurs only when both the two tags are in their reflecting (H) states. Although a tag also reflects tiny amount of signal at its L state, the reflected signal is very weak, which will decay to nearly zero after two reflections. So we can ignore the interfering signal when either of the tags is on L state.

To understand the impact of inter-tag interference on the signal trajectory, we can treat the interfered signal as if it is transmitted from a virtual signal source, which also flips between two states: silence and reflection. Specifically, it reflects the signal only when both the corresponding two tags are in the reflection states. Then, according to the principle of signal propagation and reflecting [33], the fraction of energy this virtual source reflects (denoted as $\gamma _ { I N T } ( t ) )$ is given by ( )the reflecting scale of the corresponding two tags: $\gamma _ { I N T } ( t ) =$ $\gamma _ { T _ { 1 } } ( t ) \cdot \gamma _ { T _ { 1 } } ( t )$ ( ) =. Then, the trajectory of the collided signal can ( ) ( )be viewed as a linear combination of the channels of the three reflection sources and their reflecting factors:

$$
\overrightarrow {S} (t) = \overrightarrow {S _ {B}} + \gamma_ {T _ {1}} (t) \overrightarrow {S _ {T _ {1}}} + \gamma_ {T _ {2}} (t) \overrightarrow {S _ {T _ {2}}} + \gamma_ {T _ {1}} (t) \gamma_ {T _ {2}} (t) \overrightarrow {S _ {I N T}} \tag {7}
$$

where different transition paths can be viewed as different combinations of the channels of the tags and the inter-tag interferences, as shown in Fig. 8(a). Taking the transitional sample A (which is collected when $\gamma _ { T _ { 2 } } ( t ) = 0 . 5 )$ as an exam-( ) = 0 5ple, its location is determined by a linear combination of signal vectors $\overrightarrow { S _ { B } } \ 0 . 5 \cdot \overrightarrow { S _ { T _ { 1 } } } , \overrightarrow { S _ { T _ { 2 } } }$ , and $0 . 5 \cdot \overrightarrow { S _ { I N T } }$ . Eq. (7) indicates 0 5 0 5that: i) the deviation of state HH (where $\gamma _ { T _ { 1 } } ( t ) = \gamma _ { T _ { 2 } } ( t ) = 1 )$ ( ) = ( ) = 1from its original position actually represents the signal vector of the inter-tag interference $\overrightarrow { S _ { I N T } } ; \mathrm { i i } )$ the two trajectories $L L  H L$ and $L L  L H ( \gamma _ { I N T } = \gamma _ { T _ { 1 } } ( t ) \cdot \gamma _ { T _ { 2 } } ( t ) = 0 )$ =are free from the inter-tag interference.

Then let’s consider the N -tag collision case. In this case, the trajectory of the collided signal is determined by the channels of both the N tags and the interferences among every estim $2 \sim N$ $\begin{array} { r } { N _ { i n t } = \sum _ { i = 2 } ^ { N } { \binom { N } { i } } } \end{array}$ er of interfering paths can be. Due to the signal attenuation, = the amplitude of the signal reflected for more than twice (e.g., the signal traveling from $A  T _ { 1 }  T _ { 2 }  T _ { N }  A$ in Fig. 7) will decay to nearly zero. This is demonstrated in our experiment result later. As a result, we can approximate the number of interferences as $\begin{array} { r } { M \approx \binom { N } { 2 } } \end{array}$ . Then the trajectory of the collided signal can be modeled as:

![](images/d45705d30e2968de11e9ec23de5ec28c6016eb22060cec237f42bed3624c379d.jpg)



(a) Two tags

![](images/21926d8710c7f042bad1111052c36e88d385896ddd22b2e701fd30e11d8f37dd.jpg)



(b) Three tags   
Fig. 8. The theoretical trajectory of the interfered signal.

$$
\overrightarrow {S} (t) = \overrightarrow {S _ {B}} + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} (t) \overrightarrow {S _ {T _ {i}}} + \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} \gamma_ {T _ {i}} (t) \gamma_ {T _ {j}} (t) \overrightarrow {S _ {I N T} ^ {(i , j)}} \tag {8}
$$

where S(i,j)INT ( $S _ { I N T } ^ { ( i , j ) } \left( i \neq j \right)$ denotes the inter-tag interference between $T _ { i }$ and $T _ { j }$ =. A three-tag example is shown in Fig. 8(b).

In summary, we have obtained a transformation between the channels of the tags and the geometric properties of the signal trajectory. Based on this knowledge, we can make accurate estimation of the channels directly from the collision.

# IV. DESIGN

A naive solution to estimate the channels is to use the uninterfered signal samples – the length and direction of the un-interfered paths characterize the tags’ channels. However, the number of the un-interfered samples decreases exponentially with the number of tags. For each tag, less than $\textstyle { \frac { N + 1 } { 2 ^ { N } } }$ of the signal samples can be used to extract its channel. Considering that the backscatter signal usually exhibits low SNR, using such a small fraction of samples will lead to excessively high estimation error. Our idea in solving this problem is to translate the channel estimation problem to a global optimization process: we can obtain the optimal channel estimation by finding the DTG that best fits the observed signal samples. By utilizing information contained in all the transition paths, the optimization process can obtain plenty of constraints to produce accurate results.

# A. The IIA Model

Suppose we have N tags $\textbf { T } = ~ \{ T _ { 1 } , . . . , T _ { N } \}$ , for each tag $T _ { i } ,$ =, its channel parameters can be represented by a 2-tuple $P _ { T _ { i } } ~ = ~ \left( \alpha _ { T _ { i } } , \delta _ { T _ { i } } \right)$ . The channel of the interference tags . The $T _ { i }$ and nal t $T _ { j }$ is represented byctory is represented $P _ { I N T } ^ { ( i , j ) } = ( \alpha _ { I N T } ^ { ( i , j ) ^ { \star } } , \delta _ { I N T } ^ { ( i , j ) } )$ = ( )by a set of samples whose locations are denoted by $( I , Q )$ . ( )We now present the mathematical formulations of the transform between a set of 2-tuples $\mathbf { P } = \{ \mathbf { P _ { T } } , \mathbf { P _ { I N T } } \}$ and the trajectory of the samples.

![](images/c50a6d10dc785c7beecf234955c29063ee5bbbe31e20d7b41f3629ece8bf9013.jpg)



Fig. 9. Fitting the DTG to the samples.

When N tags transmit in parallel, the signal trajectory is commonly determined by the channels of all the tags:

$$
\begin{array}{l} I (\boldsymbol {\gamma}) = \alpha_ {B} \cdot c o s (\delta_ {B}) + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} \cdot \alpha_ {T _ {i}} \cdot c o s (\delta_ {T _ {i}}) \\ + \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} \gamma_ {T _ {i}} \gamma_ {T _ {j}} \cdot \alpha_ {I N T} ^ {(i, j)} \cdot c o s (\delta_ {I N T} ^ {(i, j)}) \\ \end{array}
$$

$$
Q (\boldsymbol {\gamma}) = \alpha_ {B} \cdot s i n (\delta_ {B}) + \sum_ {i = 1} ^ {N} \gamma_ {T _ {i}} \cdot \alpha_ {T _ {i}} \cdot s i n (\delta_ {T _ {i}})
$$

$$
+ \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {N} \gamma_ {T _ {i}} \gamma_ {T _ {j}} \cdot \alpha_ {I N T} ^ {(i, j)} \cdot s i n (\delta_ {I N T} ^ {(i, j)}) \tag {9}
$$

where $\left( \alpha _ { B } , \delta _ { B } \right)$ is the background reflection and $\gamma \quad =$ $\left\{ \gamma _ { T _ { 1 } } , \dots , \gamma _ { T _ { N } } \right\}$ ) =denotes the reflecting scale of the tags. Recall that the signal’s transition is usually caused by the flip of only one tag. So we should set a constraint on the reflecting scales of the tags: at any time, there exists at most one tag $T _ { i } ,$ whose reflecting scale satisfies $\gamma _ { T _ { i } } \in ( 0 , 1 )$ . Eq. (9) is a mathematical representation of DTG.

# B. Graph Fitting

In this section, we describe the global optimization process designed to estimate channel parameters. Specifically, let $\mathbf { S _ { o b s } }$ denote the IQ domain samples, where $\mathbf { S _ { o b s } } ( i ) = ( I ( i ) , Q ( i ) )$ is the location of sample $i . \ \mathbf { S _ { e s t } ( P ) }$ ( ) = ( ( ) ( ))denotes the constructed ( )DTG based on the IIA model (Eq. (9)). Fig. 9 gives an example of $\mathbf { S _ { o b s } }$ and $\mathbf { S _ { e s t } }$ in a three-tag collision case. To obtain the optimal channel estimations, we need to compute:

$$
\mathbf {P} ^ {*} = \arg \min _ {\mathbf {P}} \sum R (\mathbf {S} _ {\text { est }} (\mathbf {P}), \mathbf {S} _ {\text { obs }}). \tag {10}
$$

where $R ( \bullet )$ captures the overall distance between the gen-( )erated DTG and the observed samples, which quantifies the goodness-of-fitting of $\mathbf { S _ { e s t } }$ under a given set of channel parameters P. Clearly, $R ( \bullet )$ will be minimized when we get ( )the optimal channel estimation.

However, we may meet two problems: i) Since $\bf { S } _ { e s t } ( \bullet )$ is a ( )multivalued piecewise function, to quantify the overall distance between $\mathbf { S _ { o b s } }$ and $\mathbf { S _ { e s t } }$ we should first match each sample to the correct path. ii) Since the optimization problem is nonconvex, to avoid the local-optimal problem, we should find a good initialization in the searching process. The following will introduce our searching method which solves these problems.

1) Mapping a Sample to the Correct Path: We solve this problem by utilizing the result of parallel decoding [27], [28], [32], [34]. Recall that the parallel decoding method can obtain the state transition sequence (i.e., s t in Eq. 3) of each tag ( )from the parallel transmitted signals. Thus we can get the flip sequence of each tag (i.e., the time points when each tag flips its state). That is to say, i) the reader can accurately decode the ID/data in the packets of all the colliding tags; and ii) for each sample, since the corresponding state of each tag is known, the reader can always map this sample to the correct cluster or transition path [34]. As a result, the samples that belong to different transition paths are separated.

![](images/31d4c42525d111132aaef4801d9973285db2adb0c11318089c958aeb48a7f9d5.jpg)



![](images/ead4b915bcac36e4be3fb4dd9c9f091afccd1b18d0eccca66e864895b1a9bf46.jpg)



Fig. 10. Coarse-grained searching: (a) A three-tag case; (b) Phase and amplitude estimation.

2) Coarse-to-Fine Searching: Now, we focus on how to search for the optimal estimation of the channels. We design a coarse-to-fine searching method that first performs a coarse estimation of the channels, which provides a good initial point. Then we approach the optimal estimation by using the gradient-descent algorithm. Here we use the three-tag case in Fig. 10(a) as a example to introduce the searching process.

Coarse-grained estimation. The N tags’ channels can be initialized using the samples on the N interference-free paths (marked by the three red lines in Fig. 10(a)). Fig. 10(b) zooms in the signal samples on clusters LLL and HLL and shows how to estimate the phase and amplitude of Tag 1. Specifically, we just find the average locations of the samples on states LLL and HLL (marked by the two red points in Fig. 10(b)). Then the length and direction of the vector connecting this two points give the amplitude and phase of Tag 1’s signal.

Of course, such a coarse-grained estimation is erroneous due to the error in state positioning. However, since the noise level (i.e., radius of the signal clusters) is limited, the error range is limited, as shown in Fig. 10(b). So, it still provides a good initial point for the following gradient descent searching process. To illustrate it, Fig. 11(a) shows $R ( \mathbf { S _ { e s t } } , \mathbf { S _ { o b s } } )$ under different channel parameters of $T _ { 1 }$ ( ), given certain channels of $T _ { 2 } , \ T _ { 3 }$ , and the inter-tag interferences. As we can see, the coarse-grained channel estimation of $T _ { 1 }$ locates in the neighbourhood of the global minima.

The channels of the interference between each pair of tags can be initialized based on the signal trajectory that contains the signal of only these two tags (e.g., the three quadrilaterals that include the all-L state, as marked in Fig. 10 (a)). We call this method as quadrilateral fitting. We take the estimation of $\overline { { S _ { I N T } ^ { ( 1 , 2 ) } } } ( t )$ in Fig. 10(a) as an example to introduce this method. ( )Given the coarse-grained estimation of the channels of $T _ { 2 }$ and $T _ { 3 }$ , we can recover the theoretical trajectory of these two tags, which presents as a parallelogram, as shown by Fig. 10(a). The deviation of state $H H L$ gives a coarse-grained estimation of $S _ { I N T } ^ { ( 2 , 3 ) } ( t )$ . Fig. 11(b) shows the residual value under different ( )channel parameters of $T _ { 1 }$ .

![](images/e9806c63739592a150424ec044e0ae8e1eadf08d259cb23f91123b7f5f9a036a.jpg)



![](images/87cec88880c8c96ab174f6591621af971be84da5ad0fcd2edc5dd359e51edb50.jpg)



Fig. 11. Fine-grained searching: (a) R(•) under different phase and amplitude of $T _ { 1 } ;$ (b) R(•) under different phase and amplitude of the interference between $T _ { 1 }$ and $T _ { 2 }$ .

To fit the DTG to the signal samples, we should also estimate the channel parameters of the background reflection, which determine the displacement of the signal from the (0,0) position. This can be easily estimated by using the signals sampled when there is not any tag transmitting.

Fine-grained estimation. In this process, we first generate DTG based on the coarse-grained estimation results, and then repeatedly adjust the channel estimation according to the residual value, until the power of the residual converges.

# C. Reducing the Computational Complexity

In the graph fitting process, Fireworks needs to search across · N channel parameters and $\textstyle { \binom { 2 } { N } }$ interference parameters on 2all the n samples. The introduced computational complexity is calculated by $O ( 2 ( N + \binom { N } { 2 } ) \cdot n \cdot I )$ , where n is the number (2( + ) )of the samples and I is the number of searching iterations. In the design of Fireworks, we have $n \leq 1 0 0 0$ . Our experi-1000mental results in Section VI show that the maximum capacity of Fireworks is $N = 5$ . The required number of iterations I is = 5usually not more than 6. Considering that the sensing systems require online processing, we in this section try to reduce the computational complexity of Fireworks by reducing the number of parameters to be searched in the graph fitting process.

1) Reducing the Number of Channel Parameters: When estimating the channel parameters of a tag, if the tag’s SNR is high enough and the number of colliding tags is low, performing the coarse-grained estimation (as introduced in Sec. IV-B) may already produce satisfying result. So, for each tag, we can only include its channel parameters into the global graph fitting process as needed.

To achieve this, Fireworks configures a channel accuracy requirement $( p , e _ { \delta } , e _ { \alpha } )$ , where $p$ is the acceptable error rate. $e _ { \delta }$ and $e _ { \alpha }$ are the tolerable error range for phase and amplitude estimation. For example, a combination of $p \ = \ 3 \%$ , $e _ { \delta } ~ = ~ 0 . 0 5 ~ \ r a d .$ , and $e _ { \alpha } ~ = ~ 0 . 0 0 2$ = 3%requires the phase and = 0 05 = 0 002amplitude error to be respectively less than 0.05 rad. and 0.002 with a probability of at least . Recall that the error 97%in channel estimation is mainly caused by the error in state positioning. For each tag $T _ { i } , e _ { \delta }$ and $e _ { \alpha }$ can be transformed to the tolerance in state position error $( e _ { p } ^ { ( i ) } )$ as:

$$
e _ {\delta} \geq \arctan \left(\frac {2 \cdot e _ {p} ^ {(i)}}{\alpha_ {i}}\right)
$$

$$
e _ {\alpha} \geq 2 \cdot e _ {p} ^ {(i)} \tag {11}
$$

where $\alpha _ { i }$ is the amplitude of $T _ { i }$ . Based on (11), we get

$$
e _ {p} ^ {(i)} = \min \{\frac {\alpha \cdot \tan (e _ {\delta})}{2}, \frac {e _ {\alpha}}{2} \} \tag {12}
$$

Then, we set the tolerance in positioning error on I-axis and Q-axis (denoted b y e(i) a $e _ { I } ^ { ( i ) }$ nd $e _ { Q } ^ { ( i ) } )$ e(iQ as $\begin{array} { r } { e _ { I } ^ { ( i ) } = e _ { Q } ^ { ( i ) } = \frac { e _ { p } ^ { ( i ) } } { \sqrt { 2 } } } \end{array}$ e I e Q e(i)

To determine whether a tag $T _ { i } { } ^ { , } \mathrm { s }$ channel parameters need to be included in the graph fitting process, Fireworks employs T-distribution to quantify the possibility that the positioning error falls into the pre-defined tolerable range $( \mathrm { i } . \mathrm { e } . , e _ { I }$ and $e _ { Q } )$ . Specifically, suppose there are $n _ { c }$ signal samples in a cluster, a confidence interval $\begin{array} { r } { ( \tilde { I } - \frac { \tilde { \sigma } } { \sqrt { n _ { c } } } \bar { t } _ { \frac { p } { 2 } } , \tilde { I } + \frac { \tilde { \sigma } } { \sqrt { n _ { c } } } { t } _ { \frac { p } { 2 } } ) } \end{array}$ can be √nc constructed along the I-axis, where I and α are the average and the standard deviation of the $n _ { c }$ ˜samples, respectively. $t _ { \frac { p } { 2 } }$ can be determined from the t-distribution look-up table. The confidence interval along the Q-axis can be similarly defined. Combining Eq. (11) and the expression of the interval, we find that with more signal samples on each cluster and higher signal SNR of the tag (i.e., lower σ and larger α), the coarse-grained ˜estimation becomes more reliable.

So, for each tag $T _ { i } ,$ if we have $\begin{array} { r } { \frac { \tilde { \sigma _ { I } } } { \sqrt { n } } t _ { \frac { p } { 2 } } \le e _ { I } ^ { ( i ) } } \end{array}$ ≤ e I and $\begin{array} { r } { \frac { \tilde { \sigma _ { Q } } } { \sqrt { n } } t _ { \frac { p } { 2 } } \leq } \end{array}$ $e _ { Q } ^ { ( i ) }$ Q , which means performing coarse-grained estimation is sufficient to maintain satisfying result, we will not update its parameters in the subsequent graph fitting process.

2) Reducing the Number of Interference Parameters: Recall that inter-tag interference occurs only between nearby tags. In a N -tag-collision case, it is unlikely that all the $\binom { 2 } { N }$ pairs of tags are closely located. Therefore, in the coarse-grained estimation process, if the estimated amplitude of the intertag interference $\overrightarrow { S _ { I N T } ^ { ( i , j ) } } ( t )$ is lower than a predefined threshold, ( )we consider the corresponding tags $T _ { i }$ and $T _ { j }$ as a noninterfering pair and directly set the interference parameters as zero. This further reduces the number of parameters to be estimated.

Algorithm 1 presents the complete workflow of Fireworks’s channel estimation process. After reducing the number of parameters to be included in the graph fitting process, the computation complexity of Fireworks is further reduced. Our experiment results show that, when implemented on an USRP N210 connected to a PC with 3.6GHz CPU and 16G memory, Fireworks takes 610∼790μs to resolve the channels of 5 tags.

# V. INTEGRATION WITH COMMERCIAL MAC PROTOCOL

We may meet a problem in applying Fireworks in practical RFID systems – commercial MAC-layer protocols are mostly designed to avoid collision, which limits the performance gain of Fireworks. For example, in standard EPC C1G2 protocol, each tag contends for the channel by first sending a random RN16 packet at a randomly selected time slot within a frame. If the RN16 packet is successfully decoded by the reader, the reader ACKs the RN16 and the corresponding tag responds its EPC (tag ID). In an M -tag collision case, although Fireworks can successfully get the channel parameters of all the M tags from the collided RN16 signal, it can only get the EPC of one tag. It cannot map the other M −  channels to the corresponding M −  tags. As a result, the throughput reported in Sec. II-A will be reduced to:

Algorithm 1 Coarse-to-Fine Searching   
Require:
Locations of the n samples: $\mathbf{S}_{\mathrm{obs}} = \{(I_i, Q_i) | 1 \leq i \leq n\}$ ;
The accuracy requirement: $\mathbf{Re} = (p, e_{\delta}, e_{\alpha})$ ;
1: $P \leftarrow \text{CoarseEstimation}(S_{\text{obs}}) \quad \triangleright \text{Initialize } P$ 2: $[\mathbf{P}_{\text{coarse}}, \mathbf{P}_{\text{fine}}] \leftarrow \text{ReduceParameters}(\mathbf{P}, \mathbf{Re})$ 3: $S_{\text{est}} \leftarrow \text{IIAModel}(\mathbf{P})$ 4: $\tilde{R} \leftarrow \text{OverallDistance}(S_{\text{obs}}, S_{\text{est}}) \quad \triangleright \text{Goodness-of-fitting}$ 5: while $\tilde{R} > Th_{R}$ do
6: $P_{fine} = P_{fine} - \eta \nabla R(P_{fine}) \quad \triangleright \text{Gradient}$ 7: $S_{\text{est}} \leftarrow \text{IIAModel}(P_{\text{coarse}}, P_{\text{fine}})$ 8: $\tilde{R} \leftarrow \text{OverallDistance}(S_{\text{obs}}, S_{\text{est}})$ 9: end while
10: return $[P_{coarse}, P_{fine}]$

$$
T h (M, N _ {a l l}) = \sum_ {N = 1} ^ {M} \binom {N _ {a l l}} {N} \left(\frac {1}{K}\right) ^ {N} \left(1 - \frac {1}{K}\right) ^ {N _ {a l l} - N} \tag {13}
$$

By comparing Eq. (13) and (1), we find that the performance gain of Fireworks is reduced when working with the collision avoidance protocol. A naive solution to this problem is to remove the RN16 process and let the tags directly send their EPCs. However, such a modified protocol cannot support standardized commercial tags in widely deployed RFID systems.

To solve this problem, we wonder whether EPC is the only identity of a tag? Existing studies [18], [35], [36] show that a tag’s PHY-layer feature can also be used as an identity. Inspired by those studies, we propose to use tags’ frequency errors and channel parameters, two features that can be extracted from the collided RN16 signal, as a fingerprint to distinguish different tags. With such a PHY-layer identity, we can identify the tags without their EPC ID.

Frequency error. A tag’s clock exhibits high frequency error (denoted as ∂), resulting differences in tags’ clock frequencies [27], [28], [35]. Such a difference further results in the difference in tags’ bit durations, i.e., the time between two bit-boundary flips of a tag’s signal. Considering that Fireworks is able to trace the flippings of each tag, it can calculate the bit duration of each tag based on the collided RN16 signal.

Due to the limited ADC sampling rate, a reader can only obtain a coarse-grained estimation of a tag’s frequency error, which has limited discernibility. The study in [35] shows that using only the frequency error achieves an identification accuracy of only . So we propose to combine tags’ frequency 71%error and channel parameters for more robust identification.

Channel parameters. Due to the difference in tags’ locations, orientations, and other physical states, different tags have different channel parameters. So, we can also use channel parameters as a PHY-layer feature to identify the colliding tags. We face two problems here. First, different tags may have similar channel parameters. Second, a tag’s channel parameters, which change with the mobility of the tag, cannot serve as a stable tag identity.

To solve the first problem, we leverage the fact that most sensing applications use multiple antennas. So, for each tag $T _ { i }$ , $M _ { A }$ tennas, we can get . It is unlikely tha $M _ { A }$ channel estimateso tags have similar $\{ \mathbf { P _ { T _ { i } } ^ { ( 1 ) } } , . . . , \mathbf { P _ { T _ { i } } ^ { ( \tilde { \mathbf { M } } _ { A } ) } } \}$ channel estimates on all the $M _ { A }$ antennas. To verify this assumption, we perform an experiment with 50 tags, which are located randomly in a 1.5m×2m area. We use $M _ { A } = 3$ = 3antennas to collect the phase readings of the tags. If the difference between two phase readings is lower than 0.06 rad. (the error variance of phase estimation, as shown in Section VI), we consider these two phases as identical. The experimental result tells that we cannot find two tags which have identical phase readings across all the three antennas. So combining the channel estimates from multiple channels gives a robust fingerprint to identify each tag.

To solve the second problem, we find that due to the limited moving speed of a tag, the change in a tag’s channel parameters between two queries is also limited. So, the reader can map a new channel estimate to the corresponding tag based on the records of the tags’ channel parameters. In the case where a tag goes out of the reading range and re-appears, the reader cannot directly identify this tag based on its channel parameters. In this case, Fireworks will consider it as a new tag and re-constructs its fingerprint.

Specifically, in our PHY-layer tag identification method, the reader forms the fingerprint $\mathbf { F } = \{ \partial , \mathbf { P _ { T } ^ { ( 1 ) } } , \dotsc , \mathbf { P _ { T } ^ { ( M _ { A } ) } } \}$ . =The fingerprints of all the tags form a fingerprint table, named F T able. In the runtime, once the reader extracts a fingerprint F from the collided RN $^ { 1 6 , }$ it measures the distance between F and all the fingerprints in F T able. If all the distances are larger than a threshold, we consider the corresponding tag as a new one. Then we ACK its RN16 to get its EPC and add F to F T able. Otherwise, the tag is identified as $T _ { i }$ if $\mathbf { F _ { i } }$ has the smallest distance with F. To capture the change in the tags’ channel parameters, the reader then updates $\mathbf { F _ { i } }$ as $\mathbf { F _ { i } } = \mathbf { F }$ .

# VI. EVALUATION

# A. Implementation and Experiment Settings

The reader side of Fireworks is built based on the USRP N210 software defined radio (SDR) with UBX RF daughterboards and 900 MHz antennas. The ADC sampling rate of the reader is set at 20MHz. The TX and RX gain of the antennas are set at 10dBi. The TX power of the reader is set at 20dBm, which is much lower than what a commercial reader can support (i.e., 30dBm). The reason we do not use a higher TX power is that an USRP based reader do not support self-interference cancellation. A high TX power will lead to poor SNR of the received signal. Due to the low TX power, the transmission distance between the tags and the reader is limited to 2 meters in our experiment.

The tag side is implemented on programmable WISP tags in our experiment. In the experiments, we use WISP tags rather than commercial tags, because WISP is more suitable for evaluating the performance of Fireworks. Recall that the main target of Fireworks is to extract the channel parameters of each tag from the collided signal, it is necessary and desirable to evaluate the accuracy of the recovered channel parameters through the experiments under different settings. Using WISP tags makes it feasible to control the parallelism and to obtain the ground truth of channel parameters of each tag. If we use commercial tags, the communication between the reader and the tags must follow the EPC protocol. In this case, we need to recover the channel parameters from the collided RN16 signal, as we have discussed in Section V. The problem here is although we can recover the channels, it is non-trivial to map them to the corresponding tags, without the knowledge of their EPC IDs. In other words, we cannot map the estimation results to the ground truth to evaluate the errors. The method proposed in Section V can solve this problem by using a tag’s PHY-layer fingerprint as its ID, however, with additional errors. Therefore, although Firework can be applied with commercial tags, we choose WISP as the hardware platform in the experiments.

# B. Channel Estimation Accuracy

In this experiment, we evaluate the accuracy of channel estimation under different influencing factors. Specifically, we adjust the number of tags, the tag-reader distance D (which leads to different signal SNR), the tag spacing $d ,$ and the bitrate of the tags to evaluate how these factors affect the performance of Fireworks. By default, we have D cm = 50(the corresponding signal SNR is about 15dB) and d cm.

= 10We treat the channel obtained in the non-collision TDMA scenario as the real value. Specifically, for each setting, we conduct experiments under both collision scenario and TDMA scenario. The estimation error is calculated as the difference between the values obtained under these two scenarios.

We compare Fireworks with a baseline method which first uses FlipTracer [28], a state-of-the-art parallel decoding method, to identify the combined state of each signal cluster, and then extracts the channel of each tag based on the centers (i.e., the density peaks) of the clusters (we term this baseline method as FlipTracer in the following of this article.)

Performance under different numbers of tags. In this experiment, we let 2∼5 tags transmit simultaneously. The estimation error under different number of tags are shown in Fig. 12(a). We have the following findings:

• With more tags, the mean error of both the two methods increase due to the aggravated interference among tags. For example, the phase error of FlipTracer increases from 0.3∼0.7 rad. to 0.6∼1.4 rad. when the number of tags increases from 2 to 5. Compared with FlipTracer, Fireworks does not suffer obvious performance degradation. Specifically, in the 5-tag case, the mean error of phase estimation is 0.135 rad., which is almost one magnitude lower than that of FlipTracer. Its mean error of phase and amplitude estimation across all the parallelism levels are 0.054 rad. and 0.0029, respectively. Such a high accuracy is achieved due to Fireworks’s ability to compensate the inter-tag interference.

• For FlipTracer, the tag number affects not only the mean error of channel estimation, but also the error variation.

![](images/df1248db0c8f8a48ea5eadd348383f193d27bbee7cc6ebf61b8cea0c24dbb42c.jpg)



![](images/cb8cc2dd8f1bf0a96ebd8bd2e4a6f93425b1f334790d20f7ad1dc109ecf3f373.jpg)  
(a)

![](images/7226637cc6ba957698cef7b563c50a145fd238694fc63ada7d768ccf2587c0bb.jpg)



![](images/4c944fcbd8c1de6825c037f05c2cc2bccc38c7c0b39b4f18fa219acac79b5937.jpg)



(b)

![](images/4ca5cd69f97326021115702a7160387a6ce2fd8a59dbdc295c16bcabc5d33c42.jpg)



![](images/8c3a4632629cb4bb213ccafadff0452411a9f2eb3e794bfe1b4276eed3494234.jpg)



（c）

![](images/d2a6145e109c903d916ebf6e41049de152187b661fda52635cc1763c21c9b7db.jpg)

![](images/5e80375569ff1c44a9e6aa70afd5d2e6b0fa3326c4b50c513924c96d4d9d4e30.jpg)

Fig. 12. Channel estimation error: (a) channel estimation error v.s. tag number; (b) channel estimation error v.s. SNR; (c) impact of d; (d) impact of bitrate.   
![](images/466ad6d38657f7d024d135a88cb98788ade361b75222dfc2f52aaf6bdbbcb244.jpg)



(a)

![](images/ec25854fce8606d6f93dc55f1014bd0c1921dbb0a6c3646b2264f9be549be6a1.jpg)



(b)

![](images/3761cacf4fc36ac5d592fad6eb0bfc37e1ee8c1d7df1b77a26712177ff432674.jpg)



(c)

![](images/d80bb3d06d9e16e06f0e84679f703c68c5153c77c69f14bfb00d627f2be4de12.jpg)



(d)

![](images/a47390776f17e19d450e5155ecf9fb18888c57c707c9889480e516ba1240a981.jpg)



(e)   
Fig. 13. Tracking accuracy: (a) recovered trajectory; (b) tracking error with one tag; (c) tracking error with two tags; (d) tracking error with three tags; (e) tracking error with four tags.

This is due to the increased flipping frequency of the signal when more tags transmit simultaneously. Fireworks is almost not affected by the increased tag number since it extracts the channels directly based on the trajectory of the signal.

Performance under different signal SNR. In this experiment, we use three tags. The tag-reader distance changes from 30cm to 100cm, and the corresponding signal SNR decreases from 15dB to 5dB. The performance under different SNRs are shown in Fig. 12(b). This two figures tell that:

A surprising observation is that the mean error of FlipTracer slightly decreases with the decreased SNR. The phase error range increases from 0.3∼0.6 rad. to 0.3∼1.2 rad. when the SNR decreases from 20dB to 5dB. This is indeed due to the aggravated inter-tag interference when the signal power is high. In contract, Fireworks is not sensitive to the SNR due to its ability to compensate the inter-tag interference.   
For both the two methods, the error variance of the phase estimation increases with the decreased signal SNR, because the low SNR amplifies the phase error.

Due to the page limitation, we do not show Fireworks’s performance in tackling the near-far problem (i.e., when there is a significant difference between tags’ signal SNRs). We leave this in the future works.

Performance under different inter-tag distances. The inter-tag distance d is an important factor which determines the intensity of inter-tag interference. In this experiment, we use 3 tags and change d from 3cm to 15cm. The experiment result is shown in Fig. 12(c). As expected, the performance of Flip-Tracer degrades significantly with the decreased d. Fireworks consistently outperforms FlipTracer at all distances. Specifically, when the inter-tag distance is only 3cm, Fireworks incurs only a 0.03 rad. median error in phase estimation and a 0.005 median error in amplitude estimation.

Performance under different bitrates. Tags’ bitrate is also an important factor which determines how fast the signal moves on the IQ domain. In this experiment, we observe how different bitrates of the tags affect the performance of Fireworks and FlipTracer. Again, we use three tags and the bitrate of the tags change from 100Kbps to 500Kbps. Since the WISP platforms currently support only a 256Kbps bitrate, we conduct simulations to see the performance of the two methods with 500 Kbps bitrate. The result is shown in Fig. 12(d). We find that for both the two methods, the bitrate affects the error variance of channel estimation. Compared with FlipTracer, Fireworks is more robust to the high bitrate because it is designed to estimate the channels of the tags directly from the moving trajectory of the collided signal.

# C. Sensing Accuracy

In this section, we use target tracking as an example to evaluate how Fireworks improves the performance of the backscatter-based sensing applications. In the experiment, we let the tags move together along different tracks. Three antennas are deployed around the three corners of the $1 0 0 \times 1 5 0 ~ c m ^ { 2 }$ surveillance region. To avoid the interference 100 150among them, we set them to different frequencies.

We compare the performance of two tracking methods:

Tagoram. Tagoram is a state-of-the-art tracking method which reconstructs the moving trajectory of a tag based on the phase of its signal. In Tagoram, the tags transmit sequentially based on the conventional EPC protocol.   
Tagoram Fireworks. In this method, the tags transmit +simultaneously, then the reader uses Fireworks to recover

the channel parameters of all the tags. The recovered channels are then used by Tagoram for tracking.

Trajectory accuracy. In the experiment, we let three tags move simultaneously along trajectories with different shapes (a line trajectory and a circle trajectory) and of different letters, as shown in Fig. 13. The movement along each trajectory is completed within 1.5 seconds. Fig. 13 shows an example of the recovered trajectories. The trajectories in gray are the ground truths, while the blue and red ones are the estimates of Tagoram and Tagoram Fireworks, respectively. +As we can see, Tagoram Fireworks accurately reconstructs +not only the relatively straight segments but also the curved strokes, while the trajectories of Tagoram deviate significantly from the ground truths, especially for the trajectories with higher complexity. This is due to the significantly reduced sampling rate of Tagoram when three tags transmit simultaneously.

Performance under different numbers of tags. In this experiment, we change the number of tags from 1 to 4. Under each tag number, we let the tags move along the trajectories shown in Fig. 13 for 20 times. The CDF of the trajectory errors for Tagoram and Tagoram Fireworks.

+The figure shows that Fireworks Tagoram significantly out-+performs Tagoram especially with more tags. This is owning to the high sampling rate of Fireworks. Specifically, when there is only one tag, the sampling rate of Tagoram is about 57Hz. The Fireworks Tagoram only slightly outperforms Tagoram. +When there are two tags, the sampling rate of Tagoram decreases to 39Hz. As a result, the median error of Tagoram increases to 1.7cm and the 90th percentile increases to 2.6cm. For Fireworks Tagoram, its median error and 90th +percentile are 1cm and 1.4cm, outperforming Tagoram by almost 2×.

When there are four tags, the median error of Tagoram +Fireworks is 1.3cm and the 90th percentile is 1.5cm. No significant performance degradation is observed compared with the two-tag case. While Tagoram’s median error increases to 5.1cm and the 90th percentile increases to 6cm. Fireworks improves the performance of Tagoram by 4× in this case.

# Performance for trajectories with different complexities.

The complexity of the trajectory is also an important factor that affects the performance of the tracking systems. First, since the movement along all the trajectories are completed within the same time length (1.5 second), different complexities of the trajectories means different moving speeds. In addition, trajectories that have more curved strokes or sharp corners (e.g., letter ‘M’) usually lead to higher tracking difficulty. So we test the performance of Fireworks using three groups of trajectories with different complexities. The CDF of the trajectory errors of Tagoram and Tagoram Fireworks for +different groups of trajectories are shown in Fig. 14.

By comparing the three figures, we find that the improvement brought by Fireworks is more obvious with complex trajectory. Tagoram’s median tracing accuracy for the trajectories with high, medium, and low complexities are 1.1cm, 2.5cm, and 3.2cm, respectively. After combined with Fireworks, the accuracy increased to 0.7cm, 1.0cm, and 1.2cm, bringing 1.5×, 2.5×, and 2.7× performance gain, respectively.

![](images/838b693b5b4dcfb48c4146be46fb4bb301bd0b59d60a37e3001a5d6eec3e90d0.jpg)  
Fig. 14. Tracking error of trajectories with different complexities.

# VII. RELATED WORK

Many works have been proposed to separate the parallel transmitted signal. A typical example is Successive Interference Cancelation (SIC) [26]. However, SIC requires significant difference in the SNR of the colliding signals. Hence it only applies to limited scenarios. Methods like ZigZag [37] and mZig [38] decode the collided signal base on the assumption that the collision is a linear addition result of the colliding signals, which is not the case of backscatter transmission.

Recently, many methods are designed to decode the parallel transmitted backscatter signals [27], [28], [32], [34], [39]–[45]. Specifically, LF-Backscatter [32], BiGroup [27], and FlipTracer [28] can decode the collided signals by exploiting the spatial and/or temporal characteristics of signals’ combined states. The latest proposal Hubble [34] further improves the practical usability of the parallel backscatter technology, achieving a 5-tag parallelism under relatively weak SNR (signal to noise ratio). However, all of the above methods are just able to recover the coarse-grained signal state of each tag, but cannot obtain the fine-grained channel parameters.

Compared with parallel decoding methods, Fireworks deepens the level of signal processing and extracts the channels of backscattered signals. Compared with its previous version introduced in [46], Fireworks in this article is more lightweight and is compatible with the commercial MAC protocol, which makes it applicable to many existing RFID sensing systems.

# VIII. CONCLUSION

This article studies the backscatter-based sensing from a new angle, namely channel estimation of parallel backscattered signals. With an eye on the increasingly dense deployment of backscatter-based IoT devices, how to make them work together as efficiently as possible is clearly a significant issue. Our proposal Fireworks is the first approach that enables channel estimation of parallel backscattered signals. Fireworks makes accurate channel estimation and indeed enhances the efficiency and accuracy of backscatterbased sensing applications. In our future work, we plan to explore the multi-antenna approach on the reader, which potentially further increases the capacity of parallel channel estimation.

# REFERENCES

[1] E. Ilie-Zudor, Z. Kemény, F. van Blommestein, L. Monostori, and A. van der Meulen, “A survey of applications and requirements of unique identification systems and RFID techniques,” Comput. Ind., vol. 62, no. 3, pp. 227–252, Apr. 2011.   
[2] Y. Ma, N. Selby, and F. Adib, “Drone relays for battery-free networks,” in Proc. SigComm, Aug. 2017, pp. 335–347.   
[3] G. Wang et al., “Towards replay-resilient RFID authentication,” in Proc. MobiCom, Oct. 2018, pp. 385–399.   
[4] Z. Luo, Q. Zhang, Y. Ma, M. Singh, and F. Adib, “3D backscatter localization for fine-grained robotics,” in Proc. NSDI, 2019, pp. 765–782.   
[5] B. Kellogg, V. Talla, and S. Gollakota, “Bringing gesture recognition to all devices,” in Proc. NSDI, 2014, pp. 303–316.   
[6] T. Wei and X. Zhang, “Gyro in the air: Tracking 3D orientation of batteryless Internet-of-Things,” in Proc. MobiCom, 2016, pp. 55–68.   
[7] S. Pradhan, E. Chai, K. Sundaresan, L. Qiu, M. A. Khojastepour, and S. Rangarajan, “RIO: A pervasive RFID-based touch gesture interface,” in Proc. MobiCom, Oct. 2017, pp. 261–274.   
[8] S. Pradhan, E. Chai, K. Sundaresan, S. Rangarajan, and L. Qiu, “Konark: A RFID based system for enhancing in-store shopping experience,” in Proc. MobiSys, 2017, pp. 19–24.   
[9] W. Jiang et al., “Towards environment independent device free human activity recognition,” in Proc. MobiCom, Oct. 2018, pp. 289–304.   
[10] J. Wang, D. Vasisht, and D. Katabi, “RF-IDraw: Virtual touch screen in the air using RF signals,” in Proc. SIGCOMM, Aug. 2014, pp. 235–246.   
[11] L. Yang, Y. Li, Q. Lin, X.-Y. Li, and Y. Liu, “Making sense of mechanical vibration period with sub-millisecond accuracy using backscatter signals,” in Proc. MobiCom, Oct. 2016, pp. 16–28.   
[12] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu, “Tagoram: Real-time tracking of mobile RFID tags to high precision using COTS devices,” in Proc. MobiCom, Sep. 2014, pp. 237–248.   
[13] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Relative localization of RFID tags using spatial-temporal phase profiling,” in Proc. NSDI, 2015, pp. 251–263.   
[14] C. Jiang, Y. He, X. Zheng, and Y. Liu, “Orientation-aware RFID tracking with centimeter-level accuracy,” in Proc. IPSN, Apr. 2018, pp. 290–301.   
[15] C. Jiang, Y. He, S. Yang, J. Guo, and Y. Liu, “3D-OmniTrack: 3D tracking with COTS RFID systems,” in Proc. IPSN, Apr. 2019, pp. 25–36.   
[16] J. Wang and D. Katabi, “Dude, where’s my card?: RFID positioning that works with multipath and non-line of sight,” in Proc. SIGCOMM, Aug. 2013, pp. 51–62.   
[17] S. Manzari, C. Occhiuzzi, S. Nawale, A. Catini, C. Di Natale, and G. Marrocco, “Polymer-doped UHF RFID tag for wireless-sensing of humidity,” in Proc. RFID, Apr. 2012, pp. 124–129.   
[18] C. Wang, L. Xie, W. Wang, T. Xue, and S. Lu, “Moving tag detection via physical layer analysis for large-scale RFID systems,” in Proc. INFOCOM, Apr. 2016, pp. 1–9.   
[19] J. Wang, J. Xiong, X. Chen, H. Jiang, R. K. Balan, and D. Fang, “TagScan: Simultaneous target imaging and material identification with commodity RFID devices,” in Proc. MobiCom, Oct. 2017, pp. 288–300.   
[20] A. Dhekne, M. Gowda, Y. Zhao, H. Hassanieh, and R. R. Choudhury, “LiquID: A wireless liquid identifier,” in Proc. MobiSys, Jun. 2018, pp. 442–454.   
[21] N. Anand, R. E. Guerra, and E. W. Knightly, “The case for UHF-band MU-MIMO,” in Proc. MobiCom, Sep. 2014, pp. 29–40.   
[22] H. Rahul, S. Kumar, and D. Katabi, “MegaMIMO: Scaling wireless capacity with user demands,” in Proc. SIGCOMM, 2012, p. 1.   
[23] S. Sur, I. Pefkianakis, X. Zhang, and K.-H. Kim, “Practical MU-MIMO user selection on 802.11ac commodity networks,” in Proc. MobiCom, Oct. 2016, pp. 122–134.   
[24] W. Zhou, T. Das, L. Chen, K. Srinivasan, and P. Sinha, “BASIC: Backbone-assisted successive interference cancellation,” in Proc. Mobi-Com, Oct. 2016, pp. 149–161.   
[25] K. C.-J. Lin, S. Gollakota, and D. Katabi, “Random access heterogeneous MIMO networks,” in Proc. SIGCOMM, 2011, pp. 146–157.   
[26] D. Halperin, T. Anderson, and D. Wetherall, “Taking the sting out of carrier sense: Interference cancellation for wireless LANs,” in Proc. MobiCom, 2008, pp. 339–350.   
[27] J. Ou, M. Li, and Y. Zheng, “Come and be served: Parallel decoding for cots RFID tags,” in Proc. MobiCom, 2015, pp. 500–511.   
[28] M. Jin, Y. He, X. Meng, Y. Zheng, D. Fang, and X. Chen, “FlipTracer: Practical parallel decoding for backscatter communication,” in Proc. MobiCom, Oct. 2017, pp. 275–287.   
[29] Q. Lin, L. Yang, H. Jia, C. Duan, and Y. Liu, “Revisiting reading rate with mobility: Rate-adaptive reading in COTS RFID systems,” in Proc. CoNEXT, Nov. 2017, pp. 199–211.

[30] L. Shangguan, Z. Zhou, and K. Jamieson, “Enabling gesture-based interactions with objects,” in Proc. MobiSys, Jun. 2017, pp. 239–251.   
[31] L. Xie, C. Wang, A. X. Liu, J. Sun, and S. Lu, “Multi-touch in the air: Concurrent micromovement recognition using RF signals,” IEEE/ACM Trans. Netw., vol. 26, no. 1, pp. 231–244, Feb. 2018.   
[32] P. Hu, P. Zhang, and D. Ganesan, “Laissez-faire: Fully asymmetric backscatter communication,” in Proc. SIGCOMM, Aug. 2015, pp. 255–267.   
[33] D. Tse and P. Viswanath, Fundamentals of Wireless Communication. Cambridge, U.K.: Cambridge Univ. Press, 2005.   
[34] M. Jin, Y. He, X. Meng, D. Fang, and X. Chen, “Parallel backscatter in the wild: When burstiness and randomness play with you,” in Proc. MobiCom, 2018, pp. 471–485.   
[35] D. Zanetti, B. Danev, and S. Capkun, “Physical-layer identification of UHF RFID tags,” in Proc. MobiCom, 2010, pp. 353–364.   
[36] D. Ma, C. Qian, W. Li, J. Han, and J. Zhao, “GenePrint: Generic and accurate physical-layer identification for UHF RFID tags,” in Proc. ICNP, Oct. 2013, pp. 1–10.   
[37] S. Gollakota and D. Katabi, “Zigzag decoding: Combating hidden terminals in wireless networks,” in Proc. SIGCOMM, 2008, pp. 159–170.   
[38] L. Kong and X. Liu, “mZig: Enabling multi-packet reception in ZigBee,” in Proc. MobiCom, 2015, pp. 552–565.   
[39] M. Hessar, A. Najafi, and S. Gollakota, “Netscatter: Enabling large-scale backscatter networks,” in Proc. NSDI, 2019, pp. 271–284.   
[40] O. Abari, D. Vasisht, D. Katabi, and A. Chandrakasan, “Caraoke: An e-toll transponder network for smart cities,” in Proc. MobiCom, Aug. 2015, pp. 297–310.   
[41] J. Wang, H. Hassanieh, D. Katabi, and P. Indyk, “Efficient and reliable low-power backscatter networks,” in Proc. SIGCOMM, 2012, pp. 61–72.   
[42] D. Shen, G. Woo, D. P. Reed, A. B. Lippman, and J. Wang, “Efficient and reliable low-power backscatter networks,” in Proc. RFID, 2009, pp. 61–72.   
[43] C. Angerer, R. Langwieser, and M. Rupp, “RFID reader receivers for physical layer collision recovery,” IEEE Trans. Commun., vol. 58, no. 12, pp. 3526–3537, Dec. 2010.   
[44] A. Bletsas, J. Kimionis, A. G. Dimitriou, and G. N. Karystinos, “Singleantenna coherent detection of collided FM0 RFID signals,” IEEE Trans. Commun., vol. 60, no. 3, pp. 756–766, Mar. 2012.   
[45] R. S. Khasgiwale, R. U. Adyanthaya, and D. W. Engels, “Extracting information from tag collisions,” in Proc. RFID, Apr. 2009, pp. 131–138.   
[46] M. Jin, Y. He, C. Jiang, and Y. Liu, “Fireworks: Channel estimation of parallel backscattered signals,” in Proc. IPSN, Apr. 2020, pp. 85–96.

![](images/62e8e0284002be0e99e8c286e58672326c271ea81d6277ba979dad968a3b0e69.jpg)



Meng Jin (Member, IEEE) received the B.S., M.S., and Ph.D. degrees in computer science from Northwest University, Xi’an, China, in 2012, 2015, and 2018, respectively. She was a Post-Doctoral Researcher with the School of Software and BNRist, Tsinghua University. She is currently an Assistant Professor with the School of Electronic Information and Electrical Engineering, Shanghai Jiao Tong University. Her current research interests include backscatter communication, wireless network co-existence at 2.4 GHz, mobile sensing, and clock synchronization. She is a member of the ACM.

![](images/4c7f6dee9db6a53efea2839f8efe9d32a3c8d8e861c55120bf5050ee7fee6b3a.jpg)



Yuan He (Senior Member, IEEE) received the B.E. degree from the University of Science and Technology of China, the M.E. degree from the Institute of Software, Chinese Academy of Sciences, and the Ph.D. degree from The Hong Kong University of Science and Technology. He is currently an Associate Professor with the School of Software and BNRist, Tsinghua University. His research interests include Internet of Things, wireless and sensor networks, and mobile and ubiquitous computing. He is a member of the ACM.

![](images/f2714fb4e099f0c0d49b4a9b50658cd18e3e139c2efe7bbf6a9a49834381e6cc.jpg)



Chengkun Jiang (Student Member, IEEE) is currently pursuing the Ph.D. degree with the School of Software, Tsinghua University under the supervision of Prof. Yuan He and Prof. Yunhao Liu. He is a Student Member of the ACM.

![](images/af1d362d549f5087d6a6aa90195bc9d879374129d3d7bffff785e561719e386f.jpg)



Yunhao Liu (Fellow, IEEE) received the B.S. degree from the Automation Department, Tsinghua University, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, USA. He is currently a MSU Foundation Professor and a Chairperson of the Department of Computer Science and Engineering, Michigan State University, and holds Chang Jiang Chair Professorship with Tsinghua University. His research interests include sensor network and pervasive computing, peer-to-peer computing, the IoT, and supply chain.

He is a fellow of the ACM. He currently serves as the Editor-in-Chief for ACM Transactions on Sensor Networks and is an ACM Distinguished Speaker.