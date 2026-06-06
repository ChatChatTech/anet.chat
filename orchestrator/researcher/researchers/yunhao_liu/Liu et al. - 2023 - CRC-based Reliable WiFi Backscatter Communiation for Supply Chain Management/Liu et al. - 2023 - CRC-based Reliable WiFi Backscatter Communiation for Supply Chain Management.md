Article

# CRC-based Reliable WiFi Backscatter Communiation for Supply Chain Management

Yun-Hao Liu 1, Tao Liu 2, Yimeng Huang 1, Han Ding 3, Wei Xi 3 and Wei Gong 1,\*

School of Computer Science and Technology, University of Science and Technology of China, Hefei, 230026, An hui, China; zkdjy2018lyh@mail.ustc.edu.cn(Y.L.); huangyimeng@mail.ustc.edu.cn(Y.H.); weigong@ustc.edu.cn(W.G.)   
2 Business School, China University of Political Science and Law, 102249, Beijing, China; Liuliutao@cutech.edu.cn(T.L.)   
3 School of Computer Science and Technology, Xi’an Jiaotong University, Xi’an, 710049, Shaanxi, China; dinghan@xjtu.edu.cn(H.D.); xiwei@xjtu.edu.cn(W.X.)   
Correspondence: weigong@ustc.edu.cn

Abstract: Supply chain management is aimed to keep going long-term performance of the supply chain and minimize the costs. Backscatter technology provides a more efficient way of being able to identify items and real-time monitoring. Among the backscatter systems, the ambient backscatter communication (AmBC) system provides a prospect of ultra-low energy consumption and does not require controlled excitation devices. In this paper, we introduce CRCScatter, a CRC reverse algorithm-based AmBC system using a single access point (AP). A CRC reverse decoder is applied to reverse the ambient data from CRC32 sequence in the backscatter packet and realize single-AP decoding. Based on the nature of DBPSK modulation in WiFi signal, the CRCScatter system obtains the tag data by XOR and Differential decoder. Our simulation results verify the effectiveness of our proposed system in the low SNR regime. The average decoding time of CRCScatter system is independent of the length of tag data. Furthermore, our system can append redundant bits in the tag data to improve the decoding accuracy while not increasing the decoding time.

Keywords: backscatter; CRC reverse; WiFi

Citation: Liu, Y.; Liu, T.; Huang, Y.; Ding H.; Xi W.; Gong W. Title. Appl. Sci. 2023, 1, 0. https://doi.org/

Received:

Revised:

Accepted:

Published:

Copyright: © 2023 by the authors. Submitted to Appl. Sci. for possible open access publication under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/).

# 1. Introduction

In the next generation Internet of Things, billions of devices will connect to existing networks for data communications. In the highly competitive industry services, supply chain management has very high requirements for informatization. The monitoring and communication equipment in the supply chain will make power consumption a serious challenge. Enterprises that give priority to the application of low energy consumption equipment and technology in the supply chain will gain higher profits. The power consumption of these devices will become a critical problem. According to a survey of wireless communication [1], most of the energy consumed by active communication systems is spent on energy-hungry active RF devices such as power amplifiers.

To reduce energy consumption and provide long-time communication in passive conditions, a novel low-cost and energy-efficient communication system, backscatter communication system was proposed and could reduce power consumption to the microwatt level. These advantages make backscattering promising for large-scale applications in smart home [2], smart agriculture [3], and other fields. So far, backscatter has been implemented in varieties of radios, including WiFi [4–6], ZigBee [7], LoRa [8] and Bluetooth [9–11]. Traditional backscatter systems require specialized hardware to achieve backscatter communication. WiFi backscatter [12] requires a power supply to support the system to connect to the network. BackFi [13] applies customized full duplex hardware to enable backscatter communication. Passive WiFi [14] requires a dedicated continuous wave signal generator as the excitation signal source. These additional requirements on hardware will limit the application scenarios of the backscatter system. HitchHike [15] achieves backscatter communication by commodity devices and introduces the idea of “codeword translation” which allows backscatter tag to embed its information on standard 802.11b packets. Codeword translation then has been extended to Bluetooth, ZigBee, and LoRa by FreeRider [16] and LoRa Backscatter [17]. In detail, HitchHike system deploys one more access point to demodulate the excitation signal and the backscatter signal respectively, which enables the system to decode the tag data by a simple and efficient XOR decoder.

