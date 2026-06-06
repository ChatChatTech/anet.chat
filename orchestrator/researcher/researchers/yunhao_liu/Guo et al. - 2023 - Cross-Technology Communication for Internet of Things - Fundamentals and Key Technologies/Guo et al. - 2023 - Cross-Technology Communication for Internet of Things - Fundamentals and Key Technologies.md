# Cross-Technology Communication for Internet of Things

# Cross-Technology Communication for Internet of Things

Fundamentals and Key Technologies

Xiuzhen Guo

School of Software

Tsinghua University

Beijing, China

Yuan He D

School of Software

Tsinghua University

Beijing, China

Yunhao Liu

Tsinghua University

Beijing, China

ISBN 978-981-99-3718-9

ISBN 978-981-99-3719-6 (eBook)

https://doi.org/10.1007/978-981-99-3719-6

© The Editor(s) (if applicable) and The Author(s), under exclusive license to Springer Nature Singapore Pte Ltd. 2023

This work is subject to copyright. All rights are solely and exclusively licensed by the Publisher, whether the whole or part of the material is concerned, specifically the rights of translation, reprinting, reuse of illustrations, recitation, broadcasting, reproduction on microfilms or in any other physical way, and transmission or information storage and retrieval, electronic adaptation, computer software, or by similar or dissimilar methodology now known or hereafter developed.

The use of general descriptive names, registered names, trademarks, service marks, etc. in this publication does not imply, even in the absence of a specific statement, that such names are exempt from the relevant protective laws and regulations and therefore free for general use.

The publisher, the authors, and the editors are safe to assume that the advice and information in this book are believed to be true and accurate at the date of publication. Neither the publisher nor the authors or the editors give a warranty, expressed or implied, with respect to the material contained herein or for any errors or omissions that may have been made. The publisher remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

This Springer imprint is published by the registered company Springer Nature Singapore Pte Ltd.

The registered company address is: 152 Beach Road, #21-01/04 Gateway East, Singapore 189721, Singapore

# Preface

Wireless communication is the key to connecting countless devices around the world. As IoT applications widely spread, wireless technologies will get proliferated everywhere. Note that IoT applications are born to be diverse, with respect to many different factors, e.g., the deployment and operational environment, system scale, communication range, energy budget, desired network bandwidth, etc. Wireless technologies for IoT are intrinsically diverse as well. One size doesn’t fit all. Every type of wireless technology fits a certain category of applications. A number of different wireless technologies therefore coexist in the IoT era. Such wireless coexistence may lead to serious cross-technology interference (CTI) problems, e.g., channel competition, signal collision, throughput degradation. Compared with traditional methods like interference avoidance, tolerance, and concurrency mechanism, direct and timely information exchange among heterogeneous devices is therefore a fundamental requirement to ensure the usability, inter-operability, and reliability of the IoT.

Under this circumstance, Cross-Technology Communication (CTC) technique thus becomes a hot topic in both academic and industrial fields, which aims at directly exchanging data among heterogeneous devices that follow different standards. It works like a “translator” between two or more wireless technologies. CTC not only creates a new avenue for inter-operation and data exchange between wireless devices but also enhances the ability to manage wireless networks.

This book reveals that the key challenge for CTC lies in the heterogeneity of IoT devices, including the incompatibility of technical standards and the asymmetry of connection capability. Based on the above finding, this book follows a bottom-up view and involves the three most important issues: packet level CTC techniques, physical level CTC techniques, and upper layer CTC techniques. Through extensively reviewing the state of-the-art literatures, it presents the latest advances and compares these CTC techniques in terms of throughput, reliability, hardware modification, and concurrency.

# Organization of the Book

The book begins with an introductory Part I. In Chap. 1, we firstly introduce the background of heterogeneous coexistence of wireless technologies, cross technology interference, and the potential applications. Then we present the state-of-the-art approaches and the structure of the whole book.

Parts II–IV consist of the main content of this book, and are further elaborated into five chapters as follows:

Part II—Packet Level CTC Techniques

In this part, we introduce the packet level CTC techniques. First, the method of energy modulation takes the signal strength as the side channel to achieve the direct communication from WiFi to ZigBee (Chap. 2). Second, the method of channel intervention takes the channel state information as the side channel to achieve the direct communication from ZigBee to WiFi (Chap. 3).

Part III—Physical Level CTC Techniques

In this part, we describe the physical level CTC techniques. First, the method of cross-demapping leverages the distinguishable features to improve the CTC rate from ZigBee to WiFi (Chap. 4). Second, the method of digital emulation emulates the phase shifts associated with the desired signals to maximize the packet reception radio of CTC (Chap. 5).

Part IV—Upper Layer CTC Techniques

In this part, we present the upper layer protocols based on the CTC technique. Specifically, in Chap. 6, we design a bidirectional coordination scheme in which resource-constrained wireless devices such as ZigBee nodes and powerful WiFi appliances coordinate their activities to increase coexistence and enhance network performance.

The book ends with a summative Part V. Chapter 7 first concludes the book and further discusses the future directions on CTC techniques.

# Anticipated Audience

