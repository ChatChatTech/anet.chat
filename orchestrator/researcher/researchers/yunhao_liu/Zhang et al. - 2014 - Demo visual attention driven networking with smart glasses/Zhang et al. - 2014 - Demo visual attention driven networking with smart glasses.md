# Demo: Visual Attention Driven Networking with Smart Glasses

Lan Zhang1, Xiang-Yang Li1,2, Wenchao Huang3, Kebin Liu1, Shuwei Zong4, Xuesi Jian2, Puchun Feng1, Taeho Jung2, Yunhao Liu1

1School of Software and TNLIST, Tsinghua University, China

2Department of Computer Science, Illinois Institute of Technology, USA

3Department of Computer Science, University of Science and Technology of China

4Department of Computer Science, Suzhou Institute for Advanced Study, China lan@greenorbs.com, xli@cs.iit.edu, yunhao@greenorbs.com

# ABSTRACT

In this demo, we propose a proof-of-concept networking system for smart glasses, through which users can express their interest and connect to a target simply by a gaze. Our system iGaze is a visual attention driven networking suite: an iGaze glass (hardware) and a networking protocol VAN (software). Our glass is a low-cost headmounted glass with a camera, orientation sensors, microphone and speakers, which are embedded with our software for visual attention capture and networking. A visual attention driven networking protocol (VAN) is carefully designed and implemented. In VAN, we design an energy efficient and highly accurate visual attention determination scheme using single camera to capture user’s communication interest and a double-matching scheme based on visual direction detection and Doppler effect of acoustic signal to lock the target devices. iGaze has separated and modularized hardware and software design. It can run on top of existing networking protocols, e.g., Wi-Fi.

# Categories and Subject Descriptors

C.3 [Special-purpose and application-based systems]: Real-time and embedded systems

# General Terms

Design, Experimentation, Performance

# Keywords

Smart Glasses; Attention Driven Networking; Device Paring; Gaze Tracking

# 1. INTRODUCTION

Emerging wearable computing devices attract extensive attention worldwide. Smart glasses, e.g., Google Glass and Vuzix Smart Glasses, are computerized eyeglasses, which are usually equipped with various sensors, such as cameras, gyroscope, accelerometer

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage, and that copies bear this notice and the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s). Copyright is held by the author/owner(s).

MobiCom’14, September 7-11, 2014, Maui, Hawaii, USA.

ACM 978-1-4503-2783-1/14/09.

http://dx.doi.org/10.1145/2639108.2641739.

and GPS, to enrich their capabilities. Many efforts have been devoted to improve human interfaces on or using smart glasses, e.g. controlling smart glasses using simple voice commands and head gestures, photo and video capture, and navigation. Some smart glasses also include features like augmented reality overlays. However smart glasses are still in the early stage and looking for revolutionary applications.

In this demo, we explore a novel networking mode with smart glasses that may enable a whole new set of applications. That is, smart glasses users can communicate with surrounding physical and cyber world by their visual attention. People can directly send messages to others without exchanging contact information explicitly or retrieve rich information about an object in the field of view freely using their eye gazes. Eye gaze based networking will bring much convenience to people in a conference and visitors in a museum; also bring many new features to the real-scene game and interactive game design. Moreover, the advertisements can also be significantly enhanced with such visual attention based augmented reality.

These requirements can hardly be fulfilled by existing network solutions. Some interest based systems provide customized information services using the user’s profile and mining results of his/her historical behaviors, e.g., [1]. A few gesture-based device pairing approaches [2,3] attempt to pair devices in proximity. However, those efforts are targeting handhold smart devices, e.g., smart phones. Their requirements for phone displacement (≥ 20cm) [2] and movement speed $( 2 \sim 6 m / s )$ [3] are hard to achieve using head-mounted glasses. Besides, certain augmented reality could also be enabled with a world camera in a visual fashion, e.g., using QR codes or object recognition techniques. But, to utilize the QR code, there are restrictions for scanning distances (≤ 3m) and angles (≥ 30◦) to the target. Object recognition usually requires extensive training and computing, and is vulnerable to environment noise. It cannot distinguish two objects with the same appearance or determine the user’s interested target when there are multiple objects in the field of view.

To achieve this future vision, we propose a new smart glasses system by which a user can connect to a target simply by a gaze. The goals and contributions of this demo can be summarized as follows:

• Our approach is designed to capture a user’s visual attention and then the visual target with high accuracy using only one lowresolution eye camera (i.e., camera capturing images of the user’s eye). We introduce a simplified geometry model to reduce the computation complexity. For better user experience, our solution puts no restriction on the user’s movement, and minimums the set up (e.g., calibration) difficulty. Besides, we use gyroscope to reduce power consumption of continuous image capturing and processing. To support these, we develop a low-cost glasses hardware, with an eye camera, orientation sensors, a microphone and speakers, which are embedded with our software for visual attention capture.

![](images/838077081e3be09f2a04b8b78cea5e7cdfc35d65c8f5986681f08c068acab2cc.jpg)



