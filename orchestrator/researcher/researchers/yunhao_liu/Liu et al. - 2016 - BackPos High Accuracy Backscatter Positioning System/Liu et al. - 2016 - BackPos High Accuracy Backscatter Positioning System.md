# BackPos: High Accuracy Backscatter Positioning System

Tianci Liu, Student Member, IEEE, Yunhao Liu, Fellow, IEEE, Lei Yang, Member, IEEE, Yi Guo, Student Member, IEEE, Cheng Wang, Member, IEEE

Abstract—Radio Frequency IDentification(RFID) technology has been widely adopted in a variety of applications from logistics to access control. Many applications gain benefits from knowing the exact position of an RFID-tagged object. Existing localization algorithms in wireless network, however, can hardly be directly employed due to tag’s limited capabilities in terms of energy and memory. In this paper, we propose BackPos, a fine-grained backscatter positioning technique using the Commercial Off-The-Shelf(COTS) RFID products with detected phases. Our studies show that the phase is a stable indicator highly related to tag’s position and preserved over frequency or tag orientation, but challenged by its periodicity and tag’s diversity. We attempt to infer the distance differences from phases detected by antennas under triangle constraint. Further, hyperbolic positioning using the distance differences is employed to shrink the tag’s candidate positions until finding out the real one. In combination with interrogation zone, we finally relax the triangle constraint and allow arbitrary deployment of antennas by sacrificing the feasible region. We implement a prototype of BackPos with COTS RFID products and evaluate this design in various scenarios. The results show that BackPos achieves the mean accuracy of 12.8cm with variance of 3.8cm.

Index Terms—RFID, hyperbolic positioning, BackPos, feasible region

# 1 INTRODUCTION

R ADIO Frequency IDentification (RFID) systems havebeen widely deployed in recent years. It is no exag- been widely deployed in recent years.It is no exaggeration to say that we are almost surrounded by RFID tags in daily life. These tags wear different skins, such as credit cards, ID cards, car keys, pass cards etc., and play a key role in assets management, object tracking, access control and logistics. Typically, a RFID system consists of one reader and many tags. Most of them utilize the backscatter radio link for communications. In such link, the tag does not need equipment of battery but modulates their information on the backscattered signals emitted from a reader. A backscatter tag nearby reader changes the impedance match on its own antenna to modulate the reader’s signal, in order to convey a message of zeros and ones back to the reader. Many applications gain the benefits from knowing the exact location of an RFID-tagged object. For example, we can quickly check whether the books on certain shelves are out of order, find out the lost credit card with no need of guessing, or pay for the groceries of the person behind.

The traditional localization algorithms in wireless networks are limited for RFID because they have very limited capabilities in terms of energy and memory. RFID positioning, one of the most important fundamental topics in RFID area, has received a lot of attentions [1]–[6]. These

• Tianci Liu, Yunhao Liu and Lei Yang are with the School of Software, Tsinghua University, Beijing, China. Emails:tian@tagsys.org, yunhao@greenorbs.com, young@tagsys.org   
• Yi Guo is with Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong. Email: yi@tagsys.org   
• Cheng Wang is with Tongji University, Shanghai, China

work can be classified into two groups. (1) Received Signal Strength (RSS) based methods [1]–[4]. These work employ the RSS as an indicator for tag’s position. They deploy reference tags with known positions in advance. When applying, k reference tags whose RSS are the most similar to that of target tag are chosen for estimating the target’s position. However, their accuracy is challenged because the RSS is not a reliable indicator being vulnerable to fluctuation as environment changes over time. Moreover, the tag’s orientation is another killer factor on RSS, which directly influences its energy absorption from reader. (2) AoA based methods [5], [6]. AoA determines the direction by measuring the Time Difference of Arrival (TDOA) at individual elements of the array. Generally this TDOA measurement is made by measuring the difference in received phase at each element in the antenna array in RFID systems. These methods need to put a strict constraint on the antennas’ spacing (6 λ/2) to convert phase values into determined phase differences, whereas commercial reader’s directional antennas are too large (25 × 25cm2) to meet.

In this paper, we introduce a fine-grained backscatter positioning technique, called BackPos, without need of reference tags. We conduct a serial of empirical studies to show that the phase exhibits a reliable indicator highly related to tag’s position, and preserved over frequency or tag orientation. More important, the phase reveals a stable linear relation to the distance within half a wavelength. With combination of these characteristics, we attempt to position a target tag using the phase. However, this idea is challenged by two factors: (i) Each tag has a small but different unknown initial phase rotation $\theta _ { T a g } ,$ , related to its unique antennas on the board, which contributes to the reader’s measured phase θ. We should carefully tackle the measurement error coming from this diversity. (ii) The phase is periodic such that the linear relation with distance behaves effective within half a wavelength only, increasing the position uncertainty. We should find a way to eliminate this uncertainty.

Our basic idea is to infer the distance difference $\Delta d$ from a target tag to two antennas using the phase difference $\Delta \theta .$ The ambiguity coming from phase periodicity can be dispelled by a triangle constraint that deploying two antennas within a half of wavelength $( < \lambda / 2 )$ . In this situation, the $\Delta d$ can be determinately formalized as a piecewise equation with parameter of $\Delta \theta .$ Then the hyperbolic positioning is employed to locate the target tag. In detail, a hyperbola can be draw up using one $\Delta d ,$ on which the points are the candidate positions of target tag. To narrow the uncertainties, multiple hyperbolas are required. As a result, target position is released on the their common intersection. Nevertheless, it is hard to meet the spacing constraint in UHF RFID as stated before. Reconsidering this issue, we observe that the interrogation zone of RFID is actually narrowed in a lobe, beyond which the targets cannot be interrogated even. We do not need care about these noninterrogation regions when positioning. Motivated by this observation, we construct a virtual hyperbola C focusing on two antennas with arbitrary spacing and let the distance difference be $\lambda / 2$ . We strictly prove that the positions in the region among the two branches of C, termed as feasible region, still meet the triangle constraint. That is to say, the points in feasible region are positionable. We believe it is acceptable to relax the spacing constraint through sacrificing the feasible region due to the existence of interrogation zone.

Our approach has three major merits. (i) It is anchorfree as well as without need to deploy any infrastructure in advance, thereby it is very convenient to use in practice. (ii) Most of high accuracy methods [7], [8] take an analysis on the physical layer signals which is beyond the support from a Commercial Off-The-Shelf (COTS) reader. Instead, our approach does not require extra information from reader or tag, being in favor of COTS RFID products. (iii) Thanks to phase difference, no need to measure the initial phase rotation $\theta _ { T A G }$ , greatly extending its usage scope.

In summary, this paper makes the following contributions:

• We extensively conduct statistical analysis of phase collected from COTS products. We show that the phase is indeed a reliable indicator for tag positioning, preserved over frequency and tag orientation.   
• We propose a fine-grained positioning technique for backscatter system, called BackPos, with regarding to the tag’s limited capabilities in terms of energy and memory as well as its diversity. To our best knowledge, we are the first to introduce the interrogation zone to the tag positioning, based on which the triangle constraint can be relaxed to a reasonable level.   
• We implement a prototype of BackPos using ImpinJ R420 reader and EPC Gen2 tag. The evaluation results show that the mean position error is around 12.8cm

with a small standard variance of 3.8cm.

The remainder of the paper is structured as follows. Related work review is in Section 2. We introduce technical background of passive RFID system and conduct empirical studies on phase of passive radio in Section 3. The main design of BackPos is presented in Section 4. We give accuracy analysis of BackPos in Section 5 and discuss some practical issues in Section 6. An implementation and evaluation is given in Section 7. Finally, Section 8 concludes the paper.

# 2 RELATED WORK

There are considerable amount of research work on positioning in RFID and other wireless area. We present most related and recent work here, grouped into RSS-based and phase-based. Some other RFID related work and excellent positioning work in other research fields are reviewed as well.

RSS-based RFID localization: Landmarc [1], enables the reader power in eight levels and leverages RSS to find k nearest reference tags of target active tag, and positions target out. VIRE [2] use virtual reference tags to enhance accuracy of positioning. Landmarc and VIRE are early work of RFID localizaton. Bekkali et al. use Kalman filtering build a probabilistic model to reduce the effect of RSS error measurement [4]. Because RSS is not an accurate direct indicator for distance in practice, RSS is used as a fingerprint in these methods. They employ reference tags to estimate targets through fingerprint comparison. Therefore, they need high density reference tag deployment and measurement work before applying. In addition, RSSbased localization was extended to 3-D positioning [3], [9]. However, they need anchor arrays with location known in advance. The anchor could be tag or reader. Phasebased RFID localization: Azzouzi et al. test AOA in the complex baseband signals of adjacent antenna elements [5]. Zhang et al. examine the applicability of directionof-arrival (DOA) estimation methods to localization of passive RFID tags [6]. These two methods need an antenna spacing constraint to be $\lambda / 2 .$ . In commercial passive RFID systems, commercial polarized antennas are used to guarantee reading range. However, these antenna cannot meet the constraint because of large size. Three techniques are stated in [10]: Time Domain Phase Difference of Arrival(TD-PDOA), Frequency Domain Phase Difference of Arrival(FD-PDOA) and Spatial Domain Phase Difference of Arrival(SD-PDOA). Thereinto, SD-PDOA is similar to AoA, that is using antenna arrays to get different phase values and then locate target tag. TD-PDOA is a method to estimate radial velocity instead of accurate position, while FD-PDOA measures range from target tag by choosing special channel pairs, demanding high frequency bandwidth which is not allowed in commercial RFID systems to achieve high accuracy [11]. PinIt innovatively employs phase array to generate multipath profile and makes use of the profile as location fingerprints [8]. PinIt acquires high accuracy in reality environment under the precondition

