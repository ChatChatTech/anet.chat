# QuinID: Enabling FDMA-Based Fully Parallel RFID with Frequency-Selective Antenna

Xin Na1, Jia Zhang1, Jiacheng Zhang1, Xiuzhen Guo2, Yang Zou1, Meng Jin3 Yimiao Sun1, Yunhao Liu1, Yuan He1∗

1Tsinghua University, 2Zhejiang University, 3Shanghai Jiao Tong University {nx20,j-zhang19,zhangjc21,zouy23,sym21}@mails.tsinghua.edu.cn, guoxz@zju.edu.cn,jinm@sjtu.edu.cn,{yunhao,heyuan}@tsinghua.edu.cn

# Abstract

Parallelizing passive Radio Frequency Identification (RFID) reading is an arguably crucial, yet unsolved challenge in modern IoT applications. Existing approaches remain limited to time-division operations and fail to read multiple tags simultaneously. In this paper, we introduce QuinID, the first frequency-division multiple access (FDMA) RFID system to achieve fully parallel reading. We innovatively exploit the frequency selectivity of the tag antenna rather than a conventional digital FDMA, bypassing the power and circuitry constraint of RFID tags. Specifically, we delicately design the frequency-selective antenna based on surface acoustic wave (SAW) components to achieve extreme narrow-band response, so that QuinID tags (i.e., QuinTags) operate exclusively within their designated frequency bands. By carefully designing the matching network and canceling various interference, a customized QuinReader communicates simultaneously with multiple QuinTags across distinct bands. QuinID maintains high compatibility with commercial RFID systems and presents a tag cost of less than 10 cents. We implement a 5-band QuinID system and evaluate its performance under various settings. The results demonstrate a fivefold increase in read rate, reaching up to 5000 reads per second.

# CCS Concepts

• Hardware → Wireless devices; • Networks → Sensor networks.

# Keywords

Backscatter; RFID; FDMA; RF computing

∗Yuan He is the corresponding author.

![](images/f828cafe2146bc92e727f9db291c22862c71bdb58fc64995cdd002a1cd4f386d.jpg)

This work is licensed under a Creative Commons Attribution 4.0 International License.

ACM MOBICOM ’25, Hong Kong, China

© 2025 Copyright held by the owner/author(s).

ACM ISBN 979-8-4007-1129-9/2025/11

https://doi.org/10.1145/3680207.3723462

# ACM Reference Format:

Xin Na1, Jia Zhang1, Jiacheng Zhang1, Xiuzhen Guo2, Yang Zou1, Meng Jin3, Yimiao Sun1, Yunhao Liu1, Yuan He1. 2025. QuinID: Enabling FDMA-Based Fully Parallel RFID with Frequency-Selective Antenna. In The 31st Annual International Conference on Mobile Computing and Networking (ACM MOBICOM ’25), November 4– 8, 2025, Hong Kong, China. ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/3680207.3723462

# 1 Introduction

RFID, known for its battery-free operation, presents a compelling solution for a broad range of Internet of Things (IoT) applications [1, 7, 14]. In sectors including logistics [8, 71], supply chain [38, 67], warehouse management [11, 53], and wireless sensing [37, 72, 74], the proliferation of RFID has witnessed an explosive growth in its deployment [6, 39].

In many applications, such as industrial and logistics, realtime and high-throughput ID collection becomes crucial. For example, large-scale logistics centers handle incoming and outgoing items in bulk, often transported by forklifts. Hundreds of tagged items are concentrated within a few meters of the reader and must be scanned simultaneously to ensure seamless inventory tracking. Similarly, on high-speed production lines, such as in electronics assembly, product components arrive in batches and bursts. Within an extremely short time window, usually just a few milliseconds, dozens of tags must be read rapidly to enable real-time status updates.

In order to enhance the efficiency of ID collection, a key research focus has been achieving parallel RFID communication. Traditional RFID employs ALOHA-based protocol, EPC Gen-2, to interrogate tags one by one [16]. To avoid collisions, the EPC standard mandates exchanging a 16-bit random number (RN16) as the handshaking process before reading the tag ID (Fig. 1(a)). In the pursuit of parallelism, recent works [2, 26, 33, 34, 52] adopt the “parallel decoding” approach, involving decoding collided signals from parallel backscatter transmissions. By leveraging subtle signal features, they propose various algorithms to disentangle interleaved signals from distinct tags effectively.

Despite the extensive efforts, no existing approach achieves genuine and practical parallel RFID reading. When applied to

![](images/880f01826ae89dc480eb293b4a1d145ac798fcdff218b85be9b728042ec1a866.jpg)



(a) Conventional RFID

![](images/1e2d3cd50a62a80a9f04c5aeb3bbc7394aa125f041c7378bf640015a3860477d.jpg)



(b) Parallel Decoding

![](images/06d34f0b7a0ee4fb447f3cfd2071dcc7f2bb45ddde8a4b0db95ef6b8b58c6ada.jpg)



w Slot (c) QuinID

Figure 1: QuinID advances from parallel transmission decoding to fully parallel reading in frequency domain.   
![](images/21f2213ce65c5babbb194a9c38e97032b9be7b8722a5d95fdbda1514f12bfc53.jpg)



Figure 2: Successful decoding rate of collided RN16s using a representative algorithm from [34].

RFID systems, parallel decoding algorithms only marginally accelerate the reading by decoding the collided RN16 handshaking signals mandated before transmitting the tag ID, as shown in Fig. 1. This fundamental limitation still confines them to a time-division multiple access (TDMA) operation, resulting in a mere 20% increase in the read rate in our evaluation. Further, in practical applications, these algorithms exhibit unstable performance due to varying collision numbers and fluctuating channel conditions. We implement a representative algorithm from [34] and simulate its ideal successful decoding rate, as shown in Fig. 2. In real-world scenarios, collisions between tags with different signal-tonoise ratio (SNR) levels can further reduce this rate.

We observe that while tags operate across wide frequencies, readers typically only excite them within a narrow band. In this paper, we explore the potential of going beyond conventional TDMA restrictions and achieving FDMA-based fully parallel RFID communication. The reader is expected to establish reliable communication with multiple tags simultaneously across different bands in both the uplink and downlink directions. Bringing this high-level concept into practice, however, faces serval critical challenges.

• Limited energy of the tag. Traditional FDMA operates at the digital baseband, consuming energy far exceeding RFID tag’s constrained power budget (\~1??W). Recent studies [75] suggest introducing various frequency shifts on the tag to generate FDMA backsactter signal. Nonetheless, the power incurred still exceeds the affordable level of RFID tags.   
• High frequency selectivity requirement. UHF RFID operates within the 902-928MHz ISM band. A functional FDMA

![](images/2b47a952a33d227a2f4c15c627b3c2953f24b293f20666fa4d86ae8b395ec998.jpg)



Figure 3: QuinID achieves FDMA-based fully parallel RFID with frequency-selective antenna.

demands interference-free communication across channels. This requires high frequency-selectivity on the tag, especially as parallelism increases. Traditional tags, however, operate across a wide bandwidth and lack such selectivity.

• Compatibility with commercial RFID. RFID systems have been widely deployed across various industries and applications, with billions of tags in circulation. An FDMA solution should ensure compatibility with existing systems in two aspects: 1) FDMA-enabled tags should remain readable by commercial readers, avoiding a complete overhaul of infrastructure, especially at stages where parallel reading is not required. 2) FDMA readers should support the coexistence of FDMA-enabled and traditional tags, ensuring exclusive reading on the former when the latter is also present.

To tackle the above challenges, we present QuinID, the first FDMA-based fully parallel RFID system. Instead of designing a digital FDMA circuit, we explore the frequency selectivity of the tag antenna based on its RF filtering capabilities and battery-free nature. Leveraging the frequencyselective antenna, the QuinID tag (QuinTag) responds solely to excitation signal within its specific frequency band. Quin-Tags are thus distributed across the whole band, each selecting a carrier from the QuinID reader (QuinReader) signal, thereby enabling parallel RFID sessions in the frequency domain, as shown in Fig. 3. The design of QuinID requires addressing issues from both the hardware and software:

• Fully passive ultra-selective filtering antenna. The key to achieving QuinTag’s functionality lies in introducing the frequency-selective antenna while maintaining a batteryfree and cost-effective design. Although conventional antennas possess filtering capabilities, they cannot meet QuinTag’s selectivity requirements. Upon a thorough exploration, we find that surface acoustic wave (SAW) filters are capable of fulfilling QuinTag’s needs (§2.1). To obtain optimal efficiency on the filtering antenna, we carefully fine-tune a decoupled matching network on the SAW’s two ports (§2.2). Our analysis indicates that this antenna has only a slight impact on QuinTag’s reading distance performance (§2.3). QuinTag maintains compatibility with conventional RFID systems, as it is essentially an RFID tag using a commercial RFID chip. Commercial readers are able to read QuinTag due to their frequency-hopping capabilities, which are typically enabled by default per FCC regulations [57].

• Interference-free multi-band reading with mutual independence. In QuinID, parallel reading occurs exclusively when QuinReader interacts with QuinTags. By leveraging digital up/down converters, we accurately merge and separate multi-band RFID signals (§3.1). To guarantee a robust parallel reading, we effectively eliminate two critical sources of interference. First, to avoid interference from mis-excited conventional tags, we ensure independence among Quin-Reader’s reading sessions (§3.2). Second, to eliminate mutual interference within multi-band sessions, we incorporate a crucial pre-distortion stage to compensate for power amplifier nonlinearity (§3.3). Additionally, we delicately design QuinReader’s real-time demodulation algorithm and optimize its performance on FPGA hardware (§3.4).

