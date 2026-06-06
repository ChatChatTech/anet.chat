# Anchor-free Backscatter Positioning for RFID Tags with High Accuracy

Tianci Liu $^{*}$ , Lei Yang $^{*}$ , Qiongzheng Lin $^{*}$ , Yi Guo $^{\dagger}$ , Yunhao Liu $^{*}$

\* School of Software and TNLIST, Tsinghua University, China

$^{\dagger}$ Hong Kong University of Science and Technology, Hong Kong

{tian, young, lin, yi}@tagsys.org, yunhao@greenorbs.com

Abstract—RFID technology has been widely adopted in a variety of applications from logistics to access control. Many applications gain benefits from knowing the exact position of an RFID-tagged object. Existing localization algorithms in wireless network, however, can hardly be directly employed due to tag's limited capabilities in terms of energy and memory. For example, the RSS based methods are vulnerable to both distance and tag orientation, while AOA based methods put a strict constraint on the antennas' spacing that reader's directional antennas are too large to meet. In this paper, we propose BackPos, a fine-grained backscatter positioning technique using the COTS RFID products with detected phase. Our study shows that the phase is indeed a stable indicator highly related to tag's position and preserved over frequency or tag orientation, but challenged by its periodicity and tag's diversity. We attempt to infer the distance differences from phases detected by antennas under triangle constraint. Further, hyperbolic positioning using the distance differences is employed to shrink the tag's candidate positions until filtering out the real one. In combination with interrogation zone, we finally relax the triangle constraint and allow arbitrary deployment of antennas by sacrificing the feasible region. We implement a prototype of BackPos with COTS RFID products and evaluate this design in various scenarios. The results show that BackPos achieves the mean accuracy of 12.8cm with variance of 3.8cm.

Keywords—RFID, hyperbolic positioning, BackPos, feasible region

# I. INTRODUCTION

Radio Frequency IDentification (RFID) technology has been widely deployed in recent years. It is no exaggeration to say that we are almost surrounded by RFID tags in daily life. These tags wear different skins, such as credit cards, ID cards, car keys, pass cards etc., and play a key role in assets management, object tracking, access control and logistics. Typically, a RFID system consists of one reader and many tags. Most of them utilize the backscatter radio link for communications. In such link, the tag does not need equipment of battery but modulates their information on the backscattered signals emitted from a reader. A backscatter tag nearby reader changes the impedance match on its own antenna to modulate the reader's signal, in order to convey a message of zeros and ones back to the reader. Many applications gain the benefits from knowing the exact location of an RFID-tagged object. For example, we can quickly check whether the books on certain shelves are out of order, find out the lose credit card with no need of guessing, or pay for the groceries of the person behind.

The traditional localization algorithms in wireless networks are limited for RFID because they have very limited capabil-

978-1-4799-3360-0/14/\$31.00 © 2014 IEEE

ities in terms of energy and memory. The RFID positioning, one of the most important fundamental topics in RFID area, has been received a lot of attentions [1]–[6]. These work can be classified into two groups. (1) Received Signal Strength (RSS) based methods [1]–[4]. These work employ the RSS as an indicator for tag's position. They deploy reference tags with known positions in advance. When applying, k reference tags whose RSS are the most similar to that of target tag are chosen for estimating the target's position. However, their accuracy is challenged because the RSS is not a reliable indicator being vulnerable to fluctuation as environment changes over time. Moreover, the tag's orientation is another fatal factor on RSS, which directly influences its energy absorption from reader. (2) AOA based methods [5], [6]. They employ multiple antennas to receive the tag' signals and estimate their angles through the phase differences from the tag to these antennas. These methods need to put a strict constraint on the antennas' spacing ( $\leqslant \lambda/2$ ) that reader's directional antennas are too large ( $25 \times 25cm^{2}$ ) to meet.

In this paper, we introduce a fine-grained backscatter positioning technique, called BackPos, without need of reference tags. We conduct a serial of empirical studies to show that the phase exhibits a reliable indicator highly related to tag's position, and preserved over frequency or tag orientation. More important, the phase reveals a stable linear relation to the distance within half a wavelength. With combination of these characteristics, we attempt to position a target tag using the phase. However, this idea is challenged by two factors: (i) Each tag has a small but different unknown initial phase rotation $\theta_{Tag}$ , related to its unique antenna on the board, which contributes to the reader's measured phase $\theta$ . We should carefully tackle the measurement error coming from such diversity. (ii) The phase is periodic such that the linear relation with distance behaves effective within half a wavelength only, increasing the position ambiguity. We should find a way to eliminate this uncertainty.

Our basic idea is to infer the distance difference $\Delta d$ from a target tag to two antennas using the phase difference $\Delta\theta$ . The ambiguity coming from phase periodicity can be dispelled by a triangle constraint that deploying two antennas within a half of wavelength ( $<\lambda/2$ ). In this situation, the $\Delta d$ can be determinately formalized as a piecewise equation with parameter of $\Delta\theta$ . Then the hyperbolic positioning is employed to locate the target tag. In detail, a hyperbola can be draw up using one $\Delta d$ , on which the points are the candidate positions of target tag. To narrow the uncertainty, multiple hyperbolas are required. As a result, target position is released on the their common intersection. Nevertheless, it is hard to meet the spacing constraint in UHF RFID as stated before. Reconsidering this issue, we observe that the interrogation zone of RFID is actually narrowed in a lobe, beyond which the targets cannot be interrogated even. We do not need care about these non-interrogation regions when positioning. Motivated by this observation, we construct a virtual hyperbola C focusing on two antennas with arbitrary spacing and let the distance difference be $\lambda/2$ . We strictly prove that the positions in the region among the two branches of C, termed as feasible region, still meet the triangle constraint. That is to say, the points in feasible region are positionable. We believe it is acceptable to relax the spacing constraint through sacrificing the feasible region due to the existence of interrogation zone.

Our approach has three major merits. (i) It is anchor-free as well as without need to deploy any infrastructure in advance, thereby it is very convenient to use in practice. (ii) Most of methods with high accuracy [7], [8] take an analysis on the PHY signals which is beyond the support from a Commercial Off-The-Shelf (COTS) reader. Instead, our approach does not require extra information from reader or tag, being in favor of COTS RFID products. (iii) Thanks to phase difference, no need to measure the initial phase rotation $\theta_{TAG}$ , greatly extending its usage scope.

In summary, this paper makes the following contributions:

- We extensively conduct statistical analysis of phase collected from COTS products, showing that the phase is indeed a reliable indicator for tag positioning, preserved over frequency and tag orientation.   
- We propose a fine-grained positioning technique for backscatter system, called BackPos, with regarding to the tag's limited capabilities in terms of energy and memory as well as its diversity. To our best knowledge, we are the first to introduce the interrogation zone to the tag positioning, based on which the triangle constraint can be relaxed to a reasonable level.   
- We implement a prototype of BackPos using ImpinJ R420 reader and EPC Gen2 tag. The evaluation results show that the mean position error is around 12.8cm with a samll standard variance of 3.8cm.

