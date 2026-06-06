# DS-PPS: A Practical Framework to Guarantee Differentiated QoS in Terabit Routers with Parallel Packet Switch

Lei Shi† , Bin Liu† , Wenjie Li† , Beibei Wu† , Yunhao Liu‡

† Department of Computer Science and Technology Tsinghua University, Beijing, 100084, P.R. China {shijim, lwjie00, wbb02}@mails.tsinghua.edu.cn liub@tsinghua.edu.cn

‡ Department of Computer Science Hong Kong University of Science and Technology Clear Water Bay, Hong Kong, P.R. China liu@cs.ust.hk

Abstract—Parallel Packet Switch (PPS) is used intensively in today’s terabit router to construct the switching fabric. Basic PPS equally deals with all of the traffic in order to achieve uniform load-balancing and high throughput, but it fails to support differentiated QoS. With the recent blooming of delaysensitive Internet traffic, such as the peer-to-peer live streaming and IPTV, differentiated QoS is becoming an urgent demand. In this paper, we propose a novel and practical framework, the Differentiated Service Parallel Packet Switch (DS-PPS), which supports three fundamental QoS features: guaranteed-delay (GD), guaranteed-bandwidth (GB) and best-effort (BE). By adaptively adjusting the number of switching planes offered to each QoS class, DS-PPS precisely controls the delay bounds of GD traffic and the drop precedence of GB traffic. We evaluate DS-PPS by extensive theoretical analyses and comprehensive simulations. Experimental results on a prototype implementation of the framework show that DS-PPS outperforms the basic PPS in three main aspects. First, the average delay of TCP short packet under full load is reduced by more than 94%. Second, the average delay of real-time traffic under full load is reduced by more than 82%. And third, the GB traffic of low drop precedence is guaranteed of nearly three times the throughput of high drop precedence at the hotspots. Significantly, our proposed DS-PPS framework is universal and scalable to support various kinds of emerging QoS-sensitive applications in multi-service terabit routers without any extra overhead.

Index Terms—Parallel Packet Switch, Differentiated QoS, Terabit Router.

# I. INTRODUCTION

Currently emerging bandwidth-cost applications, such as IPTV [7], E-Science [8], as well as the available multihundreds gigabit per second optical transmission technology, have ended the controversy over the need to deploy routers with capacity beyond 1Tb/s. They also bring the realistic challenge to the design of multi-terabit or even petabit core routers [5]. To build such routers, it is necessary to construct the terabit switching fabric with even larger capacity so that moderate speedup can be provided in order to guarantee switching performance.

Today, the capacity of an electronic switch is restricted by three key factors as follows: 1) the speed of the scheduling algorithm in Input-Queued (IQ) and Combined-Input-and-Output Queued (CIOQ) switch, or the memory bandwidth in Output-Queued (OQ) and shared-memory switch, 2) the speed of the serial data transmission link supported by the switching fabric’s interface, and 3) the number of pins that can be packaged on a single chip. While the ultra-fast scheduling algorithm in IQ/CIOQ switches is available by adopting deterministic off-line scheduling [12], frame-based scheduling [13] or pipelined scheduling [14], it is difficult, if not impossible, to scale a single switch beyond terabit capacity under state-of-the-art LVDS transmission and packaging technology [6]. Thus, practical designs of terabit switching fabric [3][4] are often composed of multiple lower-capacity switches. One popular solution is Parallel Packet Switch (PPS), in which switches are paralleled to resolve the above three bottlenecks.

Though in theory PPS can scale the switching capacity into infinity, it fails to support today’s Internet applications well as it does not support differentiated Quality of Service (QoS). For example, the real-time streaming services demand low delay bound, while the file transfer applications only require large bandwidth.

Due to the lack of processing ability and transmission bandwidth in core routers, deployment of differentiated QoS in PPS would be significant. In past years, two primary differentiated QoS frameworks have been proposed: the IntServ [9] and the DiffServ [10][11]. The IntServ provides the ability to guarantee per-flow QoS discipline, while DiffServ tries to deploy QoS on the per-class granularity. However, to achieve differentiated QoS in the PPS, both the IntServ and DiffServ are not appropriate. The IntServ is costly and impractical in maintaining per-flow status and designing fast flow-aware scheduling algorithms, while the DiffServ is inoperable since it offers little quantitative QoS disciplines for a practical implementation. Most commercial switches [15][16] adopt a cut version of DiffServ, where only strict priorities are provided by Class of Service (CoS) based scheduling.

![](images/8a61d70b2dcc4a25841cf2ccfde2615647c9c0c5f23df7beb21d7297e54a0419.jpg)  
Fig. 1: (a) The demultiplexer in DS-PPS. (b) The internal structure of a basic PPS. (c) The multiplexer in DS-PPS.

In this paper, we propose a novel QoS-driven measuringbased PPS framework, called the Differentiated Service Parallel Packet Switch (DS-PPS). It provides three fundamental QoS features: guaranteed-delay (GD), guaranteed-bandwidth (GB), and best-effort (BE). By adaptively adjusting the number of switching planes offered to each QoS class, DS-PPS precisely controls the delay bounds of GD traffic and the drop precedence of GB traffic. We evaluate DS-PPS by extensive theoretical analyses and comprehensive simulations as well as a prototype implementation.

The rest of the paper is organized as follows. Section II introduces some essential definitions and terminologies used throughout the paper. Section III presents the related works. Section IV presents the designs of DS-PPS framework. Section V analyzes the differentiated QoS guarantees of DS-PPS. Section VI presents a prototype implementation. Section VII evaluates the performance of this prototype by simulations. And finally, Section VIII concludes the work.

# II. DEFINITIONS AND TERMINOLOGIES

# A. PPS Structure

Figure 1.(b) shows a basic PPS with N ports. It is constructed in a 3-stage like topology. In the central stage, k identical N N× packet switches are paralleled. Each of these packet switches is called a switching plane. The first stage of PPS includes N demultiplexers. Each one is combined with an input port and connected to all k switching planes at the central stage. When a packet/cell arrives at the input port, the corresponding demultiplexer selects a plane by the loadbalancing algorithm and sends the packet/cell to the selected plane. Every input port operates at line rate R and each link to the central stage planes runs at the rate of $r = S _ { 1 } R / k$ to achieve 100% throughput while compensating for additional overheads by offering the speedup of S1. After the switching in the center stage, the traffic is aggregated at N output ports by the aggregating algorithm performed at the multiplexer of each output and sent to the output line. These N multiplexers compose the third stage of PPS.

Based on the basic PPS, many evolutions are introduced in recent studies and implementations. We categorize them as follows.

Centralized/Distributed PPS: The centralized PPS uses a central scheduler to compute matching for all the k central switches. Primitive centralized PPS segments the incoming cells into k identical slices and dispatches them uniformly into k central switches. Each switch performs the same scheduling synchronously. The advanced centralized PPS allows the central switches to operate asynchronously, but schedules them together. In contrast, the distributed PPS maintains one scheduler for each individual parallel switch and carries out distributed scheduling independently.

Centrally Buffered/Centrally Non-buffered PPS: The centrally buffered PPS uses buffered crossbar or sharedmemory structure to build the central packet switch, while the centrally non-buffered PPS adopts the non-buffered crossbar in the central switch. The parallel switches in the centrally buffered PPS can be IQ switch [2], OQ switch, CIOQ switch [18], or the crosspoint buffered switch [19], etc.

Input Buffered/Input Non-Buffered PPS: The input buffered PPS has coordination buffers at the demultiplexer of each input, so that the incoming packet/cell subscribed to the central plane by the load-balancing algorithm can wait until the corresponding link becomes idle. In contrast, the input non-buffered PPS must send the packet/cell out as soon as it arrives at the demultiplexer1 .

Cell-mode/Packet-mode PPS: We define packet as the variable-length IP packet arrived at the ingress, and define cell as the fixed-length segmentation processed in switch cores. Special modules are required to segment the original packet into cells before switching and reassemble them into the original one after switching. We call them the Segmentation And Reassembly (SAR) modules. The cell-mode PPS does not have SAR modules in it. It assumes that the packet is converted to cells outside the PPS. Thus, the load-balancing and aggregating algorithm works in a cell-by-cell manner. In contrast, the packet-mode PPS includes the SAR module in each switching plane, outside the cell switch. Hence, the loadbalancing and aggregating algorithm here works in a packetby-packet manner. We define external time slot as the time interval to transmit one cell at external line rate R, and internal time slot as the one to transmit one cell at internal line rate r.