Implementation. We implement QuinID in its entirety, including the commercial chip-based QuinTag and the FPGAbased integrated QuinReader, demonstrating its readiness for direct productization. We divide the entire bandwidth into five subbands after carefully considering various factors. We open source QuinID designs1, including the first highperformance software-defined radio (SDR) based RFID reader implementation supporting all data rates in the standard.

This paper makes the following contributions:

• We present QuinID, the first to enable FDMA-based fully parallel RFID, running multiple mutually independent sessions in the frequency domain.   
• We design a passive ultra-selective filtering antenna to enable frequency-selective operation on RFID tags, allowing seamless integration into existing systems. A specifically designed reader achieves interference-free parallel reading.   
• QuinID achieves a ??-fold increase in the read rate if dividing the bandwidth into ?? subbands. Our evaluation proves a fivefold improvement, reaching up to 5000 reads per second. It achieves a 5-meter reading distance with a tag manufacturing cost of less than 10 cents.

Paper organization: §2 presents the QuinTag design. §3 covers the QuinReader design. Implementation details are in §4, and evaluation in §5. We review related works in §6 and make discussions in §7. We conclude this work in §8.

# 2 QuinTag Design

This section explains how QuinTag enables FDMA with commercial RFID chips. An RFID tag consists of a fixed IC chip and a customizable antenna. Due to its power constraints, the chip cannot distinguish carrier frequencies and lacks firmware or post-production tunability. Since FDMA cannot be implemented on the chip, we explore the antenna’s filtering capability, designing a highly selective passive filtering antenna that enables the tag to respond to only one carrier.

![](images/75904125ddf234b779b2f88ccea5f22098c1c571320b02ee5853aad3db42573b.jpg)



(a) RFID Tag Operation

![](images/0ad7ec87514bbddfa46851428f8478b100b88bf3f6afc1968236e08b58b64616.jpg)



(b) QuinTag Operation   
Figure 4: Conventional tags have wideband response, while FDMA RFID tags operate in specific bands.

# 2.1 Exploring Filtering Capabilities

FDMA necessitates QuinTag to operate solely within its designated band for both transmission and reception. Unlike conventional tags that operate across the full band, QuinTag should be selectively excited and backscatter signals within a narrow band, as shown in Fig. 4. This requires the antenna to permit the passage of RF signals to and from the IC chip within the operating band while effectively blocking signals outside of this band, thereby requiring filtering capabilities.

Incorporating a filtering process into the antenna gives rise to a filtering antenna [44]. Designing a suitable antenna for QuinTag has to satisfy the following two requirements:

• Selectivity: UHF RFID operates within the 902-928MHz ISM band. Dividing this band into multiple subbands imposes a substantial selectivity requirement.   
• Size and cost: RFID applications demand lightweight and easily manufacturable tags, the same applies to its antenna. Challenges analysis. The frequency selectivity of RF filtering arises from the resonant structure. Typically, the frequency selectivity of a resonant structure is quantified by its quality factor (Q-factor):

$$
Q = \frac {f _ {c}}{\Delta f} = 2 \pi \cdot \frac {\text { energy   stored }}{\text { energy   dissipated   per   cycle }} \tag {1}
$$

where ???? represents the resonance frequency, and Δ?? signifies the passband bandwidth, corresponding to the 3dB attenuation point. A higher ?? implies a sharper frequency response, thereby resulting in a greater degree of parallelism. If five subbands parallelism is required, QuinTag necessitates a selectivity level of less than 5MHz in the 902-928MHz band, resulting in a loaded Q-factor of at least 200.

In antenna design, LC resonators or transmission line resonators are common choices. However, parasitics in LC components and heat losses in metal lines lead to irreducible dissipated energy, limiting their Q-factors to within 100 [41]. For example, a third-order LC filter theoretically could have a passband of 902-908MHz. However, it would require a parasitic resistance of less than $1 0 ^ { - 1 2 }$ Ohms, 1010 times lower than currently achievable ones. Potential high-Q solutions like waveguide resonators or dielectric resonators confine electromagnetic waves within dielectric materials, minimizing metal losses [4]. However, their voluminous cavity structures and complex manufacturing procedures make them unsuitable for RFID applications.

![](images/a0c261c46d1abd319aca8630a01306270cb12117cdf0fb0db488a45c359c7df9.jpg)



(b) Electrical Characteristic

<table><tr><td>SAW Series</td><td>B3934</td><td>B3949</td></tr><tr><td>Freq.</td><td>902.8MHz</td><td>921.4MHz</td></tr><tr><td> $R_1$ </td><td>400Ω</td><td>260Ω</td></tr><tr><td> $C_1$ </td><td>1.1pF</td><td>1.6pF</td></tr><tr><td> $R_2$ </td><td>380Ω</td><td>270Ω</td></tr><tr><td> $C_2$ </td><td>1.2pF</td><td>1.3pF</td></tr><tr><td> $Z_1$ </td><td>(55.3-138.1j)Ω</td><td>(38.2-92.1j)Ω</td></tr><tr><td> $Z_2$ </td><td>(49.4-127.8j)Ω</td><td>(52.6-107.0j)Ω</td></tr></table>

(c) Characteristic Examples   
Figure 5: (a) SAW filter, (b) Equivalent RF circuit model, (c) Numerical model values for two series SAW filters.

SAW filter. In QuinTag, we exploit SAW filters to fulfill the filtering function in its antenna. A SAW filter operates by converting electrical energy into acoustic waves on piezoelectric transducers, as depicted in Fig. 5(a). Only the incidence of the RF signal near the resonant frequency induces oscillation in the transducer, resulting in an exceptionally high Q-factor of up to 1000. It establishes bidirectional filtering to support both downlink and uplink requirements. Moreover, SAW filters offer the advantage of compact size (at the IC scale) and low cost due to their straightforward manufacturing process. Generally, SAW devices costs as little as a few cents, making them a popular choice for RFID applications [62].

# 2.2 Designing SAW-based Antenna

An RFID antenna needs to match its impedance with the IC chip in order to maximize the energy transmission. Specifically, the antenna impedance within the operating frequency range should be equal to the conjugate of the chip impedance. For the SAW-based frequency-selective antenna, precise matching is crucial for proper operation.

Inconsistent impedance of the SAW filter. As previously mentioned, the SAW device achieves filtering through internal transducers. Each transducer consists of two interleaved metal electrodes, presenting a parallel RC characteristic in the circuit’s perspective, as shown in Fig. 5(b). These two transducers remain physically unconnected, thereby generating independent capacitive impedances at the two ports

![](images/bf833dbb7dda09b26f028c7d46330516b77c41208d6ad251c4b574df40d414e3.jpg)



(a) Uniform Matching at Standard 50Ω   
![](images/7fe753fae5c64983ea442f6b370a4a224c2e038f6c9d065e2e1b906bd4123c67.jpg)



(b) Decoupled Matching

Figure 6: We use decoupled matching to optimize the filtering antenna’s performance and reduce cost.   
![](images/3f21cbc636e8aeb741f68f21f252194d0f7bd7ce890bd9c8196c211c9a640204.jpg)



$$
Z _ {A} = f (W _ {l}, S _ {1}, S _ {2}, H _ {m}, W _ {m}, H) = Z _ {1} ^ {*}
$$

Figure 7: We fine-tune the meandered line’s impedance to precisely match the SAW’s port one.

(??1 and ??2). Further, for SAWs working in different frequencies, the inherent differences in the transducers also yield distinct impedances. We illustrate numerical values for two SAW series in Fig. 5(c).

Considering this impedance inconsistency, a common approach to designing the SAW-based antenna would be uniformly matching both ends to a standard impedance of 50 ohms. Then, a regular antenna is attached on one end, while another matching circuit is introduced to connect with the RFID chip on the other end, as depicted in Fig. 6(a). However, this conventional matching technique fails to deliver optimal performance. It necessitates using up to six matching elements for the whole tag, resulting in significant losses attributable to parasitic effects in LC components. Moreover, these additional elements substantially inflate the tag’s manufacturing cost in large-scale production.

Decoupled impedance matching network. In QuinTag, we achieve optimal SAW-based antenna performance by directly matching the complex impedances. Analyzing the matching path from the RFID chip to the SAW on the Smith chart in Fig. 6(a), we observe redundant curves. Note that the SAW’s impedance point represents the conjugate of its complex impedance. This presents an opportunity to simplify the design by reducing matching elements. Instead of treating both ends as 50 ohms, we decouple them and directly match their complex impedances. We first consolidate the $C _ { 1 } , C _ { 2 } ,$ , and $L _ { 2 }$ elements into a single parallel inductor $L _ { 2 } ,$ as demonstrated in Fig. 6(b), facilitating matching between the RFID chip and the SAW. Then, the regular 50-ohm antenna element on the other end is substituted with a meandered line dipole design shown in Fig. 7. It offers a 2dBi gain and maintains a similar size to typical RFID tag antennas. Through careful adjustment of its physical parameters, the impedance of this element can be finely tuned to precisely match the SAW’s impedance. In this way, QuinTag achieves optimal matching performance using just two inductors.

![](images/815007dd856c001a84d79bb9b1246b54e281032e80084c8ceb2eaebebcb234e2.jpg)



Figure 8: Downlink loss comparison and QuinTag’s band division.

![](images/a8639cda2b056b6c3d70d166fc96896566b9c8220b87337f8343a8a267e3daa6.jpg)



