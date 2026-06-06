# See Through Walls with COTS RFID System!

Lei Yang∗, Qiongzheng Lin∗, Xiangyang Li∗†‡, Tianci Liu∗, Yunhao Liu∗

∗School of Software, Tsinghua University, China

† Department of Computer Science and Technology, Tsinghua University, China

‡Department of Computer Science, Illinois Institute of Technology, USA

young@tagsys.org, qiongzheng@tagsys.org, xli@cs.iit.edu, tian@tagsys.org, yunhao@greenorbs.com

# ABSTRACT

Through-wall tracking has gained a lot of attentions in civilian applications recently. Many applications would benefit from such device-free tracking, e.g. elderly people surveillance, intruder detection, gaming, etc. In this work, we present a system, named Tadar, for tracking moving objects without instrumenting them using COTS RFID readers and tags. It works even through walls and behind closed doors. It aims to enable a see-through-wall technology that is low-cost, compact, and accessible to civilian purpose. In traditional RFID systems, tags modulate their IDs on the backscatter signals, which is vulnerable to the interferences from the ambient reflections. Unlike past work, which considers such vulnerability as detrimental, our design exploits it to detect surrounding objects even through walls. Specifically, we attach a group of RFID tags on the outer wall and logically convert them into an antenna array, receiving the signals reflected off moving objects. This paper introduces two main innovations. First, it shows how to eliminate the flash (e.g. the stronger reflections off walls) and extract the reflections from the backscatter signals. Second, it shows how to track the moving object based on HMM (Hidden Markov Model) and its reflections. To the best of our knowledge, we are the first to implement a through-wall tracking using the COTS RFID systems. Empirical measurements with a prototype show that Tadar can detect objects behind 5′′ hollow wall and 8′′ concrete wall, and achieve median tracking errors of 7.8cm and 20cm in the X and Y dimensions.

# Categories and Subject Descriptors

C.2 [Computer Systems Organization]: Computer Communications Networks

# Keywords

RFID, See-through walls, Tracking, Tadar

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from Permissions@acm.org.

MobiCom’15, September 7–11, 2015, Paris, France.

c 2015 ACM. ISBN 978-1-4503-3619-2/15/09âA˛e\$15.00 ˘

DOI: http://dx.doi.org/10.1145/2789168.2790100.

![](images/1fa048f9e934419134b5e573ddb925055b451cc6563853a2b3a17cbdded323a0.jpg)



Figure 1: Through-wall tracking of moving object. Tadar logically transforms the tags attached on the outer wall into an antenna array receiving the reflections off the human behind the wall.

# 1. INTRODUCTION

Motion tracking and localization systems have received a lot of attentions recently. A number of innovative systems using different technologies are developed for improving the accuracy and robustness, e.g., [1–4]. However, these systems typically require the objects to carry an RF device in order to be identified and localized. This paper explores the potential of using COTS RFID systems to build a system that can capture the motion of mobile object behind a wall and in closed rooms without tagging it. Such system is able to provide life-saving benefits for emergency responders, police and military personnel arriving at dangerous situations by letting them know the locations of people inside a building without instrumenting the people in advance. Many other applications would also benefit from this system, such as elderly, people surveillance, intruder detection, and so on.

The concept underlying through-wall tracking is to emit RF signals to a closed room facing with a non-metallic wall. The signal traverses through the wall, reflects off objects and humans, and returns back, imprinted with a glimpse of what is inside a closed-room. Through-wall tracking has been extensively studied in radar community, which mainly employs ultra-wideband and MIMO radar technique [5, 6] to detect moving objects behind a wall. Their devices are almost inaccessible to non-military purpose due to ultra-widebandwith, voracious power consumption, and unaffordable. For example, a typical radar device consumes 2  4 GHz bandwidth [5, 7, 8]. The price of the through-war radar sold online is about 80, 000 US dollars [9]. Even worse, the throughwall radar systems in the market are usually prohibited from selling to civilians in most countries in the world. To address these issues, recently several breakthrough systems [10–15] are developed for seeing through the walls with WiFi. However, these past systems still need either customized devices (e.g. USRP), specialized signals (e.g. FMCW), or additional receivers inside the room.

In this work, we turn our attentions to a mature technology, RFID. RFID is evolving as a major technology enabler for identifying and tracking objects all around the world. The reason for this widespread deployment is the simplicity of tags, which enables very low lost at high volumes. One of the benefits of RFID systems is that it can identify objects without needs of line-of-sight (LOS) owing to the multi-path effect. The challenging question is “Can RFID systems enable us to identify and track objects through walls?”. At the first instinct, it seems like an impossible mission because the backscatter signals off tags are too weak (typically at -55 dBm) to traverse a wall (with  18 dB attenuation) or even a thick glass (with ∼ 3 dB attenuation) [16].

It is well known that RFID systems adopt an asymmetric architecture in order to reduce the complexity and costs of tags. Such design has three important features. First, the reader is able to provide 30 dBm transmitting signals and connected to higher-gain directional antennas. Such strong signals are sufficient for two-way traversal through a wall. Second, the tag has no transceiver and modulates its ID on the backscatter signals through changing the impedance on its antenna. Its modulation is vulnerable to the interference from ambient reflections [16]. Unlike past approaches [1, 17], which consider this vulnerability as detrimental, we exploit it as an opportunity to monitor the surrounding objects. Third, the RFID technology, stemming from the radar, has strong ability to resolve very weak signals from the background. Inspired by these these features, we redefine RFID system to extend our senses. We leverage the reader to supply RF signals lighting up objects and treat tags as the antennas receiving reflections. To illustrate Tadar’s approach, Fig. 1 shows a toy example. We attach an array of tags on the outer wall and use a reader to read them. The signal propagation between reader and tags is kept in line-of-sight. Apart from tags, the transmitting signals from reader are also reflected off other objects like walls, furnitures and mobile objects. These reflections plus the original signals from reader provide a combined signal to each tag for their modulations. As a result, the backscatter signal that carries tag’ ID implicitly contains the reflections off human. If we can extract the human’s reflections from the backscatter signals, his locations would be pinpointed.

Transforming this high-level idea into a practical system, however, requires addressing multiple challenges. First, it is quite challenging to separate a weaker signal (reflections off object) from another weak signal (backscattered signal). In particular, this task should be accomplished using the COTS RFID reader, which does not support any low-level signal access or modifications. The second challenge stems from ‘Flash Effect’ (see [11]) that the signal power after traversing the wall twice (in and out of the room) is reduced by three to five orders of magnitude, such that the reflections off objects inside the room will be drown in the reflections off the wall itself (call flash). Third, the inherent diversity of devices and objects would introduce many unknown impacts on the magnitude attenuations and phase rotations, leading to unpredictable tracking errors.

To address these issues, we present Tadar for tracking moving object through walls and behind closed doors using COTS RFID readers and tags. Our objective is to enable a see-through-wall technology that is low-cost, compact, and accessible for civilian purpose. We propose two main techniques to address the aforementioned challenging issues. First, Tadar views each read of tag as one channel estimation and recovers the signal with RSS and phase reported by reader. Since the wireless signals linearly combine over the medium, Tadar eliminates the flash by subtracting the signals learned when the room is empty. It also separates the reflections from the backscatter signals by dividing the signal learned in LOS propagation (see §5). Second, Tadar models the object’s motions using Hidden Markov Model (HMM), which considers the object’s locations as hidden states and its reflections as observations. Then it uses Viterbi decoding to recover the object’s trajectory (see §6).

Summary of results: We build a prototype of Tadar using one Impinj Reader and 45 Alien tags, and evaluate it in two office buildings (see 7). Our main results are as follows:

Tadar can detect object moving behind $8 ^ { \prime \prime }$ concrete walls, $5 ^ { \prime \prime }$ hollow walls, and $1 . 5 ^ { \prime \prime }$ wooden doors.   
• Tadar can achieve detecting ranges of 4m and 6m on average respectively when pointing at a closed room with $8 ^ { \prime \prime }$ concrete walls and $5 ^ { \prime \prime }$ hollow walls supported by steely frames.   
• Tadar can track the moving object in a closed room with median errors of 7.8cm and 20cm in X and Y dimensions when monitoring the room from one side, offering about 3×, 3.5× and 1.3× improvement compared with NRES [18], TagTrack [19] and Wision [20].   
• Tadar can correctly decode 93% gestures in our application study where 5 volunteers encode the messages through his/her movements.

Contributions: In contrast to the state-of-the-art work, Tadar introduces a low-cost solution to the through-wall tracking of moving objects, enabling civilians to use this technology. Tadar is the first to introduce through-wall tracking using RFID systems by transforming a group of tags attached on the wall into a receiving antenna array. It demonstrates a working system implemented purely based on COTS devices and made accessible to the general public.

The rest of the paper is organized as follows. We review the related work in 2 and the technical background in 3. The main design is overviewed in 4. The technique details of reflection extraction and object tracking are respectively elaborated in 5 and §6. The implementation is described in §7and the system is evaluated in 8. We also conduct an application study in 9. Lastly, we conclude our work in 11.

# 2. RELATED WORK

In this section, we briefly review the related literature in seethrough-wall technology.

See through walls with radar. Through-wall imaging or tracking has gained attentions for a decade, especially in radar community [5, 6, 8, 21–25]. The past systems eliminate the flash effect and localize the moving object by estimating the time of flight of signals. Specifically, the pulse reflected off the wall arrives earlier in time than that reflected off moving object behind it. To differentiate such slight time difference (< 1ns), the systems would transmit a linear frequency chirp at cost of ultra-wide bandwidth of the order of 2 GHz [21]. The products developed in the industry [26,27] also require multiple GHz bandwidth. Adib et al. track user’s 3D motion or heartbeat [24, 25]. These works utilize the FMCW signals (sweeping from 5.46-7.25 GHz) to estimate the time-of-flight, so it is actually UWB based. UWB would continuously occupy a wide band and may impose interference on other devices that share the same frequency. Tadar employs the COTS RFID devices communicate in 50 KHz narrow band channels [28], overcoming the need of UWB.

