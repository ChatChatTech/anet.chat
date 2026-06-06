# SmokeGrenade: A Key Generation Protocol with Artificial Interference in Wireless Networks

Dajiang Chen $^{*}$ , Xufei Mao $^{\dagger}$ , Zhen Qin $^{*}$ , Zhiguang Qin $^{*}$ , Panlong Yang $^{\ddagger}$ and Yunhao Liu $^{\dagger}$

\* School of Computer Science and Engineering, University of Electronic Science and Technology of China

$^{\dagger}$ School of Software and TNLIST, Tsinghua University, China

$^{\ddagger}$ Institute of Communication Engineering, PLA University of Science and Technology, Nanjing, China

Email: {dajiangchen2010, panlongyang}@gmail.com, {xufei, yunhao}@greenorbs.com, {qinzhen, qinzg}@uestc.edu.cn

Abstract—Leveraging a wireless multi-path channel as a source of common randomness, a number of key generation methods have been proposed according to information-theory security. However, by taking the advantages of node's mobility, existing schemes usually have low generation rate or low entropy. To overcome this limitation, we present a key generation protocol with known Artificial Interference, named SmokeGrenade, a new physical-layer approach for secret key generations in a narrowband fading channel. Our scheme utilizes artificial interference to contribute to the change of the measured values on channel states. The theoretical analysis shows that the key generation rate rises with the increment of the interference power. Particularly, the achievable key rate of SmokeGrenade achieves at least four times better than that of traditional key generation schemes when the average interference power is normalized to 1. Simulation results also show that SmokeGrenade has a higher generation rate and entropy compared with some known state-of-the-art approaches.

Index Terms—Secret key generation, Artificial interference, Physical layer security, Wireless security.

# I. INTRODUCTION

Along with the proliferation of wireless devices over the past several decades, wireless security have attracted much attention in the society since wireless communication is prone to be attacked, (e.g., eavesdropping, message modification, and node impersonation) due to the broadcast nature of wireless channels. It is well known that secret keys must be established between authorized parties before communication in order to protect the confidentiality, integrity, and authenticity of the information. Unfortunately, wireless devices are usually powered by batteries and have constrained computer ability such that the traditional cryptography methods with high computational complexity (e.g., Diffie-Hellman key exchange scheme [4]) relying on computational hardness of problems, hence face a number of challenges.

Basically, existing practical systems mainly suffer from the following major limitations, including: 1) A low key generation rate since the existing physical-layer-based (PHY-based) key generation schemes depends on channel variation and cannot generate new secret bits unless the channel changes. For instance, the state-of-the-art highest achieved secrecy rate is only 40 bits per second [14]. In addition, achieving this rate requires node mobility and leads to $4\%$ disagreement bit rate between communication nodes as well; 2) Vulnerable to predictable channel attacks since the channel change in coherence time is great slowly and the entropy of key bits is low; and 3) Performing badly in stationary scenarios due to infrequent and small scale variations in the channel measurements. According to the analysis in [13], in static scenarios, the extracted key bits have a very low entropy which makes these bits unsuitable for a secret key. In addition, the key generation may be modeled and predicted by an eavesdropper in static environments. Furthermore, as we shown in Section IV, if there exist jamming signals while the keying nodes send probes to each other for channel measurement, the key generation rate degrades rapidly.

In this work, we are aiming to address the security key generation problem in the following scenario: one node (saying Alice) wants to establish a symmetrical key with another node (saying Carol) with a help node (named Bob) in the presence of an eavesdropper (saying Eve). In addition, there is a secure channel shared between the helper and one of the keying nodes (Alice or Carol). We present a new physical layer approach, named SmokeGrenade, for secret key generation in narrowband fading channel and static environments. Our approach utilizes artificial interference (or jamming) to contribute to the changes of channel states, and thus works properly even if the environment is static. The basic idea underlying SmokeGrenade is as follows. When the sender (Alice) sends probes to the receiver (Carol), the helper (Bob) broadcasts artificial interference to change the measurement value of channel states. To achieve this, there are two technical problems need to be formally addressed.

How to ensure the correlation of information between Alice and Carol. SmokeGrenade addresses this problem using a secure channel, i.e., Bob sends the interference signals to Alice over a secure channel in order to maintain the correlation between Alice and Carol. In addition, by using this secure channel, the helper can send other useful messages (e.g., the channel state information between the helper and the keying nodes) to Alice. The gain brought by this secure channel will be described in Section V.

How to ensure the eavesdropper can not obtain any information about the channel measurement between Alice and Carol. Since if Bob only transmits time-varying jamming signals, Eve can estimate those signals (refer to the proof of

![](images/bc03a2151bb8eb73b4024fd1364db0dec609e75950a2bfee75981d10a56373da.jpg)



![](images/5a0b4166008309d3f94f6d4621c6f96bb0e9ce38492012e22cf745db3c84ec25.jpg)



Fig. 1. (a) General model with interference; (b) Our system model with Known-interference.

Theorem 2). Due to the fact that the secret key rate can be upper bounded by the conditional mutual information between the observations of two keying nodes under the observations of Eve [5], the change of channel states cannot bring the improvement of key rate. We addresses this issue by changing the transmitted signals at both Alice and Bob. Basically, we illustrate that Eve can not obtain any useful information in Section V-B.

We summarize our main contributions as follows:

- For the known-interference model, we present SmokeGrenade with a theoretically achievable key generation rate. Particularly, the theoretical achievable key rate of SmokeGrenade makes at least four times better than the traditional key generation schemes when the average interference power is normalized to 1.   
- To the best of our knowledge, this is the first work that rigorously analyzes how interfere power impacts the performance of a key generation protocol, and how secret key is generated by using the interference which contributes to the changes of channel states.   
- For general key generation model with unknown interference, we find that the key generation rate degrades rapidly when the interference power increases, and the key rate converges at zero when the interference power goes to infinite.

The rest of the paper is organized as follows. In Section II, we place our work in the context of related research in secret key extraction. Section III lays out the system model and adversary model used in this paper. In Section IV, we describe the impact of Interference on the general key generation model. Details of SmokeGrenade with complete analysis of its performance is presented in Section V. Section VI details the simulation studies. We conclude our work in Section VII.

# II. RELATED WORK

There are many active research related to PHY-based secret key generation over the past several decades. Actually, the related work can be traced back to Shannon's work on information-theoretical formulation of secure communication [2] and Wyner's work on wiretap channel model [3]. Later, following [2] and [3], a large number of theoretical results that characterize secrecy capacity appear, like work in [5], [6], [8] However, they only aimed at deriving theoretical limits and did not provide practical key generation algorithms in wireless networks due to the characteristics of non-reachability of random coding. Based on aforementioned theoretical results, recently, several radio channel features have been proposed for key extraction in wireless networks [11]–[13] Unfortunately, they suffered from some problems such as a low key generation rate, a low entropy of key bits and a high reliance on nodes mobility as well. To overcome these issues, there are several solutions which have been proposed. For example, Zeng et al. [15], proposed a key generation protocol by exploiting multi-antenna diversity with the cost of sacrificing low complexity of transceivers. In [16], Gollakota et al. introduced iJam, a channel-independent PHY-based technique to improve the rate of channel changes. However, the security of the system cannot be guaranteed when facing more powerful adversary (e.g., when an adversary has two directional antennas).

