# Achieving Private, Scalable, and Precise Data Collection in Wireless Sensor Networks

Saiyu Qi∗†, Zhenjiang Li† and Yunhao Liu‡

∗Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong

†School of Computer Engineering, Nanyang Technological University, Singapore

‡TNLIST, School of Software, Tsinghua University, China

syqi@ust.hk, lzjiang@ntu.edu.sg, liu@cse.ust.hk

Abstract—Wireless Sensor Networks (WSN) become increasingly popular to collect data over a large area. Given the collected data set, the network manager can extract various kinds of aggregate statistics from the set to characterize the physical space. On the collection of the data, three requirements should be imposed: (1) Privacy: as sensor nodes are source limited and often deployed in an open environment, the sensed data suffer from privacy vulnerabilities. Secure mechanism should be provided to protect data privacy; (2) Communication efficiency: collecting data from large-scale sensor networks often involves large-volume data generation and transmission, which may quickly consume the energy of the WSN. To prolong the lifetimes of the sensor nodes, the sensed data should be transmitted in lightweight manner; (3) Accuracy: the sensed data should be recovered accurately at the base station (BS) so that the manager can manipulate them freely to achieve any precise aggregate statistic he prefers. To satisfy these requirements, we propose two novel privacy-preserving data collection schemes based on compressive sensing techniques. Our schemes address the privacy, communication efficiency and accuracy issues simultaneously. Detailed theoretical analysis and simulation results confirm the high performance of the proposed schemes.

Keywords-Data collection; Wireless Sensor Networks; Privacy

# I. INTRODUCTION

Wireless sensor networks (WSN) are becoming increasingly popular for a wide range of applications. Wireless sensor nodes are deployed in various kinds of physical areas such as factories, office areas, forests or rivers to sense the physical space [15], [18], [19]. Sensor nodes convert physical parameters such as heat, light intensity or temperature to data items and send them to base station (BS) through multiple intermediate nodes.

In many sensor network applications, the network manager is interested in various kinds of aggregate statistics (such as SUM, AVERAGE, MAX/MIN, MEDIAN, HIS-TOGRAM, PERCENTILE, TOP-k, TRENDLINE) from the sensed data over a physical area, which are often used to present the physical characteristics of the area. To achieve these statistics, the base station needs to collect the sensed data from the whole area. However, successful accomplishment of data collection suffers privacy issues. As sensor nodes are often deployed in open environments, it is easy for an adversary to eavesdrop on the communication links to explore the content of the data. Even worse, sensors cannot provide temper-resistance for cost consideration. An adversary can thus easily compromise them to obtain their sensed data and control them.

To eliminate such privacy vulnerabilities, several privacypreserving schemes have been proposed. These schemes, however, only aim to design secure mechanism to protect data privacy without the consideration of communication efficiency or accuracy, both of which are also essential in the data collection process. In particular, (1) For communication efficiency: as sensors are usually resource-limited and power-constrained [17], forwarding large volume data innetwork may quickly consume the energy of the WSN since data transmission is a highly energy-consuming operation. To maximize sensor lifetime, it is essential to improve communication efficiency during the data collection process. (2) For accuracy: during the data collection process, each node will generate a data and forward it to the BS. Each of the data should be recovered individually and precisely by the BS so that it can manipulate them freely to achieve precise aggregate statistic. Most of the previous privacypreserving schemes suffer from the drawback of either low communication efficiency or inaccuracy, as we will discuss in detail in Section II.

In this paper, we systematically study the problem of private, scalable and precise data collection in wireless sensor networks. We design two privacy-preserving schemes to solve this problem. Firstly, our schemes can guarantee both communication efficiency and accuracy. To achieve this goal, we propose to use a novel technique called compressive sensing (CS) [7-9], which shows that spatially correlated data can be compressed during the transformation and precisely recovered when needed, as the data forwarding infrastructure for both of our two schemes. Such a utility is based on the observation of the inherent nature of the sensed data. As WSN are in general deployed in a specific area, data are not generated independently at each individual node. Instead, there exists spatial correlation between them. Such a correlation provides us a potential to compress these data by using compressive sensing (CS) technique during the forwarding process.

Secondly, our schemes provide data privacy to resist both eavesdropping attack and compromising attack with moderate computational overhead. To achieve this goal, we integrate the CS based data forwarding infrastructure with several lightweight cryptographic primitives. We design our first scheme by integrating two cryptographic primitives: pseudorandom permutations (PRP) [10] and symmetric encryption with the CS based data forwarding infrastructure. The advantage of this scheme is that it partially relies on the nature of CS technique to provide data privacy, and thus introduce little computational overhead. This scheme is resilient to the eavesdropping adversary and allows the compromising adversary to learn only restricted knowledge about the sensed data. To further eliminate the threat of compromising attack, we design the second scheme by integrating pseudorandom permutations (PRP) [10] and additively homomorphic encryption (AHE) [4] with the CS based data forwarding infrastructure. The basic idea is that we do not rely on the CS technique itself to protect data privacy. Instead, the sensed data are locally encrypted at each sensor node before sending out. We choose additively homomorphic encryption as our encryption mechanism so that the encrypted data can still be compressed in-network. Such a construction largely enhances the data privacy as the adversary cannot obtain the sensed data unless it captures the encryption key. Comparing with the first scheme, the second scheme provides a strict cryptography guarantee against the compromising threat.

The rest of this paper is organized as follows. Section II discusses related works. We introduce technique preliminaries in Section III. We describe the network and adversary models in Section IV. We present the design of our schemes in section V. We conduct security analysis and performance evaluation in Sections VI and VII respectively.

# II. RELATED WORK

Previous private-preserving schemes often raise high communication overhead or can only collect inaccurate data. They can be classified into two categories.