See through walls with Wi-Fi. Some efforts proposed recently attempt to break the limitations of UWB systems and exploit the potentials of using Wi-Fi for through-wall technologies [10, 11, 14, 20, 24, 25]. Chetty et al. [10] propose to deploy the transmitter and a reference receiver in the room, which cooperates with other receivers outside to see objects in the room. This method is limited by its deployment. Adib et al. introduce a system, called Wi-Vi, that borrows the MIMO interference nulling to eliminate the flash effect [11]. It creatively treats the motion of a human body as an antenna array and tracks the resulting RF beam. Our work differs from Wi-Vi in that Wi-Vi focuses on the relative motions of human (e.g. walking direction) while Tadar aims to exactly recover object’s trajectory. Huang et al. explore the feasibility of achieving computational imaging using Wi-Fi signals. Their system works without obstruction [20]. Depatla et al. proposed a see-through imaging based on WiFi measurements with unmanned vechicles [29,30]. In contrast, Tadar does not need any customized devices or specialized signals and really operates at the narrowband.

![](images/9238846e276d64f101ba6119cbf322cf3d4f53e1d74b6725cf64b92b223427bd.jpg)



Figure 2: Block diagram of backscatter communication used in UHF RFID system. The tag modulates its ID on the backscatter signal using ON-OFF keying through changing the impedance on its antenna.

See through walls with WSN. Some past works in radio tomography employ networks or hundred sensors to track a person even if he/she does not carry any wireless device. They can be categorized into following groups, link-based and location-based. (1) Linkbased schemes measure the RSSI for each of the resulting n2 links among n sensor nodes, and attribute the variation of RSSI on a link to a human crossing that link [31–36]. Wilson and Patwari find that the changes in RSSI due to human motion can be modeled by the skew-Laplace distribution [31]. Kleisouris et al. exploit channel diversities to enhance motion detection accuracy [33]. Nannuru et al. develop a measurement model for multi-target tracking using RF tomography, applied for tracking up to three targets [36]. (2) Location-based schemes are also known as the radio fingerprint, which is a popular approach for RF-based localization [37–39]. Zhang et al. firstly collect a radio map when the subject presents in a few predetermined locations, and then map the test location to one of these trained locations [37]. Moustafa extends RASS to a much large-scaled deployment [38]. Xu et al. employ camera to trigger recalibration and update the radio signal data to improve the localization accuracy [39]. These two groups mainly focus on the metric of RSSI, which is not a stable location indicator in RFID systems.

# 3. UNDERSTANDING REFLECTIONS

In this section, we firstly introduce the technical background of RFID system, and then conduct a series of empirical studies on the backscatter communications.

# 3.1 Technical Background

Passive RFID system communicates using a backscatter radio link, as shown in Fig. 2. The reader supplies a Continuous Wave (CW) signal, a periodic signal that persists indefinitely without changing its amplitude, frequency or phase, for tags. An RFID reader communicating with a passive tag must operate in full-duplex mode, in the sense that it must supply CW for the tag to backscatter while listening to the tag response at the same time. The tag with no battery equipped, purely harvests energy from the reader’s signal. A simple way to understand backscatter radio is as follows [16]. The current flowing on reader’s transmitting antenna leads to a voltage induced on the tag’s antenna. This induced current also leads to radiation, producing a signal that can be detected: a backscattered signal. The tag modulates its ID on the backscatter signal using ON-OFF keying through changing the impedance on its antenna to transmit a ‘1’ bit and remaining in its initial silent state for ‘0’ bit. Referring to [40] published by the ImpinJ, a reader might employ open-loop estimation techniques such a preamble correlation or closed-loop estimation for acquiring and/or tracking carrier phase and RSS. For simplicity and saving cost, most of modern RFID readers use one single antenna both for transmitting and receiving.

![](images/1ef2fc8e8bf8bb11d5fed1eb9820ca3a5ca4483d8cf5310ddd7c7b0365bae21d.jpg)



(a) Expriment setup

![](images/975ab414f502e43ea9670043ac7f8da43afcd9105da2f6ca2f5ea26a2a54ba39.jpg)



(b) Indirect impact

![](images/4bbd668c04c5d4ce7ae88fc47edded0c8d5f351402655409ea747afa11311980.jpg)



(c) Direct impact   
Figure 3: Empirical studies on measured RF phase. (a) The default setup of our experiments. (b) The indirect impact on backscatter signals. (c) The direct impact on backscatter signals.

# 3.2 Empirical Studies

We conduct empirical studies to better understand the characteristics of backscatter communications, using a COTS ImpinJ reader and an Alien tag. The experiment setup is shown in Fig. 3(a). By default, the reader antenna A, tag T and reflector X are deployed in a straight line. The tag attached on a plastic card, locates between the reader and the reflector. The reader and tag are deployed with 1m apart from each other. We horizontally move the reflector (i.e. the notebook) to observe how its reflections take impacts on the phase values of the backscatter signal 1. In an ideal environment, there are two basic channels, forward channel (A → T ) and backward channel (T → A), between the reader and tag. In our scenario, however, there emerge two additional signal propagations, $A \to X \to A$ and $A \to X \to T ,$ due to the existence of reflector. We categorize the impacts of these two propagations into two types based on whether the reflections directly or indirectly affect on the tag’s backscatter signal.

Indirect impact: The transmitting signal arrives at $X$ and is reflected back to A (i.e. $A \to X \to A )$ . As a result, the reflection mixes with the tag’s backscatter signal at reader end, which may indirectly affect the identification of the backscatter signal.   
• Direct impact: The transmitting signal reflected to $T ( i . e . \ A $ $X  T )$ adds up with the original signal through forward channel $( i . e . ~ A  T )$ , producing a combined signal at tag end. Since the tag uses this combined signal to modulate its ID, the received backscatter signal contains a direct impact from this propagation.

HYPOTHESIS 1. The indirect impact of reflections off surrounding objects can be negligible.

We firstly focus on the indirect impact incurred by the reflections propagated from $A \to X \to A$ . To isolate the indirect impact, we prevent the reflections from traversing to the tag by placing an RF absorber (with approximately 35 dB attenuation) between the tag and the reflector. The reflector is much larger than the absorber, so there are still many reflections getting back to the reader antenna. We move the reflector to adjust the distance to tag between 10cm and 40cm. The phase measurements are repeated 100 times for a particular distance. The final phase values reported by the reader are illustrated in Fig. 3(b). The dotted line indicates the baseline, $i . e .$ the phase value measured when removing the reflector but keeping the absorber. Supperisingly, the figure suggests that the phase value vibrates around the baseline with a very small deviation $( < 1 \mathrm { r a d i a n s } ) ^ { 2 }$ no matter what distance is adjusted. In other words, the impact of propagation from $A \to X \to A$ is reduced to be minimal.

Why the indirect impacts are removed? The RFID systems are originally designed for identification. Its main task is to resolve the weak backscatter signal from the CW and environment noise. The reflection from $A \to X \to A$ is a kind of self-interference because it does not carry backscatter preamble and highly correlates to the original CW that the reader emits. It can be easily removed by learning the environment before interrogating tag. Removing the self-interference is a standard procedure in RFID reader [2, 16] (see Fig. 2), and also becomes an important metric to evaluate the reader’s performance. Any modern COTS RFID reader has the strong ability to eliminate the self-interference, so the indirect impact can be negligible in practice.

HYPOTHESIS 2. The backscatter signals are vulnerable to the direct impact of the reflections off surrounding objects.

This hypothesis is our foundation of leveraging tag to sense the reflections off surrounding objects. In this experiment, we remove the RF absorber and re-collect the phase values. The results are plotted in Fig. 3(c). In contrast to the last experiment, the phase value periodically changes as the distance increases. Apparently, the backscatter signals are vulnerable to the direct impact. The tag modulates its ID using the combined signal (through $A  T$ and $A \to X \to T )$ . The received backscatter signal contains a standard preamble so the reader would not filter it. Intuitively, the phase non-linearly changes and gradually approaches to the baseline as the distance increases. This is because the direct impact from $A $ $X  T$ gradually weakens as the distance increases, resulting in the signal through $A \  \ T$ gradually dominates the backscatter signal. We will quantitatively model the reflections in $\ S 5 .$

2The vibrations are mainly caused by the thermal noise [1].

# 4. TADAR OVERVIEW

Tadar is a fine-grained UHF RFID through-wall tracking system that can locate and track moving object including human, and can provide a resolution on the order of a few to tens of centimeters, much smaller than read range of reader.

System Scope. Ultra-low cost UHF tags (5-10 cents each) become the preferred choice of many industry applications. Following the common practices, we concentrate on the UHF tags. We assume that tags are well-positioned so their locations are all known. We also assume that the surveillance region is confined within a limited space. Today’s UHF RFID has an operating range of around 10m. Thus, the assumption is acceptable and can be effectively satisfied by UHF RFID systems. To avoid the tag collisions, the reader adopts TDMA fashion to read them and discard the collided signals [17]. Thus, the effects among tags are negligible. Our systems works in the application layer of reader with the reported RSS and phase values. Our system is general and can capture any mobile objects like robot or drone.

Problem Definition. Suppose n tags, $\{ T _ { 1 } , T _ { 2 } , \dots , T _ { n } \}$ , are attached on the outer wall. We use the term $T _ { i }$ to denote the $i ^ { t h }$ tag as well as its coordinate. One reader antenna, denoted as $A ,$ is employed to light up the objects and read tags. The signals propagated between reader and tags are always kept in LOS. During the surveillance, the geometric relationships between tags remain unchanged. The reader is configured to continously and cyclically read tags, which resembles to using a camera to continously take snapshots of the room. One read frame is finished after n tags are all read once. Each frame contains n tags’ RSS and phase values reported by a COTS RFID reader. Our problem is to recovery the trajectory of the moving object behind walls and closed doors given a sequence of read frames.

Solution Sketch. At a high level, Tadar decomposes the problem into two subproblems.

• Extracting reflections: Since Tadar uses the reflections off the moving object for tracking, the first subproblem is how to extract the reflections while eliminating the flash effect. This subproblem is addressed in $\ S 5$ .