The book considers the state-of-the-art research results in many academic journals and conferences during its preparation. Thus, readers can track trends and hot topics in the field. With the detailed introduced techniques for CTC techniques, it would draw attention of scientists and researchers, who are interested in the research areas of wireless networking, wireless communication, mobile computing, and Internet of Things. The provided techniques would also systematically contribute to the practical applications and well guide the readers. Thus, it can serve as a guide book for the technicians and practitioners in the industry. Moreover, we wish this book can genuinely benefit all levels of readers.

The findings and summaries of this book are potentially significant in the following directions: (1) to guide subsequent researchers to rethink the CTC techniques regarding the design methodology; (2) to further innovate the infrastructure of future IoT by introducing CTC; (3) to enable important IoT application by enabling ubiquitous network connectivity.

Should the readers have any questions or suggestions, please contact the authors by email via guoxiuzhen94@gmail.com.

Beijing, China

March 2023

Xiuzhen Guo

Yuan He

Yunhao Liu

# Acknowledgments

During almost 10 years working on the topic of cross-technology communication, we have benefited a great lot from many professors, colleagues, and friends. We wish to take this opportunity to thank them.

Many former and present students have contributed greatly to the book. We thank them for their contributions to the original research content covered by multiple chapters. In particular, we are most grateful to Dr. Zihao Yu, Dr. Weiguo Wang, Dr. Jia Zhang, and Dr. Xin Na at Tsinghua University, Haotian Jiang at Mihoyo, and Dr. Liangcheng Yu at the University of Pennsylvania. They have done great works.

We are grateful to many professors and peer researchers who shared exciting information with us. We thank Prof. Kang G. Shin, Prof. Tian He, Prof. Qian Zhang, Prof. Falko Dressler, Prof. Joshua R. Smith, and Prof. Yuguang Fang. Especially, sincere thanks to Prof. Xiaolong Zheng at Beijing University of Posts and Telecommunications for his kind comments and advices. Thanks are also due to Prof. Longfei Shangguan at the University of Pittsburgh, who provided helpful suggestions on our research works.

We wish to express our gratitude to many colleagues, who worked closely with us and inspired us a lot on research: thanks to Dr. Meng Jin, Dr. Rui Xi, Dr. Songzhou Yang, Dr. Yimiao Sun, Dr. Yande Chen, Shuai Li, Jiacheng Zhang, Yulong Chen, etc.

Last but by no means least, we thanks our family for their encouragement and support. We affectionately dedicate this book to them.

This book is supported in part by the National Natural Science Foundation of China (NSFC) under grants No. U21B2007 and No. 62202264, China Postdoctoral Science Foundation No. 2021M701888 and No. 2022T150354.

Beijing, China

March 2023

Xiuzhen Guo

Yuan He

Yunhao Liu

# Contents

# Part I Getting Started

# 1 Introduction 3

1.1 Background and Motivation 3

1.1.1 Heterogeneous Devices Coexistence 3   
1.1.2 Cross Technology Interference . 4

1.2 Cross Technology Communication (CTC). 5

1.3 Applications . 6

1.3.1 Avoiding Cross-Technology Interference. 6   
1.3.2 Improving IoT Network Efficiency 7   
1.3.3 Working with Backscatter Networking 7   
1.3.4 Clock Synchronization 8   
1.3.5 Cross Technology Attack . 8

1.4 State-of-the-Art Approaches. 9

1.4.1 Packet Level CTCs 9   
1.4.2 Physical Level CTCs 12   
1.4.3 Overall Comparison of These CTC Works . 14

1.5 Book Organization 15

References 16

# Part II Packet Level CTCs

# 2 Packet Level CTC Based on Energy Modulation. 21

2.1 Introduction 21   
2.2 Related Work . 23   
2.3 Preliminary Study . 24

2.3.1 The Feasibility of Energy Communication 24   
2.3.2 Space of Energy Coding . 27

2.4 Overview 29   
2.5 Theoretical Analysis 30   
2.6 Modulation and Demodulation 34

2.6.1 Amplitude Modulation 34

2.6.2 Temporal Modulation. 35   
2.6.3 Online Rate Adaptation. 36

2.7 Evaluation 39

2.7.1 Evaluation Settings 39

2.7.2 Throughput and SER 40

2.7.3 Online Rate Adaptation. 41

2.7.4 SER Model Robustness. 43

2.7.5 Implementation on Commercial Devices 46

2.7.6 WiZig Performance Under Mobility 47

2.7.7 WiZig Vs. Freebee . 48

2.8 Discussion 50

2.9 Conclusion 51

References . 52

# 3 Packet Level CTC Based on Channel Intervention 53

3.1 Introduction 53

3.2 Related Work . 55

3.3 Observations. . 56

3.3.1 Infeasibility of ZigBee to WiFi CTC Using RSSI. 56

3.3.2 Feasibility of ZigBee to WiFi CTC Using CSI . 56

3.4 ZigFi Design 62

3.4.1 Overview 62

3.4.2 The Features Extracted Within a Decoding Window 63

3.4.3 The Window Length of the SVM Classifier . 64