![](images/9052e945db22a371b1e84e7fe27106c2f717f5ca5379cb2ab8bce298f99ceff5.jpg)



Fig. 1. Backscatter communication

T G = Reader antenna gain of high density reference tags. Besides, high resolution O = Carrier wavelength (meters) multipath profile need a large antenna array. PinIt uses a V = Tag Radar Cross Section (meters2 ) motion robot carrying an antenna instead.

R = Distance between reader and tag (meters) 22Other RFID related issues: Sheng et al. design polling TT PR P   3 4R 4 Squery to target tags instead of collecting all tags [12]. 8 Yang et al. explore how to make batch authentication without identification [13]. Chen et al. study the problem of collecting information from sensor augmented tags [14]. Luo et al. consider efficiency and energy saving while detecting missing tags [15]. Season shelves interference and identify tags by turns [16]. Lim [17] et al. design a query protocol for serverless mobile RFID systems. PMTI [18] identifies missing tags and OTrack [19] sequences a steam of RFID tags. ZOE [20] estimates cardinality for large-scale RFID systems.

WLAN localization: RADAR [21] was the first system to propose the use of a RF map for location and tracking users in WLAN based systems. Rai et al. leverage crowdsourcing to create training data for site-specific calibration [22]. PinPoint [23] and ArrayTrack [24] use antenna arrays at multiple APs to compute AOA of direct path, resulting in high accuracy. Hyperbolic positioning: Hyperbolic positioning comes from TDoA (Time Difference of Arrival), which mainly exists in locating GSM (Global System for Mobile Communications) base stations [25], [26]. Y.T.Chan gives a simple and efficient estimator for hyperbolic location [27]. We use the method of intersecting hyperbolas to locate target with analytical solution, which is different from [27].

# 3 PRELIMINARIES

In this section, we introduce the technical background on RFID system and also conduct a serial of empirical studies on the characteristics of phase in backscatter link.

# 3.1 Backscatter Radio Link

Passive tags not equipped with batteries do not use a radio transmitter. Instead, they use modulation of the reflected power from the tags. Figure 1 provides a conceptual diagram of the radio wave propagation between an RFID reader and a passive RFID tag. The backscatter radio link can be simply understood. The current flow on a reader’ antenna induces to a voltage on the tag’s antenna. This induced current is no different from the current on the tag’s antenna that started thing in the first place: it leads to radiation. The radiated wave can make its way back to the reader’s antenna, induce a voltage, and therefore, produce a signal that can be detected: a backscattered signal. In details, the tag replies to the reader’s query by backscattering the high power signal using ON-OFF keying. The tag transmits $\ ' _ { 1 } \ '$ bit by changing the impedance on their antennas to reflect the reader’s signal and a ’0’ bit by remaining in their initial silence state [28]. A typical UHF reader works in the frequency band that goes from the 860 MHz to the 950 MHz, such as 902 ∼ 928MHz ISM band in USA. In addition, the interrogation range of UHF reader is from a few meters up to tens of meters. Generally speaking, the range size is proportional to the power of reader’s antenna. Our approach can well accommodate these specifications.

![](images/36bc73f6e99e9e5b027e678a9d3f99949c870c272b587e6a3a16426733019461.jpg)



Fig. 2. Experiment scene in empirical studies and evaluation experiments.

# 3.2 RF Phase

Phase in backscatter system, as an important feature of wireless radio signal, is different from that in active radio. For an RF carrier wave at frequency f (Hz), the relation between frequency and wavelength λ is given by $\textstyle \lambda = { \frac { c } { f } }$ where c is the speed of the EM wave being equal to the speed of light $( \approx 3 \times 1 0 ^ { 8 } m / s )$ . The total distance traversed by the backscattered signal is $2 \times d$ as shown in Figure 1. In addition to the RF phase rotation over distance, the reader’s transmit circuits, the tag’s reflection characteristic, and the reader’s receiver circuits will all introduce some additional phase rotation, termed $\theta _ { T } , \theta _ { T A G } .$ , and $\theta _ { R } .$ Hence, the total phase rotation can be expressed as

$$
\theta + 2 k \pi = 2 \pi \frac {2 d}{\lambda} + \theta_ {T} + \theta_ {R} + \theta_ {T A G} \tag {1}
$$

where $\theta$ is an output parameter supported by a common COTS reader, and k is an integer guaranteeing the value of θ falling within [0, 2π). The $\theta _ { R }$ and $\theta _ { T }$ are constant parameters relevant to the characteristics of reader, which can be referred in reader’s manual. Although the $\theta _ { T A G }$ is another constant parameter relevant to the tag, we have no way to measure them ahead because there exist tens of thousands of tags in practice. It is a big practical challenge.

# 3.3 Empirical Studies

We firstly conduct a series of empirical studies on the characteristics of phase in backscatter link, using a COTS

![](images/36f5b0f47756ddafa710c35ccced3785cb6f04055dd64313e4cdd66648d36c67.jpg)



Fig. 3. Phase vs. Frequency

![](images/cf2c4c00faa598f076c92c074c25bc49a5d40e07b5d38db9b6a11f9c33849bb7.jpg)



Fig. 4. Phase Stability vs. Orientation

ImpinJ reader and four Alien tags and two Impinj tags. These experiments are designed towards verifying the following four hypotheses that need to hold using phase as indicator for tag positioning. The experiment scene is shown in Figure 2(Coordinates and feasible region in figure are explained in Section 7). Tag is clamped by a plastic upright.

Hypothesis 1: The phase appears random, but actually exhibits a stable statistical structure. This structure is preserved over frequency changes.

In the first experiment, one Alien Square tag is placed in front of a reader’s antenna over distance of 1.3m. We keep the tag’s position unchanged but hop the frequency during 16 available channels. Figure 3 shows the PDF of phase interrogated at different channels. For visual clarity, only three of them are displayed and the others are similar. In the figure, the results are plotted using histograms and fitted using solid curves. We can see that the phase actually follows a Gaussian distribution deviating within $\sim 5 . 7 ^ { \circ }$ . Such a small phase error leads to a very tiny ranging error $( \sim 5 . 7 / 3 6 0 * 1 6 . 5 c m = 0 . 2 6 c m )$ , which is an acceptable level.

Hypothesis 2: Phase stays stable when orientation of tag is deterministic and the impact of phase difference due to orientation change is negligible while the orientation difference is within $4 5 ^ { \circ }$ .

The second experiment involves the tag orientation, defined the angle between the tag and the antenna’s polarization orientation. We fix the frequency at the fifth channel but change the tag’s orientation from $0 ^ { \circ }$ to $3 6 0 ^ { \circ }$ . Under the plastic upright, we place a paper degree dial. Each time we rotate the tag around direction of gravity,

TABLE 1 Mean phase rotations when orientation changes 

<table><tr><td>Orientation difference (°)</td><td>Mean  $\theta_{TAG}$  variation(°)</td></tr><tr><td>90</td><td>9.4</td></tr><tr><td>60</td><td>7.1</td></tr><tr><td>45</td><td>6.3</td></tr><tr><td>30</td><td>5.5</td></tr><tr><td>10</td><td>5.8</td></tr></table>

we record phase values and the dial readings. Figure 4 shows the results at 8 orientations. We can see that phase value changes as we rotate the tag. When we fix the tag orientation, phase shows stability. Figure 4 gives all standard deviations of 8 orientations by applying Gaussian distribution fitting, evidencing the stability. However, when we use phase difference in an antenna pair, its orientations to two antennas are different, making two $\theta _ { T A G } \mathrm { s }$ not equal. Is this $\theta _ { T A G }$ difference acceptable? We sample the orientation difference at 5 levels and collect phase values, calculating the mean $\theta _ { T A G }$ variation, as listed in Table 1. The data shows that the $\theta _ { T A G }$ variation reaches about phase parsing error as stated in Hypothesis 1 when the orientation difference is under $4 5 ^ { \circ }$ , although the phase difference reaches to about $3 0 ^ { \circ }$ when the orientation is $9 0 °$ and $2 7 0 ^ { \circ }$ in Figure 4. In other words, when the orientation difference to different neighbouring antennas is within $4 5 ^ { \circ }$ , the impact of $\theta _ { T A G }$ during applying phase difference is negligible. In other words, when the orientation difference to different neighbouring antennas is within $4 5 ^ { \circ }$ , the impact of $\theta _ { T A G }$ during applying phase difference is negligible. For example, if distance between neighboring antennas is 40cm, the orientation difference requirement of being less than $4 5 ^ { \circ }$ is satisfied when the tag is more than 48.3cm straight away from the antenna line.

Hypothesis 3: The measured phase has linear relation to the distance within an intra-wave but stable periodicity at inter-wave.