![](images/fd137760e77d7bdbcf93e3573f17862941f4d90335d20a01f909025967a63d27.jpg)  
Fig. 2: (a) The cell VOQ in each switching plane. (b) The internal structure of each switching plane in DS-PPS. (c) The cell/packet OQ in each switching plane.

# B. Differentiated QoS Guarantees

In the DiffServ framework, the differentiated QoS requirements are defined as Per-Hop Behaviors (PHB) in the granularity of service aggregation. Although several PHB groups have been included in the framework, it does not give quantitative QoS disciplines. To make the service differentiations operable and accordant throughout the Internet, ITU-T publishes its QoS standard [17], i.e. aggregating QoS requirements to QoS class 0 to 5 with distinct parameters.

In this paper, our differentiated QoS definition tries to find an effective balance between the complexity and practicality. Such definition also makes it competent to fulfill the ITU-T QoS standard. Traffic here is classified into the following three QoS groups, and parameterized QoS classes are divided inside each group.

GD Group: The traffic belonging to this group requires statistical delay bound, as well as limited packet loss. It conforms to the EF PHB group in DiffServ. This group can be further divided into separate QoS classes according to the distinct and parameterized requirements at the delay bound. These classes correspond to QoS class 0-3 in the ITU-T standard.

GB Group: The traffic classified into this group requires limited packet loss only. It conforms to the AF PHB group in DiffServ. This group can be further divided into separate QoS classes according to the ranked drop precedence. These classes correspond to QoS class 4 in the ITU-T standard.

BE Group: The traffic with no QoS guarantee is classified into this group. The entire group corresponds to QoS class 5 in the ITU-T standard.

The confidence interval for the statistically guaranteed delay bound and throughput are set to be 99.9% and 99.999% respectively for evaluation purpose.

# III. RELATED WORKS

The PPS is derived from the Inverse Multiplexing for ATM (IMA) [33], and has been intensively studied in recent years [15][20]-[26]. The original motivation is to scale the switching capacity with available small-scale packet switches. Thus, centralized PPS [15] is initially adopted due to its simplicity. However, because of the bottleneck at the single scheduler and the need to synchronize all the k switches, the centralized PPS is not scalable. Later PPS designs employ distributed scheduling. In [25], the centrally buffered distributed PPS is introduced, which avoids building large buffers at line rate. Meanwhile, it is proved in [23] that the input non-buffered PPS requires the speedup of $k / { \Gamma k } / { 2 } \rceil$ to be stable, which therefore expedites the use of input buffered PPS. Other studies [20][22][24][26] focus on the load-balancing algorithm to minimize average cell delay, maximize overall throughput, and guarantee total cell order. In most approaches, resequencing buffers are required at the egress to guarantee the order of the departing cells and to reassemble them to the original packets. However, no theoretical upper bound on the buffer size is given. Moreover, the re-sequencing buffers can be competent only by using the costly non-FIFO structure.

The background of our work is that all previous approaches either do not support the differentiated QoS or are not practical for real implementations. The authors in [25] prove that the PPS can exactly mimic an OQ switch regardless of the nature of arriving traffic with speedup of $^ { 2 , }$ and provide a wide variety of QoS properties of OQ switch with speedup of 3. The emulation, however, assumes that the load-balancing algorithm is carried out based on the global on-line information of all k switches, which is impractical. Authors in [21] extend the work by emulating OQ switch with a fully distributed algorithm within a delay bound and without any speedup. The problem is that only OQ switch with FIFO discipline is emulated, and no differentiated QoS guarantee is provided. Other PPS designs inherit the CoS-based QoS feature from the parallel switching plane, but this method is not effective in supporting the more precise differentiated QoS guarantee as in Section II.B. Moreover, each plane would need to implement large numbers of costly priority queues in such structure.

# IV. DS-PPS FRAMEWORK

# A. Hardware Architecture

The top-level hardware architecture and mechanism of DS-PPS still follows the basic PPS shown in Fig. 1.(b) and defined in II.A. To avoid the centralized scheduling and large buffers running at the line rate, as well as the $k / { \Gamma k } / { 2 } \rceil$ lower bound of speedup, our DS-PPS adopts the distributed PPS structure with buffers in both input demultiplexers and the central switching planes. The line rate buffers in demultiplexers are kept small enough to be built on-chip such that most of the buffering happens at each parallel plane running approximately k times slower than line rate. Meanwhile, considering that when the line rate of terabit router increases to OC768, or even OC3092 in the future, the SAR module working at the wire speed becomes too costly and complex to build, the DS-PPS is designed to be packet-mode PPS.

The internal structures of the ingress demultiplexer and egress multiplexer of DS-PPS are shown in Fig. 1.(a) and Fig. 1.(c), respectively. The demultiplexer at each input port receives packets at line rate R. Each packet is first parsed in the Packet Dispatch Unit (PDU) to perform load-balancing based on the packet header and local information. The k FIFOs working at line rate, namely D-FIFOs, are built after the PDU to buffer the packets destined to k central planes. Each plane reads packets out of its corresponding D-FIFO at the rate of $r = S _ { 1 } R / k$ . Symmetrically in the multiplexer, k line-rate FIFOs, namely M-FIFOs, are implemented to buffer the packets coming from k central switches at rate r while counteracting the speedup. Next to these M-FIFOs, a scheduler in the multiplexer reads packets out and sends them to output link at line rate R.

We illustrate the structure of each switching plane of DS-PPS in Fig. 2.(b). CIOQ switch is used here because it has no memory bandwidth bottleneck and can emulate OQ switch with speedup of 2 [27]. This switch adopts Virtual Output Queue (VOQ) at the inputs to buffer cell and Output Queue (OQ) at the outputs to buffer cell/packet. The hierarchical structure of these cell VOQ and cell/packet OQ are as shown in Fig. 2.(a) and Fig. 2.(c). Inside each of them, three kinds of virtual sub-queues, called DS Queues (DSQ), are maintained, storing the cells of GD group, GB group and BE group, respectively. They are scheduled from the DSQ of GD group to BE group in a strict descending priority. Note that DS-PPS works in packet-mode, the SAR module in each plane is composed of two parts: one is the Input Segmentation Module (ISM) to segment packet to cells before the cell VOQ; and the other is the Output Reassembly Module (ORM) to reassemble cells into packet after the cell OQ. Since the cells of same packet could be interleaved at the arrival to ORM, Virtual Input Queued (VIQ) structure is employed here. Following ORM at each output port, a packet OQ is used to store congested packets in case of backpressure. We have more details on the scheduling algorithm used in each CIOQ switch in part F of this section.

# B. Load-Balancing Algorithm at Ingress

Like the basic PPS, the DS-PPS uses the load-balancing algorithm at the demultiplexer to dispatch packets into k central planes. However, the algorithm in this framework concerns the QoS class of each packet and works for both load-balancing and class-based traffic isolation to guarantee differentiated QoS.

The simplest QoS-class-based load-balancing algorithm is to aggregate the central switching planes into several static non-overlapped plane groups, and each group receives traffic of one specific class. This policy is named as the Static Assignment Policy (SAP). It achieves absolute traffic isolation, however, exposes three main drawbacks: 1) highly outputunbalanced traffic class will occupy too much switching planes to guarantee QoS, which degrades the overall throughput; 2) the excessive bandwidth after serving the highpriority class can not be shared by other low-priority classes; 3) the traffic fluctuations along the time axis can not be adapted with SAP.

To address these issues, we introduce the Dynamic Assignment Policy (DAP). The traffic with both same output port and QoS group is defined as a stream. There are totally 3N streams at each input according to our QoS definition in Section II.B. For each in the 2N streams belonging to GD and GB group, the central planes are divided into several nonoverlapped groups independently. The planes in each group receive packets of one specific class in the corresponding stream. The BE group is considered a single class, so there if no need to divide the planes for stream of it. To smooth the possible traffic fluctuation, these plane divisions are recalculated in a proper frequency based on the measurement results of on-line traffic. DAP avoids the drawbacks of SAP, but also eliminates the absolute traffic isolation, which is useful in providing stringent QoS guarantee.

