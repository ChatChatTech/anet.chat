# Demo: Clock Calibration Using Fluorescent Lighting

Zhenjiang Li1, Cheng Li1, Wenwei Chen1, Jingyao Dai1, Mo Li1, Xiang-yang Li2, Yunhao Liu3

1Nanyang Technological University, Singapore

2Illinois Institute of Technology, USA

3Tsinghua University, China

{lzjiang, cli6, chen0746, jydai, limo}@ntu.edu.sg, xli@cs.iit.edu, yunhao@greenorbs.com

# ABSTRACT

In this demo, we propose a novel clock calibration approach called FLIGHT, which leverages the fact that the fluorescent light intensity changes with a stable period that equals half of the alternating current’s. By tuning to the light emitted from indoor fluorescent lamps, FLIGHT can intelligently extract the light period information and achieve network wide time calibration by referring to such a common time reference. We address a series of practical challenges and implement FLIGHT in TelosB motes. In this demonstration, we will show that by taking advantage of the stability of the AC frequency, the detected light intensity, even from different lamps, exhibits a consistent and stable period. FLIGHT can achieve tightly synchronized time with low energy consumption. In addition, since FLIGHT is independent to the network message exchange, time synchronization can be retained even when the network is temporarily disconnected. Such characteristics particularly suit various mobility-enabled scenarios.

# Categories and Subject Descriptors

C.2.2 [Computer Communication Networks]: Network Protocols; C.2.4 [Computer Communication Networks]: Distributed Systems

# General Terms

Design, Performance

# Keywords

Clock calibration, Fluorescent lighting, Energy efficiency

# 1. INTRODUCTION

Maintaining a common notion of time is one fundamental service in many distributed networking systems. A variety of applications depend on the availability of tightly synchronized time cross network nodes. Retaining a common time in the network, however, faces substantial challenges. Due to the low-cost design, CMOS crystal oscillators serve as the most privileging signal source to generate on-board clocks. The frequency of an oscillator is not stable and it fluctuates with the surrounding environment. Thus, clocks on different nodes need to be precisely calibrated such that consistent time can be maintained. Due to the inherent uncertainty, no matter how accurately clocks are initially calibrated, they will ultimately tick towards divergency.

Copyright is held by the author/owner(s).

MobiCom’12, August 22–26, 2012, Istanbul, Turkey.

ACM 978-1-4503-1159-5/12/08.

Great efforts have been made in the past decade to address above issues. Proposed solutions mainly rely on heavy intercommunications between nodes to exchange their local time references [1]. The calibration error, however, gets accumulated hop by hop exponentially. Even that, those solutions lead to excessively high communication overhead and significant power drain in the system. Against the problems, an emerging type of solutions have been recently proposed, which make use of certain external signal sources as common time references. Typical examples are using power lines [2], FM radio [3], Wi-Fi [4]. Although such newly emerging solutions can dramatically reduce the communication cost, they also utilize radios for the clock calibration at the expense of higher power consumption. Even if clock calibration can be performed less frequently, the energy consumption of each calibration could remain high. Besides, most of those solutions need specific hardware components to generate or capture periodical signals, which introduce extra cost and design complexity.

In this study, we propose a new clock synchronization approach that allows network nodes to receive a globally available clock reference by tuning to the fluorescent lighting. Our approach is based on the following observations and facts. Alternating Current (AC) is a periodical signal with a frequency of 50 or 60Hz and the frequency has adequate stability of $\dot { 5 } \cdot 1 0 ^ { - 5 }$ measured by the Allan variance. Powered by AC, the fluorescent light intensity thus changes with a stable period that equals half of the alternating current’s Commonly available in most indoor environments like universities, airports, hospitals, and supermarkets, the fluorescent light provides a universal period reference. On the other hand, the light sensor or camera is widely embedded in commodity wireless platforms, e.g., sensor nodes, smart phones and notebooks. This offers a great opportunity for a plenty of indoor applications to maintain common time by referring to the light emitted from fluorescent lamps.

We propose the Fluorescent LIGHTing (FLIGHT) in this demo and the goals of the demo can be summarized as the following four aspects.

• FLIGHT does not require any extra hardware support. By sampling the light sensor or camera with a sufficiently high rate, accurate period information can be detected for clock calibration. Hence, our solution is widely available on most existing commodity platforms.

• Taking advantage of the stability of the AC frequency, the detected light intensity, even from different lamps, exhibits a consistent and stable period, which ensures high synchronization accuracy.

• Compared with prior radio operation based solutions, sampling the light sensor consumes substantially less energy, which provides us a lightweight solution.

