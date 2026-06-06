# MobiCom 2010 Poster: Capacity and Delay in Mobile Ad Hoc Networks under Gaussian Channel Model

Cheng Wang?? Xiang-Yang Li??,?? Shaojie Tang?? Changjun Jiang?? Yunhao Liu??,?? chengwang@ust.hk xli@cs.iit.edu stang7@iit.edu cjjiang@tongji.edu.cn liu@cse.ust.hk

??Department of Computer Science and Technology, Tongji University, Shanghai, China

??Department of Computer Science, Illinois Institute of Technology, Chicago, IL, 60616

??Department of Computer Science and Engineering, Hong Kong University of Science and Technology

We study the asymptotic delay and throughput in mobile ad hoc networks where ?? ad hoc nodes are distributed uniformly on a 2-D square (torus) region of area ??. The communications between nodes are characterized by Gaussian Channel model, instead of the simplified protocol model or physical model. The mobility of nodes is characterized by two general broad classes of practical mobility models, i.e., hybrid random walk models and discrete random direction models, which generalize many mobility models used in the literature. Our results either fill the gap in this area or generalize a stream of milestone results on asymptotic capacity, delay, and the tradeoffs developed recently.

# I. System Model

We consider an ad hoc network consisting of ?? mobile nodes that are distributed uniformly on a square region $\mathcal { R } ( n ) = [ 0 , \sqrt { n } ] ^ { 2 }$ initially. After that, all nodes move in accordance with the specific mobility.

# I.A. Random Mobility Model

We focus on two classes of mobility models: (1) Hybrid Random Walk Mobility Model (HRWMM) and (2) Discrete Random Direction Mobility Model (DRDMM), due to their generality, [1]. We partition a square of area ?? into $\frac { \mathfrak { a } } { \mathfrak { c } }$ subsquares of area ??, let ?? $( \mathfrak { a } , \mathfrak { c } )$ denote the resulted lattice.

HRWMM: Divide the region $\mathcal { R } ( n ) ~ = ~ [ 0 , \sqrt { n } ] ^ { 2 }$ into ?? squares of area  (henceforth referred as cells), resulting a lattice $\mathbb { L } ( n , 1 )$ . We next divide the region $\mathcal { R } ( n )$ into $n ^ { 1 - 2 \varepsilon }$ ( 1)squares of area $n ^ { 2 \varepsilon }$ (henceforth referred as super cells) for $\varepsilon \in [ 0 , { \frac { 1 } { 2 } } ]$ , resulting a lattice $\mathbb { L } ( n , n ^ { 2 \varepsilon } )$ . Then, there are $n ^ { 2 \varepsilon }$ [0 ]cells in each super cell.

( )Time is divided into phases of equal unit duration. Without loss of generality, we assume that the duration of each phase under HRWMM is $L _ { \mathrm { p } } ^ { \mathrm { h } } = 1$ . Initially, each node is equally likely to be in any of the cells, independent of the other nodes. At the beginning of each phase, a node uniformly chooses one cell at random from a randomly selected adjacent super cell, and jumps to the new cell from its current cell. And it will stay at the new cell during this phase. Please see Fig. 1(a). Particularly, for $\varepsilon ~ = ~ { \frac { 1 } { 2 } }$ , the above mobility model is essentially the i.i.d. model (Fig.1(b)); and for ?? , it becomes the random walk model (Fig.1(c)).

DRDMM: Divide the deployment region $\mathcal { R } ( n )$ into a lattice $\mathbb { L } ( n , n ^ { 2 \eta } )$ . Time is divided into phases of equal duration $L _ { \mathrm { p } } ^ { \mathrm { d } } .$ Initially, each node is equally likely to be in any of the cells, independent of the other nodes. The motion of a node during this phase is as follows: At the beginning of each phase, a node uniformly chooses an end point at random within a randomly selected adjacent cell, and moves to the end point at the velocity of constant order , as in [1]. To keep the duration of all phases the same, the speed of the node is set in proportion to the distance between the start point and end point. Note that the duration of the phases is $L _ { \mathrm { p } } ^ { \mathrm { d } } = \Theta ( n ^ { \eta } )$ . Please see Fig. 1(d). Particularly, for $\begin{array} { r } { \eta = \frac { 1 } { 2 } } \end{array}$ , the above mobility model is essentially similar to the random way-point mobility model (Fig.1(e)); and for $\eta = 0$ , it degenerates into the random walk model, which is the discrete time version of the Brownian motion model (Fig.1(f)).

