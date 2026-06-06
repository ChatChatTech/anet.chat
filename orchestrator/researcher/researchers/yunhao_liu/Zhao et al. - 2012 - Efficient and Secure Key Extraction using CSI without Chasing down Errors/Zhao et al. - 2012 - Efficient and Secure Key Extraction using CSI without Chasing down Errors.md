# Efficient and Secure Key Extraction using CSI without Chasing down Errors

Jizhong Zhao†, Wei Xi†, Jinsong Han†, Shaojie Tang∗, Xiangyang Li∗, Yunhao Liu§, Yihong Gong†, Zehua Zhou†

†School of Electronic and Information Engineering, Xi’an Jiaotong University, China

∗ Department of Computer Science, Illinois Institute of Technology, USA

§ School of Software and TNLIST, Tsinghua University, China

Abstract—Generating keys and keeping them secret is critical in secure communications. Due to the “open-air” nature, key distribution is more susceptible to attacks in wireless communications. An ingenious solution is to generate common secret keys by two communicating parties separately without the need of key exchange or distribution, and regenerate them on needs. Recently, it is promising to extract keys by measuring the random variation in wireless channels, e.g., RSS. In this paper, we propose an efficient Secret Key Extraction protocol without Chasing down Errors, SKECE. It establishes common cryptographic keys for two communicating parties in wireless networks via the realtime measurement of Channel State Information (CSI). It outperforms RSS-based approaches for key generation in terms of multiple subcarriers measurement, perfect symmetry in channel, rapid decorrelation with distance, and high sensitivity towards environments. In the SKECE design, we also propose effective mechanisms such as the adaptive key stream generation, leakageresilient consistence validation, and weighted key recombination, to fully exploit the excellent properties of CSI. We implement SKECE on off-the-shelf 802.11n devices and evaluate its performance via extensive experiments. The results demonstrate that SKECE achieves a more than 3× throughput gain in the key generation from one subcarrier in static scenarios, and due to its high efficiency, a 50% reduction on the communication overhead compared to the state-of-the-art RSS-based approaches.

# I. INTRODUCTION

Wireless networks are susceptible to various attacks due to the “open air” nature of the wireless communication [22]. Cryptographic key establishment is a fundamental requirement for secure communication to support confidentiality and authentication services. However, it is difficult to ensure availability of a certificate authority or a key management center in dynamic wireless environments [4]. It is necessary to have alternatives for key agreement between wireless entities in a common channel [12] [14] [2].

One recent trend in this regard is to use physical-layer identification [16]. For example, received signal strength (RSS) becomes a popular statistic of the radio channel and is used as the source of secret information shared between two parties [11]. The variation over time of the RSS, caused by motion multipath fading, can be quantized and used for generating secret keys. Due to presence of noise and manufacturing variations, the generated secret keys might be different, which are corrected by information reconciliation. Finally, privacy amplification is introduced to convert this bit-string into a uniformly distributed string to make it secure enough.

However, RSS cannot work well in stationary scenarios due to infrequent and small scale variations in the channel measurements. To address this issue, we propose a secret key extraction based on the inherent randomness of wireless channels. In current widely used IEEE 802.11n networks, data is modulated on multiple Orthogonal Frequency Division Multiplexing (OFDM) subcarriers simultaneously. Each network interface card (NIC) of the device can get a value of Channel State Information (CSI) which describes the current condition of the channel in each subcarrier [1].

Different from RSS, CSI is a fine-grained value derived from the physical layer. It consists of the attenuation and phase shift experienced by each spatial stream on every subcarrier in the frequency domain. In contrast to having only one RSS value per packet, NIC can obtain multiple CSI values at one time. CSI provides other attractive properties. First, it is very sensitive to location such that two closely-placed receivers have very different readings by the same sender. Second, its readings of a pair of sender and receiver have a strong correlation. Third, it presents an excellent quality of randomness. Due to these characteristics, CSI is an ideal resource for secret key extraction.

In this paper, we present the design and implementation of CSI-based Secret Key Extraction without Chasing down Errors. SKECE exploits channel diversity to generate secret key using CSI. The contributions of this work are summarized as follows.

1. We first give an insight into how CSI measurements improve the effectiveness and safety of secret key extraction based on extensive real world measurements. Our observation suggests that CSI possesses excellent symmetry in channels, sensitivity to the environment, and rapidly decorrelates over a distance, which can work well in both static and mobile scenarios, and effectively prevent the predictable channel attack. Moreover, it can be measured from multiple subcarriers simultaneously, which significantly improves the rate of key generation.   
2. We propose an efficient and secure consistency validation method. It avoids leaking any available information to attackers, when two parties check the consistency of the generated bit streams. Additionally, it has a high precision rate of consistency validation.   
3. We creatively propose a weighted key recombination.

This method can efficiently recombine the mismatched bit streams into a consistent stream for two parties without detecting which bits are mismatched. It reduces the communication overhead while enhancing privacy and security by fully exploiting the special properties of OFDM modulation.

4. We evaluate SKECE through various experiments using off-the-shelf 802.11 devices in real indoor and outdoor scenarios.

The rest of this paper is organized as follows. Section 2 briefly reviews the related work. Section 3 presents real world observations on 802.11n devices and the adversary model. The design of SKECE is elaborated in Section 4, followed by performance evaluation in Section 5. We conclude the paper in Section 6.