• Tracking objects: The second subproblem that Tadar addresses in §6 is how to recover the mobile object’s trajectory using the extracted reflections.

The next two sections elaborate on these two subproblems, providing the technical details.

# 5. EXTRACTING REFLECTIONS

In order to distinguish the signals reflected off moving object, off static objects like wall and furniture, and off tags, we respectively call these signals reflections, flash, and backscatter signals. The problem of extracting reflections off objects behind walls is exacerbated by two issues.

First, the signal power after traversing the wall twice (in and out of the room) is reduced by three to five orders of magnitude [11, 16]. The wall is much larger than the object of interest and has a higher reflection coefficient, leading to stronger reflections than that off objects behind the wall. It is like placing a mirror in front of a camera that reflects the camera’s flash and prevents it from capturing objects in the scene, which is called flash effect [11].

Second, previous through-wall systems all directly receive the reflections through the real antennas connected to the transceiver. In contrast, Tadar logically converts the RFID tags attached on the wall to a virtual antenna array receiving the reflections. These virtual antennas are wirelessly connected to the reader and carry the reflections through the backscatter signals. Thus, an additional step is required to separate the reflections off the moving object from the backscatter signals reflected by the tags. This is an extremely challenging task as the backscatter signal is already very weak .

![](images/274abf2c4ecb0d5893c2185083457fba7ccdd759824bc970230bb41b0c4c6b32.jpg)



Figure 4: Signal propagation without reflections. There are two basic channels between the reader and the tag.

To address the above challenges, we start by modeling the backscatter signals through LOS propagation. We then show how to eliminate the flash and derive the reflections from the backscatter signals. Lastly, we sketch the whole algorithm.

# 5.1 Modeling the Backscatter

A wireless signal is typically represented as a stream of complex numbers. The transmitter modulates the bits into complex symbols to transmit a packet over the wireless channel. The received signal is also represented as a stream of complex symbols. Generally, if the transmitted symbol is denoted as $S ,$ then the received symbol $S ^ { \prime }$ can be approximated as

$$
S ^ {\prime} = h \cdot S \tag {1}
$$

where $\textit { h } = \alpha e ^ { \mathbf { J } \delta }$ is also a complex number, called channel parameter, and α and δ are referred to as channel attenuation and its phase rotation. The channel can be well approximated by a linear time-variant system. If Alice and Bob concurrently transmit, their signals add up and the received signal can be represented as

$$
S ^ {\prime} = S _ {A} ^ {\prime} + S _ {B} ^ {\prime} \tag {2}
$$

where $S _ { A } ^ { \prime } = h _ { A } S _ { A }$ and $S _ { B } ^ { \prime } = h _ { B } S _ { B }$ refer to Alice’s and Bob’s signals after traversing their corresponding channels to the receiver. These two general features in wireless communications are also hold in backscatter links.

Now we consider the simple scenario that the signal propagates through the LOS between reader and tags without any surrounding objects (e.g. no reflections and flash.). In this situation, there are only two basic channels between reader A and each tag $T _ { i } \colon$ forward channel $( A \to T _ { i } )$ and backward channel $( T _ { i } ~  ~ A )$ , as shown in Fig. 4. Let $h _ { A  T _ { i } }$ and $h _ { T _ { i }  A }$ be the parameters of these two basic channels. In an ideal channel model, the channel parameter is defined as follows [16]:

$$
h _ {A \rightarrow T _ {i}} = h _ {T _ {i} \rightarrow A} = \frac {1}{\left(d _ {A \rightarrow T _ {i}}\right) ^ {2}} \cdot e ^ {\mathbf {J} \theta_ {A \rightarrow T _ {i}}} \tag {3}
$$

where the term J denotes the imaginary number and the term $e ^ { \mathbf { J } \theta }$ represents a complex exponential signal. The $d _ { A  T _ { i } }$ is the Euclidean distance between A and $T _ { i }$ . The $\theta _ { A  T _ { i } }$ is the phase shift over the distance $d _ { A  T _ { i } }$ , which can be calculated for channel wavelength λ as follows.

$$
\theta_ {A \rightarrow T _ {i}} = 2 \pi \frac {d _ {A \rightarrow T _ {i}}}{\lambda} \bmod 2 \pi \tag {4}
$$

![](images/19da4974aaff3bb25def4a826020904dc51027fbcd2eb44aa8489c3e9fb18071.jpg)



Figure 5: Signal propagation with flash. We treat the flash off wall and other static objects as if they were from a virtual reflection point W .

Apparently, $d _ { A  T _ { i } } = d _ { T _ { i }  A }$ and $h _ { A  T _ { i } } = h _ { T _ { i }  A }$ due to the geometric symmetry.