# I.B. Communication Model

When time is divided into slots of sufficiently small duration, it is reasonable to assume that the position of each node is invariable (approximately) during a slot. Then, how small the duration, denoted by $L _ { \mathrm { s } }$ , should be to ensure the above assumption?

Under the HRWMM, since the motion of every node happens instantaneously at the beginning of each phase, it follows that the position of each node remains the same during a whole phase. Hence, we set

![](images/fe13390567aac96bafd8c00758c8c8352ad158ebf423a08f043fe188d2392e3b.jpg)



(a) General HRWMM

![](images/8a12313d72be72c984218dbd7e46e974c36005b8abb2503021eddefbbcc5771e.jpg)



(d) General DRDMM

![](images/98ffdfeb6e00f26d5e7dd1c75fe99c30221ccc68268418457e350039e40f0619.jpg)



(b) I.I.D MM

![](images/3b8f374a1a1902538905063e1ac275a681dfedcb570c8a92e40c86d78df31b6d.jpg)



(e) RWPMM

![](images/a3c123487f26044c7cf3ffe6b0d3f0739229e129c8cdeed2c277f2d73c87be0c.jpg)  
(c) RWMM

![](images/0fae11537715bee804666df33382e45be618fee7a6e28269a2f4dfb885dc2b9b.jpg)



(f) DBMM   
Figure 1: Illustrations of Mobility Models.

$L _ { \mathrm { s } } ~ = ~ L _ { \mathrm { p } } ^ { \mathrm { h } } ~ = ~ 1$ for HRWMM. Under the DRDMM, each node moves with velocity of constant order, which is infinitesimal relative to the extended scaling, during a phase. Thus, it is acceptable to set $L _ { \mathrm { s } }$ to be a constant number. Without loss of generality, for DRDMM, we also set $L _ { \mathrm { s } } = 1$ .

We call the time slot with duration $L _ { s }$ static slot in the following content. Intuitively, we can treat the MANET as a static network during one static slot. For any directed link $i ,$ we use $\mathbf { t } _ { i }$ and $\mathbf { r } _ { i }$ to denote its transmitter and receiver. Let $i ^ { t } , \mathbf { t } _ { i } ^ { t }$ and $\mathbf { r } _ { i } ^ { t }$ , denote $i , \mathbf { t } _ { i }$ and $\mathbf { r } _ { i }$ presented during static slot ??, correspondingly.

Under Gaussian channel model, for any set of links, say $S ^ { t }$ , that transmit simultaneously at slot $t ,$ the rate of a link $i ^ { t } \in S ^ { t }$ is $R _ { i } ^ { t } = B \times \log ( 1 + \mathrm { S I N R } _ { i } ^ { t } )$ , where $\begin{array} { r } { \mathrm { S I N R } _ { i } ^ { t } ~ = ~ \frac { { P \cdot \ell } ( \mathbf { t } _ { i } ^ { t } , \mathbf { r } _ { i } ^ { t } ) } { { N _ { 0 } + \sum _ { j \in \mathcal { S } ^ { t } - \{ i \} } { { P \cdot \ell } ( \mathbf { t } _ { j } ^ { t } , \mathbf { r } _ { i } ^ { t } ) } } } } \end{array}$ ??0+∑ ??∈????−{??} ?? ⋅ℓ(t???? ,r???? ) . Here, ?? =?? ⋅ℓ(t????,r???? ) $P$ denotes the transmission power of each transmitter, $N _ { 0 } ~ > ~ 0$ denotes the ambient noise power at the receiver, $\ell ( \mathbf { t } _ { i } ^ { t } , \mathbf { r } _ { i } ^ { t } ) = \operatorname* { m i n } \{ 1 , \ | \mathbf { t } _ { i } ^ { t } - \mathbf { r } _ { i } ^ { t } | ^ { - \alpha } \}$ denotes the power attenuation function and $\alpha > 2$ is the power attenuation exponent.