Figure 9: RFID tag uplink amplitude in two states (wideband backscatter).

![](images/bbf97728906f46a2f71378786d2c06e76be08dfe20c18450f12b90c017d65e77.jpg)



Figure 10: QuinTag uplink amplitude (narrowband backscatter).

![](images/a2713f7de10299f63112b5c338995492d24c42335117d9375ae6a620341bc93e.jpg)



(a) Wideband Noise Mixing in the Conventional Tag

![](images/4b44a609fe319a294fa55883db781d010c2977a0ed4018e3d463749e08dbd59d.jpg)



(b) Improved Downlink Demodulation in QuinTag   
Figure 11: QuinTag filters noise to partially offset SAW insertion loss and compensate for range reduction.

Quick demonstration. For a quick proof of the above design methodology, we build and simulate QuinTag’s frequencyselective antenna using RF simulation and full wave analysis software. A commercial Qualcomm SAW filter B3300 [56] is used. We optimize the inductor-based matching and finetune the dipole so that the antenna works at 916.5MHz with a passband bandwidth of about 1.6MHz. Fig. 8 compares the excitation and downlink response between this QuinTag and commercial RFID tags. For uplink communication involving backscatter modulation, where the tag utilizes absorbing and reflecting states for on-off keying (OOK) modulation, we present the reflective frequency response of the two states for both RFID tags (shown in Fig. 9) and QuinTag (shown in Fig. 10), respectively. It can be concluded that QuinTag achieves frequency-selective operation in both uplink and downlink communication by utilizing the SAW-based antenna.

Impact of material attachment. RFID tags are often deployed on various materials like glass, wood, or acrylic, which may affect antenna impedance. However, like standard tags, QuinTag is minimally impacted by such attachment. Its frequency selectivity remains unaffected, as key components (SAW filter, matching network, and IC) are encapsulated and shielded from external influences. While slight frequency shifts may occur in the dipole antenna’s response [61], its wide bandwidth (\~100MHz) still covers the 902-928MHz range. Thus, the tag’s placement does not significantly affect its frequency selectivity or assigned sub-band.

Number of subband divisions. Dividing the RFID band into ?? FDMA subbands enables a ??-fold increase in reading capacity but requires interference-free operation across bands. Although SAW filters exhibit sharp frequency responses, they are not ideal rectangles; instead, the response gradually decreases as the frequency deviates from the resonant point, forming a roll-off section. To address this, we segment the 902-928MHz band into working and roll-off bands, as depicted in Fig. 8. QuinReader should avoid reading tags in roll-off bands to prevent interference. Considering this constraint alongside the SAW filter’s passband bandwidth and the need to maintain appropriate energy in each band, we split the ISM band into five (i.e., ??=5) distinct FDMA subbands. Each subband is associated with a specific type of frequency-selective antenna, which is optimized and tuned using the methodology outlined above. It is also achievable to use a larger number of subband divisions, but it results in less energy and narrower data bandwidth distributed across each subband. Ultimately, this trade-off should be made according to specific application needs.

# 2.3 Compensating for Range Reduction

While the SAW filter introduces superb frequency selectivity, it inevitably brings insertion losses of about 3dB, visible in Fig. 8 and may harm QuinTag’s reading range. Fortunately, its filtering property compensate for this reduction.

RFID systems range is determined mostly by the downlink communication range [5, 63]. As the distance reaches the threshold, the reader can still power up the tag and receive its backscatter signal. However, the tag can no longer demodulate the downlink command. This is because wideband noise is introduced alongside the signal, creating self-mixed noise on the tag’s envelope detection, as depicted in Fig. 11. A calculation of the minimum detectable power $\left( P _ { m } \right)$ shows a heavy impact from the noise bandwidth [28]:

$$
P _ {m} = 4 S _ {m} B _ {s} K _ {T} + 2 K _ {T} \cdot \sqrt {4 B _ {s} ^ {2} S _ {m} ^ {2} + B _ {n} B _ {s} S _ {m}}, \tag {2}
$$

![](images/f3da546a75cb0dbbd38e97a6d39016e1251083250088a1102885420c07b9cf2b.jpg)



Figure 12: QuinReader uses digital up/down converters to merge and extract signals in various bands.

where the minimum decodable SNR $S _ { m }$ and $K _ { T }$ are constants for a specific design, $B _ { s }$ and $B _ { n }$ denote the downlink signal and noise bandwidths, respectively. Although passive RFID lacks amplification, this calculation still applies. Their passive demodulators simply yield higher $K _ { T }$ and $S _ { m }$ values. Additionally, since the envelope detector compares its output to an averaged envelope [13], the specific threshold voltage does not affect $P _ { m } .$ The same applies to the receiver’s specific impedance values, as long as matching is maintained.

The wideband nature of conventional tags brings a thermal noise spanning up to 100MHz. In contrast, QuinTag significantly filters noise down to approximately 2MHz, improving the downlink detectable power by about 2dB. While it cannot completely eliminate the range reduction, it ensures an acceptable communication range for RFID applications. We evaluate this compensation in §5.6.1.

# 3 QuinReader Design

We now introduce how QuinReader effectively reads Quin-Tags across multiple bands. Using digital up/down converters, it separates and merges multi-band signals. We eliminate interference from conventional tags as well as inter-band sessions. We also outline key components enabling high rate and real-time reading on FPGA platforms.

# 3.1 Supporting Multi-band Transmission

RFID readers excites tags with a single tone and modulate it with pulse-interval encoding (PIE) for command transmission. Tags backscatter at the frequency of a few hundreds kilohertz, forming a narrow band signal around the carrier. In QuinID, multiple such signals appear at different frequencies, each carrying its QuinTag’s backscatter data.

A straightforward approach to reading multi-band tags is to use multiple conventional readers simultaneously, each set to a different band and equipped with corresponding RF filters. However, the cost and complexity of purchasing and deploying multiple readers scale with the number of sub-bands, making this approach impractical. It also limits usability in mobile applications, such as handheld devices. Instead, we adopt an integrated QuinReader design that processes multi-band signals within a single device.

![](images/871c5052e2a3b3b610895ca8f2213ec2d27e11cfb437b5e2c830978d2aaa43b3.jpg)



(a) Synchronous Logic

![](images/564bd659fcc43cda1659439d531d9e12e53ebf7a73b3fe917972b8c6529f9808.jpg)



(b) Asynchronous Logic   
Figure 13: Asynchronous downlink signals effectively avoids exciting conventional tags.

In our integrated QuinReader design, we merge and separate individual RFID signals at each frequency to enable flexible multi-band processing. As shown in Fig. 12, Quin-Reader employs a digital down converter (DDC) to isolate each backscatter signal. This process involves shifting the target band to the center, filtering out other bands, and feeding the resulting signal to the standard reader processing logic. A digital up converter (DUC) merges excitation signals from multiple sessions via upsampling and mixing, achieving the function opposite to DDC. To enable real-time FPGA operation, filtering and upsampling are staged to minimize resource usage and latency without sacrificing performance.

In this way, reader sessions in each band are separated and can run in parallel, reusing standard RFID reader processing. Existing collision decoding algorithms can also be seamlessly integrated to further enhance performance. However, robust multi-band reading in practice requires addressing two critical sources of interference: from conventional tags and between frequency bands.

# 3.2 Avoiding Conventional Tag Interference

In practice, conventional tags inevitably present within the range of QuinReader, although shouldn’t be considered in parallel reading. Once excited, their backscatter signals span all QuinID bands, impacting system efficiency. Therefore, QuinReader needs to avoid exciting these tags.

We find that applying time delays among multi-band downlink signals effectively prevents excitation of conventional tags. Due to their wideband nature, these tags aggregate the downlink power across bands and detect the envelope for demodulation. If QuinReader’s downlink signals are perfectly synchronized, as depicted in Fig. 13(a), they can decode the command and be unintentionally excited. In contrast, the asynchronous transmission of downlink signals results in irregular variations in the aggregated envelope, shown in Fig. 13(b). Due to the stringent requirements on the power variation and timing of the PIE signal, the tags do not recognize this envelope as correct downlink commands. In this way, although the conventional tags may receive power from QuinReader, they remain dormant and do not backscatter.

To maintain the asynchronous delay consistently, we ensure that sessions across bands remain independent of each other. These sessions naturally generate asynchronous downlink signals because of the difference in command durations, tag clock offsets, and the distribution of empty slots. It’s exceedingly rare for these signals to align perfectly and form a precise command structure. Even if alignment occurs momentarily, such as during the initial reading cycle, the varying durations ensure that synchronization is quickly lost.

![](images/2955586922b707df969eb667b446d4528498a27be8b8a43328f9d57c7476244f.jpg)



Figure 14: Non-linearity of the power amplifier distorts the downlink signal, causing inter-band interference.

Nevertheless, over time, there are inevitably a few moments of synchronization as the system operates continuously. In such instances, QuinReader can disregard these incorrectly excited conventional tags by refraining from responding to their RN16s. This capability arises from the fact that conventional tags backscatter across all bands, resulting in multiple occurrences of the same RN16 in various sessions simultaneously. We evaluate the impact of conventional tags on QuinReader thoroughly in §5.4.2.

# 3.3 Canceling Inter-band Interference

QuinID separates parallel RFID signals across different bands without frequency overlapping, theoretically posing no interference. However, in practice, we still find inter-band interference caused by non-ideal RF components.