However, the real signal propagations always do not conform to the ideal model due to many factors such as gains of transmitter and receiver, reflectivity, impedance, etc. These factors may all introduce additional magnitude attenuations and phase shifts. We abstract their impacts as four unknown parameters, $h _ { A T } , h _ { A R }$ and $h _ { T T _ { i } } , h _ { T R _ { i } }$ , respectively denoting the impacts from RFID reader $A \ ' \mathrm { s }$ transmitter, RFID reader A’s receiver and tag $T _ { i } \mathrm { { ' } s }$ transmitter, tag $T _ { i } \mathrm { { ' } s }$ receiver. Notice that (1) These four parameters are unknown in practice and vary over tags and readers. (2) A tag in fact does not have obvious transceiver [16]. We use $h _ { T T _ { i } }$ and $h _ { T R _ { i } }$ to denote its internal reflection characteristics for uniform mathematical expression. Let $S _ { 0 }$ be the transmitting signal from the reader. With regard to the above additional impacts, the real signal propagations of forward and backward channels can be represented as follows.

$$
\left\{\begin{array}{l}S _ {A \rightarrow T _ {i}} = h _ {T R _ {i}} h _ {A \rightarrow T _ {i}} h _ {A T} S _ {0}\\S _ {T _ {i} \rightarrow A} = h _ {A R} h _ {T _ {i} \rightarrow A} h _ {T T _ {i}} S _ {A \rightarrow T _ {i}}\end{array}\right. \tag {5}
$$

where $S _ { A  T _ { i } }$ is the signal received by $T _ { i }$ and $S _ { T _ { i }  A }$ is the backscatter signal received by A. Merging these two equations, we have

$$
S _ {T _ {i} \rightarrow A} = h _ {A R} h _ {T _ {i} \rightarrow A} h _ {T T _ {i}} h _ {T R _ {i}} h _ {A \rightarrow T _ {i}} h _ {A T} S _ {0} \tag {6}
$$

How to estimate the received signal? Tadar views each read of tag as one channel estimation. Suppose $\tilde { a } _ { T _ { i }  A }$ and ${ \tilde { \theta } } _ { T _ { i }  A }$ are the magnitude and phase values about $T _ { i }$ reported by the reader, then $S _ { T _ { i }  A }$ can be estimated by

$$
S _ {T _ {i} \rightarrow A} \approx \tilde {a} _ {T _ {i} \rightarrow A} e ^ {\mathbf {J} \tilde {\theta} _ {T _ {i} \rightarrow A}} \tag {7}
$$

The estimated $S _ { T _ { i }  A }$ is useful to recover the reflections from the combined backscatter signal later. Note that the reader reports the RSS in unit of dBm instead of watts so we should take a unit conversion between RSS and magnitude. For example, suppose we received $( R S S _ { T _ { i }  A } , \theta _ { T _ { i }  A } )$ , the magnitude of the backscattered signal can be estimated as follows:

$$
a _ {T _ {i} \rightarrow A} = 1 0 ^ {\sqrt {\frac {R S S _ {T _ {i} \rightarrow A}}{1 0 0 0}}} \tag {8}
$$

In spite of involvement of physical-layer information, Tadar only uses the common parameters reported by COTS reader without any modification on hardware or firmware.

# 5.2 Eliminating the Flash

To eliminate the impact of flash, we firstly consider the scenario that the tags are attached on the outer wall and no object of interest moves inside the room. The transmitting signals are reflected off the wall and other static objects like chairs. The key idea underlying Tadar is to treat these reflections as if they were from a virtual reflection point W due to the principle of linear superimposing of signals. As Fig. 15(a) shows, there is an additional signal (i.e. flash), denoted as $S _ { A  W  T _ { \bar { 1 } } }$ traveling from $A  W  T _ { i }$ i for each tag besides the two basic channels. The $S _ { A  W  T _ { i } }$ and $S _ { A  T _ { i } }$ concurrently arrive at the tag end and linearly add up with each other. Both of them are the continuous wave originated from the reader. The tag Ti uses this combined signal to modulate its ID and backscatters it to A. Then the final backscatter signal from $T _ { i } ,$ , denoted as $S _ { T _ { i } + W  A } ,$ , is also a combined signal and can be expressed as follows.

![](images/efb0d3a872213fb5a32b9e1ac30a810eacc2c8005318b494b751f895ab6778ad.jpg)



Figure 6: The signal propagation with flash and reflections. The flash and reflections off the moving object X add up at the tag end.

$$
S _ {T _ {i} + W \rightarrow A} = h _ {A R} h _ {T _ {i} \rightarrow A} h _ {T T _ {i}} (S _ {A \rightarrow T _ {i}} + S _ {A \rightarrow W \rightarrow T _ {i}}) \tag {9}
$$

Second, we consider the scenario that a moving object X appears in the room as shown in Fig. 6. There exists a third signal propagating from $A  X  T _ { i }$ . We denote the corresponding signal as $S _ { A  X  T _ { i } }$ . Similarly, the three signals linearly add up at tag $T _ { i }$ , resulting in a more complex combined backscatter signal, denoted as $S _ { T _ { i } + W + X  A } ,$ , given by:

$$
S _ {T _ {i} + W + X \rightarrow A} = \tag {10}
$$

$$
h _ {A R} h _ {T _ {i} \to A} h _ {T T _ {i}} (S _ {A \to T _ {i}} + S _ {A \to W \to T _ {i}} + S _ {A \to X \to T _ {i}})
$$

Likewise, $S _ { T _ { i } + W  A }$ and $S _ { T _ { i } + W + X  A }$ can be estimated using the measured magnitude and phase values. To eliminate the flash, we use Eqn. (10) to subtract Eqn. (9). As a result, we have

$$
S _ {T _ {i} + W + X \rightarrow A} - S _ {T _ {i} + W \rightarrow A} = h _ {A R} h _ {T _ {i} \rightarrow A} h _ {T T _ {i}} S _ {A \rightarrow X \rightarrow T _ {i}} \tag {11}
$$

In this way, the flash $( i . e . \mathrm {  { \mathrm { ~ \textit ~ { ~ S ~ } } } } _ { A  W  T _ { i } } )$ is removed in the above equation. Hence, the flash is eliminated by the end of this step. Notice if no object moves, i.e. $S _ { A  X  T _ { i } } ~ = ~ 0 .$ , then the signal difference approximately equals 0. Thus, we can also use the two signals’ difference to determine whether moving object appears or disapears in the room, introducing the following hypothesis.

HYPOTHESIS 3. In the case of absence (or presence) of moving object, the tags will suggest a signal difference lower (or higher) than a threshold. Thus, if the tags suggest the signal difference is lower (or higher) than a threshold, it indicates the absence (or presence) of moving object.

An experiment is conducted to verify this hypothesis. We keep the room empty and then let a person move into it. Fig. 7 shows that the signal difference firstly maintains in a very low level $( < 1 . 0 )$ , and then sharply increase by 4 due to the person’s reflections. The difference returns back a normal level after the person leaves. Notice that there may occur a small number of discrete false positives shown in the figure. To deal with this issue, we borrow the idea of background subtraction in computer vision [41] which is used for foreground segmentation. The main idea behind is to automatically learn and maintain a representation of the background using Gaussian model. When a new frame incomes, it classifies whether a moving object emerges or leaves. It aggregates the determination results of multiple successive frames to filter the false positives.

![](images/feafd11cf11ab865d0676d48f1192278758665e09af15ccbe1a512d742c1b72d.jpg)



Figure 7: The power of signal difference. The sampled results are shown every 200ms for visual clarity.

# 5.3 Deriving the Reflection

As Eqn. (11) shows, the signal difference implicitly contains the reflections off the moving object (i.e. $S _ { A  X  T _ { i } } )$ . On the other hand, the reflection can be further modeled as follows:

$$
S _ {A \rightarrow X \rightarrow T _ {i}} = h _ {T R _ {i}} h _ {X} h _ {A \rightarrow X \rightarrow T _ {i}} h _ {A T} S _ {0} \tag {12}
$$

where two new parameters, $h _ { X }$ and $h _ { A  X  T _ { i } }$ , are introduced. The $h _ { X }$ indicates the influence caused by the object, varying over its materials. The $h _ { A  X  T _ { i } }$ is the compound parameter of channel $A  X  T _ { i }$ , which equals

$$
h _ {A \rightarrow X \rightarrow T _ {i}} = \frac {e ^ {\mathbf {J} (\theta_ {A \rightarrow X} + \theta_ {X \rightarrow T _ {i}})}}{(d _ {A \rightarrow X} + d _ {X \rightarrow T _ {i}}) ^ {2}} \tag {13}
$$

It is the parameter that presents a clue about the moving object’s location, which will be employed to track moving object in 6. Next, we concentrate on introducing how to derive $h _ { A  X  T _ { i } }$ from the signal difference. Substituting Eqn. (12) into Eqn (11), we have

$$
S _ {T _ {i} + W + X \rightarrow A} - S _ {T _ {i} + W \rightarrow A} = \tag {14}
$$

$$
h _ {A R} h _ {T _ {i} \to A} h _ {T T _ {i}} \underbrace {h _ {T R _ {i}} h _ {X} h _ {A \to X \to T _ {i}} h _ {A T} S _ {0}} _ {S _ {A \to X \to T _ {i}}}
$$

In order to eliminate the unknown parameters, we divide Eqn. (14) by Eqn. (6) as follows.

$$
\frac {S _ {T _ {i} + W + X \rightarrow A} - S _ {T _ {i} + W \rightarrow A}}{S _ {T _ {i} \rightarrow A}} = \frac {h _ {X} h _ {A \rightarrow X \rightarrow T _ {i}}}{h _ {A \rightarrow T _ {i}}} \tag {15}
$$

Interesting, all unknown parameters (i.e. $h _ { A R } , h _ { A T } , h _ { T T _ { i } } , h _ { T R _ { i } } )$ relevant to the devices are removed. More importantly, the transmitting signal $S _ { 0 }$ are also removed so our tracking results are irrelevant to the transmitting signal. It introduces two benefits: First, we do not have to know the transmitting continuous wave, which actually depends on the internal implementation of reader and varies over the manufactures. Second, we can design a higher-gain antenna boosting the power (see 7) to increase the SNR of reflections, rather than worry about this behavior’s influence on the tracking results.

Consequently, the parameter $h _ { A  X  T _ { i } }$ can be derived as follows.

$$
h _ {A \rightarrow X \rightarrow T _ {i}} = \frac {(S _ {T _ {i} + W + X \rightarrow A} - S _ {T _ {i} + W \rightarrow A}) h _ {A \rightarrow T _ {i}}}{S _ {T _ {i} \rightarrow A}} \times \frac {1}{h _ {X}} (1 6)
$$

In this equation, $S _ { T _ { i } + W + X  A } , S _ { T _ { i } + W  A }$ and $S _ { T _ { i }  A }$ can be estimated using the reported magnitude and phase values. Meanwhile, $h _ { A  T _ { i } }$ is the parameter of ideal forward channel, which can be calculated using Eqn. (3). Note that all of these values are complex numbers. Let ${ \ddot { h } } _ { A  X  T _ { i } }$ be the estimated result, namely

$$
\begin{array}{l} \hat {h} _ {A \to X \to T _ {i}} = \frac {(S _ {T _ {i} + W + X \to A} - S _ {T _ {i} + W \to A}) h _ {A \to T _ {i}}}{S _ {T _ {i} \to A}} \\ = \hat {a} _ {A \rightarrow X \rightarrow T _ {i}} e ^ {\mathbf {J} \hat {\theta} _ {A \rightarrow X \rightarrow T _ {i}}} \tag {17} \\ \end{array}
$$

and $h _ { X } = a _ { X } e ^ { \mathbf { J } \theta _ { X } }$ . Then $h _ { A  X  T _ { i } }$ can be expressed as follows.

$$
h _ {A \rightarrow X \rightarrow T _ {i}} \approx \frac {\hat {a} _ {A \rightarrow X \rightarrow T _ {i}}}{a _ {X}} e ^ {\mathbf {J} (\hat {\theta} _ {A \rightarrow X \rightarrow T _ {i}} - \theta_ {X})} \tag {18}
$$

Unfortunately, $h _ { X }$ is still an unknown variable that cannot be removed in practice. We will discuss $h _ { X }$ in 6.

# 5.4 Putting Things Together

The discussion so far focuses on how to extract the reflections off the moving object. Now we put all the pieces together and sketch the algorithm as follows.

Step 1: Tadar learns the basic backscatter signal $S _ { T _ { i }  A }$ through LOS propagation for each tag before attaching tags on the wall.

Step 2: Tadar learns the backscatter signal $S _ { T _ { i } + W  A }$ that involves flash after attaching tags on the wall.

Step 3: Tadar measures the backscatter signal $\operatorname { S } _ { T _ { i } + W + X } [ t ]$ at read frame t. It starts to monitor moving object by detecting the signal difference $\left| S _ { T _ { i } + W + X } [ t ] - S _ { T _ { i } + W } \right|$ . If new object emerges, it estimates $\hat { h } _ { A  X  T _ { i } }$ using Eqn. (17) and delivers it to the next component (see 6).

The virtue of Tadar lies in its graceful and compact calculation only using the results reported by a COTS reader collected in three steps, despite the involvement of very complex mathematical derivation, physical-layer information and various unknown variables.

Another thing worth-noting is that RFID reader adopts TDMA fashion to successively identify each tag to avoid tag collisions,. The collided signals would be discarded. Since our algorithm performs in the application layer of reader, Tadar does not need to worry about the mutual interferences among tags. The question is how can we guarantee the object stays in the same position when reading these n tags? The modern COTS, e.g. ImpibJ R420, uses a variety of high performance features making it to read more than 1000+ tags per second [42]. Then we can perform 40 ∼ 50 frames per second. Such high-speed frame rate allows us to monitor the region very fast. It is similar to continuously capture the snapshot of surveillance region using a high-speed camera. Therefore, we have a good reason to assume that the object approximately stays in the same position during a read frame.

# 6. TRACKING MOBILE OBJECT

There are two main tracking methods employed in most of prior through-wall systems or tracking systems. The first method steers an antenna array’s beam to determine the direction of maximum energy. The direction corresponds to the signal’s spatial angle of arrival (AoA) [2, 11]. The second method estimates the time of flight by transmitting a specialized signal (e.g. pulse or FMCW) and measuring the delay between the transmitted pulse and its received echo [24]. Both of them require the customized device or specialized signals to infer the object’s location, which cannot be implemented by the ability-limited RFID tags. Alternatively, Tadar adopts a Hidden Markov Model (HMM) to track the mobile object. In this section, we firstly review the HMM and Viterbi decoding, and then discuss how to apply it into in tracking problem.

# 6.1 Hidden Markov Model

Consider a HMM whose latent Markovian state X is in one of N discrete states $\{ x _ { 1 } , x _ { 2 } , \dotsc , x _ { N } \}$ . Let the actual state at time t be denoted by $X [ t ]$ . The transition matrix

$$
\mathcal {A} = \{x _ {i} \mapsto x _ {j}: i, j = 1, 2, \dots N \} \tag {19}
$$

defines the state transition probabilities where $x _ { i } \mapsto x _ { j } = \operatorname* { P r } ( X [ t +$ $1 ] = x _ { j } \mid X [ t ] = x _ { i } )$ . The Markov chain is assumed to be stationary, so $x _ { i } \mapsto x _ { j }$ is independent of t. Let the discrete observation space be set $\left\{ y _ { 1 } , y _ { 2 } , \dots , y _ { M } \right\}$ with the cardinality of M . Let $Y [ t ]$ be the observation symbol at time t. The observation matrix

$$
\mathcal {B} = \{x _ {i} \mapsto y _ {k}: i = 1, 2, \dots N; k = 1, 2, \dots , M \} \tag {20}
$$

defines the emission probability where $x _ { i } \mapsto y _ { k } = \operatorname* { P r } ( Y [ t ] =$ $y _ { k } \mid X [ t ] = x _ { i } )$ . The initial state distribution is given by

$$
\Pi = \left\{\alpha_ {1}, \alpha_ {2} \dots , \alpha_ {M} \right\} \tag {21}
$$

where $\alpha _ { i } = \mathrm { P r } ( X [ 0 ] = x _ { i } )$ . The HMM is used to solve three kinds of problems. Here we concern the most famous one that given HMM models $\{ A , B , \Pi \}$ and a sequence of observations, $\{ Y [ \bar { 1 } ] $ $Y [ 2 ]  \cdots  Y [ t ] \}$ , to find an optimal state sequence for the underlying Markov process. This problem can be resolved by the Viterbi decoding.

# 6.2 Tracking Object via HMM

Inspired by HMM, Tadar treats the object’s location as the hidden states and the reflections off the moving object as the observations. Then, our tracking problem is transformed to finding the maximum likelihood sequence of positions it traversed given a sequence of reflections. The crucial task is how to represent our problem in form of HMM (i.e. ( , , Π)). Below we describe the modeling process.

Hidden State and Transition Probability. Tadar divides the whole surveillance room into N grids at cm-level. The hidden states are these N divided grids. We assume that the object’s movement during two consecutive frames is within a wavelength (i.e. its speed $\leq 3 4 m / s )$ . Suppose the object locates at $x _ { i }$ currently, it may stay at xi or move to next grid $x _ { j }$ with the constraint of $d _ { x _ { i } \to x _ { i } } \ \leq \ \lambda$ . We do not make any assumptions about the motion behavior, and use uniform transition probability between adjacent steps.

DEFINITION 1 (TRANSITION PROBABILITY). Given state xi and $x _ { j } ,$ the transition probability xi 7→ xj is defined as follows.

$$
x _ {i} \mapsto x _ {j} = \left\{ \begin{array}{l l} 1 / | \{x _ {k}: d _ {x _ {i} \to x _ {k}} \leq \lambda \} | & i f d _ {x _ {i} \to x _ {j}} \leq \lambda . \\ 0 & o t h e r w i s e. \end{array} \right.
$$

where $k = \{ 1 , \ldots , N \}$ and $| \cdot |$ is the cardinality. The grids in $\{ x _ { k } : d _ { x _ { i } \to x _ { k } } \leq \lambda \}$ are called as the $x _ { i } \ ' s$ neighbors, which are reachable within λ from $x _ { i } .$ .

Two points are worth-noting. First, $x _ { i } \ ' _ { \mathbf { S } }$ neighbors include itself because the object may remain at grid xi. Second, the grids near to that in edges of surveillance region have less neighbors than those grids in the center.

![](images/aef1221505b4c2e2f46a22e49b6659a7b7effdb83a23b3d40b01adf9a5b42ae9.jpg)



Figure 8: The distribution of emission probability. The object locates at grid (70, 100).

Initial State Distribution. We also do not make any assumption about the object’s initial location (i.e. it may emerge at anywhere), so $\alpha _ { i } \ = \ 1 / N$ . In practice, if the door is the only way that the person enters the room, we should adjust the grids near to the door with higher probabilities.

Observation and Emission Probability. The transmitting signals are scattered to one or more paths after reflected due to the none uniformities of object’s surface. Thus, the reflections off the object can be received by multiple tags in the array. On the frame t incomes, the observation $Y [ t ]$ is a vector including n reflections from n tags. The observation ${ \dot { Y } } [ t ]$ can be formalized as follows.

$$
Y [ t ] = \left[ h _ {A \rightarrow X [ t ] \rightarrow T _ {1}}, \dots , h _ {A \rightarrow X [ t ] \rightarrow T _ {n}} \right] \tag {22}
$$

where $h _ { A  X [ t ]  T _ { i } }$ is the reflection extracted from tag Ti’s backscatter signal. The emission probability for a given state presents the probability of seeing the object locates at the grid conditioned on the reflections. Correctly modeling the emission probability is a crucial task for trajectory estimation. We adopt the phase value as the metric to depict emission probability. Due to thermal noise, the measured phase value ${ \tilde { \theta } } _ { A  X [ t ]  T _ { \uparrow } }$ i is a random variable following a Gaussian model. Namely,

$$
\tilde {\theta} _ {A \to X [ t ] \to T _ {i}} \sim \mathcal {N} (\theta_ {A \to X [ t ] \to T _ {i}}, \sigma)
$$

where $\theta _ { A  X [ t ]  T _ { i } }$ is the expectation $( i . e . \quad E ( \tilde { \theta } _ { A  X [ t ]  T _ { i } } ) =$ $ { \theta _ { A \to X [ t ] \to T _ { i } } } )$ , and σ is the standard deviation. The object is supposed to located at $X [ t ]$ so the expectation in theory should equal to

$$
E \left(\tilde {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {i}}\right) = \theta_ {A \rightarrow X [ t ]} + \theta_ {X [ t ] \rightarrow T _ {i}} \tag {23}
$$

Unfortunately, we can only estimate $\widehat { \theta } _ { A  X [ t ]  T _ { i } }$ rather than $ { \tilde { \theta } } _ { A  X [ t ]  T _ { i } }$ in practice due to the unknown variable $\theta _ { X }$ , as shown in Eqn. (18). Their relationships are shown as follows:

$$
\tilde {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {i}} = \hat {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {i}} - \theta_ {X} \tag {24}
$$

The fact is that $\theta _ { X }$ is common term over different tags (because all reflections come from the same object). We select one of them $( e . g . ~ T _ { j } )$ as a reference and compute the phase difference, denoted as $\Delta \ddot { \theta } _ { i , j } ,$ , as follows.

$$
\begin{array}{l} \Delta \tilde {\theta} _ {i, j} = \tilde {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {i}} - \tilde {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {j}} \tag {25} \\ = \left(\hat {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {i}} - \theta_ {X}\right) - \left(\hat {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {j}} - \theta_ {X}\right) \\ { = } { \hat { \theta } _ { A \to X [ t ] \to T _ { i } } - \hat { \theta } _ { A \to X [ t ] \to T _ { j } } } \\ \end{array}
$$

Obviously, the unknown variable $\theta _ { X }$ is removed from the above equation, so phase difference $\Delta \tilde { \theta } _ { i , j }$ can be estimated using Eqn. (17).

![](images/9acdea6d8fcaa0f8fb9093ef0e2d165578a311bed3148abf8d34a9c07706cfa3.jpg)



Figure 9: Antenna array beams. Each pair of tags produces a hyperbola.

Since the mean of the difference of two random variables equals the difference of their expectations, the expectation $\mathrm { o f } E ( \Delta \tilde { \theta } _ { i , j } )$ is given by

$$
E (\Delta \tilde {\theta} _ {i, j}) = E (\tilde {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {i}}) - E (\tilde {\theta} _ {A \rightarrow X [ t ] \rightarrow T _ {j}}) \tag {26}
$$

$$
{ = } { \left( \theta _ { A \to X [ t ] } + \theta _ { X [ t ] \to T _ { i } } \right) - \left( \theta _ { A \to X [ t ] } + \theta _ { X [ t ] \to T _ { j } } \right) }
$$

$$
{ = } { \theta _ { X [ t ] \to T _ { i } } - \theta _ { X [ t ] \to T _ { j } } }
$$

The variance of the difference of two random variables is the sum of their variances. Thus, $\mathrm { V a r } ( \Delta \tilde { \theta } _ { i , j } ) = \sqrt { 2 } \sigma$ . The standard deviation is irrelevant to object’s location but depends on the reader’s transceiver. It can be trained in advance. Totally, we have

$$
\Delta \tilde {\theta} _ {i, j} \sim \mathcal {N} \left(E (\Delta \tilde {\theta} _ {i, j}), \sqrt {2} \sigma\right) \tag {27}
$$

Then the emission probability is defined as follows.

DEFINITION 2 (EMISSION PROBABILITY). The emission probability governs the distribution of the observations when the object locates at $X [ t ] _ { : }$ , which is defined as follows:

$$
\begin{array}{l} X [ t ] \mapsto Y [ t ] = \operatorname * {P r} \left(\left[ h _ {A \to X [ t ] \to T _ {1}}, \dots , h _ {A \to X [ t ] \to T _ {N}} \right] \mid X [ t ]\right) \\ = \frac {1}{N} \sum_ {i = 1} ^ {N} F (\Delta \tilde {\theta} _ {i, j}; E (\Delta \tilde {\theta} _ {i, j}), \sqrt {2} \sigma) \\ \end{array}
$$

where $F ( X ; \mu , \sigma )$ is the cumulative probability function of Gaussian distribution $\mathcal { N } ( \mu , \sigma )$ .

One important reason using HMM and Viterbi decoding for our tracking is that they can reduce the computations for each step considering the principle of moving continuity in time-domain. It is not necessary to search the whole surveillance region every read frame. Fig. 8 shows the distribution of emission probability from one of our experiments where the tag array is deployed in the negative direction of Y-axis. We observe that the the emission probability achieves the highest probability at the ground truth and diffuses to its neighbors as expected.

# 6.3 Further Discussion

It is known that the phase value repeats every a wavelength. How can we ensure the $X [ t ] \mapsto Y [ t ]$ archives the maximum when visiting the correct grid $\dot { X } [ t ]$ given the observation $Y [ t ] \ ?$ Suppose $\theta _ { i }$ and $\theta _ { j } , \theta _ { i } , \theta _ { j } \in [ 0 , 2 \pi ]$ , are the phases of reflections off object X received by tag $T _ { i }$ and $T _ { j }$ . The distances and the received signal phases have the following relations due to the phase rotation:

$$
\left\{\begin{array}{l}\theta_ {i} = \frac {2 \pi}{\lambda} d _ {A \rightarrow X \rightarrow T _ {i}} \bmod 2 \pi\\\theta_ {j} = \frac {2 \pi}{\lambda} d _ {A \rightarrow X \rightarrow T _ {j}} \bmod 2 \pi\end{array}\right. \tag {28}
$$

![](images/6466479e7b899ce80d16692f2d82b4a9a5616ac59563cd7001f814827d6e2b16.jpg)



(a) Antenna

![](images/790bac75b92b4b0469ad49352cd6477d67b3c3f5d7bcdba0b69c1439bfb08c66.jpg)



(b) Tag array   
Figure 10: Tadar’s setup. A plastic box is used to facilitate our tests. (a) An antenna is fixed on the bottom. (b) A group of tags are attached on its top.

Hence, the phase difference, $\Delta \theta _ { i , j } = \theta _ { i } - \theta _ { j }$ , between the received signals at the two tags relates to the difference in their distances from the object, $\Delta d _ { i , j } = d _ { A  X  T _ { i } } - d _ { A  X  T _ { j } }$ , as follows.

$$
\Delta d _ {i, j} = \lambda (\frac {\Delta \theta_ {i , j}}{2 \pi} + k) \tag {29}
$$

where k can be any integer in $\begin{array} { r } { [ - \frac { D } { \lambda } - \frac { \Delta \theta _ { i , j } } { 2 \pi } , - \frac { D } { \lambda } + \frac { \Delta \theta _ { i , j } } { 2 \pi } ] } \end{array}$ ∆θi,j ∆θi,j ] and D is the distance between two tags. In our scenario, the $\dot { \boldsymbol k } = 0$ or 1 because all tags are deployed within one wavelength. Thus, the phase difference $\Delta \theta _ { i , j }$ used in emission probability is equivalent to the distance difference $\Delta d _ { i , j }$ in essence.

$$
\begin{array}{l} \Delta d _ {i, j} = d _ {A \rightarrow X \rightarrow T _ {i}} - d _ {A \rightarrow X \rightarrow T _ {j}} \\ = \left(d _ {A \rightarrow X} + d _ {X \rightarrow T _ {i}}\right) - \left(d _ {A \rightarrow X} + d _ {X \rightarrow T _ {j}}\right) \\ = d _ {X \rightarrow T _ {i}} - d _ {X \rightarrow T _ {j}} \\ \end{array}
$$

The above equation is a standard equation representing one hyperbola that focuses on $T _ { i }$ and $T _ { j } .$ . Thus, the emission probability actually indicates how the assumed location (i.e. the hidden state) matches the $n - 1$ hyperbolas. The phase ambiguity is removed by multiple hyperbolas. Fig. 9 shows the 4 hyperbolas including 8 branches produced by the 4 phase differences where the third tag is chosen as the reference. All these curves intersect on the ground truth.

# 7. IMPLEMENTATION

We build a prototype of Tadar using the COTS RFID reader and tags. Fig. 10 shows the main setup of our devices. We use a plastic box to maintain the geometric relationships between reader antenna and tags instead of attaching them on wall for convenience, because we would move the array to different buildings with a same setting. In details, we deploy the reader antenna on the bottom and attach $5 \times 9$ tags on the top. The box’s dimension is $6 1 \times 4 3 \times 3 3 c m ^ { 3 }$ . Tags are separated by 5cm.

RFID: We adopt one ImpinJ Speedway modeled R420 reader [43] without any hardware or firmware modification. The reader is compatible with EPC Gen2 standard [28]. The whole RFID system operates in the $9 2 0 ~ \sim ~ 9 2 6 ~ \mathrm { M H z }$ band. We use the Alien tags modeled $^ { \mathrm { * * } } 2 \times 2 ^ { \mathrm { * * } } ( 2 . 2 5 \times 2 . 2 5 c m ^ { 2 } )$ [44], which are widely used in supply chain applications. Each of them costs 5 cents.

Boosting power: The reflections off the wall are $3 0 \sim 4 0 $ dB above the that off moving objects. Even eliminating the flash effect, we can hardly discern the reflections due to human because it is too weak and immersed in the receiver’s hardware noise. To boost the power, we build an antenna with 4 patches, as shown in Fig. 11(a). The antenna has a directional gain of 12 dBi, a 3 dB beam width of $4 0 ^ { \circ } .$ . Fig. 11(b) shows the comparisons between the antenna with the ordinary antenna with 8 dBi. Our antenna is composed of a couple of two-layer boards (boards with two copper layers and one substrate layer) that are physically connected to each other by plastic screws.

![](images/9ae85cc529a0a42ed655154c363c3cf76a179df78a7bb429d4c4cc1992a64e4a.jpg)



(a) 12dBi

![](images/e2e99a511f71a0a38f59998c41591128e22529587170d1ea63b94ae9f63e4ac3.jpg)



(b) 8dBi   
Figure 11: Antenna design. We design a high-gain directional antenna with 12dBi to boost power. (a) The 12dBi antenna with four patches. (b) The comparisons of our antenna with 8dBi antenna employed in logistics.

Experiment setup: Majority of our experiments are performed at our conference rooms in one office building. The conference room is $7 \times 4 m ^ { 2 }$ . There are one big table $( 4 \times 0 . 7 5 m ^ { 2 } )$ , twelve chairs, one white board, etc. The interior walls of the building are $5 ^ { \prime \prime }$ hollow walls supported by steel frames with sheet rock on top. To discuss the effect of building materials, we also conduct some experiments in a second building with $8 ^ { \prime \prime }$ concrete walls. To seize the ground truth, we command an iRobot Create robot with a $1 2 ^ { \prime \prime }$ Lenovo notebook as the reflector to move along a programed trajectory. We also invite 5 human subjects with different heights and builds for the application study. Each experiment is repeated for many times and the average value is reported only. The coordinate system is shown in Fig. 10(b) that the origin locates at the center of the tag array and the signal is emitted to positive direction of Y-axis.

# 8. EVALUATION

In this section, we evaluate Tadar from aspects of reflection acquisition, diversity elimination and object tracking.

# 8.1 Reflection Acquisition

First, we would like to automate the thresholds for the presence of moving objects. To this end, we investigate the SNRs in different scenarios. The SNR is defined as power ratio of signals acquired in presence to absence of moving objects in the room. The reflections with very weak SNR will be overwhelmed by the noise. In this experiment, we place the object at a distance of 3m away from the wall. We choose three typical kinds of materials: $0 . 9 8 ^ { \prime \prime }$ glass, $1 . 5 ^ { \prime \prime }$ wood door and $5 ^ { \prime \prime }$ hollow wall to measure their SNRs. The results in form of CDFs are plotted in Fig. 12. Each CDF contains more than 2000 samples with presence of moving objects. The average SNRs detected are 10.61, 4.69 and 7.01. As expected, the thicker and denser the obstructing material, the harder it is for Tadar to capture reflections from behind it. However, the power level is 4 higher than that of noise even in the worst case.

Second, we evaluate Tadar’s detection range considering four different building materials including $5 ^ { \prime \prime }$ hollow wall (C2), $1 . 5 ^ { \prime \prime }$ wood door (C3), $0 . 9 8 ^ { \prime \prime }$ glass (C4), and $8 ^ { \prime \prime }$ concrete (C5). We also perform experiments in free space (C1) with no obstruction between tag and the object. The range is the maximum distance that Tadar can detect the object. The results are shown in Fig. 13, which are consistent with the comparisons of SNRs. Specifically, Tadar can detect the object with a range of 7.6m in free space, and achieve a median range of 6m, 6.77m, 7.5m and 4.12m in other four different buildings materials. RFID system working at 800  900 MHz UHF has a bit weaker penetrability compared with the UWB technologies. After all, RFID system is not designed for see-through-wall originally. However, the benefits of Tadar are obvious in that it is low-cost, compact and without needs of specialized signals or customized devices.

![](images/95661767fc7b830f3b509b14397a121371bbf10833ed4f5e3bd67c3a26a1314d.jpg)



Figure 12: SNR Comparisons

![](images/e74e3da7412cd1adcf524cadbb5e063617d3442c5ca72360bbf7afd4ff504efe.jpg)



Figure 13: Detecting Range

![](images/6fe5abb783aa71a11dfcc70854b156d48c97caa46333c108457597d2d6cdae28.jpg)



Figure 14: Tracking Accuracy

![](images/5c5c5c059e61f28b489ea903ebbf6273f10a10d75e7e5a8448a69366ba53a27c.jpg)



(a) $| S _ { T _ { i }  A } |$

![](images/102f839d9f60a69d4fa0ef7b088555a99d6b367a01694aa38d2f09cab5d08052.jpg)



(b) $| S _ { T _ { i } + X  A } |$

![](images/d0d4b2457c7acc36b2c0e5932feede9db82b16471de319a2b01020ca1151bbb5.jpg)



(c) $\vert \hat { h } _ { { T } _ { i } + X  A } \vert$   
Figure 15: Magnitude distribution based on tag array. The array includes 12 × 8 tags. Each grid denotes a result collected from the corresponding tag. (a) The signal collected with an empty room. (b) The signal collected when an iPhone 6 Plus is placed in front of the wall. (c) The separated reflections.

Summary. The above two experiments show that Tadar has good behaviors in acquisition of reflections. There are three main reasons for this feature. First, the RFID technology originates from the radar so the RFID devices have the strong ability to resolve the weak signals and remove the self-interference [45]. This feature helps Tadar well suppress the environmental and thermal noise. Second, Tadar utilizes the continuous wave transmitted from the reader to light up the objects. The CW is very stable because it does not carry any information, which facilitates the removal of flash using the learned signals. Third, the tag has no hardware filters for saving cost such that it is hypersensitive to ‘interferences’, enabling us to capture the weak reflections off surrounding objects.

# 8.2 Diversity Elimination

Third, we would like to know whether the unknown parameters related to devices are well removed from the results. To visually understand this issue, let us consider a simple setup with $1 2 \times 8$ tags attached on the wall. Fig. 15(a) plots the magnitudes of signals backscattered from these 96 tags with an empty room. A grid in the figure denotes a tag’s result. The antenna is deployed at the center. In the ideal wireless model, the magnitude values would descend from center to edges because the magnitude goes as the inverse twice power of the distance (see Eqn. 3). However, the distribution is out of order due to the affects from those unknown parameters $( h _ { A T _ { i } } , h _ { A R } , h _ { T T _ { i } }$ , and $h _ { T R _ { i } } )$ . Then we place an iPhone 6 Plus in front of the wall with a distance of 1m. Fig. 15(b) again plots the magnitudes collected from those tags. In total, several grids are lightly brightened (thus large RSS values) because their signals are strengthened by the reflections. However, the results are still too ambiguous to pinpoint the iPhone. Fig. 15(c) plots the magnitude of $\hat { h } _ { A  X  T _ { i } }$ . The result shows quite in agreement with the ideal wireless model. We can even point out the area the phone locates as the tags under the phone have higher values. Specifically, the tag right below the phone has the maximum value. This example demonstrates that $\hat { h } _ { A  X  T _ { i } }$ indeed well eliminates the impacts from the unknown diversities.

# 8.3 Object Tracking

Fourth, we investigate Tadar’s tracking accuracy compared with other five methods. In the experiments, we let the robot move along a predefined track and then use the HMM and reflections to estimate its trajectory. The accuracy is calculated using the difference of the estimated trajectory and the ground truth. The comparisons are shown in Fig. 14.

NRES: NRES [18] deploys a large number of WSN nodes around the room, and tracks humans in building using changes in the signal strength incurred by the human’s motions. It obtains a median tracking error of 60cm.

TagTrack: TagTrack [19] is the similar attempt using RFID signals to passively localize the objects. It deploys the tags around the objects and employs the RSS changes as the tracking indicator. It improves the result by introducing classification technique, and achieves a median error distance of 70cm. However, TagTrack is not a see-through-wall technology because the backscatter signals cannot traverse through a wall.

![](images/11c729f386292ca24d1a6a175b71a2fced2a2d1b2186e3fbe9ef98acb7bd4b56.jpg)



Figure 16: Encoding gesture

![](images/041419fc603b61ec51eba1956d3a6a69330652238cca1315fbf45fa77a2eb62c.jpg)



Figure 17: Decoding gesture

![](images/da3ccf9e6af524e8712e0dcbc1249662f31250abf57c414654850160a835e508.jpg)



Figure 18: Gesture Accuracy

Wision: Wision [20] leverages the multi-path propagations to perform object imaging using two-dimensional antenna arrays. Wision localizes static humans (Wison/H) with a median accuracy of 26cm and metallic objects (Wison/M), like MacBook and HP desktop, with a median of 15cm. Wision suffers from the effects from objects’ materials, which is removed in Tadar by comparing with the reference tag. Note that Wision is also not a see-through-wall method.

WiTrack and WiZ: WiTrack [24] is a system that localizes the user’s motion in three-dimensional space from the radio signals reflected off his/her body. It localizes the center of a human body to within a median of 27cm. WiZ [25] is an incremental work extending WiTrack to multi-person and obtains a median of 15cm. Both WiTrack and WiZ needs a customized hardware to transmit a well-designed radio signal (e.g. FMCW) for estimating the traveling time. WiZ generate a signal that sweeps 5.46 ∼ 7.25 GHz, so both of them, strictly speaking, are UWB based methods.

Tadar: Tadar’s tracking errors are exhibited in two dimensions. It can achieve a median of tracking error of 7.8cm and 20cm at X and Y dimensions. It outperforms the existing none-UWB technologies by 3 , 3.5 and 1.3 compared with NRES, TagTrack and Wision, and performs as well as WiTrack and WiZ3. Why the results show such a dramatic difference in two dimensions? Reviewing Fig. 9, we see that all hyperbolas of emission probability are towards X-axis because all tags are deployed on one side of the surveillance region only. This incurs a lower discernibility at Y-axis. To coverage the results along Y-axis, we could attach two arrays of tags on two sides of the room. In this way, the combined error can be further reduced to a median of 9.8cm.

Summary: Totally, Tadar improves the see-through and tracking technology from three main aspects. First, Tadar well eliminates all uncertain variables (e.g. device diversity, reflectivity differences etc) in calculations. Second, the low cost of RFID tags allows us to deploy a large number of tags to acquire reflections, which helps improve the accuracy. Specifically, the cost of each antenna, used in Wision and WiTrack, is able to purchase 40 ∼ 50 RFID tags, while Wision needs to consume 64 antennas ( the same price as the sum of 3200 tags). Third, the deployment of Tadar is easier and more compact than other methods, facilitating its application in various domains.

# 8.4 Cost Comparisons

One of the virtues of the Tadar is low cost. Lastly, we investigate the cost comparisons with other through-wall technologies.

Military radar. Through-wall imaging and tracking in radar community is very mature. We search the military-level throughwall radars in Alibaba and find the prices of radar devices are ranged between 80, 000  90, 000 US dollars, 40 as much as ours on average. Apparently, our solution is very low-cost compared with the military radar. In addition, the through-wall radar systems in the market are usually prohibited from selling to civilians in most countries in the world. Our system targets to civilian purpose with COTS devices, which is totally legal in any country. This benefit cannot be offered by the military radar.

Wi-Fi based methods. Wi-Fi based through-wall technologeis need a set of software-defined radio like USRP or WARP to emit customized signals [11, 24, 25]. The total price of USRP including antennas is more than 2000 US dollars, a little higher than ours. However, we must claim that our solution totally employs the COTS devices with industry-level design and encapsulation, which can be deployed without any modification on the hardware. The tracking algorithms can run at normal PC computer. With regard to the price and convenience, we insist our solution is prior to the Wi-Fi based.

WSN based methods. Some past work in radio tomography employs hundred sensors to track a person passively. No matter the approach is linked-based or location-based, they need deploy a large number of nodes around the room to enable the links cover the entire region. Unlike our approach that deploys the tags in one side, the need cover the room from various angles. So their approach is limited by the room arrangement. With regard to the price, 200 nodes costs about 10,000 US dollars, 5× as much as ours.

Summary: We adopt a powerful reader, ImpinJ R420, to build our prototype. The reader costs about 2, 000 US dollars. At first blush, it is not cheap enough. This is because this reader is specially designed for logistics and transportation. There is a very costly industrial computer, serving as a stable HTTP/TCP server, inside the reader to fulfill offline surveillance. In our scenario, we can construct a simpler and cheaper reader only using the reader chip (like Indy RS2000). There is a large space to reduce the system cost. For example, the ThingMagic reader does not embed industrial computer. Its price is around 700 dollars, which is much lower than that of the R420. We will consider the way to further reduce the cost in our future work. Even considering the cost of the current prototype, the low cost is still a major advantage of our solution prior to other methods.

# 9. APPLICATION STUDY

One of the most popular applications in research community recently is to communicate commands or short message to a system by tracking human’s movements or gestures, e.g. [11, 46–48]. We also investigate this application using Tadar.

Gesture encoding and decoding. Tadar is more sensitive to the X-axis so we employ the rightward (X+) or leftward (X-) movement for gesture encoding. We adopt the Manchester-like encoding as proposed in Wi-Vi [11]: a ‘0’ bit is a step leftward followed by a step rightward; a ‘1’ bit is a step rightward followed by a step leftward, as shown in Fig. 16. This modulation is very simple so that a human finds it easy to perform them and compose them. To support such gesture encoding, Tadar firstly locates the human and then calculates the angle β, defined as the angle related to the vertical line. For example, Fig. 17 shows a sequence of angles detected when a subject repeatedly walks rightward and leftward. The angle equals zero when he locates at the vertical line, and becomes negative when across the vertical line to right. The main reason that we use angle for encoding instead of his absolute positions is that the human may be not know where he is. The input of this application is the angle sequence. Tadar applies two matched filters: one for the step leftward and one for the step rightward. Note that the human can change his direction at anywhere without need of coming back to the vertical line.

Evaluation. We evaluate Tadar’s ability to decode the bits associated with the gesture. All the experiments are conducted in our conference room. In each experiment, we ask a volunteer to randomly stand at the conference room, and perform the two gestures. He walks in a way that he finds comfortable. Total 5 subjects take part in experiments. The experiments are repeated with various range from 1 ∼ 6m. Fig. 18 plots the fraction of experiments that the gestures are exactly decoded. We observe that Tadar can successfully decode the gestures at all distances within 3m. The percentage falls to 75% when the distance increases to the 4m. The decoding accuracy of Wi-Vi [11] is better than that of Tadar when the distance is longer than 4m. However, Wi-Vi cannot exactly pinpoint his location.

# 10. LIMITATIONS

Tadar marks an important contribution by enabling device-free mobile object tracking. It, however, still has some limitations that are left for future work.

Direction-dependent: Both the RFID tags and reader antenna are directional, so the whole system is also direction-dependent. Current prototype distributes tags in a fairly large area to enable them to capture different perspectives of the mobile objects in the scene. Our future research may advance at both hardware and algorithmic to reduce the dependence of direction allowing for the tags to be stacked within a smaller area.

Learning environment: A second limitation stems from the fact the Tadar needs to train the channel parameters of empty room in advance to eliminate the flash effects. Not all situations, especially in the case of emergency, allow the user to learn the environment ahead. Our future research may address this issue by detecting the differences of two consecutive frames.

Tracking one object: Our algorithm design presented in this paper can track only one mobile object at any point in time. When there are multiple objects present in the scene, the reflections off multiple objects would overlapped together. This limitation is not fundamental to the design of Tadar and can be addressed as the research evolves. For example, considering the case of K moving objects, we can model the HMM state using a K-dimensional vector. Each element in the vector indicates each object’s location. Correspondingly, the observations are modeled as the combined signal of K reflections. The optimized state conforming to all observations is the current objects’ location distributions.

Beyond FCC power limits: In order to discern the weak reflections off human, we boost the power using a 12 dBi antenna. Considering 30 dBm transmission power, it would result in 42 dBm EIRP (Equivalent Isotropically Radiated Power) which is 6 dBm more than the FCC limit. To conform the FCC limit, Tadar would be confined to detect the objects with high-reflective metallic surface.

Although there is scope for many improvements, we believe that Tadar inspires us from another different perspective to advance the through-wall technology and other various aspects [49, 50].

# 11. CONCLUSION

In this work, we present Tadar for tracking moving objects without instrumenting them using COTS RFID readers and tags. It works even through walls and behind closed rooms. A key innovation is to logically transform a group of tags into an antenna array receiving the reflections from surrounding objects. We believe that it will open up a wide range of exciting opportunities bridging our physical world and the cyber world.

# ACKNOWLEDGMENT

The research is supported by NSF China Major Program 61190110. The research of Lei Yang is supported by China Postdoctoral Science Foundation funded project under NO. 2015M570100. The research of Xiangyang Li is supported by NSF ECCS-1247944, NSF ECCS-1343306, NSF CMMI 1436786, National Natural Science Foundation of China under Grant No. 61170216 and No. 61228202. We thank all the reviewers and shepherds for their valuable comments and helpful suggestions.

# 12. REFERENCES

[1] Lei Yang, Yekui Chen, Xiang-Yang Li, Chaowei Xiao, Mo Li, and Yunhao Liu. Tagoram: real-time tracking of mobile rfid tags to high precision using cots devices. In Proc. ACM MOBICOM, 2014.   
[2] Jue Wang and Dina Katabi. Dude, where’s my card?: Rfid positioning that works with multipath and non-line of sight. In Proc. of ACM SIGCOMM, 2013.   
[3] Jue Wang, Deepak Vasisht, and Dina Katabi. Rf-idraw: virtual touch screen in the air using rf signals. In Proc. of ACM SIGCOMM, 2014.   
[4] Jie Xiong and Kyle Jamieson. Arraytrack: A fine-grained indoor location system. In Proc. of USENIX NSDI, 2013.   
[5] Tyler S Ralston, Gregory L Charvat, and John E Peabody. Real-time through-wall imaging using an ultrawideband multiple-input multiple-output (mimo) phased array radar system. In Proc. of IEEE ARRAY, 2010.   
[6] Gregory L Charvat, Leo C Kempel, Edward J Rothwell, Christopher M Coleman, and E Mokole. An ultrawideband (uwb) switched-antenna-array radar imaging system. In Proc. of IEEE ARRAY, 2010.   
[7] Seeing through walls-MIT’s Lincoln Laboratory. http: //www.youtube.com/watch?v=H5xmo7iJ7KA.   
[8] Yunqiang Yang and Aly E Fathy. See-through-wall imaging using ultra wideband short-pulse radar system. In IEEE Symposium on Antennas and Propagation Society, volume 3, pages 334–337, 2005.   
[9] Through-wall Radar. http://www.alibaba.com/product-detail/ Rescue-tool-Through-wall-radar-Prism 60010869781.html.   
[10] Kevin Chetty, Graeme E Smith, and Karl Woodbridge. Through-the-wall sensing of personnel using passive bistatic

wifi radar at standoff distances. IEEE Transactions on Geoscience and Remote Sensing, 50(4):1218–1226, 2012.   
[11] Fadel Adib and Dina Katabi. See through walls with wifi! In Proc. of ACM SIGCOMM, 2013.   
[12] WiSee. http://wisee.cs.washington.edu/.   
[13] Qifan Pu, Sidhant Gupta, Shyamnath Gollakota, and Shwetak Patel. Whole-home gesture recognition using wireless signals. In Proc. of ACM MOBICOM, 2013.   
[14] Saandeep Depatla, Lucas Buckland, and Yasamin Mostofi. X-ray vision with only wifi power measurements using rytov wave models. IEEE Transactions on Vehicular Technology, 2015.   
[15] X-Ray Vision. https://www.youtube.com/watch? v=iF1fY3bPAt0&t=11.   
[16] Daniel M Dobkin. The RF in RFID: UHF RFID in Practice. Newnes, 2012.   
[17] Lei Yang, Jinsong Han, Yong Qi, Cheng Wang, Tao Gu, and Yunhao Liu. Season: Shelving interference and joint identification in large-scale rfid systems. In Proc. of IEEE INFOCOM, 2011.   
[18] Yang Zhao, Neal Patwari, Jeff M Phillips, and Suresh Venkatasubramanian. Radio tomographic imaging and tracking of stationary and moving people via kernel distance. In Proc. of ACM IPSN, 2013.   
[19] Wenjie Ruan, Lina Yao, Quan Z Sheng, Nickolas JG Falkner, and Xue Li. Tagtrack: device-free localization and tracking using passive rfid tags. In Proc. of Ubiquitous, 2014.   
[20] Donny Huang, Rajalakshmi Nandakumar, and Shyamnath Gollakota. Feasibility and limits of wi-fi imaging. In Proc. of ACM SenSys, 2014.   
[21] Gregory L Charvat, Leo C Kempel, Edward J Rothwell, Christopher M Coleman, and E Mokole. A through-dielectric radar imaging system. IEEE Transactions on Antennas and Propagation, 58(8), 2010.   
[22] Fauzia Ahmad, Yimin Zhang, and Moeness G Amin. Three-dimensional wideband beamforming for imaging through a single wall. IEEE Geoscience and Remote Sensing Letters, 5(2):176–179, 2008.   
[23] Qiong Huang, Lele Qu, Bingheng Wu, and Guangyou Fang. Uwb through-wall imaging based on compressive sensing. IEEE Transactions on Geoscience and Remote Sensing, 48(3):1408–1415, 2010.   
[24] Fadel Adib, Zach Kabelac, Dina Katabi, and Robert C Miller. 3d tracking via body radio reflections. In Proc. of USENIX NSDI, volume 14, 2013.   
[25] Fadel Adib, Zachary Kabelac, and Dina Katabi. Multi-person motion tracking via rf body reflections. In Proc. of USENIX NSDI, 2015.   
[26] Radar Vision, Time Domain Corporation. http://www.timedomain.com.   
[27] LawrenceLivermore, National Laboratory. https://www.llnl.gov.   
[28] EPC Gen2, EPCglobal. www.gs1.org/epcglobal.   
[29] Saandeep Depatla, Lucas Buckland, and Yasamin Mostofi. X-ray vision with only wifi power measurements using rytov wave models. IEEE Transactions on Vehicular Technology, 64(4):1376–1387, 2015.   
[30] Y. Mostofi. Cooperative Wireless-Based Obstacle/Object Mapping and See-Through Capabilities in Robotic Networks. IEEE Transactions on Mobile Computing, 12(5):817–829, May 2013.

[31] Joey Wilson and Neal Patwari. A fade-level skew-laplace signal strength model for device-free localization with wireless networks. IEEE Transactions on Mobile Computing, 11(6):947–958, 2012.   
[32] Kristen Woyach, Daniele Puccinelli, and Martin Haenggi. Sensorless sensing in wireless networks: Implementation and measurements. pages 1–8. in Proc. of IEEE WIOPT, 2006.   
[33] Konstantinos Kleisouris, Bernhard Firner, Richard Howard, Yanyong Zhang, and Richard P Martin. Detecting intra-room mobility with signal strength descriptors. In Proc. of ACM MobiHoc, 2010.   
[34] Debraj De, Wen-Zhan Song, Mingsen Xu, Cheng-Liang Wang, Diane Cook, and Xiaoming Huo. Findinghumo: Real-time tracking of motion trajectories from anonymous binary sensing in smart environments. In Proc. of IEEE ICDCS, 2012.   
[35] Frederic Thouin, Santosh Nannuru, and Mark Coates. Multi-target tracking for measurement models with additive contributions. In IEEE FUSION, 2011.   
[36] Santosh Nannuru, Yunpeng Li, Yan Zeng, Mark Coates, and Bo Yang. Radio-frequency tomography for passive indoor multitarget tracking. IEEE Transactions on Mobile Computing, 12(12):2322–2333, 2013.   
[37] Dian Zhang, Yunhuai Liu, Xiaonan Guo, and Lionel M Ni. Rass: A real-time, accurate, and scalable system for tracking transceiver-free objects. IEEE Transactions on Parallel and Distributed Systems, 24(5):996–1008, 2013.   
[38] Moustafa Seifeldin and Moustafa Youssef. A deterministic large-scale device-free passive localization system for wireless environments. In Proc. of ACM ICPETRAE, 2010.   
[39] Chenren Xu, Mingchen Gao, Bernhard Firner, Yanyong Zhang, Richard Howard, and Jun Li. Towards robust device-free passive localization through automatic camera-assisted recalibration. In Proc. of ACM SenSys, 2012.   
[40] EPCglobal. Low level reader protocol (llrp). 2010.   
[41] W. Hu, T. Tan, L. Wang, and S. Maybank. A survey on visual surveillance of object motion and behaviors. IEEE Transactions on Systems, Man, and Cybernetics, 2004.   
[42] Speedway installation and operations guide.   
[43] Impinj, Inc. http://www.impinj.com/.   
[44] Alien Tags. http://www.alientechnology.com/tags/2x2/.   
[45] Jeremy Landt. The history of rfid. Potentials, IEEE, 24(4):8–11, 2005.   
[46] Joey Wilson and Neal Patwari. See-through walls: Motion tracking using variance-based radio tomography networks. IEEEE Transactions on Mobile Computing, 10(5):612–621, 2011.   
[47] Herbert Bay, Andreas Ess, Tinne Tuytelaars, and Luc Van Gool. Speeded-up robust features (surf). Computer vision and image understanding, 110(3):346–359, 2008.   
[48] Bryce Kellogg, Vamsi Talla, and Shyamnath Gollakota. Bringing gesture recognition to all devices. In Proc. of USENIX NSDI, 2014.   
[49] Zhenjiang Li, Mo Li, Jiliang Wang, and Zhichao Cao. Ubiquitous data collection for mobile users in wireless sensor networks. In Proceedings IEEE INFOCOM, pages 2246–2254, 2011.   
[50] Zhenjiang Li, Wan Du, Yuanqing Zheng, Mo Li, and Dapeng Wu. From rateless to hopless. In Proceedings of ACM MobiHoc, pages 2246–2254, 2011.