Recently, cooperative jamming has recently been proposed for improving PHY-based security for wireless networks in the presence of an eavesdropper. In $[21]$ , a trusted third party jams the message signal from senders to receivers such that the latter decode the distortion information by canceling the known jamming signal while an eavesdropper cannot achieve this due to unknown jamming signal. A variation on the above model was presented in $[22]$ and $[23]$ . Their main idea is to let the sender itself transmit the key combined with a jamming signal and a third party node transmit an anti-jamming signal which cancels out the jamming signal at the receiver but not at the adversary. All in all, the purpose of cooperative jamming is to increase the interference at the adversary (i.e., regarding interference as noise) and to eliminate the jamming signal at legitimate user such that the main channel (i.e., the channel between a sender and a receiver) has less noise than the wiretap channel (i.e., the channel between a sender and an eavesdropper). In this paper, we mainly work on the performance and information theoretic limits of key extraction by using interference (or say jamming). Instead of making noise (artificial interference) simply, we utilize jamming to contribute to the changes of channel states as well.

# III. MODELS AND PRELIMINARIES

Notions: Let $T_{c}$ be the coherence time, $f_{c}$ be the coherence frequency, $f_{s}$ be the sampling rate and M be the samples by fully exploiting the coherence time interval at A and B. RVs are denoted by upper case letters (e.g., X, Y, Z, $\cdots$ ), random vector are indicated by bold face upper case letters (e.g., X, Y, Z, $\cdots$ ). A list of important notations used is shown in Tab. I

# A. System Model

We assume that two keying nodes, Alice and Carol, who plan to extract a symmetrical key for secure communication, an eavesdropper (saying Eve), who is able to observe the error-correcting information tries to break the secret key, and a node Bob, who is capable of broadcasting jamming signal to change the measured value of channel state between Alice and Carol. Under general PHY-based key generation model with interference (Fig. 1(a)), keying nodes know nothing about the jamming signal transmitted by any neighbor node or malicious node. In other words, there is no secure channel among Bob and Alice (resp. Carol) such that there is no way for Bob to send any message to one of the keying nodes, which is unknown to Eve. In this work, we focus on known-interference model (refer to Fig. 1(b)), following which there is a secure channel between Bob and Alice only, i.e., Bob can send some useful messages (e.g., the jamming signal, the channel states information between the helper and the keying nodes) to Alice privately (unknown to Eve). In this paper, we assume that the helper node Bob is a trusted third party.

TABLE I
A SUMMARY OF IMPORTANT NOTATIONS. 

<table><tr><td>Symbol</td><td>Definition</td></tr><tr><td> $X,Y,\cdots$ </td><td>random variables (RVs)</td></tr><tr><td> $\mathbb{X},\mathbb{Y},\cdots$ </td><td>random vector</td></tr><tr><td> $\mathbb{X}^{T}$ </td><td>the transpose of vector  $\mathbb{X}$ </td></tr><tr><td> $\| \mathbb{X} \|^{2}$ </td><td> $\mathbb{X}\mathbb{X}^{T}$ </td></tr><tr><td> $T_{c}$ </td><td>coherence time</td></tr><tr><td> $M$ </td><td>the number of samples in  $T_{c}$  at A and B</td></tr><tr><td> $f_{s}$ </td><td>sampling rate</td></tr><tr><td> $H_{ij}$ </td><td>channel gains between node  $i$  and  $j$ </td></tr><tr><td> $\mathcal{N}(\mu,\sigma^{2})$ </td><td>the Gaussian RV with mean  $\mu$  and variance  $\sigma^{2}$ </td></tr><tr><td> $N_{i}$ </td><td>the Gaussian noise obey  $\mathcal{N}(0,1)$ </td></tr><tr><td> $\sigma_{i,j}$ </td><td>the variance of the variable  $H_{ij}$ </td></tr><tr><td> $S_{i}$ </td><td>the signal transmitted by node  $i$ </td></tr><tr><td> $\mathcal{E}(X)$ </td><td>the mean of RV  $X$ </td></tr><tr><td> $P$ </td><td>mean power of keying nodes A and C</td></tr><tr><td> $P_{B}$ </td><td>mean power of helper B</td></tr><tr><td> $\Lambda$ </td><td>Gaussian RV with mean 0 and variance  $a^{2}$ </td></tr><tr><td> $R_{I}$ </td><td>maximum key rate of general model with jamming</td></tr><tr><td> $R^{SG}$ </td><td>maximum key rate of SmokeGrenade</td></tr></table>

# B. Channel Model

We consider the standard narrowband fading, wireless interference channel model in this work (actually, our solution can be extended to the wideband scenario with a slight modification). To be precisely, we consider a channel from node i to node j as a multi-path fading model with channel impulse $H_{ij}$ . Here, the delay spread v of the multi-path channel is small enough such that the multi-path components are typically non-resolvable according to the definition of narrowband fading model. Hence, if node i transmits a signal $S_{i}$ to node j along with a jamming signal $S_{k}$ sent by node k, the signal outputs at j is given by $Y_{j} = H_{ij}S_{i} + H_{kj}S_{k} + N_{j}$ where $N_{j}$ is the noise component. Following the work in [17], we assume that channel is reciprocal in both forward and reverse directions during the coherence time such that $H_{ij} = H_{ji}$ and the underlying noise in each channel is additive white Gaussian noise. All nodes are assumed to possess a common time reference, which can be obtained using GPS. We also assume that each node is half-duplex and possesses a single isotropic antenna.

# C. Adversary Model

Following the well-known assumptions in most key generation schemes based on physical layer approaches (e.g., work in [11]–[13]), we assume that the adversary Eve is able to listen to communications in the network and measure the channels between itself and communicating nodes. In addition, Eve is powerful enough to know the whole key generation protocol and the values of the parameters used in the protocol. During the key reconciliation process, the adversary Eve is able to observe the error-correcting information, which helps him to break the secret key. We assume that Eve always keep at least half of the wavelength of radios waves away from any one of nodes from Alice, Bob and Carol. This is reasonable since for most radios on 2.4GHz, half of the wavelength of which is usually several centimeters only [12]. We further assume that Eve does not try to prevent Alice and Carol from building the secret keys or modify any message exchanged by Alice and Carol in order to avoid being detected. In addition, the man-in-the-middle attack is not considered in this work, i.e., our methodology does not aim to authenticate Alice or Carol.

# IV. THE IMPACT OF INTERFERENCE ON THE KEY GENERATION PROTOCOL

In this section, we rigorously show the impact of interference on traditional key generation Protocols. We still take the case (shown in Fig. 1(a)) as the example. In this case, two legitimate nodes (Alice and Carol) plan to extract a symmetrical key in the presence of an eavesdropper Eve. There is some other node Bob (not necessarily a helper node in this case) who may be an adversary or a neighbor node, and generates an interference signal during the channel sensing process. In this scenario, we assume that Alice and Carol know nothing about the jamming signal. We first give the theoretical performance analysis of how the interfere power impact on the performance of a key generation protocol.

To simplify the analysis, we only consider the coherence time period, i.e., $[0,T_{c}]$ out of entire channel sensing time. If we use M to denote the number of samples in the coherence time at time A and time B and $f_{s}$ is the sampling rate, clearly we have $M=\left\lfloor\frac{1}{2}T_{c}f_{s}\right\rfloor$ . Then, the traditional key extracting schemes with interference can be described as follows. In this work, we consider that time has been divided into slots, during each of which a probing signal could be launched.

Step (1) In time slot $t_{1}$ , Alice transmits a known probe signal $S_{A}(t_{1})$ to Carol, and Bob generates an interference signal $S_{B}(t_{1})$ at the same time. Hence, the signals received by Carol and Eve in time slot $t_{1}$ can be computed as:

$$
Y _ {A B \rightarrow C} (t _ {1}) = H _ {A C} S _ {A} (t _ {1}) + H _ {B C} S _ {B} (t _ {1}) + N _ {C} (t _ {1})
$$

$$
Y _ {A B \rightarrow E} (t _ {1}) = H _ {A E} S _ {A} (t _ {1}) + H _ {B E} S _ {B} (t _ {1}) + N _ {E} (t _ {1})
$$