![](images/0356e6c84ffbd92ae7cd1636e666044f4e85f3d171b2ce45bcd1bbf01dfa63eb.jpg)



(a) backscatter system model A

![](images/36fed397033c28d2ccbdfa9523b908330977a29a31a02de976ea76bcea505a6f.jpg)



(b) backscatter system model B   
Figure 1. The structure of backscatter communication systems.

We can summarize the backscatter systems as two modes in Figure 1. In model A, the backscatter communication system with a controlled excitation source enables decoding at a single-AP receiver while employing additional requirements on the excitation source. The controlled excitation source signal does not contain valid information but adds interference to other communications. In model $\scriptstyle \mathrm { \mathrm { B } , }$ the backscatter communication system deploys one more access point (AP) to receive the excitation signal to decode tag data directly using the backscatter data and original data. In general, compared with the active communication infrastructure, these two backscatter system models have additional hardware requirements at the transmitter or receiver. The deployment of systems will cause extra costs and face difficulties in the large-scale deployment on current WiFi infrastructure.

Inspired by these observations, this paper focuses on single-AP decoding with ambient WiFi signals. The main contributions in this work are summarized as follows.

We propose a CRC reverse algorithm-based single-AP backscatter system using ambient WiFi signal. The system uses a CRC reverse decoder to solve the problem of decoding ambient data from a backscatter packet.   
We provide simulation results to verify the decoding method of our system and analyze the system performance. The CRCScatter system achieves decoding tag data bit error rate of $1 0 ^ { - 2 }$ at SNR = −7.5 dB.   
We verify that the CRC reverse algorithm is better than the brute-force search method in decoding efficiency and the average decoding time of CRCScatter system is independent of the tag data length. We propose an improved method of adding redundant bits to the tag data to improve the decoding accuracy of the system in the presence of noise interference.

# 2. System Model

The system model for the CRCScatter system consists of an excitation source, a tag, and a single-AP receiver as shown in Figure 2. The ambient excitation source broadcasts the exciting signal to the tag of the CRCScatter system. The tag transmits its data by backscattering and modulating the exciting signal. The CRCScatter receiver uses only one access point to receive the backscatter signal from the tag to the receiver. Considering the tag data transmission, the tag data is encoded on the WiFi signal by tag modulation and the receiver uses the backscatter packet to reverse the original packet and decode the tag data. In this section, we present how the tag piggybacks data on a backscatter signal using codeword translation. This paper focuses on the 1 Mbit/s data rate and other data rates will be implemented in our future work.

![](images/dc6d1804e735c7548c290568f342e9ff0dce4d08d3c10a5143ed4e339359dee6.jpg)



Figure 2. CRCScatter system model.

# 2.1. 802.11b packet structure

The 802.11b protocol specifies that the transmitted packet contains PLCP Preamble, PLCP Header, and PSDU. Among them, PSDU has variable length and contains a MAC frame in the CRCScatter system. The MAC frame consists of MAC Header, Frame Body, and the frame check sequence (FCS). The Frame Body field carries the transmitted data and the CRC32 sequence in FCS field can detect bit errors in the MAC frame. The part of the packet other than the data segment contains packet control information, if these fields are modified by tag, then the receiver may not be able to demodulate correctly. To receive and demodulate properly, the CRCScatter tag only modulates the Frame Body field in the packet. The received backscatter packet structure is shown in Figure 3.