Before being fed into the antenna, the multi-carrier PIE downlink signal needs to be amplified (e.g. to 27dBm). Ideally, the power amplifier (PA) linearly amplifies the input signal by a factor ??. For an input signal ?? (?? ), the output signal ?? (??) should be $y ( t ) = A \cdot x ( t )$ . However, real-world amplifiers are constructed with nonlinear active components like transistors, resulting in inherent nonlinearity such as gain saturation during operation [70]. As depicted in Fig. 14(a), this leads to a decrease in actual amplification gain as input power increases. Consequently, interference among downlink signals located in various bands is observed.

Fig. 14(b) shows an example. Initially, when both sessions transmit a carrier, the amplified signals remain stable. At this point, the total input power reaches its maximum, causing the amplifier to become saturated. Subsequently, when one session stops transmitting to indicate ’LOW’ in PIE modulation, the input power is halved. However, this reduction in input power does not proportionately decrease the output power. The actual output power will be higher than half of its original. Consequently, we observe an increase in the power transmitted by the other session. This interference closely resembles the tag’s backscatter signal and may confuse the receiver or even collide with the tag signal.

![](images/b30390ed3b4db27848dc0fa572b8c825f8d94500e3f2898beaaa0bae60eebc34.jpg)



Figure 15: QuinID utilizes DPD before multi-carrier downlink transmission to linearize the amplifier.

To mitigate such inter-band interference, one may avoid the saturation region by restricting the transmit power. Alternatively, one may employ a mapping-based approach, which entails fitting the nonlinear curve to a function ?? and computing its inverse function $f ^ { - 1 }$ . Linearity can be restored by adjusting the actual feed power to $f ^ { - 1 } ( x )$ for each desired input power ??. However, both techniques fall short of addressing the interference effectively. This is due to the presence of the memory effect in the PA, whereby the output at a given moment depends not only on the current input but also on previous input values. Consequently, the PA’s nonlinearity depicted in Fig. 14(a) manifests as scattered points rather than a smooth curve.

To fully eliminate inter-band interference, we use Volterra series [48] to characterize the amplifier’s nonlinearity:

$$
y (n) = \sum_ {k = 0} ^ {K - 1} \sum_ {m = 0} ^ {M - 1} a _ {k m} x (n - m) | x (n - m) | ^ {k} \tag {3}
$$

At any moment, the amplifier’s output ??(??) is determined by the present and past inputs $x ( n - m )$ , along with a coefficient matrix $a _ { k m } .$ , which is to be estimated for a specific amplifier.

We introduce digital pre-distortion (DPD) to linearize the power amplifier, as illustrated in Fig. 15. A portion of the amplified signal is split using a directional coupler and fed back to the digital processing section. By analyzing both the pre-amplified and post-amplified digital signals, an estimator evaluates the nonlinear model and calculates $a _ { k m } .$ Subsequently, a DPD unit pre-distorts the original transmission signal, utilizing the inverse function technique similar to that mentioned above, but applied to the IQ signal instead of just the power. This approach ensures that the final transmitted signal achieves linear amplification. We integrate DPD into QuinReader using the ADI ADRV9375 RF board [10] and evaluate its performance in §5.6.4.

# 3.4 FPGA-based Real-time Demodulation

To demonstrate QuinReader’s readiness for productization, we design a real-time RFID demodulation process optimized for FPGA. This FPGA-based design is also essential for supporting all EPC-specified backscatter link frequencies (BLFs) and enabling DPD, both of which are unattainable with common SDRs like USRP. In USRP-based readers, inherent delays in data streaming between the USRP and its host machine (caused by UDP transmission and kernel scheduling) hinder timely ACK command responses as required by the standard, limiting the BLF to as low as 40kHz [66].

![](images/c28d4a5c78f7929832e3ea7ff9c37235c007ddad3aeea0bcd368aec1c4d3e87c.jpg)



Figure 16: QuinID’s implementation and experiment deployment.

![](images/7615a4fb53af4507eedaf845b8105c61aee0f4efdeb0bc72d682fde3f66f1c3b.jpg)



Figure 17: QuinTags’ filtering performance and working bands.

Upon receiving the backscatter signal, we first remove the DC component induced by carrier excitation. Time synchronization is then achieved through matching the packet preamble, which also aids in channel estimation and equalization. To accommodate the RFID chip’s high and fluctuating clock drift, a symbol synchronizer is incorporated to perform clock recovery. Finally, the backscatter bits are extracted.

The latency bottleneck in this process mainly lies in channel equalization and clock recovery. Equalization requires complex operations like division and square root, which are costly on FPGA platforms. We optimize the computation time by pre-storing results in lookup tables, replacing inplace computation with fast lookups. For clock recovery, we use a phased lock loop (PLL)-based design with a simple yet efficient Gardner timing error detector for fast and accurate drift estimation [47]. We evaluate this latency in §5.3.

# 4 Implementation

# 4.1 QuinTag

Five distinct types of QuinTags corresponding to five bands are individually designed and manufactured on two-layer printed circuit boards (PCBs), each measuring 100mm by 20mm, as Illustrated in Fig. 16. They are implemented batteryfree, eliminating any need for external energy sources. Each type of QuinTag’s implementation contains four parts:

• RFID IC. To ensure compatibility with commercial RFID, we use the NXP UCODE 7 chip [51]. We opt for the packaged version rather than the bare-die for mounting on the PCB.   
• SAW filter. We use five Qualcomm SAW filters (B3934, B3943, B3300, B3949, and B3944 series) [56], with each Quin-Tag incorporating one to determine its FDMA band. The excitation (or downlink) losses for each type are shown in

Fig. 17. In each band, QuinTag suppresses cross-band interference by 30dB. Note that each FDMA band spans 2-3 RFID channels, allowing commercial readers to read QuinTags within these channels.

• Fine-tuned antenna. We design the 2dBi meandered line dipole antenna for each QuinTag type using CST Studio Suite. Their impedances are optimized to match the corresponding SAW’s complex impedance. The antenna can also be implemented in a flexible manner for general applicability.   
• RFID IC and SAW matching. We use PathWave ADS to simulate the inductor-based matching. Inductors are from muRata, and the specific values are optimized with ADS.

# 4.2 QuinReader

We implement QuinReader on an FPGA-based SDR platform, featuring a Xilinx ZC706 motherboard [69] and an ADRV9375 RF daughter board [10], as shown in the right side of Fig. 16. In addition to the streaming delays discussed in §3.4, processing delays introduced by tools like GNURadio for USRPs further increase latency to 400-700??s [12], limiting their BLF to 40kHz, as shown in Table 1.

QuinReader includes five independent RFID reading sessions, each performing the full EPC querying process. It equally distributes power across these bands. We implement all processing algorithms on the FPGA using Mathworks Simulink HDL Coder for minimal latency and real-time operation. A host computer connects to the FPGA board via Ethernet to interface with QuinReader and monitor the received IQ signal and the EPC ID.

The transmit signal from the ADRV9375 chip gets amplified to 27dBm and goes through a directional coupler. This coupler feeds a small portion of the amplified signal back to the RF board for the digital pre-distorter to cancel the inter-band interference. The signal is then transmitted to a 9dBi Laird RFID antenna, forming a 36dBm EIRP as required by FCC [15]. The receiving antenna is another Laird RFID antenna connected directly to the RF board. Currently, Quin-Reader cancels RFID self-interference digitally within FPGA processing rather than using analog circuits.

![](images/1b025da3a1129db88999089d5aacfc28bb14bc3bc01037bfd2dac190168191e3.jpg)



Figure 18: Throughput comparison with different number of tags.

![](images/242e878633ab0766c5304c835af980e3d8d9ad16b22f59ba4e21d7a28e87a733.jpg)



Figure 19: Read rate comparison with different number of tags.

![](images/9384cf76f0f6f019fb8e052550c829bad9dbf4fbb444de3736e8a73ab18874d5.jpg)



Figure 20: Read rate and ERR in different distances (5 tags present).

# 4.3 Compatibility with Commercial RFID

QuinID remains compatible with commercial RFID systems, avoiding a complete infrastructure overhaul. QuinReader is deployed only when parallel reading of QuinTags is needed at specific stages of an item’s lifecycle. In other scenarios, commercial readers can seamlessly read QuinTags due to their frequency hopping capabilities.

# 5 Evaluation

We first describe the methodology (§5.1) and overall performance (§5.2), then compare demodulation latency (§5.3) and evaluate the impact of practical factors (§5.4). Cross-band reading results follow in §5.5, with ablation studies in §5.6.

# 5.1 Methodology

A key design goal of QuinID is compatibility with commercial RFID. Therefore, we consider parallel decoding RFID the state-of-the-art and compare the performance with a representative scheme, Fliptracer [34]. Fliptracer accelerates reading by demodulating collided RN16s, reducing MAC layer resource waste. We also include a conventional reader as a baseline. The performance metrics include throughput, read rate, and EPC reception ratio. Throughput is calculated based on all uplink packets from the tag, including both the RN16s and the EPC IDs. Since the EPC ID contains a CRC inside the packet, we calculate the read rate by measuring the number of CRC-passed EPC IDs per second. EPC reception ratio (ERR) measures the proportion of CRC-passed EPC packets to the total number of received packets.

# 5.2 Overall Performance