![](images/277cf0fafa7d92436a2dc6aaa336e64c45002e36a83f390bd4323ff7b9e53bff.jpg)  
Figure 1: Single-lamp experiment in the laboratory

• Since our approach is independent to the network message exchange, time synchronization can be retained even when the network is temporarily disconnected. When individual devices are moving, they can still obtain desired periodical patterns for clock calibration. Such characteristics particularly suit various mobility-enabled scenarios.

The rest of this demo will be organized as follows. In Section 2, we will introduce the concept of clock calibration, the mechanism of fluorescent lighting, the design challenges, and the system architecture of FLIGHT. The facilities requirements of the demo is presented in Section 3.

# 2. SYSTEM OVERVIEW

# 2.1 Clock calibration

A native clock is the clock driven by a node’s built-in crystal oscillator directly. We denote the native clock as $c _ { n } ( t _ { 0 } + t )$ , referring to the measured time duration from an initial time $t _ { 0 }$ until t by the native clock. Without loss of generality, we assume t0 to be zero; hence the native clock can be written as $c _ { n } ( t )$ for short. The periodical pattern of the fluorescent light intensity can be treated as a global reference clock, which is denoted as $c _ { g } ( t )$ ). In our system, the AC frequency is 50Hz; thus, the frequency of the global reference clock $f _ { g }$ is 100Hz and the time unit of the global reference clock is $1 / ( 1 0 0 \breve { H } z ) = 1 0 m s$ . In addition, each node maintains a logic clock, written as $c _ { l } ( t )$ . The logic clock is used by upper-layer applications and it advances as follows:

$$
c _ {l} (t) = c _ {l} (0) + \int_ {0} ^ {t} r (\tau) d \tau , \tag {1}
$$

where r(τ) is the instant rate of the native clock at time τ. The goal of FLIGHT is to ensure logic clocks consistent among different nodes.

# 2.2 Mechanism of fluorescent lighting

The fluorescent lamp is a gas discharge lamp using electricity to excite mercury vapor. When the lamp is turned on, the electric power heats up the cathode to emit electrons. Emitted photons are absorbed by electrons in the atoms of the interior fluorescent coating of lamp, leading to physical reactions with emission of visible light. After being heated up, the gas conductivity inside the lamp rapidly rises, allowing the alternating current to flow through and continuously emit light. From the principle of fluorescent lighting, the emitted light is expected to exhibit a periodical pattern since its AC power source is a periodical signal. As the period of AC is adequately stable and phase-coherent, we expect that the light generated by fluorescent lamps can be used as a periodic reference for clock calibration.

![](images/f115a99705186c315222ffc55f860022b70fad2bd644a646b14dd2f35f2d7953.jpg)



![](images/59c12aa834d4bf2eb6e3aa41fca3ee7d74a7126aff14a2ec39f7c59a3da5ec62.jpg)



Figure 2: Multi-lamp experiment in the laboratory

We have conducted some preliminary experiments to validate the initial idea of FLIGHT in Figure 1 [5]. As a benchmark, we plot the instant voltage value from two frontend pins of the light sensor using an oscilloscope. We can observe that the reading from oscilloscope is quite stable and exhibits a regular fluctuation with a period of 10ms (depicted in Figure 1(a)). In practice, sensor nodes need to sample the light sensors. After sampling, we see that the sampling results exhibit the same periodical property as depicted in Figure 1(b), which suggests that the obtained light intensity pattern can be used for clock calibration. Figure 1(c) and (d) show summarize the statistics of the detected period lengths from the trace.

# 2.3 Design challenges

There exist plenty of design challenges for FLIGHT.

First, a node needs to extract the light period by sampling and further generates signals with the same period to calibrate clocks. There may exist multiple peaks in each light period as we have shown in Figure 2 [5]. The light intensity can further fluctuate when we consider node mobility (movement, rotation, etc.). We find that simple heuristics may not precisely extract periods. Existing digital processing techniques, however, introduce unacceptable computation burdens. Thus, it is not trivial to design lightweight approach for nodes to extract accurate period information from fluorescent lighting.

Second, in order to precisely calibration the clock, nodes need to select an appropriate calibration window size. By intuition, if the window size is too small, the sampling error and jitter cannot be effectively canceled out. On the other hand, if the window size is too large, the calibration will suffer a long latency to finish, which may disturb the processing of MCU for other tasks. Both scenarios will deteriorate the overall system performance. The interval length between two consecutive calibrations should be appropriate as well. As we configure the clock calibration in a periodical work mode, we need to guarantee that the clock errors should not be significantly accumulated during each calibration interval. Optimizing such calibration settings needs in-depth investigation in mathematics and practices.