Basic encryption scheme: In basic encryption scheme, each sensor shares a symmetric key with the BS for data encryption. After forwarding over multiple hops, the encrypted data will be decrypted at the BS. As each data is forwarded individually and under encryption, the requirements of privacy and accuracy can be satisfied. However, this scheme suffers from poor communication efficiency which consumes the energy of sensors in two folds: (1) Overall energy consumption: as each sensed data needs to be forwarded through multi-hop routing from the individual sensor nodes to BS, transmitting large number of them will quickly consume the energy of the sensors. (2) Energy balance: as the amount of data forwarded by those sensors

Table I FREQUENTLY USED NOTATIONS 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $Q$ </td><td>The number of sub trees</td></tr><tr><td> $u_{j}$ </td><td>In a sub tree,  $u_{j}$  denotes a single sensor node which has  $j$  hops to BS</td></tr><tr><td> $d_{j}$ </td><td>A sensed data generated at  $u_{j}$ </td></tr><tr><td> $d$ </td><td>A data vector consists of multiple  $d_{j}$ </td></tr><tr><td> $hk_{j}$ </td><td>A homomorphic key of  $u_{j}$ </td></tr><tr><td> $k_{j}$ </td><td>A PRP key of  $u_{j}$ </td></tr><tr><td> $sk_{ii+1}$ </td><td>A symmetric key shared between  $u_{i}$  and  $u_{i+1}$ </td></tr><tr><td> $\{u_{q}\}_{q=j+1}^{N}$ </td><td>All the downstream nodes of  $u_{j}$ </td></tr><tr><td> $Z_{j+1}$ </td><td>The size of  $\{u_{q}\}_{q=i+1}^{N}$ </td></tr><tr><td> $M$ </td><td>The dimension number of the compressed vector</td></tr><tr><td> $R$ </td><td>A random number generated at BS</td></tr><tr><td> $S$ </td><td>A secure parameter generated at BS</td></tr><tr><td> $A$ </td><td>A sensing matrix</td></tr><tr><td> $a_{ij}$ </td><td>An element of  $A$ </td></tr></table>

closer to the BS is up to several orders of magnitude larger than that of the nodes on the boundary of sensing area, energy consumption is not well balanced. As a result, sensors close to BS will quickly consume their energy and lose functionality.

Private data aggregation schemes: To overcome the above efficiency issues, private data aggregation schemes [1-6] are proposed. Through data aggregation, the overhead of transformation is dramatically decreased. However, data accuracy is also degrade in the aggregation process as BS can only get an inaccurate aggregation result, such as the summation of the sensed data, from which it is hard to extract various sophisticated aggregate statistics. In particular, the summation can only be directly used to extract limited aggregate statistics like COUNT and AVERAGE. More advanced aggregate statistics such as HISTOGRAM, PERCENTILE, TOP-k, TRENDLINE are hard to obtain. The private data aggregation schemes can be divided into several types based on the aggregation manner, among which the most efficient type is end to end manner [3], [4], [6]. Comparing with other types, end to end manner consumes less energy and achieves better energy balance. For this reason, we will only consider end to end manner in this study. By using an end to end private data aggregation scheme, sensed data are aggregated at intermediate nodes. Each intermediate node forwards an aggregation of data, which is generated from the sensed data of all downstream nodes. To protect data privacy, all the data are encrypted in the forwarding process. In the remainder of this paper, we just term end to end private data aggregation as private data aggregation for simplicity.

# III. TECHNIQUE PRELIMINARIES

# A. Introduction of compressive sensing

The compressive sensing (CS) technique [7-9] is a kind of compression technique for data transmission and sharing in pervasive platforms. The key idea of CS is that spatially correlated data can be jointly transmitted in an efficient compressed pattern rather than one by one. Consider a WSN consisting of $N$ nodes and a BS, each node having a sensed data $d _ { j } , j = 1 , \cdots , N .$ , which forms a spatially correlated data vector $d / = \{ d _ { 1 } , d _ { 2 } , \dotsb , d _ { N } \}$ . To get $d ,$ a trivial way is to require each node to report its sensed data one by one to BS. Instead, CS provides a more efficient way in which the vector d can be accurately recovered from a small number M $( M { < } { < } N )$ of linear combination vector $\scriptstyle y = \{ y _ { 1 } , y _ { 2 } , \cdot \cdot \cdot , y _ { M } \}$ . Each element $y _ { j }$ is a linear combination of all the elements of d: $\begin{array} { r } { y _ { j } = \sum _ { i = 1 } ^ { N } a _ { i } d _ { i } } \end{array}$ where $a _ { i }$ is a constant number. We can present y as: $y = A { \times } d .$ CS guarantees that, for a random sensing matrix A, d can be accurately recovered from $y .$

The utilization of CS is based on the assumption that the sensed data has spatial correlation. Actually, work presented in [12], [13] is among the first to use CS to recover sensed data from WSN. Experiments on real data sets [13] show that sensed data indeed has spatial correlation and can be precisely recovered by using CS. Furthermore, through reorganization, even data without spatial correlation can be precisely recovered by using CS. The schemes [12], [13] however, cannot be directly applied in our target scenario since even an eavesdropping adversary can recover all the sensed data of WSN. Recently, [20], [21] propose to use compressive sensing as encryption to secure the transmitted signals. Unfortunately, their schemes still cannot defense eavesdropping attack if deployed in our scenario.

# B. Cryptographic primitives

Additively homomorphic encryption (AHE): We choose [4] as the candidate of our additive homomorphic encryption, which can be formally described as follows: Let HE() denote the encryption algorithm. Let $h k _ { i }$ denotes a homomorphic key and MS the domain of the message space. Given two ciphertexts $c _ { 1 } = H E _ { h k _ { 1 } } ( m _ { 1 } )$ and $c _ { 2 } =$ $H E _ { h k _ { 2 } } ( m _ { 2 } )$ , (c1+c2)modM S is equal to $H E _ { h k } ( m _ { 1 } + m _ { 2 } )$ where $h k { = } h k _ { 1 } { + } h k _ { 2 }$ .