The remainder of the paper is structured as follows. We introduce the background and conduct empirical studies in Section II. The main design of BackPos is presented in Section III. We discuss additional details in Section IV. The implementation and evaluation is given in Section V. We overview related works of this paper in Section VI. Finally, Section VII concludes the paper.

# II. PRELIMINARIES

In this section, we introduce the technical background on RFID system and also conduct a serial of empirical studies on the characteristics of phase in backscatter link.

# A. Backscatter Radio Link

Passive tags not equipped with batteries do not use a radio transmitter. Instead, they use modulation of the reflected power from the tags. Figure 1 provides a conceptual diagram of the radio wave propagation between an RFID reader and a passive

![](images/ce0ca73e06578fbed0d21bb5d09fabaa00ada8802ba1913b811a0fac14d141c6.jpg)



Fig. 1. Backscatter communication

RFID tag. The backscatter radio link can be simply understood. The current flow on a reader' antenna induces to a voltage on the tag's antenna. This induced current is no different from the current on the tag's antenna that started thing in the first place: it leads to radiation. The radiated wave can make its way back to the reader's antenna, induce a voltage, and therefore, produce a signal that can be detected: a backscattered signal. A typical UHF reader has 50 channels in the $902 \sim 928z\mathrm{MH}$ ISM band. In addition, the interrogation range of UHF reader is from a few meters up to tens of meters. Generally speaking, the range size is proportional to the power of reader's antenna. Our approach can well accommodate these specifications.

# B. RF Phase

For an RF carrier wave at frequency $f$ (Hz), the relation between frequency $f$ and wavelength $\lambda$ is given by $\lambda = \frac{c}{f}$ where $c$ is the speed of the EM wave being equal to the speed of light ( $\approx 3 \times 10^{8} m/s$ ). The total distance traversed by the backscattered signal is $2 \times d$ as shown in Figure 1. In addition to the RF phase rotation over distance, the reader's transmit circuits, the tag's reflection characteristic, and the reader's receiver circuits will all introduce some additional phase rotation, termed $\theta_{T}$ , $\theta_{TAG}$ , and $\theta_{R}$ . Hence, the total phase rotation can be expressed as

$$
\theta + 2 k \pi = 2 \pi \frac {2 d}{\lambda} + \theta_ {T} + \theta_ {R} + \theta_ {T A G} \tag {1}
$$

where $\theta$ is an output parameter supported by a common COTS reader, and k is an integer guaranteeing the value of $\theta$ falling within $[0,2\pi)$ . Note that, k is an unknown parameter in practise. The $\theta_{R}$ and $\theta_{T}$ are constant parameters relevant to the characteristics of reader, which can be referred in reader's manual. Although the $\theta_{TAG}$ is another constant parameter relevant to the tag, we have no way to measure them ahead because there exist tens of thousands of tags in practice. It becomes a big practical challenge for us.

# C. Empirical Studies

We firstly conduct a serial of empirical studies using a COTS ImpinJ reader and a Alien tag. These experiments are designed towards verifying the following three hypotheses that need to hold while using phase as indicator for tag positioning.

Hypothesis 1: The phase appears random, but actually exhibits a stable statistical structure. This structure is preserved over frequency changes.

In the first experiment, the target tag is placed in front of a reader's antenna over distance of $1.3m$ . We keep the tag's position unchanged but hop the frequency during 16 available channels. Figure 2 shows the PDF of phase interrogated at different channels. For visual clarity, only three of them are displayed and the others are similar. In the figure, the results are plotted using histograms and fitted using solid curves. We can see that the phase actually follows a Gaussian distribution deviating among $\sim 5.7^{\circ}$ . Such a small phase error leads to a very tiny ranging error ( $\sim 5.7 / 360 * 16.5cm = 0.26cm$ ), which is an acceptable level.

![](images/60467e828fe644cf57e7be469e42ff48e9c7f3e68061a9a2165904a75e0dd3ca.jpg)



Fig. 2. Phase vs. Frequency

![](images/6a858d21ee95e26187ebebda9d118666132a786f0a96aed54c7ec75f317a84b5.jpg)



Fig. 3. Phase vs. Orientation

![](images/2c192309e56466eb80be476ac4d0e5f8a2f4e5510bd34fefad4111c526475bcf.jpg)



Fig. 4. Phase vs. Distance

Hypothesis 2: The phase is irrelevant to tag orientation once the tag's position remains unchanged.

The second experiment involves the tag orientation, defined the angle between the tag and the antenna's polarization orientation. We fix the frequency at the fifth channel but change the tag's orientation from $0^{\circ}$ to $360^{\circ}$ . Figure 3 shows the results at 8 orientations. We can see that almost all measured phases remain at a same level ( $\sim 200^{\circ}$ ).

Hypothesis 3: The measured phase has a linear relation to the distance within an intra-wave and a stable periodicity at inter-wave.

This hypothesis is the foundation of backscatter positioning. In the third experiment, we attach the target tag on a toy train and let it move away from the antenna at a uniform linear motion. The timestamp when the tag is interrogated, is used to calculate the distance. The result is plotted in Figure 4. In the figure, we can see that the experimental results well match the theory. According to Equation 1, the phase should repeat from 0 to $2\pi$ every half wavelength ( $\frac{\lambda}{2} \approx 16.5cm$ ). In the figure, the measured cycle is about $17cm$ , very close to theoretical value. In addition, the linear relation and its periodicity are expected to remain stable $^{1}$ .

Clearly, all of three experiments yield our hypotheses. The phase indeed a reliable indicator for tag's position.

# III. BACKPOS

In this section, we present our backscatter positioning approach, called BackPos, and gradually introduce its technical details later.

# A. Basic Idea

Although the phase is an appealing indicator for accurate ranging within half a wavelength as stated, there exist two serious uncertainties affecting the phase for positioning. The first is that the phase is periodic such that there exists a candidate position once every a propagating cycle. The second uncertainty is that the we have no idea about the initial rotation $(\theta_{TAG})$ for every tag and no way to infer the distance d from the $\theta$ reported by the reader based on Equation 1.

We notice that a common COTS reader usually has four directional antennas. They can be collaboratively used for eliminating above two uncertainties. Suppose we have two antennas, $A_{1}(x_{1},y_{1})$ and $A_{2}(x_{2},y_{2})$ , available to interrogate the target tag $T(x,y)$ , and their distances from the tag to the two antennas are $|TA_{1}|=d_{1}$ and $|TA_{2}|=d_{2}$ . Assuming the phase results are $\theta_{1}$ and $\theta_{2}$ measured by $A_{1}$ and $A_{2}$ , we can get two equations based on Equation 1 as follows.