Throughout the paper, we let the expression $f ( n )$ $[ \phi _ { 1 } ( n ) , \phi _ { 2 } ( n ) ]$ represent that $f ( n ) \ : = \ : \Omega ( \phi _ { 1 } ( n ) )$ and $f ( n ) = O { \bigl ( } \phi _ { 2 } ( n ) { \bigr ) }$ ; let $f ( n ) : ( \phi _ { 1 } ( n ) , \phi _ { 2 } ( n ) )$ represent that $f ( n ) = \omega { \bigl ( } \phi _ { 1 } ( n ) { \bigr ) }$ and $f ( n ) = o ( \phi _ { 2 } ( n ) )$ .

# II. Communication Strategy

# II.A. Contact and Waiting Intervals

Under a given communication strategy S, a key parameter is the critical distance ??S, within which two nodes will communicate directly, where ${ \mathrm { \mathbf { l } } } _ { \mathbf { S } } : [ 1 , { \sqrt { n } } ]$ . : [1 ]Depending on a specific mobility model and the critical distance ${ \mathfrak { l } } _ { \mathbf { S } } ,$ , we can define the contact interval during which data can be transmitted continually between the nodes with a distance of order $O ( \mathfrak { k } )$ ; and we define the waiting interval it takes a packet to wait for the next transmission at a relay node.

# II.B. Classical Two-Hop Strategy

Two-hop strategy was first proposed by Grossglauser and Tse [2]. Under the two-hop strategy, for each packet ?? from session $k ,$ the complete relay path can be denoted by $\mathcal { P } _ { k , z } = \{ 1 _ { k , z } ^ { t _ { 1 } } , 2 _ { k , z } ^ { t _ { 2 } } \}$ . There are generally three phases under the two-hop strategy: (1) S→R phase, during which the source node $\mathbf { t } _ { 1 , k , z }$ transmits the packet ?? to a relay node $\mathbf { r } _ { 1 , k , z } , i . e . , \mathbf { t } _ { 2 , k , z } ; ( 2 )$ waiting phase, during which $\mathbf { r } _ { 1 , k , z }$ holds the packet ?? until it meet the destination node $\mathbf { r } _ { 2 , k , \ast }$ ?? within a distance of $\mathrm { I } _ { \mathbf { S } }$ , and (3) R→D phase, during which $\mathbf { r } _ { 1 , k , z }$ transmits the packet ?? to $\mathbf { r } _ { 2 , k , z }$ . Please see the illustration in Fig.2. Here, the duration of $\mathrm { S } {  } \mathrm { R }$ phase and R D phase is of the same order as the contact time with the parameter ??S; the duration of the waiting phase can be derived based on the first hitting time. S→R phase and R D phase are the contact intervals, and the waiting phase is the waiting interval.

# III. Main Results and Discussions

# III.A. Main Results

To the best of our knowledge, this work is first one to study the scaling laws for MANETs under the Gaussian Channel model in extended networks. We mainly focus on deriving the capacity and delay for the extended MANET under the well-known two-hop strategy without replications [2] that has been extensively studied under the protocol or physical models for dense networks.

Our scheme is a simple threshold-based method: when the distance between two nodes is at most a threshold ??S, these two nodes are requested to communicate directly; otherwise, they communicate via the two-hop relay strategy. Depending on this key parameter $u _ { \mathbf { S } } : [ 1 , \sqrt { n } ]$ , we derive the asymptotic capacity and delay bounds for both HRWMM and DRDMM as following:

![](images/be1eb4d206ac0b6339677169a1362d55836a9cc48327f562b2ac9cbce2ccedb4.jpg)