# II. RELATED WORK

Encryption and authentication on communication between two parities in wireless networks is helpful for privacy and sensitive data protection [22] [24] [23] [13]. Extracting a shared secret key from the observation and processing of radio channel parameters has been proposed to address this problem without resorting to a fixed infrastructure.

Typical secret key generation process consists of three phases: randomness exploration, information reconciliation and privacy amplification [15]. In the randomness exploration, quantization is used to convert measurement values to information bits. A good quantizer can maximize the mutual information between Alice and Bob without information leakage. An algorithm is proposed in [11] to find such a quantizer. The information reconciliation process uses either error correcting codes [5], or interactive information reconciliation protocols, e.g. Cascade [3]. The universal hash functions are widely adopted in [17], [19], [10] to enhance privacy and security.

There are also many works on exploiting physical channel randomness feature to generate secret key [21], [9], [7]. The authors in [16] discuss the condition of generating secure keys and propose a solution to extract a secret key from unauthenticated wireless channels using channel impulse response and amplitude measurements. The authors in [11] summarize the processes needed for key extraction, give their choices of the methods in every process, and conduct extensive experiments to show the properties of RSS in real environment.

It can also be exploited for device pairing [8] and authentication [20]. Extracting secret keys over MIMO has been introduced in [18].

Previous works are mainly based on RSS, a coarse indicator of signal. As a fine-grained indicator of channels, CSI draws increasing attentions It can be measured using off-the-shelf 802.11n devices. In this paper, we suggest that the channel randomness can be further exploited through the channel diversity offered by CSI to efficiently extract secret key.

# III. PRELIMINARY OBSERVATION AND ATTACK MODELS

Orthogonal Frequency Division Multiplexing (OFDM) is a method of Multicarrier Modulation. OFDM divides previous single-carrier into a set of orthogonal sub-carriers, which can convert one rapidly modulated wideband signal to many slowly modulated narrowband signals. Channel state information (CSI) describes the current channels condition, which can reveal the effect of scattering, fading and power decay with distance. 802.11n protocol provides 30 pairs of amplitude and phase information out of 56/114 sub-carriers. Each pair of amplitude and phase describes the state information of a sub-carrier. The available CSI can reflect the environment influences on the signals transmitted from transmitter(s) to receiver(s):

![](images/f8a38787fc91b4274542702b25927abeab51d21249e0bbee909cc2be35972535.jpg)



Fig. 5. Alice walks freely to measure CSI values from 90 subcarriers simultaneously using a network card with 3 antennas.

$$
Y = H X + N \tag {1}
$$

$$
H = Y / X = h e ^ {j w}
$$

where X is transmit signal, Y is received signal, N is the noise, H is the CSI: the channel response at the receiver in frequency domain, h and w is the amplitude and phrase.

Utilizing off-the-shelf 802.11n wireless net card, CSI can be collected. It reports the channel matrices for 30 subcarrier groups, which is about one group for every 2 subcarriers at 20 MHz or one in 4 at 40 MHz. Although the driver does not directly provide functions to get CSI, there are some open source tools on Linux platform that can be used to collect CSI. We use Linux 802.11n CSI Tool and Intel 5300 wireless net card to spread out the signal received by one antenna and to provide 30 pairs of amplitude and phase CSI values to each antenna [6]. Since 802.11n supports MIMO, Fig. 1 shows the CSI measurements from three antennas of one NIC.

In our experiments, we setup one laptop (named Alice) to connect to the other laptop (named Bob). To establish a shared secret key, Alice and Bob should measure the variation of the wireless channel at the same time. However, typical commercial wireless transceivers are half duplex, i.e., they cannot transmit and receive signals simultaneously. We use ping command to guarantee the time between two directional channel measurements is small enough. The initiator requests the receiver to immediately reply once receiving order. The round-trip delay is always between 1ms-5ms. Another laptop (named Eve) is introduced to overhear the packets delivered between Alice and Bob and measure the CSI variation. Our observations for the feature of CSI is extracted into following 4 subsections.

![](images/ffe056fc87fdd7b0fb7f211099d2c5418cadcce280580d41bf900df6e8fa1f68.jpg)



Fig. 1. Multiple readings for CSI measurements from 30 subcarriers   
![](images/00e6832b8fde2a11d253b772311a6bc44ec12094b9a79278236803fa4235af89.jpg)



Fig. 3. Variations of CSI when Alice moves

# A. Reciprocity of Radio Wave Propagation

The multipath properties of a radio channel at any point are identical on both directions of a link. Figure 2 and Figure 3 shows the CSI values in static scenario and mobile scenario. It is easy to see that Alice and Bob have similar CSI variations.

# B. Temporal Variations in the Radio Channel

Figure 2 shows that CSI value is constantly changing over time in static scenario. That is because the multipath channel changes caused by any motion of people or objects in the environment near the link.

# C. Spatial Variations

The properties of a radio channel are unique to the locations of the two endpoints of the link. Figure 4 shows that Eve at a third location will measure a different CSI. This assertion is supported by the well-known Jakes uniform scattering model, which states that the received signal rapidly decorrelates over a distance of roughly half a wavelength, and that spatial separation of one to two wavelengths is sufficient for assuming independent fading paths.