In the DS-PPS framework, we combine SAP and DAP, which is called the Hierarchy Assignment Policy (HAP). It is illustrated in Fig. 3.

![](images/5270a89deeb004695f766484aefeaa7e7a608419025cf26be60f64f93b99aa90.jpg)



Fig. 3. The load-balancing algorithm HAP-LB at demultiplexer of DS-PPS. The packet is dispatched based on the combination of {destination port, QoS class}

Hierarchy Assignment Policy (HAP): Assuming that there are t classes that occupy bounded input/output bandwidth and need guaranteeing stringent QoS (criterion for static class). They are denoted as static class $H _ { I } , H _ { 2 } , . . . , H _ { t } { \in } \mathrm { G D }$ group. The other classes are dynamic classes, where m classes∈GD group, denoted as $L D _ { l } , L D _ { 2 } , . . . , L D _ { m } ,$ n classes∈GB group, denoted as $L B _ { l } , \ L B _ { 2 } , \ . . . , L B _ { n } ,$ and only one class falls into BE group, denoted as $L E _ { I }$ . The k central planes are divided into two groups: the Static Assignment Group (SAG), including the planes from $k { - } A S { + } I$ to $k ,$ and the Dynamic Assignment Group (DAG), the planes from 1 to $A D .$ The SAG is further partitioned into t sub-groups, denoted as SG1, SG2, …, SGt. The sub-group $S G _ { i }$ includes $A S _ { i }$ planes. The DAG is further partitioned by 2N different divisions. Each of the first N divisions partitions DAG into m sub-groups. The m subgroups at the jth division are denoted as $D G _ { _ 1 } ^ { j } , D G _ { _ 2 } ^ { j } , . . . ,$ $D G _ { _ m } ^ { j }$ . Sub-group $D G _ { i } ^ { j }$ has $A D _ { _ i } ^ { j }$ planes. Each of the second N divisions partitions DAG into n sub-groups. The n sub-groups at the $( j + N ) ^ { \circ } \mathbf { s }$ division are denoted as $B G _ { 1 } ^ { j } , B G _ { 2 } ^ { j } , . . . , B G _ { n } ^ { j }$ . Sub-group $B G _ { _ i } ^ { j }$ has $A B _ { i } ^ { j }$ planes. The above denotations satisfy

$$
A S + A D = k, \sum_ {i = 1} ^ {t} A S _ {i} = A S \tag {1}
$$

$$
\forall j \in [ 1, N ], \sum_ {i = 1} ^ {m} A D _ {i} ^ {j} = A D, \sum_ {i = 1} ^ {n} A B _ {i} ^ {j} = A D
$$

The detailed load-balancing algorithm used in DS-PPS is called the Hierarchy Assignment Policy Load Balancing (HAP-LB) algorithm. In HAP-LB, traffic of static class $H _ { i }$ is dispatched to planes in sub-group $S G _ { i } .$ , traffic of dynamic class $L D _ { i }$ with destination port $j$ to the planes in sub-group $D G _ { i } ^ { j }$ , traffic of dynamic class $L B _ { i }$ with destination port j to the planes in sub-group $B G _ { _ i } ^ { j }$ , and the traffic of dynamic class $L E _ { I }$ with destination port j to all the planes in DAG.

The load-balancing of the traffic with both the same class type and destination port to the specific plane sub-group uses the Surplus Round Robin (SRR) algorithm in [32]. Taking the traffic that belongs to static class $H _ { i }$ and also goes to output j as an example, the SRR algorithm assigns each plane in $S G _ { i }$ with a fixed Quantum of Service (QS), and a Deficit Counter (DC) initialized to zero. Packets are dispatched in a round robin fashion. When a plane in SGi is picked, its DC is increased by the QS of that plane. As long as the DC is positive, packets are sent continuously to the D-FIFO connected to this plane and the DC is decreased by the size of the transmitted packet. Once the DC becomes non-positive, the next plane in round robin order is selected. All the QSs associated with the static classes and dynamic classes of GD group are the same and determined off-line since fair loadbalancing is required here. The QSs associated with the dynamic classes of GB and BE group are recalculated on-line according to the changes of plane divisions.

In Figure 3, it is explicitly shown that the traffic sent to each D-FIFO is the aggregation of load-balancing of 3N streams for D-FIFO from 1 to $A S ,$ and the aggregation of N streams for D-FIFO from $A S { + } I$ to k. To achieve overall loadbalancing, a congestion bound $F B _ { D E M U X }$ is set at each D-FIFO. When the length of D-FIFO l increases beyond $F B _ { D E M U X } ,$ , plane l is jumped over in performing SRR algorithm for every stream. This modified algorithm is named as threshold SRR.

![](images/5ad44717f89319b2e2b46594749f24f1b0bf7f5798b9de299c7e9e80284bfa51.jpg)



Fig. 4. The multiplexer at output port j of DS-PPS.

# C. Traffic Measurement Mechanism at Egress

The plane divisions of DAG for dynamic classes are recalculated according to the traffic measurement results of every preset time cycle $T _ { m e } .$ . The measurement is carried out at the egress multiplexer of DS-PPS. Figure 4 shows the detailed mechanisms at output port j. There are two traffic counters at the output line of each switching plane in DAG, recording the data volume of packet arrivals of GD group and GB group respectively. In Fig. 4, the counters $T D _ { 1 } ^ { j } , T D _ { 2 } ^ { j } , . . . , T D _ { A D } ^ { j }$ are for the GD group, and the counters $T B _ { 1 } ^ { j } , \ T B _ { 2 } ^ { j } , \ \dots \ , \ T B _ { _ { A D } } ^ { j }$ are for the GB group. According to the HAP-LB algorithm, the total data volume of dynamic class $L D _ { i }$ and dynamic class $L B _ { i }$ that arrived at output port $j ,$ denoted as $D V _ { _ i } ^ { j }$ and $B V _ { _ i } ^ { j }$ , are given by

$$
D V _ {i} ^ {j} = \sum_ {l \in D G _ {i} ^ {j}} T D _ {l} ^ {j}, B V _ {i} ^ {j} = \sum_ {l \in D G _ {i} ^ {l}} T B _ {l} ^ {j} \tag {2}
$$

# D. Plane Division Calculation

The calculation algorithm of DAG runs by cycle $T _ { m e }$ as well. Some parameters and definitions of the algorithm are given first.

$S P _ { G D } ^ { i }$ : Speedup for class $L D _ { i }$ to guarantee its delay bound. Speedup is defined as the multiple of the provisioning bandwidth to the average of traffic arrival rate.

$R S P _ { G D } ^ { i }$ : Real speedup for class $L D _ { i }$ after calculation.

$S P _ { G B }$ : Speedup for dynamic classes of GB group to guarantee bandwidth. Assume that the drop precedence of these classes are $L B _ { n } , L B _ { n - l } , \ldots , L B _ { l } ,$ , in a descending order for priority.

$A S P _ { G B }$ : Average speedup provided for dynamic classes of

GB group after serving those of GD group.

The calculation procedure follows in two steps.

1) All the AD planes in DAG are partitioned for the dynamic classes of GD group. The number of planes assigned is proportionally to the rate of packet arrivals in the last measuring cycle. We have

$$
A D _ {i} ^ {j} = k \times \frac {D V _ {i} ^ {j} \times S P _ {G D} ^ {i}}{\sum_ {i = 1} ^ {m} \left(D V _ {i} ^ {j} \times S P _ {G D} ^ {i}\right)} \quad (3) \quad R S P _ {G D} ^ {i} = \frac {A D _ {i} ^ {j} \times r \times T _ {m e}}{D V _ {i} ^ {j}} \tag {4}
$$

If $R S P _ { G D } ^ { i } \ge S P _ { G D } ^ { i }$ , class $L D _ { i }$ is served with required speedup, otherwise the traffic of GD group is too heavy to be guaranteed. The residual output bandwidth in the lth plane after the first step, denoted as $R s d _ { l } ^ { j }$ , is calculated by $R s d _ { l } ^ { j } = \frac { R S P _ { _ { G D } } ^ { i } - 1 } { R S P _ { _ { G D } } ^ { i } } \times r$ , if plane l is assigned for class $L D _ { i }$ at output j.

2) The residual output bandwidth in AD planes is allotted to the dynamic classes of GB group. The maximal achievable average speedup for these classes is calculated by