We first evaluate the overall performance of QuinID with varying numbers of tags and different distances. As shown in Fig. 16, experiments are conducted in a hall, with the readers positioned at one end and tags placed at varying distances. To ensure a fair comparison, we implement both the standard RFID reader and the Fliptracer-based collision decoding reader using the same hardware as QuinReader. Both readers operate with commercial Alien ALN-9640 tags. Fliptracer’s sampling rate varies with the tag data rate to maintain a fixed 10 samples per symbol for effective parallel decoding. For QuinID, we use QuinReader to read QuinTags. All readers transmit at 36dBm EIRP according to the FCC’s requirements. We set the default tag bit rate as 80kbps with FM0 encoding and default distance as 2m. Since the EPC protocol requires the number of ALOHA time slots in each query round to be set to 2?? , we carefully select ?? to make the slot number close to the tag number, ensuring maximum efficiency. We let the reader operate for 10 seconds and record the packets backscattered by the tags. Unless otherwise posted, the following experiments use the same settings.

Number of tags. Fig. 18 and Fig. 19 compare the aggregated uplink throughput and read rate achieved with different numbers of tags, respectively. We can see that although Fliptracer increases the throughput by a maximum of 2× by decoding many collided RN16s, it only improves the read rate by less than 20% due to the TDMA nature of retrieving the tag ID. QuinID, on the other hand, enables fully parallel reading and significantly outperforms existing schemes, achieving a maximum of 5× read rate improvement. This improvement is because the QuinID implementation operates in five distinct frequency bands. When the tag number reaches 6, the performance no longer improves since multiple tags operate in the same band. Note that the fluctuation of traditional RFID’s performance comes from the varying ?? value. It also slightly impacts FlipTracer’s improvements.

Distance. We compare the read rate in different readertag distances with 5 tags present. As shown in Fig. 20, the read rate of conventional RFID decreases when the distance increases due to degradation of downlink energy. The improvement of Fliptracer also decreases as more decoding errors of collided RN16s occur. In comparison, QuinID provides a stable and reliable 5× rate improvement in 5 meters. The rate decreases significantly afterward mainly because the energy is spread into five bands.

To further investigate the bottleneck of this reading range, we show the EPC reception ratio in different distances in Fig. 20. We can see that as the distance increases, more uplink CRC errors appear. It suggests that the bottleneck of QuinID’s communication range is the uplink, i.e., the reader can still wake up the tag and transmit downlink information, but the low backscatter signal SNR limits the communication distance. Therefore, one way to improve the reading range is to enhance receiver sensitivity using analog carrier cancellation circuits, as seen in modern RFID readers [40, 58]. Results from §5.6.1 and §5.6.3 demonstrate the range improvement these circuits can provide. Commercial readers with analog cancellation achieve a 6-meter reading range for QuinTags at 30dBm EIRP, while QuinReader requires 33dBm EIRP to achieve the same range, considering power distribution.

![](images/7c739416a981ab6cd8fa19c0b30a74f70be94bf6eda9ac51f1eeae56a33ff989.jpg)



Figure 21: Read rate under different tag bit rates (25 tags present).

![](images/0ef17f9c8cdbd6109bda3e79cbb9fc6109d1157655ce06de27c4f69632484158.jpg)



Figure 22: Experiment setup of conventional tags’ impact.

![](images/3b0f860913b820cbbcc7d0620e411a462ea2060641751b4984f5ef56bc7d27b2.jpg)



Figure 23: Conventional tags’ impact on QuinID.

<table><tr><td>Tag rate (bps)</td><td>40k</td><td>80k</td><td>160k</td><td>320k</td><td>640k</td></tr><tr><td>Maximum allowed</td><td>500μs</td><td>250μs</td><td>125μs</td><td>62.5μs</td><td>31.25μs</td></tr><tr><td rowspan="2">FlipTracer</td><td colspan="2">50.6μs (2 tags)</td><td colspan="3">97.2μs (3 tags)</td></tr><tr><td colspan="2">189.0μs (4 tags)</td><td colspan="3">275.9μs (5 tags)</td></tr><tr><td>QuinID</td><td>64.5μs</td><td>34.8μs</td><td>19.2μs</td><td>12.2μs</td><td>22.8μs</td></tr></table>

Table 1: Comparison of demodulation latency.

Material attachment. In this experiment, QuinTags are placed on cardboard to simulate real-world deployments. We also attach them to acrylic materials (as shown in Fig. 16) in the following experiments. Both setups exhibit no observable performance difference or degradation compared to unattached cases, supporting our conclusion in §2.2.

# 5.3 Demodulation Latency

The EPC protocol imposes strict demodulation latency requirements, mandating completion within 20 tag-bit durations. We compare the average RN16 decoding latency at different tag rates to this limit in Table 1. In this experiment, FlipTracer decodes collided RN16s in the time domain on a desktop with 13th-gen Core i7 and 64GB RAM, while QuinID performs parallel decoding in the frequency domain on the ZC706 FPGA platform.

We can see that FlipTracer’s latency depends on the number of collided tags but remains consistent across data rates. The former is evident, since an increase in the tag number leads to an exponential rise in IQ clusters, significantly increasing decoding complexity. On the other hand, the consistency arises because FlipTracer requires a fixed number of samples per symbol for state transition determination, regardless of the data rate. However, as the data rate increases, the protocol demands progressively shorter decoding latencies, casuing FlipTracer to miss protocol deadlines and fail to send ACK commands. In contrast, QuinReader’s demodulation runs in parallel and ensures timely decoding, meeting the protocol requirements across all data rates.

# 5.4 Practical Scenarios

To understand the performance of QuinID in practical scenarios, including using higher bit rates and with the presence of regular RFID tags, we conduct the following experiments.

5.4.1 Tag bit rate. In practical RFID applications, a high bit rate is often required to achieve maximum reading speed. QuinTag achieves frequency-selective operation by leveraging the SAW-based filtering antenna, having a limited bandwidth. The other side of the coin is that this limited bandwidth can affect the bit rate of the tag since a higher bit rate requires wider bandwidth for the tag’s OOK modulation. This experiment investigates QuinID’s supported bit rate.

We deploy 25 conventional RFID tags and 25 QuinTags on an acrylic board, as shown in Fig. 16. We vary the bit rate of all readers from 80kbps to 640kbps (the highest defined by the EPC protocol) and measure the read rate. Since FlipTracer cannot meet the latency requirements, we record the IQ signals from the standard reader for offline decoding and derive its data rate. Fig. 21 shows that QuinID maintains a stable 5× improvement regardless of the tag’s rate. Fliptracer, however, provides less than 20% improvements and suffers from time-consuming decoding, especially at high rates. The result also shows that QuinID can provide a read rate of up to 5000 per second using the highest bit rate. However, it comes with a cost associated with the tolerance of the carrier frequency offset. We evaluate this further in §5.6.2.

5.4.2 Presence of conventional tags. In the practical applications of QuinID, conventional RFID tags’ existence is inevitable. We set four scenarios to evaluate the impact of the conventional tag’s presence on the read rate of QuinID. In all scenarios, we set QuinID to read five QuinTags in five distinct bands. We put two conventional tags within Quin-Reader’s range for the ‘mild’ and ‘medium’ impact cases and four conventional tags for the ‘heavy’ and ‘extreme’ cases. The deployment settings are shown in Fig. 22. To accommodate the potential occurrence of conventional tags, we manually set the Q value to ensure an adequate number of Aloha slots—specifically, 4 and 8 slots per query, respectively.

![](images/f02d6e979f98b2de27f94114b1ca28cca5fca29924e47b988011798d3897099b.jpg)



Figure 24: Cross-band misreading. (up): readable distance across frequencies, (down): details of band 3.

![](images/1ff90313bda1b07c0d13f758ec219acfe59aef0b447ad5d9f821916784a6d525.jpg)



Figure 25: Performance comparison between QuinTags and commercial RFID tags in commercial readers.

![](images/465b43c1c46ec9ca3787ca473cac25bdc70ca676ff3b3a40532bb21ac6cec2f1.jpg)



Figure 26: QuinTag supports all RFID bit rates since the spectrum falls inside its operating bandwidth.

Fig. 23 shows the comparison of the read rate with or without the conventional tag’s impact, as well as the misreads of these conventional tags. In all cases, QuinID is little affected, as discussed in §3.2. Nevertheless, there exist certain misreads. This is because the five independent RFID sessions in the frequency domain may sometimes align and form a receivable downlink command for the conventional tags. When these tags start to backscatter their information, collisions happen with all five bands and decrease the QuinID read rate. Even in the worst case, the read rate drop is less than 3%. Further avoidance can be done by distinguishing these RN16s and ignoring them. In short, QuinID is highly robust to conventional tags’ impact.

# 5.5 Cross-band Misreading

A reliable FDMA requires zero interference or misreading across bands. We now evaluate the cross-band reading of QuinTags. We use an Impinj R2000 handheld RFID reader to read all five types QuinTags across frequencies. Since crossband reading is more likely to occur at close range and low bit rate, we set the reader at 33dBm EIRP power and read the tags within 1 meter using a 40kbps rate.

The upper figure in Fig. 24 shows the read range of different QuinTags across all frequencies, while the lower specifically illustrates the read rate of QuinTag F3 at different frequencies and distances. Misreading outside the operating band occurs only when both the frequency and distance are very close. However, when QuinReader is used for parallel reading, the frequencies of all bands are naturally separated by more than 5MHz. This separation minimizes misreading, even when tags are placed in close proximity. In conclusion, as long as each carrier frequency in QuinReader remains within its designated operating band, tags in that band achieve maximum read rates, while cross-band misreading remains negligible. This also indicates that narrowing the band spacing is feasible within certain limits, allowing for more than five FDMA bands and greater spectrum utilization.

# 5.6 Ablation Study