# D. Multiple Subcarriers of CSI

IEEE 802. 11 a/g/n adopt OFDM to provide high throughput. In OFDM, a channel is orthogonally divided into multiple subcarriers. Figure 5 shows the multipath fading on a mobile radio channel reflected in 90 subcarriers. Measurements from multiple subcarriers can significantly improve the key generation rate.

![](images/941e881b2cdb859f41a84e0272f48ca2d4f48b1d6fc970f5edb3fa7319663609.jpg)



Fig. 2. CSI values in stationary environment

![](images/15be91286bc6add7448fdf18f87aebb1090f1d0dbcfd93f032f7c5b7aa5e6c5a.jpg)



Fig. 4. Variations of CSI in different locations

TABLE I VARIABLE DEFINITIONS 

<table><tr><td>Symbol</td><td>Definition</td></tr><tr><td>a, b</td><td>Alice, Bob</td></tr><tr><td>m</td><td>the number of subcarriers (m = 30 in our system)</td></tr><tr><td> $B_{ai}$ </td><td>a bit stream of Alice generated from her i-th subcarrier</td></tr><tr><td> $K_{ai}$ </td><td>a matched key of Alice generated from her i-th subcarrier</td></tr><tr><td> $K'_{ai}$ </td><td>a mismatched key of Alice generated from her i-th subcarrier</td></tr></table>

# E. Adversary Model

For easy of exposition, we summarize our adversary model as follows:

• An adversary Eve can listen to all communications between legitimate users.   
• Eve can also measure channels between herself and other parties anywhere she wants all the time.   
• Eve is free to set intermediate objects between two parties to affect their channels and derive some patterns known only to her.   
• Eve knows the key extraction algorithm and parameters settings.   
• Eve cannot prevent or modify any messages transmitted through the channel.

# IV. METHODOLOGY

Our CSI-based secret key extraction consists of three components: adaptive bit streams generation, leakage-resilient consistency validation, and weighted key recombination. For ease of presentation, Table I lists the symbols and notations used in this paper.

![](images/6a288288c3ace9e30344227370988cabc96cf470ef81501599d5e109520abe87.jpg)



Fig. 6. Timing diagram for SKECE

# A. Adaptive Bit Streams Generation

To establish a shared secret key, Alice and Bob measure the variations of the wireless channel between them over time by sending probes to each other and measure the CSI values. Ideally, Alice and Bob should both measure the CSI values at the same time. However, typical commercial wireless transceivers are half duplex, i.e., they cannot transmit and receive signals simultaneously. Thus, Alice and Bob can only measure the radio channel in one direction at a time. As long as the time between two directional channel measurements is much smaller than the change rate of channel, they will have similar CSI variations.

1) Converting the channel measurements to bits: Alice and Bob must convert their respective sequences of channel estimation $( i . e .$ , the amplitude of CSI $S _ { a } ( t _ { 1 } , . . . , t _ { n } )$ and $S _ { b } ( t _ { 1 } , . . . , t _ { n } ) )$ into identical bit-strings (0-1 sequences $B _ { a }$ and $B _ { b } )$ to be used as cryptographic keys. The bit-string should be (1) Sufficient long, ranging from 128 bits to 512 bits being the length of keys commonly used in symmetric cipher and (2) Statistically random, resilient to statistical defeats that could be exploited by attackers.

Many quantization methods have been proposed in previous works. For example work in [2] partitions the CSI measurements to multiple parts and performs quantization in every parts.

The quantizer we used is described as follows. (i) Alice and Bob calculate two adaptive thresholds $q _ { + }$ and $q _ { - }$ independently such that $q _ { + } = \mu _ { S ( t _ { 1 } , \ldots , t _ { n } ) } + \alpha * \sigma _ { S ( t _ { 1 } , \ldots , t _ { n } ) }$ and $q _ { - } = \mu _ { S ( t _ { 1 } , \ldots , t _ { n } ) } - \alpha * \sigma _ { S ( t _ { 1 } , \ldots , t _ { n } ) } ,$ where $\mu$ and σ are the mean value and standard deviation of $S ( t _ { 1 } , . . . , t _ { n } ) , \alpha \geq 0$ . (ii) Alice and Bob parse their CSI measurements and drop CSI estimates that lie between $q _ { + }$ and $q _ { - }$ and maintain a list of indices to track the CSI estimates that are dropped. They exchange their list of dropped CSI estimates and only keep the ones that they both decide not to drop. (iii) Alice and Bob generate their bit streams by extracting a $" 1 "$ or $\mathrm { ~ a ~ } ^ { 6 6 } 0 ^ { \circ }$ for each CSI estimate if the estimate lies above $q _ { + }$ or below $q _ { - } ,$ respectively.

# B. Leakage-resilient Consistency Validation

Alice and Bob extract the bit streams from the CSI measurements they collect using quantizers. There might be some differences in the corresponding bits between two streams. They arise due to three factors: presence of noise and interference, manufacturing variations, and the half-duplex mode of communication between transceivers.

It is crucial for Alice and Bob to validate the consistency of their bit streams without exposing available information to the channel that can be overheard by Eve.

One-way function is one that is easy to compute on every input, but hard to invert given the image of a random input. One-way function is ideal for Alice and Bob checking the consistency of keys without revealing information to malicious users. We use SHA-1 to hash the bit streams, which is highly secure and most widely used of one-way functions.