$$
A S P _ {G B} = M A X \left(\frac {k \times r \times T _ {m e} - \sum_ {i = 1} ^ {m} D V _ {i} ^ {j}}{\sum_ {i = 1} ^ {n} B V _ {i} ^ {j}}, S P _ {G B}\right) \tag {5}
$$

If $A S P _ { _ { G B } } \geq S P _ { _ { G B } }$ , the speedup of all the classes in GB group can be guaranteed, otherwise only the classes with lower drop precedence are satisfied.

Initially, we set $P L B = 1 , i = 1$ . For class $L B _ { i } ,$ ,

$$
A B _ {i} ^ {j} = \operatorname{MIN} (C) \quad \text { if } \sum_ {l = P L B} ^ {P L B + C - 1} R s d _ {l} ^ {j} \geq \frac {B V _ {i} ^ {j} \times A S P _ {G B}}{T _ {m e}} \tag {6}
$$

Then j PLB PLB AB = + , i i = +1

If there is no minimum in (6), (7) works instead of (6),

$$
A B _ {i} ^ {j} = A D - P L B + 1 \tag {7}
$$

The second step finishes until i n = +1 or (7) works once.

The divisions of the DAG at output j start from plane STj. In DS-PPS, we set $S T _ { j } = [ ( j - 1 )$ mod $A D ) ] + 1$ . Figure 5.(a) and 5.(b) show the examples of the division inside DAG.

After calculation, the new division information is delivered to the demultiplexer at each input port, so that it will adopt the latest division in the HAP-LB algorithm. The change of the division, shown in Fig. 5.(c), is put into a special frame, and broadcast through the backward data path at one of the switching planes in SAG to all the input port. It is proved in Section V that the packet delay in planes of SAG is stringently bounded.

# E. Packet Aggregation at Multiplexer

In Fig. 4, following the k M-FIFOs at the multiplexer, a scheduler (SC) runs the aggregation algorithm to read packets out to the output line using static-class-first policy. The next selected M-FIFO to send packet, denoted as $S C _ { M } ,$ is given by

![](images/bdbedc4e6f7996c4f180a459977ea400a8ded498f53b1e3ce21422db86ad34c5.jpg)



![](images/a5dec615dc06d3155e9cdd9ea7af43d8f1117553aa2b33468a9b8c66b83e97e7.jpg)



![](images/5457433c0862a621a81260fb339c4b929f902c505ef8eeb4e618e724d71ef19f.jpg)



Fig. 5. A example of updating plane division information for dynamic classes of GD group.