where $N_{C}$ and $N_{E}$ are noises at Carol and Eve, respectively.

Step (2) In time slot $t_{2}$ , Carol transmits the known probe signal $S_{C}(t_{2})$ to Alice, and the interference signal from Bob is $S_{B}(t_{2})$ . Then the signals received by Alice and Eve are:

$$
Y _ {B C \rightarrow A} (t _ {2}) = H _ {C A} S _ {C} (t _ {2}) + H _ {B A} S _ {B} (t _ {2}) + N _ {A} (t _ {2})
$$

$$
Y _ {B C \rightarrow E} (t _ {2}) = H _ {C E} S _ {C} (t _ {2}) + H _ {B E} S _ {B} (t _ {2}) + N _ {E} (t _ {2})
$$

where $N_{A}$ and $N_{E}$ are noises at Alice and Eve, respectively.

Step (3) Repeat Step (1) and Step (2) for M times for 2M time slots totally. Then all of the signals received by Alice

and Carol can be written as:

$$
\mathbb {Y} _ {B C \rightarrow A} = H _ {C A} \mathbb {S} _ {C} + H _ {B A} \mathbb {S} _ {B 2} + \mathbb {N} _ {A}
$$

$$
\mathbb {Y} _ {A B \to C} = H _ {A C} \mathbb {S} _ {A} + H _ {B C} \mathbb {S} _ {B 1} + \mathbb {N} _ {C}
$$

Moreover, all signals received by Eve can be written as:

$$
\mathbb {Y} _ {B C \to E} = H _ {C E} \mathbb {S} _ {C} + H _ {B E} \mathbb {S} _ {B 2} + \mathbb {N} _ {E}
$$

$$
\mathbb {Y} _ {A B \rightarrow E} = H _ {A E} \mathbb {S} _ {A} + H _ {B E} \mathbb {S} _ {B 1} + \mathbb {N} _ {E}
$$

Here $\mathbb{N}_A$ , $\mathbb{N}_C$ and $\mathbb{N}_E$ are drawn independent and identically distributed (i.i.d.) according to distribution $\mathcal{N}(0,\sigma_0)$ , $\mathbb{Y}_{BC\to A} = \{Y_{BC\to A}(t_{2m-1})\}_{m=1}^M$ , $\mathbb{Y}_{AB\to C} = \{Y_{AB\to C}(t_{2m})\}_{m=1}^M$ and all the probing vectors used are

$$
\left\{ \begin{array}{l l} \mathbb {S} _ {A} & = (S _ {A} (t _ {1}), S _ {A} (t _ {3}), \dots , S _ {A} (t _ {2 M - 1})) \\ \mathbb {S} _ {C} & = (S _ {C} (t _ {2}), S _ {C} (t _ {4}), \dots , S _ {C} (t _ {2 M})) \\ \mathbb {S} _ {B 1} & = (S _ {B} (t _ {1}), S _ {B} (t _ {3}), \dots , S _ {B} (t _ {2 M - 1})) \\ \mathbb {S} _ {B 2} & = (S _ {B} (t _ {2}), S _ {B} (t _ {4}), \dots , S _ {B} (t _ {2 M})) \end{array} \right.
$$

Step (4) Alice and Carol compute their channel measurements as follows.

$$
\mathbb {Y} _ {B C \rightarrow A} \frac {\mathbb {S} _ {C} ^ {T}}{\| \mathbb {S} _ {C} \| ^ {2}} = H _ {A C} + H _ {A B} \frac {\mathbb {S} _ {B 2} \mathbb {S} _ {C} ^ {T}}{\| \mathbb {S} _ {C} \| ^ {2}} + \frac {\mathbb {N} _ {A} \mathbb {S} _ {C} ^ {T}}{\| \mathbb {S} _ {C} \| ^ {2}} \tag {1}
$$

$$
\mathbb {Y} _ {A B \rightarrow C} \frac {\mathbb {S} _ {A} ^ {T}}{\| \mathbb {S} _ {A} \| ^ {2}} = H _ {A C} + H _ {B C} \frac {\mathbb {S} _ {B 1} \mathbb {S} _ {A} ^ {T}}{\| \mathbb {S} _ {A} \| ^ {2}} + \frac {\mathbb {N} _ {C} \mathbb {S} _ {A} ^ {T}}{\| \mathbb {S} _ {A} \| ^ {2}} \tag {2}
$$

For simplicity, we use $\hat{Y}_A$ (resp. $\hat{Y}_C$ ) to denote $\mathbb{Y}_{BC\to A}\frac{\mathbb{S}_C^T}{\|\mathbb{S}_C\|^2}$ (resp. $\mathbb{Y}_{AB\to C}\frac{\mathbb{S}_A^T}{\|\mathbb{S}_A\|^2}$ ).

In general, the terms in the equations above are complex RVs. For simplicity, we take them as real numbers by assuming that only the in-phase component of communication is utilized [9]. Thus, in this paper, we take the variances of $H_{AB}$ , $H_{AC}$ and $H_{BC}$ as $\sigma_{AB}^{2}$ , $\sigma_{AC}^{2}$ and $\sigma_{BC}^{2}$ , respectively. We have $H_{AB} \sim \mathcal{N}(0, \sigma_{AB}^{2})$ , $H_{AC} \sim \mathcal{N}(0, \sigma_{AC}^{2})$ and $H_{BC} \sim \mathcal{N}(0, \sigma_{BC}^{2})$ , i.e., fading coefficients are zero-mean real Gaussian RVs.

# A. Theoretical Analysis

For mathematical simplicity, we take $\mathbb{S}_{B1} = \eta \mathbb{S}_A$ and $\mathbb{S}_{B2} = \eta \mathbb{S}_C$ for some real number $\eta$ random selected by Bob, and let $\| \mathbb{S}_A \| = \| \mathbb{S}_C \|$ . Then Eq. 1 and Eq. 2 can be rewritten as $\hat{Y}_A = H_{AC} + \eta H_{AB} + \frac{\mathbb{N}_A\mathbb{S}_C^T}{\|\mathbb{S}_C\|^2}$ and $\hat{Y}_C = H_{AC} + \eta H_{BC} + \frac{\mathbb{N}_C\mathbb{S}_A^T}{\|\mathbb{S}_A\|^2}$ respectively.

We denote the average transmission power constraints by $P = \frac{1}{M} \| \mathbb{S}_A \|^2 = \frac{1}{M} \| \mathbb{S}_C \|^2$ and $P_B = \frac{1}{2M} (\| \mathbb{S}_{B1} \|^2 + \| \mathbb{S}_{B2} \|^2)$ (It is clear $\eta = \frac{P_B}{P}$ ). In order to simplify the expression, from now on, we let $\sigma_{\triangle A}^2 = \frac{P_B}{P}\sigma_{AB}^2 + \frac{1}{MP}\sigma_0^2$ , $\sigma_{\triangle C}^2 = \frac{P_B}{P}\sigma_{BC}^2 + \frac{1}{MP}\sigma_0^2$ and $\tilde{\sigma}^2 = \frac{\sigma_{\triangle A}^2(\sigma_{AC}^2 + \sigma_{\triangle C}^2) + \sigma_{AC}^2\sigma_{\triangle C}^2}{\sigma_{AC}^2 + \sigma_{\triangle C}^2}$ .

Now, we introduce a lemma on conditional density function.

Lemma 1: Let X, Y, Z be the pairwise independent Gaussian RVs with zero mean and variance $\sigma_{X}^{2}$ , $\sigma_{Y}^{2}$ and $\sigma_{Z}^{2}$ . We assume $\Gamma_{1}=X+aY$ and $\Gamma_{2}=X+bZ$ , here a and b could be any real number. Then the conditional density $f(\Gamma_1 \mid \Gamma_2 = \gamma_2)$ is Gaussian with mean $\tilde{\mu} = \frac{\sigma_X^2\gamma_2}{\sigma_X^2 + b^2\sigma_Z^2}$ and variance $\tilde{\sigma}^2 = \frac{a^2\sigma_Y^2(\sigma_X^2 + b^2\sigma_Z^2) + b^2\sigma_X^2\sigma_Z^2}{\sigma_X^2 + b^2\sigma_Z^2}$ .

Proof: Please refer to the tech-report [1] for details.

![](images/ffe03ae262af1622297b6ea35196abc9cc0c22aa229280d32c6ed3b39bdcd2d9.jpg)

Based on the measured value $(\hat{Y}_{A}, \hat{Y}_{C})$ at Alice and Carol, we have the following theorem.

Theorem 1: The theoretical maximum key rate $R_{I}$ of traditional key generation protocol with interference is

$$
R _ {I} = \frac {1}{T _ {c}} I (\hat {Y} _ {A}, \hat {Y} _ {C}) = \frac {1}{2 T _ {c}} \ln \frac {\sigma_ {A C} ^ {2} + \sigma_ {\triangle A} ^ {2}}{\tilde {\sigma} ^ {2}} \tag {3}
$$

If $P_B = 0$ , then $R_I$ is equal to the maximum key rate of general model [18]. Moreover, if $P_B \to \infty$ , then $R_I \to 0$ .

Proof: Please refer to the tech-report [1] for details.

![](images/19cb2159c21f4b4bc744f0d285d744420321b8cad047d51991b5914e97eb281c.jpg)

As an example, for the parameters $T_{c} = 15ms$ , $M = 10^{4}$ , $\delta_{AB} = \delta_{AC} = \delta_{BC} = \delta_{0} = 1$ , Fig. 2 plots the maximum key rate $R_{I}$ when the interference power $P_{B}$ increases. This figure shows that the rate of change of $R_{I}$ over the interval [0, 0.5] is very fast. Hence, it is not hard to see that a slight interference does have a huge impact on the key generation rate.

![](images/6f466f5557901a3142b513e6e13cb3f7f9246ca5355b9e89cef647f56067f389.jpg)



Fig. 2. Maximum key rate $R_{I}$ versus the interference powers $P_{B}$ under different power P at keying nodes A and C.

Actually, Theorem 1 provides a theoretical basis for how the performance of secret key generation rate relates to the interference power. Specifically, when the interference power $P_{B}$ increases, the mutual information $I(\hat{Y}_{A},\hat{Y}_{C})$ decrease, hence the key generation rate is reduced. Moreover, no secret key can be extracted when $\hat{Y}_{A}$ and $\hat{Y}_{C}$ are independent and $P_{B}$ goes to infinite, In summary, we draw the following conclusion that (1) the key rate is reduced rapidly when the interference power $P_{B}$ increases; (2) the key rate converges at zero when $P_{B}$ goes to infinite due to the fact that interference is asymmetric for the keying nodes Alice and Carol.

# V. SMOKEGRENADE KEY GENERATION PROTOCOL

In this section, we propose our key generation protocol named SmokeGrenade based on known-interference model (see Fig. 1(b) for illustration).

# A. The architecture of SmokeGrenade

Basically, SmokeGrenade consists of the following stages.

1) Collecting the Channel Information: We divide coherence time $T_{c}$ into 4M parts $t_{1}, t_{2}, \cdots, t_{2-1}, t_{4M}$ , where $M = \frac{1}{4} f_{s} T_{c}$ . Let $\Lambda$ be a Gaussian RV with mean 0 and variance $a^{2}$ . For simplify, we take $\mathbb{S} = (1, \cdots, 1)$ .