Alice sends the SHA-1 hash results $( H _ { a 1 } , . . . , H _ { a m } )$ of her bit streams to Bob, where m is the number of subcarriers. Bob hashes his bit streams in the same way, and compares the result with Alice’s value. The same hash results indicate the same original bit streams and vice versa. The same bit stream is thereby used as the secret-key, denoted as $K _ { j }$ . On the other hand, the different bit streams need to be corrected, denoted as $K _ { a i } ^ { \prime }$ and $K _ { b i } ^ { \prime } ,$ respectively.

However, SHA-1 produces a 160-bit message digest. Directly transmitting it may incur high communication cost. Fortunately, SHA-1 has the following feature: even a small change in the message will, with the overwhelming probability, result in a completely different hash. Due to the avalanche effect, it can be considered that for two different bit streams even if only one bit is different, each bit in the SHA-1 hash values will have 50%-50% chance of being different.

Due to this feature, it is unnecessary to verify entire hash values of two bit streams. Checking a small portion of hash values may have a high probability to find the difference between two different bit streams. The relationship between checking length r and the correct probability $\gamma$ can be described as follows:

$$
1 - (\frac {1}{2}) ^ {r} \geq \gamma \tag {2}
$$

$$
r = \lceil \log_ {1 / 2} (1 - \gamma) \rceil
$$

In our system, we set $r \ = \ 6$ to achieve above 98% correctness checking of detection results.

# C. Weighted Key Recombination

If the bit streams extracted from all m subcarriers are mismatched, they cannot be used as the secret key. In this case, we perform reconciliation to extract a consistent bit stream for Alice and Bob based on m extracted bit streams.Traditional information reconciliation techniques (e.g. the error correcting code and interactive information reconciliation) should first exclude matched bits to shrink the parts of the streams containing mismatched bits using parity checking or Hamming distance. The two parties permute their bit streams randomly, divide the stream into blocks, and check the parity of each block. If the parity is different between two sides, they repeat above procedure using a binary search until the size of blocks is so small that attempting to replace a few bits may correct the mismatch bits.

In contrast, using CSI can generate m bit streams from m subcarriers and most bits of each stream are consistent as we have seen in Section III. We thereby propose a weighted key recombination method. The key idea is very simple. We just let Alice and Bob randomly pick up bits from the m bit streams and recombine them into two new bit streams $B _ { a r }$ and $B _ { b r }$ without exchanging any information. Alice and Bob random select the bits in same positions from the corresponding bit stream. The newly generated bit steams have high probability to be matched. Alice and Bob check the bit stream via consistency validation. If $B _ { a r }$ is unequal to $B _ { b r }$ , they will recombine the key again. The following two components realize our method.

1) Difference degree detection: Difference degree detection estimate how different the two bit streams $K _ { a i } ^ { \prime }$ and $K _ { b i } ^ { \prime }$ are. Alice generates a random number X, and obtains the editor distance $d _ { a i }$ between $K _ { a i } ^ { \prime }$ and X. Then she sends $( d _ { a 1 } , . . . , d _ { a m } )$ and X to Bob. Bob compares its distance $d _ { b i }$ with $d _ { a i } .$ . The difference $\breve { d } _ { i }$ between $d _ { a i }$ and $d _ { b i }$ reflects the difference between $K _ { a i } ^ { \prime }$ and $K _ { b i } ^ { \prime }$ . A larger $\breve { d } _ { i }$ implies more difference between $K _ { a i } ^ { \prime }$ and $K _ { b i } ^ { \prime }$ .

Since Alice and Bob always generate very similar bit streams, $\breve { d } _ { i }$ is quite small in most situations. The value modulo $d _ { a i }$ and $d _ { b i }$ are enough to detect the difference of editor distances of two parties. We use $d _ { a i } ^ { \prime }$ instead of $d _ { a i }$ to compute the distance as follows:

$$
d _ {a i} ^ {\prime} = d _ {a i} \mod \theta \tag {3}
$$

$$
\tilde {d} _ {i} ^ {\prime} = \left| d _ {a i} ^ {\prime} - d _ {b i} ^ {\prime} \right| \tag {4}
$$

Choosing appropriate θ can reduce the communication cost and avoid leaking too much information to the adversary Eve. In our experiment, we set θ = 5.

2) Secret key recombination: Assume we randomly pick $l _ { i }$ bits from $K _ { a i } ^ { \prime }$ and $K _ { b i } ^ { \prime }$ to generate the new bit stream, the probability that all those $l _ { i }$ bits are matched in $K _ { b i } ^ { \prime }$ is

$$
\operatorname * {P r} _ {i} (l _ {i}) = (1 - \frac {\hat {d} _ {i}}{L}) (1 - \frac {\hat {d} _ {i}}{L - 1}) \dots (1 - \frac {\hat {d} _ {i}}{L - l _ {i}}) \tag {5}
$$

where $L$ is the length of the key, $\hat { d } _ { i }$ is the actual number of mismatched bits between $K _ { a i } ^ { \prime }$ and $K _ { b i } ^ { \prime }$ . Thus the overall probability to successfully generate a matched bit stream of length L within k rounds is