$$
S C _ {M} = \left\{ \begin{array}{l l} \text { next   start   from } F P _ {D} (\text { all } M - \text { FIFOs   of   SAG   are   empty }) \\ \text { next   start   from } F P _ {S} & \text {(otherwise)} \end{array} \right. \tag {8}
$$

Where $F P _ { S }$ is the service pointer for M-FIFOs of SAG, and $F P _ { D }$ is the pointer for M-FIFOs of DAG. Both pointers serves using SRR algorithm. All the M-FIFOs have identical QSs to guarantee fairness inside SAG and DAG respectively.

Since the central planes work at speedup $S _ { I \mathrm { 3 } }$ backpressure mechanism is introduced at multiplexer to avoid congestion. Let $F S _ { M U X }$ denote the size of each M-FIFO, FMLl denote the current length of M-FIFO l, RTT denote the signal round-trip time between the multiplexer and the switching plane, and $P L _ { M A X }$ denote the maximal length of incoming packet. Backpressure frame will be sent back to plane l at the beginning of each backpressure cycle $T _ { B P }$ and stop this plane sending packets during the next cycle if (9) holds.

$$
F M L _ {l} \geq F S _ {M U X} - \left(R T T + T _ {B P}\right) \times r - P L _ {M A X} = F B _ {M U X} \tag {9}
$$

The backpressure mechanism actually extends output buffer from M-FIFO at the multiplexer to the OQ of switching plane.

# F. Scheduling at Central Switches

As described in part A, CIOQ switch is used in the central switching plane. Since DS-PPS provides each dynamic class with precise number of central planes adaptively according to the required output bandwidth, it is coherent for the CIOQ switches to perform OQ-like switch with conflict only at output. Previous works have proved that with speedup of 2, the CIOQ switch can precisely emulate an OQ switch [27].

DS-PPS adopt the JPM scheduling algorithm [27] at the central CIOQ switch. JPM performs a stable matching at each time slot based on the preference list at each input and output. The preference list at the input orders cells at the inverse order of their arrival times, and at the output orders the cells by their scheduling time in corresponding OQ switch. Although three DS queues with strict priority are built inside each OQ and VOQ, both the preference lists can be emulated only by comparing the arrival timestamps in the head of these DS queues. It leads to a complexity of ${ \cal O } ( l o g N )$ to run a iteration in the stable matching, and is practical for a real implementation.

To further reduce the time complexity to O(1), parallel iterative matching algorithms can be used, such as iSLIP. We will discuss the QoS guarantee of DS-PPS that employs JPM algorithm in Section V. In Section VII, we show by simulation that the DS-PPS with iSLIP has the similar performance.

# V. ANALYSIS OF QOS GUARANTEE IN DS-PPS

Definition 1: The incoming packets with same QoS class, input and output port in DS-PPS are defined to be a sub-flow. During the kth measuring cycle $T _ { k } ,$ the packet arrivals of subflow f are modeled as a Poisson process with the rate of $R _ { f } ( k )$ . The arrival processes of different sub-flows are independent with each other. Each incoming packet is assumed to be a single cell of length $P _ { L }$ for the convenience of analysis.

Recent traffic observations show that the traffic fluctuations at small timescale (below 100ms) are almost unrelated [29]. Thus, when $T _ { m e }$ is set to be 100ms, the Poisson assumption of definition 1 holds.

Fact 1: Denote $T _ { k - I }$ and $T _ { k }$ as two continuous cycles, the traffic fluctuation $T V _ { f } ( k ) = R _ { f } ( k ) / R _ { f } ( k - 1 )$ for sub-flow $f .$ satisfies

$$
E [ T V _ {f} (k) ] \approx 1, \operatorname{Var} [ T V _ {f} (k) ] \approx 0. 0 0 5, \left| T V _ {f} (k) - 1 \right| <   0. 2 \tag {10}
$$

This fact is derived from the studies on the traces from National Laboratory for Applied Network Research (NLANR) [28], in which six segments of backbone traces at distinct links and times that last one hour each are collected. Each segment is processed into small slices by 100ms interval. The $T V _ { f } ( k )$ of all the slices are depicted in Fig. 6. It is shown that in these traces, more than 99.5% fluctuations satisfiy $\left| T V _ { _ f } ( k ) - 1 \right| < 0 . 2$ . The average and variation of the fluctuation is calculated as 1.00209 and 0.005, respectively.

Definition 2: Each CIOQ switch in the central switching plane of DS-PPS is replaced by an OQ switch operating at line rate r during the analysis. Let $O Q _ { _ i } ^ { i }$ denote the OQ at port j of switching plane l.

# A. Delay Bound of Static Class Traffic

Definition 3: Denote the sub-flow of static class $H _ { s }$ from input port i to output port j as $S f _ { i j } ^ { s }$ . During measuring cycle $T _ { k } ,$

![](images/a5b1878556835e210ae628bba7e5636e73e19937701accafa55038446d677012.jpg)



Fig.6. The fluctuation of average rate under timescale of 100ms.

the arrival process $S f _ { i j } ^ { s }$ is modeled as Poisson process $I P _ { _ { i j } } ^ { s }$ with the rate of $\alpha _ { _ i j } ^ { s } ( k )$ . Let $\alpha _ { _ { i 0 } } ^ { s } ( k )$ denote the aggregate rate of all the sub-flows at input port i, and $\alpha _ { _ { 0 j } } ^ { s } ( k )$ denote the aggregate rate at output port j. they satisfy

$$
\forall s \in [ 1, t ], i, j \in [ 1, N ], \alpha_ {i 0} ^ {s} (k) = \sum_ {j = 1} ^ {N} \alpha_ {i j} ^ {s} (k), \alpha_ {0 j} ^ {s} (k) = \sum_ {i = 1} ^ {N} \alpha_ {i j} ^ {s} (k) \tag {11}
$$

Lemma 1: Both the queues at the demultiplexer and the central switching plane buffering packets of static class can be modeled as M/D/1 queue. The packet delay of static class at the multiplexer is negligible.

Proof: Because of the fixed-length packet assumption (definition 1), the HAP-LB algorithm at the demultiplexer dispatches packets of sub-flow $S f _ { i j } ^ { s }$ to switching planes in group SGs by simple round-robin. Therefore, the sub-process of $I P _ { _ { i j } } ^ { s }$ to each plane in group SGs can be safely approximated by Poisson process of rate $\alpha _ { _ i j } ^ { s } ( k ) / A S _ { _ s }$ . As a result, the aggregate arrival process at each D-FIFO is also Poisson process of rate $\sum _ { j = 1 } ^ { N } [ \alpha _ { i j } ^ { s } ( k ) / A S _ { s } ] = \alpha _ { i 0 } ^ { s } ( k ) / A S _ { s }$ . Given that every D-FIFO reads packet out at constant rate $r ,$ the D-FIFOs corresponding to group SGs can be modeled as the M/D/1 queue with offered load of $\rho _ { _ { i 0 } } ^ { s } = \frac { \alpha _ { _ { i 0 } } ^ { s } ( k ) / A S _ { _ s } } { r }$

At the central plane, the arrival process at $O Q _ { j } ^ { l }$ is the aggregation of departure processes from the M/D/1 queue of D-FIFO l in every input port. Therefore, it is safely approximated to be Poisson process, with the rate of $\sum _ { i = 1 } ^ { N } [ \alpha _ { i j } ^ { s } ( k ) / A S _ { s } ] = \alpha _ { _ { 0 j } } ^ { s } ( k ) / A S _ { s }$ , where plane l∈SGs. Since the multiplexer schedules traffic of static class first, $O Q _ { _ i } ^ { ' }$ seldom encounters backpressure. Thus, lOQ is also modeled as M/D/1 queue, with offered load of $\rho _ { _ { 0 j } } ^ { s } ( k ) = \frac { \alpha _ { _ { 0 j } } ^ { s } ( k ) / A S _ { _ { s } } } { r }$

At the multiplexer, packet delays of first-scheduled static class are close to their transmission time, because the M-FIFOs which receive traffic of static class are empty in most times. Delay here for a 1.5k bytes packet at OC768 link is about 300ns, which is negligible.■

Lemma 2: The offered load of static class $H _ { s }$ at each input and output port is bounded by:

$$
\underset {i = 1} {\overset {N} {\operatorname{Max}}} \rho_ {i 0} ^ {s} (k) \leq B _ {s}, \underset {j = 1} {\overset {N} {\operatorname{Max}}} \rho_ {0 j} ^ {s} (k) \leq B _ {s}, \text { where } B _ {s} <   1 / S _ {1}
$$

Proof: This lemma is derived from the criterion for static class in Section IV.B.■

Theorem $I \colon$ The packet delay of static class is bounded statistically.

Proof: From Lemma 1, the packet delay of static class is the sum of delays in two M/D/1 queues with the load of both bounded by $B _ { s } .$ . Since $B _ { s } < 1$ , each delay is bounded statistically. Hence, the sum holds the same.

Using Pollaczek-Khintchine Formula [1], the delay distribution of each M/D/1 queue under load of $B _ { \it s }$ can be calculated. The statistical delay bound of each queue is presented in the second row of table 1, where u is the service time of individual packet at link rate $r ,$ satisfying $u = P _ { \mathrm { } _ { L } } / r$ . Figures in the third row shows the immediate sum of delay bound, while figures in the fourth row gives the total delay bound assuming the two queues are independent.■

Table 1. The packet delay bound of static class under load bounded by Bs 

<table><tr><td> $B_s$ </td><td>0.1</td><td>0.3</td><td>0.5</td><td>0.6</td><td>0.7</td><td>0.8</td><td>0.9</td></tr><tr><td>Single Bound ( $u$ )</td><td>5</td><td>7</td><td>12</td><td>14</td><td>19</td><td>31</td><td>56</td></tr><tr><td>Summed Bound ( $u$ )</td><td>10</td><td>14</td><td>24</td><td>28</td><td>38</td><td>62</td><td>112</td></tr><tr><td>Summed Bound ( $u$ )(Independent)</td><td>6</td><td>9</td><td>14</td><td>18</td><td>24</td><td>38</td><td>73</td></tr></table>

# B. Delay Bound of Dynamic Class Traffic in GD group

Definition 4: Let $D f _ { i j } ^ { s }$ denote the sub-flow of dynamic class $L D _ { s }$ from input i to output $j .$ The arrival process of $D f _ { i j } ^ { s }$ at cycle $T _ { k }$ is modeled as Poisson process with the rate of $\alpha _ { i j } ^ { s } ( k )$ . Let $\alpha _ { _ { i 0 } } ^ { ^ { s } } ( k )$ denote the aggregate rate of processes of $D f _ { i j } ^ { s }$ at input $i ,$ and $\alpha _ { _ { 0 j } } ^ { ^ { s } } ( k )$ denote the aggregate rate at output j. The switching planes assigned for $D f _ { i j } ^ { s }$ at cycle $T _ { k }$ is in sub-group $D G _ { s } ^ { j } ( k )$ , which includes $A D _ { s } ^ { j } ( k )$ planes. The speedup for dynamic class $L D _ { s }$ at output j is denoted as $S D _ { s } ^ { j } ( k )$ , having

$$
S D _ {s} ^ {j} (k) = \frac {A D _ {s} ^ {j} (k) \times r}{\alpha_ {0 j} ^ {s} (k - 1)} \tag {12}
$$

Lemma 3: The packet delay of dynamic class at the demultiplexer is statistically bounded by $F B _ { _ { D E M U X } } / r$ when $S _ { \scriptscriptstyle 1 } > 1 . 0 7 2 ( A D + A S ) / A D$ .

Proof: Using threshold RR algorithm, the queue length L of D-FIFO l will not increase beyond $F B _ { _ { D E M U X } }$ DEMUX unless all the D-FIFOs of the same sub-group exceed the threshold. This probability is approximately calculated by

$$
\left[ P \left(L > F B _ {\text { demux }}\right) \right] ^ {\frac {2 A D}{m + n}} \approx \left(\frac {\rho_ {i} ^ {*}}{S _ {1}}\right) ^ {\frac {F B _ {\text { demux }} 2 A D}{P _ {L} m + n}} \leq \left[ \frac {\rho_ {i} (A D + A S)}{S _ {1} A D} \right] ^ {\frac {F B _ {\text { demux }} 2 A D}{P _ {L} m + n}} \tag {13}
$$

Here $\rho _ { _ i }$ denotes the average load of all the D-FIFOs, $\rho _ { i } ^ { * }$ denotes the average load of all the D-FIFOs corresponding to DAG. Since $\rho _ { i } < 1 , \frac { \mathit { F B } _ { d e m u x } } { \mathit { P } _ { L } } \geq 1 0 0 \mathrm { a n d } \frac { \mathit { 2 A D } } { \mathit { m } + { n } } \geq 1$ demuxFB , this probability is smaller than 0.001 when $S _ { \scriptscriptstyle 1 } > 1 . 0 7 2 ( A D + A S ) / A D$ . Therefore, considering each D-FIFO is served with constant rate $r ,$ the packet delay here is statistically bounded by

$$
F B _ {D E M U X} / r. \blacksquare
$$

Lemma 4: The packet delay of dynamic class at the multiplexer is determinately bounded by $F S _ { _ { M U X } } S _ { 1 } / r$ .

Proof: According to the backpressure mechanism, the size of M-FIFO will not increase beyond $F S _ { _ { M U X } }$ . The aggregation algorithm serves the M-FIFOs corresponding to SAG with strict high priority. They at most occupy output bandwidth of $r \sum _ { s = 1 } ^ { t } \left( B _ { s } A S _ { s } \right) \le r / S _ { 1 } \sum _ { s = 1 } ^ { t } A S _ { s } = A S r / S _ { 1 }$ . Therefore, each of the M-FIFOs corresponding to DAG is served with at least constant rate of $( R - A S r / S _ { \imath } ) / A D = r / S _ { \imath }$ . Therefore, the packet delay here is determinately bounded by $F S _ { _ { M U X } } S _ { 1 } / r$ .■

Lemma 5: The statistical packet delay bound at the central OQ switch when only dynamic class traffic of GD group exists is still valid if admitting traffic of other QoS groups.

Proof: This lemma can be derived from the strict priority scheduling among DS queues of $O Q _ { _ { j } } ^ { l }$ .■

Lemma 6: lOQ at switching plane l in DAG is safely approximated to be M/D/1 model with Poisson arrival process of rate $\gamma _ { 0 j } ^ { l } ( k )$ and constant service of rate $r / S _ { \mathrm { \Omega _ { 1 } } }$ .

Proof: The $O Q _ { j } ^ { l }$ is equal to one single DS queue for GD group now. The arrival process at $O Q _ { j } ^ { l }$ is the composition of departure process at D-FIFO l from every input to output j. At input i, denote $\gamma _ { \phantom { * } i 0 } ^ { * _ { l } } ( k )$ as the arrival rate at D-FIFO l when simple SRR without threshold is employed, and $\gamma _ { i 0 } ^ { l } ( k )$ as the arrival rate with threshold SRR algorithm. Then $\gamma _ { i 0 } ^ { l } ( k )$ is approximated by

$$
\gamma_ {i 0} ^ {l} (k) = \left\{ \begin{array}{l l} r & \gamma_ {i 0} ^ {* l} (k) \geq r \\ \gamma_ {i 0} ^ {* l} (k) \times S u _ {i} ^ {l} (k) & \gamma_ {i 0} ^ {* l} (k) <   r \end{array} \right. \tag {14}
$$

Here $S u _ { \scriptscriptstyle i } ^ { \scriptscriptstyle i } ( k )$ is the rate increase caused by the congestion at D-FIFOs when $\gamma _ { \iota _ { i 0 } } ^ { * _ { l } } ( k ) \geq r$ . All the D-FIFOs are safely modeled by M/D/1 queue. As a result, the departure process at D-FIFO l of packets from input i to output j is safely modeled by Poisson process of rate $\gamma _ { _ { i j } } ^ { \prime } ( k )$ . Hence, the arrival process at

$$
O Q _ {j} ^ {l} \text {   is   Poisson   process   of   rate   } \gamma_ {0 j} ^ {l} (k) = \sum_ {i = 1} ^ {N} \gamma_ {i j} ^ {l} (k).
$$

At the output direction, since each M-FIFO corresponding to DAG receives constant service of at least rate $r / S _ { \mathrm { \Omega _ { 1 } } }$ (proof of lemma 4), $O Q _ { j } ^ { l }$ is served with constant service of at least rate $r / S _ { \mathrm { \scriptscriptstyle 1 } }$ as well.■

Lemma 7: Let $L D _ { _ { t ( l , j ) } }$ denote the dynamic class arrived at $O Q _ { j } ^ { l }$ . When N is large and $S D _ { t ( l , j ) } ^ { j } ( k ) \ge 2 ~ , ~ \gamma _ { 0 j } ^ { l } ( k )$ is the random variable with expectation $r / S D _ { t ( l , j ) } ^ { j } ( k )$ and square coefficient of variation less than 0.005.

Proof: Available on-line at http://s-router.cs.tsinghua.edu.cn /shilei/Infocom06proof.htm.■

Theorem 2: If $S D _ { s } ^ { j } ( k ) \geq 3 . 2 4 S _ { 1 } , S _ { 1 } > 1 . 0 7 2 ( A D + A S ) / A D$ , and N is large, the packet delay of dynamic class $L D _ { s }$ is statistically bounded.

Proof: From lemma 3, 4, the packet delay at demultiplexer and multiplexer are both statistically bounded. From lemma 6, $O Q _ { j } ^ { l }$ at central plane l is modeled as M/D/1 queue. Using lemma 7 and Chebyshev’s inequality [1], when $S D _ { t ( l , j ) } ^ { j } ( k ) \geq 3 . 2 4 S _ { 1 }$ , we have

$$
P \left[ \gamma_ {0 j} ^ {l} (k) \geq \frac {r}{S _ {1}} \right] \leq P \left[ \gamma_ {0 j} ^ {l} (k) \geq 3. 2 4 \times \frac {r}{S D _ {s} ^ {j} (k)} \right] \tag {15}
$$

$$
\leq P \left\{\left| \gamma_ {0 j} ^ {j} (k) - \frac {r}{S D _ {s} ^ {j} (k)} \right| \geq 2. 2 4 \times \frac {r}{S D _ {s} ^ {j} (k)} \right\} \leq 0. 0 0 5 / 2. 2 4 ^ {2} <   0. 0 0 1
$$

Knowing from (15), the delay at $O Q _ { j } ^ { l }$ are statistically bounded. Therefore, the whole packet delay of dynamic class of GD group is bounded statistically.

The delay bound for dynamic class $L D _ { s }$ is calculated based on $S D _ { s } ^ { j } ( k )$ . Table 2 presents some numeric results.■

Table 2. The delay bound for dynamic class of GD group 

<table><tr><td> $SD_{GD}^{i}(S_{I})$ </td><td>3.24</td><td>3.6</td><td>4.05</td><td>4.63</td><td>5.4</td><td>6.48</td><td>10.8</td></tr><tr><td>delay bound at central plane (u)</td><td>∞</td><td>56</td><td>31</td><td>19</td><td>14</td><td>12</td><td>7</td></tr><tr><td>delay bound at demultiplexer (u)</td><td colspan="7"> $FB_{DEMUX}/r\approx 100$ </td></tr><tr><td>delay bound at multiplexer (u)</td><td colspan="7"> $FS_{MUX}S_{1}/r\approx 100$ </td></tr></table>

# C. Throughput of Dynamic Class Traffic in GB group

Theorem 3: When the speedup for dynamic classes of GB group at output j satisfies $S B ^ { j } ( k ) \geq S _ { \mathrm { 1 } }$ , for each class $L D _ { s } ,$ $S D _ { s } ^ { j } ( k ) \geq S B ^ { j } ( k ) \geq S _ { 1 }$ , and $S _ { _ 1 } > 1 . 1 2 2 ( A D + A S ) / A D$ , the 99.999% throughput for all the dynamic class $L D _ { s }$ and $L B _ { s }$ are guaranteed.

Proof: When $S _ { 1 } > 1 . 1 2 2 ( A D + A S ) / A D$ (proof of lemma 3, 4), the packet delay at the demultiplexer and the multiplexer are both bounded with 99.999% probability, so that the 99.999% throughput is guaranteed here. Similarly to the proof of lemma $7 , \ \gamma _ { 0 j } ^ { l } ( k )$ is the random variable with expectation of $r / S B ^ { j } ( k )$ when traffic of both GD group and GB group is admitted. Since $S B ^ { j } ( k ) \geq S _ { 1 }$ , we have $r / S B ^ { j } ( k ) \le r / S _ { 1 }$ . Therefore, the throughputs of both GD group and GB group are guaranteed at the central switching plane. Thus, the total throughput is guaranteed statistically.■

# VI. PRACTICAL IMPLEMENTATION OF THE FRAMEWORK

This section introduces a practical implementation of the DS-PPS framework. Both a QoS-based traffic classification model and a practical DS-PPS prototype using this model are presented.

# A. Traffic Classification

The traffic classification is developed based on two major factors: the requirements of class-based differentiated QoS and the need for traffic isolation between classes to avoid performance degradation. Totally six QoS classes (2 classes in FT) are partitioned, each is described below.2

TCP Short Packet (TSP): A packet is classified as a TSP if and only if the two conditions are both satisfied: 1) the packet size is not more than 64 bytes; and 2) it is a TCP non-data packet. This class includes the traffic of TCP ACK and control packets. Recent study [30] shows that TSP has a great impact on the performance of TCP, but suffers from large delay due to serving long data packets when switching is run in packetmode. In DS-PPS, we assign separate static class and exclusive switching planes for TSP. The number of the planes can be tuned to achieve tight statistical delay bound of TSP. In this way, DS-PPS helps to improve TCP performance.

Real-Time Traffic (RT): RT is mostly generated by multimedia services such as VoIP, IPTV, etc. Considering that 1) it demands stringent delay, and 2) it mostly works upon UDP or RTP where no congestion control mechanism is applied, RT brings great challenge to the stability of current networks. In the DS-PPS, RT is classified into a dynamic class of GD group, so that stringent delay bound can be guaranteed without affecting other traffic much.