![](images/cb224f3cc39398412c83bfd91bff7e573923458b2401031c823bd9c45ece4413.jpg)



Figure 3. The structure of received backscatter packet.

# 2.2. Codeword translation

A novel technology called codeword translation is proposed in HitchHike [15] for tag modulation. The codeword translation method enables the piggybacking of tag data information while ensuring that the backscatter packet is still an 802.11b WiFi packet that can be demodulated by the receiver. Specifically, the 802.11b 1Mbps signal uses two codewords to encode packets and there is a 180° phase difference between these two codewords. The tag adopts BPSK modulation to change the codeword by a phase offset during modulating and backscattering the exciting signal exhibited in Table 1.

Table 1. Encoding at the tag. 

<table><tr><td>tag bit</td><td>phase offset</td></tr><tr><td>0</td><td>0</td></tr><tr><td>1</td><td> $180^{\circ}$ </td></tr></table>

In tag modulation, one tag data bit corresponds to one data bit. This correspondence indicates that the encoding scheme is efficient and redundancy-free. HitchHike system proposed an efficient XOR decoder to get the tag data from the backscatter data and original data. The decoding formula of the XOR decoder can be written as:

$$
\text { tag   data } = \text { backscatter   data } \oplus \text { original   data }. \tag {1}
$$

However, in the CRCScatter system there is only one AP for receiving signals. The backscatter data for the XOR decoder can be obtained directly, while the original data need to be calculated from the backscatter packet by the CRCScatter decoder. Thus the decoding function of the CRCScatter system can be expressed as follows:

$$
(\text { original   packet }, \text { tag   data }) = \text { CRCScatter } (\text { backscatter   packet }). \tag {2}
$$

# 3. CRCScatter decoder design

# 3.1. CRCScatter decoder overview

![](images/ac97e5f1d2d685b3a7fb53bcf54ccba72e053e543db5580cf00757ba74c2e576.jpg)



Figure 4. CRCScatter decoder overview. The decoding procedure can be divided into two steps. The first step is to reverse the original data marked in blue, and the second step is to calculate the tag data marked in red.

The overview of the CRCScatter’s decoding method at the receiver is illustrated in Figure 4. The procedure of tag data decoding by the CRCScatter decoder can be divided into two steps.

The first step is to reverse the backscatter packet into the original packet. The received backscatter MAC frame contains MAC Header, Frame Body, and FCS, but the tag only modulates the Frame Body field. The MAC Header field and FCS field in the original packet are the same as those in the backscatter packet. Nevertheless, the original data cannot be obtained directly because the Frame Body field has been modulated by the tag. The 802.11b protocol specifies the correlation between the FCS field and transmitted data in the 802.11b packet. CRC reverse decoder uses this intrinsic correlation of the 802.11b packet as a constraint in calculation and utilizes two CRC algorithms to reverse the original data from the backscatter packet.

The second step is to calculate the tag data based on the received backscatter data and the original data obtained by the CRC reverse decoder. The 802.11b data transmission uses DBPSK modulation, while the tag adopts BPSK modulation. This difference in modulation prevents the original XOR decoder from getting the correct tag data. Therefore, CRCScatter uses a decoder that combines XOR operation and differential decoding to calculate the tag data.

In summary, the CRCScatter system deploys two decoders to calculate the original packet and tag data in steps. The function of the CRC reverse decoder is to get the original data from the backscatter packet, and the XOR and Differential decoder removes the differential effects in modulation to obtain the correct tag data.

# 3.2. CRC reverse decoder

# 3.2.1. The algorithms of CRC in the CRC reverse decoder