Pseudorandom permutation (PRP): A pseudorandom permutation function $f \colon H \times P \  \ P$ is a pseudorandom permutation if given a fixed PRP key $k _ { i }$ belongs to $H ,$ , the input-output behavior of a random instance of $f$ is ”computationally indistinguishable” from that of a random permutation on a domain P . In this paper, we assume $P$ is [0, 2r] where r is a parameter determined at initialization.

# IV. NETWORK AN ADVERSARY MODELS

# A. System model

In this paper, we consider a wireless sensor network composed of a BS located at the center of the physical area and a large number of sensor nodes around it. Each sensor node monitors its direct environment and can generate sensed data. We assume that clocks on different sensors can be efficiently calibrated [16] and each sensed data is in the range [0, U] [6]. The network manager can require BS to collect data.

![](images/8b728c0ffd3c2304401f4f2ddb0e32f4760a60340fffc7e722cc0084efce7410.jpg)



Figure 1.

In practice, sensor nodes are often organized as one or multiple long routes originated from BS and extended hop by hop to the boundary of the physical area [15]. In this study, we assume that all the nodes are organized as a collection tree which consists of a root BS and $Q$ sub trees. Each of the sub trees consists of $N$ sensor nodes that form a multi-hop route originated from BS. Given a sub tree, we denote its N nodes as $u _ { 1 } , u _ { 2 } , \cdots , u _ { N }$ . For a node $u _ { j } ,$ the index $j$ represents the hop numbers from BS to $u _ { j }$ . We use the set $\left\{ u _ { q } \right\} _ { q = j + 1 } ^ { N }$ to present all the downstream nodes of uj and Zj+1 = -Nq=j $u _ { j }$ $\begin{array} { r } { Z _ { j + 1 } = \sum _ { q = j + 1 } ^ { N } \hat { \mathbf { \Omega } } . } \end{array}$ +1 1 to present the size of the set. Also, we call $u _ { N }$ leaf node and the remainder nodes from $u _ { N - 1 } ~ \mathrm { { t o } } ~ u _ { 1 }$ intermediate nodes. To collect data, BS first broadcasts a request command and the collection process is proceeded on all the sub trees concurrently. In each sub tree, data are transferred along the order: $u _ { 1 }  u _ { 2 }  \cdot \cdot \cdot  u _ { N }$ . Figure 1 shows an example of a collection tree which has three sub trees, each containing three nodes. We assume that in a sub tree, each node $u _ { j }$ knows its index $j ,$ , direct parent and direct child.

# B. Adversary model

We consider a general adversary with passive and active abilities to explore the data privacy of sensor networks. In particular, we consider:

• The adversary can eavesdrop on a communication link between two sensor nodes and try to extract useful data from it. In this study, we assume that the adversary has strong ability to launch eavesdropping attack, i.e., the adversary knows the topology of the collection tree and can adaptively select any links to eavesdropping.

• The adversary can compromise a subset of sensor nodes. After compromising several nodes, the adversary can immediately read the sensed data and all the secure materials stored in them. More seriously, the adversary can control them to receive messages from other legitimate nodes and uses the acquired secure materials to recover the sensed data from these messages. Different with the assumption of eavesdropping attack, we assume that the adversary cannot adaptively select any number of nodes to compromise as the operation of compromising is much harder than eavesdropping.

# V. SCHEME DESIGN

In this section, we describe the concrete design of our two privacy-preserving schemes. In both of our two schemes, each node shares a PRP key with BS and uses its PRP key to generate a data report from its sensed data. An intermediate node receives data reports from its downstream nodes, compresses them as well as its own data report to generate a compressed data report. On the other hand, as BS knows these PRP keys, it can recover the sensed data from the compressed data reports. Also, we differentiate four versions of data reports in a data collection process. ${ r o } ^ { \prime }$ is an original data report which is directly generated from a sensed data. If ro- is encrypted, we term it as ero- . ro is a compressed data report which is generated from two or more original data reports. If ro is encrypted, we term it as ero.

# A. Our first scheme: lightweight private data collection

In our first scheme, the data privacy partially relies on the nature of CS technique. By using CS technique, each sensor uses its sensed data to generate a data report which can be compressed in-network. We observe that once several data reports are compressed, the compression itself can provide a potential to hide the underlying data reports. By further analysis, we find that this potential can largely restrict compromising attack but cannot prevent eavesdropping attack. The reason is that as the adversary can adaptively select links to eavesdrop, it may eavesdrop several links in a clever manner and uses the eavesdropped messages to decompose the compressed data reports. This motivates us to use symmetric encryption to resist eavesdropping attack and relies on the nature of CS technique to resist compromising attack. We present the design of this scheme as follows:

Step 1. Initialization Prior to network deployment, BS sets up system parameters for each sub tree as follows:

(1) BS generates a PRP key $k _ { i }$ for each node ui and distributes $k _ { i }$ to $u _ { i } . \ k _ { i }$ is used for $u _ { i }$ to generate its data report.   
(2) For each two neighbor nodes: $u _ { i }$ and $u _ { i + 1 } , 1 { \le } i { \le } N { - } 1$ , BS distributes a symmetric key $s k _ { i i + 1 }$ to $u _ { i }$ and $u _ { i + 1 }$ . After the distribution, $u _ { i }$ and $u _ { i + 1 }$ can use $s k _ { i i + 1 }$ to securely exchange messages.

(3) As BS knows the total number N of sensor nodes in a sub tree, it can determine dimension degree M and other parameters of CS.

Step 2. Query dissemination When BS wants to collect data, it first generates a random number R which is different in each query. BS then broadcasts the query message $m =$ (query request, R, M ) to the network. After broadcasting, each node records m. As the data collection is performed on sub tree basis, we consider the collection process in a single sub tree in the following.

Step 3. Data report at leaf node $\mathbf { \boldsymbol { \mathscr { u } } } _ { N }$ After receiving $m ,$ $u _ { N }$ begins to send its data report as follows:

(1) $u _ { N }$ generates a sensed data $d _ { N }$ and establishes a data report $r o _ { N } ^ { \prime }$ as follows: $u _ { N }$ derives a set of random numbers {aqN } Mq=1 $\left\{ a _ { q N } \right\} _ { q = 1 } ^ { M }$ where $a _ { 1 N } { = } f _ { k _ { N } } ( R )$ and for $q = 1$ to $M - 1 , a _ { q + 1 N } \dot { = } f _ { k _ { N } } \big ( a _ { q N } \big )$ . Then, uN computes $r o _ { N } ^ { \prime }$ as: $r o _ { N } ^ { \prime } = \{ a _ { 1 N } d _ { N } , a _ { 2 N } d _ { N } , \cdot \cdot \cdot , a _ { M N } d _ { N } \}$ .   
(2) $u _ { N }$ uses $s k _ { N N - 1 }$ to generate a symmetric encryption $e r o _ { N } ^ { \prime } { = } E n c _ { s k _ { N N - 1 } } ( r o _ { N } ^ { \prime } )$ and transmits it to $u _ { N - 1 }$ .

Step 4. Data compression at each intermediate node $u _ { j } ( N - 1 \leq j \leq 1 ) u _ { j }$ receives a message from its child $u _ { j + 1 }$ and decrypts it using the shared private key. Suppose $u _ { j }$ has obtained a compressed data report $r o _ { j + 1 }$ from its child $u _ { j + 1 } ( r o _ { N } ^ { \prime }$ when $u _ { j + 1 }$ is $u _ { N } )$ , it generates a new compressed data report $r o _ { j }$ as follows:

(1) $u _ { j }$ generates its own data report $r o _ { j } ^ { \prime }$ as follows: $u _ { j }$ derives a set of random numbers $\left\{ a _ { q j } \right\} _ { q = 1 } ^ { M }$ where $a _ { 1 j } { = } f _ { k _ { j } } ( R )$ and for q=1 to $M \mathrm { - } 1 , a _ { q + 1 j } = f _ { k _ { j } } ( \dot { a } _ { q j } )$ . Then, $u _ { j }$ sets ro-j as: $r o _ { j } ^ { \prime } = \{ a _ { 1 j } d _ { j } , a _ { 2 j } d _ { j } , \cdot \cdot \cdot , a _ { M j } d _ { j } \}$ .   
$u _ { j }$ $r o _ { j + 1 } \quad \mathrm { t o }$ $\begin{array} { l l l } { { r o _ { j } { = } \{ { \sum _ { q = j + 1 } ^ { N } } { { a _ { 1 q } } } { d _ { q } } { + } { a _ { 1 j } } } { d _ { j } } , }  & { { \cdots , } } & { { \sum _ { q = j + 1 } ^ { N } a _ { M q } d _ { q } } } \\ { { a _ { M j } d _ { j } \} . } } \end{array} ~ + \nonumber$ N   
(3) $u _ { j }$ uses $s k _ { j j - 1 }$ to generate a symmetric encryption $e r o _ { j } { = } E n c _ { s k _ { j j - 1 } } ( r o _ { j } )$ and sends it to $u _ { j - 1 }$ .

Step 5. Data recovery Finally, BS decrypts ero1 to get a compressed data report $r o _ { 1 }$ from $u _ { 1 } . \ r o _ { 1 }$ can be presented as:

$$
r o _ {1} = \left( \begin{array}{c c c} a _ {1 1} & \dots & a _ {1 N} \\ \dots & \dots & \dots \\ a _ {M 1} & \dots & a _ {M N} \end{array} \right) \times \left( \begin{array}{c} r o _ {1} \\ \dots \\ r o _ {N} \end{array} \right)
$$

For each $u _ { i } .$ , BS uses $k _ { i }$ to derive $\left\{ a _ { q i } \right\} _ { q = 1 } ^ { M }$ . In this way, BS can get the full sensing matrix A. As each element $a _ { q i }$ of A is generated by the PRR function $f , A$ is a random matrix. BS can then recover the precise data vector $d { = } ( d _ { 1 } , d _ { 2 } , \cdots$ , $d _ { N } )$ by using CS. BS does the same thing to recover d for each sub tree. As a result, all the sensed data are recovered.

# B. Our second scheme: privacy-enhanced data collection

In our second scheme, data reports are encrypted at each sensor node before sending out. Such a construction largely enhances the data privacy as the adversary cannot obtain the data reports unless it knows the encryption key.

Furthermore, to ensure that the encrypted data reports can still be compressed at intermediate nodes, we propose to use additively homomorphic encryption, which allows direct compression among ciphertexts without decryption.

Step 1. Initialization Prior to network deployment, BS sets up system parameters for each sub tree as follows:

(1) BS generates a PRP key $k _ { i }$ for each node $u _ { i }$ and distributes $k _ { i }$ to $u _ { i } . \ k _ { i }$ is used for $u _ { i }$ to generate its data report.   
(2) BS generates a homomorphic encryption key $h k _ { i }$ for each node $u _ { i }$ and distributes $h k _ { i }$ to $u _ { i }$ for encryption. BS also securely saves each $h k _ { i }$ in its database.   
(3) As BS knows the total number N of sensor nodes in a subtree, it can generate dimension degree M and other parameters of CS.

Step 2. Query dissemination BS generates a random number R and broadcasts query message $m = ( q u e r y$ request, R, M ). Also, we consider the collection process in a single sub tree in the following.

Step 3. Data report at leaf node $\mathbf { \boldsymbol { \mathscr { u } } } _ { N }$ When receiving m, uN begins to send its data report as follows:

(1) $u _ { N }$ generates a data $d _ { N }$ and establishes $r o _ { N } ^ { \prime } { = } \{ a _ { 1 N } d _ { N }$ $a _ { 2 N } d _ { N } , \allowbreaks \cdot \cdot , a _ { M N } d _ { N } \rbrace$ the same as the first scheme.   
(2) $u _ { N }$ then uses $h k _ { N }$ to encrypt $r o _ { N } ^ { \prime }$ as an encrypted version: ero $\mathrm { , } _ { N } \mathrm { = } \{ H E _ { h k _ { N } } ( a _ { 1 N } d _ { N } ) , H E _ { h k _ { N } } ( a _ { 2 N } d _ { N } )$ , $\qquad \cdot \cdot \cdot , H E _ { h k _ { N } } ( a _ { M N } d _ { N } ) \}$ and forwards $e r o _ { N }$ to its parent $u _ { N - 1 }$ .

Step 4. Data compression at intermediate node $u _ { j } ( N - 1 \ \leq \ j \ \leq \ 1 )$ When $u _ { j }$ receives an encryption $e r o _ { j + 1 }$ of a compressed data report from its child $u _ { j + 1 } ( e r o ^ { \prime } _ { N }$ when $u _ { j + 1 } \mathrm { i s } u _ { N } )$ , it generates a new encryption $e r o _ { j }$ of a compressed data report as follows:

(1) uj generates its own data report $\begin{array} { r } { r o _ { j } ^ { \prime } { = \{ a _ { 1 j } d _ { j } , a _ { 2 j } d _ { j } , \cdot \cdot \cdot } }  \end{array}$ , $a _ { M j } d _ { j } \}$ the same as the first scheme. $u _ { j }$ then uses $h k _ { j }$ to encrypt ro-j as: $e r o _ { j } ^ { \prime } { = } \{ H E _ { h k _ { j } } ( a _ { 1 j } d _ { j } ) , H E _ { h k _ { j } } ( a _ { 2 j } d _ { j } )$ , $\quad \cdots , H E _ { h k _ { i } } ( \bar { a } _ { M j } d _ { j } ) \big \}$ .

(2) $u _ { j }$ adds up $e r o _ { j + 1 }$ and $\boldsymbol { e r o } ^ { \prime } { \boldsymbol { j } }$ to generate $e r o _ { j }$ as:

$$
e r o _ {j} = \{H E _ {h k} ((\sum_ {q = j + 1} ^ {N} a _ {1 q} d _ {q}) + H E _ {h k _ {j}} (a _ {1 j} d _ {j}))) m o d M,
$$

$$
\dots , H E _ {h k} \left(\left(\sum_ {q = j + 1} ^ {N} a _ {M q} d _ {q}\right) + H E _ {h k _ {j}} \left(a _ {M j} d _ {j}\right)\right) \text {mod} M \}
$$

$$
= \left\{H E _ {h k ^ {\prime}} \left(\left(\sum_ {q = j} ^ {N} a _ {1 q} d _ {q}\right), \dots , H E _ {h k} \left(\sum_ {q = j} ^ {N} a _ {M q} d _ {q}\right) \right. \right\}
$$

$\scriptstyle h k = \sum _ { q = j + 1 } ^ { N } h k _ { q }$ and $h k ^ { \prime } { = } h k { + } h k _ { j }$

$u _ { j }$ sends out $e r o _ { j }$ to its parent $u _ { j - 1 }$ . The parent does the same thing as $u _ { j }$ to generate data and finally, BS receives an encryption $e r o _ { 1 }$ from $u _ { 1 }$ .

computes Step 5. Data recovery When receiving $\scriptstyle h k = \sum _ { i = 1 } ^ { N } h k _ { i }$ to decrypt $e r o _ { 1 }$ 1and then uses all $e r o _ { 1 }$ , BS first $k _ { i }$ to recover A as described before. After that, BS can operate similarly with the first scheme to get the original data $d =$ $\{ d _ { 1 } , d _ { 2 } , \dots , d _ { N } \}$ . BS does the same thing to recover d for each sub tree. As a result, BS can obtain all the sensed data in WSN.

# VI. SECURITY ANALYSIS

In this section, we analyze the privacy properties of our two schemes. Due to the limited space, we omit some details of the analysis procedure.

# A. Security analysis of the first scheme

Compromising-resistance. In our system model, as data reports are forwarded from leaf nodes toward BS, the adversary can only control compromised nodes to capture the data reports of their downstream nodes. Our first scheme can guarantee that the adversary can only get restricted data reports of its downstream nodes. Generally, we differentiate two types of the compromising attacks: single node compromising and multi node compromising.

1) Single node compromising: In this attack, the adversary compromises only one node and controls it to capture data reports of its downstream nodes. Suppose the adversary selects a sub tree and compromises one node of it, there are three cases:

• Case 1. Compromising a leaf node $u _ { N } \colon \mathrm { A s } \ u _ { N }$ is a leaf node and has no child, the adversary controlling $u _ { N }$ cannot capture any data reports of other nodes.

• Case 2. Compromising an intermediate node $u _ { N - 1 } .$ By controlling $u _ { N - 1 }$ , the adversary can capture the original data report $r o _ { u _ { N } } ^ { \prime }$ from uN to infer $d _ { N }$ . In this case, we show that the adversary can fix a set which contains $d _ { N }$ with high efficiency. The reason is that we can treat $r o _ { N } ^ { \prime } { = } ( a _ { 1 N } d _ { N }$ , $a _ { 2 N } d _ { N } , \cdot \cdot \cdot , ~ a _ { M N } d _ { N } )$ as a linear equation system with the number of unknowns larger than the number of linear equations. Therefore, the unique solution of this system does not exist. As a result, $d _ { N }$ is hidden in the set of all the potential solutions. For the adversary, the lower bound of computation complexity to fix this set is $M U$ in the worst case. In real applications, the range $[ 0 , U ]$ of the sensed data is often several thousands. As a result, it is efficient for the adversary to find this set.