Interactive Traffic (IT): IT mainly refers to the traffic generated by HTTP, telnet, on-line game and other interactive services. Currently, the web traffic dominates IT class. Low delay is desired here to attract interactive users, however, its requirement is looser than RT. Further, as the web traffic is mostly transferred in the form of TCP short flows, mentioned as mice [31], they greatly affect the performance of TCP elastic traffic. Therefore, another dynamic class of GD group is assigned for IT in the DS-PPS.

File-Transfer Traffic (FT): Besides the traffic generated by traditional file transfer protocol, such as FTP, FT also includes the traffic of many new protocols, such as P2P file sharing. Different from the above three classes, it mainly concerns the bandwidth guarantee. Hence in DS-PPS, two dynamic classes of GB group are assigned for FT, including the FT-LP class with low drop precedence and FT-HP class with high drop precedence.

Best-Effort Traffic (BE): It is the traffic which requires no QoS guarantee. In DS-PPS, the sole dynamic class of BE group is assigned for it.

# B. DS-PPS Prototype

We develop a DS-PPS prototype with 32 parallel switching planes and 32 external ports. Each port runs at 40Gb/s external line rate, and each plane works at 1.5Gb/s internal line rate. Thus, this prototype has a speedup of $S _ { I } { = } 1 . 2$ at the central stage. The length of individual cell is set to be 64 bytes. Mappings of the traffic classification model in part A to this prototype are as follows: TSP serves as the only static class; RT and IT map to two dynamic classes of GD group; FT-LP and FT-HP work as two dynamic classes of GB group; BE is the sole dynamic class of BE group.