![](images/247ddcfbb501d62be61d6c8a0cb0249c60e4e56d83b22799f1719b718ae46469.jpg)



Figure 3: Illustration of the FLIGHT architecture

Third, several practical issues must be addressed in the system implementation, e.g., although nodes can launch the sampling operation with a sufficiently high rate, e.g. 32KHz, the standard sampling module for the light sensor may not be able to respond in time. For instance, by default, the sampling module in TelosB motes needs around 1ms to sample the light sensor once. No matter how fast nodes trigger the module, the effective sampling rate will not become higher as long as the built-in module is adopted directly. Even we can derive a proper sampling window size to guarantee the calibration accuracy, the limited buffer size in most commodity wireless devices prevents to hold sufficient samples during the calibration. As a result, we need to break all such technical barriers to approach a good calibration performance in FLIGHT.

# 2.4 System architecture and implementation

Figure 3 depicts the system architecture. There exist three major components in FLIGHT: clock calibration, logic time interface, and interval adaptation. Based on the readings from the light sensor, the period generation module in the calibration component is launched to produce the global reference clock for later calibration. The output of the period generation module acts as the input of the logic time maintenance module, which is responsible for updating the frequency ratio and correcting the accumulated drift between two calibrations. The newly obtained logic time can be used by upper layer applications. Meanwhile, the output from the logic time maintenance module can be adopted to determine the interval length for the next calibration.

We implement FLIGHT in TinyOS 2.1x on the TelosB platform. The kernel of FLIGHT includes 600 lines of NesC code that was complied to 2242 bytes of RAM and 16114 byes of ROM. As a result, FLIGHT only occupies 23% of the total buffer and the remaining space is available for other applications. We use the builtin light sensor on the TelosB mote in our experiments. The light sensor utilizes an ADC module to measure the light intensity and records it as a corresponding voltage value in the register. The standard TinyOS packages the ADC module and relies on the MSP430 Timer to control the ADC sampling. The maximum sampling rate of the MSP430 Timer is around 1KHz, which is not fast enough for FLIGHT. To overcome this issue, we write a driver to directly access the register of the ADC module. By so doing, the effective sampling rate can break the 1KHz barrier and achieves up to 83KHz in FLIGHT.

# 3. FACILITY REQUIREMENTS

Our facility requirements can be listed as follows.

Equipment requirement: Several TelosB sensor motes are needed, which will be synchronized by FLIGHT in the exhibition. In addition, one or two notebook computers will also be used to collect the information sent back from sensor motes and display the results through the GUI interface.   
• Space requirement: There is no special requirements for the exhibition space. A normal desk or table will work. On the desk or table, notebooks and sensor motes will be placed.   
• Power and Internet requirement: The power plug is needed for the notebooks. Sensor motes will be powered by the battery. In the demo, the Wi-Fi connection might be required.

# 4. OTHER INFORMATION

We acknowledge the support from NTU Nanyang Assistant Professorship (NAP) grant M4080738.020 and Microsoft research grant FY12-RES-THEME-001. The research of Xiang-Yang Li is partially supported by NSF CNS-0832120 and NSF CNS-1035894. The research of Yunhao Liu is supported by the NSFC Distinguished Young Scholars Program under grant No. 61125202 and NSFC Major Program 61190110. This demo is related to our recent work [5].

# 5. REFERENCES

[1] M. Maroti, B. Kusy, G. Simon, and A. Ledeczi, “The flooding time synchronization protocol,” in Proc. of ACM Sensys, 2004.   
[2] A. Rowe, V. Gupta, and R. Rajkumar, “Low-power clock synchronization using electromagnetic energy radiating from ac power lines,” in In Proc. of ACM Sensys, 2009.   
[3] L. Li, G. Xing, L. Sun, W. Huangfu, R. Zhou, and H. Zhu, “Exploiting fm radio data system for adaptive clock calibration in sensor networks,” in In Proc. of ACM Mobisys, 2011.   
[4] T. Hao, R. Zhou, G. Xing, and M. Mutka, “Wizsync: Exploiting wi-fi infrastructure for clock synchronization in wireless sensor networks,” in In Proc. of IEEE RTSS, 2011.   
[5] Z. Li, W. Chen, C. Li, M. Li, X. Li, and Y. Liu, “Flight: Clock calibration using fluorescent lighting,” in Proc. of ACM Mobicom, 2012.