To detect the unpredictable bit errors in the received packet, Cyclic Redundancy Check (CRC) sequence is invented and transmitted with the data. In the 802.11b packet, the CRC32 is applied in the FCS field of the MAC frame to protect the MAC Header and Frame Body fields. The CRC32 value can be calculated by bit shift and XOR operation on a 32-bit CRC register. The bit-oriented calculation algorithm of the CRC value is given by the 802.11b protocol shown in Algorithm 1. The CRC algorithm contains three constants: CRCPOLY, INITXOR, and FINALXOR. The value of the constants in CRC32 is given by: CRCPOLY = 0x04C11DB7, INITXOR = FINALXOR = 0xFFFFFFFF. Moreover, we can use the initial and final state of the crcreg to replace INITXOR and FINALXOR when focusing on the calculation of the CRC register.

Algorithm 1 calculation of the CRC   
```ruby
Input: data bits a
Output: CRC register value crcreg
    crcreg ← INITXOR
    i ← 0
    while i < a.length do
    LEFTSHIFT(crcreg)
    if bit_just_shifted_out ≠ ai then
    crcreg ← crcreg ⊕ CRCPOLY
    end if
    i ← i + 1
end while
crcreg ← crcreg ⊕ FINALXOR 
```

Algorithm 2 CRC32 reverse algorithm   
Input: final CRC register value r, reversed data bits a
Output: initial CRC register value $r'$ $i \leftarrow a.length - 1$ $crcreg \leftarrow r$ while $i \geq 0$ do
    if $crcreg_{31} = 1$ then $crcreg \leftarrow crcreg \oplus CRCPOLY$ RIGHTSHIFT(crcreg) $crcreg_{0} = a_{i} \oplus 1$ else
    RIGHTSHIFT(crcreg) $crcreg_{0} = a_{i}$ end if $i \leftarrow i - 1$ end while $r' \leftarrow crcreg$

Assuming the initial CRC register value $r ^ { \prime }$ and the data bits a are available, the CRC algorithm can calculate the final value r. If the final CRC register value r and the calculated data a are given, we can reverse the procedure of the CRC algorithm to obtain the initial value r0. The CRC reverse algorithm [18] is given by Algorithm 2.

We can represent CRC algorithm and CRC reverse algorithm as functions where $r ^ { \prime }$ and r stand for the initial and final value of CRC register while a stands for the calculated data bits. If a set of CRC register values and data bits are given, the two algorithms are opposite computational processes, and the two functions hold simultaneously.

$$
r = \operatorname{crc} \left(r ^ {\prime}, a\right), \quad r ^ {\prime} = \operatorname {c r c \_ r e v e r s e} (r, a). \tag {3}
$$

# 3.2.2. How to reverse the unknown data from CRC32 value?

The algorithms of CRC use forward or reverse methods to calculate the value of the CRC register from the data bits a. Suppose we want to reverse the unknown data bits from the initial and final state values of CRC32. Assuming the unknown data length l is known, we can use brute-force search to find the possible original data from all $2 ^ { l }$ data sequences. When the data length l is greater than 32 bits, the number of solutions is $2 ^ { l - 3 2 }$ . If the data length does not exceed 32 bits, the unknown data sequence is unique. The relationship between the number of solutions $N _ { l }$ and the data length l can be expressed as follows:

$$
N _ {l} = \left\{ \begin{array}{l l} 2 ^ {l - 3 2}, & l > 3 2 \\ 1, & l \leq 3 2 \end{array} \right. \tag {4}
$$

To ensure the uniqueness of the results, we discuss the unknown data bits with a length of 32 bits. In algorithms of CRC, data sequence a is the independent variable of the functions. We need to find the new connection between a and CRC register value to calculate the unknown bits. Assuming the length of data bits is the same as the length of CRC32, the CRC algorithm has properties [18] which can be written as:

$$
\operatorname{crc} \left(r _ {1}, a _ {1}\right) \oplus \operatorname{crc} \left(r _ {2}, a _ {2}\right) = \operatorname{crc} \left(r _ {1} \oplus r _ {2}, a _ {1} \oplus a _ {2}\right), \tag {5}
$$

$$
c r c (r ^ {\prime}, a) = c r c (a, r ^ {\prime}) = r. \tag {6}
$$

Taking the equivalence relation of (6) and the correlation of algorithms (3), we can obtain a new equation (7) to calculate data bits a exhibited in Figure 5.

![](images/c63f200b68d4c4ce1dfc4ed977a1e1b2da36e64ea71422a9bb2d41385c254f76.jpg)



![](images/e3c4cb18fad11a3a2fc5c677c57a6cf0196c0bc76c89dd7d26bb57346fdd601c.jpg)



(a) Forward calculation by CRC algorithm

![](images/0d046449d515d2fce63fdd476b4dfc2ed5d0a2d1ef26fbeeef7f30229cf3cce2.jpg)



![](images/12d6a3e18409be1dde5cc5a98dcada50b75e9ad6727fbec954d5199242ef0487.jpg)



(b) Reverse calculation by CRC reverse algorithm   
Figure 5. Equation relations in CRC calculation. Because the CRC algorithm and the CRC reverse algorithm are different only in the calculation direction, the functions in (a) and (b) should hold simultaneously.

$$
a = \operatorname{crc} _ {-} \text { reverse } (r, r ^ {\prime}). \tag {7}
$$

# 3.2.3. How to reverse the original data?

We can divide the MAC frame into MAC Header $K ,$ CRC32 sequence $R ,$ and the unknown original data a. Since the length of the original data is limited, theoretically, the original data can be obtained by brute-force search method. The average number of enumerations is exponential to the original data length. For the requirement of immediate communication and a high tag data transmission rate, brute-force search cannot satisfy them simultaneously.

If the length of the Frame Body field does not exceed 32 bits, we can get the original data by the method of reversing unknown data bits. First, we use the algorithms of CRC to compute the initial and final values of CRC register $r ^ { \prime }$ and r. According to the 802.11b protocol, the initial value of the CRC register for forwarding calculation is INITXOR while the final value of the CRC register $r ^ { \prime }$ can be obtained from the FCS field. Then, the original data can be calculated using the method of reversing unknown data bits. The original packet can be obtained by replacing the backscatter data in the backscatter packet with the original data. The procedure for reversing original data from the backscatter MAC frame is presented in Algorithm 3.

Algorithm 3 calculation in CRC reverse decoder   
Input: MAC Header K, CRC32 sequence R
Output: original data a $r \leftarrow R \oplus$ FINALXOR $r' \leftarrow \text{crc(INITXOR, K)}$ $a \leftarrow \text{crc\_reverse}(r, r')$

CRC reverse decoder achieves efficient decoding computation in the case of transmission tag data length not exceeding 32 bits. At the system level, the CRC reverse decoder is functionally identical to the receiver of a traditional backscatter system that receives the original packet. In other words, the CRCScatter system reduces the hardware requirements by the CRC reverse decoding method. At the principle level, the core for decoding is the presence of a bit sequence within the packet that constrains the transmitted data. Because the CRC reverse decoder only uses the constraints of the FCS field, the maximum length of the tag data is 32 bits. When the tag data length exceeds the limit, the reversed original data at the decoder will not satisfy the uniqueness of solutions. The length of the tag data transmitted by the system can be extended when more constraints are applied to the packets.

# 3.3. XOR and Differential decoder

The 802.11 protocol specifies that the DSSS system uses the baseband modulation of DBPSK to provide the 1 Mbit/s data rate and solve the problem of phase ambiguity in BPSK. In DBPSK modulation, the input original data a is calculated by differential encoding to obtain differential data $e ,$ then the differential data e is modulated by the conventional BPSK modulator. In other words, we can assume that the 802.11b signal in our system transmits the differential data e rather than the original data a. Since the CRCScatter tag can modify the transmitted data by codeword translation, we set the differential data modified by the tag to $e ^ { \prime }$ and the backscatter data to $a ^ { \prime } .$ According to the decoding formula (1) and the process shown in Figure $6 ,$ the tag data t can be represented using differential data e and $e ^ { \prime } .$ .