$$
\theta_ {1} + 2 k _ {1} \pi = 2 \pi \frac {2 d _ {1}}{\lambda} + \theta_ {T _ {1}} + \theta_ {R _ {1}} + \theta_ {T A G} \tag {2}
$$

$$
\theta_ {2} + 2 k _ {2} \pi = 2 \pi \frac {2 d _ {2}}{\lambda} + \theta_ {T _ {2}} + \theta_ {R _ {2}} + \theta_ {T A G} \tag {3}
$$

Subtracting above equations, we have

$$
\Delta \theta_ {2, 1} + 2 (k _ {2} - k _ {1}) \pi = \frac {4 \pi}{\lambda} \Delta d _ {2, 1} + \rho \tag {4}
$$

where $\Delta \theta_{2,1} = \theta_2 - \theta_1$ , $\Delta d_{2,1} = d_2 - d_1$ and $\rho = (\theta_{T_2} - \theta_{T_1} + (\theta_{R_2} - \theta_{R_1})$ . Removing the subscripts, the equation can be simplified as

$$
\Delta d = \frac {\lambda}{4 \pi} (\Delta \theta + 2 k \pi) \tag {5}
$$

where k is a new integer ensuring $\Delta\theta = (\Delta\theta_{2,1} - \rho)$ within $(-2\pi, 2\pi)$ . $\rho$ is a constant term. From Equation 5, the unknown constant term of $\theta_{TAG}$ is naturally wiped out thereby the impact of tag's diversity is eliminated. Suppose the $\Delta d$ is able to be inferred from $\Delta\theta$ , can we reveal the target position? The answer is yes. As well known, a hyperbola is a curve being composed of the locus of points for which the difference of the distances from two given fixed points is a constant. Therefore, once knowing $\Delta d$ , we can construct such a hyperbola that focuses on the two antennas' positions and formalized as follows:

$$
| \sqrt {(x - x _ {1}) ^ {2} + (y - y _ {1}) ^ {2}} - \sqrt {(x - x _ {2}) ^ {2} + (y - y _ {2}) ^ {2}} | = \Delta d
$$

If we establish coordinate system enabling the two focuses locating in x-axis and the origin coinciding with their centers, above equation can be simplified to:

$$
\frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \text {   where   } \left\{ \begin{array}{l} a = \Delta d \\ b = \sqrt {c ^ {2} - a ^ {2}} \\ c = \sqrt {(x _ {1} - x _ {2}) ^ {2} + (y _ {1} - y _ {2}) ^ {2}} / 2 \end{array} \right.
$$

![](images/5d0331b71ff34addf58e468aa7fba236ac99d59df2ebd06ea842bcfeca3f295f.jpg)



Fig. 5. Triangle constraint

![](images/d80bcfddf04c493a2070556c1a9ba2354f4be77295d01911c22dd4e58692c99e.jpg)



Fig. 6. Feasible region

![](images/4feb1c1216cccb5845c9ea11d239bf0536d57feb4b5c64a8111d1e76e9416827.jpg)



Fig. 7. Hyperbolic positioning

In this way, the target tag's position is confined on the curve. Further, when multiple hyperbolas are constructed via multiple $\Delta d$ , the target's 2D or 3D position $^{2}$ can be discovered on the their common intersection.

Although the hyperbolic positioning is able to reveal the target position using enough antennas, we still confront three uncertainties. (1) The first comes from the ambiguous relationship between $\Delta d$ and $\Delta\theta$ due to the phase periodicity. The latter cannot directly induce the former. This will lead to numerous possible candidates. We need find a way to filter out the real one. (2) The second uncertainty is that every hyperbola has two branches which may raise the possible intersections as the number of hyperbola increases, even if we exactly known the distance difference. (3) The hyperbolic equation is too complex to find a analytical solution when there are many combined equations [9]. The common method is to seek an inaccurate numerical solution, which may further contribute to the position error. Instead, we want to leverage the feature of directional antenna and specific deployment method to solve an analytical solution. Next, we are going to gradually address these issues.

# B. Finding the feasible region

From Equation 5, the distance difference is actually a large set due to the periodicity. At a first glance, it seems impossible to filter out the real one. However, we observe three important facts in practice, aiding us to carefully exclude the incorrect ones.

Fact 1 (Triangle Constraint): The fact is that the $\Delta d$ is deterministic when two antennas are deployed within a spacing of half a wavelength.

Suppose two antennas $A_{1}$ and $A_{2}$ are deployed within a spacing of half wavelength as illustrated in Figure 5, the distance difference $\Delta d$ from the target tag T to two antennas meets the following inequation:

$$
\left| \Delta d \right| = \left| d _ {2} - d _ {1} \right| <   \frac {\lambda}{2} \tag {6}
$$

Above inequality can be easily proved by the triangle inequality. Substituting Equation 5 into Inequation 6, we can obtain

$$
| \Delta d | = \left| \frac {\lambda}{4 \pi} \Theta + \frac {\lambda}{2} k \right| <   \frac {\lambda}{2} \tag {7}
$$

where $-2\pi < \Theta < 2\pi$ .

In a particular instance, the $\Theta$ can be calculated using the reader output $\theta$ and its transceiver characteristic's $\rho$ . Considering the sign of $\Theta$ , there exist two cases:

(1) Assuming $0 \leq \Theta < 2\pi$ , there are two subcases. (i) if $\Delta d = d_2 - d_1 \geq 0$ , the target is closer to $A_1$ than $A_2$ , then $k$ must equal 0 to ensure $0 \leq \frac{\lambda}{4\pi}\Theta + \frac{\lambda}{2}k < \frac{\lambda}{2}$ holding true. Therefore $\Delta d = \frac{\lambda}{4\pi}\Theta$ . (ii) contrary to the first subcase, if $\Delta d < 0$ , the target is closer to $A_2$ than $A_1$ . The $k$ must equal $-1$ to ensure $-\frac{\pi}{2} \leq \frac{\lambda}{4\pi}\Theta + \frac{\lambda}{2}k < 0$ . Hence, $\Delta d = \frac{\lambda}{4\pi}\Theta - \frac{\lambda}{2}$ . This case can be summarized as:

$$
\Delta d = \left\{ \begin{array}{l l} \frac {\lambda}{4 \pi} \Theta & \Delta d \geq 0 \\ \frac {\lambda}{4 \pi} \Theta - \frac {\lambda}{2} & \Delta d <   0 \end{array} \right. \tag {8}
$$

In fact, above piecewise expression constitutes a hyperbola which has two different branches.

(2) Assuming $-2\pi \leq \Theta < 0$ , there exist two subcases as well. (i) if $\Delta d \geq 0$ , then k must be 1 to guarantee $0 \leq \frac{\lambda}{4\pi}\Theta + \frac{\lambda}{2}k < \frac{\lambda}{2}$ . Thus, $\Delta d = \frac{\lambda}{4\pi}\Theta + \frac{\lambda}{2}$ . (ii) otherwise $\Delta d < 0$ , then k must be 0 to ensuring $-\frac{\lambda}{2} \leq \frac{\lambda}{4\pi}\Theta + \frac{\lambda}{2}k < 0$ , then k must be 0. Thus, $\Delta d = \frac{\lambda}{4\pi}\Theta$ . This case is summarized as:

$$
\Delta d = \left\{ \begin{array}{l l} \frac {\lambda}{4 \pi} \Theta + \frac {\lambda}{2} & \Delta d \geq 0 \\ \frac {\lambda}{4 \pi} \Theta & \Delta d <   0 \end{array} \right. \tag {9}
$$

This is an another hyperbola with two different halves.

For a particular instance, only one case happens because the $\Theta$ is deterministic. We choose $\lambda/2$ instead of $\lambda$ being the constraint because the wave prorogate double distance in backscatter system. Thanks to triangle constraint, we successfully confine the $\Delta d$ in a deterministic value. However, the triangle constraint behaves too rigid to meet in practice because the wavelength of UHF is very small. For example, if f = 920.625MHz, the spacing between two antennas should be within $\sim 16.3cm$ . Considering the antenna size ( $\sim 25cm \times 25cm$ ), it is impossible to enable any two antennas' spacing within 16.3cm when more than two antennas are used.

Fact 2 (Feasible Region): There always exists a continuous region meeting the triangle constraint even if the spacing of two antennas is greater than $\lambda /2$ . Such region is called feasible region.

Given the spacing between two antennas is $|A_{1}A_{2}| = d_{ant}$ , we can construct such a virtual hyperbola C that the absolute distance difference $|TA_{1} - TA_{2}| = \frac{\lambda}{2}$ for any point T on the curve. The mathematical equation of hyperbola $\mathcal{C}$ is given by

![](images/00adb0f57ce5f2f681ed1f28efe989c4c711bc5d8a1baa3922d5e0e280541827.jpg)



Fig. 8. Interrogation zone $^{3}$

$$
\frac {x ^ {2}}{a ^ {2}} - \frac {y ^ {2}}{b ^ {2}} = 1 \text {   where   } \left\{ \begin{array}{l} a = \frac {\lambda}{2} \\ b = \sqrt {c ^ {2} - a ^ {2}} \\ c = \frac {d _ {\mathrm{ant}}}{2} \end{array} \right.
$$

We claim that the space between the two branches of hyperbola C, the shadow area illustrated in Figure 6, is the feasible region. Next, we strictly prove this statement.

Theorem 1: Let $A_{1}$ and $A_{2}$ be two focus points of a hyperbola with the distance difference of $\Delta d$ . Then, for any point P in the space between two curves of the hyperbola, the inequation $|PA_{1}-PA_{2}|\leq\Delta d$ always holds true.

Proof: Suppose $A_{1}(-x_{0},0)$ , $A_{2}(x_{0},0)$ and $P(x,y)$ , illustrated in Figure 6. Apparently, $\forall P(x=0,y),|PA_{1}-PA_{2}|=0$ . Due to the symmetry, we only need to prove the case that x>0. The same procedure can be proved for the other side x<0. Define $g(x,y)$ be the distance difference for P, namely,

$$
g (x, y) = P A _ {1} - P A _ {2} = \sqrt {(x + x _ {0}) ^ {2} + y ^ {2}} - \sqrt {(x - x _ {0}) ^ {2} + y ^ {2}}
$$

we have

$$
\begin{array}{l} \frac {\partial g (x , y)}{\partial x} = \frac {x + x _ {0}}{\sqrt {(x + x _ {0}) ^ {2} + y ^ {2}}} - \frac {x - x _ {0}}{\sqrt {(x - x _ {0}) ^ {2} + y ^ {2}}} \\ = \Psi^ {- 1} [ \sqrt {(x - x _ {0}) ^ {2} (x + x _ {0}) ^ {2} + y ^ {2} (x + x _ {0}) ^ {2}} - \\ \sqrt {(x - x _ {0}) ^ {2} (x + x _ {0}) ^ {2} + y ^ {2} (x - x _ {0}) ^ {2}} ] \\ \end{array}
$$

where

$$
\Psi = \sqrt {[ (x + x _ {0}) ^ {2} + y ^ {2} ] [ (x - x _ {0}) ^ {2} + y ^ {2} ]} > 0
$$

Because $x \geq 0$ , $y^{2}(x + x_{0})^{2} \geq y^{2}(x - x_{0})^{2}$ . Therefore,

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

In addition, $\forall P(x,y)|x\geq 0,\exists P'(x',y)$ in the hyperbola $(P'A_{1} - P'A_{2} = \Delta d)$ , making:

$$
x ^ {\prime} > x > 0
$$

Combine with Inequation 10, we get $g(x', y) > g(x, y)$ . That is $|PA_1 - PA_2| < \Delta d$ .

When applying, we can coarsely estimate the target position firstly and then adjust the antennas' deployment for ensuring the target falling in the feasible region. In order to assist the adjustment, we approximate the feasible region $D_{\mathrm{abcdef}}$ using curve $C$ 's the asymptotic line and formalize it as follows.

$$
y = \left\{ \begin{array}{l l} - \frac {b}{a} x & x \leq - a \\ 0 & - a <   x \leq a \\ \frac {b}{a} x & x > a \end{array} \right. \tag {11}
$$

Substituting $(d_{\mathrm{ant}},\frac{\lambda}{2})$ into that function, we get:

$$
D = \{(x, y) | y \geq \left\{ \begin{array}{l l} - \frac {\sqrt {d _ {\mathrm{ant}} ^ {2} - (\lambda / 2) ^ {2}}}{\lambda / 2} x & x \leq - \frac {\lambda}{4} \\ 0 & - \frac {\lambda}{4} <   x \leq \frac {\lambda}{4} \\ \frac {\sqrt {d _ {\mathrm{ant}} ^ {2} - (\lambda / 2) ^ {2}}}{\lambda / 2} x & x > \frac {\lambda}{4} \end{array} \right. \tag {12}
$$

Region D is the feasible region that enabling our approach feasible when the target locates there.

Fact 3 (Interrogation Zone): The reader usually employs the directional antennas in order to increase the energy received by the tag.

The feasible region is a trade-off that balances the realizability and the practical deployment. We think such a trade-off is reasonable because the interrogation zone is narrowed in a lobe, as shown in Figure 8, being similar to our feasible region. Considering the main lobe as a cone, the beam angle $\theta_{\mathrm{lobe}} \approx \sqrt{\frac{4\pi}{G}}$ . If we need the signal gain $G$ be $5dB$ , $\theta_{\mathrm{lobe}}$ would be about $90^{\circ}$ . We plot two antennas' interrogation zones in Figure 5. They are sector $D_{CA_1F}$ and sector $D_{EA_2D}$ . The target in the shadow area can be interrogated as well as positioned by both antennas. Clearly, the common interrogation zone is smaller than the feasible region in fact. Therefore we think feasible region is acceptable in practice.

# C. Hyperbolic Positioning

We filter out a piecewise distance difference $\Delta d$ so far. With this piecewise model, we can plot an unsymmetrical hyperbola owning two different branches. For example, the hyperbola focusing on antenna $A_{1}$ and $A_{2}$ , have two halves of $c_{1}$ and $c_{3}$ , illustrated in Figure 7. In theory, there appears $\binom{n}{2}$ such hyperbolas given any n antennas. Their common intersection of these curves is indeed our target position.

An example shown in Figure 7 is displayed here to show how the hyperbolic positioning works. Let T be the target in a common feasible region of three antennas $A_{1}$ , $A_{2}$ and $A_{3}$ . All these directional antennas are deployed to interrogate the north area. Suppose the measured phase differences are $\Delta\theta_{A_{1},A_{2}}>0$ and $\Delta\theta_{A_{2},A_{3}}<0$ . Then the first piecewise hyperbola contributed by antenna $A_{1}$ and $A_{2}$ is represented:

- Curve $c_{1}$ : the west branch of the hyperbola with distance difference $|TA_{1}| - |TA_{2}| = \Delta d_{1,2} = \frac{\lambda}{4\pi}\Theta_{1,2} - \frac{\lambda}{2}$ .   
- Curve $c_3$ : the east branch of the hyperbola with distance difference $|TA_2| - |TA_1| = \Delta d_{2,1} = \frac{\lambda}{4\pi}\Theta_{1,2}$ .

The second piecewise hyperbola comprised by antenna $T_{2}$ and $T_{3}$ is represented:

- Curve $c_{2}$ : the west branch of the hyperbola with distance difference $|TA_{2}| - |TA_{3}| = \Delta d_{2,3} = \frac{\lambda}{4\pi}\Theta_{2,3}$ .   
- Curve $c_4$ : the east branch of the hyperbola with distance difference $|TA_3| - |TA_2| = \Delta d_{3,2} = \frac{\lambda}{4\pi}\Theta_{2,3} + \frac{\lambda}{2}$ .

From the figure, we can see that six intersections are released from the four curves. Since the antennas are directional, the negative direction of $y$ -axis is abandoned. Finally, we get candidate set $R = \{T_1, T_2, T_3\}$ at worst case through solving the two combined hyperbolic equations. We say that is the worst case, because there may be no intersection between $c_1$ and $c_2$ when the curve $c_1$ has greater hyperbolic eccentricity than $c_2$ . The similar case happens between $c_3$ and $c_4$ . The best case occurs only when one intersection $T_1$ exists between $c_2$ and $c_3$ , then $T = T_3$ .

If $|R| > 1$ , then we need extra effort to eliminate the uncertainty. There are two methods. One method is to construct another piecewise hyperbola through the phase difference from target T to antenna $A_{1}$ and $A_{3}$ . Utilizing the third hyperbolic, we can get another candidate set $R'$ . However, such a method may be impractical because the area of feasible region decreases as the distance $d_{ant}$ increases based on Equation 12. The distance $d_{ant}$ between $A_{1}$ and $A_{3}$ is twice as much as that of $A_{1}$ and $A_{2}$ , which may narrow the feasible region in a small centrum and cause the target out of the region. The second method is to deploy the fourth antenna $A_{4}$ in the east of antenna $A_{3}$ for constructing the new hyperbola. The new candidate set $R'$ can be obtained by antenna $A_{2}$ , $A_{3}$ and $A_{4}$ . We think the second method is more practical because a common COTS usually has four antennas. Finally the real target position is revealed by $T = R \bigcap R'$ .

In practice, there may be no exact intersection between set $R$ and $R'$ due to the measurement noise. In this situation, we advise to employ the average positions of the nearest two points as the target position, formalized as follows.

$$
T = \frac {T _ {1} + T _ {2}}{2} \text {   where   } (T _ {1}, T _ {2}) = \underset {T _ {i} \in R, T _ {j} \in R ^ {\prime}} {\operatorname{argmin}} | | T _ {i} - T _ {j} | | \tag {13}
$$

# D. Solving hyperbolic equations solution

The kernel of hyperbolic positioning is to seek the solution from a group of combined equations. The usual way is to employ numerical methods, like Steepest Descent and Newton-Raphson, to solve equations. However, These methods' outputs are just approximate. Their accuracy fully depends on times of iterations. More accurate solution requires more iterations as well as more computation resource. Here, we leverage two characteristics, antenna's directionality and horizontal deployment, to pursuit analytical solution.

As illustrated in Figure 7, three antennas are arranged at X axis, which are focus points of positioning hyperbolas. For this reason, four hyperbolic curves are shifted from standard hyperbolas along X axis. Take $c_{1}$ and $c_{2}$ in Figure 7 for example, the hyperbolic equations are:

$$
\left\{ \begin{array}{l} \frac {(x - h _ {1}) ^ {2}}{a _ {1} ^ {2}} - \frac {y ^ {2}}{b _ {1} ^ {2}} = 1 \\ \frac {(x - h _ {2}) ^ {2}}{a _ {2} ^ {2}} - \frac {y ^ {2}}{b _ {2} ^ {2}} = 1 \end{array} \right. s. t \left\{ \begin{array}{l} x <   \min (h _ {1}, h _ {2}) \\ y \geq 0 \\ a _ {i} = \frac {\triangle d _ {i}}{2} \\ c _ {i} = \frac {d _ {\text {ant, i}}}{2} \\ b _ {i} = \sqrt {c _ {i} ^ {2} - a _ {i} ^ {2}} \end{array} \right. \tag {14}
$$

where h is the middle point of two focus points, a and b are semi-minor parts of real axis and imaginary axis, respectively. We get a key observation that, both xy and y component do not exist that quadratic equations. Hence, we can combine two equations to eliminate $y^{2}$ component. Namely, the dual quadratic group is transformed into a quadratic equation of x:

$$
\left(\frac {b _ {1} ^ {2}}{a _ {1} ^ {2}} - \frac {b _ {2} ^ {2}}{a _ {2} ^ {2}}\right) x ^ {2} - 2 \left(\frac {b _ {1} ^ {2}}{a _ {1} ^ {2}} h _ {1} - \frac {b _ {2} ^ {2}}{a _ {2} ^ {2}} h _ {2}\right) x + \frac {b _ {1} ^ {2}}{a _ {1} ^ {2}} h _ {1} ^ {2} - \frac {b _ {2} ^ {2}}{a _ {2} ^ {2}} h _ {2} ^ {2} - \left(b _ {1} ^ {2} - b _ {2} ^ {2}\right) = 0 \tag {15}
$$

Now, we can use single variable quadratic solution formula to get analytical expression of x from Equation 15 and substitute it into Equations 14 to get y.

The reason why we have analytical expression of variable x and y, is that we lay antennas in a line, which will be in X axis. In this case, there are no xy and y components in all hyperbola expressions. As a result, variable x can be completely eliminated by combining two expressions. Besides, if we do not arrange antennas in a straight line, the feasible region intersection of $D_{i}$ of each antenna couple would be a narrow and close domain. Obviously, an open and broad region where objects can be positioned is what we expect. Based on these two advantages, BackPos arranges antennas in a straight line, four antennas more specific.

# E. Summary

Being different from the traditional AOA methods, our approach focuses on the features of backscatter systems and leverage them to aid our positioning. In this section, we present the details of BackPos and address the following research issues: (1) how to induce the distance difference from the measured phase difference. (2) how to relax the triangle constraint, free the antenna deployment, but still remain the capability of revealing expected distance difference. (3) how to conduct the hyperbolic positioning with a group of combined piecewise hyperbolic equations. (4) At last, we also give rather accurate analytical solution for the equations.

# IV. DISCUSSION

In this section, we attempt to answer some practical issues.

# A. Why choose $\frac{\lambda}{2}$ as distance difference constraint?

BackPos uses $\frac{\lambda}{2}$ as the difference constraint to induce a hyperbola with two different branches. Actually, the reasonable choice is to set the constraint as $\frac{\lambda}{4}$ . In this case, k must be 0 to ensure the $|\Delta d| = |\frac{\lambda}{4\pi}\Theta + \frac{\lambda}{2}k| < \frac{\lambda}{4}$ . Then $|\Delta d| = |\frac{\lambda}{4\pi}\Theta|$ and the hyperbola has a pair of symmetrical branches. However, this choice will cause the feasible region too narrow to accommodate any target tag. On the other hand, if the constraint is greater than $\lambda/2$ , there exist more than two possible values of $\Delta d$ , drawing multiple branches. Hence, we think the $\frac{\lambda}{2}$ is best constraint condition.

# B. How to combat the multipath effect?

Multipath effect is a common issue for wireless localization systems. There have been many excellent solutions $[7]$ , $[11]$ developed recent years. Their basic ideas are to find out the direct path among all paths. We directly borrow their methods here. In addition, the reader usually has multiple channels $(10+)$ available. We can choose the optimal one. However, this issue is beyond our discussion in this paper. We will take further study in our future work.

![](images/e1ef66846cd602ba673232530edd636e2637ac53db22cedea271d670911e9d5b.jpg)



Fig. 9. Experiment scene

# V. IMPLEMENTATION AND EVALUATION

In this section, we present the implementation and conduct performance evaluation on the prototype.

# A. Implementation

Hardware: We implement a prototype of BackPos using Impinj R420 with four directional antennas. There are two types of tags modeled ‘2 × 2’ or ‘Square’ from Alien company, used in our experiments. The reader works during the frequency of 920.5MHz ∼ 924.5MHz by default, which is the legal UHF band in China. Correspondingly, the wavelength ranges from 32.43.cm to 32.57cm.

Software: The software part running at personal computer is developed using Java language. It connects to the RFID reader with LLRP protocol. This protocol was ratified by EPCglobal in April 2007.

Parameter choice: The antenna's transmission power are adjusted at $30mW$ . We command the reader to immediately report its readings after a round of antenna scheduling. Although our approach is able to eliminate the tag's initial rotation $\theta_{TAG}$ , the reader transceiver's initial rotation $\theta_T$ and $\theta_R$ would still affect the measurement results as shown in Equation 1. These two values should be referred to the reader's specification. It not found, we suggest the following simple method to measure them in practice. Placing a tag on the perpendicular bisector of two antennas, then $\rho = (\Delta\theta \bmod 2\pi)$ where the distance factor is eliminated because $\Delta d = 0$ .

# B. Evaluation Methodology

Three experiments are designed towards measuring the accuracy of BackPos. Our experiments are performed in an office room whose size is $500 \times 800 cm^{2}$ . Four antennas are deployed with a spacing of 40cm in a straight line, polarized to a same direction. The antennas and target tags are all suspended at 138.1cm high from the ground. The ground truth is measured using a laser distance meter with an error of 1mm. During the measurement, we consider the antennas and tags as the points locating in their geometric centers. Figure 9 shows the experiment scene which illustrates the coordinate system, feasible region, experimental tags, reader, and antennas. The coordinates of four antennas are $A_{1}(59.7, -1)$ , $A_{2}(12.7, -4)$ , $A_{3}(-23.8, -4)$ , and $A_{4}(-61.8, -4)$ . Moreover, we find there is an interesting phenomenon that ImpinJ reader always report the $\theta' = 2\pi - \theta$ instead of $\theta$ , which does not exactly conform to its manual. That is why the phase decreases as the distance increasing in Figure 4. However, that does not affect our theoretical analysis and experiment results. In the following experiments, we always use the revised $\theta = 2\pi -\theta^{\prime}$ .

Metrics: We use the error (cm) to indicate the position accuracy, which is an absolute metric. We also employ another important metric called Receiver Operating Characteristic (ROC) curve to measure the relative accuracy. The vertical axis of ROC curve is the true positive rate (TPR) which is the total number of detected true positives divided by the number of real positives in ground truth. The horizontal axis is the false positive rate (FPR). The FPR is termed as the rate of number of false positives to the total number of negative events in ground truth.

Baseline: We compare BackPos with two baseline schemes, both of which use the reference tags. (i) LAND-MARC [1]. Its basic idea is to calculate the weighted average of the four nearest tag's locations. The weights are determined by the their RSS values. We deploy the reference tags with the interval of $1m$ in the office room ( $5 \times 8$ reference tags in total). (ii) VIRE [2]. Another modified RSS based method, which employs virtual reference tags aiming to eliminate the influence among these tags.

# C. Positioning Accuracy

To measure the absolute positioning accuracy, two experiments are conducted as follows.

1) Accuracy comparison with baseline: In the first experiment, we place a target tag in the position $T(-43.2, 283.4)$ . The distance difference $\Delta d$ from the target tag to four antennas is crucial for hyperbolic positioning. The small errors may have huge consequences. Hence, we firstly check the error of $\Delta d$ in the first experiment. In theory, there are 24 pairs of distance differences among the tag to four antennas. We randomly choose three pairs, $|TA_{2}| - |TA_{1}| = \Delta d_{2,1} = \Delta d_{1,2} = -10.9$ , $|TA_{3}| - |TA_{2}| = \Delta d_{3,2} = -6.82$ and $|TA_{4}| - |TA_{3}| = \Delta d_{4,3} = -0.16$ . We use the measured phase values to calculate their differences based on Equation 8 or 9. The experiment repeats for 100 times and the CDF of the ranging error is shown in Figure 10. From the figure, we can see that the maximum error is less than 1cm, which suggests the phase is indeed an excellent indicator for ranging once again. Interestingly, the error of $\Delta d_{2,1}$ is greater than that of $\Delta d_{4,3}$ on average. In geometry, the T is closest to the $A_{4}$ but farthest to the $A_{1}$ . We think such phenomenon may come from the assumption that the antenna can be considered as geometrical point. In fact, when the tag is off the antenna's central axis, the EM may emit from the antenna's edge instead of its geometrical center, leading to a small measurement error in ground truth. Even so, we think the error is small enough to be tolerant in practice.

Second, we plot the CDF of position error in Figure 11. The error is defined as the Euclidean distance between the ground truth and measured positions. From the figure, we observe that the phase based positioning is indeed far better than any of RSS based methods. Their errors are not in an order of magnitude even. The mean error of BackPos equals $12.8cm$ while the other two methods' mean errors are around $100cm$ . VIRE seems a little better than LANDMARC, gaining the benefits from the virtual tags. We believe the $12.8cm$ error is sufficient for major applications because the size of tagged object is bigger than the error. For example, the height of a bottle of Coke is 23cm, the width of a usual milk carton is 20cm, the size of A4 paper is 21cm × 30cm, etc. Furthermore, we found the results of VIRE and LANDMARC are very unstable. Unlike the BackPos whose error sharply concentrates on its mean value with about 3.8cm variance, VIRE and LANDMARC's errors respectively vibrate in 31.2cm and 48.6cm.

![](images/9c420f2d4a8b78660bb430ac38efea9ba9b6eed4ebce949f9b9573ff3943b912.jpg)



Fig. 10. Ranging error

![](images/2ebc107fc4c2005328802454cfe06e37086e7410b58a7fb00876651e0988f4b6.jpg)



Fig. 11. Positioning error

![](images/f7ca0084b89a75e8c29170f59311e418031f913c581710f9c24b2f35286ad1c0.jpg)  
Fig. 12. Positioning vs. positions

![](images/8923e133346a41e3d7f1de7c7b36833b67e91d103ff203b01105132337c0b4c6.jpg)



Fig. 13. Error CDF in positions

![](images/5e4d5c58beabce6e8c84f83a3da5907e09dd2d186acbf7b4ad5f2007e960a35c.jpg)



Fig. 14. Positioning sensitivity

![](images/acd20cbc6670b7a06f03b78c84aec1e7514caeee2d6c2c1dde00c7c87eeb5f21.jpg)



Fig. 15. Impact of tag diversity

2) Accuracy comparison in different positions: In the second experiment, we consider the multiple positions. There are total 9 tags deployed in a circle as shown in Figure 12. In the figure, the ground truth is marked as ‘×’. Note that the circle does not look smooth because the graph axes are distorted for unified layout. We also plot the error CDF of these positions in Figure 13. We observe that (1) the error has a little difference among the positions. Generally speaking, the points closer to the antenna arary has a smaller error compared with the farther ones. For example, $T_{1}$ has a mean error of 5.3cm while that of $T_{5}$ is 11cm. The variance behaves the same pattern. They are 4.2cm and 5.6cm for $T_{2}$ and $T_{9}$ but 6.4cm for $T_{6}$ . Because signal of farther away tags has a lower SNR, leading to the growth of error. (2) the error mainly comes from the y-axis instead of x-axis. The latter is highly clustered around its mean value. This is because the eccentricity of our hyperbola is very big, which means a litter x-value will incur a large y-value.

# D. Positioning Sensitivity

Besides the absolute accuracy, we may pay more concerns at the relative accuracy sometimes. For example, we do not want to place the poison and foods together or mix the cat food with a hamburger. In these scenarios, we need an alert when two target objects are placed too close. Here, we employ the ROC curve to represent such relative accuracy. The experiment is conducted as follows. For a given operating parameter l, we perform two tests to measure a pair of TPR and FPR. In the first test, we place two tags $T_{1}$ and $T_{2}$ within a spacing of l/2, then measure the distance between $T_{1}$ and $T_{2}$ . If $|T_{1}T_{2}| < l$ , a true positive event is recorded. The TPR is outputted after the test is repeated for 100 times. In the second test, we change their spacing to 1.5l. If $|T_{1}T_{2}| > l$ , a true negative event is recorded. The test is also repeated for 100 times to get a FPR. During the experiment, the parameter l varies from 6cm to 120cm with an increase of 2cm. Finally, we draw the ROC in Figure 14. The results of LANDMARC and VIRE are depressed because they behave as a random guessing. For BackPos, the FPR is around 40% when the l is too small. As when the l over than 15cm, this is almost no any false positives occurred.

# E. Positioning Diversity

Tag's diversity is one of the serious issues in RFID positioning. We use the phase difference to eliminate this factor. To validate its impact on the three methods, we perform the positioning on two models of tags, 'Square' and $2 \times 2$ . These two models have different antenna size and shape. We plots the comparison in Figure 15. The results show that the tag's diversity has very little impact on the accuracy of BackPos as expected. However, it takes much on the other two methods. In whole, the $2 \times 2$ has a bigger antenna size being more easily to absorb the EM from reader hence its RSS may be more sensitive to the positions and owns a relative higher accuracy.

# VI. RELATED WORK

RSS-based RFID localization: LANDMARC [1], enables the reader power in eight levels and leverages RSS to find k nearest reference tags of target active tag, and positions target out. VIRE [2] use virtual reference tags to enhance accuracy of positioning. Bekkali et al. use Kalman filtering build a probabilistic model to reduce the effect of RSS error measurement [4]. In addition, RSS-based localization was extended to 3-D positioning [3], [12]. Phase-based RFID localization: Zhang et al. examine the applicability of direction-of-arrival (DOA) estimation methods to localization of passive RFID tags [6]. Azzouzi et al. test AOA in the complex baseband signals of adjacent antenna elements [5]. Nikitin et al. describe three techniques of positioning, based on phase difference in time domain, frequency domain and spatial domain [13]. Hekimian-Williams et al. employ maximum likelihood method to estimate position base on phase difference [14]. Other RFID related issues: Liu et al. design schemes to continuous scan large-scale tags adaptively [15]. Yang et al. explore how to make batch authentication without identification [16]. Chen et al. study the problem of collecting information from sensor augmented tags [17]. Luo et al. consider efficiency and energy saving while detecting missing tags [18]. Season shelves interference and identify tags by turns [19]. PMTI [20] identifies missing tags and OTrack [21] sequences a steam of RFID tags. PinIt makes use of multipath-effect based fingerprints with the help of reference tags to acquire high accuracy in reality environment [8]. ZOE [22] and Gong et al. [23] estimate cardinality for large-scale RFID systems. WLAN localization: RADAR [24] was the first system to propose the use of a RF map for location and tracking users in WLAN based systems. Rai et al. leverage crowdsourcing to create training data for site-specific calibration [25]. PinPoint [26] and ArrayTrack [11] use antenna arrays at multiple APs to compute AOA of direct path, resulting in high accuracy. UnLoc [27] envisions signatures that naturally exist in the environment as internal landmarks of a building and localizes indoor to bypass the need of war-driving. Hyperbolic positioning: Hyperbolic positioning comes from TDoA (Time Difference of Arrival), which mainly exists in locating GSM (Global System for Mobile Communications) base stations [28], [29]. Y.T.Chan gives a simple and efficient estimator for hyperbolic location [9].

# VII. CONCLUSION

In this paper, we study characteristics of phase and propose BackPos. We implement a prototype of BackPos with COTS RFID products and conduct comprehensive evaluations. The results show that BackPos achieves mean accuracy of 12.8cm with variance of 3.8cm. We believe this is a practical positioning system for various RFID applications.

# VIII. ACKNOWLEDGEMENT

This work is supported in part by the China National Funds for Distinguished Young Scientists Program 61125202, National High-Tech R&D Program of China (863) under grant No.2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200. And we acknowledge the support from the codes of USRP2reader from the Open RFID Lab (ORL) project [30].

# REFERENCES

[1] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “Landmarc: indoor location sensing using active rfid,” Wireless networks, vol. 10, no. 6, pp. 701–710, 2004.   
[2] Y. Zhao, Y. Liu, and L. M. Ni, “Vire: Active rfid-based localization using virtual reference elimination,” in Proc. of IEEE ICPP, 2007.   
[3] C. Wang, H. Wu, and N.-F. Tzeng, “Rfid-based 3-d positioning schemes,” in Proc. of IEEE INFOCOM, 2007.

[4] A. Bekkali, H. Sanson, and M. Matsumoto, “Rfid indoor positioning based on probabilistic rfid map and kalman filtering,” in Proc. of IEEE WiMob, 2007.   
[5] S. Azzouzi, M. Cremer, U. Dettmar, R. Kronberger, and T. Knie, “New measurement results for the localization of uhf rfid transponders using an angle of arrival (aoa) approach,” in Proc. of IEEE RFID, 2011.   
[6] Y. Zhang, M. G. Amin, and S. Kaushik, “Localization and tracking of passive rfid tags based on direction estimation,” International Journal of Antennas and Propagation, 2007.   
[7] S. Sen, J. Lee, K.-H. Kim, and P. Congdon, “Avoiding multipath to revive inbuilding wifi localization,” in Proc. of ACM MobiSys, 2013.   
[8] D. K. Jue Wang, “Dude, where’s my card? rfid positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.   
[9] Y. Chan and K. Ho, “A simple and efficient estimator for hyperbolic location,” IEEE Transactions on Signal Processing, vol. 42, no. 8, pp. 1905–1915, 1994.   
[10] D. M. Dobkin, The RF in RFID: passive UHF RFID in practice. Newnes, 2007.   
[11] J. Xiong and K. Jamieson, “Arraytrack: a fine-grained indoor location system,” in Proc. of USENIX NSDI, 2013.   
[12] M. Bouet and G. Pujolle, “A range-free 3-d localization method for rfid tags based on virtual landmarks,” in Proc. of IEEE PIMRC, 2008.   
[13] P. V. Nikitin, R. Martinez, S. Ramamurthy, H. Leland, G. Spiess, and K. Rao, “Phase based spatial identification of uhf rfid tags,” in Proc. of IEEE RFID, 2010.   
[14] C. Hekimian-Williams, B. Grant, X. Liu, Z. Zhang, and P. Kumar, "Accurate localization of rfid tags using phase difference," in Proc. of IEEE RFID, 2010.   
[15] X. M. K. L. Haoxiang Liu, Wei Gong and W. He, “Towards adaptive continuous scanning in large-scale rfid systems,” in IEEE INFOCOM, 2014.   
[16] L. Yang, J. Han, Y. Qi, and Y. Liu, “Identification-free batch authentication for rfid tags,” in IEEE ICNP, 2010.   
[17] S. Chen, M. Zhang, and B. Xiao, “Efficient information collection protocols for sensor-augmented rfid networks,” in Proc. of IEEE INFOCOM, 2011.   
[18] W. Luo, S. Chen, T. Li, and S. Chen, “Efficient missing tag detection in rfid systems,” in Proc. of IEEE INFOCOM, 2011.   
[19] L. Yang, J. Han, Y. Qi, C. Wang, T. Gu, and Y. Liu, “Season: Shelving interference and joint identification in large-scale rfid systems,” in IEEE INFOCOM, 2011.   
[20] Y. Zheng and M. Li, “P-mti: Physical-layer missing tag identification via compressive sensing,” in IEEE INFOCOM, 2013.   
[21] L. Shangguan, Z. Li, Z. Yang, M. Li, Y. Liu, and J. Han, “Otrack: Towards order tracking for tags in mobile rfid system,” IEEE TPDS, 2013.   
[22] Y. Zheng and M. Li, “Zoe: Fast cardinality estimation for large-scale rfid systems,” in IEEE INFOCOM, 2013.   
[23] X. M. Wei Gong, Kebin Liu and H. Liu, “Arbitrarily accurate approximation scheme for large-scale rfid cardinality estimation,” in IEEE INFOCOM, 2014.   
[24] P. Bahl and V. N. Padmanabhan, “Radar: An in-building rf-based user location and tracking system,” in Proc. of IEEE INFOCOM, 2000.   
[25] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: Zero-effort crowdsourcing for indoor localization,” in Proc. of ACM Mobicom, 2012.   
[26] K. Joshi, S. Hong, and S. Katti, “Pinpoint: Localizing interfering radios,” in Proc. of USENIX NSDI, 2013.   
[27] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: Unsupervised indoor localization,” in ACM Mobisys, 2013.   
[28] M. Spirito and A. G. Mattioli, “On the hyperbolic positioning of gsm mobile stations,” in Proc. of IEEE ISSSE, 1998.   
[29] M. A. Spirito, “On the accuracy of cellular mobile station location estimation,” IEEE TVT, vol. 50, no. 3, pp. 674–685, 2001.   
[30] “Open rfid lab,” http://pdcc.ntu.edu.sg/wands/ORL.