Step (1) In $t_{1}$ , Alice broadcasts known probe signal $S(1)$ to Bob and Carol. The signals received by Carol and Eve are:

$$
Y _ {A \rightarrow C} (t _ {1}) = H _ {A C} S (1) + N _ {A} (t _ {1})
$$

$$
Y _ {A \rightarrow E} (t _ {1}) = H _ {A E} S (1) + N _ {E} (t _ {1})
$$

Step (2) In $t_{2}$ , Bob broadcasts known probe signal $S(1)$ to Alice and Carol. The signals received by Carol and Eve are:

$$
Y _ {B \rightarrow C} (t _ {2}) = H _ {B C} S (1) + N _ {B} (t _ {2})
$$

$$
Y _ {B \rightarrow E} (t _ {2}) = H _ {B E} S (1) + N _ {E} (t _ {2})
$$

Step (3) In $t_3$ , Carol broadcasts known probe signal $S(1)$ to Alice and Bob. The signals received by Alice, Bob and Eve are:

$$
Y _ {C \rightarrow A} (t _ {3}) = H _ {A C} S (1) + N _ {A} (t _ {3})
$$

$$
Y _ {C \rightarrow B} (t _ {3}) = H _ {B C} S (1) + N _ {B} (t _ {3})
$$

$$
Y _ {C \rightarrow E} (t _ {3}) = H _ {C E} S (1) + N _ {E} (t _ {3})
$$

Step (4) In $t_{4}$ , Alice transmits probe signal $\lambda_{A}S(1)$ to Carol, and Bob broadcasts jamming signal $S_{B}(1)=\lambda_{B}S(1)$ simultaneously, where $\lambda_{A},\lambda_{B}$ are independently generated from variable $\Lambda$ . The signals received by Carol and Eve are:

$$
Y _ {A B \rightarrow C} (t _ {4}) = \lambda_ {A} H _ {A C} S (1) + \lambda_ {B} H _ {B C} S (1) + N _ {C} (t _ {4}),
$$

$$
Y _ {A B \rightarrow E} (t _ {4}) = \lambda_ {A} H _ {A E} S (1) + \lambda_ {B} H _ {B E} S (1) + N _ {E} (t _ {4})
$$

where $N_{C}$ and $N_{E}$ are noises at Carol and Eve, respectively.

Step (5) Repeat Step (1)-(4) $M$ times. Then all of the signals received by Alice, Bob and Carol can be written as:

$$
\left\{ \begin{array}{l l} \mathbb {Y} _ {C \to A} & = H _ {A C} \mathbb {S} + \mathbb {N} _ {A} \\ \mathbb {Y} _ {C \to B} & = H _ {B C} \mathbb {S} + \mathbb {N} _ {B} \\ \mathbb {Y} _ {A \to C} & = H _ {A C} \mathbb {S} + \mathbb {N} _ {C} \\ \mathbb {Y} _ {B \to C} & = H _ {B C} \mathbb {S} + \mathbb {N} _ {C} \\ \mathbb {Y} _ {A B \to C} & = \lambda_ {A} H _ {A C} \mathbb {S} + \lambda_ {B} H _ {B C} \mathbb {S} + \mathbb {N} _ {C} \end{array} \right.
$$

And the signals received by Eve can be written as:

$$
\left\{ \begin{array}{l l} \mathbb {Y} _ {A \to E} & = H _ {A E} \mathbb {S} + \mathbb {N} _ {E} \\ \mathbb {Y} _ {B \to E} & = H _ {B E} \mathbb {S} + \mathbb {N} _ {E} \\ \mathbb {Y} _ {C \to E} & = H _ {C E} \mathbb {S} + \mathbb {N} _ {E} \\ \mathbb {Y} _ {A B \to E} & = \lambda_ {A} H _ {A E} \mathbb {S} + \lambda_ {B} H _ {B E} \mathbb {S} + \mathbb {N} _ {E} \end{array} \right.
$$

Step (6) Alice and Coral estimates $H_{AC}$ by

$$
\tilde {H} _ {A C} ^ {A} = \mathbb {Y} _ {C \rightarrow A} \frac {\mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} = H _ {A C} + \frac {\mathbb {N} _ {A} \mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} \tag {4}
$$

$$
\tilde {H} _ {A C} ^ {C} = \mathbb {Y} _ {A \rightarrow C} \frac {\mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} = H _ {A C} + \frac {\mathbb {N} _ {C} \mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} \tag {5}
$$

Bob and Coral estimates $H_{BC}$ by

$$
\tilde {H} _ {B C} ^ {B} = \mathbb {Y} _ {C \rightarrow B} \frac {\mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} = H _ {A C} + \frac {\mathbb {N} _ {B} \mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} \tag {6}
$$

$$
\tilde {H} _ {B C} ^ {C} = \mathbb {Y} _ {B \rightarrow C} \frac {\mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} = H _ {A C} + \frac {\mathbb {N} _ {C} \mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} \tag {7}
$$

Step (7) Bob sends message $\tilde{H}_{BC}^{B}$ and $\mathbb{S}_B$ to Alice by the secure channel. Alice and Carol computes:

$$
\begin{array}{l} \hat {Y} _ {A} = \lambda_ {A} \tilde {H} _ {A C} ^ {A} + \lambda_ {B} \tilde {H} _ {B C} ^ {B} \\ = \lambda_ {A} H _ {A C} + \lambda_ {B} H _ {B C} + \lambda_ {B} \frac {\mathbb {N} _ {B} \mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} + \frac {\mathbb {N} _ {A} \mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} \tag {8} \\ \end{array}
$$

$$
\hat {Y} _ {C} = \mathbb {Y} _ {A B \rightarrow C} \frac {\mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} = \lambda_ {A} H _ {A C} + \lambda_ {B} H _ {B C} + \frac {\mathbb {N} _ {C} \mathbb {S} ^ {T}}{\| \mathbb {S} \| ^ {2}} \tag {9}
$$

Step (8) Repeat Step (1)-(7) $L$ times, where $L$ is the system parameters. Then Alice obtains $\{\tilde{H}_{AC}^{A}(l)\}_{l = 1}^{L}$ , $\{\tilde{H}_{BC}^{B}(l)\}_{l = 1}^{L}$ and $\{\hat{Y}_A(l)\}_{l = 1}^L$ , and Carol obtains $\{\tilde{H}_{AC}^{C}(l)\}_{l = 1}^{L}$ , $\{\tilde{H}_{BC}^{C}(l)\}_{l = 1}^{L}$ and $\{\hat{Y}_C(l)\}_{l = 1}^L$

The details of Algorithm of SmokeGrenade at the stage of the channel information collection is shown in Alg. 1.

# Algorithm 1: SmokeGrenade

Input: $f_{s}$ : the sampling rate; the length of probe vector M for each measurement value; the random variable $\Lambda$ obeying Gaussian distribution $\mathcal{N}(0,a^{2})$ ; S: known probe vector $(1,\cdots,1)$ .

# Output:

Alice obtains $< \{\tilde{H}_{AC}^{A}(l)\}_{l = 1}^{L},\{\tilde{H}_{BC}^{B}(l)\}_{l = 1}^{L},\{\hat{Y}_{A}(l)\}_{l = 1}^{L}>$

Carol obtains $< \{\tilde{H}_{AC}^{C}(l)\}_{l = 1}^{L},\{\tilde{H}_{BC}^{C}(l)\}_{l = 1}^{L},\{\hat{Y}_{C}(l)\}_{l = 1}^{L}>$

1: for round $l = 1, \cdots, L$ do

2: In $t_{4i-3}$ ( $i=1,\cdots,M$ ), Alice sends known probe $S(i)$ to Carol.

3: In $t_{4i-2}$ ( $i=1,\cdots,M$ ), Bob sends known probe $S(i)$ Carol.

4: In $t_{4i-1}$ ( $i=1,\cdots,M$ ), Carol broadcasts known probe $S(i)$ to Alice and Bob.

5: In $t_{4i}$ ( $i=1,\cdots,M$ ), Alice and Bob generate $\lambda_{A}$ and $\lambda_{B}$ with $\Lambda$ , and then send $\lambda_{A}S(i)$ and $\lambda_{B}S(i)$ to Carol, respectively.

6: Alice estimates $H_{AC}$ with Equ. 4; Bob measures $H_{BC}$ with Equ. 6; Carol estimates $H_{AC}, H_{BC}$ and $\lambda_A H_{AC} + \lambda_B H_{BC}$ with Equ. 5, 7 and 9 respectively.

7: Bob transmits $H_{BC}$ and $\lambda_{B}$ to Alice with secure channel.

8: Alice estimates $\lambda_A H_{AC} + \lambda_B H_{BC}$ with Equ. 8.

9: end for

2) Quantizing the Collected Information: Many quantization methods have been proposed in previous work. For instance, [12] partitions the channel measurements to multiple parts and performs quantization in every part. We let

$$
\begin{array}{l} \mathbb {Y} _ {A} = <   \tilde {\mathbb {H}} _ {A C} ^ {A}, \tilde {\mathbb {H}} _ {B C} ^ {B}, \hat {\mathbb {Y}} _ {A} > \\ = <   \left\{\tilde {H} _ {A C} ^ {A} (l) \right\} _ {l = 1} ^ {L}, \left\{\tilde {H} _ {B C} ^ {B} (l) \right\} _ {l = 1} ^ {L}, \left\{\hat {Y} _ {A} (l) \right\} _ {l = 1} ^ {L} > \tag {10} \\ \end{array}
$$

$$
\mathbb {Y} _ {C} = <   \tilde {\mathbb {H}} _ {A C} ^ {C}, \tilde {\mathbb {H}} _ {B C} ^ {C}, \hat {\mathbb {Y}} _ {C} >
$$

$$
= <   \{\tilde {H} _ {A C} ^ {C} (l) \} _ {l = 1} ^ {L}, \{\tilde {H} _ {B C} ^ {C} (l) \} _ {l = 1} ^ {L} \{\hat {Y} _ {C} (l) \} _ {l = 1} ^ {L} >
$$

The quantizer that we used in this work is described as follows:

\- Alice and Carol divide $\hat{\mathbb{Y}}_A$ (resp. $\hat{\mathbb{H}}_{AC}^A$ , $\hat{\mathbb{H}}_{BC}^B$ ) and $\hat{\mathbb{Y}}_C$ (resp. $\hat{\mathbb{H}}_{AC}^C$ , $\hat{\mathbb{H}}_{BC}^C$ ) into small blocks and each block contains $\kappa$ sample values, respectively.

\- For each block, they calculate two adaptive thresholds $q^{+}$ and $q^{-}$ independently such that $q^{+} = \mu + \alpha \times \sigma$ and $q^{-} = \mu - \alpha \times \sigma$ , where $\mu$ and $\sigma$ are the mean value and standard deviation of the block, and $\alpha \geq 0$ is a chosen constant of our protocol.

\- Alice and Carol parse their channel measurements and drop channel estimates that lie between $q^{+}$ and $q^{-}$ and maintain a list of indices to track the channel estimation dropped. They exchange their list of dropped channel estimations and only keep the ones (named valid indices) that they both decide not to drop.

\- Alice and Carol generate their bit streams by extracting a “1” or a “0” for each channel estimation if the estimation lies above $q^{+}$ or below $q^{-}$ , respectively.

We denote the bit streams after being quantized as $K_{A} = \{\hat{Y}_{A}^{Q}(n)\}_{n=1}^{N}$ and $K_{C} = \{\hat{Y}_{C}^{Q}(n)\}_{n=1}^{N}$ .

3) Information Reconciliation: After obtaining $K_{A}$ and $K_{C}$ at Alice and Carol respectively. The asymmetry in the bit streams brings up the challenge of how to make Alice and Carol agree upon the same bits without giving out too much information on the channel that can be used by the adversary Eve to recreate secret bits between Alice and Carol. Following the work [7], we assume that the Hamming distance of two bit streams is at most t. We use a $[N,k,2t+1]$ error-correcting code C to correct errors in $K_{C}$ as follows. Alice randomly selects a codeword c from C and computes $S(K_{A}) = K_{A} \oplus c$ . Then Alice sends $S(K_{A})$ to Carol. Upon receiving $S(K_{A})$ , Coral computes $c' = K_{C} \oplus S(K_{A})$ . Then Carol decodes $c'$ to get c, and computes $K_{A}$ by $K_{A} = c' \oplus c \oplus K_{C}$ .   
4) Privacy Amplification: It is worth mentioning that since the reconciliation information is public to both the communicating nodes and the adversary, it can be used by the adversary as well to guess portions of the generated key. To cope with this problem, Alice and Carol can further run privacy amplification protocols [6] to recover the entropy loss.