We conduct ablation studies to further assess QuinID’s performance. §5.6.1 evaluates QuinTag’s performance on conventional readers and its compensation on the range reduction. §5.6.2 examines reader’s carrier frequency offset effects. §5.6.3 explores the trade off between range and read rate. §5.6.4 evaluates the effectiveness of the digital pre-distorter.

5.6.1 QuinTag with RFID reader. This experiment compares QuinTag’s performance to standard RFID tags when using commercial RFID readers. We use an Impinj R2000-based handheld reader, operating at 30dBm EIRP with a consistent 99% modulation depth. QuinTag’s PCB antenna, implemented with copper, has the same gain as the printed aluminum antenna in commercial tags, both featuring 2dBi directivity and 92%-95% efficiency [9]. Fig. 25 compares the read rate at different distances. We can see that QuinTag performs similarly to standard RFID within the 6-meter range. The read rate decreases significantly at 7 meters.

By filtering out noise and improving downlink SNR, the SAW filter can partially offset its insertion loss, compensating for range reduction. We reduce the reader’s power by 3dB while maintaining a 99% modulation depth and read a commercial RFID tag, emulating QuinTag with SAW’s insertion loss. This power reduction proportionally decreases the PIE-modulated signal, which represents the power difference between high and low states. The resulting improvement confirms the analysis in §2.3, showing an acceptable communication range of QuinTag.

5.6.2 Impact of carrier frequency offset. Supporting high bit rates requires QuinTag to provide sufficient bandwidth. Fig. 26 shows the operating bandwidth of a specific QuinTag and the FM0 encoded backscatter signal spectrum. We can see that the operating band covers the whole spectrum for both 320kbps and 640kbps bit rates. However, in practical reader implementations, the carrier frequency may not align perfectly with the center frequency of QuinTag. We evaluate the impact of possible carrier frequency offset. In this experiment, we vary the carrier frequency in a 150kHz step and measure the read rate under 320kbps and 640kbps bit rate. The results are shown in Fig. 27. We can see that when the offset is higher than a certain threshold, the performance decreases significantly. This is because the backscatter spectrum starts to fall outside the operating bandwidth with a high offset and gets filtered out by the SAW. The results show that QuinTag can tolerate about 150kHz offset at 640kbps bit rate and 450kHz offset at 320kbps. This level of carrier accuracy can be satisfied with modern RFID readers [50].

![](images/9466e456c8e7a83d56d74d0339d6a0fba9ca2b997a877c2e55cb41971ff362f7.jpg)



Figure 27: Impact of the carrier frequency offset.

![](images/c4b14df60654de44d1e86f8131cbd423807602d05a18bfa179d2568a92850c11.jpg)



Figure 28: Trade off between parallelism and range.

![](images/b39df00e8f249a21b8b47be8e9bec947ae43659c3653812d6d67c2e1b6c9fe09.jpg)



Figure 29: Effectiveness of the digital pre-distortion in QuinReader.

5.6.3 Trade-off between parallelism and range. Our implementation includes five independent RFID sessions across different bands with equal transmission power distribution. Given a fixed total transmission power, QuinID can trade off between read range and maximum read rate by adjusting the number of parallel sessions. We measure read rates at various distances in different session numbers, as shown in Fig. 28. We find that the stable read distance can be extended to 6 meters when two parallel sessions are running, as the 2-way QuinID increases the power by 4dB compared to the 5-way QuinID. We leave the trade-off choices to users as they can flexibly select the parallelism of QuinID according to their application needs.   
5.6.4 Effectiveness of digital pre-distortion. QuinReader includes a digital pre-distortion stage before amplifying the signal to cancel the inter-band interference. In this experiment, we show the effectiveness of this DPD stage. We switch the DPD on and off in different degree of parallelism configurations and measure the receiving rate of CRC-correct and CRC-error EPC packets. As shown in Fig. 29, regardless of the degree of parallelism configured, inter-band interference exists as long as multi-band carriers are present in the frequency domain. This interference causes failure to detect the preamble of backscatter packets, resulting in fewer EPC

packets received. It also corrupts the backscatter signal, causing bit decoding failure and CRC error in the EPC packets. With DPD enabled in QuinID, the interference is successfully eliminated, and the read rate increases linearly with the increasing parallelism with few CRC errors.

# 6 Related Work

# 6.1 Parallel Backscatter

Backscatter is a promising solution for ubiquitous sensing in IoT applications [46, 65, 73]. Many efforts aim to boost its communication throughput [18, 20, 55], particularly through parallelizing multiple tag transmissions. We categorize existing works into two groups: those collaborating with conventional OOK tags similar to RFID and those designing new tags employing diverse abilities.

Parallel RFID. These works adopt “parallel decoding”, which involves decoding collided signals from parallel transmissions at the reader using time or IQ domain features [2, 25, 26, 42, 52, 64]. At high sampling rates, collided OOK states form multiple clusters, with most works relying on the distinguishable ones for decoding. However, diverse tag channels and the exponential growth of clusters incur a significant superclustering phenomenon. To address this, recent works introduce additional information into the decoding, include temporal burstiness [32, 33], multi-frequency channel information [30], and multiple antennas [27].

While these works allow parallel decoding of backscatter signals, the mandatory handshaking (exchanging an RN16) in the EPC protocol and their unstable performance significantly limit their practical usage. Their overall improvement in the read rate is minimal, amounting to less than 20%. In comparison, QuinID achieves fully parallel RFID reading and demonstrates a stable 5× increase in the read rate.

New parallel backscatter designs. In addition to decoding concurrent signals, in recent years, researchers aim to design new backscatter systems and enhance the capabilities of tags to achieve parallelism [3, 22, 68]. Early approaches directly employ coding mechanisms on tags for collision recovery [36, 54]. These CDMA-based methods introduce prohibitive overhead in large-scale deployments. Subsequent efforts [24, 75] propose using frequency shifting on multiple tags to create OFDMA signals, enabling extensive parallelism of up to 100 tags. Nevertheless, these methods often result in high energy overhead on the tags. Recent works introduce LoRa backscatter systems, capitalizing on chirp signals’ features for parallel transmissions [23, 31]. Despite this, LoRa backscatter systems exhibit low data rates and are more suitable for long-range transmissions.

These new systems indeed offer potential for large-scale ID collection. However, they often demand more energy than an RFID tag can afford, which is typically only 1??W. Further, considering billions of RFID tags already in circulation and the widespread deployment of readers, their lack of compatibility inevitably causes resistance from the industry. In contrast, QuinID supports fully parallel RFID reading. It is specifically designed to work in RFID applications and maintains compatibility with existing RFID infrastructure.

# 6.2 SAW Technology in Battery-free IoT

Due to their battery-free nature and ease of manufacturing, surface acoustic wave devices are extensively valuable for low-power IoT [17]. They transduce physical signals into electrical ones, thus enabling sensing of pressure, temperature, and mass [29, 43]. In [21], the authors employ SAW devices as differential circuits to achieve low-power LoRa signal demodulation. Further, leveraging the unique physics of surface acoustic waves, SAW devices can function as RFID tags [62]. They backscatter hard-coded ID information while achieving significant cost-effectiveness.

Different from these works, QuinID is the first to integrate SAW filters into RFID antennas for frequency-domain parallelism. Although SAW devices have been employed directly as RFID tags, they do not support parallel operation.

# 7 Discussion

# 7.1 Cost Analysis and Application Scope

The cost of a commercial RFID tag includes the IC chip, antenna, and assembly. Using a flip-chip process, the typical cost is 3.4¢, with 1.3¢ for the IC, 1¢ for the antenna, and 1.1¢ for assembly [59]. QuinTag adds a SAW filter, two inductors, and additional assembly. SAW filters, made with a simpler manufacturing process and cheaper piezoelectric materials [45], are comparable in cost to or cheaper than RFID ICs [60]. Inductors, benefiting from a straightforward manufacturing process, cost about 1¢ each. With an estimated fourfold increase in assembly cost, QuinTag is expected to cost under 10¢ in mass production, about 3× that of a commercial tag.

To further optimize costs, the RFID IC die can be integrated with the SAW filter die into a single module, with inductors implemented on the same IC. This significantly reduces assembly costs, with the primary increase concentrated in the module itself. A rough estimate places the module cost at around 3-4¢, making it 1.5-1.8× the cost of standard RFID tags. As for QuinReader, its cost is comparable to that of a standard RFID reader, with replacement costs incurred only at specific stages requiring parallel reading.

Given these cost considerations, QuinID is particularly well-suited for industrial applications such as large logistic centers, high-speed production lines, and valuable goods tracking. Although QuinTag has a relatively higher cost, the efficiency gains from improved performance often outweigh the additional expense. Moreover, the typically higher value of tracked items allows for gerater tolerance of the tag cost.

# 7.2 More Potential Applications

Beyond parallel RFID, QuinID can also enhance and expand other applications. In logistics, assigning tags of the same frequency band to each batch helps isolate batches, naturally preventing misreads during inventory replenishment. Additionally, tagging goods of the same category with the same band enables easy grouping of scattered items [35].

# 7.3 Reconfigurable QuinTag

Currently, QuinTags operate on preassigned frequency bands determined by the SAW filter, which may limit support for wideband techniques such as RFID localization. To enable reconfigurability, multiple SAW filters can be integrated with an RF switch for dynamic band selection. This would also enable channel hopping mechanisms on the tag, further improving reading efficiency. We believe such functionality could be incorporated into future RFID chips while maintaining compatibility with existing RFID systems.