This hypothesis is the foundation of backscatter positioning. In the third experiment, we attach one Alien Square tag on a toy train and let it move away from the antenna at a uniform linear motion. The timestamp when the tag is interrogated, is used to calculate the distance. The result is plotted in Figure 5. In the figure, we can see that the experimental results well match the theory. According to Equation 1, the phase should repeat from 0 to 2π every half wavelength $( \frac { \lambda } { 2 } \approx 1 6 . 5 c m )$ . In the figure, the measured cycle is about 17cm, very close to theoretical value. In addition, the linear relation and its periodicity are expected

![](images/83b345b757a048fb1a18c44be9f7e9faae0eb489bb64951001e551b5d92b43c1.jpg)



Fig. 5. Phase vs. Distance

to remain stable1.

Hypothesis 4: Different tag has different phase rotation at the same location, while the phase value remains stable for each one.

From the first experiment, we know that the phase value can be fitted with a normal distribution once the location and frequency fixed for that Alien Square tag. We conduct another simple experiment to examine whether it is true for other tags. We choose 6 tags and put them at one fixed location in turn. Reader queries them and records phase values in the same frequency. Fitting results are shown in Table 2. The mean value differs, indicating that phase value is related to tag diversity. All of these deviations are below $7 ^ { \circ }$ , demonstrating good stability of phase value for each tag.

Clearly, all of four experiments yield our hypotheses. The phase indeed a reliable indicator for tag’s position and is sensitive to tag diversity.

# 4 BACKPOS

In this section, we present our backscatter positioning approach, called BackPos, and gradually introduce its technical details later.

# 4.1 Basic Idea

Although the phase is an appealing indicator for accurate ranging within half a wavelength as stated, there exist two serious uncertainties affecting the phase for positioning. The first is that the phase is periodic such that there exists

1. The reason why the phase decreases as the distance increasing is explained in Section 7.

TABLE 2 Phase vs. Tag Diversity 

<table><tr><td>Tag</td><td>Mean Phase(°)</td><td>Standard deviation(°)</td></tr><tr><td>Alien Square #1</td><td>328.8</td><td>6.3</td></tr><tr><td>Alien Square #2</td><td>227.6</td><td>4.4</td></tr><tr><td>Alien 2×2 #1</td><td>35.1</td><td>6.1</td></tr><tr><td>Alien 2×2 #2</td><td>100.2</td><td>5.8</td></tr><tr><td>Impinj E41B #1</td><td>196.8</td><td>6.4</td></tr><tr><td>Impinj E41B #2</td><td>344.7</td><td>5.4</td></tr></table>

a candidate position once every a propagating cycle. The second uncertainty is that the we have no idea about the initial rotation $( \theta _ { T A G } )$ for every tag and no way to infer the distance d from the θ reported by the reader based on Equation 1.

We notice that a common COTS reader usually has four directional antennas. They can be collaboratively used for eliminating above two uncertainties. Suppose we have two antennas, $A _ { 1 } ( x _ { 1 } , y _ { 1 } )$ and $A _ { 2 } ( x _ { 2 } , y _ { 2 } )$ , available to interrogate the target tag $T ( x , y )$ , and their distances from the tag to the two antennas are $| T A _ { 1 } | = d _ { 1 }$ and $| T A _ { 2 } | = d _ { 2 }$ . Assuming the phase results are $\theta _ { 1 }$ and $\theta _ { 2 }$ measured by $A _ { 1 }$ and $A _ { 2 } .$ , we can get two equations based on Equation 1 as follows.

$$
\theta_ {1} + 2 k _ {1} \pi = 2 \pi \frac {2 d _ {1}}{\lambda} + \theta_ {T _ {1}} + \theta_ {R _ {1}} + \theta_ {T A G - 1} \tag {2}
$$

$$
\theta_ {2} + 2 k _ {2} \pi = 2 \pi \frac {2 d _ {2}}{\lambda} + \theta_ {T _ {2}} + \theta_ {R _ {2}} + \theta_ {T A G - 2} \tag {3}
$$

Subtracting above equations, we have

$$
\Delta \theta_ {2, 1} + 2 (k _ {2} - k _ {1}) \pi = \frac {4 \pi}{\lambda} \Delta d _ {2, 1} + \rho \tag {4}
$$