Figure 2: Decomposition of Two-Hop Communication. $L _ { \mathrm { c } }$ and $L _ { \mathrm { w } }$ denote the average duration of the contact intervals and waiting intervals, respectively. $L _ { \mathrm { s } }$ denotes the duration of static slots. Here, $L _ { \mathrm { p } } ^ { \mathrm { h } } =$ $L _ { \mathrm { s } } ~ = ~ 1$ and $L _ { \mathrm { p } } ^ { \mathrm { d } } = \Theta ( n ^ { \eta } ) , 0 \le \eta \le \frac { 1 } { 2 }$ =. Note that the contact intervals and waiting intervals always can be divided into static slots; under the HRWMM, they also can be divided into motion phases; while, under the DRDMM, they are not necessarily divided into motion phases due to the continuous motion of nodes.

Average Capacity: (H: HRWMM, D: DRDMM) 

<table><tr><td rowspan="2">H:</td><td>$ \Omega(\frac{\log n \cdot n^{2\varepsilon}}{(\mathfrak{l}_{\mathbf{S}})^{2}}) $, when $ \mathfrak{l}_{\mathbf{S}} : [n^{\varepsilon} \sqrt{\log n}, \sqrt{n}] $</td></tr><tr><td>$ \Theta(1) $, when $ \mathfrak{l}_{\mathbf{S}} : [1, n^{\varepsilon} \sqrt{\log n}] \cap [1, \sqrt{n}] $</td></tr><tr><td rowspan="3">D:</td><td>$ \Omega\left(\frac{\log n \cdot n^{\eta}}{(\mathfrak{l}_{\mathbf{S}})^{2}}\right) $, when $ \mathfrak{l}_{\mathbf{S}} : [n^{\eta} \sqrt{\log n}, \sqrt{n}] $</td></tr><tr><td>$ \Omega(\frac{1}{n^{\eta}}) $, when $ \mathfrak{l}_{\mathbf{S}} : [n^{\eta}, n^{\eta} \sqrt{\log n}] \cap [1, \sqrt{n}] $</td></tr><tr><td>$ \Omega(\frac{1}{\mathfrak{l}_{\mathbf{S}}}) $, when $ \mathfrak{l}_{\mathbf{S}} : [1, n^{\eta}] $.</td></tr></table>

Average Delay: (H: HRWMM, D: DRDMM) 

<table><tr><td>H:</td><td> $\Theta\left(\frac{n}{(l_{S})^{2}}+\frac{\log n}{n^{2\varepsilon-1}}\right)$ , when  $l_{S}:[1,n^{\varepsilon}]\cap[1,\sqrt{n})$ Lower bound  $\Omega(\frac{n^{1-2\varepsilon}}{\log n})$ , when  $l_{S}:[n^{\varepsilon},\sqrt{n})$ Upper bound  $O(\frac{n^{1-2\varepsilon}}{\log n}+1)$ , when  $l_{S}=\Theta(\sqrt{n})$ </td></tr><tr><td>D:</td><td> $\Theta\left(\frac{n}{(l_{S})^{2}}+\frac{\log n}{n^{\eta-1.}}\right)$ , when  $l_{S}:[1,n^{\eta}]\cap[1,\sqrt{n})$ Lower bound  $\Omega(\frac{n^{1-\eta}}{\log n})$ , when  $l_{S}:[n^{\eta},\sqrt{n})$ Upper bound  $O(\frac{n^{1-\eta}}{\log n})$ , when  $l_{S}=\Theta(\sqrt{n})$ </td></tr></table>

# III.B. Discussion of Results

Insights of Results for HRWMM: (1) Under the classical two-hop strategy, to achieve the capacity of order $\Theta ( 1 )$ for dense networks, the critical distance is set to be $\mathrm { ~ l ~ } _ { \mathbf { S } } = \Theta ( \frac { 1 } { \sqrt { n } } )$ [2]. Then, it is intuitive that by a simple scaling extension from dense networks to extended networks, i.e., by letting $\mathbf { \Lambda } | _ { \mathbf { S } } ~ = ~ \Theta ( 1 )$ , the capacity is achieved of order $\Theta ( 1 )$ . We first prove that the tight bound of $\mathrm { \Delta I _ { S } }$ deriving the capac-