# 8 Conclusion

We present QuinID, an FMDA-based fully parallel RFID system. With a passive ultra-selective filtering antenna tailored for commercial RFID chips, tags in QuinID achieve frequencyselective operation. Multiple independent RFID sessions are operating simultaneously across distinct frequency bands. QuinID significantly increases the read rate of commercial RFID without significantly sacrificing read range and tag cost. From a boarder perspective, QuinID introduces a passive RF computing technique [19, 21, 49] that operates directly on the frequency of RF signals. Our evaluation shows that the five band QuinID implementation achieves a fivefold increase in the read rate, with a maximum of 5000 reads per second.

# Acknowledgments

We sincerely thank our shepherd and reviewers for their valuable feedback. This work is supported in part by the National Natural Science Foundation of China under grant No. 62425207, No. 62472379, and No. 62272293.

# References

[1] Mohamed Ibrahim Ahmed, Atul Bansal, Kuang Yuan, Swarun Kumar, and Peter Steenkiste. 2023. Battery-free Wideband Spectrum Mapping using Commodity RFID Tags. In Proceedings of the 2023 ACM MobiCom.   
[2] Christoph Angerer, Robert Langwieser, and Markus Rupp. 2010. RFID Reader Receivers for Physical Layer Collision Recovery. IEEE Transactions on Communications (2010).   
[3] Kang Min Bae, Hankyeol Moon, Sung-Min Sohn, and Song Min Kim. 2023. Hawkeye: Hectometer-range Subcentimeter Localization for Large-scale mmWave Backscatter. In Proceedings of the 2023 ACM MobiSys.   
[4] Prakash Bhartia and Protap Pramanick. 2016. Modern RF and Microwave Filter Design. Artech.   
[5] Ritochit Chakraborty, Sumit Roy, and Vikram Jandhyala. 2011. Revisiting RFID Link Budgets for Technology Scaling: Range Maximization of RFID Tags. IEEE Transactions on Microwave Theory and Techniques (2011).   
[6] Xingyu Chen, Jia Liu, He Huang, Yu-E Sun, Xu Zhang, and Lijun Chen. 2023. Revisiting Cardinality Estimation in COTS RFID Systems. In Proceedings of the 2023 ACM MobiCom.   
[7] Yunzhong Chen, Jiadi Yu, Yingying Chen, Linghe Kong, Yanmin Zhu, and Yi-Chao Chen. 2024. RFSpy: Eavesdropping on Online Conversations with Out-of-Vocabulary Words by Sensing Metal Coil Vibration of Headsets Leveraging RFID. In Proceedings of the 2024 ACM MobiSys.   
[8] Donghui Dai, Zhenlin An, Zheng Gong, Qingrui Pan, and Lei Yang. 2024. RFID+: Spatially Controllable Identification of UHF RFIDs via Controlled Magnetic Fields. In Proceedings of the 2024 USENIX NSDI.   
[9] D.D. Deavours, K. Demarest, and A. Syed. 2007. Effects of Antenna Material on the Performance of UHF RFID Tags. In Proceedings of the 2007 IEEE International Conference on RFID.   
[10] Analog Devices. 2017. Analog Devices ADRV9375-W/PCBZ Evaluation Kit. https://www.analog.com/en/resources/evaluation-hardware-andsoftware/evaluation-boards-kits/adrv9375.html   
[11] Laura Dodds, Isaac Perper, Aline Eid, and Fadel Adib. 2023. A handheld fine-grained rfid localization system with complex-controlled polarization. In Proceedings of the 2023 ACM MobiCom.   
[12] Matt Ettus. 2019. Managing Latency in Continuous GNU Radio Flowgraphs. https://www.gnuradio.org/grcon/grcon19/presentations/Ma naging\_Latency/Matt%20Ettus%20-%20Managing%20Latency.pdf   
[13] Alessio Facen and Andrea Boni. 2006. A CMOS Analog Frontend for a Passive UHF RFID Tag. In Proceedings of the 2006 International Symposium on Low Power Electronics and Design (ISLPED).   
[14] Chao Feng, Jie Xiong, Liqiong Chang, Fuwei Wang, Ju Wang, and Dingyi Fang. 2021. RF-Identity: Non-Intrusive Person Identification Based on Commodity RFID Devices. Proceedings of the ACM on Interact. Mob. Wearable Ubiquitous Technol. (IMWUT) (2021).   
[15] GS1. 2024. Overview of UHF frequency allocations (860 to 930 MHz) for RAIN RFID. https://www.gs1.org/docs/epc/uhf\_regulations.pdf   
[16] GS1. 2024. Radio-frequency identity protocols class-1 generation-2. https://www.gs1.org/standards/rfid/uhf -air-interface-protocol   
[17] Xiuzhen Guo, Yuan He, Jing Nan, Jiacheng Zhang, Yunhao Liu, and Longfei Shangguan. 2024. A Low-Power Demodulator for LoRa Backscatter Systems With Frequency-Amplitude Transformation. IEEE/ACM Transactions on Networking (2024).   
[18] Xiuzhen Guo, Yuan He, Longfei Shangguan, Yande Chen, Chaojie Gu, Yuanchao Shu, Kyle Jamieson, and Jiming Chen. 2025. Mighty: Towards Long-Range and High-Throughput Backscatter for Drones. IEEE Transactions on Mobile Computing (2025).   
[19] Xiuzhen Guo, Yuan He, Zihao Yu, Jiacheng Zhang, Yunhao Liu, and Longfei Shangguan. 2022. RF-transformer: a unified backscatter radio hardware abstraction. In Proceedings of the 2022 ACM MobiCom.

[20] Xiuzhen Guo, Yuan He, Jiacheng Zhang, Yunhao Liu, and Longfei Shangguan. 2024. Towards Programmable Backscatter Radio Design for Heterogeneous Wireless Networks. IEEE/ACM Transactions on Networking (2024).   
[21] Xiuzhen Guo, Longfei Shangguan, Yuan He, Nan Jing, Jiacheng Zhang, Haotian Jiang, and Yunhao Liu. 2022. Saiyan: Design and Implementation of a Low-power Demodulator for LoRa Backscatter Systems. In Proceedings of the 2022 USENIX NSDI.   
[22] Xiuzhen Guo, Longfei Shangguan, Yuan He, Jia Zhang, Haotian Jiang, Awais Ahmad Siddiqi, and Yunhao Liu. 2020. Aloba: rethinking ON-OFF keying modulation for ambient LoRa backscatter. In Proceedings of the 2020 ACM SenSys.   
[23] Xiuzhen Guo, Longfei Shangguan, Yuan He, Jia Zhang, Haotian Jiang, Awais Ahmad Siddiqi, and Yunhao Liu. 2022. Efficient Ambient LoRa Backscatter With On-Off Keying Modulation. IEEE/ACM Transactions on Networking (2022).   
[24] Mehrdad Hessar, Ali Najafi, and Shyamnath Gollakota. 2019. NetScatter: Enabling Large-Scale Backscatter Networks. In Proceedings of the 2019 USENIX NSDI.   
[25] Pan Hu, Pengyu Zhang, and Deepak Ganesan. 2014. Leveraging interleaved signal edges for concurrent backscatter. In Proceedings of the 2014 ACM HotWireless.   
[26] Pan Hu, Pengyu Zhang, and Deepak Ganesan. 2015. Laissez-Faire: Fully Asymmetric Backscatter Communication. In Proceedings of the 2015 ACM SIGCOMM.   
[27] Qianyi Huang, Guochao Song, Wei Wang, Huixin Dong, Jin Zhang, and Qian Zhang. 2020. FreeScatter: Enabling Concurrent Backscatter Communication Using Antenna Arrays. IEEE Internet of Things Journal (2020).   
[28] Xiongchuan Huang, Guido Dolmans, Harmke de Groot, and John R. Long. 2013. Noise and Sensitivity in RF Envelope Detection Receivers. IEEE Transactions on Circuits and Systems II: Express Briefs (2013).   
[29] Tarikul Islam, Upendra Mittal, AT Nimal, and MU Sharma. 2012. Surface Acoustic Wave (SAW) vapour sensor using 70 MHz SAW oscillator. In Proceedings of the 2012 International Conference on Sensing Technology (ICST).   
[30] Chengkun Jiang, Yuan He, Meng Jin, Xiaolong Zheng, and Junchen Guo. 2018. Canon: Exploiting Channel Diversity for Reliable Parallel Decoding in Backscatter Communication. In Proceedings of the 26th IEEE International Conference on Network Protocols (ICNP).   
[31] Jinyan Jiang, Zhenqiang Xu, Fan Dang, and Jiliang Wang. 2021. Longrange ambient LoRa backscatter with parallel decoding. In Proceedings of the 2021 ACM MobiCom.   
[32] Meng Jin, Yuan He, Chengkun Jiang, and Yunhao Liu. 2020. Fireworks: Channel Estimation of Parallel Backscattered Signals. In Proceedings of the 2020 ACM/IEEE IPSN.   
[33] Meng Jin, Yuan He, Xin Meng, Dingyi Fang, and Xiaojiang Chen. 2018. Parallel Backscatter in the Wild: When Burstiness and Randomness Play with You. In Proceedings of the 2018 ACM MobiCom.   
[34] Meng Jin, Yuan He, Xin Meng, Yilun Zheng, Dingyi Fang, and Xiaojiang Chen. 2017. FlipTracer: Practical Parallel Decoding for Backscatter Communication. In Proceedings of the 2017 ACM MobiCom.   
[35] Meng Jin, Kexin Li, Xiaohua Tian, Xinbing Wang, and Chenghu Zhou. 2023. Fast, Fine-grained, and Robust Grouping of RFIDs. In Proceedings of the 2023 ACM MobiCom.   
[36] Linghe Kong, Liang He, Yu Gu, Min-You Wu, and Tian He. 2014. A Parallel Identification Protocol for RFID systems. In Proceedings of the 2014 IEEE INFOCOM.   
[37] Songfan Li, Qianhe Meng, Yanxu Bai, Chong Zhang, Yihang Song, Shengyu Li, and Li Lu. 2023. Go Beyond RFID: Rethinking the Design of RFID Sensor Tags for Versatile Applications. In Proceedings of the 2023 ACM MobiCom.