Figure 1: Gaze vectors and device vectors of a visual attention based networking system.

• Our system establishes a network connection by matching a user’s visual target with the target’s device. At a high level, we address this problem based on the observation that the user’s sightline direction is consistent with the direction between smart glasses worn by them. Technically, we capture the direction of a user’s sightline with the onboard sensors and camera. We also propose a Phase Locked Loop (PLL) based method to estimate the direction from user’s smart glasses to the target smart glasses by tracking the subtle relative displacement of two head-mounted speakers during arbitrary head movements.

• Our system works robustly across individuals and achieves high accuracy for users’ attentions capturing, gaze direction and device direction estimation.

# 2. SYSTEM OVERVIEW

# 2.1 iGaze Design Space

iGaze is designed to enable a new communication mode for smart glasses users. We focus on making the networking devices smarter that can understand the user’s attention and automatically connect to the target of interest. Our demo assumes that the initiator is equipped with our glasses to capture her visual attention at realtime and all participating devices possess computing, networking functionalities and some common sensors, e.g., gyroscope and microphone. iGaze has separated and modularized hardware and software design. It can run on top of existing networking protocols, $e . g .$ , Wi-Fi. It applies to scenarios where networking participators do not need to exchange contact information such as IP, email, web account before connecting to each other.

As shown in Fig. 1, each user in the vision plane is associated with a co-located smart device in the device plane. The challenge is how to match the target on device plane according to user’s visual attention? Two types of scenarios are considered in this work: social networking and object-oriented augmented reality. In the first one (bidirectional application mode), the user wears smart glasses and looks around while the glasses are tracking his/her gaze direction. When two users have an eye contact, a network connection is built between their glasses. This scenario is fitted into many social applications. This type of applications require all participating devices to possess eye cameras. In the second case (unidirectional application mode), the user wearing smart glasses wants to obtain certain information about the visual target object by gazing it. For example, visitors can obtain the description of an artwork when they gaze at it for a certain time period. In these applications, the target objects need to have devices (without cameras) to respond to the ’gaze query’.

![](images/2f845b314cee706f0506549f246e126f2f03b693b0da8b01caf116f7ec88700b.jpg)



Figure 2: Our smart glasses iGaze prototype.

# 2.2 Principal of Gaze Based Networking

What we look for is a bond between the vision plane and device plane, which are dissociated currently. Note that finding the gaze direction and finding the direction of pairing devices are themselves challenging tasks. To address this association issue, we raise our idea based on the following observations. As shown in Fig. 1, when a user A is looking at a visual target B, we define the observer A’s gaze vector as $\nu _ { A } .$ , whose direction is the direction of A’s sightline and magnitude is the distance from A to B. In the device plane, we define the device vector $\mathcal { U } _ { A B }$ as the vector from A’s glasses to B’s glasses. We say two vectors are consistent if the differences between their directions and magnitudes are both less than given thresholds.

Our first observation is that given an observer and his/her gaze vector, among all device vectors started from the observer’s device, only the device vector to the correct visual target’s device is consistent with the gaze vector. As an example in Fig. 1, for the observer $\mathbf { A } ,$ only the device vector $\mathcal { U } _ { A B }$ is consistent with the gaze vector $\nu _ { A }$ . Then our system learns that device B is the correct match to A’s visual target.

Our second observation is that given a pair of users who are looking at each other, their gaze vectors have opposite directions. Taking the scenario in Fig. 1 as an example, both gaze vectors $\gamma _ { B }$ and D have opposite direction to $\nu _ { A }$ . Thus user A can firstly exclude user C by the direction of gaze vectors and only compute vectors $\mathcal { U } _ { A B }$ and $\mathcal { U } _ { A D }$ in the device plane. For bidirectional applications with many users, the first round of sightline direction matching can greatly reduce the overhead in determining pair-wise device vectors.

# 2.3 System Design and Implementation

Based on our observations, our system is designed to consist of software components for visual attention driven networking and the smart glasses hardware.

Software: There are three major building blocks:

• Gaze vector acquisition: This component includes three modules. The real-time eye tracking module captures the movement of a user’s eye using the eye camera at real-time. Attention acquisition component takes the eye movement data as input to detect a visual attention when the gaze lasts for a reasonable time. The threshold is predetermined and can be dynamically adjusted by users. After a visual attention has been captured, the gaze vector determination calculates the corresponding gaze vector to the visual target. The basic idea is that, the iris contour is a circle, but its projection on the camera image plane is elliptical, and the ellipse parameters are determined by the gaze direction. The gaze direction is estimated by determining the pose of the iris circle by back-projecting the ellipse onto a circle in 3D space. The challenge is that with only a single elliptical image, there are many circles satisfying the projection cone. In this demo, we remove ambiguities of back-projecting using a anthropometric model of eyeball, the hardware position and the principal in [4]. Based on our design, the system requires little manual calibration. Moreover, we reduce the cost for continuous image capturing and processing greatly by detecting head fixation using gyroscope before opening the camera module. To avoid unwanted paring when eyes happen to be fixed on a certain object, we ask the users to make a mild head gesture (e.g., head nod) as the postfix of the attention.