$$
1 - \left(1 - \prod_ {i = 1} ^ {m} \operatorname * {P r} _ {i} (l _ {i})\right) ^ {k}
$$

We introduce a weight $\omega _ { i }$ to decide how many bits should be selected from each one of m bit streams. The weight of each bit stream is computed as follows:

![](images/aed5370df6151977b02d1d094b5d5a20e722721060e1935672fe67e0a59aee96.jpg)



Fig. 7. Impact of α

![](images/8f1d3e0a01c7a2a69bfa7c1520af5bf34834031b69d52edeea82b75b2ac95960.jpg)



Fig. 8. Communication overhead 

<table><tr><td>Index</td><td>Status</td><td> $Distance_{ae}$ </td><td>Environment</td></tr><tr><td>A</td><td>Static</td><td>1.5 m</td><td>Indoor,</td></tr><tr><td>B</td><td>Static</td><td>3 m</td><td>Indoor, Complex</td></tr><tr><td>C</td><td>Mobile</td><td>3 m</td><td>Indoor</td></tr><tr><td>D</td><td>Mobile</td><td>10 cm</td><td>Indoor</td></tr><tr><td>E</td><td>Static</td><td>10 cm</td><td>Outdoor</td></tr><tr><td>F</td><td>Mobile</td><td>3 m</td><td>Outdoor, Complex</td></tr></table>

TABLE II PARAMETERS OF DATASETS

$$
\omega_ {i} = \frac {\theta - \tilde {d} _ {i} ^ {\prime}}{\sum_ {j = 1} ^ {m} (\theta - \tilde {d} _ {j} ^ {\prime})} \tag {6}
$$

Then, the number $l _ { i }$ of bits picked up from bit stream $B _ { i }$ used to recombine a new bit stream is

$$
l _ {i} = \left\lceil L * \omega_ {i} \right\rceil . \tag {7}
$$

Indeed, $\tilde { d } _ { i } ^ { \prime }$ is proportional to $\hat { d } _ { i } .$ , the value of ωi implies a match quality of two corresponding bit stream $B _ { a i }$ and $B _ { b i }$ . Following Equation $^ { 7 , }$ SKECE picks more bits from those streams with more matched bits between Alice and Bob.

# V. EVALUATION

We conduct our experiments in a wide variety of environmental settings and under different scenarios. The configuration is described in Section 3. In our experiments, there are six scenarios as shown in Table II.

Scenario A: Alice, Bob, and Eve put their laptops on a boardroom table in a meeting room. Alice and Eve are 1.5m apart. It’s a quiet room without subject moving.

Scenario B: Alice, Bob, and Eve stay in an office. Alice and Eve are 3m apart.There are various electronic devices and some walking people in the room.

Scenario C: Alice, Bob, and Eve are in a meeting room. Alice and Eve remain still separated with a distance of 3m. Bob walks freely in the room.

Scenario D: It is similar to scenario C, except that Alice and Eve are 10cm apart from each other.

Scenario E: Alice, Bob and Eve stay in a garden. Alice and Eve put their laptops on one bench separated with a distance of 10cm. Bob’s laptop is put on the other bench.

Scenario F: Alice, Bob and Eve walk freely on crowded street. Alice and Eve keep a 3m distance from each other.

![](images/2e3aa0c676534162dd646c71a384e435ff60e48fe6a028e34cb6a9e7b5a5a9fc.jpg)



(a) CSI measurements

![](images/a277f461067e9740743c6af1eda1864a1c61d14047dfa08ba358e8a89d4c5d31.jpg)



(b) RSS measurements   
Fig. 9. Measurements while walking in a meeting room

# A. Converting the Channel to Bits

As mentioned before, α affects the performance of bit streams extraction from CSI measurements. Figure 7 shows the impact of α in scenario C. For ease of description, we divide the bits into three kinds: ignored, mismatched and matched. An ignored bit is the dropped bit whose value ranges from $q _ { - }$ to $q _ { + }$ . A mismatched bit is the one extracted as $" 1 "$ in one party and extracted as $ { { } ^ { 6 } }  { 0 ^ { 9 } }$ in the other party. A matched bit is the one that two parties agree upon.

We investigate the variation of three kinds of bits extracted from 300 probes by increasing α from 0 to 1. Obviously, a smaller α improves the rate of bits generation but increases the mismatched bits ratio as well. With a larger $\alpha ,$ fewer bits can be extracted, while the mismatched bits ratio reduces.

Specifically, the bit error should be carefully deal with. If the sequence $B _ { a i }$ is different from $B _ { b i }$ even by a single bit, then the two bit streams cannot be used as cryptographic keys. As a result, two parties must reconciliate with each other. High probability bit error will increase the difficulty on information reconciliation. Therefore, we prefer to choose a larger α to keep low mismatched bits ratio.

However, a too large α will seriously influence the rate of bits generation. It is a fundamental trade-off in the selection α that affects the rate and the probability of error in opposing ways. An appreciate α can reduce the mismatched bits ratio at acceptable of key generation. From the figure we can see that α greater than 0.4 can reduce the bit errors to 0. In our experiment, we set α = 0.4 in mobile scenarios and α = 0.7 in static scenarios.

# B. Communication Overhead