[38] Bo Liang, Purui Wang, Renjie Zhao, Heyu Guo, Pengyu Zhang, Junchen Guo, Shunmin Zhu, Hongqiang Harry Liu, Xinyu Zhang, and Chenren Xu. 2023. RF-Chord: Towards Deployable RFID Localization System for Logistic Networks. In Proceedings of the 2023 USENIX NSDI.   
[39] K. Liu, L. Chen, J. Yu, and Z. Jia. 2024. Revisiting RFID Missing Tag Identification: Theoretical Foundation and Algorithm Design. IEEE/ACM Transactions on Networking (2024).   
[40] Shan Liu, Xinan Wang, Jinpeng Shen, Bo Wang, Tao Ye, and Ru Huang. 2014. A novel low-noise high-linearity CMOS transmitter for mobile UHF RFID reader. SCIENCE CHINA Information Sciences (2014).   
[41] Rheinhold Ludwig and Pavel Bretchko. 2007. RF Circuit Design: Theory & Applications (2nd Edition). Prentice-Hall, Inc.   
[42] Yunfei Ma, Nicholas Selby, and Fadel Adib. 2017. Drone Relays for Battery-Free Networks. In Proceedings of the 2017 ACM SIGCOMM.   
[43] Debdyuti Mandal and Sourav Banerjee. 2022. Surface acoustic wave (SAW) sensors: Physics, materials, and applications. Sensors (2022).   
[44] Chunxu Mao, Yao Zhang, Xiuyin Zhang, Pei Xiao, Yi Wang, and Steven Gao. 2021. Filtering Antennas: Design Methods and Recent Developments. IEEE Microwave Magazine (2021).   
[45] Jiyang Mei, Naiqing Zhang, and James Friend. 2020. Fabrication of surface acoustic wave devices on lithium niobate. JoVE (Journal of Visualized Experiments) (2020).   
[46] Qianwen Miao, Fu Xiao, Haiping Huang, Lijuan Sun, and Ruchuan Wang. 2020. Smart attendance system based on frequency distribution algorithm with passive RFID tags. Tsinghua Science and Technology (2020).   
[47] Rice Michael. 2008. Digital Communications: A Discrete-Time Approach. Pearson Education India.   
[48] D.R. Morgan, Z. Ma, J. Kim, M.G. Zierdt, and J. Pastalan. 2006. A Generalized Memory Polynomial Model for Digital Predistortion of RF Power Amplifiers. IEEE Transactions on Signal Processing (2006).   
[49] Xin Na, Xiuzhen Guo, Zihao Yu, Jia Zhang, Yuan He, and Yunhao Liu. 2023. Leggiero: Analog WiFi Backscatter with Payload Transparency. In Proceedings of the 2023 ACM MobiSys.   
[50] NXP. 2018. NXP UHF RAIN RFID Reader IC ST25RU3993. https: //www.st.com/zh/nfc/st25ru3993.html   
[51] NXP. 2019. NXP UCODE 7 EPC Gen2 RFID IC. https://www.nxp.co m/products/rfid-nfc/ucode-rain-rfid-uhf/ucode-7-7m:SL3S1204   
[52] Jiajue Ou, Mo Li, and Yuanqing Zheng. 2015. Come and Be Served: Parallel Decoding for COTS RFID Tags. In Proceedings of the 2015 ACM MobiCom.   
[53] Qingrui Pan, Zhenlin An, Xueyuan Yang, Xiaopeng Zhao, and Lei Yang. 2022. RF-DNA: large-scale physical-layer identifications of RFIDs via dual natural attributes. In Proceedings of the 2022 ACM MobiCom.   
[54] Aaron N. Parks, Angli Liu, Shyamnath Gollakota, and Joshua R. Smith. 2014. Turbocharging ambient backscatter communication. In Proceedings of the 2014 ACM SIGCOMM.   
[55] Qihui Qin, Kai Chen, Yaxiong Xie, Heng Luo, Dingyi Fang, and Xiaojiang Chen. 2024. Pushing the Throughput Limit of OFDM-based Wi-Fi Backscatter Communication. In Proceedings of the 2024 ACM MobiCom.   
[56] Qualcomm. 2024. Qualcomm SAW Filters. https://www.qualcomm.c om/products/technology/modems/rf fe-filter-products/product-list   
[57] RFID4u. 2024. RFID Basics - RFID Regulations. https://rfid4u.com/rfidregulations/   
[58] STMicroelectronics. 2020. Carrier cancellation for RAIN RFID readers with ST25RU3993. https://www.st.com/resource/en/application\_note/ an5532-carrier-cancellation-for-rain-rfid-readers-with-st25ru3993- stmicroelectronics.pdf   
[59] Gitanjali Swamy and Sanjay Sarma. 2003. Manufacturing cost simulations for low cost RFID systems. Auto-ID Center, White Paper (2003).

[60] Yole SystemPlus. 2023. Detailed Physical and Cost Analysis of Key SAW Filter Technologies. https://www.yolegroup.com/product/report/sawfilter-comparison-2023   
[61] Alien Technology. 2013. The Art and Science of UHF Passive Tag Design. https://www.alientechnology.com/wpcontent/uploads/whitepaper-Alien-Technology-The-Art-and-Science-of -Tag-Design-V1.0.pdf   
[62] Cristina Turcu. 2009. Development and Implementation of RFID Technology. IntechOpen.   
[63] Ju Wang, Liqiong Chang, Omid Abari, and Srinivasan Keshav. 2022. How Manufacturers Can Easily Improve Working Range of Passive RFIDs. In Proceedings of the 2022 IEEE International Conference on Sensing, Communication, and Networking (SECON).   
[64] Jue Wang, Haitham Hassanieh, Dina Katabi, and Piotr Indyk. 2012. Efficient and reliable low-power backscatter networks. In Proceedings of the 2012 ACM SIGCOMM.   
[65] Ju Wang, Jianyan Li, Mohammad Hossein Mazaheri, Keiko Katsuragawa, Daniel Vogel, and Omid Abari. 2020. Sensing finger input using an RFID transmission line. In Proceedings of the 2020 ACM SenSys.   
[66] Alex Williams. 2019. Streaming with DPDK: Raising the Throughput Ceiling with Drivers in User Space. https://www.gnuradio.org/grcon /grcon19/presentations/UHD\_Streaming\_with\_DPDK\_Raising\_the\_ Throughput\_Ceiling\_with\_Drivers\_in\_User\_Space/Alex%20William s%20-%20Streaming%20with%20DPDK.pdf   
[67] Dianhan Xie, Xudong Wang, and Aimin Tang. 2022. MetaSight: localizing blocked RFID objects by modulating NLOS signals via metasurfaces. In Proceedings of the 2022 ACM MobiSys.   
[68] Mingqi Xie, Meng Jin, Fengyuan Zhu, Yuzhe Zhang, Xiaohua Tian, Xinbing Wang, and Chenghu Zhou. 2024. Enabling High-rate Backscatter Sensing at Scale. In Proceedings of the 2024 ACM MobiCom.   
[69] Xilinx. 2015. Xilinx ZYNQ ZC706. https://www.xilinx.com/products/ boards-and-kits/ek-z7-zc706-g.html   
[70] Shatrughna Prasad Yadav and Subhash Chandra Bera. 2014. Nonlinearity effect of Power Amplifiers in wireless communication systems. In Proceedings of the 2014 International Conference on Electronics, Communication and Computational Engineering (ICECCE).   
[71] Lei Yang, Yekui Chen, Xiang-Yang Li, Chaowei Xiao, Mo Li, and Yunhao Liu. 2014. Tagoram: real-time tracking of mobile RFID tags to high precision using COTS devices. In Proceedings of the 2014 ACM MobiCom.   
[72] Lei Yang, Qiongzheng Lin, Xiangyang Li, Tianci Liu, and Yunhao Liu. 2015. See Through Walls with COTS RFID System!. In Proceedings of the 2015 ACM MobiCom.   
[73] Jiacheng Zhang, Meng Jin, Yimiao Sun, Weiguo Wang, Jia Zhang, Xin Na, Xiuzhen Guo, and Yuan He. 2024. RFinder: Pinpoint the Invisible RFID Tags in the Prefabricated Buildings. In Proceedings of the 2024 ACM EWSN.   
[74] Cui Zhao, Zhenjiang Li, Han Ding, Ge Wang, Wei Xi, and Jizhong Zhao. 2022. RF-Wise: Pushing the Limit of RFID-based Sensing. In Proceedings of the 2022 IEEE INFOCOM.   
[75] Fengyuan Zhu, Yuda Feng, Qianru Li, Xiaohua Tian, and Xinbing Wang. 2020. DigiScatter: efficiently prototyping large-scale OFDMA backscatter networks. In Proceedings of the 2020 ACM MobiSys.