3.4.4 Training the SVM Classifier 65

3.4.5 The Relationship Between the Accuracy and the SINR 65

3.4.6 The Receiver-Initiated Mechanism 66

3.4.7 The Justification of the ZigFi Overhead 68

3.4.8 Extension to Multiple-to-One Concurrent Transmissions . . . . 70

3.5 Evaluation 72

3.5.1 Implementation 72

3.5.2 Overall Performance Comparison 73

3.5.3 Performance Under Different Settings . 75

3.5.4 The Impact on Existing WiFi Communication 79

3.5.5 ZigFi Performance Under Concurrent Transmissions 80

3.6 Discussion . 81

3.7 Conclusion 83

References . 83

# Part III Physical Level CTCs

# 4 Physical Level CTC Based on Cross Demapping . 87

4.1 Introduction 87

4.2 Related Works . 90

4.3 Background and Motivation 92

4.3.1 Background 92

4.3.2 The Mismatch in Bandwidth 93   
4.3.3 Incompatibility of Modulations 96   
4.3.4 Failure in Symbol Synchronization 96

# 4.4 Design 97

4.4.1 Overview 97   
4.4.2 ZigBee Preamble Detection 98   
4.4.3 ZigBee Data Decoding 101   
4.4.4 CTC from Bluetooth to WiFi. 104   
4.4.5 Discussion . 106

# 4.5 Evaluation 107

4.5.1 Experiment Setup 107   
4.5.2 Benchmarks 109   
4.5.3 Overall Performance Comparison 111   
4.5.4 Performance Under Different Settings . 113   
4.5.5 Performance of LEGO-Fi when Receiving Bluetooth Signals . 119

# 4.6 Conclusion 120

# References 120

# 5 Physical Level CTC Based on Digital Emulation . 123

5.1 Introduction 123   
5.2 Related Works . 125   
5.3 Analog Emulation Vs. Digital Emulation. 127

5.3.1 Analog Emulation 127   
5.3.2 Digital Emulation . 129

# 5.4 Design 131

5.4.1 Overview 132   
5.4.2 Phase Sequence Generation 133   
5.4.3 Phase Sequence Optimization 137   
5.4.4 Parallel Communication 140   
5.4.5 Discussions. 141

# 5.5 Evaluation 142

5.5.1 Experiment Setup 142   
5.5.2 Emulated Phase Sequence . 143   
5.5.3 Overall Performance Comparison 143   
5.5.4 WIDE Performance with Different Optimization Methods . . . 145   
5.5.5 WIDE Performance Under Different Settings . 146   
5.5.6 Evaluation on the Commercial ZigBee Device. 149   
5.5.7 Parallel Communication . 150

# 5.6 Conclusion 150

# References 151

# Part IV Upper Layer CTCs

# 6 BiCord: Bidirectional Coordination Among Coexisting

# Wireless Devices . 155

6.1 Introduction 155   
6.2 Related Works . 158   
6.3 Motivation . 159

6.3.1 The Need for Bidirectional Coordination. 159   
6.3.2 The Challenges of Bidirectional Coordination 160

6.4 BiCord: Design Overview 162   
6.5 Cross-Technology Signaling. 162   
6.6 Adaptive White Space Allocation 164   
6.7 Implementation Details 166

6.7.1 CTI Detection 166   
6.7.2 Energy Cost of BiCord on ZigBee Nodes 167   
6.7.3 Impact of BiCord on Wi-Fi Operations . 168   
6.7.4 Extension to Other Coexistence Scenarios 168

6.8 Evaluation 168

6.8.1 Experimental Setup 169   
6.8.2 Performance of Cross-Technology Signaling 169   
6.8.3 Performance of Adaptive White Space Allocation . 170   
6.8.4 Comparison with ECC. 172   
6.8.5 Impact of Different BiCord’s Parameters . 173   
6.8.6 Performance in Mobile Scenarios . 174   
6.8.7 Prioritization of Wi-Fi Traffic 175

6.9 Conclusions 176

References 176

# Part V Conclusions

# 7 Research Summary and Future Directions 181

7.1 Research Summary. 181   
7.2 Future Directions . 181

7.2.1 Cross-Network Systems 182   
7.2.2 Cross-Frequency Systems 182   
7.2.3 Cross-Media Systems. 182

References 182

# Acronyms

BER Bit Error Rate

BLE Bluetooth Low Energy

CP Cyclic Prefix

CSI Channel State Information

CSMA Carrier Sense Multiple Access

CTC Cross Technology Communication

DTW Dynamic Time Wrapping

FFT Fast Fourier Transform

IoT Internet of Things

LoRa Long Range

LPWAN Low-Power Wide-Area Network

MAC Medium Access Control

OFDM Orthogonal Frequency Division Multiplexing

OOK ON–OFF Keying

PRR Packet Reception Ratio

QAM Quadrature Amplitude Modulation

RFID Radio Frequency Identification

RSSI Received Signal Strength Indicator

SER Symbol Error Rate

SNR Signal to Noise Ratio

TDMA Time Division Multiple Access

USRP Universal Software Radio Peripheral

WiFi Wireless Fidelity