![](images/e86301e6d845a270504a0c1b785cedb5b3af3e983ee286769d981aba8283084b.jpg)



Figure 6. The tag modulates the differential data rather than the original data, and tag data t can be calculated by e and $e ^ { \prime } .$

$$
t = e \oplus e ^ {\prime}, \tag {8}
$$

In differential encoding, the transmitted data a and the differential data e should satisfy the encoding formula written as

$$
e _ {i} = e _ {i - 1} \oplus a _ {i}. \tag {9}
$$

We can use original data a and backscatter data $a ^ { \prime }$ to calculate tag data t by differential encoding formula. The tag data calculation needs to be discussed separately. The first tag data bit $t _ { 0 }$ is calculated differently from the other tag data bits.

$$
t _ {0} = e _ {0} \oplus e _ {0} ^ {\prime} = a _ {0} \oplus a _ {0} ^ {\prime}, \tag {10}
$$

$$
t _ {i} = e _ {i} \oplus e _ {i} ^ {\prime} = (e _ {i - 1} \oplus a _ {i}) \oplus (e _ {i - 1} ^ {\prime} \oplus a _ {i} ^ {\prime}) = (a _ {i} \oplus a _ {i} ^ {\prime}) \oplus (e _ {i - 1} \oplus e _ {i - 1} ^ {\prime}) = (a _ {i} \oplus a _ {i} ^ {\prime}) \oplus t _ {i - 1}. \tag {11}
$$

Algorithm 4 presents the procedure to get correct tag data t from backscatter data $a ^ { \prime }$ and original data a described in this section.

Algorithm 4 calculation in XOR and Differential decoder   
Input: backscatter data $a'$ , original data a
Output: tag data t
temp = $a' \oplus a$ $i \leftarrow 0$ while i < t.length do
    if i = 0 then $t_i = temp_i$ else $t_i = t_{i-1} \oplus temp_i$ end if $i \leftarrow i + 1$ end while

In a real communication environment, bit errors in the received backscatter packet caused by noise will result in errors in decoding tag data. Similar to the CRC32 sequence in the MAC frame, the tag can add redundancy check bits and piggyback them together with real tag data. The CRCScatter decoder is required to check the tag data by redundant bits after tag data decoding. In this way, the system can identify and discard incorrect results, and the accuracy of the decoding will be improved.

# 4. Simulation results

In this section, simulation results are presented to evaluate the performance of the proposed system. In our simulations, DBPSK modulation is used in 802.11b transmission and the length of the Frame Body field is set to 32 bits. The tag data length N and the SNR will be varied to calibrate the results.

![](images/9fd4f93bb5ba524e55d0b58faa06e3d3a072ca50d0986d89a3534b295f1ed05f.jpg)



Figure 7. The decoding BER versus SNR for different values of N. The decoding BER is independent of tag data length N.

First, we verify the effectiveness of the CRCScatter system. In the simulation, SNR can be set to different values through its relationship with Eb/N0. Figure 7 shows the results of the decoding bit error rate of tag data versus SNR for different tag data lengths N. The SNR varies from −15 dB to −5 dB and the tag data length N is fixed as 8, 16, 24, and 32 bits. In Figure 7, we can see that the decoding BER of tag data can be reduced by increasing the SNR. Nevertheless, decoding BER is similar in terms of the tag data length N. From the figure, the system can achieve a BER level of $1 0 ^ { - 2 } \mathrm { a t } - 7 . 5 \mathrm { d B }$ , which proves the effectiveness of the CRC reverse algorithm-based decoding method in the low SNR regime. Moreover, the SNR does not affect the BER performance when the SNR is less than −13 dB. In this case, the system cannot decode correctly due to excessive noise interference.

Table 2. Comparison of two decoding methods. 

