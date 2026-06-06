# Demo: High-Precision RFID Tracking Using COTS Devices

Lei Yang\*, Yekui Chen\*, Chen Chen\*, Xiang-Yang Li\*,†, Xuan Ding\*, Yi Guo‡, Yunhao Liu\*

\* School of Software and TNLIST, Tsinghua University, China
† Department of Computer Science, Illinois Institute of Technology, USA

{young, yekui, chenchen}@tagsys.org, xli@cs.iit.edu, {xuan,yi}@tagsys.org, yunhao@greenorbs.com

# ABSTRACT

In many applications, we have to identify an object and then locate the object to within high precision (centimeter- or millimeter-level). Tracking mobile RFID tags in real time has been a daunting task, especially challenging for achieving high precision. We achieve these three goals by leveraging the phase value of the backscattered signal, provided by the COTS RFID readers, to estimate the location of the object. To illustrate the basic idea of our system, we firstly focus on a simple scenario where the tag is moving along a fixed track known to the system. We propose Differential Augmented Hologram (DAH) which will facilitate the instant tracking of the mobile RFID tag to a high precision. We then devise a comprehensive solution to accurately recover the tag's moving trajectory and its locations, relaxing the assumption of knowing tag's track function in advance.

# Categories and Subject Descriptors

C.2 [Computer Systems Organization]: Computer Communications Networks

# Keywords

RFID; Tracking; Localization

# 1. INTRODUCTION

Radio Frequency IDentification (RFID) is a rapidly developing technology which uses RF signals for automatic identification of objects. One of its most promising applications is to track the mobile objects accurately. Many applications would benefit from higher tracking accuracy. For example, supermarkets can deeply mine the consumers' shopping habits by monitoring the items' trajectories. Similarly, it is useful to conduct automatic recognition of complex multi-player behaviors through the tagged football in a world-wide game. Plenty of new battery-free human-machine interactive device can be developed using the tags, like writing letters in the air by attaching a tag on a finger. Today's robots routinely replace human labor in assembly tasks. It has been of a great interest in both the robotics academic community and industry to enable

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage, and that copies bear this notice and the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s). Copyright is held by the author/owner(s).

MobiCom'14, September 7-11, 2014, Maui, Hawaii, USA.

ACM 978-1-4503-2783-1/14/09.

http://dx.doi.org/10.1145/2639108.2641743.

robot search for a desired object, pick it up, fetch and delivery it from a assembly lines. These tasks require tracking the object to cm-level and even mm-level accuracy.

We observe that the COTS RFID products support fine-grained resolution in detecting the phase of received RF signals, i.e., with accuracy $\approx 0.0015$ radians. This accuracy offers an opportunity to locate the object with accuracy of millimeter-level displacement. Developing a practical system out of the basic principle, however, entails substantial challenges. First, the RF phase measurement is affected by the basic thermal noise at the receiver side, which results in the practically measured RF phase a random variable following Gaussian distribution. How to derive a definite and accurate tracking result from the indefinite phase measurement remains challenging. Second, the device diversity in phase measurement introduces extra phase shifts we call “diversity term”. Different RFID tags or readers have different diversity terms. Prior calibration of all tags and readers is impractical and computationally infeasible and we need to carefully sidestep the problem. Third, the fast changing environment makes the phase measurement a complex result mixing RF propagation through the line-of-sight (LOS) with the None LOS. It is hard to separate them and thus non-trivial to accurately derive the tag position.

In this study, we design Tagoram, which exploits the phase value of received signal for real-time tracking of mobile tags with a high precision. We propose a hologram based approach, called Tageram, to tackle above challenges using COTS RFID tags and readers with a few physical antennas. We build an RF phase hologram with observations from different reader antennas and at different time of scan. To tackle the challenges of mobile tags, we assume the antennas moving to the opposite direction relative to the mobile tag. Such fictitious reader “mobility” offers individual RF phase observations from different positions relative to the tag, and they form an RF hologram as if they were obtained from a virtual antenna array. If the tag movement velocity and its moving track is known in advance, the positions of the antenna array relative to the tag can be determined. We can thus rely on the instant hologram to derive the initial position of the tag and thus precisely track the tag movement. In order to tackle previously identified challenges we further develop Differential Augmented Hologram (DAH) approach from the naive one. We then relax the assumption that we know the tag moving track in advance and devise a technique to accurately recover the tag movement from antenna observations. We first identify a series of candidate tag moving paths using the continuously estimated tag velocity from the antenna array. Then DAH is extended to identify the one with the highest likelihood of generating the observed RF phases. To enable real-time localization and tracking, we propose several techniques to speedup the computation of hologram.

# 2. TAGORAM DESIGN

# 2.1 Background

Passive RFID system communicates using a backscatter radio link. The tags, no battery equipped, purely harvest energy from the reader's signal. The RF phase is a common parameter supported by COTS readers. The signal traverses a total distance of 2d back and forth in backscatter communication where d is the distance between the reader antenna and the tag. Besides the RF phase rotation over distance, the reader's transmitter, the tag's reflection characteristic, and the reader's receiver circuits will all introduce some additional phase rotations, denoted as $\theta_{T}$ , $\theta_{TAG}$ and $\theta_{R}$ respectively. The total phase rotation output by the reader can be expressed as