where $\Delta \theta _ { 2 , 1 } = \theta _ { 2 } - \theta _ { 1 } , \Delta { d } _ { 2 , 1 } = d _ { 2 } - d _ { 1 }$ and $\rho = ( \theta _ { T _ { 2 } } -$ $\theta _ { T _ { 1 } } + ( \theta _ { R _ { 2 } } - \theta _ { R _ { 1 } } ) + ( \theta _ { T A G - 2 } - \theta _ { T A G - 1 } )$ . Removing the subscripts, the equation can be simplified as

$$
\Delta d = \frac {\lambda}{4 \pi} (\Theta + 2 k \pi) \tag {5}
$$

where k is a new integer ensuring $\Theta = \left( \Delta \theta - \rho \right)$ within $( - 2 \pi , 2 \pi )$ . In Equation 5, the unknown tag diversity related term of $\left( \theta _ { T A G - 2 } - \theta _ { T A G - 1 } \right)$ is negligible if we keep orientation difference to two neighboring antennas less than about $4 5 ^ { \circ }$ , which is quite easy to satisfy as stated in Hypothesis 2. Suppose the ∆d is able to be inferred from ∆θ, can we reveal the target position? The answer is yes. As well known, a hyperbola is a curve being composed of the locus of points for which the difference of the distances from two given fixed points is a constant. Therefore, once knowing ∆d, we can construct such a hyperbola that focuses on the two antennas’ positions and formalized as follows:

$$
| \sqrt {(x - x _ {1}) ^ {2} + (y - y _ {1}) ^ {2}} - \sqrt {(x - x _ {2}) ^ {2} + (y - y _ {2}) ^ {2}} | = \Delta d
$$

If we establish coordinate system enabling the two focuses locating in x-axis and the origin coinciding with their centers, above equation can be simplified to:

$$
\frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \text {where} \left\{ \begin{array}{l} a = \Delta d \\ b = \sqrt {c ^ {2} - a ^ {2}} \\ c = \sqrt {(x _ {1} - x _ {2}) ^ {2} + (y _ {1} - y _ {2}) ^ {2}} / 2 \end{array} \right.
$$

In this way, the target tag’s position is confined on the curve. Further, when multiple hyperbolas are constructed via multiple $\Delta d ,$ the target’s 2D or 3D position2 can be discovered on the their common intersection.

2. Note that the 2D positioning is focused here for clear representation, but we must claim that our approach suitable for 3D positioning.

Although the hyperbolic positioning is able to reveal the target position using enough antennas, we still confront three uncertainties. (1) The first comes from the ambiguous relationship between $\Delta d$ and $\Delta \theta$ due to the phase periodicity. The latter cannot directly induce the former. This will leads to numerous possible candidates. We need find a way to filter out the real one. (2) The second uncertainty is that every hyperbola has two branches which may raise the possible intersections as the number of hyperbola increases, even if we exactly known the distance difference. (3) The hyperbolic equation is too complex to find an analytical solution when there are many combined equations [27]. The common method is to seek an inaccurate numerical solution, which may further contribute to the position error. Instead, we want to leverage the feature of directional antenna and specific deployment method to solve an analytical solution. Next, we are going to gradually address these issues.

# 4.2 Finding the feasible region

From Equation 5, the distance difference is actually a large set due to the periodicity. At a first glance, it seems impossible to filter out the real one. However, we observe three important facts in practice, aiding us to carefully exclude the incorrect ones.

Fact 1 (Triangle Constraint): The fact is that the ∆d is deterministic when two antennas are deployed within a spacing of half a wavelength.

Suppose two antennas $A _ { 1 }$ and $A _ { 2 }$ are deployed within a spacing of half wavelength as illustrated in Figure 6, the distance difference $\Delta d$ from the target tag $T$ to two antennas meets the following inequation:

$$
\left| \Delta d \right| = \left| d _ {2} - d _ {1} \right| <   \frac {\lambda}{2} \tag {6}
$$

Above inequality can be easily proved by the triangle inequality. Substituting Equation 5 into Inequation $^ { 6 , }$ we can obtain

$$
| \Delta d | = \left| \frac {\lambda}{4 \pi} \Theta + \frac {\lambda}{2} k \right| <   \frac {\lambda}{2} \tag {7}
$$

where $- 2 \pi < \Theta < 2 \pi$

In a particular instance, the Θ can be calculated using the reader output θ and its transceiver characteristic’s $\rho .$ Considering the sign of Θ, there exist two cases:

(1) Assuming $0 \leq \Theta < 2 \pi$ , there are two sub cases. (i) if $\Delta d = d _ { 2 } - d _ { 1 } \geq 0$ , the target is closer to $A _ { 1 }$ than $A _ { 2 } ,$ then k must equal 0 to ensure $\begin{array} { r } { 0 \leq \frac { \lambda } { 4 \pi } \Theta + \frac { \lambda } { 2 } k < \frac { \lambda } { 2 } } \end{array}$ holding true. Therefore $\begin{array} { r } { \Delta d = \frac { \lambda } { 4 \pi } \Theta } \end{array}$ 4π . (ii) contrary to the first sub case, if $\Delta d < 0$ , the target is closer to $A _ { 2 }$ than $A _ { 1 }$ . The k must equal −1 to ensure $\begin{array} { r } { - \frac { \pi } { 2 } \le \frac { \lambda } { 4 \pi } \Theta + \frac { \lambda } { 2 } k < 0 } \end{array}$ . Hence, $\begin{array} { r } { \Delta d = \frac { \lambda } { 4 \pi } \Theta - \frac { \lambda } { 2 } } \end{array}$ . This case can be summarized as:

$$
\Delta d = \left\{ \begin{array}{l l} \frac {\lambda}{4 \pi} \Theta & \Delta d \geq 0 \\ \frac {\lambda}{4 \pi} \Theta - \frac {\lambda}{2} & \Delta d <   0 \end{array} \right. \tag {8}
$$

In fact, above piecewise expression constitutes a hyperbola which has two different branches.

(2) Assuming $- 2 \pi \leq \Theta < 0 .$ , there exist two sub cases as well. (i) if $\Delta d \ge 0 .$ , then k must be 1 to guarantee $\begin{array} { r } { 0 \leq \frac { \lambda } { 4 \pi } \Theta + \frac { \lambda } { 2 } k < \frac { \lambda } { 2 } } \end{array}$ . Thus, $\begin{array} { r } { \Delta d = \frac { \lambda } { 4 \pi } \Theta + \frac { \lambda } { 2 } } \end{array}$ . (ii) otherwise $\Delta d \ < \ 0$ , then k must be 0 to ensuring $\begin{array} { r } { - \frac { \lambda } { 2 } \ \leq \ \frac { \lambda } { 4 \pi } \Theta + } \end{array}$ $\begin{array} { r } { \frac { \lambda } { 2 } k < 0 . } \end{array}$ , then k must be 0. Thus, $\begin{array} { r } { \Delta d = \frac { \lambda } { 4 \pi } \Theta . } \end{array}$ 2 4π. This case is summarized as:

$$
\Delta d = \left\{ \begin{array}{l l} \frac {\lambda}{4 \pi} \Theta + \frac {\lambda}{2} & \Delta d \geq 0 \\ \frac {\lambda}{4 \pi} \Theta & \Delta d <   0 \end{array} \right. \tag {9}
$$

This is an another hyperbola with two different halves.

For a particular instance, only one case happens because the Θ is deterministic. We choose $\lambda / 2$ instead of λ being the constraint because the wave prorogates double distance in backscatter system. Thanks to triangle constraint, we successfully confine the $\Delta d$ in a deterministic value. However, the triangle constraint behaves too rigid to meet in practice because the wavelength of UHF is very small. For example, if $f = 9 2 0 . 6 2 5 M H z$ , the spacing between two antennas should be within ∼ 16.3cm. Considering the antenna size $( \sim 2 5 c m \times 2 5 c m )$ , it is impossible to enable any two antennas’ spacing within 16.3cm when more than two antennas are used.

Fact 2 (Feasible Region): There always exists a continuous region meeting the triangle constraint even if the spacing of two antennas is greater than $\lambda / 2$ . Such region is called feasible region.

Given the spacing between two antennas is $| A _ { 1 } A _ { 2 } | =$ $d _ { \mathrm { a n t } }$ , we can construct such a virtual hyperbola C that the absolute distance difference $\begin{array} { r } { | T A _ { 1 } - T A _ { 2 } | = \frac { \lambda } { 2 } } \end{array}$ for any point $T$ on the curve. The mathematical equation of hyperbola C is given by

$$
\frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \text {   where   } \left\{ \begin{array}{l} a = \frac {\lambda}{2} \\ b = \sqrt {c ^ {2} - a ^ {2}} \\ c = \frac {d _ {\mathrm{ant}}}{2} \end{array} \right.
$$

We claim that the space between the two branches of hyperbola ${ \mathcal { C } } ,$ the shadow area illustrated in Figure 7, is the feasible region. Next, we strictly prove this statement.

Theorem 1: Let $A _ { 1 }$ and $A _ { 2 }$ be two focus points of a hyperbola with the distance difference of $\Delta d .$ Then, for any point $P$ in the space between two curves of the hyperbola, the inequation $| P A _ { 1 } - P A _ { 2 } | \leq \Delta d$ always holds true.

Proof: Suppose $A _ { 1 } ( - x _ { 0 } , 0 ) , \ A _ { 2 } ( x _ { 0 } , 0 )$ and $P ( x , y )$ , illustrated in Figure 7. Apparently, $\forall P ( x = 0 , y ) , | P A _ { 1 } -$ $P A _ { 2 } | = 0$ . Due to the symmetry, we only need to prove the case that $x > 0$ . The same procedure can be proved for the other side $x < 0$ . Define $g ( x , y )$ be the distance difference for $P ,$ , namely,

$$
g (x, y) = P A _ {1} - P A _ {2}
$$

$$
= \sqrt {(x + x _ {0}) ^ {2} + y ^ {2}} - \sqrt {(x - x _ {0}) ^ {2} + y ^ {2}}
$$

we have

$$
\frac {\partial g (x , y)}{\partial x} = \frac {x + x _ {0}}{\sqrt {(x + x _ {0}) ^ {2} + y ^ {2}}} - \frac {x - x _ {0}}{\sqrt {(x - x _ {0}) ^ {2} + y ^ {2}}}
$$

$$
= \Psi^ {- 1} [ \sqrt {(x - x _ {0}) ^ {2} (x + x _ {0}) ^ {2} + y ^ {2} (x + x _ {0}) ^ {2}} -
$$

$$
\sqrt {(x - x _ {0}) ^ {2} (x + x _ {0}) ^ {2} + y ^ {2} (x - x _ {0}) ^ {2}} ]
$$

![](images/b700ce20ea1953339034684aa21ecc89ed5fae04c2e8573b57cdada87c2d2d14.jpg)



Fig. 6. Triangle constraint

![](images/b71741d96047b32b949305d000f81488f27c100f55b5ffac4c4793557a06e9f0.jpg)



Fig. 7. Feasible region

where

$$
\Psi = \sqrt {[ (x + x _ {0}) ^ {2} + y ^ {2} ] [ (x - x _ {0}) ^ {2} + y ^ {2} ]} > 0
$$

Because $x \geq 0 , y ^ { 2 } ( x + x _ { 0 } ) ^ { 2 } \geq y ^ { 2 } ( x - x _ { 0 } ) ^ { 2 }$ . Therefore,

$$
\sqrt {(x - x _ {0}) ^ {2} (x + x _ {0}) ^ {2} + y ^ {2} (x + x _ {0}) ^ {2}} \geq
$$

$$
\sqrt {(x - x _ {0}) ^ {2} (x + x _ {0}) ^ {2} + y ^ {2} (x - x _ {0}) ^ {2}}
$$

Finally, we have

$$
\forall x > 0, \frac {\partial g (x , y)}{\partial x} > 0 \tag {10}
$$

In addition, $\forall P ( x , y ) | x \geq 0 , \exists P ^ { \prime } ( x ^ { \prime } , y )$ in the hyperbola $( P ^ { \prime } A _ { 1 } - P ^ { \prime } A _ { 2 } = \Delta d )$ , making:

$$
x ^ {\prime} > x > 0
$$

Combine with Inequation 10, we get $g ( x ^ { \prime } , y ) > g ( x , y )$ . That is $| P A _ { 1 } - P A _ { 2 } | < \Delta d$ .

When applying, we can coarsely estimate the area to localize and then adjust the antennas’ deployment for ensuring feasible region covers the area. In order to assist the adjustment, we approximate the feasible region $D _ { \mathrm { a b c d e f } }$ using curve $\mathit { c } _ { \mathrm { { s } } }$ the asymptotic line and formalize it as follows.

$$
y = \left\{ \begin{array}{l l} - \frac {b}{a} x & x \leq - a \\ 0 & - a <   x \leq a \\ \frac {b}{a} x & x > a \end{array} \right. \tag {11}
$$

Substituting $( d _ { \mathrm { a n t } } , \frac { \lambda } { 2 } )$ into that function, we get:

$$
D = \{(x, y) | y \geq \left\{ \begin{array}{l l} - \frac {\sqrt {d _ {\mathrm{ant}} ^ {2} - (\lambda / 2) ^ {2}}}{\lambda / 2} x & x \leq - \frac {\lambda}{4} \\ 0 & - \frac {\lambda}{4} <   x \leq \frac {\lambda}{4} \\ \frac {\sqrt {d _ {\mathrm{ant}} ^ {2} - (\lambda / 2) ^ {2}}}{\lambda / 2} x & x > \frac {\lambda}{4} \end{array} \right. \tag {12}
$$

Region D is the feasible region that enabling our approach feasible when the target locates there.

Fact 3 (Interrogation Zone): The reader usually employs the directional antennas in order to increase the energy received by the tag.

The feasible region is a trade-off that balances the realizability and the practical deployment. We think such a trade-off is reasonable because the interrogation zone is narrowed in a lobe, as shown in Figure 9, being similar to our feasible region. Considering the main lobe as a cone, the beam angle $\theta _ { \mathrm { l o b e } } \approx { \sqrt { \frac { 4 \pi } { G } } }$ . If we need the signal gain $G$ be 5dB, $\theta _ { \mathrm { l o b e } }$ would be about $9 0 ^ { \circ }$ . We plot two antennas’ interrogation zones in Figure 6. They are sector $D _ { C A _ { 1 } F }$ and sector $D _ { E A _ { 2 } D }$ . The target in the shadow area can be interrogated as well as positioned by both antennas. Clearly, the common interrogation zone is smaller than the feasible region in fact. Therefore we think feasible region is acceptable in practice.

# 4.3 Hyperbolic Positioning

We filter out a piecewise distance difference $\Delta d$ so far. With this piecewise model, we can plot an unsymmetrical hyperbola owning two different branches. For example, the hyperbola focusing on antenna $A _ { 1 }$ and $A _ { 2 } ,$ , have two halves of $c _ { 1 }$ and $c _ { 3 }$ , illustrated in Figure 8. In theory, there appears  n2 such hyperbolas given any n antennas. Their common intersection of these curves is indeed our target position.

An example shown in Figure 8 is displayed here to show how the hyperbolic positioning works. Let $T$ be the target in a common feasible region of three antennas $A _ { 1 } , A _ { 2 }$ and $A _ { 3 }$ . All these directional antennas are deployed to interrogate the north area. Suppose the measured phase differences are $\Delta \theta _ { A _ { 1 } , A _ { 2 } } > 0$ and $\Delta \theta _ { A _ { 2 } , A _ { 3 } } < 0$ . Then the first piecewise hyperbola contributed by antenna $A _ { 1 }$ and $A _ { 2 }$ is represented:

• Curve $c _ { 1 } { : }$ the west branch of the hyperbola with distance difference $\begin{array} { r } { | T A _ { 1 } | - | T A _ { 2 } | = \Delta d _ { 1 , 2 } = \frac { \lambda } { 4 \pi } \Theta _ { 1 , 2 } - } \end{array}$ ${ \frac { \lambda } { 2 } } .$ .   
• Curve $c _ { 3 } { : }$ the east branch of the hyperbola with distance difference $\begin{array} { r } { | T A _ { 2 } | - | T A _ { 1 } | = \Delta d _ { 2 , 1 } = \frac { \lambda } { 4 \pi } \Theta _ { 1 , 2 } . } \end{array}$   
The second piecewise hyperbola comprised by antenna $T _ { 2 }$ and $T _ { 3 }$ is represented:

• Curve $c _ { 2 } { : }$ the west branch of the hyperbola with distance difference |T A2|−|T A3| = ∆d2,3 = λ4π $\begin{array} { r } { | T A _ { 2 } | - | T A _ { 3 } | = \Delta d _ { 2 , 3 } = \frac { \lambda } { 4 \pi } \Theta _ { 2 , 3 } , } \end{array}$

• Curve $c _ { 4 } { : }$ the east branch of the hyperbola with distance difference $\begin{array} { r } { | T A _ { 3 } | - | T A _ { 2 } | = \Delta d _ { 3 , 2 } = \frac { \lambda } { 4 \pi } \Theta _ { 2 , 3 } + } \end{array}$ ${ \frac { \lambda } { 2 } } .$ .

From the figure, we can see that six intersections are released from the four curves. Since the antennas are directional, the negative direction of y-axis is abandoned. Finally, we get candidate set $R = \{ T _ { 1 } , T _ { 2 } , T _ { 3 } \}$ at worst case through solving the two combined hyperbolic equations. We say that is the worst case, because there may be no intersection between $c _ { 1 }$ and $c _ { 2 }$ when the curve $c _ { 1 }$ has greater hyperbolic eccentricity than $c _ { 2 }$ . The similar case happens between $c _ { 3 }$ and $c _ { 4 } .$ The best case occurs only when one intersection $T _ { 1 }$ exists between $c _ { 2 }$ and $c _ { 3 } ,$ , then $T { = } T _ { 3 }$ .

![](images/92c2a0fc8ffa5e16416640e8008c3554dee340126da20df867d7595567e9735a.jpg)



Fig. 8. Hyperbolic positioning

![](images/7ce3406471e2433f7eb39fece161bea554e4f2d36c688603d76f1b122b3987f8.jpg)



Fig. 9. Interrogation zone

If $| R | > 1 ~ ^ { 3 }$ , then we need extra effort to eliminate the uncertainty. There are two methods. One method is to construct another piecewise hyperbola through the phase difference from target T to antenna $A _ { 1 }$ and $A _ { 3 }$ . Utilizing the third hyperbolic, we can get another candidate set $R ^ { \prime }$ . However, such a method may be impractical because the area of feasible region decreases as the distance $d _ { \mathrm { a n t } }$ increases based on Equation 12. The distance $d _ { \mathrm { a n t } }$ between $A _ { 1 }$ and $A _ { 3 }$ is twice as much as that of $A _ { 1 }$ and $A _ { 2 }$ , which may narrow the feasible region in a small centrum and cause the target out of the region. The second method is to deploy the fourth antenna $A _ { 4 }$ in the east of antenna $A _ { 3 }$ for constructing the new hyperbola. The new candidate set $R ^ { \prime }$ can be obtained by antenna $A _ { 2 } , A _ { 3 }$ and $A _ { 4 }$ . We think the second method is more practical because a common COTS usually has four antennas. Finally the real target position is revealed by $T = R \cap R ^ { \prime }$ .

In practice, there may be no exact intersection between set R and $R ^ { \prime }$ due to the measurement noise. In this situation, we advise to employ the average positions of the nearest two points as the target position, formalized as follows.

$$
T = \frac {T _ {1} + T _ {2}}{2} \text {   where   } (T _ {1}, T _ {2}) = \underset {T _ {i} \in R, T _ {j} \in R ^ {\prime}} {\operatorname{argmin}} | | T _ {i} - T _ {j} | | \tag {13}
$$

# 4.4 Solving hyperbolic equations solution

The kernel of hyperbolic positioning is to seek the solution from a group of combined equations. The usual way is to employ numerical methods, like Steepest Descent and Newton-Raphson, to solve equations. However, These methods’ outputs are just approximate. Their accuracy fully depends on times of iterations. More accurate solution requires more iterations as well as more computation resource. Here, we leverage two characteristics, antenna’s directionality and horizontal deployment, to pursuit analytical solution.

3. |R| stands for the cardinality of set R.

As illustrated in Figure 8, three antennas are arranged at X axis, which are focus points of positioning hyperbolas. For this reason, four hyperbolic curves are shifted from standard hyperbolas along X axis. Take $c _ { 1 }$ and $c _ { 2 }$ in Figure 8 for example, the hyperbolic equations are:

$$
\left\{ \begin{array}{l} \frac {(x - h _ {1}) ^ {2}}{a _ {1} ^ {2}} - \frac {y ^ {2}}{b _ {1} ^ {2}} = 1 \\ \frac {(x - h _ {2}) ^ {2}}{a _ {2} ^ {2}} - \frac {y ^ {2}}{b _ {2} ^ {2}} = 1 \end{array} \right. s. t \left\{ \begin{array}{r c l} x & <   & \min (h _ {1}, h _ {2}) \\ y & \geq & 0 \\ a _ {i} & = & \frac {\triangle d _ {i}}{2} \\ c _ {i} & = & \frac {d _ {\text {ant,i}}}{2} \\ b _ {i} & = & \sqrt {c _ {i} ^ {2} - a _ {i} ^ {2}} \end{array} \right. \tag {14}
$$

where h is the middle point of two focus points, a and b are semi-minor parts of real axis and imaginary axis, respectively.We get a key observation that, both $x y$ and y component do not exist that quadratic equations. Hence, we can combine two equations to eliminate $y ^ { 2 }$ component. Namely, the dual quadratic group is transformed into a quadratic equation of x:

$$
\left(\frac {b _ {1} ^ {2}}{a _ {1} ^ {2}} - \frac {b _ {2} ^ {2}}{a _ {2} ^ {2}}\right) x ^ {2} - 2 \left(\frac {b _ {1} ^ {2}}{a _ {1} ^ {2}} h _ {1} - \frac {b _ {2} ^ {2}}{a _ {2} ^ {2}} h _ {2}\right) x + \frac {b _ {1} ^ {2}}{a _ {1} ^ {2}} h _ {1} ^ {2} - \frac {b _ {2} ^ {2}}{a _ {2} ^ {2}} h _ {2} ^ {2} - \left(b _ {1} ^ {2} - b _ {2} ^ {2}\right) = 0 \tag {15}
$$

Now, we can use single variable quadratic solution formula to get analytical expression of $x$ from Equation 15 and substitute it into Equations 14 to get y.

The reason why we have analytical expression of variable $x$ and $y ,$ is that we lay antennas in a line, which will be in X axis. In this case, there are no xy and y components in all hyperbola expressions. As a result, variable x can be completely eliminated by combining two expressions. Besides, if we do not arrange antennas in a straight line, the feasible region intersection of $D _ { i }$ of each antenna couple would be a narrow and close domain. Obviously, an open and broad region where objects can be positioned is what we expect. Based on these two advantages, BackPos arranges antennas in a straight line, four antennas more specific.

# 4.5 Solving antenna phase differences

BackPos calculates $\Delta d$ from Θ through hyperbolic constraint, where $\Theta = \Delta \theta - \rho$ . We can get $\Delta \theta$ by phase values to different antennas from reader in real time, while $\rho = ( \theta _ { T _ { 2 } } - \theta _ { T _ { 1 } } ) + ( \theta _ { R _ { 2 } } - \theta _ { R _ { 1 } } )$ should be measured during deployment. In other words, we can solve the antenna phase differences once for all. The method is quite simple. For each neighbouring antenna pair, we put a tag in the midperpendicular of these two antennas. Therefore, propagting distances from the tag to two antennas are equal, making $\rho = \theta _ { 2 } - \theta _ { 1 }$ , where $\theta _ { 2 }$ and $\theta _ { 1 }$ are phase values presented by reader. Afterwards, BackPos employs $\rho$ obtained and positions targets in feasible region according to steps stated above.

# 4.6 Summary

A little deployment work is required to apply BackPos. We need to put four antennas in a line and in face of application areas. For example, we could place antennas against the wall to cover goods shelves in a warehouse. Then we measure distances between neighbouring antennas as input parameter and obtain the antenna phase differences. BackPos will show the feasible region where targets could be positioned. We discuss how to adjust feasible region according to interrogation zone of RFID antenna to maximize space utilization in Section 6. After these work done, positioning is available. For example, whenever we desire to find an item on goods shelves, we just input the Electronic Product Code(EPC) into BackPos. BackPos queries the EPC and read phase values from tag through different antennas. These values would be transformed into distance differences and estimated position eventually.

Being different from the traditional AoA methods, our approach focuses on the features of backscatter systems and leverage them to aid our positioning. In this section, we present the details of BackPos and address the following research issues: (1) how to induce the distance difference from the measured phase difference. (2) how to relax the triangle constraint, make long-range commercial directional antenna adoptable, but still remain the capability of revealing expected distance difference. (3) how to conduct the hyperbolic positioning with a group of combined piecewise hyperbolic equations. (4) At last, we also give rather accurate analytical solution for the equations.

# 5 ACCURACY ANALYSIS

In spite of the analytic solution given, there still exist many noises interfering the position accuracy. Typically, the measured phase does not behave a constant but follow a Gaussian model as stated. In this section, we will study how this factor takes impact on the accuracy.

# 5.1 Analysis of phase difference

As mentioned before, the phase noises yield a typical Gaussian model due to the thermal noises of electronic components. Such model can be obtained in practice using statistical methods. We define two random variables $\theta _ { 1 }$ and $\theta _ { 2 }$ to denote the measured phases using two different antennas. These two variables are independent and follow two Gaussian models with same variance. Namely, $\theta _ { 1 } \sim \mathcal { N } ( \mu _ { 1 } , \sigma ^ { 2 } )$ and $\theta _ { 2 } \sim \mathcal { N } ( \mu _ { 2 } , \sigma ^ { 2 } )$ . It is well known that the sum or difference of two independent Gaussian random variables still follows a Gaussian model. Therefore, the phase difference $\Delta \theta = \theta _ { 2 } - \theta _ { 1 }$ is still a random variable and follows

![](images/604de8aa28b240d895200c3f94b31279dca970350e505c1bcad8d04e2bbdfec8.jpg)



Fig. 10. Effect of distance difference error on position result

$$
\Delta \theta \sim \mathcal {N} \left(\mu_ {1} - \mu_ {2}, 2 \sigma^ {2}\right) \tag {16}
$$

# 5.2 Analysis of distance difference

We attempt to reveal the distribution of distance difference $\Delta d$ by the ∆θ. Note that the $\Delta d$ is a piecewise function with variable of $\Delta \theta ,$ we should give the analysis for each piece. However, we only consider the common piece, $\Delta d =$ ${ \frac { \lambda } { 4 \pi } } \Delta \theta ^ { \ 4 }$ , here for brevity. The other pieces can be induced using the same way. Then, $\begin{array} { r } { \Delta d = \frac { \lambda } { 4 \pi } \bar { \Delta \theta } } \end{array}$ and the distribution of $\Delta d$ is expressed as

$$
\Delta d \sim \mathcal {N} \left(\frac {\lambda}{4 \pi} (\mu_ {1} - \mu_ {2}), 2 (\frac {\lambda}{4 \pi} \sigma) ^ {2}\right) \tag {17}
$$

For example, the phase standard deviation $\begin{array} { r } { \sigma = \frac { 5 . 7 ^ { \circ } } { 1 8 0 ^ { \circ } } \pi \approx } \end{array}$ 180◦ π ≈ 0.099 according to the documents of Impinj RFID reader, validated in our experiment shown in Figure 3. Assume the wave length equals 32.50cm, we have:

$$
P(| \Delta d - E(\Delta d)|\leq 1cm) = 99.5\%
$$

The result indicates that the distance difference error is bounded under 1cm with 99.5% confidence. We believe such result is accurate enough in practice.

# 5.3 Analysis of positioning

We want to know how the noise affects positioning accuracy. To answer this question, we conduct simulation as follows. We deploy 5 targets and 3 antennas in the feasible region. Based on equation 17, we randomly generate 1000 pairs of distance differences for each target with noise using an empirical Gaussian model. These values are fed into hyperbolic positioning and the error results (Euclidean distance) are plotted in Figure 10. From the figure, we observe that (1) More than 80% of error remains in 21cm

4. We simply assume $\rho = 0$ and $\Delta \theta = \Theta$ . The constant term does not influence our analysis.

for 5 positions. (2) The mean error are 12.6cm, 10.4cm, 1.4cm, 10.7cm, 7.4cm respectively. We can see that the theoretical result is rather convincing.

# 6 DISCUSSION

In this section, we attempt to answer some practical issues.

# 6.1 Why choose $\frac { \lambda } { 2 }$ as distance difference constraint?

BackPos uses $\frac { \lambda } { 2 }$ as the difference constraint to induce a hyperbola with two different branches. Actually, the reasonable choice is to set the constraint as $\frac { \lambda } { 4 }$ . In this case, k must be 0 to ensure the $| \Delta d | \ = \ | \frac { \lambda } { 4 \pi } \Theta \dot { { ^ { \ } + } } \frac { \lambda } { 2 } k | \ < \ \frac { \lambda } { 4 }$ . Then $\begin{array} { r } { | \Delta d | \ = \ | \frac { \lambda } { 4 \pi } \Theta | } \end{array}$ and the hyperbola has a pair of symmetrical branches. However, this choice will cause the feasible region too narrow to accommodate any target tag. On the other hand, if the constraint is greater than $\lambda / 2$ , there exist more than two possible values of $\Delta d ,$ drawing multiple branches. Hence, we think the $\frac { \lambda } { 2 }$ is best constraint condition.

# 6.2 How to adjust the feasible region?

As mentioned before, the feasible region is acceptable due to the existence of interrogation zone. In practice, we would adjust them to be maximum overlapped for better space utilization. Namely, let the slope of feasible region be greater than the slope of half-lobe of interrogation zone:

$$
\frac {\sqrt {d _ {\mathrm{ant}} ^ {2} - (\lambda / 2) ^ {2}}}{\lambda / 2} > t a n (\frac {\theta_ {l o b e}}{2})
$$

As mentioned before, $\begin{array} { r } { \theta _ { \mathrm { l o b e } } \approx \sqrt { \frac { 4 \pi } { G } } , } \end{array}$ . Therefore,

$$
\frac {\sqrt {d _ {\mathrm{ant}} ^ {2} - (\lambda / 2) ^ {2}}}{\lambda / 2} > \tan (\sqrt {\pi G ^ {- 1}}) \tag {18}
$$

where G is the antenna gain. During deployment, we could adjust $d _ { \mathrm { a n t } }$ to make G satisfied.

# 6.3 How to combat the multipath effect?

Multipath effect is a common issue for wireless localization systems. There have been some excellent solutions [7], [24] developed recent years. Their basic ideas are to find out the direct path among all paths. We directly borrow their methods here. In addition, the reader usually has multiple channels (10+) available. We can choose the optimal one. However, this issue is beyond our discussion in this paper. We will take further study in our future work.

# 6.4 Requirements and limitations of BackPos

BackPos requires some deployment work, as discussed in Section 4, including antenna arrangement and antenna phase differences collection. However, workload of deploying BackPos is far less than that of reference tag based methods. Working area, that is intersection of feasible region and interrogation zone of antennas, is settled and antennas stay still after deployment. Besides, since BackPos employs phase value of direct signal propagation path, i.e. line of sight link, multipath would lower positioning accuracy. As stated above, one important furture work is to find out direct path among all paths to eliminate effect of multipath.

# 7 IMPLEMENTATION AND EVALUATION

In this section, we present the implementation and conduct performance evaluation on the prototype.

# 7.1 Implementation

Hardware: We implement a prototype of BackPos using Impinj R420 with four directional antennas. There are two types of tags modeled $^ { 6 } 2 \times 2 ^ { 5 }$ or ‘Square’ from Alien company, used in our experiments. The reader works during the frequency of $9 2 0 . 5 M H z \sim 9 2 4 . 5 M H z$ by default, which is the legal UHF band in China. Correspondingly, the wavelength ranges from 32.43.cm to 32.57cm. Software: The software part running at personal computer is implemented using Java language. It connects to the RFID reader with LLRP protocol. This protocol was ratified by EPCglobal in April 2007. Parameter choice: The antenna’s transmission power are adjusted at 30mW . We command the reader to immediately report its readings after a round of antenna scheduling. Although our approach is able to weaken the impact of tag’s initial rotation $\theta _ { T A G }$ , the reader transceiver’s initial rotation $\theta _ { T }$ and $\theta _ { R }$ would still affect the measurement results as shown in Equation 1. These two values should be referred to the reader’s specification. It not found, we suggest the following simple method to measure them in practice. Placing a tag on the perpendicular bisector of two antennas, then $\rho = ( \Delta \theta$ mod 2π) where the distance factor is eliminated because $\Delta d = 0$ .

# 7.2 Evaluation Methodology

Three experiments are designed towards measuring the accuracy of BackPos. Our experiments are performed in an office room whose size is $5 \times 8 m ^ { 2 }$ . Four antennas are deployed with a spacing of 40cm in a straight line, polarized to a same direction. The antennas and target tags are all suspended at 1.32m high from the ground. The ground truth is measured using a laser distance meter with an error of 1mm. During the measurement, we consider the antennas and tags the points locating in their geometric centers. Figure 2 shows the experiment scene which illustrates the coordinate system, feasible region, experimental tags, reader, and antennas. The coordinates of four antennas are $A _ { 1 } ( 5 9 . 7 , - 1 ) , A _ { 2 } ( 1 2 . 7 , - 4 ) , A _ { 3 } ( - 2 3 . 8 , - 4 )$ , and $A _ { 4 } ( - 6 1 . 8 , - 4 )$ . Moreover, we find there is a particular phenomenon that ImpinJ reader always report the $\theta ^ { \prime } =$ $2 \pi - \theta$ instead of θ, which does not exactly conform to its manual. That is why the phase decreases as the distance increasing in Figure 5. However, that does not affect our theoretical analysis and experiment results. In the following experiments, we always use the revised $\theta = 2 \pi - \theta ^ { \prime }$ .

![](images/1995ab6ec42ca3321b5ccd5da3b5025730826dd64436eb8121cdb3fe85e93170.jpg)



Fig. 11. Ranging error

Metrics: We use the error (cm) to indicate the position accuracy, which is an absolute metric. We also employ another important metric called Receiver Operating Characteristic (ROC) curve to measure the relative accuracy. The vertical axis of ROC curve is the the true positive rate (TPR) which is the total number of detected true positives divided by the number of real positives in ground truth. The horizontal axis is the false positive rate (FPR). The FPR is termed as the rate of number of false positives to the total number of negative events in ground truth.

Baseline: We compare BackPos with three baseline schemes, all of which are reference tags based methods. (i) Landmarc [1]. Its basic idea is to calculate the weighted average of the four nearest tag’s locations. The weights are determined by the their RSS values. We deploy the reference tags with the interval of 1m in the office room $( 5 \times 8$ reference tags in total). (ii) VIRE [2]. Another modified RSS based method, which employs some virtual reference tags aiming to eliminate the influence among these tags. (iii) PinIt [8]. PinIt calculates Dynamic Time Warping(DTW) distance between the multipath profile of target and that of reference tags to find the nearest reference tag from target, where the profile is produced through phase array. It estimates the desired tags position by calculating the weighted mean of its nearest neighbors’ positions. The reference tags spacing distance is 1m as well. We build a 8 antennas array with 30cm spacing by a motion robot.

# 7.3 Positioning Accuracy

To measure the absolute positioning accuracy, two experiments are conducted as follows.

# 7.3.1 Accuracy comparision with baseline

In the first experiment, we place a target tag in the position $T ( - 4 3 . 2 , 2 8 3 . 4 )$ ). The distance difference $\Delta d$ from the target tag to four antennas is crucial for hyperbolic positioning. The small errors may have huge consequences. Hence, we firstly check the error of $\Delta d$ in the first experiment. In theory, there are 24 pairs of distance differences among the tag to four antennas. We randomly choose three pairs, $\left| | T A _ { 2 } | - | T A _ { 1 } | \right| ~ = ~ \Delta d _ { 2 , 1 } ~ = ~ \Delta d _ { 1 , 2 } ~ = ~ - 1 0 . 9 ,$ $\left| \left| T A _ { 3 } \right| - \left| T A _ { 2 } \right| \right| = \Delta d _ { 3 , 2 } = - 6 . 8 2 \mathrm { a n d } \left| \left| T A _ { 4 } \right| - \left| T A _ { 3 } \right| \right| =$ $\Delta d _ { 4 , 3 } = - 0 . 1 6$ . We use the measured phases to calculate their differences based on Equation 8 or 9. The experiment repeats for 100 times and the CDF of the ranging error is shown in Figure 11. From the figure, we can see that the maximum error is less than 1cm, which suggests the phase is indeed an excellent indicator for ranging once again. Interestingly, the error of $\Delta d _ { 2 , 1 }$ is greater than that of $\Delta d _ { 4 , 3 }$ on average. In geometry, the $T$ is closest to the $A _ { 4 }$ but farthest to the $A _ { 1 }$ . We think such phenomenon may come from the assumption that the antenna can be considered as geometrical point. In fact, when the tag is off the antenna’s central axis, the EM may emit from the antenna’s edge instead of its geometrical center, leading to a small measurement error in ground truth. Even so, we think the error is small enough to be tolerant in practice.

![](images/ac9dd73f182c881ee056e23204f29e40af76d6f01b0610037b3f00c0269cb7d9.jpg)



Fig. 12. Positioning error: reference tags spacing distance is 1m.

Second, we compare final positioning accuracy of Back-Pos with baseline methods. We randomly choose 100 positions in the feasible region and locate them through four methods in turns. Figure 12 plots the CDF of position error of all final results from BackPos, PinIt, Landmarc and VIRE. The error is defined as the Euclidean distance between the ground truth and measured positions. From the figure, we observe that the phase based positioning is indeed far better than any of RSS based methods. Their errors are not in an order of magnitude even. The mean error of BackPos equals 12.8cm and that of PinIt is 56.4cm while the other two methods’ mean errors are around 100cm. VIRE seems a little better than LANDMARC, gaining the benefits from the virtual tags. In addition, accuracy of other three methods depend on the density of deployed reference tags. Accuracy of PinIt improves to be 20.3cm when we deploy the reference tags by 50cm spacing in this experiment. However, we deployed 160 tags and measured their positions before evaluation. It is no doubt a large amount of overhead, while it does not exist in BackPos. We believe the 12.8cm error is sufficient for major applications because the size of tagged object is bigger than the error. For example, the height of a bottle of Coke is 23cm, the width of a usual milk carton is 20cm, the size of A4 paper is $2 1 c m \times 3 0 c m$ , etc. Furthermore, we found the results of VIRE and LANDMARC are very unstable. Unlike the BackPos whose error sharply concentrates on its mean value with about 3.8cm variance, VIRE and LANDMARC’s errors respectively vibrate in 31.2cm and 48.6cm.

![](images/f0ea84982679e85004dae14a09a9759bf0e4d8df823ed660bb156ba3bbafa0e7.jpg)



Fig. 13. Positioing vs. positions

![](images/55bf3b49fe653447c34372dd01b535b796a7491f1325def05e33d9ef0ac3b090.jpg)



Fig. 14. Error CDF in positions

# 7.3.2 Accuracy comparision in different positions

In the second experiment, we consider the multiple positions. There are total 9 tags deployed in a circle as shown in Figure 13. In the figure, the ground truth is marked as $\cdot _ { \times } ,$ . Note that the circle does not look smooth because the axes are distorted for unified layout. We also plot the error CDF of these positions in Figure 14. We observe that (1) the error has a little difference among the positions. Generally speaking, the points closer to the antenna arary has a smaller error compared with the farther ones. For example, $T _ { 1 }$ has a mean error of 5.3cm while that of $T _ { 5 }$ is 11cm. The variance behaves the same pattern. They are 4.2cm and 5.6cm for $T _ { 2 }$ and $T _ { 9 }$ but 6.4cm for $T _ { 6 }$ . This observation can be explained as follows. The tag located at the farther position harvests fewer energy. Correspondingly, its backscattered signals are so weak that the reader has more difficulties to solve them, leading to the growth of the error. (2) the error mainly comes from the y-axis instead of x-axis. The latter is highly clustered its mean value. This is because the eccentricity of our hyperbola is very big, which means a little x-value will incur a large y-value. In other words, the error in y-axis is augmented due to that of $x \mathrm { - }$ axis.

![](images/d7a35d00b4523347eb4ffdd8670b72a5c33def4140437bdba6331177009b143f.jpg)



Fig. 15. Positioning sensitivity: reference tags spacing distance is 1m.

# 7.4 Positioning Sensitivity

Besides the absolute accuracy, we may pay more concerns at the relative accuracy sometimes. For example, we do not want to place the poison and foods together or mix the cat food with a hamburger. In these scenarios, we need an alert when two target objects are placed too close. Here, we employ the ROC curve to represent such relative accuracy. The experiment is conducted as follows. For a given operating parameter $l ,$ we perform two tests to measure a pair of TPR and FPR. In the first test, we place two tags $T _ { 1 }$ and $T _ { 2 }$ in a spacing of $l / 2 ,$ , then measure the distance between $T _ { 1 }$ and $T _ { 2 } .$ If $| T _ { 1 } T _ { 2 } | < l ,$ , a true positive event is recorded. The TPR is output after the test is repeated for 100 times. In the second test, we change their spacing to 1.5l. If $| T _ { 1 } T _ { 2 } | > l ,$ , a true negative event is recorded. The test is also repeated for 100 times to get a FPR. During the experiment, the parameter l varies from 6cm to 120cm with an increase of 2cm. Finally, we draw the ROC in Figure 15. The results of LANDMARC and VIRE are depressed because they behave as a random guessing, while PinIt has a better performance than them. For BackPos, the FPR is around 40% when the l is too small. As when the l over than 15cm, this is almost no any false positives occurred.

# 7.5 Positioning Diversity

Tag’s diversity is one of the serious issues in RFID positioning. We use the phase difference to eliminate this factor. To validate its impact on the three methods, we perform the positioning on two models of tags, ‘Square’ and $^ { 6 } 2 \times 2 ^ { , }$ . These two models have different antenna size and shape. We plots the comparison in Figure 16. The results show that the tag’s diversity has very little impact on the accuracy of BackPos and PinIt. However, it takes much on the other two methods. In whole, the $^ { 6 } 2 \times 2 ^ { 5 }$ has a bigger antenna size being more easily to absorb the EM from reader hence its RSS may be more sensitive to the positions and owns a relative higher accuracy.

![](images/f4d93958bc5599a246844bdcbdafbd96bf35f5098d4f3f496292708fec1a7b84.jpg)



Fig. 16. Impact of tag diversity

# 8 CONCLUSION

Fine-grained anchor-free positioning is an important task in RFID backscatter system. In this paper, we study characteristics of phase and propose BackPos, an accurate positioning system in backscatter systems based on phase difference. We implement a prototype of BackPos with COTS RFID products and conduct comprehensive evaluations. The results show that BackPos achieves mean accuracy of 12.8cm with variance of 3.8cm. We believe this is a practical positioning system for various RFID applications.

# ACKNOWLEDGEMENT

This work is supported in part by the China National Funds for Distinguished Young Scientists Program 61125202, National High-Tech R&D Program of China (863) under grant No.2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200. And we acknowledge the support from the codes of USRP2reader from the Open RFID Lab (ORL) project [29].

# REFERENCES

[1] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “Landmarc: indoor location sensing using active rfid,” Wireless networks, vol. 10, no. 6, pp. 701–710, 2004.   
[2] Y. Zhao, Y. Liu, and L. M. Ni, “Vire: Active rfid-based localization using virtual reference elimination,” in Proc. of IEEE ICPP, 2007.   
[3] C. Wang, H. Wu, and N.-F. Tzeng, “Rfid-based 3-d positioning schemes,” in Proc. of IEEE INFOCOM, 2007.   
[4] A. Bekkali, H. Sanson, and M. Matsumoto, “Rfid indoor positioning based on probabilistic rfid map and kalman filtering,” in Proc. of IEEE WiMob, 2007.   
[5] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie, “New measurement results for the localization of uhf rfid transponders using an angle of arrival (aoa) approach,” in Proc. of IEEE RFID, 2011.   
[6] Y. Zhang, M. G. Amin, and S. Kaushik, “Localization and tracking of passive rfid tags based on direction estimation,” International Journal of Antennas and Propagation, 2007.   
[7] S. Sen, J. Lee, K.-H. Kim, and P. Congdon, “Avoiding multipath to revive inbuilding wifi localization,” in Proc. of ACM MobiSys, 2013.   
[8] D. K. Jue Wang, “Dude, where’s my card? rfid positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.

[9] M. Bouet and G. Pujolle, “A range-free 3-d localization method for rfid tags based on virtual landmarks,” in Proc. of IEEE PIMRC, 2008.   
[10] P. V. Nikitin, R. Martinez, S. Ramamurthy, H. Leland, G. Spiess, and K. Rao, “Phase based spatial identification of uhf rfid tags,” in Proc. of IEEE RFID, 2010.   
[11] G. Li, D. Arnitz, R. Ebelt, U. Muehlmann, K. Witrisal, and M. Vossiek, “Bandwidth dependence of cw ranging to uhf rfid tags in severe multipath environments,” in IEEE RFID, 2011, pp. 19–25.   
[12] B. Sheng, C. C. Tan, Q. Li, and W. Mao, “Finding popular categories for rfid tags,” in Proc. of ACM MobiHoc, 2008.   
[13] L. Yang, J. Han, Y. Qi, and Y. Liu, “Identification-free batch authentication for rfid tags,” in IEEE ICNP, 2010.   
[14] S. Chen, M. Zhang, and B. Xiao, “Efficient information collection protocols for sensor-augmented rfid networks,” in Proc. of IEEE INFOCOM, 2011.   
[15] W. Luo, S. Chen, T. Li, and S. Chen, “Efficient missing tag detection in rfid systems,” in Proc. of IEEE INFOCOM, 2011.   
[16] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, “Season: Shelving inteference and joint identification in large-scale rfid systems,” in IEEE INFOCOM, 2011.   
[17] J. Lim, S. Kim, H. Oh, and D. Kim, “A designated query protocol for serverless mobile rfid systems with reader and tag privacy,” Tsinghua Science and Technology, vol. 17, no. 5, pp. 521–536, 2012.   
[18] Y. Zheng and M. Li, “P-mti: Physical-layer missing tag identification via compressive sensing,” in IEEE INFOCOM, 2013.   
[19] L. Shangguan, Z. Li, Z. Yang, M. Li, Y. Liu, and J. Han, “Otrack: Towards order tracking for tags in mobile rfid system,” IEEE TPDS, 2013.   
[20] Y. Zheng and M. Li, “Zoe: Fast cardinality estimation for large-scale rfid systems,” in IEEE INFOCOM, 2013.   
[21] P. Bahl and V. N. Padmanabhan, “Radar: An in-building rf-based user location and tracking system,” in Proc. of IEEE INFOCOM, 2000.   
[22] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: Zero-effort crowdsourcing for indoor localization,” in Proc. of ACM Mobicom, 2012.   
[23] K. Joshi, S. Hong, and S. Katti, “Pinpoint: Localizing interfering radios,” in Proc. of USENIX NSDI, 2013.   
[24] J. Xiong and K. Jamieson, “Arraytrack: a fine-grained indoor location system,” in Proc. of USENIX NSDI, 2013.   
[25] M. Spirito and A. G. Mattioli, “On the hyperbolic positioning of gsm mobile stations,” in Proc. of IEEE ISSSE, 1998.   
[26] M. A. Spirito, “On the accuracy of cellular mobile station location estimation,” IEEE TVT, vol. 50, no. 3, pp. 674–685, 2001.   
[27] Y. Chan and K. Ho, “A simple and efficient estimator for hyperbolic location,” IEEE Transactions on Signal Processing, vol. 42, no. 8, pp. 1905–1915, 1994.   
[28] D. M. Dobkin, The RF in RFID: passive UHF RFID in practice. Newnes, 2007.   
[29] “Open rfid lab,” http://pdcc.ntu.edu.sg/wands/ORL.

![](images/cd9cf117fd1e689e39b7b0256c30692c900c966ad0500b82f670c561f62b387a.jpg)



Tianci Liu received the BS degree from the School of Sofware at Tsinghua University, China, in 2012. He is now a third year PhD student of School of Software at Tsinghua University, China. His research interests include RFID and sensor network, mobile sensing and computing. He is a student member of IEEE and ACM.

![](images/66f1c86f83aa87648bbd31795547cff4c6e9a3db77783b566a1443092721dea0.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, USA, in 2003 and 2004, respectively. He is now Cheung Kong Professor and Dean of School of Software at Tsinghua University, China. Yunhao is also a member of Tsinghua National Lab for Information Science and Technology. His research interests include RFID and sensor network, the Internet and Cloud Computing, and distributed computing. Yunhao is IEEE Fellow.

![](images/f4c4f510f066c2c619b6edb00fe734c0f1524cac4a2844394c447375c65221d1.jpg)



Lei Yang respectively received the B.S. degree from the School of Software and Ph.D. degree from the Department of Computer Science and Engineering at Xi’an Jiaotong, Shaanxi, China. He is currently a postdoc fellow in the School of Software at Tsinghua University, Beijing, China. His research interests include RFID, pervasive computing, network security, and smart home. He is a member of the IEEE and ACM.

![](images/520e9b421c15a9002f16b3c6ad94da40172a7114d5d5836690163a3c79e6e832.jpg)



Yi Guo received his B.E. degree of Electrical and Computer Engineering from Shanghai Jiao Tong University, Shanghai, China, in 2011. He is currently a Ph.D. student in Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include radio frequency identification (RFID) and pervasive computing. He is a student member of the IEEE and the ACM.

![](images/82f82d0c30fcbcd65426e00c83170ceaf727729e2256937fba460bf43974ce2b.jpg)



Cheng Wang received his PhD degree in Department of Computer Science at Tongji University in 2011. Currently, he is a research professor of Computer Science at Tongji University. His research interests include wireless networking, mobile social networks, and cloud computing.