• Case 3. Compromising an intermediate node $u _ { j } \ ( I \leq j \leq$ $N { - } 2 ) { : }$ : By controlling a node $u _ { j }$ , the adversary can capture the compressed data report $r o _ { j + 1 }$ from its child $u _ { j + 1 }$ . As $r o _ { j + 1 }$ s the data reports of all the (note that we term the si $u _ { j }$ $\left\{ u _ { q } \right\} _ { q = j + 1 } ^ { N }$ $\left\{ u _ { q } \right\} _ { q = j + 1 } ^ { N }$ as $Z _ { i + 1 } )$ , the adversary can use $r o _ { j + 1 }$ to infer the knowledge of their sensed data $d / = \{ d _ { i + 1 } , d _ { i + 2 } , \dotsb , d _ { N } \}$ . In this case, we show that d is hidden in a set and it is infeasible for the adversary to fix this set. Specifically, the captured $r o _ { j + 1 }$ can be treated as a linear equation system. The total number of unknowns are $( M { + } 1 ) ~ Z _ { j + 1 }$ while the total number of linear equations is M . Therefore, the unique solution of this system does not exist. As a result, d is hidden in the set of all the potential solutions. For the adversary, the lower bound of computation complexity to find this set is $2 ^ { r ( M Z _ { j + 1 } - M ) } -$ + $U ^ { Z _ { j + 1 } }$ in the worst case.

2) Multi node compromising: The adversary can compromise multiple nodes and control them to capture multiple data reports. Suppose the adversary chooses multiple nodes to compromise, there are two cases:

• Case 1. The adversary compromises multiple nodes in a single sub tree: For simplicity, we only analyze the situation where two intermediate nodes are compromised. The more complex situations are analogous. Suppose the adversary compromises two intermediate nodes $u _ { i }$ and $u _ { j } ( N \cdot$ - $2 { > } j { > } i { > } 0 )$ and thus, captures two data reports $r o _ { u _ { i + 1 } }$ and $r o _ { j + 1 }$ from their children. There are two situations. Firstly, the adversary can separately use $r o _ { i + 1 }$ and $r o _ { j + 1 }$ to infer the sensed data $\{ d _ { i + 1 } , \ d _ { i + 2 } , \ \cdot \cdot \cdot , \ d _ { N } \}$ and $\{ d _ { j + 1 } , \ d _ { j + 2 } ,$ , $\cdots , d _ { N } \}$ contained in $r o _ { i + 1 }$ and $r o _ { j + 1 }$ respectively. This situation is similar to case 3 of single node compromising. Secondly, the adversary can jointly use $r o _ { i + 1 }$ and $r o _ { j + 1 }$ to acquire additional advantage. In particular, the adversary can subtract $\scriptstyle r o _ { j + 1 } = \sum _ { q = i + 1 } ^ { j } r o _ { q } ^ { \prime }$ $r o _ { i + 1 }$ by $r o _ { j + 1 }$ contains the sensed data . The subtraction result $\{ d _ { i + 1 } , \ d _ { i + 2 } . $ $\scriptstyle r o = r o _ { i + 1 } -$ $\cdots , d _ { j } \}$ . The adversary can thus infer $\{ d _ { i + 1 } , d _ { i + 2 } , \cdot \cdot \cdot , d _ { j } \}$ from ro. We analyze the advantage of the adversary in this situation with different values of i and $j$ and we find that: (1) when $\scriptstyle j = i + 1$ , the adversary cannot get additional knowledge, (2) when $\scriptstyle j = i + 2 :$ this case is similar with the case 2 of single node compromising to get a small set of values which contains $d _ { i + 1 }$ and (3) when $j { = } i { + } \beta \ ( 3 { \leq } \beta { \leq } N )$ , this case is similar with the case 2 of single node compromising where the adversary compromises the intermediate node $u _ { N - \beta + 2 }$ in a sub tree.

• Case 2. The adversary compromises multiple nodes in multiple sub trees: For simplicity, we also analyze the situation with two nodes. The more complex situations are analogous. Suppose the adversary receives two data reports from the children of the two compromised nodes. However, as the two nodes do not belong to the same sub tree, the adversary cannot subtract the two data reports and thus cannot gain additional advantages by jointly using the two data reports. Furthermore, uniting them into a linear system of equations will lead the numbers of unknowns $a _ { j q }$ increasing two times, providing no advantage for the adversary to infer the sensed data.

Eavesdropping-resistance The resistance of eavesdropping attack is immediate. As all the data reports are transmitted in encryption, the adversary can only acquire encrypted messages by eavesdropping any communication link. On the other hand, it is still interesting to show why the nature of CS technique cannot resist eavesdropping attack. Suppose now all the data reports are transmitted without encryption. If the adversary wants to infer the knowledge of a sensed data $d _ { j }$ of an intermediate node $u _ { j } \ ( 1 \leq j \leq N - 2 )$ , it can eavesdrop the links between $u _ { j }  u _ { j + 1 }$ and $u _ { j }  u _ { j - 1 }$ to capture two compressed data reports ro-uj+1 $r o _ { u _ { j + 1 } } ^ { \prime }$ and $r o _ { j } ^ { \prime }$ respectively. The adversary can then compute the original data report $r o _ { j }$ of $u _ { j } \colon r o _ { j } { = } r o _ { j } ^ { \prime } – r o _ { j + 1 } ^ { \prime }$ . From $r o _ { j }$ , the adversary can efficiently fix a set of values that contains the sensed data $d _ { j }$ as in the case 2 of single node compromising.

# B. Security analysis of the second scheme

Compromising-resistance we also differentiate two types of compromising attacks: Single node compromising and Multi node compromising.

1) Single node compromising: Suppose the adversary compromises a node $u _ { j }$ in a sub tree, the adversary can receive an encryption $e r o _ { j + 1 }$ from $u _ { j + 1 }$ . As the adversary does not know the encryption key hk, he cannot decrypt $e r o _ { j + 1 }$ .

2) Multi node compromising: On the other hand, the adversary can compromise multiple nodes to launch attacks with collusion. By controlling multiple compromised nodes, the adversary can receive a set of encryptions. Contrary to the first scheme, the adversary cannot use the subtract operation on this set no matter whether the compromised nodes are belonging to the same sub tree. This is because the additively homomorphic encryption only supports addition operations on the encryptions. As a result, combining multiple encryptions from multiple nodes cannot help the adversary to decrease the computation complexity. In fact, to decrypt an encryption $e r o _ { j + 1 }$ received from a node $u _ { j + 1 }$ , the adversary has to compromise all the nodes in $\{ u _ { q } \} _ { q = j + 1 } ^ { N }$ to recover the key $\scriptstyle h k = \sum _ { q = j + 1 } ^ { N } h k _ { q }$ .