ity of a constant order under the Gaussian Channel model is $\Theta ( \operatorname* { m i n } \{ n ^ { \varepsilon } \sqrt { \log n } , \sqrt { n } \} )$ (The feasible region is ${ \bf \tau } ( { \bf s } ~ : { \bf \tau } [ 1$ , $\{ n ^ { \varepsilon } { \sqrt { \log n } } , { \sqrt { n } } \} ] )$ . (2) For i.i.d mobility model, $i . e . ,$ , the case of $\begin{array} { r } { \varepsilon = \frac { 1 } { 2 } } \end{array}$ , a surprising result arises: the capacity and delay can be simultaneously achieved of order $\Theta ( 1 )$ under the setting of $\mathfrak { l } _ { \mathbf { S } } = \Theta ( \sqrt { n } )$ . Recall that under i.i.d mobility model the position of any node is independent of that in the adjacent time slots. That means that in the extended network the velocity of each node under i.i.d model is assumed to increase to infinity (of order $\Theta ( { \sqrt { n } } ) )$ . The specificity of i.i.d mobility model just contributes to this surprising result. (3) Furthermore, for the delay, in the first regime, i.e., ??S $: [ 1 , n ^ { \varepsilon } ] \cap [ 1 , { \sqrt { n } } )$ , by using the tight bound, we get that the delay is inversely proportional to $( \mathrm { [ _ { S } ) ^ { 2 } }$ when $\displaystyle \mathrm { I } _ { \mathbf { S } } : [ 1 , \frac { n ^ { \varepsilon } } { \sqrt { \log n } } ]$ ???? , and becomes invariable when ??S is beyond the threshold of order $\Theta \big ( \frac { n ^ { \varepsilon } } { \sqrt { \log n } } \big )$ . For the other two regimes, it is an interesting future work to derive tight bounds if they exist, which can possibly enhance the insights of the issue.

Insights of Results for DRDMM: (1) For the cases of $0 ~ < ~ \eta ~ \le ~ 1 / 2$ , including the random way-point mobility model, one has to let $\mathfrak { k } _ { \mathbf { S } } = \Theta ( 1 )$ in order to achieve the capacity of optimal order, $i . e . , \Theta ( 1 )$ . For the discrete Brownian mobility model, $i . e . .$ , the case of $\eta = 0$ , the capacity of optimal order can be achieved when $\mathbf { \Delta } [ \mathbf { { s } } : [ 1 , \sqrt { \log n } ]$ . (2) The bound on the delay is tight in the regime of $\mathfrak { l } _ { \mathbf { S } } : [ 1 , n ^ { \eta } ] \cap [ 1 , \sqrt { n } )$ . The delay : [1is inversely proportional to $( \mathrm { [ _ { S } ) ^ { 2 } }$ [1when $\mathfrak { l } _ { \mathbf { S } } : [ 1 , \frac { n ^ { \eta / 2 } } { \sqrt { \log n } } ] .$ ????/2 and becomes invariable when ??S is beyond the threshold of order $\Theta \big ( \frac { n ^ { \eta / 2 } } { \sqrt { \log n } } \big )$ ????/2

Common Insights for Both Models: The capacity is independent of the power attenuation exponent of Gaussian Channel model, although it decreases with ${ \bf \Delta } [ _ { \bf S }$ for some regimes. The reason for this phenomenon lies in the fact that when the link rate changes with the link length under Gaussian Channel model, the data transmitted via long-distance links are indeed infinitesimal relative to those via short links.

# References

[1] G. Sharma, R. Mazumdar, and N. Shroff, “Delay and capacity trade-offs in mobile ad hoc networks: A global perspective,” IEEE/ACM Trans. on Networking (TON), vol. 15, no. 5, pp. 981–992, 2007.   
[2] M. Grossglauser and D. Tse, “Mobility increases the capacity of ad hoc wireless networks,” IEEE/ACM Trans. on Networking, vol. 10, no. 4, pp. 477–486, 2002.