The communication overhead is a major concern from both the performance and security perspectives, because the eavesdropper can overhear all communications among legitimate users. We measure the number of messages transmitted between Alice and Bob in each reconciliation process for SKECE and a typical RSS based approach, Cascade used in [3], [11].

In the simulation, both Alice and Bob have 30 different bit streams, and each stream has 300 random bits for SKECE. For Cascade, both the parties have one bit stream with 300 random bits. We randomly set 1 to 3 bits mismatched between two sides on their corresponding streams. We then measure the number of transmitted messages for achieving consistent 300 bits. Note that the number of bits for reporting differences in the reconciliation is very small, e.g. 1 bit used for parity checking plus several noise-padding bits or 6 bits for SKECE. The length of data field in the message packet is much shorter than other fields, e.g. preamble 32 bytes, address $6 \times 3$ bytes. Thus, the dominated communication overhead of reconciliation processes lies on the amount of delivered messages.

Figure 8 reports the comparison between two approaches. Clearly, SKECE outperforms Cascade. For SKECE, more than 80% cases need no more than 10 messages to achieve the consistence, while Cascade needs to deliver at least 20 messages in most rounds. This is because that SKECE exploits the excellent properties of CSI to utilize the matched bits to recombine the bit stream instead of adopting time-consuming detection and correction mechanisms in the reconciliation process. The result indicates that SKECE can reduce 50% communication overhead and benefit the efficiency improvement a lot.

# C. Mobile Endpoints

Considering that the mobility is an inherent property of wireless networks, we evaluate the performance of key extraction in scenario D. Figure 9 compares the channel estimation of CSI with that of RSS in a meeting room.

The channel often varies with a wide variation window both in CSI (17dB to 30dB) and RSS (-55dB to -42dB). Alice and Bob have a high degree of reciprocity. This experiment shows that the mobility in indoor setting helps achieve fast secret key extraction from the channel measurements, which increases the inherent entropy of the measurements and improves the reciprocity of the channel.

It is also interesting to see that Eve’s observation is quite different from Alice’s and Bob’s in CSI while she obtains some similarities with Alice and Bob in RSS. That is because CSI has more decorrelation over a distance.

# D. Static Endpoints

We conduct our experiment in static indoor and outdoor scenarios B and E as shown in Figure 10 and Figure 11.

![](images/5554557575d05d5e08e8aa734107a48eccecd8cfdd3b4ea1d28a1deba5aec59c.jpg)



(a) CSI measurements

![](images/92f91d04c15ccdd275c8ce71802f44db5f30698804987f64af4fbc21e7845720.jpg)



(b) RSS measurements

Fig. 10. Measurements in an office   
![](images/3d45bef3e52cc7cc0fb05ed3b58d69433eabe0558d578a483339dd698fbd537a.jpg)



(a) CSI measurements

![](images/a49965c8f377709f8b7ed211fdbefebd61483454ef4955eb9a352cfbb8a210c0.jpg)



(b) RSS measurements

Fig. 11. Measurements on the playground 

<table><tr><td>Test</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td></tr><tr><td>Frequency</td><td>0.73</td><td>0.57</td><td>0.84</td><td>0.38</td><td>0.12</td><td>0.75</td></tr><tr><td>Longest run of ones</td><td>0.32</td><td>0.11</td><td>0.16</td><td>0.88</td><td>0.67</td><td>0.21</td></tr><tr><td>FFT</td><td>0.60</td><td>0.73</td><td>0.95</td><td>0.34</td><td>0.79</td><td>0.68</td></tr><tr><td>Approx. Entropy</td><td>0.58</td><td>0.89</td><td>0.60</td><td>0.61</td><td>0.09</td><td>0.17</td></tr></table>

TABLE III NIST STATISTICAL TEST SUITE RESULTS

Figure 10(b) and Figure 11(b) show the variations of RSS measurements in an office and on the playground respectively. The channel variation in static scenarios are less noticeable than those in mobile scenario. We also note that the curves for Alice and Bob do not follow each other, indicating a channel with low reciprocity. This happens because the variation in a static channel is primarily caused by environment disturbance and hardware differences which are non-reciprocal. RSS measurements in this type of environment contain very low inherent entropy.

Figure 10(a) and Figure 11(a) shows the variations of CSI measurements collected in an office and on the playground respectively. Though Alice and Bob have different CSI values, their variations trends are similar. The result demonstrates that CSI significantly outperforms RSS on key generation in static scenarios. On one hand, CSI is more sensitive to environmental changes than RSS. On the other hand, CSI has a better correlation on channel estimation.

# E. Randomness of Key

Guaranteeing that the generated bits are random is crucial for key generation. Since we have assumed the adversary possesses a complete knowledge of our algorithm, any nonrandom process in the bit sequence can be leveraged by the adversary to reduce the time-complexity of cracking the key. For example, if there are always more “1”s than “0”s in bit stream, then the effective search space for the adversary would be reduced. Consequently, a variety of statistical tests have been proposed to test for various defects.

The p-value from each test is listed in Table III. To pass a test, the p-value for that test must be greater than 0.01. We find that the bit streams generated from CSI pass all the tests.

# F. The Correlation of Generated Key between Alice and Eve

The randomness test results indicate whether SKECE is secure to defend the key from crackers. It’s crucial for us to make sure whether Eve can generate the similar key from its channel measurements.