$$
\left\{ \begin{array}{l} \theta = \left(\frac {2 \pi}{\lambda} \times 2 d + c\right) \bmod 2 \pi \\ c = \theta_ {T} + \theta_ {R} + \theta_ {T A G} \end{array} \right. \tag {1}
$$

where $\lambda$ is the wavelength. The term c is called diversity term, which is related to the hardware characteristics. The phase is a periodic function with period $2\pi$ radians which repeats every $\lambda/2$ in the distance of backscatter communication.

# 2.2 Challenges

(i) The phase estimate is derived from the received signal where the thermal noise from reader receiver is always present, leading to measurement errors. We conduct an empirical studies over 100 tags with environment temperature from $0^{\circ}$ to $40^{\circ}\mathrm{C}$ , various frequencies $(920\sim 926\mathrm{MHz})$ including 16 channels, and RSS from -70 to -30dbm (different orientations). One set of the results measured at the $5^{th}$ channel is depicted in Fig. 1(a). These experiments suggest that trehe phase measurement results contain random errors, following a typical Gaussian distribution with a standard deviation of 0.1 radians. In the following sections, we will consider the phase measurement as a Gaussian random variable instead of an accurate value. (ii) To validate the existence of tag's diversity on RF phase. We place 70 tags at a same position in turn. Each tag is interrogated for 100 times and the average value is reported in Fig. 1(b). We observe that the measured phase values are distributed among $0.3007\sim 5.8438$ radians. Such an observation suggests that the tag's diversity takes impact on phase measurement and cannot be ignored in practice. We also perform the Kolmogorov-Smirnov test (KS-test) to study their predictability. These values pass the test to be verified over a uniform distribution with 0.5 significant level, which means that the tag diversity is hard to infer. In summary, both the thermal noise and tag diversity challenge the phase measurement and further affect the tracking accuracy, which were not fully studied previously.

# 2.3 Solution

In this paper, we propose a holistic system, Tagoram, to address the instant tag tracking problem. Tagoram decomposes it into two stages.

\- Controllable Case: First, we consider a simplified case where the tags move along a known track with a constant speed. This case mostly occurs at a conveyor belt or assembly line where the objects are conveyed by a predefined track. Then the trajectory function can be expressed as:

$$
f (t) = f (t _ {0}) + \int_ {t _ {0}} ^ {t} \vec {V} (t) d t \tag {2}
$$

where $\vec{V}(t)$ is the speed function. Note the trajectory function may follow a more complex model but it can be always abstracted as the above equation. The $f(t_{0})$ is termed as the initial position where the tag is interrogated at time $t_{0}$ . As long as the tag's position at time $t_{0}$ is estimated, its location at an arbitrary time t can be inferred using Eqn. 2 in combination with the track function. Thus, the main task in this case is to locate the tag's initial position $f(t_{0})$ . We build an RF hologram with observations from these antennas with different time of scan to derive the $f(t_{0})$ . The RF hologram is a likelihood exhibition using an image to display the likelihood that how a partitioned grid in tag's motion plane is likely to be the initial position. We start our technique by presenting a naive straightforward hologram solution (Naive Hologram, AH) and then present techniques that can address the negative impacts of thermal noise (Augmented Hologram, AH) and device diversity (Differential Augmented Hologram, DAH). The detailed information can be referred to our recent work [1].

![](images/b674668151d12fe6ec0b4fae13c17c9d90eefd9cf27489bd439b1d0c2706a270.jpg)



(a) Phase distribution

![](images/839d25afc7026ff9588200bcb36178e8d4aa53774c9bd7df7c242cc9f38bceb1.jpg)



(b) Tag diversity   
Figure 1: Empirical studies on measured RF phase. (a) The phase obeys a Gaussian distribution. (b) The diversity takes an impact on measured phase.

To illustrate RF hologram, an experimental study using a linear track. The naive hologram and its corresponding 3D-mesh structure are shown in Fig. 2(a). Here light colors denote lower amplitude values. From the figure, we can see that at the positions close to the target location $f(t_0)$ , the sum grows as the signals constructively add up to each other. On the other hand, at the positions away from to the $f(t_0)$ the signals superimpose at random phase angles and the sum is significantly lower. However, naive hologram cannot give distinctive result about the initial position. There exists a large continuous region with relatively high values. Fig. 2(b) depicts the augmented hologram using the same observed data as those in Fig. 2(a). We see that AH breaks up the large continuous region that has higher values. into several points and reinforces the initial position. Fig. 2(c) shows that the correct initial position has an extremely intensive value that approximately exceeds $2\times$ than those in other pixels. The error can be reduced to within $10mm$ .

\- Uncontrollable Case: We then consider a general case where no prior knowledge about the tag's moving track is known by our system. Thanks to the highly efficient anti-collision capability, the tag can be observed at a high frequency. We approximate its irregular and unpredictable trajectory at run time by exploiting the differentials between consecutive phase values. Then we use the DAH to identify a set of potential trajectories and converting the problem of selecting the optimal trajectory into a task in first stage. Tagarom deals with the unpredictable movement with the following two steps. First, Tagoram acquires the phase measured by M antennas from different directions to recover tag's trajectory every round of antenna scheduled. Second, Tagoram utilizes the DAH to evaluate all fitted trajectories and selects the optimal one corresponding to the pixel with maximum value.

![](images/07d8c18d66cb4a25a3772d23cf426d05333b34cc6565772d00622599084325bd.jpg)



![](images/bfd75971e0f42b7938eb38e46f63cc0a575eac9af5371756aabf73a364c1ba24.jpg)



![](images/cc7dff2b8188b5bd0d022b31db02ca090ae717672f6c9598a8c62c04261e1bc6.jpg)



![](images/3cc666bd12a007a2a57e8ebf9843b7a0c13928547216750d84044b23a47ecf46.jpg)



(a) Naive Hologram

![](images/2fa804f86125535b22eaee33b11fbecbd839d25316404ed7c2d2637be403f7a0.jpg)



(b) Augmented Hologram

![](images/641576fd54c27cb3c0c27742544d9d0837502a10d9018b3347a4f06cf2aaf332.jpg)



(c) Differential Augmented Hologram

Figure 2: RF Hologram. The RF hologram is an image exhibiting the likelihood that how a partitioned grid is likely to be the initial position. The ground truth is highlighted with plus notation. Three columns show the three kinds of holograms using both 2D image and 3D mesh.   
![](images/abd47f062643b8aaca3a99574344d122ee3a603987439325674d8064774d3bee.jpg)



(a) Linear Track

![](images/c6876d2f710135d966118625be26166b8e17c07fd2a1f2b7ee5939bd61323678.jpg)



(b) Circular Track   
Figure 3: Experiment setups

# 3. IMPLEMENTATION

We build Tagoram using ImpinJ [2] reader and Alien EPC Gen-2 UHF RFIDs [3].

Hardware: We adopt an ImpinJ Speedway modeled R420 reader without any hardware or firmware modification. The reader supports four directional antennas at most, being compatible with EPC Gen2 standard. The whole RFID system operates in the 920 \~ 926 MHz band with frequency hopping. The size of antenna is $225mm \times 225mm \times 40mm$ . The reader is connected to host through the wireless network (TCP/IP). Four reader antennas with circular polarization are employed to provide $\geq 8dBic$ gain in two directions. Two types of tags from Alien Corp [3], modeled $2 \times 2$ Inlay and Squiggle Inlay, are employed. Both of them are employed in our lab experiment and pilot study.

Software: We adopt LLRP protocol $[4]$ to communicate with the reader. ImpinJ reader extends this protocol for supporting the phase report. We adjust the configuration of reader to immediately report reading whenever tag is detected. The software is implemented using C# and WPF. We run the software at a Lenovo PC, which equips Intel(R) Celeron CPU G530 at 2.4 GHz and 2G memory.

Track: We emulate a mobile object via a toy train on which a tag is attached, moving at a constant speed of 0.176m/s on a track. Because an arbitrate track can be decomposed into pieces of linear and arc-shaped tracks in practice, we mainly focus on two basic tracks, linear track and circular track, as shown in Fig. 3. To capture the ground truth with high-accuracy, we install a camera above the track. When the tag is firstly interrogated, the system immediately trigger the camera to take a snapshot on the train, from which the initial position can be identified.

# 4. FACILITY REQUIREMENTS

For convenience, we are going to employ a circular track when demonstration. Our facility requirements can be listed as follows.

- Equipment requirement: First, one ImpinJ Reader modeled R420 and four antennas are needed, which is used to collect the phase values. Second, a toy train attached a RFID tag and a circular track are employed to automatically generate the movement with known track. Third, a camera is installed on the top for capturing the ground truth. Last, one or two notebook computers will also be used to calculate and display the train's trajectory.   
- Space requirement: We need an exhibition space with an area of $2m \times 2m$ at least. A desk or table will be better. On the desk or table, notebooks and the track will be placed.   
- Power and Internet requirement: The power plugins needed for the notebooks and reader. In the demo, the Wi-Fi connection might be required.

# 5. ACKNOWLEDGMENT

This research is partially supported by NSFC under Grant No. 61190110 and NSFC CERG-61361166009. The research of Xiang-Yang Li is partially supported by NSF CNS-1035894, NSF ECCS-1247944, NSF ECCS-1343306, National Natural Science Foundation of China under Grants No. 61170216, No. 61228202.

# 6. REFERENCES

[1] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu, "Tagoram: Real-time tracking of mobile rfid tags to high precision using cots devices," in Proc. of ACM MobiCom, 2014.   
[2] “Impinj, Inc,” http://www.impinj.com/.   
[3] “Alien,” http://www.alientechnology.com/tags.   
[4] EPCglobal, “Low level reader protocol (llrp),” 2010.