# B. Theoretical Analysis

In this subsection, we analyze the performance and information theoretic limits of the SmokeGrenade. It has been shown in [5] that the secret key rate can be upper bounded by the conditional mutual information between the observations of two keying nodes under the observations of Eve. Based on the measured values of $Y_{A}$ and $Y_{C}$ at Alice and Carol respectively, we have the following Theorem 2.

Theorem 2: Let $\delta_{AC} = \delta_{BC} = \delta_{0} = 1$ . If the channel gains is i.i.d across coherence periods, and the sampling number M in $T_{c}$ is sufficiently large. Then the maximum key rate $R^{SG}$ of SmokeGrenade is bounded by

$$
R ^ {S G} \geq \frac {1}{T _ {c}} [ \ln a + \frac {3}{2} \ln 2 \pi e - \frac {1}{2 e} ] \tag {12}
$$

where $T_{c}$ is the coherence time. Moreover, $R^{SG} \to \infty$ when the average interference power $P_{B} \to \infty$ . Furthermore, the protocol is information-theoretically security.

Proof: Please refer to tech-report [1] for details.

# C. Numerical analysis

As an example with the parameters $T_{c} = 15ms$ , $f_{s} = 4GHz$ , $\delta_{AC} = \delta_{BC} = \delta_0 = 1$ , Fig. 3(a) plots the achievable key rate of SmokeGrenade, which shows that the key generation rate rises when $P_B$ increases. Fig. 3(b) plots the performance of traditional protocols versus the SmokeGrenade. Notice that, by [19], the theoretical maximum key rate of traditional protocols is $\frac{1}{T_c} I(H_{AC};H_{CA}|H_{AE},H_{CE}) = \frac{1}{T_c}\mathcal{H}(H_{AC}) = \frac{1}{2T_c}\ln (2\pi e)$ when

![](images/6a88c5cf69544baf2bfa570efe16822a1a5ead0b10c78fb01e5eda36325f9835.jpg)



(a)

![](images/b9cd912e8fb604e65e307a5c224d79a949167cc350b5d61e4cc680b5f6dae734.jpg)



(b)

Fig. 3. (a) The theoretical achievable key rate $R^{SG}$ versus the interference power $P_{B}$ . (b) The theoretical performance of the SmokeGrenade versus the traditional protocols under different values of $P_{B}$ .   
![](images/d5886b4b9cfeddf6c2e83a747de0f7d168e9a44c393082c5f5da6d4280f3dac2.jpg)



(a)

![](images/f2297f77a77cc2b934f0f30fbce6962f6152e7caaaff29ccc21b6edaf51ab04a.jpg)



(b)

Fig. 4. (a) Group key distribution scene, where the secure channel 1 is established with traditional protocol, and secure channel 2, 3 are set up by using SmokeGrenade. (b) Two antennas scene, in which Alice and Bob are antennas of one wireless device. Hence, in this scenario, there exists a “secure channel” between Alice and Bob.   
![](images/7169e54bc7739fa15d8fab0070328ebd21cef4ed5a03c9948c49c90e55073d1c.jpg)



Fig. 5. The channel measurement without interference when SNR=0dB.

![](images/17a69a334488e96f21d3cef8a3845fd3a7132a8f7de00bcc78b3abc6f257114c.jpg)



Fig. 6. The channel measurement with interference when SNR=0dB, $P_{B}=4$ .

the sampling number M is sufficiently large. The result shows that the achievable key rate of the SmokeGrenade is larger than the traditional ones. In particular, our scheme is makes 3 times better than that of the traditional ones when $P_{B}=1$ , hence, has the great advantage compared with traditional protocols.

In known-interference model, we use a secure channel to achieve the symmetry of the interference for keying nodes. It seems that the assumption about adding a secure channel between Alice and Bob is too strong, in this case, we can assume that the helper has already established trust relationship between one of the keying nodes, and the keying nodes want to use Bob as a helper to facilitate secret generation between them. There are two special cases shown as follows. (i) In the process of generating a group key (Case (i) shown in Fig. 4(a) with assumption that the group nodes are within single hop), we can use the key generation scheme in [11]–[13] to produce a secure channel for a pair of nodes, while leveraging our SmokeGrenade for the others. It still improves the overall efficiency of group key generation with no doubt; (ii) Alice and Bob are the two antennas of some multiple antenna device (See Fig. 4(b) for illustration). In this scenario, there does exist a “secure channel” between Alice and Bob.

![](images/0dd2938521feb0ab24305cee3c3f412a5e5de5d727d0926bc5ccb6cf98b47344.jpg)



Fig. 7. Measurements at Alice and Carol when M=2000, SNR=0dB, $P_{B}=4$ .

![](images/f6927863fa320a5b8e796c506bcaa86cc90f6e1ffc7175479012f894017a26a1.jpg)



Fig. 8. Measurements at Alice and Eve when M=2000, SNR=0dB, $P_{B}=4$ .

# VI. SIMULATION STUDIES

In order to verify the feasibility and efficiency of SmokeGrenade, we conduct extensive simulations. Basically, we simulate a communication system, include keying nodes Alice and Carol, helper Bob and adversary Eve with the Rayleigh fading channel that each pair of these nodes experience. To simplify our simulation, we assume that the probes and artificial interference are single-tone signals. Let $s(\tau) = a_{0} \cos(\omega_{0} \tau + \theta_{0}) (\tau \in [0, T])$ be the known probing signals, where $a_{0}$ is the amplitude, $\omega_{0}$ is the angular frequency, $\theta_{0}$ is the initial phase and T is the length of a single time slot. In our simulation, the probing signals are set to be fixed at probing steps (i.e., each of the transmitters sends $s(\tau) (\tau \in [0, T])$ at Step (1) and Step (2)), and are decided by $\lambda_{A}$ (or $\lambda_{B}$ ) at jamming step (i.e., Alice sends $\lambda_{AS}(\tau) (\tau \in [0, T])$ and Bob sends $\lambda_{BS}(\tau) (\tau \in [0, T])$ at Step (3)). In addition, we assume that the carrier frequency of the single-tone signal is 0.9GHz, the sampling rate $f_{s} = 2.7GHz$ , and the Doppler frequency shift is 10HZ (hence, the coherence time $T_{c} = \frac{0.423}{10} = 42ms$ ). We further assume [127, 85, 13]-BCH code is utilized in the system with error tolerance $\frac{6}{127} \approx 0.047$ (named error threshold).