Eavesdropping-resistance As all the data reports are under additively homomorphic encryption before forwarding, eavesdropping on any communication link can only reveal encrypted versions of them. The advantage of the adversary to recover the underlying data reports is equal to breaking the additively homomorphic encryption, which is computational infeasible [4].

# VII. PERFORMANCE EVALUATION

In this section, we compare the performance of basic encryption scheme, private data aggregation and our schemes.

# A. Accuracy

Both basic encryption scheme and our schemes achieve accuracy as individual sensed data can be recovered at BS. The network manager can then use these sensed data to compute any aggregate statistic. By using private data aggregation, however, only an aggregation result can be recovered at BS. The utility of the aggregation result is limited in two folds. Firstly, the aggregation result can only support limited types of aggregate statistics. Secondly, the acquirement of each supported aggregate statistic requires multiple aggregation operations over the whole sensor network, which is energy consuming if the network manager wants to acquire multiple aggregate statistics.

# B. Transmission efficiency

We evaluate the transmission efficiency of the three schemes according to two criteria: energy balance and overall energy consumption. For energy balance, we compare the data sent by different nodes in each of the three schemes. For overall energy consumption, we use the bits of forwarding data to measure the performance of the three schemes. Note that in our system model, the data collection is performed in each sub tree independently. As a result, we will also compare the performance of the above schemes in sub tree basis.

Energy balance The energy balances of the three schemes are analyzed as follows:

• Basic encryption scheme: In this scheme, each node needs to forward the encryptions of all the sensed data generated from its downstream nodes as well as itself. In particular, the node $u _ { j } ~ ( 1 { \leq } j { \leq } N )$ needs to forward $( N { - } j { + } 1 )$ encryptions. The result reflects a large amount of communication load among sensors with different indexes. In the extreme case, the leaf node $u _ { N }$ only forwards one encryption and the root node $u _ { 1 }$ needs to forward N encryptions. As a result, the nodes closer to BS have to send significantly larger amounts of data than downstream nodes.   
• Private data aggregation: In private data aggregation, the encrypted sensed data are aggregated at each intermediate node. As a result, each node sends an encryption no matter its location. As opposed to the basic encryption scheme, the energy consumption per node is equal.   
• Our schemes: In both of our two schemes, data reports can be compressed in each intermediate node and each node only sends an encrypted compressed data report no matter its location. As a result, the transmitted data per node is equal. In the first scheme, each node needs to transmit one symmetric encryption and in the second scheme, each node needs to transmit M homomorphic encryptions.   
Overall energy consumption We assume that a sensed data $d _ { j }$ is $\mathrm { ~ a ~ } r ^ { \prime }$ length bit string and a random number $a _ { i j }$ is a r length bit string. We choose the symmetric encryption proposed in [10] to instantiate the basic encryption scheme and our first scheme. The overall energy consumption of the three schemes are analyzed as follows:   
• Basic encryption scheme: In this scheme, a symmetric encryption of a sensed data generated at a node will be forwarded to BS along the path from that node to the root. As a result, the symmetric encryption generated at $u _ { j } \ ( 1 { \leq } j { \leq } N )$ is forwarded j hops. The total bits of forwarded data over the whole sub tree is thus $N ( N + 1 ) r ^ { \prime }$ .   
• Private data aggregation: In this scheme a node $u _ { j }$ $( 1 { \le } j { \le } N )$ forwards one aggregated data to its parent $u _ { j - 1 } .$ As a result, the bits of forwarded data over the whole sub tree is $N ( l o g _ { 2 } N { + } r ^ { \prime } )$ .   
• Our schemes: In our first scheme, each node sends a symmetric encryption. As a result, the bits of forwarded data over the whole sub tree is $N ( M ( l o g _ { 2 } N + r ^ { \prime } + r ) + r ^ { \prime } )$ . In our

![](images/2947b38480d8737de410b4a6c854b4d65fd9ad216af0b2d49b3b94263e8d7314.jpg)



(a)

![](images/2ef40ce840a2aa5ee90b1ecb676bd1bfdac6115551d39dd2df0456eaa9b4cb67.jpg)



(b)

![](images/0069d27b4bfa69d5ba172c90650cbdff06387dedd7a30dbf3e0c4779c637a02b.jpg)



(c)

![](images/f8533ee451b00acb11be95bd1aeac284fc0402d7602fcd95cb3525e98a39a405.jpg)



(d)   
2. Simulation result

second scheme, each node sends a homomorphic encryption. As a result, the bits of forwarded data over the whole sub tree is $N M ( l o g _ { 2 } N + r ^ { \prime } { + } r )$ .

# C. Simulation result

We further compare our schemes with basic encryption and private data aggregation through simulation. The accuracy of our schemes is guaranteed by the CS technique which shows that the compressed data can be recovered with a precision close to one if M is large enough. In real application, the value of M is based on the physical characteristic of the sensing area and the kind of collected data. In this paper, we select the value of M based on [13], which shows that $\scriptstyle { M = 0 . 0 5 N }$ (recall N is the size of a sub tree) is large enough to recover the temperature data of ocean sensed by sensors [14] with a precision over 98%. We also set $r ^ { \prime } { = } 1 6$ and $r { = } 3 2$ . The simulation is performed on two typical topologies: chain and tree. Chaintype sensor network consists of a single route and is often deployed along narrow areas like rivers, streets or tunnels. We formalize this topology as a collection tree with $Q { = } 1$ . Tree-type sensor network consists of multiple routes and is often deployed in wide areas such as round areas or square areas. We formalize this topology as a collection tree with $Q { > } 1$ . In this simulation, we set $Q { = } 1 0$ .