Static class: From the criterion for static class in Section IV.B, the class can be taken as static class only if its peak bandwidth is bounded at both input and output. Recent Internet traffic measurement results show that the short packet with length no more than 64 bytes takes up only 6% of the total bytes. As a fraction of that, TSP occupies even less bandwidth, thus can be mapped to one static class. Here we take 4% as the peak bandwidth for TSP.

In our prototype, we assign two planes statically for it, so that the offered load of TSP is bounded by ${ \mathrm { B } } _ { \mathrm { s } } { \approx } 0 . 5 .$ Using theorem 1, the statistical delay bound for TSP is about 14µ in table 1, which corresponds to 4.78us under line rate of this prototype. Such a delay can be ignored compared with the average TCP RTT time of 100ms. In this sense, the TCP RTT time is reduced into a half when DS-PPS is deployed at every hop of the entire networks.

Dynamic class: The 30 remaining central planes serve the five dynamic classes. We set RTGDSP $S P _ { _ { G D } } ^ { ^ { R T } } = 4 > 3 . 2 4 S _ { 1 } \ , \ S P _ { _ { G D } } ^ { ^ { I T } } = 2$

$S P _ { G B } = 1 . 2 = S _ { 1 }$ based on the following observations: RT class demands stringent delay bound; IT class requires looser delay guarantee; FT classes need only bandwidth guarantee. Thus, conditions of theorem 2 for RT class and theorem 3 for each class of GD and GB group are met if all the incoming traffic does not override the traffic quota inversely proportional to the preset speedup. Therefore, delay bound of RT and bandwidth of RT, IT, FT is statistically guaranteed.

# VII. PERFORMANCE EVALUATION

# A. Simulation Methodology

To evaluate the performance of DS-PPS, we develop two software simulators. The first simulator implements all the specifications of structures, mechanisms and algorithms in DS-PPS framework. Simulated prototype here applies the traffic classification model and the setting of parameters in Section VI. Contrastively, the other simulator implements the structure of basic PPS.

![](images/4b7c8c5f43d2eff26475bccc9ed7c4fd8b8d512d2089f1a4165b77ac47b5343f.jpg)



Fig. 7. Average delays under uniform packet arrivals. (TSP, RT, IT, FT-LP, FT-HP, BE for classes in DS-PPS, Basic PPS for overall delay in basic PPS.)

The traffic generated for the two simulators is modeled according to the normal traffic pattern derived from recent traffic measurement results. The proportions of traffic of the six classes (TSP, RT, IT, FT-LP, FT-HP, BE) are set to be 4%, 10%, 30%, 15%, 15%, 26%, respectively. The packet arrivals of each class are generated as Bernoulli arrivals. Each packet is modeled as a single cell unless specially noted.

We launch five sets of simulations applying comprehensive traffic patterns on both simulators. Each simulation lasts 54 million external time slots. The traffic in DS-PPS is measured separately for each class, while the traffic in basic PPS is measured as a whole class.

# B. Results

# 1. Uniform Arrivals

In our first set of simulation, the destination of each packet is uniformly distributed among all the N output ports. The simulations are carried out in both simulators under load rate from 0.1 to 1 with an interval of 0.1.

Figure 7 plots the average delays, where TSP and RT in DS-PPS are always much smaller than that of basic PPS. Under full load, the average delay of TSP is reduced by 94% and the average delay of RT is reduced by 88%.

Figure 9 plots the statistical delay bounds of classes of GD group in DS-PPS and basic PPS. Results validate that the measured bounds of TSP and RT in DS-PPS do not override the theoretical bounds in Section V.

# 2. Unbalanced Arrivals

In this simulation, the destination of each packet follows unbalanced distribution. The probability $P _ { _ { i j } }$ of a packet at input port i going to output port j is modeled by