The first example considers the effect of interference on channel measurements. Fig. 5 shows the variation of the channel measurement without interference. The values displayed periodical changes with the transfer of coherence time and the variation range is small. Moreover, the change in each coherence time is great slowly. Thus, the generated key rate is low and the key is easily cracked by Eve. Fig. 6 shows the variation of measurements with jamming. As we can see, the variation range of the measurements is large, even in coherence time. Hence, with these values, we can make a key with high generation rate and high entropy. Fig. 7 plots the collected values at Alice and Carol when SNR=0dB and interference power $P_{B}=4$ . It is not hard to see that the values at Alice and Carol constantly change over time and have similar variations. Fig. 8 shows the collected values at Alice and Eve when SNR is 0dB and $P_{B}=4$ which shows that Eve at a third location measures different values.

![](images/3988785737b372249ef80bd7a64916222fd3d8c9195c3589b997e5632735ed02.jpg)



Fig. 9. Mismatch (match) rate againsts $\alpha$ under different values of $\kappa$ , where $\alpha = 0.3$ , $P_{B} = 4$ and M=2000.

# A. Mismatch Rate and Match Rate

We consider the effect of the quantizer parameters $\alpha$ and $\kappa$ on the mismatch rate (i.e., the ratio of the number of mismatch bits to the number of valid indices) and match rate (i.e., the ratio of the number of match bits to the number of measurements) before the information reconciliation. The quantizer in our protocol divides the measurements into smaller blocks with length $\kappa$ and calculates the thresholds for each block separately. Obviously, a smaller $\alpha$ improves the rate of bits generation but increases the mismatched bits ratio as well. For example, Fig. 9 shows the mismatch rate and match rate versus $\alpha$ under different values of $\kappa$ , where SNR=0dm, $P_{B}=4$ . When $\alpha=0.3$ , the mismatch rate is less than the error threshold 0.047, and the match rate is higher than 0.5. Thus, we choose $\alpha=0.3$ in our system. Fig. 10 shows mismatch rate an match rate with different block sizes. We can see that the matched ratio remain relatively stable, while mismatched ratio experiences relatively large fluctuation. Especially, when the block size is up to 30, the number of mismatched bits ratio is less than 0.047. In our system, we set block size $\kappa=30$ .

Then we consider the effect of M (i.e., the length of probe vector for each measurement value) on the mismatch rate and match rate respectively. Fig. 11 plots the mismatch rate versus M under different interference powers $P_{B}$ , where $\kappa = 30$ and $\alpha = 0.3$ . Fig. 12(a) shows the key rate versus interference power $P_{B}$ under different SNRs, where $\kappa = 30$ , $\alpha = 0.3$ and

![](images/4fa0a83a056913db6019aa49a08f509e4e92f1f79c111afb04b21742c6554148.jpg)



Fig. 10. Mismatch (match) rate againsts block size $\kappa$ , where $\alpha = 0.3$ , $P_B = 4$ and $M = 2000$ .   
![](images/01230dcfd74c0eb18ef37b6cd4d6a1728c9ba7365dd2371acfa106ae65f74371.jpg)



Fig. 11. Mismatch (match) rate againsts $M$ and $P_B$ , where $\kappa = 30$ , $\alpha = 0.3$ , $P_B = 4$ , SNR=0dB.

![](images/e5ed697b956597ceb7453819b8cc2bbd4e53e59ee15456d28ca17f3bd8ec582c.jpg)



(a)

![](images/e8ba9c4be88fc5c3c23793bc89512ca98c0609ca32444640344883628bb14a8a.jpg)



(b)   
Fig. 12. When $\kappa = 30$ , $\alpha = 0.3$ , M = 2000; (a) Key rate against the interference power $P_{B}$ under different SNR; (b) The conditional entropy of generated bits at Alice on condition the generated bits at Eve is known under different SNR.

M = 2000. The results show that (i) a larger M improves the matched bits ratio and decrease the mismatched bits ratio; (ii) The larger $P_{B}$ and SNR also increase the match rate and lessen the mismatch rate. However, the larger value of M is the more energy consumption is. To minimize the energy expenditure, for each pair of SNR and $P_{B}$ , we can choose the least value of M such that the mismatch rate is lower than error threshold. As shown in Table II, we conduct our simulation in a wide variety of SNR and $P_{B}$ to find the optimal value of M.

TABLE II THE OPTIMAL VALUE OF $M(\times 10^{3})$ 

<table><tr><td>SNR\ $P_B$ </td><td> $P_B$ =1</td><td> $P_B$ =2</td><td> $P_B$ =3</td><td> $P_B$ =4</td><td> $P_B$ =5</td></tr><tr><td>SNR=0dB</td><td>5.7</td><td>5.2</td><td>2</td><td>1.5</td><td>1.1</td></tr><tr><td>SNR=5dB</td><td>1.7</td><td>0.8</td><td>0.6</td><td>0.45</td><td>0.3</td></tr><tr><td>SNR=10dB</td><td>0.5</td><td>0.3</td><td>0.2</td><td>0.15</td><td>0.15</td></tr><tr><td>SNR=15dB</td><td>0.2</td><td>0.1</td><td>0.08</td><td>0.05</td><td>0.04</td></tr><tr><td>SNR=20dB</td><td>0.08</td><td>0.01</td><td>0.01</td><td>0.01</td><td>0.01</td></tr></table>

TABLE III
NIST STATISTICAL TEST SUITE RESULTS 

<table><tr><td>Test</td><td>SNR=0dB</td><td>SNR=10dB</td><td>SNR=20dB</td></tr><tr><td>Runs</td><td>0.63</td><td>0.71</td><td>0.76</td></tr><tr><td>FFT</td><td>0.60</td><td>0.73</td><td>0.81</td></tr><tr><td>Frequency</td><td>0.54</td><td>0.62</td><td>0.64</td></tr><tr><td>Approx. Entropy</td><td>0.58</td><td>0.61</td><td>0.72</td></tr><tr><td>Longest run of ones</td><td>0.62</td><td>0.78</td><td>0.74</td></tr></table>

![](images/bbc1770c3cec5f7b704a95c6e67e000c13934a6b24a6c5b67a0a2f0483e63eb5.jpg)



(a) The generated bits at Alice

![](images/dde888174e27ca89c50a93dcdbc750b896f4dd48ba4fe81fc40cfc30f9cd9251.jpg)



(b) The generated bits at Eve   
Fig. 13. The correlation of generated bits between Alice and Eve, where the black squares denotes “1”, the grey squares denote “0”, and $\kappa = 30$ , $\alpha = 0.3$ , SNR = 0, M = 1200, $P_{B} = 5$ .

# B. Key Randomness

To make sure that all generated keys are random is crucial because they are intended for being used as a cryptographic key. The randomness test results indicate whether SmokeGrenade is secure to defend the key from opponent. We employ a widely used randomness test suite NIST to verify the randomness of the generated bits from our simulation. The p-value from four kinds of tests is listed in Table III. A p-value is the probability of obtaining a test statistic larger than one observed if the sequence is random. Small values are interpreted as an evidence that a sequence is unlikely to be random. To pass a test, the p-value for that test must be greater than 0.01. Let $P_{B}=4$ and M be the corresponding optimal value for each SNR (0, 10, and 20dB), we find that the bit streams generated from SmokeGrenade pass all the tests.

# C. Key entropy