<table><tr><td>tag data length N (bit)</td><td>brute-force search Tb (s)</td><td>CRC reverse algorithm Tc (s)</td></tr><tr><td>4</td><td>0.0026</td><td>0.0104</td></tr><tr><td>6</td><td>0.0049</td><td>0.0095</td></tr><tr><td>8</td><td>0.0194</td><td>0.0103</td></tr><tr><td>10</td><td>0.0586</td><td>0.0110</td></tr><tr><td>12</td><td>0.224</td><td>0.0118</td></tr><tr><td>14</td><td>0.896</td><td>0.0099</td></tr><tr><td>16</td><td>3.529</td><td>0.0111</td></tr><tr><td>18</td><td>38.707</td><td>0.0097</td></tr></table>

Next, we test the decoding time of tag data using the brute-force search and CRC reverse algorithm. Table 2 exhibits the results of average decoding time versus different tag data lengths for the algorithms. We observe that the decoding time of brute-force search increases sharply when tag data length N increases from 4 bits to 18 bits. Due to excessive decoding time, the brute-force method is not able to meet the requirements of the real-time communication system. Nevertheless, the tag data length N does not affect the average decoding time of the CRC reverse algorithm, which is close to $1 . 0 \times 1 0 ^ { - 2 } \mathrm { s } .$ Overall, the CRC reverse algorithm is superior to the brute-force search when the tag data length is long. With the average decoding time of the CRC reverse algorithm and the maximum tag data length, we can estimate the maximum tag data rate of the system is 3.2 kbps, which is sufficient for intelligent meter reading systems, intelligent bracelets, and other micro IoT devices.

![](images/35e61204c941996c65e72af74070978bd2067ed17a4c464f76bcb506ece0876d.jpg)



(a) The decoding BER versus SNR with N = 16 bits

![](images/bbf1cd69a5a587de52c6198e0de51f728bca2bdd3c46838d9ee2e2446acff033.jpg)



(b) The decoding BER versus N with SNR = -10 dB   
Figure 8. Comparison of the decoding BER between tag data with four duplicate parity bits and tag data without check bits. Adding redundancy check bits can significantly reduce the decoding BER of the CRCScatter system.

Finally, we test the performance of using redundant bits in tag data to reduce the decoding BER. In the simulations, we use four duplicate parity bits as redundant bits for tag data. As shown in Figure 8 (a), the additional redundant bits can reduce the decoding BER when SNR is greater than −12 dB. In addition, when the SNR is higher than −7 dB, the improved method can achieve accurate decoding with tag data length N = 16 bits. With the same SNR = −10 dB, Figure 8 (b) shows that the decoding BER of tag data with redundant bits is 9% to 15% to the BER without redundant bits. We can conclude that the redundant bits can significantly reduce the system decoding error rate in the presence of noise interference. Taking advantage of the stability of CRCScatter decoding time, adding redundant check bits will not affect the efficiency of system decoding.

# 5. Discussion and conclusions

In this paper, a novel backscatter communication system called CRCScatter is proposed to enable ambient WiFi backscatter communications with a single-AP receiver. CRCScatter requires neither an extra access point at the receiver, nor applying restrictions on the excitation source. CRCScatter decoder achieves reversing the original excitation packet and decodes tag data by the received backscatter packet. The tag data can be decoded by following the procedure of CRC reverse, XOR decoding, and differential decoding. Simulation results validate the effectiveness of our proposed system.

In future work, CRCScatter will be implemented and tested in real environments, and the decoding method will be extended to QPSK or other signals such as Bluetooth and ZigBee.

# References