<table><tr><td>Component</td><td>Description</td></tr><tr><td>Raspberry Pi II</td><td>700MHz CPU, 512MB RAM, Linux</td></tr><tr><td>Eye Camera</td><td>Maximum Resolution 640x480 @ 30fps</td></tr><tr><td>Gyroscope</td><td>MPU6050, 6-axis, Accuracy - 0.01°</td></tr><tr><td>Magnetic Sensor</td><td>3-axis, Accuracy - 512c/G</td></tr><tr><td>Wi-Fi</td><td>OURLINK, 300Mbps, USB port</td></tr><tr><td>Microphone</td><td>Sample rate 44100Hz</td></tr><tr><td>Stereo Speakers</td><td>Frequency range 180Hz-20KHz</td></tr></table>

Table 1: Specifications of iGaze glass

• Device vector estimation: When the user makes a head gesture, e.g., head nod, two speakers of his/her glasses emit a binaural inaudible acoustic signal with two sine waves at different frequencies (19kHz and 19.5kHz). At receivers, the frequency of each signal is shifted due to the Doppler effects. Candidate devices invoke the phase tracking and device direction determination modules to estimate the device vector as follows. By PLL, a receiver tracks the precise phase of the received signal, where the phase shift is in proportion to relative displacement of two speakers. In this way, the measuring accuracy of the relative displacement is less than 1mm, with a small distance between the two speakers, i.e., 18cm. Then the receiver estimates its relative direction to the initiator by the relative displacement. With our method, different types of head gestures are supported.

• Visual attention driven networking (VAN): It defines the message format and communication process in our visual attention driven networks. VAN constructs a connection from initiator to the visual target’s device based on the matching results of the gaze vector and device vectors.

We implement all software blocks of iGaze using C++. It supports both unidirectional and bidirectional application modes. In the unidirectional mode, the target could also be a device without an eye camera. So we also implement the device direction estimation and VAN for Android system using Java, which enables our glasses to connect an android device in unidirectional applications. The visual attention acquisition components are developed based on the OpenCV library. For the wireless communication of VAN, both AP and Ad Hoc modes are implemented.

Hardware: Fig. 2 illustrates our prototype hardware. To obtain gaze direction, iGaze glass has a fixed eye camera tracking the eye movement. It is 3cm away from the eye. A fixed gyroscope is embedded in the front-head position of the glasses to determine the device coordinate and simplify the coordinate transformation. A magnetic sensor is co-located with the gyroscope, which is only used in the bidirectional mode to exclude unlikely neighbors with gaze direction. For the devices direction, iGaze glass has a central microphone and two separated speakers with a fixed distance (18cm). For the data processing and data transmission, we use Raspberry Pi with a Wi-Fi module. It is a credit-card-sized singleboard computer with Linux operating system. All head-mounted sensors are connected to its hardware data interfaces. It supports a wide range of programming languages, e.g. Python, C++, Java and Perl. The specifications of iGaze glass is presented in Table 1.

# 3. FACILITY REQUIREMENTS

Our facility requirements can be listed as follows:

Equipment requirement: Several iGaze Glasses (more than 3) together with Raspberry Pi platforms are needed in the demo. One WiFi AP is required to build a local area network. Besides, a display is needed to show the results.   
Space requirement: The requirements for exhibition space is 10 square meters or more to simulate a social scenario.   
Power and Internet requirement: The power plug is needed for battery charging. The smart glasses is powered by rechargeable batteries. It would be better if there is Internet connection.

# 4. OTHER INFORMATION

This research is partially supported by NSFC under Grant No. 61125020, NSFC CERG-61361166009. The research of Li is partially supported by NSF CNS-1035894, NSF ECCS-1247944, NSF ECCS-1343306, NSFC under Grants No. 61170216, No. 61228202. This work is related to our recent work [5].

# 5. REFERENCES

[1] LI, Z., WANG, C., JIANG, C., AND LI, X.-Y. Lass: Local-activity and social-similarity based data forwarding in mobile social networks. TPDS (2013).   
[2] PENG, C., SHEN, G., ZHANG, Y., AND LU, S. Point&connect: intention-based device pairing for mobile phone users. In MobiSys (2009), ACM, pp. 137–150.   
[3] SUN, Z., PUROHIT, A., BOSE, R., AND ZHANG, P. Spartacus: spatially-aware interaction for mobile devices through energy-efficient audio sensing. In MobiSys (2013).   
[4] WANG, J., SUNG, E., AND VENKATESWARLU, R. Eye gaze estimation from a single image of one eye. In International Conference on Computer Vision (2003), IEEE, pp. 136–143.   
[5] ZHANG, L., LI, X.-Y., HUANG, W., LIU, K., ZONG, S., JIAN, X., FENG, P., JUNG, T., AND LIU, Y. It starts with igaze: Visual attention driven networking with smart glasses. In Mobicom (2014), ACM.