Energy balance: To evaluate the energy balance, we fix the parameter N of chain topology to 500 and tree topology to 100 and analyze the number of forwarded data items at nodes in different hops. Fig. 2 (a) and (b) show the energy balance of the three schemes on the chain topology and tree topology at different hops of a sub tree. We can see that the basic encryption suffers from energy unbalance since the forwarding number of data items increases linearly as the hop number decrease. On the other hand, the energy is fairly dispensed to each node in our two schemes and private data aggregation.

Overall energy consumption: To evaluate the overall energy consumption, we vary the parameter N of the chain topology from 100 to 500 and tree topology from 100 to 200. As the performance of our two schemes are same, we only use the second scheme for comparison. Fig. 2 (c) and (d) show the overall energy consumption of the three schemes on the chain topology and tree topology respectively as N changes. We can see that basic encryption scheme consumes much higher energy than our schemes and private data aggregation. Also, the overall energy consumption of our two schemes is slightly higher than private data aggregation. This coincides with the intuition that the private data aggregation sacrifices data accuracy. Further, our second scheme consumes higher energy than our first one. This is because the length of additive homomorphic encryption is longer than the symmetric encryption.

# VIII. CONCLUSION

In this paper, we thoroughly analyze the requirements of data collection in wireless sensor networks including accuracy, privacy and efficiency. We then propose two private data collection protocol to fulfill these requirements. We conduct comprehensive analysis and prove the correctness and efficiency of the proposed protocols.

# IX. ACKNOWLEDGMENT

We would like to thank the anonymous reviewers for their helpful and valuable comments. This work is supported in part by Nanyang Technological University NAP Grant M4080738.020.

# REFERENCES

[1] B. Przydatek, D. Song and A. Perrig, ”SIA: Secure Information Aggregation in Sensor Networks,” in Proc. of ACM SenSys, pages 255-265, 2003.   
[2] Y. Yang, X. Wang, S. Zhu and G. Cao, ”SDAP: A Secure Hopby-Hop Data Aggregation Protocol for Sensor Networks,” in Proc. of ACM MobiHoc, pages 356-367, 2006.   
[3] D. Wagner, ”Resilient Aggregation in Sensor Networks,” in Proc. of ACM Workshop on Security of Ad Hoc and Sensor Networks, pages 78-87, 2004.   
[4] C. Castelluccia, E. Mykletun and G. Tsudik, ”Efficient Aggregation of Encrypted Data in Wireless Sensor Networks,” in Proc. of Mobiquitous, pages 109-117, 2005.   
[5] W. He, X. Liu. H. Nguyen, K. Nahrstedt and T. Abdelzaher, ”Pda:Privacy-preserving data aggregation in wireless sensor networks,” in Proc. of IEEE INFOCOM, Pages 2045-2053, 2007.   
[6] T. Feng, C. Wang, W. Zhang and L. Ruan, ”Confidentiality Protection for Distributed Sensor Data Aggregation,” in Proc. of IEEE INFOCOM, Pages 56-60, 2008.

[7] R. G. Baraniuk, ”Compressive sensing,” IEEE Signal Processing Magazine, Vol.24(Issue 4): Pages 118-121, July, 2007.   
[8] E. J. Candes, M. B. Wakin, ”An introduction to compressive sampling,” IEEE Signal Processing Magazine, Vol.25(Issue 2): Pages 21-30, March, 2008.   
[9] D. L. Donoho, ”Compressed sensing,” IEEE Transactions on Information Theory, Vol.52(Issue 4): Pages 1289-1306, April, 2006.   
[10] O.Goldreich, ”Foundations of Cryptography”.   
[11] J. Haupt, W. U. Bajwa, M. Rabbat, and R. Nowak, ”Compressed sensing for networked data,” IEEE Signal Processing Magazine, Vol.25(Issue 2) Pages 92-101, March, 2008.   
[12] C. Luo, F. Wu, J. Sun and C. Chen, ”Compressive Data Gathering for Large Scale Wireless Sensor Networks,” in Proc. of ACM MobiCom, Pages 145-156, 2009.   
[13] NBDC CTD data. http://tao.noaa.gov/refreshed/ctd delivery.php.   
[14] S. Tilak, N. B. Abu-Gahazaleh and W. Heinzelman, ”Infrastructure tradeoffs for sensor networks,” in Proc. of ACM WSNA, Pages 49-58, 2002.   
[15] Z. Li, M. Li, J. Wang and Z. Cao, ”Ubiquitous data collection for mobile users in wireless sensor networks,” in Proc. of IEEE INFOCOM, Pages 2246-2254, 2011.   
[16] Z. Li, W. Chen, C. Li, M. Li, X. Li and Y. Liu, ”FLIGHT: Clock Calibration Using Fluorescent Lighting,” in Proc. of ACM MobiCom, Pages 329-340, 2012.   
[17] J. Chen, W. Xu, S. He, Y. Sun, P. Thulasiramanz and X. Shen, ”Utility-Based Asynchronous Flow Control Algorithm for Wireless Sensor Networks,” IEEE Journal on Selected Areas in Communications, Vol.28(Issue 7) Pages 1116-1126, September, 2010.   
[18] M. Li, W. Cheng, K. Liu, Y. He, X. Li and X. Liao, ”Sweep Coverage with Mobile Sensors,” IEEE Transactions on Mobile Computing, Vol. 10(Issue 11) Pages 1534-1545, November, 2011.   
[19] Y. Zhu, L. M. Ni, ”Probabilistic Approach to Provisioning Guaranteed QoS for Distributed Event Detection,” in Proc. of IEEE INFOCOM, Pages 592C600, 2008.   
[20] Y. Rachlin, D.Baron, ”The Secrecy of Compressed Sensing Measurements,” in Proc. of Annual Allerton Conference, Pages 813-817, 2008.   
[21] A. Orsdemir, H.O.Altun, G.Sharma and M.F.Bocko, ”On The Security and Robustness of Encryption via Compressed Sensing,” in Proc. of IEEE MILCOM, Pages 1-7, 2008.