We evaluate the correlation of generated key between Eve and Alice in different scenarios. The most familiar measure of dependence between two quantities is “Pearson’s correlation”. It is +1 in the case of a perfect positive linear relationship (correlation), −1 in the case of a perfect decreasing (negative) linear relationship (anticorrelation). As it approaches zero, there is less of a relationship.

We use Pearson’s correlation to estimate the independence between Eve and Alice in scenarios B, D, and E as shown in Figure 12. All the values are between −0.15 and +0.15 for 30 subcarriers in all three scenarios. The result indicates that Eve’s keys are always independent from Alice’s key, even though Eve is 10cm apart from Alice in scenario D. It is because that the received signal rapidly decorrelates over a short distance. Since he observes a nearly independent channel, it is impossible for Eve to crack the key from the multipath fading channel used by Alice.

![](images/f6a00fe6d5f901de7e03c02ca6a4b11aa7ff491c2695c90616285de136a79fe7.jpg)



Fig. 12. The correlation of generated key between Alice and Eve

![](images/433592320e36e34c4a31dc19e55c7ab83a6458cb05e70f57a96c25e725d08e1e.jpg)



Fig. 13. The correlation of generated key among 30 subcarriers

![](images/ea9f7f4da2ef76d9074f1408272018191191a4cee9c93f5fc3cad3cb687b7a04.jpg)



Fig. 14. Secret bit rate in different scenarios

![](images/897dadba4815c2596ea55318ac8eabca604d86b1e53713dbc4a9bbdb9f624d4b.jpg)



![](images/ee898712c29631a4d188756d5b3fe81b405f7737f82b759478db9c055a440604.jpg)



(b)

Fig. 15. (a) Predictable variations of the RSS values, (b) A magnified portion of the traces.   
![](images/bcf925cb9bcf1949af5e89270dc815a093ba4dcd72e047b2be76f4e31a9949c7.jpg)



![](images/2d2ca85cb8b6389677f0262be5fcabb13e54efb630625de8132bce58cd1990a0.jpg)



(b)   
Fig. 16. (a) The variations of the CSI values, (b) A magnified portion of the traces.

# G. Independence of Bits of 30 Subcarriers

We extract secret-key based on CSI measurement from 30 subcarriers. The correlation of 30 bit streams of subcarriers concerns whether all these bit streams can be used as secretkey.

We also evaluate the correlation using Pearson’s correlation. The bit streams are generated in scenario C.

Figure 13 plots the correlations among all 30 subcarriers. All the correlations are always between −0.3 and +0.3 except the correlations with themselves. It states that the key extracted from 30 subcarriers is independent. OFDM encodes digital data on multiple carrier frequencies. These sub-carrier signals are orthogonal with different frequencies. They have the different channel responses at the receiver in frequency domain. The extracted bit streams from 30 subcarriers are independent with each other, all of which can be used as secret-keys simultaneously.

# H. Rate of Key Generation

An important quantity of interest is the rate of generating secret bits, expressed in secret-bits per second or s-bits/sec. Naturally, it is desirable that Alice and Bob achieve a high secret-bit rate. According to 802.11 recommendations, it is generally desirable for master keys to be refreshed at one hour intervals.

Figure 14 compares the rate of key generation from CSI and RSS measurements in scenarios A, C, E, and F. It is easy to find that the rate of key generation from CSI is nearly 4 times higher than RSS in scenario A, and is more than 6 times higher in scenario C.

In order to facilitate the comparison, Figure 14 only shows the mean of key generation rate of 30 subcarriers. Infact, the key generated from CSI is the sum of all the subcarriers. Thus, the rate of key generation is thirty-fold the mean value. The rate of key generation from CSI is 32 times higher than RSS in mobile scenarios, and 100 times higher in static scenarios.

# I. Predictable Channel Attack

As mentioned earlier, stationary environments reduce the variation of the channel. An intelligent adversary can use deliberately planned movements in such scenarios to produce desired and predictable changes in the channel between the actual sender and receiver.

We conduct an experiment to emulate the predictable channel attack in the meeting room. Alice and Bob are separated by 3m, they keep still and probe the channel to generate the bit streams at 10Hz frequency. Eve periodically blocks the lineof-sight transmission between Alice and Bob. The distance between Alice and Eve is around 1m.

Figure 15 shows the variation of the RSS values. The RSS values display periodical changes with the transfer of time. The RSS drops when Eve block the line of sight path, and then picks up when Eve move away. The pattern of variation follows the movements. In this scenario, it produces a predictable pattern of secret bits from RSS measurements.

Figure 16 shows the variation of the CSI values. Though its change also displays periodicity, the variation of bit streams is still random, which is unpredictable. It is because CSI is more sensitive to environment and it will be changed by any variations of different environmental factors. As long as the attacker at a third location is more than a few wavelengths from either endpoint, it will not produce a predictable pattern of secret bits from CSI measurements.

# VI. CONCLUSION

In this paper, we proposed a protocol, called SKECE, that exploits the reciprocity of the transfer function of the wireless multipath channel to establish a common secret key between two communicating entities. Our protocol obtains a security advantage from the fact that the channel is random and the response decorrelates rapidly over distance, which can defend against a passive eavesdropper as well as an active adversary attempting predictable channel attack.