1. D. Feng, C. Jiang, G. Lim, L. J. Cimini, G. Feng and G. Y. Li, “A survey of energy-efficient wireless communications,” IEEE Communications Surveys and Tutorials, 2013.   
2. G. Maselli, M. Piva and J. A. Stankovic, “Adaptive Communication for Battery-Free Devices in Smart Homes,” IEEE Internet of Things Journal, 2019.   
3. S. N. Daskalakis, G. Goussetis, S. D. Assimonis, M. M. Tentzeris and A. Georgiadis, “A uW Backscatter-Morse-Leaf Sensor for Low-Power Agricultural Wireless Sensor Networks,” IEEE Sensors Journal, 2018.   
4. R. Zhao, F. Zhu, Y. Feng, S. Peng, X. Tian, H. Yu, and X. Wang, “OFDMA-enabled Wi-Fi backscatter,” in Proc. of ACM MobiCom, Los Cabos, Mexico, 21-10-2019.   
5. Y. Yang and W. Gong, “Universal Space-Time Stream Backscatter with Ambient WiFi,” in Proc. of IEEE PerCom, Pisa, Italy, 21-3-2022.   
6. Q. Wang, S. Chen, J. Zhao and W. Gong, “RapidRider: Efficient WiFi Backscatter with Uncontrolled Ambient Signals,” in Proc. of IEEE INFOCOM, Online, 10-5-2021.   
7. P. Zhang, M. Rostami, P. Hu, and D. Ganesan, “Enabling Practical Backscatter Communication for On-body Sensors.” in Proc. of ACM SIGCOMM, Florianópolis, Brazil, 22-8-2016.   
8. Y. Peng, L. Shangguan, Y. Hu, Y. Qian, X. Lin, X. Chen, D. Fang, and K. Jamieson, “PLoRa: a passive long-range data network from ambient LoRa transmissions.” in Proc. of ACM SIGCOMM, Budapest, Hungary, 20-8-2018.   
9. V. Iyer, V. Talla, B. Kellogg, S. Gollakota, and J. Smith, “Inter-Technology Backscatter: Towards Internet Connectivity for Implanted Devices.” in Proc. of ACM SIGCOMM, Florianópolis, Brazil, 22-8-2016.   
10. M. Zhang, J. Zhao, S. Chen and W. Gong, “Reliable Backscatter with Commodity BLE,” in Proc. of IEEE INFOCOM, Online, 6-7-2020.   
11. T. Kim and W. Lee, “AnyScatter: Eliminating Technology Dependency in Ambient Backscatter Systems,” in Proc. of IEEE INFOCOM, Online, 6-7-2020.   
12. B. Kellogg, A. Parks, S. Gollakota, J. R. Smith, and D. Wetherall, “Wi-fi backscatter: internet connectivity for RF-powered devices.” in Proc. of ACM SIGCOMM, Chicago, Illinois, 17-8-2014.   
13. D. Bharadia, K. R. Joshi, M. Kotaru, and S. Katti, “BackFi: High Throughput WiFi Backscatter.” in Proc. of ACM SIGCOMM, London, United Kingdom, 17-8-2015.   
14. B. Kellogg, V. Talla, J. R. Smith, and S. Gollakot, “PASSIVE WI-FI: Bringing Low Power to Wi-Fi Transmissions.” ACM SIGMOBILE, NeW York, USA, 3-8-2016.   
15. P. Zhang, D. Bharadia, K. Joshi, and S. Katti, “Hitchhike: Practical backscatter using commodity WiFi,” in Proc. of ACM SenSys, Stanford, CA, USA, 14-11-2016.   
16. P. Zhang, C. Josephson, D. Bharadia, and S. Katti, “Freerider: Backscatter communication using commodity radios,” in Proc. of ACM CoNEXT, Seoul/Incheon, South Korea, 12-12-2017.   
17. V. Talla, M. Hessar, B. Kellogg, A. Najafi, J. R. Smith, and S. Gollakota, “LoRa Backscatter: Enabling The Vision of Ubiquitous Connectivity.” in Proc. of ACM IMWUT, 2017.   
18. Stigge, M., Plötz, H., Müller, W., and Redlich, J., “Reversing CRC – Theory and Practice”, 2006.