$$
P _ {i j} = \left\{ \begin{array}{c c} \alpha & i = j \\ (1 - \alpha) / (N - 1) & i \neq j \end{array} , \text { where } \alpha \text { is   the   unbalanced   rate. } \right.
$$

Average packet delays under fixed load rate of 0.8 and unbalanced rate from 0.1 to 1 in both simulators are plotted in Fig. 8. We can see that the unbalanced traffic pattern does not degrade the performance of DS-PPS. In most cases, it reduces the average delay slightly.

![](images/439c324595c62b2e42648dbb054a6f13b752334be85d2fd03a189031bb38b7bc.jpg)



Fig. 8. Average delay under unbalanced packet arrivals, the load rate is fixed to 0.8.

![](images/fce8ccd98d0a2dc1c64b826941143fb5365530f96e443971d1d504bea2f73147.jpg)



Fig. 9. Statistical packet delay bound of classes of GD group in DS-PPS and basic PPS under uniform packet arrivals in both cell-mode and packet-mode (with –PM).   
![](images/53a401e809ed88462122fb79e52a10c5ef88c06974b85e1c5bcdd900b047d229.jpg)



Fig. 10. Throughput under packet arrivals with hotspot, the overload rate is from 0.005 to 0.05.

# 3. Uniform Arrivals with Hotspots

Under admissible traffic patterns (e. g., simulation 1, 2), the throughput of DS-PPS is nearly 100% for every class. To validate the guaranteed throughput performance in DS-PPS, a traffic pattern with hotspot is used in this simulation, where the probability $P _ { _ j }$ of a packet going to output port j is modeled by

$P _ { _ j } = \left\{ \begin{array} { l l } { \alpha + ( 1 - \alpha ) / N } & { j = P _ { h o t } } \\ { ( 1 - \alpha ) / N } & { j \neq P _ { h o t } } \end{array} \right.$ (1 ) /  hotN j P+ − =  , where Phot is the hotspot, α is the $P _ { h o t }$ overload rate.

Figure 10 plots the throughputs under fixed load rate of 0.8 and overload rate from 0.005 to 0.05 with an interval of 0.005. Results show that the classes of GD group are guaranteed of nearly 100% throughput even under high overload rate. The FT-LP is guaranteed of nearly three times the throughput of the FT-HP, which means the absolute low drop precedence.

# 4. Uniform Packet-Mode Arrivals

Different from the above simulations, the packet length distribution here is modeled according to the real traffic measurement results. TSP is of one-cell-length, while the packet length of the other classes are modeled by TRIMODEL(1,9,24,0.56,0.2) with cell as unit. The average delays under load rate from 0.1 to 1 with an interval of 0.1 are plotted in Fig. 11. We see that in packet-mode, the average

![](images/89cdd49db1679257b48a377b7102018ab576aae012f46a46b9bfe9f698a13551.jpg)



Fig. 11. Average delay under packet-mode uniform traffic arrivals. Packets of TSP class are of one-cell-length, the other packets follow TRIMODEL(1, 9, 24, 0.56, 0.2).   
![](images/63d5e4f5be7830adf6db8ef368ca67451047edfc26f9d59430944e7060aab572.jpg)



Fig. 12. Average delay under iterative scheduling algorithm at the central switches.

delays of TSP and RT are reduced by 98% and 82%, respectively. The statistical delay bounds here are shown in Fig. 9, the traffic of TSP and RT is guaranteed of bounded delay.

# 5. Parallel Iterative Matching

In this set, the DS-PPS employing parallel iterative matching (iSLIP) in the central switching plane is simulated. The other configurations are the same with simulation 1. The average delays plotted in Fig. 12 show that the performance of this modified DS-PPS is similar to basic DS-PPS. Comparing with results in simulation 1, there is a maximum of only 21% increase in delay except the BE class. Therefore, the popular CIOQ switch with parallel iterative matching can be used in the central switching plane of DS-PPS to reduce the design complexity without greatly affecting the overall performance.

# VIII. CONCLUSIONS

Differentiated QoS is of importance in the designs of PPS. In this paper, we propose a novel and practical framework, called DS-PPS, upon the basic PPS. DS-PPS provides three fundamental QoS features, namely guaranteed-delay, guaranteed-bandwidth and best-effort. In this way, the framework is universal and scalable to support most of the upto-date QoS requirements.

We evaluate DS-PPS by extensive theoretical analyses and comprehensive simulations. Experimental results on a prototype implementation show that, DS-PPS outperforms the basic PPS by reducing more than 94% of the average delay of TCP short packet, and reducing more than 82% of the average delay of real-time traffic under full load, as well as offering the QoS class of absolute low drop precedence.

In future, we will explore other applications demanding differentiated QoS to enlarge the use of DS-PPS framework. Extended simulations in the Internet environment will be conducted to further verify the practicality of the framework.

# REFERENCES

[1] R. W. Wolff, Stochastic Modeling and the Theory of Queues, Prentice Hall, October 1989.   
[2] N. McKeown, “Scheduling Algorithms for Input-queued Cell Switches”, Ph. D. Thesis, UC Berkeley, May 1995.   
[3] Cisco CRS-1. http://www.cisco.com/go/crs/.   
[4] T640 Routing Node and TX Matrix Platform: Architecture, Juniper White Paper. http://www.juniper.net/.   
[5] H. J. Chao, K. L. Deng, Z. Jing, “A Petabit Photonic Packet Switch (P3S),” In Proc. of IEEE INFOCOM’2003, vol. 1, pp. 775-785, Match 2003.   
[6] C. Minkenberg, et al., “Current Issues in Packet Switch Design,” ACM SigComm. Comput. Comm. Rev., vol. 33, no. 1, Jan. 2003.   
[7] S. Cherry, “The Battle for Broadband [Internet protocol television],” IEEE Spectrum, vol. 42, issue 1, pp. 24-29, Jan. 2005.   
[8] H. B. Newman, M. H. Ellisman, and J. A. Orcutt, “Data-intensive Escience Frontier Research”, Commun. of the ACM, vol. 46, no. 11, pp. 68-77, 2003.   
[9] R. Braden, D. Clark, and S. Shenker, “Integrated Services in the Internet Architecture: An Overview,” RFC 1633, July 1994.   
[10] S. Blake, D. Black, D. Black, H. Schulzrinne, D. Black, M. Carlson, E. Davies, Z. Wang, and W. Weiss, “An Architecture for Differentiated Service,” RFC 2475, Dec. 1998.   
[11] Y. Bernet, J. Binder, S. Blake, M. Carlson, B. Carpenter, S. Keshav, E. Davies, B. Ohlman, Z. Wang, and W. Weiss, “A Framework for Differentiated Services,” Internet Draft, Feb. 1999.   
[12] C. S. Chang, D. S. Lee and Y. S. Jou, “Load Balanced Birkhoff-von Neumann Switches, Part I: One-stage Buffering,” In Proc. of IEEE HPSR ’01, Dallas, May 2001.   
[13] A. Bianco, P. Giaccone, E. Leonardi, and F. Neri, “A Framework for Differential Frame-based Matching Algorithms in Input-queued Switches,” In Proc. of IEEE INFOCOM’2004, vol. 2, pp. 1147-1157, March 2004.   
[14] E. Oki, R. Rojas-Cessa, and H J. Chao, “A Pipeline-based Maximalsized Matching Scheme for High-speed Input-buffered Switches,” IEICE Trans. Commun., vol. E85-B, no. 7, pp. 1302-1311, July 2002.   
[15] Vitesse GigaStream Intelligent Switch Fabric VSC872/VSC882 Design Manual, Rev 2.2, http://www.vitesse.com.   
[16] AMCC Cyclone Switch Fabric S8505-S8905 Product Concept, Rev0.07.   
[17] N. Seitz, “ITU-T QoS Standards for IP-based Networks,” IEEE Commun. Mag., vol. 41, issue 6, pp. 82-89, June 2003.   
[18] B. Prabhakar, N. McKeown, “On the Speedup Required for Combined Input and Output Queued Switching,” Automatica, vol. 35, no. 12, Dec. 1999.   
[19] R. Rojas-Cessa, E. Oki, Z. Jing, and H. J. Chao, “CIXB-1: Combined Input-one-cell-crosspoint Buffered Switch,” In Proc. of IEEE HPSR 2001, Dallas, Texas USA, May 29-31, 2001.   
[20] A. Aslam, K. Christensen, "Parallel Packet Switching using Multiplexors with Virtual Input Queues," In Proc. of IEEE LCN’2002, pp. 270-277, Nov. 2002.   
[21] S. Iyer, N. McKeown, "Analysis of the Parallel Packet Switch Architecture," IEEE Trans. Networking, vol. 11, issue. 2, pp. 314-324, April 2003.   
[22] L. Shi, W. Li, and B. Liu, “Flow Mapping in the Load Balancing Parallel Packet Switches,” In Proc. of IEEE HPSR’2005, HongKong, May 2005.   
[23] D. A. Khotimsky, S. Krishnan, “Stability Analysis of a Parallel Packet Switch with Bufferless Input Demultiplexers,” In Proc. of IEEE ICC’2001, vol. 1, pp. 100-111, June 2001.

[24] W. Wang, L. Dong, and W. Wolf, “A Distributed Switch Architecture with Dynamic Load-balancing and Parallel Input-queued Crossbars for Terabit Switch Fabrics,” In Proc. of IEEE INFOCOM’2002, pp. 352-361, June 2002.   
[25] S. Iyer, A. Awadallah, and N. McKeown, “Analysis of a Packet Switch with Memories Running Slower than the Line Rate,” In Proc. IEEE INFOCOM’2000, vol. 2, pp. 529–537, Mar. 2000.   
[26] S. Mneimneh, V. Sharma and S. Kai-Yeung, “Switching Using Parallel Input-output Queued Switches with No Speedup,” IEEE/ACM Trans. Networking, vol. 10, issue 5, pp. 653-665, Oct. 2002.   
[27] I. Stoica, H. Zhang, “Exact Emulation of an Output Queueing Switch by a Combined Input Output Queueing Switch”, In Proc. of IEEE/IFIP IWQoS’98, pp. 218-224, May 1998.   
[28] Traces from National Laboratory for Applied Network Research (NLANR), http://pma.nlanr.net/Special/.   
[29] Z. L. Zhang, V. J. Ribeiro, S. Moon, and C. Diot, “Small-time Scaling Behaviors of Internet Backbone Traffic: an Empirical Study,” In Proc. of IEEE INFOCOM’2003, vol. 3, pp. 1826-1836, Mar. 2003.   
[30] W. J. Li., B. Liu, “SPF: to Improve the Performance of Packet-Mode Scheduling,” Comput. Commun., vol. 28, pp. 1380-1391, July 2005.   
[31] L. Guo, I. Matta, “The War between Mice and Elephants,” In Proc. of ICNP’2001, pp. 180-188, Nov. 2001.   
[32] H. Adiseshu, G. Parulkar, and G. Varghese, “Reliable FIFO Load Balancing over Multiple FIFO Channels,” Washington University Technical Report WUCS-95-11.   
[33] J. Duncanson, “Inverse Multiplexing,” IEEE Commun. Mag., vol. 32, pp. 34–41, Apr. 1994.