As we know, entropy is a measure of the uncertainty in a random variable in information theory, i.e., the high randomness means the high entropy. However, the high entropy (randomness) of the generated bits at keying nodes is a necessary but not sufficient condition for security. Thus, we need the conditional entropy (or equivocation) $\mathcal{H}(X|Y)$ , which quantifies the amount of information needed to describe the outcome of a random variable X when the value of another random variable Y is given, to measure the level of the key's security. It is clear that $\mathcal{H}(K_{A}|K_{E})=0$ in the above example, where $\mathcal{H}(K_{A}|K_{E})=\sum_{i,j}\Pr_{AE}(i,j)\log(1/\Pr_{A|E}(i|j))$ , $i,j\in\{0,1\}$ . Fig. 13 plots the generated bits at Alice and Eve, where the black squares denotes “1”, the grey squares denotes “0”, and $\kappa=30$ , $\alpha=0.3$ , SNR=0, M=1200, $P_{B}=5$ . It shows that the generated bits have relatively weak correlation between Alice and Eve. Fig. 12(b) presents the conditional entropy of generated bits at Alice on condition the generated bits at Eve under different SNRs, where the number of generated bits are $10^{4}$ , $\kappa = 30$ , $\alpha = 0.3$ and M = 2000 respectively. We can see that the conditional entropy is more than 0.999 and the keys generated from SmokeGrenade have high key entropy. Notice that $\mathcal{H}(X|Y) = \mathcal{H}(X)$ if and only if Y and X are independent random variables. Hence, the generated bits $K_{A}$ and $K_{E}$ are almost independent, which indicates that the key bits are information-theory security.

![](images/9b75b6ace9401b819419ec5ae4e71752d1d8946aa254cfe66b186993ce1cb0c7.jpg)



(a)

![](images/06f2e1054d540fbdaa57cb43467e1d1d838865a813bacde10449bc003c029e75.jpg)



(b)   
Fig. 14. (a) The correlation of generated key between Alice and Eve in different scenarios; (b) Secret bit rate in different scenarios. Mismatch (match) rate against $M$ and $P_B$ under different SNRs, where $\kappa = 30$ , $\alpha = 0.3$ , $P_B = 4$ .

# D. Comparison with Related works

Compared with existing key extraction approaches (e.g., Aono [10], Mathur [12], ASBG [13]) and SmokeGrenade. SmokeGranade can generate secret key with higher entropy and key rate. The reason is that the measurements in those schemes are not uniformly distributed, and the key generation scheme highly depends on the variation of channel state. However, our scheme employs the artificial interference to increase the variation range of the measurements. Thus, the artificial jamming will improve the randomness of the key bits. Moreover, those methods only use either the deep fades, or channel measurements above or below the threshold. However, in our scheme, the artificial interference is used to amplify the value of measurements. Thus, the discarded sample will be dramatically reduced with the quantizer in our scheme. In SmokeGrenade, we set $\alpha = 0.3$ and K = 30 respectively. We conduct our simulation under different cases: $A(SNR = 0dB, P_B = 5, M = 1100)$ , $B(SNR = 5dB, P_B = 4, M = 450)$ , $C(SNR = 10dB, P_B = 3, M = 200)$ , $D(SNR = 15dB, P_B = 2, M = 100)$ and $E(SNR = 20dB, P_B = 1, M = 80)$ respectively. The performance of the different scenarios is shown in Fig. 14.

# VII. CONCLUSION

In this paper, we present a new physical layer approach, SmokeGrenade, for secret key generation in narrowband fading channel and static environments, which utilizes interference to contribute to the changes of channel states. We give the theoretical upper bound of key generate rate for the traditional model with interference. The simulation results show that SmokeGrenade generates secret bits with a high secret bit rate, a high entropy and a low mismatch bit rate.

# ACKNOWLEDGMENT

This work is supported in part by the National Nature Science Foundation of China under Grant (No. 61272426, 60903157, 61133016, 61163066, and 60902074), China Postdoctoral Science Foundation funded project under grant No. 2012M510029 and 2013T60119, and the National High Technology Joint Research Program of China (863 Program, Grant No. 2011AA010706). This work is also partly supported by Important National Science and Technology Specific Project of China (No. 20112X03002-002-03).

# REFERENCES

[1] Tech-Report: mypages.iit.edu/\~xmao3/images/smokegrenade-TR.pdf   
[2] C. E. Shannon, “Communication theory of secrecy systems,” Bell System Technical Journal, vol. 28, pp. 656-715, 1948.   
[3] A. D. Wyner, “The wire-tap channel,” Bell System Technical Journal, vol. 54, pp. 1355-387, 1975.   
[4] W. Diffie and M. Hellman, “New directions in cryptography,” IEEE Transactions on Information Theory, vol. 22, no. 6, pp. 644-654, 1976.   
[5] R. Ahlswede and I. Csiszar, “Common randomness in information theory and cryptography, Part I: Secret sharing,” IEEE Transactions on Information Theory, vol. 39, pp. 1121-1132, 1993.   
[6] U. Maurer and S. Wolf, “Secret-key agreement over unauthenticated public channels II: The simulatability condition,” IEEE Transactions on Information Theory, vol. 49, no. 4, pp. 832-838, 2003.   
[7] Y. Dodis, et al., “Fuzzy extractors: How to generate strong keys from biometrics and other noisy data,” In Proceedings of EUROCRYPT, pp. 523-540, 2004.   
[8] P. Parada and R. Blahut, “Secrecy capacity of simo and slow fading channels,” In Proceedings of IEEE ISIT, Adelaide, Australia, pp. 2152-2155, 2005.   
[9] D. Tse and P. Viswanath, Fundamental of Wireless Communication. Cambridge, U.K.: Cambridge University Press, 2005.   
[10] T. Aono, et al., “Wireless secret key generation exploiting reactance-domain scalar response of multipath fading channels,” IEEE Transactions on Antennas and Propagation, vol. 53, pp. 3776-3784, 2005.   
[11] B. Azimi-Sadjadi, et al., “Robust key generation from signal envelopes in wireless networks,” In Proceedings of ACM CCS, pp. 401-410, 2007.   
[12] S. Mathur, et al., “Radio-telepathy: extracting a secret key from an unauthenticated wireless channel,” In Proceedings of ACM MOBICOM, pp. 128-139, 2008.   
[13] S. Jana, et al., “On the effectiveness of secret key extraction from wireless signal strength in real environments,” In Proceedings of ACM MOBICOM, pp. 321-332, 2009.   
[14] J. Croft, et al., “Robust uncorrelated bit extraction methodologies for wireless sensors,” In Proceedings of ACM/IEEE ICNP, pp. 70-81, 2010.   
[15] K. Zeng, D. Wu, A. Chan, and P. Mohapatra, “Exploiting multiplean-tenna diversity for shared secret key generation in wireless networks,” In Proceedings of IEEE INFOCOM, pp. 1-9, 2010.   
[16] S. Gollskota and D. Katabi, “Physical layer wireless security made fast and channel independent,” In Proceedings of IEEE INFOCOM, pp. 1125-1133, 2011.   
[17] Q. Wang, et al., "Cooperative Secret Key Generation from Phase Estimation in Narrowband Fading Channels," IEEE Journal on Selected Areas in Communications, Special Issue on Cooperative Networking Challenges and Applications, Vol. 30, No. 9, pp. 1666-1674, 2012   
[18] K. Ren, H. Su, and Q. Wang, "Secret Key Generation Exploiting Channel Characteristics in Wireless Communication," IEEE Wireless Communications, Vol. 18, No. 4, pp. 6-12, August, 2011   
[19] J. Wallace, “Secure physical layer key generation schemes: Performance and information theoretic limits,” In Proceedings of IEEE ICC, pp. 1-5, 2009.   
[20] M.L. Jorgensen, et al., “Shout to Secure: Physical-Layer Wireless Security with Known Interference,” In Proceedings of IEEE GLOBECOM, pp. 33-38, 2007.   
[21] L. Lai and H. E. Gamal, “The relay-eavesdropper channel: Cooperation for secrecy,” IEEE Transactions on Information Theory, pp. 4005-4019, 2008.   
[22] R. Negi and S. Goel, “Secret communication using artificial noise,” In Proceedings of IEEE VTC, 2005.   
[23] S. Goel and R. Negi, “Guaranteeing Secrecy using Artificial Noise,” IEEE Transactions on Wireless Communication, 2008.