We also present the results of a thorough effort to experimentally validate the feasibility of the wireless channel for secret key generation. We used off-the-shelf 802.11n cards for collecting CSI measurements. SKECE generates secret bits at a high rate from 30 subcarriers both in static and mobile scenarios. It adopts a weighted key recombination algorithm to obtain a consistent bit stream without chasing down the mismatched bits, once all the 30 pairs of bit streams are inconsistent. It reduces the communication overhead by 50%.

# REFERENCES

[1] 802.11n working group and others. IEEE 802.11n Specification 2009.   
[2] Y. Amir, Y. Kim, C. Nita-Rotaru, J. Schultz, J. Stanton, and G. Tsudik. Exploring robustness in group key agreement. In Proceedings of IEEE ICDCS, pages 399–408, 2001.   
[3] G. Brassard and L. Salvail. Secret-key reconciliation by public discussion. In Proceedings of Advances in Cryptology-Eurocrypt, pages 410–423. Springer, 1994.   
[4] H. Chan, A. Perrig, and D. Song. Random key predistribution schemes for sensor networks. In Proceedings of Symposium on Security and Privacy, pages 197–213, 2003.   
[5] Y. Dodis, L. Reyzin, and A. Smith. Fuzzy extractors: How to generate strong keys from biometrics and other noisy data. In Proceedings of Advances in Cryptology-Eurocrypt, pages 523–540. Springer, 2004.   
[6] D. Halperin, W. Hu, A. Sheth, and D. Wetherall. Tool release: gathering 802.11 n traces with channel state information. ACM SIGCOMM Computer Communication Review, 41(1):53–53, 2011.   
[7] A. Hassan, W. Stark, J. Hershey, and S. Chennakeshu. Cryptographic key agreement for mobile radio. Digital Signal Processing, 6(4):207– 212, 1996.   
[8] T. Heartbeats. Proximate: Proximity-based secure pairing using ambient wireless signals. IEEE Wireless Communications, page 8, 2011.   
[9] J. Hershey, A. Hassan, and R. Yarlagadda. Unconventional cryptographic keying variable management. IEEE Transactions on Communications, 43(1):3–6, 1995.   
[10] R. Impagliazzo, L. Levin, and M. Luby. Pseudo-random generation from one-way functions. In Proceedings of ACM STOC, pages 12–24, 1989.   
[11] S. Jana, S. Premnath, M. Clark, S. Kasera, N. Patwari, and S. Krishnamurthy. On the effectiveness of secret key extraction from wireless signal strength in real environments. In Proceedings of ACM MobiCom, pages 321–332, 2009.   
[12] P. Lee, J. Lui, and D. Yau. Distributed collaborative key agreement and authentication protocols for dynamic peer groups. IEEE/ACM Transactions on Networking, 14(2):263–276, 2006.   
[13] M. Li, W. Lou, and K. Ren. Data security and privacy in wireless body area networks. IEEE Wireless Communications, 17(1):51–58, 2010.   
[14] D. Liu, P. Ning, and R. Li. Establishing pairwise keys in distributed sensor networks. ACM Transactions on Information and System Security, 8(1):41–77, 2005.   
[15] Y. Liu, S. Draper, and A. Sayeed. Exploiting channel diversity in secret key generation from multipath fading randomness. IEEE Transactions on Information Forensics and Security, PP(99):1, 2012.   
[16] S. Mathur, W. Trappe, N. Mandayam, C. Ye, and A. Reznik. Radiotelepathy: extracting a secret key from an unauthenticated wireless channel. In Proceedings of ACM MobiCom, pages 128–139, 2008.   
[17] U. Maurer and S. Wolf. Secret-key agreement over unauthenticated public channels - part iii: Privacy amplification. IEEE Transactions on Information Theory, 49(4):839–851, Apr. 2003.   
[18] J. Wallace and R. Sharma. Automatic secret keys from reciprocal mimo wireless channels: Measurement and analysis. IEEE Transactions on Information Forensics and Security, 5(3):381–392, 2010.   
[19] M. Wilhelm, I. Martinovic, and J. Schmitt. On key agreement in wireless sensor networks based on radio transmission properties. In Proceedings of IEEE Workshop on Secure Network Protocols, pages 37–42, 2009.   
[20] L. Xiao, L. Greenstein, N. Mandayam, and W. Trappe. Using the physical layer for wireless authentication in time-variant channels. IEEE Transactions on Wireless Communications, 7(7):2571–2579, 2008.   
[21] C. Ye, S. Mathur, A. Reznik, Y. Shah, W. Trappe, and N. Mandayam. Information-theoretically secret key generation for fading wireless channels. IEEE Transactions on Information Forensics and Security, 5(2):240 –254, june 2010.   
[22] L. Zhou and Z. Haas. Securing ad hoc networks. IEEE Network, 13(6):24–30, 1999.   
[23] S. Zhu, S. Setia, S. Jajodia, and P. Ning. An interleaved hop-byhop authentication scheme for filtering of injected false data in sensor networks. In Proceedings of IEEE Symposium on Security and Privacy, pages 259–271, 2004.   
[24] S. Zhu, S. Xu, S. Setia, and S. Jajodia. Establishing pairwise keys for secure communication in ad hoc networks: A probabilistic approach. In Proceedings of IEEE ICNP, pages 326–335, 2003.